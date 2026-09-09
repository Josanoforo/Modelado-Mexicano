# `ACTO GEN2-LOTE-ENVIPE-1` — cierre. Primer lote F4→F3: una tasa pertinente con procedencia completa

**Fecha:** 9/sep/2026 · **Entorno:** CAJA (Ubuntu/WSL2), corpus montado · **Base:** `origin/main = 6e0381b` (`PR #651`)
**Encargo:** `forense/encargos/2026-09-09-GEN2-LOTE-ENVIPE-1.md` (A.3, verbatim)
**Spec sellada:** `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md` (`prereg-caja-ENVIPE-DENUNCIA`, `sha e404e7b5…`)
**Corrida:** `data/corrida0/CALC-ENVIPE-0001/` — `PRE-FLIGHT VERDE` → `run` → `verify: REPRODUCE` (39/39)

---

## 0 · El titular, antes de nada

**La cadena `E.2` queda montada y el control positivo pasa: `P-C2-U4 = 0.29431298745731216` contra el `0.294313` que el motor ya trae sellado — delta `−1.25e-08`, y `n = 13023`, la misma que `FP-201` declaró para la corrida GEN1.** El aparato mide lo que dice medir.

**Y al montarla aparecieron tres cosas que la cifra GEN1 no dice, ninguna de ellas visible desde el valor sellado.**

---

## 1 · La compuerta se movió y se re-derivó antes de editar

El encargo contestó su A.8 contra `631fcd78`. Al arrancar, `origin/main` estaba en `6e0381b` (5 commits, `PR #651` `GEN2-C0-D-CORRECTIVO`). Re-derivado todo lo que depende del perímetro:

| lo que el encargo declaró | lo real sobre `6e0381b` |
|---|---|
| «última NC al escribir: NC-0080» | **NC-0082** → la primera de este acto es `NC-0083` |
| ADR candidato heredado | **ADR máximo real 428** → candidato `ADR-429` |
| — | rótulo `GEN2-LOTE-ENVIPE-1` **AUSENTE** de `registro-rotulos.tsv` (censado en la cascada) |
| `CORR-0009` = 6 RESULT | confirmado; pero `RES-0039..0042` **no** son razones de no-denuncia (ver §6) |

Las cuatro afirmaciones sustantivas del bloque A.8 siguen valiendo. Ninguna cifra del encargo se dio por buena sin comando.

## 2 · Cobertura retroactiva — el encargo pidió localizarla y SÍ existía

`PARCIAL:script+spec+spec_sha` no prueba ausencia de trabajo previo, y aquí no lo era:

| componente | veredicto | dónde |
|---|---|---|
| `script` | **EXISTE** | `tools/tasas_base_fase1.py:67-107` (`ACTO MAESTRA32-E18`, 31/ago/2026) |
| `spec` | **EXISTE, como nota, no como pre-registro** | `forense/notas/2026-08-31-reglas-fase1-spec.md` §(c).1 |
| `spec_sha` | **NO-ENCONTRADO** | 0 de 54 archivos de `forense/prereg-caja/` |
| corrida sellada GEN2 | **NO-ENCONTRADO** | 21 directorios `CALC-*`, ninguno de ENVIPE |

La cantidad ya estaba medida **y sellada en el motor** (`milpa/tramite.yaml:574`, `tier: FUERTE`); `tools/ya_medido.py` devuelve `MEDIDA-EN: tramite.yaml` (salida completa en el encargo archivado). Lo que faltaba era la cadena, no el número. Este acto no descubrió territorio virgen y no lo presenta como tal.

## 3 · La medición

**Estimando primario** — unidad **delito**, codificación literal `C1` = `{01,02,06}`:

| | valor |
|---|---|
| `P-C1-U1` | **0.231689** IC95 **[0.219191, 0.244462]** |
| `n` | 20 225 delitos · masa `FAC_DEL` = 23 946 194 delitos expandidos |
| escala | proporción `[0,1]`, más alto = más peso del miedo/desconfianza como razón **principal** |

