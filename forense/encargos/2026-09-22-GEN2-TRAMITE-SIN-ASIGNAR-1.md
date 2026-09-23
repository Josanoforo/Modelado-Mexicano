# ENCARGO · ACTO GEN2-TRAMITE-SIN-ASIGNAR-1 · Las 43 filas de deuda sin dueño reciben dueño por regla: conversación, acto o mesa — y las que ya cerró otro acto, cita

> ENTORNO: **NUBE**. Hook; si no coincide, PARA.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Sonnet (ruteo por regla; sube a Opus si una fila exige leer un CALC) · MODO: **ABIERTO** · CONTADOR: cero mediciones; `sucesor = SIN-ASIGNAR` 43 → 0 (reportado) · ids raíz de acto.

## 1 · OBJETIVO
Que ninguna NC abierta tenga `sucesor = SIN-ASIGNAR`: cada una recibe, por regla derivada del objeto que nombra, un sucesor con nombre — la conversación que puede correrlo (PRODUCTO-DINERO, TUBERÍA, NUBE-MEDICIÓN, dirección), un acto ya encargado (por id), o mesa (con la pregunta en una línea) — y las que cita un acto ya fusionado cierran con esa cita. «Hecho» = `awk -F'\t' '$estado ~ /ABIERTA/ && $sucesor ~ /SIN-ASIGNAR/' forense/no-corrido.tsv | wc -l` → 0; una tabla `NC · objeto · regla aplicada · sucesor`; dirección revisa el PR antes del merge.

## 2 · FIRMAS DE MESA
Ninguna nueva: asignar sucesor no decide; lo que resulte «mesa» va a la lista de mesa con su pregunta.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` 43 NC ABIERTA con `SIN-ASIGNAR` en `sucesor` al `3f48be30`; 91 con acto nombrado, 69 con mesa, 7 con dirección. Reglas de ruteo del plan de aceleración §1 (dinero → PRODUCTO-DINERO; CI/vistas/`corrida0` → TUBERÍA; adquisición/nube → NUBE-MEDICIÓN; gobierno/marcador/informe → dirección). `[LEÍDO]` PENDIENTES-RECONCILIA-1 §4: ya clasificó las 43 como VIGENTE sin asignarles dueño (no era su objeto).
- `[SUPUESTO]` El objeto de cada NC (archivo, CALC, regla) basta para rutearla sin leer el acto entero. Si una no se rutea por objeto, se lee su encargo y se declara.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
Por NC: `grep "<objeto>" forense/notas/*cierre*` — si un acto posterior ya hizo el objeto, CERRADA con cita, no asignada. Ramas vivas: TRAMITE-COLA-VIEJA-1 (nube) toca `no-corrido.tsv` — ids con raíz, sin conflicto de contenido; fusionar después.

## 5 · PIEZAS
- **P1 · Tabla de ruteo** con la regla aplicada por fila; **P2 · Enmiendas fechadas** en `sucesor` (nunca en el texto de la fila); cierres con cita donde aplique; **P3 · Lista de mesa** (las que resulten «mesa»), en RH, para dirección.

## 6 · LATITUD
DECIDES TÚ: orden, formato. PREGUNTAS A MESA: ninguna prevista (lo que sea de mesa va a la lista, no se pregunta aquí). NO DECIDES: §7.

## 7 · PAROS
a) no aplica · b) editar texto de una NC · c) no aplica · d) no aplica · e) caja · f) inalcanzable.

## 8 · COMPUERTAS
Ninguna.

## 9 · PERÍMETRO
Propio: `forense/no-corrido.tsv` (solo `sucesor` y `estado` con cita) · nota · `canon/L0/<raíz>.md`. Ajeno: todo lo demás. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No decide, no cierra sin cita, no lanza nada. Sucesor: el inventario de 004 lee los sucesores nuevos. Auditoría: no aplica. Cierre por /acto.

## NO-CORRIDO / RESERVAS

Ninguno.

## CONSUMIDO

Ejecutado por ACTO GEN2-TRAMITE-SIN-ASIGNAR-1, 23/sep/2026, `canon/gobernanza-v1_15.md` `ADR-260923-GEN2-TRAMITE-SIN-ASIGNAR-1-6eb3-01`. PR: pendiente de número real al abrirse (se cita al empujar). Verificación de «hecho»: `awk -F'\t' '$estado ~ /ABIERTA/ && $sucesor ~ /SIN-ASIGNAR/' forense/no-corrido.tsv | wc -l` → `0`. Tabla NC · objeto · regla aplicada · sucesor y lista de mesa: `forense/notas/nota-2026-09-23-gen2-tramite-sin-asignar-1.md`.
