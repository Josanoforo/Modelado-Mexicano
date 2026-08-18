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

        # Segunda relación, distinta de la primera, para poder someter una
        # ALTA sin que su `relacion_id_actual` agrupe con la propuesta
        # ordinaria en `_apply_layer4` (agrupa por relación, no por lote).
        self.relation_alta = next(
            row for row in leer_tsv(self.registry / "relaciones.tsv")
            if row["clasificacion_relacion"] == "CANDIDATA"
            and row["relacion_id"] != relation["relacion_id"]
        )
        self.material_task_id_alta = "TASK-B2-" + "a1" * 32
        self.task_id_alta = "TSEM-B2-" + "b" * 24
        self.rep_id_alta = "REP-" + "c2" * 32
        self.sha_alta = "d3" * 32
        self.object_id_alta = "OBJ-B2-" + "e4" * 32
        self.report_id_alta = "RPTC-B2-" + "f5" * 32
        self.report_record_id_alta = "E2R-" + "a6" * 32
        self.report_record_sha_alta = "b7" * 32
        self.e2_record_id_alta = "E2R-" + "c8" * 32
        self.e2_record_sha_alta = "d9" * 32
        self.payload_id_alta = "payload_prueba_barrido2_alta"
        material_task_alta = self.task_root / f"{self.material_task_id_alta}.json"
        material_task_alta.write_text('{"network_habilitada":false}\n', encoding="utf-8")

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
        }, {
            "reporte_id": self.report_id_alta,
            "record_id": self.report_record_id_alta,
            "record_sha256": self.report_record_sha_alta,
            "payload_id": self.payload_id_alta,
            "representacion_id": self.rep_id_alta,
            "sha256": self.sha_alta,
            "objeto_logico_id": self.object_id_alta,
        }])
        self.ledger = root / "ledger.tsv"
        write_tsv(self.ledger, ["payload_id", "representacion_id", "sha256"], [{
            "payload_id": self.payload_id,
            "representacion_id": self.rep_id,
            "sha256": self.sha,
        }, {
            "payload_id": self.payload_id_alta,
            "representacion_id": self.rep_id_alta,
            "sha256": self.sha_alta,
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
        self.task_alta = {
            "tarea_id": self.task_id_alta,
            "relacion_id": self.relation_alta["relacion_id"],
            "reporte_id": self.report_id_alta,
            "reporte_record_id": self.report_record_id_alta,
            "reporte_record_sha256": self.report_record_sha_alta,
            "e2_record_id": self.e2_record_id_alta,
            "e2_record_sha256": self.e2_record_sha_alta,
            "payload_id": self.payload_id_alta,
            "representacion_id": self.rep_id_alta,
            "sha256": self.sha_alta,
            "objeto_logico_id": self.object_id_alta,
            "necesidad_id": self.relation_alta["necesidad_id"],
            "reactivo_id": "REACTIVO-PRUEBA-ALTA",
            "fuente_canonica": self.relation_alta["fuente_canonica_normalizada"],
            "frontera_semantica": self.frontier,
            "material_tarea_id": self.material_task_id_alta,
            "material_task_sha256": digest(material_task_alta),
            "material_baseline_sha256": digest(self.material_baseline),
            "curador_id": "CURADOR-PRUEBA",
            "fecha": "2026-08-17",
        }
        write_tsv(self.tasks, TASK_FIELDS, [self.task, self.task_alta])
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

    def proposal_alta(self, *, estado_supervision: str = "VALIDADA") -> dict[str, str]:
        return {
            "propuesta_id": "PROP-B2-" + "b" * 24,
            "tarea_id": self.task_id_alta,
            "reporte_id": self.report_id_alta,
            "payload_id": self.payload_id_alta,
            "representacion_id": self.rep_id_alta,
            "sha256": self.sha_alta,
            "objeto_logico_id": self.object_id_alta,
            "necesidad_id": self.relation_alta["necesidad_id"],
            "reactivo_id": "REACTIVO-PRUEBA-ALTA",
            "accion_propuesta": "ALTA",
            "relacion_id_actual": self.relation_alta["relacion_id"],
            "veredicto_a4": "EXISTE-SATISFACE",
            "evidencia_ref": f"{self.e2_record_id_alta}:{self.e2_record_sha_alta}",
            "frontera_semantica": self.frontier,
            "confianza": "ALTA",
            "requiere_decision_mesa": "NO",
            "decision_mesa_id": "NO-APLICA",
            "dependencia_fp24": "NO",
            "razon_gate": "material nuevo sin par existente en el registro; propone alta de relación",
            "estado_supervision": estado_supervision,
            "supervisor_id": "SUPERVISOR-PRUEBA",
            "fecha": "2026-08-17",
        }

    def run_many(self, proposals: list[dict[str, str]], *, apply: bool = True) -> dict[str, object]:
        write_tsv(self.proposals, PROPOSAL_FIELDS, proposals)
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

    def run(self, proposal: dict[str, str], *, apply: bool = True) -> dict[str, object]:
        return self.run_many([proposal], apply=apply)


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

    def test_validated_alta_does_not_abort_the_batch_and_stays_pending(self) -> None:
        """C5: una `PROPUESTA_ALTA` validada ya no es un error de preflight que
        aborta el lote (`ALTA_REQUIERE_HIGH_PATH_NO_IMPLEMENTADO`, defecto
        encontrado por la auditoría de cinco agentes, `2026-08-18-b2-transfer.md`).
        El lote procesa la propuesta ordinaria (a), la ALTA sale `PROPUESTA_ALTA`
        sin integrarse (b), y una segunda corrida idéntica es idempotente (d)."""
        with tempfile.TemporaryDirectory() as temporary_name:
            fixture = Barrido2Fixture(Path(temporary_name))
            relation_alta_before = dict(fixture.relation_alta)
            ordinary = fixture.proposal()
            alta = fixture.proposal_alta()
            first = fixture.run_many([ordinary, alta])
            # (a) el lote no aborta: `ok` sigue True, no hay `errors`, y la
            # propuesta ordinaria se integra igual que sin la ALTA presente.
            self.assertTrue(first["ok"])
            self.assertNotIn("errors", first)
            self.assertFalse(first["high_path_built"])
            self.assertEqual(1, first["propuestas_altas_validadas"])
            relation = next(
                row for row in leer_tsv(fixture.registry / "relaciones.tsv")
                if row["relacion_id"] == fixture.relation["relacion_id"]
            )
            self.assertEqual("EXISTE-NO-SATISFACE", relation["capa4_apertura_mapeo"])

            with (fixture.output / "decisiones-integracion-barrido2.tsv").open(encoding="utf-8", newline="") as handle:
                decisions = {row["propuesta_id"]: row for row in csv.DictReader(handle, delimiter="\t")}
            self.assertEqual("INTEGRADA", decisions[ordinary["propuesta_id"]]["estado_integracion"])
            # (b) la ALTA queda `PROPUESTA_ALTA` -- ni integrada ni rechazada --
            # y su relación no se toca en absoluto (bytes iguales a antes de correr).
            self.assertEqual("PROPUESTA_ALTA", decisions[alta["propuesta_id"]]["estado_integracion"])
            relation_alta_after = next(
                row for row in leer_tsv(fixture.registry / "relaciones.tsv")
                if row["relacion_id"] == fixture.relation_alta["relacion_id"]
            )
            self.assertEqual(relation_alta_before, relation_alta_after)

            # (c) las dos pruebas de §22 del acto anterior -- corridas como
            # parte de esta misma suite -- siguen verdes; no se tocan aquí.

            # (d) idempotencia: segunda corrida idéntica, diff cero.
            second = fixture.run_many([ordinary, alta])
            self.assertTrue(second["ok"])
            self.assertEqual([], second["changed"])


if __name__ == "__main__":
    unittest.main()
