# Expediente de apertura · ENOE 2026T2 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que
mesa autorice, o mesa por escrito.

## 0 · Premisas

- [EJECUTADO] Id de la ola en `data/manifiesto.yaml` (lector YAML, filtro por id): `cc1_inegi_enoe_2026t2__enoe_2026_trim2_csv`
  (base de datos CSV, ZIP de 5 miembros, `estado_reserva: RESERVADA-NO-ABIERTA-NO-INDEXAR-L`, raíz `reserva_respondentes`).
- [LEÍDO] Contendiente sellado (regla 6: ninguno nuevo): `CALC-ENOE-PARTICIPACION-2024T4-0001` — piso ENOE 2024T4 con IC de
  diseño (bootstrap de UPM, 2 000 réplicas), 3 conductas × {TOTAL, SEXO, EDAD, LOCALIDAD, ESCOLARIDAD, ENTIDAD}; etiqueta
  «2024T4 abierta; 2026T2 RESERVADA y 2026T1 consumido para informalidad (C4), no son input». Spec humana:
  `forense/prereg-caja/COLA-ENOE-PARTICIPACION-spec-v1_0.md`. Publica P, EE, IC-LO, IC-HI, N; **sin IC de persistencia**
  (un solo trimestre).
- [EJECUTADO] Ningún CALC sellado lee un id de ENOE 2026T2 (`grep -l 'enoe_2026t2\|enoe_2026_trim2'` sobre los 390
  `data/corrida0/*/spec.yaml` → 0). Ninguna tasa de participación de 2026T2 citada en `forense/`, `canon/`, `docs/` (rg
  «ENOE…2026T2», «segundo trimestre de 2026»: las coincidencias son rótulos de reserva; la única afirmación enlazada a la
  ola en `forense/tablero/TABLERO-CARRILES.md` es de la familia 2027 ENOE-INFORMALIDAD, que este medidor no mide).
- [LEÍDO] 2026T1 (ids `enoe_2026_1t_*`) queda fuera: consumido para informalidad (C4) y con su propia reserva; no es input.
- [SUPUESTO→rama prevista] NUBE sin corpus montado: el FD 2026 no se lee aquí; los códigos se fijan **sobre el FD de la ola
  del piso** (`enoe_325_fd_c_bas_amp.pdf`, tabla SDEMT, citado en la spec del contendiente §0), rotulado así (§5). Nombre
  del miembro: `ENOE_SDEMT226.csv` por analogía con `ENOE_SDEMT424.csv`; el medidor lo resuelve por patrón
  `sdemt226.csv` (con o sin prefijo `ENOE_`, sin distinguir mayúsculas ni carpeta); cero o más de uno → PARO.

## 1 · Estimandos

Por cada conducta del contendiente y cada categoría de cada eje (144 celdas): **R = Σw·y / Σw** en ENOE 2026T2 (tabla SDEMT),
con la misma recodificación 1/0/fuera y el mismo universo del contendiente (su spec §2, `derivadas()` y CONDUCTAS del medidor
sellado, importado por bytes con sha256 fijado en `APERTURA-ENOE-2026T2-spec.yaml`):
- PARTICIPA-ECONOMICAMENTE: `clase1` = 1 (PEA) → 1; = 2 (PNEA) → 0; 15+.
- NO-ESTUDIA-NI-OCUPADO-18-24: entre 18–24 con `cs_p17` ∈ {1, 2} y `clase2` conocido: 1 si `cs_p17` = 2 y `clase2` ≠ 1; si no 0.
- MUJER-ENTRE-NO-ESTUDIA-NI-OCUPADO-18-24: entre quienes la anterior da 1: `sex` = 2 → 1; `sex` = 1 → 0.

## 2 · Universo, unidad, ponderador, diseño

