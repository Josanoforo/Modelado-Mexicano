# `ACTO GEN2-F5-DUELO-CALC` — el veredicto

**La pareada primaria (TRANSFERENCIA, `L_SOLO` vs `L_CORPUS` contra `R`, 6/6
celdas con árbitro) queda `INCONCLUSO` — pero no por la banda estadística
(que también sale `INCONCLUSO`, fila «cualquier otro traslape» de la escala
B-bis sellada: `dif_abs_pareada` punto `+6.19`, IC95 `[-16.37, +32.49]`, un
intervalo que cruza los dos límites de la banda `δ=0.5`), sino porque el
único extractor de `valor_extraido` disponible para prosa libre de
`corridas-L/` no está validado contra el formato real de estas capturas y,
verificado a mano, produce números que el propio modelo dice explícitamente
que no son la estimación pedida.** El marcador sigue `INCONCLUSO` (`#651`),
ahora con una segunda razón declarada y no resuelta: no hay instrumento de
extracción confiable con el que re-intentar la pregunta hoy.

**Fecha:** 10/sep/2026 · **Entorno:** NUBE, cero microdato/cero red ·
**Base:** `origin/main = 9dbe570` (`PR #669` fusionado; re-verificado tras
`PR #673`) · **Encargo:** `forense/encargos/2026-09-10-GEN2-F5-DUELO-CALC.md`
(A.3, verbatim) · **Corrida:** `data/corrida0/CALC-DUELO-0001/` —
`preflight VERDE` → `run exit=0` → `SELLADO`
(`sha256=c1de72df948a6d8dd462493e4cdfe4b9ffc98c4fb9053adbd210a1680b8f646d`).

---

## 1 · La pareada primaria — TRANSFERENCIA

Escala B-bis sellada por `forense/prereg-duelo-v2/F5-duelo-contemporaneo-spec-v1_0.md`
§5 (`COMMIT-1` de `ACTO GEN2-F5-RECAPTURA-L`), aplicada al pie de la letra
por `CALC-DUELO-0001`:

| Condición sobre `[ic_lo, ic_hi]` | Veredicto de la escala |
|---|---|
| `ic_hi < −0.5` | GANA `L_CORPUS` |
| `ic_lo > 0.5` | PIERDE `L_CORPUS` |
| `−0.5 ≤ ic_lo` y `ic_hi ≤ 0.5` | EMPATE |
| **cualquier otro traslape** (nuestro caso: `ic_lo=-16.37 < -0.5` **y** `ic_hi=32.49 > 0.5`) | **INCONCLUSO** |

`RESULT-DUELO-PAREADA-VEREDICTO-BANDA-BRUTO = INCONCLUSO` — el número que el
procedimiento sellado produce, calculado en su totalidad, "el primer
resultado que produzca este procedimiento" (P1, citado verbatim).

**`RESULT-DUELO-PAREADA-VEREDICTO-ADOPTADO = INCONCLUSO`, por una razón
DISTINTA y más grave:** `INSTRUMENTO-DE-EXTRACCION-NO-VALIDADO-PARA-
FORMATO-REAL-DE-CORPUS`. Medido, no supuesto (§2): de las 96 capturas reales
de las 6 celdas con árbitro (`CIV-M-01/02/04/10/12/13` × `L-solo`/`L+corpus`
× 8 réplicas), **0/96 traen el encabezado Markdown con "estimaci"** que
`tools/extrae_l_v1_1.py` (el único extractor sellado, calibrado contra el
formato de captura v1.1/v1.2) busca antes de aceptar un número. El 100% cae
a su *fallback* de "primer número en todo el documento", y 59/96 (61%)
quedan `EXTRAIBLE` por esa vía. Verificado a mano contra tres de esas 59
(citadas con su sha256 en `RESULT-DUELO-DIAGNOSTICO-EJEMPLO-*`):

- `CIV-M-12__L-solo__01` (`sha256 4673f1c2…`): el modelo cierra con
  **"Estimación puntual: no proporcionada (dato desconocido)."** — rechazo
  explícito — pero el extractor captura `92–93%`, una cifra de "cifra
  negra" de la ENVIPE citada como *"conocimiento general del programa"*, no
  como respuesta. Valor indebidamente capturado: `0.925`.
- `CIV-M-13__L+corpus__04` (`sha256 5cec84f4…`): el modelo dice
  *"eso es contexto, no una estimación de este reactivo, y no debe usarse
  como tal"* — y aun así el extractor toma `92–94%` de esa misma frase.
  Valor indebidamente capturado: `0.93`.
- Un tercer caso (`CIV-M-01__L+corpus__02`, no citado en `RESULT-*` por el
  criterio automático de la corrida, revisado manualmente en esta sesión):
  *"eso es un contexto de encuadre, **no** una estimación puntual del
  reactivo solicitado, y no debe registrarse como tal"* — el extractor
  toma `90%` igual.

