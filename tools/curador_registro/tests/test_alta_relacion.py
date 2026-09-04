import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from tools.curador_registro.baseline import (
    ARCHIVOS_TSV, leer_tsv, objeto_evidencia_id, relacion_id, validar_baseline,
)
from tools.curador_registro.alta_relacion import AltaRelacionError, run

BASELINE_JSON = "baseline.json"
NOMBRES = [*ARCHIVOS_TSV.values(), BASELINE_JSON]


def _escribir_tsv(path: Path, campos: list[str], filas: list[dict[str, str]]) -> None:
    lineas = ["\t".join(campos)]
    for fila in filas:
        lineas.append("\t".join(str(fila.get(c, "")) for c in campos))
    path.write_text("\n".join(lineas) + "\n", encoding="utf-8")


class AltaRelacionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.registro = self.root / "registro"
        self.registro.mkdir()

        self.necesidad_id = "N1"
        self.fuente_semilla = "FUENTE_SEMILLA"
        self.objeto_semilla = "OBJ-SEMILLA-0000000000000000"
        self.rid_semilla = relacion_id(self.necesidad_id, self.fuente_semilla, self.objeto_semilla)

        # ── relaciones.tsv (19 columnas reales) ──
        self.campos_relaciones = [
            "relacion_id", "necesidad_id", "fuente_canonica_normalizada",
            "objeto_evidencia_id_canonico", "fuente_nombre", "tipo_fuente",
            "id_manifiesto", "sha256_fuente", "capa1_universo_indexado",
            "capa2_manifiesto", "capa3_disco_real", "capa4_apertura_mapeo",
            "clasificacion_relacion", "reason_code", "evidencia_ref",
            "evidencia_textual_breve", "confianza", "conflicto_material", "nota",
        ]
        fila_relacion_semilla = {
            "relacion_id": self.rid_semilla, "necesidad_id": self.necesidad_id,
            "fuente_canonica_normalizada": self.fuente_semilla,
            "objeto_evidencia_id_canonico": self.objeto_semilla,
            "fuente_nombre": "Fuente Semilla", "tipo_fuente": "FUENTE_DATOS",
            "id_manifiesto": "NO_DETERMINADO", "sha256_fuente": "NO_DETERMINADO",
            "capa1_universo_indexado": "NO_DETERMINADO",
            "capa2_manifiesto": "NO_REFERENCIADO", "capa3_disco_real": "NO_REFERENCIADO",
            "capa4_apertura_mapeo": "", "clasificacion_relacion": "CANDIDATA",
            "reason_code": "SEMILLA_TEST", "evidencia_ref": "MAIN:test/semilla.md",
            "evidencia_textual_breve": "NO_DETERMINADO", "confianza": "MEDIA",
            "conflicto_material": "NO", "nota": "fila semilla de prueba",
        }
        _escribir_tsv(self.registro / "relaciones.tsv", self.campos_relaciones, [fila_relacion_semilla])

        # ── evidencias.tsv (27 columnas reales) ──
        self.campos_evidencias = [
            "procedencia_id", "relacion_id", "necesidad_id",
            "fuente_canonica_normalizada", "objeto_evidencia_id_canonico",
            "procedencia_necesidad_id", "procedencia_fuente",
            "procedencia_objeto_evidencia_id", "accion_normalizacion",
            "clasificacion_relacion", "tipo_evidencia", "evidencia_ref",
            "evidencia_localizador", "variable_reactivo_tabla", "texto_evidencia",
            "unidad_observacion", "periodo", "universo_muestra", "codificacion",
            "parte_necesidad_cubierta", "parte_necesidad_no_cubierta",
            "uso_potencial_modelo", "transformacion_requerida", "incertidumbre",
            "siguiente_accion", "objeto_modelo_origen", "objeto_modelo_origen_ref",
        ]
        fila_evidencia_semilla = {
            "procedencia_id": "PROV-SEMILLA0000000000000", "relacion_id": self.rid_semilla,
            "necesidad_id": self.necesidad_id, "fuente_canonica_normalizada": self.fuente_semilla,
            "objeto_evidencia_id_canonico": self.objeto_semilla,
            "procedencia_necesidad_id": self.necesidad_id, "procedencia_fuente": self.fuente_semilla,
            "procedencia_objeto_evidencia_id": self.objeto_semilla,
            "accion_normalizacion": "SIN_CAMBIO", "clasificacion_relacion": "CANDIDATA",
            "tipo_evidencia": "NO_DETERMINADO", "evidencia_ref": "MAIN:test/semilla.md",
            "evidencia_localizador": "NO_DETERMINADO", "variable_reactivo_tabla": "NO_DETERMINADO",
            "texto_evidencia": "NO_DETERMINADO", "unidad_observacion": "NO_DETERMINADO",
            "periodo": "NO_DETERMINADO", "universo_muestra": "NO_DETERMINADO",
            "codificacion": "NO_DETERMINADO", "parte_necesidad_cubierta": "NO_DETERMINADO",
            "parte_necesidad_no_cubierta": "NO_DETERMINADO", "uso_potencial_modelo": "NO_DETERMINADO",
            "transformacion_requerida": "NO_DETERMINADO", "incertidumbre": "NO_DETERMINADO",
            "siguiente_accion": "NO_DETERMINADO", "objeto_modelo_origen": "NO_DETERMINADO",
            "objeto_modelo_origen_ref": "NO_DETERMINADO",
        }
        _escribir_tsv(self.registro / "evidencias.tsv", self.campos_evidencias, [fila_evidencia_semilla])

        # ── utilidad-modelo.tsv (14 columnas reales) ──
        self.campos_utilidad = [
            "relacion_id", "necesidad_id", "fuente_canonica_normalizada",
            "objeto_evidencia_id_canonico", "clasificacion_relacion",
            "estado_productivo", "uso_actual", "evidencia_disponible", "reserva",
            "verificacion_requerida", "requiere_decision", "decision_id",
            "siguiente_accion", "evidencia_ref",
        ]
        fila_utilidad_semilla = {
            "relacion_id": self.rid_semilla, "necesidad_id": self.necesidad_id,
            "fuente_canonica_normalizada": self.fuente_semilla,
            "objeto_evidencia_id_canonico": self.objeto_semilla,
            "clasificacion_relacion": "CANDIDATA", "estado_productivo": "NO_DETERMINADO",
            "uso_actual": "NO_DETERMINADO", "evidencia_disponible": "NO_DETERMINADO",
            "reserva": "NO_DETERMINADO", "verificacion_requerida": "NO_DETERMINADO",
            "requiere_decision": "NO", "decision_id": "NO_APLICA",
            "siguiente_accion": "NO_DETERMINADO", "evidencia_ref": "MAIN:test/semilla.md",
        }
        _escribir_tsv(self.registro / "utilidad-modelo.tsv", self.campos_utilidad, [fila_utilidad_semilla])

        _escribir_tsv(self.registro / "artefactos-rechazados.tsv", ["artefacto_id"], [])
        _escribir_tsv(self.registro / "decisiones-humanas.tsv", ["decision_id", "estado_decision"], [])
        _escribir_tsv(self.registro / "fusiones-relaciones.tsv", ["relacion_id"], [])

        self.campos_aliases = [
            "alias_fuente", "fuente_canonica_normalizada", "base_identidad",
            "confianza", "accion_fuente", "evidencia_ref", "justificacion",
        ]
        self.fuente_nueva = "FUENTE_NUEVA"
        _escribir_tsv(self.registro / "aliases-fuentes.tsv", self.campos_aliases, [{
            "alias_fuente": "FUENTE_NUEVA_ALIAS", "fuente_canonica_normalizada": self.fuente_nueva,
            "base_identidad": "identidad de prueba", "confianza": "ALTA",
            "accion_fuente": "NORMALIZAR_FUENTE", "evidencia_ref": "MAIN:test/alias.md",
            "justificacion": "fila de alias de prueba",
        }])

        _escribir_tsv(self.registro / "necesidad-objeto-modelo.tsv",
                      ["necesidad_id", "objeto_modelo_origen", "fuentes_verificacion", "reserva"],
                      [{"necesidad_id": self.necesidad_id, "objeto_modelo_origen": "obj_origen_test",
                        "fuentes_verificacion": "forense/test.md", "reserva": "NINGUNA"}])

        self.id_manifiesto = "manifiesto_id_test"
        (self.root / "manifiesto.yaml").write_text(
            yaml.safe_dump([{"id": self.id_manifiesto, "archivo": "test.zip"}], allow_unicode=True),
            encoding="utf-8",
        )

        archivos = {}
        for archivo in ARCHIVOS_TSV.values():
            data = (self.registro / archivo).read_bytes()
            archivos[archivo] = {"sha256": hashlib.sha256(data).hexdigest(), "filas": len(leer_tsv(self.registro / archivo))}
        self.manifest = {
            "baseline_version": "1.0.0",
            "clave_relacion": ["necesidad_id", "fuente_canonica_normalizada", "objeto_evidencia_id_canonico"],
            "delimiter": "TAB", "encoding": "UTF-8",
            "invariantes": [],
            "procedencia": {"criterio": "prueba", "origen": "baseline semilla de prueba"},
            "schema_version": "1.0.0",
            "archivos": archivos,
            "conteos": {
                "relaciones_activas": 1, "procedencias_aceptadas": 1,
                "artefactos_rechazados": 0, "decisiones_pendientes": 0,
                "familias_alias": 1, "fusiones_declaradas": 0,
                "confirmadas": 0, "negativas": 0, "candidatas": 1, "no_accesibles": 0,
            },
        }
        self._guardar_manifest()
        self.assertTrue(validar_baseline(self.registro)["ok"], "el fixture debe partir válido")

        self.objeto_nuevo = objeto_evidencia_id(self.fuente_nueva, "descripcion de prueba para FUENTE_NUEVA")

    def tearDown(self):
        self.tmp.cleanup()

    def _guardar_manifest(self):
        (self.registro / BASELINE_JSON).write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")

    def _hashes(self) -> dict[str, str]:
        return {n: hashlib.sha256((self.registro / n).read_bytes()).hexdigest() for n in NOMBRES}

    def _entrada_valida(self) -> dict:
        return {
            "necesidad_id": self.necesidad_id,
            "fuente_canonica_normalizada": self.fuente_nueva,
            "descripcion_objeto": "descripcion de prueba para FUENTE_NUEVA",
            "relacion": {
                "fuente_nombre": "Fuente Nueva de Prueba", "tipo_fuente": "FUENTE_DATOS",
                "id_manifiesto": self.id_manifiesto, "sha256_fuente": "NO_DETERMINADO",
                "capa1_universo_indexado": "NO_DETERMINADO",
                "capa2_manifiesto": "NO_REFERENCIADO", "capa3_disco_real": "NO_REFERENCIADO",
                "capa4_apertura_mapeo": "", "clasificacion_relacion": "CANDIDATA",
                "reason_code": "ALTA_TEST", "evidencia_ref": "MAIN:test/alta.md",
                "evidencia_textual_breve": "texto de prueba", "confianza": "MEDIA",
                "conflicto_material": "NO", "nota": "fila de alta creada por test",
            },
            "evidencia": {
                "procedencia_necesidad_id": self.necesidad_id, "procedencia_fuente": self.fuente_nueva,
                "procedencia_objeto_evidencia_id": self.objeto_nuevo,
                "accion_normalizacion": "SIN_CAMBIO", "clasificacion_relacion": "CANDIDATA",
                "tipo_evidencia": "NO_DETERMINADO", "evidencia_ref": "MAIN:test/alta.md",
                "evidencia_localizador": "NO_DETERMINADO", "variable_reactivo_tabla": "NO_DETERMINADO",
                "texto_evidencia": "texto de prueba de evidencia", "unidad_observacion": "NO_DETERMINADO",
                "periodo": "NO_DETERMINADO", "universo_muestra": "NO_DETERMINADO",
                "codificacion": "NO_DETERMINADO", "parte_necesidad_cubierta": "NO_DETERMINADO",
                "parte_necesidad_no_cubierta": "NO_DETERMINADO", "uso_potencial_modelo": "NO_DETERMINADO",
                "transformacion_requerida": "NO_DETERMINADO", "incertidumbre": "NO_DETERMINADO",
                "siguiente_accion": "NO_DETERMINADO", "objeto_modelo_origen": "NO_DETERMINADO",
                "objeto_modelo_origen_ref": "NO_DETERMINADO",
            },
            "utilidad": {
                "estado_productivo": "PENDIENTE_EVIDENCIA", "uso_actual": "NO_DETERMINADO",
                "evidencia_disponible": "NO_DETERMINADO", "reserva": "NO_DETERMINADO",
                "verificacion_requerida": "NO_DETERMINADO", "requiere_decision": "NO",
                "decision_id": "NO_APLICA", "siguiente_accion": "NO_DETERMINADO",
                "evidencia_ref": "MAIN:test/alta.md",
            },
            "procedencia_nota": (
                "Alta de prueba via test_alta_relacion.py: agrega FUENTE_NUEVA "
                "para validar el flujo transaccional completo."
            ),
        }

    def _escribir_entrada(self, datos: dict, nombre: str) -> Path:
        path = self.root / nombre
        if nombre.endswith((".yaml", ".yml")):
            path.write_text(yaml.safe_dump(datos, allow_unicode=True, sort_keys=False), encoding="utf-8")
        else:
            path.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        return path

    # ────────────────────────────── tests ──────────────────────────────

    def test_alta_exitosa_escribe_tres_tablas_y_recifra(self):
        entrada_path = self._escribir_entrada(self._entrada_valida(), "entrada.yaml")
        resultado = run(entrada_path, self.registro, dry_run=False)

        self.assertTrue(resultado["ok"])
        self.assertTrue(resultado["applied"])
        rid_nuevo = resultado["relacion_id"]
        self.assertEqual(rid_nuevo, relacion_id(self.necesidad_id, self.fuente_nueva, self.objeto_nuevo))

        relaciones = leer_tsv(self.registro / "relaciones.tsv")
        evidencias = leer_tsv(self.registro / "evidencias.tsv")
        utilidad = leer_tsv(self.registro / "utilidad-modelo.tsv")
        self.assertEqual(len(relaciones), 2)
        self.assertEqual(len(evidencias), 2)
        self.assertEqual(len(utilidad), 2)
        self.assertIn(rid_nuevo, {f["relacion_id"] for f in relaciones})
        self.assertIn(rid_nuevo, {f["relacion_id"] for f in evidencias})
        self.assertIn(rid_nuevo, {f["relacion_id"] for f in utilidad})

        # la fila semilla sigue byte-idéntica en contenido (no reserializada)
        semilla = next(f for f in relaciones if f["relacion_id"] == self.rid_semilla)
        self.assertEqual(semilla["nota"], "fila semilla de prueba")

        validacion = validar_baseline(self.registro)
        self.assertTrue(validacion["ok"], validacion["errores"])

        journal_path = Path(resultado["journal_path"])
        self.assertTrue(journal_path.is_file())
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        self.assertEqual(journal["relacion_id"], rid_nuevo)
        self.assertIn("recomendacion", journal)
        self.assertIn("T21", journal["recomendacion"])

        # procedencia.origen conserva el texto previo y agrega el nuevo
        manifest = json.loads((self.registro / BASELINE_JSON).read_text(encoding="utf-8"))
        self.assertIn("baseline semilla de prueba", manifest["procedencia"]["origen"])
        self.assertIn("FUENTE_NUEVA", manifest["procedencia"]["origen"])

    def test_dry_run_no_escribe_nada(self):
        antes = self._hashes()
        entrada_path = self._escribir_entrada(self._entrada_valida(), "entrada.yaml")
        resultado = run(entrada_path, self.registro, dry_run=True)

        self.assertTrue(resultado["ok"])
        self.assertFalse(resultado["applied"])
        self.assertTrue(resultado["dry_run"])
        despues = self._hashes()
        self.assertEqual(antes, despues)
        # ningún archivo journal ni de más quedó en el árbol
        self.assertEqual(sorted(os.listdir(self.root)), sorted(["registro", "manifiesto.yaml", "entrada.yaml"]))

    def test_fallo_tardio_no_deja_tablas_adelantadas(self):
        antes = self._hashes()
        entrada_path = self._escribir_entrada(self._entrada_valida(), "entrada.yaml")
        listado_padre_antes = sorted(os.listdir(self.registro.parent))

        # sub-caso A: la validación de la CANDIDATA falla.
        with mock.patch(
            "tools.curador_registro.alta_relacion.validar_baseline",
            return_value={"ok": False, "errores": ["FORZADO_POR_TEST"]},
        ):
            with self.assertRaises(AltaRelacionError):
                run(entrada_path, self.registro, dry_run=False)
        self.assertEqual(antes, self._hashes())
        self.assertEqual(listado_padre_antes, sorted(os.listdir(self.registro.parent)))

        # sub-caso B: la revalidación POST-swap (dentro de _replace_with_rollback) falla.
        valido = validar_baseline(self.registro)
        self.assertTrue(valido["ok"])
        compartido = mock.Mock(side_effect=[valido, {"ok": False, "errores": ["FORZADO_POST_SWAP"]}])
        with mock.patch("tools.curador_registro.alta_relacion.validar_baseline", new=compartido), \
             mock.patch("tools.curador_registro.integrate_barrido2.validar_baseline", new=compartido):
            with self.assertRaises(Exception):
                run(entrada_path, self.registro, dry_run=False)
        self.assertEqual(antes, self._hashes())
        self.assertEqual(listado_padre_antes, sorted(os.listdir(self.registro.parent)))

    def test_relacion_duplicada_siempre_rechaza(self):
        antes = self._hashes()
        entrada = {
            "necesidad_id": self.necesidad_id,
            "fuente_canonica_normalizada": self.fuente_semilla,
            "alias_decidido": self.fuente_semilla,
            "objeto_evidencia_id_canonico": self.objeto_semilla,
            "procedencia_nota": "intento de alta duplicada",
        }
        entrada_path = self._escribir_entrada(entrada, "entrada_dup.json")
        with self.assertRaises(AltaRelacionError) as ctx:
            run(entrada_path, self.registro, dry_run=False)
        self.assertIn("duplicada", str(ctx.exception))
        self.assertEqual(antes, self._hashes())

    def test_alias_no_resuelto_hace_paro_explicito(self):
        antes = self._hashes()
        entrada = self._entrada_valida()
        entrada["fuente_canonica_normalizada"] = "FUENTE_JAMAS_VISTA"
        entrada.pop("alias_decidido", None)
        entrada_path = self._escribir_entrada(entrada, "entrada_sin_alias.json")
        with self.assertRaises(AltaRelacionError) as ctx:
            run(entrada_path, self.registro, dry_run=False)
        self.assertIn("alias_decidido", str(ctx.exception))
        self.assertEqual(antes, self._hashes())


if __name__ == "__main__":
    unittest.main()
