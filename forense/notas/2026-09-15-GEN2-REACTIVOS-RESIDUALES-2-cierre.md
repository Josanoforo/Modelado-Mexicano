# ACTO GEN2-REACTIVOS-RESIDUALES-2 · EL TEXTO QUE FALTABA YA ESTABA EN EL REPO — nota de cierre

**15/sep/2026 · entorno NUBE · Opus · cero llamadas a modelo · cero microdato abierto · cero descargas · cero adopciones · contador científico CERO.**

Base: `origin/main = 0cdbd72` (merge de `PR #789`), 0 commits detrás al arrancar.
Encargo archivado verbatim (0-bis A.3): `forense/encargos/2026-09-15-GEN2-REACTIVOS-RESIDUALES-2.md`, commit `866f922`.
Entorno crudo (`python3 tools/entorno.py`): `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default · git_status=LIMPIO(0) · python=3.11.15 · numpy/pandas/scipy/pyreadstat AUSENTES · raices=data_raw:NO · corpus=NO(examinados=0)`. Red no sondeada: este acto no la usa (sonda opt-in, «una sonda que nadie pidió es I/O que nadie declaró»).

## 0 · El titular

`NC-0136` arrastraba desde el 11/sep una frase que nadie podía comprobar: *«los 81 grupos históricamente ciegos que quedan fuera del lote»*. Este acto la convierte en comando — y al hacerlo encuentra que **26 de esos 81 grupos (36 707 de las 129 648 filas ciegas) ya tienen el enunciado del reactivo publicado dentro del propio repositorio**, en la capa FD que existe desde `ADR-215`/`ADR-216` y que el buscador **nunca consultó por ninguna clave**.

No era un problema de adquisición ni de extractor: era un cable que faltaba. La consecuencia inmediata es que la compuerta que `ACTO GEN2-F5-CIERRE-Y-PANEL-1` dejó escrita para el panel de `F6` se contesta hoy, en NUBE, sin corpus y sin adquirir nada.

## 1 · P1 · El 81 deja de ser prosa

`tools/censa_reactivos_ciegos.py` → `data/reactivos-ciegos-81-v1_0.tsv` (derivado, se re-genera, no se edita a mano):

```
$ python3 tools/censa_reactivos_ciegos.py --salida data/reactivos-ciegos-81-v1_0.tsv
UNIVERSO · 241591 filas · 116 instrumentos · archivos examinados = 2 (A.13)
CAPA FD  · 27729 filas · archivos examinados = 2 (A.13)
PANEL F6 · leido: F5-panel-candidatos-v1_2.tsv (vigente por version, no fijado en el codigo)
CIEGOS   · 102 instrumentos (21 del lote prioritario)
GRUPOS FUERA DEL LOTE · 81 · 129648 filas ciegas
  con texto FD limpio ya en el repo · 18 grupos · 16815 filas ciegas con ruta sin corpus
  candidatas por fd_ext (PDF/XLS, con artefactos de encabezado) · 8 grupos · 19892 filas ciegas
  reclamados hoy por mapa-19 o panel F6 · 18 grupos
```

**El 81 sale exacto**, y sale de la misma definición que la cabecera de `data/inventario-reactivos-v1_2.tsv` ya había publicado (102 instrumentos ciegos de 116): 102 − 21 del lote = 81. Que reproduzca un número heredado sin haberlo mirado antes es el control de que el grano es el mismo y no uno nuevo con el mismo rótulo.

| | grupos | filas ciegas |
|---|---:|---:|
| ciegos totales | 102 | 164 656 |
| del lote prioritario (`ENVIPE`/`ENIF`/`ENCUCI`/`ENSAFI`/`ENNViH`) | 21 | 35 008 |
| **fuera del lote — los 81 de `NC-0136`** | **81** | **129 648** |
| de esos, con texto FD **limpio** ya en el repo (descriptor XLSX) | 18 | 16 815 |
| de esos, **candidatos** por `fd_ext` (PDF/XLS, por verificar) | 8 | 19 892 |
| de esos, que exigen FD en corpus | 55 | 92 941 |

