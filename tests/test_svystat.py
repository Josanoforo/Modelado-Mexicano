#!/usr/bin/env python3
"""Validacion independiente de tests/svystat.py -- prop_ultimate_cluster,
diff_ultimate_cluster, did_ultimate_cluster.

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
  3. test_generador_no_falla_en_silencio() -- mismo dataset de (1), pasado
     como GENERADOR en vez de lista. prop_ultimate_cluster() recorre `rows`
     dos veces (N_hat/num, y despues el bloque de UPM); un generador se
     agota en el primer recorrido y el segundo lo veia vacio, sin excepcion
     -- doble recorrido, defecto silencioso (ENCARGO MT-mantenimiento,
     5/ago/2026). svystat.py ahora materializa `rows = list(rows)` al
     entrar; este caso exige que el resultado sobre un generador sea
     EXACTAMENTE igual al de la lista del mismo dataset.
  4. Una llamada a svystat._caso_conocido() (el autochequeo del modulo,
     ya existente) como cuarta confirmacion, gratis.

Que NO hay aqui -- las dos reproducciones archivadas (Hito D R7.2 ocho
olas; CAL-CONF Fase B ola2) se corrieron por separado, re-ejecutando los
scripts YA COMMITEADOS (tests/hitoD_r7_2_ocho_olas.py, rama
sesion/hitoD-r7-2-delito-sin-seguro; tests/cal_conf_faseb_ola2.py, main)
contra el microdato real -- no tiene sentido reimplementar esos pipelines
aqui. Detalle completo, con los tres resultados contra la cifra archivada,
en forense/notas/2026-08-04-svystat-casos-referencia.md.

ENCARGO B (12/ago/2026) anade diff_ultimate_cluster/did_ultimate_cluster
a svystat.py (estimador de contraste T-C dentro de una ola, y DiD entre
dos olas independientes -- desbloquea el commit 2 de E4c sobre
R5.1-D2). Casos nuevos, con la derivacion completa en
forense/notas/2026-08-12-estimador-contraste.md:
  5. test_diff_caso1_srs_forma_cerrada() -- SRS, T/C disjuntos, forma
     cerrada exacta. Tolerancia 1e-9, igual que los casos de prop_*.
  6. test_diff_caso2_coherencia_con_prop() -- diff_ultimate_cluster no
     contradice a prop_ultimate_cluster donde se solapan. Tolerancia
     1e-12. Ver docstring del test: el encargo pedia literalmente "todas
     las unidades en T, ninguna en C", que choca con la regla de grupo
     vacio (N_hat_C=0 -> None) que el mismo encargo exige -- contradiccion
     real, resuelta y documentada, no ignorada.
  7. test_diff_caso3_covarianza_importa() -- EL CASO QUE JUSTIFICA LA
     FUNCION. T y C correlacionados dentro de UPM; diff_ultimate_cluster
     y sqrt(var_T+var_C) deben diferir de forma visible, y el test lo
     afirma.
  8. test_diff_caso4_invariancia_fuera_de_grupo() -- opcional del
     encargo, sale barato: filas grupo=None no cambian d_hat; su efecto
     sobre se es el que la formula predice (UPM nueva en estrato
     existente), no cero por casualidad.
  9. test_did_ultimate_cluster_coherencia() -- no es uno de los tres
     casos que el encargo exige para diff_ultimate_cluster, pero
     did_ultimate_cluster es la otra funcion nueva de este mismo acto y
     quedaria sin ejercitar si no se prueba aqui: verifica theta_hat,
     la suma de varianzas entre olas, que los contadores de singleton no
     se colapsan entre olas, y que None se propaga si una ola tiene
     grupo vacio.

Corre solo, y ademas es un step bloqueante propio en CI (ENCARGO
MT-mantenimiento, 5/ago/2026: `.github/workflows/verify.yml`, standalone,
sin depender de check.py):

    python3 tests/test_svystat.py
"""
import math
import sys

sys.path.insert(0, "tests")
import svystat  # noqa: E402
from svystat import prop_ultimate_cluster, diff_ultimate_cluster, did_ultimate_cluster  # noqa: E402

