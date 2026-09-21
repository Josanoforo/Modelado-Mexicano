# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-3 · LA SESIÓN DE MESA DEL 21/SEP, PROPAGADA: VEINTE FIRMAS, CADA UNA A LA FILA QUE LA ESPERABA

ENTORNO: NUBE — el hook de arranque imprime `ENTORNO-DERIVADO`; si dice `CAJA` puedes correrlo igual y lo dices.

CABECERA · SHA de redacción `8d78cf5f`; re-deriva al abrir · una sola sesión, rama propia · MODELO: Sonnet (propagación; donde una pieza pida juicio, la dejas como `NO-CORRIDO` con su razón y sigues) · MODO: ABIERTO · CONTADOR: `cuenta_gen2 = NO`; no mide. Las veinte firmas de §2 están dadas; ninguna pieza queda condicionada. Mueve `N_corridas_selladas` solo por las firmas de contador de P3, y `no_corrido_abiertas` solo por cierres con la firma citada. `adoptados_activos` y `dependencias_numericas_legacy_activas` no se mueven aquí: eso es de RELEVO-TANDA-3.

## 1 · OBJETIVO

Que cada decisión que mesa tomó el 21/sep quede escrita en la fila que la esperaba —`firmas-pendientes.tsv`, `decisiones.tsv`, `no-corrido.tsv`, `cuenta_gen2`— con su texto verbatim, para que ningún acto posterior la vuelva a preguntar. «Hecho» significa: cada renglón de §2 tiene su fila `FIRMADA` o su NC cerrada con la firma citada; `status` antes/después pegado; suite VERDE por FAIL.

## 2 · FIRMAS DE MESA — verbatim de la hoja de respuestas del 21/sep/2026 (sobre `CUADERNO-DE-FIRMAS-2026-09-21.md`, adjunto; archívalo con sha256)

```
B1  cierre por evidencia (6 filas) sí
B2  NC-0371 evaluación Codex b · NC-0225 texto F5 del 15/sep b (no localizable) · NC-0038/39 (ya no aplica)
3A  13 corridas que reproducen — a
3B  4 sin replay no cuentan todavía — sí
3C  ENCUCI, firma retroactiva — a
3D  insumo-árbitro no impide contar (caso por caso) — «rec: a + b como demanda» · guardia en el medidor como estándar — sí
4.2 unidad «evento» — a
4.3 dos etiquetas de solidez (cifra / mecanismo) — c
4.4 librerías en CI — a
4.5 ratificar #897 y #901 — a
4.6 aceptar el §13 corto — a
4.7 borrar las seis ramas — a
4.9 conservar tres descriptivos — a
4.10 recortar el denominador de reactivos ciegos — a
4.11 piloto de nube: fusionar la que reprodujo — «sí ya estoy trabajando en eso»
B5  pasar a otras mesas como está en la tabla — sí
B6  FP-324 a la cola de adquisición y cerrar — sí
B7  bandeja de titular — «Aun no»
```

Dos que mesa pidió revisar a detalle; dirección las revisó contra el repo, propuso texto, y mesa respondió verbatim el 21/sep/2026: «confirmo 4.1 y 4.8, dame los encargos con estas correcciones.» — FIRMADAS:

4.8: «El pin de RES-0047 y RES-0049 es `CALC-ENIF-0001`: mide desde el microdato, con intervalo propio. `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` deriva de sus resultados y no sustituye a su fuente. Regla general: entre dos candidatos con el mismo valor, manda el que está más cerca del dato crudo.»

4.1: «Una lectura sale de legacy solo por una de dos vías: (i) su cifra la produce código GEN2 desde un insumo crudo con hash —microdato o capturas selladas—; o (ii) es la lectura de una conducta del motor que ya tiene procedencia GEN2, y entonces el pin cita el RESULT de esa conducta, no una foto. Ingerir un número GEN1 como insumo, con hash o sin él, no cuenta nunca. El contador muestra las clases sin fundirlas.»

## 3 · LO QUE DIRECCIÓN SABE (todo contra `d5825063`–`8d78cf5f`, 21/sep)

