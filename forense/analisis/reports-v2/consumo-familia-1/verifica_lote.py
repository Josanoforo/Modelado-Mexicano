#!/usr/bin/env python3
"""Control local de cobertura y trazabilidad; no adjudica fuerza sustantiva.

No lee microdatos ni remide. Cada cifra publicable usa [CIFRA:id]; años,
identificadores y referencias bibliográficas no se tratan como mediciones.
"""
import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
REPORTS = {
    "consumo": "Psicología_del_Consumidor_Mexicano__Patrones__Contradicciones_y_Estrategia.md",
    "familia": "La_familia_mexicana_como_sistema_psicológico__entre_el_afecto__la_obligación_y_la_adaptación_económica.md",
}
REASONS = {"adquisición", "falta de ejecución", "instrumento", "comparabilidad", "restricción del proyecto", "imposibilidad justificada", "adquisición pendiente", "instrumento inadecuado", "no comparabilidad"}
MARKER = re.compile(r"\[CIFRA:([^] ]+)\]")
# Magnitudes explícitas, no cualquier dígito: también detecta porcentajes
# desprovistos de marcador en prosa o tabla. La revisión humana cubre cifras
# escritas con palabras y decide si una cita sostiene el estimando.
MAGNITUDE = re.compile(r"(?<![\w-])\d+(?:[.,]\d+)?\s*(?:%|por ciento|pesos|millones|mil millones|hogares|personas|puntos porcentuales)\b|\d+(?:[.,]\d+)?\s*%|\$\s*\d+|\d+\s*(?:de cada|:)\s*\d+", re.I)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader((s for s in f if not s.startswith("#")), delimiter="\t"))


def verify(base=BASE, reports=None):
    errors, counts = [], []
    reports = reports or ROOT / "corpus/reports-v2"
    mapa = rows(ROOT / "canon/mapa-dominios-v1_1.tsv")
    decisions = {r["objeto"]: r["decision"] for r in rows(ROOT / "data/corrida0/decisiones.tsv")}
    signatures = rows(ROOT / "forense/firmas-pendientes.tsv")
    cache = {}
    for lane, name in REPORTS.items():
        prefix = lane + ": "
        def fail(msg):
            errors.append(prefix + msg)
        try:
            claims = load(base / lane / (lane + "-afirmaciones.json"))
            numbers = load(base / lane / (lane + "-cifras.json"))
            sources = load(base / lane / (lane + "-fuentes.json"))
            body = (reports / name).read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            fail(str(exc)); continue
        source_ids = set()
        for s in sources:
            if s.get("id") in source_ids: fail("fuente duplicada " + s["id"])
            source_ids.add(s.get("id"))
            for k in ("id", "url", "autor", "fecha", "poblacion", "metodo", "procedencia", "alcance"):
                if not s.get(k): fail("fuente sin " + k)
            if not re.match(r"https?://[^/ ]+", s.get("url", "")): fail("URL inválida " + str(s.get("id")))
            if s.get("procedencia") not in ("a", "b", "c", "(a)", "(b)", "(c)"): fail("procedencia inválida " + str(s.get("id")))
        number_ids = {n["id"] for n in numbers}
        if len(number_ids) != len(numbers): fail("cifra duplicada")
        markers = set(MARKER.findall(body))
        if markers != number_ids: fail("marcadores/cifras difieren: " + str(sorted(markers ^ number_ids)))
        for i, line in enumerate(body.splitlines(), 1):
            if MAGNITUDE.search(line) and not MARKER.search(line): fail(f"magnitud sin fuente L{i}")
        result_ids = set()
        for n in numbers:
            tag = str(n.get("id"))
            for key in ("valor", "unidad", "periodo"):
                if key not in n or n[key] in (None, ""): fail(tag + " sin " + key)
            if n.get("tipo") == "externa":
                if n.get("fuente_id") not in source_ids: fail(tag + " cifra externa sin fuente")
                if not n.get("denominador"): fail(tag + " sin denominador")
                continue
            calc, rid = n.get("calc", ""), n.get("result_id", "")
            result_ids.add(rid)
            decision = decisions.get(calc + "/" + rid, decisions.get(rid, ""))
            if "VETADA" in decision or "CONSUMO-PISOS-0001" in calc:
                fail(tag + " referencia a fila vetada " + calc); continue
            try:
                if calc not in cache:
                    folder = ROOT / "data/corrida0" / calc
                    data = load(folder / "resultados.json")
                    seal = load(folder / "sello.json")
                    execution = load(folder / "ejecucion.json")
                    digest = hashlib.sha256((folder / "resultados.json").read_bytes()).hexdigest()
                    cache[calc] = (data["resultados"], seal, execution, digest)
                values, seal, execution, digest = cache[calc]
                if seal.get("resultados.json") != digest: fail(tag + " sello no coincide")
                if n.get("hash_sello") != digest: fail(tag + " hash_sello no coincide")
                if execution.get("etiquetas", {}).get("cuenta_gen2") != "SI": fail(tag + " no cuenta GEN2")
                value = values[rid]
                transform = n.get("transformacion", "identidad")
                if transform in ("porcentaje", "x100", "*100"): value *= 100
                elif transform not in ("identidad", "ninguna", "sin transformación", "sin transformacion", "1"):
                    fail(tag + " transformación no ejecutable " + str(transform)); continue
                if not isinstance(value, (int, float)) or not isinstance(n.get("valor"), (int, float)) or not math.isclose(value, n["valor"], rel_tol=1e-10, abs_tol=1e-10): fail(tag + " valor no coincide con RESULT")
                state = n.get("estado_adopcion", "")
                if not state: fail(tag + " sin estado adopción")
                if "ADOPTAD" in state and "NO-ADOPTAD" not in state and "NO ADOPTAD" not in state and "adopcion=ADOPTAD" not in decision and not any(
                    fp["estado"] == "FIRMADA" and calc in (fp["firmada_en"] + fp["qué_se_firma"])
                    and "adopta" in fp["firmada_en"].lower() for fp in signatures
                ):
                    fail(tag + " adopción no acreditada por decisión vigente")
                for key in ("tabla", "fila"):
                    if not n.get(key): fail(tag + " sin localizador " + key)
                if n.get("tabla") and n.get("fila"):
                    table = ROOT / n["tabla"]
                    with table.open(encoding="utf-8") as f:
                        lines = list(csv.reader(f, delimiter="\t"))
                    row = lines[int(n["fila"]) - 1]
                    if calc not in row or rid not in row: fail(tag + " tabla/fila no identifica CALC y RESULT")
            except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
                fail(tag + " RESULT inválido: " + str(exc))
        old = (ROOT / "corpus/reports" / name).read_text(encoding="utf-8").splitlines()
        covered, seen, claim_ids = set(), set(), set()
        expected = {r["id_afirmacion"] for r in mapa if r["report"] == "corpus/reports/" + name}
        for c in claims:
            cid = str(c.get("id"))
            if cid in claim_ids: fail("afirmación duplicada " + cid)
            claim_ids.add(cid)
            for key in ("localizador", "texto_v1", "dictamen", "razon", "estado_adopcion", "vigencia", "cambio_editorial"):
                if not c.get(key): fail(cid + " sin " + key)
            mid = c.get("mapa_id")
            if mid:
                if mid not in expected: fail(cid + " mapa ajeno/desconocido " + mid)
                seen.add(mid)
            if c.get("dictamen") not in ("CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"): fail(cid + " dictamen inválido")
            if c.get("dictamen") == "SIN-CIFRA" and c.get("razon_sin_cifra") not in REASONS: fail(cid + " razón SIN-CIFRA inválida")
            for eid in c.get("evidencia_ids", []) + c.get("referencias", []) + c.get("result_ids", []):
                if eid not in source_ids | result_ids | number_ids: fail(cid + " evidencia desconocida " + eid)
            loc = str(c.get("localizador", ""))
            for match in re.finditer(r"L(\d+)(?:[-–](?:L)?(\d+))?", loc):
                start, end = int(match[1]), int(match[2] or match[1])
                covered.update(range(start, end + 1))
            text = c.get("texto_v1", "")
            normalized = lambda s: " ".join(s.split())
            map_text = next((r["texto_vigente"] for r in mapa if r["id_afirmacion"] == mid), "")
            if normalized(text) not in normalized("\n".join(old)) and (not mid or normalized(text) != normalized(map_text)):
                fail(cid + " texto_v1 no procede del original")
        if seen != expected: fail("mapa sin cobertura: " + str(sorted(expected - seen)))
        exclusion = base / lane / (lane + "-cobertura-v1.json")
        if exclusion.exists():
            for e in load(exclusion):
                if not e.get("razon"): fail("exclusión v1 sin razón")
                covered.add(int(e["linea"]))
        # No se decide automáticamente qué es material. Cada línea sustantiva
        # se cubre en una afirmación o recibe exclusión editorial explícita.
        omitted = [i for i, line in enumerate(old, 1) if line.strip() and not line.lstrip().startswith(("#", "---", "|---", "<!--")) and i not in covered]
        if omitted: fail("líneas v1 sin cobertura/exclusión: " + str(omitted))
        counts.append({"report": lane, "afirmaciones": len(claims), "mapa": len(seen), "cifras": len(numbers), "fuentes": len(sources)})
    return errors, counts


