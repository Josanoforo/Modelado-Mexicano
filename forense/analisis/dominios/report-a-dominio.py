"""Construye el censo report → dominio a partir de rutas vivas, con cobertura estricta."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_name("report-a-dominio-v1_0.tsv")
RULES = [
    ("Adopción_y_Resistencia", "TECNOLOGIA", "U4", "tematico"),
    ("Ausencia_sin_certeza", "DUELO", "MESA", "tematico"),
    ("Autoridad_y_jerarquía", "AUTORIDAD", "U3", "tematico"),
    ("Behavioral_Finance", "DINERO", "MESA", "tematico"),
    ("Confianza_y_Desconfianza", "CONFIANZA", "U3", "tematico"),
    ("El_Clasemediero", "MOVILIDAD", "MESA", "tematico"),
    ("El_Efecto_Ambiental", "VIOLENCIA", "U2", "tematico"),
    ("El_Mexicano_y_el_Tiempo", "TIEMPO", "U1", "tematico_transversal"),
    ("El_México_Rural", "RURAL_INDIGENA", "MESA", "tematico"),
    ("Elegir__Cortejar", "PAREJA", "U2", "tematico"),
    ("Genetica_y_Conducta", "GENETICA", "MESA", "tematico_firewall"),
    ("Health__Body", "SALUD", "MESA", "tematico"),
    ("Humor_in_Mexican", "HUMOR", "MESA", "tematico"),
    ("La_arquitectura_invisible", "INTERACCION", "MESA", "tematico"),
    ("La_familia_mexicana", "FAMILIA_CUIDADOS", "U2", "tematico"),
    ("Mexican_Population_Genomics", "GENOMICA", "MESA", "tematico_firewall"),
    ("Moral_Emotions", "EMOCIONES_MORALES", "MESA", "tematico"),
    ("Mérito__Movilidad", "MOVILIDAD", "U1", "tematico"),
    ("Non-Family_Social_Capital", "CAPITAL_SOCIAL", "MESA", "tematico"),
    ("Psicología_Política", "POLITICA", "U3", "tematico"),
    ("Psicología__Conducta", "SINTESIS", "MESA", "integrador"),
    ("Psicología_de_la_Juventud", "JUVENTUD", "U1_U4", "tematico_transversal"),
    ("Psicología_del_Consumidor", "CONSUMO", "MESA", "tematico"),
    ("Psicología_del_Trabajo", "TRABAJO", "U1", "tematico"),
    ("Psychology_of_Mexico-US", "MIGRACION", "MESA", "tematico"),
    ("Reconfiguración_de_los_Guiones", "GENERO", "U2", "tematico"),
    ("Religiosidad_y_Psicología", "RELIGIOSIDAD", "MESA", "tematico"),
    ("Report_26", "CONOCIMIENTO", "MESA", "tematico"),
    ("Salud_Mental", "SALUD_MENTAL", "MESA", "tematico"),
    ("Sanción_Social", "SANCION_SOCIAL", "U4", "tematico_transversal"),
    ("Vejez_y_Cuidado", "FAMILIA_CUIDADOS", "MESA", "tematico"),
    ("Apuestas_Conductuales", "CONSUMO", "MESA", "forense"),
    ("Consumo_Aspiracional", "CONSUMO", "MESA", "forense"),
    ("Crédito_Fácil", "DINERO", "MESA", "forense"),
    ("Crédito_Popular", "DINERO", "MESA", "forense"),
    ("Validación_Forense_del_Clientelismo", "POLITICA", "U3", "forense"),
    ("compass-4", "DINERO", "MESA", "complemento_forense_credito_popular"),
]


def main() -> None:
    sources = sorted((ROOT / "corpus/reports").glob("*.md")) + sorted(
        (ROOT / "corpus/forense").glob("*.md")
    )
    assert len(sources) == 37, f"censo cambió: {len(sources)}"
    rows = []
    for path in sources:
        matches = [rule for rule in RULES if path.name.startswith(rule[0])]
        assert len(matches) == 1, (path, matches)
        _, domain, front, role = matches[0]
        rows.append((str(path.relative_to(ROOT)), hashlib.sha256(path.read_bytes()).hexdigest(), domain, front, role))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["ruta", "sha256_recalculado", "dominio_primario", "consumidor", "rol"])
        writer.writerows(rows)


if __name__ == "__main__":
    main()
