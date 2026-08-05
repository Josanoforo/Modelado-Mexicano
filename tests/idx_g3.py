#!/usr/bin/env python3
"""
tests/idx_g3.py — CHEQUEO ID-X de la ficha borrador `ID-G3` (Encargo S2-IDG3, Tarea 2).

Robustece la condición (4) de sello de la ficha
(`forense/notas/2026-08-04-e-mxfls-ficha-borrador.md`, Paso 2(8), fila `ID-X`)
con el MISMO barrido de escenarios (ICC × pares de olas) que `tests/calx_g3.py`
aplicó al desenlace `CRH01` de `CAL-G3`. La ficha, tal como quedó redactada,
calculó `ID-X` con UN SOLO escenario -- la cota más floja posible sobre olas
2-3 (IC95%sup = 1.237, cruza el <1.25 por 0.013) -- sin el barrido de
supuestos de ICC ni de pares de olas que `calx_g3.py` sí corrió para `CRH`.
`forense/notas/2026-08-05-s-idg3-verificacion-no-sello.md` §2(4) señaló esto,
sin suavizarlo, como el hallazgo que cualquier acto que retome la ficha debe
resolver antes de confiar en `ID-C` como desenlace practicable. Este script
es esa extensión.

INSUMOS -- declarados sin excepción:
  · Cero microdato. Cero apertura NUEVA de documento: los conteos de `ah03h`
    de abajo son los que la propia ficha borrador ya publicó y citó en su
    Paso 1 (tabla de tasas base), fuente `ehh02cb_b2.pdf:1104-1106`,
    `ehh05cb_b2.pdf:1310-1312`, `ehh09cb_b2.pdf:1430-1432` (extraídos con
    `pdftotext -layout`, ver ficha borrador líneas 68-74). Este script los
    transcribe, no los re-deriva.
  · Los umbrales (IC95%sup < 1.25 de `ID-C`/`ID-9b`) tampoco se deciden aquí:
    son los pre-registrados en la ficha, Paso 2(7)-(8) ("idénticos en forma
    a los de CAL-G3 ... reutilizados por continuidad metodológica"). Se
    PRUEBAN, no se ajustan.
  · La fórmula de varianza de log(RR), el efecto de diseño DEFF = 1+(m-1)*ICC
    y el rango de ICC barrido ([0.0, 0.2, 0.5, 0.8], con 0.0 declarado "cota
    imposible", no valor plausible) son los MISMOS que `tests/calx_g3.py`
    usa para `CRH` -- no se reinventan, se reutilizan verbatim.

QUÉ CAMBIA RESPECTO A `calx_g3.py` (declarado, porque `ID-G3` no es `CAL-G3`):
  · El desenlace es binario de item único (`ah03h`: Sí/No), no requiere el
    mapeo categoría->estado de Adenda 1 que `CRH01` exigió: "Sí" es
    directamente el estado positivo.
  · `ID-G3` restringe su DISEÑO DE IDENTIFICACIÓN a olas 2-3 únicamente
    (hereda D-10 vía incomparabilidad de `TB33` en ola 1 -- ficha borrador
    §2). Por eso el escenario "B" (solo olas 2-3) es el ÚNICO diseño
    estructuralmente válido para esta ficha -- es literalmente el cálculo
    que la ficha ya publicó como `ID-X` (se reproduce aquí para verificar
    que este script coincide con esa cifra, no para repetirla como hallazgo
    nuevo). Los escenarios "A" (apilar dos transiciones) y "C" (olas 1 y 3)
    NO son diseños que esta ficha pueda ejecutar -- el módulo `TB` de ola 1
    no es comparable -- se calculan de todos modos, exactamente como
    `calx_g3.py` conservó su propio escenario "C" (olas 1,3) como
    REFERENCIA aritmética aun después de que D-10 decidiera "B" (olas 2-3)
    para `CRH`. Sirven para acotar cuánto se mueve el gate bajo supuestos
    más/menos generosos, no para proponer un diseño alterno.

CÓMO SE REPRODUCE, de cero:
  1. Los mismos tres manuales de codificación que `calx_g3.py` usa (Libro II,
     sección de activos del hogar, ítem `ah03h`), ya registrados en
     `data/manifiesto.yaml` con sha256:
         https://www.ennvih-mxfls.org/assets/ehh02cb_b2.pdf   (ola 1, 2002)
         https://www.ennvih-mxfls.org/assets/ehh05cb_b2.pdf   (ola 2, 2005-06)
         https://www.ennvih-mxfls.org/assets/ehh09cb_b2.pdf   (ola 3, 2009-12)
  2. Extraer los conteos con:
         pdftotext -layout ehh09cb_b2.pdf - | grep -E "^\\s*ah03h"
     Deben coincidir con la tabla en la ficha borrador (líneas 69-72) y con
     el diccionario OLAS de abajo. Si no coinciden, gana el PDF.
  3. python3 tests/idx_g3.py
  No requiere dependencias externas: solo stdlib (math).

NO estima nada, NO abre ningún .dta, NO decide nada y NO re-declara ningún
criterio, NO edita `tests/calx_g3.py` (su comportamiento y salida para `CRH`
quedan intactos -- verificable corriendo ambos scripts y comparando).
"""

