# Expediente de apertura · ENSU 2026 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que
mesa autorice, o mesa por escrito.

## 0 · Premisas

- [EJECUTADO] Ids de la ola en `data/manifiesto.yaml` (lector YAML, filtro por id): `cc1_inegi_ensu_2026__ensu_bd_2026_csv`
  (base de datos, «Marzo, junio», ZIP de 2 miembros, `estado_reserva: RESERVADA-NO-ABIERTA-NO-INDEXAR-L`, raíz
  `reserva_respondentes`) y `cc1_inegi_ensu_2026__ensu_fd_2026_pdf` (descripción de archivos: documentación, **no** input).
- [LEÍDO] Contendientes sellados (regla 6: ninguno nuevo): `CALC-ENSU-PISOS-0001` (pisos 2024T1, 2025T3, 2025T4 con IC
  de diseño, 15 conductas × {TOTAL, SEXO, EDAD, ENT, CIUDAD}) y `CALC-ENSU-SERIE-0001` (serie 2013T3–2025T4, τ² de
  persistencia por eje y cadencia, dictamen DONDE-CAMBIO). Los dos declaran en `spec.yaml:etiquetas.olas` «2013T3-2025T4
  abiertas; 2026 RESERVADA (E.6, F-ASTRA-5-3), no es input». Spec humana común: `forense/prereg-caja/ENSU-SERIE-spec-v1_0.md`;
  lista cerrada: `forense/analisis/seguridad-ensu/lista-cerrada-P1.md`.
- [EJECUTADO] Los dos CALC depositan el mismo `medidor.py` (sha256 `18026ad1…`, idéntico en ambos) y los mismos inputs de
  código (`pisos_diseno.py` `b82a4fef…`, `dictamen.py` `b2b846ca…`). Control cruzado sellado (spec SERIE §8.2): las 201
  celdas 2025T4 comunes PISOS/SERIE (804 cantidades P/IC-LO/IC-HI/N) son idénticas (0 discordantes).
- [LEÍDO] FP-260928-GEN2-ASTRA-CONTINUIDAD-C2-1-ba6c-01 (FIRMADA, opción b1): «ENSU dic/2025 queda ABIERTA-COMO-VISTA, nunca
  R». Aquí 2025T4 es el contendiente, nunca R: consistente.
- [EJECUTADO] Ningún CALC sellado lee un id de ENSU 2026 (`grep -l 'ensu_2026\|ensu2026'` sobre los 390 `data/corrida0/*/spec.yaml` → 0);
  ninguna cifra de ENSU 2026 citada en `forense/`, `canon/`, `docs/` (rg con patrones «ENSU…2026», «2026T[12]…ENSU»,
  «marzo/junio de 2026»: las coincidencias son otras fuentes o rótulos de reserva). Todas las celdas son PROSPECTIVAS.
- [SUPUESTO→rama prevista] El FD 2026 está en el manifiesto, pero este acto corre en NUBE sin corpus montado: los códigos se
  fijan **sobre la lista cerrada de la ola del piso** (era 2021T2+: tabla CB con `SEXO`/`EDAD`), rotulado así; la diferencia
  se declara al abrir (§5). Nombres de miembro `ensu_cb_MMAA.csv` (patrón del medidor sellado) sin verificar para 2026.

## 1 · Estimandos

**Qué trimestre es R (decisión declarada).** El piso de un marginal es «la ola anterior por eje» (v2.16 §4). El último
trimestre abierto es 2025T4 y es el único piso sellado inmediatamente anterior a la ola reservada. Por cadencia:
- C01–C14 (trimestrales): R = **2026T1** (marzo); par 2025T4 → 2026T1.
- C15-CORRUPCION-POLICIA (semestral, T2/T4; lista §3): R = **2026T2** (junio); par 2025T4 → 2026T2.
- Se aparta sin abrir: C01–C14 en 2026T2 (su ola anterior, 2026T1, no es un piso sellado: «nadie ocupó la fila»). De la
  tabla CB 2026T2 sólo se conservan diseño y las columnas de C15 (`BP3_5`, `BP3_6`); nada más se agrega.

Por cada celda del contendiente (conducta × eje × categoría con P sellado en 2025T4 en PISOS; 2025 celdas): **R = Σw·y / Σw**
en su trimestre R, con el marco (`marco()`) y la recodificación (`y_de()`, CONDUCTAS, FILTRO) del medidor sellado,
importado por bytes con sha256 fijado en `APERTURA-ENSU-2026-spec.yaml`. Códigos: lista cerrada §3 (p. ej. C01 `BP1_1` = 2
«inseguro» sobre {1, 2, 9}; C15 `BP3_6` = 1 sobre {1, 2, 9} entre `BP3_5` = 1).

## 2 · Universo, unidad, ponderador, diseño

Unidad persona seleccionada de 18+ (tabla CB, una por vivienda). Ponderador `FAC_SEL`; válido: `FAC_SEL` > 0, `EST_DIS` y
`UPM_DIS` no vacíos. Ejes del marco: SEXO (`SEXO` 1/2), EDAD (18-29, 30-44, 45-59, 60+ de `EDAD`), ENT (dos primeros dígitos
de `UPM` a 7), CIUDAD (`CD` a dos dígitos, 01–96). Categorías de 2026 que el contendiente no tiene (p. ej. una ciudad nueva)
no se emiten. Payload: `cc1_inegi_ensu_2026__ensu_bd_2026_csv`. R es un punto; no se calcula IC de R.

