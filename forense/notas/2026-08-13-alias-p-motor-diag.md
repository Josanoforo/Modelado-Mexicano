# ENCARGO B · ALIAS-P + MOTOR-DIAG — nota forense

## §0 · Arranque

**Entorno.** Repo-only, sin red a portales de datos (gesis.org, microdata.worldbank.org, inegi.org.mx no están en la lista blanca de este entorno — verificado, no asumido), sin `data/raw` montado (`ls data/raw` → `No such file or directory`). Consistente con lo asignado.

**Premisas, corridas contra `dcc4f6a` (origin/main real al redactarse — verificado `git merge-base --is-ancestor dcc4f6a origin/main` → sí, y de hecho `dcc4f6a` era el tip exacto):**

```
$ wc -l data/inventarios/alias-fuentes.yaml data/curacion-registro/aliases-fuentes.tsv
 1529 data/inventarios/alias-fuentes.yaml
    5 data/curacion-registro/aliases-fuentes.tsv

$ python3 tools/curador_registro/via_capa2.py | head -4
Filas en relaciones.tsv: 197
Diffs propuestos (capa2_manifiesto): 0

Diagnóstico auxiliar ...: 78

$ grep -oE '\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -nu | tail -1
71
```

**Colisión con ADR-provisionalidad — real, no evitada, coordinada.** Al arrancar no había rastro del acto en ningún clon local (`/home/pc0/Modelado-Mexicano`, `/home/pc0/proyectos/Modelado-Mexicano`), ninguna rama con "provisional" en el nombre, ningún PR abierto salvo `#197` (SONDA-1, perímetro ajeno). Se creó el worktree (`~/mm-alias-p-motor-diag`, rama `alias-p/motor-diag`) y se empezó §3.1. A mitad de ARRANQUE, `PR #199` ("ADR-72: Declare provisional status...") apareció como abierto — exactamente el acto que el encargo advertía. Verificado antes de tocar `canon/`: `gh pr view 199` mostraba `mergeable: MERGEABLE`, tocaba `canon/gobernanza-v1_15.md`/`canon/estado-programa-v1_10.md`. Se esperó — no se editó `canon/` en paralelo. `PR #199` fusionó (`c490a3a`, ADR-72 sellado), y `PR #201` (censo de explotación, ver abajo) fusionó después (`49e987f`→`184882b`). Se hizo `git merge origin/main` en el worktree (limpio, sin conflicto — este acto nunca había commiteado nada en `canon/` todavía) antes de escribir el ADR propio.

**VENTANA 5 (mensaje de seguimiento, verbatim en `forense/encargos/2026-08-13-B-alias-p-motor-diag.md`), verificada punto por punto antes de aplicarla — ninguna se tomó de la palabra:**

- **(a) Censo de explotación.** `gh pr view 201` → `MERGED`, `data/censo-explotacion-2026-08-13.tsv` existe en `origin/main`, 550 filas. `estado`: `SIN-DEMANDA=538`, `REFERENCIADO-NO-ABIERTO=4`, `EXPLOTADO=4`, `ABIERTO-SIN-HALLAZGO=4` (538/550 = 97.818...% — coincide con la cifra del mensaje). `necesidades_que_lo_citan` no vacío en exactamente 8 filas — coincide. De esas 8, 7 son `*_fd_*`/`*_cuestionario*`/`*_questionnaire*` (descriptor o cuestionario) y 1 sola es `ensafi2023_bd_csv_zip` (`bd_csv` = base de datos, microdato) — coincide exacto, verificado con el archivo real, no con la palabra del mensaje.
- **(b) Número de ADR.** `grep -oE '\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md` tras el merge de `PR #199` → único máximo 72, contiguo 1..72, sin huecos. Este acto sella **ADR-73** (ver `canon/gobernanza-v1_15.md`).
- **(c) Nombre de archivo.** Verificado el precedente real: `forense/encargos/2026-08-13-A-censo-explotacion.md` tuvo que renombrarse en el propio `PR #201` (commit `500080a`) porque compartía nombre base con `forense/notas/2026-08-13-censo-explotacion.md` — `T02` no distingue directorio. Este registro se llama `forense/encargos/2026-08-13-B-alias-p-motor-diag.md` (prefijo `B`, esta sesión ya se llama a sí misma "ENCARGO B" internamente — no colisiona con la nota, que es `forense/notas/2026-08-13-alias-p-motor-diag.md`).
- **(d) La prueba obligatoria del parche no cambia.** Ver §1.

