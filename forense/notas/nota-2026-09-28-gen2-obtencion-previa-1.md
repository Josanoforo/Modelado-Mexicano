# Nota de cierre · ACTO GEN2-OBTENCION-PREVIA-1 · ADR-260928-GEN2-OBTENCION-PREVIA-1-8e6a-01

Encargo: `forense/encargos/2026-09-27-GEN2-OBTENCION-PREVIA-1.md` (SHA de redacción `b3bc5b2f`; base `feeabe59`, 0 detrás; 0-bis `8e6acaf2`). NUBE (sonda INEGI 200). Cero mediciones; no adopta; no abre microdato ni reservas. Cada pieza corrió en un subagente con perímetro propio (REGLAS-DE-LECTURA).

## Dictamen por letra (se devuelve a FIRMAS-21; ninguna NC se cierra)
| letra | archivo | hallazgo |
|---|---|---|
| A1 | `forense/analisis/obtencion-previa-1/P1-A1-M05-M23.tsv` | M05 EXISTE-NO-SATISFACE (RESULT en unidad delito, conjunta; falta persona y sanción creíble) · M23 EXISTE-SATISFACE con reserva (RETROSPECTIVA, solo descriptivo). La premisa de la hoja («no hay con qué responder») no se sostiene en ninguno de los dos. |
| A2 | `forense/analisis/obtencion-previa-1/momentos-09-22.tsv` | Los RES-0184…0197 sí están en `tabla-consumidores-v1_0.tsv` l.186–199, pero en la columna `slot`; el detalle por momento vive en `forense/analisis/astra4-relevo/`. 14 dictámenes: ninguno EXISTE-SATISFACE; M19 responde la pregunta del catálogo pero no es RESULT GEN2 (hace falta un CALC desde WVS7, que ya está en el corpus). El proxy de nube rechazó datos.gob.mx, gob.mx, Zenodo, Dataverse, Banxico, CONEVAL y cses.org (A.5). |
| D1 | `forense/analisis/obtencion-previa-1/P3-D1-descontinuados.tsv` | Ninguno sale DESCONTINUADO-CITABLE. CAAS, ENG (en realidad ENGPEE 2010) y ENCRIGE tienen SUCESORA-EXISTE (CPV2020-CAAS, CNGSPSPE→CNGE, ENCRIGE 2020 ya en el corpus); MIGRACIÓN 2002 queda NO-VERIFICABLE-DESDE-NUBE. La premisa de la opción (a) cae en 3 de 4. |
| I1 | `forense/analisis/obtencion-previa-1/P4-I1-enaproce.tsv` · `P4-I1-solicitud-LM.md` | R03 pide carga regulatoria **y** pago informal en empresas MIPyME. Ningún cuestionario de ENAPROCE trae pago informal, así que el microdato del LM tampoco resuelve esa mitad. Los datos abiertos 2018 (nuevos) cubren la carga en parte: solo micro y solo nacional. La solicitud al LM está redactada. Premisa corregida: el manifiesto tiene 24 entradas ENAPROCE, no 75. |

## Premisas que cayeron (logística; no PARO)
- «75 entradas enaproce_*» → 24 [EJECUTADO por el subagente P4 sobre 7 035 entradas].
- «RES-0184… no está en tabla-consumidores» → sí está, pero en la columna `slot` [LEÍDO l.186–199].

## Registro en el manifiesto: NO hecho
Se bajaron 16 payloads públicos a `data/raw/obtencion-previa-1/` (nube; ids, URL y sha en las tablas P3/P4). `tests/manifiesto.py --registra` rechaza todo registro porque la validación de todo el archivo falla en entradas ajenas (`enoe_2026_1t_csv`: el `estado_reserva` no está en `ESTADOS_RESERVA`, y la raíz `data_raw` es incompatible con la reserva). Intenté ampliar la lista en una línea y apareció un segundo choque, así que revertí. El append directo al manifiesto quedó denegado por permisos de la sesión. Queda NC; dos payloads ya estaban registrados por sha (Solicitud_Uso LM y el descriptor CAAS 2020).

## Registro en el manifiesto: HECHO (28/sep, tras orden de mesa)
Mesa, en el chat de la sesión: «no hay nada que decidir, regístralos y asegurate de que queden asentados donde deben de estar asentados». Se hizo un append directo a `data/manifiesto.yaml` de 14 ids, con el esquema de campos de `--registra`, porque `--registra` sigue rechazando por las entradas ajenas `enoe_2026_1t_*`. Los dos payloads cuyo sha ya estaba registrado no se duplicaron. `python3 tests/manifiesto.py --verifica <14 ids>` → `data_raw: coincide=14 · no_coincide=0`. Quedan asentados además en `data/curacion-registro/cola-adquisicion-registro.tsv` (dos filas: ENAPROCE P4 y D1 P3). `NC-…-8e6a-01` pasa a CERRADA. Sigue abierta `-02`: traer los payloads a caja.
