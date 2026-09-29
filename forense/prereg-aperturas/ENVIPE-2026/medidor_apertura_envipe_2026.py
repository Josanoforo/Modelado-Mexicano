#!/usr/bin/env python3
"""Medidor de APERTURA de ENVIPE 2026 (reserva restante) — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-ENVIPE-2026-spec-v1_0.md`; contrato: `APERTURA-ENVIPE-2026-spec.yaml`;
receta: `RECETA-APERTURA-ENVIPE-2026.md`. NO SE HA CORRIDO sobre ENVIPE 2026.

ENVIPE 2026 ya fue abierta PARCIALMENTE por los duelos sellados (CALC-DUELO-ENVIPE2026-ADJUDICACION-0001,
-MARGINALES-ADJUDICACION-0001): leyeron la tabla de delitos `tmod_vic` (unidad DELITO) y `NIV` de `tsdem`;
«lo que no emita este CALC sigue RESERVADA». Este medidor lee lo que ellos NO leyeron: la tabla de persona
elegida `tper_vic1` (AP4_* de los dos contendientes y ejes/diseño) y, por `ID_PER`, `NIV` de `tsdem` como eje;
de `tmod_vic` (ya abierta) sólo lee las columnas de MC2, para celdas RETROSPECTIVAS que no puntúan.
Ninguna celda de PERCEPCION coincide con una celda vista (spec §0.1).

Dos contendientes sellados antes de abrir (E.6: una apertura sirve a todos, una sola comparación primaria):

  · `CALC-ENVIPE-PERCEPCION-2024-0001` — R = razón ponderada de cada conducta en ENVIPE 2026 por categoría
    de UN eje a la vez, con la recodificación y el universo del medidor sellado (CONDUCTAS, MAPAS, EDADES,
    EJES_CATS, une; importado por bytes con sha fijado) y el motor de pisos. Contendiente por celda: piso
    2024 con su IC de diseño (IC-LO/IC-HI sellados; sin IC de persistencia).
  · `CALC-MC2-ENVIPE2025-0001` — R = razón ponderada de cada celda del medidor sellado (frame_del,
    frame_per, celdas_del, celdas_per; su propio lector `_lee`, por bytes con sha fijado) con la ola 2026 en
    la ranura de la última ola de cada estimando; contendiente: su P e IC95 bootstrap de esa última ola.
    Celdas marcadas en el id (A.16): `MC2-<celda>` PROSPECTIVA y puntuada; `MC2-RETROSPECTIVA-<celda>`
    (tmod_vic, unidad DELITO: tabla abierta por los duelos antes del COMMIT-1 de MC2) y
    `MC2-DUPLICADA-<celda>` (mismo estimando que una celda de PERCEPCION, que la puntúa) emiten R y no
    puntúan. EDO-INSEGURO-2024 (ola superada por 2025) y la diferencia SINALOA 2025-2024 se apartan.

Guardia E.6: auditoría AST de este archivo antes de leer; `guardia_apertura.proporcion_por_grupo` es el
único agregador (una variable de agrupación por llamada); única lectura: `lee_payload_reservado`.
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
SELLADO_MC2 = ("mc2_medidor", "data/corrida0/CALC-MC2-ENVIPE2025-0001/medidor.py",
               "6cfd637b68d2dddfd664d92e2685b86af0272222a48fb4ebbb996194cf927ea8")
PISO_MC2 = ("mc2_resultados", "data/corrida0/CALC-MC2-ENVIPE2025-0001/resultados.json",
            "d004f24f61b4844bb5f49e8da70eb65eb19df5a1081edff4dfef51635be4fded")
CALC_PERC = "CALC-ENVIPE-PERCEPCION-2024-0001"
CALC_MC2 = "CALC-MC2-ENVIPE2025-0001"
PAYLOAD = "envipe2026_csv"
# Miembros por sufijo (la carpeta interna cambia de ola en ola; así los resolvió el duelo sellado:
# RESULT-DUELO26-ADJ-R-ND-MIEMBRO = tmod_vic_envipe2026/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2026.csv).
SUF_PER = "conjunto_de_datos_tper_vic1_envipe2026.csv"
SUF_SDEM = "conjunto_de_datos_tsdem_envipe2026.csv"
SUF_DEL = "conjunto_de_datos_tmod_vic_envipe2026.csv"   # sólo para MC2 (celdas RETROSPECTIVAS)
ESTRUCTURA_PER = ("ID_PER", "EDAD", "FAC_ELE", "EST_DIS", "UPM_DIS")   # ausente -> PARO
ESTRUCTURA_SDEM = ("ID_PER",)
DOMINIO = {"U": "URBANO", "C": "COMPLEMENTO-URBANO", "R": "RURAL"}   # mide() del contendiente, verbatim

# ── CALC-MC2-ENVIPE2025-0001 (spec humana forense/prereg-caja/MC2-ENVIPE2025-spec-v1_0.md) ──────────────
# Tablas 2026 que lee su recodificación: la ola 2026 ocupa la ranura de la última ola de cada estimando
# (los nombres de tabla son los que su `frame_del`/`frame_per` piden a `_lee`).
TABLA_DEL_26 = "tmod_vic_envipe2026"
TABLA_PER_26 = "tper_vic1_envipe2026"
RANURAS_MC2 = {"tmod_vic_envipe2025": TABLA_DEL_26, "tper_vic1_envipe2024": TABLA_PER_26,
               "tper_vic1_envipe2025": TABLA_PER_26}
ESTRUCTURA_MC2 = {TABLA_DEL_26: ("EST_DIS", "UPM_DIS", "FAC_DEL"), TABLA_PER_26: ("EST_DIS", "UPM_DIS", "FAC_ELE")}
# Clasificación de las celdas del árbitro (resultados.json de MC2), por prefijo del id sin `PFX-` (spec §0.2):
RETRO_MC2 = "DEL-"                     # tmod_vic (DELITO): RETROSPECTIVA, R sin puntuar
DUP_MC2 = "EDO-INSEGURO-2025-"         # duplica ESTADO-INSEGURO de PERCEPCION: R sin puntuar
APARTA_MC2 = ("EDO-INSEGURO-2024-", "EDO-INSEGURO-SINALOA-DIF-")   # ola superada; diferencia entre olas
# Gemelo en PERCEPCION de cada segmento de EDO-INSEGURO-2025 (mismo reactivo AP4_3_3 2/1, FAC_ELE, tper_vic1).
GEMELO_SEG = {"NAC": ("TOTAL", "TODOS"), "HOMBRE": ("SEXO", "HOMBRE"), "MUJER": ("SEXO", "MUJER"),
              "DOM-U": ("DOMINIO", "URBANO"), "DOM-C": ("DOMINIO", "COMPLEMENTO-URBANO"),
              "DOM-R": ("DOMINIO", "RURAL"), "SINALOA": ("ENTIDAD", "25")}
# v2.16 §4: `-MAE-PUNTO` (descriptivo) no promedia delito con persona: el punto de las celdas DELITO va None
# (además no puntúan; la cobertura, que es la primaria, sólo usa celdas PERSONA).
UNIDAD_MAE = "PERSONA"

CONTRATO = {
    "x": X, "programa": "ENVIPE", "ola": "2026", "unidad": "PERSONA",
    "contendientes": [CALC_PERC, CALC_MC2],
    "payloads": [(PAYLOAD, "ENVIPE 2026 datos abiertos CSV -- reserva RESTANTE: tper_vic1 (los dos contendientes) y "
                           "tsdem.NIV como eje de persona elegida; tmod_vic (ya abierta por los duelos sellados) sólo para "
                           "las celdas RETROSPECTIVAS de MC2, sin puntuar; sólo este medidor la lee")],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: CONDUCTAS, MAPAS, EDADES, EJES_CATS, COLS_*, une"),
             (PISO[0], PISO[1], "piso 2024 sellado: P, IC-LO, IC-HI por celda"),
             (RECETA[0], RECETA[1], "lee_csv_zip, miembro_unico de la receta de pisos"),
             (MOTOR[0], MOTOR[1], "prepara_diseno, recodifica, eje_mapa, eje_rango, num del motor de pisos"),
             (SELLADO_MC2[0], SELLADO_MC2[1], "medidor sellado de CALC-MC2-ENVIPE2025-0001: _lee, frame_del, frame_per, "
                                              "celdas_del, celdas_per, PFX, PREOC, AP44, COLS_* (no importa recetas)"),
             (PISO_MC2[0], PISO_MC2[1], "resultados sellados de MC2: rejilla de celdas y P, IC95-INF, IC95-SUP por celda"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "PERCEPCION: persona elegida de 18-97 años (EDAD), ENVIPE 2026, tabla tper_vic1; FAC_ELE > 0, EST_DIS y "
                "UPM_DIS no vacíos; NIV de tsdem por ID_PER. MC2: el de su medidor sellado -- persona elegida de "
                "tper_vic1 con FAC_ELE > 0 y UPM_DIS no vacía (sin tope de EDAD); delitos de tmod_vic con FAC_DEL > 0 "
                "(celdas RETROSPECTIVAS, no puntúan)",
    "filtros": "Un eje a la vez (PERCEPCION: TOTAL, SEXO, EDAD, ESCOLARIDAD, DOMINIO, ENTIDAD; MC2: un segmento "
               "NAC/SEXO/DOMINIO/EDAD/SINALOA por llamada); nunca cruces (guardia E.6)",
    "ponderador": "FAC_ELE (persona elegida); FAC_DEL sólo en las celdas RETROSPECTIVAS de MC2 (delito)",
    "transformacion": "Recodificación de cada contendiente, sin tocar: PERCEPCION (spec COLA-ENVIPE-PERCEPCION §2: "
                      "bin(col, UNO, CERO)); MC2 (frame_del/frame_per de su medidor sellado, con la ola 2026 en la ranura "
                      "de la última ola de cada estimando). Columna ausente en el catálogo 2026 -> NO-ESTIMABLE (R None), "
                      "sin recodificación ad hoc",
    "estimando": "R = Σw·y/Σw por celda en ENVIPE 2026; cobertura de R en el IC del contendiente (PERCEPCION: IC de "
                 "diseño del piso 2024; MC2: IC95 bootstrap de su última ola). Una sola primaria sobre todas las celdas "
                 "puntuadas (todas de unidad PERSONA)",
    "variables": [{"nombre": "ESTADO-INSEGURO", "definicion": "AP4_3_3 = 2 frente a 1 (spec contendiente §2)"},
                  {"nombre": "INSEGURO-CAMINAR-DE-NOCHE", "definicion": "AP4_4_A ∈ {3,4} frente a {1,2} (spec contendiente §2)"},
                  {"nombre": "DEJO-PERMITIR-MENORES-SALIR-SOLOS",
                   "definicion": "AP4_10_02 = 1 frente a 2 (spec contendiente §2)"},
                  {"nombre": "MC2-DEJO-SALIR-NOCHE",
                   "definicion": "AP4_10_01 = 1 frente a 2; piso ENVIPE 2024 (spec MC2 §1; PROSPECTIVA; unidad PERSONA)"},
                  {"nombre": "MC2-PREOC-<tema>",
                   "definicion": "AP4_2_<código de PREOC> = 1, entre quienes no marcaron AP4_2_99; once temas; piso ENVIPE "
                                 "2024 (spec MC2 §1; PROSPECTIVA; unidad PERSONA)"},
                  {"nombre": "MC2-INSEGURO-<espacio>",
                   "definicion": "AP4_4_<código de AP44> = 2 frente a 1; cinco espacios; piso ENVIPE 2024 (spec MC2 §1; "
                                 "PROSPECTIVA; unidad PERSONA)"},
                  {"nombre": "MC2-DUPLICADA-EDO-INSEGURO-2025-<segmento>",
                   "definicion": "AP4_3_3 = 2 frente a 1; mismo estimando que ESTADO-INSEGURO de PERCEPCION, que la puntúa; "
                                 "R sin puntuar (unidad PERSONA)"},
                  {"nombre": "MC2-RETROSPECTIVA-DEL-<indicador>-<segmento>",
                   "definicion": "DENUNCIA (BP1_20 = 1 o BP1_21 = 1), CIFRA-NEGRA, CARPETA-DADA-DENUNCIA (BP1_24 = 1), "
                                 "EXT-TELEFONICA (BP1_5A_2, BPCOD = 9) sobre tmod_vic; RETROSPECTIVA, R sin puntuar "
                                 "(unidad DELITO)"}],
}


def sellados(inputs=None):
    S = E.modulo("m_envipe_percepcion_sellado", E.bytes_repo(inputs, *SELLADO))
    R = E.modulo("receta_pisos_salud_envipe", E.bytes_repo(inputs, *RECETA))
    M = E.modulo("motor_pisos_confianza_envipe", E.bytes_repo(inputs, *MOTOR))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return S, R, M, piso


def sellados_mc2(inputs=None):
    S2 = E.modulo("m_mc2_envipe2025_sellado", E.bytes_repo(inputs, *SELLADO_MC2))
    piso2 = E.json_repo(inputs, *PISO_MC2)["resultados"]
    return S2, piso2


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(S):
    out = []
    for c in S.CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(S.EJES_CATS.items()):
            out += [(c, eje, cat) for cat in cats]
    return out


# ── MC2: rejilla leída del árbitro (su resultados.json), no tecleada ────────────────────────────────────────
def bases_mc2(S2, piso2):
    """Toda celda de MC2 con `-P` sellado (sin DIAG), como id sin `PFX-`."""
    pfx = S2.PFX + "-"
    return sorted(k[len(pfx):-2] for k in piso2
                  if k.startswith(pfx) and k.endswith("-P") and not k[len(pfx):].startswith("DIAG-"))


def clase_mc2(b):
    if b.startswith(APARTA_MC2):
        return "APARTADA"
    if b.startswith(RETRO_MC2):
        return "RETROSPECTIVA"
    if b.startswith(DUP_MC2):
        return "DUPLICADA"
    return "PROSPECTIVA"


def celdas_mc2(S2, piso2):
    """[(base, clase)] de las celdas que entran (las APARTADAS no emiten nada)."""
    return [(b, clase_mc2(b)) for b in bases_mc2(S2, piso2) if clase_mc2(b) != "APARTADA"]


def _cid_mc2(b, clase):
    return f"MC2-{b}" if clase == "PROSPECTIVA" else f"MC2-{clase}-{b}"


def gemelo_percepcion(b):
    """Celda de PERCEPCION con el mismo estimando que la DUPLICADA `b` (EDO-INSEGURO-2025-<segmento>)."""
    seg = b[len(DUP_MC2):]
    eje, cat = ("EDAD", seg[len("EDAD-"):]) if seg.startswith("EDAD-") else GEMELO_SEG[seg]
    return _cid("ESTADO-INSEGURO", eje, cat)


def columnas_mc2(S2, b):
    """(tabla 2026, columnas del desenlace) que la recodificación sellada usa para la celda `b`; una ausente en
    el catálogo 2026 hace la celda NO-ESTIMABLE (los ejes ausentes vacían la máscara por sí solos)."""
    if b.startswith(("DEL-CIFRA-NEGRA-", "DEL-CARPETA-DADA-DENUNCIA-")):
        return TABLA_DEL_26, ("BP1_20", "BP1_21", "BP1_24")
    if b.startswith("DEL-DENUNCIA-"):
        return TABLA_DEL_26, ("BP1_20", "BP1_21")
    if b.startswith("DEL-EXT-TELEFONICA-"):
        return TABLA_DEL_26, ("BPCOD", "BP1_5A_2")
    if b.startswith("EDO-INSEGURO-"):
        return TABLA_PER_26, ("AP4_3_3",)
    if b.startswith("DEJO-SALIR-NOCHE-"):
        return TABLA_PER_26, ("AP4_10_01",)
    fam, k = b.split("-")[:2]
    if fam == "PREOC":
        return TABLA_PER_26, (f"AP4_2_{S2.PREOC[k]}", "AP4_2_99")
    if fam == "INSEGURO":
        return TABLA_PER_26, (S2.AP44[k],)
    raise G.ParoDeGuardia(f"celda MC2 sin columnas declaradas: {b}")


def cols_mc2(S2):
    return {TABLA_DEL_26: list(S2.COLS_DEL), TABLA_PER_26: list(dict.fromkeys(S2.COLS_PER24 + S2.COLS_PER25))}


def esquema_resultados():
    S, _R, _M, _p = sellados()
    S2, piso2 = sellados_mc2()
    return E.esquema(P, [_cid(*k) for k in celdas_de(S)] + [_cid_mc2(b, c) for b, c in celdas_mc2(S2, piso2)])


def lee_payload_reservado(S, R, S2, ruta):
    """Única lectura de la ola reservada (la auditoría AST lo exige). PERCEPCION: (tper_vic1, tsdem) con sus
    columnas que existan, por la receta de pisos. MC2: (tmod_vic, tper_vic1) con su lector sellado `_lee`, sólo
    las columnas de su medidor que existan. Estructura ausente es PARO; desenlace o eje ausente queda vacío
    (-> NO-ESTIMABLE). La cabecera se lee de los primeros 64 KiB con fin de línea normalizado (\\r solo, como
    advierte el medidor de MC2)."""
    import zipfile

    miembros, cabeceras = {}, {}
    with zipfile.ZipFile(ruta) as z:
        nombres = [n for n in z.namelist() if not n.startswith("__MACOSX")]
        for suf in (SUF_PER, SUF_SDEM, SUF_DEL):
            cands = [n for n in nombres if n.lower().endswith(suf)]
            if len(cands) != 1:
                raise G.ParoDeGuardia(f"*{suf}: {len(cands)} miembros ({cands})")
            with z.open(cands[0]) as fh:
                crudo = fh.read(1 << 16)
            try:
                cab = crudo.decode("utf-8")
            except UnicodeDecodeError:
                cab = crudo.decode("latin-1")
            primera = cab.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n").split("\n", 1)[0]
            miembros[suf] = cands[0]
            cabeceras[suf] = {c.strip().strip('"') for c in primera.split(",")}
    tablas = []
    for suf, cols, estructura in ((SUF_PER, S.COLS_PER, ESTRUCTURA_PER), (SUF_SDEM, S.COLS_SDEM, ESTRUCTURA_SDEM)):
        reales = {c.upper() for c in cabeceras[suf]}
        faltan = [c for c in estructura if c not in reales]
        if faltan:
            raise G.ParoDeGuardia(f"columnas de estructura ausentes en {miembros[suf]}: {faltan}")
        f = R.lee_csv_zip(ruta, [c for c in cols if c in reales], miembro=miembros[suf])
        for c in cols:
            if c.lower() not in f.columns:
                f[c.lower()] = ""
        tablas.append(f)
    mc2, ausentes = {}, set()
    for tabla, suf in ((TABLA_DEL_26, SUF_DEL), (TABLA_PER_26, SUF_PER)):
        reales = cabeceras[suf]
        faltan = [c for c in ESTRUCTURA_MC2[tabla] if c not in reales]
        if faltan:
            raise G.ParoDeGuardia(f"columnas de estructura de MC2 ausentes en {miembros[suf]}: {faltan}")
        cols = cols_mc2(S2)[tabla]
        try:
            d = S2._lee(ruta, tabla, [c for c in cols if c in reales])
        except S2.ReservaRota as e:
            raise G.ParoDeGuardia(f"lector sellado de MC2: {e}") from e
        for c in cols:
            if c not in d.columns:
                d[c] = ""
                ausentes.add((tabla, c))
        mc2[tabla] = d
    return {"per": tablas[0], "sdem": tablas[1], "mc2": mc2, "ausentes_mc2": ausentes}


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


def mide_r_mc2(S2, piso2, mc2, ausentes):
    """{base: p}. La recodificación es la de MC2 (frame_del/frame_per/celdas_*), servida con las tablas 2026 ya
    leídas por `lee_payload_reservado` en la ranura de la última ola de cada estimando; el universo es el de su
    `_estima` (peso finito > 0, estrato y UPM no vacíos). Una llamada al agregador por celda, con UNA variable
    de agrupación: la máscara del segmento."""
    servidas = {vieja: mc2[nueva] for vieja, nueva in RANURAS_MC2.items()}
    S2._lee = lambda _ruta, tabla, cols: servidas[tabla][list(cols)].copy()
    quiero = {b for b, _c in celdas_mc2(S2, piso2)}
    d_del, _diag = S2.frame_del("ENVIPE-2026")
    c_del, _f = S2.celdas_del(d_del)
    d_per, _diag = S2.frame_per("ENVIPE-2026", "ENVIPE-2026")
    c_per, _f = S2.celdas_per(d_per)
    out = {}
    for d, celdas in ((d_del, c_del), (d_per, c_per)):
        ok = d["_w"].notna() & (d["_w"] > 0) & d["_est"].ne("") & d["_upm"].ne("")
        w = d["_w"].where(ok).to_numpy(dtype=float)
        for rid, m, y in celdas:
            b = rid[len(S2.PFX) + 1:]
            if b not in quiero:
                continue
            tabla, cols = columnas_mc2(S2, b)
            if any((tabla, c) in ausentes for c in cols):
                out[b] = None
                continue
            g = np.where(m.reindex(d.index, fill_value=False).to_numpy(dtype=bool), b, None).astype(object)
            out[b] = G.proporcion_por_grupo(y.reindex(d.index).to_numpy(dtype=float), w, g).get(b, {}).get("p")
    return out


def filas(S, M, r, piso):
    return [{"id": _cid(c, eje, cat), "conglomerado": c,
             "lo": piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, "IC-LO")),
             "hi": piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, "IC-HI")),
             "punto": piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, "P")),
             "r": r.get((c, eje, cat))} for c, eje, cat in celdas_de(S)]


def filas_mc2(S2, r2, piso2):
    """Sólo PROSPECTIVA puntúa (lo/hi = IC95 sellado de su última ola); RETROSPECTIVA y DUPLICADA emiten R con
    lo/hi None. Punto None en unidad DELITO (UNIDAD_MAE)."""
    out = []
    for b, clase in celdas_mc2(S2, piso2):
        base = f"{S2.PFX}-{b}"
        puntua = clase == "PROSPECTIVA"
        unidad = "DELITO" if b.startswith(RETRO_MC2) else "PERSONA"
        out.append({"id": _cid_mc2(b, clase), "conglomerado": CALC_MC2,
                    "lo": piso2.get(f"{base}-IC95-INF") if puntua else None,
                    "hi": piso2.get(f"{base}-IC95-SUP") if puntua else None,
                    "punto": piso2.get(f"{base}-P") if unidad == UNIDAD_MAE else None,
                    "r": r2.get(b)})
    return out


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAYLOAD} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    S, R, M, piso = sellados(inputs)
    S2, piso2 = sellados_mc2(inputs)
    leidas = lee_payload_reservado(S, R, S2, inputs[PAYLOAD]["ruta_absoluta"])
    r = mide_r(S, M, leidas["per"], leidas["sdem"])
    r2 = mide_r_mc2(S2, piso2, leidas["mc2"], leidas["ausentes_mc2"])
    return E.salida(P, filas(S, M, r, piso) + filas_mc2(S2, r2, piso2))