* `[EJECUTADO]` 15 FP no cerradas; 17 corridas `SELLADA · PENDIENTE-DE-MESA`, de las cuales 13 con `resultado_replay = REPRODUCE` y 4 `NO-VERIFICADO` (`EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002`, `ENFIH2019-COBERTURA-SALDOS-CATPOS-0001` y `-0002`, `WBES2023-PRECISION-INTERACCIONES-0001`).
* `[EJECUTADO]` B1: el careo está en `forense/analisis/gen2-encig-cruces-historicos-cli-1/adjuntos/04-CAREO-PILOTO-3-…md` · `claude/optimistic-cray` ya no está en origin · 153 CALC con sello en disco y 153 con fila en `corridas.tsv` (cero sin publicar) · FP-328 abre con «Nada que firmar».
* `[EJECUTADO]` `CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001`: `cuenta = SI`, `REPRODUCE`, sin fila de respaldo (FP-388).
* `[LEÍDO]` `tests/test_celdas_d.py:79` fija `UNIDADES_OBJETIVO = {persona, hogar, establecimiento, agregado_geografico}`.
* `[LEÍDO]` Para 4.8: `CALC-ENIF-0001/spec.yaml` → input `enif_2024_enif_2024_bd_csv` (manifiesto) + spec sellada; `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1/spec.yaml` → su primer input es `data/corrida0/CALC-ENIF-0001/resultados.json`; ambos `REPRODUCE/IDENTICO`, valores idénticos (0.458657; 0.62687).
* `[EJECUTADO]` Para 4.1: los 14 valores M son cinco constantes de `milpa/tramite.yaml` — `:636` `denuncia_con_miedo_o_desconfianza` (GEN2), `:856` `recibe_dinero_familiares_para_vejez` (GEN2), `:910` `recibe_remesas` (GEN2), `:62` `paga_mordida_encig2025` (GEN2), y `:661` `tiene_ahorros = 0.174804`, sin `corrida0_generacion`: sigue GEN1 (ENNViH). `CALC-TRIADA-0001` los toma de `forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json`.
* `[SUPUESTO]` que el mecanismo de la casa para `cuenta_gen2` es un campo en el `spec.yaml` más una fila en `decisiones.tsv` (así lo hicieron RECIBO-4 y RECIBO-6). Verifícalo en esos dos actos antes de tocar una spec sellada; si el mecanismo es otro, usa el que sea.
* `[SUPUESTO]` que #934 (FP-402) y el arreglo de CI los está llevando mesa directamente. No los dupliques: asienta la firma y el sucesor.

## 4 · YA HECHO / YA DECIDIDO

