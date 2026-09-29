#!/usr/bin/env python3
"""Medidor de APERTURA de ENVIPE 2026 (reserva restante) — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-ENVIPE-2026-spec-v1_0.md`; contrato: `APERTURA-ENVIPE-2026-spec.yaml`;
receta: `RECETA-APERTURA-ENVIPE-2026.md`. NO SE HA CORRIDO sobre ENVIPE 2026.

ENVIPE 2026 ya fue abierta PARCIALMENTE por los duelos sellados (CALC-DUELO-ENVIPE2026-ADJUDICACION-0001,
-MARGINALES-ADJUDICACION-0001): leyeron la tabla de delitos `tmod_vic` (unidad DELITO) y `NIV` de `tsdem`;
«lo que no emita este CALC sigue RESERVADA». Este medidor lee lo que ellos NO leyeron: la tabla de persona
elegida `tper_vic1` (AP4_3_3, AP4_4_A, AP4_10_02 y ejes/diseño) y, por `ID_PER`, `NIV` de `tsdem` como eje.
Ninguna celda del contendiente coincide con una celda vista (spec §1.1).

Al abrir: R = razón ponderada de cada conducta de `CALC-ENVIPE-PERCEPCION-2024-0001` en ENVIPE 2026, por
categoría de UN eje a la vez, con la recodificación y el universo del medidor sellado (CONDUCTAS, MAPAS,
EDADES, EJES_CATS, une; importado por bytes con sha fijado) y el motor de pisos. Contendiente por celda:
piso 2024 con su IC de diseño (IC-LO/IC-HI sellados; sin IC de persistencia). Guardia E.6: auditoría AST
de este archivo antes de leer; `guardia_apertura.proporcion_por_grupo` es el único agregador.
"""
from __future__ import annotations

import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENVIPE-2026"
P = "RESULT-APERTURA-ENVIPE-2026"
OLA_PISO = "2024"
PREF_PISO = "RESULT-ENVIPE-PERCEPCION-2024"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", "data/corrida0/CALC-ENVIPE-PERCEPCION-2024-0001/medidor.py",
           "f0ef11b56f05c1fda1d4f2c1b5e4a60882ec72798d91e09b72cf63aec045e2ab")
PISO = ("contendiente_resultados", "data/corrida0/CALC-ENVIPE-PERCEPCION-2024-0001/resultados.json",
        "40bb5bc35a5454d8cf3ccd12d2bdedca95a91061c0c565e9bc7e0dad19589080")
RECETA = ("receta_pisos_salud", "tools/dominios/salud/pisos_diseno.py",
          "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9")
MOTOR = ("motor_pisos_confianza", "tools/dominios/confianza/motor_pisos.py",
         "7d0494f43052e0ea39ce0baf5f6505ccf889b386cfa3c0775b0dbdfb56ef958e")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOAD = "envipe2026_csv"
# Miembros por sufijo (la carpeta interna cambia de ola en ola; así los resolvió el duelo sellado:
# RESULT-DUELO26-ADJ-R-ND-MIEMBRO = tmod_vic_envipe2026/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2026.csv).
SUF_PER = "conjunto_de_datos_tper_vic1_envipe2026.csv"
SUF_SDEM = "conjunto_de_datos_tsdem_envipe2026.csv"
ESTRUCTURA_PER = ("ID_PER", "EDAD", "FAC_ELE", "EST_DIS", "UPM_DIS")   # ausente -> PARO
ESTRUCTURA_SDEM = ("ID_PER",)
DOMINIO = {"U": "URBANO", "C": "COMPLEMENTO-URBANO", "R": "RURAL"}   # mide() del contendiente, verbatim

CONTRATO = {
    "x": X, "programa": "ENVIPE", "ola": "2026", "unidad": "PERSONA",
    "contendientes": ["CALC-ENVIPE-PERCEPCION-2024-0001"],
    "payloads": [(PAYLOAD, "ENVIPE 2026 datos abiertos CSV -- reserva RESTANTE (tper_vic1 y tsdem.NIV como eje de "
                           "persona elegida); tmod_vic ya consumida por los duelos sellados; sólo este medidor la lee")],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: CONDUCTAS, MAPAS, EDADES, EJES_CATS, COLS_*, une"),
             (PISO[0], PISO[1], "piso 2024 sellado: P, IC-LO, IC-HI por celda"),
             (RECETA[0], RECETA[1], "lee_csv_zip, miembro_unico de la receta de pisos"),
             (MOTOR[0], MOTOR[1], "prepara_diseno, recodifica, eje_mapa, eje_rango, num del motor de pisos"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Persona elegida de 18-97 años (EDAD), ENVIPE 2026, tabla tper_vic1; FAC_ELE > 0, EST_DIS y UPM_DIS no "
                "vacíos (universo del contendiente); NIV de tsdem por ID_PER",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ESCOLARIDAD, DOMINIO, ENTIDAD); nunca cruces (guardia E.6)",
    "ponderador": "FAC_ELE",
    "transformacion": "Recodificación del contendiente (spec COLA-ENVIPE-PERCEPCION §2: bin(col, UNO, CERO)); "
                      "columna ausente en el catálogo 2026 -> NO-ESTIMABLE (R None), sin recodificación ad hoc",
    "estimando": "R = Σw·y/Σw por conducta×eje×categoría en ENVIPE 2026; cobertura de R en el IC de diseño del piso 2024",
    "variables": [{"nombre": "ESTADO-INSEGURO", "definicion": "AP4_3_3 = 2 frente a 1 (spec contendiente §2)"},
                  {"nombre": "INSEGURO-CAMINAR-DE-NOCHE", "definicion": "AP4_4_A ∈ {3,4} frente a {1,2} (spec contendiente §2)"},
                  {"nombre": "DEJO-PERMITIR-MENORES-SALIR-SOLOS",
                   "definicion": "AP4_10_02 = 1 frente a 2 (spec contendiente §2)"}],
}


