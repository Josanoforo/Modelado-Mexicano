# ACTO GEN2-ADOPCION-COLA-5 · ningún RESULT se queda envejeciendo en la ventanilla

Nota de cierre. Encargo archivado verbatim en
`forense/encargos/2026-09-14-GEN2-ADOPCION-COLA-5.md` (0-bis `33f861b`),
con la adenda P4 (registro ENSANUT) recibida mientras el acto ya corría.

Redactado y ejecutado contra `origin/main = 38d25ad2` (`PR #745`) — verificado
al arrancar, `git fetch --prune` da `HEAD..origin/main = 0`, base al día.

## ARRANQUE

```
$ git fetch --prune && git rev-list --count HEAD..origin/main
0
$ git status --porcelain
(vacío)
$ git ls-remote --heads origin | grep -i adopcion
(sin salida)
$ python3 tools/limpia_arbol.py --reporta
A · worktrees vivos: 1
B · ramas locales ya fusionadas a origin/main y vivas: 1 (claude/festive-feynman-hc6nig)
C · base: HEAD esta 0 commits detras de origin/main (al_dia=SI)
D · NO-VERIFICABLE-SIN-GH (gh no disponible; verificado en su lugar con
    mcp__github__search_pull_requests / list_pull_requests: cero PR abierto
    que cite "adopcion" o el rótulo)
```

`data/raw` ausente (normal en clon fresco / nube), `numpy`/`pandas`/
`pyreadstat` ausentes — consistentes con la cabecera del encargo: **NO se
lanza en CAJA, cero microdato**. `python3 tools/entorno.py` pegado en el
0-bis del arranque de esta sesión.

**COMPUERTA: ninguna** — el propio encargo lo declara; no dispara
verificación.

## P1 · El censo de la ventanilla

```
$ python3 tools/corrida0.py status
N_resultados_gen2_pendientes_adopcion=5
N_resultados_gen2_adoptados_activos=16
```

Los 5 ids se derivan re-ejecutando la lógica de `status`
(`tools/corrida0.py:4178-4187`: `_resultados_citados_en(PROPUESTA) ∩
ids_sellados_gen2 − ids_adoptados`, donde `PROPUESTA =
milpa/tramite-ola5-propuesta-v0.yaml`):

| RESULT id | CALC origen | consumidor declarado (hoy) | estimando / grano | valor | reglas_impacto | decisión previa que lo toca |
|---|---|---|---|---|---|---|
| `RESULT-C1-POSEL-OFERTA-VEREDICTO` | `CALC-0001` (S12, CIDE-CSES 2015) | ninguno cargado en `milpa/tramite.yaml`; sólo citado `PENDIENTE-DE-MESA` en `milpa/tramite-ola5-propuesta-v0.yaml:3948-3950` (`civico.voto_alineado.clientelar_cses2015`) | contraste T1/T0 alineamiento tras oferta clientelar, por brazo | `NO-ESTIMABLE` (`p: null`) — `N-T0=0` en los 4 brazos, estructural (control positivo: código `2=No` existe y es mayoritario) | `R7.3`/`R7.6` — ninguna regla se mueve | `FP-357`/`ADR-422` (gobernanza:7419-7429): `NO-ESTIMABLE-CON-ESTA-FUENTE`, "no rescatable con `n`"; `D14`/`ADR-456` (CALC-0001-v2, 10/sep): descompone composición dentro de receptores **"sin mover R7.3/R7.6 ni cargar tasas al motor"` — cierra `NC-0064` sin sustituir el contraste |
| `RESULT-C1-POSEL-AMENAZA-VEREDICTO` | `CALC-0001` (idéntico, brazo amenaza) | igual que arriba (`milpa/tramite-ola5-propuesta-v0.yaml:3948-3952`) | contraste T1/T0 alineamiento tras amenaza clientelar | `NO-ESTIMABLE` (`p: null`), mismo defecto estructural | `R7.3`/`R7.6` — ninguna regla se mueve | igual que arriba |
| `RESULT-CTX-2019-P-ALTO` | `CALC-0002` (S13, LAPOP 2019/2021/2023, antecedente de `R10.3`) | ninguno cargado; sólo `PENDIENTE-DE-MESA` en `milpa/tramite-ola5-propuesta-v0.yaml:3978-3979` (`civico.contexto_institucional_victimas.lapop`) | proporción ponderada de índice de contexto institucional ALTO entre víctimas de extorsión, 2019 | `0.7862745098039216`, IC95 `[0.75, 0.823079]`, N=520 | `R10.3` (antecedente, no la regla) | `GEN2-E5-0` (gobernanza:7186-7188): "mide el **antecedente** de `R10.3`, no la regla — `R10.3` no se mueve"; `D15`/`ADR-456` (gobernanza:7907): D2-h "no evaluable con 2019/2021/2023... sólo reexamina ante fuente nueva con pregunta original **o decisión explícita sobre otro estimando**"; cierra `NC-0043` sin afirmar réplica |
| `RESULT-CTX-2023-P-ALTO` | `CALC-0002` (idéntico, ola 2023) | igual que arriba | proporción ponderada, 2023 | `0.7341176470588235`, IC95 `[0.684320, 0.782011]`, N=428 | `R10.3` (antecedente, no la regla) | igual que arriba |
| `RESULT-CTX-2021-P-ALTO` | `CALC-0002` (idéntico, ola 2021) | igual que arriba | proporción ponderada, 2021 | `None` — `NO-ESTIMABLE-INDICE-INCOMPLETO`: `aoj12` no existe en ese archivo (control positivo: `aoj11`/`b18`/`vic1ext`/`wt`/`upm`/`estratopri` sí están, entre 262 columnas) | `R10.3` (antecedente, no la regla) | igual que arriba |

`D1` (complementos, patrón `NC-0085`/`NC-0108`): **no aplica a ninguno de
los 5** — ninguno es `1 − primario` sobre un denominador recortado; los
cinco son mediciones directas (dos `NO-ESTIMABLE` estructurales, tres
proporciones directas de las que una también sale `NO-ESTIMABLE`).

Sonda de consumo del emisor, en solo-lectura, para los 5 (cero citas en
ningún lado del registro — consistente con `n_usos=0` en
`data/corrida0/resultados.tsv`):

```
$ for rid in RESULT-C1-POSEL-AMENAZA-VEREDICTO RESULT-C1-POSEL-OFERTA-VEREDICTO \
             RESULT-CTX-2019-P-ALTO RESULT-CTX-2021-P-ALTO RESULT-CTX-2023-P-ALTO; do
    grep -c "$rid" data/corrida0/usos.tsv; done
