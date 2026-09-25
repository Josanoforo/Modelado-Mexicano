"""GEN2-CLASE-AMAI-2 · guardia de apertura acotada de ENIGH 2024 (firma C7).

Todo sobre un zip SINTÉTICO con la estructura de miembros de ENIGH 2024 y
columnas señuelo (ingreso, remesas, sexo) que la guardia no debe leer.
Prueba por mutación: cualquier lectura de otra columna o agrupación por otra
variable hace fallar la guardia; la auditoría estática detecta el fuente mutado.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.dominios.amai import auditoria_enigh2024 as A  # noqa: E402
from tools.dominios.amai import enigh2024 as E  # noqa: E402

FUENTE = (ROOT / "tools/dominios/amai/enigh2024.py").read_text(encoding="utf-8")


def zip_sintetico(ruta: Path, n: int = 3000, semilla: int = 7) -> Path:
    rng = np.random.default_rng(semilla)
    viv = ["folioviv,cuart_dorm,bano_comp,mat_pisos"]
    hog = ["folioviv,foliohog,conex_inte,num_auto,num_van,num_pick,num_moto"]
    con = ["folioviv,foliohog,educa_jefe,ocupados,factor,est_dis,upm,ing_cor,remesas,sexo_jefe"]
    for i in range(n):
        fv = f"{i:010d}"
        viv.append(f"{fv},{rng.integers(0, 6)},{rng.integers(0, 4)},2")
        hog.append(f"{fv},1,{rng.integers(1, 3)},{rng.integers(0, 3)},{rng.integers(0, 2)},"
                   f"{rng.integers(0, 2)},1")
        con.append(f"{fv},1,{rng.integers(1, 12):02d},{rng.integers(0, 6)},"
                   f"{rng.integers(50, 400)},{i % 6:03d},{i // 4:07d},1234.5,0,1")
    with zipfile.ZipFile(ruta, "w") as z:
        for t, filas in (("viviendas", viv), ("hogares", hog), ("concentradohogar", con)):
            base = f"conjunto_de_datos_{t}_enigh2024_ns"
            z.writestr(f"{base}/conjunto_de_datos/{base}.csv",
                       ("﻿" + "\n".join(filas) + "\n").encode("utf-8"))
            z.writestr(f"{base}/diccionario_de_datos/diccionario_datos_{t}_enigh2024_ns.csv",
                       "x\n1\n")
    return ruta


def contrato():
    return {"parametros": {"input_id": "P", "calc_id": "CALC-SINTETICO", "columnas_leidas": E.lista_blanca(),
                           "umbral_desvio_pp": 5.0, "n_min": 200}, "seed": {"valor": 20260925}}


class TestGuardia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.zip = zip_sintetico(Path(cls.tmp.name) / "x.zip")
        cls.raiz, E.RAIZ = E.RAIZ, Path(cls.tmp.name)
        cls.out = E.medir({"P": {"ruta_absoluta": str(cls.zip)}}, contrato())

    @classmethod
    def tearDownClass(cls):
        E.RAIZ = cls.raiz
        cls.tmp.cleanup()

    def test_auditoria_verde_sobre_el_fuente(self):
        self.assertEqual(A.audita(FUENTE), [])

    def test_lee_exactamente_la_lista_blanca(self):
        self.assertEqual(self.out["RESULT-AMAI-NSE-ENIGH-2024-COLUMNAS-LEIDAS"].split(","),
                         E.lista_blanca())
        ref = self.out["RESULT-AMAI-NSE-ENIGH-2024-JSON"]
        self.assertTrue(ref.startswith("REF:data/corrida0/CALC-SINTETICO/tablas/"))
        tabla = (Path(self.tmp.name) / ref[4:].split("#")[0]).read_text(encoding="utf-8")
        self.assertNotIn("ing_cor", tabla)

    def test_distribucion_suma_uno(self):
        s = sum(self.out[f"RESULT-AMAI-NSE-ENIGH-2024-DIST-{g}-P"] for g in ("BAJO", "MEDIO", "ALTO"))
        self.assertAlmostEqual(s, 1.0, places=12)

    def test_supresion_n_min(self):
        c = contrato()
        c["parametros"]["n_min"] = 10**6
        out = E.medir({"P": {"ruta_absoluta": str(self.zip)}}, c)
        self.assertIsNone(out["RESULT-AMAI-NSE-ENIGH-2024-DIST-BAJO-P"])

    def test_mutacion_columna_extra_en_lector(self):
        with self.assertRaises(E.GuardiaColumnas):
            E.lee_acotado(self.zip, "concentrado", ("folioviv", "ing_cor"))

    def test_mutacion_tabla_no_autorizada(self):
        with self.assertRaises(E.GuardiaColumnas):
            E.lee_acotado(self.zip, "poblacion", ("folioviv",))

    def test_mutacion_lista_blanca_ampliada_para_en_medir(self):
        spec = importlib.util.spec_from_loader("mut", loader=None)
        mut = importlib.util.module_from_spec(spec)
        mut.__file__ = str(ROOT / "tools/dominios/amai/enigh2024.py")
        exec(compile(FUENTE.replace('"est_dis", "upm"),', '"est_dis", "upm", "ing_cor"),'),
                     "mut", "exec"), mut.__dict__)
        self.assertIn("concentrado.ing_cor", mut.lista_blanca())
        mut.RAIZ = Path(self.tmp.name)
        with self.assertRaises(mut.GuardiaColumnas):
            mut.medir({"P": {"ruta_absoluta": str(self.zip)}}, contrato())

    def test_mutacion_agrupacion_por_otra_variable(self):
        with self.assertRaises(E.GuardiaAgrupacion):
            E.agrega(E.componentes(self.zip), "EST_DIS")

    def test_mutacion_salida_con_corte_extra(self):
        with self.assertRaises(E.GuardiaAgrupacion):
            E.guardia_salida({**self.out, "RESULT-AMAI-NSE-ENIGH-2024-DIST-BAJO-URBANO-P": 0.1})

    def test_auditoria_roja_ante_fuentes_mutados(self):
        mutaciones = {
            "A1": FUENTE.replace("from tools.dominios.amai import regla as R",
                                 "from tools.dominios.amai import regla as R\n"
                                 "from tools.dominios.amai import componentes as C"),
            "A2": FUENTE.replace("dist = M.distribucion(comp)",
                                 "dist = M.distribucion(comp); M.nse_hogares"),
            "A3": FUENTE.replace("    comp = componentes(ruta)\n",
                                 "    comp = componentes(ruta)\n    pd.read_csv(ruta)\n"),
            "A4": FUENTE.replace('lee_acotado(ruta, "viviendas", COLUMNAS["viviendas"])',
                                 'lee_acotado(ruta, "viviendas", ("folioviv", "mat_pisos"))'),
            "A5": FUENTE.replace('"educa_jefe": _num(d["educa_jefe"]),',
                                 '"educa_jefe": _num(d["educa_jefe"]), "x": d["ing_cor"],'),
            "A6": FUENTE.replace("    dist = M.distribucion(comp)\n",
                                 "    dist = M.distribucion(comp)\n"
                                 "    comp.groupby('EST_DIS')\n"),
        }
        for regla, fuente in mutaciones.items():
            self.assertNotEqual(fuente, FUENTE, regla)
            fallas = A.audita(fuente)
            self.assertTrue(any(f.startswith(regla) for f in fallas), (regla, fallas))



class TestCopiaDelCalc(unittest.TestCase):
    def test_medidor_del_calc_es_copia_byte_a_byte(self):
        calc = ROOT / "data/corrida0/CALC-AMAI-NSE-ENIGH-2024-0001/medidor.py"
        self.assertEqual(calc.read_bytes(), (ROOT / "tools/dominios/amai/enigh2024.py").read_bytes())


if __name__ == "__main__":
    unittest.main()
