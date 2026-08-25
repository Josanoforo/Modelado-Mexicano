# U2-CRUCE · Ficha B-bis — el cruce oficial-vs-propio, congelado antes de estimar

### `bbis-u2-cruce` · **v1.0** · 25 de agosto de 2026 · **COMMIT 1 — ESPECIFICACIÓN CONGELADA**

> | | |
> |---|---|
> | **ARCHIVO** | `bbis-u2-cruce-v1_0.md` |
> | **NOMBRE ESTABLE** | **`bbis-u2-cruce`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La ficha `B-bis` del `ACTO U2-CRUCE`, que ejecuta la opción **(a)** de `FP-70` (firma de mesa verbatim, `ADR-155(d)`: *«FP-70: a, y si fuera necesario exploramos el universo desconocido.»*) por su fila sucesora `FP-125`. Congela **antes** de estimar nada: cuáles son los dos estimandos y cómo los define el documento oficial (§1), por qué son distintos del pre-registro original y qué siguen validando (§2), las dos reservas que mesa dejó escritas al firmar (§3 y §4), qué vía calcula y qué desviación tiene respecto de `produce.py` (§5), universo y escalas (§6), el criterio de éxito — **uno solo** (§7), y la escala `B-bis` completa con su regla de precedencia (§8) |
> | **QUÉ NO ES** | No adjudica ningún veredicto del Hito D · no mueve el contador `18 de 27` · no toca `milpa/` ni el pre-registro del Hito D · no re-etiqueta ningún resultado sellado · no estima ningún coeficiente del modelo · no compara nada contra la θ sellada de `familismo_obligacion` (escala distinta, prohibido por `A-bis` regla 3) |
> | **VERIFICAS ASÍ** | §1 cita los dos renglones oficiales celda por celda, con hoja y fila · §3 deja la aritmética `NC90 → IC95` completamente a la vista · §4 fija el factor con cita textual del descriptor y del propio archivo oficial · §7 elige **un** criterio y lo escribe · §8 nombra los cinco desenlaces posibles y cuál manda si dos se satisfacen a la vez · §9 pre-declara tres comprobaciones estructurales que **no** adjudican · §12 cierra con la cláusula de primer resultado |
> | **ESTADO** | **CONGELADO.** El Commit 2 no edita este archivo. Si la especificación estaba mal, lo dice un commit posterior — nunca se corrige hacia atrás |

---

## 0 · Qué vio esta sesión antes de congelar, y qué no — declarado antes que nada

**Lo que esta sesión SÍ abrió antes de congelar esta ficha, y es lectura legítima porque el propio encargo la exige:**

| abierto | para qué | ¿contamina el resultado? |
|---|---|---|
| `IPE_CV-EE-IC_ENASIC_2022-00_Def_V1_260923.xlsx`, hoja `INDICADORES`, íntegra | §1 exige citar los dos renglones oficiales celda por celda | **No.** Es el lado *oficial* del cruce. Conocerlo antes es la definición misma de un cruce contra un valor publicado: el estimando es ese número |
| `enasic_2022_fd.xlsx`, hojas `TCSDemPO` / `TPER_ELE` / `THOGAR`, catálogo de variables | §4 exige *«la cita del descriptor que lo justifica»* para fijar el factor | **No.** Es metadato del instrumento, no dato |
| `enasic_2022_bd_csv.zip` — **sólo la estructura**: nombres de los 6 miembros, encabezados de columna, número de filas | fijar en §5/§6 qué tabla, qué columnas y qué universo se usan | **No.** Ninguna suma, ningún promedio, ningún ponderador acumulado. Ver el párrafo de abajo |

**Lo que esta sesión NO había hecho al congelar esta ficha, y es la frontera exacta que el encargo traza (*«antes de abrir el microdato para estimar»*):** no se sumó ni un solo `FAC_HOG`, no se contó ni una sola fila por valor de ninguna variable sustantiva, no se calculó ninguna varianza, ningún total, ninguna proporción. El Commit 1 de este acto **no contiene un solo número estimado a partir del microdato** — y eso es verificable en su diff, que es precisamente el sello que el encargo pide.

**Contaminación real, declarada y no minimizada:** esta sesión conoce los dos números oficiales antes de estimar. En un cruce contra un valor publicado eso es inevitable y es el diseño, pero tiene un costo concreto: si la corrida no reprodujera el número, quien la ejecuta está en posición de *buscar* la variante de universo o de factor que sí lo reproduzca. Contra eso van §4, §6 y §12: el factor, el universo y la regla de reporte quedan cerrados **aquí**, y el §12 obliga a reportar el primer resultado del procedimiento, no el mejor.

---

## 1 · Los dos estimandos, como el documento oficial los define

