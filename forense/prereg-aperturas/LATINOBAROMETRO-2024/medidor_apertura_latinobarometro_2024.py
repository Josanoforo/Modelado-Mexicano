#!/usr/bin/env python3
"""Medidor de APERTURA de Latinobarómetro 2024 (México) — ACTO GEN2-APERTURAS-PREREGISTRADAS-1.

Spec humana: `APERTURA-LATINOBAROMETRO-2024-spec-v1_0.md`; contrato: `APERTURA-LATINOBAROMETRO-2024-spec.yaml`;
receta: `RECETA-APERTURA-LATINOBAROMETRO-2024.md`. NO SE HA CORRIDO sobre Latinobarómetro 2024: corre sólo en
caja, en el commit de apertura que mesa autorice.

Una apertura sirve a los dos contendientes sellados antes (E.6), con UNA comparación primaria:
  · CALC-LATINOBAROMETRO-PISOS-2023-0001 (21 conductas; piso 2023, IC de diseño IC-LO/IC-HI)
  · CALC-LATINOBAROMETRO-COLA-2023-0001  (3 conductas; piso 2023, IC de diseño; su ORO-CONFIA-GOBIERNO
                                          repite CONFIA-GOBIERNO del primero y queda fuera: contaría la misma
                                          R dos veces en k/n)
R = Σw·y/Σw por conducta×eje×categoría en las filas `idenpa = 484` de 2024, con la recodificación, el
universo y los ejes de cada contendiente (sus tablas, importadas por bytes con sha256 fijado). Guardia E.6:
auditoría AST de este archivo antes de leer un byte; `guardia_apertura.proporcion_por_grupo` es el único
agregador.
"""
from __future__ import annotations

import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "LATINOBAROMETRO-2024"
P = "RESULT-APERTURA-LATINOBAROMETRO-2024"
OLA = "2024"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

PIS = ("contendiente_pisos_medidor", "data/corrida0/CALC-LATINOBAROMETRO-PISOS-2023-0001/medidor.py",
       "39362de57eba9245d58b5eba63dcfed586cbd0348323d59a6470046e1f826dc5")
PIS_RES = ("contendiente_pisos_resultados", "data/corrida0/CALC-LATINOBAROMETRO-PISOS-2023-0001/resultados.json",
           "0db9ee6d0e150a908425d39be7aa76958efb9db069f0a03161186436ce3d1038")
COL = ("contendiente_cola_medidor", "data/corrida0/CALC-LATINOBAROMETRO-COLA-2023-0001/medidor.py",
       "fa6e98f7516e770dee8e81584a2a8da8681f919ef4c1e0133ee68346226ad38f")
COL_RES = ("contendiente_cola_resultados", "data/corrida0/CALC-LATINOBAROMETRO-COLA-2023-0001/resultados.json",
           "d1e0dbbdd2c81479080dc19c8cd98455a90919aef300039053b688a634d0c11a")
MOTOR = ("motor_pisos_confianza", "tools/dominios/confianza/motor_pisos.py",
         "7d0494f43052e0ea39ce0baf5f6505ccf889b386cfa3c0775b0dbdfb56ef958e")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAY = "latinobarometro2024_bd_stata"

CONTENDIENTES = {"PISOS": "CALC-LATINOBAROMETRO-PISOS-2023-0001", "COLA": "CALC-LATINOBAROMETRO-COLA-2023-0001"}
EXCLUIDAS = {"COLA": ("ORO-CONFIA-GOBIERNO",)}
MIEMBRO_MARCA = "_esp"            # el zip trae .dta en español e inglés: se toma el único *_esp*.dta
OBLIGATORIAS = ("idenpa", "wt", "edad")


