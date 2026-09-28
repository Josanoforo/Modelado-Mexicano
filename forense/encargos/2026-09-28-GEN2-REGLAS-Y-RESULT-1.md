# ENCARGO · ACTO GEN2-REGLAS-Y-RESULT-1 · Todas las reglas SI [segmento] ENTONCES [conducta] — PORQUE [driver] — [TIER] que el programa tiene propuestas —las que Codex dejó en `forense/analisis/reports-v2/reglas-propuestas-v1_0.tsv`, las de los 31 reports v1 y las del integrador— se contrastan una por una contra los RESULT GEN2 sellados: qué RESULT la CONFIRMA, MATIZA o ROMPE con punto e IC en la unidad correcta, qué reglas no tienen cifra y qué instrumento del corpus la daría (mapa), y qué tier declarado no aguanta la evidencia. Sale el primer bloque candidato de adopción de reglas para mesa: ninguna se adopta aquí

> ENTORNO: **NUBE** — lee reports, tablas de reglas, RESULT sellados (`data/corrida0/`), catálogo v1.3, mapa de instrumentos alternos; escribe una tabla y una hoja. Cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `723b62c1` (re-deriva al abrir) · una sesión, rama propia; PR por dominio o por lote de reglas · MODELO: **Opus** (contrastar una regla con un RESULT en la unidad correcta es juicio) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0) · ids con raíz de acto · D-21 aplica.
CONTADOR: **cero mediciones; no adopta**. Ninguna cifra nueva; ninguna regla cambia de estado en el catálogo o el motor: se produce el bloque candidato.

## 1 · OBJETIVO
(P1) **Universo de reglas por objeto.** `reglas-propuestas-v1_0.tsv` (Codex, C3-1), las reglas SI-ENTONCES de `corpus/reports/` (v1) y de `corpus/reports-v2/`, el integrador y `milpa/tramite.yaml` / `catalogo-momentos` donde una regla ya vive como consumidor. Una fila por regla con id estable (llave por texto normalizado), report de origen, segmento, conducta, driver, tier declarado, disparadores, y el momento/consumidor del motor que la usa si lo hay. Duplicados y variantes se funden citando ambas fuentes.
(P2) **Contraste con RESULT sellados.** Para cada regla: los RESULT GEN2 que hablan de esa conducta en ese segmento (buscar por llave lógica, consumidor y texto de estimando; catálogo v1.3 como índice), y dictamen cerrado en la unidad de la regla: `CONFIRMA (RESULT, punto, IC)` · `MATIZA (qué segmento o magnitud cambia)` · `ROMPE (RESULT contrario con IC que lo despeja)` · `SIN-CIFRA-GEN2 (instrumento y reactivo que la daría, del mapa; o NO-CONSTRUIBLE con texto y secciones)` · `INCOMPARABLE (unidad o escala distinta: qué enlace faltaría)`. Un RESULT en unidad delito no contrasta una regla de persona (§4); una regla con SI condicional se contrasta contra el cruce, no contra el marginal, y si solo hay marginal es MATIZA-SIN-CRUCE. Todo RETROSPECTIVO: ninguna regla se «valida» prospectivamente aquí.
(P3) **Tier y procedencia.** Tier declarado vs evidenciado (fuerte / media / hipótesis razonable / narrativa popular), procedencia (a)/(b)/(c) de la evidencia que la sostiene; las reglas cuya única base es (b) o (c) se marcan y no entran al bloque; firewall genético y §3 (¿incentivo o psicología? ¿clase media urbana?) como columnas.
(P4) **Bloque candidato y hoja.** `canon/reglas-contrastadas-v1_0.tsv` (una fila por regla con todo lo anterior) y `forense/analisis/reglas-y-result-1/bloque-candidato-adopcion-1.md`: las reglas CONFIRMA con tier evidenciado ≥ media, en formato de adopción por bloque (E.2: el merge del PR que traiga el bloque será la adopción, si mesa lo decide), con lo que cada una implica para el motor (`tramite.yaml`) y el catálogo; más la hoja RH para mesa con opciones (adoptar el bloque · adoptar por dominio · esperar cruces) y el conteo por dictamen. Las ROMPE van con la corrección propuesta al report (PROPUESTA, no editada aquí).

