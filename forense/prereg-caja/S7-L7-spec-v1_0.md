# S7 · Pre-registro de `salud.vacunacion.disponible` — objeto verbatim del canon (`R9.2`)

### `prereg-caja-S7-L7` · **v1.0** · 5 de septiembre de 2026

| ARCHIVO | `forense/prereg-caja/S7-L7-spec-v1_0.md` |
|---|---|
| NOMBRE ESTABLE | `prereg-caja-S7-L7` — cítese por este nombre, nunca por la ruta de archivo |
| QUÉ ES | Pre-registro congelado de la regla `salud.vacunacion.disponible` (`R9.2`), clasificada `MEDIBLE-COMO-ESTÁ` *(propuesta, dirección revisa)* por `ACTO MAESTRA38-N10` §2.5, con la corrección de dominio de `§3.9` |
| QUÉ NO ES | No mide nada de México. No abre microdato. No sella `R9.2` en canon. **No reabre ni revisita el veredicto `D` de Hito D** (§0.2) — declara su existencia, no lo discute |
| VERIFICAS ASÍ | `sha256sum -c S7-L7-spec-v1_0.sha256`; el acto futuro `MAESTRA38-L7` compara su primer resultado contra esta spec |

**Acto:** `ACTO MAESTRA38-N11 · PRE-REGISTRO-OLA6-MEDIBLES-Y-FICHAS`, 5/sep/2026, entorno **NUBE**, sobre `origin/main = b17d19bd`. `data/raw` ausente, ningún microdato abierto.

---

## 0 · Ficha bajo prueba — y un hallazgo de A.8 que N10 no tenía cruzado

### 0.1 · Definición vigente, verbatim de `canon/modelo-decision-v4_0.md:575` (`§3.9`, no `§3.4`)

> **SI** la vacuna/servicio está disponible y la campaña llega **ENTONCES** la mayoría acepta — PORQUE el default es aceptación y el hueco es logístico (no actitudinal) — `[FUERTE]`. · **id:** `salud.vacunacion.disponible` ⚠️ *id ya existente en `procedencia.yaml`, con dominio equivocado (`salud.*` en un id de `§3.9`, no `§3.4`) — no se corrige, ver `forense/hallazgos.md`*

Cruce `§7`: `` | `R9.2` | L289 | Vacuna/servicio disponible + campaña llega → la mayoría acepta | `[FUERTE]` | Sí | `` — columna final **Sí**: `R9.2` **sí** tiene ficha/veredicto en Hito D. Esto es lo que §0.2 declara.

### 0.2 · A.8/D-13 — Hito D ya corrió un intento de falsación sobre este `id`, con veredicto `D`, sobre un diseño DISTINTO del que N10/esta pieza pre-registra

`tools/ya_medido.py R9.2` (salida completa en §0.4) encuentra `canon/modelo-decision-v4_0.md:704` — la línea que abre el bloque de veredictos de `§7` — pero el extracto que el script imprime está **truncado antes de llegar al texto real**: esa línea es un párrafo único y larguísimo que, más adelante, contiene literalmente `` `R9.2` → veredicto `D` `` (verificado por lectura directa, no por el resumen del script). El bottom-line `NUNCA-MEDIDA` del script es correcto respecto de su propio vocabulario (`CORROBORADA`/`CONTRARIA`/etc., el de las notas de espacio `L`) — **pero ese vocabulario no cubre las letras `A`–`E` de Hito D**, y por eso el script no lo cuenta como "medida". Esto **no es un error de N10**: su §5(a) declaró honestamente "ninguna discrepancia contra `ya_medido.py`" citando exactamente ese mismo criterio de vocabulario — pero un `id` con veredicto `D` archivado en el propio `§7` que el script sí cruza merece quedar escrito en A.8 de cualquier acto que, como este, vaya a pre-registrar sobre ese `id`, para no repetir el patrón que `N7`/`N9` ya corrigieron dos veces.

**Detalle del veredicto, verbatim de `forense/hitoD-preregistro-v2_0.md:1016`** (Nota 25, archivado 4/ago/2026, `ADR-56`, Encargo Z):

> **`R9.2` → `D`.** El Umbral exige cobertura baja **Y** abasto/campaña verificados por tercero; la segunda condición no tiene ninguna fuente en el catálogo completo — la única disponible (DGIS) es el propio prestador, excluida por la ficha misma... **Este `D` es ausencia determinable de instrumento auditor, no ausencia del fenómeno ni evidencia de que el hueco sea actitudinal**.

