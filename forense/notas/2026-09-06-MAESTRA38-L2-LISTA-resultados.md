# `ACTO MAESTRA38-L2-LISTA` · MPS-2012, experimento de lista de PRIMERA MANO — resultados

**6 de septiembre de 2026** · caja (Ubuntu, corpus montado) · rama `acto/maestra38-l2-lista` · base `origin/main = b0c2a80`

Ejecuta **`prereg-caja-S10-L2-LISTA`** (`forense/prereg-caja/S10-L2-LISTA-spec-v1_0.md`, blob `260847ff`, sellada por `ADR-347`, `ACTO MAESTRA38-N15`) sobre `data/mexico.tab` del paquete R `list`. **La spec no se editó.** Medidor: `tools/medidor_l2lista_mps2012.py`. Salida cruda: `data/l2lista-resultados-v1_0.json`.

---

## 0 · Procedencia, verificada byte a byte

| | declarado por S10 §1 | medido hoy | |
|---|---|---|---|
| commit del repo | `e088e5f…` | `e088e5f88af5f3d3f7d61dcffe6d7eb6d28c5120` | **coincide** |
| `sha256` de `data/mexico.tab` | `fe1014…c04488` | `fe101499b591d90d9e2122f439e26306fcdeab443e42d14f9455e9efa1c04488` | **coincide** |

`git clone --depth 1 https://github.com/SensitiveQuestions/list`, fuera del sandbox, a `descargas_mx/ACADEMICO-list-cran/`. **No hay divergencia: A.7 no se dispara.** Registrado en `data/manifiesto.yaml` como `list_cran_mexico_tab` (78 065 B) y `list_cran_mexico_rd` (3 592 B), ambos `--verifica` → **COINCIDE**; manifiesto 1 515 → 1 517. Fila hermana (no fusión) en `data/curacion-registro/aliases-fuentes.tsv`, 19 → 20 filas — la firma A.7 de mesa sobre esa decisión se pide en **`FP-317`**.

## 1 · P0 — lo que el archivo real dice, antes de calcular nada

- **`n` = 1 004**, igual al pre-registrado (S10 §1). **25 columnas** nombradas.
- **Defecto de lectura que la cabecera esconde, resuelto antes de medir:** la cabecera trae **25** nombres y cada fila trae **26** campos. El campo 0 son los **rownames de R** (únicos, 5–1 150, no consecutivos — consistente con «1 004 de ~1 555» de S10 §1), no una variable. Leer el archivo alineando cabecera con campos desde el índice 0 desplaza **todas** las columnas una posición y produce cifras que parecen razonables: control positivo de que la alineación elegida es la correcta → `mex.age2` = `mex.age`² en todo el rango (1.8²=3.24 … 9.0²=81.0), y los 25 rangos caen dentro de lo que declara `man/mexico.Rd`.
- **`y` de `man/mexico.Rd` NO existe en `data/mexico.tab`.** El `.Rd` documenta 26 variables e incluye `y` = *"the number of items that make respondents angry"* — glosa arrastrada de otro dataset del mismo paquete. El conteo de lista de México es **`mex.y.all`** (*"the number of activities that respondent did"*, 0–4), que es el que corresponde al wording de cuatro actividades del propio `.Rd`. **Se declara: el descriptor y el dato no concuerdan en este punto**, y la elección se hace por el wording, no por el nombre.
- Segunda divergencia descriptor/dato, declarada aunque no se use: `mex.cleanelections` se documenta como indicador 0–1 y el dato real va **0–4**. No entra en ningún estimando de S10 §2.
- `mex.vote` tiene 4 `NA`; ninguna variable usada en §2 tiene faltantes.

## 2 · S10 §4 — condición de entrada, CUMPLIDA por texto y por mecánica

- **Por texto** (`man/mexico.Rd`): la lista de cuatro actividades, con *"item c. is presented only to the treatment group, and the control list only contains the other three items"*, y el ítem c es **"Exchange your vote for a gift, favor, or access to a service"** — venta del voto.
- **Por mecánica** (el dato, no la prosa): `max(mex.y.all | control) = 3` y `max(mex.y.all | tratamiento) = 4`. Lista tratamiento = lista control + **un** ítem.

**No se dispara `PROPUESTA-REFUTADA-POR-DISEÑO`.**

## 3 · Estimandos (S10 §2) — proporciones 0–1, SIN PONDERAR

IC95: analítico para §2.1 (diferencia de medias, varianzas desiguales) y §2.2 (Wilson binomial); **bootstrap no paramétrico percentil, B=10 000, semilla 20260906** para §2.3, §2.4 y §2.5 — el contraste lista−directa usa las **mismas filas** en sus dos términos, así que una fórmula de independencia sobreestimaría su IC.

