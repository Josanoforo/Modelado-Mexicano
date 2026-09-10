# Regla de extracción de `valor_extraido` — formato v1.3 (`tools/extrae_l_v1_3.py`)

**Acto:** `GEN2-F5-EXTRACTOR-L-v1` (nube, Opus). Sucesor de
`regla-extraccion-L-v1_1.md` / `tools/extrae_l_v1_1.py` — ninguno de los dos
se edita. Este documento y `tools/extrae_l_v1_3.py` son P1 (COMMIT-1): la
regla se congela aquí, contra las formas de salida ya observadas en las 224
capturas reales de `corridas-L/*__v1_3.json`, **antes** de aplicarse al
universo completo (P2, COMMIT-2). No se edita después de ver el resultado
sobre las 224.

## 0 · Por qué existe

`ACTO GEN2-F5-DUELO-CALC` (`PR #674`) midió que `tools/extrae_l_v1_1.py`
—calibrado contra un encabezado Markdown fijo (`## Estimación`) que las
capturas v1.1/v1.2 sí traían— no encuentra ese encabezado en las 96 capturas
reales de las 6 celdas con árbitro del marco v1.3 (0/96) y cae a su
*fallback* declarado: "primer número del documento completo". Verificado a
mano contra tres ejemplos con hash (citados en
`forense/notas/2026-09-10-GEN2-F5-DUELO-CALC-veredicto.md` §1 y reproducidos
como controles negativos en `tests_extrae_l_v1_3.py`), ese fallback captura
una "cifra negra" de contexto (∼90–94 %, ENVIPE, citada por el modelo como
conocimiento general) que el propio texto declara explícitamente que **no**
es la estimación pedida. `NC-0142` quedó abierta por esta razón instrumental,
no por ausencia de capturas (224/224 existen, embudo limpio).

## 1 · Lo que esta regla NO hace, por diseño

- **No** usa "primer número del documento" en ningún punto, ni como regla
  principal ni como fallback.
- **No** trata un intervalo, un año, un tamaño de muestra, una "cifra negra"
  u otra estadística de contexto como candidato a `valor_extraido` solo por
  aparecer en el texto — una cifra sólo es candidata si aparece **dentro**
  de una de las dos anclas estructurales/textuales de la §2.
- **No** decide entre dos candidatos que sobreviven sin una regla de
  desempate explícita y congelada aquí mismo (§2, desempate intra-ventana
  "mi punto" > rango). Si no hay regla de desempate aplicable, el resultado
  es `AMBIGUA`, nunca una elección post-hoc.
- **No** depende del valor de `R`, de `M`, ni del error resultante: opera
  exclusivamente sobre `texto_crudo` y la identidad declarada de cada
  captura. El extractor puede correr sin abrir `CALC-R-*/`, `corridas-R/`,
  ni ningún `CALC-DUELO-*/` (control de independencia, verificado por
  `tests_extrae_l_v1_3.py::TestUniversoReal224::
  test_extractor_no_referencia_R_ni_duelo`).

## 2 · La regla, en dos familias de ancla

Ver el docstring de `tools/extrae_l_v1_3.py` (única fuente de verdad
ejecutable; este documento es la prosa de acompañamiento, no una segunda
copia que pueda desincronizarse). Resumen:

- **Familia H (encabezado).** Un encabezado Markdown (`#+`) cuyo título
  contiene "estimaci". Dentro de su sección, párrafo por párrafo, se
  excluyen los párrafos de banda/incertidumbre ("rango subjetivo",
  "intervalo de confianza", etc.) y se busca un número (`≈N%`, rango, `N%`,
  o decimal en `[0,1]`) en los párrafos restantes.
- **Familia F (frase-ancla).** Las frases fijas "estimación puntual", "mi
  punto", "punto central", dondequiera que aparezcan (encabezado, tabla,
  prosa). Se examina una ventana corta después de la frase: rechazo
  explícito, número, o ninguno de los dos (ancla no informativa, se
  descarta).

Todas las anclas informativas (de ambas familias, todas las ocurrencias) se
combinan: si todas coinciden en "rechazo" → `NO-EXTRAIBLE`; si todas
coinciden en el mismo número → `EXTRAIBLE`; cualquier mezcla o desacuerdo →
`AMBIGUA`; ninguna ancla informativa en absoluto → `NO-EXTRAIBLE` con razón
`SIN-ANCLA` (nunca un fallback posicional).

## 3 · Identidad (fallo material, no extracción)

Antes de intentar extraer, se verifica que el nombre de archivo, el
`id_celda`/`variante`/`indice` **dentro** del JSON, y la entrada
correspondiente del manifiesto sellado de `F5-RECAPTURA-L`
(`manifiesto-capturas-P3-v1_0.json`, incluido su `sha256_archivo`)
coincidan entre sí. Cualquier discrepancia es `estado = ERROR-IDENTIDAD`,
un cuarto estado distinto de `{EXTRAIBLE, NO-EXTRAIBLE, AMBIGUA}` — no se
intenta extracción sobre una captura cuya identidad no se pudo confirmar.

## 4 · Controles congelados (`tests_extrae_l_v1_3.py`)

- **Negativos obligatorios (los tres de `NC-0142`):** `CIV-M-12__L-solo__01`,
  `CIV-M-13__L+corpus__04`, `CIV-M-01__L+corpus__02` — los tres deben volver
  `NO-EXTRAIBLE` vía `ANCLA-RECHAZO`, nunca la cifra de contexto (0.90–0.94)
  que el viejo extractor capturaba.
- **Positivos** (formas reales con punto comprometido): encabezado `##
  Estimación` con `≈N%` (`FAM-M-05__L+corpus__02`, sin confundir el "rango
  subjetivo" del mismo bloque); frase-ancla con "mi punto" desempatando un
  rango en la misma ventana (`TRA-M-03__L-solo__03`); tabla `| Estimación
  puntual | **Abstención** |` como rechazo (`CIV-M-12__L-solo__07`).
- **Sintéticos:** ausencia total de ancla (`SIN-ANCLA`, no cae al primer
  número); dos anclas numéricas distintas (`AMBIGUA`); número y rechazo
  mezclados (`AMBIGUA`); rango sin punto declarado (punto medio, regla de
  normalización).
- **Identidad:** captura real con identidad íntegra; JSON alterado
  (`id_celda` cruzado) → `ERROR-IDENTIDAD`; archivo ausente del manifiesto →
  `ERROR-IDENTIDAD`.
- **Universo real:** las 224 rutas `corridas-L/*__v1_3.json` existen y
  `procesar_224` corre sobre ellas sin ninguna `ERROR-IDENTIDAD` (embudo de
  captura ya limpio, citado del manifiesto de `F5-RECAPTURA-L` — no se
  espera ninguna aquí).

## 5 · Qué produce P2 (no forma parte de esta congelación)

`L-extraido-v1_3.tsv` (una fila por captura: `id_celda · variante · replica
· estado · valor_extraido · evidencia_textual · regla_de_extraccion ·
razon_no_extraible · archivo`) y `manifiesto-extraccion-L-v1_3.json` (hash
del extractor, hash del manifiesto de capturas insumo, resumen de cobertura
y regla por archivo) — ambos productos de correr `tools/extrae_l_v1_3.py`
sin argumentos sobre las 224 capturas, en el commit P2 de este mismo acto.
Este documento no adjudica quién gana la pareada primaria del duelo: eso
sigue perteneciendo al `ENCARGO 5/5` (sucesor `GEN2-F5-TRIADA-CALC`).