TOL = 1e-9  # misma tolerancia que el autochequeo del propio modulo
            # (_caso_conocido); generosa frente a la precision real de
            # float64 (~1e-16) -- cualquier desviacion real la atrapa
            # con margen de sobra.
TOL_STRICT = 1e-12  # exigida por el Caso 2 del ENCARGO B (coherencia
                     # exacta contra prop_ultimate_cluster).


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


def test_generador_no_falla_en_silencio():
    """rows como GENERADOR, no lista -- prop_ultimate_cluster() la recorre
    dos veces (N_hat/num arriba, bloque de UPM abajo); un generador se agota
    en el primer recorrido y el segundo lo ve vacio SIN lanzar excepcion --
    el defecto exacto que motiva este caso (ENCARGO MT-mantenimiento,
    5/ago/2026: `rows = list(rows)` al entrar a la funcion). Mismo dataset
    que test_caso_sintetico_dos_estratos(), para comparar contra un
    resultado ya conocido en vez de derivar un segundo esperado a mano.
    """
    rows_lista = [
        ("A", "A1", 2.0, 1.0), ("A", "A1", 3.0, 0.0),
        ("A", "A2", 1.0, 1.0), ("A", "A2", 1.0, 1.0), ("A", "A2", 2.0, 0.0),
        ("A", "A3", 4.0, 0.0), ("A", "A3", 2.0, 1.0),
        ("B", "B1", 6.0, 1.0), ("B", "B1", 2.0, 0.0),
        ("B", "B2", 2.0, 0.0), ("B", "B2", 4.0, 1.0), ("B", "B2", 3.0, 1.0),
    ]

    def rows_generador():
        for r in rows_lista:
            yield r

    out_lista = prop_ultimate_cluster(rows_lista)
    out_generador = prop_ultimate_cluster(rows_generador())

    print("TEST 3 -- mismo dataset via GENERADOR, no lista:")
    print(f"  p_hat lista={out_lista['p_hat']:.12f} generador={out_generador['p_hat']:.12f}")
    print(f"  se   lista={out_lista['se']:.12f} generador={out_generador['se']:.12f}")

    assert out_generador == out_lista, (
        "prop_ultimate_cluster(generador) debe dar EXACTAMENTE el mismo dict "
        "que prop_ultimate_cluster(lista) del mismo dataset -- si difiere, el "
        "doble recorrido volvio a romperse en silencio")
    print("  OK -- resultado sobre generador identico al de la lista.")


def test_diff_caso1_srs_forma_cerrada():
    """Caso 1 del ENCARGO B -- forma cerrada exacta, SRS.

    Un solo estrato, una UPM por observacion, pesos uniformes w=1, T y C
    disjuntos, ninguna unidad fuera de grupo. Con una UPM por observacion,
    z_bar_h=0 (mismo argumento que el caso degenerado de prop_ultimate_
    cluster: bajo SRS el promedio del residual ponderado dentro de cada
    grupo es cero por construccion de p_T/p_C), asi que la formula del
    docstring de diff_ultimate_cluster colapsa a:

      var(d) = [n/(n-1)] * [ p_T(1-p_T)/n_T + p_C(1-p_C)/n_C ]   con n=n_T+n_C

    Dataset: T con y=[1,1,0,1] (n_T=4, p_T=3/4); C con y=[0,1,0] (n_C=3,
    p_C=1/3).

      d_esperado = 3/4 - 1/3 = 5/12
      n = 7
      var_esperado = (7/6) * [ (3/4)(1/4)/4 + (1/3)(2/3)/3 ]
                   = (7/6) * [ 3/64 + 2/27 ]
                   = (7/6) * (81/1728 + 128/1728)
                   = (7/6) * (209/1728)
                   = 1463/10368
      se_esperado = sqrt(1463/10368)
    """
    rows = [
        ("unico", "upmT0", 1.0, 1.0, "T"), ("unico", "upmT1", 1.0, 1.0, "T"),
        ("unico", "upmT2", 1.0, 0.0, "T"), ("unico", "upmT3", 1.0, 1.0, "T"),
        ("unico", "upmC0", 1.0, 0.0, "C"), ("unico", "upmC1", 1.0, 1.0, "C"),
        ("unico", "upmC2", 1.0, 0.0, "C"),
    ]
    d_esperado = 3 / 4 - 1 / 3
    var_esperado = (7 / 6) * (3 / 64 + 2 / 27)
    se_esperado = math.sqrt(var_esperado)

    out = diff_ultimate_cluster(rows)

    print("TEST 5 -- diff Caso 1, SRS forma cerrada (T/C disjuntos, un solo estrato):")
    print(f"  d_hat calculado = {out['d_hat']:.12f} (esperado {d_esperado:.12f})")
    print(f"  se calculado    = {out['se']:.12f} (esperado {se_esperado:.12f})")

    assert abs(out["d_hat"] - d_esperado) < TOL, "d_hat no coincide con la forma cerrada"
    assert abs(out["se"] - se_esperado) < TOL, "se no coincide con la forma cerrada"
    assert out["n_estratos_singleton"] == 0, "n_estratos_singleton"
    print("  OK -- coincide con la forma cerrada dentro de tolerancia 1e-9.")


