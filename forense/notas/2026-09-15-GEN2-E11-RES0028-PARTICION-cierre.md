# E11 · Ficha sucesora de RES-0028 — partición/universo y propuesta de uso

Fecha: 15 de septiembre de 2026. `ACTO GEN2-E11-RES0028-PARTICION`, entorno
NUBE. Autoridad: `forense/encargos/2026-09-15-GEN2-E11-RES0028-PARTICION.md`,
`D11` (`forense/notas/BENCHMARK-D11-COMPLEMENTOS-Y-USO-EN-MOTOR.md` §6) y la
reserva de `NC-0085` (`forense/no-corrido.tsv:86`). **Propuesta para firma de
mesa. No adopta nada.**

No se abrió ningún byte de microdato: la reconstrucción de partición y
universo, y el punto/IC del residual, ya existen selladas por
`ACTO GEN2-MOTOR-USOS-Y-COMPLEMENTOS` (10/sep/2026) y por
`prereg-caja-ENVIPE-DENUNCIA` (9/sep/2026). Este documento las cita y
construye sobre ellas — no vuelve a medir.

**A.8** — `python3 tools/ya_medido.py civico.denuncia.miedo_desconfianza`
(corrido en el ARRANQUE de este acto, última línea):
`MEDIDA-EN: CALC-ENVIPE-0001, tramite-ola5-propuesta-v0.yaml, tramite.yaml`.
Consistente con que este acto no reclasifica ni resella la regla: solo
propone, sin ejecutar, un `corrida0_resultado_id` propio para el derivado
`RES-0028`, ya `MEDIDA-EN:` en el motor por la corrida padre.

## 1 · Partición y universo, citando lo ya reconstruido

Fuente: `forense/notas/2026-09-10-GEN2-MOTOR-USOS-Y-COMPLEMENTOS-cierre.md`
§F3 y `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md` §3.1-3.2, 6.2.

| bloque | contenido | valor / cita |
|---|---|---|
| padre | `RESULT-ENVIPE-DEN-P-C2-U4` | `0.29431298745731216`, publicado `0.294313` |
| unidad / universo del padre | persona 18+ con ≥1 delito no denunciado, `BPCOD 05..15`, colapso a persona, ponderador `FAC_ELE` | `U1`, `n=13023` |
| codificación `C2` (evento padre) | razón principal `∈{01,02,06,08}` («miedo al agresor», «miedo a extorsión», «desconfianza en la autoridad», «actitud hostil de la autoridad») | §3.1 spec |
| codificación residual | razón principal `∈{03,04,05,07}` («delito de poca importancia», «pérdida de tiempo», «trámites largos y difíciles», «no tenía pruebas») | resto de `U1`, no es el código `09` |
| excluidos de `U1` (no entran en ninguno de los dos bloques) | `09` «Otra» (texto abierto) — 2200 delitos; `99` NS/NR — 111 delitos; blanco | `U1=20225`, `U3=22536` delitos totales del recorte |
| fórmula | `q = 1 − p`; por réplica `q[b] = 1 − p[b]`; `Cov(p,q) = −Var(p)` | `BENCHMARK-D11` §3 |
| punto materializado | `q = 0.7056870125426878`, publicado `0.705687` | `demanda-resultados.tsv:30` |
| incertidumbre | IC95 del padre `[0.2830197508253073, 0.3057991950047491]` → por transformación, IC95(q) `[0.6942008049952509, 0.7169802491746927]` | mismo diseño, misma incertidumbre que el padre |
| peso de lo excluido, en `U3` | `P-OTRA-U3 = 0.087445`; `P-NSNR-U3 = 0.004484` | spec §6.2, fila `NC-0085` |

### 1.1 · Veredicto de exhaustividad — reproducido literal

`VEREDICTO-EXHAUSTIVIDAD = EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-U1` (spec
§6.2). El residual y el padre suman 1 **por construcción del recorte** —
`U1` excluye por definición `09`, `99` y blanco — no porque el reactivo
`BP1_23` sea de por sí exhaustivo en dos categorías. Bajo el universo
completo `U3` la misma codificación `C2` da **`0.242676`**, no `0.267243`.
**`0.705687` no es una cantidad medida independiente**: es `1 −` el
primario sobre un denominador que excluye categorías reales del reactivo.
Citarlo suelto como si fuera un `RESULT` medido lo presentaría como algo
que no es.

### 1.2 · Nombre descriptivo preciso del residual

El rótulo actual del consumidor, `denuncia_por_otra_razon`, es ambiguo
contra el código literal `09` («Otra», texto abierto), que es una
categoría distinta con peso propio (`0.087445` en `U3`). Dos cosas no
pueden llamarse igual: la de aquí es el resto de las **ocho razones
sustantivas de `U1`** excluyendo `{01,02,06,08}`, no el texto libre de
quien marcó «Otra».

