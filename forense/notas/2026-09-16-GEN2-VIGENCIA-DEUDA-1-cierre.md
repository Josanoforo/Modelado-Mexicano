# NOTA DE CIERRE · ACTO GEN2-VIGENCIA-DEUDA-1 (16/sep/2026)

Encargo archivado verbatim: `forense/encargos/2026-09-16-GEN2-VIGENCIA-DEUDA-1.md`.
Compuerta: fusión de PR #795 (GEN2-MANTENIMIENTO-Y-ARCHIVO-2), PR #798
(GEN2-PANEL-F6-EXPANSION-1) y PR #797 (GEN2-MARCADOR-C0-D, el "MARCADOR" que
cita el encargo) — las tres verificadas `merged: true` vía
`mcp__github__pull_request_read` antes de arrancar. CUMPLIDA.

## 0 · Corrección de vocabulario, antes de leer el resto

El encargo cita cinco rótulos para P1 (RESUELTA-POR-PRODUCTO, PREMISA-VENCIDA,
CADUCA-POR-DISEÑO, DUPLICADA, VIGENTE) y cuatro para P2 (LANZADO-COMO,
SUPERADO-POR, VIGENTE, CADUCO) que **no existen como tokens del árbol**.
Verificado por búsqueda recursiva, universo declarado (A.4): ninguno aparece
en `tools/estado_comun.py::CIERRES_ADMITIDOS` (NC) ni en el vocabulario real
de `ESTADO:` de `.claude/commands/despacha.md` (cola). Se usan aquí
exclusivamente como **etiquetas de esta auditoría** — el mapeo a los tokens
reales se declara en cada sección. Dos citas del propio encargo también están
cruzadas: "tu F-11" es en realidad el **OBJETO 11** de la HOJA DE FIRMAS DE
MESA 1 (15/sep/2026), que autorizó `CERRADA-POR-DISEÑO` en
`tools/estado_comun.py` sobre NC-0073; y "A.6" — citada como "solo se reabre
lo que hoy gatea algo" — es en realidad el **corolario retroactivo** de A.6
(`instrucciones-proyecto-v2_13.md:282-292`), no su enunciado. No cambia el
alcance del acto, pero mesa debe saber que estas citas se corrigieron para
poder confiar en el resto.

## 1 · Metodología

`Workflow` con dos fases independientes (P1: 62 filas ABIERTA de
`forense/no-corrido.tsv`; P2: 65 archivos de `forense/encargos/cola/`), cada
una en pipeline **investiga → verifica adversarial**: un agente investiga
cada fila/archivo con comando y salida reales contra el árbol; si propone un
cambio, un segundo agente independiente intenta REFUTARLO corriendo los
mismos comandos por su cuenta (default a refutar ante la duda). 90 + 118 = 208
llamadas de agente, todas en Sonnet 5 (heredado de la sesión, sin override).

