# ACTO GEN2-TRAMITE-FIRMAS-3 · nota de cierre

Encargo archivado verbatim: `forense/encargos/2026-09-21-GEN2-TRAMITE-FIRMAS-3-PROPAGACION.md`.

## §0 · Premisa de logística caída, replanteada (v2.15 §2)

El encargo asume que existe `GEN2-TRAMITE-FIRMAS-2`; sólo existe `-1`
(`forense/encargos/2026-09-08-GEN2-TRAMITE-FIRMAS-1-PROPAGACION.md`), usado
como precedente de mecánica junto con
`forense/notas/2026-09-08-GEN2-TRAMITE-FIRMAS-1-propaga-firmas.md`. El
objetivo seguía alcanzable; se siguió con `-1` como único precedente.

## §1 · El defecto real de la sesión: editar `spec.yaml` rompe el sello

El primer intento de aplicar 3A/3D editó `etiquetas.cuenta_gen2` directamente
en catorce `spec.yaml` sellados. `tools/corrida0.py registro` paró dos veces
con `RESULT-SIN-SELLO` (`CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001`,
luego `CALC-ENADID2023-UNION-SEXO-EDAD-0004`). Revertidos los catorce
archivos. El mecanismo correcto, que `_cuenta_gen2_resuelto()`
(`tools/corrida0.py:3702`) ya documenta en su propio docstring como remedio
de un intento anterior de romper el sello de la misma manera
(`T-CORRIDA0`/`T-REPRO`, `fcddf9a`): una fila en `data/corrida0/decisiones.tsv`
con `objeto = <calc_id exacto>` (nunca `contador:<calc_id>`) y `decision` que
empieza literalmente `cuenta_gen2=SI · <motivo>`. Asentado en
`forense/hallazgos.md` (21/sep) para que no se repita.

`python3 tools/corrida0.py status` — **antes**: `N_corridas_selladas=102`,
`N_resultados_gen2_sellados=6686`; **después**: `N_corridas_selladas=118`,
`N_resultados_gen2_sellados=9479`. `adoptados_activos` y
`dependencias_numericas_legacy_activas` no se movieron (perímetro vedado).

`data/corrida0/corridas.tsv` (vista derivada) **no se reescribió** en este
acto: `registro --escribe` paró por `REPLAY-PISADO` sobre
`CALC-ENIF-0001--afbf3c76d71b` (`contexto_replay: IDENTICO -> DISTINTO`),
una corrida ajena a este lote (deriva de `ACTO GEN2-NUBE-PILOTO-1-bis`,
`ADR-573`, verificado reproducible incluso con `git stash` de todos mis
cambios). No se forzó con `--lote`: mover un veredicto ajeno sin entenderlo
viola el "no forzar" del propio comando. Ver `## NO-CORRIDO / RESERVAS`.

## §2 · P1-P7, pieza por pieza

