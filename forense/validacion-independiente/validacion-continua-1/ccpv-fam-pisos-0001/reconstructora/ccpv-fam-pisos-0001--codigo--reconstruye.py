"""Reconstrucción CALC-CCPV-FAM-PISOS-0001 desde paquete/docs/spec-humana.md.

Uso (desde el directorio de trabajo): python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json y salida/diagnostico.json.
Variable opcional CCPV_CACHE=<ruta.pkl>: caché de las columnas autorizadas ya leídas.
"""
import csv
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from carga import carga  # noqa: E402

ESQUEMA = os.path.join("paquete", "esquema-identidades.tsv")
SALIDA = "salida"
IDENTIDAD = {"paquete": "ccpv-fam-pisos-0001", "version_entrada": "validacion-continua-1",
             "sha256_entrada": "e912ced96a72ada8a3cafd4fdf7e17775071ae178c460cd36b97bb26f8496d01"}
SEMILLA = 20260925
B = 1000
TIPOHOG_OK = [1, 2, 3, 4, 5, 6]
PARENT_CAT = [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]


def r(x):
    return repr(float(x))


# --------------------------------------------------------------------------- hogares
def construye_hogares(viv, per, diag):
    n0 = len(viv)
    filtro = (viv.factor > 0) & (viv.estrato.astype(str) != "") & (viv.upm.astype(str) != "")
    diag["filtro_muestra"]["HOGAR"] = {"filas_viviendas": int(n0), "excluidas_factor_estrato_upm": int((~filtro).sum()),
                                       "filas_validas": int(filtro.sum())}
    H = viv[filtro].copy()
    H["ent"] = H.ent.astype(str)
    H = H.reset_index(drop=True)
    H["hid"] = np.arange(len(H))

    # composición: todas las filas de PERSONAS de la vivienda (ver decisiones D1)
    P = per[["ent", "id_viv", "sexo", "edad", "parent", "nivacad"]].copy()
    P["ent"] = P.ent.astype(str)
    idx = pd.MultiIndex.from_frame(H[["ent", "id_viv"]])
    P["hid"] = idx.get_indexer(pd.MultiIndex.from_frame(P[["ent", "id_viv"]]))
    diag["filtro_muestra"]["personas_sin_vivienda_valida"] = int((P.hid < 0).sum())
    P = P[P.hid >= 0]
    edad = P.edad
    e_conocida = edad.notna() & (edad != 999)
    par = P.parent
    par_ok = par.isin([1, 2, 3, 4, 5, 6, 7, 8, 9])
    f = pd.DataFrame({
        "hid": P.hid.values,
        "n": 1,
        "a60": (e_conocida & (edad >= 60)).values,
        "m18": (e_conocida & (edad < 18)).values,
        "e999": (~e_conocida).values,
        "p4": (par == 4).values,
        "p67": par.isin([6, 7]).values,
        "p3": (par == 3).values,
        "pdesc": (~par_ok).values,
        "jefe": (par == 1).values,
    })
    g = f.groupby("hid").sum()
    g = g.reindex(H.hid, fill_value=0)
    for c in ["n", "a60", "m18", "e999", "p4", "p67", "p3", "pdesc", "jefe"]:
        H["c_" + c] = g[c].values
    # diagnósticos de catálogo (personas)
    diag["catalogo_personas"] = {
        "sexo_fuera_1_3": int((~P.sexo.isin([1, 3])).sum()),
        "parent_fuera_1_9_99": int((~P.parent.isin(PARENT_CAT)).sum()),
        "parent_99": int((P.parent == 99).sum()),
        "edad_999": int((P.edad == 999).sum()),
    }
    # jefe
    J = P[P.parent == 1]
    unico = H.c_jefe == 1
    diag["jefe"] = {"G-VIV-SIN-JEFE": int((H.c_jefe == 0).sum()),
                    "G-VIV-JEFE-MULTIPLE": int((H.c_jefe > 1).sum()),
                    "viviendas_jefe_unico": int(unico.sum())}
    Ju = J[J.hid.isin(H.hid[unico])].set_index("hid")
    H["j_sexo"] = Ju.sexo.reindex(H.hid).values
    H["j_edad"] = Ju.edad.reindex(H.hid).values
    H["j_nivacad"] = Ju.nivacad.reindex(H.hid).values
    return H


