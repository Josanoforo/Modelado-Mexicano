# `ADV1-M5` · escala de cinco casillas del piloto — 20/ago/2026

**Acto:** `DUELO-PREREG-V2` (nube, Opus; gate `T-SELLO` + `ACT-PIL-2` fusionados). Nombre estable de este mecanismo: **`ADV1-M5`** — nunca el rótulo pelado a secas (colisiona con el mismo rótulo pelado usado en `ADR-MOTOR-2-esqueleto`, mecanismo distinto).

**Fuente:** copiado VERBATIM de `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B, párrafo `ADV1-M5` (única definición de la escala en el corpus). Sin edición de cuerpo — cualquier palabra fuera del bloque en cursiva de abajo es aparato de este acto, no del careo.

**Firma que la ancla, citada junto a la tabla (`D-ii`, `TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md` §4 y `CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §C, texto idéntico en ambos, FIRMADA 19/ago/2026):**

> **D-ii** · "Firma la tabla de cinco casillas de `ADV1-M5` antes de la primera celda — 'incluso un piloto imperfecto es seguro si su peor resultado deja de ser pivote estratégico y pasa a ser dato'." — FIRMADA 19/ago.

## Estado de este documento: **NO SELLADO — COMPUERTA B-bis ACTIVADA**

Este acto verificó, antes de sellar, si el texto de la careo especifica con claridad (a) qué significa que "el falsador no refute" y (b) la precedencia entre las cinco casillas cuando más de una condición aplica a la vez a una misma celda o al conjunto del piloto. Resultado de la verificación, por comando sobre el árbol completo (`forense/`, `canon/`, `forense/adv-duelo/`):

```
grep -rn "falsador\|refute\|refuta\|precedencia" forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md \
    forense/TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md forense/adv-duelo/*.md
# → sin resultados
```

Ni "falsador" ni "refute"/"refuta" ni "precedencia" aparecen en ninguno de los cinco documentos fundacionales del duelo. La frase "el falsador no refute" no tiene definición operativa en el corpus citable — no es que esté implícita y haya que interpretarla; es que el término no existe en el texto que `ADV1-M5` sella. Y el propio párrafo `ADV1-M5` no ordena sus cinco casillas: no dice qué prevalece si, por ejemplo, la casilla (3) *Empate-TOST dentro de banda pre-declarada* y la casilla (5) *ambos fuera del IC de R en la mayoría* describen condiciones compatibles sobre el mismo conjunto de celdas (una celda puede estar dentro de la banda TOST de L vs M y a la vez ambos corredores fuera del IC de R — son ejes distintos, uno mide L contra M y el otro mide cada corredor contra R, y el texto no dice cuál gobierna la lectura del piloto cuando ambos aplican).

Conforme a la instrucción de arranque de este acto (COMPUERTA B-bis): **este acto PARA de escribir `ADV1-M5` como sellada.** No se aplana ni se inventa la ambigüedad. Las dos preguntas abiertas quedan documentadas, sin resolver, en `forense/prereg-duelo-v2/mesa-pendientes.md` §1 y §2, para decisión humana.

Lo que SÍ queda fijo por este acto, porque no es ambiguo en el texto: el contenido verbatim de las cinco casillas (abajo), su nombre estable `ADV1-M5`, y la cita de `D-ii` junto a ellas. Lo que NO queda fijo: la interpretación operativa de "el falsador no refute" (inexistente en el corpus — hay que preguntar a mesa si es una paráfrasis de otra cosa, ver mesa-pendientes §1) y el orden de precedencia entre casillas cuando compiten (mesa-pendientes §2).

## Texto verbatim — `ADV1-M5` (`CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B, párrafo `ADV1-M5`)

> **ADV1-M5 · Tabla de consecuencias, cinco casillas, firmada antes de la primera celda.** (1) L más cerca → "en estos momentos el canal LLM quedó más cerca del dato"; NO licencia "el motor sobra" (procedencia, contrafactuales e interpretabilidad no se puntuaron). (2) M más cerca → "el motor transportó mejor que la memoria del LLM"; NO licencia "M es bueno" salvo skill material sobre B. (3) Empate-TOST dentro de banda pre-declarada. (4) **Ninguno supera a B** → ninguno utilizable v1; re-tierización dirigida sin coronación. (5) **Ambos fuera del IC de R en la mayoría** → el fenómeno no es predecible con estas herramientas hoy; consecuencia propia, y es la casilla que el FFC dice esperar. Cláusula de alcance: ningún resultado autoriza abandonar L ni M para usos no muestreados — el duelo mide estimación de cantidades encuestables y nada más.

## Cierre

Este documento no autoriza a ningún acto sucesor a tratar `ADV1-M5` como sellada para efectos de adjudicar una celda o el piloto completo mientras las preguntas de `mesa-pendientes.md` §1-§2 sigan abiertas. Cuando mesa responda, este archivo se actualiza (mismo nombre, misma ruta) para pasar de NO SELLADO a SELLADO, citando el ADR/firma que lo resuelva.
