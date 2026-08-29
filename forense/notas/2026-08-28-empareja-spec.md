# Especificación congelada · MAESTRA32-E2 · EMPAREJA-MOTOR-TEXTO

COMMIT-1 del acto (`forense/encargos/2026-08-28-MAESTRA32-E2-EMPAREJA-MOTOR-TEXTO.md`). Escrita **antes** de correr ninguna búsqueda de término contra `variable_id`/`texto_reactivo` de las dos tablas. Lo único ya inspeccionado al redactar esto son hechos estructurales de premisa (conteo de filas, nombres de columna, lista de valores únicos de `instrumento`, tasa de llenado de `texto_reactivo`) — no el contenido semántico de los 9 pares. Si un tercer commit corrige esta especificación, se declara como corrección, nunca se edita hacia atrás.

## 0 · Hecho estructural que gobierna toda la búsqueda (premisa 3, re-derivada)

Comando y resultado, contra `2953716`/`3181d55` (ver nota de cierre para el detalle completo de A.13):

```
data/inventario-reactivos-v1_1.tsv: 178246 filas de datos (5 líneas de comentario + 1 encabezado + 178246 filas, wc -l=178252)
data/inventario-fd-v1_0.tsv:         17094 filas de datos (0 comentarios + 1 encabezado, wc -l=17095)
texto_reactivo vacío en inventario-reactivos-v1_1: 178246 de 178246 (100% vacío — la tabla solo trae variable_id/instrumento/metadata, nunca texto)
texto_reactivo vacío en inventario-fd-v1_0:        0 de 17094 (100% con texto)
```

**Consecuencia para la receta:** la vía `texto` (columna `via`) solo puede producir hits reales contra `inventario-fd-v1_0.tsv` — correrla contra `inventario-reactivos-v1_1.tsv` es válido (A.13 exige correrla y declarar el conteo) pero su resultado en cero está estructuralmente garantizado, no es un negativo del contenido. La vía `id` (`variable_id`, y `instrumento` solo para co-observación, nunca como generador de candidato por sí solo) corre contra las dos tablas.

`inventario-fd-v1_0.tsv` cubre 21 instrumentos únicos (entre ellos `enasem*`, `enasic2022`, `enfih2019`, `endutih*`, `ADQ15_CNBV_*`, `mociba*`, `envipe2013`, `(raiz)`). **No cubre** `enif2024`, `encuci2020`, `envipe2018-2025` (salvo 2013), `endireh*`, `enoe*`, Latinobarómetro — es decir, los instrumentos donde viven las anclas de θ ya fijadas (`familismo_apoyo`→ENIF 2024, `radio_confianza`→ENCUCI 2020) no tienen ficha de texto en este universo. Esto se declara aquí porque acota de antemano lo que la búsqueda de texto puede encontrar para los pares G5; no es un ajuste posterior a ver resultados de término.

## 1 · Método de búsqueda (aplica a los tres bloques (a)-(d) de todos los pares)

Búsqueda en Python 3 (`csv`, UTF-8), nunca `grep`/`sed` de shell — regla del encargo tras el incidente del 28/ago (0 hits de shell contra 13 reales por acentos). Cada término de la lista cerrada se escribe **en las dos formas, con acento y sin acento** (columna "términos" abajo), y adicionalmente el comparador normaliza both needle y haystack quitando diacríticos (`unicodedata.NFKD` + filtro de combining marks) y baja a minúsculas, de modo que un término mal capturado en una sola forma no produce un falso negativo — cinturón y tirantes sobre la misma falla que ya rompió un negativo el 28/ago. Substring match, no regex de límites de palabra (los `variable_id` son códigos cortos tipo `p9_9_4`/`AP5_1_1`, no prosa). Columnas exploradas: `variable_id` y `texto_reactivo` para generar candidatos; `instrumento` se lee siempre junto con cada hit pero **no** se busca por término — solo sirve para el criterio de co-observación (§3).

## 2 · Por par: requisito de θ y de desenlace, con cita, y lista cerrada de términos

Fuente común de "qué genera" cada generador: `canon/modelo-decision-v4_0.md` tabla §2.1, líneas 432-440. Fuente común de la fila B (columna `nota`): `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente.detalle`, líneas 1113-1126.

