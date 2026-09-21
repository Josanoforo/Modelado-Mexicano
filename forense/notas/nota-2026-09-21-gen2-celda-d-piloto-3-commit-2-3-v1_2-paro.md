# `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2` · PARO (b) sin parche: el CALC congelado en `#926`/`#944` corre pero **no sella** — `corrida0 run` termina en `RUN: FALLO — nada se sella` por 40 RESULT `valor_null_sin_NO-ESTIMABLE_permitido`; ENCIG 2025 fue leída por el medidor congelado (una variable, en proceso), ninguna cifra salió, nada quedó en el árbol

**Veredicto del piloto: NO HAY.** Universo: pagos ordinarios del servicio de luz (`N_TRA == 01`), unidad TRÁMITE, escala proporción/pp. Clase de evidencia: **ninguna nueva** — cero corridas selladas, cero adjudicación, cero celda-D llena. Lo que este acto entrega es el **quinto** fallo de conducto del piloto 3, y el primero **posterior** a que el preflight saliera VERDE: la prueba del congelador de `#944` (pytest 7/7 + `preflight` VERDE) todavía no cubre el conducto completo. El falsador que el propio encargo dejó escrito «a tres meses» se cumplió a las 0 h del día siguiente.

Entorno **CAJA** (WSL2, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, corpus montado `archivos_examinados=419`, `raices data_raw:SI descargas_mx:SI`), Opus 5, sesión `c0ab3df1`, sin sub-agentes, MODO RÍGIDO. Encargo archivado verbatim (A.3) con sello de cuerpo: `forense/encargos/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2.md` (`50d4b0ef…ac0e`, idéntico al `.sha256` que acompañó al original en `Descargas MX`). Base: `origin/main = 13129c05` = merge de `#944` (el encargo declaraba `73d7c816` + `#944`; main se movió 19 commits por `#946` y el propio `#944`; re-derivado, no es PARO).

---

## 0 · Para mesa, en una página

**Qué se iba a probar.** Si la interacción edad × escolaridad en el pago digital de luz, estable en ENCIG 2021 y 2023, se transporta a 2025 cuando el nivel subió once puntos. Tres candidatos (C2 piso, S½ y Sλ retadores), 15 celdas puntuadas, B-bis verbatim.

**Qué salió.** Nada. P0 completo y en verde (sidecar OK · `tests/test_piloto3_v11.py` 7/7 con la prueba de oro sobre 2023 · `corrida0 preflight EMISIONES-0002` VERDE con el payload `COINCIDE` · `cuenta_gen2 = SI` resuelto por `_cuenta_gen2_resuelto` para los dos CALC). Después, `python3 tools/corrida0.py run CALC-GOB-DIGITAL-EXE-EMISIONES-0002` ejecutó el medidor congelado (13,7 s) y `corrida0` **se negó a sellar**: 40 de los 565 RESULT declarados vienen `null` y la spec no declara `permite_no_estimable: true` para ninguno (`tools/corrida0.py:1951`). Salida cruda en §4.

**Por qué, en dos líneas (diagnóstico por lectura, §5).** (A) 32 RESULT: los IC de la referencia C1a son «NO-DERIVABLE» **por diseño de la spec** (no hay réplicas selladas de 2023 para componer) — el medidor emite `None` (`medidor.py:416`) y el `spec.yaml` lo declara con `unidad: "NO-DERIVABLE (null)"`, pero le falta la llave que el runner exige. (B) 8 RESULT: el control C2-compuesto de la banda **60-96** no se encuentra porque el CALC sellado `CALC-C2-COMPUESTO-RESERVADAS-0001` rotula esa banda `…-60-X-…` y el medidor la busca como `…-60-96-X-…` (`medidor.py:355`); `.get` devuelve `None` en las 4 celdas y arrastra `C2-VS-CONTROL-ABS`.

**Por qué no lo vio `#944`.** `preflight` no ejecuta el medidor. La prueba de oro reproduce 2023 con el `resultados.json` real de C2-compuesto pero **no asevera que los 16 controles sean no nulos**, y el test sintético construye el fixture del control **con la clave del propio medidor** (`tests/test_piloto3_v11.py:98`), así que nunca pudo discrepar. Ninguna prueba llama a `corrida0._valida_outputs`. Misma clase que `#903`, `#924`, `#926`, `#941`: el congelador valida el procedimiento, no el conducto.

