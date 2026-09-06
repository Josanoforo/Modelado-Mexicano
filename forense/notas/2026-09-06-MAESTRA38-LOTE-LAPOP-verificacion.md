# `ACTO MAESTRA38-LOTE-LAPOP` · verificación adversarial de las tres piezas

Antes de commitear ninguna cifra, cada pieza (`L4`, `L5`, `L18`) pasó por **tres verificadores
independientes con lentes distintas**, cada uno instruido para **refutar**, no para revisar:

1. **Fidelidad a la spec sellada** — ¿el código implementa lo que la spec pre-registró, o algo
   parecido? Cortes, universos, signo del estimando, celdas de más y de menos, guardia de
   numerador, ponderador, estrato/PSU; y `sha256` de la spec contra su `.sha256`.
2. **Exclusión silenciosa y aritmética** — reconstruir cada `n`, numerador y proporción **sin usar
   el medidor**, comprobar que las celdas suman al universo declarado y que las personas excluidas
   están contadas y explicadas; verificar que no hay códigos `NS/NR` numéricos colándose como
   válidos; y que el bootstrap remuestrea **UPM dentro de estrato**, no personas.
3. **Derivación del veredicto y honestidad de la fila `B-bis`** — dar por buenas las cifras y atacar
   la lectura: veredicto declarado contra el IC real, corazón compuesto caído por guardia leído como
   si se hubiera medido, suma de lo simple sustituyendo a lo compuesto, `se_mueve_si` parafraseado,
   eje anidado en el desenlace leído como muestra general, causalidad sobre corte transversal,
   reapertura de sellos ajenos, tier movido.

Los nueve corrieron sobre el árbol de trabajo en modo **sólo lectura** (sus scripts de comprobación
viven en `$TMPDIR`, no en el repo). **9 resultados: 7 `CONFIRMA`, 2 `REFUTA`.** Los dos `REFUTA`
eran defectos reales, se corrigieron, y los medidores se re-corrieron. **Ninguno cambió un veredicto
`B-bis` ni una cifra de celda.**

---

## Los dos defectos reales, y qué se hizo

### 1 · `L4`, lente 3 — **SERIO**: se comparaba el rótulo del veredicto, no el signo del efecto

`tools/medidor_l4_clientelar_lapop2019.py` emitía un campo
`misma_direccion_de_lectura_que_L9_L11` calculado como `veredicto == "CONTRARIA"` — mientras la
`nota` de su propio bloque decía «…y sólo se compara el **SIGNO**». Lo que el código hacía no era lo
que la nota decía que hacía.

Y los signos **no coinciden**: `Δ` de esta pieza = **−4.07 pp**; los cuatro de `L9`/`L11` = **+14.37,
+17.98, +6.38, +11.57 pp**. El campo afirmaba «misma dirección» cuando la dirección empírica es la
contraria. Es exactamente la trampa de **diferencia de conjuntos, no léxico**: las tres piezas caen
en `CONTRARIA` porque cada una refuta la predicción de **su propio** diseño, no porque el efecto
apunte al mismo lado.

**Corregido.** El campo se partió en dos —`mismo_signo_del_efecto_que_L9_L11` (`False`, calculado
sobre los números por `_mismo_signo()`) y `mismo_rotulo_de_veredicto_que_L9_L11` (`True`)— más un
campo que explica por qué difieren. **Y la corrección alcanzó a la prosa**: §5.2 de
`…-L4-resultados.md` decía que las tres piezas «van en el mismo sentido», que es el mismo error;
ahora trae la tabla de signos y aplica la **segunda** rama de spec §4.3 (sentidos distintos ⇒ los
dos mecanismos se comportan distinto, el `id` podría necesitar partirse — decisión de mesa), no la
primera. Sin la lente adversarial, ese párrafo se habría commiteado invertido.

### 2 · `L5`, lente 3 — **MENOR**: el JSON afirmaba una replicación que no ocurrió

`data/l5-protesta-multiola-v1_0.json` decía, en `notas_spec.C_agravio_es_replicacion`, que
`C_agravio` «repite el diseño ya corrido y sellado por `L9 §4` (+5.60 pp) y `L11 §2` (+3.72 pp)».
Falso: esas cifras son el `C2` de `L9` (agravio varía, entorno fijo en urbano); lo que el medidor
calcula —fijar `AGRAVIO=1` y contrastar urbano vs. rural, que es lo que spec §3.1 define
literalmente— es el `C1`, el que **cayó por guardia** en `L9` (rural-víctima `n=65`, num `7`). Y
vuelve a caer aquí en las tres olas (num rural 5, 4, 2). La medidora lo había declarado en su
reporte narrativo, pero **el matiz nunca llegó al artefacto persistido**, que es el que mesa
consume.

