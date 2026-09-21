# DIN · lote de cruces ENIF 2024 · `ahorra_solo_informal` × 14 pares — spec humana **v0.1 · PROPUESTA**

> **ESTO NO ESTÁ CONGELADO.** Es una **PROPUESTA** escrita en NUBE, sin abrir un solo
> byte de microdato. Quien congela es el **COMMIT-1 del lote, en CAJA, en otro acto**.
> Mientras diga `PROPUESTA` en el nombre del archivo, **ninguna corrida puede citarla
> como spec congelada** y ningún resultado puede sellarse contra ella.
>
> `ACTO GEN2-DIN-LOTE-ENIF2024-A`, 21/sep/2026, rama `acto/gen2-din-lote-enif2024-a`.
> Sucede operativamente al diseño `DISENO-LOTE-CRUCES-ENIF2024-protocolo-unico-v0_1.md`
> con sus enmiendas `v0_2` (firma F2 de mesa) y `v0_3` (regla de victoria).
> **Nada de esta spec remite a «como el piloto»: lo que rige está escrito aquí.**

**Universo, unidad y escala, en la primera línea.** Personas **elegidas de 18 años y
más** de ENIF 2024 (tabla `TMODULO`, una fila por persona), ponderadas por `fac_per`,
con `est_dis` × `upm_dis` como estrato y conglomerado. La cantidad estimada es una
**proporción de personas en `[0,1]`**; el error se reporta en **puntos porcentuales
(pp)**. **No se compara contra ENCIG (unidad trámite) ni contra el duelo nacional**, y
ninguna cifra de este lote se suma a una de otra escala sin función de enlace (A-bis 3).

---

## 1 · Qué mide, exactamente

**Estimando por celda.** `p(ahorra_solo_informal │ eje_A, eje_B)` — proporción ponderada
de personas del universo que, en la ventana de referencia de ENIF 2024 (junio de 2023 a
la fecha), **ahorraron por alguna vía informal y por ninguna vía formal** del conjunto
declarado.

```
informal   := alguna de P5_1_1 … P5_1_6 == "1"
formal_9   := alguna de P5_6_1 … P5_6_9 == "1"        (los NUEVE tipos de cuenta)
D9         := informal  AND  NOT formal_9              ← el desenlace, primario y único
```

`D9` es el desenlace conmensurable con el marginal público del árbitro
(`milpa/tramite-ola5-propuesta-v0.yaml:1426`). **Esta spec no reabre `D7`**: aquella
sensibilidad es del piloto 1 y no compite aquí.

**Códigos de respuesta.** Dominio declarado `"1,2"` en el FD de 2024 — `1 = Sí`,
`2 = No`. Un valor distinto de `"1"` (incluido vacío) **no** cuenta como Sí. Toda fila
con un valor fuera de `{"1","2",""}` en cualquiera de las 6 + 9 variables se **cuenta y
se emite como `RESULT`**, nunca se descarta en silencio.

**Gate del cuestionario, heredado y no corregido.** `P5_4_k` («¿Usted tiene…?») gatea a
`P5_5_k`/`P5_6_k` por posición `k`. Quien no tiene la cuenta `k` no responde la pregunta
de ahorro en `k` y entra al desenlace como «no usó esa vía formal». Cambiarlo produciría
otro estimando y rompería la comparación con el árbitro sellado.

**Filtros del universo, en este orden y sin ninguno más.**
1. `edad_v` numérica, **`18 ≤ edad ≤ 97`**. El `98` es centinela de no-especificación:
   **no es una edad**, no se imputa, no se reparte, y sale del universo con su conteo
   emitido como `RESULT` propio.
2. `tloc ∈ {1,2,3,4}`.
3. `fac_per` presente y `> 0`.

**Los seis ejes y sus cortes**, leídos del FD de 2024 (`enif_2024_fd.xlsx`,
`sha256/16=17e2ad86ce9e4fd5`) y no tecleados:

| eje | variable 2024 | categorías |
|---|---|---|
| `sexo` | `SEXO` | 2 — `1` hombre · `2` mujer |
| `edad` | `EDAD_V` | 4 tramos, declarados en `spec.yaml` |
| `escolaridad` | `NIV` (tabla `TMODULO`) | 4 tramos, **mapeados por ETIQUETA** (§2) |
| `localidad` | `TLOC` | 2 — `{1,2}` ≥ 15 000 hab · `{3,4}` < 15 000 hab |
| `formalidad` | `P3_13` | 2 — `{1..6}` con seguridad social · `{7}` sin |
| `cuenta_formal` | `P5_4_1..P5_4_9` | 2 — alguna `= 1` · ninguna |

---

## 2 · La trampa de la escolaridad, escrita antes de que nadie la pise

**El catálogo de `NIV` de 2024 NO es el de 2021.** Verificado por archivo en este acto
(`data/ahorro-comparabilidad-texto-v1_0.tsv`, filas `E-ESC`):

| código | 2012 · 2015 · 2018 · **2021** | **2024** |
|---|---|---|
| `04` | Estudios técnicos con secundaria terminada | **Normal básica** |
| `05` | Normal básica | **Estudios técnicos con secundaria terminada** |
| `09` | Maestría o doctorado | **Especialidad** |
| `10` | — | **Maestría** |
| `11` | — | **Doctorado** |

**Regla congelable:** el mapa de `NIV` a tramos se escribe **por etiqueta**, nunca por
número de código, y `spec.yaml` lo transporta como pares `(etiqueta, tramo)`. Cualquier
código que no case con una etiqueta declarada **detiene la corrida**: no se asigna a un
tramo por cercanía numérica. Un recodificado por número produciría cifras falsas en
`escolaridad` y en los cuatro pares que la contienen.

---

## 3 · Los 14 pares, clasificados, con la razón correcta de cada grupo

Seis ejes dan 15 pares; `localidad × edad` (8 celdas) ya se gastó en el piloto 1.
Quedan **14 pares**.

### 3.1 · Primarios — **5 pares, 44 celdas**

`sexo × edad` (8) · `sexo × escolaridad` (8) · `sexo × localidad` (4) ·
`edad × escolaridad` (16) · `escolaridad × localidad` (8) = **44 celdas**.

**Razón:** son los pares cuyos dos ejes viven en el **universo completo** y para los que
`C2` está adjudicado. Es la comparación primaria de la firma F2 de mesa (21/sep),
verbatim: «La comparación primaria es C2 contra R2 sobre los 5 pares con C2 adjudicado
(44 celdas)».

### 3.2 · Formalidad — **4 pares, secundarios y rotulados**

`formalidad × {sexo, edad, escolaridad, localidad}`.

**Razón, que no es la de 3.3 y no se confunde con ella:** `formalidad` **no vive en el
universo completo**. Su pregunta (`P3_13`) sólo se hace a quien trabajó o tuvo trabajo y
no es trabajador sin pago — cobertura `0.69`. `C2-COMPUESTO-RESERVADAS-spec-v1_0.md`
líneas 129-132 dictamina ese `C2` **NO-EMITIBLE contra ejes de universo completo**. Su
`C2` se restringe al universo de quien trabaja y el par se rotula **secundario**: A-bis
4 — un estimando restringido a una subpoblación no se compara contra uno poblacional.

### 3.3 · `cuenta_formal` — **5 pares, se adjudican aparte**

`cuenta_formal × {sexo, edad, escolaridad, localidad, formalidad}`.

**Razón, corregida por la enmienda v0.2 y escrita con sus palabras:** «en "sin cuenta"
el estimando cambia **por construcción del cuestionario, no por tautología**». El pase
`5.4 → 5.6` hace que, sin ninguna cuenta, ninguna vía formal pueda valer `1`; luego en
la celda «sin cuenta» `ahorra_solo_informal` **colapsa a `informal_cualquiera`**.
**Confirmado por el flujo del cuestionario de 2024 en este acto** (no por memoria ni por
reporte). No es que la celda sea trivialmente predecible: es que **mide otra cosa**.
Estos cinco pares se adjudican en su propio bloque y **no entran a la cifra principal**.