**Lectura completa, como pide el encargo:**
- `data/inventarios/alias-fuentes.yaml` líneas 1-40 (cabecera): documenta el método de MAP-1 (`acron()` sobre 11 inventarios) y **dos exclusiones deliberadas por ambigüedad de truncamiento** — `"ENCUESTA NACIONAL DE CALIDAD D"` (ENCAL vs. posible ENCC) y `"REGISTROS ADMINISTRATIVOS DE A"` (IMSS vs. ISSSTE). Ninguna de las dos se toca en este acto.
- `forense/notas/2026-08-13-map-b-crosswalk.md` §duplicados: nombra `CSES`/`COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018`, `GPS`/`GLOBAL_PREFERENCES_SURVEY` y las dos entradas de `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_*` como probables duplicados **del lado de la demanda** (dos `fuente_canonica_normalizada` distintas para el mismo instrumento real), y los declara explícitamente "fuera de perímetro... eso es resolución de alias del lado de la demanda, no crosswalk demanda↔puerta — declarado para quien mantenga `aliases-fuentes.tsv`". Ese archivo está en el perímetro ESCRIBE de este acto, pero el propio §5 del encargo dice "No toca el archivo paralelo de demanda (ALIAS-D sigue siendo acto aparte)" — CSES/GPS/COMPETENCIAS_FINANCIERAS son exactamente esa clase de defecto (identidad **duplicada en el lado de relaciones.tsv**, no identidad fuente↔payload), así que quedan **declarados aquí, no resueltos** — para ALIAS-D.
- `tools/curador_registro/via_capa2.py` completo (222 líneas antes del parche) — ver §1.

---

## §1 · Parche de `via_capa2.py`, y su ADR

**ADR-73 sellado en `canon/gobernanza-v1_15.md`** (mantenimiento acotado bajo la ventana de ADR-70(d) — `tools/curador_registro/` está congelado hasta la apertura del piloto E0, y el mantenimiento previo "queda permitido únicamente con ADR que lo selle"). Texto completo, evidencia y la prueba de los 4 casos: ver el bloque `**ADR-73 ·**` en ese archivo — no se repite verbatim aquí para no duplicar la fuente de verdad; el resumen ejecutivo:

1. Desglose de estados de `verificar_entrada()` impreso antes de los diffs (`COINCIDE=0 NO_COINCIDE=0 AUSENTE=29 SIN_PAYLOAD=0 RAIZ_NO_CONFIGURADA=14`, 43 filas con `id_manifiesto` resoluble, corpus ausente).
2. Salida con código 1 si `COINCIDE==0` habiendo ≥1 fila con `id_manifiesto` — probado, dispara en este entorno.
3. Frontera de letra (`(?<![a-z])forma(?![a-z])`, dígitos/guion_bajo/espacio/puntuación sí son frontera) + `unicodedata.normalize('NFKD', ...)` sin diacríticos, en vez de `forma in texto_manifiesto`.

**Resultado de la prueba obligatoria (diff exacto de membresía, no solo conteo — `diagnostico_candidatas_sin_id` antes/después importando `derivar()` real):**

