# ACTO `GEN2-CELDA-D-CAREO-1` · correctivo pre-emisión del diseño del piloto celda-D

**Qué es.** La respuesta operativa a la **devolución de revisión del 16/sep/2026** (ChatGPT/Codex) sobre `PR #827`, árbol examinado `e83c1af`. La devolución conserva el careo y la reserva y ordena **corregir el diseño ejecutable antes de lanzar `GEN2-CELDA-D-PILOTO-1`**. Mesa autorizó la corrección dentro de este mismo acto, con pruebas sintéticas, sin abrir otro frente que escriba registros compartidos.

**Qué NO es.** No es una firma, no es una adopción y no ejecuta el piloto. **No deriva el cruce `localidad × edad` de ENIF 2024, no abre microdato, no congela `tests/baseline.json` y no genera capturas.** Donde una corrección cambiaría algo que mesa firmó, la alternativa se devuelve **como alternativa**, nombrada y sin atribuirla como adoptada (§7).

**Qué se preserva intacto.** `forense/notas/insumos-direccion/CELDA-D-PILOTO-diseno-direccion-v1_1-post-careo-2026-09-17.md` es **insumo verbatim** (sha256 del cuerpo `68a794936ef2ca47…`) y **no se edita**: esta nota lo sucede operativamente. Lo mismo para el v1.0, el retorno de Astra, el brief externo y los dos D-θ. Las firmas históricas no se reescriben.

**Regla de lectura.** Donde esta nota y el diseño v1.1 discrepen sobre **cómo se calcula o qué se concluye**, manda esta nota. Donde discrepen sobre **qué autorizó mesa**, manda la firma del 17/sep y el v1.1: esta nota no la amplía.

---

## 1 · H1 · El desenlace de `C2` no es el de `R` ni el de `C1`

**El defecto.** El diseño v1.1 §1 define `R` y `C1` sobre los **siete códigos comunes** `P5_6_{1,2,3,4,5,8,9}` —y lo hace bien, porque `P5_6_6/7` no existen en ENIF 2021— y **reconoce por escrito** que el marginal público del árbitro usa los **nueve** (`milpa/tramite-ola5-propuesta-v0.yaml:1426`). Después construye `C2` **con ese marginal de nueve** (v1.1 §2 C3 y §9). Las dos cantidades son proporciones en `[0,1]`; **eso no las hace medidas del mismo evento**. Quien ahorra sólo por `P5_6_6` o `P5_6_7` cuenta como «sin vía formal» en `R`/`C1` y como «con vía formal» en los marginales que alimentan `C2`.

**Por qué importa más de lo que parece.** `C2` no es un candidato cualquiera: es **el piso que decide si la interacción aporta información**. Un error absoluto de `C2` contra `R` mezcla dos cosas —lo que la independencia no capta, y lo que dos definiciones distintas del desenlace separan— y no hay forma de repartirlas después. El propio careo tiene la regla en su tabla fundida, fila 12 (`universos o constructos distintos bajo la misma escala`, `YA-OCURRIÓ-AQUÍ`, `forense/hallazgos.md:842`, `:421`): **el diseño la enunció y no se la aplicó a sí mismo.**

**Tres salidas, y ninguna es del ejecutor.** Se documentan en §7 como **D1**. La recomendación del correctivo es **(a)**, con **(c)** como repliegue que no necesita decisión nueva:

- **(a) Marginales del mismo desenlace.** Derivar `p̂(l)`, `p̂(e)` y `p̂` sobre los **siete códigos comunes**, en `COMMIT-2`, con la misma receta que `R`. **No toca la reserva**: la reserva es el **cruce** `p(Y|l,e)`, no los marginales. Precio, dicho sin adorno: `C2` deja de ser «lo que todos ya vieron» y pasa a ser una cantidad derivada dentro del piloto — **cambia su dieta**, y por eso es decisión de mesa.
- **(b) Otro estimando común.** Redefinir `R`, `C1` y `C2` sobre los nueve códigos. **Se rechaza aquí con razón escrita:** rompe la persistencia, que es el piso del piloto, porque `P5_6_6/7` no existen en 2021.
- **(c) Retirar o reclasificar `C2`.** `C2` sale de la competencia y queda como **diagnóstico** (`rol: COMPLEMENTO`, `resultado: NO-APLICA`), y la pregunta del piloto se acota a «¿alguien vence a la persistencia?». No requiere derivar nada nuevo. Precio: sin `C2`, «`L` vence a la persistencia» **no distingue** información de interacción de información de marginales — exactamente lo que v1.1 §7(3) decía que `C2` existe para distinguir.

