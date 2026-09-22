#!/usr/bin/env python3
"""Guardia E.6 y conducto del medidor de `CALC-C2-RESTRINGIDO-IC-ENIF2024-0001`.

ACTO `GEN2-DIN-LOTE-C2-RESTRINGIDO-1` (22/sep/2026). Spec humana:
`forense/prereg-caja/C2-RESTRINGIDO-ENIF2024-spec-v1_0.md` §7-§8. Qué defecto
real atrapa cada capa:

  1. AST con un control positivo por regla -- NC-0328 (reserva quemada por
     un script de scratch) y PARO a del encargo (derivar un cruce de ENIF
     2024): el medidor no puede combinar dos comparaciones, tocar `.df` fuera
     del núcleo, ni leer otro payload.
  2. Guardia de una variable en tiempo de ejecución, sobre datos FABRICADOS
     (cero microdato, E.5).
  3. El plan de réplicas del medidor ES el de `_estimate` del piso que el
     árbitro GEN2 importó (`CALC-PISOS-ENIF2021-EJES-0003/medidor.py`,
     importado AQUÍ, no en el medidor): punto, IC, N, DEN-W y B-VALIDAS a
     1e-12 sobre una ola fabricada. Sin esto el oro del COMMIT-2 sería el
     primer lugar donde se descubre un plan distinto (defecto medido en
     #926: IC corridos 2e-3 por recortar el marco).
  4. Conducto (D-22): el procedimiento entero sobre una ola fabricada pasa
     `corrida0._valida_outputs` en cada rama terminal -- oro REPRODUCE, oro
     NO-REPRODUCE, categoría sin filas en T, marginal degenerado, réplicas
     bajo el umbral. #951 perdió un acto con preflight VERDE por no hacerlo.
     El árbitro sellado del fixture se fabrica desde los ids REALES de su
     `resultados.json` y con valores de `_estimate` del piso, nunca con la
     clave ni el código del medidor (#951: fixture circular).
  5. `spec.yaml` declara EXACTAMENTE el catálogo del medidor.

Correr:  python3 tests/test_c2_restringido_enif2024_guardia.py
"""
from __future__ import annotations

import copy
import dataclasses
import hashlib
import importlib.util
import json
import random
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data" / "corrida0" / "CALC-C2-RESTRINGIDO-IC-ENIF2024-0001"
MEDIDOR = CALC / "medidor.py"
PISO = RAIZ / "data" / "corrida0" / "CALC-PISOS-ENIF2021-EJES-0003" / "medidor.py"
PISO_SHA = "d069f38bd75c47fd5550015b179c7b2e61f1ab20ce6b22c630c66392afea06a3"


def _carga(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


M = _carga("medidor_c2_restringido_enif2024", MEDIDOR)
sys.path.insert(0, str(RAIZ / "tools"))
import corrida0  # noqa: E402


# ══ fixture fabricado: la forma que `carga()` del árbitro devuelve ═══════════

def fabrica_df(n: int = 1200, seed: int = 11) -> pd.DataFrame:
    rng = random.Random(seed)
    filas = []
    for i in range(n):
        est = f"{1 + i % 6:03d}"
        upm = f"{1 + (i // 3) % 60:04d}"
        fila = {
            "SEXO": rng.choice(["1", "2"]),
            "EDAD_V": str(rng.randint(18, 99)),
            "NIV": rng.choice(["00", "01", "02", "03", "04", "05", "06", "07",
                               "08", "09", "10", "11", "99"]),
            "TLOC": rng.choice(["1", "2", "3", "4"]),
            "P3_13": rng.choice(["1", "2", "3", "4", "5", "6", "7", "7", "9", ""]),
            "FAC_PER": str(rng.randint(50, 900)),
            "EST_DIS": est, "UPM_DIS": upm,
        }
        for c in M._ARB.INFORMAL:
            fila[c] = rng.choice(["1", "2", "2", ""])
        for c in M._ARB.FORMAL:
            fila[c] = rng.choice(["1", "2", "2", "2", ""])
        for c in M._ARB.CUENTAS:
            fila[c] = rng.choice(["1", "2", "2", ""])
        filas.append(fila)
    df = pd.DataFrame(filas)
    df["_w"] = pd.to_numeric(df["FAC_PER"])
    df["_edad"] = pd.to_numeric(df["EDAD_V"])
    return df


def _spec():
    return yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))


