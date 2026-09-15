# TRIADA-B-PISO · Pre-registro de la tabla común de la tríada con `B` de persistencia como piso

### `prereg-caja-TRIADA-B-PISO` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-TRIADA-B-PISO`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro de **una corrida de registro**: la tabla común de `B`, `L_CORPUS`, `L_SOLO` y `M` sobre el único universo donde los cuatro tienen punto (`U_COMUN = U3 ∩ {celdas con B bajo PERSISTENCIA}`), **derivada** celda a celda desde `celdas.tsv` del sucesor y el asiento sellado de `B`, no heredada de ningún `MAE` previo. Gobierna **un** CALC: `CALC-TRIADA-B-PISO-0001`. Sucesora **por consumo** de `prereg-caja-B-MARCO` (`sha256 = e61969b9cbf302004fd6b3bf04f2b3785edda331d1165dac6603acd404d1ab38`): aquélla dejó `B` extendido **DISPONIBLE** para «la próxima corrida de tríada que mesa autorice» (§7.3); ésta es esa corrida, y es descriptiva. |
> | **QUÉ NO ES** | **No es un duelo.** No corre pareadas, no calcula IC, no adjudica y no corona. **No re-corre la tríada**: `CALC-TRIADA-0002` no se toca y su `SIN-GANADOR-UNICO` se cita intacto. **No redefine `B`** ni toca `CALC-B-MARCO-*`. **No adopta**: ninguna cifra suya entra a una regla del motor (`T9`), y `NC-0187` cierra **por consumo de `B` en su consumidor declarado —la tríada—, no por adopción**. No abre microdato, no llama a ningún modelo, no imputa y no rellena. No habilita `F6`. |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py preflight CALC-TRIADA-B-PISO-0001` en VERDE; después `run` y `verify`. **Control de derivación** (§4.1), que es la razón de ser del CALC: los tres `MAE` de `CALC-TRIADA-0002` sobre `U3`, recalculados desde `celdas.tsv`, contra los sellados, en tres ramas con consecuencia escrita antes de correr. Pruebas prospectivas sobre datos **sintéticos** en `data/corrida0/CALC-TRIADA-B-PISO-0001/pruebas-sinteticas.py`. |

**Acto:** `ACTO GEN2-F5-CIERRE-Y-PANEL-1`, 15/sep/2026, entorno **NUBE**, cero llamadas. Bajo la **FIRMA DE MESA, 15 de septiembre de 2026**, `D-2` (D-A) y `D-1` (tesis).

---

## 0 · Premisas del encargo verificadas contra el árbol, y la contaminación declarada

### 0.1 · Las premisas del lanzamiento se reproducen, con su comando

1. **`celdas.tsv` del sucesor existe y es el marco completo.** `forense/prereg-duelo-v2/F5-aprendizajes-sucesor-v1_0/celdas.tsv`: **14 filas**, 22 columnas; trae por celda `R_pct`, las medianas y coberturas de `L_SOLO`/`L_CORPUS`, `m_pct`, los tres `error_abs_*_pp`, los tres `contrib_mae_*_pp` y `en_u3`. `en_u3 = SI` en **12** filas.
2. **El asiento de `B` existe y cubre 10.** `data/corrida0/CALC-B-MARCO-MAE-0001/resultados.json`: 155 `RESULT`; `RESULT-BM-MAE-<celda>-PERSISTENCIA-ERR-PP` **no nulo en 10** de 14 celdas (`RESULT-BM-MAE-PERSISTENCIA-N-CELDAS = 10`, `-MAE-PP = 0.9229306553900927`).
3. **La intersección es 9, no 10 ni 12.** Las 10 con `B` menos `TRA-M-07`, que tiene `B` (`PERSISTENCIA-ERR-PP = 1.2668595552796882`) pero `en_u3 = NO` porque `L_CORPUS` se abstuvo válidamente en sus 8 réplicas (`NC-0152`). **`U_COMUN` = 9 celdas:** `CIV-M-01`, `CIV-M-02`, `CIV-M-04`, `CIV-M-10`, `CIV-M-12`, `CIV-M-13`, `FAM-M-05`, `FAM-M-06`, `FAM-M-07`.
4. **`CALC-TRIADA-0002` está sellado y dice lo que el lanzamiento dice.** `RESULT-F5C-U3-N = 12`; `RESULT-F5C-MAE-L-SOLO-PP = 3.9573621816025666`; `-L-CORPUS-PP = 3.889025747112979`; `-M-PP = 4.9866732397828875`; `RESULT-F5C-VEREDICTO-GLOBAL = SIN-GANADOR-UNICO`; las tres pareadas `INCONCLUSO`.

### 0.2 · Contaminación declarada (ADR-46) — TOTAL, y por eso la regla no tiene grados de libertad

El lanzamiento **ya trae el resultado**: dirección verificó, antes de encargar, que `celdas.tsv` reproduce al centésimo los `MAE` sellados de la `0002` sobre `U3` y que la tabla común da **B 0.885 / L_CORPUS 1.223 / L_SOLO 1.481 / M 4.638**. Esta sesión pudo ver, y vio, los cuatro insumos. **No se finge ceguera.** Lo que hace que la corrida siga valiendo no es el desconocimiento, sino que **la regla no admite alternativas**: el universo es una intersección (no hay criterio que elegir), el estadístico es la media simple de `abs(err_pp)` que la familia ya usa (`A-bis.4`, heredada de `CALC-TRIADA-0002` y de `CALC-B-MARCO-MAE-0001`, ninguna de las dos escrita hoy), el brazo de `B` es `PERSISTENCIA` porque es el que la `0002` compara y el único con cobertura 10, y las columnas de `celdas.tsv` son las que ya existen. **Ninguna decisión de esta spec depende de un valor observado**, y ninguna se puede recalibrar después: lo no fijado aquí no existe.

Lo que esta contaminación **sí** cuesta, dicho sin descuento: esta corrida **no puede sorprender**. Su valor es de registro —congelar la tabla con su `n`, su lista, su control y su rótulo— no de descubrimiento. Se declara así en `§4`.

### 0.3 · Lo que se leyó, y con qué (A.13)

`celdas.tsv` (14 filas, por columna, con `csv.DictReader`); `resultados.json` de `CALC-B-MARCO-MAE-0001` (155 `RESULT`) y de `CALC-TRIADA-0002` (por llave, sólo las cinco citadas en §0.1); `marco-M-sorteado-v1_3.tsv` (14 `id`); `forense/no-corrido.tsv` (filas `NC-0152`, `NC-0180`, `NC-0187` por columna); `forense/firmas-pendientes.tsv` (fila `FP-374`); `tools/corrida0.py` (regla `E.1`, `_cuenta_gen2_resuelto`, herencia por cadena). **No se abrió** microdato, `corridas-R/M/L`, `L-extraido-*` ni `M-*.json`.

---

## 1 · El universo, congelado antes de correr

**Criterio, único y previo:** una celda entra a `U_COMUN` si y sólo si tiene punto en **los cuatro** corredores, es decir `en_u3 = SI` en `celdas.tsv` **y** `RESULT-BM-MAE-<celda>-PERSISTENCIA-ERR-PP` no nulo. Nada se imputa; ninguna celda se rellena; ninguna se sustituye.

| celda | en `U3` | `B` PERSISTENCIA | en `U_COMUN` | razón si no |
|---|---|---|---|---|
| `CIV-M-01` · ENVIPE 2012 | SÍ | SÍ | **SÍ** | — |
| `CIV-M-02` · ENVIPE 2013 | SÍ | SÍ | **SÍ** | — |
| `CIV-M-04` · ENVIPE 2015 | SÍ | SÍ | **SÍ** | — |
| `CIV-M-10` · ENVIPE 2021 | SÍ | SÍ | **SÍ** | — |
| `CIV-M-12` · ENVIPE 2023 | SÍ | SÍ | **SÍ** | — |
| `CIV-M-13` · ENVIPE 2024 | SÍ | SÍ | **SÍ** | — |
| `FAM-M-05` · ENIGH 2016 | SÍ | SÍ | **SÍ** | — |
| `FAM-M-06` · ENIGH 2018 | SÍ | SÍ | **SÍ** | — |
| `FAM-M-07` · ENIGH 2020 | SÍ | SÍ | **SÍ** | — |
| `TRA-M-07` · ENCIG 2021 | **NO** | SÍ | NO | `FUERA-DE-U3` — `L_CORPUS` se abstuvo válidamente 8/8 (`NC-0152`) |
| `FAM-M-01` · ENIF 2018 | SÍ | **NO** | NO | `SIN-B-PERSISTENCIA` — batería 9.9 nace en 2018 (`prereg-caja-B-MARCO` §1) |
| `TRA-M-02` · ENCUCI 2020 | SÍ | **NO** | NO | `SIN-B-PERSISTENCIA` — ENCUCI tiene una sola ola (ídem) |
| `TRA-M-03` · ENCIG 2013 | SÍ | **NO** | NO | `SIN-B-PERSISTENCIA` — reactivo ausente en ENCIG 2011 (ídem) |
| `DIN-M-01` · ENNViH 2002 | **NO** | **NO** | NO | `FUERA-DE-U3-Y-SIN-B` — primera ola del panel; `L_CORPUS` abstenida (`NC-0152`) |

**Cobertura congelada: `n(U_COMUN) = 9` de 14.** Las cinco ausencias se reportan con razón nominal y **no se rellenan**. Todo `MAE` de esta spec vive sobre esas 9 celdas y se publica **siempre** con su `n` y su lista (`A-bis.4`): **no es comparable** con el `MAE` de la `0002` (n=12) ni con el del asiento de `B` (n=10), y esta spec prohíbe citarlo como si lo fuera.

---

## 2 · La regla — heredada, no elegida

1. **Estadístico.** `MAE_pp(corredor)` = media simple de `abs(err_pp)` sobre las 9 celdas de `U_COMUN`, en orden fijo de `id`. Es el mismo estadístico de `CALC-TRIADA-0002` (§Método) y de `CALC-B-MARCO-MAE-0001`; no se pondera, no se recorta, no se winsoriza.
2. **De dónde sale cada `|err_pp|`.** `L_SOLO`, `L_CORPUS` y `M`: las columnas `error_abs_l_solo_pp`, `error_abs_l_corpus_pp` y `error_abs_m_pp` de `celdas.tsv`, tal cual. `B`: el valor absoluto de `RESULT-BM-MAE-<celda>-PERSISTENCIA-ERR-PP` del asiento sellado.
3. **Brazo de `B`: `PERSISTENCIA`, y sólo ése.** Es el brazo con cobertura 10 (`OPERATIVO` cubre 5) y el que `prereg-caja-B-MARCO` §3 define contra el corte temporal que la tríada usa. `OPERATIVO` **no entra** a esta spec, ni siquiera como nota.
4. **Guardia de identidad.** Las 14 filas de `celdas.tsv` son exactamente los 14 `id` de `marco-M-sorteado-v1_3.tsv`, o el medidor levanta y no hay corrida.
5. **Orden de reporte de corredores:** `B`, `L_CORPUS`, `L_SOLO`, `M` — fijado aquí para que el desempate de la ordenación descriptiva sea determinista y no dependa del resultado.

---

## 3 · Lo que emite el CALC

`RESULT-TBP-…`: guardia de identidad (`-N-CELDAS-MARCO`); `U3` re-derivado (`-U3-N`, `-U3-IDS`); el control de derivación por corredor (`-U3-CONTROL-<c>-{DERIVADO-PP,SELLADO-PP,DELTA-PP,RAMA}`) y `-U3-CONTROL-VEREDICTO`; cobertura de `B` (`-COBERTURA-B-PERSISTENCIA`, `-COBERTURA-B-IDS`); `U_COMUN` (`-UCOMUN-N`, `-UCOMUN-IDS`); por celda del marco, `-<celda>-EN-UCOMUN`, `-<celda>-RAZON-EXCLUSION` y `-<celda>-ERR-ABS-<c>-PP` para los cuatro; los cuatro `-UCOMUN-MAE-<c>-PP`; `-UCOMUN-ORDEN-DESCRIPTIVA`; `-UCOMUN-N-CELDAS-B-MENOR-QUE-M`; `-VEREDICTO`; `-TRIADA-VEREDICTO-VIGENTE` (citado intacto); y los cuatro contadores de lo no hecho: `-PAREADAS-NUEVAS`, `-IC-NUEVOS`, `-ADOPCIONES`, `-LLAMADAS-A-MODELO`, **todos `0` por construcción**.

---

## 4 · B-bis — lo que se lee, escrito ANTES de correr

### 4.1 · Control de derivación — tres ramas y su consecuencia

El acto **deriva, no hereda**. La prueba de que derivó es que, recalculando desde `celdas.tsv` sobre `U3`, salgan los `MAE` que la `0002` selló:

| rama | criterio sobre `abs(Δ)`, con `Δ = derivado − sellado` | consecuencia, escrita antes de correr |
|---|---|---|
| `REPRODUCE-EXACTO` | `abs(Δ)` ≤ `1e-9` pp | la derivación es la misma cuenta; la tabla común se emite |
| `REPRODUCE-AL-CENTESIMO` | `abs(Δ)` < `0.005` pp (umbral **estricto**) | la derivación coincide al centésimo, que es la precisión que el lanzamiento exige; la tabla común se emite, y la diferencia residual se reporta |
| `NO-REPRODUCE` | `abs(Δ)` ≥ `0.005` pp | **la tabla común NO se emite.** `-VEREDICTO = NO-DERIVA-CONTROL-FALLA`, los cuatro `MAE` salen `null`, y el acto entrega un `NC` en vez de una tabla |

**Precedencia, fijada al sellar y no después** (`B-bis`, regla de precedencia): si dos ramas pudieran satisfacerse a la vez, manda la más estricta. Si los tres corredores no caen en la misma rama, manda **la peor** de las tres para el veredicto del control. Un `U_COMUN` vacío no es una rama del control: es `-VEREDICTO = NO-EMITE-UCOMUN-VACIO`, porque un `MAE` de cero celdas no es un `MAE`.

### 4.2 · Qué significa el resultado, y qué no — la fila que faltaba

`B-bis` v2.4 existe porque una escala que sólo sabe anotar refutaciones describe mal el estado de validación. Esta corrida **no tiene falsador**, y se declara así antes de verla: **el resultado es descriptivo. No refuta ni corrobora nada.**

- **Si `B` queda primero en la ordenación** —que es lo que §0.2 dice que ya se sabe— eso **no** refuta a `M`, **no** refuta a `L`, **no** invierte `SIN-GANADOR-UNICO` y **no** corona a `B`. Cuatro medias sobre nueve celdas, sin IC y sin pareadas, no discriminan: `CALC-TRIADA-0002` ya declaró `INCONCLUSO` las tres pareadas sobre un universo **mayor**, y recortar de 12 a 9 celdas no añade poder, lo quita. Lo único que la tabla acredita es **cuánto yerra cada corredor sobre el universo donde los cuatro compiten**, con su `n` y su lista.
- **Si `B` no quedara primero**, tampoco corrobora a `M`: la misma frase, con los nombres cambiados.
- **Lo que sí cambia de estado**, y es el producto: `NC-0180` pedía «ninguna corrida de tríada con `B` de cobertura real» y esta la produce; `NC-0187` pedía el consumidor declarado de los `RESULT` de `B-MARCO` —la tríada, no el motor— y esta corrida **es** ese consumidor. Ambas cierran **por producto**, no por adjudicación.
- **Lo que queda pendiente y esta corrida no toca:** el valor predictivo añadido de `M` (`D-1`) sigue **por demostrar**; `SIN-GANADOR-UNICO` sigue vigente; `B-MARCO` se consume aquí y no vuelve a consumirse.

### 4.3 · Lo derivable de metadatos ya leídos — declarado como derivación, no como pronóstico

De `§0.1` se sigue aritméticamente, sin correr nada, que `-U3-N = 12`, `-COBERTURA-B-PERSISTENCIA = 10` y `-UCOMUN-N = 9`, con la lista de `§1`. Se escribe aquí para que no se lea después como hallazgo.

---

## 5 · Lo que esta spec explícitamente NO autoriza

1. **No adjudica, no corona, no ordena con consecuencia.** La ordenación sale rotulada `ORDEN-DESCRIPTIVA` y el veredicto es `NO-ADJUDICA-POR-DISENO`.
2. **No corre pareadas ni IC nuevos.** `-PAREADAS-NUEVAS = -IC-NUEVOS = 0`, verificable en `resultados.json`.
3. **No re-corre la tríada** ni toca `CALC-TRIADA-0002`, sus `RESULT` ni su veredicto.
4. **No redefine `B`** ni toca `CALC-B-0001`, `CALC-B-MARCO-*` ni sus pre-registros.
5. **No adopta** (`T9`): ninguna cifra suya entra a una regla del motor; `-ADOPCIONES = 0` y `usos.tsv` no recibe filas. `NC-0187` cierra por **consumo**, y el precedente no se generaliza.
6. **No llama a ningún modelo** (`-LLAMADAS-A-MODELO = 0`), no abre microdato y no descarga nada.
7. **No usa el brazo `OPERATIVO`** de `B`, ni lo reporta.
8. **No habilita `F6`** ni cambia el protocolo de `FP-374`.
9. **No recalibra nada tras ver resultados.** Lo no fijado aquí no existe.
10. **No firma por mesa, y no disfraza el contador.** `cuenta_gen2 = SI` se escribe en `data/corrida0/decisiones.tsv` citando **verbatim** la firma de contador con objeto del lanzamiento del 15/sep/2026. Y se declara lo que la firma está pasando por encima: la regla `E.1` marca esta corrida **`envuelto_legacy = SI` por cadena** (consume `RESULT` de `CALC-B-MARCO-MAE-0001` y `CALC-TRIADA-0002`, ambos lectores de `corridas-R/`), de modo que **sin firma el registro la resolvería `NO`**. `prereg-caja-B-MARCO` §7.7 declinó firmar sobre un envuelto —«forzar la firma sobre un envuelto sería miscategorizar para mover un contador»—; **esta spec se aparta de ese precedente por decisión explícita y más reciente de mesa**, que es la precedencia 1 del propio `corrida0.py` (`_cuenta_gen2_resuelto`). La desviación se registra aquí, en `spec.md` y en la nota de cierre, para que el contador **nunca** se lea como derivado por la máquina.

---

## 6 · Sello

Esta spec queda congelada en el `COMMIT-1` del `ACTO GEN2-F5-CIERRE-Y-PANEL-1`, junto con `medidor.py` (probado sólo sobre datos **sintéticos**: 18 aserciones en `pruebas-sinteticas.py`, incluidas las tres ramas del control, `U_COMUN` vacío y la guardia de identidad), `spec.md` y `spec.yaml`. **El primer resultado que produzca este procedimiento es el que se reporta.** El `COMMIT-2` sella.
