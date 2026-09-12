# GEN2-38 · descubrimiento, adquisición y suficiencia · cierre CAJA

Fecha de ejecución: 2026-09-11, `America/Mexico_City`. Encargo canónico:
`forense/encargos/2026-09-12-GEN2-DESCUBRIMIENTO-ADQUISICION-Y-SUFICIENCIA-PRODUCCION.md`.

## Identidad y corte consumido

- Repositorio: `Josanoforo/Modelado-Mexicano`.
- Worktree de implementación:
  `/home/pc0/mm-gen2-descubrimiento-adquisicion-suficiencia`.
- Rama: `acto/gen2-descubrimiento-adquisicion-suficiencia`.
- Clon productivo: `/home/pc0/mm-adq`.
- Revisión ejecutada por el ciclo real:
  `8a44e6b5faf690ceeb9c916bcb91fd699e4b3251`; revisión final corregida y
  desplegada después de integrar el recibo y los bytes:
  `2b2c6e742e98c6f6847cb834ea26760101d6782b`.
- `main` consumido: `7fc287e3`, que además de #734/#737/#735/#736 ya contiene
  #738 y la materialización documental F5 de #728.

El staging ajeno de `data/manifiesto-staging.yaml` en `mm-adq` se conservó.
No se cambió F5, FP-373/374/F6 ni configuración global de otro CLI.

## Resultado de ingeniería

El ciclo operativo ya no confunde «cero descargas elegibles» con «cero
investigación pendiente». La selección de adquisición y la selección de
necesidades científicas son independientes; si ambas quedan vacías, el cierre
es mecánico y no invoca un LLM.

La entrega conecta:

`necesidad → investigación web → candidata/evidencia → autorización pública
por alcance → residual → descarga/validación → registro/corpus → suficiencia
por dimensión → consumidor`.

Componentes materiales:

- `tools/adq_investigacion.py` proyecta las necesidades ABIERTAS desde
  `forense/no-corrido.tsv` y cruza usos/RESULT, antecedente GEN1, decisiones,
  necesidad→objeto y utilidad-modelo. Selecciona por prioridad/bloqueo/fecha,
  reserva con vencimiento y persiste cursor, frontera y próxima revisión por
  versión de pregunta. La vista derivada final acredita 52 activas: 6 con
  contrato científico completo, 45 con descripción mínima derivada que sigue
  contando como científicamente incompleta, y NC-0165 como contrato operativo
  no científico. Ninguna desaparece por quedar fuera del selector. Explica los
  207 elementos activos del alcance aprobado —incluidos 191 anteriores a la
  adopción— y distingue datos, preparación, cálculo, validación, adopción y
  decisión sin reactivar sus valores GEN1.
- `tools/adq_suficiencia.py` decide por identidad, concepto, población,
  selección/no respuesta, unidad, temporalidad, diseño e identificación. No
  produce un porcentaje único de suficiencia ni convierte por sí sola una
  aptitud reportada por investigación en autorización de emisión.
- `tools/adq_autorizacion.py` separa JSON e historia, y reconoce el mandato
  `AUTORIZADA-POR-ALCANCE` sólo para el objeto público vinculado. Rechaza
  negación, objeto distinto, fecha inválida y ambigüedad. Un intento efectivo
  sin fecha queda `FECHA_INDETERMINADA`, no habilita reintento automático.
- `tools/adquiere_cron.sh` ejecuta descubrimiento con búsqueda web real aun con
  cero descargas, aísla las sondas por proveedor, conserva presupuestos y
  exige un recibo estructurado. La publicación ocurre desde el clon dedicado;
  el wrapper normaliza sólo las selecciones autoritativas, no redecide el
  hallazgo científico del operador.
- Los escritores comunes de cola/registro/vista usan locks cortos y reemplazo
  atómico; ningún lock de publicación se retiene durante investigación web.
- La acción de Task Scheduler usa un PowerShell no interactivo y oculto que
  espera a `wsl.exe` y propaga su código real; el doctor decodifica la acción
  sin ejecutarla y acredita `sin_ventana=true` y
  `espera_y_propaga_resultado=true`.
- `tools/consulta_gen2.py` consulta la guardia por identidad exacta de
  consumidor. La versión v2 enlaza necesidad, versión de pregunta, consumidor,
  RESULT, uso y evidencia. Descarta estados de otra necesidad o versión y
  mantiene `NO_COVERAGE` aunque el JSON de investigación diga
  `APTA_USO_DECLARADO` ni `APTA_ALCANCE_MENOR`, salvo que exista una decisión
  evidenciada y vínculo exacto del uso aplicable que adopte un
  sucesor calculado o autorice explícitamente el RESULT existente. El estado
  efectivo, el SHA del JSON observado y el vínculo evaluado forman parte del
  hash reproducible del contrato. Las tres emisiones de horizonte vinculadas a
  NC-0126 omiten valor/fallback; trece emisiones no afectadas conservan su ruta
  GEN2.

