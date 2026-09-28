# Lanzamiento de las 312 residuales · ACTO GEN2-C1-SUCESORES-Y-LOTE-3 · P1

La receptora escribe este archivo **antes** de entregar ningún paquete, y lo commitea antes del lanzamiento. Ese commit fija la regla de dictamen y asiento antes de revelar, y cumple las compuertas del encargo §8: «paquete con sha antes de entregar» y «números del reconstructor antes de abrir sellados». La receptora no ha abierto ningún valor sellado de estas 312 llaves.

## 1 · Gates por paquete

Todos los paquetes usan la misma receta que C1-LOTE-3, el contenedor `residuales-documentales-v2` (#1229) y `CONTRATO-v3.md` (sha `821a5ecb…94eb`).

| Paquete | Llaves | APTO-TECNICAMENTE | CONTEXTO-NUEVO-ACREDITADO | CONTRATO-FIRMADO | ACCESO-AUTORIZADO |
|---|---:|---|---|---|---|
| `enbiare-pisos-bienestar-0001` | 180 | SÍ | SÍ, sujeto a auditoría del transcript | SÍ: R31 v3, R26 (a)+(b), R23 | SÍ: ADENDA-1 de FIRMAS-21, ENBIARE 2021 delimitado |
| `encodat-pisos-sustancias-0001` | 130 | SÍ | SÍ, sujeto a auditoría | SÍ: R31, R26 (b), R23 | SÍ: ADENDA-1, ENCODAT 2016-17 delimitado; 2025 reservada, no entra |
| `encuci-0001` | 1 | SÍ | SÍ, sujeto a auditoría | SÍ: R31, R26 (b), R23 | SÍ: firma de mesa del 28/sep en el chat del acto (abajo) |
| `enigh-0001` | 1 | SÍ | SÍ, sujeto a auditoría | SÍ: R31, R26 (b), R23 | SÍ: la misma firma |

Qué respalda cada gate:
- **APTO-TECNICAMENTE:** suite v3 15/15 OK en CAJA (Python 3.14.4, numpy 2.3.5, pandas 2.3.3); contenedor con sha; `entrada/allowlist.json` con el sha de cada archivo entregado.
- **CONTEXTO-NUEVO-ACREDITADO:** R32 (opción A) más la sonda de aislamiento de este acto (`lanzamiento-residuales/sonda-transcript.jsonl`). La sonda ve solo su propio directorio y `$TMPDIR`. No ve el repo, el corpus, `~/.claude/projects` ni `/mnt/c`, y la red a INEGI da `000`.
- **Firma de acceso a ENCUCI 2020 y ENIGH 2022**, verbatim (mesa, 28/sep/2026, chat de dirección de este acto): «mesa lo extiende ahora, en este chat, con el mismo régimen delimitado que ee49: olas vistas, módulos y campos del paquete, sin otra reserva.»

La R26 (b) se lee como firmada para las cuatro cohortes (ver `catalogo-1-sucesores/R26-…`). El registro que viaja en cada paquete es `FIRMAS-Y-ACCESO.md`.

## 2 · Delimitación de acceso

- **Por miembro:** solo los miembros de `allowlist.json → fuente_datos`, extraídos byte a byte y con el sha del ZIP verificado:
  - ENBIARE: `TENBIARE.csv`, `TSDEM.csv`;
  - ENCODAT: los dos `.dta`, Individual y Hogar;
  - ENCUCI: `SEC_4_5.dbf`, `SEC_6_7_8.dbf`;
  - ENIGH: el CSV de `concentradohogar` y su diccionario.
- **Por campo:** lo fija `campos_autorizados` en el prompt y lo verifica la auditoría del código entregado.

## 3 · Tolerancia (fijada antes de revelar)

`abs 1e-10, rel 0` para el punto y los dos extremos de IC en los cuatro paquetes. Es el `tolerancia.json` de lote 2 de cada paquete (`flotante, abs 1e-10`), traducido a v2 (`entrada/tolerancia-v2.json`). Los estados se comparan de forma literal.

## 4 · Regla de dictamen y asiento (fijada antes de revelar)

Los IC se reportan, pero son diagnóstico R23: sin el margen que fije mesa, no adjudican.

| Grupo | Comparación | Dictamen (vocabulario ASTRA6-1) | Asiento en `validaciones-independientes.tsv` (fila nueva, ref propia; unicidad por llave y ref, `dc4653ae`) |
|---|---|---|---|
| ENBIARE 126 (lote 2 punto COINCIDE, R28) · ENCODAT 130 · ENCUCI 1 · ENIGH 1 | punto e IC contra el sellado, `compare_v3` | punto dentro → SOSTENER; punto fuera → ACOTAR si la causa se identifica con los diagnósticos que la reconstructora selló, si no DISCREPA-SIN-CAUSA; sin estimación → según el estado | punto e IC dentro → PASA; punto dentro e IC fuera → CONCUERDA-NO-APROBADA; punto fuera → NO-PASA. Alcance con rótulo `C1-LOTE3-CIEGA-POR-CONTEXTO-NUEVO` y la tolerancia citada. |
| ENBIARE 54 (lote 2 NO-RECALCULABLE; estimando cambiado por R26 a) | contra el sellado, solo diagnóstica | SOSTENER-SIN-CORROBORACION (histórico); el valor queda como identidad sucesora `<llave>--R26A` | ninguno: la identidad sucesora no tiene RESULT sellado |

El grupo de 126/54 se toma de `catalogo-1-ejecucion-lote2/lote2-tabla-estimadores.tsv` (`estado_punto`), que solo se lee por rótulo. La receptora no conoce valores sellados.

## 5 · Orden E.2

1. Lanzar las reconstructoras.
2. Archivar `salida/` y el transcript con sha, y commitear y empujar.
3. Auditar el transcript (lecturas fuera del directorio, red, campos, modelo).
4. `runtime.py freeze-export` y `compare_v3 freeze`, y commitear.
5. Solo entonces construir la referencia desde el sellado y correr `compare_v3 compare`.
