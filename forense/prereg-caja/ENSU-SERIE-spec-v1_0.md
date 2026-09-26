# ENSU · pisos por segmento, serie trimestral 2013–2025 y dictamen por ciudad · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-SEGURIDAD-ENSU-SERIE-1`, 25/sep/2026, CAJA, rama
`gen2-seguridad-ensu-serie-1`, 0-bis `591689ab`. Encargo:
`forense/encargos/2026-09-25-GEN2-SEGURIDAD-ENSU-SERIE-1.md` (P2). CALC:
`CALC-ENSU-PISOS-0001` (pisos) y `CALC-ENSU-SERIE-0001` (serie, τ² y dictamen). Congelada en
el COMMIT-1, **antes** de leer un solo valor de microdato ENSU. **El primer resultado que
produzca este procedimiento es el que se reporta.** Lista cerrada, parte de esta spec:
`forense/analisis/seguridad-ensu/lista-cerrada-P1.md`.

## 0 · Exposición declarada y premisas verificadas

Esta sesión leyó, antes de congelar: el encargo; los métodos (no los resultados) de
`DONDE-CAMBIO-spec-v1_0.md` y `tools/series/dictamen.py`; la receta
`tools/dominios/salud/pisos_diseno.py`; la spec y el medidor de `CALC-ENGASTO-CONSUMO-PISOS-0001`
(forma); los FD ENSU 2013, 2015, 2016, 2019, 2020, 2021 y 2025 (estructura, catálogos, textos de
pregunta); los **nombres de columna** de las tablas CB y CS de los 48 trimestres
(`tools/dominios/ensu/cabeceras.py`); y el texto de las siete afirmaciones del mapa que cita la
lista §5, **que traen cifras de los comunicados INEGI** (p. ej. 63.0 % inseguridad 2025T3). Esas
cifras son públicas y se declaran vistas: por eso esta spec no pre-registra ninguna predicción
sobre ellas; el cotejo del Bloque C es RETROSPECTIVA. **Ningún valor** de microdato ENSU ni
ningún RESULT de ENSU (no existe ninguno: `ls data/corrida0 | grep -ic ENSU` → 0).

- `[EJECUTADO]` «164 payloads de ENSU» (encargo, ENTORNO): son 164 **menciones**; 30 entradas,
  13 bases de datos (lista §1). Logística; se declara.
- `[EJECUTADO]` «último trimestre publicado reservado»: 2026 (T1–T2 publicados) está reservado en
  el manifiesto y ausente del disco; último abierto 2025T4. Ningún trimestre de 2013–2025 se
  reserva: F-ASTRA-5-3 reserva «solo el último periodo publicado».
- `[SUPUESTO→EJECUTADO]` «factor y diseño por trimestre y ciudad»: sí (lista §2), con tres eras.
- `[SUPUESTO→NO-VERIFICADO]` «el cuestionario cambió en 2016 y 2020 (modo telefónico)»: 2016 sí
  (FD 2016: nuevo cuestionario `BP*`, `FAC_SEL`, `EST_DIS`). 2020: **ningún FD 2020–2021 menciona
  levantamiento telefónico** (`grep -ci telef` = 0 en los siete FD); lo que los FD sep/dic 2020
  documentan es que «se canceló el levantamiento del segundo trimestre a causa de la contingencia
  por COVID-19» y que en T3/T4 se aplicó la sección de victimización en lugar de «formas de
  enterarse». Se usa lo documentado (§5 R2) y la marca `PAR-2020` en todos los pares que tocan
  2020; el modo telefónico no se presume (A.15).
- `[EJECUTADO]` 2021T1 no publicado como microdato (lista §1): par 2020T4→2021T2 salta un
  trimestre; se declara, no se corrige.

## 1 · Unidad, universo, diseño

Unidad: **persona seleccionada de 18+** de la tabla CB (una por vivienda). Ponderador `FAC_SEL`
(E2/E3), `FACTOR` (E1). Estrato del bootstrap = `CD` + estrato de diseño (`EST_DIS`; E1 `EDIS`);
UPM = `UPM_DIS` dentro del estrato. Válido: factor > 0, estrato y UPM no vacíos. Sexo y edad por
las llaves de la lista §2; una llave CS duplicada sale del eje (`G-CS-DUPLICADA`), una persona sin
pareja CS cuenta en `G-JOIN-SIN-CS` y queda fuera de SEXO/EDAD pero dentro de TOTAL.

## 2 · Conductas

