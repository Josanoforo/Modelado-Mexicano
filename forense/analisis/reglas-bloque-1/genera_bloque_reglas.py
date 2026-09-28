#!/usr/bin/env python3
"""Bloque de adopción de reglas 1 (ACTO GEN2-CIERRE-Y-PRODUCTO-3, P2).

Deriva, sin teclear una cifra, desde `canon/reglas-contrastadas-v1_1.tsv`:

  canon/reglas-bloque-adopcion-1.tsv   una fila por regla del bloque (CONFIRMA con tier
                                       evidenciado ≥ media; variantes fundidas en su regla madre)
  canon/reglas-bloque-adopcion-1.md    portada: el bloque, el destino de las 162 reglas y el
                                       texto de firma
  forense/analisis/reglas-bloque-1/destino-reglas-v1_0.tsv   destino de cada regla

Formato de ADOPCION-BLOQUE-Y-PINES-1 y del bloque candidato de GEN2-REGLAS-Y-RESULT-1
(regla_id con fuentes fundidas · regla · RESULT · punto [IC95] · unidad · tier · implica).
Cada `resultado_id` se re-lee de su CALC sellado (sello.sha256 → resultados.json): si el
punto no coincide, falla. La adopción es el merge de mesa (E.2); este derivador no escribe
`milpa/tramite.yaml` (lo escribe el escritor de relevo, y solo tras la decisión del criterio
de CONFIRMA, FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01).

Uso:  python3 forense/analisis/reglas-bloque-1/genera_bloque_reglas.py [--verifica]
"""
from __future__ import annotations

import csv
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
FUENTE = ROOT / "canon/reglas-contrastadas-v1_1.tsv"
TSV = ROOT / "canon/reglas-bloque-adopcion-1.tsv"
MD = ROOT / "canon/reglas-bloque-adopcion-1.md"
DESTINO = ROOT / "forense/analisis/reglas-bloque-1/destino-reglas-v1_0.tsv"
CORRIDA = ROOT / "data/corrida0"
FP_CRITERIO = "FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01"
TIER_ORDEN = {"narrativa popular": 0, "hipótesis razonable": 1, "media": 2, "fuerte": 3}
csv.field_size_limit(sys.maxsize)

CAMPOS = ["regla_id", "variantes_fundidas", "texto", "segmento_si", "conducta_entonces", "driver_porque",
          "resultado_id", "calc", "punto", "ic95_inf", "ic95_sup", "unidad", "tier_declarado",
          "tier_evidenciado", "procedencia", "firewall_genetico", "temporalidad", "report", "estado_bloque"]


def lee(p: pathlib.Path) -> list[dict]:
    with p.open(newline="", encoding="utf-8") as s:
        return list(csv.DictReader((l for l in s if not l.startswith("#")), delimiter="\t"))


