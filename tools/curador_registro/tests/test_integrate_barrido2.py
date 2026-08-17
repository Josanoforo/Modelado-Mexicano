from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.curador_registro.baseline import ARCHIVOS_TSV, leer_tsv, validar_baseline
from tools.curador_registro.integrate_barrido2 import (
    PROPOSAL_FIELDS,
    TASK_FIELDS,
    integrate_barrido2,
    registry_hashes,
)


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "data/curacion-registro"
UNIVERSE = ROOT / "data/curacion-universo"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class Barrido2Fixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.registry = root / "registry"
        self.registry.mkdir()
        for filename in [*ARCHIVOS_TSV.values(), "baseline.json", "bootstrap-semantico.tsv", "trabajo-semantico.tsv"]:
            shutil.copy2(REGISTRY / filename, self.registry / filename)
        # La pertenencia histórica no es una regla del integrador. El fixture
        # elige dinámicamente una relación cuya propia procedencia menciona el
        # caso, y demuestra que dependencia_fp24=NO se procesa ordinariamente.
        relation = next(
            row for row in leer_tsv(self.registry / "relaciones.tsv")
            if row["clasificacion_relacion"] == "CANDIDATA" and "gemela" in row.get("nota", "").lower()
        )
        self.relation = relation
        # La tarea semántica tiene identidad propia; el descriptor material que
        # le da su hash se nombra aparte, para que dos relaciones puedan
        # apoyarse en la misma representación sin colisionar de tarea_id.
        self.material_task_id = "TASK-B2-" + "1" * 64
        self.task_id = "TSEM-B2-" + "a" * 24
        self.rep_id = "REP-" + "2" * 64
        self.sha = "3" * 64
        self.object_id = "OBJ-B2-" + "4" * 64
        self.report_id = "RPTC-B2-" + "5" * 64
        self.report_record_id = "E2R-" + "6" * 64
        self.report_record_sha = "7" * 64
        self.e2_record_id = "E2R-" + "8" * 64
        self.e2_record_sha = "9" * 64
        self.payload_id = "payload_prueba_barrido2"
        self.frontier = "representación sintética completa; observaciones no persistidas"
        self.task_root = root / "material-tasks"
        self.task_root.mkdir()
        material_task = self.task_root / f"{self.material_task_id}.json"
        material_task.write_text('{"network_habilitada":false}\n', encoding="utf-8")

        self.reports = root / "reports.tsv"
        report_fields = [
            "reporte_id", "record_id", "record_sha256", "payload_id",
            "representacion_id", "sha256", "objeto_logico_id",
        ]
        write_tsv(self.reports, report_fields, [{
            "reporte_id": self.report_id,
            "record_id": self.report_record_id,
            "record_sha256": self.report_record_sha,
            "payload_id": self.payload_id,
            "representacion_id": self.rep_id,
            "sha256": self.sha,
            "objeto_logico_id": self.object_id,
        }])
        self.ledger = root / "ledger.tsv"
        write_tsv(self.ledger, ["payload_id", "representacion_id", "sha256"], [{
            "payload_id": self.payload_id,
            "representacion_id": self.rep_id,
            "sha256": self.sha,
        }])
        self.material_baseline = root / "material-baseline.json"
        self.material_baseline.write_text(json.dumps({
            "network_habilitada": False,
            "reports": {"durable_sha256": digest(self.reports)},
            "ledger_sha256": digest(self.ledger),
        }, sort_keys=True) + "\n", encoding="utf-8")
        self.tasks = root / "tasks.tsv"
        self.task = {
            "tarea_id": self.task_id,
            "relacion_id": relation["relacion_id"],
            "reporte_id": self.report_id,
            "reporte_record_id": self.report_record_id,
            "reporte_record_sha256": self.report_record_sha,
            "e2_record_id": self.e2_record_id,
            "e2_record_sha256": self.e2_record_sha,
            "payload_id": self.payload_id,
            "representacion_id": self.rep_id,
            "sha256": self.sha,
            "objeto_logico_id": self.object_id,
            "necesidad_id": relation["necesidad_id"],
            "reactivo_id": "REACTIVO-PRUEBA",
            "fuente_canonica": relation["fuente_canonica_normalizada"],
            "frontera_semantica": self.frontier,
            "material_tarea_id": self.material_task_id,
            "material_task_sha256": digest(material_task),
            "material_baseline_sha256": digest(self.material_baseline),
            "curador_id": "CURADOR-PRUEBA",
            "fecha": "2026-08-17",
        }
        write_tsv(self.tasks, TASK_FIELDS, [self.task])
        self.proposals = root / "proposals.tsv"
        self.output = root / "output"

    def proposal(self, *, dependency: str = "NO") -> dict[str, str]:
        blocked = dependency == "SI"
        return {
            "propuesta_id": "PROP-B2-" + "a" * 24,
            "tarea_id": self.task_id,
            "reporte_id": self.report_id,
            "payload_id": self.payload_id,
            "representacion_id": self.rep_id,
            "sha256": self.sha,
            "objeto_logico_id": self.object_id,
            "necesidad_id": self.relation["necesidad_id"],
            "reactivo_id": "REACTIVO-PRUEBA",
            "accion_propuesta": "CAMBIO",
            "relacion_id_actual": self.relation["relacion_id"],
            "veredicto_a4": "EXISTE-NO-SATISFACE",
            "evidencia_ref": f"{self.e2_record_id}:{self.e2_record_sha}",
            "frontera_semantica": self.frontier,
            "confianza": "ALTA",
            "requiere_decision_mesa": "SI" if blocked else "NO",
            "decision_mesa_id": "FP-24" if blocked else "NO-APLICA",
            "dependencia_fp24": dependency,
            "razon_gate": (
                "aceptar esta propuesta exige decidir la regla pendiente de pares"
                if blocked else "evidencia fuente/objeto-específica; no decide política de pares"
            ),
            "estado_supervision": "REQUIERE_DECISION_FP24" if blocked else "VALIDADA",
            "supervisor_id": "SUPERVISOR-PRUEBA",
            "fecha": "2026-08-17",
        }

    def run(self, proposal: dict[str, str], *, apply: bool = True) -> dict[str, object]:
        write_tsv(self.proposals, PROPOSAL_FIELDS, [proposal])
        return integrate_barrido2(
            self.registry,
            self.material_baseline,
            self.proposals,
            self.tasks,
            self.reports,
            self.ledger,
            self.task_root,
            REGISTRY / "necesidad-objeto-modelo.tsv",
            UNIVERSE / "declaraciones-activos-t0.tsv",
            UNIVERSE / "universo-declarado-t0.tsv",
            UNIVERSE / "estado-activos.tsv",
            REGISTRY / "reglas-clasificacion-trabajo.json",
            self.output,
            apply=apply,
        )


