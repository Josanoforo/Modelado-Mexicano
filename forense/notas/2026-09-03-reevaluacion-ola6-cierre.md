# Cierre — `ACTO MAESTRA34-N5 · RE-EVALUA-OLA6`

Encargo: `forense/encargos/cola/2026-09-01-MAESTRA34-N5-RE-EVALUA-OLA6.md`
(dirección/Fable, maestra-34, 1/sep/2026, SHA de redacción `9d2e69d`).
Ejecutado 3/sep/2026 con `/acto` (`ADR-237`) invocado desde `/despacha`
(`ADR-239`), rama `claude/despacha-MAESTRA34-N5`, base `origin/main =
8fc70f4`. **Relanzamiento de `ACTO MAESTRA33-E14`** (`ADR-265`,
`forense/notas/2026-09-01-evaluacion-ola6-cierre.md`) con la precondición
que entonces era **«lógicamente imposible»** ya satisfecha.

## ARRANQUE

- **REPO** `/home/user/Modelado-Mexicano`, clon existente (no se clonó
  nada). Árbol limpio al arrancar.
- **SHA** base `8fc70f4`; el encargo se redactó contra `9d2e69d`. **`main`
  se movió** entre ambos — no es PARO: se refrescó antes de leer la cola
  y se re-derivó todo contra `8fc70f4`. Lo que ese movimiento trae es
  precisamente `MAESTRA36-N2`/`PR #503`, que es lo que destraba la
  compuerta.
- **`data/raw`** ausente (`ls data/raw/` → 0 archivos). No es PARO y **no
  se creó ni se enlazó**: este acto no abre microdato ni descarga nada.
- **ENTORNO (A.2, tres partes, crudas)** —
  `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` ·
  `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/`
  → **`000`** (sin salida a INEGI) · `ls data/raw/ | wc -l` → **0**
  (corpus compartido **no** montado). Los tres son los esperados en nube y
  ninguno bloquea: las 75 búsquedas de P2 corren sobre metadato
  versionado, no sobre payloads.
- **ESPEJO** no se consultó. Toda cifra de esta nota sale del clon, con
  el comando a la vista.

## COMPUERTA — CUMPLE

`COMPUERTA: MAESTRA34-N3 fusionado en origin/main con
scoreboard-v1_2-AGREGADO.md que traiga puntos L sobre celdas de los
CUATRO dominios activos (…) verifica por producto`.

Verificada **por producto**, no por `git log --grep` (`ADR-277`):

```
$ git show origin/main:forense/prereg-duelo-v2/scoreboard-v1_2-AGREGADO.md | grep -c DIN-M
8
$ … CIV-M → 14   · … FAM-M → 9   · … TRA-M → 4
```

Los cuatro `> 0`. El archivo existe en `origin/main` y lo trajo
`ACTO MAESTRA36-N2 · CIERRA-N3-AGREGA-2` (`PR #503`), que es el ejecutor
real de `MAESTRA34-N3`.

## P1 · Criterio 1 de `§3.a` — **CUMPLE, por primera vez desde que se selló**

`§3.a` criterio 1 exige un agregado publicado con puntos de **`L`** —no
sólo `M`/`R`— sobre los cuatro dominios `ACTIVO` **simultáneamente**.

Universo: **14 celdas** de `marco-M-sorteado-v1_2.tsv`, todas puntuadas
(`0` en `VERIFICACION-NO-PUNTUA`, `0` en `AMBIGUA-POR-DISEÑO`). Celdas con
punto de `L` por dominio, contadas sobre la tabla §1 del scoreboard:

| dominio `ACTIVO` | celdas en el universo | con `L-solo` | con `L+corpus` | ≥1 punto de `L` |
|---|---|---|---|---|
| cívico (`CIV-M`) | 6 (`01,02,04,10,12,13`) | 5 | 6 | **SÍ** |
| dinero (`DIN-M`) | 1 (`01`) | 1 | 1 | **SÍ** |
| familia (`FAM-M`) | 4 (`01,05,06,07`) | 4 | 4 | **SÍ** |
| trámite (`TRA-M`) | 3 (`02,03,07`) | 3 | 3 | **SÍ** |
| **total** | **14** | **13** | **14** | **4 de 4 dominios** |

`CIV-M-04` es la única sin `L-solo` (sus 8 réplicas son todas
`NO-EXTRAIBLE`); sí tiene `L+corpus`, así que no rompe el criterio ni por
celda ni por dominio.