**Nombre propuesto, si mesa adopta:** `denuncia_sin_miedo_ni_desconfianza`
(o, si se prefiere el eje positivo, `otras_razones_del_recorte_c2_u1`),
con una nota de campo obligatoria: *«complemento de C2 sobre U1; excluye
09-Otra, 99-NS/NR y blanco; no equivale al código 09»*. El rótulo actual
(`denuncia_por_otra_razon`) queda desaconsejado por la misma ambigüedad
que esta sección documenta.

## 2 · Uso concreto propuesto — sin adoptar

### 2.1 · Entrada de registro propuesta (no escrita en el TSV real)

Hoy `RES-0028` comparte fila de derivado con su padre y su columna
`corrida0_resultado_id` está `NO-DECLARADO-EN-EL-REGISTRO`
(`data/corrida0/demanda-resultados.tsv:30`). La recomendación que la
propia fila de `NC-0085` deja pendiente es exactamente ésta: darle un
`corrida0_resultado_id` propio. Si mesa firma, la entrada sería:

| campo | valor propuesto |
|---|---|
| `id` | `RES-0028` (sin cambio) |
| `corrida0_resultado_id` | `CALC-ENVIPE-0001::RESULT-ENVIPE-DEN-Q-C2-U1-RESIDUAL` (nuevo, derivado del mismo `CALC` que el padre — no una corrida nueva) |
| `tipo` | `conducta_p_derivado` (sin cambio; se conserva el rótulo `DERIVADO`, no pasa a `MEDIDO`) |
| `fórmula` citada | `q = 1 − p(C2,U1)`, mismo `payload_sha256` que `RES-0027` |
| `consumidor propuesto` | `civico.denuncia.miedo_desconfianza:denuncia_sin_miedo_ni_desconfianza` (rótulo nuevo, §1.2) o el alias actual con la nota de ambigüedad adjunta |

Esta fila **no se escribe** en `data/corrida0/demanda-resultados.tsv` por
este acto: es la propuesta que mesa evalúa. Escribirla es adopción, y
`D11` no la autoriza.

### 2.2 · Dominio de aplicación si se adopta

- **Válido:** persona 18+ con al menos un delito no denunciado de
  `BPCOD 05..15` (delito personal), dentro del recorte `U1`
  (`BP1_23∈{01..08}`). El derivado responde: de quienes dieron una de las
  ocho razones sustantivas, qué proporción dio una razón **distinta** de
  miedo/desconfianza/hostilidad.
- **No cubre:** una tasa sobre el universo completo `U3` (sería
  `0.242676`, no `0.705687`); el código literal `09` «Otra»; no se
  propaga a otra ola de ENVIPE (spec §7.1); no es un veredicto causal
  (spec §7.3); no se combina con `RES-0039..0042` (otra apertura, unidad
  delito, `BPCOD=01`, spec §7.4).
- **Incertidumbre:** comparte exactamente el IC del padre por
  transformación (§1). No se sortea como parámetro independiente ni se
  presenta como segunda confirmación.

### 2.3 · Recomendación a mesa

Dos caminos, ninguno ejecutado por este acto:

1. **Adoptar el residual acotado sobre `U1`**, con el rótulo nuevo
   (§1.2) y la entrada de registro propuesta (§2.1) — cierra `NC-0085`
   con el alcance ya documentado, sin volver a medir.
2. **Pedir un estimando sucesor sobre `U3`** si mesa prefiere que
   «otras razones» cubra la población completa del recorte (incluyendo
   `09` y `99`) — esto es un objeto nuevo, no una reinterpretación del
   `RESULT` actual, y requeriría su propia spec y corrida.

Ningún camino se ejecuta aquí. `NC-0085` permanece `ABIERTA` hasta la
firma.

## 3 · Cierre del acto

Producido: esta ficha, citando en su totalidad la reconstrucción previa
(§1) y materializando la propuesta de uso (§2) sin tocar el motor. No se
editó `milpa/tramite.yaml`, `milpa/procedencia.yaml`, `milpa/src/emisor.py`
ni `data/corrida0/demanda-resultados.tsv`. No se emitió ningún `RESULT`
nuevo. No se abrió microdato.

`NC-0085` se actualiza en el mismo commit para enlazar este documento en
vez de seguir apuntando genéricamente a «E11: reconstruir…» — el estado
permanece `ABIERTA`: la firma de adopción sigue pendiente de mesa.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Adopción de RES-0028 (escribir `corrida0_resultado_id` real, cambiar consumidor en `milpa/tramite.yaml`) | `DECISIÓN-DE-MESA-PENDIENTE` — `D11` autoriza desarrollar la propuesta, no adoptarla | `RES-0028` sigue sin `corrida0_resultado_id` propio; el motor sigue citando el alias actual | Firma de mesa sobre este documento; si adopta, ejecuta §2.1 en un acto posterior |
| Estimando sucesor sobre `U3` («otras razones» de la población completa) | `DECISIÓN-DE-MESA-PENDIENTE` — camino 2 de §2.3, objeto nuevo fuera de este perímetro | Ninguno mientras mesa no elige | Acto nuevo, si mesa prefiere ese camino sobre adoptar el residual acotado |