| Estimando | Estimación | IC95 | IC95 incluye 0 |
|---|---|---|---|
| §2.1 Prevalencia por lista (T−C) | 0.1874 | [0.0797, 0.2950] | no |
| §2.2 Prevalencia directa (`mex.direct`) | 0.0568 | [0.0441, 0.0728] | no |
| §2.3 Contraste lista − directa | 0.1306 | [0.0216, 0.2375] | **NO** |

| Estrato | n | §2.1 lista | IC95 (bootstrap) | §2.2 directa | §2.3 contraste | IC95 | incluye 0 |
|---|---|---|---|---|---|---|---|
| `mex.wealth` — bajo (<=mediana) | 513 | 0.1737 | [0.0282, 0.3241] | 0.0565 | 0.1171 | [-0.0312, 0.2674] | sí |
| `mex.wealth` — alto (>mediana) | 491 | 0.2173 | [0.0658, 0.3728] | 0.0570 | 0.1603 | [0.0070, 0.3143] | **no** |
| `mex.urban` — rural (0) | 278 | 0.0605 | [-0.1333, 0.2512] | 0.0576 | 0.0030 | [-0.1920, 0.1945] | sí |
| `mex.urban` — urbano (1) | 726 | 0.2397 | [0.1112, 0.3672] | 0.0565 | 0.1832 | [0.0552, 0.3089] | **no** |
| `mex.loyal` — no leal (0) | 632 | 0.2059 | [0.0717, 0.3439] | 0.0633 | 0.1426 | [0.0082, 0.2806] | **no** |
| `mex.loyal` — leal (1) | 372 | 0.1561 | [-0.0180, 0.3328] | 0.0457 | 0.1104 | [-0.0635, 0.2868] | sí |

| `mex.votecard` | n | «sí» directa | tasa | IC95 |
|---|---|---|---|---|
| 1 — voto verificado por encuestador | 614 | 31 | 0.0505 | [0.0358, 0.0708] |
| 0 — no verificado | 390 | 26 | 0.0667 | [0.0459, 0.0959] |
| **diferencia (1−0)** | | | -0.0162 | [-0.0471, 0.0132] |

n tratamiento = 508, n control = 496; medias del conteo 1.7559 (T) vs 1.5685 (C). Directa: 57 «sí» de 1 004.

## 4 · Fila B-bis (S10 §3) — NO se dispara

La rama de S10 §3 está escrita para el caso en que **la lista no supere a la directa**. **Ese no es el caso aquí**: la prevalencia por lista (0.1874) más que **triplica** la directa (0.0568), y el contraste es **+0.1306 con IC95 [0.0216, 0.2375] que excluye 0**. En puntos porcentuales (sólo en prosa, S10 §5): 18.7% frente a 5.7%, brecha de **+13.1 pp**.

Lectura, acotada a lo que este instrumento soporta: en este subconjunto el diseño de lista **sí** detecta subreporte adicional respecto de la pregunta directa. No se afirma nada sobre la magnitud poblacional — el universo es restringido (1 004 de ~1 555), sin ponderar, y el semiancho del IC95 del contraste es 0.1080, ancho.

**Heterogeneidad — dónde vive la brecha.** El contraste excluye 0 en **urbano** (+0.1832), en **riqueza alta** (+0.1603) y en **no leales** (+0.1426); incluye 0 en **rural** (+0.0030, prácticamente nulo), riqueza baja y leales. El estrato rural es el más informativo por contraste: con n=278 la lista y la directa dan **lo mismo**. No se decide entre «no hay subreporte en el campo rural» y «no hay potencia con n=278» — los dos son compatibles con este IC, y S10 §3 (b) advierte exactamente eso.

**§2.5 NO es `SIN-INSTRUMENTO`.** El dataset **sí** trae un indicador de participación distinto de la autodeclaración: `mex.votecard` es *"respondent's enumerator-verified turnout"*, frente a `mex.vote` *"self-reported turnout"*. La diferencia en la tasa de «sí» directa entre verificados y no verificados es **−0.0162, IC95 [−0.0471, 0.0132], incluye 0**: no hay señal.

## 5 · Lo que este acto NO hace

- **No mueve ningún tier del canon.** `R7.3` y `R7.6` no tienen ni una variable en este dataset (S10 §0): `list::mexico` no trae `W2_P39B`, `W2_P40`, `W2_P36C` ni `W2_P8`.
- **No sustituye la rama MEDICIÓN/TEXTO de `S2-L2`** sobre el `.dta` completo y restringido de ICPSR 35024 (`FP-314`/`FP-316`). Cuando ese llegue, su veredicto **reemplaza** a éste (S10 §6), no promedia con él.
- **No toca** `milpa/tramite.yaml`, ni las specs `S1`–`S9`, ni ninguna salida de `MAESTRA36-L12`.
- `MAESTRA38-L2` (la rama que depende del `.dta`) sigue gateado a `A4`. Esto es la rama LISTA, hermana, no su sustituto.

