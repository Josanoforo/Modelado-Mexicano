# `ACTO MAESTRA35-L6 · FUENTE-COERCITIVO-Y-PUENTE` — P0 · censo A.4

**2 de septiembre de 2026** · encargo de dirección (Fable), archivado por A.3 en
`forense/encargos/2026-09-02-MAESTRA35-L6-FUENTE-COERCITIVO-Y-PUENTE.md`
(SHA de redacción `792b7ef`) · `COMPUERTA: ninguna` (declaración explícita del
encargo; no dispara verificación) · entorno **UBUNTU** con corpus montado y red.

Este archivo es el **censo**, y se escribe **antes** de medir nada. Los
denominadores de abajo se contaron **sin cruzarlos jamás contra el desenlace**.

---

## 0 · ARRANQUE (A.2) y verificación de premisas contra el árbol

**Las cinco líneas del ARRANQUE.**

1. **REPO.** `/home/pc0/mm-l6-fuente-coercitivo`, worktree propio creado sobre
   `origin/main` fresco. `git log -1` = `4d7bd1e Merge pull request #474 from
   Josanoforo/claude/maestra35-n2-launch-jip2j0`. `git status` limpio al
   arrancar.
2. **SHA.** El encargo declara `792b7ef` (merge `PR #470`). Verificado que es
   ancestro real. **`main` se movió**: `792b7ef..4d7bd1e`, cuatro merges
   (`PR #471`, `#472`, `#473`, `#474`). **No es PARO**: perímetro y contadores
   re-derivados contra `4d7bd1e`; la diferencia se reporta aquí antes de editar.
3. **`data/raw`.** Ausente en el worktree nuevo — es lo esperado, está
   gitignorada (`.gitignore:5-6`). **La enlacé** a `/home/pc0/mm-corpus/raw`.
4. **ENTORNO — tres partes (A.2).**
   - `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → **sin variable**
   - `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → **`200`**
     y `…https://www.banxico.org.mx/` → **`200`** (exit 0 en las dos)
   - `ls data/raw/ | head -1` → **`2005trim1_csv.zip`**; `ls data/raw/ | wc -l` → **370**
5. **ESPEJO.** No se usa. Toda cifra de esta nota sale de este clon, con el
   comando a la vista.

**Contadores re-derivados por el comando de la casa, no heredados del encargo.**

| contador | el encargo dice | el árbol dice | comando |
|---|---|---|---|
| ADR máximo | 292 | **296** | `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md \| grep -oE '[0-9]+' \| sort -n \| tail -1` |
| FP máximo | 244 | **248** | `cut -f1 forense/firmas-pendientes.tsv \| grep -oE '^FP-[0-9]+' \| grep -oE '[0-9]+' \| sort -n \| tail -1` |
| líneas de `data/manifiesto.yaml` | 20 331 | **20 529** | `wc -l data/manifiesto.yaml` |

Candidatos de este acto: **`ADR-298`**, **`FP-249`**. `0` PR abiertos al
arrancar (`gh pr list --state open` → `[]`), así que el riesgo de colisión es
bajo — se declara igual: **renumera quien fusiona segundo**.
`FP-249`/`FP-250` aparecen en el árbol **solo** como pre-asignaciones que
`MAESTRA35-L3` renumeró y no usó; la fuente canónica (`forense/firmas-pendientes.tsv`,
239 filas) llega a `FP-248`.

### 0.1 · Tres premisas del encargo que el árbol corrige

Se declaran porque el encargo era, en lo demás, exacto: su verificación de
existencia (A.8) acertó en las seis entradas de manifiesto de ENDUTIH/CoDi, en
los dos ceros de `cngf`/`sat.gob`, en el hueco de `texto_reactivo` de
`inventario-reactivos-v1_2.tsv` (`FP-190`) y en la ubicación de la regla.

**(P1) «ENDUTIH 2023/2024/2025 (FD + cuestionario)» — no hay cuestionario.**
El corpus trae, para las tres olas, **solo `FD` (`.xlsx`) y `BD` (`.dbf.zip`)**:

```
$ ls data/raw/endutih2023/  →  FD_ENDUTIH2023.xlsx  endutih2023_bd_dbf.zip
$ ls data/raw/endutih2024/  →  endutih2024_bd_dbf.zip  fd_endutih2024.xlsx
$ ls data/raw/endutih2025/  →  endutih2025_bd_dbf.zip  fd_endutih2025.xlsx
```

El censo de (a) corrió, por tanto, sobre **el FD y sobre los nombres, catálogos
y valores reales del DBF**, no sobre un cuestionario ausente. No es pérdida: el
texto del reactivo vive en el FD — es la misma declaración que
`forense/ficha-r34-condBC-v1_0.md:68(b)` ya hacía.

**(P2) «el "puente" … la condición que la regla nombra y nadie ha buscado en el
instrumento» — sí se buscó, hace ocho días, y se encontró.**
`forense/ficha-r34-condBC-v1_0.md` (25/ago/2026, `ADR-186`, `ACTO R34-BC-MECANISMO`)
censó **ENIF 2024 a nivel de reactivo** —cuestionario PDF + `enif_2024_fd.xlsx` +
cabecera de `TMODULO.csv` (398 columnas)— y su fila 1 declara, en la columna
*canal **personal***, **«sí (`P5_15_2`)»**. La misma tabla censó **ENDUTIH
2023·2024·2025** (fila 4) y declaró **«exposición fiscal: NO — cero ítems»**,
que es exactamente la mitad `riesgo_fiscal_percibido: true` de la situación de
la regla que este acto viene a censar.

Esto **no vacía el acto**: aquel censo juzgaba las condiciones `B`/`C` de `R3.4`
(conjunción riesgo-fiscal × fricción sobre el desenlace CoDi), no las dos reglas
de este encargo, y **no midió nada**. Pero cambia el punto de partida: el trabajo
de este acto no es descubrir si el puente existe, sino **decidir si el puente que
existe sirve para la regla que lo nombra**, y ese es un juicio de universo, no de
léxico. Se declara conforme a
[[feedback_encargo_premisa_se_verifica_contra_el_arbol]].

