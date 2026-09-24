# ENCARGO · ACTO GEN2-RELEVO-MOTOR-34-1 · Las 34 lecturas legacy que el motor todavía usa para contestar, relevadas una por una: pin a un RESULT sellado, CALC de re-medición, o regla nueva por el escritor con campos redactados; al cerrar, el motor contesta solo con GEN2 o dice por qué no

> ENTORNO: **NUBE** para pines y escritor; si una lectura exige re-medir desde microdato, esa pieza se declara y va a un CALC en **CAJA** dentro del mismo acto (la sesión cambia de entorno o abre uno hermano; se declara). Hook imprime ENTORNO-DERIVADO.

CABECERA · SHA de redacción `8358b891` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-relevo-motor-34-1` (o la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: mueve `dependencias_numericas_legacy_activas_por_consumidor__motor` 34 → 0 (o el residuo con NC por lectura); `adoptados` sube por cada regla o pin que el escritor materialice. Escribir el motor es adopción: **merge de mesa**.

## 1 · OBJETIVO
Es la deuda más visible del programa: 231 lecturas del motor, 85 GEN2, 146 legacy, siete cortes sin moverse; de las 146, las **34 del consumidor `motor`** son las que responden al usuario. Con el escritor extendido (ADOPCION-4: crea reglas desde propuesta), el contrato del catálogo consistente (CATALOGO-1) y las vías de relevo firmadas (4.1 del 21/sep; D6), ya no hay razón de proceso para no cerrarlas. (P1) Inventario por comando de las 34 (desde `usos.tsv` re-derivado en árbol y `relevo-usos-v1_0.tsv`): llave, valor legacy, dónde vive en `milpa/`, qué RESULT GEN2 la cubre si existe (por conducta y texto de pregunta, A.15), vía candidata. (P2) Por lectura, en este orden: **vía (i)/(ii)** pin a RESULT sellado con replay afirmativo (eje RESULTADO, D6) → escritor escribe etiqueta; **vía (iii)** derivado determinista de GEN2 → pin clase iii; **regla nueva** desde una propuesta o desde un RESULT con campos redactados (`PROPUESTO-POR-EJECUTOR`, fuente en el report GEN1); **re-medición** (E.1: GEN1 que agregó de otro modo) → CALC en caja con COMMIT-1; **NO-CONSTRUIBLE** con texto de pregunta buscada y FD recorrido. (P3) Diff seco del motor pegado, `--apply` por el escritor, tests por llave, motor carga y emite, `T-REPRO` VERDE. (P4) Tabla final «34 → vía → estado» y `status` en árbol antes/después.
«Hecho»: `legacy_activas_por_consumidor__motor` en árbol re-derivado = 0, o = residuo con una NC por lectura (razón de la lista de A.14) · cada pin con fila en `pines-de-mesa.tsv` y las cuatro guardas · cada regla nueva con `p` = RESULT por test · `milpa/*.yaml` sin edición manual (solo escritor; diff en la nota) · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas, verbatim
**4.1 (21/sep)**: vías de relevo (i)/(ii)/(iii) con cuatro guardas automáticas y canal por firma. **D6 (23/sep)**: «La vía (i) de relevo lee el eje RESULTADO; CONTEXTO se declara en la nota del pin.» **D7 (23/sep)**: motor editable con perímetro. **N (24/sep)**: escritor extendido según contratos; momento 08 unidad DELITO. **W (24/sep) + INTERPRETACIÓN de ADOPCION-4**: reglas nuevas por el escritor, campos pendientes redactados y rotulados, merge de mesa. **Cláusula v1.0**: un campo `PENDIENTE-DE-MESA` heredado no es PARO, es un campo por redactar.

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` `status` (usos.tsv del 21/sep): motor 34 · procedencia 40 · catálogo 23 · marco 43 · celdas-D 6; `tramite.yaml`: 22 reglas + 3 de ADOPCION-4, 56 etiquetas `corrida0_resultado_id`. `[LEÍDO]` `forense/analisis/astra4-relevo/` (estado-y-decision, contratos, cotejo documental): el trabajo de Astra U2 es el inventario de partida; se cita, no se rehace. `[LEÍDO]` ADOPCION-1 y -2: el pin `i-CRUDO` al catálogo rompió T-REPRO(c) (resuelto por CATALOGO-1: verificar que fusionó, #1115). `[SUPUESTO]` que la mayoría de las 34 tienen RESULT GEN2 por conducta (el catálogo de U1 lo sugiere); las que no, se re-miden o se dictaminan.

## 4 · YA HECHO / YA DECIDIDO
`git ls-remote --heads origin | grep -i relevo` → 0 (Astra U2 fusionó #1073/#1091/#1092). Pines existentes: `data/corrida0/pines-de-mesa.tsv` (51 líneas; vías i 14 / ii 13 / iii 1): los ya firmados se aplican aquí si el escritor no lo hizo.

## 5 · PIEZAS
P1 inventario 34 → P2 relevo por lectura (pin > regla > re-medición > dictamen) → P3 escritor, tests, motor → P4 tabla y `status`.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja; lo no alcanzado va a NO-CORRIDO. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir ola reservada · b) editar `milpa/*.yaml` a mano, reescribir un sello, cambiar un `p` sin RESULT · c) mover contadores a mano · d) cambiar un procedimiento congelado · e) —

## 8 · COMPUERTAS
«Motor solo por escritor, diff seco, test por llave» protege: **adoptar / congelar**. «Pin solo con replay afirmativo (eje RESULTADO)» protege: **adoptar**. «Merge de mesa» protege: **adoptar** (E.2).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `milpa/*.yaml` (solo escritor), `tools/escribe_relevo_consumo.py` + tests, `data/corrida0/pines-de-mesa.tsv` (filas nuevas sin firma → FP; aplicar las firmadas), `forense/analisis/relevo-motor/`, CALC de re-medición si los hay (caja), `replay-evidencia.tsv`, TSV de gobierno, nota, L0, cascada. Ajeno: procedencia (40), catálogo (23), marco (43), celdas-D (6) — son `RELEVO-CONSUMIDORES-2`, no este. En vuelo: los cinco de caja (no tocan `milpa/`), TABLERO-EN-CANAL (CI).

## 10 · LO QUE NO HACE · SUCESORES
No releva los otros consumidores; no adopta lo de Astra. Sucesores: `GEN2-RELEVO-CONSUMIDORES-2` (procedencia, catálogo, marco, celdas-D); FIRMAS-16 asienta pines y reglas.

## NO-CORRIDO / RESERVAS

| qué (verbatim) | por qué | impacto | sucesor |
|---|---|---|---|
| «P2 relevo por lectura» — 8 lecturas ASIGNADO con hermano GEN2 (RES-0001/0002/0007/0008/0019/0020/0023/0024) | DECISIÓN-DE-MESA-PENDIENTE: `emitir_binaria` devuelve el par ASIGNADO; sustituirlo por el medido cambia el estimando, no es relevo | `legacy_activas_por_consumidor__motor` no baja en 8 | FIRMAS-16 (FP-260924-GEN2-RELEVO-MOTOR-34-1-a157-01); NC …-a157-01..25 por lectura |
| ídem — 4 lecturas NO-ADOPTAR-NC-0107 (RES-0009..0012) | DECISIÓN-DE-MESA-PENDIENTE: rotuladas «sólo historia» pero activas | no baja en 4 | FIRMAS-16 (FP …-a157-02) |
| ídem — 6 cortes `CORTES_C1` (RES-0165..0170) | DECISIÓN-DE-MESA-PENDIENTE: dato sellado sin RESULT numérico; sacarlos del contador sería moverlo a mano | no baja en 6 | FIRMAS-16 (FP …-a157-03) |
| «re-medición (E.1) → CALC en caja con COMMIT-1» — RES-0017/0018, RES-0029/0030, RES-0050..0052 | DIFERIDO-A:GEN2-RELEVO-MOTOR-34-2-CAJA: sesión NUBE sin corpus; L8 ingiere un JSON GEN1 (4.1) | no baja en 7 | GEN2-RELEVO-MOTOR-34-2-CAJA |
| «`check.py --baseline` VERDE» | NO-VERIFICABLE-AQUÍ: la sesión corre `--rapido` (0 FAIL) y `T-REPRO` aislado (0 FAIL); la suite completa la juzga el CI del PR | ninguno si CI verde | CI del PR |
| «cada pin con fila en `pines-de-mesa.tsv`» | SUSTITUIDO-POR:escritor V3 — para el motor la marca del consumidor manda sobre el pin (`corrida0.py:4485`); las cuatro guardas corren en `guardas_v3`. Huérfano: la clase (iii) no se muestra aparte en `status` (hallazgo) | `relevadas_por_pin_de_mesa__iii` sigue en 0 | SIN-ASIGNAR |
