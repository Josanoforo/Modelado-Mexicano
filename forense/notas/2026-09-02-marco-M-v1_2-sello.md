# `MARCO-M-v1_2` — sello del congelado (P1)

`ACTO MAESTRA34-N2 · MARCO-M-v1_2`, 2/sep/2026, NUBE `cloud_default`, skill
`/acto` (`ADR-237`). Encargo redactado por dirección (Fable) 1/sep/2026 contra
`8598a72`, archivado por A.3 en `forense/encargos/cola/2026-09-01-MAESTRA34-N2-MARCO-M-v1_2.md`
(PR `[COLA]`, firma D4-a).

**Este archivo se escribe ANTES de sortear.** El sorteo (P2) vive en
`sorteo-marco-M-resultados-v1_2.md`, con su propio pre-registro.

## Compuerta (verificada por comando, no por prosa)

`COMPUERTA: MAESTRA34-N1 fusionado en origin/main con ≥1 regla nueva cargada en
milpa/tramite.yaml (reglas del motor > 8) Y MAESTRA33-E21 fusionado (#446).`

Al primer lanzamiento de esta sesión la compuerta **no** se cumplía y el acto
paró con cero commits (`MAESTRA34-N1` no aparecía en `origin/main`; motor en 8
reglas). `origin/main` se movió de `92fd3f7` a `ec3cf0f` durante la sesión y se
re-verificó:

- `git log --oneline origin/main | grep -i "MAESTRA34-N1"` → `ec3cf0f Merge pull request #449 …`.
- `git show origin/main:milpa/tramite.yaml | grep -cE '^\s*-\s*id:\s*\S'` → **10** (`>8`), con
  las dos reglas nuevas `familia.seguro.volatilidad_ausencia_estado` y
  `dinero.planeacion.formal_estable`.
- `git log --oneline origin/main | grep -i "446"` → `84433c7 Merge pull request #446 …`.

Ambas condiciones cumplidas. `SHA del merge de MAESTRA34-N1` =
`ec3cf0f2d98346205fafa7ece756ca5875cb5707` — es el que P2 usa para derivar la
semilla, no un SHA heredado de prosa.

## Entorno (A.2, tres partes)

- `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable`.
- `ls data/raw/` → **ausente** (esperado en nube).
- Este acto **no abre microdato y no descarga nada**: no aplica el anti-PR#77.