Fuente única, ya en corpus con `sha256` verificado: **`enasic2022_ipe_cv_ee_ic`** → `IPE_CV-EE-IC_ENASIC_2022-00_Def_V1_260923.xlsx`, `sha256 c37b5fc687ae9fc727d0cd1d883adef00165086e54453d3070b9eae51801c540`, 51 724 B. Es un `.xlsx`, no tiene paginación; **la coordenada equivalente a la página es hoja + fila**, y se cita así: **hoja `INDICADORES` (1 de 2; la otra es `Catálogo`), fila 2 y fila 3** — las dos únicas filas con contenido de las 337 barridas. Los encabezados son la fila 1, 21 columnas (`Tipo_Programa` … `IntConf_Sup`).

**Fila 2 — estimando U2-E1**, celda por celda, verbatim:

| columna | valor |
|---|---|
| `Tipo_Programa` | `2` |
| `Unidad_Ad` | `DGES` |
| `Programa` | `ENASIC` |
| `Año` | `2022` |
| `Unidad_Obs` | **`Población`** |
| `Clave_Entidad` / `Nombre_Entidad` | `00` / `Nacional` |
| `Dominio_estudio` / `Nivel_Agreg_Dom` | `Nacional` / `Nacional` |
| `Variable` | **`Población total (Se excluyen 21,090 casos que no especificaron la edad de la población menor de 15 años)`** |
| `Parametro` | `Total` |
| `Estimación` | **`128857388`** |
| `CV` | `1.391962655` |
| `ErrorEst` | `1793646.71919227` |
| `Niv_Conf` | **`90`** |
| `IntConf_Inf` / `IntConf_Sup` | `125907101.688467` / `131807674.311533` |

**Fila 3 — estimando U2-E2**, mismas 13 primeras columnas salvo `Variable`:

| columna | valor |
|---|---|
| `Variable` | **`Sí requirió apoyo o cuidados (Se excluyen 21,090 casos que no especificaron la edad de la población menor de 15 años)`** |
| `Parametro` | `Total` |
| `Estimación` | **`58594471`** |
| `CV` | `1.6048742386` |
| `ErrorEst` | `940367.570351719` |
| `Niv_Conf` | **`90`** |
| `IntConf_Inf` / `IntConf_Sup` | `57047703.9912394` / `60141238.0087606` |

**Coherencia interna del archivo oficial, verificada aquí y no supuesta** (aritmética sobre el lado oficial, no una estimación nuestra):

```
U2-E1:  CV/100 x Estimación = 1.391962655/100 x 128857388 = 1793646.719168   (publicado 1793646.71919227; dif -0.000024)
     (Estimación - IntConf_Inf)/ErrorEst = 1.644853627
     (IntConf_Sup - Estimación)/ErrorEst = 1.644853627
U2-E2:  CV/100 x Estimación = 1.6048742386/100 x 58594471 =  940367.570323   (publicado  940367.570351719; dif -0.000029)
     (Estimación - IntConf_Inf)/ErrorEst = 1.644853627
     (IntConf_Sup - Estimación)/ErrorEst = 1.644853627
```

Los tres campos (`Estimación`, `CV`, `ErrorEst`, `IntConf_*`) son mutuamente consistentes a la sexta cifra decimal, y el `z` implícito es **1.644853627** en los cuatro extremos — el cuantil normal exacto de dos colas al 90 %, no un `1.645` redondeado. Esto importa para §3: la conversión de nivel de confianza no tiene que adivinar qué constante usó el INEGI.

---

## 2 · El estimando es DISTINTO del pre-registrado. Una línea, y por qué no lo invalida

**La línea:** el pre-registro de `U2/EV-1` (`forense/notas/2026-08-19-u2-ev1-paro-red.md` §5) fijó como objeto el **EE del reactivo `P7_12_7`** de `familismo_obligacion`, y el archivo oficial adquirido **no publica ese reactivo** (`NO-ENCONTRADO` con universo `A.4` de cinco vías, `ADR-126(a)`); este acto cruza en su lugar **dos totales poblacionales nacionales** — un estimando distinto, sobre la misma encuesta, la misma edición y el mismo diseño muestral.

**Por qué eso no lo invalida como validación de pipeline, y qué exactamente valida:** lo que se pone a prueba no es la regla vieja sino la **maquinaria**. Concretamente, y esto es lo comparable:

| pieza de la maquinaria | ¿la ejercía la θ sellada `ESP-OPACA-B-d13ec4fe`? | ¿la ejerce este cruce? |
|---|---|---|
| lectura del mismo ZIP de microdato (`sha256 8a5e8c5e…`) | sí (`TPER_ELE.csv`) | sí (`TCSDEMPO.csv`) |
| expansión por ponderador declarado | sí (`FAC_ELE`) | sí (`FAC_HOG`) |
| estrato `EST_DIS` + conglomerado último `UPM_DIS` | sí | sí — **las mismas dos columnas, el mismo diseño** |
| varianza por conglomerados últimos / linealización de Taylor | sí | sí — **el mismo estimador de varianza** |
| forma del estimando | proporción de una categoría | **total poblacional** |

Las cuatro primeras filas son idénticas; la quinta no. Por eso el veredicto de este acto se enuncia **sobre la maquinaria de ponderación y diseño**, y jamás sobre la regla vieja ni sobre el valor de la θ: `A-bis` regla 3 prohíbe explícitamente comparar entre escalas, y una proporción y un total son escalas distintas. Este acto **no** dice nada sobre si θ = 69.33 % es correcto.

---

## 3 · Reserva (i), resuelta — `NC90 → IC95` con la aritmética a la vista

**Qué pide la reserva** (`FP-70`, arrastrada literalmente por `FP-125` y por `ADR-155(d)`): *«el oficial reporta a Niv_Conf 90 y lo propio es IC95, hay que convertir con la fórmula a la vista»*.

**Cuál de los dos lados se convierte, y por qué.** Se convierte el **lado oficial**, no el nuestro. Razón: nuestro intervalo lo produce el motor a IC95 por construcción (`produce.py` multiplica por `1.96` de forma fija, `taylor_distribution`), y reescribir el motor está fuera del perímetro de este acto; el lado oficial, en cambio, publica el **error estándar** directamente, de modo que su intervalo a cualquier nivel es aritmética de una línea sobre un dato publicado, sin re-estimar nada.

**La fórmula, explícita:**

```
IC(1-α) oficial = Estimación ± z(1-α/2) × ErrorEst
z(0.95)  = 1.6448536269514715      ← el que INEGI usó (§1 lo verifica: 1.644853627 en los 4 extremos)
z(0.975) = 1.9599639845400536      ← el que este cruce necesita
```

**La aritmética, completa, para los dos estimandos:**

```
U2-E1 · Población total
   semiamplitud IC95 = 1.9599639845400536 × 1793646.71919227 = 3515482.970605
   IC95 oficial      = 128857388 − 3515482.970605  ,  128857388 + 3515482.970605
                     = [ 125341905.029395 , 132372870.970605 ]
                     ≈ [ 125,341,905 , 132,372,871 ]  personas
   (a modo de control: el IC90 publicado es [125907101.688467 , 131807674.311533],
    semiamplitud 2950286.311533 = 1.6448536… × 1793646.71919227 ✓)

U2-E2 · Sí requirió apoyo o cuidados
   semiamplitud IC95 = 1.9599639845400536 × 940367.570351719 = 1843086.570119
   IC95 oficial      = 58594471 − 1843086.570119  ,  58594471 + 1843086.570119
                     = [ 56751384.429881 , 60437557.570119 ]
                     ≈ [ 56,751,384 , 60,437,558 ]  personas
   (control: IC90 publicado [57047703.9912394 , 60141238.0087606],
    semiamplitud 1546767.008761 = 1.6448536… × 940367.570351719 ✓)
```

**Supuesto declarado, no escondido:** la conversión asume que el intervalo oficial es simétrico normal alrededor del punto — supuesto que **el propio archivo confirma**, porque su `IntConf_Inf`/`IntConf_Sup` son exactamente `Estimación ∓ 1.6448536 × ErrorEst` a la sexta decimal (§1). No se asume nada sobre cómo INEGI calculó `ErrorEst`; sólo sobre cómo construyó el intervalo a partir de él.

**Estos dos IC95 son el criterio de §7 y quedan congelados aquí.**

---

## 4 · Reserva (ii), resuelta — el factor, fijado ANTES de correr, con cita

**Qué pide la reserva:** *«la fila oficial cuenta PERSONAS mientras el factor de esa tabla se llama `FAC_HOG` — el factor correcto se fija ANTES de correr, no después»*.

**Decisión, congelada: se usa `FAC_HOG` de `TCSDEMPO.csv`.** Sin reescalar, sin dividir entre tamaño de hogar, sin usar ningún otro factor del ZIP.

**Las tres citas que la justifican:**

