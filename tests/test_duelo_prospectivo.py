#!/usr/bin/env python3
"""Pruebas del duelo prospectivo ENVIPE 2026 — ACTO GEN2-DUELO-ENVIPE2026-COMMIT-1.

Tres bloques, todos sobre datos SINTÉTICOS (E.5: cero microdato aquí):
  1. `tools/duelo/cruces_familia.py` — la familia C2/P/S1/Sλ/AP y la regla
     v0.3, contra fórmulas cerradas y contra `piso_log_aditivo` (contrato
     pinado del piloto 2, importado y no reimplementado).
  2. `tools/duelo/tendencia_nacional.py` — K/T3/T5/TC, E+, origen móvil.
  3. `tools/duelo/envipe_duelo.py` — punta a punta sobre zips FABRICADOS
     (`tests/test_marginales_una_variable.py::fabrica_zip`): emisiones con
     la ola nueva reservada, adjudicación abriéndola, celda rara (n = 0),
     cero no finitos, y `corrida0._valida_outputs` vacío contra la spec de
     cada CALC del duelo (D-22 ampliada, requisito 2 y 3).

Defecto real que atrapa (regla de señal §1): el piloto 3 perdió tres actos
por conducto — join por índice, `medir()` vacío, `null` sin
`permite_no_estimable` — con pytest en verde. Aquí cada rama terminal del
procedimiento pasa por `_valida_outputs` antes de congelar.
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tests"))


def _importa(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


cf = _importa("cruces_familia", RAIZ / "tools" / "duelo" / "cruces_familia.py")
tn = _importa("tendencia_nacional", RAIZ / "tools" / "duelo" / "tendencia_nacional.py")
ed = _importa("envipe_duelo", RAIZ / "tools" / "duelo" / "envipe_duelo.py")
c2mod = _importa("test_celda_d_c2", RAIZ / "tests" / "test_celda_d_c2.py")
fab = _importa("test_marginales_una_variable",
               RAIZ / "tests" / "test_marginales_una_variable.py")
corrida0 = _importa("corrida0_duelo", RAIZ / "tools" / "corrida0.py")

CALCS_DUELO = {
    "CALC-DUELO-ENVIPE2026-EMISIONES-0001": "emisiones",
    "CALC-DUELO-ENVIPE2026-ADJUDICACION-0001": "adjudicacion",
    "CALC-DUELO-ENSAYO-ENVIPE2025-EMISIONES-0001": "emisiones",
    "CALC-DUELO-ENSAYO-ENVIPE2025-ADJUDICACION-0001": "adjudicacion",
    "CALC-DUELO-ORIGEN-MOVIL-0001": "origen_movil",
}


def _logit(p):
    return math.log(p / (1 - p))


def _expit(z):
    return 1 / (1 + math.exp(-z))


def _celda(p, n_rep=200, ruido=1e-3, seed=0, n=500):
    rng = np.random.default_rng(seed)
    reps = np.clip(p + rng.normal(0, ruido, n_rep), 1e-6, 1 - 1e-6)
    return cf.Celda(p=p, ic95=(p - 0.02, p + 0.02), replicas=reps, n=n)


def _marginales(pa, pb, pn, **kw):
    return cf.Marginales(a={f"a{i}": _celda(p, seed=10 + i, **kw) for i, p in enumerate(pa)},
                         b={f"b{j}": _celda(p, seed=20 + j, **kw) for j, p in enumerate(pb)},
                         nac=_celda(pn, seed=30, **kw),
                         orden_a=tuple(f"a{i}" for i in range(len(pa))),
                         orden_b=tuple(f"b{j}" for j in range(len(pb))))


def _cruce_log_aditivo(m: cf.Marginales, delta=None, **kw):
    """Cruce = C2 exacto (+ delta en logit por celda si se pide)."""
    out = {}
    for ka in m.orden_a:
        for kb in m.orden_b:
            z = _logit(m.a[ka].p) + _logit(m.b[kb].p) - _logit(m.nac.p)
            if delta:
                z += delta[(ka, kb)]
            out[(ka, kb)] = _celda(_expit(z), seed=hash((ka, kb)) % 1000, **kw)
    return out


# ══ 1 · familia de cruces ═════════════════════════════════════════════════

class Familia(unittest.TestCase):
    def setUp(self):
        self.m_t = _marginales([0.3, 0.5, 0.7], [0.4, 0.6], 0.55)
        self.m_p = _marginales([0.28, 0.48, 0.66], [0.38, 0.58], 0.52)

    def test_c2_es_piso_log_aditivo_del_piloto_2(self):
        c2 = cf.c2(self.m_t)
        for (ka, kb), cel in c2.items():
            esperado = c2mod.piso_log_aditivo(
                {"desenlace_id": "x", "p": self.m_t.a[ka].p},
                {"desenlace_id": "x", "p": self.m_t.b[kb].p},
                {"desenlace_id": "x", "p": self.m_t.nac.p})["p"]
            self.assertAlmostEqual(cel.p, esperado, places=12)
            self.assertTrue(np.all(np.isfinite(cel.replicas)))

    def test_sin_interaccion_S1_igual_a_C2(self):
        ant = cf.OlaAnterior("p", _cruce_log_aditivo(self.m_p), self.m_p)
        fam = cf.familia(self.m_t, [ant])
        for c in fam["meta"]["celdas"]:
            self.assertAlmostEqual(fam["meta"]["interaccion_media"][c][0], 0.0, places=12)
            self.assertAlmostEqual(fam["candidatos"]["S1"][c].p,
                                   fam["candidatos"]["C2"][c].p, places=12)

    def test_lambda_cero_hace_SL_igual_a_C2_y_lambda_uno_a_S1(self):
        # Ī idéntico en todas las celdas (Var_entre = 0) → τ² = 0 → λ = 0
        delta = {(ka, kb): 0.3 for ka in self.m_p.orden_a for kb in self.m_p.orden_b}
        ant = cf.OlaAnterior("p", _cruce_log_aditivo(self.m_p, delta), self.m_p)
        fam = cf.familia(self.m_t, [ant])
        self.assertAlmostEqual(fam["meta"]["lambda"]["lambda"], 0.0, places=12)
        for c in fam["meta"]["celdas"]:
            self.assertAlmostEqual(fam["candidatos"]["SL"][c].p,
                                   fam["candidatos"]["C2"][c].p, places=12)
        # Ī muy distinto entre celdas y réplicas casi sin ruido → λ → 1
        delta = {(ka, kb): (-1) ** (i + j) * 0.8 for i, ka in enumerate(self.m_p.orden_a)
                 for j, kb in enumerate(self.m_p.orden_b)}
        m_p = _marginales([0.28, 0.48, 0.66], [0.38, 0.58], 0.52, ruido=1e-9)
        ant = cf.OlaAnterior("p", _cruce_log_aditivo(m_p, delta, ruido=1e-9), m_p)
        fam = cf.familia(self.m_t, [ant])
        self.assertGreater(fam["meta"]["lambda"]["lambda"], 0.999)
        for c in fam["meta"]["celdas"]:
            self.assertAlmostEqual(fam["candidatos"]["SL"][c].p,
                                   fam["candidatos"]["S1"][c].p, places=6)

    def test_persistencia_y_ajuste_proporcional_formulas(self):
        x = _cruce_log_aditivo(self.m_p)
        ant = cf.OlaAnterior("p", x, self.m_p)
        fam = cf.familia(self.m_t, [ant])
        for c in fam["meta"]["celdas"]:
            self.assertEqual(fam["candidatos"]["P"][c].p, x[c].p)
            esperado = _expit(_logit(x[c].p) + _logit(0.55) - _logit(0.52))
            self.assertAlmostEqual(fam["candidatos"]["AP"][c].p, esperado, places=12)

    def test_dos_olas_anteriores_promedian_la_interaccion(self):
        d1 = {c: 0.2 for c in [(a, b) for a in self.m_p.orden_a for b in self.m_p.orden_b]}
        d2 = {c: 0.6 for c in d1}
        a1 = cf.OlaAnterior("p1", _cruce_log_aditivo(self.m_p, d1), self.m_p)
        a2 = cf.OlaAnterior("p2", _cruce_log_aditivo(self.m_p, d2), self.m_p)
        fam = cf.familia(self.m_t, [a1, a2])
        self.assertEqual(fam["meta"]["ola_persistencia"], "p2")
        for c in fam["meta"]["celdas"]:
            self.assertAlmostEqual(fam["meta"]["interaccion_media"][c][0], 0.4, places=10)

    def test_marginal_degenerado_da_none_sin_recorte(self):
        m = _marginales([0.0, 0.5], [0.4], 0.5)
        c2 = cf.c2(m)
        self.assertIsNone(c2[("a0", "b0")].p)
        self.assertIsNotNone(c2[("a1", "b0")].p)
        ant = cf.OlaAnterior("p", _cruce_log_aditivo(self.m_p), self.m_p)
        fam = cf.familia(self.m_t, [ant])
        for cid, celdas in fam["candidatos"].items():
            for cel in celdas.values():
                self.assertFalse(np.isnan(cel.p), cid)  # ningún NaN escapa como punto

    def test_orden_distinto_levanta(self):
        m_p = _marginales([0.28, 0.48], [0.38, 0.58], 0.52)
        ant = cf.OlaAnterior("p", _cruce_log_aditivo(m_p), m_p)
        with self.assertRaises(cf.FamiliaError):
            cf.familia(self.m_t, [ant])


class Adjudicacion(unittest.TestCase):
    def _escena(self, err_c2_pp, err_sl_pp, ruido=1e-4):
        m_t = _marginales([0.3, 0.5, 0.7], [0.4, 0.6], 0.55, ruido=ruido)
        c2 = cf.c2(m_t)
        R, cand_sl = {}, {}
        for c, cel in c2.items():
            r = cel.p + err_c2_pp / 100.0
            R[c] = cf.Celda(p=r, ic95=(r - 0.01, r + 0.01),
                            replicas=np.full(len(cel.replicas), r), n=500)
            s = r - err_sl_pp / 100.0
            cand_sl[c] = cf.Celda(p=s, replicas=np.full(len(cel.replicas), s), n=500)
        punt = {c: True for c in R}
        return R, {"C2": c2, "SL": cand_sl}, punt

    def test_vence_retador_cuando_despeja_medio_punto(self):
        R, cand, punt = self._escena(err_c2_pp=2.0, err_sl_pp=0.0)
        adj = cf.adjudica(R, cand, punt)
        sl = adj["candidatos"]["SL"]
        self.assertAlmostEqual(sl["delta_mae_pp"], 2.0, places=6)
        self.assertEqual(sl["veredicto"], "VENCE-RETADOR")
        self.assertEqual(sl["rol"], "PRIMARIA")
        self.assertEqual(adj["candidatos"]["C2"]["veredicto"], "PISO")

    def test_propuesta_con_reserva_entre_cero_y_medio(self):
        R, cand, punt = self._escena(err_c2_pp=0.3, err_sl_pp=0.0)
        adj = cf.adjudica(R, cand, punt)
        self.assertEqual(adj["candidatos"]["SL"]["veredicto"], "PROPUESTA-CON-RESERVA")

    def test_nadie_vence_y_piso_se_sostiene(self):
        R, cand, punt = self._escena(err_c2_pp=0.0, err_sl_pp=1.5)
        adj = cf.adjudica(R, cand, punt)
        sl = adj["candidatos"]["SL"]
        self.assertEqual(sl["veredicto"], "NADIE-VENCE")
        self.assertTrue(sl["piso_se_sostiene"])
        self.assertLess(sl["delta_mae_pp"], 0)

    def test_sin_puntuadas_es_no_adjudicable(self):
        R, cand, punt = self._escena(err_c2_pp=2.0, err_sl_pp=0.0)
        punt = {c: False for c in punt}
        adj = cf.adjudica(R, cand, punt)
        self.assertEqual(adj["celdas_puntuadas"], 0)
        self.assertEqual(adj["candidatos"]["SL"]["veredicto"], "NO-ADJUDICABLE")

    def test_puntuadas_exige_n_en_todas_las_olas(self):
        p = cf.puntuadas({"2024": {"x": 250, "y": 150}, "2025": {"x": 300, "y": 400}}, 200)
        self.assertEqual(p, {"x": True, "y": False})
        p = cf.puntuadas({"2024": {"x": None}, "2025": {"x": 300}}, 200)
        self.assertEqual(p, {"x": False})


# ══ 2 · tendencia nacional ════════════════════════════════════════════════

def _serie_lineal_logit(olas, z0, pendiente, ee=0.005):
    out = []
    for o in olas:
        p = _expit(z0 + pendiente * (o - olas[0]))
        out.append(tn.Punto(ola=o, p=p, lo=p - 1.96 * ee, hi=p + 1.96 * ee))
    return out


class Tendencia(unittest.TestCase):
    def test_tendencia_exacta_en_logit(self):
        s = _serie_lineal_logit(list(range(2012, 2026)), -1.0, 0.05)
        objetivo = _expit(-1.0 + 0.05 * (2026 - 2012))
        for cid in ("T3", "T5", "TC"):
            pr = tn.predice(s, 2026, cid)
            self.assertEqual(pr.estado, "CONSTRUIBLE")
            self.assertAlmostEqual(pr.p, objetivo, places=12)
            self.assertAlmostEqual(pr.pendiente_logit, 0.05, places=10)
            self.assertLess(pr.ic95[0], pr.p)
            self.assertGreater(pr.ic95[1], pr.p)
        self.assertEqual(tn.predice(s, 2026, "T3").olas_usadas, (2023, 2024, 2025))
        self.assertEqual(len(tn.predice(s, 2026, "TC").olas_usadas), 14)

    def test_k_y_no_construibles(self):
        s = _serie_lineal_logit([2023, 2024, 2025], -0.2, 0.1)
        k = tn.predice(s, 2026, "K")
        self.assertEqual(k.p, s[-1].p)
        self.assertEqual(k.ic95, (s[-1].lo, s[-1].hi))
        self.assertEqual(tn.predice(s, 2026, "T3").estado, "CONSTRUIBLE")
        self.assertTrue(tn.predice(s, 2026, "T5").estado.startswith("NO-CONSTRUIBLE"))
        self.assertIsNone(tn.predice(s, 2026, "T5").p)
        self.assertTrue(tn.predice(s, 2026, "TC").estado.startswith("NO-CONSTRUIBLE"))

    def test_no_comparable_queda_fuera_del_ajuste_y_de_los_objetivos(self):
        s = _serie_lineal_logit(list(range(2011, 2026)), -1.0, 0.05)
        s[0] = tn.Punto(2011, 0.9, 0.85, 0.95, comparable=False)   # ola rara
        pr = tn.predice(s, 2026, "TC")
        self.assertNotIn(2011, pr.olas_usadas)
        om = tn.origen_movil(s)
        self.assertNotIn(2011, om["por_ola"])
        self.assertEqual(om["olas_no_comparables"], [2011])

    def test_e_mas_formula_y_replicas(self):
        self.assertAlmostEqual(tn.e_mas(0.4, 0.5, 0.55),
                               _expit(_logit(0.4) + _logit(0.55) - _logit(0.5)), places=12)
        rng = np.random.Generator(np.random.PCG64(1))
        reps = tn.e_mas_replicas(np.full(50, 0.4), np.full(50, 0.5), 0.55, None, rng)
        self.assertTrue(np.allclose(reps, tn.e_mas(0.4, 0.5, 0.55)))
        reps = tn.e_mas_replicas(np.array([0.4, 0.0, np.nan]), np.full(3, 0.5), 0.55, 0.01, rng)
        self.assertTrue(np.isfinite(reps[0]) and np.isnan(reps[1]) and np.isnan(reps[2]))

    def test_origen_movil_sin_seleccion(self):
        s = _serie_lineal_logit(list(range(2012, 2026)), -1.0, 0.05)
        om = tn.origen_movil(s)
        self.assertEqual(om["rotulo"], "RETROSPECTIVA-MECANICA")
        self.assertEqual(min(om["por_ola"]), 2013)             # K desde la 2ª ola
        self.assertEqual(om["ventana_comun"], list(range(2018, 2026)))   # TC exige 6 olas
        r = om["resumen"]
        self.assertAlmostEqual(r["TC"]["ventana_comun"]["mae_pp"], 0.0, places=8)
        self.assertGreater(r["K"]["ventana_comun"]["mae_pp"], 0.0)
        self.assertEqual(r["T5"]["todas"]["n_olas"], 9)
        self.assertEqual(r["T3"]["todas"]["n_olas"], 11)
        self.assertEqual(sorted(r), ["K", "T3", "T5", "TC"])   # las cuatro, siempre

    def test_wilson(self):
        lo, hi = tn.wilson(9, 10)
        self.assertLess(lo, 0.9)
        self.assertGreater(hi, 0.9)
        self.assertLessEqual(hi, 1.0)
        self.assertIsNone(tn.wilson(0, 0))


# ══ 3 · cableado ENVIPE sobre zips fabricados ═════════════════════════════

def _spec(calc_id):
    with (RAIZ / "data" / "corrida0" / calc_id / "spec.yaml").open(encoding="utf-8") as fh:
        return corrida0._yaml_safe_load(fh)


def _contrato(spec):
    return corrida0.contrato_ejecutable(spec)


class CableadoSintetico(unittest.TestCase):
    """Punta a punta con zips fabricados (n = 600 delitos por ola)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name)
        cls.zips = {}
        for anio, seed in ((2023, 3), (2024, 4), (2025, 5), (2026, 6)):
            z = cls.dir / f"envipe{anio}_csv.zip"
            fab.fabrica_zip(z, anio, n_delitos=600, seed=seed)
            cls.zips[anio] = z
        # celda rara: ola nueva chica, celdas vacías
        cls.zip_raro = cls.dir / "envipe2026_raro.zip"
        fab.fabrica_zip(cls.zip_raro, 2026, n_delitos=40, seed=9)
        cls.serie = (RAIZ / "data" / "corrida0" / "envipe-serie-denuncia-v1_0.tsv").read_bytes()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def _inputs(self, spec, zips=None):
        zips = zips or self.zips
        inputs = {}
        for ent in spec["inputs"]:
            iid = ent["id"]
            d = dict(ent)
            d["sha256"] = "sintetico"
            if ent.get("origen") == "repo":
                ruta = RAIZ / ent["ruta"]
                if ruta.exists():
                    d["bytes"] = ruta.read_bytes()
                d["ruta_absoluta"] = str(ruta)
            else:
                anio = int(iid.replace("envipe", "").replace("_csv", ""))
                d["ruta_absoluta"] = str(zips[anio])
            inputs[iid] = d
        return inputs

    def _corre(self, calc_id, zips=None, inputs_extra=None):
        spec = _spec(calc_id)
        con = _contrato(spec)
        con["parametros"]["bootstrap_replicas"] = 60       # rápido; la spec real trae 10 000
        inputs = self._inputs(spec, zips)
        if inputs_extra:
            inputs.update(inputs_extra)
        return spec, ed.medir(inputs, con)

    def _sin_no_finitos(self, out):
        for k, v in out.items():
            if isinstance(v, float):
                self.assertTrue(math.isfinite(v), f"{k} no finito: {v}")

    def test_emisiones_2026_guardia_y_valida_outputs(self):
        spec, out = self._corre("CALC-DUELO-ENVIPE2026-EMISIONES-0001")
        P = spec["parametros"]["prefijo_result"]
        self.assertEqual(out[f"{P}-G-RESERVA-OLA-CARGADA-RESERVADA"], "SI")
        self.assertEqual(out[f"{P}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO"], "NO")
        self.assertTrue(out[f"{P}-G-RESERVA-GUARDIA-PROBADA"].startswith("ReservaRota"))
        self.assertTrue(out[f"{P}-G-VETO-EXD-2025-PROBADO"].startswith("ReservaRota"))
        # ningún marginal crudo ni nacional de la ola nueva sale en emisiones
        self.assertFalse([k for k in out if "W2026-NUMERADOR" in k or "-R-" in k])
        self.assertIn(out[f"{P}-NAC-EN-T3-ESTADO"], ("CONSTRUIBLE",))
        self.assertTrue(out[f"{P}-NAC-EN-T5-ESTADO"].startswith("NO-CONSTRUIBLE"))
        self.assertIsNone(out[f"{P}-NAC-EN-T5-P"])
        self.assertEqual(out[f"{P}-NAC-ND-TC-ESTADO"], "CONSTRUIBLE")
        self._sin_no_finitos(out)
        self.assertEqual(corrida0._valida_outputs(spec, out), [])
        self.assertEqual(out[f"{P}-G-MEDIDOR-IDENTICO-A-TOOLS"], "SI")
        self.__class__.emisiones_2026 = (spec, out)

    def test_adjudicacion_2026_reproduce_y_adjudica(self):
        if not hasattr(self.__class__, "emisiones_2026"):
            self.test_emisiones_2026_guardia_y_valida_outputs()
        spec_e, out_e = self.__class__.emisiones_2026
        sellado = json.dumps({"spec_id": spec_e["calc_id"], "resultados": out_e}).encode()
        spec, out = self._corre("CALC-DUELO-ENVIPE2026-ADJUDICACION-0001",
                                inputs_extra={"emisiones_selladas": {
                                    "bytes": sellado, "sha256": "sintetico",
                                    "ruta_absoluta": "sintetico"}})
        P = spec["parametros"]["prefijo_result"]
        self.assertEqual(out[f"{P}-G-EMISIONES-REPRODUCIDAS"], "SI")
        self.assertEqual(out[f"{P}-G-OLA-NUEVA-ABIERTA"], "SI")
        self.assertEqual(out[f"{P}-G-SXD-ESTADO"], "ADJUDICADO")
        self.assertEqual(out[f"{P}-G-EXD-ESTADO"], "ADJUDICADO")
        self.assertIn(out[f"{P}-G-SXD-VEREDICTO-PRIMARIO"], cf.VEREDICTOS)
        self.assertIn(out[f"{P}-SXD-SL-ROL"], ("PRIMARIA",))
        self._sin_no_finitos(out)
        self.assertEqual(corrida0._valida_outputs(spec, out), [])

    def test_adjudicacion_para_si_emisiones_no_reproducen(self):
        if not hasattr(self.__class__, "emisiones_2026"):
            self.test_emisiones_2026_guardia_y_valida_outputs()
        spec_e, out_e = self.__class__.emisiones_2026
        alterado = dict(out_e)
        k = next(k for k in alterado if k.endswith("-SXD-C2-S1xD1-P"))
        alterado[k] = 0.123456
        sellado = json.dumps({"spec_id": spec_e["calc_id"], "resultados": alterado}).encode()
        with self.assertRaises(RuntimeError):
            self._corre("CALC-DUELO-ENVIPE2026-ADJUDICACION-0001",
                        inputs_extra={"emisiones_selladas": {
                            "bytes": sellado, "sha256": "x", "ruta_absoluta": "x"}})

    def test_celda_rara_n_cero_pasa_valida_outputs(self):
        zips = dict(self.zips)
        zips[2026] = self.zip_raro
        spec, out = self._corre("CALC-DUELO-ENVIPE2026-EMISIONES-0001", zips=zips)
        P = spec["parametros"]["prefijo_result"]
        nulos = [k for k in out if k.startswith(f"{P}-SXD-C2-") and k.endswith("-P") and out[k] is None]
        self.assertTrue(nulos, "la ola chica debía dejar alguna celda de C2 sin construir")
        self._sin_no_finitos(out)
        self.assertEqual(corrida0._valida_outputs(spec, out), [])
        sellado = json.dumps({"spec_id": spec["calc_id"], "resultados": out}).encode()
        spec_a, out_a = self._corre("CALC-DUELO-ENVIPE2026-ADJUDICACION-0001", zips=zips,
                                    inputs_extra={"emisiones_selladas": {
                                        "bytes": sellado, "sha256": "x", "ruta_absoluta": "x"}})
        self._sin_no_finitos(out_a)
        self.assertEqual(corrida0._valida_outputs(spec_a, out_a), [])

    def test_ensayo_2025_emisiones_y_adjudicacion_con_veto(self):
        spec, out = self._corre("CALC-DUELO-ENSAYO-ENVIPE2025-EMISIONES-0001")
        P = spec["parametros"]["prefijo_result"]
        self.assertEqual(out[f"{P}-G-OLA-NUEVA"], "2025")
        self.assertEqual(out[f"{P}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO"], "NO")
        self.assertIn(f"{P}-CTRL-SXD-C2-DELTA-P-MAX", out)     # control contra piloto 2
        self._sin_no_finitos(out)
        self.assertEqual(corrida0._valida_outputs(spec, out), [])
        sellado = json.dumps({"spec_id": spec["calc_id"], "resultados": out}).encode()
        spec_a, out_a = self._corre("CALC-DUELO-ENSAYO-ENVIPE2025-ADJUDICACION-0001",
                                    inputs_extra={"emisiones_selladas": {
                                        "bytes": sellado, "sha256": "x", "ruta_absoluta": "x"}})
        PA = spec_a["parametros"]["prefijo_result"]
        self.assertEqual(out_a[f"{PA}-G-SXD-ESTADO"], "ADJUDICADO")
        self.assertTrue(out_a[f"{PA}-G-EXD-ESTADO"].startswith("NO-ADJUDICABLE-VETO"))
        self.assertEqual(out_a[f"{PA}-G-EXD-VEREDICTO-PRIMARIO"], "NO-ADJUDICABLE")
        self._sin_no_finitos(out_a)
        self.assertEqual(corrida0._valida_outputs(spec_a, out_a), [])

    def test_origen_movil_sobre_sellados(self):
        spec = _spec("CALC-DUELO-ORIGEN-MOVIL-0001")
        out = ed.medir(self._inputs(spec), _contrato(spec))
        P = spec["parametros"]["prefijo_result"]
        self.assertEqual(out[f"{P}-G-ND-OLAS-EN-SERIE"], 15)
        self.assertEqual(out[f"{P}-OM-ND-OLAS-NO-COMPARABLES"], "2011")
        for cid in ("K", "T3", "T5", "TC"):
            self.assertIn(f"{P}-OM-ND-RESUMEN-{cid}-VENTANA-COMUN-MAE-PP", out)
        self._sin_no_finitos(out)
        self.assertEqual(corrida0._valida_outputs(spec, out), [])

    def test_medidor_de_cada_calc_es_byte_a_byte_el_de_tools(self):
        ref = (RAIZ / "tools" / "duelo" / "envipe_duelo.py").read_bytes()
        for calc_id, pe in CALCS_DUELO.items():
            med = RAIZ / "data" / "corrida0" / calc_id / "medidor.py"
            self.assertEqual(med.read_bytes(), ref, calc_id)
            self.assertEqual(_spec(calc_id)["parametros"]["punto_de_entrada"], pe)


if __name__ == "__main__":
    unittest.main()
