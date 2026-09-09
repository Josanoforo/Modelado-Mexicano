# Cierre · `ACTO GEN2-LOTE-ENIF-1` — ahorro y confianza financiera, ENIF 2024

**9 de septiembre de 2026 · CAJA (Ubuntu/WSL2) · base `origin/main = 0f62668`**
Spec sellada: `forense/prereg-caja/ENIF-AHORRO-spec-v1_0.md`
(`prereg-caja-ENIF-AHORRO` v1.0, sha `697ab9e8…`)
Corrida: `data/corrida0/CALC-ENIF-0001/` (sello `0c908018…`)

---

## 0 · Lo que cierra

**El ciclo entero, por tercera vez.** Se midió, se citó en el motor y se
probó el consumo: **4** de los 8 consumidores quedan adoptados con cita
`corrida0_resultado_id` + `corrida0_generacion: GEN2`, la sonda de consumo
pasa **4/4** contra `milpa.src.emisor`, y los contadores se mueven:
`adoptados_activos` **6 → 10**, `dependencias_legacy` **199 → 195**.

Y cierra algo más: **`FP-201` es falso también para ENIF**, con lo que la
parte ENIF de `NC-0086` queda contestada con dato.

---

## 1 · Cuatro premisas del encargo que no se sostienen (ninguna bloqueó)

| # | el encargo decía | el árbol / el codebook / **el dato** |
|---|---|---|
| **P1** | «la plaza: `CORR-0017`» | `CORR-0017` es `S7-L17` (ENSANUT, vacunación), **2** `RESULT`, `entorno = INDECIDIBLE-SIN-PAYLOAD-DECLARADO`. La plaza ENIF2024 es **`CORR-0009`**: 10 `RESULT`, `entorno = CAJA`. Los 8 `RESULT` que el encargo nombra por `id` existen y **todos** están en `CORR-0009`. Se obedeció la **identidad**, no el rótulo |
| **P2** | «¿adultos 18-70?» | FD: `EDAD_V = 18-95`. Cuestionario: **«PARA PERSONAS DE 18 AÑOS Y MÁS»**. **Medido** (guardia `G-P1`): min 18, max 95, +5 con código 97 y 10 con 98 → `18-Y-MAS · PREMISA-18-70-REFUTADA`. La `escala_legacy` de `RES-0059`/`RES-0060`, que dice «18 a 70», queda **desmentida** y corregida en la cita |
| **P3** | «el filtro de conocimiento ANTES de la pregunta de desconfianza» | El flujo es el **inverso**: `5.20 → PASE A 5.23`. `5.23` va **después** |
| **P4** | «el denominador de esa tasa es **solo quienes conocen**» | Es la población **sin cuenta**, **partida en dos** por `P5_23`. Y `P5_23` **no trae código `b`** — la única del tramo `5.19`-`5.24` que no lo trae: se le pregunta a **todo el mundo** |

`P3` y `P4` son premisas ajenas **sobre el dato**, así que no se supusieron:
se escribieron como **guardias que PARAN** (`G-C1`, `G-C2`) antes de abrir el
microdato. Ambas pasaron — pero pasaron **medidas**, no asumidas.

---

## 2 · Guardias, 8/8 en verde

| guardia | qué verifica | resultado |
|---|---|---|
| `G-P1` | la población es 18+ | `18-Y-MAS · PREMISA-18-70-REFUTADA` (18..95, +5×`97`, +10×`98`) |
| `G-C1` | `P5_23` es partición de la población | **0** blancos en 13 502 filas → `SI` |
| `G-C2` | quien contesta `5.20` no declara cuenta | **0** filas violan el flujo → `SI` |
| `G-D1` | `EST_DIS`/`UPM_DIS`/`FAC_PER` existen | las tres presentes; `0` columnas ausentes de 33 |
| `G-D2` | `FAC_PER` > 0 | **0** filas sin ponderador |
| `G-D3` | estratos de una sola UPM | 4 (familia A) y 46 (familia C); IC rotulado, no colapsado |
| `G-D4` | llaves opacas como texto | **13 502 / 13 502** filas traen cero a la izquierda — leerlas como número habría fusionado estratos en silencio |
| `G-D5` | dominio de códigos del FD | **0** celdas fuera de dominio. **El descriptor no miente en esta ola** |