def test_diff_caso2_coherencia_con_prop():
    """Caso 2 del ENCARGO B -- coherencia con el estimador que ya existe.

    El encargo pide literalmente "todas las unidades en T y ninguna en
    C". Tomado al pie de la letra eso es N_hat_C=0, que la decision de
    diseno 4 de diff_ultimate_cluster (grupo vacio -> None, exigida por
    el mismo encargo) convierte en None -- None no es igual a ningun
    d_hat/se numerico. Contradiccion real entre dos instrucciones del
    mismo encargo, verificada antes de escribir este test (no solo
    argumentada) y documentada en
    forense/notas/2026-08-12-estimador-contraste.md S5.1.

    Resolucion: se mantiene la decision 4 tal como el encargo la dicta
    (protege un caso real: una ola sin ningun caso en un grupo no deberia
    dar un numero que se vea valido) y se adapta el Caso 2 para probar la
    MISMA propiedad -- que el lado T de diff_ultimate_cluster es
    identico, formula por formula, a prop_ultimate_cluster -- sin chocar
    con esa decision: se anade UNA fila a C, en un estrato propio de una
    sola UPM (n_h=1, saltada por la politica de singleton) con y=0. Con
    esa construccion N_hat_C>0 (no dispara el None), p_C=0/w=0 exacto
    (d_hat=p_T-0=p_T), y la UPM de C no aporta nada a var(d) por ser
    singleton -- d_hat y se deben coincidir con prop_ultimate_cluster
    sobre las filas de T a 1e-12, la tolerancia que pide el encargo.

    Mismo dataset de T que test_caso_sintetico_dos_estratos() (ya
    validado a mano ahi: p_hat=19/32, se=sqrt(313/262144)).
    """
    rows_T_4tupla = [
        ("A", "A1", 2.0, 1.0), ("A", "A1", 3.0, 0.0),
        ("A", "A2", 1.0, 1.0), ("A", "A2", 1.0, 1.0), ("A", "A2", 2.0, 0.0),
        ("A", "A3", 4.0, 0.0), ("A", "A3", 2.0, 1.0),
        ("B", "B1", 6.0, 1.0), ("B", "B1", 2.0, 0.0),
        ("B", "B2", 2.0, 0.0), ("B", "B2", 4.0, 1.0), ("B", "B2", 3.0, 1.0),
    ]
    out_prop = prop_ultimate_cluster(rows_T_4tupla)

    rows_diff = [(est, upm, w, y, "T") for est, upm, w, y in rows_T_4tupla]
    rows_diff.append(("ZZ_C_SINGLETON", "upm_c0", 1.0, 0.0, "C"))
    out_diff = diff_ultimate_cluster(rows_diff)

    print("TEST 6 -- diff Caso 2, coherencia con prop_ultimate_cluster (T puro + 1 fila C singleton):")
    print(f"  d_hat={out_diff['d_hat']:.12f} p_hat(prop)={out_prop['p_hat']:.12f}")
    print(f"  se(diff)={out_diff['se']:.12f} se(prop)={out_prop['se']:.12f}")

    assert abs(out_diff["d_hat"] - out_prop["p_hat"]) < TOL_STRICT, "d_hat no coincide con p_hat de prop_ultimate_cluster"
    assert abs(out_diff["se"] - out_prop["se"]) < TOL_STRICT, "se no coincide con el de prop_ultimate_cluster"
    assert out_diff["n_estratos_singleton"] == 1, "la fila C debe quedar marcada como singleton, no escondida"
    print("  OK -- diff_ultimate_cluster no contradice a prop_ultimate_cluster donde se solapan (1e-12).")


