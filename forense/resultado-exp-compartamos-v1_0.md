# `EXP-COMPARTAMOS-1` — ejercicio de la llave: resultado

### `resultado-exp-compartamos-v1_0` · **v1.0** · 26 de agosto de 2026 · ENTORNO UBUNTU · `ACTO MAESTRA30-E3 · EJERCE-LLAVE-COMPARTAMOS`

> | | |
> |---|---|
> | **ARCHIVO** | `forense/resultado-exp-compartamos-v1_0.md` |
> | **NOMBRE ESTABLE** | **`resultado-exp-compartamos-v1_0`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | El ejercicio de la llave de identificación `EXP-COMPARTAMOS-1` (clase (iii)) bajo la spec sellada `spec-bbis-exp-compartamos-v1_0-propuesta` (`FP-160` `FIRMADA`, `ADR-199`). Dos commits, en este orden y sin reescritura hacia atrás: **§COMMIT-1** congela el procedimiento antes de abrir un solo valor del microdato; **§COMMIT-2** reporta lo que ese procedimiento produjo y adjudica por la escala §4 de la spec. |
> | **QUÉ NO ES** | No sustituye el `[MEDIA](a)` de `dinero.credito.baja_friccion_usura_dano_downstream` — eso exige acto propio de mesa (§3 de la spec). No estima TOT/LATE. No usa `BTreatment`/línea base. No compara contra la escala de `dinero.credito.scoring_alternativo`. No toca `milpa/`. |
> | **VERIFICAS ASÍ** | §COMMIT-1 está en un commit anterior al de §COMMIT-2 en el historial de este repositorio (`git log --follow forense/resultado-exp-compartamos-v1_0.md`), y el diff del segundo no toca una sola línea del primero. |

---

## §COMMIT-0 · Compuerta cero — la firma que habilita este acto

**Fila `FP-160` de `forense/firmas-pendientes.tsv:158`, campo `estado`, verbatim: `FIRMADA`.** Campo `firmada_en`, verbatim:

> `ADR-199, 26/ago/2026 -- firma de mesa verbatim: "SELLO FP-160: la spec B-bis de EXP-COMPARTAMOS-1 queda sellada tal como está propuesta." Mesa elige (a): sella el texto tal cual -- pasa a v1.0 congelada, habilita el acto EJERCE-LLAVE posterior en UBUNTU. Enmienda de ESTADO, no de archivo: forense/spec-bbis-exp-compartamos-v1_0-PROPUESTA.md conserva su nombre (las citas viven con ese nombre); queda declarada "sellada, vigente" en ADR-199 y en este tablero.`

**`ADR-199` (`canon/gobernanza-v1_15.md`), sección `L4`, verbatim:**

> **L4 — `FP-160` sella la spec B-bis de `EXP-COMPARTAMOS-1`.** Mesa elige la opción (a) de la fila: sella el texto tal cual — pasa a v1.0 congelada, habilita el acto `EJERCE-LLAVE` posterior en `UBUNTU`. **Enmienda de ESTADO, no de archivo** […] Gatea, sin ejecutarlo, el acto futuro `EJERCE-LLAVE` — **este acto no abre el microdato de `116334-V1.zip`**. […] El numerador sube a `5` de `5` solo cuando el acto `EJERCE-LLAVE` corra el diseño.

**Lo que la firma NO eligió.** La fila `FP-160` planteaba **dos** disyuntivas: sellar/no sellar el texto, y elegir el destino del número futuro entre (a) competir por el `[MEDIA](a)` y (b) entrar como fila nueva de la octava clase de `milpa/procedencia.yaml`. El campo `firmada_en` y `ADR-199 §L4` resuelven **solo la primera**. El destino queda sin elegir; la `RANURA DE MESA — DESTINO M-EXPCOMP` del encargo de este acto llegó **VACÍA**. Consecuencia aplicada en §COMMIT-2 §5: el número queda **PROPUESTO**, `milpa/` no se toca, y se abre fila nueva de tablero para que mesa elija — mismo patrón que `CAL-G3` (`EJERCIDA_ACOTA` con β `PROPUESTO`, `FP-127`).