`spec-check`: **33 OK · 0 FAIL**, 317 718 filas de inventario examinadas.
`preflight` VERDE · `run` exit=0 · `verify` **REPRODUCE** (`CONTEXTO=IDENTICO`).

---

## 3 · Los 8 `RESULT`

| `RESULT` | celda | `p` | IC95 | n | denominador |
|---|---|---|---|---|---|
| `RES-0046` | `A-P-CORTO-SIN` | **0.541343** | [0.5216, 0.5619] | 4 973 | 18+ con trabajo **sin** seg. social |
| `RES-0047` | `A-P-NOCORTO-SIN` | **0.458657** | [0.4381, 0.4784] | 4 973 | ídem |
| `RES-0048` | `A-P-CORTO-CON` | **0.373130** | [0.3499, 0.3938] | 3 969 | 18+ con trabajo **con** seg. social |
| `RES-0049` | `A-P-NOCORTO-CON` | **0.626870** | [0.6062, 0.6501] | 3 969 | ídem |
| `RES-0057` | `B-P-FORMAL` | **0.284927** | [0.2742, 0.2968] | 13 502 | **toda** la población 18+ |
| `RES-0058` | `B-P-INFORMAL` | **0.561920** | [0.5502, 0.5740] | 13 502 | **el mismo** — único par que comparte |
| `RES-0059` | `C-P-DESCONFIA-CONOCE` | **0.060780** | [0.0377, 0.0867] | 426 | 18+ **sin cuenta** que **sí** conocen |
| `RES-0060` | `C-P-DESCONFIA-NOCONOCE` | **0.054767** | [0.0457, 0.0647] | 2 544 | 18+ **sin cuenta** que **no** conocen |

**Seis denominadores distintos para ocho `RESULT`.** Compartir la apertura del
archivo —una sola tabla, un solo ponderador— no autorizó compartir
denominador. `RES-0059` + `RES-0060` **no suma nada**: son tasas
condicionales a celdas ajenas, y el propio medidor lo dice en su salida
(`C-NOTA-NO-SUMAR`).

---

## 4 · Control positivo GEN1: **4/8 REPRODUCE**, y los otros 4 **quedan atribuidos**

| `RESULT` | GEN1 | medido | delta | veredicto |
|---|---|---|---|---|
| `RES-0046` | 0.330600 | 0.541343 | **+0.210743** | `NO-REPRODUCE` |
| `RES-0047` | 0.669400 | 0.458657 | −0.210743 | `NO-REPRODUCE` |
| `RES-0048` | 0.173400 | 0.373130 | **+0.199730** | `NO-REPRODUCE` |
| `RES-0049` | 0.826600 | 0.626870 | −0.199730 | `NO-REPRODUCE` |
| `RES-0057` | 0.284927 | 0.284927 | **+0.000000** | `REPRODUCE` |
| `RES-0058` | 0.561920 | 0.561920 | **+0.000000** | `REPRODUCE` |
| `RES-0059` | 0.060780 | 0.060780 | **+0.000000** | `REPRODUCE` |
| `RES-0060` | 0.054767 | 0.054767 | **+0.000000** | `REPRODUCE` |

### 4.1 · La discrepancia de la familia A está atribuida al 100 %

Diagnóstico **posterior y read-only** — no tocó el CALC sellado. Fase 1 usó
**tres** convenciones distintas de las de esta spec; con las tres, esta
corrida la reproduce al grano al que GEN1 está sellado (cuatro decimales):

1. **El corte.** `corto = P4_10 {1}`, no `{1,2}`. Ya estaba declarado en la
   spec como sensibilidad `S1` **antes** de correr.
2. **Qué contó como «con seguridad social».** GEN1 usó `P3_13 ∈ {1..6}` —
   **incluyendo el código `5` (seguro PRIVADO de gastos médicos) y el `6`
   («otra institución»)**. Eso no es seguridad social: es «tiene derecho a
   servicios médicos por su trabajo, de donde sea». Esta spec usa
   `{1,2,3,4}` y lo justifica en §3.3.
