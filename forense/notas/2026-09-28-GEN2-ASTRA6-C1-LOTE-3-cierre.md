# Nota de cierre · ACTO GEN2-ASTRA6-C1-LOTE-3

**Contadores movidos: cero.** `celdas_validadas` 219 → 219 · `resultados_con_validacion_independiente` 215 → 215. Se asienta un NO-PASA con tolerancia citada.

28/sep/2026 · CAJA · MODO RÍGIDO · modelo Opus 5.5 (`claude-opus-5-5`) en las dos sesiones · base `16ba3d02` (= SHA de redacción), fusionado `origin/main` `48114c5d` antes del cierre · 0-bis `0c1f63e7` · encargo `forense/encargos/2026-09-28-GEN2-ASTRA6-C1-LOTE-3.md` + `-ADENDA-1.md`.

## 0 · Arranque y premisas

- ENTORNO-DERIVADO = CAJA en la receptora y en las cuatro sesiones lanzadas (tres sondas y la reconstructora): corpus montado, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin variable. Sin duplicados del rótulo (rama, worktree, PR).
- **Firmas de §2.** No había ADENDA-1. Se preguntaron a mesa en esta sesión y mesa firmó `26a2-02` (opción A, verbatim) y `26a2-01` (contrato v3 por sha). Eligió además que la receptora lance la reconstructora con `claude -p`. Todo va verbatim en ADENDA-1, sellada al recibirse (`20d95094`). El sha del contrato (`821a5ecb…94eb`) se verificó en el árbol antes de preguntar.
- **[REPORTADO] lote 2 → verificado en el árbol.** 56 = ENBIARE 54 + ENIGH 1 + ENCUCI 1 (`estado_punto = NO-RECALCULABLE-DESDE-SPEC`). 92 = ENDIREH 2016 apartadas. 312 = filas con IC NO-RECALCULABLE, idénticas por diferencia de conjuntos a las llaves de `tabla-llave-componente.tsv` (0 y 0). Las 56 están contenidas en las 312, así que la unión es **404**, no 460.
- **Premisa que cae (logística, no toca qué se mide):** el encargo llama a las 312 «residuales de ENDIREH», pero son ENBIARE 180, ENCODAT 130, ENCUCI 1 y ENIGH 1 (0 filas ENDIREH). Por eso ENDIREH 2021 no se abrió: ninguna de las 404 es ENDIREH 2021. La regla del propio encargo decide: gate ACCESO-AUTORIZADO en NO → `NO-LANZADO (gate)`.
- **[LEÍDO] RECIBO-ASTRA6-3, «2 ERROR en pruebas C1 en su entorno».** En esta caja, la suite v3 da 15/15 OK, incluida la e2e namespace. Los ERROR eran de entorno, no de resultado; no se reparó nada.
- **Lectura declarada de la frase «nunca ve el paquete antes que el reconstructor».** Se aplicó como E.2: la receptora no abrió valores sellados antes de que los números de la reconstructora estuvieran commiteados. La receptora sí armó el paquete, porque «prepara, entrega» (§título), y leyó la spec (`metodo.md`, sin valores) para verificar que el recorte de acceso bastaba.

## 1 · P0/P1 · Paquete y gates