**Hash del payload.** `data/manifiesto.yaml:12448`, `id: 116334_v1`, `archivo: Descargas Manuales/116334-V1.zip`, `raiz: descargas_mx`, `sha256: 776d56bf91535beaecef9480c352b022c3aec1ec7fae36c969ccdf6c8cc89d1c`, `tamano_bytes: 1404772`. Una invocación de `python3 tests/manifiesto.py --verifica` (951 líneas de reporte, 790 payloads con veredicto), línea 609, verbatim:

> `116334_v1 [descargas_mx]: COINCIDE -- sha256 y tamaño (1404772 bytes) verificados contra data/manifiesto.yaml`

**A.1 — las tres respuestas no se colapsan, y aquí se vieron dos de las tres.** La **primera** invocación en esta caja devolvió, para este mismo payload: `116334_v1 [descargas_mx]: RAÍZ NO CONFIGURADA -- este entorno no define 'descargas_mx' en data/raices.local.yaml`. Eso **no es** `AUSENTE` ni es hash discordante: es la tercera respuesta, y significa que el verificador **no examinó ni un archivo** para ese payload. Se resolvió configurando `data/raices.local.yaml` (gitignorado, `\.gitignore:7`) con `descargas_mx: /mnt/c/Users/PC0/Descargas MX`, copiado del clon principal, y **solo entonces** la respuesta pasó a `COINCIDE`. `AUSENTE`: 0 ocurrencias en el reporte. Hash discordante: 1 en todo el manifiesto (`endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf [data_raw]: NO COINCIDE`, `:323`) — **ajeno a este acto y a su perímetro**, se declara y no se toca.

**A.13 — un negativo de un comando que no examinó archivos no es un negativo.** Al buscar el payload, un primer `find /mnt/c/Users/PC0 -maxdepth 2 -name "116334*"` salió vacío. Ese vacío **no era un negativo**: el archivo vive a profundidad 3 (`Descargas MX/Descargas Manuales/116334-V1.zip`) y el comando nunca llegó a mirarlo. El positivo se obtuvo con la ruta completa: `ls -l` → `1404772` bytes, `sha256sum` → `776d56bf…c89d1c`, idéntico al manifiesto.

---

## §COMMIT-1 · Especificación congelada — escrita ANTES de abrir un solo valor del microdato

**Ceguera de este commit, declarada.** Al redactar §COMMIT-1 se abrió el zip y se leyeron: (i) el **listado** de sus 98 archivos; (ii) los **nombres y etiquetas** de las 124 variables de `Compartamos_AEJ/Main/data/analysis_data_AEJ_pub.dta`, obtenidos con `pandas.io.stata.StataReader(...).variable_labels()` — metadatos del encabezado del `.dta`, **sin materializar una sola fila**; (iii) el texto de los `.do`/`.ado` del paquete. **Ningún valor de ninguna celda se abrió antes de este commit.** El encargo lo permite en esos términos: *«permitido leer nombres y etiquetas; prohibido mirar un valor antes de este commit»*.

### 1 · Universo

Ola de **seguimiento** (`Endline`), la que el propio paquete usa: `Compartamos_AEJ/Main/Compartamos-AEJ-tables-2-8.do:3`, verbatim → `use if survey == "Endline" using data/analysis_data_AEJ_pub, clear`. **N = 16,560** declarado, unidad de análisis **la persona** (mujer, 18-60 años), tal como lo fija la spec §2. La línea base (`BTreatment`, N=6,778) **no entra**: la spec §2 la admite solo como universo secundario con justificación propia, y el encargo la prohíbe salvo declaración explícita — **este acto no la declara y no la usa**.

### 2 · Tratamiento

`Treatment` (variable `:2`, etiqueta `Treatment`), constante dentro de cada conglomerado. **No** `BTreatment` (`:19`, `Treatment Assignment`, línea base).

### 3 · Estimador — copia exacta del procedimiento del paquete