---

## 4 · Contendientes — lista cerrada, con fórmula cerrada

Todos se declaran aquí y se sellan **antes** de derivar un solo cruce. `p̂_A(a)` y
`p̂_B(b)` son los marginales ponderados de ENIF 2024 por categoría de cada eje; `p̂` el
marginal nacional; el subíndice `21` marca ENIF 2021.

| # | contendiente | clase | fórmula cerrada |
|---|---|---|---|
| `C2` | composición de marginales públicos de la **misma ola**, con IC | **piso adjudicado** (firma 17/sep) | `p̂(a,b) = p̂_A(a)·p̂_B(b)/p̂`, en escala **logit**; IC95 por delta sobre las réplicas compartidas. Rótulo obligatorio: **«ausencia de interacción en escala logit»**, nunca «independencia» a secas |
| `P2` | persistencia | piso | `p̂(a,b) = p̂_21(a,b)`: el mismo cruce medido en ENIF 2021 |
| `R1` | interacción histórica **cruda** | retador, secundario | `logit p̂(a,b) = logit C2(a,b) + δ_21(a,b)`, con `δ_21(a,b) = logit p̂_21(a,b) − logit C2_21(a,b)` |
| `R2` | interacción histórica **encogida** | **retador, familia primaria** | `logit p̂(a,b) = logit C2(a,b) + λ·δ_21(a,b)`, con **`λ = ½` fija** (§5) |
| `R3` | ajuste proporcional iterativo (IPF) | retador, secundario | tabla inicial `p̂_21(a,b)`, escalada iterativamente hasta casar los marginales de 2024 en las dos direcciones; criterio de paro y tope de iteraciones en `spec.yaml` |
| `L1` | LLM solo | retador, secundario | mediana de las repeticiones declaradas, por celda (§8) |
| `L2` | LLM con corpus (recibe los marginales públicos de 2024) | retador, secundario | ídem, con el mismo agregador |
| `M` | emisor del motor / matriz `B(x)·h_r` | **`NO-DERIVABLE`** | — |

**`M` se sella `NO-DERIVABLE`, con su razón,** por la firma F2: hoy no existe una `θ`
calibrada que emita esta celda, y la matriz **no es estimador por defecto** de una celda
que no adjudicó bajo el contrato celda-D (A-bis 5, `ADR-68`). **El silencio se escribe:**
`M` emite un `RESULT` de texto `NO-DERIVABLE` con su razón, no una ausencia.

**Multiplicidad, dicha antes:** la comparación que adjudica es **una sola** (`C2` contra
`R2`). `P2`, `R1`, `R3`, `L1`, `L2` y los 9 pares no primarios son **secundarios y se
rotulan así**; con ocho contendientes y 96 celdas alguien gana por azar, y por eso no
adjudican solos.

---

## 5 · `R2` lleva **λ = ½ fija**, y por qué — declarado antes de abrir

La firma F2 dice, verbatim: «R2 con λ estimada se define por la estabilidad de la
interacción entre las olas históricas de ENIF que resulten comparables por texto de
pregunta …; **si solo una lo es, R2 es solo λ = ½ y se declara antes de abrir**».

**Solo una lo es: 2021.** Lo estableció la pieza P1 de este acto, leyendo los cinco
descriptores y los cinco cuestionarios completos
(`data/ahorro-comparabilidad-texto-v1_0.tsv`; razón por ola en
`forense/notas/2026-09-21-lote-enif2024-comparabilidad-y-R2.md` §3):

- **2012** — los dos componentes del desenlace usan **ventanas de referencia distintas**
  (~3 meses el informal, ~12 el formal), y falta una vía informal.
- **2015** — el lado formal tiene 6 posiciones con nómina y pensión **colapsadas** y sin
  «apoyos de gobierno»; la partición no se recupera desagregando.
- **2018** — tiene **8 de las 9** vías formales: lo construible es `D8`, y `D9 ⊆ D8`.
- Y las tres arrastran, además, una **población base de 18 a 70 años**, no 18 y más.

