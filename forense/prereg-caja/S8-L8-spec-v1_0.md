# S8 · Pre-registro de `comunicacion.inseguridad.ver_oir_callar` — objeto verbatim del canon (`R10.3`)

### `prereg-caja-S8-L8` · **v1.0** · 5 de septiembre de 2026

| ARCHIVO | `forense/prereg-caja/S8-L8-spec-v1_0.md` |
|---|---|
| NOMBRE ESTABLE | `prereg-caja-S8-L8` — cítese por este nombre, nunca por la ruta de archivo |
| QUÉ ES | Pre-registro congelado de la regla `comunicacion.inseguridad.ver_oir_callar` (`R10.3`), clasificada `MEDIBLE-COMO-ESTÁ` *(propuesta, dirección revisa)* por `ACTO MAESTRA38-N10` §2.6 — hallazgo nuevo de ese acto, vía módulo `AOJ` de LAPOP |
| QUÉ NO ES | No mide nada de México. No abre microdato. No sella `R10.3` en canon. No reabre las corridas de `N5`/`N6` sobre este `id` (ENDIREH/CNGMD) — las cita como continuidad, no las repite |
| VERIFICAS ASÍ | `sha256sum -c S8-L8-spec-v1_0.sha256`; el acto futuro `MAESTRA38-L8` compara su primer resultado contra esta spec |

**Acto:** `ACTO MAESTRA38-N11 · PRE-REGISTRO-OLA6-MEDIBLES-Y-FICHAS`, 5/sep/2026, entorno **NUBE**, sobre `origin/main = b17d19bd`. `data/raw` ausente, ningún microdato abierto.

---

## 0 · Ficha bajo prueba — continuidad con N5/N6, ausencia verificada en Hito D

### 0.1 · Definición vigente, verbatim de `canon/modelo-decision-v4_0.md:585`

> **SI** el contexto es de inseguridad/autoridad no confiable **ENTONCES** "ver, oír y callar" — PORQUE G4 (adaptación racional, no timidez) — `[FUERTE]`. · **id:** `comunicacion.inseguridad.ver_oir_callar`

Cruce `§7`: `` | `R10.3` | L299 | Inseguridad/autoridad no confiable → "ver, oír y callar" | `[FUERTE]` | Sí | `` — la columna **Sí** indica que `R10.3` tiene ficha en Hito D (identificación de `id`, no necesariamente veredicto de falsación real — ver §0.2).

### 0.2 · A.8 contra Hito D — sin veredicto `A`–`E` archivado

`tools/ya_medido.py R10.3` (§0.4) encuentra `R10.3` en `canon/modelo-decision-v4_0.md:727` (la nota de política de IDs, "`R1.1`–`R10.3` quedan exactamente como están") y en la fila de la tabla cruzada (línea 778) — **ninguna de las dos es un veredicto de falsación**. Verificado además por lectura directa del bloque de veredictos archivados (`§7` línea 704, la lista cerrada de 26 `R-n` con letra `A`–`E`): **`R10.3` no aparece en esa lista** (confirmado contra los mismos 26 `R-n` citados en `S6 §0.2`/`S7 §0.2`). `R10.3` **no** está en el perímetro de 27 reglas de Hito D. Este pre-registro es, hasta donde el repo permite verificar, el primer intento de falsación pre-registrado sobre este `id` que usa el módulo `AOJ`.

### 0.3 · Continuidad declarada con `N5`/`N6` — no una primera medición del `id`, sí del instrumento

`N5` (encuesta, `v1_2`/`ext`): `EXISTE-NO-SATISFACE` — los 170 aciertos de `denunci*` son `p6_19_1..4` (ENDIREH 2016), pero el universo de ENDIREH es violencia contra la mujer, no "contexto de inseguridad" en general. `N6` (administrativo): `EXISTE-NO-SATISFACE` — `CNGMD` registra denuncias que **ocurrieron**, sin denominador de quienes callaron (sesgo de selección). **Ninguno de los dos corrió `busca_reactivos.py --tablas descargas_mx_v1_1`** (nacida el 3/sep, un día antes de que `N5` clasificara) — `N10` sí, y encontró el módulo `AOJ` de LAPOP AmericasBarometer, población general adulta, no restringida a violencia de género. Esta pieza congela ese hallazgo; no repite ni reabre las corridas de ENDIREH/CNGMD.

### 0.4 · `tools/ya_medido.py`, salida completa

