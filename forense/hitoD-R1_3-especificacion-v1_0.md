# HITO D · Falsador `R1.3` — especificación pre-registrada, congelada antes de abrir microdato
### `hitoD-R1.3-especificacion` · **v1.0** · 4 de agosto de 2026

> ⚠️ **Congelado ANTES de abrir ningún CSV de microdato de ENIF/ENDUTIH.** Este documento se cierra y se commitea antes de leer una sola fila de `conjunto_de_datos_tmodulo_enif2024.csv`, `conjunto_de_datos_tsdem_enif2024.csv` o cualquier archivo de `endutih2024_bd_dbf.zip`. Todo lo que sigue se deriva de la ficha ya sellada (`forense/hitoD-preregistro-v2_0.md`, R1.3, líneas 49-57), del cruce `forense/cruce-catalogo-fichas-v2_0.md` (filas 50-51, ya archivado, no re-derivado), y de los diccionarios de archivos (FD) de ENIF 2018/2021/2024 y ENDUTIH 2024 — documentación/estructura, no microdato. Este documento fue escrito leyendo esos FD (`data/raw/enif_2018_fd.xlsx`, `enif_2021_fd_pdf.zip:enif_2021_estructura_del_archivo.xlsx`, `enif_2024_fd.xlsx`, `endutih2024/fd_endutih2024.xlsx`) — exploración de **estructura**, no de contenido; **declaración ADR-46 al final de este documento (§8)**.

---

## 0 · Ficha bajo prueba, verbatim

> **R1.3 · Canal de confianza personal → adopción `[FUERTE]`**
> SI se ofrece un producto financiero por un canal de confianza personal ENTONCES sube la adopción; sin puente, desconfía — PORQUE G1
>
> **Falsador.** Producto con penetración masiva en el segmento popular por canal 100% digital, sin sucursal y sin recomendación estructurada.
> **Umbral.** Penetración ≥10% de adultos del segmento popular, brecha rural-urbana <10 puntos, sin programa de referidos que explique el grueso de las altas.
>
> **A** umbral cruzado → *"sin puente, desconfía"* cae; decidir si G1a sobrevive más estrecho o si G1 baja de tier · **B** penetración alta con referidos dominantes · **C** exigiría canal de alta desagregado (dato propietario) · **D** si ninguna fintech lo publica.

---

## 1 · Construibilidad de las tres condiciones del Umbral — adjudicada ANTES de abrir microdato

**No se supone: se verifica contra el cruce ya archivado y contra los FD.**

**Condición 1 (penetración ≥10%) y Condición 2 (brecha rural-urbana <10pp): CONSTRUIBLES.** Ya lo dice `forense/cruce-catalogo-fichas-v2_0.md:50` (archivado, acto previo, no re-derivado aquí): *"Penetración ≥10% segmento popular, brecha rural-urbana <10pp | ENIF, ENDUTIH | ... | Individuo | Sí, ambas condiciones en el mismo instrumento | VIABLE, a nivel de penetración/brecha"*. Este acto confirma esa viabilidad contra el FD de ENIF 2024 (§3 abajo): existe un ítem de tenencia de producto 100% digital sin sucursal (`P5_4_8`) y una variable derivada de tamaño de localidad (`TLOC`) en la misma tabla — **"el mismo instrumento" del cruce es literal: ambas condiciones viven dentro de ENIF solo, sin necesitar ENDUTIH para el cómputo** (ver §4 sobre el papel de ENDUTIH).

**Condición 3 (sin programa de referidos que explique el grueso de las altas): NO CONSTRUIBLE, confirmado contra dos fuentes archivadas independientes.** `forense/cruce-catalogo-fichas-v2_0.md:51`: *"Ninguna — dato propietario de la fintech ... NO EXISTE — verificado en las 6 clases de `inventario_fuentes_clase-fuente-mexico.md`: ninguna (Registro administrativo, Regulador — ni CNBV publica canal de alta por fintech) lo construye."* Y `forense/cruce-catalogo-fichas-v1_0.md:80`: *"Miden adopción/uso, no 'canal de alta' desagregado — dato propietario de la fintech sigue siendo el hueco real."* Este acto revisó el FD de ENIF 2024 buscando un proxy y **no encontró ninguno limpio**: existe una batería `P5_14`/`P5_15_1..7`/`P5_16` ("¿comparó su cuenta?", "¿usó recomendación de amistades?", "¿cómo la contrató?") pero se refiere explícitamente a **"su (última) cuenta"** — singular, la cuenta más reciente del respondiente, **no** desagregada por tipo de producto. Un respondiente con varias cuentas (p. ej. nómina + `P5_4_8`) no permite atribuir esa batería al producto bajo prueba sin asumir que la última cuenta contratada es la digital — asunción no verificable limpiamente y que el propio corpus ya descartó como ruta (línea citada arriba). **Se confirma la sospecha de mesa: solo 2 de 3 condiciones son construibles.**

