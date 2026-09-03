# P0 · ENMIENDA 4 a `tools/extrae_l_v1_1.py` — parche a la línea 136 y override de cuatro constantes

3/sep/2026, contra `68742de`. Ejecuta el P0 de la **ENMIENDA 4**, que sustituye
íntegra a la ENMIENDA 3 (commit `5bf4df4`, cuerpo «sin editar, dos constantes»
vs firma «parche a :136, cuatro constantes» — contradictoria) y gobierna sobre
las ENMIENDAS 1, 2 y 3 para este mismo asunto. Precedente: `ADR-282`, N4,
firma `DL-(1)`.

## Edición mínima aplicada

`tools/extrae_l_v1_1.py`:

- Se añade la constante de módulo `CELDAS_ESPERADAS = 11` (cerca de
  `CORRIDAS_L`/`SALIDA_TSV`/`LOG_CIERRE`, con nota de procedencia de la
  enmienda).
- El literal `176` de la aserción (antes línea 136) pasa a
  `CELDAS_ESPERADAS * 2 * 8`.
- Nada más del archivo se toca. Los pasos (1)–(8) de
  `regla-extraccion-L-v1_1.md` quedan intactos (no se editó `extraer_valor`
  ni `_localizar_seccion`).

**`sha256` del script parcheado**:
`efb71de15da18f8239647b0467f85e085f69450db12c5a54728af66aac1ab48f`

El previo (script sin editar, el que corrió `E21`):
`cac791efe18b257ecf31f916cd8fe82ff3675228e9876f79baad9107178c086b` — queda
como historia, no se recongela en ningún sitio más.

## Override en runtime de las cuatro constantes

Patrón `PAQUETE-L-v1_2.md` §4 (mismo mecanismo sellado ahí para
`runner_l_cli.py`/`carga_l_v1_1.L_SPEC_JSON`): importar el módulo por ruta con
`importlib.util`, asignar los atributos de módulo, y solo entonces llamar a
`procesar_176()`. Ningún archivo sellado se edita para esto.

- `CORRIDAS_L` → directorio temporal con enlaces simbólicos a las capturas
  seleccionadas **por `id_celda` derivado de la spec, no por sufijo de
  archivo** (el glob `*-M-*.json` de `corridas-L/` trae hoy 304 archivos de
  19 celdas — 11 de v1_1 más 8 nuevas de v1_2 — así que filtrar solo por
  sufijo habría sido incorrecto).
- `SALIDA_TSV` → `forense/prereg-duelo-v2/L-extraido-v1_2.tsv`.
- `LOG_CIERRE` → `forense/prereg-duelo-v2/L-extraido-v1_2-notas-cierre.md`
  (ruta distinta a la de `E21`, `L-extraido-v1_1-notas-cierre.md` — el
  override nunca pudo sobreescribir el cierre sellado, y se verificó después
  de correr que su `sha256` no cambió).
- `CELDAS_ESPERADAS = 14` (14 celdas de `L-spec-v1_2.json`).

## Control (a) — reproducción byte a byte

Override apuntado a las 176 capturas de v1_1 (las 11 celdas de
`L-spec-v1_1.json`, seleccionadas por `id_celda`) con `CELDAS_ESPERADAS = 11`
(176 = 11×2×8) y `SALIDA_TSV`/`LOG_CIERRE` a rutas temporales:

- TSV generado idéntico byte a byte al `L-extraido-v1_1.tsv` del repo.
- `sha256` del TSV generado: `22915b5c39e09136e4d7b8547c092fc30a2b8b4386044c715331fde82a675110`
  — coincide con el sellado (`22915b5c…5110`).

**PASA.**

## Control (b) — regresión CIV-08

`--regresion`-equivalente (`regresion_civ08()`) contra las 8 capturas de
piloto CIV-08: `Coinciden: 3/8`, `Divergen en valor: 5/8`,
`Piloto NO-DISPONIBLE, regla SI extrae: 0/8` — idéntico al sellado por `E21`
en `L-extraido-v1_1-notas-cierre.md`.

**PASA.**

Ambos controles pasan → no hay PARO; se procede a la corrida real.

## Corrida real v1_2

224 capturas (14 celdas de `L-spec-v1_2.json`: `CIV-M-01/02/04/10/12/13`,
`DIN-M-01`, `FAM-M-01/05/06/07`, `TRA-M-02/03/07`, 16 capturas cada una),
seleccionadas por `id_celda`, enlazadas por symlink en un directorio
temporal. Salida:

- `forense/prereg-duelo-v2/L-extraido-v1_2.tsv` — 224 filas.
- `forense/prereg-duelo-v2/L-extraido-v1_2-notas-cierre.md` — conteo
  `L-solo: 21/112`, `L+corpus: 12/112`, total `33/224`.

**Declarado, no corregido**: la primera línea de
`L-extraido-v1_2-notas-cierre.md` dice «Corrida real sobre las 176 capturas
`corridas-L/*-M-*.json`» — texto fijo del script (no parametrizado por la
enmienda, que solo autorizó tocar el literal de la aserción), reproduce el
`176` sobre las 224 reales de esta corrida. Es la instrucción explícita de
la ENMIENDA 4, no un defecto de esta ejecución.

Verificado tras la corrida: `forense/prereg-duelo-v2/L-extraido-v1_1.tsv` y
`L-extraido-v1_1-notas-cierre.md` (cierre sellado de `E21`) sin cambios
(`git diff` vacío, mismo `sha256` de antes de la corrida).

## CONSUMIDO

`sha256` del script parcheado (el mismo de arriba):
`efb71de15da18f8239647b0467f85e085f69450db12c5a54728af66aac1ab48f` —
`tools/extrae_l_v1_1.py`.

Ejecutado en la rama `claude/enmienda-4-linea-136-avb1y6`, contra `68742de`.
Perímetro: el de la ENMIENDA 3 (`tools/extrae_l_v1_1.py`, edición acotada a la
línea de la aserción y la constante `CELDAS_ESPERADAS`; se añade
`forense/prereg-duelo-v2/L-extraido-v1_2-notas-cierre.md`) — sin ampliar.

Firma de mesa (verbatim, ENMIENDA 4): «Autorizo el parche a la línea 136 y el
override de las cuatro constantes, incluida `LOG_CIERRE`; mi firma es la
fusión de este PR. — mesa, 3/sep/2026».
