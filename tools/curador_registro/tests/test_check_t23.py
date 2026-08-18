"""Pruebas negativas obligatorias de T23 (`tests/check.py`), encargo madre §22
y `forense/notas/2026-08-17-b2-derivaciones-c4.md` §4 verbatim:

    - una relación del conjunto histórico de 20, decidible por evidencia
      específica y dependencia_fp24=NO, puede integrarse ordinariamente;
    - cualquier propuesta, histórica o nueva, con dependencia_fp24=SI no
      puede quedar INTEGRADA mientras FP-24 esté ABIERTA.

Sintéticas a propósito, mismo criterio que `test_barrido2_recupera.py`: T23
no conoce los 20 IDs históricos (§22), así que "decidible por evidencia
específica" se demuestra con una relación cualquiera, no con una de las 20
reales -- conocerlas por ID sería precisamente lo que el test debe NO hacer.

`tests/check.py` no es un paquete (vive fuera de `tools/`, sin
`__init__.py`), así que se importa por ruta y se monkeypatchea `check.ROOT`
para apuntar a un árbol sintético -- exactamente lo que activa T23 (necesita
`data/cableado-universo-v1_0.tsv` bajo ese ROOT) sin tocar el repo real.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
_SPEC = importlib.util.spec_from_file_location("check_t23_bajo_prueba", ROOT / "tests" / "check.py")
check = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = check
_SPEC.loader.exec_module(check)


def _write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(fields)]
    for row in rows:
        lines.append("\t".join(str(row.get(f, "")) for f in fields))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _fila_valida(*, relacion_id: str, propuesta_id: str, dependency: str) -> dict[str, str]:
    """Fila de cableado sintéticamente válida contra las 19 condiciones,
    salvo por lo que cada prueba module a propósito."""
    blocked = dependency == "SI"
    return {
        "payload_id": "payload_test_" + relacion_id[-6:],
        "representacion_id": "REP-" + ("2" * 64),
        "sha256_12": "3" * 12,
        "sha256": "3" * 64,
        "fuente_canonica": "FUENTE-PRUEBA",
        "objeto_logico_id": "OBJ-B2-" + ("4" * 64),
        "necesidad_id": "N1",
        "reactivo_id": "REACTIVO-PRUEBA",
        "texto_reactivo_recortado": "texto de reactivo recortado de prueba",
        "grado_inspeccion": "E2",
        "afirmacion_tipo": "MEDICION",
        "veredicto_a4": "EXISTE-SATISFACE",
        "evidencia": "evidencia sintética específica del objeto, no de lista histórica",
        "frontera_inspeccion": "frontera sintética completa",
        "reporte_neutral_ref": "E2R-" + relacion_id[-6:] + ":" + ("5" * 64),
        "propuesta_id": propuesta_id,
        "relacion_id": relacion_id,
        "semrun_id": "SEMRUN-PRUEBA",
        "requiere_decision_mesa": "SI" if blocked else "NO",
        "decision_mesa_id": "FP-24" if blocked else "NO-APLICA",
        "dependencia_fp24": dependency,
        "razon_gate": "evidencia objeto-específica; no depende de lista histórica ni de par",
        "estado_integracion": "REQUIERE_DECISION_FP24" if blocked else "INTEGRADA",
        "cegamiento_roto": "NO",
        "fecha": "2026-08-18",
        "razon": "fila sintética de prueba T23",
    }


class T23NegativeTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self._orig_root = check.ROOT
        check.ROOT = str(self.root)
        self.addCleanup(setattr, check, "ROOT", self._orig_root)

    def _run_t23(self, rows: list[dict[str, str]], *, extra_joins: bool = True) -> tuple[list, list]:
        relacion_id = rows[0]["relacion_id"]
        propuesta_id = rows[0]["propuesta_id"]
        _write_tsv(self.root / "data" / "cableado-universo-v1_0.tsv", check.CABLEADO_CABECERA, rows)
        _write_tsv(
            self.root / "data" / "curacion-registro" / "relaciones.tsv",
            ["relacion_id", "capa4_apertura_mapeo", "capa3_disco_real"],
            [{"relacion_id": relacion_id, "capa4_apertura_mapeo": "NO-APLICA", "capa3_disco_real": "NO_REFERENCIADO"}],
        )
        b2 = self.root / "data" / "curacion-registro" / "ejecucion-semantica" / "barrido2"
        if extra_joins:
            _write_tsv(b2 / "propuestas-barrido2.tsv", ["propuesta_id", "tarea_id"],
                       [{"propuesta_id": propuesta_id, "tarea_id": "TSEM-B2-prueba"}])
            _write_tsv(b2 / "tareas-semanticas-barrido2.tsv", ["tarea_id", "payload_id"],
                       [{"tarea_id": "TSEM-B2-prueba", "payload_id": rows[0]["payload_id"]}])
            _write_tsv(b2 / "decisiones-integracion-barrido2.tsv", ["propuesta_id", "estado_integracion"],
                       [{"propuesta_id": propuesta_id, "estado_integracion": rows[0]["estado_integracion"]}])
        check.FAILS[:] = []
        check.WARNS[:] = []
        check.t23_cableado()
        return list(check.FAILS), list(check.WARNS)

    def test_specific_evidence_no_fp24_integrates_ordinarily(self) -> None:
        """Una relación decidible por evidencia específica, dependencia_fp24=NO,
        INTEGRADA -- T23 no la marca FAIL. No usa ninguno de los 20 IDs
        históricos (T23 no los conoce, §22)."""
        fila = _fila_valida(
            relacion_id="REL-historica-sintetica-01", propuesta_id="PROP-B2-" + "a" * 24, dependency="NO",
        )
        fails, _warns = self._run_t23([fila])
        self.assertEqual([], fails, f"fila ordinaria válida no debería fallar T23: {fails}")

    def test_any_fp24_dependency_cannot_stay_integrated_while_open(self) -> None:
        """Cualquier propuesta -- histórica o nueva -- con dependencia_fp24=SI
        no puede quedar INTEGRADA mientras FP-24 esté abierta. T23 no
        adjudica FP-24 caso por caso: la regla es incondicional (fail-closed,
        igual que el schema congelado)."""
        fila = _fila_valida(
            relacion_id="REL-fp24-sintetica-02", propuesta_id="PROP-B2-" + "b" * 24, dependency="SI",
        )
        # estado_integracion se fuerza a INTEGRADA a propósito: es exactamente
        # la combinación (dependencia_fp24=SI + INTEGRADA) que la condición 18
        # de T23 debe atrapar, tanto para una fila histórica como nueva.
        fila["estado_integracion"] = "INTEGRADA"
        fails, _warns = self._run_t23([fila])
        self.assertTrue(
            any("no puede quedar INTEGRADA mientras FP-24 esté abierta" in msg for _test, msg in fails),
            f"T23 debió fallar por dependencia_fp24=SI + INTEGRADA, dio: {fails}",
        )


if __name__ == "__main__":
    unittest.main()
