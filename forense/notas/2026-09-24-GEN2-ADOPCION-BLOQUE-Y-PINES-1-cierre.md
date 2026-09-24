# Nota de cierre · ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-1 · 24/sep/2026

Ejecuta las firmas L–P de `GEN2-TRAMITE-FIRMAS-14-ADENDA-3` tal como las trae
el encargo `forense/encargos/2026-09-24-GEN2-ADOPCION-BLOQUE-Y-PINES-1.md`
(SHA de redacción `b2690dcc`), con la corrección de `ADENDA-1` (P-L reducida,
"Hecho" redefinido mientras el canal de derivados está caído por GH001,
NC `…CONTADORES-CONSUMO-2-749c-03`).

**Desviación de logística declarada en el 0-bis** (D-19/§4.2, no PARO): esta
sesión de Claude Code Remote tiene asignada la rama `claude/new-session-q4k5jc`
con instrucción de no empujar a otra rama sin permiso explícito; se ejecuta
ahí en vez de `acto/gen2-adopcion-bloque-y-pines-1`. `tools/cierre_acto.py`
lo confirma: el rótulo derivado de la rama (`NEW-SESSION-Q4K5JC`) no trae
`GEN2`, así que el ADR de este acto se acuña con el rótulo real del encargo
(`GEN2-ADOPCION-BLOQUE-Y-PINES-1`), como el propio tool indica hacer cuando
ambos difieren.

## `status` antes → después (comando: `python3 tools/corrida0.py status`)

| Contador | Antes (`b2690dcc`) | Después | Δ | Pieza |
|---|---|---|---|---|
| `N_corridas_selladas` | 234 | 244 | +10 | P-M |
| `N_resultados_gen2_sellados` | 65599 | 65890 | +291 | P-M |
| `N_resultados_gen2_pendientes_adopcion` | 10 | 10 | 0 | ninguna lo mueve — ver §"Hallazgo de premisa 1" |
| `N_resultados_gen2_adoptados_activos` | 72 | 73 | +1 | P-N (pin M08, no P-M) |
| `dependencias_numericas_legacy_activas` | 146 | 145 | −1 | P-N |
| `legacy_activas_por_consumidor__catalogo_de_momentos` | 23 | 22 | −1 | P-N |
| `legacy_activas_por_consumidor__motor` | 34 | 34 | 0 | ninguna lo mueve — ver §"Hallazgo de premisa 1" |
| `relevadas_por_pin_de_mesa__i_CRUDO` | 14 | 15 | +1 | P-N |
| `celdas_validadas` | 219 | 219 | 0 | (P-P sólo etiqueta la definición, no la cambia) |
| `celdas_validadas_definicion_desde` | (no existía) | `38dd709` | nuevo | P-P |

## P-L · Marcador y procedencia — reducida por ADENDA-1, sin cambios propios

`PR #1101` (ya fusionado en `origin/main` antes de este acto — confirmado por
`git merge-base --is-ancestor fd7b804 HEAD` y por el propio `git log`) ya
trae: `marcador_segmento.py --escribe` en dos pasadas en el paso de
derivados de `verify.yml`, las 5 aserciones de `test_c2_compuesto.py`
actualizadas al marcador en punto fijo, y las 16 filas `origen_numerico=NUEVO`
de `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` en `decisiones.tsv`
(`CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` verificado sin uso activo, no
requiere fila). Verificado en esta sesión, sin editar nada:

- `python3 tools/corrida0.py registro --verifica --lote CALC-GOB-DIGITAL-EXE-EMISIONES-0002,CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001,CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` → 0 `NO_APTA` en todo el log (103300 líneas examinadas).
- Con el marcador re-derivado **en el árbol, sin commitear** (`python3 tools/marcador_segmento.py --escribe`, revertido después con `git checkout --`, tal como hizo #1101): `status` sube `adoptados_activos` 72 → 103 y `celdas_validadas_retrospectiva` 59 → 75; `python3 tests/check.py --baseline --parallel` da **19 FAIL** (3 heredados + **16 nuevos, todos T35 T-REPRO(g)**), exactamente:
  ```
  (g) marcador:CRUCE::GOB.gobierno_digital.encig2025.edad_x_sexo::{18-29,30-44,45-59,60-96}x{1,2}
      -> RESULT-ENCIG-DUELO-2025-ADJ-EDADXSEXO-*-C2-P: el origen numérico no está acreditado
  (g) marcador:CRUCE::GOB.gobierno_digital.encig2025.escolaridad_x_sexo::{HASTA-PRIMARIA,SECUNDARIA,MEDIA-SUPERIOR,SUPERIOR}x{1,2}
      -> RESULT-ENCIG-DUELO-2025-ADJ-ESCOLARIDADXSEXO-*-C2-P: el origen numérico no está acreditado
  ```
- **Clasificación (firma L, tercer punto):** estos 16 FAIL **no** describen el marcador viejo — describen, con exactitud, el estado actual real de `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` (0 filas `origen_numerico` en `decisiones.tsv`, verificado por `grep -c`). **Protegen una medición** (si acreditar ese tercer CALC, unidad y todo): quedan sin tocar, gateadas por `FP-260923-GEN2-CONTADORES-CONSUMO-2-749c-01` (releída ahora, sigue `ABIERTA`, A.17). Firma L nombra sólo `CALC-GOB-DIGITAL-EXE-EMISIONES-0002`/`-ADJUDICACION-0001`; extender a `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` sin que una firma de mesa lo nombre habría sido PARO (c) del encargo — no se hace.
- Los cambios del marcador **no se commitean** (canal caído, `NC-…-749c-03`; `derivados_protegidos.py` los rechazaría en un PR sin prefijo `[deriva]`, lección de `NC-…-749c-02`).

**Nada que commitear en esta pieza.**

## P-M · Bloque ENIGH — 10 corridas adoptadas por `cuenta_gen2=SI`

10 filas `cuenta_gen2=SI` en `decisiones.tsv` (una por CALC): la corrida de
duelo por origen móvil de ENIGH más las 3×3 de intensidad de remesas / perfil
estructural / remesas en contexto de las olas 2016, 2018 y 2020. Las 10
verificadas por comando: `resultado_replay=REPRODUCE` /
`contexto_replay=IDENTICO` en `corridas.tsv`; `_inputs_legacy_de(spec)` vacío
en las 10 specs (nada legacy que mesa esté pisando).

**Hallazgo de premisa 1 (§0/A.17):** el "Hecho" del encargo esperaba que
adoptar estas 10 corridas bajara `pendientes_adopcion` a ≤4 y subiera
`adoptados_activos`. Verificado por comando (`_resultados_citados_en`
sobre `milpa/tramite-ola5-propuesta-v0.yaml`, antes y después): los 10
`RESULT` `pendientes_adopcion` de hoy (`RESULT-BANXICO-2024-*` ×5,
`RESULT-CTX-2019/2023-P-ALTO`, `RESULT-MOTRAL15-*` ×3) son un conjunto
**disjunto** de las 10 corridas ENIGH — es el objeto de
`NC-260922-GEN2-TRAMITE-FIRMAS-7-369b-01`, que ya declaró
`FUERA-DE-PERIMETRO`: el único mecanismo de adopción para ese conjunto exige
editar `milpa/` (wiring de consumidor), ajeno a este acto (§9) igual que lo
fue para `GEN2-TRAMITE-FIRMAS-7`. `cuenta_gen2` (si una corrida "cuenta"
como GEN2 en el linaje E.1) y `adoptados_activos`/`pendientes_adopcion` (si
un consumidor activo ya la lee, E.2) son **dos ejes distintos**; el encargo
los trató como uno. Ver NC nueva abajo.

**Hallazgo de premisa 2:** de las 14 corridas PENDIENTE-DE-MESA que el
tablero citó, sólo 10 tienen replay `REPRODUCE`; las **5** restantes (no 4)
son `NO-VERIFICADO`: `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001` **y**
`-0002` (firma M nombra sólo "EDER-0002"), `CALC-ENFIH2019-COBERTURA-SALDOS-
CATPOS-0001`/`-0002`, `CALC-WBES2023-PRECISION-INTERACCIONES-0001` — 9+1+5=15,
no 14. Las 5 quedan `PENDIENTE-DE-MESA` sin fila nueva (ninguna firma las
autoriza); ver NC.

## P-N · Relevo: momento 08 acotado, momentos 01/02 dictaminados, escritor no extendido con código

- **Momento 08** (`civico.denuncia.con_seguro`): pin nuevo en
  `pines-de-mesa.tsv`, `catalogo-momentos::M08` → `RESULT-ENVIPE-SEG-CON-P-
  DENUNCIA` (`CALC-ENVIPE-DENUNCIA-SEGURO-0001`, vía `i-CRUDO`). Validado
  **contra el código real**, no a mano:
  `pines_mesa.valida_pin(fila, ctx, specs, {})` → `('ACEPTADO', '')`. Efecto
  medido: `legacy_activas_por_consumidor__catalogo_de_momentos` 23→22,
  `relevadas_por_pin_de_mesa__i_CRUDO` 14→15, y — hallazgo no anticipado,
  verificado tras escribir el pin — el `uso` de `catalogo-momentos::M08`
  pasa a `aptitud_uso=APTA-POR-LINAJE` y entra a `adoptados_activos` (72→73):
  el motivo de aptitud trae el mismo matiz que la nota del pin
  ("no certifica compatibilidad semántica del estimando con el parámetro").
  Acotado a unidad **DELITO** (BPCOD=01, robo total de vehículo) según
  `cotejo-documental-catalogo.md` momento 08, no al registro PERSONA/ENIGH
  2022 que `milpa/catalogo-momentos-v0_1.tsv` declara. **NO-REPRODUCE-GEN1**
  rotulado en la nota del pin: no reproduce la regla **ASIGNADA** de
  `milpa/procedencia.yaml:859-862` (`valores=[0.78,0.22]`, "ENVIPE no
  publica esta condicional en esa forma") — el valor medido aquí
  (0.790906/0.209094) es de otra unidad y otra clase de evidencia (medido,
  no asignado), aunque numéricamente cercano.
- **Momentos 01/02** (`tramite.mordida.discrecional` / `con_registro`):
  dictamen `NO-CONSTRUIBLE` en `decisiones.tsv`, rama (ii) que el propio
  encargo previó — el cotejo documental (`cotejo-documental-catalogo.md`
  momentos 01/02) no cita pregunta/registro que satisfaga el estimando:
  ENCIG P8_3 registra SOLICITUD de trámite, no pago con o sin
  discrecionalidad. Verdicto `NO-EQUIVALENTE-PAGO`; no se fuerza candidato.
- **Escritor de consumo — NO extendido con código nuevo**, y se documenta
  por qué en vez de forzarlo: `milpa/src/momentos.py:119-134`,
  `valor_de()`, lanza `NotImplementedError` para **todo** momento `AJUSTE`
  en E0, por diseño deliberado ("E0 no mira el disco, §3.3 de la
  propuesta"). Ninguna cita lateral que este acto pudiera escribir cambia lo
  que el motor consume hoy — D-14 (gate para automatizar) falla: no hay
  medición ni decisión que ese código mueva todavía. El pin de M08 sí mueve
  la trazabilidad de gobierno (arriba) sin escribir código nuevo, con el
  canal ya construido (`tools/pines_mesa.py`).

## P-O · El pin de vía (iii) no estaba huérfano

Firma O asumía que la llave del pin `iii-DERIVADO-DE-GEN2`
(`tramite::civico.denuncia.miedo_desconfianza::denuncia_por_otra_razon`)
ya no existía en el motor. Verificado por comando
(`corrida0._filas_registro().avisos`): el aviso real es
`PIN-SOBRE-CONSUMIDOR-YA-MARCADO`, no `PIN-SIN-CONSUMIDOR`. La llave sigue
vigente; el consumidor (`milpa/tramite.yaml`) ya trae
`corrida0_generacion: GEN2` escrito directamente por
`tools/escribe_relevo_consumo.py` (PR #1080, RES-0028), fusionado antes de
que este pin se evaluara — "manda el consumidor, no el pin" (comentario del
propio código, `corrida0.py:4462`). No hay renombre que buscar con
`git log -S`: nota aclaratoria añadida a la fila existente (perímetro §9:
"sólo nota/re-apunte del huérfano"); ninguna firma nueva. Las otras 29 filas
pasan las cuatro guardas (`pines_rechazados` vacío, verificado por comando)
y ya se aplican por la lógica de aplicación en vivo de `corrida0.py`.

## P-P · Marca de definición de `celdas_validadas`

`tools/celdas_validadas.py::DEFINICION_DESDE = "38dd709"`, declarado primero
en `forense/prereg-caja/METRICA-CELDAS-VALIDADAS-spec-v1_0.md` §9 (D-15).
`corrida0 status`, `--json` y `--linea` lo imprimen al lado del total, nunca
fundido. **Corrección de premisa:** el encargo citó "commit de #1078"; ese
PR (`GEN2-TRAMITE-FIRMAS-12`, rescate de su ADENDA-1) no toca
`celdas_validadas.py` — verificado con `git log --oneline -- tools/
celdas_validadas.py`. El commit real que trajo la definición vigente
(crédito por conducta + sufijo `-D-C2`, el salto 92→219) es `38dd709`,
fusionado por **PR #1086**. La misma confusión #1078/#1086 ya la había
corregido `GEN2-TRAMITE-FIRMAS-14` el 23/sep para otra fila (657c-03) —
`canon/registro-rotulos.tsv` lo registra: es una cita recurrente de
dirección, no un hallazgo nuevo de esta sesión. 4 tests nuevos; suite de
`celdas_validadas` completa (22 tests) VERDE.

## Verificación de esta sesión

- `python3 tests/check.py --rapido` → VERDE, 0 FAIL (corrido después de cada pieza).
- `python3 -m unittest tests.test_celdas_validadas_spec tests.test_celdas_validadas tests.test_celdas_validadas_monotonia` → 22 tests, OK.
- `python3 tools/pines_mesa.py` (vía script ad-hoc contra el `valida_pin` real): pin de M08 → `ACEPTADO`; `pines_rechazados` de las 30 filas previas → vacío.
- `python3 tools/corrida0.py registro --verifica --lote …` → 0 `NO_APTA` para los dos CALC de firma L en el árbol committeado.

## Lo que decide mesa a continuación

- `FP-260923-GEN2-CONTADORES-CONSUMO-2-749c-01`: sigue `ABIERTA` — declarar
  `origen_numerico` de `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` (16 RESULT)
  es de mesa, no de este acto (firma L no lo nombra).
- El bloque `RESULT-BANXICO-2024-*`/`CTX-*`/`MOTRAL15-*` (10 RESULT
  `pendientes_adopcion`) sigue esperando un acto con `milpa/` en perímetro
  (`NC-…-369b-01`).
- El canal de derivados sigue caído por GH001 (`NC-…-749c-03`) — lo repara
  `GEN2-TUBERIA-VISTA-NORMALIZADA-1` (encargo ya recibido, no ejecutado en
  esta sesión: es un acto propio, con su propia rama y perímetro).