Para cada desenlace `Y` de la lista cerrada de §4:

```
regress Y Treatment i.supercluster_xi , vce(cl cluster)
```

exactamente la forma de `Compartamos-AEJ-tables-2-8.do` para estos desenlaces (`:11` `in_admin`, `:13` `Q21_3_comp`, `:18` `A_ever_late_not_cond`, `:76` `Q9_4_soldloan_none`), con `xi i.supercluster_xi` / `unab sc_controls : _Isuper*` de `:5-6`. Los efectos fijos de supercluster son controles del propio paquete (`supercluster_xi`, `:16`, etiqueta `Supercluster - used for fixed effects`), no una adición de este acto.

**Ninguno de los cuatro desenlaces lleva controles de línea base.** El paquete añade `BaselineValue BaselineValueMDum InPanel` solo *«if the dependent variable has a baseline equivalent»* (`Source/Analysis/Set-specification-properties.do:65`); ninguno de los cuatro tiene par `BE_*` en el archivo, y las cuatro líneas citadas del `.do` los omiten. Copiar eso es copiar el paquete, no simplificarlo.

**Sin ponderador.** `command grep -rnE "\[(pw|aw|fw|iw)" --include="*.do"` sobre los **14** archivos `.do` del paquete → **cero** coincidencias (negativo con su conteo de archivos examinados, A.13). El paquete no pondera; este acto tampoco.

**Equivalente exacto en este stack.** No hay Stata ni `statsmodels` en esta caja (`pandas 2.3.3`, `numpy 2.3.5`, `scipy 1.16.3`). Se implementa MCO con VCE agrupado replicando **la aritmética de Stata `regress … , vce(cl cluster)`**, no una aproximación:

- `V = (G/(G−1)) · ((N−1)/(N−k)) · (X'X)⁻¹ · [ Σ_g (X_g'u_g)(X_g'u_g)' ] · (X'X)⁻¹`, con `G` = conglomerados efectivos, `N` = observaciones efectivas, `k` = parámetros estimados (constante incluida);
- inferencia con **t de `G−1` grados de libertad**, no normal — es lo que Stata usa y lo que fija el ancho del IC95%;
- `i.supercluster_xi` como indicadoras con la primera categoría omitida, más constante; colinealidades exactas se eliminan por rango y `k` se cuenta sobre el rango efectivo, igual que Stata.

**Control positivo obligatorio de la implementación** (memoria de programa: contra una cifra de referencia se exige coincidencia exacta, la pertenencia a un IC no es reproducción). Antes de reportar un solo ITT, la rutina corre **dos** comprobaciones con valor esperado conocido y **PARA si alguna falla**: (i) con cada observación en su propio conglomerado (`G = N`), la matriz `V` debe reducirse **numéricamente** a HC1 calculada por separado; (ii) sobre datos sintéticos con coeficiente verdadero conocido y agrupamiento impuesto, `β̂` debe recuperar la solución MCO por normal-ecuaciones al orden de la precisión de máquina. Ambas se reportan en §COMMIT-2 con su resultado.

### 4 · Desenlaces — lista cerrada, derivada SOLO de nombres y etiquetas

Derivada del `variable_labels()` de las 124 variables y de los `.do`. **Cerrada aquí; no se amplía en §COMMIT-2.**

| # | variable | etiqueta verbatim del codebook | papel | dirección que el mecanismo postula |
|---|---|---|---|---|
| 1 | `in_admin` | `Any loan from Compartamos - admin data` | **adopción** (registro administrativo del banco) | ITT **> 0** |
| 2 | `Q21_3_comp` | `Any loan from Compartamos - survey data` | **adopción** (autorreporte) | ITT **> 0** |
| 3 | `A_ever_late_not_cond` | `Client was ever late on payments` | **daño downstream — mora/atraso**, primario | ITT **> 0** |
| 4 | `Q9_4_soldloan_none` | `Did not sell an asset to help pay for a loan` | **daño downstream — cobranza/apremio**, secundario | ITT **< 0** |