- **P1 (B1):** `NC-0349`, `NC-0359`, `NC-0358`, `NC-0415` → `CERRADA`
  (evidencia re-verificada, ya estaba en el propio texto de cada fila).
  `NC-0033` → `CERRADA` ("hipotético sin caso real; se reabre si aparece
  uno", ya era el texto vigente). `FP-328` → `CERRADA` (recibo sin materia).
- **P2 (B2):** `NC-0371` → `CERRADA` (mesa declara: evaluación Codex no
  entra como anexo). `NC-0225` → `CERRADA` (su objeto principal, la
  lectura v1.1 y el adversarial, ya está archivado por `NC-0219`; el
  segundo insumo de Astra no bloquea ninguna cifra). `NC-0038`/`NC-0039`
  → `CERRADA` (ya no aplica).
- **P3 (contador):** trece CALC → `cuenta_gen2=SI` (3A):
  `CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001` (3C, retroactiva),
  `CALC-ENIGH2022-REMESAS-CONTEXTO-0001`,
  `CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001-v1_1` (abre `FP-406`),
  `CALC-ENUT2024-DISTRIBUCION-HORAS-0002` (abre `FP-407`),
  `CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001`, `CALC-WBES2023-PRECISION-0001`,
  `CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001`,
  `CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001`,
  `CALC-ENCRIGE-CARGA-INTENSIDAD-0001`, `CALC-ENVIPE-RES0028-U4-DERIVADO-0001`,
  `CALC-ISSP2017-CONSISTENCIA-APOYO-FAMILIAR-0001`,
  `CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001`,
  `CALC-ENADID2023-UNION-SEXO-EDAD-0004`. Las 4 `NO-VERIFICADO` (3B) no
  cambian (`NC-0441`). Cuatro CALC del árbitro (3D) →
  `cuenta_gen2=SI` caso por caso: `CALC-C2-COMPUESTO-RESERVADAS-0001`,
  `CALC-C2-COMPUESTO-IC-ENIF2024-0001`, `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001`,
  `CALC-PISOS-ENIF2021-FORMALIDAD-0001`; `FP-395`/`FP-396`/`FP-397` →
  `FIRMADA`; `NC-0350`/`NC-0380`/`NC-0387` → `CERRADA` (gemelas por E.1);
  `NC-0388` (marcador, inciso 2 de FP-397, ya ejecutado por otro acto) no
  se tocó — no es gemela de cuenta_gen2. Demanda declarada: `NC-0442`
  (re-medir el árbitro bajo cadena GEN2, entorno CAJA, sin sucesor).
- **P4:** `PARA-v2.16` (guardia de una variable en el medidor, estándar)
  asentado en `forense/hallazgos.md`.
- **P5:** `evento` entra a `UNIDADES_OBJETIVO`
  (`tests/test_celdas_d.py`, con caso de test positivo y negativo); la
  celda-D `GOB.gobierno_digital.encig2025.edad_x_escolaridad` declara
  `unidad_objetivo: evento`; `FP-393` → `FIRMADA`. La celda-D
  `TRA.evade_norma.envipe2025.escolaridad_x_dominio` (delito) **no se
  tocó**: queda listada como pregunta en `hallazgos.md`. `FP-387` →
  `FIRMADA` (c, no se cambia el esquema; sucesor mesa MOTOR). `FP-398` →
  `FIRMADA` (a; ejecución la lleva mesa); `FP-403` → absorbida por
  `FP-398`. `FP-394` → `FIRMADA` (a: ratifica `#897` y `#901`; recibo de
  gobierno de `#901` en el ADR de este acto). `FP-386` → `FIRMADA` (a).
  `FP-402` → `FIRMADA` (a; ejecución en `#934`). `NC-0317` → `CERRADA`
  (4.9). `NC-0260` (4.10, `tools/censa_reactivos_ciegos.py`) **no se
  tocó** por presupuesto de esta sesión — se evaluó que no era una
  extensión trivial de verificar en el tiempo disponible; queda `ABIERTA`
  con su sucesor vigente. Ver `## NO-CORRIDO / RESERVAS`.
- **P6:** `NC-0244` → `CERRADA`; `decisiones.tsv` objeto
  `pin:RES-0047-0049` (4.8) y objeto `contador:legacy-semantica` (4.1);
  ninguno de los dos mueve un contador ni edita `milpa/tramite.yaml`.
- **P7:** `sucesor` actualizado sin cerrar en `NC-0161`/`0162`/`0234`/`0237`
  y `FP-374` (mesa MOTOR), `NC-0164`/`0318`/`0037` (mesa PRODUCTO-DINERO),
  `NC-0213` (mesa TUBERÍA), `NC-0217`/`0319` (RELEVO-TANDA-3), `NC-0218`
  (informe v1.2), `NC-0324` (confirmado, sigue diferida a F6). `FP-324` →
  `CERRADA` (B6; dos recetas abiertas quedan como sucesor «carril de
  adquisición», sin escribir su cola).

Cuaderno de firmas archivado como reconstrucción legítima (v2.15 §0/A.3):
`forense/encargos/CUADERNO-DE-FIRMAS-2026-09-21.md` + `.sha256` — el texto
verbatim ya vivía íntegro en la sección 2 del encargo; este archivo lo
materializa como adjunto propio, sin agregar ni quitar palabra.

## §3 · Adenda de mesa (fuera de P1-P7)

Recibida en conversación mientras el acto seguía en curso, antes de la
cascada de cierre. Tres firmas asentadas VERBATIM, sólo como fila, sin
ejecución adicional:

1. `reserva:envipe2026` en `decisiones.tsv`. Búsqueda de una lista central
   de patrones "ola reservada" (guardias/configs): no existe una; el
   estado de reserva se marca por payload en `data/manifiesto.yaml`
   (campo `estado_reserva`) al registrarlo. ENVIPE 2026 aún no está en el
   manifiesto (no se ha bajado el payload), así que no hay campo que
   tocar hoy — la reserva rige desde la firma y se aplica al ingerir el
   payload. Declarado como hallazgo, no silenciado.
2. `alcance:v0` en `decisiones.tsv`, citando (no duplicando) la reserva de
   crédito ya en `main` (`ACTO GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1`,
   `data/credito-comparabilidad-texto-v1_0.tsv`).
3. `metrica:rectora` en `decisiones.tsv` — ya implementada por `#933`;
   sólo faltaba la fila.

## §4 · Defecto adyacente corregido (D-21, ≤10 líneas)

`canon/estado-programa-v1_14.md` traía, ya en `main`, tres marcadores de
conflicto de `git merge` sin resolver (`<<<<<<< HEAD` / `=======` /
`>>>>>>> origin/main`) entre las anotaciones L0 de `ADR-573` y `ADR-572`.
Removidos los tres marcadores preservando íntegro el texto de ambas
anotaciones (ninguna palabra de contenido tocada). Esto bloqueaba insertar
la anotación propia "antes de la anterior" de forma limpia y arriesgaba que
la suite fallara sobre un archivo canónico roto.
