# Sorteo del marco-M v1.1 — `ACTO MAESTRA33-B2 · MARCO-M-SORTEA-v1_1` (ACTO B″), resultados

## Pre-registro del primer commit (antes de correr el PRNG)

- `SHA_A` (dado literal por el encargo, no re-derivado): `af41796f50baad1737987b7e9a1e737c38ab85f2`. Verificado: (a) `git merge-base --is-ancestor af41796f50baad1737987b7e9a1e737c38ab85f2 origin/main` → ancestro; (b) `git show af41796 --stat` → `Merge pull request #410 from Josanoforo/claude/maestra32-e20-lote-nube-elu7me` — "ACTO MAESTRA32-E20: Load 4 rules, re-emit P1, freeze framework M", que es exactamente el commit que escribe `forense/prereg-duelo-v2/marco-M-congelado-v1_1.tsv` y `CONGELADO-M-v1_1.sha256` (`git log --oneline -- forense/prereg-duelo-v2/marco-M-congelado-v1_1.tsv forense/prereg-duelo-v2/CONGELADO-M-v1_1.sha256` → un solo commit, `77939ce P2 A'' MARCO-M-CONGELA-v1_1: 27 filas, N_elegibles=22 bajo F-DD`, contenido en ese merge). Coincide con la `SHA de redacción` que el propio encargo declara.
- `scope_id = "MARCO-M-v1_1"` (dado literal por el encargo — distinto del `"MARCO-M-v1"` de B′, así que la semilla no puede coincidir con la de B′ ni con la del `ACTO B` original por construcción, §3.4 del reglamento).
- Semilla derivada por `sorteo_v2.semilla_desde_sha_merge(SHA_A, "MARCO-M-v1_1")` (misma función, `sorteo_v2.py:191`, importada sin editar — vía `sorteo_marco_m.py`, que ya la reexporta): **`34354141898495593251517379743390345279`**.
- `N_elegibles`: leído de `forense/prereg-duelo-v2/CONGELADO-M-v1_1.sha256` → `N_elegibles=22`. sha256 recomputado de `marco-M-congelado-v1_1.tsv` (`8e6459dd49869063986daa16cfbb8067575ee7c747e3cadd6a35f1b51d582477`) coincide byte a byte con el declarado en ese archivo. **Control PASA** — sin este control no habría corrida.
- **Hallazgo, no decisión de este acto — columna de elegibilidad correcta.** `marco-M-congelado-v1_1.tsv` trae DOS columnas de elegibilidad: la legacy `elegible` (23 filas `SI`) y la nueva `elegible_v1_1` (22 filas `SI`, bajo el criterio F-DD de `ADR-237`: `(transferencia==SI) AND (en_corpus==SI) AND (la estadística tiene regla en cargar_reglas() post-P0)`, según el propio sidecar `CONGELADO-M-v1_1.sha256`). Esta junta ya fue adjudicada por `FP-208`/`ACTO MAESTRA33-E2 · AGENTE-DESPACHO-1` al encolar este encargo, y el encargo mismo declara `N_elegibles esperado 22` — coincide con `elegible_v1_1`, no con `elegible`. Este acto sortea sobre `elegible_v1_1`. `sorteo_marco_m.cargar_marco_m` (v1_0, no editado) no conoce esta columna y no se usa contra este archivo — ver `sorteo_marco_m_v1_1.py`.
- **Hallazgo, no decisión de este acto — columna `estrato`.** De las 22 filas elegibles, 21 traen `estrato=PENDIENTE` (valor placeholder — las celdas de transferencia que `ACTO MAESTRA32-E15 · MARCO-M-CORRIGE-Y-CENSA` censó no llevaban `estrato` propio, a diferencia de `TRA-M-01`/`TRA-M-02` originales) y solo `TRA-M-02` trae un valor real (`tramite|P1|MEDIA`). El mecanismo de `sortear()` trata `PENDIENTE` como un estrato válido más (agrupa por el valor literal de la columna, sin juzgarlo) — este acto no reclasifica ni inventa un `estrato` mejor: reporta el dato tal como el congelado lo trae, y dirección decide si vale la pena una estratificación real para v1.2.
- Regla de tamaño (`ADR-231` §e, `forense/notas/2026-08-31-marco-M-spec.md`, fijada por `MAESTRA32-E13` antes de ver ningún `N` — la misma función `regla_de_tamano`, no editada, reutilizada tal cual la usó B′): `N≥30 → n_sorteo=15`; `15≤N<30 → n_sorteo=ceil(N/2)`; `N<15 → sin sorteo`. Con `N_elegibles=22`: **`n_sorteo = ceil(22/2) = 11`**; **`cuota_max = floor(0.20·11) = 2`**. A diferencia de B′ (`N=2<15`, identidad), aquí `N=22≥15`: el PRNG **sí** corre.
- Clasificación F-DD por celda (`ADR-237`): ya congelada en la columna `grado_DD` de `marco-M-congelado-v1_1.tsv` para cada fila (no se deriva de nuevo en este acto — sería redescubrir lo que `MAESTRA32-E20` ya selló). Las 22 filas elegibles traen las 22 `grado_DD=P1 PUNTUA` (consistente con el criterio de elegibilidad, que ya excluye por construcción las 5 filas `P0 VERIFICACION-NO-PUNTUA` de calibración — esas 5 se conservan en el archivo pero fuera del universo sorteable). Este acto reporta el valor `grado_DD` real de cada celda que salga sorteada, no lo asume.
- Invocación exacta a ejecutar:
  ```python
  from sorteo_marco_m_v1_1 import cargar_marco_m_v1_1, semilla_desde_sha_merge, regla_de_tamano, sortear_marco_m

  SHA_A = "af41796f50baad1737987b7e9a1e737c38ab85f2"
  semilla = semilla_desde_sha_merge(SHA_A, "MARCO-M-v1_1")
  marco = cargar_marco_m_v1_1()  # marco-M-congelado-v1_1.tsv, filtrado elegible_v1_1=='SI', assert n == N_elegibles de CONGELADO-M-v1_1.sha256
  n_sorteo, cuota_max = regla_de_tamano(len(marco))
  resultado = sortear_marco_m(marco, n_sorteo=n_sorteo, cuota_max=cuota_max, semilla=semilla)
  ```
