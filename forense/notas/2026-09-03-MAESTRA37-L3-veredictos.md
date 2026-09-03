# MAESTRA37-L3 · P1/P2 — cinco veredictos A.4 con texto de reactivo a la vista (COMMIT-2)

Universo: el congelado por `COMMIT-1` en
`forense/notas/2026-09-03-MAESTRA37-L3-universo.md` — **11 archivos**, 121
etiquetas de `utilizadores`, **8 790 filas** de catálogo sobre 1 914
variables (`data/l3-ensanut2024-catalogos-v1_0.tsv`) y **8 973 líneas** de
cuestionario sobre 136 páginas (`data/l3-ensanut2024-cuestionarios-v1_0.txt`).
Vocabulario A.4 verbatim de `.claude/commands/mapea.md` §4, los cuatro
términos: `EXISTE-SATISFACE`, `EXISTE-NO-SATISFACE`, `NO-ENCONTRADO`,
`NO-ACCESIBLE`.

**`NO-ACCESIBLE` se usa aquí en su sentido literal de A.4/A.13** — *"falta el
archivo […]; cero filas examinadas no es un negativo, es un comando que no
corrió"*. Es la etiqueta correcta, y no `NO-ENCONTRADO`, para una regla cuyo
reactivo **sí existe en el instrumento leído** pero cuyo microdato no está en
el corpus. La distinción no es cosmética: decide si lo que falta es
**adquisición** o **instrumento**, que es justamente lo que `P2` tiene que
decir.

---

## R4.1 · `salud.atencion.leve_sin_imss` — `EXISTE-NO-SATISFACE`

> **SI** el padecimiento es leve-moderado y no hay IMSS (`segsoc`=2)
> **ENTONCES** farmacia con consultorio o automedicación
> (`canon/modelo-decision-v4_0.md`:526)

| | reactivo · código |
|---|---|
| **desenlace** | `u0201` / `u0202b1` «¿En qué institución de salud se atendió/recibió atención?» — **código `12` = «Consultorios pertenecientes a farmacias / Farmacias con consultorio médico»**. La mitad "farmacia con consultorio" del consecuente está operacionalizada **literalmente**, con su propio código, en tres instrumentos (utilizadores 2.1 y 2.2.b.1; hogar 4.8 `H0408`). Privado 13–18, público 1–6 y 26, tradicional 20–21 |
| **disparador** | `u0202b` «¿Entonces tiene(s) derecho/puede(s) atenderse(te) en los siguientes servicios médicos…» — **código `10` = «Ninguno»**, y `uh0310_m` (3.10 de hogar) como fuente original. Derechohabiencia queda medida, incluida la distinción IMSS (`1`) / IMSS-BIENESTAR (`11`) / seguro privado (`8`) |
| **unidad** | persona × último episodio de necesidad de salud en 3 meses |

**Qué falta, en la misma línea (dos cosas, ninguna menor):**

1. **«Leve-moderado» no se pregunta en ninguna parte del universo.** Lo más
   cercano es `H0402` (hogar 4.2), que da **tipo** de necesidad en ~30 códigos
   (`01` infecciones respiratorias, `02` diarrea, `16` diabetes, `27` cáncer,
   `38` lesión, `40` dolor de cabeza, `46` cirugía, `47` depresión…), no
   **gravedad**. La única gravedad explícita del universo es `H0405` código `1`
   «Decidió que no era necesario buscar atención **porque no era tan grave**» —
   pero su universo es **quien NO buscó atención**, es decir, el complemento
   exacto de las personas cuyo desenlace R4.1 quiere observar. Derivar
   "leve" del tipo de padecimiento sería **aproximación**, y por la regla del
   propio encargo eso es `EXISTE-NO-SATISFACE`, no `SATISFACE`.
