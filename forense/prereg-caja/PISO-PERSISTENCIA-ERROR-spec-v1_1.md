# PISO-PERSISTENCIA-ERROR · v1.1 · sucesión por input (F4 (a))

**Qué cambia y qué no.** Acto `GEN2-PISOS-Y-ADENDAS-1` (P2), 28/sep/2026, CAJA, 0-bis `fa42a3c1`; firma de mesa **F4 (a)** (28/sep/2026, «firmado»; FP `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-22`). `CALC-PISO-PERSISTENCIA-ERROR-0001` se selló (19/sep, commit `24afe8b9`) con un medidor que **importa `tools/marcador_segmento.py` vivo** y deriva el marcador del árbol; ese archivo cambió 14 veces desde entonces y `milpa/tramite-ola5-propuesta-v0.yaml` también cambió (sha en HEAD `f19f2c51…` ≠ `93dfa3f9…` declarado), así que el verify aislado del 22/sep dio `NO-EJECUTABLE` (NC `NC-260922-GEN2-PENDIENTES-CAJA-1-c09b-03`). Esta v1.1 es **la misma spec humana salvo el input**: el estimando, el universo, `z95`, la clasificación, los agregados, la tolerancia y los 317 ids de `RESULT` son los de v1.0; lo único que cambia es que el medidor lee una **constancia congelada** con sha256 (D-22(4)) en lugar del módulo vivo. El medidor de `CALC-PISO-PERSISTENCIA-ERROR-0002` es el de 0001 con `_marcador()` sustituido por la lectura de la constancia; ninguna otra línea de cálculo cambia.

**Qué constancia (INTERPRETACIÓN-DECLARADA).** La hoja F4 dice «congele el marcador-segmento vigente como input con hash … y reproduzca los 317 RESULT contra ese snapshot fijo». El marcador de hoy ya no produce esos 317 ids (el verify del 22/sep lo midió: faltan y sobran ids; hoy además hay celdas que pasaron de `SOLO-PISO` a `EVALUADA` por los R GEN2 del árbitro, medidas aparte por `CALC-ARBITRO-PERSISTENCIA-ERROR-0001`). Las dos mitades de la firma sólo se cumplen a la vez con el marcador **vigente en el sello de 0001**: la constancia se deriva con `tools/marcador_segmento.py` del árbol exacto del commit `24afe8b9` (`git archive`), sin leer ningún `resultados.json` de 0001. Se declara aquí, antes de correr.

**Relación con 0001 (E.3).** 0001 no se edita ni se re-corre: queda como evidencia histórica. 0002 declara `repite_de: CALC-PISO-PERSISTENCIA-ERROR-0001` en la raíz de su `spec.yaml`. Tras la corrida, la nota compara punto e IC de los 317 `RESULT` contra los sellados de 0001 con la tolerancia de v1.0 (`abs 1.0e-10`), rotulada **RETROSPECTIVA-MECÁNICA**. Unidad de cada cifra: la del piso y la del R de su celda (proporción ponderada; persona, trámite o delito según instrumento, declarada por celda); nunca se promedian entre instrumentos (§5).

**Ejecución previa declarada (E.5).** Antes de este COMMIT-1 el medidor de 0002 se ejecutó **una vez** por línea de comandos sobre la constancia, como prueba de humo del reemplazo de `_marcador()`, e imprimió sólo su línea de resumen: `celdas enlazadas=53 comparables=53 PERSISTE=22 CAMBIA=31`. No se miró ningún `RESULT` ni ningún valor por celda, y no se cambió nada después. El procedimiento es determinista (sin semilla) y ése es el mismo resultado que dará `corrida0 run`; se declara aquí, no se oculta.

**Todo lo que sigue es el cuerpo de v1.0, verbatim, salvo** el título de versión, las filas ARCHIVO / QUÉ ES / VERIFICAS ASÍ de la tabla de cabecera, la fila `R` de §0 (más una fila nueva «v1.1 · lo que el medidor lee») y una frase aclaratoria en §1. Sha256 de v1.0: `3e462662b30c5c7d2eaebc27bf2f6dd85ceba78959347b4754dd69d5133875e0`.

---

# PISO-PERSISTENCIA-ERROR · Pre-registro de la medición del error de la persistencia `t−1` por eje

