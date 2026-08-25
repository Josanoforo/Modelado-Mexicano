from __future__ import annotations

import copy
import unittest

from tools.curador_registro.generar_marco import (
    MARCO_FIELDS,
    diagnostics_bytes,
    generate,
    tsv_bytes,
)


def manifest(identifier: str = "MAN-1", **extra: str) -> dict[str, str]:
    return {"id": identifier, **extra}


def census(identifier: str = "MAN-1", batch: str = "E2B-1", **extra: str) -> dict[str, str]:
    return {
        "id_manifiesto": identifier,
        "reporte_neutral_ref": batch,
        "objetos_logicos": "999",
        **extra,
    }


def binary_report(**extra: str) -> dict[str, str]:
    return {
        "record_id": "R-1", "batch_id": "E2B-1", "payload_id": "MAN-1",
        "objeto_logico_id": "OBJ-B2-evidencia", "objeto_tipo": "VARIABLE-DICCIONARIO-XLSX",
        "localizador": "hoja=Variables#diccionario-fila=2:variable=Q_REAL",
        "variable": "Q_REAL", "encuesta": "ENCUESTA-CANONICA", "ola": "2024",
        "universo": "personas adultas residentes", "tipo_variable": "BINARIA",
        "codificacion": "0=No|1=Si", "categorias": "0|1", "missing": "9=No especificado",
        "ponderador": "FAC_EXACTO", "ponderador_exacto": "SI",
        "ponderador_fuente_ola_tabla": "SI", "cv": "12.5%", "n_no_ponderado": "2",
        "grado_dependencia": "P2", "publicada": "NO",
        "frase_discriminacion": "L memoriza una marginal; M condiciona por subgrupo.",
        "post_corte_u_ola_retenida": "SI", "dominio": "civico", "dificultad": "MEDIA",
        **extra,
    }


