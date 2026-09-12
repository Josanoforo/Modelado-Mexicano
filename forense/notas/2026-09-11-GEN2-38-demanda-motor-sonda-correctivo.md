# GEN2-38 · correctivo demanda del motor → SONDA

Fecha de corte: 2026-09-11, `America/Mexico_City`.

## Universo y precedencia

`tools/adq_investigacion.py` reconstruye la demanda desde siete insumos
versionados: NC canónicas, usos y RESULT vigentes, demanda GEN1 antecedente,
decisiones de mesa, mapa necesidad→objeto y utilidad-modelo. La vista publica
el SHA de cada insumo y no edita ninguno de esos registros.

El corte contiene 16 consumidores GEN2 activos y 51 NC abiertas. Las seis NC
con contrato científico completo lo conservan. Las otras 45 reciben un
contrato **mínimo derivado** que mantiene literalmente su pregunta, impacto y
sucesor, y añade etapa, responsable, siguiente acción y estado de ruteo. No
inventa población, unidad o periodo: cuando la NC no los declara quedan como
precondición explícita de una eventual evaluación, no como campos ausentes.

El selector sólo envía automáticamente a SONDA una NC abierta cuya propia
redacción acredita una brecha de fuente/variable y una acción de búsqueda sin
compuerta posterior. `DIFERIDO`, `SUSTITUIDO`, `DESCARTADO`, espera de mesa,
acceso con identidad, paro de entorno y frente delegado permanecen excluidos
con causa, responsable y siguiente acción. NC-0111 no se duplica: la decisión
D08 ya produjo su sucesora NC-0153 y el ruteo continúa allí.

## Situación de los 16 elementos vigentes

| elementos | situación efectiva | faltante/siguiente acción |
|---:|---|---|
| 3 (`RES-0046`, `RES-0048`, `RES-0065`) | adoptados en el registro pero bloqueados para emisión por NC-0126 | fuente/reactivo que separe tenencia de ahorro y duración; continuar SONDA desde el cursor público |
| 4 (`RES-0003`, `RES-0005`, `RES-0013`, `RES-0015`) | adoptados para su uso acotado; NC-0153 conserva la brecha prospectiva de tasa nacional evento×canal | espera de folio INEGI o vía pública concreta; no extrapolar ENEAC |
| 9 restantes | RESULT sellado, validación independiente `PASA` y adopción vigente; sin NC abierta enlazada al uso actual | mantener; reabrir sólo por nueva versión, evidencia contradictoria o cambio de uso |

Cada fila individual vive en `data/adq-demanda-activa-v1_0.json` y distingue:
antecedente GEN1, RESULT, validación, adopción, NC abiertas, utilidad-modelo,
decisiones posteriores, dependencias, evidencias y siguiente acción. Que una
regla no tenga relación exacta en `utilidad-modelo.tsv` se declara como tal y
no se interpreta como ausencia de datos.

## Correctivo suficiencia → consulta

`CONSULTA-GEN2-v2` ya no acepta `APTA_USO_DECLARADO` como autorización. La
guardia exige coincidencia exacta de necesidad, versión de pregunta,
consumidor, RESULT, uso aprobado y evidencia local reproducible. El bloqueo
sólo puede levantarse por:

1. `ADOPTA_SUCESOR_CALCULADO`, con RESULT distinto, `calculada=true` y
   `adoptada=true`; o
2. `AUTORIZA_RESULTADO_EXISTENTE`, decisión explícita para el RESULT actual.

En ambos casos la decisión y sus evidencias deben pertenecer al estado vigente.
El SHA del JSON observado, su validez, los hashes de evidencia, el vínculo y el
estado efectivo forman parte del hash contractual. Un estado de otra NC o de
otra versión se registra como descartado y se usa el bloqueo inicial.

## Revisión de aplazamientos y selección

- NC-0122: rutas generales ya recorridas; espera hasta octubre o una pista
  nueva concreta.
- NC-0153: la búsqueda general ya se agotó y existe expediente; espera acción
  humana/folio.
- NC-0164: #734 agotó las rutas declaradas; espera fuente mexicana exacta o
  decisión de preespecificación.
- NC-0136 y NC-0037: continúan bajo sus frentes dueños; SONDA no los duplica.
- NC-0126: ENIF/EACF/ENSAFI/Findex quedaron agotadas, pero ENFIH y
  cuestionarios públicos subnacionales u otras ediciones/módulos mexicanos no
  indexados seguían sin examinar. Se reabre desde ese cursor, sin repetir la
  búsqueda anterior.

Selección determinista previa al ciclo real: 51 abiertas, 51 con contrato
operativo, una lista para SONDA (`NC-0126`) y 50 exclusiones explicadas. Cero
tareas elegibles nunca se traduce en suficiencia general.

## Ciclo productivo

Pendiente de completar después del despliegue de esta revisión. No se repetirá
la búsqueda anterior ni se fabricará una descarga si las pistas resultan
incompatibles.
