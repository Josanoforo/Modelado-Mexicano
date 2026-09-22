# ENIF-PERSISTENCIA-IC-CALIBRADO · spec v1.0 (COMMIT-1, congelada)

ACTO GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1 · 22/sep/2026 · encargo
`forense/encargos/2026-09-22-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1.md` (0-bis `286889ee`).
CALC: `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001` · MODO RÍGIDO desde este commit ·
cuenta_gen2 = SI (encargo, CABECERA) · no adopta · `celdas_validadas` no se mueve.

Rótulo de todo lo que este procedimiento produce: **RETROSPECTIVA-MECÁNICA** — R 2024 ya
fue vista (`FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02`: 6/32 = 0.19 [0.09, 0.35]); una
sola regla, sin selección de variante (v2.16 §4, E.6 «un cruce ya visto sigue sirviendo
para describir, calibrar y evaluar en retrospectiva, rotulado así»). Ninguna frase de
producto mezcla esta cobertura con la PROSPECTIVA de los pilotos.

## §0 · Premisas verificadas y exposición declarada

1. **Qué vio esta sesión antes de congelar.** R 2024 y el 6/32 (ya públicos en el repo);
   la estructura de ENIF 2015, 2018 y 2021: descriptores de campos (nombres de columna del
   DBF `tmodulo1.DBF` de 2015 y cabecera de los CSV 2018/2021), y el diccionario de datos
   de 2018 y 2021 (texto de P5_4/P5_5/P5_9/P5_13 y P5_4/P5_7). **Ningún valor** de 2015
   ni de 2018, ni de 2021 en el universo 18-70 armonizado. Sobre ENIF 2021 18+ corrió el
   ORO (§7), que sólo reproduce los 32 pisos ya sellados. Exposición:
   `CIEGO-A-2015-2018-ESTRUCTURA-LEIDA`.
2. **Marginales 2015/2018 por eje no estaban sellados** para estos desenlaces: los CALC que
   leen ENIF 2015/2018 (`DIN-CREDITO-PISOS-ENIF2015/2018-0001`, `DIN-CREDITO-K2-BANCARIA-
   HISTORIA-0001`, `R-FAM-M-01*`, `ENIF-FINTECH-0001`) miden crédito, FAM o fintech, no
   ahorro por vía (búsqueda por `spec.yaml`, sin abrir sus resultados). Se derivan aquí.
3. **Premisa `[EXISTE]` `enif2015_csv` es falsa**: el manifiesto no tiene ese id. El
   payload de 2015 es `enif_2015_enif_2015_bd_dbf` (DBF), el mismo que usó el carril
   histórico de crédito. Logística, no toca qué se mide.
4. **R 2024 se lee del CALC sellado GEN2**, `CALC-ARBITRO-MARGINALES-ENIF2024-0001`
   (`resultados.json`), no de `milpa/tramite-ola5-propuesta-v0.yaml`: el árbitro midió que
   el yaml no discrepa en ninguna de las 57 celdas (4.95e-7) y leer `milpa/` volvería la
   corrida `envuelto_legacy`. ENIF 2024 no se abre.

## §1 · Celdas

Las 32 celdas con `instrumento = ENIF` de `forense/prereg-caja/ARBITRO-MARGINALES-metadatos-
v1_0.tsv` (sha256 `80af0c37…`), leídas de la tabla (E.5), con su `cell_id_R`, `cell_id_piso`
y `calc_piso`: 2 desenlaces (D9 `ahorra_solo_informal`, `informal_cualquiera`) × 16
categorías en 6 ejes (sexo 2, edad 4, escolaridad 4, localidad 2, formalidad 2, cuenta 2).
El medidor PARA si la tabla no trae exactamente 32.

## §2 · Comparabilidad por texto por ola (A.15c) y constructo del cambio

Fuente: `data/ahorro-comparabilidad-texto-v1_0.tsv` (sha256 `d3512b93…`), sin reinterpretar.
Una ola entra a una celda si **todos** sus objetos (desenlace + eje) son MISMO-INSTRUMENTO o
CAMBIO-MENOR. Veredictos congelados (el medidor PARA si la tabla dice otra cosa):

