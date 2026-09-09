# `ACTO GEN2-C0-D-CORRECTIVO` — nota de cierre

**9 de septiembre de 2026 · CAJA (UBUNTU), Opus · rama `acto/gen2-c0-d-correctivo` · base `main = 631fcd7` (`PR #650`)**

Encargo archivado verbatim (0-bis A.3): `forense/encargos/2026-09-09-GEN2-C0-D-CORRECTIVO.md`.
`COMPUERTA: ninguna` — declaración explícita, no dispara verificación.

---

## 0 · El resultado, primero: las cifras se quedan, el destino deja de decir de más

> **`RESULT-C0D-VEREDICTO-PAREADA = NO-DISCRIMINA`** — **idéntico a `v2`**
> **`RESULT-C0D-ADJUDICACION-HALLAZGO = INCONCLUSO`** — era `EXPLICADO-POR-METRICA`
> **`RESULT-C0D-ADJUDICACION-SUCESOR = NC-0077`** — era `NO-APLICA`
> **`RESULT-C0D-CONTROL-CIFRAS-INTACTAS = INTACTAS`** sobre **149 cifras**, tolerancia `0.0`

```
media d_i = |err_pp(L_CORPUS)| − |err_pp(L_SOLO)|  =  +4.6978 pp     ← idéntica a v2
IC95 bootstrap sobre celdas (seed 42, 10 000 réplicas) = [ −0.8022 , +11.2747 ]   ← idéntica
n_LL = 13                                                            ← idéntica
```

**De los 152 `RESULT` que `CALC-C0D-MARCADOR-v2` selló, cambiaron exactamente DOS, y los dos son de destino.** No es una afirmación: es lo que mide `RESULT-C0D-CONTROL-CIFRAS-INTACTAS`, con tolerancia `0.0` —**identidad exacta, no aproximación**— sobre las 149 cifras comparables. `verify` → **`REPRODUCE`**.

**La lectura canónica, adoptada verbatim de la revisión adversarial:**

> *«…el IC95 va de −0.80 a +11.27: la comparación no discrimina la dirección… Igualar el universo reduce la diferencia marginal; no demuestra que el resto esté explicado por la métrica.»*

El hallazgo del 8/sep **no queda explicado, y tampoco refutado: no se puede decidir con este `n` y este intervalo.** Eso es `INCONCLUSO`, y es estrictamente **menos** de lo que decía `EXPLICADO-POR-METRICA`.

---

## 1 · Qué se pidió y qué salió

| pieza | pedido | entregado |
|---|---|---|
| **P0** | commitear verbatim la revisión adversarial de Astra | **NO CORRIDO — `PARO-PREMISA` (`NC-0082`).** El texto verbatim **no llegó**: no venía en el mensaje que lanzó el acto, no está en el árbol, y `PR #649` no tiene comentarios (§5). Ninguna otra pieza dependía de él. |
| **P1** | spec `v1.2` + medidor sucesores, ramas exhaustivas sin `else`, primaria no vetable, sucesor separado del signo, guardia de identidad | **HECHO, entero.** `prereg-caja-C0D-MARCADOR` **v1.2** (`COMMIT-1`), `sucesora_de: v1_1` |
| **P2** | `CALC-C0D-v3` sobre los mismos 260 insumos, cifras permanecen, falsadores ejecutados | **HECHO, entero.** 162 `RESULT`, `verify` **REPRODUCE**, `CIFRAS-INTACTAS`, **siete falsadores en verde** (§3) |
| **P3** | corrección por sucesión: enmiendas fechadas, `n=14→13`, lectura canónica verbatim, sin prueba de equivalencia | **HECHO, entero.** Enmiendas en la nota de `PR #649` y en `ADR-426`, ambas **por anexión** (§6, §7) |

---

## 2 · El defecto estaba en el CÓDIGO, y se verificó línea a línea antes de tocar nada

