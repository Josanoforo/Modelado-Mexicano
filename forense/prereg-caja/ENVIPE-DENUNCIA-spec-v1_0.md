# ENVIPE-DENUNCIA · Pre-registro de la tasa de no-denuncia por miedo o desconfianza, ENVIPE 2025

### `prereg-caja-ENVIPE-DENUNCIA` · **v1.0** · 9 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-ENVIPE-DENUNCIA`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado **antes de abrir un solo byte de microdato**, de la corrida `CALC-ENVIPE-0001`: la proporción ponderada de delitos no denunciados cuya **razón principal** declarada es miedo o desconfianza, en ENVIPE 2025 (`BP1_23`). Releva bajo el registro GEN2 la demanda `CORR-0009` (`RES-0027` / `RES-0028`), cuyo consumidor es `milpa/tramite.yaml:civico.denuncia.miedo_desconfianza`. |
> | **QUÉ NO ES** | No es un veredicto causal: la diferencia entre tasas es **descripción/asociación** y ningún `RESULT` de esta spec se rotula causal. No mide ENCIG ni ENIF. No mide los cuatro `RESULT` restantes de `CORR-0009` (`RES-0039..0042`, denuncia condicional a seguro, **unidad delito, `BPCOD=01`**): apertura distinta, quedan en `## NO-CORRIDO`. No transfiere a 2012–2024 (§7.1). No toca `milpa/tramite.yaml` ni ningún sello previo. |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py preflight CALC-ENVIPE-0001` en VERDE antes de correr; después `run` y `python3 tools/corrida0.py verify CALC-ENVIPE-0001`. El control positivo externo está pre-declarado en §6 con sus tres ramas y su consecuencia en cada una. |

**Acto:** `ACTO GEN2-LOTE-ENVIPE-1`, 9/sep/2026, entorno **CAJA (UBUNTU)**, corpus montado (`data/raw` → `/home/pc0/mm-corpus/raw`, 400 archivos examinados), sobre `origin/main = 6e0381b` (`PR #651`).

---

## 0 · Premisas verificadas contra el árbol, y la contaminación declarada

### 0.1 · La premisa del encargo sobre `origin/main` no se sostiene, y no bloquea

El encargo declara su `VERIFICACIÓN DE EXISTENCIA` «contra el clon de `631fcd78`» y ordena: *«si origin/main se movió de 631fcd78, re-deriva y reporta antes de editar»*. Se movió: `631fcd7..6e0381b` (`PR #651`, `GEN2-C0-D-CORRECTIVO`, 5 commits). Re-derivación completa, con los comandos a la vista:

```
$ grep "^CORR-0009" data/corrida0/demanda-corridas.tsv
CORR-0009 | ENVIPE2025 | envipe2025_csv | SIN-CANDIDATO-EN-EL-REGISTRO | 6
          | RES-0027;RES-0028;RES-0039;RES-0040;RES-0041;RES-0042 | CAJA
          | PARCIAL:script+spec+spec_sha | 1
$ grep -rn "CORR-0009" forense/prereg-caja/        → 0 aciertos (54 archivos examinados, A.13)
$ sha256sum data/raw/envipe2025_csv.zip
8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa   ← coincide con el manifiesto
```

Las cuatro afirmaciones del bloque A.8 del encargo **siguen valiendo** sobre `6e0381b`. Tres cifras derivadas **no**, y se corrigen aquí: ADR máximo real **428** (no el heredado), `NO-CORRIDO` máxima **NC-0082** (el encargo decía `NC-0080`), y el rótulo `GEN2-LOTE-ENVIPE-1` está **AUSENTE** de `canon/registro-rotulos.tsv` (se censa en la cascada).

### 0.2 · COBERTURA RETROACTIVA — el encargo pidió localizarla, y SÍ existe

La receta `PARCIAL:script+spec+spec_sha` no prueba ausencia de trabajo previo. Localizado, con universo declarado (`grep -rn "0.294313"` sobre todo el árbol, `--include=*.md,*.yaml,*.tsv,*.py,*.json`):