Consecuencia directa sobre las columnas: toda cifra de diseño de las filas
nuevas (`ponderador`, `n_no_ponderado`, `universo`) se **copia** del campo
homónimo de la regla que `MAESTRA34-N1` selló verbatim, citada por celda en
`razon` — no se re-deriva. Por eso `base_medida=NO` en las 7, misma regla de
columnas que `forense/notas/2026-08-31-marco-M-v1_1-spec.md` §(e) ("nada se ha
medido todavía para esas olas **en este acto**").

## Qué entra (7 filas nuevas)

Regla del encargo: *una celda por (regla nueva del motor × ola en corpus por la
vía del índice/manifiesto)*.

`corpus/indice.yaml` **no** es la vía: mapea claves `report:`/`validacion:` a
reports del corpus, no payloads de microdato (leído entero, 153 líneas). La vía
real es `data/manifiesto.yaml`, el manifiesto que `tests/manifiesto.py --verifica`
usa. Los 7 `payload_manifiesto_id` que las dos reglas declaran están **los 7** en
ese manifiesto, y en los dos casos verificables el `sha256` del manifiesto
coincide con el `sha256_payload` de la regla (`enigh2022_nc_csv` →
`3b2b0bc9…9e06`; `enfih2019_bd_csv_zip` → `be372533…ef4d5`).

| id | encuesta | ola | regla | `grado_DD` | elegible |
|---|---|---|---|---|---|
| `FAM-M-03` | ENIGH | 2012 | `familia.seguro.volatilidad_ausencia_estado` | `P1 PUNTUA` | SI |
| `FAM-M-04` | ENIGH | 2014 | idem | `P1 PUNTUA` | SI |
| `FAM-M-05` | ENIGH | 2016 | idem | `P1 PUNTUA` | SI |
| `FAM-M-06` | ENIGH | 2018 | idem | `P1 PUNTUA` | SI |
| `FAM-M-07` | ENIGH | 2020 | idem | `P1 PUNTUA` | SI |
| `FAM-M-08` | ENIGH | 2022 | idem | `P0 VERIFICACION-NO-PUNTUA` | NO |
| `DIN-M-04` | ENFIH | 2019 | `dinero.planeacion.formal_estable` | `P0 VERIFICACION-NO-PUNTUA` | NO |

`N_filas` 27 → **34**; `N_elegibles` 22 → **27**; `N_verificacion_no_puntua`
5 → **7**.

## El juicio de marco que este acto sí tuvo que hacer

`familia.seguro.volatilidad_ausencia_estado` trae `serie_olas` con **p medida
para las 6 olas ENIGH**, no sólo para la de calibración. Eso abre la pregunta de
si las 5 olas no-calibración son transferencia real o calibración encubierta —
que es exactamente lo que `F-DD` existe para decidir, y no se resuelve leyendo
la cadena `ola_calibracion` y ya.

**El precedente que obliga a preguntarlo.** `dinero.ahorro.tiene_ahorros` declara
`ola_calibracion` de **una** ola (ola 2), pero `marco-M-congelado-v1_1.tsv` marcó
`P0` a **ola 2 y ola 3** (`DIN-M-02`, `DIN-M-03`), con `razon_DD` leyendo
"ola_calibracion=ENNViH olas 2-3 … panel retenido". Es decir: F-DD ya se aplicó
una vez por **si la ola alimentó el número sellado**, no por coincidencia
literal. Si ese criterio se extiende, las 6 olas ENIGH serían `P0` y esta pieza
aportaría **cero** celdas puntuables.

**Lo que decide, verificado contra el motor y no supuesto.**
`milpa/src/emisor.py:475-481` — `emitir_binaria` recorre **únicamente**
`regla.entonces` y devuelve `s.p` de la conducta; **nunca** toca `serie_olas`.
Luego M emite `0.045694` (el p de 2022) para *toda* ola ENIGH, y la p que
`serie_olas` guarda para 2016 es **inerte al emisor**. La distinción con el
precedente DIN es de sustancia: allí las dos olas produjeron **juntas** el único
p asertado (`universo`: "válidos en **ambas olas**, panel retenido"); aquí el p
asertado sale de 2022 **sola**, y la regla lo dice verbatim — "las otras 5 van en
`serie_olas`, **NO promediadas**".

Veredicto: las 5 olas no-calibración son transferencia **de ola** genuina
(mismo instrumento, distinta ola) → `P1 PUNTUA`. ENIGH 2022 es `P0`, y lo es por
partida doble: coincide con `ola_calibracion` **y** es la ola de la que sale el p
asertado.

**Límite declarado, que esta pieza no puede cerrar sola.** La p medida de las 5
olas puntuables **sí** está publicada en `milpa/tramite.yaml` (`serie_olas`). Eso
no contamina a M —su predicción es `0.045694`, fija e independiente— ni a R —que
mide contra microdato—, pero **sí contaminaría a L** si el paquete que la mesa le
entrega dejara ver ese archivo. P4 lo cierra por construcción: la `L-spec` toma
sólo `id`/`encuesta`/`ola`/`universo`/`conducta`/`escala`, y el `universo` de
estas filas se redactó **deliberadamente sin una sola cita** de
`milpa/tramite.yaml`, de `serie_olas` ni de la regla, porque `universo` viaja
**verbatim** dentro de `pregunta_L`. Queda como fila de firmas para mesa, no como
decisión de este acto.

**`DIN-M-04` aporta 0 celdas puntuables** — ENFIH tiene una sola ola en el
corpus, no hay ola a la que transferir. Se reporta en vez de fabricar una celda
de transferencia que no existe.

## Columnas: por qué `elegible_v1_1` conserva su nombre

El encargo exige "columnas idénticas". Se cumple al pie: los 32 encabezados de
`v1_1` salen intactos, **incluido el nombre `elegible_v1_1`**. No es descuido —
es lo que permite que `sorteo_marco_m_v1_1.cargar_marco_m_v1_1(ruta=…, ruta_sha=…)`
lea este marco tal cual, con su verificación de `sha256` y su `assert` de conteo,
**sin editar ni duplicar un solo módulo sellado**. La versión del marco la fija el
nombre del archivo, no el de la columna.

## Controles que corrieron (y que habrían parado el acto)

1. `sha256(marco-M-congelado-v1_1.tsv)` == `8e6459dd…2477` declarado en
   `CONGELADO-M-v1_1.sha256` — el insumo no se movió.
2. Las 27 líneas de `v1_1` salen **byte a byte idénticas** como prefijo de
   `v1_2` (`assert nuevo[:len(orig)] == orig`) — "celdas v1_1 intactas"
   verificado, no prometido.
3. Invariante F-DD por fila: `elegible_v1_1 == 'SI'` ⟺ `grado_DD == 'P1 PUNTUA'`,
   en las 34.
4. 32 columnas en las 34 filas, terminador `LF`, sin `CR`, sin campo desalineado
   (releído con `csv.DictReader`).
5. Anti-fuga: ningún `universo` de las filas nuevas contiene `tramite.yaml`,
   `serie_olas`, `milpa/`, `sha256` ni literal numérico de p.

`marco-M-congelado-v1_2.tsv` → `sha256` sellado en `CONGELADO-M-v1_2.sha256`.

## Lo que este archivo NO hace

No sortea, no emite M, no calcula R, no corre L, no puntúa, no toca `v1_1` ni
sus corridas, no toca `milpa/**` (sólo lectura).
