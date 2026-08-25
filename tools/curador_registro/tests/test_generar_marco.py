from __future__ import annotations

import csv
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import yaml

from tools.curador_registro.generar_marco import (
    MARCO_FIELDS,
    diagnostics_bytes,
    generate_from_e2_paths,
    tsv_bytes,
)
from tools.curador_registro.tests.test_marco_e2_adapter import e2_record, jsonl_bytes


def tsv_text(rows: list[dict[str, object]]) -> str:
    if not rows:
        raise ValueError("fixture TSV vacío")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=list(rows[0]),
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def complete_authority(variable: str = "Q_REAL", **overrides: str) -> dict[str, str]:
    authority = {
        "representacion_id": "REP-" + "4" * 64,
        "tabla": "hogar",
        "objeto_padre_id": "OBJ-B2-" + "7" * 64,
        "variable": variable,
        "encuesta": "ENCUESTA-CANONICA",
        "ola": "2024",
        "universo_poblacional": "personas adultas residentes",
        "tipo_estadistico": "BINARIA",
        "codificacion": "0=No|1=Sí",
        "missing": "9=No especificado",
        "ponderador": "FAC_EXACTO",
        "ponderador_exacto": "SI",
        "ponderador_fuente_ola_tabla": "SI",
        "cita_procedencia": "DOC-ESTRUCTURADO-1#tabla=hogar#variable=Q_REAL",
    }
    authority.update(overrides)
    return authority


class CorpusFixture:
    def __init__(self, root: Path):
        self.root = root
        self.manifest = root / "manifest.yaml"
        self.census = root / "census.tsv"
        self.ledger = root / "ledger.tsv"
        self.t0 = root / "t0.tsv"
        self.contract = root / "contract.json"
        self.baseline = root / "baseline.json"
        self.index = root / "e2-neutral-index.jsonl"
        self.compact = root / "compact.tsv"
        record = e2_record()
        self.manifest.write_text(
            yaml.safe_dump([{"id": "MAN-1", "archivo": "activo.dta"}], sort_keys=True),
            encoding="utf-8",
        )
        self.census.write_text(
            tsv_text(
                [
                    {
                        "id_manifiesto": "MAN-1",
                        "representacion_id": record["representacion_id"],
                        "reporte_neutral_ref": record["batch_id"],
                        "sha256_observado": record["sha256"],
                        "objetos_logicos": "999",
                        "universo_declarado": "universo operativo de activos",
                    }
                ]
            ),
            encoding="utf-8",
        )
        self.ledger.write_text(
            tsv_text(
                [
                    {
                        "representacion_id": record["representacion_id"],
                        "reporte_neutral_ref": record["batch_id"],
                        "payload_id": record["payload_id"],
                        "sha256": record["sha256"],
                    }
                ]
            ),
            encoding="utf-8",
        )
        self.t0.write_text(
            tsv_text(
                [
                    {
                        "hash_local": record["sha256"],
                        "fuente_programa": "data_raw",
                        "edicion_periodo": "2026-08-17",
                    }
                ]
            ),
            encoding="utf-8",
        )
        self.contract.write_text(
            json.dumps(
                {
                    "schema_version": "BARRIDO2-CONTRACT-1.0",
                    "private_e2_index": ".barrido2/private/e2-neutral-index.jsonl",
                }
            ),
            encoding="utf-8",
        )
        self.compact.write_text(
            tsv_text(
                [
                    {
                        "batch_id": record["batch_id"],
                        "objeto_tipo": "VARIABLE-DTA",
                        "descripcion_neutral": "objetos=999;muestra=E2R-compacta",
                    }
                ]
            ),
            encoding="utf-8",
        )

    def run(
        self,
        records: list[dict[str, object]],
        *,
        authority: list[dict[str, str]] | None = None,
    ):
        payload = jsonl_bytes(records)
        self.index.write_bytes(payload)
        self.baseline.write_text(
            json.dumps({"e2_index_sha256": hashlib.sha256(payload).hexdigest()}),
            encoding="utf-8",
        )
        return generate_from_e2_paths(
            repo=self.root,
            manifest_path=self.manifest,
            census_path=self.census,
            ledger_path=self.ledger,
            declared_universe_path=self.t0,
            contract_path=self.contract,
            baseline_path=self.baseline,
            index_path=self.index,
            compact_report_path=self.compact,
            semantic_authority=authority or (),
        )


class GenerarMarcoCorpusRealTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = CorpusFixture(Path(self.temporary.name))

    def test_real_e2_name_creates_seed_but_compact_never_does(self) -> None:
        result = self.fixture.run([e2_record()])
        self.assertEqual(1, result.diagnostics["resumen"]["semillas_reales"])
        self.assertEqual(0, result.diagnostics["resumen"]["candidatas_emitidas"])
        self.assertEqual(1, result.diagnostics["validacion_indice"]["reporte_compacto_filas_control"])
        empty = self.fixture.run([])
        self.assertEqual(0, empty.diagnostics["resumen"]["semillas_reales"])

    def test_missing_compact_report_is_visible_but_not_gating(self) -> None:
        self.fixture.compact.unlink()
        result = self.fixture.run([e2_record()], authority=[complete_authority()])
        self.assertEqual(1, len(result.rows))
        validation = result.diagnostics["validacion_indice"]
        self.assertEqual("AUSENTE_NO_GATING", validation["reporte_compacto_estado"])
        self.assertEqual(0, validation["reporte_compacto_filas_control"])

    def test_file_identity_and_ingestion_date_are_not_survey_or_wave(self) -> None:
        result = self.fixture.run([e2_record()])
        coverage = result.diagnostics["cobertura_campos"]
        self.assertEqual(1, coverage["variable"]["EXISTE_ESTRUCTURADO"])
        self.assertEqual(1, coverage["encuesta"]["NO_SEMANTICAMENTE_APTO"])
        self.assertEqual(1, coverage["ola"]["NO_SEMANTICAMENTE_APTO"])
        reasons = result.diagnostics["razones_insuficiencia"]
        self.assertEqual(1, reasons["ENCUESTA_NO_SEMANTICAMENTE_APTA"])
        self.assertEqual(1, reasons["OLA_NO_SEMANTICAMENTE_APTA"])

    def test_operational_census_universe_never_fills_population(self) -> None:
        result = self.fixture.run([e2_record(poblacion="NO-APLICA")])
        self.assertEqual(
            1,
            result.diagnostics["razones_insuficiencia"][
                "UNIVERSO_POBLACIONAL_AUSENTE_EN_CONTRATO"
            ],
        )

    def test_categories_and_labels_are_preserved_but_do_not_invent_semantics(self) -> None:
        result = self.fixture.run([e2_record()])
        evidence = result.diagnostics["evidencia_e2_estructurada"]
        self.assertEqual(1, evidence["categorias"])
        self.assertEqual(1, evidence["value_labels"])
        coverage = result.diagnostics["cobertura_campos"]
        self.assertEqual(1, coverage["estimador"]["AUSENTE_EN_CONTRATO"])
        self.assertEqual(1, coverage["escala"]["AUSENTE_EN_CONTRATO"])

    def test_physical_numeric_type_is_not_promoted_to_continuous(self) -> None:
        result = self.fixture.run([e2_record(definicion="tipo_fisico=float64")])
        self.assertEqual(
            1,
            result.diagnostics["razones_insuficiencia"][
                "TIPO_ESTADISTICO_AUSENTE_EN_CONTRATO"
            ],
        )

    def test_ambiguous_weight_authority_is_conflictive(self) -> None:
        authority = complete_authority()
        result = self.fixture.run([e2_record()], authority=[authority, dict(authority)])
        self.assertEqual(0, len(result.rows))
        self.assertEqual(1, result.diagnostics["resumen"]["conflictos"])
        self.assertEqual(
            1,
            result.diagnostics["cobertura_campos"]["ponderador"]["CONFLICTIVO"],
        )

    def test_n1_enrichment_without_e2_seed_cannot_create_candidate(self) -> None:
        n1_enrichment = complete_authority()
        n1_enrichment["record_id"] = "N1-1"
        result = self.fixture.run([], authority=[n1_enrichment])
        self.assertEqual(0, result.diagnostics["resumen"]["semillas_reales"])
        self.assertEqual((), result.rows)

    def test_complete_candidate_requires_explicit_structured_authority(self) -> None:
        incomplete = complete_authority()
        incomplete.pop("missing")
        self.assertEqual(
            (), self.fixture.run([e2_record()], authority=[incomplete]).rows
        )
        complete = self.fixture.run(
            [e2_record(poblacion="personas adultas residentes")],
            authority=[complete_authority(universo_poblacional="")],
        )
        self.assertEqual(1, len(complete.rows))
        self.assertEqual("Q_REAL", complete.rows[0]["variable"])
        self.assertEqual("PROPORCION_PONDERADA", complete.rows[0]["estimador"])
        self.assertIn("value_labels", complete.rows[0]["escala"])

    def test_weight_requires_exact_source_wave_table_attestation(self) -> None:
        authority = complete_authority(ponderador_fuente_ola_tabla="NO")
        result = self.fixture.run([e2_record()], authority=[authority])
        self.assertEqual((), result.rows)
        self.assertEqual(
            1,
            result.diagnostics["razones_insuficiencia"][
                "PONDERADOR_EXACTO_SCOPE_AUSENTE_EN_CONTRATO"
            ],
        )

    def test_unweighted_n_is_non_excluding_and_output_has_18_columns(self) -> None:
        result = self.fixture.run([e2_record()], authority=[complete_authority()])
        self.assertEqual(1, len(result.rows))
        self.assertEqual(
            "POR_MEDIR :: NO-EXCLUYENTE-ADR-135",
            result.rows[0]["n_no_ponderado"],
        )
        header = tsv_bytes(result.rows).decode("utf-8").splitlines()[0].split("\t")
        self.assertEqual(18, len(header))
        self.assertEqual(list(MARCO_FIELDS), header)

    def test_order_and_serialization_are_deterministic(self) -> None:
        second = e2_record(
            record_id="E2R-" + "8" * 64,
            objeto_logico_id="OBJ-B2-" + "9" * 64,
            nombre="Q_2",
        )
        authority = [complete_authority(), complete_authority("Q_2")]
        left = self.fixture.run([e2_record(), second], authority=authority)
        repeated = self.fixture.run([e2_record(), second], authority=authority)
        right = self.fixture.run([second, e2_record()], authority=authority)
        self.assertEqual(tsv_bytes(left.rows), tsv_bytes(repeated.rows))
        self.assertEqual(diagnostics_bytes(left), diagnostics_bytes(repeated))
        self.assertEqual(tsv_bytes(left.rows), tsv_bytes(right.rows))

    def test_diagnostic_never_claims_saturation(self) -> None:
        result = self.fixture.run([e2_record()])
        serialized = (tsv_bytes(result.rows) + diagnostics_bytes(result)).decode(
            "utf-8"
        ).lower()
        self.assertNotIn("satur", serialized)
        self.assertNotIn("universo completo", serialized)
        self.assertNotIn("no hay más", serialized)


if __name__ == "__main__":
    unittest.main()
