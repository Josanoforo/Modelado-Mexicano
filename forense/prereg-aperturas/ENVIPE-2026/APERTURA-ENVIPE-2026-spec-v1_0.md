# Expediente de apertura · ENVIPE 2026 (reserva restante) · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: lo que no leyeron los duelos
sellados sigue RESERVADO (E.6; firma FP-260922-GEN2-DUELO-ENVIPE2026-MARGINALES-2-b05c-01: «lo que no emita este CALC
sigue RESERVADA»); lo levanta el código congelado de este expediente, en caja, en el commit que mesa autorice.

## 0 · Premisas

- [EJECUTADO] Id de la ola en `data/manifiesto.yaml` (lector YAML, filtro por id): `envipe2026_csv` (datos abiertos CSV,
  sha256 `dd79f589…`, «no inspeccionado, solo hasheado»), **sin** `estado_reserva` en el campo; la reserva vive en
  `data/corrida0/decisiones.tsv` (`reserva:envipe2026`) y en la firma citada arriba. Vista
  `data/corrida0/aperturas-pendientes-v1_0.tsv`: `PREMISA-CAIDA-YA-ABIERTA` (apertura PARCIAL, abajo).
- [LEÍDO] Contendiente sellado (regla 6: ninguno nuevo): `CALC-ENVIPE-PERCEPCION-2024-0001` — piso ENVIPE 2024 con IC de
  diseño (bootstrap de UPM, 2 000 réplicas), 3 conductas × {TOTAL, SEXO, EDAD, ESCOLARIDAD, DOMINIO, ENTIDAD}; etiqueta
  «2024 abierta; 2026 RESERVADA (E.6), no es input». Spec humana: `forense/prereg-caja/COLA-ENVIPE-PERCEPCION-spec-v1_0.md`.
  Publica P, EE, IC-LO, IC-HI, N; sin IC de persistencia.
- [LEÍDO] Qué leyeron de ENVIPE 2026 los CALC sellados que la consumen (`spec.yaml:variables` con archivo `*2026*`):
  `CALC-DUELO-ENVIPE2026-EMISIONES-0001` y `-ADJUDICACION-0001`: `tmod_vic` (BP1_20, BP1_23, BPCOD, DOMINIO, EDAD, EST_DIS,
  FAC_DEL, ID_PER, SEXO, UPM_DIS; unidad **DELITO**) y `tsdem` (ID_PER, NIV, como eje del delito);
  `CALC-DUELO-ENVIPE2026-MARGINALES-ADJUDICACION-0001`: `tmod_vic` (BPCOD, BP1_20, BP2_1, EST_DIS, FAC_DEL, UPM_DIS).
  **Ninguno lee `tper_vic1`** ni los reactivos AP4_* de percepción (sección 4 del cuestionario principal).

### 0.1 · Celdas del contendiente ya vistas (RETROSPECTIVAS) y reservadas

Una celda del contendiente es «vista» si algún CALC sellado emitió (o pudo derivar de lo que leyó) su R: la proporción
ponderada por `FAC_ELE` de una conducta AP4_* entre personas elegidas de 18+ en una categoría de un eje. Los duelos
agregaron **delitos** ponderados por `FAC_DEL` (otra unidad y otra tabla), y usaron `NIV`, `SEXO`, `EDAD`, `DOMINIO` sólo
como ejes de delitos. Resultado [LEÍDO, por variable]: **0 de 138 celdas vistas; 138 reservadas**, todas PROSPECTIVAS.
Nada se reporta aparte como RETROSPECTIVO. Coincide con el asiento de los duelos en `data/corrida0/decisiones.tsv`
(`reserva:envipe2026-consumida-por-duelo`: «QUEDÓ SIN ABRIR y SIGUE RESERVADA … toda otra tabla del zip (el código sólo leyó
tmod_vic y tsdem), todo otro desenlace o variable»; ídem `…-marginales-2`). Exposición previa declarada en
`reserva:envipe2026`: «dirección vio titulares nacionales de denuncia en el comunicado de prensa» — denuncia, no percepción.
Lo que esta apertura consume de la reserva restante: las columnas del contendiente en `tper_vic1` y `NIV` de `tsdem` como
eje de persona elegida.
- [EJECUTADO] Ninguna cifra de percepción de ENVIPE 2026 citada en `forense/`, `canon/`, `docs/` (rg «ENVIPE 2026…%»,
  «ENVIPE 2026…percep»: las coincidencias son de 2024/2025 o rótulos de reserva).
- [EJECUTADO] Nombre de miembro 2026: el duelo sellado resolvió por sufijo
  `tmod_vic_envipe2026/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2026.csv` (`RESULT-DUELO26-ADJ-R-ND-MIEMBRO`);
  por la misma convención, este medidor resuelve por sufijo `conjunto_de_datos_tper_vic1_envipe2026.csv` y
  `conjunto_de_datos_tsdem_envipe2026.csv` [SUPUESTO por analogía; cero o más de uno → PARO].
- [SUPUESTO→rama prevista] NUBE sin corpus montado: los catálogos 2026 del paquete no se leen aquí; los códigos se fijan
  **sobre los catálogos de la ola del piso** (2024, spec del contendiente §0 y §2), rotulado así (§5).

## 1 · Estimandos

