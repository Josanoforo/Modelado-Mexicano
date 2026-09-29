# Expediente de apertura · ENPECYT 2017 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), escrito en NUBE sobre `7393b17e`, sin corpus
montado. Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que mesa
autorice, o mesa por escrito.

## 0 · Premisas

- [LEÍDO] Contendiente sellado (regla 6: ningún contendiente nuevo): `CALC-ENPECYT-CONOC-PISOS-0001`,
  `spec.yaml:23` «olas: 2011, 2013, 2015 abiertas; 2017 RESERVADA (E.6), no es input»; spec humana
  `forense/prereg-caja/ENPECYT-CONOC-PISOS-spec-v1_0.md` §0–§4: 10 conductas de personas 18+ urbanas, piso 2015
  con **IC calibrado de persistencia** (τ² sobre 2011→2013→2015) para 9; RESPETA-10-INVENTOR sólo 2015 (sin ICC).
- [EJECUTADO] Manifiesto por id (A.15; `yaml.CSafeLoader`, 7 198 entradas; filtro `enpecyt` en id o `archivo`):
  la ola 2017 tiene **un** payload de microdato, `enpecyt2017_bd_dbf_zip` (`ENPECYT/2017/enpecyt2017_bd_dbf.zip`,
  «no abierto (sólo sha, tamaño y directorio central)»), y su FD `enpecyt2017_fd_pdf` (documentación, no payload).
- [EJECUTADO] Reserva: `enpecyt2017_bd_dbf_zip` no lleva `estado_reserva` en el manifiesto y `tools/corpus_loader.py`
  no lo reserva; **la reserva la declara la spec sellada del contendiente** (hallazgo; la receta §4a no tiene
  custodia que levantar).
- [EJECUTADO] Ninguna corrida lee la ola: `grep` de los 390 `data/corrida0/*/spec.yaml` por
  `enpecyt2017_bd_dbf_zip` → 0 archivos.
- [REPORTADO] Cifras 2017 ya publicadas: la spec del contendiente §5 nombra «las cifras 2017 que citan los
  reports (75.0 %, 92.2/92.3 %, 59.5/41.5/34.6/48.4 %, ~72 %)» como marginales nacionales. No se leyeron aquí
  (E.6: tabulados y comunicados de una ola reservada no se leen). Decisión fijada antes de abrir: **la celda
  TOTAL de cada conducta se aparta de la comparación primaria** (su R se reporta, no se puntúa; E.6 «lo que se
  aparta sin abrir se declara y por qué»). Riesgo residual declarado: si alguna de esas cifras fuera por sexo,
  edad o escolaridad, esa celda sería RETROSPECTIVA; el acto de apertura lo declara en su nota sin cambiar la
  primaria.
- [LEÍDO→rama prevista] La spec del contendiente §0 dice que los reactivos de 2017 se revisaron «por cuestionario
  y FD, sin abrir datos», pero no fija campos 2017. Los campos y códigos se fijan **sobre la ola del piso 2015**
  (`ITEMS["2015"]`, ciudad `CD_A`), rotulado así; la diferencia se declara al abrir (§5).

## 1 · Estimandos

Por cada una de las 10 conductas y cada categoría de cada eje (TOTAL; SEXO 2; EDAD 4; ESCOLARIDAD 3 = 10
celdas por conducta, **100 celdas**): **R = Σw·y / Σw** en ENPECYT 2017, con la recodificación del contendiente
(medidor sellado importado por bytes, sha256 fijado en `APERTURA-ENPECYT-2017-spec.yaml`). Campos y códigos
(2015): INTERES `S4P1_3` (CB1; AL-MENOS-MODERADO = 1–3 de 1–4; GRANDE-O-MAS = 1–2 de 1–4); GOB-INVERTIR `S4P25_1`
y FE-CIENCIA `S4P31_1_1` (CB2; -ACUERDO = 1–2 de 1–5, «no sabe» 5 en el denominador; -SIN-NS = 1–2 de 1–4);
RESPETA-10-BOMBERO `S4P14_12`, -ENFERMERA `S4P14_13`, -INVESTIGADOR `S4P14_16`, -INVENTOR `S4P14_17` (CB1; = 10
de 1–10). Ejes (CS): `SEX` 1 HOMBRE / 2 MUJER; `EDA` 18-29, 30-44, 45-59, 60-MAS; `NIV` BASICA-O-MENOS 0–3,
MEDIA 4–6, SUPERIOR 7–10.

## 2 · Universo, unidad, ponderador, diseño