def sellados(inputs=None):
    M = E.modulo("motor_pisos_confianza", E.bytes_repo(inputs, *MOTOR))
    mods = {"PISOS": E.modulo("m_latinobarometro_pisos_sellado", E.bytes_repo(inputs, *PIS)),
            "COLA": E.modulo("m_latinobarometro_cola_sellado", E.bytes_repo(inputs, *COL))}
    res = {"PISOS": E.json_repo(inputs, *PIS_RES)["resultados"],
           "COLA": E.json_repo(inputs, *COL_RES)["resultados"]}
    return {"M": M, "mods": mods, "res": res}


def celdas_de(S):
    """[(tag, conducta, eje, cat)] en orden determinista, derivado de las tablas selladas."""
    out = []
    for tag in CONTENDIENTES:
        m = S["mods"][tag]
        for c in m.CONDUCTAS:
            if c in EXCLUIDAS.get(tag, ()):
                continue
            for eje, cats in [("TOTAL", ("TODOS",))] + list(m.EJES_CATS.items()):
                out += [(tag, c, eje, cat) for cat in cats]
    return out


def _cid(tag, c, eje, cat):
    return f"{tag}-{c}-{eje}-{cat}"


def esquema_resultados():
    return E.esquema(P, [_cid(*k) for k in celdas_de(sellados())])


def columnas_pedidas(S):
    cols = list(OBLIGATORIAS)
    for tag in CONTENDIENTES:
        m = S["mods"][tag]
        cols += [r[1].lower() for c, r in m.CONDUCTAS.items() if c not in EXCLUIDAS.get(tag, ())]
        cols += [col.lower() for col, _mapa in m.MAPAS.values()]
    return list(dict.fromkeys(cols))


def lee_payload_reservado(M, ruta, pedidas, pais):
    """Única lectura de la ola reservada (la auditoría AST lo exige). La lista de miembros del zip es envoltura
    (A.7); del .dta en español se leen primero los metadatos (nombres de columna = libro de códigos): si falta
    una columna obligatoria (idenpa, wt, edad), PARO antes de leer una fila. Después, sólo las columnas pedidas
    que existen y sólo las filas de México (el resto de países no sale del lector)."""
    import tempfile
    import zipfile
    from pathlib import Path

    import pyreadstat

    with zipfile.ZipFile(ruta) as z, tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as tmp:
        dta = [n for n in z.namelist() if n.lower().endswith(".dta") and MIEMBRO_MARCA in Path(n).name.lower()
               and not n.startswith("__MACOSX")]
        if len(dta) != 1:
            raise G.ParoDeGuardia(f"se esperaba 1 miembro *{MIEMBRO_MARCA}*.dta, hay {len(dta)}")
        destino = Path(tmp) / "m.dta"
        destino.write_bytes(z.read(dta[0]))
        _, meta = pyreadstat.read_dta(str(destino), metadataonly=True)
        reales = {c.lower() for c in meta.column_names}
        faltan = [c for c in OBLIGATORIAS if c not in reales]
        if faltan:
            raise G.ParoDeGuardia(f"columnas de diseño ausentes en 2024: {faltan}")
        return M.lee(destino, [c for c in pedidas if c in reales], pais=pais)


