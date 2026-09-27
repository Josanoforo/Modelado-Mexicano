#!/usr/bin/env python3
"""Verifica identidad/custodia de preparación, nunca recalcula estimadores."""
import csv, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
BASE = REPO / "forense/validacion-independiente/catalogo-1-preparacion-lote2/astra6-c1-lote2-entrega-59.tsv"
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    all_before = list(csv.DictReader(BASE.open(), delimiter="\t"))
    before = [r for r in all_before if r["estado_preparacion"] == "NO-PREPARADO"]
    for row in all_before:
        archives = list((BASE.parent / "entradas" / row["paquete_original"]).glob("*.tar.gz"))
        assert len(archives) == 1, row["paquete_original"]
        assert sha(archives[0]) == row["sha256_contenedor"], row["paquete_original"]
    after = list(csv.DictReader((ROOT / "impedimentos-lote2-delta-48.tsv").open(), delimiter="\t"))
    b = {r["paquete_original"]: r for r in before}
    a = {r["paquete_original"]: r for r in after}
    assert len(before) == len(b) == len(after) == len(a) == 48
    assert set(a) == set(b), "No puede sustituir, ampliar ni perder identidades"
    assert sum(int(r["estimadores"]) for r in after) == 32347
    for key, row in a.items():
        assert row["estimadores"] == b[key]["estimadores"]
        assert row["estado_1185"] == b[key]["dictamen_preparatorio"]
        for field in ("avance_ejecutado", "artefactos", "impedimento_restante", "decision_exacta"):
            assert row[field].strip(), (key, field)
        for item in row["artefactos"].split(" | "):
            p = REPO / item
            assert p.is_file() and not p.is_symlink(), (key, item)
        assert row["estado_validacion"] == "NO-EVALUADO", "La preparación no constituye validación"
    manifest = json.loads((ROOT / "impedimentos-lote2-hashes-entrega.json").read_text())
    for rel, expected in manifest["archivos"].items():
        p = REPO / rel
        assert p.is_file() and not p.is_symlink()
        assert sha(p) == expected, rel
    bundle = json.loads((ROOT / "p1/impedimentos-lote2-p1-b-materializacion-recibo.json").read_text())
    destination = Path(bundle["destino"])
    assert not destination.is_symlink() and not destination.is_relative_to(REPO)
    for name, entry in bundle["archivos"].items():
        p = destination / name
        assert p.is_file() and not p.is_symlink()
        assert sha(p) == entry["sha256"]
        assert p.stat().st_mode & 0o777 == 0o600
    print(json.dumps({"identidades":len(a), "estimadores":32347, "archivos_verificados":len(manifest["archivos"]), "archivos_B_materializados":len(bundle["archivos"]), "validadores_ejecutados":0, "aperturas_reservadas":0}, ensure_ascii=False))
if __name__ == "__main__":
    main()