Unidad **persona** elegida de 18+ (una fila de CB1), áreas urbanas de 100 000+ habitantes. Tablas del ZIP:
miembros `enpecyt2017_cb1.dbf`, `enpecyt2017_cb2.dbf`, `enpecyt2017_cs.dbf` (patrón `enpecyt<ola>_<tabla>.dbf`
del contendiente, sin distinguir mayúsculas). Unión CB1–CB2–CS por `CD_A+PER+CON+V_SEL+N_HOG+N_REN`, sólo llaves
únicas. Válido: `FAC` (CB1) > 0, `EST_DIS` y `UPM_DIS` (CS) no vacíos (`prepara(tablas, "2015")` del contendiente).
Payload: `enpecyt2017_bd_dbf_zip`. R es un punto; no se calcula IC de R.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce
levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo:
`groupby`/`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera de
`lee_payload_reservado` → PARO. `lee_payload_reservado` PARA si el ZIP no es `enpecyt2017*` o si falta un
miembro. Probado por mutación y con sintético del esquema del contendiente: `tests/test_apertura_enpecyt_2017.py`
(con soporte, conducta sin soporte, categoría vacía, DBF en ZIP con campo ausente, PARO por `FAC` ausente y por
ola equivocada; cada mutación de `expediente_apertura.MUTACIONES` detectada) y `tests/test_prereg_aperturas.py`.

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del contendiente y R finitos, **y** celda fuera de TOTAL (§0) **y** conducta con ICC.
lo/hi = **IC calibrado de persistencia del piso 2015** (`RESULT-ENPECYT-CONOC-PISOS-<c>-<eje>-<cat>-ICC-LO/-ICC-HI`);
punto = `RESULT-ENPECYT-CONOC-PISOS-<c>-2015-<eje>-<cat>-P`. Candidatas a puntuar: 9 conductas × 9 celdas fuera
de TOTAL = 81. **Primaria** (una sola): cobertura k/n = #celdas con lo ≤ R ≤ hi, IC de Wilson al 95 %. Dictamen:
**CALIBRADO** si 0.95 ∈ Wilson; **SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95;
**NO-ESTIMABLE** si n = 0. Orden: NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO (excluyentes). Secundarias,
descriptivas, no adjudican: cobertura por conglomerado (conducta), recalculable de R y lo/hi, y error absoluto
medio punto-2015 vs R (`-MAE-PUNTO`, sólo sobre las celdas puntuadas).
B-bis: CALIBRADO = piso **corroborado en alcance** para 2017; SOBRECUBRE = piso **acotado** (IC conservador);
SUBCUBRE = el piso con IC de persistencia no anticipa 2017. Una apertura sirve a todos los sellados antes: el
único contendiente sellado es `CALC-ENPECYT-CONOC-PISOS-0001`.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- Numeración de reactivos: 2015 renumeró respecto de 2011/13 (S4P26_1 → S4P25_1, S4P33_2_1 → S4P31_1_1,
  profesiones S4P14_*). Si 2017 renumeró otra vez, un campo 2015 puede existir con otra pregunta: el preflight
  documental (FD 2017 + cuestionario) decide por texto; un campo con otro texto → esa conducta NO-ESTIMABLE en
  la nota de apertura.
- Redacción del interés: 2015 y 2017 comparten «Nuevos inventos, descubrimientos científicos y desarrollo
  tecnológico» (spec del contendiente §0) → mismo reactivo que el piso.
- Ciudad `CD_A`, estrato `CD_A|EST_DIS`, UPM `CD_A|EST_DIS|UPM_DIS`: si 2017 cambia el nombre de la ciudad, es PARO.

Regla fijada, mecánica: campo de reactivo o de eje ausente del DBF → entra vacío → las celdas que lo usan salen
NO-ESTIMABLE; campo de ciudad, llave, `FAC`, `EST_DIS` o `UPM_DIS` ausente, o miembro ausente → **PARO**. Si en
caja, antes de correr, el FD/cuestionario de 2017 no trae un campo del contendiente con el mismo texto de
pregunta y códigos, esa conducta se declara NO-ESTIMABLE en la nota de apertura (no se recodifica ad hoc). Leer
el FD y el cuestionario no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-ENPECYT-2017-<conducta>-<eje>-<cat>-R` (100), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`,
`-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA). None sólo en R de celdas NO-ESTIMABLE y en Wilson/MAE cuando n = 0.
Contrato: `APERTURA-ENPECYT-2017-spec.yaml` (calc_id `CALC-APERTURA-ENPECYT-2017-0001`; payload con sha del
manifiesto; medidor sellado del contendiente, su `resultados.json`, la guardia y el expediente común como inputs
`origen: repo` con sha). La apertura es copiarlo a `data/corrida0/CALC-APERTURA-ENPECYT-2017-0001/spec.yaml` y
correr (receta).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA: el contendiente se selló (en main desde `bf5fc5e7`, 27/sep) antes de que exista cualquier R de
  2017 medida en el repo; las celdas TOTAL, cuyo marginal nacional ya publicó INEGI, se apartan de la primaria
  (§0). Ninguna frase mezcla esta cobertura con marcadores RETROSPECTIVOS.
- Unidad: **persona** 18+ en R y en el piso; nada se promedia con hogar, delito o trámite.
- Escala: proporción 0..1; se compara «R dentro del ICC del piso» (cobertura), no punto contra punto.
- Segmentación: sexo, edad, escolaridad, uno a la vez. **Universo urbano ≥ 100 000**: nada dice del México rural
  ni de localidades pequeñas; el sesgo de clase media urbana está en el universo mismo y no se corrige.
- Actitud declarada ≠ conducta; «respeto» a profesiones es una calificación, no una práctica.
- Qué sería peligroso leído simplista: un SUBCUBRE no dice «el mexicano perdió interés en la ciencia»: dice que
  el piso 2015 con su IC de persistencia no anticipa 2017 en esa proporción de celdas.
- Cifras escritas a mano: ninguna; constantes = hashes fijados y umbrales (0.95, z = 1.959964), antes de abrir.
