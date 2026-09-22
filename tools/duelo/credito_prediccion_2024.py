#!/usr/bin/env python3
"""commit_3: adjudica CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001
(R, marginal real de ENIF 2024) contra
CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001 (candidatos ya sellados:
PERSISTENCIA / TENDENCIA-2 / TENDENCIA-3 / TENDENCIA-SERIE), con la regla
fijada en `commit_3a`
(`forense/prereg-caja/DIN-CREDITO-PREDICCION-2024-ADJUDICACION-spec-v1_1.md`
§6): ninguno de los dos lados trae réplicas propias (R sólo tiene punto +
IC percentil bootstrap; las emisiones sólo punto + IC analítico en logit),
así que se fabrican 10 000 réplicas SINTÉTICAS por cantidad, de forma
independiente entre sí, desde el SE analítico derivado del IC declarado
(`_ee_logit`), con una semilla y un orden de consumo fijados ANTES de leer
este RESULT. Esas réplicas sintéticas se alimentan al comparador de
REFERENCIA del proyecto, `tools/duelo/cruces_familia.py::adjudica()` (ya
genérico sobre instrumento: "recibe celdas ya estimadas -- punto, IC95,
réplicas -- y devuelve candidatos y adjudicación"), con
`umbral_vence_pp=inf` para que `VENCE-RETADOR` sea INALCANZABLE-POR-DISEÑO
(sin umbral de materialidad, decisión de commit_3a) y `umbral_reserva_pp`
en su valor por defecto (0.0).

No abre microdato: aritmética sobre dos RESULT ya sellados.

DEFECTO HEREDADO DECLARADO (hallado en este acto, código sellado en
COMMIT-1, no editable -- E.3): `abre_conducta_2024`
(`CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001/medidor.py`) pasa la
columna `niv` (códigos 2024, dos dígitos con cero inicial, "00".."11") por
`m._code()` (importado de `CALC-PISOS-ENIF2021-EJES-0003`), que le quita el
cero inicial (regex `^0+` antes de un dígito) -- diseñada para el código de un solo dígito de
2021 (`P3_1_1`, "0".."9"). El resultado: los códigos "00".."09" nunca
calzan contra las llaves de dos dígitos de `NIV_A_ESCOLARIDAD`
("00".."11") y quedan NaN (celdas HASTA-PRIMARIA/SECUNDARIA/MEDIA-SUPERIOR
-- N=0, P=None, declarado, seguro); los códigos "10"/"11" SÍ calzan, así
que la celda ESCOLARIDAD-SUPERIOR de este CALC NO está vacía pero SÍ está
mal compuesta: excluye "08"/"09" (que también son "superior" según el
propio mapa) y termina midiendo sólo maestría/doctorado (`niv` 10/11,
N=283 de 12 379 en K1) bajo la etiqueta "superior" -- un universo mucho
más chico y no representativo del que la spec pretendía. Este script
EXCLUYE el eje escolaridad completo (las 4 celdas, no sólo las 3 nulas) de
toda comparación cuantitativa, en las 9 conductas, y lo declara aparte.
Corregir el código está fuera de perímetro (PARO c, spec sellada): el
`medidor.py` de ADJUDICACION-0001 ya está sellado (E.3, `run` se niega) y
no se edita.

ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cruces_familia as cf  # implementación de referencia (Celda/adjudica)

RAIZ = Path(__file__).resolve().parents[2]
ADJ_PATH = RAIZ / "data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001/resultados.json"
EMI_PATH = RAIZ / "data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001/resultados.json"

Z95 = 1.959964
SEED = 20260922
REPS = 10000

ENTERING = ["K1", "K2-DEPARTAMENTAL", "K2-NOMINA", "K2-AUTOMOTRIZ", "K3",
            "K4A-AUTOEXCLUSION", "K4B-OFERTA", "K5", "K6-P-TENEDORES"]
CELLS_ADJ = ["NACIONAL-TODOS", "SEXO-1", "SEXO-2",
             "EDAD-18-29", "EDAD-30-44", "EDAD-45-59", "EDAD-60-MAS",
             "ESCOLARIDAD-HASTA-PRIMARIA", "ESCOLARIDAD-SECUNDARIA",
             "ESCOLARIDAD-MEDIA-SUPERIOR", "ESCOLARIDAD-SUPERIOR",
             "LOCALIDAD-MENOR-DE-15-000", "LOCALIDAD-15-000-Y-MAS",
             "FORMALIDAD-SIN-SEGURIDAD-SOCIAL", "FORMALIDAD-CON-SEGURIDAD-SOCIAL",
             "UNIVERSO-UNIVERSO-TRABAJA"]
ESCOLARIDAD_EXCLUIDA = {"ESCOLARIDAD-HASTA-PRIMARIA", "ESCOLARIDAD-SECUNDARIA",
                        "ESCOLARIDAD-MEDIA-SUPERIOR", "ESCOLARIDAD-SUPERIOR"}
PISOS = ("PERSISTENCIA", "TENDENCIA-2", "TENDENCIA-3", "TENDENCIA-SERIE")
CONTEXTO = ("K4B-OFERTA", "K5")  # oferta antes que preferencia, v2.16 §3


def _logit(p): return math.log(p / (1.0 - p))
def _expit(x): return 1.0 / (1.0 + math.exp(-x))
def _ee_logit(lo, hi): return (_logit(hi) - _logit(lo)) / (2.0 * Z95)


def _wilson(exitos: int, n: int, z: float = Z95):
    if n == 0:
        return None
    phat = exitos / n
    denom = 1.0 + z * z / n
    centro = (phat + z * z / (2 * n)) / denom
    radio = (z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, centro - radio), min(1.0, centro + radio))


def _cargar(ruta: Path) -> dict:
    d = json.loads(ruta.read_text())
    return d.get("resultados", d)


def _celda_sintetica(rng: np.random.Generator, p, lo, hi):
    """10000 draws SIEMPRE, orden fijo (commit_3a): se consumen y se
    descartan aunque la celda esté ausente o sea rara."""
    z = rng.standard_normal(REPS)
    if p is None or lo is None or hi is None:
        return cf.Celda(p=None, ic95=None, replicas=None), "SIN-CELDA"
    if not (0.0 < lo < 1.0 and 0.0 < hi < 1.0 and 0.0 < p < 1.0):
        return cf.Celda(p=None, ic95=None, replicas=None), "CELDA-RARA-LOGIT-INDEFINIDO"
    se = _ee_logit(lo, hi)
    reps = np.array([_expit(_logit(p) + se * zi) for zi in z])
    return cf.Celda(p=float(p), ic95=(float(lo), float(hi)), replicas=reps), "OK"


def _mae_puntual(candidatos: dict, R: dict, celdas: list) -> float | None:
    errores = [100.0 * abs(candidatos[c].p - R[c].p) for c in celdas
               if candidatos[c].p is not None and R[c].p is not None]
    return (sum(errores) / len(errores)) if errores else None


def adjudica_conducta(cid: str, R_all: dict, E_all: dict, rng: np.random.Generator) -> dict:
    R, candidatos, estados = {}, {p: {} for p in PISOS}, {}
    for cell in CELLS_ADJ:
        base_r = f"RESULT-DIN-CREDITO-PREDICCION-2024-ADJ-{cid}-{cell}"
        celda_r, estado_r = _celda_sintetica(
            rng, R_all.get(base_r + "-P"), R_all.get(base_r + "-IC-LO"), R_all.get(base_r + "-IC-HI"))
        R[cell] = celda_r
        estados[cell] = {"R": estado_r}
        for piso in PISOS:
            base_c = f"RESULT-DIN-CREDITO-PREDICCION-2024-{cid}-{cell}-2024-{piso}"
            celda_c, estado_c = _celda_sintetica(
                rng, E_all.get(base_c + "-P"), E_all.get(base_c + "-IC-LO"), E_all.get(base_c + "-IC-HI"))
            candidatos[piso][cell] = celda_c
            estados[cell][piso] = estado_c

    # celdas elegibles: con R, no escolaridad (defecto heredado declarado arriba).
    elegibles = [c for c in CELLS_ADJ if c not in ESCOLARIDAD_EXCLUIDA and R[c].p is not None]

    def _n_por_ola(piso_o_r):
        fuente = R if piso_o_r == "R" else candidatos[piso_o_r]
        return {c: (1 if (c in elegibles and fuente[c].p is not None) else None) for c in CELLS_ADJ}

    habilitados = [p for p in PISOS[1:] if any(candidatos[p][c].p is not None for c in elegibles)]

    mae_por_piso = {}
    for piso in PISOS:
        punt = cf.puntuadas({"R": _n_por_ola("R"), piso: _n_por_ola(piso)}, 1)
        celdas_p = [c for c, ok in punt.items() if ok]
        mae_por_piso[piso] = {"mae_pp": _mae_puntual(candidatos[piso], R, celdas_p),
                               "n_celdas_puntuadas": len(celdas_p),
                               "celdas_puntuadas": celdas_p}

    retador = None
    if habilitados:
        con_mae = [(p, mae_por_piso[p]["mae_pp"]) for p in habilitados if mae_por_piso[p]["mae_pp"] is not None]
        if con_mae:
            retador = min(con_mae, key=lambda t: t[1])[0]

    adjudicaciones = {}
    for piso in habilitados:
        punt = cf.puntuadas({"R": _n_por_ola("R"), "PERSISTENCIA": _n_por_ola("PERSISTENCIA"),
                              piso: _n_por_ola(piso)}, 1)
        adj = cf.adjudica(R, {"PERSISTENCIA": candidatos["PERSISTENCIA"], piso: candidatos[piso]},
                           punt, piso="PERSISTENCIA", retador=piso,
                           umbral_vence_pp=math.inf, umbral_reserva_pp=0.0)
        fila = adj["candidatos"][piso]
        fila["rol"] = "PRIMARIA" if piso == retador else "SECUNDARIA"
        # cobertura: R dentro del IC del candidato, con Wilson sobre la proporcion
        celdas_p = [c for c, ok in punt.items() if ok]
        dentros = [fila["celdas"][c]["R_dentro_ic_cand"] for c in celdas_p
                   if fila["celdas"][c]["R_dentro_ic_cand"] is not None]
        n_cob = len(dentros)
        exitos = sum(1 for x in dentros if x)
        fila["cobertura"] = {
            "n_celdas": n_cob, "exitos": exitos,
            "proporcion": (exitos / n_cob) if n_cob else None,
            "ic95_wilson": _wilson(exitos, n_cob) if n_cob else None,
        }
        adjudicaciones[piso] = fila

    return {
        "conducta": cid, "n_celdas_elegibles": len(elegibles), "celdas_elegibles": elegibles,
        "celdas_excluidas_escolaridad": sorted(ESCOLARIDAD_EXCLUIDA),
        "habilitados": habilitados, "retador_primario": retador,
        "mae_por_contendiente": mae_por_piso,
        "adjudicacion_por_retador": adjudicaciones,
        "estados_celda": estados,
    }


def contexto_oferta(cid: str, R_all: dict, elegibles: list) -> dict:
    """K4B-OFERTA y K5 (R real de la MISMA celda) al lado de K1/K2-*/K3
    (oferta antes que preferencia, v2.16 §3) -- no entra al computo de MAE."""
    if cid not in ("K1", "K2-DEPARTAMENTAL", "K2-NOMINA", "K2-AUTOMOTRIZ", "K3"):
        return {}
    out = {}
    for cell in elegibles:
        fila = {"P": R_all.get(f"RESULT-DIN-CREDITO-PREDICCION-2024-ADJ-{cid}-{cell}-P")}
        for cx in CONTEXTO:
            fila[cx] = R_all.get(f"RESULT-DIN-CREDITO-PREDICCION-2024-ADJ-{cx}-{cell}-P")
        out[cell] = fila
    return out


def main():
    R_all = _cargar(ADJ_PATH)
    E_all = _cargar(EMI_PATH)
    rng = np.random.Generator(np.random.PCG64(SEED))

    salida = {"seed": SEED, "replicas": REPS, "conductas": {}}
    for cid in ENTERING:
        res = adjudica_conducta(cid, R_all, E_all, rng)
        res["contexto_oferta"] = contexto_oferta(cid, R_all, res["celdas_elegibles"])
        salida["conductas"][cid] = res
    return salida


if __name__ == "__main__":
    out = main()
    destino = RAIZ / "data/corrida0/duelo-credito-prediccion-2024.json"
    destino.write_text(json.dumps(out, indent=2, ensure_ascii=False, default=lambda o: None))
    print(f"escrito: {destino}")
    for cid, res in out["conductas"].items():
        r = res["retador_primario"]
        v = res["adjudicacion_por_retador"].get(r, {}).get("veredicto") if r else "NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO"
        dmae = res["adjudicacion_por_retador"].get(r, {}).get("delta_mae_pp") if r else None
        print(f"{cid:20s} retador={r or '-':16s} veredicto={v:16s} deltaMAE_pp={dmae}")
