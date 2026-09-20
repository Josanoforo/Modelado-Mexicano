#!/usr/bin/env python3
"""Guardia E.6 del medidor de `CALC-C2-COMPUESTO-IC-ENIF2024-0001`.

ACTO `GEN2-C2-COMPUESTO-IC-ENIF2024-1` (19/sep/2026). El encargo pide, verbatim:
«test que recorre el AST del medidor y falla si hay cualquier agrupación por
más de una variable, cualquier crosstab/pivot, o cualquier lectura de payload
fuera de los payloads de ENIF 2024 (TMODULO)». El defecto que cubre ya
ocurrió: NC-0328, una reserva quemada por un script de scratch.

Dos capas, ninguna de prosa:

  1. `auditoria_ast()` vive DENTRO del medidor y `medir()` la corre sobre su
     propio archivo antes de abrir el zip. Aquí se corre igual (debe dar 0)
     y, además, se le da a comer una MUTACIÓN por regla -- un `groupby` de
     dos variables, un `crosstab`, `.df` fuera del núcleo, dos máscaras
     combinadas, un payload de otro instrumento -- y debe reportarla. Un
     negativo sin control positivo no es un negativo
     (`forense/hallazgos.md`, regla de la casa).
  2. La guardia en tiempo de ejecución, sobre datos FABRICADOS con la forma
     que `tools/medidor_ahorro_enif24.py::carga()` devuelve (cero microdato,
     cero cifras del modelo): dos variables lanzan `TypeError`, un eje
     inventado `ValueError`, una ola filtrada `ReservaRota`, réplicas de otra
     ola `ReservaRota`; el marginal es razón de totales ponderados; las
     réplicas son deterministas por seed; el C2 vectorizado coincide con
     `piso_log_aditivo`.

Además coteja que `spec.yaml` declare EXACTAMENTE los RESULT que el medidor
enumera (`catalogo_resultados`, leyendo el dictamen y el yaml del árbitro del
árbol) -- una spec que declara de más o de menos es un `run` que no sella.

Correr:  python3 tests/test_c2_ic_enif2024_guardia.py
"""
from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import random
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data" / "corrida0" / "CALC-C2-COMPUESTO-IC-ENIF2024-0001"
MEDIDOR = CALC / "medidor.py"


def _carga_medidor():
    spec = importlib.util.spec_from_file_location("medidor_c2_ic_enif2024", MEDIDOR)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


M = _carga_medidor()


# ══ fixture fabricado: la forma que `carga()` del árbitro devuelve ═══════════

