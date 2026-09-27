#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_arnes_sesion.py -- arnes del hook `SessionStart` + `CLAUDE.md`.

ACTO SESSION-START-HOOK-CLAUDE-MD (rama
`claude/session-start-hook-claude-md-ncxwc7`), reescrito al estilo de la
casa (script, sin pytest) por ACTO GEN2-CI-GUARDIAS-VIVAS-1
(20/sep/2026, P3/P4): era uno de los 5 archivos que importaban `pytest`
sin que `requirements.txt` lo declarara -- nunca corria en CI. `pytest` no
esta decidido (FP de mesa, censo-tests.tsv); reescribir evita esperar esa
decision para que esta guardia deje de ser huerfana.

Dos grupos:

1. `CLAUDE.md` nombra el archivo `instrucciones-proyecto-v*.md` de version
   mas alta que exista en el arbol y que no traiga sufijo `-HISTORIA` ni
   `-DELTA` -- ni un archivo inexistente, ni uno atrasado.
2. `tools/entorno.py --arranque`: los CUATRO estados de red (P4) se
   alcanzan con `subprocess.run` mockeado, y la salida REAL del script
   (corrida de verdad, sin mocks) cumple <=12 lineas y exit code 0
   siempre.

Corre sola:

    python3 tests/test_arnes_sesion.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import entorno as E  # noqa: E402

FAILS = []


def _falla(nombre, msg):
    FAILS.append(f"{nombre}: {msg}")


# ---------------------------------------------------------------------------
# Derivacion de "version mas alta", misma logica que se uso para escribir
# CLAUDE.md: candidatos `instrucciones-proyecto-v<mayor>[_<menor>].md` en la
# raiz del repo, sin sufijo `-HISTORIA` ni `-DELTA`, ordenados por version.
# ---------------------------------------------------------------------------
_PATRON = re.compile(r"^instrucciones-proyecto-v(\d+)(?:_(\d+))?\.md$")


def _version_mas_alta(raiz: Path) -> str:
    candidatos = []
    # GEN2-FRONT-3-PORTADA-1: la vigente vive en gobierno/; las viejas, en archivo/.
    for p in (raiz / "gobierno").glob("instrucciones-proyecto-v*.md"):
        if "-HISTORIA" in p.name or "-DELTA" in p.name:
            continue
        m = _PATRON.match(p.name)
        if not m:
            continue
        mayor = int(m.group(1))
        menor = int(m.group(2)) if m.group(2) else 0
        candidatos.append(((mayor, menor), f"gobierno/{p.name}"))
    if not candidatos:
        raise AssertionError("ningun instrucciones-proyecto-v*.md vigente en el arbol")
    candidatos.sort()
    return candidatos[-1][1]


def _archivo_citado_en_claude_md(raiz: Path) -> str:
    texto = (raiz / "CLAUDE.md").read_text(encoding="utf-8")
    m = re.search(r"(?:gobierno/)?instrucciones-proyecto-v[\w.]+\.md", texto)
    if not m:
        raise AssertionError("CLAUDE.md no cita ningun instrucciones-proyecto-v*.md")
    return m.group(0)


# --- Grupo 1: CLAUDE.md apunta al archivo vigente correcto -----------------


def prueba_archivo_citado_existe_en_el_arbol():
    citado = _archivo_citado_en_claude_md(RAIZ)
    if not (RAIZ / citado).exists():
        _falla(
            "archivo_citado_existe_en_el_arbol",
            f"CLAUDE.md cita {citado!r}, que no existe en el arbol del repo",
        )


def prueba_archivo_citado_es_el_de_version_mas_alta():
    citado = _archivo_citado_en_claude_md(RAIZ)
    vigente = _version_mas_alta(RAIZ)
    if citado != vigente:
        _falla(
            "archivo_citado_es_el_de_version_mas_alta",
            f"CLAUDE.md cita {citado!r} pero la version mas alta disponible "
            f"(sin -HISTORIA/-DELTA) es {vigente!r}",
        )


def prueba_archivo_citado_no_es_historia_ni_delta():
    citado = _archivo_citado_en_claude_md(RAIZ)
    if "-HISTORIA" in citado or "-DELTA" in citado:
        _falla("archivo_citado_no_es_historia_ni_delta", f"citado={citado!r}")


# --- Grupo 2: tools/entorno.py --arranque -----------------------------------


def _resultado_curl(cuerpo_stdout: str, returncode: int = 0):
    r = mock.Mock()
    r.stdout = cuerpo_stdout
    r.returncode = returncode
    return r


def _marca(http_code: str, http_connect: str, cabeceras: str = "") -> str:
    """Reproduce lo que `curl -D - -o /dev/null -w ...` deja en stdout:
    cabeceras (si las hay) primero, la marca al final."""
    partes = []
    if cabeceras:
        partes.append(cabeceras)
    partes.append(f"__CI_GUARDIAS_MARCA__ {http_code} {http_connect}")
    return "\n".join(partes)