| componente de `PARCIAL` | ¿existe? | dónde |
|---|---|---|
| `script` | **SÍ** | `tools/tasas_base_fase1.py:67-107` (`regla_civico_denuncia()`), `ACTO MAESTRA32-E18 · REGLAS-OLA5-FASE1`, 31/ago/2026 |
| `spec` | **SÍ, pero como nota, no como pre-registro** | `forense/notas/2026-08-31-reglas-fase1-spec.md` §(c).1 |
| `spec_sha` | **NO-ENCONTRADO** | no hay `.sha256` ni entrada en `forense/prereg-caja/` (0 de 54 archivos) |
| corrida sellada GEN2 (`CALC-*`) | **NO-ENCONTRADO** | `ls data/corrida0/` — 21 directorios `CALC-*`, ninguno de ENVIPE |

Es decir: **la cantidad ya se midió una vez en GEN1 y ya está sellada en el motor** (`milpa/tramite.yaml:574`, `p=0.294313`, `tier: FUERTE`), y `tools/ya_medido.py civico.denuncia.miedo_desconfianza` devuelve `MEDIDA-EN: tramite.yaml` (salida completa en el encargo archivado). Lo que **no** existe es la cadena `E.2` que el registro GEN2 exige. Producirla es el objeto de este acto; no duplica nada.

### 0.3 · Contaminación declarada (ADR-46) — esta corrida NO es ciega

Se dice antes de cualquier cifra, no después. Al congelar esta spec la sesión **ya había leído**:

| dónde | qué | valor |
|---|---|---|
| el propio encargo, cuerpo de A.8 | los dos valores GEN1 y su suma | `0.294313` / `0.705687` |
| `data/corrida0/demanda-resultados.tsv:RES-0027/0028` | idem, con `payload_sha256` | idem |
| `forense/firmas-pendientes.tsv:FP-201` | el IC95 y la `n` de la corrida GEN1 | `IC95[0.282822, 0.306570]`, `n=13023`, ponderador `FAC_ELE` |
| `forense/notas/2026-08-31-reglas-fase1-spec.md` §(c).1 | **la codificación GEN1 completa** | `miedo/desconfianza = {01,02,06,08}` vs `práctica = {03,04,05,07}`, excluyendo `09`, `99` y blanco |

**Consecuencia, sin adornos:** el ejecutor conoce el resultado GEN1 y la partición GEN1 antes de congelar. El procedimiento obligatorio del encargo (contestar A.8 y localizar la cobertura retroactiva) es la vía por la que entró la contaminación — se asienta aquí, no se descubre al cerrar.

**Qué se hace con eso.** Tres cosas mecánicas, no promesas:

1. La codificación **primaria** de esta spec (`C1`, §3.1) **no es la de GEN1**: se deriva sólo del texto literal del reactivo y deja fuera el código `08`, que en GEN1 estaba dentro. La partición GEN1 entra como brazo **secundario declarado** (`C2`), no como el estimando principal.
2. El criterio de lectura de §6 se ancla al **IC95 medido por esta misma corrida**, no a un umbral que esta sesión pudiera calibrar hacia la cifra que ya conoce.
3. Lo derivable de lo ya leído se **pre-declara en §6.3** como derivación de metadato leído, no como pronóstico ciego, para que mesa lo descuente.

**Qué sigue siendo genuinamente desconocido al congelar:** todos los `RESULT` de esta spec sin excepción. La cifra GEN1 conocida es **de otra unidad de observación y de otra codificación** que la primaria de aquí; los conteos de `09`, `99` y blanco —de los que depende el veredicto de exhaustividad de §6.2, que es la pregunta que el encargo manda contestar— **no aparecen en ninguna fuente leída**, ni en la nota GEN1, ni en `FP-201`, ni en el registro.

---

## 1 · Identidad: instrumento, ola, payload, tablas

### 1.1 · Payload, por el manifiesto (nunca «está en `data/raw`»)

| campo | valor |
|---|---|
| `id` de manifiesto | **`envipe2025_csv`** (`data/manifiesto.yaml:306-321`) |
| archivo | `envipe2025_csv.zip` |
| `sha256` | `8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa` |
| `tamano_bytes` | `17600019` |
| `url_origen` | `https://www.inegi.org.mx/contenidos/programas/envipe/2025/datosabiertos/conjunto_de_datos_ENVIPE_2025_csv.zip` |
| `fecha_descarga` | `2026-07-30` |

