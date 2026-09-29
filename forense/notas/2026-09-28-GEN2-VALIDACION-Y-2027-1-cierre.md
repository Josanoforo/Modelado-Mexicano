# Nota de cierre · ACTO GEN2-VALIDACION-Y-2027-1

28/sep/2026 · CAJA (`ENTORNO-DERIVADO = CAJA`, corpus montado, 515 archivos examinados, red 200) · una sesión (receptora). No se lanzó ninguna reconstructora porque ningún paquete pasó el gate de acceso. Base `9d2550b9` = SHA de redacción · 0-bis `f926d95c` · ADR `ADR-260928-GEN2-VALIDACION-Y-2027-1-f926-01`.

**Contadores movidos: cero.** `resultados_con_validacion_independiente` sin cambio (0 asientos). celdas_validadas 219 → 219. No se adopta nada, no se abre ninguna ola, ningún sello cambia.

## P1 · Validación ciega continua
- **Universo (EJECUTADO).** RESULT del catálogo v1.3 cuya llave no está en v1.2: **20 518 en 14 CALC**, con 0 filas en `validaciones-independientes.tsv` por `resultado_id`. Comando: `python3 forense/validacion-independiente/validacion-continua-1/gates.py --verifica` → `universo=20518 con_fila_ciega=0 ids_sin_fila_ni_razon=0`.
- **Gates (tabla `gates-v1_3.tsv`).**
  - CONTRATO-FIRMADO: SÍ (R31).
  - CONTEXTO-NUEVO-ACREDITADO: SÍ por receta (R32, opción A).
  - APTO-TECNICAMENTE: PARCIAL. Las 14 specs humanas existen y su sha casa; el contenedor y la allowlist se construyen tras el acceso.
  - **ACCESO-AUTORIZADO: NO en los 14.** Sobre 647 filas de `firmas-pendientes.tsv`, solo `0c1f-02` concede «Acceso C1», y nombra ENBIARE, ENCODAT, ENCUCI y ENIGH. Control positivo: la misma búsqueda encuentra `0c1f-02` para esos tres.
- **Resultado.** 14/14 paquetes `NO-LANZADO (gate ACCESO)`. Razón por id: `SIN-VALIDACION-CIEGA`. Cero dictámenes, cero specs insuficientes nuevas (no hubo recálculo que las revele) y cero lecturas de sellados.
- **Criterio de una semana.** Ninguna cifra queda sin validación ciega ni razón declarada: la razón es el gate, que abre mesa (hoja §1).

## P2 · Lote 4 (ENIF / ENUT / ENSANUT 2024)
Re-verificado de estado (A.17). `FP-260926-GEN2-ASTRA6-C1-PAQUETES-2-9c9e-01` (R13 (1)) difiere los permisos «por textos separados», y ninguno se ha firmado. R06 mantiene ENIF 2024 m7 RESERVADA. Los tres paquetes (ENIF 2024 99 RESULT en 7 CALC, 7 de ellos ya en el libro · ENUT 2024 1 · ENSANUT 2024 169) quedan `NO-LANZADO (gate ACCESO)`. El texto de firma que abriría cada uno está en `lote4-gates.tsv`. No se abrió nada.

## P3 · Frente 2027
- **Expediente** `forense/analisis/familias-2027/EXPEDIENTE-v1_2.md` + `familias-2027-estado-v1_2.tsv`: 8 filas · LISTA 5 · NO-LANZAR-TODAVIA 2 · SUSPENDIDA 1 (PAGO-DIGITAL, se dice y no se reactiva).
- **Cinco de C2 re-verificadas.** spec 16/16 CASA, archivos del sello 43/43 COINCIDE, potencia existe, emisiones sin diff. La fila en vista queda NO-VERIFICABLE-AQUÍ porque la vista va por trozos y el control positivo también falta.
- **ENOE-INFORMALIDAD y ENSU-CAMPECHE: PARO-PREMISA** (toca una firma de mesa). El encargo supone «contrato firmado (R27 (2))»; el texto verbatim de R27 (2) deja ENOE en NO-LANZAR-TODAVIA y pide firma propia para cualquier regla nueva, y ENSU-Campeche solo tiene `71cf-01` («recibir sin adoptar»). Sin COMMIT-1 ni emisión: congelarlas habría fijado un contrato no firmado (§7 d). Hoja §3.
- **Manifiesto de sellos** `forense/sellos/manifiesto-sellos-2026-09-28.tsv` (`python3 tools/sello_externo.py manifiesto --escribe --fecha 2026-09-28`): 578 filas, sha256-manifiesto (cuerpo, pie del TSV) ff020b94…a6e0; sha256 del archivo 31f57ff2…0fbd, el que cubre el .ots. Está listo para el `.ots` de mesa (hoja §2, receta de un minuto).

