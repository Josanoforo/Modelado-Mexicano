# HITO D · Paso 2 · Veredicto **R3.2**
### `hitoD-R3.2` · **v1.0** · 29 de julio de 2026 · **Digitalización/testigos/registrable → baja la mordida**

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R3.2-veredicto-v1.0.md` |
> | **REEMPLAZA A** | — *(nuevo)* |
> | **VERIFICAS ASÍ** | el veredicto es **B**, trae las seis cifras (dos interpretaciones × sin ponderar/FAC_TRA/FAC_P18), la estandarización directa con IC, y la verificación de escala contra `modelo §3.3` / `tramite.yaml` |
> | **NOMBRE ESTABLE** | **`hitoD-R3.2`** |

> ⚠️ **ARTEFACTO FORENSE FECHADO — append-only.** Registra lo hallado el 29/jul/2026 contra ENCIG 2023 (microdatos, tablas `encig2023_04_sec_7` y `encig2023_05_sec_8`, descargados por el usuario el mismo día — procedencia completa en `data/manifiesto.yaml`). No se actualiza: reescribirlo para que cuadre con el estado posterior sería la racionalización post-hoc que el Bloque C prohíbe.

---

## 1 · Lo que estaba pre-registrado *(citado literal, para probar que no se movió)*

> **Regla.** `modelo §3.3`: *"SI el trámite se digitaliza / hay testigos / el funcionario es registrable ENTONCES la mordida baja — PORQUE se rompe la trampa social (G1)"* — `[FUERTE]`, `tramite.yaml: tramite.mordida.con_registro`.
>
> **Serie fijada.** ENCIG 2023, nacional, población que realizó un trámite. Variable: incidencia de corrupción al realizar el trámite, desagregada por modalidad (presencial/discrecional vs. digital/con registro).
>
> **Regla de selección de pregunta ejecutada:** Respaldo 1 (cruce de dos preguntas — `P7_3` modalidad y `P8_4` corrupción por trámite — vía microdatos, unidas por la llave documentada `CVE_ENT+UPM+V_SEL+R_ELE+N_TRA`). No existía candidata primaria (pregunta combinada).
>
> **Umbral.** Brecha de incidencia ≥20 puntos porcentuales, pareando por tipo de trámite cuando la fuente lo permita — declarado `ASIGNADO`, no derivado.
>
> **Definición de B** (`hitoD-preregistro` Nota 4): *"brecha presente pero sin parear tipo de trámite ni entidad, o resuelta solo por Respaldo 2 — degrada a `[MEDIA]`, no refuta: hay señal en la dirección correcta pero no aislada de los confundidores 1-3."*

**Nota sobre el encaje del veredicto:** lo que se encontró —brecha real, dirección correcta, confundidor 1 sí aislado (§2.3)— no coincide en la letra con la definición de B arriba (que asume que *no* se pareó). Es una extensión deliberada de la categoría, no una lectura literal: se documenta como tal en §2.1 y §3.

---

## 2 · Veredicto: **B**

### 2.1 · Motivo de B: gate inalcanzable por construcción, no falla de identificación

**Aritmética explícita.** La incidencia presencial máxima observada, entre los seis cómputos de §2.2, es **13.38%** (interpretación (a) restrictiva, ponderada con `FAC_P18`). Para que la brecha alcanzara el umbral pre-registrado de 20 puntos, la incidencia digital tendría que ser **13.38% − 20% = −6.62%** — un valor negativo, imposible para una probabilidad. **Ninguna incidencia digital posible (acotada por abajo en 0%) puede producir una brecha ≥20pp contra un techo presencial de ~13%.** El gate no falló por ruido, tamaño de muestra o identificación débil: **fue construido sobre una magnitud (0.62/0.38, ~50pp de brecha implícita) que ENCIG 2023 nunca sostuvo como valor** — ver §2.5. Esto no es una falla de este falsador: es una propiedad aritmética de la brecha entre el `ASIGNADO` de `tramite.yaml` y el techo real de incidencia medido.

*(Excepción de grano fino, no de gate: a nivel de tipo de trámite individual, tres celdas — `N_TRA` 13, 17 y el 22B — superan 20pp de brecha bruta, pero con `n_dig` de 3, 7 y 1 respectivamente y cero eventos digitales: es ruido de celdas pequeñas, no evidencia de paso del gate agregado, que es el que la regla de selección pre-registró.)*

### 2.2 · Dirección confirmada en seis cómputos, razón relativa 3.61x–4.86x

*(Corrección de cifra: el encargo citó "razón relativa 3.6x–4.1x". Verificado por aritmética directa sobre los seis cómputos, el rango real es **3.61x–4.86x** — 3.6x–4.1x cubre solo los dos cómputos sin ponderar, no los cuatro ponderados. Se reporta el rango completo, no el parcial.)*

| interpretación | ponderador | presencial | digital | brecha (pp) | razón (pres/dig) |
|---|---|---|---|---|---|
| (a) restrictiva | sin ponderar | 12.21% | 3.00% | 9.21 | 4.070x |
| (b) NA→0 | sin ponderar | 1.84% | 0.51% | 1.33 | 3.608x |
| (a) restrictiva | `FAC_TRA` | 10.81% | 2.23% | 8.59 | 4.855x |
| (b) NA→0 | `FAC_TRA` | 1.42% | 0.37% | 1.05 | 3.822x |
| (a) restrictiva | `FAC_P18` | 13.38% | 2.77% | 10.60 | 4.825x |
| (b) NA→0 | `FAC_P18` | 2.04% | 0.46% | 1.58 | 4.420x |

En los seis, la dirección es la predicha (presencial > digital) y ninguno cruza 20pp. El **valor absoluto** de la brecha depende fuerte de la interpretación de `P8_4=NA` (§2.6) y del ponderador; la **razón relativa** es más estable.

### 2.3 · Confundidor 1 descartado — estandarización directa

Estandarización directa (mezcla de tipos de trámite de un grupo aplicada al otro), IC95% Wald:

| interpretación | dirección | tasa estandarizada | IC95% | cobertura |
|---|---|---|---|---|
| (a) restrictiva | digital → mezcla presencial | 5.07% | [3.36%, 6.79%] | 97.0% (excluye `N_TRA`=18, 3.0% del peso) |
| (a) restrictiva | presencial → mezcla digital | 6.80% | [6.02%, 7.59%] | 100% |
| (b) NA→0 | digital → mezcla presencial | 0.79% | [0.51%, 1.07%] | 100% |
| (b) NA→0 | presencial → mezcla digital | 1.06% | [0.95%, 1.17%] | 100% |

En las cuatro comparaciones el IC de la tasa estandarizada no traslapa con la tasa bruta observada del grupo contrario. **El confundidor 1 (selección de trámite) no explica la brecha**: reponderar cada grupo a la mezcla de trámites del otro no la cierra.

### 2.4 · Reserva metodológica

Varios estratos (`N_TRA`) tienen n>0 pero cero eventos de corrupción; su varianza Wald es 0, lo que angosta artificialmente el IC combinado de la estandarización. Un método exacto (Poisson / regla de los tres) daría IC más anchos en esas celdas. La reserva no cambia la dirección ni el orden de magnitud del resultado, pero los IC de §2.3 deben leerse como un piso de incertidumbre, no un techo.

### 2.5 · Verificación contra `modelo §3.3` y `tramite.yaml` — refutación de escala, no de valor

**Unidad de análisis, verificada, no asumida.** `tramite.yaml:24-46` declara `situacion: realiza_tramite_gobierno` para ambas reglas (`tramite.mordida.discrecional`, `tramite.mordida.con_registro`), y da la probabilidad como `{conducta: paga_mordida, p: 0.62}` — una probabilidad condicionada a la *situación* de realizar un trámite, no a una ventana anual ni a una persona. `modelo §3.3` enuncia la regla en la misma forma: *"SI el trámite... ENTONCES..."*, por trámite, no por persona/año. Ninguno de los dos archivos menciona "año", "anual" ni "al menos una vez" en esta regla. **El motor está construido por-trámite — la misma unidad que este falsador midió** (`P7_3`/`P8_4` son ambas por fila de trámite, `N_TRA`). No hay descalce de unidad entre el motor y la medición.

**Con la unidad igualada, la comparación es de escala.** `tramite.mordida.discrecional` asigna `p(paga_mordida)=0.62` a la condición sin registro/testigos; el techo medido en ENCIG 2023 para la modalidad presencial más cercana a esa condición es **13.38%** (máximo de los seis cómputos), y baja a **1.84%** bajo la interpretación poblacional (b) sin ponderar. `tramite.mordida.con_registro` asigna `p(paga_mordida)=0.12`; el techo digital medido es **2.77%** (máximo de los seis), bajando a **0.46%** en (b). En ambos casos el valor asignado por el motor está **entre 4x y 34x por encima** de lo medido, según la interpretación. **La dirección y la razón relativa (§2.2) se sostienen; los valores absolutos 0.62/0.12 no.**

**Por qué es escala y no valor, y qué implica.** El encargo pidió distinguir esto porque tienen consecuencias distintas: una refutación de *valor* invalidaría el mecanismo (la regla estaría mal incluso en signo/existencia); una refutación de *escala* dice que el mecanismo y su dirección son correctos, pero la magnitud asignada estaba fuera de rango. Es lo segundo. **Por instrucción explícita, la refutación se reformula y los números no se sustituyen**: `tramite.yaml:24-46` no se edita en este veredicto para reemplazar 0.62/0.12 por un nuevo par — porque la propia medición no produce un par único (depende de interpretación de `P8_4=NA` y de ponderador, §2.6), y sustituir un `ASIGNADO` sin fuente por otro número igual de específico repetiría el defecto que `procedencia.yaml:226` señalaba. Lo que se registra es la naturaleza y magnitud del error de escala (este documento) y la propagación a `procedencia.yaml` (§2.5.1).

**2.5.1 · Cierre de `procedencia.yaml:226`.** El pendiente decía: *"ENCIG mide prevalencia de corrupción por trámite; verificar si 0.62 corresponde a alguna categoría concreta o es asignado."* **Verificado: no corresponde a ninguna categoría medida de ENCIG 2023.** Es `ASIGNADO`, confirmado — no una cifra sin verificar. La dirección y la razón relativa (~3.6x-4.9x) sí encuentran apoyo empírico; el valor 0.62 no. Ver propagación en la tabla de §4.

### 2.6 · Límites del pre-registro que no se anticiparon

1. **Códigos intermedios de `P7_3`** (2 banco/tienda, 3 línea telefónica, 5 cajero/kiosco, 6 módulo móvil) — reportados aparte con su n, no asignados a ningún grupo por decisión de quien ejecuta el falsador (ver `hitoD-preregistro` para las cifras completas por código).
2. **Ponderadores distintos entre las dos tablas del cruce.** `encig23_estructura_base_datos.pdf` declara `FAC_TRA` para `encig2023_04_sec_7` y `FAC_P18` para `encig2023_05_sec_8` — ningún documento de INEGI declara un ponderador único para este cruce específico. Se reportaron los tres regímenes (sin ponderar, `FAC_TRA`, `FAC_P18`) en vez de elegir uno.
3. **Ambigüedad de `P8_4=NA` por ruta de cuestionario**, no por azar: solo se pregunta "¿en cuál trámite?" (8.4) a quien ya reportó corrupción en general (8.3); quien no, tiene NA en *todos* sus trámites. Esto separa dos poblaciones-objetivo — (a) restrictiva, entre quienes ya reportaron corrupción, y (b) NA→0, población total — sin que el pre-registro hubiera anticipado la distinción. Se reportan ambas.
4. **`NT_TIPO` rompe la unicidad de la llave documentada.** `CVE_ENT+UPM+V_SEL+R_ELE+N_TRA` —la llave primaria que declara `encig23_estructura_base_datos.pdf`— no es única en `encig2023_04_sec_7`: existe una variable `NT_TIPO`, ausente del diccionario leído, que junto con `N_TRA` sí distingue filas (hasta 3 instancias del mismo tipo de trámite por persona). De las 7,644 llaves repetidas, 7,101 tenían `P7_3` consistente entre instancias (se colapsaron sin pérdida) y **543 tenían `P7_3` divergente** entre instancias de la misma llave — se **excluyeron** del cruce por no poder atribuir sin ambigüedad la modalidad al veredicto de corrupción por tipo de trámite que da `sec_8`.
5. **El "FD" (Descriptor de archivos) de 3 MB que se buscó no se encontró** — ni en la carpeta de descarga del usuario ni embebido en el paquete de microdatos. Se usó `encig23_estructura_base_datos.pdf` (mismo programa/edición, descargado directamente de `inegi.org.mx`, hash registrado) como sustituto funcional. "No pude alcanzar el archivo", no "el archivo no tiene el dato".
6. **Cobertura poblacional de ENCIG, no anticipada en la ficha original.** `encig23_estructura_base_datos.pdf §1.3`: *"La encuesta está diseñada para recoger información de la población de 18 años y más residente en las viviendas particulares seleccionadas en la muestra en ciudades de cien mil habitantes y más."* **Este veredicto, y por tanto `R3.2` bajo esta prueba, no dice nada sobre población rural o de ciudades menores a 100,000 habitantes** — ver también Módulo de auditoría, abajo.

### 2.7 · `N_TRA` 18 — único caso de no penetración digital

En la interpretación (a) restrictiva, el tipo de trámite 18 (*"trámites en un juzgado o tribunal por conflictos legales de tipo familiar, laboral, penal, etcétera"*) tiene 288 filas presenciales (29.86% de corrupción) y **cero filas digitales** — no es que la incidencia digital sea baja, es que la modalidad digital no está representada en absoluto para ese trámite en esta interpretación. En (b) NA→0 sí aparecen 4 filas digitales (0% de corrupción, n insuficiente para leerlo). Es el único de los 21-22 tipos de trámite pareados con esta propiedad; el resto tiene observaciones en ambas modalidades, aunque en varios casos con n de un solo dígito del lado digital.

### 2.8 · Hipótesis nueva, NO pre-registrada — marcada como no confirmada

Los tipos de trámite con mayor incidencia de corrupción **en ambas modalidades** son consistentemente los de mayor discrecionalidad del funcionario: `N_TRA` 17 (Ministerio Público/Fiscalía, 38.71%/12.87% presencial según interpretación), 13 (uso de suelo/construcción, 32-33%), 18 (juzgado/tribunal, ~30/9.75%), 05 (trámites vehiculares con inspección, 27.66%/5.83%) — todos con **algún componente de juicio discrecional del servidor público**. Los trámites de pago rutinario y no discrecional (01 luz, 02 agua, 03 predial) tienen incidencia baja en **ambas** modalidades (2-4% presencial, <1% digital). **Hipótesis candidata, no pre-registrada, no falsada aparte:** el driver dominante podría ser la **discrecionalidad del acto**, no el **medio** por el que se realiza — la digitalización bajaría la mordida principalmente en la medida en que también reduce la discrecionalidad, no por sí misma como canal. Esto no se probó de forma independiente en este ejercicio (discrecionalidad y modalidad están correlacionadas en los propios datos, no se separaron) y **queda marcada explícitamente como no confirmada**, candidata a su propio falsador.

---

## 3 · Por qué **B** y no A / C / D

| | Por qué no |
|---|---|
| **A · Confirmada** | Ningún cómputo (6 de 6) alcanza el gate de 20pp, y §2.1 muestra que el gate era aritméticamente inalcanzable dado el techo de incidencia presencial medido (~13%) |
| **B · Sostenida, no cerrada** ✅ | Señal real, dirección predicha, confundidor 1 aislado (§2.3) y no explica la brecha — pero la magnitud no alcanza el umbral pre-registrado. **Extensión de la categoría** (§1): la definición original de B asumía "sin parear"; aquí sí se pareó/estandarizó y aun así no se alcanza el gate. Se documenta como extensión deliberada, no lectura literal |
| **C · Refutada** | La brecha no está ausente ni invertida en ningún cómputo (6 de 6 en la dirección predicha); refutar exigiría exactamente lo contrario de lo observado |
| **D · Inejecutable** | ENCIG 2023 sí permitió la prueba, vía Respaldo 1 (microdatos, llave documentada, aunque con la corrección de §2.6.4) |

---

## 4 · Tabla de propagación *(ADR-34)*

| Veredicto | Regla / ítem del canon, citado | Edición que exige | Aplicado |
|---|---|---|---|
| **Resuelve** | `milpa/procedencia.yaml:226` — *"verificar si 0.62 corresponde a alguna categoría concreta o es asignado"* | Cerrar como **asignado, confirmado** — no cifra sin verificar. Dirección y razón relativa sostenidas; valor absoluto no | ⬜ pendiente |
| **No toca al valor** | `milpa/tramite.yaml:24-46` — `p(paga_mordida)=0.62`/`0.12` | **No se sustituyen los números** (refutación de escala, §2.5) — se deja constancia de la magnitud del error de escala en este documento | — |
| **Anota, no edita** | `modelo §3.3` — regla `[FUERTE]` de digitalización/mordida | Sin cambio al enunciado (la dirección se sostiene); candidata a nota de escala si el corpus decide anotar tiers contra evidencia cuantitativa | ⬜ pendiente |
| **Registra, no falsa** | Hipótesis nueva §2.8 (discrecionalidad vs. medio) | Candidata a su propio falsador, fuera de este pre-registro | — |

---

## Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** El riesgo aquí no es culturalista de origen —la regla misma es estructural (trampa social, anonimato/registro)— pero una lectura descuidada de "digital baja la mordida" podría deslizarse a "el ciudadano digital es más honesto". El mecanismo medido es institucional (se rompe el anonimato del trámite), no un rasgo de quien lo usa.

**¿Qué sobregeneraliza desde clases medias urbanas?** Esto, de forma literal y verificada (§2.6.6): ENCIG 2023 muestrea **solo población de 18 años y más en ciudades de cien mil habitantes y más** (`encig23_estructura_base_datos.pdf §1.3`, cita textual arriba). Este veredicto no dice nada sobre población rural o de municipios menores — no por elección metodológica de este falsador, sino porque la fuente fijada por Nota 4 no cubre esa población. Es una generalización heredada de la fuente, no introducida por este análisis, y no estaba anticipada en la ficha original.

**¿Qué está sesgado por marcos o muestras extranjeras?** Ninguno. Todo el dato usado es ENCIG 2023, procedencia **(a)** limpia — encuesta mexicana, población mexicana, sin marco importado.

**¿Qué cambiaría con foco rural, indígena o popular?** No se puede saber con esta fuente — es exactamente el hueco del punto anterior. La ficha (`hitoD-preregistro` Nota 4) ya advertía heterogeneidad oculta por agregación a nivel nacional; aquí el problema es más fuerte: no es agregación que oculta al segmento rural, es **ausencia total** del segmento rural en el marco muestral.

**¿Qué parece psicológico y es incentivo racional?** El corpus podría leer "menos corrupción con testigos/registro" como un juicio de carácter (deshonestidad situacional). El mecanismo que sostiene la regla (`modelo §3.3`, G1) es incentivo racional: sin registro nadie observa, con registro el costo de ser detectado sube. No hay apelación a rasgo.

**¿Dónde hay evidencia débil e intuición fuerte?** Dos lugares. (1) Los tipos de trámite con brecha bruta >20pp a nivel individual (`N_TRA` 13, 17, 22B) tienen `n_dig` de 1 a 7 — es exactamente el tipo de "contraejemplo espectacular" que `hitoD-R1.1 §7` ya advirtió que puede ser artefacto de muestra pequeña, no señal. (2) La hipótesis de discrecionalidad (§2.8) es intuitivamente fuerte —los trámites de mayor corrupción son también los de mayor juicio discrecional— pero no se aisló de la modalidad: es observación, no prueba.

**¿Qué sería peligroso mal usado?** Tres lecturas. **(1)** *"R3.2 fue confirmada"* — no: el gate no se alcanzó en ningún cómputo, y §2.1 muestra por qué no podía alcanzarse dado el `ASIGNADO` original. **(2)** *"R3.2 fue refutada"* — tampoco: la dirección se sostuvo 6 de 6, con confundidor 1 descartado. **(3)** *"0.62 y 0.12 ahora se saben mal y el motor debe corregirse con los nuevos números"* — es precisamente lo que este documento evita hacer (§2.5): es refutación de escala, no de valor, y sustituir un `ASIGNADO` por otro número específico sin fuente repite el defecto original.
