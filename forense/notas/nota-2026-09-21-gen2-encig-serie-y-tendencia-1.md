# ACTO GEN2-ENCIG-SERIE-Y-TENDENCIA-1 · nota de sesión

Encargo: `forense/encargos/2026-09-21-GEN2-ENCIG-SERIE-Y-TENDENCIA-1.md`
(0-bis `852f5f06`, sello de cuerpo `10c4f61f…`). Rama
`acto/gen2-encig-serie-y-tendencia-1`. Base `fc13cdcc` (main se movió 61
commits desde el `55c8d57c` del encargo; re-derivado: el piso, el marcador y
`milpa/tramite.yaml` se leyeron en esa base). Entorno `CAJA` (corpus montado,
420 archivos; `sin_variable`; red 200). `data/raw` enlazada a
`mm-corpus/raw`; `raices.local.yaml` copiada del clon padre.

Contadores al abrir: `celdas_validadas` 73 · `N_corridas_selladas` +0 ·
`cuenta_gen2 = SI` prometido para la serie · no adopta.

## 0 · Premisas verificadas (§3 del encargo)

- `[EJECUTADO]` manifiesto: los seis payloads de microdato y los seis
  cuestionarios están en `data/raw` (14/14 archivos localizados por nombre;
  sha256/16 en la tabla P1). ✔
- `[EXISTE]` `CALC-PISOS-ENCIG2023-EJES-0002` sellado (60 ids `-DIGITAL-`,
  10 celdas × 6); `milpa/tramite.yaml:425-470` trae los once valores 2025
  con IC (firma s1); `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` (PR #961, ya en
  main) trae 9 marginales con casos completos (ALL 0.672905, n 20 088). ✔
- `[EJECUTADO]` `marcador-segmento.tsv`: 57 filas `SOLO-PISO`, 10 de
  `encig2025`, todas de **una** conducta,
  `tramite.gobierno_digital.util_sin_coercion_ejes_encig2025` (sexo 2, edad
  4, escolaridad 4). «Las 10 celdas» son diez marginales de un solo
  reactivo, no diez conductas: P1 es una conducta × seis olas. ✔
- `[REPORTADO]` NC-0355 (`CAMBIO-MENOR` 2021↔2023↔2025) leída en
  `nota-2026-09-20-gen2-celda-d-piloto-3-ejecucion-paro.md §2`; las
  páginas de 7.3 de 2023 y 2025 se re-leyeron aquí. ✔
- `[SUPUESTO]` nivel sube sostenido: es la hipótesis; la decide P3.
- Ya hecho, por objeto («ENCIG» × «serie|tendencia|persistencia») en
  `forense/encargos/`, `forense/prereg-caja/`, `data/corrida0/` y ramas
  remotas: `CALC-ENVIPE-SERIE-*` (15 olas ENVIPE), `CALC-ENCIG202{1,3}-
  CRUCES-HISTORICOS-*` (cruces, un trámite, dos olas),
  `CALC-PISO-PERSISTENCIA-ERROR-0001` (el error que motiva el encargo),
  ninguna serie ENCIG ni origen móvil: **NO-ENCONTRADO**. ✔

## 1 · P1 · Comparabilidad por texto, seis olas

Tabla: `data/encig-canal-comparabilidad-texto-v1_0.tsv` (test
`tests/test_encig_canal_comparabilidad_texto.py`, cableado en `verify.yml`).
Fuentes: cuestionarios 2015/2017/2019/2021 (`pdftotext -layout` y `-raw`,
pdf-págs 10-12) y FD de las cuatro olas; catálogos `p7_3`/`n_tra`/`niv` de
los zip; cuestionarios 2023/2025 pdf-pág 14 re-leídos; NC-0355 para el
resto de 2023/2025.

