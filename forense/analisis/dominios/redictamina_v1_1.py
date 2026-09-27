"""Derivador del mapa de dominios v1.1 (ACTO GEN2-MAPA-DOMINIOS-V1-1-1).

Extensión declarada del mapa v1.0 (`ensambla_mapa.py`), que no se toca: lee
`canon/mapa-dominios-v1_0.tsv` como insumo congelado y re-dictamina cada
afirmación MEDIBLE-CON-ADQUISICIÓN contra el corpus de CORPUS-COMPLETO-1
(`forense/analisis/corpus-completo/tabla-final-v1_0.tsv`).

Piezas (encargo §5):
  P1  equivalencias instrumento → programa_id   (equivalencias-v1_1.tsv)
  P2  re-dictamen por afirmación                 (canon/mapa-dominios-v1_1.tsv)
  P3  cola de medición por (dominio, programa)  (cola-medicion-v1_0.tsv)
  P4  cobertura por report (forma de cobertura-31) (cobertura-v1_1.tsv)

Compuerta A.15 (encargo §8): MEDIBLE-EN-CORPUS sólo si la afirmación tiene
fila en `verificaciones-texto-v1_1.tsv` y su `texto_pregunta` casa,
byte a byte, con una fila del inventario de reactivos del repo para esa
`variable` y ese instrumento-ola. Un texto que no casa es error, no
degradación silenciosa. NO-CONSTRUIBLE-EN-CORPUS sólo con fila en
`no-construibles-v1_1.tsv` (pregunta buscada + secciones recorridas).
Sin fila en ninguna de las dos, la afirmación sigue MEDIBLE-CON-ADQUISICIÓN
y la columna `estado_corpus_v1_1` dice por qué (programa y ola en corpus
con texto no verificado aquí, programa no obtenido, instrumento sin
equivalencia).

    python3 forense/analisis/dominios/redictamina_v1_1.py            # escribe
    python3 forense/analisis/dominios/redictamina_v1_1.py --verifica # byte a byte
"""
from __future__ import annotations

import csv
import io
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DIR = Path(__file__).resolve().parent
MAPA_V10 = ROOT / "canon/mapa-dominios-v1_0.tsv"
MAPA_V11 = ROOT / "canon/mapa-dominios-v1_1.tsv"
TABLA = ROOT / "forense/analisis/corpus-completo/tabla-final-v1_0.tsv"
VERIF = DIR / "verificaciones-texto-v1_1.tsv"
NOCONS = DIR / "no-construibles-v1_1.tsv"
OUT_EQ = DIR / "equivalencias-v1_1.tsv"
OUT_COLA = DIR / "cola-medicion-v1_0.tsv"
OUT_COB = DIR / "cobertura-v1_1.tsv"
INVENTARIOS = [
    "data/inventario-reactivos-v1_2.tsv",
    "data/inventario-fd-v1_1.tsv",
    "data/inventario-reactivos-ext-v1_0.tsv",
    "data/inventario-reactivos-fd-recuperado-v1_0.tsv",
    "data/inventario-reactivos-contexto-fd26-v1_0.tsv",
    "data/inventario-reactivos-contexto-v1_1.tsv",
    # ACTO GEN2-SEGURIDAD-ENSU-SERIE-1: textos ENSU del FD (sin inventario previo).
    "forense/analisis/seguridad-ensu/inventario-reactivos-ensu-v1_0.tsv",
    # ACTO GEN2-COLA-COMPLETA-1: textos transcritos del FD/cuestionario (MMSI, ENDISEG, ENADID, Latinobarómetro, PEW, ENSANUT).
    "tools/dominios/cola-completa/inventario-reactivos-cola-completa-v1_0.tsv",
]

MED_ADQ = "MEDIBLE-CON-ADQUISICIÓN"
MED_CORPUS = "MEDIBLE-EN-CORPUS"
NO_CONS = "NO-CONSTRUIBLE-EN-CORPUS"
NO_DISENO = "NO-MEDIBLE-POR-DISEÑO"

