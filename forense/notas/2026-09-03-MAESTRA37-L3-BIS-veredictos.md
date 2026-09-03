# MAESTRA37-L3-BIS · P1/P2 — cinco veredictos A.4 sobre el universo v2 (COMMIT-2)

Universo: el congelado por `COMMIT-1` en
`forense/notas/2026-09-03-MAESTRA37-L3-BIS-universo.md` — 8 636 filas del
inventario `v1_1` bajo `ENSANUT2024-v2026-09-01/`, 19 598 filas de los 38
catálogos v2, 11 de los 16 PDF de cuestionario transcritos. Vocabulario A.4
verbatim de `.claude/commands/mapea.md` §4: `EXISTE-SATISFACE`,
`EXISTE-NO-SATISFACE`, `NO-ENCONTRADO`, `NO-ACCESIBLE`.

**Ninguna línea de `forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md` se
edita.** Los sellos de L3 quedan VENCIDOS EN ALCANCE (A.10), no refutados. Este
acto los re-sella contra el universo nuevo y cita cada uno verbatim.

---

## 0 · El hallazgo que gobierna tres de los cinco veredictos

**El portal republicó el microdato pero NO cambió el instrumento.** Diff de
etiquetas de variable entre el censo de julio (`data/l3-ensanut2024-catalogos-v1_0.tsv`)
y el de septiembre, módulo por módulo:

| módulo | vars julio | vars sept | sólo julio | sólo sept | etiquetas distintas |
|---|---:|---:|---:|---:|---:|
| utilizadores | 122 | 120 | 2 | **0** | **0** |
| hogar | 204 | 203 | 1 | **0** | **0** |
| integrantes | 261 | 258 | 3 | **0** | **0** |
| adultos | 843 | 841 | 2 | **0** | **0** |
| menores | 484 | 482 | 2 | **0** | 2 |

Las «sólo julio» son `Variables en el archivo de trabajo` (renglón de encabezado
del xlsx, no una variable), `fech_nac` y `h0304`/`h0304d` — retiros, no altas.
Las 2 «etiquetas distintas» de menores (`m0112e`, `m0112g`) **no son cambios de
contenido**: la extracción de julio arrastró bytes basura al final
(`…etapas de desarroF51�`) y la de septiembre no. Verificado carácter a carácter.

**Consecuencia:** para toda regla cuyo juicio se apoye en el texto de esos cinco
módulos, el universo **no cambió**, y el sello de L3 se **confirma, no se
re-escribe**. Lo que sí cambió es (a) que el microdato de `adultos` ya está
accesible y (b) que entraron componentes que L3 nunca vio — `etiquetado` entre
ellos.

---

## R4.1 · `salud.atencion.leve_sin_imss` — `EXISTE-NO-SATISFACE` · **CONFIRMADO SIN CAMBIO**

L3 (verbatim): *«`EXISTE-NO-SATISFACE` […] desenlace literal (`u0201`=12); falta
gravedad y automedicación (esta última, excluida por diseño del módulo)»*.

`utilizadores` y `hogar` tienen **0 variables nuevas y 0 etiquetas distintas**
entre julio y septiembre. El desenlace sigue siendo `u0201` código `12`
«Consultorios pertenecientes a farmacias / Farmacias con consultorio médico»; el
disparador sigue siendo `u0202b` código `10` «Ninguno» / `uh0310_m`. Las dos
faltas que L3 escribió siguen exactamente donde estaban: **«leve-moderado» no se
pregunta** y **la automedicación está excluida por construcción** del módulo
(`u0103`=«No» → *Fin de la entrevista*).

**Veredicto nuevo = veredicto de L3.** No se re-escribe. Nada en v2 lo mueve.

## R4.4 · `salud.atencion.grave` — `EXISTE-SATISFACE` · **CONFIRMADO SIN CAMBIO**

L3 (verbatim): *«`EXISTE-SATISFACE` — confirmado con texto (`u0201` público +
`u0205` espera + `H0409` internamiento/urgencias)»*.

Mismo argumento: cero cambios de texto en `utilizadores` y `hogar`. `H0409` sigue
midiendo la **intensidad de atención que el episodio requirió** (internamiento /
urgencias) y no imputando gravedad por el nombre del padecimiento — que es la
razón por la que R4.4 se sostiene y R4.1 no.

**Veredicto nuevo = veredicto de L3.** Es el único `EXISTE-SATISFACE` que salud
traía desde N5.

