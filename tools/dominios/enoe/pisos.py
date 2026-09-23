"""Estimaciones ENOE sobre SDEM, con réplicas por UPM dentro de estrato.

El primer resultado que produzca este procedimiento es el que se reporta.
No abre la ola reservada ni construye enlaces longitudinales.
"""
from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import defaultdict

import numpy as np
import pandas as pd


VARIABLES = {
    "r_def", "c_res", "eda", "sex", "fac", "fac_tri", "est_d",
    "est_d_tri", "upm", "ent", "t_loc", "niv_ins", "clase1", "clase2",
    "emp_ppal", "tue_ppal", "sub_o", "busqueda", "pnea_est", "hrsocup",
    "ingocup", "t_tra", "tip_con", "remune2c",
}

# (conducta, denominador, numerador/valor, unidad). Los códigos vienen de
# con_basedatos_proy2010.pdf y enoe_325_fd_c_bas_amp.pdf; la especificación
# humana declara la cobertura y los saltos. Un blanco no es una respuesta 0.
CONDUCTAS = (
    ("empleo_informal", "ocupados_emp", "emp_ppal=1", "proporcion"),
    ("sector_informal", "ocupados", "tue_ppal=1", "proporcion"),
    ("subocupacion", "ocupados", "sub_o=1", "proporcion"),
    ("busca_otro_trabajo", "ocupados_busqueda", "busqueda=1", "proporcion"),
    ("pluriempleo", "ocupados_ttra", "t_tra=2", "proporcion"),
    ("sin_contrato_escrito", "subordinados_contrato", "tip_con=5", "proporcion"),
    ("jornada_mas_50_horas", "ocupados_horas", "hrsocup>50", "proporcion"),
    ("desocupacion", "pea", "clase2=2", "proporcion"),
    ("desaliento_desistio", "pnea", "pnea_est=1", "proporcion"),
    ("desaliento_sin_posibilidades", "pnea", "pnea_est=2", "proporcion"),
    ("no_participacion_obligaciones", "pnea", "pnea_est=4", "proporcion"),
    ("horas_ocupado", "ocupados_horas", "hrsocup", "horas_por_semana"),
    ("ingreso_ocupado_nominal", "ocupados_ingreso", "ingocup", "pesos_por_mes"),
)

COLUMNA_CONDUCTA = {
    "empleo_informal": "emp_ppal", "sector_informal": "tue_ppal",
    "subocupacion": "sub_o", "busca_otro_trabajo": "busqueda",
    "pluriempleo": "t_tra", "desocupacion": "clase2",
    "sin_contrato_escrito": "tip_con", "jornada_mas_50_horas": "hrsocup",
    "desaliento_desistio": "pnea_est", "desaliento_sin_posibilidades": "pnea_est",
    "no_participacion_obligaciones": "pnea_est", "horas_ocupado": "hrsocup",
    "ingreso_ocupado_nominal": "ingocup",
}


def _col(frame, name):
    if name not in frame:
        return pd.Series("", index=frame.index, dtype="string")
    return frame[name].fillna("").astype("string").str.strip()


def _numero(frame, name):
    return pd.to_numeric(_col(frame, name), errors="coerce")


def _segmentos(f):
    edad = _numero(f, "eda")
    nivel = _numero(f, "niv_ins")
    loc = _numero(f, "t_loc")
    ent = _numero(f, "ent")
    return {
        "nacional": pd.Series("NAC", index=f.index),
        "sexo": _col(f, "sex").map({"1": "HOMBRE", "2": "MUJER"}),
        "edad": pd.cut(edad, [14, 29, 44, 59, 98],
                         labels=["15-29", "30-44", "45-59", "60+"]).astype("string"),
        "escolaridad": nivel.map({1: "PRIM-INCOMPLETA", 2: "PRIM-COMPLETA",
                                   3: "SECUNDARIA", 4: "MEDIA-SUPERIOR"}),
        "localidad": loc.map({1: "100K+", 2: "15K-99K", 3: "2K5-15K", 4: "MENOS-2K5"}),
        "entidad": ent.where(ent.between(1, 32)).map(lambda v: f"{int(v):02d}" if pd.notna(v) else None),
    }


