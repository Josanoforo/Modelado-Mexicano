# `ACTO MAESTRA36-L14 · COERCITIVO-TRES-UNIVERSOS` — P0 · denominadores (COMMIT-1)

3/sep/2026 · UBUNTU · `/home/pc0/mm-l14-coercitivo` · base `18fd2bd` · encargo
archivado por `A.3` en `daabae2` (SHA de redacción `18fd2bd`).

> **«Los denominadores quedan congelados antes de dividir.»**
> Lo están. La spec —trimestre de corte, filtro, ponderador, los tres
> denominadores, el estimador de varianza, el numerador y su corrección de
> premisa, y la lista de incompatibilidades con su signo— vive entera en el
> encabezado de `tools/medidor_l14_coercitivo_universos.py`, en **este** commit,
> antes de que ninguna cifra agregada exista. `--censo` abrió el zip para leer
> estructura y verificar claves; **no sumó un solo `fac_tri`**.

## Perímetro

> **«Este acto sólo toca lo que el encargo enumera.»**
> `tools/medidor_l14_coercitivo_universos.py` ·
> `data/l14-coercitivo-universos-v1_0.json` · `data/INFRAESTRUCTURA-v1_0.md` ·
> `milpa/tramite-ola5-propuesta-v0.yaml` (append) · `forense/notas/…L14-*` ·
> `forense/hallazgos.md` · `forense/firmas-pendientes.tsv` · cascada.
> **No toca** `milpa/tramite.yaml`, `milpa/procedencia.yaml`,
> `data/manifiesto.yaml` ni `data/curacion-registro/**`.

## Trimestre de corte — el encargo dejó la elección a P0, y no la desempata la existencia

El encargo dice «2025-4T o 2026-1T, **el que exista con COE y SDEM**». **Los dos
existen** en el corpus, con `coe1`, `coe2`, `sdem`, `hog` y `viv` completos:

```
$ python3 - (namelist del zip)
conjunto_de_datos_enoe_2025_4t_csv.zip  →  coe1 coe2 hog sdem viv   (349 entradas)
conjunto_de_datos_enoe_2026_1t_csv.zip  →  coe1 coe2 hog sdem viv   (414 entradas)
```

El criterio de existencia no desempata, así que hace falta uno y se declara
**antes** de medir: **`2025-4T`**, porque su período de referencia (oct–dic 2025)
**contiene** el corte del numerador del SAT (`2025-12`, L13/`ADR-312`). Emparejar
un numerador de diciembre de 2025 con un denominador de enero–marzo de 2026
metería un desfase de un trimestre sin ninguna ganancia. **No se mide el otro
trimestre «para ver cuál sale mejor»**: la elección es previa y por razón, no
posterior y por resultado.

## Payload, por identidad

```
payload   data/raw/conjunto_de_datos_enoe_2025_4t_csv.zip
sha256    e4d4284cc9924a40c39544a5530715f320a5627cd81997214c0430827616d9d6  (manifiesto: IGUAL)
id        enoe_2025_4t_csv  (data/manifiesto.yaml, raíz data_raw)
tabla     conjunto_de_datos_sdem_enoe_2025_4t.csv — 167 361 793 bytes, 115 campos
```

El módulo abre **por sha256 contra el manifiesto**, no por nombre; si no calza, `PARO`.

## Códigos: leídos del diccionario y del catálogo del propio zip, no de memoria

Los nueve campos de la spec existen en el diccionario del zip, con su tipo:

| campo | tipo | rango | descripción |
|---|---|---|---|
| `r_def` | C | `00,15` | Resultado definitivo de la entrevista |
| `c_res` | C | `[1-3]` | P6 Condición de residencia |
| `eda` | C | `00-99` | P9 Edad |
| `clase2` | N | `[1-4]` | Clasificación en ocupada y desocupada; disponible y no disponible |
| `emp_ppal` | N | `[1-2]` | Clasificación de empleos formales e informales de la primera actividad |
| `pos_ocu` | N | `[1-5]` | Clasificación de la población ocupada por posición en la ocupación |
| `fac_tri` | N | `1-999999` | Ponderador trimestral |
| `upm` | C | `0000001-9999999` | Unidad primaria de muestreo |
| `est_d_tri` | C | `0001-9999` | Estrato de diseño trimestral |

Y las ocho claves que la spec usa se verifican contra el catálogo del zip
—**discordancia → `PARO`**, literal del encargo—:

```
r_def     0  Entrevista completa                      OK
c_res     1  Residente habitual                       OK
c_res     3  Nuevo residente                          OK
clase2    1  Población ocupada                        OK
emp_ppal  1  Empleo informal                          OK
emp_ppal  2  Empleo formal                            OK
pos_ocu   2  Empleadores                              OK
pos_ocu   3  Trabajadores por cuenta propia           OK
-> las 8 concuerdan; no hay PARO por catálogo.
```

La guardia **no es decorativa: disparó**. En su primera corrida el `PARO` saltó
con `clase2=1: spec «Poblacion ocupada» vs catalogo «PoblaciÃ³n ocupada»` — los
catálogos del zip vienen en **UTF-8** y el microdato en **latin-1**, y decodificar
todo con una sola codificación convierte un acento en un falso `PARO`. Se corrigió
el lector (`dec()`, UTF-8 con caída a latin-1) **antes** de este commit, no la
guardia. Queda anotado porque la clase de defecto —adivinar la codificación de un
payload ajeno— es reincidente en esta casa.

**Nota de nomenclatura, no discordancia:** el encargo escribe «`EST_D`»; el
diccionario del corpus no tiene ese campo, tiene `est_d_tri` (trimestral) y
`est_d_men` (mensual). Con ponderador **trimestral** el estrato que corresponde es
`est_d_tri`. No es una discordancia de código, es el nombre exacto leído de la
fuente, que es lo que el encargo manda pegar.

## Los tres denominadores, congelados

Filtro común (población en universo): `r_def == 0` · `c_res ∈ {1,3}` ·
`15 ≤ eda ≤ 98` · `clase2 == 1`. Total = suma de `fac_tri`.

- **(a) ocupados totales** — el filtro.
- **(b) informales** (`emp_ppal == 1`) y **formales** (`emp_ppal == 2`).
  Guardia de partición: `(a) − informales − formales` debe igualar el peso de
  `emp_ppal ∉ {1,2}`; si no cierra, `PARO`.
- **(c) formales no asalariados** (`emp_ppal == 2` **y** `pos_ocu ∈ {2,3}`),
  aproximación ENOE del «obligado»: excluye subordinados y remunerados (1), sin
  pago (4) y no especificado (5). Guardia: si `(c) ≥ formales`, el filtro
  `pos_ocu` no discrimina → `PARO`.

## IC95 por diseño

Estimador de **conglomerado último** sobre el diseño estratificado bietápico:
estrato = `est_d_tri`, UPM = `upm`.

```
v(Ŷ) = Σ_h  n_h/(n_h−1) · Σ_a (y_ha − ȳ_h)²        y_ha = total ponderado de la UPM
IC95 = Ŷ ± 1.95996 · √v
```

Los estratos con **una sola UPM** aportan `0` y **se cuentan** en el JSON: no se
colapsan en silencio. El `IC` de la razón `p = N/D` con `N` constante
administrativa se obtiene **invirtiendo** el del denominador — el límite inferior
de `p` usa el límite **superior** de `D` —; el numerador no aporta varianza porque
es un censo, no una muestra.

## Numerador: la premisa del encargo, corregida contra la fuente

El encargo pide «contribuyentes con e.firma **vigente** al corte». **La fuente no
dice eso.** `firelenumcontri` cuenta *primeras* e.firma emitidas, acumuladas desde
`2004-01`; el certificado caduca a los cuatro años y el acumulado **no da de baja**
a quien salió del padrón — L13 lo declaró así en su propio cierre. Se mide con la
premisa corregida y se escribe la consecuencia donde no se puede perder: **las
cuatro `p` de ENOE son cotas SUPERIORES de la adopción vigente**, igual que las
dos de L13. No se hereda el supuesto ajeno; se convierte en guardia declarada.

`N = 32 331 680`, corte `2025-12`, re-citado de `data/l13-sat-efirma-v1_0.json`.
`p_B` y `p_C` se re-citan de ahí también: **no se recalculan**, el encargo lo
prohíbe.

## Lo que este commit no hace

No divide. No emite veredicto ni evalúa tramo del falsador `B-bis`: **este acto
mide y no adjudica**. No toca el prior `0.91`/`0.09` `ASIGNADO` ni el tier
`MEDIA-FUERTE`. No descarga nada.