- Semillas anteriores de la misma familia — no reutilizadas bajo ninguna circunstancia (§3.4, `scope_id` distinto las distingue por construcción): semilla anulada `867948c` (`ADR-135(d)`), semilla del `ACTO B` original (`174266824551963846210387427777144587800`, `scope_id="ACT-PIL-3-v1"`), semilla de B′ (`63114853283919194858838455602446543838`, `scope_id="MARCO-M-v1"`).

**El primer resultado que produzca este procedimiento es el que se reporta.**

---

## Resultado (segundo commit — salida íntegra, una sola corrida)

`sortear_marco_m(marco, n_sorteo=11, cuota_max=2, semilla=34354141898495593251517379743390345279)` sobre las 22 filas `elegible_v1_1=='SI'` de `marco-M-congelado-v1_1.tsv` (`N_elegibles` verificado contra `CONGELADO-M-v1_1.sha256`, `sorteo_marco_m_v1_1.py`). Con `len(marco)=22 ≥ 15`, se delega literalmente en `sorteo_v2.sortear` (no la rama identidad).

### Salida cruda

```
semilla = 34354141898495593251517379743390345279
len(marco) = 22   n_sorteo = 11   cuota_max = 2
len(resultado.resultado) = 11
ids sorteados (orden de salida del algoritmo): ['CIV-M-08', 'TRA-M-07', 'CIV-M-11', 'CIV-M-13', 'TRA-M-05', 'CIV-M-09', 'CIV-M-12', 'TRA-M-03', 'CIV-M-06', 'FAM-M-01', 'CIV-M-01']
skips: []
estratos_excluidos: []
exclusiones: []
```

### Las 11 filas sorteadas (orden por `id`, columnas clave)

| # | id | estrato | grado_DD (F-DD, ya congelado) | ola_calibracion | publicada |
|---|----|---------|-------------------------------|------------------|-----------|
| 1 | CIV-M-01 | PENDIENTE | P1 PUNTUA | ENVIPE 2025 (única ola disponible para este universo) | (vacío→NO) |
| 2 | CIV-M-06 | PENDIENTE | P1 PUNTUA | ENVIPE 2025 (única ola disponible para este universo) | (vacío→NO) |
| 3 | CIV-M-08 | PENDIENTE | P1 PUNTUA | ENVIPE 2025 (única ola disponible para este universo) | (vacío→NO) |
| 4 | CIV-M-09 | PENDIENTE | P1 PUNTUA | ENVIPE 2025 (única ola disponible para este universo) | (vacío→NO) |
| 5 | CIV-M-11 | PENDIENTE | P1 PUNTUA | ENVIPE 2025 (única ola disponible para este universo) | (vacío→NO) |
| 6 | CIV-M-12 | PENDIENTE | P1 PUNTUA | ENVIPE 2025 (única ola disponible para este universo) | (vacío→NO) |
| 7 | CIV-M-13 | PENDIENTE | P1 PUNTUA | ENVIPE 2025 (única ola disponible para este universo) | (vacío→NO) |
| 8 | FAM-M-01 | PENDIENTE | P1 PUNTUA | ENIF 2024 (única ola) | (vacío→NO) |
| 9 | TRA-M-03 | PENDIENTE | P1 PUNTUA | ENCIG 2023 | (vacío→NO) |
| 10 | TRA-M-05 | PENDIENTE | P1 PUNTUA | ENCIG 2023 | (vacío→NO) |
| 11 | TRA-M-07 | PENDIENTE | P1 PUNTUA | ENCIG 2023 | (vacío→NO) |