def mide_r(S, frame):
    """{(tag, conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    M = S["M"]
    faltan = [c for c in OBLIGATORIAS[1:] if c not in frame.columns]
    if faltan:
        raise G.ParoDeGuardia(f"columnas de diseño ausentes: {faltan}")
    out = {}
    for tag in CONTENDIENTES:
        m = S["mods"][tag]
        f, _etiqueta, _n = M.prepara_diseno(frame, peso=m.PESO, estrato=None, upm=m.UPM)
        w = f["_w"].to_numpy()
        nada = np.full(len(f), None, dtype=object)
        ejes = {e: (M.eje_mapa(f, col, mapa) if col.lower() in f.columns else nada)
                for e, (col, mapa) in m.MAPAS.items()}
        ejes["EDAD"] = M.edad(f, m.EDAD_COL)
        universo = M.num(f[m.EDAD_COL.lower()]) >= 18
        grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
        grupos.update({e: ejes[e] for e in m.EJES_CATS})
        for c, regla in m.CONDUCTAS.items():
            if c in EXCLUIDAS.get(tag, ()) or regla[1].lower() not in f.columns:
                continue
            y = np.asarray(M.recodifica(f, regla), dtype=float)
            y[~universo] = np.nan
            for eje, g in grupos.items():
                for cat, r in G.proporcion_por_grupo(y, w, g).items():
                    out[(tag, c, eje, cat)] = r["p"]
    return out


def filas(S, r):
    M, out = S["M"], []
    for tag, c, eje, cat in celdas_de(S):
        m, res = S["mods"][tag], S["res"][tag]
        q = lambda k: res.get(M.rid(m.P, c, m.OLA, eje, cat, k))  # noqa: E731
        out.append({"id": _cid(tag, c, eje, cat), "conglomerado": CONTENDIENTES[tag],
                    "lo": q("IC-LO"), "hi": q("IC-HI"), "punto": q("P"), "r": r.get((tag, c, eje, cat))})
    return out


def _variables():
    S = sellados()
    out = []
    for tag in CONTENDIENTES:
        m = S["mods"][tag]
        for c, (t, col, uno, cero) in m.CONDUCTAS.items():
            if c in EXCLUIDAS.get(tag, ()):
                continue
            out.append({"nombre": f"{tag}-{c}",
                        "definicion": f"{t}({col}: 1={list(uno)}, 0={list(cero)}; resto fuera); códigos de la ola "
                                      f"del piso {m.OLA} de {CONTENDIENTES[tag]}"})
    return out


CONTRATO = {
    "x": X, "programa": "LATINOBAROMETRO", "ola": "2024", "unidad": "PERSONA",
    "contendientes": list(CONTENDIENTES.values()),
    "payloads": [(PAY, "Latinobarómetro 2024 (zip con .dta esp/eng y cuestionarios) -- ola RESERVADA por la spec "
                       "sellada de los dos contendientes; sólo este medidor la lee, sólo idenpa = 484")],
    "repo": [(PIS[0], PIS[1], "medidor sellado CALC-LATINOBAROMETRO-PISOS-2023-0001: CONDUCTAS, MAPAS, EJES_CATS, PAIS"),
             (PIS_RES[0], PIS_RES[1], "piso 2023 sellado: P, IC-LO, IC-HI por celda"),
             (COL[0], COL[1], "medidor sellado CALC-LATINOBAROMETRO-COLA-2023-0001: CONDUCTAS, MAPAS, EJES_CATS"),
             (COL_RES[0], COL_RES[1], "piso 2023 sellado: P, IC-LO, IC-HI por celda"),
             (MOTOR[0], MOTOR[1], "lee, num, recodifica, eje_mapa, edad, prepara_diseno, rid"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Personas entrevistadas en México en Latinobarómetro 2024 (idenpa = 484), wt finito > 0, edad >= 18 "
                "(la regla de los dos contendientes)",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ESCOLARIDAD, TAMLOC, CLASE-SUBJETIVA); nunca cruces (guardia E.6)",
    "ponderador": "wt",
    "transformacion": "Recodificación bin de cada contendiente con los códigos de 2023 (spec §1); columna ausente en "
                      "2024 -> NO-ESTIMABLE; nombre presente con otro texto de pregunta -> re-sello previo (spec §5)",
    "estimando": "R = Σw·y/Σw por contendiente×conducta×eje×categoría en Latinobarómetro 2024 México; cobertura de R "
                 "en el IC de diseño sellado del piso 2023 (IC-LO/IC-HI)",
    "variables": _variables(),
    "dependencias": ["numpy", "pandas", "pyreadstat"],
}


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAY} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    S = sellados(inputs)
    pais = S["mods"]["PISOS"].PAIS
    frame = lee_payload_reservado(S["M"], inputs[PAY]["ruta_absoluta"], columnas_pedidas(S), pais)
    return E.salida(P, filas(S, mide_r(S, frame)))