def selftest():
    # Copias temporales; los informes de entrega permanecen intactos.
    with tempfile.TemporaryDirectory(prefix="consumo-familia-mutaciones-") as tmp:
        tmp = Path(tmp)
        shutil.copytree(BASE, tmp / "lote")
        report = tmp / "reports"; report.mkdir()
        for name in REPORTS.values(): shutil.copy2(ROOT / "corpus/reports-v2" / name, report / name)
        path = report / REPORTS["consumo"]
        path.write_text(path.read_text() + "\nEl 73% de los hogares compra por prestigio.\n")
        errors, _ = verify(tmp / "lote", report)
        assert any("magnitud sin fuente" in e for e in errors), errors
        shutil.copy2(ROOT / "corpus/reports-v2" / REPORTS["consumo"], path)
        path = tmp / "lote/consumo/consumo-cifras.json"
        data = load(path)
        own = next(n for n in data if n.get("tipo") != "externa")
        own["calc"] = "CALC-ENIGH-CONSUMO-PISOS-0001"
        path.write_text(json.dumps(data, ensure_ascii=False))
        errors, _ = verify(tmp / "lote", report)
        assert any("fila vetada" in e for e in errors), errors
    print("AUTOPRUEBA VERDE: cifra sin fuente y fila vetada rechazadas en copia temporal")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--autoprueba", action="store_true")
    args = parser.parse_args()
    errors, counts = verify()
    for row in counts: print(json.dumps(row, ensure_ascii=False))
    if errors:
        for err in errors: print("FAIL " + err)
        return 1
    print("VERDE: cobertura, cifras, referencias y estados; revisión sustantiva humana requerida")
    if args.autoprueba: selftest()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