## P4 · Conteos
- Cifras validadas a ciegas esta semana: 0 (por dictamen: SOSTENER 0 · ACOTAR 0 · PROPONER-SUSPENDER 0 · SOSTENER-SIN-CORROBORACION 0 nuevos).
- Specs insuficientes nuevas: 0.
- Familias: LISTA 5 · BLOQUEADA 2 (contrato) · SUSPENDIDA 1.
- Hoja RH: `forense/validacion-independiente/validacion-continua-1/hoja-mesa.md` (acceso P1, acceso lote 4, `.ots` y la premisa ENOE/ENSU). FP `f926-01..04`.

## Criterios de «hecho», uno por uno
| Criterio | Estado |
|---|---|
| ids sin fila ni razón = 0 | CUMPLE (comando arriba) |
| números del reconstructor antes de la comparación | NO-APLICA: no hubo reconstructor |
| transcripts archivados | NO-APLICA: no hubo reconstructor |
| ocho filas en el expediente v1.2 | CUMPLE |
| ENOE y ENSU con `sello.json` y potencia | NO CUMPLE: PARO-PREMISA (potencia sí; sello no) |
| ninguna emisión previa cambiada | CUMPLE (`git diff --stat` vacío) |
| ninguna ola reservada abierta | CUMPLE |
| `check.py --baseline` VERDE | se reporta en el PR |

## Premisas verificadas (§3 del encargo)
- `[EJECUTADO] 9d2550b9`: base = `origin/main`, 0 commits de diferencia.
- Expediente v1.1 con 8 filas: sí.
- `validaciones-independientes.tsv` con más de 490 filas: 748.
- `CONTRATO-v3.md`, `LANZAMIENTO.md` y `compare_v3` existen.
- `[SUPUESTO] settings.local.json de la reconstructora`: no se ejerció porque no hubo lanzamiento. Receta para el sucesor: `forense/validacion-independiente/catalogo-1-lote3/lanzamiento/lanza-aislado.sh`.

## Módulo de auditoría (v2.16)
Unidad por instrumento: cada paquete la hereda de su spec humana; este acto no produjo cifras. PROSPECTIVA y RETROSPECTIVA: las emisiones 2027 son PROSPECTIVAS y no hay ninguna RETROSPECTIVA nueva. Nada escrito a mano: todos los conteos salen de los comandos citados.

## Continuación · firmas de mesa en el chat del acto (28/sep/2026, verbatim)

Mensaje de mesa tras abrir el PR #1310: «Adelante, sigue corriendo el encargo, lo quiero completo, cualquier cosa de firmas o settings lo ajustamos».

La sesión preguntó así: «Tomo tu mensaje como firma de mesa del acceso C1 para los 14 paquetes de P1 (olas abiertas) y lo copio verbatim a la nota. ¿Qué hago con el lote 4 (ENIF, ENUT y ENSANUT 2024)?». Mesa no objetó la primera frase y respondió lo siguiente:

- **Lote 4 (FP f926-02):** «Opción 2, delimitada: acceso de C1 a ENIF 2024 solo en los módulos que ya tienen firma de apertura (m7 sigue reservado, R06) y a ENUT 2024 solo en los módulos abiertos por FP-bda6-02; verifica por id qué módulos son antes de armar el paquete y deja NO-LANZADO (gate ACCESO) lo que no tenga firma. ENSANUT 2024 sigue reservada: su paquete queda diferido hasta firma por escrito. Este texto es firma de mesa del 28/sep y va verbatim a la nota.»
- **`.ots` (FP f926-03):** «Lo corro yo (Recomendado)».
- **ENOE/ENSU (FP f926-04):** «1; deja lista la consulta a INEGI sobre el diseño de ENOE (C2-1 la redactó) como receta para que mesa la envíe con las solicitudes de mañana».
- **Acceso P1 (FP f926-01):** firmado por el mensaje de arriba, con la interpretación declarada en la pregunta y sin objeción de mesa. Texto por paquete: columna `firma_que_lo_abre` de `gates-v1_3.tsv`.

## Continuación · P1 ejecutado tras la firma (28/sep/2026, noche)

Los apartados P1, P2 y P4 de arriba describen el estado antes de la firma de mesa; esta sección los sucede y no los reescribe.

**Contadores movidos.** El libro `validaciones-independientes.tsv` sube de 748 a 21 266 filas (+20 518): PASA 5 718 · CONCUERDA-NO-APROBADA 14 048 · NO-PASA 752. `resultados_con_validacion_independiente` se deriva por el `[deriva]` tras el merge; el libro pasa de 199 a 5 917 filas PASA. No se adopta nada: E.2, la adopción es el merge de mesa. `celdas_validadas` no cambia (219).

**P1 · 14 paquetes (orden E.2 por paquete, commit a commit en la rama):**
1. Paquete con sha antes de entregar (`ed733a1e`).
2. Reconstructora `claude -p` aislada, lanzada por mesa desde su terminal (`cola.sh`, 3 en paralelo, 17:51–18:20). El clasificador del modo automático negó el lanzamiento desde la sesión («Create Unsafe Agents»).
3. Salida archivada y commiteada antes de abrir el sellado (`archiva.py`).
4. Auditoría del transcript, `freeze-export` y `compare_v3 freeze`; referencia desde `resultados.json`; `compare_v3 compare` (`compara_vc1.py`).
5. Dictamen y asiento con la regla de `LANZAMIENTO-VC1.md` (`asienta.py`).

Tolerancia: la sellada en cada `spec.yaml` (flotante abs 1e-10). IC diagnóstico (R23), no adjudica.

| CALC | llaves | SOSTENER | ACOTAR | PASA | CONCUERDA-NO-APROBADA | NO-PASA |
|---|---:|---:|---:|---:|---:|---:|
| CALC-CCPV-FAM-PISOS-0001 | 640 | 413 | 227 | 6 | 407 | 227 |
| CALC-EDR-SUICIDIO-PISOS-0001 | 2578 | 2578 | 0 | 2290 | 288 | 0 |
| CALC-EMAT-PAREJA-PISOS-0001 | 3304 | 3304 | 0 | 3079 | 225 | 0 |
| CALC-ENADID-COLA-2018-0001 | 100 | 100 | 0 | 94 | 6 | 0 |
| CALC-ENASEM-ESCOLARIDAD-2021-0001 | 14 | 14 | 0 | 0 | 14 | 0 |
| CALC-ENDISEG-PISOS-2021-0001 | 424 | 424 | 0 | 15 | 409 | 0 |
| CALC-ENOE-PARTICIPACION-2024T4-0001 | 136 | 136 | 0 | 2 | 134 | 0 |
| CALC-ENPECYT-CONOC-PISOS-0001 | 280 | 280 | 0 | 90 | 190 | 0 |
| CALC-ENSU-PISOS-0001 | 5445 | 5408 | 37 | 4 | 5404 | 37 |
| CALC-ENSU-SERIE-0001 | 7189 | 6701 | 488 | 0 | 6701 | 488 |
| CALC-ENVIPE-PERCEPCION-2024-0001 | 138 | 138 | 0 | 138 | 0 | 0 |
| CALC-LATINOBAROMETRO-COLA-2023-0001 | 68 | 68 | 0 | 0 | 68 | 0 |
| CALC-MMSI-PISOS-2016-0001 | 158 | 158 | 0 | 0 | 158 | 0 |
| CALC-PEW-RELIGION-2024-0001 | 44 | 44 | 0 | 0 | 44 | 0 |
| **total** | **20518** | **19766** | **752** | **5718** | **14048** | **752** |