**Prohibido mientras tanto, y es lo que este correctivo sí cierra:** presentar los marginales de nueve como si fueran los de siete. La celda registrada lleva desde hoy el aviso.

---

## 2 · H2 · La fórmula de `C2` no devuelve una probabilidad

**El defecto.** v1.1 §2 C3 y §9 definen `p̂(l,e) = p̂(l)·p̂(e)/p̂`. Esta forma **no preserva el rango**. Contraejemplo **exclusivamente sintético**, el de la devolución:

```
p = 0.5, p_l = 0.8, p_e = 0.8   →   0.8 × 0.8 / 0.5 = 1.28     ∉ [0,1]
```

Los marginales pueden ser perfectamente factibles: el problema es la **composición**, no los insumos.

**Lo que no se hace.** No se recorta a `[0,1]` en silencio. Un recorte convierte un modelo mal especificado en un número presentable y borra la única señal de que estaba mal.

**Lo que se propone (D2 en §7): baseline log-aditivo**, declarado **como modelo distinto**, no como una normalización del anterior:

```
logit(x) = ln(x / (1 − x))        expit(z) = 1 / (1 + e^(−z))

p̂(l,e) = expit( logit(p̂_l) + logit(p̂_e) − logit(p̂) )
```

- **Rango:** `(0,1)` estricto por construcción, para cualquier logit finito. Preserva el rango **sin recortar**.
- **Casos límite:** si `p̂`, `p̂_l` o `p̂_e` ∈ `{0,1}` el logit diverge → **rechazo explícito** (`SIN-DEFINIR`), nunca recorte, nunca sustitución por un valor cercano.
- **Mismo contraejemplo:** `expit(logit .8 + logit .8 − logit .5) = 0.941176`, dentro de rango.
- **Qué supone, dicho:** es **ausencia de interacción en la escala logit**. **No es «independencia»**, y hay que dejar de llamarlo así: la independencia de `localidad` y `edad` como variables **no identifica** `P(Y | localidad, edad)`, ni con esta forma ni con la anterior.
- **Qué NO hace:** no reproduce los marginales exactamente (a diferencia de un raking/IPF, que exigiría la conjunta `L×E` y por tanto tocar el microdato), y **no estima la verdad**. Es un **piso**: una construcción declarada, reproducible y sólo-marginal que un challenger debe vencer para poder decir que la interacción aporta algo explotable.

**Nota de honestidad sobre el alcance del defecto.** Con los marginales públicos de ENIF 2024 la forma multiplicativa no supera 1 en ninguna de las ocho celdas — el defecto **no está vivo en esta celda concreta**. Se corrige igual, y por la razón que importa: un piloto no puede embarcar una regla general que funciona por suerte aritmética, y `C2` está escrito para reusarse en las celdas-D siguientes, donde la suerte no está garantizada.

---

## 3 · H3 · La incertidumbre de `C2` supone lo que no puede suponer

**El defecto.** v1.1 §4 declara para `C2` «IC muestral propagado bajo independencia (delta)». Los tres marginales **salen de la misma muestra**: un supuesto sobre las **variables** (`localidad ⊥ edad`) no convierte sus **estimadores** en independientes. Propagar con covarianzas cero subestima la anchura, y no por poco.