| objeto | 2015 | 2018 |
|---|---|---|
| D-INF (vías informales) | CAMBIO-MENOR (orden distinto; «alguna» es invariante) | MISMO |
| D-FOR (vías formales) | CAMBIO-DE-INSTRUMENTO | CAMBIO-MENOR (8 de 9: falta la vía 8) |
| E-SEX / E-LOC | MISMO | MISMO |
| E-EDA | CAMBIO-MENOR (18-70) | CAMBIO-MENOR (18-70) |
| E-ESC | CAMBIO-MENOR (un dígito) | MISMO |
| E-FOR | CAMBIO-DE-INSTRUMENTO | MISMO |
| E-CTA | CAMBIO-DE-INSTRUMENTO | CAMBIO-MENOR (8 de 9) |

Consecuencia: **D9 no es construible en 2015 y en 2018 sólo como D8**; informal-cualquiera ×
{formalidad, cuenta} no entra en 2015. 2015 es comparable en 12 de 32 celdas (informal ×
sexo/edad/escolaridad/localidad) y NO en 20 de 32.

**Rama elegida (encargo §6, la recomendada, declarada; pregunta a mesa abierta en el
cierre):** como 2015 no es comparable en la mayoría de las celdas, **el intervalo se calibra
sólo con el cambio 2018→2021** en las 32 celdas. 2015 se mide donde es comparable y entra
**sólo como DESCRIPTIVO** (Δ 2015→2018 y un τ² «con 2015» por grupo), nunca al intervalo ni
a la cobertura.

Constructo del cambio, idéntico en las dos olas del par:
- **Universo:** persona elegida de **18 a 70 años** (2018 sólo elige en 18-70; en 2021 el
  18-70 es un DOMINIO — máscara sobre el marco entero, sin recortarlo, para que el
  bootstrap sortee las mismas UPM que el piso). La celda 60+ es 60-70 en el cambio.
- **informal-cualquiera:** alguna de P5_1_1..P5_1_6 = 1; No si las seis = 2 (2018 y 2021,
  mismos seis reactivos).
- **D9 → D8:** «ahorra sólo informal» con las vías formales armonizadas a OCHO: 2021
  P5_4/P5_7 k ∈ {1..7, 9} (se quita k = 8, «cuenta contratada por Internet o aplicación
  como Mercado Pago o Albo», diccionario 2021); 2018 P5_9/P5_13 k ∈ {1..8} (k = 8 «Otro»
  ↔ 2021 k = 9 «otro», por texto del diccionario 2018). Reglas de `_formal`/`_known_any`
  del medidor sellado de -0003. **2018 — blanco por pase = No:** quien respondió No a 5.4
  y a 5.5 no pasa a 5.9; sus P5_9_k en blanco se leen como 2 (cuestionario: 5.4 Sí → 5.9;
  No → 5.5; 5.5 Sí → 5.9). El matiz (en 2018 la batería por tipo está gateada por dos
  filtros agregados que no nombran cheques, plazo fijo ni fondo de inversión) es el
  CAMBIO-MENOR de la tabla y se declara, no se corrige.
- **Ejes:** sexo `SEXO`; edad `EDAD` con los cortes de -0003; escolaridad `NIV` (2018) /
  `P3_1_1` (2021) con los cortes de -0003; localidad `TLOC` 1-2 / 3-4; formalidad `P3_11`
  (2018) / `P3_10` (2021): 1-5 con seguridad social, 6 sin, 9/blanco fuera; cuenta —
  2018: con cuenta si P5_4 = 1 o P5_5 = 1, sin cuenta si ambas = 2 (regla sellada del mapa
  `DIN-CREDITO-PISOS-HISTORIA-mapa-v1_0.tsv`); 2021 armonizada: la batería P5_4 sin k = 8.
- **Diseño:** `FAC_PER` (2015/2018) / `FAC_ELE` (2021), `EST_DIS` × `UPM_DIS`;
  `_estimate` de -0003 importado por bytes: bootstrap de UPM estratificado, 10 000
  réplicas, PCG64(42), un plan por ola, IC percentil 2.5/97.5.
- **2015 (descriptivo):** `tmodulo1.DBF` (P5_1_1..6, SEXO, EDAD, NIV, TLOC, FAC_PER,
  EST_DIS, UPM_DIS), lector DBF del medidor histórico sellado importado por bytes.

## §3 · Pregunta a mesa (encargo §6), sin detener el acto

«2015 no es comparable por texto en 20 de 32 celdas. ¿Calibrar sólo con 2018→2021
(**recomendado**, es lo que este COMMIT-1 congela) o esperar?» La alternativa «mezclar 2015
donde es comparable» no se evalúa: sería una segunda variante con R ya vista.

## §4 · Regla del intervalo (congelada; no se ajusta con el resultado)

