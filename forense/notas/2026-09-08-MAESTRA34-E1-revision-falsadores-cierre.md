# ACTO MAESTRA34-E1 · REVISION-FALSADORES — nota de cierre

Encargo: `forense/encargos/cola/2026-09-08-MAESTRA34-E1-REVISION-FALSADORES.md`
(dirección/Fable, redactado 1/sep/2026 contra v2.12, `SHA de redacción e4af4ed`;
enmienda fechada MAESTRA34-N8, 2/sep/2026, sustituye la compuerta). Acto de
DIRECCIÓN: propone veredictos, mesa firma (contador cero directo, declarado).

## ARRANQUE

1. Repo: clon existente `/home/user/Modelado-Mexicano`, rama
   `claude/maestra34-e1-falsadores-ou8qcp`, `HEAD` = `6330ea3` (PR #462),
   árbol limpio.
2. `git fetch origin main` → `origin/main` = `6330ea3`, mismo commit que
   `HEAD`: sin diferencia que refrescar.
3. `data/raw/`: ausente. No es PARO — este acto no abre microdato (dirección,
   revisión de falsadores del aparato, no toca `data/raw`).
4. Entorno: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (coherente con
   `ENTORNO ASIGNADO: NUBE` del encargo); `curl … inegi.org.mx` → `000` (sin
   red real, esperado en nube); `ls data/raw/` → ausente, coherente con nube
   sin corpus montado. Este acto no abre microdato ni depende de red real; se
   reporta por A.2 completo de todas formas.
5. Espejo: ninguna cifra de esta nota sale del espejo del proyecto; todas del
   clon de (1), comando a la vista en cada renglón.

## COMPUERTA

El cuerpo verbatim del encargo declara `Estado: GATED por FECHA —
NO-LANZAR-ANTES-DE: 2026-09-08`, pero la **enmienda fechada MAESTRA34-N8
(2026-09-02)**, al pie del mismo archivo, la sustituye explícitamente:
*"COMPUERTA (sustituye): digesto del día existente en `forense/digesto/`. La
fecha 2026-09-08 pasa a ser `vence`, no compuerta. Ejecutable desde hoy."*
La cabecera de cola (`BITACORA`) repite la misma compuerta sustituida.

Verificación mecánica, por producto: `ls forense/digesto/ | grep
"$(date -u +%F)"` → `DIGESTO-2026-09-02.md` existe. **CUMPLE.** No hay
segunda compuerta que verificar contra `origin/main` (esta no es una
compuerta de fusión).

## P1 · Universo

Piezas con falsador «a un mes», censadas contra el árbol:

- **5 de la tabla** del pie del digesto (`tools/digesto_tramite.py`
  `FALSADORES`, reflejado en `DIGESTO-2026-09-02.md`): `/acto`, agente de
  trámite, `/tramite`, agente de despacho, `/despacha`.
- **2 fuera de tabla**, declaradas por el propio digesto (`⚠️ 3 piezas
  declaran un falsador «en un mes» y no está en la tabla`, `DIGESTO-2026-09-02.md`
  §Pie) — de las tres que el digesto de hoy nombra
  (`.claude/commands/revisa.md`, `forense/agente-adquisicion-v1_0.md`,
  `forense/agente-revisor-v1_0.md`), el encargo (redactado 1/sep, digesto de
  ese día) solo cita **2**: `.claude/commands/revisa.md` y `forense/agente-revisor-v1_0.md`.
  `forense/agente-adquisicion-v1_0.md` es una tercera pieza que apareció
  **después** de la redacción del encargo (digesto del 1/sep listaba 2 piezas
  fuera de tabla, el de hoy 09-02 lista 3) — fuera del perímetro literal de
  este encargo, se declara como hallazgo pendiente para el próximo ciclo, no
  se juzga aquí (el encargo cita 2, no 3).
- **4 reglas de v2.12** (`instrucciones-proyecto-v2_12.md`, Bloque D-quater):
  D-10 (skill /acto), D-11 (lotes), D-12 (formato corto), D-13
  (escalonamiento de modelos). Comparten un solo texto de falsador conjunto
  (los tres criterios (a)/(b)/(c), unidos por «o»); D-10 es, en sustancia, el
  mismo falsador que la fila `/acto` de la tabla.
- **A.13** (`instrucciones-proyecto-v2_12.md` l.396): origen `2026-08-21`
  (v2.11), ventana de tres meses vence `2026-11-21` — **no vencida**, entra
  al universo.
- **A.10** (l.382): estampa de universo, regla operable desde v2.10; origen
  declarado en `ADR-67` (`10/ago/2026`), ventana de tres meses vence
  `≈2026-11-10` — **no vencida**, entra al universo.
- **A.12** (l.360): tablero derivado, origen `14/ago/2026` (v2.9), ventana
  vence `2026-11-14` — **no vencida**, entra al universo.

**Conteo A.13**: archivos examinados para censar este universo: `12`
(`instrucciones-proyecto-v2_12.md`, `tools/digesto_tramite.py`,
`forense/digesto/DIGESTO-2026-09-01.md`, `forense/digesto/DIGESTO-2026-09-02.md`,
`.claude/commands/acto.md`, `.claude/commands/tramite.md`,
`.claude/commands/despacha.md`, `.claude/commands/revisa.md`,
`forense/agente-tramite-v1_0.md`, `forense/agente-despacho-v1_0.md`,
`forense/agente-revisor-v1_0.md`, `forense/agente-adquisicion-v1_0.md`).

## P2 · Por falsador

### D-10 / fila `/acto` — criterio (a): «no evita ni un acto perdido por compuerta»

Evidencia derivada: `grep -l "cero commits" forense/notas/2026-0[89]*.md | wc -l`
→ **7** notas con "cero commits" desde el 1/ago; de ellas, **4** son actos
posteriores al sellado de v2.12 (`PR #413`, `26cb24c`, 31/ago) que pararon
o repasaron por compuerta **verificada mecánicamente antes de escribir**, no
por compuerta perdida: `2026-09-01-MAESTRA34-L2-ARBITRA-v1_2-cierre.md`,
`2026-09-01-criterios-y-vencimientos-cierre.md`,
`2026-09-01-maestra33-e12-sella-1-cierre.md`,
`2026-09-02-marco-M-v1_2-sello.md`. Este último documenta explícitamente:
*"Al primer lanzamiento de esta sesión la compuerta **no** se cumplía"* — la
skill la atrapó antes de commitear, exactamente lo que D-10 promete. Ningún
acto post-v2.12 se perdió por compuerta declarada-y-no-verificada (el
defecto que motivó D-10, `ADR-224`/`ADR-234`, es anterior a v2.12).

**Veredicto: SOBREVIVE.** El mecanismo de verificación por producto
funcionó en los 4 casos post-sellado observados.

### D-11 — lotes

No hay evidencia, a favor ni en contra, de un lote cuya pieza PARE sin
tumbar a las demás (el único requisito distintivo de D-11 frente al acto
simple). Los dos lotes reales del periodo (`MAESTRA34-L1`, `MAESTRA34-L2`)
no tuvieron ninguna pieza que parara — `MAESTRA34-L2` excluyó una celda por
contaminación (§0 de su cierre), que es una decisión de perímetro, no un
PARO de lote.

**Veredicto: SIN-DATO.** Falta un lote con una pieza que PARE realmente
para medir si D-11 sostiene a las demás; nadie lo ha producido todavía.

### D-12 — formato corto, objetivo medible ≤40% del formato anterior (≥60% de reducción); falsador genérico: «no baja al menos 50%»

Tamaño mediano por serie, `wc -l` sobre cada encargo:

- `MAESTRA34` (formato corto v2.12, 8 encargos con rótulo de pieza
  simple, excluye `N8` que es una enmienda de 18 líneas atípica): `32, 44,
  50, 50, 54, 54, 55` + `N8`=18 → mediana de los 8 valores ordenados
  `[18,32,44,50,50,54,54,55]` = `(50+50)/2` = **50 líneas**.
- `MAESTRA32` (formato largo, previo a v2.12), 20 encargos: mediana de
  `[47,49,51,52,54,54,56,59,63,63,75,79,81,83,83,96,102,106,113,114]` =
  `(63+63)/2` = **63 líneas**.

Reducción real: `(63-50)/63` = **20.6%**. Ni el objetivo explícito de D-12
(`≤40%` del anterior, es decir ≥60% de reducción) ni el umbral genérico del
falsador conjunto (`≥50%`) se cumplen.

**Veredicto: CAE.** La pieza exacta que se revierte: **D-12 · Formato corto
de encargo** (`instrucciones-proyecto-v2_12.md`, Bloque D-quater, párrafo
D-12) y la sección correspondiente de `.claude/commands/acto.md` que hereda
el formato corto. Introducidas en el commit `26cb24c` (`PR #413`, sella
`ADR-237`, `ACTO MAESTRA32-E19 · SELLA-CAMINO-1`). **Propuesta a mesa**, no
ejecutada por este acto (`LO QUE NO HACE`, encargo): revertir D-12 a un
formato con más contenido obligatorio, o relajar el objetivo declarado a lo
que el dato ya sostiene (~20%) en vez de retirarlo — con el caso citado
arriba, mesa decide cuál.

### D-13 — escalonamiento de modelos y agente de fondo

No hay evidencia de una sugerencia de modelo ignorada hacia abajo en un
acto que mida, ni de que el agente de fondo (`tests/check.py --baseline`,
listado de `ABIERTA`, PRs de trámite) haya fallado en su práctica registrada
— `forense/agente-tramite-v1_0.md` sigue produciendo el digesto diario
observado en esta misma nota (§ARRANQUE).

**Veredicto: SOBREVIVE**, con la misma reserva que D-11: evidencia delgada,
no un caso adverso.

### Agente de trámite / `/tramite` — «PR `[TRAMITE]` requiere retrabajo de mesa» · «toca algo fuera de su perímetro de tres rutas»

Sin evidencia de un PR `[TRAMITE]` retrabajado por mesa ni de un PR
`[TRAMITE]` que tocara una ruta fuera de perímetro en las notas examinadas.

**Veredicto: SOBREVIVE.**

### Agente de despacho / `/despacha` — «ejecuta fuera de la cola o fuera de `main`» · «dos sesiones de nube coinciden»

`git log --merges --oneline -20` sobre `origin/main`: **0** merges con
rótulo repetido / colisión de dos sesiones de nube en el mismo encargo
(coincide con "0 desde D4-a" que el encargo ya declaraba). Sin evidencia de
ejecución fuera de la cola.

**Veredicto: SOBREVIVE.**

### `.claude/commands/revisa.md` / agente-revisor — §3, (a) falso negativo a la primera · (b) falso positivo ×3

El encargo mismo delega esta lectura a mesa: *"BLOQUEA del revisor (6 en la
calibración A1; comentarios en PRs #442–#455, mesa los lee en GitHub)"*. Este
acto no reabre esa cuenta (no tiene acceso ni mandato para juzgar cuáles de
los 6 fueron descartados por mesa "con razón" — eso es lectura de mesa, no
de comando). Sin una lista de cuáles `NO-FUSIONAR` mesa descartó y por qué,
no se puede distinguir «bloqueo correcto» de «falso positivo».

**Veredicto: SIN-DATO.** Falta: por cada uno de los 6 `BLOQUEA`
(PRs #442–#455), si mesa fusionó por encima o corrigió antes de fusionar, y
si el punto que bloqueó era real. Lo produce mesa, leyendo los hilos de
GitHub citados (el encargo ya apunta al lugar exacto).

### A.13, A.10, A.12 — ventana de tres meses

Ninguna vencida (arriba, P1). Sin ventana vencida no hay falsador que
evaluar todavía; se declaran vivas y se difiere su revisión a su propia
fecha (`2026-11-10/14/21`), que ya es sucesor declarado del encargo.

**Veredicto: SOBREVIVE** (por no-vencimiento, no por medición positiva).

## P3 · Caso (c) de v2.12 — ¿un lote dejó pasar un defecto de contenido?

Universo examinado: los dos únicos lotes reales del periodo,
`MAESTRA34-L1 · MORDIDA-SERIE` y `MAESTRA34-L2 · ARBITRA-v1_2` (sus notas
de cierre: `forense/notas/2026-09-01-MAESTRA34-L1-MORDIDA-SERIE-cierre.md`,
`forense/notas/2026-09-01-MAESTRA34-L2-ARBITRA-v1_2-cierre.md`), contra sus
ADR de cierre en `canon/gobernanza-v1_15.md`. `MAESTRA33-L1`, que el
encargo nombra como tercer lote a revisar, **no existe** en el repo
(`grep -rn "MAESTRA33-L1\b" canon/registro-rotulos.tsv forense/notas/*.md`
→ vacío): el encargo cita un rótulo que no fue redactado — se declara como
hallazgo del propio encargo, no un lote perdido.

`MAESTRA34-L2` trae, en su propia nota de cierre §0, una declaración de
contaminación auto-detectada (`TRA-M-02` visto antes de que su compuerta
abriera) que el acto resolvió excluyendo la celda del lote — es la prueba
de que el formato de lote **atrapó** el riesgo antes de que llegara a
`main`, no de que lo dejara pasar.

**No aparece ningún caso** de defecto de contenido que un lote dejó pasar y
que el formato largo habría atrapado, sobre el universo de 2 lotes
examinados (más el rótulo inexistente que el encargo citaba de más).

**Veredicto: NO-ENCONTRADO**, con el universo declarado arriba — 2 lotes
reales existentes en el repo, 0 defectos de contenido.

## P4 · Propuesta a mesa (lenguaje de RH)

| pieza | veredicto | qué desbloquea cada opción |
|---|---|---|
| D-10 (mecanismo de compuerta) | SOBREVIVE | mantener: sigue el ARRANQUE mecánico tal cual |
| D-11 (lotes) | SIN-DATO | medir más: esperar un lote con una pieza que PARE de verdad, o declarar la regla sin caso adverso posible por ahora |
| **D-12 (formato corto)** | **CAE** | **revertir**: bajar el objetivo declarado de ≤40% a lo que el dato sostiene (~20%), o volver a exigir más contenido obligatorio en el encargo corto — mesa elige cuál, con el caso citado arriba |
| D-13 (modelos/agente de fondo) | SOBREVIVE (evidencia delgada) | mantener |
| agente/`/tramite` | SOBREVIVE | mantener |
| agente/`/despacha` | SOBREVIVE | mantener |
| `revisa`/agente-revisor | SIN-DATO | medir más: mesa lee PRs #442–#455 y clasifica cada `BLOQUEA` como correcto o falso positivo |
| A.13 / A.10 / A.12 | SOBREVIVE (por no vencer) | mantener hasta su propia fecha |

`FP-226` → **EJECUTADA con veredictos PROPUESTOS** (arriba); mesa firma.
`FP-222` → cerrada, sustituida por `FP-226` (ya declarado así en el
tablero desde su redacción).

Las 2 piezas fuera de tabla (`.claude/commands/revisa.md`, `forense/agente-revisor-v1_0.md`) entran
a la tabla de falsadores del pie del digesto: `tools/digesto_tramite.py`
`FALSADORES` (edición aplicada en el mismo commit que esta nota).