**Por lo tanto `R2` entra al lote con `λ = ½`, para los catorce pares, sin excepción, y
sin miembro `Sλ`.** Si mesa admite la Opción B de la nota (armonizar a `D8` en 2018 y
2021 y estimar `λ` ahí), esta spec se enmienda **con un archivo propio antes del
COMMIT-1** — nunca in situ.

---

## 6 · Rejilla y regla de soporte

**Rejilla.** La rejilla de celdas **se lee del árbitro, no se teclea**: el conjunto de
categorías de cada eje y su orden salen del marcador vigente y del `spec.yaml`, y el
medidor los toma de ahí. Una categoría que el árbitro no declare **no existe** para este
lote.

**Regla de soporte, escrita como regla y no como número** (el umbral depende de `n`, que
sólo se conoce al abrir):

1. El umbral de soporte por celda se declara en `spec.yaml` **antes** de abrir
   microdato, como una función del tamaño efectivo de la celda; **no** se elige después
   de ver los conteos.
2. El soporte es un ***caveat*, no un bloqueo**: ninguna celda detiene la corrida por
   `n`. Una celda `FUERA-DE-SOPORTE` **no puntúa** en la comparación primaria y se
   reporta con su `n`.
3. **El soporte no se promete desde los marginales.** Las cotas de Fréchet–Hoeffding
   sobre márgenes publicados no acotan por abajo la intersección: en el piloto 1 las
   ocho cotas inferiores fueron `0`. Por tanto `n` es **`DESCONOCIDO`** hasta que la
   corrida lo calcule, y esta spec **no afirma** que ninguna celda esté bajo el umbral.
4. Una celda sin soporte en **cualquiera** de las dos olas que la alimentan no puntúa,
   aunque lo tenga en la otra.

---

## 7 · La regla de victoria (enmienda v0.3), con su estadística, su remuestreo y sus tres salidas

**Estadística primaria, una sola.** `Δ = MAE(C2) − MAE(R2)` en **pp**, sobre las celdas
**puntuadas** de los **5 pares primarios**, contra el árbitro `R` del cruce.

**Remuestreo.** IC95 **por réplica**: un **único plan de réplicas compartido** por todos
los contendientes y todas las celdas —mismas réplicas bootstrap con `est_dis` ×
`upm_dis`, semilla y número de remuestras congelados en `spec.yaml`—, de modo que `Δ` se
recalcula **réplica a réplica** y su IC95 recoge la correlación entre `C2` y `R2`.
Calcular dos IC independientes y restarlos **está prohibido**: ignoraría que los dos
emisores se evalúan sobre la misma muestra.

**Las tres salidas, excluyentes:**

| IC95 de `Δ` | veredicto |
|---|---|
| **despeja 0.5 pp** | **`R2` VENCE** |
| despeja **0** pero **no 0.5** | **PROPUESTA CON RESERVA** — un punto que satisface un umbral con un IC que no lo despeja **no adjudica** (A-bis) |
| **incluye 0** | **NADIE VENCE** |

**El conteo de ¾ de celdas es secundario y descriptivo.** Se reporta; no adjudica.

**Simulación de potencia — pieza obligatoria del COMMIT-1.** Antes de abrir nada del
lote, el COMMIT-1 corre esta regla sobre **datos ya abiertos** (pilotos 1, 2 y 3) y
reporta con qué tamaño de efecto y cuántas celdas el IC95 llega a despejar 0.5 pp. No
gasta reserva: los tres pilotos ya están abiertos. **Si la simulación muestra que la
regla no puede despejar 0.5 pp con 44 celdas, eso se declara antes de medir**, y la
consecuencia la decide mesa — no el ejecutor, y no después de ver el resultado.

---

## 8 · Los dos emisores `L`

