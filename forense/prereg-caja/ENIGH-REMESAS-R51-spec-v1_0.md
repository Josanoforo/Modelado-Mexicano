# ENIGH 2022 · hogares que reciben remesas — pre-registro congelado de `CALC-ENIGH-0001`

### `prereg-caja-ENIGH-REMESAS-R51` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/ENIGH-REMESAS-R51-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-ENIGH-REMESAS-R51`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado **en NUBE y antes de abrir un solo byte de microdato**, de `CALC-ENIGH-0001`: la **celda de la regla** `familia.seguro.volatilidad_ausencia_estado` sobre ENIGH 2022 — proporción ponderada de hogares con `remesas > 0`, su complemento **contado directamente**, e IC95 de diseño. Releva `CORR-0011` (`RES-0035`, `RES-0036`). |
> | **QUÉ NO ES** | **No es una segunda medición del ensayo `B`.** `CALC-B-0001` ya midió esta misma cantidad sobre este mismo payload (§0.2) — y su propia spec sellada le prohíbe alimentar un veredicto (`T9`). Esta spec no re-abre esa prohibición: **nace del lado de la regla**, que es donde `CALC-B-0001` declaró no estar. No promedia olas, no ajusta tendencia, no extrapola, no mide 2012–2020. No adopta nada a `milpa/`. No corre el medidor. |
> | **VERIFICAS ASÍ** | CAJA confirma, antes de calcular, que **`remesas` trae cero nulos** (si no, `NO-ESTIMABLE-NULOS-INESPERADOS`), que `est_dis`/`upm` están presentes en cada fila válida, y que `A-P` y `A-P-COMPLEMENTO` suman 1 dentro de tolerancia. Si no suman, hay filas fuera del mapa y el `RESULT` `A-SUMA-UNO` lo dice en vez de taparlo con `1 − p`. |

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1`, 15/sep/2026, entorno **NUBE** (`cloud_default`, `data/raw` ausente, corpus `montado=NO`, `archivos_examinados=0`), sobre `origin/main = f5a52272a8208eaf56f3b6d5db9531786d0d6534`.

**Regla consumidora:** `familia.seguro.volatilidad_ausencia_estado` (`R5.1`, `canon/modelo-decision-v4_0.md:751`), `milpa/tramite.yaml:863`, `situacion: SELLADA`, `tier: FUERTE`.

---

## 0 · A.8 — qué ya existe, y por qué esta spec no es un duplicado

### 0.1 · La salida de la herramienta, cruda

```
$ python3 tools/ya_medido.py familia.seguro.volatilidad_ausencia_estado
  resuelto por canon: familia.seguro.volatilidad_ausencia_estado -> R5.1
  -- milpa/tramite.yaml --  :863  situacion=SELLADA tier=FUERTE p=0.045694  [TASA-EJECUTADA]
  -- milpa/tramite-ola5-propuesta-v0.yaml -- :267  p=0.045694
  -- data/corrida0 (RESULT + ejecución + sello) --
     data/corrida0/CALC-B-0001/resultados.json:41  resultado_id=RESULT-B-ENIGH-2022-P
        ejecutado=SI  sello=VALIDO   RESULT-B-ENIGH-2022-P = 0.04569409956405095
  -- canon/modelo-decision-v4_0.md §7 -- :751  R5.1 | L249 | ... | [FUERTE] | Sí
  -- forense/notas/*-L*-*.md -- 2026-09-01-MAESTRA33-E18-P3-L1-spec.md:77
  ========================================
  MEDIDA-EN: tramite-ola5-propuesta-v0.yaml, tramite.yaml
```

### 0.2 · `EXISTE-NO-SATISFACE`, y exactamente por qué

`CALC-B-0001` (`ACTO GEN2-C0-B`, spec sellada `prereg-caja-B-REMESAS`) **ya
produjo**, con sello válido y sobre `enigh2022_nc_csv`:

| `RESULT` | valor |
|---|---|
| `RESULT-B-ENIGH-2022-P` | `0.04569409956405095` |
| `RESULT-B-ENIGH-2022-IC-LO` / `-IC-HI` | `0.043772848428537396` / `0.047770249605883566` |
| `RESULT-B-ENIGH-2022-N` | `90102` |
| `RESULT-B-ENIGH-2022-N-NULOS-REMESAS` | `0` |
| `RESULT-B-ENIGH-2022-N-SIN-DISENO` | `0` |

Y su propio `spec.yaml` declara, verbatim:

> `tipo: ENSAYO-LINEA-BASE-TEMPORAL-B` · `cuenta_gen2: PENDIENTE-DE-MESA`
> `reglas_bajo_prueba: "NINGUNA. R5.1 / familia.seguro.volatilidad_ausencia_estado NO se mueve: este CALC no la falsa ni la re-calibra. T9, verbatim: es modelo nuevo y ninguna cifra suya entra a un veredicto."`

**Lectura, sin adorno:** el número existe y no puede usarse. El bloqueo de
`CORR-0011` **no es de medición: es de autorización**, y lo puso una firma de
mesa (`T9`) sobre un ensayo cuyo objeto era otro (probar el selector `B`).
Esta spec no levanta esa firma ni discute el ensayo: **abre la corrida que
`T9` dejó vacante** — la celda de la regla, con su propia cadena `E.2`, su
complemento contado y su propia vía de adopción.

### 0.3 · Lo que esta corrida añade y el ensayo no tiene

1. **El complemento contado directamente.** `RES-0036` (`no_recibe_remesas`,
   `0.954306`) es `DERIVADO·q=1−p` en GEN1. `CALC-B-0001` **no** emite ningún
   complemento. Aquí `A-P-COMPLEMENTO` se cuenta sobre `d == 0` y
   `A-SUMA-UNO` verifica el cierre: si no suman 1, hay filas fuera del mapa
   — y con `1 − p` eso es invisible por construcción.
2. **Una reejecución independiente de un número GEN2.** El diagnóstico que
   motivó `v2.13` midió *«0 reproducciones por reejecución independiente en
   seis semanas»*. `A-REPLICA-B0001` compara `A-P` contra
   `0.04569409956405095` con la tolerancia declarada. **Ojo con el
   vocabulario (`E.3`):** código distinto sobre el mismo dato da
   `REPLICA-RESULTADO`, **no** `REPRODUCE`. La spec no confunde los dos ejes.
3. **Un camino de adopción.** `CALC-B-0001` no lo tiene y no puede tenerlo.

---

## 1 · A.15 — los reactivos existen, verificados **por archivo**

### 1.1 · El payload, resuelto por manifiesto

| | |
|---|---|
| `payload_id` | **`enigh2022_nc_csv`** |
| archivo | `enigh2022_nc_csv.zip` |
| `sha256` | `3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06` |
| bytes | 90 030 937 |
| raíz lógica | `data_raw` |

### 1.2 · El archivo miembro, y por qué el nombre **no** se infiere

La tabla interna **cambia de nombre entre series** de ENIGH, y adivinarlo es
un error ya pagado: 2012/2014 (serie `ncv`) usan
`concentradohogar_enigh<AAAA>ncv/conjunto_de_datos/concentradohogar.csv`;
2016–2022 (Nueva Serie, `_ns`) usan el patrón largo. Para 2022, el miembro es,
verbatim del inventario:

```
conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/
    conjunto_de_datos_concentradohogar_enigh2022_ns.csv
```

y en el **mismo ZIP** viven el codebook y el metadato que `E.5` autoriza a
abrir — y sólo ellos:

```
conjunto_de_datos_concentradohogar_enigh2022_ns/diccionario_de_datos/
    diccionario_datos_concentradohogar_enigh2022_ns.csv
conjunto_de_datos_concentradohogar_enigh2022_ns/metadatos/metadatos_enigh_2022_ns.txt
conjunto_de_datos_concentradohogar_enigh2022_ns/catalogos/{clase_hog,educa_jefe,
    est_socio,sexo,tam_loc,ubica_geo}.csv
```

### 1.3 · Las seis columnas, en **ese** archivo

```
$ python3 -c "…" data/inventario-reactivos-v1_2.tsv   # payload enigh2022_nc_csv.zip
  …|3b2b0bc9c953|conjunto_de_datos_concentradohogar_eni…|est_dis  |
  …|3b2b0bc9c953|…                                      |factor   |
  …|3b2b0bc9c953|…                                      |foliohog |
  …|3b2b0bc9c953|…                                      |folioviv |
  …|3b2b0bc9c953|…                                      |remesas  |
  …|3b2b0bc9c953|…                                      |upm      |
  --- filas examinadas=317718  aciertos=6  archivos_distintos=1  (A.13)
```

El `sha256_12` del inventario (`3b2b0bc9c953`) **coincide** con el prefijo del
`sha256` del manifiesto: el inventario se derivó del mismo archivo que la
corrida va a abrir, no de otro con el mismo nombre (`A.7`).

| variable | papel | mapa |
|---|---|---|
| **`remesas`** | **desenlace** — ingreso corriente monetario del hogar por remesas | numérica; `recibe_remesas = 1` si `remesas > 0`, `0` si `remesas == 0` |
| **`factor`** | ponderador de hogar de la Nueva Serie | flotante tal cual |
| **`est_dis`** | estrato de diseño | llave de **texto opaca** |
| **`upm`** | unidad primaria de muestreo | llave de **texto opaca** |
| `folioviv` + `foliohog` | llave de hogar | — |

**La rama NA no existe, y no se fabrica.** Verificado en las seis olas por
`ACTO MAESTRA33-E18-P3` (`forense/notas/2026-09-01-MAESTRA33-E18-P3-L1-spec.md:107-118`)
y re-confirmado por el ensayo `B` en 2022 (`RESULT-B-ENIGH-2022-N-NULOS-REMESAS = 0`):
el hogar sin remesas trae `0`, no vacío. Si esta corrida encuentra un nulo,
**para**: `NO-ESTIMABLE-NULOS-INESPERADOS`. `CERO NUNCA SUSTITUYE FALTA DE DATO`.

### 1.4 · El ponderador no se hereda de la serie

`A.15(c)`, caso medido: el encargo que originó el barrido de 2026-09-01
declaró `factor` para las seis olas; **en 2012 y 2014 esa columna no existe**
— el nombre es `factor_hog`. Esta spec mide **sólo 2022**, donde la columna
verificada por archivo es `factor` (§1.3). Ninguna otra ola entra, y el
nombre del ponderador de otra ola **no se extrapola a ésta**.

---

## 2 · Qué mide, exactamente

### 2.1 · Universo

Hogares: universo **completo** de `concentradohogar` de ENIGH 2022 Nueva
Serie, llave `folioviv + foliohog`, **sin filtro adicional** — la regla no
declara ninguno, y el `SI` de §3.5 es **circular con el desenlace** (incluye
*«hogar con remesas»* entre sus disparadores para medir *recibir remesas*).
Medir `p(remesas | remesas)` sería vacuo: lo que se mide es la **tasa base**.
Esto no es un hallazgo de esta spec — `milpa/tramite.yaml:865` ya lo declara
—; se re-declara aquí porque un lector del contrato no tiene por qué ir a
buscarlo.

Entran las filas con `factor` finito y `> 0` y `remesas` no nula.

### 2.2 · Estimando

`A-P` = `Σ(w·d)/Σ(w)` con `w = factor`, `d = 1[remesas > 0]`, sumas en orden
fijo de llave. **DESCRIPTIVO.** `A-P-COMPLEMENTO` se cuenta sobre `d == 0`.
Ningún `RESULT` es causal: la regla dice *«volatilidad/ausencia de Estado →
familia como seguro»* y esto es la prevalencia del desenlace, no la flecha.

### 2.3 · Diseño

Bootstrap de `upm` con reemplazo **dentro de** `est_dis`, conservando el
número de UPM por estrato, 2 000 réplicas, `numpy.PCG64`, semilla `20260915`,
percentiles 2.5/97.5. `est_dis`/`upm` como **cadena cruda** (`dtype=str`):
nunca a entero, nunca re-rellenadas. Estrato con UPM única se re-muestrea a
sí mismo, **no se colapsa ni se descarta**; si el conteo es `> 0`,
`A-METODO-IC = IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite
inferior** de la anchura verdadera.

Nota de reproducibilidad, declarada porque cambia el resultado y no la
intención: la semilla y el número de réplicas de esta spec **difieren** de las
del ensayo `B` (10 000 réplicas, semilla 42). Por eso `A-REPLICA-B0001` se
juega **sobre el punto**, nunca sobre los extremos del IC: dos bootstraps con
semillas distintas no tienen por qué coincidir en el quinto decimal del IC, y
pedirlo sería fabricar un falso `NO-REPRODUCE`.

---

## 3 · Control positivo y adopción

Dos comparaciones **calculadas después de medir y por script** (`E.1`), que
no se colapsan:

| `RESULT` | contra qué | vocabulario |
|---|---|---|
| `A-DELTA-VS-GEN1` | `0.045694` (GEN1, `milpa/tramite.yaml:863`) | delta con signo |
| `A-REPRODUCE-GEN1` | `round(A-P, 6) == 0.045694` | `REPRODUCE` / `NO-REPRODUCE` |
| `A-DELTA-VS-B0001` | `0.04569409956405095` (`CALC-B-0001`, GEN2) | delta con signo |
| `A-REPLICA-B0001` | `|A-P − 0.04569409956405095| <= 1e-10` | `REPLICA-RESULTADO` / `NO-REPLICA` — **nunca** `REPRODUCE` (`E.3`: mismo resultado con otro código es réplica) |

`A-ADOPCION` sale `LISTADO-PARA-MESA-REPRODUCE` / `-NO-REPRODUCE` /
`NO-ADOPTABLE-NO-ESTIMABLE`. **Este acto no escribe cita en `milpa/`.**

**Contaminación declarada (`ADR-46`).** Al congelar, la sesión ya había leído
la serie GEN1 completa de seis olas con sus IC (`milpa/tramite.yaml:850-900`),
los `RESULT` de `CALC-B-0001` y la spec sellada `prereg-caja-B-REMESAS`. **No
es ciega, y en el caso de `B` ni siquiera podría serlo**: leer `CALC-B-0001`
es precisamente lo que `A.8` obliga a hacer antes de escribir esta spec. Lo
genuinamente desconocido al congelar: cuántos estratos con UPM única hay en
2022, la anchura del IC bajo **esta** semilla, y si `A-P` replica el punto del
ensayo en la décima cifra o sólo en la sexta.

---

## 4 · Lo que NO hace

No abre microdato · no corre el medidor (lo escribe el acto de CAJA a partir
de este contrato) · no mide 2012, 2014, 2016, 2018 ni 2020 · no promedia olas
ni toca `serie_olas` · no levanta la restricción `T9` sobre `CALC-B-0001` ni
reinterpreta su spec sellada · no adopta cifra alguna a `milpa/` · no toca
`CORR-0012`, `CORR-0013` ni `CORR-0014`, que llevan spec propia en este mismo
acto.