## 6 · Efecto sobre P3 (S10 §6)

**`P3 → MEDIDO (primera mano, subconjunto restringido n=1 004, sin ponderar)`.** Nunca «primera mano, panel completo». Piezas de `MAESTRA36-L12` con dato de primera mano: **0 → 1**.

## 7 · Enmienda a `FP-263`

`FP-263` (iii) pedía *el texto de los ítems* como lo único que convierte P3 de PROPUESTA en medición. Este acto lo obtiene **para esta fuente**: el wording de `man/mexico.Rd` satisface la condición de entrada, y además la mecánica del dato la confirma. **Precisión que no se debe redondear:** el wording verificado es el **inglés de `list::mexico`**, no el español de `P35A`/`P35B`/`W2_P35A`/`W2_P35B` del cuestionario de ICPSR 35024 — mismo estudio, pero que sean los mismos ítems es una inferencia razonable, no algo medido aquí. `FP-263` (i) y (ii) siguen dependiendo del `.dta` completo y no se tocan.

---

## 8 · Opción B (encargo (d)) — Dataverse: **OBTENIDO**, sin medir nada

Los dos DOI que `MAESTRA38-N15 §3` fila B nombraba. **Ningún archivo de estos dos DOI se abrió, se leyó ni se midió en este acto** — se hashearon y se registraron, nada más.

**Alcance declarado, no silenciado:** se aplicó el **protocolo de rutas múltiples** de `/adquiere` §3, pero **no** el resto de la skill: `data/curacion-registro/cola-adquisicion-registro.tsv` y su vista `data/cola-adquisicion-v1_0.tsv` quedaron **fuera del perímetro** de este encargo y no se tocaron. La adquisición está registrada en la capa payload, no en la capa cola.

| Ruta (`/adquiere` §3) | Resultado crudo |
|---|---|
| **(i) URL directa** por archivo, `api/access/datafile/<id>`, UA de navegador real | **HTTP 200 en 16 de 16 intentos**, tamaño descargado = tamaño declarado en todos |
| **(ii) API del portal**, `api/datasets/:persistentId/versions/:latest` | **HTTP 200** en los dos DOI (9 357 B y 11 016 B). Los dos `RELEASED`, licencia **CC0 1.0**, **`restricted: false` en los 17 archivos** |
| **(iii) Formato alterno** | **No aplica**, y se dice por qué: Dataverse sirve el archivo depositado tal cual; no hay conversión alterna publicada para `.rda`/`.tab`/`.R` en estos dos depósitos |
| **(iv) Espejo académico** | **No se necesitó** — Dataverse *es* el repositorio académico de origen (ruta (iv) del protocolo), y abrió por la ruta (i). No se cierra en `NO-OBTENIDO`: se cierra en **OBTENIDO** |

`NO-OBTENIDO` **no se declara** porque no procede: las rutas abrieron.

**Manifiesto: 1 517 → 1 533 (+16).** `--verifica` sobre los 16: **16 COINCIDE, 0 DISCREPANCIA, 0 AUSENTE**. Raíz `descargas_mx/ACADEMICO-dataverse-mps2012/`.

**Un archivo de 17 no se bajó, y no se disfraza de fallo:** `empirical_models.zip` (`doi:10.7910/DVN/27083`, id 2497899, **527 533 432 B**) es salida de modelos, no microdato. Que la ruta funciona para él está **medido, no supuesto**: `curl -r 0-1023` → **HTTP 206**, 1 024 B servidos. Es una decisión de no bajar 527 MB inútiles para este acto, no un `NO-OBTENIDO`; queda disponible por la misma ruta para quien lo necesite.

Las dos respuestas de la API (`meta-10.7910_DVN_27083.json`, `meta-10.7910_DVN_VOB5JL.json`) quedaron en la misma carpeta como evidencia de la ruta (ii); **no se registraron como payloads** porque no son dato de la fuente sino respuesta generada por esta caminata.

**Qué contienen, según el metadato (no según haberlos abierto):** `DVN/27083` trae `mexico.rda` y `mexicoall.rda` — candidatos a traer más covariables de la ola 2 que las 25 de `list::mexico`, que es exactamente lo que la fila B anticipaba. `DVN/VOB5JL` trae `Mexico TB Paper Data.tab`, `meta analysis data.tab`, `Pentagono PRI Edomex 2017_v1.tab` (9.7 MB) y un cuestionario parcial de la encuesta VB México 2021. **Nada de esto se abrió**: decir qué miden exigiría abrirlos, y este acto no lo hace.

## 9 · Anti-PR#77 — dónde quedaron los payloads

Los 18 payloads de este acto (2 de `list`, 16 de Dataverse) están en **`descargas_mx`**, que es raíz **compartida** declarada en `data/raices.local.yaml`, no en el worktree de esta sesión. `--verifica` los resuelve por el campo `raiz`, no por ruta local.