### `prereg-caja-PISO-PERSISTENCIA-ERROR` · **v1.1** · 28 de septiembre de 2026 (sucede a v1.0 sólo en el input)

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/PISO-PERSISTENCIA-ERROR-spec-v1_1.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-PISO-PERSISTENCIA-ERROR`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, **congelado antes de calcular una sola diferencia**, de `CALC-PISO-PERSISTENCIA-ERROR-0002` (v1.0 lo fue de `CALC-PISO-PERSISTENCIA-ERROR-0001`): la medición de cuánto se equivoca el piso de persistencia `t−1` de la rejilla frente al `R` sellado de la misma celda marginal, celda por celda, en puntos porcentuales. |
> | **QUÉ NO ES** | **No adopta el piso como estimador de nada.** No abre microdato: los dos lados de cada resta ya están sellados. No deriva ni mira ningún cruce. No evalúa retadores. No decide `cuenta_gen2`. No reescribe ni re-corre ningún `CALC-PISOS-*`. **No se resta contra el MAE 1.47/1.57 de C2**: aquél es sobre celdas de cruce y éste sobre marginales — estimandos distintos (§7). |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py verify CALC-PISO-PERSISTENCIA-ERROR-0002` reproduce los `RESULT` desde la constancia congelada `data/corrida0/CALC-PISO-PERSISTENCIA-ERROR-0002/insumos/constancia-marcador-24afe8b9.json` (sha256 declarado en `spec.yaml`); la constancia se re-deriva byte a byte con `forense/notas/2026-09-28-GEN2-PISOS-Y-ADENDAS-1/p2_deriva_constancia.py` sobre el árbol del commit `24afe8b9`. |

**Acto:** `ACTO GEN2-MARCADOR-PISOS-ENLACE-1`, 19/sep/2026, entorno **NUBE**, sin corpus montado (`data/raw` ausente; `tools/entorno.py` → `acceso_corpus.montado = NO`, `archivos_examinados = 0`). Base `origin/main = 8e455bd6`. Encargo archivado: `forense/encargos/2026-09-19-GEN2-MARCADOR-PISOS-ENLACE-1.md`.

**Frase de sello:** «el primer resultado que produzca este procedimiento es el que se reporta».

---

## 0 · Insumos, sellados antes de esta spec

Cero microdato. Los dos lados de cada resta ya existían y están sellados antes de que se escribiera una línea de `medidor.py`:

| lado | fuente | sello |
|---|---|---|
| **piso** (`t−1`) | `data/corrida0/CALC-PISOS-ENVIPE2024-EJES-0002` | `sello.sha256 = 393c418420d52363e5a659d568f00689e7d36271034f64dcefdc91b772f6fd66` |
| **piso** (`t−1`) | `data/corrida0/CALC-PISOS-ENCIG2023-EJES-0002` | `sello.sha256 = 548ea868ee45fe7477ba00c7b793c62e68f325390344c4c38d0b0f31787de352` |
| **piso** (`t−1`) | `data/corrida0/CALC-PISOS-ENIF2021-EJES-0003` | `sello.sha256 = 795b960b5d23ea9a0ce801cd321f7537664d6c4f1ee9b0e3c59ae1f00524c707` |
| **identidad** | `forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv` | `sha256 = 1715da9303957dac11146bd14e5498d11c554671edcdfb9c6ea7230845433a95` |
| **`R`** (ola objetivo) | `milpa/tramite-ola5-propuesta-v0.yaml`, las celdas de los siete ids `_ejes_` (`p`, `ic95`) | el yaml del árbitro **tal como estaba en el commit `24afe8b9`** (sha256 `93dfa3f9aab250dabf9cbe8c93ccef2012cb763c5367d023f24dbfbd867fbc8f`) |
| **v1.1 · lo que el medidor lee** | `data/corrida0/CALC-PISO-PERSISTENCIA-ERROR-0002/insumos/constancia-marcador-24afe8b9.json` | constancia congelada (D-22(4)): lo que `tools/marcador_segmento.py` **del commit `24afe8b9`** derivaba de las cinco fuentes de arriba — las filas `MARGINAL` con `resultado_id`, las filas de la tabla de identidad que citan y `NORMALIZA_UNIT_TABLA`; sha256 en `spec.yaml`. El medidor **no importa** `tools/marcador_segmento.py` ni lee `milpa/` |

Los cuatro `CALC-PISOS-*-EJES-0001` vetados (`veto:pisos-866`, `data/corrida0/decisiones.tsv:126`) **no se leen**, por nombre, incondicionalmente. `CALC-PISOS-ENIF2021-EJES-0002` tampoco: existe en el árbol pero es spec-only (sin `resultados.json`).

