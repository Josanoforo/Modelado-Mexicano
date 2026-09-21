# CALC-L-DESDE-CAPTURAS-v1_0 · spec humana

**Acto:** `GEN2-L-DESDE-CAPTURAS-1`, 21/sep/2026. **Encargo:**
`forense/encargos/2026-09-21-GEN2-L-DESDE-CAPTURAS-1.md`.

## 1 · Qué mide

Por cada una de las 14 celdas del duelo (`L-spec-v1_4.json`) y sus dos
variantes (`L-solo`, `L+corpus`) — 28 slots — la lectura L del LLM: mediana
de réplicas válidas, dispersión entre repeticiones (MAD: mediana de las
desviaciones absolutas a la mediana) e intervalo bootstrap (percentil
2.5–97.5, 10 000 réplicas, semilla 42) de esa mediana.

## 2 · Universo y fuente

Las 224 capturas de `forense/prereg-duelo-v2/corridas-L-completa-v1_0/`
(14 celdas × 2 brazos × 8 réplicas), congeladas por
`F5-completa-spec-v1_0.md` (commit `7d97681`, 10/sep/2026) — **es el
conjunto vigente**: esa spec declara que las 224 sustituyen a la corrida
v1.3 porque ésta no registró `modelo_real` (§1 de esa spec). Verificado en
este acto: 224/224 archivos presentes (`git ls-files` sobre el directorio),
`identidad` de cada captura casa con `F5-completa-plan-v1_0.json` (0
errores de identidad).

## 3 · Regla de inválidas (no se decide aquí — se hereda, sellada antes)

La regla de qué cuenta como `VALIDA`/`ABSTENCION`/`MALFORMADA`/
`ERROR_TECNICO` es la de `F5-completa-spec-v1_0.md` §4, sellada el
10/sep/2026 — **antes** de este acto y antes de las 224 capturas. Este CALC
no la re-decide (PARO (d) del encargo): sólo lee la última línea no vacía
de `texto_crudo`; `ESTIMACION_PUNTUAL=N%` con `0<=N<=100` es válida;
`ABSTENCION` es abstención; cualquier otra terminación es malformada; un
fallo técnico agotado es error técnico. El código vive en
`tools/calcula_f5_completa.py::extraer` — este CALC lo importa, no lo
copia.

## 4 · Agregador

Mediana de réplicas válidas por celda/variante — la misma spec §4:
«El punto L de una celda/brazo es la mediana de réplicas válidas; si no hay
ninguna, queda ausente.» El módulo reusable (P5) es
`tools/agrega_l_v1_0.py::agregar_celda`, con su test
`tools/test_agrega_l_v1_0.py`.

## 5 · Ramas terminales (D-22 ampliada)

- **Oro sobre sintético:** ocho réplicas con respuesta conocida a mano
  (caso `TRA-M-02:L-solo` del análisis de los 9 L, P6) → mediana esperada
  reproducida exacto.
- **Celda con todas las réplicas inválidas:** mediana/dispersión/IC en
  `None`, conteos intactos.
- **Celda con una sola réplica válida:** mediana = ese valor, dispersión =
  0.0, IC degenerado (`ic_lo == ic_hi == mediana`) — declarado, no omitido.

Las tres se prueban en `tools/test_agrega_l_v1_0.py`, corrido antes de este
COMMIT-1 (código y medidor se congelan juntos, E.5).

## 6 · Diferencias contra GEN1 (P4), descompuestas

Por celda/variante, cuando reconstruible: GEN1 (media, sobre su propio
conjunto v1.2 de `L-extraido-v1_2.tsv`, estado `EXTRAIBLE`) → mediana sobre
ESE MISMO conjunto v1.2 (`delta_agregador_pp` = efecto de cambiar media→
mediana, mismas réplicas) → mediana sobre las 224 capturas completas
(`delta_conjunto_pp` = efecto de cambiar de conjunto de extracción,
mismo agregador). Cuando el conjunto v1.2 no trae ninguna fila `EXTRAIBLE`
para esa celda/variante, ambos deltas quedan `NO-RECONSTRUIBLE` — no se
estima.

**Hallazgo derivado (no tecleado, verificado en este acto):** en el
conjunto vigente (224 completas), `TRA-M-02:L-solo` da mediana `0.15`,
igual a la mediana sobre las réplicas v1.2 (`delta_conjunto_pp ≈ 0`) —
distinto del `0.14` que reportó `CALC-TRIADA-0001`. Esa diferencia viene de
que `CALC-TRIADA-0001` agregó sobre `corridas-L/` (731 archivos, extractor
v1.3, el conjunto viejo), no sobre `corridas-L-completa-v1_0/` (224, el
conjunto que la spec sellada declara vigente). Este CALC usa el vigente;
`CALC-TRIADA-0001` no se toca (no es de este acto, y su RESULT no se
adopta ni se mueve — el encargo lo prohíbe explícitamente).

## 7 · No hace

No pinea ninguna lectura. No corre LLM ni genera capturas. No juzga si el
LLM «sabe» de México — mide qué dijo (auditoría §10 del encargo). No toca
`CALC-TRIADA-0001` ni `CALC-TRIADA-0002`, ni sus RESULT.

## 8 · Tolerancia y determinismo

Todo `RESULT-*-PP` de dispersión/IC es de punto flotante; tolerancia
`1e-6` (mismo orden que `calcula_f5_completa.py`). El bootstrap es
determinista por semilla fija (42) — dos corridas del mismo CALC producen
el mismo IC exacto (probado en `test_agrega_l_v1_0.py
::test_determinismo_misma_semilla`).
