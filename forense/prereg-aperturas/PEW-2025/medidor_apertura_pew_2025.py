#!/usr/bin/env python3
"""Medidor de APERTURA de Pew Global Attitudes Spring 2025 (México) — ACTO GEN2-APERTURAS-PREREGISTRADAS-1.

Spec humana: `APERTURA-PEW-2025-spec-v1_0.md`; contrato: `APERTURA-PEW-2025-spec.yaml`;
receta: `RECETA-APERTURA-PEW-2025.md`. NO SE HA CORRIDO sobre Pew 2025: corre sólo en caja, en el commit
de apertura que mesa autorice.

Una apertura sirve a los tres contendientes sellados antes (E.6), con UNA comparación primaria:
  · CALC-PEW-RELIGION-2024-0001            (4 conductas; piso 2024, IC de diseño IC-LO/IC-HI)
  · CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001 (7 conductas; piso = última ola con la conducta; ICC si lo
                                            publica finito, si no IC-LO/IC-HI)
  · CALC-PEW-MIGRACION-MEX-0001            (6 conductas; piso = última ola con la pregunta; ICC si finito,
                                            si no IC-LO/IC-HI)
R = Σw·y/Σw por conducta×eje×categoría en las filas de México de 2025, con la recodificación, el universo y
los ejes de CADA contendiente (sus tablas, importadas por bytes con sha256 fijado). Guardia E.6: auditoría
AST de este archivo antes de leer un byte; `guardia_apertura.proporcion_por_grupo` es el único agregador.
"""
from __future__ import annotations

import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "PEW-2025"
P = "RESULT-APERTURA-PEW-2025"
OLA = "2025"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

REL = ("contendiente_religion2024_medidor", "data/corrida0/CALC-PEW-RELIGION-2024-0001/medidor.py",
       "e141217b7798ebd260d96b457a7cb097d3a836367886e08af49ad6db551050b6")
REL_RES = ("contendiente_religion2024_resultados", "data/corrida0/CALC-PEW-RELIGION-2024-0001/resultados.json",
           "1dd1769d5b0617ca4fd351dc6ca584d78be3e275e3db03483bedd066761aa410")
PIS = ("contendiente_pisos_medidor", "data/corrida0/CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001/medidor.py",
       "c45c9802d27fae8fb57fbe81daaaee1829de956216069d277d8ae9093eb65ece")
PIS_RES = ("contendiente_pisos_resultados", "data/corrida0/CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001/resultados.json",
           "4dacfff3622f26985af232c24c6d9feaf62cc4403453265007e5112a4e7e9c03")
MIG = ("contendiente_migracion_medidor", "data/corrida0/CALC-PEW-MIGRACION-MEX-0001/medidor.py",
       "2b2328dfcd836976ea7e4f7bbf3b25dedaf1928f89d556dc97c8a2b605873824")
MIG_RES = ("contendiente_migracion_resultados", "data/corrida0/CALC-PEW-MIGRACION-MEX-0001/resultados.json",
           "f8b1443715e116fa266345a0997116472718c6893eb8a16fe97cf3b7f0fd0cdc")
MOTOR = ("motor_pisos_confianza", "tools/dominios/confianza/motor_pisos.py",
         "7d0494f43052e0ea39ce0baf5f6505ccf889b386cfa3c0775b0dbdfb56ef958e")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAY = "pew_gas_spring2025"

CONTENDIENTES = {"RELIGION2024": "CALC-PEW-RELIGION-2024-0001",
                 "PISOS": "CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001",
                 "MIGRACION": "CALC-PEW-MIGRACION-MEX-0001"}
# Columnas de diseño en 2025: la primera presente de cada lista (nombres de las olas del piso, en minúsculas).
DISENO = {"PAIS": ("country",), "PESO": ("weight",), "EDAD": ("age",), "SEXO": ("gender", "sex"),
          "ESCOLARIDAD": ("d_educ_mexico", "d_educ_mexico_2017")}
OBLIGATORIAS = ("PAIS", "PESO", "EDAD")
ETIQUETA_PAIS = "mexico"
SEXO_MAPA = {"HOMBRE": [1], "MUJER": [2]}


