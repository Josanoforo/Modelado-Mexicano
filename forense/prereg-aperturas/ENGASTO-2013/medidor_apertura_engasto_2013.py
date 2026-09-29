#!/usr/bin/env python3
"""Medidor de APERTURA de ENGASTO 2013 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-ENGASTO-2013-spec-v1_0.md`; contrato: `APERTURA-ENGASTO-2013-spec.yaml`;
receta: `RECETA-APERTURA-ENGASTO-2013.md`. NO SE HA CORRIDO sobre ENGASTO 2013: corre sólo en caja,
en el commit de apertura que mesa autorice.

Al abrir: R = razón ponderada de hogares de cada conducta de `CALC-ENGASTO-CONSUMO-PISOS-0001` en la
ola 2013 (carpeta `engasto2013/`), por categoría de UN eje a la vez, con la recodificación del medidor
sellado (input `origen: repo`, sha fijado; `prepara`/`conducta_y` con los códigos de 2012). Adjudica la
cobertura del contendiente: piso 2012 con IC95 de DISEÑO (IC-LO/IC-HI de su `resultados.json`; el
contendiente no tiene IC de persistencia: una sola ola abierta). Guardia E.6: auditoría AST de este
archivo antes de leer un byte; `guardia_apertura.proporcion_por_grupo` es el único agregador.

Tabla ausente en la ola: LUGAR_COMPRA 2013 no está en el manifiesto (spec §0, §5): sus 76 columnas
entran como faltantes y las conductas que dependen de ellas salen NO-ESTIMABLE (R None) por
construcción. Columna ausente de reactivo o eje → NaN → NO-ESTIMABLE en las celdas que la usan;
columna ausente de llave, ponderador o diseño → ParoDeGuardia (no hay universo que medir).
"""
from __future__ import annotations

import ast
import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENGASTO-2013"
P = "RESULT-APERTURA-ENGASTO-2013"
CALC = "CALC-ENGASTO-CONSUMO-PISOS-0001"
CARPETA_OLA = "engasto2013"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", f"data/corrida0/{CALC}/medidor.py",
           "d996dbf3e38ae7d0fafae7f94710b7374d88e7fcc47cf8eb8940b413df773c86")
PISO = ("contendiente_resultados", f"data/corrida0/{CALC}/resultados.json",
        "0afd04101ed0c8e7b927b6df4072188b36309e2f9299b665f6590a0ab8729bd8")
RECETA = ("receta_pisos", "tools/dominios/salud/pisos_diseno.py",
          "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
# Ids del manifiesto de la carpeta engasto2013/ con el mismo rol que los inputs 2012 del contendiente.
# Dos llevan rótulo «2012» en el id aunque su `archivo` es engasto2013/ (defecto de rotulación ya
# declarado en forense/analisis/consumo-gasto/lista-cerrada-P1.md §1): se eligen por `archivo`+sha.
PAYLOADS = {
    "hogar": "engasto_2012_hogar_dta",                       # engasto2013/hogar_dta.zip (HOGAR 173 campos)
    "vivienda": "engasto_2013_viviendas_dta",                # engasto2013/viviendas_dta.zip
    "ajustado": "engasto_2012_gasto_de_consumo_ajustado_dta",  # engasto2013/gasto_de_consumo_ajustado_dta.zip
}
TABLA_AUSENTE = "lugar"  # LUGAR_COMPRA: sin id en engasto2013/ (NO-ENCONTRADO en el manifiesto)


def _estructurales(M):
    return {"hogar": set(M.LLAVE_HOG) | {"factor_hog"},
            "vivienda": set(M.LLAVE_VIV) | {"est_dis", "upm"},
            "ajustado": set(M.LLAVE_HOG)}


CONTRATO = {
    "x": X, "programa": "ENGASTO", "ola": "2013", "unidad": "HOGAR",
    "contendientes": [CALC],
    "payloads": [(PAYLOADS["hogar"], "ENGASTO 2013 HOGAR (archivo engasto2013/hogar_dta.zip; id con rótulo 2012) -- ola RESERVADA; sólo este medidor la lee"),
                 (PAYLOADS["vivienda"], "ENGASTO 2013 VIVIENDAS (diseño, tam_loc) -- ola RESERVADA; sólo este medidor la lee"),
                 (PAYLOADS["ajustado"], "ENGASTO 2013 GASTO_DE_CONSUMO_AJUSTADO (jefe; archivo engasto2013/, id con rótulo 2012) -- ola RESERVADA")],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: COLS/prepara/conducta_y/EJES/rid"),
             (PISO[0], PISO[1], "piso 2012 sellado: P, IC-LO, IC-HI (diseño) por celda"),
             (RECETA[0], RECETA[1], "lee_dta y num de la receta de pisos"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "dependencias": ["numpy", "pandas", "pyreadstat"],
    "universo": "Hogares de ENGASTO 2013 (carpeta engasto2013/): HOGAR con factor_hog > 0 y est_dis, upm (VIVIENDAS) "
                "no vacíos (prepara() del contendiente); universo de cada conducta el del contendiente",
    "filtros": "Un eje a la vez (TOTAL, SEXO-JEFE, EDAD-JEFE, ESCOLARIDAD-JEFE, TLOC); nunca cruces (guardia E.6)",
    "ponderador": "factor_hog",
    "transformacion": "Recodificación del contendiente (forense/analisis/consumo-gasto/lista-cerrada-P1.md §3, §5; "
                      "códigos del FD 2012). LUGAR_COMPRA 2013 ausente del manifiesto -> sus conductas NO-ESTIMABLE; "
                      "columna ausente o con texto/códigos distintos -> NO-ESTIMABLE; llave/ponderador/diseño ausente -> PARO",
    "estimando": "R = Σw·y/Σw por conducta×eje×categoría en ENGASTO 2013; cobertura de R en el IC95 de diseño del piso 2012",
    "variables": [{"nombre": c, "definicion": "conducta del contendiente (spec CONSUMO-ENGASTO-PISOS §2; lista-cerrada-P1 §3)"}
                  for c in ("GRAN-COMPRA-*(8)", "{CARNE,FRUTA,VERDURA,PAN,LECHE}-EN-{SUPER-MEMBRESIA,MERCADO-TIANGUIS-AMBULANTE}",
                            "COMPRA-INTERNET-ALGUN-RUBRO", "COMPRA-INTERNET-SI-CONEXION", "TIENE-CELULAR", "CONEX-INTERNET")],
}


def sellados(inputs=None):
    M = E.modulo("m_engasto_pisos_sellado", E.bytes_repo(inputs, *SELLADO))
    R = E.modulo("receta_pisos_engasto", E.bytes_repo(inputs, *RECETA))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return M, R, piso


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(M):
    out = []
    for c in M.CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(M.EJES.items()):
            out += [(c, eje, cat) for cat in cats]
    return out


def esquema_resultados():
    M, _R, _p = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(M)])


