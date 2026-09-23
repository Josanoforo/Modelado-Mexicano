# Nota de ejecución · ACTO GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2 · 22/sep/2026

Encargo: `forense/encargos/2026-09-22-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2.md`
(sellado, cuerpo 0-bis ya commiteado). Esta nota cubre P1-P4 con lo
efectivamente corrido en esta sesión; lo que no se corrió va marcado con su
categoría A.14 y se lista aparte para el cierre.

## P1 · Consumo de adjudicaciones

### GOB (CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001) — CORRIDO, real

`[LEÍDO]` `data/curacion-registro/celdas-d/GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml`:
`champion_actual: C2` desde el COMMIT-3 (704d5289, firma F3, 21/sep/2026).
`[EJECUTADO]` `filas_cruce_adoptadas()` YA lee cualquier celda-D con
`champion_actual: C2` sin distinguir dominio: la celda GOB ya calzaba en el
mecanismo existente y sólo faltaba re-derivar. `python3
tools/marcador_segmento.py --escribe` (antes de tocar código) hizo pasar
`adoptadas_c2` de 20 (el TSV commiteado, obsoleto) a 36 — las 16 sub-celdas
`CRUCE::GOB.…::<edad>x<escolaridad>` entraron como `PISO-ADMISIBLE-NO-ADOPTADO`
(no hay fila `adopcion:piso-C2-20-celdas` que las cubra por nombre, `tiene_adopcion`
sigue leyendo sólo esa firma — se declara, no se corrige: está fuera de §7(c)
de este encargo, que sólo autoriza adoptar por F2).

Pero el PAR agrupado `CRUCE-GRUPO::tramite.gobierno_digital.util_sin_coercion_ejes_encig2025::edadxescolaridad`
seguía `RESERVADA` — ese es exactamente el defecto que
`NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-3619-01` describe. Causa
real, `[LEÍDO]` en `filas_cruce_reservadas()`: `pares_piloteados` sólo
reconocía celdas-D con id `DIN.` o `TRA.`, nunca `GOB.` — un `elif` que
faltaba, no una adjudicación pendiente. Se agregó la tercera rama
(`tools/marcador_segmento.py`, ~15 líneas) y se re-derivó: 22→21 grupos
`RESERVADA`, 206→190 `EMITIDA-SIN-EVALUAR` (las 16 emisiones del par ya no
se cuentan aparte de sus 16 sub-celdas adoptadas). **Esto cierra NC 3619-01**
(fila actualizada en `forense/no-corrido.tsv`, `estado=CERRADA`).

### DUELO-ENVIPE2026 y DIN-LOTE-ENIF2024 — NO CORRIDO

`[LEÍDO]` `data/corrida0/CALC-DUELO-ENVIPE2026-ADJUDICACION-0001/` y
`data/corrida0/CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001/`: ninguna celda-D
en `data/curacion-registro/celdas-d/*.yaml` referencia estos dos CALC (`grep
-rl` sobre los tres CALC id sólo encontró la celda-D de GOB). El marcador no
tiene, hoy, ningún camino que no sea celda-D + `champion_actual` para
convertir un CALC de adjudicación en filas de `marcador-segmento.tsv`; estos
dos son adjudicaciones "sueltas" (DUELO: 42 `VS-PERSISTENCIA` en tres
bloques T3/T5/TC de 14 cada uno, no 24 como dice el §1 del encargo — la
cuenta de "24 cruces" no calza con lo que el CALC sella y no se pudo
reconciliar sin arriesgar inventar el mapeo; LOTE: 14 pares con métricas de
cobertura de IC, no un veredicto por celda directamente comparable al
esquema `adjudicacion_por_celda` que el resto del tool consume).

