#!/usr/bin/env python3
"""ACTO GEN2-VALIDACION-Y-2027-1 · P1 · dictamen por identidad y asiento, con la regla de
LANZAMIENTO-VC1.md (commit anterior a revelar):

  sin punto de la reconstructora            → SOSTENER-SIN-CORROBORACION (sin fila en el libro);
                                              NO-RECALCULABLE-DESDE-SPEC → specs-insuficientes-v1_3.tsv (D-15)
  punto dentro de la tolerancia sellada      → SOSTENER · asiento PASA si compare_v3 dice COINCIDE,
                                              si no CONCUERDA-NO-APROBADA (IC diagnóstico R23, no adjudica)
  punto fuera                                → ACOTAR · asiento NO-PASA

Escribe (con --escribe): dictamen-vc1.tsv · ../specs-insuficientes-v1_3.tsv (v1_2 + filas nuevas) ·
append por línea a data/corrida0/validaciones-independientes.tsv (unicidad por (llave, validacion_ref)).
Uso: asienta.py [--escribe] <paq> [<paq> ...]   (sin paquetes: todos los que tengan comparacion/)
"""
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[3]
AQ = Path(__file__).resolve().parent
VI = AQ.parent
ROT = "VC1-CIEGA-POR-CONTEXTO-NUEVO"
LED = R / "data/corrida0/validaciones-independientes.tsv"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def lee(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def dictamina(paq):
    allow = json.loads((AQ / paq / "entrada" / f"{paq}--allowlist.json").read_text())
    calc = allow["calc"]
    cmp_ = AQ / paq / "comparacion" / f"{paq}--comparacion.json"
    aud = json.loads((AQ / paq / "comparacion" / f"{paq}--auditoria.json").read_text())["veredicto"]
    if not all(aud.values()):
        raise SystemExit(f"PARO · {paq}: auditoría del transcript no limpia {aud}; se dictamina aparte (RETROSPECTIVA-MECÁNICA)")
    rec = {f["llave"]: f for f in json.loads(
        (AQ / paq / "reconstructora" / f"{paq}--resultado.json").read_text())["filas"]}
    tol = allow["tolerancia_sellada"]
    filas, asientos, insuf = [], [], Counter()
    for r in json.loads(cmp_.read_text())["resultados"]:
        k = r["llave"]
        pt = r["campos"].get("punto", {})
        ic = ("dentro" if all(r["campos"].get(c, {}).get("dentro") for c in ("ic95_inf", "ic95_sup")) else "fuera") \
            if r["estado_ic_referencia"] == "CALCULADO" and r["estado_ic_actual"] == "CALCULADO" \
            else f"ref {r['estado_ic_referencia']} / rec {r['estado_ic_actual']}"
        f = {"llave": k, "calc": calc, "paquete": paq, "estado_comparador": r["estado"], "rotulo_ceguera": ROT,
             "ic": ic, "dictamen_ic_r23": "IC-DIAGNOSTICO-R23-NO-ADJUDICA"}
        if rec[k]["estado"] != "RECONSTRUIDO":
            f.update(punto="NO-COMPARADO", dictamen="SOSTENER-SIN-CORROBORACION", asiento="SIN-FILA",
                     motivo=f"reconstructora: {rec[k]['estado']}: {rec[k].get('motivo', '')[:200]}")
            if rec[k]["estado"] == "NO-RECALCULABLE-DESDE-SPEC":
                insuf[(calc, rec[k].get("motivo", "")[:300])] += 1
        else:
            dentro = bool(pt.get("dentro"))
            f["punto"] = "dentro" if dentro else f"fuera Δ={pt.get('delta')}"
            if dentro:
                est = "PASA" if r["estado"] == "COINCIDE" else "CONCUERDA-NO-APROBADA"
                f.update(dictamen="SOSTENER", asiento=est, motivo="punto dentro de la tolerancia sellada; IC diagnóstico R23")
            else:
                est = "NO-PASA"
                f.update(dictamen="ACOTAR", asiento=est, motivo="punto fuera de la tolerancia sellada")
            alc = (f"{ROT} tol abs={tol.get('abs')} rel=0 (tolerancia sellada en spec.yaml de {calc}): punto "
                   f"{'dentro' if dentro else 'fuera'} (Δ={pt.get('delta')}); IC {ic} — diagnóstico R23 sin margen, no adjudica; "
                   f"dictamen {f['dictamen']} (GEN2-VALIDACION-Y-2027-1; sesión nueva auditada por transcript, /tmp privado, "
                   f"Bash sin red; no es broker)")
            asientos.append((calc, k, est, cmp_, alc))
        filas.append(f)
    return filas, asientos, insuf


def main():
    escribe = "--escribe" in sys.argv
    paqs = [a for a in sys.argv[1:] if not a.startswith("--")] or sorted(
        p.name for p in AQ.iterdir() if (p / "comparacion").is_dir())
    todas, asientos, insuf = [], [], Counter()
    for paq in paqs:
        f, a, i = dictamina(paq)
        todas += f; asientos += a; insuf += i
        print(paq, dict(Counter(x["dictamen"] for x in f)), dict(Counter(x["asiento"] for x in f)))
    print("TOTAL", len(todas), dict(Counter(x["dictamen"] for x in todas)), dict(Counter(a[2] for a in asientos)))
    if not escribe:
        return
    cols = ["llave", "calc", "paquete", "estado_comparador", "rotulo_ceguera", "punto", "ic", "dictamen_ic_r23",
            "dictamen", "asiento", "motivo"]
    (AQ / "dictamen-vc1.tsv").write_text("\t".join(cols) + "\n" + "".join(
        "\t".join(str(f.get(c, "")).replace("\t", " ").replace("\n", " ") for c in cols) + "\n" for f in todas), encoding="utf-8")
    si = (VI / "specs-insuficientes-v1_2.tsv").read_text(encoding="utf-8")
    for (calc, motivo), n in sorted(insuf.items()):
        si += "\t".join([calc, "(llaves en dictamen-vc1.tsv con NO-RECALCULABLE-DESDE-SPEC)", "D15-SPEC-INSUFICIENTE",
                         motivo.replace("\t", " ").replace("\n", " "), "spec humana del CALC, versión sucesora", str(n),
                         "ADENDA-DE-SPEC", "GEN2-VALIDACION-Y-2027-1, <paq>--insuficiencias.md"]) + "\n"
    (VI / "specs-insuficientes-v1_3.tsv").write_text(si, encoding="utf-8")
    txt = LED.read_text(encoding="utf-8")
    if not txt.endswith("\n"):
        raise SystemExit("PARO · libro sin salto final")
    previas = lee(LED)
    ya = {(x["spec_id"], x["resultado_id"], x["validacion_ref"]) for x in previas}
    pasa = {(x["spec_id"], x["resultado_id"]) for x in previas if x["validacion_independiente"] == "PASA"}
    add = []
    for calc, k, est, ref, alc in asientos:
        if (calc, k) in pasa:
            continue
        rel = str(Path(ref).relative_to(R))
        if (calc, k, rel) in ya:
            raise SystemExit(f"PARO · asiento repetido {k}")
        add.append("\t".join([calc, k, est, rel, sha(ref), alc.replace("\t", " ")]) + "\n")
    LED.write_text(txt + "".join(add), encoding="utf-8")
    print("escrito ·", len(add), "filas nuevas en el libro")


if __name__ == "__main__":
    main()