def _lee_sdem(ruta):
    with zipfile.ZipFile(ruta) as z:
        miembros = [n for n in z.namelist() if "sdemt" in n.lower() and n.lower().endswith(".csv")]
        if len(miembros) != 1:
            raise ValueError(f"SDEM CSV único no encontrado: {len(miembros)} miembros")
        with z.open(miembros[0]) as fh:
            return pd.read_csv(fh, encoding="latin-1", dtype="string", low_memory=False,
                               usecols=lambda c: c.lower() in VARIABLES).rename(columns=str.lower)


def _estadistico(f, mascara, valor, segmento, replicas, rng):
    """Media de razón, réplicas PSU/estrato; suprime dominios sin soporte."""
    v = pd.to_numeric(valor, errors="coerce")
    idx = mascara & v.notna() & segmento.notna()
    if not idx.any():
        return []
    t = pd.DataFrame({"segmento": segmento[idx].astype(str),
                      "w": f.loc[idx, "_w"].to_numpy(),
                      "v": v[idx].to_numpy(),
                      "estrato": f.loc[idx, "_estrato"].astype(str).to_numpy(),
                      "upm": f.loc[idx, "upm"].astype(str).to_numpy()})
    t["wv"] = t.w * t.v
    t["w2"] = t.w * t.w
    out = []
    for seg, s in t.groupby("segmento", sort=True):
        n = len(s)
        den = float(s.w.sum())
        n_eff = den * den / float(s.w2.sum()) if den else 0.0
        psu = s.groupby(["estrato", "upm"], sort=True)[["w", "wv"]].sum()
        k = len(psu)
        if n < 100 or n_eff < 100 or k < 2:
            out.append((seg, None, None, None, n, n_eff, k, "SUPRIMIDA-N-O-PSU"))
            continue
        punto = float(s.wv.sum() / den)
        # Plan de multiplicidades por PSU, re-muestreado dentro de cada
        # estrato. Las UPM de una sola unidad aportan el mismo valor.
        draws = np.zeros((replicas, k), dtype=np.int16)
        estratos = psu.index.get_level_values(0).to_numpy()
        for e in np.unique(estratos):
            ix = np.flatnonzero(estratos == e)
            for b in range(replicas):
                draws[b, ix] = rng.multinomial(len(ix), [1 / len(ix)] * len(ix))
        a = psu[["w", "wv"]].to_numpy(dtype=float)
        sums = draws @ a
        rb = np.divide(sums[:, 1], sums[:, 0], out=np.full(replicas, np.nan),
                       where=sums[:, 0] > 0)
        rb = rb[np.isfinite(rb)]
        if len(rb) < int(.95 * replicas):
            out.append((seg, None, None, None, n, n_eff, k, "SUPRIMIDA-REPLICAS"))
            continue
        lo, hi = np.percentile(rb, [2.5, 97.5])
        cv = float(np.std(rb, ddof=1) / abs(punto)) if punto else None
        calidad = "ALTA" if cv is not None and cv < .15 else ("MODERADA" if cv is not None and cv < .30 else "BAJA")
        out.append((seg, punto, float(lo), float(hi), n, n_eff, k, calidad))
    return out


