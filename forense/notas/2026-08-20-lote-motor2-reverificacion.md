# Nota · LOTE-MOTOR2 — re-verificación M2/M4/M5, sello MOTOR-2, avance de `FP-26`

**Entorno:** NUBE (repo-only) · **Modelo:** Opus · **Gate:** `T-SELLO` fusionado (`PR #299`, `ADR-132` en el árbol) · **Fecha:** 20/ago/2026.

## 0 · Qué mueve

`FP-26` (`DISPARADOR-POSTBARRIDO`) es la fila `ABIERTA` más vieja del tablero. Su `DISPARADOR-B`
(`ADR-101(h)`) queda armado por el cierre de la fase semántica de `BARRIDO-2` (`ADR-108`/`ADR-109`,
`PR #268`, ya fusionado). La propia nota de cierre de `B2-SEMANTICO` (`forense/notas/2026-08-18-b2-semantico.md`
§6.2) deja escrito que la re-verificación `M2`/`M4`/`M5` — condición de `ADR-100(9)` — **"es de
dirección, no de este ejecutor"**. Este acto es esa re-verificación.

## 1 · T1 — Re-verificación `M2`/`M4`/`M5` contra el universo nuevo de `BARRIDO-2`

**Universo declarado (A.4):** el "universo nuevo de BARRIDO-2" que `ADR-100(9)` cita es
`data/curacion-universo/` — los durables regenerados y cerrados por `ACTO B2-SEMANTICO`
(commits C4-C6, `ADR-108`/`ADR-109`), gate material verde (`validate.py --barrido2-material
--require-complete` → `672/672`), muestra adversarial `39/39`, `§28` con 22 criterios verificados
por comando. Verificado hoy que sigue vigente y sin drift:

```
python3 tests/check.py --baseline
```
→ `23 FAIL · 138 WARN` — `LÍNEA BASE VERDE` (HEAD congelado `e24d033`), cero `--freeze`.

**Rótulo con prefijo (`T25`, per `registro-rotulos.tsv`):** la `M5` que este acto re-verifica es el
**HABITANTE 3 de 4** — "una de las seis M del sello del motor (M1-M6), `ADR-100`" — distinta de la
`M5` defecto de `RONDA-M:61`, del `M5` de `hallazgos.md:65`, y de `ADV1-M5` (`ADR-128(e)`). No se toca
ninguna de las otras tres. Mismo criterio para `M2`/`M4`: son las incisos (2)/(4) de `ADR-100`, no
los defectos homónimos de `RONDA-M`.

### M2 — Granularidad `D` (cortes por eje, tres ejes de hogar)

Dueño del sello por eje, per `ADR-100(2)`, es el catálogo de momentos (M4) en su commit 1 —
`milpa/catalogo-momentos-v0_1.md` §3. Sus cinco cortes son nativos del instrumento (ENIGH):
`segsoc` binario, `tam_loc.csv`, `est_socio.csv`, `celular`/`conex_inte` binario, `edad`/`residencia`
`PENDIENTE` (deuda declarada, `FP-53`). Comando — ¿algún corte referencia `data/curacion-universo/`?

```
grep -n "curacion-universo\|BARRIDO-2\|BARRIDO2" milpa/catalogo-momentos-v0_1.tsv milpa/catalogo-momentos-v0_1.md
```
→ una sola coincidencia, la propia cláusula que cita la condición de `ADR-100(9)` (línea 36 del `.md`,
narrativa, no dato). Cero cortes derivados del universo de `BARRIDO-2`.

**Veredicto M2: SOBREVIVE, sin cambio.** Los tres ejes de hogar (urbanización, ingreso, acceso
digital) y su cascada dependen del vector de atributos de `modelo §1.1.A` y del instrumento ENIGH,
dominio disjunto del universo material/semántico de `BARRIDO-2` (inventario de activos INEGI
internos). `milpa/src/celdas.py` sigue rechazando al construirse todo corte intra-hogar en los ejes
3/4/5 (`tests/test_motor_clases.py`, sin tocar por este acto).

### M4 — Catálogo de momentos como pre-registro

Universo declarado: las 22 filas de `milpa/catalogo-momentos-v0_1.tsv` deben resolver su
`necesidad_id` contra el libro de demanda (M5) y sus fuentes deben seguir siendo las que el catálogo
cita (`milpa/tramite.yaml`, `milpa/procedencia.yaml`, `forense/censo-estimabilidad-coeficientes-v1_0.md`,
`forense/hitoD-preregistro-v2_0.md`). Comando:

```python
import csv
cat = list(csv.DictReader(open('milpa/catalogo-momentos-v0_1.tsv'), delimiter='\t'))
nec = list(csv.DictReader(open('data/curacion-registro/necesidad-objeto-modelo.tsv'), delimiter='\t'))
nec_ids = {r['necesidad_id'] for r in nec}
missing = [r['id_momento'] for r in cat if r['necesidad_id'] not in nec_ids]
```
→ `filas catalogo: 22 · filas necesidad: 37 · momentos con necesidad_id no encontrado: []`. Las 22
filas siguen resolviendo, cero huérfanas.

