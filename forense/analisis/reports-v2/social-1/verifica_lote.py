#!/usr/bin/env python3
"""Control local: evita repetir la cifra WVS sin procedencia de v1.

No dictamina tesis ni busca dígitos: verifica el universo declarado, los
registros cuantitativos y sus fuentes. No lee registros individuales.
"""
import argparse
import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path
from urllib.parse import urlparse

LOCAL = Path(__file__).resolve().parent
ROOT = LOCAL.parents[3]
DICTAMENES = {"CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_claim(c, refs):
    errors = []
    for field in ("id", "afirmacion", "argumento", "vigencia", "cambio_editorial", "estado_adopcion"):
        if not c.get(field):
            errors.append(f"{c.get('id')}: falta {field}")
    if c.get("dictamen") not in DICTAMENES:
        errors.append(f"{c.get('id')}: dictamen inválido")
    if c.get("dictamen") == "SIN-CIFRA" and not c.get("razon_sin_cifra"):
        errors.append(f"{c.get('id')}: SIN-CIFRA sin razón")
    for ref in c.get("evidencia", []):
        if ref not in refs:
            errors.append(f"{c.get('id')}: evidencia no registrada {ref}")
    return errors


def validate_figure(f, sources, result_cache, firmas):
    errors = []
    ident = f.get("id", "SIN-ID")
    for field in ("id", "unidad", "periodo", "transformacion", "estado"):
        if not f.get(field):
            errors.append(f"{ident}: falta {field}")
    if f.get("tipo") == "externa":
        if f.get("fuente_id") not in sources:
            errors.append(f"{ident}: cifra externa sin fuente")
        elif urlparse(sources[f["fuente_id"]].get("url", "")).scheme not in ("http", "https"):
            errors.append(f"{ident}: cifra externa sin fuente pública")
        return errors
    if f.get("tipo") != "propia":
        return errors + [f"{ident}: tipo inválido"]
    for field in ("calc", "result", "fila", "hash"):
        if not f.get(field):
            errors.append(f"{ident}: falta {field}")
    estado = str(f.get("estado", "")).upper()
    if any(x in estado for x in ("VETADO", "RETIRADO", "RESERVADO")):
        errors.append(f"{ident}: estado no publicable {estado}")
    calc = f.get("calc", "")
    path = ROOT / "data/corrida0" / calc / "resultados.json"
    if not path.is_file():
        return errors + [f"{ident}: CALC inexistente"]
    if calc not in result_cache:
        sello = read(path.parent / "sello.json")
        result_cache[calc] = (read(path)["resultados"], sha(path), sello.get("resultados.json"))
    results, actual, sealed = result_cache[calc]
    if f.get("hash") != actual or actual != sealed:
        errors.append(f"{ident}: hash no coincide con archivo y sello")
    rid = f.get("result")
    if rid not in results:
        errors.append(f"{ident}: RESULT inexistente {rid}")
    else:
        value = results[rid]
        if isinstance(value, list):
            try:
                value = value[int(f["fila"])]
            except (ValueError, IndexError, TypeError):
                errors.append(f"{ident}: fila inválida")
        if value != f.get("valor"):
            errors.append(f"{ident}: valor distinto del RESULT sellado")
        for field in ("ic_lo", "ic_hi", "n"):
            if field in f:
                aux = f.get("result_" + field)
                if not aux or aux not in results:
                    errors.append(f"{ident}: {field} sin RESULT auxiliar")
                elif results[aux] != f[field]:
                    errors.append(f"{ident}: {field} distinto del RESULT auxiliar")
    if "ADOPTADO" in estado:
        fp = f.get("firma_fp")
        if not fp or firmas.get(fp, {}).get("estado") != "FIRMADA":
            errors.append(f"{ident}: adopción sin FP FIRMADA")
    return errors


def run():
    errors, summary, cache = [], {}, {}
    cut = read(LOCAL / "social-corte.json")
    archived = subprocess.check_output(["git", "show", f"{cut['corte']}:{cut['encargo']}"], cwd=ROOT)
    if not (ROOT / cut["encargo"]).read_bytes().startswith(archived):
        errors.append("encargo: cuerpo archivado modificado")
    if (ROOT / (cut["encargo"] + ".cuerpo.sha256")).read_text().strip() != cut["sidecar"]:
        errors.append("encargo: sello existente modificado")
    with (ROOT / "canon/mapa-dominios-v1_1.tsv").open() as stream:
        mapa = list(csv.DictReader(stream, delimiter="\t"))
    with (ROOT / "forense/firmas-pendientes.tsv").open() as stream:
        firmas = {r["id"]: r for r in csv.DictReader(stream, delimiter="\t")}
    names = list(cut["reports"])
    for prefix, name in zip(("confianza", "capital", "religion"), names):
        original = ROOT / "corpus/reports" / name
        report = ROOT / "corpus/reports-v2" / name
        if sha(original) != cut["reports"][name]:
            errors.append(f"{prefix}: v1 cambió frente al corte")
        claims = read(LOCAL / f"{prefix}-afirmaciones.json")
        figures = read(LOCAL / f"{prefix}-cifras.json")
        sources = {s["id"]: s for s in read(LOCAL / f"{prefix}-fuentes.json")}
        ids = {c["id"] for c in claims}
        refs = set(sources) | {f["id"] for f in figures}
        with (LOCAL / f"{prefix}-afirmaciones.tsv").open() as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        if {r["id"] for r in rows} != ids or len(rows) != len(claims):
            errors.append(f"{prefix}: TSV/JSON difieren en el universo")
        by_id = {r["id"]: r for r in rows}
        for c in claims:
            row = by_id.get(c["id"], {})
            if any(row.get(k) != c.get(k) for k in ("afirmacion", "dictamen", "argumento")):
                errors.append(f"{prefix}: TSV/JSON difieren en el dictamen de {c['id']}")
        if len(ids) != len(claims):
            errors.append(f"{prefix}: id de afirmación repetido")
        for c in claims:
            errors += validate_claim(c, refs)
        expected = {r["id_afirmacion"] for r in mapa if r["report"] == "corpus/reports/" + name}
        got = {ident for c in claims for ident in str(c.get("mapa_id") or "").split(";") if ident}
        if expected != got:
            errors.append(f"{prefix}: mapa sin cobertura exacta: faltan {sorted(expected-got)}; sobran {sorted(got-expected)}")
        coverage = read(LOCAL / f"{prefix}-cobertura.json")
        lines = original.read_text().splitlines()
        covered = set()
        for kind in ("incluidas", "excluidas"):
            for block in coverage[kind]:
                a, b = block["linea"], block["linea_fin"]
                if not 1 <= a <= b <= len(lines):
                    errors.append(f"{prefix}: rango de cobertura inválido")
                covered.update(range(a, b + 1))
                if kind == "incluidas" and (not block.get("afirmaciones") or not set(block["afirmaciones"]) <= ids):
                    errors.append(f"{prefix}: bloque sin afirmaciones registradas")
                if kind == "excluidas" and not block.get("razon"):
                    errors.append(f"{prefix}: exclusión sin razón")
        missing = {i for i, line in enumerate(lines, 1) if line.strip()} - covered
        if missing:
            errors.append(f"{prefix}: líneas omitidas en silencio {sorted(missing)}")
        for s in sources.values():
            url = s.get("url", "")
            if urlparse(url).scheme not in ("https", "http") and not (url and (ROOT / url.split('#')[0]).is_file()):
                errors.append(f"{prefix}: URL inválida {s['id']}")
            for field in ("autor", "fecha", "poblacion", "metodo", "tier", "tesis", "lectura"):
                if not s.get(field):
                    errors.append(f"{prefix}: fuente {s['id']} sin {field}")
        text = report.read_text()
        for f in figures:
            errors += validate_figure(f, sources, cache, firmas)
            if f["id"] not in text:
                errors.append(f"{prefix}: cifra registrada sin vínculo al report {f['id']}")
        summary[prefix] = {d: sum(c["dictamen"] == d for c in claims) for d in sorted(DICTAMENES)}
        summary[prefix].update(afirmaciones=len(claims), mapa=len(expected), cifras=len(figures), fuentes=len(sources))
    return errors, summary


def mutation_test():
    sources = {"F": {"url": "https://example.org"}}
    clean = dict(id="X", tipo="externa", unidad="persona", periodo="2020", transformacion="identidad", estado="EXTERNA", fuente_id="F")
    assert not validate_figure(clean, sources, {}, {})
    broken = copy.deepcopy(clean)
    broken.pop("fuente_id")
    assert validate_figure(broken, sources, {}, {}), "no detecta cifra sin fuente"
    own = dict(id="V", tipo="propia", unidad="persona", periodo="2018", transformacion="identidad", estado="VETADO", calc="CALC-NO-EXISTE", result="R", fila="R", hash="x", valor=0)
    assert any("no publicable" in e for e in validate_figure(own, {}, {}, {}))
    print("MUTACIONES VERDE: cifra externa sin fuente y estado vetado rechazados")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prueba-mutacion", action="store_true")
    args = parser.parse_args()
    if args.prueba_mutacion:
        mutation_test()
    try:
        failures, totals = run()
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f"LOTE INCOMPLETO: {exc}")
    print(json.dumps(totals, ensure_ascii=False, indent=2))
    for failure in failures:
        print("FAIL:", failure)
    print(f"{'VERDE' if not failures else 'ROJO'}: {len(failures)} errores de cobertura/trazabilidad; juicio sustantivo separado")
    raise SystemExit(bool(failures))
