# ENCARGO · ACTO MOTOR-3/E0 — CUERPO AUTOCONTENIDO (para la sesión ya abierta: responde el widget con "opción 2" y sube ESTE archivo)
### 14/ago/2026 · dirección · verificado contra `origin/main = 865b54a` (#234: esqueleto del ADR del sello EN MAIN, `forense/ADR-MOTOR-2-esqueleto-2026-08-14.md`, SIN sellar; RONDA-M fusionada #233: **APROBAR CON CAMBIOS, cero defectos conceptuales**)

## GATE MAESTRO — léelo antes que nada, resuelve tu situación actual
Fuiste lanzada ANTES del sello. Eso NO te detiene: te parte en dos.
```bash
git fetch -q origin && git checkout -q origin/main 2>/dev/null || git merge -q origin/main
grep -cE "^\*\*ADR-8[4-9] .*(motor|matriz|M1)" canon/gobernanza-v1_15.md   # 0 = SIN SELLO: solo FASE-PLAN. ≥1 = SELLADO: lee ese ADR íntegro, llena las ranuras M de abajo con SUS firmas verbatim, y ejecuta completo.
```
**SIN SELLO (hoy):** ejecutas SOLO la FASE-PLAN — commit A.3 (este archivo verbatim a `forense/encargos/`) + `forense/notas/<fecha>-motor3-plan.md` con el diseño completo de `milpa/src/` (módulos, firmas de funciones, contratos de I/O, plan de tests) derivado de los insumos de abajo. **CERO archivos en `milpa/src/`, cero código ejecutable, cero catálogo** — el diseño se presenta a mesa y esperas. Re-corres el gate al retomar.
**CON SELLO:** todo lo de abajo, en orden.

## INSUMOS — todos EN EL REPO, con ruta exacta (nada que pedir al chat)
1. **La definición del ejecutable:** el ADR del sello (cuando exista) + `propuesta-motor-matriz-v0_1.md` §1-§5 **corregida por el veredicto de RONDA-M** (`forense/RONDA-M-motor-matriz-veredicto-opus-2026-08-13-v1_0.md`): los **12 defectos materiales + 3 de cita se aplican como checklist** — cada uno con su fix de una línea del propio veredicto; tu nota lista los 15 con "aplicado en <archivo:línea>".
2. **La cascada medida:** `forense/CASCADA-M1-2026-08-14.md` — banner ADR-62 (`milpa/milpa-spec-v0_2.md:4-6`), gate de Fase 1 (`milpa/milpa-plan-v0_1.md`), sitios del ejecutable en `modelo` (22 g.l.: `modelo:260,628`), veredicto sobre `4 de 144`.
3. **El contrato de insumos:** `milpa/procedencia.yaml` es LA fuente — tu código LEE clases y las respeta: `MEDIDO·NACIONAL` jamás se segmenta por eje · `MEDIDO·PARCIAL(x)` solo sobre sus ejes x · `ASIGNADO` con su banda declarada · `GATE·ID-X` excluye (el gate detiene, no estima) · `PENDIENTE` no entra. Violación de clase = bug de contrato, test lo atrapa.
4. **La escala de falsación:** `propuesta-motor-matriz-v0_1.md` §6 (líneas 188-191), **verbatim con su regla de precedencia** — es TU escala; declara antes de correr qué significa que el falsador no refute (B-bis).
5. **Los 7 umbrales go/no-go:** ADR-68, `canon/gobernanza-v1_15.md:906-916` — se transcriben como **asserts ejecutables** en `tests/` del motor; el go/no-go de Fase 1 se decide por comando.
6. **π(x):** anclada en `milpa/procedencia.yaml` (ej. `tasa_informalidad {v:0.31, src:ENOE, sae:true}`) y tick trimestral (`milpa/milpa-spec-v0_2.md:269`); los cortes por eje = **[RANURA M2 del ADR]**; si el ADR delega cortes a un acto de datos, tu plan lo nombra y NO los inventa.
7. **Las 3 celdas-semilla:** `data/curacion-registro/celdas-d/` (radio — clase `CONVERGENTE-CONFIGURAL` por ADR-82 · familismo.actitud · obligación_medida) — tu rebanada corre ESTAS tres contra momentos `AJUSTE`.

