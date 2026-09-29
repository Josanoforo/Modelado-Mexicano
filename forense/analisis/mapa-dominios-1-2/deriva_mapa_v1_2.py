"""GEN2-MAPA-DOMINIOS-Y-LICENCIAS-1 · P1 · deriva canon/mapa-dominios-v1_2.tsv desde v1.1.

Uso:
    python3 forense/analisis/mapa-dominios-1-2/deriva_mapa_v1_2.py            # dry-run: conteos
    python3 forense/analisis/mapa-dominios-1-2/deriva_mapa_v1_2.py --escribe  # escribe v1.2 y anexos

Qué cambia (solo columnas de estado; v1.1 intacta):
  * gen2_existente — «VISTA: …» cuando la afirmación se une a un CALC con RESULT
    GEN2 SELLADA registrado en data/corrida0/resultados.tsv (E.7). Unión por
    instrumento × ola: instrumentos con el vocabulario y los patrones de
    tools/tablero_carriles.py sobre `instrumento_ola`+`programa_id`; olas = años
    de `instrumento_ola`+`ola_v1_1`; del lado del CALC, los mismos patrones y
    años sobre el id del CALC. Es unión por objeto medido, no por pregunta: el
    valor lo dice. Un CALC sellado en disco (data/corrida0/CALC-*/sello.json)
    sin fila en la vista NO cuenta: «sellado en disco, no registrado».
  * siguiente_operacion — vocabulario del tablero (FIRMA · RESERVA · ADQUISICION ·
    CALC · EDITORIAL · NADA), con el valor de v1.1 en siguiente_operacion_v1_1.
  * dictamen (clase) — re-dictaminado solo si el cruce de las
    INSTRUMENTO-SIN-EQUIVALENCIA con mapa-instrumentos-alternos-v1_0 y
    reglas-contrastadas-v1_1 encuentra reactivo que satisface (ver cruce-611.tsv).
Columnas nuevas: gen2_existente_v1_1, siguiente_operacion_v1_1, calc_vista,
estado_corpus_v1_2, reserva_v1_2 (desde data/manifiesto.yaml por id, A.15), cambio_v1_2.
"""
import collections
import csv
import glob
import os
import re
import sys
import unicodedata

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import tablero_carriles as tc  # noqa: E402

csv.field_size_limit(10**9)
V11 = "canon/mapa-dominios-v1_1.tsv"
V12 = "canon/mapa-dominios-v1_2.tsv"
DIR = "forense/analisis/mapa-dominios-1-2"
NUEVAS = ["gen2_existente_v1_1", "siguiente_operacion_v1_1", "calc_vista",
          "estado_corpus_v1_2", "reserva_v1_2", "cambio_v1_2"]
ANIO = re.compile(r"(?<!\d)(?:19[5-9]\d|20[0-3]\d)(?!\d)")
UMBRAL_CRUCE = 0.15  # Jaccard de palabras ≥5 letras; solo para listar candidatos, nunca para promover


def r(rel):
    return os.path.join(RAIZ, rel)


def lee(rel):
    return tc.lee_tsv(rel)


def calc_base(cid):
    return cid.split("--")[0]


def texto_calc(cid):
    """CALC-DIN-CREDITO-PISOS-ENIF2021 → 'DIN CREDITO PISOS ENIF 2021' (los patrones exigen frontera)."""
    t = re.sub(r"([A-Za-z])(\d)", r"\1 \2", cid)
    t = re.sub(r"(\d)([A-Za-z])", r"\1 \2", t)
    return t.replace("-", " ").replace("_", " ")


def vista():
    """{calc_base: {'n': RESULT, 'cuenta': Counter}} de la vista (GEN2, SELLADA)."""
    out = {}
    for x in lee("data/corrida0/resultados.tsv"):
        if x.get("generacion") != "GEN2" or x.get("estado") != "SELLADA":
            continue
        b = calc_base(x["corrida_id"])
        e = out.setdefault(b, {"n": 0, "cuenta": collections.Counter()})
        e["n"] += 1
        e["cuenta"][x["cuenta_gen2"]] += 1
    return out


def disco():
    return {calc_base(os.path.basename(os.path.dirname(p)))
            for p in glob.glob(r("data/corrida0/CALC-*/sello.json"))}


def indice_calc(calcs, pats):
    """(instrumento, ola) → [calc] sobre los ids de CALC."""
    idx = collections.defaultdict(list)
    for c in sorted(calcs):
        t = texto_calc(c)
        for ins in tc.instrumentos_en(t, pats):
            for a in set(ANIO.findall(t)):
                idx[(ins, a)].append(c)
    return idx


