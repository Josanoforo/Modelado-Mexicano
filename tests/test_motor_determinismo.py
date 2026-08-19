#!/usr/bin/env python3
"""Misma semilla ⇒ mismo hash. Dos corridas en el mismo proceso y dos en
procesos distintos -- porque el orden de un `set` puede variar ENTRE procesos y
no dentro de uno, y probarlo sólo intra-proceso deja pasar justo ese defecto.
"""

import json
import subprocess
import sys

from _motor_arnes import RAIZ, Arnes, cierto, codigo_efectivo, igual  # noqa: E402

from milpa.src import motor, salida  # noqa: E402

_SUBPROCESO = (
    "import sys; sys.path.insert(0, %r);"
    "from milpa.src import motor, salida;"
    "print(salida.hash_salida(motor.correr(semilla=%d)))"
)


def main():
    a = Arnes("T-MOTOR-DETERMINISMO")

    def test_misma_semilla_mismo_hash_intra_proceso():
        h1 = salida.hash_salida(motor.correr(semilla=7))
        h2 = salida.hash_salida(motor.correr(semilla=7))
        igual(h1, h2, "hash con la misma semilla:")

    def test_misma_semilla_mismo_hash_inter_proceso():
        h_local = salida.hash_salida(motor.correr(semilla=7))
        salidas = []
        for _ in range(2):
            r = subprocess.run(
                [sys.executable, "-c", _SUBPROCESO % (RAIZ, 7)],
                capture_output=True, text=True, cwd=RAIZ, check=True,
                env={"PYTHONHASHSEED": "random", "PATH": "/usr/bin:/bin"},
            )
            salidas.append(r.stdout.strip())
        igual(salidas[0], salidas[1], "hash entre dos procesos:")
        igual(salidas[0], h_local, "hash de subproceso vs. local:")

    def test_semilla_distinta_se_ve_en_la_salida():
        r7 = motor.correr(semilla=7)
        r8 = motor.correr(semilla=8)
        igual(r7["semilla"], 7, "semilla registrada:")
        igual(r8["semilla"], 8, "semilla registrada:")
        cierto(salida.hash_salida(r7) != salida.hash_salida(r8),
               "dos semillas distintas dieron el mismo hash: la semilla no "
               "está entrando a la serialización")

    def test_serializacion_es_canonica():
        # `repr()` de un dict depende del orden de inserción; el hash tiene que
        # ser inmune a eso o el determinismo es una coincidencia.
        a1 = salida.serializar({"b": 1, "a": 2})
        a2 = salida.serializar({"a": 2, "b": 1})
        igual(a1, a2, "serialización canónica:")
        json.loads(a1)

    def test_sin_reloj_ni_azar_en_las_fuentes():
        import os
        prohibidos = ("datetime.now", "time.time", "random.", "uuid")
        for raiz, _, archivos in os.walk(os.path.join(RAIZ, "milpa", "src")):
            for n in sorted(archivos):
                if not n.endswith(".py"):
                    continue
                txt = codigo_efectivo(os.path.join(raiz, n))
                for p in prohibidos:
                    cierto(p not in txt,
                           f"{n} usa `{p}`: el determinismo se rompe")

    for nombre, fn in sorted(locals().items()):
        if nombre.startswith("test_"):
            a.prueba(nombre, fn)
    return a.cerrar()


if __name__ == "__main__":
    raise SystemExit(main())
