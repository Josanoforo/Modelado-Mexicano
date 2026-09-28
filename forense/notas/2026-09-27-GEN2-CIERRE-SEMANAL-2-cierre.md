# GEN2-CIERRE-SEMANAL-2 · nota de cierre (27/sep/2026)

`ADR-260927-GEN2-CIERRE-SEMANAL-2-facd-01` · encargo `forense/encargos/2026-09-27-GEN2-CIERRE-SEMANAL-2.md` (SHA de redacción `5f708a47`; base al 0-bis `9536e5e2` = `origin/main`, 0 detrás) · sha256 del adjunto `394def59…29cf` verificado contra su sidecar · NUBE (hook: `ENTORNO-DERIVADO = NUBE`, corpus montado=NO, examinados=0, red DENEGADA-POR-POLITICA) · MODO AUTÓNOMO-AMPLIO · un PR, rama `claude/new-session-qubfoa`. Este acto **es** `GEN2-CATALOGO-V1-3-1`, el sucesor que nombran `NC-…-96f9-03`, la columna `gatea` de `beee-02` y los `EJECUTA:` de FIRMAS-20.

**Contadores (primera línea del módulo de auditoría):** cero mediciones. Un contador de `status` se mueve, con autorización de firma: `N_resultados_gen2_vetados_por_decision` pasa de 4 a 813 <!-- comando: python3 forense/analisis/informe-v1_5/cifra_v1_5.py vetados_eic -->, porque se asentó el veto de Intercensal 2015 (FIRMAS-20 A6). Ningún otro valor de `status` cambió: `diff` entre `status` antes y después = una línea. `celdas_validadas` queda en 219 (Δ0).

## Qué se entregó

| pieza | archivo | derivación | test |
|---|---|---|---|
| P1 catálogo v1.3 | `canon/catalogo-del-mexicano-v1_3.{md,tsv}` | `python3 forense/analisis/catalogo/genera_catalogo_v1_3.py [--sin-registro]` | `tests/test_catalogo_v1_3.py` |
| P2 tabla de piso v1.2 | `canon/tabla-de-piso-v1_2.tsv` | `python3 tools/genera_tabla_piso_v1_2.py --escribe` | `tests/test_catalogo_v1_3.py` (mismas filas y rótulos) |
| P3 informe v1.5 | `canon/informe-programa-v1_5.md` | `forense/analisis/informe-v1_5/cifra_v1_5.py <clave>` + `corrida0 status` | `tests/test_informe_derivado.py` (toma el más nuevo) |
| P4 estado v1.18 | `canon/estado-programa-v1_18.md` | comandos en §18 | `tests/test_estado_derivado.py` (toma el más nuevo) |
| P5 receta + punteros | esta nota §P5; `docs/{catalogo,reto,one-pager,estado,informe,guia-lectura-publica,ejemplos}.md`, `docs/data/catalogo-v1_3.json` | `tools/deriva_cifras.py --escribe`, `tools/benchmark.py exporta/ejemplos` | `tests/test_frente_publico_2.py` |

Asientos: `beee-01` y `beee-02` quedan FIRMADA con el verbatim «Firmo Beee, las dos». `f2e5-17` queda CERRADA, `YA-CUBIERTA-POR` beee-02. Se escriben 809 filas `adopcion=VETADA-POR-DECISION` en `data/corrida0/decisiones.tsv` y se cierran `NC-…-96f9-03` y `NC-…-dea2-02`.

## Premisas y discrepancias (cláusula de autonomía, puntos 1, 2 y 4)

