#!/usr/bin/env python3
"""`B`: 15 celdas no-cero, clave compuesta, `SinMagnitud` en G5, y la no-suma
de los 22 g.l. con las condicionales.
"""

from _motor_arnes import Arnes, cierto, igual, lanza  # noqa: E402

from milpa.src import matriz as M  # noqa: E402
from milpa.src import procedencia as P  # noqa: E402
from milpa.src.clases import SinMagnitud  # noqa: E402


def main():
    a = Arnes("T-MOTOR-MATRIZ")
    proc = P.cargar()
    B = M.cargar_B(proc)

    def test_quince_celdas_no_cero():
        # G1:2 + G2:2 + G3:3 + G4:4 + G5:3 + G6:1 = 15. La cifra se re-deriva
        # del archivo, no se hereda: el propio `procedencia.yaml` registra que
        # este conteo ya estuvo mal una vez (decía 14).
        igual(B.no_cero, 15, "celdas no-cero de B:")
        igual(len(B.generadores), 6, "generadores:")

    def test_clave_compuesta_obligatoria():
        # Seis nombres de coeficiente se repiten entre generadores. Con clave
        # simple, media matriz se sobrescribiría en silencio.
        nombres = [n for _, n in B.celdas]
        repetidos = {n for n in nombres if nombres.count(n) > 1}
        cierto(len(repetidos) >= 6,
               f"esperaba >=6 nombres repetidos entre generadores, hay "
               f"{len(repetidos)}: {sorted(repetidos)}")
        igual(len(set(B.celdas)), B.no_cero,
              "la clave compuesta no es única:")

    def test_g5_familismo_obligacion_sin_magnitud():
        igual(len(B.sin_magnitud), 1, "celdas SIN MAGNITUD:")
        c = B.sin_magnitud[0]
        igual((c.generador, c.nombre), ("G5", "familismo_obligacion"),
              "celda SIN MAGNITUD:")
        cierto("SIN MAGNITUD" in c.literal,
               "el literal perdió su propia declaración")

    def test_catorce_puntuales_mas_una():
        # M5 de RONDA-M: son 14 puntuales + 1 sin magnitud, NUNCA "15".
        igual(len(B.puntuales), 14, "coeficientes puntuales:")
        igual(len(B.puntuales) + len(B.sin_magnitud), 15, "suma:")

    def test_sin_magnitud_no_se_computa_como_cero():
        lanza(SinMagnitud, M.g, B, object(), None)

    def test_denominador_22_con_su_assert():
        igual(M.verificar_denominador([]), 22, "grados de libertad:")
        lanza(AssertionError, M.verificar_denominador, ["forma_h_r_alpha"])

    def test_no_existe_operacion_que_sume_beta_y_theta():
        # El error de categoría de `modelo`: sumar los 22 g.l. del ajuste y las
        # condicionales medidas. Los tipos son distintos y no hay `__add__`.
        c = M.Coeficiente("G1", "confianza_institucional", -0.60)
        t = M.Condicional("norma_de_género", "MEDIDO·NACIONAL")
        lanza(TypeError, lambda: c + t)

    for nombre, fn in sorted(locals().items()):
        if nombre.startswith("test_"):
            a.prueba(nombre, fn)
    return a.cerrar()


if __name__ == "__main__":
    raise SystemExit(main())
