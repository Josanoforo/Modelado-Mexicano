# `CALC-0003-v3` — cara local de `prereg-caja-S6-L16` **v1.3** (ENNViH-1 2002)

**Acto:** `ACTO GEN2-SPECS-SUCESORAS · S6 v1.3 + S12 v1.1`, 8/sep/2026,
**UBUNTU (caja)**, sobre `origin/main = c5b89a9`. Sucede a `CALC-0003-v2`
(`repite_de: CALC-0003-v2`), sellada por `ACTO GEN2-E5-1` con
`VERIFY: REPRODUCE` y 128/128. **Los bytes de `CALC-0003` y de `CALC-0003-v2`
quedan intactos**; en el registro `CALC-0003-v2` pasa a
`SUPERADO→CALC-0003-v3`. Cadena completa: `CALC-0003` (PARO por `MergeError`,
`FP-355`) → `CALC-0003-v2` (SELLADA) → `CALC-0003-v3` (esta).

**Firma de mesa que autoriza la sucesión, verbatim del 8/sep/2026:**
«si hagamos las specs sucesoras..»

---

## 0 · 🛑 La ÚNICA diferencia operativa con `CALC-0003-v2`, declarada y no absorbida

Todo lo demás de esta spec —universo, disparadores, desenlaces, las tres tablas
de clasificación, `P_PUB` y su sensibilidad, el umbral `n < 10`, la pareja de
ponderadores del brazo `bx`, `seed`, réplicas, tolerancia, el filtro de llave
ausente de `c_portad` que introdujo v2, y los **128** `RESULT` con sus **mismos
ids**— es el sellado de `GEN2-E5-1`, sin tocar.

**La diferencia:** el bootstrap **remuestrea LOCALIDADES (`id_loc` de
`c_portad.dta`) dentro de estrato**, no HOGARES (`folio`) dentro de estrato.

**Por qué.** `S6 v1.2` §3.5 afirmó que la unidad primaria de `ENNViH` (la
localidad) *«no está en los archivos»* y de ahí pre-registró conglomerado =
hogar **con reserva declarada de varianza subestimada**. La premisa es falsa:
`ehh02dta_bc/c_portad.dta` —el mismo archivo del que la spec ya tomaba
`estrato`— trae `edo`, `mpio`, `loc` e `id_loc`. Es `FP-351`. `S6 v1.3` §3.5
corrige la premisa, pre-registra **conglomerado = localidad** y **levanta esa
reserva** (y sólo esa: multiplicidad, pareja de ponderadores, coincidencia de
signo, umbral de `n` y la prohibición causal de §3.6 siguen íntegras).

**Qué NO cambia del estimando ni del universo.** `Δ = P_PUB(T=1) − P_PUB(T=0)`
es el mismo; entran exactamente las mismas personas en cada celda; el
ponderador es el mismo; la `seed` (`20260908`) y las réplicas (`2000`) son las
mismas. **Es un cambio de estimador de varianza, y sólo eso.** Los `Δ`
puntuales, las `P`, las `n` y los conteos de `LUGAR` deben salir **idénticos**
a los de `CALC-0003-v2` — y eso es el control de regresión de esta corrida, no
un supuesto: si alguno se mueve, el cambio arrastró algo que no debía y se
reporta como defecto, no como resultado.

**Dirección esperada del efecto sobre los IC, declarada ANTES de correr para
que nadie la lea después como si fuera un hallazgo:** conglomerados más grandes
⇒ intervalos **más anchos**, salvo correlación intraclase nula dentro de
localidad. Que se ensanchen no es noticia; **cuánto**, y qué veredicto cambia
por ello, es lo que §0.3 pre-declara cómo leer.

**Los 14 `RESULT` nuevos.** Son diagnóstico de esta única diferencia y
**ninguno es un `Δ`, un IC ni un veredicto**: `RESULT-CONGLOMERADO-LOCALIDAD`,
`RESULT-CONGLOMERADO-ANIDAMIENTO`, y por cada una de las 6 filas efectivas
`RESULT-<fila>-N-CONGLOMERADOS` y `RESULT-<fila>-N-SIN-CONGLOMERADO`. Los 128
ids de v2 se reproducen tal cual: **142 en total**.