⚠️ **Homónimo peligroso, sellado aquí.** El propio manifiesto advierte que ENVIPE 2025 está registrada **dos veces con payloads distintos**: el otro es `envipe_2025_bd_envipe_2025_csv` (canasta masiva, otro `sha256`, sin abrir). **No son intercambiables por nombre.** Esta spec usa `envipe2025_csv` y sólo ése, resuelto por `id` de manifiesto a través de `tests/payload_resolver.py` — el medidor nunca busca su payload por su cuenta.

### 1.2 · Ola y periodo de referencia, por el metadato del propio payload

`*/metadatos/metadatos_envipe2025.txt`, verbatim:

```
Identifier: MEX-INEGI.EGS3.02-ENVIPE-2025
Temporal: 2024-01-01-2024-12-31 y 2025-03-01-2025-04-30
Modified: 2025-09-18
AccrualPeriodicity: Anual
```

**La ola se llama 2025; los delitos que mide ocurrieron en 2024.** El levantamiento fue marzo–abril de 2025. Toda unidad de esta spec dice «ENVIPE 2025 (delitos de 2024)».

### 1.3 · Tablas y unidad de observación — **declarado, porque cambia el denominador**

| tabla | unidad de la fila | llave | ponderador |
|---|---|---|---|
| `tmod_vic_envipe2025` | **un DELITO** (hasta 15 por persona) | `ID_DEL` | `FAC_DEL` («Factor delito») |
| `tper_vic2_envipe2025` | **una PERSONA** (informante seleccionado) | `ID_PER` | `FAC_ELE` («Factor de personas elegidas») |

Fuente: `*/diccionario_de_datos/diccionario_de_datos_*.csv`, campos `NOMBRE_CAMPO`/`NEMONICO`/`TIPO`/`LONGITUD`/`RANGO_CLAVES`. **`BP1_23` vive en `tmod_vic`, o sea a nivel DELITO.** La unidad natural del reactivo es el delito; la corrida GEN1 reportó a nivel persona, colapsando. Esta spec mide **las dos** y declara cuál es primaria (§3.3).

---

## 2 · El reactivo, verbatim del cuestionario

`data/raw/cuest_modulo_envipe2025.pdf` (`sha256 21df3861…`, `id` de manifiesto `envipe2025_cuest_modulo_pdf`), extraído con `pdftotext -layout`:

```
1.20 ¿Acudió ante el Ministerio Público o Fiscalía Estatal a denunciar el delito?
     Sí ... 1   PASE A 1.24
     No ... 2
     CIRCULE UN SOLO CÓDIGO
     SI EL CÓDIGO DEL DELITO ES DEL 05 AL 15, PASE A LA PREGUNTA 1.23.

1.21 ¿Algún(a) otro(a) integrante de este hogar acudió a denunciar el delito
     ante el Ministerio Público o Fiscalía Estatal?
     Sí ... 1 · No ... 2  PASE A 1.23 · No sabe / no responde ... 9

1.23 ¿Cuál fue la razón principal por la que no denunció o no denunciaron el
     delito ante el Ministerio Público o Fiscalía Estatal?
     CIRCULE UN SOLO CÓDIGO
     Por miedo al (a la) agresor(a) ................................. 01
     Por miedo a que lo (la) extorsionaran ......................... 02
     Delito de poca importancia .................................... 03
     Pérdida de tiempo ............................................. 04
     Trámites largos y difíciles ................................... 05
     Desconfianza en la autoridad .................................. 06
     No tenía pruebas .............................................. 07
     Por actitud hostil de la autoridad ............................ 08
     Otra_____________________________________________ ............. 09
     No sabe / no responde ......................................... 99
```

Nombre del campo en el descriptor: **`BP1_23` — «Razón principal de la no denuncia»**, `TIPO=Numérico`, `LONGITUD=2`, claves `01..09`, `99`, `b` (blanco). Catálogo `tmod_vic_envipe2025/catalogos/bp1_23.csv`, leído en UTF-8, idéntico al cuestionario.

**Tres propiedades del reactivo que gobiernan todo lo que sigue, y que salen del instrumento, no de GEN1:**