2. **«Automedicación» no tiene código en ninguna pregunta de necesidad de
   salud.** El término aparece **2 veces en 8 973 líneas**, ambas en el módulo
   de violencia (`D0806`, «Remedios caseros, automedicación» como respuesta a
   dónde se atendió tras una agresión) — otro desenlace, otro universo. Y hay
   una razón estructural, no un descuido de vocabulario: el cuestionario de
   utilizadores declara en su portada que es **«solo para las personas que SÍ
   recibieron atención médica en los últimos 3 meses»**, y `u0103` = «No»
   manda a *Fin de la entrevista*. **Quien se automedicó está excluido del
   módulo por construcción.** Ninguna reformulación lo recupera.

**Lo que sí gana este acto sobre `L1`:** `L1` reportó *"`farmacia`/`automedic*`:
0/31 677"*. Sobre el universo de este acto, `farmacia` da **45 aciertos en el
catálogo y 32 en los cuestionarios**, y uno de ellos es el código `12` que
operacionaliza el consecuente al pie de la letra. El cero de `L1` era del
extractor y de las formulaciones, no del instrumento. Va a `hallazgos.md`.

**Bonus que el modelo pedía y el instrumento sí trae:** el `PORQUE` de R4.1
está acotado a *costo, tiempo y trato*, y el modelo advierte que **«el trato es
la dimensión que no mejora al abrir una clínica — sin medir trato no se
distingue refutación de re-atribución»**. Las baterías `U0202CA/CB/CC` y
`U0202C1A/B/C` («¿por qué motivos no se atendió en el lugar que le
correspondía?») traen las tres: costo (`07`), tiempo (`08`, `09`, `03`, `04`),
y **trato explícito** (`10` «No me gusta la atención que dan/no son amables»,
`11` «En general no confío en el diagnóstico/tratamiento», `12` instalaciones).
`U0202DA/D1A` da la versión contrafactual («¿qué tendría que cumplirse
para que acudiera…?»). Eso no cambia el veredicto —no mide el desenlace— pero
es el instrumento que la advertencia del modelo pedía y que nadie había
localizado.

---

## R4.4 · `salud.atencion.grave` — `EXISTE-SATISFACE` (confirmado con texto)

> **SI** el síntoma es grave o crónico complejo **ENTONCES** busca el sistema
> público pese a la espera (`modelo-decision-v4_0.md`:527)

| | reactivo · código |
|---|---|
| **desenlace** | `u0201` códigos `1` IMSS, `26` IMSS-BIENESTAR, `2` ISSSTE, `6` Centro de Salud u Hospital de la SSA = sistema público; **«pese a la espera»** se mide directo con `u0205h`/`u0205m` «Una vez en el lugar de atención, ¿cuánto tiempo tuvo que esperar?» y `u0204h/m` (tiempo de traslado). `U0202UA` código `09` «No tuve otra opción» da el motivo declarado |
| **disparador** | `H0409A–D` (hogar 4.9) «La atención que buscó ¿requirió… `2` **hospitalización (internamiento)**? `3` **consulta de urgencias**?» — más los códigos crónico-complejos de `H0402` (`16` diabetes, `17` hipertensión, `27` cáncer o tumores, `46` cirugía) |
| **unidad** | persona × episodio |

`L1` lo dio `EXISTE-SATISFACE` sin cambio (heredado de `N5`); este acto lo
**confirma con el texto a la vista**, que es lo que el encargo pedía.

**Reserva escrita, y se aplica el mismo rasero que a R4.1:** la palabra
"grave" tampoco se pregunta. La diferencia que sostiene el veredicto —y que
hay que poder defender— es que `H0409` **no aproxima la gravedad por el
nombre del padecimiento**, sino que mide directamente la **intensidad de
atención que el episodio requirió** (internamiento / urgencias). Eso es un
observable del propio episodio, no una imputación del analista; "gripe = leve"
sí lo sería. Es la razón por la que R4.1 no sube y R4.4 no baja.

---

## R4.3 · `salud.adherencia.desabasto_vs_cuidadora` — `NO-ACCESIBLE` (rama desabasto) · `NO-ENCONTRADO` (rama cuidadora)

> **SI** hay desabasto + gasto de bolsillo alto **ENTONCES** abandono o
> intermitencia del tratamiento crónico; **SI** hay familia cuidadora +
> medicamento surtido **ENTONCES** mayor adherencia
> (`modelo-decision-v4_0.md`:529)