| ola | veredicto vs 2021 | qué cambia |
|---|---|---|
| 2015 | CAMBIO-MENOR | opción 6 de 7.3 «Oficinas temporales o móviles» (sin «Módulos, clínicas u»); 6.1 sin código 3 «No aplica»; salto a «SECCIÓN IX» por numeración de 2015; base sin `ID_PER` (llave `ENT+UPM+V_SEL+N_HOG` y `R_ELE`=`N_REN`); códigos de catálogo sin cero a la izquierda |
| 2017 | MISMO-INSTRUMENTO | nada en 7.3, 6.1, catálogo 01–22, flujo, unidad, ponderador |
| 2019 | MISMO-INSTRUMENTO | idem (Guardia Nacional entra en sección IV, ajena) |
| 2021 | ancla | — |
| 2023 | CAMBIO-MENOR | NC-0355: «etc.»→«etcétera»; 07/08/17 nombran IMSS-Bienestar/Fiscalía |
| 2025 | CAMBIO-MENOR | NC-0355: código 15 nuevo desplaza 15–22→16–23; voz usted; salto «TRÁMITE 21» |

Reactivo 7.3, sus nueve opciones y códigos 1–9, el filtro `N_TRA` = 01 «el
pago ordinario del servicio de luz?», la regla «PARA LOS TRÁMITES Y PAGOS
DEL 1 AL 7 INDAGA SOBRE EL ÚLTIMO TRÁMITE REALIZADO POR TIPO», la
instrucción «REGISTRA UN SOLO CÓDIGO» y el salto «NO APLICAR … SI EN 7.3 LOS
CÓDIGOS DE RESPUESTA SON 4, 5 Ó 9» son idénticos en 2015–2021. Ningún
cambio entra en el numerador {4,5} ni mueve el denominador {1,2,4,5,6}.
**Seis olas comparables; la serie empieza en 2015. `cambio_instrumento_en_ola
= NINGUNA` para P4.**

Contaminación declarada (ADR-46): esta sesión leyó cuestionarios y FD de
2015–2025 (estructura) y los encabezados de columna de los CSV de las seis
olas (estructura, sin filas); no abrió respuestas antes del COMMIT-1.

## 2 · COMMIT-1 · procedimiento congelado (P2 y P3)

- `forense/prereg-caja/ENCIG-SERIE-CANAL-spec-v1_0.md` sha256
  `c46c0a7cd9d30b309b807d762f9dd2a3d706368bc0b79023240ea6a4f3754287`, con sidecar.
- `tools/encig_serie_canal.py` sha256
  `5911279d73fa4328b9091231c599d7d51f440b14f869b1b9f2ea18f05a6b280a`
  (`script_sha256_congelado` en las cinco specs).
- `data/corrida0/CALC-ENCIG-SERIE-CANAL-{2015,2017,2019,2021,2023}/spec.yaml`:
  71 ids cada una (11 celdas × 6 + 5 diagnósticos); P/IC con
  `permite_no_estimable: true` (soporte vacío); `cuenta_gen2: SI` con la
  firma de §2 del encargo. `spec-check` 10/10 OK (18/18 en 2015);
  `preflight` sólo bloqueado por `working_tree_dirty` antes de este commit.
- `forense/prereg-caja/ENCIG-ORIGEN-MOVIL-spec-v1_0.md` sha256
  `cecb68a89e0837fec3504e415361b451f031bd00e7e04b0a76604f99defb4620`, con
  sidecar; `tools/encig_origen_movil.py` sha256
  `8ddb293d8d580630099317fc820b47c66b1646ba87a12a5812bfae53b9cf0bc1`.
  Reglas del dictamen (§4): «sube sostenida» = ≥4 de 5 pares positivos, sin
  decremento con IC disjuntos, cambio total > 0; «materialmente menos» =
  ΔMAE ≥ 3.0 pp sobre las olas comunes {2021, 2023, 2025}. Su `spec.yaml`
  (`CALC-ENCIG-ORIGEN-MOVIL-0001`) se escribe en COMMIT-2 con los hashes de
  los cinco `resultados.json` sellados y de
  `milpa/tramite-ola5-propuesta-v0.yaml` (`93dfa3f9…`, sin cambios desde
  agosto): identidad de insumos, no procedimiento.
- D-22: `tests/test_encig_serie_canal.py` — 13 pruebas sintéticas
  (ramas: normal con `ID_PER`, 2015 sin `ID_PER`, celda rara sin soporte,
  nacional sin demografía, llave duplicada → PARA; origen móvil: pesos de
  los cuatro pisos, serie logit-lineal → TENDENCIA, plana →
  SALTO-SIN-EXPLICAR, punto nulo, NO-DECIDIBLE, CAMBIO-DE-INSTRUMENTO,
  lectura del YAML 2025) todas con `_valida_outputs` vacío; `test_oro_2023`
  se salta hasta que el CALC 2023 exista. 12 OK · 1 saltada.
