# Piso C2 de gobierno digital ENCIG 2025, re-medido desde microdato · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-ENCIG-PISOS-GEN2-1`, 24/sep/2026, CAJA, rama
`acto/gen2-encig-pisos-gen2-1`, 0-bis `19a384ae`. Encargo archivado:
`forense/encargos/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1.md` (P2). Congelada en el COMMIT-1,
**antes** de ejecutar su medidor sobre ENCIG 2025.

## 0 · Por qué existe, y qué cambió respecto del encargo

El `-C2-P` que el marcador consume de `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` se copia
(`medidor.py:639`) de las emisiones, que lo copian de `CALC-C2-COMPUESTO-RESERVADAS-0001`,
cuyos insumos numéricos son `milpa/tramite-ola5-propuesta-v0.yaml` (marginales a seis
decimales) y `milpa/tramite.yaml` (nacional): cadena legacy (firma S, ADOPCION-2).

El encargo pedía «el piso ENCIG **2023** medido desde microdato». Al verificar la premisa
contra el árbol, el piso del duelo **no es de 2023**: la spec del -0001 (§3) lo define como
`expit(L p₂₅(a) + L p₂₅(b) − L p₂₅)`, marginales **de la misma ola (2025)** sin
interacción, que es también la regla vigente de pisos en cruces (instrucciones v2.16 §4,
firma 17/sep). Lo legacy son los **números** de esos marginales, no la ola. Un piso 2023
cambiaría el contendiente C2 del duelo (PARO d del encargo). Pregunta a mesa (24/sep/2026),
respuesta **verbatim**: «Marginales 2025 (Recommended)» — «C2 con la MISMA definición,
re-medido desde el microdato ENCIG 2025: 11 marginales de un eje, que no están reservados,
más la composición y el IC por réplica. Es el precedente del piloto 3. Control: reproduce
CALC-ARBITRO-MARGINALES-ENCIG2025-0001 a 1e-10 y el C2 sellado a 1e-5. El -0002 hereda todo
lo demás por sha.» Por eso este CALC se llama `ENCIG2025-PISOS-…` y no `ENCIG2023-PISOS-…`
(el perímetro §9 del encargo nombraba el prefijo 2023 por la premisa que cayó).

Precedente: el piloto 3 (`CALC-GOB-DIGITAL-EXE-EMISIONES-0002`) ya compone su C2 desde
marginales de `encig25_base_datos_csv` y mesa lo acreditó `origen_numerico=NUEVO` en
`data/corrida0/decisiones.tsv`.

## 1 · Estimando, universo, celdas

**Mismo objeto que el duelo** (spec `ENCIG-DUELO-2025-cierre-spec-v1_0.md` §1, sidecar
`2cf3bb95…623d`): proporción de pagos ordinarios del servicio de luz (`N_TRA == 01`, texto
«el pago ordinario del servicio de luz?») hechos por canal digital (`P7_3 ∈ {4,5}`,
reactivo 7.3: internet/app · cajero o kiosco inteligente) entre los de canal válido
(`P7_3 ∈ {1,2,4,5,6}`), ENCIG 2025. **Unidad: TRÁMITE.** Ponderador `FAC_TRA > 0`; diseño
`EST_DIS × UPM_DIS` no vacíos; unión trámite→persona por `ID_PER`, `m:1` validada.
`SEXO` (1 hombre, 2 mujer), `EDAD` (18-29 · 30-44 · 45-59 · 60-96; 97 y 98/99 fuera del eje,
FP-399/F1-bis), `NIV` → escolaridad (`{0,1,2}` hasta primaria · `{3}` secundaria ·
`{4,5,6,7}` media superior · `{8,9}` superior), de `encig2025_02_residentes_sec_2.csv`.

**Marginales (11):** sexo 2, edad 4, escolaridad 4, total 1; **cada eje sobre su propio
denominador válido** (un trámite con edad fuera de 18-96 sigue contando en sexo y en el
total). Es exactamente la máscara de un eje del árbitro -0001 (`_r_y_marginales`, índice
`idx_m`) y la de `CALC-ARBITRO-MARGINALES-ENCIG2025-0001`.

**Celdas C2 (16):** `edad × sexo` (8) y `escolaridad × sexo` (8), por
`C2(a,b) = expit(logit p(a) + logit p(b) − logit p(total))`. Si algún término es 0, 1 o
indefinido, la celda es `None` (no se recorta).

**Agrupación: UNA sola variable, siempre.** Ninguna máscara combina dos ejes. El cruce 2025
ya fue visto por el -0001 (E.6); este CALC no lo necesita y no lo toca.

## 2 · Incertidumbre

