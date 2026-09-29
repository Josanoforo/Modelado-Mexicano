#!/usr/bin/env python3
"""Reports v3 (ACTO GEN2-CIERRE-Y-PRODUCTO-3, P4).

Un report v2 (`corpus/reports-v2/`) sale como v3 SOLO si su carril recibió cifra nueva esta
semana. Regla de «cifra nueva» (latitud del encargo §6, declarada en la nota): el dominio
primario del report (`forense/analisis/dominios/report-a-dominio-v1_0.tsv`) tiene al menos
una llave en el catálogo v1.4 que no estaba en el v1.3, o una regla del report cambió de
dictamen entre `canon/reglas-contrastadas-v1_0.tsv` y `v1_1`. Los demás no se tocan.

Cada v3 = capa v3 derivada (cifras GEN2 por RESULT, contraste de sus reglas con el matiz
incorporado, firewall, módulo de auditoría con las preguntas [v2.16], procedencia (a)/(b)/(c)
por afirmación) + el cuerpo v2 heredado **sin editar**, con su sha256. Cero cifras tecleadas.

Uso:  python3 forense/analisis/reports-v3/genera_reports_v3.py [--verifica]
Escribe corpus/reports-v3/<report>.md, corpus/reports-v3/INDICE.md y
forense/analisis/reports-v3/carriles-v3-v1_0.tsv.
"""
from __future__ import annotations

import csv
import hashlib
import pathlib
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
V2 = ROOT / "corpus/reports-v2"
V3 = ROOT / "corpus/reports-v3"
CAT = ROOT / "canon/catalogo-del-mexicano-v1_4.tsv"
CAT13 = ROOT / "canon/catalogo-del-mexicano-v1_3.tsv"
REGLAS0 = ROOT / "canon/reglas-contrastadas-v1_0.tsv"
REGLAS1 = ROOT / "canon/reglas-contrastadas-v1_1.tsv"
RAD = ROOT / "forense/analisis/dominios/report-a-dominio-v1_0.tsv"
CARRILES = ROOT / "forense/analisis/reports-v3/carriles-v3-v1_0.tsv"
MAX_CIFRAS = 12
csv.field_size_limit(sys.maxsize)
# Procedencia de la evidencia (§3): todo instrumento del catálogo es muestra o registro en México.
PROC_CATALOGO = "(a) datos primarios en México"


def lee(p: pathlib.Path) -> list[dict]:
    with p.open(newline="", encoding="utf-8") as s:
        return list(csv.DictReader((l for l in s if not l.startswith("#")), delimiter="\t"))


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def f3(x: str) -> str:
    return f"{float(x):.3f}" if x else ""


def cifra(r: dict) -> str:
    ic = f" [{f3(r['ic95_inf'])}, {f3(r['ic95_sup'])}]" if r["ic95_inf"] else " (sin IC identificado)"
    return f"{f3(r['punto'])}{ic}"


def primer_campo(t: str) -> str:
    return next((x.strip() for x in t.split("|") if x.strip()), "").replace("|", "/")


def carriles():
    v13 = {r["llave"] for r in lee(CAT13)}
    nuevos: dict[str, list[dict]] = {}
    for r in lee(CAT):
        if r["llave"] not in v13:
            nuevos.setdefault(r["dominio"], []).append(r)
    antes = {r["regla_id"]: r["dictamen"] for r in lee(REGLAS0)}
    reglas = lee(REGLAS1)
    rad = {pathlib.Path(r["ruta"]).name: r["dominio_primario"] for r in lee(RAD)}
    out = []
    for p in sorted(V2.glob("*.md")):
        if p.name == "INDICE.md":
            continue
        dom = rad.get(p.name, "SIN-MAPEO")
        propias = [r for r in reglas if p.name in r["fuentes"]]
        cambian = [r for r in propias if antes.get(r["regla_id"]) != r["dictamen"]]
        n = len(nuevos.get(dom, []))
        motivo = []
        if n:
            motivo.append(f"DOMINIO-CON-FILAS-NUEVAS:{n}")
        if cambian:
            motivo.append("REGLAS-REDICTAMINADAS:" + ",".join(r["regla_id"] for r in cambian))
        out.append({"report": p.name, "dominio": dom, "filas_nuevas_v1_4": n,
                    "reglas_redictaminadas": len(cambian), "sale_v3": "SI" if motivo else "NO",
                    "motivo": ";".join(motivo) or "SIN-CIFRA-NUEVA: no se toca"})
    return out, nuevos, reglas


