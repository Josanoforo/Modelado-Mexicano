#!/usr/bin/env python3
"""Reconstrucción CALC-MMSI-PISOS-2016-0001 desde paquete/docs/spec-humana.md.

Ejecutar desde el directorio de trabajo: python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json y salida/diagnostico.json.
"""
import csv
import json
import os

import numpy as np
import pandas as pd

PAQ = "paquete"
SAL = "salida"
CSV = os.path.join(PAQ, "datos", "mmsi2016.csv")
ESQ = os.path.join(PAQ, "esquema-identidades.tsv")

# Columnas autorizadas (y únicas leídas)
COLS = ["P1_1", "P1_2", "Factor_Per", "upm_ENH", "est_dis_ENH", "NivEsc_Inf",
        "DivOcu_Act", "Per_SitEco", "P10_1", "P10_2", "P10_3", "tam_loc_ENH"]

IDENTIDAD = {"paquete": "mmsi-pisos-2016-0001",
             "version_entrada": "validacion-continua-1",
             "sha256_entrada": "33f97f5f4db2f51c79f0624ccfb52175c3830c9e6f1d7268b365df7a57c4cefd"}

SEED = 20260927
B = 2000
BLOQUE = 50

# ---------------------------------------------------------------- conductas (spec §2)
# (variable, códigos UNO, códigos CERO, filtro de sexo P1_1 o None)
CONDUCTAS = {
    "educacion-superior": ("NivEsc_Inf", {"7"}, {"1", "2", "3", "4", "5", "6"}, None),
    "educacion-superior-mujer": ("NivEsc_Inf", {"7"}, {"1", "2", "3", "4", "5", "6"}, "2"),
    "educacion-superior-hombre": ("NivEsc_Inf", {"7"}, {"1", "2", "3", "4", "5", "6"}, "1"),
    "ocupacion-directiva": ("DivOcu_Act", {"01"},
                            {"02", "03", "04", "05", "06", "07", "08", "09"}, None),
    "percibe-mejora-socioeconomica": ("Per_SitEco", {"1"}, {"2", "3"}, None),
}

# ---------------------------------------------------------------- ejes (spec §3)
TONOS = "ABCDEFGHIJK"


def segmento_mask(d, eje, seg):
    if eje == "TOTAL" and seg == "TODOS":
        return pd.Series(True, index=d.index)
    if eje == "SEXO":
        return d["P1_1"] == {"HOMBRE": "1", "MUJER": "2"}[seg]
    if eje == "EDAD":
        lo, hi = (int(x) for x in seg.split("-"))
        return (d["edad"] >= lo) & (d["edad"] <= hi)
    if eje == "TONO":
        if seg.startswith("TONO-"):
            letra = seg[len("TONO-"):]
            return d["tono"] == TONOS.index(letra) + 1
        if seg.startswith("TRAMO-"):
            a, b = seg[len("TRAMO-"):].split("-")
            return (d["tono"] >= TONOS.index(a) + 1) & (d["tono"] <= TONOS.index(b) + 1)
    if eje == "ORIGEN":
        cod = {"AUTOADSCRITO-NEGRA-MULATA": "1", "AUTOADSCRITO-INDIGENA": "2",
               "AUTOADSCRITO-MESTIZA": "3", "AUTOADSCRITO-BLANCA": "4",
               "AUTOADSCRITO-OTRA": "5"}[seg]
        return d["P10_3"] == cod
    if eje == "LENGUA":
        return d["P10_1"] == {"INDIGENA-SI": "1", "INDIGENA-NO": "2"}[seg]
    if eje == "TAMLOC":
        cod = {"100MIL-MAS": "1", "15MIL-99MIL": "2", "2500-14999": "3",
               "MENOS-2500": "4"}[seg]
        return d["tam_loc_ENH"] == cod
    raise KeyError((eje, seg))


def r(x):
    return repr(float(x))