1. **El propio archivo oficial declara su unidad de observación.** Hoja `INDICADORES`, columna 8 (`Unidad_Obs`), filas 2 y 3: **`Población`**. El renglón oficial cuenta personas — no lo inferimos, lo dice él.
2. **El descriptor declara que la unidad de fila de `TCSDemPO` es la persona.** `enasic_2022_fd.xlsx`, hoja `TCSDemPO`, bloque `LLAVE PRIMARIA`: *«Llave de identificación **del residente en el hogar**»* → `LLAVESDE`, alfanumérico, 8. Cada fila del archivo es **un residente**, no un hogar. La especificación ya sellada del programa lo dice con las mismas palabras al excluirlo de su propio universo: `ESP-OPACA-B-d13ec4fe`, campo `poblacion`, verbatim — *«No es TCSDEMPO (residentes en general)…»*.
3. **Por tanto la suma de `FAC_HOG` sobre `TCSDEMPO.csv` expande personas.** `FAC_HOG` es el factor de expansión del hogar replicado en cada renglón de residente: cada persona del hogar hereda el factor de su hogar, y sumarlo **sobre renglones-persona** estima personas, exactamente como sumarlo **sobre renglones-hogar** (`THOGAR.csv`) estima hogares. **Lo que fija la unidad del estimando no es el nombre del factor: es la unidad de fila del archivo sobre el que se suma.**

**Hallazgo que esta ficha registra al resolver la reserva, y que la reserva no anticipaba:** el descriptor **no distingue los factores por su etiqueta**. Las tres tablas relevantes traen literalmente el mismo concepto escrito — `TCSDemPO` fila 770: *«FACTOR HOGAR DE EXPANSIÓN | `FAC_HOG` | Numérico | 6 | 708 - 34887»*; `THOGAR` fila 265: *«FACTOR HOGAR DE EXPANSIÓN | `FAC_HOG` | Numérico | 6 | 708 - 34887»*; y **`TPER_ELE` fila 1067: *«FACTOR HOGAR DE EXPANSIÓN* | `FAC_ELE` | Numérico | 6 | **702 - 166061**»* — un factor de persona elegida, con rango distinto, etiquetado *«FACTOR HOGAR»* igual que los otros dos. La etiqueta del descriptor es, para este propósito, **inservible como oráculo**; el rango y la unidad de fila sí discriminan. Ésta es exactamente la trampa que la reserva de mesa olfateó, y queda escrita.

**Los otros factores del ZIP, y por qué ninguno sirve aquí** (barrido completo de los 6 miembros, ninguno omitido): `TVIVIENDA.csv`/`FAC_VIV` expande viviendas · `THOGAR.csv`/`FAC_HOG` expande hogares · `THOG_UNIP.csv`/`FAC_UNI` expande hogares unipersonales · `TPER_ELE.csv`/`FAC_ELE` expande *personas elegidas* de 15 a 60 años, una por hogar — **no** la población total · `TPOB_CUI.csv`/`FAC_CUI` expande población cuidadora · `TCSDEMPO.csv`/`FAC_HOG` expande **residentes**, y es el único cuyo universo de fila es la población completa. Es el único candidato posible para un estimando cuya `Unidad_Obs` es `Población`.

---

## 5 · La vía de cálculo — y la desviación respecto de `produce.py`, declarada

**Lo que la fila nombra.** `FP-70` dice que el microdato *«trae el diseño completo que `tools/curador_registro/produce.py` necesita»*, y el encargo admite *«`produce.py` (o la vía que la fila nombre)»*.

**La desviación, medida y declarada antes de correr:** `produce.py::taylor_distribution` **no puede producir el estimando de este cruce.** Leído el código (`tools/curador_registro/produce.py`, líneas 56-151), su salida es una **distribución de proporciones** por categoría: calcula `proportion = category_weight / total_weight` y linealiza la varianza de esa **razón**, centrando cada conglomerado por `p` (`psu_z[(estrato,upm)] += w × (1[y=c] − p)`). Un total poblacional no es una razón y su varianza no se centra por `p`. Correr `produce.py` tal cual devolvería proporciones, no los 128.9 y 58.6 millones que el renglón oficial publica.

**Lo que se hace en su lugar, y por qué es la misma maquinaria y no otra:** se usa el **mismo estimador de conglomerados últimos** que `produce.py` ya implementa —misma partición por `EST_DIS`, mismos conglomerados `UPM_DIS`, mismo factor de corrección `m/(m−1)`— aplicado a la forma de **total** en vez de la de razón:

```
Ŷ        = Σ_{r ∈ U}  w_r · y_r
z_{h,i}  = Σ_{r ∈ UPM i del estrato h, r ∈ U}  w_r · y_r
V̂(Ŷ)    = Σ_h  [ m_h / (m_h − 1) ] · Σ_i ( z_{h,i} − z̄_h )²        con  z̄_h = (1/m_h) Σ_i z_{h,i}
EE(Ŷ)    = √ V̂(Ŷ)
CV(Ŷ)    = EE(Ŷ) / Ŷ × 100
IC95(Ŷ)  = Ŷ ± 1.9599639845400536 × EE(Ŷ)
```