**Por qué este pre-registro no repite ese diseño bloqueado.** El Umbral que Hito D declaró inejecutable exigía un **auditor institucional tercero** (no el propio prestador) que verificara `abasto`/`campaña` a nivel administrativo — esa pieza sigue sin existir (DGIS es prestador, `CNGMD` no cubre salud). El diseño que `N10`/esta pieza pre-registra es **categóricamente distinto**: opera con **autorreporte del hogar, mismo instrumento y misma persona** (ENNViH: costo de la vacuna en la consulta como antecedente de disponibilidad; recepción de la vacuna como desenlace) — no depende de ningún auditor tercero, y por eso el bloqueo de Hito D no le aplica mecánicamente. **Esto no reabre ni discute el veredicto `D`** (D-13: los IDs y sus veredictos archivados son un registro congelado) — es una vía de medición distinta sobre el mismo `id`, declarada como tal.

### 0.3 · Objeto verbatim de `N10 §2.5`

Disparador (antecedente): `ce19d_2 COSTO VACUNA CONSULTA`, `hs16d_2 COSTO VACUNA HOSPITAL` (ENNViH). Desenlace, mismo instrumento: `cen12_1a CONSULTA RECIBIO:VACUNACION`, `he25c SERV EMBARAZO:VACUNA TETANOS`. Reforzado por un tercer instrumento —**no requerido para el sello**— `ENSANUT 2024` (`adultos_ensanut2024_w`, sección de vacunación: `d0321j`/`d0321p` y otras del mismo bloque), que corrobora únicamente el lado del desenlace.

### 0.4 · `tools/ya_medido.py`, salida completa

```
$ python3 tools/ya_medido.py R9.2
=== ya_medido: R9.2 ===
  resuelto por canon: R9.2 -> id `salud.vacunacion.disponible` (canon/modelo-decision-v4_0.md §3, tag **id:**)
  términos de búsqueda (match exacto): R9.2, salud.vacunacion.disponible

-- milpa/tramite.yaml --
  (sin apariciones)
-- milpa/tramite-ola5-propuesta-v0.yaml --
  (sin apariciones)
-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:704  tier=[MEDIA]
      - **49 reglas** ... **Hito D (perímetro de 27 reglas, subconjunto de las 49): 26 de 27 corridas archivadas** ...
  canon/modelo-decision-v4_0.md:774  tier=[FUERTE]
      | `R9.2` | L289 | Vacuna/servicio disponible + campaña llega → la mayoría acepta | `[FUERTE]` | Sí |
-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-03-MAESTRA37-L1-censo.md:90
  forense/notas/2026-09-03-MAESTRA37-L1-remapeo.md:56,80
-- forense/prereg-caja/S*-spec-*.md --
  (sin apariciones)
-- canon/registro-rotulos.tsv (alias) --
  (sin apariciones)
========================================
NUNCA-MEDIDA
```

`NUNCA-MEDIDA` en el vocabulario del script, con el hallazgo de §0.2 declarado aparte — pegado de nuevo tal como el encargo pide, y leído, no sólo pegado.

---

## 1 · Variables — texto de reactivo copiado del inventario, no parafraseado

| variable | instrumento | ola | etiqueta verbatim |
|---|---|---|---|
| `ce19d_2` | ENNViH | **por confirmar en CAJA** — el manifiesto no indexa por variable (búsqueda exhaustiva, cero coincidencias de `ce19d_2`/`hs16d_2`/`cen12_1a`/`he25c` como texto en `data/manifiesto.yaml`); ni `N5` ni `N10` citan la ola | `COSTO VACUNA CONSULTA` |
| `hs16d_2` | ENNViH | íd. | `COSTO VACUNA HOSPITAL` |
| `cen12_1a` | ENNViH, **mismo instrumento que `ce19d_2`/`hs16d_2`** | íd. | `CONSULTA RECIBIO:VACUNACION` |
| `he25c` | ENNViH | íd. | `SERV EMBARAZO:VACUNA TETANOS` |
| `d0321j`, `d0321p` (y sección completa de vacunación) | ENSANUT 2024, módulo `adultos` | 2024 | vacunación (tétanos, Tdap/tosferina) — **corroboración del desenlace, no del antecedente**; `N10` reporta 268/42 536 aciertos de `vacun\w+` contra `descargas_mx_v1_1` |

**Declarado, no verificado (A.13):** a diferencia de `S6` (donde la ola de `es09`/`cen10*` se pudo anclar por el texto de `N5`, "ventana de 4 años" ⇒ ENNViH-3), ni `N5` ni `N10` fijan la ola de `ce19d_2`/`hs16d_2`/`cen12_1a`/`he25c`. Este pre-registro **no adivina** la ola — la deja como primer paso de CAJA (§6 lista los tres bundles de ENNViH completos como candidatos, no uno solo).

---

## 2 · Universo y ponderador

**Universo pre-registrado:** personas con respuesta válida en `ce19d_2` o `hs16d_2` (tuvieron una consulta/hospitalización donde el costo de la vacuna fue registrado) — la regla es condicional al contacto con el servicio, igual que `S6`.