def conductas_hogar(H):
    """Devuelve dict conducta -> (y, universo_conducta, etiqueta_exclusion)."""
    th = H.tipohog
    th_ok = th.isin(TIPOHOG_OK)
    todas_edades = H.c_e999 == 0
    con60 = H.c_a60 > 0
    con18 = H.c_m18 > 0
    ambos = con60 & con18
    tresg = (H.c_p4 > 0) | ((H.c_p67 > 0) & (H.c_p3 > 0))
    par_todos = H.c_pdesc == 0
    np_ok = H.numpers.between(1, 60)
    js = H.j_sexo
    c = {}
    for nom, k in [("hog-nuclear", 1), ("hog-ampliado", 2), ("hog-compuesto", 3),
                   ("hog-unipersonal", 5), ("hog-corresidentes", 6)]:
        c[nom] = ((th == k).astype(float), th_ok, pd.Series(True, index=H.index), "")
    c["hog-con-60mas"] = (con60.astype(float), th_ok, con60 | todas_edades, "edad_999_sin_60mas")
    c["hog-con-menor-18"] = (con18.astype(float), th_ok, con18 | todas_edades, "edad_999_sin_menor18")
    c["hog-60mas-y-menor-18"] = (ambos.astype(float), th_ok, ambos | todas_edades, "edad_999_sin_ambos")
    c["hog-tres-generaciones"] = (tresg.astype(float), th_ok, tresg | par_todos, "parent_desconocido_sin_condicion")
    c["hog-jefa-mujer"] = ((js == 3).astype(float), th_ok, (H.c_jefe == 1) & js.isin([1, 3]),
                           "sin_jefe_unico_o_sexo_jefe_fuera_catalogo")
    c["hog-tamano-medio"] = (H.numpers.where(np_ok, 0.0).astype(float), th_ok, np_ok, "numpers_fuera_1_60")
    c["am-hog-nuclear-o-ampliado"] = (th.isin([1, 2]).astype(float), th_ok, con60, "sin_residente_60mas")
    c["am-hog-unipersonal"] = ((th == 5).astype(float), th_ok, con60, "sin_residente_60mas")
    return c


def ejes_hogar(H):
    unico = H.c_jefe == 1
    je, jn, js = H.j_edad, H.j_nivacad, H.j_sexo
    je_ok = unico & je.notna() & (je != 999)
    e = {("TOTAL", "TODOS"): (pd.Series(True, index=H.index), pd.Series(True, index=H.index), "")}
    e[("SEXO-JEFE", "HOMBRE")] = (unico & js.isin([1, 3]), js == 1, "sin_jefe_unico_o_sexo_fuera_catalogo")
    e[("SEXO-JEFE", "MUJER")] = (unico & js.isin([1, 3]), js == 3, "sin_jefe_unico_o_sexo_fuera_catalogo")
    e[("EDAD-JEFE", "HASTA-29")] = (je_ok, je <= 29, "sin_jefe_unico_o_edad_jefe_999")
    e[("EDAD-JEFE", "30-44")] = (je_ok, je.between(30, 44), "sin_jefe_unico_o_edad_jefe_999")
    e[("EDAD-JEFE", "45-59")] = (je_ok, je.between(45, 59), "sin_jefe_unico_o_edad_jefe_999")
    e[("EDAD-JEFE", "60-MAS")] = (je_ok, je >= 60, "sin_jefe_unico_o_edad_jefe_999")
    bas, med, sup = [0, 1, 2, 3, 5, 6, 7], [4, 8], [9, 10, 11, 12]
    jn_ok = unico & jn.isin(bas + med + sup)
    e[("ESCOLARIDAD-JEFE", "BASICA-O-MENOS")] = (jn_ok, jn.isin(bas), "sin_jefe_unico_o_nivacad_jefe_99_o_vacio")
    e[("ESCOLARIDAD-JEFE", "MEDIA-SUPERIOR")] = (jn_ok, jn.isin(med), "sin_jefe_unico_o_nivacad_jefe_99_o_vacio")
    e[("ESCOLARIDAD-JEFE", "SUPERIOR")] = (jn_ok, jn.isin(sup), "sin_jefe_unico_o_nivacad_jefe_99_o_vacio")
    tl = H.tam_loc
    for seg, k in [("MENOS-2500", 1), ("2500-14999", 2), ("15MIL-99MIL", 3), ("100MIL-MAS", 4)]:
        e[("TLOC", seg)] = (tl.isin([1, 2, 3, 4]), tl == k, "tam_loc_fuera_1_4")
    for i in range(1, 33):
        ee = "%02d" % i
        e[("ENT", ee)] = (pd.Series(True, index=H.index), H.ent == ee, "")
    return e


