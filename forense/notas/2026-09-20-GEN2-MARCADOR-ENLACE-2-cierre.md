# ACTO GEN2-MARCADOR-ENLACE-2 · CIERRE — el marcador ya se enteró: 6 celdas ganan piso (`sin_piso` 21 → 15) y 174 de 206 emisiones ganan su IC95 sellado; las 4 filas EDER siguen esperando una decisión de vocabulario de mesa

Encargo archivado por A.3 (0-bis): `forense/encargos/2026-09-20-GEN2-MARCADOR-ENLACE-2.md`
(sha256 `453ae0e89a7c958e1231dd42814be10ece95e43e2c0530b4506f1c788edd1628`).

## 0 · Arranque, compuerta, entorno

- **ENTORNO = NUBE**, el que el encargo asigna. Firma de tres partes (A.2):
  `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE = cloud_default` · sonda `curl` a
  `https://www.inegi.org.mx/` → `CONNECT tunnel failed, response 403`,
  `http_code=000` (DENEGADA-POR-POLÍTICA) · corpus **NO montado**:
  `ls data/raw` → `No such file or directory`, **archivos examinados = 0**
  (A.13). No es PARO: este acto no abre ningún microdato — todo insumo es un
  RESULT ya sellado. Ninguna cifra sale del espejo (§2): todas se derivan en
  esta sesión por comando, sobre el clon.
- **REPO**: `/home/user/Modelado-Mexicano`, rama `claude/pensive-keller-7wxjod`,
  `git status` limpio al abrir.
- **SHA**: `git fetch origin main` → `origin/main = 8b7b056`, **idéntico** al
  SHA de redacción `8b7b0562`. No hubo que re-derivar por movimiento de main.
- **COMPUERTA cumplida, verificada por producto** en el historial de
  `origin/main`, no por memoria: `436d17a` (`Merge pull request #916`),
  `be53e6f` (`Merge pull request #915`) y `1f4468b` (que declara la
  renumeración por `#910, #911, #912`) están todos en `origin/main`.
- `tools/corrida0.py` **no se tocó** (corre `#922` en paralelo): confirmado en
  el diff del PR.

## 1 · P1 · Por qué paró `#915`, y qué se resolvió

La nota de `#915` §3 nombra cuatro causas, y las cuatro estaban fuera de «una
línea». Se resolvieron las cuatro, y sólo esas:

| causa de `#915` §3 | resolución |
|---|---|
| (1) `indice_identidad()` indexa con `setdefault`: las 4 filas `NO-CONSTRUIBLE` de la rejilla ganan por orden de lectura | `TABLAS_IDENTIDAD`, lista única en orden cronológico de sello; el índice asigna en vez de `setdefault`, así que **manda la más reciente**. `sucesiones_identidad()` nombra a la sucedida y `colisiones_dentro_de_una_tabla()` separa el caso que sí es defecto (clave repetida **dentro** de una tabla, donde ningún orden desempata) — hoy **0**. |
| (2) `MAPA_CONSUMER` no tiene `dinero.ahorro.horizonte_corto_ejes_enif2024` | entrada explícita, citando `yaml:2159` y las filas 6-7 de la tabla, como las demás. |
| (3) `CALC_PISOS_SELLADOS` no lista el CALC nuevo | `CALC-PISOS-ENIF2021-FORMALIDAD-0001` añadido. Sigue **por nombre**, nunca por glob, y el cinturón contra `CALC_PISOS_VETADOS` no se tocó (`T-VETO-POR-NOMBRE` verde). |
| (4) la guardia 3 de `T-ENLACE-BIYECTIVO` exige que la causa `P3_13 comparable no existe en ENIF 2021` siga apareciendo en alguna fila SIN-PISO | acotada a las `NO-CONSTRUIBLE` **VIGENTES**. Una fila que una tabla más reciente sucede ya no gobierna su celda, y exigir su causa obligaría al marcador a transportar una causa que `#908` refutó por texto y `#915` refutó sobre el dato. **La fila sucedida no se edita ni se borra** (A.10): sigue sellada en la tabla de la rejilla y el marcador la nombra. |

**Ninguna tabla de identidad se escribió** (perímetro). Las 4 sucesiones, derivadas:

```
EXCLUSION-PISOS-ENIF2021-AHORRA-SOLO-INFORMAL-FORMALIDAD-{SIN,CON}-SEGURIDAD-SOCIAL
EXCLUSION-PISOS-ENIF2021-INFORMAL-CUALQUIERA-FORMALIDAD-{SIN,CON}-SEGURIDAD-SOCIAL
  → RESULT-PISOS-ENIF2021-FORMALIDAD-{D9,INFORMAL-CUALQUIERA}-FORMALIDAD-{SIN,CON}-SEGURIDAD-SOCIAL-P
```