- **(a) Es de RESPUESTA ÚNICA** («CIRCULE UN SOLO CÓDIGO») y pide la razón **principal**. No es una batería de múltiples razones: una tasa sobre él es «proporción de delitos cuya razón *principal* fue X», nunca «proporción de delitos en que X influyó».
- **(b) Tiene DIEZ categorías sustantivas, no dos.** `09` («Otra», con texto abierto) y `99` («No sabe / no responde») son categorías del propio instrumento, no artefactos.
- **(c) Su universo lo fija el flujo de salto**, no el analista: se llega a 1.23 sólo si el delito no fue denunciado (`BP1_20 = 2`) y, para los delitos de hogar (`BPCOD 01..04`), sólo si además nadie más del hogar denunció (`BP1_21 ≠ 1`). Para los delitos **personales** (`BPCOD 05..15`) el salto es directo y de una sola condición.

---

## 3 · Universo, codificación y unidad — todo pre-declarado

### 3.1 · Codificación del desenlace, con dirección de escala

**Dos codificaciones, ambas congeladas aquí. La primaria es `C1`.**

| | códigos `= 1` | códigos `= 0` | de dónde sale |
|---|---|---|---|
| **`C1` · núcleo léxico** (PRIMARIA) | `01`, `02`, `06` | `03`, `04`, `05`, `07`, `08` | los tres códigos cuyo **texto literal** dice «miedo» o «desconfianza». Cero interpretación. |
| **`C2` · núcleo + actitud hostil** (SECUNDARIA DECLARADA) | `01`, `02`, `06`, `08` | `03`, `04`, `05`, `07` | añade `08` («Por actitud hostil de la autoridad»). **Es la partición que usó GEN1.** |

**Dirección de escala (A-bis.3):** ambas son **proporciones en `[0,1]`**; **más alto = mayor peso del miedo/desconfianza como razón principal**. Ningún `RESULT` de esta spec es un porcentaje ni puntos porcentuales.

**Por qué `C1` es la primaria y no `C2`.** `08` describe una **conducta atribuida a la autoridad**, no un estado del declarante; leerlo como «desconfianza» es un juicio, y `E.1` prohíbe que GEN1 elija la codificación de GEN2. La spec no oculta el juicio: lo **mide**. `RESULT-ENVIPE-DEN-DELTA-C2-C1` es exactamente lo que vale reclasificar el código `08`, y se reporta con signo.

### 3.2 · Universos (denominadores), pre-declarados

Todos parten de: filas de `tmod_vic` con **`BPCOD ∈ {05,…,15}`** (delitos personales, salto de una sola condición) y **`BP1_20 = 2`**.

| id | denominador | por qué existe |
|---|---|---|
| **`U1`** (PRIMARIO) | `BP1_23 ∈ {01,…,08}` | las ocho razones sustantivas clasificables por `C1`/`C2`. Es el denominador **bajo el cual, y sólo bajo el cual**, `C2` y su complemento pueden sumar 1. |
| `U2` | `BP1_23 ∈ {01,…,09}` | añade `09` («Otra»), categoría sustantiva del instrumento |
| `U3` | `BP1_23 ∈ {01,…,09, 99}` | universo completo de quien llegó al reactivo y contestó algo |
| `U4` | personas (`ID_PER`) con ≥1 delito en `U1` | **unidad de la corrida GEN1**; ponderador `FAC_ELE` |

Los delitos con `BP1_23` en blanco pese a `BP1_20 = 2` **no se imputan a cero**: se cuentan (`RESULT-…-N-BP1_23-BLANCO`) y quedan fuera de los cuatro universos. **Cero no sustituye falta de dato.**

### 3.3 · Unidad primaria: **el DELITO**

El estimando primario es a nivel **delito**, ponderado por `FAC_DEL`. Razón: `BP1_23` es un atributo del delito, el instrumento lo pregunta una vez por delito, y **ninguna regla de colapso a persona está dictada por el instrumento** — la que usó GEN1 («si algún delito de la persona califica, la persona = 1») es una elección de analista, legítima pero no derivable del reactivo.

`U4` (persona, `FAC_ELE`, regla de colapso GEN1 verbatim) se mide igual y se reporta como **secundario declarado**, porque es la única forma de comparar contra GEN1 sin cambiar dos cosas a la vez.

### 3.4 · Ponderador, estrato y UPM — **disponibles, y la regla para grupos sin conglomerado**

