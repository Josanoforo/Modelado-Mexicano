# `CALC-0003-v2` — cara local de `prereg-caja-S6-L16` **v1.2** (ENNViH-1 2002)

**Acto:** `ACTO GEN2-E5-1 · VERIFICADOR REPARADO + CALC-0003-v2`, 8/sep/2026,
**UBUNTU (caja)**. Sucede a `CALC-0003` (`repite_de: CALC-0003`), congelado por
`ACTO GEN2-E5-0` sobre `origin/main = d8b5f0b` y **PARADO** en `ACTO GEN2-E5`
con `MergeError` contra el dato real (`FP-355`). Los bytes de `CALC-0003`
quedan **intactos**; en el registro pasa a `SUPERADO→CALC-0003-v2`.

## 0 · 🛑 La ÚNICA diferencia con `CALC-0003`, declarada y no absorbida

Todo lo demás de esta spec —universo, variables, filtros, ponderador,
parámetros, `seed`, tolerancia y los **128** `RESULT` declarados, con sus
mismos ids— es el congelado de `GEN2-E5-0`, sin tocar.

**La diferencia:** el medidor **filtra de `c_portad.dta` las filas cuya llave
de join (`folio`, `ls`) está ausente, ANTES de construir la llave.**

**Por qué.** `_llave()` vuelve esas filas `<NA>`; `duplicated` cuenta
`NA == NA` como repetido, y el merge `validate="m:1"` levanta `MergeError`.
Es exactamente lo que paró a `CALC-0003`.

**Qué son, medido en el archivo crudo — no lo que el encargo supuso.** El
encargo de este acto y `FP-355` las llaman «3 filas **totalmente vacías**».
No lo son: filas con las 11 columnas vacías hay **cero**. Son 3 filas
(índices 7321, 7567, 8189 de 8441) que traen **8 de sus 11 columnas con
dato** —`rel`, `reh`, `edo`, `mpio`, `loc`, `control`, `edad`, `id_loc`— y a
las que les faltan exactamente `folio`, `ls` y `estrato`. Se identifican por
la **llave ausente**, que es lo que rompe el join; el rótulo «vacía»
filtraría **cero** filas sobre este archivo y `CALC-0003-v2` habría vuelto a
parar igual que v1.

**Qué cambia del universo declarado.** Nada alcanzable: una fila sin
`folio`/`ls` no puede casar con ninguna fila real de ningún miembro, así que
no estaba en el universo de ninguna celda ni antes ni después — el join la
descartaba por construcción, sólo que levantando en vez de omitiendo. Medido:
`c_portad` pasa de 8441 a **8438** filas y de **2** llaves duplicadas a
**0**. La spec sellada `S6 v1.2` no habla de estas filas.

**Conteo A.13.** Viaja en `RESULT-LLAVE-UNICA-PORTAD`, el `RESULT` de texto
que la spec **ya declaraba**: filas leídas · filtradas · las que entraron al
join. El conjunto de 128 ids no cambia.

**Alcance verificado.** Las **seis** tablas que el medidor usa como lado
derecho de un merge `m:1` se midieron antes de correr: sólo `c_portad` traía
el defecto. `w_b3b` (35 677), `w_bx` (35 677), `iiib_es` (19 804), `p_es`
(1 848) e `iiib_ec` (17 728) tienen **cero** filas sin llave y **cero**
duplicados. No hay una segunda sorpresa esperando en el siguiente merge.

**Spec sellada que gobierna:** `forense/prereg-caja/S6-L16-spec-v1_2.md`,
`sha256 = c1cd3b6367d4edc4d38401e19752adb9656d238a81ae6cff9db11dacaf73da1c`
(íntegra contra su sidecar).