---

## 1 · Universo de la medición

Las **celdas marginales enlazadas**: toda fila `MARGINAL` de `data/corrida0/marcador-segmento.tsv` (en v1.1: de la constancia, es decir, del marcador tal como se derivaba en el commit `24afe8b9`) con `estado = SOLO-PISO`, es decir, con un piso `PERSISTENCIA(t−1)` sellado detrás por la tabla de identidad (P1 de este mismo acto). El enlace es biyectivo y lo garantiza mecánicamente `tests/test_marcador_segmento.py::t_enlace_biyectivo`.

Una celda marginal `SIN-PISO` **no entra**: no hay resta que hacer. Las cuatro `NO-CONSTRUIBLE` de la tabla quedan fuera con la causa que la tabla escribe (`P3_13 comparable no existe en ENIF 2021`), no con una causa inventada aquí.

---

## 2 · El estimando, por celda

Para cada celda enlazada `c`:

```
d(c) = R(c) − piso(c)      expresado en PUNTOS PORCENTUALES
```

con `R(c)` y `piso(c)` ambos **proporciones en `[0,1]`** (misma escala; lo declaran las dos fuentes: la spec de cada `CALC-PISOS-*` rotula cada `-P` como `tipo: proporcion, unidad: "proporción ponderada [0,1]"`, y el `p` del árbitro es la proporción de la misma ola objetivo). La conversión a puntos porcentuales es `×100` y es la **única** transformación de escala del procedimiento.

Signo: `d > 0` significa que la ola objetivo quedó **por encima** de lo que la persistencia predecía; `d < 0`, por debajo.

**Universo y unidad.** Se leen de la tabla de identidad (`unit`) y del `payload` del árbitro, no se suponen. Los tres valores posibles son `DELITO`, `TRAMITE` y `PERSONA ELEGIDA 18+`. **Si la unidad o el universo no coinciden entre el piso y el `R` de la misma celda, la celda sale `NO-COMPARABLE` con causa y no se fuerza** (A-bis 3–4). No se convierte, no se reescala, no se descarta en silencio.

---

## 3 · Incertidumbre de `d`

De los **dos IC95 ya sellados**, no de una re-corrida: el piso trae `IC-LO`/`IC-HI` (bootstrap UPM estratificado, 10 000 réplicas, percentiles 2.5/97.5 — declarado en el `spec.yaml` de cada `CALC-PISOS-*`) y `R` trae su `ic95` en el yaml del árbitro.

**Método declarado, y su supuesto declarado:** las dos olas se tratan como **muestras independientes** (son levantamientos distintos de años distintos; no hay panel entre ellas). Cada IC95 se convierte a un error estándar aproximado por

```
ee = (ic95sup − ic95inf) / (2 · 1.959964)
```

(supuesto de simetría normal del intervalo; es una aproximación y aquí se dice que lo es). Entonces

```
ee_d = sqrt(ee_R² + ee_piso²)
IC95(d) = d ∓ 1.959964 · ee_d      en puntos porcentuales
```

**Lo que este método NO captura**, escrito antes de correr: el bootstrap del piso es por percentiles y puede ser asimétrico — reducirlo a un `ee` simétrico pierde esa asimetría; y la independencia entre olas no cubre la correlación que introduce un marco muestral compartido. Ambas cosas **ensanchan o estrechan** `IC95(d)` en un margen que esta spec no mide. Por eso la clasificación de §4 se reporta como lectura de este procedimiento, no como prueba de hipótesis.

---

## 4 · Clasificación por celda (congelada)

| clase | criterio |
|---|---|
| **`PERSISTE`** | `IC95(d)` **incluye** 0 |
| **`CAMBIA`** | `IC95(d)` **excluye** 0 |
| **`NO-COMPARABLE`** | unidad o universo discrepan entre piso y `R` (§2), o falta alguno de los dos IC95 |

No hay una cuarta clase y no hay umbral de magnitud: el criterio es el intervalo, y sólo el intervalo.

---

## 5 · Agregados

**Por instrumento y por desenlace, nunca entre instrumentos.** Las brechas temporales son distintas y se declaran en cada fila:

