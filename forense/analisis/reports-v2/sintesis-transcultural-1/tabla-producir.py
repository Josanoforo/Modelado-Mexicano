"""Produce la tabla editorial desde decisiones explícitas, nunca desde palabras clave."""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
NAME = "Psicología__Conducta_y_Sociedad_en_el_México_Contemporáneo__Análisis_Transcultural_y_Estructural.md"
V1 = ROOT / "corpus/reports" / NAME
MAP = ROOT / "canon/mapa-dominios-v1_1.tsv"
DEC = HERE / "tabla-decisiones.tsv"
OUT = HERE / "tabla-afirmaciones.tsv"
FIELDS = ["id", "origen", "localizador_v1", "afirmacion", "dictamen", "razon", "fuente_especifica", "traza", "revision_humana"]


def read(path):
    with path.open(encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f, delimiter="\t")


def main():
    v1_hash = hashlib.sha256(V1.read_bytes()).hexdigest()
    mapped = {r["id_afirmacion"]: r for r in read(MAP) if r["report"] == f"corpus/reports/{NAME}"}
    decisions = list(read(DEC))
    ids = [r["id"] for r in decisions]
    assert len(ids) == len(set(ids)), "id duplicado"
    assert set(mapped) <= set(ids), f"faltan filas del mapa: {sorted(set(mapped)-set(ids))}"
    assert len(mapped) == 28, f"cambió mapa: {len(mapped)}"
    out = []
    for d in decisions:
        m = mapped.get(d["id"])
        if m:
            assert d["origen"] == "MAPA"
            assert m["report_sha256"] == v1_hash
            assert d["localizador_v1"] == m["localizador"]
            d["afirmacion"] = m["texto_vigente"]
            d["traza"] = f"canon/mapa-dominios-v1_1.tsv#{d['id']}"
        else:
            assert d["origen"] == "ADICIONAL"
            d["traza"] = f"corpus/reports/{NAME}#{d['localizador_v1']}"
        assert d["dictamen"] in {"CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"}
        assert all(d.get(k) for k in ("razon", "fuente_especifica", "revision_humana")), d["id"]
        out.append({k: d[k] for k in FIELDS})
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(out)
    print(f"{len(out)} afirmaciones; {len(mapped)} mapa; {len(out)-len(mapped)} adicionales; v1 sha256 {v1_hash}")


if __name__ == "__main__":
    main()