**`L1` lo dio `NO-ENCONTRADO` (0/0/0 en las tres formulaciones dirigidas). Es
el negativo que este acto corrige, y no por poco.** El módulo `adultos` de
ENSANUT 2024 trae desenlace y disparador **en la misma persona y en la misma
pregunta**:

| | reactivo · código |
|---|---|
| **desenlace** | `a0313` «En los últimos seis meses ¿Ha **suspendido** algún(os) de los medicamentos **más de una vez a la semana**?» (`1` Sí / `2` No / `9` NS) — *intermitencia*, literal. `a0405b` «¿Por cuánto tiempo ha **dejado de tomar** el medicamento?» (`1` 1 día · `2` 2–6 días · `3` 1–3 semanas · `4` 1 mes o más) — *abandono*, con duración |
| **disparador desabasto** | `a0314` / `a0405c` «¿Cuál fue la **causa principal** de haber dejado de tomar sus medicamentos?» — código **`5` «No le surtieron los medicamentos en la unidad médica»**, código **`6` «No encontró el medicamento en la farmacia»**, código `10`/`7` «Se le terminó el medicamento antes de surtir su siguiente receta» |
| **disparador gasto** | misma pregunta, código **`7`/`8` «No tuvo dinero para comprarlo(s)»** |
| **unidad** | persona con condición crónica × tratamiento (diabetes §3, hipertensión §4) |

Esto **satisfaría** el criterio de A.4 sin faltante: el reactivo pregunta
literalmente lo que la definición pide, y además atribuye la causa, que es
más de lo que la regla exigía.

**Por qué no dice `EXISTE-SATISFACE`:**
`adultos_ensanut2024_w.stata.stata.zip` **no está en `descargas_mx`**
(`AUSENTE-EN-RAIZ`, verificado al arrancar: 14 aciertos ENSANUT 2024 sobre
149 archivos, y de `adultos` sólo el catálogo). **Cero filas de microdato
examinadas.** Por A.13 eso no es un negativo, es un archivo que falta —
`NO-ACCESIBLE`. **Lo que falta aquí es adquisición, no instrumento.**

**La segunda rama sí es `NO-ENCONTRADO` sobre el universo declarado.**
«Familia cuidadora» no existe como ítem: `cuidador` da **3 aciertos en 8 973
líneas y 2 en 8 790 filas de catálogo**, todos ajenos — `m0103_id` «Seleccione
al cuidador/a que responde el cuestionario de niños de 0 a 9 años» (rol del
informante) y `a0819f` «Del recuerdo de su mamá, cuidadora o informante»
(fuente de un dato de peso al nacer). Ninguno mide apoyo de un cuidador a la
adherencia. `adherenc` da **0/0**. La rama contrastiva de la regla —la que la
hace falsable, porque opone estructura a G5— **no tiene instrumento aquí, ni
siquiera con `adultos` en la mano.**

---

## R4.2 · `salud.prevencion.hombre_sin_permiso` — `EXISTE-NO-SATISFACE`

> **SI** es hombre trabajador **sin permiso laboral** (modificador machista)
> **ENTONCES** pospone el chequeo hasta el síntoma grave
> (`modelo-decision-v4_0.md`:528)

El encargo anticipaba `NO-ENCONTRADO` acotado a «módulo adultos ausente del
corpus». **El universo congelado permite decir algo más exacto, y menos
favorable a la regla**, porque `P0(b)`/`P0(c)` metieron al censo el catálogo
de `adultos` (843 variables) y su cuestionario (44 páginas): se puede leer
**qué se preguntó** aunque no se puedan contar respuestas.

