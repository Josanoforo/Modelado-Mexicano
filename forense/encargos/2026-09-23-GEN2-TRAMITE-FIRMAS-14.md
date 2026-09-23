# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-14 · Asienta las decisiones de mesa sobre las once FP abiertas al 23/sep (tarde), con texto verbatim, y cierra las que otros actos ya resolvieron

> ENTORNO: **NUBE**. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `6a2cd6c7` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-tramite-firmas-14` (D-17) · MODELO: Sonnet · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; las adopciones que aquí se asientan mueven contadores solo cuando el derivador corra (CONTADORES-2 y el canal).

## 1 · OBJETIVO
Que las once FP abiertas a `6a2cd6c7` tengan decisión escrita o dueño con fecha. Hoja para mesa (lenguaje llano; mesa contesta con letras; el texto de firma ya está):
- **A · `…657c-02` contrato celda-D.** Situación: el contrato v0.6 exige punto e IC en un mismo CALC; un piso compuesto de marginales públicos solo tiene IC cuando nace con R. Opciones: A1 aceptar «IC nacido con R» rotulado así · A2 exigir IC propio (veta esos pisos). Recomendación: **A1**, con rótulo `IC-CON-R` en el yaml. Firma: «El contrato celda-D admite IC nacido con la R, rotulado IC-CON-R; no cambia PROSPECTIVA de la emisión.»
- **B · `…657c-04` canal del marcador y C · `…988c-01` procedencia.** Las resuelve CONTADORES-CONSUMO-2 con la firma de su §2 (viaja en el encargo; aquí solo se marcan `EJECUTA: CONTADORES-CONSUMO-2`).
- **D · `…1f30-01` ENDUTIH 1 551 celdas y E · `…1f30-02` MOCIBA 279 celdas.** Situación: Astra pide adoptarlas como piso **descriptivo retrospectivo**, sin uso predictivo. Opciones: (i) adoptar con ese rótulo · (ii) esperar la auditoría post hoc. Recomendación: **(ii)** — se adoptan cuando AUDITORIA-POST-HOC-ASTRA-1 diga LIMPIO; texto listo: «Se adoptan como piso descriptivo retrospectivo, sin uso predictivo, las celdas de <CALC> que la auditoría marcó LIMPIO.»
- **F · `…e422-01` ENOE.** Igual que D/E: adoptar tras auditoría; además verificar que el último trimestre quedó reservado (F-ASTRA-5-3).
- **G · `…cfce-01` cascada de sello externo.** Opciones: G1 `stamp` no bloqueante en cada cierre · G2 solo manual por mesa. Recomendación: **G1**. Firma en SELLO-EXTERNO-2 §2 (viaja allá).
- **H · `…4296-01` Pages y Zenodo.** Es acción tuya (dos casillas en Settings → Pages; cuenta Zenodo + release `v2026.09`). Aquí se asienta cuando esté: URL y DOI.
- **I · `…1269-01` cola de fusión** y decisión de proceso: ¿`codex/*` entra sin recibo? Opciones: I1 auto-merge fusiona rutinas `[deriva]` y trámites; `codex/*` y `acto/*` que sellan corridas siempre con recibo/botón · I2 todo por botón. Recomendación: **I1**. Firma: «El auto-merge cubre `claude/encola-*`, `acto/gen2-tramite-*` y `[deriva]`; `codex/*` entra por recibo; nada que selle corridas se fusiona sin mesa.»
- **J · `…3d56-01` respaldo.** Vence domingo 27/sep; sin decisión nueva.
- **K · `…c3fa-05` alianza académica.** Dueño mesa; fecha a fijar.
«Hecho»: cada una de las once con estado FIRMADA (texto verbatim), EJECUTA:<acto> o ABIERTA con `vence:`; `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA
Las que mesa dé sobre la hoja de §1 al lanzar, verbatim. Sin ellas, el acto asienta solo B, C, G (que viajan en otros encargos) y J, K (sin cambio), y deja el resto ABIERTA: no es PARO.

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` once FP ABIERTA en el TSV a `6a2cd6c7` (lista en §1); `…657c-03` ya cerró con #1078. `[LEÍDO]` textos de las FP (citados en §1). ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -c 'FIRMAS-14' forense/firmas-pendientes.tsv` → 0. FIRMAS-13-v2 (#1081) es el último trámite.

## 5 · PIEZAS
P1 · una fila por decisión con texto verbatim y ejecutor. P2 · cierre de las que otros actos resolvieron (`657c-03` si aún dice ABIERTA en alguna vista; ninguna otra sin verificar por id, A.17). P3 · `vence:` en J y K.

## 6 · LATITUD
Orden libre. Pregunta a mesa: la fecha de K.

## 7 · PAROS — lista cerrada
a) no aplica · b) editar una fila FIRMADA previa · c) adoptar a mano (una FP FIRMADA de adopción no mueve nada hasta que su acto ejecutor corra) · d) no aplica · e) CAJA · f) todo ya asentado.

## 8 · COMPUERTAS
«Texto verbatim; adopción de Astra solo tras LIMPIO de la auditoría» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/firmas-pendientes.tsv`, `no-corrido.tsv` (append/estado), nota, L0, cascada. Ajeno: todo lo demás. En vuelo: AUDITORIA-POST-HOC-ASTRA-1, CONTADORES-2, MOTOR-2, RECIBO-5, SELLO-EXTERNO-2 (union en TSV).

## 10 · LO QUE NO HACE · SUCESORES
No ejecuta ninguna decisión. Sucesores: los actos nombrados en cada fila; FIRMAS-15 para DOI/Pages y adopciones tras auditoría.

## NO-CORRIDO / RESERVAS

- **qué**: A · `…657c-02` contrato celda-D (rótulo `IC-CON-R` propuesto por dirección). **por qué**: `DECISIÓN-DE-MESA-PENDIENTE` -- ninguna firma verbatim llegó con el lanzamiento. **impacto**: el contrato v0.6 de celda-D sigue sin resolver si un piso con IC nacido de R se rotula `IC-CON-R`; ningún piso C2-compuesto de marginales públicos se adopta con ese rótulo mientras tanto. **sucesor**: `GEN2-TRAMITE-FIRMAS-15` (§10 del encargo).
- **qué**: D · `…1f30-01` adopción ENDUTIH (1551 celdas) como piso descriptivo retrospectivo. **por qué**: `DECISIÓN-DE-MESA-PENDIENTE` -- Adenda-1 solo actualiza el rótulo esperado del veredicto (`LIMPIO` → `RECIBO-COMPLETO`), no sustituye la firma. **impacto**: `adoptados_activos`/pisos descriptivos de tecnología no suben; ninguna celda ENDUTIH se usa como piso hasta la firma. **sucesor**: `AUDITORIA-POST-HOC-ASTRA-1` (veredicto `RECIBO-COMPLETO`) + `GEN2-TRAMITE-FIRMAS-15`.
- **qué**: E · `…1f30-02` adopción MOCIBA (279 celdas) como piso descriptivo retrospectivo. **por qué**: `DECISIÓN-DE-MESA-PENDIENTE`, misma razón que D. **impacto**: igual que D, para MOCIBA. **sucesor**: `AUDITORIA-POST-HOC-ASTRA-1` + `GEN2-TRAMITE-FIRMAS-15`.
- **qué**: F · `…e422-01` adopción de los pisos y el dictamen de límites ENOE (ASTRA5-U1). **por qué**: `DECISIÓN-DE-MESA-PENDIENTE`, misma razón que D/E; además pendiente verificar que el último trimestre quedó reservado (F-ASTRA-5-3). **impacto**: los reports Trabajo, Mérito/Movilidad y Juventud no pueden citar el piso ENOE como adoptado. **sucesor**: `AUDITORIA-POST-HOC-ASTRA-1` + `GEN2-TRAMITE-FIRMAS-15`.
- **qué**: H · `…4296-01` activar GitHub Pages y decidir DOI Zenodo. **por qué**: `NO-VERIFICABLE-AQUÍ` -- es acción de dirección fuera del repo (Settings → Pages de GitHub; cuenta Zenodo), no verificable ni ejecutable por comando de esta sesión. **impacto**: sin URL de landing ni DOI que citar. **sucesor**: `GEN2-TRAMITE-FIRMAS-15` (§10 del encargo, nombrado explícitamente para DOI/Pages).
- **qué**: I · `…1269-01` decisión de proceso sobre la cola de fusión (`codex/*` con o sin recibo). **por qué**: `DECISIÓN-DE-MESA-PENDIENTE` -- `ADENDA-1` de dirección reescribe la recomendación (opción (i): auto-merge de rutinas + recibo de Codex a la vista para `codex/*` y actos que sellan corridas) pero no es una firma de mesa. **impacto**: la política real de fusión de `codex/*` sigue sin asentarse con texto verbatim. **sucesor**: `GEN2-TRAMITE-FIRMAS-15`.
- **qué**: K · `…c3fa-05` fecha de la alianza académica (P3 del encargo: «`vence:` en J y K»). **por qué**: `DECISIÓN-DE-MESA-PENDIENTE` -- §6 del encargo pide preguntar la fecha a mesa; sin respuesta, no hay fecha que asentar como `vence:`. **impacto**: `FP-260923-GEN2-TRAMITE-FIRMAS-12-c3fa-05` sigue sin plazo. **sucesor**: `GEN2-TRAMITE-FIRMAS-15`.
