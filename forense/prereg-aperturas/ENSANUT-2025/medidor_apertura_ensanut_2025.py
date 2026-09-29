#!/usr/bin/env python3
"""Medidor de APERTURA de ENSANUT 2025 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (28/sep/2026).

Spec humana: `APERTURA-ENSANUT-2025-spec-v1_0.md`; contrato: `APERTURA-ENSANUT-2025-spec.yaml`;
receta: `RECETA-APERTURA-ENSANUT-2025.md`. NO SE HA CORRIDO sobre ENSANUT 2025: corre sólo en caja,
en el commit de apertura que mesa autorice.

Sirve a DOS contendientes sellados antes de la apertura (E.6: una apertura sirve a todos; una sola primaria):

  · `CALC-ENSANUT-PISOS-SALUD-0001`: R = razón ponderada de cada conducta en ENSANUT 2025, por categoría de UN
    eje a la vez, con la recodificación de su medidor sellado; IC = ICC-LO/ICC-HI (piso 2024 con IC calibrado
    de persistencia) de su `resultados.json` sellado.
  · `CALC-MC2-ENSANUT2024-0001`: R = razón ponderada de cada celda de nivel de su medidor sellado
    (`frame_inte`/`frame_adul` + `celdas_inte`/`celdas_adul`, recodificación verbatim) en ENSANUT 2025; IC =
    IC95-INF/IC95-SUP (bootstrap de diseño 2024) de su `resultados.json` sellado. Celdas `MC2-<celda>`.
    Apartadas sin abrir: las 7 diferencias (contrastes de dos celdas que ya entran) y 4 celdas que duplican
    `BUSCO-ATENCION` de PISOS-SALUD (mismo estimando, mismo universo; `DUPLICADAS_MC2`).

Todas las celdas puntuadas entran a UNA primaria (cobertura con Wilson). Guardia E.6: auditoría AST de este
archivo antes de leer un byte del payload; `guardia_apertura.proporcion_por_grupo` es el único agregador; la
única lectura es `lee_payload_reservado` (una por archivo, con la unión de columnas de los dos contendientes).
"""
from __future__ import annotations

import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENSANUT-2025"
P = "RESULT-APERTURA-ENSANUT-2025"
OLA_PISO = "2024"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", "data/corrida0/CALC-ENSANUT-PISOS-SALUD-0001/medidor.py",
           "f334da45a248ccf6d4b812cef2b6108a6dbb3a76825f3af9d5bd9d648e13abe8")
PISO = ("contendiente_resultados", "data/corrida0/CALC-ENSANUT-PISOS-SALUD-0001/resultados.json",
        "a2d6654d84c002179dc40eb1c01999f7351dd27be09c52b414d3151033537434")