El encargo traía una premisa verificable —*«`medidor.py:378-385` reproduce la escalera exacta»*— y se comprobó **contra el código que corrió**, no contra la prosa. Verbatim de `data/corrida0/CALC-C0D-MARCADOR-v2/medidor.py:373-385`:

```python
    if diverge or out["RESULT-C0D-CONTROL-CORRESPONDENCIA"] != "CORRESPONDE":
        adj = "NO-ADJUDICA-POR-CONTROL"
    elif veredicto == "NO-ESTIMABLE-POR-COBERTURA":
        adj = "NO-ESTIMABLE-POR-COBERTURA"
    elif (not identicos) and (rank_marginal != rank_comun):   # 378 ← veto de universo
        adj = "EXPLICADO-POR-UNIVERSO"
    elif veredicto == "NO-DISCRIMINA":
        adj = "EXPLICADO-POR-METRICA"                          # 381 ← explica lo inconcluso
    elif veredicto == "CORPUS-ESTORBA":
        adj = "CONFIRMADO-CON-ALCANCE"
    else:
        adj = "EXPLICADO-POR-METRICA"                          # 385 ← el else mudo
```

**La premisa se reprodujo exacta, en las líneas exactas.** Los tres defectos:

**(a) Veto de universo.** La línea 378 se evalúa **antes** de mirar la pareada. La primaria es `L_SOLO ↔ L_CORPUS` sobre `U_LL`: misma celda, mismo `R`, misma ventana, mismo modelo, y la única diferencia es el corpus. **`M` no participa en ella** — y sin embargo el orden de los tres `MAE` podía vetarla. **En el caso real no llegó a disparar** (`RESULT-C0D-DIAGNOSTICO-UNIVERSO = ORDEN-ESTABLE`: los universos difieren, el orden no cambia), pero **estaba latente**: con `ic_lo > 0` y un orden cambiado, `v2` habría archivado como artefacto de universo un intervalo que excluye cero.

**(b) `NO-DISCRIMINA → EXPLICADO-POR-METRICA`.** La línea 381 llama *explicado* a lo que la 380 acaba de reconocer como *no discrimina*. Un IC95 que cruza cero dice **no sé de qué lado está**; `EXPLICADO` dice **ya sé por qué pasaba lo que se veía**. Lo segundo no se sigue de lo primero, y el token es lo que viaja al ADR y a `estado-programa`.

**(c) El `else` mudo.** Las líneas 384-385 no son una rama: son el resto. Y en ese resto caía exactamente un caso — `CORPUS-AYUDA` (`ic_hi < 0`), la **refutación inequívoca** del hallazgo y la confirmación directa de D-2 en su lectura literal. **El resultado más informativo que este marcador puede producir salía rotulado como el más neutro.**

### La corrección, en `v1.2` §5

```python
MAPA_ADJUDICACION = {
    "CORPUS-ESTORBA": "CONFIRMADO-CON-ALCANCE",
    "CORPUS-AYUDA":   "REFUTADO-CON-ALCANCE",
    "NO-DISCRIMINA":  "INCONCLUSO",
}
```

Dos guardias de insumo por delante (`NO-ADJUDICA-POR-CONTROL`, `NO-ESTIMABLE-POR-COBERTURA`) y luego el **diccionario**. Sin `else`, sin destino por defecto: una clave ausente **levanta excepción y para la corrida**.

**Y la prueba estructural de que (a) está cerrado no es una promesa, es una firma:**

```
_adjudica(veredicto, convergencia, correspondencia, posteriores, sucesor)
```

**La función de adjudicación no recibe el ranking, ni los universos, ni los marginales.** No puede vetarse con lo que no tiene.

---

## 3 · Los falsadores, EJECUTADOS y sellados — no argumentados

El mapa es código, y se falsa corriéndolo. Siete casos **sintéticos y ajenos al dato observado**, con su valor esperado **congelado en `spec.yaml` antes de correr** (`parametros.falsadores_pre_declarados`). Uno solo en rojo **para la corrida**.

