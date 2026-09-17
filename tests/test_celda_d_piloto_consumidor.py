#!/usr/bin/env python3
"""El consumidor lee la fila nueva del catálogo de momentos SIN CAMBIAR CÓDIGO.

`ACTO GEN2-CELDA-D-PILOTO-1`, `COMMIT-3`. Lo que el encargo pide, verbatim:
*«una fila de `milpa/catalogo-momentos-v0_1.tsv` con `estatus_disponibilidad`
distinto de `NO-VERIFICADO` y `spec_ref`; prueba de que el consumidor
(`tramite.yaml:1306`) puede leerla sin cambiar código (test, no prosa)»*.

Esto es esa prueba. **Ni `milpa/src/momentos.py` ni `tools/corrida0.py` se
tocaron** para que la fila `M23` se lea: el `csv.DictReader` de `momentos.py`
resuelve por nombre de columna, así que una columna nueva al final no rompe a
nadie y las 22 filas legado siguen leyéndose exactamente igual. Eso es lo que
se verifica aquí, no lo que se afirma.

**Lo que este test NO hace, y es deliberado:** no lee el VALOR del momento. `M23`
es `HOLDOUT` — fue la reserva de evaluación de su propio piloto, ya se consumió,
y `valor_de()` tiene que seguir lanzando. Un muro que se puede cruzar avisando
no es un muro. Se comprueba que sigue lanzando.

**Hallazgo que este test deja a la vista** (`test_append_only_no_reasigna_roles`):
el catálogo se declara *«append-only por construcción»*
(`milpa/src/momentos.py::sellar_catalogo`), pero
`tests/test_motor_holdout.py::test_a2_firma_contra_el_commit_de_sello` comparaba
la firma COMPLETA contra el commit de sello, de modo que **añadir un id nuevo lo
rompía aunque no reasignara ningún rol**. La intención declarada de esa guardia
era, verbatim, *«Si alguien reasignó un rol después de sellar, esto lo ve»* — y
eso es exactamente lo que el test de abajo comprueba, sin prohibir el append.
CORREGIDO por `ACTO GEN2-GUARDIAS-1` (NC-0309, 17/sep/2026): la guardia ahora
compara por rama (id sellado que cambió de rol / id nuevo sin rol), no la firma
completa; el hallazgo que este comentario describía queda documentado por
histórico, ya no reproduce.
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

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from milpa.src import momentos as MM  # noqa: E402

CATALOGO = "milpa/catalogo-momentos-v0_1.tsv"
ID_NUEVO = "M23"
REGLA_CONSUMIDORA = "dinero.ahorro.via_informal"
TRAMITE = "milpa/tramite.yaml"

# NC-0330: congelado al escribir este test (commit `18b9914`, COMMIT-3 de
# GEN2-CELDA-D-PILOTO-1), no un conteo. `M05` era `NO-VERIFICADO` entonces y
# pasó a derivada el mismo día (17/sep/2026); bajar de este conjunto es
# correcto -- ids que se verifican con el tiempo --, subir por encima de él
# (un id sellado que reaparece como NO-VERIFICADO, o uno nuevo que nace así
# sin pasar por adjudicación) no lo es.
IDS_NO_VERIFICADO_CONGELADO_18b9914 = frozenset({
    "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10",
    "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20",
    "M21", "M22",
})


def _git(*args):
    return subprocess.run(["git", "-C", str(RAIZ), *args],
                          capture_output=True, text=True, check=False)


def _catalogo():
    return MM.cargar_catalogo()


def _m23(cat):
    return next(m for m in cat.momentos if m.id_momento == ID_NUEVO)


def _filas_crudas(texto):
    return list(csv.DictReader(io.StringIO(texto), delimiter="\t"))


class ElConsumidorLaLeeSinCambiarCodigo(unittest.TestCase):
    """`momentos.py` y `corrida0.py` intactos; la fila entra igual."""

    def test_el_catalogo_carga_con_el_lector_de_siempre(self):
        cat = _catalogo()                     # si la columna nueva rompiera
        self.assertEqual(len(cat), 23)        # algo, esto lanzaría
        self.assertIn(ID_NUEVO, [m.id_momento for m in cat.momentos])

    def test_las_22_filas_legado_se_leen_identicas(self):
        """La columna `spec_ref` es nueva: las de antes no cambian de sentido."""
        r = _git("show", f"HEAD:{CATALOGO}")
        if r.returncode != 0:
            self.skipTest("sin historia de git para el catálogo")
        antes = {f["id_momento"]: f for f in _filas_crudas(r.stdout)}
        ahora = {f["id_momento"]: f
                 for f in _filas_crudas((RAIZ / CATALOGO).read_text(encoding="utf-8"))}
        comunes = sorted(set(antes) & set(ahora))
        self.assertGreaterEqual(len(comunes), 22)
        for mid in comunes:
            for col, v in antes[mid].items():
                if col == "spec_ref":
                    continue
                self.assertEqual(ahora[mid][col], v,
                                 f"{mid}.{col} cambió y no debía")

    def test_la_fila_nueva_esta_disponible_y_trae_spec_ref(self):
        m = _m23(_catalogo())
        self.assertNotEqual(m.estatus_disponibilidad, "NO-VERIFICADO")
        self.assertEqual(m.estatus_disponibilidad, "DERIVADO-Y-SELLADO-GEN2")
        filas = {f["id_momento"]: f for f in _filas_crudas(
            (RAIZ / CATALOGO).read_text(encoding="utf-8"))}
        spec_ref = filas[ID_NUEVO]["spec_ref"]
        self.assertTrue(spec_ref and spec_ref != "NO-APLICA")
        # `spec_ref` no es prosa: cada ruta que nombra tiene que existir.
        rutas = [x.strip() for x in spec_ref.split("|")]
        self.assertGreaterEqual(len(rutas), 2)
        for ruta in rutas:
            self.assertTrue((RAIZ / ruta).exists(), f"spec_ref apunta a {ruta}, que no existe")

    def test_las_22_legado_siguen_sin_verificar_y_solo_se_movio_una(self):
        cat = _catalogo()
        sin_verificar = {m.id_momento for m in cat.momentos
                         if m.estatus_disponibilidad == "NO-VERIFICADO"}
        extra = sin_verificar - IDS_NO_VERIFICADO_CONGELADO_18b9914
        self.assertEqual(extra, set(),
                         f"ids NO-VERIFICADO fuera del congelado: {sorted(extra)}")
        self.assertNotIn(ID_NUEVO, sin_verificar)

    def test_la_regla_consumidora_existe_en_el_motor(self):
        """`fuente_regla` nombra una regla REAL de `tramite.yaml`, no una cita."""
        m = _m23(_catalogo())
        self.assertIn(REGLA_CONSUMIDORA, m.fuente_regla)
        lineas = (RAIZ / TRAMITE).read_text(encoding="utf-8").splitlines()
        anclas = [i + 1 for i, l in enumerate(lineas)
                  if l.strip() == f"- id: {REGLA_CONSUMIDORA}"]
        self.assertEqual(len(anclas), 1,
                         f"`{REGLA_CONSUMIDORA}` debe aparecer una vez en {TRAMITE}")
        # El número de línea que el encargo cita (1306) es informativo: si
        # `tramite.yaml` se mueve, la regla sigue siendo la misma y el enlace
        # se identifica por su id, no por su renglón.
        self.assertGreater(anclas[0], 0)

    def test_el_registro_gen2_deriva_su_fila_sin_tocar_corrida0(self):
        """`tools/corrida0.py::_consumidores_momentos` la recorre sin ambigüedad."""
        spec = importlib.util.spec_from_file_location(
            "corrida0_consumidor", RAIZ / "tools" / "corrida0.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["corrida0_consumidor"] = mod
        cwd = os.getcwd()
        os.chdir(RAIZ)
        try:
            spec.loader.exec_module(mod)
            ambiguas = []
            filas = mod._consumidores_momentos(ambiguas)
        finally:
            os.chdir(cwd)
        consumidores = [f["consumidor"] for f in filas]
        self.assertIn(f"{CATALOGO}:{ID_NUEVO}", consumidores)
        self.assertEqual(len(filas), 23)
        # La fila nueva NO entra a la lista de ambiguas: su
        # `universo_candidatos` está declarado, no `POR DECLARAR`.
        self.assertFalse([a for a in ambiguas if ID_NUEVO in a],
                         f"{ID_NUEVO} salió ambigua: {ambiguas}")


class ElMuroSigueEnPie(unittest.TestCase):
    """Leer la fila NO es poder usar su valor."""

    def test_valor_de_m23_sigue_lanzando(self):
        m = _m23(_catalogo())
        self.assertEqual(m.rol_calibracion, "HOLDOUT")
        with self.assertRaises(MM.HoldoutTocado):
            MM.valor_de(m)

    def test_m23_cuenta_como_holdout_y_no_como_ajuste(self):
        cat = _catalogo()
        ids_holdout = {m.id_momento for m in MM.momentos_holdout(cat)}
        ids_ajuste = {m.id_momento for m in MM.momentos_ajuste(cat)}
        self.assertIn(ID_NUEVO, ids_holdout)
        self.assertNotIn(ID_NUEVO, ids_ajuste)
        # Sin `DIAGNÓSTICO` poblado, los dos conjuntos siguen sumando el total.
        self.assertEqual(len(ids_holdout) + len(ids_ajuste), len(cat))


class AppendOnlyDeVerdad(unittest.TestCase):
    """Lo que la guardia del muro QUERÍA decir, y que el catálogo cumple.

    `momentos.sellar_catalogo` se declara «append-only por construcción». Esta
    es esa propiedad, comprobada: ningún id sellado cambió de rol; lo único que
    pasó es que hay ids nuevos.
    """

    def test_append_only_no_reasigna_roles(self):
        r = _git("log", "--diff-filter=A", "--format=%H", "--", CATALOGO)
        if r.returncode != 0 or not r.stdout.strip():
            self.skipTest("sin historia de git para el catálogo")
        sha_c1 = r.stdout.split()[-1]
        s = _git("show", f"{sha_c1}:{CATALOGO}")
        if s.returncode != 0:
            self.skipTest("no se pudo leer el catálogo del commit de sello")
        sellados = {f["id_momento"]: f["rol_calibracion"]
                    for f in _filas_crudas(s.stdout)}
        hoy = {m.id_momento: m.rol_calibracion for m in _catalogo().momentos}
        for mid, rol in sellados.items():
            self.assertIn(mid, hoy, f"{mid} DESAPARECIÓ del catálogo")
            self.assertEqual(hoy[mid], rol,
                             f"{mid} cambió de rol desde el sello: {rol} -> {hoy[mid]}")
        nuevos = sorted(set(hoy) - set(sellados))
        self.assertEqual(nuevos, [ID_NUEVO],
                         f"ids añadidos desde el sello: {nuevos}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
