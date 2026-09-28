"""Produce tabla de afirmaciones desde el mapa y juicios editoriales explícitos."""
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
ORIGINAL = "corpus/reports/Sanción_Social_Horizontal_en_México__Chisme__Envidia_y_Mal_de_Ojo_como_Mecanismos_de_Nivelación.md"
decisiones = json.loads((BASE / "decisiones.json").read_text(encoding="utf-8"))
with (REPO / "canon/mapa-dominios-v1_1.tsv").open(encoding="utf-8", newline="") as file:
    mapa = {row["id_afirmacion"].split("-")[-1]: row for row in csv.DictReader(file, delimiter="\t") if row["report"] == ORIGINAL}
assert set(mapa) == {k for k in decisiones if not k.startswith("X")}, (len(mapa), len(decisiones))
campos = ["id", "id_mapa", "origen", "localizador", "afirmacion_original", "dictamen", "razon", "evidencia", "RESULT", "adopcion"]
extras = {
    "X01": ("Marco conceptual / Patrón 2", "El mal de ojo articula la envidia y prescribe ocultar y no ostentar; se distingue creencia de mecanismo social."),
    "X02": ("Segmentación explícita", "El mecanismo pesa menos en el norte y más en centro/sur."),
    "X03": ("Causas / Segmentación explícita", "Mayor educación implica mayor confianza y menor dependencia del mecanismo; acceso digital reintroduce vigilancia."),
    "X04": ("Implicaciones aplicadas: marketing", "La aspiración se comunica mejor como pertenencia y esfuerzo compartido que como superioridad."),
    "X05": ("Recomendaciones: etapa 4", "Menos extorsión/secuestro y más confianza indicarían que puede ceder el no destaques racional."),
    "X06": ("Implicaciones aplicadas: RH", "Ocultar la posición relativa en rankings mejora resultados educativos; conviene evitar rankings públicos individuales."),
    "X07": ("Implicaciones aplicadas: salud", "El mal de ojo puede retrasar el inicio del tratamiento médico."),
    "X08": ("Patrón 5: funa", "La funa digital puede ser nivelación o crítica legítima; su frontera debe distinguirse."),
}
with (BASE / "tabla-afirmaciones.tsv").open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=campos, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for clave, (dictamen, razon, evidencia) in decisiones.items():
        row = mapa.get(clave)
        writer.writerow({"id": row["id_afirmacion"] if row else f"SANC-V1-{clave}", "id_mapa": row["id_afirmacion"] if row else "", "origen": "mapa" if row else "material_extra_v1", "localizador": row["localizador"] if row else extras[clave][0], "afirmacion_original": row["texto_vigente"] if row else extras[clave][1], "dictamen": dictamen, "razon": razon, "evidencia": evidencia, "RESULT": "", "adopcion": "NO_ADOPTA"})
