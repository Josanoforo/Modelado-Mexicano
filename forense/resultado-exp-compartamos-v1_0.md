# `EXP-COMPARTAMOS-1` — ejercicio de la llave: resultado

### `resultado-exp-compartamos-v1_0` · **v1.0** · 26 de agosto de 2026 · ENTORNO UBUNTU · `ACTO E3 · EJERCE-LLAVE-COMPARTAMOS`

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
