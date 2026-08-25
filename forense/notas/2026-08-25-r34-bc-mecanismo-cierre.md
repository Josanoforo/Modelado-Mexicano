# Nota de cierre · `ACTO R34-BC-MECANISMO` — 25/ago/2026

**Encargo:** `forense/encargos/2026-08-25-R34-BC-MECANISMO.md` (archivado verbatim por este acto, `A.3`). **ADR:** `ADR-186`. **Entorno:** UBUNTU. **Base:** `2b7d787` (= `origin/main`, `PR #356`). **Rama:** `acto/r34-bc-mecanismo`.

## 1 · Firma de entorno (`A.2`, tres partes) y arranque

| parte | salida cruda |
|---|---|
| variable | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable` |
| sonda | `curl -s -o /dev/null -w "http=%{http_code} bytes=%{size_download} tiempo=%{time_total}" --max-time 25 -r 0-11 https://www.inegi.org.mx/` → `http=206 bytes=12 tiempo=0.575848` (GET crudo con rango; **no** `curl -I`) |
| corpus | `data/raw` → `/home/pc0/mm-corpus/raw`; `head -1` = `2005trim1_csv.zip`; 321 entradas; 9.6 GB |

`SHA` de redacción: `git rev-list --count 2b7d787..origin/main` = **0**. El worktree del acto se creó sobre `2b7d787` exacto.

## 2 · Un negativo propio, corregido en vivo — y el mecanismo que lo atrapó

La primera corrida de `F0` se hizo contra el **worktree principal**, que estaba parado en `ea22bdd` (rama `acto/cal-g3-puntual`), un árbol **anterior** a `PR #356`. Sobre él, `forense/ficha-r34-conda-v2-spec.md` no existía, `ADR-177` no existía, el máximo de `ADR` era `157` y `FP-104` figuraba `ABIERTA` — es decir, **las cuatro premisas del encargo parecían falsas**. Re-corrido `F0` sobre la caja del acto (`2b7d787`, el SHA que el propio encargo fija), **las cuatro son ciertas**.

Se registra porque es exactamente el modo de falla que `forense/hallazgos.md:349` ya canonizó — *«re-correr el comando, no heredar su salida»*— aplicado esta vez no a una salida heredada de otro acto sino a **un árbol equivocado**. La lección operativa, que no estaba escrita: **el universo de un comando incluye el árbol sobre el que corre**, y un `git rev-parse HEAD` al arrancar la habría atrapado antes. Ningún veredicto de este acto depende de la corrida errónea; se declara porque el negativo llegó a estar escrito.

## 3 · Qué se hizo, en orden

1. **`F0`** — `find` sobre `forense/` completo (**1,524 archivos examinados**) con patrones `r34`/`r3_4`/`r3-4`/`codi`/`spei`: 8 aciertos, los 8 de la condición `A` o su cadena. Ningún abridor `B`/`C`. **Sin `PARO`** (`A.8`).
2. **`F1` · censo** — 11 candidatas, cada una abierta **a nivel de reactivo** (cuestionario o descriptor, nunca sólo el nombre de la variable), más un barrido mecánico de `data/raw/` completo con `tools/censo_r34_bc.py`: **20,838 archivos examinados**, `20,280` con texto de longitud > 0. Veredicto `A.4` por candidata y por condición.
3. **`F2` · Commit 1** — censo y **criterio de aceptación** congelados. Con cero `EXISTE-SATISFACE` no hay spec de corrida que congelar y el acto no la inventa: se congela qué tendría que traer una fuente para que el veredicto cambie, **antes** de que exista sucesor que pudiera relajarlo.
4. **`F3` · Commit 2** — propuesta por condición, el defecto del pre-registro, la vía, `ADR-186`, `estado`, tablero, esta nota.

## 4 · El resultado, en una línea

**Cero `EXISTE-SATISFACE` para `B` y cero para `C`, y la razón es una sola variable ausente, no una ausencia de fuentes.**

Ningún instrumento del corpus mide la **percepción de riesgo fiscal o de vigilancia asociada a *usar*** un medio de pago o un servicio de gobierno digital. `B` apaga esa variable; `C` la sostiene encendida; sin ella **ninguna de las dos es evaluable**, por buenas que sean las demás piezas. Y las demás piezas son buenas:

- **desenlace** exacto —no-uso de CoDi entre usuarios digitales— **dos veces, en dos emisores**: `ENDUTIH` `P7_32_6` (INEGI, olas 2023-2024-2025, con `FAC_PER`/`UPM_DIS`/`EST_DIS`) e `IFT SFD 2024`;
- **fricción declarada** en tres instrumentos;
- **canal personal separado del institucional en la misma batería y sobre los mismos individuos**, en `ENCIG` — la pieza cara de `C`, y está resuelta.