`L1` (solo) y `L2` (con los marginales públicos de 2024) se corren **por CLI, sin API**
(`FP-228`), por mesa, con el paquete de
`forense/prereg-duelo-v2/PAQUETE-L-LOTE-ENIF2024-v0_1.md`. Modelo, versión, temperatura
y prompts **se congelan en el COMMIT-1**; modelo y versión se fijan al correr, con cita
del proveedor para la fecha de corte. **Las capturas se sellan antes de que exista el
COMMIT-2 mecánico** — una captura producida después de ver una emisión mecánica no
cuenta. Agregación declarada: **mediana** de las repeticiones por celda.

---

## 9 · Cobertura — por celda y por par, con su apellido

Se reporta la cobertura del IC95 de `C2` y la de `P2`, **tres veces**: (a) por celda;
(b) por par, como 5 conglomerados en la lectura principal (14 contando los secundarios);
(c) junto a las celdas de los otros instrumentos ya medidos.

**Las 44 celdas no son independientes:** salen de una sola muestra, y `sexo × edad` y
`edad × escolaridad` comparten a las mismas personas. **Por eso ninguna frase de producto
dice «cobertura del 9X %» sin el apellido «dentro de ENIF 2024».** Amplitud dentro de un
levantamiento es lo que este lote puede afirmar; independencia entre levantamientos sólo
la dan ENVIPE y ENCIG, que **se apartan sin abrir**.

---

## 10 · B-bis — pre-registro de falsación, antes de ver el dato

**Qué pasa si el falsador NO refuta:**

| salida | condición |
|---|---|
| **CORROBORADA** | nadie vence por §7 **y** la cobertura de `C2` por par es ≥ 80 % en la lectura principal |
| **ACOTADA** | vence alguien sólo en un eje — **se nombra el eje** en el veredicto |
| **FALSADOR DÉBIL** | ≥ ⅓ de las celdas de los 5 pares primarios quedan **sin soporte** |

**Si dos filas pueden satisfacerse a la vez, manda `FALSADOR DÉBIL`.** Se declara aquí,
al sellar, y no se decide al ver el dato.

**Qué refutaría el argumento de producto:** cobertura de `C2` **por par < 80 %** en la
lectura principal → «sé cuánto me equivoco» queda **acotado a los cruces ya vistos** y no
se generaliza.

---

## 11 · Los dos oros del COMMIT-1

1. **El oro del piloto 1.** El código genérico, corrido sobre `localidad × edad`,
   reproduce **a 1e-9** las emisiones y la `R` selladas del piloto 1. Es retrospectivo,
   no gasta reserva, y prueba el conducto de punta a punta con `corrida0 run`.
   **Si no reproduce, el código genérico no es el mismo procedimiento y el lote no se
   lanza.**
2. **El oro del `C2` sellado** (segundo oro, firma F2). El `C2` que el código genérico
   produce sobre los marginales públicos de 2024 reproduce el `C2` **ya sellado**, con
   la misma tolerancia.

Los dos son **condición de congelado**, no un chequeo posterior.

---

## 12 · «Congelado» — D-22 ampliada, como definición

El COMMIT-1 **no está congelado** hasta que las cinco se cumplan sobre el commit final
con `origin/main` fusionado:

1. `corrida0 preflight` **VERDE**.
2. **El punto de entrada ha corrido**, al menos sobre datos sintéticos. Un medidor cuyas
   pruebas sólo ejercitan guardias y constantes **no es un COMMIT-1**.
3. `_valida_outputs` acepta la salida de **cada rama terminal** del procedimiento —todas
   con soporte, soporte parcial, fuera de soporte global, cero celdas puntuadas, celda
   rara— sobre sintético **y** sobre oro.
4. **Todo `id` que el código pueda emitir nulo por lectura estática está declarado.**
5. **Ningún input con hash sobre un archivo vivo:** constancias, no libros abiertos.

Y el sello **cubre el código que mide**, no un shim que lo importa.

---

## 13 · Lo que NO significa — escrito ya, antes del dato

- **Que el piso gane no dice que la conducta sea estable por cultura.** Dice que la
  interacción entre ejes aporta poco sobre los marginales **en este levantamiento**.
