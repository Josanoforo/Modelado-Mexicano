# M19 · ENCUCI 2020 · confianza con puente frente a sin puente, por confianza en la policía y por dominio

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-CALC-ALTERNOS-LOTE-1` (0-bis `795b1053`), fila 53 de
`canon/mapa-instrumentos-alternos-v1_0.tsv`. Firma R08 A2 (b), 28/sep/2026:
«se encargan CALC-caja descriptivos para … M19 (ENCUCI 2020, tras reconciliar
conf.06). Cada spec declara que consume el HOLDOUT de su momento». Un CALC:
`CALC-ALT-M19-ENCUCI2020-0001`. No adopta; no es retador; sin θ.

## Compuerta conf.06: reconciliada antes de congelar

`canon/glosario-v*.md` (línea de conf.06): «Cerrado por ADR-64, 5/ago/2026.
No competían: son tres reactivos distintos de la pregunta 5.1, ENCUCI 2020,
ponderador `FAC_SEL`, los tres al corte ≥8/10». Esta spec usa exactamente esa
convención (reactivo por reactivo, corte ≥ 8, `FAC_SEL`) y no mezcla
reactivos en una sola «cifra de confianza».

## Qué ya está medido y no se repite (E.5)

`ya_medido.py R8.3` → `NUNCA-MEDIDA` (en GEN2). Los CALC ENCUCI sellados
(`CALC-ENCUCI-0001`, `CALC-ARBITRO-MARGINALES-2-ENCUCI2020-0001`,
`CALC-ENCUCI2020-*`) miden pago informal, contacto y reactivos de las
secciones 6–7; ninguno usa `AP5_1_*` ni `AP5_3_3` (barrido de `spec.yaml`).

## Estimando, unidad, escala, universo

- **Unidad:** persona elegida de 15 años y más (`ENCUCI_2020_SEC_4_5`).
- **Escala:** proporción ponderada; diferencia pareada en puntos de
  proporción.
- **Universo:** filas con `FAC_SEL` > 0, `EST_DIS` y `UPM_DIS` presentes;
  por reactivo, código sustantivo 00–10; `99` fuera y contado.
- **Reactivos (A.15, FD pp. 21–22):**
  - `AP5_1_1` — «5.1 … ¿cuánto confía en… 1. la mayoría de las personas?»
    (SIN PUENTE). Evento: `≥ 8` (`{8, 9, 10}`).
  - `AP5_1_2` — «2. la mayoría de las personas que conoce personalmente?»
    (CON PUENTE). Evento: `≥ 8`.
  - Diferencia pareada `p(AP5_1_2 ≥ 8) − p(AP5_1_1 ≥ 8)` sobre filas
    sustantivas en ambos.
- **Grupos:** `AP5_3_3` «5.3 … 3. Policía»: `CONFIA-POLICIA = {1 Mucha,
  2 Algo}`, `NO-CONFIA-POLICIA = {3 Poca, 4 Nada}`; `5 No aplica`, `9 NS/NR`
  quedan fuera del grupo (no de la muestra). `DOMINIO` (FD, campo 51):
  `U Urbano`, `C Complemento urbano`, `R Rural`.
- **Contraste pre-registrado (el falsador de R8.3 en proxy):**
  `p(AP5_1_1 ≥ 8 | CONFIA-POLICIA) − p(AP5_1_1 ≥ 8 | NO-CONFIA-POLICIA)`.
- n mínimo por celda 30.

## Ponderador y diseño

`FAC_SEL` (FD: «ponderador que se utiliza … población mexicana de 15 años y
más»), estrato `EST_DIS`, UPM `UPM_DIS`. IC95 bootstrap de UPM con reemplazo
dentro de estrato, 2 000 réplicas, semilla PCG64 `20260928`, percentiles,
réplicas compartidas (pareado). Lectura por `tools/corpus_loader.py::cargar`
(caché Parquet con constancia), fijado por sha256.

## Agregador (E.1)

Razón de sumas ponderadas por celda; ninguna agregación entre celdas.

## Pre-registro: qué pasa si el falsador no refuta

Falsador de R8.3 (`hitoD-preregistro-v2_0.md`, verbatim en
`hitoD-R8_3-especificacion-v1_0.md` §0): «donde el riesgo de fraude baja
(enforcement creíble), la confianza en desconocidos debe subir aunque no haya
puente. Si no sube, es rasgo».
- IC95 del contraste enteramente > 0 → la confianza SIN PUENTE es mayor
  donde se confía en la policía: **consistente con «cálculo»**, con la
  reserva de método común (desenlace y grupo del mismo informante sesgan el
  contraste hacia arriba, igual que el eje 1 del abridor GEN1).
- IC95 que cubre 0 o < 0 → **no sube**: consistente con el abridor GEN1
  (rasgo). No se re-especifica el corte ni el grupo.
No adjudica R8.3 (descriptivo, proxy confiar ≠ transar); la lectura es de
mesa.

## Auditoría v2.16

- **Unidad:** persona 15+. **Escala:** proporción ≥8/10.
- **RETROSPECTIVA:** ENCUCI 2020, ola vista.
- **¿Incentivo o psicología?** Confianza declarada (psicología); el grupo
  de policía es percepción, no enforcement exógeno.
- **¿Clase media urbana?** Se reporta por `DOMINIO` (urbano, complemento,
  rural) para no hablar sólo de la ciudad.
- **HOLDOUT gastado: `M19`** (rol HOLDOUT en
  `milpa/catalogo-momentos-v0_1.tsv`). Censo de familias 2027 antes de
  gastar (R01 (b)): 0 menciones de M19/R8.3 en 140 archivos de
  `forense/analisis/familias-2027` (control positivo `ENIF`: 66). Lo
  consumido queda RETROSPECTIVA y no vuelve a servir como prueba.
  `holdout_gastado = M19`.