```
$ python3 tools/ya_medido.py R10.3
=== ya_medido: R10.3 ===
  resuelto por canon: R10.3 -> id `comunicacion.inseguridad.ver_oir_callar` (canon/modelo-decision-v4_0.md §3, tag **id:**)
  términos de búsqueda (match exacto): R10.3, comunicacion.inseguridad.ver_oir_callar

-- milpa/tramite.yaml --
  (sin apariciones)
-- milpa/tramite-ola5-propuesta-v0.yaml --
  (sin apariciones)
-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:727
      **Decisión: los IDs son un registro CONGELADO, no una fórmula.** (a) Los **24 IDs ya usados en fichas** (`R1.1`–`R10.3`, ver `hitoD-preregistro`) quedan exactamente como están...
  canon/modelo-decision-v4_0.md:778  tier=[FUERTE]
      | `R10.3` | L299 | Inseguridad/autoridad no confiable → "ver, oír y callar" | `[FUERTE]` | Sí |
-- forense/notas/*-L*-*.md --
  (sin apariciones)
-- forense/prereg-caja/S*-spec-*.md --
  (sin apariciones)
-- canon/registro-rotulos.tsv (alias) --
  (sin apariciones)
========================================
NUNCA-MEDIDA
```

`NUNCA-MEDIDA`, consistente con §0.2 (sin veredicto Hito D archivado) y con §0.3 (ninguna de las corridas de `N5`/`N6` es una falsación real, ambas son "existencia de reactivo").

---

## 1 · Variables — texto de reactivo copiado del inventario, no parafraseado

**Instrumento:** LAPOP AmericasBarometer México, módulo `AOJ` ("Rule of Law"). **Lista de olas — no cerrada en esta pieza:** `N10` cita 2004/2006/2019/2021/2023 como el universo del módulo, y verificó específicamente contra `1658622845Mexico 2004 Export Version.sav`/`.dta` (gemelos byte-a-byte, integridad de corpus, no disponibilidad de ítem por ola). **A diferencia de `S5`** (que cerró la lista de olas de `PROT1`/`PROT2`/`prot3` variable por variable), esta pieza **no** verificó ítem por ola qué subconjunto de `AOJ11`/`B18`/`B10A`/`AOJ12`/`aoj1`/`aoj1a`/`aoj1b` aparece en cada una de las cinco — CAJA lo hace como primer paso (§6 lista las cinco olas).

| variable | rol | etiqueta verbatim (`N10 §2.6`) |
|---|---|---|
| `AOJ11` | antecedente | "¿se siente seguro/inseguro en su barrio ante un asalto o robo?" |
| `B18` | antecedente | confianza en la Policía |
| `B10A` | antecedente | confianza en el sistema de justicia |
| `AOJ12` | antecedente | "si fuera víctima, ¿cuánto confiaría en que el sistema judicial castigaría al culpable?" |
| `aoj1` | desenlace, mismo instrumento y misma persona que el antecedente | "¿Denunció el hecho ante alguna institución?" — **condicionado al filtro de victimización del propio módulo** (sólo se pregunta a quien reportó haber sido víctima) |
| `aoj1a` | contexto del desenlace | "¿ante qué institución?" |
| `aoj1b` | contexto del desenlace, **no exigido para el sello** | "¿por qué no denunció el hecho?" — reserva declarada por `N10`: sin abrir el codebook en CAJA no se confirma si sus categorías distinguen desconfianza en la autoridad de una razón puramente instrumental; **no es necesaria para el SI/ENTONCES de la regla**, sólo para probar el `PORQUE` (mecanismo, no antecedente exigible) |

---

## 2 · Universo y ponderador

**Universo pre-registrado, por ola:** adultos de la muestra LAPOP México que respondieron el filtro de victimización del módulo `AOJ` (universo condicional — la regla predice la conducta de quien ya fue víctima, no de la población general). País completo, sin restricción de género (a diferencia de ENDIREH, que `N5` ya usó y que esta pieza no repite — §0.3).

**Ponderador — declarado por precedente citado, no heredado de prosa nueva:** `wt`/`weight1500` según la ola, mismo nombre de columna que `S4 §2` verificó por una corrida real de `L9` (`wt` constante = 1) y que `N7 A.8` cita como precedente de spec LAPOP (`"ponderador wt/weight1500, celdas por ola"`). Esta pieza reutiliza el **nombre**, no re-verifica el valor — CAJA confirma cuál de los dos nombres trae cada ola antes de correr.

---

## 3 · Dicotomizaciones y celdas

**`INSEGURO`** = 1 si al menos una de: `AOJ11`=inseguro, `B18`=baja confianza en policía, `B10A`=baja confianza en sistema de justicia, `AOJ12`=bajo confiaría en castigo (disyunción — el antecedente de la regla es "inseguridad **o** autoridad no confiable", no una conjunción de las cuatro); 0 si ninguna se cumple. Puntos de corte exactos de cada escala pendientes de codebook (CAJA).

**`CALLA`** = 1 si `aoj1` = "No" (no denunció), dentro del universo condicionado a víctima.

### 3.1 · Celdas — contraste de dos brazos, por ola

```
C_ola = P(CALLA=1 | INSEGURO=1, ola) − P(CALLA=1 | INSEGURO=0, ola)
```

**Cota de n mínima por celda:** numerador `< 10` ⇒ esa celda `NO-ESTIMABLE` — misma guardia que `S4`/`S5`/`S6`/`S7` fijan. El riesgo de caer aquí es **mayor que en `S6`/`S7`**: `aoj1` sólo se pregunta a víctimas, y el filtro de victimización reduce el `n` disponible por ola de forma sustancial (no cuantificado en esta pieza, CAJA lo reporta al abrir).