Las 15 de la lista §3, con su texto, numerador, universo y disponibilidad por trimestre (la
disponibilidad se deriva de las cabeceras y queda congelada en `spec.yaml:parametros.disponibilidad`).
Un trimestre en que el reactivo no existe no emite RESULT para esa conducta.

## 3 · Estimación (P3, pisos)

Proporción ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato, `PCG64(20260925)`, 1 000
réplicas, percentiles 2.5/97.5, UPM única de certeza, contrato conservador (réplica degenerada →
sin IC), receta común por sha256. Emite por celda `P`, `IC-LO`, `IC-HI`, `N` (personas sin
ponderar). Una celda sin personas emite `N`=0 y `P`/IC nulos.

## 4 · Puntos de entrada

- **`CALC-ENSU-PISOS-0001`** — trimestres **2024T1, 2025T3, 2025T4** (los que citan las
  afirmaciones §5 de la lista; 2025T4 es el último abierto). Las 15 conductas donde existen ×
  {TOTAL, SEXO, EDAD, ENT, CIUDAD}, un eje a la vez.
- **`CALC-ENSU-SERIE-0001`** — los 48 trimestres 2013T3–2025T4. Las 15 conductas × {TOTAL, SEXO,
  EDAD}; y CIUDAD (01–96) **sólo para C01-INSEG-CIUDAD**, desde 2016T1. Por qué sólo C01 por
  ciudad (PROPUESTO-POR-EJECUTOR, cláusula 3): la serie por conducta × ciudad completa son
  ≈ 250 000 RESULT; C01 es la conducta que el encargo y VIOL-035 piden por ciudad y la bandera de
  ENSU. El resto por ciudad queda en NO-CORRIDO con sucesor. Las celdas compartidas con el CALC de
  pisos se calculan con el mismo marco, semilla y réplicas: deben coincidir **exactamente**
  (control cruzado, spec §8).

## 5 · Comparabilidad del par (por texto; reglas en este orden, la primera que aplica)

Para cada serie (conducta, eje, categoría) y cada par de trimestres consecutivos disponibles (a, b):

- **R1** b = 2016T1 → `CAMBIO-DOCUMENTADO` (FD 2016: cuestionario `BP*` sustituye a `P*`,
  ponderador y estrato nuevos; el texto de C12 cambia).
- **R2** b = 2020T3 y conducta ∈ {C13, C14} → `CAMBIO-DOCUMENTADO` (FD sep 2020: la sección que
  antecede a 1.7–1.9 se sustituyó por victimización en T3/T4 de 2020; contexto de pregunta
  distinto). C01–C12 anteceden a 1.6 y no se tocan; C15 es la sección 3.
- **R3** eje ∈ {TOTAL, SEXO, EDAD}: el conjunto de códigos `CD` presentes cambia entre a y b
  (`G-<ola>-CIUDADES-SHA256` distinto) → `CAMBIO-DOCUMENTADO` (universo de ciudades; FD: catálogo
  de ciudades de interés, 32→54→91). El agregado «nacional» de ENSU es la suma de las ciudades de
  ese trimestre, no un universo fijo.
- **R4** si no → `COMPARABLE`. Todo par que toca 2020 lleva marca `PAR-2020`; el par
  2020T4→2021T2 lleva además `HUECO-2021T1` en la nota.

`NO-DOCUMENTADO` y `NO-COMPARABLE` no aparecen: todo par tiene fuente escrita (FD) o cae en R4
porque el FD de ambos trimestres trae el mismo texto y catálogo.

## 6 · IC calibrado de persistencia y dictamen (P3 · vocabulario DONDE-CAMBIO #1125)

Se aplica **sin cambios** `tools/series/dictamen.py` (input por sha256), que es la regla sellada
por `DONDE-CAMBIO-spec-v1_0.md` §2–§4:

- Tramo evaluable = corrida más larga de pares `COMPARABLE`/`CAMBIO-DOCUMENTADO` con `P`, `IC-LO`,
  `IC-HI` en (0,1) (desempate: la más reciente); `k` = olas del tramo.
