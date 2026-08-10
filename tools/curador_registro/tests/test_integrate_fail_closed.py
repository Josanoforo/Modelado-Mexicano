from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.curador_registro.baseline import ARCHIVOS_TSV
from tools.curador_registro.integrate import integrate, read_tsv, validate_integration_dossier


REPO = Path(__file__).resolve().parents[3]
REGISTRY = REPO / "data" / "curacion-registro"
UNIVERSE = REPO / "data" / "curacion-universo"


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class IntegrationFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.inspector = root / "inspector"
        self.curator = root / "curator"
        self.output = root / "output"
        self.inspector.mkdir(parents=True)
        self.curator.mkdir(parents=True)
        snapshot = json.loads((UNIVERSE / "snapshot-t0.json").read_text(encoding="utf-8"))
        self.snapshot_hash = snapshot["snapshot_t0_sha256"]
        self.baseline_hash = sha256(REGISTRY / "baseline.json")
        assets = {row["activo_id"]: row for row in read_tsv(UNIVERSE / "universo-declarado-t0.tsv")}
        evidence = {row["relacion_id"]: row for row in read_tsv(REGISTRY / "evidencias.tsv")}
        linked = next(
            row for row in read_tsv(REGISTRY / "bootstrap-semantico.tsv")
            if row.get("activo_id_vinculado") in assets and row.get("relacion_id") in evidence
        )
        self.relation_id = linked["relacion_id"]
        self.asset = assets[linked["activo_id_vinculado"]]
        self.provenance_id = evidence[self.relation_id]["procedencia_id"]
        relation = next(row for row in read_tsv(REGISTRY / "relaciones.tsv") if row["relacion_id"] == self.relation_id)
        self.current = relation["clasificacion_relacion"]
        self.task_id = "TOBS-test-integracion"
        self.report_id = "RINS-test-integracion"
        self.proposal_id = "PADJ-test-integracion"
        self.task = {
            "tarea_observacion_id": self.task_id,
            "run_id": "RUN-test-integracion",
            "snapshot_t0_sha256": self.snapshot_hash,
            "activo_id": self.asset["activo_id"],
            "objeto_logico_id": self.asset["objeto_logico_id"],
            "familia_logica_id": self.asset.get("familia_logica_id", "NO_DETERMINADO"),
            "rutas_localizadores": [self.asset.get("ruta_local", "NO_DETERMINADO")],
            "grado_inspeccion": "SEMANTICA_DIRIGIDA",
            "criterio_parada": "reporte neutral emitido",
        }
        self.report = {
            "reporte_id": self.report_id,
            "tarea_observacion_id": self.task_id,
            "activo_id": self.asset["activo_id"],
            "objeto_logico_id": self.asset["objeto_logico_id"],
            "afirmacion_tipo": "HECHO_OBSERVADO",
            "objeto_inspeccionado": self.asset["objeto_logico"],
            "universo_inspeccionado": "activo completo",
            "metodo": "prueba determinista",
            "valor_o_descripcion": "hecho de prueba",
            "evidencia_ref": "sha256:" + (self.asset.get("hash_local") or "0" * 64),
            "localizador": self.asset.get("ruta_local", "NO_DETERMINADO"),
            "limitacion": "prueba sintética",
            "bloqueo": "NINGUNO",
            "siguiente_objeto_no_inspeccionado": "NINGUNO",
        }
        self.proposal = {
            "propuesta_id": self.proposal_id,
            "snapshot_t0_sha256": self.snapshot_hash,
            "baseline_sha256": self.baseline_hash,
            "reporte_inspeccion_ref": self.report_id,
            "tarea_observacion_id": self.task_id,
            "activo_id": self.asset["activo_id"],
            "objeto_logico_id": self.asset["objeto_logico_id"],
            "procedencia_ref": self.provenance_id,
            "relacion_id": self.relation_id,
            "accion": "CONSERVAR_ADJUDICACION",
            "afirmacion_origen_tipo": "HECHO_OBSERVADO",
            "tratar_como_hecho": "NO",
            "adjudicacion_propuesta": self.current,
            "evidencia_nueva_material": "NO",
            "cegamiento_roto": "NO",
            "excepcion_cegamiento_ref": "NO_APLICA",
            "reserva": "prueba de integración",
        }
        self.curator_task = {
            "tarea_curacion_id": "TCUR-test-integracion",
            "run_id": "RUN-test-integracion",
            "snapshot_t0_sha256": self.snapshot_hash,
            "baseline_sha256": self.baseline_hash,
            "asignaciones": [{
                "relacion_id": self.relation_id,
                "reporte_inspeccion_ref": self.report_id,
                "activo_id": self.asset["activo_id"],
            }],
            "criterio_parada": "propuesta o terminal explícito",
        }

    def materialize(self, proposals: list[dict[str, str]] | None = None, with_curator_input: bool = True) -> Path:
        proposal_path = self.curator / "adjudicaciones-propuestas.tsv"
        write_tsv(proposal_path, proposals or [self.proposal])
        write_json(self.inspector / "input.json", self.task)
        write_tsv(self.inspector / "reporte-inspeccion.tsv", [self.report])
        write_json(self.inspector / "hashes.json", {
            "input.json": sha256(self.inspector / "input.json"),
            "reporte-inspeccion.tsv": sha256(self.inspector / "reporte-inspeccion.tsv"),
        })
        if with_curator_input:
            write_json(self.curator / "input.json", self.curator_task)
        curator_hashes = {proposal_path.name: sha256(proposal_path)}
        if with_curator_input:
            curator_hashes["input.json"] = sha256(self.curator / "input.json")
        write_json(self.curator / "hashes.json", curator_hashes)
        return proposal_path

    def run(self, proposal_path: Path) -> dict[str, object]:
        return integrate(REGISTRY, UNIVERSE / "snapshot-t0.json", proposal_path, [self.inspector], self.output)