class GenerarMarcoTests(unittest.TestCase):
    def generate_one(self, report: dict[str, str] | None = None):
        return generate([manifest()], [census()], [report or binary_report()])

    def test_complete_candidate_emits_without_n1_n33_relations_or_evidence(self) -> None:
        result = self.generate_one()
        self.assertEqual(1, len(result.rows))
        self.assertEqual("Q_REAL", result.rows[0]["variable"])
        self.assertEqual("MAN-1", result.rows[0]["origen_manifiesto_id"])
        self.assertEqual("2 :: REPORTADO-NO-EXCLUYENTE-ADR-135", result.rows[0]["n_no_ponderado"])

    def test_manifest_is_start_and_join_is_census_ref_to_batch(self) -> None:
        decoy = binary_report(record_id="R-DECOY", batch_id="E2B-NO-JOIN", variable="Q_DECOY")
        result = generate([manifest(), manifest("MAN-SIN-CENSO")], [census()], [binary_report(), decoy])
        self.assertEqual(["Q_REAL"], [row["variable"] for row in result.rows])
        self.assertEqual(2, result.summary["manifiestos_examinados"])
        self.assertEqual(1, result.summary["entradas_con_e2"])
        self.assertEqual(1, result.summary["lotes_unidos"])

    def test_objetos_logicos_is_count_and_does_not_create_variables(self) -> None:
        result = generate([manifest()], [census()], [])
        self.assertEqual((), result.rows)
        self.assertEqual(0, result.summary["observaciones_examinadas"])

    def test_only_real_variable_seed_is_eligible(self) -> None:
        invalid = [
            binary_report(record_id="OBJ", variable="OBJ-B2-deadbeef"),
            binary_report(record_id="HASH", variable="a" * 64),
            binary_report(record_id="COL", objeto_tipo="COLUMNA", variable="42", localizador="tabla=x#columna=42"),
        ]
        result = generate([manifest()], [census()], invalid + [binary_report()])
        self.assertEqual(["Q_REAL"], [row["variable"] for row in result.rows])

    def test_value_label_observation_can_enrich_but_not_seed_by_itself(self) -> None:
        seed = binary_report(categories="")
        labels = {
            "record_id": "LABELS", "batch_id": "E2B-1", "payload_id": "MAN-1",
            "objeto_tipo": "VALUE-LABEL-COLLECTION-SAV", "variable": "Q_REAL",
            "categorias": "0|1",
        }
        result = generate([manifest()], [census()], [seed, labels])
        self.assertEqual(1, len(result.rows))
        labels["variable"] = "Q_SIN_SEMILLA"
        result = generate([manifest()], [census()], [labels])
        self.assertEqual((), result.rows)

    def test_census_operational_universe_never_fills_population(self) -> None:
        report = binary_report()
        report.pop("universo")
        result = generate(
            [manifest()], [census(universo_declarado="manifiesto.yaml@hash-operativo")], [report]
        )
        self.assertEqual((), result.rows)
        self.assertIn("UNIVERSO_NO_DOCUMENTADO", result.insufficient[0]["motivos"])

    def test_estimator_derivation_for_binary_categorical_numeric_and_admin(self) -> None:
        cases = [
            (binary_report(), "PROPORCION_PONDERADA"),
            (binary_report(tipo_variable="CATEGORICA_EXCLUYENTE", categorias="1|2|3", categorias_excluyentes="SI"), "DISTRIBUCION_PONDERADA"),
            (binary_report(tipo_variable="NUMERICA_CONTINUA", categorias="", rango="0..100", unidad="pesos", codificacion="decimal"), "MEDIA_PONDERADA"),
            (binary_report(tipo_variable="ADMINISTRATIVA", categorias="", rango="0..infinito", unidad="casos", codificacion="conteo", ponderador="NO APLICA", ponderador_exacto="", ponderador_fuente_ola_tabla="", no_aplica_ponderador_documentado="SI", operacion_estimador="SUMA_REGISTRADA"), "SUMA_REGISTRADA"),
        ]
        for index, (report, expected) in enumerate(cases, 1):
            report.update(record_id=f"R-{index}", variable=f"Q_{index}")
            with self.subTest(expected=expected):
                result = self.generate_one(report)
                self.assertEqual(expected, result.rows[0]["estimador"])

    def test_ambiguous_transformations_are_observation_insufficient(self) -> None:
        for kind in ("MULTIRRESPUESTA", "INDICE", "TEXTO", "TRANSFORMACION_AMBIGUA"):
            with self.subTest(kind=kind):
                result = self.generate_one(binary_report(tipo_variable=kind))
                self.assertEqual((), result.rows)
                self.assertEqual("OBSERVACION_INSUFICIENTE", result.insufficient[0]["estado"])

    def test_weight_requires_exact_source_wave_table_attestation(self) -> None:
        result = self.generate_one(binary_report(ponderador="peso_probable", ponderador_exacto="NO"))
        self.assertEqual((), result.rows)
        self.assertIn("PONDERADOR_EXACTO_NO_DOCUMENTADO", result.insufficient[0]["motivos"])

    def test_n_is_reported_but_never_excludes_while_cv_does(self) -> None:
        low_n = self.generate_one(binary_report(n_no_ponderado="1", cv="29.9%"))
        self.assertEqual(1, len(low_n.rows))
        high_cv = self.generate_one(binary_report(n_no_ponderado="100000", cv="30%"))
        self.assertEqual((), high_cv.rows)
        self.assertIn("EXCLUIDA-ADR-135", high_cv.insufficient[0]["motivos"])

        for written, expected in (("1%", "0.01"), ("0.5%", "0.005")):
            with self.subTest(cv=written):
                result = self.generate_one(binary_report(cv=written))
                self.assertEqual(1, len(result.rows))
                self.assertEqual(f"ADMISIBLE-ADR-135-CV={expected}", result.rows[0]["cv_arbitro"])

        negative = self.generate_one(binary_report(cv="-1%"))
        self.assertEqual(1, len(negative.rows))
        self.assertEqual("PENDIENTE-FILTRO-iii-CV", negative.rows[0]["cv_arbitro"])

    def test_output_has_exactly_18_columns_and_real_provenance(self) -> None:
        payload = tsv_bytes(self.generate_one().rows)
        header = payload.decode("utf-8").splitlines()[0].split("\t")
        self.assertEqual(18, len(header))
        self.assertEqual(list(MARCO_FIELDS), header)
        self.assertFalse(payload.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(payload.endswith(b"\n"))

    def test_duplicate_identity_is_deduplicated_and_conflicts_fail_closed(self) -> None:
        duplicate = copy.deepcopy(binary_report())
        duplicate["record_id"] = "R-2"
        result = generate([manifest()], [census()], [binary_report(), duplicate])
        self.assertEqual(1, len(result.rows))
        self.assertEqual(1, result.summary["duplicados"])

        conflicting = copy.deepcopy(duplicate)
        conflicting["record_id"] = "R-3"
        conflicting["universo"] = "otro universo incompatible"
        result = generate([manifest()], [census()], [binary_report(), conflicting])
        self.assertEqual((), result.rows)
        self.assertEqual(1, result.summary["conflictos"])

    def test_same_material_candidate_across_manifests_has_one_stable_provenance(self) -> None:
        second_report = binary_report(record_id="R-2", batch_id="E2B-2", payload_id="MAN-2")
        result = generate(
            [manifest("MAN-2"), manifest("MAN-1")],
            [census("MAN-2", "E2B-2"), census("MAN-1", "E2B-1")],
            [second_report, binary_report()],
        )
        self.assertEqual(1, len(result.rows))
        self.assertEqual("MAN-1", result.rows[0]["origen_manifiesto_id"])
        self.assertEqual(1, result.summary["duplicados"])

    def test_determinism_and_no_claim_beyond_candidate_counts(self) -> None:
        second = binary_report(record_id="R-2", variable="Q_2")
        left = generate([manifest()], [census()], [binary_report(), second])
        right = generate([manifest()], [census()], [second, binary_report()])
        self.assertEqual(tsv_bytes(left.rows), tsv_bytes(right.rows))
        self.assertEqual(diagnostics_bytes(left), diagnostics_bytes(right))
        serialized = (tsv_bytes(left.rows) + diagnostics_bytes(left)).decode("utf-8").lower()
        self.assertNotIn("satur", serialized)
        self.assertNotIn("universo completo", serialized)
        self.assertNotIn("no hay más", serialized)

    def test_missing_filters_remain_pending_and_phrase_is_not_synthesized(self) -> None:
        report = binary_report()
        for field in ("publicada", "grado_dependencia", "cv", "frase_discriminacion", "post_corte_u_ola_retenida"):
            report.pop(field)
        result = self.generate_one(report)
        row = result.rows[0]
        self.assertEqual("PENDIENTE-FILTRO-i", row["publicada"])
        self.assertEqual("PENDIENTE-FILTRO-ii", row["grado_dependencia"])
        self.assertEqual("PENDIENTE-FILTRO-iii-CV", row["cv_arbitro"])
        self.assertEqual("PENDIENTE-FILTRO-iv", row["frase_discriminacion"])
        self.assertEqual("PENDIENTE-FILTRO-v", row["post_corte_u_ola_retenida"])


if __name__ == "__main__":
    unittest.main()
