# S6 · Pre-registro de `salud.atencion.grave` — objeto verbatim del canon (`R4.4`)

### `prereg-caja-S6-L6` · **v1.0** · 5 de septiembre de 2026

| ARCHIVO | `forense/prereg-caja/S6-L6-spec-v1_0.md` |
|---|---|
| NOMBRE ESTABLE | `prereg-caja-S6-L6` — cítese por este nombre, nunca por la ruta de archivo |
| QUÉ ES | Pre-registro congelado de la regla `salud.atencion.grave` (`R4.4`), clasificada `MEDIBLE-COMO-ESTÁ` *(propuesta, dirección revisa)* por `ACTO MAESTRA38-N10 · COBERTURA-COMPLETA-OLA6` §2.2 |
| QUÉ NO ES | No mide nada de México. No abre microdato. No sella `R4.4` en canon — la clasificación sigue `(propuesta)` hasta que dirección la revise |
| VERIFICAS ASÍ | `sha256sum -c S6-L6-spec-v1_0.sha256`; el acto futuro `MAESTRA38-L6` compara su primer resultado real contra esta spec congelada, nunca la corrige hacia atrás |

**Acto:** `ACTO MAESTRA38-N11 · PRE-REGISTRO-OLA6-MEDIBLES-Y-FICHAS`, 5/sep/2026, entorno **NUBE**, sobre `origin/main = b17d19bd` (exacto al arrancar, sin desfase; `data/raw` ausente, esperado en NUBE — ningún microdato abierto en esta pieza).

---

## 0 · Ficha bajo prueba — continuidad con Hito D, N5 y N10

### 0.1 · Definición vigente, verbatim de `canon/modelo-decision-v4_0.md:526`

> **SI** el síntoma es grave o crónico complejo **ENTONCES** busca el sistema público pese a la espera — PORQUE la complejidad excede al consultorio — `[MEDIA]`. · **id:** `salud.atencion.grave`

Cruce `§7`: `` | `R4.4` | L241 | Grave/crónico complejo → sistema público pese a la espera | `[MEDIA]` | No | `` — la columna final ("¿ficha en Hito D?") es **No**: confirmado por A.8 de este acto (ver 0.2), `R4.4` **no** está entre las 27 reglas del perímetro de Hito D.

### 0.2 · A.8 contra Hito D — ausencia verificada, no asumida

`tools/ya_medido.py R4.4` (corrido en esta pieza, salida completa pegada más abajo en §0.4) sólo encuentra `canon/modelo-decision-v4_0.md:747` (la fila de la tabla `§7`, sin veredicto adjunto) — ninguna coincidencia con el bloque de veredictos `A`–`E` de `§7` (línea 704 y siguientes) ni con `forense/hitoD-preregistro-v2_0.md`. Verificado además por lectura directa: la lista de 26 `R-n` con veredicto archivado en `§7` (línea 704: `R1.1, R3.2, R7.2, R4.2, R4.1, R9.1, R4.3, R9.2, R5.1, R5.2, R1.2, R3.1, R1.3, R8.1, R7.1, R7.3, R7.4, R7.5, R8.3, R1.4, R10.2, R8.2, R2.2, R3.4, R10.1, R2.1`) **no contiene `R4.4`**. Este pre-registro es, hasta donde el repo permite verificar, el primer intento de falsación pre-registrado sobre este `id`.

### 0.3 · Objeto verbatim de `N10 §2.2`, sin reformular

`ACTO MAESTRA38-N10` (5/sep/2026) propuso `MEDIBLE-COMO-ESTÁ` bajo el criterio "antecedente y desenlace en la misma persona, en el mismo instrumento": disparador `es09 HA TENIDO PROBLEMA SALUD GRAVE` + `es09a` (ENNViH, ventana de 4 años); desenlace `cen10*` (ENNViH, **mismo instrumento**, lugar de consulta), corroborado —no requerido para el sello— por `p6_15_8_*`/`p6_17_8` (ENDIREH 2016, público vs. privado, población distinta: mujeres, contexto de violencia). El "pese a la espera" del `PORQUE` es mecanismo, no antecedente exigible — mismo criterio que `N5` ya aplicó aquí (`forense/notas/2026-09-03-mapeo-ola6-N5.md:59`, veredicto `EXISTE-SATISFACE (propuesta)`). Este pre-registro **no reformula el objeto**: lo congela tal como `N5`/`N10` lo dejaron, con las variables verificadas contra el inventario (§1).

### 0.4 · `tools/ya_medido.py`, salida completa