0
0
0
0
0
```

## P2 · Adopción o declaración, uno por uno

**`RESULT-C1-POSEL-OFERTA-VEREDICTO` y `RESULT-C1-POSEL-AMENAZA-VEREDICTO`
→ (b) NO-ADOPTABLE-POR-DECISIÓN.** Los dos traen `p: null` — no hay valor
que citar en ningún consumidor (el patrón línea-583/línea-613 cita un `p`
numérico; `NO-ESTIMABLE` no tiene precedente cargado en `milpa/tramite.yaml`
— cero coincidencias de `NO-ESTIMABLE` en ese archivo). Y aunque lo
tuviera: `FP-357`/`ADR-422` ya selló que el contraste **no es rescatable
con `n`** ("ausencia de medición, no evidencia contra R7.3/R7.6"), y su
propio sucesor sellado (`CALC-0001-v2`, `D14`/`ADR-456`, 10/sep/2026)
declara explícitamente que la descomposición por receptores que sí midió
algo **"sin mover R7.3/R7.6 ni cargar tasas al motor"**. Adoptar aquí
sería exactamente lo que `NC-0064` ya cerró sin hacer. Queda fuera de la
cola por decisión vigente, no por indecisión de este acto.

**`RESULT-CTX-2019-P-ALTO`, `RESULT-CTX-2023-P-ALTO`, `RESULT-CTX-2021-P-ALTO`
→ (c) DECISIÓN-DE-MESA, propuesta sin ejecutar.** Los tres miden el
**antecedente** de `R10.3` (contexto institucional entre víctimas), no la
regla — así lo sella `GEN2-E5-0` y lo reafirma `D15`/`ADR-456`: `R10.3` conserva
`[FUERTE]` con el `NO-DISCRIMINA` de 2004, y `D2-h` sigue `NO-CONSTRUIBLE`
con estas tres olas. **No existe hoy ningún consumidor** en
`milpa/tramite.yaml` cuyo `p` sea "proporción de contexto institucional
alto entre víctimas" — crearlo sería inventar un estimando/consumidor
nuevo, exactamente lo que `D15` reserva a "decisión explícita sobre otro
estimando". Además 2021 sale `NO-ESTIMABLE-INDICE-INCOMPLETO` (falta
`aoj12`), así que una serie de tres olas quedaría con un hueco estructural
en medio. **Pregunta exacta para mesa:** ¿se adopta "contexto institucional
alto entre víctimas de extorsión" (LAPOP 2019/2023, `RESULT-CTX-2019-P-ALTO`/
`RESULT-CTX-2023-P-ALTO`) como un estimando **descriptivo nuevo**, con su
propio consumidor en `milpa/tramite.yaml` y `uso_motor` marcado
explícitamente no-inferencial (mismo patrón que `rol_uso:
proxy_descriptivo` de `RESULT-ENCIG-MOR-B-P-*`), dejando 2021
`NO_COVERAGE` sin valor ni *fallback*? Si mesa dice sí, el vehículo de
adopción es una línea nueva en `milpa/tramite.yaml` citando los dos
`corrida0_resultado_id`, patrón línea-583, en un acto sucesor con esa firma
citada por objeto — no por inferencia de este PR. No se ejecuta aquí.

**Contador de pendientes, hallazgo declarado, no improvisado.**
`N_resultados_gen2_pendientes_adopcion` (`tools/corrida0.py:4200`) cuenta
TODO lo citado en `PROPUESTA` que está sellado y no adoptado — no
distingue "pendiente de que alguien lo cite" de "vetado por decisión
vigente" (nuestro caso `(b)`, los dos `C1-POSEL-*`). Por eso el contador
**no baja** con este acto aunque dos de los cinco queden resueltos: la
resolución es "declarado NO-ADOPTABLE", no "adoptado", y el índice de hoy
no tiene una tercera categoría para eso. Ver `NC-0168` (abajo) — la
distinción se propone, no se escribe a mano en `status()` sin firma.

## P3 · El cierre contable

```
$ python3 tools/corrida0.py status
N_corridas_requeridas=82
N_corridas_selladas=59
N_resultados_activos=207
N_resultados_sellados=3039
N_resultados_pendientes=207
dependencias_numericas_legacy_activas=191
N_resultados_gen2_sellados=2497
N_resultados_gen2_pendientes_adopcion=5
N_resultados_gen2_adoptados_activos=16
resultados_con_validacion_independiente=199
diferencias_materiales=0
no_corrido_abiertas=52
replays_legacy_sellados=4
corredores_envueltos_legacy=17
```

| contador | antes | después | por qué no se movió |
|---|---|---|---|
| `N_resultados_gen2_adoptados_activos` | 16 | 16 | Cero adopciones ejecutadas: los 5 candidatos resultan `(b)`×2 / `(c)`×3, ninguno con consumo probado nuevo. `P4` (`RES-0063`/`RES-0064`) tampoco cierra — ver abajo. |
| `N_resultados_gen2_pendientes_adopcion` | 5 | 5 | El índice no distingue "vetado por decisión" de "pendiente de mesa" (`NC-0168`); los 2 `(b)` siguen contando aquí hasta que el índice tenga esa tercera categoría. Improvisar la distinción a mano en este acto sería exactamente lo que el encargo prohíbe. |
| `dependencias_numericas_legacy_activas` | 191 | 191 | `RES-0063`/`RES-0064` (P4) seguirán `LEGACY-NO-DECLARADO` en `milpa/tramite.yaml:1303-1304` hasta que un acto en CAJA registre el `CALC` en `corrida0` (`NC-0169`) — ningún relevo las bajó en esta sesión. |
| `no_corrido_abiertas` | 52 | 55 | Este acto abre `NC-0167`/`NC-0168`/`NC-0169` (ver `## NO-CORRIDO / RESERVAS` del encargo). |

