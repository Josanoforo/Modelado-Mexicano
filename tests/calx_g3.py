#!/usr/bin/env python3
"""
tests/calx_g3.py — CHEQUEO CAL-X de la ficha CAL-G3, previo a abrir microdatos.

La ficha (Nota 7, punto 9a, celda CAL-X) ordena, textual:

    "antes de estimar nada, se verifica contra los conteos del codebook que
     cada celda del criterio es aritméticamente alcanzable con las tasas base
     observadas. Si alguna no lo es, el criterio se re-declara EN MESA antes
     de abrir microdatos"

Este script hace exactamente eso y nada más. Toda cifra de entrada viene del
MANUAL DE CODIFICACIÓN (documentación publicada), no de microdato: los conteos
de `crh01_1*` y el `folio` de la sección CRH del Libro II de cada ola.

INSUMOS -- declarados sin excepción:
  · SOLO codebook. Ningún .dta se abre aquí, ni por este script ni por la
    sesión que lo escribió antes de correrlo. Las constantes de abajo están
    transcritas a mano desde los PDF y son verificables una por una contra
    ellos (ver "cómo se reproduce").
  · El mapeo categoría->estado NO se decide aquí: se toma de CAL-G3 Adenda 1,
    punto (c), tal como quedó sellado. Este script lo aplica, no lo discute.
  · Los umbrales (RR 1.5, IC95%sup 1.25, banda [0.80, 1.25]) tampoco se
    deciden aquí: son los pre-registrados en 9a/9b. Se PRUEBAN, no se ajustan.

CÓMO SE REPRODUCE, de cero:
  1. Bajar los tres manuales de codificación del Libro II (son públicos y
     están registrados en data/manifiesto.yaml con sha256):
         https://www.ennvih-mxfls.org/assets/ehh02cb_b2.pdf   (ola 1, 2002)
         https://www.ennvih-mxfls.org/assets/ehh05cb_b2.pdf   (ola 2, 2005-06)
         https://www.ennvih-mxfls.org/assets/ehh09cb_b2.pdf   (ola 3, 2009-12)
  2. Extraer los conteos con:
         pdftotext -layout ehh09cb_b2.pdf - | grep -E "^\\s*(folio|crh01_1)"
     El `folio` que precede a `crh01_1a` es el N de la sección CRH; los once
     `crh01_1a`..`crh01_1k` son los conteos por categoría. Deben coincidir con
     el diccionario OLAS de abajo. Si no coinciden, gana el PDF.
  3. python3 tests/calx_g3.py
  No requiere dependencias externas: solo stdlib (math).

Salida: por celda del criterio, ALCANZABLE / NO ALCANZABLE, con la aritmética
que lo sostiene.

EXTENSIÓN 30/jul/2026 -- aritmética de poder sobre el panel completo. La parte
original acotó el techo de discordantes sobre UNA transición (olas 1 y 3); el
panel tiene tres olas, o sea DOS transiciones. La extensión pregunta si
apilarlas mueve CAL-C de inalcanzable a alcanzable, y responde reportando N
EFECTIVO (tras efecto de diseño por conglomeración a nivel hogar), nunca el N
nominal. Añade un supuesto que la parte original no necesitaba y que se declara
aquí: la correlación intra-hogar (ICC) NO se mide -- exigiría microdatos -- se
barre en un rango y se reporta el resultado bajo cada valor. Todo lo demás
sigue igual: sólo codebook, ningún .dta, ninguna estimación, ninguna decisión.
La salida completa está versionada en forense/notas/2026-07-30-calx-g3-salida.txt.
"""

import math

# ---------------------------------------------------------------------------
# Entradas: conteos del manual de codificación, Libro II, sección CRH.
# Fuente por ola (verificado con pdftotext -layout sobre el PDF descargado):
#   ola 1  data/raw/ennvih/doc/ehh02cb_b2.pdf  (folio sección CRH; crh01_1a..k)
#   ola 2  data/raw/ennvih/doc/ehh05cb_b2.pdf
#   ola 3  data/raw/ennvih/doc/ehh09cb_b2.pdf
# ---------------------------------------------------------------------------

