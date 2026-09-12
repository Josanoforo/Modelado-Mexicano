# GEN2-38 · correctivo demanda del motor → SONDA

Fecha de corte: 2026-09-11, `America/Mexico_City`.

## Universo y precedencia

`tools/adq_investigacion.py` reconstruye la demanda desde siete insumos
versionados: NC canónicas, usos y RESULT vigentes, demanda GEN1 antecedente,
decisiones de mesa, mapa necesidad→objeto y utilidad-modelo. La vista publica
el SHA de cada insumo y no edita ninguno de esos registros.

El corte contiene **207 elementos activos del alcance aprobado**, no sólo los
16 ya adoptados en GEN2, y 52 NC abiertas. Las seis NC con contrato científico
explícito completo lo conservan; NC-0165 es un contrato operativo explícito no
científico. Las otras 45 reciben sólo una **descripción
mínima derivada** que mantiene literalmente pregunta, impacto y sucesor, y
añade etapa, responsable, siguiente acción y ruteo. Se contabilizan como
`contrato_cientifico_incompleto=45`: rellenar población, unidad o periodo con
advertencias genéricas no las convierte en contratos científicos completos.

La entrada al inventario es `activo=SI` en `data/corrida0/usos.tsv`; no depende
de `corrida0_generacion=GEN2`. Para 191 elementos todavía no adoptados, GEN1 se
publica únicamente como antecedente histórico y jamás como valor reactivado.
`tools/integra_demanda_motor_sonda.py`, mediante el escritor común
`tsv_crudo.upsert_fila`, dio de alta idempotente `NC-0165`: así cada brecha
preadopción queda enlazada al ejecutor MOTOR_GEN2 y sólo salta a SONDA cuando
el primer faltante verificado sea fuente/variable o acceso.

El selector sólo envía automáticamente a SONDA una NC abierta cuya propia
redacción acredita una brecha de fuente/variable y una acción de búsqueda sin
compuerta posterior. `DIFERIDO`, `SUSTITUIDO`, `DESCARTADO`, espera de mesa,
acceso con identidad, paro de entorno y frente delegado permanecen excluidos
con causa, responsable y siguiente acción. NC-0111 no se duplica: la decisión
D08 ya produjo su sucesora NC-0153 y el ruteo continúa allí.

## Mapa conciliado de los 207 elementos vigentes

| elementos | situación efectiva | faltante/siguiente acción |
|---:|---|---|
| 9 | `CUBIERTA` | mantener la adopción; reabrir sólo por evidencia o decisión nueva aplicable |
| 3 (`RES-0046`, `RES-0048`, `RES-0065`) | `PENDIENTE_DATOS_O_DECISION_DE_USO`; adoptados pero bloqueados por NC-0126 | conservar `NO_COVERAGE`; fuente/reactivo que separe tenencia y duración o decisión exacta aplicable |
| 4 | `PENDIENTE_ACCESO_O_DESCARGA` | conservar la barrera humana y el expediente; no extrapolar ni reiniciar búsqueda general |
| 144 | `PENDIENTE_PREPARACION` | MOTOR_GEN2 completa contrato/spec corriente antes de calcular; la receta legacy parcial es evidencia, no cobertura |
| 47 | `PENDIENTE_DECISION_CIENTIFICA` | mesa decide opciones concretas o el veredicto de una oferta ya calculada; `SIN-RECETA` no se disfraza de dato ausente |

Cada fila individual vive en `data/adq-demanda-activa-v1_0.json` y distingue:
antecedente GEN1, RESULT, validación, adopción, NC abiertas, utilidad-modelo,
decisiones posteriores, dependencias, evidencias y siguiente acción. Que una
regla no tenga relación exacta en `utilidad-modelo.tsv` se declara como tal y
no se interpreta como ausencia de datos.

## Correctivo suficiencia → consulta

`CONSULTA-GEN2-v2` no acepta `APTA_USO_DECLARADO` ni
`APTA_ALCANCE_MENOR` como autorización por sí solas. La
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

