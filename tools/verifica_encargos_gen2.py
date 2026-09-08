#!/usr/bin/env python3
"""`tools/verifica_encargos_gen2.py` -- ACTO GEN2-PRE-E5 ·
CABLEADO-Y-AUTOMATIZACION-FINAL, P4.

Este defecto ya ocurrió una vez: dirección emitió una versión nueva de
`ENCARGOS-GEN2-v*.md` y los archivos de `forense/encargos/cola/` se
quedaron con el cuerpo de la versión anterior. Este verificador comprueba,
byte a byte, que cada encargo GEN2 ACTIVO en cola (`GATEADO`/`LISTO-*` --
todavía por ejecutar; `EN-CURSO`/`CONSUMIDO` quedan fuera de perímetro)
coincide con la sección que le corresponde de la versión maestra vigente
(`forense/notas/ENCARGOS-GEN2-v*-*.md` de versión numérica máxima presente
en el árbol -- se deriva, nunca se clava un nombre en el código).

No es un framework de despacho: chico y determinista a propósito.

Uso:
    python3 tools/verifica_encargos_gen2.py --verifica
    python3 tools/verifica_encargos_gen2.py --aplica <archivo-de-cola.md>

`--aplica` copia VERBATIM la sección correspondiente de la versión maestra
sobre el cuerpo del archivo de cola indicado -- reemplaza solo lo que sigue
a la línea delimitadora `CUERPO VERBATIM DEL ENCARGO`; la cabecera
`ESTADO`/`ENTORNO`/`ENCOLADO`/`BITACORA` no se toca. Sin decisiones: si el
archivo no es un encargo GEN2 reconocible, no hace nada y sale con error.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
COLA = RAIZ / "forense" / "encargos" / "cola"
NOTAS = RAIZ / "forense" / "notas"

RE_MASTER = re.compile(r"^ENCARGOS-GEN2-v(\d+)_(\d+)-.*\.md$")
RE_HEADING = re.compile(r"^## (\S+) · ACTO\b", re.M)
RE_CONTADOR_FIN = re.compile(r"^Contador:.*$", re.M)
DELIM_CUERPO = "CUERPO VERBATIM DEL ENCARGO"


def _sha256_texto(texto: str) -> str:
    import hashlib
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def version_maestra() -> Path | None:
    """La `ENCARGOS-GEN2-v*.md` de version maxima presente en el arbol --
    misma regla que `instrucciones_vigentes` en `tools/tablero_programa.py`:
    se deriva, nunca se clava un nombre en el codigo."""
    candidatos = []
    if NOTAS.exists():
        for f in NOTAS.glob("ENCARGOS-GEN2-v*-*.md"):
            m = RE_MASTER.match(f.name)
            if m:
                candidatos.append(((int(m.group(1)), int(m.group(2))), f))
    if not candidatos:
        return None
    return max(candidatos)[1]


def secciones_maestras(texto: str) -> dict[str, str]:
    """`{ID: sección}` de la versión maestra, una por cada `## <ID> · ACTO
    ...`. Una sección termina al final de su propia línea `Contador:` --
    convención que las cinco secciones de v1.5 y los cuerpos de cola ya
    comparten hoy; lo que sigue (separador `---`, epílogo del documento)
    no es parte del cuerpo del encargo."""
    posiciones = list(RE_HEADING.finditer(texto))
    finales_contador = [m.end() for m in RE_CONTADOR_FIN.finditer(texto)]
    secciones: dict[str, str] = {}
    for m in posiciones:
        inicio = m.start()
        fin = next((f for f in finales_contador if f > inicio), len(texto))
        secciones[m.group(1)] = texto[inicio:fin]
    return secciones


def cuerpo_de_cola(texto: str) -> str | None:
    """El CUERPO VERBATIM de un archivo de cola: todo lo que sigue a la
    línea delimitadora, hasta EOF o hasta una cabecera de cierre que el
    despachador sí puede añadir (`## NO-CORRIDO / RESERVAS` / `##
    CONSUMIDO`)."""
    idx = texto.find(DELIM_CUERPO)
    if idx == -1:
        return None
    salto = texto.find("\n", idx)
    resto = texto[salto + 1:] if salto != -1 else ""
    m = re.search(r"^## (NO-CORRIDO / RESERVAS|CONSUMIDO)\b", resto, re.M)
    if m:
        resto = resto[:m.start()]
    return resto.strip("\n")


def es_activo(texto: str) -> bool:
    """`GATEADO`/`LISTO-*` -- todavía por ejecutar. `EN-CURSO` y
    `CONSUMIDO` quedan fuera: ya arrancaron o ya cerraron, y no son lo que
    v1.5 reencola (P4.3: solo lo que TODAVÍA FALTA EJECUTAR)."""
    lineas = texto.splitlines()
    if not lineas or not lineas[0].startswith("ESTADO:"):
        return False
    estado = lineas[0][len("ESTADO:"):].strip()
    return estado.startswith("GATEADO") or estado.startswith("LISTO")


def id_de(texto_cuerpo: str) -> str | None:
    m = RE_HEADING.match(texto_cuerpo)
    return m.group(1) if m else None


def encargos_gen2_activos() -> list[Path]:
    if not COLA.exists():
        return []
    return [f for f in sorted(COLA.glob("*.md"))
            if "GEN2" in f.name and es_activo(f.read_text(encoding="utf-8"))]


def verifica() -> int:
    maestro = version_maestra()
    if maestro is None:
        print("PARO · ENCARGO-GEN2-DESFASADO", file=sys.stderr)
        print("  no existe ninguna `forense/notas/ENCARGOS-GEN2-v*.md` en el árbol",
              file=sys.stderr)
        return 1

    secciones = secciones_maestras(maestro.read_text(encoding="utf-8"))
    activos = encargos_gen2_activos()
    if not activos:
        print(f"SIN-ENCARGOS-GEN2-ACTIVOS (versión maestra: {maestro.name})")
        return 0

    fallos = 0
    for f in activos:
        cuerpo = cuerpo_de_cola(f.read_text(encoding="utf-8"))
        if cuerpo is None:
            print("PARO · ENCARGO-GEN2-DESFASADO", file=sys.stderr)
            print(f"  archivo: {f.relative_to(RAIZ)}", file=sys.stderr)
            print(f"  razón: no trae la línea delimitadora '{DELIM_CUERPO}'",
                  file=sys.stderr)
            fallos += 1
            continue
        ident = id_de(cuerpo)
        seccion = secciones.get(ident) if ident else None
        if seccion is None:
            print("PARO · ENCARGO-GEN2-DESFASADO", file=sys.stderr)
            print(f"  archivo: {f.relative_to(RAIZ)}", file=sys.stderr)
            print(f"  versión maestra: {maestro.relative_to(RAIZ)}", file=sys.stderr)
            print(f"  razón: no hay sección '## {ident} · ACTO' en la versión maestra",
                  file=sys.stderr)
            fallos += 1
            continue
        if cuerpo != seccion:
            print("PARO · ENCARGO-GEN2-DESFASADO", file=sys.stderr)
            print(f"  archivo: {f.relative_to(RAIZ)}", file=sys.stderr)
            print(f"  versión maestra: {maestro.relative_to(RAIZ)}", file=sys.stderr)
            print(f"  sección: {ident}", file=sys.stderr)
            print(f"  sha esperado:  {_sha256_texto(seccion)}", file=sys.stderr)
            print(f"  sha observado: {_sha256_texto(cuerpo)}", file=sys.stderr)
            fallos += 1
            continue
        print(f"OK · {f.relative_to(RAIZ)} == sección {ident} de {maestro.name}")
    return 1 if fallos else 0


def aplica(ruta_cola: str) -> int:
    f = Path(ruta_cola)
    if not f.is_absolute():
        f = RAIZ / ruta_cola
    if not f.exists():
        print(f"error: no existe {ruta_cola}", file=sys.stderr)
        return 1
    maestro = version_maestra()
    if maestro is None:
        print("error: no hay versión maestra ENCARGOS-GEN2 en el árbol", file=sys.stderr)
        return 1
    texto = f.read_text(encoding="utf-8")
    idx = texto.find(DELIM_CUERPO)
    if idx == -1:
        print(f"error: {ruta_cola} no trae la línea delimitadora '{DELIM_CUERPO}'",
              file=sys.stderr)
        return 1
    cuerpo_actual = cuerpo_de_cola(texto)
    ident = id_de(cuerpo_actual) if cuerpo_actual else None
    if ident is None:
        print(f"error: no se reconoce el id del encargo en {ruta_cola}", file=sys.stderr)
        return 1
    seccion = secciones_maestras(maestro.read_text(encoding="utf-8")).get(ident)
    if seccion is None:
        print(f"error: {maestro.name} no trae una sección '## {ident} · ACTO'",
              file=sys.stderr)
        return 1
    salto = texto.find("\n", idx)
    fin_delim = salto + 1 if salto != -1 else len(texto)
    nuevo = texto[:fin_delim] + "\n" + seccion + "\n"
    f.write_text(nuevo, encoding="utf-8")
    print(f"APLICADO · {ruta_cola} <- sección {ident} de {maestro.name} (verbatim)")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if "--verifica" in argv:
        return verifica()
    if "--aplica" in argv:
        i = argv.index("--aplica")
        if i + 1 >= len(argv):
            print("uso: verifica_encargos_gen2.py --aplica <archivo-de-cola.md>",
                  file=sys.stderr)
            return 2
        return aplica(argv[i + 1])
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
