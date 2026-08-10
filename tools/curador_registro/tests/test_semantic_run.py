from __future__ import annotations

import csv
import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
REGISTRY = REPO / "data/curacion-registro"
SEMANTIC = REGISTRY / "ejecucion-semantica"
FORBIDDEN_NEUTRAL = {"relacion_id", "necesidad_id", "adjudicacion_vigente", "objeto_modelo_origen"}
TERMINALS = {
    "EJECUTADA_CON_RESULTADO", "NO_ALCANZO_TRAS_INTENTOS",
    "FUENTE_ABIERTA_SIN_OBJETO_REQUERIDO", "BLOQUEADA_INPUT_FALTANTE",
    "REQUIERE_DECISION_HUMANA", "NO_CORRIDA",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SemanticRunRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((SEMANTIC / "manifest.json").read_text(encoding="utf-8"))
        cls.run_dir = SEMANTIC / "runs" / cls.manifest["run_id"]
        cls.relations = {row["relacion_id"]: row for row in rows(REGISTRY / "relaciones.tsv")}
        cls.candidates = {rid for rid, row in cls.relations.items() if row["clasificacion_relacion"] == "CANDIDATA"}

    def test_original_actions_and_individual_closure_are_preserved(self) -> None:
        evidence = {row["relacion_id"]: row for row in rows(REGISTRY / "evidencias.tsv") if row["relacion_id"] in self.candidates}
        utility = {row["relacion_id"]: row for row in rows(REGISTRY / "utilidad-modelo.tsv")}
        work = {row["relacion_id"]: row for row in rows(REGISTRY / "trabajo-semantico.tsv")}
        preserved = {row["relacion_id"]: row for row in rows(SEMANTIC / "acciones-originales-preservadas.tsv")}
        results = {row["relacion_id"]: row for row in rows(self.run_dir / "resultados-acciones.tsv")}
        self.assertEqual(self.candidates, set(preserved))
        self.assertEqual(self.candidates, set(results))
        for rid in self.candidates:
            self.assertEqual(evidence[rid]["siguiente_accion"], preserved[rid]["siguiente_accion_original"])
            self.assertEqual(evidence[rid]["evidencia_ref"], preserved[rid]["evidencia_ref_original"])
            self.assertEqual(utility[rid]["verificacion_requerida"], preserved[rid]["input_requerido_original"])
            self.assertEqual(utility[rid]["reserva"], preserved[rid]["reserva_original"])
            self.assertEqual(work[rid]["criterio_cierre"], preserved[rid]["criterio_cierre_individual"])
            self.assertEqual(preserved[rid]["siguiente_accion_original"], results[rid]["siguiente_accion_original"])
            self.assertEqual(preserved[rid]["criterio_cierre_individual"], results[rid]["criterio_cierre_individual"])

    def test_partitions_are_disjoint_and_derive_complete_denominator(self) -> None:
        assigned: list[str] = []
        for partition in rows(self.run_dir / "particiones.tsv"):
            relation_ids = [rid for rid in partition["relaciones"].split(";") if rid]
            self.assertEqual(int(partition["numero_relaciones"]), len(relation_ids))
            assigned.extend(relation_ids)
        self.assertEqual(len(assigned), len(set(assigned)))
        self.assertEqual(self.candidates, set(assigned))

    def test_neutral_inputs_and_reports_are_blinded_and_hash_joined(self) -> None:
        supervisor = rows(self.run_dir / "mapa-privado-supervisor.tsv")
        self.assertEqual(self.candidates, {row["relacion_id"] for row in supervisor})
        for link in supervisor:
            input_path = REPO / link["input_inspector_ref"]
            report_path = REPO / link["reporte_neutral_ref"]
            curator_path = REPO / link["input_curador_ref"]
            inspector = json.loads(input_path.read_text(encoding="utf-8"))
            report = json.loads(report_path.read_text(encoding="utf-8"))
            curator = json.loads(curator_path.read_text(encoding="utf-8"))
            self.assertFalse(FORBIDDEN_NEUTRAL.intersection(inspector))
            self.assertFalse(FORBIDDEN_NEUTRAL.intersection(report))
            self.assertEqual(inspector["tarea_observacion_id"], report["tarea_observacion_id"])
            self.assertEqual(sha256(input_path), report["input_sha256"])
            self.assertEqual(sha256(report_path), curator["reporte_neutral_sha256"])
            self.assertEqual(link["relacion_id"], curator["relacion_id"])
            self.assertEqual(0, report["afirmaciones_semanticas_como_hecho"])

    def test_searches_performed_real_bounded_attempts_or_show_missing_locator(self) -> None:
        results = {row["tarea_observacion_id"]: row for row in rows(self.run_dir / "resultados-acciones.tsv")}
        for report_path in (self.run_dir / "reportes-neutrales").glob("*.json"):
            report = json.loads(report_path.read_text(encoding="utf-8"))
            result = results[report["tarea_observacion_id"]]
            if result["tipo_trabajo"] != "BUSQUEDA_DIRIGIDA":
                continue
            self.assertTrue(report["objetos_abiertos"])
            self.assertTrue(any(row["resultado"] == "ABIERTO_REFERENCIA_MAIN" for row in report["objetos_abiertos"]))
            self.assertLessEqual(len(report["intentos"]), 2)
            if report["universo_inspeccionado"]["localizadores_declarados"]:
                self.assertTrue(report["intentos"])
                self.assertTrue(all(item["orden"] in {1, 2} for item in report["intentos"]))
                self.assertFalse(any(item["resultado_http_archivo_error"] == "NO_CORRIDA_RED_DESHABILITADA" for item in report["intentos"]))

    def test_supervision_recalculates_states_and_rejects_no_relation(self) -> None:
        proposals = rows(self.run_dir / "propuestas-curador.tsv")
        supervision = rows(self.run_dir / "supervision.tsv")
        self.assertEqual(self.candidates, {row["relacion_id"] for row in proposals})
        self.assertEqual(self.candidates, {row["relacion_id"] for row in supervision})
        self.assertEqual(len(proposals), len({row["propuesta_id"] for row in proposals}))
        for row in supervision:
            self.assertIn(row["estado_recalculado"], TERMINALS)
            self.assertEqual("SI", row["accion_preservada"])
            self.assertEqual("SI", row["joins_validos"])
            self.assertEqual("SI", row["hashes_validos"])
            self.assertEqual("SI", row["cegamiento_validado"])
            self.assertEqual("NINGUNO", row["errores"])
        self.assertNotIn("NO_CORRIDA", Counter(row["estado_recalculado"] for row in supervision))

    def test_manifest_coverage_is_derived_from_disk(self) -> None:
        results = rows(self.run_dir / "resultados-acciones.tsv")
        supervision = rows(self.run_dir / "supervision.tsv")
        executed = sum(row["estado_recalculado"] != "NO_CORRIDA" for row in supervision)
        coverage = self.manifest["coberturas"]
        self.assertEqual(len(self.candidates), self.manifest["denominador_candidatas_derivado"])
        self.assertEqual({"numerador": len(results), "denominador": len(self.candidates)}, coverage["EXPEDIENTES_ADMINISTRATIVOS_MATERIALIZADOS"])
        self.assertEqual({"numerador": executed, "denominador": len(self.candidates)}, coverage["COBERTURA_SEMANTICA_EJECUTADA_COLA"])
        self.assertEqual(0, coverage["PROPUESTAS_INTEGRABLES"]["numerador"])
        self.assertNotIn("UNIVERSO_SEMANTICO_PROCESADO", json.dumps(self.manifest))

    def test_integrate_compatible_interface_is_explicitly_empty_and_hashed(self) -> None:
        proposal_path = self.run_dir / "propuestas-integrate-compatibles.tsv"
        input_path = self.run_dir / "input.json"
        hashes = json.loads((self.run_dir / "hashes.json").read_text(encoding="utf-8"))
        self.assertEqual([], rows(proposal_path))
        self.assertEqual(self.manifest["run_id"], json.loads(input_path.read_text(encoding="utf-8"))["run_id"])
        self.assertEqual(sha256(proposal_path), hashes["files"][proposal_path.name])
        self.assertEqual(sha256(input_path), hashes["files"][input_path.name])
        dossier = rows(self.run_dir / "expediente-integracion.tsv")
        self.assertEqual(self.candidates, {row["relacion_id"] for row in dossier})
        self.assertTrue(all(row["destino_integracion"] == "NO_ENVIAR" for row in dossier))


if __name__ == "__main__":
    unittest.main()
