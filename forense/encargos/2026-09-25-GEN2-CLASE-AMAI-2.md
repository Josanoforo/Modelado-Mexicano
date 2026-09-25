# ENCARGO · ACTO GEN2-CLASE-AMAI-2 · La única reserva que mesa levantó por escrito: ENIGH 2024 se abre solo para los seis componentes AMAI y la distribución NSE nacional por hogares, con el medidor congelado de CLASE-AMAI-1, y el eje de clase entra al marcador donde la firma A4 lo autorizó

> ENTORNO: **CAJA** — ENIGH 2024 (reservada; apertura parcial por firma C7), ENIGH 2022, ENIF 2024, ENDUTIH 2023. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `40058c09` (re-deriva al abrir) · una sola sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus (mide; no bajar) · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie, con esas palabras.
CONTADOR: sella `CALC-AMAI-NSE-ENIGH-2024-0001` (`cuenta_gen2: SI`, `adopta: NO`) y la calibración; el eje NSE entra al marcador por A4 (adopción firmada; este acto la ejecuta por el derivador y mesa fusiona). `celdas_validadas` no cambia.

## 1 · OBJETIVO
(P1) **Apertura acotada** (E.6, firma C7): código congelado en COMMIT-1 que lee de ENIGH 2024 **únicamente** las seis variables de vivienda/escolaridad del jefe que la Regla AMAI 2024 usa (por texto de pregunta y nombre en el FD, citados) y el factor/estratos; guardia de una sola variable de agrupación (NSE), auditoría automática del código antes de abrir y prueba por mutación (una lectura de cualquier otra columna hace fallar la guardia). Ninguna conducta, ningún ingreso, nada más. (P2) Distribución NSE nacional por hogares 2024 y comparación con la publicada por AMAI (cita); `APROXIMACIÓN-DESVIADA` si excede el umbral fijado en la spec. (P3) Con la calibración 2024, el eje NSE entra al marcador para los instrumentos de A4 (ENIGH 2022, ENIF 2024; ENDUTIH 2023 rotulado aproximación): los RESULT de `CALC-AMAI-NSE-*-0001` (#1127) por id; ENDUTIH 2024–25 y ENIF 2021 fuera (DESVIADA). (P4) Cobertura por clase actualizada (`forense/analisis/clase-amai/`).
«Hecho»: COMMIT-1 con guardia y auditoría citados antes de cualquier lectura de 2024 · `CALC-AMAI-NSE-ENIGH-2024-0001` con sello, asiento, `verify` REPRODUCE, y `ejecucion.json` que lista exactamente las columnas leídas · manifiesto: ENIGH 2024 sigue `RESERVADA` con anotación `APERTURA-PARCIAL: C7, columnas […]` · marcador re-derivado en árbol con eje `nse` para los instrumentos de A4 (valores por derivador) · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas, verbatim
- **C7 (FIRMAS-16, 24/sep)**: «mesa levanta por escrito la reserva solo para los seis componentes AMAI y la distribución NSE nacional por hogares, con el medidor congelado de CLASE-AMAI-1 y guardia de una sola variable de agrupación; ninguna conducta se abre.»
- **A4 (FIRMAS-16)**: «NSE AMAI como eje del marcador: SÍ con reserva de instrumento: ENIGH 2022 y ENIF 2024; ENDUTIH 2023 como aproximación rotulada; fuera ENDUTIH 2024–25 (DESVIADA) y ENIF 2021.»
- **F-U5-2** (umbral y supresión en la spec antes de abrir), **E.6**.

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` CLASE-AMAI-1 (#1127): `forense/prereg-caja/AMAI-NSE-spec-v1_0.md` (+sidecar); CALC `AMAI-NSE-{ENDUTIH-2023/2024/2025, ENIF-2021/2024, ENIGH-2022}-0001` sellados. ENIGH 2024 en manifiesto con `estado_reserva: RESERVADA` (el duelo ENIGH abrió otra parte: su celda-D lo registra; **no se toca**). `[SUPUESTO]` que el medidor de #1127 lee las seis variables por nombre de columna parametrizable: la spec de este acto las fija para 2024 por texto de pregunta del FD 2024 (pueden haber cambiado de nombre).

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -c 'AMAI-NSE-ENIGH-2024'` → 0. `git ls-remote --heads origin | grep -i amai` → 0.

## 5 · PIEZAS
P1 COMMIT-1 (spec 2024, guardia, auditoría, mutación) → P2 COMMIT-2 (apertura acotada, distribución, calibración) → P3 marcador por derivador → P4 cobertura.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) leer de ENIGH 2024 cualquier columna fuera de las seis + factor/estratos (la guardia lo hace PARO técnico) · b) reescribir sellos de #1127 · c) meter NSE al marcador fuera de los instrumentos de A4 · d) cambiar la regla AMAI o el umbral después de COMMIT-1 · e) NUBE.

## 8 · COMPUERTAS
«COMMIT-1 con guardia de una variable y prueba por mutación antes de abrir» protege: **abrir dato** (E.6). «Eje al marcador solo por derivador y solo A4» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/AMAI-NSE-ENIGH2024-*`, `data/corrida0/CALC-AMAI-NSE-ENIGH-2024-0001/`, `tools/dominios/amai/` (parametrización 2024), `data/manifiesto.yaml` (solo la anotación de apertura parcial), marcador por derivador, `forense/analisis/clase-amai/`, TSV de gobierno, nota, L0, cascada. Ajeno: celdas-D, CALC de #1127, el resto de ENIGH 2024. En CAJA: las unidades de medición de esta tanda (otras olas).

## 10 · LO QUE NO HACE · SUCESORES
No mide conductas por NSE en 2024. Sucesores: catálogo v1.2 y FRONT-3 consumen el eje; DONDE-CAMBIO-2 por clase si mesa lo pide.

## NO-CORRIDO / RESERVAS

- Ninguno.

## CONSUMIDO

Ejecutado por PR #1152 (rama `acto/gen2-clase-amai-2`), ADR `ADR-260925-GEN2-CLASE-AMAI-2-f601-01`, 25/sep/2026.