- **[EJECUTADO] 3 371 filas y el reparto por `recomendacion`.** Se re-derivaron con lector CSV y se sostienen: SOSTENER 1 876, SOSTENER-SIN-CORROBORACION 799, ACOTAR 689 (679 con `efecto=cifra` y 10 con `efecto=alcance`), PROPONER-SUSPENDER 7. Las 3 371 llaves del recibo están todas en el catálogo v1.3 (el generador falla si falta una). El test comprueba que el conjunto suspendido y el acotado son exactamente los del recibo.
- **Dónde vive la suspensión (latitud §6).** Solo en el catálogo y la tabla de piso: `estado_adopcion = SUSPENDIDA-POR-FIRMA`, `validacion_ciega` y `sucesor`. **`status` no puede verla**, y se declara. Las 7 son celdas `#i` dentro de un único RESULT, `RESULT-ENDIREH2011-MOD-TABLA`. `status` veta por id de RESULT (`tools/corrida0.py:5335`), así que asentar la suspensión en `decisiones.tsv` vetaría la tabla entera, y eso incluye cientos de celdas que el recibo sostiene. No se hizo.
- **Rótulos de las 689 (latitud §6).** `ACOTADA:DELTA-PUNTO-EN-VALIDACION-CIEGA` (679, con su `delta_punto` en la fila) y `ACOTADA:PUBLICABILIDAD-FRAGIL-AL-RNG` (10, con margen y banda). Salen de la columna `efecto` de la tabla del recibo. No se usó la cota «≤ 5 pp» como rótulo porque no es una columna de esa tabla.
- **Sucesor de las 7.** Se nombra por llave, `<CALC-ENDIREH-PISOS-2011-MODULOS-sucesor>` (D-24): hoy existe un solo CALC con ese prefijo <!-- comando: ls data/corrida0 | grep -c ENDIREH-PISOS-2011-MODULOS -->, y no se abre ni se acuña número aquí.
- **VETO de Intercensal 2015.** Se escriben 809 filas, una por RESULT que el registro ve de `CALC-EIC-HOGARES-2015-0001`. Son los 160 puntos más sus IC, EE, N y diagnósticos: la firma veta el CALC, no una celda. El sello queda intacto. INTERPRETACIÓN-DECLARADA: vetar todos los RESULT del CALC, y no solo los puntos, es lo que hace que `status` no lo cuente como «pendiente de adopción».
- **«Una FP de adopción que siga ABIERTA no entra y se lista».** Al abrir, las 6 FP de FIRMAS-20 A1–A6 ya estaban FIRMADA. El generador busca en el TSV de firmas toda `ADOPCION POR INSTRUMENTO` FIRMADA sin sección propia y la lista como pendiente: salen 0.
- **Premisa de logística caída: `dea2-01`.** Ya estaba CERRADA: la cerró FIRMAS-20 (`PR #1190`). No se tocó.
- **«26 de 31 dominios con medición» del transfer [REPORTADO]: no se reproduce.** El mapa v1.1 tiene 28 dominios, y 17 tienen estimador en el catálogo v1.3 <!-- comando: python3 forense/analisis/informe-v1_5/cifra_v1_5.py mapa11_dominios_medidos && python3 forense/analisis/informe-v1_5/cifra_v1_5.py mapa11_dominios -->. Por report, son 19 de 31 <!-- comando: python3 forense/analisis/informe-v1_5/cifra_v1_5.py cat:reports_medidos -->. El informe cita lo derivado y dice que el transfer no se reproduce.
- **«adoptados 128 sobre el árbol del `[deriva]`» [EJECUTADO por dirección sobre otra rama].** Sobre el commit final `status` da 81, y es lo que el informe cita, con la fecha de la última vista publicada en `main`, 24/sep <!-- comando: python3 forense/analisis/informe-v1_5/cifra_v1_5.py vista_fecha -->. Leída en una rama sin fusionar, la cifra es de tipo (3) (§2) y no se cita como hecho.
- **Estado v1.17 contra «`diff` vacío».** `T01` admite una sola versión viva de `estado-programa`. Se siguió el precedente firmado de v1.12–v1.17: `git mv` a v1.18, que la hereda **verbatim** y le añade cabecera nueva y §18. Los punteros van a `v1_18`: `RUTA_ESTADO_PROGRAMA` y las dos listas de exención de `tests/check.py`, `tools/cierre_acto.py`, `tests/test_cierre_acto.py`, `tests/test_tuberia_ids_union.py`, `forense/analisis/informe-v1_3/censo_evaluaciones.py`, `.claude/commands/{acto,revisa}.md` y `docs/`. INTERPRETACIÓN-DECLARADA: retirar no es editar. Catálogo v1.2, informe v1.4 y tabla de piso v1.1 quedan con diff vacío.
- **Dominio de los CALC nuevos (PROPUESTO-POR-EJECUTOR).** ENSU y ENVIPE 2024 van a `VIOLENCIA`. EMAT va a `PAREJA`, EDR a `SALUD_MENTAL` y ENPECYT a `CONOCIMIENTO`. MMSI y ENASEM van a `MOVILIDAD`. CCPV y ENADID 2018 van a `FAMILIA_CUIDADOS`, Latinobarómetro COLA a `POLITICA` y PEW 2024 a `RELIGIOSIDAD`. ENDISEG va a `GENERO`, pero en la tabla de piso lleva área propia («Diversidad sexual y de género»), para no aparecer como «violencia contra las mujeres».
- **Marca regional de la tabla de piso.** El eje `ENT` (ENSU, CCPV, EDR, EMAT) cuenta como `REGION`, igual que `ENTIDAD`. Es un cambio de una línea en el generador nuevo; el v1.1 queda intacto.
- **Defectos adyacentes (D-21):**
  - El clon era superficial, y los comandos `git log --merges` heredados del informe y del estado no reproducían. Se corrió `git fetch --unshallow`, el mismo remedio que el precedente.
  - `pytest` no está instalado en el entorno. Los tests son `unittest` y se corrieron con `python3 -m unittest`.