Es la **única** diferencia con el código sellado: donde `produce.py` acumula `w·(1[y=c] − p)`, aquí se acumula `w·y`. Todo lo demás —partición, factor `m/(m−1)`, tratamiento de estratos con una sola UPM— se conserva idéntico.

**Tres convenciones de estimación que se fijan aquí y no después:**

1. **La estructura de diseño (`m_h`, qué UPM existen en cada estrato) se cuenta sobre la muestra COMPLETA de `TCSDEMPO.csv`**, no sobre el dominio. Una UPM sin ningún miembro del dominio aporta `z_{h,i} = 0`, no desaparece. Es la convención estándar de estimación por dominios, y es la que evita inflar artificialmente la varianza de `U2-E2`.
2. **Estratos con una sola UPM:** si aparece alguno, el acto lo **reporta con su lista y su conteo** y no lo colapsa en silencio — misma respuesta que `produce.py` (que levanta `ESTRATOS_UNA_UPM`). Si aparecen, el resultado se declara `NO_ESTIMABLE` para el estimando afectado y eso **es** el resultado que se reporta (§12).
3. **Sin corrección por población finita, sin recalibración, sin recorte de pesos.** Los pesos se toman tal cual vienen del archivo.

**Dónde vive el script:** en `scratchpad`, que el PERÍMETRO incluye — no se añade código a `tools/`, que está fuera. Para que el cálculo sea reproducible sin depender del scratchpad, **su código fuente completo se pega verbatim en la nota del acto**, junto con su `sha256`.

---

## 6 · Universo y escalas, declaradas

**Universo `U`, congelado** (estampa `A.10`): los renglones de **`TCSDEMPO.csv`** (miembro del ZIP `enasic_2022_bd_csv.zip`, `sha256 8a5e8c5ed2dcda6e25dfe2dd630c0ac7273e0736e7b99662a15a4ef68c3ab36e`), **21 776 renglones, 181 columnas**, **menos** los renglones con `EDAD = '99'`.

**Por qué `EDAD = '99'` y no otra cosa:** los dos renglones oficiales excluyen, textualmente, *«los casos que no especificaron la edad de la población menor de 15 años»*. El descriptor de `TCSDemPO` codifica exactamente eso en un solo valor: `EDAD`, alfanumérico 2 — *«`98` = No sabe, en personas de **15 años y más**; `99` = No sabe, en personas **menores de 15 años**»*. Se excluye **`99` y sólo `99`**: `98` es la no-respuesta de edad del otro grupo y el renglón oficial no lo menciona.

| cantidad | símbolo | escala declarada |
|---|---|---|
| U2-E1 · Población total | `Ŷ₁` | **personas** (conteo poblacional expandido) |
| U2-E2 · Sí requirió apoyo o cuidados | `Ŷ₂` | **personas** (conteo poblacional expandido) |
| error estándar de diseño de cada uno | `EE(Ŷ)` | **personas** |
| coeficiente de variación | `CV` | **porcentaje** (adimensional) |
| razón de discrepancia de EE (§9c) | `\|EE_propio − EE_oficial\| / EE_oficial` | **adimensional** |
| tamaño de muestra | `n` | **renglones-persona** (no hogares, no viviendas) |

**Prohibido por esta ficha, y es `A-bis` regla 3:** comparar cualquiera de estas cantidades contra la θ sellada de `familismo_obligacion` (0.6933) o contra su EE (0.0106). Son proporciones sobre otra tabla y otra subpoblación; no hay función de enlace declarada y no la habrá aquí.

**Operacionalización de `U2-E2`, congelada, con su reserva.** `y₂ = 1` si el renglón trae **`1` (= Sí)** en **cualquiera** de las cinco banderas de identificación de la Sección 4 del propio archivo —`PN_CDISC`, `PN_C0005`, `PN_C0617`, `PN_C60MA`, `PN_CETEM`—, `0` en otro caso. La sección se titula, verbatim en el descriptor, *«SECCIÓN 4. IDENTIFICACIÓN DE PERSONAS DEL HOGAR QUE NECESITAN CUIDADOS»*, y las cinco banderas son sus identificadores derivados (`1` = Sí · `2` = No · `b` = Blanco por secuencia), una por módulo: discapacidad, 0-5 años, 6-17 años, 60 y más, enfermedad temporal. La disyunción evita el doble conteo de quien cae en dos módulos.

> **Reserva de `U2-E2`, escrita antes de correr y no después:** el archivo oficial **no publica el mnemónico** de su renglón *«Sí requirió apoyo o cuidados»* — sólo la etiqueta en prosa. La operacionalización de arriba es una **derivación del descriptor**, no una lectura de la definición oficial. En consecuencia, una discrepancia en `U2-E2` es **ambigua** entre defecto de pipeline y operacionalización distinta, y §8 la trata como tal. `U2-E1` no tiene esta ambigüedad: su universo lo define el propio renglón oficial.

