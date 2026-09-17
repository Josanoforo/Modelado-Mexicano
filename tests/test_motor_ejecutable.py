#!/usr/bin/env python3
"""Guarda de ejecutabilidad del motor -- `ACTO AUTO-MOTOR-1`, NC-0023.

`PR #615` (`ACTO GEN2-T9`) midió que `procedencia.cargar()` LANZABA
`ClaseDesconocida` sobre `milpa/procedencia.yaml`: dos valores de `clase:`
(`REFUTADO-POR-COTA`, `EVIDENCIA_EXPERIMENTAL_TERCEROS`) sin prefijo
reconocido. Nada lo notó porque nada corría el motor. Esta prueba existe
para que la próxima vez que alguien rompa esa ruta, CI lo diga -- no un
acto que la vuelva a descubrir por accidente.

Se ejerce la ruta REAL sobre las entradas REALES versionadas: sin corpus,
sin red, sin sesión de Claude, sin escribir ningún resultado de producción
(no toca `data/corrida0/**`, no llama a `corrida0 run`). No admite `skip`
ni captura `ClaseDesconocida` como éxito -- si `procedencia.cargar()`
volviera a lanzar, esta prueba debe FALLAR, no saltarse.
"""

import os
import tempfile

from _motor_arnes import RAIZ, Arnes, cierto, codigo_efectivo, igual, lanza  # noqa: E402

from milpa.src import clases as K  # noqa: E402
from milpa.src import matriz as M  # noqa: E402
from milpa.src import momentos as MM  # noqa: E402
from milpa.src import motor  # noqa: E402
from milpa.src import procedencia as P  # noqa: E402


