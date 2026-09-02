# ACTO MAESTRA34-L5 · GOBIERNO-DIGITAL-EVASION-AHORRO · P0 · CENSO A.4

**Acto:** `ACTO MAESTRA34-L5` · **Fecha:** 2/sep/2026 · **Entorno:** UBUNTU
(`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable`, sonda INEGI `200`, corpus
compartido montado con 368 entradas en primer nivel).
**Encargo archivado (A.3):** `forense/encargos/2026-09-02-MAESTRA34-L5-GOBIERNO-DIGITAL-EVASION-AHORRO.md`,
SHA de redacción `4de5b1e`.
**Base real del acto:** `29ab80a` — `main` avanzó **6 commits** desde el SHA de
redacción (PR #465, `[L] corridas v1_2`). No es PARO: el perímetro se re-derivó
contra el árbol real y todas las premisas se re-verificaron contra `29ab80a`, no
contra `4de5b1e`.

Este commit es el P0 del encargo: **el censo antecede a toda medición**. Ninguna
pieza P1–P4 tiene aquí spec congelada ni resultado; las specs viven en sus propias
notas (COMMIT-1 de cada pieza) y los resultados en el COMMIT-2 de cada una.

---

## §0 · Premisas del encargo, verificadas contra el árbol (A.8)

Las cinco premisas sustantivas del encargo se comprobaron una por una contra
`29ab80a`. **Las cinco son verdaderas.** Se declara el comando de cada una.

| premisa del encargo | comando | resultado |
|---|---|---|
| `tramite.evasion_norma` vigente con clase ASIGNADO 0.66/0.34, `situacion: enfrenta_norma_percibida_inutil_o_extractiva`, `disparadores {sancion_creible: false}` | `sed -n '203,228p' milpa/tramite.yaml` | **VERDADERA**, verbatim; añade `contexto_norma: {percibida_util: false}` que el encargo no cita y que este acto sí usa |
| `tramite.gobierno_digital.coercitivo` ASIGNADO, `rechaza_servicio` 0.91, `cobertura_formal: false` | `sed -n '162,175p' milpa/tramite.yaml` | **VERDADERA**, verbatim; añade `contexto_producto: {coercitivo: true, riesgo_fiscal_percibido: true}` |
| `tramite.gobierno_digital.util_sin_coercion` ASIGNADO, `adopta` 0.71 | `sed -n '177,201p' milpa/tramite.yaml` | **VERDADERA**; la regla **no tiene bloque `disparadores`**, solo `contexto_producto: {coercitivo: false, riesgo_fiscal_percibido: false}` |
| «filas 3-4 de `MAESTRA33-E18`·P1: sin generador declarado» | `grep -nE '^\|' forense/notas/2026-09-01-MAESTRA33-E18-P1-reglas-activos-sin-p.md` | **VERDADERA y exacta**: fila 3 = `tramite.evasion_norma`, fila 4 = las dos de gobierno digital, ambas «NO — solo ASIGNADO», generador «(no declarado en yaml)» |
| corpus: `encig25_base_datos_csv`, `enif_2024`, ENCUCI 2020 existen | `ls data/raw/`, `data/manifiesto.yaml:4214/992/5427` | **VERDADERA** las tres; se añade que `envipe2025_csv` también existe y se usa (ver P3) |

**Corrección de una lectura del encargo, no de una premisa.** El encargo trata
`dinero.ahorro.tiene_ahorros` como cuarta pieza de un lote de «priors ASIGNADO
contra dato». No lo es: en `milpa/tramite.yaml:285-303` esa regla ya está
**MEDIDA** (`clase: "MEDIDO·p(tasa base ponderada)"`, p=0.174804, IC95
[0.159250, 0.190543], n=6028, ENNViH ola 2 2005-06, ponderador `fac_3b`). El
propio encargo lo dice bien al describir P4 («enmienda de re-medición»); solo la
línea del CONTADOR podía leerse mal. El contador correcto se declara en §6.

**Dos notas de higiene, sin consecuencia para el acto:** `data/raw` nació ausente
en el worktree (gitignorada, `\.gitignore:5-6`) y se enlazó a
`/home/pc0/mm-corpus/raw`; y `canon/gobernanza-v1_15.md` no tiene ADR duplicados
(`grep -oE '^\*\*ADR-[0-9]+' … | sort | uniq -d` vacío), a diferencia del defecto
de fusión que ya se documentó en este repositorio.

---

## §1 · Método del censo y universo examinado (A.13)

El censo se hace **sobre documentación** (estructura de base de datos, descriptor
de archivos, catálogos) y sobre **listas de columnas** del microdato. Se contaron
además **denominadores** — nunca cruzados contra la variable de desenlace — para
poder adjudicar si la `n` alcanza, y no solo si la variable existe. Ningún
numerador, ninguna proporción y ningún cruce desenlace×universo se calculó en
este commit.

Archivos y universos efectivamente examinados:

| fuente | archivo examinado | tamaño del examen |
|---|---|---|
| ENCIG 2025 | `data/raw/encig25_estructura_base_datos.pdf` → texto | 4 540 líneas |
| ENCIG 2025 | `data/raw/encig25_base_datos_csv.zip` (6 CSV) | **483 columnas** listadas, 124 314 filas de la sección VII contadas |
| ENCIG 2023/2021/2019/2017 | 5 ZIP de microdato | **~100 000 columnas** listadas (control de olas) |
| ENCUCI 2020 | `data/raw/FD_ENCUCI2020.pdf` → texto | 4 005 líneas / 3 081 no vacías |
| ENVIPE 2025 | `data/raw/fd_envipe2025.pdf` → texto | 7 207 líneas |
| ENVIPE 2025 | `tmod_vic_envipe2025` | 137 columnas, 40 280 filas contadas |
| ENIF 2024 | `data/raw/enif_2024_fd.xlsx` hoja `TMODULO` | 1 579 filas de descriptor |
| ENIF 2024 | `enif_2024_bd_csv.zip` → `TMODULO.csv` | 398 columnas, 13 502 filas contadas |

**Control positivo de todo negativo de este censo.** Cada «no existe» de abajo se
acompaña del conteo de lo que sí se examinó, porque un negativo producido por un
comando que no abrió archivos no es un negativo. En particular, el negativo
central (ENCIG no distingue obligatoriedad) se emite tras listar 483 columnas de
2025 y ~100 000 columnas de cinco olas, no tras un `grep` que pudo no leer nada.

---

## §2 · P1 · `tramite.gobierno_digital.util_sin_coercion` — ENCIG 2025

**Lo que la regla pide.** `situacion: le_ofrecen_servicio_gobierno_digital`;
`contexto_producto: {coercitivo: false, riesgo_fiscal_percibido: false}`;
`entonces: adopta p=0.71 / rechaza_servicio p=0.29`.

**Lo que ENCIG 2025 tiene.**

| componente | ítem | veredicto |
|---|---|---|
| situación — «le ofrecen» el canal digital | **ninguno** | **NO-ENCONTRADO como ítem** |
| disparador — `coercitivo: false` | **ninguno** | **NO-ENCONTRADO como ítem** |
| disparador — `riesgo_fiscal_percibido: false` | **ninguno** | **NO-ENCONTRADO como ítem** |
| conducta — adopta / rechaza | **`P7_3`** «¿A qué tipo de lugar acudió o a qué medio recurrió para realizar el trámite o pago?» (1 instalaciones de gobierno · 2 banco/supermercado/tienda/farmacia · 3 líneas telefónicas · 4 **Internet: página web, aplicaciones de celular o tablet** · 5 **cajero automático o kiosco inteligente** · 6 módulos/oficinas móviles · 7 no se ha podido concluir · 8 otro · 9 NS/NR) | **EXISTE** |

La sección X (`GOBIERNO ELECTRÓNICO`) de ENCIG 2025 son **seis binarias de uso**
y nada más: `P10_1_1` consultó páginas de gobierno · `P10_1_2` llenó y envió un
formato en línea · `P10_1_3` pagó en un portal público · `P10_1_4` usó redes
sociales para quejarse · `P10_1_5` hizo un trámite **completamente en línea** ·
`P10_1_6` pidió información o apoyo. Ninguna tiene denominador de oferta: son
conductas sobre toda la población adulta, no sobre quien tuvo el canal disponible.
El barrido de columnas de las cinco olas confirma que **`P10_*` nunca ha sido más
que `P10_1_1..P10_1_6`** (cuatro en 2017), es decir, la batería de *motivos de no
uso de internet* que el encargo esperaba censar **no existe en ninguna ola del
corpus**, no solo en 2025.

**Veredicto: EXISTE-SATISFACE con mapeo declarado.** La conducta se mide
directamente con `P7_3`. La situación y los dos disparadores **no** los dicta el
dato: los suple un **juicio declarado del acto** sobre el universo de trámites —
restringir a un tipo de trámite (`N_TRA`) para el que el canal digital es de
disponibilidad nacional y de uso **opcional**, de modo que «le ofrecen el
servicio», «no coercitivo» y «sin riesgo fiscal» se cumplan por construcción del
universo y no por declaración del informante. Es exactamente la forma que
`MAESTRA34-L1` usó para `con_registro` (precedente citado por el encargo) y queda
**congelada en el COMMIT-1 de P1**, no aquí.

**La `n` alcanza** (denominadores contados, sin cruzar contra `P7_3`): sección VII
tiene 124 314 filas, `P7_3` **no-blanco en las 124 314** (cero pérdida por
blanco), con `FAC_TRA`, `EST_DIS` y `UPM_DIS` presentes. Por tipo de trámite:
`N_TRA=01` (pago ordinario de luz) **n=20 392**; `02` agua potable 16 019; `03`
predial 9 533; `04` tenencia 7 851; `07` cita médica 12 128. Cualquiera de ellos
soporta IC95 conglomerado holgadamente.

**Reserva que hereda de L1 y que el COMMIT-1 debe absorber:** `sec_7` trae
**10 597 duplicados exactos** (113 717 `ID_TRA` únicos de 124 314 filas), ya
verificados y documentados por `MAESTRA34-L1` en
`forense/prereg-duelo-v2/codificacion-R-v1_0.tsv` fila `TRA-M-13`. La spec de P1
debe declarar si deduplica y con qué criterio.

---

## §3 · P2 · `tramite.gobierno_digital.coercitivo` — ENCIG 2025

**Lo que la regla pide.** `disparadores: {cobertura_formal: false}`;
`contexto_producto: {coercitivo: true, riesgo_fiscal_percibido: true}`;
`entonces: rechaza_servicio p=0.91`.

**Veredicto: EXISTE-NO-SATISFACE. No pasa a medición.** Faltan **tres** cosas, y
la tercera es la que no tiene arreglo dentro de ENCIG:

1. **Obligatoriedad — no hay ítem.** ENCIG 2025 no pregunta, en ninguna de sus
   483 columnas, si el trámite debía hacerse por fuerza en línea. El encargo
   previó exactamente este caso («si ENCIG no distingue obligatoriedad,
   EXISTE-NO-SATISFACE y se declara»), y la condición se cumple: no distingue.
2. **La conducta `rechaza_servicio` no es observable bajo obligación.** El único
   candidato en el dato es `P7_3=7` / `P7_8=3` («no se ha podido concluir el
   trámite o pago»), que es **fracaso**, no **rechazo voluntario**. Contarlos
   como rechazo sería fabricar el desenlace. Y hay una razón lógica anterior:
   donde el canal digital es obligatorio no existe canal alternativo que elegir,
   así que el rechazo deja de tener una huella en la variable de canal.
3. **`cobertura_formal: false` selecciona fuera del universo.** La regla habla de
   quien está fuera de la cobertura formal; a la sección VII solo se entra
   **habiendo realizado el trámite**. Quien evita al fisco por completo no
   aparece. Cualquier estimación sobre `N_TRA=06` (trámites fiscales ante el SAT)
   estaría condicionada a haber hecho el trámite, es decir, condicionada a la
   negación del disparador. Esto es selección por construcción, no ruido, y
   ningún ponderador la corrige.

El punto 3 es también la razón por la que **no se propone un sucesor en ENCIG**:
la ola siguiente tendría el mismo defecto. Un sucesor útil necesitaría una fuente
con población informal *y* obligación digital observada, que este censo no ubicó.

**Consecuencia sobre la comparación que el encargo pedía.** El encargo mandaba
comparar SIGNO y razón de P2 contra P1 en la misma corrida. Con P2 en
EXISTE-NO-SATISFACE esa comparación **no se hace**, y en particular **no se
compara la cifra de P1 contra el 0.91 ni contra el 0.71** salvo lo que el propio
COMMIT-2 de P1 declare sobre su propia escala. Una pieza que PARA no tumba el lote.

---

## §4 · P3 · `tramite.evasion_norma` — ENCUCI 2020 examinada, **ENVIPE 2025 preferida**

**Lo que la regla pide.** `situacion: enfrenta_norma_percibida_inutil_o_extractiva`;
`disparadores: {sancion_creible: false}`; `contexto_norma: {percibida_util: false}`;
`entonces: evade_norma p=0.66 / cumple_norma p=0.34`.

### (a) ENCUCI 2020 — examinada, **no elegida**

El único reactivo cercano es **`AP5_11`** (5.11 «En su opinión, ¿cuál de las
siguientes frases se acerca más a lo que usted piensa?»): 1 «Las personas deben
obedecer siempre las leyes aunque sean injustas» · 2 «Las personas pueden pedir
que cambien las leyes si estas no les parecen» · **3 «Las personas pueden
desobedecer la ley si esta es injusta»** · 4 Ninguna · 9 NS/NR. Cerca está también
`AP5_10` («¿qué tanto cree que se respetan las leyes en México?»).

- situación / `percibida_util: false` — **EXISTE**, embebida en el propio
  enunciado («si esta es injusta»).
- `sancion_creible: false` — **NO-ENCONTRADO**. Barrido del descriptor completo
  (3 081 líneas no vacías, con control positivo): `sanci` 0 aciertos, `castig` 0,
  `impunidad` 0, `multa` 0. Las baterías 5.4, 5.7, 9.2 y 9.3 se leyeron enteras y
  ninguna toca probabilidad de sanción.
- conducta `evade_norma` — **EXISTE-NO-SATISFACE**. `AP5_11=3` declara que
  desobedecer **es admisible**; no declara que el informante **haya incumplido**.
  El encargo pide «proporción que **declara incumplir**». Permisibilidad no es
  conducta, y tratarlas como la misma cosa infla o desinfla el desenlace sin
  forma de saber en qué dirección.

Queda registrado como el mejor reactivo **actitudinal** disponible, por si mesa
quiere una pieza de actitud; este acto no lo mide.

### (b) ENVIPE 2025 — **elegida**

El encargo autoriza expresamente ENVIPE «si el censo lo prefiere». Lo prefiere,
por cuatro razones que se sostienen en el dato:

| componente | ítem de ENVIPE 2025 | veredicto |
|---|---|---|
| situación — *enfrenta* la norma | ser víctima de un delito, y con ello enfrentar la norma de denunciar ante el Ministerio Público (tabla `tmod_vic_envipe2025`, unidad = **delito**) | **EXISTE** — y es un «enfrenta» real, no hipotético |
| `contexto_norma: {percibida_util: false}` | **`BP1_23`** «¿Cuál fue la razón principal por la que no denunció…?»: 04 **pérdida de tiempo** · 05 **trámites largos y difíciles** · 06 **desconfianza en la autoridad** · 08 **actitud hostil de la autoridad** (además de 01 miedo al agresor, 02 miedo a que lo extorsionaran, 03 delito de poca importancia, 07 no tenía pruebas, 09 otra, 99 NS/NR) | **EXISTE** — el informante nombra la inutilidad o el carácter extractivo de la norma con sus propias palabras |
| conducta `evade_norma` | **`BP1_20`** «¿Acudió ante el Ministerio Público o Fiscalía Estatal a denunciar el delito?» (1 Sí / 2 No) | **EXISTE y es conductual**, no actitudinal |
| `sancion_creible: false` | ningún ítem | **se cumple estructuralmente**: en México no existe sanción por no denunciar un delito del que se fue víctima. Es premisa jurídica externa, declarada como juicio del acto — **no** una medición de ENVIPE |

**Veredicto: EXISTE-SATISFACE. Pasa a medición en ENVIPE 2025.**

**La `n` alcanza** (denominadores, sin cruzar contra `BP1_23`): `tmod_vic` tiene
**40 280 delitos**; `BP1_20` está completo (4 110 denunciaron, 36 170 no);
`BP1_23` es no-blanco en 36 040 y **solo** entre los `BP1_20=2` (los 4 110 que
denunciaron lo tienen en blanco, y 130 no-denunciantes también) — el gate del
cuestionario es el esperado y se verificó por cruce de validez, no por supuesto.
Ponderador `FAC_DEL`, con `EST_DIS` y `UPM_DIS` presentes.

**Límite que la spec debe declarar y que no se puede esquivar.** `BP1_23` solo se
pregunta a quien **no** denunció. Por tanto la percepción de inutilidad de la
norma se observa **únicamente entre los evasores**, y la condicional exacta de la
regla —P(evade | enfrenta ∧ norma percibida inútil ∧ sin sanción)— **no es
estimable**. Lo estimable es la conjunta P(evade ∧ norma percibida inútil |
enfrenta la norma), que es lo que el encargo pide con «proporción que declara
incumplir una norma percibida como inútil». El COMMIT-1 de P3 congela esa lectura
explícitamente; no se reportará como si fuera la condicional.

---

## §5 · P4 · `dinero.ahorro.tiene_ahorros` — ENIF 2024 (re-medición)

**Firma de mesa DS1 (2/sep) autoriza la re-medición.** No es un prior ASIGNADO
contra dato: es re-medir una regla ya MEDIDA.

**Veredicto: EXISTE-SATISFACE.** ENIF 2024 tiene **sección 5 · AHORRO INFORMAL Y
FORMAL** completa:

- **informal `P5_1_1..P5_1_6`** («en los últimos 12 meses, de junio de 2023 a la
  fecha, ¿usted…»): 1 ahorró prestando dinero · 2 ahorró comprando animales o
  bienes · 3 guardó en caja de ahorro del trabajo o de conocidos · 4 guardó con
  familiares o conocidos · 5 participó en una tanda · 6 guardó dinero en su casa.
- **formal `P5_6_1..P5_6_9`** («de junio de 2023 a la fecha, ¿usted guardó o
  ahorró en su…»): 1 cuenta/tarjeta de nómina · 2 de pensión · 3 para apoyos de
  gobierno · 4 cuenta de ahorro · 5 cuenta de cheques · 6 depósito a plazo fijo ·
  7 fondo de inversión · 8 cuenta contratada por Internet o aplicación no
  bancaria · 9 otro tipo de cuenta.

**La `n` alcanza y el universo es el que el encargo pide:** `TMODULO.csv` tiene
**13 502 personas elegidas**, `EDAD_V` de **18 a 98** (es decir, adultos 18+, no
un rango truncado), las 15 variables de sección 5 no-blancas en **las 13 502**,
población expandida por `FAC_PER` = **94 221 441**, con `EST_DIS` y `UPM_DIS`.

**Dos no-comparabilidades con la cifra de 2005-06, que se declaran ahora y que la
spec de P4 congela.** La regla vigente vale p=0.174804 sobre ENNViH ola 2. Esa
cifra y la de 2024 **no forman una serie temporal**:

1. **Acervo contra flujo.** La medición de 2005-06 usa `cr27` = «¿Tiene
   ahorros?», un **acervo** al momento de la entrevista (1=Sí / 3=No, según
   `forense/notas/2026-08-24-cal-g3-puntual-cierre.md:38`). ENIF 2024 pregunta si
   **ahorró o guardó en los últimos 12 meses**: un **flujo**. Son cantidades
   distintas y no hay razón para que coincidan aunque nada hubiera cambiado.
2. **Universo.** La propia nota de cierre de 2005-06 dice de su universo, textual:
   «No es "México", no es "los adultos de México": es la intersección de
   panel-retenido × módulo-aplicable × respuesta-sustantiva en ambas mediciones»
   (n=6 028 con ponderador `fac_3b`). ENIF 2024 es una muestra nacional de
   adultos 18+. Comparar las dos como si midieran la misma población sería
   precisamente el error que esa nota se adelantó a marcar.

Por eso P4 entra **como enmienda de re-medición con ola declarada**, conservando
la entrada de 2005-06, y **sin** leer la diferencia entre ambas como cambio en el
tiempo. Si la diferencia excede el doble o la mitad, eso **no** dispara por sí
solo `REFUTADA-POR-DATO`: dos definiciones distintas sobre dos universos distintos
no se refutan entre sí. La spec de P4 lo dirá con esas palabras.

**Reactivo alterno examinado y descartado como principal:** `P4_10` («si dejara de
recibir ingresos, ¿por cuánto tiempo podría cubrir sus gastos con sus ahorros?»)
es el análogo de **acervo** más cercano a `cr27`, pero su código 1 fusiona «menos
de una semana» con «no tiene ahorros», así que no separa limpiamente tener de no
tener. Se registra por si mesa quiere la serie de acervo; el encargo fija
«formal ∪ informal», y eso es lo que P4 medirá.

---

## §6 · Resumen, contador y qué pasa a medición

| pieza | regla | fuente | veredicto del censo | ¿mide? |
|---|---|---|---|---|
| P1 | `tramite.gobierno_digital.util_sin_coercion` | ENCIG 2025 | **EXISTE-SATISFACE con mapeo declarado** | **sí** |
| P2 | `tramite.gobierno_digital.coercitivo` | ENCIG 2025 | **EXISTE-NO-SATISFACE** (sin ítem de obligatoriedad; rechazo ≠ no-conclusión; `cobertura_formal: false` selecciona fuera del universo) | **no** |
| P3 | `tramite.evasion_norma` | ENVIPE 2025 (ENCUCI 2020 examinada y no elegida) | **EXISTE-SATISFACE** | **sí** |
| P4 | `dinero.ahorro.tiene_ahorros` | ENIF 2024 | **EXISTE-SATISFACE** (re-medición, con dos no-comparabilidades declaradas) | **sí** |

**CONTADOR real que este acto puede alcanzar:** priors ASIGNADO con dato
**+2 de 3** (P1 y P3; P2 queda sin dato por defecto de la fuente, no del acto) ·
re-mediciones **+1** (P4). Se declara el real, no el máximo del encargo.

**Prohibiciones que este censo hereda al resto del acto.** No se carga nada al
motor: las entradas nuevas viven solo en `milpa/tramite-ola5-propuesta-v0.yaml`
con tier `PENDIENTE-DE-MESA`. No se toca `milpa/tramite.yaml` ni
`forense/prereg-duelo-v2/`. Las corridas M/L no se leen: este acto es CIEGO a
ellas y su única lectura de `codificacion-R-v1_0.tsv` fue la fila `TRA-M-13` para
heredar el hallazgo de duplicados de `sec_7`, que es marco, no corrida.
