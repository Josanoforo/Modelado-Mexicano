ENCARGO · ACTO MAESTRA34-L5 · GOBIERNO-DIGITAL-EVASION-AHORRO — invoca /acto
SHA de redacción: 4de5b1e. Redacta dirección (Fable), 2/sep/2026, contra v2.12. Estado: LISTO PARA LANZAR cuando la caja quede libre (PR [L] corridas v1_2 fusionado o abortado). Un solo acto de caja a la vez.
ENTORNO ASIGNADO: UBUNTU (abre ENCIG 2025, ENIF 2024, ENCUCI/ENVIPE). NO se lanza en NUBE. MODELO SUGERIDO: Opus (lote medidor, dos commits por pieza). COMPUERTA: ninguna.

FIRMAS DE MESA: DS1 (2/sep) autoriza re-medir dinero.ahorro.tiene_ahorros en ENIF 2024. Para las tres ASIGNADO restantes rige la regla de señal (v2.3) y el precedente de ADR-270/ADR-276: prior ASIGNADO contra dato.

A.8 contra 4de5b1e: motor con clase ASIGNADO vigente (no refutada): tramite.evasion_norma (0.66/0.34, situacion enfrenta_norma_percibida_inutil_o_extractiva, sancion_creible=false), tramite.gobierno_digital.coercitivo (rechaza 0.91, cobertura_formal=false), tramite.gobierno_digital.util_sin_coercion (adopta 0.71) → tres priors sin dato (E18-P1 filas 3-4: sin generador declarado). Corpus: encig25_base_datos_csv EXISTE (sección VII trámites: canal P7_3 ya usado en L1; motivos de no uso de internet y satisfacción por canal: CENSAR); enif_2024 EXISTE (ahorro formal/informal; usado_para familismo); ENCUCI 2020 EXISTE (normas, sanción percibida). Filas de codificacion-R para estas reglas: NO-ENCONTRADO por construcción (no son celdas del marco) — dicotomización se congela en la spec de cada pieza. Precedente de forma: MAESTRA34-L1 (calibración fuera del marco, entrada MEDIDO·p a la propuesta, PENDIENTE-DE-MESA).

P0 · CENSO A.4 (un commit, antes de medir): para cada regla, qué ítem del cuestionario/FD operacionaliza situación, disparador y conducta; veredicto EXISTE-SATISFACE / EXISTE-NO-SATISFACE (qué falta) / NO-ENCONTRADO con archivos examinados (A.13). Solo las EXISTE-SATISFACE pasan a P1–P4. Mapeo declarado como juicio del acto, no dictado por el dato (precedente con_registro).
P1 · gobierno_digital.util_sin_coercion — ENCIG 2025: entre quienes tuvieron un trámite disponible en canal digital sin obligación (censo decide el ítem), proporción que lo usó; ponderador y diseño de sección VII; IC95 conglomerado.
P2 · gobierno_digital.coercitivo — ENCIG 2025: entre trámites de uso digital obligatorio (censo decide; si ENCIG no distingue obligatoriedad, EXISTE-NO-SATISFACE y se declara), rechazo/abandono. Escala: proporción; compara SIGNO y razón contra P1 en la misma corrida (A-bis 3), nunca contra el 0.91/0.71 en otra escala sin enlace.
P3 · evasion_norma — ENCUCI 2020 (o ENVIPE si el censo lo prefiere): proporción que declara incumplir una norma percibida como inútil cuando la sanción es improbable; si no hay ítem de "sanción improbable", se mide la tasa base y se dice.
P4 · dinero.ahorro.tiene_ahorros — ENIF 2024: proporción con ahorro (formal ∪ informal; censo fija la definición) sobre adultos; entra como enmienda de re-medición a la regla (misma id, ola 2024) con la de 2005-06 conservada como serie.
Cada pieza: COMMIT-1 congela variables, universo, ponderador, dicotomización, escala; frase de sello «el primer resultado que produzca este procedimiento es el que se reporta». COMMIT-2 resultados; entrada MEDIDO·p en la propuesta, tier PENDIENTE-DE-MESA; si refuta el prior por más del doble o mitad, cabecera REFUTADA-POR-DATO propuesta (mesa sella). CIEGO a corridas-M/L. Una pieza que PARA no tumba el lote.
PERÍMETRO: milpa/tramite-ola5-propuesta-v0.yaml (entradas nuevas) · tools/ (scripts) · forense/notas/ (censo, specs, cierre) · forense/hallazgos.md · tablero · A.3 · cascada. NO toca milpa/tramite.yaml ni prereg-duelo-v2. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR: deriva al arrancar. CONTADOR: priors ASIGNADO con dato +N (hasta 3) · re-mediciones +1 · declara el real.
LO QUE NO HACE: no carga al motor (sello de mesa, formato RH al cierre); no toca la cívica; no abre Ola 6.

---

## CONSUMIDO

Ejecutado por `ACTO MAESTRA34-L5 · GOBIERNO-DIGITAL-EVASION-AHORRO` el
2/sep/2026 en entorno **UBUNTU**, con la skill `/acto` (`ADR-237`). `ADR-286`.
Rama `acto/maestra34-l5-gobierno-digital-evasion-ahorro`, **PR #467** (abierto, no
fusionado: el merge es de mesa).

