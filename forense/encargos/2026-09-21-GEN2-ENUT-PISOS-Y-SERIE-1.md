# ENCARGO · ACTO GEN2-ENUT-PISOS-Y-SERIE-1 · EL DOMINIO CUIDADO Y USO DEL TIEMPO DEJA DE ESTAR SIN PISO: SE SABE QUÉ OLAS DE ENUT SON COMPARABLES, SE SELLAN SUS PISOS Y LA PERSISTENCIA SE CALIFICA CONTRA ENUT 2024

> ENTORNO: **CAJA** (corpus montado: abre microdato de ENUT 2009–2024). Si el hook no dice CAJA, PARA en una línea. NO es NUBE.

CABECERA · SHA de redacción `fc13cdcc`; re-deriva al abrir · una sola sesión, rama `acto/gen2-enut-pisos-y-serie-1` · MODELO: Opus (mide) · MODO: **ABIERTO** hasta cada COMMIT-1; desde ahí RÍGIDO · CONTADOR: sella corridas; `cuenta_gen2 = SI` (§2); no adopta; filas `SIN-PISO` del marcador, antes y después · FP/ADR/NC: raíz de acto.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación.** Si `canon/L0/` ya existe al cerrar, tu anotación va ahí.
**NO CHOCAR CON TUBERÍA (acto en vuelo):** no edites `.github/workflows/verify.yml`, `tests/check.py`, `.gitattributes`, `.claude/commands/*.md`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `tools/estado_comun.py` ni `tools/digesto_tramite.py`. Tu test nuevo **no** se cablea a mano: el job de guardias lo ejecuta como huérfano (`tools/ci_guardias.py --ejecuta-huerfanos`) `[EJECUTADO por dirección: 56 ejecutados]`. Si tu cierre exige tocar uno de esos archivos, déjalo en NC con sucesor y dilo.

## 1 · OBJETIVO
El programa tiene celdas validadas en tres dominios —dinero (ENIF), trato con la norma (ENVIPE), gobierno digital (ENCIG)— y **ninguna** en familia y cuidado, que es donde viven las afirmaciones más cargadas sobre México (quién cuida, cuántas horas, con qué reparto). En el marcador, ENUT 2024 tiene 11 celdas `SIN-PISO` y 10 `IDENTICO` `[EJECUTADO sobre marcador-segmento.tsv]`: no hay pronóstico sellado contra el cual calificar nada. El manifiesto trae ENUT 2002, 2009, 2014, 2019 y 2024. Este acto le da piso al dominio y, de paso, su primera serie.
«Hecho» significa: comparabilidad por texto de las conductas de esas 21 celdas entre olas · pisos sellados de ENUT 2019 por eje · R de ENUT 2024 por eje, medida por **una sola variable** · persistencia calificada (error y cobertura del IC del piso) · serie de lo comparable y validación de origen móvil · nota por conducta.

## 2 · FIRMAS DE MESA — verbatim
Piso adjudicado (17/sep): «Un piso no vencido es el estimador adjudicado de su celda y se adopta salvo veto de mesa. Pisos: […] en marginales, la ola anterior por eje.» Reserva viva: el cruce `reparto_hogar × sexo_edad` de ENUT 2024 está `RESERVADA` en el marcador. 3D, segunda mitad (21/sep): «cuando no existe módulo guardián para una ola reservada, la guardia de una sola variable puede vivir en el medidor, con la misma semántica que el guardián, auditoría automática del código antes de abrir el dato, y prueba por mutación». D-22 ampliada (21/sep): «Congelado exige: `preflight` VERDE sobre el commit final con main fusionado; que `_valida_outputs` acepte la salida de cada rama terminal del procedimiento, incluida la de celda rara, sobre sintético y sobre oro; que todo id que el código pueda emitir nulo por lectura estática esté declarado; y ningún input con hash sobre un archivo vivo.»
**Propuesta de dirección — el lanzamiento es el sello:** «Las corridas de GEN2-ENUT-PISOS-Y-SERIE-1 cuentan (`cuenta_gen2 = SI`), sea cual sea el error que le encuentren a la persistencia. La validación de origen móvil se rotula RETROSPECTIVA-MECÁNICA y sus variantes entran todas o ninguna.»

