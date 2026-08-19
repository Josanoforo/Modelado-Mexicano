# Ficha B-bis · Gradiente de radio de confianza en ENBIARE 2021 — ESPECIFICACIÓN CONGELADA

> | | |
> |---|---|
> | **ARCHIVO** | `bbis-radio-confianza-enbiare-v1_0.md` |
> | **QUÉ ES** | Especificación **congelada antes de calcular**, del ACTO COEF-UNIVERSO. Commit 1 del patrón de dos commits. Los resultados van en un commit posterior y **el primer resultado que produzca este procedimiento es el que se reporta**. |
> | **QUÉ NO ES** | No es una producción sellada. **No pasa por el motor formal** (`especificaciones-produccion.json` → `prepare_production.py` → `produce.py` → `integrate_production.py`), porque ese archivo está **fuera del perímetro** de este acto y porque la regla del Dominio 4 dice que un mismo acto nunca hace de analista y de supervisor. Es medición **exploratoria y declarada como tal**. |
> | **ROTULADO A-bis** | **ASOCIACIÓN.** No hay llave de identificación de ninguna de las tres clases de `ADR-57(c)`. Ningún resultado de esta ficha autoriza la palabra "coeficiente". |

---

## 1 · Por qué existe

`ADR-109(d)` (sellado 18/ago/2026) revocó la relación `REL-51392f82` de `EXISTE-SATISFACE` a `EXISTE-NO-SATISFACE`. Su `razon_gate`, verbatim en `data/cableado-universo-v1_0.tsv`: *"radio_confianza exige el contraste, no un item"*. La evaluación que produjo ese veredicto fue de grado **E2**, declarado por el propio pipeline como hecho **sin abrir microdatos**, y miró `PB1_01` **aislada**.

El contraste que ese `razon_gate` echa en falta es la variable **inmediatamente siguiente de la misma batería**: `PB1_02`. Esta ficha no revoca `ADR-109(d)` — evalúa un **objeto distinto**: el **par**, no el ítem.

## 2 · Qué se estima, exactamente

Fuente: `data/raw/enbiare2021/enbiare_2021_base_de_datos_csv.zip`, tabla `TENBIARE.csv` (284 columnas).

- **`PB1_01`** — *"En general, ¿cuánto confía en la gente?"*, escala declarada **0 a 10** (`enbiare_2021_fd.pdf`: `Alfanumérico`, longitud 2, rango `00 - 10`).
- **`PB1_02`** — *"En general, ¿cuánto confía en la gente que usted conoce?"*, misma escala.
- **`PB2_1`** — la familia siempre ayuda (categórica).
- **`PB2_2`** — amigos o no-familia siempre ayudan (categórica).

**Estimandos, los cuatro:**

1. `μ₁` = media poblacional de `PB1_01`, en puntos de escala 0-10.
2. `μ₂` = media poblacional de `PB1_02`, en puntos de escala 0-10.
3. `D` = `μ₂ − μ₁`, en **puntos de escala**, con IC95%.
4. `p₁`, `p₂` = proporciones poblacionales de respuesta afirmativa en `PB2_1` y `PB2_2`, y su diferencia `Δ = p₁ − p₂`, con IC95%.

**Diseño muestral, obligatorio:** estimadores ponderados por `FAC_ELE`, con varianza por el estimador de **conglomerado último** sobre estratos `EST_DIS` y UPM `UPM_DIS`. Para medias y diferencias, linealización de Taylor. Un estrato con una sola UPM aporta 0 a la varianza y **se cuenta y se declara**.

**Universo:** el de ENBIARE 2021, **población de 18 años y más**, tal como el propio instrumento lo define. Casos con código fuera de `0..10` en `PB1_01` o `PB1_02` se **excluyen y se cuentan**; el `n` efectivo se reporta.

## 3 · El falsador, y qué se sabía antes de congelar

**Se declara lo que ya se sabía, porque callarlo invalidaría el pre-registro.** Una corrida exploratoria **sin ponderar** de este mismo acto ya observó `mean(PB1_01)=5.26`, `mean(PB1_02)=7.56`, `r=0.57`, `n=31 166`, y `PB2_1` Sí=29 204/No=1 921 contra `PB2_2` Sí=22 788/No=8 378. **La dirección del gradiente ya se conocía al escribir esta ficha.** Lo que **no** se conoce, y es lo que esta ficha pre-registra, es la **magnitud poblacional bajo el diseño complejo y la amplitud de su intervalo** — que es exactamente lo que decide si el contraste sostiene algo o es ruido de una muestra grande.

- **Refuta** si `D ≤ 0`, **o** si el IC95% de `D` contiene 0, **o** si el IC95% de `Δ` contiene 0.
- **No refuta** si `D > 0` con IC95% que despeja 0 **y** `Δ > 0` con IC95% que despeja 0.

## 4 · B-bis — qué significa que el falsador NO refute

Esto es lo que la ficha existe para fijar **antes** de ver el número.

**Sí compra, y sólo esto:** que el instrumento ENBIARE **sí gradúa** el radio de confianza — que la batería expresa un contraste ordenado (familia > conocidos > gente en general) y no un solo polo. Es decir, que la premisa fáctica del `razon_gate` de `ADR-109(d)` —*"la batería no gradúa"*— **es falsa como afirmación sobre el instrumento**, aunque la decisión de revocar `REL-51392f82` siga siendo correcta para el **objeto que esa relación evaluó** (un ítem suelto).

**No compra, y hay que decirlo entero:**