- Compuerta §8: «COMMIT-1 en origin con su oro en verde» protege abrir
  dato. Orden: push de este commit → `run` de 2023 (ya abierta por el piso)
  → oro → sólo entonces 2015–2021.

## 3 · COMMIT-2 · la serie (P2)

Compuerta §8 cumplida por producto: COMMIT-1 `d060d222` en `origin` (`git
ls-remote`), `preflight` VERDE, `run` de 2023 (`e574c238`) y
`test_oro_2023` en verde — 61/61 ids (10 celdas × 6 + `N-UNIVERSO`)
coinciden con `CALC-PISOS-ENCIG2023-EJES-0002` a 1e-10 — **antes** de
abrir 2021 (`264e1441`), 2019 (`cfb70cb3`), 2017 (`6f6d24d9`) y 2015
(`c5968d1a`). Cinco corridas selladas, `verify` aislado REPRODUCE/IDENTICO,
asiento en `forense/replay-evidencia.tsv` y vista por `registro --escribe
--verifica --lote` (E.7): `corridas.tsv` +6, `resultados.tsv` +1 075,
`cuenta_gen2 = SI`, `envuelto_legacy = NO` en las cinco de la serie.

| ola | filas sec_7 | universo (N_TRA=01, P7_3∈{1,2,4,5,6}) | excluidas P7_3 | sin demografía | llave |
|---|---|---|---|---|---|
| 2015 | 97 659 | 16 455 | 49 | 0 | ENT+UPM+V_SEL+N_HOG+R_ELE → N_REN |
| 2017 | 119 036 | 20 529 | 937 | 0 | ID_PER |
| 2019 | 116 904 | 20 669 | 209 | 0 | ID_PER |
| 2021 | 106 629 | 21 152 | 130 | 0 | ID_PER |
| 2023 | 123 186 | 20 934 | 122 | 0 | ID_PER |

Proporción de pago de luz por canal digital útil (P7_3 ∈ {4,5}), unidad
trámite, FAC_TRA; 2025 = valor sellado por mesa (`milpa/tramite.yaml`,
firmas a1/s1), el mismo R del marcador:

| celda | 2015 | 2017 | 2019 | 2021 | 2023 | 2025 |
|---|---|---|---|---|---|---|
| nacional | 0.5042 | 0.5213 | 0.5242 | 0.5732 | 0.5604 | 0.6734 |
| hombre | 0.5318 | 0.5536 | 0.5521 | 0.5976 | 0.5780 | 0.6813 |
| mujer | 0.4930 | 0.4908 | 0.4967 | 0.5468 | 0.5413 | 0.6652 |
| 18–29 | 0.5417 | 0.5755 | 0.5413 | 0.6317 | 0.6358 | 0.7518 |
| 30–44 | 0.5352 | 0.5731 | 0.5889 | 0.6279 | 0.6542 | 0.7747 |
| 45–59 | 0.4744 | 0.5134 | 0.5408 | 0.5733 | 0.5356 | 0.6692 |
| 60+ | 0.3873 | 0.3863 | 0.3848 | 0.4245 | 0.3985 | 0.4758 |
| hasta primaria | 0.3859 | 0.3758 | 0.3803 | 0.4043 | 0.3121 | 0.3920 |
| secundaria | 0.4765 | 0.5133 | 0.4825 | 0.4948 | 0.4391 | 0.5646 |
| media superior | 0.5133 | 0.5360 | 0.5261 | 0.5457 | 0.5572 | 0.6786 |
| superior | 0.5911 | 0.6011 | 0.6309 | 0.7050 | 0.7304 | 0.8129 |