**(P3) Las dos reglas de «puente» no existen como regla del motor.**
`milpa/procedencia.yaml:120` lo dice literal: los ids
`dinero.ahorro.informal_sin_puente` / `con_puente_y_respaldo` **«no existen
literalmente en»** el modelo — el motor describe sus 49 reglas en prosa, sin id
estable —, y `milpa/procedencia.yaml:110-112` aclara que las dos entradas son
**las dos mitades condicionales de UN bullet**, no dos reglas. El bullet
canónico está en `canon/modelo-decision-v4_0.md:501`, verbatim:

> **SI** se ofrece un producto financiero por un **canal de confianza personal**
> (recomendación, no institución fría) **ENTONCES** sube la adopción; sin puente,
> desconfía — PORQUE G1 — `[FUERTE]`. · **id:** `dinero.ahorro.informal_sin_puente`
> **+** `con_puente_y_respaldo`

Consecuencia operativa, y es la que decide el veredicto de (d): **la SITUACIÓN
de la regla no es «tener una red personal», es «que el producto llegue por un
canal personal»**. Su falsador está escrito aparte, en `G1a`
(`canon/modelo-decision-v4_0.md:436`): *«Se refuta si un producto llega a un
segmento por canal personal y **no** sube la adopción frente a un canal
impersonal comparable, a utilidad igual.»* Eso exige observar el canal en
**adoptantes y no adoptantes**.

---

## 1 · Método del censo, y su límite declarado

Siete censores independientes (uno por pieza; ENDUTIH y ENIF partidos por ola y
por fuente) abrieron los payloads reales, y **un refutador adversarial por
pieza** atacó cada veredicto con comandos propios: si el veredicto era negativo,
buscando lo que se le hubiera escapado; si positivo, tratando de romper el
mapeo. Un crítico de completitud cerró preguntando qué modalidad no se corrió.
La supervisión abrió por su cuenta el FD de ENDUTIH 2024/2025, el cuestionario de
ENIF 2024, `data/manifiesto.yaml` y `data/diseno-muestral.yaml`, y las cifras que
esta nota cita están comprobadas contra esos archivos.

**A.13 — todo negativo declara qué examinó y trae control positivo.** Cada
veredicto negativo de abajo nombra el comando, el número de archivos/filas/
variables que recorrió y el control positivo que demuestra que el comando estaba
mirando donde se cree. En esta caja `grep` es `ugrep -I` y descarta en silencio
un archivo con un byte no-UTF8; los barridos sobre datos de INEGI (latin-1)
corrieron con `grep -a` o con Python `encoding='latin-1'`.

**Diseño muestral — citado, y re-verificado, no heredado.**
`data/diseno-muestral.yaml:589-612` declara `ENDUTIH 2024` **`MAPEADO`** con
**cuatro** ponderadores por tabla (`FAC_VIV`, `FAC_HOG`, `FAC_HOGAR`, `FAC_PER`),
`EST_DIS` (≠ `ESTRATO`, que es socioeconómico) y `UPM_DIS` (≠ `UPM`, que es
llave), y corrige expresamente a `FP-84`, que atribuía a ENDUTIH un solo
`FAC_PER`. `:194-199` declara `ENIF` `MAPEADO` con `fac_per`/`est_dis`/`upm_dis`.
Los tres nombres se re-verificaron **contra la cabecera real** del DBF y del CSV
en este acto: en el microdato están en **mayúsculas** (`FAC_PER`, `EST_DIS`,
`UPM_DIS`), no en minúsculas como los escribe `diseno-muestral.yaml` para ENIF.

---

## 2 · Veredicto por pieza

| pieza | fuente | qué se abrió | veredicto A.4 |
|---|---|---|---|
| (a) | **ENDUTIH 2023** | `FD_ENDUTIH2023.xlsx` (1 099 filas de FD) + `endutih2023_bd_dbf.zip` (5 DBF, `tic_2023_usuarios` 229 var., N=58 922) | `EXISTE-NO-SATISFACE` |
| (a) | **ENDUTIH 2024** | `fd_endutih2024.xlsx` (477 var. en 5 tablas) + `endutih2024_bd_dbf.zip` (5 DBF, N=58 080) | `EXISTE-NO-SATISFACE` |
| (a) | **ENDUTIH 2025** | `fd_endutih2025.xlsx` (8 hojas) + `endutih2025_bd_dbf.zip` (5 DBF, `ti25usu.dbf` 239 var., N=57 810) | `EXISTE-NO-SATISFACE` |
| (b) | **CoDi / Banxico** | `banxico_codi_cuentas_validadas_x_mil_hab_trimestral.xlsx` (3 hojas) + `banxico_codi_avances_banco_mexico.html` | `EXISTE-NO-SATISFACE` |
| (c) | **SAT / CNGF** | 2 sondas de red + `data/manifiesto.yaml` (20 529 líneas) | `NO-ENCONTRADO` |
| (d) | **ENIF 2024 · cuestionario** | `enif_2024_cuestionario.pdf` (32 pág., 14 secciones, 2 534 líneas de volcado) | `EXISTE-NO-SATISFACE` |
| (d) | **ENIF 2024 · FD + microdato** | `enif_2024_fd.xlsx` (398 var.) + `enif_2024_bd_csv.zip::TMODULO.csv` (13 502 personas 18+) | `EXISTE-NO-SATISFACE` |

**Cierre del censo: `0` `EXISTE-SATISFACE` de `7` piezas sobre `4` candidatas.**
El propio encargo lo previó: *«NO-ENCONTRADO en las cuatro» es entregable, no
fracaso*. Lo que sigue es **por qué**, que es lo que vale.

---

## 3 · (a) · ENDUTIH — la conducta sí está; la situación no, y el ítem fiscal se autoselecciona

### 3.1 · Lo que ENDUTIH **sí** trae, y es más de lo que el encargo suponía

Las tres olas traen, en la tabla de personas (`*_usuarios`), un bloque explícito
de **gobierno digital**, con el texto verbatim del FD:

