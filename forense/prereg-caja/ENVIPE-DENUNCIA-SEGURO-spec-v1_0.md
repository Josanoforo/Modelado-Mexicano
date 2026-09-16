# ENVIPE-DENUNCIA-SEGURO · Pre-registro de la denuncia por estrato de cobertura de seguro, robo total de vehículo, ENVIPE 2025

### `prereg-caja-ENVIPE-DENUNCIA-SEGURO` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/ENVIPE-DENUNCIA-SEGURO-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-ENVIPE-DENUNCIA-SEGURO`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado **antes de abrir un solo byte de microdato**, de la corrida `CALC-ENVIPE-DENUNCIA-SEGURO-0001`: las **dos probabilidades de denuncia por estrato de cobertura de seguro y sus complementos exactos contados dentro del mismo estrato**, unidad **delito**, restringido a `BPCOD = 01` (robo total de vehículo), ENVIPE 2025. Releva bajo el registro GEN2 los cuatro `RESULT` que restaban de la demanda `CORR-0007`: `RES-0039`, `RES-0040`, `RES-0041`, `RES-0042`. |
> | **QUÉ NO ES** | **No es causal.** No es la opción B de la propuesta (redefinición de motor): mesa NO la firmó y esta spec no se desliza hacia ella. No extrapola a otros delitos ni a `BPCOD ≠ 01`. No mide razones de no denuncia (eso es `prereg-caja-ENVIPE-DENUNCIA`, otra apertura, sellada y no tocada aquí). No adopta: **no escribe cita en `milpa/` bajo ninguna rama**. No corre: ningún byte de microdato se abre en este acto. |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py preflight CALC-ENVIPE-DENUNCIA-SEGURO-0001`. Reportará `BLOQUEADO:script_ausente` hasta que el acto de CAJA escriba el medidor: eso es **correcto**, no un defecto de esta spec (§9.2). |

**Acto:** `ACTO GEN2-FIRMAS-MESA-1`, 15/sep/2026, entorno **NUBE**, rama `claude/epic-thompson-wbbmg7`.
**Autoridad:** firma de mesa verbatim «**Si a todas.**» sobre la HOJA DE FIRMAS DE MESA 2026-09-15, archivada en `forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-1.md`.
**OBJETO 10, verbatim:** «*NC-0088 — apertura estrecha ENVIPE-DENUNCIA-SEGURO-v1_0 para RES-0039..0042. Spec aquí; corrida en caja.*»

**CONGELADO en el COMMIT-1, en NUBE, antes de abrir un solo byte de microdato.**

---

## 0 · Premisas verificadas contra el árbol

### 0.1 · Qué firmó mesa, exactamente

La propuesta `forense/prereg-caja/ENVIPE-DENUNCIA-SEGURO-propuesta-v1_0.md` puso dos opciones a la vista y **no** tomó la decisión («*Este documento hace visible la elección; no la toma*»). El OBJETO 10 firma la **opción A — estrecha descriptiva**. Esta spec implementa A al pie de la letra, elemento por elemento:

| elemento de la opción A, verbatim de la propuesta | dónde queda en esta spec |
|---|---|
| fuente/ola: `envipe2025_csv`, ENVIPE 2025 | §1.1 |
| unidad: **delito** | §2.1 |
| población: registros con `BPCOD=01` y respuesta válida de seguro y denuncia | §2.2 |
| capas: `BP2_1` define con/sin seguro; `BP1_20` define denuncia/no denuncia | §3.2, §3.3 |
| ponderador: `FAC_DEL` | §3.4 |
| diseño: `EST_DIS` y `UPM_DIS` | §3.5 (**verificado en el inventario**, §0.3) |
| estimandos: las dos probabilidades de denuncia por estrato de seguro y sus complementos exactos dentro del mismo estrato | §8 |
| propósito: describir la asociación seguro–denuncia en esa apertura, sin interpretación causal ni extrapolación a otros delitos | §8.4 |

**La opción B queda fuera y se dice aquí para que no entre por descuido.** Opción B era «*redefinir población, unidad, tratamiento de cobertura, desenlace y uso en el motor*». Esta spec **no redefine ninguna de las cinco**: conserva la población histórica, la unidad delito, `BP2_1` tal cual, `BP1_20` tal cual, y **no declara uso en el motor**. Si al correr se descubriera que la apertura A no es medible, la consecuencia es `NO-ESTIMABLE` (§7), **nunca** una migración silenciosa a B — B requiere una decisión científica nueva y una spec distinta, y mesa no la firmó.

### 0.2 · El entorno, dicho sin disfraz

Este acto corre en **NUBE**. `data/raw/` **no existe**, el corpus no está montado y `numpy`/`pandas`/`pyreadstat` están **ausentes**. La regla de la casa E.5 permite en nube abrir **sólo codebook y metadato**. Por tanto:

- **cero afirmaciones sobre el dato** que no estén ancladas a un archivo del repo;
- toda cifra de esta spec que describa el microdato es **cita de un archivo del repo**, marcada como tal, no observación propia;
- lo que no pudo verificarse se declara como tal en §10, y eso es **entregable, no fracaso**.

### 0.3 · La verificación que el encargo pidió explícitamente: `EST_DIS` y `UPM_DIS`

La propuesta nombra el diseño como `EST_DIS` y `UPM_DIS`. **Comprobado contra `data/inventario-reactivos-v1_2.tsv`** — inventario a nivel de COLUMNA construido por inspección real de los ZIP (`INSPECT_ZIP`, `PRESENTE_EN_DATA_RAW`), que es metadato del repo y no microdato:

```
$ awk -F'\t' '$5=="tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv"{print $6}' \
      data/inventario-reactivos-v1_2.tsv | grep -nxE 'EST_DIS|UPM_DIS|BPCOD|BP1_20|BP2_1|FAC_DEL|ID_DEL'