La configuración efectiva es Codex CLI `gpt-5.6-sol`, búsqueda web habilitada,
máximo 3 investigaciones y 5 objetos por ciclo, presupuestos nominales de
1,800 s de descubrimiento + 1,800 s de adquisición y límite global de 3,900 s
más 60 s de gracia. Son límites de ejecución, no umbrales científicos.

## Demostración productiva atribuible

La activación final fue manual mediante la tarea Windows; no se presenta como
un disparo programado. El canal
`Microsoft-Windows-TaskScheduler/Operational` acredita para la instancia
`{5de63737-6502-4b04-ae17-f6ba669637c8}`:

- evento 110 a `2026-09-11 19:41:29-06:00`, usuario `PC0`;
- eventos 100/129/200 de inicio e invocación de `wsl.exe`;
- eventos 201/102 a `2026-09-11 19:47:06-06:00`;
- retorno Windows `2147942465 = 0x80070041`, cuyo byte bajo es 65.

Ese recorrido es `run_id=2026-09-11T194129-2173366`, runner
`adq-codex-4`, revisión `61a72e48cd4c77bc9602667d0bd6bf537b7277f3`,
Codex CLI 0.154.0 y modelo efectivo `gpt-5.6-sol`. Seleccionó cero de 148
objetos de descarga y, sin detenerse, seleccionó NC-0122 y NC-0126 de 52
necesidades activas al corte de esa corrida. Ejecutó ocho consultas web
explícitas en dos lotes, además de búsquedas sobre 241,591 filas del índice
local. La sonda de transporte de INEGI dio HTTP 200.

El operador persistió ambos estados, escribió
`forense/notas/2026-09-11-GEN2-38-investigacion-continuacion-codex.md`, hizo
commit y push, y abrió el PR #738:

- rama `adq/2026-09-11-gen2-38-investigacion-codex`;
- commit `b7c1864102f811a0319a0537d13dae58a922926d`;
- ref comprobada con `git ls-remote`:
  `b7c1864102f811a0319a0537d13dae58a922926d\trefs/heads/adq/2026-09-11-gen2-38-investigacion-codex`.

El código 65 no fue un fallo de búsqueda ni de publicación. El validador
había construido por error `sha→ref` y luego consultaba por `ref`; por ello
rechazó precisamente la línea remota correcta que imprimió. Se corrigió a
`ref→sha`, se añadió prueba dirigida y se revalidó el mismo recibo inmutable
contra esa ref ya comprobada, sin repetir investigación:

```json
{
  "valido": true,
  "cierre_exitoso": true,
  "resultado_trabajo": "descubrimiento_documentado",
  "publicacion_trabajo": "publicada",
  "errores": []
}
```

Las tres activaciones inmediatamente anteriores quedan separadas y no se
mezclan con el recibo final: `192634-2150980` descubrió backticks ejecutables
en EXTRAE-PROMPT (exit 2); `193048-2156495` descubrió la incompatibilidad
inicial del esquema con Structured Outputs (exit 1); `193258-2162505` hizo la
primera exploración, pero el sandbox no permitía publicar y la selección del
modelo no era autoritativa (exit 65). Cada defecto fue corregido y probado;
no se lanzó otra corrida cara para fabricar un último exit 0.

## Resultado científico y bytes

| necesidad | objeto exacto | examen externo | decisión y suficiencia |
|---|---|---|---|
| NC-0122 | producto/lender fintech y canal de alta del mismo producto en México | COFINFAD enlaza `acquisition_channel` y productos para 48,723 clientes de una fintech colombiana; también se revisaron ENIF/ENAFIN, Dataverse, openICPSR y el índice local | COFINFAD es `EXISTE-NO-SATISFACE`: población Colombia y un prestador. ENIF sigue como alcance descriptivo menor; identidad/concepto/unidad PARCIAL. Pregunta ABIERTA. |
| NC-0126 | tenencia de ahorro separada de duración de cobertura entre quienes sí ahorran | Findex 2025 México `fin17d` mide frecuencia, no duración; EACF, ENSAFI y ENIF no separan el constructo requerido | evidencia existente e INCOMPATIBLE. El consumidor no emite el resultado solicitado. Pregunta ABIERTA. |
| NC-0164 / N34 | producto/costo/fricción y daño individual mexicano, con identificación causal | #734 ya fusionado aporta Banxico persona-ola, SHED BNPL extranjero y CFPB agregado | Banxico habilita sólo descripción/asociación mexicana; SHED/CFPB son mecanismo/contexto extranjero. Producto/CAT exacto y causalidad siguen NO_ACREDITADOS. |
| NC-0136 | texto de reactivos encontrable | #737 ya fusionado aporta 22,367/55,895 identidades del lote prioritario y cobertura en 21/102 grupos antes ciegos | infraestructura útil con alcance parcial; 33,528 identidades y 81 grupos siguen sin cobertura. Un negativo del overlay no prueba ausencia científica. |
| NC-0037 | ledger de tanda con turno, pagos e impago | #735 ya fusionado mide panel/attrition, no ledger | sólo alcance menor; unidad e identificación pedidas siguen no acreditadas. |
| NC-0153 | evento×canal nacional con negativos y diseño | expediente INEGI ya preparado; revisión 2026-10-10 | alcance subnacional menor; la tasa nacional exacta permanece abierta. |