3. **Los complementos.** GEN1 los derivó por `1 − p`, no los contó:
   `0.6694 = 1 − 0.3306` **exacto** y `0.8266 = 1 − 0.1734` **exacto**. Esta
   spec los cuenta directamente (`P4_10 ∈ {3,4,5}`).

Con (1) + (2): `sin_ss = 0.330639` (GEN1 `0.3306`) y `con_ss = 0.173418`
(GEN1 `0.1734`); `|delta|` = **3.9e-5** y **1.8e-5** — residuo del redondeo
del propio sellado GEN1, que sólo publica cuatro decimales.

> **⚠️ Residuo NO explicado, declarado.** La **cobertura**. GEN1 declara
> `66.89%`. Esta corrida mide `67.53%` (`P3_13 ∈ {1..7}`) y `68.06%`
> (incluyendo el `9`). **No se reconcilia y no se fuerza.** Queda como
> `NC` abierta.

⚠️ **A-bis.3 respetado.** Fase 1 midió **sin** diseño; esta corrida **sí** lo
estima. **Sólo se comparó el punto.** Ninguna salida de este acto pone los IC
de fase 1 y los de esta corrida lado a lado, y el propio `resultados.json` lo
declara en `G-NOTA-IC-NO-COMPARABLE`.

`NO-REPRODUCE` **no invalidó la corrida, no autorizó tocar el medidor y no se
ajustó nada hacia atrás.**

---

## 5 · La coexistencia, medida

`formal_cualquiera` **0.284927** + `informal_cualquiera` **0.561920** =
**0.846847**. En esta ola la suma **no** excede 1 — pero el par **no es una
partición**, y el dato lo demuestra:

| complemento | n | fracción ponderada |
|---|---|---|
| **ahorra por LAS DOS vías** | 2 969 | **0.204767** |
| ahorra por **ninguna** | 4 803 | **0.357920** |

**Nada se normalizó, nada se re-escaló.** Si en otra ola la suma pasara de 1,
eso seguiría siendo coexistencia y no defecto (Astra §2.4; hallazgo 3.2 del
lote ENVIPE).

**Control interno** contra la variable derivada `FILTRO_S5_1` del propio
INEGI: **COINCIDE**, `0` filas discrepantes. La derivación propia desde
`P5_6_1..P5_6_9` reproduce el filtro que INEGI publica — y `FILTRO_S5_1`
nunca se usó como fuente.

---

## 6 · `FP-201` es falso también para ENIF — cierra la parte ENIF de `NC-0086`

`FP-201` declaró «sin campo de diseño UPM/estrato reproducible» para las cinco
fuentes de fase 1. Para ENVIPE ya había resultado falso. Aquí, contra el FD
(bloque `VARIABLES DE DISEÑO ESTADÍSTICO` de `TMODULO`, filas 1478-1483):

| variable | tipo | tamaño | códigos | usado en esta corrida |
|---|---|---|---|---|
| `EST_DIS` | Alfanumérico | 3 | `001 - 190` | **sí** — estratificación |
| `UPM_DIS` | Alfanumérico | 5 | `00001 - 02172` | **sí** — conglomerado del bootstrap |
| `FAC_PER` | Numérico | 6 | `126 - 106896` | **sí** — ponderador del punto |

Medido: **190 estratos y 2 164 UPM** en el universo completo; `0` filas sin
diseño. **`FP-201` es falso para ENIF 2024.** Quedan tres fuentes de fase 1
sin re-examinar (ENCUCI, ENNViH/MxFLS y la quinta): este acto **no** las
resuelve — sólo aplica la lección a ENIF, como el encargo pedía.

---

## 7 · Adopción y consumo (P3)

### 7.1 · Cuatro citas, cuatro sin cita — decidido por la medición

| `RESULT` | veredicto | cita en `milpa/tramite.yaml` |
|---|---|---|
| `RES-0057`, `RES-0058` | `REPRODUCE` (delta `+0.000000`) | **SÍ** |
| `RES-0059`, `RES-0060` | `REPRODUCE` (delta `+0.000000`) | **SÍ** |
| `RES-0046`…`RES-0049` | `NO-REPRODUCE` | **NO** — `NC-0114`…`NC-0117` |

