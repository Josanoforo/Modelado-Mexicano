# `CALC-0002` — cara local de `prereg-caja-S13`, **ruta (c)** del encargo

**Acto:** `ACTO GEN2-E5-0 · SPECS EJECUTABLES`, 8/sep/2026, **UBUNTU (caja)**,
sobre `origin/main = d8b5f0b`.

**Spec sellada que gobierna:** `forense/prereg-caja/S13-R10-3-spec-v1_0.md`,
`sha256 = c41235b804b0834881b7d3467e25ab0b74946fc03ba14245918e9c7a2e69a515`
(íntegra contra su sidecar). **No se escribe `S13 v1.1`** — ver §1.

**Qué se abrió:** sólo **metadato** de los tres `.dta`
(`pyreadstat.read_dta(..., metadataonly=True)`). Ni una observación leída.

---

## 1 · La ruta: **(c)**, y por qué — con el codebook citado

El encargo autorizó tres rutas y exigió reportar cuál y por qué:

> «(a) Confirmar en los codebooks de las tres olas si existe desenlace comparable
> al de la corrida 2004 …; (b) si existe: escribir **S13 v1.1** …; (c) si no:
> `spec.yaml` contra v1.0 con `veredicto_D2h: NO-CONSTRUIBLE` y solo outputs
> descriptivos pre-registrados.»

**Desenlace de la corrida 2004** (leído en la nota de `LOTE-LAPOP`,
`forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-L18-resultados.md`): **`aoj1`**,
«¿Denunció el hecho a alguna institución?», códigos `1 Sí · 2 No lo denunció ·
8 NS/NR · 9 Inap`; el falsador midió el **silencio** (`aoj1 = 2`) sobre 266
víctimas con `aoj1` válido.

**Resultado del paso (a), contra el codebook real de cada ola** (no contra el
inventario — que es lo que `S13 §0.2` sólo pudo hacer):

| ola | archivo | `aoj1` | familia `aoj*` presente | familia `vic*` presente |
|---|---|---|---|---|
| 2019 | `Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta` | **AUSENTE** | `aoj11`, `aoj12`, `aoj22new` | `vic1ext`, `vic1exta`, `vicbar4a`, `vicbar7`, `vicbar7f` |
| 2021 | `MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta` | **AUSENTE** | `aoj11`, `aojg2n`, `aojg3n1` | `vic1ext` |
| 2023 | `MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta` | **AUSENTE** | `aoj11`, `aoj12` | `vic1ext` |

**Barrido por etiqueta** (`denunc|report…`) sobre las etiquetas de variable de
las tres olas: **0 aciertos**. **Control positivo del barrido, exigido por A.13:**
las tres olas traen etiqueta **en el 100 % de sus variables** — `221/221`,
`262/262`, `195/195`, en español (p. ej. `aoj11` = «Percepción de inseguridad en
el barrio»). El cero **no** es un archivo sin etiquetas leído como vacío.
**Archivos examinados: 3. Variables examinadas: 678.**

**Ruta (c).** No existe desenlace de denuncia en ninguna de las tres olas, ni
bajo `aoj1` ni bajo otro nombre localizable en el codebook completo.
`veredicto_D2h: NO-CONSTRUIBLE`. **`S13 v1.1` no se escribe** — la ruta (b) no
se dispara, y escribirla habría sido inventar un desenlace sin mandato de mesa
(el `Camino A` que `S13 §0.2` dejó declarado y no ejecutado).

---

## 2 · Lo que sí se resolvió del codebook (`S13` lo dejó abierto)

**`S13 §1` dejó pendiente: «Dirección de las escalas `b18`/`aoj12`/`b10a` no
confirmada sin codebook para las olas nuevas».** Confirmada — las tres olas **sí**
traen etiquetas de valor, a diferencia de la de 2004:

| variable | etiquetas de valor (verbatim) | dirección congelada |
|---|---|---|
| `aoj11` | `1 Muy seguro(a) · 2 Algo seguro(a) · 3 Algo inseguro(a) · 4 Muy inseguro(a)` | inseguridad = `{3,4}` |
| `aoj12` | `1 Mucho · 2 Algo · 3 Poco · 4 Nada` (confianza en que castiguen) | desconfianza = `{3,4}` |
| `b18` | `1 Nada … 7 Mucho` (confianza en la policía) | desconfianza = `{1,2,3}` (mitad inferior) |
| `vic1ext` | `1 Sí · 2 No` | filtro de universo = `1` |

**Faltantes:** las tres olas usan **missing extendidos de Stata** — `a` = No sabe,
`b` = No responde, `c` = No aplica. `pyreadstat.read_dta` los entrega como `NaN`
sin `user_missing=True`; se declara para que nadie los lea como códigos válidos.

**`S13 §3` dejó pendiente: «UPM/estrato no confirmados … para ninguna de las tres
olas».** Confirmados: **`upm`** («Unidad Primaria de Muestreo» / «Unidad de
muestreo primaria») y **`estratopri`** («Estrato Primario» / «Región»,
`101 Norte · 102 Centro Occidente · 103 Centro · 104 Sur`) **existen en las
tres**.

⚠️ **La trampa de `S13 §3`, confirmada en LOS DOS SENTIDOS.** La spec avisó que
`weight1500` trae nombre de peso y etiqueta de estrato. El codebook lo confirma
**y añade el reflejo inverso**:

| variable | ola | el NOMBRE sugiere | la ETIQUETA dice | qué es |
|---|---|---|---|---|
| `weight1500` | 2021 | peso | «Estratos de muestra» | **no se usa para ponderar** |
| `strata` | 2021, 2023 | estrato | «**Peso estandarizado**» | **no se usa para estratificar** |

Ponderador usado: **`wt`** en las tres («Peso del país» en 2019, «Peso de la
muestra» en 2021/2023).

---

## 3 · Lo único que este `CALC` mide (`S13 §2`, Camino B)

El **marginal de `INDICE_CONTEXTO`** (proporción `ALTO`) sobre el subuniverso
`vic1ext = 1`, **una ola a la vez, nunca agrupadas**, con IC95. `S13 §2` es
explícita en que **este marginal NO dispara el `se_mueve_si` de D2-h** y **no
decide si `R10.3` discrimina**: es el antecedente sin su desenlace.

`INDICE_CONTEXTO` = número de indicadores en dirección de inseguridad/
desconfianza entre `aoj11`, `b18`, `aoj12`; **`ALTO` = 2 o 3 de 3**, `BAJO` =
0 o 1 de 3 (`S13 §1`, idéntico a `S8 §3`).

⚠️ **2021 sale `NO-ESTIMABLE-INDICE-INCOMPLETO`, declarado ahora.** `aoj12` está
ausente en 2021 (confirmado arriba, ya conocido desde `S8 §0.2`). El corte
pre-registrado es «2 o 3 **de 3**»: con dos indicadores no existe, y **fabricar
un corte de 2 sería re-pre-registrar el índice después de ver qué falta**. Se
declara la celda no estimable y se publican igual los dos marginales simples de
2021 (`aoj11`, `b18`) como descriptivo, rotulados como tales.

**IC95 — ranura que `S13` no pre-registró:** bootstrap de `upm` dentro de
`estratopri`, `B = 2000`, `seed = 20260908`, `rng = numpy.PCG64`. Elección del
ejecutor sobre ranura vacía, declarada y elevada a mesa.

**Cota:** numerador `< 10` ⇒ `NO-ESTIMABLE` (`S13 §2`).

---

## 4 · Qué NO hace

No escribe `S13 v1.1`. No inventa desenlace sustituto (Camino A sigue sin
mandato). No mueve el tier de `R10.3` (`[FUERTE]`). No reescribe D2-h. No agrupa
olas. No convierte la ausencia de desenlace en veredicto D2-h — que es
exactamente lo que el encargo prohibió.

**El primer resultado que produzca este procedimiento es el que se reporta.**