**Existe variable de daño por nombre — el candidato `inejecutable` de la spec §4 no se dispara por esta vía.** `A_ever_late_not_cond` (`:66`) es literalmente mora/atraso, y es **administrativa**, no autorreportada: las notas del propio paquete (`Source/Analysis/Set-category-properties.do`, bloque `CatCreditChimera`, `outcome_notes1`) dicen verbatim que *«The dependent variables in Columns 2 and 10 are from administrative data and refer to all the respondent's loans from Compartamos from April 2009 to February 2012»* — la columna 2 es `in_admin` y la 10 es `A_ever_late_not_cond`, en ese orden dentro de `loc g1`. El sufijo `_not_cond` significa **no condicionada a haber tomado crédito**: es la tasa sobre todo el universo, que es exactamente lo que un ITT necesita.

`Q9_4_soldloan_none` (`:21`) entra como **secundario y así etiquetado**: vender un activo para pagar un préstamo es la cara del hogar del apremio de cobranza, no un registro de mora. Está **invertida por construcción** (`1` = *no* vendió), de modo que daño mayor ⇒ valor menor ⇒ ITT negativo. La adjudicación de §4 de la spec se ancla en el **primario**; el secundario entra como corroboración o como reserva escrita, nunca como el desenlace que decide la fila por sí solo.

**Barrido de la lista completa, para que la ausencia sea un negativo con universo.** Se leyeron las **124** etiquetas, una por una. Ninguna otra nombra mora, atraso, incumplimiento, cobranza, castigo ni recuperación: los `Q21_3_*`/`Q21_5_*` son tenencia y monto de crédito por fuente, y el resto son negocio, ingreso, consumo, activos, escolaridad, decisión intrahogar, confianza, bienestar subjetivo y controles de línea base `BE_*`. Las cuatro de la tabla son la lista cerrada.

### 5 · Escala del veredicto

**Puntos porcentuales (pp) de la variable de desenlace, ITT por conglomerado** — la escala que la spec §3 fijó antes del dato, por `A-bis` regla 3. Los cuatro desenlaces son indicadores `0/1` por nombre y etiqueta (`Any loan…`, `…was ever late…`, `Did not sell…`; el paquete declara `Q9_4_soldloan_none` binaria en `Source/Analysis/Quantile/Quantile-outcome-group.do:59`), de modo que `ITT × 100` está en pp directamente.

**Contingencia declarada por adelantado, para no necesitar un segundo intento de especificación:** si la verificación de §COMMIT-2 encuentra que alguno de los cuatro **no** toma solo valores en `{0,1}` sobre el universo efectivo, ese desenlace se reporta en su unidad nativa, se dice con esas palabras, y **queda fuera de la adjudicación en pp** — no se re-especifica nada.

**Esta escala jamás se compara contra el «techo de mora regulada 15-20%» de `dinero.credito.scoring_alternativo` (`canon/modelo-decision-v4_0.md:500`)** — otro objeto, otro mecanismo, otra escala, y este acto no declara ningún enlace entre las dos (`A-bis` 3, spec §3 y §5).

### 6 · Adjudicación — la escala §4 de la spec y su precedencia sellada

Se aplica la tabla de `spec-bbis-exp-compartamos-v1_0-propuesta` §4 tal como está, con su precedencia **`rompe → inejecutable → acota → corrobora → no-refuta`**. Reglas de disciplina que este commit fija antes de ver el dato:

- Ninguna fila se fuerza **por cercanía**. Un IC95% que no despeja el umbral en **ninguna** dirección es `no-refuta`, con la reserva `A-bis` escrita — nunca `rompe` y nunca `corrobora`.
- El mecanismo que se somete a prueba es el de tres condiciones de `dinero.credito.baja_friccion_usura_dano_downstream`: *baja fricción + tasa usuraria + reporte incompleto → daño downstream*. Este microdato puede medir **la primera** (adopción, desenlaces 1-2) y **la tercera vía su consecuencia** (mora/apremio, desenlaces 3-4); **no mide la tasa ni la calidad del reporte al buró**. Ese hueco de medición se declara aquí, antes del resultado, y viaja con el veredicto sea cual sea.
- `rompe` exige que el IC95% del desenlace de **daño primario** cruce cero o vaya en dirección contraria **bajo potencia suficiente**. La potencia se juzga con `N` y `G` efectivos reportados en §COMMIT-2, no supuesta.