```
$ python3 tools/ya_medido.py R4.4
=== ya_medido: R4.4 ===
  resuelto por canon: R4.4 -> id `salud.atencion.grave` (canon/modelo-decision-v4_0.md §3, tag **id:**)
  términos de búsqueda (match exacto): R4.4, salud.atencion.grave

-- milpa/tramite.yaml --
  (sin apariciones)
-- milpa/tramite-ola5-propuesta-v0.yaml --
  (sin apariciones)
-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:747  tier=[MEDIA]
      | `R4.4` | L241 | Grave/crónico complejo → sistema público pese a la espera | `[MEDIA]` | No |
-- forense/notas/*-L*-*.md --
  (sin apariciones)
-- forense/prereg-caja/S*-spec-*.md --
  (sin apariciones)
-- canon/registro-rotulos.tsv (alias) --
  (sin apariciones)
========================================
NUNCA-MEDIDA
```

`NUNCA-MEDIDA`, sostenido por lectura de las apariciones (no sólo por la línea final): la única aparición en `§7` es la fila de la tabla cruzada, sin veredicto — consistente con 0.2.

---

## 1 · Variables — texto de reactivo copiado del inventario, no parafraseado

| variable | instrumento | ¿en qué libro/ola? | etiqueta verbatim |
|---|---|---|---|
| `es09` | ENNViH-3 (2009) | Libro III (individual, adulto) — declarado por convención de prefijo `es`=«encuesta de salud»; **no verificado columna por columna en esta pieza NUBE**, CAJA lo confirma antes de abrir | `HA TENIDO PROBLEMA SALUD GRAVE` |
| `es09a` | ENNViH-3 (2009) | íd. | detalle/seguimiento del problema declarado en `es09`, ventana de 4 años (citado así por `N5`/`N10`, texto exacto de la sub-pregunta pendiente de confirmar contra el cuestionario en CAJA) |
| `cen10*` (familia de columnas) | ENNViH-3 (2009) | íd., **mismo instrumento que `es09`** | lugar/institución de consulta (familia `cen10a`.. — la CAJA resuelve el sufijo exacto contra el codebook) |
| `p6_15_8_*` / `p6_17_8` | ENDIREH 2016 | módulo de atención por violencia (`TB_SEC_VI_2.csv`) | lugar de atención: público (`institución pública de salud`) vs. `consultorio médico, clínica u hospital privado` — **corroboración, no requisito**: población de mujeres víctimas de violencia, no la población general de la regla |

**Declarado, no verificado (A.13):** el manifiesto no indexa ENNViH por variable — cada `id` de manifiesto es el ZIP completo de un libro/ola (confirmado por búsqueda exhaustiva en `data/manifiesto.yaml`, cero coincidencias de `es09`/`cen10` como texto). La cita de arriba es al nivel de bundle (§6); CAJA localiza la columna exacta dentro del `.dta` correspondiente antes de correr.

---

## 2 · Universo y ponderador

**Universo pre-registrado:** personas del Libro III de ENNViH-3 (2009) con respuesta válida en `es09` (declararon haber tenido un problema de salud grave o crónico complejo en la ventana de 4 años) — la regla es condicional: predice **a dónde se acude dado que se tuvo el problema**, no si se tiene el problema. Sin restricción adicional de derechohabiencia (`segsoc`): la regla no la exige, a diferencia de `salud.atencion.leve_sin_imss`.

**Ponderador — búsqueda exhaustiva por payload previo, ninguna heredada de prosa nueva:** `fac_3a` (Libro IIIA, individual, transversal) — columna verificada por lectura real de cabeceras `.dta` en `ACTO RECENSO-DISENO-14` (`forense/notas/2026-08-24-recenso-diseno.md:114`: *"`data/raw/ennvih/ehh09w_all.zip` trae un `.dta` por «libro» con las columnas `fac_1, fac_2, fac_3a, fac_3b, fac_4, fac_5, fac_c, fac_ea, fac_en, fac_s`"*) — no una cifra inventada para esta pieza. Se reutiliza el **nombre** de columna, ya confirmado por esa lectura anterior en CAJA; el valor no se ha corrido. Se reporta también sin ponderar, como corroboración (mismo criterio que `ficha-id-g3` §7). `FP-118` advierte que ENNViH no tiene diseño de varianza completo en este corpus (sin estrato/UPM confiables) — cualquier IC de esta pieza declara el supuesto de muestreo aleatorio simple, mismo criterio que la mesa ya fijó (`FP-118 FIRMADA`, opción (i)).

---

## 3 · Dicotomizaciones y celdas

**`GRAVE`** = 1 si `es09` = 1 (tuvo problema de salud grave/crónico complejo en la ventana); universo restringido a esta subpoblación (la regla no predice nada sobre quien no tuvo el problema).

**`BUSCA_PUBLICO`** = 1 si `cen10*` codifica una institución del sistema público (IMSS/ISSSTE/SSA/Seguro Popular-INSABI, sufijo exacto pendiente de CAJA); 0 si privado, farmacia con consultorio, o no buscó atención.

### 3.1 · Celda — una proporción, no un contraste de dos brazos