Por cada conducta del contendiente y cada categoría de cada eje (138 celdas): **R = Σw·y / Σw** en ENVIPE 2026, con la
recodificación y el universo del contendiente (CONDUCTAS, MAPAS, EDADES, `une()` del medidor sellado, importado por bytes
con sha256 fijado en `APERTURA-ENVIPE-2026-spec.yaml`):
- ESTADO-INSEGURO: `AP4_3_3` = 2 (inseguro) → 1; = 1 (seguro) → 0; 9 fuera.
- INSEGURO-CAMINAR-DE-NOCHE: `AP4_4_A` ∈ {3, 4} → 1; ∈ {1, 2} → 0; 5, 9 fuera.
- DEJO-PERMITIR-MENORES-SALIR-SOLOS: `AP4_10_02` = 1 → 1; = 2 → 0; 3, 9 fuera.

## 2 · Universo, unidad, ponderador, diseño

Unidad persona elegida de 18–97 (`EDAD`, tabla `tper_vic1`); ponderador `FAC_ELE`; válido `FAC_ELE` > 0, `EST_DIS` y `UPM_DIS`
no vacíos. Ejes: SEXO (1/2), EDAD (18-29, 30-44, 45-59, 60+), ESCOLARIDAD (`NIV` de `tsdem` por `ID_PER`, deduplicado:
00-02 / 03-05 / 06-07 / 08-09), DOMINIO (`U`/`C`/`R`), ENTIDAD (`CVE_ENT` 01–32). Payload: `envipe2026_csv`. R es un punto.
**IC del contendiente por celda:** IC-LO/IC-HI sellados de 2024 (IC de diseño); punto = P sellado. Sin persistencia.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce levanta
`ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo. Única lectura:
`lee_payload_reservado` — sólo `tper_vic1` y `tsdem` (nunca `tmod_vic`), sólo las columnas del contendiente. Estructura
ausente (`ID_PER`, `EDAD`, `FAC_ELE`, `EST_DIS`, `UPM_DIS`; `ID_PER` en `tsdem`) → PARO; conducta o eje ausente → vacío → R
None. Probado sobre sintético con el esquema del contendiente: `tests/test_apertura_envipe_2026.py` (con soporte, conducta
sin columna, categoría vacía, estructura ausente, auditoría y las 9 mutaciones) y `tests/test_prereg_aperturas.py`.

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi y R finitos. **Primaria** (una sola): cobertura k/n = #celdas con lo ≤ R ≤ hi, con IC de Wilson al
95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson; **SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si
Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Orden: NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO (excluyentes).
Secundarias, descriptivas: cobertura por conglomerado (conducta) y error absoluto medio punto-del-piso vs R.
B-bis: el IC es de diseño de 2024 (dos olas antes; ENVIPE 2025 está abierta pero ningún CALC sellado mide AP4_* sobre ella —
`grep -l 'AP4_3_3\|AP4_4_A\|AP4_10_02'` sobre los 390 `spec.yaml` → sólo el contendiente—: «nadie ocupó la fila»): no absorbe el error muestral de R ni el cambio 2024→2026. **SUBCUBRE es
esperable aun sin cambio**; se lee «el piso 2024 con su IC de diseño no anticipa 2026». CALIBRADO = piso **corroborado en
alcance**; SOBRECUBRE = **acotado**. Falsador débil por construcción, declarado.
Una apertura sirve a todos los sellados antes: el único contendiente sobre `tper_vic1` es `CALC-ENVIPE-PERCEPCION-2024-0001`.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- Periodo de referencia: la pregunta 4.10 de 2024 dice «Durante 2023» [LEÍDO, spec del contendiente §2]; se espera «Durante
  2025» en 2026 [SUPUESTO; lo verifica la receta paso 3]. Mismo texto con otro año = misma pregunta.
- Regla fijada: si en caja, antes de correr, el catálogo 2026 del paquete no trae una columna del contendiente con el mismo
  texto y códigos, **esa conducta (o eje) sale NO-ESTIMABLE** (ausente → R None; sin recodificación ad hoc) y se declara. Si
  trae la columna con códigos distintos, el acto de apertura PARA antes de correr y se emite una v1_1. Leer catálogos y
  cuestionario no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-ENVIPE-2026-<conducta>-<eje>-<cat>-R` (138), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`, `-MAE-PUNTO`, `-MARCA`
(= PROSPECTIVA). Ningún None/NaN fuera de R NO-ESTIMABLE, Wilson y MAE cuando n = 0.
Contrato: `APERTURA-ENVIPE-2026-spec.yaml` (calc_id `CALC-APERTURA-ENVIPE-2026-0001`). Como el payload no lleva
`estado_reserva`, el paso 4a de la receta (levantar custodia) no mueve nada; el cierre re-rotula la reserva en
`decisiones.tsv` como consumida por completo.

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción (contendiente sellado 2026-09-26T18:51Z; tper_vic1 2026 no leída por nadie, §0.1). Las
  RETROSPECTIVAS de los duelos (unidad delito) no se mezclan con esta cobertura en ninguna frase.
- Unidad: **persona elegida 18+**; nada se promedia con unidad delito (los duelos) ni hogar.
- Escala: proporción 0..1; «R dentro del IC de diseño del piso»; MAE descriptivo.
- Violencia es estructura: la percepción de inseguridad y la restricción a menores son respuesta adaptativa al entorno, no
  rasgo cultural. DOMINIO es urbano/complemento/rural, no clase; ESCOLARIDAD aproxima clase sólo en parte.
- Cifras escritas a mano: ninguna; las constantes son hashes fijados y la regla (0.95, z = 1.959964).