| variable | texto del FD | universo | ponderador / diseño |
|---|---|---|---|
| `P7_31_2` | *7.31 … los pagos que ha realizado por internet, ¿han sido por… servicios o trámites de gobierno?* | `P7_28=1` (ya pagó algo por internet) | `FAC_PER` / `EST_DIS`×`UPM_DIS` |
| `P7_35_1..5` | *7.35 En los últimos 12 meses, ¿ha utilizado internet para… comunicarse con el gobierno? / consultar información del gobierno? / descargar formatos del gobierno? / **realizar trámites del gobierno**? / Otra interacción* | **todos los usuarios de internet (`P7_1=1`)** | `FAC_PER` / `EST_DIS`×`UPM_DIS` |
| `P7_36_1..5` | *7.36 En los últimos 12 meses, por internet, ¿ha realizado… **declaración de impuestos**? / gestión o solicitud de documentos personales como CURP, credencial de elector, cédula profesional, pasaporte…? / trámites de instituciones de educación pública…? / citas médicas en instituciones públicas (IMSS, ISSSTE…)? / Otros trámites* | **solo quienes dijeron Sí a algún `P7_35_*`** | `FAC_PER` / `EST_DIS`×`UPM_DIS` |
| `P7_37` | *7.37 … ¿con qué frecuencia ha realizado consultas o trámites de gobierno?* | ídem `P7_36` | `FAC_PER` / `EST_DIS`×`UPM_DIS` |

La estructura del bloque es **idéntica en 2024 y 2025** (verificado comparando
los volcados de las dos hojas `*_usuarios`): la serie es comparable.

**`P7_35_4` corrige parcialmente el faltante (iii) de `ADR-287`.** En ENCIG, la
sección VII solo la contesta quien hizo el trámite, así que
`cobertura_formal: false` seleccionaba fuera del universo. En ENDUTIH,
`P7_35_4` se le pregunta a **todo usuario de internet**, adopte o no:

| ola | `N` tabla usuarios | `P7_1=1` (usa internet) | `P7_35_4=1` | `P7_35_4=2` |
|---|---|---|---|---|
| 2023 | 58 922 | 46 631 | **8 062** | 38 569 |
| 2024 | 58 080 | 47 240 | *(no desglosado por el censor; universo 47 240)* | — |
| 2025 | 57 810 | 48 718 | **9 221** | 39 497 |

Conteos crudos, leídos del DBF completo, **sin ponderar y sin cruzar contra nada**.

**Y `P7_36_1` es el único ítem de trámite fiscal explícito de todo el corpus.**

### 3.2 · Por qué aun así **no satisface**: tres faltantes, uno nuevo

**(i) Cero marcador de obligatoriedad o de coerción del canal.** Barrido
`obliga|obligator|exig|forzos|forzad|coerc` sobre el FD completo de las tres olas:
**0 aciertos** — 1 099 filas de FD en 2023, 477 variables documentadas en 2024,
**374 columnas de dato** (27 residentes + 239 usuarios + 108 usuarios2) sobre
~1 119-1 136 filas no vacías de FD en 2025. *Control positivo con el mismo comando y el mismo
archivo*: `gobierno` devuelve 6 líneas en 2023 y 6 en 2024, `pago` devuelve 27 en
2024 — el comando sí examinaba el contenido. Tampoco hay ítem de **percepción**
de riesgo: `riesgo|miedo|temor|multa|sanción` = 0 en 2025. Los únicos
«desconfía» del instrumento (`P7_22_5`, `P7_29`=3) son sobre **fraude y robo de
datos** en compras y pagos en línea, no sobre una autoridad fiscal.

**(ii) El faltante (ii) de `ADR-287` empeora: aquí no es mala
operacionalización, es ausencia total del ítem.** En ENCIG el defecto era que
`P7_3=7` mide *fracaso del trámite*, no *rechazo del canal*. En ENDUTIH,
**el bloque de gobierno no trae batería «por qué no»**, mientras que las cuatro
áreas hermanas sí la traen: dispositivo (`P6_3`), internet general (`P7_2`),
compras (`P7_22`) y pagos (`P7_29`). Los 39 497 usuarios de internet que en 2025
dijeron «No» a *realizar trámites del gobierno* **no reciben ninguna pregunta de
motivo**. Sin motivo, un «No» no se puede leer como *rechaza_servicio*: puede ser
que no tuviera trámite que hacer.

*Precisión que aporta la refutación adversarial, y que acota el argumento sin
tumbarlo*: gobierno **no** es la única área sin batería de motivo — `P7_19`
(ventas por internet) y `P7_33` (banca electrónica) tampoco la tienen. Lo que se
sostiene no es la exclusividad del hueco, sino su consecuencia: **para la única
conducta que la regla necesita, el motivo no existe**.

**(iii) El ítem fiscal está autoseleccionado al 100 %, y eso está medido, no
supuesto.** `P7_36_1` solo se pregunta a quien contestó Sí a algún `P7_35_*`.
Verificado por cruce exhaustivo **sobre el DBF entero**, no sobre el FD:

- **2025**: `16 362 / 16 362` de los `P7_36_1` no-blancos tienen algún
  `P7_35_i = '1'`; **cero** sin ninguno.
- **2024**: la intersección `P7_36`-lleno ∧ `P7_35`-unión=Sí es **`15 557`**, que
  es *exactamente* la unión.
- **2023**: `n = 15 083`, misma construcción, verificada en el propio microdato
  (**el FD no documenta este salto** — se descubrió leyendo los datos).

Es la réplica exacta del defecto (iii) de `ADR-287`, en otra encuesta.

**(iv) Y un cuarto faltante, propio de esta fuente y que `ADR-287` no tenía:
`P7_36_1` no tiene denominador de exposición.** Aunque se aceptara el universo
autoseleccionado, `P7_36_1 = 2` («no hizo declaración de impuestos por internet»)
mezcla a **quien rechazó el canal coercitivo** con **quien no está obligado a
declarar**. ENDUTIH no pregunta si la persona tiene obligación fiscal —no hay
`RFC`, ni régimen, ni condición de contribuyente en las 239 variables—, así que
el denominador de «a quién se le ofreció el servicio coercitivo» **no existe**.
Es el mismo error de clase que `fracaso ≠ rechazo`, un nivel más arriba:
*no obligado ≠ rechaza*.