**Es, otra vez, una regla que el propio careo ya tenía escrita y no se aplicó:** tabla fundida, fila 9 (`dependencia entre celdas e intervalos marginales`, `PREVISTO-SIN-MECANISMO`, `RONDA1:66`), cuyo mecanismo mínimo es literalmente *«compartir índices de réplicas cuando la muestra es común»*.

**Lo que se propone, y depende de D1:**

- **Bajo (a)** — los marginales se derivan en `COMMIT-2`: **las mismas réplicas bootstrap** que producen `p̂_l`, `p̂_e` y `p̂` producen su distribución conjunta. Se propaga **réplica por réplica** a través de la función de §2 y el intervalo sale de los cuantiles del vector resultante. **Sin delta, sin supuesto de independencia entre estimadores, sin covarianzas inventadas** — y sin exponer `R`, porque las réplicas son de los marginales, no del cruce. Es el mecanismo mínimo de `RONDA1:66`, aplicado.
- **Bajo (c)** — sólo hay errores marginales publicados y **las covarianzas son desconocidas**: `C2` se emite como **punto**, con `incertidumbre: NO-ACREDITADA`, y **se enmienda el contrato**: v1.1 §4 promete un intervalo tipado para cada candidato, y esa promesa deja de ser cierta (**D3** en §7). No se inventan covarianzas cero para poder imprimir una banda.

---

## 4 · H4 · El soporte del cruce no está acreditado — y la cota lo dice

**El defecto.** v1.1 §1 deriva el `n` esperado por celda multiplicando marginales (*«mínimo ≈ 4 646 × 0.21 ≈ 980»*) y §4 concluye que **ninguna celda cae bajo el umbral** de 200, prometiendo verificarlo «sin abrir microdato». **El producto de márgenes es un punto bajo un supuesto, no evidencia del `n` de la intersección.**

**La cota, que es aritmética sobre márgenes ya sellados y no deriva nada reservado.** En una población común de tamaño `N`, el tamaño de la intersección está acotado (Fréchet–Hoeffding) por

```
max(0, n_l + n_e − N)  ≤  n_(l,e)  ≤  min(n_l, n_e)
```

Con los `n` publicados del árbitro (`milpa/tramite-ola5-propuesta-v0.yaml:1440-1470`; `N = 13 487`, el subconjunto cubierto por `edad`, cobertura `0.998889`):

| celda | cota inferior | cota superior | punto bajo independencia (lo que v1.1 usó) |
|---|---:|---:|---:|
| `<15 000 × 18-29` | **0** | 2 924 | 1 007 |
| `<15 000 × 30-44` | **0** | 4 256 | 1 466 |
| `<15 000 × 45-59` | **0** | 3 411 | 1 175 |
| `<15 000 × 60+` | **0** | 2 896 | 998 |
| `≥15 000 × 18-29` | **0** | 2 924 | 1 920 |
| `≥15 000 × 30-44` | **0** | 4 256 | 2 795 |
| `≥15 000 × 45-59` | **0** | 3 411 | 2 240 |
| `≥15 000 × 60+` | **0** | 2 896 | 1 902 |

**Las ocho cotas inferiores son `0`.** Los márgenes publicados son compatibles con una celda vacía. La afirmación de v1.1 §4 —«ninguna lo está por lo esperado»— **no está establecida por lo que el diseño cita**, y no puede estarlo sin abrir el dato.

**Lo que se fija en su lugar, sin adelantar nada:**

1. **`COMMIT-1`** fija la **regla y el umbral** y, sobre todo, la **salida predefinida para soporte insuficiente** (qué se emite, qué no, y cómo se reporta la celda). El umbral, las celdas y los candidatos **no se tocan después** de verlo.
2. **`n` queda `DESCONOCIDO`** hasta el paso autorizado que lo calcula. No se escribe un `n` esperado como si fuera medido.
3. **El paso de `C1`** (que ya abre ENIF 2021) **verifica el soporte de 2021**, que es el que el umbral gobierna.
4. **`COMMIT-3`** informa el soporte de 2024 junto con `R`.

---

## 5 · H5 · La conclusión y la parada estaban sobredimensionadas

