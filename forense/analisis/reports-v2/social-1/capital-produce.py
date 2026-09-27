#!/usr/bin/env python3
"""Reproduce la tabla y cobertura desde textos conservados; no automatiza juicio.

Defecto material que controla: omitir cláusulas fuera del mapa o transportar una
cifra sin su unidad/hash. No abre microdatos ni altera un RESULT.
"""
import csv
import hashlib
import json
from pathlib import Path

LOCAL = Path(__file__).resolve().parent
ROOT = LOCAL.parents[3]
NAME = "Non-Family_Social_Capital_in_Mexico__Cooperation__Trust__and_Collective_Action_Beyond_Kinship.md"


def main():
    claims = json.loads((LOCAL / "capital-afirmaciones.json").read_text())
    source = (ROOT / "corpus/reports" / NAME).read_text().splitlines()
    with (ROOT / "canon/mapa-dominios-v1_1.tsv").open() as stream:
        mapa = {r["id_afirmacion"]: r for r in csv.DictReader(stream, delimiter="\t")
                if r["report"] == "corpus/reports/" + NAME}
    found = set()
    for claim in claims:
        if claim["origen"] == "mapa":
            found.add(claim["mapa_id"])
            assert claim["afirmacion"] == mapa[claim["mapa_id"]]["texto_vigente"]
        else:
            assert claim["afirmacion"] == source[claim["linea"] - 1]
    assert found == set(mapa)
    figures = json.loads((LOCAL / "capital-cifras.json").read_text())
    for figure in figures:
        path = ROOT / "data/corrida0" / figure["calc"] / "resultados.json"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == figure["hash"]
        assert json.loads(path.read_text())["resultados"][figure["result"]] == figure["valor"]
    fields = list(dict.fromkeys(k for claim in claims for k in claim))
    with (LOCAL / "capital-afirmaciones.tsv").open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows({**c, "evidencia": ";".join(c["evidencia"])} for c in claims)
    coverage = {"incluidas": [], "excluidas": []}
    for index, line in enumerate(source, 1):
        if not line.strip():
            continue
        block = {"linea": index, "linea_fin": index}
        if line.startswith("#"):
            block["razon"] = "título/encabezado sin afirmación material"
            coverage["excluidas"].append(block)
        else:
            block["afirmaciones"] = [f"CAP-V1-L{index:03}"]
            coverage["incluidas"].append(block)
    (LOCAL / "capital-cobertura.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n")
    print(f"CAPITAL DERIVADO: mapa={len(mapa)}; v1={len(coverage['incluidas'])}; cifras={len(figures)}; cero microdatos")


if __name__ == "__main__":
    main()