class Barrido2IntegrationTests(unittest.TestCase):
    def test_source_specific_historical_case_with_fp24_no_integrates_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_name:
            fixture = Barrido2Fixture(Path(temporary_name))
            first = fixture.run(fixture.proposal())
            self.assertTrue(first["ok"])
            self.assertFalse(first["high_path_built"])
            self.assertEqual(0, first["propuestas_altas_validadas"])
            self.assertTrue(validar_baseline(fixture.registry)["ok"])
            relation = next(
                row for row in leer_tsv(fixture.registry / "relaciones.tsv")
                if row["relacion_id"] == fixture.relation["relacion_id"]
            )
            self.assertEqual("EXISTE-NO-SATISFACE", relation["capa4_apertura_mapeo"])
            second = fixture.run(fixture.proposal())
            self.assertTrue(second["ok"])
            self.assertEqual([], second["changed"])

    def test_any_fp24_dependency_cannot_be_integrated_while_open(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_name:
            fixture = Barrido2Fixture(Path(temporary_name))
            before = registry_hashes(fixture.registry)
            result = fixture.run(fixture.proposal(dependency="SI"))
            self.assertTrue(result["ok"])
            self.assertEqual(before, registry_hashes(fixture.registry))
            with (fixture.output / "decisiones-integracion-barrido2.tsv").open(encoding="utf-8", newline="") as handle:
                decision = next(csv.DictReader(handle, delimiter="\t"))
            self.assertEqual("REQUIERE_DECISION_FP24", decision["estado_integracion"])
            self.assertNotEqual("INTEGRADA", decision["estado_integracion"])


if __name__ == "__main__":
    unittest.main()