**La capa adversarial encontró y detuvo defectos reales**, no solo
formalismo: 6 de 62 hallazgos de P1 y 18 de 52 `LANZADO-COMO` de P2 fueron
refutados. La causa dominante en P2 — presente en al menos 9 refutaciones
independientes — es un patrón sistémico de alucinación: múltiples agentes,
sin coordinación entre sí, citaron el mismo commit falso (`3aef05d`, en
realidad el merge ajeno de PR #735 sobre paneles de tandas) como si fuera el
que sincronizó su archivo. Ninguna de esas 9 conclusiones de fondo resultó
falsa por eso — pero ninguna hubiera sobrevivido publicarse sin el segundo
agente. Se registra como hallazgo de método, no solo de contenido.

Base del árbol: `origin/main` fusionó 20 commits más (PR #800, #803) mientras
las dos fases corrían; se re-fusionó dos veces contra este acto (ver §5). Los
62 ids de NC no se movieron ni renumeraron; aparecieron 2 filas nuevas
(NC-0245/0246, GEN2-RESIDUAL-81-1, PR #803) que no estaban en el barrido
original — auditadas aparte, §2.6.

---

## 2 · P1 — Las 62 NC ABIERTA (+ 2 nuevas)

| Veredicto | Filas | Acción tomada |
|---|---|---|
| VIGENTE | 34 + 2 nuevas = 36 | Ninguna — se listan, `estado` sin tocar |
| PREMISA-VENCIDA, confirmada | 20 | **Aplicada**: enmienda fechada en `sucesor` (patrón NC-0024) |
| PREMISA-VENCIDA, refutada | 5 | Ninguna — ver §2.4 |
| DUPLICADA, confirmada | 1 | Propuesta a mesa, sin aplicar (§2.3) |
| DUPLICADA, refutada | 1 | Ninguna — ver §2.4 |
| RESUELTA-POR-PRODUCTO, confirmada | 1 | Propuesta a mesa, sin aplicar (§2.3) |
| CADUCA-POR-DISEÑO | 0 | — |

### 2.1 · Las 20 enmiendas fechadas aplicadas hoy

Todas siguen el patrón exacto que `ACTO GEN2-MARCADOR-C0-D` usó con NC-0024
(15/sep/2026): el texto original de `sucesor` **no se reescribe**; se le
aplica ` || ENMIENDA FECHADA 2026-09-16 (ACTO GEN2-VIGENCIA-DEUDA-1, PROPUESTA
A MESA, no decision del ejecutor): ...` con la medición de hoy y un sucesor
propuesto. `estado` permanece `ABIERTA` en las 20 — esto es medición, no
cierre.

NC-0029 · NC-0048 · NC-0061 · NC-0070 · NC-0072 · NC-0075 · NC-0078 ·
NC-0090 · NC-0098 · NC-0111 · NC-0161 · NC-0170 · NC-0185 · NC-0194 ·
NC-0216 · NC-0228 · NC-0231 · NC-0232 · NC-0236 · NC-0237.

Patrones que se repiten entre varias de estas filas y valen como hallazgo
propio:

- **Trabajo real hecho en una rama nunca fusionada ni con PR abierto**
  (`origin/acto/gen2-f6-panel-caja-1`, commits `698f958a`/`246bbfa9`):
  resuelve de hecho NC-0231, NC-0232, y avanza NC-0161/NC-0230/NC-0233/0234,
  pero viola la política de cero ramas (A.14) — nunca se propuso a mesa.
  Verificado con `mcp__github__list_pull_requests` (cero PR, abierto o
  cerrado, para esa rama). Mesa decide: recuperarla o repetir el trabajo.
- **Bloqueador re-diagnosticado, no resuelto**: NC-0070, NC-0072, NC-0075,
  NC-0078 nombraban a `C0-D`/`C0-C` como sucesor; `C0-D` corrió
  (`GEN2-MARCADOR-C0-D`, 15/sep) pero midió que el bloqueador real es
  θ (`theta.py` lanza `ThetaNoDisponible` en 43/43 entradas) — las cuatro
  filas se re-apuntan a la misma cadena (θ computable → crosswalk de ejes
  firmado → marcador por segmento), no se cierran.
- **Mesa ya decidió, falta la implementación mecánica**: NC-0216 (F-1/F-3,
  HOJA DE FIRMAS DE MESA 2) — la regla de "el veredicto más reciente
  gobierna" está firmada, pero `tools/relevo_usos.py` no la implementa
  todavía. NC-0194 (F-10) — mesa ya decidió suceder la celda ENADID, falta
  la spec.

### 2.2 · Las 36 VIGENTE

Sobreviven las cuatro preguntas con un bloqueador real verificado hoy (mayoría
`PARO-ENTORNO`/`DECISIÓN-DE-MESA-PENDIENTE` genuinos, o filas que ya son el
producto de una re-medición reciente — NC-0239/0240/0241/0242/0243/0244, del
15/sep, un día antes de este acto):

NC-0033 · NC-0037 · NC-0038 · NC-0039 · NC-0055 · NC-0056 · NC-0076 ·
NC-0085 · NC-0107 · NC-0120 · NC-0136 · NC-0151 · NC-0153 · NC-0156 ·
NC-0159 · NC-0162 · NC-0164 · NC-0166 · NC-0202 · NC-0210 · NC-0212 ·
NC-0217 · NC-0218 · NC-0225 · NC-0227 · NC-0229 · NC-0234 · NC-0235 ·
NC-0239 · NC-0240 · NC-0241 · NC-0242 · NC-0243 · NC-0244.

### 2.3 · Propuestas a mesa (no aplicadas — "no decide caducidades")

- **NC-0158 → DUPLICADA de NC-0161** (misma familia F6/roles retenidos,
  confirmado por verificación independiente). Sucesor propuesto: cerrar
  NC-0158 citando NC-0161. **No se cierra aquí.**
- **NC-0174 → RESUELTA-POR-PRODUCTO**. El enlace demanda-ficha que pedía ya
  existe. Sucesor propuesto: cerrar citando el producto real. **No se cierra
  aquí.**

### 2.4 · Las 6 investigadas cuya evidencia no sobrevivió verificación adversarial

Ninguna se tocó — quedan `ABIERTA` con su texto intacto, sin enmienda. La
sustancia de varias probablemente sobrevive una relectura cuidadosa, pero el
camino de evidencia presentado no, y por disciplina A.4/A.13 no se escribe
sobre esa base:

- **NC-0012**: el veredicto (premisa vencida — NC-0007 ya cerró por otra vía)
  se sostuvo en su mayor parte al re-verificar, pero el comando citado para
  fechar la corrección de sucesor citaba un commit que no existe con ese
  contenido. Requiere re-medición antes de escribir la enmienda.
- **NC-0024**: el diagnóstico de fondo (bloqueada por θ, misma deuda que
  NC-0076/NC-0239) se sostiene; lo que no se sostiene es cerrarla como
  DUPLICADA de NC-0239 — la propia nota de cierre de `GEN2-MARCADOR-C0-D`
  dice explícitamente que no cierra ninguna de las siete filas.
- **NC-0026**: el hecho técnico (envoltura no cableada, bloqueada por θ) se
  sostiene; la analogía usada para justificar la acción (que "replica" el
  patrón de NC-0024/NC-0076) no se verificó y no se sostiene tal cual.
- **NC-0213**: el hecho base (spec.yaml sin corregir, NC-0130 cerrada) es
  correcto, pero la cadena causal que declara vencido el bloqueador es falsa
  — NC-0130 ya estaba cerrada desde antes de que se escribiera NC-0213.
- **NC-0230**: sobre-extiende lo que la evidencia prueba (confunde una
  batería de acoso, P4_01-P4_13, con la definición de universo que la fila
  necesita).
- **NC-0233**: el propio informe midió contra una base git desactualizada
  (252 commits detrás de `origin/main` real) y citó un `git grep` que no
  reproduce.

### 2.5 · NO-CORRIDO nuevo, de este mismo acto (A.14)

Como fila propia del ledger, no como enmienda de otra: las 6 investigaciones
de §2.4 y sus dos análogas de P2 son trabajo que este acto empezó y no llegó
a cerrar por sí solo (bloqueado por la calidad de la evidencia de primera
mano, no por el entorno). Se registra: **NO-CORRIDO** — re-verificar y, si
procede, escribir la enmienda fechada de NC-0012/0024/0026/0213/0230/0233 —
razón `NO-VERIFICABLE-AQUÍ` (evidencia de primera mano falló verificación
adversarial dentro de esta sesión) — impacto: esas 6 filas siguen con su texto
sin re-apuntar, aunque el bloqueador real probablemente cambió — sucesor:
`SIN-ASIGNAR` hasta la próxima auditoría o acto que las retome citando NC-0012
et al.

### 2.6 · Las 2 filas nuevas, no incluidas en el barrido original

NC-0245 y NC-0246 (`GEN2-RESIDUAL-81-1`, PR #803) se escribieron en `main`
**después** de que el barrido de P1 arrancara sobre las 62 filas originales.
Verificado hoy: ambas describen deuda recién medida (residual del residual de
81 grupos; consumo del overlay recién publicado), sin producto que las
resuelva, sin duplicado entre las 64 filas ABIERTA actuales, y sin premisa
que pueda haber vencido en horas. **VIGENTE**, sin cambio.

---

## 3 · P2 — Los 65 archivos de `forense/encargos/cola/`

| Veredicto | Archivos | Acción tomada |
|---|---|---|
| LANZADO-COMO, ya ejecutados | 52 | 6 correcciones factuales aplicadas; 46 sin defecto, sin editar |
| CADUCO | 1 | **Movido a histórico** (`## HISTÓRICO — NO EJECUTADO`, patrón A.14) |
| NO-ES-ENCARGO | 12 | Sin cambio — no son encargos despachables |
| SUPERADO-POR | 0 | — |

### 3.1 · Las 6 correcciones factuales aplicadas

Todas encontradas por la capa de verificación adversarial, no por el
investigador original:

1. **`POST-694/15-GEN2-ENIF-FINTECH-SERIE-DESCRIPTIVA.md`** — decía "PR #706
   abierto; merge reservado a mesa". Falso desde hace 5 días:
   `mcp__github__pull_request_read` confirma `merged: true`,
   `merged_at: 2026-09-11T05:49:02Z`. Corregido.
2. **`POST-701/18-GEN2-MOTOR-Y-HERENCIA-EXPLICITA.md`** — mismo defecto, PR
   #712, `merged_at: 2026-09-11T15:56:35Z`. Corregido.
3. **`POST-701/19-GEN2-EVALUACION-SIN-FUGAS.md`** — mismo defecto, PR #713,
   `merged_at: 2026-09-11T17:00:37Z`. La frase falsa se escribió 1h33min
   *antes* del propio merge y nunca se actualizó. Corregido.
4. **`POST-707/20-GEN2-CNBV-CONDUSEF-FUENTES-Y-SERIES.md`** — mismo defecto,
   PR #717, `merged_at: 2026-09-11T21:29:29Z`. Corregido.
5. **`POST-726/34-GEN2-REACTIVOS-CON-TEXTO-Y-BUSQUEDA.md`** — sin ninguna
   cabecera `ESTADO:`. El homónimo archivado
   (`forense/encargos/2026-09-11-GEN2-REACTIVOS-CON-TEXTO-Y-BUSQUEDA.md`)
   trae `## CONSUMIDO · PR #742`, pero es un **trasplante erróneo**: PR #742
   nunca tocó ese archivo (trajo, en cambio, el Encargo 39, de nombre
   parecido); el PR real es #737, confirmado por diff contra primer padre y
   por la propia cabecera original del archivo ("Estado: CONSUMIDO por PR
   #737"). Corregido en la copia de cola citando #737. **El defecto en el
   archivado (`## CONSUMIDO · PR #742`) NO se corrigió aquí** — fuera del
   perímetro de esta auditoría (cola/, no encargos/ archivados) — queda
   para un acto de mantenimiento con ese perímetro.
6. **`POST-685/06-GEN2-ADQUISICION-DIRIGIDA-Y-DIN.md`** — su `BITÁCORA:`
   citaba `forense/encargos/2026-09-10-GEN2-ADQUISICION-DIRIGIDA-Y-DIN.md`,
   que **no existe** (`git cat-file -e` falla) — a diferencia de sus 4
   hermanos del mismo lote (01-04), este ítem nunca recibió su homónimo
   archivado. PR #693 sí es real y fusionado; la nota de cierre sí existe.
   Corregido para citar la nota de cierre real; se deja explícito que falta
   completar el archivado (decisión de mesa, no de esta auditoría).

### 3.2 · El único CADUCO: movido a histórico

`2026-09-02-MAESTRA35-L10-OLA6-SALUD-L1.md` → movido de `cola/` a
`forense/encargos/`, con cabecera `## HISTÓRICO — NO EJECUTADO` (patrón A.14,
mismo criterio que `2026-09-03-MAESTRA37-L2-MPS-CODEBOOK-Y-P3.md`). Ya
llevaba `ESTADO: RETIRADO` desde el 7/sep/2026 (D12, `ACTO
MAESTRA38-TRAMITE-3`); nunca se ejecutó con ningún nombre. Sin ambigüedad ni
riesgo de colisión T02 (nunca tuvo homónimo).

### 3.3 · Los 46 LANZADO-COMO sin defecto — sin editar, por decisión de alcance

Confirmados por verificación adversarial independiente: PR real y
fusionado, homónimo (propio o externo) con `## CONSUMIDO` correcto. La
mayoría tiene una brecha puramente cosmética (falta el renglón de
`BITACORA:` que el patrón 2-ter pide junto con la corrección de `ESTADO:`,
o alguna redacción menos formal) que **no afecta la mecánica real** — `T37
T-COLA-SINCRONIZADA` y `tools/cierre_acto.py` ya los reconocen como
sincronizados. Se listan para que mesa decida si vale la pena homogeneizar
la redacción; no se tocaron 46 archivos por una brecha cosmética repetida
cuando el campo operativo (`ESTADO:`) ya es correcto.

### 3.4 · Los 12 NO-ES-ENCARGO

Índices de lote (`00-LEEME-*`), la adenda `ADENDA-09-CIERRES-YA-ACREDITADOS`
ya cubierta por §3.1, el índice general
`2026-09-07-ENCARGOS-GEN2-en-orden.md` (`ESTADO: INDICE-DE-COLA — NO SE
DESPACHA`, declarado así por su propio autor) y el documento de revisión
`REVISION-CANDADOS-GEN1-GEN2-2026-09-11.md`. Ninguno es un encargo
despachable; el mapeo LANZADO-COMO/SUPERADO-POR/VIGENTE/CADUCO no les aplica.
Sin cambio.

### 3.5 · Pregunta de política abierta para mesa — no decidida por esta auditoría

El encargo dice, verbatim: *"Entregable: la cola queda con solo lo
lanzable"* y que "los muertos" (que incluiría LANZADO-COMO, agrupado junto a
SUPERADO-POR/CADUCO) van a histórico, "no se borran ni se quedan en cola".
Leído literalmente, los 52 `LANZADO-COMO` deberían **salir físicamente** de
`cola/`. Pero el mecanismo YA establecido y probado
(`.claude/commands/despacha.md` 2-ter, `T37 T-COLA-SINCRONIZADA`,
`tools/cierre_acto.py::cola_desincronizada`) asume exactamente lo contrario:
que un `CONSUMIDO` se corrige *in situ* y permanece en `cola/` para que
`/despacha` no lo retome. Mover los 52 archivos exige además decidir, caso
por caso, si cada uno se **retira** (cuando ya existe un homónimo externo con
`## CONSUMIDO` — precedente real: PR #747, "copia de cola retirada") o se
**archiva** (cuando la copia de cola es el único registro) — y en varios
casos (lotes `POST-685`, `POST-693`, etc.) mover unos ítems y dejar el
`00-LEEME` del lote crea un índice que apunta a archivos que ya no están
donde dice. Esta auditoría **no ejecuta esa reorganización** — la deja
evidenciada, con la lista completa de los 52 candidatos y su disposición
(retirar/archivar) en `forense/encargos/cola/` mismo, para que mesa decida
entre (a) mantener el patrón 2-ter (cola con etiquetas correctas, no
físicamente vacía) o (b) autorizar el barrido físico completo, con o sin un
acto dedicado a reconciliar los índices de lote.

### 3.6 · Hallazgo nuevo, fuera de perímetro: `tools/tablero_programa.py` no lee `ESTADO:`/`BITACORA:`

Medido en la verificación de `2026-09-07-GEN2-E4-LIMPIEZA-C2-PODA.md`: el tablero
derivado (`forense/tablero/TABLERO-PROGRAMA.md`) clasifica cola por el
substring literal `"## CONSUMIDO"` en el cuerpo crudo
(`tools/tablero_programa.py:269`), no por la cabecera `ESTADO:`. Confirmado
sistémico, no aislado: `2026-09-07-GEN2-E2-C0-A-DEMANDA.md` (ESTADO dice
CONSUMIDO) sigue `GATED` en el tablero; `2026-09-07-GEN2-E1-LIMPIEZA-C1.md`
sigue `LISTO`. Ningún
test cruza `tools/tablero_programa.py::cola_encargos` contra `ESTADO:` real
— el desfase es silencioso. Fuera del perímetro de este acto
(`tools/tablero_programa.py` no está en "no-corrido, cola/ e histórico,
tests/check.py, nota"); se declara aquí para que mesa lo asigne.

---

## 4 · P3 — WARN `T43 T-SUCESOR-EXISTE` en `tests/check.py`

Ejecutado y comiteado antes de este barrido (`f89591c`). Encontró, de
inmediato y sin falsos positivos sobre las 62 filas, los dos casos reales que
motivaron el gate D-14 del encargo: `NC-0075` cita `ACTO C0-C` (nunca
redactado) y `NC-0218` cita `ACTO D-A` (declarado ausente por su propia
fila). Después de las 20 enmiendas de §2.1, el conteo de WARN de `T43` puede
cambiar — se reporta el valor final en `tests/check.py --baseline` de este
mismo acto (§5).

---

## 5 · `tests/check.py --baseline`, dos corridas

1. Después de las 6 correcciones + el archivado de MAESTRA35-L10 (P2),
   antes de las 20 enmiendas de P1: `T02`/`T37` en verde (sin colisión de
   nombre, sin desincronización nueva).
2. Después de las 20 enmiendas de P1 (final): ver salida cruda pegada en el
   PR de este acto.

## NO-CORRIDO / RESERVAS

Ver `## NO-CORRIDO / RESERVAS` al final del encargo archivado
(`forense/encargos/2026-09-16-GEN2-VIGENCIA-DEUDA-1.md`), que es donde A.14
exige que viva — esta nota es la memoria de trabajo, esa sección es el
registro exigido.