35:BP1_20
89:BP2_1
118:BPCOD
122:EST_DIS
123:FAC_DEL
136:UPM_DIS
```

**Veredicto: `EST_DIS` y `UPM_DIS` SÍ existen con ese nombre exacto** en el archivo de víctimas de ENVIPE 2025, junto con las cuatro variables de la opción A. No hubo que inventar nada y no se declara guardia de renombre.

⚠️ **Dos homónimos del diseño, sellados aquí para que el medidor no resuelva por nombre parecido.** El mismo archivo declara también `ESTRATO` (línea 121 del listado) y `UPM` (línea 135), que **no son** `EST_DIS` ni `UPM_DIS`. El medidor toma **exactamente `EST_DIS` y `UPM_DIS`**, por nombre literal; tomar `ESTRATO`/`UPM` partiría o fusionaría conglomerados en silencio (`A.15(c)`). Igual con el ponderador: existe `FAC_DEL_AM` (línea 124) además de `FAC_DEL`; **se usa `FAC_DEL`**, nunca `FAC_DEL_AM`.

### 0.4 · La llave de registro, verificada y no inventada

El encargo pide lo mismo para cualquier llave de registro. El inventario declara en ese mismo archivo, entre las columnas de identificación: `ID_DEL`, `ID_HOG`, `ID_PER`, `ID_VIV`, `VIV_SEL`, `HOGAR`, `R_SEL`, `UPM`. **`ID_DEL` existe** y es la llave de grano **delito**, que es la unidad de esta spec.

**Lo que NO puedo verificar en nube (declarado, no supuesto):** que `ID_DEL` sea **única por sí sola** en el archivo, o que haga falta componerla con `ID_VIV+ID_HOG+ID_PER`. El inventario lista columnas, no cardinalidades. Consecuencia mecánica, no promesa: el medidor **prueba las dos** y lo reporta como `RESULT` de texto (`G-LLAVE-DELITO`), y si **ninguna** de las dos es única, sale `NO-ESTIMABLE-LLAVE-NO-UNICA` y no hay cifra (§7).

### 0.5 · La cita de demanda, corregida de origen

Esta spec cita **`CORR-0007`**, no `CORR-0009`. Verificado contra la demanda vigente:

```
$ grep -n "^CORR-0007" data/corrida0/demanda-corridas.tsv
CORR-0007  ENVIPE2025  envipe2025_csv  ...  RES-0025;RES-0026;RES-0027;RES-0028;RES-0039;RES-0040;RES-0041;RES-0042  CAJA
```

`prereg-caja-ENVIPE-DENUNCIA` (sellada, 9/sep) citaba `CORR-0009` para estos mismos `RESULT`; la sucesión fechada `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0-CORRECCION-2026-09-15.md` ya asentó que la cita correcta es `CORR-0007`. Esta spec nace con la cita corregida. **Ninguno de los dos archivos anteriores se edita: están sellados.**

---

## 1 · Identidad: instrumento, ola, payload, tabla

### 1.1 · Payload, por el manifiesto (nunca «está en `data/raw`»)

| campo | valor |
|---|---|
| `id` de manifiesto | **`envipe2025_csv`** |
| archivo | `envipe2025_csv.zip` |
| `sha256` | `8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa` |
| `tamano_bytes` | `17600019` |
| `url_origen` | `https://www.inegi.org.mx/contenidos/programas/envipe/2025/datosabiertos/conjunto_de_datos_ENVIPE_2025_csv.zip` |
| `fecha_descarga` | `2026-07-30` |

