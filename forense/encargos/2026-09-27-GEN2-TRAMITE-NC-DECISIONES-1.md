# ENCARGO · ACTO GEN2-TRAMITE-NC-DECISIONES-1 · Setenta y dos NC dicen «decisión de mesa pendiente» y ninguna tiene fila en el tablero de firmas; veinte no tienen sucesor: se barren una vez por objeto — superada con cita, convertida en fila FP con texto de firma, o asignada — y sale una hoja única para mesa

> ENTORNO: **NUBE**. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `11602de8` (re-deriva al abrir) · una sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus (lee 92 NC por objeto) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0 `3fbc487684b77b7f`) · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
CONTADOR: cero mediciones; no adopta; mueve `no_corrido_abiertas` hacia abajo solo por cierres verificados por objeto; sube `firmas-pendientes` ABIERTA por cada decisión real que hoy no tiene fila (A.12).

## 1 · OBJETIVO
(P1) **Las 72 NC con razón `DECISIÓN-DE-MESA-PENDIENTE` (dos grafías)**, ABIERTAS a `11602de8`: por cada una, leer el objeto que cita (CALC, regla, momento, FP, ADR) y dictaminar una de tres: **SUPERADA** — una firma posterior ya la resolvió (FIRMAS-11 a -20, ADOPCION-1..4, RELEVO-3, CATALOGO-1, etc.): cerrar con `DECISIÓN-DADA: <fila>` y cita; **REQUIERE-FIRMA** — sigue viva: abrir fila FP con texto de firma propuesto (recomendación con razón, opción alternativa) y `EJECUTA:`; **SIN-OBJETO** — el objeto ya no existe o la pregunta perdió sentido (p. ej. una lectura legacy que ya se relevó): cerrar con la evidencia. Empezar por las 18 de RELEVO-MOTOR-34-1 (`a157-*`), que son el bloque mayor y en parte las cubrió FIRMAS-16 B1/B2. (P2) **Las 20 NC sin sucesor** (`SIN-ASIGNAR` o vacío): asignar por objeto al acto vigente que lo cubre (RELEVO-CONSUMIDORES-3, CI-TIEMPO-2, CORPUS-RESPALDO, AUTOMERGE, ENDIREH-CIERRE…), o cerrar si ya se hizo (p. ej. `9641-01/02` del parser de FP: verificar si TUBERIA-PARSER-FP los resolvió). (P3) **Dos deudas de corpus sin dueño** con recomendación: el microdato real de ENAPROCE (`e7be-02`) → cola de adquisición v1.1 con receta; las **588 entradas del manifiesto sin licencia** (`e7be-04`) → acto propio `GEN2-CORPUS-LICENCIAS-1` (nube: licencia por payload desde el portal de origen, INEGI = Términos de Libre Uso; registro en manifiesto; es requisito de «ir más público»). (P4) **Hoja única** `forense/analisis/nc-decisiones/hoja-2026-09-27.md`: solo las REQUIERE-FIRMA, en el formato de RH que mesa usa (situación · qué te pide · opciones · recomendación · plazo), letra por decisión; el trámite siguiente (FIRMAS-21) la asienta.
«Hecho»: 0 NC ABIERTAS con razón «decisión de mesa pendiente» **sin** fila FP asociada (cada una: cerrada con cita, o con `FP:` en su campo de sucesor) · 0 NC ABIERTAS sin sucesor · hoja con N decisiones vivas, cada una con texto de firma · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
A.12 (todo pendiente de mesa tiene fila en `firmas-pendientes.tsv`), A.17 (re-verificar estado antes de heredar), A.14 (razones de la lista cerrada), FIRMAS-11..20 (las firmas que superan NC viejas: se citan por id), cláusula v1.0 (dictaminar y redactar rotulado). **Mesa, 26/sep:** «¿qué podríamos revisar? Pendientes» — este barrido es la respuesta.

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` (`11602de8`) `no-corrido.tsv`: 476 ABIERTA; 64 `DECISIÓN-DE-MESA-PENDIENTE` + 8 `DECISION-DE-MESA-PENDIENTE` (misma razón, dos grafías: P1 unifica el token, A.16); por acto: RELEVO-MOTOR-34-1 18, FIRMAS-14 6, RELEVO-CONSUMIDORES-2 5, CORPUS-INTEGRIDAD 2, DIN-CREDITO-HISTORIA 2, ENUT-PISOS 2, ENIF-IC 2, PENDIENTES-CAJA 2, ADOPCION-2 2, C2-CIERRE-MATERIAL 2, CI-TIEMPO-1 2, FIRMAS-20 2, NC-0151, NC-0153…; 20 sin sucesor (lista en la salida de dirección, 12 primeras: L-DESDE-CAPTURAS `1d7c-03`, ADQ-F6 `e7be-02/04`, PARSER-FP `9641-01/02`, FIRMAS-10 `6980-02`, FIRMAS-9 `673c-02`, CORPUS-RESPALDO `a307-01`, AUTOMERGE-2 `1269-02`, ADOPCION-1 `ec71-03`, ENDIREH-CIERRE `b0df-01`, RELEVO-2 `e760-10`). `[SUPUESTO]` que la mayoría de las 18 de RELEVO-MOTOR-34 quedaron superadas por B1/B2/B3 (FIRMAS-16) y H1–H3 (FIRMAS-18): se verifica una por una.

## 4 · YA HECHO / YA DECIDIDO
`ls forense/encargos | grep -c NC-DECISIONES` → 0. `ls forense/analisis/nc-decisiones` → no existe.

## 5 · PIEZAS
P1 (por acto, del bloque mayor al menor) → P2 → P3 → P4.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 + AMPLITUD
1–7 verbatim. Orden y agrupación: tuyos. Una NC cuyo objeto no puedas localizar se cierra `SIN-OBJETO` con el comando que lo buscó (A.4: universo y conteo). Pregunta a mesa prevista: **ninguna** (las preguntas van a la hoja).

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) editar una fila FIRMADA, un sello, o el texto de una NC (solo `estado`, `sucesor`, `razon` normalizada) · c) adoptar; cerrar una NC sin cita · d) no aplica · e) CAJA.

## 8 · COMPUERTAS
«Cerrar solo con cita al objeto o a la firma que la resolvió» protege **borrar** (deuda). «Toda decisión viva termina en fila FP con texto» protege **adoptar** (A.12).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/no-corrido.tsv` (estado, sucesor, razón normalizada), `forense/firmas-pendientes.tsv` (append ABIERTA), `forense/analisis/nc-decisiones/`, nota, L0, cascada. Ajeno: todo lo demás. En vuelo: CI-TIEMPO-2, Astra (TSV de gobierno: union).