## R4.2 · `salud.prevencion.hombre_sin_permiso` — `EXISTE-NO-SATISFACE` · **CONFIRMADO, ahora con microdato**

L3 (verbatim): *«`EXISTE-NO-SATISFACE` — batería `A1001` existe; falta «permiso
laboral» y el aplazamiento-hasta-gravedad»*. Y su consecuencia escrita: *«aun si
mesa depositara mañana el microdato de `adultos`, R4.2 seguiría sin satisfacer»*.

**Mesa depositó el microdato. La predicción de L3 se cumple.** Sobre las **841
variables** del `.dta` abierto (`adultos_ensanut2024_w.dta`, 12 924 personas):

- La batería existe: **20 variables `a1001*`** — `a1001a`…`a1001j` «Durante los
  últimos 12 meses, un médico u otro profesional de la salud le realizó…» con su
  par `a1001*b` «¿Por qué no le realizaron la detección?».
- **«Sin permiso laboral» sigue sin existir.** Barrido sobre los 38 catálogos v2
  (19 598 filas) y los 11 cuestionarios v2, con control positivo en el mismo
  comando:

  | término | catálogos | cuestionarios |
  |---|---:|---:|
  | `permiso` | 2 | 0 |
  | `prestacion` | **0** | **0** |
  | `incapacidad` | **0** | **0** |
  | `aguinaldo` | **0** | **0** |
  | *control:* `medicamento` | 216 | 0 |
  | *control:* `farmacia` | 86 | 3 |
  | *control:* `diabetes` | 66 | 0 |

  Los 2 aciertos de `permiso` son los mismos que L3 encontró: `d0901a`
  (adolescentes) y `m0405a` (menores), ambos *«Le quitaron permisos, le
  prohibieron algo que le gusta»* — castigo infantil en el módulo de violencia.
  `vacaciones` da 65 aciertos y **ninguno es prestación laboral**: son la
  categoría de gasto `H0605A*` código `10` «Vacaciones o en entretenimiento como
  ir al cine, libros, museos, conciertos».
- **El aplazamiento-hasta-gravedad tampoco existe.** Barrido sobre las 841
  etiquetas del `.dta` por `pospon|aplaz|postergo|hasta que se agrav|espero a que`:
  **0 variables.**

**Lo que falta es INSTRUMENTO, y ahora está probado contra el archivo, no
inferido de su ausencia.** Ésta es la diferencia real que este acto aporta sobre
R4.2: L3 lo dedujo del catálogo; aquí se verificó con las 841 variables del
microdato en la mano.

## R4.3 · `salud.adherencia.desabasto_vs_cuidadora` — desabasto: **`NO-ACCESIBLE` → `EXISTE-SATISFACE`** · cuidadora: `NO-ENCONTRADO` sin cambio

L3 (verbatim): *«`NO-ACCESIBLE` (desabasto: reactivo exacto `a0313`/`a0314`,
microdato ausente) · `NO-ENCONTRADO` (cuidadora)»*, y *«Lo que falta aquí es
adquisición, no instrumento»*.