| | reactivo · código |
|---|---|
| **desenlace** (existe) | Batería `A1001` «Durante los últimos 12 meses, un médico u otro profesional de la salud le realizó… **`j)` detección de cáncer de próstata**, `g)` detección de diabetes, `h)` de hipertensión, `f)` de sobrepeso u obesidad, `i)` colesterol» — con su contraparte `A1001*B` «¿**Por qué no** le realizaron la detección?», que trae `11` «**No tiene tiempo**», `7` «No ha ido al médico», `8` «No tiene acceso a servicio médico», `5` «No le interesa realizarse el estudio», `6` «No tiene dinero» |
| **disparador parcial** | sexo (`sexo`, `sexo_u`) y condición laboral (`h0321` «¿trabajó al menos una hora la semana pasada?», `h0324` posición en la ocupación) |
| **disparador que falta** | **«sin permiso laboral»: no existe.** `prestacion*` da **0 aciertos en los cuestionarios y 0 en el catálogo**; `permiso` da 2+3 aciertos y **todos** son `m0405a` «Le quitaron permisos, le prohibieron algo que a (NOMBRE) le gusta» — disciplina infantil, no prestaciones de trabajo. `h0324` da posición en la ocupación, no si le dan permiso de ausentarse |
| **desenlace que falta** | **«pospone el chequeo hasta el síntoma grave»**: el diferimiento *hasta que aparece la gravedad* no se mide. `A1001*B` dice por qué no se hizo la detección, no que se haya aplazado hasta agravarse |

**Consecuencia que conviene decir con todas sus letras: aun si mesa
depositara mañana el microdato de `adultos`, R4.2 seguiría sin satisfacer.**
Lo que falta es **instrumento**, no sólo adquisición — a diferencia de R4.3.
Notar también que `A1001*B` código `11` es «No tiene **tiempo**», que no es
«no le dan **permiso**»: usar uno por otro sería re-atribuir, exactamente el
riesgo que `ADR-29` ya marcó en esta regla (el patrón conductual tiene dato
mexicano; la atribución causal, no).

---

## R4.5 · `salud.consumo.sellos_precio_similar` — `NO-ENCONTRADO`

> **SI** el producto tiene **sellos** y hay alternativa de **precio similar**
> **ENTONCES** elige el de menos sellos (`modelo-decision-v4_0.md`:530)

**Términos y universo sobre los que se buscó (A.4/A.13), con control
positivo en el mismo comando:**

| término | cuestionarios (8 973 líneas) | catálogos (8 790 filas) |
|---|---:|---:|
| `sello` | **0** | **0** |
| `etiquetado` | **0** | **0** |
| `octagon` | **0** | **0** |
| `advertencia` | **0** | **0** |
| *control:* `farmacia` | 32 | 45 |
| *control:* `medicamento` | 54 | 254 |
| *control:* `necesidad de salud` | 14 | 88 |

Los controles positivos disparan en el mismo comando y sobre los mismos dos
archivos, así que el cero no es un comando que no corrió. Barrido adicional
sobre las 843 etiquetas de `adultos` por `consum|bebida|refresc|alimento|
comida|azúcar|frituras|compra`: lo que devuelve es tratamiento de diabetes,
consumo de **alcohol** (`a1308`–`a1314`), dificultad **para realizar compras**
(`a1702`, módulo de discapacidad) y gasto en oxígeno (`a2006a`–`a2008a`).
**No hay sección de compra de alimentos ni de etiquetado frontal en los cinco
módulos congelados de ENSANUT 2024.** Ni desenlace ni disparador.

**Lo que falta es instrumento**, y no se resuelve con ninguna adquisición
dentro de esta ola. (Que otras olas de ENSANUT hayan levantado etiquetado
frontal queda **fuera del universo declarado** y este acto no lo afirma.)

---

# P2 · Recuento del criterio 2 para `salud` — cuatro columnas

`N5` y `N6` verbatim de `forense/notas/2026-09-03-MAESTRA37-L1-remapeo.md`;
`L1` verbatim de esa misma nota, líneas 24-28; la cuarta columna es este acto.
Por **D9** (firma de mesa, 3/sep/2026) una fuente administrativa que mida
desenlace **Y** disparador cuenta para (ii).