---

## 1 · Cómo se identifica una localidad — y la trampa que la guardia impide

`c_portad.dta` trae **cinco** columnas de geografía además de la llave
(`folio`, `ls`) y de `estrato`: `edo` («ESTADO»), `mpio` («MUNICIPIO»), `loc`
(«LOCALIDAD»), `control` («NO. DE CONTROL DE HOGARES») e `id_loc` («ID
LOCALIDAD»). **El archivo no trae ninguna etiqueta de valor** (`variable_to_label`
vacío), así que ninguna de las dos candidatas se adjudica por etiqueta.

🛑 **`loc` a secas NO sirve como conglomerado.** Bajo la convención
geoestadística de INEGI, `loc` es único **dentro de su municipio**, no a nivel
nacional: usarlo solo colapsaría en un mismo conglomerado localidades de
estados distintos que comparten número, **ensanchando el IC por un artefacto de
codificación y no por diseño**. La llave que identifica una localidad sin
ambigüedad es la compuesta `(edo, mpio, loc)` — o `id_loc`, si resulta ser la
misma partición.

**Llave congelada: `id_loc`. Control: la compuesta `(edo, mpio, loc)`. Y el
control se publica, no se promete.** `RESULT-CONGLOMERADO-LOCALIDAD` emite los
tres conteos —bajo `id_loc`, bajo la compuesta y bajo `loc` a secas— más
estratos, hogares y localidades por estrato, y dice si las dos primeras
particionan igual (`BIYECCION-VERIFICADA`) o no (`DISCREPAN`, en cuyo caso
**manda la compuesta**, `S6 v1.3 §3.5`).

**Anidamiento.** El remuestreo supone hogar ⊂ localidad ⊂ estrato.
`RESULT-CONGLOMERADO-ANIDAMIENTO` publica cuántas localidades cruzan más de un
estrato, cuántos hogares cruzan más de una localidad y cuántas filas traen
`id_loc` nulo. Si el anidamiento se rompe **se reporta y no se inventa uno que
el archivo no tiene**.

**Cobertura por celda.** Una fila cuya localidad no resolviera en el `left-join`
contra `c_portad` entraría al bootstrap con clave `NaN` y **todas las `NaN`
caerían en un solo conglomerado** — el modo de falla silencioso de esta clase
de cambio. `RESULT-<fila>-N-SIN-CONGLOMERADO` lo convierte en número, por fila.

---

## 2 · Qué se abrió ANTES de congelar esta spec, y qué no (A.13)

Declarado con precisión, no omitido, y con el mismo estándar que `CALC-0003-v2`
§0 usó para sus tres filas de `c_portad`:

| qué | cómo | por qué era necesario antes de congelar |
|---|---|---|
| **metadato** de `c_portad.dta` (11 columnas, sus etiquetas y formatos) | `pyreadstat.read_dta(..., metadataonly=True)` | fijar los nombres reales de las columnas de geografía — `loc`/`id_loc` — y comprobar que el archivo **no trae etiquetas de valor** |
| **metadato** de los 8 `.dta` de microdato y los 2 de ponderador | ídem | comprobar que **ninguno** trae ya una columna llamada `id_loc`, `estrato`, `edo`, `mpio` o `loc`: un choque de nombres haría que el `merge` creara sufijos `_x`/`_y` **en silencio**. Resultado: **cero choques en los diez archivos** |
| **observación** de 5 columnas de `c_portad.dta` (`edo`, `mpio`, `loc`, `id_loc`, `estrato`) | lectura completa del miembro | guardia marginal: sin ella, esta spec congelaría un conglomerado sin saber si tiene nulos, si `loc` a secas colapsa, o si el anidamiento se sostiene |

**Ni una variable de disparador (`es09`, `ec01*`) ni de desenlace (`hs01`,
`ce01`, `hs02*`, `ce04*`, `hs08_*`) ni un ponderador se leyó como observación
al redactar esta spec.** Lo que se abrió es geografía de diseño: no contiene
ningún `Δ`, ninguna proporción y ninguna celda del contraste.