# --------------------------------------------------------------------------- personas 60+
def construye_personas(per, H, diag):
    n0 = len(per)
    filtro = (per.factor > 0) & (per.estrato.astype(str) != "") & (per.upm.astype(str) != "")
    P = per[filtro].copy()
    P["ent"] = P.ent.astype(str)
    idx = pd.MultiIndex.from_frame(H[["ent", "id_viv"]])
    hid = idx.get_indexer(pd.MultiIndex.from_frame(P[["ent", "id_viv"]]))
    P["tipohog"] = np.where(hid >= 0, H.tipohog.values[np.maximum(hid, 0)], np.nan)
    diag["filtro_muestra"]["PERSONA"] = {"filas_personas": int(n0),
                                         "excluidas_factor_estrato_upm": int((~filtro).sum()),
                                         "filas_validas": int(filtro.sum()),
                                         "sin_hogar_valido": int((hid < 0).sum())}
    return P.reset_index(drop=True)


def piezas_personas(P):
    ed = P.edad
    e60 = ed.notna() & (ed != 999) & (ed >= 60)
    th_ok = P.tipohog.isin(TIPOHOG_OK)
    y = (P.tipohog == 5).astype(float)
    ejes = {("TOTAL", "TODOS"): (pd.Series(True, index=P.index), pd.Series(True, index=P.index), "")}
    ejes[("SEXO", "HOMBRE")] = (P.sexo.isin([1, 3]), P.sexo == 1, "sexo_fuera_catalogo")
    ejes[("SEXO", "MUJER")] = (P.sexo.isin([1, 3]), P.sexo == 3, "sexo_fuera_catalogo")
    ejes[("EDAD", "60-69")] = (pd.Series(True, index=P.index), ed.between(60, 69), "")
    ejes[("EDAD", "70-79")] = (pd.Series(True, index=P.index), ed.between(70, 79), "")
    ejes[("EDAD", "80-MAS")] = (pd.Series(True, index=P.index), (ed >= 80) & (ed != 999), "")
    tl = P.tam_loc
    for seg, k in [("MENOS-2500", 1), ("2500-14999", 2), ("15MIL-99MIL", 3), ("100MIL-MAS", 4)]:
        ejes[("TLOC", seg)] = (tl.isin([1, 2, 3, 4]), tl == k, "tam_loc_fuera_1_4")
    for i in range(1, 33):
        ee = "%02d" % i
        ejes[("ENT", ee)] = (pd.Series(True, index=P.index), P.ent == ee, "")
    return e60, th_ok, y, ejes


# --------------------------------------------------------------------------- diseño
def indices_diseno(H, P):
    s_h = H.ent + "|" + H.estrato.astype(str)
    u_h = s_h + "|" + H.upm.astype(str)
    s_p = P.ent + "|" + P.estrato.astype(str)
    u_p = s_p + "|" + P.upm.astype(str)
    tab = pd.DataFrame({"s": pd.concat([s_h, s_p]).values, "u": pd.concat([u_h, u_p]).values})
    tab = tab.drop_duplicates().sort_values(["s", "u"]).reset_index(drop=True)
    if tab.u.duplicated().any():
        raise ValueError("UPM en más de un estrato")
    upm_pos = pd.Index(tab.u)
    return tab, upm_pos.get_indexer(u_h), upm_pos.get_indexer(u_p)