⚠️ **Homónimo peligroso, sellado aquí.** El propio manifiesto advierte que ENVIPE 2025 está registrada **dos veces con payloads distintos**: el otro es `envipe_2025_bd_envipe_2025_csv` (canasta masiva, otro `sha256`). **No son intercambiables por nombre.** Esta spec usa `envipe2025_csv` y sólo ése, resuelto por `id` de manifiesto; el medidor nunca busca su payload por su cuenta. El `sha256` de arriba es además el que `data/corrida0/demanda-resultados.tsv` declara en las cuatro filas `RES-0039..0042`: coinciden, y por eso la corrida releva esa demanda y no otra.

### 1.2 · Miembro del ZIP, declarado por nombre completo

```
tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv
```

Un solo miembro de datos. **Ninguna otra tabla se abre** — ni `TPer_Vic`, ni la vivienda, ni el módulo de percepción.

⚠️ **Segundo homónimo, también sellado.** El inventario declara un gemelo: `envipe2025/bd_envipe_2025_csv.zip` contiene `TMod_Vic.csv` con las mismas cuatro variables y con `EST_DIS`/`UPM_DIS`. **Ese gemelo NO se abre en esta corrida.** El payload es el del §1.1, resuelto por `id` de manifiesto, y el miembro es el de arriba, resuelto por ruta completa dentro del ZIP. Si el miembro no está con esa ruta exacta → `NO-ESTIMABLE-MIEMBRO-AUSENTE` (§7); **no** se cae al gemelo.

### 1.3 · Catálogos, que son metadato y por eso sí son citables en nube

El inventario declara, en el **mismo** ZIP, los catálogos del propio instrumento:

```
tmod_vic_envipe2025/catalogos/bpcod.csv     (columnas: BPCOD, descrip)
tmod_vic_envipe2025/catalogos/bp1_20.csv    (columnas: BP1_20, descrip)
tmod_vic_envipe2025/catalogos/bp2_1.csv     (columnas: BP2_1, descrip)
tmod_vic_envipe2025/catalogos/fac_del.csv   (columnas: FAC_DEL, descrip)
```

Son metadato. El medidor los **lee y los contrasta** contra el mapa de códigos de §3; ese contraste es un `RESULT` pre-declarado (`G-CATALOGO-*`), no una comprobación informal.

---

## 2 · Unidad y universo

### 2.1 · Unidad de observación: **delito**

No persona, no hogar, no vivienda. Una fila de `conjunto_de_datos_tmod_vic_envipe2025.csv` es un **delito** declarado por una víctima; una misma persona puede aportar más de una fila. El ponderador que corresponde a ese grano es `FAC_DEL` (§3.4) y ningún otro. Esto **no** es intercambiable con `prereg-caja-ENVIPE-DENUNCIA`, cuya apertura es otra; los dos no se suman ni se comparan.

### 2.2 · Universo `U`, verbatim de la opción A

`U` = registros de ese archivo que cumplen **las tres** condiciones, en este orden:

1. `BPCOD == "01"` (robo total de vehículo), leído como **cadena**, comparado literalmente con `"01"`;
2. **respuesta válida de seguro**: `BP2_1` dentro del mapa de estratos de §3.2;
3. **respuesta válida de denuncia**: `BP1_20` dentro del mapa de desenlaces de §3.3;

y además `FAC_DEL` finito y `> 0` (§3.4).

Nada más. **No** hay filtro de edad, sexo, entidad, dominio ni año de ocurrencia: la opción A no declara ninguno y esta spec no añade los que mesa no firmó.

### 2.3 · Los dos estratos

`U` se parte en exactamente dos subuniversos por `BP2_1`:

- `U_CON` = `U` ∧ con cobertura de seguro;
- `U_SIN` = `U` ∧ sin cobertura de seguro.

Son **disjuntos y exhaustivos dentro de `U`** por construcción del mapa de §3.2: `U_CON ∪ U_SIN = U`, y eso se comprueba contando (`RESULT` `G-PARTICION-ESTRATOS`), no se da por hecho.

### 2.4 · Lo que el universo deja fuera, y por qué eso NO es un defecto

Queda fuera todo `BPCOD ≠ 01`. Es **deliberado y firmado**: la propuesta lo llama «la apertura histórica documentada es estrecha» y el OBJETO 10 la llama «apertura estrecha». Esta spec **no mide, no estima y no insinúa** nada sobre los demás delitos. Véase la prohibición operativa de §8.4.

---

## 3 · Variables: las cuatro de la opción A, más el diseño

### 3.1 · `BPCOD` — filtro de clase de delito

Columna verificada presente (§0.3). Se lee como **cadena cruda** (`dtype=str`), sin convertir a entero: `"01"` convertido a entero se vuelve `1` y deja de cotejar contra el catálogo, que está escrito con cero a la izquierda. Se compara **literalmente** contra `"01"`. El catálogo `catalogos/bpcod.csv` se lee y se contrasta.

### 3.2 · `BP2_1` — la capa: con seguro / sin seguro