«Hecho», por comando sobre el commit final con `origin/main` fusionado: toda regla de `reglas-propuestas-v1_0.tsv` y toda regla SI-ENTONCES detectable en los reports (patrón declarado, conteo en la nota) tiene fila en `reglas-contrastadas-v1_0.tsv` (ids sin fila: 0) · ninguna fila con dictamen vacío · toda `CONFIRMA`/`ROMPE` cita `resultado_id` existente en `data/corrida0/` (0 ausentes) y su `sello.json` · bloque candidato presente con conteo · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
§5 (reglas SI-ENTONCES con tier y disparadores; una regla sin RESULT sellado queda PROPUESTA) · §3 y §4 (unidad, procedencia, firewall) · E.2 (adopción por merge y por bloque) · MISION-ASTRA-6 C3 (reports v2; reglas propuestas, no adoptadas) · mesa 28/sep: «capitalicemos todo lo posible». **No decide**: adopción (bloque para mesa), edición de reports (propuestas).

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `723b62c1` · `forense/analisis/reports-v2/reglas-propuestas-v1_0.tsv` existe (C3-1, #1261); `corpus/reports-v2/INDICE.md` regenerado con 31 filas; `canon/catalogo-del-mexicano-v1_3.tsv` (7 suspendidas, 689 acotadas); `canon/mapa-instrumentos-alternos-v1_0.tsv` (64 pares, 17 incógnitas); adoptados 138.
- [LEÍDO] Transfer de Astra §4: #1243 «nueve reglas propuestas, no adoptadas»; #1247 «105 tesis», 22 ROMPE; #1246 55 dictámenes; #1251 78. C3-1 los recibió y consolidó en la tabla: **parte de ahí**, no de los bodies.
- [EXISTE] `corpus/reports/` (v1, 31), integrador, `milpa/tramite.yaml`, `milpa/catalogo-momentos-v0_1.tsv` (23 momentos con `computo_pretendido` y reglas R1.4…R10.3 citadas).
- [SUPUESTO] Que las reglas de los reports v1 siguen el formato SI/ENTONCES/PORQUE/TIER de §5; si un report las trae en prosa, el patrón de detección lo declara y el conteo de «no detectadas por patrón» va a la nota.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'REGLAS-Y-RESULT\|REGLAS-CONTRASTADAS\|ADOPCION-REGLAS'` → 0. Consumidos y citados: ASTRA-CONTINUIDAD-C3-1 (tabla de reglas, índice), CIERRE-SEMANAL-2 (catálogo v1.3), MAPA-INSTRUMENTOS-ALTERNOS-1, los reports v2 de Astra (no se reescriben). Homónimo: `GEN2-ADOPCION-BLOQUE-Y-PINES-1` (24/sep) adoptó cifras por bloque, no reglas: cítalo como modelo del formato de bloque. En vuelo: DEMANDA-DICTAMEN-1 y RELEVO-TRAMITE-CAJA-1 (si un RESULT nuevo entra a main durante el acto, se incorpora y se dice), TUBERIA-Y-CURACION-1.

## 5 · PIEZAS
P1 → P2 → P3 → P4; P2 por dominio. Rama prevista: report con reglas en prosa → patrón declarado + revisión manual contada; RESULT con `sello.json` pero sin fila en la vista → se cita como «sellado en disco, no registrado» y se abre NC para el canal, no se descarta.

## 6 · LATITUD
Orden por dominio, agrupación en PR, columnas adicionales: tuyos. Puedes proponer reglas nuevas que un RESULT sostenga y nadie escribió, rotuladas PROPUESTO-POR-EJECUTOR y fuera del bloque. PREGUNTA A MESA: ninguna fuera de la hoja. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato · b) editar un report, el catálogo, `tramite.yaml`, un sello · c) adoptar; marcar CONFIRMA sin RESULT citado; promover un tier sin evidencia (a) · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«CONFIRMA/ROMPE solo con RESULT sellado citado, punto e IC, misma unidad» protege **adoptar** · «El bloque lo adopta mesa por merge; aquí es candidato» protege **adoptar** · «Reports y motor no se editan» protege **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `canon/reglas-contrastadas-v1_0.tsv`, `forense/analisis/reglas-y-result-1/` (bloque, hoja, tablas por dominio), TSV de gobierno (append), nota, L0, cascada. Ajeno: `corpus/reports*`, `milpa/`, `canon/catalogo-*`, sellos, `data/corrida0/` (lectura). «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No adopta, no mide, no edita reports ni motor, no valida prospectivamente. Sucesores: `GEN2-ADOPCION-REGLAS-BLOQUE-1` (mesa, por merge, con la hoja), reports v3 con las correcciones ROMPE, CALC de caja para las SIN-CIFRA con instrumento identificado. Módulo de auditoría v2.16 **sí** (la tabla afirma qué reglas sobre México tienen evidencia): procedencia por regla; unidad por cifra; ¿incentivo o psicología?; ¿clase media urbana?; PROSPECTIVA/RETROSPECTIVA (todo RETROSPECTIVO aquí). El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-REGLAS-Y-RESULT-1-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS
- **qué:** P2 «CALC de caja para las SIN-CIFRA con instrumento identificado» (7 reglas) · **por qué:** FUERA-DE-PERÍMETRO: acto de caja sucesor (cero microdato en NUBE) · **impacto:** el bloque candidato no crece · **sucesor:** CALC de caja (§10) · NC-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01.
- **qué:** P2 «una regla con SI condicional se contrasta contra el cruce» (6 MATIZA-SIN-CRUCE) · **por qué:** DIFERIDO-A:GEN2-ADOPCION-REGLAS-BLOQUE-1 · **impacto:** 6 reglas fuera del bloque · **sucesor:** GEN2-ADOPCION-REGLAS-BLOQUE-1 · NC-…-a3cc-02.
- **qué:** P4 «las reglas CONFIRMA … en formato de adopción por bloque» · **por qué:** DECISIÓN-DE-MESA-PENDIENTE: criterio de CONFIRMA (conducta vs regla completa) · **impacto:** bloque = 1 regla o 0 · **sucesor:** GEN2-ADOPCION-REGLAS-BLOQUE-1 · NC-…-a3cc-03.

## CONSUMIDO
PR #1272 (https://github.com/Josanoforo/Modelado-Mexicano/pull/1272) · ADR-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01.