## 5 · Lo que este acto entrega y que no estaba antes

1. El **censo con universo declarado** para `B` y `C`, que nadie había corrido: los cuatro sitios previos del árbol (`cruce-catalogo-fichas-v2_0.md:67`, `matriz-impacto-universal-2026-08-06.md:48`, `notas/2026-08-08-barrido1.md:116`, y el `Respaldo 2` del pre-registro) **proyectaban** el resultado —«NO ENLAZA para B/C», «probablemente inejecutables»— pero ninguno lo había **medido** contra el corpus. Ahora está medido, y con conteo.
2. El **nombre exacto** de la única variable que bloquea las dos condiciones, y la lista de lo que ya existe alrededor de ella.
3. Tres **defectos de forma** medidos que impiden usar el mejor casi-acierto: la batería fiscal de `ENIF` es de **respuesta única** (`CIRCULE UN SOLO CÓDIGO`), su objeto **no es CoDi**, y en `ENDUTIH`/`IFT SFD` la batería de razones y el desenlace viven en universos **complementarios** — por diseño del salto, ningún individuo tiene los dos.
4. Una **contradicción interna del pre-registro sellado** de `R3.4`: su `Respaldo 2` manda este desenlace a la fila `D`, pero la fila `D` exige que `A` falle y `A` está `SELLADA`. Va a mesa (`FP-155`), no se adjudica.
5. `tools/censo_r34_bc.py`, reejecutable y reanudable, con sus límites escritos en el propio docstring.

## 6 · Contadores

**CONTADOR: cero, declarado.** No se movió ningún contador de medición sobre México. `Hito D` sin cambio. **Base medida de `B`/`C`: sigue en `0 de 2`** — este acto no produjo dato mexicano sobre esos umbrales porque no hay fuente de la que producirlo; lo que produjo es el universo del negativo. El contador de `ADR` pasa de `185` a `186` (recifrado en `estado` L0). El tablero pasa de **0 filas `ABIERTA`** a **1** (`FP-155`).

## 7 · Lo que este acto NO hizo, y se dice

No adjudicó `R3.4` — sigue **sin veredicto**. No tocó `tests/aceptacion_r3_4.py`. No re-abrió la condición `A`. No cableó disparadores a `milpa/tramite.yaml`. No descargó ninguna fuente (`ENSAFI` `FD` queda como la vía propuesta, **no ejecutada**). No corrió `B` ni `C` sobre ningún proxy — el encargo lo prohíbe y el acto está de acuerdo con la prohibición: cualquiera de las cuatro fuentes daría un número, y ese número sería el defecto que `ADR-25` creó y `ADR-37` corrigió.

## 8 · Suite

`python3 tests/check.py --baseline` → **LÍNEA BASE: VERDE**, nada nuevo frente a `tests/baseline.json`. Cifras: **19 FAIL núcleo (sin cambio) · 129 WARN** (`128 → 129`), medido y no derivado por aritmética. El `+1` de WARN es **`FP-155` naciendo `ABIERTA`** y `T22` señalándola — que es exactamente lo que `A.12` existe para hacer: el WARN sigue gritando hasta que mesa la atienda.

Tres cosas se corrigieron durante el cierre, todas de contabilidad del programa sobre sí mismo y ninguna sobre México:

1. **`T15` ×2** — `canon/estado-programa-v1_10.md:27` y `canon/gobernanza-v1_15.md:2` citaban `185 ADR`; con `ADR-186` son `186`. Recifradas las dos cabeceras.
2. **`T22` ×1** — el encargo archivado dispara `_T22_MARCADOR_PENDIENTE` (patrón `PROPUESTA.*mesa`) y ninguna fila lo citaba. **No se añadió a `_T22_ARCHIVOS_CONOCIDOS`**: el pendiente es real, así que la corrección correcta era la contraria — `FP-155` cita ahora en su columna `dónde` el encargo, la ficha y esta nota. El test hacía bien su trabajo.
3. **`T16` ×2** — `estado:303`/`:305` declaraban `128 WARN`. Recifradas a `129`; y la cifra vieja de `ACTO PACK-NUBE2-CIERRE-R101` en `:305` recibió su marca `{cita-historica}` inmediatamente después del cierre de negritas, que es la convención que el propio archivo ya usa en sus otras diez cifras históricas.

## 9 · Qué queda vivo

`FP-155`, `ABIERTA`, con tres decisiones separables para mesa: (1) si se adopta `B`/`C` `INDETERMINADA`; (2) en qué fila aterriza el gate —el acto propone `B` y explica por qué la `D` que el `Respaldo 2` nombra es imposible con `A` sellada—; y (3) si se autoriza la vía, cuyo primer paso es **una descarga**: el `FD` de `ENSAFI 2023`, que `FP-115`(c) ya tenía identificado con su patrón de URL.
