#!/usr/bin/env python3
"""Test de `tools/enut_persistencia_serie.py` (P4 de GEN2-ENUT-PISOS-Y-SERIE-1).

D-22: primero sintético — un diccionario de resultados inventado con respuesta
conocida ejercita cada rama del dictamen §5.3 (PERSISTE, TENDENCIA,
NO-DECIDIBLE por n < 4, NO-DECIDIBLE por cobertura, razón por cobertura mutua
y por tendencia) y el Clopper-Pearson se coteja contra valores cerrados
(k=0 y k=n) y contra la identidad binomial; después la tabla real derivada se
recomputa desde los resultados.json sellados y debe coincidir byte a byte
con la publicada (la tabla es derivación, no fuente). Sin numpy; sin módulo csv.
"""
from __future__ import annotations

import io
import math
import os
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))
import enut_persistencia_serie as E  # noqa: E402


def _res(ola: str, variante: str, valores: dict[tuple[str, str], tuple[float, float, float]],
         razon: tuple[float, float, float]) -> dict:
    """valores: (eje, cat) → (p, lo, hi) para las 14 celdas; razón nacional."""
    r = {}
    for (eje, cat), (p, lo, hi) in valores.items():
        b = f"RESULT-ENUT{ola}-{variante}-{eje}-{cat}"
        r.update({b + "-P": p, b + "-IC-LO": lo, b + "-IC-HI": hi, b + "-N": 100})
    b = f"RESULT-ENUT{ola}-RAZON-{variante}-NACIONAL"
    r.update({b + "-P": razon[0], b + "-IC-LO": razon[1], b + "-IC-HI": razon[2], b + "-N": 50})
    return r


def _celdas(nivel: float, ancho: float = 1.0, faltan: int = 0) -> dict:
    todas = [(e, c) for e, cs in E.EJES.items() for c in cs]
    out = {}
    for i, (e, c) in enumerate(todas):
        if i < len(todas) - faltan:
            out[(e, c)] = (nivel + i * 0.1, nivel + i * 0.1 - ancho, nivel + i * 0.1 + ancho)
    return out


def _mundo(nucleo_2014, nucleo_2019, nucleo_2024, razones, faltan_2024=0):
    r = {o: {} for o in ("2009", "2014", "2019", "2024")}
    r["2014"].update(_res("2014", "NUCLEO", _celdas(nucleo_2014), razones["2014"]))
    r["2019"].update(_res("2019", "NUCLEO", _celdas(nucleo_2019), razones["2019"]))
    r["2024"].update(_res("2024", "NUCLEO", _celdas(nucleo_2024, faltan=faltan_2024), razones["2024"]))
    r["2024"].update(_res("2024", "CONCP", _celdas(nucleo_2024 + 2), razones["2024"]))
    # MIN: serie plana en las cuatro olas (PERSISTE en todo)
    for o in ("2009", "2014", "2019", "2024"):
        r[o].update(_res(o, "MIN", _celdas(5.0), (0.2, 0.19, 0.21)))
    return r


def _dict(r):
    filas, dic = E.deriva(r)
    return {(d["variante"], d["escala"], d["objetivo"]): d for d in dic}, filas


