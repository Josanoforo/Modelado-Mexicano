# ACTO GEN2-PISOS-ENUT2019-EJES-1 · DICTAMEN P0/P3 — el piso t−1 del reparto de cuidado (ENUT 2019) es NO-CONSTRUIBLE por texto; horizonte_corto × formalidad (ENIF 2021) tiene contraparte bajo otro nemónico; union.libre × cohorte (EDER) es SIN-PISO-POR-DISEÑO

Encargo archivado por A.3: `forense/encargos/2026-09-19-GEN2-PISOS-ENUT2019-EJES-1.md`.
SHA de redacción `a92126f0` = `origin/main` al abrir (delta 0). Entorno CAJA:
`python3 tools/entorno.py --sonda-red` → `commit=a92126f0 · git_status=LIMPIO(0) ·
python=3.14.4 · CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable · red=200 ·
raices=data_raw:SI descargas_mx:SI · corpus=SI(examinados=419)`.

Este documento es el **entregable** del acto (P0, tercer veredicto): «Si es lo
tercero, el entregable es ese dictamen y las 11 celdas salen de SIN-CONSUMER a
NO-CONSTRUIBLE con causa». No congela spec (P1), no corre CALC (P2). Todo lo que
sigue se leyó de **documentación** (FD, diccionarios RNM, descripciones de
archivos); **ningún microdato de ENUT 2019, ENUT 2024, EDER ni ENIF se abrió**
en esta sesión. Declaración ADR-46: la sesión leyó `milpa/tramite-ola5-propuesta-v0.yaml`
(las 11 celdas de ENUT 2024 con sus p, las 4 de EDER 2017, las 2 de ENIF 2024),
`data/corrida0/CALC-ENUT-0001/spec.yaml` completo y las notas de `MAESTRA35-L7`
(P0-censo). No es ciega respecto de ENUT 2024; sí lo es respecto de ENUT 2019
(sólo FD + RNM).

## 0 · Premisas del encargo, verificadas contra `a92126f0`

