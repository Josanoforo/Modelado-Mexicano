#!/usr/bin/env python3
"""Medidor de APERTURA de ENIGH 2024 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-ENIGH-2024-spec-v1_0.md`; contrato: `APERTURA-ENIGH-2024-spec.yaml`;
receta: `RECETA-APERTURA-ENIGH-2024.md`. NO SE HA CORRIDO sobre ENIGH 2024: corre sólo en caja, en el
commit de apertura que mesa autorice.

Unidad HOGAR; ponderador `factor`. Una apertura sirve a los tres contendientes sellados (E.6):
  · CONSUMO — celdas de `CALC-ENIGH-CONSUMO-PISOS-0002` (PART-*, HOG-*; MEDIA-* fuera: media en pesos sin
    IC calibrado), recodificación de su medidor sellado (`prepara`, `conducta`, `ejes_de`); lo/hi = su ICC
    de persistencia sobre el piso 2022. `CALC-ENIGH-CONSUMO-PISOS-0001` comparte procedimiento e ids: queda
    servido por las mismas R y apartado de la primaria (SUSTITUIDO-POR 0002; spec §4).
  · PDR1 — celdas de `CALC-PDR1-ENIGH2022-0001` (PRIV, ASIPRIV por ámbito × decil/bloque, CARGA, PRIV por
    segmento), recodificación de su medidor sellado (`prepara`); lo/hi = su IC95 de diseño 2022.
R = Σw·y/Σw (razón de totales para PART-* y CARGA) por categoría de UN eje a la vez. Guardia E.6: auditoría
AST de este archivo antes de leer un byte; `guardia_apertura.proporcion_por_grupo` es el único agregador.
"""
from __future__ import annotations

import io
import os
import zipfile

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENIGH-2024"
P = "RESULT-APERTURA-ENIGH-2024"
OLA = "2024"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

CONSUMO = ("consumo_medidor", "data/corrida0/CALC-ENIGH-CONSUMO-PISOS-0002/medidor.py",
           "0c173db6f480b7b21da328d88df84c11ef7faf7b03b44bef1cffb619b21f90a4")
CONSUMO_PISO = ("consumo_resultados", "data/corrida0/CALC-ENIGH-CONSUMO-PISOS-0002/resultados.json",
                "d4f5f2fbd7cce9ca2fd54d23e8e2eb79c77284ba05113330566e9f3553da83a1")
PDR1 = ("pdr1_medidor", "data/corrida0/CALC-PDR1-ENIGH2022-0001/medidor.py",
        "f05d60e84a058a35a8196214dafa6c887b280817e98c2d7866ef4d032b78a811")
PDR1_PISO = ("pdr1_resultados", "data/corrida0/CALC-PDR1-ENIGH2022-0001/resultados.json",
             "28478ff27e798fc4a172e97caf7d1c1ca0c28e54e609035c894e6859e79e4df7")
