# ACTO GEN2-ARBITRO-MARGINALES-2 · P1 · clasificación de las 40 reglas · 21/sep/2026 · CAJA

Encargo: `forense/encargos/2026-09-21-GEN2-ARBITRO-MARGINALES-2.md` (0-bis `8a5badd5`).
Rama `acto/gen2-arbitro-marginales-2`, worktree `/home/pc0/mm-arbitro-marginales-2`.
Sonnet 5, MODO ABIERTO hasta cada COMMIT-1. Entorno derivado CAJA (`tools/entorno.py
--arranque`: corpus montado, 436 archivos examinados; `sin_variable`; red 200 vía
proxy=NO). SHA de redacción del encargo `99a43faf` = `origin/main` al abrir (0 commits
de diferencia).

Tabla: `data/arbitro-marginales-2-clasificacion-v1_0.tsv` (40 filas, generada por
`data/arbitro-marginales-2-clasificacion-v1_0.tsv.build.py` desde
`milpa/tramite-ola5-propuesta-v0.yaml` — campos numéricos derivados, no tecleados).
**Conteo: RE-MEDIDA 16 · SIN-PAYLOAD 3 · FUERA-DE-ALCANCE 21.**

## 0 · Premisas verificadas contra `99a43faf`

- `[EJECUTADO]` 53 reglas totales en `milpa/tramite-ola5-propuesta-v0.yaml`
  (`reglas_propuestas`), verificado con `yaml.safe_load` + `len()` — **cierto**,
  coincide con el encargo.
- `[EJECUTADO]` las 13 reglas con `payload_manifiesto_id` exactamente
  `envipe2025_csv` (4), `encig25_base_datos_csv` (4) o `enif_2024_enif_2024_bd_csv`
  (5) son las que `#971` re-midió — **cierto**, 53 − 13 = 40, coincide con el conteo
  del encargo. Excluidas de la tabla de este acto (columna `YA_CUBIERTAS_971` del
  script generador).
- **Hallazgo sobre la premisa §3 del encargo (no bloquea, es logística/bookkeeping,
  §2 v2.16): el desglose `[EJECUTADO]` de dirección («15 sin payload · ENCUCI 4 ·
  EDER 3 · LAPOP 3 · ENNViH 1 · ENIGH 1 · ENFIH 1 · electorales 3») suma 31, no 40.**
  Verificado por conteo exacto de `payload_manifiesto_id` sobre las 40 (script de
  arriba, `Counter`): faltan por nombrar en la premisa 9 reglas reales — ICPSR
  MPS2012 (×2), `list::mexico` (×1), ENDUTIH2025 (×1), ENIF2024-respaldo (×1),
  CIDE-CSES2015 (×1), ENNViH real es **2** no 1 (falta `salud.atencion.
  grave_ennvih2002`), electorales real es **4** no 3 (falta
  `civico.participacion.concurrencia_presidencial_conversion`, que además YA está
  sellada en GEN2 — ver §2), y LAPOP real es **7** no 3 (2019 ×5 contando las
  reformuladas por `MAESTRA38-N5`, 2023 ×1, 2004 ×1). Ninguna de las 40 quedó sin
  clasificar — el hallazgo es que la premisa de dirección subestimó la heterogeneidad
  del árbitro, no que falte trabajo.

## 1 · Cómo se derivó cada destino (A.15 — por objeto, con comando)

- **Payload**: `python3 tests/manifiesto.py --verifica --id <id>` contra cada
  `payload_manifiesto_id` distinto de los 40 (17 ids únicos, algunos compuestos).
  **COINCIDE en los 17** — incluidos LAPOP 2019/2023 (`descargas_mx`), CIDE-CSES2015
  (`descargas_mx`), ICPSR MPS2012 (`descargas_mx`), `list::mexico` (`descargas_mx`),
  ENDUTIH 2025, ENNViH (2 olas + ponderador). El único caso sin id resoluble es
  `familia.apoyo.recibe_dinero_familiares`, cuyo campo es una nota de texto libre, no
  un id — verificado que `enif_2024_bd_csv` (el id que la nota sugiere) no existe en
  el manifiesto; el archivo real usado fue `data/raw/enif_2024_bd_csv.zip` por ruta
  directa, no por id.
