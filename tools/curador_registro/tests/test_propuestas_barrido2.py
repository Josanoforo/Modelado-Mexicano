"""Pruebas dirigidas de la fase `propuestas` (§17, §26).

Lo que se prueba aquí es el bicondicional de FP-24, porque es la regla que el
§17 enuncia y que tres artefactos distintos vuelven a exigir por su cuenta (el
schema congelado, el preflight del integrador y T23 regla 17). La fase no
copia lo que le pasen: lo impone.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "tools" / "curador_registro"))

import tareas_barrido2 as tb  # noqa: E402
import integrate_barrido2 as ib  # noqa: E402

TAREA = {
    "tarea_id": "TSEM-B2-a", "relacion_id": "REL-1", "reporte_id": "RPTC-B2-x",
    "reporte_record_id": "E2R-r", "reporte_record_sha256": "b" * 64,
    "e2_record_id": "E2R-r", "e2_record_sha256": "b" * 64,
    "payload_id": "p1", "representacion_id": "REP-1", "sha256": "a" * 64,
    "objeto_logico_id": "OBJ-1", "necesidad_id": "N1", "reactivo_id": "OBJ-1",
    "fuente_canonica": "FUENTE", "frontera_semantica": "diccionario completo",
    "material_tarea_id": "TASK-B2-1", "material_task_sha256": "c" * 64,
    "material_baseline_sha256": "d" * 64, "curador_id": "CUR-1", "fecha": "2026-08-18",
}

RELACION = {
    "relacion_id": "REL-1", "necesidad_id": "N1",
    "fuente_canonica_normalizada": "FUENTE",
    "objeto_evidencia_id_canonico": "OE-1", "fuente_nombre": "n",
    "tipo_fuente": "FUENTE_DATOS", "id_manifiesto": "p1", "sha256_fuente": "a" * 64,
    "capa1_universo_indexado": "SI", "capa2_manifiesto": "SI",
    "capa3_disco_real": "EXISTE;COINCIDE;INTEGRO",
    "capa4_apertura_mapeo": "INDEXADO-NO-DESCARGADO",
    "clasificacion_relacion": "CANDIDATA", "reason_code": "x", "evidencia_ref": "y",
    "evidencia_textual_breve": "z", "confianza": "ALTA", "conflicto_material": "NO",
    "nota": "",
}


class PropuestasTests(unittest.TestCase):
    def _corre(self, veredicto):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            reg = raiz / "reg"
            reg.mkdir()
            tb.write_tsv(reg / "relaciones.tsv", list(RELACION), [RELACION])
            tareas = raiz / "tareas.tsv"
            tb.write_tsv(tareas, tb.TASK_FIELDS, [TAREA])
            ver = raiz / "veredictos.tsv"
            tb.write_tsv(ver, tb.VEREDICTO_FIELDS, [veredicto])
            return tb.derivar_propuestas(reg, tareas, ver, "2026-08-18")

    def test_cabecera_es_la_del_integrador(self) -> None:
        self.assertEqual(tb.PROPOSAL_FIELDS_17, ib.PROPOSAL_FIELDS)
        self.assertEqual(len(tb.PROPOSAL_FIELDS_17), 22)

    def test_dependencia_no_fuerza_no_aplica_aunque_le_pasen_otra_cosa(self) -> None:
        # El relevo de este acto pedía decision_mesa_id="FP-24/ADR-93"; ese
        # valor no existe en el enum. La fase lo impone, no lo copia.
        props, _ = self._corre({
            "relacion_id": "REL-1", "veredicto_a4": "EXISTE-SATISFACE",
            "confianza": "ALTA", "estado_supervision": "VALIDADA",
            "supervisor_id": "SUP-1", "dependencia_fp24": "NO",
            "razon_gate": "adjudicada con la politica de pares sellada en ADR-93",
        })
        self.assertEqual(len(props), 1)
        self.assertEqual(props[0]["decision_mesa_id"], "NO-APLICA")
        self.assertEqual(props[0]["requiere_decision_mesa"], "NO")
        self.assertIn("ADR-93", props[0]["razon_gate"])

    def test_dependencia_si_arrastra_los_tres_campos_y_el_estado(self) -> None:
        props, resumen = self._corre({
            "relacion_id": "REL-1", "veredicto_a4": "EXISTE-SATISFACE",
            "confianza": "MEDIA", "estado_supervision": "VALIDADA",
            "supervisor_id": "SUP-1", "dependencia_fp24": "SI",
            "razon_gate": "aceptarla exige decidir la regla de pares pendiente",
        })
        self.assertEqual(props[0]["requiere_decision_mesa"], "SI")
        self.assertEqual(props[0]["decision_mesa_id"], "FP-24")
        self.assertEqual(props[0]["estado_supervision"], "REQUIERE_DECISION_FP24")
        self.assertEqual(resumen["dependencia_fp24_SI"], 1)

    def test_dependencia_no_declarada_se_rechaza(self) -> None:
        props, resumen = self._corre({
            "relacion_id": "REL-1", "veredicto_a4": "EXISTE-SATISFACE",
            "confianza": "ALTA", "estado_supervision": "VALIDADA",
            "supervisor_id": "SUP-1", "dependencia_fp24": "",
            "razon_gate": "x",
        })
        self.assertEqual(props, [])
        self.assertEqual(resumen["rechazos"][0]["motivo"], "DEPENDENCIA_FP24_NO_DECLARADA")

    def test_evidencia_ref_es_la_cadena_que_exige_el_preflight(self) -> None:
        props, _ = self._corre({
            "relacion_id": "REL-1", "veredicto_a4": "EXISTE-SATISFACE",
            "confianza": "ALTA", "estado_supervision": "VALIDADA",
            "supervisor_id": "SUP-1", "dependencia_fp24": "NO", "razon_gate": "x",
        })
        self.assertEqual(props[0]["evidencia_ref"],
                         f"{TAREA['e2_record_id']}:{TAREA['e2_record_sha256']}")

    def test_accion_se_deriva_del_veredicto_contra_la_capa4_vigente(self) -> None:
        # capa4 vigente es INDEXADO-NO-DESCARGADO: un positivo la mueve.
        props, _ = self._corre({
            "relacion_id": "REL-1", "veredicto_a4": "EXISTE-SATISFACE",
            "confianza": "ALTA", "estado_supervision": "VALIDADA",
            "supervisor_id": "SUP-1", "dependencia_fp24": "NO", "razon_gate": "x",
        })
        self.assertEqual(props[0]["accion_propuesta"], "CAMBIO")
        props, _ = self._corre({
            "relacion_id": "REL-1",
            "veredicto_a4": "NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO",
            "confianza": "ALTA", "estado_supervision": "VALIDADA",
            "supervisor_id": "SUP-1", "dependencia_fp24": "NO", "razon_gate": "x",
        })
        self.assertEqual(props[0]["accion_propuesta"], "TERMINAL")

    def test_sin_veredicto_no_hay_propuesta(self) -> None:
        props, resumen = self._corre({
            "relacion_id": "REL-OTRA", "veredicto_a4": "EXISTE-SATISFACE",
            "confianza": "ALTA", "estado_supervision": "VALIDADA",
            "supervisor_id": "SUP-1", "dependencia_fp24": "NO", "razon_gate": "x",
        })
        self.assertEqual(props, [])
        self.assertEqual(resumen["rechazos"][0]["motivo"], "SIN_VEREDICTO_SUPERVISADO")


if __name__ == "__main__":
    unittest.main()
