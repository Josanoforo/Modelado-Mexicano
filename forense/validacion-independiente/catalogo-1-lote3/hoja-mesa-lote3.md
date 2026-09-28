# Hoja para mesa · lote 3 de C1 · ACTO GEN2-ASTRA6-C1-LOTE-3

28/sep/2026 · La redacta la sesión receptora; mesa sella. Nada de esta hoja adopta cifras ni toca sellos.
Filas FP de esta hoja: `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01..02` (append en `forense/firmas-pendientes.tsv`).

## En una frase

Entraron 92 de las 404 llaves: todas las de ENDIREH 2016, la única fuente con acceso firmado. Una sesión nueva de Claude, sin historial, recalculó las 92 desde la spec humana. El punto coincide con el sellado dentro de 1e-10 en 90. Las otras 2 difieren por una lectura de la spec (EDAD = 98 en «60+»). El IC no coincide en ninguna bajo 1e-10: otro generador de bootstrap, diferencias de 0.12–0.42 SE. Dictamen: **SOSTENER 90 · ACOTAR 2**. Cero PASA; el contador no se mueve.

## 1 · Recibo de las dos sesiones

| Sesión | Qué hizo | Transcript | sha256 |
|---|---|---|---|
| Receptora (esta) | preparó y entregó el paquete, recibió la salida, la congeló, abrió el sellado y comparó | el de esta sesión de Claude Code (Opus 5.5); todo lo que produjo está en la rama `acto/GEN2-ASTRA6-C1-LOTE-3` | — |
| Reconstructora | `claude -p`, Opus 5.5, `session_id` en el `init` del transcript; 30 turnos, 223 s, US$1.80 | `endireh-pisos-2016-pareja-fisica-0002/reconstructora/transcript.jsonl` | `61aac0a9704da0b308748db152eeb2b5bf2b5093fbb0753966068a347c1c3063` |

Auditoría del transcript (`endireh2016-pf-l3--auditoria-transcript.json`, regla escrita antes de leerlo, con control positivo sobre la sonda 1):
- 29 llamadas: Bash 9 · Read 12 · Grep 5 · Write 3.
- **0 rutas fuera del directorio de trabajo, 0 comandos con red.**
- Columnas pedidas por el código: todas dentro de `ee49-02`; ningún `read_csv` sin `usecols`.
- Modelo único: `claude-opus-5-5`.
- Dos comandos Bash fueron denegados por permisos (inspeccionar el FD e imprimir un resumen). La sesión los rehízo con Read y Grep dentro del paquete.

## 2 · Gates por paquete

| Paquete | Llaves | APTO | CONTEXTO-NUEVO | CONTRATO | ACCESO | Estado |
|---|---:|---|---|---|---|---|
| `endireh-pisos-2016-pareja-fisica-0002` | 92 | SÍ | SÍ (auditado) | SÍ (26a2-01) | SÍ (ee49-02) | LANZADO |
| `enbiare-pisos-bienestar-0001` | 180 | — | — | — | NO | NO-LANZADO (gate) |
| `encodat-pisos-sustancias-0001` | 130 | — | — | — | NO | NO-LANZADO (gate) |
| `encuci-0001` | 1 | — | — | — | NO | NO-LANZADO (gate) |
| `enigh-0001` | 1 | — | — | — | NO | NO-LANZADO (gate) |

El detalle y la evidencia están en `LANZAMIENTO-LOTE3.md` §2.

## 3 · Conteos por dictamen (`dictamen-lote3.tsv`, 404 llaves)

| Dictamen | Llaves | Qué es |
|---|---:|---|
| SOSTENER | 90 | punto dentro de 1e-10; IC fuera por el generador de bootstrap (sin margen de equivalencia firmado) |
| ACOTAR | 2 | `RESULT-ENDIREH2016-PF-TABLA#4` y `#50` (edad 60+, vida y desde oct-2015) |
| PROPONER-SUSPENDER | 0 | — |
| SOSTENER-SIN-CORROBORACION | 312 | NO-LANZADO (gate ACCESO-AUTORIZADO); nada comparado |

Asiento en la vista: `CALC-ENDIREH-PISOS-2016-PAREJA-FISICA-0002 / RESULT-ENDIREH2016-PF-TABLA` → **NO-PASA**, tolerancia citada `abs 1e-10, rel 0`, rótulo `C1-LOTE3-CIEGA-POR-CONTEXTO-NUEVO`. `resultados_con_validacion_independiente` = 215 → 215.

## 4 · Propuestas para el catálogo v1.4

**FP 0c1f-01 · ACOTAR #4 y #50 (edad 60+).**
- *Qué pasó.* El sellado cuenta en «60+» a las 96 mujeres con EDAD = 98 («edad no especificada en personas de 15 años o más», FD TSDem). La reconstructora ciega las excluye de los grupos de edad.
- *Tamaño.* Δp = 7.7e-4 (0.13 SE) en vida y 4.9e-4 (0.11 SE) en la ventana reciente. Las 90 celdas restantes coinciden, así que es la única diferencia de lectura con efecto.
- *Recomendación.* Rótulo, no suspensión: la diferencia está muy dentro del IC. Spec sucesora (ADENDA-DE-SPEC) que fije el trato de EDAD = 98; el sello no se toca. Queda como D-15 en `specs-insuficientes-v1_1.tsv`.
- *Texto de firma.* «Las celdas RESULT-ENDIREH2016-PF-TABLA#4 y #50 quedan ACOTADAS en el catálogo v1.4 con el rótulo "60+ incluye EDAD=98 (edad no especificada, 96 casos)". Autorizo una spec sucesora que fije el tratamiento de EDAD=98; el sello no se edita.»

## 5 · FP que el lote necesita

**FP 0c1f-02 · las 312 residuales.** Las 56 «no reconstruidas» están contenidas en ellas.
- *Por qué no entraron.* Ninguna firma de acceso C1 cubre ENBIARE 2021, ENCODAT 2016, ENCUCI 2020 ni ENIGH 2022. Además, sus contratos sucesores siguen sin firma (fb50-01, 157c-01, 1653-01).
- *Opciones.* (1) Autorizar lectura ciega nueva por paquete con los cuatro gates y firmar los contratos sucesores, para lanzarlas en C1-LOTE-4 con esta misma receta. (2) Dejarlas SOSTENER-SIN-CORROBORACION.
- *Recomendación: (1).* La receta ya está probada y cuesta menos de US$2 por paquete.
- *Texto de firma.* «Autorizo la lectura ciega C1 de ENBIARE 2021, ENCODAT 2016, ENCUCI 2020 y ENIGH 2022, delimitada a los módulos y campos de los paquetes residuales v2, para una sesión reconstructora nueva por paquete bajo la receta de LANZAMIENTO-LOTE3; los contratos sucesores se firman por hash aparte. No adopta resultados.»

Sin FP nueva (NC 0c1f-03): **las 767 identidades ENDIREH 2021 con ventana** no estaban en el universo de este encargo, pero ya tienen acceso firmado (`ee49-01`). Son el candidato natural del siguiente lote con esta receta; lo decide dirección.

## 6 · Lo que esta hoja no pide

No pide un margen de equivalencia para el IC: es 157c-01, ya abierta, y su sucesor es GEN2-METODO-COMPARACION-INFERENCIAL-1. No pide broker: B sigue como meta. No pide la reserva por paquete: 26a2-03 sigue ABIERTA y este acto la aplicó de hecho.