def main():
    esquema = pd.read_csv(ESQ, sep="\t", dtype=str, keep_default_na=False)

    d = pd.read_csv(CSV, usecols=COLS, dtype=str, keep_default_na=False,
                    encoding="utf-8-sig")
    for c in COLS:
        d[c] = d[c].str.strip()
    n_archivo = len(d)

    # ------------------------------------------------ universo y validez (spec §1)
    d["edad"] = pd.to_numeric(d["P1_2"], errors="coerce")
    en_universo = (d["edad"] >= 25) & (d["edad"] <= 64)
    w = pd.to_numeric(d["Factor_Per"], errors="coerce")
    valido = (w > 0) & (d["est_dis_ENH"] != "") & (d["upm_ENH"] != "")
    excl_universo = int((~en_universo).sum())
    excl_diseno = int((en_universo & ~valido).sum())
    d = d[en_universo & valido].copy()
    d["w"] = w[d.index].astype(float)
    d["tono"] = pd.to_numeric(d["P10_2"], errors="coerce")

    # ------------------------------------------------ motor bootstrap (spec §4)
    upm_keys = d[["est_dis_ENH", "upm_ENH"]].drop_duplicates().sort_values(
        ["est_dis_ENH", "upm_ENH"]).reset_index(drop=True)
    upm_keys["j"] = np.arange(len(upm_keys))
    d = d.merge(upm_keys, on=["est_dis_ENH", "upm_ENH"], how="left")
    J = len(upm_keys)
    estratos = []
    for h, g in upm_keys.groupby("est_dis_ENH", sort=True):
        estratos.append((h, g["j"].to_numpy()))
    n_h = {h: len(js) for h, js in estratos}
    singletons = [h for h, n in n_h.items() if n < 2]

    rng = np.random.Generator(np.random.PCG64(SEED))
    F = np.zeros((B, J))  # factor de réplica por UPM (Rao-Wu, m_h = n_h - 1)
    for b0 in range(0, B, BLOQUE):
        for h, js in estratos:
            n = len(js)
            if n < 2:
                F[b0:b0 + BLOQUE, js] = 1.0
                continue
            draws = rng.integers(0, n, size=(BLOQUE, n - 1))
            cnt = np.zeros((BLOQUE, n))
            np.add.at(cnt, (np.repeat(np.arange(BLOQUE), n - 1), draws.ravel()), 1.0)
            F[b0:b0 + BLOQUE, js] = cnt * (n / (n - 1.0))

    filas = []
    diag_llaves = []
    for _, e in esquema.iterrows():
        llave, unidad = e["llave"], e["unidad"]
        var, uno, cero, sexo = CONDUCTAS[e["conducta"]]
        m_seg = segmento_mask(d, e["eje"], e["segmento"])
        m_sexo = (d["P1_1"] == sexo) if sexo else pd.Series(True, index=d.index)
        dom = m_seg & m_sexo
        y1 = d[var].isin(uno)
        y0 = d[var].isin(cero)
        val = dom & (y1 | y0)
        n_dom = int(dom.sum())
        info = {
            "llave": llave,
            "filas_archivo": n_archivo,
            "excluidas_fuera_universo_25_64": excl_universo,
            "excluidas_diseno_invalido": excl_diseno,
            "excluidas_fuera_de_segmento": int((~m_seg).sum()),
            "excluidas_filtro_sexo_conducta": int((m_seg & ~m_sexo).sum()),
            "n_dominio": n_dom,
            "excluidas_conducta_sin_dato": int((dom & ~(y1 | y0)).sum()),
            "detalle_conducta_sin_dato": {
                (k if k != "" else "blanco"): int(v)
                for k, v in d.loc[dom & ~(y1 | y0), var].value_counts().items()},
            "n_valido": int(val.sum()),
            "n_uno": int((val & y1).sum()),
            "upm_con_casos": int(d.loc[val, "j"].nunique()),
            "estratos_con_casos": int(d.loc[val, "est_dis_ENH"].nunique()),
        }
        fila = {"llave": llave, "unidad": unidad}
        if info["n_valido"] == 0:
            fila["estado"] = "DENOMINADOR-CERO"
            fila["motivo"] = "dominio sin casos válidos observados bajo la spec"
            filas.append(fila)
            diag_llaves.append(info)
            continue
        wv = np.where(val, d["w"].to_numpy(), 0.0)
        num_j = np.bincount(d["j"], weights=wv * y1.to_numpy(), minlength=J)
        den_j = np.bincount(d["j"], weights=wv, minlength=J)
        p = num_j.sum() / den_j.sum()
        fila["estado"] = "RECONSTRUIDO"
        fila["punto"] = r(p)
        den_b = F @ den_j
        num_b = F @ num_j
        cero_b = int((den_b <= 0).sum())
        info["replicas_denominador_cero"] = cero_b
        info["suma_pesos_valida"] = float(den_j.sum())
        if cero_b > 0:
            fila["estado_ic"] = "NO-IDENTIFICADA"
            fila["motivo_ic"] = (f"{cero_b} de {B} réplicas bootstrap sin casos válidos en el "
                                 "dominio (denominador cero); contrato conservador: no se "
                                 "descartan réplicas")
        else:
            pb = num_b / den_b
            lo, hi = np.percentile(pb, [2.5, 97.5])
            info["replicas_sd"] = float(np.std(pb, ddof=1))
            if hi - lo <= 0:
                fila["estado_ic"] = "NO-IDENTIFICADA"
                fila["motivo_ic"] = ("distribución bootstrap degenerada (todas las réplicas "
                                     f"iguales a {r(p)}): varianza no identificada")
            else:
                fila["estado_ic"] = "CALCULADO"
                fila["ic95_inf"] = r(lo)
                fila["ic95_sup"] = r(hi)
        filas.append(fila)
        diag_llaves.append(info)

    res = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    with open(os.path.join(SAL, "resultado.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)

    diag = {
        "paquete": IDENTIDAD["paquete"],
        "columnas_leidas": COLS,
        "motor": {
            "rng": f"numpy.random.Generator(PCG64({SEED}))",
            "replicas": B, "bloque": BLOQUE,
            "upm": J, "estratos": len(estratos),
            "estratos_una_upm": singletons,
            "percentiles": "numpy.percentile(método 'linear'), 2.5 y 97.5",
        },
        "universo": {"filas_archivo": n_archivo,
                     "excluidas_fuera_universo_25_64": excl_universo,
                     "excluidas_diseno_invalido": excl_diseno,
                     "filas_universo_valido": int(len(d))},
        "decisiones": DECISIONES,
        "llaves": diag_llaves,
    }
    with open(os.path.join(SAL, "diagnostico.json"), "w", encoding="utf-8") as f:
        json.dump(diag, f, ensure_ascii=False, indent=1)


DECISIONES = [
    {"decision": "Esquema de réplica: bootstrap de reescalamiento Rao-Wu con m_h = n_h - 1 UPM "
                 "extraídas con reemplazo en cada estrato; factor de réplica de la UPM = "
                 "(n_h/(n_h-1)) × veces extraída, multiplicado por Factor_Per.",
     "frase": "bootstrap de UPM `upm_ENH` dentro de estrato `est_dis_ENH`",
     "alternativas": "bootstrap ingenuo con m_h = n_h sin reescalar; la receta ENDISEG citada "
                     "por sha256 no está en el paquete."},
    {"decision": "Orden de consumo del generador: 40 bloques de 50 réplicas; en cada bloque, "
                 "estratos en orden lexicográfico de est_dis_ENH y UPM en orden lexicográfico "
                 "de upm_ENH; rng.integers(0, n_h, size=(50, n_h-1)).",
     "frase": "`PCG64(20260927)`, 2 000 réplicas, bloques de 50",
     "alternativas": "cualquier otro orden de consumo; la spec no lo fija en prosa."},
    {"decision": "Un único conjunto de 2000 réplicas de diseño, común a todas las llaves.",
     "frase": "Receta y motor por sha256 (los de ENDISEG, misma spec §4)",
     "alternativas": "réplicas independientes por llave o por eje."},
    {"decision": "Percentiles con numpy.percentile interpolación lineal.",
     "frase": "percentiles 2.5/97.5",
     "alternativas": "percentil empírico por orden (inferior/superior, nearest)."},
    {"decision": "«Contrato conservador»: no se descartan réplicas; si alguna réplica deja el "
                 "dominio con denominador cero, o la distribución bootstrap es degenerada "
                 "(ancho cero), el IC se reporta NO-IDENTIFICADA con el punto intacto.",
     "frase": "percentiles 2.5/97.5, contrato conservador",
     "alternativas": "descartar réplicas con denominador cero; reportar IC de ancho cero."},
    {"decision": "Denominador de cada proporción: personas del dominio con conducta en UNO o "
                 "CERO; los códigos fuera de ambas listas (NivEsc_Inf 9/blanco, DivOcu_Act "
                 "99/blanco) salen de numerador y denominador. DivOcu_Act blanco (por pase, "
                 "no ocupados) queda fuera, no como CERO.",
     "frase": "`NivEsc_Inf` 9 y blanco, `DivOcu_Act` 99 y blanco: fuera.",
     "alternativas": "tratar blanco por pase de DivOcu_Act como CERO (población total)."},
    {"decision": "Las exclusiones de conducta se aplican por llave (conducta), no como filtro "
                 "global de filas: una persona sin NivEsc_Inf sigue contando para "
                 "OCUPACION-DIRECTIVA.",
     "frase": "Un eje a la vez; nunca cruces",
     "alternativas": "caso completo sobre las tres conductas."},
    {"decision": "Para ejes, personas con código fuera de las categorías del segmento (p. ej. "
                 "P10_3 = 9) sólo quedan fuera de los segmentos de ese eje; en TOTAL y en "
                 "otros ejes permanecen.",
     "frase": "5 Otra raza; 9 No sabe fuera",
     "alternativas": "excluir P10_3 = 9 del universo de todas las llaves."},
    {"decision": "EDUCACION-SUPERIOR-MUJER/-HOMBRE: dominio = segmento del eje ∩ P1_1 = 2/1; "
                 "no se considera cruce de ejes.",
     "frase": "EDUCACION-SUPERIOR-MUJER es una conducta de subpoblación, no un cruce de ejes",
     "alternativas": "ninguna razonable."},
    {"decision": "Tono: P10_2 01..11 → A..K; TRAMO-A-E = 01..05, F-G = 06..07, H-K = 08..11.",
     "frase": "01–11 = A…K, once categorías · TONO-TRAMO (A–E, F–G, H–K)",
     "alternativas": "ninguna."},
    {"decision": "Edad de P1_2 en años cumplidos; universo 25 ≤ P1_2 ≤ 64 inclusive. Cada fila "
                 "del archivo se toma como la persona informante (el archivo es del módulo, "
                 "una persona seleccionada por hogar).",
     "frase": "persona informante de 25 a 64 años (`P1_2`)",
     "alternativas": "ninguna con las columnas autorizadas."},
    {"decision": "Estado de identidad: se escribe literal la identidad del encargo; el sha256 "
                 "del CSV de paquete/datos no se usa para ella.",
     "frase": "identidad = {...} (encargo)",
     "alternativas": "—"},
]


if __name__ == "__main__":
    main()
