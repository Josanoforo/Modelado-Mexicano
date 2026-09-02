# ACTO MAESTRA34-L5 · P4 · `dinero.ahorro.tiene_ahorros` — SPEC CONGELADA (re-medición)

**COMMIT-1 de la pieza P4.** Se escribe **antes de calcular ningún desenlace**.
De ENIF 2024 se han tocado hasta aquí: el descriptor `enif_2024_fd.xlsx` (hoja
`TMODULO`, 1 579 filas), la lista de 398 columnas de `TMODULO.csv`, el rango de
`EDAD_V` (18-98), la suma de `FAC_PER` (94 221 441) y el conteo de filas con
respuesta no-blanca en la sección 5 (13 502 de 13 502). **No se ha calculado
ninguna proporción de ahorro** (P0 · §5).

**Firma que la autoriza:** DS1 de mesa, 2/sep/2026, citada por el encargo.

**Lo que se re-mide** (`milpa/tramite.yaml:285-303`): la regla ya está **MEDIDA**,
no ASIGNADA — `tiene_ahorros p=0.174804`, `clase MEDIDO·p(tasa base ponderada)`,
IC95 [0.159250, 0.190543], n=6 028, ola de calibración **ENNViH ola 2 (2005-06)**,
ponderador `fac_3b`. Esta pieza **no la refuta ni la sustituye**: añade la ola
2024 y conserva la de 2005-06.

---

## §1 · Spec

### 1.1 Payload y tabla

| campo | valor |
|---|---|
| payload | `data/raw/enif_2024_bd_csv.zip` · id de manifiesto `enif_2024_enif_2024_bd_csv` (`data/manifiesto.yaml:5427`) · `sha256 = 00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` |
| tabla | `TMODULO.csv` (módulo de la persona elegida) |
| encoding | `latin-1` |
| unidad de análisis | **PERSONA elegida**, 18 años y más |

### 1.2 Universo

Las **13 502 personas elegidas** de `TMODULO.csv`, con `EDAD_V` entre 18 y 98 —
es decir, **adultos 18+**, que es lo que el encargo pide («sobre adultos»). No se
trunca por edad superior. La corrida **PARA** si aparece alguna `EDAD_V` menor de
18, si `FAC_PER` no es numérico positivo en toda fila, o si alguna persona tiene
las 15 variables de la sección 5 en blanco.

### 1.3 Definición de `tiene_ahorros` — la que fija este censo

ENIF 2024 tiene la **sección 5 · AHORRO INFORMAL Y FORMAL**, con dos baterías
binarias (`1` Sí · `2` No · `b` blanco por secuencia), todas referidas al periodo
**junio 2023 – fecha de levantamiento (12 meses)**:

**Informal — `P5_1_1..P5_1_6`** («¿usted…»): ahorró prestando dinero · ahorró
comprando animales o bienes · guardó dinero en una caja de ahorro del trabajo o de
personas conocidas · guardó dinero con familiares o personas conocidas · participó
en una tanda · guardó dinero en su casa.

**Formal — `P5_6_1..P5_6_9`** («¿guardó o ahorró en su…»): cuenta o tarjeta de
nómina · de pensión · para recibir apoyos de gobierno · cuenta de ahorro · cuenta
de cheques · depósito a plazo fijo · fondo de inversión · cuenta contratada por
Internet o aplicación no bancaria (Mercado Pago, Nu, Spin) · otro tipo de cuenta.

```
tiene_ahorros = 1  ⟺  alguna de las 15 variables vale '1'
tiene_ahorros = 0  en caso contrario
```

Es la **unión formal ∪ informal** que el encargo manda. El blanco por secuencia en
`P5_6_*` (quien no tiene la cuenta correspondiente) cuenta como **no** haber
ahorrado por esa vía, que es su lectura correcta: sin cuenta no hay ahorro en esa
cuenta.

### 1.4 Ponderador, diseño e intervalo

| campo | valor |
|---|---|
| ponderador | **`FAC_PER`** — factor de expansión a nivel persona |
| estrato · UPM | `EST_DIS` · `UPM_DIS` |
| IC95 | bootstrap **conglomerado estratificado**, `n_boot = 10 000`, `seed = 42`, con `wprop_ic_conglomerado` |
| escala | proporción en [0, 1] |

La medición de 2005-06 usó `wprop_ic_bootstrap` (**sin** conglomerado). Se declara
la diferencia de estimador; no se recalcula la pieza ajena.

### 1.5 Sensibilidades pre-declaradas

- **A** · solo **formal** (`P5_6_1..P5_6_9`).
- **B** · solo **informal** (`P5_1_1..P5_1_6`).

Se declaran para que la unión sea auditable: quien quiera saber cuánto de la cifra
viene de cada mitad, lo tiene sin volver al microdato.

### 1.6 Las dos no-comparabilidades con 2005-06 — **congeladas antes de medir**

Esta pieza produce una segunda entrada de la misma regla. **No forma una serie
temporal con la primera**, por dos razones independientes, y ninguna de ellas se
puede corregir con más cuidado estadístico:

1. **Acervo contra flujo.** 2005-06 midió `cr27`, «¿Tiene ahorros?» — un **acervo**
   al momento de la entrevista (1=Sí / 3=No; `forense/notas/2026-08-24-cal-g3-puntual-cierre.md:38`).
   ENIF 2024 pregunta si **ahorró o guardó en los últimos 12 meses** — un **flujo**.
   Son cantidades distintas: alguien puede haber ahorrado durante el año y no tener
   nada guardado hoy, y al revés.