**Las dos capas FD no prometen lo mismo, y el censo dejó de mezclarlas.** `fd` (`inventario-fd-v1_1.tsv`, descriptores XLSX) da pares `variable → enunciado` limpios. `fd_ext` (`inventario-fd-ext-v1_0.tsv`, PDF/XLS) arrastra **encabezados de tabla como si fueran reactivos**: 6 745 de sus 10 635 filas caen en tripletas `(instrumento, variable_id, texto)` repetidas, y `elcos2012` es el caso extremo — sus 29 filas son el encabezado «(2) | (1)», con **cero** enunciados utilizables. Por eso los 26 se parten en **18 resueltos** y **8 `CANDIDATA-FD-EXT-POR-VERIFICAR`**, y el censo no promete texto que no existe. Esto se descubrió al reconciliar con el panel v1.2 (§7), no antes: la primera versión del censo habría rotulado `elcos2012` como resuelto.

**Lo que el censo NO dice (A.15), declarado antes de que alguien lo lea al revés:** `filas_ciegas` mide que el enunciado no está indexado en el universo del buscador. No certifica que el reactivo no exista en la fuente, ni suficiencia ni insuficiencia científica de nada. La búsqueda por `variable_id` sí cubre estos grupos, y siempre lo hizo.

**Un límite honesto de la derivación mecánica.** `demanda_hoy` se deriva por **igualdad** de `instrumento` contra el mapa-19 y por prefijo contra las filas `RETENIDA*` del panel — nunca por subcadena, porque `ACTO GEN2-F5-CIERRE-Y-PANEL-1` midió que la subcadena inventa y omite en las dos direcciones. El precio es visible y se paga a la vista: `enadid2023` sale `NINGUNA-DECLARADA-HOY` aunque la **nota** de `CORR-0013` lo reclame materialmente (§3.2), porque la columna `instrumento` de esa fila dice `EDER2017`. La demanda que vive en prosa no se deriva; se lee.

## 2 · P2 · El cableado, no el barrido

`tools/busca_reactivos.py` gana dos claves **explícitas** de `--tablas`: `fd` (`data/inventario-fd-v1_1.tsv`, 17 094 filas) y `fd_ext` (`data/inventario-fd-ext-v1_0.tsv`, 10 635 filas). Mismo convenio que `contexto_v1_0` y `descargas_mx`: **nunca** entran en `vigente` ni en `--fuente`. Reapuntar `vigente` habría cambiado en silencio lo que ya lee quien no pidió esta capa.

**Control de conservación, medido y no supuesto** — cinco consultas contra `vigente` con el archivo nuevo y con el archivo anterior (`git show HEAD:tools/busca_reactivos.py`), cifra idéntica en las cinco:

| consulta | antes | después |
|---|---:|---:|
| `tanda` | 79 | 79 |
| `atraso` | 125 | 125 |
| `no denuncio` | 49 | 49 |
| `ahorro` | 522 | 522 |
| `corrupcion` | 134 | 134 |

**El grano no es el mismo, y se dice.** La capa FD indexa el **descriptor de archivo**, no el payload: su `archivo_miembro` es la tabla del FD y no trae `contexto_busqueda`. Un acierto en `fd` es un enunciado publicado por el instrumento, **no** una identidad acreditada del lote — el censo lo llama `CABLEAR-CAPA-FD-YA-EN-REPO` y no lo suma a la cobertura del overlay (43 020/55 895 sigue siendo 43 020/55 895).

`tests/test_reactivos_ciegos_fd.py`: **8/8**, incluida la prueba de que `fd`/`fd_ext` **no** están en `FUENTES`.

## 3 · P3 · El gasto útil, sobre la demanda de hoy

### 3.1 · Panel `F6` · la compuerta de `R01 · MOCIBA` se contesta: **SÍ trae batería de denuncia**

`ACTO GEN2-F5-CIERRE-Y-PANEL-1` dejó la parada escrita palabra por palabra: *«si el FD **no** trae batería de denuncia ante autoridad, MOCIBA cae, **no queda ninguna familia retenida ejecutable**, y eso se declara en vez de estirar la lista»*. Contra la capa recién cableada:

```
$ python3 tools/busca_reactivos.py --tablas fd --regex "Denunciar ante el Ministerio"
# universo examinado (A.13): fd=17094(texto=17094) -- 17094 identidades revisadas
# candidatas: 7 total
```

