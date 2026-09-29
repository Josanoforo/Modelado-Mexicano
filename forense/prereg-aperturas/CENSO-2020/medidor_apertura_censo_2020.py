#!/usr/bin/env python3
"""Medidor de APERTURA del Censo 2020 (muestra censal, cuestionario ampliado) — ACTO GEN2-APERTURAS-PREREGISTRADAS-1.

29/sep/2026. Spec humana: `APERTURA-CENSO-2020-spec-v1_0.md`; contrato: `APERTURA-CENSO-2020-spec.yaml`;
receta: `RECETA-APERTURA-CENSO-2020.md`. NO SE HA CORRIDO sobre el Censo 2020: corre sólo en caja, en el
commit de apertura que mesa autorice.

Una apertura sirve a los dos contendientes sellados que declaran «Censo 2020 RESERVADO» (E.6):
  · `CALC-EIC-HOGARES-2015-0001` (Intercensal 2015, tabla de viviendas: TIPOHOG, JEFE_SEXO, TAMLOC, ENT);
    celdas `EIC15-<conducta>-<eje>-<cat>`.
  · `CALC-CCPV-FAM-PISOS-0001` (muestra censal 2010, viviendas + personas; 12 proporciones, 1 media y
    PER60-VIVE-SOLO de persona); celdas `CCPV10-<conducta>-<eje>-<cat>`.
R = razón ponderada Σw·y/Σw (media ponderada en HOG-TAMANO-MEDIO) en la muestra censal 2020, por categoría
de UN eje a la vez, con la recodificación y el marco de cada medidor sellado (importados por bytes con sha
fijado). Códigos y nombres de columna fijados sobre la ola del piso: columna ausente en 2020 -> vacía ->
NO-ESTIMABLE. Contendiente por celda: su P con el IC de diseño sellado (IC-LO/IC-HI; sin persistencia).
Guardia E.6: auditoría AST de este archivo antes de leer; `guardia_apertura.proporcion_por_grupo` es el
único agregador.
"""
from __future__ import annotations

import os
import re

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "CENSO-2020"
P = "RESULT-APERTURA-CENSO-2020"
PREF_EIC, PREF_CCPV = "EIC15", "CCPV10"
OLA_EIC = "2015"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

EIC_MED = ("eic_medidor", "data/corrida0/CALC-EIC-HOGARES-2015-0001/medidor.py",
           "70143371f65ec58c4c87d2ee5bfa016e53a4066bed27bf678584a28c9389b0cb")
EIC_RES = ("eic_resultados", "data/corrida0/CALC-EIC-HOGARES-2015-0001/resultados.json",
           "9f92fc2f6484cd136c31f142c69092208b5bfc74e13ea988327b36c985b704f1")
CCPV_MED = ("ccpv_medidor", "data/corrida0/CALC-CCPV-FAM-PISOS-0001/medidor.py",
            "61de9a68a70ae2db02d0968f2a1d045c0793ffae5240cc8fe0f344940df92808")
CCPV_RES = ("ccpv_resultados", "data/corrida0/CALC-CCPV-FAM-PISOS-0001/resultados.json",
            "5cbf8273f2859b7b3e24368db03f9f811914e8b3413a48ca862c6f48d0b553a3")
RECETA = ("receta_pisos", "tools/dominios/salud/pisos_diseno.py",
          "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9")
MOTOR = ("motor_pisos_confianza", "tools/dominios/confianza/motor_pisos.py",
         "7d0494f43052e0ea39ce0baf5f6505ccf889b386cfa3c0775b0dbdfb56ef958e")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")

# Muestra censal 2020 (cuestionario ampliado), 32 ZIP estatales del manifiesto, en orden de clave de entidad.
ABREV = ("ags", "bc", "bcs", "cam", "coa", "col", "chs", "chh", "cdmx", "dgo", "gto", "gro", "hgo", "jal", "mex",
         "mich", "mor", "nay", "nl", "oax", "pue", "qro", "qroo", "slp", "sin", "son", "tab", "tam", "tla", "ver",
         "yuc", "zac")