**Conclusión.** v1.1 §3 (B-bis) dice: *«Si nadie vence a `C2` → la interacción no aporta información explotable a este `n`»*. **Eso no se sigue.** Lo que ese resultado dice, y todo lo que dice:

> **Los candidatos ensayados no superaron este piso, bajo esta evaluación, en estas ocho celdas.**

No identifica ausencia de interacción, ni ausencia de información aprovechable por otros métodos, ni una propiedad de la población. Un piso no vencido acota a los **retadores**, no al **fenómeno**.

**Parada.** v1.1 §6 exige, como condición de factibilidad, *«una entrada del catálogo de momentos poblada con estimador adjudicado»*. Eso **fuerza un ganador**. Se corrige: la factibilidad se cumple **también** cuando el resultado honesto es que no hay ganador. Salidas admisibles, todas terminales y ninguna con adopción forzada:

| salida | cuándo | qué se escribe en el catálogo |
|---|---|---|
| `ADJUDICADA` | un challenger vence a los pisos bajo §3 de v1.1 | el estimador adjudicado |
| `INDECIDIBLE` | se cumplen las condiciones verbatim de `ADV1-M3`, o hay < 6 celdas `PUNTUADA` | la entrada, con `estado_decidibilidad: INDECIDIBLE` y su conteo |
| `SIN-CANDIDATO-SUPERIOR` | todos ejecutaron y ninguno vence a los pisos | la entrada, con el piso corroborado y **sin adoptar nada** |
| `FUERA-DE-SOPORTE` | el soporte de §4 no alcanza en ≥ 3 de las 8 | la entrada, con la salida predefinida en `COMMIT-1` |

**Y el límite que la propia evaluación se impone.** Si el ganador se **elige** con las ocho celdas, **esa misma evaluación no lo valida de forma independiente**. Es la fila 7 de la tabla fundida del careo (`el holdout usado para elegir deja de ser prueba final`, `PREVISTO-SIN-MECANISMO inequívoco`) aplicada al piloto mismo: el careo la marcó «parcialmente atrapada» y éste es el residuo. **Consecuencia operativa:** el resultado del piloto se reporta como **selección más desempeño conjunto**, nunca como desempeño independiente del ganador, y la frase de v1.1 §6 «desempeño local, ahora sí reclamable» se acota a eso.

---

## 6 · H6 · Qué acredita la búsqueda negativa de la reserva

**El defecto.** El careo escribió que las ocho celdas de cruce *«son 8 números que nadie ha visto — ni dirección, ni `L`, ni el emisor»*. Lo que la evidencia sostiene es más estrecho, y hay que decirlo: `git grep -iE "localidad × edad|reserva por interacci"` sobre **5 256** archivos rastreados de `9dffd64` → **2 coincidencias**, ambas del 12/ago sobre clustering de `R5.1`. **Eso acredita que el cruce no está en el árbol. No acredita que ninguna persona ni ningún modelo lo haya visto nunca.**

**Lo que se mantiene, que es lo que el piloto necesita y sí es defendible:**

1. **Reserva operacional** — la cantidad no está derivada en el árbol y no se deriva hasta `COMMIT-3`, con el **orden del diff** como sello auditable.
2. **Dieta declarada por candidato** — qué ve cada uno, explícitamente, incluidos los marginales que `C3` recibe a propósito.
3. **Exposición conocida, declarada** — quién vio qué, hasta donde la trazabilidad alcanza, sin extenderla a lo que no cubre.

**Lo que se retira:** la promesa de cegamiento absoluto por orden de commits. El orden protege contra el **doble uso del dato dentro del piloto**; no es una afirmación sobre el mundo. La nota del careo lleva la enmienda fechada correspondiente.

---

## 7 · Las decisiones que faltan, y son de mesa

Ninguna se adopta aquí. Las tres primeras nacen de este correctivo; las tres últimas ya venían de v1.1 §7 y siguen abiertas.