| canónico | filas antes | filas después | ¿invierte? |
|---|---|---|---|
| PI | 1 (N19) | 0 | ✅ sí — casaba embebida en "propia" |
| INE | 2 (N25,N26) | 0 | ✅ sí — casaba embebida en "inegi" |
| LATINOBARÓMETRO | 2 (N15,N30) | 2 (N15,N30) | ✅ evidencia correcta ahora — antes casaba solo por una mención tangencial en `usado_para` de 6 payloads ENCUP ajenos ("...proxy vía Latinobarómetro P4NOIJ..."); después casa TAMBIÉN contra los 3 payloads propios (`latinobarometro2024_bd_stata`/`cuestionario_esp`/`fichas_tecnicas`, forma sin acento) |
| SE | 3 (N21,N22,N32) | 3 (N21,N22,N32) | ⚠️ parcial, declarado — deja de casar embebida en "forense" (el mecanismo que el encargo describe), pero sigue casando como palabra suelta: `se` es el pronombre más común del español, 13 apariciones con frontera de letra válida en el corpus, y `SE` no tiene entrada en `alias-fuentes.yaml` (cae al *fallback* del canónico desnudo). Ningún mecanismo de frontera de letra distingue un acrónimo de 2 letras de un pronombre real de 2 letras. Defecto distinto del mecanismo parcheado — declarado para quien extienda `alias-fuentes.yaml` con `SE`, fuera del perímetro de las 4 fuentes que este encargo autorizó (§3.2). |

**3 de 4 invierten limpio; el 4° (`SE`) invierte el mecanismo específico que el encargo cita (embebido en "forense", no en "falsador" — verificado carácter por carácter que "falsador" no contiene la subcadena "se") pero no la membresía, por una causa raíz distinta y declarada.** No se fuerza un resultado falso "4/4" para cerrar en verde: el propio §0 de la Regla de señal del programa dice que un hallazgo real declarado vale más que un checkbox forzado.

**Bonus, mismo mecanismo, no pedido:** `BIARE` (`REL-75de72336ada4a506a3b5476`, N30) también sale del diagnóstico — casaba embebida en "enbiare".

**Efecto neto:** diagnóstico auxiliar 78 → 74 (cifra vigente al parchear — NO se heredó el "78"/"97" que el encargo advertía no asumir; se re-derivó). Diffs propuestos: 0 antes y después (sin corpus, ninguna fila puede promoverse a `SI`).

**Suite dedicada, sin cambios de comportamiento roto:** `python3 -m unittest tools.curador_registro.tests.test_via_capa2` → 4/4 OK, antes y después del parche. Ninguno de los 4 tests ejercita `main()` ni el código de salida (2) — no había cobertura previa de ese camino que el parche pudiera romper, ni se agregó ninguna (fuera del perímetro ESCRIBE: solo `via_capa2.py`, no su carpeta `tests/`).

---

## §2 · Criterio de identidad de alias (COMMIT 1 — spec, antes de escribir alias-fuentes.yaml)

Un payload P es de la fuente F cuando concurre y se cita cuál, con evidencia verificable en `data/manifiesto.yaml`, no por parecido de cadena:

- **(a)** `url_origen` de P pertenece al portal institucional de F.
- **(b)** `usado_para` de P nombra el instrumento de F sin ambigüedad.
- **(c)** `archivo`/`id` de P lleva el identificador de catálogo que el portal de F publica.

Reserva obligatoria: cada alias declara qué clase de objeto ampara — **microdato** / **instrumento** (cuestionario o protocolo aplicado) / **documentación** (codebook, ficha técnica, descriptor, reporte) — para que el diagnóstico auxiliar de `via_capa2.py`, que nunca distingue tipo de objeto, no se lea como "hay microdato" cuando solo hay documentación.

**El primer resultado que produzca este procedimiento es el que se reporta.**

### Los cuatro casos de arranque, verificados (no copiados)