---

## 7 · Criterio de éxito, pre-declarado — **uno**, elegido aquí

El encargo ofrece dos y exige elegir **uno**. Se elige:

> ### **Nuestro punto estimado cae dentro del IC95 oficial.**
> Formalmente, para cada estimando `k ∈ {1,2}`:  `IC95_oficial_inf(k) ≤ Ŷ_k ≤ IC95_oficial_sup(k)`, con los dos intervalos que §3 dejó calculados:
> * **U2-E1:** `125 341 905.03 ≤ Ŷ₁ ≤ 132 372 870.97`
> * **U2-E2:** ` 56 751 384.43 ≤ Ŷ₂ ≤  60 437 557.57`

**Por qué éste y no el traslape de intervalos.** Tres razones, todas escritas antes de ver el resultado:

1. **Es el más exigente de los dos.** El traslape de dos IC95 centrados casi en el mismo punto es casi imposible de fallar: con un `CV` oficial de 1.39 %, dos intervalos se seguirían tocando aun con un error relativo de nuestro lado del orden del 5 %. El criterio de punto-dentro es estrictamente más estrecho y por tanto informa más.
2. **Aísla el confundido metodológico.** El traslape depende de **nuestro** EE, y nuestro EE puede diferir del oficial por método de varianza (calibración, corrección por población finita, bootstrap) sin que haya defecto alguno en el pipeline. El criterio de punto-dentro depende sólo de nuestro **estimador puntual** y del EE **oficial** — el confundido se sale de la adjudicación y baja a diagnóstico (§9c).
3. **Es el que puede fallar de verdad.** Ŷ es aritmética determinista sobre el archivo: si nuestra lectura del ponderador, del universo o de la tabla está mal, el punto se va y se va lejos, no un poco.

**Regla de suficiencia, pre-declarada:** el criterio se evalúa **por separado** para `U2-E1` y `U2-E2`, y **`U2-E1` es el estimando primario** — porque su operacionalización no tiene la ambigüedad de `U2-E2` (§6, reserva).

**`A-bis`, la contraparte, aplicada por adelantado:** un punto que satisface el umbral con un intervalo **propio** que no lo despeja no adjudica; se reporta como **propuesta con la reserva escrita**. Todo veredicto de este acto es, por tanto, **propuesto**, nunca firmado por el ejecutor.

---

## 8 · La escala `B-bis` — qué significa que NO refute, y quién manda

`B-bis` exige declarar, antes de correr, qué pasa si el falsador no refuta, y qué fila manda si dos pueden satisfacerse a la vez. Los cinco desenlaces posibles, cerrados:

| # | desenlace | condición, pre-declarada | qué significa |
|---|---|---|---|
| **1** | **`PIPELINE CORROBORADO`** | `Ŷ₁` y `Ŷ₂` dentro de su IC95 oficial **y** la razón de discrepancia de EE (§9c) ≤ 0.15 en los dos | La maquinaria de ponderación + diseño + varianza **reproduce al INEGI** sobre este instrumento. Primera validación externa material del programa: pasa de 0 a **1** |
| **2** | **`PIPELINE CORROBORADO · DISCREPANCIA ACOTADA`** | `Ŷ₁` y `Ŷ₂` dentro **pero** la razón de EE > 0.15 en al menos uno | El **estimador puntual** reproduce; el de **varianza** difiere, y la diferencia queda **medida y acotada**. No adjudica cuál de los dos métodos de varianza es el correcto — eso exigiría el documento metodológico de INEGI a nivel de fórmula, que este acto no tiene. Cuenta como validación externa **con reserva** |
| **3** | **`NO CONCLUYENTE POR OPERACIONALIZACIÓN`** | `Ŷ₁` dentro, `Ŷ₂` fuera | La operacionalización derivada de `U2-E2` (§6) no coincide con la del INEGI. **No es evidencia de defecto de pipeline** y no se reporta como tal: `U2-E1` ya mostró que la maquinaria lee bien. Se reporta el tamaño de la brecha de `U2-E2` como dato, sin veredicto |
| **4** | **`REFUTADO · DEFECTO DE PIPELINE`** | `Ŷ₁` **fuera** de su IC95 oficial | Defecto material en la lectura de microdato, ponderador o universo. **Bloquea** el uso de todo resultado producido por la misma vía hasta remediarse, y es el desenlace más informativo de los cinco |
| **5** | **`PRUEBA DÉBIL`** | El criterio se satisface pero se descubre, al correr, que no podía fallar — p. ej. si el IC95 oficial resultara tan ancho que cualquier lectura plausible cayera dentro | El acto no informa sobre el pipeline. Se dice, no se maquilla como corroboración |