**Veredicto P1: CUMPLE.** Y con eso cae la frase que gobernaba a
`MAESTRA33-E14` — «antes de que `L` tenga al menos un agregado publicado,
ningún candidato de Ola 6 puede evaluarse contra este criterio». Ya no es
imposible: ahora es evaluable, y por eso este acto sí evalúa.

⚠️ **Lo que P1 NO dice.** El criterio 1 pide que **existan puntos de
`L`**, no que digan algo favorable. Dicen lo contrario: los tres
corredores sobre-estiman `R` masivamente (mediana `|z|` 11.43 / 11.16 /
29.19; **1 de 14** celdas en banda), y la comparación principal
`L_SOLO_vs_M` sale **`INDETERMINADO`** (IC `[-74.02, +9.40]`, cruza cero).
El criterio 1 es de **existencia de medición**, no de calidad de ajuste, y
se lee como está escrito — pero mesa merece leer las dos cosas juntas.

## P2 · Criterio 2 re-derivado — `/mapea` dirigido, **0 de 6 CUMPLEN**

Detalle completo, 25 reglas × ≥3 formulaciones, en
`forense/notas/2026-09-03-mapeo-ola6-N5.md`. **Universo declarado en cada
corrida (A.13): 241 591 filas** (`inventario-reactivos-v1_2` 178 246 +
`-ext-v1_0` 63 345). Ninguna abrió microdato.

| dominio | (i) ≥2 encuestas en corpus | (ii) ≥3 `EXISTE-SATISFACE` | criterio 2 |
|---|---|---|---|
| `salud` | CUMPLE (2) | **1** — `salud.atencion.grave` | **NO-CUMPLE** |
| `información` | CUMPLE (2) | **1** — `salud.vacunacion.disponible` | **NO-CUMPLE** |
| `trabajo` | CUMPLE (3) | **0** | **NO-CUMPLE** |
| `cooperación` | CUMPLE (3) | **0** | **NO-CUMPLE** |
| `comunicación` | NO-CUMPLE (1) | **0** | **NO-CUMPLE** |
| `tiempo` | NO-CUMPLE (0) | **0** | **NO-CUMPLE** |

**(i) se re-declara, no se re-deriva, y se dice.** La tabla rule-level de
`forense/notas/2026-07-31-inventario-segmentacion.md` sigue siendo del
31/jul/2026, y el caveat que `MAESTRA33-E14` levantó —ENDUTIH/ENASEM/
ENTI/ENADID/ENBIARE entraron después sin cruce regla-por-regla— **sigue
en pie**. Lo que este acto puede afirmar sobre esas fuentes es lo que P2
midió: **ninguna de ellas aparece como candidata en ninguna de las 25
reglas**, en 75 formulaciones. Eso es evidencia de que re-correr el cruce
no movería (ii), no prueba de que no movería (i). Se declara así.

**Ver `MAESTRA34-A1`:** el encargo pide incluir lo que ese acto haya
registrado (Cero Desabasto, Observatorio de Cuidados, CNGMD, DGIS, SICEE)
**si ya fusionó, verificado por manifiesto**. No fusionó: ninguna de las
cinco aparece en `data/manifiesto.yaml`, y el mapeo de
`salud.adherencia.desabasto_vs_cuidadora` —que es justo la regla que Cero
Desabasto tocaría— sale `NO-ENCONTRADO` con **0/241 591**. Se declara la
ausencia, no se cuenta lo que no está.

## P3 · Criterio 3 · caja — **LIBRE, declarado y no ejercido**

El encargo prohíbe ejercer la caja (`ENTORNO: NUBE`, «el criterio 3 se
DECLARA, no se ejerce»). Derivado sin abrirla, contra `origin/main`:

- Encargos de la cola con `ENTORNO: CAJA` o `ENTORNO: UBUNTU`: **1 sobre
  6 archivos examinados** —
  `2026-09-01-MAESTRA34-L2-ARBITRA-v1_2.md`, y está **`CONSUMIDO`**.
  Ninguno pendiente.
- Ramas de acto abiertas en el remoto: `git ls-remote --heads origin` →
  **2 refs**, `main` y la de este tick. Ninguna otra sesión en vuelo.

**Caja LIBRE por ambos comprobantes.** Con la cota superior que ya declara
`/despacha`: `gh` no existe en este entorno, así que la **rama** es cota
superior segura del PR y «sin rama» implica «sin PR abierto sobre ella».
Lo que esto NO establece: que la máquina Ubuntu física esté encendida y
disponible — eso no es derivable desde la nube y no se finge.

## P4 · Veredicto por dominio candidato