Clasificación F-DD: las 11 son `P1 PUNTUA` — ninguna celda `P0 VERIFICACION-NO-PUNTUA` puede salir sorteada porque el universo elegible (`elegible_v1_1=='SI'`) ya las excluye por construcción (criterio F-DD de `ADR-237`, ver Pre-registro arriba). Ninguna es transferencia circular respecto a su propia calibración.

### Verificación de las reglas duras del reglamento (§2, `sorteo-act-pil-3-v2-PROPUESTA.md`)

- **Regla 1 (tamaño)**: `len(resultado) = 11 == n_sorteo = 11` ✓.
- **Regla 2 (`publicada=SI ≤ cuota_max`)**: `count(publicada=SI) = 0 ≤ cuota_max = 2` ✓ (con margen: los 22 elegibles traen `publicada` vacío→`NO`, cero `SI` en todo el universo elegible).
- **Regla 3 (piso 1 por estrato no vacío) — NO SE CUMPLE, hallazgo no forzado.** Ver sección siguiente.
- **Regla 4 (sin reposición)**: 11 ids únicos, verificado (`len(ids) == len(set(ids))`).
- **Regla 5 (determinismo)**: misma semilla (derivada de `SHA_A` fijo) + mismo `.tsv` (sha256 verificado) ⇒ mismo resultado, por construcción de `random.Random` + orden estable por `id` antes de cualquier permutación — no se corrió una segunda vez para "confirmar" (violaría "el primer resultado que produzca este procedimiento es el que se reporta").

### Hallazgo, no forzado — regla 3 no se cumple, primera vez que el mecanismo la ejercita bajo cuotas fraccionarias ajustadas

El marco elegible tiene 2 estratos no vacíos: `PENDIENTE` (21 filas) y `tramite|P1|MEDIA` (1 fila, `TRA-M-02`). Con `n_sorteo=11`: `asignar_asientos_proporcional` (`sorteo_v2.py:111`, §2.2 del reglamento, **no editado**) computa `cuota_exacta = {"PENDIENTE": 11*21/22 = 10.5, "tramite|P1|MEDIA": 11*1/22 = 0.5}`, `floor = {10, 0}`, `restantes = 1`. Los dos estratos EMPATAN en parte fraccionaria (`0.5` cada uno); el desempate determinista de §2.2 es alfabético por nombre de estrato (`"PENDIENTE" < "tramite|P1|MEDIA"`, `P` < `t` en ASCII), así que el asiento remanente va a `PENDIENTE`: `asientos = {"PENDIENTE": 11, "tramite|P1|MEDIA": 0}`. `TRA-M-02` (el único miembro de `tramite|P1|MEDIA`) queda sin asiento — 0 filas de ese estrato en el resultado, aunque el estrato no está vacío y `n_sorteo=11 ≥ n_estratos_no_vacios=2`.