### 7 · Reservas nombradas, con las cifras del censo (`ADR-162`), no re-derivadas aquí

- **`in_admin` = 12.37%** (2,048/16,560) de toma de tratamiento por registro administrativo, sin desglose por brazo en el censo. Este acto **no** la usa como instrumento ni como covariable: TOT/LATE está prohibido y no se estima.
- **Atrición = 37.43%** (1,090/2,912) sobre el universo buscado para seguimiento. Este acto **no corrige** por atrición diferencial: la deja como **reserva escrita, sin corregir**, porque corregirla sería una especificación distinta de la que el paquete corre y de la que esta spec congela.
- **Sin identificador de persona ni de hogar** en el archivo público: todo el ejercicio es transversal por conglomerado, nunca intra-persona. La vía de panel está cerrada por el propio archivo.
- **Un solo experimento, un solo estado (Nogales, Sonora), un solo producto** (crédito grupal de Compartamos Banco). No se declara vía de transporte a otra geografía ni a otro producto de `dinero.credito.*`.

### 8 · Cierre del commit

**el primer resultado que produzca este procedimiento es el que se reporta**

---

## §COMMIT-2 · Resultados — el primer resultado que produjo el procedimiento, y la adjudicación

**Este commit no edita una sola línea de §COMMIT-1.** Verificable: `git diff <commit-1> <commit-2> -- forense/resultado-exp-compartamos-v1_0.md` es puro `+` por debajo de la línea de cierre de §COMMIT-1.

### 1 · Controles positivos de la implementación — corridos ANTES de reportar un solo ITT

Los dos que §COMMIT-1 §3 exigió, más dos que no exigía y que valen más porque su valor esperado es **externo a este acto**:

| # | qué comprueba | valor esperado | resultado | veredicto |
|---|---|---|---|---|
| 1 | con `G = N`, la VCE agrupada debe reducirse a HC1 calculada por separado | `max\|V_cl − V_HC1\| = 0` | `3.036e-18` | **PASA** |
| 2 | `β̂` resuelve las normal-ecuaciones | `max\|b − (X'X)⁻¹X'y\| = 0` | `8.882e-16` | **PASA** |
| 3 | `in_admin` sobre la ola de seguimiento | **2,048 / 16,560 = 12.37%** — cifra del censo `ADR-162`, derivada por otro acto, en otra caja, con otro código | `2048/16560 = 12.37%` | **PASA — coincidencia exacta** |
| 4 | atrición sobre `!mi(attrited)` | **1,090 / 2,912 = 37.43%** — misma procedencia | `1090/2912 = 37.43%` | **PASA — coincidencia exacta** |

Los controles 3 y 4 son de **valor esperado**, no de pertenencia a un intervalo: la pregunta era si el conteo cae en el número publicado por el censo previo, y cae en el número exacto, no cerca de él.

**Lo que NO se pudo controlar, dicho como es.** No hay control contra las cifras **publicadas** del artículo. El paquete no las trae: `Main/results/Tables/{Unformatted,Formatted}/` y `Main/results/Datasets/` contienen solo `empty.txt`, y `Format-Compartamos-tables.xlsm` es un libro de macros de formato — sus 34 cadenas son rótulos de parámetros y rutas, ningún valor de tabla (inspeccionado con `zipfile`+`sharedStrings.xml`). Traer las cifras publicadas exigiría descargar el artículo, que el encargo **prohíbe**. Se declara el hueco; no se rellena por memoria.

### 2 · Universo efectivo — verificado, no supuesto

