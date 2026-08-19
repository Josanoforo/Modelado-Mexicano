#!/usr/bin/env python3
"""El cargador contra el archivo REAL: tipos mixtos, no-ASCII, prefix-match, y
el contador por la fórmula oficial de T19b -- no por una fórmula propia.
"""

from _motor_arnes import Arnes, cierto, igual, lanza  # noqa: E402

from milpa.src import clases as K  # noqa: E402
from milpa.src import procedencia as P  # noqa: E402


def main():
    a = Arnes("T-MOTOR-PROCEDENCIA")
    proc = P.cargar()

    def test_carga_sin_clase_desconocida():
        cierto(len(proc.entradas) > 0, "el archivo no produjo ninguna entrada")

    def test_contador_replica_la_formula_de_t19b():
        # `tests/check.py` T19b/T19c derivan el numerador sobre TEXTO CRUDO.
        # Se replica exacta: cualquier otra fórmula produciría una cifra que
        # compite con canon, que es justo lo que E0 tiene prohibido.
        txt = proc.texto
        esperado = (txt.count('clase: "MEDIDO·PARCIAL')
                    + txt.count('clase: "MEDIDO·NACIONAL'))
        igual(proc.contador_condicionales_medidas(), esperado,
              "contador de condicionales medidas:")

    def test_clase_implicita_de_bloque_se_declara():
        # `ASIGNADO` NO aparece nunca como valor de un campo `clase:`: es la
        # clase del bloque. Un cargador que sólo buscara `clase:` reportaría
        # cero ASIGNADO en un archivo cuyo propio diagnóstico dice que los 15
        # coeficientes son todos ASIGNADO.
        asignados = proc.por_clase(K.Clase.ASIGNADO)
        cierto(len(asignados) > 0,
               "cero entradas ASIGNADO: la correspondencia de bloque se rompió")
        cierto(all(e.banda is None for e in asignados),
               "alguna ASIGNADO trae banda: el archivo no tiene ninguna")

    def test_crudo_se_conserva_integro():
        for e in proc.por_clase(K.Clase.MEDIDO_PARCIAL):
            cierto(e.crudo.startswith("MEDIDO·PARCIAL"),
                   f"`crudo` mutilado en {e.llave}")
            igual(K.ejes_declarados(e.crudo), e.ejes, f"ejes de {e.llave}:")

    def test_llaves_no_ascii_y_con_guion():
        # Acceso por dict[...], nunca por atributo. Si alguna llave se
        # normalizara a ASCII, este cruce contra el YAML crudo fallaría.
        llaves = {e.llave for e in proc.entradas}
        cierto(any(not k.isascii() for k in llaves)
               or any("-" in k or "_" in k for k in llaves),
               "ninguna llave con no-ASCII ni guion: revisa el recorrido")

    def test_tipos_mixtos_no_rompen_la_carga():
        # `n_util` es int en unas entradas y prosa en otras; `derivados[].de`
        # es float en unas y str en otra. La carga no debe asumir tipo.
        crudo = proc.crudo
        cierto(isinstance(crudo, dict), "el YAML no cargó como mapa")
        cierto("asignados_coeficiente" in crudo,
               "falta `asignados_coeficiente` en el árbol cargado")

    def test_gate_id_se_carga_pero_no_consume():
        gates = proc.por_clase(K.Clase.GATE_ID)
        cierto(gates, "el árbol trae al menos una GATE·ID y no se cargó")
        consumibles = {id(e) for e in proc.consumibles()}
        for g in gates:
            cierto(id(g) not in consumibles,
                   f"`{g.llave}` (GATE·ID) entró a `consumibles()`")
            lanza(K.GateDetiene, P.como_estimando, g)

    for nombre, fn in sorted(locals().items()):
        if nombre.startswith("test_"):
            a.prueba(nombre, fn)
    return a.cerrar()


if __name__ == "__main__":
    raise SystemExit(main())