**Veredicto M4: SOBREVIVE, sin cambio.** El catálogo no cita ni un archivo de `data/curacion-universo/`
(mismo `grep` de arriba, cero hits en dato). El pre-registro de `gobernanza:461` y los roles
`AJUSTE`/`HOLDOUT` sellados en su commit 1 (`385b626`) no dependen del universo material/semántico de
`BARRIDO-2` — dependen del instrumento ENIGH y del libro de demanda (M5), verificados intactos abajo.
La deuda nombrada §5 del catálogo (`S1 ≈ M5`, si el catálogo es capa de demanda del registro celda-D
de `ADR-68(a)` o artefacto hermano) sigue **abierta y sin adjudicar por este acto** — es una pregunta
de diseño ya declarada `bloqueante del sello` por `RONDA-M §5`, pero `ADR-100(4)` ya la nombró como
deuda conocida al firmar M4, y `ADR-100(9)` sólo condiciona M4 al universo de `BARRIDO-2`, no a esa
deuda. No cambia el veredicto de este inciso.

### M5 — Libro de demanda como fuente única

Comando — ¿el libro de demanda cita algún archivo de `data/curacion-universo/` como fuente de
verificación?

```
cut -f3 data/curacion-registro/necesidad-objeto-modelo.tsv | tail -n +2 | tr ';' '\n' | sort -u
```
→ cinco fuentes, todas ajenas a `BARRIDO-2`: `forense/censo-estimabilidad-coeficientes-v1_0.md` ·
`forense/hitoD-preregistro-v2_0.md` · `forense/notas/2026-08-08-barrido1.md` (BARRIDO **1**, acto
anterior y distinto) · `milpa/procedencia.yaml` · `milpa/tramite.yaml`. Cero referencias a
`data/curacion-universo/` o a `BARRIDO-2`.

**Veredicto M5: SOBREVIVE, sin cambio.** `necesidad-objeto-modelo.tsv` es la fuente única del curador
por diseño de instrumento (ENIGH + censo de estimabilidad), dominio disjunto del inventario de
activos INEGI internos que `BARRIDO-2` produce. Mismo hallazgo de dominio que `FP-10`/`FP-12` ya
midieron para `universo-puertas` (`forense/notas/2026-08-19-fusion-puertas.md`): `data/curacion-universo/`
es activos internos, no fuentes de instrumento de encuesta — cero columnas o llaves compartidas con
el libro de demanda.

### Conclusión de T1

Ninguna de las tres cambia frente al universo nuevo de `BARRIDO-2` — no porque el universo nuevo no
exista (existe, cerrado por `ADR-108`/`109`, gate verde), sino porque las tres M viven en un dominio
disjunto de lo que ese universo mide (activos INEGI internos vs. instrumento de encuesta + libro de
demanda propio del curador). Per `ADR-100(9)` verbatim: *"si no cambian, el sello procede sin volver
a mesa"*. Aplica. `M2`/`M4`/`M5` pasan de `CONDICIONADA` a firme, sin reabrir mesa.

## 2 · T2 — Sello MOTOR-2, `FP-01`..`FP-06`

Las seis ya estaban `FIRMADA` con `ejecutada_en = ADR-100` (`ACTO MESA-18AGO`, 18/ago/2026): la firma
de mesa por lote de `ADR-91` se ejecutó ahí. Lo que faltaba, y que este acto entrega, es la condición
que las tres `CONDICIONADA` (`M2`/`M4`/`M5`, incisos (2)/(4)/(5) de `ADR-100`) tenían pendiente por
`ADR-100(9)`: la re-verificación de T1. Con T1 resuelto SOBREVIVE×3, las seis M quedan firmes sin
excepción — `M1`/`M3`/`M6` ya lo eran (incondicionales, `DISPARADOR-A`), `M2`/`M4`/`M5` lo son ahora
(`DISPARADOR-B`, condición descargada). No se re-ejecuta nada material: no hay ADR que reabrir, no
hay archivo de `milpa/` que tocar — el sello ya estaba puesto en `ADR-100`, esto descarga su única
condición pendiente.

## 3 · T3 — `FP-26`, las ocho etapas, una por una con evidencia