| cantidad | valor derivado | fuente del contraste |
|---|---|---|
| filas del `.dta` | 21,523 | censo `ADR-162`: 21,523 ✓ |
| filas con `survey == "Endline"` | **16,560** | §COMMIT-1 §1 declaró 16,560 ✓ |
| conglomerados (`cluster`) en seguimiento | **238** | censo: 238 ✓ |
| conglomerados por brazo | **120 tratados / 118 control** | censo: 120/118 ✓ |
| `Treatment` constante dentro del conglomerado | **238 de 238** | censo lo afirmaba; aquí se comprueba ✓ |
| personas por brazo | 8,262 tratadas / 8,298 control | derivado en este acto |
| superclusters (efectos fijos) | 45 | derivado en este acto |

**Binariedad — la contingencia de §COMMIT-1 §5 no se activó.** Los cuatro desenlaces toman exactamente dos valores, `{0, 1}`, sobre el universo efectivo. Faltantes: `in_admin` 0 · `Q21_3_comp` 715 · `A_ever_late_not_cond` 0 · `Q9_4_soldloan_none` 99. Los faltantes se pierden por listwise, igual que en Stata, y bajan el `N` de la corrida, no el universo. La escala en **pp** queda como se fijó.

### 3 · ITT por desenlace — `regress Y Treatment i.supercluster_xi, vce(cl cluster)`

Todos en **pp**, IC95% con **t de 237 gl** (`G − 1`), `k = 46` en las cuatro corridas.

| desenlace | papel | N | G | media control (pp) | **ITT (pp)** | EE (pp) | IC95% (pp) | dirección postulada | ¿la cumple? |
|---|---|---|---|---|---|---|---|---|---|
| `in_admin` | adopción (admin) | 16,560 | 238 | 5.845 | **+11.4735** | 0.8991 | **[+9.7022, +13.2448]** | `> 0` | **sí**, IC excluye cero |
| `Q21_3_comp` | adopción (autorreporte) | 15,845 | 238 | 3.888 | **+8.2199** | 0.7819 | **[+6.6794, +9.7603]** | `> 0` | **sí**, IC excluye cero |
| `A_ever_late_not_cond` | **daño primario — mora** | 16,560 | 238 | 0.337 | **+1.1009** | 0.2328 | **[+0.6423, +1.5595]** | `> 0` | **sí**, IC excluye cero |
| `Q9_4_soldloan_none` | daño secundario (invertida) | 16,461 | 238 | 95.061 | **+0.9908** | 0.3833 | **[+0.2357, +1.7460]** | `< 0` | **NO — signo contrario, y el IC excluye cero** |

**Niveles de mora, misma variable y misma escala** (no es comparación entre escalas): control **28 de 8,298 = 0.337 pp**; tratados **116 de 8,262 = 1.404 pp**.

**Lectura literal, antes de adjudicar.** La primera condición del mecanismo —que la baja fricción de acceso efectivamente ocurre— se cumple con holgura: la adopción por registro administrativo sube 11.47 pp sobre una base de 5.85 pp. Y sobre esa expansión, la **mora administrativa sube 1.10 pp sobre una base de 0.34 pp**, con IC95% que excluye cero en la dirección que el mecanismo postula. El desenlace secundario va al revés: los hogares tratados venden un activo para pagar un préstamo **menos** a menudo, no más.

### 4 · Adjudicación — escala §4 de la spec, recorrida en su precedencia sellada

Precedencia: **`rompe → inejecutable → acota → corrobora → no-refuta`**. Se recorre entera, en orden, y cada fila se descarta con su razón antes de pasar a la siguiente.

**`rompe` — NO dispara.** Condición: *«El IC95% del ITT del desenlace de daño downstream cruza cero o va en dirección contraria a la que el mecanismo postula, bajo un universo con potencia suficiente»*. El desenlace de daño **primario**, `A_ever_late_not_cond`, ni cruza cero ni va en dirección contraria: va en la dirección postulada, con IC95% `[+0.64, +1.56]` que excluye cero.
El **secundario**, `Q9_4_soldloan_none`, sí satisface literalmente la condición. **No dispara la fila igualmente**, y la razón está escrita en §COMMIT-1 §4, **antes de ver el dato**: *«La adjudicación de §4 de la spec se ancla en el primario; el secundario entra como corroboración o como reserva escrita, nunca como el desenlace que decide la fila por sí solo.»* Esa regla se redactó a ciegas y aquí se obedece a ciegas. **Aquí entra, entonces, como reserva escrita — y es la reserva más pesada de este ejercicio (§5).**

