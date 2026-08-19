#!/usr/bin/env python3
"""EL MURO. Tres verificaciones, no una -- porque un pre-registro que sólo se
declara no es un pre-registro.

(a) el conjunto HOLDOUT sellado en C1 es idéntico al que ve C2;
(b) ninguna ruta de código que evalúe celdas-semilla accede al VALOR de un
    momento HOLDOUT;
(c) los roles quedaron sellados en un commit ANTERIOR EN HISTORIA DE GIT a todo
    resultado -- que es literalmente el umbral (1) de ADR-68 (Ronda 1 §7).
"""

import os
import subprocess

from _motor_arnes import (RAIZ, Arnes, cierto, codigo_efectivo, igual,  # noqa: E402
                          lanza, saltar)

from milpa.src import matriz as M  # noqa: E402
from milpa.src import momentos as MM  # noqa: E402
from milpa.src import motor  # noqa: E402
from milpa.src import procedencia as P  # noqa: E402

CATALOGO = os.path.join("milpa", "catalogo-momentos-v0_1.tsv")
FUENTES_DEL_MOTOR = os.path.join("milpa", "src")


def _git(*args):
    return subprocess.run(
        ["git", "-C", RAIZ, *args],
        capture_output=True, text=True, check=False,
    )


def main():
    a = Arnes("T-MOTOR-HOLDOUT")
    cat = MM.cargar_catalogo()

    def test_a_conjunto_holdout_estable():
        firma = MM.firma_de_roles(cat)
        de_nuevo = MM.firma_de_roles(MM.cargar_catalogo())
        igual(de_nuevo, firma, "la firma de roles cambió entre lecturas:")
        holdout = MM.momentos_holdout(cat)
        cierto(len(holdout) > 0, "el catálogo no tiene ningún HOLDOUT")
        igual(len(holdout) + len(MM.momentos_ajuste(cat)), len(cat),
              "AJUSTE + HOLDOUT no suman el total (¿DIAGNÓSTICO poblado?):")

    def test_a2_firma_contra_el_commit_de_sello():
        # El catálogo tal como quedó en el commit C1 -- no como está en el
        # árbol de trabajo. Si alguien reasignó un rol después de sellar, esto
        # lo ve.
        r = _git("log", "--diff-filter=A", "--format=%H", "--", CATALOGO)
        if r.returncode != 0 or not r.stdout.strip():
            saltar("sin historia de git para el catálogo en este entorno")
        sha_c1 = r.stdout.split()[-1]
        s = _git("show", f"{sha_c1}:{CATALOGO}")
        if s.returncode != 0:
            saltar("no se pudo leer el catálogo del commit de sello")
        import csv
        import io
        filas = list(csv.DictReader(io.StringIO(s.stdout), delimiter="\t"))
        sellada = tuple(sorted(
            (f["id_momento"], f["rol_calibracion"]) for f in filas))
        igual(MM.firma_de_roles(cat), sellada,
              "los roles cambiaron desde el commit de sello:")

    def test_b_ningun_valor_holdout_se_lee():
        for m in MM.momentos_holdout(cat):
            lanza(MM.HoldoutTocado, MM.valor_de, m)

    def test_b2_la_rebanada_completa_no_toca_holdout():
        proc = P.cargar()
        B = M.cargar_B(proc)
        for _, celda_d in motor.celdas_semilla():
            r = motor.evaluar(celda_d, cat, B, semilla=0)
            igual(r.momentos_holdout_intocados, len(MM.momentos_holdout(cat)),
                  f"{r.celda_id}: HOLDOUT intocados:")
        salida = motor.correr(semilla=0)
        igual(salida["holdout_reproducidos"], 0,
              "momentos HOLDOUT reproducidos en E0:")

    def test_b3_el_codigo_del_motor_no_llama_valor_de_en_holdout():
        # Prueba estructural, no de comportamiento: ninguna fuente del motor
        # puede saltarse el muro leyendo el TSV por su cuenta.
        for raiz, _, archivos in os.walk(os.path.join(RAIZ, FUENTES_DEL_MOTOR)):
            for n in archivos:
                if not n.endswith(".py") or n == "momentos.py":
                    continue
                txt = codigo_efectivo(os.path.join(raiz, n))
                cierto("catalogo-momentos" not in txt,
                       f"{n} lee el catálogo por su cuenta, sin pasar por "
                       f"`momentos.py` -- el muro se rodea así")

    def test_c_roles_sellados_antes_que_todo_resultado():
        r = _git("log", "--diff-filter=A", "--format=%H", "--", CATALOGO)
        s = _git("log", "--diff-filter=A", "--format=%H", "--",
                 os.path.join(FUENTES_DEL_MOTOR, "motor.py"))
        if r.returncode != 0 or not r.stdout.strip() or not s.stdout.strip():
            saltar("sin historia de git en este entorno")
        sha_catalogo = r.stdout.split()[-1]
        sha_motor = s.stdout.split()[-1]
        if sha_catalogo == sha_motor:
            raise AssertionError(
                "el catálogo y el motor entraron en el MISMO commit: el "
                "umbral (1) de ADR-68 exige `commit_declaracion` ANTERIOR en "
                "git a todo resultado")
        anc = _git("merge-base", "--is-ancestor", sha_catalogo, sha_motor)
        cierto(anc.returncode == 0,
               "el commit del catálogo no es ancestro del commit del motor")

    for nombre, fn in sorted(locals().items()):
        if nombre.startswith("test_"):
            a.prueba(nombre, fn)
    return a.cerrar()


if __name__ == "__main__":
    raise SystemExit(main())
