# ACTO MAESTRA34-L2 · ARBITRA-v1_2 — nota de cierre

Encargo: `forense/encargos/cola/2026-09-01-MAESTRA34-L2-ARBITRA-v1_2.md`
(dirección/Fable, maestra-34, formato corto v2.12, SHA de redacción `8598a72`,
encolado por firma D4-a en el PR [COLA] `#448`). Entorno UBUNTU, caja con
corpus, skill `/acto` (`ADR-237`) + `/arbitra`. Base: `6d9692d`.

## 0 · Declaración de contaminación — `TRA-M-02` no se arbitró

**Esta sesión vio, antes de que su compuerta abriera, un valor `p` del motor
para la conducta de `TRA-M-02`.** Se declara primero porque condiciona el
alcance del acto, no al final como nota al pie.

Qué se vio y por dónde: el cuerpo del encargo de `MAESTRA34-L1`, leído para
verificar la condición B de la compuerta, cita verbatim tres líneas de
`milpa/tramite.yaml` — entre ellas `paga_mordida_encuci2020 p=0.125822 MEDIDO`
y `p: 0.62, clase: ASIGNADO` de `tramite.mordida.discrecional`. `TRA-M-02` es
**ENCUCI 2020, `AP5_17|AP5_18`, regla `tramite.mordida.discrecional`**: la tasa
que R calcularía para esa celda es la misma cantidad que ese número nombra.

Además, para verificar la compuerta de `MAESTRA34-N2` (motor > 8 reglas) esta
sesión corrió `grep -E '^\s*-\s*id:' milpa/tramite.yaml` dos veces. Esa corrida
devolvió **sólo ids de regla**, ningún `p` ni `clase` — se declara igual, por
`ADR-46` (la unidad de contaminación es la sesión) y porque `/arbitra` dice
que ese archivo no se abre ni «para confirmar».

Consecuencia aplicada: `TRA-M-02` **no entra en ningún lote**. No se le escribió
fila de `codificacion-R` ni se calculó su R — escribir su codificación es el
paso contaminable (define universo y dicotomización), no sólo el cálculo. Queda
para una sesión limpia. Las otras siete celdas no están afectadas: sus reglas
son `civico.denuncia.miedo_desconfianza`,
`familia.seguro.volatilidad_ausencia_estado` y `dinero.ahorro.tiene_ahorros`,
y de ninguna se vio valor alguno.

## 1 · Compuerta, verificada por producto

Las dos condiciones, verificadas **por un producto del acto, nunca por su
nombre** — porque bajo D4-a el propio commit de encolado mete los rótulos en
el historial:

- `marco-M-sorteado-v1_2.tsv` existe en `origin/main` (`git cat-file -e` → 0;
  daba 128 antes del merge de MAESTRA34-N2). 435 archivos examinados bajo
  `forense/prereg-duelo-v2/`, 13 artefactos `v1_2`, control positivo `v1_1`=30.
- `MAESTRA34-L1` fusionado: PR `#451`, merge `6d9692d`, verificado por los seis
  archivos que tocó fuera de `forense/encargos/`.

Este acto ya había parado antes con **cero commits**, dos veces, mientras la
compuerta estaba cerrada. `grep -c 'MAESTRA34-L1'` sobre el log daba `1` — y
ese `1` era el commit `[COLA]`. Es un falso positivo nuevo, introducido por
D4-a el 1/sep, sobre un mecanismo que `/acto` §2.2 ofrece como válido.

## 2 · Censo del universo — el «once» del tablero era seis

`FP-227` declara «Once de las 14 ya tienen R o no según `corridas-R/` — el acto
R-v1_2 censa cuáles faltan, no se asume aquí». Censado:

**6 de 14 ya tienen R** (`CIV-M-01`, `CIV-M-12`, `CIV-M-13`, `FAM-M-01`,
`TRA-M-03`, `TRA-M-07`) y se reutilizan sin duplicar. **8 no lo tienen.** El
tablero hizo bien en no fijar el número.

## 3 · Lote 1 · ENVIPE — tres R medidos

`CIV-M-02` (2013), `CIV-M-04` (2015), `CIV-M-10` (2021), variable `BP1_23`.

| celda | ola | R | EE | IC95 | n_efectivo | estratos | UPM |
|---|---|---|---|---|---|---|---|
| `CIV-M-02` | 2013 | **0.243400** | 0.006238 | — | 40 889 | 268 | 10 526 |
| `CIV-M-04` | 2015 | **0.243668** | 0.007484 | — | 39 286 | 238 | 9 477 |
| `CIV-M-10` | 2021 | **0.204934** | 0.004773 | — | 32 967 | 597 | 9 903 |