Ningún otro contador de `status` se mueve: este acto no mide, no re-corre
ningún `CALC`, no toca `data/corrida0/decisiones.tsv`.

## P4 (adenda) · Registro ENSANUT RES-0063/RES-0064

**Lo que ya existe, verificado (A.8):**

```
$ grep -n "RES-0063\|RES-0064" data/adq-demanda-activa-v1_0.json | head
5391:      "elemento_id": "RES-0063",
5466:      "elemento_id": "RES-0064",
```

El contrato (`data/adq-demanda-activa-v1_0.json`, ambos elementos) ya
declara `situacion: MEDICION_ADOPTADA_SIN_COBERTURA_CONTRATO_GEN2`,
`medicion_disponible_hoy: true`, `incertidumbre_pendiente: "sólo falta la
representación registral; el motor ya consume 0.777762"` (y `0.222238`
para `RES-0064`), `primer_faltante: REGISTRO_CORRIDA0`,
`ejecutor_siguiente: MOTOR_GEN2_REGISTRO`. El consumidor ya está sellado y
cargado — `milpa/tramite.yaml:1297-1325`
(`salud.vacunacion.disponible_ensanut2024`, `situacion: SELLADA`, `ADR-D2i`,
firma de mesa verbatim *"1, la cargamos"*, 7/sep/2026) — con los mismos dos
valores exactos (`razon_no_vacunacion_logistica: p=0.777762`,
`razon_no_vacunacion_no_logistica: p=0.222238`) y sin
`corrida0_resultado_id`/`corrida0_generacion` todavía: hoy cuenta como
`LEGACY-NO-DECLARADO`.

