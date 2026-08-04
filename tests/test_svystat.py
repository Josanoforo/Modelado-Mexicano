#!/usr/bin/env python3
"""Validacion independiente de tests/svystat.py -- prop_ultimate_cluster.

Encargo E-3 (4/ago/2026). Contexto: svystat.py se reimplemento desde cero
el 03/ago/2026 (CAL-CONF Fase B / segunda ola, commit 40e5248) y desde
entonces varias mediciones del programa dependen de el (CAL-CONF Fase B,
Hito D R7.2, la condicional en curso al momento de este acto). El propio
modulo trae un autochequeo (_caso_conocido) pero es un caso degenerado:
SRS, un solo estrato, un solo elemento por UPM -- nunca ejercita mas de
un estrato, ni mas de una observacion por UPM, ni pesos desiguales entre
UPM. Este archivo cierra exactamente esa brecha.

Que hay aqui:
  1. test_caso_sintetico_dos_estratos() -- EL CASO QUE VALIDA. Dataset
     chico (2 estratos x 5 UPM x pesos desiguales, ninguna UPM con una
     sola fila), con p_hat y var(p_hat) derivados A MANO con la formula
     del docstring de svystat.py, verificados contra prop_ultimate_cluster().
  2. test_estrato_singleton() -- chequeo barato adyacente: confirma que
     un estrato de una sola UPM se excluye de la varianza (documentado en
     el propio modulo) de forma identificable, no como un cero indistin-
     guible de precision real.
  3. Una llamada a svystat._caso_conocido() (el autochequeo del modulo,
     ya existente) como tercera confirmacion, gratis.

Que NO hay aqui -- las dos reproducciones archivadas (Hito D R7.2 ocho
olas; CAL-CONF Fase B ola2) se corrieron por separado, re-ejecutando los
scripts YA COMMITEADOS (tests/hitoD_r7_2_ocho_olas.py, rama
sesion/hitoD-r7-2-delito-sin-seguro; tests/cal_conf_faseb_ola2.py, main)
contra el microdato real -- no tiene sentido reimplementar esos pipelines
aqui. Detalle completo, con los tres resultados contra la cifra archivada,
en forense/notas/2026-08-04-svystat-casos-referencia.md.

Corre solo; no esta cableado a check.py (decision de mesa aparte si se
quiere agregar como test obligatorio):

    python3 tests/test_svystat.py
"""
import math
import sys

sys.path.insert(0, "tests")
import svystat  # noqa: E402
from svystat import prop_ultimate_cluster  # noqa: E402

TOL = 1e-9  # misma tolerancia que el autochequeo del propio modulo
            # (_caso_conocido); generosa frente a la precision real de
            # float64 (~1e-16) -- cualquier desviacion real la atrapa
            # con margen de sobra.