Tres comprobaciones, no una:

1. **Control positivo del mecanismo.** `--regresion CIV-M-01 CIV-M-12 CIV-M-13`
   sobre celdas ya existentes: **3 de 3 COINCIDE**, bit a bit en `R`, `EE_R`,
   `n_efectivo`, `n_estratos` y `n_upm_total`. El árbitro reproduce lo que ya
   estaba antes de que se le acepte lo nuevo.
2. **Cuadre aritmético.** `n_efectivo` = filas − (código 99 + blanco), exacto en
   las tres: 47 117−6 228=40 889 · 44 699−5 413=39 286 · 37 156−4 189=32 967.
3. **Coherencia de serie.** Con las tres nuevas dentro, la serie ENVIPE de no
   denuncia por miedo/desconfianza queda 2012 .2590 · **2013 .2434** ·
   **2015 .2437** · 2017 .2227 · 2019 .2347 · 2020 .2038 · **2021 .2049** ·
   2022 .2131 · 2023 .2081 · 2024 .1946. Ninguna nueva es atípica.

**Lo que la verificación por ola atrapó.** Las siete filas `CIV-M-*` previas
comparten codificación literal, así que heredar era lo cómodo. Se verificó cada
ola contra su propia fuente y **2013 y 2015, olas contiguas, NO comparten
nombres de diseño**: 2013 trae `EST`/`UPM` (`EST_DIS`/`UPM_DIS` ausentes) y 2015
trae `EST_DIS`/`UPM_DIS` (`EST` ausente). Heredar en cualquiera de las dos
direcciones habría apuntado a una columna inexistente. Catálogo de `BP1_23`
verificado idéntico en las tres olas: `fd_envipe2013.xlsx` (hoja `TMod_Vic`,
fila 291), `fd_envipe2015.pdf` (pág. 57), catálogo embebido
`catalogos/BP1_23.csv` (2021).

## 4 · Lote 2 · ENIGH + ENNViH — cero R, cuatro filas y un defecto

`FAM-M-05/06/07` + `DIN-M-01`. **0 de 4 R.** Las cuatro filas de
`codificacion-R` se escribieron igual, con el bloqueo nombrado y verificado
contra el microdato: es lo que le falta al mecanismo para que otro acto lo
cierre sin reabrir un solo payload.

- **`FAM-M-05/06/07`** — el marco declara el desenlace como **umbral**
  (`remesas > 0`) y `remesas` es monto continuo: 1 313 / 1 424 / 1 389 valores
  distintos en 2016 / 2018 / 2020. `parsea_codificacion_binaria` sólo reconoce
  conjuntos literales y `estima()` compara pertenencia, no orden. El árbitro
  se abstuvo con el motivo exacto. Correcto: enumerar ~1 300 montos daría un
  número hoy y se rompería en silencio mañana.
- **`DIN-M-01`** — bloqueo doble: `ehh02dta_all.zip` es 137 de 137 miembros
  `.dta` y `correr-R.py` sólo tiene `csv_zip`/`dbf_zip`; y el ponderador
  (`fac_3b`) vive en otro payload con JOIN por `folio`+`ls`, que
  `calcula_desde_tabla` rechaza. Ni `iiib_cr.dta` ni `ehh02w_b3b.dta` traen
  estrato ni UPM: el diseño sólo existe en prosa en `ennvih_diseno/*.pdf`.

### Hallazgo · el árbitro elige lector por sufijo y una celda que PARA sí tumba el lote

`DIN-M-01` no se abstuvo: **reventó**. `tools/arbitra.py:294` decide con una
dicotomía sobre el nombre — `dbf_zip(...) if miembro.endswith(".dbf") else
csv_zip(...)` — así que todo lo que no es `.dbf` se asume CSV. Un `.dta`
(primeros bytes `b'q\x01\x01R\x001\x00\x00MZVERSIO'`) entra a `csv.DictReader`,
el resto de fila cae en `restkey` como **lista**, y `correr-R.py:25` llama
`.strip()` sobre la lista → `AttributeError`.

Lo grave no es el diagnóstico ilegible, sino que la excepción **escapa de
`produce()`**, que imprime sólo al terminar toda la lista: la corrida del lote
completo no imprimió **ni una** de las tres abstenciones limpias que ya había
calculado. Es decir, **una celda que PARA sí tumba el lote** — justo lo que el
encargo dice que no debe pasar. Se detecta corriendo, no leyendo: hace falta un
payload que no sea `.csv` ni `.dbf`, y `DIN-M-01` es el primero que llega.

