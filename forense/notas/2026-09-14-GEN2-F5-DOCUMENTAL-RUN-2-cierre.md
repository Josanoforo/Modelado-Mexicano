# ACTO GEN2-F5-DOCUMENTAL-RUN-2 · la secundaria corre entera bajo v1.1: 16/16 puntos trazables con fuente nativa, 0/16 con contexto

Fecha: 14 de septiembre de 2026 (CST; 15/sep en UTC — la firma de mesa dice 15/sep).

Entorno: CAJA (Ubuntu/WSL2), `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`,
red 200, corpus montado (413 archivos examinados por `tools/entorno.py`),
`claude 2.1.272 (Claude Code)`. Base: `7de3acb43b2d43b89970af63ed0ff5e66cda7aee`
(merge de PR #761, compuerta cumplida por producto). Encargo archivado:
`forense/encargos/2026-09-14-GEN2-F5-DOCUMENTAL-RUN-2.md`, que ejecuta el
texto de `2026-09-14-GEN2-F5-DOCUMENTAL-RUN.md` contra el contrato
`F5-documental-ejecucion-v1_1.md` (PR #758). Firma: la ya archivada en
`F5-documental-firma-v1_0.md` (sha256 `aa7135c8…`), válida para v1.1 por el
propio contrato; el verificador sellado la aceptó sin cambio.

## Veredicto de la secundaria — documental, acotado al panel y al paquete

La pregunta secundaria del duelo (uso documental, **acotado al panel y al
paquete**: `DIN-M-01` y `TRA-M-07`, brazos `CONTEXTUAL-v2` y
`FUENTE-DIRIGIDA-v1`, 8 réplicas) se mide contra su fila del criterio, textual
de `forense/prereg-duelo-v2/F5-panel-viabilidad-presupuesto-spec-v1_0.md` §4.3:
«Éxito por celda: dirigido con >=6/8 puntos válidos y trazables, cero
sustituciones y mejora de cobertura >=4/8 contra su control contemporáneo.»
Corrieron las **32 posiciones** (22 en la primera pasada, que paró por techo
en 94/96; las 10 restantes tras la firma de mesa que re-dimensionó el techo —
ver §«El hueco en la escala»). Resultado, celda por celda:

- **`TRA-M-07` — ÉXITO.** Dirigido: **8/8 `PUNTO` válidos y trazables**
  (7.18 % las ocho; `fuente_documental` ⊆ paquete; derivación nombra `P8_3_1`
  y `FAC_P18`; el punto reproduce al centésimo la distribución mecánica de
  `analysis.tsv`, Sí/(Sí+No) = 3 671 036 / 51 117 793 = 7.1815 %),
  `sustitucion_semantica=false` en las ocho. Control: **0/8 puntos** (8
  `ABSTENCION`). `≥6/8`: 8 ✓ · cero sustituciones ✓ · mejora de cobertura
  8 − 0 = 8 ≥ 4 ✓.
- **`DIN-M-01` — ÉXITO.** Dirigido: **8/8 `PUNTO` válidos y trazables**
  (15.56 % las ocho; punto mecánico Sí/(Sí+No) = 10 579 946 / 68 002 840 =
  15.5581 %; derivación nombra `cr27` y `fac_3b` y excluye el código 7/8 «NS»
  como fija el contrato), cero sustituciones. Control: **0/8 puntos** (8
  `ABSTENCION`). `≥6/8`: 8 ✓ · cero sustituciones ✓ · mejora 8 − 0 = 8 ≥ 4 ✓.

En una línea: **el acceso a la fuente nativa produjo un punto trazable en
16/16 réplicas dirigidas y el contexto contemporáneo en 0/16; las dos celdas
cumplen el criterio §4.3 con margen máximo.** Lo que esto mide es
recuperación/análisis documental sobre el paquete, no generalización (§4.1
de la spec); no prueba transferencia, no abre `FP-374` ni `F6`. Este párrafo
no toca la primaria (`CALC-TRIADA-0002`, `SIN-GANADOR-UNICO`) ni la
re-adjudica, y no se lee junto con ella — esa lectura es de mesa y dirección.

**Contador: no se mueve.** El contrato no sella CALC; no hay cadena E.2 ni
`cuenta_gen2`. Se dice en una línea, como pide el encargo.

## Embudo, contado en vivo (ledger `solicitudes-ledger-v1_0.json`, arrastrado)

| paso | resultado | solicitudes (ledger / 96) |
|---|---|---|
| arrastre del PARO (PR #756) | sonda v1.0, 1 invocación, 3 turnos, cargo conservador v1.0 | **2** |
| `--verify` | FALLA sólo por `sha256_manifiesto_fuentes` (mismo único campo que en #756; `data/manifiesto.yaml` sigue creciendo por commits ajenos); fuentes, paquetes y ancestros reproducen | 0 (local) |
| `--freeze-plan` (v1.1) | `F5-documental-plan-v1_1.json`: 32 posiciones, cliente `2.1.272`, `claude-opus-5`, HEAD `2897970`; mismo orden, mismos `sha256_prompt` y materialización que v1.0 (sólo cambian las identidades por la versión del cliente) | 0 (local) |
| `--transport-probe` (v1.1) | **`TRANSPORTE-VALIDADO`**, 5/5 condiciones del contrato (marcador en `nota`; `usage` reconcilia exacto con `modelUsage.claude-opus-5` en los cuatro campos; `permission_denials=[]`; `total_cost_usd=1.355 ≤ 2.00`; cargo real 3) — auxiliar `claude-haiku-4-5` presente con 15 tokens de salida, admitido bajo `AUX_TOPE_SALIDA=200` | 2 + 3 = **5** |
| `--run` (1.ª pasada, techo 96) | 22 posiciones resueltas (12 `PUNTO`, 10 `ABSTENCION`, 0 `MALFORMADA`, 0 `ERROR_TECNICO`, 0 `ERROR_IDENTIDAD`); 1 reintento técnico (posición 2, `error_max_budget_usd`: caché fría de 316 601 tokens de creación → `total_cost_usd=3.31 > 2.00`; el segundo intento con caché tibia costó 1.81 y resolvió); parada por `TECHO-SOLICITUDES` al intentar la posición 23 | 5 + 89 = **94** |
| firma de mesa en sesión | «termina el encargo entonces, ese techo es un estimado» → techo re-dimensionado a **288 turnos** (32 × 3 intentos × 3 turnos mínimos), ledger arrastrado; plan v1.2 (identidades idénticas a v1.1) | 0 (local) |
| `--run` (2.ª pasada, techo 288) | 22 reanudadas por identidad (no se repiten), **10 nuevas resueltas** (5 `PUNTO`, 5 `ABSTENCION`, 0 errores, 0 reintentos) | 94 + 36 = **130** |

Total contra el techo: **130 / 288** (94 de los cuales contra el 96 original). Invocaciones reales en este acto: 34 (1 sonda
+ 33 intentos de posición). Turnos reales cargados por posición: 3 en las 16
dirigidas; 3–8 en las 16 contextuales (el brazo control intenta la herramienta
sobre rutas inexistentes en su raíz aislada, que sólo contiene
`contextual.txt` — exactamente lo que el contrato v1.0 fija: «el mismo
conjunto de capacidades se ofrece a ambos brazos»). Coste de lista acumulado
(`modelUsage.costUSD`, base de lista, no cargo observado): 11.00 USD.
Ventana: `2026-09-15T00:59Z`–`01:07Z` (1.ª pasada) y `01:26Z`–`01:31Z` (2.ª).

## Revisión de trazabilidad de las 16 derivaciones `PUNTO`

`revision-traza-v1_1.json` (en el directorio del contrato) la registra por
posición. Criterio mecánico, aplicado sin excepción: (1) `fuente_documental`
⊆ archivos del paquete de ese brazo; (2) `sustitucion_semantica=false`;
(3) la derivación nombra la variable y el ponderador de la tarjeta; (4) el
punto reproduce, con tolerancia 0.01 pp, la distribución ponderada mecánica
de `analysis.tsv` por `weighted_distribution` (`DIN-M-01`: `cr27`×`fac_3b`,
válidos {1,3}; `TRA-M-07`: `P8_3_1`×`FAC_P18`, válidos {1,2}). **16/16
cumplen los cuatro.** Las 16 `ABSTENCION` del control declaran que el
paquete contextual no contiene ENNViH-1 2002/`cr27` ni ENCIG 2021/`P8_3_1` y
no emiten cifra «para evitar una sustitución» — abstención correcta según el
prompt sellado, no fallo.

| # | celda | brazo | rép | estado | punto | sust. | intentos | turnos | coste lista |
|---|---|---|---|---|---|---|---|---|---|
| 1 | TRA-M-07 | FUENTE-DIRIGIDA-v1 | 3 | PUNTO · trazable | 7.18 | false | 1 | 3 | 1.35 |
| 2 | DIN-M-01 | FUENTE-DIRIGIDA-v1 | 4 | PUNTO · trazable | 15.56 | false | 2 | 3 | 1.81 |
| 3 | TRA-M-07 | CONTEXTUAL-v2 | 4 | ABSTENCION | null | false | 1 | 4 | 0.32 |
| 4 | DIN-M-01 | FUENTE-DIRIGIDA-v1 | 5 | PUNTO · trazable | 15.56 | false | 1 | 3 | 0.32 |
| 5 | TRA-M-07 | FUENTE-DIRIGIDA-v1 | 8 | PUNTO · trazable | 7.18 | false | 1 | 3 | 0.24 |
| 6 | TRA-M-07 | FUENTE-DIRIGIDA-v1 | 7 | PUNTO · trazable | 7.18 | false | 1 | 3 | 0.24 |
| 7 | DIN-M-01 | CONTEXTUAL-v2 | 4 | ABSTENCION | null | false | 1 | 8 | 0.65 |
| 8 | TRA-M-07 | FUENTE-DIRIGIDA-v1 | 2 | PUNTO · trazable | 7.18 | false | 1 | 3 | 0.24 |
| 9 | DIN-M-01 | CONTEXTUAL-v2 | 8 | ABSTENCION | null | false | 1 | 6 | 0.17 |
| 10 | TRA-M-07 | CONTEXTUAL-v2 | 7 | ABSTENCION | null | false | 1 | 3 | 0.07 |
| 11 | TRA-M-07 | CONTEXTUAL-v2 | 2 | ABSTENCION | null | false | 1 | 4 | 0.09 |
| 12 | DIN-M-01 | FUENTE-DIRIGIDA-v1 | 2 | PUNTO · trazable | 15.56 | false | 1 | 3 | 0.32 |
| 13 | DIN-M-01 | CONTEXTUAL-v2 | 2 | ABSTENCION | null | false | 1 | 4 | 0.13 |
| 14 | TRA-M-07 | FUENTE-DIRIGIDA-v1 | 6 | PUNTO · trazable | 7.18 | false | 1 | 3 | 0.24 |
| 15 | DIN-M-01 | CONTEXTUAL-v2 | 7 | ABSTENCION | null | false | 1 | 4 | 0.14 |
| 16 | TRA-M-07 | FUENTE-DIRIGIDA-v1 | 4 | PUNTO · trazable | 7.18 | false | 1 | 3 | 0.24 |
| 17 | TRA-M-07 | FUENTE-DIRIGIDA-v1 | 1 | PUNTO · trazable | 7.18 | false | 1 | 3 | 0.24 |
| 18 | TRA-M-07 | CONTEXTUAL-v2 | 5 | ABSTENCION | null | false | 1 | 5 | 0.10 |
| 19 | TRA-M-07 | CONTEXTUAL-v2 | 3 | ABSTENCION | null | false | 1 | 4 | 0.08 |
| 20 | DIN-M-01 | CONTEXTUAL-v2 | 5 | ABSTENCION | null | false | 1 | 7 | 0.18 |
| 21 | DIN-M-01 | FUENTE-DIRIGIDA-v1 | 1 | PUNTO · trazable | 15.56 | false | 1 | 3 | 0.32 |
| 22 | DIN-M-01 | FUENTE-DIRIGIDA-v1 | 8 | PUNTO · trazable | 15.56 | false | 1 | 3 | 0.31 |
| 23 | DIN-M-01 | FUENTE-DIRIGIDA-v1 | 3 | PUNTO · trazable | 15.56 | false | 1 | 3 | 0.31 |
| 24 | DIN-M-01 | FUENTE-DIRIGIDA-v1 | 6 | PUNTO · trazable | 15.56 | false | 1 | 3 | 0.32 |
| 25 | TRA-M-07 | CONTEXTUAL-v2 | 1 | ABSTENCION | null | false | 1 | 3 | 0.08 |
| 26 | DIN-M-01 | CONTEXTUAL-v2 | 6 | ABSTENCION | null | false | 1 | 4 | 0.13 |
| 27 | TRA-M-07 | CONTEXTUAL-v2 | 6 | ABSTENCION | null | false | 1 | 4 | 0.08 |
| 28 | DIN-M-01 | CONTEXTUAL-v2 | 3 | ABSTENCION | null | false | 1 | 3 | 0.13 |
| 29 | TRA-M-07 | FUENTE-DIRIGIDA-v1 | 5 | PUNTO · trazable | 7.18 | false | 1 | 3 | 0.24 |
| 30 | DIN-M-01 | FUENTE-DIRIGIDA-v1 | 7 | PUNTO · trazable | 15.56 | false | 1 | 3 | 0.31 |
| 31 | DIN-M-01 | CONTEXTUAL-v2 | 1 | ABSTENCION | null | false | 1 | 6 | 0.18 |
| 32 | TRA-M-07 | CONTEXTUAL-v2 | 8 | ABSTENCION | null | false | 1 | 4 | 0.09 |

(Orden = orden congelado del plan, semilla 20260911. Posiciones 1–22: 1.ª pasada; 23–32: 2.ª pasada tras la firma de mesa.)

## El hueco en la escala del contrato — se reportó, y mesa lo resolvió en sesión

El techo de 96 nació en §4.4 de la spec como 32 llamadas lógicas × (1 + 2
reintentos) **solicitudes facturables**, a razón de una por llamada. El
contrato v1.1 (c) decidió, con razón contable, cargar el `num_turns` real de
cada invocación sin recorte; y este cliente reporta 3 turnos por invocación
mínima (usuario → `tool_use` → `tool_result` → respuesta) y hasta 8 cuando el
modelo tantea la herramienta. Con ese cargo, 96 alcanza para ~20 posiciones,
no para 32: el techo no fue re-dimensionado cuando cambió la unidad de
cuenta. El encargo lo dice: «si encuentras un hueco en su escala o sus pasos,
PARA y repórtalo: es entregable, no licencia para improvisar». Se paró donde
el runner paró (94/96, 22/32) y se reportó a mesa con las dos salidas
(contrato con techo en turnos, o veredicto con lo observado). **Mesa firmó en
sesión, verbatim: «termina el encargo entonces, ese techo es un estimado».**
Efecto: el mismo diseño de §4.4 se re-dimensiona en la unidad que v1.1
cuenta —32 llamadas × 3 intentos × 3 turnos mínimos = **288 turnos**—, el
ledger se arrastra (94 ya gastados), el plan se re-congela como v1.2 con
identidades idénticas a v1.1 (sólo cambia el hash del runner por la
constante), y el runner reanuda las 22 capturas por identidad y corre sólo
las 10 faltantes. Terminó en 130/288 sin un solo reintento. La firma queda
archivada en el encargo (`## Firma de mesa en sesión`) y en el ledger
(`techo_historia`). `NC-0186` se abre y se cierra en este mismo acto, para
que el hueco quede registrado con su resolución.

Otras dos observaciones del transporte, ambas dentro del contrato:

- `--max-budget-usd 2.00` frenó una vez (posición 2, caché fría del prompt
  dirigido de `DIN-M-01`, 323 655 bytes): es el freno técnico que (c)
  instaló, funcionó, y el reintento técnico permitido resolvió con caché
  tibia. Costó 4 cargos de reserva (sobre ausente → reserva conservada) más
  los 3 del intento bueno.
- El cliente instalado es `2.1.272`, no el `2.1.270` con el que v1.1 verificó
  que `--max-turns` no existe. Se re-verificó en vivo antes de congelar:
  `claude -p --help` de `2.1.272` tampoco lista `--max-turns` y sí lista
  `--max-budget-usd` y `--allowedTools`. El plan v1.1 registra `2.1.272`.

## Tokens de tablero (P3 c)

- `FP-373`: sigue `FIRMADA`; `ejecutada_en` pasa de `NO-EJECUTADA` a
  `EJECUTADA` con este acto (32/32, 130/288).
- `NC-0160` → `CERRADA`: su pregunta a mesa (tabla P1 de TANDA-2: «¿Autoriza
  mesa el texto de firma del encargo 31…?») quedó contestada por la firma
  archivada y ejecutada; el desenlace real son las 32 posiciones corridas
  y las dos celdas en ÉXITO.
- `NC-0177` → `CERRADA`: el transporte que denunciaba valida bajo v1.1 (5/5) y
  las 32 posiciones corrieron.
- `NC-0178` sin tocar: `--verify` volvió a fallar por el mismo único campo;
  fuera de perímetro por letra del contrato v1.1 (e).
- `NC-0186` (nueva, abierta y `CERRADA` en este acto): las 10 posiciones que
  el techo de 96 dejó sin correr; hueco de escala del contrato resuelto por la
  firma de mesa en sesión (techo re-dimensionado a 288 turnos).

## Lo que este acto no hace

No toca la primaria ni su veredicto; no abre `FP-374` ni `F6`; no negoció el
techo desde el ejecutor (paró en 94/96 y lo re-dimensionó sólo con la firma
de mesa, archivada verbatim); no enmienda la escala del criterio; no escribe
la lectura estratégica conjunta.