def _inputs_repo(spec):
    inputs = {}
    for ent in spec["inputs"]:
        d = dict(ent)
        if ent.get("origen") == "repo":
            d["bytes"] = (RAIZ / ent["ruta"]).read_bytes()
            d["sha256"] = hashlib.sha256(d["bytes"]).hexdigest()
        else:
            d["sha256"] = "0" * 64
        inputs[ent["id"]] = d
    return inputs


def _piso():
    assert hashlib.sha256(PISO.read_bytes()).hexdigest() == PISO_SHA, "el piso sellado cambió"
    return _carga("piso_enif2021_ejes_0003", PISO)


def _estimate_de_la_ola(ola, ejes, n_rep):
    """Marginales de la ola por el `_estimate` del piso (código ajeno al
    medidor): {(eje, celda): {P, IC-LO, IC-HI, N, DEN-W, B-VALIDAS}}."""
    piso = _piso()
    d = pd.DataFrame({"_w": ola.df["_w"], "_est": ola.df["EST_DIS"], "_upm": ola.df["UPM_DIS"]})
    y = ola.df[f"_y_{M.DESENLACE}"]
    cells = []
    for e in ejes:
        for k in M._orden(e):
            cells.append({"base": f"X|{e}|{k}", "mask": ola.df[e].eq(k), "y": y})
    r = piso._estimate(d, cells, reps=n_rep, seed=42)
    out = {}
    for e in ejes:
        for k in M._orden(e):
            b = f"X|{e}|{k}"
            out[(e, k)] = {s: r[f"{b}-{s}"] for s in ("P", "IC-LO", "IC-HI", "N", "DEN-W", "B-VALIDAS")}
    return out


class Fixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ola = M._ola_desde_df(fabrica_df())
        cls.rep = M.replicas_t(cls.ola, seed=42, n_rep=200, bloque=50)


# ══ capa 1 · el AST del medidor, con un control positivo por regla ══════════

FUENTE = MEDIDOR.read_text(encoding="utf-8")
ANCLA = "def medir(inputs: dict, contrato: dict) -> dict:\n"


def _muta(anadido: str, ancla: str = ANCLA) -> str:
    assert ancla in FUENTE, "ancla de mutación ausente"
    cuerpo = "".join(f"    {l}\n" for l in anadido.splitlines())
    return FUENTE.replace(ancla, ancla + cuerpo, 1)


