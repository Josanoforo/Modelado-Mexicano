# ENCARGO · ACTO GEN2-TUBERIA-ENRUTAMIENTO-PR-1 · CADA PR DICE, DERIVADO DE SU DIFF Y EN CI, QUÉ TIPO DE MERGE ES: SI ADOPTA CIFRAS, SI TOCA SUPERFICIE DE FIRMA, SI CAMBIA EL APARATO, O SI ES REVISIÓN ORDINARIA

**CABECERA** · redactado contra `fc13cdcc` (re-deriva al abrir; si `main` se movió no es PARO) · **ENTORNO: NUBE**, `cloud_default`, con credenciales de Git y publicación de PR; cero microdato; no usa la API de GitHub · una sola sesión, rama propia (D-17) · **MODO: ABIERTO** · **MODELO SUGERIDO: Opus** · **COMPUERTA: ninguna** (D-20) · **CONTADOR: `cuenta_gen2 = NO`** · vehículo: `/acto`.

**EL PR NO SE FUSIONA EN ESTE ACTO**: queda propuesto; mesa central fusiona.

**IDS.** Todo con raíz de acto: `ADR-<AAMMDD>-GEN2-TUBERIA-ENRUTAMIENTO-PR-1-<hhhh>-<NN>`.

---

## 1 · FIRMA DE MESA, verbatim (20/sep/2026)

> «Opción B. El Entregable 2 pasa a ser taxonomía de PR + regla de enrutamiento derivada del diff y verificable en CI. El auto-merge queda anotado como NO instrumentado, con su razón (9 % de los merges, ninguna de las renumeraciones), reevaluable si esa fracción crece.»

Es el **Entregable 2 del brief original de TUBERÍA**, firmado y nunca escrito. **La firma no está en el repo: este acto la asienta (A.12).**

## 2 · POR QUÉ — el defecto que atrapa (§1, D-14)

**El merge de mesa adopta cifras sin que el PR lo diga.** Por E.2, el merge del PR que trae un bloque sellado **es** la adopción, y por la firma del 17/sep un piso no vencido se adopta salvo veto. En la revisión del PR #943, que traía 2 939 resultados sellados, eso no estaba escrito en ninguna parte del PR: hubo que deducirlo del diff. `EJECUTADO` sobre los **198 PR** fusionados a `main` en 7 días, con una clasificación por diff:

| Clase | PR | Qué la dispara en el diff |
|---|---|---|
| **ADOPTA** | **44** (22 %) | añade un `data/corrida0/CALC-*/sello.json` |
| **FIRMA** | 33 | toca `milpa/`, `data/corrida0/decisiones.tsv` o el `spec.yaml`/`sello.json` de un CALC |
| **APARATO** | 38 | toca `.claude/commands/`, `.github/workflows/`, `tools/cierre_acto.py`, `tools/corrida0.py`, `tests/check.py` o `.gitattributes` |
| **REVISIÓN** | 83 | el resto |

Uno de cada cinco merges de la semana fue una adopción, y ninguno lo anunciaba. Esas cifras son **referencia para comparar, no valor esperado**: el acto las re-deriva con su propia regla.

`LEÍDO` · `.github/workflows/verify.yml` no escribe nada en el resumen del job (`GITHUB_STEP_SUMMARY`: cero usos). El CI clona con profundidad 1, sin la base: un job que necesite el diff contra `main` lleva su propio clonado (D-23), como hacen hoy los jobs `preflight-calc` y `guardas-res`.

## 3 · PIEZAS — resultado esperado, no receta

**P0 · 0-bis y firma.** Este encargo verbatim **desde el `.md` recibido**, con su sello de cuerpo. Chequeo de duplicado por contenido. **Asienta la firma de §1 verbatim**, y la línea del auto-merge **NO instrumentado** con su razón.

**P1 · La regla, en un solo sitio.** Una herramienta de un solo archivo que, dado un diff —lista de archivos con su estado—, devuelve:
1. **Todas las señales que dispara**, no sólo una: un PR puede adoptar y tocar aparato a la vez.
2. **La clase principal**, por precedencia: **ADOPTA > FIRMA > APARATO > REVISIÓN**.
3. **La instrucción de enrutamiento** de esa clase, en una línea que mesa lea sin abrir el diff:
   - **ADOPTA** — *«Tu merge adopta N corridas selladas (E.2): comprueba su asiento de replay y, si son pisos, ésta es tu ventana de veto.»*, con N y los CALC contados del diff.
   - **FIRMA** — *«Toca superficie de firma de mesa: el PR debe citar la firma verbatim.»*, con los archivos que la disparan.
   - **APARATO** — *«Cambia el aparato: la suite en verde y el perímetro del encargo son la revisión.»*, con los archivos.
   - **REVISIÓN** — revisión ordinaria.

Las rutas que disparan cada señal viven en una tabla **dentro de esa herramienta**, cada una con una línea que diga por qué (D-15: un solo sitio). **La herramienta no falla por la clase**: la clase informa, no adjudica (D-16). Sólo falla si no puede leer el diff.

**P2 · En CI, a la vista de mesa.** Un **job propio** en `verify.yml`, con su clonado que traiga la base (D-23), que corre la herramienta sobre el diff del PR contra `main` y **escribe el resultado en el resumen del job** (`GITHUB_STEP_SUMMARY`), donde mesa lo ve en la pestaña *Checks*. Corre en `pull_request` y en `push` a `main`. Segundos.

