# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-8 · Tres firmas del 22/sep con fila: lote estricto del canal, auto-merge de rutinas, R02/R08 fuera del panel F6 — y lo que cada una cierra

> ENTORNO: **NUBE**. Hook; si no coincide, PARA.

CABECERA · SHA `c9b67bf8` (22/sep/2026 19:02 −06:00; re-deriva al abrir: hay tres PR en cola de merge — #1014, el de MARCADOR-CONSUMO-2 y el del duelo) · una sola sesión (D-17) · MODELO: Sonnet (propagación con textos dados) · MODO: **ABIERTO** · CONTADOR: cero mediciones; FP `ABIERTA` 3 → 1 (queda la del respaldo del corpus, física) · ids raíz de acto.

## 1 · OBJETIVO
Que las tres firmas que mesa dio en conversación de dirección el 22/sep queden con fila en `decisiones.tsv`, sus FP FIRMADAS con cita, y las NC que cada una gatea con sucesor nombrado o cerradas. «Hecho» = `decisiones.tsv` con una fila por firma de §2 (objeto = id de la FP); `digesto --mesa` sin 7d98-01, e889-01 ni e7be-01 en ABIERTA; NC 7d98-02 con `sucesor = GEN2-TUBERIA-LOTE-ESTRICTO-1`; NC de ADQ-F6 sobre R02/R08 cerradas con cita; NC 8e53-04 CERRADA si mesa rellenó las tres líneas, ABIERTA con la pregunta si no.

## 2 · FIRMAS DE MESA — verbatim (conversación de dirección, 22/sep/2026, «Firmado»); mesa corrige aquí lo que no sea exacto
- **FP-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01:** «Opción (a): lote ESTRICTO en `corrida0.py registro` (≤ 30 líneas, con test): la escritura del canal se restringe a las filas del lote derivado de `lote_desde_asientos.py`. Las 13 corridas con drift no se re-proyectan por el canal: las asienta `GEN2-REPLAY-ASIENTOS-2` con evidencia fresca.»
- **FP-260923-GEN2-TUBERIA-RUTINAS-AUTOMERGE-1-e889-01:** «Se instrumenta el auto-merge de CI para los cuatro PR diarios de rutina bajo las cuatro condiciones de §1; cualquier PR que no sea rutina, o una rutina que toque fuera de su clase, sigue exigiendo mi merge.» **8e53-04 (mesa rellena o deja en blanco):** «protección de `main`: ___ · merge queue: ___ · quién fusiona: ___.»
- **FP-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-01:** «Opción (a): R02-WBES y R08-ENCRIGE quedan fuera del panel F6 por unidad (establecimiento no es panel de M); R08 además no es público en microdato. Ninguna de las dos se adquiere.»

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` FP abiertas en main al `c9b67bf8`: las tres de arriba + `…CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01` (física; no va aquí). `[EJECUTADO]` NC `…CANAL-PUBLICACION-1-7d98-02`: «bandera de lote estricto … no se añadió · DECISIÓN-DE-MESA-PENDIENTE»; `-7d98-01`: «primer push real que registre el backlog (22 CALC selladas sin fila)»; `-7d98-04`: «cierre de las cuatro NC DIFERIDO-A: acto TUBERIA (#1008/#1012/#1005/#1003)» — las cuatro siguen ABIERTAS porque sus filas no están publicadas aún. `[EJECUTADO]` `grep -c estricto tools/corrida0.py` → 7, **todos** de `_asigna_ids(estricto=…)` (otro objeto: ids), ninguno de `registro --lote`.
- `[EJECUTADO]` FP e7be-01 (rama `ceszds`, PR #1014 sin fusionar al redactar): si al abrir #1014 ya fusionó, la FP está en main y se marca; si no, tipo (3): se cita el PR y la fila de `decisiones.tsv` se escribe igual (la firma es de mesa, no del PR).
- `[SUPUESTO]` Mesa rellenó las tres líneas de 8e53-04 al firmar T2. Si el lanzamiento las trae en blanco, 8e53-04 queda ABIERTA con la pregunta y el automerge se relanza igual (su job puede instalarse apagado hasta tener permiso).
- ADJUNTOS: ninguno (las firmas van en §2; el sello del cuerpo las cubre).

## 4 · YA HECHO / YA DECIDIDO
Por id de FP en `decisiones.tsv` antes de asentar (`grep -c 7d98-01|e889-01|e7be-01` → 0 al redactar). Ramas vivas: duelo (caja), MARCADOR-CONSUMO-2 (cerrado), `ceszds` (#1014) — sin archivo común salvo el tablero al cierre (union + guarda).

## 5 · PIEZAS
- **P1** una fila por firma en `decisiones.tsv`; FP → FIRMADA con cita a este acto.
- **P2 · Lo que cada firma gatea.** 7d98-01 → NC 7d98-02: `sucesor = GEN2-TUBERIA-LOTE-ESTRICTO-1` (enmienda fechada; sigue ABIERTA hasta que ese acto fusione); NC 7d98-01/-04 y las cuatro `DIFERIDO-A: acto TUBERIA` (#1008/#1012/#1005/#1003): enmienda fechada «cierran con el primer push real tras el lote estricto» — no se cierran aquí. e889-01 → NC 8e53-04 según §3; nota para mesa: «relanzar `GEN2-TUBERIA-RUTINAS-AUTOMERGE-1` con la firma pegada». e7be-01 → las NC de ADQ-F6 sobre R02/R08 CERRADAS con cita; NC-0161/0162 enmienda fechada (panel F6 sin R02/R08; lo conseguido y lo pendiente según la nota de #1014).
- **P3** nota con la tabla firma · fila · qué desbloquea · qué sigue abierto y por qué.

## 6 · LATITUD
DECIDES TÚ: orden, formato. PREGUNTAS A MESA: ninguna prevista. NO DECIDES: §7.

## 7 · PAROS
a) no aplica · b) editar una firma ya sellada o el cuerpo de una NC · c) adoptar · d) no aplica · e) caja · f) inalcanzable.

## 8 · COMPUERTAS
Ninguna. Orden sugerido: lanzar cuando #1014 fusione (cita en vez de duplicar); no es compuerta.

## 9 · PERÍMETRO
Propio: `data/corrida0/decisiones.tsv` · `forense/firmas-pendientes.tsv` · `forense/no-corrido.tsv` (estado/sucesor/enmiendas de las filas nombradas) · nota · `canon/L0/<raíz>.md`. Ajeno: `tools/corrida0.py` (lo toca `GEN2-TUBERIA-LOTE-ESTRICTO-1`), `verify.yml`, CALC, vistas. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No implementa la bandera, no relanza el automerge (lo hace mesa), no adquiere nada. Sucesores: `GEN2-TUBERIA-LOTE-ESTRICTO-1`; relanzamiento de `GEN2-TUBERIA-RUTINAS-AUTOMERGE-1`. Auditoría: no aplica. Cierre por /acto.