**Veredicto (a): `EXISTE-NO-SATISFACE` en las tres olas. No se propone sucesor
en ENDUTIH para `tramite.gobierno_digital.coercitivo`.** La razón no es que
falte la conducta —está, y mejor medida que en ENCIG— sino que **falta entera la
situación**: sin marcador de obligatoriedad, sin percepción de riesgo fiscal y
sin denominador de obligación, `contexto_producto {coercitivo: true,
riesgo_fiscal_percibido: true}` no se puede construir ni por reactivo ni por
construcción del universo.

**Por qué no vale el atajo de construir el universo, como sí valió en
`MAESTRA34-L5`.** Aquel acto impuso `coercitivo: false, riesgo_fiscal: false`
restringiendo a `N_TRA=01` (pago de luz): un tipo de trámite del catálogo cuya
naturaleza no coercitiva es una propiedad del **trámite**. Aquí haría falta lo
simétrico —restringir a la declaración de impuestos— pero la coerción de declarar
es una propiedad de **la persona** (estar obligada), no del trámite, y esa
propiedad **no está en el instrumento**. El atajo produciría un número, y sería
el defecto que `ADR-25` creó y `ADR-37` corrigió: un gate que pasa por la razón
equivocada.

---

## 4 · (b) · CoDi — qué mide de verdad, y por qué su escala no es una `p`

Se abrió `banxico_codi_cuentas_validadas_x_mil_hab_trimestral.xlsx`, que
`data/manifiesto.yaml:10658` declaraba **«No abierto/parseado en este acto»**.

- **3 hojas**: `Metadatos`, `Cifras_Estatales` (544 filas = 32 entidades × 17
  trimestres, **2022-T1 → 2026-T1**) y `Fuente_LADA` (6 725 filas, ~411 LADAs).
- **Qué mide**, verbatim de los metadatos: *«acumulado histórico de cuentas
  validadas en CoDi activas hasta el último día del trimestre»*.
- **Emisores**: Banxico + CNBV + CONAPO.
- **Denominador**: la columna `Cuentas_por_1000_Adultos` usa **población de 15 a
  64 años de CONAPO, interpolada** — *no* «habitantes» totales, pese al nombre
  del archivo. **El rótulo del archivo contradice su propia hoja**, y se declara:
  es el tercer caso de esta clase que el programa registra, tras la columna
  `T VOTARON` de Zacatecas 2024 y el `Votación Total = 3` de Chihuahua 2016
  ([[feedback_identifica_contenido_por_identidad_no_por_rotulo]]).
- **Cross-check exacto** entre las dos hojas de agregación en las 17 filas
  trimestrales: mismo dato primario, dos vistas.
- **Nacional 2025-T3 = `21 884 617` cuentas validadas acumuladas**, que confirma
  contra fuente primaria el «21.8 M» de prensa (`+0.39 %`), reproduciendo lo que
  `forense/notas/2026-08-08-explora2.md` ya había establecido.
- `banxico_codi_avances_banco_mexico.html` es **avance institucional**
  (participantes SPEI, tiempos de procesamiento), no cuentas de usuario final.

**Corrección que la refutación adversarial sí impuso, y que vale registrar.**
El censo original sostuvo, además del veredicto, que *«no existe un desenlace
binario rechaza/adopta por persona»* para CoDi. **Eso es falso**, y el propio
árbol lo desmiente: `forense/ficha-r34-condBC-v1_0.md:117` declara que el
desenlace exacto —no-uso de CoDi entre usuarios digitales— **existe dos veces**,
en `ENDUTIH` `P7_32_6` (*«…mediante sistema de Cobro Digital (CoDi)?»*, tres
olas, con `FAC_PER`/`UPM_DIS`/`EST_DIS`) y en `IFT SFD 2024`, y una tercera en
`ENIF 2024` (`P7_2_1`/`P7_3_1`). **El veredicto de (b) no cambia** —lo sostiene
el argumento de escala de abajo, no la inexistencia del desenlace— pero su razón
se acota aquí: lo que falta en las tres fuentes con desenlace individual **no es
la conducta, es la situación**, exactamente como en §3.2.

**Dictamen de escala (A-bis 3).** La serie es **agregada y administrativa**: su
unidad es la **cuenta**, no la persona; su escala es **cuentas acumuladas** (y
cuentas por mil adultos), no una **proporción de individuos**. Por tanto **no es
la `p` de `tramite.gobierno_digital.coercitivo` y no puede serlo sin un enlace
declarado que este acto no tiene**. Sirve, y solo sirve, como **backtest
actualizado de la `nota_validacion`** de la regla —*«Backtest: CoDi = 3.09M
cuentas con ≥1 transacción en 6 años»*— y así se reporta: **sin entrada en la
propuesta**, exactamente como el encargo ordenó.

---

## 5 · (c) · SAT / CNGF — dos sondas, dos negativos, y las recetas

**En corpus: no están.** Barrido propio de la supervisión sobre
`data/manifiesto.yaml` (20 530 líneas, 1 516 869 caracteres, Python `utf-8`):

| término | aciertos |
|---|---|
| `SAT` (palabra completa) | **0** |
| `buzón`/`buzon` | **0** |
| `e.firma` | **0** |
| `RFC` | **0** |
| `gobierno digital` / `gobierno electrónico` | **0** |
| `coerc` | **0** |
| `cngf` | **0** |
| `obligator` | 31 |
| `fiscal` | 17 |
| `trámite` | 30 |

*Control positivo*: los tres términos con aciertos demuestran que el comando
examinaba el archivo. Y los aciertos, **abiertos uno por uno**, no son el
constructo: los **31** `obligator` son, 27 de ellos, la fórmula de **cita
obligatoria** de ENNViH (*«obligatoria: Rubalcava, L. y Teruel, G. …»*), más
`cses5` y `gps` (cita obligatoria), un `voluntario/obligatorio` de un padrón
agrícola y un `percent-encoding obligatorio`; los **17** `fiscal` son
**fiscalización electoral del INE**, la **ASF**, un calendario fiscal agrícola y
`ejercicio_fiscal` de Contraloría Social. **Ninguno es percepción de riesgo ni
obligatoriedad de canal.**

**En red: dos sondas, una cada una, como el encargo ordenó.**

```
curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/programas/cngf/   → 200, exit 0
curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.sat.gob.mx                     → 200, exit 0
```

**Identidad, no rótulo — y los dos `200` son engañosos.** Se bajó el cuerpo de
las dos:

- `https://www.inegi.org.mx/programas/cngf/` devuelve **321 bytes**: un *stub* de
  redirección por JavaScript. El programa real vive en
  `https://www.inegi.org.mx/programas/cngf/2025/`. **CNGF existe**, pero su
  identidad —confirmada por título y metadatos, y por la ficha RNM
  `https://www.inegi.org.mx/rnm/index.php/catalog/1145`, que es estática y
  declara *«UNIDAD DE ANÁLISIS: Instituciones…»*— es un **censo administrativo a
  instituciones de la Administración Pública Federal**. **No tiene unidad de
  observación individual**, así que no puede dar la conducta *rechaza/adopta* que
  la regla necesita; a lo sumo daría **oferta** agregada. La ficha RNM tampoco
  menciona `obligator` ni una vez, lo que descarta además la hipótesis de
  «oferta de trámites digitales **obligatorios**».
- `https://www.sat.gob.mx` devuelve **1 477 bytes**: el *shell* de una SPA
  (SvelteKit), **sin `<title>` y sin texto**. Todo el contenido se renderiza por
  JavaScript. **`200` no es contenido**: la sonda no puede afirmar ni negar qué
  publica el SAT desde el HTML estático.

**`datos.gob.mx` (CKAN) no se reintentó.** Dio `404` / `curl exit 35` el
1/sep/2026; el encargo ordenó declararlo y no reintentar sin ruta nueva, y así se
hizo.

**Veredicto (c): `NO-ENCONTRADO`.** No es `NO-ACCESIBLE`: la red respondió las
dos veces. Es que **ninguna de las dos fuentes publica lo que la regla necesita**
—CNGF por unidad de observación (instituciones, no personas), SAT porque su
portal no expone microdato ni estadística de obligatoriedad de canal por esta
ruta—. Recetas para mesa, ≤1 minuto cada una, en §8.

---

## 6 · (d) · ENIF 2024 — el puente existe, y está anidado en el desenlace

### 6.1 · Lo que hay, con universo y `n` contados

`enif_2024_bd_csv.zip::TMODULO.csv`, **13 502 personas de 18+** (`EDAD_V` 18-98,
sin faltantes), ponderador `FAC_PER`, diseño `EST_DIS` × `UPM_DIS` —los tres
nombres verificados **contra la cabecera real del CSV**, no heredados—.

**PUENTE — el canal personal, que es la situación que la regla nombra:**

| variable | texto verbatim | universo | `n` no-blanco |
|---|---|---|---|
| `P5_15_2` | *5.15 Para comparar su cuenta, ¿utilizó… **recomendaciones de amistades o personas conocidas**?* | gateado en `P5_14=1` (comparó antes de contratar), que a su vez está gateado en **tener la cuenta** | 1 529 (729 Sí / 800 No) |
| `P6_11_2` | ídem, crédito | gateado en `P6_10=1` ∧ tener el crédito | 1 512 (651 / 861) |
| `P8_12_2` | ídem, seguro | gateado en `P8_11=1` ∧ tener el seguro | 866 (354 / 512) |
| `P5_16` / `P6_6` / `P8_9` | *5.16 ¿Usted contrató su (última) cuenta… en la sucursal(1) / a través de **la empresa donde trabaja**(2) / app(3) / internet(4) / **Oxxo, Walmart**(5) / **con personal promotor**(6) / **a través del programa social**(7)…* | gateado en tener el producto (verificado exacto: `P5_16` ↔ `any(P5_4_*=1)` = 9 156) | 9 156 / 5 248 / 1 922 |

**AFORE (sección 9) no tiene ninguna variable de puente** —ni comparación ni
canal—, a diferencia de los otros tres productos. **Y las seis vías informales de
ahorro (`P5_1_1..6`) tampoco**: el instrumento nunca pregunta quién le recomendó
su tanda, su caja de ahorro o guardar con familiares. *Control positivo del
silencio*: el mismo barrido de `comparar|recomendación|promotor` sobre el volcado
íntegro del FD (1 578 líneas, las 398 variables con sus catálogos) encuentra
**45** coincidencias reales —incluidas las tres `*_2` de arriba y `P6_17_5`— y
**cero** en la sección 9 y en la 5.1. El comando sí veía; la ausencia es real.

**RESPALDO — «¿alguien responde por mí?»:**

| variable | texto | universo | `n` |
|---|---|---|---|
| `P6_17_5` | *6.17 ¿Cuáles son las razones por las que le negaron el crédito? **Falta de garantía, fiadora, fiador o aval*** | **triple gate**: tuvo/solicitó crédito → fue rechazado | 2 463, de los cuales **`n=72`** en la categoría de interés |
| **`P4_9_4`** | *4.9 Si el día de hoy se le presentara la oportunidad de comprar una casa, un terreno o abrir un negocio, ¿usted podría aprovecharla… **con el préstamo de familiares o amistades**?* | **universo completo, sin gate: `13 502 / 13 502`** | **3 145 Sí / 10 357 No** |
| `P4_4_1` | *4.4 La última vez que no pudo cubrir sus gastos, ¿usted **pidió prestado a familiares o personas conocidas**?* | gateado en `P4_3=2` (no le alcanzó); `n` = 5 321, coincide exacto | 2 763 / 2 558 |
| `P13_3` (ítem 4) | financiamiento de un activo con *préstamo de familiares, amistades o personas conocidas* | por activo poseído | — |

**`aval|fiador|garante` aparece UNA sola vez en las 2 534 líneas del
cuestionario** (verificado por barrido): es `6.17`. Y **«se lo han ofrecido»
aparece una sola vez** (opción 3 de `8.3`): **ENIF nunca pregunta a la población
general si le ofrecieron un producto**, ni por qué canal.

**CONFIANZA como razón de no tenencia** — existe y es amplia, pero toda en
baterías de **código único** (`CIRCULE UN SOLO CÓDIGO`), lo que la hace competir
con 6-10 razones alternativas y **subestimarla**: `P5_20`=03 (`n=183`),
`P6_14`=4 (`n=217`), `P8_3`=2 (`n=336`), `P9_2`=6 (**`n=38`**), `P11_5`=2.
Tres de las cuatro caen por debajo o cerca de 200. `P11_1` (confianza
institucional genérica, sin gate) es la única batería de confianza **no**
contaminada por selección, pero mide confianza en el **sistema**, no en un canal
personal.