class TestSintetico(unittest.TestCase):
    def test_clopper_pearson(self):
        self.assertEqual(E.clopper_pearson(0, 14)[0], 0.0)
        self.assertEqual(E.clopper_pearson(14, 14)[1], 1.0)
        lo, hi = E.clopper_pearson(7, 14)
        self.assertAlmostEqual(lo, 0.230361, places=5)
        self.assertAlmostEqual(hi, 0.769639, places=5)
        # k = 12 de 14 es el mínimo con CP95_lo ≥ 0.5 (regla §5.3): PERSISTE exige ≥ 12/14
        self.assertLess(E.clopper_pearson(11, 14)[0], 0.5)
        self.assertGreaterEqual(E.clopper_pearson(12, 14)[0], 0.5)
        self.assertTrue(all(math.isnan(x) for x in E.clopper_pearson(0, 0)))

    def test_persiste(self):
        d, _ = _dict(_mundo(10.0, 10.0, 10.0, {"2014": (0.2, 0.19, 0.21), "2019": (0.2, 0.19, 0.21), "2024": (0.2, 0.19, 0.21)}))
        self.assertEqual(d[("NUCLEO", "media", "2024")]["dictamen"], "PERSISTE")
        self.assertEqual(d[("NUCLEO", "media", "2024")]["cobertura_v1_k"], 14)
        self.assertEqual(d[("NUCLEO", "razon", "2024")]["dictamen"], "PERSISTE")
        self.assertEqual(d[("MIN", "media", "2024")]["dictamen"], "PERSISTE")
        self.assertEqual(d[("MIN", "razon", "2019")]["dictamen"], "PERSISTE")

    def test_tendencia_media(self):
        # 10 → 15 → 20 con IC ±1: V1 no cubre, V2 acierta exacto
        d, _ = _dict(_mundo(10.0, 15.0, 20.0, {"2014": (0.2, 0.19, 0.21), "2019": (0.2, 0.19, 0.21), "2024": (0.2, 0.19, 0.21)}))
        x = d[("NUCLEO", "media", "2024")]
        self.assertEqual(x["cobertura_v1_k"], 0)
        self.assertAlmostEqual(x["mae_v2"], 0.0)
        self.assertEqual(x["dictamen"], "TENDENCIA")
        self.assertIsNone(x["mae_v3"])   # NUCLEO sólo tiene dos olas previas

    def test_no_decidible_por_salto(self):
        # 10 → 10 → 20: ni persistencia ni tendencia
        d, _ = _dict(_mundo(10.0, 10.0, 20.0, {"2014": (0.2, 0.19, 0.21), "2019": (0.2, 0.19, 0.21), "2024": (0.2, 0.19, 0.21)}))
        self.assertEqual(d[("NUCLEO", "media", "2024")]["dictamen"], "NO-DECIDIBLE")

    def test_no_decidible_por_n(self):
        d, _ = _dict(_mundo(10.0, 10.0, 10.0, {"2014": (0.2, 0.19, 0.21), "2019": (0.2, 0.19, 0.21), "2024": (0.2, 0.19, 0.21)}, faltan_2024=11))
        x = d[("NUCLEO", "media", "2024")]
        self.assertEqual(x["n_celdas"], 3)
        self.assertEqual(x["dictamen"], "NO-DECIDIBLE")
        self.assertIn("n < 4", x["regla_aplicada"])

    def test_razon_tendencia_y_no_decidible(self):
        d, _ = _dict(_mundo(10.0, 10.0, 10.0, {"2014": (0.20, 0.19, 0.21), "2019": (0.25, 0.24, 0.26), "2024": (0.30, 0.29, 0.31)}))
        self.assertEqual(d[("NUCLEO", "razon", "2024")]["dictamen"], "TENDENCIA")
        d, _ = _dict(_mundo(10.0, 10.0, 10.0, {"2014": (0.20, 0.19, 0.21), "2019": (0.25, 0.24, 0.26), "2024": (0.20, 0.19, 0.21)}))
        self.assertEqual(d[("NUCLEO", "razon", "2024")]["dictamen"], "NO-DECIDIBLE")

    def test_delta_instrumento_y_c1(self):
        d, filas = _dict(_mundo(10.0, 10.0, 10.0, {"2014": (0.2, 0.19, 0.21), "2019": (0.2, 0.19, 0.21), "2024": (0.2, 0.19, 0.21)}))
        deltas = [f for f in filas if f["metodo"] == "DELTA-INSTRUMENTO" and f["escala"] == "media"]
        self.assertEqual(len(deltas), 14)
        self.assertTrue(all(abs(f["error"] - 2.0) < 1e-9 for f in deltas))
        c1 = [x for x in E.deriva(_mundo(10.0, 10.0, 10.0, {"2014": (0.2, 0.19, 0.21), "2019": (0.2, 0.19, 0.21), "2024": (0.2, 0.19, 0.21)}))[1] if x["conducta"].startswith("C1")]
        self.assertEqual(c1[0]["dictamen"], "CAMBIO-DE-INSTRUMENTO")


class TestTablaReal(unittest.TestCase):
    def test_tabla_publicada_es_la_derivada(self):
        if not E.SALIDA_SERIE.exists():
            self.skipTest("tabla aún no publicada")
        r = E._carga()
        filas, dic = E.deriva(r)
        import tempfile
        with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as t:
            a, b = Path(t) / "s.tsv", Path(t) / "d.tsv"
            E.escribe(filas, a, E.COLS_SERIE)
            E.escribe(dic, b, E.COLS_DICT)
            self.assertEqual(a.read_bytes(), E.SALIDA_SERIE.read_bytes())
            self.assertEqual(b.read_bytes(), E.SALIDA_DICTAMEN.read_bytes())
        vocab = {"PERSISTE", "TENDENCIA", "CAMBIO-DE-INSTRUMENTO", "NO-DECIDIBLE"}
        self.assertTrue(all(d["dictamen"] in vocab for d in dic))

    def test_main_sin_flag_no_escribe(self):
        if not E.SALIDA_SERIE.exists():
            self.skipTest("tabla aún no publicada")
        antes = E.SALIDA_SERIE.stat().st_mtime_ns
        with redirect_stdout(io.StringIO()):
            E.main([])
        self.assertEqual(E.SALIDA_SERIE.stat().st_mtime_ns, antes)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]] + sys.argv[1:], verbosity=2)