| # | Etapa | Estado | Evidencia |
|---|---|---|---|
| 1 | Adjudicación `FP-10`/`FP-12` | ✅ EJECUTADA | `FP-10`: `ADR-115`, `ACTO FP10-PRECEDENCIA` (19/ago) — diff aplicado, `data/universo-puertas-2026-08-14.tsv` 122→106 filas, `forense/notas/2026-08-19-fp10-precedencia.md`. `FP-12`: `ACTO FUSION-PUERTAS` (19/ago) — no superada, dominios disjuntos, ningún archivo tocado, `forense/notas/2026-08-19-fusion-puertas.md`. |
| 2 | Re-verificación `M2`/`M4`/`M5` y sello `MOTOR-2` (`FP-01`..`06`) | ✅ EJECUTADA (este acto) | §1-§2 arriba. |
| 3 | `E0` | ✅ EJECUTADA | `ACTO LANE-A-E0-E5` (18/ago), fase CON SELLO completa (`milpa/src/` existe), encargo `forense/encargos/2026-08-18-LANE-A-E0-E5.md` `(CONSUMIDO)`. |
| 4 | `FP-15` (Entrada 5) | ✅ CERRADA | Mismo acto — `RECALCULADO — SIN CAMBIO`, universo declarado, `forense/notas/2026-08-18-motor3-con-sello-y-entrada-5.md`. |
| 5 | Sello `ficha-id-g3` (`FP-11`) | ✅ FIRMADA/EJECUTADA | `ADR-107`; ejecución `CORRIDA-IDG3` adjudicó `ID-X` en el mismo acto (los tres payloads MxFLS `AUSENTE` en este entorno, mesa adjudicó en vez de relanzar), `forense/notas/2026-08-19-sello-ficha-g3-v2-adjudica-idx.md`. |
| 6 | `E3-TRIAGE` (`FP-14`) | ✅ EJECUTADA | `ACTO E3-TRIAGE` (18/ago), encargo `forense/encargos/2026-08-18-E3-TRIAGE.md` `(CONSUMIDO)` — 7 fichas B-bis re-triage, 0 reaperturas. |
| 7 | `T20` (`FP-18`) | ✅ EJECUTADA | `ACTO T20-LLAVES` (18/ago) — condición de activación cumplida 13/ago (contador 0→1, `ACTO ADJ-4`). |
| 8 | Descargas `FP-17` | ✅ EJECUTADA (en lo alcanzable) | `ACTO ADQ-15` (18/ago) + complemento `LOTE UBUNTU-ADQ-1` T3 (19/ago) — 89+9 payloads nuevos, `COINCIDE` bajo `tests/manifiesto.py --verifica`. Tres residuos son barreras de credencial/institucionales, no fallas de descarga, declarados en la propia fila. |

**Las ocho etapas verificadas, una por una, con evidencia por etapa.** `FP-26` se cierra.

## 4 · Contador y medición sobre México

Seis condicionales ejecutadas (`FP-01`..`FP-06`, ya `FIRMADA`/`ejecutada_en=ADR-100`, condición
descargada en este acto). `FP-26` avanza **8 de 8 etapas** — se cierra. Medición sobre México: **0** —
este acto no corre una estimación, no mueve el contador de coeficientes en escala del modelo
(sigue `0 de 15`), no toca `milpa/`, no toca `forense/marco-candidatas-piloto-v1_0.tsv` (perímetro de
`ACT-PIL-2`).

## 5 · Suite y línea base

Primera corrida tras T1-T3, antes de tocar `PLAN-CALCULO-TOTAL`:

```
python3 tests/check.py --baseline
```
→ `23 FAIL · 137 WARN` — `LÍNEA BASE: ROJO`, dos entradas nuevas, ambas la misma causa: `T15` sobre
`canon/PLAN-CALCULO-TOTAL-v1_1.md:8`, cuya "FOTO VERIFICADA" (fechada 12/ago/2026, `A.10` corolario 1,
cuerpo intacto) cita dos cifras de ADR ya vencidas (71, y el `178` de "`#178 ADR-71`") contra el
conteo vigente de `gobernanza` — el mensaje de `T15` incrusta el conteo vigente en su propio texto,
así que dispara de nuevo en **cada** acto que sella un ADR, sin que el archivo citado cambie un byte.

Confirmado en CI real (`PR #301`, run `32425349524`, disparado a mano vía `workflow_dispatch` porque
el evento `pull_request` no había corrido): mismo fallo, mismas dos líneas de `T15`, nada más — sin
regresión ajena a esta causa. Consultada dirección (`AskUserQuestion`, tres opciones: autorizar
`--freeze`, dejarlo ROJO documentado, o corregir la cita) — **"Fix PLAN-CALCULO-TOTAL instead"**: se
marcan las dos cifras `{cita-historica}` en `canon/PLAN-CALCULO-TOTAL-v1_1.md:8` (mismo mecanismo que
`MARCA_HISTORICA`/`T03` ya usa en decenas de sitios de `gobernanza`/`estado-programa` — el cuerpo
`FOTO VERIFICADA` no se toca, solo se declara que la cifra ya no es la vigente). `T15` vuelve a verde
sin `--freeze`.

Con `T15` verde, `T16` (auto-chequeo del propio `estado-programa`) expuso un punto fijo: declarar
`22 FAIL` (el total ingenuo tras restar solo la causa de `T15`) todavía dejaba a `T16` disparando un
FAIL propio por el desfase transitorio contra el `23` declarado antes — declarar en cambio `21 FAIL`
(el número que deja a `T16` en silencio) converge. Verificado corriendo `tests/check.py` sin
`--baseline` hasta que `T16` deja de aparecer en la lista de FAIL.

```
python3 tests/check.py --baseline
```
→ `21 FAIL · 137 WARN` — `LÍNEA BASE: VERDE` (HEAD congelado `e24d033`, 3 entradas de la línea base ya
no aparecen — mejora, no baja la cifra sin `--freeze`). Cero `--freeze` en todo este acto.