def test_diff_caso3_covarianza_importa():
    """Caso 3 del ENCARGO B -- EL CASO QUE JUSTIFICA LA FUNCION.

    T y C correlacionados dentro de UPM (8 UPM, pesos desiguales,
    correlacion positiva pero NO perfecta -- una UPM rompe el patron a
    proposito; con correlacion perfecta se_diff da exactamente 0.0, caso
    matematicamente correcto pero demasiado degenerado para ilustrar el
    punto general). Se compara diff_ultimate_cluster (que SI ve la
    covarianza, via el residual linealizado compartido por UPM) contra
    sqrt(var_T+var_C) usando prop_ultimate_cluster sobre cada grupo POR
    SEPARADO (que asume covarianza cero, el error que este acto existe
    para evitar). Deben diferir de forma visible -- se afirma, no solo se
    reporta.
    """
    rows = [
        ("s", "upm1", 3.0, 1.0, "T"), ("s", "upm1", 2.0, 1.0, "C"),
        ("s", "upm2", 2.0, 1.0, "T"), ("s", "upm2", 4.0, 1.0, "C"),
        ("s", "upm3", 5.0, 1.0, "T"), ("s", "upm3", 1.0, 0.0, "C"),  # rompe el patron
        ("s", "upm4", 1.0, 0.0, "T"), ("s", "upm4", 3.0, 0.0, "C"),
        ("s", "upm5", 4.0, 0.0, "T"), ("s", "upm5", 2.0, 0.0, "C"),
        ("s", "upm6", 2.0, 0.0, "T"), ("s", "upm6", 5.0, 0.0, "C"),
        ("s", "upm7", 3.0, 1.0, "T"), ("s", "upm7", 1.0, 1.0, "C"),
        ("s", "upm8", 6.0, 1.0, "T"), ("s", "upm8", 3.0, 1.0, "C"),
    ]
    out_diff = diff_ultimate_cluster(rows)

    rows_T = [(est, upm, w, y) for est, upm, w, y, grupo in rows if grupo == "T"]
    rows_C = [(est, upm, w, y) for est, upm, w, y, grupo in rows if grupo == "C"]
    out_T = prop_ultimate_cluster(rows_T)
    out_C = prop_ultimate_cluster(rows_C)
    se_suma_ingenua = math.sqrt(out_T["se"] ** 2 + out_C["se"] ** 2)

    print("TEST 7 -- diff Caso 3, la covarianza importa (T/C correlacionados dentro de UPM):")
    print(f"  p_T={out_diff['p_T']:.6f} p_C={out_diff['p_C']:.6f} d_hat={out_diff['d_hat']:.6f}")
    print(f"  se(diff_ultimate_cluster, con covarianza) = {out_diff['se']:.12f}")
    print(f"  sqrt(var_T+var_C) (ingenuo, covarianza=0)  = {se_suma_ingenua:.12f}")

    assert abs(out_diff["se"] - se_suma_ingenua) > 0.05, (
        "el SE con covarianza y el SE que asume covarianza cero deben diferir "
        "de forma visible -- si no difieren, el dataset no esta ejerciendo la "
        "covarianza y el caso no prueba lo que dice probar")
    print("  OK -- difieren de forma visible: sumar varianzas SI habria dado un SE distinto.")