La continuación real de NC-0126 encontró microdatos públicos IIEG Jalisco
2022–2024. Los tres XLSX se descargaron por duplicado, pasaron identidad de
bytes y estructura, entraron al corpus y quedaron registrados en
`data/manifiesto.yaml`. La lectura no los confunde con cobertura: ahorro
institucional del hogar está separado, pero la duración conserva la categoría
colapsada y la población/unidad son Jalisco/hogar. Son evidencia pertinente
`EXISTE-NO-SATISFACE`; NC-0126 y los tres RESULT vinculados siguen bloqueados.

Los bytes concurrentes de N34 sí están en el corpus compartido y son legibles
desde otra sesión mediante `data/raw -> /home/pc0/mm-corpus/raw`; #734 publica
rutas, tamaños y SHA-256 de seis objetos (Banxico, SHED y CFPB). Este acto los
consume, pero no los atribuye falsamente a la corrida #738.

La frontera no examinada y el cursor exacto de NC-0122/NC-0126 viven en sus
archivos `data/curacion-registro/investigacion-estado/`; ambos fijan próxima
revisión `2026-10-11`. Login, compra, contacto, instrumentos privados, tesis no
indexadas y nuevas ediciones no afloradas no se declaran agotados.

## Consumo demostrado

La consulta real del consumidor
`milpa/tramite.yaml:dinero.ahorro.horizonte_corto:horizonte_corto` devuelve
`estado=NO_COVERAGE`, `accion_consumidor=NO_EMITIR_RESULTADO_SOLICITADO` y
causa `NC-0126: ... no puede distinguir horizonte corto de ausencia de
ahorro`. Conserva linaje y estimando observables, pero no devuelve `valor` ni
recurre a GEN1.

## Programación final y siguiente ciclo

Existe una sola tarea `\ModeladoMexicano\AdquiereCron`, estado `Ready`, acción
PowerShell `-NonInteractive -WindowStyle Hidden -EncodedCommand`, principal
`PC0`, `Interactive`, `Limited`, `StartWhenAvailable=true` y
`MultipleInstances=IgnoreNew`. Su comando efectivo espera `wsl.exe`, ejecuta
`/home/pc0/mm-adq/tools/adquiere_launcher.sh` y devuelve `$LASTEXITCODE`. El
crontab WSL no contiene un disparador del runner. La tarea usa los siete días
(`DaysOfWeek=127`) a las 07:30, zona
`Central Standard Time (Mexico)` ↔ `America/Mexico_City`; el doctor acredita
`dias_coinciden=true`, `hora_coincide=true` y `disparador_atribuible=true`.
Próxima ejecución: `2026-09-12 07:30:00-06:00`.
El diagnóstico posterior acredita `LastTaskResult=0`, lock libre y comando
efectivo con `ADQ_DEPLOY_REVISION=2b2c6e742e98c6f6847cb834ea26760101d6782b`.

Limitación explícita: `Interactive` requiere una sesión de Windows `PC0`
iniciada. `StartWhenAvailable` recupera retraso cuando Windows vuelve a poder
evaluar la tarea, pero un equipo apagado no ejecuta. Operar con sesión cerrada
requiere conceder «Log on as a batch job» y reinstalar/verificar `S4U`; no se
afirma que hoy funcione.

Con el estado productivo incorporado, la proyección corregida elige cero
investigaciones listas: NC-0122/0126/0164 esperan 11/oct, NC-0153 conserva la
barrera humana y NC-0136/0037 continúan con sus dueños. Ese cero sólo describe
trabajo listo en ese corte; el JSON sigue publicando las 52 NC y los 207
elementos con situación y siguiente acción. Una necesidad o vía nueva elegible
entra por derivación sin editar una lista fija. Al corte simulado 11/oct,
NC-0164 transita desde `ESPERA_NUEVA_PISTA` y queda primera por prioridad.

## Verificación

Pasaron las baterías dirigidas de descubrimiento, autorización, cierre remoto,
configuración, residuales, cableado, doctor, vigilancia del cron, escritor
concurrente, corpus y consulta GEN2, además de las pruebas consumidas de N34,
reactivos y delta. El cierre final incluye 10 casos de recibo, 20 de contrato,
27 de cableado, 9 de doctor, 10 de vigilancia y 13 de consulta; `bash -n` y
`git diff --check` pasan. La prueba real de red dio HTTP 200 y el lock quedó
libre.

Quedan abiertas, por diseño y no por fallo del servicio, 45 NC con descripción
mínima derivada —no contrato científico completo—, los accesos humanos y una
necesidad sin vía heredados de #726, y las fronteras científicas descritas
arriba. La
candidata pública nueva ya produjo bytes y evidencia; no produjo suficiencia.