La regla, tal como está escrita, no predice un contraste entre dos grupos (a diferencia de `R4.1`, que si tuviera dato compararía derechohabientes vs. no): predice que, **dado `GRAVE`=1**, la mayoría busca el sistema público. El diseño es de una sola celda:

```
C = P(BUSCA_PUBLICO=1 | GRAVE=1) − 0.5
```

**Cota de n mínima:** numerador (`BUSCA_PUBLICO`=1 dentro de `GRAVE`=1) `< 10` ⇒ `NO-ESTIMABLE` — misma guardia que `S4 §3`/`S5 §3.1`/`L9 §1.3` fijan, no se reinventa un umbral distinto.

**Estratificación secundaria, no requerida para el sello:** repetir `C` dentro de `segsoc`=2 (sin IMSS) — si el patrón se sostiene igual con y sin seguridad social, refuerza que el mecanismo es la gravedad, no el acceso; si sólo se sostiene en un estrato, se declara como hallazgo adicional, no cambia el veredicto principal.

---

## 4 · Falsador — signo, y las dos filas que `B-bis` exige

| fila | condición |
|---|---|
| **Signo esperado** | `C > 0` (mayoría busca sistema público), IC95% que excluye 0 |
| **`CORROBORADA`** | `C` estimable, IC95% excluye 0 en signo positivo |
| **`CONTRARIA`** | `C` estimable, IC95% excluye 0 en signo negativo (mayoría **no** busca público) |
| **`NO-DISCRIMINA`** | IC95% de `C` contiene 0 |
| **`NO-ESTIMABLE`** — **fila que `B-bis` exige, qué pasa si no refuta** | numerador `< 10` dentro de `GRAVE`=1 (ventana de 4 años puede dejar la subpoblación chica en algunas olas de comparación). **Si cae aquí, el veredicto sale de la corroboración sin ponderar (§2) como diagnóstico, y se declara explícitamente que el corazón de la regla —qué hace la mayoría de quienes tuvieron un problema grave— no se pudo medir con este instrumento**, no que la regla sea falsa ni verdadera. |

---

## 5 · `se_mueve_si`

El objeto se mueve (dejaría de sostenerse como está escrito) si una mejora documentada de acceso al sistema público (costo, tiempo, trato — mismo eje que `D-04` fija para `salud.atencion.leve_sin_imss`) coincide con una caída de `BUSCA_PUBLICO` en vez de una subida: eso apuntaría a que la elección no es por gravedad sino por otra dimensión no capturada por `es09`/`cen10*`. Este pre-registro no tiene el dato de "antes/después" de una mejora de acceso — se declara como condición de movimiento, no como diseño que esta pieza vaya a correr.

---

## 6 · Archivos que la caja necesita abrir

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `ennvih3_2009_hogar_dta` | `ennvih/ehh09dta_all.zip` | `00a7649a1839a3523be22612c2fa3555d5e743cf5329d6bcdc432b901e98bd15` |
| `ennvih3_2009_ponderador_transversal` | `ennvih/ehh09w_all.zip` | `e7929b49a7cd4f1eae5aa17da77c7eea4794d0f26265fbd40dde5e9c8e3ef8b8` |
| `endireh_2016_bd_mujeres_endireh2016_sitioinegi_csv` *(corroboración, no requerido)* | `endireh2016/bd_mujeres_endireh2016_sitioinegi_csv.zip` | `02c06ab73a53942ddb575e3e35d8c1dd775406277b74e0605735e3eced4e6f10` |

**Advertencia sobre el id `endireh_2016_..._dbf`** (no usado aquí): el manifiesto marca esa variante `retirada` — su sha256 declarado no coincidía con el archivo en disco; usar el `_csv` o `_dbf_redescarga`, nunca el `_dbf` original.

---

## 7 · Qué NO hace este acto

No abre ningún `.dta`/`.zip` de los listados en §6 — `data/raw` está ausente en esta sesión NUBE, confirmado (`ls data/raw/` → no existe), consistente con A.3 del `/acto`. No sella `R4.4` en `canon/modelo-decision-v4_0.md` — sigue `(propuesta)`, dirección revisa antes de mover el tier. No corrige la anomalía de dominio de ningún otro `id` (ver `S7`). No reabre ni discute ningún veredicto de Hito D — confirmado que `R4.4` no tiene uno (§0.2). No inventa el nombre de la sub-columna exacta de `cen10*` ni la codificación de `es09a` — declarado pendiente, no adivinado.

**Medición: caja, acto `MAESTRA38-L6`** — nombre nuevo, asignado por este pre-registro (D-13: no heredado de prosa de un encargo anterior); verificado sin colisión: `grep -rn "MAESTRA38-L6"` contra el árbol al escribir esta pieza → 0 apariciones previas.

**El primer resultado que produzca este procedimiento es el que se reporta.**