Embudo completo, contado paso a paso: 40 280 filas del módulo → 24 762 delitos personales (`BPCOD 05-15`) → **22 536 no denunciados** → 20 225 en `U1` + 2 200 (`09` Otra) + 111 (`99` NS/NR) = 22 536 exacto. `N-BP1-23-BLANCO = 0`, `N-SIN-PONDERADOR = 0`, `N-SIN-DISENO = 0`.

### 3.1 · Hallazgo 1 — el código `08` vale 3.56 puntos, y nadie lo había declarado

`DELTA-C2-C1 = +0.035555`. Sobre el **mismo** universo, la tasa pasa de **0.231689** (`C1`) a **0.267243** (`C2`) según se cuente o no el código `08`, *«Por actitud hostil de la autoridad»*, como desconfianza.

GEN1 lo contó dentro. Es una lectura defendible — pero es un **juicio**, no un dato: `08` describe una conducta atribuida a la autoridad, no un estado declarado del informante. `E.1` prohíbe que GEN1 elija la codificación de GEN2, así que esta spec puso como primaria la partición que **sólo** usa los códigos cuyo texto literal dice «miedo» o «desconfianza», y **midió** lo que vale la diferencia en vez de heredarla en silencio. Los dos brazos están sellados; mesa puede quedarse con el que prefiera, sabiendo el precio.

### 3.2 · Hallazgo 2 — «los dos valores suman 1» es propiedad del RECORTE, no del instrumento

`VEREDICTO-EXHAUSTIVIDAD = EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-U1`.

La pregunta 1.23 es de **respuesta única** y tiene **diez** categorías sustantivas, no dos. De los 22 536 delitos no denunciados, **2 200 contestaron `09` (Otra)** y **111 contestaron `99` (NS/NR)**: 10.25% de las filas y **9.19% del peso** (`P-OTRA-U3 = 0.087445`, `P-NSNR-U3 = 0.004484`).

Consecuencia directa sobre la demanda: **`RES-0028` (`0.705687`) no es «el complemento medido».** Es `1 −` el primario sobre un denominador que **excluye categorías reales del reactivo**. Sobre el universo completo, la misma codificación `C2` da **0.242676**, no 0.267243. `RES-0028` queda cubierto **sólo en ese sentido**, escrito con su denominador en la unidad del `RESULT` — no como cantidad medida independiente.

### 3.3 · Hallazgo 3 — la varianza de diseño sí era identificable

`FP-201` declaró, para las cinco reglas de fase 1, *«sin campo de diseño UPM/estrato reproducible en el perímetro de este acto para ninguna de las cinco fuentes»*, y por eso su IC95 fue un bootstrap simple de filas. **Para ENVIPE 2025 eso no se sostiene:** `EST_DIS` y `UPM_DIS` están en las dos tablas, y el inventario de reactivos de la casa los confirma dentro de los archivos, no sólo en el descriptor. En `U1`: **725 estratos, 7 830 UPM**.

Esta corrida estima varianza de diseño (bootstrap de UPM con reemplazo dentro de estrato, 2 000 réplicas, `PCG64` semilla `20260909`). **83 estratos quedan con una sola UPM** tras el recorte a no-denunciantes → `METODO-IC = IC-CON-ESTRATOS-DE-UPM-UNICA`, y **el IC se lee como límite inferior de la anchura verdadera**, tal como quedó pre-declarado en §3.4 de la sellada. No se presenta un IC ingenuo como IC de diseño.

Esto **no** reabre las otras cuatro reglas de fase 1: cada fuente es suya y ninguna se toca aquí. Queda como `NC-0085`.

### 3.4 · Un defecto del descriptor, encontrado y declarado — no muerde

El descriptor declara `EST_DIS` como `Carácter(3)`, rango `001..607`, y `UPM_DIS` como `Carácter(7)`. **El archivo trae `EST_DIS` de 4 caracteres, `0001..0746`, con 739 valores distintos, y `UPM_DIS` de 5.** El descriptor está desfasado respecto de su propio microdato.

