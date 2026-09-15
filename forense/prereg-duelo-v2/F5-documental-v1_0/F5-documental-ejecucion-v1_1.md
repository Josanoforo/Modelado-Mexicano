# FP-373 · ejecución documental v1.1 — sucesión de v1.0 (transporte corregido)

Este archivo es una **sucesión** de `F5-documental-ejecucion-v1_0.md`. El
v1.0 queda **intacto** — no se edita, no se enmienda, no se borra — y este
v1.1 lo sucede como el contrato vigente para el próximo `--freeze-plan` /
`--transport-probe` / `--run`. Redactado con el archivo v1.0 y la evidencia
cruda del PARO (`ACTO GEN2-F5-DOCUMENTAL-RUN`, PR #756) enfrente:
`forense/notas/2026-09-14-GEN2-F5-DOCUMENTAL-RUN-paro.md`,
`forense/prereg-duelo-v2/F5-documental-v1_0/sonda-transporte-v1_0.json`,
`tools/f5_documental.py` (líneas 385–486 al momento de redactar), y el
`claude -p --help` del cliente `2.1.270` realmente instalado en esta sesión
(el mismo cliente que corrió la sonda del PARO).

Este acto **redacta**, no ejecuta: cero solicitudes al proveedor gastadas
contra el techo por este archivo, y el runner (`tools/f5_documental.py`) no
se toca todavía — lo ajusta el acto sucesor (`GEN2-F5-DOCUMENTAL-RUN`
relanzado apuntando a v1.1).

---

## (a) El auxiliar `claude-haiku-4-5` — no toca la ruta de respuesta; se declara componente auxiliar permitido

**Evidencia cruda** (`sonda-transporte-v1_0.json`, `sobre_cli_original`):

```
modelUsage.claude-haiku-4-5-20251001 = {inputTokens: 91703, outputTokens: 22,
                                          cacheReadInputTokens: 0, cacheCreationInputTokens: 0}
modelUsage.claude-opus-5             = {inputTokens: 4, outputTokens: 867,
                                          cacheReadInputTokens: 117745, cacheCreationInputTokens: 118212}
usage (bloque de nivel superior, el que respalda `result`/`structured_output`) =
       {input_tokens: 4, output_tokens: 867,
        cache_creation_input_tokens: 118212, cache_read_input_tokens: 117745}
```

Las cuatro cifras del bloque `usage` de nivel superior — el que respalda
`result` y `structured_output`, es decir la respuesta que el contrato
evalúa — **coinciden exactamente, campo a campo**, con la entrada
`modelUsage["claude-opus-5"]`, y en **ninguna** coinciden con la entrada de
`claude-haiku-4-5`. La respuesta (`estado=ABSTENCION`,
`derivacion=…weighted_distribution…fue bloqueada…`, el marcador en `nota`)
es texto de 867 tokens de salida — exactamente el `outputTokens` de Opus, y
muy por encima de los 22 de Haiku. **Haiku no generó ni un carácter de la
respuesta evaluada.**

La forma de la llamada de Haiku es la de una tarea auxiliar, no de una
generación de respuesta: 91 703 tokens de entrada, 0 tokens de caché
(ninguna reutilización, consistente con una pasada de una sola vez sobre
contenido grande) y apenas 22 tokens de salida — la proporción entrada/salida
(≈4 168:1) es la firma de una compactación o un resumen interno del
contexto que Opus venía acumulando (118 212 tokens de creación de caché +
117 745 de lectura de caché en la llamada de Opus), no la de responder la
pregunta del prompt. `--prompt-suggestions false` (ya presente en
`comando_mcp`) apaga el mensaje `prompt_suggestion` posterior a cada turno,
pero no apaga esta pasada auxiliar — son mecanismos distintos del cliente;
el contrato v1.0 apostó a que sí y la sonda demostró que no.

**Conclusión: Haiku NO toca la ruta de respuesta.** No hay flag que lo
prohíba porque no hay nada que prohibir — el auxiliar no participa de la
respuesta evaluada; el contrato lo **declara componente auxiliar
permitido**, con la siguiente evidencia de identidad exigida **por
mensaje**, mecánica y no discrecional:

**Regla de identidad del modelo respondedor (nueva; sustituye
`modelos(sobre) == {MODELO}`).** Para cada invocación, la sonda y cada
posición de la corrida verifican:

1. El bloque `usage` de nivel superior reconcilia **exactamente** contra
   `modelUsage[MODELO]` en los cuatro campos: `input_tokens`,
   `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`.
   Si no reconcilia, el modelo primario no está probadamente detrás de la
   respuesta: `TRANSPORTE-NO-VALIDADO`.
2. Cualquier modelo adicional en `modelUsage` que no sea `MODELO`
   (`claude-opus-5`) se admite **sólo** si su `outputTokens` ≤
   `AUX_TOPE_SALIDA = 200` (margen sobre los 22 observados; una pasada de
   compactación/telemetría real no necesita más). Un auxiliar que reporte
   más que eso deja de ser "auxiliar leve" y exige repetir este análisis
   antes de admitirlo — no se ignora ni se admite por omisión.
3. Ambas condiciones se registran en el propio `sonda-transporte-v1_1.json`
   y en cada sobre de posición, no sólo se verifican en memoria: la
   identidad del modelo respondedor queda trazable por mensaje, no por
   confianza en `modelos_reportados`.

Nunca se ignora la presencia del auxiliar (como hacía v1.0 al no verificar
nada sobre él); se admite con evidencia y con tope, tal como pedía el
sucesor declarado en `NC-0177`.

---

## (b) Conjunto mínimo de `--allowedTools` / negaciones MCP que preserva el blindaje

Comando sellado en v1.0 (`tools/f5_documental.py::comando_mcp`, línea 389):

```
claude -p --model claude-opus-5 --output-format json --json-schema {…}
  --system-prompt {…} --tools mcp__f5docs__weighted_distribution --max-turns 2
  --strict-mcp-config --mcp-config {…} --disable-slash-commands
  --no-session-persistence --prompt-suggestions false --permission-prompts none --restricted
```

Causa 1 del `TRANSPORTE-NO-VALIDADO`: `--permission-prompts none` deniega
automáticamente cualquier cosa que pediría aprobación — y sin
`--allowedTools`, el propio `mcp__f5docs__weighted_distribution` cae en esa
denegación por defecto (`permission_denials` de la sonda lo confirma
verbatim). El conjunto mínimo, línea por línea, con lo que cada línea aporta
al blindaje:

| flag | efecto | por qué se conserva / se agrega |
|---|---|---|
| `--allowedTools mcp__f5docs__weighted_distribution` | **NUEVA.** Concede permiso explícito a esa única herramienta. | Es la única línea que faltaba. Sin ella, `--permission-prompts none` deniega la herramienta que el propio contrato exige usar — el hueco exacto que produjo la causa 1. Concede exactamente una herramienta, nada más: el blindaje no se ensancha más allá de lo que el contrato ya necesitaba. |
| `--permission-prompts none` | Deniega automáticamente todo lo que no esté explícitamente permitido; nadie (ni "host") responde por el modelo. | Se conserva sin cambio. Con `--allowedTools` acotado a una sola herramienta, esta línea sigue siendo la que cierra la puerta a cualquier otra cosa que intente pedir aprobación — el blindaje para todo lo demás no se toca. |
| `--strict-mcp-config` | Sólo carga los servidores MCP listados en `--mcp-config`; ignora cualquier configuración MCP de usuario/proyecto/local. | Se conserva. Sin esto, un `.mcp.json` de proyecto o de usuario podría añadir servidores no auditados al alcance del modelo. |
| `--restricted` | Quita Bash/PowerShell/REPL y demás herramientas que ejecutan código, y `WebFetch`, salvo que `--tools` las nombre; confina las herramientas de archivo a los directorios de trabajo; ignora ajustes de usuario/proyecto/local. | Se conserva. Es la línea que impide que el modelo salga del directorio aislado de la celda o toque red, incluso si algo más fallara. |
| `--tools mcp__f5docs__weighted_distribution` | Restringe el catálogo de herramientas **incorporadas** (`--tools` opera sobre el conjunto incorporado, según su propio texto de ayuda: "available tools from the built-in set"). El nombre MCP pasado aquí no es un nombre incorporado, así que el efecto de facto es dejar el catálogo de herramientas incorporadas en cero — no es, como asumía v1.0, el mecanismo que habilita la herramienta MCP (eso lo hace `--allowedTools`, arriba). | Se conserva por su efecto de facto (cero herramientas incorporadas disponibles, lo cual es exactamente lo que se quiere: el modelo no necesita `Read`/`Bash`/nada incorporado porque el documento ya viene completo por `stdin`), pero el contrato deja de atribuirle el papel de "habilitar la MCP" — ese papel es de `--allowedTools`. Corregir esta atribución evita que un futuro lector repita el error de v1.0 (asumir que `--tools` + `--permission-prompts none` bastaban). |
| `--no-session-persistence` | No guarda sesión para reanudar. | Se conserva: ninguna celda debe heredar estado de otra. |
| `--disable-slash-commands` | Quita skills/comandos personalizados de la superficie. | Se conserva: reduce superficie a lo estrictamente necesario. |
| `--prompt-suggestions false` | Apaga el mensaje `prompt_suggestion` posterior a cada turno. | Se conserva por su propio efecto (menos mensajes, menos superficie), pero **se deja de invocar como la causa que elimina al auxiliar Haiku** (ítem (a) arriba demuestra que no lo hace). |

No se agrega `--disallowedTools` explícito: con el catálogo incorporado ya
en cero (vía `--tools`) y `--allowedTools` acotado a una sola herramienta
MCP, no queda ninguna otra herramienta que negar explícitamente — negar algo
que ya no está disponible sería ruido, no blindaje adicional.

---

## (c) Por qué el print mode consumió 3 turnos contra el límite de 2 — la causa, no el conteo

**Verificado en vivo contra el cliente `2.1.270`** (el mismo que corrió la
sonda del PARO), `claude -p --help`:

```
$ claude -p --help | grep -in "turn\|max-turns"
   (sin ninguna línea "--max-turns"; la única mención de "turn" es
    --fallback-model, que re-intenta "at the start of each user turn",
    y --prompt-suggestions, que emite un mensaje "after each turn")
$ echo "..." | claude -p --max-turns 2 --model claude-haiku-4-5 --output-format json
   → returncode 0, JSON de resultado normal, ninguna advertencia de flag
     desconocido, ningún error.
```

**La causa: `--max-turns` no es un flag reconocido por el cliente `2.1.270`
instalado.** No aparece en su `--help`; probado en vivo, el cliente lo
acepta sin error y sin efecto — lo ignora en silencio. El comando sellado
de v1.0 (`comando_mcp`, línea 389) pasa `"--max-turns", str(MAX_TURNS)`
(`"2"`) a un cliente que nunca aplicó ese techo. **`num_turns=3` no es una
violación de un límite real de 2: es simplemente cuántos pasos internos
necesitó el modelo sin ningún techo de turnos en vigor.** No hay "3 porque
salió 3" que enmendar con un número distinto de turnos — el mecanismo de
enmienda correcto es dejar de fingir que ese techo existe.

Consecuencia sobre la contabilidad del ledger, que **sí** es un defecto
propio (no del cliente): `cargo_solicitudes()` (línea 399-405) computa
`turnos = sobre.get("num_turns")` y, si `turnos` no cae en `1 <= turnos <=
MAX_TURNS`, **devuelve `MAX_TURNS` (2)** — es decir, un `num_turns=3` real
(fuera del rango válido) se contabiliza como si hubiesen sido 2, no como 3
ni como el máximo observado. Esto no es conservador: es un **sub-conteo**
sistemático contra el techo de 96 cada vez que el número real de turnos
exceda `MAX_TURNS`, precisamente el caso que ya se observó una vez y que,
sin un `--max-turns` real, puede repetirse sin aviso.

**El límite nuevo, y su razón:**

1. **Se retira `--max-turns` de `comando_mcp`.** Mantenerlo sugeriría al
   lector que existe un techo técnico de turnos; no existe en este cliente.
   Sostener un flag que no hace nada es peor que no ponerlo: finge una
   protección que no está.
2. **El freno técnico real de este cliente es `--max-budget-usd`,** el
   único límite de ejecución que `claude -p --help` (2.1.270) documenta
   hoy. Se fija en `--max-budget-usd 2.00` por invocación: la propia sonda
   del PARO costó `total_cost_usd=1.3545` en una llamada con caché completa
   (118 212 de creación + 117 745 de lectura); `2.00` deja margen sobre ese
   costo observado sin permitir una espiral sin freno.
3. **La contabilidad contra el techo de 96 deja de fingir un tope de
   turnos.** `cargo_solicitudes()` pasa a cargar el `num_turns` **real**
   reportado (sin recortarlo hacia abajo cuando excede el viejo
   `MAX_TURNS`; sólo se sanea hacia arriba a 1 si el dato es inválido o
   ausente). La reserva previa a cada invocación (`reservar_invocacion`,
   hoy fija a `MAX_TURNS`) se sube a una constante nueva de contabilidad,
   `CARGO_RESERVA = 4` (el único dato observado, 3, más un turno de
   margen), desacoplada de cualquier flag de cliente — es un número de
   libro contable, no una instrucción al CLI.

---

## (d) La sonda de transporte, re-especificada

**Qué valida** (sustituye `sonda_transporte()`, línea 458-485, criterio
`ok` de la línea 476-477):

1. El marcador (`sha256(tabla + firma)`) aparece en
   `structured_output.nota` — sin cambio respecto a v1.0.
2. Identidad del modelo respondedor: la regla de (a) — reconciliación
   exacta de `usage` contra `modelUsage[MODELO]`, y cualquier modelo
   adicional con `outputTokens ≤ AUX_TOPE_SALIDA (200)`.
3. `mcp__f5docs__weighted_distribution` **no** aparece en
   `permission_denials` — la prueba directa de que `--allowedTools` cerró
   el hueco de la causa 1 del PARO.
4. `total_cost_usd` de la invocación ≤ `--max-budget-usd` (2.00) — que el
   freno técnico de (c) sostuvo, no sólo que no truene.
5. El cargo contra el techo (`cargo_solicitudes`, ya corregido en (c)) se
   registra con el `num_turns` real, sin recorte hacia abajo.

Si cualquiera de las cinco falla: `TRANSPORTE-NO-VALIDADO`, cero llamadas
experimentales — la misma regla sellada de v1.0, sin cambio.

**Qué evidencia pega:** el mismo formato de v1.0
(`sonda-transporte-v1_1.json`, publicado por `json_publico`), con
`sobre_cli_original` íntegro, más los tres campos nuevos que la regla de
(a)/(c) exige explícitamente en el registro: `reconciliacion_usage_modelo`
(booleano + los cuatro pares comparados), `modelos_auxiliares`
(lista de `{modelo, outputTokens}` con su cotejo contra `AUX_TOPE_SALIDA`),
y `cargo_real_turnos` (el `num_turns` tal cual, sin recorte).

**Cuántas solicitudes cuesta:** 1 invocación real, cargada contra el techo
por `CARGO_RESERVA = 4` reservados antes de invocar y ajustados al cierre
al `num_turns` real reportado (nunca menos de lo realmente usado) — el
mismo mecanismo de reserva-y-cierre de v1.0 (`reservar_invocacion` /
`cerrar_reserva`), con la reserva y el cargo corregidos según (c).

**El embudo que ARRASTRA las 2/96 ya gastadas:** el ledger
(`solicitudes-ledger-v1_0.json`, `consumidas_conservadoras: 2` tras el
cierre de la sonda del PARO) **no se reinicia.** v1.1 continúa escribiendo
sobre el mismo ledger — la sonda de v1.1 es una invocación nueva que se
reserva y se cierra igual que cualquier otra, sumándose al total ya
existente. Si la sonda re-corrida bajo v1.1 reporta de nuevo 3 turnos
reales, el total pasa de **2/96** a **2 + 3 = 5/96** (contra la reserva
`CARGO_RESERVA=4` que se ajusta al cierre al valor real de 3) **antes** de
que se intente la posición 1 de 32. Las 32 posiciones, si corren, se
descuentan del remanente real (96 − 5 = 91 solicitudes lógicas máximas
restantes bajo el mismo techo), no de un techo reiniciado a 96.

---

## (e) Todo lo demás del v1.0 — copiado sin tocar

Lo siguiente es **idéntico a v1.0**, no se toca ni se re-abre en este
contrato:

- **FP-373**, 32 posiciones lógicas (2 brazos contemporáneos ×
  2 celdas [`DIN-M-01`, `TRA-M-07`] × 8 réplicas), máximo 2 reintentos sólo
  técnicos por posición → techo de **96 solicitudes facturables**.
- Criterio de éxito por celda: **≥6/8 puntos válidos y trazables, cero
  sustituciones semánticas y mejora de cobertura ≥4/8** contra su control
  contemporáneo (textual de
  `forense/prereg-duelo-v2/F5-panel-viabilidad-presupuesto-spec-v1_0.md`
  §4.3, ya citado en la nota del PARO). Este contrato **no re-abre la
  escala del criterio**.
- Exclusión de **FP-374 y F6**: este contrato no autoriza el piloto de
  transferencia (FP-374, `ABIERTA`, 0/18 familias retenidas ejecutables) ni
  abre F6 bajo ninguna lectura de sus resultados.
- Las materializaciones DIN (ENNViH-1: cuestionario, codebook, libro 3B,
  `fac_3b`, nota de muestra) y TRA (ENCIG 2021: cuestionario, estructura,
  CSV con `P8_3_1`/`FAC_P18`/`EST_DIS`/`UPM_DIS`), verbatim de v1.0 —
  incluida la nota sobre `NS=8` en el codebook contra el código 7 en el
  `.dta` transportado (ninguno altera el estimando: sólo cuentan `1=Sí` y
  `3=No`), y la nota sobre el ZIP histórico con Deflate64 no soportado.
- La secuencia local (`--prepare`, `--verify`) y el requisito de firma
  archivada fuera de `forense/encargos/cola/` con marcador `FIRMA DE MESA` y
  las cuatro frases literales que el verificador exige — sin cambio; la
  firma ya archivada (`F5-documental-firma-v1_0.md`, sha256
  `aa7135c8ad53053592798141d1ea91f4c37d467cd10f640522578e5298583f60`) sigue
  siendo válida para v1.1: v1.1 no reabre la firma, sólo corrige el
  transporte que la firma ya autorizó.
- El paso `--verify` (`sha256_manifiesto_fuentes`) **queda fuera del
  alcance de este contrato v1.1** — no es una de las piezas (a)-(e) que
  este acto redacta; sigue como reserva de mesa (`NC-0178`, `ABIERTA`), sin
  tocar por este archivo.

---

Este contrato gatea exclusivamente la corrección de transporte descrita en
(a)-(d) y la redacción de v1.1; no reabre `TRIADA-0002` ni la re-adjudica,
no autoriza `FP-374` ni `F6`, y no cambia la escala del criterio (`≥6/8`,
cero sustituciones, mejora de cobertura `≥4/8`) sellada en v1.0.

---

## Enmienda fechada · EJECUCIÓN BAJO v1.1 Y PARO POR TECHO (2026-09-14, `ACTO GEN2-F5-DOCUMENTAL-RUN-2`)

Original intacto arriba; esta enmienda se añade, no edita. El encargo pedía
la enmienda de reanudación en `F5-documental-ejecucion-v1_0.md`; este contrato
manda que v1.0 «no se edita, no se enmienda», así que se asienta aquí, en el
contrato que gobernó la corrida (declarado en el encargo archivado).

- **Runner ajustado a (a)-(d)** (`tools/f5_documental.py`, commit `2897970`):
  `--allowedTools mcp__f5docs__weighted_distribution`; `--max-turns` retirado y
  `--max-budget-usd 2.00` instalado; `identidad_modelo()` reconcilia `usage`
  contra `modelUsage[claude-opus-5]` en los cuatro campos y admite auxiliares
  con `outputTokens ≤ AUX_TOPE_SALIDA=200`; `cargo_solicitudes()` carga el
  `num_turns` real sin recorte (sobre ausente → reserva conservada;
  `num_turns` inválido → 1); `CARGO_RESERVA=4`; sonda de cinco condiciones con
  `reconciliacion_usage_modelo`, `modelos_auxiliares` y `cargo_real_turnos`
  registrados. Plan y sonda escritos como `v1_1`; ledger `v1_0` arrastrado.
- **Cliente:** `2.1.272 (Claude Code)`; `claude -p --help` re-verificado: sin
  `--max-turns`, con `--max-budget-usd` y `--allowedTools`.
- **`--verify`:** falla por el mismo único campo (`sha256_manifiesto_fuentes`);
  `NC-0178` sin cambio (fuera de alcance por (e)).
- **`--freeze-plan`:** `F5-documental-plan-v1_1.json`, 32 posiciones, HEAD
  `2897970`, firma `aa7135c8…`; orden, prompts y materialización idénticos a v1.0.
- **`--transport-probe`:** `2026-09-15T00:59Z`, **`TRANSPORTE-VALIDADO`** 5/5;
  `claude-haiku-4-5` auxiliar con 15 tokens de salida, admitido; 3 turnos
  reales; ledger 2 → **5/96**.
- **`--run`:** 22 de 32 posiciones (12 `PUNTO` trazables 12/12, 10
  `ABSTENCION`, 0 errores de identidad); 1 reintento técnico por
  `error_max_budget_usd` (caché fría); parada por `TECHO-SOLICITUDES` en la
  posición 23 con el ledger en **94/96**. Los 10 restantes: `NO-CORRIDA`
  (`NC-0186`). Veredicto y revisión de trazabilidad en
  `forense/notas/2026-09-14-GEN2-F5-DOCUMENTAL-RUN-2-cierre.md`.
- **Hueco de escala, reportado y no enmendado:** el techo 96 está
  dimensionado a una solicitud por llamada lógica (§4.4 de la spec) y (c) carga
  turnos reales (3–8 por invocación); con esa unidad 96 cubre ~20 posiciones.
  Decisión de mesa (`NC-0186`).
- **Estado tras esta enmienda: FIRMADA; PLAN CONGELADO v1.1; TRANSPORTE
  VALIDADO; 94/96; 22/32 CORRIDAS, 10 NO-CORRIDAS POR TECHO.**
