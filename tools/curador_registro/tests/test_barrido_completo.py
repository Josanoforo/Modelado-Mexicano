from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path

from tools.curador_registro.integrate import integrate
from tools.curador_registro.prepare_production import FORBIDDEN as ANALYST_FORBIDDEN, prepare
from tools.curador_registro.snapshot_universe import Declaration, assign_declaration_ids, reconcile, stable_id
from tools.curador_registro.validate import (
    FORBIDDEN_LEVEL1,
    inspectable_coverage,
    material_exception,
    read_tsv,
    validate,
    validate_level1_input,
)


REPO = Path(__file__).resolve().parents[3]
REGISTRY = REPO / "data" / "curacion-registro"
UNIVERSE = REPO / "data" / "curacion-universo"


class SyntheticIdentityTests(unittest.TestCase):
    def declaration(self, fingerprint: str, url: str, identifier: str) -> Declaration:
        return Declaration(
            input_id="INP-test", localizador=url, identificador=identifier,
            fingerprint=fingerprint, url=url, objeto_logico=identifier, formato="CSV",
        )

    def test_ids_are_independent_of_order(self) -> None:
        left = [self.declaration("f2", "https://example.test/b.csv", "b"), self.declaration("f1", "https://example.test/a.csv", "a")]
        right = list(reversed([self.declaration("f2", "https://example.test/b.csv", "b"), self.declaration("f1", "https://example.test/a.csv", "a")]))
        assign_declaration_ids(left)
        assign_declaration_ids(right)
        self.assertEqual(sorted(row.declaration_id for row in left), sorted(row.declaration_id for row in right))
        self.assertEqual(stable_id("ACT-", "x"), stable_id("ACT-", "x"))

    def test_same_url_is_not_content_identity(self) -> None:
        rows = [self.declaration("one", "https://example.test/a.csv", "catalog-a"), self.declaration("two", "https://example.test/a.csv", "manifest-a")]
        assign_declaration_ids(rows)
        assets, families, _ = reconcile(rows, Path("/nonexistent-corpus"))
        self.assertEqual(2, len({row.declaration_id for row in rows}))
        self.assertEqual(2, len(assets))
        self.assertNotEqual(rows[0].activo_id, rows[1].activo_id)
        self.assertEqual(1, len({row["familia_logica_id"] for row in families}))

    def test_fuzzy_basename_only_creates_candidate(self) -> None:
        rows = [self.declaration("one", "https://one.test/data.csv", "one"), self.declaration("two", "https://two.test/data.csv", "two")]
        assign_declaration_ids(rows)
        assets, _, candidates = reconcile(rows, Path("/nonexistent-corpus"))
        self.assertEqual(2, len(assets))
        self.assertEqual(1, len(candidates))
        self.assertEqual("PENDIENTE", candidates[0]["estado_revision"])

    def test_structural_url_identity_and_declarations_preserve_urls(self) -> None:
        urls = ["https://example.test/a.csv", "https://example.test/b.dbf"]
        rows = [self.declaration(str(i), url, str(i)) for i, url in enumerate(urls)]
        assign_declaration_ids(rows)
        assets, _, _ = reconcile(rows, Path("/nonexistent-corpus"))
        self.assertEqual(2, len(assets))
        self.assertEqual(set(urls), {row.localizador for row in rows})


