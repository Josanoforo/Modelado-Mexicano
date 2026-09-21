#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/sella_sha256.py -- sella o verifica el sidecar sha256 de un
archivo pasado explícitamente (ACTO AUTOMATIZA-2-C · SELLA-SIDECAR,
`forense/encargos/2026-09-07-AUTOMATIZA-2-C-SELLA-SIDECAR.md`).

QUÉ ES Y QUÉ NO ES. Un sellador/verificador de sidecars hermanos, uno
archivo a la vez, siempre pasado por el llamador -- nunca descubre nada
por su cuenta: sin glob, sin caminar directorios, sin sellado recursivo,
sin timestamps, sin YAML, sin registry de hashes, sin firmas, sin Git, sin
decidir si una modificación está autorizada. No se integra globalmente a
`/acto`: que el cierre reselle un archivo no vuelve aceptable un cambio
accidental en una spec.

Convención del sidecar (specs congeladas de `forense/prereg-caja/`): el
sidecar sustituye SÓLO la última extensión del archivo fuente --
`S7-L17-spec-v1_1.md` -> `S7-L17-spec-v1_1.sha256`, equivalente conceptual
a `Path.with_suffix(".sha256")`. Nunca se concatena `.sha256` al nombre
completo (`S7-L17-spec-v1_1.md.sha256` es la convención que ESTE tool no
usa).

Formato del sidecar, una línea:
    <64-hex-minúsculas><dos espacios><basename>\n
mismo formato que produce `sha256sum` de la casa. El hash se calcula
sobre los bytes exactos del archivo fuente.

Sellado -- escribe (temporal en el mismo directorio + `os.replace()`,
atómico):
    python3 tools/sella_sha256.py <archivo>

Verificación -- SIEMPRE de sólo lectura, nunca escribe. Valida el
CONTENIDO COMPLETO del sidecar contra el contrato exacto de arriba --
una segunda línea, bytes tras el `\n`, o la ausencia del `\n` final
son SELLO_NO_COINCIDE tanto como un hash o basename distinto:
    python3 tools/sella_sha256.py --verifica <archivo>
Tres resultados, tres exit codes:
    0  SELLO_COINCIDE        -- sidecar presente y coincide
    2  SIDECAR_AUSENTE       -- no hay sidecar (no es lo mismo que discordar)
    3  SELLO_NO_COINCIDE     -- sidecar presente, hash o formato no coincide

Rechazos de entrada (exit != 0, sin sellar ni verificar nada):
    - la fuente termina en `.sha256` (evita sellar un sidecar como si
      fuera el archivo fuente)
    - la fuente es un directorio (no se trata como lote implícito)

MODO `--cuerpo` -- el sello de un encargo cubre su CUERPO
====================================================================
(ACTO GEN2-TUBERIA-SIDECAR-CUERPO-1, 21/sep/2026; firmas de mesa D-a1,
D-a2, D-a3, D-a5.) El modo de arriba no cambia: `tools/corrida0.py` y
`tests/check.py` lo importan y siguen viendo exactamente lo mismo.

