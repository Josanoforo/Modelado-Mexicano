# `ACTO MAESTRA36-N12` · `P1`+`P2` — propuesta de conversión y presentación a mesa

Insumo: `forense/notas/2026-09-03-MAESTRA36-N12-benchmark.md`. Base `18fd2bd`.
**Nada de este documento se carga al motor.** La entrada que este acto añade a
`milpa/tramite-ola5-propuesta-v0.yaml` es `PROPUESTA-DE-CARGA`,
`PENDIENTE-DE-MESA`; `FP-255` sigue `ABIERTA`. `milpa/tramite.yaml` intocado.

---

## §1 · La regla propuesta

```
SI   el municipio celebra elección de ayuntamiento el mismo día que una
     jornada federal PRESIDENCIAL
ENTONCES el individuo participa con  p = clip(p₀(municipio) + 0.040167, 0, 1)
```

`Δ = β_pres / 100 = 0.040167`, re-derivado por comando de esta sesión:

```
$ python3 -c "import json; print(json.load(open('data/l8-resultados-tipo-boleta-v1_0.json'))['estimador']['beta_pres_pp'])"
4.016715486813227
```

**Tier propuesto: `MEDIA`**, heredado de `L8` (firma `e1`), sin re-evaluar.
**Veredicto heredado: `ACOTADA`** — `β_pres` sostiene el signo con IC wild
cluster que excluye cero por poco (`[+0.049, +7.887]`); `β_int ≈ 0`
(`+0.286 [−1.222, +1.794]`) no lo sostiene. La regla propuesta **solo usa la
vía presidencial**, que es la única acotada.

### §1.1 · De dónde sale `p₀` y cuál es su rango — declarado

`p₀(municipio)` **no es un parámetro nuevo**: es la participación municipal
base del propio panel de `L8`, definida en
`forense/notas/2026-09-02-MAESTRA35-L8-spec.md §1.2` como

```
participacion(m, e) = 100 * votos_totales(m, e) / lista_nominal(m, e)
```

sobre la unidad **municipio × elección de ayuntamiento**. El JSON de `L8` no
publica la serie municipio a municipio; publica las **medias municipales por
transición** (`por_transicion[].y_de_media` / `y_a_media`, 20 transiciones → 40
medias). Ese es el rango observable declarable con lo que hay en el repo:

```
$ python3 -c "
import json,statistics as st
d=json.load(open('data/l8-resultados-tipo-boleta-v1_0.json'))
ys=[r['y_de_media'] for r in d['por_transicion']]+[r['y_a_media'] for r in d['por_transicion']]
print(len(ys), min(ys), max(ys), st.mean(ys))"
40 30.510... 71.044... 57.966...
```

| | valor |
|---|---|
| `n` medias municipales | **40** (20 transiciones × 2 patas) |
| mínimo | **0.3051** — Baja California 2019→2021 (`n = 5` municipios) |
| máximo | **0.7104** — Veracruz 2017→2021 (`n = 209` municipios) |
| media | **0.5797** |
| mediana | **0.6094** |
| control de rango del propio `L8` | `fuera_de_rango: []` — ningún municipio con participación fuera de `[0,1]` |

**Rango declarado de `p₀`: `[0.3051, 0.7104]`.** El recorte a `[0,1]` de la
regla **nunca se activa** en este rango (se activaría solo con `p₀ > 0.9598`):
es una guardia, no un mecanismo.

**Reserva honesta:** este rango es de **medias por entidad-transición**, no de
municipios individuales. La dispersión municipal real es mayor en ambas colas.
Un acto sucesor que necesite el rango municipal verdadero tiene que volver al
panel crudo en Ubuntu; para la sensibilidad de §2 el rango de medias basta
porque la brecha entre convenciones es monótona y su cota se lee en los
extremos.

### §1.2 · Escala declarada — es ecológica, y se escribe así

