#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/verifica_sidecars.py -- recorre los sidecars sha256 de
`forense/encargos/` y `forense/notas/` y reporta, sin colapsar, en qué
estado está cada uno (ACTO GEN2-TUBERIA-SIDECAR-CUERPO-1, 21/sep/2026;
firma de mesa D-a4).

QUÉ ES Y QUÉ NO ES. Un verificador de SÓLO LECTURA sobre dos
directorios nombrados. **Nunca escribe, nunca reescribe, nunca
normaliza ningún sidecar** -- ni los viejos ni los nuevos. No se
extiende a los 261 sidecars del árbol: ese alcance no está firmado.

POR QUÉ NO BASTA `sha256sum -c`. Medido el 21/sep/2026 sobre los 261
sidecars versionados: `sha256sum -c` ingenuo da 21 negativos, 17 de
ellos FALSAS ALARMAS DE FORMATO -- el sidecar está bien, el lector no
entiende cómo cita a su objetivo. Un verificador que grita 17 veces en
falso no lo lee nadie y deja pasar los 4 negativos reales. Por eso este
tool entiende EN LECTURA los tres formatos que el repo ya tiene:

    (1) `<hash>  <basename>`  -- relativo al directorio del sidecar
    (2) `<hash>  <ruta>`      -- relativa a la raíz del repo
    (3) `<hash>` pelado       -- contra el archivo hermano

y las dos convenciones de nombre que conviven: `X.sha256` (sustituye la
última extensión) y `X.md.sha256` (concatena). Los sidecars NUEVOS
nacen en un solo formato: `X.cuerpo.sha256`, `<hash>  <basename>`.

CUATRO ESTADOS QUE NO SE COLAPSAN (A.4):
    CASA              -- el objetivo existe y el hash coincide
    NO-CASA           -- el objetivo existe y el hash NO coincide
    HUÉRFANO          -- el sidecar cita un objetivo que no está
    TESTIGO           -- sidecar declarado histórico: no adjudica

QUÉ ADJUDICA (D-16: los WARN se listan, no adjudican):
    FAIL  -- todo `.cuerpo.sha256` que no case o quede huérfano, y todo
             sidecar viejo NO-CASA/HUÉRFANO que no esté declarado
             testigo. El sello de cuerpo es nuevo: no tiene historia
             que lo excuse.
    WARN  -- `WARN_ENCABEZADO_AJENO` de `sella_sha256 --cuerpo`: lo que
             sigue al cuerpo sellado abre con un encabezado distinto de
             `## NO-CORRIDO` o `## CONSUMIDO` (una adenda pegada al
             final pasa el sello, pero no pasa inadvertida).

Uso:
    python3 tools/verifica_sidecars.py            # sobre el repo
    python3 tools/verifica_sidecars.py --raiz DIR # sobre otra raíz