def test_diff_caso4_invariancia_fuera_de_grupo():
    """Caso 4 (opcional) del ENCARGO B -- invariancia a unidades fuera de grupo.

    Anadir filas grupo=None no debe cambiar d_hat (no aportan a los
    numeradores/denominadores de T o C). Dos variantes, para separar "no
    cambia nada" de "no cambia por casualidad":
      (a) grupo=None en una UPM que YA es de T -- z_i=0 se suma a una UPM
          que ya estaba; d_hat y se identicos al caso base, bit a bit.
      (b) grupo=None en UPM NUEVAS dentro de estratos ya existentes --
          d_hat identico, pero se SI cambia (mas UPM en el estrato mueve
          m_h, z_bar_h y la suma de cuadrados) -- el efecto que la
          formula predice, no un cero por casualidad.
    """
    rows_base = [
        ("A", "A1", 2.0, 1.0, "T"), ("A", "A1", 3.0, 0.0, "T"),
        ("A", "A2", 1.0, 1.0, "T"), ("A", "A2", 1.0, 1.0, "T"), ("A", "A2", 2.0, 0.0, "T"),
        ("A", "A3", 4.0, 0.0, "C"), ("A", "A3", 2.0, 1.0, "C"),
        ("B", "B1", 6.0, 1.0, "C"), ("B", "B1", 2.0, 0.0, "C"),
        ("B", "B2", 2.0, 0.0, "T"), ("B", "B2", 4.0, 1.0, "T"), ("B", "B2", 3.0, 1.0, "T"),
    ]
    out_base = diff_ultimate_cluster(rows_base)

    rows_none_en_upm_existente = rows_base + [("A", "A1", 10.0, 1.0, None)]
    out_a = diff_ultimate_cluster(rows_none_en_upm_existente)

    rows_none_en_upm_nueva = rows_base + [
        ("A", "A4_none", 5.0, 1.0, None), ("A", "A4_none", 5.0, 0.0, None),
        ("B", "B3_none", 3.0, 1.0, None),
    ]
    out_b = diff_ultimate_cluster(rows_none_en_upm_nueva)

    print("TEST 8 -- diff Caso 4 (opcional), invariancia a filas grupo=None:")
    print(f"  base:                  d_hat={out_base['d_hat']:.12f} se={out_base['se']:.12f}")
    print(f"  None en UPM existente: d_hat={out_a['d_hat']:.12f} se={out_a['se']:.12f}")
    print(f"  None en UPM nueva:     d_hat={out_b['d_hat']:.12f} se={out_b['se']:.12f}")

    assert out_a["d_hat"] == out_base["d_hat"], "d_hat no deberia cambiar con None en UPM existente"
    assert out_a["se"] == out_base["se"], "se no deberia cambiar con None en UPM existente (aporta z_i=0 a una UPM que ya estaba)"
    assert out_b["d_hat"] == out_base["d_hat"], "d_hat no deberia cambiar con None en UPM nueva"
    assert out_b["se"] != out_base["se"], (
        "se SI deberia cambiar con None en UPM nueva (cambia m_h del estrato) "
        "-- si no cambia, la invariancia es sospechosamente completa")
    print("  OK -- d_hat invariante en ambos casos; se invariante solo cuando no cambia la estructura de UPM.")


