# K8 · DESTINO DEL CRÉDITO FUERA DE ENIF · ENFIH 2019 (nómina y personal) · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-DIN-CREDITO-HISTORIA-1 (21/sep/2026, CAJA), pieza P3. CALC
reservado: `CALC-DIN-CREDITO-K8-ENFIH2019-0001`. Encargo archivado por A.3 en
`forense/encargos/2026-09-21-GEN2-DIN-CREDITO-HISTORIA-1.md` (sello de cuerpo
`a66577f187bb778a75a7acdbad9cbf00227a5ff6679044ab1dc78ed5428f428b`). Firma de
mesa FP-404 (1): «K8 sale de la serie ENIF […] se triangula en ENSAFI 2023 /
ENFIH 2019 en acto propio; no se construye serie 2012-2018». Compuerta única
(protege: abrir dato): esta spec, `spec.yaml` y `medidor.py` congelados en el
COMMIT-1 con sidecar y sintético corrido, antes de abrir `TNOMINA.csv` o
`TPERSONAL.csv`.

## 0 · Primero por texto (encargo §5 P3) — `data/credito-k8-triangulacion-texto-v1_0.tsv`

¿Preguntan lo mismo, a la misma unidad, con el mismo periodo de referencia?

- **ENSAFI 2023: `NO-ESTIMABLE`.** El cuestionario completo (24 páginas) y el
  FD (4 hojas, 1 284 filas) no traen ninguna pregunta de destino de crédito:
  «destin» 0, «para qué» 0, «último crédito» 0; los dos «utilizó» son medios
  para cubrir gastos del último mes (6.10). Tiene tenencia (6.5/6.6 con el
  texto de 6.1/6.2 de ENIF 2021), atraso y nivel de endeudamiento: otro
  objeto. **Nada de ENSAFI se lee en esta corrida.**
- **ENFIH 2019: `CAMBIO-DE-INSTRUMENTO`** frente a la definición de mesa.
  Pregunta el destino **principal** (un código) de **cada** crédito de nómina
  (8.31, `P8_31`, TNomina) y de **cada** crédito personal (8.47, `P8_47`,
  TPersonal) vigentes: unidad crédito (PR) y respuesta única, pero no «el
  último crédito», sólo dos familias (sin tarjetas, automotriz, vivienda,
  educativo, grupal) y **sin «negocio» en el catálogo** (el código 4 lo
  excluye: «Pagar una deuda (diferente a negocio)»). No hay cuestionario de
  ENFIH en el manifiesto: el texto es el del FD.
- **No son comparables entre sí** (ENSAFI no tiene el reactivo): se mide
  **sólo ENFIH, por separado, rotulado**, y **no se presenta como serie** con
  ENIF ni con ENSAFI (PARO d). El medidor PARA si la tabla dijera otra cosa.

## 1 · Exposición declarada (ADR-46)

- Leídos antes de congelar: cuestionario ENSAFI 2023 completo; FD ENSAFI 2023
  (TMODULO); FD ENFIH 2019 completo (16 hojas); **cabeceras** de
  `TNOMINA.csv`, `TPERSONAL.csv`, `TMODULO.csv`, `TSDEM.csv` (nombres de
  columna, entrecomillados; cero registros). NO abierto: ningún registro de
  ENFIH 2019 ni de ENSAFI 2023.
- Sintético de D-22: `tests/test_din_credito_k8_enfih2019.py::payload_sintetico`
  (cabecera entrecomillada, `default_rng(11)`), sin parecido con el dato.
- Cifra esperada: ninguna.

## 2 · Estimando, unidad y desenlaces

Proporción ponderada de créditos vigentes de nómina y personales (ENFIH 2019)
cuyo destino principal es cada categoría, con IC95 bootstrap; **unidad PR =
crédito** (una fila por crédito; las llaves `FOLIO, VIV_SEL, HOGAR, N_REN`
identifican a la persona seleccionada y `CONSEC` al crédito). Códigos de
`P8_31`/`P8_47` (mismo catálogo, FD TNomina filas 50-58 y TPersonal 48-56):