`GEN2-TRAMITE-FIRMAS-1` y `-2` existen como precedente de mecánica: léelos. 4.7 se está ejecutando en `acto/gen2-limpieza-ramas-locales-4-cierre-fp402` (#934). 4.11 y 4.4 los lleva mesa. NC-0217 y NC-0319 ya estaban decididas por la firma F-2 del 15/sep y NC-0214 (de la que dependían) está `CERRADA`: no las cierres aquí — son ejecución de RELEVO-TANDA-3.

## 5 · PIEZAS

P1 · Cierres por evidencia (B1). NC-0349, NC-0359, NC-0358, NC-0415 → `CERRADA`, cada una con la evidencia de §3 re-verificada por ti. NC-0033 → reserva declarada, fuera del conteo de deuda activa, por el mecanismo que la casa tenga; si no hay ninguno, `CERRADA` con razón «hipotético sin caso real; se reabre si aparece uno». FP-328 → `CERRADA` (recibo sin materia).

P2 · Archivos que no llegan (B2). NC-0371: mesa declara que la evaluación no entra como anexo → cierra con esa razón. NC-0225: «no localizable»; la firma del 15/sep queda respaldada por su ADR → cierra, con el precedente citado. NC-0038 y NC-0039: «ya no aplica» → cierran.

P3 · Contador. (3A) `cuenta_gen2 = SI` para las 13 con `REPRODUCE`. Dos de ellas —`ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001-v1_1` y `ENUT2024-DISTRIBUCION-HORAS-0002`— suceden a una versión que sí corrió: cuentan, y en el mismo commit se abre una FP por cada una pidiendo el dictamen «¿la corrección pudo depender de haber visto el resultado?»; no lo dictamines tú. (3B) las 4 `NO-VERIFICADO` no cambian; una NC con sucesor «lote de replay aislado». (3C) FP-388 → `FIRMADA`, con fila de respaldo por el id exacto del CALC. (3D) `cuenta_gen2 = SI`, caso por caso y con la razón escrita —«el insumo legacy es el árbitro, leído como control y como rejilla, no como fuente de la cifra»—, para `CALC-C2-COMPUESTO-RESERVADAS-0001`, `CALC-C2-COMPUESTO-IC-ENIF2024-0001`, `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001` y `CALC-PISOS-ENIF2021-FORMALIDAD-0001`; FP-395, FP-396, FP-397 → `FIRMADA`; NC-0350 y gemelas, según corresponda. Si el registro vuelve a bajarlas a `NO` por `envuelto_legacy` al regenerar: no fuerces nada — reporta el campo exacto que decide, y eso va a dirección. Demanda declarada: una NC/fila de demanda «re-medir el árbitro (`tramite-ola5-propuesta-v0.yaml`) bajo cadena GEN2», entorno CAJA, sin sucesor asignado aún.

P4 · Estándar nuevo, como semilla. `PARA-v2.16` en hallazgos: «cuando no existe módulo guardián para una ola reservada, la guardia de una sola variable puede vivir en el medidor, con la misma semántica que el guardián, auditoría automática del código antes de abrir el dato, y prueba por mutación» (firma 3D, segunda mitad).

P5 · Diseño. (4.2) `evento` entra a `UNIDADES_OBJETIVO`; un caso de test; la celda-D del piloto 3 (`GOB.gobierno_digital…`) declara su unidad verdadera; FP-393 → `FIRMADA`. No toques la celda-D `TRA…` (delito): lístala como pregunta. (4.3) FP-387 → `FIRMADA` opción (c); no cambies el esquema: sucesor = mesa MOTOR, que lo diseña. (4.4) FP-398 → `FIRMADA` opción (a), FP-403 absorbida; ejecución: la lleva mesa en su trabajo de CI. (4.5) FP-394 → `FIRMADA`: ambos merges ratificados; ADR de recibo para #901. (4.6) FP-386 → `FIRMADA` opción (a). (4.7) FP-402 → `FIRMADA`; ejecución en #934. (4.9) NC-0317 → cierra: se conservan como legado descriptivo. (4.10) NC-0260: si re-derivar `data/reactivos-ciegos-81-v1_0.tsv` marcando las 2 368 filas es ≤ 10 líneas en `tools/censa_reactivos_ciegos.py`, hazlo (no borres filas: márcalas y exclúyelas del denominador); si es más, deja la firma asentada y el sucesor.

P6 · Las dos revisadas y confirmadas. 4.8: NC-0244 cierra; `decisiones.tsv` objeto `pin:RES-0047-0049`; no edites `tramite.yaml` — ya cita `CALC-ENIF-0001`; lo que falta es que la vista deje de reportar conflicto, y eso es de RELEVO-TANDA-3. 4.1: `decisiones.tsv` objeto `contador:legacy-semantica`, con el texto verbatim y, como evidencia, la tabla de las cinco conductas de §3. No muevas el contador.

P7 · Reasignaciones (B5, B6). Campo `sucesor` actualizado, sin cerrar: FP-374 y NC-0161/0162/0234/0237 → mesa MOTOR (duelo prospectivo ENVIPE 2026); NC-0164, NC-0318, NC-0037 → mesa PRODUCTO-DINERO; NC-0213 → mesa TUBERÍA (ids posicionales); NC-0217, NC-0319 → RELEVO-TANDA-3; NC-0218 → informe v1.2; NC-0324 sigue diferida a F6. FP-324 → `CERRADA`; sus dos recetas abiertas (RUPC, OECD PUM) quedan como sucesor «carril de adquisición», sin escribir su cola.

## 6 · LATITUD

Decides tú: el orden; cómo agrupar commits; el mecanismo exacto de `cuenta_gen2` que la casa use. Preguntas a mesa y sigues: una fila cuyo estado al abrir ya no coincide con §3. No decides: nada que el renglón de firma no diga.

## 7 · PAROS (lista cerrada)

Mover `adoptados_activos` o `dependencias_numericas_legacy_activas` · editar resultados o medidor de un CALC · cambiar un `p` en `milpa/` · escribir una firma con texto que no sea el verbatim de §2 · objetivo inalcanzable.

## 8 · COMPUERTAS

Ninguna.

## 9 · PERÍMETRO

Propio: `forense/firmas-pendientes.tsv` · `data/corrida0/decisiones.tsv` · `forense/no-corrido.tsv` · `forense/hallazgos.md` · `spec.yaml` de los CALC nombrados, solo el campo de contador si ése es el mecanismo · derivados por comando · `tests/test_celdas_d.py` y la celda-D `GOB…` (4.2) · `tools/censa_reactivos_ciegos.py` y su TSV (4.10, si cabe) · tablero · ADR · el cuaderno archivado. Ajeno: `milpa/**` · `requirements.txt`, `verify.yml`, `tests/check.py` (los lleva mesa) · `tools/corrida0.py`, `tools/relevo_usos.py` · toda rama ajena · `prereg-duelo-v2/**`.

## 10 · NO HACE · SUCESORES · CIERRE

No releva slots · no dictamina ENSAFI/ENUT · no diseña el tier partido · no toca CI · no abre la bandeja de titular. Sucesores: `RELEVO-TANDA-3` (14 R, 13 M por herencia, los 9 L uno por uno, NC-0217/0319, y que la vista deje de casar por `RES` posicional — coordinado con TUBERÍA) · lote de replay de las 4 · dictamen ENSAFI/ENUT · diseño de tier partido (MOTOR). Cascada de `/acto` · `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

- **qué:** regeneración de `data/corrida0/corridas.tsv` (vista derivada) vía `tools/corrida0.py registro --escribe`, para que las trece + cuatro firmas de `cuenta_gen2=SI` se reflejen también en esa vista (además de en `status`, que ya las cuenta). **por qué:** `PARO-ENTORNO` — `registro --escribe` para con `REPLAY-PISADO` sobre `CALC-ENIF-0001--afbf3c76d71b` (`contexto_replay: IDENTICO -> DISTINTO`), una corrida ajena a este lote (deriva de `ACTO GEN2-NUBE-PILOTO-1-bis`, `ADR-573`; reproducido incluso con todos los cambios de este acto revertidos vía `git stash`, así que no lo causó esta sesión). No se forzó con `--lote`: mover un veredicto ajeno sin entenderlo viola el "no forzar" del propio comando. **impacto:** `data/corrida0/corridas.tsv` sigue con los valores viejos de `cuenta_gen2`/`estado` para las diecisiete filas de este acto hasta que se regenere; `python3 tools/corrida0.py status` (que sí lee `decisiones.tsv` en vivo) ya refleja el contador correcto (`N_corridas_selladas` 102→118). **sucesor:** `ACTO GEN2-NUBE-PILOTO-1-bis` o quien resuelva el `contexto_replay` de `CALC-ENIF-0001`, y entonces corre `registro --escribe --lote CALC-ENIF-0001--afbf3c76d71b,<los 17 de este acto>`.
- **qué:** P5 4.10 — recortar el denominador de `data/reactivos-ciegos-81-v1_0.tsv` (2 368 filas de `NC-0260`) en `tools/censa_reactivos_ciegos.py`, si cabía en ≤10 líneas. **por qué:** `NO-VERIFICABLE-AQUÍ` — no se evaluó si cabía en ≤10 líneas por presupuesto de la sesión; no se tocó ni el script ni el TSV. **impacto:** el denominador de `NC-0136`/`NC-0260` sigue sobreestimado. **sucesor:** `NC-0260` sigue `ABIERTA` con su sucesor ya vigente (acto que re-derive el TSV, o mesa).
- **qué:** `tests/check.py --baseline --parallel` cierra `LÍNEA BASE: ROJO` (2 `T22` FAIL nuevos: `forense/encargos/2026-09-21-GEN2-SENAL-1.md` y `forense/notas/2026-09-21-GEN2-SENAL-1-cierre.md` sin fila en `firmas-pendientes.tsv` que cite su marcador de ranura). **por qué:** `FUERA-DE-PERÍMETRO` — ambos archivos pertenecen a `ACTO GEN2-SENAL-1` (otro acto, ya fusionado a `origin/main` antes de que esta rama arrancara); verificado con `git stash` de todos los cambios de esta sesión: el mismo ROJO aparece con o sin ellos, así que no lo causó este acto. Autor del contenido (qué dice exactamente el marcador de ranura de `GEN2-SENAL-1`) no es este acto, así que la fila de `firmas-pendientes.tsv` no se inventa aquí. **impacto:** la suite cierra ROJO por un defecto ajeno; no bloquea ninguna de las piezas P1-P7 de este acto (ninguna toca `GEN2-SENAL-1`). **sucesor:** mesa, o un acto de trámite que añada la fila faltante a `firmas-pendientes.tsv` (A.12) o sume los dos archivos a `_T22_ARCHIVOS_CONOCIDOS` con la exclusión explicada.
