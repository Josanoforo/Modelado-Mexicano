# ACTO TABLERO-FIRMAS · Sella `ADR-84` — crea `forense/firmas-pendientes.tsv`, sella `A.12`, encarga `T-FIRMAS`

**Acto:** ACTO TABLERO-FIRMAS · **Entorno:** repo-only, nube, sin red, sin `data/raw` · **Depende de:** `ADR-76`/`ADR-79` (patrón SELLA-3, citado por nombre en el encargo) · `ADR-MOTOR-2-esqueleto-2026-08-14.md` (M1-M6) · `ADR-78`/`ADR-81(c)` (A.9) · `ADR-76(h)`/`ADR-77`/`ADR-79(e)`/`ADR-81` (A.7/A.10) · `ADR-76(e)` (precedencia de puertas).

## §0 · ARRANQUE

1. **REPO.** Clon existente en uso: `/home/user/Modelado-Mexicano`, rama `claude/tablero-firmas-mecanismo-tocpwi`.
2. **HEAD / SHA.** Al arrancar: `865b54a` (merge PR #234, S7-MOTOR-2-AMANUENSE). **`origin/main` se movió durante la investigación de este mismo acto** — `PR #235` (`ACTO PROD-P638`) fusionó a `2f2125c` mientras se derivaba el barrido de la sección §1 de abajo. Verificado con `git fetch` + `git diff HEAD...origin/main --stat` antes de escribir ningún archivo; el diff tocaba `canon/estado-programa-v1_10.md`, `canon/modelo-decision-v4_0.md`, `forense/hallazgos.md`, `milpa/procedencia.yaml` y expedientes de `data/curacion-registro/` — ninguno de `canon/gobernanza-v1_15.md`, así que sin riesgo de colisión de número de ADR. `git merge origin/main --no-edit` — limpio, sin conflictos. Re-derivado tras el merge: `python3 -c "..."` sobre `canon/gobernanza-v1_15.md` → únicos 83 · max 83 · huecos [] → **ADR-84** contiguo, sin colisión. No es PARO — refresca y reporta la diferencia, exactamente lo que Bloque D exige.
3. **data/raw.** Ausente, no requerida — acto de gobierno puro, sin microdato.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`; este acto no toca red ni microdato, sonda saltada.
5. **Baseline, antes de tocar nada (tras el merge de `PR #235`):** `python3 tests/check.py` (crudo) → **20 FAIL · 119 WARN**.
6. **Ramas vivas.** `git ls-remote --heads origin` → `main`, `claude/motor-3-e0-codigo-m2jo24`, `enlace-2`. Ninguna toca `canon/gobernanza-v1_15.md` (`git diff origin/main...<rama> --stat`, verificado para las dos) — sin riesgo de colisión de ADR mientras corre este acto.

## §1 · Los dos barridos mandados por el encargo, salida cruda

```
$ grep -rn "RANURA" canon/ forense/ milpa/
forense/notas/2026-08-13-proc-11.md:202:## §5 · RANURA D3 — **VACÍA en este acto**
forense/encargos/2026-08-13-MOTOR-COND-v2-encargos-finales.md:75:...(e) [RANURA D3 — SOLO con firma pegada verbatim: ...]
```

Dos hits, ninguno dentro de `forense/ADR-MOTOR-2-esqueleto-2026-08-14.md` — ese archivo usa "ranuras" en minúscula y `[FIRMA M_ — VACÍA]`, no la palabra `RANURA` en mayúscula. **Los seis incisos M1-M6 se añaden al tablero por la lista explícita del encargo, no por este grep** — verificado de nuevo por lectura directa del archivo, confirmando las seis `[FIRMA M_ — VACÍA]` vacías (líneas 35, 45, 55, 65, 75, 85). El propio hit de `RANURA D3` se verificó por separado (§2 abajo) y resultó ya resuelta.

```
$ grep -rn "requiere_decision.*true\|PENDIENTE de mesa\|pendiente nombrado.*mesa\|PROPUESTA.*mesa" \
    canon/ forense/ milpa/ data/ tools/ tests/ *.md
```
48 líneas de salida (archivo completo conservado en el historial de comandos de esta sesión; no se pega íntegro aquí por longitud — cada hallazgo sustantivo que produjo fila nueva o corrección está citado por archivo:línea en `forense/firmas-pendientes.tsv` y en las notas de §2). Clasificación aplicada a las 48 líneas: duplicados del mismo hallazgo bajo cita distinta se colapsan a una fila (p. ej. la reserva de género de `P7_12_7` aparece en 9 líneas distintas de 8 archivos — una fila); menciones de plantilla/definición del mecanismo (`propuesta-motor-adaptativo-celda-v0_1/2/3.md`, donde `requiere_decision_mesa` se define, no se instancia) se excluyen — no son un pendiente, son la especificación del campo; bloqueos técnicos declarados como `EN-ESPERA-DE-VIA` sin lenguaje de "decisión de mesa" se excluyen — son backlog de ingeniería, no firma; el resto, una fila cada uno, con la fecha y el estado verificados contra el archivo real, no contra la cita.

## §2 · Verificación contra archivo, no contra la cita — lo que cambió el resultado

**A.9 (item nombrado por el encargo, "sin fecha aún").** El encargo de hoy trae esta premisa. Verificado contra `canon/gobernanza-v1_15.md:1226` (`ADR-81`, ACTO SELLA-FREEZE, 14/ago/2026, ya en `main` antes de que este acto empezara): inciso (c) enmienda `ADR-78` con `> Fecha del pegado: 13/ago/2026.` y declara "`A.9` pasa de `PENDIENTE` a vigente" (`gobernanza:1246`). **La premisa del encargo estaba vencida antes de escribirse.** Se registra `FP-08` como `FIRMADA` (`ADR-81(c)`), no `ABIERTA` — per A.12 misma ("el tablero se deriva, no se recuerda"), incluida en el encargo o no.

**RANURA D3 (hit del primer grep).** `forense/notas/2026-08-13-proc-11.md` §5 la deja "VACÍA en este acto" (13/ago). Verificado contra `canon/modelo-decision-v4_0.md:290` (nota vigente, no historia fechada): *"Decisión D3, resuelta `D3-A`"*, vía `ADR-79(a)`. Resuelta. Se registra `FP-21` como `FIRMADA`.

**Propagación de `obligación_medida` (candidata a fila `ABIERTA`, derivada de D3-A sin la θ específica).** Al momento de derivar el barrido (antes del merge de §0.2), `canon/modelo-decision-v4_0.md:275` decía *"rótulo sin actualizar por `PROC-10-bis` — declarado, no ejecutado"* y el numerador de condicionales estaba en `10 de 15`. **Mientras este acto seguía investigando, `PR #235` (`ACTO PROD-P638`) fusionó** y resolvió exactamente esto: `obligación_medida` entra a `milpa/procedencia.yaml` bajo `MEDIDO·NACIONAL`, numerador `10 → 11 de 15`, la fila de `modelo-decision-v4_0.md:275` queda explícitamente vacía ("`0`"). Verificado post-merge, no heredado del estado pre-merge. Se registra `FP-16` como `FIRMADA` (`ACTO PROD-P638`, `PR #235`) — nunca estuvo `ABIERTA` en el tablero commiteado, aunque sí lo estuvo en el borrador de este mismo acto minutos antes.

**Hallazgo nuevo del propio `PR #235`, no nombrado por el encargo.** `forense/hallazgos.md` (entrada "ACTO PROD-P638, hallazgo fuera de perímetro", fusionada con el mismo `PR #235`) declara que `data/curacion-registro/especificaciones-produccion.json` tiene dos `supervisor_link.requiere_decision` en `"SI"` (`ESP-OPACA-B-d13ec4fe`/`norma_de_género`, `ESP-OPACA-C-9ecb5c61`/`radio_confianza`) que ya no reflejan las decisiones reales (`ADR-75(a)`, veredicto de `ENCARGO 9`/`ADR-82`). Verificado contra archivo real, no contra la cita: `grep -n "requiere_decision" data/curacion-registro/especificaciones-produccion.json` → líneas 61 y 106 siguen en `"SI"` al momento de escribir este tablero. Registrado `FP-23`, `ABIERTA` — encontrado por lectura de la cola de `hallazgos.md` durante la verificación de `FP-16`, no por ninguno de los dos greps mandados; cae bajo "lo que el barrido encuentre además".

**Disputa de rótulo `A.7` (item nombrado).** Tres reclamos históricos (`ADR-76(h)`) → dos tras `ADR-77`/A.8 → el segundo reclamo (estampa de universo) redirigido a `A.10` por `ADR-79(e)`, pero **la disputa de `A.7` en sí no se cierra**: `ADR-79(e)` mismo dice "No adjudica el rótulo `A.7` disputado — sigue en mesa" y su cláusula de Reversión contempla que mesa aún podría decidir que `A.7`, no `A.10`, debe absorber el principio. Reconfirmado por el ADR más reciente que toca el tema, `ADR-81` (14/ago, `gobernanza:1254`): "No adjudica el rótulo `A.7`, disputado — sigue en mesa." Fila `FP-07`, `ABIERTA`.

**"Política de pares de relaciones" (item nombrado, sin coincidencia literal).** `grep -rni "pares de relaciones\|pares_relaciones\|par de relaciones"` sobre todo el árbol → cero resultados, verificado dos veces. La lectura más cercana, sustanciada por `git log --all --grep="pares" -i` (cinco commits, todos de `ACTO RECONCILIA-PUERTAS`/`ADR-76(e)`): la regla de precedencia que decide, para **pares de filas** de `data/universo-puertas-*.tsv` que describen la **misma fuente** (misma relación fuente↔puerta), cuál gobierna. `ADR-76(e)` sella la regla (Regla 1/Regla 2, firma de mesa "Reconciliemos") pero declara expresamente que el diff (16 pares de filas contradictorias) **no se aplicó** — "Pendiente nombrado para acto propio, con perímetro que sí alcance `data/`." Reconfirmado hoy mismo por `ACTO SANEA-MAPEO` (`forense/notas/2026-08-14-sanea-mapeo.md:56`), que declara explícitamente no ejecutar esa retirada de fila, fuera de su propio perímetro. Fila `FP-10`, `ABIERTA`. Si esta lectura no es la que mesa tenía en mente, la fila queda como candidata corregible — el propio tablero permite retitular sin perder el registro (columna `estado` → `RETIRADA` con nota, nunca borrado de fila).

## §3 · Filas adicionales encontradas por el segundo barrido, no nombradas por el encargo

Ver `forense/firmas-pendientes.tsv` para el texto completo de cada una; resumen: `ficha-id-g3` (propuesta de sello completa, 5/ago) · `FUSION-PUERTAS` (firma dada, acto sucesor sin ejecutar) · `RUTA-SELLO` (ídem, taxonomía RUTA-A/RUTA-C/RUTA-I/SIN-RUTA) · `E3-TRIAGE` (ídem, Entrada 3 de `registro-recalculo`) · Entrada 5 de `registro-recalculo` (gateada por el sello de `ADR-MOTOR-2`, es decir por M1-M6) · `PROD-P638`→propagación (resuelta en vivo, ver §2) · cola de adquisición del sondeo-27 (`PROPUESTA-cola-sondeo27-2026-08-14.md`, de hoy mismo) · marcador `T20 pob=llaves` (condición de activación ya cumplida el 13/ago, `ACTO ADJ-4`) · precedencia E4c §4 (metodológica, para corridas futuras del mismo tipo).

## §4 · Contadores

**Contador propio del acto:** `0 → 19` firmas de mesa `ABIERTA` visibles, de 23 filas totales (19 `ABIERTA` + 4 `FIRMADA`) — el número exacto lo produce el barrido de §1-§3, no el encargo, que no proponía cifra.

**Contadores de medición que NO se mueven, declarados uno por uno:** `13 de 27` (Hito D) · `11 de 15` (condicionales — ya en 11 antes de que este acto tocara nada, por `PROD-P638`) · `0 de 15` (coeficientes) · `1 de 2` (llaves) · `4 de 144`. Ninguno — este acto no mide sobre México, gobierna el propio programa.

## §5 · Perímetro tocado

Commit 1: `forense/firmas-pendientes.tsv` (nuevo) · `instrucciones-proyecto-v2_9.md` (nuevo, incorpora v2.8 verbatim + `A.12`) · `canon/gobernanza-v1_15.md` (`ADR-84`, cabecera) · `canon/estado-programa-v1_10.md` (cascada) · este archivo. Commit 2 (separado, declarado en `ADR-84(c)`): `tests/check.py` (`T-FIRMAS`) — ver nota de ese commit para su propio diff y su propia corrida de suite antes/después. Nada de `milpa/`, `data/` ni `canon/modelo-decision-v4_0.md` en ninguno de los dos commits.
