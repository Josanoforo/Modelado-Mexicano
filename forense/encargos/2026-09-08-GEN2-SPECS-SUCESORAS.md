# GEN2-SPECS-SUCESORAS · ACTO GEN2-SPECS-SUCESORAS · S6 v1.3 + S12 v1.1

- **SHA de redacción (base del encargo):** `351fd25f` (`PR #639`). **SHA de ejecución:** `origin/main = c5b89a9` (`PR #642`, `ACTO GEN2-SONDA-3 · ESCALAMIENTO-LATERAL`, fusionado) — main avanzó 9 commits entre redacción y arranque; re-derivado, no heredado (ARRANQUE paso 2).
- **Entorno asignado:** UBUNTU (caja, corpus montado), worktree nuevo desde `origin/main`, Opus.
- **Estado:** VIVO.

---

ENCARGO · ACTO GEN2-SPECS-SUCESORAS · S6 v1.3 + S12 v1.1 — las cuatro erratas del contrato se corrigen por la vía formal, y la prueba de robustez que las corroboradas se deben

Cabecera: CAJA (UBUNTU), Opus (re-corre microdato ENNViH ya en corpus) · COMPUERTA: ninguna · redactado contra origin/main = 351fd25f (PR #639) · candidatos: deriva con cierre_acto.py (retro-2, SONDA-3, CHECADOR-2 y TRÁMITE renumeran en paralelo). ORDEN DE CAJA: éste primero, C0-B detrás. CONCURRENCIA: los actos NUBE no tocan forense/prereg-caja/ ni data/corrida0/CALC-*.

FIRMA DE MESA, verbatim del 8/sep/2026: «si hagamos las specs sucesoras..» — resuelve FP-349, FP-350, FP-351 y FP-357 por la vía sucesora (E.3: el sello viejo no se edita; nace la versión que lo supera).

PIEZAS P1 · S6 v1.3 (sucesora_de: v1_2, dos diferencias declaradas en cabecera y ninguna más): (a) §1 alinea el texto al código ya corrido — «No» = código 3, cita ehh02cb_b3b.pdf pág. 8 (FP-349: el CALC ya lo hizo bien; el papel se pone al día); (b) §3.5 corrige la premisa falsa — loc/id_loc SÍ existen en c_portad.dta (FP-351) → conglomerado = localidad, y la reserva de IC-subestimado se levanta. Pre-declaración B-bis, escrita ANTES de correr: si C3/C4 conservan su intervalo sobre el umbral con el conglomerado correcto → corroboración secundaria robusta; si algún IC cruza → la fila baja a PROPUESTA y se dice; si C1 (primaria, hoy NO-DISCRIMINA) cambia de estado en cualquier dirección → es EL hallazgo y se reporta primero. El veredicto de la regla sigue gobernado por la cláusula de multiplicidad de la spec: C1/b3b decide; secundarias solas = PROPUESTA con reserva. P2 · CALC-0003-v3 (sucesor_de: CALC-0003-v2): única diferencia operativa = conglomerado localidad; COMMIT-1 congela con la frase de sello; run → sello → verify de las 6 filas efectivas; tabla comparativa v2↔v3 en la nota (misma escala, mismo universo — comparable sin enlace). El v2 queda SUPERADO en registro; bytes intactos. P3 · S12 v1.1 (sucesora_de: v1_0): incorpora al papel las premisas corregidas de FP-350 (peledip existe y fue el desenlace usado; nacional_preelectoral trae ítems post-electorales y no es réplica) y declara §4 NO-ESTIMABLE-CON-ESTA-FUENTE con la evidencia de FP-357 verbatim (el brazo control carece de desenlace por construcción del cuestionario; código 2=No existe y es mayoritario — no es rescatable con n). El contraste acotado-a-receptores cambia el estimando: si mesa lo quiere, es spec nueva con pregunta propia — se deja como fila de decisión, no se cuela aquí. CALC-0001 no se re-corre: sus 54 RESULT no cambian (el defecto era del papel, no del cálculo) — y se dice con esas palabras. P4 · Registro. FP-349/350/351/357 → EJECUTADAS con esta firma; los cuatro cierres con estampa de universo; una línea en hallazgos: «las cuatro salieron de abrir el codebook completo — A.15 pagándose por cuarta vez hoy».

PERÍMETRO: forense/prereg-caja/S6-L16-spec-v1_3.md (+sidecar) · S12-CSES-spec-v1_1.md (+sidecar) · data/corrida0/CALC-0003-v3/** · data/corrida0/{corridas,resultados,usos}.tsv re-derivados · data/corrida0/decisiones.tsv (fila cuenta_gen2 del v3 SOLO si la firma viaja en el lanzamiento — mismo estándar que FIRMA-CONTADOR: autoridad, fecha, objeto) · forense/{firmas-pendientes,no-corrido}.tsv · nota · 0-bis · cascada. No toca sellos previos, CALC-0001/0002, specs v1_0/v1_2 (quedan como historia). Frase del perímetro de siempre: si escribes fuera de la lista, PARA. CONTADOR: medición sí — un CALC sucesor sellado con cadena completa, y las corroboradas salen de esta corrida o más firmes o honestamente matizadas. ## NO-CORRIDO / RESERVAS obligatoria. Dos commits mínimo para P2; tercero declara, nunca corrige hacia atrás.

---

## A.8 · `ya_medido` (ADR-340) — corrido por el ejecutor, no heredado

*(Sección del ejecutor, **añadida al archivo, nunca dentro del texto verbatim del encargo**. El cuerpo del encargo de arriba no se edita.)*

Este acto **pre-registra y sella** specs sobre `R4.4` (`S6 v1.3`) y sobre `R7.3`/`R7.6` (`S12 v1.1`), de modo que A.8 aplica. Salida cruda, corrida sobre `origin/main = c5b89a9`:

```
$ python3 tools/ya_medido.py R4.4
  resuelto por canon: R4.4 -> id `salud.atencion.grave`
  milpa/tramite.yaml            (sin apariciones)
  milpa/tramite-ola5-propuesta-v0.yaml:3649  situacion=SELLADA-SIN-CARGA tier=SELLADA
        veredicto_Bbis=NO-DISCRIMINA  p=0.522295   id: salud.atencion.grave_ensanut2024
  milpa/tramite-ola5-propuesta-v0.yaml:3818  situacion=NO-ESTIMABLE-EN-v1_1 tier=SELLADA
        veredicto_Bbis=NO-ESTIMABLE  [NO-ESTIMABLE]  id: salud.atencion.grave_ennvih2002
  canon/modelo-decision-v4_0.md:747  tier=[MEDIA]

$ python3 tools/ya_medido.py R7.3
  resuelto por canon: R7.3 -> id `civico.voto.agencia_con_secreto`
  milpa/tramite-ola5-propuesta-v0.yaml:2284  SELLADA-SIN-CARGA  CONTRARIA  p=0.658228
        id: civico.voto.agencia_lapop2023
  milpa/tramite-ola5-propuesta-v0.yaml:2557  SELLADA-SIN-CARGA  CONTRARIA  p=0.321633
        id: civico.voto.agencia_con_secreto_encuci2020
  canon/modelo-decision-v4_0.md:761  tier=[FUERTE] (tabla histórica)
  canon/modelo-decision-v4_0.md:781  Enmienda D2-f -> tier vigente [MEDIA]

$ python3 tools/ya_medido.py R7.6
  resuelto por canon: R7.6 -> id `civico.voto.clientelar_si_observable`
  milpa/tramite.yaml            (sin apariciones)
  milpa/tramite-ola5-propuesta-v0.yaml:3398  SELLADA-SIN-CARGA  CONTRARIA-REPLICADA
        id: civico.voto.clientelar_si_observable_lapop2019
  canon/modelo-decision-v4_0.md:762  tier=[MEDIA]
  canon/modelo-decision-v4_0.md:783  Enmienda D2-g (ambos brazos, ninguno movido)
  ── veredicto de cada corrida (linea final del script) ──
  R4.4 -> MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-ENSANUT-resultados.md, L16,
          MAESTRA38-SELLO-3, S6, tramite-ola5-propuesta-v0.yaml
  R7.3 -> MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md,
          2026-09-07-MAESTRA38-CARGA-LAPOP-2-spec.md, L11, L12, L2, L9, N6,
          S12, S2, S4, canon§7, tramite-ola5-propuesta-v0.yaml, tramite.yaml
  R7.6 -> MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md,
          2026-09-07-MAESTRA38-CARGA-LAPOP-2-spec.md, L11, L12, L2, L4, L9,
          S12, S4, canon§7
```

**Ninguna de las tres es `NUNCA-MEDIDA`.**

**Lo que esta salida obliga a decir, y se dice:** las tres reglas **ya tienen medición** y ninguna de ellas se mueve por este acto. `R4.4` tiene dos entradas (`NO-DISCRIMINA` en `ENSANUT 2024`, `NO-ESTIMABLE` en `ENNViH 2002` `v1.1`) y las corridas de `CALC-0003-v3`/`v4` **no añaden una tercera al motor**: son el falsador de `S6` Rama A′, con la etiqueta `reglas_bajo_prueba: "R4.4 / salud.atencion.grave (NO se mueve por este CALC)"` heredada de la spec sellada. `R7.3` y `R7.6` conservan su `[MEDIA]` vigente (D2-f / D2-g): el `NO-ESTIMABLE-CON-ESTA-FUENTE` de `S12 v1.1` §4 es **ausencia de medición**, no evidencia contra ninguna de las dos, y §4.2 lo declara con esas palabras. **Ninguna regla del motor se re-clasifica, se carga ni se sella en este acto.**

---

## NO-CORRIDO / RESERVAS

| # | qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|---|
| **NC-0063** | «`data/corrida0/decisiones.tsv` (fila `cuenta_gen2` del v3 SOLO si la firma viaja en el lanzamiento — mismo estándar que `FIRMA-CONTADOR`: autoridad, fecha, objeto)» | **`DECISIÓN-DE-MESA-PENDIENTE`** | `N_resultados_gen2_sellados` se queda en **211** y `N_corridas_selladas` en **3**, pese a dos `CALC` sellados con `verify REPRODUCE`. Simulado en memoria, sin escribir el árbol: con la firma serían **226 (+15)** y **4**. La firma de este lanzamiento («si hagamos las specs sucesoras..») tiene por **objeto** las specs, no el contador; escribir la fila sería inventar una firma. | **`FP-362`** |
| **NC-0064** | «El contraste acotado-a-receptores cambia el estimando: si mesa lo quiere, es spec nueva con pregunta propia — se deja como fila de decisión, no se cuela aquí.» | **`DECISIÓN-DE-MESA-PENDIENTE`** | `S12` §4 queda `NO-ESTIMABLE-CON-ESTA-FUENTE` **sin sustituto**: `R7.3`/`R7.6` no reciben medición de CIDE-CSES 2015 por esta vía. Ejecutado tal como el encargo lo pidió — la fila existe para que la deuda no quede implícita. | **`FP-363`** |
| **NC-0065** | *(no pedido por el encargo; deuda descubierta al ejecutarlo)* una `S6 v1.4` que tabule en §3.4 el join contra `c_portad.dta`, de donde §3.5 toma `estrato` e `id_loc` | **`FUERA-DE-PERÍMETRO`** | El pre-registro sigue **sin declarar la llave** del join de diseño; cualquier `CALC` futuro que tome diseño de `c_portad` puede repetir el defecto de cobertura. `CALC-0003-v4` lo repara para **esta cadena**, no para la spec. El perímetro nombra `v1_3`, no `v1_4`, y una tercera diferencia habría roto el «dos y ninguna más» del propio encargo. | **`FP-361`** |
| **NC-0066** | «`run` → `sello` → `verify` de las 6 filas efectivas» — `CALC-0003-v3` queda SELLADA **con reserva**: los seis `N-SIN-CONGLOMERADO` > 0 | **`SUSTITUIDO-POR:CALC-0003-v4`** | Sus **IC95 no son usables como estimación**: el conglomerado `NaN` colapsado los estrecha artificialmente. **Qué absorbe el sustituto:** los 142 ids de `v3` con sus mismos valores salvo `IC`/`VEREDICTO` y los cinco textos que describen el join, más `RESULT-COBERTURA-DISENO`. **Qué queda huérfano:** de `v3`, nada — lo que aporta (el diagnóstico que descubrió el defecto heredado) no lo aporta `v4`, y por eso no se retira ni se re-corre (E.3; «tercero declara, nunca corrige hacia atrás»). **Sí queda huérfano** el estatus de `CALC-0003-v2`, que conserva `cuenta_gen2=SI` con la misma cobertura parcial nunca publicada — eso va en `FP-362`, no se resuelve aquí. | `CALC-0003-v4` (sellada en este mismo acto) + **`FP-362`** para el estatus de `v2` |
| **NC-0067** | *(no pedido; condición de cierre del `/acto`)* dejar la suite en VERDE **en esta caja** | **`NO-VERIFICABLE-AQUÍ`** | **El veredicto de `T-YAMEDIDO` depende del HUSO HORARIO del ejecutor, no del árbol.** El test compara la fecha del nombre del encargo contra `datetime.date.today()` en hora **local**: en esta caja (CST) hoy es `2026-09-08` y `forense/encargos/2026-09-08-GEN2-TRAMITE-BANDEJA.md` **entra**; en el runner de CI (UTC) hoy ya es `2026-09-09` y **queda excluido**. **Medido en la misma caja y en la misma sesión:** `python3 tests/check.py --baseline` → **ROJO** (1 entrada) · `TZ=UTC python3 tests/check.py --baseline` → **VERDE**. **Control adicional:** worktree limpio sobre `origin/main = 0763457`, sin un solo commit de esta rama, da la **misma única entrada** — tampoco es de este acto; y el CI de `main` tras `PR #644` salió `success`. **Dos ejecutores honestos con el mismo árbol leen veredictos distintos según su `TZ`, y esa ventana se abre todos los días.** | acto de aparato con `tests/` en su perímetro (anclar `T-YAMEDIDO` a UTC o a la fecha del commit, no a la hora local) |

**Diferencias declaradas contra la letra del encargo, ninguna omitida:**

1. **Se sellaron DOS `CALC`, no uno.** El encargo pidió «un CALC sucesor sellado con cadena completa». `CALC-0003-v3` salió con un defecto de cobertura que su propia guardia midió; la casa manda no corregir hacia atrás, así que un tercer commit congeló `CALC-0003-v4` y un cuarto lo corrió. Es **más** de lo pedido, no menos, y era la única forma de entregar el objeto real del encargo: reportar `v3` sola habría dicho «los IC se estrecharon» sabiendo que eso era un artefacto.
2. **La tabla comparativa de la nota es `v2↔v3↔v4`, no `v2↔v3`.** Misma escala, mismo universo, misma `seed` — comparable sin enlace, tal como el encargo pide, con una columna más.
3. **La pre-declaración `B-bis` vive en `CALC-0003-v3/spec.md` §5, no en `S6 v1.3`.** Decisión declarada, no olvido: el encargo exige «dos diferencias declaradas en cabecera y ninguna más» para la spec sellada, y una cláusula de lectura del re-corrido habría sido la tercera. Se congeló en el mismo `COMMIT-1`, antes de abrir un `.dta` para calcular, que es lo que el encargo pedía de ella («escrita ANTES de correr»).
4. **`S6 v1.3` corrige el código «No» en DOS sitios** (§1 y la cláusula `se_mueve_si` de §5, que repetía el `0`). Es el mismo hecho de codebook llevado hasta donde llegaba; la cuenta de diferencias no sube, y se dice en §0.5 para que nadie tenga que descubrirlo leyendo.
5. **`S12 v1.1` trae dos anotaciones de resolución** (§1 y §3) además de sus dos diferencias: citan lo que `CALC-0001` ya había resuelto de los cuatro «no confirmado sin abrir el `.sav`» de `v1.0`, **sin borrar** el texto que declaró la incertidumbre. Son citas, no cambios de criterio.
6. **La base de ejecución no es la del encargo.** Redactado contra `origin/main = 351fd25f` (`PR #639`); ejecutado sobre `c5b89a9` (`PR #642`), 9 commits después. Re-derivado, no heredado — ninguno de los 9 toca el perímetro.

---

## CONSUMIDO

Ejecutado por **`PR #645`** (`ACTO GEN2-SPECS-SUCESORAS · S6 v1.3 + S12 v1.1`), rama `acto/gen2-specs-sucesoras`, 8/sep/2026, **UBUNTU (caja)**, `ADR-422`.

**Productos sellados:** `forense/prereg-caja/S6-L16-spec-v1_3.md` (`e075356b…`) · `forense/prereg-caja/S12-CSES-spec-v1_1.md` (`31100ef8…`) · `data/corrida0/CALC-0003-v3/` (142 `RESULT`, sello `3b2399b1…`, `VERIFY REPRODUCE`) · `data/corrida0/CALC-0003-v4/` (143 `RESULT`, sello `b3845dba…`, `VERIFY REPRODUCE`).

**Firmas:** `FP-349`, `FP-350`, `FP-351`, `FP-357` → `EJECUTADAS`. `FP-361`, `FP-362`, `FP-363` abiertas.

**No fusionado por el ejecutor** — el merge es de mesa, y es la autorización, no un trámite.
