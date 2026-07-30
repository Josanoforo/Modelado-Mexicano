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