**Qué se hizo con eso.** Nada más. PARO (b) del encargo: «el código congelado no corre → no se parcha; el sucesor es un COMMIT-1 v1.3 de otra sesión». No se editó ningún `spec.yaml`, ningún `.py`, la spec humana ni su sidecar. `git status` limpio tras el `run`; los dos directorios CALC siguen sin `ejecucion.json`, `resultados.json` ni `sello.*`. No se repitió la corrida (es determinista y no habría producido nada distinto).

**Qué NO significa.** No dice nada sobre la interacción, ni sobre el +11 pp, ni sobre «gobierno digital» o confianza en el Estado. El universo sigue siendo el pago ordinario de luz por trámite. El conteo del código 97 (S2, `FP-399`) **no se reporta**: el medidor lo calculó en memoria pero el sello no existe, y un número fuera del sello es una salida que el procedimiento no produjo.

**Exposición de esta sesión, declarada (ADR-46 / F3).** El medidor congelado leyó `encig25_base_datos_csv.zip` y agrupó **por una variable** (lo autorizado); `corrida0` descartó el resultado antes de escribir nada y la consola sólo mostró la lista de ids nulos. **No vi ninguna cifra de 2025**, ni marginales ni conteos. No leí diseños A/B ni el careo. Comparto memoria persistente con las sesiones de `#941`/`#944`; el puntero de estado del piloto 3 que hay ahí **no lo abrí**. Aun así, por prudencia, **esta sesión no debería congelar el v1.3** (§7).

**Lo que mesa decide** está en `FP-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-01` (§8): quién congela el v1.3, si la clave del control cuenta como cableado aunque viva en `medidor.py`, si la firma de contador se hereda una tercera vez, y qué debe cubrir la prueba del congelador (D-22) para que no haya un sexto acto perdido.

---

## 1 · Arranque (`/acto`, guard 0.a–0.d) y F3

- **F3.** Sesión nueva (`c0ab3df1`); no es `pc0-77` (v1.1, `#926`) ni la que paró en `#941` y congeló v1.2 en `#944`. Sin diseños A/B ni careo en contexto. Declarado arriba lo de la memoria compartida.
- **0.a** `git fetch --prune` · `rev-list --count HEAD..origin/main = 0` sobre el worktree nuevo `/home/pc0/mm-piloto3-c23` creado desde `origin/main` (`13129c05`). `#944` en main: `git merge-base --is-ancestor 48a4aa54 origin/main` → SI.
- **0.b** `git status --porcelain` vacío.
- **0.c** `git ls-remote --heads origin | grep -i piloto-3-commit-2-3` → 0 (la rama de `#941` ya no existe en el remoto); `git worktree list` → sólo `mm-piloto-3-v12` (`#944`, fusionado) y esta caja; `gh pr list --search PILOTO-3 --state open` → sólo `#948` (otro rótulo, `GEN2-TUBERIA-PREFLIGHT-CI-1`). Sin duplicado.
- **0.d** `tools/limpia_arbol.py --reporta`: 10 ramas locales ya fusionadas y vivas (entre ellas las de `#941` y `#944`), base al día, 1 rama remota fuera de política (`claude/epic-cori-4aiuak`, ajena). Sólo reporte.
- **data/raw** enlazado a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiada de `mm-piloto-3-v12` (gitignorados los dos). `tools/entorno.py`: `montado=SI`, `archivos_examinados=419`.
- **0-bis** `a6f5f399`, empujado; `git ls-remote` lo confirma. Sello de cuerpo `SELLADO_CUERPO` / `SELLO_COINCIDE candidato=archivo-entero`.

## 2 · `[SUPUESTO]` nadie abrió ENCIG 2025 por dos variables — censo por nombre, sin abrir nada

- Repo (`git ls-files | grep -iE "encig ?2025|encig25"`, fuera de encargos/notas): la celda-D `GOB…` y dos herramientas versionadas desde el 2/sep (`tools/medidor_gobierno_digital_encig25.py`, `tools/recorre_mordida_con_registro_encig25.py`). Ningún directorio `CALC-*ENCIG2025*` en `data/corrida0`.
- Disco (`find -L /home/pc0 -newermt 2026-09-20 -iname "*encig25*" -o "*encig2025*"`, excluyendo `.git`): 25 rutas, **todas** copias de esos mismos archivos versionados en los worktrees vivos (timestamps de checkout). Scratchpad vacío.
- Los dos directorios CALC en `mm-piloto3-c23`, `mm-piloto-3-v12`, `Modelado-Mexicano` y `mm-adq`: sólo `spec.yaml`, `.py`, la copia inmutable `fp399-firmada-826bf3a1.tsv` y `__pycache__` (del pytest de `#944`). Cero salidas. → no es PARO (h).

