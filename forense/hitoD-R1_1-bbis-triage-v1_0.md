# Ficha B-bis de re-triage — `R1.1` · v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R1_1-bbis-triage-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R1.1-bbis`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La ficha B-bis propia que la **Entrada 3** de `registro-recalculo` exige para el veredicto `D` de `R1.1`: volatilidad → horizonte corto, falsador de participación voluntaria en Fondos de Aseguramiento agrícola |
> | **QUÉ NO ES** | **No adjudica, no emite y no retira ningún veredicto `RX.Y`.** El veredicto `D` de `R1.1` sigue archivado donde siempre, en el bloque append-only de `hitoD-preregistro` (ADR-40); esta ficha no lo toca ni reproduce su forma canónica. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | trae la escala de re-triage completa (4 filas + precedencia), la pregunta de la Entrada 3 contestada con cita, y una sola fila asignada. |

**Acto:** `ACTO E3-TRIAGE`, 18/ago/2026, entorno NUBE (repo-only), sobre `origin/main = f3d3f95`.
**Encargo:** `forense/encargos/2026-08-18-E3-TRIAGE.md` (`FP-14`, firmada-condicional `ADR-91`, `PR #246`).
**Criterio, verbatim de la Entrada 3** (`forense/registro-recalculo-v1_0.md` §1, fila 3): *"archivo por hueco de diseño: hay que preguntar si el hueco era de instrumento y el instrumento estaba en disco"*.

---

## La pregunta de la Entrada 3, en dos partes

### 1 · ¿El hueco era de instrumento? — **SÍ, y de dos capas.**

El `D` de `R1.1` se archivó por **hueco de mercado**, no de dato: el Seguro Agrícola Catastrófico
no lo contrata el productor de temporal (SADER, textual), y los Fondos de Aseguramiento concentran
62 % de fondos y 66 % de cobertura en Sonora-Sinaloa-Tamaulipas — riego, tecnificado, gran
extensión, no la población de volatilidad máxima. Cero de seis candidatos sobrevivieron al confusor
pre-registrado (Nota 5, `hitoD-preregistro-v2_0.md:454`; detalle en `hitoD-R1_1-veredicto-v1_0.md`).

Sobre ese hueco de mercado quedó, además, un **hueco de instrumento con reserva declarada y nunca
cerrada**: `forense/cruce-catalogo-fichas-v2_0.md` §3.1 marca la condición *"participación
voluntaria ≥3 ciclos en Fondos de Aseguramiento agrícola, por productor y ciclo"* como
**"NO EXISTE, con reserva declarada — no se buscó específicamente un padrón de Fondos de
Aseguramiento Agrícola/AGROASEMEX"**. Esa reserva es lo que la Entrada 3 puede contestar hoy y no
podía el 4/ago.

### 2 · ¿El instrumento estaba en disco? — **SÍ. Cuatro payloads, íntegros, inspeccionados a E2.**

Medido contra `data/curacion-universo/ledger-inspecciones-barrido2.tsv` (672 filas, `sha256`
`81b72932b406753a…`), filtrando por `payload_id`:

| `payload_id` | `ruta_relativa` | `estado_e0` | grado | `objetos_e2` | terminal |
|---|---|---|---|---|---|
| `conf17_r1_1_padron_fondos_agroasemex` | `R1_1_AGROASEMEX/padron_integrantes_sistema_nacional_aseguramiento_agropecuario.csv` | `PRESENTE-INTEGRO` | `E2` | 5 | `SI` |
| `conf17_r1_1_paa_componente_apoyo` | `R1_1_AGROASEMEX/PAA_componente_apoyo.csv` | `PRESENTE-INTEGRO` | `E2` | 6 | `SI` |
| `conf17_r1_1_paa_componente_subsidio_agricola` | `R1_1_AGROASEMEX/PAA_componente_subsidio_ramo_agricola.csv` | `PRESENTE-INTEGRO` | `E2` | 8 | `SI` |
| `conf17_r1_1_paa_componente_subsidio_ganadero` | `R1_1_AGROASEMEX/PAA_componente_subsidio_ramo_ganadero.csv` | `PRESENTE-INTEGRO` | `E2` | 9 | `SI` |

**El padrón que la reserva de `cruce-catalogo-fichas` daba por no buscado está en disco desde el
5/ago/2026, descargado, registrado en el manifiesto y verificado byte a byte.** La reserva queda
cerrada por este acto — en el sentido material, no en el semántico: se buscó, se encontró, se
bajó.

### 3 · ¿Construye la condición del Umbral? — **NO, y está leído, no inferido.**

`CONF-17` corrida B (`forense/notas/2026-08-05-conf17-fetch-corrida-B.md:378-402`) abrió los cuatro
CSV completos y leyó sus encabezados:

```
padron_integrantes...csv:      47848 bytes | clave,nombre_fondo,estado,municipio
PAA_componente_apoyo.csv:     210586 bytes | beneficiario,apoyo,anio,importe,moneda
PAA_...ramo_agricola.csv:    1553774 bytes | ejercicio,mes,subsidio,cultivo,superficie_asegurada,estado,municipio
PAA_...ramo_ganadero.csv:    1153815 bytes | anio_pago,mes_pago,subsidio,especie,cabezas_aseguradas,unidades_aseguradas,estado,municipio
```

Tres hechos, verbatim de esa lectura, cada uno matando una pieza del Umbral:

1. **Ninguno de los cuatro tiene identificador de productor individual** (folio, nombre, CURP/RFC).
   El padrón está a nivel **Fondo/asegurador**; los tres "componente" están agregados por
   estado/municipio/cultivo-o-especie/año-mes. El Umbral pide *"por productor y ciclo"*.
2. **El campo temporal del archivo agrícola es `ejercicio,mes`** — año calendario y mes, **no**
   ciclo agrícola primavera-verano/otoño-invierno. El Umbral pide **ciclos**, y "≥3 ciclos" sobre
   un eje fiscal no es la misma cantidad.
3. **Ninguna columna, en ninguno de los cuatro, distingue voluntario de obligatorio-atado-a-crédito**
   — que es exactamente el confusor pre-registrado de la ficha (AMUCSS, textual), el que ya había
   matado a los seis candidatos.

Correcciones que este re-triage hereda y hace suyas, sin rehacerlas: la premisa de segunda mano
*"el padrón por productor sí existe y es descargable"* **no se sostiene** contra los archivos
reales (CONF-17 corrida B, mismo tramo). Ese es el hallazgo que convierte la reserva en medición.

## Escala de re-triage — cuatro filas mutuamente excluyentes, con regla de precedencia estricta

Declarada íntegra en cada una de las siete fichas de este acto (no por referencia: la escala de la
ficha gobierna sobre cualquier legend genérico, y hay que decirlo en la ficha — Bloque B-bis,
`instrucciones-proyecto-v2_10.md:113`).

| fila | significa |
|---|---|
| `T-1 · D SOSTENIDO — sin instrumento en disco` | el hueco es de instrumento, y **ninguna** pieza candidata aparece en el ledger durable de las 672 representaciones inspeccionadas. El disco no tiene nada que decir. |
| `T-2 · D SOSTENIDO — instrumento en disco, no construye la condición` | la pieza candidata **sí** está en disco, `PRESENTE-INTEGRO`, grado `E2`, terminal `SI`, y su lectura directa ya archivada muestra que no construye la condición del Umbral. |
| `T-3 · D SOSTENIDO CON RAZÓN CORREGIDA` | el veredicto se sostiene, pero al menos una de las razones escritas en su Nota de archivo es **falsa** contra el instrumento real, medido. |
| `T-4 · D RE-ABRIBLE` | la pieza está en disco y su lectura directa **sí** construye la condición: el `D` deja de ser inejecutable y pasa a mesa. |

**Regla de precedencia, fijada al sellar y no después:** `T-4` manda sobre las tres. `T-3` manda
sobre `T-1` y `T-2` cuando ambas aplican — una razón falsa se declara aunque el veredicto no se
mueva, porque el archivo de un `D` es su razón, no solo su letra.

**Qué significa que el re-triage NO reabra** (obligación propia del Bloque B-bis: declarar el
desenlace de no-refutación antes de correr): que el `D` era correcto y **además** hoy es
correcto contra un disco medido, no contra un catálogo. Eso es un resultado, no un no-resultado:
sube el `D` de "no encontramos el instrumento" a "el instrumento está aquí, íntegro, y no
construye la condición". Es el desenlace más informativo de los cuatro para `T-2`, y el que
esta escala existe para poder anotar.

**Límite duro del criterio, declarado antes de aplicarlo.** "En disco" se decide contra
`data/curacion-universo/ledger-inspecciones-barrido2.tsv` — 672 filas, todas `PRESENTE-INTEGRO`
y `estado_terminal=SI`, gate material cerrado por `ACTO GATE-DURABLE-V7` (`ADR-103`, `PR #260`).
Ese ledger decide **a granularidad de representación/payload**, que es exactamente la
granularidad que la pregunta de la Entrada 3 pide ("¿estaba el *instrumento* en disco?"). No
decide a granularidad de variable: el índice E2 completo (1 331 710 registros, ~2.1 GB) vive solo
en `.barrido2/`, gitignorado, fuera de este entorno — y aun estando, conserva evidencia semántica
en el 4.09 % de sus registros (`forense/hallazgos.md:333`). Donde este acto necesita nivel de
variable, **cita una lectura directa ya archivada; no la rehace ni la sustituye por inferencia.**

---

## Fila asignada

**`T-2 · D SOSTENIDO — instrumento en disco, no construye la condición`.**

`T-4` no aplica: los cuatro recursos, leídos, no construyen ninguna de las tres piezas del Umbral.
`T-1` no aplica: el instrumento sí está en disco, y decirlo importa — cambia el archivo de
"no se buscó" a "se buscó, está aquí, no sirve para esto". `T-3` no aplica: ninguna razón escrita
en Nota 5 resultó falsa; el hueco de mercado sigue siendo el hueco de mercado.

**Lo que este re-triage cambia y lo que no.** No cambia el veredicto ni el contador. Cambia el
estado de una reserva: `cruce-catalogo-fichas-v2_0.md` §3.1 podía leerse como "quizá el padrón
existe y nadie fue a ver". Hoy se fue a ver, está en disco íntegro, y la respuesta es no. Ese
documento es append-only y **no se edita**; esta ficha es donde vive la respuesta.

**Qué haría falta para reabrir `R1.1`:** un padrón nominal por productor y ciclo agrícola, con
marca de voluntariedad — ninguno de los cuatro recursos públicos de AGROASEMEX lo es, y el hueco
de mercado seguiría en pie aunque apareciera.