y cada celda gobernada por una sucesora lo **dice** en `piso_fuente`
(`… · SUCEDE-A:<cell_id sucedido>`), probado por `T-PRECEDENCIA`.

## 2 · P2 · ENUT y EDER

- **ENUT 2019 · 11 celdas: `#908` ya lo hizo.** El marcador muestra
  `NO-CONSTRUIBLE:ENUT 2019 sin tvar_crea; horas_cuidado 2024 (*_CON_CP) incluye
  cuidados emocionales y esperas sin otra actividad que 2019 no pregunta, exige
  presencia en el cuidado pasivo y separa 0-5 de 6-14 donde 2019 anida 0-5 en
  0-14` en las 11, **no** `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD`. Una línea y sigue.
- **EDER 2017 · 4 celdas: `#908` NO lo hizo, y lo declaró.** Siguen
  `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD`. El dictamen de `#908` §2.2 dice por qué,
  verbatim: «La tabla de identidad de este acto **no** escribe filas para EDER
  (no es ENUT 2019 y el estado `SIN-PISO-POR-DISEÑO` no existe en el vocabulario
  `status` de la tabla de la rejilla; inventarlo aquí sería escribir fuera del
  perímetro) … salvo que mesa quiera que el marcador distinga
  `SIN-PISO-POR-DISEÑO` de `SIN-CONSUMER` — **decisión de vocabulario, de mesa**».
  Ese perímetro es también el de este acto («No toca … ninguna tabla de
  identidad»), así que el estado no cambia: **`NC-0404`, `DECISIÓN-DE-MESA-PENDIENTE`**.
  No es un enlace roto — es ausencia de fuente, y el marcador la rotula como tal.

## 3 · P3 · IC de las emisiones

`ic_de_emisiones()` (en `tools/marcador_segmento.py`, dentro del perímetro) lee
los dos CALC por **identidad exacta de celda**: el sufijo del `resultado_id` de
la emisión (`RESULT-C2COMP-<sufijo>`) es el mismo sufijo del CALC. Las dos
plantillas de id difieren y cada una se declara citando la spec de su CALC —
no se inventó una regla común:

| CALC | plantilla | cita |
|---|---|---|
| `CALC-C2-COMPUESTO-IC-ENIF2024-0001` (`#911`) | `RESULT-C2IC-ENIF2024-{suf}-{campo}` | `spec.md:86` |
| `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001` (`#916`) | `RESULT-C2IC25-{campo}-{suf}` | `spec.md:103` |

Los sufijos se **desarman con la misma plantilla que los arma**, no con recortes
a mano. Guardas: si un CALC declara `IC-ESTADO` y no es el bootstrap réplica por
réplica, la celda **no entra** (conserva `NO-PROPAGADA`); si dos CALC reclamaran
la misma celda, no se elige uno — sale `COLISION:` y `NO-PROPAGADA`. Hoy: 0
colisiones, y los 136 `IC-ESTADO` de ENIF son todos el bootstrap (ENVIPE no
sella ese campo, y el campo es opcional).

**Cobertura derivada, no tecleada:** 174 de 206 emisiones. Las **32** restantes
son exactamente las de `tramite.gobierno_digital.util_sin_coercion_ejes_encig2025`
— ENCIG 2025 no tiene CALC de IC — y conservan `ic95_inf`/`ic95_sup` vacíos y
`NO-PROPAGADA-COVARIANZA-NO-SELLADA`. (El CALC de ENIF selló 196 celdas; 174−38 =
136 corresponden a emisiones y las otras 60 no son emisiones: no se consumen.)

Esto **ejecuta el inciso (2) de `FP-397`**, que pedía literalmente «autorizar el
sucesor de nube (una línea) que haga que el lector del marcador tome el IC sellado
de este CALC para las 38 emisiones de ENVIPE 2025». Su inciso (1) (`cuenta_gen2`)
**sigue ABIERTA** y este acto no lo toca. Cierra también los sucesores
«no actualiza el marcador» de `#911` y `#916` (`NC-0388`).

**Lo que este acto NO hizo a la guardia.** `GuardiaD14` sigue entera: una emitida
no sale por la vía por defecto y no cuenta como `ADOPTADO_ACTIVO` — los dos casos
que el encargo nombra están **sin editar** y verdes. El caso vecino
`test_una_emitida_nunca_trae_IC` sí se sustituyó, y se declara aquí porque el
archivo no está en la lista del perímetro: fue escrito cuando **ningún** CALC había
sellado el IC de una emisión compuesta, y entonces «nunca trae IC» y «nunca
**fabrica** IC» eran la misma frase; desde `#911`/`#916` ya no lo son, y exigir el
campo vacío obligaría al marcador a esconder una medición que el repo ya selló.
Se reemplazó por `test_una_emitida_nunca_FABRICA_IC`, que prueba lo mismo **contra
los RESULT sellados** (el IC presente es exactamente el del CALC y nombra su
`ic95_fuente`; el ausente va con `NO-PROPAGADA`; el rango diagnóstico nunca se deja
leer como IC) — estrictamente más fuerte que probarlo contra la cadena vacía. Si
mesa lo considera fuera de perímetro, la pieza que se revierte es esa sola función;
el resto del acto no depende de ella. **`NC-0405`.**