Columna verificada presente. Se lee como cadena cruda.

| código | estrato |
|---|---|
| `"1"` | **con seguro** → `U_CON` |
| `"2"` | **sin seguro** → `U_SIN` |
| cualquier otro (incl. `"9"`, vacío, nulo) | **fuera de `U`**, `CONTADO` como `N-SEGURO-INVALIDO`, nunca imputado |

**Procedencia honesta de este mapa, y su guardia.** No pude abrir `catalogos/bp2_1.csv` en nube. El mapa `1 = asegurado / 2 = no asegurado / 9 = no sabe` está **citado de dos archivos del repo**: `tools/medidor_denuncia_seguro_envipe25.py:59` y `:111-115`, y `milpa/tramite.yaml:1004` (`BP2_1∈{1,2}`). Por eso **no se da por verificado**: el medidor debe leer `catalogos/bp2_1.csv` y **contrastar** que `"1"` y `"2"` estén ahí con descripciones consistentes con «tiene/no tiene seguro». Si el catálogo contradice el mapa, o si aparece en `U` un código de `BP2_1` que no está en el catálogo → `NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA` (§7). **El código `9` NO se reparte entre estratos ni se imputa: sale del universo y se cuenta.**

### 3.3 · `BP1_20` — el desenlace: denuncia / no denuncia

Columna verificada presente. Cadena cruda.

| código | desenlace |
|---|---|
| `"1"` | **denuncia** |
| `"2"` | **no denuncia** |
| cualquier otro (vacío, nulo, `"9"`) | **fuera de `U`**, `CONTADO` como `N-DENUNCIA-INVALIDA`, nunca imputado |

Misma procedencia y misma guardia que §3.2 (`tools/medidor_denuncia_seguro_envipe25.py:106`, `BP1_20.isin(["1","2"])`), con contraste obligatorio contra `catalogos/bp1_20.csv`.

### 3.4 · `FAC_DEL` — el ponderador

Columna verificada presente. **Flotante tal cual: sin normalizar, sin redondear, sin truncar, sin re-escalar.** Ningún otro ponderador entra. En particular **NO** entra `FAC_DEL_AM`, que existe en el mismo archivo (§0.3): se declara aquí como parámetro y no como detalle, porque resolver el ponderador por nombre parecido tomaría uno u otro sin aviso (`A.15(c)`). Fila con `FAC_DEL` vacío, no finito o `<= 0` **sale de `U`** y se cuenta como `N-SIN-PONDERADOR`.

### 3.5 · `EST_DIS` y `UPM_DIS` — el diseño

Ambas verificadas presentes con ese nombre exacto (§0.3). Se agrupan como **cadena cruda opaca** (`dtype=str`): nunca a entero, nunca re-rellenadas con ceros: normalizarlas partiría o fusionaría estratos en silencio. El perfil observado de anchos sale como `RESULT` de texto.

Fila del universo **sin** `EST_DIS` o **sin** `UPM_DIS` se **cuenta** (`N-SIN-DISENO`) pero **no sale del punto**: afecta al IC, no al estimador. Si **toda** fila del universo carece de diseño → `METODO-IC = NO-ESTIMABLE-DISENO-INCOMPLETO`, los IC salen `null` y el punto se reporta igual.

---

## 4 · Hipótesis pre-registrada, escrita ANTES de abrir el dato

Se escribe aquí, en nube, con el microdato cerrado, para que al abrirlo no se pueda reescribir:

> **H1.** Dentro de `BPCOD = 01`, la proporción ponderada de denuncia es **mayor** en `U_CON` que en `U_SIN`; la diferencia `P-CON-DENUNCIA − P-SIN-DENUNCIA` sale **positiva**.
>
> **H2.** La diferencia es **material y no sólo de signo**: su magnitud supera la anchura típica del ruido de muestreo de las dos estimaciones.

**H1 y H2 están contaminadas y se declaran como tales, no como pronóstico ciego** — véase §5. La sesión ya leyó `0.7909` y `0.6720` en el registro antes de congelar. Por eso:

- H1/H2 se registran como **derivaciones de metadato leído**, para que mesa las descuente, no como aciertos;
- el **veredicto** de esta corrida **no** cuelga de H1/H2. Lo que gobierna es §6: los cuatro puntos, sus complementos contados, sus IC de diseño, y el delta con signo contra el registro.

> **H0 explícita, que es la que importa:** esta corrida **no** postula ningún mecanismo. Que la denuncia sea más alta con seguro **no** se afirma causado por el seguro. Véase §8.4.

---

## 5 · Contaminación declarada (ADR-46) — esta corrida NO es ciega

Se dice antes de cualquier cifra, no después.

### 5.1 · Qué sabe ya la sesión al congelar

