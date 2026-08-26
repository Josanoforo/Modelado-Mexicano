# DERIVACIÓN DE MECÁNICA M — paso 2 del ENCARGO E7, del árbol y no de memoria

**ACTO E7 · R-SCORING**, 26/ago/2026. Se commitea junto al `COMMIT-1` porque **no toca un solo valor de microdato**: es un censo del procedimiento, no una corrida.

## Qué pedía el encargo

> «los puntos M por celda los produce el emisor del motor (`milpa/src/emisor.py` + crosswalk pregunta↔regla sellado) sobre la SpecCelda de cada una de las 15. Localiza en el árbol el procedimiento sellado que mapea SpecCelda → punto M […] Si no existe procedimiento sellado para alguna celda, eso es PARO-reporte con la lista exacta de celdas huérfanas — es el tipo de hueco que el piloto existe para exhibir; **no inventes un mapeo**.»

## Qué hay en el árbol

El procedimiento sellado **existe** y **cubre las 15**: `forense/crosswalk-pregunta-regla-v1_0.tsv`, 60 filas —el mismo universo que el marco congelado—, producido por `milpa/src/emisor.py:construir_crosswalk`. **Cero celdas del piloto están ausentes de él.** Ese no es el hueco.

El hueco es **qué produce**. Su salida para las 15:

| `emisibilidad_p1` | celdas | cuáles |
|---|---:|---|
| `NO-EMITE` | **12** | CIV-08, DIN-05, DIN-07, DOC-06, EMP-02, EMP-04, EMP-05, SFT-04, SFT-06, TIC-01, TIC-08, TIC-12 |
| `CANDIDATO-EMITE` | **3** | DIN-03, DIN-11, TIC-06 |

(En las 60 del marco completo: 50 `NO-EMITE`, 10 `CANDIDATO-EMITE`.)

## Los 3 `CANDIDATO-EMITE` son falsos positivos de subcadena — los tres

`construir_crosswalk` decide con un `if var and var in l`: **match de subcadena, línea por línea, sin comparar la columna `encuesta`**. Abiertos los hits, ninguno de los tres es la variable de la celda:

- **DIN-03 · ENIF 2012 · `P7_1`** → los hits son `AP7_1` de **ENCUCI** (`milpa/procedencia.yaml:468`, cuya propia línea 470 dice «no es la AP7_1 de ENVIPE de este acto») y `P7_12_7` de **ENASIC 2022** (`:504`, `:527`). Ninguno es `P7_1` de ENIF 2012.
- **DIN-11 · ENIF 2018 · `P5_3`** → los hits son `AP5_3_XX` de **ENVIPE 2025** (`:231`) y `AP5_3_6/7/8` de **ENCUCI 2020** (`:254`). Ninguno es `P5_3` de ENIF 2018.
- **TIC-06 · ENTI 2022 · `P2`** → los hits son la cadena `(P2 §2.d)` en `:298` y `:317` — **una referencia a un documento**, no un nombre de variable.

Los tres cruzan encuesta. Es el modo de fallo que el propio docstring anticipa al llamar al vocabulario «conservador».

## Y aun si no lo fueran, `CANDIDATO-EMITE` no es un punto M

Docstring de `construir_crosswalk`, verbatim: «`CANDIDATO-EMITE` (con archivo:línea) **exige aún enlace de escala/universo declarado antes de emitir**». Es decir: el crosswalk es la **pasada 1**, y la pasada que convertiría un candidato en punto —el enlace de escala/universo, más el par `(regla, conducta)` que `emisor.emitir_binaria(regla, conducta)` exige como argumentos— **no está sellada en ninguna parte del árbol**. Nada mapea `SpecCelda → (regla, conducta)`.

## Veredicto del paso 2

**Cero de quince celdas tienen punto `M` derivable de un procedimiento sellado.** Se reporta así, con dos matices que cambian qué clase de hueco es cada uno:

- **12 celdas — `NO-EMITE`.** No son huérfanas: el procedimiento **sí las cubre** y su respuesta es «el motor no emite aquí». `emisor.py` declara `NO_COVERAGE` como «salida de primera clase, nunca silencio». M simplemente no compite en estas celdas.
- **3 celdas — `CANDIDATO-EMITE` que no resiste inspección** (DIN-03, DIN-11, TIC-06). Estas **sí son huérfanas** en el sentido estricto del encargo: el procedimiento no llega a punto, y el paso que faltaría no está sellado. **Ésta es la lista exacta de celdas huérfanas que el encargo pedía.**

**No se inventa un mapeo para ninguna**, ni se «corrige» el crosswalk: es artefacto sellado y este acto no lo toca. Los falsos positivos se **reportan**, no se reparan.

## Consecuencia aguas abajo

1. **La columna `M` del marcador va vacía en las 15**, con su razón por celda.
2. **El scope adjudicante de `scoring-adv1-m3.py` es `{L seleccionado, M}`** (docstring, verbatim). Sin `M`, `PASO 1`/`PASO 2` **no tienen scope** y no pueden adjudicar. Eso **no rompe el acto**: `D-i` ya manda `PILOTO SIN VEREDICTO`, y lo que el marcador debía hacer era puntuar, no adjudicar. Se corre lo que sí tiene universo —los marginales contra `R`— y se dice dónde se detiene.
3. Sumado a `FP-165` (que dejó `E` inejecutable por falta de `L+corpus`), el piloto queda con **dos** de los cuatro corredores fuera: `M` sin punto y `E` sin definición. Compiten `L-solo` y `B`.

Este hallazgo abre una fila de firma pendiente para mesa. Este acto **no la decide**.