Por celda c del grupo de pooling g = (desenlace, eje) — 12 grupos, el pooling es **por eje
dentro de cada desenlace**, no por celda sola ni entre desenlaces:

- Δ_c = logit h2021(c) − logit h2018(c), con h los marginales armonizados de §2.
- τ²_g = media de Δ_c² sobre las celdas de g con Δ definido. **Sin centrar** (la
  persistencia predice Δ = 0: un cambio común a todo el eje es error de persistencia, no
  se descuenta) y **sin restar ruido muestral** (el error que se evalúa, R2024 − p2021,
  también trae el ruido de dos olas). Ambas decisiones hacen el intervalo más ancho, no
  más angosto.
- ee_m(c) = (logit IC-HI − logit IC-LO) / (2 · 1.959964), del IC95 sellado del piso 2021
  (`CALC-PISOS-ENIF2021-EJES-0003` o `-FORMALIDAD-0001`).
- **IC calibrado:** expit( logit p2021(c) ± 1.959964 · √(ee_m² + τ²_g) ) →
  `IC-CALIBRADO-INF` / `IC-CALIBRADO-SUP`; `tipo_incertidumbre = muestral +
  cambio-entre-olas`. Centro = el piso sellado (18+); τ² se estima en 18-70 y se aplica
  al piso 18+ (declarado: es el único universo común).
- **NO-CALIBRABLE:** una celda cuyo grupo no tiene ningún Δ definido (h en 0 o 1) o cuyo
  piso no tiene IC en (0, 1); queda fuera del denominador de la cobertura y se cuenta.

Descriptivos que **no** entran al intervalo: media de Δ por grupo, ruido medio
se²(2018) + se²(2021) en logit por grupo, y τ² «con 2015» (informal × 4 ejes).

## §5 · Cobertura (v2.16 §4)

- Por celda: **DENTRO** si IC-CALIBRADO-INF ≤ R2024 ≤ IC-CALIBRADO-SUP (R punto,
  `CALC-ARBITRO-MARGINALES-ENIF2024-0001`). Control: el mismo cotejo con el IC muestral
  sellado debe dar 6/32 (COINCIDE, o el medidor lo reporta DISCREPA).
- Agregada: GLOBAL, por desenlace, por eje y por conglomerado (grupo desenlace × eje):
  N, N-DENTRO, cobertura con IC binomial de Wilson (z = 1.959964, n = celdas calibrables).
- **Por conglomerado (las celdas comparten muestra):** para GLOBAL, además, Wilson con
  n efectivo = número de grupos desenlace × eje con celdas calibrables (12), sobre la misma
  proporción — el IC conservador que manda en §6.

## §6 · Umbral X para la FP de adopción (P3), fijado aquí, antes del dato

Propuesta de FP a mesa (este acto la abre, no la firma): «adoptar ENIF con IC calibrado si
cobertura GLOBAL ≥ **X = 0.80**». Lectura mecánica que el medidor emite
(`REGLA-X-LECTURA-MECANICA`):
- cobertura ≥ 0.80 y límite inferior Wilson por conglomerado ≥ 0.50 → `CUMPLE`;
- cobertura ≥ 0.80 y ese límite < 0.50 → `CUMPLE-CON-RESERVA` (propuesta con reserva);
- 0.50 ≤ cobertura < 0.80 → `NO-CUMPLE` (ENIF sigue DIFERIDA);
- cobertura < 0.50 → `NO-CUMPLE-PERSISTENCIA-TRIENAL-NO-ES-PISO` (el supuesto del
  encargo §3 resultó falso: va al informe).
Por qué 0.80: nominal 0.95 menos la holgura de estimar τ² con 2 a 4 cambios por grupo; y
0.50 es el piso que el propio encargo nombra.

## §7 · Oro, semilla, tolerancias, entorno

- **ORO (antes de este commit, y de nuevo dentro de la corrida):** `mide_2021` con
  `armonizada=False` (18+, nueve vías) reproduce P, IC-LO, IC-HI y N de los 32 pisos
  sellados a |Δ| ≤ 1e-10 (N exacto). Sin tocar el dominio 18-70.
- Semilla PCG64(42), 10 000 réplicas; tolerancia de replay 1e-10 (flotante).
- Prueba de congelación: `tests/test_enif_persistencia_ic_calibrado.py` (sintético con la
  forma de las tres olas, regla a mano, guardia de comparabilidad, ids declarados; `--oro`).
- Entorno CAJA; corpus `data/raw` → `mm-corpus/raw`.

El primer resultado que produzca este procedimiento es el que se reporta.