### 6.2 · Por qué no satisface: la situación está anidada en el desenlace

La regla exige (`G1a`) comparar **canal personal contra canal impersonal, a
utilidad igual, sobre la adopción**. En ENIF 2024:

- El **canal** (`P5_15_*`, `P6_11_*`, `P8_12_*`) solo se observa entre quienes
  **ya adoptaron y además compararon** — un gate doble.
- Dentro de ese universo, **la adopción es constante e igual a 1**. La varianza
  del desenlace que la regla quiere explicar **no existe ahí**.
- `P5_16` sí da el canal de contratación sobre todos los tenedores, pero **no
  incluye «recomendación de un familiar o amigo» entre sus 8 opciones** — el
  puente personal, justamente, no es una de ellas.
- Y no hay pregunta alguna, a la población general, sobre si le ofrecieron un
  producto por un canal personal.

Es el **cuarto** caso del mismo patrón que este programa lleva registrado:
`ADR-287`(iii) en ENCIG, `P7_36_1` en ENDUTIH (§3.2), `P5_15` aquí, y el eje
anidado que `MAESTRA35-L1` documentó con `P5_4` frente a `informal_cualquiera`
([[feedback_eje_anidado_en_el_desenlace]]). **Medir el puente sobre ese universo
no refutaría ni corroboraría nada: el instrumento garantiza el resultado.**

**Veredicto (d): `EXISTE-NO-SATISFACE` para la regla completa.**

### 6.3 · Pero la mitad «respaldo» **sí** es observable, y ésa es la entrega

La regla nombra dos condiciones —`sin_puente` y `con_puente_**y_respaldo**`—.
El **canal** no es observable fuera del universo de adoptantes. El **respaldo**,
en cambio, tiene en `P4_9_4` una medida **declarada, general y no anidada**:
`13 502 / 13 502`, sin gate, y lógicamente previa a cualquier producto formal
(pregunta por la capacidad de conseguir un préstamo personal, no por tener uno).
Cruzarla contra la tenencia de producto formal (`P5_6_*`, `P6_2_*`, `P8_6_*`) es
una **asociación** (A-bis 1/2) sobre el universo completo, con `FAC_PER` y
bootstrap conglomerado — y es exactamente el dato que la firma `m1` de mesa pedía
para que la re-lectura de la regla la traiga dirección **con dato y no con
narrativa**. Se congela en `COMMIT-1` (§7) y se mide en `P2`.

---

## 7 · Lo que este censo habilita, y lo que no

**No habilita** ninguna `p` para `tramite.gobierno_digital.coercitivo`. El prior
`0.09 / 0.91` **sigue siendo el único `ASIGNADO` vigente sin dato**, y `S1` del
tablero **no baja de 1 a 0**. Se declara en el contador.

**No habilita** ninguna `p` para el canal personal de
`dinero.ahorro.informal_sin_puente` / `con_puente_y_respaldo`.

**Sí habilita**, y este acto las mide en `P1` y `P2` con spec congelada aparte:

1. **`P4_9_4` × tenencia de producto formal** (ENIF 2024) — la mitad *respaldo*
   de la regla, sobre universo completo. Es la entrega de (d).
2. **`P7_35_4`** (ENDUTIH 2023/2024/2025) — la **adopción nacional de trámites de
   gobierno por internet**, sobre universo limpio (todo usuario de internet).
   Esto **no es** la `p` de `coercitivo`, y se dice: es la cifra que la
   `estampa A.10` de la regla espejo `tramite.gobierno_digital.util_sin_coercion`
   declara expresamente **no** haber medido —*«No es la adopción de gobierno
   digital en México»*, `milpa/tramite.yaml`—. Medirla cierra una reserva que el
   propio motor tiene escrita.

**Ambas van a la propuesta como `PENDIENTE-DE-MESA`; ninguna se carga al motor.**
La segunda **excede la letra de `P1`** del encargo, que la condicionaba a que (a)
satisficiera; se declara aquí como adición razonada bajo la instrucción de mesa
del 2/sep («censo y medición en el mismo acto») y la regla de señal, y **la
adjudica mesa**, no el ejecutor.

---

## 8 · Recetas para mesa (≤1 min cada una) y filas de cola

**CNGF.** `curl -s https://www.inegi.org.mx/rnm/index.php/catalog/1145` (ficha
RNM, estática, sin SPA) confirma unidad de análisis = instituciones. Si mesa
quiere **oferta** de trámites digitales obligatorios como covariable de contexto,
la ruta es el tabulado del programa `cngf/2025/`, no el microdato — y **no da
conducta individual**, así que no cierra la regla por sí sola.

**SAT.** El portal es una SPA; la ruta estática es el **Anuario Estadístico del
SAT** / `omawww.sat.gob.mx`. Sonda de 1 minuto:
`curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 http://omawww.sat.gob.mx/cifras_sat/Paginas/inicio.html`.
Aun así, el SAT publica **agregados de contribuyentes**, no percepción: cerraría
el **denominador de obligación** que §3.2(iv) declara faltante, no la conducta.

### 8.1 · Una quinta candidata, censada por la supervisión y cerrada

El corpus trae tres **Encuestas de Competencias Financieras de Banxico**
(`banxico_encuesta_competencias_financieras_2019/2021/2024.xlsx`, con manuales
de 2019 y 2021 — **la de 2024 no tiene manual en el corpus**, así que sus 145
columnas son códigos `SD*`/`SF*` sin texto de reactivo, el mismo hueco de
descriptor que `FP-115(c)` levantó para ENSAFI 2023). Ninguna de las cuatro
piezas del encargo la nombra; se censó igual, porque es la única otra fuente del
corpus con unidad **persona** y objeto **financiero**.

Barrido sobre el manual de 2021 (`pdftotext -layout`, **1 170 líneas / 70 533
caracteres**):

| término | aciertos |
|---|---|
| `recomend` | **0** |
| `aval\|fiador\|garant` | **0** |
| `obligator\|coerc\|fiscal\|impuest` | **0** |
| `amistad\|amigo\|familiar\|conocid` | 19 |
| `ahorr` *(control positivo)* | 28 |