1. **No es identificación.** Co-observación en el mismo cuestionario da **ASOCIACIÓN**. No hay panel, ni experimento natural, ni diseño experimental de terceros. La palabra "coeficiente" queda prohibida sobre este resultado (`ADR-57(a)`, `ADR-57(c)`).
2. **No corrobora el `0.15` asignado a `G5.radio_confianza`.** La escala de este resultado es **puntos de una escala 0-10 declarada**; la del coeficiente de generador es la del índice del modelo. **No hay enlace entre las dos escalas**, y sin enlace no se comparan magnitudes — ni para confirmar ni para desmentir. Concordancia de signo tampoco corrobora (`ADR-57(a)`).
3. **No mueve `0 de 15`.** Ningún coeficiente en escala del modelo se produce aquí.
4. **No re-adjudica `ADR-109(d)`.** Propone a mesa un objeto nuevo — el par — sobre el cual mesa decide. Un ejecutor no revoca un ADR.
5. **No es transportable fuera de 2021** ni fuera del universo de 18+ de ENBIARE.
6. **Condicionar no lo arreglaría.** Si un acto futuro parte este gradiente por formalidad o ingreso, el resultado condicionado sigue siendo asociación (`A-bis` regla 2).

**Y la contraparte, igual de vinculante:** si el IC no despeja el umbral, el resultado es **propuesta con reserva**, no adjudicación — y se reporta igual.

## 5 · Procedimiento, congelado

**El script no vive en `tests/`**: crear un archivo ahí queda **fuera del perímetro** de este acto. Va incrustado aquí, verbatim y congelado en este commit, de modo que sea reproducible copiándolo. **El primer resultado que produzca es el que se reporta**, sin reejecución selectiva, sin cambio de universo y sin cambio de estimador después de ver la cifra.

```python
import zipfile, io, csv, math

Z = "data/raw/enbiare2021/enbiare_2021_base_de_datos_csv.zip"
VAL01 = set(range(0, 11))          # PB1_01 / PB1_02: rango declarado 00-10 en el fd
VAL2 = {1, 2}                      # PB2_1 / PB2_2: 1=Si, 2=No (3 = sin familia -> se excluye y se cuenta)

def leer():
    z = zipfile.ZipFile(Z)
    with z.open("TENBIARE.csv") as fh:
        for r in csv.DictReader(io.TextIOWrapper(fh, encoding="latin-1")):
            yield r

def num(v):
    v = (v or "").strip()
    if v == "":
        return None
    try:
        return int(v)
    except ValueError:
        return None

def ultimate_cluster(z_por_unidad):
    """Varianza de conglomerado ultimo sobre valores YA linealizados.
    z_por_unidad: lista de (estrato, upm, z). Devuelve (varianza, estratos_de_una_upm)."""
    por_estrato = {}
    for h, a, z in z_por_unidad:
        por_estrato.setdefault(h, {}).setdefault(a, 0.0)
        por_estrato[h][a] += z
    V = 0.0
    singleton = 0
    for h, upms in por_estrato.items():
        n_h = len(upms)
        if n_h < 2:
            singleton += 1           # aporta 0 y se declara
            continue
        tot = list(upms.values())
        media = sum(tot) / n_h
        V += (n_h / (n_h - 1.0)) * sum((t - media) ** 2 for t in tot)
    return V, singleton

def estimar(filas, valor_fn, valido_fn):
    """Media/proporcion ponderada + IC95% por linealizacion de Taylor."""
    us = []
    for r in filas:
        if not valido_fn(r):
            continue
        w = float(r["FAC_ELE"])
        us.append((r["EST_DIS"], r["UPM_DIS"], w, valor_fn(r)))
    W = sum(u[2] for u in us)
    R = sum(u[2] * u[3] for u in us) / W
    z = [(h, a, w * (y - R) / W) for (h, a, w, y) in us]
    V, sing = ultimate_cluster(z)
    ee = math.sqrt(V)
    return {"est": R, "ee": ee, "ic": (R - 1.96 * ee, R + 1.96 * ee),
            "n": len(us), "suma_pesos": W, "estratos_1upm": sing}

filas = list(leer())
print("filas TENBIARE:", len(filas))

ok12 = lambda r: num(r["PB1_01"]) in VAL01 and num(r["PB1_02"]) in VAL01
m1 = estimar(filas, lambda r: num(r["PB1_01"]), ok12)
m2 = estimar(filas, lambda r: num(r["PB1_02"]), ok12)
D = estimar(filas, lambda r: num(r["PB1_02"]) - num(r["PB1_01"]), ok12)

ok2 = lambda r: num(r["PB2_1"]) in VAL2 and num(r["PB2_2"]) in VAL2
p1 = estimar(filas, lambda r: 1.0 if num(r["PB2_1"]) == 1 else 0.0, ok2)
p2 = estimar(filas, lambda r: 1.0 if num(r["PB2_2"]) == 1 else 0.0, ok2)
Delta = estimar(filas, lambda r: (1.0 if num(r["PB2_1"]) == 1 else 0.0)
                               - (1.0 if num(r["PB2_2"]) == 1 else 0.0), ok2)

for nom, e in [("mu1 PB1_01 (0-10)", m1), ("mu2 PB1_02 (0-10)", m2),
               ("D = mu2-mu1 (puntos)", D),
               ("p1 PB2_1 familia (prop)", p1), ("p2 PB2_2 no-familia (prop)", p2),
               ("Delta = p1-p2 (pp)", Delta)]:
    print(f"{nom:26s} {e['est']:+.4f}  EE {e['ee']:.4f}  "
          f"IC95 [{e['ic'][0]:+.4f}, {e['ic'][1]:+.4f}]  "
          f"n={e['n']}  sumaW={e['suma_pesos']:.0f}  estratos_1upm={e['estratos_1upm']}")

excl12 = sum(1 for r in filas if not ok12(r))
excl2 = sum(1 for r in filas if not ok2(r))
print("excluidos por codigo fuera de rango -- PB1:", excl12, " PB2:", excl2)
```