La familia A **no recibe cita** porque su `p` medido **no es** el `p`
publicado: citarla afirmaría que el `0.330600` de `milpa/` sale de este
`RESULT`, y no sale. La cifra de `milpa/` **no se movió** — este acto no
cambia ningún `p`; sólo declara, donde puede, de dónde viene.

Las cuatro citas también **corrigen el denominador** que la `escala_legacy`
declaraba mal (18-70 → 18+) en `RES-0059`/`RES-0060`.

### 7.2 · Complementos: sin cita, con `NC` de advertencia

`A-FUERA-DEL-EJE` (n=148, 1.14 %), `A-SIN-EJE-BLANCO` (n=4 134, **31.94 %** —
la gente a la que `3.13` nunca se le pregunta porque no trabajó),
`B-AMBAS-VIAS`, `B-NINGUNA-VIA` y `C-OTRAS-RAZONES` se emiten **con su
denominador escrito y sin rango de cantidad medida**, y **ninguno** lleva cita
`corrida0_*`. Patrón `NC-0085`.

### 7.3 · Sonda de consumo (solo lectura): **PASA 4/4**

```
cargar_reglas() -> 21 reglas
  dinero.ahorro.via_informal              formal_cualquiera         0.284927 == 0.284927  PASA
  dinero.ahorro.via_informal              informal_cualquiera        0.56192 ==  0.56192  PASA
  dinero.ahorro.seguro_deposito_enif2024  …conoce_proteccion…        0.06078 ==  0.06078  PASA
  dinero.ahorro.seguro_deposito_enif2024  …no_conoce…               0.054767 == 0.054767  PASA
  SONDA: 4/4 PASA
```

El árbol quedó intacto tras la sonda. **La compatibilidad queda demostrada,
no supuesta.**

### 7.4 · Contadores, crudos, sin esperados

| contador | antes | después |
|---|---|---|
| `N_resultados_gen2_adoptados_activos` | 6 | **10** |
| `dependencias_numericas_legacy_activas` | 199 | **195** |

---

## 8 · El veredicto ajeno que este acto movió, y por qué

`registro --verifica --escribe` paró con `REPLAY-PISADO (NC-0094)`: la pasada
que llena las columnas de replay de `CALC-ENIF-0001` **también** re-corre
`CALC-ENCIG-0001--c3ae00e62e59`, cuyo veredicto pasaba de `NO-VERIFICADO` a
`REPRODUCE` / `IDENTICO`.

Se autorizó explícitamente
(`--lote CALC-ENIF-0001,CALC-ENCIG-0001--c3ae00e62e59`) **por esta razón**:
el cambio es `NO-VERIFICADO → REPRODUCE`, es decir **más evidencia, no menos**,
y la produjo re-ejecutar el medidor congelado de ENCIG en esta misma caja
contra el mismo corpus. **No se borró ningún veredicto: se llenó uno que
estaba vacío.** `resultados.tsv` está dentro del perímetro declarado
(«TSV re-derivados»). No existe `--force` y no se usó ningún atajo.

---

## 9 · Límites declarados

1. **`P4_10 = 1` es una categoría colapsada**: «menos de una semana» y **«no
   tiene ahorros»** son la misma casilla. Todo corte que incluya el `1` —el
   primario y `S1`— arrastra gente **sin ahorros** dentro de «horizonte
   corto». El descriptor no permite separarlas.
2. **`P5_20 = '03'` conflaciona desconfianza y mal servicio.** El `RESULT`
   mide la **categoría del codebook**, no el constructo.
3. **La familia A excluye a quien no trabaja** — `31.94 %` ponderado de la
   población. No es descuido: `3.13` no se les pregunta. El peso se midió;
   el estimando **no existe** para ellos.
4. **`razón cualquiera` = `NO-APLICA`.** `P5_20` es de respuesta única y ENIF
   2024 no trae batería de menciones múltiples para `5.20` (contraste: `5.7`,
   `5.8`, `5.15`, `5.17` sí lo son). `NO-APLICA` es un valor, no un hueco.
