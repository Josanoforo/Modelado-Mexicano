#!/usr/bin/env python3
"""Medidor de `CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001`
(`COMMIT-3`). ACTO `GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1`. Contrato humano:
`forense/prereg-caja/TRA-evade-norma-cruces-encogida-spec-v1_0.md` §3, §3.1
(criterio escrito antes del dato). Deriva `R` — las 38 celdas de los cuatro
cruces de ENVIPE 2025 — con la receta del árbitro, y adjudica contra las
emisiones **ya selladas** en `COMMIT-2`
(`CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001`, input de repo por
sha256).

Este es el primer código del acto que cruza ENVIPE 2025 (el `COMMIT-2` sólo
tocó marginales, nunca `mr.cruce`): la ola se carga con `reservada=False`.
El orden lo prueba el historial (`NC-0313`): el directorio de este CALC no
existe en ningún commit anterior al `COMMIT-3`.

`ΔMAE` con IC: la incertidumbre que se propaga réplica a réplica es la de
`R` (recién estimado de la ola liberada); el punto de cada candidato viene
**fijo** de la emisión sellada de `COMMIT-2` (que ya llevaba su propio IC,
reportado aparte, `-VS-C2` y `-DENTRO-IC-R` abajo) — es una simplificación
declarada, no una IC conjunta candidato×R, y se documenta como tal.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[3]


def _importa(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


mr = _importa("marginales_reproduccion",
              RAIZ / "tools" / "celda_d" / "marginales_reproduccion.py")
M = _importa("p4_medidor",
            RAIZ / "data" / "corrida0" /
            "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001" / "medidor.py")

P_EMI = M.P
PISOS = ("C1", "C2")
RETADORES = ("C7", "C-ENCOGIDA")
CANDIDATOS = PISOS + RETADORES
TOL_C2 = 1e-9


class ParoDeGuardia(RuntimeError):
    pass


def prefijo(cruce_id):
    return f"RESULT-TRA-ENCOGIDA-ARB-{cruce_id}"


def _dentro(p, ic):
    return p is not None and ic is not None and ic[0] <= p <= ic[1]


def _estado_gana(ic_delta_vs_c2, umbral_pp):
    """Spec humana §3: el IC primario decide; el conteo de celdas es descriptivo."""
    if ic_delta_vs_c2 is None or ic_delta_vs_c2[0] is None:
        return "NO"
    if ic_delta_vs_c2[0] > umbral_pp:
        return "SI"
    if ic_delta_vs_c2[0] > 0:
        return "PROPUESTA-CON-RESERVA"
    return "NO"


def _lee_json(bytes_):
    raw = json.loads(bytes_.decode("utf-8"))
    resultados = raw.get("resultados", raw) if isinstance(raw, dict) else raw
    if isinstance(resultados, list):
        resultados = {x["id"]: x["valor"] for x in resultados}
    return resultados


def _guardia_sello(inputs):
    if "emisiones_resultados" not in inputs or "emisiones_sello" not in inputs:
        raise ParoDeGuardia("faltan emisiones_resultados/emisiones_sello -- COMMIT-2 no sellado")
    sello = _lee_json(inputs["emisiones_sello"]["bytes"])
    import hashlib
    huella = hashlib.sha256(inputs["emisiones_resultados"]["bytes"]).hexdigest()
    if sello.get("resultados.json") != huella:
        raise ParoDeGuardia(f"sha256 de emisiones_resultados no coincide con emisiones_sello "
                            f"({huella} != {sello.get('resultados.json')})")
    return _lee_json(inputs["emisiones_resultados"]["bytes"])


def medir(inputs, contrato):
    par = contrato["parametros"]
    umbral = int(par["n_minimo_celda"])
    delta_mae_umbral = float(par["delta_mae_umbral_pp"])
    out: dict = {}
    emis = _guardia_sello(inputs)
    out["RESULT-TRA-ENCOGIDA-ARB-G-INPUT-ENVIPE2025-CSV-SHA256"] = str(inputs["envipe2025_csv"]["sha256"])

    # ── R · las 38 celdas, receta del árbitro, primera apertura del cruce ─
    ola25 = mr.carga_ola(inputs["envipe2025_csv"]["ruta_absoluta"], 2025, reservada=False)
    out["RESULT-TRA-ENCOGIDA-ARB-G-R-FILAS-UNIVERSO"] = int(ola25.meta["filas_universo"])
    out["RESULT-TRA-ENCOGIDA-ARB-G-R-ESTRATOS"] = int(ola25.meta["estratos"])
    out["RESULT-TRA-ENCOGIDA-ARB-G-R-UPM"] = int(ola25.meta["upm"])

    lectura_bbis_global = []
    for cruce_id, (eje_a, eje_b) in M.CRUCES.items():
        pre_out = prefijo(cruce_id)
        pre_emi = M.prefijo(cruce_id)
        x = mr.cruce(ola25, eje_a, eje_b)
        out[f"{pre_out}-G-COBERTURA-CRUCE"] = float(x["cobertura"])

        R, EE, ICR, d_pp, cand_p = {}, {}, {}, {k: {} for k in CANDIDATOS}, {k: {} for k in CANDIDATOS}
        fuera25 = 0
        celdas_lista = M.celdas(cruce_id)
        for ka, kb in celdas_lista:
            c = M.celda_corta(cruce_id, ka, kb)
            cel = x["celdas"][(ka, kb)]
            out[f"{pre_out}-{c}-R-N"] = int(cel["n"])
            sop = "SOPORTE-OK" if cel["n"] >= umbral else "FUERA-DE-SOPORTE"
            fuera25 += sop != "SOPORTE-OK"
            out[f"{pre_out}-{c}-SOPORTE-2025"] = sop
            out[f"{pre_out}-{c}-R-P"] = cel["p"]
            if cel["ic95"] is not None:
                lo, hi = float(cel["ic95"][0]), float(cel["ic95"][1])
                out[f"{pre_out}-{c}-R-IC-LO"] = lo
                out[f"{pre_out}-{c}-R-IC-HI"] = hi
                out[f"{pre_out}-{c}-R-EE"] = (hi - lo) / 3.92
                R[c], EE[c], ICR[c] = float(cel["p"]), (hi - lo) / 3.92, (lo, hi)
            else:
                out[f"{pre_out}-{c}-R-IC-LO"] = out[f"{pre_out}-{c}-R-IC-HI"] = None
                out[f"{pre_out}-{c}-R-EE"] = None
                R[c], EE[c], ICR[c] = None, None, None
            for k in CANDIDATOS:
                v = emis.get(f"{pre_emi}-{c}-{k}-P")
                cand_p[k][c] = v
        out[f"{pre_out}-G-CELDAS-FUERA-DE-SOPORTE-2025"] = int(fuera25)

        # ── C2 reproduce (guardia D-22): recalculado desde los marginales
        # sellados de 2025 (los mismos que COMMIT-2 usó) vs. el C2 sellado
        peor_c2 = 0.0
        sell = M._marginales_2025_sellados(inputs) if "marginales_2025_resultados" in inputs else None
        if sell is not None:
            for ka, kb in celdas_lista:
                c = M.celda_corta(cruce_id, ka, kb)
                pa, pb, pn = sell[eje_a][ka]["p"], sell[eje_b][kb]["p"], sell["nacional"]["p"]
                p_c2 = M._expit(M._logit(pa) + M._logit(pb) - M._logit(pn))
                sellado = cand_p["C2"][c]
                if sellado is not None:
                    peor_c2 = max(peor_c2, abs(p_c2 - sellado))
        out[f"{pre_out}-G-C2-REPRODUCE-MAX-ABS"] = float(peor_c2)
        if sell is not None and peor_c2 > TOL_C2:
            raise ParoDeGuardia(f"{cruce_id}: C2 recalculado no reproduce el sellado "
                               f"({peor_c2} > {TOL_C2})")

        puntuadas = 0
        gana_ambos = {k: 0 for k in RETADORES}
        indecid = {k: 0 for k in RETADORES}
        for ka, kb in celdas_lista:
            c = M.celda_corta(cruce_id, ka, kb)
            r = R[c]
            for k in CANDIDATOS:
                v = cand_p[k][c]
                d_pp[k][c] = (100.0 * abs(v - r)) if (v is not None and r is not None) else None
                out[f"{pre_out}-{c}-D-{k}"] = d_pp[k][c]
            con_soporte = out[f"{pre_out}-{c}-SOPORTE-2025"] == "SOPORTE-OK"
            puntuable = (r is not None and con_soporte
                        and all(cand_p[k][c] is not None for k in CANDIDATOS))
            out[f"{pre_out}-{c}-PUNTUADA"] = "SI" if puntuable else "NO"
            if not puntuable:
                for j in RETADORES:
                    for piso in PISOS:
                        out[f"{pre_out}-{c}-VEREDICTO-{j}-VS-{piso}"] = "NO-PUNTUADA"
                continue
            puntuadas += 1
            for j in RETADORES:
                vered = {}
                for piso in PISOS:
                    dl, dm = d_pp[j][c], d_pp[piso][c]
                    ambos_dentro = _dentro(cand_p[j][c], ICR[c]) and _dentro(cand_p[piso][c], ICR[c])
                    cerca = abs(dl - dm) < 0.5 * (100.0 * EE[c])
                    vered[piso] = "INDECIDIBLE" if (ambos_dentro or cerca) else (
                        "GANA-CHALLENGER" if dl < dm else "GANA-PISO")
                    out[f"{pre_out}-{c}-VEREDICTO-{j}-VS-{piso}"] = vered[piso]
                if all(v == "GANA-CHALLENGER" for v in vered.values()):
                    gana_ambos[j] += 1
                elif any(v == "INDECIDIBLE" for v in vered.values()):
                    indecid[j] += 1
        out[f"{pre_out}-G-PUNTUADAS-N"] = int(puntuadas)

        def _mae(k):
            v = []
            for ka2, kb2 in celdas_lista:
                cc = M.celda_corta(cruce_id, ka2, kb2)
                if out[f"{pre_out}-{cc}-PUNTUADA"] == "SI" and d_pp[k][cc] is not None:
                    v.append(d_pp[k][cc])
            return float(np.mean(v)) if v else None

        mae = {k: _mae(k) for k in CANDIDATOS}
        for k in CANDIDATOS:
            out[f"{pre_out}-G-MAE-{k}"] = mae[k]

        ganadores_pp = {}
        for j in RETADORES:
            for piso in PISOS:
                dm = (mae[piso] - mae[j]) if (mae[piso] is not None and mae[j] is not None) else None
                out[f"{pre_out}-G-DELTA-MAE-{j}-VS-{piso}-PP"] = dm
                # IC de DeltaMAE, propagado desde las réplicas de R en las
                # celdas PUNTUADA (declarado en el docstring: no es IC
                # conjunta con el candidato, sólo con R).
                reps_r = []
                celdas_p = [M.celda_corta(cruce_id, ka, kb) for ka, kb in celdas_lista
                           if out[f"{pre_out}-{M.celda_corta(cruce_id, ka, kb)}-PUNTUADA"] == "SI"]
                if celdas_p and mae[piso] is not None and mae[j] is not None:
                    rep_r_por_celda = {}
                    replicas_ola = mr.replicas_compartidas(ola25, int(contrato["seed"]["valor"]),
                                                           int(par.get("bootstrap_replicas_r", 2000)))
                    a_arr = ola25.df[eje_a].to_numpy()
                    b_arr = ola25.df[eje_b].to_numpy()
                    for ka2, kb2 in celdas_lista:
                        cc = M.celda_corta(cruce_id, ka2, kb2)
                        if cc not in celdas_p:
                            continue
                        mask = (a_arr == ka2) & (b_arr == kb2)
                        rep_r_por_celda[cc] = mr._reps_de_mascara(ola25, replicas_ola, mask)
                    n_rep_r = len(next(iter(rep_r_por_celda.values())))
                    dmae_r = np.empty(n_rep_r)
                    for rr in range(n_rep_r):
                        vals = []
                        for cc in celdas_p:
                            rv = rep_r_por_celda[cc][rr]
                            if not np.isfinite(rv) or not (0 < rv < 1):
                                continue
                            vp = 100.0 * abs(cand_p[piso][cc] - rv)
                            vj = 100.0 * abs(cand_p[j][cc] - rv)
                            vals.append(vp - vj)
                        dmae_r[rr] = np.mean(vals) if vals else np.nan
                    ok = dmae_r[np.isfinite(dmae_r)]
                    out[f"{pre_out}-G-DELTA-MAE-{j}-VS-{piso}-IC-LO"] = M._pct(ok, 2.5)
                    out[f"{pre_out}-G-DELTA-MAE-{j}-VS-{piso}-IC-HI"] = M._pct(ok, 97.5)
                    ganadores_pp[(j, piso)] = (M._pct(ok, 2.5), M._pct(ok, 97.5))
                else:
                    out[f"{pre_out}-G-DELTA-MAE-{j}-VS-{piso}-IC-LO"] = None
                    out[f"{pre_out}-G-DELTA-MAE-{j}-VS-{piso}-IC-HI"] = None

        for j in RETADORES:
            out[f"{pre_out}-G-{j}-VENCE-A-AMBOS-EN-CELDAS"] = int(gana_ambos[j])
            out[f"{pre_out}-G-{j}-INDECIDIBLES"] = int(indecid[j])
            ic_c2 = ganadores_pp.get((j, "C2"))
            out[f"{pre_out}-G-{j}-GANA"] = _estado_gana(ic_c2, delta_mae_umbral)

        # ── B-bis del cruce ────────────────────────────────────────────────
        if puntuadas == 0 or out[f"{pre_out}-G-CELDAS-FUERA-DE-SOPORTE-2025"] >= int(
                par["fuera_de_soporte_global"][cruce_id] if isinstance(par.get("fuera_de_soporte_global"), dict)
                else round(len(celdas_lista) / 3)):
            bbis = "FUERA-DE-SOPORTE-GLOBAL"
        else:
            nadie_c1 = all(out[f"{pre_out}-G-{j}-GANA"] == "NO" for j in RETADORES)
            venc = [j for j in RETADORES if out[f"{pre_out}-G-{j}-GANA"] == "SI"]
            if venc:
                bbis = ("LIMITA-C2" if len(venc) == 2 else "LIMITA-C2-SOBRE-CUANTO-ENCOGER")
            else:
                his = [out[f"{pre_out}-G-DELTA-MAE-{j}-VS-C2-IC-HI"] for j in RETADORES]
                his_def = [h for h in his if h is not None]
                if his_def and all(h <= delta_mae_umbral for h in his_def):
                    bbis = "CORROBORADA"
                else:
                    bbis = "FALSADOR-DEBIL"
        out[f"{pre_out}-G-B-BIS"] = bbis
        if bbis != "FUERA-DE-SOPORTE-GLOBAL":
            lectura_bbis_global.append(bbis)

    orden_precedencia = ["LIMITA-C2", "LIMITA-C2-SOBRE-CUANTO-ENCOGER", "FALSADOR-DEBIL", "CORROBORADA"]
    agregado = next((v for v in orden_precedencia if v in lectura_bbis_global),
                    "SIN-CRUCES-CON-SOPORTE" if not lectura_bbis_global else lectura_bbis_global[0])
    out["RESULT-TRA-ENCOGIDA-ARB-G-B-BIS-AGREGADO"] = agregado
    out["RESULT-TRA-ENCOGIDA-ARB-G-CHAMPION"] = "NINGUNO"
    out["RESULT-TRA-ENCOGIDA-ARB-G-ADOPCION"] = "NINGUNA"
    return out


def esquema_resultados(*_args):
    filas = [
        {"id": "RESULT-TRA-ENCOGIDA-ARB-G-INPUT-ENVIPE2025-CSV-SHA256", "tipo": "texto", "unidad": "hash sha256"},
        {"id": "RESULT-TRA-ENCOGIDA-ARB-G-R-FILAS-UNIVERSO", "tipo": "entero", "unidad": "delitos"},
        {"id": "RESULT-TRA-ENCOGIDA-ARB-G-R-ESTRATOS", "tipo": "entero", "unidad": "estratos"},
        {"id": "RESULT-TRA-ENCOGIDA-ARB-G-R-UPM", "tipo": "entero", "unidad": "UPM"},
        {"id": "RESULT-TRA-ENCOGIDA-ARB-G-B-BIS-AGREGADO", "tipo": "texto", "unidad": "categoría"},
        {"id": "RESULT-TRA-ENCOGIDA-ARB-G-CHAMPION", "tipo": "texto", "unidad": "categoría"},
        {"id": "RESULT-TRA-ENCOGIDA-ARB-G-ADOPCION", "tipo": "texto", "unidad": "categoría"},
    ]
    for cruce_id in M.CRUCES:
        pre = prefijo(cruce_id)
        filas += [
            {"id": f"{pre}-G-COBERTURA-CRUCE", "tipo": "proporcion", "unidad": "proporción [0,1]"},
            {"id": f"{pre}-G-CELDAS-FUERA-DE-SOPORTE-2025", "tipo": "entero", "unidad": "celdas"},
            {"id": f"{pre}-G-C2-REPRODUCE-MAX-ABS", "tipo": "flotante", "unidad": "diferencia de proporción"},
            {"id": f"{pre}-G-PUNTUADAS-N", "tipo": "entero", "unidad": "celdas"},
            {"id": f"{pre}-G-B-BIS", "tipo": "texto", "unidad": "categoría"},
        ]
        for k in CANDIDATOS:
            filas.append({"id": f"{pre}-G-MAE-{k}", "tipo": "flotante", "unidad": "pp",
                         "permite_no_estimable": True})
        for j in RETADORES:
            filas += [
                {"id": f"{pre}-G-{j}-VENCE-A-AMBOS-EN-CELDAS", "tipo": "entero", "unidad": "celdas"},
                {"id": f"{pre}-G-{j}-INDECIDIBLES", "tipo": "entero", "unidad": "celdas"},
                {"id": f"{pre}-G-{j}-GANA", "tipo": "texto", "unidad": "categoría"},
            ]
            for piso in PISOS:
                filas += [
                    {"id": f"{pre}-G-DELTA-MAE-{j}-VS-{piso}-PP", "tipo": "flotante", "unidad": "pp",
                     "permite_no_estimable": True},
                    {"id": f"{pre}-G-DELTA-MAE-{j}-VS-{piso}-IC-LO", "tipo": "flotante", "unidad": "pp",
                     "permite_no_estimable": True},
                    {"id": f"{pre}-G-DELTA-MAE-{j}-VS-{piso}-IC-HI", "tipo": "flotante", "unidad": "pp",
                     "permite_no_estimable": True},
                ]
        for ka, kb in M.celdas(cruce_id):
            c = M.celda_corta(cruce_id, ka, kb)
            base = f"{pre}-{c}"
            filas += [
                {"id": f"{base}-R-N", "tipo": "entero", "unidad": "delitos"},
                {"id": f"{base}-SOPORTE-2025", "tipo": "texto", "unidad": "categoría"},
                {"id": f"{base}-R-P", "tipo": "proporcion", "unidad": "proporción [0,1]", "permite_no_estimable": True},
                {"id": f"{base}-R-IC-LO", "tipo": "proporcion", "unidad": "proporción [0,1]", "permite_no_estimable": True},
                {"id": f"{base}-R-IC-HI", "tipo": "proporcion", "unidad": "proporción [0,1]", "permite_no_estimable": True},
                {"id": f"{base}-R-EE", "tipo": "flotante", "unidad": "error estándar en proporción", "permite_no_estimable": True},
                {"id": f"{base}-PUNTUADA", "tipo": "texto", "unidad": "categoría"},
            ]
            for k in CANDIDATOS:
                filas.append({"id": f"{base}-D-{k}", "tipo": "flotante", "unidad": "pp", "permite_no_estimable": True})
            for j in RETADORES:
                for piso in PISOS:
                    filas.append({"id": f"{base}-VEREDICTO-{j}-VS-{piso}", "tipo": "texto", "unidad": "categoría"})
    return filas
