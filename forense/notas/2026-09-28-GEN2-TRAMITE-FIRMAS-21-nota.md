# Nota de cierre · ACTO GEN2-TRAMITE-FIRMAS-21 · 28/sep/2026

Encargo: `forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21.md` (+ ADENDA-1). SHA de redacción `3c55bfc5` = base (0 commits detrás). 0-bis `856059c5` (raíz `8560`). ENTORNO NUBE (hook: ENTORNO-DERIVADO = NUBE; corpus montado NO, 0 archivos; red DENEGADA). Cero microdato, cero mediciones. ADR: `ADR-260928-GEN2-TRAMITE-FIRMAS-21-8560-01`.

CONTADORES (derivados con csv.DictReader, HEAD vs árbol final): firmas_pendientes ABIERTA 41 → 28; no_corrido ABIERTA 509 → 496. adoptados: sin cambio (no adopta cifras).

## P2 · reservas y HOLDOUT
- [EJECUTADO] Premisa «campo `reserva`» cae (logística): el campo es `estado_reserva` con vocabulario cerrado (`tests/manifiesto.py` ESTADOS_RESERVA); «abierta» se expresa por ausencia.
- R04/R05: `estado_reserva: RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO-ABRIR` en `cses5_modulo5_2016_2021_csv` y `endutih_2025_endutih2025_bd_dbf` (token vigente de última ola; validador VERDE, 7198 entradas).
- R02/R03 (ABIERTA-COMO-VISTA): sin campo en el manifiesto (ya ausente); se retiran de `RESERVA_FUERA_DEL_MANIFIESTO` en `tools/corpus_loader.py` (defecto adyacente ≤10 líneas, D-21, declarado: sin ello la firma no surte efecto en el cargador).
- R06 ENIF 2024 m7: no se marca a nivel de payload (cerraría módulos 1–6; 69 archivos lo citan); la reserva por módulo sigue en `corpus_loader` con la firma citada.
- R09: CAAS 2015, ENG 2009, MIGRACIÓN 2002 — reserva E.6 levantada por escrito (esta firma). Sus payloads `cc1_inegi_*` viven en la raíz de custodia `reserva_respondentes` y el validador exige `estado_reserva` ahí: quitarlo exige mover el archivo, en CAJA → NO-CORRIDO. ENCRIGE 2016 conserva la preservación F5 R08 (sin cambio).
- R01 (b): columna `holdout_decision` en `milpa/catalogo-momentos-v0_1.tsv`; M09–M23 (15) GASTABLE-COMO-PISO (0 menciones en familias-2027/prereg-caja; M13 solo homónimo MAESTRA38-M13); resto NO-APLICA.

## P1 · asiento
Renglones FIRMADA aquí: R09 R11 R12 R13 R14 R17 R18 R19 R20 R27 R52 R53 (+ R48 y R50 con FP nuevas `FP-260928-GEN2-TRAMITE-FIRMAS-21-8560-01/-02`) y la FP de delegación `3fc6-01`. VIAJA-EN (A.12, no asentadas aquí): CALC-ALTERNOS-LOTE-1 → R01–R08, R10; C1-SUCESORES-Y-LOTE-3 → R15 R21–R26 R28 R33 y el acceso nuevo; R31/R32 ya FIRMADA por C1-LOTE-3 (#1282) (A.17). Para mañana (ABIERTA, `PLAZO 2026-09-29` en `gatea`, la tabla no tiene columna `plazo`): R46 R47 R49 R51. R58–R86 ya asentadas por HOJA-FIRMAS-21-1 (verificado por id). `decisiones-21.tsv`: 0 renglones PIDE-FIRMA.

## P4 · forma
R52: nota de idioma en `corpus/reports-v2/INDICE.md` vía su productor (`indice.py`; --verify VERDE). R53: L8 del report de duelo marcada «pendiente de cotejo de fuente y corte»; ROMPE clínicos DUEL-018/X04/X05 con reserva «una sola fuente». R50: sucesor GEN2-CORPUS-LICENCIAS-2 (ya en la NC 1997-01), no ejecutado.

## P3 · 19 NC-pregunta — decidido por delegación
| Letra | NC | Decisión | Acción |
|---|---|---|---|
| 1 | NC-0164 | (b) buscar fuente MX (aceptar estimandos ya firmado 15/sep) | sucesor GEN2-SONDA-DINERO-CREDITO-FUENTE-MX-1 |
| 2 | NC-0259 | (b) no acreditar a mano (ADR-522) | CERRADA |
| 3 | NC-0290 | redactar 4ª condición como PROPUESTA; sello → hoja | sucesor GEN2-TRAMITE-REGLA-ADOPCION-BLOQUE-1 + hoja |
| 4 | NC-0318 | irreversible (ENCO) | hoja de cierre |
| 5 | NC-0324 | (a) R01 en espera de enlace pre-R | sucesor GEN2-MOCIBA-F6-ENLACE-PRE-R-1 |
| 6 | NC-0335 | (a) sale de reintentos, hueco NO-ENCONTRADO | CERRADA |
| 7 | NC-0346 | (a) acreditación documental; (b) irreversible | sucesor GEN2-ACREDITA-CATALOGOS-PISOS-1 + hoja |
| 8 | NC-0438 | contrato rc=3 | sucesor GEN2-TUBERIA-VERIFY-RC-1 |
| 9 | …c09b-02 | (a) subir evidencia citando #1004 | sucesor GEN2-CROSSWALK-EJES-2 |
| 10 | …7e23-03 | (a) revisión manual retirada (derivada) | CERRADA |
| 11 | …0eca-02 | (a)+(b) CONSUMIDO/HISTÓRICO | sucesor GEN2-TRAMITE-COLA-VIEJA-2 |
| 12 | …fa47-02 | (a) HISTÓRICO-SIN-RETIRO | CERRADA |
| 13 | …e760-07 | irreversible (E.3 vía (i)) | hoja de cierre |
| 14 | …e760-11 | (a) 12 lecturas θ fuera del relevo | CERRADA |
| 15 | …5916-04 | (a) en cola con dueño | sucesor GEN2-SEGURIDAD-ENSU-CIUDAD-1 |
| 16 | …5916-05 | (a) límite del instrumento declarado | CERRADA |
| 17 | …c6d9-01 | forma: COMMIT-D ratificado | CERRADA |
| 18 | …c6d9-02 | forma: SIN-OBJETO D-14 | CERRADA |
| 19 | 33 NC | dueño asignado a cada una (sucesor en la fila); cierres por cita: NC-0279, NC-0280, c6d9-03, e773-02, 3fc6-01 | 5 CERRADA, 16 reasignadas, 12 = letras 1–18 |

Decisiones redactadas con lectura por subagentes (una pieza por grupo de letras; solo lectura), aplicadas por el hilo principal. Irreversible: `forense/analisis/hoja-firmas-21/hoja-cierre-irreversible-21.md` → FIRMAS-22.