| instrumento | piso (`t−1`) | `R` (ola objetivo) | brecha |
|---|---|---|---|
| ENVIPE | 2024 (periodo de referencia 2023) | 2025 (2024) | **1 año** |
| ENCIG | 2023 | 2025 | **2 años** |
| ENIF | 2021 | 2024 | **3 años** |

Agregados que se emiten por (instrumento × desenlace) y por (instrumento × eje): `n` de celdas, `n` `PERSISTE`, `n` `CAMBIA`, `n` `NO-COMPARABLE`, **MAE en pp** (media de `|d|`) y `d` medio con signo. **Ningún agregado cruza instrumentos**: un MAE que promedie una brecha de 1 año con una de 3 no es un número de nada.

---

## 6 · B-bis — qué se concluye, escrito ANTES de ver un solo `d`

**Por instrumento**, sobre sus celdas comparables:

- **Si la mayoría `PERSISTE`** → la persistencia queda **corroborada como piso a esa brecha**: en ese instrumento, una ola vieja ya predice la nueva dentro del ruido, y **un retador tiene poco margen que ganar** ahí. Consecuencia operativa: no se prioriza piloto en ese instrumento.
- **Si la mayoría `CAMBIA`** → el piso es **débil a esa brecha**: ahí sí vale la pena un retador, y **es donde un piloto rinde**. Consecuencia operativa: PILOTO-3 va a ese instrumento (sucesor declarado del encargo).
- **Si en un instrumento ambas lecturas caben según el eje** (unos ejes mayormente `PERSISTE` y otros mayormente `CAMBIA`) → **manda la lectura por eje**, no la del instrumento, y se dice explícitamente al sellar cuáles ejes van por cada lado.

Empate exacto (mismo número de `PERSISTE` que de `CAMBIA`) → se lee como **sin mayoría** y se reporta así, sin desempatar por magnitud.

---

## 7 · Lo que NO se hace con este resultado

- **No se compara contra el MAE 1.47 / 1.57 pp de C2.** Aquél mide celdas de **cruce**; éste mide **marginales**. Son estimandos distintos. Se pueden poner **lado a lado con ese rótulo**; **no se restan**, no se ordenan juntos, y ninguno "gana" al otro.
- Un `CAMBIA` **no adopta** nada ni desadopta nada.
- Un `PERSISTE` **no** dice que el piso sea el estimador de la celda.

---

## 8 · Módulo de auditoría (afirma sobre México — aplica completo)

Un **`CAMBIA` es cambio en el tiempo de una proporción en un universo restringido** —delitos, trámites, personas elegidas 18+—, **no** un cambio de disposiciones de un segmento de la población.

**Confusor estructural declarado:** el periodo de referencia de ENIF 2021 es *«julio 2020 a levantamiento 2021»*: pandemia. Una diferencia 2021→2024 en ahorro informal es **primero** choque de ingreso y de acceso a sucursales, y **sólo después, si algo queda**, conducta. Ninguna lectura de las celdas ENIF de este CALC puede saltarse esa frase.

**ENVIPE mide delitos declarados por víctimas**: un cambio en `evasión` carga cambios en la **composición del delito**, no sólo en la conducta frente a la norma.

**Los ejes (escolaridad, localidad, sexo, edad, dominio, cobertura de seguro, cuenta) son marcadores de estructura**, no causas. **La rejilla no ve región ni condición indígena** — límite declarado, no subsanado aquí.

**Clase de evidencia:** (a) datos primarios en México, en los tres instrumentos. **Ninguna cifra de este CALC es esperada: todas se derivan.** Escalas: proporción en todo objeto; **ninguna comparación cruza unidad**.

**Peligroso leído simplista:** «la persistencia acierta» leído como «los mexicanos no cambian». Un `PERSISTE` dice que una proporción agregada en un universo restringido se movió menos que el ruido de dos muestras — nada sobre personas.

---

## 9 · Salidas

- Un `RESULT` por celda comparable, con sufijos `-D-PP` (la diferencia), `-D-IC-LO-PP`, `-D-IC-HI-PP` y `-CLASE`.
- Un `RESULT` por agregado: `-MAE-PP`, `-D-MEDIO-PP`, `-N`, `-N-PERSISTE`, `-N-CAMBIA`.
- Columnas nuevas en `data/corrida0/marcador-segmento.tsv`: `error_piso_pp` y `clase_persistencia`, **derivadas del CALC** — el marcador no las recalcula.
- Asiento en `forense/replay-evidencia.tsv` de este mismo acto (E.7).
