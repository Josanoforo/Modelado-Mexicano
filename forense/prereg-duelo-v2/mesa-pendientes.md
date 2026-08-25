# Mesa — pendientes de decisión humana, `DUELO-PREREG-V2`

**Acto:** `DUELO-PREREG-V2`, nube, Opus, 20/ago/2026. Gate: `T-SELLO` + `ACT-PIL-2` fusionados. Este archivo nace con este acto; queda abierto — mesa añade su resolución cuando decida, sin que el ejecutor la anticipe.

Regla que gobierna este archivo: cuando el texto fuente no especifica con claridad una decisión que un acto de escritura necesitaría tomar por su cuenta, el acto documenta las opciones y para — no decide en lugar de mesa (regla general del programa; aplicada aquí a la COMPUERTA B-bis de `DUELO-PREREG-V2` y a la definición de `⊕` del corredor E).

---

## §1 · "El falsador no refute" — término sin definición operativa en el corpus

**Origen del término:** aparece en la cabecera del acto que produjo este documento (encargo de mesa, no en el corpus forense). Verificado por comando (ver `forense/escala-cinco-casillas-piloto-v1_0.md`) que ni "falsador" ni "refute"/"refuta" existen en `CAREO-ADV-DUELO-diseno-v2-2026-08-19.md`, `TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md`, ni en los cuatro informes adversariales de `forense/adv-duelo/`.

**Lecturas candidatas, ninguna elegida por este acto:**

1. **Lectura popperiana literal** — "el falsador" = quien intenta refutar un corredor (L o M) mostrando que su predicción cae fuera del IC de R; "no refute" = el intento de refutación falla, es decir el corredor sobrevive el intento de falsación de esa celda. Bajo esta lectura, `ADV1-M5` sería en parte una tabla de qué corredor "sobrevive" el intento de falsación, casilla por casilla.
2. **Lectura de robustez del diseño** — "el falsador" = un lector adversarial del propio piloto (rol que las cuatro corridas ADV-1/ADV-2 ya ocuparon); "no refute" = que el diseño del piloto mismo resista una nueva ronda de demolición adversarial, sin que ninguna casilla de `ADV1-M5` le dé munición nueva.
3. **Lectura de `ADV1-M6` (gates de proceso)** — "el falsador" se refiere a los 7 umbrales de `ADV1-M6` (`FP-91`, `ABIERTA` — contradicción de qué criterio GO/NO-GO gobierna, ya registrada); "no refute" = que ninguno de los umbrales activos falle. Esta lectura conectaría el término con una fila ya abierta y sin resolver del tablero (`FP-91`).
4. **Error de transcripción / paráfrasis de mesa** de una idea que sí está en el corpus bajo otras palabras — p. ej. la cláusula de alcance de `ADV1-M5` ("ningún resultado autoriza abandonar L ni M para usos no muestreados") o la condición `INDECIDIBLE` de `ADV1-M3`. Ninguna de las dos usa el verbo "refutar".

**Este acto no elige entre las cuatro.** Pide a mesa: (a) confirmar cuál lectura rige, o (b) declarar que el término no aplica a `ADV1-M5` y retirarlo de la compuerta B-bis para actos futuros.

**RESUELTA, 2026-08-24 — enmienda fechada, texto original intacto arriba.** Mesa firmó `FP-101` el 24/ago/2026 (`ACTO SELLA-AGO24-C-v2`, sello `canon/gobernanza-v1_15.md` `ADR-154`). La resolución **no elige entre las cuatro lecturas candidatas**: declara que el término ya tenía definición operativa en el corpus y que este archivo no la había localizado. **El origen es el Bloque B-bis de `instrucciones-proyecto-v2_11.md`, líneas 111-113** — el mismo bloque cuyo nombre lleva la compuerta que abrió esta pregunta. Cita verbatim de la definición, `instrucciones-proyecto-v2_11.md:113`:

> *«La ficha declara, antes de correr, qué significa que el falsador no refute: si la regla queda corroborada, si queda acotada, o si el falsador era demasiado débil para decir nada. Si el resultado esperado bajo corroboración es interesante —y suele serlo más que la refutación— se dice también, antes de ver el dato.»*