class LiveMissionInvariantTests(unittest.TestCase):
    def test_t0_snapshot_hashes_and_post_t0_do_not_mutate_denominator(self) -> None:
        snapshot = json.loads((UNIVERSE / "snapshot-t0.json").read_text(encoding="utf-8"))
        assets = read_tsv(UNIVERSE / "universo-declarado-t0.tsv")
        discovered = read_tsv(UNIVERSE / "activos-descubiertos-durante-ronda.tsv")
        self.assertTrue(discovered)
        self.assertEqual(snapshot["conteos"]["componentes_declarados_conservadores"], len(assets))
        self.assertEqual("NO_DETERMINADO", snapshot["conteos"]["denominador_activos_declarados"])
        self.assertEqual("NO_DETERMINADO", snapshot["conteos"]["cobertura_adquisicion_puntual"])
        for name, expected in snapshot["hashes_outputs"].items():
            self.assertEqual(expected, hashlib.sha256((UNIVERSE / name).read_bytes()).hexdigest())

    def test_declared_coverage_uses_unique_assets(self) -> None:
        declarations = read_tsv(UNIVERSE / "declaraciones-activos-t0.tsv")
        assets = read_tsv(UNIVERSE / "universo-declarado-t0.tsv")
        states = read_tsv(UNIVERSE / "estado-activos.tsv")
        self.assertGreater(len(declarations), len(assets))
        self.assertEqual({row["activo_id"] for row in assets}, {row["activo_id"] for row in states})

    def test_duplicates_require_strong_evidence(self) -> None:
        for row in read_tsv(UNIVERSE / "familias-activos.tsv"):
            if row["tipo_relacion"] == "DUPLICADO_VERIFICADO":
                self.assertTrue(row["evidencia_estructural"].startswith("sha256:"))

    def test_acquired_did_not_imply_inspected_in_t0(self) -> None:
        acquired = [row for row in read_tsv(UNIVERSE / "universo-declarado-t0.tsv") if row["estado_adquisicion"] == "ADQUIRIDO"]
        self.assertTrue(acquired)
        self.assertEqual({"ADQUIRIDO_NO_INSPECCIONADO"}, {row["estado_inspeccion"] for row in acquired})

    def test_all_inspectable_acquired_objects_have_report(self) -> None:
        states = read_tsv(UNIVERSE / "estado-activos.tsv")
        reports = read_tsv(UNIVERSE / "reportes-inspeccion.tsv")
        exceptions = read_tsv(UNIVERSE / "excepciones-inspeccion.tsv")
        denominator, numerator, missing = inspectable_coverage(states, reports, exceptions)
        self.assertEqual(denominator, numerator)
        self.assertFalse(missing)

    def test_low_relevance_is_not_material_exception(self) -> None:
        self.assertFalse(material_exception("BAJA_RELEVANCIA"))
        self.assertFalse(material_exception("RESULTADO_NO_PROMETEDOR"))
        self.assertTrue(material_exception("CORRUPCION"))

    def test_level1_contract_omits_semantic_fields(self) -> None:
        columns = set(read_tsv(UNIVERSE / "plan-inspeccion.tsv")[0])
        self.assertFalse(columns & FORBIDDEN_LEVEL1)
        payload = {
            "tarea_observacion_id": "TOBS-x", "run_id": "RUN-x", "snapshot_t0_sha256": "0" * 64,
            "activo_id": "ACT-x", "objeto_logico_id": "OBJ-x", "criterio_parada": "fin",
        }
        self.assertEqual([], validate_level1_input(payload))
        payload["necesidad_id"] = "N1"
        self.assertIn("necesidad_id", validate_level1_input(payload)[0])

    def test_every_recorded_blinding_break_has_exception(self) -> None:
        exceptions = read_tsv(UNIVERSE / "excepciones-cegamiento.tsv")
        self.assertEqual(len(exceptions), len({row["tarea_observacion_id"] for row in exceptions}))
        self.assertTrue(all(row["excepcion_cegamiento_id"].startswith("EXCEG-") for row in exceptions))

    def test_analyst_specs_are_blinded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = prepare(
                REGISTRY / "especificaciones-produccion.json",
                UNIVERSE / "snapshot-t0.json", REGISTRY, Path(tmp),
            )
            for path in paths:
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertFalse(set(payload) & ANALYST_FORBIDDEN)

    def test_inspector_cannot_emit_adjudication(self) -> None:
        reports = read_tsv(UNIVERSE / "reportes-inspeccion.tsv")
        self.assertTrue(reports)
        self.assertFalse({"adjudicacion_semantica", "clasificacion_relacion", "necesidad_id", "relacion_id"} & set(reports[0]))

    def test_new_level1_objects_cannot_receive_need(self) -> None:
        for row in read_tsv(UNIVERSE / "objetos-observados-no-representados.tsv"):
            self.assertEqual("NO_DETERMINADO", row["posible_necesidad"])
            self.assertEqual("NO_DETERMINADO", row["razon_inferencia"])

    def test_no_observed_requires_universe_method_and_boundary(self) -> None:
        for row in read_tsv(UNIVERSE / "reportes-inspeccion.tsv"):
            if row["afirmacion_tipo"] == "NO_OBSERVADO_EN_UNIVERSO_INSPECCIONADO":
                self.assertTrue(row["objeto_inspeccionado"])
                self.assertTrue(row["universo_inspeccionado"])
                self.assertTrue(row["metodo"])
                self.assertTrue(row["limitacion"])

    def test_no_access_does_not_become_negative(self) -> None:
        for row in read_tsv(REGISTRY / "bootstrap-semantico.tsv"):
            if row["clasificacion_relacion_legacy"] == "NO_ACCESIBLE":
                self.assertEqual("NO_ACCESIBLE", row["estado_evidencia"])
                self.assertEqual("CANDIDATA", row["adjudicacion_semantica"])

    def test_denominators_are_separate(self) -> None:
        dashboard = json.loads((UNIVERSE / "tablero-cobertura.json").read_text(encoding="utf-8"))
        coverage = dashboard["coberturas"]
        baseline = read_tsv(REGISTRY / "relaciones.tsv")
        candidate_count = sum(row["clasificacion_relacion"] == "CANDIDATA" for row in baseline)
        self.assertNotEqual(coverage["COBERTURA_DECLARADA"]["denominador"], coverage["COBERTURA_BOOTSTRAP_RUTEO"]["denominador"])
        self.assertNotEqual(coverage["RELACIONES_CON_CALCULO_DESCRIPTIVO"]["denominador"], coverage["COBERTURA_BOOTSTRAP_RUTEO"]["denominador"])
        self.assertEqual(
            {"numerador": len(baseline), "denominador": len(baseline)},
            coverage["COBERTURA_BOOTSTRAP_RUTEO"],
        )
        self.assertEqual(candidate_count, coverage["COBERTURA_SEMANTICA_EJECUTADA_COLA"]["denominador"])
        self.assertEqual({"numerador": 2, "denominador": 3}, coverage["RELACIONES_CON_CALCULO_DESCRIPTIVO"])
        self.assertEqual({"numerador": 1, "denominador": 3}, coverage["RELACIONES_LISTAS_PARA_USO_MODELO"])

    def test_semantic_identity_and_destination_are_stable(self) -> None:
        baseline = read_tsv(REGISTRY / "relaciones.tsv")
        boot = read_tsv(REGISTRY / "bootstrap-semantico.tsv")
        self.assertEqual({row["relacion_id"] for row in baseline}, {row["relacion_id"] for row in boot})
        self.assertTrue(all(row["destino_procesamiento"] for row in boot))

    def test_state_is_not_propagated_by_source(self) -> None:
        by_source: dict[str, set[str]] = defaultdict(set)
        for row in read_tsv(REGISTRY / "relaciones.tsv"):
            by_source[row["fuente_canonica_normalizada"]].add(row["clasificacion_relacion"])
        self.assertTrue(any(len(states) > 1 for states in by_source.values()))

    def test_negatives_aliases_fusion_and_decisions_are_preserved(self) -> None:
        manifest = json.loads((REGISTRY / "baseline.json").read_text(encoding="utf-8"))
        relations = read_tsv(REGISTRY / "relaciones.tsv")
        self.assertEqual(manifest["conteos"]["negativas"], sum(row["clasificacion_relacion"] == "NEGATIVA" for row in relations))
        self.assertEqual(manifest["conteos"]["familias_alias"], len(read_tsv(REGISTRY / "aliases-fuentes.tsv")))
        self.assertEqual(manifest["conteos"]["fusiones_declaradas"], len(read_tsv(REGISTRY / "fusiones-relaciones.tsv")))
        decisions = read_tsv(REGISTRY / "decisiones-humanas.tsv")
        self.assertEqual({"DH-332a13a70cbbf875", "DH-ea9e932f3970ce12"}, {row["decision_id"] for row in decisions})
        self.assertEqual({"PENDIENTE"}, {row["estado_decision"] for row in decisions})

    def test_need_to_model_object_mapping_has_37_declared_rows(self) -> None:
        mapping = read_tsv(REGISTRY / "necesidad-objeto-modelo.tsv")
        self.assertEqual(37, len(mapping))
        self.assertEqual({f"N{number}" for number in range(1, 34)}, {row["necesidad_id"] for row in mapping})
        self.assertEqual(
            {"R7.4", "R7.5"},
            {row["objeto_modelo_origen"] for row in mapping if row["necesidad_id"] == "N27"},
        )

    def test_production_requires_material_specification(self) -> None:
        production = read_tsv(REGISTRY / "produccion-modelo.tsv")
        self.assertEqual(11, len(production))
        self.assertEqual(10, sum(row["estado"] == "CALCULO_REPRODUCIBLE" for row in production))
        for row in production:
            if row["estado"] == "CALCULO_REPRODUCIBLE":
                self.assertNotIn("NO_DETERMINADO", {row["n"], row["suma_pesos"], row["unidad"], row["incertidumbre"]})

    def test_obsolete_noop_proposals_are_not_retroactively_integrated(self) -> None:
        rows = read_tsv(REGISTRY / "integracion-barrido" / "integracion-propuestas.tsv")
        self.assertEqual([], rows)
        result = json.loads((REGISTRY / "integracion-barrido" / "integracion-validada.json").read_text(encoding="utf-8"))
        self.assertEqual(0, result["cambios_adjudicacion_integrados"])
        self.assertTrue(result["expediente_completo"])
        integrity = result["validacion_baseline_original_intacto"]
        self.assertEqual(integrity["hashes_antes"], integrity["hashes_despues"])

    def test_residual_queue_has_concrete_destinations(self) -> None:
        residual = read_tsv(REGISTRY / "cola-residual.tsv")
        self.assertTrue(residual)
        self.assertTrue(all(row["siguiente_accion"] and row["criterio_cierre"] for row in residual))
        self.assertFalse(any("investigar más" in row["siguiente_accion"].casefold() for row in residual))
        self.assertEqual(2, sum(row["capa"] == "DECISION_HUMANA" for row in residual))

    def test_full_validator_passes(self) -> None:
        result = validate(REPO)
        self.assertTrue(result["ok"], result["errores"])