| dominio | crit. 1 | crit. 2 | crit. 3 | **veredicto** | qué falta |
|---|---|---|---|---|---|
| `salud` | CUMPLE | **NO** (1/3) | LIBRE | **NO-CUMPLE** | 2 reglas más `EXISTE-SATISFACE`. Las dos más cercanas (`leve_sin_imss`, `prevencion.hombre_sin_permiso`) fallan por **antecedente no instrumentado**, no por payload faltante |
| `información` | CUMPLE | **NO** (1/3) | LIBRE | **NO-CUMPLE** | 2 más. `deferencia.costo_acceso_experto` y `escuela.miedo_a_caer` fallan por disparadores que el canon **ya declara no observados** |
| `trabajo` | CUMPLE | **NO** (0/3) | LIBRE | **NO-CUMPLE** | 3. Ninguna regla del dominio tiene desenlace medido; `jefe` en el corpus es siempre **jefe de hogar** |
| `cooperación` | CUMPLE | **NO** (0/3) | LIBRE | **NO-CUMPLE** | 3. Desenlaces sí medidos (tanda, membresía); **los tres disparadores de vínculo, cero** |
| `comunicación` | CUMPLE | **NO** (0/3) | LIBRE | **NO-CUMPLE** | 3, más una segunda encuesta para (i). El desenlace «directividad del habla» no existe en 241 591 filas |
| `tiempo` | CUMPLE | **NO** (0/3) | LIBRE | **NO-CUMPLE** | 3, más (i) desde cero. Único con faltante **real de dato**; la búsqueda quedó cerrada 0/8 fuentes el 31/jul |

**Ningún dominio queda `ABRE-PROPUESTO`. Cero de seis.** En consecuencia
**no se redacta ningún lote `REGLAS-OLA6-<dominio>-L1`**: el encargo los
pide «para cada `ABRE-PROPUESTO`», y no hay ninguno. No es una omisión
del ejecutor — es el condicional del propio encargo evaluándose en falso.

**Este acto no cambia ningún dominio a `ACTIVO`, y no podría**: la
apertura la firma mesa.

### Lo que cambió de verdad entre `MAESTRA33-E14` y hoy

`MAESTRA33-E14` cerró con **el mismo veredicto y una razón distinta**.
Entonces: criterio 1 imposible (`L pendiente 11 de 11`) y criterio 2 sin
buscar. Hoy: **criterio 1 CUMPLE** y **criterio 2 buscado, dirigido, y
sigue sin cumplirse**. El bloqueo se movió de «falta medir `L`» a «faltan
instrumentos para los disparadores», y eso es información nueva aunque el
veredicto se lea igual — es la diferencia entre un no-sé y un no.

### La pregunta que este acto deja a mesa, y no responde

Las 23 reglas que no llegan se reparten en **13 `NO-ENCONTRADO`** (hueco
de dato) y **10 `EXISTE-NO-SATISFACE`** (hueco de **instrumento**: el
corpus mide el desenlace y no el disparador). Adquirir más encuestas de
INEGI del mismo tipo mueve las primeras y **no** mueve las segundas,
porque INEGI levanta estructura y conducta, y estas reglas condicionan
sobre percepción y vínculo. Si eso es así, **el criterio 2 de `§3.a` puede
no ser alcanzable por adquisición** para varios de los seis. Cambiar el
criterio es de mesa; este acto sólo mide que el patrón está ahí, en 10 de
25 filas.

## `FP-220`

Ya estaba `EJECUTADA` por `MAESTRA33-E14`. **No se reabre ni se
re-resuelve**: se le añade el recibo de esta segunda evaluación en su
propia columna, con el cambio de razón. `FP-220` sigue `EJECUTADA`.

## CONTADOR

**Cero, declarado desde el encargo.** Ningún dominio abierto
(`milpa/tramite.yaml` sin diff), ninguna regla cargada, ninguna medición
corrida, ningún lote lanzado ni redactado, `marco`/`corridas-M`/
`corridas-R`/`corridas-L` sin tocar. Este acto **propone y no decide**.
El del despacho que lo ejecutó: también cero.

## Lo que este acto NO hizo

No abrió ningún dominio de Ola 6; no activó el corredor `E`; no tocó los
criterios de `§3.a` (la enmienda es **fechada y aparte**, no los
reescribe); no abrió microdato ni descargó nada; no ejerció la caja; no
redactó ni encoló ningún encargo; no editó `tools/extrae_l_v1_1.py`,
`agregado_v1_1.py` ni el scoreboard; no re-corrió el cruce rule-level del
31/jul (lo declaró pendiente).
