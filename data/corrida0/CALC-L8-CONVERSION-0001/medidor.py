"""`CALC-L8-CONVERSION-0001` -- las tres celdas de la conversion presidencial
(`participa_p0_minimo/maximo/media`) como derivacion DETERMINISTA de cuatro
escalares del artefacto de repo `data/l8-resultados-tipo-boleta-v1_0.json`.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO POR `ACTO GEN2-MEDICION-DEMANDA-1` (CAJA, 15/sep/2026) EN
UN COMMIT PROPIO, ANTES DE CORRERLO, contra el contrato que
`ACTO GEN2-SPECS-DEMANDA-1` (tanda 2) congelo en NUBE. Sin RNG, sin
ponderador, sin microdato: solo biblioteca estandar. El JSON se lee de los
BYTES que `preflight` ya verifico por sha256 (`origen: repo`), no reabriendo
el archivo.

Lo que decide el CODIGO y no la spec, declarado aqui: (1) las 40 medias se
toman de `por_transicion[i].y_de_media` y `.y_a_media`, en el orden del JSON
(20 x 2); una pata `null` o ausente cuenta en `G-N-MEDIA-AUSENTE` y no entra;
(2) `p0_media`/`p0_mediana` se calculan con `statistics.fmean`/`median` sobre
las medias presentes, en proporcion (pp / 100), y se cotejan contra la regla
al grano de 4 decimales que la regla publica; (3) `A-CLIP-ACTIVO` compara el
valor antes y despues de `clip`; (4) el sha256 del insumo se recalcula sobre
los bytes recibidos y se compara con el declarado en la spec -- si discorda,
todo sale `NO-ESTIMABLE-INSUMO-DISCORDA`.
"""
from __future__ import annotations

import hashlib
import json
import statistics

P = "RESULT-L8CONV-"
JSON_ID = "IN-L8-JSON"