PAYLOADS = {f"{i:02d}": f"cc1_inegi_ccpv_2020__censo2020_ca_{a}_csv" for i, a in enumerate(ABREV, start=1)}
RX_VIV = re.compile(r"(?i)(^|/)viviendas[^/]*\.csv$")
RX_PER = re.compile(r"(?i)(^|/)personas[^/]*\.csv$")
# Celdas cuya R 2020 ya fue vista (cifras publicadas de hogares citadas en el repo antes de este expediente:
# canon/mapa-dominios-v1_1.tsv FAM-025 «24.4% ampliados, 12.4% unipersonales», VEJEZ-006 «16.8% unipersonales
# entre hogares con 60+ ... 1.8 millones de personas de 60+», y forense/prereg-caja/CCPV-FAM-PISOS-spec-v1_0.md §5
# «82 % / 16.8 % entre hogares con 60+»). Son RETROSPECTIVAS: R se emite, no puntúan en la primaria
# PROSPECTIVA (lo/hi None); su cobertura va aparte en la nota, rotulada así (E.6, §4 v2.16).
VISTAS = frozenset({
    "EIC15-HOGAR-AMPLIADO-TOTAL-TODOS", "EIC15-HOGAR-UNIPERSONAL-TOTAL-TODOS",
    "CCPV10-HOG-AMPLIADO-TOTAL-TODOS", "CCPV10-HOG-UNIPERSONAL-TOTAL-TODOS",
    "CCPV10-AM-HOG-UNIPERSONAL-TOTAL-TODOS", "CCPV10-AM-HOG-NUCLEAR-O-AMPLIADO-TOTAL-TODOS",
    "CCPV10-PER60-VIVE-SOLO-TOTAL-TODOS",
})
ESTRUCTURA_VIV = ("ENT", "ID_VIV", "FACTOR", "ESTRATO", "UPM")          # ausente -> PARO
ESTRUCTURA_PER = ("ENT", "ID_VIV", "EDAD", "FACTOR", "ESTRATO", "UPM")

