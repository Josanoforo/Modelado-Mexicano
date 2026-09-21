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
