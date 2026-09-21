# PISOS HISTÓRICOS DE CRÉDITO · ENIF 2018, 2015 y 2012 · conductas K1–K7 por ejes · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-DIN-CREDITO-HISTORIA-1 (21/sep/2026, CAJA), pieza P2. Tres CALC,
uno por ola, un solo medidor byte a byte:
`CALC-DIN-CREDITO-PISOS-ENIF2018-0001` · `CALC-DIN-CREDITO-PISOS-ENIF2015-0001`
· `CALC-DIN-CREDITO-PISOS-ENIF2012-0001`. Encargo archivado por A.3 en
`forense/encargos/2026-09-21-GEN2-DIN-CREDITO-HISTORIA-1.md` (sello de cuerpo
`a66577f187bb778a75a7acdbad9cbf00227a5ff6679044ab1dc78ed5428f428b`).
Compuerta única (protege: abrir dato): esta spec, el mapa, los tres `spec.yaml`
y el medidor congelados en el COMMIT-1 con sus sidecars, el sintético de
D-22 corrido sobre las tres formas de archivo y el ORO verificado, antes de
tocar microdato de 2018, 2015 o 2012.

## 0 · Exposición declarada (ADR-46)

- Leídos antes de congelar: `data/credito-comparabilidad-texto-v1_1.tsv`
  (40 filas; P1 de este acto), los cuestionarios 2012/2015/2018 (secciones 3,
  5 y 6; universo), los FD 2012/2015 (hojas TMODULO1/TMODULO2/TSDEM y
  TModulo1/TModulo2/TSDem: llaves, diseño, factores, NIV, 3.9/3.10, 5.3/5.4),
  el diccionario y los catálogos del ZIP 2018 (`niv`, `p3_11`, `p5_4`, `p5_5`,
  `p6_*`, `tloc`, `sexo`, `edad`), **la cabecera de campos de cada DBF** de
  2012 y 2015 (descriptor: nombres, tipos y anchos — el FD 2015 no documenta
  `UPM_DIS` y el archivo sí lo trae), y la cabecera del CSV 2018 (columnas en
  minúsculas). Del molde #943: su spec, `spec.yaml`, medidor y
  `resultados.json` (sellado, público en el repo).
- NO abierto: ningún registro de microdato de 2018, 2015 ni 2012 (ni valor
  ni distribución). ENIF 2024 no se abre en ninguna forma (PARO a). ENIF 2021
  se leyó **sólo** para el ORO (§4): reproducir #943 con el mismo punto de
  entrada, cifra ya sellada y pública; no produce ninguna cifra nueva.
- Los tres payloads sintéticos de D-22 los fabrica
  `tests/test_din_credito_pisos_historia.py` (`payload_2018/2015/2012`, 2 400
  filas, `default_rng(7)`), con la forma real de cada ola (CSV en minúsculas;
  pares DBF con cabecera dBase y los saltos de cada cuestionario). No se
  parecen a la distribución real y no producen ninguna cifra esperada.
- Cifra esperada: ninguna. Las series públicas de ENIF (crédito formal por
  ola) son `[REPORTADO]` y no validan ni invalidan nada.
- `[SUPUESTO]` verificado por descriptor: 2018 `fac_per`, `est_dis` (001-012),
  `upm_dis` (00001-00826) en `tmodulo.csv`; 2015 `FAC_PER` (C5), `EST_DIS`
  (C3), `UPM_DIS` (C5) en `tmodulo1.DBF`; 2012 `FAC_PER` (N10; el FD admite
  0), `EST_DIS` (C2: 11-14, 21, 22, 31, 32, 41, 42), `UPM_DIS` (C5) en
  `stmodulo1_e2.dbf`; `SEXO`/`EDAD` de 2012 sólo en `stsdem_e2.dbf`.

## 1 · Alcance por ola — leído de la tabla v1.1, no tecleado

El medidor recibe `data/credito-comparabilidad-texto-v1_1.tsv` y emite una
conducta **sólo si su fila K·ola es `MISMO-INSTRUMENTO` o `CAMBIO-MENOR`** y el
mapa trae la variable de su rol; **PARA** si la tabla es positiva y el mapa no
trae la variable, o si el mapa la trae y la tabla dice otra cosa; PARA si K8 es
positivo en cualquier ola (FP-404). Toda conducta emitida lleva
`-VEREDICTO-TEXTO` y `-MATIZ` (el `alcance_del_veredicto` de su fila) — firma
de mesa: «una ola CAMBIO-MENOR entra a la serie con su matiz escrito en cada
RESULT».