**No se reparó**: `arbitra.py` y `correr-R.py` están fuera del perímetro. La
reparación mínima cabe en dos líneas y es otro acto. Se declara además que
`pandas` y `pyreadstat` están disponibles en esta caja y el cálculo de las
cuatro celdas sería trivial con cualquiera de los dos — **no se tomó ese
atajo**, por lo que el propio encargo ordena: «Si te encuentras escribiendo
fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale
más que el atajo».

## 5 · Desviación declarada · nombre de los archivos de R

El encargo pide `corridas-R/R-<id>__v1_2.json`. `tools/arbitra.py` escribe
`corridas-R/<id>.json` por `escribe()` de `correr-R.py`, que está sellado y
fuera del perímetro. Se conservó el nombre nativo por dos razones: `--regresion`
y `correr-R.py` buscan `<id>.json`, así que con el sufijo **ningún acto futuro
podría re-verificar estos tres R**; y R es invariante de versión — los mismos
11 archivos ya servían a v1_1 y a v1_2, que es justo lo que el A.8 del encargo
afirma al decir «corridas-R 11/11 para v1_1 EXISTE-SATISFACE». Mesa decide si
renombrar.

## 6 · Contador y perímetro

**R marco-M: 11 → 14.** Filas de `codificacion-R`: 27 → 34 (+3 ejecutadas, +4
bloqueadas con causa). Celdas del sorteo v1_2 con R: 6 → 9 de 14. Sin R quedan
5: `FAM-M-05/06/07` y `DIN-M-01` (mecanismo) y `TRA-M-02` (contaminación).

Escrito: `codificacion-R-v1_0.tsv` (sólo filas nuevas), `corridas-R/` (3
archivos nuevos, ninguno existente tocado), `notas-arbitra/` (2), esta nota, el
tablero, `registro-rotulos`, la cascada. Nada fuera de esa lista.

**Ciego a M/L**: ninguna corrida ni lectura de este acto abrió `corridas-M/`,
`corridas-L/` ni `milpa/tramite.yaml` (salvo el `grep` de ids declarado en §0).

## 7 · Suite — ROJA por defecto preexistente, medido con control positivo

`python3 tests/check.py --baseline` en esta caja: **29 259 FAIL · 167 WARN ·
LÍNEA BASE ROJO, 29 240 entradas nuevas**. No se declara VERDE y no se sigue
sin reportarlo (`/acto` §6). Tres comprobaciones dicen que no es de este acto:

1. **Las 29 240 entradas nuevas son T27. Las 29 240.** Desglose por prueba
   sobre la sección posterior a la línea `LÍNEA BASE`: `29240 · T27:` y nada
   más. Cero entradas nuevas de cualquier otra prueba.
2. **T27 sólo escanea `data/`, y este acto no escribe nada ahí.**
   `git diff --name-only origin/main...HEAD | grep -c '^data/'` → **0**. Las
   29 244 líneas T27 nombran `data/raw/...`; **0** nombran
   `codificacion-R`, `corridas-R`, `notas-arbitra` o `MAESTRA34-L2`.
3. **Control positivo en árbol limpio.** Worktree nuevo en `origin/main`
   (`6d9692d`) **sin un solo commit de este acto**, en la misma caja y con la
   misma `data/raw` enlazada: **30 779 FAIL · 168 WARN · ROJO con 30 760
   entradas nuevas, 30 760 de 30 760 T27**. El árbol limpio sale **más rojo
   que el de este acto**.

Causa, ya conocida y no reparada:
`/home/pc0/mm-corpus/raw/raw -> /home/pc0/mm-corpus/raw` — **símlink
auto-referente**, creado el 12/ago/2026. El glob recursivo de T27 lo recorre
en bucle (`data/raw/raw/raw/...`) y multiplica cada archivo del corpus por
cada nivel. `/acto` §1.3 **obliga** a enlazar `data/raw`, así que esto le
ocurre a **todo acto de caja**; un acto de NUBE no lo ve porque ahí el corpus
no está montado — que es por lo que la línea base sellada dice 19 FAIL.

Este acto **no lo repara**: `data/` y el corpus compartido están fuera de su
perímetro, y borrar un símlink del corpus no es algo que un acto de árbitro
deba hacer de paso. Queda medido, con control positivo, para quien lo tome.