OLAS = {
    "ola 1 · 2002": {
        "hogares": 8046,
        "cat": {"1 No tiene ahorros": 6805, "2 Banco": 772, "3 Cooperativa": 26,
                "4 Caja de Ahorro": 217, "5 Tanda": 22, "6 Apartado": 1,
                "7 Amigo/pariente": 20, "8 Afores voluntarias": 28,
                "9 Cajas solidarias": 3, "10 En su casa": 144, "11 Otro": 49},
    },
    "ola 2 · 2005-06": {
        "hogares": 8134,
        "cat": {"1 No tiene ahorros": 7061, "2 Banco": 626, "3 Cooperativa": 30,
                "4 Caja de Ahorro": 219, "5 Tanda": 18, "6 Apartado": 1,
                "7 Amigo/pariente": 6, "8 Afores voluntarias": 21,
                "9 Cajas solidarias": 4, "10 En su casa": 138, "11 Otro": 45},
    },
    "ola 3 · 2009-12": {
        "hogares": 9092,
        "cat": {"1 No tiene ahorros": 7932, "2 Banco": 644, "3 Cooperativa": 30,
                "4 Caja de Ahorro": 172, "5 Tanda": 12, "6 Apartado": 0,
                "7 Amigo/pariente": 14, "8 Afores voluntarias": 13,
                "9 Cajas solidarias": 6, "10 En su casa": 209, "11 Otro": 30},
    },
}

# Mapeo categoría->estado: CAL-G3 Adenda 1, punto (c). No se re-decide aquí.
FORMALES = ["2 Banco", "8 Afores voluntarias"]
INFORMALES = ["3 Cooperativa", "4 Caja de Ahorro", "5 Tanda", "6 Apartado",
              "7 Amigo/pariente", "9 Cajas solidarias", "10 En su casa"]

# Umbrales pre-registrados. NO se ajustan: se prueban.
RR_CAL_A = 1.5          # 9a CAL-A
IC_SUP_CAL_C = 1.25     # 9a CAL-C  y  9b (límite superior)
IC_INF_9B = 0.80        # 9b (límite inferior de la banda de nulo estricto)
Z = 1.959963985         # normal 97.5%


def var_log_rr(p, n1, n0):
    """Varianza aproximada de log(RR) para dos brazos de tamaño n1, n0
    con probabilidad de desenlace p en ambos (escenario del nulo)."""
    return (1.0 - p) / (n1 * p) + (1.0 - p) / (n0 * p)


def n_por_brazo_para_ic(p, ic_sup):
    """n por brazo (brazos iguales) necesario para que, con RR puntual = 1,
    el límite superior del IC95% quede por debajo de `ic_sup`."""
    se_max = math.log(ic_sup) / Z
    # var = 2*(1-p)/(n*p)  <  se_max^2
    return 2.0 * (1.0 - p) / (p * se_max ** 2)


print("=" * 78)
print("CHEQUEO CAL-X · ficha CAL-G3 · insumos = manual de codificación, sin microdato")
print("=" * 78)

resumen = {}

for ola, d in OLAS.items():
    N = d["hogares"]
    c = d["cat"]
    f_sup = sum(c[k] for k in FORMALES)          # cota superior (sin traslape)
    f_inf = max(c[k] for k in FORMALES)          # cota inferior (uno contenido en otro)
    i_sup = sum(c[k] for k in INFORMALES)
    p_sup, p_inf = f_sup / N, f_inf / N

    print(f"\n### {ola} — hogares en la sección CRH: N = {N:,}")
    print(f"  marcas FORMAL (Banco + Afores voluntarias) : {f_sup:,}  "
          f"-> p('algún acceso formal') entre {p_inf:.2%} y {p_sup:.2%}")
    print(f"  marcas INFORMAL (bloque agregado)          : {i_sup:,}")
    print(f"  'No tiene ahorros'                          : {c['1 No tiene ahorros']:,} "
          f"({c['1 No tiene ahorros']/N:.1%})")
    vacias = [k for k in INFORMALES + FORMALES if c[k] <= 30]
    print(f"  categorías con n<=30 (celda propia inevaluable): "
          f"{', '.join(f'{k}={c[k]}' for k in vacias)}")
    resumen[ola] = dict(N=N, p=p_sup, formal=f_sup, informal=i_sup)

print("\n" + "=" * 78)
print("CELDA POR CELDA")
print("=" * 78)

