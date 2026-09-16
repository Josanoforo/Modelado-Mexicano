# ENUT 2024 · reparto de las horas de cuidado del hogar — pre-registro congelado de `CALC-ENUT-0001`

### `prereg-caja-ENUT-CUIDADO` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/ENUT-CUIDADO-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-ENUT-CUIDADO`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado **en NUBE y antes de abrir un solo byte de microdato**, de `CALC-ENUT-0001`: el **estimador de razón** `Σ w·(horas de cuidado de mujeres 40+) / Σ w·(horas de cuidado totales del hogar)` en ENUT 2024, con IC95 de diseño. Releva `CORR-0014` (`RES-0045`). |
> | **QUÉ NO ES** | No es una proporción de un binario — es una **razón**, y su bootstrap es otro (§2.3). No es el contraste por ocupación de `Y1`/`Y5` (4/ago/2026): mide reparto, no reducción. No adopta nada a `milpa/`. No corre el medidor. No re-abre el `veredicto_acotado` de mesa (`ACOTADA-EN-EDAD`, firma c1, 2/sep/2026). |
> | **VERIFICAS ASÍ** | CAJA confirma, antes de calcular, que `EST_DIS`/`UPM_DIS` son **constantes dentro de `LLAVEHOG`** (si no, el conglomerado del hogar no está definido y la razón sale `NO-ESTIMABLE-DISENO-NO-CONSTANTE`), que ningún hogar de `tvar_crea.csv` queda sin `FAC_HOG`, y —lo que ninguna corrida anterior comprobó— que **`FAC_HOG` de `tsdem.csv` y `FAC_HOG` de `thogar.csv` coinciden hogar por hogar** (§1.4). |

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1`, 15/sep/2026, entorno **NUBE** (`cloud_default`, `data/raw` ausente, corpus `montado=NO`, `archivos_examinados=0`), sobre `origin/main = f5a52272a8208eaf56f3b6d5db9531786d0d6534`.

**Regla consumidora:** `familia.cuidado.recae_mujeres_40mas` (`R5.2`, `canon/modelo-decision-v4_0.md:752`), `milpa/tramite.yaml:1024`, `situacion: hogar_con_carga_de_cuidado`, `tier: FUERTE`, `alcance: ACOTADA-EN-EDAD`.

---

## 0 · A.8 — qué ya existe

```
$ python3 tools/ya_medido.py familia.cuidado.recae_mujeres_40mas
  resuelto por canon: familia.cuidado.recae_mujeres_40mas -> R5.2
  -- milpa/tramite.yaml -- :1024  situacion=hogar_con_carga_de_cuidado tier=FUERTE
       veredicto=DISCRIMINA  p=0.221500  [CORROBORADA]
  -- milpa/tramite-ola5-propuesta-v0.yaml -- (sin apariciones)
  -- data/corrida0 (RESULT + ejecución + sello) -- (sin apariciones)
  -- canon/modelo-decision-v4_0.md §7 -- :752  R5.2 | L250 | ... | [FUERTE] | Sí
  -- forense/notas/*-L*-*.md --
       2026-09-02-MAESTRA35-L7-P0-censo.md:40,189
```

Cero `CALC`. El medidor y la spec congelada **sí existen** desde el
2/sep/2026 (`tools/medidor_cuidado_enut.py`,
`forense/notas/2026-09-02-MAESTRA35-L7-spec.md`), y de ahí sale la
operacionalización que esta spec reverifica y eleva a `D-15`. **Nada de lo de
abajo se descubre aquí por primera vez salvo §1.4**, que es una guarda nueva.

---

## 1 · A.15 — los reactivos existen, verificados **por archivo**

### 1.1 · Payload y codebook, resueltos por manifiesto

| | `payload_id` | archivo | `sha256` |
|---|---|---|---|
| microdato | **`enut2024_bd_csv`** | `enut2024_bd_csv.zip` | `25f35626464053441b367b24001d255dbca408b5f576e614e0e09ac58691c4ba` |
| codebook | `enut2024_fd_xlsx` | `enut2024_fd.xlsx` | `4a7dddf1bc0612f5e72694b146848804edc47d8f00c86e7d34d1cfb8f5ec3f58` |

### 1.2 · Las secciones, del índice del codebook — y el conteo que cuadra

El FD de ENUT indexa **varias olas en el mismo libro**, y las hojas se llaman
casi igual: `THOGAR` (60 variables) es la de **2024**; `THogar` (52) es la de
2019. Tomar la hoja por parecido de nombre es exactamente el defecto que
`A.15(b)` nombra. Las hojas de 2024, contra los archivos reales del ZIP:

| hoja del FD | variables en el FD | archivo real | columnas reales |
|---|---|---|---|
| `TVAR_CREA` | 60 | `tvar_crea.csv` | **60** |
| `THOGAR` | 60 | `thogar.csv` | **60** |
| `TSDEM` | 33 | `tsdem.csv` | — (no se cuenta aquí: sólo se leen 2 columnas) |
| `TMODULO` | 694 | `tmodulo.csv` | — (no se abre) |

```
--- filas examinadas=27729  aciertos=1813  secciones=11  (A.13, inventario-fd-v1_1)
--- filas examinadas=317718 (A.13, inventario-reactivos-v1_2)
```

### 1.3 · Las columnas, en `tvar_crea.csv`, etiqueta verbatim del FD

| variable | etiqueta oficial (FD, hoja `TVAR_CREA`) | papel |
|---|---|---|
| `CUID_ESP_INT_HOG_CON_CP` | *«Cuidados especiales a integrantes del hogar por enfermedad crónica, temporal o discapacidad, con cuidados pasivos»* | sumando 1/4 de horas |
| `CUID_INT_0A5_CON_CP` | *«Cuidado a integrantes del hogar de 0 a 5 años, con cuidados pasivos»* | sumando 2/4 |
| `CUID_INT_6A14_CON_CP` | *«Cuidado a integrantes del hogar de 6 a 14 años, con cuidados pasivos»* | sumando 3/4 |
| `CUID_INT_60MAS_CON_CP` | *«Cuidado a integrantes del hogar de 60 años y más, con cuidados pasivos»* | sumando 4/4 |
| `SEXO` | *«3.4 (NOMBRE) es hombre (NOMBRE) es mujer»* | `'1'` hombre · `'2'` mujer |
| `EDAD` | *«3.5 ¿Cuántos años cumplidos tiene (NOMBRE)?»* | corte 40+ |
| `FAC_PER` | *«Factor»* | ponderador de persona (D1) |
| `EST_DIS` | *«Estrato de Diseño Muestral»* | estratificación |
| `UPM_DIS` | *«Unidad Primaria de Muestreo»* | conglomerado |
| `LLAVEHOG` | *«Llave de identificación del hogar»* | agregación a hogar |

### 1.4 · `FAC_HOG` **no está en `tvar_crea.csv`** — y está en dos archivos a la vez

`milpa/tramite.yaml:1036` declara el ponderador de la regla como
*«`FAC_HOG` (D2, razón) / `FAC_PER` (D1, descriptivo por sexo × edad)»* y
`milpa/tramite.yaml:1038` sitúa el universo en *«los 29 181 hogares de
`tvar_crea.csv`»*. Las dos cosas juntas no se pueden hacer:

```
$ awk -F'\t' '$5=="tvar_crea.csv"{print $6}' data/inventario-reactivos-v1_2.tsv \
      | grep -c '^FAC_HOG$'
0                       # 60 columnas reales, FAC_HOG no es una de ellas
$ awk -F'\t' 'toupper($6) ~ /^FAC/ {print $5"  "$6}' …enut2024_bd_csv.zip…
  thogar.csv    FAC_HOG
  tsdem.csv     FAC_HOG
  tvar_crea.csv FAC_PER
  tmodulo.csv   FAC_PER
  tvivienda.csv FAC_VIV
```

**`FAC_HOG` vive en `tsdem.csv` y en `thogar.csv`, en ninguno de los cuales
están las horas.** Un medidor que confiara en la letra de la regla —
`FAC_HOG` sobre `tvar_crea.csv` — falla en la primera línea; uno que
resolviera `FAC_HOG` por nombre tomaría el de cualquiera de los dos archivos
sin que nada se queje. Esta spec, por tanto:

1. **fija el archivo**: `FAC_HOG` se toma de **`tsdem.csv`**, unido por
   `LLAVEHOG`, siguiendo el precedente ya corrido de
   `tools/medidor_cuidado_enut.py` (`ACTO MAESTRA35-L7`), que verificó que
   `FAC_PER` **no** es constante dentro del hogar y `FAC_HOG` **sí** lo es; y
2. **añade la guarda que nadie había corrido**:
   `G-FAC-HOG-TSDEM-IGUAL-THOGAR` compara, hogar por hogar, el `FAC_HOG` de
   `tsdem.csv` contra el de `thogar.csv`. `IGUAL` / `DIFIERE:<n_hogares>`.
   Si difieren, la elección de archivo **cambia la cifra** y eso deja de ser
   un detalle de implementación para volverse una decisión de mesa: el punto
   se emite igualmente, con la marca.

`A.4` — universo del negativo de §1.4: las 60 columnas de `tvar_crea.csv` y
las 60 de `thogar.csv` listadas en `data/inventario-reactivos-v1_2.tsv` para
el payload `enut2024_bd_csv.zip` (`sha256_12` coincidente con el manifiesto),
más las hojas `TVAR_CREA` y `THOGAR` de `data/inventario-fd-v1_1.tsv`,
15/sep/2026.

---

## 2 · Qué mide, exactamente

### 2.1 · El recorte de «cuidado», medido antes de rotular

`horas_cuidado(persona)` = suma de las **cuatro** variables `*_CON_CP` de
§1.3. Es la definición del precedente `Y1` (4/ago/2026), **reusada, no
redefinida** — y se declara lo que deja fuera, porque «horas de cuidado del
hogar» es propiedad del recorte, no del instrumento:

- **`CUID_INT_15A59` queda fuera** (cuidado a integrantes del hogar de 15 a
  59 años). No tiene variante `CON_CP` en el FD, así que incluirla mezclaría
  dos definiciones de cuidado pasivo. `C-P-RESIDUO-15A59` mide su peso sobre
  el total, para que el recorte se pueda auditar por su tamaño, no por su
  nombre.
- Quedan fuera, por diseño, los cuidados **a otros hogares**
  (`CUID_ESP_DISC_ENF`, `CUID_PER_OTROS_HOG`): la regla habla del hogar.
- Se usa la variante **con cuidados pasivos**. `C-P-SIN-CP` re-calcula la
  razón con las variantes `*_SIN_CP` disponibles y emite el delta con signo.
  **Ninguna de las dos ramas se elige sobre la marcha**: la primaria es
  `CON_CP` porque es la del precedente, y la otra es rama declarada.

### 2.2 · Universo y estimando

Universo: **todos** los hogares de `tvar_crea.csv` (`LLAVEHOG`), incluidos
los que no registran ninguna hora de cuidado — aportan `0/0` y **no se
excluyen**: excluirlos cambiaría la pregunta de *«cómo se reparte el cuidado
que hay»* a *«cómo se reparte en los hogares que cuidan»*. `A-N-HOGARES` y
`A-N-HOGARES-CON-CARGA` salen ambos como `RESULT`, y también
`A-N-HOGARES-SIN-MUJER-40MAS` (aportan 0 al numerador, correctamente, sin
salir del denominador).

`A-R` = `Σ_h w_h · num_h / Σ_h w_h · den_h`, con `w = FAC_HOG` (de
`tsdem.csv`), `num_h` = horas de cuidado de las mujeres 40+ del hogar
(`SEXO == '2' ∧ EDAD >= 40`), `den_h` = horas de cuidado totales del hogar.
**Estimador de RAZÓN**, no proporción de un binario. **DESCRIPTIVO**: mide
reparto, y ningún `RESULT` es causal — la flecha de `R5.2` (*«el cuidado
recae sobre mujeres 40+»*) no se adjudica aquí.

Contexto obligatorio junto al punto, porque sin él la cifra se lee al revés:
`A-SHARE-POBLACIONAL-MUJERES-40MAS` = participación de las mujeres 40+ en la
población del universo, ponderada. La regla se lee comparando `A-R` contra
ese share, no contra cero. (GEN1 publica `0.2657` como contexto de su
`0.2215`; aquí se **re-mide**, no se copia.)

### 2.3 · Diseño — el bootstrap de una razón no es el de una proporción

Conglomerado = `(EST_DIS, UPM_DIS)` del hogar, **verificado constante dentro
de `LLAVEHOG`** antes de usarlo (`G-DISENO-CONSTANTE-EN-HOGAR`). Se
re-muestrean **UPM con reemplazo dentro de `EST_DIS`**, y en cada réplica se
recalcula `Σw·num / Σw·den` — **numerador y denominador de la misma réplica**.
2 000 réplicas, `numpy.PCG64`, semilla `20260915`, percentiles 2.5/97.5.
`EST_DIS`/`UPM_DIS` como **cadena cruda opaca**. Estrato con UPM única se
re-muestrea a sí mismo, no se colapsa ni se descarta; si el conteo es `> 0`,
`A-METODO-IC = IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite
inferior**.

---

## 3 · Control positivo y adopción

| `RESULT` | contra qué | vocabulario |
|---|---|---|
| `A-DELTA-VS-GEN1` | `0.2215` (`milpa/tramite.yaml:1027`) | delta con signo |
| `A-REPRODUCE-GEN1` | `round(A-R, 4) == 0.2215` | `REPRODUCE` / `NO-REPRODUCE` |
| `A-DELTA-SHARE-POBLACIONAL-VS-GEN1` | `0.2657` (`:1029`) | delta con signo |
| `A-N-HOGARES` | `29181` | `COINCIDE` / `DIFIERE:<delta>` |

El grano de GEN1 es de **cuatro** decimales (`0.2215`), no seis: la
comparación se hace a cuatro y `A-GRANO-GEN1` lo declara, en vez de fabricar
un `NO-REPRODUCE` por redondear a un grano que la cifra vieja nunca tuvo.
`NO-REPRODUCE` no autoriza tocar el medidor. `A-ADOPCION` sale
`LISTADO-PARA-MESA-*`; **este acto no escribe cita en `milpa/`**.

**Contaminación declarada (`ADR-46`).** Al congelar, la sesión ya había leído
`p = 0.2215`, el share poblacional `0.2657`, `n = 29181`, `upm = 4200`, las
diez celdas de `eje_sexo_edad` con sus medias de horas, el `veredicto_acotado`
de mesa y el medidor de `MAESTRA35-L7` completo. **No es ciega, y en el caso
del medidor tampoco podría serlo**: leerlo es lo que permitió encontrar §1.4.
Lo genuinamente desconocido al congelar: si `FAC_HOG` de `tsdem.csv` y de
`thogar.csv` coinciden, el peso del residuo `CUID_INT_15A59`, la distancia
entre la rama `CON_CP` y la `SIN_CP`, la anchura del IC bajo esta semilla y
cuántos estratos quedan con UPM única.

---

## 4 · Lo que NO hace

No abre microdato · no corre el medidor (lo escribe el acto de CAJA a partir
de este contrato) · no usa ENUT 2019 ni 2009 (sin `tvar_crea`; reconstruir
`CON_CP` desde ~40 ítems crudos no tiene precedente validado en este repo) ·
no re-abre el `veredicto_acotado` de mesa · no repite el contraste por
ocupación de `Y1`/`Y5` · no adopta cifra alguna a `milpa/` · no toca
`CORR-0011`, `CORR-0012` ni `CORR-0013`.