Un solo paquete lanzable: `endireh-pisos-2016-pareja-fisica-0002`, contenedor `c1-ventana-v1` (`6ce9c8a5…a555`, #1203). La receptora le añadió `CONTRATO-v3.md` y los dos miembros autorizados del ZIP ENDIREH 2016 (`TB_SEC_XIII.csv`, `TSDem.csv`), extraídos byte a byte sin parsear. El resto del ZIP no se entregó. El manifiesto de entrada tiene sha canónico `7f467a4a…4a58` y se commiteó en `ba5d2f1a`, antes del lanzamiento. Gates y receta: `forense/validacion-independiente/catalogo-1-lote3/LANZAMIENTO-LOTE3.md`.

**Aislamiento, con control positivo antes del lanzamiento real (tres sondas desechables):**
- Con `--restricted` + settings propios, el repo, el corpus, la red y la memoria quedaron fuera. Pero el `$TMPDIR` compartido `/tmp/claude-1000` seguía legible, con los scratchpads de otras sesiones.
- `CLAUDE_CODE_TMPDIR` no lo cambia.
- La reconstructora corrió en un namespace de montaje propio con `/tmp` en tmpfs vacío. Ahí `/home/pc0` solo mostraba su propio directorio.

## 2 · P2 · Reconstrucción

- **Ejecución.** Sesión nueva, lanzada a las 11:19:20 y terminada a las 11:23:10: 30 turnos, US$1.80, solo Opus. Estimó las 92 llaves con numpy/pandas desde `metodo.md`. `sha256(resultado.json) = 49ac3ff7…7c53`.
- **Archivo con sha.** La salida y el transcript se archivaron con sha y se commitearon en `fe2cf2af` (11:27:39). La exportación se ancló y congeló (`compare_v3 freeze` = `eae56077…d5a7`) en `585a0135` (11:28:50). Solo después se abrió el sellado (referencia construida a las 11:37:13, sha `7ee1f4a7…1124`).
- **Auditoría del transcript.** 0 lecturas fuera del paquete, sin red, campos dentro de `ee49-02`, solo Opus.
- **Nombres.** `diagnostico.json` y `replicas.json` se archivaron con el prefijo `endireh2016-pf-l3--` por T02. Mapa y verificador del sello: `reconstructora/MAPA-NOMBRES.md` y `verifica_sello_reconstructora.py`.

## 3 · P3 · Comparación y asiento

`compare_v3.py` con tolerancia `abs 1e-10, rel 0` (la de `tolerancia.json` del paquete, traducida a v2 y fijada antes de revelar). Resultado: DISCREPA 92/92.
- **Punto.** Dentro 90/92.
- **IC.** Dentro 0/92 en ambos extremos. Mediana de |ΔIC| entre 0.12 y 0.16 SE sellado, máximo 0.42 SE. Razón de anchos 0.88–1.16. El punto sellado cae dentro del IC reconstruido en 92/92. La causa es la que la reconstructora declaró sin conocer la referencia: la spec fija semilla y réplicas, pero no el generador, el orden de extracción ni la interpolación del percentil.
- **Las 2 discrepancias de punto: edad 60+ (#4 vida, #50 reciente).** n sellado 9 480, n reconstruido 9 384. La diferencia, 96, es exactamente el número de casos con EDAD = 98, que la reconstructora declaró antes de comparar (insuficiencias, punto 6). |Δp| = 0.13 y 0.11 SE.
- **Dictamen** (vocabulario ASTRA6-1, `dictamen-lote3.tsv`): SOSTENER 90 · ACOTAR 2 · SOSTENER-SIN-CORROBORACION 312 (NO-LANZADO). «Coinciden» no se escribe en ningún lado: el comparador dice DISCREPA en las 92.
- **Asiento.** Una fila, NO-PASA, rótulo `C1-LOTE3-CIEGA-POR-CONTEXTO-NUEVO`, evidencia `…/comparacion/endireh2016-pf-l3--comparacion.json` con su sha.
- **D-15** → `specs-insuficientes-v1_1.tsv` (v1_0 + 2): EDAD = 98 (ADENDA-DE-SPEC) y la reproducción bit a bit del IC (contrato inferencial, no spec). Las otras diez lecturas de la reconstructora no tuvieron efecto observable (las 90 celdas coinciden) y quedan solo en su `insuficiencias.md`.

## 4 · P4 · Hoja

`forense/validacion-independiente/catalogo-1-lote3/hoja-mesa-lote3.md`: recibo de las dos sesiones, conteos, FP 0c1f-01 (ACOTAR #4/#50 en v1.4 + spec sucesora) y FP 0c1f-02 (acceso y contratos de las 312 para C1-LOTE-4).

## 5 · Incidencias

- `/tmp` de la caja (tmpfs de 12 G) llegó al 100 % durante el acto. Lo llenaban clones temporales ajenos: `/tmp/modelado-deriva-*`, `astra6-c2-clon-limpio`. Hizo fallar la captura de salida de un comando (el commit sí entró). No se borró nada ajeno. Una línea en hallazgos.
- La primera corrida de `check.py --rapido` dio 1 FAIL que no se reprodujo en la siguiente (0 FAIL); no se investigó.

## 6 · Módulo de auditoría (v2.16)

- **¿Cuántos contadores movió?** Cero (arriba).
- **¿PROSPECTIVA o RETROSPECTIVA?** Todo es RETROSPECTIVO: reconstrucción de cifras ya selladas de ENDIREH 2016, un dato que el programa ya había visto. Ninguna frase lo mezcla con una predicción.
- **¿Qué unidad tiene cada cifra?** La mujer de 15 años o más, en entrevista A1/A2 (con pareja), con factor `FAC_MUJ`. La prevalencia es de violencia física de pareja y no se promedia con cifras de hogar ni de evento. «Vida» y «desde octubre de 2015» son dos ventanas del mismo universo, no dos universos.
- **¿En qué escala está cada cantidad y contra qué se compara?** Δ en proporción (0–1), contra la tolerancia 1e-10 y contra el SE sellado. Una Δ de 7.7e-4 son 0.08 puntos porcentuales, 0.13 SE.
- **¿Evidencia débil con intuición fuerte?** «El IC difiere solo por el generador» es una lectura, no una prueba: sin margen de equivalencia firmado, el IC no se adjudica, y por eso no hay PASA.
- **¿Qué sería peligroso leído simplista?** «90 de 92 coinciden» no dice que la violencia de pareja en 2016 esté bien medida. Dice que dos implementaciones independientes de la misma spec dan el mismo número. La validez del estimando (E.2, pregunta 2) no se tocó. Lo mismo vale para «ACOTAR 60+»: no dice que las mayores tengan otra prevalencia, sino que la celda incluye 96 edades no especificadas.
- **¿Qué afirmación sobre el estado del corpus se escribió a mano y no se derivó?** Ninguna. Los conteos 56/92/312/404 salen por diferencia de conjuntos (comando en §0), y el dictamen y el asiento de `asienta_lote3.py`.
- **Foco rural, indígena o popular; sesgo de marco extranjero.** No aplica a una reconstrucción numérica. El eje localidad (U/C/R) se reconstruyó igual que los demás.
