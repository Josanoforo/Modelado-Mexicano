# ARBITRO-R-1 · PARO en P3 (regresión)

ENCARGO: `forense/encargos/2026-08-31-MAESTRA33-C2-ARBITRO-R-1.md`.

## P1 entregado

`tools/arbitra.py` — lee un marco congelado, filtra por columna de
elegibilidad, localiza el payload en `data/manifiesto.yaml` por
(encuesta, ola) con una heurística de sustring sobre `id`/`archivo`
(nunca inventa un `payload_id`), y escribe `corridas-R/<id>.json` con el
esquema leído dinámicamente de un archivo existente.

## P3 · regresión (ANTES de producir nada nuevo)

Comando ejecutado (contra copia en `$TMPDIR`, corridas-R/ real intacto):

```
python3 tools/arbitra.py forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv "" DIN-11 SFT-04 TIC-08
```

Resultado — **no coincide** con lo existente:

| celda  | R real (corridas-R/) | estado real | R del mecanismo nuevo | estado del mecanismo nuevo |
|--------|----------------------|-------------|------------------------|------------------------------|
| DIN-11 | 0.4583913965555015   | COMPUTADO   | (ninguno)              | NO-EJECUTABLE-SIN-CODIFICACION |
| SFT-04 | 0.0604055335123943   | COMPUTADO   | (ninguno)              | NO-EJECUTABLE-SIN-CODIFICACION |
| TIC-08 | 0.9044714694763597   | COMPUTADO   | (ninguno)              | NO-EJECUTABLE-SIN-CODIFICACION |

## Causa (verificada, no supuesta)

Ni `marco-M-congelado-v1_1.tsv` (27 filas) ni `marco-congelado-piloto-v1_0.tsv`
(60 filas) declaran, como columna estructurada:

- **codificación binaria** (qué valor de la variable es "sí"/1 y cuál
  "no"/0) — no existe columna `codificacion` en ninguno de los dos.
- **diseño muestral real** (estrato/UPM) — la columna llamada `estrato`
  en ambos marcos carga en realidad una etiqueta compuesta
  `dominio|grado_dependencia|dificultad` (verificado: fila `TRA-M-01`,
  valor `tramite|P1|MEDIA`), no una variable de diseño.

Los 9 R que sí existen en `corridas-R/` (vía
`forense/prereg-duelo-v2/correr-R.py`) se calcularon con esa
codificación y ese diseño **hardcodeados a mano por celda**, tras leer
el FD de cada encuesta — información que ningún marco de este acto trae
en forma legible por máquina. Un "árbitro genérico" que lea solo el
marco no puede reproducirlos sin inventar la codificación o el diseño;
`tools/arbitra.py` declara esa carencia (`NO-EJECUTABLE-SIN-CODIFICACION`
+ lista de columnas faltantes) en vez de adivinar.

## Veredicto (P3, verbatim del encargo)

> No coincide → PARO-reporta las cifras y el comando; no ajusta.

Este acto se detiene aquí. No corre `arbitra.py` sobre las 22 celdas
elegibles de `marco-M-congelado-v1_1.tsv` — hacerlo produciría 22 filas
`NO-EJECUTABLE-SIN-CODIFICACION` más, sin ningún R nuevo real, y el
encargo prohíbe seguir tras un no-coincide.

## CONTADOR

Puntos R nuevos: **0**. Este acto solo alcanzó la regresión (P3), como
el propio encargo prevé como resultado posible ("si este acto solo
alcanza la regresión, 0 y dicho").

## CIEGO

Este acto no abrió `corridas-M/` ni `milpa/tramite.yaml` en ningún
punto.

## Archivos abiertos (para auditoría del CIEGO)

`forense/encargos/2026-08-31-MAESTRA33-C2-ARBITRO-R-1.md`,
`forense/prereg-duelo-v2/marco-M-congelado-v1_1.tsv`,
`forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv`,
`forense/prereg-duelo-v2/corridas-R/*.json`,
`forense/prereg-duelo-v2/corridas-R/correr-R.py`,
`forense/prereg-duelo-v2/corridas-R/correr-B.py`,
`data/manifiesto.yaml`, `data/inventarios/alias-fuentes.yaml` (consultado,
no usado en la versión final del script), `tools/arbitra.py`,
`.claude/commands/arbitra.md`.

## Sucesor sugerido

Antes de que un acto sucesor intente calcular R sobre las celdas de
`marco-M-congelado-v1_1.tsv`, alguien tiene que producir, celda por
celda, la codificación binaria y el diseño muestral real (estrato/UPM)
leyendo el FD de cada encuesta — el mismo trabajo manual que
`correr-R.py` ya hizo para las 9 celdas del piloto. Es trabajo de
lectura de FD, no de automatización de marco.
