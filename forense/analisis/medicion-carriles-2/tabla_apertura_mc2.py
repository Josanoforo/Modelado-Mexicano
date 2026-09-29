#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · P1 · tabla de apertura por comando.

Una fila por afirmación MEDIBLE-EN-CORPUS del mapa v1.1 (235) y por regla
SIN-CIFRA-GEN2 de reglas-contrastadas v1.1 (141). Columnas: estado C3 (juicio de
los reports v2), si PISOS-DOMINIOS-Y-REGLAS-1 ya la midió, instrumento (primer
token reconocido de `instrumento_ola`/`instrumento_sugerido`), y la decisión de
este acto: la de sus fragmentos `*-dictamenes.tsv` (MEDIDO), la de la tabla
DECISIONES de abajo (CITADO-E5, DIFERIDO-A, NO-CONSTRUIBLE, CONGELADO) o
PENDIENTE-<instrumento>. Escribe tabla-apertura-mc2-v1_0.tsv y conteos-apertura.json.
No lee microdato."""
import collections
import glob
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIR = RAIZ / "forense/analisis/medicion-carriles-2"
TOK = re.compile(r"\b(ENVIPE|ENSU|ENDUTIH|ENIF|ENCIG|ENCUCI|ENOE|ENUT|ENIGH|ENSANUT|ENADID|ENDIREH|ENDISEG|"
                 r"ENASEM|ENBIARE|EDER|LAPOP|WVS|LATINOBAROMETRO|CNBV|BANXICO|CONEVAL|CPV2020|ITER|MMSI|PEW|"
                 r"ENSAFI|ENAFIN|ENCO|EMOVI|ENASIC|ENPECYT|EMAT|EDR|INEGI|INE)\b")
# decisiones de este acto que no salen de un fragmento de dictámenes (declaradas en las specs MC2-*)
DECISIONES = {
    "ASTRA5-U0-APUEST-030": "DIFERIDO-A:R06 (ENIF 2024 módulo 7 RESERVADO)",
    "ASTRA5-U0-APUEST-032": "DIFERIDO-A:R06 (ENIF 2024 módulo 7 RESERVADO)",
    "ASTRA5-U0-CONS-010": "DIFERIDO-A:R06 (ENIF 2024 módulo 7 RESERVADO)",
    "ASTRA5-U0-APUEST-011": "CITADO-E5:CALC-ENIF-FINTECH-0001 (nacional); segmentos en CALC-MC2-ENIF2024-0001",
    "ASTRA5-U0-CLIENT-014": "NO-CONSTRUIBLE (conteo de registro administrativo; spec MC2-ENIF2024 §3)",
    "ASTRA5-U0-CAPSOC-016": "CITADO-E5:CALC-PDR1-ENVIPE2025-0001 (AP4_11_06)",
    "ASTRA5-U0-SALUD-031": "CITADO-E5:S6-L16 (linajes sin reconciliar; no se repite)",
    "RG-34a21bc6a2": "NO-CONSTRUIBLE (ENIF no pregunta el tipo de organizador de la tanda; spec MC2-ENIF2024 §3)",
    "RG-145b91d071": "NO-CONSTRUIBLE (unidad comunidad; registro de autodefensas no está en el corpus)",
    "RG-7c6dd83a03": "INCOMPARABLE-v1.1 (banda fijada tras ver el dato; no se puede pre-registrar sobre dato visto)",
}
CONGELADO = {"VIOL-007", "TRUST-026", "CAPSOC-017", "VIOL-020", "CAPSOC-018", "VIOL-033", "VIOL-032",
             "VIOL-043", "TIME-038", "POL-009"}


def lee(p):
    L = Path(p).read_text(encoding="utf-8").split("\n")
    h = [x.strip('"') for x in L[0].split("\t")]
    return h, [dict(zip(h, [x.strip('"') for x in l.split("\t")])) for l in L[1:] if l]


def token(txt):
    m = TOK.findall(txt.upper())
    return m[0] if m else "SIN-TOKEN"


_, mapa = lee(RAIZ / "canon/mapa-dominios-v1_1.tsv")
med = {r["id_afirmacion"]: r for r in mapa if "MEDIBLE-EN-CORPUS" in r["dictamen"]}
c3 = collections.defaultdict(list)
for f in sorted(glob.glob(str(RAIZ / "forense/analisis/reports-v2/**/*.tsv"), recursive=True)):
    try:
        h, R = lee(f)
    except Exception:
        continue
    dk = next((k for k in ("juicio_v2", "dictamen") if k in h), None)
    if not dk:
        continue
    for r in R:
        i = r.get("mapa_id") or r.get("id_afirmacion") or r.get("id")
        if i in med and r.get(dk):
            c3[i].append(r[dk].split()[0])
_, pdr = lee(RAIZ / "forense/analisis/pisos-dominios-1/tabla-apertura-v1_0.tsv")
pdr1 = {r["id"]: r["pieza"] for r in pdr if r.get("pieza", "—") != "—"}
mc2 = {}
for f in sorted(glob.glob(str(DIR / "*-dictamenes.tsv"))):
    _, R = lee(f)
    for r in R:
        mc2[r["id"]] = f"MEDIDO:{r['dictamen']} ({r['calc'] or Path(f).name})"

filas = []
for i, r in sorted(med.items()):
    corto = i.replace("ASTRA5-U0-", "")
    tok = token(r["instrumento_ola"])
    if i in mc2:
        dec = mc2[i]
    elif i in DECISIONES:
        dec = DECISIONES[i]
    elif corto in CONGELADO:
        dec = "CONGELADO:CALC-MC2-ENVIPE2025-0001 (COMMIT-1; corre al liberarse cupo)"
    elif i in pdr1:
        dec = f"CITADO-E5:{pdr1[i]} (PISOS-DOMINIOS-Y-REGLAS-1)"
    elif c3.get(i) and not any(x.startswith("SIN-CIFRA") for x in c3[i]):
        dec = f"CON-JUICIO-C3:{c3[i][0]} (sin RESULT propio verificado)"
    else:
        dec = f"PENDIENTE-{tok}"
    filas.append(["afirmacion", i, r["dominio"], tok, r["instrumento_ola"][:120].replace("\t", " "),
                  ";".join(sorted(set(c3.get(i, [])))) or "SIN-C3", pdr1.get(i, ""), dec])
_, reg = lee(RAIZ / "canon/reglas-contrastadas-v1_1.tsv")
for r in reg:
    if not r["dictamen"].startswith("SIN-CIFRA"):
        continue
    dec = mc2.get(r["regla_id"]) or DECISIONES.get(r["regla_id"]) or ("NO-CONSTRUIBLE-v1.1 (sin motivo nuevo en este acto)"
                                     if r["detalle_dictamen"].startswith(("NO-CONSTRUIBLE", "PDR1 NO-CONSTRUIBLE"))
                                     else f"PENDIENTE-{token(r['instrumento_sugerido'])}")
    filas.append(["regla", r["regla_id"], r["dominio_catalogo"], token(r["instrumento_sugerido"]),
                  r["instrumento_sugerido"][:120].replace("\t", " "), "—", "", dec])
cab = ["clase", "id", "dominio", "instrumento", "instrumento_texto", "estado_c3", "pieza_pdr1", "decision_mc2"]
(DIR / "tabla-apertura-mc2-v1_0.tsv").write_text("\t".join(cab) + "\n" + "".join("\t".join(f) + "\n" for f in filas),
                                            encoding="utf-8")
cont = collections.Counter((f[0], f[7].split(":")[0].split(" ")[0]) for f in filas)
pend = collections.Counter(f[3] for f in filas if f[7].startswith("PENDIENTE"))
res = {"por_clase_y_decision": {f"{a}|{b}": n for (a, b), n in sorted(cont.items())},
       "pendientes_por_instrumento": dict(pend.most_common())}
(DIR / "conteos-apertura.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(json.dumps(res, ensure_ascii=False))