**Frase obligatoria del encargo, y no es retórica:** *un IC estrecho sobre un C2
compuesto mide el ruido muestral de un estimador que **supone** no-interacción; no
mide el error de ese supuesto.* Esa es justamente la evaluación que falta, y por eso
las 174 siguen `EMITIDA-SIN-EVALUAR`, su cruce sigue `RESERVADA`, y la vía por
defecto del lector sigue sin devolverlas. Leer estas 206 como «206 estimaciones con
IC» sería el error que toda la separación estructural (clave aparte en el YAML,
espacio de nombres de id propio) existe para impedir.

## 4 · P4 · Contadores, antes → después, cada uno con su denominador

Todo derivado en esta sesión por comando (`python3 tools/marcador_segmento.py
--json` antes; `--escribe` después), no tecleado:

| contador | antes | después | denominador |
|---|---|---|---|
| `sin_piso` | **21** | **15** | 74 celdas MARGINALES del universo (i) (7 reglas `_ejes_`, 24 ejes) |
| `cobertura_de_piso` | **73** | **79** | 94 filas que pueden tener piso = 74 MARGINALES + 20 CRUCE piloteadas |
| filas MARGINAL con piso real | 53 | **59** | 74 MARGINALES — y **59 = las 59 filas `CONSTRUIBLE` de las tres tablas**: biyección, no coincidencia (`T-ENLACE-BIYECTIVO`) |
| emisiones con `tipo_incertidumbre = IC95-BOOTSTRAP-…` | **0** | **174** | 206 emisiones `EMITIDA-SIN-EVALUAR` |
| emisiones `NO-PROPAGADA-COVARIANZA-NO-SELLADA` | 206 | **32** | 206 — las 32 son ENCIG 2025 |
| **`estimador_adoptado` (`adoptados_activos`)** | **20** | **20** | 20 celdas C2 piloteadas — **no se movió**, como el encargo exige |
| `evaluadas` · `valor_anadido` · `total_filas` | 20 · 0 · 214 | 20 · 0 · 214 | sin cambio |

Desglose del `sin_piso` que queda (15 de 74): **11** ENUT 2019 con su causa de
`#908` · **4** EDER 2017 `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD` (`NC-0404`, arriba).
El diff del TSV derivado son **6 filas** y nada más.

**Dos celdas salen `NO-COMPARABLE`, y es correcto que salgan así.** Las de
`horizonte_corto × formalidad` ganan su piso sellado, pero el marcador las rotula
`UNIDAD-DISCREPANTE:tabla=PERSONA ELEGIDA 18+/marcador=persona`: el `payload` del
árbitro para esa regla declara `unidad = PERSONA` a secas
(`tramite-ola5-propuesta-v0.yaml:2163`) mientras su propio `universo` dice «18+
elegidas» (`:2164`) y la tabla sellada de `#915` dice `PERSONA ELEGIDA 18+`. Por
A-bis 3-4 no se equiparan dos escalas sin enlace: se rotula y no se tira. **El
yaml del árbitro está fuera de perímetro y no se editó** — `NC-0406`. Por eso
`cobertura_de_piso` sube 6 (las 6 tienen piso) y los estados son 4 `SOLO-PISO` +
2 `NO-COMPARABLE`.

## 5 · Módulo de auditoría (§5) — ¿cuántos contadores movió este trabajo?

**Seis celdas y 174 emisiones; ninguna cifra nueva.** Este acto no midió nada: no
abrió microdato, no selló ninguna corrida, no tocó ningún CALC. Movió lo que un
lector del marcador **ve** de mediciones que el repo ya tenía selladas y que tres
actos anteriores habían dejado invisibles. `cuenta_gen2` = **NO-APLICA**;
adopciones = **0**.

Sobre México, con la cautela de §3: los pisos nuevos dicen que en ENIF **2021**,
entre quien trabaja, «sin seguridad social» ahorra por vía informal **exclusiva**
más que «con seguridad social» (0.441 vs 0.345) y con horizonte más corto (0.349 vs
0.207), pero ahorra por vía informal *cualquiera* **menos** (0.563 vs 0.621) — el
signo cambia entre desenlaces, así que «los informales ahorran en tandas» no se
sostiene ni como resumen. Es **acceso** y un proxy de seguridad social, no cultura;
2021 es dato de pandemia; y un piso **no identifica nada**: acota a los retadores
(§4.6). Evidencia clase (a), datos primarios en México, universo «personas elegidas
18+ que trabajan» — no la población. Peligroso leído simplista: tomar estos seis
puntos, o las 174 emisiones con IC, como estimaciones adoptadas del motor. No lo son,
y el aparato lo impide por construcción.

