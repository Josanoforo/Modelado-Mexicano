#!/usr/bin/env python3
"""Arma la vista descriptiva y comprueba su coherencia sin recalcular microdatos."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "distribucion-total-sexo.csv"
COVERAGE = ROOT / "cobertura-total-sexo.csv"
CONTRAST = ROOT / "contraste-mujeres-menos-hombres.csv"
OUTPUT = ROOT / "tabla-descriptiva-apoyo-monetario-total-sexo.csv"

DOMAINS = ("TOTAL", "HOMBRES", "MUJERES")
CODES = tuple(str(code) for code in range(1, 8))
QUESTION = "Q8a Whom or where to ask for help: borrow large sum of money?"
VARIABLE = "v26"
WEIGHT = "WEIGHT=1 (No weighting), documentado para México"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def same_number(left: str, right: str, tolerance: float = 1e-10) -> bool:
    return abs(float(left) - float(right)) <= tolerance


def main() -> int:
    distribution = rows(DIST)
    coverage = rows(COVERAGE)
    contrast_rows = rows(CONTRAST)
    if len(contrast_rows) != 1:
        raise SystemExit("PUBLICACION-FALLA:CONTRASTE-NO-UNICO")
    contrast = contrast_rows[0]

    output: list[dict[str, str]] = []
    by_domain: dict[str, list[dict[str, str]]] = {}
    for domain in DOMAINS:
        dist_rows = [row for row in distribution if row["dominio_id"] == domain]
        if sorted(row["codigo"] for row in dist_rows) != list(CODES):
            raise SystemExit(f"PUBLICACION-FALLA:CATEGORIAS:{domain}")
        if len({row["n_denominador_valido"] for row in dist_rows}) != 1:
            raise SystemExit(f"PUBLICACION-FALLA:BASE-N:{domain}")
        if len({row["masa_denominador_valido"] for row in dist_rows}) != 1:
            raise SystemExit(f"PUBLICACION-FALLA:BASE-MASA:{domain}")
        for row in dist_rows:
            if not same_number(row["porcentaje"], str(100 * float(row["proporcion"]))):
                raise SystemExit(f"PUBLICACION-FALLA:PORCENTAJE:{domain}:{row['codigo']}")

        cov = {row["clasificacion"]: row for row in coverage if row["dominio_id"] == domain}
        expected_states = {"VALIDA", "NO_PUEDE_ELEGIR", "NO_RESPUESTA", "PESO_INVALIDO"}
        if set(cov) != expected_states:
            raise SystemExit(f"PUBLICACION-FALLA:FALTANTES:{domain}")
        valid = cov["VALIDA"]
        if dist_rows[0]["n_denominador_valido"] != valid["n"]:
            raise SystemExit(f"PUBLICACION-FALLA:DENOMINADOR-N:{domain}")
        if not same_number(dist_rows[0]["masa_denominador_valido"], valid["masa"]):
            raise SystemExit(f"PUBLICACION-FALLA:DENOMINADOR-MASA:{domain}")
        if len({row["n_elegible"] for row in cov.values()}) != 1:
            raise SystemExit(f"PUBLICACION-FALLA:ELEGIBLES:{domain}")

        by_domain[domain] = dist_rows
        for row in dist_rows:
            output.append(
                {
                    "calc_id": row["calc_id"],
                    "variable": VARIABLE,
                    "pregunta_integrada_exacta": QUESTION,
                    "ponderador": WEIGHT,
                    "universo_elegible": row["universo"],
                    "dominio_id": domain,
                    "dominio": row["dominio"],
                    "codigo": row["codigo"],
                    "categoria_integrada": row["texto_integrado"],
                    "categoria_mexico": row["texto_mexico"],
                    "n_elegible": valid["n_elegible"],
                    "masa_elegible": valid["masa_elegible_peso_utilizable"],
                    "n_no_puede_elegir": cov["NO_PUEDE_ELEGIR"]["n"],
                    "n_no_respuesta": cov["NO_RESPUESTA"]["n"],
                    "n_peso_invalido": cov["PESO_INVALIDO"]["n"],
                    "n_denominador_valido": row["n_denominador_valido"],
                    "masa_denominador_valido": row["masa_denominador_valido"],
                    "n_categoria": row["n_categoria"],
                    "masa_categoria": row["masa_categoria"],
                    "porcentaje": row["porcentaje"],
                    "unidad_punto": "porcentaje",
                    "precision": row["precision"],
                }
            )

    women = next(row for row in by_domain["MUJERES"] if row["codigo"] == "1")
    men = next(row for row in by_domain["HOMBRES"] if row["codigo"] == "1")
    checks = (
        contrast["codigo"] == "1",
        contrast["texto_integrado"] == women["texto_integrado"] == men["texto_integrado"],
        contrast["n_denominador_mujeres"] == women["n_denominador_valido"],
        contrast["n_denominador_hombres"] == men["n_denominador_valido"],
        same_number(contrast["masa_denominador_mujeres"], women["masa_denominador_valido"]),
        same_number(contrast["masa_denominador_hombres"], men["masa_denominador_valido"]),
        same_number(contrast["p_mujeres"], women["proporcion"]),
        same_number(contrast["p_hombres"], men["proporcion"]),
        same_number(
            contrast["diferencia_puntos_porcentuales"],
            str(100 * float(contrast["diferencia_menos_mas"])),
        ),
    )
    if not all(checks):
        raise SystemExit("PUBLICACION-FALLA:CONTRASTE-BASE-O-CATEGORIA")

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    print(
        "PUBLICACION-OK: 21 filas; categorías 1..7 y bases coinciden; "
        f"contraste={contrast['diferencia_puntos_porcentuales']} puntos porcentuales"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