def medir_ola(ruta, ola, era, replicas=200, semilla=42):
    f = _lee_sdem(ruta)
    fac = "fac" if era == "clasica" else "fac_tri"
    est = "est_d" if era == "clasica" else "est_d_tri"
    oblig = {"r_def", "c_res", "eda", "sex", "upm", fac, est, "ent", "clase1", "clase2"}
    falta = oblig - set(f)
    if falta:
        raise ValueError(f"{ola}: faltan columnas obligatorias {sorted(falta)}")
    f["_w"] = _numero(f, fac)
    f["_estrato"] = _col(f, est)
    base = ((_numero(f, "r_def") == 0) & _numero(f, "c_res").isin([1, 3]) &
            _numero(f, "eda").between(15, 98) & f._w.gt(0) &
            _col(f, "upm").ne("") & f._estrato.ne(""))
    clase1, clase2 = _numero(f, "clase1"), _numero(f, "clase2")
    emp, tue, ttra = _numero(f, "emp_ppal"), _numero(f, "tue_ppal"), _numero(f, "t_tra")
    bus = _numero(f, "busqueda")
    pnea_est = _numero(f, "pnea_est")
    tip_con = _numero(f, "tip_con")
    remune2c = _numero(f, "remune2c")
    hrs, ing = _numero(f, "hrsocup"), _numero(f, "ingocup")
    denominadores = {
        "ocupados": base & clase2.eq(1),
        "ocupados_emp": base & clase2.eq(1) & emp.isin([1, 2]),
        "ocupados_busqueda": base & clase2.eq(1) & bus.isin([1, 2]),
        "ocupados_ttra": base & clase2.eq(1) & ttra.isin([1, 2]),
        "subordinados_contrato": base & clase2.eq(1) & remune2c.isin([1, 2]) & tip_con.isin([1, 2, 3, 4, 5]),
        "ocupados_horas": base & clase2.eq(1) & hrs.between(1, 168),
        "ocupados_ingreso": base & clase2.eq(1) & ing.between(1, 999998),
        "pea": base & clase1.eq(1),
        "pnea": base & clase1.eq(2) & pnea_est.isin([1, 2, 3, 4, 5, 6]),
    }
    def flag(serie, codigo):
        return serie.eq(codigo).fillna(False).astype(float)

    valores = {"emp_ppal=1": flag(emp, 1), "tue_ppal=1": flag(tue, 1),
               "sub_o=1": flag(_numero(f, "sub_o"), 1),
               "busqueda=1": flag(bus, 1), "t_tra=2": flag(ttra, 2),
               "tip_con=5": flag(tip_con, 5), "hrsocup>50": hrs.gt(50).fillna(False).astype(float),
               "clase2=2": flag(clase2, 2),
               "pnea_est=1": flag(pnea_est, 1),
               "pnea_est=2": flag(pnea_est, 2),
               "pnea_est=4": flag(pnea_est, 4),
               "hrsocup": hrs, "ingocup": ing}
    rng = np.random.default_rng(semilla)
    segmentos = _segmentos(f)
    filas = []
    for conducta, den, v, unidad in CONDUCTAS:
        if COLUMNA_CONDUCTA[conducta] not in f:
            filas.append({"ola": ola, "era": era, "conducta": conducta,
                          "eje": "nacional", "segmento": "NAC", "unidad": unidad,
                          "punto": None, "ic95_lo": None, "ic95_hi": None, "n": 0,
                          "n_efectivo_kish": 0.0, "upm": 0,
                          "calidad": "NO-ESTIMABLE-COLUMNA-AUSENTE"})
            continue
        for eje, seg in segmentos.items():
            for categoria, punto, lo, hi, n, neff, psu, calidad in _estadistico(
                    f, denominadores[den], valores[v], seg, replicas, rng):
                filas.append({"ola": ola, "era": era, "conducta": conducta,
                              "eje": eje, "segmento": categoria, "unidad": unidad,
                              "punto": punto, "ic95_lo": lo, "ic95_hi": hi,
                              "n": n, "n_efectivo_kish": round(neff, 2),
                              "upm": psu, "calidad": calidad})
    return filas, int(base.sum()), len(f)


def medir(inputs, contrato):
    olas = contrato["parametros"]["olas"]
    replicas = int(contrato["parametros"]["replicas"])
    semilla = int(contrato["seed"]["valor"])
    todas = []
    n_base = n_leidas = 0
    for i, o in enumerate(olas):
        filas, nb, nl = medir_ola(inputs[o["id"]]["ruta_absoluta"],
                                  o["ola"], o["era"], replicas, semilla + i)
        todas.extend(filas)
        n_base += nb
        n_leidas += nl
    return {"RESULT-ENOE-PISOS-TABLA": json.dumps(todas, ensure_ascii=False,
                                                     sort_keys=True, separators=(",", ":")),
            "RESULT-ENOE-PISOS-OLAS": len(olas),
            "RESULT-ENOE-PISOS-FILAS-LEIDAS": n_leidas,
            "RESULT-ENOE-PISOS-PERSONAS-BASE": n_base,
            "RESULT-ENOE-PISOS-CELDAS": len(todas)}