- **Lo que v1.2 prometió para v1.3 y no entra:** la desagregación por celda de las tablas ENIGH de Firma M. Va como NC, con sucesor v1.4.

## Receta de release para mesa (P5)

La serie de tags no ha empezado: `origin` no tiene ningún tag <!-- comando: git ls-remote --tags origin | wc -l -->. `v2026.09.2`, la receta de CIERRE-SEMANAL-1, no se publicó. Esta receta es su sucesora y la reemplaza. Si mesa publica ya, el primer tag de la serie es este.

- **Tag:** `v2026.09.3`
- **Título:** Benchmark del Mexicano — catálogo v1.3, informe v1.5, estado v1.18 (cierre del 22–27/sep)
- **Dos líneas derivadas:**
  1. Catálogo del mexicano v1.3: 63 706 estimadores, cada uno con su firma de mesa citada por id <!-- comando: python3 forense/analisis/informe-v1_5/cifra_v1_5.py cat:estimadores -->. De ellos, 7 están suspendidos por la validación ciega, conservados y rotulados <!-- comando: python3 forense/analisis/informe-v1_5/cifra_v1_5.py cat_estado:SUSPENDIDA-POR-FIRMA -->. Cubre 17 de los 28 dominios del mapa <!-- comando: python3 forense/analisis/informe-v1_5/cifra_v1_5.py mapa11_dominios_medidos -->. Todo es retrospectivo.
  2. 219 celdas validadas (20 prospectivas, reportadas aparte) sobre 300 corridas selladas <!-- comando: python3 tools/corrida0.py status | grep -E "^(celdas_validadas|celdas_validadas_prospectiva|N_corridas_selladas)=" -->. Primer lote de validación ciega: 3 371 identidades rotuladas <!-- comando: python3 forense/analisis/informe-v1_5/cifra_v1_5.py cat:vc:filas -->.
- **Qué sube a Zenodo:** el tag completo. Mesa activa la integración GitHub → Zenodo y decide el DOI; la FP del DOI es `FP-260923-GEN2-FRONT-1-4296-01`. `CITATION.cff` va sin cambios.
- Este acto **no publica en Zenodo ni crea el tag**.

## Módulo de auditoría de rigor extremo

- **¿Cuántos contadores movió este trabajo?** Uno de `status`, `vetados_por_decision` (4 → 813), por firma. Además se mueven los del catálogo, porque se ejecutan adopciones firmadas.
- **¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA? ¿Se mezclan?** No se mezclan. Catálogo, tabla de piso y validación ciega son RETROSPECTIVOS. El informe §F pone las prospectivas en su propia columna.
- **¿Qué unidad tiene cada cifra?** Está en la columna `unidad` de cada fila: persona, hogar, matrimonio o contrayente, defunción, delito o trámite. La validación ciega cuenta mujeres. Nada se promedia entre unidades.
- **¿Pobreza, violencia o informalidad confundidas con cultura?** EDR es composición de defunciones registradas, no tasa ni rasgo. EMAT es inscripción civil, no unión. ENSU es percepción urbana.
- **¿Sobregeneralización desde clase media urbana?** Los universos de ENSU y ENPECYT son urbanos, y así lo dicen las filas.
- **¿Qué afirmación sobre el corpus se escribió a mano?** Ninguna cifra: cada una sale de un comando o de la plantilla con test. «26 de 31» y «128» no se copiaron.
- **¿Qué sería peligroso leído simplista?** Leer «63 706» como hallazgos independientes. Casi todas son celdas de trimestre × eje × segmento (ENOE y ENSU).

## Suite

`python3 tests/check.py --rapido` y los tests propios y heredados que tocan los cuatro documentos se corrieron localmente; el resultado va en el cuerpo del PR. `check.py --baseline` completo lo juzga el CI.