**Qué se abrió:** metadato de los ocho `.dta` + `c_portad.dta` + los dos de
ponderador (`metadataonly=True`), el **cuestionario del Libro IIIB**
(`ehh02q_b3b.pdf`, dentro de `ennvih1_2002_hogar_q`) y los **manuales de
codificación** `ehh02cb_b3b.pdf` (suelto en la raíz) y `ehh02cb_bx.pdf` (dentro
de `ennvih1_2002_hogar_cb`). Ni una observación leída.

---

## 1 · 🛑 El hallazgo que impide una corrida degenerada: **`es09` no tiene código `0`**

`S6 v1.2 §1` congeló: *«`T1 = 1` si `es09 == 1`; `T1 = 0` si `es09 == 0`»*.

**Estos `.dta` no traen ninguna etiqueta de valor** (`variable_to_label` vacío
para todas las variables de interés en los ocho archivos): el **manual de
codificación es la única autoridad sobre los códigos**. Y dice:

| variable | manual · página | códigos verbatim | total |
|---|---|---|---|
| `es09` (b3b) | `ehh02cb_b3b.pdf` **pág. 8** | `1. Si` = 3 972 · `3. No` = 15 832 | 19 804 |
| `es09` (bx) | `ehh02cb_bx.pdf` **pág. 49** | `1. Si` = 414 · `3. No` = 1 419 · `8. NS` = **15** | 1 848 |
| `ce01` (b3b) | `ehh02cb_b3b.pdf` **pág. 21** | `1. Si` = 3 179 · `3. No` = 16 624 | 19 803 |
| `ce01` (bx) | `ehh02cb_bx.pdf` **pág. 56** | `1. Si` = 233 · `3. No` = 1 568 · `8. NS` = 47 | 1 848 |
| `hs01` (b3b) | `ehh02cb_b3b.pdf` **pág. 28** | `1. Si` = 1 062 · `3. No` = 18 737 | 19 799 |
| `hs01` (bx) | `ehh02cb_bx.pdf` **pág. 60** | `1. Si` = 93 · `3. No` = 1 740 · `8. NS` = 15 | 1 848 |

**«No» se codifica `3`, no `0`. El código `0` no existe en ninguna de las tres.**
Corrida verbatim, la regla `es09 == 0` habría seleccionado el **conjunto vacío**
—sin error, sin aviso— y las cuatro celdas de contraste habrían salido
degeneradas: `T1 = 0` vacío ⇒ `P_PUB(T=0)` indefinido ⇒ `Δ` indefinido en las
seis filas. **Este `CALC` congela `T1 = 0` si `es09 == 3`**, y declara la
discrepancia con la spec sellada aquí, sin editarla: la spec dice qué se mide,
el codebook dice con qué códigos, y el segundo no se adivina (prohibición
explícita del encargo). **Elevado a mesa como candidato a `S6 v1.3`.**

**Corroboración independiente de que estos manuales describen ESTOS datos:** los
totales del manual coinciden exactamente con las filas de cada `.dta`
(19 804 / 19 803 / 19 799 / 1 848 / 1 200), y el `8. NS` = **15** de `es09` en el
brazo `bx` reproduce, al caso, los «15 NS/NC en `p_es.dta`» que `v1.1` midió.

`ec01a`…`ec01i_1` (`ehh02cb_b3b.pdf` **pág. 18**): `1. Si`; `T2 = 1` si al menos
una vale `1`. Los nueve nombres reales son los que `S6 §1` ya corrigió
(`ec01h_1`, `ec01i_1` con sufijo).

---

## 2 · Ventanas de referencia, con página — `S6 §3.6` las exigía antes de calcular

Leídas de `ehh02q_b3b.pdf` (cuestionario del Libro IIIB, dentro de
`ennvih1_2002_hogar_q`; extraído con `zipfile-deflate64` — el miembro viene en
**deflate64** y `zipfile` de Python lo rechaza):

