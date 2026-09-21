# P6 · Los 9 puntos L «rehechos con diferencia», uno por uno — para firma de mesa

**Acto:** GEN2-RELEVO-TANDA-3 · **Fecha:** 21/sep/2026 · **Base:** `67e157a`
**Encargo:** `forense/encargos/2026-09-21-GEN2-RELEVO-TANDA-3.md`, P6 — «Casa su
estimando por texto (qué agrega GEN1 y qué agrega "mediana de réplicas EXTRAIBLE"
de la spec sellada; por qué difieren hasta 1.1 pp) y entrégalos a mesa uno por uno,
con delta y recomendación.»

**Ninguno de los nueve se pinea en este acto.** P6 lo prohíbe explícitamente y,
además, no pasarían: son `RESULT-TRIADA-*`, y la guarda (d) de 4.1 rechaza todo
RESULT de un CALC que ingiere (`CALC-TRIADA-0001` toma
`forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json` como input).

---

## 1 · El hallazgo: son DOS diferencias, no una

El informe de `GEN2-RELEVO-RECONCILIA-1` (#928 §, «Aparte —
`REHECHO-CON-DIFERENCIA`») lee el delta así: «La diferencia es de procedimiento de
agregación entre GEN1 y el `mediana de réplicas EXTRAIBLE` de la spec sellada.»
**Derivado en esta sesión, eso es la mitad.** Hay dos diferencias independientes, y
la segunda no estaba nombrada.

**(1) El agregador.** `CALC-TRIADA-0001/spec.yaml:transformacion` declara
«Agregacion L por celda: mediana de las replicas EXTRAIBLE
(`pipeline-L-adv1-m2.py::agregar_continua`), **heredada sin cambio**». El legacy
**no** es la mediana: es la **MEDIA**. Medido sobre las réplicas `EXTRAIBLE` de
`forense/prereg-duelo-v2/L-extraido-v1_2.tsv`, el valor de
`agregado-v1_3-resultado.json` reproduce la media **exacta en 9 de 9**. Así que
«heredada sin cambio» no describe lo que GEN1 hizo.

**(2) El conjunto de réplicas.** Si la única diferencia fuera el agregador, el valor
GEN2 tendría que ser la mediana de ESAS MISMAS réplicas. **Coincide en 1 de 9**
(`FAM-M-05:L-solo`). GEN2 re-extrae de las 224 capturas con `tools/extrae_l_v1_3.py`;
GEN1 agrega `L-extraido-v1_2.tsv` (extractor v1.2). El conjunto `EXTRAIBLE` no es el
mismo.

## 2 · La tabla, derivada (no tecleada)

`legacy` = `agregado-v1_3-resultado.json:celdas.<celda>.<L_solo|L_corpus>` ·
`gen2` = `data/corrida0/CALC-TRIADA-0001/resultados.json` ·
`media_v12`/`mediana_v12` = sobre las réplicas `EXTRAIBLE` de `L-extraido-v1_2.tsv`
(n = 8 examinadas y 8 con valor en las nueve).

| slot | celda:variante | legacy | media v1_2 | mediana v1_2 | GEN2 | delta (pp) | legacy = media | GEN2 = mediana v1_2 |
|---|---|---|---|---|---|---|---|---|
| RES-0137 | FAM-M-05:L-solo | 0.046125 | 0.046125 | 0.045 | 0.045 | −0.113 | **sí** | sí |
| RES-0138 | FAM-M-05:L+corpus | 0.045875 | 0.045875 | 0.045 | 0.046 | +0.013 | **sí** | no |
| RES-0142 | FAM-M-06:L-solo | 0.04875 | 0.04875 | 0.0485 | 0.045 | −0.375 | **sí** | no |
| RES-0143 | FAM-M-06:L+corpus | 0.04725 | 0.04725 | 0.048 | 0.05 | +0.275 | **sí** | no |
| RES-0147 | FAM-M-07:L-solo | 0.052875 | 0.052875 | 0.054 | 0.045 | −0.787 | **sí** | no |
| RES-0148 | FAM-M-07:L+corpus | 0.051625 | 0.051625 | 0.051 | 0.05 | −0.163 | **sí** | no |
| RES-0152 | TRA-M-02:L-solo | 0.15125 | 0.15125 | 0.15 | 0.14 | **−1.125** | **sí** | no |
| RES-0157 | TRA-M-03:L-solo | 0.1225 | 0.1225 | 0.1225 | 0.125 | +0.250 | **sí** | no |
| RES-0162 | TRA-M-07:L-solo | 0.14425 | 0.14425 | 0.145 | 0.146 | +0.175 | **sí** | no |

