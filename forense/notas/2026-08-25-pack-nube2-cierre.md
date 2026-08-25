# PACK NUBE-2 — cierre de FP-118 + ejecución de FP-144/FP-147/FP-148 — nota de cierre

25/ago/2026, entorno NUBE, sesión única, Actos 1-3 en serie. Redactado desde el canon (SHA de redacción del pack: `dfdf4fd+`; `main` había avanzado por `CONGELA-SORTEA`/`ESCALAS-P2` al arrancar esta sesión — HEAD real `151cf04`, no es PARO, refrescado y reportado). ACTO 4 (`CORRE-R10.1`) queda explícitamente FUERA de este pack — es lanzamiento aparte en sesión fresca, no ejecutado aquí.

## Verificación de arranque

- Repo: clon existente en el contenedor de sesión, rama `claude/pack-nube-2-closure-yf52y2` sobre `151cf04` (merge de `#354`, `ACTO ESCALAS-P2`).
- `data/raw/`: ausente — no es PARO, este pack no descarga nada.
- Entorno: NUBE confirmado, sin microdato montado, sonda saltada.
- Tablero (`forense/firmas-pendientes.tsv`): verificado por comando (`awk -F'\t' 'NR>1 && $6=="ABIERTA"'`) que `FP-118` era la única fila `ABIERTA` antes de este acto.

## Acto 1 — FP-118

Ranura F0 firmada con la opción (i), sin variante. `data/diseno-muestral.yaml` fila ENNViH gana el campo nuevo `supuesto_varianza` (alta de vocabulario documentada en la cabecera del archivo, no un quinto valor de `estado` — precedente `FP-116` consultado y descartado por no aplicar). `FP-118` → `FIRMADA` + `ejecutada_en`. Tablero verificado en CERO `ABIERTA` tras el cambio.

## Acto 2 — FP-144 (ejecuta PROPUESTA-SELLADA de FP-131)

- `tests/test_celdas_d.py`: `DISENOS_DATOS` gana `experimento_aleatorizado_terceros`.
- `propuesta-motor-adaptativo-celda-v0_5.md`: addendum fechado (sexto cambio, versión sin subir).
- `milpa/procedencia.yaml`: octava clase `EVIDENCIA_EXPERIMENTAL_TERCEROS` (cita+llave_id obligatorios), nace VACÍA.
- Las dos citas de `Progresa_RCT` (`milpa/procedencia.yaml:715`, `milpa/refutations.yaml` `ref.A.05.no_saben_planear`) quedan EXCEPCIÓN FECHADA — sin fila de llave para `Progresa_RCT` en el registro de llaves, no hay `llave_id` que las reclasifique.
- `tests/test_celdas_d.py` revalida los 3 archivos de celdas-D sin regresión.

## Acto 3 — FP-147 + FP-148

Dos filas nuevas en `data/curacion-registro/necesidad-objeto-modelo.tsv`: `N34` (objeto `dinero.credito.baja_friccion_usura_dano_downstream`, reclama `EXP-COMPARTAMOS-1`, opción b — no reutiliza `confianza_institucional`/`radio_confianza`) y `N35` (objeto `trabajo.prestaciones.formalidad_pesa_mas_que_salario`, alimentada por `LLAVE2-DECRETO`/ENOE). A la llave `EXP-COMPARTAMOS-1` le falta su spec B-bis — acto futuro, no de este pack.

## Suite

`python3 tests/check.py --baseline`: VERDE antes y después de cada acto. Total pasó de **19 FAIL · 132 WARN** a **19 FAIL · 128 WARN** (neto −4: las cuatro firmas ejecutadas dejan de imprimirse en `T22`). `T15`/`T16` resincronizados (conteo de ADR 182→185 (renumerado tras colisión con `PACK-UBUNTU-2`/`PR #355`, quien fusiona segundo renumera), cifra de WARN vigente 132→128) en `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md`. Sin `--freeze` en ningún punto.

## ADR

`ADR-183` (Acto 1), `ADR-184` (Acto 2), `ADR-185` (Acto 3) en `canon/gobernanza-v1_15.md`.

## Perímetro

Tocado exactamente lo cerrado por el pack: `data/diseno-muestral.yaml`, `milpa/procedencia.yaml`, `milpa/refutations.yaml`, `tests/test_celdas_d.py`, `propuesta-motor-adaptativo-celda-v0_5.md`, `data/curacion-registro/necesidad-objeto-modelo.tsv`, `forense/firmas-pendientes.tsv`, `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`, esta nota. Nada de `corpus/`, `data/raw/`, `tools/`, el duelo, el sorteo ni el pool de 253.

## Contador de medición sobre México

Cero en los tres actos, declarado. Ningún número de medición sobre México se mueve.

## Lo que este pack NO hizo

No tocó corpus/microdato. No ejerció la llave `EXP-COMPARTAMOS-1` (falta su spec B-bis). No corrió `CAL-G3`. No tocó el duelo, el sorteo, el pool de 253 ni `tools/`. No archivó ningún veredicto de `CORRE-R10.1` — ese acto queda para lanzamiento aparte en sesión fresca, con su propia higiene de contexto.