| `RESULT` | obtenido | esperado |
|---|---|---|
| `FALSADOR-A-VETO-UNIVERSO` | `CONFIRMADO-CON-ALCANCE` | ✔ la primaria manda; el ranking de `M` no la veta |
| `FALSADOR-B-CORPUS-AYUDA` | `REFUTADO-CON-ALCANCE` | ✔ rama propia, no el `else` |
| `FALSADOR-C-NO-DISCRIMINA` | `INCONCLUSO` | ✔ el caso real |
| `FALSADOR-D-CONTROL` | `NO-ADJUDICA-POR-CONTROL` | ✔ la guardia de insumo precede |
| `FALSADOR-E-COBERTURA` | `NO-ESTIMABLE-POR-COBERTURA` | ✔ la guardia de cobertura precede |
| `FALSADOR-F-EXHAUSTIVO` | `LEVANTA-EXCEPCION` | ✔ no hay destino por defecto |
| `FALSADOR-G-SUCESOR-SIN-SIGNO` | `NC-0077` | ✔ el sucesor no depende del signo |

**`A` y `B` son los dos contraejemplos de la revisión adversarial.** Que estén en verde y sellados es la diferencia entre *decir* que el defecto está cerrado y *mostrarlo*.

---

## 4 · El control que separa «corregí el mapa» de «volví a medir hasta que saliera otra cosa»

Este acto se redactó **conociendo el resultado de `v2`**, y eso está declarado sin adorno en `spec.yaml::etiquetas.contaminacion_declarada` (ADR-46). Precisamente por eso la spec **congela, antes de correr**, que ninguna cifra puede moverse:

- Los **260 insumos** de `v2` viajan **byte-idénticos** — mismos `id`, mismas rutas, mismos `sha256`. Verificado el día del acto **antes** de escribir la spec: **0 discrepantes de 260**. El insumo 261 es `IN-V2-RESULTADOS`, **de control**, que ninguna medición lee.
- Mismos estimadores, mismos parámetros de bootstrap, y los `scope_id` **conservan el sufijo `c0d_v1_0` a propósito**: cambiarlos cambiaría la semilla derivada y por tanto las cifras.
- `RESULT-C0D-CONTROL-CIFRAS-INTACTAS` compara con **tolerancia `0.0`** y `MOVIDAS` **PARA la corrida**.
- `RESULT-C0D-CONTROL-N-CIFRAS-COMPARADAS = 149`, para que «`INTACTAS`» no pueda leerse sin su `n` (A.13): un control que compara cero cifras y dice `INTACTAS` no es un control.

**Y la dirección de la corrección es la que hace que no sea sospechosa: va hacia MENOS.** Retira una afirmación que el intervalo no sostenía. Las cuatro ramas de §4 —las que miran el intervalo— **no se tocaron**, y el dato observado sigue cayendo en la misma.

---

## 5 · P0 no se corrió, y por qué — `PARO-PREMISA` (`NC-0082`)

El encargo manda commitear verbatim la revisión adversarial en `forense/notas/…REVISION-ADVERSARIAL-PR649-astra.md` con procedencia declarada. **El texto verbatim no llegó.** Lo que se buscó, con el comando a la vista (A.13):

```
ls forense/notas/ | grep -i astra
  → 2026-09-08-cierre-escalamiento-lateral-astra.md            (ajena, otro objeto)
  → 2026-09-09-PROPUESTA-GOBIERNO-DECISIONES-PENDIENTES-astra.md (ajena, ejecutada por PR #650)
gh pr view 649 --json comments   → cero comentarios
```

**Un texto verbatim no se reconstruye de memoria ni de paráfrasis**: escribirlo sería fabricar justamente la procedencia que el paso existe para asentar. Lo que **sí** queda asentado y es verbatim: los fragmentos que el propio encargo trae —incluida la lectura canónica que P3 adopta y la descripción de la escalera—, archivados por 0-bis A.3. Y la descripción **se verificó contra el código** (§2), que es la comprobación que el encargo mismo pedía.

