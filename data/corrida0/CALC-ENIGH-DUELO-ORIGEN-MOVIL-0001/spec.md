# ENIGH-DUELO-ORIGEN-MOVIL · RETROSPECTIVA-MECÁNICA · especificación humana v1.0

`ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1`, P4. Molde:
`forense/prereg-caja/DISENO-duelo-prospectivo-ENIGH2024-v1_0.md §5.2` y su
precedente `CALC-DUELO-ORIGEN-MOVIL-0001` (ENVIPE, ya sellado — mismo
diseño matemático, código propio porque `tools/duelo/` está ajeno al
perímetro de este acto, ver docstring de `tools/enigh_duelo_nacional.py`).
Fecha de congelamiento: 21/sep/2026.

## 1. Qué mide y qué no mide

Corre los cinco contendientes del diseño (`C-PISO`, `C-T2`, `C-T3`, `C-TS`,
`C-MEDIA`, `§4.2` del diseño) sobre la serie SELLADA de `remesas>0`
(`CALC-B-0001`, 4 puntos: 2016/2018/2020/2022) en modo **origen móvil**:
cada ola predicha sólo con las anteriores de la misma serie sellada. **No
toca ENIGH 2024** — el "oro «2022 como ola nueva»" que pide P4 del encargo
es exactamente la fila `ola=2022` de esta corrida (predicha con
2016+2018+2020, los tres contendientes de tendencia y persistencia y media
construibles a la vez, la única ola donde los cinco lo son).

**No adjudica nada.** Es evidencia cruda de qué tan bien predeciría cada
contendiente si el punto nuevo fuera cualquiera de las tres olas ya
conocidas — no dice qué contendiente ganará el duelo real de 2024, que
necesita el punto de 2024 (COMMIT-3, fuera de este acto).

## 2. Universo y datos

Cero microdato de ninguna ola: los cuatro puntos son la proporción y el
IC95 YA SELLADOS de `CALC-B-0001/resultados.json`
(`RESULT-B-ENIGH-{2016,2018,2020,2022}-{P,IC-LO,IC-HI}`), citado como
input `origen: repo` con hash. `2014` queda fuera de la serie de este duelo
(ver `CALC-ENIGH2016-PERFIL-ESTRUCTURAL-0001/spec.md §2` — corte de serie
NCV vs nueva serie).

## 3. Contendientes (verbatim del diseño §4.2, código en `tools/enigh_duelo_nacional.py`)

- **C-PISO**: persistencia t−1, con su IC95 sellado.
- **C-T2**: MCO en logit sobre las 2 olas anteriores más recientes.
- **C-T3**: MCO en logit sobre las 3 olas anteriores más recientes.
- **C-TS**: MCO en logit sobre TODAS las olas anteriores comparables
  (mínimo 2; con la ventana de 4 olas de este duelo, coincide exactamente
  con C-T3 cuando hay 3 anteriores y con C-T2 cuando hay 2 — el propio
  diseño §4.2 pide comprobar esto por comando antes de congelar:
  `RESULT-ENIGHDM-COINCIDENCIAS-JSON` lo hace).
- **C-MEDIA**: media en logit de todas las olas anteriores comparables.

Todos en escala logit (diseño §4.1); IC95 por método delta desde el EE en
proporción de cada punto sellado.

## 4. D-22 — nulos posibles, declarados

Con sólo 3 olas de historia máxima (2016→2018→2020→2022), varios
contendientes son `NO-CONSTRUIBLE` en las olas tempranas: `C-T2`/`C-T3`/
`C-TS` no existen para predecir 2018 (0 o 1 ola anterior). Esto es
`NO-CONSTRUIBLE-SERIE-INSUFICIENTE`, no un error — `_resumen()` filtra a
`n_olas=0` con todos los campos `flotante` en `None`, declarado
`permite_no_estimable: true` en cada uno. Ningún `NaN`: todo valor no
finito se convierte en `None` antes de canonizar (los propios cálculos de
`tools/enigh_duelo_nacional.py` sólo producen `float` finito o `None`, sin
paso por `NaN`).

## 5. RESULT

27 RESULT: por contendiente (`N-OLAS`, `MAE-PP`, `SESGO-PP`,
`COBERTURA-R-EN-IC-CAND`) × 5 contendientes = 20; más `MODULO-SHA256`
(declara el sha256 de `tools/enigh_duelo_nacional.py` en el momento de esta
corrida — mismo patrón que el precedente de ENVIPE con
`tools/duelo/tendencia_nacional.py`), `SERIE-OLAS-JSON`,
`VENTANA-COMUN-JSON`, `RESUMEN-JSON` + su `SHA256`, `POR-OLA-JSON`,
`COINCIDENCIAS-JSON`.

## 6. Resultado medido (declarado aquí, antes del RESULT — D-22 exige que el
resultado no sea sorpresa para quien lea la spec después)

`C-MEDIA` obtiene el MAE más bajo (0.1406 pp sobre las 3 olas
construibles) frente a `C-PISO` (0.1867 pp) en este ensayo retrospectivo —
**esto NO corrobora ni refuta B-bis-1 del diseño** (que es sobre el duelo
REAL de 2024, no sobre este ensayo de 3 puntos históricos); se declara
honestamente como lo que es: evidencia cruda de una ventana muy corta (3
olas), no un veredicto.