| dónde, con línea | qué se leyó | valor |
|---|---|---|
| `data/corrida0/demanda-resultados.tsv` · `RES-0039..0042` | los cuatro valores legacy y su `payload_sha256` | `0.7909` / `0.2091` / `0.672` / `0.328` |
| `milpa/tramite.yaml:987-1007` (`civico.denuncia.con_seguro`) | punto, IC95, `n`, estratos, UPM, ponderador, universo | `p=0.790900` / `0.209100`; `ic95=[0.752301, 0.827811]`; `n=402`; `estratos=200`; `upm=377`; `FAC_DEL` |
| `milpa/tramite.yaml:1009-1029` (`civico.denuncia.sin_seguro`) | idem | `p=0.672000` / `0.328000`; `ic95=[0.642490, 0.701624]`; `n=614`; `estratos=289`; `upm=567`; `FAC_DEL` |
| `milpa/tramite.yaml:1004` y `:1026` | el universo GEN1 verbatim y su total | `BPCOD='01' ∧ BP2_1∈{1,2}`; **`n = 402 + 614 = 1 016`** |
| `milpa/tramite.yaml` (`nota_hito_d`, ambas entradas) | el veredicto previo de Hito D | «`79.1/67.2/11.9 pp`» |
| `tools/medidor_denuncia_seguro_envipe25.py:11-28`, `:48-130` | la premisa de degeneración (`BP2_1` degenerada fuera de `BPCOD=01`, «1 028 de 40 280 filas»), el mapa de códigos y el diseño `EST_DIS×UPM_DIS` con bootstrap | — |
| `forense/prereg-caja/ENVIPE-DENUNCIA-SEGURO-propuesta-v1_0.md` | la opción A entera y sus controles mínimos | — |

**Consecuencia, sin adornos:** el ejecutor conoce los cuatro valores legacy, sus IC, sus `n`, su número de estratos y de UPM, y el veredicto previo de Hito D, **antes** de congelar. No es una corrida ciega y no se presenta como tal.

### 5.2 · Qué se hace con eso, mecánicamente

1. Los cuatro valores legacy entran **sólo** como `valores_gen1_referencia` y producen deltas **con signo** (`DELTA-VS-GEN1`), no un umbral que esta sesión pudiera calibrar hacia la cifra que ya conoce.
2. **`n=402`, `n=614` y `n=1016` NO son filtro ni criterio de parada.** Entran como `n_gen1_referencia` para contraste; si el medidor cuenta otra cosa, **manda lo contado**, y la discrepancia es un hallazgo que se reporta, no un error que se corrige forzando el universo.
3. Los complementos se **cuentan** (§8.2). Conocer que `0.7909 + 0.2091 = 1` exactamente **no** autoriza a derivar uno del otro: si el complemento contado no suma uno dentro de tolerancia, eso es precisamente el hallazgo que la partición contada existe para producir.
4. `criterio_adopcion` sale `LISTADO-PARA-MESA-*`: esta spec **no adopta**, y por tanto la contaminación no puede convertirse en un sello.

### 5.3 · Qué queda genuinamente desconocido al congelar

Dicho como lista, porque es entregable:

- **si `ID_DEL` es única por sí sola** en el archivo, o hace falta componerla (§0.4) — el inventario lista columnas, no cardinalidades;
- **el soporte observado real** de `BP2_1`, `BP1_20` y `BPCOD`, y por tanto **cuántas filas caen fuera** por `BP2_1 = 9`, por `BP1_20` inválido o por blanco: **ninguna fuente leída trae esos conteos**, ni el registro, ni `milpa/`, ni el script antecedente;
- **si el contenido de `catalogos/bp2_1.csv` y `catalogos/bp1_20.csv` confirma el mapa de §3.2/§3.3**: no se abrió el ZIP;
- **cuántas filas tiene el archivo de víctimas de 2025** y cuántas caen en `BPCOD = 01`: la cifra «1 028 de 40 280» del script antecedente es de **su** corrida, no una lectura de este acto, y esta spec la trata como referencia a contrastar, no como dato;
- **cuántos estratos quedan con UPM única** y cuánto se ensancha el IC por eso;
- **si `FAC_DEL` es finito y positivo en todas las filas** del universo;
- **si el IC de diseño de esta corrida reproduce la anchura de los IC95 sellados** en `milpa/`: los sellados no declaran método de IC verificable desde aquí.

---

## 6 · Controles mínimos de la propuesta, como `RESULT` pre-declarados

La propuesta exige, verbatim: «*El futuro medidor debe declarar negativos y faltantes, tamaños sin ponderar por celda, sumas de pesos, puntos, EE e IC95 con el diseño indicado, particiones que suman uno dentro de tolerancia, hashes de payload/spec/script y un replay independiente.*» Cada uno es un `RESULT` con id, no una promesa en prosa:

| control exigido | `RESULT` que lo cumple |
|---|---|
| negativos y faltantes | `G-N-SEGURO-INVALIDO`, `G-N-DENUNCIA-INVALIDA`, `G-N-SIN-PONDERADOR`, `G-N-SIN-DISENO`, `G-N-PESOS-NO-POSITIVOS`, `G-N-FUERA-DE-BPCOD-01` |
| tamaños **sin ponderar** por celda | `CON-N-DENUNCIA`, `CON-N-NO-DENUNCIA`, `SIN-N-DENUNCIA`, `SIN-N-NO-DENUNCIA`, más `CON-N-U` y `SIN-N-U` |
| sumas de pesos | `CON-SUMA-PESOS`, `SIN-SUMA-PESOS`, `G-SUMA-PESOS-U` |
| puntos | `CON-P-DENUNCIA`, `CON-P-NO-DENUNCIA`, `SIN-P-DENUNCIA`, `SIN-P-NO-DENUNCIA` |
| **EE** e IC95 con el diseño indicado | `CON-EE-DENUNCIA`, `SIN-EE-DENUNCIA`, `CON-IC-LO/HI`, `SIN-IC-LO/HI`, `METODO-IC` |
| particiones que suman uno dentro de tolerancia | `CON-SUMA-UNO`, `SIN-SUMA-UNO`, `G-PARTICION-ESTRATOS` |
| hashes de payload / spec / script | `G-SHA256-PAYLOAD`, `G-SHA256-SPEC-SELLADA`, `G-SHA256-SPEC-YAML`, `G-SHA256-SCRIPT` |
| replay independiente | `G-REPLAY-INDEPENDIENTE` (§6.1) |

### 6.1 · Qué significa «replay independiente», para que no se cumpla de mentira

Segunda pasada sobre el **mismo** payload, recorriendo el universo por **orden de llave** en lugar del orden de lectura, y recalculando los cuatro puntos y las cuatro sumas de pesos con acumulación independiente. `G-REPLAY-INDEPENDIENTE` sale `REPLICA` si los ocho valores coinciden dentro de la tolerancia de §9.1, y `NO-REPLICA:<peor residuo>` si no. **`NO-REPLICA` no autoriza tocar el medidor para que replique**: es un hallazgo que se reporta a mesa.

### 6.2 · El antecedente técnico, con su salvedad verbatim

Existe `tools/medidor_denuncia_seguro_envipe25.py`. La propuesta lo califica —y esta spec lo repite sin suavizar— como «*cobertura técnica localizada, no autoridad para correr ni adoptar*».

**En claro:** ese archivo **no se edita**, **no es el script de esta spec**, y **no gobierna nada aquí**. El script de esta corrida es `data/corrida0/CALC-ENVIPE-DENUNCIA-SEGURO-0001/medidor.py`, que **todavía no existe** y lo escribe el acto de CAJA a partir de este contrato. Del antecedente se cita únicamente, y con atribución explícita, el mapa de códigos de §3.2/§3.3 y la premisa de degeneración de §5.1 — ambos **marcados como pendientes de contraste contra el catálogo**, no como verificados.

---

## 7 · Guardias: `NO-ESTIMABLE` en vez de una cifra

**CERO NUNCA SUSTITUYE FALTA DE DATO.** Cuando el dato no alcanza, el `RESULT` sale `NO-ESTIMABLE` con su causa; no sale `0`, no sale imputado, no sale de otra fuente.

| condición | token |
|---|---|
| el miembro declarado no está en el ZIP con esa ruta exacta | `NO-ESTIMABLE-MIEMBRO-AUSENTE:<m>` |
| una columna declarada (`BPCOD`, `BP2_1`, `BP1_20`, `FAC_DEL`, `EST_DIS`, `UPM_DIS`) no está | `NO-ESTIMABLE-COLUMNA-AUSENTE:<col>` |
| `BP2_1`, `BP1_20` o `BPCOD` traen en `U` un código ausente de su catálogo, o el catálogo contradice §3.2/§3.3 | `NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:<col>` |
| ni `ID_DEL` ni `ID_DEL+ID_VIV+ID_HOG+ID_PER` son únicas | `NO-ESTIMABLE-LLAVE-NO-UNICA` |
| `U`, `U_CON` o `U_SIN` queda vacío | `NO-ESTIMABLE-UNIVERSO-VACIO:<subuniverso>` |
| **toda** fila del universo carece de `EST_DIS` o `UPM_DIS` | `NO-ESTIMABLE-DISENO-INCOMPLETO` (afecta IC/EE; el punto se reporta igual) |

Un `NO-ESTIMABLE` en cualquiera de los cuatro puntos fuerza `ADOPCION = NO-ADOPTABLE-NO-ESTIMABLE`. **Un universo más chico de lo esperado no es una guardia**: es un hallazgo y se reporta con su conteo.

---