**Agregación entre olas — declarada antes de correr:** el veredicto agregado se declara `CORROBORADA` sólo si **al menos dos olas individualmente estimables** coinciden en signo positivo; una sola ola estimable con signo positivo se reporta como `CORROBORADA-PARCIAL` (mismo vocabulario que `S5`/`L9`/`L11` usan), no como corroboración completa.

---

## 4 · Falsador — signo, y las dos filas que `B-bis` exige

| fila | condición |
|---|---|
| **Signo esperado** | `C_ola > 0` en al menos dos olas estimables (mayor no-denuncia en el grupo inseguro/desconfiado) |
| **`CORROBORADA`** | ≥2 olas con IC95% que excluye 0 en signo positivo |
| **`CORROBORADA-PARCIAL`** | exactamente 1 ola con IC95% que excluye 0 en signo positivo, el resto `NO-ESTIMABLE` o `NO-DISCRIMINA` |
| **`CONTRARIA`** | alguna ola con IC95% que excluye 0 en signo negativo, ninguna positiva |
| **`NO-DISCRIMINA`** | todas las olas estimables tienen IC95% que contiene 0 |
| **`NO-ESTIMABLE`** — **fila que `B-bis` exige, qué pasa si no refuta** | todas las olas caen bajo la guardia de numerador (filtro de victimización deja `n` insuficiente en cada una). **Si cae aquí, el veredicto declara explícitamente que el filtro de victimización del módulo `AOJ` —diseñado para otro propósito— no alcanza a sostener esta celda con los datos disponibles, sin que esto implique nada sobre si el mecanismo de la regla opera o no en México.** No reabre el `EXISTE-NO-SATISFACE` de `N5`/`N6` (§0.3): esas corridas siguen siendo lo que fueron, evidencia sobre un instrumento distinto (ENDIREH/CNGMD). |

---

## 5 · `se_mueve_si`

El objeto se mueve si, dentro de `INSEGURO`=1, la mayoría **sí** denuncia — contradiciendo "ver, oír y callar" como respuesta por defecto al entorno inseguro. También se matiza (no se mueve, pero se anota) si `aoj1b` —abierta en CAJA, no exigida para el sello— muestra que las razones de no-denuncia son mayoritariamente instrumentales ("no tenía pruebas", "pérdida de tiempo") y no de desconfianza en la autoridad: eso afectaría el `PORQUE` (mecanismo), no el `SI/ENTONCES` de la regla, mismo criterio que `N10 §2.6` ya declaró.

---

## 6 · Archivos que la caja necesita abrir

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `1658622845mexico_2004_export_version` | `Descargas Manuales/1658622845Mexico 2004 Export Version.sav` | `e725383552753223d263a1d65e2aaf9549a59859eb1b5777b666f32728700c99` |
| `1008973606mexico_lapop_final_2006_data_set_092906` | (2006, `.sav`) | `f43fcf78533febabe4eacb539f0ed03470c8320d606f29f54c220cda5abb3039` |
| `mexico_lapop_americasbarometer_2019_v1_0_w` | (2019, `.dta`) | `c88f79ebb8e73c473cd78d894eb093261f172e736a35bd7bc677b4e8b1454a57` |
| `mex_2021_lapop_americasbarometer_v1_2_w` | (2021, `.dta`) | `153fb0f81acfffb41bbe247b7fce81159350e1fdfcb342a14bb034bcb7d95566` |
| `mex_2023_lapop_americasbarometer_v1_0_w` | (2023, `.dta`) | `4a9410a53cde9d11edeb23465bdbadce8a6abcc18330b6eebe2a4493be6e765c` |

**Advertencia declarada en el propio manifiesto:** las cinco entradas cargan la nota "URL exacta de descarga NO confirmada" / "NO re-verificada" — no bloquea la lectura del payload ya adquirido, sí significa que el origen de descarga no está re-verificado por este acto (NUBE, sin red utilizable — ver `## CONSUMIDO` de este encargo).

---

## 7 · Qué NO hace este acto

No abre ningún archivo de §6 — `data/raw` ausente en NUBE. No sella `R10.3` en canon. No cierra la lista de olas variable por variable (a diferencia de `S5`) — declarado como primer paso de CAJA, no adivinado. No reabre las corridas `EXISTE-NO-SATISFACE` de `N5` (ENDIREH) ni `N6` (CNGMD) sobre este `id` — las cita como continuidad de instrumento distinto (§0.3). No exige `aoj1b` para el sello del `SI/ENTONCES` — declarado mecanismo, no antecedente, mismo criterio que `N10`.

**Medición: caja, acto `MAESTRA38-L8`** — nombre nuevo, asignado por este pre-registro; sin colisión verificada (`grep -rn "MAESTRA38-L8"` → 0 apariciones previas).

**El primer resultado que produzca este procedimiento es el que se reporta.**