**Corregido.** El campo se reescribió como `C_agravio_NO_es_la_replicacion_que_la_spec_anuncia`,
con la tensión `§3.1` vs. `§0.3` explícita y el envío a `FP-314`. El medidor se re-corrió.

## Un tercer hallazgo, del que el defecto era mío, no de las piezas

Dos lentes distintas (`L4`-2 y `L5`-2), de forma independiente, señalaron que el resumen de diseño
muestral que la orquestación les entregó decía «2019 · `upm` (130)» cuando el `.dta` tiene **129**
UPM distintas (y 129 pares `(estratopri, upm)`). Los JSON de las piezas **nunca** afirmaron 130 —
`L4` reportaba `n_upm: 129` desde la primera corrida. El dígito viejo estaba en mi resumen de
contexto y se había filtrado a la tabla §1 de `…-L5-resultados.md`. **Corregido** ahí y en la
entrada de la propuesta. Se registra porque un negativo que nadie contradice se vuelve cifra: aquí
lo contradijeron dos verificadores que sí contaron.

## Lo que los siete `CONFIRMA` sí comprobaron (no es «se ve bien»)

- **Reproducción byte a byte**: tres lentes re-ejecutaron el medidor a un archivo de scratch y
  diffearon contra el JSON commiteado — **diff vacío** en las tres piezas. Los medidores son
  deterministas (seed 42).
- **Reconstrucción desde cero**: cada lente 2 escribió su propio lector (`pyreadstat` directo, su
  propia `_cod`, sus propias dicotomizaciones, sin importar nada de `tools/`) y recalculó todos los
  `n`, numeradores y proporciones. `L5`: los **24** pares `n`/numerador (4 celdas × urbano/rural ×
  3 olas) coinciden exactamente. `L18`: las 14 celdas coinciden a 6 decimales, y los 6 excluidos de
  `C_completo` se explican uno por uno (2 por `b18` faltante + 4 por `aoj12` faltante, sin solape).
  `L4`: las 12 celdas coinciden hasta el sexto decimal.
- **Un verificador reimplementó el bootstrap de conglomerado entero desde cero** (estructuras
  propias, sin `import`) para `C_falla` 2004, y reprodujo el IC.
- **Códigos escondidos**: se comprobó, contra los `value_labels` y `missing_user_values` crudos de
  cada payload, que **no** hay códigos `8`/`9`/`88`/`99` colándose como válidos. En 2004 `vic1` sí
  trae `3` y `8` — el filtro usa `vic1==1` exacto, así que quedan fuera; verificado, no supuesto.
- **La llave de PSU**: un verificador contó al principio 79 UPM donde el JSON decía 82, y encontró
  que **su propio** conteo estaba mal — en 2004 los 127 códigos `msec` se reparten en 131 pares
  `(mestrat, msec)`, y el objeto correcto de PSU en un diseño estratificado es el par, no el código
  pelado. El medidor ya usaba el par. Vale registrarlo: es el mismo error que habría estrechado el
  IC en silencio.
- **El cuestionario 2004**: verificado independientemente que `B10A`/`B18` usan la Tarjeta «A»
  (`1 = NADA … 7 = MUCHO`) y que `AOJ1` está gateada por `VIC1=1`, con `sha256` del PDF contra el
  manifiesto.
- **Robustez del veredicto de `L5` a la ambigüedad de lectura**: la lente 1 recalculó el veredicto
  **por ola** (en vez de la agregación de 9 celdas que usa `_veredicto()`) y las tres olas dan
  `NO-DISCRIMINA` igual. El veredicto no depende de esa elección.

## Una propiedad estructural que la verificación dejó anotada

En `L5`, la rama «corroboración del patrón por partes» de spec §4 es **inalcanzable por
construcción** tal como está codificada: exigiría que `C_agravio`, `C_falla` y `C_red` fueran las
tres limpias y positivas, y `C_agravio` nunca puede serlo aquí (cae por guardia en las tres olas).
No es un defecto aritmético y no afecta el resultado —`NO-DISCRIMINA` es correcto con los datos que
hay—, pero significa que el diseño de §4, en este corpus, sólo podía terminar en
`NO-DISCRIMINA` o en `CONTRARIA`. Se declara para quien vuelva a plantear esta regla.

---

**Escala de la verificación:** 12 agentes (3 de medición + 9 adversariales), 0 errores,
273 llamadas a herramienta, ~21 min de reloj. Los verificadores corrieron en `Sonnet`; la
supervisión, la réplica independiente de las cifras y las correcciones de arriba, en la sesión
principal.