def texto_tsv(campos, filas) -> str:
    import io
    b = io.StringIO()
    w = csv.DictWriter(b, fieldnames=campos, delimiter="\t", lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    w.writerows(filas)
    return b.getvalue()


def sellado(calc: str, rid: str):
    """Valor del RESULT leído por la cadena sello.sha256 → sello.json → resultados.json (falla si no casa)."""
    sys.path.insert(0, str(ROOT / "forense/analisis/catalogo"))
    sys.path.insert(0, str(ROOT / "tools"))
    from genera_catalogo import verified  # noqa: PLC0415
    return verified(calc)[0].get(rid)


def madre(r: dict) -> str:
    m = re.search(r"VARIANTE-DE[: ]+(RG-[0-9a-f]+)", r.get("detalle_dictamen", "") + " " + r.get("rp_id", ""))
    return m.group(1) if m else ""


def destino(r: dict) -> str:
    d = r["dictamen"]
    if d == "CONFIRMA":
        return ("BLOQUE" if TIER_ORDEN.get(r["tier_evidenciado"], -1) >= TIER_ORDEN["media"]
                else "FUERA-DEL-BLOQUE:TIER-EVIDENCIADO-BAJO-MEDIA")
    if d.startswith("MATIZA"):
        return "REPORT-V3:MATIZ-CON-CIFRA" if r["resultado_id"] else "PROPUESTA:MATIZA-SIN-RESULT"
    if d == "ROMPE":
        return "REPORT-V3:CORRECCION"
    return "PROPUESTA:SIN-CIFRA (instrumento pendiente: " + (r["instrumento_sugerido"] or "SIN-SUGERENCIA")[:60] + ")"


def filas():
    R = lee(FUENTE)
    dest = [{"regla_id": r["regla_id"], "dictamen": r["dictamen"], "tier_evidenciado": r["tier_evidenciado"],
             "procedencia": r["procedencia"], "resultado_id": r["resultado_id"], "report": r["fuentes"],
             "destino": destino(r)} for r in R]
    bloque = {}
    confirma = [r for r in R if destino(r) == "BLOQUE"]
    # variante fundida: misma RESULT y mismo dictamen que una regla madre de origen REPORT-V2/V1
    por_rid = {}
    for r in confirma:
        por_rid.setdefault(r["resultado_id"], []).append(r)
    for rid, grupo in sorted(por_rid.items()):
        grupo.sort(key=lambda r: (r["origen"] == "TABLA-C3-1", r["regla_id"]))
        m = grupo[0]
        v = sellado(m["calc"], rid)
        if v is None or abs(float(v) - float(m["punto"])) > 1e-12:
            raise SystemExit(f"punto de {m['regla_id']} no coincide con su RESULT sellado {rid}")
        bloque[m["regla_id"]] = {**m, "variantes_fundidas": ";".join(r["regla_id"] for r in grupo[1:]),
                                 "report": m["fuentes"],
                                 "estado_bloque": f"CANDIDATO · condicional al criterio de CONFIRMA ({FP_CRITERIO})"}
    return list(bloque.values()), dest


def regla(texto: str) -> str:
    """Primer campo no vacío del texto de la regla (el TSV fuente trae celdas de tabla markdown pegadas)."""
    return next((t.strip() for t in texto.split("|") if t.strip()), "").replace("|", "/")


def md(bloque, dest) -> str:
    c = Counter(d["destino"].split(" ")[0].split(":")[0] + (":" + d["destino"].split(":")[1].split(" ")[0]
                                                               if ":" in d["destino"] else "") for d in dest)
    L = ["# Bloque de adopción de reglas · 1 · ACTO GEN2-CIERRE-Y-PRODUCTO-3",
         "",
         f"Derivado de `canon/reglas-contrastadas-v1_1.tsv` ({len(dest)} reglas) con "
         "`python3 forense/analisis/reglas-bloque-1/genera_bloque_reglas.py`. Cero cifras tecleadas: cada punto se "
         "re-lee de su CALC sellado. Todo RETROSPECTIVO (olas vistas); ninguna regla se valida prospectivamente aquí.",
         "",
         "**Cómo se adopta.** El merge de mesa del PR que trae este archivo es la adopción del bloque (E.2), "
         f"condicional a la decisión pendiente sobre el criterio de CONFIRMA (`{FP_CRITERIO}`, ABIERTA): si CONFIRMA "
         "cubre la conducta descriptiva, el bloque es el de abajo; si exige la regla completa (SI+ENTONCES+PORQUE), "
         "la regla pasa a MATIZA y el bloque queda vacío. Adoptar no escribe `milpa/tramite.yaml`: la regla viva la "
         "escribe el escritor de relevo tras esa decisión (NC de este acto).",
         "",
         "## 1 · El bloque (CONFIRMA con tier evidenciado ≥ media)",
         "",
         "| regla_id (variantes fundidas) | regla (verbatim, primer campo del texto) | RESULT · punto [IC95] · unidad | tier declarado → evidenciado | procedencia | firewall |",
         "|---|---|---|---|---|---|"]
    for b in bloque:
        L.append(f"| `{b['regla_id']}` ({b['variantes_fundidas'] or '—'}) | {regla(b['texto'])} | `{b['resultado_id']}` · {float(b['punto']):.3f} "
                 f"[{float(b['ic95_inf']):.3f}, {float(b['ic95_sup']):.3f}] · {b['unidad']} | "
                 f"{b['tier_declarado'] or '—'} → {b['tier_evidenciado']} | {b['procedencia']} | {b['firewall_genetico'] or 'NO-APLICA'} |")
    L += ["", "Se adopta la **conducta descriptiva** (SI), no el ENTONCES prescriptivo ni el PORQUE: el driver no se "
          "identifica con un marginal descriptivo (A-bis: co-observación no es identificación).",
          "", "## 2 · Destino de las reglas", "", "| destino | filas de regla |", "|---|---:|"]
    for k, n in sorted(c.items()):
        L.append(f"| `{k}` | {n} |")
    L += ["",
          f"- `BLOQUE`: {sum(1 for d in dest if d['destino'] == 'BLOQUE')} filas = {len(bloque)} regla(s) madre con sus variantes fundidas.",
          "- `FUERA-DEL-BLOQUE:TIER-EVIDENCIADO-BAJO-MEDIA`: CONFIRMA cuya evidencia no pasa de hipótesis razonable "
          "(una ola, contraste rural−urbano sin identificar el driver). Siguen PROPUESTA.",
          "- `REPORT-V3:MATIZ-CON-CIFRA`: la regla se reescribe en su report v3 con el matiz y la cifra (P4).",
          "- `PROPUESTA:SIN-CIFRA`: quedan PROPUESTA con su instrumento pendiente (columna `instrumento_sugerido`).",
          "- ROMPE: ninguna regla.",
          "", "Destino por regla: `forense/analisis/reglas-bloque-1/destino-reglas-v1_0.tsv`.",
          "", "## 3 · Texto de firma (listo para mesa)", "",
          "«Mesa adopta el bloque 1 de reglas de GEN2-CIERRE-Y-PRODUCTO-3 como regla descriptiva de conducta "
          "(SI), sin adoptar su ENTONCES ni su PORQUE, si y solo si el criterio de CONFIRMA de "
          f"{FP_CRITERIO} cubre la conducta descriptiva.»", ""]
    return "\n".join(L)


def main(argv) -> int:
    bloque, dest = filas()
    salidas = {TSV: texto_tsv(CAMPOS, bloque),
               DESTINO: texto_tsv(list(dest[0].keys()), dest),
               MD: md(bloque, dest)}
    if "--verifica" in argv:
        malos = [str(p) for p, t in salidas.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
        print("COINCIDE" if not malos else "DIFIERE " + " ".join(malos))
        return 1 if malos else 0
    for p, t in salidas.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(t, encoding="utf-8")
    print(f"bloque={len(bloque)} reglas={len(dest)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