class FailClosedDossierTests(unittest.TestCase):
    def test_complete_schema_joins_and_unique_proposal_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = IntegrationFixture(Path(tmp))
            result = fixture.run(fixture.materialize())
            self.assertTrue(result["ok"], result["errores_expediente"])
            self.assertTrue(result["expediente_completo"])
            decision = read_tsv(fixture.output / "integracion-propuestas.tsv")[0]
            for field in fixture.proposal:
                self.assertEqual(fixture.proposal[field], decision[field])
            integrity = result["validacion_baseline_original_intacto"]
            self.assertEqual(integrity["hashes_antes"], integrity["hashes_despues"])
            self.assertFalse(integrity["diferencias"])

    def test_integrated_task_input_must_exist_and_be_hashed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = IntegrationFixture(Path(tmp))
            result = fixture.run(fixture.materialize(with_curator_input=False))
            self.assertFalse(result["ok"])
            self.assertIn("TAREA_CURADOR_INEXISTENTE", result["errores_expediente"])
            self.assertEqual(1, result["rechazadas"])

    def test_duplicate_proposal_and_relation_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = IntegrationFixture(Path(tmp))
            duplicate = dict(fixture.proposal)
            result = fixture.run(fixture.materialize([fixture.proposal, duplicate]))
            self.assertFalse(result["ok"])
            self.assertIn("PROPUESTA_ID_DUPLICADA", result["errores_expediente"])
            self.assertIn("RELACION_PROPUESTA_DUPLICADA", result["errores_expediente"])
            self.assertEqual(2, result["rechazadas"])

    def test_proposal_report_asset_join_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = IntegrationFixture(Path(tmp))
            broken = dict(fixture.proposal)
            broken["activo_id"] = "ACT-inexistente"
            result = fixture.run(fixture.materialize([broken]))
            self.assertFalse(result["ok"])
            self.assertIn("JOIN_PROPUESTA_REPORTE_INVALIDO", result["errores_expediente"])
            self.assertIn("RELACION_ACTIVO_NO_ASIGNADO", result["errores_expediente"])

    def test_validator_rechecks_versioned_dossier_instead_of_trusting_flags(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = IntegrationFixture(root / "worker")
            result = fixture.run(fixture.materialize())
            self.assertTrue(result["ok"])
            registry = root / "repo" / "data" / "curacion-registro"
            universe = root / "repo" / "data" / "curacion-universo"
            schemas = root / "repo" / "tools" / "curador_registro" / "schemas"
            registry.mkdir(parents=True)
            universe.mkdir(parents=True)
            schemas.mkdir(parents=True)
            for name in [*ARCHIVOS_TSV.values(), "baseline.json", "bootstrap-semantico.tsv"]:
                shutil.copy2(REGISTRY / name, registry / name)
            for name in ["snapshot-t0.json", "universo-declarado-t0.tsv", "excepciones-cegamiento.tsv"]:
                shutil.copy2(UNIVERSE / name, universe / name)
            for name in [
                "adjudication-proposal.schema.json", "inspection-report.schema.json",
                "inspector-task.schema.json", "semantic-curator-task.schema.json",
            ]:
                shutil.copy2(REPO / "tools" / "curador_registro" / "schemas" / name, schemas / name)
            shutil.copytree(fixture.output, registry / "integracion-barrido")
            fake_repo = root / "repo"
            self.assertEqual([], validate_integration_dossier(fake_repo))
            with (registry / "integracion-barrido" / "integracion-propuestas.tsv").open("a", encoding="utf-8") as handle:
                handle.write("alteracion\n")
            self.assertIn(
                "EXPEDIENTE_HASH_INVALIDO:integracion-propuestas.tsv",
                validate_integration_dossier(fake_repo),
            )


if __name__ == "__main__":
    unittest.main()