El defecto que este modo atrapa es concreto: el sello del 0-bis de un
encargo dejaba de casar en cuanto el propio acto le añadía su sección de
cierre (`## NO-CORRIDO / RESERVAS`, `## CONSUMIDO`), y el remedio
practicado --re-sellar al cerrar-- destruye la única evidencia de que el
cuerpo del encargo no se tocó. Este modo sella el CUERPO: lo que el
encargo pidió, no lo que el ejecutor añadió después.

  * Normalización N(texto) (D-a1), idéntica al sellar y al verificar: se
    quita al final todo blanco y toda línea de solo `---`, y se termina
    en exactamente un salto de línea.
  * CANDIDATOS al verificar (D-a2 + D-a5): el prefijo anterior a CADA
    línea que empieza en `^## `, más el archivo entero. Pasa si alguno,
    normalizado, casa con el sidecar. Sin centinela: el hash desambigua
    solo, y un encargo con dos líneas `## NO-CORRIDO` no obliga a
    escoger delimitador. La verificación REPORTA cuál candidato casó.
  * WARN, no FAIL (D-a5): si lo que sigue al cuerpo sellado abre con un
    encabezado distinto de `## NO-CORRIDO` o `## CONSUMIDO`, el sello
    pasa y se emite `WARN_ENCABEZADO_AJENO`. Una adenda pegada al final
    pasa el sello del cuerpo, pero no pasa inadvertida (D-16: los WARN
    se listan, no adjudican).
  * Sidecar propio (D-a3): `X.cuerpo.sha256` -- sufijo CONCATENADO al
    nombre completo, no `with_suffix`. El nombre dice que `sha256sum -c`
    no es su verificador. Un solo formato, el mismo que el modo de
    arriba: `<64-hex><dos espacios><basename de la fuente>\n`.
  * ESTE SELLO NO SE REGENERA NUNCA: ni al cierre, ni tras una
    renumeración, ni para que un verificador pase. Vale la advertencia
    del 7/sep de este mismo módulo -- que el cierre reselle un archivo
    no vuelve aceptable un cambio accidental. Nace en el 0-bis y ahí se
    queda.

    python3 tools/sella_sha256.py --cuerpo <archivo>
    python3 tools/sella_sha256.py --cuerpo --verifica <archivo>