| ítem | página | texto verbatim de la ventana | ventana |
|---|---|---|---|
| `ES09` | **5** | «¿Ha tenido algún problema serio de salud **a lo largo de su vida**?» | **de por vida** |
| `EC01` | **10** | «¿**Alguna vez** ha sido usted diagnosticado(a) con (...)?» | **alguna vez** |
| `CE01` | **12** | «En las **últimas 4 semanas**, ¿visitó usted algún hospital, clínica, personal de salud, doctor o curandero, sin haber sido hospitalizado(a)?» | **4 semanas** |
| `HS01` | **18** | «Durante los **últimos 12 meses**, ¿se ha quedado usted internado en algún hospital, clínica, centro de salud o en la casa o consultorio de algún médico, partera o curandero, al menos por una noche?» | **12 meses** |

⚠️ **`S6 §3.6` mandó declararlo «aunque no le guste lo que lea». No gusta, y se
declara:** en **las cuatro celdas** la ventana del desenlace **no cubre** la del
disparador, y la brecha es **mayor** que el ejemplo que la propia spec imaginó
(«`ce01` a 4 semanas contra un `es09` a 12 meses»): `es09` no es de 12 meses,
es **de por vida**.

| celda | disparador | desenlace | brecha |
|---|---|---|---|
| `C1` | `es09` de por vida | `hs01` 12 meses | vida ≫ 12 meses |
| `C2` | `es09` de por vida | `ce01` 4 semanas | vida ≫ 4 semanas |
| `C3` | `ec01*` alguna vez | `hs01` 12 meses | vida ≫ 12 meses |
| `C4` | `ec01*` alguna vez | `ce01` 4 semanas | vida ≫ 4 semanas |

Las seis filas miden **co-ocurrencia, no secuencia**. Ninguna sostiene una
afirmación causal. Va congelado en `spec.yaml`
(`parametros.ventanas`) y se emite como output (`RESULT-VENTANAS`) para que
quede en `resultados.json`, no sólo en la prosa.

---

## 3 · Las tres tablas de clasificación — **verificadas contra el `.dta`, 0 desajustes**

`S6 §2.1` congeló tres tablas y ordenó: *«si caja encuentra que una etiqueta no
corresponde a su clase, lo reporta y NO reclasifica»*. Cotejadas variable por
variable contra el metadato real:

| tabla | archivo | declaradas | reales con el prefijo | declaradas-y-ausentes | reales-sin-clasificar |
|---|---|---|---|---|---|
| A | `iiib_hs.dta` | 11 | 11 | **0** | **0** |
| B | `p_hs.dta` | 14 | 14 | **0** | **0** |
| C (b3b) | `iiib_ce.dta` | 14 | 14 | **0** | **0** |
| C (bx) | `p_ce.dta` | 14 | 14 | **0** | **0** |

Las etiquetas coinciden verbatim, erratas incluidas (`hs02b` «INTERNADO **IMMS**»
en Tabla A, `hs02f` «INTERNADO **CON**sultorio PRIVADO»). Las de Tabla C difieren
en redacción entre `iiib_ce` y `p_ce` (`ISSSTE`/`ISSTE`,
`ENFERMERA/PARAMEDICO`/`ENFERMERA`): **no importa** — `S6 §0.4` ordena clasificar
por `variable_id`, nunca por etiqueta, y los `variable_id` son idénticos.
**Ninguna reclasificación. Cero.**

---

## 4 · Llaves — dónde está exactamente el join que rompe

`S6 §3.4` exigió normalizar `folio`/`ls` a entero. El metadato dice **dónde**:

| archivo | tipo de `folio` |
|---|---|
| los ocho `.dta` de microdato · `c_portad.dta` | `%9.0g` / `%10.0g` — **numérico** |
| `ehh02w_b3b.dta` · `ehh02w_bx.dta` (ponderadores) | **`%8s` — CADENA** |

El único join en riesgo es **microdato × ponderador**: numérico contra cadena da
**0 filas y ningún error**. Los joins microdato × microdato son numérico contra
numérico. La normalización se aplica igual a todos (barata) y el medidor
**publica cuántas filas entraron y cuántas resolvieron en cada join**
(`RESULT-JOIN-*`), que es la guardia que convierte el bug en un número visible.