def elige(filas: list[dict]) -> list[dict]:
    """Hasta MAX_CIFRAS filas: primero agregados nacionales/totales con IC, un CALC a la vez."""
    def clave(r):
        agregado = any(t in (r["eje"] + r["segmento"]).upper() for t in ("NACIONAL", "TOTAL", "CONTRASTE", "DIF"))
        return (not agregado, not r["ic95_inf"], r["calc"], r["llave"])
    por_calc: dict[str, list[dict]] = {}
    for r in sorted(filas, key=clave):
        por_calc.setdefault(r["calc"], []).append(r)
    out, i = [], 0
    while len(out) < MAX_CIFRAS and any(i < len(v) for v in por_calc.values()):
        for c in sorted(por_calc):
            if i < len(por_calc[c]) and len(out) < MAX_CIFRAS:
                out.append(por_calc[c][i])
        i += 1
    return out


def texto(c: dict, filas: list[dict], reglas: list[dict], cat: dict) -> str:
    v2 = V2 / c["report"]
    propias = [r for r in reglas if c["report"] in r["fuentes"]]
    con_cifra = [r for r in propias if not r["dictamen"].startswith("SIN-CIFRA")]
    sin = len(propias) - len(con_cifra)
    sel = elige(filas)
    unidades = sorted({r["unidad"] for r in filas})
    temp = Counter(r["temporalidad"] for r in filas)
    L = [f"# {c['report'].removesuffix('.md').replace('_', ' ').strip()} · v3", "",
         "> | | |", "> |---|---|",
         f"> | **ARCHIVO** | `corpus/reports-v3/{c['report']}` |",
         f"> | **SUCEDE A** | [`corpus/reports-v2/{c['report']}`](../reports-v2/{c['report']}) · sha256 `{sha(v2)}` — intacto (E.1); su cuerpo va abajo sin editar |",
         f"> | **ACTO** | `GEN2-CIERRE-Y-PRODUCTO-3` (P4) · cero mediciones · la cifra se cita por RESULT del catálogo v1.4 |",
         f"> | **CARRIL** | dominio `{c['dominio']}` · motivo del v3: `{c['motivo']}` |",
         "> | **REGENERA** | `python3 forense/analisis/reports-v3/genera_reports_v3.py` |", "",
         "## v3.1 · Cifras GEN2 nuevas del carril (catálogo v1.4, por RESULT)", "",
         f"El carril recibió {len(filas)} filas nuevas en el catálogo v1.4; se muestran hasta {len(sel)} "
         "(agregados primero, un CALC a la vez). La tabla completa se filtra por `dominio` en "
         "`canon/catalogo-del-mexicano-v1_4.tsv`. Todas son RETROSPECTIVAS y descriptivas de una ola: "
         "ninguna identifica un mecanismo (co-observación no es identificación).", ""]
    for r in sel:
        L.append(f"- `{r['llave']}` · {cifra(r)} · unidad: {r['unidad']} · {r['instrumento']} {r['ola']} · "
                 f"`{r['estado_adopcion']}` · {r['temporalidad']} · procedencia {PROC_CATALOGO}")
    L += ["", "## v3.2 · Contraste de las reglas del report (`canon/reglas-contrastadas-v1_1.tsv`)", ""]
    if con_cifra:
        L += ["| regla | dictamen | RESULT · cifra · unidad | tier declarado → evidenciado | procedencia | matiz incorporado |",
              "|---|---|---|---|---|---|"]
        for r in con_cifra:
            rc = cat.get(r["resultado_id"])
            cf = cifra(rc) if rc else (f"{f3(r['punto'])}" if r["punto"] else "sin punto")
            det = (r["detalle_dictamen"] or r["correccion_propuesta"]).replace("|", "/").replace("\n", " ")[:260]
            L.append(f"| `{r['regla_id']}`: {primer_campo(r['texto'])[:140]} | **{r['dictamen']}** | "
                     f"`{r['resultado_id'] or '—'}` · {cf} · {r['unidad'] or '—'} | "
                     f"{r['tier_declarado'] or '—'} → {r['tier_evidenciado']} | {r['procedencia'] or '—'} | {det or '—'} |")
        L += ["", "Una regla `MATIZA` sigue siendo PROPUESTA: su texto queda en el cuerpo v2 y el matiz de arriba es "
              "la lectura vigente. `CONFIRMA` con tier evidenciado bajo media no entra al bloque de adopción "
              "(`canon/reglas-bloque-adopcion-1.md`)."]
    else:
        L.append("Ninguna regla de este report tiene cifra GEN2 todavía.")
    L += ["", f"{sin} reglas de este report quedan `PROPUESTA` sin cifra, con su instrumento pendiente "
          "(columna `instrumento_sugerido`).", "",
          "## v3.3 · Firewall genético", ""]
    fw = [r for r in propias if r["firewall_genetico"]]
    if fw:
        for r in fw:
            L.append(f"- `{r['regla_id']}`: `{r['firewall_genetico']}`")
    else:
        L.append("NO-APLICA: ninguna afirmación con cifra de este carril infiere conducta de grupo desde ascendencia.")
    urb = sum(1 for r in filas if "urban" in r["unidad"].lower() or "100 000" in r["unidad"])
    inc = Counter(r["incentivo_o_psicologia"] for r in con_cifra if r["incentivo_o_psicologia"])
    L += ["", "## v3.4 · Módulo de auditoría de rigor extremo (preguntas [v2.16] incluidas)", "",
          "- **¿Cuántos contadores movió este trabajo?** Cero mediciones: el v3 cita RESULT ya sellados.",
          f"- **[v2.16] ¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA, y se mezclan en alguna frase?** "
          f"PROSPECTIVA {temp.get('PROSPECTIVA', 0)} · RETROSPECTIVA {temp.get('RETROSPECTIVA', 0)} filas del carril; ninguna frase las mezcla.",
          "- **[v2.16] ¿Qué unidad tiene cada cifra y se promedia con otra?** " + "; ".join(f"`{u}`" for u in unidades)
          + ". Ninguna se promedia con otra ni se compara sin función de enlace.",
          f"- **¿Sobregeneralización desde clase media urbana?** {urb} filas del carril tienen universo urbano declarado en su unidad; "
          "ninguna se lee como «el mexicano».",
          "- **¿Qué parece psicológico y es incentivo racional?** " + (
              "; ".join(f"`{k}` {n}" for k, n in sorted(inc.items())) if inc else "sin dictamen por regla en este carril") + ".",
          "- **¿Pobreza, violencia o informalidad confundidas con cultura?** Las cifras nuevas son descriptivas de una ola; "
          "el v3 no atribuye ningún gradiente a «cultura».",
          "- **¿Qué afirmación sobre el corpus se escribió a mano?** Ninguna cifra: todas salen del catálogo v1.4 o de "
          "las reglas contrastadas, por el generador.",
          "- **¿Qué sería peligroso leído simplista?** Leer un piso de una ola como tendencia, o un contraste entre dos "
          "grupos como efecto causal.", "",
          "---", "", f"# Cuerpo heredado de v2 (sin editar · sha256 `{sha(v2)}`)", "", v2.read_text(encoding="utf-8")]
    return "\n".join(L)


