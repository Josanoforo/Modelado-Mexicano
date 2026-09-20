#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_arnes_sesion.py -- arnes del hook `SessionStart` + `CLAUDE.md`.

ACTO SESSION-START-HOOK-CLAUDE-MD (rama
`claude/session-start-hook-claude-md-ncxwc7`). Dos grupos:

1. `CLAUDE.md` nombra el archivo `instrucciones-proyecto-v*.md` de version
   mas alta que exista en el arbol y que no traiga sufijo `-HISTORIA` ni
   `-DELTA` -- ni un archivo inexistente, ni uno atrasado.
2. `tools/entorno.py --arranque`: los tres estados de red se alcanzan con
   `subprocess.run` mockeado, y la salida REAL del script (corrida de
   verdad, sin mocks) cumple <=12 lineas y exit code 0 siempre.

Corre sola:

    python3 -m pytest tests/test_arnes_sesion.py -v
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import entorno as E  # noqa: E402


# ---------------------------------------------------------------------------
# Derivacion de "version mas alta", misma logica que se uso para escribir
# CLAUDE.md: candidatos `instrucciones-proyecto-v<mayor>[_<menor>].md` en la
# raiz del repo, sin sufijo `-HISTORIA` ni `-DELTA`, ordenados por version.
# ---------------------------------------------------------------------------
_PATRON = re.compile(r"^instrucciones-proyecto-v(\d+)(?:_(\d+))?\.md$")


def _version_mas_alta(raiz: Path) -> str:
    candidatos = []
    for p in raiz.glob("instrucciones-proyecto-v*.md"):
        if "-HISTORIA" in p.name or "-DELTA" in p.name:
            continue
        m = _PATRON.match(p.name)
        if not m:
            continue
        mayor = int(m.group(1))
        menor = int(m.group(2)) if m.group(2) else 0
        candidatos.append(((mayor, menor), p.name))
    if not candidatos:
        raise AssertionError("ningun instrucciones-proyecto-v*.md vigente en el arbol")
    candidatos.sort()
    return candidatos[-1][1]


def _archivo_citado_en_claude_md(raiz: Path) -> str:
    texto = (raiz / "CLAUDE.md").read_text(encoding="utf-8")
    m = re.search(r"instrucciones-proyecto-v[\w.]+\.md", texto)
    assert m, "CLAUDE.md no cita ningun instrucciones-proyecto-v*.md"
    return m.group(0)


# --- Grupo 1: CLAUDE.md apunta al archivo vigente correcto -----------------

class TestClaudeMdApuntaAVigente:
    def test_archivo_citado_existe_en_el_arbol(self):
        citado = _archivo_citado_en_claude_md(RAIZ)
        assert (RAIZ / citado).exists(), (
            f"CLAUDE.md cita {citado!r}, que no existe en el arbol del repo"
        )

    def test_archivo_citado_es_el_de_version_mas_alta(self):
        citado = _archivo_citado_en_claude_md(RAIZ)
        vigente = _version_mas_alta(RAIZ)
        assert citado == vigente, (
            f"CLAUDE.md cita {citado!r} pero la version mas alta disponible "
            f"(sin -HISTORIA/-DELTA) es {vigente!r}"
        )

    def test_archivo_citado_no_es_historia_ni_delta(self):
        citado = _archivo_citado_en_claude_md(RAIZ)
        assert "-HISTORIA" not in citado and "-DELTA" not in citado


# --- Grupo 2: tools/entorno.py --arranque -----------------------------------

def _resultado_curl(http_code: str, http_connect: str, returncode: int = 0):
    r = mock.Mock()
    r.stdout = f"{http_code} {http_connect}"
    r.returncode = returncode
    return r


class TestSondaRedTresEstados:
    def test_permitida(self):
        with mock.patch.object(E.subprocess, "run",
                                return_value=_resultado_curl("200", "000")):
            assert "PERMITIDA" in E._sonda_red_arranque()

    def test_denegada_por_politica(self):
        # proxy responde 403 al CONNECT; la peticion final ni se hizo
        # (http_code queda en 000).
        with mock.patch.object(E.subprocess, "run",
                                return_value=_resultado_curl("000", "403")):
            assert "DENEGADA-POR-POLITICA" in E._sonda_red_arranque()

    def test_sin_red(self):
        with mock.patch.object(E.subprocess, "run",
                                side_effect=OSError("no hay interfaz")):
            assert "SIN-RED" in E._sonda_red_arranque()

    def test_sin_red_por_timeout(self):
        with mock.patch.object(
            E.subprocess, "run",
            side_effect=subprocess.TimeoutExpired(cmd="curl", timeout=10),
        ):
            assert "SIN-RED" in E._sonda_red_arranque()


class TestArranqueCorridaReal:
    """Sin mocks: corre `tools/entorno.py --arranque` de verdad."""

    def test_arranque_sale_con_codigo_0(self):
        r = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "entorno.py"), "--arranque"],
            capture_output=True, text=True, timeout=15,
        )
        assert r.returncode == 0, r.stderr

    def test_arranque_no_excede_12_lineas(self):
        r = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "entorno.py"), "--arranque"],
            capture_output=True, text=True, timeout=15,
        )
        lineas = [l for l in r.stdout.splitlines() if l.strip()]
        assert len(lineas) <= 12, f"{len(lineas)} lineas: {lineas}"

    def test_arranque_trae_la_linea_fija_final(self):
        r = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "entorno.py"), "--arranque"],
            capture_output=True, text=True, timeout=15,
        )
        assert (
            "SI EL ENCARGO DECLARA OTRO ENTORNO QUE ENTORNO-DERIVADO: "
            "PARA ANTES DE CUALQUIER OTRA COSA." in r.stdout
        )

    def test_arranque_trae_entorno_derivado(self):
        r = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "entorno.py"), "--arranque"],
            capture_output=True, text=True, timeout=15,
        )
        assert "ENTORNO-DERIVADO = " in r.stdout


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
