from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.curador_registro.marco_e2_adapter import (
    E2AdapterError,
    E2IndexReader,
    ProvenanceIndex,
    is_variable_seed,
    resolve_private_index,
)


def e2_record(**overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
        "schema_version": "BARRIDO2-E2-1.0",
        "record_id": "E2R-" + "1" * 64,
        "record_sha256": "2" * 64,
        "batch_id": "E2B-" + "3" * 64,
        "batch_sha256": "3" * 64,
        "payload_id": "MAN-1",
        "representacion_id": "REP-" + "4" * 64,
        "sha256": "5" * 64,
        "objeto_logico_id": "OBJ-B2-" + "6" * 64,
        "root_id": "data_raw",
        "ruta_relativa": "fuente/activo.dta",
        "format": ".dta",
        "depth": 0,
        "localizador": "tabla=hogar#variable=Q_REAL",
        "objeto_tipo": "VARIABLE-DTA",
        "nombre": "Q_REAL",
        "etiqueta": "",
        "texto_reactivo": "",
        "definicion": "tipo_fisico=int64",
        "categorias": ["0", "1"],
        "value_labels": ["0=No", "1=Sí"],
        "unidad": "NO-APLICA",
        "periodo": "NO-APLICA",
        "poblacion": "NO-APLICA",
        "pagina": "NO-APLICA",
        "hoja": "NO-APLICA",
        "tabla": "hogar",
        "objeto_padre_id": "OBJ-B2-" + "7" * 64,
        "relacion_estructural": "CONTENIDO-EN-OBJETO",
        "frontera_inspeccion": "estructura completa",
        "parser": "barrido2-stdlib-1+pandas-stata",
        "parser_version": "BARRIDO2-MATERIAL-1.1",
        "estado": "E2-COMPLETO",
        "privacidad": "DEPURADO",
        "fecha": "2026-08-17",
    }
    record.update(overrides)
    return record


def jsonl_bytes(records: list[dict[str, object]]) -> bytes:
    return b"".join(
        (
            json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        for record in records
    )


class E2IndexReaderTests(unittest.TestCase):
    def test_streams_real_schema_and_validates_sha(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "e2-neutral-index.jsonl"
            payload = jsonl_bytes([e2_record()])
            path.write_bytes(payload)
            reader = E2IndexReader(path)
            records = list(reader)
            reader.require_sha(hashlib.sha256(payload).hexdigest())
            self.assertEqual(1, reader.records_read)
            self.assertEqual("Q_REAL", records[0]["nombre"])

    def test_missing_or_wrong_sha_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract = root / "contract.json"
            contract.write_text(
                json.dumps({"private_e2_index": ".barrido2/private/e2-neutral-index.jsonl"}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(E2AdapterError, "INDICE_E2_AUSENTE"):
                resolve_private_index(root, contract)
            path = root / "e2-neutral-index.jsonl"
            path.write_bytes(jsonl_bytes([e2_record()]))
            resolved, _ = resolve_private_index(root, contract, path)
            reader = E2IndexReader(resolved)
            list(reader)
            with self.assertRaisesRegex(E2AdapterError, "SHA256_DIVERGENTE"):
                reader.require_sha("0" * 64)

            declared = root / ".barrido2/private/e2-neutral-index.jsonl"
            declared.parent.mkdir(parents=True)
            declared.write_bytes(path.read_bytes())
            resolved, _ = resolve_private_index(root, contract)
            self.assertEqual(declared, resolved)

    def test_compact_sample_is_not_a_seed_but_real_name_is(self) -> None:
        compact = {
            "objeto_tipo": "VARIABLE-DTA",
            "descripcion_neutral": "VARIABLE-DTA; objetos=40; muestra=E2R-x",
        }
        self.assertFalse(is_variable_seed(compact))
        self.assertTrue(is_variable_seed(e2_record()))
        self.assertFalse(is_variable_seed(e2_record(objeto_tipo="COLUMNA")))


class ProvenanceIndexTests(unittest.TestCase):
    def index(self, *, duplicate_t0: bool = False) -> ProvenanceIndex:
        record = e2_record()
        t0 = [
            {
                "hash_local": record["sha256"],
                "fuente_programa": "data_raw",
                "edicion_periodo": "2026-08-17",
            }
        ]
        if duplicate_t0:
            t0.append(dict(t0[0]))
        return ProvenanceIndex(
            [{"id": "MAN-1"}],
            [
                {
                    "id_manifiesto": "MAN-1",
                    "representacion_id": record["representacion_id"],
                    "reporte_neutral_ref": record["batch_id"],
                    "sha256_observado": record["sha256"],
                }
            ],
            [
                {
                    "representacion_id": record["representacion_id"],
                    "reporte_neutral_ref": record["batch_id"],
                    "payload_id": record["payload_id"],
                    "sha256": record["sha256"],
                }
            ],
            t0,
        )

    def test_exact_join_uses_ids_and_hashes(self) -> None:
        resolution = self.index().resolve(e2_record())
        self.assertEqual("EXACTA", resolution.status)
        self.assertEqual("MAN-1", resolution.provenance.manifest_id)
        self.assertEqual(e2_record()["sha256"], resolution.provenance.hash_local)

    def test_ambiguous_and_absent_join_fail_closed(self) -> None:
        self.assertEqual("AMBIGUA", self.index(duplicate_t0=True).resolve(e2_record()).status)
        changed = e2_record(sha256="8" * 64)
        self.assertEqual("AUSENTE", self.index().resolve(changed).status)

    def test_repairs_only_t0_absent_with_exact_census_and_ledger(self) -> None:
        record = e2_record()
        index = ProvenanceIndex(
            [{"id": "MAN-1"}],
            [
                {
                    "id_manifiesto": "MAN-1",
                    "representacion_id": record["representacion_id"],
                    "reporte_neutral_ref": record["batch_id"],
                    "sha256_observado": record["sha256"],
                }
            ],
            [
                {
                    "representacion_id": record["representacion_id"],
                    "reporte_neutral_ref": record["batch_id"],
                    "payload_id": record["payload_id"],
                    "sha256": record["sha256"],
                }
            ],
            [],
        )

        self.assertEqual("AUSENTE", index.resolve(record).status)
        repaired = index.resolve_repaired(record)
        self.assertEqual("EXACTA_REPARADA", repaired.status)
        self.assertEqual(
            "T0_AUSENTE_RECONSTRUIDO_POR_CENSO_LEDGER_HASH", repaired.reason
        )

        no_census = ProvenanceIndex([{"id": "MAN-1"}], [], [], [])
        self.assertEqual("AUSENTE", no_census.resolve_repaired(record).status)


if __name__ == "__main__":
    unittest.main()