Lectura descriptiva (A-bis 1: asociación, no efecto): de 2015 a 2023 el
nacional sube **5.6 pp en ocho años** (50.4 → 56.0), con un escalón en 2021
(+4.9) y un retroceso en 2023 (−1.3, IC traslapados). De 2023 a 2025 sube
**11.3 pp en dos años**. Dos celdas caen en 2023 (hasta primaria −9.2 pp,
secundaria −5.6 pp) y rebotan en 2025; superior sube en cada ola.

## 4 · P3 · Origen móvil (`CALC-ENCIG-ORIGEN-MOVIL-0001`, RETROSPECTIVA-MECÁNICA)

720 ids, `verify` REPRODUCE/IDENTICO, `envuelto_legacy = INDETERMINADO` en
la vista porque uno de sus seis insumos (`milpa/tramite-ola5-propuesta-v0.yaml`,
el 2025) es un YAML de firma de mesa y no un CALC sellado — se declara en
§6. Once celdas × olas objetivo 2017–2025; olas comunes a los cuatro pisos
{2021, 2023, 2025} (33 pares celda × ola).

| piso | MAE común (pp) | cobertura común | MAE nacional común | MAE 2017 | 2019 | 2021 | 2023 | 2025 | ΔMAE vs persistencia | vence a persistencia (de 33) |
|---|---|---|---|---|---|---|---|---|---|---|
| PERSISTENCIA | **6.03** | 6/33 (0.18) | 5.83 | 2.11 | 1.49 | 4.33 | 2.88 | 10.88 | — | — |
| TENDENCIA-2 | 7.49 | 8/33 (0.24) | 7.75 | — | 2.54 | 4.27 | 5.78 | 12.43 | −1.46 | 12 |
| TENDENCIA-3 | 5.07 | 10/33 (0.30) | 5.08 | — | — | 3.15 | 3.36 | 8.70 | +0.96 | 22 |
| TENDENCIA-SERIE | **4.89** | 11/33 (0.33) | 4.90 | — | 2.54 | 3.15 | 2.92 | 8.59 | +1.15 | 25 |

Error nacional por ola (piso − R, pp): persistencia −1.7 (2017), −0.3
(2019, cubre), −4.9 (2021), +1.3 (2023), **−11.3 (2025)**; tendencia-serie
+1.4 (2019, cubre), −3.7, +2.3, **−8.8 (2025)**. En 2025 **ninguno de los
cuatro pisos cubre ninguna de las once celdas**; el mejor (TENDENCIA-3)
yerra 8.5 pp nacional y entre 3.4 (superior) y 13.6 (secundaria) por celda.
El 2025 explica la diferencia entre pisos: sin esa ola, persistencia y
tendencia-serie quedan a 3.6 vs 3.0 pp (2021+2023).

## 5 · P4 · Dictamen: `SALTO-SIN-EXPLICAR`

Con las reglas escritas en la spec antes de ver la serie (§4):

1. **Sube sostenida: SI.** 4 de 5 pares positivos, el negativo (2021→2023,
   −1.3 pp) con IC95 traslapados, cambio total +16.9 pp.
2. **Un piso de tendencia erra materialmente menos: NO.** La mejor
   reducción (TENDENCIA-SERIE) es 1.15 pp sobre las olas comunes, por debajo
   de los 3.0 pp declarados. Tendencia gana en 25/33 pares, pero poco: el
   salto de 2025 (11.3 pp, `SALTO-MAXIMO-OLA = 2025`) es 2× el crecimiento
   acumulado de los ocho años anteriores (5.6 pp) y ninguna recta ajustada
   a 2015–2023 lo alcanza.
3. `olas_comparables = 6 ≥ 3`; `cambio_instrumento_en_ola = NINGUNA` (P1).

**Palabra: `SALTO-SIN-EXPLICAR`.** No es `CAMBIO-DE-INSTRUMENTO`: el texto,
las opciones, el filtro, el flujo y la unidad de 7.3 sobre pago de luz son
los mismos en las seis olas (P1). No es `TENDENCIA`: la serie sube, pero
extrapolarla habría fallado casi tanto como repetir el último valor. El
0 de 10 del marcador no se debe al instrumento ni a haber elegido
persistencia en vez de tendencia: se debe a que 2023→2025 es un salto de
una sola ola, sin precedente en la serie.