| premisa | veredicto | comando / evidencia |
|---|---|---|
| `sin_piso: 21` = 17 `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD` + 4 `NO-CONSTRUIBLE` | **CIERTA** | `python3 tools/marcador_segmento.py --json` → `sin_piso=21`; `data/corrida0/marcador-segmento.tsv`: 10 `sexo_edad` + 1 `reparto_hogar` (ENUT) + 4 `cohorte_nacimiento` (EDER) + 2 `formalidad` (ENIF horizonte_corto) = 17 SIN-CONSUMER; 4 `formalidad` (ENIF via_informal) NO-CONSTRUIBLE |
| Gobiernan `tramite-ola5-propuesta-v0.yaml:2089`, `tools/pisos_ejes.py`, `PISOS-REJILLA-arbitro-metadatos-v1_0.tsv` | **CIERTA** | los tres existen; la tabla de rejilla no trae ningún `consumer` ENUT (`grep -c enut` = 0 sobre 57 filas) |
| `ls data/corrida0 \| grep -i ENUT` → 4 CALC, ninguno piso 2019 | **CIERTA** | `CALC-ENUT-0001`, `CALC-ENUT2024-DISTRIBUCION-HORAS-0001/-0002`, `CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001`. `CALC-ENUT-0001/spec.yaml` fija `horas_cuidado = CUID_ESP_INT_HOG_CON_CP + CUID_INT_0A5_CON_CP + CUID_INT_6A14_CON_CP + CUID_INT_60MAS_CON_CP` (tvar_crea.csv) y declara: «ENUT 2019 y 2009 NO entran (sin tabla tvar_crea; reconstruir CON_CP desde ~40 items crudos no tiene precedente validado)» |
| manifiesto: `enut2019_bd_csv`, `enut2019_fd_xlsx`, `enut2019_der_zip`, `enut2019_diccionario_variables_html` presentes | **CIERTA** (los cuatro, sha256 verificados contra `data/raw/`) | `d3da76a0…`, `8577edc8…`, `4cf74d14…`, `3c47a134…` |
| **«¿Existe en 2019 el mismo agregado (enut2019_der_zip)…?»** — el encargo lee `der` como *derivadas* | **PREMISA FALSA, corregida** | `data/manifiesto.yaml:3187-3204`: `enut2019_der_zip` = `enut_2019_diagrama_er.zip`, «ZIP (diagrama entidad-relación ENUT 2019)»; contenido real (zipfile): **un solo miembro, `modelo_er_enut_2019.png`, 176 623 B**. No hay tabla de variables agregadas en ese ZIP ni en ninguno de 2019 |
| «La rejilla de pisos (#871) no cubrió ENUT» | **CIERTA** | `tools/marcador_segmento.py:216-220` lo declara y la tabla lo confirma |
| Compuerta: `GEN2-CELDA-D-PILOTO-3-P0` cerró su rama | **CUMPLIDA (vacua)** | `git ls-remote --heads origin \| grep -i piloto` → 0; `git worktree list \| grep -i piloto-3` → 0; `gh pr list --state open` → 0 PR. `PILOTO-3` cerró por #894 (`## CONSUMIDO` en `origin/main`); su P0 en caja (`NC-0355`, sucesor «Acto en CAJA con corpus montado») **nunca se lanzó** — no hay encargo, rama, worktree ni PR con ese rótulo. Las tres ramas `claude/*` vivas (`RECIBO-CODEX-6`, `RELEVO-TANDA-1`, `TABLERO-SENAL-1`) declaran `ENTORNO: NUBE; NO caja`. Un acto de caja a la vez: se cumple |

## 1 · P0 · Comparabilidad por texto — ENUT 2019 vs ENUT 2024

### 1.1 · Qué es el agregado de 2024 que la regla reusa

`enut2024_fd.xlsx`, hoja `TVAR_CREA` (filas 45-53), etiqueta y **concepto** verbatim:

| nemónico 2024 | pregunta (col. [1]) | concepto (col. [6]) |
|---|---|---|
| `CUID_ESP_INT_HOG_CON_CP` | Cuidados especiales a integrantes del hogar por enfermedad crónica, temporal o discapacidad, con cuidados pasivos | «…**incluye cuidados pasivos y cuidados emocionales**» |
| `CUID_INT_0A5_CON_CP` | Cuidado a integrantes del hogar de 0 a 5 años, con cuidados pasivos | «…**con cuidados pasivos y con cuidados emocionales**» |
| `CUID_INT_6A14_CON_CP` | Cuidado a integrantes del hogar de 6 a 14 años, con cuidados pasivos | «…**con cuidados pasivos y con cuidados emocionales**» |
| `CUID_INT_60MAS_CON_CP` | Cuidado a integrantes del hogar de 60 años y más, con cuidados pasivos | «…**con cuidados pasivos y con cuidados emocionales**» |
| `CUID_INT_15A59` (residuo declarado, fuera de `horas_cuidado`) | Cuidado a integrantes del hogar de 15 a 59 años | «…con cuidados emocionales» |

El FD **no** documenta la fórmula (qué ítems de `TMODULO` suma cada variable ni si topa
en 168 h); sólo el rango (`CUID_INT_0A5_CON_CP` llega a 280 h/semana, luego suma
declaraciones sin tope). El agregado, por su propio concepto, **incluye la clase
«cuidados emocionales»**.

### 1.2 · Qué existe en 2019

`enut2019_bd_csv.zip` (zipfile): `enut_2019/{THOGAR,TMODULO,TSDEM,TVIVIENDA}.csv` +
`enut_2019_indigena/{…}` + `nota_bd_enut_2019.txt`. **No hay `tvar_crea` ni ninguna
tabla de variables creadas.** `enut2019_fd.xlsx` tiene 4 hojas (`TVivienda, THogar,
TSDem, TModulo`); 2024 tiene 5 (la quinta es `TVAR_CREA`). El módulo de cuidado de 2019
vive crudo en `TModulo`, preguntas 6.11–6.15, cada sub-ítem con 4 columnas de tiempo
(`P6_1xA_nn_{1,2,3,4}` = horas/minutos L-V, horas/minutos S-D) — mismo esquema de
captación que 2024.

### 1.3 · Bloques por edad — la primera diferencia estructural

Diccionario RNM (`enut2019_diccionario_variables.html`, catálogo 618, descripción de
`TMODULO`) vs `enut2024_diccionario_variables.html`:

| bloque | ENUT 2019 (RNM, verbatim) | ENUT 2024 (RNM, verbatim) |
|---|---|---|
| 6.11 | Cuidados a personas dependientes por discapacidad, enfermedad crónica o temporal | Cuidados especiales a integrantes del hogar por discapacidad, enfermedad crónica o temporal |
| 6.12 | Cuidado a integrantes del hogar de **0 a 5 años**, no dependientes | Cuidados a integrantes del hogar de **0 a 5 años**, sin cuidados especiales |
| 6.13 | Cuidado a integrantes del hogar de **0 a 14 años**, no dependientes | Cuidados a integrantes del hogar de **6 a 14 años**, sin cuidados especiales |
| 6.14 | 15 a 59 años, no dependientes | 15 a 59 años, sin cuidados especiales |
| 6.15 | 60 años y más, no dependientes | 60 años y más, sin cuidados especiales |

En 2019 el bloque 6.13 cubre **0–14** (los de 0–5 vuelven a entrar: llevar a la
guardería, terapia, tareas, juntas, salud, cuidado pasivo), y 6.12 sólo pregunta tres
actividades físicas del bebé. En 2024, 6.12 y 6.13 son **disjuntos** (0–5 con 12 ítems;
6–14 con 9). Consecuencia: `CUID_INT_0A5` y `CUID_INT_6A14` **no son separables en
2019**; sólo su suma (0–14) tendría contraparte, y sólo en cobertura de edad, no de
ítems (§1.4).

### 1.4 · Actividad por actividad (cita del FD de cada ola: `TModulo`/`TMODULO`, col. [1])

Convención: **=** misma actividad y misma redacción sustantiva; **≈** misma actividad con
redacción distinta o fusionada/partida; **∅** sin contraparte en 2019.

**6.11 · cuidados especiales (dependientes)**

| ENUT 2024 | ENUT 2019 | mapa |
|---|---|---|
| `P6_11_01` dio de comer o ayudó | `P6_11_01` | = |
| `P6_11_02` bañó, aseó, vistió, arregló | `P6_11_02` | = |
| `P6_11_03` cargó, acostó | `P6_11_03` | = |
| `P6_11_04` remedios caseros / alimento especial | `P6_11_04` | = |
| `P6_11_05` medicamentos / síntomas | `P6_11_05` | = |
| `P6_11_06` **sin considerar el traslado y sin hacer otra actividad**, acompañó mientras recibía atención de salud o terapia | `P6_11_06` «llevó, recogió **o esperó** para que recibiera(n) atención de salud … o alguna terapia especial» | ≈ 2019 fusiona traslado+espera+acompañamiento en un ítem; 2024 lo parte en `_06` (acompañar, sin simultaneidad) y `_07` (llevar/recoger) |
| `P6_11_07` llevó o recogió para atención de salud o terapia | `P6_11_06` (parte) | ≈ |
| `P6_11_08` dio terapia o ayudó a ejercicios | `P6_11_07` | = |
| `P6_11_09` **sin considerar el traslado y sin hacer otra actividad**, esperó de clases, trabajo u otro lugar | — (2019 `P6_11_08` sólo «llevó y/o recogió») | **∅** (la espera no se pregunta en 2019 para este bloque) |
| `P6_11_10` llevó o recogió de clases, trabajo u otro lugar | `P6_11_08` | = |
| `P6_11_11` ayudó en tareas de escuela o trabajo | `P6_11_09` | = |
| `P6_11_12` juntas, festivales, apoyo escolar | `P6_11_10` | = |
| `P6_11_13` **sin hacer otra actividad**, dedicó tiempo para jugar, leerle(s), escucharle(s), orientarle(s) o consolarle(s) | — | **∅ · cuidado emocional, nuevo en 2024** |
| `P6_11_14` mientras hacía otra cosa, **le(s) vigiló o estuvo al pendiente de forma presente** | `P6_11_11` «mientras hacía otra cosa, **lo(s) cuidó o estuvo al pendiente**» | ≈ **cuidado pasivo: 2024 exige presencia («de forma presente»); 2019 no** |

**6.12 · 0–5 años**

| ENUT 2024 | ENUT 2019 | mapa |
|---|---|---|
| `P6_12_01` dio de comer (amamantó) / beber | `P6_12_1` | = |
| `P6_12_02` bañó, aseó, cambió pañales, vistió | `P6_12_2` | = |
| `P6_12_03` cargó o acostó | `P6_12_3` | = |
| `P6_12_04` **sin hacer otra actividad**, esperó de clase/actividad/taller | — | **∅** |
| `P6_12_05` llevó/recogió de guardería, preescolar, casa de familiares | `P6_13_1` (bloque **0–14**) | ≈ (2019 lo pregunta para 0–14, no separable) |
| `P6_12_06` ayudó en actividades de educación inicial/preescolar | `P6_13_3` «tareas de la escuela» (0–14) | ≈ |
| `P6_12_07` juntas/festivales de educación inicial/preescolar | `P6_13_4` (0–14) | ≈ |
| `P6_12_08` **sin hacer otra actividad**, acompañó en atención de salud | `P6_13_5` «llevó, recogió o esperó para atención de salud» (0–14) | ≈ (fusionado en 2019) |
| `P6_12_09` llevó/recogió para atención de salud | `P6_13_5` (parte) | ≈ |
| `P6_12_10` revisó/dio atención a su salud (pomada, vendaje, ejercicios de terapia) | `P6_13_2` «terapia especial o ejercicios» (0–14) | ≈ |
| `P6_12_11` **sin hacer otra actividad**, jugar, leerle(s), escucharle(s), orientarle(s), consolarle(s) | — | **∅ · cuidado emocional, nuevo** |
| `P6_12_12` mientras hacía otra cosa, vigiló / al pendiente **de forma presente** | `P6_13_6` «lo(s) cuidó o estuvo al pendiente» (0–14) | ≈ **presencia exigida sólo en 2024; y en 2019 el ítem es 0–14** |

**6.13 · 6–14 años (2024) vs 0–14 (2019)**

| ENUT 2024 | ENUT 2019 | mapa |
|---|---|---|
| `P6_13_1` **sin hacer otra actividad**, esperó de clase/taller | — | **∅** |
| `P6_13_2` llevó/recogió de escuela, taller, casa de familiares | `P6_13_1` | ≈ (0–14) |
| `P6_13_3` tareas de la escuela | `P6_13_3` | ≈ (0–14) |
| `P6_13_4` juntas/festivales escuela | `P6_13_4` | ≈ (0–14) |
| `P6_13_5` **sin hacer otra actividad**, acompañó en atención de salud | `P6_13_5` (fusionado) | ≈ |
| `P6_13_6` llevó/recogió para atención de salud | `P6_13_5` (parte) | ≈ |
| `P6_13_7` revisó/dio atención a su salud | `P6_13_2` | ≈ |
| `P6_13_8` **sin hacer otra actividad**, jugar, leerle(s), escucharle(s)… | — | **∅ · cuidado emocional, nuevo** |
| `P6_13_9` vigiló / al pendiente **de forma presente** | `P6_13_6` | ≈ (presencia; 0–14) |

**6.14 · 15–59 (residuo `CUID_INT_15A59`, fuera de `horas_cuidado` en la regla — se
tabula para completar el dictamen, no entra al estimando)**: 2024 tiene 6 ítems
(`_1` computadora/celular =`P6_14_1`; `_2` acompañó salud ≈`P6_14_2` fusionado; `_3`
llevó/recogió salud ≈`P6_14_2`; `_4` esperó **∅**; `_5` llevó/recogió clases/trabajo
=`P6_14_3`; `_6` escucharle(s)/orientarle(s)/consolarle(s) **∅ emocional**). 2019: 3 ítems.

**6.15 · 60 y más**

| ENUT 2024 | ENUT 2019 | mapa |
|---|---|---|
| `P6_15_1` apoyó en computadora/celular/cursos | `P6_15_1` | = |
| `P6_15_2` **sin hacer otra actividad**, acompañó en atención de salud | `P6_15_2` «llevó, recogió o esperó…» | ≈ (fusionado) |
| `P6_15_3` llevó/recogió para atención de salud | `P6_15_2` (parte) | ≈ |
| `P6_15_4` **sin hacer otra actividad**, esperó del trabajo/trámite | — (2019 `P6_15_3` sólo llevó/recogió) | **∅** |
| `P6_15_5` llevó/recogió del trabajo/trámite | `P6_15_3` | = |
| `P6_15_6` **sin hacer otra actividad**, leerle(s), escucharle(s), orientarle(s), consolarle(s) | — | **∅ · cuidado emocional, nuevo** |
| `P6_15_7` vigiló / al pendiente **de forma presente** | `P6_15_4` «cuidó o estuvo al pendiente» | ≈ (presencia exigida sólo en 2024) |

**Periodo de referencia**: idéntico («durante la semana pasada»; L-V y S-D, horas y
minutos; FD de ambas olas, columnas `P6_1xA_nn_{1..4}`). **Universo del módulo**: 12+
en ambas (RNM 2019: «integrantes del hogar de 12 y más años»; 2024: `tvar_crea` 74 053
personas 12+ según el árbitro). **Ponderadores/diseño**: `FAC_PER`/`FAC_HOG`,
`EST_DIS`/`UPM_DIS` existen en ambas olas por FD. Nada de esto rescata el estimando:
la diferencia está en el **contenido** de `horas_cuidado`, no en su captación ni en su
diseño.

### 1.5 · Las cuatro diferencias que fijan el veredicto

1. **Actividades componentes.** El agregado 2024 incluye, por concepto del FD, la clase
   «cuidados emocionales» (`P6_11_13`, `P6_12_11`, `P6_13_8`, `P6_15_6`; también
   `P6_14_6` en el residuo) y las esperas «sin hacer otra actividad» (`P6_11_09`,
   `P6_12_04`, `P6_13_1`, `P6_15_4`). **Ninguna de esas nueve actividades se pregunta
   en 2019.** Una reconstrucción 2019 mide, por construcción, un conjunto de
   actividades más chico que el que la regla sella para 2024.
2. **Tratamiento de simultaneidad.** 2024 califica cinco ítems por bloque con «sin
   considerar el traslado y sin hacer otra actividad» / «sin hacer otra actividad»;
   2019 no califica ninguno. El módulo de auditoría del encargo lo dice: «ENUT mide horas
   declaradas, con simultaneidad: no es tiempo de reloj» — y la regla de simultaneidad
   cambió entre olas.
3. **Cuidado pasivo.** 2019: «mientras hacía otra cosa, lo(s) cuidó o estuvo al
   pendiente». 2024: «mientras hacía otra cosa, le(s) vigiló o estuvo al pendiente **de
   forma presente**». El `CON_CP` de 2024 es cuidado pasivo *con presencia*; el de 2019
   admite pendiente sin presencia. Es exactamente el componente que domina los valores
   > 168 h/semana del agregado (L7 P0-censo §ENUT 2024) — no es un ítem marginal.
4. **Bloques de edad.** 2019 anida 0–5 ⊂ 0–14 (§1.3); `CUID_INT_0A5` y `CUID_INT_6A14`
   no son reconstruibles por separado. Para `horas_cuidado` (que suma ambos) la suma
   0–14 sí tiene cobertura de edad equivalente, pero eso no repara (1)–(3).

A esto se suma un límite **de este acto**, no del instrumento: la fórmula con que INEGI
construye `*_CON_CP` no está en el FD, y el perímetro prohíbe abrir `enut2024*` más allá
del FD, así que ninguna reconstrucción podría **validarse** aquí contra `tvar_crea`
(sumar los ítems de 2024 y comparar). Sin esa validación, un piso 2019 sería una
definición nueva de `horas_cuidado` **no verificada ni en la ola donde sí existe el
agregado** — la clase de riesgo que `feedback_spec_congelada_puede_salir_degenerada` y
el `hallazgo_a15_del_acto` de `CALC-ENUT-0001` documentan.

### 1.6 · Veredicto P0

**NO-CONSTRUIBLE.** Causa, en una línea (la que llevan las 11 filas de la tabla de
identidad):

> `ENUT 2019 sin tvar_crea; horas_cuidado 2024 (*_CON_CP) incluye cuidados emocionales y esperas sin otra actividad que 2019 no pregunta, exige presencia en el cuidado pasivo y separa 0-5 de 6-14 donde 2019 anida 0-5 en 0-14`

No es COMPARABLE-CON-RECONSTRUCCION porque no hay reconstrucción que **no cambie el
estimando**: cualquier suma de ítems 2019 excluye clases de actividad que el
`horas_cuidado` sellado incluye y aplica otra regla de simultaneidad y de presencia.
Para el eje `sexo_edad` (media de horas/semana por persona) la diferencia mueve el nivel
directamente; para `reparto_hogar` (razón Σw·num/Σw·den) mueve numerador y denominador
con pesos desconocidos por sexo y edad — no hay argumento por texto de que la razón sea
invariante a quitar el cuidado emocional y la presencia, y el acto no puede medirlo.

Consecuencia en el marcador: las 11 celdas pasan de `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD`
a `NO-CONSTRUIBLE:<causa>` por la tabla `forense/prereg-caja/PISOS-ENUT2019-ejes-metadatos-v1_0.tsv`.
`sin_piso` **sigue en 21**: este acto cambia la causa, no el conteo — un dictamen
NO-CONSTRUIBLE no fabrica piso.

**Nota para dirección (no para este acto).** Lo que sí sería construible por texto es un
**núcleo común 2019/2024** (los ítems marcados `=`/`≈` sin las clases ∅, con el pasivo
tomado tal cual en cada ola y declarando la diferencia de presencia) medido en **ambas**
olas como estimando nuevo — no como piso de las celdas del árbitro, porque no es
`horas_cuidado`. Requiere abrir `tmodulo` 2024 y validar la suma contra `tvar_crea`
(fórmula de INEGI). Es un acto de caja nuevo con COMMIT-1 propio; no se abre aquí.

Registro documental colateral: el propio portal advierte (manifiesto `:3163`) que los
microdatos de ENUT 2019 se **reemplazaron el 28/ago/2025** con estimaciones de
población actualizadas; la copia del corpus es esa versión. No afecta el veredicto
(que es de contenido, no de ponderador), pero cualquier sucesor que abra 2019 lo cita.

## 2 · P3 · Dictamen, sin medir, de las otras 6 celdas

### 2.1 · (a) `dinero.ahorro.horizonte_corto_ejes_enif2024` × `formalidad` (2 celdas)

Pregunta del encargo: «¿es el mismo P3_13 ausente? Si sí, NO-CONSTRUIBLE con la misma
causa, una línea». **No es sí.** El eje `formalidad` de ENIF 2024 se define por
`P3_13` (yaml `:2164`: universo `P3_13∈{1..7}`; `tools/medidor_ahorro_enif24.py:145`
mapea `"7"` → «sin seguridad social», resto → «con»). La causa que la rejilla escribió
para las 4 celdas de `via_informal` — «P3_13 comparable no existe en ENIF 2021»
(`PISOS-REJILLA-arbitro-metadatos-v1_0.tsv:39-40,55-56`;
`PISOS-ENIF2021-ejes-spec-v2_1.md:19` «Formalidad sigue NO-CONSTRUIBLE por ausencia de
contraparte de P3_13») — se verificó **por nemónico**, no por texto. Leído el FD de ENIF
2021 (`enif_2021_fd_pdf.zip` → `enif_2021_estructura_del_archivo.xlsx`, hoja `TModulo`,
fila 83) contra el de 2024 (`enif_2024_fd.xlsx`, hoja `TMODULO`):

| | ENIF 2021 · `P3_10` | ENIF 2024 · `P3_13` |
|---|---|---|
| pregunta | 3.10 Por parte de su trabajo, ¿usted tiene derecho a los servicios médicos... | 3.13 Por parte de su trabajo, ¿usted tiene derecho a los servicios médicos... |
| 1 | del IMSS o Seguro Social? | del Seguro Social (IMSS)? |
| 2 | del ISSSTE Federal o Estatal? | del ISSSTE? |
| 3 | de PEMEX, SEDENA o SEMAR? | del ISSSTE estatal? |
| 4 | de un seguro médico privado? | de PEMEX, Defensa o Marina? |
| 5 | de otra institución? | de un seguro privado de gastos médicos? |
| 6 | **No tiene servicio médico** (incluye Seguro Popular, INSABI) | de otra institución? |
| 7 | — | **carece de derecho a servicios médicos por parte de su trabajo** (incluye IMSS-Bienestar, antes Seguro Popular, INSABI) |
| 9 / b | No sabe / Blanco por secuencia | No sabe / Blanco por secuencia |

La misma pregunta, el mismo residual («no tiene / carece»), con el ISSSTE federal y
estatal fundidos en un código en 2021 y partidos en dos en 2024. La dicotomía del árbitro
(«con seguridad social» = tiene derecho por su trabajo a cualquiera de las instituciones;
«sin» = el residual) es **construible por texto** en 2021: `{1..5}`→con, `{6}`→sin. El
desenlace `P4_10` («Si usted dejara de recibir ingresos, ¿por cuánto tiempo podría cubrir
sus gastos con sus ahorros?») existe en 2021 con **los mismos 7 códigos** (`1` = «Menos
de una semana/ No tiene ahorros» … `5`, `8`, `9`), hoja `TModulo` fila 227.

**Dictamen (a): CONSTRUIBLE-POR-TEXTO, NO MEDIDO AQUÍ** (P3 es dictamen, no medición; y
`enif2021*` no está en el perímetro de este acto para abrir microdato). Consecuencias
que este acto **no** ejecuta y asienta como NC:
- las 2 celdas de `horizonte_corto × formalidad` quedan `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD`
  (no se les escribe fila NO-CONSTRUIBLE, porque no lo son);
- las 4 celdas `via_informal × formalidad` que la rejilla selló como NO-CONSTRUIBLE
  tienen causa **refutada por texto**; la tabla de identidad de la rejilla es sellada y
  no se edita desde aquí. Sucesor: un acto de caja que congele `formalidad_2021 :=
  P3_10∈{1..5}/{6}` y mida las 6 celdas como `CALC-PISOS-ENIF2021-EJES-0004`, con la
  diferencia de código (ISSSTE fundido; «no tiene servicio médico» vs «carece de derecho
  … por parte de su trabajo») declarada como límite de comparabilidad.

Es el patrón de `feedback_identifica_contenido_por_identidad_no_por_rotulo` y de
`feedback_n45_no_existe_desplazamiento_de_rotulos`: un nemónico desplazado entre olas no
es una pregunta ausente.

### 2.2 · (b) `familia.union.libre_ejes_eder2017` × `cohorte_nacimiento` (4 celdas)

Celdas del árbitro (yaml `:2060-2063`): cohortes **1961-1970, 1971-1980, 1981-1990,
1991+**; desenlace = tipo de **primera** unión (libre vs directa), leído del panel
retrospectivo `historiavida.csv` (primer `edo_civil1` no-cero por persona). EDER 2017
entrevista a **personas de 20 a 54 años** (`eder2017_fd.pdf:103,169,203`), es decir,
nacidas ~1962-1997, en edades continuas.

La «ola anterior», EDER 2011 (`eder2011_descripcion_de_archivos.xls`, hoja
`EDER_TABLARETRO`, variable `COHORTE`, filas 910-914): muestra **tres cohortes discretas
de tres años** — `1 = 1951-1953`, `2 = 1966-1968`, `3 = 1978-1980` (`0 = Fuera de
cohorte`; `ANIO_NACI` 1947-1990). Cruce con las celdas del árbitro:

| celda 2017 | cobertura en EDER 2011 |
|---|---|
| 1961-1970 | sólo 1966-1968 (3 de 10 años de nacimiento) |
| 1971-1980 | sólo 1978-1980 (3 de 10) |
| 1981-1990 | **ninguna** |
| 1991+ | **ninguna** |

Además, el desenlace no es un estado de periodo sino un **evento de historia de vida
fijo por cohorte**: para una cohorte re-observada, el tipo de la primera unión no
«persiste» ni «cambia» entre 2011 y 2017 — lo que cambia es la **censura** (en 2011 la
cohorte 1978-80 tenía 31-33 años y parte de ella no había tenido aún su primera unión) y
la calidad del recuerdo retrospectivo. Un «piso de persistencia t−1» aquí no acotaría a
un retador sobre la conducta: mediría consistencia de reporte retrospectivo más censura
diferencial, sobre 3 de 10 años de nacimiento en dos celdas y sobre nada en las otras dos.

**Dictamen (b): SIN-PISO-POR-DISEÑO** para las 4 celdas. El propio gradiente por cohorte
(que el árbitro ya sella como CORROBORADA y cross-valida con ENADID 2023) es la
comparación que el diseño de EDER admite; una «ola anterior» no lo es. La tabla de
identidad de este acto **no** escribe filas para EDER (no es ENUT 2019 y el estado
`SIN-PISO-POR-DISEÑO` no existe en el vocabulario `status` de la tabla de la rejilla;
inventarlo aquí sería escribir fuera del perímetro). Se asienta como dictamen en esta
nota y como fila NC con sucesor `SIN-ASIGNAR` salvo que mesa quiera que el marcador
distinga `SIN-PISO-POR-DISEÑO` de `SIN-CONSUMER` — decisión de vocabulario, de mesa.

Nota para dirección (del encargo, no abierta): `eder2025_bd_csv_zip` es una ola
posterior; si mesa quisiera cohortes re-observadas *hacia adelante* (2017→2025), el
mismo argumento de censura aplica en sentido inverso y con mejor cobertura de cohortes;
no se dictamina aquí.

## 3 · Resumen de estados

| celdas | antes (marcador `a92126f0`) | después de este acto | quién lo escribe |
|---|---|---|---|
| ENUT `sexo_edad` ×10 + `reparto_hogar` ×1 | `SIN-PISO` / `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD` | `SIN-PISO` / `NO-CONSTRUIBLE:<causa §1.6>` | tabla `PISOS-ENUT2019-ejes-metadatos-v1_0.tsv` + enlace en `tools/marcador_segmento.py` |
| ENIF `horizonte_corto × formalidad` ×2 | `SIN-CONSUMER…` | **sin cambio** (constructible por texto; medir es de un sucesor) | NC |
| ENIF `via_informal × formalidad` ×4 | `NO-CONSTRUIBLE:P3_13 comparable no existe…` | **sin cambio** en el árbol; causa refutada por texto | NC + hallazgo |
| EDER `cohorte_nacimiento` ×4 | `SIN-CONSUMER…` | **sin cambio** en el árbol; dictamen SIN-PISO-POR-DISEÑO | NC |

`sin_piso` derivado tras este acto: **21** (misma cifra; 11 causas nuevas).