def test_caso_sintetico_dos_estratos():
    """El caso que valida.

    2 estratos, 5 UPM (3 en A, 2 en B), pesos y conteos de fila desiguales,
    ninguna UPM con una sola fila. Formula (verbatim del docstring de
    svystat.py):

      p_hat = sum(w*y) / sum(w)
      t_h_i = sum(w*y) en la UPM i del estrato h
      n_h_i = sum(w)   en la UPM i del estrato h
      e_h_i = t_h_i - p_hat * n_h_i
      var(p_hat) = (1/N_hat^2) * sum_h [ (n_h/(n_h-1)) * sum_i (e_h_i - mean_i(e_h_i))^2 ]

    Dataset (estrato, upm, peso, y):
      A1: (2,1) (3,0)         -> t=2  n=5
      A2: (1,1) (1,1) (2,0)   -> t=2  n=4
      A3: (4,0) (2,1)         -> t=2  n=6
      B1: (6,1) (2,0)         -> t=6  n=8
      B2: (2,0) (4,1) (3,1)   -> t=7  n=9

    N_hat = (5+4+6) + (8+9) = 32
    num   = (2+2+2) + (6+7) = 19
    p_hat = 19/32 = 0.59375

    e_h_i = t_h_i - p_hat*n_h_i  (p_hat=19/32, todo sobre denominador 32):
      A1 = 2 - 19/32*5 = 64/32 - 95/32  = -31/32
      A2 = 2 - 19/32*4 = 64/32 - 76/32  = -12/32
      A3 = 2 - 19/32*6 = 64/32 - 114/32 = -50/32
      B1 = 6 - 19/32*8 = 192/32 - 152/32 = 40/32
      B2 = 7 - 19/32*9 = 224/32 - 171/32 = 53/32

    Estrato A (n_h=3): mean_e_A = (-31-12-50)/32/3 = -93/96 = -31/32
      desviaciones: 0, 19/32, -19/32  ->  ss_A = 2*(19/32)^2 = 361/512
      aporte_A = (n_h/(n_h-1)) * ss_A = (3/2) * 361/512 = 1083/1024

    Estrato B (n_h=2): mean_e_B = (40+53)/32/2 = 93/64
      desviaciones: -13/64, 13/64  ->  ss_B = 2*(13/64)^2 = 169/2048
      aporte_B = (2/1) * ss_B = 169/1024

    suma = 1083/1024 + 169/1024 = 1252/1024 = 313/256
    var(p_hat) = suma / N_hat^2 = (313/256) / 1024 = 313/262144

    (32 = 2^5 y ambos n_h-1 (2 y 1) tambien son potencias de 2, asi que
    todo denominador intermedio se queda en potencias de 2 -- 313/262144
    es exactamente representable en binario, sin redondeo de por medio
    que pueda esconder un error de calculo en esta derivacion.)
    """
    rows = [
        ("A", "A1", 2.0, 1.0), ("A", "A1", 3.0, 0.0),
        ("A", "A2", 1.0, 1.0), ("A", "A2", 1.0, 1.0), ("A", "A2", 2.0, 0.0),
        ("A", "A3", 4.0, 0.0), ("A", "A3", 2.0, 1.0),
        ("B", "B1", 6.0, 1.0), ("B", "B1", 2.0, 0.0),
        ("B", "B2", 2.0, 0.0), ("B", "B2", 4.0, 1.0), ("B", "B2", 3.0, 1.0),
    ]
    p_esperado = 19 / 32
    var_esperado = 313 / 262144
    se_esperado = math.sqrt(var_esperado)

    out = prop_ultimate_cluster(rows)

    print("TEST 1 -- caso sintetico, 2 estratos x 5 UPM x pesos desiguales:")
    print(f"  p_hat calculado = {out['p_hat']:.12f} (esperado {p_esperado:.12f})")
    print(f"  se calculado    = {out['se']:.12f} (esperado {se_esperado:.12f})")
    print(f"  n_estratos={out['n_estratos']} (esperado 2) "
          f"n_upm_total={out['n_upm_total']} (esperado 5) "
          f"n_estratos_singleton={out['n_estratos_singleton']} (esperado 0)")

    assert abs(out["p_hat"] - p_esperado) < TOL, "p_hat no coincide con la derivacion a mano"
    assert abs(out["se"] - se_esperado) < TOL, "se no coincide con la derivacion a mano"
    assert out["n_estratos"] == 2, "n_estratos"
    assert out["n_upm_total"] == 5, "n_upm_total"
    assert out["n_estratos_singleton"] == 0, "n_estratos_singleton"
    print("  OK -- coincide con la derivacion a mano dentro de tolerancia 1e-9.")


def test_estrato_singleton():
    """Chequeo adyacente, barato: un estrato de una sola UPM no aporta
    varianza -- el propio docstring de svystat.py lo declara ('se
    reportan aparte, no se fuerzan a cero silenciosamente'). Este caso
    verifica que el "cero" que devuelve queda identificado como tal via
    n_estratos_singleton, no como un cero indistinguible de precision real.

    Una UPM, un estrato, tres filas con pesos desiguales:
      (3,1) (5,0) (2,1)  ->  N_hat=10, num=3+0+2=5, p_hat=5/10=0.5
    Una sola UPM en el estrato -> n_h=1 < 2 -> no aporta al sumando de
    varianza (var = 0/N_hat^2 = 0) y se cuenta en n_estratos_singleton.
    """
    rows = [
        ("estrato_solo", "upm_x", 3.0, 1.0),
        ("estrato_solo", "upm_x", 5.0, 0.0),
        ("estrato_solo", "upm_x", 2.0, 1.0),
    ]
    out = prop_ultimate_cluster(rows)

    print("TEST 2 -- estrato de una sola UPM (varianza no estimable):")
    print(f"  p_hat={out['p_hat']:.6f} se={out['se']:.6f} "
          f"n_estratos={out['n_estratos']} n_estratos_singleton={out['n_estratos_singleton']}")

    assert abs(out["p_hat"] - 0.5) < TOL, "p_hat"
    assert out["se"] == 0.0, "se deberia ser exactamente 0.0 (var=0, no NaN ni excepcion)"
    assert out["n_estratos"] == 1, "n_estratos"
    assert out["n_upm_total"] == 1, "n_upm_total"
    assert out["n_estratos_singleton"] == 1, "n_estratos_singleton -- el caso singleton debe quedar marcado"
    print("  OK -- el estrato singleton queda marcado, no escondido en un cero falso.")


if __name__ == "__main__":
    test_caso_sintetico_dos_estratos()
    print()
    test_estrato_singleton()
    print()
    print("TEST 3 -- autochequeo existente del modulo (svystat._caso_conocido):")
    svystat._caso_conocido()
    print()
    print("Los tres casos de este archivo coinciden. Las dos reproducciones")
    print("archivadas (Hito D R7.2 ocho olas; CAL-CONF Fase B ola2) se")
    print("corrieron por separado -- detalle en")
    print("forense/notas/2026-08-04-svystat-casos-referencia.md.")
