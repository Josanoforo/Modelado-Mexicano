"""Control dirigido de cobertura, enlaces y coherencia editorial del report."""
import csv
import json
from collections import Counter
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[4]
report = root / "corpus/reports-v2/El_México_Rural_e_Indígena_en_sus_Propios_Términos__Comunalidad__Autoridad_y_Reciprocidad_como_Sistemas_con_Lógica_Propia.md"
mapa = root / "canon/mapa-dominios-v1_1.tsv"
with mapa.open(newline="") as f:
    ids = {r["id_afirmacion"] for r in csv.DictReader(f, delimiter="\t") if "Comunalidad" in r["report"]}
with (here / "tabla-afirmaciones.tsv").open(newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))
assert len(ids) == 49 and len(rows) == len({r["id"] for r in rows}) == 60
assert {r["id"] for r in rows if r["id"].startswith("ASTRA5-")} == ids
assert all(r["dictamen_v2"] in {"CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"} and r["razon_editorial"] for r in rows)
assert all(not r["result_id"] for r in rows), "No se publican cifras RESULT en esta pieza"
assert next(r for r in rows if r["id"].endswith("-041"))["reserva"] == "NO-ABRIR"
summary = json.loads((here / "resumen.json").read_text())
assert summary["registros"] == len(rows) and summary["mapa_filas"] == len(ids)
assert summary["dictamenes"] == dict(Counter(r["dictamen_v2"] for r in rows))
by_id = {r["id"]: r for r in rows}
assert by_id["ASTRA5-U0-RURAL-004"]["dictamen_v2"] == "MATIZA"
assert by_id["ASTRA5-U0-RURAL-030"]["dictamen_v2"] == "MATIZA"
assert by_id["EXTRA-RURAL-005"]["dictamen_v2"] == "SIN-CIFRA"
assert {r["id"] for r in rows if r["dictamen_v2"] == "ROMPE"} == {"EXTRA-RURAL-002", "EXTRA-RURAL-011"}
txt = report.read_text()
for token in ("## Resumen ejecutivo", "## Marco", "## Mapa de evidencia", "## Patrones", "## Comparación internacional", "## Implicaciones", "## Reglas SI", "## Auditoría final", "418 municipios SNI", "falacia ecológica"):
    assert token in txt, token
assert "417 de los" not in txt and "99,759,455" not in txt
print(f"VERDE: {len(rows)} afirmaciones (49 mapa, 11 añadidas); reserva ENASEM explícita; estructura completa")
