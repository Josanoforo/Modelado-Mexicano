#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""El primer resultado que produzca este procedimiento es el que se reporta.

`CALC-PISO-PERSISTENCIA-ERROR-0001` -- mide cuánto se equivoca el piso de
persistencia `t-1` de la rejilla frente al `R` sellado de la misma celda
marginal. Pre-registro congelado: `prereg-caja-PISO-PERSISTENCIA-ERROR`
(`forense/prereg-caja/PISO-PERSISTENCIA-ERROR-spec-v1_0.md`).

CERO MICRODATO. Los dos lados de cada resta ya están sellados:
  · el piso  -> `CALC-PISOS-{ENVIPE2024-EJES-0002, ENCIG2023-EJES-0002,
    ENIF2021-EJES-0003}/resultados.json`, vía la tabla de identidad
    `forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv`;
  · el `R`   -> las celdas marginales de `milpa/tramite-ola5-propuesta-v0.yaml`,
    leídas por `tools/marcador_segmento.py` (enlace biyectivo, guardia D-14).

Sólo stdlib: este CALC no estima nada, resta valores ya estimados.

Uso:
    python3 data/corrida0/CALC-PISO-PERSISTENCIA-ERROR-0001/medidor.py
    python3 .../medidor.py --escribe     # escribe resultados.json
    python3 .../medidor.py --verifica    # re-deriva y compara con lo sellado
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
RESULTADOS_JSON = AQUI / "resultados.json"
CALC_ID = "CALC-PISO-PERSISTENCIA-ERROR-0001"

# z de dos colas al 95%. Único parámetro del procedimiento; congelado en §3
# de la spec junto con su supuesto (simetría normal del intervalo).
Z95 = 1.959964

# Brecha temporal por instrumento, declarada en CADA fila de salida. No se
# agrega nunca entre instrumentos: 1, 2 y 3 años no promedian (spec §5).
# Los valores se LEEN de la tabla de identidad (`source_edition` ->
# `target_edition`); este mapa sólo nombra el instrumento.
def _brecha(fila_tabla: dict) -> str:
    try:
        return str(int(fila_tabla["target_edition"]) - int(fila_tabla["source_edition"]))
    except (KeyError, TypeError, ValueError):
        return "NO-DERIVABLE"


