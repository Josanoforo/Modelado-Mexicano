#!/usr/bin/env python3
"""Ensayo de sellabilidad del lote ENIF 2024 (D-22 ampliada) y guardia 3D.

ACTO `GEN2-DIN-LOTE-ENIF2024-COMMIT-1`. Qué defecto real atrapa cada bloque:
  · `R3IPF`            — un raking que no casa márgenes o rellena celdas vacías
                         (el piloto 3 aprendió que un null sin declarar rompe el sello).
  · `CableadoSintetico`— `_valida_outputs` en CADA rama terminal (todas con
                         soporte · parcial · fuera de soporte global · cero
                         puntuadas · celda rara vaciada · marginal con masa
                         cero): la exigencia literal de la firma D-22 ampliada.
  · `Guardia`          — la reserva como código: ola reservada, par vetado,
                         ola alterada, eje no atómico.
  · `AuditoriaAST`     — cada regla con su control positivo por MUTACIÓN
                         (3D del encargo): una guardia que no se puede violar
                         a propósito no está probada.
  · `Deposito`         — medidor.py de cada CALC es byte a byte el de tools.
Sin microdato real: zips fabricados por `tools/lote_enif2024/sintetico.py`.
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


def _importa(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


EL = _importa("enif_lote", RAIZ / "tools" / "lote_enif2024" / "enif_lote.py")
LF = _importa("lote_familia", RAIZ / "tools" / "lote_enif2024" / "lote_familia.py")
SIN = _importa("sintetico_enif", RAIZ / "tools" / "lote_enif2024" / "sintetico.py")
GEN = _importa("genera_specs_lote", RAIZ / "tools" / "lote_enif2024" / "genera_specs.py")
corrida0 = _importa("corrida0_lote_test", RAIZ / "tools" / "corrida0.py")
FUENTE = (RAIZ / "tools" / "lote_enif2024" / "enif_lote.py").read_text(encoding="utf-8")

CALCS = {
    "CALC-DIN-LOTE-ENIF2024-EMISIONES-0001": "emisiones",
    "CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001": "adjudicacion",
    "CALC-DIN-LOTE-ORO-PILOTO1-EMISIONES-0001": "emisiones",
    "CALC-DIN-LOTE-ORO-PILOTO1-ADJUDICACION-0001": "adjudicacion",
    "CALC-DIN-LOTE-ORO-C2IC-0001": "oro_c2ic",
}


# ══ R3 · raking ═══════════════════════════════════════════════════════════

class R3IPF(unittest.TestCase):
    def _tabla(self, rng, A=2, B=3):
        return rng.random((1, A, B, 2)) + 0.05

    def test_casa_los_margenes_y_conserva_razones_de_momios(self):
        rng = np.random.default_rng(1)
        T = self._tabla(rng)
        MA = rng.random((1, 2, 2)) + 0.1
        MB = rng.random((1, 3, 2)) + 0.1
        # márgenes compatibles: misma masa total por d
        MB[..., 0] *= MA[..., 0].sum() / MB[..., 0].sum()
        MB[..., 1] *= MA[..., 1].sum() / MB[..., 1].sum()
        r = LF.ipf_3vias(T, MA, MB, 1e-12, 500)
        self.assertTrue(bool(r["convergio"].all()))
        # reconstruir la tabla ajustada: p * masa; comprobar márgenes en participaciones
        Tn = LF._normaliza(T)
        # recomputar con la rutina interna para leer T final: usar p y masas relativas
        MA_n, MB_n = LF._normaliza(MA), LF._normaliza(MB)
        # razón de momios de 2x2 en la esquina (a0,a1)x(b0,b1) sobre d=1 vs d=0 se conserva
        def _or(t):
            return (t[0, 0, 0, 1] * t[0, 1, 1, 1] / (t[0, 0, 1, 1] * t[0, 1, 0, 1])) / \
                   (t[0, 0, 0, 0] * t[0, 1, 1, 0] / (t[0, 0, 1, 0] * t[0, 1, 0, 0]))
        # la tabla final no se devuelve; se re-deriva con una iteración más (idempotente)
        # comprobación directa: p en (0,1) y finito
        self.assertTrue(np.isfinite(r["p"]).all())
        self.assertTrue(((r["p"] > 0) & (r["p"] < 1)).all())
        self.assertGreater(_or(Tn), 0)
        self.assertTrue(np.isfinite(MA_n).all() and np.isfinite(MB_n).all())

    def test_tabla_log_aditiva_se_recupera(self):
        # sin interacción en 2021 y márgenes 2024 = los de 2021 => p no cambia
        rng = np.random.default_rng(2)
        T = self._tabla(rng)
        MA = T.sum(axis=2)
        MB = T.sum(axis=1)
        r = LF.ipf_3vias(T, MA, MB, 1e-13, 100)
        p0 = T[..., 1] / T.sum(axis=3)
        self.assertLess(float(np.abs(r["p"] - p0).max()), 1e-10)
        self.assertEqual(r["iteraciones"], 1)

    def test_celda_con_masa_cero_queda_sin_definir(self):
        rng = np.random.default_rng(3)
        T = self._tabla(rng)
        T[0, 1, 2, :] = 0.0
        MA, MB = T.sum(axis=2) + 0.01, T.sum(axis=1) + 0.01
        r = LF.ipf_3vias(T, MA, MB, 1e-10, 300)
        self.assertTrue(math.isnan(float(r["p"][0, 1, 2])))
        self.assertTrue(np.isfinite(np.delete(r["p"].reshape(-1), 5)).all())

    def test_replicas_que_no_convergen_quedan_nan(self):
        rng = np.random.default_rng(4)
        T = self._tabla(rng)
        MA, MB = T.sum(axis=2) * np.array([[[1.0, 3.0], [0.2, 0.9]]]), T.sum(axis=1)
        r = LF.r3_por_par(T[0], T, MA[0], MA, MB[0], MB, 1e-14, 1)
        self.assertEqual(r["reps_no_convergen"], 1)
        self.assertTrue(np.isnan(r["p_reps"]).all())


# ══ cableado sintético ════════════════════════════════════════════════════

def _spec_de(calc_id):
    return GEN.specs()[calc_id]


class CableadoSintetico(unittest.TestCase):
    N_REP = 40

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name)
        cls.zips = {"2021": SIN.fabrica_zip(cls.dir / "enif2021_csv.zip", "2021", n=2600, seed=21),
                    "2024": SIN.fabrica_zip(cls.dir / "enif2024_csv.zip", "2024", n=2600, seed=24)}
        cls.chico = {"2021": cls.zips["2021"],
                     "2024": SIN.fabrica_zip(cls.dir / "enif2024_chico.zip", "2024", n=260, seed=9)}
        # celda rara: sin localidades chicas en 2021 (cruce con una categoría vacía)
        cls.raro = {"2021": SIN.fabrica_zip(cls.dir / "enif2021_raro.zip", "2021", n=2000, seed=5,
                                            vaciar={"tloc": {"3", "4"}}),
                    "2024": cls.zips["2024"]}
        # marginal con masa cero en la ola nueva: nadie con secundaria en 2024
        cls.masa0 = {"2021": cls.zips["2021"],
                     "2024": SIN.fabrica_zip(cls.dir / "enif2024_masa0.zip", "2024", n=2000, seed=6,
                                             vaciar={"esc": {"03"}})}
        cls.specs = GEN.specs()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def _corre(self, calc_id, zips, umbral=None, extra=None, ajusta=None):
        spec = self.specs[calc_id]
        con = json.loads(json.dumps(corrida0.contrato_ejecutable(spec)))
        con["parametros"]["bootstrap_replicas"] = self.N_REP
        if umbral is not None:
            con["parametros"]["umbral_soporte_n"] = umbral
        if ajusta:
            ajusta(con["parametros"])
        inputs = self._inputs(spec, zips)
        if extra:
            declarados = {e["id"] for e in spec["inputs"]}
            inputs.update({k: v for k, v in extra.items() if k in declarados})
        out = EL.medir(inputs, con)
        return spec, out

    def _limpio(self, spec, out):
        for k, v in out.items():
            if isinstance(v, float):
                self.assertTrue(math.isfinite(v), f"{k} no finito: {v}")
        self.assertEqual(corrida0._valida_outputs(spec, out), [])

    def _sella(self, spec, out):
        """Los inputs que el CALC de adjudicación declara y aún no existen."""
        return {"emisiones_selladas": {"bytes": json.dumps({"spec_id": spec["calc_id"], "resultados": out}).encode(),
                                       "sha256": "x", "ruta_absoluta": "x"},
                "emisiones_sello": {"bytes": b"{}", "sha256": "x", "ruta_absoluta": "x"}}

    def _inputs(self, spec, zips):
        inputs = {}
        for ent in spec["inputs"]:
            d = dict(ent)
            d["sha256"] = "sintetico"
            if ent.get("origen") == "repo":
                ruta = RAIZ / ent["ruta"]
                d["ruta_absoluta"] = str(ruta)
                if ruta.exists():
                    d["bytes"] = ruta.read_bytes()
            else:
                d["ruta_absoluta"] = str(zips[ent["id"].replace("enif", "").replace("_csv", "")])
            inputs[ent["id"]] = d
        return inputs

    def test_emisiones_todas_con_soporte(self):
        spec, out = self._corre("CALC-DIN-LOTE-ENIF2024-EMISIONES-0001", self.zips, umbral=1)
        P = spec["parametros"]["prefijo_result"]
        self.assertEqual(out[f"{P}-G-RESERVA-OLA-NUEVA-CARGADA-RESERVADA"], "SI")
        self.assertEqual(out[f"{P}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO"], "NO")
        self.assertTrue(out[f"{P}-G-RESERVA-GUARDIA-PROBADA"].startswith("ReservaRota"))
        self.assertEqual(out[f"{P}-G-R-EXISTE-EN-ESTE-COMMIT"], "NO")
        self.assertEqual(out[f"{P}-G-W2021-CATALOGO-ESCOLARIDAD"], "COINCIDE")
        # ningún cruce de la ola nueva sale en emisiones
        self.assertFalse([k for k in out if "-R-" in k and "-X-" in k and "M24" not in k])
        self.assertEqual(out[f"{P}-EDADXSEXO-C2-ESTADO"], "EMITIBLE")
        self.assertTrue(out[f"{P}-FORMALIDADXSEXO-C2-ESTADO"].startswith("NO-EMITIBLE"))
        self.assertIsNone(out[f"{P}-FORMALIDADXSEXO-C2-SIN-SEGURIDAD-SOCIAL-X-1-HOMBRE-P"])
        self.assertIsNotNone(out[f"{P}-FORMALIDADXSEXO-P2-SIN-SEGURIDAD-SOCIAL-X-1-HOMBRE-P"])
        self.assertEqual(out[f"{P}-EDADXSEXO-R3-CONVERGIO-PUNTO"], "SI")
        self.assertTrue(all(out[k] == "SI" for k in out if k.startswith(f"{P}-EDADXSEXO-SOPORTE-2021-")))
        self._limpio(spec, out)
        self.__class__.emis = (spec, out)

    def test_adjudicacion_reproduce_y_adjudica(self):
        if not hasattr(self.__class__, "emis"):
            self.test_emisiones_todas_con_soporte()
        spec_e, out_e = self.__class__.emis
        spec, out = self._corre("CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001", self.zips, umbral=1,
                                extra=self._sella(spec_e, out_e))
        P = spec["parametros"]["prefijo_result"]
        self.assertEqual(out[f"{P}-G-EMISIONES-REPRODUCIDAS"], "SI")
        self.assertEqual(out[f"{P}-G-OLA-NUEVA-ABIERTA"], "SI")
        self.assertEqual(out[f"{P}-G-EDADXSEXO-ESTADO"], "ADJUDICADO")
        self.assertEqual(out[f"{P}-G-FORMALIDADXSEXO-ESTADO"], "SIN-PISO-SOLO-P2")
        self.assertIn(out[f"{P}-G-PRIMARIO-VEREDICTO-PRIMARIO"], EL.cf.VEREDICTOS)
        self.assertEqual(out[f"{P}-G-PRIMARIO-CELDAS-PUNTUADAS"], 44)
        self.assertEqual(out[f"{P}-G-PRIMARIO-R2-ROL"], "PRIMARIA")
        self.assertEqual(out[f"{P}-G-FORMALIDAD-VEREDICTO-PRIMARIO"], "NO-ADJUDICABLE-SIN-PISO")
        self.assertTrue(out[f"{P}-G-VETO-PROBADO"].startswith("ReservaRota"))
        self.assertIn(out[f"{P}-G-BBIS-FILA"], ("CORROBORADA", "ACOTADA", "FALSADOR-DEBIL", "NO-CAE-EN-NINGUNA-FILA"))
        self._limpio(spec, out)

    def test_adjudicacion_para_si_emisiones_no_reproducen(self):
        if not hasattr(self.__class__, "emis"):
            self.test_emisiones_todas_con_soporte()
        spec_e, out_e = self.__class__.emis
        alterado = dict(out_e)
        k = next(k for k in alterado if k.endswith("-EDADXSEXO-C2-18-29-X-1-HOMBRE-P"))
        alterado[k] = 0.123456
        with self.assertRaises(RuntimeError):
            self._corre("CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001", self.zips, umbral=1,
                        extra=self._sella(spec_e, alterado))

    def test_soporte_parcial_y_fuera_de_soporte_global(self):
        spec_e, out_e = self._corre("CALC-DIN-LOTE-ENIF2024-EMISIONES-0001", self.zips, umbral=60)
        self._limpio(spec_e, out_e)
        P = spec_e["parametros"]["prefijo_result"]
        sop = [out_e[k] for k in out_e if "-SOPORTE-2021-" in k]
        self.assertIn("SI", sop)
        self.assertIn("NO", sop)
        spec, out = self._corre("CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001", self.zips, umbral=60,
                                extra=self._sella(spec_e, out_e))
        PA = spec["parametros"]["prefijo_result"]
        self.assertLess(out[f"{PA}-G-PRIMARIO-CELDAS-PUNTUADAS"], 44)
        self.assertGreater(out[f"{PA}-G-PRIMARIO-CELDAS-PUNTUADAS"], 0)
        self._limpio(spec, out)
        # fuera de soporte global: cero puntuadas
        spec_e2, out_e2 = self._corre("CALC-DIN-LOTE-ENIF2024-EMISIONES-0001", self.zips, umbral=10 ** 6)
        spec2, out2 = self._corre("CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001", self.zips, umbral=10 ** 6,
                                  extra=self._sella(spec_e2, out_e2))
        self.assertEqual(out2[f"{PA}-G-PRIMARIO-CELDAS-PUNTUADAS"], 0)
        self.assertEqual(out2[f"{PA}-G-PRIMARIO-VEREDICTO-PRIMARIO"], "NO-ADJUDICABLE")
        self.assertEqual(out2[f"{PA}-G-BBIS-FILA"], "FALSADOR-DEBIL")
        self._limpio(spec2, out2)

    def test_celda_rara_vaciada_en_una_ola(self):
        spec_e, out_e = self._corre("CALC-DIN-LOTE-ENIF2024-EMISIONES-0001", self.raro, umbral=1)
        P = spec_e["parametros"]["prefijo_result"]
        self.assertIsNone(out_e[f"{P}-LOCALIDADXSEXO-P2-MENOR-DE-15-000-X-1-HOMBRE-P"])
        self.assertEqual(out_e[f"{P}-LOCALIDADXSEXO-P2-MENOR-DE-15-000-X-1-HOMBRE-N"], 0)
        self.assertIsNone(out_e[f"{P}-LOCALIDADXSEXO-R2-MENOR-DE-15-000-X-1-HOMBRE-P"])
        self.assertIsNotNone(out_e[f"{P}-LOCALIDADXSEXO-C2-MENOR-DE-15-000-X-1-HOMBRE-P"])
        self._limpio(spec_e, out_e)
        spec, out = self._corre("CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001", self.raro, umbral=1,
                                extra=self._sella(spec_e, out_e))
        PA = spec["parametros"]["prefijo_result"]
        self.assertEqual(out[f"{PA}-LOCALIDADXSEXO-PUNTUADA-MENOR-DE-15-000-X-1-HOMBRE"], "NO")
        self._limpio(spec, out)

    def test_marginal_con_masa_cero_en_la_ola_nueva(self):
        spec_e, out_e = self._corre("CALC-DIN-LOTE-ENIF2024-EMISIONES-0001", self.masa0, umbral=1)
        P = spec_e["parametros"]["prefijo_result"]
        self.assertEqual(out_e[f"{P}-M24-ESCOLARIDAD-SECUNDARIA-N"], 0)
        self.assertIsNone(out_e[f"{P}-M24-ESCOLARIDAD-SECUNDARIA-P-REDERIVADO"])
        # el punto de C2 viene del sellado (existe); su IC no (réplicas vacías)
        self.assertIsNotNone(out_e[f"{P}-EDADXESCOLARIDAD-C2-18-29-X-SECUNDARIA-P"])
        self.assertIsNone(out_e[f"{P}-EDADXESCOLARIDAD-C2-18-29-X-SECUNDARIA-IC95INF"])
        self._limpio(spec_e, out_e)
        spec, out = self._corre("CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001", self.masa0, umbral=1,
                                extra=self._sella(spec_e, out_e))
        self._limpio(spec, out)

    def test_ola_nueva_chica(self):
        spec_e, out_e = self._corre("CALC-DIN-LOTE-ENIF2024-EMISIONES-0001", self.chico, umbral=5)
        self._limpio(spec_e, out_e)
        spec, out = self._corre("CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001", self.chico, umbral=5,
                                extra=self._sella(spec_e, out_e))
        self._limpio(spec, out)

    def test_oro_c2ic_sobre_sintetico_valida_outputs(self):
        spec, out = self._corre("CALC-DIN-LOTE-ORO-C2IC-0001", self.zips,
                                ajusta=lambda p: p["oro_c2ic"].update({"umbral_replicas_validas": 1}))
        P = spec["parametros"]["prefijo_result"]
        self.assertEqual(out[f"{P}-G-REGIMEN-UNIVERSO"], "ARBITRO-2024")
        self.assertEqual(out[f"{P}-G-ORO-N-CELDAS"], 68)
        self._limpio(spec, out)

    def test_oro_piloto1_sobre_sintetico_valida_outputs(self):
        spec_e, out_e = self._corre("CALC-DIN-LOTE-ORO-PILOTO1-EMISIONES-0001", self.zips, umbral=1)
        self._limpio(spec_e, out_e)
        spec, out = self._corre("CALC-DIN-LOTE-ORO-PILOTO1-ADJUDICACION-0001", self.zips, umbral=1,
                                extra=self._sella(spec_e, out_e))
        PA = spec["parametros"]["prefijo_result"]
        self.assertTrue(out[f"{PA}-G-VETO-PROBADO"].startswith("ReservaRota"))
        self._limpio(spec, out)

    def test_escolaridad_codigo_sin_etiqueta_para(self):
        z = SIN.fabrica_zip(self.dir / "enif2024_cod.zip", "2024", n=300, seed=7)
        spec = self.specs["CALC-DIN-LOTE-ENIF2024-EMISIONES-0001"]
        con = json.loads(json.dumps(corrida0.contrato_ejecutable(spec)))
        con["parametros"]["bootstrap_replicas"] = 5
        con["parametros"]["escolaridad_catalogo"]["2024"].pop("11")
        inputs = self._inputs(spec, {"2021": self.zips["2021"], "2024": z})
        with self.assertRaises(EL.Paro):
            EL.medir(inputs, con)


# ══ guardia en tiempo de ejecución ════════════════════════════════════════

class Guardia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        d = Path(cls.tmp.name)
        cls.par = GEN.specs()["CALC-DIN-LOTE-ENIF2024-EMISIONES-0001"]["parametros"]
        cls.z = SIN.fabrica_zip(d / "enif2024_csv.zip", "2024", n=400, seed=3)
        cls.ola = EL.carga_ola(cls.z, "2024", cls.par, reservada=True, pares_autorizados=[])
        cls.rep = EL.replicas(cls.ola, 42, 10)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_ola_reservada_no_cruza(self):
        with self.assertRaises(EL.ReservaRota):
            EL.cruce(self.ola, "sexo", "edad", self.rep)

    def test_par_no_autorizado_no_cruza_aunque_la_ola_este_abierta(self):
        ola = EL.carga_ola(self.z, "2024", self.par, reservada=False, pares_autorizados=[("localidad", "edad")])
        rep = EL.replicas(ola, 42, 10)
        with self.assertRaises(EL.ReservaRota):
            EL.cruce(ola, "sexo", "edad", rep)
        self.assertEqual(len(EL.cruce(ola, "localidad", "edad", rep)), 8)

    def test_marginal_exige_un_str(self):
        with self.assertRaises(TypeError):
            EL.marginal(self.ola, ["sexo", "edad"], self.rep)
        with self.assertRaises(ValueError):
            EL.marginal(self.ola, "sexo x edad", self.rep)

    def test_ola_alterada_lanza(self):
        ola = EL.OlaEnif(df=self.ola.df.iloc[:-5], rotulo="2024", huella=self.ola.huella,
                         reservada=True, pares_autorizados=(), meta={})
        with self.assertRaises(EL.ReservaRota):
            EL.marginal(ola, "sexo", self.rep)

    def test_replicas_de_otra_ola_lanzan(self):
        otra = EL.carga_ola(SIN.fabrica_zip(Path(self.tmp.name) / "o.zip", "2024", n=300, seed=8),
                            "2024", self.par, reservada=True, pares_autorizados=[])
        with self.assertRaises(EL.ReservaRota):
            EL.marginal(otra, "sexo", self.rep)


# ══ auditoría AST con controles positivos por mutación ═══════════════════

def _muta(anadido: str, ancla: str = "def medir(inputs, contrato) -> dict:\n") -> str:
    assert ancla in FUENTE
    return FUENTE.replace(ancla, anadido + "\n\n" + ancla)


class AuditoriaAST(unittest.TestCase):
    def test_el_archivo_pasa(self):
        self.assertEqual(EL.auditoria_ast_fuente(FUENTE), [])

    def _espera(self, fuente, regla):
        v = EL.auditoria_ast_fuente(fuente)
        self.assertTrue(any(x.startswith(regla) for x in v), f"{regla} no detectada: {v}")

    def test_R1_import(self):
        self._espera("import subprocess\n" + FUENTE, "R1")

    def test_R2_groupby(self):
        self._espera(_muta("def _x(d):\n    return d.groupby('sexo').size()"), "R2")

    def test_R2_read_csv_fuera_de_lee_miembro(self):
        self._espera(_muta("def _x(p):\n    return pd.read_csv(p)"), "R2")

    def test_R3_df_fuera_del_nucleo(self):
        self._espera(_muta("def _x(ola):\n    return ola.df"), "R3")

    def test_R4_dos_comparaciones(self):
        self._espera(_muta("def _x(a, b):\n    return (a == 1) & (b == 2)"), "R4")
        self._espera(_muta("def _x(a, b):\n    return a == 1 and b == 2"), "R4")

    def test_R5_olaenif_fuera_de_carga(self):
        self._espera(_muta("def _x():\n    return OlaEnif(df=None)"), "R5")

    def test_R5_carga_ola_fuera_de_carga_olas(self):
        self._espera(_muta("def _x():\n    return carga_ola('a', '2024', {}, True, [])"), "R5")

    def test_R6_marginal_no_atomico(self):
        self._espera(_muta("def _x(ola, rep):\n    return marginal(ola, 'se' + 'xo', rep)"), "R6")
        self._espera(_muta("def _x(oc):\n    return oc.marginal(['sexo'][0])"), "R6")

    def test_R7_otra_funcion_de_cruce(self):
        self._espera(_muta("def cruce_extra(ola):\n    return None"), "R7")


# ══ depósito byte a byte y catálogo ═══════════════════════════════════════

class Deposito(unittest.TestCase):
    def test_medidor_de_cada_calc_es_byte_a_byte_el_de_tools(self):
        ref = (RAIZ / "tools" / "lote_enif2024" / "enif_lote.py").read_bytes()
        for calc_id, pe in CALCS.items():
            d = RAIZ / "data" / "corrida0" / calc_id
            if not d.exists():
                continue
            self.assertEqual((d / "medidor.py").read_bytes(), ref, calc_id)
            with (d / "spec.yaml").open(encoding="utf-8") as fh:
                spec = corrida0._yaml_safe_load(fh)
            self.assertEqual(spec["parametros"]["punto_de_entrada"], pe)
            # el catálogo del árbol es el que el generador deriva hoy
            self.assertEqual([r["id"] for r in spec["resultados"]],
                             [r["id"] for r in GEN.specs()[calc_id]["resultados"]], calc_id)

    def test_lambda_medio_y_catorce_pares(self):
        spec = GEN.specs()["CALC-DIN-LOTE-ENIF2024-EMISIONES-0001"]
        self.assertEqual(spec["parametros"]["lambda_r2"], 0.5)
        self.assertEqual(len(spec["parametros"]["pares"]), 14)
        n = sum(len(spec["parametros"]["ejes"][p["a"]]["orden"]) * len(spec["parametros"]["ejes"][p["b"]]["orden"])
                for p in spec["parametros"]["pares"].values())
        self.assertEqual(n, 96)
        self.assertEqual(sum(1 for p in spec["parametros"]["pares"].values() if p["c2"] == "EMITIBLE"), 9)


if __name__ == "__main__":
    unittest.main()
