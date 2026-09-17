#!/usr/bin/env python3
"""La capa del esquema E1 cubre EXACTAMENTE los nombres de `theta.py`.

`ADR-531` rama B selló "Esquema E1: capa separada". La capa es
`milpa/theta-esquema-e1-v1_0.yaml`, derivada del censo E1 §3. Este test la
ata a su única fuente de verdad —el conjunto de llaves que `theta.py`
entrega— para que no se pueda desincronizar en silencio: una entrada nueva
en `procedencia.yaml` sin fila en la capa, o una fila de la capa que ya no
corresponde a ninguna θ, rompe aquí.

El segundo test es el que importa de verdad: **hoy ninguna θ propia del
modelo alcanza `ARGUMENTO_EXPLICITO`** (censo E1 §4.3; el único intento,
`G3_horizonte_temporal`, es un `GATE·ID-X` detenido por falta de potencia
antes de producir estimando). El test FALLA el día que una lo alcance —
a propósito. No es un candado contra la identificación: es el aviso de que
ese día llegó y alguien tiene que mirarlo, en vez de que la primera θ
identificada del programa entre sin que nadie se entere.
"""

import os

import yaml

from _motor_arnes import Arnes, cierto, igual  # noqa: E402

from milpa.src import procedencia as P  # noqa: E402
from milpa.src import theta as T  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPA = os.path.join(RAIZ, "milpa", "theta-esquema-e1-v1_0.yaml")


def _capa():
    with open(CAPA, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main():
    a = Arnes("T-THETA-ESQUEMA-E1")
    capa = _capa()
    nombres_theta = set(T.Theta.desde(P.cargar()).entradas)
    nombres_capa = set(capa["theta"])

    def test_cobertura_exacta():
        # Ni uno más ni uno menos. Los dos sentidos se reportan por separado
        # porque son defectos distintos: falta una θ en la capa, o la capa
        # arrastra un nombre que `theta.py` ya no entrega.
        igual(sorted(nombres_theta - nombres_capa), [],
              "θ de `theta.py` SIN fila en la capa:")
        igual(sorted(nombres_capa - nombres_theta), [],
              "filas de la capa SIN θ en `theta.py`:")
        igual(capa["contador"]["nombres_theta"], len(nombres_theta),
              "`contador.nombres_theta` contra el conjunto real:")

    def test_ninguna_theta_alcanza_argumento_explicito():
        # Hoy debe ser 0 (censo E1 §4.3). Si este test falla, NO se edita
        # la capa para acallarlo: se mira la θ que lo alcanzó.
        con_argumento = sorted(
            n for n, e in capa["theta"].items()
            if str(e["identificacion"]).startswith("ARGUMENTO_EXPLICITO")
        )
        igual(con_argumento, [], "θ con ARGUMENTO_EXPLICITO:")
        igual(capa["contador"]["argumento_explicito"], 0,
              "`contador.argumento_explicito`:")

    def test_tres_campos_por_entrada():
        faltan = sorted(
            n for n, e in capa["theta"].items()
            if not all(str(e.get(c) or "").strip()
                       for c in ("escala", "universo", "identificacion"))
        )
        igual(faltan, [], "entradas sin los tres campos:")

    def test_la_capa_no_carga_ninguna_theta():
        # La capa es METADATO. `theta.valor()` sigue lanzando para los 43:
        # si algún día deja de lanzar, no será porque este archivo exista.
        t = T.Theta.desde(P.cargar())
        for nombre in nombres_capa:
            try:
                t.valor(nombre)
            except T.ThetaNoDisponible:
                continue
            cierto(False, f"`{nombre}` dejó de lanzar ThetaNoDisponible")

    def test_dispersion_quince_familias_sin_declarar():
        # La enmienda de E1 §4.4: son 15 familias, no 90 parámetros
        # (`canon/modelo-decision-v4_0.md:806`, ADR-28.d). Los 15 pares se
        # comparan contra `asignados_coeficiente.detalle`, no contra una
        # lista transcrita a mano.
        familias = capa["dispersion"]["familias"]
        igual(len(familias), 15, "familias de dispersión:")
        crudo = P.cargar().crudo
        pares = {
            "%s×%s" % (d["gen"], c)
            for d in crudo["asignados_coeficiente"]["detalle"]
            for c in d["coefs"]
        }
        igual(sorted(familias), sorted(pares),
              "pares gen×coef de la capa contra `asignados_coeficiente.detalle`:")
        igual(sorted({str(v) for v in familias.values()}), ["NO-DECLARADA"],
              "estado de las 15 familias:")

    def test_g5_esta_en_su_seccion():
        # NC-0263: la llave se movió de `propuesta_de_esquema:` a
        # `coeficientes_generador_medidos:` sin tocar un solo valor.
        crudo = P.cargar().crudo
        cierto("G5_familismo_apoyo" in crudo["coeficientes_generador_medidos"],
               "G5_familismo_apoyo bajo coeficientes_generador_medidos")
        cierto("G5_familismo_apoyo" not in crudo["propuesta_de_esquema"],
               "G5_familismo_apoyo ya NO bajo propuesta_de_esquema")
        igual(capa["theta"]["G5_familismo_apoyo"]["ruta_yaml"],
              "coeficientes_generador_medidos.G5_familismo_apoyo",
              "ruta_yaml de G5 en la capa:")

    def test_cero_mediciones_de_este_acto():
        igual(capa["contador"]["mediciones_de_este_acto"], 0,
              "mediciones del acto que escribió la capa:")

    for nombre, fn in sorted(locals().items()):
        if nombre.startswith("test_"):
            a.prueba(nombre, fn)
    return a.cerrar()


if __name__ == "__main__":
    raise SystemExit(main())