**No afecta a ninguna cifra de esta corrida**, y por una razón que conviene dejar escrita: el medidor trata `EST_DIS`/`UPM_DIS` como **llaves de texto opacas** — nunca las convierte a entero ni las re-rellena con ceros. Si las hubiera normalizado a `int` o a un ancho fijo tomado del descriptor, habría partido o fusionado estratos en silencio. El formato es consistente dentro del archivo (ancho fijo, sin espacios, verificado sobre las 40 280 y las 91 182 filas), así que la agrupación por cadena cruda es exacta.

## 4 · P3 · Adopción y consumo

### 4.1 · La prueba dirigida de consumo — **pasa**

Sonda de sólo lectura sobre el motor real (`milpa.src.emisor`), sin escribir un byte en el árbol (`git status --porcelain` vacío después):

```
cargar_reglas() -> 21 reglas · civico.denuncia.miedo_desconfianza · tier=FUERTE · situacion=SELLADA
emitir_binaria(regla, 'denuncia_con_miedo_o_desconfianza') ->
    tipo_escala     = 'binaria'
    valor_punto     = 0.294313      <-- el parámetro que el emisor EJECUTA
    valor_categoria = 'denuncia_con_miedo_o_desconfianza'
    clase           = 'MEDIDO·p(tasa base ponderada)'

RESULT-ENVIPE-DEN-P-C2-U4 = 0.29431298745731216
round(RESULT, 6)          = 0.294313  ==  valor_punto   -> True
```

Y llega hasta el final del camino: **diez corridas M ya selladas** consumen esa regla con ese punto —
`M-CIV-M-01, -02, -04, -06, -08, -09, -10, -11, -12, -13`, todas `valor_punto = 0.294313`, `grado_DD = P1 PUNTUA`.

`RESULT-ENVIPE-DEN-ADOPCION-P3 = ADOPTABLE-POR-REPLICA`, `ADOPCION-P3-DELTA = 0.0` al grano de seis decimales con que `milpa/` materializa. **La compatibilidad queda demostrada, no supuesta.**

### 4.2 · La adopción queda PREPARADA, no escrita — y éste es el bloqueo exacto

El encargo enumera el perímetro y cierra con: *«Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»* **`milpa/` no está en esa lista.** No es un olvido interpretable: el encargo hermano de `GEN2-C0-D` sí escribió *«milpa/+tablero solo las citas de P4»* cuando quiso autorizarlo. Aquí no está.

Así que la cita **no se escribe**, y P3 cierra por la vía que el propio encargo prevé (*«Si la adopción pertenece a otro acto por diseño del registro, el bloqueo exacto se registra — eso también cierra la pieza»*). `usos.tsv` se re-derivó y quedó **sin cambio** (205 filas): sin la cita, no hay adopción que registrar. Eso es correcto, no una omisión.

**El parche exacto, listo para aplicar** (una línea, `milpa/tramite.yaml:583`, el `p` NO se mueve — sigue el patrón que estrenó `ACTO GEN2-PRIMERA-SILLA` en `milpa/tramite.yaml:839`):

```yaml
      - {conducta: denuncia_con_miedo_o_desconfianza, p: 0.294313, clase: "MEDIDO·p(tasa base ponderada)", corrida0_resultado_id: RESULT-ENVIPE-DEN-P-C2-U4, corrida0_generacion: GEN2}  # ACTO GEN2-LOTE-ENVIPE-1: CALC-ENVIPE-0001 remidió esta tasa bajo GEN2 (RESULT-ENVIPE-DEN-P-C2-U4 = 0.29431298745731216) y reproduce el 0.294313 publicado al grano de seis decimales con que milpa/ materializa (delta −1.254e-08). El merge del PR que aplique esta línea es la adopción (E.2). El `p` NO se movió: se declara de dónde viene.
```