def sellados(inputs=None):
    M = E.modulo("motor_pisos_confianza", E.bytes_repo(inputs, *MOTOR))
    mods = {"RELIGION2024": E.modulo("m_pew_religion2024_sellado", E.bytes_repo(inputs, *REL)),
            "PISOS": E.modulo("m_pew_pisos_sellado", E.bytes_repo(inputs, *PIS)),
            "MIGRACION": E.modulo("m_pew_migracion_sellado", E.bytes_repo(inputs, *MIG))}
    res = {"RELIGION2024": E.json_repo(inputs, *REL_RES)["resultados"],
           "PISOS": E.json_repo(inputs, *PIS_RES)["resultados"],
           "MIGRACION": E.json_repo(inputs, *MIG_RES)["resultados"]}
    return {"M": M, "mods": mods, "res": res}


def _conductas_pisos(Pm):
    out = []
    for o in Pm.OLAS:
        out += [c for c in Pm.OLAS[o][7] if c not in out]
    return out


def ola_piso(S, tag, c, olas):
    """Última ola del contendiente con la conducta y P TOTAL finito en su resultados.json sellado; si ninguna
    lo tiene, la última ola con la conducta (sus celdas quedan sin intervalo: no se puntúan)."""
    con = [o for o in olas if _fin(S["res"][tag].get(_ids(S, tag, c, o, "TOTAL", "TODOS")("P")))]
    return (con or list(olas))[-1]


def celdas_de(S):
    """[(tag, conducta, ola_piso, eje, cat)] en orden determinista, derivado de las tablas y pisos sellados."""
    R, Pm, Mg = S["mods"]["RELIGION2024"], S["mods"]["PISOS"], S["mods"]["MIGRACION"]
    out = []
    for c in R.CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(R.EJES_CATS.items()):
            out += [("RELIGION2024", c, R.OLA, eje, cat) for cat in cats]
    for c in _conductas_pisos(Pm):
        piso = ola_piso(S, "PISOS", c, [o for o in Pm.OLAS if c in Pm.OLAS[o][7]])
        for eje, cats in [("TOTAL", ("TODOS",))] + list(Pm.ejes_de(piso).items()):
            out += [("PISOS", c, piso, eje, cat) for cat in cats]
    for c in Mg.CONDUCTAS:
        piso = ola_piso(S, "MIGRACION", c, Mg.olas_de(c))
        for eje, cats in [("TOTAL", ("TODOS",))] + list(Mg.EJES.items()):
            out += [("MIGRACION", c, piso, eje, cat) for cat in cats]
    return out


def _cid(tag, c, eje, cat):
    return f"{tag}-{c}-{eje}-{cat}"


def esquema_resultados():
    return E.esquema(P, [_cid(t, c, e, k) for t, c, _o, e, k in celdas_de(sellados())])


def regla(S, tag, c, piso):
    """("bin", columna, códigos 1, códigos 0) de la conducta en su ola del piso."""
    m = S["mods"][tag]
    if tag == "RELIGION2024":
        return m.CONDUCTAS[c]
    if tag == "PISOS":
        return m.OLAS[piso][7][c]
    var, si, no = m.CONDUCTAS[c][piso]
    return ("bin", var, list(si), list(no))


def columnas_pedidas(S):
    cols = [a for r in DISENO.values() for a in r] + ["religion_combined", "religion_christian"]
    for tag, c, piso, _e, _k in celdas_de(S):
        col = regla(S, tag, c, piso)[1]
        if not col.startswith("_"):
            cols.append(col.lower())
    return list(dict.fromkeys(cols))


def lee_payload_reservado(M, ruta, pedidas):
    """Única lectura de la ola reservada (la auditoría AST lo exige). Primero metadatos del .sav (nombres de
    columna y etiqueta de valor del país: equivalen al libro de códigos); si falta una columna de diseño
    obligatoria o la etiqueta «Mexico» no identifica un solo código, PARO antes de leer una fila. Después, sólo
    las columnas pedidas que existen y sólo las filas de México (el resto de países no sale del lector)."""
    import tempfile
    import zipfile
    from pathlib import Path

    import pyreadstat

    with zipfile.ZipFile(ruta) as z, tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as tmp:
        sav = [n for n in z.namelist() if n.lower().endswith(".sav") and not n.startswith("__MACOSX")]
        if len(sav) != 1:
            raise G.ParoDeGuardia(f"se esperaba 1 miembro .sav, hay {len(sav)}")
        destino = Path(tmp) / "m.sav"
        destino.write_bytes(z.read(sav[0]))
        _, meta = pyreadstat.read_sav(str(destino), metadataonly=True)
        reales = {c.lower(): c for c in meta.column_names}
        faltan = [r for r in OBLIGATORIAS if not any(a in reales for a in DISENO[r])]
        if faltan:
            raise G.ParoDeGuardia(f"columnas de diseño ausentes en 2025: {faltan}")
        pais = next(a for a in DISENO["PAIS"] if a in reales)
        etiquetas = (meta.variable_value_labels or {}).get(reales[pais], {})
        cods = [k for k, v in etiquetas.items() if str(v).strip().lower() == ETIQUETA_PAIS]
        if len(cods) != 1:
            raise G.ParoDeGuardia(f"etiqueta de país «Mexico»: {len(cods)} códigos")
        presentes = [c for c in pedidas if c in reales]
        return M.lee(destino, presentes, pais=(pais, cods[0]))