**ISSP — 16 payloads (`za6980_*`×4, `za5900_*`×10, `za7600_*`×2).** (c) las 16 llevan el número de catálogo GESIS explícito en `archivo`. (b) las 16 nombran el módulo exacto en `usado_para` ("ISSP 2017 Social Networks...", "ISSP 2012 Family and Changing Gender Roles IV...", "ISSP 2019 Social Inequality V..."). (a) 9 de 16 tienen `url_origen=gesis.org/...` real; los otros 7 (`za5900_backgroundvar_mx`/`bq`/`cdb`/`mr`/`overview`/`q_mx`/`questionnaire_development_report`) tienen `url_origen: no determinada` — **(a) NO se cumple para esos 7**, se incluyen solo por (b)+(c) — matiz que la tabla del encargo no traía. **Ampara:** microdato (7) + instrumento (3: los `q_mx`/`bq`) + documentación (6). **Hallazgo propio, no en la tabla del encargo:** `za7600` (2 payloads, microdato) documenta ISSP 2019 Social Inequality V, cuyo `usado_para` declara literalmente "NINGUNA -- Mexico ausente de la muestra" — identidad ISSP confirmada igual, pero esos 2 no pueden satisfacer ninguna necesidad que pida dato mexicano, a diferencia de los otros 14.

**LATINOBARÓMETRO — 3 payloads.** (c) `latinobarometro2024_bd_stata`/`cuestionario_esp`/`fichas_tecnicas`, sin acento en `id`/`archivo`, la brecha es exactamente la que el parche de §1 cierra. (a) los 3 con `url_origen=latinobarometro.org/documents/LAT-2024/*`. La entrada `LATINOBARÓMETRO` ya existía en `alias-fuentes.yaml` (MAP-1, 128 entradas) con un solo alias (acentuado) — no necesita alias nuevo, el parche de código ya la hace casar; se extiende solo con `ampara`/`evidencia_identidad`. **Ampara:** microdato (1: `bd_stata`) + instrumento (1: `cuestionario_esp`) + documentación (1: `fichas_tecnicas`).

**CCPV — 8 payloads (`cpv2020_*`).** (a)+(b)+(c) las 8 (url_origen INEGI con slug `ccpv`, `usado_para` nombra CPV/Censo2020/Cuestionario Ampliado, `archivo` lleva `Censo2020`/`cpv2020`) — más fuerte que la tabla del encargo, que solo citaba (b)+(c). **Hallazgo propio, importante:** `alias-fuentes.yaml` ya tenía una entrada `CPV` (de MAP-1, línea ~250) con `slug_portal: ccpv` — **misma fuente real**, verificado por el slug exacto. Pero `via_capa2.py` indexa el diccionario de alias únicamente por `canonico.upper()`, no busca dentro de las listas `alias:` de otras entradas — así que añadir "CCPV" solo a la lista `alias:` de la entrada `CPV` no habría tenido ningún efecto mecánico sobre las filas de `relaciones.tsv` que usan el string `CCPV` (verificado con `cargar_alias()`, que construye `resultado[canon.upper()] = formas`, nunca al revés). Ampliar ese mecanismo de búsqueda sería un 4° cambio a `via_capa2.py`, fuera de los tres que este encargo autorizó. Se optó por una **entrada `CCPV` separada**, cruzada explícitamente con `CPV` en su campo `nota` — no por creer que son fuentes distintas, sino porque el mecanismo actual no permite unirlas sin tocar el archivo fuera de perímetro. **Segundo hallazgo:** ninguno de los 3 payloads "microdato" del grupo (`caas_eum_csv`, `iter_nal_csv`, `ceu_eum_csv`) es la muestra de personas/viviendas del Cuestionario Ampliado — son CAAS (censo de alojamientos de asistencia social), Iter (agregados por localidad) y CEU (cartografía urbana). La muestra real de personas/viviendas del Cuestionario Ampliado **sigue sin descargarse** (`usado_para` de `cpv2020_caas_eum_csv` lo declara explícito: "La muestra real del Cuestionario Ampliado... NO está entre las 576 URLs de este XML — sigue sin bajarse"). **Ampara:** microdato (3, ninguno es la muestra de personas/viviendas) + instrumento (1) + documentación (4).

**EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014 — 7 payloads (`wb2661_*`).** (c) las 7 llevan `wb2661`/`catalog/2661` explícito. (a) las 7 con `url_origen=microdata.worldbank.org/catalog/2661/*`. **Ampara: SOLO instrumento (4: ASQ + Baseline/Year1/Endline) + documentación (3: los tres reportes técnicos) — 0 de 7 es microdato**, confirmado — ningún payload de este grupo puede satisfacer una fila que pida microdato. **Hallazgo mecánico propio:** el canónico completo (con guiones bajos) no aparece así en ningún texto libre del manifiesto — el título real usa espacios y guion ("Early Childhood Education Program Impact Evaluation 2012-2014"). La forma que realmente casa con frontera de letra es `wb2661`; sin ella el alias sería decorativo (no cambiaría el diagnóstico). Se añadió como segunda forma de `alias:`.

---

## §3 · Barrido de alcanzabilidad — dos preguntas distintas, no una (por VENTANA 5)

`data/censo-explotacion-2026-08-13.tsv` (PR #201, fusionado, no repetido aquí) mide: **¿alguna fila de `relaciones.tsv` cita este payload por `id_manifiesto` exacto?** → `SIN-DEMANDA` 538/550 (97.82%).

Este acto mide una pregunta distinta: **¿algún nombre canónico de `relaciones.tsv` (los 75 valores distintos de `fuente_canonica_normalizada`, con sus formas de `alias-fuentes.yaml` o su fallback desnudo) aparece con frontera de letra en el texto propio del payload (`usado_para`+`archivo`)?** — reutiliza literalmente la función `_con_frontera_de_letra()`/`_sin_acentos()` del §1, aplicada payload por payload contra el conjunto de 75 canónicos, no corpus completo contra corpus completo.

**Universo: 550 payloads con `archivo`+`sha256` en el manifiesto** (554 entradas totales, 4 sin ninguno de los dos — notas metodológicas/de licencia, no payloads reales — mismo filtro que usó el censo de explotación, verificado).

**Resultado:**

- **Alcanzables por nombre: 252/550 (45.8%).**
- **Huérfanos por nombre: 298/550 (54.2%).**

**Comparación con ADR-72 (≈321/550, 58%):** cercano pero no idéntico — 23 de diferencia. No se puede reconciliar exacto: ADR-72 no dejó su script exacto en el repo, solo la cifra. Declarado, no forzado a coincidir.

**Comparación con el censo de explotación (538/550 SIN-DEMANDA por id exacto):** la brecha es la sustancia del hallazgo. Verificado: **los 8 payloads citados por id exacto son subconjunto exacto de los 252 alcanzables por nombre** (intersección = 8, ninguno de los 8 queda fuera — control de sanidad del propio método). Eso deja **244 payloads (252−8)** que son "nominalmente del tema correcto" — su propio texto menciona un canónico que `relaciones.tsv` ya usa — pero que **ninguna fila cita por `id_manifiesto`**. Ese es, literalmente, el tamaño de la población que el diagnóstico auxiliar de `via_capa2.py` existe para poner enfrente de un revisor humano — nunca se auto-promueven (§1), pero hoy son estructuralmente invisibles para cualquier mecanismo que solo mire `id_manifiesto`.

**Bloques huérfanos más grandes, por prefijo de `id` (no son defecto de alias, son corpus sin demanda — no se les inventa canónico):**

| prefijo | huérfanos |
|---|---|
| mociba | 47 |
| engasto | 46 |
| endireh | 41 |
| enut | 15 |
| enestyc | 15 |
| banxico | 15 |
| eder | 14 |
| enoen | 10 |
| enaproce | 10 |
| enoe | 7 |
| cpv | 7 |
| wb | 7 |

El encargo citaba "mociba 48, engasto 46, endireh 41" — mociba da 47 aquí, no 48 (±1, método de bucketing distinto, no investigado más a fondo: no cambia la conclusión "corpus sin demanda"). Nota: esta tabla **no es comparable** con la tabla equivalente del censo de explotación (`envipe` 76, `encig` 37, `ennvih` 27, `enoe` 25) — miden universos distintos (huérfanos-por-nombre de 298 vs. `SIN-DEMANDA`-por-id de 538) y por eso las cifras por prefijo difieren mucho (p. ej. `enoe`: 7 aquí vs. 25 allá — la mayoría de `enoe` sí es alcanzable por nombre, solo no está citada por id).

---

## §4 · COMMIT 2 — vía antes → escribe alias → vía después

**Vía en lectura, antes de tocar `alias-fuentes.yaml`** (código de §1 ya aplicado, Commit 1 ya en la rama): `Diagnóstico auxiliar: 74`. `Diffs propuestos: 0`.

**Se extiende `data/inventarios/alias-fuentes.yaml`** (nunca reemplazado — `git diff --stat`: `84 insertions(+), 0 deletions(-)`, un solo archivo): cabecera con la documentación de los dos campos nuevos (`ampara`, `evidencia_identidad`); las 4 entradas de §2 (`CCPV` nueva, `EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014` nueva, `ISSP` nueva, `LATINOBARÓMETRO` extendida con los dos campos nuevos sobre su entrada ya existente). Las dos exclusiones deliberadas de la cabecera (ENCAL/ENCC, IMSS/ISSSTE) no se tocan. `data/curacion-registro/aliases-fuentes.tsv` **no se toca** — su formato (`alias_fuente` → `fuente_canonica_normalizada`, normalización de duplicados **dentro** de `relaciones.tsv`) es el mecanismo de ALIAS-D declarado fuera de perímetro en §0/§5, no el de identidad fuente↔payload que resuelve este acto; ninguna de las 4 fuentes de §2 lo necesitaba.

`CCPV` ganó dos formas de alias adicionales (`cpv2020`, `censo2020`) más allá del canónico desnudo, y `EARLY_CHILDHOOD...` ganó `wb2661` — verificado antes de añadirlas que son las formas que realmente casan con frontera de letra contra el texto propio de los payloads (el canónico completo con guiones bajos de `EARLY_CHILDHOOD...` no aparece así en ningún texto libre del manifiesto; ver §2).

**Vía en lectura, después:** `Diagnóstico auxiliar: 75`. `Diffs propuestos: 0`.

**Diff exacto de membresía (conjunto completo de `diagnostico_candidatas_sin_id`, no la lista impresa — el script trunca su impresión a 50 filas, "no se trunca la cuenta"):**

- **ENTRARON (1):** `REL-894b3c5025557df7ef942f2a` [N13/`EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014`] — la forma `wb2661` añadida es la que la mete; el canónico desnudo no casaba.
- **SALIERON (0):** ninguna.

`CCPV`, `ISSP` y `LATINOBARÓMETRO` no cambian membresía: sus filas correspondientes en `relaciones.tsv` ya casaban antes de este commit (vía el *fallback* de canónico desnudo, o —en el caso de `LATINOBARÓMETRO`— vía la mención tangencial que §1 ya documentó). Las entradas nuevas/extendidas no cambian eso, pero fijan la evidencia correcta y declarada (`ampara`/`evidencia_identidad`) donde antes no había ninguna, y `CCPV` queda con dos formas adicionales verificadas que hacen el casamiento robusto contra los 8 payloads propios en vez de depender de una mención de navegación de portal en una entrada ajena (ver §2).

**Lista nominal de filas que la vía promovería con `--escribe`: ninguna.** `Diffs propuestos: 0` antes y después — sin `data/raw` montado, ninguna fila puede alcanzar `COINCIDE` bajo la regla de promoción vigente (intacta, ver §1), así que `--escribe` no tendría nada que escribir en ningún momento de este acto. **No se corrió `--escribe`** contra el `relaciones.tsv` real, en ningún momento, sobre ningún archivo del repo — `relaciones.tsv` está fuera del perímetro ESCRIBE de este encargo (§1/§5).

---