**Conclusión de este punto, declarada antes de ver una fila:** el Umbral tal como está escrito **nunca puede evaluarse completo** con las fuentes de este acto. Lo único que este acto puede decidir es el estado de las condiciones 1 y 2. Eso fija el árbol de decisión de §2.

---

## 2 · Árbol de decisión de la escala — declarado ANTES de ver el resultado (Bloque B-bis, Nota 26/ADR-58)

Dado que la condición 3 es estructuralmente inconstruible (§1) y el Umbral es una conjunción de tres condiciones, ningún resultado de este acto puede producir honestamente la fila `A` (que exige el umbral cruzado **completo**). Dos ramas, mutuamente excluyentes, cubren el espacio de resultados de las condiciones 1 y 2:

**Rama 1 — Penetración <10% de adultos del segmento popular, O brecha rural-urbana ≥10 puntos (falla al menos una de las dos condiciones evaluables).** El falsador **corrió limpio sobre las dos condiciones que sí se pueden medir y no se satisfizo**. Por Nota 26/ADR-58 (fila `E` prospectiva): esto **no refuta** la regla — la corrobora, **acotada** a las dos condiciones medibles, con la condición 3 declarada permanentemente fuera de alcance. **Propuesta de fila: `E`**, con esta redacción: *"el falsador corrió limpio en penetración y brecha rural-urbana, y no se satisfizo — la regla sobrevive esta prueba, acotada porque la condición 3 (canal de alta desagregado) nunca pudo evaluarse."*

**Rama 2 — Penetración ≥10% Y brecha rural-urbana <10 puntos (ambas condiciones evaluables cruzan su umbral).** Aun así **no se propone `A`**: el Umbral de la ficha exige las tres condiciones conjuntamente, y la tercera permanece genuinamente desconocida, no ausente-y-descartable. Forzar `A` aquí sería tratar una condición inconstruible como satisfecha por omisión, que es precisamente el error que la fila `C` de la propia ficha ya nombra para este caso: *"C exigiría canal de alta desagregado (dato propietario)"*. **Propuesta de fila: `C`**, con esta redacción: *"penetración y brecha cruzan su umbral, pero el falsador no puede decidirse sin el canal de alta desagregado — dato propietario de la fintech, inexistente en fuentes públicas (confirmado por `cruce-catalogo-fichas-v2_0.md:51` antes de este acto)."*

**Qué sería interesante bajo corroboración (Rama 1), dicho antes de verlo — obligación de Bloque B-bis.** La ficha (línea 52) ya declara que el caso Nu (citado ahí: 15M de clientes, sin sucursales, adopción rural ≈ urbana) parece contradecir "sin puente, desconfía" a nivel de un caso. Si la Rama 1 sale (penetración baja o brecha alta a nivel del **segmento popular medido en la población general**, no solo entre los clientes ya captados de una fintech), el resultado interesante es que **Nu sería una vanguardia/outlier de mercado, no todavía representativo del grueso del segmento popular nacional** — dato distinto de "Nu tiene 15M de clientes" (una cifra de la empresa, sobre su propia base, sesgada hacia quien ya adoptó) y más cercano a lo que la ficha realmente pregunta: si el patrón **se generalizó** al segmento popular en su conjunto. Sería el primer dato poblacional (no anecdótico-de-una-fintech) sobre esta pregunta específica.

**Reserva declarada de antemano (A-bis, contraparte).** Un punto que satisface la lectura de "cruza el umbral" pero cuyo IC95% no despega claramente del umbral (10% de penetración o 10pp de brecha) no se adjudica limpio — se reporta con la reserva escrita, mismo criterio que `R5.2`/Nota 18 y `R7.2`/Nota 12 ya aplicaron.