Mismos tres resultados y mismos tres exit codes (0 / 2 / 3).
"""
import argparse
import hashlib
import os
import re
import sys
import tempfile

_SIDECAR_RE = re.compile(r"^([0-9a-f]{64})  ([^\n]+)\n$")

SUFIJO_CUERPO = ".cuerpo.sha256"

# Los dos encabezados que un cierre de `/acto` puede abrir legítimamente
# después del cuerpo sellado (paso 10 y paso 11 de la skill). Cualquier
# otro es WARN, nunca FAIL.
_ENCABEZADOS_DE_CIERRE = ("## NO-CORRIDO", "## CONSUMIDO")


def _ruta_sidecar(ruta_fuente):
    """Sustituye SÓLO la última extensión -- equivalente a
    Path(ruta_fuente).with_suffix('.sha256'), sin concatenar."""
    raiz, _ext = os.path.splitext(ruta_fuente)
    return raiz + ".sha256"


def _sha256_de(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def _linea_sidecar(hash_hex, basename):
    return f"{hash_hex}  {basename}\n"


def _valida_entrada(ruta_fuente):
    """Devuelve None si la entrada es válida; si no, un mensaje de error."""
    if ruta_fuente.endswith(".sha256"):
        return f"RECHAZADO: la fuente termina en .sha256 ({ruta_fuente}) -- no se sella un sidecar"
    if os.path.isdir(ruta_fuente):
        return f"RECHAZADO: {ruta_fuente} es un directorio -- no se trata como lote implícito"
    if not os.path.exists(ruta_fuente):
        return f"RECHAZADO: {ruta_fuente} no existe"
    return None


def sella(ruta_fuente):
    """Escribe el sidecar. Devuelve (codigo, mensaje)."""
    error = _valida_entrada(ruta_fuente)
    if error:
        return 1, error

    basename = os.path.basename(ruta_fuente)
    hash_hex = _sha256_de(ruta_fuente)
    contenido = _linea_sidecar(hash_hex, basename)
    ruta_sidecar = _ruta_sidecar(ruta_fuente)

    directorio = os.path.dirname(ruta_sidecar) or "."
    fd, ruta_tmp = tempfile.mkstemp(dir=directorio, prefix=".sella_sha256-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(contenido)
        os.replace(ruta_tmp, ruta_sidecar)
    except BaseException:
        try:
            os.remove(ruta_tmp)
        except OSError:
            pass
        raise

    return 0, f"SELLADO\nfuente={ruta_fuente}\nsidecar={ruta_sidecar}\nsha256={hash_hex}"


def verifica(ruta_fuente):
    """Sólo lectura -- nunca escribe. Devuelve (codigo, mensaje)."""
    error = _valida_entrada(ruta_fuente)
    if error:
        return 1, error

    ruta_sidecar = _ruta_sidecar(ruta_fuente)
    if not os.path.exists(ruta_sidecar):
        return 2, f"SIDECAR_AUSENTE\nfuente={ruta_fuente}\nsidecar={ruta_sidecar}"

    with open(ruta_sidecar, encoding="utf-8") as f:
        contenido = f.read()

    basename = os.path.basename(ruta_fuente)
    m = _SIDECAR_RE.fullmatch(contenido)
    if not m:
        return 3, (
            "SELLO_NO_COINCIDE\n"
            f"fuente={ruta_fuente}\nsidecar={ruta_sidecar}\n"
            f"diagnostico=formato de sidecar irreconocible: {contenido!r}"
        )
    hash_esperado, basename_sidecar = m.group(1), m.group(2)
    hash_real = _sha256_de(ruta_fuente)

    if basename_sidecar != basename:
        return 3, (
            "SELLO_NO_COINCIDE\n"
            f"fuente={ruta_fuente}\nsidecar={ruta_sidecar}\n"
            f"diagnostico=basename no coincide: sidecar cita {basename_sidecar!r}, "
            f"se pidió {basename!r}"
        )

    if hash_esperado != hash_real:
        return 3, (
            "SELLO_NO_COINCIDE\n"
            f"fuente={ruta_fuente}\nsidecar={ruta_sidecar}\n"
            f"esperado={hash_esperado}\nreal={hash_real}"
        )

    return 0, f"SELLO_COINCIDE\nfuente={ruta_fuente}\nsidecar={ruta_sidecar}\nsha256={hash_real}"


# --------------------------------------------------------------------
# MODO --cuerpo (D-a1 · D-a2 · D-a3 · D-a5)
# --------------------------------------------------------------------

def ruta_sidecar_cuerpo(ruta_fuente):
    """`X` -> `X.cuerpo.sha256`. CONCATENA -- no sustituye extensión,
    a diferencia de `_ruta_sidecar`. El nombre es parte del contrato
    (D-a3)."""
    return ruta_fuente + SUFIJO_CUERPO


def normaliza_cuerpo(texto):
    """N(texto) de D-a1: quita al final todo blanco y toda línea de solo
    `---`, y termina en exactamente un salto de línea.

    El bucle es necesario: `---` seguido de blancos seguido de otro
    `---` es un final que hay que pelar entero, no por una sola capa."""
    while True:
        podado = texto.rstrip()
        lineas = podado.split("\n")
        if lineas and lineas[-1].strip() == "---":
            podado = "\n".join(lineas[:-1])
        if podado == texto:
            break
        texto = podado
    return texto + "\n"


def candidatos_cuerpo(texto):
    """Devuelve [(etiqueta, texto_candidato, encabezado_siguiente)] en
    orden: un candidato por cada línea `^## ` (el prefijo ANTERIOR a
    ella), y al final el archivo entero.

    `encabezado_siguiente` es la línea `## …` con la que abre lo que
    queda fuera del candidato, o None para el archivo entero."""
    lineas = texto.split("\n")
    candidatos = []
    desplazamiento = 0
    for indice, linea in enumerate(lineas):
        if linea.startswith("## "):
            etiqueta = "prefijo-antes-de-linea-{}: {}".format(indice + 1, linea.strip())
            candidatos.append((etiqueta, texto[:desplazamiento], linea.strip()))
        desplazamiento += len(linea) + 1  # +1 por el "\n" que `split` quitó
    candidatos.append(("archivo-entero", texto, None))
    return candidatos


def _lee_texto(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def _sha256_de_texto(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def sella_cuerpo(ruta_fuente):
    """Sella N(archivo entero). En el 0-bis el cuerpo ES el archivo
    entero: no hay cierre todavía. Devuelve (codigo, mensaje)."""
    error = _valida_entrada(ruta_fuente)
    if error:
        return 1, error

    basename = os.path.basename(ruta_fuente)
    cuerpo = normaliza_cuerpo(_lee_texto(ruta_fuente))
    hash_hex = _sha256_de_texto(cuerpo)
    ruta_sidecar = ruta_sidecar_cuerpo(ruta_fuente)

    directorio = os.path.dirname(ruta_sidecar) or "."
    fd, ruta_tmp = tempfile.mkstemp(dir=directorio, prefix=".sella_sha256-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(_linea_sidecar(hash_hex, basename))
        os.replace(ruta_tmp, ruta_sidecar)
    except BaseException:
        try:
            os.remove(ruta_tmp)
        except OSError:
            pass
        raise

    return 0, (
        "SELLADO_CUERPO\n"
        f"fuente={ruta_fuente}\nsidecar={ruta_sidecar}\nsha256={hash_hex}\n"
        "aviso=este sello no se regenera nunca: ni al cierre, ni tras una "
        "renumeración, ni para que un verificador pase"
    )


def verifica_cuerpo(ruta_fuente):
    """Sólo lectura. Devuelve (codigo, mensaje). El mensaje nombra el
    candidato que casó y, si aplica, emite `WARN_ENCABEZADO_AJENO`."""
    error = _valida_entrada(ruta_fuente)
    if error:
        return 1, error

    ruta_sidecar = ruta_sidecar_cuerpo(ruta_fuente)
    if not os.path.exists(ruta_sidecar):
        return 2, f"SIDECAR_AUSENTE\nfuente={ruta_fuente}\nsidecar={ruta_sidecar}"

    contenido = _lee_texto(ruta_sidecar)
    basename = os.path.basename(ruta_fuente)
    m = _SIDECAR_RE.fullmatch(contenido)
    if not m:
        return 3, (
            "SELLO_NO_COINCIDE\n"
            f"fuente={ruta_fuente}\nsidecar={ruta_sidecar}\n"
            f"diagnostico=formato de sidecar irreconocible: {contenido!r}"
        )
    hash_esperado, basename_sidecar = m.group(1), m.group(2)
    if basename_sidecar != basename:
        return 3, (
            "SELLO_NO_COINCIDE\n"
            f"fuente={ruta_fuente}\nsidecar={ruta_sidecar}\n"
            f"diagnostico=basename no coincide: sidecar cita {basename_sidecar!r}, "
            f"se pidió {basename!r}"
        )

    texto = _lee_texto(ruta_fuente)
    examinados = 0
    for etiqueta, candidato, encabezado in candidatos_cuerpo(texto):
        examinados += 1
        if _sha256_de_texto(normaliza_cuerpo(candidato)) != hash_esperado:
            continue
        lineas = [
            "SELLO_COINCIDE",
            f"fuente={ruta_fuente}",
            f"sidecar={ruta_sidecar}",
            f"sha256={hash_esperado}",
            f"candidato={etiqueta}",
        ]
        if encabezado is not None and not encabezado.startswith(_ENCABEZADOS_DE_CIERRE):
            lineas.append(
                "WARN_ENCABEZADO_AJENO=lo que sigue al cuerpo sellado abre con "
                f"{encabezado!r}, no con '## NO-CORRIDO' ni '## CONSUMIDO' "
                "(D-a5: se lista, no adjudica)"
            )
        return 0, "\n".join(lineas)

    return 3, (
        "SELLO_NO_COINCIDE\n"
        f"fuente={ruta_fuente}\nsidecar={ruta_sidecar}\n"
        f"esperado={hash_esperado}\n"
        f"diagnostico=ningún candidato normalizado casa; candidatos examinados={examinados}"
    )


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Sella o verifica el sidecar sha256 hermano de un archivo explícito."
    )
    ap.add_argument("--verifica", action="store_true",
                     help="verifica el sidecar existente; nunca escribe")
    ap.add_argument("--cuerpo", action="store_true",
                     help="modo cuerpo de encargo: sidecar `X.cuerpo.sha256`, "
                          "normalización N y candidatos por hash (D-a1/D-a2/D-a5)")
    ap.add_argument("archivo", help="ruta al archivo fuente (nunca un .sha256, nunca un directorio)")
    args = ap.parse_args(argv)

    if args.cuerpo:
        codigo, mensaje = (verifica_cuerpo if args.verifica else sella_cuerpo)(args.archivo)
    elif args.verifica:
        codigo, mensaje = verifica(args.archivo)
    else:
        codigo, mensaje = sella(args.archivo)
    print(mensaje)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