### G2.sens_estatus (B: `milpa/procedencia.yaml:1114`, nota "búsqueda de reactivo cerrada, ADR-54")
- **θ** = sensibilidad al estatus/posición social. Requisito derivado de `modelo-decision:436` ("Desigualdad + baja movilidad" → "Ansiedad de estatus, consumo compensatorio (rama estatus)"): un reactivo que mida qué tanto le importa a la persona su posición/imagen social relativa.
- **Desenlace** = el generador G2 completo produce un solo desenlace nombrado en `modelo-decision:436`: "ansiedad de estatus, consumo compensatorio". Aplica igual a `G2.aversion_riesgo` (mismo generador, mismo desenlace nombrado).
- Términos θ: `estatus`, `status`, `prestigio`, `prestigiosa`, `prestigioso`, `imagen social`, `que dirán`, `que diran`, `aparentar`, `apariencia social`, `ostentar`, `ostentación`, `ostentacion`, `posición social`, `posicion social`, `nivel social`, `envidia`, `comparación social`, `comparacion social`.
- Términos desenlace: `ansiedad de estatus`, `ansiedad social`, `estrés social`, `estres social`, `consumo compensatorio`, `consumo conspicuo`, `gasto en imagen`, `compra por estatus`, `compra por status`, `deuda por aparentar`, `gasto ostentoso`, `compra impulsiva`.

### G2.aversion_riesgo (B: `milpa/procedencia.yaml:1115`, nota "búsqueda de reactivo cerrada, ADR-52 A")
- **θ** = aversión/tolerancia al riesgo. `modelo-decision:436,456` (coeficiente `aversion_riesgo 0.20` dentro de G2).
- **Desenlace** = el mismo de G2 arriba ("ansiedad de estatus, consumo compensatorio").
- Términos θ: `aversión al riesgo`, `aversion al riesgo`, `tolerancia al riesgo`, `preferencia por seguridad`, `evitar riesgo`, `evita el riesgo`, `riesgo financiero`, `disposición a arriesgar`, `disposicion a arriesgar`, `prefiere no arriesgar`, `toma de riesgos`.
- Términos desenlace: los mismos de G2.sens_estatus (mismo generador).

### G3.aversion_riesgo (B: `milpa/procedencia.yaml:1117`, nota "misma búsqueda cerrada que G2·aversion_riesgo, ADR-52 A")
- **θ** = aversión al riesgo (mismos términos que G2.aversion_riesgo — misma θ, generador distinto).
- **Desenlace** = `modelo-decision:437` ("Informalidad + volatilidad de ingreso" → "Horizonte corto, ahorro informal, aversión").
- Términos θ: idénticos a G2.aversion_riesgo arriba.
- Términos desenlace: `horizonte corto`, `corto plazo`, `ahorro informal`, `tanda`, `cundina`, `guardadito`, `debajo del colchón`, `debajo del colchon`, `sin cuenta bancaria`, `ahorro en efectivo`, `no planea a futuro`, `sin planeación`, `sin planeacion`.

### G4.horizonte_temporal (B: `milpa/procedencia.yaml:1121`, nota "sin reactivo dedicado; único proxy (ENIF P4_10) es de G3 y cruza instrumento distinto de los desenlaces de G4")
- **θ** = horizonte temporal (orientación a corto/largo plazo). `modelo-decision:438` coeficiente compartido con G3 en la tabla de §2.2 pero aquí como θ de G4.
- **Desenlace** = `modelo-decision:438` ("Exposición a violencia + impunidad" → "Conducta defensiva, retracción del espacio público"). Aplica igual a `G4.sens_estatus`.
- Términos θ: `horizonte temporal`, `planeación a futuro`, `planeacion a futuro`, `corto plazo`, `largo plazo`, `futuro cercano`, `expectativas a futuro`, `orientación al futuro`, `orientacion al futuro`.
- Términos desenlace: `conducta defensiva`, `evita salir`, `deja de salir`, `restringe sus salidas`, `evita lugares`, `miedo a salir`, `cambió de ruta`, `cambio de ruta`, `cambio de rutina`, `retracción`, `retraccion`, `espacio público`, `espacio publico`, `deja de frecuentar`, `autoconfinamiento`, `evita transitar`.

### G4.sens_estatus (B: `milpa/procedencia.yaml:1122`, nota "misma búsqueda cerrada que G2·sens_estatus, ADR-54")
- **θ** = sensibilidad al estatus (mismos términos que G2.sens_estatus — misma θ, generador distinto).
- **Desenlace** = el mismo de G4.horizonte_temporal arriba ("conducta defensiva, retracción del espacio público").
- Términos θ: idénticos a G2.sens_estatus arriba.
- Términos desenlace: idénticos a G4.horizonte_temporal arriba.