La receta ENCIG (`tools/encig_cruces_historicos.py`, sha256 `31d7cf3b…8f83`, input
`origen: repo`, ejecutada desde sus bytes): `_load_wave` (universo y diseño), `_bootstrap`
(UPM con reposición dentro de estrato, singleton de certeza, réplicas en bloques de 50),
`_summary` (IC 2.5/97.5; contrato conservador: si una réplica degenera, no se publica IC).
**10 000 réplicas, `PCG64(20260919)`**: la semilla del duelo. La receta sortea sobre las UPM
del marco entero, así que las réplicas no dependen de qué máscaras se piden: con la misma
semilla, estos marginales tienen las **mismas réplicas** que los del -0001.

IC de C2: percentiles 2.5/97.5 de la composición réplica a réplica,
`expit(logit p_r(a) + logit p_r(b) − logit p_r)`, sólo si las 10 000 réplicas están definidas
y el control de marginales (§3) dio `REPRODUCE`; si no, `None` con el estado en
`G-C2-IC-ESTADO`.

## 3 · Controles (umbrales declarados aquí, antes de correr)

1. **Marginales** contra `CALC-ARBITRO-MARGINALES-ENCIG2025-0001` (GEN2, origen manifiesto):
   `-P` a `1e-10` y `-N` exacto en los 11 → `REPRODUCE`; si no, `NO-REPRODUCE` y el IC de
   C2 no se emite. (Ese CALC usó semilla 42 y otro medidor: sus IC no se comparan.)
2. **Contra el -0001** (`CALC-ENCIG-DUELO-2025-ADJUDICACION-0001`, sellado): el `C2-P` de
   aquí contra su `-C2-P-RECALCULADO` y el `C2-IC-LO/HI` de aquí contra el suyo, a `1e-10`
   → `REPRODUCE`. Es la prueba de que este piso es la misma composición que el árbitro ya
   calculó en la ola, ahora en un CALC de cadena limpia.
3. **Contra el C2 sellado (legacy), a `1e-5`** (el umbral del control 2 del -0001; C2 se armó
   con números públicos a seis decimales): `C2-P − C2-P(-0001)` por celda, su máximo absoluto
   y `G-CTRL-C2-SELLADO-VEREDICTO`. Mide cuánto difería el piso legacy del medido; no
   adjudica nada y no para. Se declara `origen_numerico: MIXTO` porque resta un número de
   cadena legacy.

Los dos inputs de control se declaran `funcion: CONTROL-HISTORICO`: no son insumo numérico
del piso. El `-C2-P`, los marginales y sus IC declaran `dependencias_numericas:
[encig25_base_datos_csv]`.

## 4 · Guardia y auditoría del código (en cada corrida; PARA si falla)

`auditoria()` sobre los bytes del propio `medidor.py`: (1) `.eq(` sólo dentro de
`_mascara1(frame, eje, valor)`, que admite cero o un eje y levanta `ReservaRota` ante
cualquier otro; (2) `_bootstrap` sólo se llama desde `_marginales`, que sólo usa
`_mascara1`; (3) `medir` llama `_guardia_inputs` (lista cerrada de cuatro inputs). Prueba
por mutación en `tests/test_encig_pisos_gen2.py`.

## 5 · Secuencia y validación D-22

COMMIT-1: esta spec + `spec.yaml` + `medidor.py` + test. COMMIT-2: `corrida0 run`, sello,
asiento de replay. Test D-22: (a) sintético — todas las ramas terminales (todo con soporte,
categoría con masa cero, celda que una réplica vacía, control que no reproduce) con
`corrida0._valida_outputs` vacío y ningún `NaN`/`inf`; (b) **oro 2023** con el corpus
montado: el medidor apuntado a `encig23_base_datos_csv` reproduce `-P` de
`CALC-PISOS-ENCIG2023-EJES-0002` a `1e-10`; (c) mutantes atrapados; (d) `resultados:` del
`spec.yaml` = `esquema_resultados()`. `corrida0 preflight` VERDE antes de commitear.

**Ejecución diagnóstica: ninguna sobre 2025.** El primer `run` es el resultado.

## 6 · Auditoría (afirma sobre México)

Contadores: una corrida sellada (`cuenta_gen2: SI`, no adopta). **Escala:** proporciones
de **trámites** de pago de luz; nada se promedia con cifras por persona. **Universo:**
ciudades de 100 mil habitantes o más; nada aquí habla de lo rural. Un gradiente por edad o
escolaridad describe **acceso y oferta** (cuenta bancaria, conectividad, cajeros) antes que
preferencia (§3: oferta antes que preferencia); el denominador es quien pagó, no quien pudo
pagar. **PROSPECTIVA vs RETROSPECTIVA:** este piso es **RETROSPECTIVA** — se sella después
de que el -0001 derivó R; su fórmula no tiene variante que seleccionar y no lee R.
**Cifra escrita a mano:** ninguna; los umbrales de §3 son los del -0001.

El primer resultado que produzca este procedimiento es el que se reporta.