| regla | N5 (encuestas `data/raw`) | N6 (administrativas) | L1 (`descargas_mx`, formulaciones N5) | **L3 (lectura dirigida)** |
|---|---|---|---|---|
| `salud.atencion.leve_sin_imss` | EXISTE-NO-SATISFACE | NO-APLICA | EXISTE-NO-SATISFACE | **EXISTE-NO-SATISFACE** — desenlace literal (`u0201`=12); falta gravedad y automedicación (esta última, excluida por construcción del módulo) |
| `salud.atencion.grave` | **EXISTE-SATISFACE** | NO-APLICA | sin cambio | **EXISTE-SATISFACE** — confirmado con texto (`u0201` público + `u0205` espera + `H0409` internamiento/urgencias) |
| `salud.prevencion.hombre_sin_permiso` | EXISTE-NO-SATISFACE | NO-APLICA | NO-ENCONTRADO | **EXISTE-NO-SATISFACE** — batería `A1001` existe; falta «permiso laboral» y el aplazamiento-hasta-gravedad |
| `salud.adherencia.desabasto_vs_cuidadora` | NO-ENCONTRADO | EXISTE-NO-SATISFACE (Cero Desabasto) | NO-ENCONTRADO | **NO-ACCESIBLE** (desabasto: reactivo exacto `a0313`/`a0314`, microdato ausente) · **NO-ENCONTRADO** (cuidadora: sin ítem) |
| `salud.consumo.sellos_precio_similar` | NO-ENCONTRADO | NO-APLICA | NO-ENCONTRADO | **NO-ENCONTRADO** — 0/0 en los 4 términos, con control positivo |

## Recuento

**`EXISTE-SATISFACE` en `salud`: 1 de 5.** El mismo 1 (`salud.atencion.grave`)
que ya tenía `N5`, ahora sostenido por texto de reactivo y no sólo por
formulación. **No llega a 3.**

> **NO hay `ABRE-CANDIDATO-CON-RESERVA`.** No se redacta lote, no se mide `p`,
> no se toca `L10` ni su cola, no se toca `milpa/**`. El contador de dominios
> abiertos queda en **0 → 0**, y las cargas al motor en **0**.

## Qué falta exactamente, y de qué tipo es

Ésta es la parte accionable, y es distinta de la que `L1` podía dar:

| regla | qué falta | **adquisición o instrumento** |
|---|---|---|
| `salud.adherencia.desabasto_vs_cuidadora` | **el archivo `adultos_ensanut2024_w.stata.stata.zip`** | **ADQUISICIÓN** — el reactivo ya existe y satisface; es la única de las cuatro que puede voltear con una descarga. La rama *cuidadora*, en cambio, es instrumento y no voltea |
| `salud.prevencion.hombre_sin_permiso` | ítem de permiso/prestación laboral **y** el aplazamiento-hasta-gravedad | **INSTRUMENTO** (además del archivo). Con `adultos` en mano seguiría sin satisfacer |
| `salud.atencion.leve_sin_imss` | gravedad del padecimiento; automedicación | **INSTRUMENTO** — y la automedicación es *estructural*: el módulo de utilizadores excluye por diseño a quien no fue atendido |
| `salud.consumo.sellos_precio_similar` | todo: sellos y precio | **INSTRUMENTO** — ENSANUT 2024 no levanta etiquetado frontal en sus cinco módulos |

**Una sola adquisición (`adultos` 2024) llevaría `salud` de 1 a 2, no a 3.**
Las otras tres brechas no las cierra ninguna descarga de esta ola. Si mesa
quiere que `salud` alcance el criterio 2, el camino no es bajar más ENSANUT:
es otro instrumento, u otra ola, o una fuente administrativa que mida
desenlace y disparador bajo D9.

**Sucesor que este acto deja escrito, sin ejecutarlo:** `L3-bis` sobre
`adultos` únicamente, cuando mesa deposite
`adultos_ensanut2024_w.stata.stata.zip` en `descargas_mx` — alta por A.7,
tres capas del curador, doble hash, y re-veredicto de R4.3 y R4.2 contra
microdato. Se espera que R4.3 pase a `EXISTE-SATISFACE` y R4.2 se quede en
`EXISTE-NO-SATISFACE`; que el acto lo confirme o lo refute es su falsador.
