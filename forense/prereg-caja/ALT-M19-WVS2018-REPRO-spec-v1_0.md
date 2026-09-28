# M19 · WVS 7 México 2018 · reproducción GEN2 del abridor GEN1 de R8.3 (eje 2)

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-CALC-ALTERNOS-LOTE-1` (0-bis `795b1053`), fila 59 de
`canon/mapa-instrumentos-alternos-v1_0.tsv` («reproducción GEN2 del
abridor»). Dictamen de OBTENCION-PREVIA-1 (`momentos-09-22.tsv`, fila M19,
`RES-0194`): «EXISTE-NO-SATISFACE como RESULT GEN2: abridor (WVS7 México
2018, persona, 1741 filas, eje 2 d=-0.4422pp IC[-3.36,+2.47]) … es GEN1 sin
CALC ni sello … Camino: CALC GEN2 que reproduzca el abridor desde WVS7
(payloads f00013146_wvs_wave_7_mexico_csv_v5_1 en corpus)». Un CALC:
`CALC-ALT-M19-WVS2018-REPRO-0001`. No adopta; no re-adjudica R8.3.

## Qué ya está medido (E.5)

`CALC-WVS-PISOS-2018-0001` selló marginales por segmento de `Q57`–`Q61` y
otros; no el contraste por contexto de entidad. Este CALC no recalcula esos
pisos: reproduce el estimando del abridor.

## Procedimiento, verbatim de la spec GEN1 (no se cambia nada)

Fuente: `forense/hitoD-R8_3-especificacion-v1_0.md` §3.1 y §4.
- **CONFÍA EN EL DESCONOCIDO** := `Q61 ∈ {1 Trust completely, 2 Trust
  somewhat}` sobre `Q61 ∈ {1,2,3,4}`.
- **TIENE PUENTE** := `Q60 ∈ {1, 2}`; **SIN PUENTE** := `Q60 ∈ {3, 4}`
  (complemento dentro de la escala; un código perdido no es SIN PUENTE —
  las máscaras con perdido se vuelven falso, como declaró el abridor, §1 (i)).
- **ENFORCEMENT ALTO** := `Q70 ∈ {1 A great deal, 2 Quite a lot}`.
- **Eje 2:** proporción ponderada (`W_WEIGHT`) de ENFORCEMENT ALTO sobre
  `Q70 ∈ {1..4}` dentro de cada `N_REGION_ISO`; entidades elegibles con
  `n ≥ 30`, donde `n` = filas del archivo en la entidad («la entidad más
  pequeña del archivo tiene n=8»); corte en la **mediana** de las elegibles;
  `ALTO` := proporción **estrictamente mayor** que la mediana, `BAJO` el
  resto (el abridor reporta 9 ALTO y 10 BAJO de 19: con 19 valores la
  mediana es el décimo y queda en BAJO). A cada informante, el nivel de su
  entidad.
- **Estimando principal:** `d = p(CONFÍA | SIN PUENTE, ALTO) − p(CONFÍA |
  SIN PUENTE, BAJO)`. **Secundaria:** el mismo contraste sin restringir
  por puente.
- **Varianza:** `tests/svystat.py::diff_ultimate_cluster`, un solo estrato,
  UPM `I_PSU`; el archivo completo entra (dominio, no submuestra). Fijado
  por sha256.
- Payload: el `.dta` v5.1 que leyó el abridor
  (`f00013084_wvs_wave_7_mexico_stata_v5_1`, misma versión que el CSV
  `f00013146` que nombra la fila del mapa). Se prefiere el `.dta` porque el
  CSV v5.1 va separado por `;` y su separador decimal no está declarado: una
  coma decimal en `W_WEIGHT` anularía los pesos en silencio. Desviación de id
  frente al mapa, declarada.

## Criterio de reproducción, fijado antes de correr

Referencia (`forense/hitoD-R8_3-abridor-v1_0.md` §2): 19 entidades
elegibles; mediana `0.243483`; `p_ALTO = 0.045580`; `p_BAJO = 0.050002`;
`d = −0.004422`. **REPRODUCE** si el número de elegibles es idéntico y las
cuatro cifras casan con `|Δ| ≤ 5e-7` (media unidad del último decimal
publicado en %). Si no, **NO-REPRODUCE**, se reporta con las cifras propias
y no se corrige el procedimiento para que case (D-d, spec congelada). El IC
del abridor ([−3.36, +2.47] pp) se reporta al lado, sin ser criterio.

## Qué pasa si el falsador no refuta

La reproducción no re-adjudica: el veredicto A del abridor (25/ago) es de
mesa. Si REPRODUCE, el RESULT GEN2 sellado sustituye la cifra GEN1 sin
sello como fuente de `RES-0194`; si NO-REPRODUCE, se reporta la
discrepancia (E.3) y la cifra GEN1 queda sin respaldo GEN2.

## Auditoría v2.16

- **Unidad:** persona adulta. **Escala:** proporción; `d` en proporción.
- **RETROSPECTIVA:** ola 2018 vista y ya usada por el abridor.
- **¿Incentivo o psicología?** Confianza declarada; el contexto es
  percepción agregada por entidad, no enforcement medido.
- **¿Clase media urbana?** 12 de 31 entidades quedan fuera por n < 30.
- **HOLDOUT gastado: `M19`** (el mismo momento que gasta el CALC ENCUCI;
  censo C2: 0 menciones en 140 archivos). `holdout_gastado = M19`.
