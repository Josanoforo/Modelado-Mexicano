#!/usr/bin/env python3
"""EMISIONES ciegas — `GEN2-DUELO-ENVIPE2026-MARGINALES-2`, COMMIT-2.

Piso 2025 (verbatim, sellado) + retador TENDENCIA-SERIE (2024+2025,
sellados) por celda de `civico.denuncia.con_seguro × cobertura_seguro`;
declara NO-CONSTRUIBLE lo que el spec-v1_0.md §0 ya determinó que no lo es.
Aritmética entre sellados: NO abre microdato, ningún guardián se ejerce
aquí (spec-v1_0.md §3, "Guardián `reservada=True` heredado").

El primer resultado que produzca este procedimiento es el que se reporta.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path


def _raiz() -> Path:
    p = Path(__file__).resolve()
    for d in p.parents:
        if (d / "tools" / "corrida0.py").exists():
            return d
    raise RuntimeError("raíz del repo no encontrada desde " + str(p))


RAIZ = _raiz()
_RUTA_TS = RAIZ / "tools" / "duelo" / "tendencia_serie.py"
SHA256_TENDENCIA_SERIE_CONGELADO = "7de0a988861bda7fb4be79129270350f25a1919607b116f6c7f2c2f3dd41c38f"


def _importa(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


def _verifica_dependencia_congelada():
    real = hashlib.sha256(_RUTA_TS.read_bytes()).hexdigest()
    if real != SHA256_TENDENCIA_SERIE_CONGELADO:
        raise SystemExit(
            f"tools/duelo/tendencia_serie.py cambió desde el sello de COMMIT-1: "
            f"esperado {SHA256_TENDENCIA_SERIE_CONGELADO}, encontrado {real}")


_verifica_dependencia_congelada()
ts = _importa("tendencia_serie", _RUTA_TS)

CELDAS = ("ASEGURADO", "NO-ASEGURADO")
BASE_ARBITRO_2025 = "RESULT-ARBITRO-ENVIPE2025-DENUNCIA-COBERTURA-SEGURO-{}"
BASE_PISO_2024 = "RESULT-PISOS-ENVIPE2024-V2-DENUNCIA-COBERTURA-SEGURO-{}"


def _resultados(inputs: dict, calc_id: str) -> dict:
    r = json.loads(inputs[calc_id]["bytes"].decode("utf-8"))
    return r.get("resultados", r)


def _punto(res: dict, base: str) -> tuple[float, float, float, int]:
    return (res[base + "-P"], res[base + "-IC-LO"], res[base + "-IC-HI"], res[base + "-N"])


def medir(inputs: dict, contrato: dict) -> dict:
    out = {}
    res_2025 = _resultados(inputs, "CALC-ARBITRO-MARGINALES-ENVIPE2025-0001")
    res_2024 = _resultados(inputs, "CALC-PISOS-ENVIPE2024-EJES-0002")
    for celda in CELDAS:
        p25, lo25, hi25, n25 = _punto(res_2025, BASE_ARBITRO_2025.format(celda))
        p24, lo24, hi24, _ = _punto(res_2024, BASE_PISO_2024.format(celda))
        base = f"RESULT-DUELO-MARGINALES-{celda}"
        out[base + "-PISO-P"] = p25
        out[base + "-PISO-IC-LO"] = lo25
        out[base + "-PISO-IC-HI"] = hi25
        out[base + "-PISO-N"] = n25
        retador = ts.tendencia_serie([(2024.0, p24, lo24, hi24), (2025.0, p25, lo25, hi25)], 2026.0)
        out[base + "-RETADOR-P"] = retador["p"] if retador else None
        out[base + "-RETADOR-IC-LO"] = retador["lo"] if retador else None
        out[base + "-RETADOR-IC-HI"] = retador["hi"] if retador else None
        out[base + "-RETADOR-CONSTRUIBLE"] = "SI" if retador else "NO"
    # spec-v1_0.md §0: NO-CONSTRUIBLE verificado contra el árbol, no medido aquí.
    out["RESULT-DUELO-MARGINALES-NACIONAL-RETADOR-CONSTRUIBLE"] = "NO"
    out["RESULT-DUELO-MARGINALES-NACIONAL-MOTIVO"] = (
        "un solo punto sellado (2025); CALC-PISOS-ENVIPE2024-EJES-0002 no trae DENUNCIA-TOTAL-TODOS")
    out["RESULT-DUELO-MARGINALES-SEXO-CONSTRUIBLE"] = "NO"
    out["RESULT-DUELO-MARGINALES-SEXO-MOTIVO"] = "ningún RESULT DENUNCIA-SEXO-* sellado en ningún CALC del árbol"
    out["RESULT-DUELO-MARGINALES-EDAD-CONSTRUIBLE"] = "NO"
    out["RESULT-DUELO-MARGINALES-EDAD-MOTIVO"] = "ningún RESULT DENUNCIA-EDAD-* sellado en ningún CALC del árbol"
    out["RESULT-DUELO-MARGINALES-DEMAS-REGLAS-ENVIPE-SERIE-N"] = 0
    out["RESULT-DUELO-MARGINALES-DEMAS-REGLAS-ENVIPE-SERIE-MOTIVO"] = (
        "CALC-ENVIPE-SERIE-* es una sola regla (p_c1_u1/no-denunciado), ya consumida por "
        "GEN2-DUELO-ENVIPE2026-EJECUCION-1 (decisiones.tsv: reserva:envipe2026-consumida-por-duelo)")
    return out