2. **Universo.** La nota de cierre de 2005-06 dice de su propio universo, textual:
   «No es "México", no es "los adultos de México": es la intersección de
   panel-retenido × módulo-aplicable × respuesta-sustantiva en ambas mediciones»
   (n=6 028, ponderador `fac_3b`). ENIF 2024 es una muestra nacional de adultos 18+
   con expansión a 94 millones de personas.

**Consecuencia sobre el criterio de refutación, decidida ahora y no cuando se vea
el número:** aunque la cifra de 2024 exceda el doble o la mitad de 0.174804,
**eso NO dispara `REFUTADA-POR-DATO`**. Dos definiciones distintas sobre dos
universos distintos no se refutan entre sí; una diferencia entre ellas mide la
diferencia de definición y de universo, no un cambio en México. La entrada nueva
se propone como **enmienda de re-medición con ola declarada**, y la de 2005-06 se
conserva íntegra.

### 1.7 Reactivo alterno examinado y descartado como principal

`P4_10` («si dejara de recibir ingresos, ¿por cuánto tiempo podría cubrir sus
gastos con sus ahorros?») es el análogo de **acervo** más cercano a `cr27` y
resolvería la no-comparabilidad (1). Se descarta como principal porque su código
`1` fusiona «menos de una semana» con «no tiene ahorros», de modo que **no separa
tener de no tener**. Queda anotado por si mesa quiere abrir una pieza de acervo;
el encargo fija «formal ∪ informal» y eso es lo que se mide.

---

## §2 · Sello

**El primer resultado que produzca este procedimiento es el que se reporta.**

---

## §3 · RESULTADO (COMMIT-2 de la pieza)

Corrida: `python3 tools/medidor_ahorro_enif24.py`.
Payload `data/raw/enif_2024_bd_csv.zip`,
`sha256 = 00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039`.
Las tres guardias de §1.2 pasaron: ninguna `EDAD_V` menor de 18 (rango 18-98),
`FAC_PER` numérico positivo en las 13 502 filas, ninguna persona con las 15
variables de la sección 5 en blanco.

### 3.1 Principal

| campo | valor |
|---|---|
| estimando | proporción de adultos 18+ que ahorró o guardó dinero, formal **o** informalmente, entre junio de 2023 y el levantamiento |
| **p̂** | **0.642080** |
| **IC95** | **[0.630602, 0.653440]** |
| n | 13 502 personas · con ahorro 8 699 |
| estratos · UPM | 190 · 2 164 |
| población expandida | 94 221 441 adultos |
| ponderador | `FAC_PER` |

### 3.2 Sensibilidades pre-declaradas

| variante | p̂ | IC95 | n con ahorro |
|---|---|---|---|
| **A** · solo **formal** (`P5_6_1..9`) | 0.284927 | [0.273502, 0.296342] | 4 078 |
| **B** · solo **informal** (`P5_1_1..6`) | 0.561920 | [0.549922, 0.573502] | 7 590 |

Esta descomposición es el resultado más informativo de la pieza, y no estaba
buscada: **el ahorro informal casi duplica al formal** (0.562 contra 0.285), con
intervalos que no se traslapan ni de lejos. De la unión (0.642) se sigue que
**0.205 de los adultos ahorran por ambas vías** y que **0.357 ahorran únicamente
por vías informales** — tandas, guardar en casa, con familiares, cajas de ahorro.
Es apoyo directo para la familia de reglas `dinero.ahorro.informal_sin_puente` /
`con_puente_y_respaldo` del modelo, que hoy no tienen `p` medida; esta pieza **no**
las mide ni las reclama, solo deja anotado dónde está el dato.

### 3.3 Frente a la cifra de 2005-06 — **no es una serie, y no hay refutación**

| | ola | definición | universo | p |
|---|---|---|---|---|
| vigente | ENNViH ola 2 (2005-06) | `cr27` «¿tiene ahorros?» — **acervo** | panel retenido, n=6 028, `fac_3b` | 0.174804 |
| **nueva** | **ENIF 2024** | ahorró en **12 meses** — **flujo** | nacional 18+, n=13 502, `FAC_PER` | **0.642080** |

La razón aritmética es **3.67×**, es decir, **excede el umbral de «más del doble»**
del encargo. **No dispara `REFUTADA-POR-DATO`**, y esto no es una concesión hecha
al ver el número: quedó congelado en §1.6 de esta misma spec, escrito antes de
medir, con sus dos razones —acervo contra flujo, y universo panel-retenido contra
muestra nacional—. Una diferencia entre dos definiciones sobre dos universos mide
la diferencia de definición y de universo, no un cambio en México.

Que el orden de magnitud sea el que es no debería sorprender: preguntar «¿guardó
algo de dinero en algún momento del último año, aunque fuera en su casa?» tiene
que dar mucho más que preguntar «¿tiene usted ahorros?». La comparación que sí
valdría —acervo contra acervo— requeriría un reactivo que ENIF 2024 no tiene
limpio (`P4_10` fusiona «menos de una semana» con «no tiene ahorros», §1.7).

**Propuesta a mesa:** entrada nueva con ola declarada, tier `PENDIENTE-DE-MESA`,
**conservando íntegra** la entrada de 2005-06, y con la no-comparabilidad escrita
dentro del propio YAML para que no se pierda al citarla.