**IC del contendiente por celda** (regla sellada de SERIE §6, «piso t−1 cubre a t»; `tools/series/dictamen.py::dictamina`
y `pisos_diseno.py::ic_calibrado`, misma fórmula): con p, lo, hi de 2025T4 en (0,1),
ee = (logit hi − logit lo) / (2·1.959964); lo′, hi′ = expit(logit p ∓ 1.959964·√(ee² + τ²)). τ² = `RESULT-ENSU-DICTAMEN-TAU2-
<TRIMESTRAL|SEMESTRAL>-<EJE>` de SERIE según la cadencia de la conducta; eje sin τ² propio (ENT en las dos cadencias; CIUDAD
en la semestral) → `tau2_para`: media de los τ² de su cadencia (regla sellada). p, lo o hi fuera de (0,1) o nulo → sin IC
(celda no puntuada). 1 899 de 2 025 celdas tienen IC [EJECUTADO].

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce levanta
`ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo (`groupby`/`value_counts` con
dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o lectura fuera de `lee_payload_reservado` → PARO). Única lectura:
`lee_payload_reservado` (ZIP → `tablas()` → `marco()` del sellado). Tabla CB ausente para 2026T1 o 2026T2 → PARO; columna de
diseño ausente → PARO (del `marco()` sellado). Antes de leer, el control cruzado PISOS/SERIE se re-verifica (Δ ≠ 0 → PARO).
Probado sobre sintético con el esquema CB: `tests/test_apertura_ensu_2026.py` (con soporte, conducta sin columna, categoría
vacía, CB ausente, auditoría y las 9 mutaciones de `expediente_apertura.MUTACIONES`) y `tests/test_prereg_aperturas.py`.

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi y R finitos. **Primaria** (una sola): cobertura k/n = #celdas con lo ≤ R ≤ hi, con IC de Wilson al
95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson; **SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si
Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Si dos filas pudieran satisfacerse a la vez, manda NO-ESTIMABLE > SUBCUBRE >
SOBRECUBRE > CALIBRADO (excluyentes por construcción). Secundarias, descriptivas, no adjudican: cobertura por conglomerado
(conducta: sus celdas comparten muestra) y error absoluto medio punto-del-piso vs R.
B-bis: CALIBRADO = el piso 2025T4 con su IC de persistencia queda **corroborado en alcance** para el trimestre siguiente;
SOBRECUBRE = piso **acotado** (τ² conservador: incluye los pares juzgados, spec SERIE §6); SUBCUBRE = el piso no anticipa el
trimestre (cambio de percepción o de universo de ciudades que τ² no absorbe). Falsador débil declarado: con ~100 ciudades
de n ≈ 250 el CIUDAD domina n; la cobertura por conglomerado se lee junto.
Una apertura sirve a todos los sellados antes: PISOS (punto e IC de diseño) y SERIE (τ² y regla) se sirven juntos en esta
única comparación primaria; lo imaginable que se aparta sin abrir: la cobertura con el IC de diseño sin τ² (no es intervalo
de predicción; subcubre aun sin cambio) y el dictamen DONDE-CAMBIO extendido a 2026 (exige re-correr la serie: CALC nuevo).

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- 2025T4 y 2026 son de la misma era (2021T2+): CB con `SEXO`/`EDAD`, sin unión CS.
- El catálogo de ciudades de 2026 puede diferir del de 2025T4 (R3 de SERIE): TOTAL/SEXO/EDAD de ENSU son la suma de las
  ciudades del trimestre, no un universo fijo; se declara `CIUDADES` del marco en la nota de apertura.

Regla fijada: si en caja, antes de correr, el FD 2026 no trae una columna del contendiente con el mismo texto de pregunta y
códigos, **esa conducta sale NO-ESTIMABLE** (columna ausente → R None; no se recodifica ad hoc) y se declara en la nota.
Si trae la columna con códigos distintos, el acto de apertura PARA antes de correr y se emite una v1_1 de este expediente
(el código congelado no distingue códigos). Leer el FD no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-ENSU-2026-<conducta>-<eje>-<cat>-R` (2 025), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`, `-MAE-PUNTO`,
`-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE, Wilson y MAE cuando n = 0.
Contrato: `APERTURA-ENSU-2026-spec.yaml` (calc_id `CALC-APERTURA-ENSU-2026-0001`; payload con sha del manifiesto; medidor
sellado, los dos `resultados.json`, receta, `dictamen.py`, guardia y plantilla como inputs `origen: repo` con sha). La
apertura es copiarlo a `data/corrida0/CALC-APERTURA-ENSU-2026-0001/spec.yaml` y correr (receta).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción: los contendientes se sellaron (`ejecucion.json` 2026-09-26T03:52Z y T04:33Z) antes de cualquier apertura de 2026, que sigue
  RESERVADA en el manifiesto; ninguna celda vista (§0). Nada RETROSPECTIVO se mezcla.
- Unidad: **persona urbana 18+** de las ciudades de interés; nada se promedia con hogar, delito o trámite.
- Escala: proporción 0..1 en R y en el piso; la comparación es «R dentro del IC calibrado del piso» (en logit); el MAE es
  descriptivo.
- Segmentación: un eje a la vez; ENSU no capta NSE ni escolaridad (NO-CONSTRUIBLE, spec SERIE §7): el sesgo de clase no se
  corrige aquí y se declara. Es urbana: nada dice del México rural.
- Violencia es estructura, no cultura: un SUBCUBRE dice que el piso del trimestre anterior no anticipa el siguiente, no que
  «cambió la psicología del mexicano».
- Cifras escritas a mano: ninguna; las constantes son hashes fijados y la regla (0.95, z = 1.959964), declaradas antes de abrir.