import math

# ---------------------------------------------------------------------------
# Entradas: conteos de ah03h ("Sí" = tenencia de Activos Financieros/AFORE
# del hogar), Libro II, ya publicados y citados por la ficha borrador
# (líneas 68-74). Transcritos aquí, no re-derivados.
# ---------------------------------------------------------------------------

OLAS = {
    "ola 1 · 2002": {"si": 1332, "no": 6708, "N": 8040},
    "ola 2 · 2005-06": {"si": 1117, "no": 7015, "N": 8132},
    "ola 3 · 2009-12": {"si": 1136, "no": 7909, "N": 9045},
}

for _ola, _d in OLAS.items():
    assert _d["si"] + _d["no"] == _d["N"], f"{_ola}: Sí+No != Total"

# Umbral pre-registrado por la ficha (Paso 2(8), fila ID-C/ID-9b). NO se
# ajusta: se prueba.
IC_SUP_ID_C = 1.25
Z = 1.959963985  # normal 97.5%


def var_log_rr(p, n1, n0):
    """Misma fórmula que calx_g3.py: varianza aproximada de log(RR) para dos
    brazos de tamaño n1, n0 con probabilidad de desenlace p en ambos
    (escenario del nulo)."""
    return (1.0 - p) / (n1 * p) + (1.0 - p) / (n0 * p)


def se_log_rr(p, n_total):
    """Misma fórmula que calx_g3.py: SE(log RR) con brazos iguales de tamaño
    n_total/2 cada uno y probabilidad de desenlace p en ambos."""
    n = n_total / 2.0
    return math.sqrt(var_log_rr(p, n, n))


def efecto_diseno(m, icc):
    """Misma fórmula que calx_g3.py: DEFF = 1 + (m-1)*ICC, con m =
    observaciones por conglomerado."""
    return 1.0 + (m - 1.0) * icc


# Mismo rango de ICC que calx_g3.py barrió para CRH. ICC=0 declarado "cota
# imposible" (no valor plausible), igual que allá.
ICC_RANGO = [(0.0, "cota imposible"), (0.2, "bajo"), (0.5, "medio"), (0.8, "alto")]
OBS_POR_HOGAR = 2.0  # dos transiciones por hogar bajo apilamiento (mismo m que calx_g3.py)

print("=" * 78)
print("CHEQUEO ID-X · ficha borrador ID-G3 · desenlace ah03h · insumos = codebook")
print("(mismo barrido de ICC y pares de olas que tests/calx_g3.py aplicó a CRH)")
print("=" * 78)

f1, N1 = OLAS["ola 1 · 2002"]["si"], OLAS["ola 1 · 2002"]["N"]
f2, N2 = OLAS["ola 2 · 2005-06"]["si"], OLAS["ola 2 · 2005-06"]["N"]
f3, N3 = OLAS["ola 3 · 2009-12"]["si"], OLAS["ola 3 · 2009-12"]["N"]

print(f"""
Tasas base ah03h ('Sí'), por ola:
  ola 1 · 2002      {f1:>5,}  de {N1:>6,}   p = {f1/N1:.2%}
  ola 2 · 2005-06   {f2:>5,}  de {N2:>6,}   p = {f2/N2:.2%}
  ola 3 · 2009-12   {f3:>5,}  de {N3:>6,}   p = {f3/N3:.2%}
""")

ESCENARIOS = [
    ("A", "Apilar dos transiciones (1->2, 2->3) -- NO es diseño ejecutable por esta "
          "ficha (TB de ola 1 no comparable, D-10); referencia de mejor caso, igual "
          "que el escenario A de calx_g3.py",
     (f1 + f2) + (f2 + f3), (f1 + f2 + f3) / (N1 + N2 + N3), True),
    ("B", "Solo olas 2-3, una transición -- EL ÚNICO diseño que esta ficha puede "
          "ejecutar (D-10/incomparabilidad TB ola 1). Es el cálculo que la ficha "
          "ya publicó como ID-X.",
     f2 + f3, (f2 + f3) / (N2 + N3), False),
    ("C", "Olas 1 y 3 -- NO es diseño ejecutable por esta ficha (misma razón que A); "
          "referencia aritmética, igual que el escenario C de calx_g3.py para CRH",
     f1 + f3, (f1 + f3) / (N1 + N3), False),
]