Exit: 0 sin FAIL · 1 con al menos un FAIL.
"""
import argparse
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sella_sha256  # noqa: E402

DIRECTORIOS = ("forense/encargos", "forense/notas")

# Sidecars viejos cuyo desajuste está DECLARADO y no adjudica. La
# declaración vive aquí, en el código que la usa, y cita su motivo: un
# testigo sin motivo escrito es un FAIL silenciado.
#
# A.10 -- un sello cuyo universo cambió queda VENCIDO EN ALCANCE: no
# refutado, no borrado, no vigente. Se reactiva por RE-SELLO (el
# `.cuerpo.sha256` hermano), nunca editando el viejo.
TESTIGOS_DECLARADOS = {
    "forense/notas/ENCARGOS-GEN2-v1_5-aparato-antes-de-calcular-2026-09-08.sha256": (
        "TESTIGO VENCIDO EN ALCANCE (A.10) -- casa con la versión de `7c6042e4` "
        "(8/sep/2026); la nota se editó después en `cf904d60` (15/sep, ACTO "
        "GEN2-MANTENIMIENTO-Y-ARCHIVO-2, NC-0050 CERRADA). Firma de mesa "
        "`ENCARGOS-GEN2-v1_5`, 21/sep/2026: no se edita, no se borra, no se "
        "revierte el texto; el re-sello vive en el `.cuerpo.sha256` hermano."
    ),
    "forense/notas/insumos-externos/pisos-enif2021-0002-rama-codex/"
    "pisos-enif2021-0002-codex-2026-09-20-sello.sha256": (
        "HUÉRFANO DECLARADO -- el sidecar cita `sello.json` a secas; el archivo "
        "que está junto a él se llama "
        "`pisos-enif2021-0002-codex-2026-09-20-sello.json`. Es un insumo externo "
        "recibido tal cual: no se toca (ACTO GEN2-TUBERIA-SIDECAR-CUERPO-1, P-h)."
    ),
}

_LINEA_RE = re.compile(r"^([0-9a-f]{64})(?:[ \t]+[*]?([^\n]+))?[ \t]*$")

CASA = "CASA"
NO_CASA = "NO-CASA"
HUERFANO = "HUÉRFANO"
TESTIGO = "TESTIGO"


def _sha256_bytes(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def _lee_primera_linea_util(ruta):
    with open(ruta, encoding="utf-8", errors="replace") as f:
        for linea in f:
            if linea.strip():
                return linea.rstrip("\n")
    return ""


def _objetivos_candidatos(ruta_sidecar, raiz, referencia):
    """Rutas donde el objetivo citado puede estar, en orden. Cubre los
    tres formatos de lectura."""
    directorio = os.path.dirname(ruta_sidecar)
    candidatos = []
    if referencia:
        # Formatos (1) y (2). Si el sidecar CITA un nombre, se le toma la
        # palabra: no se cae al hermano. Un sidecar que cita `sello.json`
        # y tiene junto a él un `…-sello.json` con el hash correcto es una
        # CITA ROTA, no un acierto -- resolverlo por parecido convertiría
        # un huérfano real en un CASA y taparía justo lo que se busca.
        candidatos.append(os.path.join(directorio, referencia))   # formato (1)
        candidatos.append(os.path.join(raiz, referencia))         # formato (2)
    else:
        # Formato (3): hash pelado contra el archivo hermano, en las dos
        # convenciones de nombre que conviven.
        sin_sufijo = ruta_sidecar[: -len(".sha256")]
        candidatos.append(sin_sufijo)                             # `X.md.sha256` -> `X.md`
        for ext in (".md", ".yaml", ".json", ".txt", ".py", ".tsv"):
            candidatos.append(sin_sufijo + ext)                   # `X.sha256`    -> `X.md`
    vistos, unicos = set(), []
    for c in candidatos:
        c = os.path.normpath(c)
        if c not in vistos:
            vistos.add(c)
            unicos.append(c)
    return unicos


def _verifica_viejo(ruta_sidecar, raiz):
    linea = _lee_primera_linea_util(ruta_sidecar)
    m = _LINEA_RE.match(linea)
    if not m:
        return NO_CASA, None, f"formato de sidecar irreconocible: {linea!r}", []
    hash_esperado, referencia = m.group(1), (m.group(2) or "").strip()

    for objetivo in _objetivos_candidatos(ruta_sidecar, raiz, referencia):
        if os.path.isfile(objetivo):
            real = _sha256_bytes(objetivo)
            rel = os.path.relpath(objetivo, raiz)
            if real == hash_esperado:
                return CASA, rel, f"formato leído: cita {referencia!r}" if referencia else "formato leído: hash pelado", []
            return NO_CASA, rel, f"esperado={hash_esperado} real={real}", []
    return HUERFANO, None, f"objetivo citado {referencia!r} no está junto al sidecar ni en la raíz", []


def _verifica_cuerpo(ruta_sidecar, raiz):
    objetivo = ruta_sidecar[: -len(sella_sha256.SUFIJO_CUERPO)]
    if not os.path.isfile(objetivo):
        return HUERFANO, None, "el archivo que el sello de cuerpo cubre no existe", []
    codigo, mensaje = sella_sha256.verifica_cuerpo(objetivo)
    rel = os.path.relpath(objetivo, raiz)
    detalle, warns = [], []
    for linea in mensaje.split("\n"):
        if linea.startswith("WARN_"):
            warns.append(linea)
        elif linea.startswith(("candidato=", "diagnostico=", "esperado=")):
            detalle.append(linea)
    return (CASA if codigo == 0 else NO_CASA), rel, " · ".join(detalle), warns


def recorre(raiz):
    """Devuelve la lista de filas, una por sidecar, ordenada por ruta."""
    filas = []
    for directorio in DIRECTORIOS:
        base = os.path.join(raiz, directorio)
        if not os.path.isdir(base):
            continue
        for actual, _dirs, archivos in os.walk(base):
            for nombre in archivos:
                if not nombre.endswith(".sha256"):
                    continue
                ruta = os.path.join(actual, nombre)
                rel_sidecar = os.path.relpath(ruta, raiz).replace(os.sep, "/")
                es_cuerpo = nombre.endswith(sella_sha256.SUFIJO_CUERPO)
                if es_cuerpo:
                    estado, objetivo, detalle, warns = _verifica_cuerpo(ruta, raiz)
                else:
                    estado, objetivo, detalle, warns = _verifica_viejo(ruta, raiz)
                declarado = TESTIGOS_DECLARADOS.get(rel_sidecar)
                # Un sello de CUERPO no se declara testigo: es nuevo y no
                # tiene historia que lo excuse (D-a4).
                if declarado and not es_cuerpo and estado in (NO_CASA, HUERFANO):
                    estado, detalle = TESTIGO, f"{detalle} || {declarado}"
                filas.append({
                    "sidecar": rel_sidecar,
                    "cuerpo": es_cuerpo,
                    "estado": estado,
                    "objetivo": objetivo.replace(os.sep, "/") if objetivo else None,
                    "detalle": detalle,
                    "warns": warns,
                })
    filas.sort(key=lambda f: f["sidecar"])
    return filas


def adjudica(filas):
    """FAIL: todo sello de cuerpo que no case, y todo sidecar viejo
    NO-CASA/HUÉRFANO no declarado testigo."""
    return [f for f in filas if f["estado"] in (NO_CASA, HUERFANO)]


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Verifica los sidecars de forense/encargos/ y forense/notas/. Nunca escribe."
    )
    ap.add_argument("--raiz", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="raíz del repo (por omisión, la de este archivo)")
    args = ap.parse_args(argv)
    raiz = os.path.abspath(args.raiz)

    filas = recorre(raiz)
    print("VERIFICA-SIDECARS · sólo lectura, nunca reescribe ni normaliza")
    print(f"  universo: {' + '.join(DIRECTORIOS)}  ·  sidecars examinados: {len(filas)}  (A.13)")
    print("")
    for f in filas:
        marca = "cuerpo" if f["cuerpo"] else "viejo "
        print(f"  [{marca}] {f['estado']:<9} {f['sidecar']}")
        if f["objetivo"]:
            print(f"             objetivo: {f['objetivo']}")
        if f["detalle"]:
            print(f"             {f['detalle']}")
        for w in f["warns"]:
            print(f"             WARN · {w}")

    fallos = adjudica(filas)
    warns = [(f["sidecar"], w) for f in filas for w in f["warns"]]
    print("")
    print(f"  WARN (se listan, no adjudican — D-16): {len(warns)}")
    for sidecar, w in warns:
        print(f"    - {sidecar}: {w}")
    if fallos:
        print(f"  FAIL: {len(fallos)}")
        for f in fallos:
            print(f"    - {f['estado']} {f['sidecar']} :: {f['detalle']}")
        return 1
    print("  FAIL: 0 — VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