| ola | entran (veredicto v1.1) | no entran (veredicto v1.1) | conductas emitidas | celdas |
|---|---|---|---|---|
| 2018 | K1 K2 K3 K4 K5 K6 (`CAMBIO-MENOR`) | K7 `NO-ESTIMABLE` · K8 `CAMBIO-DE-INSTRUMENTO` | 14: `K1`, `K2-DEPARTAMENTAL/-NOMINA/-AUTOMOTRIZ`, `K3`, `K4A-AUTOEXCLUSION`, `K4B-OFERTA`, `K4B1/2/3`, `K5`, `K5-ENTRE-SOLICITANTES`, `K6-PR`, `K6-P-TENEDORES` | 18 (como #943) |
| 2015 | K1 K2 K3 K5 K6 (`CAMBIO-MENOR`) | K4 `CAMBIO-DE-INSTRUMENTO` (multirrespuesta) · K7 `NO-ESTIMABLE` · K8 `CAMBIO-DE-INSTRUMENTO` | 9 | 15 (sin formalidad ni universo) |
| 2012 | K1 K2 K3 K5 K6 (`CAMBIO-MENOR`) | K4 `CAMBIO-DE-INSTRUMENTO` (multirrespuesta, base «no tiene hoy», autoexclusión fundida) · K7 · K8 | 9 | 15 |

Bancaria (`K2` familia 6.x.2) **no se lee ni se emite** en ninguna ola (FP-404
(2): su descriptivo rotulado es P4 de este acto y no cruza por ejes). `K3`
en 2012 es la unión de **cuatro** ítems (empeño, amigos o conocidos,
familiares, otro): la «caja de ahorro entre amigos o conocidos» de 2012 tiene
otro referente que la «caja del trabajo o de personas conocidas» y **se
excluye, no se colapsa** (PARO c del encargo: nada se colapsa). El matiz va
en cada RESULT de `K3·2012`.

## 2 · Desenlaces — códigos del mapa (`DIN-CREDITO-PISOS-HISTORIA-mapa-v1_0.tsv`)

Qué variable cumple cada rol en cada ola vive en el mapa, con su fuente (FD
fila, cuestionario página, cabecera DBF) y su regla; el medidor lo lee y no
trae ningún nemónico de ola (los de 2021 tampoco: la fila 2021 del mapa es la
del ORO). Reglas, idénticas a #943 salvo lo que la ola obliga:

- **Tenencia** (`K1`): 2021 batería universal. 2018/2015/2012 la batería está
  **gateada por un filtro** (6.3+6.4 · 6.4 · 6.4): tenedor = filtro Sí o algún
  ítem = 1; sin producto = filtro No (batería en blanco por pase → No);
  otro caso indefinido y contado. «Filtro Sí y batería toda No» se cuenta
  (`FILTRO-SI-BATERIA-TODO-NO-N`), no se corrige.
- **`K2-*`** = 1 si el ítem de la familia = 1; 0 si = 2 **o** blanco de quien
  dijo No al filtro. Familias por texto, nunca por sufijo: en 2012
  departamental es `P6_6_2` (orden invertido).
- **`K3`** = 1 si algún ítem informal = 1; 0 si todos = 2. 2015 reordena los
  ítems (la unión no depende del orden); 2012 sin caja (§1).
- **`K4*`** sólo 2018 (y 2021): base «nunca ha tenido» = filtro No ∧ 6.5 = 2;
  (a) = {6,7}; (b) = {1,2,3}; b1/b2/b3 = {1}/{2}/{3}; catálogo 1..8 (8 =
  Otro; «impuestos» no existe): fuera de la base o de catálogo → indefinido.
- **`K5`** = 1 si rechazo = 1; 0 si ∈ {2,3}; entre solicitantes 0 sólo si 2.
- **`K6-PR`**: una fila por par persona × producto tenido **con variable de
  atraso**, comparación posicional k↔k. 2021/2018: atraso 1 = Sí, 2 = No.
  2015/2012: una variable de cinco códigos, atraso = {1, 2}, No = 3. 8, 9 y
  blanco indefinidos. En 2018 el ítem 8 «Otro» no tiene variable de atraso:
  sus productos tenidos se cuentan (`K6-PRODUCTOS-TENIDOS-SIN-VARIABLE-DE-
  ATRASO-N`) y no entran al marco PR.
- **`K6-P-TENEDORES`**: persona con ≥ 1 producto cubierto por variable de
  atraso: 1 si alguno atrasó; 0 si todos los cubiertos No; si no, indefinido.
- **`K7`** sólo 2021 (NO-ESTIMABLE en las tres olas históricas).

## 3 · Ejes y rejilla — de la tabla de identidad GEN2; mapa por ola

Categorías leídas de `PISOS-REJILLA-arbitro-metadatos-v1_0.tsv` (filas
`ENIF·2021·CONSTRUIBLE`) y, cuando el eje es construible,
`PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv`; cortes importados por bytes
del medidor sellado de -0003 (`_age`, `_school`, `TLOC` 1-2/3-4). Variable
por ola en el mapa, resuelta por texto:

- `sexo`, `edad`, `localidad`: mismos catálogos en las cuatro olas
  (`TL` en 2012). **Población 18-70** en 2012/2015/2018 (diseño de la ola):
  la celda `60+` es 60-70 y `NACIONAL-TODOS` es 18-70; contra #943 (18+)
  son conmensurables **sin recorte** las celdas de `edad` 18-29, 30-44 y
  45-59, y **con recorte de 2021 a 18-70** las demás — recorte que este acto
  no corre (no abre un CALC nuevo sobre 2021; la corrida de #943 es sellada)
  y que se pregunta a mesa (encargo §6).
- `escolaridad`: `NIV` con el mismo catálogo de 11 códigos que `P3_1_1`.
- `cuenta`: 2021 batería `P5_4_1..9`; 2018 filtros `P5_4` ∨ `P5_5`; 2015
  `P5_4`; 2012 `P5_3` (sólo bancos: referente más estrecho, declarado en el
  mapa como MATIZ del eje).
- `formalidad`: 2018 `P3_11` («Por parte de su trabajo…», catálogo idéntico a
  `P3_10` de 2021: 1-5 con, 6 sin, 9/blanco fuera; universo trabaja = 1..6).
  **2015 y 2012 NO-CONSTRUIBLE por texto**: 3.10 (2015) y 3.9 (2012)
  preguntan derechohabiencia general (código 1 = Seguro Popular; sin «por
  parte de su trabajo»; texto buscado en los dos cuestionarios completos: 0
  aciertos), otro referente que el de `PISOS-ENIF2021-formalidad-spec-v1_0.md`
  §1. Esas dos olas no emiten celdas de formalidad ni `UNIVERSO-TRABAJA`.

Celdas por conducta: 2018 = 18 (`NACIONAL-TODOS` + 14 + 2 formalidad +
`UNIVERSO-TRABAJA`); 2015/2012 = 15. Por celda: `-P`, `-IC-LO`, `-IC-HI`,
`-N`, `-DEN-W`, `-B-VALIDAS`, `-SOPORTE`.

## 4 · Procedimiento congelado, guardias y ORO

- Lectura: 2018 CSV del ZIP `enif2018_csv` (miembro
  `conjunto_de_datos/tmodulo.csv`, `utf-8-sig`/`latin-1`, `dtype=str`,
  columnas normalizadas a mayúsculas); 2015 DBF `tmodulo1.DBF` ⋈ `tmodulo2.DBF`
  (join interno por `UPM, VIV_SEL, HOGAR, R_SEL`; **PARA** si pierde o
  duplica filas); 2012 DBF `stmodulo1_e2.dbf` ⋈ `stsdem_e2.dbf` (join
  izquierdo por `CONTROL, VIV_SEL, HOGAR, R_SEL = N_REN`; sin pareja → sexo y
  edad indefinidos, contados; **PARA** si cambia el número de filas). El
  lector DBF es propio (cabecera + anchos fijos, latin-1); registros marcados
  como borrados se excluyen y se cuentan.
- Marco heredado verbatim de #943: ponderador de persona de la ola
  (`FAC_PER`; `FAC_ELE` en 2021) > 0; diseño `EST_DIS × UPM_DIS` no vacíos;
  bootstrap de UPM con reemplazo dentro de estrato, **10 000 réplicas,
  `numpy.PCG64(42)`**, IC percentil 2.5/97.5; **un solo plan de réplicas por
  corrida** (una llamada a `_estimate` sobre el marco combinado
  persona + producto). Sin filtro de edad ni de otro eje.
- **Guardia 1 · Unidad** (`-UNIDAD` P/PR por conducta; el medidor no suma ni
  promedia conductas). **Guardia 2 · Soporte** (`n < 200` → `BAJO-N-MENOR-200`,
  se emite igual; nunca se colapsan categorías). **Guardia 3 · Coherencia**
  por conducta × eje contra `NACIONAL-TODOS` (formalidad contra
  `UNIVERSO-TRABAJA`), tolerancia `1e-6 × den_w`; si no cierra, **PARA**.
  **Guardia 4 · Comparabilidad**: §1. **Guardia 5 · Mapa**: PARA si falta un
  rol de la ola.
- **ORO (encargo §5 P2).** El mismo `medir()` con `parametros.ola = 2021`
  (fila 2021 del mapa = variables de #943) reproduce los **2 939 RESULT** de
  `CALC-DIN-CREDITO-PISOS-ENIF2021-0001/resultados.json`: 0 faltantes, 0
  discordantes, `max |Δ| = 0.0` en flotantes; una sola clave extra
  (`K6-PRODUCTOS-TENIDOS-SIN-VARIABLE-DE-ATRASO-N`, que en 2021 vale 0). Los
  diagnósticos de #943 llevan nombre por variable y aquí por rol
  (`TRADUCCION_2021` del test, biyectiva, 11 claves). Asiento:
  `DIN-CREDITO-PISOS-HISTORIA-oro-2021.json`. Verificado el 21/sep/2026 antes
  del COMMIT-1 (`python3 tests/test_din_credito_pisos_historia.py --oro`).
- Ejecución diagnóstica sobre microdato histórico: **ninguna**. El medidor
  corrió antes de congelarse sobre los tres sintéticos (60 y 120 réplicas) y
  sobre ENIF 2021 para el ORO; la primera corrida real de cada ola es la que
  se reporta.

## 5 · Diagnóstico y exclusiones (se reportan, no se corrigen)

Por ola: `FILAS-PERSONAS`, `FILAS-PRODUCTO`, `TENEDORES-N`, `SIN-PRODUCTO-N`,
`TENENCIA-INDEFINIDO-N`, `FILTRO-SI-BATERIA-TODO-NO-N`,
`K5-FUERA-DE-CATALOGO-N`, `K6-ATRASO-NO-SABE-NO-RESPONDE-N`,
`K6-ATRASO-BLANCO-EN-PRODUCTO-TENIDO-N`,
`K6-PRODUCTOS-TENIDOS-SIN-VARIABLE-DE-ATRASO-N`, `UPM-EN-PLAN`,
`REGISTROS-DBF-BORRADOS` (2015/2012), `FILAS-SIN-SOCIODEMOGRAFICO-N` y
`TSDEM-LLAVE-DUPLICADA-N` (2012), `NUNCA-HA-TENIDO-N` y `EX-USUARIOS-N`
(2018/2015), `K4-MOTIVO-FUERA-DE-CATALOGO-N` y `-FUERA-DE-BASE-N` (2018),
`FORMALIDAD-N-UNIVERSO` y exclusiones (2018); por conducta `-N-UNIVERSO`,
`-COHERENCIA-<EJE>-DELTA-*`, `-EJE-<EJE>-INDEFINIDO-N`; textos
`POBLACION-BASE`, `FORMALIDAD-EJE`, `CONDUCTAS-EMITIDAS-N` y
`K<n>-VEREDICTO-TABLA` para las siete conductas.

## 6 · Lo que esta spec no hace

No abre ENIF 2024; no recorta ni reejecuta #943; no presenta como serie
ninguna ola `CAMBIO-DE-INSTRUMENTO` (PARO d); no colapsa empeño con gota a
gota ni K4(a) con K4(b) (PARO c); no mide K8 ni K2-bancaria; no adjudica ni
adopta (`cuenta_gen2 = SI` propuesto por dirección, «el lanzamiento es el
sello»); no edita ninguna spec, tabla de identidad ni CALC sellado; no toca
`tools/marcador_segmento.py`, `data/corrida0/marcador-segmento.tsv`,
`tools/corrida0.py` ni `milpa/`.