| ola | tabla | variable | enunciado |
|---|---|---|---|
| `mociba2017` | `MOD_2017_CIBERACOSO` | `P10_5` | Denunciar ante el ministerio, policía o el proveedor del servicio |
| `mociba2019` | `TR_ENDUTIH_MOCIBA` | `P10_5` | Denunciar ante el Ministerio Público o policía |
| **`mociba2021`** | **`TMOCIBA`** | **`P12_5`** | 12.5 ¿Qué acciones tomó o ha tomado como consecuencia de la(s) situación(es) que vivió(vive)? Denunciar ante el Ministerio Público o policía |
| `mociba2022` | `TMociba` | `P12_5` | (idéntico a 2021) |
| **`mociba2023`** | **`TMociba`** | **`P12_05`** | 12.05 … Denunciar ante el Ministerio Público o **Fiscalía Estatal** |
| `mociba2024` / `mociba2025` | `TMociba` | `P12_05` | (idéntico a 2023) |

Y la batería no es un reactivo suelto: 2021 trae además `P12_10` (denunciar ante autoridades escolares o laborales) y 2023 trae `P12_10` más `P12_11` (reportar ante la policía).

**La compuerta queda contestada en positivo. MOCIBA no cae.** Con tres precisiones que son del mismo hallazgo y se declaran aquí, no se guardan:

1. **La numeración del reactivo cambia entre las dos olas propuestas**: `P12_5` en 2021, `P12_05` en 2023. Una spec que fije la variable por nombre sin distinguir ola se rompe en silencio; el índice lo hace visible antes de escribirla.
2. **La redacción cambia**: 2021 dice «Ministerio Público o policía»; 2023 dice «Ministerio Público o Fiscalía Estatal» y **desdobla** el reporte a la policía en `P12_11`. Que 2023 tenga un reactivo más significa que la codificación «puso el hecho en conocimiento de una autoridad» **no es la misma unión de opciones en las dos olas**. El panel afirmó «mismo bloque de diseño»: para la batería de denuncia, esto lo matiza y hay que decirlo antes de fijar la codificación.
3. **Esto no autoriza nada más.** No abre `F6`, no autoriza piloto ni confirmación ni llamadas, no toca `FP-374` (sigue `ABIERTA`, con su recomendación *NO AUTORIZAR EL PILOTO HOY* intacta) y no cierra `NC-0161`: fijar universo, codificación y ponderador sigue exigiendo el FD completo y la decisión de mesa. Lo que cae es **un bloqueo material**, no la decisión.

### 3.2 · mapa-19 · dos corroboraciones y dos negativos acotados

De los 19 `CORR`, cuatro nombran instrumentos ciegos que este acto alcanza. La capa FD contesta, desde el repo, cosas que se creían de CAJA:

| `CORR` | qué decía la fila | qué dice la capa FD hoy |
|---|---|---|
| **`CORR-0014`** `ENUT2024` | *«`milpa` declara ponderador `FAC_HOG` sobre `tvar_crea.csv`; `tvar_crea.csv` NO tiene `FAC_HOG` … `FAC_HOG` vive en `tsdem.csv` Y en `thogar.csv`»* (hallazgo A.15) | **Corroborado independientemente, sin abrir microdato**: el FD de `enut2024` trae `FAC_PER` en `TVAR_CREA` y `TMODULO`, `FAC_HOG` en `THOGAR` y `TSDEM`, `FAC_VIV` en `TVIVIENDA`. `TVAR_CREA` tiene **60** columnas — las 60 que la fila decía |
| **`CORR-0012`** `ENFIH2019` | *«`FAC_HOG` fijado POR ARCHIVO (`TCONCENTRADORA.csv`): la misma etiqueta existe en `THOGAR.csv` sobre otro universo»* | **Corroborado**: el FD trae `FAC_HOG` exactamente en `TConcentradora` y `THogar`, `FAC_VIV` en `TVivienda` y `FACTOR` en las otras 13 tablas. La ambigüedad que la spec resolvió a mano es visible en el índice |
| **`CORR-0013`** `EDER2017` | *«`RES-0043/RES-0044` declaran payload EDER 2017 y clase “ENADID 2023, `p3_27_ag`”. El payload declarado no produjo el número … ENADID no aparece en ninguna corrida»* | **El defecto material se estrecha y se localiza**: `P3_27_AG` **existe**, con enunciado publicado — `enadid2023`, tabla `TSDEM`, *«Situación conyugal agrupada»* (y `P3_27`, *«¿Actualmente (NOMBRE) …»*). En el FD de `eder2017`: **cero** filas `p3_27` (examinadas las 1 422 de `inventario-fd-ext-v1_0.tsv`). O sea: la variable no falta — **está en el instrumento que la fila dice, y no en el payload que la fila declara**. Es un desajuste de payload, no una variable inexistente |
| **`CORR-0001`/`CORR-0002`** `ENCIG2023`/`ENCIG2025` | `BLOQUEADA` por decisión de mesa / `EXISTE-SATISFACE` | **Negativo acotado (A.13/A.15)**: `encig2023` y `encig2025` están entre los 81 y **no** tienen texto FD en el repo (0 filas; sólo `encig2011` trae 6). Examinadas las 27 729 filas de las dos tablas FD. Esto no dice que el FD no exista: dice que **no está indexado aquí**, y su ruta es `REQUIERE-FD-EN-CORPUS` |