Es decir: **el término no nombra un agente ni un evento, sino un desenlace que la ficha debe pre-declarar, con tres valores — corroborada / acotada / falsador débil.** Eso disuelve las lecturas 1, 2 y 3 (las tres suponían un agente: el refutador, el lector adversarial, los umbrales de `ADV1-M6`) y confirma la 4 en su forma más benigna: no era error de transcripción, era una cita del corpus normativo (`instrucciones`) que la búsqueda original de este archivo no alcanzó porque se restringió al corpus **forense** (`CAREO-ADV-DUELO-diseno-v2`, `TRANSFER-MAESTRA-FASE-CALCULO`, `forense/adv-duelo/`) — verificado leyendo el propio párrafo de «Origen del término» de arriba, que enumera esos cuatro sitios y ninguno de `instrucciones`. `forense/escala-cinco-casillas-piloto-v2_0.md:82` ya citaba este mismo bloque B-bis (contra `instrucciones-proyecto-v2_10.md:113`) sin conectarlo con esta pregunta.

**Lo que esta enmienda NO hace, declarado:** no edita `forense/escala-cinco-casillas-piloto-v1_0.md` —el sitio donde la `COMPUERTA B-bis` de `DUELO-PREREG-V2` está materialmente activada (`:13`, `:25`)— ni `forense/escala-cinco-casillas-piloto-v2_0.md:82`. Los dos archivos viven **fuera** de `forense/prereg-duelo-v2/` y por tanto fuera del perímetro que el encargo de este acto declaró; el encargo suponía que la compuerta vivía dentro de ese directorio y no vive ahí. `PARO` conforme a la cláusula del propio encargo, discrepancia declarada en `ADR-154` y en `forense/notas/2026-08-24-sella-c-v2.md`, no improvisada. La compuerta sigue activada hasta que un acto con el perímetro correcto la cierre.

---

## §2 · Precedencia entre las cinco casillas de `ADV1-M5`

El párrafo `ADV1-M5` de la careo (copiado verbatim en `forense/escala-cinco-casillas-piloto-v1_0.md`) enumera cinco casillas (1)-(5) sin declarar orden de prelación. Los ejes que miden no son mutuamente excluyentes por construcción:

- (1)/(2) comparan **L contra M** (quién quedó más cerca del dato).
- (3) compara **L contra M** con una banda de indiferencia (TOST).
- (4) compara **L y M contra B** (baseline).
- (5) compara **L y M contra R** (el árbitro mismo), no entre sí.

Una misma celda, o el conjunto del piloto, puede satisfacer simultáneamente, por ejemplo, (3) y (5): L y M pueden estar en empate-TOST el uno con el otro (dentro de la banda de indiferencia mutua) y al mismo tiempo ambos fuera del IC de R (lejos del dato real). El texto no dice si en ese caso la lectura publicable del piloto es "(3) empate" o "(5) fenómeno no predecible con estas herramientas", ni si ambas casillas se reportan a la vez sin jerarquía.

**Opciones abiertas, ninguna elegida por este acto:**

- **Opción A — sin jerarquía, reporte conjunto.** Cada celda se etiqueta con TODAS las casillas que satisface; el resumen del piloto es un conteo por casilla, no una asignación exclusiva. Consistente con que `ADV1-M4` ya pide "conteo de INDECIDIBLES y SKIPS publicado al mismo tamaño que el marcador" — sugiere que el diseño tolera categorías no excluyentes.
- **Opción B — precedencia por severidad decreciente:** (5) > (4) > (3) > {(1),(2)}. Razonamiento posible: (5) y (4) son las casillas que el careo marca en negrita como las de mayor consecuencia ("ninguno utilizable v1", "el fenómeno no es predecible"), así que si aplican deberían dominar la lectura sobre una comparación L-vs-M que en ese contexto sería secundaria.
- **Opción C — precedencia por orden de evaluación del script de scoring:** primero se evalúa (4) contra B (si nadie supera a B, ahí termina la lectura de esa celda); solo si alguien supera a B se evalúa (3) INDECIDIBLE (`ADV1-M3`) y luego (1)/(2); (5) se calcula siempre en paralelo como diagnóstico independiente, nunca sustituyendo a las otras cuatro. Esta opción es la que mejor encaja con cómo `ADV1-M3`/`ADV1-M4` de la careo están redactadas (skill se define relativo a B primero), pero el texto de `ADV1-M5` no lo dice explícitamente para las cinco casillas como conjunto.

