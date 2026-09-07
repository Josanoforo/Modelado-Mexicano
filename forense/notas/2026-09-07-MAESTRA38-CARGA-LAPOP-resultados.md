# ACTO MAESTRA38-CARGA-LAPOP · PROPAGA-FP316-FP315 — PARO por desajuste de terreno en las tres piezas, cero decisiones ejecutadas

Encargo: `forense/encargos/2026-09-07-MAESTRA38-CARGA-LAPOP.md` (archivado verbatim en el 0-bis). SHA declarado `693ea23`; base real de este acto `038ec4f` (`origin/main`, PR #564 `MAESTRA38-L2` + PR #565 `MAESTRA38-LOTE-ENSANUT` ya fusionados — COMPUERTA verificada por producto contra `origin/main`, cumplida). Entorno nube, sin `data/raw` (el acto no toca microdato).

**El ejecutor propaga una decisión dictada, no decide (ADR-76/79). Se encontraron tres puntos donde el encargo no cuadra con el árbol — se PARA en los tres, no se ajusta el texto para que cuadre.**

## 1 · Decisión (b): el id citado no es el que FP-315/FP-316 midieron

El encargo dicta: *"`civico.protesta.agravio_urbano_lapop2019` → `situacion: ACOTADA-CON-RESERVA` ... reserva: 'el corazón de la regla no se midió; lo estimable en LAPOP no discrimina' ..."*

Verificado contra `milpa/tramite-ola5-propuesta-v0.yaml`:

- `civico.protesta.agravio_urbano_lapop2019` (línea 2356) ya está `situacion: SELLADA-SIN-CARGA` desde la enmienda **D2-e** (firma de mesa 3/sep/2026, `ACTO MAESTRA37-N8`), `tier: MEDIA`. Es una pieza distinta y ya cerrada: mide **C1** (contraste contra rural) sobre una sola ola (2019), veredicto `AMBIGUA-ENTRE-INSTRUMENTOS` (n=65, numerador 7, cae por guardia). No tiene nada que ver con el hallazgo de `MAESTRA38-L5` que `FP-315`/`FP-316` narran.
- La pieza que sí corresponde al texto de la decisión (b) — tres olas LAPOP (2004/2006/2019), `C_completo` `NO-ESTIMABLE` en las tres con celda rural mínima **14/21/1** (`n_rural` de los tres contrastes `C_completo_2004/2006/2019`), la tensión C1-vs-C2 de `prereg-caja-S5-L5-spec-v1_0.md §3.1`/`§0.3` — es `civico.protesta.agravio_urbano_multiola` (línea 3449), hoy `situacion: PENDIENTE-DE-MESA`. La propia fila `FP-316` en `forense/firmas-pendientes.tsv` nombra correctamente esta pieza como `civico.protesta.agravio_urbano_multiola` en su punto (b) — el desajuste está en el bloque de decisión que llegó a este acto, no en el tablero de firmas.

Comando de verificación:
```
grep -n "situacion:" milpa/tramite-ola5-propuesta-v0.yaml | sed -n '1,999p' | grep -A0 -B0 ""
# fila 2356 → situacion: SELLADA-SIN-CARGA  # D2-e ...
# fila 3460 → situacion: PENDIENTE-DE-MESA  # ... falsador CORRIDO por ACTO MAESTRA38-L5 ... FP-316.
```

No se toca ninguna de las dos entradas. No se decide cuál es "la correcta" — esa lectura ya la tiene la propia `FP-316`, pero cambiar el id que la decisión de mesa dictó verbatim sería decidir, no propagar. `FP-315` **no se firma**: la resolución que el encargo le atribuye depende de ejecutar (b) sobre el id correcto.

## 2 · Decisión (a): la premisa "ya SELLADA por D2-f" no es cierta para las dos piezas gemelas

El encargo dicta que, tras retocar `referida_a`, no se toque `situacion` de `civico.voto.agencia_lapop2023` y `civico.voto.agencia_con_secreto_encuci2020` "sin tocar su `situacion` (ya SELLADA por D2-f)".

Verificado: ambas siguen `situacion: PENDIENTE-DE-MESA` (líneas 2287 y 2558). La enmienda **D2-f** (`canon/modelo-decision-v4_0.md:781`) selló el **tier que el motor consume** para `R7.3` en el canon — nunca escribió `situacion: SELLADA` en estas dos filas de la propuesta, que siguen abiertas. La instrucción de no tocar `situacion` es inofensiva de por sí (no pide ninguna escritura ahí), pero su justificación es falsa y se declara así en vez de dejarla pasar sin verificar.

## 3 · Decisión (a): `registro-rotulos.tsv` no registra IDs de regla (`R7.x`)

El encargo dicta: *"`registro-rotulos.tsv` gana R7.10 y R7.11."*

Verificado: la fila propia de `registro-rotulos.tsv` para la familia de espacios `N, R, H, S, U, D` dice explícitamente *"no derivado fila por fila en este acto"* para "Necesidades / fichas-reglas / hallazgos / se..." — este archivo censa rótulos de **actos y espacios** (`MAESTRA38-N14`, `E4a`, `D-1..D-6`, `ADR-NNN`, `FP-NN`, `TNN`...), no los IDs de regla del catálogo de `canon/modelo-decision-v4_0.md`. El mecanismo real que ancla IDs de regla (`R7.1`...`R7.9`) es el **registro congelado** del propio canon (`§7`, tabla de IDs) más `tests/validador_registro_ids.py`, que ancla cada ID por subcadena estable de su texto — no `registro-rotulos.tsv`.

Añadir `R7.10`/`R7.11` a `registro-rotulos.tsv` habría sido escribir en un archivo cuyo propio contenido declara que ese tipo de fila no le corresponde: el "no cuadra" más nítido de los tres.

## Consecuencia

Cero ediciones sustantivas de canon, propuesta o tablero en este acto. No se crean `R7.10`/`R7.11`, no se toca la fila de `R7.6`, no se escriben las enmiendas `D2-g`/`D2-h`, no se marca ninguna de las cinco entradas de la propuesta, `FP-315` y `FP-316` permanecen `ABIERTA`. El único commit sustantivo de este acto es el 0-bis (archivo del encargo verbatim) y este mismo reporte. `milpa/tramite.yaml` no se tocó: sigue en 20 entradas, verificado.

```
$ grep -c "^  - id:" milpa/tramite.yaml
20
```

**Mesa decide:** (i) si (b) debe leerse sobre `civico.protesta.agravio_urbano_multiola` en vez de `_lapop2019` — y de ser así, relanzar el encargo con el id corregido; (ii) confirmar o corregir la premisa de (a) sobre el estado de las dos piezas gemelas de `R7.3`; (iii) indicar el mecanismo correcto para registrar `R7.10`/`R7.11` si la partición de `R7.6` se sostiene (el candidato natural es el propio `§7` de `modelo-decision-v4_0.md` + `validador_registro_ids.py`, no `registro-rotulos.tsv`).