def _col(frame, rol):
    return next((a for a in DISENO[rol] if a in frame.columns), None)


def _y(S, frame, tag, c, piso, derivadas):
    M = S["M"]
    tipo, col, uno, cero = regla(S, tag, c, piso)
    base = derivadas if col.startswith("_") else frame
    if base is None or col.lower() not in base.columns:
        return None
    y = M.recodifica(base, (tipo, col, uno, cero))
    cond = getattr(S["mods"][tag], "CONDICIONAL", {}) if tag == "MIGRACION" else {}
    if c in cond:
        _t, bcol, bsi, _bno = regla(S, tag, cond[c], piso)
        if bcol.lower() not in frame.columns:
            return None
        y = np.where(np.isin(M.num(frame[bcol.lower()]), bsi), y, np.nan)
    return np.asarray(y, dtype=float)


def mide_r(S, frame):
    """{(tag, conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    M, mods = S["M"], S["mods"]
    faltan = [r for r in OBLIGATORIAS[1:] if _col(frame, r) is None]
    if faltan:
        raise G.ParoDeGuardia(f"columnas de diseño ausentes: {faltan}")
    f, _etiqueta, _n = M.prepara_diseno(frame, peso=_col(frame, "PESO"))
    w = f["_w"].to_numpy()
    edad = M.num(f[_col(frame, "EDAD")])
    nada = np.full(len(f), None, dtype=object)
    sx, ed = _col(frame, "SEXO"), _col(frame, "ESCOLARIDAD")
    sexo = M.eje_mapa(f, sx, SEXO_MAPA) if sx else nada
    edad_motor = M.edad(f, _col(frame, "EDAD"))
    ejes = {"RELIGION2024": {"SEXO": sexo, "EDAD": edad_motor,
                             "ESCOLARIDAD": M.eje_mapa(f, ed, mods["RELIGION2024"].ESCOL) if ed else nada},
            "PISOS": {"SEXO": sexo, "EDAD": edad_motor,
                      "ESCOLARIDAD": M.eje_mapa(f, ed, mods["PISOS"].ESCOL) if ed else nada},
            "MIGRACION": {"SEXO": sexo, "EDAD": M.eje_rango(f, _col(frame, "EDAD"), mods["MIGRACION"].EDADES)}}
    universo = {"RELIGION2024": (edad >= 18) & (edad <= 97), "PISOS": edad >= 18,
                "MIGRACION": (edad >= 18) & (edad <= 97)}
    tiene_rel = {"religion_combined", "religion_christian"} <= set(f.columns)
    derivadas = mods["RELIGION2024"].derivadas(f, M) if tiene_rel else None
    out, hechas = {}, set()
    for tag, c, piso, _e, _k in celdas_de(S):
        if (tag, c) in hechas:
            continue
        hechas.add((tag, c))
        y = _y(S, f, tag, c, piso, derivadas)
        if y is None:
            continue
        y[~universo[tag]] = np.nan
        grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
        grupos.update(ejes[tag])
        for eje, g in grupos.items():
            for cat, r in G.proporcion_por_grupo(y, w, g).items():
                out[(tag, c, eje, cat)] = r["p"]
    return out


def _ids(S, tag, c, piso, eje, cat):
    m = S["mods"][tag]
    if tag == "MIGRACION":
        return lambda q: m.rid(c, piso, eje, cat, q)
    return lambda q: S["M"].rid(m.P, c, piso, eje, cat, q)


def _fin(x):
    return isinstance(x, (int, float)) and x == x and abs(x) != float("inf")


def intervalo(S, tag, c, piso, eje, cat):
    """(lo, hi, punto, fuente): ICC de persistencia si el contendiente lo publica finito; si no, IC-LO/IC-HI."""
    res, rid = S["res"][tag], _ids(S, tag, c, piso, eje, cat)
    lo, hi = res.get(rid("ICC-LO")), res.get(rid("ICC-HI"))
    fuente = "ICC"
    if not (_fin(lo) and _fin(hi)):
        lo, hi, fuente = res.get(rid("IC-LO")), res.get(rid("IC-HI")), "IC"
    return lo, hi, res.get(rid("P")), fuente


def filas(S, r):
    out = []
    for tag, c, piso, eje, cat in celdas_de(S):
        lo, hi, punto, _f = intervalo(S, tag, c, piso, eje, cat)
        out.append({"id": _cid(tag, c, eje, cat), "conglomerado": CONTENDIENTES[tag],
                    "lo": lo, "hi": hi, "punto": punto, "r": r.get((tag, c, eje, cat))})
    return out


def _variables():
    S = sellados()
    vistas, out = set(), []
    for tag, c, piso, _e, _k in celdas_de(S):
        if (tag, c) in vistas:
            continue
        vistas.add((tag, c))
        t, col, uno, cero = regla(S, tag, c, piso)
        out.append({"nombre": f"{tag}-{c}",
                    "definicion": f"{t}({col}: 1={list(uno)}, 0={list(cero)}; resto fuera); códigos de la ola del "
                                  f"piso {piso} de {CONTENDIENTES[tag]}"})
    return out


CONTRATO = {
    "x": X, "programa": "PEW", "ola": "2025", "unidad": "PERSONA",
    "contendientes": list(CONTENDIENTES.values()),
    "payloads": [(PAY, "Pew GAS Spring 2025 (zip con el .sav) -- ola RESERVADA por la spec sellada de los tres "
                       "contendientes; sólo este medidor la lee, sólo filas de México")],
    "repo": [(REL[0], REL[1], "medidor sellado CALC-PEW-RELIGION-2024-0001: CONDUCTAS, ESCOL, EJES_CATS, derivadas"),
             (REL_RES[0], REL_RES[1], "piso 2024 sellado: P, IC-LO, IC-HI por celda"),
             (PIS[0], PIS[1], "medidor sellado CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001: OLAS, ESCOL, ejes_de"),
             (PIS_RES[0], PIS_RES[1], "pisos sellados: P, IC-LO/IC-HI, ICC-LO/ICC-HI por celda"),
             (MIG[0], MIG[1], "medidor sellado CALC-PEW-MIGRACION-MEX-0001: CONDUCTAS, CONDICIONAL, EDADES, rid"),
             (MIG_RES[0], MIG_RES[1], "pisos sellados: P, IC-LO/IC-HI, ICC-LO/ICC-HI por celda"),
             (MOTOR[0], MOTOR[1], "lee, num, recodifica, eje_mapa, eje_rango, edad, prepara_diseno, rid"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Personas entrevistadas en México en Pew GAS Spring 2025 (código de `country` cuya etiqueta de valor es "
                "«Mexico»), weight finito > 0; edad 18-97 (RELIGION2024, MIGRACION) o >= 18 (PISOS), la regla de cada "
                "contendiente; IRIA-SIN-AUTORIZACION sólo entre quienes responden 1 a IRIA-A-VIVIR-A-EEUU",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ESCOLARIDAD donde el contendiente lo publica); nunca cruces (guardia E.6)",
    "ponderador": "weight",
    "transformacion": "Recodificación bin de cada contendiente con los códigos de la ola de su piso (spec §1); "
                      "columna ausente en 2025 -> NO-ESTIMABLE (sin recodificación ad hoc)",
    "estimando": "R = Σw·y/Σw por contendiente×conducta×eje×categoría en Pew 2025 México; cobertura de R en el "
                 "intervalo sellado del piso del contendiente (ICC si finito, si no IC de diseño)",
    "variables": _variables(),
    "dependencias": ["numpy", "pandas", "pyreadstat"],
}


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAY} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    S = sellados(inputs)
    frame = lee_payload_reservado(S["M"], inputs[PAY]["ruta_absoluta"], columnas_pedidas(S))
    return E.salida(P, filas(S, mide_r(S, frame)))
