#!/usr/bin/env python3
"""Guardia de UNA variable de agrupación -- `tools/celda_d/marginales_reproduccion.py`.

ACTO `GEN2-CELDA-D-PILOTO-2` v1.1 (17/sep/2026), Firma 2 de mesa: «El control
de reproducción se congela como código en COMMIT-1 con guardia de una sola
variable de agrupación». Este archivo es la prueba de que la guardia es
mecánica y no prosa: llamar a `marginal` con dos variables LANZA.

Fixtures FABRICADOS (zips con la forma exacta que la spec declara: miembro
`<tabla>_envipe<anio>/conjunto_de_datos/conjunto_de_datos_<tabla>_envipe<anio>.csv`,
BOM, `\\r` como fin de línea). Cero microdato real, cero cifras del modelo.
E.5-compatible: no toca el corpus.

Correr:  python3 tests/test_marginales_una_variable.py
"""
from __future__ import annotations

import dataclasses
import importlib.util
import inspect
import os
import random
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "marginales_reproduccion", RAIZ / "tools" / "celda_d" / "marginales_reproduccion.py")
mr = importlib.util.module_from_spec(_spec)
sys.modules["marginales_reproduccion"] = mr
_spec.loader.exec_module(mr)


def _csv(filas: list[list[str]], cabecera: list[str]) -> bytes:
    lineas = [",".join(f'"{c}"' for c in cabecera)]
    lineas += [",".join(f'"{c}"' for c in f) for f in filas]
    return ("\r".join(lineas) + "\r").encode("utf-8-sig")   # BOM + CR solo


def fabrica_zip(ruta: Path, anio: int, n_delitos: int = 600, seed: int = 7,
                *, sin_persona: int = 0, fac_del_cero: bool = False) -> None:
    rng = random.Random(seed)
    personas = [f"{i:07d}.01.01.{1 + i % 5:02d}" for i in range(1, 301)]
    sdem = []
    for p in personas:
        niv = rng.choice(["00", "01", "02", "03", "04", "05", "06", "07",
                          "08", "09", "99", ""])
        sdem.append([p, niv, "1", "030", "0000012"])
    tmod = []
    for i in range(n_delitos):
        pid = personas[rng.randrange(len(personas))]
        if i < sin_persona:
            pid = f"9{i:06d}.01.01.01"          # huérfano deliberado
        bp1_20 = rng.choice(["1", "2", "2", "2", "b"])
        bp1_23 = rng.choice(["01", "02", "03", "04", "05", "06", "07", "08",
                             "09", "99"]) if bp1_20 == "2" else "b"
        est = f"{1 + rng.randrange(6):03d}"
        upm = f"{1 + rng.randrange(4):07d}"
        fac = "0" if (fac_del_cero and i == 5) else str(rng.randrange(1, 900))
        # GEN2-GUARDIAN-ENVIPE-EJES-IC-1: SEXO/EDAD crudos en tmod_vic, con
        # fuera de banda deliberado (menor, 97+, 99 = no especificado, blanco).
        sexo = rng.choice(["1", "2", "2", "1", "9"])
        edad = rng.choice([str(rng.randrange(18, 97)), str(rng.randrange(18, 97)),
                           str(rng.randrange(18, 97)), "15", "97", "99", ""])
        tmod.append([f"{i:06d}", pid, bp1_20, bp1_23, fac,
                     est, upm, rng.choice(["U", "C", "R"]), "01", sexo, edad])
    with zipfile.ZipFile(ruta, "w") as zf:
        zf.writestr(f"tmod_vic_envipe{anio}/conjunto_de_datos/"
                    f"conjunto_de_datos_tmod_vic_envipe{anio}.csv",
                    _csv(tmod, ["ID_DEL", "ID_PER", "BP1_20", "BP1_23", "FAC_DEL",
                                "EST_DIS", "UPM_DIS", "DOMINIO", "BPCOD",
                                "SEXO", "EDAD"]))
        zf.writestr(f"tsdem_envipe{anio}/conjunto_de_datos/"
                    f"conjunto_de_datos_tsdem_envipe{anio}.csv",
                    _csv(sdem, ["ID_PER", "NIV", "SEXO", "EST_DIS", "UPM_DIS"]))


class Fixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.zip = Path(cls.tmp.name) / "envipe2099_csv.zip"
        fabrica_zip(cls.zip, 2099, sin_persona=3)
        cls.ola = mr.carga_ola(cls.zip, 2099, reservada=True)
        cls.libre = mr.carga_ola(cls.zip, 2099, reservada=False)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()


class GuardiaUnaVariable(Fixture):
    """Lo que el encargo exige, verbatim: «un test que asierta que llamarla
    con dos lanza»."""

    def test_firma_un_solo_grupo_posicional(self):
        sig = inspect.signature(mr.marginal)
        params = list(sig.parameters.values())
        posicionales = [p for p in params
                        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
        self.assertEqual([p.name for p in posicionales], ["ola", "grupo"])
        self.assertEqual(sig.parameters["grupo"].annotation, "str")
        self.assertFalse(any(p.kind == p.VAR_POSITIONAL for p in params),
                         "no hay *grupos")

    def test_dos_variables_posicionales_lanza(self):
        with self.assertRaises(TypeError):
            mr.marginal(self.ola, "escolaridad_proxy", "dominio_urbano_rural")

    def test_lista_de_variables_lanza(self):
        with self.assertRaises(TypeError):
            mr.marginal(self.ola, ["escolaridad_proxy", "dominio_urbano_rural"])
        with self.assertRaises(TypeError):
            mr.marginal(self.ola, ("escolaridad_proxy", "dominio_urbano_rural"))

    def test_eje_inventado_lanza(self):
        for malo in ("escolaridad_proxy x dominio_urbano_rural", "celda",
                     "escolaridad_proxy,dominio_urbano_rural", "DOMINIO"):
            with self.assertRaises(ValueError, msg=malo):
                mr.marginal(self.ola, malo)

    def test_ola_filtrada_lanza_reserva_rota(self):
        mask = self.ola.df["dominio_urbano_rural"].to_numpy() == "Rural"
        filtrada = dataclasses.replace(self.ola, df=self.ola.df.loc[mask])
        with self.assertRaises(mr.ReservaRota):
            mr.marginal(filtrada, "escolaridad_proxy")

    def test_ola_reordenada_lanza_reserva_rota(self):
        alterada = dataclasses.replace(
            self.ola, df=self.ola.df.iloc[::-1].reset_index(drop=True))
        with self.assertRaises(mr.ReservaRota):
            mr.marginal(alterada, "nacional")

    def test_cruce_sobre_ola_reservada_lanza(self):
        with self.assertRaises(mr.ReservaRota):
            mr.cruce(self.ola, "escolaridad_proxy", "dominio_urbano_rural")

    def test_cruce_sobre_ola_libre_da_12_celdas(self):
        c = mr.cruce(self.libre, "escolaridad_proxy", "dominio_urbano_rural")
        self.assertEqual(len(c["celdas"]), 12)
        self.assertEqual(sum(v["n"] for v in c["celdas"].values()),
                         c["n_universo"] - c["n_fuera"])

    def test_replicas_de_otra_ola_lanzan(self):
        rep = mr.replicas_compartidas(self.libre, seed=42, n_rep=50)
        otra = mr.carga_ola(self.zip, 2099, reservada=True)
        # misma huella (mismos bytes): las réplicas SÍ valen para ella
        mr.marginal(otra, "nacional", replicas=rep)
        # réplicas con huella ajena: no
        ajena = dataclasses.replace(rep, huella_ola="0" * 64)
        with self.assertRaises(mr.ReservaRota):
            mr.marginal(otra, "nacional", replicas=ajena)


class LoQueSiHace(Fixture):
    def test_universo_y_conteos(self):
        m = self.ola.meta
        self.assertEqual(m["filas_archivo"],
                         m["filas_universo"] + m["filas_bp1_20_fuera"])
        self.assertEqual(m["delitos_sin_persona"], 3)
        self.assertGreaterEqual(m["escolaridad_fuera"], 3)   # huérfanos + 99/blanco
        self.assertEqual(m["dominio_fuera"], 0)
        self.assertTrue(set(self.ola.df["BP1_20"]) <= {"1", "2"})

    def test_marginal_es_razon_de_totales_ponderados(self):
        m = mr.marginal(self.ola, "dominio_urbano_rural")
        df = self.ola.df
        for k, c in m["celdas"].items():
            sel = df["dominio_urbano_rural"] == k
            esperado = float((df.loc[sel, "_w"] * df.loc[sel, "_y"]).sum()
                             / df.loc[sel, "_w"].sum())
            self.assertAlmostEqual(c["p"], esperado, places=12)
            self.assertLessEqual(c["ic95"][0], c["p"])
            self.assertGreaterEqual(c["ic95"][1], c["p"])
        self.assertEqual(m["cobertura"], 1.0)

    def test_escolaridad_usa_la_construccion_del_arbitro(self):
        self.assertIs(mr.ESC_2DIG, sys.modules["ejes_maestra35_l1"].ESC_2DIG)
        m = mr.marginal(self.ola, "escolaridad_proxy")
        self.assertEqual(list(m["celdas"]), ["hasta primaria", "secundaria",
                                             "media superior", "superior"])
        self.assertLess(m["cobertura"], 1.0)
        self.assertEqual(m["n_fuera"], self.ola.meta["escolaridad_fuera"])

    def test_replicas_deterministas_y_compartidas(self):
        r1 = mr.replicas_compartidas(self.libre, seed=42, n_rep=200)
        r2 = mr.replicas_compartidas(self.libre, seed=42, n_rep=200)
        self.assertTrue(np.array_equal(r1.counts, r2.counts))
        m = mr.marginal(self.libre, "nacional", replicas=r1)
        reps = m["celdas"]["NAC"]["replicas"]
        self.assertEqual(reps.shape, (200,))
        self.assertTrue(np.all(np.isfinite(reps)))
        # la réplica 0 del nacional es la suma de las réplicas 0 de los
        # dominios, ponderadas: mismo remuestreo, no remuestreos distintos
        md = mr.marginal(self.libre, "dominio_urbano_rural", replicas=r1)
        df = self.libre.df
        c0 = r1.counts[0].astype(float)
        num = den = 0.0
        for k, c in md["celdas"].items():
            mask = (df["dominio_urbano_rural"] == k).to_numpy()
            w = df["_w"].to_numpy() * mask
            W = np.bincount(r1.pos_fila, weights=w, minlength=r1.n_upm)
            den_k = float(c0 @ W)
            num += c["replicas"][0] * den_k
            den += den_k
        self.assertAlmostEqual(num / den, reps[0], places=10)

    def test_cotejo_reproduce_y_no_reproduce(self):
        m = mr.marginal(self.ola, "dominio_urbano_rural")
        sell = {k: {"p": c["p"], "ic95": c["ic95"], "n": c["n"]}
                for k, c in m["celdas"].items()}
        self.assertEqual(mr.cotejo(m, sell, 1e-6, 1e-4)["veredicto"], "REPRODUCE")
        sell["Rural"]["p"] += 0.01
        r = mr.cotejo(m, sell, 1e-6, 1e-4)
        self.assertEqual(r["veredicto"], "NO-REPRODUCE")
        self.assertAlmostEqual(r["filas"]["Rural"]["delta_p"], -0.01, places=9)

    def test_paro_si_fac_del_no_positivo(self):
        with tempfile.TemporaryDirectory() as d:
            z = Path(d) / "envipe2098_csv.zip"
            fabrica_zip(z, 2098, fac_del_cero=True)
            with self.assertRaises(mr.Paro):
                mr.carga_ola(z, 2098)


class ExtensionSexoEdad(Fixture):
    """ACTO `GEN2-GUARDIAN-ENVIPE-EJES-IC-1` (20/sep/2026), firma «2 si
    extendemos»: casos NUEVOS; los de arriba no se editan."""

    def test_ejes_nuevos_al_final_y_los_viejos_intactos(self):
        self.assertEqual(mr.EJES[:3], ("escolaridad_proxy", "dominio_urbano_rural",
                                       "nacional"))
        self.assertEqual(mr.EJES[3:], ("sexo", "edad"))

    def test_marginal_sexo_funciona_con_la_construccion_del_arbitro(self):
        l1 = sys.modules["ejes_maestra35_l1"]
        self.assertIs(mr.SEXO, l1.SEXO)
        self.assertIs(mr.tramos_edad, l1.tramos_edad)
        m = mr.marginal(self.ola, "sexo")
        self.assertEqual(list(m["celdas"]), ["1 Hombre", "2 Mujer"])
        self.assertEqual(m["n_fuera"], self.ola.meta["sexo_fuera"])
        self.assertGreater(m["n_fuera"], 0)                 # el "9" del fixture
        self.assertEqual(sum(c["n"] for c in m["celdas"].values()),
                         m["n_universo"] - m["n_fuera"])

    def test_marginal_edad_tramos_y_fuera_de_banda(self):
        m = mr.marginal(self.ola, "edad")
        self.assertEqual(list(m["celdas"]), ["18-29", "30-44", "45-59", "60+"])
        self.assertEqual(m["n_fuera"], self.ola.meta["edad_fuera"])
        df = self.ola.df
        e = df["EDAD"].apply(lambda v: int(v) if v.isdigit() else -1)
        self.assertEqual(m["n_fuera"], int(((e < 18) | (e > 96)).sum()))
        self.assertGreater(m["n_fuera"], 0)                 # 15 / 97 / 99 / ""
        for k, c in m["celdas"].items():
            sel = df["edad"] == k
            esperado = float((df.loc[sel, "_w"] * df.loc[sel, "_y"]).sum()
                             / df.loc[sel, "_w"].sum())
            self.assertAlmostEqual(c["p"], esperado, places=12)

    def test_sexo_y_edad_tambien_son_una_sola_variable(self):
        with self.assertRaises(TypeError):
            mr.marginal(self.ola, "sexo", "edad")
        with self.assertRaises(TypeError):
            mr.marginal(self.ola, ["sexo", "edad"])
        with self.assertRaises(TypeError):
            mr.marginal(self.ola, "edad", "dominio_urbano_rural")

    def test_cruce_edad_dominio_vetado_por_nombre_en_ola_libre(self):
        self.assertFalse(self.libre.reservada)
        ola2025 = dataclasses.replace(self.libre, anio=2025)
        for a, b in (("edad", "dominio_urbano_rural"), ("dominio_urbano_rural", "edad")):
            with self.assertRaises(mr.ReservaRota) as cm:
                mr.cruce(ola2025, a, b)
            self.assertIn("NC-0328", str(cm.exception))
        # el veto es por nombre y por ola: en otra ola el mismo par no lo dispara
        c = mr.cruce(self.libre, "edad", "dominio_urbano_rural")   # anio 2099
        self.assertEqual(len(c["celdas"]), 12)

    def test_cruce_de_los_pares_del_dictamen_sigue_prohibido_en_reservada(self):
        for a, b in (("dominio_urbano_rural", "sexo"), ("edad", "escolaridad_proxy"),
                     ("edad", "sexo"), ("escolaridad_proxy", "sexo")):
            with self.assertRaises(mr.ReservaRota):
                mr.cruce(self.ola, a, b)

    def test_replicas_compartidas_valen_para_los_ejes_nuevos(self):
        rep = mr.replicas_compartidas(self.ola, seed=42, n_rep=100)
        ms = mr.marginal(self.ola, "sexo", replicas=rep)
        me = mr.marginal(self.ola, "edad", replicas=rep)
        for m in (ms, me):
            for c in m["celdas"].values():
                self.assertEqual(c["replicas"].shape, (100,))


if __name__ == "__main__":
    unittest.main(verbosity=2)
