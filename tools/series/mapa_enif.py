#!/usr/bin/env python3
"""Mapa de series ENIF -- DONDE-CAMBIO-EL-MEXICANO-1.

Genera forense/analisis/donde-cambio/mapa/enif.tsv siguiendo
forense/analisis/donde-cambio/mapa/ESQUEMA.md y
forense/prereg-caja/DONDE-CAMBIO-spec-v1_0.md SS1-2.

REGLA DURA DE CEGUERA (B-bis): este script NUNCA lee ni imprime los valores
numericos de las columnas 9 (punto), 10 (ic95_inf), 11 (ic95_sup) ni 24
(oferta_valor_ic) del catalogo. Solo verifica EXISTENCIA de llaves de RESULT
como claves de resultados.json (nunca sus valores).

Nota declarada: la columna 8 (unidad_escala) del catalogo incluye, en varias
filas ENIF, un sufijo "-- releva RES-NNNN (esperado 0.NNNNNN)" que es un
VALOR numerico de punto. Este script LEE la columna 8 solo para clasificar si
la unidad es una proporcion (texto, no el numero), recorta ese sufijo antes de
cualquier uso, y NUNCA lo escribe en la salida. Ese valor no se repite en
ningun reporte de esta sesion.

Lee TSV con split('\t') (nunca el modulo csv). Escribe con '\n'.join,
conservando celdas vacias finales.
"""
import json
import os
import re
import sys
import unicodedata

REPO = "/home/pc0/mm-gen2-donde-cambio-el-mexicano-1"
CATALOGO = os.path.join(REPO, "canon/catalogo-del-mexicano-v1_0.tsv")
CORRIDA0 = os.path.join(REPO, "data/corrida0")
CREDITO_TXT = os.path.join(REPO, "data/credito-comparabilidad-texto-v1_1.tsv")
AHORRO_TXT = os.path.join(REPO, "data/ahorro-comparabilidad-texto-v1_0.tsv")
FINTECH_SPEC = os.path.join(REPO, "forense/prereg-caja/ENIF-FINTECH-SERIE-spec-v1_0.md")
FINTECH_CORR = os.path.join(REPO, "data/corrida0/enif-fintech-correspondencia-v1_0.tsv")
OUT = os.path.join(REPO, "forense/analisis/donde-cambio/mapa/enif.tsv")

EJES_SELLADOS_TAU2 = {"CUENTA", "EDAD", "ESCOLARIDAD", "FORMALIDAD", "LOCALIDAD", "SEXO"}

HEADER = ["serie_id", "instrumento", "dominio", "conducta", "conducta_texto", "eje",
          "segmento", "unidad", "ola", "calc", "result_p", "result_lo", "result_hi",
          "par_con_anterior", "cita_par", "marca_2020", "nota"]