RECETA = ("receta_pisos_salud", "tools/dominios/salud/pisos_diseno.py",
          "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
SELLADO_MC2 = ("contendiente_medidor_mc2", "data/corrida0/CALC-MC2-ENSANUT2024-0001/medidor.py",
               "11e22394dafda219c2d2209c756c0660281d6f81f29fb3aa80ba4172b788dc6c")
PISO_MC2 = ("contendiente_resultados_mc2", "data/corrida0/CALC-MC2-ENSANUT2024-0001/resultados.json",
            "69c41814965b485552496b00da067f0d968a25daa4ae863a58af761c80cacf3c")
CALC_MC2 = "CALC-MC2-ENSANUT2024-0001"
PFX_MC2 = "RESULT-MC2-ENSANUT2024"
# archivo de la ola -> (función de marco, función de celdas, columnas) del medidor sellado de MC2; mismo rol en
# 2025 que en 2024 (integrantes_ensanut2024_w_icb -> integrantes_2025_w; adultos_ensanut2024_w -> adultos_2025_w)
ARCH_MC2 = {"INTE": ("frame_inte", "celdas_inte", "COLS_INTE"), "ADUL": ("frame_adul", "celdas_adul", "COLS_ADUL")}
# Celdas de MC2 que duplican una celda de PISOS-SALUD (mismo estimando h0404=1|h0401=1, mismo universo y
# estrato 1/2/3): se apartan sin abrir; su R es la de la celda de PISOS-SALUD, que ya entra a la primaria.
DUPLICADAS_MC2 = {"BUSCO-NAC": "BUSCO-ATENCION-TOTAL-TODOS", "BUSCO-RURAL": "BUSCO-ATENCION-ESTRATO-RURAL",
                  "BUSCO-URBANO": "BUSCO-ATENCION-ESTRATO-URBANO",
                  "BUSCO-METRO": "BUSCO-ATENCION-ESTRATO-METROPOLITANO"}
PAYLOADS = {
    "ADUL": "ensanut_2025__adultos_2025_w_stata_stata_zip",
    "INTE": "ensanut_2025__integrantes_2025_w_stata_stata_zip",
    "UTIL": "ensanut_2025__utilizadores_2025_w_stata_stata_zip",
    "ADOL": "ensanut_2025__adolescentes_2025_w_stata_stata_zip",
}

CONTRATO = {
    "x": X, "programa": "ENSANUT", "ola": "2025", "unidad": "PERSONA",
    "contendientes": ["CALC-ENSANUT-PISOS-SALUD-0001", CALC_MC2],
    "dependencias": ["numpy", "pandas", "pyreadstat"],
    "payloads": [(pid, f"ENSANUT 2025 {a} -- ola RESERVADA; sólo este medidor la lee") for a, pid in PAYLOADS.items()],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: prepara/conducta_y/universo_edad/ejes_de"),
             (PISO[0], PISO[1], "piso 2024 sellado: P, ICC-LO, ICC-HI por celda"),
             (RECETA[0], RECETA[1], "lee_dta y num de la receta de pisos"),
             (SELLADO_MC2[0], SELLADO_MC2[1], "medidor sellado de MC2: frame_inte/frame_adul, celdas_inte/celdas_adul "
                                              "(recodificación; no importa receta del repo)"),
             (PISO_MC2[0], PISO_MC2[1], "MC2 2024 sellado: P, IC95-INF, IC95-SUP por celda"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Personas de ENSANUT 2025: adultos 20+, integrantes (todas las edades), utilizadores, adolescentes 10-19; "
                "ponde_f > 0 con est_sel y upm no vacíos (prepara() de PISOS-SALUD). Celdas MC2-*: el universo de "
                "cada celda del medidor sellado de MC2 (integrantes con necesidad de salud en 3 meses; adultos 20+ "
                "con diabetes diagnosticada y en tratamiento), mismo filtro de diseño",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ESTRATO, ESCOLARIDAD 20+); nunca cruces (guardia E.6). MC2-*: "
               "una llamada por celda sellada, agrupada por su indicador de pertenencia; 7 diferencias y 4 "
               "duplicados de PISOS-SALUD apartados sin abrir",
    "ponderador": "ponde_f",
    "transformacion": "Recodificación del contendiente (forense/analisis/salud-bienestar/lista-cerrada-P1.md §2); "
                      "columna ausente o con texto/códigos distintos en el catálogo 2025 -> NO-ESTIMABLE",
    "estimando": "R = Σw·y/Σw por celda en ENSANUT 2025; cobertura de R en el IC del contendiente (ICC del piso "
                 "2024 de PISOS-SALUD; IC95 de diseño 2024 de MC2), una sola primaria sobre todas las celdas",
    "variables": [{"nombre": c, "definicion": "conducta del contendiente (spec SALUD-ENSANUT-PISOS §2)"}
                  for c in ("DEPRESION-CESD7", "IDEACION-SUICIDA-ADULTOS", "DX-DIABETES", "DX-HIPERTENSION",
                            "FUMA-ACTUAL", "ALCOHOL-12M", "ALCOHOL-EXCESIVO-30D", "NECESIDAD-SALUD-3M",
                            "BUSCO-ATENCION", "FUE-ATENDIDO", "ATENCION-CONSULTORIO-FARMACIA",
                            "ATENCION-CURANDERO-HIERBERO", "IDEACION-SUICIDA-ADOLESCENTES")]
    + [{"nombre": f"MC2-{c}", "definicion": d} for c, d in (
        ("BUSCO", "buscó atención (h0404 1 vs 2) | necesidad de salud 3 meses (h0401 = 1); sólo NORURAL "
                  "(NAC/RURAL/URBANO/METRO duplican BUSCO-ATENCION)"),
        ("BUSCO-MENTAL", "buscó atención | necesidad de salud mental (h0402 en 47/48/50/59)"),
        ("ACCESO", "algún motivo de no búsqueda (H0405A-C) en 2/3/4 | no buscó con motivo válido 01-13"),
        ("NO-GRAVE", "algún motivo de no búsqueda = 1 | no buscó con motivo válido 01-13"),
        ("DM-SUSPENDE", "suspendió medicamento 6 meses (a0313 1 vs 2) | adulto 20+ con a0301 = 1 y a0307 1-3"),
        ("DM-ECON-ACCESO", "causa de suspensión (a0314) en 5/6/7/10 | suspendió con causa válida"),
        ("DM-PAGA", "pagó por el tratamiento (0 < a0310a < 99999) | tratado con monto válido"))],
}


def sellados(inputs=None):
    M = E.modulo("m_ensanut_pisos_sellado", E.bytes_repo(inputs, *SELLADO))
    R = E.modulo("receta_pisos_salud", E.bytes_repo(inputs, *RECETA))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return M, R, piso


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(M):
    out = []
    for c, (arch, ejes_c) in M.CONDUCTAS.items():
        for eje, cats in [("TOTAL", ("TODOS",))] + list(M.ejes_de(arch, ejes_c).items()):
            out += [(c, eje, cat) for cat in cats]
    return out


def esquema_resultados():
    M, _R, _p = sellados()
    M2, _p2 = sellados_mc2()
    return E.esquema(P, [_cid(*k) for k in celdas_de(M)] + [f"MC2-{c}" for c in celdas_mc2(M2)])


def columnas_de(M, arch, M2=None):
    """Unión (sin distinguir mayúsculas, en orden) de las columnas de los dos contendientes para `arch`, y las
    columnas duras (diseño y llave de PISOS-SALUD; diseño de MC2)."""
    cols, vistas = [], set()
    extra = list(getattr(M2, ARCH_MC2[arch][2])) if (M2 is not None and arch in ARCH_MC2) else []
    for c in list(M.COLS[arch]) + extra:
        if c.lower() not in vistas:
            vistas.add(c.lower())
            cols.append(c)
    duras = {c.lower() for c in list(M.DISENO) + (list(M2.DISENO) if M2 is not None else [])}
    return cols, duras


def lee_payload_reservado(R, M, arch, ruta, M2=None):
    """Única lectura de la ola reservada (la auditoría AST lo exige); una por archivo, con la unión de columnas
    de los dos contendientes. Spec §5: una columna de diseño o llave ausente es PARO; un reactivo o eje ausente
    entra vacío y sus celdas salen NO-ESTIMABLE (sin recodificar). Columnas en minúsculas (receta)."""
    cols, duras = columnas_de(M, arch, M2)
    try:
        return R.lee_dta(ruta, cols)
    except KeyError as exc:
        faltan = [c for c in cols if repr(c) in str(exc)]
    graves = [c for c in faltan if c.lower() in duras]
    if graves or not faltan:
        raise G.ParoDeGuardia(f"columnas de diseño o llave ausentes en {arch}: {graves or faltan}")
    df = R.lee_dta(ruta, [c for c in cols if c not in faltan])
    for c in faltan:
        df[c.lower()] = np.nan
    return df


def mide_r(M, R, frames):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    out = {}
    inte = frames["INTE"]
    for arch in ("ADUL", "INTE", "UTIL", "ADOL"):
        f, ejes, _diag, edad = M.prepara(arch, frames[arch], None if arch == "INTE" else inte, R)
        w = f["_w"].to_numpy()
        for c, (a, ejes_c) in M.CONDUCTAS.items():
            if a != arch:
                continue
            y = np.asarray(M.conducta_y(c, f, R), dtype=float)
            y[~np.asarray(M.universo_edad(arch, edad))] = np.nan
            grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
            grupos.update({e: np.asarray(ejes[e], dtype=object) for e in M.ejes_de(arch, ejes_c)})
            for eje, g in grupos.items():
                for cat, r in G.proporcion_por_grupo(y, w, g).items():
                    out[(c, eje, cat)] = r["p"]
    return out


def filas(M, r, piso):
    return [{"id": _cid(c, eje, cat), "conglomerado": c,
             "lo": piso.get(M.rid(c, OLA_PISO, eje, cat, "ICC-LO")),
             "hi": piso.get(M.rid(c, OLA_PISO, eje, cat, "ICC-HI")),
             "punto": piso.get(M.rid(c, OLA_PISO, eje, cat, "P")),
             "r": r.get((c, eje, cat))} for c, eje, cat in celdas_de(M)]


# ── contendiente 2: CALC-MC2-ENSANUT2024-0001 ───────────────────────────────
def sellados_mc2(inputs=None):
    M2 = E.modulo("m_mc2_ensanut2024_sellado", E.bytes_repo(inputs, *SELLADO_MC2))
    return M2, E.json_repo(inputs, *PISO_MC2)["resultados"]


def _inyecta_marcos(M2, frames):
    """El medidor sellado de MC2 lee con su propio `_lee_dta`; aquí se le entrega el marco YA LEÍDO por
    `lee_payload_reservado` (sus columnas, en minúsculas), así su recodificación corre verbatim sin otra
    lectura. `ruta` es la etiqueta del archivo (INTE/ADUL)."""
    def _ya_leido(tag, cols):
        return frames[tag][[c.lower() for c in cols]].copy()
    M2._lee_dta = _ya_leido


def _celdas_y_difs_mc2(M2):
    """(celdas de nivel, diferencias) del medidor sellado, en su orden, sobre marcos vacíos (sin dato)."""
    import pandas as pd
    vacios = {a: pd.DataFrame({c.lower(): pd.Series(dtype=float) for c in getattr(M2, cols)})
              for a, (_f, _c, cols) in ARCH_MC2.items()}
    _inyecta_marcos(M2, vacios)
    C, F = [], []
    for a, (fr, ce, _cols) in ARCH_MC2.items():
        c, f = getattr(M2, ce)(getattr(M2, fr)(a)[0])
        C += [x[0][len(PFX_MC2) + 1:] for x in c]
        F += [x[0][len(PFX_MC2) + 1:] for x in f]
    return C, F


def celdas_mc2(M2):
    """Celdas MC2 que entran a la primaria: las de nivel menos las duplicadas de PISOS-SALUD."""
    C, _F = _celdas_y_difs_mc2(M2)
    return [c for c in C if c not in DUPLICADAS_MC2]


def mide_r_mc2(M2, frames):
    """{celda: p} con la recodificación verbatim del medidor sellado de MC2 y UNA variable de agrupación por
    llamada (el indicador de pertenencia a la celda sellada, dentro del diseño válido de su `_estima`)."""
    import pandas as pd
    entra = set(celdas_mc2(M2))
    _inyecta_marcos(M2, frames)
    out = {}
    for a, (fr, ce, _cols) in ARCH_MC2.items():
        d, _diag = getattr(M2, fr)(a)
        C, _F = getattr(M2, ce)(d)
        ok = (d["_w"].notna() & (d["_w"] > 0) & d["_est"].ne("") & d["_upm"].ne("")).to_numpy(dtype=bool)
        w = d["_w"].to_numpy(dtype=float)
        for rid, m, y in C:
            c = rid[len(PFX_MC2) + 1:]
            if c not in entra:
                continue
            mm = ok & pd.Series(m, index=d.index).fillna(False).to_numpy(dtype=bool)
            g = np.where(mm, c, None).astype(object)
            res = G.proporcion_por_grupo(np.asarray(y, dtype=float), w, g)
            out[c] = res.get(c, {}).get("p")
    return out


def filas_mc2(M2, r, piso2):
    return [{"id": f"MC2-{c}", "conglomerado": CALC_MC2,
             "lo": piso2.get(f"{PFX_MC2}-{c}-IC95-INF"), "hi": piso2.get(f"{PFX_MC2}-{c}-IC95-SUP"),
             "punto": piso2.get(f"{PFX_MC2}-{c}-P"), "r": r.get(c)} for c in celdas_mc2(M2)]


def todas_las_filas(M, R, piso, M2, piso2, frames):
    """Las celdas de los dos contendientes, para UNA sola adjudicación."""
    return filas(M, mide_r(M, R, frames), piso) + filas_mc2(M2, mide_r_mc2(M2, frames), piso2)


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = set(PAYLOADS.values()) | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    M, R, piso = sellados(inputs)
    M2, piso2 = sellados_mc2(inputs)
    frames = {a: lee_payload_reservado(R, M, a, inputs[pid]["ruta_absoluta"], M2) for a, pid in PAYLOADS.items()}
    return E.salida(P, todas_las_filas(M, R, piso, M2, piso2, frames))
