# ACTO GEN2-ARBITRO-MARGINALES-1 · cierre · 21/sep/2026 · CAJA

Encargo: `forense/encargos/2026-09-21-GEN2-ARBITRO-MARGINALES-1.md` (sello de cuerpo
`b6d73b3f…`, SHA de redacción `55c8d57c` = `origin/main` al abrir; 0-bis `ed7d8482`).
Rama `acto/gen2-arbitro-marginales-1`, worktree `/home/pc0/mm-arbitro-marginales-1`,
Opus 5, MODO ABIERTO hasta cada COMMIT-1 y RÍGIDO desde ahí. Entorno derivado
CAJA (corpus montado, 420 archivos examinados; `sin_variable`; red 200). Contadores
movidos: **corridas GEN2 selladas +4** (`cuenta_gen2 = SI` ×4, `envuelto_legacy = NO`
×3 y `SI` ×1 con firma 3D caso por caso en `decisiones.tsv`); **`celdas_validadas`
73 → 77**; **`SOLO-PISO` 57 → 0 (57 `EVALUADA`)**; `adoptados_activos` no se mueve; nada
se adopta.

## 0 · Premisas verificadas (§3 del encargo) y latitud tomada (§6)

- `[EJECUTADO]` marcador en `55c8d57c`: 57 `SOLO-PISO` (ENIF 2024 32 · ENVIPE 2025 13+2 ·
  ENCIG 2025 10) — **cierto**; 89 `IDENTICO` — cierto.
- `[EXISTE]` pisos sellados y sus medidores — **funcionan**: el punto de entrada nuevo,
  corrido sobre la ola anterior, reproduce los tres pisos + formalidad con Δ = 0
  (192 / 90 / 60 RESULT, IC incluidos).
- `[EJECUTADO]` «de la ola nueva sólo existen los C2-IC y los pilotos… 9 marginales
  sellados» — **parcialmente falso, sin efecto en qué se mide**:
  `CALC-C2-COMPUESTO-IC-ENIF2024-0001` ya tiene sellados **28** marginales por eje de
  ENIF 2024 (`…-G-MARG-*`, punto e IC), y `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` **8** de
  ENCIG 2025; ENVIPE 2025 ninguno con `P` (el C2-IC de ENVIPE sólo selló deltas de
  control). Se **citan y cotejan** en la adjudicación (36 celdas), no se re-miden como
  cifra: el procedimiento es el del piso (encargo §3, «mismo procedimiento… apuntado a la
  ola nueva») y se reporta su distancia al sellado.
- Latitud: un CALC por encuesta (tres) + un CALC de adjudicación (aritmética entre
  sellados), que es lo que el marcador y el tablero consumen. El remuestreo, la rejilla y
  las conductas se **importan** del medidor sellado del piso (input por sha256), no se
  reescriben. El `total` por desenlace se emite además de las celdas del marcador (nacional
  y control de coherencia).
- `origin/main` se movió durante el acto (`#962`, TUBERÍA): fusionado sin conflicto;
  esta cascada usa el mecanismo nuevo (ADR de raíz, fragmento `canon/L0/`).

## 1 · Lo que se midió (GEN2, cadena completa)

| CALC | corrida | RESULT | null | universo | replay |
|---|---|---|---|---|---|
| `CALC-ARBITRO-MARGINALES-ENIF2024-0001` | `--6fb36eb86eaf` | 222 | 0 | 13 502 personas elegidas 18+; formalidad 9 312 (4 134 blanco por secuencia, 56 «no sabe») | REPRODUCE/IDENTICO (aislado) |
| `CALC-ARBITRO-MARGINALES-ENVIPE2025-0001` | `--2fbfd8c334e6` | 116 | 0 | 40 280 delitos (evasión); 1 016 (denuncia, BPCOD=01) | REPRODUCE/IDENTICO |
| `CALC-ARBITRO-MARGINALES-ENCIG2025-0001` | `--d7455c958e41` | 79 | 0 | 20 203 trámites de luz con canal válido (189 excluidos); 1 con EDAD 97, 114 con 98/99 fuera del eje edad | REPRODUCE/IDENTICO |
| `CALC-ARBITRO-PERSISTENCIA-ERROR-0001` | `--72bc60d4f763` | 903 | 0 | 57 celdas enlazadas | REPRODUCE/IDENTICO |

Guardia de una sola variable (firma 3D, segunda mitad) en cada medidor: `marginal()`
con un `str` de eje de lista blanca; auditoría AST antes de abrir el zip (imports,
`groupby`/`crosstab`/`pivot`, `merge` sólo `ID_PER`/`m:1` en `_carga`, eje literal, `_cells`
sólo en `marginal`, ningún `_eje_*` con dos comparaciones, ninguna constante de otro
instrumento); 7 reglas × 3 medidores probadas por mutación en
`tests/test_arbitro_marginales.py` (41 casos verdes en CAJA; censado
`NECESITA-DEPENDENCIA(pytest)` en CI, como sus hermanos). Ningún cruce visto, derivado
ni impreso; los 20 pares `RESERVADA` de las tres olas siguen reservados; `envipe2026*`
no se nombra en ningún input ni constante; la sección de crédito de ENIF 2024 no se carga.