**Esto contradice la letra de la regla 3** ("Todo estrato con al menos una fila en `marco` recibe al menos una fila en `resultado` si `n_sorteo ≥ n_estratos_no_vacios`" — listada como "regla dura: rechazada si se viola, no relajada"). Pero el **pseudocódigo autoritativo de §2** (el mismo documento, sección "5. Verificación final") solo hace `assert` de las reglas 1 y 2 como postcondición ejecutable — la regla 3 no está codificada como gate de rechazo en `sortear()` ni en su pseudocódigo de referencia; es una propiedad que la prosa de la regla 3 ATRIBUYE al método Hamilton/mayor-resto, pero que el método, matemáticamente, no garantiza en general: con una cuota exacta de `0.5` y un empate de parte fraccionaria, cuál estrato gana el asiento remanente depende del desempate (aquí, alfabético), no de un piso mínimo de 1 aplicado ANTES del reparto proporcional. Confirmado además por el propio código de `asignar_asientos_proporcional`: `asientos = {e: int(q) for e, q in cuota_exacta.items()}` es `floor()` puro (puede dar `0`), sin excepción para estratos no vacíos — coincide exactamente con el pseudocódigo de §2.2 (`asientos[e] = floor(cuota_exacta[e])`), así que el código no diverge de SU PROPIO pseudocódigo: la divergencia es entre la prosa de la regla 3 (que promete un piso 1 que el método no garantiza matemáticamente) y el propio §2.2 que esa misma regla 3 cita como mecanismo. `tests_sorteo_v2.py::TestCaso1Normal.test_asientos_hamilton` (el único test existente de `asignar_asientos_proporcional`) usa 3 estratos con cuotas fraccionarias que no producen ningún piso 0 sobre estrato no vacío (`6.0/3.6/2.4 → 6/4/2`) — este caso límite (cuota exacta de un estrato ≤ 0.5 con empate de fracción) no estaba cubierto por ningún caso de prueba previo, ni por el sorteo original (`ACT-PIL-3`, 3 estratos con más filas) ni por B′ (`ACTO MAESTRA32-E14`, un solo estrato, rama identidad — regla 3 trivialmente satisfecha).

**Este acto NO edita `sorteo_v2.py` ni `sorteo_marco_m.py`** (fuera de perímetro, "cero juicio, receta congelada"; el encargo B″ es explícito: la función de semilla y, por extensión, el resto del mecanismo sellado, "NO se edita") **y NO re-corre el sorteo con un desempate distinto** — eso sería exactamente el defecto que la disciplina de pre-registro de este mismo documento existe para impedir ("el primer resultado que produzca este procedimiento es el que se reporta", declarado arriba antes de conocer el resultado). El resultado de 11 celdas queda sellado tal cual salió. Dirección decide qué hacer con la tensión entre la regla 3 (prosa) y el §2.2 (mecanismo) — posibles vías, ninguna ejecutada aquí: (a) precisar la prosa de la regla 3 en `sorteo-act-pil-3-v2-PROPUESTA.md` para que describa lo que Hamilton/mayor-resto realmente garantiza (no un piso 1 incondicional); (b) añadir un piso-1 explícito a `asignar_asientos_proporcional` para los sorteos futuros (cambiaría el algoritmo sellado por `ADR-178`, palabra mayor); (c) aceptar que `TRA-M-02` y su estrato queden fuera de esta ronda y confiar en que un sorteo futuro (marco v1.2 o más adelante) los alcance. Consecuencia práctica declarada: `TRA-M-02` (que YA tiene un punto M emitido, `corridas-M/M-TRA-M-01.json`/`M-TRA-M-02.json`, de una emisión anterior sin herramienta formal — ver `A.8` del encargo `MAESTRA33-E6`) simplemente no vuelve a salir sorteado en esta ronda; no hay ninguna otra consecuencia sobre datos ya existentes.

### Intocables verificados

`git diff --stat` contra `sorteo_v2.py`, `sorteo_marco_m.py`, `tests_sorteo_v2.py`, `tests_sorteo_marco_m.py`, `marco-M-congelado-v1_1.tsv`, `CONGELADO-M-v1_1.sha256`, todo el duelo original (`marco-congelado-piloto-v1_0.tsv`, `marco-M-congelado-v1_0.tsv`, `marco-M-sorteado-v1_0.tsv`, `sorteo-resultados-v1_0.md`, `sorteo-marco-M-resultados-v1_0.md`, `corridas-*`, `scoring-adv1-m3.py`) y `milpa/**`: vacío (verificado antes de cerrar este acto).

### Contador

Celdas del marco-M sorteadas en v1.1: `0 → 11`. El sorteo v1.0 (2 celdas, identidad, ya emitidas) y este sorteo v1.1 (11 celdas nuevas) son conjuntos disjuntos salvo por la ausencia declarada de `TRA-M-02` en este segundo (ver hallazgo arriba) — `TRA-M-02` solo aparece en v1.0.

### Lo que este acto NO hace

No emite puntos M (eso es `EMISOR-M-1`/`tools/emite_m.py`, sucesor declarado, gated a este sorteo), no abre `corridas-R/` (CIEGO, mismo criterio que `.claude/commands/arbitra.md`), no calcula R ni L, no decide grado_dependencia, no edita `sorteo_v2.py`/`sorteo_marco_m.py`, no re-sortea.