def multiplicadores(tab):
    """Matriz B x U (int16) de conteos de selección, UPM dentro de estrato.

    Estratos en orden lexicográfico de 'ent|estrato', UPM en orden de 'ent|estrato|upm'.
    Estrato con una sola UPM: certeza (multiplicador 1 en todas las réplicas).
    Réplica b: para cada UPM del bloque de estratos con n_h>=2 se sortea
    floor(U(0,1) * n_h) -> índice de UPM elegida dentro de su estrato (n_h extracciones con
    reemplazo); multiplicador = número de veces elegida.
    """
    U = len(tab)
    sidx = pd.factorize(tab.s, sort=True)[0]
    nh = np.bincount(sidx)
    n_de_upm = nh[sidx]
    inicio = np.concatenate([[0], np.cumsum(nh)[:-1]])[sidx]
    multi = np.where(n_de_upm >= 2)[0]
    M = np.ones((B, U), dtype=np.int16)
    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    nm = n_de_upm[multi].astype(np.float64)
    ini = inicio[multi]
    for b in range(B):
        u = rng.random(len(multi))
        eleg = ini + np.minimum(np.floor(u * nm).astype(np.int64), n_de_upm[multi] - 1)
        cnt = np.bincount(eleg, minlength=U)
        fila = M[b]
        fila[multi] = cnt[multi]
    return M, {"estratos": int(len(nh)), "upms": int(U), "estratos_upm_unica_certeza": int((nh == 1).sum()),
               "upms_en_estratos_certeza": int((n_de_upm == 1).sum())}


