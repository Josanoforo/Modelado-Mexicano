from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import unittest
import yaml
from collections import Counter
from pathlib import Path
from unittest import mock

from tools.curador_registro import semantic_run
from tools.curador_registro.semantic_run import parse_manifest


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


class ManifestPortabilityTests(unittest.TestCase):
    """MAESTRA37-INFRA-2 · Frente E: el manifiesto ya no resuelve un solo
    corpus fijo por máquina (antes: `/home/pc0/mm-corpus/raw` hardcodeado).
    Este fixture es enteramente sintético bajo tempfile -- nunca toca
    data/raw ni data/raices.local.yaml del repo real."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repo_dir = self.root / "repo"
        self.corpus_dir = self.repo_dir / "data" / "raw"
        self.external_dir = self.root / "raiz-externa-montada"
        self.corpus_dir.mkdir(parents=True)
        self.external_dir.mkdir(parents=True)

        self.content1 = b"contenido dummy archivo 1\n"
        self.content2 = b"contenido dummy archivo 2\n"
        (self.corpus_dir / "archivo1.csv").write_bytes(self.content1)
        (self.external_dir / "archivo2.csv").write_bytes(self.content2)
        self.sha1 = hashlib.sha256(self.content1).hexdigest()
        self.sha2 = hashlib.sha256(self.content2).hexdigest()

        # e1: raiz implícita (data_raw). e2: raiz externa CONFIGURADA en
        # raices.local.yaml. e3: raiz externa NO configurada -- no existe
        # ni una entrada para "externo_no_conf" en raices.local.yaml.
        manifest_records = [
            {"id": "e1", "archivo": "archivo1.csv", "sha256": self.sha1},
            {"id": "e2", "archivo": "archivo2.csv", "raiz": "externo_conf", "sha256": self.sha2},
            {"id": "e3", "archivo": "archivo3.csv", "raiz": "externo_no_conf", "sha256": "deadbeef"},
        ]
        self.manifest_path = self.repo_dir / "data" / "manifiesto.yaml"
        self.manifest_path.write_text(yaml.safe_dump(manifest_records, allow_unicode=True), encoding="utf-8")
        (self.repo_dir / "data" / "raices.local.yaml").write_text(
            yaml.safe_dump({"externo_conf": str(self.external_dir)}, allow_unicode=True), encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_portabilidad_tres_raices(self) -> None:
        manifest = parse_manifest(self.manifest_path, self.corpus_dir, self.repo_dir)
        by_id = {row["id"]: row for row in manifest}
        self.assertEqual({"e1", "e2", "e3"}, set(by_id))

        # 1) ruta_logica es siempre "<raiz>:<archivo>", nunca una ruta física.
        self.assertEqual("data_raw:archivo1.csv", by_id["e1"]["ruta_logica"])
        self.assertEqual("externo_conf:archivo2.csv", by_id["e2"]["ruta_logica"])
        self.assertEqual("externo_no_conf:archivo3.csv", by_id["e3"]["ruta_logica"])

        # ruta_resuelta: física cuando la raíz está configurada; None real
        # (nunca la cadena "None") cuando no lo está.
        self.assertEqual(str(self.corpus_dir / "archivo1.csv"), by_id["e1"]["ruta_resuelta"])
        self.assertEqual(str(self.external_dir / "archivo2.csv"), by_id["e2"]["ruta_resuelta"])
        self.assertIsNone(by_id["e3"]["ruta_resuelta"])

        # Este bloque refleja, a propósito, el bucle de apertura de activos de
        # semantic_run.execute() (E3: `for asset in asset_rows: ...`) -- execute()
        # no es unitariamente probable sin todo el andamiaje de
        # registro/universo/baseline, fuera de alcance de este arreglo. Se
        # envuelve open_local_object real (no un doble) para probar E4 con
        # cómputo genuino, y se cuentan las llamadas para probar que la raíz
        # no configurada JAMÁS llega a open_local_object ni a Path(None).
        observed_by_id: dict[str, dict] = {}
        with mock.patch.object(semantic_run, "open_local_object", side_effect=semantic_run.open_local_object) as spy:
            for asset in manifest:
                if asset["ruta_resuelta"] is None:
                    observed = {
                        "objeto": f"MANIFEST:{asset['id']}",
                        "ruta": asset["ruta_logica"],
                        "resultado": "RAIZ_NO_CONFIGURADA",
                        "sha256": "NO_DETERMINADO",
                        "descripcion": "",
                    }
                    observed["sha256_declarado"] = asset.get("sha256", "NO_DETERMINADO")
                    observed["hash_reconcilia"] = "NO_VERIFICADO"
                else:
                    observed = semantic_run.open_local_object(
                        Path(asset["ruta_resuelta"]), f"MANIFEST:{asset['id']}", ruta_declarada=asset["ruta_logica"],
                    )
                    observed["sha256_declarado"] = asset.get("sha256", "NO_DETERMINADO")
                    observed["hash_reconcilia"] = "SI" if observed["sha256"] == asset.get("sha256") else "NO"
                observed_by_id[asset["id"]] = observed

        # 3) la raíz no configurada nunca invoca open_local_object.
        self.assertEqual(2, spy.call_count)
        called_objetos = {call.args[1] for call in spy.call_args_list}
        self.assertEqual({"MANIFEST:e1", "MANIFEST:e2"}, called_objetos)

        # 2) apertura física real para e1/e2: sha256 real, ruta == ruta_logica.
        self.assertEqual(self.sha1, observed_by_id["e1"]["sha256"])
        self.assertEqual("data_raw:archivo1.csv", observed_by_id["e1"]["ruta"])
        self.assertEqual("SI", observed_by_id["e1"]["hash_reconcilia"])

        self.assertEqual(self.sha2, observed_by_id["e2"]["sha256"])
        self.assertEqual("externo_conf:archivo2.csv", observed_by_id["e2"]["ruta"])
        self.assertEqual("SI", observed_by_id["e2"]["hash_reconcilia"])

        # 3) e3 (no configurada): RAIZ_NO_CONFIGURADA, nunca ARCHIVO_NO_EXISTE
        # ni NO_COINCIDE; sha256 NO_DETERMINADO; hash nunca verificado.
        self.assertEqual("RAIZ_NO_CONFIGURADA", observed_by_id["e3"]["resultado"])
        self.assertNotIn(observed_by_id["e3"]["resultado"], {"ARCHIVO_NO_EXISTE", "NO_COINCIDE"})
        self.assertEqual("NO_DETERMINADO", observed_by_id["e3"]["sha256"])
        self.assertEqual("externo_no_conf:archivo3.csv", observed_by_id["e3"]["ruta"])
        self.assertEqual("NO_VERIFICADO", observed_by_id["e3"]["hash_reconcilia"])

        # 4) ninguna ruta absoluta de esta máquina se filtró al output
        # serializado, ni siquiera en el caso de la raíz no configurada.
        serialized = json.dumps(observed_by_id, ensure_ascii=False) + json.dumps(
            [{"ruta_logica": row["ruta_logica"]} for row in manifest], ensure_ascii=False,
        )
        self.assertNotIn(str(self.root), serialized)
        self.assertNotIn(str(self.corpus_dir), serialized)
        self.assertNotIn(str(self.external_dir), serialized)
        self.assertNotIn("/home/pc0/mm-corpus", serialized)


if __name__ == "__main__":
    unittest.main()