**Ninguna pieza de P1, P2 ni P3 dependía de tener el texto completo, y las tres se ejecutaron enteras.**

---

## 6 · `n = 14 → 13`, corregido en el enunciado y no en las cifras

§0 y §2 de la nota de `PR #649`, y `ADR-426`, dicen *«Sobre estas 14 celdas `M` le gana a `L` con corpus y sin corpus»*. **El enunciado correcto es `13`.** Las dos secundarias se calculan sobre el universo común:

```
RESULT-C0D-PAREADA-SEC-LSOLO-M-N    = 13
RESULT-C0D-PAREADA-SEC-LCORPUS-M-N  = 13
RESULT-C0D-N-UNIVERSO-COMUN         = 13     (CIV-M-04 tiene L_CORPUS y no L_SOLO)
```

**Las cifras `+7.2287` y `+11.9265` y sus IC no cambian** —siempre se calcularon sobre 13—; lo que se corrige es la frase que las acompaña. **El marco tiene 14 celdas; la comparación tiene 13.** Y lo que sobrevive al pareo sigue en pie: `|L_SOLO| − |M| = +7.2287` IC95 `[+0.7499, +16.6527]` y `|L_CORPUS| − |M| = +11.9265` IC95 `[+4.1377, +21.3208]` — **`M` le gana a `L` con corpus y sin corpus.**

---

## 7 · El sucesor de alcance se separa del signo, y `NC-0077` se REUTILIZA

`v1.1` ataba el sucesor a `CONFIRMADO-CON-ALCANCE`, de modo que **sólo una confirmación podía nombrarlo**. Es la condición equivocada: **el alcance limita a los tres destinos por igual**, porque el corpus que estaba delante del corredor es el mismo cualquiera que sea el signo del intervalo.

`v1.2` §5.4 vuelve a la condición **material** del encargo original: se nombra sucesor si entró corpus después de la ventana de captura. Entró — **435 payloads**, la misma cifra que `PR #649` ya medía. `RESULT-C0D-ADJUDICACION-SUCESOR = NC-0077`.

**`NC-0077` se reutiliza y no se duplica: cero deuda nueva por este concepto.** Lo que cambia es su estatuto: deja de ser *«deuda que este veredicto no exige»* y pasa a ser **el sucesor que el alcance nombra**. Su fila lleva la enmienda fechada, sigue `ABIERTA`, y su texto original no se reescribe.

---

## 8 · Contador: NO se mueve, y por las mismas dos razones estructurales

**(1) No viajaba firma.** El encargo condicionó: *«`cuenta_gen2` viaja como firma en el lanzamiento (estándar de siempre) o no cuenta y se dice»* — no viajaba ninguna. **Esto es el decirlo.** `data/corrida0/decisiones.tsv` **no se toca**: escribir ahí sería falsificar una firma de mesa.

**(2) Y ésta no la levanta ninguna firma sola.** La regla `E.1` clasifica `CALC-C0D-MARCADOR-v3` **`envuelto_legacy = SI`**, derivado por el comando de la casa y no por opinión, porque sus insumos **son** los artefactos GEN1 del duelo. `cuenta_gen2 = NO`. Es estructural: un marcador GEN2 de un duelo GEN1 es un corredor envuelto.

**Único contador que se mueve: `corredores_envueltos_legacy` 10 → 11.**

**`FP-368`, y por qué es fila propia y no glosa de `FP-367`.** `FP-367` nombra `CALC-C0D-MARCADOR-v2` **y nada más**, y `v2` quedó `SUPERADO→v3`. Por el estándar `FIRMA-CONTADOR` (autoridad, fecha, **objeto**), una firma sobre `v2` **no alcanza a `v3`** — leerla como que sí lo hace es el defecto *«la compuerta se verifica por producto, no por rótulo»*. `FP-368` absorbe las dos preguntas de `FP-367` **sin cambiarles una coma**, con el objeto actualizado, y **nada queda huérfano**: si mesa firma, `FP-367` cierra con la misma firma por objeto superado; si declina, cierran juntas.