def fabrica_df(n: int = 900, seed: int = 11) -> pd.DataFrame:
    rng = random.Random(seed)
    filas = []
    for i in range(n):
        est = f"{1 + i % 6:03d}"
        upm = f"{1 + (i // 3) % 40:04d}"
        fila = {
            "SEXO": rng.choice(["1", "2"]),
            "EDAD_V": str(rng.randint(18, 99)),
            "NIV": rng.choice(["00", "01", "02", "03", "04", "05", "06", "07",
                               "08", "09", "10", "11", "99"]),
            "TLOC": rng.choice(["1", "2", "3", "4"]),
            "P3_13": rng.choice(["1", "2", "3", "4", "5", "6", "7", ""]),
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


class Fixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ola = M._ola_desde_df(fabrica_df())
        cls.rep = M.replicas_enif(cls.ola, seed=42, n_rep=200)


# ══ capa 1 · el AST del medidor, con un control positivo por regla ══════════

FUENTE = MEDIDOR.read_text(encoding="utf-8")


def _muta(anadido: str, ancla: str = "def medir(inputs: dict, contrato: dict) -> dict:\n") -> str:
    """Inserta `anadido` como primera(s) línea(s) del cuerpo de `medir`."""
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
        self._espera(_muta('x = pd.DataFrame().groupby(["sexo", "edad"]).size()'), "R2")

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

    def test_R4_dos_comparaciones_por_and(self):
        self._espera(_muta("x = [1 for i in range(3) if i > 0 and i < 2]"), "R4")

    def test_R4_producto_de_dos_mascaras(self):
        self._espera(_muta("x = (np.arange(3) > 0) * (np.arange(3) < 2)"), "R4")

    def test_R5_ola_construida_fuera_de_su_sitio(self):
        self._espera(_muta("x = OlaEnif(df=pd.DataFrame(), huella='', meta={})"), "R5")

    def test_R5_carga_del_arbitro_fuera_de_su_sitio(self):
        self._espera(_muta("x = _ARB.carga()"), "R5")

    def test_R5_importa_modulo_no_autorizado(self):
        self._espera(_muta('x = _importa("otro", RAIZ / "tools" / "marcador_segmento.py")'), "R5")

    def test_R6_marginal_con_lista(self):
        self._espera(_muta('x = marginal_enif(None, ["sexo", "edad"], desenlace="informal_cualquiera")'), "R6")

    def test_R6_marginal_con_tres_posicionales(self):
        self._espera(_muta('x = marginal_enif(None, "sexo", "edad")'), "R6")

    def test_R7_funcion_de_cruce(self):
        self._espera(FUENTE + "\n\ndef cruce_enif(ola, a, b):\n    return None\n", "R7")

    def test_R8_payload_de_otro_instrumento(self):
        self._espera(_muta('x = inputs["envipe2025_csv"]'), "R8")

    def test_R8_archivo_no_autorizado(self):
        self._espera(_muta('x = "conjunto_de_datos_tmodulo_enif2024.csv"'), "R8")

    def test_R8_input_no_declarado(self):
        self._espera(_muta('x = inputs["IN-OTRO"]'), "R8")


# ══ capa 2 · la guardia en tiempo de ejecución, sobre datos fabricados ═══════

class GuardiaUnaVariable(Fixture):
    def test_firma_un_solo_grupo_posicional(self):
        import inspect
        sig = inspect.signature(M.marginal_enif)
        pos = [p for p in sig.parameters.values()
               if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
        self.assertEqual([p.name for p in pos], ["ola", "grupo"])
        self.assertTrue(all(p.kind != p.VAR_POSITIONAL for p in sig.parameters.values()))
        self.assertFalse(hasattr(M, "cruce"))
        self.assertFalse(any("cruce" in n.lower() for n in dir(M) if callable(getattr(M, n))))

    def test_dos_variables_posicionales_lanza(self):
        with self.assertRaises(TypeError):
            M.marginal_enif(self.ola, "sexo", "edad", desenlace="informal_cualquiera")

    def test_lista_de_variables_lanza(self):
        with self.assertRaises(TypeError):
            M.marginal_enif(self.ola, ["sexo", "edad"], desenlace="informal_cualquiera")
        with self.assertRaises(TypeError):
            M.marginal_enif(self.ola, ("sexo",), desenlace="informal_cualquiera")

    def test_eje_inventado_o_no_admitido_lanza(self):
        for malo in ("sexo x edad", "sexoxedad", "formalidad", "_y_informal_cualquiera", "EST_DIS"):
            with self.assertRaises(ValueError, msg=malo):
                M.marginal_enif(self.ola, malo, desenlace="informal_cualquiera")

    def test_desenlace_inventado_lanza(self):
        with self.assertRaises(ValueError):
            M.marginal_enif(self.ola, "sexo", desenlace="sexo")

    def test_ola_filtrada_lanza_reserva_rota(self):
        df = self.ola.df[self.ola.df["localidad"] == "menor de 15 000"]
        rota = dataclasses.replace(self.ola, df=df)
        with self.assertRaises(M.ReservaRota):
            M.marginal_enif(rota, "escolaridad", desenlace="informal_cualquiera")

    def test_ola_reordenada_lanza_reserva_rota(self):
        df = self.ola.df.iloc[::-1].reset_index(drop=True)
        rota = dataclasses.replace(self.ola, df=df)
        with self.assertRaises(M.ReservaRota):
            M.marginal_enif(rota, "sexo", desenlace="ahorra_solo_informal")

    def test_ola_con_columna_alterada_lanza_reserva_rota(self):
        df = self.ola.df.copy()
        df.loc[0, "sexo"] = "2 Mujer" if df.loc[0, "sexo"] == "1 Hombre" else "1 Hombre"
        rota = dataclasses.replace(self.ola, df=df)
        with self.assertRaises(M.ReservaRota):
            M.marginal_enif(rota, "sexo", desenlace="ahorra_solo_informal")

    def test_replicas_de_otra_ola_lanzan(self):
        otra = M._ola_desde_df(fabrica_df(seed=12))
        rep_otra = M.replicas_enif(otra, seed=42, n_rep=50)
        with self.assertRaises(M.ReservaRota):
            M.marginal_enif(self.ola, "sexo", desenlace="informal_cualquiera", replicas=rep_otra)

    def test_no_se_acepta_cualquier_objeto_como_ola(self):
        with self.assertRaises(TypeError):
            M.marginal_enif(self.ola.df, "sexo", desenlace="informal_cualquiera")


class LoQueSiHace(Fixture):
    def test_marginal_es_razon_de_totales_ponderados(self):
        r = M.marginal_enif(self.ola, "sexo", desenlace="informal_cualquiera")
        df = self.ola.df
        for k in ("1 Hombre", "2 Mujer"):
            sel = df["sexo"] == k
            esperado = float((df.loc[sel, "_w"] * df.loc[sel, "_y_informal_cualquiera"]).sum()
                             / df.loc[sel, "_w"].sum())
            self.assertAlmostEqual(r["celdas"][k]["p"], esperado, places=12)
            self.assertEqual(r["celdas"][k]["n"], int(sel.sum()))
        self.assertEqual(sum(c["n"] for c in r["celdas"].values()) + r["n_fuera"], len(df))

    def test_orden_y_rotulos_son_los_del_arbitro(self):
        self.assertEqual(list(M._orden("edad")), list(M._ARB.ORD_EDAD))
        self.assertEqual(list(M._orden("escolaridad")), list(M._ARB.ORD_ESC))
        self.assertEqual(list(M._orden("sexo")), list(M._ARB.ORD_SEXO))
        self.assertEqual(M._orden("localidad"), ["menor de 15 000", "15 000 y mas"])
        self.assertEqual(M._orden("cuenta_formal"), ["sin cuenta", "con cuenta"])
        self.assertEqual(M._orden("nacional"), ["NAC"])

    def test_nacional_es_el_universo_entero(self):
        r = M.marginal_enif(self.ola, "nacional", desenlace="ahorra_solo_informal")
        self.assertEqual(r["celdas"]["NAC"]["n"], len(self.ola.df))
        self.assertEqual(r["n_fuera"], 0)

    def test_desenlaces_son_los_del_arbitro(self):
        df = fabrica_df(seed=3)
        ola = M._ola_desde_df(df)
        des = M._ARB.desenlaces(df)
        np.testing.assert_array_equal(
            ola.df["_y_ahorra_solo_informal"].to_numpy(),
            des["ahorra_solo_informal (PRINCIPAL)"].to_numpy())
        np.testing.assert_array_equal(
            ola.df["_y_informal_cualquiera"].to_numpy(),
            des["informal_cualquiera (SECUNDARIO)"].to_numpy())

    def test_replicas_deterministas_y_compartidas(self):
        r1 = M.replicas_enif(self.ola, seed=42, n_rep=60)
        r2 = M.replicas_enif(self.ola, seed=42, n_rep=60)
        np.testing.assert_array_equal(r1.counts, r2.counts)
        r3 = M.replicas_enif(self.ola, seed=43, n_rep=60)
        self.assertFalse(np.array_equal(r1.counts, r3.counts))
        # cada réplica remuestrea n_h UPM por estrato: la suma de counts por
        # estrato es n_h
        est = self.ola.df["EST_DIS"].to_numpy()
        upm_est = {}
        for pos, e in zip(r1.pos_fila, est):
            upm_est[int(pos)] = e
        for e in sorted(set(est)):
            cols = [u for u, ee in upm_est.items() if ee == e]
            self.assertTrue((r1.counts[:, cols].sum(axis=1) == len(cols)).all())

    def test_replicas_de_un_marginal_promedian_cerca_del_punto(self):
        r = M.marginal_enif(self.ola, "localidad", desenlace="informal_cualquiera",
                            replicas=self.rep)
        for k, c in r["celdas"].items():
            self.assertEqual(len(c["replicas"]), self.rep.n_rep)
            self.assertTrue(np.isfinite(c["replicas"]).all())
            self.assertLess(abs(float(np.mean(c["replicas"])) - c["p"]), 0.05, k)

    def test_c2_vectorizado_coincide_con_la_forma_sellada(self):
        rng = np.random.default_rng(0)
        a, b, n = rng.uniform(0.05, 0.95, 50), rng.uniform(0.05, 0.95, 50), rng.uniform(0.2, 0.8, 50)
        lc2 = np.log(a / (1 - a)) + np.log(b / (1 - b)) - np.log(n / (1 - n))
        vec = 1.0 / (1.0 + np.exp(-lc2))
        for i in range(50):
            ref = M.piso_log_aditivo(M._marg(a[i], "x"), M._marg(b[i], "x"), M._marg(n[i], "x"))["p"]
            self.assertAlmostEqual(float(vec[i]), ref, places=12)

    def test_paro_si_faltan_estratos(self):
        df = fabrica_df(seed=5)
        df.loc[0, "EST_DIS"] = ""
        with self.assertRaises(M.Paro):
            M._ola_desde_df(df)


# ══ la spec declara exactamente lo que el medidor emite ═════════════════════

class SpecDeclaraElCatalogo(unittest.TestCase):
    def _inputs_repo(self):
        spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
        inputs = {}
        for ent in spec["inputs"]:
            d = dict(ent)
            if ent.get("origen") == "repo":
                ruta = RAIZ / ent["ruta"]
                d["bytes"] = ruta.read_bytes()
                d["sha256"] = hashlib.sha256(d["bytes"]).hexdigest()
            inputs[ent["id"]] = d
        return spec, inputs

    def test_resultados_declarados_igualan_al_catalogo(self):
        spec, inputs = self._inputs_repo()
        cat = M.catalogo_resultados(inputs)
        declarados = {r["id"]: r for r in spec["resultados"]}
        esperados = {r["id"]: r for r in cat}
        self.assertEqual(set(declarados), set(esperados),
                         f"faltan={sorted(set(esperados) - set(declarados))[:5]} "
                         f"sobran={sorted(set(declarados) - set(esperados))[:5]}")
        for rid, r in esperados.items():
            self.assertEqual(declarados[rid]["tipo"], r["tipo"], rid)
            self.assertEqual(bool(declarados[rid].get("permite_no_estimable")),
                             bool(r.get("permite_no_estimable")), rid)

    def test_inputs_declarados_igualan_a_los_permitidos(self):
        spec, _ = self._inputs_repo()
        self.assertEqual({e["id"] for e in spec["inputs"]}, set(M.INPUTS_PERMITIDOS))
        manif = [e for e in spec["inputs"] if e.get("origen") == "manifiesto"]
        self.assertEqual([e["id"] for e in manif], [M.PAYLOAD_ID])

    def test_sha_de_los_insumos_de_codigo_coinciden_con_el_arbol(self):
        spec, inputs = self._inputs_repo()
        for ent in spec["inputs"]:
            if ent.get("origen") == "repo":
                self.assertEqual(ent["sha256"], inputs[ent["id"]]["sha256"], ent["id"])

    def test_el_arbitro_apunta_al_payload_declarado(self):
        self.assertEqual(Path(str(M._ARB.ZIP)).name, M.PAYLOAD_ARCHIVO)
        self.assertEqual(str(M._ARB.TABLA), M.PAYLOAD_TABLA)

    def test_el_modulo_guardado_no_admite_ningun_eje_de_enif(self):
        for e in M.EJES_ENIF[:-1]:
            with self.assertRaises(ValueError, msg=e):
                M._MR.marginal(None, e)
        self.assertNotIn("sexo", M._MR.EJES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