### G5.familismo_apoyo (B: `milpa/procedencia.yaml:1123`, nota "único candidato (ENIF p9_9_4) excluido por circularidad, marca C3, línea 265-270 arriba")
- **θ** = familismo de apoyo (transferencias/ayuda económica intrafamiliar). Ancla ya fijada: ENIF 2024, TMÓDULO, batería P9.9, `milpa/procedencia.yaml:300-319`. `marca_c3` (`milpa/procedencia.yaml:314-319`) excluye por circularidad usar esa misma batería (P9_9_1..6, incluido `p9_9_4`) para identificar el desenlace de G5, porque el desenlace de G5 en ENIF se observa con la misma batería.
- **Desenlace** = `modelo-decision:439` ("Familia como seguro ante Estado ausente" → "Pooling, corresidencia, carga de cuidado"). Aplica igual a `G5.familismo_obligacion` y `G5.radio_confianza` (mismo generador).
- Términos θ: `apoyo familiar`, `ayuda económica de familiares`, `ayuda economica de familiares`, `dinero de familiares`, `préstamo familiar`, `prestamo familiar`, `apoyo de la familia`, `remesas familiares`, `ayuda entre parientes`, `transferencias familiares`.
- Términos desenlace: `pooling`, `corresidencia`, `vive con`, `hogar extendido`, `cuidado de familiares`, `carga de cuidado`, `cuidador`, `cuida a`, `comparte gastos del hogar`, `hogar compartido`, `mudarse con la familia`, `se mudó con`, `se mudo con`.
- **Exclusión de circularidad (precedente citado en el encargo):** cualquier candidato cuyo `variable_id` sea `p9_9_1`..`p9_9_6` (batería ENIF P9.9 completa, no solo `p9_9_4`) se marca `CIRCULAR-EXCLUIDO` cuando se evalúa como lado-desenlace de este par, por ser la misma batería que opera la θ (`marca_c3`, `milpa/procedencia.yaml:314-319`); sigue siendo válido como candidato del lado-θ.

### G5.familismo_obligacion (B: `milpa/procedencia.yaml:1124`, nota "sin magnitud asignada (ADR-30); condicional propia solo PROXY CON SUPUESTO DECLARADO, forma PENDIENTE")
- **θ** = familismo de obligación (deber/obligación moral hacia la familia, distinto de apoyo recibido).
- **Desenlace** = el mismo de G5.familismo_apoyo arriba ("pooling, corresidencia, carga de cuidado").
- Términos θ: `obligación familiar`, `obligacion familiar`, `deber con la familia`, `responsabilidad familiar`, `compromiso familiar`, `deber moral con los padres`, `obligado a ayudar a la familia`, `debe cuidar a`, `debe mantener a`.
- Términos desenlace: idénticos a G5.familismo_apoyo arriba.

### G5.radio_confianza (B: `milpa/procedencia.yaml:1125`, nota "reactivo (ENCUCI) y desenlace (ENIF) en instrumentos distintos, sin muestra común")
- **θ** = radio de confianza interpersonal. Ancla ya fijada: ENCUCI 2020, SEC_4_5, ítems AP5_1_1/AP5_1_2/AP5_1_3, `milpa/procedencia.yaml:280-293`.
- **Desenlace** = el mismo de G5.familismo_apoyo arriba ("pooling, corresidencia, carga de cuidado"). La propia nota de B ya declara la instrumentación esperada del choque: θ vive en ENCUCI, el desenlace declarado de G5 vive en ENIF — instrumentos distintos, sin muestra común conocida de antemano.
- Términos θ: `radio de confianza`, `confía en`, `confia en`, `personas que conoce`, `vecinos de su colonia`, `desconocidos`, `confianza interpersonal`, `círculo de confianza`, `circulo de confianza`.
- Términos desenlace: idénticos a G5.familismo_apoyo arriba.