# --- CAL-A -------------------------------------------------------------------
print("\n[CAL-A]  RR >= 1.5 sobre P(mixto o solo formal), IC95% que excluye 1")
print("  Un criterio en RAZÓN tiene techo p_max/p_min, no p_max - p_min.")
print("  RR >= 1.5 exige únicamente p(jefe informal) <= 1/1.5 = 66.67%.")
ok_a = True
for ola, r in resumen.items():
    holgura = 0.6667 / r["p"]
    print(f"    {ola}: p ~ {r['p']:.2%}  <<  66.67%  (holgura {holgura:.0f}x)")
    ok_a &= r["p"] <= 0.6667
print(f"  -> {'ALCANZABLE' if ok_a else 'NO ALCANZABLE'}. "
      "El modo de falla de R3.2 (gate en pp por encima del techo observado)")
print("     NO se repite: es exactamente lo que el punto (7) evitó al ponerlo en razón.")

# --- CAL-B -------------------------------------------------------------------
print("\n[CAL-B]  1 < RR < 1.5, o IC que cruza 1, o confundidor de oferta sin descartar")
print("  -> ALCANZABLE. Es la celda residual: no impone cota de precisión ni de nivel.")

# --- CAL-C y 9b --------------------------------------------------------------
print("\n[CAL-C] y [9b nulo estricto]  RR <= 1 con IC95% de límite superior < 1.25")
print("        (9b además exige el IC95% entero dentro de [0.80, 1.25])")
print("  Estas celdas NO acotan un nivel: acotan una PRECISIÓN. Con RR puntual = 1,")
print("  el IC95% superior cae por debajo de 1.25 sólo si n es suficientemente grande.\n")

ok_c = True
for ola, r in resumen.items():
    p = r["p"]
    n_req = n_por_brazo_para_ic(p, IC_SUP_CAL_C)
    # Techo DURO de hogares discordantes en el desenlace entre dos olas:
    # un hogar sólo puede ser discordante si tiene ahorro formal en exactamente
    # una de las dos olas -> #discordantes <= #(formal en w) + #(formal en w').
    print(f"  {ola}:  p = {p:.2%}")
    print(f"     n por brazo requerido para IC95%sup < 1.25 : {n_req:,.0f}"
          f"   (total {2*n_req:,.0f} hogares con el contraste)")

techo_disc = resumen["ola 1 · 2002"]["formal"] + resumen["ola 3 · 2009-12"]["formal"]
p3 = resumen["ola 3 · 2009-12"]["p"]
n_req3 = n_por_brazo_para_ic(p3, IC_SUP_CAL_C)

print(f"\n  TECHO DURO de hogares discordantes en el desenlace (olas 1 y 3):")
print(f"     <= {resumen['ola 1 · 2002']['formal']:,} + "
      f"{resumen['ola 3 · 2009-12']['formal']:,} = {techo_disc:,} hogares")
print("     (cota flojísima: supone traslape cero y que TODO hogar con ahorro")
print("      formal es panel presente en ambas olas, antes de exigir que además")
print("      cambie la formalidad del jefe, antes de atrición y antes de excluir EE.UU.)")

se_mejor = math.sqrt(var_log_rr(p3, techo_disc / 2, techo_disc / 2))
ic_sup_mejor = math.exp(Z * se_mejor)
print(f"\n  MEJOR IC95% superior alcanzable con ese techo (brazos iguales, RR=1):")
print(f"     SE(log RR) = {se_mejor:.4f}  ->  IC95%sup = {ic_sup_mejor:.3f}")
print(f"     requerido por CAL-C: < {IC_SUP_CAL_C}")
ok_c = ic_sup_mejor < IC_SUP_CAL_C
print(f"  -> {'ALCANZABLE' if ok_c else 'NO ALCANZABLE'}: "
      f"{ic_sup_mejor:.3f} >= {IC_SUP_CAL_C} incluso en el escenario más favorable")
print(f"     que los conteos del codebook permiten construir "
      f"({techo_disc:,} < {2*n_req3:,.0f} necesarios).")

se_req_9b = min(math.log(IC_SUP_CAL_C), -math.log(IC_INF_9B)) / Z
print(f"\n  [9b] banda [0.80, 1.25] exige SE(log RR) < {se_req_9b:.4f}; "
      f"el techo permite {se_mejor:.4f}.")
print(f"  -> NO ALCANZABLE por el mismo motivo.")