Caso legible a mano, `TRA-M-02:L-solo`: las ocho réplicas `EXTRAIBLE` de v1.2 son
`[0.12, 0.12, 0.15, 0.15, 0.15, 0.15, 0.17, 0.20]` → media `0.15125` (= el legacy,
exacto), mediana `0.15`. GEN2 publica `0.14`, que no es ninguna de las dos: sus
réplicas son otras.

## 3 · Estimando casado por texto, cinco dimensiones — el mismo veredicto para los nueve

| dimensión | GEN1 | GEN2 | ¿casa? |
|---|---|---|---|
| evento | predicción L del corredor sobre la celda, variante `L-solo` / `L+corpus` | la misma | **sí** |
| unidad / escala | proporción en `[0,1]` sobre la celda | proporción en `[0,1]` | **sí** (A-bis.3: no son escalas distintas) |
| ola | no aplica (la celda fija la ola) | igual | **sí** |
| universo (conjunto de réplicas) | réplicas `EXTRAIBLE` de `L-extraido-v1_2.tsv` (extractor v1.2) | re-extracción de las 224 capturas con `extrae_l_v1_3.py` | **NO** |
| denominador / agregador | **media** de las réplicas con valor | **mediana** de las réplicas `EXTRAIBLE` | **NO** |

**Veredicto: el estimando NO está casado en dos de las cinco dimensiones.** Por
A-bis.4, dos cantidades que no comparten universo ni regla de agregación no se
aparean. El rótulo `REHECHO-CON-DIFERENCIA` que hoy llevan sugiere que es la misma
medición con otro número; lo derivado dice que son **dos estimandos distintos que
coinciden de cerca**, que es otra cosa.

## 4 · Recomendación, uno por uno

La recomendación es **la misma para los nueve**, y por eso va una vez y no nueve: lo
que los separa es estructural (agregador y extractor), no de celda. Los deltas
individuales están en la tabla de §2 para que mesa los vea por slot.

1. **No pinear ninguno de los nueve** — ni por vía (i) ni por vía (ii). La guarda (d)
   los rechaza y el estimando no casa. Esto NO es un cambio de contador: los nueve ya
   contaban como legacy y siguen contando.
2. **Re-rotularlos.** `REHECHO-CON-DIFERENCIA` → algo que diga lo medido, p. ej.
   `RE-DERIVADO-CON-ESTIMANDO-DISTINTO`. El rótulo actual es el que hace que parezcan
   candidatos a pin.
3. **Una decisión de mesa, una sola:** ¿qué agregador gobierna L, la **media** que GEN1
   usó de hecho o la **mediana** que la spec sellada declara? La spec sellada no se
   edita (A.10); si gobierna la mediana, GEN1 queda como historia (E.1) y el relevo de
   L exige un CALC propio que mida L desde las capturas con el agregador y el extractor
   declarados — no `CALC-TRIADA-0001`, que ingiere.
4. **Corregir en el registro la lectura de #928** (§1 de esta nota), para que el
   sucesor no herede «es el agregador» como premisa. Va como hallazgo, no como
   reescritura de aquel informe.

## 5 · Los 33 `SIN-REHACER` del marco — demanda de nube, con receta

19 L + 14 AGREGADO, tal como `GEN2-RELEVO-RECONCILIA-1` los dejó:
`forense/analisis/relevo-reconcilia-1/reconcilia-173-v1_0.tsv` lleva la receta y el
entorno de cada uno y no se reescribe aquí. Entran como **demanda de nube**: no
necesitan caja (las capturas y el agregado están en el repo), y lo que les falta no es
acceso sino una corrida que los produzca. Los 14 AGREGADO además están en
`NO-ENCONTRADO` declarado —`CALC-TRIADA-0001` no emite ningún RESULT de agregado—, que
es el hueco, no el dato.