**Este acto no elige entre las tres.** El script de scoring (`forense/prereg-duelo-v2/scoring-adv1-m3.py`) implementa las funciones necesarias para calcular las cinco condiciones de forma independiente y las deja sin componer en una única etiqueta por celda — la composición/precedencia se deja como parámetro configurable pendiente de que mesa elija A, B, C, u otra.

**RESUELTA, 2026-08-21.** Mesa adoptó la **Opción C** (precedencia por orden de evaluación) vía la firma verbatim «Vamos con 1» sobre el benchmark de `forense/adv-duelo/ADV1-M5-v2-propuesta-2026-08-20.md`. Sello: `canon/gobernanza-v1_15.md` ADR-136, formalizado en el tablero como `FP-102` (`ADR-137(a)`). Detalle de la secuencia adoptada: `forense/escala-cinco-casillas-piloto-v2_0.md` §4.

---

## §3 · Definición mecánica de `⊕` (combinación L⊕M del corredor E)

El careo nombra el corredor E como "combinación mecánica L⊕M pre-registrada, por script" (`§B`, línea de corredores; también `§A` "Ensemble E = L⊕M como corredor", 3/5 corridas adversariales lo incorporan) pero **no define el operador `⊕`** en ningún punto del corpus — verificado por comando (`grep -rn "⊕" forense/ canon/`: sólo las tres menciones nominales, ninguna con fórmula).

**Este acto propone, sin sellar, la combinación mecánica más simple posible** (documentada como propuesta en `forense/prereg-duelo-v2/corredor-E-combinacion-LM.py`): promedio simple por celda para variables continuas (media aritmética de la mediana pre-registrada de L y del punto de M) y voto por mayoría con desempate por confianza declarada para variables categóricas/ordinales. Se documenta explícitamente en el script que esto es una propuesta, no una definición sellada de `⊕`; mesa puede sustituirla por ponderación por skill histórico, por inversa de varianza, u otra regla, antes de que el script se ejecute (este acto no lo ejecuta).

**RESUELTA, 2026-08-21.** Mesa selló la definición de `⊕`, firma verbatim «D-a» (`ACTO SELLA-OPLUS`, nube, Opus, gate `#3`/`ADR-140` fusionado). Sello: `canon/gobernanza-v1_15.md` `ADR-141`, formalizado en el tablero como `FP-99` (`ABIERTA`→`FIRMADA`). Definición sellada: `E = mediana_por_cuantil({L-solo, L+corpus, M})` — tres corredores, no dos (`L-solo` y `L+corpus`, las dos variantes de `L` de `ADV1-M2`, más `M`), peso igual, sin entrenar, mediana en vez de media. Las tres razones (forecast combination puzzle, robustez de la mediana frente a la media, y la mediana solo está bien definida con tres o más componentes) quedan citadas en la cabecera de `forense/prereg-duelo-v2/corredor-E-combinacion-LM.py`, que implementa la definición sellada y sustituye la PROPUESTA de dos corredores de este párrafo. Sin entrenar por falta de historial de desempeño (este es el primer piloto) — razón escrita, no preferencia. El script sigue sin ejecutarse en este acto.

---

## Cómo cerrar este archivo

Cuando mesa resuelva cualquiera de §1, §2 o §3, la resolución se agrega aquí como una nueva sección fechada con la cita de la firma/ADR que la sella, y el archivo correspondiente (`escala-cinco-casillas-piloto-v1_0.md` para §1/§2, `corredor-E-combinacion-LM.py` para §3) se actualiza para reflejar el sello. Ninguna sección de este archivo se borra al resolverse — se marca RESUELTA con su fecha, seg el patrón de `firmas-pendientes.tsv`.