- **τ² de persistencia, parámetro nuevo y reutilizable**: por eje, media entre pares de olas (peso
  igual por par) de la media dentro del par de Δ² en logit sobre series `COMPARABLE`; sin centrar ni
  restar ruido (método #1009/#1041, §3.3 de DONDE-CAMBIO). Se calcula **por cadencia**: trimestral
  (C01–C14; `RESULT-ENSU-DICTAMEN-TAU2-TRIMESTRAL-<EJE>`, ejes TOTAL, SEXO, EDAD, CIUDAD) y
  semestral (C15, T2/T4; `…-TAU2-SEMESTRAL-<EJE>`). Mezclarlas inflaría el τ² trimestral con
  cambios de medio año.
- Piso t−1 cubre a t si `p_b ∈ expit(logit p_a ± 1.959964·√(ee_a² + τ²))`, `ee_a` del IC de a.
- Dictamen, primera regla que se cumpla: `SIN-SERIE` (k < 3) · `CAMBIO-SOSTENIDO` (≥ 2 pares
  `COMPARABLE` FUERA en una dirección y estrictamente más que en la contraria; con `SUBE`/`BAJA`) ·
  `SALTO-DE-INSTRUMENTO` (≥ 1 par `CAMBIO-DOCUMENTADO` FUERA) · `SALTO-SIN-EXPLICAR` (≥ 1 par
  `COMPARABLE` FUERA) · `ESTABLE`. La quinta palabra es la sellada por #1125/#972; el encargo la
  omite de su lista de cuatro («ESTABLE · CAMBIO-SOSTENIDO · SALTO-DE-INSTRUMENTO · SIN-SERIE»):
  INTERPRETACIÓN-DECLARADA (cláusula 2) — se sigue el vocabulario **ejecutado** en #1125, que es
  el que la firma de mesa aprobó.

Declarado, no corregido (igual que #1125): τ² incluye los pares que después se juzgan, lo que
empuja hacia `ESTABLE`; un `CAMBIO-SOSTENIDO` aquí es conservador. Con 48 trimestres y 91 ciudades
un par FUERA aislado por azar es esperable (≈ 5 % por par): por eso un solo par FUERA no da
`CAMBIO-SOSTENIDO`. **Dictamen por ciudad** = el dictamen de la serie C01 × CIUDAD de esa ciudad.

Por serie emite `K`, `N-FUERA`, `DICTAMEN`, `DIRECCION` (`SUBE`/`BAJA`/`NINGUNA`), `DELTA-PP`
(p_fin − p_ini del tramo, en pp), `OLA-INI`, `OLA-FIN`, `N-CAMBIO-DOCUMENTADO`.

## 7 · Lo que no hace

No compara ENSU con ENVIPE (escalas y universos distintos, encargo §10). No evalúa
prospectivamente: todo es RETROSPECTIVA. No adopta, no mueve `celdas_validadas`. No abre 2026.
Escolaridad, formalidad, NSE y región: NO-CONSTRUIBLE en ENSU CB (lista §4). No atribuye causa:
«cambió la percepción» es un hecho de la serie, no de la psicología (v2.16 §3); la violencia es
estructura, no cultura.

## 8 · Controles y secuencia

1. **Sintético** (`tests/test_ensu_serie_gen2.py`): tres eras de llaves, zips anidados, DBF y CSV
   con `\r`, ids exactos por `corrida0._valida_outputs` en los dos puntos de entrada, reglas R1–R4,
   guardia 2026, medidor byte a byte.
2. **Oro**: no hay CALC ENSU previo. Control cruzado interno: toda celda común PISOS/SERIE
   (TOTAL/SEXO/EDAD de 2024T1, 2025T3, 2025T4; C01 × CIUDAD) debe ser idéntica (Δ = 0).
3. **Cotejo externo (Bloque C, retrospectivo)**: cada cifra de las afirmaciones §5 frente al
   RESULT: CONFIRMA si la cifra del report cae en el IC95 de diseño; MATIZA si cae fuera pero a
   ≤ 3 pp del punto o el report omite una reserva material (universo, denominador, trimestre);
   ROMPE si cae fuera a > 3 pp. Umbral de 3 pp fijado aquí, antes de abrir.
4. Secuencia: COMMIT-1 (esta spec, lista, `spec.yaml`, medidor, test) → `preflight` VERDE →
   `run` PISOS → commit del sello → `run` SERIE → commit del sello → `verify` ambos → nota.

## 9 · Auditoría (afirma sobre México)

**Violencia es estructura.** Percepción de inseguridad y cambio de hábitos son respuesta
adaptativa a un entorno, no rasgo cultural. **Escala:** personas urbanas de las ciudades de
interés de ENSU, no México entero ni rural (el agregado «nacional urbano» de ENSU cambia de
ciudades con el tiempo, R3). **Clase:** ENSU no capta NSE; la brecha por clase no es medible aquí.
**Género:** la brecha por sexo es de percepción declarada, no de riesgo objetivo. **Cifra escrita a
mano:** ninguna; toda cifra de la nota cita su RESULT.

El primer resultado que produzca este procedimiento es el que se reporta.
