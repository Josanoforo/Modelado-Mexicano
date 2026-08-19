# Nota · ACTO B2-SEMANTICO — la fase semántica de BARRIDO-2 (C4/C5/C6)

**Fecha:** 2026-08-18 · **Rama:** `b2-semantico` · **PR:** #268 (borrador, no fusionado)
**Base:** `origin/main = f3d3f95` (fusión de `PR #263`). **ADR:** `ADR-106`, `ADR-107`.
**Encargo:** `forense/encargos/2026-08-18-B2-SEMANTICO-C4-C5-C6.md`. **Ley:** encargo madre §17-§23.

Entorno (A.2, tres partes): sin `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` (local, Ubuntu/WSL2);
`unshare -Urn -- true` termina 0 y el namespace no alcanza `1.1.1.1:53`; `ls data/raw/ | head -1`
devuelve `20260813130000.export.CSV.zip` — corpus montado, 273 entradas en `data_raw` y 70 en
`descargas_mx`. Toda curación corrió bajo `unshare -Urn`.

---

## 1 · Dos premisas del relevo que no se sostuvieron

La regla aplicada es de `instrucciones-proyecto-v2_10.md`: quien ejecuta verifica las premisas
antes de ejecutarlas, y encontrar una mal fundada es un entregable.

### (a) «Bloqueo real: identidad (0/39 `id_manifiesto`→payload)» — describe otra columna

El relevo daba por bloqueada la absorción de M-APERTURA por un fallo de identidad. Medido:

```text
ids únicos declarados en lista-apertura (excluido el literal NO_DETERMINADO): 20
  contra ledger-inspecciones-barrido2.tsv (payload_id)      20/20
  contra reportes-inspeccion-barrido2-v1_0.tsv (payload_id) 20/20
  contra data/manifiesto.yaml (^ id: <token>)               20/20
```

39 de 41 pares resuelven, y los 2 que no son el mismo placeholder. La cifra «0/39» **sí existe**,
pero es de otra columna: `relaciones.tsv.id_manifiesto` en las 19 filas `INDEXADO-NO-DESCARGADO`.
Ahí, **12 traen `NO_DETERMINADO`** y las **otras 7 apuntan al cuestionario**
(`cses5_…_cuestionario` ×3, `za6980_q_mx` ×2, `za5900_q_mx` ×2) cuando lo que abre la celda es el
codebook o el microdato. Ninguna apunta al payload que la abriría: 0 de 19.

Ese 12/7 explica **todo** lo demás. `via_capa2.py` sólo promueve cuando `id_manifiesto` resuelve a
un payload `COINCIDE`; por eso las 12 se quedaron en `capa2/capa3 = NO_REFERENCIADO`, y las 7 que
citan el cuestionario sí se promovieron y son **exactamente las 7** que hacían fallar la condición
de aperturas absorbidas de T23 antes de este acto.

### (b) `FP-46` tiene denominador 20, pero `SI_O_REFERENCIADO` son 22

`relaciones.tsv` tiene hoy **199 filas** (la nota de `FP-24` se derivó contra 197) y **22**
`SI_O_REFERENCIADO`. Los 20 históricos reproducen exactos (`ENSAFI 9 · ENFIH 8 · ENBIARE 3`); las 2
restantes son `N14` con `fuente_canonica_normalizada` literal `01-` y `02-` — el normalizador truncó
`01-SintesisMHB.pdf` y `02-Heredabilidad TLP MHB.pdf`. Es el defecto que
`2026-08-17-b2-derivaciones-c4.md` §2 ya había descrito. No entran al denominador ni se descartan
callando: son `FUENTE_CANDIDATA` con `id_manifiesto=NO_DETERMINADO` y no tienen material que abrir.

### (c) Un tercer error del relevo, mecánico y fatal

El relevo pedía escribir `decision_mesa_id = FP-24/ADR-93`. Ese valor **no existe**: el enum
congelado de `barrido2-semantic-proposal.schema.json` es `["FP-24","NO-APLICA"]`, su `allOf` obliga
a `NO-APLICA` cuando `dependencia_fp24=NO`, el preflight del integrador lo repite y T23 regla 17 lo
exige por separado. Escribirlo revienta tres validadores a la vez. La cita de `ADR-93` va en
`razon_gate`, que es texto libre de 160. Hay prueba dirigida:
`test_fp24_no_con_decision_mesa_poblada_es_inconsistente`.

### (d) Otras dos cifras del relevo, corregidas

