# GEN2-TRAMITE-PENDIENTES-1 · nota de cierre

ACTO GEN2-TRAMITE-PENDIENTES-1 · 22/sep/2026 · NUBE (`ENTORNO-DERIVADO = NUBE`, `cloud_default`, red DENEGADA-POR-POLITICA, corpus no montado, 0 archivos examinados) · cero microdato · Opus 5.5 · sin sub-agentes · MODO ABIERTO · COMPUERTA: ninguna (§8 del encargo es un orden sugerido; #1004 y #1001 ya estaban fusionados al abrir).

Encargo: `forense/encargos/2026-09-22-GEN2-TRAMITE-PENDIENTES-1.md` + `.cuerpo.sha256` (`aef8828d…`), 0-bis `18fab80`. SHA de redacción `31da26e0`. Base al abrir: `origin/main = 8ddb42d` (merge de #1004), 0 detrás. Antes de la cascada se fusionó `origin/main = 0f83308` (#1005). Guard 0.c: sin rama, worktree ni PR abierto con el rótulo (5 PR abiertos: #1002, #1003, #1005, #1007, #1009).

**¿Cuántos contadores movió este trabajo?** Cero mediciones. `corrida0.py status`: `N_corridas_selladas` 156 → 160 por P1(a) (después del merge de #1005, 161); `N_resultados_gen2_pendientes_adopcion = 12` sin cambio (este acto no adopta); `no_corrido_abiertas` 203 → 201 (antes del merge).

## 1 · Premisas re-verificadas

| Premisa del encargo | Rótulo | Resultado |
|---|---|---|
| `grep -c PENDIENTE-DE-MESA corridas.tsv` → 22 | EJECUTADO | Se sostiene como `grep`. Por campo (`cuenta_gen2`, con un lector de CSV) son **21**: la línea 22 es `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`, que lleva el texto en otra columna. |
| Las 4 corridas de P1(a) sin fila de contador | por objeto | Ninguna tenía fila en `decisiones.tsv`. Hallazgo: la firma 3B del 21/sep («4 sin replay no cuentan todavía») era sobre exactamente estas cuatro; #1004 asentó replay REPRODUCE/IDENTICO de las cuatro y cerró NC-0447. P1(a) no contradice 3B: su condición ya se cumplía. |
| P1(b): las lecturas Codex llevan `cuenta_gen2 = NO` | firma | **Falsa. Toca una firma de mesa, así que no se asentó.** Los CALC de NC-0316/0320/0321/0326 (`WBES2023-CORRUPCION-DESCRIPTIVA-0001`, `ENCRIGE-CARGA-INTENSIDAD-0001`, `WBES2023-PRECISION-0001`, `ENIGH2022-INTENSIDAD-REMESAS-0001`) ya cuentan SI por la firma 3A del 21/sep, y los cuatro tienen replay REPRODUCE. Asentar NO restaría 4 a `N_corridas_selladas`. Va a mesa en `FP-260922-GEN2-TRAMITE-PENDIENTES-1-18fa-02`, con opciones. |
| «Hecho»: `grep -c` baja en exactamente 4 | logística | **No se puede cumplir por PR.** Desde #984, `tools/derivados_protegidos.py` (verify.yml, firma §2(2) de TUBERIA-EFICIENCIA-1) prohíbe que un PR toque `corridas/resultados/usos.tsv`, y el canal que los publica (T6, `FP-…-c09b-02` opción (a), FIRMADA) aún no corre. `registro --escribe` se corrió en local y se revirtió en un commit propio (`git checkout origin/main --` de los tres derivados). En seco, sobre las 285 filas previas, **solo cambian las 4 de P1(a)** (21 → 17). Sin embargo, la vista estaba atrasada 18 corridas selladas no registradas, y 10 de ellas nacerían PENDIENTE-DE-MESA por etiqueta (ENIGH 2016/2018/2020 ×3 y `ENIGH-DUELO-ORIGEN-MOVIL-0001`). Cuando T6 corra, el `grep` subirá, no bajará. Lo que el criterio buscaba se verifica por `status`. |
| 12 RESULT con valor GEN1 por comando | SUPUESTO | El comando no los expone: `status` solo da la cuenta. Se derivaron con el mismo filtro de `status` (`tools/corrida0.py:4867-4887`) desde el registro en memoria. `valor_legacy` de la vista = NO-COMPARABLE en los 12. Solo `RESULT-EDER-A-P` tiene lectura previa (`p=0.996086`, propuesta:110-117, «MISMO estimando que la tasa de fase 1»). Las otras 11 reglas nacieron GEN2 (0 menciones en `milpa/tramite.yaml`): `NO-DERIVADO`, dicho en la hoja. |
| Tabla SENAL-1 con 10 filas BANDEJA-TITULAR | EXISTE | La tabla trae 13 filas (derivada el 20/sep); 3 ya están CERRADAS → 10 abiertas. No trae receta por fila; las recetas salen de cada NC y de los expedientes. NC-0156 y NC-0166 están también entre las 5 HUMANO → **13 entradas únicas, no 15**. |
| T6 en main | por objeto | `FP-260922-GEN2-PENDIENTES-CAJA-1-c09b-02` FIRMADA (opción a) en main por #1004, y cubre también `…0af9-01` (#1005). |
| #1002 (MARGINALES-ADOPCION-1) toca los 12 RESULT | tipo (3), rama | No: sus objetos son 57 pisos t-1 marginales. |

Pregunta de §6 (¿algún RESULT con `verify = NO-REPRODUCE`?): no aplica. Los 12 están en REPRODUCE/IDENTICO.

## 2 · Piezas

- **P1(a).** 4 filas `cuenta_gen2=SI` en `data/corrida0/decisiones.tsv` con la firma verbatim. `_cuenta_gen2_resuelto` las proyecta: `status` pasa de 156 a 160.
- **P1(b).** NO ASENTADA: FP `-18fa-02`. NC-0316/0320/0321/0326 siguen ABIERTAS y sin tocar.
- **P1(c).** NC-0259: enmienda fechada con la firma; sigue ABIERTA. Fila en `decisiones.tsv`.
- **P2.** `FP-260922-GEN2-TRAMITE-PENDIENTES-1-18fa-01` sobre `forense/notas/2026-09-22-GEN2-TRAMITE-PENDIENTES-1-hoja-adopcion.tsv` (sha256 `76c269f7…`). La recomendación es ADOPTAR 10 y VETAR 2: `RESULT-CTX-2021-P-ALTO`, porque el valor es nulo, y `RESULT-EDER-A-P`, porque su regla es SELLADA-SIN-CARGA por D2-b. Se citan como precedente los dos vetos C1-POSEL. No se adopta nada.
- **P3.** `7ef3-02` → CERRADA con la firma (26/35), con fila en `decisiones.tsv`. `8e53-01` → CERRADA por superación, citando T6. `8e53-04` → ABIERTA: mesa no rellenó los tres huecos y la pregunta queda escrita en la enmienda. `b6dc-02` → (i) y (iii) resueltas con E.2 y E.6; (ii) es la FP `3d56-01`, física, así que la fila sigue ABIERTA. `48d4-02` → ABIERTA, con el sucesor que nombra F8 (el canal de relevo). NC-0161/0162 → enmienda con sucesor en la adquisición dirigida (NUBE-MEDICIÓN) y el dictamen EN-ESPERA-PANEL (`dfbe-01`, #998).
- **P4.** `forense/notas/2026-09-22-BANDEJA-TITULAR.md`: 13 entradas únicas más una añadida (8e53-04). Ninguna NC cambia de estado.
- **P5.** Una línea en `forense/hallazgos.md`, con las cifras re-contadas (11 + 7 = 18).

## 3 · Firmas de mesa

Firmas asentadas verbatim desde §2 del encargo: P1(a), P1(c), P3-7ef3-02. No se asentaron dos: P3-8e53-04, porque sus huecos están en blanco, y P1(b), por el choque con 3A. Las firmas ya selladas (T5/T6, `dfbe-01`, E.2, E.6) se citan y no se duplican.

## 4 · Firma recibida con el PR abierto (22/sep/2026), verbatim

Mesa respondió a FP `-18fa-02`: **«a»**. Asentado en este acto (A.12): la FP pasa a FIRMADA. NC-0316, NC-0320, NC-0321 y NC-0326 pasan a CERRADA, con la firma como cita y sucesor «cita en TRA v-siguiente». `NC-…-18fa-01` pasa a CERRADA. Se añade una fila en `decisiones.tsv` sobre el objeto FP; no hay fila de contador y `cuenta_gen2` de los cuatro CALC sigue en SI por 3A.