# Alias textuales → programa_id del catálogo (además del código del programa
# como token exacto). Se declaran aquí, una sola vez; la tabla de
# equivalencias que sale cita cuál casó.
ALIAS = {
    "latinobar": "LATINOBAROMETRO",
    "world values": "WVS",
    "americasbarometer": "LAPOP",
    "americas barometer": "LAPOP",
    "barómetro de las américas": "LAPOP",
    "pew research": "PEW",
    "censo de poblaci": "CCPV",
    "encuesta intercensal": "INTERCENSAL",
    "banxico": "BANXICO",
    "banco de méxico": "BANXICO",
    "emovi": "CEEY_EMOVI",
    "estadística de matrimonios": "EMAT",
    "estadisticas de defunciones": "EDR",
}
# Códigos que son palabra común o sigla ambigua: sólo casan por alias.
NO_TOKEN = {"CA", "CE", "DH", "ED", "EDF", "SALUD", "MUSEOS", "ACCIDENTES",
            "INVESTIGACION", "MIGRACION", "NATALIDAD", "MORTALIDAD",
            "NUPCIALIDAD", "EIA", "EAC", "EAT", "ENE", "ENH", "EMS", "ETI",
            "EVF", "PEME", "CJM", "MCS", "MTI", "EOD", "EIM", "ENG"}
# C4 de FIRMAS-16 (encargo §2): boletín ENOE 2026T1 consumido.
C4 = ("C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de "
      "informalidad puede usarlo para preparación ciega")
TIER_PRIORIDAD = re.compile(r"^\s*(FUERTE|MEDIA|MEDIO|SÓLID|SOLID|MEDIA-FUERTE)", re.I)


def lee(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader((l for l in fh if not l.startswith("#")), delimiter="\t"))