def prueba_permitida():
    with mock.patch.object(
        E.subprocess, "run", return_value=_resultado_curl(_marca("200", "000"))
    ):
        salida = E._sonda_red_arranque()
        if "PERMITIDA" not in salida:
            _falla("permitida", salida)


def prueba_denegada_por_politica_connect():
    # proxy responde 403 al CONNECT; la peticion final ni se hizo
    # (http_code queda en 000).
    with mock.patch.object(
        E.subprocess, "run", return_value=_resultado_curl(_marca("000", "403"))
    ):
        salida = E._sonda_red_arranque()
        if "DENEGADA-POR-POLITICA" not in salida:
            _falla("denegada_por_politica_connect", salida)


def prueba_denegada_por_politica_respuesta_final():
    # Defecto real (P4): proxy transparente que SI deja salir la peticion
    # y contesta el la con un 403 final, cabecera `x-deny-reason` incluida
    # -- antes de este acto, `_sonda_red_arranque` la leia como SIN-RED
    # igual que si nadie hubiera contestado.
    cuerpo = _marca("403", "000", cabeceras="x-deny-reason: host_not_allowed")
    with mock.patch.object(
        E.subprocess, "run", return_value=_resultado_curl(cuerpo)
    ):
        salida = E._sonda_red_arranque()
        if "DENEGADA-POR-POLITICA" not in salida:
            _falla("denegada_por_politica_respuesta_final", salida)


def prueba_respuesta_no_ok():
    # Hubo conexion y alguien contesto un codigo que no es 2xx/3xx y no es
    # la denegacion de politica reconocida (sin `x-deny-reason`): no se
    # sabe si fue un proxy intermedio o INEGI, y se dice asi.
    with mock.patch.object(
        E.subprocess, "run", return_value=_resultado_curl(_marca("503", "000"))
    ):
        salida = E._sonda_red_arranque()
        if "RESPUESTA-NO-OK(503)" not in salida:
            _falla("respuesta_no_ok", salida)


def prueba_sin_red():
    with mock.patch.object(
        E.subprocess, "run", side_effect=OSError("no hay interfaz")
    ):
        salida = E._sonda_red_arranque()
        if "SIN-RED" not in salida:
            _falla("sin_red", salida)


def prueba_sin_red_por_timeout():
    with mock.patch.object(
        E.subprocess,
        "run",
        side_effect=subprocess.TimeoutExpired(cmd="curl", timeout=10),
    ):
        salida = E._sonda_red_arranque()
        if "SIN-RED" not in salida:
            _falla("sin_red_por_timeout", salida)


def _corre_arranque():
    return subprocess.run(
        [sys.executable, str(RAIZ / "tools" / "entorno.py"), "--arranque"],
        capture_output=True,
        text=True,
        timeout=15,
    )


def prueba_arranque_sale_con_codigo_0():
    r = _corre_arranque()
    if r.returncode != 0:
        _falla("arranque_sale_con_codigo_0", r.stderr)


def prueba_arranque_no_excede_12_lineas():
    r = _corre_arranque()
    lineas = [l for l in r.stdout.splitlines() if l.strip()]
    if len(lineas) > 12:
        _falla("arranque_no_excede_12_lineas", f"{len(lineas)} lineas: {lineas}")


def prueba_arranque_trae_la_linea_fija_final():
    r = _corre_arranque()
    esperado = (
        "SI EL ENCARGO DECLARA OTRO ENTORNO QUE ENTORNO-DERIVADO: "
        "PARA ANTES DE CUALQUIER OTRA COSA."
    )
    if esperado not in r.stdout:
        _falla("arranque_trae_la_linea_fija_final", r.stdout)


def prueba_arranque_trae_entorno_derivado():
    r = _corre_arranque()
    if "ENTORNO-DERIVADO = " not in r.stdout:
        _falla("arranque_trae_entorno_derivado", r.stdout)


def main():
    prueba_archivo_citado_existe_en_el_arbol()
    prueba_archivo_citado_es_el_de_version_mas_alta()
    prueba_archivo_citado_no_es_historia_ni_delta()
    prueba_permitida()
    prueba_denegada_por_politica_connect()
    prueba_denegada_por_politica_respuesta_final()
    prueba_respuesta_no_ok()
    prueba_sin_red()
    prueba_sin_red_por_timeout()
    prueba_arranque_sale_con_codigo_0()
    prueba_arranque_no_excede_12_lineas()
    prueba_arranque_trae_la_linea_fija_final()
    prueba_arranque_trae_entorno_derivado()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_arnes_sesion.py: 13 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
