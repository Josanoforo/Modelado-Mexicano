# Nota de cierre · ACTO GEN2-DIN-CREDITO-CELDAS-D-2

23/sep/2026, NUBE. Encargo:
`forense/encargos/2026-09-23-GEN2-DIN-CREDITO-CELDAS-D-2.md`
(sha256 cuerpo `8187fe44956c8ec1b5f487b3764317f9d6431fff3e0a922c247fc298b8da6877`).
Rama `acto/gen2-din-credito-celdas-d-2`. Firma de unidad de mesa dada
verbatim al lanzar (§2 del encargo).

## 0 · Premisas verificadas

- `[EJECUTADO]` `spec.yaml` de `CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002`
  confirma: l.8 `tipo: ADJUDICACION-GUARDADA-RESERVA`; l.13 `sucede_eje_de` al
  `-0001` solo en el eje escolaridad (A.10); l.60-63 (`regla_adjudicacion`)
  `umbral_vence_pp: inf`, vocabulario `[NADIE-VENCE, PROPUESTA-CON-RESERVA,
  NO-ADJUDICABLE, NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO]`.
- `[EJECUTADO]` `resultados.json` del -0002: 1346 RESULT, sha256
  `9ad5c0864b308ab1e8c57846c087aa33e206d9e795fd75c59d4fb3fa054ccc9e`.
  `RESULT-DIN-CREDITO-PREDICCION-2024-ESC2-ORO-VEREDICTO = REPRODUCE-ORO`
  (las 12 celdas no-escolaridad reproducen el oro del -0001, sha256
  `95f027ef0b58d30db29a7d787642d785dc21713094f2e34fca234f39c8864e26`).
- Por lector JSON (`data/corrida0/.../resultados.json`, no awk): **9
  conductas** tienen `*-VEREDICTO-PRIMARIO` bajo `ADJ16`, no 7 (el NC
  `…e6b2-01` citaba 7 conductas de un conteo distinto/parcial — se
  re-deriva aquí y se corrige).

## 1 · P1 · Tabla fuente (por lector JSON, antes del primer yaml)

Piso = PERSISTENCIA (heredado del backtest 2012→2021, -0001). Retador
primario = mejor `TENDENCIA-X` por MAE puntual. `n_elegibles` = celdas del
eje (16, salvo K2-AUTOMOTRIZ=15); `n_puntuadas` = 13 (12 para
K2-AUTOMOTRIZ) por candidato tendencia.

| conducta | retador primario | dictamen (VEREDICTO-PRIMARIO) | ΔMAE pp | IC95 | n_eleg / n_punt | piso MAE pp |
|---|---|---|---|---|---|---|
| K1 | TENDENCIA-SERIE | **PROPUESTA-CON-RESERVA** | +1.7506 | [+0.6843, +2.4126] | 16/13 | 4.7467 |
| K2-AUTOMOTRIZ | TENDENCIA-3 | NADIE-VENCE | −0.0644 | [−0.4499, +0.0816] | 15/12 | 0.3405 |
| K2-DEPARTAMENTAL | TENDENCIA-2 | NADIE-VENCE | +0.2644 | [−1.1433, +0.9356] | 16/13 | 2.5837 |
| K2-NOMINA | TENDENCIA-SERIE | NADIE-VENCE | −0.1476 | [−0.3788, +0.1231] | 16/13 | 1.0162 |
| K3 | TENDENCIA-3 | NADIE-VENCE | +0.5581 | [−0.8438, +0.9738] | 16/13 | 2.2179 |
| K4A-AUTOEXCLUSION | NINGUNO-HABILITADO | **NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO** | — | — | 16/0 | 4.8588 |
| K4B-OFERTA | NINGUNO-HABILITADO | **NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO** | — | — | 16/0 | 4.8272 |
| K5 | TENDENCIA-SERIE | NADIE-VENCE | +0.6930 | [−0.4453, +1.1734] | 16/13 | 2.2323 |
| K6-P-TENEDORES | TENDENCIA-SERIE | **PROPUESTA-CON-RESERVA** | +2.5434 | [+0.4820, +3.2201] | 16/13 | 4.4615 |

Conductas sin dictamen: ninguna — las 9 conductas de la lista blanca
`CONDUCTAS_AUTORIZADAS` del -0001 tienen `VEREDICTO-PRIMARIO` sellado en el
-0002, incluidas K4A/K4B con `NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO` (el
silencio no es un valor, E.5 — se registran igual, con ese dictamen).

## 2 · P2 · Nueve celdas-D registradas

`data/curacion-registro/celdas-d/DIN.credito_{k1,k2_automotriz,
k2_departamental,k2_nomina,k3,k4a_autoexclusion,k4b_oferta,k5,
k6_p_tenedores}.enif2024.marginal16.yaml` — una por conducta, esquema del
piloto 4 (`tests/test_celdas_d.py`, `vocabulario_version: 0.5`, sin
`adjudicacion_por_celda` — ese campo es exclusivo de v0.6). Cada yaml:

- `momentos_holdout_refs`: `CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002--04564bb97815`
  (commit `1d9322a`, `[COMMIT-2]`).
- `veredicto` = dictamen verbatim del CALC (columna "dictamen" de la tabla
  §1).
- `champion_actual: PERSISTENCIA` en las 9 — ningún retador venció
  (`VENCE-RETADOR` es inalcanzable por diseño, `umbral_vence_pp: inf`);
  `PROPUESTA-CON-RESERVA` (K1, K6-P-TENEDORES) **no adopta** al retador
  (A-bis 6 / firma de mesa 17/sep/2026: el piso no vencido se adopta salvo
  veto de mesa).