**Y lo que sí se sabía ya, dicho con todas sus letras:** esta sesión conoce los
resultados sellados de `CALC-0003-v2` — están publicados en
`forense/notas/2026-09-08-GEN2-E5-1-verificador-y-calc0003v2.md` §2 y en
`data/corrida0/CALC-0003-v2/resultados.json`, en `origin/main`. **No hay
sesión ciega que reclamar aquí y no se reclama.** La garantía que esta spec sí
provee, y que es verificable por el solo orden de los commits en git, es que
**el criterio de lectura de §0.3 se fijó antes de que existiera un solo número
de `v3`**, y que la única diferencia de método está congelada por un hecho de
archivo (`FP-351`) que no depende de ningún desenlace.

---

## 3 · Ventanas, códigos y tablas — heredados de v2, sin cambio

`S6 v1.3` §1 escribe ya `T1 = 0 si es09 == 3` (`FP-349`), de modo que la
**discrepancia que `CALC-0003-v2` §1 tuvo que declarar contra su spec sellada
desaparece**: papel y código coinciden. La autoridad sigue siendo la misma —
`ehh02cb_b3b.pdf` pág. 8 (`1. Si` = 3 972 · `3. No` = 15 832 · total 19 804) y
`ehh02cb_bx.pdf` pág. 49 (`1. Si` = 414 · `3. No` = 1 419 · `8. NS` = 15 ·
total 1 848) — y `RESULT-CODIGOS-SI-NO` la sigue emitiendo.

Ventanas (`RESULT-VENTANAS`), sin cambio: `es09` = **de por vida** (cuestionario
pág. 5) · `ec01*` = **alguna vez** (pág. 10) · `ce01` = **últimas 4 semanas**
(pág. 12) · `hs01` = **últimos 12 meses** (pág. 18). **En las cuatro celdas la
ventana del desenlace no cubre la del disparador: co-ocurrencia, no secuencia.
Ninguna fila de esta corrida sostiene una afirmación causal**, y levantar la
reserva de varianza de §3.5 no toca esta limitación en absoluto.

Las tres tablas de clasificación (A: `iiib_hs`, 11 · B: `p_hs`, 14 · C:
`iiib_ce`/`p_ce`, 14) se heredan verbatim; `CALC-0003-v2` §3 las cotejó contra
el metadato real con **0 desajustes** y esta corrida no reclasifica nada.

---

## 4 · Control de regresión — la guardia que distingue «cambió el IC» de «se rompió algo»

`CALC-0003-v2` está sellada y su `resultados.json` vive en `origin/main`. Por
construcción de §0, **todo lo que no sea `IC-LO` / `IC-HI` / `VEREDICTO` debe
reproducir idéntico**: los ocho `DELTA`, los ocho `DELTA-SENS`, las dieciséis
`P-T1`/`P-T0`, las `N-T1`/`N-T0`, los `N-UNIVERSO`, los cuatro niveles de
`LUGAR` por fila, los `N-PONDERADOR-VALIDO`, `RESULT-JOINS`,
`RESULT-LLAVE-UNICA-*`, `RESULT-DHS-N-EPISODIOS-*` y `RESULT-T2-N-VARIABLES`.

**Se compara explícitamente en la nota de cierre, id por id.** Un `DELTA` que
se moviera sería prueba de que el cambio de conglomerado arrastró algo que no
debía —un `merge` con sufijo, una fila perdida— y **se reporta como defecto,
no como resultado**. La comparación es legítima sin enlace de registro: misma
escala, mismo universo, misma `seed`.

---

## 5 · 🛑 Pre-declaración `B-bis`, congelada ANTES de correr

**Dónde vive y por qué aquí.** El encargo de este acto ordena que `S6 v1.3`
tenga **dos** diferencias con `v1.2` «y ninguna más». La lectura de un
re-corrido concreto no es una cláusula del contrato de pre-registro: por eso
esta pre-declaración vive **en el `CALC`**, congelada en el mismo `COMMIT-1`,
antes de abrir un solo `.dta` para calcular. Su texto es el del encargo
archivado por A.3 (`forense/encargos/2026-09-08-GEN2-SPECS-SUCESORAS.md`),
operado fila por fila.