**Ponderador:** **no declarado en esta pieza** — depende de qué ola/libro de ENNViH resulte confirmado en CAJA (§1); cada ola trae su propio ponderador transversal (`ennvih1_2002_ponderador`, `ennvih2_2005_ponderador_transversal`, `ennvih3_2009_ponderador_transversal`, ver §6). Declarar el ponderador antes de tener la ola sería heredar de prosa sin verificar — exactamente lo que `D-13` prohíbe.

---

## 3 · Dicotomizaciones y celdas

**`DISPONIBLE`** = 1 si `ce19d_2`/`hs16d_2` indica costo cero/gratuito (servicio disponible sin barrera de costo); 0 si costo > 0 o "no disponible" — codificación exacta pendiente de codebook (CAJA).

**`ACEPTA`** = 1 si `cen12_1a`/`he25c` indica que recibió la vacuna.

### 3.1 · Celda — una proporción, mismo patrón que `S6`

```
C = P(ACEPTA=1 | DISPONIBLE=1) − 0.5
```

**Cota de n mínima:** numerador `< 10` ⇒ `NO-ESTIMABLE` — misma guardia que `S4`/`S5`/`S6` fijan.

---

## 4 · Falsador — signo, y las dos filas que `B-bis` exige

| fila | condición |
|---|---|
| **Signo esperado** | `C > 0` (mayoría acepta cuando está disponible), IC95% excluye 0 |
| **`CORROBORADA`** | `C` estimable, IC95% excluye 0 en signo positivo |
| **`CONTRARIA`** | `C` estimable, IC95% excluye 0 en signo negativo |
| **`NO-DISCRIMINA`** | IC95% de `C` contiene 0 |
| **`NO-ESTIMABLE`** — **qué pasa si no refuta** | numerador `< 10`, o la ola de ENNViH que CAJA confirme no trae ambas variables en el mismo respondente. **Si cae aquí, no reabre el veredicto `D` de Hito D** (§0.2) ni lo confirma — declara únicamente que esta vía alternativa (autorreporte de hogar) tampoco alcanzó a discriminar, con su propia razón, distinta de la razón de Hito D. |

---

## 5 · `se_mueve_si`

El objeto se mueve si, estando `DISPONIBLE`=1, una fracción mayoritaria **no** acepta — eso apuntaría a que el hueco es actitudinal, no logístico, contradiciendo el `PORQUE` de la regla. También se mueve si la campaña "llega" (variable no operacionalizada en este pre-registro: `ce19d_2`/`hs16d_2` miden costo, no alcance de campaña) resulta ser una condición distinta de "costo cero" — declarado como límite del diseño, no resuelto aquí.

---

## 6 · Archivos que la caja necesita abrir

**Sin ola confirmada (§1), se listan los tres bundles completos de ENNViH — CAJA descarta dos una vez localizada la variable:**

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `ennvih1_2002_hogar_dta` | `ennvih/ehh02dta_all.zip` | `8b9b51904ca8790421d82a8a81f7f4edbce9a296cba2ce86fef74f8f379b5923` |
| `ennvih2_2005_hogar_dta` *(id de manifiesto, sha por confirmar en CAJA — no citado en esta pieza)* | `ennvih/ehh05dta_all.zip` | — |
| `ennvih3_2009_hogar_dta` | `ennvih/ehh09dta_all.zip` | `00a7649a1839a3523be22612c2fa3555d5e743cf5329d6bcdc432b901e98bd15` |
| `adultos_ensanut2024_w_stata_stata__v2026_09_01` *(corroboración del desenlace, no requerido)* | `ENSANUT2024-v2026-09-01/adultos_ensanut2024_w.stata.stata.zip` | `0fa8f4436fa427cc23d1d43164d449462c09eb787cb45ad20961576cb095a6c4` |

---

## 7 · Qué NO hace este acto

No abre ningún archivo de §6 — `data/raw` ausente en NUBE. No sella `R9.2` en canon. **No reabre, no confirma y no refuta el veredicto `D` de Hito D** (`ADR-56`) — lo cita como registro congelado y declara por qué el diseño de esta pieza es distinto (§0.2). No corrige la anomalía de dominio del `id` en `canon/modelo-decision-v4_0.md` (fuera de perímetro: `canon/modelo-decision*` no se toca) — la corrección de **mapa** va en `canon/registro-rotulos.tsv` (P3 de este acto, pieza aparte). No fija la ola de ENNViH — declarado pendiente, no adivinado (§1).

**Medición: caja, acto `MAESTRA38-L7`** — nombre nuevo, asignado por este pre-registro; sin colisión verificada (`grep -rn "MAESTRA38-L7"` → 0 apariciones previas).

**El primer resultado que produzca este procedimiento es el que se reporta.**