| # | decisión | opciones | recomendación del correctivo |
|---|---|---|---|
| **D1** | Desenlace de `C2` (§1) | (a) marginales de **siete códigos** derivados en `COMMIT-2` — cambia la dieta de `C2` · (b) redefinir todo a nueve — **rompe la persistencia**, se rechaza con razón · (c) retirar `C2` a diagnóstico y acotar la pregunta del piloto | **(a)**, con **(c)** como repliegue que no necesita decisión nueva |
| **D2** | Forma de `C2` (§2) | baseline **log-aditivo** con rechazo explícito en los casos límite, declarado como **modelo distinto** · o mantener el multiplicativo · o retirar `C2` | **log-aditivo**; el multiplicativo no preserva el rango y no debe embarcarse |
| **D3** | Contrato de incertidumbre (§3) | bajo (a): **réplicas compartidas**, sin delta ni independencia de estimadores · bajo (c): `C2` como **punto**, `incertidumbre: NO-ACREDITADA`, y **enmendar** la promesa de v1.1 §4 de un intervalo por candidato | réplicas compartidas si se toma (a); si se toma (c), enmendar la promesa y decirlo |
| **D4** | `FP-376` — `localidad` como `MAPEO-N-A-1` | firmar o devolver | sin ella el piloto corre; **el marcador no puede consumirlo** |
| **D5** | Definición por **siete códigos comunes** | aceptar con la diferencia escrita, o rechazar | aceptar; rechazarla cuesta la persistencia |
| **D6** | Admisión de `C2` como segundo piso | admitir, o no | queda **subordinada a D1–D3**: admitir `C2` sin resolverlas es admitir un piso que mide otro evento |

**Lo que sigue siendo válido y no se toca:** la firma de mesa del 17/sep; el careo y sus tres hechos re-ejecutados; la **reserva por interacción** como mecanismo; la celda elegida; la salida de `formalidad`; `C1` (persistencia 2021, siete códigos); el emisor fuera de competencia; `C4` `INEJECUTABLE` con sus cuatro faltantes; y el orden de tres commits. **Nada de lo corregido aquí toca el veredicto del careo.**

---

## 8 · Qué se tocó en el árbol, y qué no

**Se escribió:**

- Esta nota.
- `tests/test_celda_d_c2.py` — **pruebas sintéticas** de lo que §2–§5 fijan: rango `[0,1]`, casos límite `p ∈ {0,1}` con **rechazo explícito**, mismo identificador de desenlace en entradas y salida, tratamiento declarado de la incertidumbre compartida, celda sin soporte y resultado sin ganador. **Fixtures sintéticos únicamente; cero microdato, cero cifras del modelo.**
- Un **bloque de comentario fechado** en `data/curacion-registro/celdas-d/DIN.ahorro_solo_informal.enif2024.localidad_x_edad.yaml` que apunta aquí. **Los valores firmados de la celda no se editan**: siguen byte a byte los de v1.1 §9, porque cambiarlos sería adoptar D1–D3 sin firma. La celda ya declara `requiere_decision_mesa: true` y `estado_operativo: PENDIENTE`.
- Enmiendas fechadas en la nota del careo (§6 de aquí) y en la hoja del sucesor.

**No se tocó:** ningún insumo verbatim · ninguna firma histórica · `tests/baseline.json` · `milpa/` · specs · el crosswalk · el marcador · las otras tres celdas-D. **Cero microdato, cero derivación del cruce, cero capturas.**

**Una pieza de la devolución queda sin ejecutar y se dice:** *«Mantener el hallazgo 17→16 como enmienda fechada»*. **No se ejecuta porque no se identificó a qué conteo se refiere** — ni la nota del careo ni el encargo ni los insumos contienen un par `17 → 16` que se pueda enmendar sin adivinar cuál es. **Se pide la referencia concreta** (archivo y línea, o el conteo por su nombre) antes de escribir nada: inventar la enmienda sería peor que dejarla pendiente, y enmendar el conteo equivocado es un defecto nuevo. Fila: `NC-0282`.