Nemónicos resueltos por texto (A.15), todos ya documentados en el repo, sin abrir la ola
antes del COMMIT-1: ENIF `FAC_ELE→FAC_PER`, `EDAD→EDAD_V`, `P3_1_1→NIV` (00-11; 09
especialidad, 10 maestría, 11 doctorado → superior, 300 personas), `P5_7_i→P5_6_i`,
`P3_10→P3_13` (1-6 con / 7 sin); ENVIPE y ENCIG sólo cambian el nombre del miembro.

## 2 · Adjudicación de la persistencia, por encuesta (PROSPECTIVA)

`d = (R − piso)·100` pp; cobertura = punto R dentro del IC95 del piso; clase por IC de d
(normal, olas independientes). Nunca se promedia entre encuestas.

| encuesta (brecha, unidad) | N | error medio | MAE | máx \|d\| | cobertura (Wilson 95 %) | PERSISTE / CAMBIA |
|---|---|---|---|---|---|---|
| **ENIF 2024** (3 años, persona) | 32 | +0.98 pp | 2.92 pp | 5.20 | **6/32 = 0.19** [0.09, 0.35] | 16 / 16 |
| · D9 `ahorra_solo_informal` | 16 | −1.65 | 2.22 | 4.75 | 5/16 = 0.31 [0.14, 0.56] | 10 / 6 |
| · `informal_cualquiera` | 16 | **+3.62** | 3.62 | 5.20 | 1/16 = 0.06 [0.01, 0.28] | 6 / 10 |
| **ENVIPE 2025** (1 año, delito) | 15 | +2.22 | 2.59 | 5.36 | **8/15 = 0.53** [0.30, 0.75] | 8 / 7 |
| · `evasion` | 13 | +2.14 | 2.56 | 5.36 | 6/13 = 0.46 | 6 / 7 |
| · `denuncia` (cobertura de seguro) | 2 | +2.77 | 2.77 | 3.85 | 2/2 | 2 / 0 |
| **ENCIG 2025** (2 años, trámite) | 10 | **+10.84** | 10.84 | 13.36 | **0/10 = 0.00** [0.00, 0.28] | 0 / 10 |

**Dónde erró la persistencia.**
- **ENCIG (pago de luz por canal digital):** la persistencia falla en las 10 celdas, con un
  salto de nivel de +7.7 a +13.4 pp que ningún eje explica (edad MAE 11.2, escolaridad
  10.2, sexo 11.4): es el mismo hallazgo que el árbitro GEN1 ya había dado (0/10), ahora
  con cadena GEN2. El piso 2023 no sirve como estimador adjudicado de 2025 a dos años; lo
  que persiste es el ORDEN entre categorías (gradiente de escolaridad 0.39 → 0.81, caída
  en 60+), no el nivel. Lectura acotada (§3 de las instrucciones): puede persistir la
  oferta (despliegue del canal) y no un rasgo.
- **ENIF (ahorro):** los dos desenlaces se mueven en sentido opuesto. El ahorro **sólo
  informal** (D9) baja de 2021 a 2024 en casi toda celda (error medio −1.65 pp; `CAMBIA`
  en 18-29 −4.2, superior −4.8, formalidad −3.6/−2.7, 15 000+ −2.3, hombres −2.6), mientras
  el ahorro informal **de cualquier tipo** sube en toda celda (+2.2 a +5.2 pp; 10/16
  `CAMBIA`). Juntos dicen que creció el ahorro informal *con* pata formal, no el
  informal exclusivo: consistente con la lectura de `MAESTRA35-L1` (complemento, no
  sustituto). La persistencia cubre 6/32: a tres años y con 2021 como dato de pandemia, el
  piso es débil en ENIF y el retador tiene margen — pero el eje **cuenta** (4/4 `PERSISTE`)
  y las celdas de nivel bajo (45-59, 60+, hasta primaria) sí persisten.
- **ENVIPE (evasión de norma / denuncia):** a un año la persistencia cubre 8/15 y la mitad
  persiste; erra hacia arriba (+2.2 pp: más evasión en 2025), con `CAMBIA` en complemento
  urbano (+5.0), 45-59 (+5.4), secundaria (+4.2), superior (+3.7), hombres (+3.5) y urbano
  (+2.3). Rural, 18-29, 60+, hasta primaria, media superior y mujeres persisten. Las dos
  celdas de denuncia por cobertura de seguro persisten (n pequeño: IC de d de ±7-8 pp).