def test_did_ultimate_cluster_coherencia():
    """Chequeo adicional, no uno de los tres casos exigidos por el encargo
    para diff_ultimate_cluster, pero did_ultimate_cluster es la otra
    funcion nueva de este mismo acto y quedaria sin ejercitar si no se
    prueba aqui.

    Dos olas independientes (datasets de los Casos 1 y 3 de arriba, sin
    relacion sustantiva entre si -- solo para tener dos resultados de
    diff_ultimate_cluster ya conocidos que combinar). Verifica:
      - theta_hat = d_post - d_pre
      - se = sqrt(se_pre^2 + se_post^2) (suma de varianzas entre olas,
        valida SOLO porque son independientes -- ver docstring de
        did_ultimate_cluster)
      - los contadores de singleton de cada ola se reportan por separado,
        sin colapsar (una ola con singleton, la otra sin)
      - None se propaga si una de las dos olas tiene grupo vacio
    """
    rows_pre = [
        ("unico", "upmT0", 1.0, 1.0, "T"), ("unico", "upmT1", 1.0, 1.0, "T"),
        ("unico", "upmT2", 1.0, 0.0, "T"), ("unico", "upmT3", 1.0, 1.0, "T"),
        ("unico", "upmC0", 1.0, 0.0, "C"), ("unico", "upmC1", 1.0, 1.0, "C"),
        ("unico", "upmC2", 1.0, 0.0, "C"),
    ]
    rows_post = [
        ("s", "upm1", 3.0, 1.0, "T"), ("s", "upm1", 2.0, 1.0, "C"),
        ("s", "upm2", 2.0, 1.0, "T"), ("s", "upm2", 4.0, 1.0, "C"),
        ("s", "upm3", 5.0, 1.0, "T"), ("s", "upm3", 1.0, 0.0, "C"),
        ("s", "upm4", 1.0, 0.0, "T"), ("s", "upm4", 3.0, 0.0, "C"),
        ("s", "upm5", 4.0, 0.0, "T"), ("s", "upm5", 2.0, 0.0, "C"),
        ("s", "upm6", 2.0, 0.0, "T"), ("s", "upm6", 5.0, 0.0, "C"),
        ("s", "upm7", 3.0, 1.0, "T"), ("s", "upm7", 1.0, 1.0, "C"),
        ("s", "upm8", 6.0, 1.0, "T"), ("s", "upm8", 3.0, 1.0, "C"),
    ]
    out_pre = diff_ultimate_cluster(rows_pre)
    out_post = diff_ultimate_cluster(rows_post)
    out_did = did_ultimate_cluster(rows_pre, rows_post)

    theta_esperado = out_post["d_hat"] - out_pre["d_hat"]
    se_esperado = math.sqrt(out_pre["se"] ** 2 + out_post["se"] ** 2)

    print("TEST 9 -- did_ultimate_cluster, coherencia con dos llamadas a diff_ultimate_cluster:")
    print(f"  theta_hat={out_did['theta_hat']:.12f} (esperado {theta_esperado:.12f})")
    print(f"  se={out_did['se']:.12f} (esperado sqrt(se_pre^2+se_post^2)={se_esperado:.12f})")

    assert abs(out_did["theta_hat"] - theta_esperado) < TOL_STRICT, "theta_hat"
    assert abs(out_did["se"] - se_esperado) < TOL_STRICT, "se"
    assert out_did["d_pre"] == out_pre["d_hat"], "d_pre"
    assert out_did["d_post"] == out_post["d_hat"], "d_post"
    assert out_did["n_estratos_singleton_pre"] == out_pre["n_estratos_singleton"], "singleton_pre"
    assert out_did["n_estratos_singleton_post"] == out_post["n_estratos_singleton"], "singleton_post"

    out_did_vacio = did_ultimate_cluster([], rows_post)
    assert out_did_vacio is None, "did_ultimate_cluster debe devolver None si una ola tiene grupo vacio"
    print("  OK -- theta_hat, se y contadores de singleton por ola coinciden; None se propaga en grupo vacio.")


if __name__ == "__main__":
    test_caso_sintetico_dos_estratos()
    print()
    test_estrato_singleton()
    print()
    test_generador_no_falla_en_silencio()
    print()
    print("TEST 4 -- autochequeo existente del modulo (svystat._caso_conocido):")
    svystat._caso_conocido()
    print()
    test_diff_caso1_srs_forma_cerrada()
    print()
    test_diff_caso2_coherencia_con_prop()
    print()
    test_diff_caso3_covarianza_importa()
    print()
    test_diff_caso4_invariancia_fuera_de_grupo()
    print()
    test_did_ultimate_cluster_coherencia()
    print()
    print("Los nueve casos de este archivo coinciden. Las dos reproducciones")
    print("archivadas (Hito D R7.2 ocho olas; CAL-CONF Fase B ola2) se")
    print("corrieron por separado -- detalle en")
    print("forense/notas/2026-08-04-svystat-casos-referencia.md. Derivacion")
    print("completa de diff_ultimate_cluster/did_ultimate_cluster en")
    print("forense/notas/2026-08-12-estimador-contraste.md.")