**La adquisición ocurrió (A1, PR #518) y el reactivo cumple lo que L3 anticipó.**
Medido sobre el microdato abierto, 12 924 personas:

| | reactivo · código | n |
|---|---|---:|
| **desenlace, diabetes §3** | `a0313` «En los últimos seis meses ¿Ha suspendido algún(os) de los medicamentos **más de una vez a la semana**?» | Sí **337** · No 1 150 · (no aplica 11 437) |
| **disparador, misma persona** | `a0314` «¿Cuál fue la **causa principal** de haber dejado de tomar sus medicamentos?» | **337 de 337** responden |
| **desenlace, hipertensión §4** | `a0405b` «¿Por cuánto tiempo ha dejado de tomar el medicamento?» (1 día … 1 mes o más) | **679** |
| **disparador, misma persona** | `a0405c`, mismos códigos de causa | **679 de 679** responden |

Códigos que operacionalizan el antecedente, sumando las dos secciones:

- **desabasto** (`a0314`=5 ∨ `a0405c`=5, «No le surtieron los medicamentos en la
  unidad médica»): **39 personas**
- **gasto de bolsillo** (`a0314`=7 ∨ `a0405c`=8, «No tuvo dinero para
  comprarlo(s)»): **99 personas**
- desabasto en farmacia (`…`=6, «No encontró el medicamento en la farmacia»): 18

**Desenlace y disparador en la misma persona, con cero pérdida condicional
(337/337, 679/679).** El reactivo pregunta literalmente lo que la definición
pide y además atribuye la causa. → **`EXISTE-SATISFACE`.**

**Reserva escrita, y no es menor.** *Que la variable exista no es que la `n`
alcance.* Las celdas realizadas del brazo que la regla predice son **39**
(desabasto) y **99** (dinero). A.4 juzga el instrumento, no la potencia, así que
el veredicto no cambia; pero cualquier medición de `p` sobre esta regla arranca
con celdas de dos dígitos y eso hay que decidirlo antes, no después.

**La rama cuidadora sigue `NO-ENCONTRADO`, ahora sobre un universo 2,2× mayor.**
`adherenc` da **0 en los 38 catálogos y 0 en los 11 cuestionarios**. `cuidador`
da 3 + 2 aciertos y son **los mismos tres ajenos que L3 ya había descartado**:
`m0103_id` (rol del informante), `a0819f` y `d0325a` («Del recuerdo de su mamá,
cuidadora o informante» — fuente de un dato de peso al nacer). `apoyo` da 82
aciertos y **todos son programas sociales** (`h0601a`–`h0601m`: LICONSA, pensión
de adultos mayores, despensas DIF, becas Benito Juárez…), no apoyo familiar a la
adherencia. La rama contrastiva —la que hace falsable a la regla, porque opone
estructura a G5— **sigue sin instrumento incluso con `adultos` en la mano**.

## R4.5 · `salud.consumo.sellos_precio_similar` — **`NO-ENCONTRADO` → `EXISTE-NO-SATISFACE`**

L3 (verbatim): *«`NO-ENCONTRADO` — 0/0 en los 4 términos, con control
positivo»*, y *«No hay sección de compra de alimentos ni de etiquetado frontal
en los cinco módulos congelados»*.

**Ese cero era del universo de julio, y v2 lo rompe.** El módulo
`etiquetado_ensanut2924_w` (141 variables, 578 filas de valor, 14 páginas de
cuestionario) es un instrumento de etiquetado frontal completo. `sello` pasa de
**0/0** a **19 aciertos en catálogo y 24 en cuestionarios**; `etiquetado frontal`
de 0/0 a 1/2.

Lo que sí mide, con el texto a la vista:

| | reactivo · código |
|---|---|
| **desenlace, conducta declarada** | `eti27` «Piense en la última vez que fue de compras y uno de los productos que normalmente consume tenía algún **sello de advertencia** ¿Qué hizo con ese producto?» — `1` **«Lo compró igual»** · `2` **«Compró un producto similar, pero con menos sellos de exceso»** · `3` «Compró un producto similar sin sellos de exceso» · `4` «Compró menos cantidad…» · `5` «No lo compró» |
| **desenlace, regla declarada** | `eti25` «Al momento de realizar sus compras, al ver los sellos de advertencia, usted:» — `1` «Compara la cantidad de sellos y **elige el que tiene la menor cantidad**» · `2` «Prefiere elegir alimentos sin sellos» · `4` «Le es indiferente» |
| **desenlace, uso declarado** | `eti21` «¿Usted utiliza los sellos de "EXCESO" para **decidir la compra**…?» (`1` Sí / `2` No / `3` No está haciendo las compras) |
| **disparador «tiene sellos»** | el enunciado de `eti27` lo fija; `eti04` «¿Me puede decir si ha visto estos sellos?»; `eti33a`–`eti33e` ordenan los cinco sellos por importancia en la decisión de compra |
| **razón del desenlace** | `eti28` «¿Por qué?» — `3` «Por la cantidad de sellos» · `5` **«Costo»** · `2` «Hábito/le gusta/antojo» |
| **criterio de compra** | `ETI32A/B/C` «¿en qué se fija para decidirse?» — `2` «Número de sellos de advertencia» · `4` **«Precio»** |

Los códigos `eti27`=1 vs `eti27`=2/3 son **exactamente las dos ramas de la
regla**: *«compra igual»* frente a *«elige el de menos sellos»*, en la misma
persona y sobre un episodio real.

**Por qué NO llega a `EXISTE-SATISFACE`, y es una sola cosa:**

> **«Alternativa de precio similar» — la condición que hace falsable a la regla —
> no se establece en ninguna parte.**

- `eti27` dice «producto **similar**», sin calificar en qué. No dice precio
  similar, y el entrevistado no informa el precio de ninguno de los dos.
- `eti06`/`eti07` («¿Cuál de los cuatro productos compraría?», productos A–D)
  parecen una tarea de elección que podría fijar el precio, pero el cuestionario
  instruye *«ENTREVISTADOR/A **MUESTRE LAS IMÁGENES** y espere la respuesta»* y
  **no enuncia precio alguno**: no hay control de precio ni variación medida.
- `precio` aparece **4 veces en 19 598 filas de catálogo y 1 en los
  cuestionarios**, y las cuatro son el mismo código: `ETI32A/B/C` = `4`
  «Precio», es decir **precio como criterio autodeclarado**, no como atributo
  del sustituto disponible. Igual `eti28`=5 «Costo».

El `PORQUE` de la regla es **«el precio domina sobre la información»**: sin el
precio del sustituto no se puede separar *«eligió menos sellos porque leyó el
sello»* de *«eligió menos sellos porque además era más barato»*. Usar `eti28`=5
o `ETI32A`=4 como si fueran «alternativa de precio similar» sería
**aproximación**, y por la regla de honestidad congelada en `COMMIT-1` eso es
`EXISTE-NO-SATISFACE`, no `SATISFACE`.

**Lo que falta es INSTRUMENTO, y es pequeño:** un ítem de precio (del producto
con sello y del sustituto) o una tarea de elección con precio enunciado. **R4.5
es hoy la brecha más corta de las cuatro que no cumplen.**

---

## Adjudicación regla ↔ componente (las ocho altas de A1 §5.1)

A1 asentó ocho altas bajo `N36` *«porque el alta exige una necesidad
existente»*, declarando que no afirmaba que sirvieran a R4.3 y dejando la
adjudicación a este acto. Con texto a la vista:

| componente dado de alta por A1 | regla a la que sirve | por qué |
|---|---|---|
| **etiquetado** | **R4.5** `salud.consumo.sellos_precio_similar` | `eti21`/`eti25`/`eti27`/`eti33*` miden el desenlace de la regla; es el único componente que la toca |
| **actividad física** | **ninguna** de R4.1–R4.5 | mide conducta de ejercicio; ninguna regla de §3.4 la condiciona ni la predice. *(El encargo la sugería como «apoyo» de R4.2: no lo es — no contiene permiso laboral ni aplazamiento; ver R4.2 arriba.)* |
| antropometría | ninguna | medición física (peso, talla), no decisión |
| frecuencias (`frec_*`) | ninguna | frecuencia de consumo de alimentos; podría servir a una regla de nutrición que el modelo **no tiene** |
| rec24h | ninguna | recordatorio de 24 h; misma razón |
| lactancia | ninguna | ninguna regla de §3.4 la menciona |
| plomo | ninguna | biomarcador |
| sangre / micronutrimentos | ninguna | biomarcador |

**El componente que sí sirve a R4.3 no está entre las ocho altas: es `adultos`**,
que A1 registró como payload pero cuyo alta de curador no era nueva (`N36` ya
existía para R4.3). La adjudicación queda hecha: **1 de 8 altas tiene regla
(etiquetado→R4.5); 7 de 8 no la tienen** y su `clasificacion_relacion =
CANDIDATA` es correcta y se queda.

---

# P2 · Recuento del criterio 2 para `salud` — cinco columnas

`N5`, `N6` y `L1` verbatim de `forense/notas/2026-09-03-MAESTRA37-L1-remapeo.md`;
`L3` verbatim de `forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md`; la quinta
es este acto. Por **D9** una fuente administrativa que mida desenlace **Y**
disparador cuenta para (ii).

| regla | N5 (encuestas `data/raw`) | N6 (administrativas) | L1 (`descargas_mx`, formulaciones N5) | L3 (julio, 5 módulos) | **L3-BIS (v2, 38 módulos)** |
|---|---|---|---|---|---|
| `salud.atencion.leve_sin_imss` | EXISTE-NO-SATISFACE | NO-APLICA | EXISTE-NO-SATISFACE | EXISTE-NO-SATISFACE | **EXISTE-NO-SATISFACE** — confirmado sin cambio (0 diffs de texto) |
| `salud.atencion.grave` | **EXISTE-SATISFACE** | NO-APLICA | sin cambio | **EXISTE-SATISFACE** | **EXISTE-SATISFACE** — confirmado sin cambio |
| `salud.prevencion.hombre_sin_permiso` | EXISTE-NO-SATISFACE | NO-APLICA | NO-ENCONTRADO | EXISTE-NO-SATISFACE | **EXISTE-NO-SATISFACE** — confirmado contra las 841 variables del microdato |
| `salud.adherencia.desabasto_vs_cuidadora` | NO-ENCONTRADO | EXISTE-NO-SATISFACE | NO-ENCONTRADO | NO-ACCESIBLE (desabasto) + NO-ENCONTRADO (cuidadora) | **EXISTE-SATISFACE** (desabasto, 337/337 y 679/679) · **NO-ENCONTRADO** (cuidadora) |
| `salud.consumo.sellos_precio_similar` | NO-ENCONTRADO | NO-APLICA | NO-ENCONTRADO | NO-ENCONTRADO | **EXISTE-NO-SATISFACE** — módulo `etiquetado`; falta «precio similar» |

## Recuento

> **`EXISTE-SATISFACE` en `salud`: 2 de 5** (`salud.atencion.grave` y
> `salud.adherencia.desabasto_vs_cuidadora` rama desabasto). Era 1.
> **No llega a 3.**

> **NO hay `ABRE-CANDIDATO-CON-RESERVA`.** No se redacta lote, no se mide `p`,
> no se toca `L10` ni su cola, no se toca `milpa/**`, no se da de alta ninguna
> necesidad. Dominios abiertos **0 → 0**; cargas al motor **0**.

## El techo de L3: VENCIDO EN ALCANCE, y su predicción se cumplió

L3 escribió: *«Una sola adquisición (`adultos` 2024) llevaría `salud` de 1 a 2,
no a 3»*. Ese techo se midió sobre cinco módulos de julio y por eso queda
**VENCIDO EN ALCANCE** (A.10). Pero al re-medirlo sobre un universo **3,4× mayor**
(5 → 38 módulos con catálogo) **da lo mismo: salud pasó de 1 a 2, y no a 3.**
El falsador que L3 dejó escrito —*«se espera que R4.3 pase a EXISTE-SATISFACE y
R4.2 se quede en EXISTE-NO-SATISFACE»*— se **corrobora en sus dos mitades**.

**Lo que este acto refuta es la predicción de dirección**, escrita antes de
mirar: *«si etiquetado levanta sellos frontales × decisión de compra, R4.5 puede
pasar a EXISTE-SATISFACE y salud llegar a 3»*. El módulo `etiquetado` **sí**
levanta sellos frontales × decisión de compra —eso era correcto— y aun así R4.5
**no** satisface, porque la regla no pide sellos × compra: pide sellos × compra
**a precio similar**, y el precio del sustituto no se levanta.

**Techo nuevo, derivado:**

> **Ninguna descarga de ENSANUT 2024 lleva `salud` a 3.** Los 125 payloads de v2
> —incluido el instrumento de etiquetado frontal completo, que era la carta más
> prometedora— dejan el dominio en **2 de 5**. Las tres brechas restantes son de
> **instrumento**, no de adquisición, y ya no hay archivo de esta encuesta que
> las cierre.

## Qué falta exactamente, y de qué clase

| regla | qué falta | clase | ¿lo cierra una descarga? |
|---|---|---|---|
| `salud.consumo.sellos_precio_similar` | **un ítem de precio**: el del producto con sello y el del sustituto, o una tarea de elección con precio enunciado | **INSTRUMENTO** | **No** — pero es la brecha más corta: un ítem, no un módulo |
| `salud.atencion.leve_sin_imss` | gravedad del padecimiento; automedicación | **INSTRUMENTO** — y la automedicación es *estructural*: el módulo de utilizadores excluye por diseño a quien no fue atendido | No |
| `salud.prevencion.hombre_sin_permiso` | ítem de permiso/prestación laboral **y** el aplazamiento-hasta-gravedad | **INSTRUMENTO** — verificado contra las 841 variables, no inferido | No |
| `salud.adherencia.…` rama cuidadora | apoyo de un cuidador familiar a la adherencia | **INSTRUMENTO** — `adherenc` 0/0 sobre 38 módulos | No |

Si mesa quiere que `salud` alcance el criterio 2, el camino ya no es bajar más
ENSANUT: es **otro instrumento, otra ola, o una fuente administrativa que mida
desenlace y disparador bajo D9**. Con una diferencia útil respecto de lo que L3
podía decir: **la brecha más barata es un solo ítem de precio en R4.5.**