## 3 · P0 — las cuatro, crudas

1. `cd forense/prereg-caja && sha256sum -c GOB-gobierno-digital-exe15-spec-v1_1.sha256` → `OK`.
2. `python3 -m pytest tests/test_piloto3_v11.py -v` → **7 passed in 22.45s**, incluida `test_b_oro_2023_reproduce_los_sellados`.
3. `python3 tools/corrida0.py preflight CALC-GOB-DIGITAL-EXE-EMISIONES-0002` → **`PRE-FLIGHT: VERDE`**; `spec_md_sha256 [EN-MAIN-COINCIDE] 62d8d07d…`; 5/5 inputs `COINCIDE`, entre ellos `encig25_base_datos_csv` `raiz=data_raw`, `47daf2f7…`, 37 624 925 B; `script_blob_sha256 05d4c205…`; 565 ids de resultados; `[SIN-SELLO-PREVIO]`.
4. `_cuenta_gen2_resuelto` (`tools/corrida0.py:3736`) sobre `_lee_decisiones()` → `('SI', 'decision de mesa (decisiones.tsv): cuenta_gen2=SI · sea cual sea el veredicto (firma de contador del piloto 3, heredada por FP-407 c)')` para **ambos** CALC (`decisiones.tsv:184-185`, escritas por `#944`).

## 4 · El bloqueo, crudo

`time python3 tools/corrida0.py run CALC-GOB-DIGITAL-EXE-EMISIONES-0002` (preflight interno VERDE, idéntico al de §3) →

```
RUN CALC-GOB-DIGITAL-EXE-EMISIONES-0002
RUN: FALLO -- nada se sella:
  RESULT-GOB-EXE15-2025-18-29-HASTA-PRIMARIA-C1A-P-IC-LO: valor_null_sin_NO-ESTIMABLE_permitido
  RESULT-GOB-EXE15-2025-18-29-HASTA-PRIMARIA-C1A-P-IC-HI: valor_null_sin_NO-ESTIMABLE_permitido
  … (los 16 pares C1A-P-IC-LO / C1A-P-IC-HI, una pareja por celda: 32 ids) …
  RESULT-GOB-EXE15-2025-60-96-HASTA-PRIMARIA-CONTROL-C2COMP-P: valor_null_sin_NO-ESTIMABLE_permitido
  RESULT-GOB-EXE15-2025-60-96-HASTA-PRIMARIA-C2-VS-CONTROL-ABS: valor_null_sin_NO-ESTIMABLE_permitido
  RESULT-GOB-EXE15-2025-60-96-SECUNDARIA-CONTROL-C2COMP-P: valor_null_sin_NO-ESTIMABLE_permitido
  RESULT-GOB-EXE15-2025-60-96-SECUNDARIA-C2-VS-CONTROL-ABS: valor_null_sin_NO-ESTIMABLE_permitido
  RESULT-GOB-EXE15-2025-60-96-MEDIA-SUPERIOR-CONTROL-C2COMP-P: valor_null_sin_NO-ESTIMABLE_permitido
  RESULT-GOB-EXE15-2025-60-96-MEDIA-SUPERIOR-C2-VS-CONTROL-ABS: valor_null_sin_NO-ESTIMABLE_permitido
  RESULT-GOB-EXE15-2025-60-96-SUPERIOR-CONTROL-C2COMP-P: valor_null_sin_NO-ESTIMABLE_permitido
  RESULT-GOB-EXE15-2025-60-96-SUPERIOR-C2-VS-CONTROL-ABS: valor_null_sin_NO-ESTIMABLE_permitido

real 0m13.760s
```

Exactamente **40** líneas: 32 (A) + 8 (B). Ningún otro problema de `_valida_outputs` (faltantes, sobrantes, tipo, rango): los otros 525 RESULT pasaron la validación. Después: `git status --porcelain` vacío; `ls data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/` = `__pycache__ fp399-firmada-826bf3a1.tsv medidor.py spec.yaml`.

## 5 · Diagnóstico por lectura — nada se editó

**(A) 32 ids — `permite_no_estimable` ausente para un `null` que la spec sí prevé.**
- `medidor.py:416`: `f"{base}-C1A-P-IC-LO": None, f"{base}-C1A-P-IC-HI": None` — por la spec v1.1 (C1a = compuesto con marginales 2023, punto sellado, «IC NO-DERIVABLE (sin réplicas selladas)»), citado también en la celda-D.
- `medidor.py:460` (autodeclaración) y `spec.yaml`: `{id: …-C1A-P-IC-LO, tipo: proporcion, unidad: "NO-DERIVABLE (null)"}`; las claves del resultado son sólo `id, tipo, unidad`. Cero `permite_no_estimable` en las 565 declaraciones.
- `tools/corrida0.py:1949-1952`: `if valor is None: if not r.get("permite_no_estimable"): problemas.append(f"{rid}: valor_null_sin_NO-ESTIMABLE_permitido")`.

