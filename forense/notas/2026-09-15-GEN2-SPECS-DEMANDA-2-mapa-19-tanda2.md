# ACTO GEN2-SPECS-DEMANDA-2 · tanda 2 del mapa de las 19 — nota de cierre

**Acto:** `ACTO GEN2-SPECS-DEMANDA-2`, 15/sep/2026, NUBE (`cloud_default`,
`data/raw` ausente, corpus `montado=NO`, `numpy`/`pandas`/`scipy`/`pyreadstat`
AUSENTES — verificado con `python3 tools/entorno.py`). Sobre `origin/main =
da9b47a361143d408cd9fd9c20d17b101c4fe381` (merge de `PR #775`,
`ACTO GEN2-SPECS-DEMANDA-1`, ya en el árbol).

Encargo archivado verbatim:
`forense/encargos/2026-09-15-GEN2-SPECS-DEMANDA-2.md` (0-bis `b7453f9`).

## Qué hace esta pieza

Cierra la tanda 2 que `ACTO GEN2-SPECS-DEMANDA-1 §NC-0193` dejó diferida:
las cuatro `CORR` que ese acto ya identificó como construibles sin bloqueo
material (`CORR-0016`, `CORR-0017`, residuos de `CORR-0009` y `CORR-0007`),
más `CORR-0010`/`CORR-0015` (P3) y las sondas de `CORR-0018`/`CORR-0008`
(P4). El detalle metodológico completo de cada pieza vive en su propia spec
congelada — esta nota es el índice y el resumen de comandos, no la
repetición.

## P1 · Capa 2 faltante

| `CORR` | pieza | resultado |
|---|---|---|
| `CORR-0016` | `prereg-caja-L8-CONCURRENCIA-CONVERSION` + `CALC-L8-CONVERSION-0001` | **SPEC-CONGELADA, 3/3**. Payload = artefacto de repo (`data/l8-resultados-tipo-boleta-v1_0.json`). Transformación determinista (`p0` de `por_transicion[]` + `beta_pres_pp/100`) reproduce los 3 valores legacy exactos con comando a la vista. |
| `CORR-0017` | `CALC-S7-L17-0001` (capa 2 nueva sobre `prereg-caja-S7-L17` v1.1, sellada, sin tocar) | **SPEC-CONGELADA, 2/2**. La medición YA CORRIÓ (`ACTO MAESTRA38-LOTE-ENSANUT` L17, 6/sep) y está SELLADA en `milpa/` — el hueco era registro, no medición. |

## P2 · Las parciales

| `CORR` | pieza | resultado |
|---|---|---|
| `CORR-0007` | `prereg-caja-ENVIPE-EVASION-NORMA` + `CALC-EVASION-NORMA-0001` | **6/8**. Corrección de premisa: `RES-0025`/`RES-0026` (`evasion_norma`) **sí** tenían valor MEDIDO/SELLADO desde el 2/sep (`ACTO MAESTRA35-N1`) — el mapa de tanda 1 decía "no tienen nada", falso, corregido con comando. Residuo real (`RES-0039..0042`) queda declarado explícitamente `DECISIÓN-DE-MESA-PENDIENTE` (`NC-0088`, propuesta sin firmar) — no se elige por mesa. |
| `CORR-0009` | `prereg-caja-ENIF-TIENE-AHORROS` + `CALC-TIENE-AHORROS-0001` | **AGOTADA, 9/9**. Dos correcciones de premisa: `RES-0031`/`RES-0032` ya MEDIDOS/SELLADOS (mismo acto, misma fecha que `evasion_norma`); `RES-0065` YA estaba relevado por `CALC-ENIF-0002` (sellado, `ADR-459`) desde antes de este acto — verificado con `grep -rn RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P data/corrida0/CALC-ENIF-0002/`. |

## P3 · Identidad y encadenamiento