## 10 · LO QUE NO HACE · SUCESORES
No decide nada: prepara la hoja. Sucesores: FIRMAS-21 (asienta la hoja), `GEN2-CORPUS-LICENCIAS-1` (P3).

## NO-CORRIDO / RESERVAS

- **qué**: reparar la estructura de columnas de `NC-260923-GEN2-TRAMITE-FIRMAS-9-673c-02` (10 campos en vez de 12; `cerrado_por`/`fecha_cierre` ausentes, sin corrupción de `razón`/`sucesor`/`estado`). — **por qué**: `FUERA-DE-PERÍMETRO:GEN2-TRAMITE-PENDIENTES-2` (acto concurrente que declara explícitamente esta reparación como su propia P2 y pide que esta fila se deje intacta hasta después del merge de este PR). — **impacto**: el dictamen de contenido de esta fila (REQUIERE-FIRMA, letra B1 de la hoja) sí se produjo y sí tiene fila `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-03`; solo la reparación mecánica de columnas queda para el otro acto. — **sucesor**: `GEN2-TRAMITE-PENDIENTES-2`.
- **qué**: ejecutar la adquisición real de ENAPROCE 2015/2018 (NC e7be-02) — la fila de `data/cola-adquisicion-v1_0.tsv` con la receta ya existe; falta que mesa decida si designa titular. — **por qué**: `DECISIÓN-DE-MESA-PENDIENTE` (letra I1 de la hoja). — **impacto**: R03 sigue sin microdato real; F6 no gana la familia TRA por esta vía mientras tanto. — **sucesor**: `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-29`, y el acto que ejecute la solicitud si mesa la autoriza.
- **qué**: archivar y ejecutar el acto `GEN2-CORPUS-LICENCIAS-1` (NC e7be-04) — está fuera del perímetro §9 de este acto (`forense/encargos/` es ajeno) y, además, la premisa del encargo sobre su universo (588 sin licencia, receta única INEGI) está vencida: son 554 hoy y cero de INEGI. — **por qué**: `DECISIÓN-DE-MESA-PENDIENTE` (letra I2 de la hoja, con el universo corregido). — **impacto**: 554 entradas del manifiesto siguen sin licencia registrada; ningún bloqueo inmediato declarado. — **sucesor**: `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-30`, y `GEN2-CORPUS-LICENCIAS-1` una vez que mesa firme el alcance.
- **qué**: correr `tests/check.py --baseline` completo (criterio 4 de «Hecho», literal). — **por qué**: `NO-VERIFICABLE-AQUÍ` — la corrida completa excede los minutos razonables de una sesión interactiva (tope de 580s agotado sin salida; los tiempos declarados de T32-quater/T32/T45/T35 solos ya suman >8 min) y el propio `/acto` (§5, paso 6) fija que la sesión corre `--rapido` (VERDE, 0 FAIL · 590 WARN, confirmado dos veces: antes y después del merge de `origin/main`) y que la suite completa la juzga el CI en el push. — **impacto**: ninguno declarado; ningún FAIL nuevo visto en `--rapido`. — **sucesor**: el CI de este PR.

## CONSUMIDO

PR #1213.