def tsv(cols: list[str], rows: list[dict], cabecera: str | None = None) -> str:
    buf = io.StringIO()
    if cabecera:
        buf.write(cabecera + "\n")
    w = csv.DictWriter(buf, cols, delimiter="\t", lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def olas(celda: str) -> list[str]:
    return [o.split(" [")[0].strip() for o in celda.split(";") if o.strip()]


def corpus() -> dict[str, dict]:
    out = {}
    for r in lee(TABLA):
        en = olas(r["olas_adquiridas_por_este_acto"]) + olas(r["olas_ya_en_corpus"])
        out[r["programa"]] = {"fuente": r["fuente"], "olas": en,
                              "reservadas": olas(r["olas_reservadas_al_entrar"]),
                              "no_obtenido": r["no_obtenido"]}
    return out


def equivalencia(texto: str, programas: list[str]) -> list[tuple[str, str]]:
    """(programa_id, cómo casó), en orden de aparición en el texto."""
    hits = []
    low = texto.lower()
    for p in programas:
        if p in NO_TOKEN:
            continue
        m = re.search(r"(?<![A-Za-z0-9_])" + re.escape(p) + r"(?![A-Za-z0-9_])", texto)
        if m:
            hits.append((m.start(), p, f"token:{p}"))
    for a, p in ALIAS.items():
        i = low.find(a)
        if i >= 0 and p in programas:
            hits.append((i, p, f"alias:{a}"))
    vistos, out = set(), []
    for _, p, como in sorted(hits):
        if p not in vistos:
            vistos.add(p)
            out.append((p, como))
    return out


def inventario() -> dict[tuple[str, str], set[str]]:
    """(instrumento en minúsculas, variable) → textos de reactivo."""
    idx: dict[tuple[str, str], set[str]] = defaultdict(set)
    for rel in INVENTARIOS:
        for r in lee(ROOT / rel):
            if r.get("texto_reactivo"):
                idx[(r["instrumento"].lower(), r["variable_id"])].add(r["texto_reactivo"])
    return idx


def main(verifica: bool) -> int:
    v10 = lee(MAPA_V10)
    cols10 = list(v10[0].keys())
    cp = corpus()
    programas = sorted(cp)
    verif = {r["id_afirmacion"]: r for r in lee(VERIF)}
    nocons = {r["id_afirmacion"]: r for r in lee(NOCONS)}
    inv = inventario()
    errores = []

    eq_rows, mapa, cola = [], [], defaultdict(lambda: {"ids": [], "olas": set(), "reports": set(), "prio": 0})
    for r in v10:
        r = dict(r)
        nuevo = {"dictamen_v1_0": r["dictamen"], "programa_id": "", "ola_v1_1": "",
                 "variable_v1_1": "", "texto_pregunta_v1_1": "", "unidad_v1_1": "",
                 "estado_corpus_v1_1": "", "reserva_v1_1": ""}
        texto = r["instrumento_ola"] + " " + r["datos_id_estado"]
        if "ENOE" in texto.upper() and ("informal" in (r["texto_vigente"] + texto).lower()):
            nuevo["reserva_v1_1"] = C4
        if r["dictamen"] == MED_ADQ:
            citado = r["instrumento_ola"].strip() or ("(instrumento_ola vacío en v1.0) datos_id_estado: "
                                                      + (r["datos_id_estado"].strip() or r["siguiente_operacion"].strip()))
            eq = equivalencia(citado, programas)
            en = [(p, c) for p, c in eq if cp[p]["olas"]]
            eq_rows.append({
                "id_afirmacion": r["id_afirmacion"],
                "instrumento_texto": citado,
                "programa_id": ";".join(p for p, _ in eq) or "NO-ENCONTRADO",
                "casado_por": ";".join(c for _, c in eq),
                "programa_en_corpus": ";".join(p for p, _ in en),
                "nota": "" if eq else "NO-ENCONTRADO: ningún código ni alias del catálogo "
                        f"({len(programas)} programas) en el texto citado",
            })
            anios = set(re.findall(r"(?<!\d)(?:19|20)\d\d(?!\d)", citado))
            prog = en[0][0] if en else (eq[0][0] if eq else "")
            nuevo["programa_id"] = prog
            if r["id_afirmacion"] in verif:
                v = verif[r["id_afirmacion"]]
                if r["id_afirmacion"] in nocons:
                    errores.append(f"{r['id_afirmacion']}: en verificaciones y en no-construibles")
                textos = inv.get((v["instrumento_inventario"].lower(), v["variable"]), set())
                if v["texto_pregunta"] not in textos:
                    errores.append(f"{r['id_afirmacion']}: texto_pregunta no casa con el inventario "
                                   f"({v['instrumento_inventario']}, {v['variable']})")
                    continue
                if v["ola"] in cp.get(v["programa_id"], {}).get("reservadas", []):
                    errores.append(f"{r['id_afirmacion']}: ola reservada {v['programa_id']} {v['ola']}")
                    continue
                r["dictamen"] = MED_CORPUS
                r["dictamen_razon"] = (f"v1.1: texto de pregunta verificado en inventario "
                                       f"{v['fuente_inventario']} ({v['instrumento_inventario']}:{v['variable']}); "
                                       f"cubre: {v['cubre']}")
                nuevo.update({"programa_id": v["programa_id"], "ola_v1_1": v["ola"],
                              "variable_v1_1": v["variable"], "texto_pregunta_v1_1": v["texto_pregunta"],
                              "unidad_v1_1": v["unidad"], "estado_corpus_v1_1": "TEXTO-VERIFICADO"})
            elif r["id_afirmacion"] in nocons:
                n = nocons[r["id_afirmacion"]]
                r["dictamen"] = NO_CONS
                r["dictamen_razon"] = (f"v1.1: {n['programa_id']} {n['ola']} en corpus; pregunta buscada "
                                       f"«{n['pregunta_buscada']}» no está; recorrido: {n['secciones_recorridas']}")
                nuevo.update({"programa_id": n["programa_id"], "ola_v1_1": n["ola"],
                              "estado_corpus_v1_1": "PREGUNTA-NO-ESTA"})
            elif en:
                p = en[0][0]
                ola = sorted(a for a in anios if a in cp[p]["olas"] and a not in cp[p]["reservadas"])
                nuevo["ola_v1_1"] = ";".join(ola)
                nuevo["estado_corpus_v1_1"] = (
                    ("PROGRAMA-Y-OLA-EN-CORPUS" if ola else "PROGRAMA-EN-CORPUS-OLA-NO-CASADA")
                    + ": texto de pregunta NO-VERIFICADO-AQUÍ (payload fuera de este clon; "
                    "sin fila en inventarios del repo que la sostenga)")
            elif eq:
                nuevo["estado_corpus_v1_1"] = (f"PROGRAMA-NO-OBTENIDO: {eq[0][0]} sin olas en tabla final; "
                                               f"receta: {cp[eq[0][0]]['no_obtenido'][:200]}")
            else:
                nuevo["estado_corpus_v1_1"] = "INSTRUMENTO-SIN-EQUIVALENCIA (ver equivalencias-v1_1.tsv)"
        elif r["dictamen"] == MED_CORPUS:
            nuevo["estado_corpus_v1_1"] = "DE-V1_0"
        else:
            nuevo["estado_corpus_v1_1"] = "NO-REVISADO (NO-MEDIBLE-POR-DISEÑO, encargo P2)"
        r.update(nuevo)
        mapa.append(r)
        if r["dictamen"] in (MED_CORPUS, MED_ADQ) and nuevo["programa_id"] and nuevo["estado_corpus_v1_1"] != "DE-V1_0" \
                and cp.get(nuevo["programa_id"], {}).get("olas"):
            k = (r["dominio"], nuevo["programa_id"])
            c = cola[k]
            c["ids"].append(r["id_afirmacion"])
            c["olas"].update(o for o in nuevo["ola_v1_1"].split(";") if o)
            c["reports"].add(Path(r["report"]).name)
            c["verificadas"] = c.get("verificadas", 0) + (r["dictamen"] == MED_CORPUS)
            if TIER_PRIORIDAD.match(r["tier_report"]):
                c["prio"] += 1

    cols11 = cols10 + ["dictamen_v1_0", "programa_id", "ola_v1_1", "variable_v1_1", "texto_pregunta_v1_1",
                       "unidad_v1_1", "estado_corpus_v1_1", "reserva_v1_1"]
    cola_rows = [{"dominio": d, "programa": p, "ola": ";".join(sorted(c["olas"])) or "SIN-OLA-CASADA",
                  "n_afirmaciones": len(c["ids"]), "n_texto_verificado": c.get("verificadas", 0),
                  "reports": len(c["reports"]), "reports_que_sostiene": ";".join(sorted(c["reports"])),
                  "prioridad": c["prio"], "ids": ";".join(c["ids"])}
                 for (d, p), c in cola.items()]
    cola_rows.sort(key=lambda x: (-x["prioridad"], -x["n_afirmaciones"], x["dominio"], x["programa"]))

    cob: dict[str, Counter] = defaultdict(Counter)
    dom = {}
    for r in mapa:
        rep = Path(r["report"]).name
        dom[rep] = r["dominio"]
        cob[rep]["afirmaciones"] += 1
        cob[rep][r["dictamen"]] += 1
        cob[rep]["v10_" + r["dictamen_v1_0"]] += 1
    cob_rows = [{"report": rep, "dominio": dom[rep], "afirmaciones": c["afirmaciones"],
                 "medible_en_corpus": c[MED_CORPUS], "medible_con_adquisicion": c[MED_ADQ],
                 "no_construible_en_corpus": c[NO_CONS], "no_medible_por_diseno": c[NO_DISENO],
                 "medible_en_corpus_v1_0": c["v10_" + MED_CORPUS],
                 "medible_con_adquisicion_v1_0": c["v10_" + MED_ADQ]} for rep, c in sorted(cob.items())]

    gen = "# GENERADO por forense/analisis/dominios/redictamina_v1_1.py — no editar"
    salidas = {
        MAPA_V11: tsv(cols11, mapa),
        OUT_EQ: tsv(["id_afirmacion", "programa_id", "casado_por", "programa_en_corpus", "nota",
                     "instrumento_texto"], eq_rows, gen),
        OUT_COLA: tsv(list(cola_rows[0].keys()), cola_rows, gen),
        OUT_COB: tsv(list(cob_rows[0].keys()), cob_rows, gen),
    }
    if errores:
        print("ERROR-COMPUERTA-A15", *errores, sep="\n  ")
        return 2
    malos = 0
    for path, txt in salidas.items():
        if verifica:
            ok = path.exists() and path.read_text(encoding="utf-8") == txt
            malos += not ok
            print(("COINCIDE " if ok else "DIFIERE  ") + str(path.relative_to(ROOT)))
        else:
            path.write_text(txt, encoding="utf-8")
    cuenta = Counter(r["dictamen"] for r in mapa)
    print("dictamen v1.1:", dict(sorted(cuenta.items())), "· sin dictamen:",
          sum(1 for r in mapa if not r["dictamen"]))
    print("equivalencias NO-ENCONTRADO:", sum(e["programa_id"] == "NO-ENCONTRADO" for e in eq_rows),
          "· sin texto:", sum(e["programa_id"] == "NO-ENCONTRADO" and not e["instrumento_texto"] for e in eq_rows))
    print("estado_corpus:", dict(Counter(r["estado_corpus_v1_1"].split(":")[0].split(" (")[0] for r in mapa)))
    print("cola:", len(cola_rows), "filas (dominio, programa)")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main("--verifica" in sys.argv))