**Estado de partida, ya público** (`CALC-0003-v2`, conglomerado = hogar):

| fila | `Δ` | IC95 | veredicto v2 |
|---|---|---|---|
| `C1-B3B-FAC3B` (**primaria**) | −0.065961 | [−0.148043, +0.020537] | `NO-DISCRIMINA` |
| `C1-BX-FAC3APX` | +0.000790 | [−0.036578, +0.022008] | `NO-DISCRIMINA` |
| `C1-BX-FAC3BPX` | +0.000148 | [−0.037034, +0.021274] | `NO-DISCRIMINA` |
| `C2-B3B-FAC3B` | +0.032666 | [−0.003639, +0.069743] | `NO-DISCRIMINA` |
| `C2-BX-FAC3APX` | −0.026564 | [−0.088181, +0.032465] | `NO-DISCRIMINA` |
| `C2-BX-FAC3BPX` | −0.027617 | [−0.089011, +0.031167] | `NO-DISCRIMINA` |
| `C3-B3B-FAC3B` | **+0.181865** | **[+0.090029, +0.281877]** | **`CORROBORADA`** |
| `C4-B3B-FAC3B` | **+0.067035** | **[+0.027643, +0.104595]** | **`CORROBORADA`** |

**Las tres reglas de lectura, en este orden de prioridad:**

1. **Si `C1`/`b3b` —la fila primaria, hoy `NO-DISCRIMINA`— CAMBIA DE ESTADO en
   cualquier dirección, ESO es EL hallazgo y se reporta PRIMERO**, antes que
   cualquier fila secundaria, y con la advertencia de que un cambio de estado
   producido por un ensanchamiento de IC no es evidencia nueva sobre la
   conducta: es la misma evidencia medida con la varianza correcta.
2. **Si `C3` y/o `C4` —las dos `CORROBORADA` de v2— conservan su intervalo
   por encima del umbral con el conglomerado correcto, su corroboración es
   SECUNDARIA ROBUSTA** y se reporta como tal.
3. **Si el IC95 de `C3` o de `C4` cruza 0 con el conglomerado correcto, esa
   fila BAJA a `PROPUESTA` y se dice** — sin rescatarla, sin bajar el umbral y
   sin apelar a la definición de sensibilidad.

**Lo que NINGUNA de las tres autoriza.** El veredicto de la **regla** sigue
gobernado por la cláusula de multiplicidad de `S6` §2.5, intacta: **`C1`/`b3b`
decide; una fila secundaria sola es `PROPUESTA con reserva`, nunca
`CORROBORADA` de la regla.** `C3` y `C4` corren sobre `T2` (`ec01*`), que
`S6` §1 declara aproximación de «crónico», **no** de «crónico complejo»: aun
robustas, corroboran «crónico». Y `R4.4` **no se mueve por este `CALC`** —
etiqueta de la propia spec sellada, heredada sin cambio.

**Y lo que se reporta pase lo que pase:** las 6 filas efectivas con sus IC
nuevos y viejos lado a lado, los 14 diagnósticos de conglomerado, y el control
de regresión de §4 completo. **Ningún resultado se omite por incómodo.**

---

## 6 · Qué NO hace

No edita `S6-L16-spec-v1_2.md`, `v1_1`, `v1_0` ni sus sidecars. No edita
`CALC-0003` ni `CALC-0003-v2` — sus bytes y sus sellos quedan intactos. No
reclasifica ninguna institución. No adjudica el ponderador del `bx` (los corre
en pareja). No cambia el universo, el estimando, el umbral de `n`, la `seed`
ni las réplicas. No usa `loc` a secas ni `control`. No mueve el tier de `R4.4`.
No corre 2005/2009 ni el brazo `ENDIREH`. No re-corre `CALC-0001` ni
`CALC-0002`. No sostiene ninguna afirmación causal (§3).

**El primer resultado que produzca este procedimiento es el que se reporta — de
cada celda y de cada brazo, por separado.**