print("\n" + "=" * 78)
print("VEREDICTO DEL CHEQUEO")
print("=" * 78)
print("""
CAL-A  : ALCANZABLE.
CAL-B  : ALCANZABLE.
CAL-C  : NO ALCANZABLE por construcción.
9b     : NO ALCANZABLE por construcción (nulo estricto con poder).
CAL-X  : DISPARA — y no sobre la celda que la ficha ya había anticipado.

La ficha ya había declarado caída la celda tanda-sola (n=12). Lo que este
chequeo añade es asimétrico y más grave: con las tasas base del codebook, el
criterio puede CONFIRMAR G3 (CAL-A) pero no puede REFUTARLO (CAL-C / 9b). Un
criterio que sólo admite confirmación no es un falsador. Por el punto 9a, esto
se re-declara EN MESA antes de abrir microdatos, no después.
""")


# =============================================================================
# EXTENSIÓN · 30/jul/2026 — ¿apilar las DOS transiciones del panel mueve CAL-C?
# =============================================================================
#
# Lo de arriba calculó el techo de discordantes sobre UNA transición (olas 1 y 3).
# El panel tiene tres olas, o sea DOS transiciones (1->2 y 2->3), y un diseño de
# efectos fijos dentro-de-unidad usa todas las disponibles, no sólo los extremos.
# Esta sección pregunta si apilarlas mueve CAL-C de inalcanzable a alcanzable.
#
# NO estima nada, NO abre ningún .dta, NO decide nada y NO re-declara ningún
# criterio: es aritmética de poder sobre los mismos conteos del codebook, como
# insumo de la decisión de mesa D-09/D-10, no como su respuesta.
#
# EL PUNTO QUE DECIDE NO ES EL CONTEO BRUTO. Apilar dos transiciones no duplica
# el N efectivo: el mismo hogar aparece en ambas, las observaciones están
# correlacionadas dentro de hogar y los errores estándar exigen clustering a
# nivel hogar. Se reporta N EFECTIVO, nunca el nominal como si fuera poder.

# Correlación intra-hogar: SUPUESTO DECLARADO, no medido. No se puede medir sin
# abrir microdatos, que esta ficha prohíbe en esta fase. Se barre un rango y se
# reporta el resultado bajo cada valor. ICC=0 se incluye como COTA IMPOSIBLE
# (equivaldría a que las dos transiciones del mismo hogar fueran independientes),
# no como valor plausible: para conducta financiera del mismo hogar a tres años
# de distancia, la persistencia empuja el ICC hacia arriba, no hacia cero.
ICC_RANGO = [(0.0, "cota imposible"), (0.2, "bajo"), (0.5, "medio"), (0.8, "alto")]

OBS_POR_HOGAR = 2.0   # dos transiciones por hogar bajo apilamiento


def efecto_diseno(m, icc):
    """Efecto de diseño por conglomeración (Kish): DEFF = 1 + (m-1)*ICC,
    con m = observaciones por conglomerado (aquí, transiciones por hogar)."""
    return 1.0 + (m - 1.0) * icc


def se_log_rr(p, n_total):
    """SE(log RR) con brazos iguales de tamaño n_total/2 cada uno y probabilidad
    de desenlace p en ambos (escenario del nulo, RR puntual = 1)."""
    n = n_total / 2.0
    return math.sqrt(var_log_rr(p, n, n))


def n_requerido(p, se_max):
    """N total (ambos brazos) para que SE(log RR) baje de se_max."""
    return 4.0 * (1.0 - p) / (p * se_max ** 2)


f1 = resumen["ola 1 · 2002"]["formal"]
f2 = resumen["ola 2 · 2005-06"]["formal"]
f3 = resumen["ola 3 · 2009-12"]["formal"]
N1 = resumen["ola 1 · 2002"]["N"]
N2 = resumen["ola 2 · 2005-06"]["N"]
N3 = resumen["ola 3 · 2009-12"]["N"]

SE_REQ = math.log(IC_SUP_CAL_C) / Z          # 9a CAL-C
SE_REQ_9B = min(math.log(IC_SUP_CAL_C), -math.log(IC_INF_9B)) / Z   # 9b

print("=" * 78)
print("EXTENSIÓN · ¿apilar las dos transiciones del panel mueve CAL-C?")
print("=" * 78)

