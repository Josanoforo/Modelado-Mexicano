#!/usr/bin/env python3
"""Check source identities, decision traces, report references and generated files."""

import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from produce import HERE, ROOT, PIECES, MAP, build, read_map, sha

LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
LINE = re.compile(r"\bL(\d+)\b")


def broken_links(markdown, report_path):
    broken = []
    for target in LINK.findall(markdown):
        target = target.strip().split(" ", 1)[0].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or not parsed.path:
            continue
        location = unquote(parsed.path)
        path = ROOT / location.lstrip("/") if location.startswith("/") else report_path.parent / location
        if not path.exists():
            broken.append(target)
    return broken


def inspect():
    errors = []
    map_rows = read_map()
    for piece, (original, report) in PIECES.items():
        source = ROOT / original
        product = ROOT / report
        if not source.is_file() or not product.is_file():
            errors.append(f"{piece}: falta v1 o v2")
            continue
        source_lines = source.read_text(encoding="utf-8").splitlines()
        report_text = product.read_text(encoding="utf-8")
        expected = {r["id_afirmacion"]: r for r in map_rows if r["report"] == original}
        for row in expected.values():
            if row["report_sha256"] != sha(source):
                errors.append(f"{piece}: hash v1 distinto del mapa")
                break
        decisions = json.loads((HERE / piece / "decisiones.json").read_text(encoding="utf-8"))
        for decision in decisions:
            label = f"{piece}/{decision.get('id', '<sin-id>')}"
            trace = str(decision.get("trace", ""))
            places = [int(x) for x in LINE.findall(trace)]
            if not places or any(n < 1 or n > len(source_lines) for n in places):
                errors.append(f"{label}: traza v1 inválida")
            if str(decision.get("id", "")) not in report_text:
                errors.append(f"{label}: id ausente del report v2")
            url = str(decision.get("fuente_url", ""))
            if url and urlsplit(url).scheme not in {"https", "http"}:
                errors.append(f"{label}: URL de fuente inválida")
        for target in broken_links(report_text, product):
            errors.append(f"{piece}: enlace local roto: {target}")
    try:
        products = build()
        for path, content in products.items():
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                errors.append(f"derivado desactualizado: {path.name}")
    except (ValueError, KeyError, FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
    return sorted(set(errors))


def main():
    errors = inspect()
    print(json.dumps({"estado": "PASS" if not errors else "FAIL", "errores": errors}, ensure_ascii=False))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