def _num(v):
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def medir(inputs, contrato):
    p = contrato["parametros"]
    g4 = int(p["grano_ancla_decimales"])
    g6 = int(p["grano_delta_decimales"])
    grano = int(p["grano_gen1_decimales"])
    ref = p["valores_gen1_referencia"]
    anclas = list(p["anclas"])
    out: dict[str, object] = {}

    def no_estimable(codigo: str):
        for k in ("A-P-MINIMO", "A-P-MAXIMO", "A-P-MEDIA", "A-DELTA-VS-GEN1-MINIMO",
                  "A-DELTA-VS-GEN1-MAXIMO", "A-DELTA-VS-GEN1-MEDIA"):
            out.setdefault(P + k, None)
        for k in ("A-CLIP-ACTIVO", "A-GRANO-VERIFICADO", "A-REPRODUCE-GEN1",
                  "G-ANCLAS-COINCIDEN-GEN1", "C-IC-BETA-PRES", "C-IC-BETA-ROZA-CERO",
                  "C-VIA-INTERMEDIA-DESCARTADA", "G-SHA256-INSUMO"):
            out.setdefault(P + k, codigo)
        for k in ("G-N-MEDIAS", "G-N-MEDIA-AUSENTE"):
            out.setdefault(P + k, 0)
        for k in ("G-BETA-PRES-PP", "G-DELTA", "G-P0-MINIMO", "G-P0-MAXIMO", "G-P0-MEDIA", "G-P0-MEDIANA"):
            out.setdefault(P + k, 0.0)
        out[P + "A-ADOPCION"] = "NO-ADOPTABLE-NO-ESTIMABLE"
        return out

    ent = inputs[JSON_ID]
    crudo = ent.get("bytes")
    if crudo is None:
        with open(ent["ruta_absoluta"], "rb") as fh:
            crudo = fh.read()
    sha = hashlib.sha256(crudo).hexdigest()
    declarado = str(ent.get("sha256", ""))
    if sha != declarado:
        out[P + "G-SHA256-INSUMO"] = f"DISCORDA:{sha}"
        return no_estimable("NO-ESTIMABLE-INSUMO-DISCORDA")
    out[P + "G-SHA256-INSUMO"] = "COINCIDE"
    d = json.loads(crudo.decode("utf-8"))
    try:
        est = d["estimador"]
        beta = float(est["beta_pres_pp"])
        wc = est["wild_cluster_beta_pres"]
        ic = [float(wc["ic95"][0]), float(wc["ic95"][1])]
        beta_int = float(est["beta_int_pp"])
        wci = est["wild_cluster_beta_int"]["ic95"]
        trans = d["por_transicion"]
    except (KeyError, IndexError, TypeError) as exc:
        return no_estimable(f"NO-ESTIMABLE-CLAVE-AUSENTE:{exc}")
    medias, ausentes = [], 0
    for t in trans:
        for k in ("y_de_media", "y_a_media"):
            v = t.get(k)
            if v is None:
                ausentes += 1
            else:
                medias.append(float(v))
    out[P + "G-N-MEDIAS"] = len(medias)
    out[P + "G-N-MEDIA-AUSENTE"] = ausentes
    out[P + "G-BETA-PRES-PP"] = _num(beta)
    delta = round(beta / 100.0, g6)
    out[P + "G-DELTA"] = _num(delta)
    out[P + "C-IC-BETA-PRES"] = (f"ic95=[{ic[0]!r},{ic[1]!r}] pp; p={wc.get('p')!r}; "
                                 f"B={wc.get('B')!r}; n_conglomerados={wc.get('n_conglomerados')!r}")
    out[P + "C-IC-BETA-ROZA-CERO"] = "SI" if (ic[0] <= 0.0 or ic[0] < 0.1 * (ic[1] - ic[0])) else "NO"
    contiene = float(wci[0]) <= 0.0 <= float(wci[1])
    out[P + "C-VIA-INTERMEDIA-DESCARTADA"] = (f"beta_int={beta_int!r}; ic95=[{float(wci[0])!r},{float(wci[1])!r}]; "
                                              f"CONTIENE-CERO={'SI' if contiene else 'NO'}")
    if len(medias) != int(ref["p0_n_medias"]):
        return no_estimable(f"NO-ESTIMABLE-UNIVERSO-CAMBIO:{len(medias)}")
    if not medias:
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")
    p0 = {"minimo": min(medias) / 100.0, "maximo": max(medias) / 100.0,
          "media": statistics.fmean(medias) / 100.0}
    mediana = statistics.median(medias) / 100.0
    out[P + "G-P0-MINIMO"] = _num(p0["minimo"])
    out[P + "G-P0-MAXIMO"] = _num(p0["maximo"])
    out[P + "G-P0-MEDIA"] = _num(p0["media"])
    out[P + "G-P0-MEDIANA"] = _num(mediana)
    difs = []
    rango = ref["p0_rango_observado"]
    for nombre, mio, suyo in (("min", p0["minimo"], float(rango[0])), ("max", p0["maximo"], float(rango[1])),
                              ("media", p0["media"], float(ref["p0_media"])), ("mediana", mediana, float(ref["p0_mediana"]))):
        if round(mio, g4) != round(suyo, g4):
            difs.append(f"{nombre}={round(mio, g4)}!={suyo}")
    out[P + "G-ANCLAS-COINCIDEN-GEN1"] = "COINCIDE" if not difs else "DIFIERE:" + ",".join(difs)

    con, sin, recortadas = {}, {}, []
    for a in anclas:
        bruto = round(p0[a], g4) + delta
        val = min(1.0, max(0.0, bruto))
        if val != bruto:
            recortadas.append(a)
        con[a] = val
        sin[a] = min(1.0, max(0.0, p0[a] + delta))
    out[P + "A-P-MINIMO"] = _num(con["minimo"])
    out[P + "A-P-MAXIMO"] = _num(con["maximo"])
    out[P + "A-P-MEDIA"] = _num(con["media"])
    out[P + "A-CLIP-ACTIVO"] = "NO" if not recortadas else "SI:" + ",".join(recortadas)
    dmax = max(abs(con[a] - sin[a]) for a in anclas)
    out[P + "A-GRANO-VERIFICADO"] = ("con_ancla_r4=" + ";".join(f"{con[a]:.6f}" for a in anclas)
                                     + " | sin_redondear=" + ";".join(f"{sin[a]:.6f}" for a in anclas)
                                     + f" | diferencia_max={dmax:.1e}")
    no_rep = []
    for a, k in (("minimo", "participa_p0_minimo"), ("maximo", "participa_p0_maximo"), ("media", "participa_p0_media")):
        out[P + f"A-DELTA-VS-GEN1-{a.upper()}"] = _num(con[a] - float(ref[k]))
        if round(con[a], grano) != round(float(ref[k]), grano):
            no_rep.append(a)
    out[P + "A-REPRODUCE-GEN1"] = "REPRODUCE" if not no_rep else "NO-REPRODUCE:" + ",".join(no_rep)
    out[P + "A-ADOPCION"] = "LISTADO-PARA-MESA-REPRODUCE" if not no_rep else "LISTADO-PARA-MESA-NO-REPRODUCE"
    return out
