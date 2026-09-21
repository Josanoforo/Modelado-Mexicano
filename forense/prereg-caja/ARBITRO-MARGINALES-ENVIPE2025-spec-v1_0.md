# ÁRBITRO GEN2 · marginales por eje · ENVIPE 2025 · evasión y denuncia · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-ARBITRO-MARGINALES-1 · pieza P-ENVIPE (21/sep/2026, CAJA). CALC:
`CALC-ARBITRO-MARGINALES-ENVIPE2025-0001`. Encargo archivado por A.3 en
`forense/encargos/2026-09-21-GEN2-ARBITRO-MARGINALES-1.md` (sello de cuerpo
`b6d73b3f…`). Compuerta interna del encargo (§8): este COMMIT-1 en `origin`
con su oro en verde protege **abrir dato**; ENVIPE 2025 no se abre antes.

## 1 · Qué estima (primera línea: universo, unidad, escala)

**Universo:** delitos de `tmod_vic` de ENVIPE 2025 (`envipe2025_csv`) con
ponderador `FAC_DEL` positivo y diseño `EST_DIS × UPM_DIS` no vacío; para
`evasion`, `BP1_20 ∈ {1,2}`; para `denuncia`, `BPCOD = 01` (robo total de
vehículo) y `BP1_20 ∈ {1,2}` y `BP2_1 ∈ {1,2}`. Cada eje conserva su
denominador válido. **Unidad:** DELITO. **Escala:** proporción ponderada en
[0, 1], IC95 por bootstrap de UPM estratificado (10 000 réplicas,
`numpy.PCG64(42)`, percentiles 2.5/97.5, réplicas compartidas).

**Estimando:** `evasion` = `BP1_20 = 2` y `BP1_23 ∈ {04,05,06,08}` (la
conjunta, no la condicional) por sexo (1/2), edad (18-29 / 30-44 / 45-59 /
60-96), escolaridad (proxy de formalidad: `NIV` de `tsdem` vía `ID_PER`) y
dominio (Rural / Complemento urbano / Urbano); `denuncia` = `BP1_20 = 1` por
cobertura de seguro (`BP2_1`: asegurado / no asegurado); más el total por
desenlace. Es la **realidad R** contra la que se califica el piso de
persistencia t-1 (`CALC-PISOS-ENVIPE2024-EJES-0002`).

## 0 · Exposición declarada (ADR-46)

- Leídos antes de congelar: medidor y spec sellados del piso
  (`PISOS-ENVIPE2024-ejes-spec-v2_0.md`), el yaml del árbitro con sus `p`
  GEN1 de 2025 a la vista (`tramite.evasion_norma_ejes_envipe2025`,
  `civico.denuncia.con_seguro_ejes_envipe2025`), y los RESULT de control de
  `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001` (`CTRL-ARBITRO-*`, deltas ≤ 5e-7
  contra GEN1, sin `P` sellado por marginal).
- NO abierto: ningún microdato de ENVIPE 2025 ni de `envipe2026*`. Sí
  abierto ENVIPE 2024 (ola anterior, no reservada) para la prueba de oro.
- Cifra esperada: las GEN1 existen y se citan en la adjudicación; no
  gobiernan este procedimiento.

## 2 · Procedimiento: el del piso, apuntado a la ola nueva

`medidor.py` IMPORTA por ruta (input `MEDIDOR-PISO-EJES-0002`, sha256
`0a1f3385…`) `_csv`, `_code`, `_age`, `_school`, `_slug`, `_cells`,
`_estimate` del piso; añade sólo el mapa de miembros por ola y la guardia.
Con `parametros.ola = "2024"` sobre `envipe2024_csv` el mismo punto de
entrada reproduce los 90 RESULT del piso sellado con Δ = 0 (prueba de oro,
`tests/test_arbitro_marginales_envipe2025.py`); con `ola = "2025"` mide R.

**Mapa 2024 → 2025 (A.15):** sólo cambian los nombres de miembro
(`conjunto_de_datos_tmod_vic_envipe2024.csv` → `…_envipe2025.csv`;
`conjunto_de_datos_tsdem_envipe2024.csv` → `…_envipe2025.csv`). Variables y
catálogos idénticos, ya verificados sobre 2025 por el árbitro GEN1
(`MAESTRA35-L1 P4`, `L7`) y por `tools/celda_d/marginales_reproduccion.py`
(`carga_ola(zip, 2025)`): `BP1_20`, `BP1_23`, `BP2_1`, `BPCOD`, `FAC_DEL`,
`EST_DIS`, `UPM_DIS`, `ID_PER`, `SEXO`, `EDAD`, `DOMINIO` (`R/C/U`) en
`tmod_vic`; `NIV` (00-09, `catalogos/niv.csv`) en `tsdem`. Unión delito ←
persona por `ID_PER`, `m:1` validado, cero huérfanos esperados (diagnóstico
`G-JOIN-SIN-DEMOGRAFIA`).

## 3 · Celdas del marcador que cubre (por id)

Las 15 filas `SOLO-PISO` de ENVIPE 2025 en `marcador-segmento.tsv`
(`55c8d57c`): 13 de `tramite.evasion_norma_ejes_envipe2025` y 2 de
`civico.denuncia.con_seguro_ejes_envipe2025`, enlazadas en
`ARBITRO-MARGINALES-metadatos-v1_0.tsv`: id de R = id del piso con
`RESULT-PISOS-ENVIPE2024-V2-` sustituido por `RESULT-ARBITRO-ENVIPE2025-`.
Además el total por desenlace y los diagnósticos `G-*`.

## 4 · Guardia de una sola variable (firma 3D)

Como en P-ENIF; el único `merge` autorizado es delito ← persona por
`ID_PER` con `validate="m:1"` dentro de `_carga` (regla R2b de la
auditoría AST; no agrupa, adjunta atributos). Reserva: con `ola ≠ 2025`
ningún input que nombre 2025; ningún input ni constante nombra 2026.

## 5 · Nulos y ramas terminales (D-22 ampliada)

Como en P-ENIF: `-P/-IC-LO/-IC-HI` con `permite_no_estimable: true`
(categoría sin masa → `None`); el resto nunca nulo; sintético con categoría
vacía y eje vacío por `corrida0._valida_outputs`.

## 6 · Lo que NO hace

No agrupa por dos variables (los 4 cruces `RESERVADA` siguen reservados;
el par edad×dominio consumido, NC-0328, no se toca) · no abre 2026 · no
adopta · no corrige el yaml GEN1 · no compara contra el piso (eso es
`CALC-ARBITRO-PERSISTENCIA-ERROR-0001`).