class FailClosedIntegrationTests(unittest.TestCase):
    def test_inference_cannot_be_integrated_as_fact(self) -> None:
        report = read_tsv(UNIVERSE / "reportes-inspeccion.tsv")[0]
        relation = read_tsv(REGISTRY / "relaciones.tsv")[0]
        snapshot_hash = json.loads((UNIVERSE / "snapshot-t0.json").read_text(encoding="utf-8"))["snapshot_t0_sha256"]
        baseline_hash = hashlib.sha256((REGISTRY / "baseline.json").read_bytes()).hexdigest()
        fields = [
            "propuesta_id", "snapshot_t0_sha256", "baseline_sha256", "reporte_inspeccion_ref", "relacion_id", "accion",
            "afirmacion_origen_tipo", "tratar_como_hecho", "adjudicacion_propuesta", "evidencia_nueva_material",
            "cegamiento_roto", "excepcion_cegamiento_ref", "reserva",
        ]
        proposal = {
            "propuesta_id": "P-test", "snapshot_t0_sha256": snapshot_hash, "baseline_sha256": baseline_hash,
            "reporte_inspeccion_ref": report["reporte_id"], "relacion_id": relation["relacion_id"],
            "accion": "CONSERVAR_ADJUDICACION", "afirmacion_origen_tipo": "INFERENCIA_PROPUESTA",
            "tratar_como_hecho": "SI", "adjudicacion_propuesta": relation["clasificacion_relacion"],
            "evidencia_nueva_material": "NO", "cegamiento_roto": "NO", "excepcion_cegamiento_ref": "NO_APLICA", "reserva": "test",
        }
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            proposal_path = tmp_path / "proposal.tsv"
            report_path = tmp_path / "report.tsv"
            with proposal_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
                writer.writeheader(); writer.writerow(proposal)
            with report_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(report), delimiter="\t", lineterminator="\n")
                writer.writeheader(); writer.writerow(report)
            result = integrate(REGISTRY, UNIVERSE / "snapshot-t0.json", proposal_path, [report_path], tmp_path / "out")
            self.assertEqual(1, result["rechazadas"])
            decision = read_tsv(tmp_path / "out" / "integracion-propuestas.tsv")[0]
            self.assertIn("INFERENCIA_COMO_HECHO", decision["razones"])


if __name__ == "__main__":
    unittest.main()