Del descriptor de ambas tablas:

| campo | tipo | rango | presente en |
|---|---|---|---|
| `FAC_DEL` | Numérico(6) | `000001,…,999999` | `tmod_vic` |
| `FAC_ELE` | Numérico(6) | `000001,…,999999` | `tper_vic2` |
| **`EST_DIS`** | Carácter(3) | `001,…,607` | **ambas** |
| **`UPM_DIS`** | Carácter(7) | `0000001,…,9999999` | **ambas** |

⚠️ **Corrige a la corrida GEN1.** `FP-201` declaró, para las cinco reglas de fase 1, *«sin campo de diseño UPM/estrato reproducible en el perímetro de este acto para ninguna de las cinco fuentes»*, y por eso su IC95 fue un bootstrap simple de filas. **Para ENVIPE 2025 eso no se sostiene:** `EST_DIS` y `UPM_DIS` están declarados en el descriptor de las dos tablas que esta spec usa. Esta corrida **sí** estima varianza de diseño. (Esto NO reabre las otras cuatro reglas de fase 1: cada fuente es suya, y ninguna se toca aquí.)

**Método de IC (ranura no pre-registrada, se declara y se eleva a mesa):** bootstrap de **`UPM_DIS` con reemplazo dentro de `EST_DIS`**, conservando el número de UPM por estrato; percentiles 2.5/97.5; 2000 réplicas; `numpy.PCG64`, semilla `20260909`. Nadie pre-registró el método de IC para esta serie: lo elige el ejecutor sobre ranura vacía. **No se hereda el bootstrap de filas de GEN1** (otra implementación y otro supuesto): no se espera coincidencia dígito a dígito de los extremos.

**Regla para estratos con una sola UPM** (lo que el encargo llama «grupos sin conglomerado»), pre-declarada:

- Un estrato con **exactamente una** `UPM_DIS` no aporta varianza entre conglomerados. **No se colapsa con otro estrato** (colapsar es una decisión de diseño que esta spec no está autorizada a tomar) y **no se descarta** (sesgaría el punto). Entra al punto y, en el bootstrap, **se re-muestrea a sí mismo**, contribuyendo varianza cero.
- Su conteo va en `RESULT-ENVIPE-DEN-N-ESTRATOS-UPM-UNICA`. Si es `> 0`, `RESULT-…-METODO-IC` sale **`IC-CON-ESTRATOS-DE-UPM-UNICA`** y el IC se reporta como **límite inferior de la anchura verdadera**, no como IC exacto. **Un IC ingenuo no se presenta como IC de diseño.**
- Si `EST_DIS` o `UPM_DIS` faltan en el archivo pese al descriptor, o vienen vacíos en toda fila válida, el IC sale `null` y el veredicto es **`NO-ESTIMABLE-DISENO-INCOMPLETO`** — el punto se reporta igual, sin IC.

### 3.5 · Guardias de existencia, antes de medir

Pre-declaradas porque el descriptor puede documentar una variable que el archivo no trae, y una columna puede existir y estar vacía:

1. **Columna ausente.** Si falta cualquiera de `ID_PER`, `ID_DEL`, `BPCOD`, `BP1_20`, `BP1_23`, `FAC_DEL`, `EST_DIS`, `UPM_DIS` en `tmod_vic`, o `ID_PER`, `FAC_ELE` en `tper_vic2` → todos los `RESULT` de estimación salen `null` y el veredicto global es **`NO-ESTIMABLE-COLUMNA-AUSENTE`**, nombrando la columna.
2. **Columna vacía.** Si una columna existe pero tiene **0 valores válidos** sobre el universo → mismo tratamiento, veredicto **`NO-ESTIMABLE-COLUMNA-VACIA`**.
3. **Universo vacío.** Si `N` de `U1` es `0` → **`NO-ESTIMABLE-UNIVERSO-VACIO`**.
4. **Ponderador no positivo.** Filas con `FAC_DEL` no finito o `≤ 0` se cuentan (`N-SIN-PONDERADOR`) y salen del universo.

Ninguna guardia «arregla» el dato: cada una **para y declara**.

---

## 4 · Estimadores

Sobre el universo `Uk` y la codificación `Cj`:

```
p(Cj, Uk) = Σ_{i ∈ Uk} w_i · d_i(Cj)  /  Σ_{i ∈ Uk} w_i
```

con `w = FAC_DEL` (`U1..U3`) o `FAC_ELE` (`U4`), y `d ∈ {0,1}` según §3.1. Sumas en orden fijo de fila para que dos corridas del mismo árbol den bytes idénticos.

- **Estimando primario:** `p(C1, U1)`.
- **Réplica de la partición GEN1:** `p(C2, U1)` y `p(C2, U4)`.
- **Complemento:** `p_complemento(C2, U1) = Σ w·1[BP1_23 ∈ {03,04,05,07}] / Σ_{U1} w`.
- **Descomposición del universo completo:** `p(C2, U3)`, `p_otra(U3)`, `p_nsnr(U3)`.

---

## 5 · Lo que emite `CALC-ENVIPE-0001` (contrato)

Todos los `RESULT` llevan `tipo` y `unidad` con **escala explícita** (A-bis.3). La lista cerrada vive en `data/corrida0/CALC-ENVIPE-0001/spec.yaml` y es la que `corrida0 run` valida output por output; aquí va su lectura humana:

| bloque | qué trae |
|---|---|
| **A · universo y faltantes** | `N` del módulo, `N` de `BPCOD 05-15`, `N` de no denunciados, `N` por tramo de `BP1_23` (`01-08`, `09`, `99`, blanco), `N-SIN-PONDERADOR`, `N-SIN-DISENO`, y la **masa de ponderadores** de `U1`. Conteos **antes y después** de cada filtro. |
| **B · estimación primaria** | `p(C1,U1)` con `IC-LO`/`IC-HI` y su veredicto |
| **C · codificación GEN1** | `p(C2,U1)` con IC, y `DELTA-C2-C1` (lo que vale reclasificar `08`) |
| **D · exhaustividad** | complemento de `C2` en `U1`, su **suma**, el veredicto de exhaustividad, y `p(C2,U3)`, `p_otra(U3)`, `p_nsnr(U3)` |
| **E · unidad persona** | `N` de personas, `p(C2,U4)` con IC, masa de `FAC_ELE` |
| **F · control positivo** | `DELTA-VS-GEN1` con signo y `REPRODUCE-GEN1` |
| **G · diseño** | `N` de estratos, de UPM, de estratos con UPM única, y `METODO-IC` |
| **H · adopción P3** | rama de adopción y su delta |

---

## 6 · Ramas pre-declaradas — escritas ANTES del dato

### 6.1 · Control positivo externo contra GEN1 (`REPRODUCE-GEN1`)

Se compara **`p(C2, U4)`** —única celda que comparte codificación **y** unidad con GEN1— contra `0.294313`, y el resultado es informativo en las tres ramas:

- **`REPRODUCE`** si `|Δ| ≤ 1.0e-6`. Lectura: el medidor GEN2 reconstruye la cifra sellada; la cadena `E.2` queda montada sobre la misma cantidad, y la diferencia de método de IC es lo único nuevo.
- **`NO-REPRODUCE`** si `|Δ| > 1.0e-6`. **Esto NO invalida la corrida y NO se ajusta el medidor para cerrarlo.** Se reporta el delta con signo y se abre `NC` con el sucesor: reconciliar universo GEN1 vs GEN2 (el candidato conocido es que GEN1 filtró por el tamiz `AP7_3_05..15` de `tper_vic2` y esta spec filtra por `BPCOD` en `tmod_vic`; son la misma intención por dos caminos y pueden no dar la misma `n`).
- **`NO-COMPARABLE`** si `U4` sale `NO-ESTIMABLE` por cualquiera de las guardias de §3.5.

**Ninguna rama cambia la codificación primaria `C1`.** El control positivo verifica el aparato, no elige el estimando.

### 6.2 · La hipótesis «los dos valores GEN1 suman 1» (`VEREDICTO-EXHAUSTIVIDAD`)

Ésta es la pregunta que el encargo manda contestar, y su respuesta **ya está determinada por el instrumento**, no por el microdato — lo que el microdato decide es cuánto pesa:

- **`EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-U1`** si `N(09) + N(99) + N(blanco) > 0`. Lectura: `denuncia_con_miedo_o_desconfianza` y `denuncia_por_otra_razon` suman 1 **por construcción del recorte**, no porque el instrumento las haga exhaustivas. `RES-0028` no es «el complemento medido»: es `1 −` el primario sobre un denominador que **excluye** categorías reales del reactivo, y la magnitud de lo excluido va en `p_otra(U3)` y `p_nsnr(U3)`.
- **`EXHAUSTIVAS-EN-EL-UNIVERSO-COMPLETO`** si `N(09) + N(99) + N(blanco) = 0`. Lectura: el recorte no quita nada y la suma a 1 es propiedad del universo entero.
- **`NO-EXHAUSTIVAS`** si `|p(C2,U1) + p_complemento(C2,U1) − 1| > 1.0e-9`. Sería un defecto del medidor (partición de `U1` en dos bloques disjuntos que agotan `U1`), no un hallazgo sustantivo: dispara PARO y se reporta.

**Consecuencia pre-declarada para `RES-0028`:** bajo la primera rama, el complemento **no se emite como cantidad medida independiente**. Se emite el complemento de `C2` sobre `U1` con su denominador escrito en la unidad, y la nota dice que `RES-0028` está cubierto **sólo en ese sentido**. `E.1` verbatim: GEN1 no elige la codificación.

### 6.3 · Derivaciones de lo ya leído (§0.3), declaradas para que mesa las descuente

No son pronósticos ciegos. De la codificación GEN1 ya leída se sigue, **por aritmética y no por medición**, que `p(C2,U1) + p_complemento(C2,U1) = 1` exactamente, y que por tanto la rama `NO-EXHAUSTIVAS` sólo puede caer por defecto de software. Lo que **no** se sigue de nada leído, y por eso es la aportación real de esta corrida: los conteos de `09`/`99`/blanco, el valor de `p(C1,U1)`, el `DELTA-C2-C1`, el punto a nivel delito, y los IC de diseño.

---

## 7 · Límites declarados (van también en la nota)

### 7.1 · Alcance temporal
**ENVIPE 2025 (delitos de 2024) no valida transferencia a 2012–2024 ni cumple cortes de ola previa.** Ninguna cifra de esta spec se propaga a otra ola. Para un duelo temporal hay que reconstruir la fuente permitida ola por ola o excluir ese camino con cita — **decisión de mesa**, no de este acto (queda en `## NO-CORRIDO`).

### 7.2 · Prohibición de calibrar contra las celdas del marco
Las seis celdas ENVIPE del marco `M` ya vistas (`CIV-M-01/-02/-04/-10/-12/-13`, todas con el mismo `0.294313`) **no se usan para calibrar nada aquí**, y ninguna mejora observada en ellas se presentará como confirmación independiente. Esta spec no toca el marcador ni sus capturas.

### 7.3 · Causalidad
Ningún `RESULT` de esta spec se rotula causal. «Miedo/desconfianza como razón principal» es lo que la persona **declaró**, no una causa medida de la no-denuncia.

### 7.4 · Lo que queda fuera y no se declara cubierto
`RES-0039..0042` (`civico.denuncia.con_seguro` / `.sin_seguro`) tienen **otra apertura**: unidad delito restringida a `BPCOD=01` (robo total de vehículo), condicionada a cobertura de seguro, con desenlace `denuncia`/`no_denuncia` — no razones de no-denuncia. Su spec **no** quedó completa en P1 y por tanto, según el propio encargo, **no entran**: quedan citados en `## NO-CORRIDO` sin declararse cubiertos.

---

## 8 · Congelamiento

Esta spec se congela en el **COMMIT-1** de `ACTO GEN2-LOTE-ENVIPE-1`, junto con `data/corrida0/CALC-ENVIPE-0001/{spec.md, spec.yaml, medidor.py}`, **antes de abrir un solo byte de microdato**. Lo abierto hasta este punto, y nada más: el manifiesto, el descriptor (`diccionario_de_datos/*`), los catálogos (`catalogos/*`), el metadato (`metadatos/*.txt`), la lista de miembros del ZIP, y los PDF de cuestionario y FD. **Ningún `conjunto_de_datos/*.csv`.**

> **El primer resultado que produzca este procedimiento es el que se reporta.**