`β_pres` está estimado sobre **agregados municipales**: numerador votos
totales, denominador lista nominal. La regla lo aplica como probabilidad de
que **un individuo** participe. Eso es **inferencia ecológica**: el efecto
agregado municipal no identifica el efecto individual salvo bajo homogeneidad
dentro del municipio, supuesto que este acto **no verifica y no asume como
cierto** — lo declara. La entrada de la propuesta lleva el campo
`escala: ecologica` con este texto, no como nota al pie.

Consecuencia operativa: `+4.0 pp` significa «la participación municipal sube
4 pp», y la regla lo reparte uniformemente entre los individuos del municipio.
Si el efecto real se concentra en un subgrupo (p. ej. votantes marginales
jóvenes), la regla acierta el agregado y yerra el individuo.

---

## §2 · Sensibilidad — la misma conversión en logit

Se calibra `δ` para **reproducir exactamente** `+4.0167 pp` en `p₀ = 0.50`:

```
δ = logit(0.50 + 0.040167) − logit(0.50) = 0.161016      (OR = 1.17470)
```

y se aplica `p₁ = logit⁻¹(logit p₀ + δ)` a los extremos del rango observado.

| `p₀` | quién | `p₁` aditiva | `p₁` logit | Δ logit (pp) | **brecha logit − aditiva (pp)** |
|---|---|---|---|---|---|
| **0.3051** | Baja California 2019→2021 (mín. observado) | 0.3453 | 0.3403 | +3.517 | **−0.500** |
| 0.4000 | — | 0.4402 | 0.4392 | +3.919 | −0.098 |
| **0.5000** | punto de calibración | 0.5402 | 0.5402 | +4.017 | **0.000** |
| 0.5797 | media del panel | 0.6199 | 0.6184 | +3.865 | −0.152 |
| 0.6000 | — | 0.6402 | 0.6380 | +3.795 | −0.222 |
| 0.7000 | — | 0.7402 | 0.7327 | +3.269 | −0.748 |
| **0.7104** | Veracruz 2017→2021 (máx. observado) | 0.7506 | 0.7424 | +3.197 | **−0.820** |

### §2.1 · Cuánto difieren las dos convenciones en los municipios extremos

**Brecha máxima: 0.82 pp**, en el extremo alto (Veracruz, `p₀ = 0.7104`).
En el extremo bajo (Baja California, `p₀ = 0.3051`) la brecha es **0.50 pp**.
El logit siempre da **menos** que la aditiva fuera del punto de calibración,
como debe ser por la concavidad de la inversa logística fuera de `p = 0.5`.

**El contraste que importa para decidir:**

| magnitud | pp |
|---|---|
| brecha máxima entre convenciones, en el rango observado | **0.82** |
| ancho del IC95 wild cluster por entidad de `β_pres` (el conservador, el que la spec designó para decidir) | **7.84** (`[+0.049, +7.887]`) |
| ancho del IC95 bootstrap por municipio | **1.34** (`[+3.347, +4.684]`) |
| heterogeneidad ya medida por tamaño de municipio (`heterogeneidad_tamano`) | **3.57** (chico +2.598 → grande +6.163) |

**Lectura:** la elección de convención mueve el resultado **menos de un décimo**
del ancho del IC conservador, y **menos de un cuarto** de la heterogeneidad por
tamaño de municipio que `L8` ya midió y que la regla propuesta **no** incorpora.
La discusión aditiva-vs-logit es, en este rango de `p₀` y con esta precisión,
**de segundo orden**. Lo que sí es de primer orden es la incertidumbre de
`β_pres` y la escala ecológica.

Esto no decide por mesa; acota el costo de la decisión.

---

## §3 · Corroboración externa del tamaño (no dato del motor)

De `…-N12-benchmark.md §1`, con la reserva de conducto de su §0 (los tres PDF
**no se abrieron**; política de egreso, `A.13`):

- **A favor del orden de magnitud:** INE 2015 — 53.3 % con concurrencia local
  vs 50.2 % sin, **+3.1 pp**, mismo signo y mismo orden que `+4.0`. Es la
  única fuente externa con un contraste concurrente/no-concurrente.
- **Sin efecto aislado:** TEPJF 1991-2018 (serie temporal, no contraste) e INE
  2024 (32 entidades concurrentes, sin contrafactual dentro del año).
