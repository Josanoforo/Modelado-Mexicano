# ENCARGO · ACTO GEN2-AUDITORIA-POST-HOC-ASTRA-1 · Los catorce PR de Astra que entraron a main sin recibo, auditados con los seis criterios del recibo; lo que no debió entrar se revierte por acto sucesor, no se edita en main

> ENTORNO: **NUBE** — lee main, RESULT sellados y el manifiesto. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `6a2cd6c7` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-auditoria-post-hoc-astra-1` (D-17) · MODELO: Opus (lote grande con CALC nuevos) · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; no adopta; no mueve `cuenta_gen2`; no revierte nada (propone reversión por FP).

## 1 · OBJETIVO
Sustituye a `RECIBO-ASTRA-PRODUCTO-2/3/4` (retirados: sus PR ya están en main). Entre `8e41f72f` y `6a2cd6c7` mesa fusionó, sin recibo previo, catorce PR de Astra: `astra4-catalogo-1` (#1071), `astra4-region-1` (#1072), `astra4-relevo-1` (#1073, #1091), `astra4-relevo-sucesor-1` (#1092), `astra4-anexo-informe-1` (#1075), `astra4-familias-prospectivas-1` (#1076), `astra4-escritor-consumo-1`, `astra5-trabajo-enoe-1` (#1087), `astra5-genero-endireh-1` (#1093), `astra5-tecnologia-1` (#1085), `astra5-enut2024-docs-1` (#1090), `astra5-enif-diseno-1`, `astra5-documentos-dirigidos-1`. Auditarlos con los seis criterios del recibo (cifras sin RESULT · adendas · etiquetas y sellos · perímetro · México §3 · recomendación) y dejar, por PR, un veredicto: LIMPIO · CON-NC · **REVERTIR** (con FP para mesa y el sha exacto a revertir). E.2: lo fusionado ya está adoptado por merge; una reversión también es merge de mesa.
«Hecho»: nota con catorce filas de veredicto · script `tools/recibo/cifras_sin_result.py` corrido sobre cada PR (`git diff <base>...<merge>`), con conteo total y sin cita = 0 o listado · NC por defecto que Astra no abrió · FP `REVERTIR` solo con evidencia: una cifra sin RESULT en canon/, un derivado protegido escrito a mano, una ola reservada leída, `milpa/tramite.yaml` editado a mano · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA
Las adopciones que Astra pidió por FP (`…U4-TECNOLOGIA-1f30-01/02`, `…U1-TRABAJO-ENOE-e422-01`) **no** son de este acto: se auditan las corridas, no se adopta. Decisión de proceso que mesa da al lanzar (o queda como FP): ¿los PR `codex/*` siguen entrando sin recibo? Recomendación de dirección: **no** — se excluyen del auto-merge y del botón hasta recibo; hoy se audita post hoc una sola vez.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `git log --first-parent 8e41f72f..6a2cd6c7` → los merges listados; `ls forense/notas | grep -i recibo` → solo `RECIBO-ASTRA-1` (#1033). `celdas_validadas` 219 tras #1078 (CONTADORES): las celdas-D nuevas de Astra (región, ENOE, ENDIREH, tecnología) ya cuentan, con o sin recibo — razón de más para auditar hoy.
- `[LEÍDO]` FP de Astra: ENDUTIH 2023–2025 «1 551 celdas utilizables… sin uso predictivo»; MOCIBA 2015–2017 «279 celdas, incluida 2015 no estimable»; ENOE «pisos y dictamen de límites». Son adopciones **descriptivas retrospectivas**: el auditor verifica que cada RESULT lo rotule así y que ninguna ola reservada (ENOE último trimestre) se haya leído.
- `[SUPUESTO]` que ninguno de los catorce tocó `milpa/tramite.yaml`, marcador o celdas-D ajenas a su unidad: **es lo primero que verificas** (`git diff --stat` por PR).
- ADJUNTOS: ninguno (la plantilla RECIBO-ASTRA-PRODUCTO-N está archivada; se cita, no se adjunta).

## 4 · YA HECHO / YA DECIDIDO
`ls forense/encargos | grep -c 'AUDITORIA-POST-HOC-ASTRA'` → 0. `revisa-post-hoc-1036` (#1051) es el precedente de forma (un PR auditado tras fusión).

## 5 · PIEZAS
- **P1 · Script y tabla.** `cifras_sin_result.py`: por PR, extrae números de `.md`/`.tsv`/`.yaml` añadidos bajo `canon/` y `forense/analisis/` y busca cita `RESULT-*`; imprime conteo. Tabla PR × criterio × veredicto.
- **P2 · Perímetro y olas** por PR (`git diff --stat`; inputs de cada `ejecucion.json` contra `data/manifiesto.yaml` por id; `estado_reserva`).
- **P3 · Adendas y §3**: catálogo con «Benchmark del Mexicano», tabla de cobertura de 31 dominios, corroboración externa en el anexo; muestra de 10 afirmaciones sobre México por PR de texto (semilla declarada).
- **P4 · Veredictos, NC y FP.** REVERTIR solo con la evidencia de §1; la FP trae `git revert -m 1 <merge>` como texto de firma. Cerrar con la recomendación de proceso (§2).

## 6 · LATITUD
Orden libre; puedes agrupar PR de la misma unidad. Pregunta a mesa (sigues): si un PR mezcla una pieza limpia con una que debe revertirse (recomendación: revertir el merge completo y que Astra reabra la parte limpia).

## 7 · PAROS — lista cerrada
a) abrir dato reservado · b) editar main, un sello o la rama de Astra (auditar es leer) · c) adoptar, o poner `cuenta_gen2` · d) no aplica · e) CAJA · f) los catorce ya tienen recibo en origin/main.

## 8 · COMPUERTAS
«Este acto no revierte: propone por FP con el sha» protege: **borrar/reescribir** (una reversión es merge de mesa). «REVERTIR solo con evidencia de §1» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: nota, `tools/recibo/cifras_sin_result.py` + test, `firmas-pendientes.tsv`/`no-corrido.tsv`/`hallazgos.md` (append), L0, cascada. Ajeno: todo lo demás. En vuelo: `codex/astra5-mapa-dominios-1` (67 commits), `astra5-politica-1` (#1084, con recibo propio), `astra5-envipe2025-diseno-1`.

## 10 · LO QUE NO HACE · SUCESORES
No adopta las FP de Astra (eso es FIRMAS-14), no revierte. Sucesores: acto de reversión si mesa firma; RECIBO-ASTRA-PRODUCTO-N para lo que siga abierto.

## NO-CORRIDO / RESERVAS
- **P2 · Cascada de cierre de PR #1093 (astra5-genero-endireh-1).** FUERA-DE-PERÍMETRO — el propio recibo de Codex de esta unidad declara «PR #1093 permanece borrador hasta [completar]… ADR raíz»; mesa lo fusionó a `main` sin ese cierre. Verificado: `canon/gobernanza-v1_15.md` sin entrada `ADR-…-ASTRA5-U2…`, `canon/L0` sin fragmento, `canon/registro-rotulos.tsv` sin fila. Auditar es leer (PARO b): este acto no lo completa. Impacto: nueve CALC/RESULT ENDIREH ya sellados en `forense/replay-evidencia.tsv` no están indexados en la gobernanza. Sucesor: acto de cierre de ASTRA5-U2-GENERO-ENDIREH (Astra/Codex, continuación que su propio recibo declara pendiente). Fila: `NC-260923-GEN2-AUDITORIA-POST-HOC-ASTRA-1-39d2-01`.
- **P3 · Tabla de cobertura de 31 dominios.** FUERA-DE-PERÍMETRO — es el entregable declarado de `astra5-mapa-dominios-1` (PR #1079, en vuelo, ya listado en §9 como «en vuelo»). Impacto: P3 de la nota no trae esa tabla; no cambia ningún veredicto de P1/P2/P4. Sucesor: `astra5-mapa-dominios-1` (PR #1079). Fila: `NC-260923-GEN2-AUDITORIA-POST-HOC-ASTRA-1-39d2-02`.
- **P3 · Anexo de corroboración externa.** DIFERIDO-A — verificar contra fuentes fuera del repo las cifras citadas por los PR de texto (AMAI, ENDIREH, ENDUTIH, eje regional) habría más que duplicado este acto sin cambiar el veredicto de P1/P2/P4. Impacto: la muestra de diez afirmaciones de P3 se verificó contra §3, no contra fuentes externas independientes. Sucesor: `GEN2-AUDITORIA-POST-HOC-ASTRA-CORROBORACION-1` (acto no lanzado). Fila: `NC-260923-GEN2-AUDITORIA-POST-HOC-ASTRA-1-39d2-03`.