- **Ahorrar sólo por vías informales responde a acceso, ingreso y oferta antes que a
  preferencia.** No es una elección cultural medida: es lo que queda cuando la vía formal
  no está disponible, no conviene o no se ofrece. No se romantiza («el mexicano prefiere
  la tanda») ni se patologiza («no sabe ahorrar»).
- **`cuenta_formal` es estructura de acceso, no conducta.** Por eso sus cinco pares se
  adjudican aparte y no entran a la cifra principal.
- **`formalidad` no es un rasgo de la persona.** Es una posición en el mercado de
  trabajo, y su celda «sin seguridad social» no describe a un tipo de mexicano.
- **El universo sub-representa a quien no decide el dinero del hogar**: la ENIF elige una
  persona por hogar y le pregunta por sus propias cuentas.
- **Ninguna cifra de este lote es un dato sobre «los mexicanos» sin segmentar.** Se
  reporta por eje, y `localidad` y `formalidad` existen precisamente para ver el sesgo de
  clase dentro de la modernidad urbana.
- **Ninguna cifra se compara contra ENCIG ni contra el duelo nacional** (otra unidad).

---

## 14 · Módulo de auditoría de rigor extremo (§5 de las instrucciones)

- **¿Pobreza, violencia, informalidad confundidas con cultura?** Es el riesgo central del
  lote y está atendido en §3.3, §10 y §13: lo que separa las celdas de `cuenta_formal` y
  de `formalidad` del resto es precisamente que ahí se mide estructura.
- **¿Sobregeneralización desde clase media urbana?** Los ejes `localidad` y `formalidad`
  existen para verlo y **se reportan por eje**, nunca agregados.
- **¿Sesgo de marcos o muestras estadounidenses/europeas?** Ninguno: toda la evidencia es
  **clase (a), dato primario en México**. Cero marcos importados, cero muestras de
  diáspora.
- **¿Qué cambia con foco rural/popular?** Localidades de menos de 15 000 habitantes y
  personas sin seguridad social son donde se espera **más** error del piso; se reporta
  aparte y no se promedia con el resto.
- **¿Qué parece psicológico y es incentivo racional?** El desenlace entero. Véase §13.
- **¿Dónde hay evidencia débil e intuición fuerte?** En la lectura «ahorro informal =
  desconfianza en los bancos». Este lote **no mide desconfianza** y ninguna frase suya la
  nombra.
- **¿Qué sería peligroso leído simplista?** «`X` % de los mexicanos sólo ahorra por fuera
  del sistema» sin el apellido del universo (18 y más, persona elegida, ENIF 2024) ni la
  segmentación.
- **¿Qué afirmación sobre el estado del corpus fue escrita a mano y no derivada?** Las
  variables, códigos y catálogos de §1 y §2 se leyeron del FD de 2024 en este acto y su
  procedencia está fila por fila en `data/ahorro-comparabilidad-texto-v1_0.tsv`. Los
  cortes de los tramos de `edad` y `escolaridad` **no se fijan aquí**: los fija
  `spec.yaml` en el COMMIT-1, leyéndolos del árbitro.
- **¿Qué deuda «asumida a propósito» caducó?** Ninguna de este lote: nace hoy.
- **¿Cuántos contadores movió este trabajo?** **Cero.** Esta spec es una propuesta; no
  hay corrida, no hay `RESULT`, `cuenta_gen2 = NO-APLICA`.
- **¿En qué escala está cada cantidad y contra qué se compara?** Proporción de personas
  en `[0,1]`; error en pp; comparación **sólo** entre emisores de la misma celda de la
  misma corrida.

---

## 15 · Lo que esta spec **no** hace

No congela · no abre microdato · no adopta nada al motor · no toca `milpa/`, el marcador
ni el crosswalk · no corona un campeón (`champion_actual = NINGUNO`; adoptar es de mesa,
por merge y por bloque) · no reabre el veredicto del piloto 3, que **sigue siendo
FALSADOR DÉBIL** · no gasta ninguna de las reservas apartadas (ENVIPE 2025, ENCIG 2025,
ENUT 2024 y ENVIPE 2026 entera).
