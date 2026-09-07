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
"""
import argparse
import hashlib
import os
import re
import sys
import tempfile

_SIDECAR_RE = re.compile(r"^([0-9a-f]{64})  ([^\n]+)\n$")


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


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Sella o verifica el sidecar sha256 hermano de un archivo explícito."
    )
    ap.add_argument("--verifica", action="store_true",
                     help="verifica el sidecar existente; nunca escribe")
    ap.add_argument("archivo", help="ruta al archivo fuente (nunca un .sha256, nunca un directorio)")
    args = ap.parse_args(argv)

    if args.verifica:
        codigo, mensaje = verifica(args.archivo)
    else:
        codigo, mensaje = sella(args.archivo)
    print(mensaje)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