def main():
    diag = {"filtro_muestra": {}, "llaves": {}, "decisiones": DECISIONES}
    cache = os.environ.get("CCPV_CACHE")
    viv, per, rutas, varlists = carga(cache=cache)
    diag["archivos_microdato"] = rutas
    faltan = {}
    for p, vl in varlists.items():
        req = ["ent", "id_viv", "tipohog", "numpers", "factor", "estrato", "upm", "tam_loc"] if "/viv_" in p \
            else ["ent", "id_viv", "sexo", "edad", "parent", "nivacad", "factor", "estrato", "upm", "tam_loc"]
        m = [c for c in req if c not in vl]
        if m:
            faltan[p] = m
    diag["columnas_faltantes"] = faltan

    H = construye_hogares(viv, per, diag)
    P = construye_personas(per, H, diag)
    del viv, per
    cond = conductas_hogar(H)
    ejes = ejes_hogar(H)
    e60, pth_ok, py, pejes = piezas_personas(P)

    tab, uh, up = indices_diseno(H, P)
    U = len(tab)
    wH = H.factor.values.astype(np.float64)
    wP = P.factor.values.astype(np.float64)

    esquema = list(csv.DictReader(open(ESQUEMA, encoding="utf-8"), delimiter="\t"))
    filas, T_cols, pendientes = [], [], []
    for row in esquema:
        llave, unidad = row["llave"], row["unidad"]
        conducta, eje, seg = row["conducta"], row["eje"], row["segmento"]
        d = {"conducta": conducta, "eje": eje, "segmento": seg, "ola": row["ola"]}
        fila = {"llave": llave, "unidad": unidad}
        if row["ola"] != "2010":
            fila.update(estado="NO-RECALCULABLE-DESDE-SPEC", motivo="La spec solo mide la ola 2010.")
            filas.append(fila); diag["llaves"][llave] = d; continue
        if conducta == "per60-vive-solo":
            if (eje, seg) not in pejes:
                fila.update(estado="NO-RECALCULABLE-DESDE-SPEC", motivo="Eje/segmento no definido en la spec para personas 60+.")
                filas.append(fila); diag["llaves"][llave] = d; continue
            eje_ok, dom, lab = pejes[(eje, seg)]
            base = e60
            d["n_personas_60mas_filtradas"] = int(base.sum())
            m1 = base & eje_ok
            d["excl_eje:" + (lab or "ninguna")] = int((base & ~eje_ok).sum())
            m2 = m1 & dom
            d["n_dominio"] = int(m2.sum())
            m3 = m2 & pth_ok
            d["excl_tipohog_fuera_1_6_o_sin_hogar"] = int((m2 & ~pth_ok).sum())
            mask = m3.values
            y = py.values
            w, ui = wP, up
            d["n_valido"] = int(mask.sum())
            d["total_expandido_personas_60mas_vive_solo"] = r((w * y * mask).sum())
            d["total_expandido_universo"] = r((w * mask).sum())
        else:
            if conducta not in cond or (eje, seg) not in ejes:
                fila.update(estado="NO-RECALCULABLE-DESDE-SPEC", motivo="Conducta o eje/segmento no definido en la spec.")
                filas.append(fila); diag["llaves"][llave] = d; continue
            yv, th_ok, u_ok, lab_c = cond[conducta]
            eje_ok, dom, lab_e = ejes[(eje, seg)]
            n0 = len(H)
            d["n_hogares_filtrados"] = n0
            m1 = eje_ok
            d["excl_eje:" + (lab_e or "ninguna")] = int((~eje_ok).sum())
            m2 = m1 & dom
            d["n_dominio"] = int(m2.sum())
            m3 = m2 & th_ok
            d["excl_tipohog_fuera_1_6"] = int((m2 & ~th_ok).sum())
            m4 = m3 & u_ok
            d["excl_universo_conducta:" + (lab_c or "ninguna")] = int((m3 & ~u_ok).sum())
            mask = m4.values
            y = yv.values
            w, ui = wH, uh
            d["n_valido"] = int(mask.sum())
        diag["llaves"][llave] = d
        den = float((w * mask).sum())
        if d["n_valido"] == 0 or den <= 0:
            fila.update(estado="DENOMINADOR-CERO", motivo="Dominio observado sin unidades válidas (n=%d) bajo la spec." % d["n_valido"])
            filas.append(fila); continue
        num = float((w * y * mask).sum())
        fila.update(estado="RECONSTRUIDO", punto=r(num / den))
        tn = np.bincount(ui[mask], weights=(w * y)[mask], minlength=U)
        td = np.bincount(ui[mask], weights=w[mask], minlength=U)
        pendientes.append((len(filas), len(T_cols)))
        T_cols.append(tn); T_cols.append(td)
        filas.append(fila)

    # bootstrap común a todas las llaves
    M, info = multiplicadores(tab)
    diag["diseno_bootstrap"] = info
    T = np.column_stack(T_cols)
    del T_cols
    R = np.empty((B, T.shape[1]))
    paso = 50
    for i in range(0, B, paso):
        R[i:i + paso] = M[i:i + paso].astype(np.float64) @ T
    for fi, c in pendientes:
        rn, rd = R[:, c], R[:, c + 1]
        fila = filas[fi]
        dd = diag["llaves"][fila["llave"]]
        ceros = int((rd <= 0).sum())
        dd["replicas_denominador_cero"] = ceros
        if ceros:
            fila.update(estado_ic="NO-IDENTIFICADA",
                        motivo_ic="%d de %d réplicas bootstrap con denominador cero; la spec no fija su tratamiento." % (ceros, B))
            continue
        rep = rn / rd
        lo, hi = np.percentile(rep, [2.5, 97.5])
        fila.update(estado_ic="CALCULADO", ic95_inf=r(lo), ic95_sup=r(hi))

    # orden de campos
    orden = ["llave", "unidad", "estado", "punto", "estado_ic", "ic95_inf", "ic95_sup", "motivo", "motivo_ic"]
    filas = [{k: f[k] for k in orden if k in f} for f in filas]
    doc = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    with open(os.path.join(SALIDA, "resultado.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")
    cuenta = {}
    for f_ in filas:
        k = f_["estado"] + "/" + f_.get("estado_ic", "-")
        cuenta[k] = cuenta.get(k, 0) + 1
    diag["resumen_estados"] = cuenta
    with open(os.path.join(SALIDA, "diagnostico.json"), "w", encoding="utf-8") as f:
        json.dump(diag, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(json.dumps(cuenta, ensure_ascii=False))


DECISIONES = [
    {"id": "D1", "frase": "PERSONA (sólo PER60-*): filas de PERSONAS con el mismo filtro y su propio `factor`.",
     "decision": "La composición del hogar (edades, parentescos, jefe) se construye con todas las filas de PERSONAS de la vivienda; el filtro factor/estrato/upm de personas se aplica solo a la unidad PER60. En los datos ninguna fila de personas falla ese filtro, así que no cambia nada."},
    {"id": "D2", "frase": "HOG-CON-60MAS (≥1 residente de 60+; universo: hay uno, o todas las edades conocidas) · HOG-CON-MENOR-18 (ídem con <18) · HOG-60MAS-Y-MENOR-18 (ambos; ...)",
     "decision": "Para HOG-60MAS-Y-MENOR-18 el universo es: se observan ambos, o todas las edades son conocidas (edad≠999). 60+ = edad 60–998; <18 = edad 0–17."},
    {"id": "D3", "frase": "HOG-TRES-GENERACIONES (nieta(o) de la jefa(e), o madre/padre/suegra(o) junto con hija(o); universo: parentesco conocido de todos, o la condición se cumple)",
     "decision": "Condición: algún parent=4, o (algún parent∈{6,7} y algún parent=3). Parentesco desconocido = parent 99 o fuera de 1–9."},
    {"id": "D4", "frase": "HOG-JEFA-MUJER (sexo del jefe = 3)",
     "decision": "Universo: hogares TIPOHOG 1–6 con jefe único y sexo del jefe en {1,3}. En el eje SEXO-JEFE el resultado es 0/1 por construcción y se reporta igual."},
    {"id": "D5", "frase": "HOG-TAMANO-MEDIO (media de `numpers`, 1–60)",
     "decision": "Razón ponderada Σw·numpers/Σw sobre hogares TIPOHOG 1–6 con numpers entre 1 y 60; otros valores excluidos del universo."},
    {"id": "D6", "frase": "AM-HOG-NUCLEAR-O-AMPLIADO y AM-HOG-UNIPERSONAL (universo: hogares con 60+ y `TIPOHOG` 1–6)",
     "decision": "Hogar con 60+ = al menos un residente con edad 60–998. Numerador TIPOHOG∈{1,2} o TIPOHOG=5."},
    {"id": "D7", "frase": "Hogares (universo: `TIPOHOG` 1–6 salvo donde se dice)",
     "decision": "El universo TIPOHOG 1–6 se aplica a todas las conductas de hogar, incluidas HOG-JEFA-MUJER y HOG-TAMANO-MEDIO; TIPOHOG 4 queda en el denominador de las proporciones por tipo."},
    {"id": "D8", "frase": "Jefe = la única persona con `parent = 1` de la vivienda; vivienda con 0 o >1 jefes → fuera de los ejes del jefe",
     "decision": "Ejes del jefe: jefe único y valor válido del atributo (edad≠999; NIVACAD en 0–12; sexo en {1,3}); fuera de ello el hogar sale del eje. Los ejes TOTAL, TLOC y ENT no requieren jefe."},
    {"id": "D9", "frase": "EDAD-JEFE (≤29, 30–44, 45–59, 60+) · ... Persona 60+: ... EDAD (60–69, 70–79, 80+)",
     "decision": "Cortes en años cumplidos enteros; 60+ y 80+ excluyen el código 999."},
    {"id": "D10", "frase": "PER60-VIVE-SOLO (persona de 60+ en hogar `TIPOHOG` = 5; universo: 60+ con `TIPOHOG` 1–6) y su total expandido (Σ factor, sin IC)",
     "decision": "TIPOHOG de la persona = el de su vivienda (ent+id_viv) en VIVIENDAS filtradas; ejes SEXO/TLOC/ENT de la persona (sus propias columnas). El total expandido no tiene llave en el esquema: se reporta solo en diagnostico.json."},
    {"id": "D11", "frase": "bootstrap de UPM dentro de estrato (certeza para UPM única, `PCG64(20260925)`, 1 000 réplicas, percentiles 2.5/97.5, contrato conservador)",
     "decision": "Bootstrap ingenuo: en cada estrato con n_h≥2 se extraen n_h UPM con reemplazo y el peso se multiplica por el número de veces elegida (sin reescalado Rao-Wu); estrato con UPM única: multiplicador 1 (certeza). Un solo generador np.random.Generator(PCG64(20260925)); réplica a réplica, un uniforme por UPM de estratos n_h≥2 en orden lexicográfico 'ent|estrato|upm', índice = floor(u·n_h). Las mismas 1000 réplicas sirven a todas las llaves (hogar y persona comparten UPM). Percentiles con np.percentile (interpolación lineal)."},
    {"id": "D12", "frase": "contrato conservador",
     "decision": "Si alguna réplica tiene denominador cero, no se descartan réplicas: el IC se declara NO-IDENTIFICADA con motivo_ic."},
    {"id": "D13", "frase": "estrato = `ent|estrato`, UPM = `ent|estrato|upm`",
     "decision": "Claves de texto con espacios recortados; el diseño de personas se toma de sus propias columnas (coinciden con las de su vivienda en todos los casos)."},
    {"id": "D14", "frase": ".dta se lee con pandas.read_stata (encargo)",
     "decision": "viv_15.dta y per_15.dta están en formato Stata 110, que pandas no lee; se leen con pyreadstat (paquete/lib) limitando usecols a las columnas autorizadas."},
    {"id": "D15", "frase": "Una ola abierta: **sin IC de persistencia**.",
     "decision": "No aplica a llaves transversales 2010; los IC reportados son los del bootstrap de diseño de cada razón."},
]

if __name__ == "__main__":
    main()