print(f"""
(1) HOGARES CON ACCESO FORMAL EN LAS TRES OLAS (Banco + afores voluntarias,
    mapeo de Adenda 1 (c)), derivados del manual de codificación:

      ola 1 · 2002      {f1:>5,}  de {N1:>6,}   p = {f1/N1:.2%}
      ola 2 · 2005-06   {f2:>5,}  de {N2:>6,}   p = {f2/N2:.2%}
      ola 3 · 2009-12   {f3:>5,}  de {N3:>6,}   p = {f3/N3:.2%}

(2) TECHO DE PARES HOGAR-TRANSICIÓN BAJO APILAMIENTO. Misma lógica generosa
    que el chequeo original: un hogar sólo puede ser discordante en una
    transición si tiene ahorro formal en exactamente una de las dos olas, luego
    #discordantes(w,w') <= #formal(w) + #formal(w').

      transición 1->2   <= {f1:,} + {f2:,} = {f1+f2:,}
      transición 2->3   <= {f2:,} + {f3:,} = {f2+f3:,}
      apiladas          <= {f1+f2+f3+f2:,} pares hogar-transición (NOMINAL)

    La cota es igual de floja que antes, y se declara igual: supone traslape
    cero, supone que TODO hogar con ahorro formal es hogar panel presente en
    ambas olas de cada transición, cuenta a los formales de la ola 2 en las dos
    transiciones, y no descuenta todavía el cambio de formalidad del jefe, ni la
    atrición, ni la exclusión de las observaciones levantadas en EE.UU.""")

nominal_A = (f1 + f2) + (f2 + f3)
print(f"""
(3) EFECTO DE DISEÑO Y N EFECTIVO. El nominal de {nominal_A:,} NO es poder.
    Con {OBS_POR_HOGAR:.0f} transiciones por hogar, DEFF = 1 + (m-1)*ICC = 1 + ICC.
""")
print(f"    {'ICC':>6}  {'':14} {'DEFF':>6}  {'N efectivo':>11}  {'vs. escenario C':>16}")
print("    " + "-" * 62)
for icc, etiq in ICC_RANGO:
    deff = efecto_diseno(OBS_POR_HOGAR, icc)
    neff = nominal_A / deff
    print(f"    {icc:>6.2f}  ({etiq+')':<16} {deff:>6.2f}  {neff:>11,.0f}  "
          f"{neff/(f1+f3)-1:>+15.0%}")

# ---------------------------------------------------------------------------
# (4) MATRIZ CONJUNTA. D-09 y D-10 no son independientes: qué transiciones se
#     pueden apilar depende de cómo se resuelva la armonización de la exposición.
# ---------------------------------------------------------------------------
ESCENARIOS = [
    ("A", "Tres olas, dos transiciones apiladas",
     nominal_A, (f1 + f2 + f3) / (N1 + N2 + N3), True,
     "exige resolver D-10 con imputación de 'ninguna' en 2002"),
    ("B", "Sólo olas 2-3, una transición",
     f2 + f3, (f2 + f3) / (N2 + N3), False,
     "D-10 opción 1, la limpia: descarta la línea basal"),
    ("C", "Olas 1 y 3, una transición",
     f1 + f3, (f1 + f3) / (N1 + N3), False,
     "referencia: lo ya calculado en el chequeo original"),
]

print(f"""
(4) MATRIZ CONJUNTA — mejor IC95% superior alcanzable con RR puntual = 1,
    contra el < {IC_SUP_CAL_C} que exige CAL-C, y SE(log RR) contra el
    < {SE_REQ_9B:.4f} que exige la banda [0.80, 1.25] de 9b.

    p de cada escenario = tasa base agrupada sobre las olas que lo componen.
""")
hdr = (f"    {'esc':<4} {'ICC':>5} {'N nominal':>10} {'N efectivo':>11} "
       f"{'SE':>8} {'IC95%sup':>9}  {'CAL-C':>9}  {'9b':>9}")
print(hdr)
print("    " + "-" * (len(hdr) - 4))

resultados = []
for cod, nombre, nominal, p_esc, apila, _nota in ESCENARIOS:
    for icc, etiq in (ICC_RANGO if apila else [(None, None)]):
        deff = efecto_diseno(OBS_POR_HOGAR, icc) if apila else 1.0
        neff = nominal / deff
        se = se_log_rr(p_esc, neff)
        ic = math.exp(Z * se)
        ok_calc = ic < IC_SUP_CAL_C
        ok_9b = se < SE_REQ_9B
        resultados.append((cod, icc, neff, se, ic, ok_calc, ok_9b))
        print(f"    {cod:<4} {(f'{icc:.2f}' if icc is not None else '  --'):>5} "
              f"{nominal:>10,} {neff:>11,.0f} {se:>8.4f} {ic:>9.3f}  "
              f"{'ALCANZA' if ok_calc else 'no alcanza':>9}  "
              f"{'ALCANZA' if ok_9b else 'no alcanza':>9}")

