#!/usr/bin/env python3
"""El consumidor lee la fila `M05` re-escrita del catálogo SIN CAMBIAR CÓDIGO,
y el orden de los tres commits del piloto se lee del historial, no de la prosa.

`ACTO GEN2-CELDA-D-PILOTO-2` v1.1 (relanzamiento), `COMMIT-3`. Lo que el
encargo pide: *«fila M05 del catálogo; test de lectura por el consumidor»*.

A diferencia del primer piloto (que AÑADIÓ `M23`, `HOLDOUT`), aquí la fila ya
existía: `M05` (`tramite.evasion_norma`, `AJUSTE`, `NO-VERIFICADO`, con
`universo_candidatos` e `instrumentos_candidatos` `POR DECLARAR`). El acto la
pasa a `DERIVADO-Y-SELLADO-GEN2` y le declara universo, instrumentos, cómputo,
reserva y `spec_ref`. **El rol no cambia** (append-only de roles) y **ni
`milpa/src/momentos.py` ni `tools/corrida0.py` se tocaron**.

**Lo que este test NO hace, y es deliberado:** no lee el VALOR del momento.
`M05` es `AJUSTE` y `valor_de()` sigue lanzando `NotImplementedError` en E0
(«E0 no mira el disco»): que exista un `CALC` sellado con la cifra no la
convierte en insumo del motor. Adoptar es de mesa.

Correr:  python3 tests/test_celda_d_piloto2_consumidor.py
"""
from __future__ import annotations

import csv
import importlib.util
import io
import os
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from milpa.src import momentos as MM  # noqa: E402

CATALOGO = "milpa/catalogo-momentos-v0_1.tsv"
ID_FILA = "M05"
REGLA_CONSUMIDORA = "tramite.evasion_norma"
TRAMITE = "milpa/tramite.yaml"
CELDA_D = "data/curacion-registro/celdas-d/TRA.evade_norma.envipe2025.escolaridad_x_dominio.yaml"
CALC_EMISIONES = "data/corrida0/CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001"
CALC_ARBITRO = "data/corrida0/CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001"
# El catálogo tal como estaba ANTES de que este acto tocara la fila: el
# COMMIT-2 del propio acto (emisiones selladas), un SHA fijo de la historia.
SHA_ANTES = "cdd78f9"
COLUMNAS_QUE_ESTE_ACTO_DECLARA = {
    "universo_candidatos", "universo_instrumento", "instrumentos_candidatos",
    "computo_pretendido", "estatus_disponibilidad", "fuente_regla", "reserva",
    "spec_ref",
}


def _git(*args):
    return subprocess.run(["git", "-C", str(RAIZ), *args],
                          capture_output=True, text=True, check=False)


def _historia_truncada():
    """`True` si el clon es shallow -- NC-0273: en un clon truncado,
    `git log --diff-filter=A` puede devolver el MISMO borde de injerto
    (`.git/shallow`) para dos archivos distintos, dando un falso `FAIL` de
    "nacieron en el mismo commit" que no es un defecto de contenido. El
    checkout de `.github/workflows/verify.yml` usa `--depth=1` a propósito
    (ver su cabecera), así que CI SIEMPRE es shallow -- esto no es un caso
    raro a cubrir "por si acaso".
    """
    r = _git("rev-parse", "--is-shallow-repository")
    return r.returncode == 0 and r.stdout.strip() == "true"


def _catalogo():
    return MM.cargar_catalogo()


def _m05(cat):
    return next(m for m in cat.momentos if m.id_momento == ID_FILA)


def _filas_crudas(texto):
    return list(csv.DictReader(io.StringIO(texto), delimiter="\t"))


