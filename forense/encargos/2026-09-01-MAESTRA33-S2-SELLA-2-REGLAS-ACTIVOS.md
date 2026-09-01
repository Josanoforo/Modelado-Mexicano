ENCARGO · MAESTRA33-S2 · SELLA-2-REGLAS-ACTIVOS v1.1 — invoca /acto

## ENCARGO VERBATIM (redactado en tres mensajes, 1/sep/2026, sin editar)

### Mensaje 1 (redacción original)

ENCARGO · MAESTRA33-S2 · SELLA-2-REGLAS-OLA6 — invoca /acto
SHA de redacción: b827824 (merge PR #442). ENTORNO: NUBE. COMPUERTA: al menos un PR REGLAS-OLA6-ACTIVOS-L<n> (MAESTRA33) fusionado Y el corchete con texto; si falta cualquiera, cero commits. MODELO SUGERIDO: Sonnet (propagación mecánica, precedente E20-P0).
FIRMAS DE MESA (verbatim): «[sello por lote — o devolución con razón]».
A.8 (dirección contra b827824): milpa/tramite.yaml = 8 reglas; carga de reglas por sello: precedente ACTO MAESTRA32-E20-P0 (descongelamiento acotado + smoke emitir_binaria == p); INFRAESTRUCTURA D4 gobierna (cita la línea al arrancar).
P1 · Carga verbatim al motor cada regla sellada, con descongelamiento acotado a esas ids; smoke por regla; entrada de propuesta marcada SELLADA (no se borra). Devueltas → cabecera DEVUELTA-POR-MESA con la razón verbatim.
P2 · Cierra FP-219 citando PR #442 (la corrida L fusionada) y abre la fila MARCO-M-v1_2 con vence: 2026-09-04.
PERÍMETRO: milpa/tramite.yaml, milpa/tramite-ola5-propuesta-v0.yaml (estado), tablero, notas, A.3, cascada. Frase exacta vigente. FP/ADR: deriva. CONTADOR: reglas del motor 8→N, declarado.
LO QUE NO HACE: no mide; no edita valores; no toca el marco.

### Mensaje 2 (corrección de nombre + compuerta v1.1)

Corrección de dirección (MAESTRA33): en P3 los lotes se nombran REGLAS-ACTIVOS-L1/L2/L3 (no REGLAS-OLA6-ACTIVOS): son reglas nuevas dentro de los 4 dominios ya ACTIVOS, no apertura de dominio (eso lo evaluó E14 y es otra cosa). Añade esa aclaración en la cabecera de cada lote.  ENCARGO · MAESTRA33-S2 · SELLA-2-REGLAS-ACTIVOS v1.1 — invoca /acto
COMPUERTA: al menos un PR REGLAS-ACTIVOS-L<n> (MAESTRA33) fusionado Y firma de mesa escrita fuera de corchetes «[ ]» (un corchete con placeholder es VACÍO); si falta cualquiera, cero commits.
ACLARACIÓN: "ACTIVOS" = reglas nuevas dentro de los 4 dominios ya activos (trámite, cívico, dinero, familia). No es apertura de Ola 6; E14/ADR-265 sigue vigente.
P2 · Cierra FP-179 (cinco entradas resueltas) y registra C8-b: AP7_1 re-etiquetar sí, P4_10 no reabrir (firmas de mesa del 1/sep). FP-219 ya la cierra E13.

### Mensaje 3 (alcance exacto de ejecución + compuerta final)

Confirmado, procede — con este alcance exacto:
1. 0-bis A.3: archiva el encargo v1.1 y añade en su cabecera esta corrección de dirección: la compuerta (a) decía "PR REGLAS-ACTIVOS-L<n> fusionado" y debió decir "PR de EJECUCIÓN de un lote REGLAS-ACTIVOS-L<n> (con p medida) fusionado". Lo fusionado hoy es el lote redactado por E18, no ejecutado: la compuerta se cumplió por letra, no por sustancia, y así queda registrado.
2. P1: SIN INSUMO, declarado. Cero reglas SELLADA que cargar; no toques milpa/tramite.yaml ni la propuesta. Escribe en la nota que S2 se relanza cuando exista un PR de ejecución del lote y firma de mesa por regla.
3. P2 completo: cierra FP-179 (cinco entradas resueltas, con las citas que ya derivaste) y registra C8-b — AP7_1 re-etiquetar sí, P4_10 no reabrir — con la firma de mesa del 1/sep verbatim. FP-219 ya la cerró E13: no la toques.
4. Cascada normal, ADR con el alcance real ("propagación; sello sin insumo"), CONTADOR cero declarado. Abre el PR. & COMPUERTA: PR de EJECUCIÓN de al menos un lote REGLAS-ACTIVOS-L<n> (o de MIDE-PAGA-MORDIDA), MAESTRA33, fusionado en origin/main — es decir, con entradas MEDIDO·p en milpa/tramite-ola5-propuesta-v0.yaml que citen ese PR — Y firma de mesa por regla escrita fuera de corchetes «[ ]». Un lote solo redactado NO cumple.

## CORRECCIÓN DE DIRECCIÓN — añadida por este mismo acto, A.3 no edita el verbatim de arriba

La compuerta del Mensaje 2, leída por letra ("al menos un PR REGLAS-ACTIVOS-L<n> (MAESTRA33) fusionado"), se dio por cumplida contra `PR #443` (`ACTO MAESTRA33-E18 · MAPEA-DENTRO-DE-ACTIVOS`), que fusiona el lote **redactado** `forense/encargos/2026-09-01-MAESTRA33-E18-P3-REGLAS-OLA6-ACTIVOS-L1.md` (spec `LISTO-CAJA`, ninguna `p` medida, las 3 reglas candidatas en `PENDIENTE-VERIFICACIÓN-EN-ACTO-SUCESOR`/`PENDIENTE-DE-MESA`). Dirección corrige (Mensaje 3, 1/sep/2026): la compuerta debió pedir un **PR de EJECUCIÓN** de ese lote (con `p` medida, entradas `MEDIDO·p` en `milpa/tramite-ola5-propuesta-v0.yaml` citando ese PR), no la mera redacción del lote. **La compuerta se cumplió por letra, no por sustancia** — se registra así, y la compuerta vigente hacia adelante (formalizada al cierre del Mensaje 3) exige la ejecución, no la redacción. Este acto (`S2`) procede con el alcance reducido que dirección fija: `P1` sin insumo (declarado, cero reglas `SELLADA` para cargar), `P2` con el trabajo de tablero que sí es independiente de esa sustancia (`FP-179`, `C8-b`).

## LO QUE NO HACE

No abre ningún dominio de Ola 6 (`E14`/`ADR-265` sigue vigente, sin tocar). No mide ninguna `p`. No edita `milpa/tramite.yaml` ni `milpa/tramite-ola5-propuesta-v0.yaml`. No toca `FP-219` (ya cerrada por `E13`).