| destino emitido | códigos = 1 | lista de mesa |
|---|---|---|
| `CONSUMO` | 3 gastos de comida, personales o pago de servicios | consumo |
| `EMERGENCIA` | 5 atender una emergencia o imprevistos | emergencia |
| `EMERGENCIA-MAS-SALUD` | 5 + 6 gastos de salud | emergencia (rotulada aparte) |
| `REFINANCIAR-DEUDA` | 4 pagar una deuda (diferente a negocio) | refinanciar deuda |
| `LISTA-DE-MESA-ALGUNO` | 3, 4, 5 | unión (sin negocio) |
| `VIVIENDA` · `VEHICULO` · `SALUD` · `EDUCACION` · `OTRO` | 1 · 2 · 6 · 7 · 8 | fuera de la lista |

Ceros: los demás códigos 1..8. **`9` No sabe y blanco → indefinido**, contado,
fuera del denominador. **`NEGOCIO`: NO-ESTIMABLE**, se emite como texto, no
como cero. Celdas: `NACIONAL-TODOS`, `FAMILIA-NOMINA`, `FAMILIA-PERSONAL`
(3 × 10 destinos = 30 celdas × `-P -IC-LO -IC-HI -N -DEN-W -B-VALIDAS
-SOPORTE`). Sin ejes sociodemográficos: el encargo pide K8 triangulada y su
comparabilidad, no un piso por ejes.

## 3 · Procedimiento congelado y guardias

- Lectura: ZIP `enfih2019_bd_csv_zip` (sha256 `be372533d5043920…`), miembros
  `TNOMINA.csv` y `TPERSONAL.csv`, `dtype=str`, cabecera entrecomillada
  normalizada. PARA si la llave persona × `CONSEC` se duplica.
- Marco: `FACTOR` de la tabla del crédito (> 0; es el factor de la persona
  seleccionada replicado por crédito, FD TNomina fila 65 / TPersonal 63);
  diseño `EDIS × UPM_DIS` no vacíos; bootstrap de UPM con reemplazo dentro
  de estrato, **10 000 réplicas, `numpy.PCG64(42)`**, IC percentil 2.5/97.5,
  **un solo plan** (una llamada a `_estimate`, importado por bytes del
  medidor sellado de -0003) para los 10 destinos y las 3 celdas.
- Guardia 1 · Comparabilidad: la tabla declara ENFIH `CAMBIO-DE-INSTRUMENTO`
  con `P8_31`/`P8_47`, unidad PR y «negocio» NO-ESTIMABLE, y ENSAFI
  `NO-ESTIMABLE`; si no, PARA. Guardia 2 · Soporte `n < 200`. Guardia 3 ·
  Coherencia nacional = nómina + personal (num y den, `1e-6 × den_w`), si no
  PARA. Guardia 4 · Unidad `PR` emitida por destino.
- Ejecución diagnóstica sobre microdato: **ninguna**; el medidor corrió sólo
  sobre el sintético (120 réplicas) antes de congelarse.

## 4 · Diagnóstico

`FILAS-NOMINA`, `FILAS-PERSONAL`, `FILAS-CREDITOS`, `PERSONAS-CON-CREDITO-N`,
`NO-SABE-N`, `BLANCO-O-FUERA-DE-CATALOGO-N`, `SIN-DISENO-N`, `UPM-EN-PLAN`;
por destino `-N-UNIVERSO`, `-CODIGOS-1`, `-COHERENCIA-FAMILIA-DELTA-*`;
textos `VEREDICTO-TEXTO`, `MATIZ`, `NEGOCIO`, `ENSAFI2023`, `SERIE`.

## 5 · Lo que esta spec no hace

No presenta serie alguna (PARO d); no lee ENSAFI; no lee tarjetas, automotriz,
vivienda, educativo ni grupal de ENFIH (sin destino); no lee 8.7 (destino de
préstamos informales, unidad P multirrespuesta: EXISTE-NO-SATISFACE, queda
declarado en la tabla); no cruza por ejes; no compara con ENIF 2012-2018
(unidad P multirrespuesta) sin función de enlace (A-bis 3); no adopta
(`cuenta_gen2 = SI`, cuenta y no adopta).