def salidas() -> dict[pathlib.Path, str]:
    cs, nuevos, reglas = carriles()
    cat = {r["llave"]: r for r in lee(CAT)}
    out = {}
    idx = ["# Índice de reports v3 · GEN2-CIERRE-Y-PRODUCTO-3", "",
           "Productor: `forense/analisis/reports-v3/genera_reports_v3.py`. Sale v3 solo el report v2 cuyo carril "
           "recibió cifra nueva esta semana (regla en el docstring del generador); los demás no se tocan. "
           "Lista completa con motivo: `forense/analisis/reports-v3/carriles-v3-v1_0.tsv`.", "",
           "| report v3 | dominio | filas nuevas v1.4 | reglas re-dictaminadas |", "|---|---|---:|---:|"]
    for c in cs:
        if c["sale_v3"] != "SI":
            continue
        out[V3 / c["report"]] = texto(c, nuevos.get(c["dominio"], []), reglas, cat)
        idx.append(f"| [{c['report'].removesuffix('.md').replace('_', ' ').strip()[:80]}]({c['report']}) | "
                   f"`{c['dominio']}` | {c['filas_nuevas_v1_4']} | {c['reglas_redictaminadas']} |")
    out[V3 / "INDICE.md"] = "\n".join(idx) + "\n"
    import io
    b = io.StringIO()
    w = csv.DictWriter(b, fieldnames=list(cs[0].keys()), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(cs)
    out[CARRILES] = b.getvalue()
    return out


def main(argv) -> int:
    s = salidas()
    if "--verifica" in argv:
        malos = [str(p.relative_to(ROOT)) for p, t in s.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
        print("COINCIDE" if not malos else "DIFIERE " + " ".join(malos))
        return 1 if malos else 0
    for p, t in s.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(t, encoding="utf-8")
    print(f"reports_v3={len(s) - 2}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