def read_tsv(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    rows = [l.split("\t") for l in lines]
    header = rows[0]
    out = []
    for r in rows[1:]:
        # pad short rows (trailing empty cells split() would otherwise drop)
        if len(r) < len(header):
            r = r + [""] * (len(header) - len(r))
        out.append(dict(zip(header, r)))
    return out


def slugify(text):
    text = text.split(" -- ")[0].split(" -- releva")[0]
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_ = "".join(c for c in nfkd if not unicodedata.combining(c))
    ascii_ = ascii_.upper()
    ascii_ = re.sub(r"[^A-Z0-9]+", "-", ascii_)
    ascii_ = re.sub(r"-+", "-", ascii_).strip("-")
    return ascii_[:80] if ascii_ else "SIN-ROTULO"


def es_proporcion(unidad_escala_raw):
    """Clasifica por TEXTO (nunca por el numero) si la unidad es una
    proporcion en (0,1). Recorta el sufijo '-- releva RES-... (esperado X)'
    ANTES de mirar el texto -- ese sufijo es un valor, no se usa nunca."""
    texto = unidad_escala_raw.split(" -- releva")[0].split("--releva")[0].strip()
    texto_low = texto.lower()
    if "proporci" in texto_low:
        return True, texto
    if texto_low.startswith("p ponderado de") or texto_low.startswith("p (proporcion"):
        return True, texto
    if texto_low.startswith("complemento contado, 1-"):
        return True, texto
    return False, texto


def build_corrida0_index():
    """calc_dir_name -> set(llaves) presentes en resultados.json (solo llaves)."""
    idx = {}
    if not os.path.isdir(CORRIDA0):
        return idx
    for name in os.listdir(CORRIDA0):
        d = os.path.join(CORRIDA0, name)
        rjson = os.path.join(d, "resultados.json")
        if os.path.isfile(rjson):
            try:
                with open(rjson, encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue
            r = data.get("resultados", data) if isinstance(data, dict) else data
            if isinstance(r, dict):
                idx[name] = set(r.keys())
    return idx


def resolve_calc_keys(idx, calc_col):
    """Dado el texto de la columna calc (puede tener sufijo -vX_Y), busca el
    directorio en data/corrida0 que contenga sus llaves. Devuelve set() vacio
    si no existe -- eso hace que la ola se excluya (regla de reserva /
    verificacion por llave)."""
    if not calc_col:
        return set()
    if calc_col in idx:
        return idx[calc_col]
    # variante sin sufijo -vX_Y
    base = re.sub(r"-v\d+_\d+$", "", calc_col)
    if base in idx:
        return idx[base]
    # variante con -0001 si calc_col no lo trae
    for name in idx:
        if name.startswith(calc_col) or name.startswith(base):
            return idx[name]
    return set()


def parse_llave(llave):
    """Deriva (eje, segmento, conducta_toks) del propio llave de RESULT,
    escaneando tokens por los nombres de eje sellados (o NACIONAL)."""
    toks = llave[len("RESULT-"):].split("-") if llave.startswith("RESULT-") else llave.split("-")
    clean_toks = []
    for t in toks:
        t2 = re.sub(r"(19|20)\d\d$", "", t)
        if t2:
            clean_toks.append(t2)
    eje_idx = None
    for i, t in enumerate(clean_toks):
        if t in EJES_SELLADOS_TAU2:
            eje_idx = i
            break
    if eje_idx is None:
        for i, t in enumerate(clean_toks):
            if t == "NACIONAL":
                eje_idx = i
                break
    if eje_idx is not None:
        eje = clean_toks[eje_idx]
        resto = clean_toks[eje_idx + 1:]
        if resto and resto[-1] == "P":
            resto = resto[:-1]
        segmento = "-".join(resto) if resto else "TOTAL"
        conducta_toks = clean_toks[:eje_idx]
    else:
        eje, segmento = "NACIONAL", "TOTAL"
        conducta_toks = clean_toks[:-1] if clean_toks and clean_toks[-1] == "P" else clean_toks[:]
    return eje, segmento, conducta_toks


def ola_year(instrumento_ola):
    m = re.search(r"(20\d\d)", instrumento_ola)
    return m.group(1) if m else ""


PAR_ORDEN = {"NO-COMPARABLE": 3, "NO-DOCUMENTADO": 2, "CAMBIO-DOCUMENTADO": 1, "COMPARABLE": 0}


def peor(a, b):
    return a if PAR_ORDEN[a] >= PAR_ORDEN[b] else b


def veredicto_a_estado(v):
    if v in ("MISMO-INSTRUMENTO", "CAMBIO-MENOR"):
        return "COMPARABLE-ENDPOINT"
    if v == "CAMBIO-DE-INSTRUMENTO":
        return "CAMBIO-DOCUMENTADO"
    if v in ("NO-ESTIMABLE",):
        return "NO-COMPARABLE"
    return "NO-DOCUMENTADO"


def main():
    catalogo = read_tsv(CATALOGO)
    idx = build_corrida0_index()

    credito_rows = read_tsv(CREDITO_TXT)
    ahorro_rows = read_tsv(AHORRO_TXT)

    # credito: (kcode, ola) -> (veredicto, row_text_has_2020, cita_row)
    credito_map = {}
    for r in credito_rows:
        credito_map[(r["conducta"], r["ola"])] = r
    ahorro_map = {}
    for r in ahorro_rows:
        ahorro_map[(r["objeto"], r["ola"])] = r

    EJE_A_ECODE = {"CUENTA": "E-CTA", "EDAD": "E-EDA", "ESCOLARIDAD": "E-ESC",
                   "FORMALIDAD": "E-FOR", "LOCALIDAD": "E-LOC", "SEXO": "E-SEX"}

    series = {}  # serie_key -> {meta..., olas: {ola: row}}

    n_leidas = 0
    n_no_proporcion = 0
    n_sin_result_en_corrida0 = 0

    for row in catalogo:
        instrumento_ola = row.get("instrumento_ola", "")
        if not instrumento_ola.startswith("ENIF"):
            continue
        n_leidas += 1
        ola = ola_year(instrumento_ola)
        if ola not in ("2012", "2015", "2018", "2021", "2024"):
            continue
        result_p = row.get("result_punto", "").strip()
        if not result_p:
            continue
        es_prop, unidad_txt = es_proporcion(row.get("unidad_escala", ""))
        if not es_prop:
            n_no_proporcion += 1
        calc_col = row.get("calc", "").strip()
        keys = resolve_calc_keys(idx, calc_col)
        if result_p not in keys:
            n_sin_result_en_corrida0 += 1
            continue
        result_lo = row.get("result_inf", "").strip()
        result_hi = row.get("result_sup", "").strip()
        if result_lo and result_lo not in keys:
            result_lo = ""
        if result_hi and result_hi not in keys:
            result_hi = ""

        llave = row.get("llave", "")
        dominio = row.get("dominio", "")
        conducta_texto = row.get("conducta", "")

        # --- eje/segmento/conducta se derivan del LLAVE (no del texto
        # compartido de la columna "conducta", que colisiona entre K1..K8 y
        # entre canales de una misma conducta: ver nota en el reporte) ---
        eje, segmento, conducta_toks = parse_llave(llave)
        conducta_slug = "-".join(conducta_toks) if conducta_toks else slugify(conducta_texto)
        conducta_slug = conducta_slug[:80]
        serie_key = (conducta_slug, eje, segmento, unidad_txt)
        serie_id = "-".join(["ENIF", conducta_slug, eje, segmento])

        s = series.setdefault(serie_key, {
            "serie_id": serie_id, "dominio": dominio, "conducta": conducta_slug,
            "conducta_texto": conducta_texto, "eje": eje, "segmento": segmento,
            "unidad": unidad_txt, "llave_muestra": llave, "olas": {},
        })
        s["olas"][ola] = {
            "calc": calc_col, "result_p": result_p, "result_lo": result_lo,
            "result_hi": result_hi, "llave": llave,
            "row_text": "\t".join(row.values()),
            "fuera_de_escala": not es_prop,
        }

    # --- inyeccion directa: CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001/-0002,
    # nombrados explicitamente como fuente por el encargo. El catalogo (via el
    # bucle de arriba) no trae la ola 2024 de esta serie (verificado: cero
    # filas ENIF 2024 con "K2-BANCARIA" en el catalogo); esta CALC si la
    # tiene sellada en data/corrida0, asi que se completa desde ahi. ---
    for k2_dir in ("CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001", "CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0002"):
        if k2_dir not in idx:
            continue
        k2keys = idx[k2_dir]
        for k in sorted(k2keys):
            if not k.endswith("-P"):
                continue
            m_ola = re.search(r"-(\d{4})-", k)
            if not m_ola:
                continue
            ola_k = m_ola.group(1)
            if ola_k not in ("2012", "2015", "2018", "2021", "2024"):
                continue
            eje, segmento, conducta_toks = parse_llave(k)
            conducta_slug = ("-".join(conducta_toks))[:80]
            serie_key = (conducta_slug, eje, segmento, "proporción ponderada [0,1]")
            if serie_key in series and ola_k in series[serie_key]["olas"]:
                continue  # ya cubierta por el catalogo
            serie_id = "-".join(["ENIF", conducta_slug, eje, segmento])
            s = series.setdefault(serie_key, {
                "serie_id": serie_id, "dominio": "dinero", "conducta": conducta_slug,
                "conducta_texto": "tenencia de crédito bancario; ver denominador (K2, %s)" % k2_dir,
                "eje": eje, "segmento": segmento, "unidad": "proporción ponderada [0,1]",
                "llave_muestra": k, "olas": {},
            })
            lo_k, hi_k = k[:-2] + "-IC-LO", k[:-2] + "-IC-HI"
            s["olas"][ola_k] = {
                "calc": k2_dir, "result_p": k,
                "result_lo": lo_k if lo_k in k2keys else "",
                "result_hi": hi_k if hi_k in k2keys else "",
                "llave": k, "row_text": "",
            }

    # --- inyeccion directa: CALC-ENIF-FINTECH-0001 (no esta en el catalogo:
    # cero filas ENIF con "FINTECH" en canon/catalogo-del-mexicano-v1_0.tsv,
    # verificado por grep). Fuente pedida explicitamente por el encargo. ---
    fintech_dir = "CALC-ENIF-FINTECH-0001"
    if fintech_dir in idx:
        fkeys = idx[fintech_dir]
        for k in sorted(fkeys):
            m_can = re.match(r"^RESULT-ENIF-FINTECH-(\d{4})-(CREDITO|CUENTA)-CANAL-(.+)-P$", k)
            if not m_can:
                continue
            ola_f, fam, canal = m_can.groups()
            lo_k = k[:-2] + "-IC-LO"
            hi_k = k[:-2] + "-IC-HI"
            serie_key = ("FINTECH-%s-CANAL-%s" % (fam, canal), "NACIONAL", "TOTAL", "conditional-P-fintech")
            serie_id = "ENIF-FINTECH-%s-CANAL-%s-NACIONAL-TOTAL" % (fam, canal)
            s = series.setdefault(serie_key, {
                "serie_id": serie_id, "dominio": "dinero",
                "conducta": "FINTECH-%s-CANAL-%s" % (fam, canal),
                "conducta_texto": ("canal de contratacion del ultimo producto fintech (%s), entre quienes "
                                    "declaran tener cuenta/credito por Internet o app; "
                                    "ENIF-FINTECH-SERIE-spec-v1_0.md SS1" % fam.lower()),
                "eje": "NACIONAL", "segmento": "TOTAL", "unidad": "proporcion condicional al canal declarado [0,1]",
                "llave_muestra": k, "olas": {},
            })
            s["olas"][ola_f] = {
                "calc": fintech_dir, "result_p": k,
                "result_lo": lo_k if lo_k in fkeys else "",
                "result_hi": hi_k if hi_k in fkeys else "",
                "llave": k, "row_text": "",
            }

    # --- comparabilidad especial: DIN-CREDITO K-series ---
    k_re = re.compile(r"-K([1-8])-")
    fintech_re = re.compile(r"FINTECH")
    for s in series.values():
        m = None
        for o in s["olas"].values():
            m = k_re.search(o["llave"])
            if m:
                break
        s["kcode"] = ("K" + m.group(1)) if m else None
        s["is_fintech"] = any(fintech_re.search(o["llave"]) for o in s["olas"].values())
        dom_low = s["dominio"].lower()
        conducta_low = s["conducta_texto"].lower()
        s["is_ahorro"] = (dom_low == "dinero" and ("ahorr" in conducta_low or "guard" in conducta_low)
                           and s["kcode"] is None and not s["is_fintech"])

    filas = []
    n_pares_por_estado = {"COMPARABLE": 0, "CAMBIO-DOCUMENTADO": 0, "NO-DOCUMENTADO": 0,
                           "NO-COMPARABLE": 0}
    decisiones = []

    for s in series.values():
        olas_ordenadas = sorted(s["olas"].keys())
        if not olas_ordenadas:
            continue
        # determinar veredicto-vs-ancla por ola (si hay fuente)
        veredicto_por_ola = {}
        cita_fuente = None
        fuente_2020_hint = {}
        if s["kcode"]:
            for o in olas_ordenadas:
                r = credito_map.get((s["kcode"], o))
                if r:
                    veredicto_por_ola[o] = r["veredicto"]
                    fuente_2020_hint[o] = "2020" in r.get("reactivo", "") + r.get("texto_literal", "") + \
                        r.get("filtro_y_flujo", "")
            cita_fuente = "data/credito-comparabilidad-texto-v1_1.tsv:conducta=%s" % s["kcode"]
        elif s["is_ahorro"]:
            # decide D-code por texto de conducta y E-code por eje
            dcode = None
            cl = s["conducta_texto"].lower()
            if "informal" in cl:
                dcode = "D-INF"
            elif "formal" in cl:
                dcode = "D-FOR"
            code = EJE_A_ECODE.get(s["eje"]) if s["eje"] != "NACIONAL" else dcode
            if code:
                for o in olas_ordenadas:
                    r = ahorro_map.get((code, o))
                    if r:
                        veredicto_por_ola[o] = r["veredicto"]
                        fuente_2020_hint[o] = "2020" in r.get("reactivo", "") + r.get("texto_literal", "") + \
                            r.get("filtro_y_flujo", "")
                cita_fuente = "data/ahorro-comparabilidad-texto-v1_0.tsv:objeto=%s" % code

        for i, ola in enumerate(olas_ordenadas):
            o = s["olas"][ola]
            if i == 0:
                par = "PRIMERA"
                cita = cita_fuente or ""
                marca_2020 = "SI" if ("2020" in o["row_text"] or fuente_2020_hint.get(ola)) else "NO"
                nota = ""
                if o.get("fuera_de_escala"):
                    nota = "FUERA-DE-ESCALA-(0,1)"
                if s["is_fintech"]:
                    cita = ("forense/prereg-caja/ENIF-FINTECH-SERIE-spec-v1_0.md SS2 (2018 "
                            "NO-ESTIMABLE; 2024 no emite RESULT nuevo) + %s" % FINTECH_CORR.replace(REPO + "/", ""))
                    nota = "serie de una sola ola verificable (2021); 2018 dictaminada NO-ESTIMABLE, 2024 no emite RESULT numerico nuevo (spec SS2)."
            else:
                prev_ola = olas_ordenadas[i - 1]
                v_prev = veredicto_por_ola.get(prev_ola)
                v_cur = veredicto_por_ola.get(ola)
                if v_prev is None or v_cur is None:
                    par = "NO-DOCUMENTADO"
                    cita = cita_fuente or ""
                    nota = "sin fila de comparabilidad por texto para alguna de las dos olas del par" if cita_fuente else "sin fuente de comparabilidad por texto para esta conducta"
                else:
                    e_prev = veredicto_a_estado(v_prev)
                    e_cur = veredicto_a_estado(v_cur)
                    if e_prev == "NO-COMPARABLE" or e_cur == "NO-COMPARABLE":
                        par = "NO-COMPARABLE"
                    elif e_prev == "CAMBIO-DOCUMENTADO" or e_cur == "CAMBIO-DOCUMENTADO":
                        par = "CAMBIO-DOCUMENTADO"
                    elif e_prev == "COMPARABLE-ENDPOINT" and e_cur == "COMPARABLE-ENDPOINT":
                        par = "COMPARABLE"
                    else:
                        par = "NO-DOCUMENTADO"
                    cita = "%s ola=%s(%s) ola=%s(%s)" % (cita_fuente, prev_ola, v_prev, ola, v_cur)
                    nota = ""
                if o.get("fuera_de_escala"):
                    nota = (nota + "; " if nota else "") + "FUERA-DE-ESCALA-(0,1)"
                n_pares_por_estado[par] += 1
                marca_2020 = "SI" if (fuente_2020_hint.get(prev_ola) or fuente_2020_hint.get(ola)
                                        or "2020" in o["row_text"]) else "NO"

            filas.append([
                s["serie_id"], "ENIF", s["dominio"], s["conducta"], s["conducta_texto"],
                s["eje"], s["segmento"], s["unidad"], ola, o["calc"], o["result_p"],
                o["result_lo"], o["result_hi"], par, cita, marca_2020, nota,
            ])

    filas.sort(key=lambda f: (f[0], f[8]))

    lines = ["\t".join(HEADER)]
    for f in filas:
        lines.append("\t".join(f))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("catalogo ENIF filas leidas: %d" % n_leidas)
    print("excluidas por no-proporcion (texto de unidad_escala): %d" % n_no_proporcion)
    print("excluidas por no existir la llave en data/corrida0: %d" % n_sin_result_en_corrida0)
    print("series: %d" % len(series))
    print("filas escritas: %d" % len(filas))
    print("pares por estado: %s" % n_pares_por_estado)


if __name__ == "__main__":
    main()