`NC-0165` (`ACTO GEN2-DEMANDA-CONCILIADA-Y-EJECUCION-NC0165`, `CERRADA`
11/sep/2026) es el antecedente histórico: su sucesor declarado es
exactamente `data/adq-demanda-activa-v1_0.json#elementos_gen2; cada
pendiente continúa por su contrato_id, primer_faltante y
ejecutor_siguiente` — este acto continúa esa cadena, no la reabre.

**Por qué no se completa "hasta emisión GEN2" en esta sesión.** Registrar
en `corrida0` (`tools/corrida0.py preflight/run/verify` → `registro
--escribe`) exige sellar un `CALC` nuevo, y `run` ejecuta de verdad
`medir()` del medidor declarado
(`tools/medidor_l17_vacunacion_disponible.py`), que abre
`adultos_ensanut2024_w.dta`/`adolescentes_ensanut2024_w.dta` vía
`pyreadstat` y usa `numpy`/`pandas` — los tres ausentes en este entorno
(`python3 tools/entorno.py`: `numpy=AUSENTE pandas=AUSENTE
pyreadstat=AUSENTE`, `data/raw` ausente). Fabricar a mano un `sello.json`/
`resultados.json` sin una ejecución real sería sellar sin medir —
exactamente lo que `A.13`/el propio motor de `corrida0` existen para
impedir ("la máquina registra, verifica y conecta mecánicamente lo que
efectivamente ocurrió"), y la cabecera de este mismo encargo restringe la
sesión a "cero microdato". Esto **no es una decisión científica nueva**
(la adenda es explícita en que no la pide) — es una ejecución de
infraestructura (`run`/`verify`/`registro`) que estructuralmente pertenece
a CAJA, igual que `CALC-0001`/`CALC-0002`/`CALC-0003` se sellaron fuera del
sandbox nube y sus artefactos se heredaron aquí ya sellados
(`forense/notas/2026-09-08-GEN2-E5-corridas-selladas.md:53`).

Queda declarado en `## NO-CORRIDO / RESERVAS` (`NC-0169`), con el paso
exacto que falta: un acto en CAJA con el corpus ENSANUT montado corre
`corrida0.py preflight`/`run`/`verify` sobre un `CALC` nuevo con
`tools/medidor_l17_vacunacion_disponible.py` (spec ya sellada,
`forense/prereg-caja/S7-L17-spec-v1_0.md`), sella los dos `RESULT`
(`razon_no_vacunacion_logistica`, `razon_no_vacunacion_no_logistica`),
corre `registro --escribe`, y añade `corrida0_resultado_id` +
`corrida0_generacion: GEN2` a `milpa/tramite.yaml:1303-1304` — sin volver a
decidir nada científico, exactamente como pide la adenda.

## Perímetro cumplido

Toca: `forense/encargos/2026-09-14-GEN2-ADOPCION-COLA-5.md` (0-bis) ·
`forense/notas/` (esta nota) · `forense/no-corrido.tsv` (`NC-0167`,
`NC-0168`, `NC-0169`) · `canon/gobernanza-v1_15.md` (ADR de cierre) ·
`canon/estado-programa-v1_12.md` (§L0) · `canon/registro-rotulos.tsv`.
**No toca** `milpa/*.yaml` (cero adopciones ejecutadas, así que cero
citas nuevas), `data/corrida0/decisiones.tsv`, ni ningún `CALC` sellado.

## Contador

Cero adopciones — declarado, no forzado. `N_resultados_gen2_adoptados_activos`
sigue en 16; los 5 candidatos originales quedan 2 `NO-ADOPTABLE-POR-DECISIÓN`
(cerrados aquí) y 3 `DECISIÓN-DE-MESA` (propuestos, abiertos); `RES-0063`/
`RES-0064` quedan `DIFERIDO-A` un acto de CAJA. Ninguna decisión científica
nueva, ninguna firma FP, ningún brazo de la tríada tocado.