Para alcance menor se exige además un `vinculos_alcance_menor` exacto que una
consumidor, RESULT bloqueado, uso original y uso menor, más una decisión clase
`AUTORIZA_ALCANCE_MENOR_RESULTADO_EXISTENTE` con esos mismos campos y evidencia
reproducible. NC-0126 no tiene ese vínculo para `MEDICION-GEN2`: cambiar sólo
su etiqueta a `APTA_ALCANCE_MENOR` devuelve `NO_COVERAGE` y nunca materializa
`0.541343` como `horizonte_corto`.

## Revisión de aplazamientos y selección

- NC-0122: rutas generales ya recorridas; su condición efectiva queda
  registrada como fecha vigente vencida o evidencia nueva estructurada con NC
  y versión exactas; no reabre por palabras sueltas de la historia.
- NC-0153: la búsqueda general ya se agotó y existe expediente; espera acción
  humana/folio.
- NC-0164: #734 agotó las rutas declaradas; `ESPERA_NUEVA_PISTA` transita a
  `LISTA_SONDA` al vencer 2026-10-11 o por evidencia nueva estructurada. Una
  simulación al corte 2026-10-11 la selecciona primera por prioridad.
- NC-0136 y NC-0037: continúan bajo sus frentes dueños; SONDA no los duplica.
- NC-0126: ENIF/EACF/ENSAFI/Findex quedaron agotadas, pero ENFIH y
  cuestionarios públicos subnacionales u otras ediciones/módulos mexicanos no
  indexados seguían sin examinar. Se reabre desde ese cursor, sin repetir la
  búsqueda anterior.

Selección determinista del correctivo al 2026-09-11: 52 abiertas, 52 con
descripción/ruteo operativo y **cero listas para SONDA**. NC-0122, NC-0126 y
NC-0164 esperan al 11/oct; NC-0153 conserva acceso humano; NC-0165 está
delegada a MOTOR_GEN2; las demás exclusiones publican causa, responsable y
siguiente acción. Cero tareas elegibles nunca se traduce en suficiencia
general.

## Ciclo productivo

El recibo productivo previo se conserva sin repetir búsquedas agotadas. La tarea
`\ModeladoMexicano\AdquiereCron` ejecutó manualmente un ciclo real
con `run_id=2026-09-11T212121-2241921` sobre la revisión desplegada
`8a44e6b5faf690ceeb9c916bcb91fd699e4b3251`. Terminó con exit `0`, resultado
`descubrimiento_documentado` y publicación `OK`:

- la cola de adquisición tuvo cero objetos elegibles y 151 exclusiones; eso no
  se interpretó como suficiencia porque el selector científico eligió
  `NC-0126` y explicó las otras 50 NC;
- SONDA continuó desde ENFIH/subnacionales, sin repetir ENIF, EACF, ENSAFI ni
  Findex, y encontró la Encuesta de Inclusión Financiera IIEG Jalisco;
- se descargaron por duplicado y se incorporaron al corpus las tres bases
  públicas 2022–2024, se abrieron sus hojas de datos/descriptor y se registraron
  en `data/manifiesto.yaml`;
- la lectura mostró ahorro institucional del hogar separado en `ahorro`/`P6`,
  pero `cubrir_gastos`/`P14` conserva «Menos de una semana/ No tiene ahorros».
  La fuente es estatal y de hogar: `EXISTE-NO-SATISFACE`, no cobertura;
- el recibo productivo fue publicado en PR #740, commit `4b3c5264`, e
  integrado por avance rápido en este PR.

Avanzaron los tres elementos de horizonte (`RES-0046`, `RES-0048`,
`RES-0065`) en evidencia y descarte de una pista, no en aptitud: siguen sin
emitir. Los otros 13 elementos conservan su situación previa. El próximo ciclo
recalculará todo el universo; mientras no llegue el 11/oct o aparezca una
fuente/versión nueva, `NC-0126` conserva la espera y el cursor hacia una
secuencia tenencia→duración de persona con cobertura nacional. El correctivo
no ejecutó otra búsqueda ni descarga: su selección real actual quedó vacía con
52 causas publicadas, por lo que fabricar una tarea habría violado el contrato.
Que haya cero elegibles se publica como agenda sin trabajo listo, nunca como
suficiencia general.
