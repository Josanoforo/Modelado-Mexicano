# S14 · Pre-registro de `R7.4` sobre las tres encuestas del corpus que sí traen desenlace de protesta — y por qué ninguna satisface la regla

### `prereg-caja-S14` · **v1.0** · 7 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S14-R7-4-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S14`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.sav`/`.dta`/`.xlsx`, de `civico.protesta.agravio_urbano_multiola` (`R7.4`) sobre las tres encuestas del corpus que el inventario revela con desenlace de protesta: **ENCUP 2012**, **losmexicanos Cultura Política** (UNAM-IIJ) y **Tercera Encuesta Nacional de Cultura Constitucional** (UNAM-IIJ). Corrige el alcance de la cláusula vigente (§0.2) y cierra con veredicto de existencia (§2). |
> | **QUÉ NO ES** | No abre dato. No mide. No mueve el tier de `R7.4` (`[MEDIA-FUERTE]`, `ACOTADA-CON-RESERVA`). **No reescribe la cláusula `se_mueve_si` de la propuesta** — la reescribe el SELLO que consuma esta spec, si mesa lo firma. No habilita `L22`: §2 cierra `EXISTE-NO-SATISFACE` y la condición que el encargo puso para `L22` («solo si S14 §2 pre-registra al menos una encuesta con los cinco términos») **no se cumple**. |
> | **VERIFICAS ASÍ** | Caja —si mesa la lanza pese a §2— abre cada encuesta por separado y confirma, antes de calcular, que ningún ítem de victimización personal existe bajo un nombre que el inventario no capturó. Si aparece, ese hallazgo reabre esta spec y se reporta antes de calcular nada. |