**Precedencia (ADR-58(b), declarada explícita por B-bis).** Las dos ramas son mutuamente excluyentes por construcción (Rama 1 y Rama 2 cubren particiones disjuntas del espacio penetración×brecha), así que no debería haber colisión. Si, por algún artefacto de borde (p. ej. un IC que cruza el umbral en una dirección y no en la otra), ambas lecturas parecieran aplicar a la vez, manda la fila más específica sobre la razón exacta de la indecisión: `C` (que nombra la causa concreta — dato propietario ausente) sobre cualquier lectura genérica de `E`.

---

## 3 · Operacionalización de variables — citada literal contra el FD

### 3.1 · Ola de ENIF: **2024, sola. No se combinan las tres olas.**

Verificado contra los tres FD, antes de decidir:
- **ENIF 2018** (`enif_2018_fd.xlsx`, hoja `TModulo`): el ítem de cuenta "contratada por internet o aplicación" **no existe** — la batería de tipos de cuenta de 2018 no tiene esa categoría. El producto bajo prueba no era nombrable en 2018.
- **ENIF 2021** (`enif_2021_fd_pdf.zip:enif_2021_estructura_del_archivo.xlsx`, hoja `TModulo`, campo `P5_4_8`): *"5.4 ¿Usted tiene cuenta contratada por Internet o aplicación como Mercado Pago o Albo?"* — existe, pero nombra **Mercado Pago o Albo**, sin Nu (Nu México todavía no tenía escala relevante en el mercado de cuentas en el periodo de referencia de esa ola).
- **ENIF 2024** (`enif_2024_fd.xlsx`, hoja `TMODULO`, campo `P5_4_8`, líneas 429-431 del volcado): *"5.4 ¿Usted tiene cuenta contratada por internet o aplicación (no bancaria) como Mercado Pago, Nu o Spin de Oxxo?"* — **es la única ola que nombra Nu explícitamente**, el caso que la propia ficha cita como posible falsación (línea 52).

**Decisión:** se usa **solo ENIF 2024**. Razones: (a) el ítem no existe en 2018 — no hay serie que combinar; (b) el ítem de 2021 mide una canasta de productos distinta (sin Nu, mercado inmaduro) — combinarlo con 2024 mezclaría dos operacionalizaciones no comparables del mismo código de campo, violación de A-bis 3 (escala/definición distinta, aunque el nemónico `P5_4_8` sea el mismo); (c) 2024 es la ola donde el producto que motiva la ficha (Nu) es nombrable y donde la penetración fintech tiene más probabilidad de acercarse al umbral de 10% — es la prueba más favorable a encontrar el falsador satisfecho, no la más conveniente para confirmar la regla.

### 3.2 · Producto "canal 100% digital, sin sucursal, sin recomendación estructurada"

**Variable:** `P5_4_8` de `TMODULO` (tabla `conjunto_de_datos_tmodulo_enif2024.csv` dentro de `enif2024_csv.zip`). Wording literal del FD: *"5.4 ¿Usted tiene cuenta contratada por internet o aplicación (no bancaria) como Mercado Pago, Nu o Spin de Oxxo?"* Códigos: `1` = Sí, `2` = No. Sin código de blanco — se pregunta a todo el universo de la tabla (confirmado: la batería `P5_4_1`...`P5_4_9` no tiene ningún `FILTRO` que la condicione; los primeros `FILTRO` de la sección 5 aparecen después, en la línea 478 del volcado, downstream de esta batería).

**Adopción (`y`):** `y=1` si `P5_4_8=1`, `y=0` si `P5_4_8=2`.

### 3.3 · Segmento popular

**No existe variable de ingreso ni de nivel socioeconómico en ENIF** — verificado contra las tres tablas relevantes del FD 2024 (`TSDEM`, `THOGAR`, `TVIVIENDA`): `TSDEM` trae `SEXO`/`EDAD`/`NIV`(escolaridad)/`GRA`; `THOGAR` trae solo número de personas con trabajo remunerado; `TVIVIENDA` trae cuartos, baños, auto e internet del hogar, sin escala socioeconómica derivada. Ninguna de las tres nombra ingreso, decil, NSE ni estrato AMAI.

**Proxy declarado: escolaridad.** `NIV` de `TSDEM` (wording literal: *"2.6 ¿Hasta qué año o grado aprobó (NOMBRE) en la escuela?"*), aplicada **a la propia persona seleccionada del módulo** (join `TMODULO.LLAVEMOD = TSDEM.LLAVESDE`, ambas llaves del mismo formato de 10 caracteres). **Segmento popular = `NIV` ∈ {00 Ninguno, 01 Preescolar o kínder, 02 Primaria, 03 Secundaria}** — es decir, sin estudios más allá de la secundaria. Se excluyen `NIV` 99 (No sabe) y blancos.