- `relacion_complemento` cita el oro (-0001) por hash y
  `RESULT-...-ORO-VEREDICTO=REPRODUCE-ORO`.
- **Marcador PROSPECTIVA/RETROSPECTIVA** (§4 v2.16): `RETROSPECTIVA-MECANICA`.
  El propio `spec.yaml` del -0002 declara `exposicion_historica:
  "ENIF-2024-CREDITO-YA-ABIERTA-POR-0001"` (l.14) — el -0001 ya abrió y
  selló ENIF 2024 con estas mismas 9 conductas y columnas; este CALC no
  abre dato nuevo ni selecciona variante: solo recorrige por bytes la
  lectura de dos dígitos de `niv` en el eje escolaridad (defecto heredado,
  A.10). Es exactamente la definición de `RETROSPECTIVA-MECÁNICA`
  ("validación de origen móvil sin selección de variante"), no una emisión
  PROSPECTIVA nueva — aunque las emisiones del -0001 mismas sí lo fueron
  (selladas antes de abrir 2024). No se colapsan las dos columnas.
- Validado contra `tests/test_celdas_d.py`: 19/19 archivos ok (10 previos +
  9 nuevos).

## 3 · Clase de `_celdas_validadas` — no admite esta unidad (§6 del encargo)

`tools/celdas_validadas.py:197` `_celdas_validadas` (ajeno, no se edita)
compone tres clases:

- **Clase 1 · CRUCE vs R** (`_celdas_d_adjudicadas`, l.62): exige un RESULT
  por CELDA con sufijo `-C2-D-PP` o prefijo `-ARB-D-C2-` en el CALC citado
  por `momentos_holdout_refs`. El -0002 emite por **conducta** (`ADJ16-K1-
  TENDENCIA-SERIE-DELTA-MAE-PP`, agregado sobre 13-16 celdas), no por celda
  individual con ese patrón — **no calza**.
- **Clase 2 · PERSISTENCIA t-1 vs R**: lee filas con `error_piso_pp` en
  `data/corrida0/marcador-segmento.tsv`. El -0002 no tiene fila ahí.
- **Clase 3 · duelo de tres nacional**: lee `CALC-TRIADA-0002`, no aplica.

**Verificado por comando** (`python3 tools/celdas_validadas.py`):
`total_celdas_validadas` = 92 antes y después de este acto (sin cambio).
Las 9 celdas-D de crédito aparecen en `clase_1_celdas_d_sin_contar` con
motivo declarado por comando: *"veredicto sellado pero ningún RESULT de
error por celda localizado en sus momentos_holdout_refs (-C2-D-PP /
-ARB-D-C2-)"* — negativo con universo (A.4), no un silencio.

**Esto es un desvío de premisa de §0 tipo "qué se mide" (el CONTADOR),
pero el propio encargo §6 lo previó y dio la latitud exacta**: "si
`_celdas_validadas` no admite la clase... pregunta a mesa (sigues)".
`tools/celdas_validadas.py` es **ajeno** (§9 del encargo, perímetro de
concurrencia) — extenderlo con una cuarta clase ("conducta agregada vs
piso, N-CELDAS-PUNTUADAS ponderado") es trabajo de TUBERÍA, no de este
acto. Se registra (P2) sin contar, se pregunta a mesa, y se sigue: NC
`DECISIÓN-DE-MESA-PENDIENTE`, sucesor `GEN2-TUBERIA-CELDAS-D-CONDUCTA-1`
(diferido, `SIN-ASIGNAR` hasta que mesa decida si vale la pena extender el
contador o dejar esta clase fuera por diseño).

## 4 · Corrección de premisa — conteo de "conductas con dictamen"

El criterio "hecho" del encargo (`ls ... | grep -c '^DIN\.'` = número de
conductas con dictamen) asumía cero archivos `DIN.*` previos. Ya existía
`DIN.ahorro_solo_informal.enif2024.localidad_x_edad.yaml` (piloto 1, otro
dominio/CALC — homónimo de prefijo, no de acto, se descarta por A.8). El
conteo correcto es: `ls celdas-d | grep -c '^DIN\.'` = **10** (1 previa +
9 nuevas); las **9 nuevas** son las conductas con dictamen del -0002. Se
declara aquí en vez de ajustar el criterio (logística/estado del repo,
objetivo intacto — v2.16 §2).

## 5 · Una línea

**Las 9 conductas de crédito 2024 (eje escolaridad corregido) entran a
`celdas-d/` con dictamen verbatim del CALC y el -0001 citado como oro; el
contador `celdas_validadas` no sube porque la unidad "conducta agregada"
no calza en ninguna de las tres clases que el derivador admite hoy — se
declara, se pregunta a mesa si vale extenderlo, y no se adopta nada.**

## CONTADOR

`cuenta_gen2 = SI` (cabecera del encargo); no adopta. Cero corridas nuevas
(este acto solo registra celdas-D desde RESULT ya sellados del -0002).
`celdas_validadas`: 92 → 92 (sin cambio; ver §3). `status` sube en `ls
celdas-d | grep -c DIN`: 1 → 10.

`tests/test_celdas_d.py`: 19/19 ok. `tests/test_din_credito_celdas_d_2.py`
(nuevo, huérfano): RESULT citados existen, verificado.