`CORR-0011` (`ENIGH2022`) y las cinco olas de `ENESTYC` y las dos de `ENAPROCE` que el panel toca caen igual en `REQUIERE-FD-EN-CORPUS`: nombradas en el censo, sin ruta desde NUBE, sin fingir que la tienen.

### 3.3 · El residual del lote (12 875 filas), ordenado por demanda en vez de re-barrido

El lanzamiento pidió explícitamente **no repetir todo el barrido**. Cruzando los 6 091 grupos residuales contra la columna `instrumento` del mapa-19:

| | grupos | filas físicas | % |
|---|---:|---:|---:|
| residual que pertenece a un instrumento **reclamado hoy** por el mapa-19 | 1 106 | **2 693** | 21% |
| residual que **no bloquea nada hoy** | 4 985 | **10 182** | 79% |
| **total** | **6 091** | **12 875** | |

Y dentro de las 2 693 reclamadas, por motivo acreditado:

| instrumento | `CORR` que lo reclama | ambigua | etiqueta técnica | auxiliar sin reactivo |
|---|---|---:|---:|---:|
| `envipe2025` | `CORR-0007` | 643 | 451 | 701 |
| `enif2024` | `CORR-0009`/`0010`/`0015` | 0 | 1 | 839 |
| `encuci2020` | `CORR-0003` | 26 | 32 | 0 |

**La lectura que esto permite, y que antes no se podía hacer:** de las 12 875 filas residuales, las que hoy bloquean una demanda viva y **no** son llaves/ponderadores (`FILA_AUXILIAR_SIN_REACTIVO`, que por diseño no tienen reactivo y siguen en el denominador) son **1 153**. El resto es deuda real pero sin consumidor declarado hoy. Eso es el orden de trabajo del sucesor, no un permiso para borrar nada: las 10 182 siguen contadas, con su motivo, en `data/reactivos-contexto-residual-v1_1.tsv`, que este acto **no tocó**.

## 4 · Lo que este acto NO hizo

No re-extrajo texto de ninguna fuente (no hay corpus en NUBE) · no publicó `contexto-v1_2` ni re-generó ningún índice · no editó `inventario-reactivos-*`, `inventario-fd-*`, `contexto-v1_1` ni `residual-v1_1` · no cerró `NC-0136` (siguen los 55 grupos sin FD en repo y el residual del lote) · no cerró `NC-0161` ni movió `FP-374` · no abrió `F6` · no adquirió, no descargó, no firmó por mesa, no adoptó y no fusionó ningún PR.

## 5 · Verificación