## 6 · Suite y perímetro

- `python3 tests/test_marcador_segmento.py` → **PASA — 12 casos** (10 previos + `T-PRECEDENCIA` + `T-CONTRATO-TABLAS`).
- `python3 tests/test_estimadores_segmento.py` → **PASA — 3 casos** (sin editar).
- `python3 -m unittest tests.test_c2_compuesto` → **OK, 30 tests**.
- `python3 tests/check.py --baseline` → **LÍNEA BASE: VERDE** — sin FAIL nuevos
  frente a `tests/baseline.json`. 3 FAIL heredados (`T06`, `T08`), 4 WARN nuevos,
  todos `T03` sobre archivos ajenos a este diff (`2026-09-20-GEN2-RECIBO-CODEX-6.md`,
  `hallazgos.md`, `nota-arnes-sesion-claude-md.md`). D-16: los WARN son estado y no
  adjudican; esta cabecera no aserta ningún total de WARN.

Archivos escritos: `tools/marcador_segmento.py` · `milpa/src/estimadores_segmento.py`
(sólo docstring) · `milpa/estimadores-por-segmento.yaml` y
`data/corrida0/marcador-segmento.tsv` (derivados) · `tests/test_marcador_segmento.py`
· `tests/test_c2_compuesto.py` (declarado en §3) · `data/INFRAESTRUCTURA-v1_0.md` ·
cascada. **No tocados:** ningún CALC, ninguna tabla de identidad, `tools/corrida0.py`,
`milpa/tramite-ola5-propuesta-v0.yaml`, las celdas-D, el par del piloto 3.

## NO-CORRIDO / RESERVAS

- **`NC-0404`** · `DECISIÓN-DE-MESA-PENDIENTE` — las 4 celdas de
  `familia.union.libre_ejes_eder2017 × cohorte_nacimiento` siguen
  `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD` en vez de `SIN-PISO-POR-DISEÑO`. Requiere
  vocabulario nuevo en el `status` de una tabla de identidad, que este perímetro
  excluye. Impacto: el marcador no distingue «nadie midió» de «el diseño no admite
  piso». Sucesor: decisión de vocabulario de mesa + acto que escriba la tabla.
- **`NC-0405`** · `FUERA-DE-PERÍMETRO` — `tests/test_c2_compuesto.py` no está en la
  lista del encargo y se editó una función (`test_una_emitida_nunca_trae_IC` →
  `test_una_emitida_nunca_FABRICA_IC`). Sin ese cambio, P3 no puede cerrar con la
  suite verde, porque ese caso asertaba la ausencia del IC que P3 existe para traer.
  Se sustituyó por una prueba más fuerte, no más débil. Impacto: si mesa lo veta, se
  revierte esa sola función y P3 vuelve a PARO. Sucesor: veto o ratificación de mesa.
- **`NC-0406`** · `FUERA-DE-PERÍMETRO` — `dinero.ahorro.horizonte_corto_ejes_enif2024`
  declara `unidad = PERSONA` en su `payload` mientras su `universo` dice «18+
  elegidas» y la tabla sellada dice `PERSONA ELEGIDA 18+`; sus 2 celdas salen
  `NO-COMPARABLE`. El yaml del árbitro está excluido del perímetro. Impacto: 2 celdas
  con piso sellado que no comparan contra su R. Sucesor: acto que corrija el `payload`
  del árbitro, o que declare que `PERSONA` y `PERSONA ELEGIDA 18+` son la misma escala.
- **`NC-0407`** · `FUERA-DE-PERÍMETRO` — el error de persistencia de las 6 celdas
  nuevas no se mide («LO QUE NO HACE» del encargo). `CALC-PISO-PERSISTENCIA-ERROR-0001`
  cubre 53 celdas (las `CONSTRUIBLE` de la rejilla) y no estas 6, así que salen sin
  `error_piso_pp` ni `clase_persistencia`. Impacto: 4 filas `SOLO-PISO` sin clase.
  Sucesor: CALC nuevo, nube.

## CONSUMIDO

`ACTO GEN2-MARCADOR-ENLACE-2`, rama `claude/pensive-keller-7wxjod`. Encargo
`forense/encargos/2026-09-20-GEN2-MARCADOR-ENLACE-2.md` marcado CONSUMIDO.
`FP-397` inciso (2) **EJECUTADO**; su inciso (1) sigue ABIERTA.
