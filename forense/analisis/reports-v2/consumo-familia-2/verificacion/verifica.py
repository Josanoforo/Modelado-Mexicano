#!/usr/bin/env python3
"""Regresiones C3 materiales y trazabilidad; no decide epistemología por contenido no vacío."""
import argparse
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
LIVE = ROOT / "forense/analisis/reports-v2/consumo-familia-1"
NEW = HERE.parent
FIVE = ("ASTRA5-U0-FAM-022", "ASTRA5-U0-FAM-045", "FAM-FUERA-L187", "FAM-FUERA-L189", "FAM-FUERA-L193")


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


legacy = module("control_anterior", LIVE / "verifica_lote.py")
consulta = module("consulta", ROOT / "tools/consulta.py")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def regressions(consumo, familia):
    errors = []
    fam = {r["id"]: r for r in familia}
    con = {r["id"]: r for r in consumo}
    for cid in FIVE:
        row = fam.get(cid, {})
        if row.get("dictamen") != "SIN-CIFRA" or not row.get("razon_sin_cifra"):
            errors.append(cid + ": ausencia no es evidencia contraria")
    zeiders = fam.get("ASTRA5-U0-FAM-001", {})
    if zeiders.get("dictamen") != "ROMPE" or zeiders.get("tipo_evidencia") != "correccion_bibliografica" or "F-ZEIDERS" not in zeiders.get("referencias", []):
        errors.append("Zeiders: corregir bibliografía con primaria, sin exigir RESULT propio")
    if zeiders.get("result_ids"):
        errors.append("Zeiders: corrección bibliográfica confundida con medición propia")
    clauses = {r["id"]: r for r in con.get("CONS-V1-L086", {}).get("clausulas", [])}
    for cid in ("L086-GASTO", "L086-TARJETA", "L086-BANCARIZACION", "L086-ESTRUCTURA"):
        if cid not in clauses: errors.append("L086: falta cláusula " + cid)
    gasto = clauses.get("L086-GASTO", {})
    if gasto.get("dictamen") != "MATIZA" or len(gasto.get("evidencia_ids", [])) < 4:
        errors.append("L086: gasto/deciles requieren evidencia diferenciada ENIGH2022")
    for cid in ("L086-BANCARIZACION", "L086-ESTRUCTURA"):
        if clauses.get(cid, {}).get("dictamen") != "SIN-CIFRA": errors.append(cid + ": cifra de gasto no confirma mecanismo")
    clauses = {r["id"]: r for r in con.get("ASTRA5-U0-CONS-024", {}).get("clausulas", [])}
    if clauses.get("CONS024-DESCRIPTIVA", {}).get("dictamen") != "MATIZA" or not clauses.get("CONS024-DESCRIPTIVA", {}).get("evidencia_ids"):
        errors.append("CONS024: descripción regional requiere RESULT y límites")
    if clauses.get("CONS024-CAUSAL", {}).get("dictamen") != "SIN-CIFRA":
        errors.append("CONS024: descripción no identifica exposición estadounidense")
    return errors


def mutation_tests(consumo, familia):
    cases = []
    for cid in FIVE:
        changed = copy.deepcopy(familia)
        next(r for r in changed if r["id"] == cid)["dictamen"] = "ROMPE"
        cases.append((cid, consumo, changed))
    for parent, clause in (("CONS-V1-L086", "L086-BANCARIZACION"), ("CONS-V1-L086", "L086-ESTRUCTURA"), ("ASTRA5-U0-CONS-024", "CONS024-CAUSAL")):
        changed = copy.deepcopy(consumo)
        row = next(r for r in changed if r["id"] == parent)
        next(r for r in row["clausulas"] if r["id"] == clause)["dictamen"] = "CONFIRMA"
        cases.append((clause, changed, familia))
    for label, con, fam in cases:
        assert regressions(con, fam), "Mutación no detectada: " + label
    number = next(n for n in load(LIVE / "consumo/consumo-cifras.json") if n.get("tipo") == "externa")
    sources = {s["id"]: s for s in load(LIVE / "consumo/consumo-fuentes.json")}
    assert not validate_external(number, sources), "Fuente real no habilita cifra externa"
    mutated = copy.deepcopy(sources)
    mutated[number["fuente_id"]]["estado_acceso_sucesor"] = "BLOQUEADA; cifra no verificada"
    assert validate_external(number, mutated), "Cifra habilitada por primaria inaccesible no rechazada"
    return [label for label, _, _ in cases] + ["externa-inaccesible"]


def inaccessible(origin):
    state = str(origin.get("estado_acceso_sucesor", origin.get("estado_acceso", origin.get("acceso", "")))).upper()
    return any(word in state for word in ("BLOQUE", "INACCES", "NO-VERIFIC", "NO_VERIFIC"))


def validate_external(number, sources):
    origin = sources.get(number.get("fuente_id"), {})
    return [number["id"] + ": cifra externa afirmativa con fuente inaccesible"] if inaccessible(origin) else []