Aplicarlo es de un acto con `milpa/` en su perímetro. Queda como **`NC-0083`**.

**Advertencia para quien lo aplique:** la cita natural para `denuncia_por_otra_razon` (`RES-0028`) **no debe escribirse igual**. Ese `0.705687` no es una cantidad medida: es `1 −` el primario sobre un denominador que excluye 9.19% del peso del universo (§3.2). Adoptarlo con un `corrida0_resultado_id` lo presentaría como medido cuando no lo es. Queda como **`NC-0084`**.

## 5 · Límites declarados (§7 de la sellada, repetidos aquí)

- **Temporal.** ENVIPE 2025 mide delitos de **2024**. No valida transferencia a 2012–2024 ni cumple cortes de ola previa. El hueco temporal es **decisión de mesa** con esta nota a la vista; este acto no lo decide. → `NC-0086`.
- **No se calibró contra el marco.** Las diez celdas ENVIPE de `M` que consumen esta regla se usaron sólo como **evidencia de consumo** (§4.1), nunca para calibrar; ninguna mejora en ellas se presenta como confirmación independiente. El marcador y sus capturas no se tocaron.
- **Causalidad: ninguna.** «Miedo/desconfianza como razón principal» es lo que la persona **declaró**. Ningún `RESULT` de este lote se rotula causal.
- **Contaminación (ADR-46).** La corrida **no fue ciega**: al congelar, la sesión ya había leído los dos valores GEN1, su IC95, su `n` y **la codificación GEN1 completa**. Está declarado en §0.3 de la sellada y es la razón de que la primaria sea `C1` y no `C2`. Lo genuinamente desconocido al congelar —y lo que resultó ser el hallazgo— eran los conteos de `09`/`99`/blanco, que no aparecen en ninguna fuente leída.

## 6 · Lo que NO se corrió, y por qué no se declara cubierto

`RES-0039..0042` (`civico.denuncia.con_seguro` / `.sin_seguro`) tienen **otra apertura**: unidad delito restringida a `BPCOD = 01` (robo total de vehículo), condicionada a cobertura de seguro, con desenlace `denuncia`/`no_denuncia` — **no** razones de no-denuncia. El encargo los admitía *«solo si comparten apertura coherente y su spec quedó completa en P1»*. No la comparten y su spec no se escribió. → `NC-0087`, con `tools/medidor_denuncia_seguro_envipe25.py` ya localizado como cobertura retroactiva para el sucesor.

Tabla completa en `forense/no-corrido.tsv`, filas `NC-0083` … `NC-0087`.

## 7 · Contador

`cuenta_gen2` de `CALC-ENVIPE-0001` queda en **`PENDIENTE-DE-MESA`**. La firma que ordena el lote (9/sep/2026) **no tiene como objeto el contador** — estándar `FP-367`: autoridad + fecha + **OBJETO**. Mientras no viaje una firma explícita sobre `cuenta_gen2`, **el contador no lo cuenta, y se dice aquí** en vez de darlo por contado. No se repite el defecto de `FP-362`.

## 8 · A.13 — qué se examinó

Microdato: **2 archivos** (`conjunto_de_datos_tmod_vic_envipe2025.csv`, 40 280 filas; `conjunto_de_datos_tper_vic2_envipe2025.csv`, 91 182 filas), abiertos **por primera vez en el COMMIT-2**, nunca antes de congelar.
Codebook y metadato (COMMIT-1): manifiesto (2 entradas + 3 de documentación), 2 `diccionario_de_datos/*.csv` (542 y 611 campos), 4 catálogos, 1 `metadatos_envipe2025.txt`, la lista de 651 miembros del ZIP, y 2 PDF de cuestionario.
Inventario de reactivos: 317 718 filas, 24 063 `archivo_miembro` distintos → `spec-check` **12 OK · 0 FAIL**.
`forense/prereg-caja/`: 54 archivos, 0 aciertos de `CORR-0009` (negativo con universo declarado).