`ADR` vigentes eran **105**, no 104 (`canon/gobernanza-v1_15.md:2`, receta de T15: 105 únicos, sin
huecos), así que este acto usa 106 y 107. Y `ESTADO-SPLIT` **no** ha fusionado:
`estado-programa-v1_10.md:101` sigue siendo una sola línea de 31 462 caracteres, de modo que la
cascada va a `:27` y `:101` como siempre, cláusula por cláusula (FP-48).

---

## 2 · Lo que había que arreglar antes de curar nada

### La cascada de cobertura ocultaba la segunda entrada de programa

`resolve_sources` era de **primer match**: `R1` acierta con el `id_manifiesto` que las relaciones ya
declaran y corta, y `R7-SLUG-DE-PROGRAMA-INEGI` vive detrás de `if not payloads`. Resultado medido:
ENFIH y ENBIARE resolvían a **un** payload mientras el ledger tiene **dos**. La segunda entrada no
la cita ninguna relación — y es justo la que `ADR-93` exige poder evaluar.

Se adoptó la **unión declarada `R1 ∪ R7`**, autorizada por mesa antes de tocar el código. Delta
medido y acotado: 8 de 77 fuentes, todas INEGI (`ENASIC 1→3`, `ENBIARE 1→2`, `ENCIG 1→37`,
`ENCUCI 1→2`, `ENFIH 1→2`, `ENIF 1→22`, `ENOE 25→36`, `ENVIPE 1→76`). ENSAFI sigue en 1, que es lo
correcto. Fuentes `CON-MATERIAL` sigue en 27 y `relaciones_con_material` en 116: la unión enriquece
fuentes ya cubiertas, no reclama ninguna nueva.

### Las 199 fichas del curador salían sin la necesidad escrita

`escribe_paquetes_de_relacion` leía `descripcion` u `objeto_modelo`; la columna es
`objeto_modelo_origen`. Las **199 de 199** fichas decían `necesidad_texto=NO-DETERMINADO`: el curador
recibía el expediente sin el enunciado de lo que tenía que adjudicar. Además la tabla se indexaba
como `dict` por `necesidad_id` y trae 37 filas para 33 necesidades, así que `N16/N17/N19/N27`
perdían uno de sus dos objetos. Tras corregir: 0 de 199.

### Las 17 absorbidas no eran alcanzables desde su ficha

16 de las 17 declaran un payload que la cobertura de su fuente no ofrece. Se añadió
`R10-PAYLOAD-DECLARADO-EN-LISTA-APERTURA` como unión **por relación** (§18.3 manda unir «por
identidad vigente»), y la regla compuesta queda escrita, de modo que se ve cuándo la fuente no
aportó nada: `R0-SIN-CANDIDATO-MATERIAL+R10-…`. Tras el cambio: 0 de 17 sin su payload.

### Faltaban las dos fases que el propio módulo prometía

El docstring de `tareas_barrido2.py` declaraba una fase `tareas` que «convierte la elección del
curador en expediente y sólo acepta lo que puede volver a verificar por hash». No existía; el módulo
sólo exponía `fuentes` y `paquetes`. Se escribió con esa semántica — **ingiere, no enumera** — y con
ella `propuestas`, que produce las 22 columnas del §17. Cadena de verificación por fila:

```text
e2_record_id   -> presente en el fragmento del payload candidato
               -> record_sha256 coincide con el declarado
registro E2    -> (representacion, objeto_tipo, estado, privacidad, frontera)
                  identifica UNA fila de reporte durable   [400/400 único, 0 ambiguo]
representacion -> fila de ledger con mismo payload_id y sha256
representacion -> descriptor TASK-B2-*.json, hasheado en vivo  [672 indexados, 0 faltantes]
```

---

## 3 · Curaduría y supervisión (C4)

Tres curadores etapa-2 sobre particiones disjuntas de 37 relaciones (17 M-APERTURA + 20 pares),
leyendo el índice E2 completo por fragmento. No se les dio la lista histórica de 20 ni el rótulo
`FP-46`: juzgan material contra necesidad, que es lo único que el §17 les deja juzgar.

**La supervisión no se delegó a otro agente.** Se corrió aquí, con comando, sobre las 37:

| | |
|---|---:|
| ELEGIDO con `record_id` existente y `record_sha256` coincidente | **23 / 23** |
| negativos con los tres campos de identidad vacíos y frontera declarada | **14 / 14** |
| fallos de identidad | **0** |