## RANURAS DEL SELLO (se llenan del ADR, verbatim — hoy vacías a propósito)
**M1** (¿matricial como definición; antes del gate de Fase 1 o espera su veredicto; banner ADR-62): ______ · **M2** (cortes de `D` por eje, tres ejes de hogar respetados; quién los sella): ______ · **M3** (`G1b` campo medio como HIPÓTESIS declarada): ______ · **M4** (catálogo de momentos = el pre-registro de `gobernanza:461`, roles `AJUSTE`/`HOLDOUT` sellados ANTES de escanear): ______ · **M5** (libro de demanda como fuente única del curador, o cruce declarado): ______ · **M6** (compass: YA en repo vía MOTOR-1 — la ranura registra si el ADR los cita): ______

## PERÍMETRO Y REGLAS (fase CON SELLO)
ESCRIBE: `milpa/src/**` (nuevo) · `milpa/catalogo-momentos-v0_1.md` + su tabla · `tests/` SOLO tests nuevos del motor (`test_motor_*.py`) · nota · A.3 · hallazgos (union). **NO ESCRIBE:** `tools/curador_registro/**` (**ventana ADR-70(d) CERRADA — consumes, no tocas**) · `canon/**` · `data/curacion-registro/**` · `relaciones.tsv` · manifiesto. **LEY DE MESA vigente (cableada en el ENCARGO BARRIDO-2):** E0 compila y reproduce lo YA adjudicado — **prohibido producir cifra nueva al canon**; toda calibración E1+ espera el cierre de BARRIDO-2. Fuera de la lista: PARA.

## COMMITS (fase CON SELLO)
**C1 · El catálogo, constituido ANTES de escanear:** momentos del piloto finanzas-del-hogar enumerados según **[M5]** desde el libro de demanda; **roles `AJUSTE`/`HOLDOUT` sellados en ESTE commit** — tocar un momento `HOLDOUT` después es violación de pre-registro, y un test lo vigila; π(x) con los cortes de **[M2]**; `G1b` según **[M3]**; la escala §6 copiada verbatim como la tuya; los 7 umbrales como asserts (skip-hasta-datos permitido, texto verbatim obligatorio). Frase de siempre.
**C2 · La rebanada que corre:** `milpa/src/` mínimo que (a) carga `procedencia.yaml` validando clases (insumo 3), (b) construye π(x) y el estado, (c) evalúa las 3 celdas-semilla contra momentos `AJUSTE` — **holdout intocado, con test que lo prueba**, (d) salida determinista con hash (misma semilla ⇒ mismo hash, test incluido). `python3 tests/check.py --baseline` cruda (base vigente por `tests/baseline.json`, hoy `0ad9b7b` — re-derívala, no la heredes de aquí).
**C3 · Cierre:** los 15 fixes de RONDA-M aplicados y listados · el estado del gate de semana 1 de ADR-68 declarado · contador nuevo del programa nace: **"momentos HOLDOUT reproducidos: 0 de M"** — y desde hoy se cuenta.

**Qué NO haces bajo ninguna fase:** no calculas β/θ nuevas · no tocas la Entrada 5 (E5, ajeno) · no sellas nada · no editas la matriz (si un fix de RONDA-M exige texto nuevo de la propuesta, va como `propuesta-motor-matriz-v0_2.md` PROPUESTA a mesa, no como edición del v0_1).

---

## ADENDA · 18/ago/2026 — RANURAS DEL SELLO, llenas · `ACTO LANE-A-E0-E5`

