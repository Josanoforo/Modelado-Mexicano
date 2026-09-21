# ÁRBITRO GEN2 · marginales por eje · ENCIG 2025 · pago de luz por canal digital · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-ARBITRO-MARGINALES-1 · pieza P-ENCIG (21/sep/2026, CAJA). CALC:
`CALC-ARBITRO-MARGINALES-ENCIG2025-0001`. Encargo archivado por A.3 en
`forense/encargos/2026-09-21-GEN2-ARBITRO-MARGINALES-1.md` (sello de cuerpo
`b6d73b3f…`). Compuerta interna del encargo (§8): este COMMIT-1 en `origin`
con su oro en verde protege **abrir dato**; ENCIG 2025 no se abre antes.

## 1 · Qué estima (primera línea: universo, unidad, escala)

**Universo:** trámites de `encig2025_04_sec_7.csv` (`encig25_base_datos_csv`)
con `N_TRA = 01` (pago ordinario del servicio de luz) y `P7_3 ∈
{01,02,04,05,06}` (canal válido; 03 teléfono y 07/08/09/blanco fuera,
contados), ponderador `FAC_TRA` positivo y diseño `EST_DIS × UPM_DIS` no
vacío; sexo, edad y escolaridad vienen de `encig2025_02_residentes_sec_2.csv`
por `ID_PER` (`m:1`). **Unidad:** TRÁMITE (quien pagó doce veces contribuye
doce veces). **Escala:** proporción ponderada en [0, 1], IC95 por bootstrap
de UPM estratificado (10 000 réplicas, `numpy.PCG64(42)`, percentiles
2.5/97.5, réplicas compartidas).

**Estimando:** `digital` = `P7_3 ∈ {04,05}` (internet/app · cajero o kiosco)
por sexo (1/2), edad (18-29 / 30-44 / 45-59 / 60-96) y escolaridad (hasta
primaria / secundaria / media superior / superior), más el total. Es la
**realidad R** contra la que se califica el piso de persistencia t-1
(`CALC-PISOS-ENCIG2023-EJES-0002`).

## 0 · Exposición declarada (ADR-46)

- Leídos antes de congelar: medidor y spec sellados del piso
  (`PISOS-ENCIG2023-ejes-spec-v2_0.md`), el yaml del árbitro con sus `p` GEN1
  de 2025 a la vista (`tramite.gobierno_digital.util_sin_coercion_ejes_encig2025`),
  el medidor del piloto 3 (`CALC-GOB-DIGITAL-EXE-EMISIONES-0002`, misma
  unidad y universo) y sus 8 marginales de edad/escolaridad 2025 sellados
  (`RESULT-GOB-EXE15-2025-MARGINAL-*`), y FP-399 (edad 97 = censurada).
- NO abierto: ningún microdato de ENCIG 2025. Sí abierto ENCIG 2023 (ola
  anterior, no reservada) para la prueba de oro.
- Cifra esperada: las GEN1 y las del piloto existen y se citan en la
  adjudicación; no gobiernan este procedimiento.

## 2 · Procedimiento: el del piso, apuntado a la ola nueva

`medidor.py` IMPORTA por ruta (input `MEDIDOR-PISO-EJES-0002`, sha256
`29be74a2…`) `_csv`, `_code`, `_age`, `_school`, `_slug`, `_cells`,
`_estimate` del piso; añade sólo el mapa de miembros por ola y la guardia.
Con `parametros.ola = "2023"` sobre `encig23_base_datos_csv` el mismo punto
de entrada reproduce los 60 RESULT del piso sellado con Δ = 0 (prueba de
oro, `tests/test_arbitro_marginales_encig2025.py`); con `ola = "2025"` mide R.

**Mapa 2023 → 2025 (A.15):** sólo cambian los nombres de miembro
(`encig2023_04_sec_7.csv` → `encig2025_04_sec_7.csv`;
`encig2023_02_residentes_sec_2.csv` → `encig2025_02_residentes_sec_2.csv`).
Variables y catálogos idénticos, verificados sobre 2025 por el árbitro GEN1
(`MAESTRA35-L1 P3`, `NIV` 1 dígito 0-9) y por el piloto 3. **Edad 97/98/99
en 2025** (FP-399, firmada 20/sep/2026: 97 es edad real censurada): el
procedimiento del piso corta la edad en 18-96, así que esos trámites quedan
fuera del eje edad — se cuentan (`G-EDAD-97-N`, `G-EDAD-98-99-N`) y no se
reinterpretan aquí; siguen dentro de sexo, escolaridad y total.

## 3 · Celdas del marcador que cubre (por id)

Las 10 filas `SOLO-PISO` de ENCIG 2025 en `marcador-segmento.tsv`
(`55c8d57c`), enlazadas en `ARBITRO-MARGINALES-metadatos-v1_0.tsv`: id de R =
id del piso con `RESULT-PISOS-ENCIG2023-V2-` sustituido por
`RESULT-ARBITRO-ENCIG2025-`. Además el total y los diagnósticos `G-*`.

## 4 · Guardia de una sola variable (firma 3D)

Como en P-ENIF; el único `merge` autorizado es trámite ← persona por
`ID_PER` con `validate="m:1"` dentro de `_carga` (regla R2b). Reserva: con
`ola ≠ 2025` ningún input que nombre 2025/`encig25`. Ninguna función agrupa
por dos variables: los 2 cruces `RESERVADA` de ENCIG 2025 siguen reservados
(el piloto 3 ya consumió edad×escolaridad por su propio código; aquí no se
mira).

## 5 · Nulos y ramas terminales (D-22 ampliada)

Como en P-ENIF: `-P/-IC-LO/-IC-HI` con `permite_no_estimable: true`; el
resto nunca nulo; sintético con categoría vacía y eje vacío por
`corrida0._valida_outputs`.

## 6 · Lo que NO hace

No agrupa por dos variables · no adopta · no corrige el yaml GEN1 · no
compara contra el piso ni contra el piloto (eso es
`CALC-ARBITRO-PERSISTENCIA-ERROR-0001`).