def main():
    a = Arnes("T-MOTOR-EJECUTABLE")

    def test_carga_real_sin_clase_desconocida():
        # La entrada real versionada, no un fixture: si `clasificar()`
        # deja de reconocer algo del árbol de hoy, esto revienta aquí --
        # no se envuelve en try/except.
        proc = P.cargar()
        cierto(len(proc.entradas) > 0, "procedencia.cargar() no produjo entradas")

    # ENMIENDA FECHADA 2026-09-17 (ACTO GEN2-CELDA-D-CAREO-1, ADR-533).
    # Este test cableaba `igual(len(semillas), 3)` y `igual(len(resultados), 3)`,
    # y el 3 se rompió en cuanto el programa hizo lo que su propio contrato
    # anuncia: registrar la primera celda-D del piloto (celdas-d/ pasa de 3 a
    # 4 archivos). El cableado contradecía dos cosas ya escritas: el docstring
    # de `motor.celdas_semilla()` -- «Las celdas-D del disco. Son las que hay;
    # NO SE ENUMERAN DE MEMORIA» -- y el de `tests/test_celdas_d.py`, que dice
    # que «el piloto va a escribir 10-15 más». Un conteo literal sobre un
    # directorio que el contrato declara creciente es una bomba de tiempo con
    # fecha, no una invariante.
    #
    # NO se relaja el test: se sustituye el conteo por lo que ese conteo
    # protegía de verdad -- que ninguna celda sellada desaparezca en silencio
    # (p. ej. por un fallo de lectura que devolviera la lista corta) -- y eso
    # se afirma por ID, que es más fuerte que por cardinalidad. Las tres
    # aserciones por celda (vocabulario A.4, HOLDOUT intocados, un veredicto
    # por celda) siguen intactas y ahora cubren TODA celda del disco, no tres.
    SEMILLAS_SELLADAS = {
        "G5.familismo_obligacion.actitud",
        "G5.obligacion_medida.conducta",
        "G5.radio_confianza.encuci_vs_enbiare",
    }

    def test_evalua_las_celdas_semilla_con_salida_identificable():
        proc = P.cargar()
        B = M.cargar_B(proc)
        cat = MM.cargar_catalogo()
        semillas = motor.celdas_semilla()
        ids = {str(c.get("id")) for _, c in semillas}
        faltantes = SEMILLAS_SELLADAS - ids
        cierto(not faltantes,
               f"celdas-D selladas que desaparecieron del disco: "
               f"{sorted(faltantes)}")
        cierto(len(semillas) >= len(SEMILLAS_SELLADAS),
               f"celdas-D en el disco ({len(semillas)}) por debajo de las "
               f"selladas ({len(SEMILLAS_SELLADAS)})")
        resultados = [motor.evaluar(c, cat, B) for _, c in semillas]
        igual(len(resultados), len(semillas), "veredictos producidos:")
        for r in resultados:
            cierto(r.veredicto in motor.VEREDICTOS,
                   f"{r.celda_id}: veredicto fuera del vocabulario A.4: "
                   f"{r.veredicto!r}")
            igual(r.momentos_holdout_intocados,
                  len(MM.momentos_holdout(cat)),
                  f"{r.celda_id}: HOLDOUT intocados:")

    def test_refutado_por_cota_no_reingresa_como_consumible():
        # El contrato de P1: un prior REFUTADO-POR-COTA no reaparece como
        # ASIGNADO consumible, ni por su propia clase ni por la del bloque
        # que lo contiene.
        proc = P.cargar()
        refutadas = proc.por_clase(K.Clase.REFUTADO_POR_COTA)
        cierto(refutadas, "no hay ninguna entrada REFUTADO-POR-COTA en el árbol")
        consumibles_llaves = {e.llave for e in proc.consumibles()}
        for e in refutadas:
            cierto(e.llave not in consumibles_llaves,
                   f"`{e.llave}` (REFUTADO-POR-COTA) entró a consumibles()")

    def test_evidencia_terceros_no_alimenta_magnitud_no_autorizada():
        proc = P.cargar()
        evidencia = proc.por_clase(K.Clase.EVIDENCIA_EXPERIMENTAL_TERCEROS)
        cierto(evidencia, "no hay ninguna entrada EVIDENCIA_EXPERIMENTAL_TERCEROS")
        for e in evidencia:
            cierto(e.crudo.startswith("EVIDENCIA_EXPERIMENTAL_TERCEROS"),
                   f"`crudo` mutilado en {e.llave}")
        # Garantía ESTRUCTURAL, no de comportamiento: `matriz.cargar_B()` --
        # lo único que el motor consume numéricamente -- no menciona el
        # bloque `evidencia_experimental_terceros` en ninguna parte de su
        # código. No hay ruta por la que un número de esa clase entre a B.
        ruta_matriz = os.path.join(RAIZ, "milpa", "src", "matriz.py")
        txt = codigo_efectivo(ruta_matriz)
        cierto("evidencia_experimental_terceros" not in txt,
               "matriz.py menciona el bloque de terceros -- ya no es "
               "estructuralmente imposible que le extraiga una magnitud")
        B = M.cargar_B(proc)
        igual(B.no_cero, 15, "B sigue con sus 15 celdas de siempre:")

    def test_determinismo_mismos_insumos_misma_semilla():
        from milpa.src import salida
        h1 = salida.hash_salida(motor.correr(semilla=0))
        h2 = salida.hash_salida(motor.correr(semilla=0))
        igual(h1, h2, "hash con la misma semilla:")

    def test_clase_desconocida_en_fixture_temporal_falla():
        # Fixture EN UN TEMPORAL, nunca en una entrada versionada: se copia
        # el archivo real y se le inyecta una clase inventada al final.
        # `cargar()` debe LANZAR -- no admitir skip, no capturarla como
        # éxito silencioso.
        ruta_real = P.RUTA_POR_DEFECTO
        with open(ruta_real, encoding="utf-8") as fh:
            texto = fh.read()
        texto_roto = texto + (
            "\ncondicionales_prueba_ejecutable_temporal:\n"
            "  fixture_clase_inventada:\n"
            "    clase: \"CLASE-QUE-NO-EXISTE-EN-CLASES-PY\"\n"
        )
        with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False, encoding="utf-8") as fh:
            fh.write(texto_roto)
            ruta_temporal = fh.name
        try:
            lanza(K.ClaseDesconocida, P.cargar, ruta_temporal)
        finally:
            os.unlink(ruta_temporal)
        # y la entrada real versionada sigue intacta -- no se tocó.
        with open(ruta_real, encoding="utf-8") as fh:
            igual(fh.read(), texto, "milpa/procedencia.yaml no debía cambiar")

    for nombre, fn in sorted(locals().items()):
        if nombre.startswith("test_"):
            a.prueba(nombre, fn)
    return a.cerrar()


if __name__ == "__main__":
    raise SystemExit(main())