def llaves_afirmacion(x, pats):
    ins = tc.instrumentos_en(x["instrumento_ola"] + " " + x["programa_id"], pats)
    olas = set(ANIO.findall(x["instrumento_ola"] + " " + x["ola_v1_1"]))
    return [(i, a) for i in ins for a in sorted(olas)]


def union(mapa, pats, idx):
    return {x["id_afirmacion"]: sorted({c for k in llaves_afirmacion(x, pats) for c in idx.get(k, [])})
            for x in mapa}


def patrones_tablero(mapa):
    cat = lee(tc.FUENTES["F2"])
    tfinal = lee(tc.FUENTES["F12"])
    return tc.patrones(tc.vocabulario([x for x in mapa if x["report"].startswith("corpus/reports/")],
                                      {x["instrumento"] for x in cat}, tfinal))


def manifiesto():
    with open(r("data/manifiesto.yaml"), encoding="utf-8") as f:
        return {e["id"]: e for e in yaml.safe_load(f)}


TOK = re.compile(r"[A-Za-z0-9_]+")


def ids_citados(x, man):
    s = " ".join(x[c] for c in ("datos_id_estado", "documento_id_hash_pagina", "instrumento_ola"))
    return sorted(set(TOK.findall(s)) & set(man))


def nt(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return {w for w in re.findall(r"[a-z]{5,}", "".join(c for c in s if not unicodedata.combining(c)))}


def cruce_611(mapa):
    """Candidatos ≥ UMBRAL_CRUCE; veredicto por candidato (ninguno promueve si no es EXISTE-SATISFACE pleno)."""
    alt = lee("canon/mapa-instrumentos-alternos-v1_0.tsv")
    reg = lee("canon/reglas-contrastadas-v1_1.tsv")
    filas, univ = [], 0
    for x in mapa:
        if not x["estado_corpus_v1_1"].startswith("INSTRUMENTO-SIN-EQUIVALENCIA"):
            continue
        univ += 1
        A = nt(x["texto_vigente"] + " " + x["componente_contrastable"])
        for fuente, lst, txt in (("alternos", alt, lambda y: y["texto_pregunta"] + " " + y["que_falta_para_la_incognita"]),
                                 ("reglas", reg, lambda y: y["texto"] + " " + y["conducta_entonces"])):
            for i, y in enumerate(lst):
                B = nt(txt(y))
                j = len(A & B) / max(1, len(A | B))
                if j < UMBRAL_CRUCE:
                    continue
                if fuente == "alternos":
                    satisface = y["dictamen_A4"].startswith("EXISTE-SATISFACE(")
                    ref = f"fila {i + 2}: {y['incognita']} {y['instrumento']} {y['ola']}"
                    dic = y["dictamen_A4"]
                else:
                    satisface = bool(y["resultado_id"]) and y["dictamen"] in ("CONFIRMA", "MATIZA")
                    ref = f"{y['regla_id']} ({y['dictamen']})"
                    dic = y["dictamen"] + (f" {y['resultado_id']}" if y["resultado_id"] else "")
                veredicto = ("REVISAR-A-MANO" if satisface else
                             "NO-PROMUEVE (" + ("dictamen PARCIAL/NO-SATISFACE del alterno" if fuente == "alternos"
                                                else "regla sin cifra GEN2") + ")")
                filas.append({"id_afirmacion": x["id_afirmacion"], "dominio": x["dominio"], "fuente": fuente,
                              "referencia": ref, "jaccard": f"{j:.3f}", "dictamen_fuente": dic[:160],
                              "veredicto": veredicto})
    return univ, len(alt), len(reg), filas


def sig_op(x, calcs, v, reserva_v12):
    d = x["dictamen"]
    if d in ("NO-MEDIBLE-POR-DISEÑO", "NO-CONSTRUIBLE-EN-CORPUS"):
        return f"NADA · {d}"
    if reserva_v12.startswith("RESERVADA"):
        return f"RESERVA · {reserva_v12[:80]}"
    if calcs:
        cu = collections.Counter()
        for c in calcs:
            cu.update(v[c]["cuenta"])
        if not cu.get("SI"):
            return "FIRMA · RESULT en vista sin cuenta_gen2=SI (" + ", ".join(f"{k} {n}" for k, n in cu.most_common(3)) + ")"
        return "EDITORIAL · cifra GEN2 en vista por instrumento×ola; falta citarla por afirmación"
    if d == "MEDIBLE-CON-ADQUISICIÓN":
        return "ADQUISICION · instrumento fuera del corpus (v1.1)"
    return "CALC · medible en corpus sin RESULT en vista por instrumento×ola"


def deriva():
    mapa = lee(V11)
    pats = patrones_tablero(mapa)
    v = vista()
    d = disco()
    idx_v = indice_calc(v.keys(), pats)
    idx_d = indice_calc(d - set(v), pats)
    u_v = union(mapa, pats, idx_v)
    u_d = union(mapa, pats, idx_d)
    man = manifiesto()
    out = []
    for x in mapa:
        y = dict(x)
        a = x["id_afirmacion"]
        cambios = []
        calcs = u_v[a]
        y["gen2_existente_v1_1"] = x["gen2_existente"]
        y["siguiente_operacion_v1_1"] = x["siguiente_operacion"]
        y["calc_vista"] = ";".join(calcs)
        if calcs:
            nres = sum(v[c]["n"] for c in calcs)
            y["gen2_existente"] = (f"VISTA: {nres} RESULT GEN2 SELLADA en {len(calcs)} CALC por instrumento×ola "
                                   f"({', '.join(sorted({f'{i} {o}' for i, o in llaves_afirmacion(x, pats) if idx_v.get((i, o))}))}); "
                                   f"ej. {', '.join(calcs[:3])}; unión por objeto, no por pregunta")
            cambios.append("gen2_existente")
        elif u_d[a]:
            y["gen2_existente"] = (f"sellado en disco, no registrado ({len(u_d[a])} corridas; no cuenta, E.7)"
                                   + (f" · v1.1: {x['gen2_existente']}" if x["gen2_existente"] else ""))
            cambios.append("gen2_existente(disco)")
        ids = ids_citados(x, man)
        if ids:
            res = sorted({str(man[i].get("estado_reserva") or "") for i in ids} - {""})
            y["estado_corpus_v1_2"] = f"EN-MANIFIESTO: {len(ids)} id ({';'.join(ids[:6])}{'…' if len(ids) > 6 else ''})"
            rv = [s for s in res if s.startswith("RESERV")]
            y["reserva_v1_2"] = (rv[0] if rv else ("ninguna en manifiesto" + (f" ({res[0]})" if res else "")))
        else:
            y["estado_corpus_v1_2"] = f"SIN-ID-DE-MANIFIESTO-CITADO · v1.1: {x['estado_corpus_v1_1']}"
            y["reserva_v1_2"] = ""
        y["siguiente_operacion"] = sig_op(x, calcs, v, y["reserva_v1_2"])
        cambios.append("siguiente_operacion")
        y["cambio_v1_2"] = ";".join(cambios)
        out.append(y)
    return mapa, out, v, d, cruce_611(mapa)


def escribe_tsv(rel, filas, campos):
    with open(r(rel), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    mapa, out, v, d, (univ, nalt, nreg, cruce) = deriva()
    gan = sum(1 for y in out if y["calc_vista"])
    dis = sum(1 for y in out if "gen2_existente(disco)" in y["cambio_v1_2"])
    print(f"filas v1.1 {len(mapa)} · v1.2 {len(out)}")
    print(f"vista: {len(v)} CALC GEN2 SELLADA · disco: {len(d)} CALC con sello.json · disco sin vista: {len(d - set(v))}")
    print(f"gen2_existente VISTA: {gan} · sellado en disco no registrado: {dis}")
    print("clase antes:", dict(collections.Counter(x["dictamen"] for x in mapa)))
    print("clase después:", dict(collections.Counter(y["dictamen"] for y in out)))
    print("siguiente_operacion:", dict(collections.Counter(y["siguiente_operacion"].split(" · ")[0] for y in out)))
    print(f"cruce 611: universo {univ} × {nalt} alternos + {nreg} reglas; candidatos ≥{UMBRAL_CRUCE}: {len(cruce)}; "
          f"veredictos: {dict(collections.Counter(c['veredicto'].split(' ')[0] for c in cruce))}")
    if "--escribe" in argv:
        escribe_tsv(V12, out, list(mapa[0].keys()) + NUEVAS)
        os.makedirs(r(DIR), exist_ok=True)
        escribe_tsv(f"{DIR}/cruce-611.tsv", cruce, ["id_afirmacion", "dominio", "fuente", "referencia", "jaccard",
                                                    "dictamen_fuente", "veredicto"])
        with open(r(f"{DIR}/vista-usada.txt"), "w", encoding="utf-8") as f:
            f.write(tc.blob("data/corrida0/resultados.tsv") + "\n")
        print(f"escrito {V12}, {DIR}/cruce-611.tsv y {DIR}/vista-usada.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