CONTRATO = {
    "x": X, "programa": "CCPV", "ola": "2020", "unidad": "HOGAR",
    "contendientes": ["CALC-EIC-HOGARES-2015-0001", "CALC-CCPV-FAM-PISOS-0001"],
    "payloads": [(pid, f"Censo 2020, muestra censal (cuestionario ampliado), entidad {e}: tablas VIVIENDAS y PERSONAS "
                       "-- ola RESERVADA por los contendientes; sólo este medidor la lee")
                 for e, pid in PAYLOADS.items()],
    "repo": [(EIC_MED[0], EIC_MED[1], "medidor sellado EIC 2015: CONDUCTAS, MAPAS, EJES_CATS, PESO/ESTRATO/UPM"),
             (EIC_RES[0], EIC_RES[1], "piso EIC 2015 sellado: P, IC-LO, IC-HI por celda"),
             (CCPV_MED[0], CCPV_MED[1], "medidor sellado CCPV 2010: prepara, conducta_hogar, conducta_persona, EJES_*"),
             (CCPV_RES[0], CCPV_RES[1], "piso CCPV 2010 sellado: P, IC-LO, IC-HI por celda"),
             (RECETA[0], RECETA[1], "lee_csv_zip y num de la receta de pisos"),
             (MOTOR[0], MOTOR[1], "prepara_diseno, recodifica, eje_mapa del motor de pisos (contendiente EIC)"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Muestra censal 2020: viviendas particulares habitadas de la tabla VIVIENDAS (EIC15: TIPOHOG en "
                "1,2,3,5,6; CCPV10: universo de cada conducta en su spec §2) y personas 60+ de PERSONAS (PER60-*); "
                "FACTOR > 0, ESTRATO y UPM no vacíos",
    "filtros": "Un eje a la vez (EIC15: TOTAL, JEFATURA, TAMLOC, ENTIDAD; CCPV10 hogar: TOTAL, SEXO-JEFE, EDAD-JEFE, "
               "ESCOLARIDAD-JEFE, TLOC, ENT; persona: TOTAL, SEXO, EDAD, TLOC, ENT); nunca cruces (guardia E.6)",
    "ponderador": "FACTOR (VIVIENDAS para hogar; PERSONAS para PER60-*)",
    "transformacion": "Recodificación de cada contendiente con los nombres y códigos de su ola (EIC 2015; muestra 2010); "
                      "columna ausente en 2020 (p. ej. tam_loc, parent) -> vacía -> NO-ESTIMABLE, sin recodificación ad hoc",
    "estimando": "R = Σw·y/Σw por conducta×eje×categoría en la muestra censal 2020 (media ponderada en HOG-TAMANO-MEDIO); "
                 "cobertura de R en el IC de diseño de cada piso (EIC 2015, CCPV 2010)",
    "variables": ([{"nombre": f"{PREF_EIC}-{c}", "definicion": "tipo de hogar de TIPOHOG (spec COLA-EIC-HOGARES §2)"}
                   for c in ("HOGAR-AMPLIADO", "HOGAR-NUCLEAR", "HOGAR-UNIPERSONAL", "HOGAR-AMPLIADO-ENTRE-FAMILIARES")]
                  + [{"nombre": f"{PREF_CCPV}-{c}", "definicion": "conducta de hogar o persona 60+ (spec CCPV-FAM-PISOS §2)"}
                     for c in ("HOG-NUCLEAR", "HOG-AMPLIADO", "HOG-COMPUESTO", "HOG-UNIPERSONAL", "HOG-CORRESIDENTES",
                               "HOG-CON-60MAS", "HOG-CON-MENOR-18", "HOG-60MAS-Y-MENOR-18", "HOG-TRES-GENERACIONES",
                               "HOG-JEFA-MUJER", "HOG-TAMANO-MEDIO", "AM-HOG-NUCLEAR-O-AMPLIADO", "AM-HOG-UNIPERSONAL",
                               "PER60-VIVE-SOLO")]),
}


def sellados(inputs=None):
    SE = E.modulo("m_eic_hogares_sellado", E.bytes_repo(inputs, *EIC_MED))
    SC = E.modulo("m_ccpv_fam_sellado", E.bytes_repo(inputs, *CCPV_MED))
    R = E.modulo("receta_pisos_censo", E.bytes_repo(inputs, *RECETA))
    M = E.modulo("motor_pisos_confianza_censo", E.bytes_repo(inputs, *MOTOR))
    pe = E.json_repo(inputs, *EIC_RES)["resultados"]
    pc = E.json_repo(inputs, *CCPV_RES)["resultados"]
    return SE, SC, R, M, pe, pc


def celdas_eic(SE):
    out = []
    for c in SE.CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(SE.EJES_CATS.items()):
            out += [(c, eje, cat) for cat in cats]
    return out


def celdas_ccpv(SC):
    out = []
    for conds, ejes in ((SC.HOGAR, SC.EJES_HOG), (SC.PERSONA, SC.EJES_PER)):
        for c in conds:
            for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes.items()):
                out += [(c, eje, cat) for cat in cats]
    return out


def _cid(pref, c, eje, cat):
    return f"{pref}-{c}-{eje}-{cat}"


def esquema_resultados():
    SE, SC, _R, _M, _pe, _pc = sellados()
    celdas = [_cid(PREF_EIC, *k) for k in celdas_eic(SE)] + [_cid(PREF_CCPV, *k) for k in celdas_ccpv(SC)]
    esq = E.esquema(P, celdas)
    medias = {f"{P}-{_cid(PREF_CCPV, *k)}-R" for k in celdas_ccpv(SC) if k[0] in SC.MEDIAS}
    for f in esq:
        if f["id"] in medias:
            f["tipo"] = "flotante"
            f["unidad"] = "media ponderada de personas por hogar en la ola reservada"
    return esq


def lee_payload_reservado(SE, SC, R, rutas):
    """Única lectura de la ola reservada (la auditoría AST lo exige): (VIVIENDAS, PERSONAS) de las 32 entidades,
    columnas en minúsculas; estructura ausente es PARO; conducta o eje ausente queda vacío (-> NO-ESTIMABLE)."""
    import zipfile

    cols_viv = list(dict.fromkeys([c.upper() for c in SE.COLS_CRUDAS] + [c.upper() for c in SC.COLS_VIV]))
    cols_per = [c.upper() for c in SC.COLS_PER]
    vs, ps = [], []
    for e, ruta in rutas.items():
        if not os.path.basename(ruta).lower() == f"censo2020_ca_{ABREV[int(e) - 1]}_csv.zip":
            raise G.ParoDeGuardia(f"entidad {e}: {ruta} no es la muestra censal 2020 de esa entidad")
        for rx, cols, estructura, dest in ((RX_VIV, cols_viv, ESTRUCTURA_VIV, vs), (RX_PER, cols_per, ESTRUCTURA_PER, ps)):
            with zipfile.ZipFile(ruta) as z:
                cands = [n for n in z.namelist() if rx.search(n) and not n.startswith("__MACOSX")]
                if len(cands) != 1:
                    raise G.ParoDeGuardia(f"entidad {e}: {len(cands)} miembros para {rx.pattern} ({cands})")
                with z.open(cands[0]) as fh:
                    crudo = fh.readline()
            try:
                cab = crudo.decode("utf-8")
            except UnicodeDecodeError:
                cab = crudo.decode("latin-1")
            reales = {c.strip().strip('"').upper() for c in cab.strip().split(",")}
            faltan = [c for c in estructura if c not in reales]
            if faltan:
                raise G.ParoDeGuardia(f"entidad {e}: columnas de estructura ausentes en {cands[0]}: {faltan}")
            f = R.lee_csv_zip(ruta, [c for c in cols if c in reales], miembro=cands[0])
            for c in cols:
                if c.lower() not in f.columns:
                    f[c.lower()] = ""
            dest.append(f)
    return pd.concat(vs, ignore_index=True), pd.concat(ps, ignore_index=True)


def mide_r_eic(SE, M, viv):
    """{(conducta, eje, cat): p} del contendiente EIC con UNA variable de agrupación por llamada."""
    f, _et, _d = M.prepara_diseno(viv[[c.lower() for c in SE.COLS_CRUDAS]], peso=SE.PESO, estrato=SE.ESTRATO, upm=SE.UPM)
    ejes = {e: M.eje_mapa(f, col, mapa) for e, (col, mapa) in SE.MAPAS.items()}
    tipo = M.num(f["tipohog"])
    universo = (tipo == 1) | (tipo == 2) | (tipo == 3) | (tipo == 5) | (tipo == 6)
    w = f["_w"].to_numpy(dtype=float)
    out = {}
    for c, regla in SE.CONDUCTAS.items():
        y = np.asarray(M.recodifica(f, regla), dtype=float)
        y[~universo] = np.nan
        grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
        grupos.update({e: np.asarray(ejes[e], dtype=object) for e in SE.EJES_CATS})
        for eje, g in grupos.items():
            for cat, r in G.proporcion_por_grupo(y, w, g).items():
                out[(c, eje, cat)] = r["p"]
    return out


def mide_r_ccpv(SC, R, viv, per):
    """{(conducta, eje, cat): p} del contendiente CCPV con UNA variable de agrupación por llamada."""
    fv, fp, ejes_h, ejes_p, _diag = SC.prepara(viv[list(SC.COLS_VIV)], per[list(SC.COLS_PER)], R)
    out = {}
    for conds, f, ejes, fn in ((SC.HOGAR, fv, ejes_h, SC.conducta_hogar), (SC.PERSONA, fp, ejes_p, SC.conducta_persona)):
        w = f["_w"].to_numpy(dtype=float)
        grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
        grupos.update({e: np.asarray(serie, dtype=object) for e, (serie, _cats) in ejes.items()})
        for c in conds:
            y = np.asarray(fn(c, f, R), dtype=float)
            for eje, g in grupos.items():
                for cat, r in G.proporcion_por_grupo(y, w, g).items():
                    out[(c, eje, cat)] = r["p"]
    return out


def _fila(cid, cong, q, r, punto=True):
    vista = cid in VISTAS
    return {"id": cid, "conglomerado": cong, "lo": None if vista else q["IC-LO"], "hi": None if vista else q["IC-HI"],
            "punto": q["P"] if punto else None, "r": r}


def filas(SE, SC, M, r_eic, r_ccpv, pe, pc):
    out = []
    for c, eje, cat in celdas_eic(SE):
        q = {k: pe.get(M.rid(SE.P, c, OLA_EIC, eje, cat, k)) for k in ("P", "IC-LO", "IC-HI")}
        out.append(_fila(_cid(PREF_EIC, c, eje, cat), f"{PREF_EIC}-{c}", q, r_eic.get((c, eje, cat))))
    for c, eje, cat in celdas_ccpv(SC):
        q = {k: pc.get(SC.rid(c, eje, cat, k)) for k in ("P", "IC-LO", "IC-HI")}
        # MAE-PUNTO sólo sobre proporciones de hogar: la media (personas/hogar) y PER60 (unidad persona) no se
        # promedian con ellas (§4 v2.16); sí cuentan en la cobertura, que es un conteo de celdas.
        punto = not (c in SC.MEDIAS or c in SC.PERSONA)
        out.append(_fila(_cid(PREF_CCPV, c, eje, cat), f"{PREF_CCPV}-{c}", q, r_ccpv.get((c, eje, cat)), punto))
    return out


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = set(PAYLOADS.values()) | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    SE, SC, R, M, pe, pc = sellados(inputs)
    viv, per = lee_payload_reservado(SE, SC, R, {e: inputs[pid]["ruta_absoluta"] for e, pid in PAYLOADS.items()})
    return E.salida(P, filas(SE, SC, M, mide_r_eic(SE, M, viv), mide_r_ccpv(SC, R, viv, per), pe, pc))