- **Ya sellado en GEN2 (RE-MEDIDA sin trabajo nuevo)**: se buscó por contenido (nunca
  por nombre de carpeta) en `data/corrida0/*/spec.yaml`. Confirmado por lectura
  directa: `civico.participacion.concurrencia_presidencial_conversion` →
  `CALC-L8-CONVERSION-0001` (RES-0050/51/52, `ejecucion.json` presente, "NINGUNA
  cambia de cifra por esta corrida" — reproduce lo sellado en `milpa/tramite.yaml`,
  no adopta). `tramite.gobierno_digital.coercitivo_efirma_sat` y
  `tramite.gobierno_digital.coercitivo_tabla_de_universos` ya corrieron bajo GEN2
  (`MAESTRA36-L13`/`L14`, `data/l13-sat-efirma-v1_0.json` /
  `data/l14-coercitivo-universos-v1_0.json`) pero son **proporción administrativa
  agregada, no marginal de encuesta** (L13 mismo: "un campo del entorno, no una
  probabilidad individual de conducta") — clasificadas FUERA-DE-ALCANCE por esa
  razón, con la salvedad de que ya tienen medición GEN2 propia (no son deuda nueva).
- **SIN-PAYLOAD**: las 3 reglas que `MAESTRA38-N5` (COMMIT-2, 4/sep/2026) clasificó
  como (b) SIN-INSTRUMENTO con 4–7 formulaciones de búsqueda cada una contra
  `data/inventario-reactivos-descargas-mx-v1_1.tsv` (42536 filas, A.13 cumplido en
  esa pieza) y recomendación MANTENER-COMO-HIPÓTESIS. No se repite la búsqueda aquí
  — se cita, per E.5 "lo ya sellado se cita, no se re-mide".
- **FUERA-DE-ALCANCE por encuesta no nombrada**: ENDUTIH2025, ENIF2024 (2 reglas),
  ICPSR-MPS2012 (2), `list::mexico` (1), CIDE-CSES2015 (1). Todas con payload
  COINCIDE en el corpus — el corte es de **objetivo del acto** (el título nombra
  ENCUCI/EDER/LAPOP/ENIGH/ENFIH/ENNViH/electorales; estas seis fuentes no están en
  esa lista), no de disponibilidad de dato. Sucesor: un acto propio por encuesta,
  igual que `ARBITRO-MARGINALES-1`/`-2` hicieron con ENIF/ENVIPE/ENCIG/ENCUCI/EDER/etc.
- **FUERA-DE-ALCANCE, electorales**: 3 reglas de cómputos municipales por instituto
  electoral estatal (Coahuila/Nayarit/Zacatecas/Durango/BC/Chihuahua), tal cual el
  propio OBJETIVO del encargo las nombra como ejemplo.
- **FUERA-DE-ALCANCE, SHED2025**: población de EE. UU., ya sellada en otro acto
  (PR #745) con cláusula explícita de no-transporte a México — no es un marginal de
  encuesta mexicana y no lo será nunca por diseño de esa pieza.
- **FUERA-DE-ALCANCE, ENUT2024**: el propio encargo (§3) declara "no es este acto —
  mesa decide el rótulo"; el núcleo común de ENUT ya lo midió
  `GEN2-ENUT-PISOS-Y-SERIE-1` (`#976`).

## 2 · Pregunta a mesa — LAPOP (7 reglas), una línea con opciones

**P2 de este encargo no nombra LAPOP** en su lista cerrada de encuestas a re-medir
("ENCUCI 2020, EDER 2017, ENIGH 2022, ENFIH 2019, ENNViH si el payload está"), pese a
que el título del encargo sí nombra LAPOP y el payload de las olas 2019/2023 **SÍ
COINCIDE** en el corpus (`descargas_mx`, ya usado internamente por `MAESTRA38-N5` para
reformular 2 de las 7 reglas con reactivos concretos). La licencia de
AmericasBarometer/Vanderbilt no está verificada en el repo más allá de "derechos
reservados, términos de reuso no verificados" (`data/manifiesto.yaml`, entrada del
cuestionario); dos consultas a `vanderbilt.edu/lapop`/`cgd/data-access` (esta sesión,
21/sep) sólo confirman "Authors must not share data files… viola el user agreement" —
nada sobre publicar estadísticos agregados derivados.

**¿Cómo se clasifican las 7 reglas LAPOP?**
- **(A, tomada en esta tabla)** FUERA-DE-ALCANCE — no está en el lote de P2 de este
  acto; sucesor propio (`GEN2-ARBITRO-LAPOP-1` o similar) que primero verifique la
  licencia antes de abrir/medir.
- **(B)** SIN-PAYLOAD — tratar la licencia no verificada como bloqueo equivalente a
  payload ausente hasta que se resuelva (aunque el archivo sí está en el corpus).
- **(C)** RE-MEDIDA — añadir LAPOP como 6ª pieza de P2 en este mismo acto (excede el
  lote D-11 de cuatro piezas afines, y P2 no lo pidió).

Se sigue con las otras piezas mientras mesa contesta (D-19); si la respuesta es (C),
el sucesor de este acto es simplemente "en este mismo PR", y se declara en el cierre.

## 3 · Lo que esta pieza no hace

No re-mide las 13 de `#971`. No abre `envipe2026*`, `enigh2024*` ni crédito de ENIF
2024 (PARO b). No edita `milpa/tramite-ola5-propuesta-v0.yaml` ni ningún sello. No
adopta nada — `cuenta_gen2` de esta pieza es `NO-APLICA` (P1 no corre CALC, sólo
clasifica). El trabajo de re-medición real (COMMIT-1/COMMIT-2 por encuesta) es P2,
en la(s) pieza(s) siguiente(s) de este mismo acto.
