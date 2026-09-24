"""Participación federal publicada por SICEE-INE: votos totales / lista nominal.

Gobernado por forense/prereg-caja/INE-SICEE-PARTICIPACION-spec-v1_0.md y su
sucesor v1_1 (null publicado -> SIN-DATO-PUBLICADO).
Registro administrativo: sin IC, sin suma entre cargos ni entre distribuciones.
"""
from __future__ import annotations

import json

PID = "a6_sicee_participacion_nacional_1991_2024"
VACIO_SICEE = "sinregistro"  # marcador literal de vacío publicado por SICEE (v1_1)


def numero(valor, entero):
    texto = str(valor).strip().replace(",", "").replace("%", "").replace(" ", "")
    if texto == "" or texto.lower() in {"none", "nan", "null"}:
        raise ValueError(f"valor no numérico: {valor!r}")
    return int(texto) if entero else float(texto)


def filas_medidas(registros, cargos):
    salida = []
    for r in registros:
        cargo = str(r["cargo"])
        if cargo not in cargos:
            raise ValueError(f"cargo fuera de contrato: {cargo}")
        tv = None if r["total_votos"] is None else numero(r["total_votos"], True)
        ln = None if r["lista_nominal"] is None else numero(r["lista_nominal"], True)
        pub = (None if r["porcentaje_participacion"] in (None, VACIO_SICEE)
               else numero(r["porcentaje_participacion"], False))
        base = {"cargo": cargo, "anio": int(r["anio"]), "distribucion": int(r["distribucion"]),
                "total_votos": tv, "lista_nominal": ln, "tasa_publicada_pct": pub}
        if tv is None or ln is None:
            salida.append({**base, "estado": "SIN-DATO-PUBLICADO", "tasa": None, "dif_pp": None})
            continue
        if ln <= 0:
            salida.append({**base, "estado": "NO-ESTIMABLE", "tasa": None, "dif_pp": None})
            continue
        tasa = tv / ln
        salida.append({**base, "estado": "ESTIMADA", "tasa": tasa,
                       "dif_pp": None if pub is None else round(100 * tasa - pub, 6)})
    salida.sort(key=lambda x: (x["cargo"], x["anio"], x["distribucion"]))
    pares = {}
    for f in salida:
        pares.setdefault((f["cargo"], f["anio"]), []).append(f)
    diagnostico = []
    for (cargo, anio), fs in sorted(pares.items()):
        diagnostico.append({
            "cargo": cargo, "anio": anio, "n_distribuciones": len(fs),
            "total_votos_igual": len({f["total_votos"] for f in fs}) == 1,
            "lista_nominal_igual": len({f["lista_nominal"] for f in fs}) == 1})
    return salida, diagnostico


def medir(inputs, contrato):
    with open(inputs[PID]["ruta_absoluta"], encoding="utf-8") as fh:
        registros = json.load(fh)
    cargos = set(contrato["parametros"]["cargos"])
    filas, diagnostico = filas_medidas(registros, cargos)
    tabla = {"filas": filas, "diagnostico_distribucion": diagnostico}
    return {"RESULT-INE-PISOS-SICEE-FILAS": len(registros),
            "RESULT-INE-PISOS-SICEE-TABLA": json.dumps(
                tabla, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                allow_nan=False)}