## 8 · El estimando, exactamente como mesa lo firmó

### 8.1 · Los cuatro puntos

Con `w = FAC_DEL`, dentro de cada estrato por separado:

```
CON-P-DENUNCIA     = Σ w·[BP1_20 = "1"]  /  Σ w      sobre U_CON
CON-P-NO-DENUNCIA  = Σ w·[BP1_20 = "2"]  /  Σ w      sobre U_CON
SIN-P-DENUNCIA     = Σ w·[BP1_20 = "1"]  /  Σ w      sobre U_SIN
SIN-P-NO-DENUNCIA  = Σ w·[BP1_20 = "2"]  /  Σ w      sobre U_SIN
```

Sumas en orden fijo de llave. El denominador de cada punto es la suma de pesos **de su propio estrato**, nunca la de `U` entero.

### 8.2 · Los complementos se CUENTAN, nunca `1 − p`

Regla dura, sin excepción: `CON-P-NO-DENUNCIA` y `SIN-P-NO-DENUNCIA` se obtienen **contando directamente** las filas con `BP1_20 = "2"` y ponderándolas, **dentro del mismo estrato**. Están escritos arriba como sumas propias por esa razón. **Está prohibido calcularlos como `1 − p`.**

Por qué importa: derivar el complemento hace que la partición sume uno **por construcción**, y entonces el control de suma-uno de §6 no comprueba nada. Contándolo, `CON-SUMA-UNO` y `SIN-SUMA-UNO` son una prueba real de que el universo está bien partido, y un residuo fuera de tolerancia es un hallazgo (típicamente un tercer código que se coló) en vez de un error invisible.

### 8.3 · Mapeo explícito de cada `RES` a su `RESULT`

Localizado en `data/corrida0/demanda-resultados.tsv` por su consumidor:

| `RES` | consumidor, verbatim del registro | valor legacy | **`RESULT` de esta spec** |
|---|---|---|---|
| **`RES-0039`** | `milpa/tramite.yaml:civico.denuncia.con_seguro:denuncia` | `0.7909` | **`RESULT-ENVIPE-SEG-CON-P-DENUNCIA`** |
| **`RES-0040`** | `milpa/tramite.yaml:civico.denuncia.con_seguro:no_denuncia` | `0.2091` | **`RESULT-ENVIPE-SEG-CON-P-NO-DENUNCIA`** |
| **`RES-0041`** | `milpa/tramite.yaml:civico.denuncia.sin_seguro:denuncia` | `0.672` | **`RESULT-ENVIPE-SEG-SIN-P-DENUNCIA`** |
| **`RES-0042`** | `milpa/tramite.yaml:civico.denuncia.sin_seguro:no_denuncia` | `0.328` | **`RESULT-ENVIPE-SEG-SIN-P-NO-DENUNCIA`** |

Los cuatro pertenecen a `CORR-0007` (§0.5). **Esta corrida no releva ningún otro `RESULT`** — en particular no releva `RES-0025`, `RES-0026`, `RES-0027` ni `RES-0028` de la misma `CORR-0007`.

### 8.4 · Propósito, y la prohibición, **dentro** de la spec

Propósito, verbatim de la opción A firmada: **describir la asociación seguro–denuncia en esa apertura, sin interpretación causal ni extrapolación a otros delitos.**

Esto es normativo, no una nota al pie. **Prohibiciones que esta spec impone a cualquier lectura de sus `RESULT`:**

1. **Prohibido leer causalmente.** Ningún `RESULT` de esta spec está rotulado causal y ninguno puede citarse como evidencia de que la cobertura de seguro **causa** la denuncia. `DELTA-CON-MENOS-SIN` es una **diferencia descriptiva entre dos estratos observados**, no un efecto. Quien tenga seguro difiere de quien no en vehículo, ingreso, lugar y mil cosas más que esta corrida **no** mide y **no** ajusta.
2. **Prohibido extrapolar a otros delitos.** Todo lo que aquí se mide vale **sólo** dentro de `BPCOD = 01`. Ningún `RESULT` puede citarse como tasa de denuncia «de los delitos asegurables», «del robo» en general, ni «de México». La restricción es parte del estimando, no una limitación que se supere promediando.
3. **Prohibido transportar entre olas.** Vale para ENVIPE **2025** y sólo esa ola. No hay serie aquí y no se construye ninguna.
4. **Prohibido cruzar con la otra apertura.** Estos cuatro `RESULT` **no** se suman, promedian ni comparan con los de `prereg-caja-ENVIPE-DENUNCIA` (razones de no denuncia): otra unidad, otro denominador, otra codificación.

### 8.5 · Secundarios declarados, NO adoptables

`DELTA-CON-MENOS-SIN` (con signo) y su IC de diseño se emiten como **descriptivo secundario**, sujeto íntegro a §8.4. No es un `RESULT` de demanda, no releva ningún `RES`, y mesa no lo adopta por esta spec.

