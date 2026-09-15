# Conversión presidencial de L8 · de un efecto agregado a tres celdas — pre-registro congelado de `CALC-L8-CONVERSION-0001`

### `prereg-caja-L8-CONVERSION-PRESIDENCIAL` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/L8-CONVERSION-PRESIDENCIAL-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-L8-CONVERSION-PRESIDENCIAL`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado **antes de correr nada**, de `CALC-L8-CONVERSION-0001`: las tres celdas de `civico.participacion.concurrencia_presidencial_conversion` como **derivación determinista** de cuatro escalares que ya viven en un artefacto versionado del repo. Releva `CORR-0016` (`RES-0050`, `RES-0051`, `RES-0052`). |
> | **QUÉ NO ES** | **No es una medición nueva y no toca microdato**: el insumo es `data/l8-resultados-tipo-boleta-v1_0.json`, producido y sellado por `ACTO MAESTRA35-L8`. No re-estima `beta_pres`, no re-corre el panel, no toca el wild cluster bootstrap. No adopta nada a `milpa/`. No resuelve la inferencia ecológica (§3): la declara, como ya la declara la regla. |
> | **VERIFICAS ASÍ** | La corrida **debe reproducir exactamente** los tres valores de `milpa/` — y sólo lo hace si el ancla `p0` se redondea a **cuatro** decimales antes de sumar (§2.3). Si el medidor usa precisión completa, los tres salen distintos en el quinto decimal y el `NO-REPRODUCE` sería **del redondeo, no de la cifra**. |

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1` (tanda 2), 15/sep/2026, entorno **NUBE**, sobre `d117ef1`.

**Regla consumidora:** `civico.participacion.concurrencia_presidencial_conversion`, `milpa/tramite.yaml`, `situacion: SELLADA`, `tier: MEDIA`, `veredicto_heredado: ACOTADA`, `escala: ecologica`.

---

## 0 · A.8 — qué ya existe

```
$ grep -rl "CORR-0016" data/corrida0/*/spec.yaml forense/prereg-caja/
  (0 aciertos)
```

Cero spec, cero `CALC`. Lo que **sí** existe, sellado desde el 2/sep y el
3/sep/2026, es el **insumo**: `data/l8-resultados-tipo-boleta-v1_0.json`
(43 545 bytes, versionado), con su spec (`forense/notas/2026-09-02-MAESTRA35-L8-spec.md`)
y su propuesta de conversión (`forense/notas/2026-09-03-MAESTRA36-N12-propuesta.md`).

**Esta corrida es la más barata de las 19 y la única que no necesita `data/raw`.**
Su «payload» es un artefacto del repo, resuelto por `origen: repo` + `sha256`,
no por manifiesto + raíz lógica. En consecuencia **puede correr en nube**; que
este acto no la corra es decisión del acto (contador cero declarado), no una
restricción del entorno.

---

## 1 · El insumo, resuelto por `sha256`

| | |
|---|---|
| ruta | `data/l8-resultados-tipo-boleta-v1_0.json` |
| `sha256` | `30f3e16dd6ea770ad72ab957547159c5427788a97a24a0ef30f2765752ef8f99` |
| bytes | 43 545 |
| origen | `repo` (versionado), **no** manifiesto |
| productor | `ACTO MAESTRA35-L8` (2/sep/2026) |

---

## 2 · Qué mide, exactamente

### 2.1 · Los cuatro escalares, y de qué clave del JSON sale cada uno

| escalar | clave del JSON | valor crudo |
|---|---|---|
| `beta_pres_pp` | `estimador.beta_pres_pp` | `4.016715486813227` |
| `p0` mínimo | `min` de las 40 medias | `30.509568846824635` |
| `p0` máximo | `max` de las 40 medias | `71.043832719488` |
| `p0` media | media de las 40 | `57.966254320884…` |

Las **40 medias** son `por_transicion[].y_de_media` y `por_transicion[].y_a_media`
sobre las 20 transiciones (2 patas × 20). **Verificado, no supuesto:** `n = 40`,
igual que `conversion_propuesta.p0_n_medias`. Y los cuatro derivados coinciden
con lo que la regla publica:

```
p0_rango_observado  declarado [0.3051, 0.7104]   derivado [0.3051, 0.7104]   COINCIDE
p0_media            declarado 0.5797             derivado 0.5797             COINCIDE
p0_mediana          declarado 0.6094             derivado 0.6094             COINCIDE
p0_n_medias         declarado 40                 derivado 40                 COINCIDE
```

### 2.2 · La transformación

`delta = round(beta_pres_pp / 100, 6) = 0.040167` — de puntos porcentuales a
proporción. Y para cada ancla:

`p = clip(round(p0, 4) + delta, 0, 1)`

`clip` **no está activo** en el rango observado (la regla lo declara:
`recorte_activo_en_rango_observado: false`) y se conserva porque la fórmula
sellada lo trae; `A-CLIP-ACTIVO` lo reporta en vez de asumirlo.

### 2.3 · La decisión que esta spec toma y que decide si la corrida reproduce

**El ancla se redondea a cuatro decimales ANTES de sumar.** No es cosmético —
es la diferencia entre reproducir y no:

| celda | sin redondear el ancla | con ancla a 4 decimales | GEN1 |
|---|---|---|---|
| `participa_p0_minimo` | `0.345263` | **`0.345267`** | `0.345267` |
| `participa_p0_maximo` | `0.750605` | **`0.750567`** | `0.750567` |
| `participa_p0_media` | `0.619830` | **`0.619867`** | `0.619867` |

La diferencia llega a `3.8 · 10⁻⁵` — **tres órdenes de magnitud por encima de
cualquier tolerancia de flotante**. Un medidor que usara precisión completa
reportaría `NO-REPRODUCE` en las tres celdas **por el redondeo, no por la
cifra**, y quien lo leyera buscaría un defecto donde no lo hay. Por eso el
grano va en el contrato (`parametros.grano_ancla_decimales: 4`) y no en la
cabeza de quien escriba el medidor.

`A-GRANO-VERIFICADO` emite **las dos** variantes para que el hallazgo sea
auditable sin tener que recalcularlo.

---

## 3 · Lo que esta corrida NO puede arreglar, y no finge arreglar

La regla declara `escala: ecologica` y lo dice con todas sus letras: `beta_pres`
se estimó sobre **agregados municipales** (votos totales / lista nominal) y la
regla lo aplica como **probabilidad individual**. *«el efecto agregado no
identifica el efecto individual salvo bajo homogeneidad dentro del municipio,
supuesto que este acto NO verifica y NO asume»*.

Esta corrida **hereda esa limitación entera** y no la toca: es una derivación
aritmética de cuatro escalares, no una re-identificación. Los tres `RESULT`
salen rotulados `DERIVADO-ECOLOGICO` y **ninguno es causal**. Los otros tres
riesgos que la regla declara —régimen casi universalmente concurrente,
precisión frágil (`IC95 [+0.049, +7.887]`, `p = 0.0413`, roza cero) y
heterogeneidad por tamaño (+2.60 pp en municipios chicos vs. +6.16 pp en
grandes)— **tampoco se resuelven aquí**, y `A-IC-BETA-ROZA-CERO` los deja a la
vista junto al punto en vez de dejarlos en la ficha.

---

## 4 · Control positivo y adopción

Las tres celdas contra su valor GEN1, **calculadas después de derivar y por
script** (`E.1`): `A-DELTA-VS-GEN1-*` con signo y `A-REPRODUCE-GEN1`
(`REPRODUCE` sólo si las **tres** coinciden a seis decimales). Como la
derivación es determinista y sin RNG, `NO-REPRODUCE` aquí **no es ruido**:
significa que el JSON cambió, que el grano no es el declarado, o que la
fórmula sellada no es la que se aplicó. `A-ADOPCION` sale
`LISTADO-PARA-MESA-*`; **este acto no escribe cita en `milpa/`**.

**Contaminación declarada (`ADR-46`).** Al congelar, la sesión ya había leído
los tres valores GEN1, la fórmula `conversion_A_aditiva` entera, el rango, la
media y la mediana de `p0`, y `n = 40`. **No es ciega y no podría serlo:** la
corrida *es* la fórmula que la regla publica, y el objeto del acto es cablearla
con cadena `E.2`, no descubrirla. Lo genuinamente desconocido al congelar era
si las 40 medias del JSON reproducían el rango declarado y con qué grano — y es
justo lo que §2.1 y §2.3 contestan.

---

## 5 · Lo que NO hace

No toca microdato (no hay) · **no escribe el medidor** (lo escribe el acto de
CAJA, aunque esta corrida no necesita CAJA) · no re-estima `beta_pres` ni
re-corre el panel de L8 · no toca el wild cluster bootstrap ni sus IC · no
resuelve la inferencia ecológica ni la heterogeneidad por tamaño · no propone
la vía **intermedia** (`beta_int = +0.2864 pp`, `IC95 [-1.2216, +1.7945]`,
contiene cero — la regla ya la descartó y esta spec no la reabre) · no adopta
cifra alguna a `milpa/`.