Construir el lector nuevo (sin celda-D, leyendo `resultados.json` +
`ejecucion.json` directo, con su propia regla de PROSPECTIVA/RETROSPECTIVA
por comparación de sellos) es un diseño nuevo, no una extensión de 15
líneas como el de GOB, y la discrepancia 42-vs-24 es exactamente el tipo de
premisa que v2.16 §2 manda no ajustar en silencio. **PARO-PREMISA**: el
`[SUPUESTO]` del §3 del encargo ("el lote ENIF 2024 derivó R para sus 14
cruces en COMMIT-3... esas filas son EVALUADA") no cae dentro de PAROS (a-f)
tal como está escrito, pero tocar el universo de cruces sin la aclaración de
cuántos son "los 24" del duelo sí toca qué se mide — no se adivinó.

No se escribió el test "un CALC de fixture por fuente" que P1 pide, porque
sólo se implementó consumo real para una de las tres fuentes (GOB, que ya
tenía cobertura de test — `tests/test_c2_compuesto.py`,
`tests/test_marcador_segmento.py::t_veinte_adoptadas` — actualizada a 36).

## P2 · ENIF con reserva de ancho — CORRIDO, real, 32/32

`[LEÍDO]` `forense/firmas-pendientes.tsv:452`
(`FP-260922-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1-2868-01`, FIRMADA
22/sep/2026, ACTO GEN2-TRAMITE-FIRMAS-7) — tres opciones declaradas,
`ADOPTAR-CON-RESERVA-DE-ANCHO` es la que el §1/§5 de este encargo da por
resuelta (se tomó como premisa LEÍDA, no se re-abrió la decisión de mesa).

Implementado en `tools/marcador_segmento.py`:
- `ADOPCION_MARGINAL_POR_INSTRUMENTO["ENIF 2024"]` pasa de `DIFERIDA` a
  `ADOPTADO-CON-RESERVA-DE-ANCHO` (constante `ESTADO_ENIF_RESERVA_ANCHO`).
- `_ic_calibrado_enif()`: lee `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001/resultados.json`
  (1125 RESULT sellados) y arma `{resultado_id del piso: (inf, sup)}` por
  identidad de sufijo de celda contra los DOS prefijos de piso que
  alimentan el eje ENIF (`RESULT-PISOS-ENIF2021-V2-…` de `CALC-PISOS-ENIF2021-EJES-0003`,
  y `RESULT-PISOS-ENIF2021-FORMALIDAD-…` de `CALC-PISOS-ENIF2021-FORMALIDAD-0001`
  para el eje `formalidad`, que usa un CALC distinto — `[EJECUTADO]`: sin
  el segundo prefijo, 4/32 celdas (las de `formalidad`) se quedaban sin IC
  calibrado; se corrigió y verificó 32/32).
- `_aplica_adopcion_marginales_por_instrumento()` sustituye, sólo para estas
  filas, `piso_ic95` por el IC calibrado y `tipo_incertidumbre` por
  `"calibrado: un solo choque 2018→2021, conservador"` (string exacto que
  pide el §1 del encargo), y `decision_ref` por
  `FP-260922-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1-2868-01`.
- `escribe_estimadores_yaml()`: la rama que escribe punto+IC en
  `marginales` ahora cubre `ADOPTADO-POR-FIRMA` **y**
  `ADOPTADO-CON-RESERVA-DE-ANCHO`.

Verificado (`python3 -c` sobre el yaml escrito): 32/32 celdas ENIF con
`champion: PERSISTENCIA(t-1)`, `punto` = el piso t-1 (de
`CALC-PISOS-ENIF2021-EJES-0003`/`-FORMALIDAD-0001`, sucesores sellados del
`CALC-PISOS-ENIF2021-EJES-0001` vetado — el `punto de CALC-PISOS-ENIF2021-EJES-0001`
del §5 del encargo es la lineage, no el CALC vetado literal), `ic95_inf` con
el IC calibrado, `tipo_incertidumbre` exacto, `decision_ref` la fila F2.
`estimadores-por-segmento.yaml`: "47 adoptadas / 10 vetadas-o-diferidas"
(15 ENVIPE + 32 ENIF adoptadas; 10 ENCIG vetadas-en-nivel).

## P3 · ENUT (`reparto_hogar` / `sexo_edad`) — NO CORRIDO

`[LEÍDO]` `canon/L0/ADR-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-01.md`: el
acto predecesor (`GEN2-ENUT-NUCLEO-CELDAS-1`) PARÓ en el ARRANQUE
(PARO-PREMISA) sin escribir nada, y su sucesor declarado es
`GEN2-ENUT-ENLACE-MARCADOR-1` — que es, en sustancia, este P3. Ese ADR trae
la firma (a)(b′)(c) ya FIRMADA sobre
`FP-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-01` con la enmienda "21→12 filas":
(a) C2×2019 = CAMBIO-DE-INSTRUMENTO en tabla nueva `v1_1`; (b′) 10
`sexo_edad` → `NO-CONSTRUIBLE-POR-CRUCE`; (c) `cuenta_gen2=SI`; y cita el
enlace sin medir "0.2379 → 0.2255, ambas selladas".

`[LEÍDO]` `forense/prereg-caja/PISOS-ENUT2019-ejes-metadatos-v1_1.tsv`: YA
existe (creada por el acto que PARÓ) y YA está en
`tools/marcador_segmento.py::TABLAS_IDENTIDAD` (línea 108, sucede a la
`v1_0`), pero su contenido hoy es idéntico en sustancia a la `v1_0`/al
`SIN-PISO-POR-DISEÑO` ya vigente — no trae todavía el enlace a
`CALC-ENUT2019-NUCLEO-EJES-0001` ni el rótulo `NO-CONSTRUIBLE-POR-CRUCE`
que (b′) manda. Escribir esas filas exige entender con precisión el
contrato `cell_id`/`resultado_id` que `_piso_de_fila()` espera (cómo se
arma el id contra `CALC-ENUT2019-NUCLEO-EJES-0001`/`CALC-ENUT2024-NUCLEO-EJES-0001`,
qué corresponde a "razón de núcleo nacional" en esos `resultados.json`) y
verificar que 0.2379/0.2255 efectivamente salen de ahí — no se alcanzó a
hacer esa verificación con la certeza que este proyecto exige (§2: ninguna
cifra se teclea) en el tiempo de esta sesión.

**NO-VERIFICABLE-AQUÍ** (no PARO-PREMISA: la firma SÍ existe y SÍ basta —
es una cuestión de tiempo de esta sesión, no de premisa caída). El
`data/curacion-registro/celdas-d/` sigue sin tocar (perímetro respetado);
`forense/prereg-caja/PISOS-ENUT2019-ejes-metadatos-v1_1.tsv` tampoco se
tocó (fuera de la lista PROPIO del §9 del encargo, y de tocarla sin la
verificación de arriba se habría arriesgado teclear 0.2379/0.2255 sin
confirmarlas contra el CALC — exactamente lo que §2 prohíbe).

## P4 · Cierres

- **NC `…PILOTO-3-COMMIT-2-3-v1_3-3619-01`: CERRADA** (`forense/no-corrido.tsv`,
  fila actualizada con el commit y el comando que la resuelve). Ver P1/GOB
  arriba.
- **Lista real de `RESERVADA` tras este acto** (21 grupos, para
  `GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1`):

  ```
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::cuenta_formalxedad
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::cuenta_formalxescolaridad
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::cuenta_formalxformalidad
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::cuenta_formalxlocalidad
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::cuenta_formalxsexo
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::edadxescolaridad
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::edadxformalidad
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::edadxsexo
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::escolaridadxformalidad
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::escolaridadxlocalidad
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::escolaridadxsexo
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::formalidadxlocalidad
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::formalidadxsexo
  CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::localidadxsexo
  CRUCE-GRUPO::tramite.gobierno_digital.util_sin_coercion_ejes_encig2025::edadxsexo
  CRUCE-GRUPO::tramite.gobierno_digital.util_sin_coercion_ejes_encig2025::escolaridadxsexo
  CRUCE-GRUPO::tramite.evasion_norma_ejes_envipe2025::dominio_urbano_ruralxsexo
  CRUCE-GRUPO::tramite.evasion_norma_ejes_envipe2025::edadxescolaridad_proxy
  CRUCE-GRUPO::tramite.evasion_norma_ejes_envipe2025::edadxsexo
  CRUCE-GRUPO::tramite.evasion_norma_ejes_envipe2025::escolaridad_proxyxsexo
  CRUCE-GRUPO::familia.cuidado.reparto_mujeres40_ejes_enut2024::reparto_hogarxsexo_edad
  ```

  (`n_celdas_reservadas` = 160, de `python3 tools/marcador_segmento.py --json`.)

## Verificación corrida

- `python3 tools/marcador_segmento.py --escribe` → `229 filas`; `36 celdas
  adoptadas + 190 EMITIDA-SIN-EVALUAR + 57 marginales (47 adoptadas / 10
  vetadas-o-diferidas)`.
- `python3 tests/test_marcador_segmento.py` → `PASA -- 13 casos` (incluye
  T-RESERVA, T-EMISOR-NO-COMPARA/T-EMISOR, T-PISO-NO-CIRCULAR/T-PISO, y
  T-MARGINALES-ADOPCION actualizada a 47/10 con la firma F2).
- `python3 tests/test_c2_compuesto.py` → `OK`, 30 tests (tres conteos
  hardcoded actualizados: 22→21 pares reservados, 16→15 emitibles, 20→36
  adoptadas — todos consecuencia directa y verificada del fix de P1/GOB,
  ninguno tecleado a mano sin correr el derivador primero).
- `python3 tests/test_marcador_metrica_y_prospectividad.py`,
  `tests/test_derivados_protegidos.py`, `tests/test_pisos_enut2019.py`,
  `tests/test_tablero_programa.py`, `tests/gonogo_marcador.py` → sin
  regresión (comparados contra el estado previo a los cambios).
  `tests/test_arbitro_marginales.py`,
  `tests/test_c2_ic_enif2024_guardia.py`,
  `tests/test_c2_restringido_enif2024_guardia.py` no corrieron aquí
  (`ModuleNotFoundError: numpy` — entorno de esta sesión, no relacionado
  con este acto; NO-VERIFICABLE-AQUÍ).
- `python3 tests/check.py` (suite completa): lanzada; ver resultado en el
  commit de cierre — corre ~3-4 min y esta nota se escribió mientras
  terminaba.

## Decisión dentro de latitud (§6 del encargo)

No se encontró ningún cruce con R derivado en un CALC que NO sea de
adjudicación (la pregunta del §6 no se disparó en el universo tocado esta
sesión: GOB y ENIF pasan por celda-D/`ADOPCION_MARGINAL_POR_INSTRUMENTO`,
no por un descriptivo suelto). Se deja constancia de que, si aparece al
completar DUELO/LOTE, la recomendación del encargo (`CONSUMIDA-SIN-PILOTO`)
es la que aplica.

## Premisas verificadas

- `[EJECUTADO]` §3 "16 `EMITIDA-SIN-R`": no existe ese estado literal en el
  código (`grep` sin resultado); la cifra citada en el encargo se leía de
  otra columna/versión del TSV. No cambia nada de lo pedido: se declara.
- `[EJECUTADO]` §3 "el lote ENIF 2024 derivó R para sus 14 cruces... y el
  piloto 3 para edadxescolaridad ENCIG: esas filas son EVALUADA" — la parte
  de ENCIG (piloto 3 / GOB) SE CONFIRMÓ correcta una vez re-derivado; la
  parte del lote ENIF (DIN-LOTE) NO se pudo confirmar sin diseñar el lector
  nuevo (ver P1 arriba) — premisa parcialmente sostenida.
- `[LEÍDO]` §5 P2 "punto de `CALC-PISOS-ENIF2021-EJES-0001`": ese CALC está
  VETADO (`CALC_PISOS_VETADOS`); el punto que efectivamente se usa viene de
  sus sucesores sellados (`CALC-PISOS-ENIF2021-EJES-0003`/
  `-FORMALIDAD-0001`), que es la lectura correcta de la lineage del veto
  ("hasta que GEN2-PISOS-REJILLA-CLI-1 entregue sucesores"). No se
  interpretó como discrepancia que requiera PARO.