**Lectura.**
- En 19 766 de 20 518 llaves el punto reconstruido desde la spec humana cae dentro de 1e-10 del sellado. En 5 718 de ellas coinciden también el IC y su estado: el comparador dice COINCIDE.
- Las 752 fuera tienen causa identificada, y en los dos casos es una insuficiencia de la spec (D-15), no un defecto del cálculo sellado:
  - 525 de ENSU (EDAD 60-MAS): la reconstructora incluyó el código 97 («97 o más años»), que la spec deja sin decir, y el sellado no. Es el mismo punto que firmó `c09b-01`. |Δ| ≤ 0.0045.
  - 227 de CCPV (cinco conductas con edades o atributos del jefe): la spec no fija el tratamiento de EDAD 999 / NIVACAD 99 ni el universo conjunto de «60+ y menor de 18». |Δ| ≤ 0.0065.
- Por la regla congelada se asientan como ACOTAR / NO-PASA. `specs-insuficientes-v1_3.tsv` suma 3 filas (las dos de arriba y la receta de bootstrap en código).
- **«Coinciden» solo donde el comparador dice COINCIDE** (5 718); el resto es «punto dentro de tolerancia».

**Auditoría de transcripts.**
- 14/14 SOLO-OPUS; ninguno salió a la red.
- 7 con marca automática revisada a mano y asentada en `<paq>--revision-auditoria.md`:
  - ENADID y ENOE: tokens de columna internos, con `usecols` idéntico al autorizado.
  - ENPECYT: `/d` de `sed` y un `git log` fallido, declarado como intento.
  - EDR, CCPV, EMAT y ENSU-PISOS: derivados propios en `$TMPDIR` y nombres de binario.
- **Reserva general:** la receta aísla `/tmp`, pero `$TMPDIR` de las reconstructoras resultó ser `/home/pc0/tmp/claude-1000`, en disco y compartido entre sesiones. En los 14 transcripts ninguna listó ni leyó contenido ajeno ahí; la ceguera se sostiene por la auditoría del transcript (rótulo `VC1-CIEGA-POR-CONTEXTO-NUEVO`), no por el aislamiento.

**P2 · lote 4 (firma delimitada de mesa).** Verificación por id en `lote4-modulos.tsv`:
- Ninguno de los 8 CALC de ENIF/ENUT 2024 usa m7.
- Ningún módulo que usan tiene firma de apertura por id: `9c9e-01` difiere los permisos; `bda6-02` no nombra módulos de ENUT; `2868-01` es una adopción, y su microdato es ENIF 2015–2021.
- Resultado: 8/8 NO-LANZADO (gate ACCESO). ENSANUT 2024 diferida por la firma. Nada se abrió.

**`.ots` (P3).** `manifiesto-sellos-2026-09-28.tsv.ots`, sellado con cuatro calendarios; pendiente de anclaje. Tras el anclaje: `ots upgrade`.
- El sha256 del archivo es `31f57ff2…0fbd`, y es el que cubre el `.ots`.
- `ff020b94…a6e0` es el `sha256-manifiesto` del cuerpo, escrito al pie del TSV.

**ENOE.** La solicitud a INEGI está lista para la PNT: `forense/analisis/familias-2027/solicitud-inegi-enoe-varianza-singleton.md`.

**P4 · conteos finales.**
- Cifras validadas a ciegas esta semana: 20 518 (SOSTENER 19 766 · ACOTAR 752 · SOSTENER-SIN-CORROBORACION 0 · PROPONER-SUSPENDER 0).
- Specs insuficientes nuevas: 3.
- Familias: LISTA 5 · BLOQUEADA 2 · SUSPENDIDA 1.
