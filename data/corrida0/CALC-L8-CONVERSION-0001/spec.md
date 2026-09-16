# `CALC-L8-CONVERSION-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA
`forense/prereg-caja/L8-CONVERSION-PRESIDENCIAL-spec-v1_0.md`
(**`prereg-caja-L8-CONVERSION-PRESIDENCIAL`**,
`sha256 9a873e92a75e3f514f5890d63f30c377d28245ae07f5259c7393533264be1a6d`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1` tanda 2, 15/sep/2026, **NUBE**, sobre `d117ef1`.
**Releva:** `CORR-0016` → **3** `RESULT`: `RES-0050`, `RES-0051`, `RES-0052`.
Consumidor: `milpa/tramite.yaml:civico.participacion.concurrencia_presidencial_conversion`.

**CONGELADO en el COMMIT-1, antes de correr nada.**

---

## La única de las 19 que no necesita `data/raw`

Su insumo es un **artefacto versionado del repo**
(`data/l8-resultados-tipo-boleta-v1_0.json`, `sha256 30f3e16d…`, 43 545 bytes),
resuelto por `origen: repo`, no por manifiesto + raíz lógica. **Puede correr en
nube.** Que este acto no la corra es decisión del acto (contador cero
declarado), no una restricción del entorno.

## Qué mide

`p = clip(round(p0, 4) + round(beta_pres_pp/100, 6), 0, 1)` para tres anclas
de `p0`, derivadas de las **40 medias municipales** del JSON
(`por_transicion[].y_de_media` y `.y_a_media`, 20 transiciones × 2 patas):

| `RESULT` | ancla | `p0` | `p` |
|---|---|---|---|
| `RES-0050` | mínimo | 0.3051 | 0.345267 |
| `RES-0051` | máximo | 0.7104 | 0.750567 |
| `RES-0052` | media | 0.5797 | 0.619867 |

`delta = 0.040167` (de `estimador.beta_pres_pp = 4.016715486813227`).

## La decisión que decide si reproduce

**El ancla se redondea a 4 decimales ANTES de sumar.** Sin eso las tres celdas
salen `0.345263` / `0.750605` / `0.619830` — hasta `3.8·10⁻⁵` de diferencia,
tres órdenes por encima de cualquier tolerancia de flotante. Un `NO-REPRODUCE`
así sería **del redondeo, no de la cifra**. Va en el contrato
(`parametros.grano_ancla_decimales: 4`), no en la cabeza de quien escriba el
medidor. `A-GRANO-VERIFICADO` emite las dos variantes.

## Lo que NO hace

No toca microdato (no hay) · **no escribe el medidor** · no re-estima
`beta_pres` ni re-corre el panel de L8 · **no resuelve la inferencia
ecológica**: los tres `RESULT` salen rotulados `DERIVADO-ECOLOGICO` y ninguno
es causal · no propone la vía intermedia (`beta_int` contiene cero) · no adopta
nada a `milpa/`.