print("\n    Escenarios (qué decisión de mesa presupone cada uno):")
for cod, nombre, _n, p_esc, _a, nota in ESCENARIOS:
    print(f"      ({cod}) {nombre}  ·  p = {p_esc:.2%}\n          {nota}")

# Discrepancia declarada, no silenciada: el chequeo original usó la p de la ola 3
# sola (7.23%) para el escenario C; esta matriz usa p agrupada por escenario, para
# que las tres filas sean comparables entre sí. Cambia el número de C, no su lado
# del umbral. Se reportan los dos.
p3_sola = resumen["ola 3 · 2009-12"]["p"]
se_c_orig = se_log_rr(p3_sola, f1 + f3)
print(f"""
    NOTA DE CONVENCIÓN, declarada porque cambia una cifra ya publicada:
      el chequeo original evaluó el escenario C con la p de la ola 3 SOLA
      ({p3_sola:.2%}) y obtuvo IC95%sup = {math.exp(Z*se_c_orig):.3f}. Esta matriz lo evalúa
      con p agrupada sobre las olas 1 y 3 ({(f1+f3)/(N1+N3):.2%}) y obtiene
      {math.exp(Z*se_log_rr((f1+f3)/(N1+N3), f1+f3)):.3f}, para que las tres filas sean comparables entre sí.
      Misma cota de discordantes ({f1+f3:,}), distinta convención de p. No cambia
      el lado del umbral en ninguna de las dos: ambas quedan por encima de {IC_SUP_CAL_C}.""")

# ---------------------------------------------------------------------------
mejor = min(resultados, key=lambda r: r[4])
ic_c = [r[4] for r in resultados if r[0] == 'C'][0]
n_req_A = n_requerido(ESCENARIOS[0][3], SE_REQ)
ganancia_nominal = nominal_A / (f1 + f3) - 1
neff_alto = nominal_A / efecto_diseno(OBS_POR_HOGAR, 0.8)
ganancia_alta = neff_alto / (f1 + f3) - 1

print("\n" + "=" * 78)
print("HALLAZGO — se reporta, no se concluye")
print("=" * 78)
print(f"""
El mejor caso de toda la matriz es el escenario {mejor[0]} con ICC = {mejor[1]:.2f}
(la cota imposible), y da IC95%sup = {mejor[4]:.3f}. El umbral de CAL-C es
< {IC_SUP_CAL_C}. NO alcanza.

Apilar las dos transiciones NO mueve CAL-C de inalcanzable a alcanzable, y el
resultado no depende del supuesto de correlación: falla incluso con ICC = 0,
que es una cota que ningún panel real alcanza. Al escenario A le faltarían
{n_req_A:,.0f} pares hogar-transición y su techo nominal es {nominal_A:,}.

EL EFECTO DE DISEÑO SE COME LA GANANCIA. Apilar sube el conteo nominal
{ganancia_nominal:+.0%} ({f1+f3:,} -> {nominal_A:,}), pero eso no es poder:
con ICC alto (0.8) el N efectivo queda en {neff_alto:,.0f}, apenas
{ganancia_alta:+.0%} sobre el escenario C. La ganancia bruta es real y la
ganancia efectiva es marginal.

Lo que sí cambia, y se reporta porque es material: el margen se estrecha.
El escenario C, la referencia de una sola transición, da IC95%sup = {ic_c:.3f}
en esta matriz; el mejor caso la baja a {mejor[4]:.3f}. Sigue del lado inalcanzable del umbral,
pero la distancia deja de ser holgada.

VEREDICTO DE CAL-X: SIN CAMBIO en ninguna celda. CAL-A y CAL-B siguen
alcanzables; CAL-C y 9b siguen NO alcanzables por construcción, ahora
verificado sobre las dos transiciones del panel y no sólo sobre una.

Esto es insumo de D-09 y D-10, no su resolución. No se recomienda escenario,
no se re-declara ningún criterio, y la decisión de mesa sigue abierta.
""")