def sellados(inputs=None):
    S = E.modulo("m_envipe_percepcion_sellado", E.bytes_repo(inputs, *SELLADO))
    R = E.modulo("receta_pisos_salud_envipe", E.bytes_repo(inputs, *RECETA))
    M = E.modulo("motor_pisos_confianza_envipe", E.bytes_repo(inputs, *MOTOR))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return S, R, M, piso


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(S):
    out = []
    for c in S.CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(S.EJES_CATS.items()):
            out += [(c, eje, cat) for cat in cats]
    return out


def esquema_resultados():
    S, _R, _M, _p = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(S)])


def lee_payload_reservado(S, R, ruta):
    """Única lectura de la ola reservada (la auditoría AST lo exige): (tper_vic1, tsdem) con las columnas del
    contendiente que existan; estructura ausente es PARO; conducta o eje ausente queda vacío (-> NO-ESTIMABLE)."""
    import zipfile

    tablas = []
    for suf, cols, estructura in ((SUF_PER, S.COLS_PER, ESTRUCTURA_PER), (SUF_SDEM, S.COLS_SDEM, ESTRUCTURA_SDEM)):
        with zipfile.ZipFile(ruta) as z:
            cands = [n for n in z.namelist() if n.lower().endswith(suf) and not n.startswith("__MACOSX")]
            if len(cands) != 1:
                raise G.ParoDeGuardia(f"*{suf}: {len(cands)} miembros ({cands})")
            with z.open(cands[0]) as fh:
                crudo = fh.readline()
        try:
            cab = crudo.decode("utf-8")
        except UnicodeDecodeError:
            cab = crudo.decode("latin-1")
        reales = {c.strip().strip('"').upper() for c in cab.strip().split(",")}
        faltan = [c for c in estructura if c not in reales]
        if faltan:
            raise G.ParoDeGuardia(f"columnas de estructura ausentes en {cands[0]}: {faltan}")
        f = R.lee_csv_zip(ruta, [c for c in cols if c in reales], miembro=cands[0])
        for c in cols:
            if c.lower() not in f.columns:
                f[c.lower()] = ""
        tablas.append(f)
    return tablas[0], tablas[1]


def mide_r(S, M, per, sdem):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    f, _etiqueta, _descartadas = M.prepara_diseno(S.une(per, sdem), peso="FAC_ELE", estrato="EST_DIS", upm="UPM_DIS")
    ejes = {e: M.eje_mapa(f, col, mapa) for e, (col, mapa) in S.MAPAS.items()}
    ejes["EDAD"] = M.eje_rango(f, "EDAD", S.EDADES)
    ejes["DOMINIO"] = f["dominio"].astype(str).str.strip().map(DOMINIO).to_numpy(dtype=object)
    edad = M.num(f["edad"])
    universo = (edad >= 18) & (edad <= 97)
    w = f["_w"].to_numpy(dtype=float)
    out = {}
    for c, regla in S.CONDUCTAS.items():
        y = np.asarray(M.recodifica(f, regla), dtype=float)
        y[~universo] = np.nan
        grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
        grupos.update({e: np.asarray(ejes[e], dtype=object) for e in S.EJES_CATS})
        for eje, g in grupos.items():
            for cat, r in G.proporcion_por_grupo(y, w, g).items():
                out[(c, eje, cat)] = r["p"]
    return out


def filas(S, M, r, piso):
    return [{"id": _cid(c, eje, cat), "conglomerado": c,
             "lo": piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, "IC-LO")),
             "hi": piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, "IC-HI")),
             "punto": piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, "P")),
             "r": r.get((c, eje, cat))} for c, eje, cat in celdas_de(S)]


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAYLOAD} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    S, R, M, piso = sellados(inputs)
    per, sdem = lee_payload_reservado(S, R, inputs[PAYLOAD]["ruta_absoluta"])
    return E.salida(P, filas(S, M, mide_r(S, M, per, sdem), piso))