---

## 5 · Dos asimetrías entre brazos que `S6` no nombra, declaradas aquí

1. **El filtro de motivo de `D-HS` no existe en el brazo `bx`.** `S6 §2.2` define
   el universo como `hs01 == 1` **y** ≥1 episodio con `hs08_1a` o `hs08_1e` en
   `iiib_hs1.dta`. **No hay `p_hs1.dta`** en el libro proxy (verificado: los 27
   miembros de `ehh02dta_bx/` no incluyen ninguno). El brazo `bx` de `C1` corre,
   por fuerza, **sin filtro de motivo** — universo `hs01 == 1` a secas. Se
   declara y se rotula en la fila (`RESULT-C1-BX-*-FILTRO`), no se disimula
   comparando dos universos distintos como si fueran uno.
2. **`p_ec.dta` no existe** — confirma `S6 §1`: `T2` no tiene brazo `bx`, y su
   ausencia es ausencia de instrumento, no `NO-ESTIMABLE`.

---

## 6 · Ponderadores — la pareja, y por qué la etiqueta no la resuelve

`ehh02w_bx.dta` trae `fac_3a_px`, `fac_3b_px` y `fac_4_px` con la **misma
etiqueta**: «FACTOR DE EXPANSIÓN LIBRO PROXY». **La etiqueta no distingue entre
los tres** — que es exactamente por lo que `S6 §3.2` mandó correr la pareja en
vez de adjudicar. Confirmado, no supuesto. `fac_4_px` no entra (§3.2 punto 4).
`b3b` usa `fac_3b` («FACTOR DE EXPANSIÓN LIBRO 3B»), único en su archivo.

**Regla congelada (S6 §3.2):** el veredicto del brazo `bx` **sólo cuenta si
`fac_3b_px` y `fac_3a_px` coinciden en signo**; si discrepan, `NO-ESTIMABLE por
ponderador indeterminado` y la regla se lee de `b3b`.

⚠️ **`S6 §3.5` dice que la localidad «no está en los archivos». Está.**
`c_portad.dta` —el mismo archivo del que la spec toma `estrato`— trae **`loc`
(«LOCALIDAD»)** e **`id_loc` («ID LOCALIDAD»)**. **No se usa**: el diseño
pre-registrado es «conglomerado = hogar (`folio`), estrato = `c_portad.estrato`,
IC95 por bootstrap de hogares dentro de estrato», y cambiarlo aquí sería
re-pre-registrar la varianza después de mirar. Se declara el hecho y se conserva
la reserva de §3.5 (el IC por hogar subestima la varianza) **tal cual**, con la
nota de que una `v1.3` podría levantarla sin descargar nada.

---

## 7 · `zipfile-deflate64` — declarada, con su alcance real

`S6 §6` la marca como dependencia material. **Precisión medida:** los 148
miembros de `ehh02dta_all.zip` y los 11 de `ehh02w_all.zip` están en **deflate
normal** (`compress_type = 8`); el **cálculo no la necesita**. La necesitan
`ehh02q_all.zip` y `ehh02cb_all.zip` (`compress_type = 9`), que es de donde
salieron §1 y §2 — y eso ya ocurrió, aquí. Se declara igual, con el nombre de
import correcto (`zipfile_deflate64`), porque el encargo la nombra y porque
`ejecucion.json` debe registrar si la caja de `GEN2-E5` la tiene.

---

## 8 · Qué NO hace

No abre microdato. No calcula. No edita `S6-L16-spec-v1_2.md` ni su sidecar. No
reclasifica ninguna institución. No adjudica el ponderador del `bx`. No usa
`loc`/`id_loc`. No mueve el tier de `R4.4`. No corre 2005/2009 ni el brazo
`ENDIREH`.

**El primer resultado que produzca este procedimiento es el que se reporta — de
cada celda y de cada brazo, por separado.**