def _faltantes(err, pedidas, estructurales, tabla):
    """Columnas pedidas que el KeyError del lector declara ausentes; una estructural → PARO."""
    msg = str(err.args[0]) if err.args else ""
    try:
        dichas = {str(c).lower() for c in ast.literal_eval(msg[msg.rindex(": [") + 2:])}
    except (ValueError, SyntaxError) as e:
        raise G.ParoDeGuardia(f"{tabla}: KeyError ilegible del lector: {msg}") from e
    faltan = [c for c in pedidas if c.lower() in dichas]
    duras = sorted(c for c in faltan if c in estructurales)
    if duras or not faltan:
        raise G.ParoDeGuardia(f"{tabla}: columnas de llave/ponderador/diseño ausentes {duras or msg}: PARO")
    return faltan


def lee_payload_reservado(R, M, tabla, ruta):
    """Única lectura de la ola reservada (la auditoría AST lo exige). Devuelve (frame, faltantes)."""
    if CARPETA_OLA not in str(ruta):
        raise G.ParoDeGuardia(f"`{tabla}` no resuelve a la carpeta {CARPETA_OLA}/ (ola 2013): {ruta}")
    cols = list(M.COLS[tabla])
    try:
        return R.lee_dta(ruta, cols), []
    except KeyError as err:
        faltan = _faltantes(err, cols, _estructurales(M)[tabla], tabla)
    df = R.lee_dta(ruta, [c for c in cols if c not in faltan])
    for c in faltan:
        df[c] = np.nan
    return df, faltan


def marco_sin_tabla(M, hogar):
    """LUGAR_COMPRA ausente de la ola: llaves del hogar y las 76 columnas `lc_*` vacías (NaN)."""
    lug = hogar[list(M.LLAVE_HOG)].copy()
    return lug.assign(**{c: np.nan for c in M.LC})


def mide_r(M, R, frames):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    fr = dict(frames)
    if TABLA_AUSENTE not in fr:
        fr[TABLA_AUSENTE] = marco_sin_tabla(M, fr["hogar"])
    f, ejes, _diag = M.prepara(fr, R)
    w = f["_w"].to_numpy()
    out = {}
    for c in M.CONDUCTAS:
        y = np.asarray(M.conducta_y(c, f, R), dtype=float)
        grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
        grupos.update({e: np.asarray(ejes[e][0], dtype=object) for e in M.EJES})
        for eje, g in grupos.items():
            for cat, r in G.proporcion_por_grupo(y, w, g).items():
                out[(c, eje, cat)] = r["p"]
    return out


def filas(M, r, piso):
    return [{"id": _cid(c, eje, cat), "conglomerado": c,
             "lo": piso.get(M.rid(c, eje, cat, "IC-LO")),
             "hi": piso.get(M.rid(c, eje, cat, "IC-HI")),
             "punto": piso.get(M.rid(c, eje, cat, "P")),
             "r": r.get((c, eje, cat))} for c, eje, cat in celdas_de(M)]


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = set(PAYLOADS.values()) | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    M, R, piso = sellados(inputs)
    frames = {t: lee_payload_reservado(R, M, t, inputs[pid]["ruta_absoluta"])[0] for t, pid in PAYLOADS.items()}
    return E.salida(P, filas(M, mide_r(M, R, frames), piso))