5. **Los IC no son comparables con fase 1** (A-bis.3, §4.1).
6. **Los IC de las familias A y C están rotulados
   `IC-CON-ESTRATOS-DE-UPM-UNICA`** (4 y 46 estratos con una sola UPM): se
   leen como **límite inferior** de la anchura verdadera, nunca como IC
   exacto. La familia B, con 190 estratos y 2 164 UPM, sale
   `BOOTSTRAP-UPM-EN-ESTRATO` limpio.
7. **Nada causal.** `P4_10`, `P5_1_*`, `P5_6_*`, `P5_20` y `P5_23` son
   declaraciones del informante en una sección transversal. `P3_13` no es
   asignación aleatoria: comparar las celdas de la familia A es
   **descripción**, no efecto.

---

## 10 · Hallazgo colateral, fuera de perímetro (no se tocó)

`forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md:10` dice «los cuatro
`RESULT` restantes de **`CORR-0009`** (`RES-0039..0042`)». En la demanda
vigente `RES-0039`…`RES-0042` son de **`CORR-0007`**, y `CORR-0009` es
ENIF2024. Es una referencia cruzada equivocada en una spec ya fusionada.
**No se editó** (spec sellada, fuera del perímetro de este acto). Va a
`## NO-CORRIDO` con sucesor.

---

## 11 · `ya_medido.py` (A.8, `ADR-340`) — salida cruda, y un falso negativo más

El encargo archivado es **verbatim** y no se edita para complacer un test
(misma regla que rige `T25`), así que la salida vive aquí. `T-YAMEDIDO`
registra la exención en `_T_YAMEDIDO_ARCHIVOS_CONOCIDOS` con esta razón.

```
$ python3 tools/ya_medido.py dinero.ahorro.horizonte_corto
  milpa/tramite.yaml:1025  situacion=ingreso_sin_seguridad_social tier=FUERTE p=0.330600
      id: dinero.ahorro.horizonte_corto
  MEDIDA-EN: L7

$ python3 tools/ya_medido.py dinero.ahorro.horizonte_no_corto_con_seguridad_social
  milpa/tramite.yaml:1049  situacion=ingreso_con_seguridad_social tier=FUERTE p=0.173400
      id: dinero.ahorro.horizonte_no_corto_con_seguridad_social
  NUNCA-MEDIDA          <-- FALSO NEGATIVO

$ python3 tools/ya_medido.py dinero.ahorro.via_informal
  MEDIDA-EN: MAESTRA38-SELLO-3

$ python3 tools/ya_medido.py dinero.ahorro.seguro_deposito_enif2024
  milpa/tramite.yaml:1190  situacion=SELLADA tier=FUERTE veredicto=veredicto_Bbis=NO-DISCRIMINA p=0.060780
      id: dinero.ahorro.seguro_deposito_enif2024
  MEDIDA-EN: MAESTRA38-SELLO-3, canon§7, tramite-ola5-propuesta-v0.yaml
```

**El segundo es un falso negativo verificado.** `ya_medido.py` devuelve
`NUNCA-MEDIDA` para una regla que **está medida y sellada** en
`milpa/tramite.yaml:1049`, `tier=FUERTE`, `p=0.173400` — y la **propia sección
de listado de la herramienta la imprime ahí, en la línea anterior a su
veredicto**. Es el defecto que `ACTO GEN2-LOTE-ENCIG-1` (`ADR-438`) diagnosticó:
`_tiene_veredicto_real()` **no reconoce `MEDIDO`**, sólo los veredictos de
falsación `R` o un campo `veredicto:`, así que una regla medida como **tasa
base** —el patrón de toda la cartera F4→F3— le es invisible.

**Cuarta familia de reglas donde se confirma.** `T-YAMEDIDO` existe para que
ningún acto llame «territorio virgen» a una regla ya medida: para ésta habría
dejado pasar exactamente ese error. **No se repara aquí** (fuera de
perímetro); va a `## NO-CORRIDO` con sucesor.

Nótese la asimetría que lo delata: los otros tres ids sí devuelven
`MEDIDA-EN:`. Lo que separa al que falla no es que esté menos medido —está
medido igual— sino dónde cae su evidencia respecto de la ventana y del
vocabulario de veredictos que el script sabe leer.