Los 19 aciertos de red personal son, uno por uno, **conducta informal ya
realizada** —*«Pidieron prestado a familiares o amigos»*, *«lo que ustedes han
prestado a amigos o familiares»*—, nunca el canal por el que llega un producto
formal. Es el mismo constructo distinto que §6.2. Coincide con lo que
`forense/ficha-r34-condBC-v1_0.md` fila 7 ya había censado sobre los dos manuales
(179 645 caracteres): cero aciertos fiscales, control positivo `ahorro` = 34 y 38.
**No aporta candidata: `EXISTE-NO-SATISFACE`, quinta.**

**Término no barrido que mesa podría querer:** `ENCRIGE` (Encuesta Nacional de
Calidad Regulatoria e Impacto Gubernamental en Empresas) — unidad *empresa*, no
persona; se nombra para que el siguiente censo no lo redescubra.

---

## 9 · Estampa A.10

Este censo describe **el corpus del 2 de septiembre de 2026** y las olas
**ENDUTIH 2023/2024/2025** y **ENIF 2024**. ENDUTIH publica cada año y ENIF cada
tres: **una ola futura puede añadir el reactivo que falta y este veredicto
caducaría**. Lo que caduca es el veredicto sobre la fuente, no el defecto de
diseño que lo produce.

---

## 10 · Adenda del crítico de completitud — dos piezas que el censo no abrió

**Escrita después del commit de `P0` (`833604c`), no dentro de él.** El censo se
cerró con siete piezas y siete refutaciones; un último agente preguntó **qué
falta** y encontró dos fuentes que el propio acto ya nombraba por escrito y que
nadie había abierto. Las dos se verificaron **contra el archivo real** por la
supervisión antes de escribirse aquí, y una de las dos afirmaciones del crítico
se corrige en el proceso.

### 10.1 · Sexta candidata · IFT · Servicios Financieros Digitales 2024

`data/raw/ADQ15_IFT_SFD_uso_confianza/basededatossfd.zip` →
`Bases_de_datos_Servicios_Financieros_Digitales (SFD).xlsx`, dos hojas de
microdato con factor de expansión (`Int&TV` 8 400 × 107, `TelMóvil` 5 305 × 76).
El censo la citaba en §4 sin abrirla.

**Y trae el puente — publicado, real, e invisible en las columnas.** La batería
*«¿A través de qué medios se enteró de los SFD?»* tiene **cinco** columnas
codificadas (sucursal, aplicación de celular, página de internet, redes
sociales, «Otro»), todas sobre un universo de **2 681**. **«Familiares y
amistades» no es una de ellas.** Pero el reporte del IFT sí la publica como
categoría del gráfico, y el rastro está en el texto libre: de las **96**
respuestas «Otro», **70 escriben literalmente «Familiares y amigos»** y **7**
«Recomendación de personas que trabajan ahí» — **77 de 96**, contadas por la
supervisión sobre el archivo.

**Esto es un hallazgo de método, no sólo de fuente.** Quien abra únicamente la
cabecera del `xlsx` concluye que la variable **no existe**, y se equivoca: existe,
está medida, y el emisor la publica agregada. Es la misma clase de defecto que
[[feedback_identifica_contenido_por_identidad_no_por_rotulo]] ya registró en otro
sentido: **el catálogo de columnas no agota lo que el instrumento midió.**

**Aun así, `EXISTE-NO-SATISFACE` para las dos reglas de este acto**, por tres
razones contadas:

1. **Nada de gobierno ni de riesgo fiscal.** Barrido propio de
   `gobierno|trámite|SAT|impuest|obligator|coerc|fiscal` sobre el texto del
   reporte (**2 788 líneas / 305 510 caracteres**) → **6 aciertos**, abiertos uno
   por uno: cuatro son *«trámites ágiles»* / *«pocos trámites y requisitos»* como
   **argumento de venta de fintechs**, uno es *«Regulaciones del gobierno»* como
   factor cualitativo de confianza en el regulador, y ninguno es el constructo.
   Sobre las **183** cabeceras de las dos hojas → **1** acierto, que es *«¿sabe a
   qué institución acudir ante algún problema…?»* — a quién reclamar, no riesgo
   fiscal. *Control positivo*: `confian` = **29** aciertos en el mismo texto.
   *(Aquí se **corrige** al crítico, que había reportado «0 hits sustantivos»:
   son 6, y el negativo se sostiene por lectura, no por ausencia de aciertos —
   misma disciplina que los 22 casi-aciertos de `ADR-186`.)*
2. **`n = 70` en texto libre sin codificar**, sobre 2 681. No alcanza para
   ninguna celda, y exigiría un paso de codificación que este acto no hace.
3. **Sin diseño muestral.** `data/diseno-muestral.yaml` no tiene fila para IFT
   SFD: hay factor de expansión post-estratificado, **no** estrato ni UPM, así
   que ningún `IC` conglomerado es construible. Corrobora
   `forense/ficha-r34-condBC-v1_0.md:196`.

### 10.2 · La fuente narrativa de las dos reglas se desmiente a sí misma

`corpus/reports/Adopción_y_Resistencia_Tecnológica_en_México…md` (177 líneas) es
**`report:tecnologia`**, y `milpa/procedencia.yaml` lo cita como `fuente_citada`
de `dinero.ahorro.con_puente_y_respaldo` **y** de la regla `coercitivo` vía
`validacion:CoDi`. Nadie lo había abierto. Verbatim, de su propia sección
`## Caveats` (línea 159), bajo el rótulo **«Mitos y sobreinterpretaciones a
desmontar»**:

> **4.** *«La confianza radial explica la adopción.» Hipótesis atractiva **sin
> evidencia conductual directa**; usarla como hallazgo repite el error del corpus
> previo.*

Y en su línea 37 la marca **`[HIPÓTESIS]`**, no hallazgo:

> *13. **[HIPÓTESIS]** La confianza radial puede canalizar adopción vía
> recomendación interpersonal más que frenarla. Es plausible —pero **no probado
> con datos conductuales directos mexicanos**—…*