**Cuerpo del encargo, sin editar.** Las seis ranuras de arriba se conservan vacías tal como se lanzaron: A.3 pide el texto verbatim del encargo, y reescribirlo destruiría la auditoría de qué se pidió exactamente. Las firmas se registran **aquí**, en adenda fechada — mismo mecanismo que `ACTO CONSOLIDA-2` usó para `CONSOLIDA-17AGO`.

**Gate maestro, re-corrido contra el árbol (no heredado, y con el rango del predicado ampliado a los ADR de tres dígitos que el original no contemplaba):**

```bash
grep -cE "^\*\*ADR-(8[4-9]|9[0-9]|10[0-9]) .*(motor|matriz|M1)" canon/gobernanza-v1_15.md   # → 1
```

`1 ≥ 1` = **SELLADO**. El ADR que lo cierra es `ADR-100` (`canon/gobernanza-v1_15.md:1811`). La fase **CON SELLO** se ejecutó completa: C1 (catálogo), C2 (rebanada), C3 (cierre).

**Las firmas, verbatim de `ADR-100`.** Mesa no dio seis firmas separadas: dio **una firma por lote** con una cláusula propia por M dentro de la misma frase. La firma, entera y una sola vez — `ADR-91`, `PR #246`, 17/ago/2026: *"Adelante con la propuesta."* sobre el texto adoptado: *"Doy por firmadas M1-M6 con los textos recomendados del 14/ago […], CONDICIONADAS a que al cierre de BARRIDO-2 dirección re-verifique M2/M4/M5 contra el universo nuevo: si no cambian, el sello procede sin volver a mesa; si alguna cambia, vuelve a mesa solo esa."*

- **M1** — *"M1 cómputo matricial como definición del ejecutable"*. Adoptado con la rama del gate: procede **antes** del gate de Fase 1 de `milpa-plan` (`ADR-100(1)`). **Incondicional.**
- **M2** — *"M2 cortes iniciales por eje conforme a la cascada, respetando los tres ejes de hogar"*. Dueño del sello por eje: **el catálogo de momentos, en su commit 1** (`ADR-100(2)`) — ejercido en `milpa/catalogo-momentos-v0_1.md` §3. **CONDICIONADA** por el inciso (9).
- **M3** — *"M3 campo medio para G1b con estatus HIPÓTESIS"*. **Incondicional.**
- **M4** — *"M4 catálogo de momentos como pre-registro de gobernanza:461, roles AJUSTE/HOLDOUT sellados en su commit 1"*. **CONDICIONADA** por el inciso (9).
- **M5** — *"M5 libro de demanda como fuente única del curador"*, con la rama "fuente única" gateada por el GO del piloto — no choca con `ADR-68(a)`, lo respeta. **CONDICIONADA** por el inciso (9).
- **M6** — *"M6 los compass ya están en el repo y el ADR los cita"*. Era la única M que bloqueaba el sello por sí sola; con los cinco archivos del espejo en el árbol desde `PR #237` y esta firma, deja de bloquear. **Incondicional.**

**La condición, no retirada.** `ADR-100(9)`: la re-verificación de `M2`/`M4`/`M5` contra los productos semánticos del barrido **queda en el carril B y NO la sustituye este sello**. `M1`/`M3`/`M6` viajan en DISPARADOR-A, que es el carril de este acto; `M2`/`M4`/`M5` llevan la condición y viajan en DISPARADOR-B.

**Estado:** `CONSUMIDO` — fase FASE-PLAN por `ACTO MOTOR-3/E0` (`PR #237`, 14/ago/2026); fase **CON SELLO** por `ACTO LANE-A-E0-E5`, este PR, 18/ago/2026.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fn -- "2026-08-14-MOTOR-3-E0-autocontenido.md" canon/gobernanza-v1_15.md` cita ADR-101, ADR-128, pero el bloque mezcla lenguaje de ejecución y de encargo pendiente (o el rótulo del ADR es compartido entre varios encargos sin desenlace individual claro) — rastro parcial, no se decide aquí. Para mesa: verificar manualmente contra ADR-101, ADR-128 en canon/gobernanza-v1_15.md.