| `CORR` | pieza | resultado |
|---|---|---|
| `CORR-0010` | `prereg-caja-ENIF-DINERO-FAMILIARES-VEJEZ` + `CALC-DINERO-FAMILIARES-VEJEZ-0001` | **AGOTADA, 2/2**. Identidad resuelta por hash (A.7): `sha256_payload` de la regla coincide exacto con `enif_2024_enif_2024_bd_csv` del manifiesto. `milpa/tramite.yaml:845` no se edita (`FUERA-DE-PERÍMETRO`, `NC-0195` sigue `ABIERTA`). |
| `CORR-0015` | `prereg-caja-ENIF-HORIZONTE-VIA-DERIVADOS` + `CALC-HORIZONTE-VIA-DERIVADOS-0001` | **AGOTADA, 7/7**. Condición de encadenamiento verificada cumplida: `CORR-0009` (padre) quedó agotada en esta misma tanda. Los 7 `RESULT` son aritmética exacta (complemento, inclusión-exclusión) sobre insumos ya sellados — cero microdato. |

## P4 · Sonda sobre lo que no tiene fuente

| objeto | pieza | resultado |
|---|---|---|
| `CORR-0018` | `forense/notas/2026-09-15-GEN2-SPECS-DEMANDA-2-sonda-CORR-0018.md` | `/sonda CONSTRUCTO`. Las 7 candidatas se resolvieron **dentro del propio repo** (`coeficientes_generador_medidos`, bloque hermano) — 6 de 7 con `sha256` confirmado contra `data/manifiesto.yaml`. `D3` (rotular `SIN-PROCEDENCIA-VERIFICABLE`) queda superada por el hallazgo; la tabla de candidatas es el insumo para formalizar sin arqueología nueva. |
| `CORR-0008` | `forense/notas/2026-09-15-GEN2-SPECS-DEMANDA-2-sonda-CORR-0008.md` | `/sonda LATERAL+HERMANAS`. Tres candidatas web quedan `SIN-FETCH` — bloqueo de red de **esta sesión**, confirmado por 3 mecanismos independientes (`curl` directo, estado del proxy, `WebFetch`) y por control de calibración contra `inegi.org.mx` (también bloqueado hoy). El expediente `03-ENNVIH-DIN-S6.md` ya está `LISTO-PARA-TITULAR` pero no cubre estos 2 `RESULT` — ampliarlo es la receta de un minuto. |
| `CORR-0001` | `forense/notas/2026-09-15-GEN2-SPECS-DEMANDA-2-CORR-0001-premisa.md` | **No se corrió `/sonda`** — el objeto ya está `EXISTE-SATISFACE` por identidad de payload (verificado desde tanda 1, `NC-0197`). Correr una sonda sobre una fuente ya localizada sería el defecto que `A.8` existe para prevenir. El bloqueo real es `D1` (decisión de mesa), documentado, no re-abierto. |

## Handoffs GATED

Ningún handoff llega a `data/cola-adquisicion-v1_0.tsv` ni a `tools/adq_*`:
`ACTO ADQUISICION-CONTINUA` está en vuelo sin PR abierto hoy (verificado,
`search_pull_requests`/`git ls-remote` sin resultado) y el perímetro de este
acto lo declara explícitamente fuera de alcance. Las candidatas de `P4`
quedan como tabla por consumidor en las dos notas de sonda — exactamente el
insumo que el servicio nuevo va a leer.

## Recuento del mapa

`data/corrida0/mapa-demanda-19-corr-v1_0.tsv`, tras esta tanda: **9
`SPEC-CONGELADA`** (4 tanda 1 + 5 tanda 2) · **2 `EXISTE-SATISFACE`** · **1
`EXISTE-NO-SATISFACE`** (`CORR-0007`, 6/8) · **7 `BLOQUEADA`**
(`CORR-0001`, `0004`, `0005`, `0006`, `0008`, `0018`, `0019` — todas con
bloqueador nombrado, seis de ellas esperando una de las tres firmas de
mesa que `ACTO GEN2-SPECS-DEMANDA-1` dejó armadas, más `CORR-0008` que
espera `NC-0156`).

## Contador

**Cero mediciones propias**, dicho sin disfraz. Nueve specs congeladas
(capa 1+2 donde faltaba alguna) es munición para CAJA, no una corrida.