**`inejecutable` — NO dispara.** Condición: *«El microdato no trae ninguna variable de daño downstream identificable (mora, cobranza)»*. Sí la trae: `A_ever_late_not_cond`, `Client was ever late on payments`, administrativa y no condicionada a haber tomado crédito. La llave **sí se ejerce**; no queda `SELLADA_NO_EJERCIDA`.

**`acota` — NO dispara, y la razón por la que no dispara es un hallazgo de este acto.** La fila tiene dos ramas:
- *Rama 2* — *«el desenlace disponible en el microdato solo cubre adopción y no daño downstream»*: **falsa aquí**. Se cubren las dos cosas.
- *Rama 1* — *«El ITT es significativo pero de magnitud menor a la que el `[MEDIA]` vigente asumiría»*: **no es evaluable, porque el `[MEDIA]` vigente no asume ninguna magnitud.** La regla, verbatim de `canon/modelo-decision-v4_0.md:501`: *«**SI** el producto de crédito combina **baja fricción de acceso** **Y** tasa usuraria (CAT >100%) **Y** reporte crediticio incompleto o invisible (BNPL) **ENTONCES** la adopción produce **daño downstream** — concentración de mora en productos no garantizados, quejas de cobranza […] `[MEDIA]` **(a)**»*. No hay cifra, ni umbral, ni banda: **no existe el número contra el cual esta rama compararía**. Dispararla exigiría inventar la magnitud que el `[MEDIA]` "asumiría", que es precisamente forzar una fila por cercanía — prohibido por la spec §4 y por §COMMIT-1 §6.
  ⚠️ **Y no se rellena el hueco con la única cifra a la mano.** El «techo de mora regulada 15-20%» y el umbral de IMOR «~25-30% sostenido» viven en `dinero.credito.scoring_alternativo` (`:500`), **otro objeto y otra escala**; `A-bis` regla 3, la spec §3 y §5 y el encargo lo prohíben expresamente, y este acto **no declara ningún enlace de escala** entre las dos reglas. La mora medida aquí (0.34 pp → 1.40 pp) **no se compara** con esos números, ni para adjudicar ni para calificar.

**`corrobora` — DISPARA.** Condición: *«El ITT del desenlace de adopción/daño downstream identificado va en la misma dirección que el mecanismo […] con IC95% que excluye cero en esa dirección»*. Se cumple en **tres de los cuatro** desenlaces, incluido el **de daño primario**: adopción administrativa `+11.47` pp, adopción autorreportada `+8.22` pp y mora administrativa `+1.10` pp, los tres con IC95% que excluye cero por el lado postulado.

**`no-refuta` — no se alcanza**, por definición: solo aplica si ninguna de las otras cuatro dispara, y `corrobora` disparó.

> ### VEREDICTO: **`corrobora`** → estado de la llave **`EJERCIDA_CORROBORA`**
> **En la escala declarada:** ITT de **+1.10 pp** (IC95% `[+0.64, +1.56]`, `N=16,560`, `G=238`, t de 237 gl) sobre `A_ever_late_not_cond` — *client was ever late on payments*, registro administrativo de Compartamos —, producido por una expansión aleatorizada de colocación que subió la adopción administrativa en **+11.47 pp** (IC95% `[+9.70, +13.24]`) sobre una base de 5.85 pp.

### 5 · Reservas que viajan con el veredicto — sin ellas el veredicto está mal citado