**Regla de precedencia, exigida por `B-bis` y fijada aquí:** si dos filas pudieran satisfacerse a la vez, **manda la fila 4** sobre todas (un `U2-E1` fuera es defecto, y ningún acierto en `U2-E2` lo compensa); después manda la **fila 5** sobre 1, 2 y 3 (una prueba que no podía fallar no corrobora nada, aunque el criterio se cumpla); después la **fila 3** sobre 1 y 2 (`U2-E2` fuera bloquea la lectura fuerte aunque `U2-E1` acierte); y **la fila 2 manda sobre la 1**. Esta escala gobierna sobre cualquier lectura genérica de «pasó / no pasó».

**Lo que este acto declara ANTES de ver el dato que sería interesante si NO refuta** —`B-bis` lo pide expresamente—: la corroboración es aquí **más informativa que la refutación para el programa**, porque hoy el programa tiene **cero** validaciones externas y una θ sellada (`familismo_obligacion`, 69.33 %) cuyo IC95 se produjo por esta misma maquinaria de varianza sin que nadie de fuera la haya contrastado nunca. Si el desenlace es 1 o 2, ese IC95 gana por primera vez respaldo externo — y eso se dice ahora, no después, para que nadie lea la corroboración como un acto sin hallazgo.

**Y lo que sigue siendo cierto en los cinco desenlaces:** este acto **no** convierte a `familismo_obligacion` en `LISTA_PARA_USO_MODELO`, **no** mueve `18 de 27`, y **no** adjudica ningún coeficiente. Ninguna fila de esta escala puede hacerlo.

---

## 9 · Tres comprobaciones estructurales pre-declaradas — **no adjudican**

Se calculan y se reportan **siempre**, sea cual sea el desenlace. Ninguna mueve el veredicto de §8; existen para que una discrepancia, si aparece, se pueda localizar en vez de sólo constatarse.

**(a) La exclusión del universo se puede verificar contra el propio renglón oficial.** El renglón dice que excluye **21 090 casos**. Si nuestra lectura del universo es la del INEGI, entonces:

```
Σ FAC_HOG sobre TODOS los renglones de TCSDEMPO  −  Σ FAC_HOG sobre {EDAD ≠ '99'}  =  21 090
```

Se pre-declara el valor esperado **exacto**: `21 090`. Si sale otra cosa, la regla de universo de §6 no es la del INEGI y eso se reporta como reserva de `U2-E1`, **sin cambiar el criterio de §7** — el criterio ya está congelado y se evalúa igual.

**(b) Coherencia persona/hogar del factor.** `Σ FAC_HOG` sobre `TCSDEMPO.csv` (renglones-persona) dividido entre `Σ FAC_HOG` sobre `THOGAR.csv` (renglones-hogar) debe dar el **tamaño medio de hogar**, que para México en 2022 está en el orden de **3.3 a 3.8**. Es la comprobación de que §4 no confundió la unidad. Fuera de ese rango, la decisión de factor queda en duda y se dice.

**(c) Diagnóstico de error estándar — con umbral heredado, no inventado aquí.** Se reporta, para los dos estimandos:

```
razón = |EE_propio − EE_oficial| / EE_oficial      contra el umbral 0.15
```

El **0.15 no se inventa en esta ficha**: es el mismo umbral de discrepancia material que el pre-registro de `U2/EV-1` ya había fijado en su §5 (*«razón `|EE_propio − EE_oficial| / EE_oficial > 0.15`, mismo umbral que `ADR-80`/`benchmark-enlace-invarianza` usa para invarianza — no se inventa uno nuevo»*). Entra en §8 sólo para separar la fila 1 de la fila 2; **no** puede por sí solo producir un `REFUTADO`.

---

## 10 · Falsador, y lo que este acto NO puede concluir

**Qué falsaría el veredicto de este acto, si sale corroboración:** que el mismo cruce, corrido sobre otro instrumento del corpus con indicadores oficiales de precisión publicados (hoy no hay ninguno más adquirido: el segundo recurso de la ficha RNM 922 es la plantilla del formato estandarizado, sin estimaciones — `ADR-126(a)`), diera un punto fuera del IC95 oficial. Corroborar aquí no generaliza: valida **esta** vía sobre **este** diseño.

**Cuatro cosas que este acto no puede concluir, y quedan escritas antes de correr:**