---

## 9 · Suite

Con **`TZ=UTC`**: al arrancar **`3 FAIL · 662 WARN`**, al cerrar **`3 FAIL · 664 WARN`** — **`LÍNEA BASE: VERDE` en ambas**. Los tres `FAIL` son los mismos heredados (`T06` ×2, `T08` ×1), **ninguno en el perímetro**: **este acto no agrega ni quita un solo `FAIL`.**

**El `+2` de WARN es deuda declarada, no defecto introducido**, y sale exactamente de las dos filas que este acto abre: `T34 T-NO-CORRIDO` 39 → **40** (`NC-0082`; `NC-0081` nace `CERRADA` y no cuenta) y `T22 T-FIRMAS` 51 → **52** (`FP-368`). **`T35 T-REPRO` no se mueve — 443 → 443**, coherente con §8: el marcador no cuenta como GEN2, así que sus 162 `RESULT` no entran al universo `SELLADA-SIN-ADOPTAR`.

**Un `FAIL` que apareció y se cerró dentro del acto, dicho y no escondido.** `T22` marcó en rojo el encargo archivado y `forense/no-corrido.tsv`: los dos traen el marcador `PENDIENTE de mesa` y **ninguna fila abierta de `firmas-pendientes.tsv` los citaba en su `dónde`**. No se silenció tocando `tests/check.py` —que además está **fuera del perímetro**—: se corrigió por la vía que el propio test nombra primero (A.12), haciendo que **`FP-368` cite los dos archivos**, que es donde su decisión pendiente está efectivamente asentada. El pendiente deja de vivir en un archivo que ninguna firma abierta reclama.

Sin `TZ=UTC` aparece un cuarto `FAIL` de `T-YAMEDIDO` sobre `forense/encargos/2026-09-08-GEN2-TRAMITE-BANDEJA.md`, un encargo **ajeno**: es el falso rojo por huso horario que `NC-0080` ya había declarado el día anterior, **reproducido aquí exactamente** y no un daño de este PR.

---

## 10 · Perímetro e higiene

- **Perímetro cumplido, y nada fuera.** `forense/prereg-caja/C0D-MARCADOR-spec-v1_2*` · `data/corrida0/CALC-C0D-MARCADOR-v3/**` + los TSV re-derivados · enmiendas fechadas en la nota de `PR #649` y en `ADR-426` · `forense/notas/` · `forense/no-corrido.tsv` (`NC-0077` citada) · `forense/firmas-pendientes.tsv` · 0-bis · cascada.
- **No se tocó** ningún sello de `v1`/`v2`, ninguna captura, ni se re-capturó nada: no se abrió `corridas-L/`, `corridas-M/`, `corridas-R/`, `agregado_v1_*.py`, `tools/emite_m.py`, `milpa/`, ni `decisiones.tsv`.
- **Las specs `v1.0` y `v1.1` y las corridas `CALC-C0D-MARCADOR` y `-v2` quedan intactas y verificando**, superadas por `repite_de`. La cadena la derivó el comando de la casa: `v1 SUPERADO→v2`, `v2 SUPERADO→v3`.
- Todos los `git add` **por ruta explícita**, nunca `-A` ni `.`.
- `registro --escribe` corrido **una sola vez**, después de sellar.
- **Prohibido y no hecho:** ninguna prueba de equivalencia, ningún umbral post-hoc, ninguna banda de indiferencia. `INCONCLUSO` es la ausencia de una conclusión, no la afirmación de que no hay diferencia.
- Un `.claude/` espurio apareció en `data/corrida0/CALC-C0D-MARCADOR-v3/` al ejecutar un comando con `cd` a ese subdirectorio; **se borró antes de cualquier `git add`** y no llegó a ningún commit.