1. **El desenlace de daño secundario contradice al primario, con IC95% que excluye cero.** `Q9_4_soldloan_none` = `+0.99` pp, IC95% `[+0.24, +1.75]`: los hogares tratados venden un activo para pagar un préstamo **menos** a menudo. Bajo el mecanismo esto debía ir al revés. Lectura alternativa que este acto **nombra pero no adjudica** (no está en la escala sellada): el crédito puede **sustituir** la venta de activos como forma de cubrir un pago, de modo que el mismo dato admite una lectura de daño y una de alivio. Que la regla se archive `corrobora` y no `rompe` **depende enteramente** de la regla de anclaje en el primario que §COMMIT-1 fijó a ciegas.
2. **El daño primario descansa sobre 144 eventos.** 28 en control y 116 en tratamiento, sobre 16,560 personas. El ITT es un modelo lineal de probabilidad sobre una tasa base de 0.34%; el IC95% agrupado es el que es, pero la corroboración se sostiene sobre pocos eventos y así debe citarse.
3. **Dos de las tres condiciones del mecanismo NO se miden.** La regla es explícitamente condicional a la **estructura**: baja fricción **Y** CAT >100% **Y** reporte crediticio incompleto. Este microdato identifica la **primera** y mide la consecuencia de daño; **no mide la tasa ni la calidad del reporte al buró**. La propia regla advierte, verbatim, que *«la lectura peligrosa es la inversa: leerla como "la baja fricción daña" culpa al diseño accesible y borra las dos condiciones estructurales que la activan»*. **Este ejercicio corrobora la dirección sin poder verificar las dos condiciones estructurales** — que es exactamente la forma que tiene la lectura peligrosa. La corroboración es por eso **de dirección, no de la cláusula condicional completa**.
4. **Atrición 37.43% sin corregir**, por decisión declarada en §COMMIT-1 §7: corregirla sería otra especificación.
5. **`in_admin` 12.37%** de toma, sin desglose por brazo en el censo; no se usó como instrumento (TOT/LATE prohibido y no estimado).
6. **Transversal, un estado, un producto.** Nogales, Sonora; crédito grupal de Compartamos Banco; ola de seguimiento, sin identificador de persona. Sin vía de transporte declarada a otra geografía ni a otro producto de `dinero.credito.*`.
7. **Hallazgo lateral, declarado y no ejercido: la regla `dinero.credito.baja_friccion_usura_dano_downstream` no tiene magnitud.** Mientras el `[MEDIA](a)` siga siendo puramente cualitativo, **ninguna evidencia futura podrá acotarlo por magnitud** — la rama 1 de `acota` de esta escala, y de cualquier escala que se le parezca, es inevaluable contra él. Se declara aquí y se lleva a tablero; **este acto no le pone número a la regla** ni toca el `[MEDIA](a)`.

### 6 · Destino del número — `RANURA DE MESA` llegó **VACÍA**

`FP-160` selló la spec pero **no eligió** entre (a) competir por el `[MEDIA](a)` y (b) entrar a la octava clase de `milpa/procedencia.yaml` (§COMMIT-0). Por tanto, y siguiendo el patrón de `CAL-G3` (`EJERCIDA_ACOTA` con β `PROPUESTO`, `FP-127`):

- La llave **se ejerce igual** — el renglón del registro es el entregable, y se mueve a `EJERCIDA_CORROBORA`.
- El número queda **`PROPUESTO`**. **`milpa/procedencia.yaml` no se toca**: cero líneas de diferencia en este acto. La octava clase `EVIDENCIA_EXPERIMENTAL_TERCEROS` sigue **VACÍA**, como debe estar mientras mesa no elija.
- El `[MEDIA](a)` de `canon/modelo-decision-v4_0.md:501` **no se toca**: sustituirlo exige acto propio de mesa (spec §3).
- Se abre **una** fila nueva en `forense/firmas-pendientes.tsv` para que mesa elija destino (a)/(b), con el hallazgo de §5.7 nombrado dentro de ella.

### 7 · Especificación — no hubo tercer commit

§COMMIT-1 no resultó mal: la contingencia de binariedad no se activó, la lista cerrada de desenlaces resultó ejecutable, la variable de daño existía por nombre y el estimador reprodujo las dos cifras del censo previo al dígito. No hay nada que corregir hacia atrás, y no se corrigió nada.