**Límite declarado, no maquillado:** esto es un proxy de escolaridad, no de ingreso ni de NSE. Es la única variable disponible en el propio instrumento para aproximar "segmento popular" sin salir de ENIF; una definición por ingreso o AMAI no es construible con este instrumento. Se reporta como tal en el commit 2 — no se compara contra ninguna cifra de "segmento popular" definida por otra escala (A-bis 3/4).

### 3.4 · Eje rural-urbano

**Variable:** `TLOC` ("Tamaño de localidad"), variable derivada presente tanto en `TSDEM` como en `TVIVIENDA` (mismo campo, misma fuente censal, consistente entre tablas). Códigos: `1` = 100,000 y más habitantes, `2` = 15,000 a 99,999, `3` = 2,500 a 14,999, `4` = menor de 2,500.

**Dicotomización — el corte oficial mexicano, no uno arbitrario:** **Rural = `TLOC` 4** (localidades menores de 2,500 habitantes — el umbral rural/urbano estándar de INEGI/CONAPO). **Urbano = `TLOC` 1, 2, 3** (2,500 habitantes o más). Se elige este corte, y no un corte "extremos contra extremos" (`TLOC`=1 vs `TLOC`=4 solamente), porque el corte oficial es el que hace la brecha comparable con cualquier cifra publicada que use la misma definición, y porque descartar las localidades intermedias (`TLOC` 2 y 3) reduciría artificialmente el denominador del segmento popular sin motivo declarado en la ficha.

### 3.5 · Universo, ponderador y diseño

- **Universo:** personas de la tabla `TMODULO` (población 18+, personas seleccionadas del módulo — universo estándar de ENIF) con `NIV` ∈ {00,01,02,03} (segmento popular, §3.3).
- **Ponderador:** `FAC_PER` ("Factor de expansión a nivel persona"), declarado en `TMODULO` (línea 1483 del volcado) — no `FAC_HOG` (ese es el factor a nivel hogar, de `TVIVIENDA`/`THOGAR`; para un desenlace medido a nivel de la persona seleccionada corresponde el factor de persona).
- **Diseño:** `EST_DIS`/`UPM_DIS`, declarados en `TMODULO` — mismos campos que `svystat.py: prop_ultimate_cluster` espera como `(estrato, upm, peso, y)`.
- **Llave de unión** `TMODULO`↔`TSDEM`: `LLAVEMOD` (en `TMODULO`) = `LLAVESDE` (en `TSDEM`) — ambas de 10 caracteres, mismo formato de llave de identificación de persona, documentado en ambos FD como "Llave de identificación de la persona elegida"/"Llave de identificación de la tabla sociodemográfica".

### 3.6 · Cómputo del Umbral

- **Penetración:** `prop_ultimate_cluster` sobre `(EST_DIS, UPM_DIS, FAC_PER, y)` restringido al universo de §3.5 completo (segmento popular, ambas zonas). Umbral: `p_hat ≥ 0.10`.
- **Brecha rural-urbana:** dos corridas separadas de `prop_ultimate_cluster`, una para el subconjunto rural (`TLOC=4`) y otra para el urbano (`TLOC` 1-3), ambas dentro del segmento popular. `brecha = |p_urbano - p_rural|` en puntos porcentuales. `SE_brecha = sqrt(se_urbano² + se_rural²)` — válido bajo independencia entre las dos submuestras, que se cumple aquí porque rural y urbano son estratos de diseño disjuntos por construcción (ninguna UPM pertenece a ambas). `IC95_brecha = brecha ± 1.96·SE_brecha`. Umbral: `brecha < 10` puntos porcentuales.

### 3.7 · Papel de ENDUTIH 2024 — declarado, no supuesto