def _marcador():
    spec = importlib.util.spec_from_file_location(
        "marcador_segmento_para_calc", RAIZ / "tools" / "marcador_segmento.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _ee_de_ic(inf: float, sup: float) -> float:
    """Error estándar aproximado desde un IC95, por simetría normal.
    La spec §3 declara que esto pierde la asimetría del bootstrap por
    percentiles; se usa igual y se dice que se usa."""
    return (float(sup) - float(inf)) / (2.0 * Z95)


def _slug(s: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in str(s)).strip("-").upper()


def celdas() -> list[dict]:
    """Una entrada por celda marginal ENLAZADA, con los dos lados y su
    procedencia. No decide nada: sólo junta."""
    M = _marcador()
    idx = M.indice_identidad()
    por_cell_id = {f["cell_id"]: f for f in M.lee_tabla_identidad()}
    v = M.deriva()
    fuera = []
    salida = []
    for f in v["filas"]:
        if f["tipo"] != "MARGINAL":
            continue
        if not f["resultado_id"]:
            continue                      # SIN-PISO: no hay resta que hacer
        tabla = por_cell_id.get(f["resultado_id"], {})
        salida.append({
            "celda_id": f["celda_id"],
            "regla": f["regla_o_eje_origen"],
            "eje": f["eje_o_par"],
            "categoria": f["categoria"],
            "instrumento": tabla.get("source_instrument", "NO-DECLARADO"),
            "desenlace": tabla.get("outcome", "NO-DECLARADO"),
            "brecha_anios": _brecha(tabla),
            "piso_edicion": tabla.get("source_edition", ""),
            "piso_periodo": tabla.get("source_reference_period", ""),
            "R_edicion": tabla.get("target_edition", ""),
            "R_periodo": tabla.get("target_reference_period", ""),
            "unit_tabla": tabla.get("unit", ""),
            "unidad_marcador": f["unidad_dato"],
            "estado_marcador": f["estado"],
            "piso": f["piso"],
            "piso_ic95": f["piso_ic95"],
            "piso_fuente": f["piso_fuente"],
            "resultado_id_piso": f["resultado_id"],
            "R": f["R"], "R_ic95inf": f["R_ic95inf"], "R_ic95sup": f["R_ic95sup"],
        })
    del fuera
    return salida


def mide_celda(c: dict) -> dict:
    """`d = R - piso` en puntos porcentuales, su IC95, y la clase.
    Una celda que no es comparable sale rotulada, no se fuerza (A-bis 3-4)."""
    base = dict(c)

    # A-bis 3-4: unidad/universo. La unidad del piso la declara la tabla; la
    # del R, el payload del árbitro. Si no coinciden, no se resta.
    M = _marcador()
    unit_norm = M.NORMALIZA_UNIT_TABLA.get(
        (c["unit_tabla"] or "").strip().upper(),
        f"NO-NORMALIZADA:{c['unit_tabla']}")
    if unit_norm != c["unidad_marcador"]:
        base.update({"clase": "NO-COMPARABLE", "d_pp": "", "d_ic95inf_pp": "",
                     "d_ic95sup_pp": "",
                     "causa": (f"UNIDAD-DISCREPANTE: tabla={c['unit_tabla']!r} "
                               f"vs marcador={c['unidad_marcador']!r}")})
        return base
    if c["estado_marcador"] != "SOLO-PISO":
        base.update({"clase": "NO-COMPARABLE", "d_pp": "", "d_ic95inf_pp": "",
                     "d_ic95sup_pp": "",
                     "causa": f"ESTADO-NO-SOLO-PISO:{c['estado_marcador']}"})
        return base

    try:
        piso = float(c["piso"]); R = float(c["R"])
        p_lo, p_hi = [float(x) for x in
                      c["piso_ic95"].strip("[]").split(",")]
        r_lo = float(c["R_ic95inf"]); r_hi = float(c["R_ic95sup"])
    except (TypeError, ValueError, AttributeError):
        base.update({"clase": "NO-COMPARABLE", "d_pp": "", "d_ic95inf_pp": "",
                     "d_ic95sup_pp": "",
                     "causa": "FALTA-PUNTO-O-IC95-EN-ALGUNO-DE-LOS-DOS-LADOS"})
        return base

    d_pp = (R - piso) * 100.0
    ee_pp = math.sqrt(_ee_de_ic(p_lo, p_hi) ** 2 + _ee_de_ic(r_lo, r_hi) ** 2) * 100.0
    lo = d_pp - Z95 * ee_pp
    hi = d_pp + Z95 * ee_pp
    # clase: el criterio es el intervalo y sólo el intervalo (spec §4).
    clase = "PERSISTE" if (lo <= 0.0 <= hi) else "CAMBIA"
    base.update({"clase": clase, "d_pp": d_pp, "d_ee_pp": ee_pp,
                 "d_ic95inf_pp": lo, "d_ic95sup_pp": hi, "causa": ""})
    return base


def agrega(medidas: list[dict]) -> dict:
    """Agregados por (instrumento x desenlace) y por (instrumento x eje).
    NUNCA entre instrumentos: las brechas son 1, 2 y 3 años (spec §5)."""
    out: dict[str, dict] = {}

    def _grupo(clave: str, filas: list[dict]) -> dict:
        comp = [f for f in filas if f["clase"] in ("PERSISTE", "CAMBIA")]
        brechas = sorted({f["brecha_anios"] for f in filas})
        g = {
            "n_celdas": len(filas),
            "n_comparables": len(comp),
            "n_persiste": sum(1 for f in comp if f["clase"] == "PERSISTE"),
            "n_cambia": sum(1 for f in comp if f["clase"] == "CAMBIA"),
            "n_no_comparable": len(filas) - len(comp),
            "brecha_anios": brechas[0] if len(brechas) == 1 else brechas,
        }
        if comp:
            g["mae_pp"] = sum(abs(f["d_pp"]) for f in comp) / len(comp)
            g["d_medio_pp"] = sum(f["d_pp"] for f in comp) / len(comp)
        else:
            g["mae_pp"] = ""
            g["d_medio_pp"] = ""
        return g

    for llave, etiqueta in (("desenlace", "DESENLACE"), ("eje", "EJE")):
        vistos: dict[tuple, list[dict]] = {}
        for f in medidas:
            vistos.setdefault((f["instrumento"], f[llave]), []).append(f)
        for (inst, val), filas in sorted(vistos.items()):
            out[f"{inst}::{etiqueta}::{val}"] = _grupo(f"{inst}::{val}", filas)

    # por instrumento entero -- sigue siendo DENTRO de un instrumento
    vistos_i: dict[str, list[dict]] = {}
    for f in medidas:
        vistos_i.setdefault(f["instrumento"], []).append(f)
    for inst, filas in sorted(vistos_i.items()):
        out[f"{inst}::INSTRUMENTO"] = _grupo(inst, filas)
    return out


def deriva() -> dict:
    medidas = [mide_celda(c) for c in celdas()]
    agregados = agrega(medidas)

    resultados: dict[str, object] = {}
    for m in medidas:
        base = f"RESULT-PISO-ERR-{_slug(m['instrumento'])}-{_slug(m['desenlace'])}-{_slug(m['eje'])}-{_slug(m['categoria'])}"
        resultados[f"{base}-CLASE"] = m["clase"]
        if m["clase"] in ("PERSISTE", "CAMBIA"):
            resultados[f"{base}-D-PP"] = m["d_pp"]
            resultados[f"{base}-D-IC-LO-PP"] = m["d_ic95inf_pp"]
            resultados[f"{base}-D-IC-HI-PP"] = m["d_ic95sup_pp"]
        else:
            resultados[f"{base}-CAUSA"] = m["causa"]
    for clave, g in agregados.items():
        b = f"RESULT-PISO-ERR-AGG-{_slug(clave)}"
        resultados[f"{b}-N"] = g["n_celdas"]
        resultados[f"{b}-N-PERSISTE"] = g["n_persiste"]
        resultados[f"{b}-N-CAMBIA"] = g["n_cambia"]
        if g["mae_pp"] != "":
            resultados[f"{b}-MAE-PP"] = g["mae_pp"]
            resultados[f"{b}-D-MEDIO-PP"] = g["d_medio_pp"]
    return {"spec_id": CALC_ID, "celdas": medidas, "agregados": agregados,
            "resultados": resultados}


def medir(inputs, contrato):
    """Interfaz única de la casa (`tools/corrida0.py`, plan v2.0 §4 B-1).

    Este medidor no abre `inputs`: los cinco insumos ya son archivos del
    repo con `sha256` declarado en `spec.yaml`, y el pre-flight los verifica
    antes de llamar aquí. `contrato` se lee sólo para comprobar que el `z95`
    que gobierna la clasificación es el congelado en la spec -- si alguien
    lo moviera, la corrida PARA en vez de reportar otra cosa con el mismo
    nombre."""
    z = (contrato or {}).get("parametros", {}).get("z95")
    if z is not None and float(z) != Z95:
        raise RuntimeError(f"z95 del contrato ({z}) != z95 congelado ({Z95})")
    return deriva()["resultados"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--escribe", action="store_true")
    ap.add_argument("--verifica", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    v = deriva()
    if args.verifica:
        if not RESULTADOS_JSON.exists():
            print("NO-SELLADO: no existe resultados.json")
            return 2
        sellado = json.loads(RESULTADOS_JSON.read_text(encoding="utf-8"))
        if sellado.get("resultados") != v["resultados"]:
            print("DIVERGE: la re-derivación no reproduce lo sellado")
            return 1
        print(f"VERIFICA-OK: {len(v['resultados'])} RESULT reproducidos")
        return 0
    if args.escribe:
        RESULTADOS_JSON.write_text(
            json.dumps({"spec_id": CALC_ID, "resultados": v["resultados"],
                        "celdas": v["celdas"], "agregados": v["agregados"]},
                       ensure_ascii=False, indent=1, sort_keys=True) + "\n",
            encoding="utf-8")
        print(f"ESCRITO {RESULTADOS_JSON.relative_to(RAIZ)}: "
              f"{len(v['resultados'])} RESULT")
    if args.json:
        print(json.dumps(v["agregados"], ensure_ascii=False, indent=2, sort_keys=True))
    else:
        comp = [m for m in v["celdas"] if m["clase"] in ("PERSISTE", "CAMBIA")]
        print(f"celdas enlazadas={len(v['celdas'])} comparables={len(comp)} "
              f"PERSISTE={sum(1 for m in comp if m['clase']=='PERSISTE')} "
              f"CAMBIA={sum(1 for m in comp if m['clase']=='CAMBIA')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
