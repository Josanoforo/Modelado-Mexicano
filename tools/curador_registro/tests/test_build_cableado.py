"""Pruebas dirigidas del ensamblador de cableado (§21, §26).

La primera es la que importa y la razón por la que existe este archivo: el
escritor (`build_cableado.CABLEADO_CABECERA`) y el validador
(`check.CABLEADO_CABECERA`) mantienen copias SEPARADAS de las 26 columnas. Eso
es deliberado -- compartir la constante haría que un error de cabecera se
validara a sí mismo, que es exactamente el defecto de escritor-y-validador que
el eje durable de este barrido ya pagó una vez (ADR-103). El precio de
separarlas es que pueden divergir en silencio, y esta prueba es quien cobra ese
precio.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "tools" / "curador_registro"))

import build_cableado  # noqa: E402


def _carga_check():
    ruta = RAIZ / "tests" / "check.py"
    spec = importlib.util.spec_from_file_location("check_para_cableado", ruta)
    modulo = importlib.util.module_from_spec(spec)
    # check.py corre su suite al importarse sólo bajo __main__; importarlo como
    # módulo es barato y no toca el repo.
    os.environ.setdefault("CHECK_SELFCHECK_CHILD", "1")
    spec.loader.exec_module(modulo)
    return modulo


BASE_TAREA = {
    "tarea_id": "TSEM-B2-a", "relacion_id": "REL-1", "reporte_id": "RPTC-B2-x",
    "reporte_record_id": "E2R-r", "reporte_record_sha256": "b" * 64,
    "e2_record_id": "E2R-r", "e2_record_sha256": "b" * 64,
    "payload_id": "p1", "representacion_id": "REP-1", "sha256": "a" * 64,
    "objeto_logico_id": "OBJ-1", "necesidad_id": "N1", "reactivo_id": "OBJ-1",
    "fuente_canonica": "FUENTE", "frontera_semantica": "todo el diccionario",
    "material_tarea_id": "TASK-B2-1", "material_task_sha256": "c" * 64,
    "material_baseline_sha256": "d" * 64, "curador_id": "CUR-1", "fecha": "2026-08-18",
}

BASE_PROPUESTA = {
    "propuesta_id": "PROP-1", "tarea_id": "TSEM-B2-a", "reporte_id": "RPTC-B2-x",
    "payload_id": "p1", "representacion_id": "REP-1", "sha256": "a" * 64,
    "objeto_logico_id": "OBJ-1", "necesidad_id": "N1", "reactivo_id": "OBJ-1",
    "accion_propuesta": "CAMBIO", "relacion_id_actual": "REL-1",
    "veredicto_a4": "EXISTE-SATISFACE", "evidencia_ref": "E2R-r:" + "b" * 64,
    "frontera_semantica": "todo el diccionario", "confianza": "ALTA",
    "requiere_decision_mesa": "NO", "decision_mesa_id": "NO-APLICA",
    "dependencia_fp24": "NO", "razon_gate": "decidible por evidencia",
    "estado_supervision": "VALIDADA", "supervisor_id": "SUP-1", "fecha": "2026-08-18",
}

BASE_DECISION = dict(BASE_PROPUESTA, estado_integracion="INTEGRADA",
                     razon_integracion="capa 4 proyectada", journal_id="JRN-1")

BASE_REPORTE = {
    "reporte_id": "RPTC-B2-x", "record_id": "E2R-r", "record_sha256": "b" * 64,
    "payload_id": "p1", "representacion_id": "REP-1", "sha256": "a" * 64,
    "objeto_logico_id": "OBJ-1", "grado_inspeccion": "E2",
    "afirmacion_tipo": "RESUMEN-NEUTRAL-COMPACTO", "objeto_tipo": "COLUMNA",
    "localizador": "loc", "descripcion_neutral": "COLUMNA; objetos=3",
    "frontera_inspeccion": "contenedor completo", "estado": "E2-COMPLETO",
    "privacidad": "DEPURADO", "fecha": "2026-08-18",
}


class CabeceraTests(unittest.TestCase):
    def test_escritor_y_validador_declaran_la_misma_cabecera(self) -> None:
        check = _carga_check()
        self.assertEqual(
            build_cableado.CABLEADO_CABECERA, check.CABLEADO_CABECERA,
            "el ensamblador y T23 tienen copias separadas de las 26 columnas a "
            "propósito; si divergen, el producto se valida contra un contrato "
            "que no es el que se escribió",
        )

    def test_son_las_26_del_encargo(self) -> None:
        self.assertEqual(len(build_cableado.CABLEADO_CABECERA), 26)


class EnsambladoTests(unittest.TestCase):
    def _ensambla(self, **cambios):
        propuesta = dict(BASE_PROPUESTA, **cambios.get("propuesta", {}))
        decision = dict(BASE_DECISION, **cambios.get("decision", {}))
        return build_cableado.ensambla(
            [propuesta], [dict(BASE_TAREA)], [decision], [dict(BASE_REPORTE)],
            "SEMRUN-t", "2026-08-18",
        )

    def test_fila_completa_no_tiene_celda_vacia(self) -> None:
        filas, rechazos = self._ensambla()
        self.assertEqual(rechazos, [])
        self.assertEqual(len(filas), 1)
        vacias = [c for c in build_cableado.CABLEADO_CABECERA if filas[0][c] == ""]
        self.assertEqual(vacias, [], f"celdas vacías: {vacias}")
        self.assertEqual(build_cableado.valida(filas), [])
        self.assertEqual(filas[0]["sha256_12"], "a" * 12)
        self.assertEqual(filas[0]["reporte_neutral_ref"], "RPTC-B2-x:" + "b" * 64)

    def test_propuesta_sin_decision_no_produce_fila(self) -> None:
        filas, rechazos = build_cableado.ensambla(
            [dict(BASE_PROPUESTA)], [dict(BASE_TAREA)], [], [dict(BASE_REPORTE)],
            "SEMRUN-t", "2026-08-18")
        self.assertEqual(filas, [])
        self.assertEqual(rechazos[0]["motivo"], "PROPUESTA_SIN_DECISION_DE_INTEGRACION")

    def test_propuesta_sin_tarea_no_produce_fila(self) -> None:
        filas, rechazos = build_cableado.ensambla(
            [dict(BASE_PROPUESTA)], [], [dict(BASE_DECISION)], [dict(BASE_REPORTE)],
            "SEMRUN-t", "2026-08-18")
        self.assertEqual(filas, [])
        self.assertEqual(rechazos[0]["motivo"], "PROPUESTA_SIN_TAREA")

    def test_fp24_si_integrada_es_error_de_validacion(self) -> None:
        filas, _ = self._ensambla(
            propuesta={"dependencia_fp24": "SI", "requiere_decision_mesa": "SI",
                       "decision_mesa_id": "FP-24",
                       "estado_supervision": "REQUIERE_DECISION_FP24"},
            decision={"estado_integracion": "INTEGRADA"})
        errores = build_cableado.valida(filas)
        self.assertTrue(any("no puede quedar INTEGRADA" in e for e in errores), errores)

    def test_fp24_no_con_decision_mesa_poblada_es_inconsistente(self) -> None:
        # Es el error que el relevo de este acto pedía cometer:
        # decision_mesa_id="FP-24/ADR-93" con dependencia_fp24=NO.
        filas, _ = self._ensambla(propuesta={"decision_mesa_id": "FP-24"})
        errores = build_cableado.valida(filas)
        self.assertTrue(any("dependencia_fp24=NO inconsistente" in e for e in errores), errores)

    def test_orden_es_determinista(self) -> None:
        tarea_b = dict(BASE_TAREA, tarea_id="TSEM-B2-b", payload_id="p0",
                       representacion_id="REP-0")
        prop_b = dict(BASE_PROPUESTA, propuesta_id="PROP-0", tarea_id="TSEM-B2-b",
                      payload_id="p0", representacion_id="REP-0")
        dec_b = dict(BASE_DECISION, propuesta_id="PROP-0")
        filas, _ = build_cableado.ensambla(
            [dict(BASE_PROPUESTA), prop_b], [dict(BASE_TAREA), tarea_b],
            [dict(BASE_DECISION), dec_b], [dict(BASE_REPORTE)], "SEMRUN-t", "2026-08-18")
        self.assertEqual([f["payload_id"] for f in filas], ["p0", "p1"])

    def test_texto_largo_se_recorta_a_160(self) -> None:
        filas, _ = self._ensambla(propuesta={"razon_gate": "x" * 400})
        self.assertLessEqual(len(filas[0]["razon_gate"]), 160)
        self.assertEqual(build_cableado.valida(filas), [])


if __name__ == "__main__":
    unittest.main()
