# ENFIH 2019 · tenencia de Afore — pre-registro congelado de `CALC-ENFIH-0001`

### `prereg-caja-ENFIH-AFORE` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/ENFIH-AFORE-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-ENFIH-AFORE`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado **en NUBE y antes de abrir un solo byte de microdato**, de la corrida `CALC-ENFIH-0001`: la proporción ponderada de hogares con cuenta de ahorro para el retiro o Afore en ENFIH 2019, con IC95 **de diseño**. Releva `CORR-0012` (2 `RESULT`: `RES-0037`, `RES-0038`). |
> | **QUÉ NO ES** | No es un veredicto causal: `R1.2` dice *«empleo formal estable → planeación larga»* y esta corrida mide la **tasa base incondicional**, no la condicional. No mide formalidad laboral (no es construible en ENFIH, §3). No adopta ninguna cifra a `milpa/` — la adopción es de mesa. No corre el medidor: este acto congela el contrato, la corrida es de CAJA. |
> | **VERIFICAS ASÍ** | CAJA confirma, antes de calcular, que `TCONCENTRADORA.csv` trae exactamente las 88 columnas que el FD declara para `TConcentradora`, que `C_AFORE` no trae nulos y su soporte es `⊆ {0,1}`, y que `EDIS`/`UPM_DIS` están en **ese mismo archivo** y no se toman de `THOGAR.csv`. Si alguna falla, el `RESULT` correspondiente sale `NO-ESTIMABLE-*` y **no se elige otra columna sobre la marcha**. |

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1`, 15/sep/2026, entorno **NUBE** (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, `data/raw` ausente, corpus `montado=NO`, `archivos_examinados=0`), sobre `origin/main = f5a52272a8208eaf56f3b6d5db9531786d0d6534`.

**Regla consumidora:** `dinero.planeacion.formal_estable` (`R1.2`, `canon/modelo-decision-v4_0.md:732`), `milpa/tramite.yaml:897`, `situacion: SELLADA`, `tier: FUERTE`.

---

## 0 · A.8 — qué ya existe, con el comando al lado

```
$ python3 tools/ya_medido.py dinero.planeacion.formal_estable
  resuelto por canon: dinero.planeacion.formal_estable -> R1.2
  -- milpa/tramite.yaml --                 :897  situacion=SELLADA tier=FUERTE p=0.538502  [TASA-EJECUTADA]
  -- milpa/tramite-ola5-propuesta-v0.yaml -- :317  situacion=PENDIENTE-DE-MESA p=0.538502
  -- data/corrida0 (RESULT + ejecución + sello) -- (sin apariciones)
  -- forense/notas/*-L*-*.md --  2026-09-01-MAESTRA33-E18-P3-L1-spec.md:225
  ========================================
  MEDIDA-EN: tramite-ola5-propuesta-v0.yaml, tramite.yaml
```

Lectura, sin disfraz: la regla **ya tiene cifra** (`p = 0.538502`, GEN1) y
**no tiene ni un solo `CALC` en `data/corrida0`**. Eso es exactamente lo que
`CORR-0012` dice — `SIN-CANDIDATO-EN-EL-REGISTRO` — y lo que esta spec existe
para cerrar: no falta el número, falta la **cadena** (`E.2`).

Estructura previa que sí existe y que esta spec **no duplica**: la resolución
de variable, archivo y ponderador está congelada desde el 1/sep/2026 en
`forense/notas/2026-09-01-MAESTRA33-E18-P3-L1-spec.md` §Regla 2, y su medidor
en `tools/tasas_base_ola6_activos.py::regla2_afore`. Esta spec **la reverifica
contra los inventarios canónicos** (§1) y la eleva a las dos capas de `D-15`;
no la re-descubre ni la contradice.

---

## 1 · A.15 — los reactivos existen, verificados **por archivo**

### 1.1 · El payload, resuelto por manifiesto

| | |
|---|---|
| `payload_id` | **`enfih2019_bd_csv_zip`** |
| archivo | `enfih2019/enfih_2019_base_de_datos_csv.zip` |
| `sha256` | `be372533d5043920892142e8bf792b7293a5f20ab466a6441bc89925b42ef4d5` |
| bytes | 4 404 049 |
| raíz lógica | `data_raw` — **no** «está en data/raw» |

El codebook oficial es un payload aparte, también resuelto por manifiesto:
`enfih2019_fd_xlsx` → `enfih2019/enfih_2019_fd.xlsx`, `sha256
326b68b342797de45a7a4eb3dbf04f3790d11035df2611d7f9153d1ae12a48e1`, 202 396 bytes.

### 1.2 · Las secciones del instrumento, leídas del **índice del codebook**

`A.15(b)`: las secciones se listan del FD oficial, no de lo que el nombre de
la sección sugiere. Las 16 hojas del FD, con su conteo de variables:

```
$ python3 -c "…" data/inventario-fd-v1_1.tsv   # payload enfih2019/enfih_2019_fd.xlsx
  TAuto 19 · TBanca 16 · TComparte 14 · TConcentradora 88 · TDepar 16 ·
  TEduca 19 · TGrupal 19 · THogar 11 · TModulo 212 · TMoto 19 · TNomina 19 ·
  TPersonal 19 · TPropiedad 29 · TSDem 17 · TUnico 29 · TVivienda 118
  --- filas examinadas=27729  aciertos=664  secciones=16  (A.13)
```

Y el mismo conteo contra el **archivo real**, no contra el descriptor:

```
$ python3 -c "…" data/inventario-reactivos-v1_2.tsv  # payload enfih2019/…_csv.zip
  16 archivos miembro · 664 variables · TCONCENTRADORA.csv = 88 columnas
  --- filas examinadas=317718  aciertos=664  archivos_distintos=16  (A.13)
```

**664 = 664 y 88 = 88.** Descriptor y archivo coinciden en la sección que
esta spec usa. (Discrepancia menor declarada y **fuera de perímetro**:
`THogar` son 11 variables en el FD y `THOGAR.csv` trae 9 columnas reales.
Esta spec no abre `THOGAR.csv`, §2.3.)

### 1.3 · Las cuatro columnas, en **el archivo exacto**

Todas en `TCONCENTRADORA.csv` (miembro del ZIP de arriba), etiqueta verbatim
del FD, hoja `TConcentradora`:

| variable | etiqueta oficial (FD) | papel |
|---|---|---|
| **`C_AFORE`** | *«Condición de tenencia de cuenta de ahorro para el retiro o Afore»* | **desenlace** |
| **`FAC_HOG`** | *«FACTOR DE EXPANSIÓN»* | ponderador de hogar |
| **`EDIS`** | *«ESTRATO DE DISEÑO»* | estratificación del bootstrap |
| **`UPM_DIS`** | *«UNIDAD PRIMARIA DE MUESTREO DE DISEÑO»* | conglomerado que se re-muestrea |
| `H_PPAL` | *«Condición de hogar principal»* | filtro de la rama de robustez |
| `FOLIO` · `VIV_SEL` · `HOGAR` | *«Número de folio»* · *«Número de vivienda seleccionada»* · *«Número de Hogar»* | llave de hogar |

`A.15(c)` — **por qué esto no se verifica por nombre de variable.** `FAC_HOG`
existe **en dos archivos** de este mismo ZIP: `TCONCENTRADORA.csv` y
`THOGAR.csv`. No son intercambiables: son dos tablas con universos distintos.
El contrato fija el archivo, no sólo el nombre, y el medidor lee `FAC_HOG`
**de `TCONCENTRADORA.csv`**. Un medidor que resolviera «FAC_HOG» por nombre
podría tomar el de `THOGAR.csv` sin que nada se queje.

### 1.4 · El mapa de códigos de `C_AFORE`

`0` = No tiene · `1` = Sí tiene. **No se adivina** (`E.5` prohíbe adivinar
códigos para lograr un preflight verde): el catálogo está resuelto y
verificado contra el FD **y contra el dato** por `ACTO MAESTRA33-E18-P3`
(`forense/notas/2026-09-01-MAESTRA33-E18-P3-L1-spec.md:254`), que además
registra la corrección que importa: la tenencia es `C_AFORE` y **no**
`V_AFORE`, que es el **monto en pesos** (0 – 108 264 000). Un medidor que
hubiera leído «V_AFORE = indicador de tenencia» habría medido dinero.

`C_AFORE` ya es dicotómica: **no se recodifica**. Si el soporte observado no
es `⊆ {0,1}`, o trae nulos, el punto sale `NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA`
y la spec **no** decide sobre la marcha qué hacer con el código nuevo.

---

## 2 · Qué mide, exactamente

### 2.1 · Universo

Hogares: **todas** las filas de `TCONCENTRADORA.csv`, llave
`FOLIO + VIV_SEL + HOGAR`, **sin filtro adicional** — la regla no declara
ninguno. Entran las filas con `FAC_HOG` finito y `> 0`.

### 2.2 · Estimando

`A-P` = proporción ponderada de hogares con `C_AFORE == 1`:
`p = Σ(w·d) / Σ(w)`, `w = FAC_HOG`, `d = C_AFORE`, sumas en orden fijo de
llave. **DESCRIPTIVO.** El complemento `A-P-COMPLEMENTO` se cuenta
directamente sobre `d == 0`, **nunca** como `1 − p` — si los dos no suman 1
dentro de la tolerancia, hay filas fuera del mapa y el `RESULT`
`A-SUMA-UNO` lo dice.

### 2.3 · Lo que esta spec decide y GEN1 no decidió

1. **El IC nace de diseño, no de fila.** GEN1 selló
   `ic95 = [0.5267, 0.550616]` sin declarar un solo campo de diseño en la
   regla. `EDIS` y `UPM_DIS` **están en `TCONCENTRADORA.csv`** (§1.3):
   hay diseño que usar y esta corrida lo usa. Bootstrap de `UPM_DIS` con
   reemplazo **dentro de** `EDIS`, conservando el número de UPM por estrato,
   2 000 réplicas, `numpy.PCG64`, semilla `20260915`, percentiles 2.5/97.5.
   `A-DELTA-IC-VS-GEN1` mide, con signo, cuánto cambia la anchura.
2. **`EDIS`/`UPM_DIS` como llaves de texto opacas.** Cadena cruda, `dtype=str`.
   Nunca a entero, nunca re-rellenadas al ancho del descriptor: normalizarlas
   parte o fusiona estratos en silencio. El perfil de anchos sale como
   `RESULT` de texto.
3. **Estrato con UPM única no se colapsa ni se descarta.** Se re-muestrea a
   sí mismo (aporta varianza cero); si el conteo es `> 0`, `A-METODO-IC` sale
   `IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite inferior** de
   la anchura verdadera. Colapsar estratos es una decisión de diseño que esta
   spec no está autorizada a tomar.
4. **`FAC_HOG` se toma de `TCONCENTRADORA.csv`.** Declarado como decisión, no
   como detalle de implementación (§1.3). `THOGAR.csv` **no se abre**.
5. **La rama de robustez es secundaria y va rotulada.** `B-P` sobre
   `H_PPAL == 1` (hogar principal) es **sensibilidad de universo**, no el
   punto adoptable; `B-DELTA-VS-A` sale con signo.

### 2.4 · Lo que NO es construible, con su universo declarado

`R1.2` condiciona en *empleo formal estable*. La condicional **no es
construible en ENFIH 2019**: barrido de las 16 tablas / 664 columnas del
inventario, 0 aciertos de formalidad laboral (seguridad social, contrato,
prestaciones). `CAT_POS` (*«Categoría de posición en el trabajo»*, la más
cercana) **no es formalidad** — un empleado puede ser informal — y por eso
esta spec la emite como **descriptivo no sellado** (`C-*`), nunca como la
condicional. `A.4`: universo examinado = las 664 columnas de las 16 tablas de
`enfih2019_bd_csv_zip` en `data/inventario-reactivos-v1_2.tsv`, más las 664
del FD `enfih2019_fd_xlsx` en `data/inventario-fd-v1_1.tsv`, 15/sep/2026.
Esto **no** es un negativo nuevo: `milpa/tramite.yaml:899` ya lo declara
(«barrido 16 tablas / 664 columnas, 0 hits … control positivo AFORE 2 hits,
`#447`»); aquí se re-verifica con el comando, que es lo que faltaba.

---

## 3 · Control positivo y adopción

Contra la cifra GEN1 sellada, **calculada después de medir y por script**
(`E.1`): `A-P` vs `0.538502`, con `A-DELTA-VS-GEN1` **con signo**.
`A-REPRODUCE-GEN1 = REPRODUCE` sólo si `round(A-P, 6) == 0.538502`.
`NO-REPRODUCE` **no** autoriza tocar el medidor ni ajustar hacia atrás: se
reporta y la lectura es de mesa.

`A-ADOPCION` sale `LISTADO-PARA-MESA-REPRODUCE` / `-NO-REPRODUCE` /
`NO-ADOPTABLE-NO-ESTIMABLE`. **Este acto no escribe cita en `milpa/`.**

**Contaminación declarada (`ADR-46`).** Al congelar, la sesión ya había leído
`p = 0.538502`, `n = 17765`, el `ic95` GEN1 y la variante `H_PPAL = 1`
(`milpa/tramite.yaml:897-930`). No es ciega. Lo genuinamente desconocido al
congelar: cuántos estratos y UPM reales hay, cuántos estratos quedan con UPM
única, la anchura del IC de diseño frente al de GEN1, y el soporte observado
de `C_AFORE`. **Ninguna elección de variable, archivo, filtro ni ponderador
de esta spec viene de GEN1**: las cuatro columnas salen del FD y del
inventario por archivo (§1.3), y donde GEN1 y el archivo pudieran discordar,
manda el archivo.

---

## 4 · Lo que NO hace

No abre microdato · no corre el medidor (lo escribe el acto de CAJA a partir
de este contrato) · no mide formalidad laboral · no adopta ninguna cifra a
`milpa/` · no toca `CALC-EDER-0001` ni ningún CALC sellado · no promedia olas
(ENFIH 2019 es la única ola de ENFIH en el corpus) · no toca `CORR-0011`,
`CORR-0013` ni `CORR-0014`, que llevan spec propia en este mismo acto.