**Acto:** `ACTO MAESTRA38-N23-N25 · TRES-SPECS-NEGATIVOS`, 7/sep/2026, entorno **NUBE** (`cloud_default`), sobre `origin/main = 604793fa` (PR #591, base confirmada por `git fetch origin main` al arrancar).

**Evidencia de existencia sobre la que se congela:** `forense/notas/2026-09-07-MAESTRA38-N23-N25-barrido-negativos.md` §3 — script `tools/barrido_negativos_m38.py`, 317 718 filas de inventario examinadas, conteo por término y por encuesta.

---

## 0 · Ficha bajo prueba y corrección de alcance (A.8/A.13)

### 0.1 · Definición vigente

`canon/modelo-decision-v4_0.md:558`: *«**SI** hay agravio personal/familiar + falla estatal palpable + red previa **Y** el entorno es **urbano con espacio público disponible** **ENTONCES** se suma a **protesta** … PORQUE G4 (destructor selectivo) — `[MEDIA-FUERTE]`»*.

`python3 tools/ya_medido.py R7.4` (corrido al redactar): resuelve a `civico.protesta.agravio_urbano`; `milpa/tramite.yaml:1212` trae `situacion=SELLADA tier=FUERTE`, `veredicto_Bbis=NO-DISCRIMINA` / `CORROBORADA`, `p=0.112192`; veredicto del script: **`MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md, 2026-09-07-MAESTRA38-CARGA-LAPOP-resultados.md, L11, L5, L9, S5`**. La entrada que esta spec toca es la **tercera formulación**, `milpa/tramite-ola5-propuesta-v0.yaml:3467` `civico.protesta.agravio_urbano_multiola`, `situacion: ACOTADA-CON-RESERVA`, `tier: PENDIENTE-DE-MESA`.

**Cláusula vigente, verbatim (`milpa/tramite-ola5-propuesta-v0.yaml:3482`):** *«sin instrumento hoy: ENVIPE 2025 no trae desenlace de protesta (FP-329 (c)); se mueve si entra al corpus una fuente con sobremuestra rural Y desenlace de protesta; hasta entonces, ACOTADA-CON-RESERVA (D2-h) sin fecha»*.

### 0.2 · Corrección de alcance — la cláusula es correcta sobre ENVIPE y excede su universo

El universo del cierre que produjo esa cláusula es **ENVIPE FD 2025** (FP-329 (c)). Sobre ese universo la afirmación se sostiene y esta spec no la contradice. Lo que la cláusula hace y no debió hacer es **escribir «sin instrumento hoy» sin haber consultado el inventario por instrumento completo**: el barrido de `MARCHA|PROTEST|MANIFEST|PLANTON|MITIN|BLOQUEO|HUELGA|PARO|PETICION` sobre las 317 718 filas devuelve **197 aciertos**, con desenlace declarado de protesta en tres encuestas del corpus que ENVIPE no es.

**Redacción que el alcance verificado soporta:** *«sin instrumento **en ENVIPE 2025**: no trae desenlace de protesta»*. **Esta spec no la escribe** — la propuesta no está en su perímetro; la reescribe el SELLO que consuma esta pieza, si mesa lo firma. Aquí queda declarada, con el comando y la salida que la justifican, para que quien la escriba no tenga que re-investigar.

Esta corrección de alcance es el caso número tres del hallazgo `PARA-v2.13` que este mismo acto registra en `forense/hallazgos.md`.

---

## 1 · Tabla de existencia — los cinco términos de la regla, por encuesta

Verificado contra los tres inventarios vigentes, campos `variable_id` **y** `texto_reactivo`, insensible a mayúsculas. Patrón por término, verbatim, en `tools/barrido_negativos_m38.py::TERMINOS_R74`. Filas de inventario examinadas por encuesta declaradas en la primera columna (A.13).

| término de la regla | **ENCUP 2012** (282 filas) | **losmexicanos Cultura Política** (610 filas) | **Cultura Constitucional 3ª** (864 filas) |
|---|---|---|---|
| **PROTESTA** (desenlace) | X · `P56_5` «Para resolver un problema que afecta a usted y a otras personas, ¿alguna vez ha tratado de **Asistir a manifestaciones**»; `P58_7` «Firmar documentos en señal de protesta»; `P58_8` «Participar en manifestaciones a favor o en contra del gobierno» | X · `p48_6`/`p48_7` «Participado en una protesta»; `p48_9` «Participado en una manifestación»; `p48_12` «Participado en una huelga o paro»; `p54_1` (qué hacen los vecinos) | X · `P52` «cuando un grupo social exige sus derechos mediante paros, bloqueos y plantones»; `P53_4`/`P53_6` (mejor forma de actuar: hacer una marcha / hacer bloqueos) — **actitud/norma, no conducta propia**; `P54_*` es qué deberían hacer las autoridades |
| **VÍCTIMA** (antecedente 1) | **`NO-ENCONTRADO`** | **`NO-ENCONTRADO`** | **`NO-ENCONTRADO`** |
| **FALLA_ESTATAL** (antecedente 2) | X · `P30_17` jueces, `P30_18` Suprema Corte, `P30_21` gobernadores (escala 0-10) — 35 variables de confianza | X · 54 variables; `p54_*` «Si las autoridades no resuelven algún problema en donde usted vive…» | X · `P13_1` policía, `P13_10` Suprema Corte, `P13_15` Ministerio Público, `P13_17` tribunales (escala 0-10) — 67 variables |
| **RED_PREVIA** (antecedente 3) | X · `P57_1`…`P57_5` «Durante el último año, ¿asistió a alguna reunión de… juntas de vecinos / junta de colonos / agrupación u organización de ciudadanos / asambleas de la comunidad?»; `P56_4` pedir apoyo a asociación civil | X · `p53_1`…`p53_9` «En cuáles de las siguientes organizaciones participa o ha participado»; `p48_8` buscado apoyo de una organización | **`NO-ENCONTRADO` como pertenencia** · solo 2 aciertos, ambos de **confianza** en organizaciones (`P13_8` ONG, `P13_11` sindicatos) — confianza no es red previa |
| **URBANO/RURAL** (estrato) | **`NO-ENCONTRADO`** · el archivo trae `Tipo de seccion` y `Circunscripcion`; ninguna declara urbanidad en su etiqueta, y el mapa de valores no está en el inventario | X · `Estrato`; `Tam_loc` «Tamaño de localidad»; `loca` «Localidad» | **`NO-ENCONTRADO` como estrato** · solo `LOC` «Localidad» (identificador, no clasificación urbano/rural) |
| **PONDERADOR** | X · `factor`; `POND` (dos candidatos, ninguno con etiqueta que los distinga) | X · `Pondi2` «Factor de expansión»; `Pondi_v` «Factor de expansión vivienda» | X · `Pondi2` «Factor de expansión post-estratificado» |

### 1.1 · El negativo de `VÍCTIMA`, declarado como manda A.13

**Patrón usado** (deliberadamente ancho, para que el negativo signifique algo): `VICTIM|DELITO|DELINCUEN|ROBO|ROBAR|ASALT|EXTORSI|SECUESTR|INSEGURID|LE HA PASADO|HA SUFRIDO|FUE OBJETO|CRIMEN`.

**Filas examinadas:** 282 + 610 + 864 = **1 756**, sobre las 317 718 del universo total.

**Aciertos y por qué ninguno sirve:**

| encuesta | aciertos brutos | qué son |
|---|---|---|
| ENCUP 2012 | 1 | `P67_4` «¿usted aceptaría o no que su hijo… **probara alguna vez alguna droga**?» — acierto por `droga`≠, actitud parental |
| Cultura Política | 4 | `p13_1`/`p13_3`/`p13_6`/`p13_8` «¿Quién o quiénes realizan las siguientes funciones? **Juzgar a los delincuentes**» — conocimiento cívico de atribuciones |
| Cultura Constitucional 3ª | 12 | `P55_1_1`…`P55_7_3`, la misma batería de atribuciones («juzgar a los delincuentes», «aprobar los impuestos») |

**Cero de las tres pregunta si la persona fue víctima de un delito.** El primer término del `SI` —el que define el universo del contraste, no un covariado— no existe en ninguna.

---

## 2 · Veredicto de esta spec: `EXISTE-NO-SATISFACE` en las tres, con el término faltante nombrado

El encargo fija la regla de decisión: *«se pre-registra la medición solo en la(s) encuesta(s) que tengan los cinco; si ninguna los tiene, la spec cierra como `EXISTE-NO-SATISFACE` con el término faltante nombrado por encuesta — y eso es entregable».*

| encuesta | términos presentes | términos faltantes | veredicto |
|---|---|---|---|
| **ENCUP 2012** | PROTESTA, FALLA_ESTATAL, RED_PREVIA (3 de 5) | **VÍCTIMA**, **URBANO/RURAL** | `EXISTE-NO-SATISFACE` |
| **losmexicanos Cultura Política** | PROTESTA, FALLA_ESTATAL, RED_PREVIA, URBANO/RURAL (4 de 5) | **VÍCTIMA** | `EXISTE-NO-SATISFACE` — **la más cercana: le falta un solo término** |
| **Cultura Constitucional 3ª** | PROTESTA (actitudinal), FALLA_ESTATAL (2 de 5) | **VÍCTIMA**, **RED_PREVIA**, **URBANO/RURAL** | `EXISTE-NO-SATISFACE` |

**Ninguna encuesta tiene los cinco ⇒ esta spec no pre-registra ninguna medición.** No se sustituye `VÍCTIMA` por un proxy (percepción de inseguridad, confianza en la policía, «qué hacen los vecinos cuando las autoridades no resuelven»): sustituir el término que define el universo, después de ver que falta, es exactamente lo que un pre-registro existe para impedir. `S13 §0.2` sentó el precedente al negarse a inventar un desenlace sustituto sin mandato de mesa; aquí aplica al antecedente.

**Consecuencia declarada, no adjudicada:** `L22` **no queda habilitada** (la condición del encargo era «al menos una encuesta con los cinco»). Lo que sí queda establecido, y es lo que la cláusula vigente negaba: el desenlace de protesta **existe** en el corpus fuera de ENVIPE, y **una sola variable** —victimización personal— separa a `losmexicanos Cultura Política` de ser instrumento completo para `R7.4`. Eso reorienta la búsqueda de fuente: no hace falta «una fuente con sobremuestra rural Y desenlace de protesta» (cláusula vigente); hace falta **una fuente con desenlace de protesta Y victimización personal**, con estrato urbano/rural — dos condiciones distintas, y la segunda es la que nadie había nombrado.

---

## 3 · Forma del contraste, congelada por si mesa habilita un sucesor con instrumento completo

Copiada de `prereg-caja-S5-L5 §3.1`, sin cambio de forma. Se congela aquí **aunque §2 cierre negativo**, para que un sucesor que encuentre el instrumento no re-derive el diseño después de ver el dato.

**Celda principal (2 celdas) — el subgrupo de alto riesgo contra sí mismo por entorno:**

```
C_completo = P(protesta | AGRAVIO ∧ FALLA_ESTATAL_BAJA ∧ RED_PREVIA, URBANO) −
             P(protesta | AGRAVIO ∧ FALLA_ESTATAL_BAJA ∧ RED_PREVIA, RURAL)
```

**Celdas diagnósticas** (una por antecedente, 2×2 contra `URBANO`), para que la caída de `C_completo` por guardia no deje la pieza sin nada que reportar: `C_agravio`, `C_falla`, `C_red`.

**Dicotomizaciones, regla conceptual (corte exacto pendiente de codebook en todos los casos):** `FALLA_ESTATAL` = mitad inferior de la escala de confianza en justicia (`P30_17`/`P30_18` en ENCUP; `P13_1`/`P13_15`/`P13_17` en Cultura Constitucional) = `BAJA`. `RED_PREVIA` = 1 si cualquier ítem de participación/asistencia (`P57_1`…`P57_5`; `p53_1`…`p53_9`) es distinto de «nunca». `URBANO` = dicotomización de `Tam_loc`/`Estrato` (categorías de ciudad = urbano; resto = rural). `AGRAVIO` = **no construible** (§1.1).

**Cota de n mínima por celda:** numerador `< 10` ⇒ `NO-ESTIMABLE`, misma guardia que `S4 §3`, `S5 §3.1` y `S13 §2` — no se reinventa un umbral distinto.

**Ponderador y estrato, por nombre de variable:** Cultura Política `Pondi2` (persona) / `Pondi_v` (vivienda), estrato `Estrato` + `Tam_loc`; Cultura Constitucional `Pondi2`; ENCUP `factor` **o** `POND` — **dos candidatos sin etiqueta que los distinga: caja adjudica contra el codebook antes de ponderar, nunca por parecido de nombre** (`S6 §1.3`, `fac_3b` vs `fac_3b_px`; `S13 §3`, `weight1500`).

**Cláusula PARA (patrón S6/S12, verbatim):** **si la variable no existe en el archivo, PARA.** No se sustituye, no se aproxima, no se elige después de ver el dato.

---

## 4 · Escala de falsación `B-bis` — qué significaría corroborar

| fila | qué la satisface |
|---|---|
| `CORROBORADA` | `C_completo` positivo con IC95 íntegramente sobre 0: entre quienes cumplen los tres antecedentes, protestar es más frecuente en entorno urbano que rural |
| `CONTRARIA` | `C_completo` negativo con IC95 íntegramente bajo 0 |
| `NO-DISCRIMINA` | IC95 cruza 0 con ambos brazos estimables |
| `NO-ESTIMABLE` | numerador `< 10` en cualquiera de los dos brazos (resultado esperado a priori en la rama rural: `S5 §3.1` lo anticipó y `L5` lo confirmó — `p=NO-ESTIMABLE` en las tres olas LAPOP) |
| **`EXISTE-NO-SATISFACE`** | **la fila que esta spec devuelve hoy**: el instrumento existe y el desenlace se mide, pero falta un término del `SI` — se nombra cuál, por encuesta (§2), y no se corre nada |

---

## 5 · Archivos que la caja necesitaría abrir

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `encup_2012_base_datos_xlsx` | `encup_2012_base_datos_xlsx.xlsx` | `50341d97a3e305e6ed3348757632e5b23ab2e87b2052304961905619d85612e4` |
| `encuesta_nacional_de_cultura_politica_3` | `losmexicanos_unam_iij/culturapolitica/Encuesta_Nacional_de_Cultura_Politica.sav` | `d428b11b02d24666c6ecf8397a51d6dc7f868fad772d6bda4f2b7fabe228c7f9` |
| `tercera_encuesta_nacional_de_cultura_constitucional_3` | `cultura_constitucional_unam_iij/Tercera_Encuesta_Nacional_de_Cultura_Constitucional.sav` | `1cda92a6036c27c131b247c8ab2116df1a6f8005c94dd0d8efae2fed8b50a75d` |

**Ninguno se abre en este acto.** Los gemelos `.dta` de las dos encuestas UNAM-IIJ existen en el corpus y traen las mismas variables (verificado en el inventario); se citan como verificación cruzada, no como fuente alterna.

---

## 6 · Qué NO hace este acto

No abre ninguno de los archivos de §5. No mide, no calcula ninguna celda ni IC95. No mueve el tier de `R7.4`. **No edita `milpa/tramite-ola5-propuesta-v0.yaml`** — la corrección de alcance de §0.2 queda declarada, no aplicada. No habilita `L22` (§2). No sustituye `VÍCTIMA` por proxy. No toca `S15`/`S16` (piezas hermanas, archivos separados) ni ninguna spec existente. No toca `data/cruce-ola6-v1_0.tsv`.

**El primer resultado que produzca este procedimiento es el que se reporta.**
