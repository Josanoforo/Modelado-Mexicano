#!/usr/bin/env python3
"""Pruebas del acto GEN2-ENCIG-SERIE-Y-TENDENCIA-1 (21/sep/2026).

D-22: el punto de entrada de cada medidor corre sobre datos SINTÉTICOS
antes de abrir microdato, y `_valida_outputs` de `corrida0` acepta la salida
de cada rama terminal (celda con soporte, celda rara sin soporte, ola 2015
sin `ID_PER`, serie con punto nulo, los cuatro dictámenes). Cero microdato
real salvo `test_oro_2023`, que solo compara dos `resultados.json` ya
sellados y se salta si el CALC 2023 todavía no existe.

Defectos reales que atrapa: `preflight` VERDE no prueba el conducto (FP del
piloto 3, PR #944 → #951); un id que el código emite nulo sin
`permite_no_estimable` revienta `run` después de abrir el dato.
"""
from __future__ import annotations

import importlib.util
import io
import json
import math
import os
import sys
import tempfile
import unittest
import zipfile

import numpy as np
import pandas as pd
import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))


def _carga(nombre, rel):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SERIE = _carga("encig_serie_canal", "tools/encig_serie_canal.py")
OM = _carga("encig_origen_movil", "tools/encig_origen_movil.py")
C0 = _carga("corrida0", "tools/corrida0.py")


def _zip_sintetico(ruta, ola, n_upm=12, llave_2015=False, sin_soporte_edad60=False, seed=7):
    """ENCIG de juguete: residentes + sec_7 con la llave real de la ola."""
    rng = np.random.default_rng(seed)
    people, events = [], []
    for u in range(n_upm):
        est = f"{(u % 3) + 1:04d}"; upm = f"{u + 1:05d}"
        for r in range(1, 4):
            edad = int(rng.choice([22, 35, 50, 70]))
            if sin_soporte_edad60 and edad == 70:
                edad = 50
            base = {"ENT": "01", "UPM": upm, "V_SEL": "01", "N_HOG": "1",
                    "SEXO": str(rng.integers(1, 3)), "EDAD": str(edad), "NIV": str(rng.integers(0, 10))}
            if llave_2015:
                base["N_REN"] = f"{r:02d}"
            else:
                base["ID_PER"] = f"01.{upm}.01.{r:02d}"
            people.append(base)
            for tra in ("01", "02", "01"):        # dos pagos de luz, uno de agua
                ev = {"N_TRA": tra if not llave_2015 else tra.lstrip("0"),
                      "P7_3": str(rng.choice([1, 2, 4, 5, 6, 9])),
                      "FAC_TRA": str(int(rng.integers(50, 500))),
                      "EST_DIS": est, "UPM_DIS": upm}
                if llave_2015:
                    ev.update({"ENT": "01", "UPM": upm, "V_SEL": "01", "N_HOG": "1", "R_ELE": f"{r:02d}"})
                else:
                    ev["ID_PER"] = base["ID_PER"]
                events.append(ev)
    with zipfile.ZipFile(ruta, "w") as zf:
        pfx = "conjunto_de_datos_" if ola in ("2019", "2021") else ""
        zf.writestr(f"x/conjunto_de_datos/{pfx}encig{ola}_04_sec_7.csv", pd.DataFrame(events).to_csv(index=False))
        zf.writestr(f"x/diccionario_de_datos/{pfx}encig{ola}_04_sec_7.csv", "NOMBRE_CAMPO,NEMONICO\n")
        zf.writestr(f"x/conjunto_de_datos/{pfx}encig{ola}_02_residentes_sec_2.csv", pd.DataFrame(people).to_csv(index=False))