**El mecanismo del bullet de puente está citado como fuente de un prior por un
reporte que declara, en su propio texto, que no tiene evidencia conductual para
sostenerlo.**

Lo mismo, con otra forma, del lado `coercitivo`. El reporte llama al miedo al SAT
*«freno específico y documentado»* (línea 129), pero su **procedencia declarada**
(línea 64) es *«Banxico **vía El Economista/Fintechexpert**, sept. 2025»* —
**prensa, no encuesta**— y la cifra que da no es la de la `nota_validacion` del
motor: dice **21.8 M cuentas registradas, mayormente inactivas, con 17.8 M
transacciones acumuladas en seis años**, mientras el motor dice **«3.09 M cuentas
con ≥1 transacción en 6 años»**. Son cantidades distintas y **el `3.09 M` no
aparece en el reporte**.

**Esto no cambia ningún veredicto del censo** —no es una candidata de dato— pero
es lo más relevante que el acto encontró para la pregunta que lo motivó: las dos
reglas `ASIGNADO` que este acto vino a buscar dato **descansan sobre una fuente
narrativa que se auto-clasifica como sin sustento conductual**. Va a mesa como
tal, sin proponer reclasificación: `procedencia.yaml` está fuera del perímetro.

### 10.3 · Infraestructura que existía y no se reusó

`tools/censo_r34_bc.py` (113 líneas, en el árbol) es el barrido mecánico
corpus-completo que `ADR-186` corrió el 25/ago/2026: **321 entradas de primer
nivel de `data/raw`, 20 838 archivos** desempacados (CSV en ZIP, XLSX hoja por
hoja, PDF con unión `pypdf`+`pdftotext`), con la búsqueda `FISCAL`×`PERSONAL`
que es casi exactamente la de este acto. Los siete censores hicieron barrido
artesanal pieza por pieza. **Se declara para el siguiente acto**: la
infraestructura ya está escrita y comiteada.

---

## 11 · Séptimo instrumento, censado al propagar la firma `c1`

**Escrita al propagar la respuesta de mesa del 2/sep/2026, después del commit de
la cascada.** La firma `c1` enumera **siete instrumentos** de encuesta de hogares
en el universo examinado, y uno de ellos —**`ENCUCI 2020`**— **este acto no lo
había censado**. `ADR-287` sí la examinó, pero **para otra regla**: su `AP5_11`
mide *permisibilidad declarada* y sirvió a la pieza `P3` de `MAESTRA34-L5`
(evasión de norma), no a `tramite.gobierno_digital.coercitivo`. Heredar el
séptimo instrumento de la firma habría sido citar sin examinar, así que se censó
antes de escribirlo.

**Qué se abrió.** `data/raw/FD_ENCUCI2020.pdf` (**4 006 líneas / 422 073
caracteres**, volcado con `pdftotext -layout`) y `data/raw/BD_ENCUCI2020_dbf.zip`
— **5 tablas**, cabeceras leídas directamente del `DBF`:

| tabla | registros | campos |
|---|---|---|
| `ENCUCI_2020_SD.dbf` | 75 189 | 54 |
| `ENCUCI_2020_SEC_4_5.dbf` | 21 519 | 164 |
| `ENCUCI_2020_SEC_6_7_8.dbf` | 21 519 | 156 |
| `ENCUCI_2020_SEC_9_10.dbf` | 21 519 | 50 |
| `ENCUCI_2020_VIV.dbf` | 21 564 | 34 |

**Barrido y veredicto.**

| término | aciertos | qué resultaron ser |
|---|---|---|
| `fiscal\|impuest\|SAT\|contribuy\|RFC` | **0** | — |
| `obligator\|obliga\|coerc\|forzos\|exig` | 6 | *«derechos y **obligaciones** como ciudadano(a)»* (×3) y la batería de **exigencia** ciudadana `AP7_2_5` — ninguno es obligatoriedad de canal |
| `trámite\|gobierno digital\|en línea\|internet` | 7 | `AP4_4_08`/`AP4_6_08` *«Por internet»* como **medio de informarse/participar**; la batería de mordida (`trámite` en contexto de dádiva); `AP8_2_3` *«Agilizar trámites»* como **motivo de una dádiva** |
| `confian\|desconfian` *(control positivo)* | **79** | confianza interpersonal e institucional (`AP5_2_*`, escala de 4 puntos) |

**Veredicto: `NO-ENCONTRADO`.** ENCUCI 2020 es cultura cívica —participación,
confianza, corrupción vivida—: **no tiene bloque de gobierno digital**, no tiene
percepción de riesgo fiscal, y su único `trámite` es el objeto de una mordida.
El control positivo de 79 aciertos demuestra que el barrido sí examinaba el
archivo.

## 12 · La firma `c1` llegó corregida, y la corrección invierte el veredicto de fondo

Se deja constancia porque cambia lo que la regla dice de sí misma. La **primera**
redacción de `c1` mandaba declarar `tramite.gobierno_digital.coercitivo` como
**«HUECO DE MUNDO, no deuda de trabajo»**, con el tablero contando
«huecos de mundo: 1» y **`S1` bajando a 0**. Alcanzó a escribirse como campo
`hueco_de_mundo` en `milpa/tramite.yaml`.

La redacción **corregida**, que es la que quedó ejecutada, dice lo contrario: **la
regla sigue SIN DATO y `S1` sigue en 1**, y lo que se declara no es una ausencia
de mundo sino un **universo examinado con su veredicto** —`NO-ENCONTRADO` en
siete instrumentos por defecto de universo **de esas fuentes**, `NO-ACCESIBLE` en
las dos administrativas—, **sin afirmar nada sobre el universo no examinado**. El
campo se llama ahora `sin_dato_universo_examinado`, y `hueco_de_mundo` **no
existe** en el árbol.

La diferencia no es de redacción. «Hueco de mundo» afirma algo sobre **el mundo**;
«`NO-ENCONTRADO` en siete instrumentos, `NO-ACCESIBLE` en dos» afirma algo sobre
**lo que este programa examinó**, y deja escrito qué falta examinar — que es lo
que la cola de adquisición ya lleva como **siguiente universo declarado**:
fuentes administrativas (SAT/CNGF) **por navegador o por solicitud de
transparencia**, no por sonda desde la caja, que ya se agotó.