**(B) 8 ids — la banda 60-96 del control no existe con ese nombre en el CALC sellado.**
- `medidor.py:55` `EDAD_BANDAS … ("60-96", 60, 96)`; `:74` `PREFIJO_CONTROL = "RESULT-C2COMP-ADOPTA-ENCIG2025-LUZ-EDADXESCOLARIDAD"`; `:355` `"control": ctl.get(f"{PREFIJO_CONTROL}-{a}-X-{b}")`.
- `data/corrida0/CALC-C2-COMPUESTO-RESERVADAS-0001/resultados.json` (632 ids): para el par existen `…-EDADXESCOLARIDAD-18-29-X-…`, `…-30-44-X-…`, `…-45-59-X-…` y **`…-60-X-…`** (4 escolaridades). No hay `…-60-96-X-…`.
- `medidor.py:423-425`: `CONTROL-C2COMP-P = s["control"]` y `C2-VS-CONTROL-ABS = … if s["control"] is not None … else None`. Las 12 celdas de las otras tres bandas sí encontraron control (no aparecen en la lista).

**Por qué la prueba del congelador no lo atrapa.** `tests/test_piloto3_v11.py:98` `ctl = {f"{M.PREFIJO_CONTROL}-{a}-X-{b}": 0.55 …}` (fixture derivado de la clave del medidor: circular). `:246` la prueba de oro usa el `CTL` real pero no asevera control no nulo. Ningún test importa `corrida0._valida_outputs`. `preflight` hashea inputs y valida el esquema de la spec, no los valores.

**Latente en ADJUDICACION (para el v1.3, no disparó aquí).** `spec.yaml` de `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001`: 349 resultados, **0** `permite_no_estimable`. `adjudicacion.py` emite `None` en `-R-P`/`-DELTA-25` si R no es finita (`:202-204`), en `-D-PP` si falta punto (`:208`) y en **todo el bloque ΔMAE cuando no hay PUNTUADA suficiente** (`:239-242`), es decir, justo en el camino `FUERA-DE-SOPORTE` global que la spec declara como veredicto legítimo (§1 «si fallan ≥ 5 de 15»). Con el cableado actual, ese veredicto **no podría sellarse**. Es la misma clase de defecto que (A), un CALC más adelante.

## 6 · Contadores y perímetro

- `N_corridas_selladas` **+0**; `adoptados_activos` **sin mover**; `usos.tsv`, `corridas.tsv`, `resultados.tsv`, `replay-evidencia.tsv` **intactos**; `decisiones.tsv` intacto (las dos filas `cuenta_gen2=SI` siguen ahí, resueltas a SI, sin corrida a la que aplicarse).
- Celda-D `GOB.gobierno_digital.encig2025.edad_x_escolaridad`: **intacta**, `SPEC-CONGELADA`. Marcador: el par sigue `RESERVADA`; los otros dos cruces de ENCIG 2025 no se tocaron.
- Spec humana, sidecar, `medidor.py`, `adjudicacion.py`, los dos `spec.yaml`, `fp399-firmada-826bf3a1.tsv`, `tools/`, `tests/test_piloto3_v11.py`: **byte a byte iguales a `origin/main`** (perímetro ajeno).
- COMMIT-2, COMMIT-3a, COMMIT-3, veredicto, registro: **no existen** → `## NO-CORRIDO / RESERVAS` del encargo y NC de abajo.
- `NC-0451`–`NC-0454` (de `#941`): siguen ABIERTAS por objeto (ningún COMMIT-2/3 existe); sucesor re-apuntado al v1.3 (edición de la columna `sucesor`, nada más). `NC-0455`: **CERRADA por producto** — la firma de contador quedó asentada por `#944` en `decisiones.tsv:184-185` y aquí se comprobó que el registro la resuelve a `SI` (§3.4).
- Cero red, cero descargas, cero salidas en scratch (PARO d no aplica), cero sub-agentes.

## 7 · Sucesor — qué necesita el COMMIT-1 v1.3 (para quien lo congele; no es instrucción de mesa)

