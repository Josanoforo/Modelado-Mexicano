#!/usr/bin/env python3
"""Qué tipo de merge es este PR, derivado de su diff.

ACTO `GEN2-TUBERIA-ENRUTAMIENTO-PR-1`, P1. Firma de mesa 20/sep/2026
(Opción B: taxonomía de PR + regla de enrutamiento derivada del diff y
verificable en CI).

El defecto REAL que atrapa (§1: el aparato tiene costo)
=======================================================
El merge de mesa ADOPTA cifras sin que el PR lo diga. Por E.2, «el merge
del PR que trae un bloque ES la adopción»; por la firma del 17/sep/2026,
«un piso no vencido es el estimador adjudicado de su celda y se adopta
salvo veto de mesa». En la revisión del `PR #943` -- 2 939 resultados
sellados -- eso no estaba escrito en ninguna parte del PR: hubo que
deducirlo del diff. Medido sobre los 198 PR fusionados a `main` en los 7
días previos al 21/sep/2026, uno de cada cinco merges fue una adopción y
ninguno lo anunciaba.

Qué hace y qué NO hace
======================
Dado un diff -- lista de archivos con su estado -- devuelve:

  1. TODAS las señales que dispara, no sólo una: un PR puede adoptar y
     tocar aparato a la vez, y colapsarlas a una pierde la mitad.
  2. La CLASE PRINCIPAL, por precedencia ADOPTA > FIRMA > APARATO >
     REVISIÓN.
  3. La INSTRUCCIÓN DE ENRUTAMIENTO de esa clase, en una línea que mesa
     lea sin abrir el diff.

**La clase informa, no adjudica (D-16).** Esta herramienta NO falla por
la clase: sale con 0 clasifique lo que clasifique. Sólo sale distinto de
0 si no puede LEER el diff -- que es un defecto de la herramienta, no del
PR. No fusiona, no etiqueta, no bloquea, no decide nada por mesa.

Las rutas viven en `SEÑALES`, aquí y en ningún otro sitio (D-15): un
parámetro no vive en dos lugares, y cada ruta lleva la línea que dice por
qué dispara.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

# --- La tabla. Un solo sitio (D-15). -----------------------------------
# Cada entrada: (patrón regex sobre la ruta, por qué dispara).
# El orden dentro de cada señal no importa; el de las señales sí (abajo).

SEÑALES: dict[str, dict[str, object]] = {
    "ADOPTA": {
        "precedencia": 0,
        "rutas": [
            (
                r"^data/corrida0/CALC-[^/]+/sello\.json$",
                "un sello de CALC que entra con el merge ES la adopción de "
                "esa corrida (E.2): el merge no es un trámite, es la firma",
            ),
        ],
    },
    "FIRMA": {
        "precedencia": 1,
        "rutas": [
            (
                r"^milpa/",
                "superficie de firma de mesa: lo que vive en `milpa/` se "
                "decide, no se deriva",
            ),
            (
                r"^data/corrida0/decisiones\.tsv$",
                "el registro de decisiones de mesa: una fila nueva aquí es "
                "una decisión tomada",
            ),
            (
                r"^data/corrida0/CALC-[^/]+/spec\.yaml$",
                "la spec de un CALC es el contrato ejecutable normativo "
                "(D-15); tocarla cambia qué se mide",
            ),
        ],
    },
    "APARATO": {
        "precedencia": 2,
        "rutas": [
            (
                r"^\.claude/commands/",
                "las skills son el vehículo de todo acto (D-10): un cambio "
                "aquí cambia cómo corren TODOS los actos siguientes",
            ),
            (
                r"^\.github/workflows/",
                "CI es quien verifica; un cambio aquí cambia qué se verifica",
            ),
            (
                r"^tools/cierre_acto\.py$",
                "la cascada de cierre de todo acto (D-10)",
            ),
            (
                r"^tools/corrida0\.py$",
                "el contador derivado y el sellado de corridas (E.4)",
            ),
            (
                r"^tests/check\.py$",
                "la suite que adjudica por FAIL (D-16)",
            ),
            (
                r"^\.gitattributes$",
                "cómo git ve los archivos: un filtro mal puesto altera "
                "silenciosamente lo que la suite lee",
            ),
        ],
    },
}

# Precedencia explícita, de mayor a menor. REVISIÓN es el resto.
PRECEDENCIA = ["ADOPTA", "FIRMA", "APARATO", "REVISIÓN"]

# `git diff --name-status` marca los renombres como `R100 viejo nuevo`.
# Un archivo RENOMBRADO A una ruta que dispara cuenta: la ruta nueva es la
# que existe tras el merge. Un borrado (`D`) también cuenta -- borrar el
# sello de un CALC no es menos grave que añadirlo.
_ESTADO = re.compile(r"^([ACDMRTUX])(\d*)\t(.*)$")


def rutas_de_name_status(texto: str) -> list[tuple[str, str]]:
    """De `git diff --name-status -z`-menos-el-z a [(estado, ruta)].

    Para un renombre `R100\tviejo\tnuevo` devuelve la ruta NUEVA, que es la
    que existirá en `main` tras el merge.
    """
    pares: list[tuple[str, str]] = []
    for linea in texto.splitlines():
        if not linea.strip():
            continue
        m = _ESTADO.match(linea)
        if not m:
            # Sin estado (p. ej. `--name-only`): la línea entera es la ruta.
            pares.append(("?", linea.strip()))
            continue
        estado, _pct, resto = m.group(1), m.group(2), m.group(3)
        campos = resto.split("\t")
        ruta = campos[-1] if estado in ("R", "C") and len(campos) > 1 else campos[0]
        pares.append((estado, ruta))
    return pares


def clasifica(rutas: list[str]) -> dict:
    """Señales disparadas, clase principal y enrutamiento. Nunca lanza."""
    disparos: dict[str, list[tuple[str, str]]] = {}
    for señal, cfg in SEÑALES.items():
        for patron, porque in cfg["rutas"]:  # type: ignore[index]
            rx = re.compile(patron)
            for ruta in rutas:
                if rx.search(ruta):
                    disparos.setdefault(señal, []).append((ruta, porque))

    señales = [s for s in PRECEDENCIA if s in disparos]
    clase = señales[0] if señales else "REVISIÓN"

    # Los CALC que este diff adopta, contados del diff -- no tecleados.
    calc = sorted(
        {
            m.group(1)
            for ruta, _ in disparos.get("ADOPTA", [])
            if (m := re.search(r"^data/corrida0/(CALC-[^/]+)/sello\.json$", ruta))
        }
    )

    return {
        "clase": clase,
        "señales": señales,
        "disparos": disparos,
        "calc_adoptados": calc,
        "n_archivos": len(rutas),
        "enrutamiento": enrutamiento(clase, disparos, calc),
    }


def enrutamiento(clase: str, disparos: dict, calc: list[str]) -> str:
    """La línea que mesa lee sin abrir el diff."""
    if clase == "ADOPTA":
        n = len(calc)
        plural = "corrida sellada" if n == 1 else "corridas selladas"
        return (
            f"Tu merge adopta {n} {plural} (E.2): comprueba su asiento de "
            f"replay y, si son pisos, ésta es tu ventana de veto. "
            f"CALC: {', '.join(calc)}"
        )
    if clase == "FIRMA":
        archivos = sorted({r for r, _ in disparos.get("FIRMA", [])})
        return (
            "Toca superficie de firma de mesa: el PR debe citar la firma "
            f"verbatim. Archivos: {', '.join(archivos)}"
        )
    if clase == "APARATO":
        archivos = sorted({r for r, _ in disparos.get("APARATO", [])})
        return (
            "Cambia el aparato: la suite en verde y el perímetro del encargo "
            f"son la revisión. Archivos: {', '.join(archivos)}"
        )
    return "Revisión ordinaria."


def markdown(res: dict, titulo: str = "Enrutamiento de este PR") -> str:
    """El resumen para `GITHUB_STEP_SUMMARY`. Sin colores, sin adornos."""
    L = [f"## {titulo}", ""]
    L.append(f"**Clase: `{res['clase']}`**  ·  {res['n_archivos']} archivo(s) en el diff")
    L.append("")
    L.append(f"> {res['enrutamiento']}")
    L.append("")
    if res["señales"]:
        L.append(f"Señales disparadas (todas, por precedencia): "
                 f"{' > '.join(f'`{s}`' for s in res['señales'])}")
        L.append("")
        L.append("| Señal | Archivo | Por qué dispara |")
        L.append("|---|---|---|")
        for señal in res["señales"]:
            for ruta, porque in res["disparos"][señal]:
                L.append(f"| `{señal}` | `{ruta}` | {porque} |")
    else:
        L.append("Ninguna señal disparada: revisión ordinaria.")
    L.append("")
    L.append(
        "_La clase informa, no adjudica (D-16): este job no falla por la "
        "clase y no bloquea el merge. El merge es de mesa._"
    )
    return "\n".join(L) + "\n"


def _diff_de_git(base: str, cabeza: str) -> str:
    return subprocess.run(
        ["git", "diff", "--name-status", "-M", f"{base}...{cabeza}"],
        cwd=RAIZ, capture_output=True, text=True, check=True,
    ).stdout


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--base", help="ref base (por defecto origin/main)")
    p.add_argument("--cabeza", default="HEAD", help="ref cabeza")
    p.add_argument("--diff", help="archivo con salida de `git diff --name-status` ('-' = stdin)")
    p.add_argument("--resumen", help="escribe el markdown a este archivo (además de stdout)")
    a = p.parse_args(argv)

    try:
        if a.diff:
            texto = sys.stdin.read() if a.diff == "-" else Path(a.diff).read_text(encoding="utf-8")
        else:
            texto = _diff_de_git(a.base or "origin/main", a.cabeza)
    except Exception as exc:  # noqa: BLE001 -- único fallo legítimo (P1)
        print(f"NO-PUDE-LEER-EL-DIFF: {exc}", file=sys.stderr)
        return 2

    rutas = [r for _, r in rutas_de_name_status(texto)]
    res = clasifica(rutas)
    md = markdown(res)
    print(md)
    if a.resumen:
        with open(a.resumen, "a", encoding="utf-8") as fh:
            fh.write(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