class AuditoriaAST(unittest.TestCase):
    def test_el_medidor_congelado_pasa_limpio(self):
        viol = M.auditoria_ast(MEDIDOR)
        self.assertEqual(viol, [], "\n".join(viol))

    def _espera(self, fuente: str, regla: str):
        viol = M.auditoria_ast_fuente(fuente)
        self.assertTrue(any(v.startswith(regla) for v in viol),
                        f"la mutación {regla} no fue detectada: {viol}")

    def test_R1_import_fuera_de_lista(self):
        self._espera("import zipfile\n" + FUENTE, "R1")

    def test_R2_groupby_de_dos_variables(self):
        self._espera(_muta('x = pd.DataFrame().groupby(["sexo", "formalidad"]).size()'), "R2")

    def test_R2_crosstab(self):
        self._espera(_muta("x = pd.crosstab([1], [2])"), "R2")

    def test_R2_pivot_table(self):
        self._espera(_muta("x = pd.DataFrame().pivot_table(index='a', columns='b')"), "R2")

    def test_R2_apertura_directa_de_archivo(self):
        self._espera(_muta("x = open('/dev/null').read()"), "R2")

    def test_R2_getattr_para_alcanzar_el_df(self):
        self._espera(_muta("x = getattr(ola, 'd' + 'f')"), "R2")

    def test_R3_df_fuera_del_nucleo(self):
        self._espera(_muta("ola0 = _carga_ola_enif(inputs)\nx = ola0.df"), "R3")

    def test_R4_dos_mascaras_combinadas_en_el_nucleo(self):
        ancla = "        mask = celda == k\n"
        assert ancla in FUENTE
        fuente = FUENTE.replace(ancla, ancla + "        mask = (celda == k) & (y_all > 0)\n", 1)
        self._espera(fuente, "R4")

    def test_R4_formalidad_por_eje_en_la_construccion_de_la_ola(self):
        ancla = "    d[\"nacional\"] = np.where(fuera_de_t, FUERA, NAC_T)\n"
        assert ancla in FUENTE
        fuente = FUENTE.replace(ancla, ancla + "    x = (universo == 'x') & (d['sexo'] == 'y')\n", 1)
        self._espera(fuente, "R4")

    def test_R4_dos_comparaciones_por_and(self):
        self._espera(_muta("x = [1 for i in range(3) if i > 0 and i < 2]"), "R4")

    def test_R4_producto_de_dos_mascaras(self):
        self._espera(_muta("x = (np.arange(3) > 0) * (np.arange(3) < 2)"), "R4")

    def test_R5_ola_construida_fuera_de_su_sitio(self):
        self._espera(_muta("x = OlaT(df=pd.DataFrame(), huella='', meta={})"), "R5")

    def test_R5_carga_del_arbitro_fuera_de_su_sitio(self):
        self._espera(_muta("x = _ARB.carga()"), "R5")

    def test_R5_importa_modulo_no_autorizado(self):
        self._espera(_muta('x = _importa("otro", RAIZ / "tools" / "marcador_segmento.py")'), "R5")

    def test_R6_marginal_con_lista(self):
        self._espera(_muta('x = marginal_t(None, ["sexo", "formalidad"], desenlace="ahorra_solo_informal")'), "R6")

    def test_R6_marginal_con_tres_posicionales(self):
        self._espera(_muta('x = marginal_t(None, "sexo", "formalidad")'), "R6")

    def test_R7_funcion_de_cruce(self):
        self._espera(FUENTE + "\n\ndef cruce_t(ola, a, b):\n    return None\n", "R7")

    def test_R8_payload_de_otro_instrumento(self):
        self._espera(_muta('x = inputs["envipe2025_csv"]'), "R8")

    def test_R8_archivo_no_autorizado(self):
        self._espera(_muta('x = "conjunto_de_datos_tmodulo_enif2024.csv"'), "R8")

    def test_R8_input_no_declarado(self):
        self._espera(_muta('x = inputs["IN-C2-COMPUESTO-RESULTADOS"]'), "R8")


# ══ capa 2 · la guardia en tiempo de ejecución, sobre datos fabricados ═══════