print("=" * 78)
print("MATRIZ DE ESCENARIOS")
print("=" * 78)
hdr = (f"  {'esc':<4} {'ICC':>5} {'techo(nominal)':>14} {'N efectivo':>11} "
       f"{'SE':>8} {'IC95%sup':>9}  {'<1.25?':>10}")
print(hdr)
print("  " + "-" * (len(hdr) - 2))

resultados = []
for cod, nombre, nominal, p_esc, apila, in [(c, n, t, p, a) for c, n, t, p, a in ESCENARIOS]:
    for icc, etiq in (ICC_RANGO if apila else [(None, None)]):
        deff = efecto_diseno(OBS_POR_HOGAR, icc) if apila else 1.0
        neff = nominal / deff
        se = se_log_rr(p_esc, neff)
        ic = math.exp(Z * se)
        ok = ic < IC_SUP_ID_C
        resultados.append((cod, icc, nominal, neff, se, ic, ok))
        print(f"  {cod:<4} {(f'{icc:.2f}' if icc is not None else '  --'):>5} "
              f"{nominal:>14,} {neff:>11,.0f} {se:>8.4f} {ic:>9.3f}  "
              f"{'ALCANZA' if ok else 'no alcanza':>10}")

print("\n  Escenarios (qué representan, mismo criterio de declaración que calx_g3.py):")
for cod, nombre, _n, _p, _a in ESCENARIOS:
    print(f"    ({cod}) {nombre}")

# Verificación cruzada: el escenario B debe reproducir la cifra que la ficha
# borrador ya publicó a mano (IC95%sup = 1.237, Paso 2(8) fila ID-X).
b = [r for r in resultados if r[0] == "B"][0]
print(f"""
VERIFICACIÓN CRUZADA CONTRA LA FICHA: el escenario B (única transición
ejecutable, olas 2-3) debe reproducir IC95%sup = 1.237 (Paso 2(8), fila
ID-X, ficha borrador línea 145). Este script obtiene {b[5]:.3f}. {'COINCIDE' if abs(b[5]-1.237) < 0.001 else 'NO COINCIDE -- revisar'}.
""")

print("=" * 78)
print("VEREDICTO DEL BARRIDO")
print("=" * 78)

todos_alcanzan = all(r[6] for r in resultados)
ninguno_alcanza_salvo_floja = (not any(r[6] for r in resultados if r[0] != "B")) and b[6]
algunos_si_algunos_no = not todos_alcanzan and any(r[6] for r in resultados)

if todos_alcanzan:
    desenlace = "TODOS los escenarios cruzan <1.25."
elif algunos_si_algunos_no:
    desenlace = "ALGUNOS escenarios cruzan <1.25 y otros no."
else:
    desenlace = "NINGÚN escenario cruza <1.25 salvo, como mucho, la cota floja original."

peor = max(resultados, key=lambda r: r[5])
mejor = min(resultados, key=lambda r: r[5])

print(f"""
{desenlace}

Peor caso de la matriz:  escenario {peor[0]}"""
      + (f", ICC={peor[1]:.2f}" if peor[1] is not None else "")
      + f"  ->  IC95%sup = {peor[5]:.3f}"
      f"""
Mejor caso de la matriz: escenario {mejor[0]}"""
      + (f", ICC={mejor[1]:.2f}" if mejor[1] is not None else "")
      + f"  ->  IC95%sup = {mejor[5]:.3f}"
      f"""

Comparación con el precedente que puede matar esta condición (CRH,
tests/calx_g3.py): allá, el mejor caso teórico (escenario A, ICC=0,
apilado) dio 1.281 -- YA por encima de 1.25 -- y los escenarios reales de
una sola transición (B: 1.461, C: 1.401) quedaron todavía más lejos. Aquí,
el peor caso de toda la matriz ({peor[0]}"""
      + (f" ICC={peor[1]:.2f}" if peor[1] is not None else "")
      + f""") da {peor[5]:.3f}, que {'SIGUE' if peor[5] < IC_SUP_ID_C else 'NO SIGUE'} por debajo de {IC_SUP_ID_C}.

Esto es insumo de la condición (4) de sello de la ficha ID-G3, no su
resolución -- la resolución (sellar / elevar a mesa / no sellar) la fija
el acto que corrió este script, según los tres desenlaces que ese acto
declaró antes de correr (Encargo S2-IDG3 §3).
""")