**Este acto no inventa un extractor nuevo para corregirlo.** Sería
exactamente la clase de regla improvisada después de ver resultados que el
propio encargo prohíbe en espíritu ("prohibido... elegir entre variantes de
agregación después de ver resultados — lo no fijado en P1 no existe"). Se
declara el hueco (`NC-0142`, abajo) y se deja como trabajo de un sucesor con
instrumento validado — no se adjudica sobre un número que ya se demostró
contaminado.

### Tabla por celda

| Celda | Ola | Docs. incl./excl. | `R` | `EE(R)` | `L-solo` (mediana, n extraíble/8) | `L+corpus` (mediana, n/8) | `z_LSOLO` | `z_LCORPUS` | `dif_abs_pareada` |
|---|---|---|---:|---:|---|---|---:|---:|---:|
| CIV-M-01 | ENVIPE 2012 | 31/6 | 0.2590 | 0.00697 | 0.7725 (4/8) | 0.900 (5/8) | 73.67 | 91.96 | +18.29 |
| CIV-M-02 | ENVIPE 2013 | 31/6 | 0.2434 | 0.00624 | 0.920 (5/8) | 0.900 (6/8) | 108.47 | 105.26 | −3.21 |
| CIV-M-04 | ENVIPE 2015 | 31/6 | 0.2437 | 0.00748 | 0.925 (3/8) | 0.6285 (6/8) | 91.04 | 51.42 | −39.62 |
| CIV-M-10 | ENVIPE 2021 | 31/6 | 0.2049 | 0.00477 | 0.620 (1/8) | 0.935 (7/8) | 86.95 | 152.94 | +65.99 |
| CIV-M-12 | ENVIPE 2023 | 31/6 | 0.2081 | 0.00476 | 0.925 (7/8) | 0.900 (5/8) | 150.60 | 145.35 | −5.25 |
| CIV-M-13 | ENVIPE 2024 | 31/6 | 0.1946 | 0.00539 | 0.925 (3/8) | 0.930 (7/8) | 135.47 | 136.40 | +0.93 |

Los `z` de magnitud 50–150 no son un artefacto de cómputo: son la
consecuencia directa de la contaminación de arriba — un `agregado(brazo)`
de `~0.9` construido sobre "cifras negras" de contexto contra un `R` real
de `~0.2–0.26` produce exactamente esa distancia. Ninguna celda tiene un
`agregado(brazo)` plausible como estimación genuina del reactivo, así que
ninguna fila de esta tabla se lee como evidencia de transferencia — se
publica por transparencia mecánica (P1), no porque se confíe en ella.

`z_M` (contexto, sin poder de veto, no gatante): `CIV-M-01=5.07`,
`CIV-M-02=8.16`, `CIV-M-04=6.77`, `CIV-M-10=18.72`, `CIV-M-12=18.11`,
`CIV-M-13=18.49` — el corredor de reglas `M` (`0.294313` para las seis,
tasa base ENVIPE 2025) también está lejos de `R`, pero a una distancia mucho
menor y más estable que `L`, sin el mismo patrón de contaminación (M no
pasa por el extractor de prosa libre).

## 2 · Secundaria (b) — USO DOCUMENTAL, acotada al panel de 6 celdas y al paquete-corpus F5

`RESULT-DUELO-SECUNDARIA-USO-DOCUMENTAL-*`: de las 48 capturas `L+corpus`
del panel (6 celdas × 8), el campo estructurado `fuente_citada` está
**`null` en el 100% (0/48)** — el runner nunca lo puebla por parseo
mecánico; no es evidencia de ausencia de uso documental, es un campo que no
se llena.

**Lectura cualitativa (no mecanizada, acotada a lo que esta sesión leyó a
mano de las mismas capturas citadas en §1):** el modelo, en las capturas
`L+corpus` inspeccionadas, describe con precisión qué encuestas/temas SÍ y
NO contiene el paquete-corpus entregado (p. ej. *"el corpus tierizado que se
me entregó… no contiene ningún documento de la ENVIPE… los reports
disponibles citan ENSU, ENDIREH, ENIF, ENOE, ENSANUT, ENCODAT, ENCUCI,
Latinobarómetro y CONEVAL"*) — un engagement real y correcto con el
contenido entregado, incluso cuando correctamente se abstiene de fabricar
una cifra. Esto es evidencia de que el corte temporal/paquete llegó
legible al modelo; **no** es evidencia de que el corpus permita estimar el
reactivo — las dos cosas son distintas y esta nota no las mezcla.
`RESULT-DUELO-SECUNDARIA-PP-VEREDICTO = NO-COMPUTABLE-MISMO-INSTRUMENTO-
QUE-LA-PRIMARIA`: la métrica secundaria en puntos porcentuales (D4) hereda
exactamente la misma contaminación de extracción que la primaria, así que
no se reporta como si fuera un dato independiente.

## 3 · Cobertura, citada del embudo ya sellado de `RECAPTURA-L`

`RESULT-DUELO-COBERTURA-*`, sobre las 14 celdas completas del marco (no
recalculado, citado de `manifiesto-capturas-P3-v1_0.json`): **224/224 OK, 0
rechazadas, 0 reintentos**. La cobertura NO es el problema de este acto — el
embudo de captura está limpio; el problema es exclusivamente el instrumento
de extracción de texto a número.

## 4 · Límites que mordieron

- **Instrumento de extracción no validado** (§1) — el límite que produjo el
  `INCONCLUSO` adoptado.
- **Réplicas.** La dispersión entre las 8 réplicas por (celda, variante) no
  se propaga al IC de la pareada (bootstrapea sobre celdas, no sobre
  réplicas) — límite heredado de la spec sellada §6, no nuevo de este acto.
- **Error de `R` condicional.** `EE(R)` se trata como fijo — mismo límite
  heredado, no nuevo.
- **Universo pequeño.** 6 celdas es el universo pareado completo posible
  hoy (todas las celdas con árbitro entraron, `n=6/6`) — no hay celdas
  perdidas, pero 6 sigue siendo un universo chico para un IC bootstrap.

## 5 · Frontera — qué NO adjudica este duelo

Este acto **no** adjudica causalidad alguna entre tener o no tener corpus y
la calidad de la estimación (aun si el instrumento fuera válido, la
comparación seguiría siendo `L_SOLO` vs `L_CORPUS` sobre el mismo modelo, no
un experimento causal más amplio). **No** adjudica nada sobre las 8 celdas
del marco sin árbitro `R` (`DIN-M-01`, `FAM-M-01/05/06/07`,
`TRA-M-02/03/07`) — quedan fuera del universo pareado por construcción, sin
opinión de este acto sobre ellas. **No** generaliza fuera del marco de 14
celdas ni fuera de la ventana de captura (`RECAPTURA-L`, sep/2026). **No**
reabre ni re-adjudica el marcador histórico (`#651`) ni sus `NC` — el
`#651` sigue exactamente como estaba, con una segunda razón de por qué
sigue abierto.

## 6 · Contraste descriptivo contra el marcador histórico (script, no re-adjudicación)

`agregado-v1_3-resultado.json` (acto `MAESTRA38-M13`, previo a este,
comparación `L_SOLO_vs_M`/`L_CORPUS_vs_M` sobre las 14 celdas con la spec
`procedimiento-scoring-v1_2.md`) usa una fuente de `L` distinta
(`L-extraido-v1_2.tsv`, extraída ANTES de que existieran las 224 capturas
reales de `RECAPTURA-L`) — no es la misma pregunta ni la misma captura que
este acto, y no se re-adjudica aquí. Se cita solo para notar que ese
agregado *también* reportó `z` de magnitud alta para `L` (`mediana_abs_z`
punto `11.16`–`29.19` marginal) contra `R`, consistente con que el
`L`/extracción de prosa libre ha sido una fuente de ruido/contaminación
recurrente en este programa, no un defecto aislado de este acto.

## 7 · Contadores del programa, salida cruda, sin esperados (E.4)

`python3 tools/corrida0.py status`, antes (commit `1fec316`, tras el 0-bis,
antes de `CALC-DUELO-0001`) vs. después (commit `0732f93`, este cierre):

- corridas escaneadas: **112 → 113** (`+1`, `CALC-DUELO-0001`)
- resultados escaneados: **2129 → 2230** (`+101`, los `RESULT-DUELO-*` de
  este CALC)
- `N_corridas_selladas`: **17 → 17** (sin cambio — este contador no cuenta
  por directorio `CALC-*` nuevo; crudo, no se investiga más en este acto)
- `no_corrido_abiertas`: **80 → 80 aquí; → 81 al registrar `NC-0142`** en la
  cascada de este mismo cierre (append, no en este comando)
- `corredores_envueltos_legacy`: **11 → 12** (crudo; no se atribuye causa
  sin verificarla — no es un contador que este acto haya tocado a propósito)

**Contador de este acto:** sí — `CALC-DUELO-0001`, con cadena `E.2` completa
(`spec.yaml` congelado en `COMMIT-1`, corrida y sello en `COMMIT-2`,
firma de contador con objeto citada en `spec.yaml:etiquetas.firma_de_
contador`). Lo que NO hace: no enmienda la escala sellada de
`F5-duelo-contemporaneo-spec-v1_0.md`, no re-captura, no adopta ningún
veredicto en ningún consumidor de `milpa/` (no hay consumidor que citar), no
toca el marcador histórico ni sus `NC`.

## 8 · Sucesores

- **La lectura de mesa del veredicto** — con esta nota como único insumo
  necesario: el duelo NO resolvió la tesis de transferencia; mesa decide si
  eso cambia F6/Ola 6/cartera.
- **`NC-0142`** (abajo, en el encargo archivado): construir y sellar un
  extractor de `valor_extraido` calibrado contra el formato real de
  `corridas-L/*__v1_3.json` (prosa sin encabezados de sección, refusals
  ricos en cifras de contexto) antes de re-intentar la pareada primaria.