class GuardiaUnaVariable(Fixture):
    def test_firma_un_solo_grupo_posicional(self):
        import inspect
        sig = inspect.signature(M.marginal_t)
        pos = [p for p in sig.parameters.values()
               if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
        self.assertEqual([p.name for p in pos], ["ola", "grupo"])
        self.assertTrue(all(p.kind != p.VAR_POSITIONAL for p in sig.parameters.values()))
        self.assertFalse(any("cruce" in n.lower() for n in dir(M) if callable(getattr(M, n))))

    def test_dos_variables_posicionales_lanza(self):
        with self.assertRaises(TypeError):
            M.marginal_t(self.ola, "sexo", "formalidad", desenlace=M.DESENLACE)

    def test_lista_de_variables_lanza(self):
        with self.assertRaises(TypeError):
            M.marginal_t(self.ola, ["sexo", "formalidad"], desenlace=M.DESENLACE)
        with self.assertRaises(TypeError):
            M.marginal_t(self.ola, ("formalidad",), desenlace=M.DESENLACE)

    def test_eje_inventado_lanza(self):
        for malo in ("sexo x formalidad", "formalidadxsexo", "_y_ahorra_solo_informal", "EST_DIS", "P3_13"):
            with self.assertRaises(ValueError, msg=malo):
                M.marginal_t(self.ola, malo, desenlace=M.DESENLACE)

    def test_desenlace_no_autorizado_lanza(self):
        with self.assertRaises(ValueError):
            M.marginal_t(self.ola, "sexo", desenlace="informal_cualquiera")

    def test_ola_filtrada_a_una_formalidad_lanza_reserva_rota(self):
        df = self.ola.df[self.ola.df["formalidad"] == "sin seguridad social"]
        rota = dataclasses.replace(self.ola, df=df)
        with self.assertRaises(M.ReservaRota):
            M.marginal_t(rota, "sexo", desenlace=M.DESENLACE)

    def test_ola_reordenada_lanza_reserva_rota(self):
        rota = dataclasses.replace(self.ola, df=self.ola.df.iloc[::-1].reset_index(drop=True))
        with self.assertRaises(M.ReservaRota):
            M.marginal_t(rota, "sexo", desenlace=M.DESENLACE)

    def test_ola_con_columna_alterada_lanza_reserva_rota(self):
        df = self.ola.df.copy()
        i = int(np.flatnonzero(df["sexo"].to_numpy() != M.FUERA)[0])
        df.loc[i, "sexo"] = "2 Mujer" if df.loc[i, "sexo"] == "1 Hombre" else "1 Hombre"
        rota = dataclasses.replace(self.ola, df=df)
        with self.assertRaises(M.ReservaRota):
            M.marginal_t(rota, "sexo", desenlace=M.DESENLACE)

    def test_replicas_de_otra_ola_lanzan(self):
        otra = M._ola_desde_df(fabrica_df(seed=12))
        rep_otra = M.replicas_t(otra, seed=42, n_rep=50, bloque=50)
        with self.assertRaises(M.ReservaRota):
            M.marginal_t(self.ola, "sexo", desenlace=M.DESENLACE, replicas=rep_otra)

    def test_no_se_acepta_cualquier_objeto_como_ola(self):
        with self.assertRaises(TypeError):
            M.marginal_t(self.ola.df, "sexo", desenlace=M.DESENLACE)

    def test_paro_si_t_vacio(self):
        df = fabrica_df(seed=5)
        df["P3_13"] = ""
        with self.assertRaises(M.Paro):
            M._ola_desde_df(df)


class UniversoT(Fixture):
    def test_fuera_de_t_todos_los_ejes_son_fuera(self):
        df = self.ola.df
        fuera_t = df["formalidad"].to_numpy() == M.FUERA
        for e in M.EJES_T:
            self.assertTrue((df[e].to_numpy()[fuera_t] == M.FUERA).all(), e)

    def test_t_es_p3_13_en_1_a_7_por_texto(self):
        crudo = fabrica_df()["P3_13"].to_numpy()
        en_t = self.ola.df["nacional"].to_numpy() == M.NAC_T
        esperado = np.isin(crudo, ["1", "2", "3", "4", "5", "6", "7"])
        np.testing.assert_array_equal(en_t, esperado)
        self.assertEqual(self.ola.meta["filas_t"] + self.ola.meta["fuera_t"], len(crudo))

    def test_marco_de_diseno_entero_no_se_recorta(self):
        self.assertEqual(len(self.ola.df), len(fabrica_df()))
        self.assertEqual(self.rep.n_upm, self.ola.meta["upm"])

    def test_marginal_es_razon_de_totales_ponderados_dentro_de_t(self):
        r = M.marginal_t(self.ola, "sexo", desenlace=M.DESENLACE)
        df = self.ola.df
        for k in ("1 Hombre", "2 Mujer"):
            sel = df["sexo"] == k
            esperado = float((df.loc[sel, "_w"] * df.loc[sel, "_y_ahorra_solo_informal"]).sum()
                             / df.loc[sel, "_w"].sum())
            self.assertAlmostEqual(r["celdas"][k]["p"], esperado, places=12)
        self.assertEqual(sum(c["n"] for c in r["celdas"].values()), self.ola.meta["filas_t"])

    def test_formalidad_en_t_es_la_formalidad_del_arbitro(self):
        df = fabrica_df()
        crudo = M._ejes_del_arbitro()["formalidad"].deriva(df).astype(str).to_numpy()
        np.testing.assert_array_equal(self.ola.df["formalidad"].to_numpy(), crudo)


class PlanDeReplicasEsElDelPiso(Fixture):
    def test_marginales_identicos_a_estimate_del_piso(self):
        ejes = ("sexo", "edad", "formalidad", "cuenta_formal", "nacional")
        ref = _estimate_de_la_ola(self.ola, ejes, n_rep=200)
        for e in ejes:
            r = M.marginal_t(self.ola, e, desenlace=M.DESENLACE, replicas=self.rep)
            for k in M._orden(e):
                c, s = r["celdas"][k], ref[(e, k)]
                self.assertEqual(c["n"], s["N"], (e, k))
                self.assertEqual(c["b_validas"], s["B-VALIDAS"], (e, k))
                self.assertAlmostEqual(c["den_w"], s["DEN-W"], delta=1e-6)
                self.assertAlmostEqual(c["p"], s["P"], delta=1e-12)
                self.assertAlmostEqual(c["ic95"][0], s["IC-LO"], delta=1e-12)
                self.assertAlmostEqual(c["ic95"][1], s["IC-HI"], delta=1e-12)

    def test_replicas_deterministas(self):
        r1 = M.replicas_t(self.ola, seed=42, n_rep=60, bloque=50)
        r2 = M.replicas_t(self.ola, seed=42, n_rep=60, bloque=50)
        np.testing.assert_array_equal(r1.counts, r2.counts)
        r3 = M.replicas_t(self.ola, seed=43, n_rep=60, bloque=50)
        self.assertFalse(np.array_equal(r1.counts, r3.counts))

    def test_c2_vectorizado_coincide_con_la_forma_sellada(self):
        rng = np.random.default_rng(0)
        a, b, n = rng.uniform(0.05, 0.95, 50), rng.uniform(0.05, 0.95, 50), rng.uniform(0.2, 0.8, 50)
        vec = 1.0 / (1.0 + np.exp(-(np.log(a / (1 - a)) + np.log(b / (1 - b)) - np.log(n / (1 - n)))))
        for i in range(50):
            ref = M.piso_log_aditivo(M._marg(a[i], "x"), M._marg(b[i], "x"), M._marg(n[i], "x"))["p"]
            self.assertAlmostEqual(float(vec[i]), ref, places=12)


# ══ capa 4 · el conducto en cada rama terminal (D-22) ═══════════════════════

N_REP_TEST = 200


def _contrato(spec, **cambios):
    c = copy.deepcopy({"parametros": spec["parametros"], "seed": spec["seed"]})
    c["parametros"]["bootstrap_replicas"] = N_REP_TEST
    c["parametros"]["umbral_replicas_validas"] = 190
    c["parametros"].update(cambios)
    return c


def _arbitro_fabricado(inputs, spec, df, ola):
    """El `resultados.json` sellado del árbitro, con sus ids REALES y los
    valores del fixture calculados por `_estimate` del piso y por conteo
    directo de P3_13 (no por el medidor)."""
    doc = json.loads(inputs["IN-ARBITRO-GEN2"]["bytes"].decode("utf-8"))
    res = doc["resultados"]
    lote = yaml.safe_load(inputs["IN-LOTE-CONTRATO"]["bytes"].decode("utf-8"))["parametros"]
    ids = lote["marginales_sellados"]["puntos"]["ids"]["formalidad"]
    ref = _estimate_de_la_ola(ola, ("formalidad",), n_rep=N_REP_TEST)
    for k, pid in ids.items():
        assert pid in res, pid
        base = pid[:-2]
        for suf, clave in (("P", "P"), ("IC-LO", "IC-LO"), ("IC-HI", "IC-HI"),
                           ("N", "N"), ("DEN-W", "DEN-W"), ("B-VALIDAS", "B-VALIDAS")):
            assert f"{base}-{suf}" in res
            res[f"{base}-{suf}"] = ref[("formalidad", k)][clave]
    g = spec["parametros"]["control_arbitro_ids"]
    assert g["filas_universo"] in res and g["fuera_t"] in res
    res[g["filas_universo"]] = len(df)
    res[g["fuera_t"]] = int((~df["P3_13"].isin(list("1234567"))).sum())
    nuevo = dict(inputs)
    nuevo["IN-ARBITRO-GEN2"] = dict(inputs["IN-ARBITRO-GEN2"])
    nuevo["IN-ARBITRO-GEN2"]["bytes"] = json.dumps(doc).encode("utf-8")
    return nuevo


def _corre(df, contrato, arbitro_real=False):
    spec = _spec()
    inputs = _inputs_repo(spec)
    ola = M._ola_desde_df(df)
    if not arbitro_real:
        inputs = _arbitro_fabricado(inputs, spec, df, ola)
    out = {f"{M.P}-G-INPUT-{M._slug(i)}-SHA256": str(inputs[i]["sha256"]) for i in M.INPUTS_PERMITIDOS}
    out[f"{M.P}-G-GUARDIA-AST-VIOLACIONES"] = 0
    out[f"{M.P}-G-GUARDIA-AST"] = "PASA"
    out = M.procedimiento(ola, inputs, contrato, out)
    return spec, out


class ConductoEnCadaRama(unittest.TestCase):
    def _valida(self, spec, out):
        self.assertEqual(corrida0._valida_outputs(spec, out), [])
        for k, v in out.items():
            if isinstance(v, float):
                self.assertTrue(np.isfinite(v), k)

    def test_rama_oro_reproduce_publica_ic(self):
        spec = _spec()
        s, out = _corre(fabrica_df(), _contrato(spec))
        self._valida(s, out)
        self.assertEqual(out[f"{M.P}-G-CONTROL-ARBITRO-VEREDICTO"], "REPRODUCE")
        self.assertEqual(out[f"{M.P}-G-IC-PUBLICADO"], "SI")
        self.assertEqual(out[f"{M.P}-G-N-CELDAS"], 28)
        self.assertGreater(out[f"{M.P}-G-N-CELDAS-CON-IC"], 0)
        self.assertEqual(out[f"{M.P}-G-N-CELDAS-CON-IC"] + out[f"{M.P}-G-N-CELDAS-SIN-IC"], 28)
        for k, v in out.items():
            if k.endswith("-UNIVERSO") and not k.startswith(f"{M.P}-G-"):
                self.assertIn("P3_13 en 1..7", v)
        self.assertLess(out[f"{M.P}-G-C2-VECTORIZADO-VS-REFERENCIA-DELTA-MAX"], 1e-12)

    def test_rama_oro_no_reproduce_deja_ic_en_null(self):
        spec = _spec()
        s, out = _corre(fabrica_df(), _contrato(spec), arbitro_real=True)
        self._valida(s, out)
        self.assertEqual(out[f"{M.P}-G-CONTROL-ARBITRO-VEREDICTO"], "NO-REPRODUCE")
        self.assertEqual(out[f"{M.P}-G-IC-PUBLICADO"], "NO")
        self.assertEqual(out[f"{M.P}-G-N-CELDAS-CON-IC"], 0)
        ic = [v for k, v in out.items()
              if k.endswith(("-IC95INF", "-IC95SUP")) and "-DELTA-" not in k]
        self.assertTrue(all(v is None for v in ic))

    def test_rama_categoria_sin_filas_en_t(self):
        spec = _spec()
        df = fabrica_df(seed=21)
        en_t = df["P3_13"].isin(list("1234567"))
        df.loc[en_t, "TLOC"] = "1"            # nadie de T en «menor de 15 000»
        s, out = _corre(df, _contrato(spec))
        self._valida(s, out)
        self.assertEqual(out[f"{M.P}-G-MARG-T-LOCALIDAD-MENOR-DE-15-000-N"], 0)
        self.assertIsNone(out[f"{M.P}-G-MARG-T-LOCALIDAD-MENOR-DE-15-000-P"])
        self.assertGreater(out[f"{M.P}-G-N-CELDAS-SIN-PUNTO"], 0)

    def test_rama_marginal_degenerado(self):
        spec = _spec()
        df = fabrica_df(seed=22)
        con = df["P5_4_1"].eq("1")
        for c in M._ARB.CUENTAS:
            df.loc[:, c] = "2"
        df.loc[con, "P5_4_1"] = "1"
        df.loc[con, "P5_6_1"] = "1"            # con cuenta => ahorro formal => D9 = 0
        s, out = _corre(df, _contrato(spec))
        self._valida(s, out)
        self.assertEqual(out[f"{M.P}-G-MARG-T-CUENTA-FORMAL-CON-CUENTA-P"], 0.0)
        self.assertTrue(out[f"{M.P}-G-CUENTA-FORMALXFORMALIDAD-DEGENERACION"].startswith("DEGENERADO:"))
        self.assertGreater(out[f"{M.P}-G-N-CELDAS-SIN-PUNTO"], 0)

    def test_rama_replicas_bajo_el_umbral(self):
        spec = _spec()
        s, out = _corre(fabrica_df(), _contrato(spec, umbral_replicas_validas=N_REP_TEST + 1))
        self._valida(s, out)
        self.assertEqual(out[f"{M.P}-G-N-CELDAS-CON-IC"], 0)
        estados = [v for k, v in out.items() if k.endswith("-IC-ESTADO")]
        self.assertTrue(any(v.startswith("IC-NO-CONSTRUIBLE:REPLICAS-VALIDAS-") for v in estados))


# ══ capa 5 · la spec declara exactamente lo que el medidor emite ════════════

class SpecDeclaraElCatalogo(unittest.TestCase):
    def test_resultados_declarados_igualan_al_catalogo(self):
        spec = _spec()
        cat = M.catalogo_resultados(_inputs_repo(spec))
        declarados = {r["id"]: r for r in spec["resultados"]}
        esperados = {r["id"]: r for r in cat}
        self.assertEqual(set(declarados), set(esperados))
        for rid, r in esperados.items():
            self.assertEqual(declarados[rid]["tipo"], r["tipo"], rid)
            self.assertEqual(declarados[rid]["unidad"], r["unidad"], rid)
            self.assertEqual(bool(declarados[rid].get("permite_no_estimable")),
                             bool(r.get("permite_no_estimable")), rid)

    def test_cada_result_de_celda_declara_el_universo_t(self):
        spec = _spec()
        for r in spec["resultados"]:
            if "-G-" not in r["id"] or "-G-MARG-T-" in r["id"]:
                self.assertIn("universo T", r["unidad"], r["id"])

    def test_inputs_declarados_igualan_a_los_permitidos(self):
        spec = _spec()
        self.assertEqual({e["id"] for e in spec["inputs"]}, set(M.INPUTS_PERMITIDOS))
        manif = [e for e in spec["inputs"] if e.get("origen") == "manifiesto"]
        self.assertEqual([e["id"] for e in manif], [M.PAYLOAD_ID])

    def test_sha_de_los_insumos_coinciden_con_el_arbol(self):
        spec = _spec()
        inputs = _inputs_repo(spec)
        for ent in spec["inputs"]:
            if ent.get("origen") == "repo":
                self.assertEqual(ent["sha256"], inputs[ent["id"]]["sha256"], ent["id"])

    def test_ningun_input_es_el_c2_poblacional(self):
        spec = _spec()
        rutas = [e.get("ruta", "") for e in spec["inputs"]]
        self.assertFalse(any("C2-COMPUESTO" in r for r in rutas), rutas)

    def test_el_arbitro_apunta_al_payload_declarado(self):
        self.assertEqual(Path(str(M._ARB.ZIP)).name, M.PAYLOAD_ARCHIVO)
        self.assertEqual(str(M._ARB.TABLA), M.PAYLOAD_TABLA)

    def test_plan_real_cinco_pares_veintiocho_celdas(self):
        plan = M._plan(_inputs_repo(_spec()))
        self.assertEqual(len(plan["pares"]), 5)
        self.assertEqual(sum(len(plan["ejes"][a]) * len(plan["ejes"][b]) for _p, a, b in plan["pares"]), 28)


if __name__ == "__main__":
    unittest.main(verbosity=2)