## 3 · LO QUE DIRECCIÓN SABE (contra `fc13cdcc`, sin corpus)
- `[EJECUTADO sobre el manifiesto]` `enut2002_bd_dbf`, `enut2009_bd_dbf`, `enut2014_bd_dbf`, `enut2019_bd_csv` (+ `enut2019_der_zip`), con descriptores o diccionarios de cada ola. De ENUT 2024 busca tú el id (el marcador cita `tvar_crea.csv`).
- `[EXISTE]` `forense/prereg-caja/PISOS-ENUT2019-ejes-metadatos-v1_0.tsv` (con `.sha256`): **alguien empezó los pisos de ENUT 2019 y no hay CALC sellado con ese nombre** `[EJECUTADO: ls data/corrida0]`. Averigua qué acto lo dejó y por qué paró (A.17) antes de rehacerlo. También: `ENUT-CUIDADO-spec-v1_0.md`, `ENUT2024-DISTRIBUCION-HORAS-spec-v1_0.md`, `ENUT2024-PARTICIPACION-INTENSIDAD-spec-v1_0.md`; sellados `CALC-ENUT-0001`, `CALC-ENUT2024-DISTRIBUCION-HORAS-0002`, `CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001`.
- `[LEÍDO: C2-COMPUESTO-RESERVADAS-spec-v1_0.md, tras :132]` en ENUT, `reparto_hogar` es un estimador de **razón** sobre hogares (`FAC_HOG`) y `sexo_edad` una **media**: no son proporciones. La escala se declara por conducta y ninguna se compara contra otra sin enlace (A-bis).
- `[EXISTE]` el molde: `CALC-PISOS-ENIF2021-EJES-0003`, `CALC-PISOS-ENVIPE2024-EJES-0002`, `CALC-PISOS-ENCIG2023-EJES-0002` y sus specs `PISOS-*-ejes-spec-v2_*.md`.
- `[EJECUTADO]` FP-409 está ABIERTA: pregunta si la corrección de `CALC-ENUT2024-DISTRIBUCION-HORAS-0002` pudo depender de haber visto el resultado. No la dictamines; **no uses ese CALC como oro** sin decirlo.

## 4 · YA HECHO
Por objeto («ENUT», «cuidado», «PISOS-ENUT») en encargos, `prereg-caja`, `data/corrida0/` y las 8 ramas remotas vivas: hay mediciones de ENUT 2024 y metadatos de pisos 2019 sin corrida; no hay comparabilidad entre olas ni serie. **Repítela tú.**

## 5 · PIEZAS
**P1 · Comparabilidad por texto** de las conductas de las 21 celdas en 2009, 2014, 2019 y 2024: reactivo, texto, periodo de referencia (semana pasada / día), unidad (persona, hogar, hora), población base, lista de actividades que componen «cuidado» y «trabajo doméstico», ponderador y diseño. Forma de `data/credito-comparabilidad-texto-v1_0.tsv`. ENUT cambió su clasificación de actividades entre levantamientos: es el riesgo central; se busca por texto (A.15).
**P2 · Pisos ENUT 2019 por eje.** COMMIT-1 (spec con sidecar, rejilla de ejes **la de la casa** —sexo, edad, escolaridad, localidad—, `spec.yaml`, medidor; «congelado» es D-22 ampliada con su oro: reproduce un sellado existente de ENUT que no sea el de FP-409) → COMMIT-2 (`corrida0 run`).
**P3 · R de ENUT 2024 por eje**, mismo procedimiento apuntado a 2024, con guardia de una sola variable en el medidor y prueba por mutación (3D). Mismos dos commits.
**P4 · Calificación y serie.** Persistencia 2019→2024: error por celda en la escala de cada conducta, cobertura del IC del piso con intervalo binomial. Serie 2009–2019 de lo comparable y origen móvil de persistencia y tendencias (2 olas, 3 olas, serie), todas juntas. Dictamen por conducta con una palabra: `PERSISTE` · `TENDENCIA` · `CAMBIO-DE-INSTRUMENTO` · `NO-DECIDIBLE`.

## 6 · LATITUD
Decides tú: estructura de CALC, qué reutilizas, orden. `NO-CONSTRUIBLE` cita texto buscado y secciones recorridas. Pregunta a mesa, siguiendo: si «cuidado» no es construible igual en 2019 y 2024.

## 7 · PAROS — lista cerrada
a) agrupar ENUT 2024 por **dos** variables · b) comparar una razón contra una proporción, o promediar escalas distintas · c) elegir variante de tendencia tras ver el origen móvil · d) cambiar procedimiento tras su COMMIT-1 · e) `corrida0 run` no sella → no se parcha · f) adoptar · g) entorno equivocado.

## 8 · COMPUERTAS
«COMMIT-1 de la pieza en `origin` con su oro en verde» protege: **abrir dato**.

## 9 · PERÍMETRO
Propio: tabla de comparabilidad de ENUT y su test · CALC nuevos y specs · filas propias de vista y replay · marcador por comando · nota · cascada. Ajeno: sellos existentes · celdas-D · `milpa/` · la lista de TUBERÍA. Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · NO HACE · SUCESORES · AUDITORÍA · CIERRE
No abre el cruce reservado · no dictamina FP-409. Sucesor: lote de cruces de ENUT con el módulo genérico. Auditoría (afirma sobre México): que las mujeres carguen más horas de cuidado es estructura —oferta de guarderías, mercado laboral, composición del hogar— además de norma; el acto reporta niveles y persistencia, no causa; «familismo» y «marianismo» son en buena parte evidencia (b), de diáspora: no se invocan para explicar un marginal; horas autoreportadas: sesgo de recuerdo distinto por sexo, se declara; rural e indígena difuso: localidad es el único eje que lo asoma. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.