### G6.deferencia (B: `milpa/procedencia.yaml:1126`, nota "único proxy (Latinobarómetro P4NOIJ) sin desenlace de G6 documentado en el mismo instrumento; SIN_DISEÑO_PUBLICADO")
- **θ** = deferencia hacia la autoridad. `modelo-decision:440` ("Jerarquía + indulgencia" → "Deferencia, iniciativa suprimida, paternalismo"); aquí la θ y una palabra del desenlace comparten nombre (`deferencia`), riesgo de circularidad declarado de antemano (ver §3).
- **Desenlace** = `modelo-decision:440`, la parte del desenlace que NO es la propia θ: "iniciativa suprimida" (y, secundariamente, "paternalismo").
- Términos θ: `deferencia`, `obediencia`, `obedece`, `respeto a la autoridad`, `no cuestiona`, `acata órdenes`, `acata ordenes`, `sumisión`, `sumision`, `subordinación`, `subordinacion`.
- Términos desenlace: `iniciativa suprimida`, `no toma la iniciativa`, `espera instrucciones`, `no opina`, `se abstiene de proponer`, `paternalismo`, `decisiones tomadas por otros`, `no participa en las decisiones`.
- **Exclusión de circularidad:** un candidato cuyo `texto_reactivo`/`variable_id` sea la propia palabra "deferencia" o su transformación trivial (p. ej. "deferente", "obediencia" como sinónimo estricto del mismo constructo) no cuenta como lado-desenlace aunque aparezca en la lista de términos de desenlace por error de redacción — solo cuenta "iniciativa suprimida"/"paternalismo" y sus términos propios como desenlace válido.

## 3 · Criterio de CANDIDATO

Una fila de cualquiera de las dos tablas cuenta como **CANDIDATO** de un lado (θ o desenlace) de un par cuando:

1. Al menos un término de la lista cerrada de ese lado aparece como subcadena (comparación sin acentos, minúsculas) en `variable_id` **o** en `texto_reactivo` de esa fila; **y**
2. Una lectura del recorte (`texto_reactivo` cuando existe; si no, el propio `variable_id` y su `archivo_miembro`) confirma que el término refiere al constructo del par, no a un homónimo. Riesgo declarado de antemano: `estatus` puede matchear "estatus migratorio"/"estatus civil"/"estatus legal" — ninguno de esos es sensibilidad al estatus social (G2/G4) y se marca `DESCARTADO-con-razón`, no `CANDIDATO`, aunque el término haya hecho match textual.

`instrumento` **nunca** genera un candidato por sí solo (un nombre de instrumento no es una operacionalización de nada) — solo se usa para el criterio de co-observación, §4.

## 4 · Criterio de co-observación

Un par se sella `EXISTE-SATISFACE` únicamente cuando existe al menos un `CANDIDATO` de lado-θ **no circular** y al menos un `CANDIDATO` de lado-desenlace **no circular**, ambos con el **mismo valor exacto** de columna `instrumento` (p. ej. `enif2024`, `encuci2020` — el campo ya codifica instrumento+ola/año). La mera co-familia (dos años de la misma encuesta, p. ej. `envipe2023` y `envipe2024`, o dos instrumentos del mismo levantamiento institucional) **no basta**: cada valor de `instrumento` es una muestra distinta salvo que el string sea idéntico byte a byte.

## 5 · Exclusión de circularidad (regla general)

Un candidato se marca `CIRCULAR-EXCLUIDO` cuando su operacionalización es la propia θ del par (o una transformación trivial de ella: recodificación, dicotomización, negación, cambio de unidad sin cambio de constructo) evaluada como si fuera el lado-desenlace, o viceversa. Precedente citado en el encargo: `p9_9_4` (ENIF, "dinero de familiares") es la θ de `familismo_apoyo`; la misma batería P9_9_1..6 es también donde ENIF observa el desenlace de G5 (`marca_c3`, `milpa/procedencia.yaml:314-319`) — por eso ningún ítem de esa batería puede contar como candidato de lado-desenlace de `G5.familismo_apoyo`/`G5.familismo_obligacion`/`G5.radio_confianza`, aunque sí sigue siendo válido (y ya anclado) como lado-θ de `G5.familismo_apoyo`.

## 6 · Prioridad de corrida

1. `G5.familismo_apoyo`
2. `G5.radio_confianza`
3. `G5.familismo_obligacion`
4. `G2.sens_estatus`
5. `G2.aversion_riesgo`
6. `G3.aversion_riesgo`
7. `G4.horizonte_temporal`
8. `G4.sens_estatus`
9. `G6.deferencia`

El primer resultado que produzca este procedimiento es el que se reporta.