**ENDUTIH NO aporta ninguna variable al cómputo del Umbral.** Razón estructural, no de pereza: ENIF y ENDUTIH son **muestras independientes** de INEGI (diseños muestrales propios, sin llave de persona ni de vivienda compartida entre los dos instrumentos) — no existe forma de unir un registro de ENIF con un registro de ENDUTIH a nivel de unidad. El cruce ya archivado (`cruce-catalogo-fichas-v2_0.md:50`) ya lo anticipa al decir que ambas condiciones construibles viven **"en el mismo instrumento"** — ENIF, sola, ya trae `P5_4_8` y `TLOC` en la misma tabla. Verificado contra el FD de ENDUTIH (`fd_endutih2024.xlsx`, hojas `tic_2024_hogares`/`tic_2024_residentes`/`tic_2024_usuarios`/`tic_2024_usuarios2`): ENDUTIH sí tiene un eje rural-urbano propio (`DOMINIO` R/U) y un `ESTRATO` socioeconómico de 4 niveles (Bajo/Medio bajo/Medio alto/Alto) — más rico que el proxy de escolaridad de §3.3 — pero **ninguna variable de ENDUTIH sobre productos financieros fintech nombra Nu, Mercado Pago o Spin de Oxxo**: lo más cercano es "Banca Móvil (BBVA, Citibanamex, Santander, etcétera)" (`P8_13_7`/`P8_16_7`), que mide banca móvil de **bancos tradicionales con sucursal**, justo lo contrario del producto que el falsador exige (sin sucursal). ENDUTIH no puede sustituir ni mejorar la operacionalización de §3.2.

**Por esto, el DBF de microdato de ENDUTIH (`endutih2024_bd_dbf.zip`) NO se abre en este acto.** Solo se exploró su FD (estructura). Abrir el microdato sin una razón de cómputo sería gastar contaminación (ADR-46) sin producir nada — el mismo criterio de economía que gobierna el resto del corpus.

---

## 4 · Validación del estimador — límite declarado

`tests/svystat.py: prop_ultimate_cluster` no se modifica; ya está respaldado contra tres casos de referencia (E-3, PR #97). No se re-verifica aquí.

**No existe ancla académica publicada para el estimando exacto de esta ficha** (penetración de cuentas fintech 100%-digitales, en el segmento de baja escolaridad, por localidad rural/urbana) — barrido contra `canon/integrador-psicologia-mexicano.md`, `canon/modelo-decision-v4_0.md` y `canon/glosario-v5_6.md`: las cifras de Nu que ya circulan en el corpus (13M+, 15M, 70M+ usuarios) son **cifras de la empresa sobre su propia base de clientes** (denominador = sus propios usuarios), no una tasa de penetración poblacional con denominador de "adultos del segmento popular" — no son comparables sin enlace de escala (A-bis 3), y por eso no sirven de ancla para el `p_hat` de este acto. Se declara como límite; se reportará en el commit 2, sin forzar una comparación entre escalas distintas.

**Sustituto de validación de canalización (pipeline), no de estimando:** se reportará, en el commit 2, la penetración agregada de `P5_4_8=1` sobre el universo completo de ENIF 2024 (sin restringir a segmento popular) — si la canalización de datos (join, filtros, ponderador) está bien construida, esa cifra agregada debe ser del orden de magnitud razonable frente a las cifras de adopción fintech generales ya citadas en `canon/integrador-psicologia-mexicano.md:214` (paradoja fintech, Nu >13M) aun sin ser un ancla formal — mismo espíritu que la validación de canalización que `hitoD-R3.1-especificacion` usó contra el techo de `hitoD-R3.2`.

---

## 5 · Qué NO hace este acto

No descarga nada (payloads ya en `data/raw`, 11 hashes verificados contra `data/manifiesto.yaml` antes de este documento — ver reporte de arranque). No modifica `tests/svystat.py`, `data/manifiesto.yaml`, `canon/`, ni sella ningún ADR. No escribe en `## Registro de veredictos archivados` de `hitoD-preregistro-v2_0.md` — el resultado del commit 2 es una **propuesta de fila**, con su razón, para que mesa adjudique. No abre el DBF de ENDUTIH (§3.7).

---

## 6 · Declaración ADR-46

Al abrir `conjunto_de_datos_tmodulo_enif2024.csv` y `conjunto_de_datos_tsdem_enif2024.csv` (dentro de `enif2024_csv.zip`) en el próximo commit, esta sesión queda inhabilitada para pre-registrar ninguna otra ficha contra ENIF. La exploración de este documento sobre los FD de ENIF 2018/2021/2024 y ENDUTIH 2024 (estructura, no contenido) ya es, por sí misma, contaminación **parcial** declarada aquí para las cuatro fuentes — ADR-46 distingue exploración de estructura (parcial, declarada) de apertura de contenido (total): este documento hizo lo primero para las cuatro; el próximo commit hace lo segundo solo para ENIF 2024. ENDUTIH 2024 queda con contaminación de estructura únicamente — su microdato (DBF) no se abre (§3.7).

---

**el primer resultado que produzca este procedimiento es el que se reporta.**