class ElConsumidorLaLeeSinCambiarCodigo(unittest.TestCase):

    def test_el_catalogo_carga_con_el_lector_de_siempre(self):
        cat = _catalogo()
        self.assertEqual(len(cat), 23)
        self.assertIn(ID_FILA, [m.id_momento for m in cat.momentos])

    def test_la_fila_paso_a_derivada_y_conserva_su_rol(self):
        m = _m05(_catalogo())
        self.assertEqual(m.rol_calibracion, "AJUSTE")
        self.assertEqual(m.estatus_disponibilidad, "DERIVADO-Y-SELLADO-GEN2")
        self.assertEqual(m.objeto_modelo, REGLA_CONSUMIDORA)
        filas = {f["id_momento"]: f for f in _filas_crudas(
            (RAIZ / CATALOGO).read_text(encoding="utf-8"))}
        fila = filas[ID_FILA]
        self.assertNotIn("POR DECLARAR", fila["universo_candidatos"])
        self.assertNotIn("POR DECLARAR", fila["instrumentos_candidatos"])
        rutas = [x.strip() for x in fila["spec_ref"].split("|")]
        self.assertEqual(len(rutas), 3)
        for ruta in rutas:
            self.assertTrue((RAIZ / ruta).exists(), f"spec_ref apunta a {ruta}, que no existe")

    def test_las_otras_22_filas_no_cambiaron_un_byte(self):
        r = _git("show", f"{SHA_ANTES}:{CATALOGO}")
        if r.returncode != 0:
            self.skipTest(f"sin {SHA_ANTES} en esta historia")
        antes = {f["id_momento"]: f for f in _filas_crudas(r.stdout)}
        ahora = {f["id_momento"]: f
                 for f in _filas_crudas((RAIZ / CATALOGO).read_text(encoding="utf-8"))}
        self.assertEqual(set(antes), set(ahora), "este acto no añade ni quita filas")
        for mid in antes:
            for col, v in antes[mid].items():
                if mid == ID_FILA and col in COLUMNAS_QUE_ESTE_ACTO_DECLARA:
                    continue
                self.assertEqual(ahora[mid][col], v, f"{mid}.{col} cambió y no debía")
        # y en M05 las columnas de identidad siguen intactas
        for col in ("id_momento", "objeto_modelo", "necesidad_id", "rol_calibracion", "nivel"):
            self.assertEqual(ahora[ID_FILA][col], antes[ID_FILA][col])

    def test_la_regla_consumidora_existe_en_el_motor(self):
        m = _m05(_catalogo())
        self.assertIn(REGLA_CONSUMIDORA, m.fuente_regla)
        lineas = (RAIZ / TRAMITE).read_text(encoding="utf-8").splitlines()
        anclas = [i + 1 for i, l in enumerate(lineas)
                  if l.strip() == f"- id: {REGLA_CONSUMIDORA}"]
        self.assertEqual(len(anclas), 1)

    def test_el_registro_gen2_deriva_su_fila_sin_tocar_corrida0(self):
        spec = importlib.util.spec_from_file_location(
            "corrida0_consumidor2", RAIZ / "tools" / "corrida0.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["corrida0_consumidor2"] = mod
        cwd = os.getcwd()
        os.chdir(RAIZ)
        try:
            spec.loader.exec_module(mod)
            ambiguas = []
            filas = mod._consumidores_momentos(ambiguas)
        finally:
            os.chdir(cwd)
        self.assertIn(f"{CATALOGO}:{ID_FILA}", [f["consumidor"] for f in filas])
        self.assertEqual(len(filas), 23)
        self.assertFalse([a for a in ambiguas if ID_FILA in a])


class ElMuroSigueEnPie(unittest.TestCase):
    """Que la cifra esté sellada en corrida0 no la vuelve insumo del motor."""

    def test_valor_de_m05_sigue_lanzando_en_e0(self):
        m = _m05(_catalogo())
        with self.assertRaises(NotImplementedError):
            MM.valor_de(m)

    def test_m05_cuenta_como_ajuste_y_no_como_holdout(self):
        cat = _catalogo()
        self.assertIn(ID_FILA, {m.id_momento for m in MM.momentos_ajuste(cat)})
        self.assertNotIn(ID_FILA, {m.id_momento for m in MM.momentos_holdout(cat)})

    def test_append_only_no_reasigna_roles_ni_este_acto_anade_ids(self):
        r = _git("log", "--diff-filter=A", "--format=%H", "--", CATALOGO)
        if r.returncode != 0 or not r.stdout.strip():
            self.skipTest("sin historia de git para el catálogo")
        s = _git("show", f"{r.stdout.split()[-1]}:{CATALOGO}")
        if s.returncode != 0:
            self.skipTest("no se pudo leer el catálogo del commit de sello")
        sellados = {f["id_momento"]: f["rol_calibracion"] for f in _filas_crudas(s.stdout)}
        hoy = {m.id_momento: m.rol_calibracion for m in _catalogo().momentos}
        for mid, rol in sellados.items():
            self.assertIn(mid, hoy)
            self.assertEqual(hoy[mid], rol, f"{mid} cambió de rol desde el sello")
        self.assertLessEqual(set(hoy) - set(sellados), {"M23"},
                             "este acto no añade ids; el único añadido histórico es M23")


class LaCeldaDYElOrdenDeLosCommits(unittest.TestCase):

    def test_la_celda_d_valida_y_cita_lo_que_existe(self):
        spec = importlib.util.spec_from_file_location(
            "test_celdas_d_v05", RAIZ / "tests" / "test_celdas_d.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        doc = yaml.safe_load((RAIZ / CELDA_D).read_text(encoding="utf-8"))
        self.assertEqual(mod.errors_for(doc["celda_d"], CELDA_D), [])
        c = doc["celda_d"]
        self.assertEqual(c["champion_actual"], "NINGUNO")
        self.assertFalse(c["requiere_decision_mesa"])
        self.assertEqual(c["estado_decidibilidad"], "PUNTUADA")
        refs = c["momentos_holdout_refs"]
        self.assertIn(f"{CATALOGO}:{ID_FILA}", refs)
        corrida = next(x for x in refs if x.startswith("CALC-"))
        self.assertTrue((RAIZ / CALC_ARBITRO / "sello.sha256").exists())
        self.assertTrue(corrida.startswith("CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001--"))

    def test_las_emisiones_se_sellaron_antes_de_que_r_existiera(self):
        """El falsador de orden, leído del historial (lección NC-0313)."""
        e = _git("log", "--diff-filter=A", "--format=%H", "--",
                 f"{CALC_EMISIONES}/resultados.json")
        a = _git("log", "--diff-filter=A", "--format=%H", "--",
                 f"{CALC_ARBITRO}/resultados.json")
        if e.returncode != 0 or a.returncode != 0 or not e.stdout.strip() or not a.stdout.strip():
            self.skipTest("sin historia de git para los dos CALC (p. ej. antes de COMMIT-3)")
        sha_e, sha_a = e.stdout.split()[-1], a.stdout.split()[-1]
        if sha_e == sha_a and _historia_truncada():
            self.skipTest("clon shallow (NC-0273): el borde de injerto de "
                          "`.git/shallow` devuelve el mismo SHA para archivos "
                          "distintos -- no es evidencia de que nacieran juntos")
        self.assertNotEqual(sha_e, sha_a, "R y las emisiones no pueden nacer en el mismo commit")
        es_ancestro = _git("merge-base", "--is-ancestor", sha_e, sha_a)
        self.assertEqual(es_ancestro.returncode, 0,
                         "el commit que selló las emisiones debe ser ancestro del que creó R")
        # y en el commit de las emisiones, el directorio del árbitro NO existía
        ls = _git("ls-tree", "--name-only", sha_e, f"{CALC_ARBITRO}/")
        self.assertEqual(ls.stdout.strip(), "",
                         "el directorio del árbitro existía cuando se sellaron las emisiones")


if __name__ == "__main__":
    unittest.main(verbosity=2)