def _spec(ola):
    with open(os.path.join(RAIZ, "data", "corrida0", f"CALC-ENCIG-SERIE-CANAL-{ola}", "spec.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def _contrato(ola, reps=200):
    s = _spec(ola)
    return {"parametros": {**s["parametros"], "bootstrap_replicas": reps}, "seed": s["seed"]}


class MedidorSerieTest(unittest.TestCase):
    def _corre(self, ola, **kw):
        with tempfile.TemporaryDirectory() as d:
            z = os.path.join(d, "x.zip")
            _zip_sintetico(z, ola, llave_2015=(ola == "2015"), **kw)
            pid = _spec(ola)["parametros"]["payload_id"]
            return SERIE.medir({pid: {"ruta_absoluta": z}}, _contrato(ola))

    def test_spec_yaml_declara_exactamente_lo_que_emite(self):
        for ola in ("2015", "2017", "2019", "2021", "2023"):
            ids_spec = {r["id"] for r in _spec(ola)["resultados"]}
            ids_code = {r["id"] for r in SERIE.ids_resultado(ola)}
            self.assertEqual(ids_spec, ids_code, ola)

    def test_rama_normal_con_id_per_pasa_valida_outputs(self):
        for ola in ("2017", "2019", "2021", "2023"):
            out = self._corre(ola)
            self.assertEqual(C0._valida_outputs(_spec(ola), out), [], ola)
            p = out[f"RESULT-ENCIG-SERIE-{ola}-DIGITAL-ALL-ALL-P"]
            self.assertTrue(0.0 < p < 1.0)
            self.assertEqual(out[f"RESULT-ENCIG-SERIE-{ola}-JOIN-SIN-DEMOGRAFIA"], 0)
            self.assertGreater(out[f"RESULT-ENCIG-SERIE-{ola}-P7-3-EXCLUIDAS"], 0)

    def test_rama_2015_sin_id_per_usa_la_llave_de_vivienda(self):
        out = self._corre("2015")
        self.assertEqual(C0._valida_outputs(_spec("2015"), out), [])
        self.assertEqual(out["RESULT-ENCIG-SERIE-2015-LLAVE-JOIN"],
                         "ENT+UPM+V_SEL+N_HOG+R_ELE->ENT+UPM+V_SEL+N_HOG+N_REN")
        self.assertEqual(out["RESULT-ENCIG-SERIE-2015-JOIN-SIN-DEMOGRAFIA"], 0)
        # N_TRA «1» sin cero a la izquierda cuenta como pago de luz.
        self.assertGreater(out["RESULT-ENCIG-SERIE-2015-DIGITAL-N-UNIVERSO"], 0)

    def test_celda_rara_sin_soporte_sale_nula_y_declarada(self):
        out = self._corre("2021", sin_soporte_edad60=True)
        self.assertEqual(C0._valida_outputs(_spec("2021"), out), [])
        self.assertIsNone(out["RESULT-ENCIG-SERIE-2021-DIGITAL-EDAD-60-MAS-P"])
        self.assertEqual(out["RESULT-ENCIG-SERIE-2021-DIGITAL-EDAD-60-MAS-N"], 0)
        self.assertEqual(out["RESULT-ENCIG-SERIE-2021-DIGITAL-EDAD-60-MAS-B-VALIDAS"], 0)

    def test_la_celda_nacional_no_exige_demografia(self):
        with tempfile.TemporaryDirectory() as d:
            z = os.path.join(d, "x.zip")
            _zip_sintetico(z, "2021")
            # Quita a una persona de residentes: sus trámites quedan sin ejes pero cuentan en ALL.
            with zipfile.ZipFile(z) as zf:
                names = zf.namelist(); data = {n: zf.read(n) for n in names}
            res = [n for n in names if "residentes" in n][0]
            df = pd.read_csv(io.BytesIO(data[res]), dtype=str); df = df.iloc[1:]
            data[res] = df.to_csv(index=False).encode()
            with zipfile.ZipFile(z, "w") as zf:
                for n, b in data.items(): zf.writestr(n, b)
            out = SERIE.medir({"encig2021_csv": {"ruta_absoluta": z}}, _contrato("2021"))
        self.assertEqual(C0._valida_outputs(_spec("2021"), out), [])
        # Dos pagos de luz de esa persona; los que caen en el universo (P7_3 válida) quedan sin ejes.
        self.assertIn(out["RESULT-ENCIG-SERIE-2021-JOIN-SIN-DEMOGRAFIA"], (1, 2))
        self.assertEqual(out["RESULT-ENCIG-SERIE-2021-DIGITAL-ALL-ALL-N"],
                         out["RESULT-ENCIG-SERIE-2021-DIGITAL-N-UNIVERSO"])

    def test_llave_de_residentes_duplicada_para(self):
        with tempfile.TemporaryDirectory() as d:
            z = os.path.join(d, "x.zip")
            _zip_sintetico(z, "2017")
            with zipfile.ZipFile(z) as zf:
                names = zf.namelist(); data = {n: zf.read(n) for n in names}
            res = [n for n in names if "residentes" in n][0]
            df = pd.read_csv(io.BytesIO(data[res]), dtype=str)
            data[res] = pd.concat([df, df.iloc[:1]]).to_csv(index=False).encode()
            with zipfile.ZipFile(z, "w") as zf:
                for n, b in data.items(): zf.writestr(n, b)
            with self.assertRaises(RuntimeError):
                SERIE.medir({"encig2017_csv": {"ruta_absoluta": z}}, _contrato("2017"))

    def test_oro_2023(self):
        mio = os.path.join(RAIZ, "data", "corrida0", "CALC-ENCIG-SERIE-CANAL-2023", "resultados.json")
        piso = os.path.join(RAIZ, "data", "corrida0", "CALC-PISOS-ENCIG2023-EJES-0002", "resultados.json")
        if not os.path.exists(mio):
            self.skipTest("SALTADO: CALC-ENCIG-SERIE-CANAL-2023 no sellado todavía (0 archivos comparados)")
        with open(mio, encoding="utf-8") as f: a = json.load(f)
        with open(piso, encoding="utf-8") as f: b = json.load(f)
        a = a.get("resultados", a); b = b.get("resultados", b)
        n = 0
        for k, v in b.items():
            if "-DIGITAL-" not in k: continue
            mine = k.replace("RESULT-PISOS-ENCIG2023-V2-DIGITAL-", "RESULT-ENCIG-SERIE-2023-DIGITAL-")
            self.assertIn(mine, a)
            if isinstance(v, float):
                self.assertAlmostEqual(a[mine], v, delta=1e-10, msg=k)
            else:
                self.assertEqual(a[mine], v, k)
            n += 1
        self.assertEqual(n, 60)


class OrigenMovilTest(unittest.TestCase):
    PARAMS = {"olas_serie": ["2015", "2017", "2019", "2021", "2023"],
              "olas_comunes": ["2021", "2023", "2025"], "delta_mae_material_pp": 3.0,
              "olas_comparables": 6, "cambio_instrumento_en_ola": "NINGUNA"}

    @staticmethod
    def _serie(l0=-0.5, slope=0.4, ancho=0.1):
        s = {}
        for c in OM.CELDAS:
            s[c] = [(float(y), OM._expit(l0 + slope * i), OM._expit(l0 + slope * i - ancho),
                     OM._expit(l0 + slope * i + ancho)) for i, y in enumerate((2015, 2017, 2019, 2021, 2023, 2025))]
        return s

    def _spec_om(self):
        return {"resultados": OM.ids_resultado(self.PARAMS["olas_serie"])}

    def test_pesos_reproducen_los_cuatro_pisos(self):
        anios = [2015.0, 2017.0, 2019.0, 2021.0]
        self.assertEqual(OM.pesos("PERSISTENCIA", anios, 2023.0), [0, 0, 0, 1])
        self.assertEqual([round(w, 9) for w in OM.pesos("TENDENCIA-2", anios, 2023.0)], [0, 0, -1, 2])
        w3 = OM.pesos("TENDENCIA-3", anios, 2023.0)
        self.assertAlmostEqual(sum(w3), 1.0)
        self.assertAlmostEqual(sum(w * a for w, a in zip(w3, anios)), 2023.0)   # reproduce la recta
        ws = OM.pesos("TENDENCIA-SERIE", anios, 2023.0)
        self.assertAlmostEqual(sum(ws), 1.0)
        self.assertAlmostEqual(sum(w * a for w, a in zip(ws, anios)), 2023.0)
        self.assertIsNone(OM.pesos("TENDENCIA-3", anios[:2], 2019.0))

    def test_serie_logit_lineal_da_tendencia_y_persistencia_yerra(self):
        out = OM.origen_movil(self._serie(), self.PARAMS)
        self.assertEqual(C0._valida_outputs(self._spec_om(), out), [])
        self.assertLess(out["RESULT-ENCIG-OM-TENDENCIA-2-MAE-COMUN-PP"], 1e-9)
        self.assertGreater(out["RESULT-ENCIG-OM-PERSISTENCIA-MAE-COMUN-PP"], 3.0)
        self.assertEqual(out["RESULT-ENCIG-OM-NACIONAL-SUBE-SOSTENIDA"], "SI")
        self.assertEqual(out["RESULT-ENCIG-OM-DICTAMEN"], "TENDENCIA")
        self.assertEqual(out["RESULT-ENCIG-OM-PERSISTENCIA-N-COMUN"], 33)
        self.assertEqual(out["RESULT-ENCIG-OM-TENDENCIA-3-N-PREDICCIONES"], 33)
        self.assertEqual(out["RESULT-ENCIG-OM-PERSISTENCIA-N-PREDICCIONES"], 55)

    def test_serie_plana_da_salto_sin_explicar(self):
        out = OM.origen_movil(self._serie(slope=0.0), self.PARAMS)
        self.assertEqual(C0._valida_outputs(self._spec_om(), out), [])
        self.assertEqual(out["RESULT-ENCIG-OM-DICTAMEN"], "SALTO-SIN-EXPLICAR")
        self.assertEqual(out["RESULT-ENCIG-OM-PERSISTENCIA-COBERTURA-COMUN"], 1.0)

    def test_punto_nulo_no_predice_ni_es_predicho(self):
        s = self._serie(); s[("SEXO", "2")][2] = (2019.0, None, None, None)
        out = OM.origen_movil(s, self.PARAMS)
        self.assertEqual(C0._valida_outputs(self._spec_om(), out), [])
        self.assertEqual(out["RESULT-ENCIG-OM-2019-SEXO-2-PERSISTENCIA-CUBRE"], "NO-DEFINIDO")
        self.assertIsNone(out["RESULT-ENCIG-OM-2019-SEXO-2-TENDENCIA-2-P"])
        # 2021 se predice desde 2017 (persistencia salta el hueco).
        self.assertAlmostEqual(out["RESULT-ENCIG-OM-2021-SEXO-2-PERSISTENCIA-P"], s[("SEXO", "2")][1][1])

    def test_dictamen_no_decidible_y_cambio_de_instrumento(self):
        out = OM.origen_movil(self._serie(), {**self.PARAMS, "olas_comparables": 2})
        self.assertEqual(out["RESULT-ENCIG-OM-DICTAMEN"], "NO-DECIDIBLE")
        out = OM.origen_movil(self._serie(), {**self.PARAMS, "cambio_instrumento_en_ola": "2021"})
        self.assertEqual(out["RESULT-ENCIG-OM-DICTAMEN"], "CAMBIO-DE-INSTRUMENTO")

    def test_lectura_de_2025_desde_el_yaml_sellado(self):
        ruta = os.path.join(RAIZ, "milpa", "tramite-ola5-propuesta-v0.yaml")
        with open(ruta, "rb") as f: b = f.read()
        inputs = {"TRAMITE-OLA5-PROPUESTA": {"bytes": b}}
        r = {}
        for ola in self.PARAMS["olas_serie"]:
            fake = {}
            for eje, cat in OM.CELDAS:
                base = f"RESULT-ENCIG-SERIE-{ola}-DIGITAL-{eje}-{cat}"
                fake[base + "-P"] = 0.5; fake[base + "-IC-LO"] = 0.45; fake[base + "-IC-HI"] = 0.55
            inputs[f"CALC-ENCIG-SERIE-CANAL-{ola}"] = {"bytes": json.dumps({"resultados": fake}).encode()}
        serie = OM._serie_desde_inputs(inputs, {"parametros": self.PARAMS})
        self.assertEqual(serie[("ALL", "ALL")][-1], (2025.0, 0.673393, 0.663165, 0.683910))
        self.assertEqual(serie[("EDAD", "60-MAS")][-1][1], 0.475822)
        self.assertEqual(serie[("ESCOLARIDAD", "HASTA-PRIMARIA")][-1][1], 0.391961)
        self.assertEqual(len(serie[("SEXO", "1")]), 6)


if __name__ == "__main__":
    unittest.main()