Ningún curador inventó un identificador. **Dos veredictos se revocaron**, ambos `radio_confianza`:
`REL-72ff714a` (ISSP `za6980 V35`, «People can be trusted or can't be too careful») y
`REL-51392f82` (ENBIARE `PB1_01`) pasan de `EXISTE-SATISFACE` a `EXISTE-NO-SATISFACE`. Un ítem de
confianza generalizada da **un polo**; el radio exige el contraste conocidos/desconocidos, y el
propio curador del ISSP lo escribió: «la batería no gradúa el radio». Fail-closed: la duda rechaza.

Eso deja un resultado sustantivo, no sólo un rechazo: **en el universo barrido no hay hoy instrumento
que gradúe el radio de confianza**, que es lo que `ADR-20` supuso medible.

### `FP-46`, adjudicada por la condición literal de `ADR-93`

> «cada `objeto_evidencia` conserva su fila; la gemela `NO_DETERMINADO` se enlaza **SOLO si su objeto
> es evidenciable con una entrada distinta del manifiesto**»

Para las 20, el gemelo `SI` ocupa **una sola** entrada, y es la misma de la que el curador tomó el
objeto. La pregunta entonces es si ese objeto existe **también** en otra entrada:

| fuente | filas | entrada del gemelo | entrada distinta | ¿el objeto está también ahí? | veredicto |
|---|---:|---|---|---|---|
| ENFIH | 8 | `enfih2019_fd_xlsx` | `enfih2019_bd_csv_zip` (696 obj. E2, 0 exc.) | **sí** — 527 nombres comunes; `P11_1_5` y `P8_55` en ambas | **condición SATISFECHA** |
| ENBIARE | 3 | `enbiare2021_fd_pdf` | `enbiare2021_bd_csv_zip` (357, 0) | **sí** — 305 comunes; `PB1_01`, `PB2_1`, `PA6` en ambas | **condición SATISFECHA** |
| ENSAFI | 9 | `ensafi2023_bd_csv_zip` | — | **no existe** otra entrada en todo el manifiesto | **condición NO satisfecha** |

Las cinco entradas siguen declarando en el manifiesto «No se abrio ni extrajo». Este barrido deja ese
rótulo factualmente falso: las abrió las cinco, a E2, con 0 excepciones.

**`FP-24` derivada: 0 de 37.** La unidad es la propuesta (`ADR-92(c)`, §17) y está prohibido derivar
la dependencia de pertenecer a la lista histórica. Las 20 son decidibles con evidencia
fuente/objeto-específica, luego `dependencia_fp24=NO`. El §22 y el §28 admiten ese cero, y coincide
con lo que `2026-08-17-b2-derivaciones-c4.md` §2 ya sostenía por su cuenta.

**Adjudicar no es enlazar.** Que 11 satisfagan la condición no promueve su `capa2`: eso lo hace
`via_capa2.py` y exige `id_manifiesto` resuelto, que es precisamente lo que sigue roto (§1a).

---

## 4 · Integración (C5)

`integrate.py --barrido2`, vía fail-closed con journal y rollback. Ninguna edición manual de TSV.

```text
preflight   ok:true · 37 propuestas · 37/37 INTEGRADA · 0 errores · 0 PROPUESTA_ALTA
--apply     changed: baseline.json, bootstrap-semantico, evidencias, relaciones,
                     trabajo-semantico, utilidad-modelo
2ª corrida  changed: []  · hashes del registro byte a byte iguales · decisiones idénticas
T21         verde antes y después
```

**High path: no se construye.** El §19 lo condiciona a que exista al menos una `PROPUESTA_ALTA`
validada, y hay 0. Se registra «0 altas propuestas» y se sigue, que es lo que el §19 manda.

### M-APERTURA absorbido (§18)

Las 17 salen todas de `INDEXADO-NO-DESCARGADO`: **6** `EXISTE-SATISFACE`, **4**
`EXISTE-NO-SATISFACE`, **7** `NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO`. Violaciones del §18.8 tras
el acto: **0**. Las únicas 2 filas que conservan `INDEXADO-NO-DESCARGADO` en todo `relaciones.tsv`
son las 2 de `destino=PROPUESTA-A-COLA`, que no tienen payload en el ledger y llevan denominador
propio.

Un negativo **no se cae del expediente**: se ancla a la representación que de verdad se recorrió, con
la frontera del curador escrita. El §22 falla explícitamente un «negativo sin frontera», y un
negativo sin universo declarado no significa nada.

### Los dos hallazgos sustantivos

- `REL-08af2a45` (`N28` → `R8.1`, «comité con monitoreo + sanción visible → contribuye; sin ellos,
  free-riding») encuentra en IEPEP `PB56 "Aportación APF"` **el desenlace exacto de la regla**, con
  comité (`PB18-PB23`), monitoreo por quejas (`PB55_1/2`) y participación (`PB52`) en el mismo
  instrumento.
- `REL-9dfab617` (`N12` → `G5.familismo_apoyo`) obtiene en ISSP `za6980 V22` («¿a quién recurriría
  por ayuda en casa estando enfermo?», que separa familiar cercano, lejano, amigo, vecino y compañero)
  un reactivo directo para un coeficiente que seguía sin instrumento.

Reserva sobre `R7.1` (CSES, 2 filas): el objeto citado es el **ancla de respuesta** del reactivo, y
el `.csv` de microdato no trae ninguna columna con ese nombre (0 coincidencias sobre 607 registros).
La celda queda abierta con material documentado, pero **el mapeo ancla→columna no está establecido**.

---

## 5 · Cableado y cierre (C6)

`build_cableado.py` — ensamblador determinista y nada más (§21): no decide correspondencias, no lee
N1-N33, y cada celda se copia de un producto que otro paso firmó. Mantiene copia **propia** de las 26
columnas, separada de la de `tests/check.py`, para que un error de cabecera no se valide a sí mismo
(el defecto escritor-validador que `ADR-103` ya pagó); `test_build_cableado.py` compara ambas.

```text
data/cableado-universo-v1_0.tsv   37 filas · 26 columnas · 0 celdas vacías
                                  0 celdas >160 · 0 rutas absolutas · 0 errores
python3 tests/check.py --require-cableado   ->  T23 T-CABLEADO [ ok ]
python3 tests/check.py --baseline           ->  19 FAIL · 129 WARN, LÍNEA BASE VERDE
```

Las mismas 19/129 de **antes** del acto: ni una entrada nueva, y sin `--freeze`.

`FP-35` ejecutada: `INFRAESTRUCTURA-v1_0.md` gana **Dominio 3-bis** (cobertura material) y
**Dominio 4-bis** (semántica, integración y cableado), cada tabla con vía de escritura, contrato,
lectores y trampa conocida. Su condición era observar los mecanismos reales, y sólo se cumplió al
correrlos de punta a punta aquí.

PRISMA semántico y PRISMA de M-APERTURA: `data/curacion-universo/prisma-semantico-barrido2.md`,
derivados por script, cada cifra con denominador y comando.

---

## 6 · Lo que queda abierto, dicho por su nombre

1. **La identidad de las 19 sigue rota.** 12 con `id_manifiesto=NO_DETERMINADO` y 7 apuntando al
   cuestionario. `_apply_layer4` escribe `capa4`, **nunca** `id_manifiesto`, así que corregirlo no
   cabía en la vía fail-closed de capa 4 de este acto. Mientras siga así, `via_capa2.py` no puede
   promover su `capa2/capa3` y esas celdas quedan con `capa4` medida sobre `capa2=NO_REFERENCIADO`.
   Necesita acto propio con perímetro en `relaciones.tsv` y vía declarada.
2. **`FP-26` no se cierra**: es de mesa, con sus ocho etapas. El cierre de la fase semántica de
   BARRIDO-2 es precisamente la condición que arma su `DISPARADOR-B` (`ADR-101(h)`), que incluye la
   re-verificación `M2/M4/M5` — condición de `ADR-100(9)` y de `FP-01`, que está FIRMADA
   *condicionada* a esa re-verificación al cierre de BARRIDO-2. **Esa re-verificación es de
   dirección, no de este ejecutor**, y queda señalada aquí para que no se pierda.
3. **`FP-56`** (ocho refutaciones sin objeto) sigue ABIERTA. Su perímetro es
   `milpa/refutations.yaml`; este acto no toca `milpa/` y no la bloquea.
4. **Las 2 filas espurias** `01-` / `02-` siguen en `relaciones.tsv` como `FUENTE_CANDIDATA` sin
   material. Documentadas, no barridas.
5. **La suite de `tools/curador_registro/tests/`** trae 13 failures + 2 errors **preexistentes**, con
   conjuntos de nombres idénticos antes y después de este acto (diff vacío). Viven en los caminos
   T0/`produccion`/`semantic_run`; ninguna la introduce este acto y ninguna se tocó.

---

## 7 · Auditoría de medición sobre México

**Cero.** Este acto no mide nada sobre México: no corre una estimación, no toca `milpa/`, no mueve el
contador de coeficientes en escala del modelo, que sigue **0 de 15**. Lo que produce es cobertura
semántica — qué reactivo de qué instrumento abierto responde a qué necesidad — y eso es insumo de
medición, no medición.