def verify():
    errors, counts = legacy.verify()
    claims = {lane: load(LIVE / lane / (lane + "-afirmaciones.json")) for lane in legacy.REPORTS}
    errors.extend(regressions(claims["consumo"], claims["familia"]))
    evidence = []
    for lane in legacy.REPORTS:
        source = NEW / lane / (lane + "-juicios.json")
        if not source.exists() or (load(source).get("juicios") if isinstance(load(source), dict) else load(source)) != claims[lane]:
            errors.append(lane + ": tabla derivada difiere de fuente explícita")
        numbers = load(LIVE / lane / (lane + "-cifras.json"))
        known = {n["id"] for n in numbers} | {n.get("result_id") for n in numbers} | {s["id"] for s in load(LIVE / lane / (lane + "-fuentes.json"))}
        for claim in claims[lane]:
            for clause in claim.get("clausulas", []) + claim.get("componentes", []):
                for eid in clause.get("evidencia_ids", []) + clause.get("result_ids", []) + clause.get("referencias", []):
                    if eid not in known: errors.append(claim["id"] + ": evidencia desconocida en cláusula " + eid)
        for number in numbers:
            if number.get("tipo") == "externa":
                sources = {r["id"]: r for r in load(LIVE / lane / (lane + "-fuentes.json"))}
                # Una fuente con acceso fallido nunca habilita cifra afirmativa.
                errors.extend(validate_external(number, sources))
                continue
            rid = number["result_id"]
            row, _ = consulta.busca_tsv(consulta.RESULTADOS, "resultado_id", rid)
            if row is None:
                # Registro publicado puede ir detrás del sello; el control
                # legado verifica identidad/valor/sello/GEN2 y firma directamente.
                digest = hashlib.sha256((ROOT / "data/corrida0" / number["calc"] / "resultados.json").read_bytes()).hexdigest()
                evidence.append({"id": number["id"], "result_id": rid, "calc": number["calc"], "valor": number["valor"], "unidad": number["unidad"], "periodo": number["periodo"], "denominador": number.get("denominador"), "ic": number.get("ic", [number.get("ic_lo"), number.get("ic_hi")]), "ic_calibrado": number.get("ic_calibrado"), "fuente": number.get("tabla"), "fila": number.get("fila"), "cuenta_gen2": load(ROOT / "data/corrida0" / number["calc"] / "ejecucion.json").get("etiquetas", {}).get("cuenta_gen2"), "estado_adopcion": number.get("estado_adopcion"), "registro_local": "derivado del sellado, no registro global vigente", "consulta": "NO-ENCONTRADO: registro derivado no contiene este RESULT; cotejo directo de sellado por control legado", "sha256_resultados_json": digest})
                continue
            digest = hashlib.sha256((ROOT / "data/corrida0" / number["calc"] / "resultados.json").read_bytes()).hexdigest()
            if row.get("corrida_id") != number["calc"] or row.get("cuenta_gen2") != "SI":
                errors.append(rid + ": registro no identifica corrida GEN2 autorizada")
            value = float(row["valor"])
            if number.get("transformacion") in ("porcentaje", "x100", "*100"): value *= 100
            if not math.isclose(value, number["valor"], rel_tol=1e-10, abs_tol=1e-10):
                errors.append(rid + ": valor no coincide con consulta.py")
            if digest != number.get("hash_sello"):
                errors.append(rid + ": hash difiere de tabla de cifras")
            evidence.append({"id": number["id"], "result_id": rid, "consulta": consulta._linea(rid, row, consulta.CAMPOS["result"][1]), "sha256_resultados_json": digest})
    return errors, counts, evidence, claims


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--escribe", action="store_true")
    args = ap.parse_args()
    errors, counts, evidence, claims = verify()
    mutations = mutation_tests(claims["consumo"], claims["familia"]) if not regressions(claims["consumo"], claims["familia"]) else []
    report = {"errores": errors, "conteos": counts, "mutaciones_rechazadas": mutations, "evidencia_consultada": evidence, "alcance": "Trazabilidad y regresiones materiales; no certificación independiente ni recálculo C1. Filas, identidades del mapa, líneas v1 y cláusulas no son tesis únicas."}
    if args.escribe:
        (HERE / "resultado.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        produce_index(counts, errors)
        index = NEW / "indice-consumo-familia-2.md"
        first = index.read_bytes()
        produce_index(counts, errors)
        assert first == index.read_bytes(), "Índice no reproducible"
        for c in counts:
            assert f"| {c['report']} | {c['afirmaciones']} | {c['mapa']} | {c['cifras']} | {c['fuentes']} |" in index.read_text(), "Conteos no regenerados"
    for row in counts: print(json.dumps(row, ensure_ascii=False))
    for error in errors: print("FAIL " + error)
    print("REGRESIONES", len(mutations), "rechazadas; errores", len(errors))
    return bool(errors)


def produce_index(counts, errors):
    lines = ["# Índice sucesor consumo y familia · C3 tanda 2", "", "Generado por `python3 forense/analisis/reports-v2/consumo-familia-2/verificacion/verifica.py --escribe`.", "", "Los conteos son unidades de trazabilidad; no expresan número de tesis únicas ni fuerza de evidencia.", "", "| Report | Filas dictaminadas | Identidades mapa cubiertas | Cifras trazadas | Fuentes |", "|---|---:|---:|---:|---:|"]
    for c in counts:
        lines.append(f"| {c['report']} | {c['afirmaciones']} | {c['mapa']} | {c['cifras']} | {c['fuentes']} |")
    lines += ["", "Estado de controles: " + ("sin errores detectados" if not errors else f"{len(errors)} errores; no entregar como verificado") + ".", "", "Fuentes explícitas: `consumo/consumo-juicios.json` y `familia/familia-juicios.json` en este sucesor. Productos publicados: reports v2 y tablas vivas de consumo-familia-1. El índice anterior se conserva como testimonio del corte previo.", "", "Revisión independiente de Claude y validación numérica C1 pendientes; este control no las sustituye. Consulta.py puede devolver NO-ENCONTRADO por rezago del registro derivado; resultado.json distingue esa reserva del cotejo directo contra sello/valor/GEN2/firmas."]
    (NEW / "indice-consumo-familia-2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
