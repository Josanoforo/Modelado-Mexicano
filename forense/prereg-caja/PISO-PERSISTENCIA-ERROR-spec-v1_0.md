# PISO-PERSISTENCIA-ERROR · Pre-registro de la medición del error de la persistencia `t−1` por eje

### `prereg-caja-PISO-PERSISTENCIA-ERROR` · **v1.0** · 19 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/PISO-PERSISTENCIA-ERROR-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-PISO-PERSISTENCIA-ERROR`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, **congelado antes de calcular una sola diferencia**, de `CALC-PISO-PERSISTENCIA-ERROR-0001`: la medición de cuánto se equivoca el piso de persistencia `t−1` de la rejilla frente al `R` sellado de la misma celda marginal, celda por celda, en puntos porcentuales. |
> | **QUÉ NO ES** | **No adopta el piso como estimador de nada.** No abre microdato: los dos lados de cada resta ya están sellados. No deriva ni mira ningún cruce. No evalúa retadores. No decide `cuenta_gen2`. No reescribe ni re-corre ningún `CALC-PISOS-*`. **No se resta contra el MAE 1.47/1.57 de C2**: aquél es sobre celdas de cruce y éste sobre marginales — estimandos distintos (§7). |
> | **VERIFICAS ASÍ** | `python3 data/corrida0/CALC-PISO-PERSISTENCIA-ERROR-0001/medidor.py --verifica` reproduce los `RESULT` desde las mismas dos fuentes selladas; `python3 tests/test_marcador_segmento.py` mantiene la biyección del enlace. |

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
| **`R`** (ola objetivo) | `milpa/tramite-ola5-propuesta-v0.yaml`, las celdas de los siete ids `_ejes_` (`p`, `ic95`) | el yaml del árbitro, leído por `tools/marcador_segmento.py` |

Los cuatro `CALC-PISOS-*-EJES-0001` vetados (`veto:pisos-866`, `data/corrida0/decisiones.tsv:126`) **no se leen**, por nombre, incondicionalmente. `CALC-PISOS-ENIF2021-EJES-0002` tampoco: existe en el árbol pero es spec-only (sin `resultados.json`).

---

## 1 · Universo de la medición

Las **celdas marginales enlazadas**: toda fila `MARGINAL` de `data/corrida0/marcador-segmento.tsv` con `estado = SOLO-PISO`, es decir, con un piso `PERSISTENCIA(t−1)` sellado detrás por la tabla de identidad (P1 de este mismo acto). El enlace es biyectivo y lo garantiza mecánicamente `tests/test_marcador_segmento.py::t_enlace_biyectivo`.

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
