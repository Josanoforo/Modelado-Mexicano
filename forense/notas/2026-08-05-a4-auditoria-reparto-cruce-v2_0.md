# Auditoría del reparto de veredictos — `cruce-catalogo-fichas-v2_0.md`

*5 de agosto de 2026. Acto A4, mesa. Rama `claude/audit-reparto-cruce-dof-0xqo7u`. Base: `origin/main` en
`32d9321` (Merge PR #100), que ya incluye `9729894` (base declarada del encargo) como ancestro directo —
`main` avanzó un merge entre la declaración del encargo y la apertura de esta sesión; sin discrepancia que
bloquee, reportado por disciplina.*

**Qué es este documento y qué no es.** Nota forense de auditoría — no edita `forense/cruce-catalogo-fichas-v2_0.md`
(append-only, CONTRIBUTING §3) ni ninguna ficha de `hitoD-preregistro-v2_0.md`. No adjudica ningún
veredicto `RX.Y`. Responde la pregunta de mesa: de las tres cifras circulando para el reparto del cruce
v2.0, ¿cuál se deriva mecánicamente del archivo y por qué difieren las otras dos?

---

## 1 · Receta y salida cruda

**Regla seguida:** parsear la columna `Veredicto` (última columna) de cada una de las 7 tablas `§3.x` del
archivo, fila por fila — no contar ocurrencias de palabras sobre el archivo completo. Script en
`/tmp/.../scratchpad/parse_cruce.py` (sesión), ejecutado contra el archivo real:

```
$ python3 parse_cruce.py
=== 32 filas de datos encontradas en 7 tablas ===

--- Conteo por PRIMER token de veredicto en la celda (1 voto por fila) ---
  VIABLE: 10
  VIABLE ECOLÓGICO: 5
  NO ENLAZA: 3
  NO EXISTE: 14
  SIN_TOKEN_RECONOCIBLE: 0
  TOTAL filas: 32

--- Filas con MÁS DE UN token de veredicto distinto en la misma celda ---
  L67 R3.4: VIABLE ECOLÓGICO + NO ENLAZA
  L78 R5.1: VIABLE ECOLÓGICO + VIABLE
  L102 R9.2: VIABLE ECOLÓGICO + NO EXISTE

--- Filas sin bold **VIABLE**/... al inicio (veredicto en prosa, no forma canónica de celda) ---
  L48 R1.1: "VIABLE ECOLÓGICO en el mejor caso — solo si el padrón (arriba) apareciera..."
  L50 R1.3: "VIABLE, a nivel de penetración/brecha..."
  L65 R3.1: "VIABLE en diseño — corrida completa pendiente de adjudicación..."
```

**Resultado: `32 · 14 NO EXISTE · 10 VIABLE · 5 ECOLÓGICO · 3 NO ENLAZA`.** Coincide exacto, dígito por
dígito, con la fila **"Columna Veredicto de sus 7 tablas"** de la tabla de mesa. Esa cifra es la única de
las tres que se reproduce con una receta mecánica y reproducible sobre el archivo real.

---

## 2 · La brecha entre las tres cifras

### 2.1 · "Los dos documentos de traspaso" (48 · 21 · 13 · 7 · 7) — grep crudo sobre el archivo completo

Hipótesis probada: que esta cifra es un conteo LITERAL de ocurrencias de las cuatro palabras sobre **todo**
el archivo (prosa incluida), justo lo que el encargo prohíbe. Verificado:

```
$ python3 - <<'EOF'
import re
texto = open("forense/cruce-catalogo-fichas-v2_0.md", encoding="utf-8").read()
no_existe = len(re.findall(r"NO EXISTE", texto))
viable_eco = len(re.findall(r"VIABLE ECOLÓGICO", texto))
no_enlaza = len(re.findall(r"NO ENLAZA", texto))
viable_solo = len(re.findall(r"VIABLE\b", texto)) - viable_eco
print(no_existe, viable_eco, no_enlaza, viable_solo, no_existe+viable_eco+no_enlaza+viable_solo)
EOF
21 7 7 13 48
```

**Coincide exacto con `48 · 21 · 13 · 7 · 7`.** El desglose de dónde viven esas 16 menciones de más
(48 − 32) que no están en ninguna fila de tabla:

- **6 en la leyenda** (`## Veredictos, los cuatro valores y su lectura`, líneas 30-39) — cada uno de los
  cuatro valores se **define** ahí una vez (dos veces `VIABLE`, porque `VIABLE ECOLÓGICO` contiene la
  palabra `VIABLE`), y `NO EXISTE` se repite una segunda vez en la aclaración de la propia leyenda
  ("no se marca NO EXISTE por default", línea 39).
- **7 en el §Resumen mismo** (líneas 117-120) — el propio resumen, al **citarse a sí mismo en prosa**
  ("**7 VIABLE**, **6 VIABLE ECOLÓGICO**... **5 NO ENLAZA**, **~16 NO EXISTE**"), genera nuevas
  coincidencias para un grep ciego: cuenta su propio conteo como si fueran filas adicionales.
- **1 en "Lo que este documento no hace"** (línea 135), citando la palabra `"NO EXISTE"` entre comillas
  como advertencia de estilo, no como veredicto de ninguna fila.
- El resto de la diferencia son las **segundas menciones dentro de celdas mixtas** (R3.4, R5.1, R9.2) que
  el conteo de "primer token" no cuenta dos veces pero el grep crudo sí.

**Los "dos documentos de traspaso" no están en este clon** (se buscó `TRANSFER-maestra-8.md`
y `TRANSFER-maestra-9.md`, y por nombre de archivo/contenido con `grep -rl "traspaso"` en todo el repo — ninguno contiene
`48`/`21`/`13`/`7`/`7` junto a estos rótulos). No se puede verificar su método de conteo directamente; lo
que sí se puede verificar, y se verificó arriba, es que **su cifra es exactamente reproducible con un grep
ingenuo de palabra sobre el archivo completo** — el defecto exacto que el encargo advirtió no cometer. Se
reporta como hallazgo, no como acusación: no hay forma de confirmar *cómo* se generó esa cifra sin ver el
documento, pero sí de mostrar que el archivo del cruce, leído de la forma incorrecta, produce ese número
exacto.

### 2.2 · El §Resumen (~34 · ~16 · 7 · 6 · 5) — cuenta por condición, no por fila, con ambigüedad reconocida

El propio §Resumen (líneas 116-121) declara la fuente de su tilde: *"La proporción exacta depende de cómo
se cuenten las fichas con condiciones mixtas... no se colapsa a una sola cifra por ficha porque la
pregunta de este acto es por condición, no por ficha."* Esto es honesto y verificable: las tres filas
mixtas (R3.4, R5.1, R9.2-segunda) empaquetan **dos condiciones o dos lecturas de una condición** en una
sola celda de la tabla física. Repartir cada una de esas tres filas en dos "condiciones" en vez de una
sube el total de 32 físicas a un rango 33-35 según cuántas de las tres se partan — de ahí el **32 → ~34**
y la tilde. No se intentó forzar una regla de partición que reproduzca 34/16/7/6/5 exacto porque el propio
documento renuncia explícitamente a comprometerse con una — inventar una regla "descubierta" sería
retropropagación fabricada, no auditoría. **Se confirma el porqué del `~`: no es descuido, es una
ambigüedad de conteo declarada por escrito en el mismo documento que la usa.**

### 2.3 · Ocurrencias que viven en prosa, no en forma canónica de celda

Tres filas dan su veredicto en prosa suelta, sin el `**negrita**` que usan las otras 29: `R1.1` (segunda
fila, condicional — *"VIABLE ECOLÓGICO en el mejor caso"*, dependiente de un padrón que la fila anterior
ya declara no buscado), `R1.3` (primera fila, *"VIABLE, a nivel de penetración/brecha"*) y `R3.1`
(*"VIABLE en diseño — corrida completa pendiente de adjudicación"*). El parser las cuenta igual (toma el
primer token reconocible venga o no en negrita) — se documentan aquí porque son las candidatas más débiles
si alguien quisiera exigir forma canónica estricta para "contar", análogo a como T18 exige forma canónica
estricta para los veredictos `RX.Y` archivados (ver §3).

**Conclusión de mesa recomendada:** la cifra a usar para priorizar es **`32 · 14 NO EXISTE · 10 VIABLE ·
5 ECOLÓGICO · 3 NO ENLAZA`** — la única derivada con receta mecánica reproducible. El `~34` del §Resumen
es válido para lo que mide (condiciones, no filas) pero no reproducible sin una regla de partición que el
documento mismo se niega a fijar. El `48` de los documentos de traspaso no se puede verificar desde este
clon y coincide exactamente con el patrón de conteo que el encargo prohibió.

---

## 3 · Verificación de la afirmación de mesa: "solo `R1.3` y `R3.1` de las VIABLE carecen de veredicto archivado"

**Fichas cuya fila primaria en el cruce es `VIABLE`** (9 distintas, de las 10 filas del §1): `R1.2`,
`R1.3`, `R3.1`, `R3.2`, `R4.2`, `R4.3` (A y B), `R5.2`, `R7.2`, `R9.2`.

**Receta de T18 corrida directamente contra el archivo real** (mismo regex de `tests/check.py:684`, no la
prosa de `estado-programa`):

```
$ python3 - <<'EOF'
import re, glob
h = sorted(glob.glob("forense/hitoD-preregistro-v*.md"))[-1]
texto = open(h, encoding="utf-8").read()
m = re.search(r"^## Registro de veredictos archivados.*$", texto, re.M)
bloque = texto[m.end():]
VEREDICTO_CANONICO = re.compile(r"`(R\d+\.\d+)`\s*→\s*veredicto\s*`([A-E])`")
for l in bloque.split("\n"):
    mm = VEREDICTO_CANONICO.search(l)
    if mm: print(mm.group(1), "->", mm.group(2))
EOF
R1.1 -> D
R3.2 -> B
R7.2 -> D
R4.2 -> D
R4.1 -> D
R9.1 -> D
R4.3 -> D
R4.3 -> D
R9.2 -> D
R5.1 -> A
R5.2 -> A
R1.2 -> E
```

**Fichas archivadas (11, `set()` como hace T18 sobre `R4.3` que aparece dos veces):** `R1.1, R1.2, R3.2,
R4.1, R4.2, R4.3, R5.1, R5.2, R7.2, R9.1, R9.2`.

**Cruce contra las 9 VIABLE:**

| Ficha VIABLE | ¿Archivada? |
|---|---|
| R1.2 | Sí — `E` |
| **R1.3** | **No** |
| **R3.1** | **No** |
| R3.2 | Sí — `B` |
| R4.2 | Sí — `D` |
| R4.3 | Sí — `D` (mitad A y mitad B) |
| R5.2 | Sí — `A` |
| R7.2 | Sí — `D` |
| R9.2 | Sí — `D` |

**Afirmación de mesa CONFIRMADA, verbatim, con receta reproducible:** exactamente `R1.3` y `R3.1` faltan.
Nada más se toca (no se adjudica veredicto para ninguna de las dos, no se edita el bloque append-only).

---

## 4 · Filas `NO EXISTE` contra `data/catalogo-fuentes-v2_0.md` y `data/inventarios/` de hoy

14 filas primarias `NO EXISTE`. Vocabulario usado abajo, sin colapsar los tres casos entre sí (regla del
encargo): **"sigue cierto"** (se buscó en catálogo/inventarios de hoy y sigue sin aparecer fuente) ·
**"hallazgo"** (hay una fuente o candidata en el catálogo/inventario de hoy que la fila no cita) ·
**"pendiente — exige red"** (resolverlo del todo requiere salir a verificar fuera del catálogo, no se
intentó).

**Primero, el chequeo específico que pide el encargo — los cuatro casos que fallaron el 4/ago (ENASEM,
ENSANUT, CLUES, Cero Desabasto):**

```
$ grep -n -i -E "ENASEM|ENSANUT|CLUES|Cero Desabasto" forense/cruce-catalogo-fichas-v2_0.md
```

Las cuatro aparecen en el cruce v2.0 — pero **como fuentes candidatas citadas** en filas `VIABLE`/`NO
ENLAZA`/mixtas (`R4.2`, `R4.3-A/B`, `R9.1`, `R9.2` usan ENSANUT/CLUES/Cero Desabasto), nunca dentro de una
fila `NO EXISTE`. **El defecto puntual del 4/ago no se repite en este documento**: ninguna de las 14 filas
`NO EXISTE` declara inexistente a ninguna de las cuatro fuentes que ese barrido confundió con "sin
payload" el 4/ago.

**Recorrido fila por fila:**

| Ficha | Tema | Verificación contra catálogo/inventarios de hoy | Estado |
|---|---|---|---|
| R1.1 | Fondos de Aseguramiento Agrícola/AGROASEMEX | `grep -rni "AGROASEMEX\|Aseguramiento Agrícola" data/` → 0 resultados | Sigue cierto — y la fila ya declara su propia reserva ("no se buscó específicamente"), consistente con no encontrarlo |
| R1.3 (2ª) | Canal de alta de fintech (dato propietario) | Clase Regulador no-INEGI/CNBV no publica esto por diseño; sin hallazgo en catálogo | Sigue cierto |
| R1.4 | Panel de consumo D/E por marca | `grep -rni "panel de consumo"` en catálogo+inventarios → 0; único "consumo" relevante es cartera crediticia (Banxico), no panel de marca | Sigue cierto |
| R2.1 | Clima organizacional / reporte de errores | `grep -rni "clima organizacional"` → 0 | Sigue cierto |
| R2.2 | Rotación/productividad, liderazgo | STPS "Información Laboral" (`inventario_fuentes_trabajo_ingreso_formalidad_mexico.md` #21) existe pero es **PDF agregado por entidad, sin microdato, sin variable de liderazgo/clima** — no cubre la granularidad pedida | Sigue cierto, con la fuente más cercana ya descartada por granularidad, no por ausencia |
| R4.1 (1ª) | Panel/evento fechado, farmacia-con-consultorio | La fila misma ya cita SINERHIAS como candidata parcial, no verificada — reserva ya declarada correctamente (Tarea D) | Sigue cierto, ya hedged |
| R7.3 | Diseño RDD listo | La fila ya reconoce que PUB+INE existen por separado; lo que falta es el cruce construido, no la fuente | Sigue cierto (es hueco de diseño, no de fuente) |
| R7.4/R7.5 | Registro de eventos de protesta/autodefensa | `grep -rni "protesta\|autodefensa\|conflicto"` en `inventario_fuentes_seguridad_justicia_mexico.md` → 0; clase Transparencia/sociedad civil del catálogo trae solo 2 fuentes (Cero Desabasto, MCCI), ninguna es registro de eventos | Sigue cierto |
| **R8.1** | **Inventario de comités con mecanismo de sanción** | `inventario_fuentes_capital_social_mexico.md:258`, tabla "Fuentes que se sospecha existen pero no pudieron confirmarse": **"Registros de comités de contraloría social y comités de obra — Secretaría de Bienestar, Secretaría de la Función Pública — falta verificar: publicación como bases descargables"** | **Ni "sigue cierto" ni "existe": nadie corrió el mecanismo de resolución contra esta fuente.** Es un lead ya catalogado (no confirmado, tabla F de la propia disciplina del inventario) que la fila `NO EXISTE` de R8.1 no cita ni descarta — dice "no hay padrón ni registro administrativo de comités vecinales identificado en el barrido", pero el barrido de R8.1 no llegó hasta esta entrada del inventario de capital social, que sí la nombra como sospecha sin confirmar. **Pendiente — exige red** (verificar si Bienestar/Función Pública publican la base) |
| R8.2 | Tandas digitales, plataforma propietaria | `grep -rni "tandas"` → 0 en catálogo/inventarios | Sigue cierto |
| R9.1 (2ª) | Variable de "no consultó a nadie" dentro de ENSANUT | No es hueco de fuente sino de diseño de cuestionario dentro de un instrumento que sí existe — no aplica verificación de catálogo | Sigue cierto (clase distinta, ya bien etiquetada) |
| R10.1 | Estudio académico Félix-Brasdefer, actos de habla | No es dato de encuesta/registro por diseño — no aplica catálogo | Sigue cierto (clase distinta, ya bien etiquetada) |
| R10.2 | Retro pública/privada, dato organizacional propietario | Mismo vacío de clase que R2.1/R2.2 | Sigue cierto |
| R10.3 | Testificar tras protección a testigos | Bloqueo ético declarado explícitamente por la propia ficha, no ausencia de dato — no aplica catálogo | Sigue cierto (y la fila ya lo dice: "preferible que así sea") |

**Un hallazgo real, tipo tercero (ni "no existe" confirmado ni "existe" confirmado):** `R8.1` cita un
candidato en `data/inventarios/inventario_fuentes_capital_social_mexico.md:258` que la sesión que escribió
el cruce v2.0 no parece haber cruzado. No se afirma aquí que el registro exista utilizable (la propia
entrada del inventario lo marca sin confirmar) — se afirma que **nadie corrió el mecanismo de resolución
contra él**, que es exactamente la tercera categoría que el encargo pidió no colapsar con las otras dos.
Queda para que mesa decida si amerita una fila de excepción en un v2.1 del cruce (no se toca el archivo
append-only desde esta nota).

---

## Lo que este acto no hizo

No editó `forense/cruce-catalogo-fichas-v2_0.md` ni ninguna ficha de `hitoD-preregistro-v2_0.md`. No
adjudicó ningún veredicto `RX.Y`. No abrió microdato ni red (el chequeo de R8.1 se resolvió con catálogo e
inventarios locales; verificarlo del todo — si Bienestar/Función Pública publican esa base — exige red y
queda nombrado como pendiente arriba, no resuelto aquí).
