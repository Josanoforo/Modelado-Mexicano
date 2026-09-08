#!/usr/bin/env python3
"""Regresiones del riesgo observado: B sin corte y P1 con la misma ola de R.

Datos ficticios, independientes de los valores del modelo y de GEN1.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import asdict, replace
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from tools.baseline_temporal import Objetivo, Observacion, Serie, seleccionar_baseline


class BaselineTemporalTest(unittest.TestCase):
    def setUp(self):
        self.serie = Serie("ENCUESTA-FICTICIA", "P1", "adultos", "si=1;no=0", "total", "proporcion")
        self.objetivo = Objetivo(self.serie, date(2021, 1, 1), date(2021, 12, 31), date(2020, 12, 31))

    def obs(self, anio, p, **cambios):
        base = Observacion(self.serie, date(anio, 1, 1), date(anio, 12, 31),
                           date(anio + 1, 6, 1), True, p,
                           f"RESULT-FICTICIO-{anio}", f"fixture {anio}")
        return replace(base, **cambios)

    def test_excluye_objetivo_y_futuro_y_elige_ultima_previa(self):
        historial = [self.obs(2025, .9), self.obs(2017, .1), self.obs(2021, .7), self.obs(2019, .2)]
        a = seleccionar_baseline(self.objetivo, historial)
        b = seleccionar_baseline(self.objetivo, historial[::-1])
        self.assertEqual(a["p"], .2)
        self.assertEqual(a["resultado_id"], b["resultado_id"])
        self.assertEqual({x["motivo"] for x in a["excluidas"]}, {"OLA_NO_ANTERIOR"})

    def test_ola_antigua_revisada_despues_del_corte_no_entra(self):
        revisada = self.obs(2019, .8, disponible_desde=date(2022, 1, 1))
        r = seleccionar_baseline(self.objetivo, [self.obs(2017, .1), revisada])
        self.assertEqual(r["p"], .1)
        self.assertEqual(r["excluidas"][0]["motivo"], "NO_DISPONIBLE_AL_CORTE")

    def test_no_confunde_mismo_nombre_con_misma_poblacion_o_escala(self):
        for campo in ("encuesta", "reactivo", "universo", "codificacion", "segmento"):
            with self.subTest(campo=campo):
                ajena = self.obs(2019, .7, serie=replace(self.serie, **{campo: "OTRO"}))
                r = seleccionar_baseline(self.objetivo, [self.obs(2017, .1), ajena])
                self.assertEqual(r["p"], .1)
        with self.assertRaises(ValueError):
            replace(self.serie, unidad="porcentaje")

    def test_disponibilidad_desconocida_y_no_estimable_no_inventan_cero(self):
        for historial in ([], [self.obs(2019, .2, disponible_desde=None)], [self.obs(2019, None)]):
            with self.subTest(historial=historial):
                r = seleccionar_baseline(self.objetivo, historial)
                self.assertEqual(r["estado"], "SIN_BASELINE")
                self.assertIsNone(r["p"])
        self.assertEqual(seleccionar_baseline(self.objetivo, [self.obs(2019, 0)])["p"], 0)

    def test_conserva_precedencia_publica_y_persistencia_explicita(self):
        privada = self.obs(2019, .3, publicada=False)
        r = seleccionar_baseline(self.objetivo, [self.obs(2017, .1), privada])
        self.assertEqual((r["metodo"], r["p"]), ("ultima_ola_publica", .1))
        r = seleccionar_baseline(self.objetivo, [privada])
        self.assertEqual((r["metodo"], r["p"]), ("persistencia", .3))

    def test_ambiguedad_no_se_resuelve_por_orden_ni_por_media(self):
        with self.assertRaisesRegex(ValueError, "ambiguo"):
            seleccionar_baseline(self.objetivo, [self.obs(2019, .1), self.obs(2019, .5)])

    def test_rechaza_valores_fechas_e_identidades_invalidas(self):
        for p in (float("nan"), float("inf"), -.1, 12, True, "0.2"):
            with self.subTest(p=p), self.assertRaises(ValueError):
                self.obs(2019, p)
        with self.assertRaises(ValueError):
            replace(self.objetivo, fecha_corte=date(2022, 1, 1))
        with self.assertRaises(ValueError):
            self.obs(2019, .2, disponible_desde=date(2018, 1, 1))
        with self.assertRaises(ValueError):
            replace(self.serie, universo="PENDIENTE")
        with self.assertRaises(ValueError):
            self.obs(2019, .2, resultado_id=123)

    def test_intervalos_superpuestos_no_son_ola_previa(self):
        solapada = self.obs(2019, .7, periodo_fin=date(2021, 6, 1), disponible_desde=date(2022, 1, 1))
        r = seleccionar_baseline(self.objetivo, [solapada])
        self.assertEqual(r["estado"], "SIN_BASELINE")
        self.assertEqual(r["excluidas"][0]["motivo"], "OLA_NO_ANTERIOR")

    def test_cli_corre_sobre_fixture_y_rechaza_entrada_invalida(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "fixture.json"
            doc = {"objetivo": asdict(self.objetivo), "historial": [asdict(self.obs(2019, .2))]}
            ruta.write_text(json.dumps(doc, default=str), encoding="utf-8")
            cmd = [sys.executable, str(RAIZ / "tools/baseline_temporal.py"), str(ruta)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(json.loads(r.stdout)["p"], .2)
            doc["historial"][0]["p"] = 20
            ruta.write_text(json.dumps(doc, default=str), encoding="utf-8")
            r = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)
            self.assertEqual(r.stdout, "")


if __name__ == "__main__":
    unittest.main()
