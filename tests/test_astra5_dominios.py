"""Guardias de cobertura e integridad del corte documental ASTRA5-U0."""

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "forense/analisis/dominios"


def read(name):
    with (DIR / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def test_censo_vivo_y_complemento():
    paths = list((ROOT / "corpus/reports").glob("*.md")) + list(
        (ROOT / "corpus/forense").glob("*.md")
    )
    rows = read("report-a-dominio-v1_0.tsv")
    assert len(paths) == len(rows) == 37
    assert {row["ruta"] for row in rows} == {str(p.relative_to(ROOT)) for p in paths}
    for row in rows:
        assert hashlib.sha256((ROOT / row["ruta"]).read_bytes()).hexdigest() == row["sha256_recalculado"]
    compass = [row for row in rows if row["ruta"].endswith("compass-4-e29a28d4-credito-popular-2026.md")]
    assert len(compass) == 1
    assert compass[0]["rol"] == "complemento_forense_credito_popular"


def test_candidatas_tienen_procedencia_y_no_son_dictamen():
    rows = read("candidatas-v1_0.tsv")
    assert {row["ruta"] for row in rows} == {row["ruta"] for row in read("report-a-dominio-v1_0.tsv")}
    for row in rows:
        path = ROOT / row["ruta"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256_recalculado"]
        assert path.read_text(encoding="utf-8").splitlines()[int(row["linea"]) - 1].strip() == row["pasaje_candidato"]


def test_corte_enoe_no_confunde_medibilidad_y_reserva():
    rows = read("corte-enoe-v1_0.tsv")
    assert len(rows) == 3
    assert len({row["id_afirmacion"] for row in rows}) == len(rows)
    for row in rows:
        assert row["dictamen"] == "MEDIBLE-CON-ADQUISICIÓN"
        assert row["estado_verificacion"] == "CERRADA"
        assert "diseño muestral" in row["dictamen_razon"]
        assert "NO ABIERTO" in row["datos_id_estado"]
        assert hashlib.sha256((ROOT / row["report"]).read_bytes()).hexdigest() == row["report_sha256"]


def test_cortes_documentales_conservan_componentes_y_fuentes():
    files = ["corte-tecnologia-v1_0.tsv", "corte-endireh-v1_0.tsv", "corte-politica-v1_0.tsv"]
    for name in files:
        rows = read(name)
        assert len(rows) == 1
        row = rows[0]
        assert row["estado_verificacion"] == "CERRADA"
        assert row["dictamen"] == "MEDIBLE-CON-ADQUISICIÓN"
        assert row["componente_contrastable"] and row["limite_inferencial"]
        assert "NO ABIERTO" in row["datos_id_estado"] or "no recalculado" in row["datos_id_estado"]
        assert hashlib.sha256((ROOT / row["report"]).read_bytes()).hexdigest() == row["report_sha256"]