RECETA = ("receta_pisos", "tools/dominios/salud/pisos_diseno.py",
          "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
# Descarga por tabla (un solo miembro .csv por ZIP, manifiesto «ZIP-OK(1 miembros)»): evita el truncamiento
# en 1 048 575 filas que tuvo el ZIP integrado en 2016/2018 (sucesión 0001 -> 0002). Spec §2.
PAYLOADS = {
    "conc": "cc1_inegi_enigh_2024__enigh2024_ns_concentradohogar_csv",
    "hog": "cc1_inegi_enigh_2024__enigh2024_ns_hogares_csv",
    "gas": "cc1_inegi_enigh_2024__enigh2024_ns_gastoshogar_csv",
    "pob": "cc1_inegi_enigh_2024__enigh2024_ns_poblacion_csv",
    "gp": "cc1_inegi_enigh_2024__enigh2024_ns_gastospersona_csv",
}
_GAS = tuple(f"gas.{c}" for c in ("folioviv", "foliohog", "clave", "tipo_gasto", "forma_pag1", "forma_pag2",
                                  "forma_pag3", "lugar_comp", "gasto_tri"))
_GP = tuple(f"gp.{c}" for c in ("folioviv", "foliohog", "numren", "clave", "tipo_gasto", "inscrip", "colegia",
                                "gasto_tri"))
# Columnas crudas («tabla.columna») cuya ausencia daría un valor falso en lugar de NaN: la conducta sale
# NO-ESTIMABLE (spec §5). Las demás ausencias ya dan NaN por construcción (y o universo vacío).
DEPENDE = {
    "CONSUMO-PART-EFECTIVO-EN-GASTO-DIRECTO": _GAS,
    "CONSUMO-HOG-COMPRA-FIADO": _GAS,
    "CONSUMO-HOG-COMPRA-TARJETA-CREDITO": _GAS,
    "CONSUMO-HOG-COMPRA-INTERNET": _GAS,
    "CONSUMO-HOG-COMPRA-INTERNET-SI-CONEXION": _GAS + ("hog.conex_inte",),
    "PDR1-PRIV": _GP + ("pob.tipoesc", "pob.asis_esc", "pob.numren"),
    "PDR1-ASIPRIV": ("pob.tipoesc", "pob.asis_esc"),
    "PDR1-CARGA": _GP + ("pob.tipoesc", "pob.asis_esc", "pob.numren", "conc.ing_cor"),
}

CONTRATO = {
    "x": X, "programa": "ENIGH", "ola": "2024", "unidad": "HOGAR",
    "contendientes": ["CALC-ENIGH-CONSUMO-PISOS-0002", "CALC-ENIGH-CONSUMO-PISOS-0001", "CALC-PDR1-ENIGH2022-0001"],
    "payloads": [(pid, f"ENIGH 2024 NS, tabla {pid.rsplit('_ns_', 1)[-1][:-4]} (descarga por tabla) -- ola RESERVADA; "
                       "sólo este medidor la lee") for pid in PAYLOADS.values()],
    "repo": [(CONSUMO[0], CONSUMO[1], "medidor sellado de CONSUMO-0002: prepara/conducta/ejes_de/CONDUCTAS/columnas"),
             (CONSUMO_PISO[0], CONSUMO_PISO[1], "piso 2022 de CONSUMO-0002: P, ICC-LO, ICC-HI por celda"),
             (PDR1[0], PDR1[1], "medidor sellado de PDR1: prepara/columnas/claves/ámbitos/bloques/segmentos"),
             (PDR1_PISO[0], PDR1_PISO[1], "piso 2022 de PDR1: P, IC-LO, IC-HI (IC95 de diseño) por celda"),
             (RECETA[0], RECETA[1], "num de la receta de pisos (la usan prepara/conducta de los sellados)"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Hogares de ENIGH 2024 NS en concentradohogar con factor > 0, est_dis y upm no vacíos (prepara() de "
                "los sellados); PDR1: hogares con al menos un integrante que asiste a la escuela (asis_esc = 1)",
    "filtros": "Un eje a la vez: CONSUMO por TOTAL, SEXO-JEFE, EDAD-JEFE, ESCOLARIDAD-JEFE, TLOC, DECIL y ENTIDAD "
               "(sólo conductas marcadas); PDR1 por decil y bloque dentro de cada ámbito pre-registrado (TOTAL, "
               "URBANO, RURAL: restricción de universo) y PRIV por TLOC, SEXO-JEFE, EDAD-JEFE; nunca cruces libres",
    "ponderador": "factor (concentradohogar); PART-* y CARGA: razón de totales con peso factor×denominador",
    "transformacion": "Recodificación de los contendientes (specs CONSUMO-ENIGH-PISOS v1.1 §2 y PDR1-ENIGH2022 §2); "
                      "MEDIA-* y DIF-* fuera de la primaria; columna ausente -> NO-ESTIMABLE",
    "estimando": "R = Σw·y/Σw (o razón de totales) por conducta×eje×categoría en ENIGH 2024; cobertura de R en el ICC "
                 "2022 de CONSUMO-0002 y en el IC95 de diseño 2022 de PDR1",
    "variables": [{"nombre": "CONSUMO-<conducta>", "definicion": "34 conductas PART-*/HOG-* de CONSUMO-0002 (spec "
                                                              "CONSUMO-ENIGH-PISOS v1.1 §2): concentradohogar, hogares, gastoshogar"},
                  {"nombre": "PDR1-PRIV", "definicion": "hogar con gasto G1 en inscripción/colegiatura (E001-E007) de un "
                                                        "integrante en escuela privada (poblacion.tipoesc = 2)"},
                  {"nombre": "PDR1-ASIPRIV", "definicion": "hogar con integrante que asiste a escuela privada"},
                  {"nombre": "PDR1-CARGA", "definicion": "Σw·gasto_tri(PRIV) / Σw·ing_cor entre hogares PRIV con ing_cor > 0"}],
}


def sellados(inputs=None):
    C = E.modulo("m_enigh_consumo_0002_sellado", E.bytes_repo(inputs, *CONSUMO))
    D = E.modulo("m_pdr1_enigh2022_sellado", E.bytes_repo(inputs, *PDR1))
    R = E.modulo("receta_pisos", E.bytes_repo(inputs, *RECETA))
    pc = E.json_repo(inputs, *CONSUMO_PISO)["resultados"]
    pd_ = E.json_repo(inputs, *PDR1_PISO)["resultados"]
    return C, D, R, pc, pd_


def columnas(C, D):
    """Columnas por tabla (minúsculas); CONSUMO y PDR1 comparten concentradohogar."""
    conc = list(dict.fromkeys(list(C.COLS_CONC) + list(D.COLS_CONC)))
    return {"conc": conc, "hog": list(C.COLS_HOG), "gas": list(C.COLS_GAS), "pob": list(D.COLS_POB),
            "gp": list(D.COLS_GP)}


def _conductas_consumo(C):
    return [c for c, (tipo, _e) in C.CONDUCTAS.items() if tipo != "media"]


def celdas_de(C, D):
    """[(id, contendiente, conducta, eje_o_ambito, cat)]."""
    out = []
    for c in _conductas_consumo(C):
        for eje, cats in [("TOTAL", ("TODOS",))] + list(C.ejes_de(c).items()):
            out += [(f"CONSUMO-{c}-{eje}-{cat}", "CONSUMO", c, eje, cat) for cat in cats]
    cats_amb = ("TODOS",) + tuple(D.DECILES) + tuple(D.BLOQUES)
    for c, ambs in (("PRIV", D.AMBITOS), ("ASIPRIV", D.AMBITOS), ("CARGA", D.AMB_CARGA)):
        out += [(f"PDR1-{c}-{a}-{cat}", "PDR1", c, a, cat) for a in ambs for cat in cats_amb]
    for eje, cats in D.SEGMENTOS.items():
        out += [(f"PDR1-PRIV-{eje}-{cat}", "PDR1", "PRIV-SEG", eje, cat) for cat in cats]
    return out


def esquema_resultados():
    C, D, _R, _pc, _pd = sellados()
    return E.esquema(P, [k[0] for k in celdas_de(C, D)],
                     unidad_r="proporción o razón de totales ponderada de hogares en ENIGH 2024", tipo_r="flotante")


def lee_payload_reservado(ruta, cols, filtro=None, chunk=200_000):
    """Única lectura de la ola reservada (la auditoría AST lo exige): el único miembro .csv del ZIP por tabla,
    sólo `cols`, por bloques; `filtro` = (columna, valores) se aplica por bloque (claves E001-E007 de PDR1).
    Devuelve (frame de texto con columnas en minúsculas, columnas ausentes); una ausente entra vacía."""
    quiero = [c.lower() for c in cols]
    partes = []
    with zipfile.ZipFile(ruta) as z:
        cand = [n for n in z.namelist() if n.lower().endswith(".csv") and not n.startswith("__MACOSX")]
        if len(cand) != 1:
            raise G.ParoDeGuardia(f"{os.path.basename(ruta)}: se esperaba 1 miembro .csv, hay {len(cand)}")
        with z.open(cand[0]) as fb:
            texto = io.TextIOWrapper(fb, encoding="utf-8-sig", errors="replace", newline="")
            for df in pd.read_csv(texto, usecols=lambda c: c.strip().lower() in quiero, dtype=str,
                                  keep_default_na=False, chunksize=chunk):
                df.columns = [c.strip().lower() for c in df.columns]
                if filtro is not None and filtro[0] in df.columns:
                    df = df[df[filtro[0]].astype(str).str.strip().str.upper().isin(filtro[1]).to_numpy()]
                partes.append(df)
    df = pd.concat(partes, ignore_index=True) if partes else pd.DataFrame(columns=[])
    faltan = [c for c in quiero if c not in df.columns]
    for c in faltan:
        df[c] = np.full(len(df), "", dtype=object)
    return df[quiero], faltan


def _etiquetas(mascaras: dict, n: int):
    """Un vector de etiquetas desde máscaras disjuntas de UNA variable (decil, bloque o segmento)."""
    g = np.full(n, None, dtype=object)
    for cat, m in mascaras.items():
        g[np.asarray(m, dtype=bool)] = cat
    return g


def _registra(out, clave, y, w, g):
    for cat, r in G.proporcion_por_grupo(y, w, g).items():
        out[clave + (cat,)] = r["p"]


def mide_r(C, D, R, frames, faltan=()):
    """{(contendiente, conducta, eje_o_ambito, cat): p} con UNA variable de agrupación por llamada."""
    faltan = set(faltan)
    fuera = {k for k, dep in DEPENDE.items() if faltan & set(dep)}
    out = {}
    # ── CONSUMO-0002
    f, ejes, _diag = C.prepara(frames["conc"], frames["hog"], frames["gas"], R)
    w = f["_w"].to_numpy()
    todos = np.full(len(f), "TODOS", dtype=object)
    for c in _conductas_consumo(C):
        if f"CONSUMO-{c}" in fuera:
            continue
        y, mult = C.conducta(c, f, R)
        y = np.asarray(y, dtype=float)
        wc = w * np.asarray(mult, dtype=float)
        _registra(out, ("CONSUMO", c, "TOTAL"), y, wc, todos)
        for eje in C.ejes_de(c):
            _registra(out, ("CONSUMO", c, eje), y, wc, ejes[eje][0])
    # ── PDR1
    fr = {"conc": frames["conc"][list(D.COLS_CONC)], "pob": frames["pob"], "gp": frames["gp"]}
    f, amb, seg, _diag = D.prepara(fr, R)
    w = f["_w"].to_numpy()
    n = len(f)
    univ = f["_univ"].to_numpy().astype(bool)
    dec = f["_dec"].to_numpy()
    g_dec = np.asarray(dec, dtype=object)
    g_blq = _etiquetas({b: np.isin(dec, ds) for b, ds in D.BLOQUES.items()}, n)
    todos = np.full(n, "TODOS", dtype=object)
    ing = f["_ing"].to_numpy()
    okc = f["_priv"].to_numpy().astype(bool) & np.isfinite(ing) & (ing > 0)
    y_carga = np.full(n, np.nan)
    y_carga[okc] = f["_gpriv"].to_numpy()[okc] / ing[okc]
    series = {"PRIV": (np.where(univ, f["_priv"].to_numpy().astype(float), np.nan), w, D.AMBITOS),
              "ASIPRIV": (np.where(univ, f["_asipriv"].to_numpy().astype(float), np.nan), w, D.AMBITOS),
              "CARGA": (y_carga, np.where(okc, w * np.where(okc, ing, 0.0), 0.0), D.AMB_CARGA)}
    for c, (y, wc, ambs) in series.items():
        if f"PDR1-{c}" in fuera:
            continue
        for a in ambs:
            ya = np.where(np.asarray(amb[a], dtype=bool), y, np.nan)  # ámbito = restricción de universo
            for g in (todos, g_dec, g_blq):
                _registra(out, ("PDR1", c, a), ya, wc, g)
    if "PDR1-PRIV" not in fuera:
        y = series["PRIV"][0]
        for eje, d in seg.items():
            _registra(out, ("PDR1", "PRIV-SEG", eje), y, w, _etiquetas(d, n))
    return out


def filas(C, D, r, pc, pd_):
    out = []
    for cid, cont, c, eje, cat in celdas_de(C, D):
        if cont == "CONSUMO":
            q = lambda k: pc.get(C.rid(c, C.OLA_PISO, eje, cat, k))  # noqa: E731
            lo, hi, pt = q("ICC-LO"), q("ICC-HI"), q("P")
            cong = f"CONSUMO-{c}"
        elif c == "PRIV-SEG":
            q = lambda k: pd_.get(f"{D.P}-PRIV-{eje}-{cat}-{k}")  # noqa: E731
            lo, hi, pt = q("IC-LO"), q("IC-HI"), q("P")
            cong = "PDR1-PRIV-SEG"
        else:
            q = lambda k: pd_.get(D.rid(c, eje, cat, k))  # noqa: E731
            lo, hi, pt = q("IC-LO"), q("IC-HI"), q("P")
            cong = f"PDR1-{c}"
        out.append({"id": cid, "conglomerado": cong, "lo": lo, "hi": hi, "punto": pt,
                    "r": r.get((cont, c, eje, cat))})
    return out


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = set(PAYLOADS.values()) | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    C, D, R, pc, pd_ = sellados(inputs)
    cols = columnas(C, D)
    frames, faltan = {}, []
    for t, pid in PAYLOADS.items():
        filtro = ("clave", tuple(D.CLAVES_COLEG)) if t == "gp" else None
        frames[t], f_t = lee_payload_reservado(inputs[pid]["ruta_absoluta"], cols[t], filtro)
        faltan += [f"{t}.{c}" for c in f_t]
    return E.salida(P, filas(C, D, mide_r(C, D, R, frames, faltan), pc, pd_))
