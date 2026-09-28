#!/usr/bin/env python3
"""ACTO GEN2-C1-SUCESORES-Y-LOTE-3 · P3. Dictamen por identidad de las 312 residuales y
asiento, aplicando mecánicamente la regla de LANZAMIENTO-LOTE3-RESIDUALES.md §4 (commit
1f089cc0, anterior a revelar). Escribe:
  dictamen-lote3-v1_1.tsv            404 filas (92 de v1 + columna dictamen_ic_r23; 312 nuevas)
  sucesoras-r26a.tsv                 identidades sucesoras ENBIARE (estimando cambiado por R26 a)
  ../specs-insuficientes-v1_2.tsv    v1_1 + filas nuevas (D-15)
  data/corrida0/validaciones-independientes.tsv   append por línea (llave, ref) nueva
Uso: asienta_residuales.py [--escribe]
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
ESCRIBE = "--escribe" in sys.argv
AB = {"enbiare-pisos-bienestar-0001": ("enbiare-l3r", "CALC-ENBIARE-PISOS-BIENESTAR-0001"),
      "encodat-pisos-sustancias-0001": ("encodat-l3r", "CALC-ENCODAT-PISOS-SUSTANCIAS-0001"),
      "encuci-0001": ("encuci-l3r", "CALC-ENCUCI-0001"),
      "enigh-0001": ("enigh-l3r", "CALC-ENIGH-0001")}
ROT = "C1-LOTE3-CIEGA-POR-CONTEXTO-NUEVO"
TOL = "tol abs=1e-10 rel=0 (tolerancia.json de lote 2 del paquete)"


def lee(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


PASA_PREVIO = {(x["spec_id"], x["resultado_id"]) for x in lee(R / "data/corrida0/validaciones-independientes.tsv")
               if x["validacion_independiente"] == "PASA" and "C1-SUCESORES" not in x["alcance_validacion"]}
lote2 = {x["llave"]: x["estado_punto"] for x in lee(VI / "catalogo-1-ejecucion-lote2/lote2-tabla-estimadores.tsv")}
v1 = lee(AQ / "dictamen-lote3.tsv")
cols = list(v1[0].keys()) + ["dictamen_ic_r23", "asiento", "identidad_sucesora"]
nuevas, suces, asientos = {}, [], []
for paq, (ab, calc) in AB.items():
    cmp_repo = AQ / paq / "comparacion" / f"{ab}--comparacion.json"
    if not cmp_repo.exists():
        raise SystemExit(f"PARO · falta {cmp_repo}")
    comp = json.loads(cmp_repo.read_text())
    ref_sha = sha(cmp_repo)
    rec = {f["llave"]: f for f in json.loads(
        (AQ / paq / "reconstructora/salida" / f"{ab}--resultado.json").read_text())["filas"]}
    for r in comp["resultados"]:
        k = r["llave"]
        pt = r["campos"].get("punto", {})
        ic = [r["campos"].get(c, {}).get("dentro") for c in ("ic95_inf", "ic95_sup")]
        ic_txt = ("dentro" if all(ic) else "fuera") if r["estado_ic_referencia"] == "CALCULADO" and r["estado_ic_actual"] == "CALCULADO" \
            else f"ref {r['estado_ic_referencia']} / rec {r['estado_ic_actual']}"
        grupo = "54" if paq.startswith("enbiare") and lote2.get(k) != "COINCIDE" else "cmp"
        f = {"llave": k, "calc": calc, "result_id": k, "paquete": paq, "gate": "LANZADO",
             "estado_comparador": r["estado"], "rotulo_ceguera": ROT,
             "dictamen_ic_r23": "IC-DIAGNOSTICO-R23-NO-ADJUDICA", "identidad_sucesora": "", "asiento": ""}
        if rec[k]["estado"] != "RECONSTRUIDO":
            f.update(punto="NO-COMPARADO", ic="NO-COMPARADO", dictamen="SOSTENER-SIN-CORROBORACION",
                     motivo=f"reconstructora: {rec[k]['estado']} (D-15: esquema pide unidad proporcion; la spec define media 0-10)")
            if grupo == "cmp":
                f["asiento"] = "CONCUERDA-NO-APROBADA (R28, rótulo NO-CIEGA-PENDIENTE: la re-comparación ciega no produjo punto)"
                asientos.append((calc, k, "CONCUERDA-NO-APROBADA", VI / "catalogo-1-sucesores/r28-130-no-ciegas.tsv",
                                 f"C1-LOTE2 NO-CIEGA-PENDIENTE (R28, FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-04): la re-comparación ciega del lote 3 (GEN2-C1-SUCESORES-Y-LOTE-3) no produjo punto: NO-RECALCULABLE-DESDE-SPEC por unidad proporcion frente a media 0-10 (D-15)"))
        elif grupo == "54":
            f.update(punto=("dentro" if pt.get("dentro") else f"fuera Δ={pt.get('delta')}"), ic=ic_txt,
                     dictamen="SOSTENER-SIN-CORROBORACION", identidad_sucesora=f"{k}--R26A",
                     motivo="estimando cambiado por firma R26 (a) (EDAD=98 fuera de tramos/CESD-7; 97/99 fuera del universo): comparación solo diagnóstica; el valor es de la identidad sucesora")
            suces.append({"identidad_sucesora": f"{k}--R26A", "llave_historica": k, "calc_historico": calc,
                          "punto": rec[k]["punto"], "estado_ic": rec[k].get("estado_ic", ""),
                          "ic95_inf": rec[k].get("ic95_inf", ""), "ic95_sup": rec[k].get("ic95_sup", ""),
                          "contrato": "R26 (a) sha 95f614a4…d67d + (b) diagnóstico", "fuente": str(cmp_repo.relative_to(R))})
        else:
            dentro = bool(pt.get("dentro"))
            f.update(punto="dentro" if dentro else f"fuera Δ={pt.get('delta')}", ic=ic_txt)
            if dentro:
                f.update(dictamen="SOSTENER", motivo="punto dentro de tolerancia; IC diagnóstico R23 (otra semilla/receta por R26 b), no adjudica")
                est = "PASA" if r["estado"] == "COINCIDE" else "CONCUERDA-NO-APROBADA"
            else:
                f.update(dictamen="ACOTAR", motivo="CESD-7: R26 (a) excluye EDAD=98 de CESD-7 en todos los ejes (decisión D03 sellada por la reconstructora); el sellado lo incluía: cambio de estimando firmado, no fallo de reproducción")
                est = "NO-PASA"
            f["asiento"] = est if (calc, k) not in PASA_PREVIO else \
                "SIN-FILA-NUEVA: PASA vigente de GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS; esta comparación ciega concuerda en punto"
            asientos.append((calc, k, est, cmp_repo,
                             f"{ROT} {TOL}: punto {'dentro' if dentro else 'fuera'} (Δ={pt.get('delta')}); IC {ic_txt} — diagnóstico R23 sin margen, no adjudica; dictamen {f['dictamen']} (GEN2-C1-SUCESORES-Y-LOTE-3; sesión nueva auditada por transcript, /tmp privado, Bash sin red; no es broker)"))
        nuevas[k] = f
if len(nuevas) != 312:
    raise SystemExit(f"PARO · {len(nuevas)} llaves, no 312")
filas = []
for x in v1:
    if x["llave"] in nuevas:
        n = dict(x); n.update(nuevas[x["llave"]]); filas.append(n)
    else:
        n = dict(x, dictamen_ic_r23="IC-DIAGNOSTICO-R23-NO-ADJUDICA", asiento="NO-PASA (tabla, C1-LOTE-3; se sostiene)", identidad_sucesora="")
        filas.append(n)
if {f["llave"] for f in filas} != {x["llave"] for x in v1} or len(filas) != 404:
    raise SystemExit("PARO · universo v1 ≠ v1_1")
print("dictamen", dict(Counter(f["dictamen"] for f in filas)))
print("asientos", dict(Counter(a[2] for a in asientos)), "· sucesoras", len(suces))

if ESCRIBE:
    t = lambda cs, fs: "\t".join(cs) + "\n" + "".join("\t".join(str(f.get(c, "")) for c in cs) + "\n" for f in fs)
    (AQ / "dictamen-lote3-v1_1.tsv").write_text(t(cols, filas), encoding="utf-8")
    (AQ / "sucesoras-r26a.tsv").write_text(t(list(suces[0].keys()), suces), encoding="utf-8")
    si = (VI / "specs-insuficientes-v1_1.tsv").read_text(encoding="utf-8")
    llaves90 = sum(1 for f in filas if f["punto"] == "NO-COMPARADO" and f["gate"] == "LANZADO")
    si += "\t".join(["CALC-ENBIARE-PISOS-BIENESTAR-0001", "RESULT-ENBIARE-PISOS-BIENESTAR-*-{PA1,PA5,PB1_01,PB1_02,PB1_04,PB1_11}-P",
                     "D15-UNIDAD-CONTRADICTORIA",
                     "unidad de seis escalas 0-10 (satisfacción, Cantril, confianza ×4): el esquema del paquete y la llave (-P) dicen proporcion; enbiare-metodo-base.md §4 y residuales-p3-modulos-ic.md dicen media 0-10; ninguna spec fija dicotomización",
                     "spec humana ENBIARE (metodo-base) o esquema-identidades del contenedor, versión sucesora",
                     str(llaves90), "ADENDA-DE-SPEC",
                     "GEN2-C1-SUCESORES-Y-LOTE-3, enbiare-l3r--insuficiencias.md §1"]) + "\n"
    (VI / "specs-insuficientes-v1_2.tsv").write_text(si, encoding="utf-8")
    led = R / "data/corrida0/validaciones-independientes.tsv"
    ya = {(x["spec_id"], x["resultado_id"], x["validacion_ref"]) for x in lee(led)}
    txt = led.read_text(encoding="utf-8")
    if not txt.endswith("\n"):
        raise SystemExit("PARO · libro sin salto final")
    pasa = {(x["spec_id"], x["resultado_id"]) for x in lee(led) if x["validacion_independiente"] == "PASA"}
    add = []
    for calc, k, est, ref, alc in asientos:
        if (calc, k) in pasa:  # no se tapa un PASA de otra validación (no se colapsan)
            print("sin fila nueva: PASA previo de otra validación ·", k)
            continue
        rel = str(Path(ref).relative_to(R))
        if (calc, k, rel) in ya:
            raise SystemExit(f"PARO · asiento repetido {k} {rel}")
        if "\t" in alc:
            raise SystemExit("PARO · tab en alcance")
        add.append("\t".join([calc, k, est, rel, sha(ref), alc]) + "\n")
    led.write_text(txt + "".join(add), encoding="utf-8")
    print("escrito ·", len(add), "filas nuevas en el libro")