**Lectura (b) del encargo, tal como se enunció, cae**: «el nivel sube de
forma sostenida ola tras ola» es cierto en signo (4/5) pero no en magnitud;
lo que sube sostenido (≈0.7 pp/año) no es lo que se midió en 2025 (≈5.6
pp/año).

### Propuesta para mesa (no cambia nada adjudicado)

- **Piso en marginales de conductas con pendiente:** no adjudicar hoy un
  piso de tendencia en ENCIG; la evidencia retrospectiva no lo justifica
  (ΔMAE +1.15 pp < 3 pp; en 2025 tampoco cubre). Si mesa quiere un piso de
  tendencia como *retador* en el duelo ENVIPE 2026 (prospectivo, donde sí
  hay 15 olas), la variante con mejor origen móvil aquí es
  **TENDENCIA-SERIE** (mínimos cuadrados en logit sobre toda la serie
  previa), sin parámetros; entra como candidato, no como piso.
- **Regla propuesta para decir que una conducta «tiene pendiente»:** con
  ≥ 4 olas comparables por texto, (i) ≥ 3/4 de los pares consecutivos con
  el mismo signo en logit, (ii) ningún par contrario con IC95 disjuntos, y
  (iii) origen móvil sobre las olas ya vistas donde TENDENCIA-SERIE reduzca
  el MAE de persistencia en ≥ 3 pp. ENCIG pago de luz cumple (i) y (ii) y
  no (iii): **no tiene pendiente adjudicable**.
- **Sucesor útil**: explicar el salto 2023→2025 exige otra variable, no
  otro piso — oferta de canal (CFE app/portal, bancos con pago en línea),
  no disposición. Fuera de este acto.

## 6 · Reservas y hallazgos

- El punto 2025 entra desde `milpa/tramite-ola5-propuesta-v0.yaml` (firma de
  mesa, MAESTRA34-L5/MAESTRA35-N4, época GEN1 con receta congelada), no
  desde un CALC GEN2: por eso la vista marca `envuelto_legacy =
  INDETERMINADO` en `CALC-ENCIG-ORIGEN-MOVIL-0001`. El único 2025 GEN2
  sellado (`CALC-GOB-DIGITAL-EXE-EMISIONES-0002`) usa casos completos en
  edad × escolaridad (n 20 088 vs 20 203) y no trae sexo; sus nueve
  marginales difieren de los de milpa en ≤ 0.3 pp y el dictamen no cambia
  con ninguno de los dos (el salto es de 11 pp). Un CALC GEN2 de 2025 por
  una variable (sexo) que cierre esta reserva es sucesor
  (`NC-260921-…-852f-01`).
- 2017 tiene 937 trámites de luz con P7_3 fuera del universo (4.4 %),
  contra 49–209 en las otras olas. El desglose por código (3/7/8/9/blanco)
  no se derivó: la spec sólo promete el conteo. No se convierten en no
  adopción; una sensibilidad que los reasigne no se corrió (reserva
  declarada, sin fila NC porque la spec no la prometió).
- Ninguna celda salió sin soporte; los `permite_no_estimable` no se
  ejercieron en dato real (sí en sintético).

## 7 · Auditoría (afirma sobre México)

Contadores que movió este trabajo: `N_corridas_selladas` +6 (121 → 127),
`cuenta_gen2 = SI` en las seis; `celdas_validadas` 73 → 73 (no adopta, no
re-adjudica); `adoptados_activos` sin cambio. Que el pago digital de luz
suba no es «cambio cultural»: bancarización, cobertura de internet, la
pandemia y la oferta de canales de CFE y gobiernos lo explican antes que
una disposición, y el salto de 2025 en particular pide una explicación de
oferta que este acto no midió. Unidad trámite, no persona: quien paga más
veces pesa más, y eso sesga hacia hogares con servicio a su nombre y a
quien paga en persona cada bimestre. El promedio esconde edad y
escolaridad: en 2025 la brecha entre superior (0.81) y hasta primaria
(0.39) es de 42 pp, y el salto 2023→2025 es mayor donde el nivel era más
bajo (secundaria +12.6, hasta primaria +8.0) — compatible con difusión
tardía, no con un rasgo. ENCIG cubre ciudades de 100 mil habitantes o más:
nada de esto habla del México rural.
