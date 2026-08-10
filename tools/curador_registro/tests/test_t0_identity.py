from __future__ import annotations

import hashlib
import csv
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from tools.curador_registro.derive_recovered import PRIMERA, REUTILIZADA, derive
from tools.curador_registro.snapshot_universe import Declaration, assign_declaration_ids, reconcile


REPO = Path(__file__).resolve().parents[3]
UNIVERSE = REPO / "data" / "curacion-universo"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class CorrectedT0IdentityTests(unittest.TestCase):
    def declaration(self, fingerprint: str, url: str, digest: str = "", local_path: str = "") -> Declaration:
        return Declaration(
            input_id="INP-test", localizador=url or f"data_raw:{local_path}",
            identificador=fingerprint, fingerprint=fingerprint, url=url,
            local_path=local_path, sha256=digest, objeto_logico=fingerprint,
            formato="CSV",
        )

    def test_same_url_with_incompatible_hashes_remains_two_assets(self) -> None:
        rows = [
            self.declaration("a", "https://example.test/landing", "a" * 64),
            self.declaration("b", "https://example.test/landing", "b" * 64),
        ]
        assign_declaration_ids(rows)
        assets, families, _ = reconcile(rows, Path("/nonexistent-corpus"))
        self.assertEqual(2, len(assets))
        self.assertEqual(2, len({row.activo_id for row in rows}))
        self.assertEqual(1, len({row["familia_logica_id"] for row in families}))
        self.assertEqual({"LOCALIZADOR_COMPARTIDO"}, {row["tipo_relacion"] for row in families})

    def test_common_landing_without_hash_does_not_merge_assets(self) -> None:
        url = "https://example.test/catalogo"
        rows = [self.declaration("uno", url), self.declaration("dos", url), self.declaration("tres", url)]
        assign_declaration_ids(rows)
        assets, _, _ = reconcile(rows, Path("/nonexistent-corpus"))
        self.assertEqual(3, len(assets))

    def test_identical_sha256_is_strong_duplicate_evidence(self) -> None:
        digest = "c" * 64
        rows = [
            self.declaration("uno", "https://one.test/a.csv", digest),
            self.declaration("dos", "https://two.test/b.csv", digest),
        ]
        assign_declaration_ids(rows)
        assets, _, _ = reconcile(rows, Path("/nonexistent-corpus"))
        self.assertEqual(1, len(assets))
        self.assertEqual(rows[0].activo_id, rows[1].activo_id)

    def test_local_asset_hash_is_observed_from_path_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = b"contenido observado"
            (root / "dato.csv").write_bytes(payload)
            row = self.declaration("local", "", "0" * 64, "dato.csv")
            assign_declaration_ids([row])
            assets, _, _ = reconcile([row], root)
            observed = hashlib.sha256(payload).hexdigest()
            self.assertEqual(observed, assets[0]["hash_local"])
            self.assertEqual(observed, hashlib.sha256((root / assets[0]["ruta_local"]).read_bytes()).hexdigest())
            self.assertEqual("0" * 64, row.hash_declarado)

    def test_live_counts_are_derived_independently_from_corpus(self) -> None:
        snapshot = json.loads((UNIVERSE / "snapshot-t0.json").read_text(encoding="utf-8"))
        counts = snapshot["conteos"]
        corpus = Path(snapshot["corpus_root"])
        paths = sorted(path for path in corpus.rglob("*") if path.is_file())
        digests = [sha256_file(path) for path in paths]
        unique_digests = set(digests)
        self.assertEqual(len(paths), counts["representaciones_locales"])
        self.assertEqual(len(unique_digests), counts["contenidos_locales_sha256_unicos"])
        self.assertEqual(len(paths) - len(unique_digests), counts["duplicados_locales_reales"])
        self.assertEqual(len(paths), counts["hashes_representaciones_locales_verificados"])
        assets = [row for row in read_tsv(UNIVERSE / "universo-declarado-t0.tsv") if row["estado_adquisicion"] == "ADQUIRIDO"]
        self.assertEqual(len(unique_digests), len(assets))
        self.assertEqual(len(assets), counts["identidades_locales_verificadas"])
        self.assertEqual(len(assets), counts["numerador_adquirido_identidades_locales_verificadas"])
        self.assertEqual(unique_digests, {row["hash_local"] for row in assets})
        for asset in assets:
            path = Path(snapshot["corpus_root"]) / asset["ruta_local"]
            self.assertEqual(asset["hash_local"], sha256_file(path))

    def test_declared_components_are_labeled_as_upper_bound_not_point_denominator(self) -> None:
        snapshot = json.loads((UNIVERSE / "snapshot-t0.json").read_text(encoding="utf-8"))
        counts = snapshot["conteos"]
        declarations = read_tsv(UNIVERSE / "declaraciones-activos-t0.tsv")
        components = read_tsv(UNIVERSE / "universo-declarado-t0.tsv")
        self.assertEqual(len(declarations), counts["declaraciones_parseadas"])
        self.assertEqual(len(components), counts["componentes_declarados_conservadores"])
        self.assertEqual(len(components), counts["cota_superior_activos_declarados"])
        self.assertEqual("NO_DETERMINADO", counts["denominador_activos_declarados"])
        self.assertEqual("NO_DETERMINADO", counts["cobertura_adquisicion_puntual"])
        self.assertNotIn("activos_unicos", counts)

    def test_ledger_conditions_are_derived_without_literal_oracles(self) -> None:
        assets = {
            row["activo_id"] for row in read_tsv(UNIVERSE / "universo-declarado-t0.tsv")
            if row["estado_adquisicion"] == "ADQUIRIDO"
        }
        reused = {row["activo_id"] for row in read_tsv(UNIVERSE / "reutilizacion-inspecciones.tsv")}
        ledger = read_tsv(UNIVERSE / "ledger-inspecciones-t0.tsv")
        self.assertEqual(assets, {row["activo_id"] for row in ledger})
        by_condition = {
            condition: {row["activo_id"] for row in ledger if row["condicion"] == condition}
            for condition in (REUTILIZADA, PRIMERA)
        }
        self.assertEqual(reused, by_condition[REUTILIZADA])
        self.assertEqual(assets - reused, by_condition[PRIMERA])
        self.assertEqual(
            len(assets), sum(Counter(row["condicion"] for row in ledger).values())
        )
        self.assertTrue(all("/tmp/" not in value for row in ledger for value in row.values()))

    def test_ledger_rerun_is_byte_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / "ledger-inspecciones-t0.tsv"
            recovered = root / "objetos-recuperados-t0.tsv"
            derive(UNIVERSE, recovered, ledger)
            first = (ledger.read_bytes(), recovered.read_bytes())
            self.assertEqual((UNIVERSE / ledger.name).read_bytes(), first[0])
            self.assertEqual((UNIVERSE / recovered.name).read_bytes(), first[1])
            derive(UNIVERSE, recovered, ledger)
            second = (ledger.read_bytes(), recovered.read_bytes())
            self.assertEqual(first, second)

    def test_active_blinding_exceptions_have_complete_current_joins(self) -> None:
        snapshot = json.loads((UNIVERSE / "snapshot-t0.json").read_text(encoding="utf-8"))
        contracts = {}
        with (UNIVERSE / "contratos-inspeccion.jsonl").open(encoding="utf-8") as handle:
            for line in handle:
                payload = json.loads(line)
                contracts[payload["tarea_observacion_id"]] = payload
        report_groups: dict[str, list[dict[str, str]]] = {}
        for row in read_tsv(UNIVERSE / "reportes-inspeccion.tsv"):
            report_groups.setdefault(row["tarea_observacion_id"], []).append(row)
        active = read_tsv(UNIVERSE / "excepciones-cegamiento.tsv")
        for row in active:
            task = row["tarea_observacion_id"]
            self.assertIn(task, contracts)
            self.assertIn(task, report_groups)
            self.assertEqual(snapshot["snapshot_t0_sha256"], row["snapshot_t0_sha256"])
            self.assertEqual(canonical_sha(contracts[task]), row["contrato_input_sha256"])
            report_groups[task].sort(
                key=lambda item: (item["reporte_id"], item["afirmacion_tipo"], canonical_sha(item))
            )
            self.assertEqual(canonical_sha(report_groups[task]), row["reporte_filas_sha256"])
            self.assertEqual("ACTIVA_REFERENCIALIDAD_COMPLETA", row["estado"])
        history = read_tsv(UNIVERSE / "excepciones-cegamiento-historicas.tsv")
        self.assertTrue(history)
        self.assertFalse({row["excepcion_cegamiento_id"] for row in active}.intersection(
            row["excepcion_cegamiento_id"] for row in history
        ))
        for row in history:
            self.assertEqual("HISTORICA_NO_ACTIVA", row["estado_historia"])
            self.assertNotEqual(snapshot["snapshot_t0_sha256"], row["snapshot_t0_sha256_historico"])
            self.assertNotIn(row["tarea_observacion_id"], contracts)


if __name__ == "__main__":
    unittest.main()