**Lectura B-bis (spec §3):** ENVIPE — persistencia corroborada como piso a un año
(cobertura 0.53, IC que incluye 0.5; no incluye 0.95). ENIF — piso débil a tres años
(cobertura 0.19, IC excluye 0.5); por eje manda la lectura: cuenta persiste, sexo y
formalidad no. ENCIG — piso inservible a dos años en NIVEL (0/10); persiste el orden.

## 3 · Hallazgo sobre GEN1 y sobre los pilotos

- **El yaml GEN1 no discrepa en ninguna de las 57 celdas**: máx |R − p_GEN1| = 4.95e-7
  (redondeo a 6 decimales del yaml). El árbitro GEN1 estaba bien medido; lo que le faltaba
  era la cadena (spec, CALC, inputs por hash, sello, replay), no la cifra. No se corrige
  nada en `milpa/`.
- **ENIF vs `CALC-C2-COMPUESTO-IC-ENIF2024-0001`:** 28/28 `COINCIDE` (≤ 1e-6, punto e IC).
- **ENCIG vs `CALC-GOB-DIGITAL-EXE-EMISIONES-0002`:** edad 4/4 `COINCIDE`; escolaridad 3
  `COINCIDE-1E-3` y 1 `DISCREPA` (hasta primaria: Δp = +2.3e-3, n 2 299 aquí vs 2 277 en el
  piloto). Causa, por lectura de los dos medidores: el piloto aplica «caso completo» en
  edad *y* escolaridad dentro de cada máscara (excluye de las celdas de escolaridad los
  trámites con EDAD 97/98/99), el procedimiento del piso —éste— sólo saca del eje al que la
  variable inválida pertenece. Diferencia de universo declarada, no defecto de ninguno de
  los dos; ambos sellados quedan como están.

## 4 · Marcador y tablero (por comando)

`tools/marcador_segmento.py`: lee la tabla de identidad propia
(`forense/prereg-caja/ARBITRO-MARGINALES-metadatos-v1_0.tsv`, `cell_id_piso → cell_id_R`) y,
donde el R GEN2 está sellado en `CALC_ARBITRO_R`, la fila pasa de `SOLO-PISO` (R GEN1 del
yaml) a **`EVALUADA`** con R/IC GEN2, `fuente = <CALC>/<RESULT>` y `error_piso_pp` /
`clase_persistencia` leídos de `CALC-ARBITRO-PERSISTENCIA-ERROR-0001`. Cero cifras nuevas
en el tool. Antes/después (`--json`): `marginales_solo_piso` 57 → 0,
`marginales_evaluadas_gen2` 0 → 57, `cobertura_de_piso` 79 → 79, `sin_piso` 15 → 15,
`estimador_adoptado` 20 → 20; `milpa/estimadores-por-segmento.yaml` byte a byte igual (no
se adopta). Tablero `celdas_validadas` 73 → 77 (clase 2: 53 → 57; las 4 de formalidad
entran; quedan 2 `NO-COMPARABLE` de horizonte_corto sin error). `T-ERROR-PISO-DERIVADO`
se prueba ahora en dos universos (GEN1 y GEN2), cada uno contra su CALC y en los dos
sentidos; `CALC-PISO-PERSISTENCIA-ERROR-0001` queda como la lectura contra GEN1 (no se
toca, sus ids siguen teniendo que calzar).

## 5 · Perímetro y no tocado

Escrito: los 4 CALC nuevos y sus specs (prereg-caja + sidecars), la tabla de identidad
propia, `tests/test_arbitro_marginales.py`, `tools/marcador_segmento.py` +
`tests/test_marcador_segmento.py` (una guardia, forma), `data/corrida0/{corridas,resultados,
marcador-segmento,decisiones}.tsv` por comando, `forense/replay-evidencia.tsv` (4 asientos),
`forense/analisis/gen2-arbitro-marginales-1/`, esta nota, cascada. No tocado: pisos y
pilotos sellados, `milpa/`, celdas-D, `tools/corrida0.py`, la rejilla del árbitro,
`CALC-PISO-PERSISTENCIA-ERROR-0001`. Pisadas ajenas en las vistas: 0 (el diff de
`resultados.tsv` reordena sólo filas propias).

## 6 · Preguntas a mesa (con recomendación) — no bloquean

1. **Adopción del piso en marginales (A-bis 6).** «Un piso no vencido es el estimador
   adjudicado de su celda y se adopta salvo veto»: aquí hay 57 pisos y ninguno tiene
   retador; con la cobertura medida (ENIF 0.19, ENVIPE 0.53, ENCIG 0.00) mesa decide si
   «no vencido» aplica sin retador. Recomendación: adoptar por encuesta donde la cobertura
   no excluye 0.5 (ENVIPE), diferir ENIF y vetar ENCIG en nivel. PARO g: este acto no adopta.
2. **`cuenta_gen2 = SI` de `CALC-ARBITRO-PERSISTENCIA-ERROR-0001`** vía fila 3D en
   `decisiones.tsv` (el yaml entra sólo como control): ratificar o vetar al fusionar (FP).
