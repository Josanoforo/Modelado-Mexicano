"""Verifica identidades, cobertura y trazas de la tabla editorial."""
import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
NAME = "Psicología__Conducta_y_Sociedad_en_el_México_Contemporáneo__Análisis_Transcultural_y_Estructural.md"


def rows(p):
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main():
    v1 = ROOT / "corpus/reports" / NAME
    maprows = {r["id_afirmacion"]: r for r in rows(ROOT / "canon/mapa-dominios-v1_1.tsv") if r["report"] == f"corpus/reports/{NAME}"}
    decisions = rows(HERE / "tabla-decisiones.tsv")
    table = rows(HERE / "tabla-afirmaciones.tsv")
    assert len(table) == len(decisions)
    assert len({r["id"] for r in table}) == len(table)
    assert [r["id"] for r in table] == [r["id"] for r in decisions]
    assert set(maprows) <= {r["id"] for r in table}
    assert all(r["report_sha256"] == hashlib.sha256(v1.read_bytes()).hexdigest() for r in maprows.values())
    lines = v1.read_text(encoding="utf-8").splitlines()
    for d, t in zip(decisions, table):
        assert d["id"] == t["id"]
        for field in ("origen", "localizador_v1", "dictamen", "razon", "fuente_especifica", "revision_humana"):
            assert d[field] == t[field], (d["id"], field)
        assert t["fuente_especifica"] and t["razon"] and t["revision_humana"]
        assert t["dictamen"] in {"CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"}
        if t["origen"] == "MAPA":
            m = maprows[t["id"]]
            assert t["afirmacion"] == m["texto_vigente"] and t["localizador_v1"] == m["localizador"]
        else:
            assert t["origen"] == "ADICIONAL"
            assert t["localizador_v1"].startswith("L")
            n = int(t["localizador_v1"].split("-")[0][1:])
            assert 1 <= n <= len(lines)
    assert all(r["revision_humana"] == "PENDIENTE" for r in table if r["dictamen"] == "ROMPE")
    print(f"OK: {len(table)} decisiones trazadas, {len(maprows)} filas mapa cubiertas, {len(table)-len(maprows)} adicionales")


if __name__ == "__main__":
    main()