**P3 · Pruebas.** Un test cableado en CI (D-21) con diffs sintéticos: uno por clase; uno que dispara dos señales y sale con la de mayor precedencia listando ambas; uno sin archivos; y uno que **adopta varios CALC** y los cuenta bien. Más la **re-corrida retrospectiva** sobre los PR fusionados a `main` en los 7 días previos al redactado, con su tabla en la nota: cuántos por clase, y **una línea por cada PR que la regla de este acto clasifique distinto que la de §2**, con la razón.

**P4 · Cierre.** Cascada, `python3 tests/check.py --baseline --parallel` en **LÍNEA BASE VERDE**, `## NO-CORRIDO / RESERVAS` al final, `## CONSUMIDO` con el PR real. **Y la prueba en vivo:** el resumen del job en el propio PR de este acto muestra su clase —que, por tocar `.github/workflows/`, debe ser APARATO—.

## 4 · CRITERIO DE «HECHO» — por comando, con salida cruda en la nota

1. La firma y la línea del auto-merge están asentadas.
2. La herramienta devuelve señales, clase y enrutamiento para los diffs sintéticos de P3, y el test está en CI.
3. El job nuevo escribe el resumen en el PR de este acto, con clase APARATO.
4. La re-corrida retrospectiva está en la nota, con cada discrepancia explicada.
5. Suite en LÍNEA BASE VERDE.

## 5 · LATITUD · PAROS · PERÍMETRO

**Latitud:** el cómo es tuyo —nombre de la herramienta, formato del resumen—. Si la re-corrida muestra que una ruta dispara mal una señal, se corrige la tabla y se declara. Un obstáculo reversible y barato se resuelve (D-19).

**PAROS — lista cerrada:** que la clase haga fallar el CI · instrumentar cualquier forma de auto-merge o de fusión automática · dar a un job permisos de escritura sobre el repo o sobre los PR · tocar los jobs existentes de `verify.yml` · abrir microdato · objetivo inalcanzable.

**Perímetro:** la herramienta nueva en `tools/` · su test en `tests/` · `.github/workflows/verify.yml` (**sólo** el job nuevo) · `forense/analisis/enrutamiento-pr-1/` (la re-corrida) · `forense/encargos/`, `forense/notas/`, `forense/hallazgos.md`, `forense/no-corrido.tsv` · lo que asienta la firma · y la cascada. Más D-21. **Si te encuentras escribiendo fuera de esta lista, PARA.**

## 6 · LO QUE NO HACE · SUCESORES

No fusiona nada, no etiqueta PR, no bloquea por clase, no decide nada por mesa. **Sucesor posible:** que `/revisa` lea la clase del resumen en vez de deducirla —se propone con evidencia de uso, no antes—.

## 7 · FALSADOR

Si en un mes mesa fusiona un PR de clase ADOPTA sin haber visto su enrutamiento, o la regla clasifica como REVISIÓN un PR que adoptó cifras, la herramienta no hace lo que dice.

## NO-CORRIDO / RESERVAS

*(A.14. Añadido al FINAL del encargo archivado; nada por encima de esta
línea se editó — es lo que mantiene válido el sello de cuerpo del 0-bis,
D-a6.)*

- **qué** — «**Sucesor posible:** que `/revisa` lea la clase del resumen en
  vez de deducirla —se propone con evidencia de uso, no antes—.» (§6,
  verbatim).
  **por qué** — `DIFERIDO-A: acto propio de /revisa, cuando haya evidencia
  de uso del job `enrutamiento-pr``. El propio encargo lo declara sucesor
  **posible** y condiciona su lanzamiento a evidencia de uso; hoy no existe
  ni una corrida del job en un PR real, así que la evidencia es cero y
  lanzarlo ahora sería construir sobre un supuesto.
  **impacto** — ninguno sobre los cinco criterios de «hecho» de este acto.
  `/revisa` sigue deduciendo la clase del diff exactamente como hasta hoy;
  no se degrada nada.
  **sucesor** — acto propio sobre `/revisa`
  (`NC-260921-GEN2-TUBERIA-ENRUTAMIENTO-PR-1-9a2c-01`, `SIN-ASIGNAR` a sesión).

Todo lo demás del encargo se corrió: P0, P1, P2, P3 (diffs sintéticos **y**
re-corrida retrospectiva) y P4, con los cinco criterios de «hecho»
verificados por comando en
`forense/notas/nota-2026-09-21-gen2-tuberia-enrutamiento-pr-1.md`.
Ninguno de los seis PAROS de la lista cerrada de §5 se tocó.

## CONSUMIDO

Ejecutado por el **ACTO `GEN2-TUBERIA-ENRUTAMIENTO-PR-1`**, 21/sep/2026,
entorno NUBE (`cloud_default`), Opus 5, rama
`claude/exciting-mccarthy-qcvxdv`, 0-bis `9a2ca8b3`.

**PR #965** — https://github.com/Josanoforo/Modelado-Mexicano/pull/965
(propuesto, **no fusionado por este acto**: el merge es de mesa central,
como el propio encargo ordena).

`ADR-260921-GEN2-TUBERIA-ENRUTAMIENTO-PR-1-9a2c-01` ·
`FP-260921-GEN2-TUBERIA-ENRUTAMIENTO-PR-1-9a2c-01` (la firma del 20/sep,
asentada) · `NC-260921-GEN2-TUBERIA-ENRUTAMIENTO-PR-1-9a2c-01`.
Nota de cierre:
`forense/notas/nota-2026-09-21-gen2-tuberia-enrutamiento-pr-1.md`.