---

## 9 · Método, tolerancia y congelamiento

### 9.1 · IC y tolerancia

IC95 y EE por **bootstrap de `UPM_DIS` con reemplazo dentro de `EST_DIS`**, conservando el número de UPM por estrato, **2 000** réplicas, `numpy.PCG64`, semilla `20260915`, percentiles 2.5/97.5; EE = desviación estándar de las réplicas. Un estrato con **una sola UPM se re-muestrea a sí mismo** (aporta varianza cero): **no se colapsa** —decisión de diseño que esta spec no está autorizada a tomar— y **no se descarta** —sesgaría el punto—. Si el conteo es `> 0`, `METODO-IC` sale `IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite inferior** de la anchura verdadera, nunca como IC exacto.

Tolerancia de flotante `1e-10` para suma-uno y para el replay; enteros y textos se comparan **exacto**.

### 9.2 · Congelamiento

- Esta spec queda **SELLADA** con su `sha256` en `forense/prereg-caja/ENVIPE-DENUNCIA-SEGURO-spec-v1_0.sha256` y cableada desde `data/corrida0/CALC-ENVIPE-DENUNCIA-SEGURO-0001/spec.yaml`. Donde la cara mecánica y ésta digan cosas distintas, **manda ésta**.
- **`medidor_ejecutado_al_congelar: NO`**, y el medidor **tampoco se escribe aquí**: es del acto de CAJA. Consecuencia declarada: `preflight` reporta `BLOQUEADO:script_ausente`, y **eso es correcto**.
- **`cuenta_gen2: PENDIENTE-DE-MESA`.** El OBJETO 10 autoriza **la apertura estrecha y su spec**, y dice «*corrida en caja*»; **no declara OBJETO sobre el contador GEN2**. El estándar `FP-367/368` exige autoridad + fecha + OBJETO explícito sobre el contador: hay autoridad y hay fecha, **falta el OBJETO**. Se dice aquí en vez de darlo por concedido.
- **Cero adopción.** Esta spec **no escribe cita en `milpa/` bajo ninguna rama**, ni en la rama `REPRODUCE`. Las entradas `civico.denuncia.con_seguro` / `sin_seguro` de `milpa/tramite.yaml` **no se tocan**. Si la corrida reproduce, sale `LISTADO-PARA-MESA-REPRODUCE`; si no, `LISTADO-PARA-MESA-NO-REPRODUCE`. En ambos casos **decide mesa por merge**, no este acto y no el de CAJA.
- **Nada sellado se edita.** `ENVIPE-DENUNCIA-spec-v1_0.md`, su sucesión `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0-CORRECCION-2026-09-15.md`, la propuesta y `tools/medidor_denuncia_seguro_envipe25.py` quedan **intactos**.

---

## 10 · Lo que NO pude verificar en nube, declarado como entregable

Con `data/raw/` ausente y E.5 permitiendo sólo codebook y metadato, queda **sin verificar** y se entrega como tal:

1. **Contenido de los catálogos.** Que `catalogos/bp2_1.csv` y `catalogos/bp1_20.csv` confirmen el mapa de §3.2/§3.3. El inventario prueba que los archivos **existen** y qué **columnas** traen (`BP2_1`/`BP1_20` + `descrip`); no prueba qué dicen. → guardia `NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA`.
2. **Unicidad de la llave de delito.** `ID_DEL` existe; su cardinalidad, no. → guardia `NO-ESTIMABLE-LLAVE-NO-UNICA` y `RESULT` `G-LLAVE-DELITO` que reporta cuál de las dos formas resultó única.
3. **Todo conteo de filas.** Filas del archivo, filas en `BPCOD = 01`, filas fuera por `BP2_1 = 9`, por `BP1_20` inválido o por peso no positivo. Nada de eso está en ninguna fuente del repo. Las cifras «1 028 de 40 280» (script antecedente) y `n = 402 / 614 / 1 016` (`milpa/`) son **referencias a contrastar**, no datos de este acto.
4. **Número real de estratos y UPM** en el universo y cuántos estratos quedan con UPM única. `milpa/` declara `200/377` y `289/567` para GEN1: referencia, no verificación.
5. **Que `FAC_DEL` sea finito y positivo** en todas las filas.
6. **Que el gemelo `envipe2025/bd_envipe_2025_csv.zip` traiga el mismo contenido** que el payload elegido. El inventario prueba que trae las mismas columnas; **no** que traiga las mismas filas. Por eso el gemelo **no se abre** y no hay caída a él (§1.2).

Ninguno de los seis bloquea el congelamiento: cada uno tiene su guardia o su `RESULT`, y una cifra que no se pueda sostener saldrá `NO-ESTIMABLE` en vez de salir bonita.