1. **EMISIONES `spec.yaml`:** `permite_no_estimable: true` en los 32 `…-C1A-P-IC-LO/HI` (la unidad ya dice «NO-DERIVABLE (null)»; es hacer explícito lo que la spec humana ya declara). `corrida0` lee la declaración del `spec.yaml`, no `medidor.esquema_resultados` (que sólo consumen los tests, por `id`): la llave va en el `spec.yaml`; si además se añade al esquema del medidor, es un cambio de `.py` que entra en la misma pregunta de mesa que el punto 2.
2. **Clave del control 60-96:** o un mapa de banda en el medidor (`"60-96" → "60"` sólo para `PREFIJO_CONTROL`), o declarar `permite_no_estimable` en los 8 y perder el control en 60-96. La primera conserva el control en las 16 celdas y toca **una línea de `medidor.py`** — que `FP-407 (b)` excluyó del «hereda verbatim»; por eso es pregunta de mesa (§8), no decisión del congelador.
3. **ADJUDICACION `spec.yaml`:** `permite_no_estimable: true` donde `adjudicacion.py` puede emitir `None` (`-R-P`, `-DELTA-25`, `-D-PP`, bloque `ΔMAE` por retador, `C1A/C1B-MAE-PP`), para que `FUERA-DE-SOPORTE` global sea sellable.
4. **Prueba del congelador (D-22):** además de pytest 7/7 y `preflight` VERDE, (i) `corrida0._valida_outputs(spec, out)` **vacía** sobre la salida de la prueba de oro (2023) y sobre el sintético, para los dos CALC; (ii) el fixture del control construido desde los ids **reales** de `CALC-C2-COMPUESTO-RESERVADAS-0001`, con aserción de 16/16 controles no nulos; (iii) un caso sintético `FUERA-DE-SOPORTE` global que pase `_valida_outputs` en ADJUDICACION. Las tres se pueden ejecutar sin abrir 2025.
5. **Quién congela:** otra sesión sin diseños A/B ni exposición a 2025. Esta sesión ejecutó el medidor sobre 2025 en proceso (una variable, sin ver cifras): por prudencia, que tampoco congele.
6. **CALC-id:** no cambian; la firma de contador (`decisiones.tsv:184-185`) sigue apuntando a los mismos ids y no habría que re-asentarla si mesa la hereda otra vez (`FP-407 (c)` fue por herencia explícita; aquí se vuelve a pedir).

## 8 · FP · NC · ADR

- **`FP-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-01`** (ABIERTA): mesa decide (a) quién congela el v1.3; (b) si el arreglo de la clave del control en `medidor.py:355` cuenta como cableado (recomendación: sí, una línea, con la prueba 4.ii) o si se pierde el control en 60-96; (c) si la firma de contador se hereda al v1.3 y a sus COMMIT-2/3a/3 sin re-asentar; (d) si D-22 adopta la prueba del punto 7.4 como obligatoria antes de congelar.
- **`NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-01`…`-05`**: P1 (COMMIT-2), P2 (COMMIT-3a), P3 (COMMIT-3), P4 (veredicto), P5 (registro y marcador), todas `PARO-PREMISA` o `DIFERIDO-A:` con sucesor nombrado. P6 (página para mesa) sí se ejecutó, en forma de PARO: es el §0.
- Raíz de acto (D-2): `a6f5` = commit del 0-bis `a6f5f399`.
- ADR: candidato contiguo re-derivado por `tools/cierre_acto.py` = **`ADR-585`** (máximo real 584; ninguna rama remota lo tiene redactado). Renumera quien fusiona segundo.

## 9 · Auditoría (§5 de las instrucciones) — tres líneas obligatorias

1. **Universo:** pago ordinario del servicio de luz (`N_TRA == 01`), unidad trámite. Aunque hubiera resultado, no se leería como conducta de personas ni como actitud hacia el Estado.
2. **Qué parece psicológico y es estructura:** el salto de once puntos entre olas es de nivel con el mismo instrumento (`CAMBIO-MENOR`, `NC-0355`). Si la interacción se transportara, diría que la *forma* de la brecha por edad y escolaridad es estable, no por qué; acceso, bancarización y cobertura del servicio explican canal antes que preferencia. Hoy no se sabe ni lo uno ni lo otro.
3. **Escala:** proporción de trámites, en pp; ΔMAE con IC. Nada de esto existe todavía; nada se compara contra el duelo nacional.

**Falsador del encargo, cumplido:** paró por una causa de cableado que ni `#944` ni el texto nombraron. D-22 tiene que exigir más que `preflight` VERDE: tiene que exigir que el conducto **selle** una salida de prueba.