Unidad persona. Universo: `r_def` = 0, `c_res` ∈ {1, 3}, `eda` 15–98; ponderador `fac_tri`; válido `fac_tri` > 0, `est_d_tri` y
`upm` no vacíos (`prepara_diseno` del motor). Ejes: SEXO (`sex` 1/2), EDAD (15-17, 18-24, 25-44, 45-64, 65+), LOCALIDAD
(`t_loc_tri` 1–4), ESCOLARIDAD (`niv_ins` 1–4; 5 fuera), ENTIDAD (`ent` 01–32). Payload:
`cc1_inegi_enoe_2026t2__enoe_2026_trim2_csv`. R es un punto; no se calcula IC de R.
**IC del contendiente por celda:** IC-LO/IC-HI sellados de 2024T4 (IC de diseño, percentiles 2.5/97.5 del bootstrap); punto
= P sellado. El contendiente no publica IC de persistencia; no se construye uno aquí.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce levanta
`ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo (dos llaves en
`groupby`/`value_counts`, `crosstab`, `pivot`, `pivot_table`, `unstack` o lectura fuera de `lee_payload_reservado` → PARO).
Única lectura: `lee_payload_reservado` (cabecera del miembro → columnas presentes → `lee_csv_zip` de la receta). Columna de
diseño o universo ausente (`fac_tri`, `est_d_tri`, `upm`, `r_def`, `c_res`, `eda`) → PARO; columna de conducta o eje ausente →
vacía → R None. Probado sobre sintético con el esquema SDEMT: `tests/test_apertura_enoe_2026t2.py` (con soporte, conducta sin
columna, categoría vacía, diseño ausente, auditoría y las 9 mutaciones) y `tests/test_prereg_aperturas.py`.

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi y R finitos. **Primaria** (una sola): cobertura k/n = #celdas con lo ≤ R ≤ hi, con IC de Wilson al
95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson; **SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si
Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Orden si dos filas pudieran cumplirse: NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE >
CALIBRADO (excluyentes). Secundarias, descriptivas, no adjudican: cobertura por conglomerado (conducta) y error absoluto
medio punto-del-piso vs R.
B-bis, declarado antes de ver el dato: el IC es **de diseño de 2024T4**, no un intervalo de predicción: no absorbe el error
muestral de R ni seis trimestres de cambio ni la estacionalidad T4→T2. **SUBCUBRE es el desenlace esperado aun sin cambio
real** (con errores iguales, P(|R−P| ≤ 1.96·EE) ≈ 0.83 por celda) y se lee como «el piso 2024T4 con su IC de diseño no
anticipa 2026T2», nunca como «cambió la participación». CALIBRADO = piso **corroborado en alcance**; SOBRECUBRE = IC
conservador (**acotado**). Falsador débil por construcción: se declara, no se corrige.
Una apertura sirve a todos los sellados antes: el único contendiente sellado es `CALC-ENOE-PARTICIPACION-2024T4-0001`.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- 2024T4 → 2026T2: seis trimestres y otra estación del año; el FD de 2024T4 (`enoe_325_fd_c_bas_amp.pdf`, «Estructura de la
  base de datos. 2025») ya es la edición 2025; se verifica que 2026 conserva SDEMT y sus nombres.

Regla fijada: si en caja, antes de correr, el FD 2026 no trae una columna del contendiente con el mismo texto de pregunta y
códigos, **esa conducta (o eje) sale NO-ESTIMABLE** (columna ausente → R None; no se recodifica ad hoc) y se declara en la
nota. Si trae la columna con códigos distintos, el acto de apertura PARA antes de correr y se emite una v1_1 (el código
congelado no distingue códigos). Leer el FD no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-ENOE-2026T2-<conducta>-<eje>-<cat>-R` (144), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`, `-MAE-PUNTO`, `-MARCA`
(= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE, Wilson y MAE cuando n = 0.
Contrato: `APERTURA-ENOE-2026T2-spec.yaml` (calc_id `CALC-APERTURA-ENOE-2026T2-0001`; payload con sha del manifiesto; medidor
sellado, `resultados.json`, receta, motor, guardia y plantilla como inputs `origen: repo` con sha).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción: contendiente sellado (`ejecucion.json` 2026-09-26T18:51Z) antes de cualquier apertura de
  2026T2, que sigue RESERVADA; ninguna celda vista (§0).
- Unidad: **persona** (15+, o 18–24 en las dos conductas NINI); nada se promedia con hogar, delito o trámite.
- Escala: proporción 0..1; la comparación es «R dentro del IC de diseño del piso»; MAE descriptivo.
- Estructura ≠ cultura: participación y NINI responden a oferta laboral y educativa, cuidado no remunerado y ciclo económico;
  una MUJER-ENTRE-NINI alta no es «preferencia femenina» (spec del contendiente §6). Oferta antes que preferencia (§3).
- Segmentación: un eje a la vez; LOCALIDAD es tamaño de localidad, no clase; el sesgo de clase media urbana no se corrige aquí.
- Cifras escritas a mano: ninguna; las constantes son hashes fijados y la regla (0.95, z = 1.959964); el 0.83 de §4 es una
  cota ilustrativa de la regla (Φ(1.959964/√2)·2−1), no un umbral.