1. **No puede concluir que el EE del motor sea correcto en general.** Reproduce (o no) un EE de **total** bajo un diseño estratificado por conglomerados últimos. La θ sellada es una **proporción** sobre otra tabla; que la varianza de un total coincida no demuestra que la de una razón coincida, aunque comparten el estimador.
2. **No puede distinguir «nuestro método de varianza» de «el método de varianza del INEGI»** si difieren. El archivo oficial publica el número, no la fórmula; el documento metodológico que declara *«Conglomerados Últimos junto con… Series de Taylor»* no fija si hay corrección por población finita ni cómo se trata la calibración de los factores.
3. **No puede validar la operacionalización de `U2-E2`** (§6, reserva). Un acierto en `U2-E2` es *compatible* con que nuestra derivación coincida con la del INEGI; no la demuestra.
4. **No puede convertirse en una validación del instrumento.** Nuestro estimador y el del INEGI se calculan sobre **la misma muestra**: no son dos mediciones independientes de México, son dos lecturas del mismo archivo. Lo que se prueba es la lectura, no el dato. Esto es exactamente lo que hace de la fila 5 (`PRUEBA DÉBIL`) un desenlace posible y no una formalidad.

---

## 11 · Contadores que este acto mueve

* **Hito D:** cero. No archiva ninguna corrida de regla, no mueve `18 de 27`.
* **Coeficientes medidos:** cero. No estima ningún coeficiente del modelo.
* **Validaciones externas materiales:** hoy **0**. Pasa a **1** si el desenlace es fila 1 o fila 2 de §8; se queda en **0 con razón escrita** en las filas 3, 4 y 5. Es la población propia que el encargo declara bajo `v2.3`.
* **Payloads nuevos al manifiesto:** cero. Este acto **no descarga nada**; los tres insumos ya están en corpus con `sha256` verificado uno por `--id` (`A.1`).

---

## 12 · La cláusula de reporte

**El primer resultado que produzca este procedimiento es el que se reporta.** No hay segunda corrida, no hay variante de universo, no hay factor alternativo, no hay ajuste de la operacionalización de `U2-E2` para acercarse al número oficial. Si el resultado contradice esta ficha, el Commit 2 lo dice y un commit posterior explica en qué se equivocó la ficha — **nunca se corrige hacia atrás**.

---

## Enmienda in situ · 25 de agosto de 2026 · `ACTO U2-CRUCE`, Commit 3 — **la ficha estaba mal en un punto**

**Qué estaba mal.** Esta ficha nombró sus dos estimandos con la letra `E` seguida de un dígito, sin prefijo de espacio: rótulos **pelados** de esa familia, que es exactamente lo que `D-6` (`ADR-128`, `ACTO SELLA-ADV`, 20/ago/2026) prohíbe crear desde ese día — *«lo que ya está en uso se registra, no se renombra; ningún rótulo NUEVO puede ser letra+número pelado»*. La regla nació de una colisión medida: siete rótulos distintos de esa misma familia conviviendo en el rango de `0` a `5`, uno de ellos citado por nombre en una fila del tablero. `T25` marcó `FAIL` los dos archivos nuevos de este acto, que es precisamente para lo que existe. Los rótulos viejos no se reproducen aquí en su forma pelada, a propósito: escribirlos volvería a crear el defecto que esta enmienda corrige — mención y uso no se distinguen para un test de rótulos.

**Qué se corrige, y qué NO.** Se renombran los **30** rótulos de esta ficha a **`U2-E1`** y **`U2-E2`** — prefijo de espacio del propio acto, la forma que `D-6` exige. **Ninguna otra cosa cambia**: ni un estimando, ni un intervalo, ni el criterio, ni la escala `B-bis`, ni una cifra. El renombrado es de token, no de sustancia.

**Por qué esto no es «corregir hacia atrás».** La cláusula §12 y la del encabezado protegen contra mover la *especificación* después de ver el resultado, que es lo que falsearía el pre-registro. Un rótulo que viola una regla de canon no es especificación: es forma, y `D-6` manda sobre la auto-congelación de cualquier ficha. El encargo lo previó con estas palabras — *«Si la ficha estaba mal: tercer commit que lo diga; nunca hacia atrás»* — y esto es ese commit: **lo dice**, en vez de arreglarlo en silencio dentro del Commit 2.

**Trazabilidad de la corrida.** El script usaba los mismos rótulos en cuatro cadenas de impresión. Se produjo una `v2` que cambia **sólo esas cuatro cadenas** (`sha256 3b36e1c4…` → `f25e84a9…`) y se volvió a correr. Las dos salidas son **idénticas byte a byte tras normalizar los rótulos**, verificado por `cmp`; el diff completo va en la nota del acto. **Ninguna cifra reportada cambia**, así que §12 se mantiene: lo que se reporta sigue siendo el primer —y único— resultado del procedimiento.