`COMPUERTA: ninguna` — declaración explícita, no dispara verificación. La
condición de lanzamiento «caja libre» se verificó **por producto**:
`forense/notas/2026-09-02-L-corridas-v1_2-cierre.md` y
`forense/prereg-duelo-v2/PAQUETE-L-v1_2/` presentes en `origin/main` (PR #465
fusionado), 0 PR abiertos. `SHA de redacción 4de5b1e`; base real `29ab80a`,
**6 commits por delante** — perímetro re-derivado y las cinco premisas del A.8
re-verificadas contra el árbol real: **las cinco verdaderas**, incluida «filas
3-4 de `MAESTRA33-E18`·P1 sin generador declarado», que resultó exacta.

**Tres de las cuatro piezas midieron; la cuarta paró con veredicto razonado.**

- **P0 · censo A.4** (un commit, antes de medir), sobre cuestionario/FD y listas
  de columnas, con denominadores contados **sin cruzarlos nunca contra el
  desenlace**: P1 `EXISTE-SATISFACE con mapeo declarado`, P2
  `EXISTE-NO-SATISFACE`, P3 `EXISTE-SATISFACE` en ENVIPE 2025, P4
  `EXISTE-SATISFACE`.
- **P1 · `tramite.gobierno_digital.util_sin_coercion`** (ENCIG 2025) — **tres**
  commits, no dos: la guardia que la spec congeló disparó antes de haber
  resultado y forzó una enmienda declarada. **p̂ = 0.673393, IC95
  [0.663165, 0.683910], n = 20 203 trámites.** Prior ASIGNADO `0.71`, razón
  **0.9484** → **NO refutado**; se propone `CONFIRMADA-EN-MAGNITUD`.
- **P2 · `tramite.gobierno_digital.coercitivo`** — **PARA**, y no tumbó el lote.
  Tres faltantes, el tercero sin arreglo dentro de ENCIG: sin ítem de
  obligatoriedad en 483 columnas de 2025 ni en ~100 000 de cinco olas; `P7_3=7`
  es fracaso y no rechazo voluntario; y `cobertura_formal: false` selecciona
  fuera del universo, porque a la sección VII solo se entra habiendo hecho el
  trámite. Por esto último **no se propone sucesor en ENCIG**. En consecuencia,
  la comparación de SIGNO y razón contra P1 que este encargo pedía **no se hizo**,
  y tampoco se comparó nada contra el `0.91` en otra escala.
- **P3 · `tramite.evasion_norma`** (ENVIPE 2025, no ENCUCI 2020 — el censo la
  prefirió porque `BP1_20`/`BP1_23` son conductuales y `AP5_11` es actitudinal).
  **p̂ = 0.562774, IC95 [0.551982, 0.573448], n = 40 280 delitos.** Prior `0.66`,
  razón **0.8527** → **NO refutado**.
- **P4 · `dinero.ahorro.tiene_ahorros`** (ENIF 2024, firma `DS1`). **p̂ =
  0.642080, IC95 [0.630602, 0.653440], n = 13 502 adultos 18+.** Hallazgo no
  buscado: el **ahorro informal casi duplica al formal** (0.561920 vs 0.284927).
  La razón 3.67× contra la cifra de 2005-06 **excede** el umbral de «más del
  doble» y **no dispara** `REFUTADA-POR-DATO` — decisión congelada en la spec
  **antes** de medir, por acervo-contra-flujo y por universo.

**Defecto encontrado en un acto ya sellado, reportado y no reparado** (`FP-237`):
`ID_TRA` no es la llave de `encig2025_04_sec_7.csv` — lo es `(ID_TRA, NT_TIPO)` —
y la fila `TRA-M-13` de `codificacion-R-v1_0.tsv` (`ACTO MAESTRA34-L1`) afirma
duplicados exactos que no existen; su deduplicación descartó 3 835 eventos reales.
`forense/prereg-duelo-v2/` está fuera del perímetro de este acto.

**Dos desviaciones de la letra del encargo, ambas declaradas.** (1) El CONTADOR
del encargo insinuaba «hasta 3 priors +1 re-medición»; el real es **+2 de 3 y
+1**, porque P2 no tiene dato por defecto de la fuente y porque
`dinero.ahorro.tiene_ahorros` **ya estaba MEDIDA**, no ASIGNADA. (2) El encargo
pedía para P4 «misma id, ola 2024»; se usó `dinero.ahorro.tiene_ahorros_enif2024`
con los campos `misma_regla_motor` y `enmienda_de`, porque el acumulador ya
contiene una entrada con la id base y dos homónimas en la misma lista serían
ambiguas — es la convención que ese archivo ya usa para
`tramite.mordida.con_registro_encig2025`.

**Perímetro respetado**: solo `milpa/tramite-ola5-propuesta-v0.yaml`, `tools/`,
`forense/notas/`, `forense/hallazgos.md`, el tablero de firmas, A.3 y la cascada.
`milpa/tramite.yaml` y `forense/prereg-duelo-v2/` **intocados**; no se cargó nada
al motor; no se tocó la cívica; no se abrió Ola 6. Este acto no descargó nada
(anti-PR#77 no aplica). `python3 tests/check.py --baseline` → **VERDE**.