- **No comparable pese al nombre:** la literatura *on-cycle/off-cycle*
  estadounidense (**+27 a +36 pp**, Hajnal-Lewis, Wood, Caren) mide otro
  estimando — su contrafactual fuera de ciclo parte de ~10-25 % de
  participación, mientras el contrafactual mexicano no concurrente parte de
  **30.5-71.0 %** (§1.1). **No se debe usar para juzgar que `+4 pp` es "bajo".**

Ninguna de estas cifras entra al motor. Se citan como corroboración del
tamaño, en los términos que el encargo fijó.

---

## §4 · `P2` — presentación a mesa (RH), una página

### Qué se propone cargar

Una regla cívica: **si el ayuntamiento del municipio se elige el mismo día que
la presidencial, la probabilidad de que la persona vote sube 4.0 pp** sobre la
base de su municipio. Una sola vía (la presidencial). La vía intermedia
**no** se propone: `β_int ≈ 0`.

### En qué escala

Probabilidad individual, obtenida de un efecto **agregado municipal**. Es
**inferencia ecológica** y así queda escrito en la entrada. La conversión es
**aditiva** (diferencia de riesgo), que es la escala nativa de la medición y la
convención de la literatura de turnout para efectos de contexto (benchmark §2.3).

### Qué gana el modelo

Sería la **primera regla cívica del motor con dato causal propio**: no una
frecuencia de encuesta, sino un `Δ` identificado por diseño (DD escalonado por
tipo de boleta federal, 864 transiciones municipio, 9 entidades). Hoy el motor
tiene **16** reglas y ninguna de participación electoral con identificación.

### Qué riesgo

1. **Inferencia ecológica** (§1.2): el efecto agregado se reparte uniforme
   entre individuos; si se concentra en un subgrupo, la regla yerra el
   individuo aunque acierte el municipio.
2. **Régimen casi universalmente concurrente.** El efecto se estima sobre
   transiciones de 2016-2024, y 2024 fue concurrente en las 32 entidades. La
   regla extrapola a escenarios contrafactuales de no-concurrencia que el
   calendario real casi ya no produce.
3. **Precisión frágil.** El IC conservador `[+0.049, +7.887]` **roza cero**:
   `p = 0.0413`. Cargar `+4.0` como punto es cargar el centro de un intervalo
   que casi contiene el nulo.
4. **Heterogeneidad no incorporada.** `L8` ya midió que el efecto va de
   **+2.60 pp** (municipios chicos) a **+6.16 pp** (grandes). La regla propuesta
   usa un solo número para los tres estratos.
5. **Corroboración externa indiciaria, no verificada** (benchmark §0): los tres
   PDF de partida no se pudieron abrir desde este entorno.

### Las tres opciones que `FP-255` ya nombra

| opción | qué implica | costo medido |
|---|---|---|
| **A · cargar aditiva** | `p = clip(p₀ + 0.040167, 0, 1)` | escala nativa de la medición; convención de la literatura; puede requerir recorte solo si `p₀ > 0.96` (no ocurre en `[0.3051, 0.7104]`) |
| **B · cargar logit** | `logit p₁ = logit p₀ + 0.161016` (`OR = 1.1747`) | respeta `[0,1]` sin recorte; **difiere de A en ≤ 0.82 pp** en el rango observado — un décimo del IC conservador |
| **C · dejar sellada** | `SELLADA-SIN-CARGA` se queda como está | el motor sigue en 16 reglas; no se paga el riesgo ecológico ni el de precisión |

**Dirección presenta; no recomienda entre A y B**, porque la evidencia medida
dice que la diferencia entre ambas es de segundo orden frente a la
incertidumbre de `β_pres`. Lo que dirección **sí** deja escrito es que si mesa
elige A o B, la reserva de heterogeneidad por tamaño (riesgo 4) queda como
sucesor declarado, no como cosa resuelta.

**Sucesor si la letra sale A o B:** `N13 · CARGA-CIVICA` (motor 16 → 17).
**Sucesor si sale C:** ninguno; `FP-255` se cierra sin carga.