- `python3 -m unittest tests.test_reactivos_ciegos_fd`: **8/8**.
- Control de conservación del buscador: 5/5 consultas con cifra idéntica al archivo anterior (§2).
- Censo idempotente: dos corridas seguidas escriben el mismo archivo byte a byte.
- `python3 tests/check.py --baseline`: **LÍNEA BASE VERDE**, 3 FAIL · 4 354 WARN, nada nuevo contra `tests/baseline.json`. La primera corrida sí trajo un `FAIL` nuevo — `T27`: un archivo nuevo bajo `data/` sin cita en `data/INFRAESTRUCTURA-v1_0.md` — y se reparó por la vía que el propio test nombra (fila nueva en el índice, dominio de reactivos, no `_T_INFRA_ARCHIVOS_CONOCIDOS`), no silenciándolo.
- Contador científico: **cero**. Ninguna corrida, ningún `RESULT`, ninguna adopción.

## 6 · Concurrencia declarada

Al arrancar, `git ls-remote --heads origin` mostraba una rama viva ajena (`claude/gracious-turing-6v83oj`, sin PR verificable desde este entorno). Ninguna coincidencia con este rótulo en las tres superficies del guard 0.c (rama remota, worktree, PR). Si esa rama toma `ADR-519` primero, renumera quien fusione segundo — regla de la casa.

## 7 · Reconciliación con `main` (cuarta sincronización) — y lo que obligó a corregir

Mientras este acto estaba en vuelo, `main` avanzó 15 commits y fusionó, entre otros, `ACTO GEN2-MANTENIMIENTO-Y-ARCHIVO-2` (`ADR-517`, `NC-0225..0228`) y **`ACTO GEN2-PANEL-F6-EXPANSION-1`** (`ADR-518`, `NC-0230..0234`). Renumera quien fusiona segundo: este acto pasa a **`ADR-519`** y **`NC-0235`/`NC-0236`/`NC-0237`**. En `forense/no-corrido.tsv`, `canon/registro-rotulos.tsv` y `canon/gobernanza-v1_15.md` las entradas de `origin` van primero; en `L0`, la anotación propia se inserta delante de la ajena sin reescribirla.

**Y la reconciliación no fue sólo de texto — encontró dos defectos propios:**

1. **El censo leía un panel superado.** `tools/censa_reactivos_ciegos.py` apuntaba a `F5-panel-candidatos-v1_1.tsv` fijo en el código. `GEN2-PANEL-F6-EXPANSION-1` publicó **v1.2 con 27 familias** (14 retenidas), así que el censo habría declarado `NINGUNA-DECLARADA-HOY` sobre familias que el panel nuevo **sí** reclama — en silencio, que es la clase de defecto que esta casa persigue. Ahora resuelve la **versión más alta presente** y **declara cuál leyó** (A.13). Efecto inmediato: los grupos reclamados suben de **15 a 18**, y aparecen dos con texto FD ya en el repo que antes no figuraban — `enpol2021` (`R11-TRA-ENPOL-MORDIDA`) y `elcos2012` (`R13-FAM-ELCOS`).
2. **`fd_filas_con_texto > 0` no era lo mismo que «hay enunciados utilizables».** Al mirar esos dos grupos nuevos se vio que la capa `fd_ext` (PDF/XLS) arrastra encabezados de tabla como filas: `elcos2012` tiene **29 filas y cero reactivos** (las 29 son «(2) | (1)»), y `enpol2021` mezcla reactivos reales (`P4_1_01`, *«¿El agente del Ministerio Público se identificó como autoridad?»*) con decenas de `Nemónico | Pregunta`. El censo separaba mal y **prometía de más**. Corregido con una distinción medida, no inventada: 6 745 de las 10 635 filas de `fd_ext` caen en tripletas repetidas, así que un grupo cuya única ruta viene de esa capa sale `CANDIDATA-FD-EXT-POR-VERIFICAR`. Los 26 se parten en **18 + 8**.

**Lo que esto NO cambia:** los 81 grupos, las 129 648 filas ciegas, las 27 729 filas de la capa FD, el hallazgo de MOCIBA (§3.1, que viene de la capa `fd` limpia) y las corroboraciones de §3.2. La suite sigue **VERDE** y las pruebas propias pasan **10/10** — dos nuevas, una por cada defecto de arriba, para que ninguno vuelva en silencio.

**Lo que queda dicho y no hecho:** verificar `enpol2021` y `elcos2012` contra su FD real es trabajo de CAJA, y `R11`/`R13` del panel v1.2 no reciben de este acto ninguna compuerta contestada — sólo la ruta y su grado de promesa. Va en `NC-0235`.
