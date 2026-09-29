# Nota de cierre · GEN2-TUBERIA-TABLERO-UNICO-1

ACTO GEN2-TUBERIA-TABLERO-UNICO-1 · 29/sep/2026 · NUBE · AUTÓNOMO-AMPLIO · encargo `forense/encargos/2026-09-29-GEN2-TUBERIA-TABLERO-UNICO-1.md` (sello de cuerpo `7654e498…a160`) con `…-ADENDA-1.md` (sello `53219638…1625b`, archivada como archivo propio). ADR `ADR-260929-GEN2-TUBERIA-TABLERO-UNICO-1-22ee-01`. celdas_validadas: 219 → 219 (Δ0). Contadores que movió: el semáforo y las siguientes acciones de los carriles (efecto buscado); lecturas, adopciones y `no_corrido_abiertas` solo por la NC propia (+1).

## 1 · Premisas y adjuntos
- Los tres adjuntos no llegaron con el encargo; llegaron después, con la adenda. Sus sha256 se recalcularon al recibirlos y coinciden con los de la adenda (completos en `forense/encargos/2026-09-29-GEN2-TUBERIA-TABLERO-UNICO-1-adjuntos/SHA256SUMS`): `TABLERO-PROGRAMA.md` `9d976c05fda3266a9414a57e7d8c09c3b2d40355d38cbd12a0d98872faaab0e7`, `tablero_unico.py` `991771c2eb6afc110845886c943c69b882f45d9fa9f8c530e2611953b9ce9935`, `tablero_vista.py` `f0865da914c6af3c6d76917c4d7b280d41e00bec038ef5cd6db48622f791a53e`. Archivados con sufijo `.adjunto` para no colisionar con T02.
- Firma de mesa 5-bis (b): dada en chat verbatim («Firmo la opción (b): el cuerpo curado del tablero es el del puesto, entra por /tramite como adjunto y CI solo reescribe los bloques entre marcadores.»). Se implementó: el cuerpo de `TABLERO-PROGRAMA.md` es el del adjunto v2.24.
- «Ya hecho» (búsqueda por objeto): PR abiertos con `TABLERO-UNICO`: 0 (búsqueda de GitHub); ramas remotas con ese rótulo: 0; `forense/encargos/*TABLERO-UNICO*`: solo este acto. No había trabajo previo.
- `tablero_unico.py` del adjunto se tomó como referencia, no como código: depende de JSON «previo» y de rutas del puesto (`/home/claude/…`); `tools/tablero_unico.py` es nuevo y determinista.

## 2 · Criterios de «hecho»
1. **Un tablero, dos bloques.** `grep -c -x '<!-- TABLERO-UNICO:CARRILES:BEGIN -->'` = 1 y lo mismo para `PENDIENTES` en `TABLERO-PROGRAMA.md`. Idempotencia: `tablero_programa.py --actualiza --permitir-rama` corrido dos veces; md5 de `TABLERO-PROGRAMA.md` y `docs/tablero.md` idénticos tras la segunda (`md5sum -c`: OK/OK). Reserva: se corrió con `--permitir-rama` (bloque rotulado NO-ES-ORIGIN-MAIN); el canal lo regenera sobre origin/main.
2. **Ningún otro tablero con cifras.** `TABLERO-CARRILES.md` y `docs/tablero-carriles.html` retirados (0 coincidencias de `TABLERO-DERIVADO` porque no existen). Enlaces a otro tablero en `canon/`, `docs/`, `README.md` (excluye L0/gobernanza): `grep -rIn "](.*\(TABLERO-CARRILES\|tablero-carriles\)"` = 0. `README.md` y `docs/index.md` apuntan al tablero del programa. Consumidor no previsto en §3: `tests/test_tablero_carriles.py` (usaba el HTML) — ajustado.
3. **Carriles con lo vigente.** `tests/test_tablero_carriles.py::prueba_vigentes` (huérfano ya cableado) afirma sobre `tablero_carriles.py --json`: F2 = catálogo del puntero (v1_4); F1, F3, F11 = versión más alta; `c6aa-01` no es stopper ni siguiente acción; `43d6-01` frena CARRIL-03 y CARRIL-18. Pasa; con la regla de aparato desactivada falla y reproduce los 7 carriles de `c6aa-01` de dirección (03, 08, 09, 12, 15, 19, 26).
4. **Validación independiente reconciliada.** `corrida0.py status` da `resultados_con_validacion_independiente=5933`; el libro tiene 5933 asientos PASA (5933 resultados distintos): iguales. Se añadieron 16 filas al libro (tabla en §4).
5. **Firma `3c2e-01`: NO cumplido.** Ver §5.

## 3 · P2 y P3 (reglas)
- P2: `_serie_alta()` y `_catalogo_vigente()` en `tools/tablero_carriles.py`; F1, F3, F5, F9, F11, F12, F15 por serie más alta, F2 por puntero. Sin cambio de esquema (las columnas nuevas no se leen). `CROSSWALK` (F14) conserva su nombre porque es la salida propia de la herramienta; `canon/crosswalk-carriles-v1_0.tsv` se regeneró (D-21: su test compara byte a byte). Simulado por el puesto: ROJO 4 · AMARILLO 23 · VERDE 1 · GRIS 3; re-derivado aquí: idéntico.
- P3: `firma_de_aparato(x)`: una FP no es stopper si el basename de su encargo contiene `-TUBERIA-` o su `qué_se_firma` cita `tools/`, `tests/`, `gobierno/`, `.github/`, «regla del semáforo» o `tablero_(carriles|programa)`. Regla del ejecutor (latitud). Gate D-14: el defecto real es `c6aa-01`; a un lector le costaba leer que firmar una regla del tablero mide Rural Indígena.

## 4 · P4 · los 16 (SUPUESTO del encargo: se sostiene)
Cada uno ya tenía `validacion_independiente=PASA` en `data/corrida0/decisiones.tsv` (ACTO GEN2-VALIDACION-INDEPENDIENTE-2, mesa/Opus 15/sep/2026), con ref a un control en `forense/prereg-caja/validacion-independiente-caja2/` y su alcance; no tenían asiento en el libro. Se asentaron con el sha256 del control. LEÍDO, no re-ejecutado: no corrí los controles y no afirmo que reproduzcan; el PASA es el de aquel acto.

| resultado | spec | alcance | dictamen |
|---|---|---|---|
| `RESULT-EDER-ACT-A-P` | `CALC-EDER-0002` | PUNTO-PRIMARIO-Y-FUNNEL-COMPLETO | ASENTADO (PASA; `2f5181656d84…`) |
| `RESULT-EDER-ACT-B-P` | `CALC-EDER-0002` | PUNTO-SENSIBILIDAD | ASENTADO (PASA; `2f5181656d84…`) |
| `RESULT-ENCIG23-MOR-B-P-DIG-SD` | `CALC-ENCIG-2023-0001-v1_1` | PUNTO-PRIMARIO-DIGITAL | ASENTADO (PASA; `b8f8871fdc7c…`) |
| `RESULT-ENCIG23-MOR-B-P-PRE-SD` | `CALC-ENCIG-2023-0001-v1_1` | PUNTO-PRIMARIO-PRESENCIAL | ASENTADO (PASA; `b8f8871fdc7c…`) |
| `RESULT-ENCIG23-MOR-B-VEREDICTO-CANAL` | `CALC-ENCIG-2023-0001-v1_1` | VEREDICTO-CANAL | ASENTADO (PASA; `b8f8871fdc7c…`) |
| `RESULT-ENCIG23-MOR-H1-VEREDICTO` | `CALC-ENCIG-2023-0001-v1_1` | VEREDICTO-HIPOTESIS | ASENTADO (PASA; `b8f8871fdc7c…`) |
| `RESULT-ENIF-COB-C-VEREDICTO-0-668937` | `CALC-ENIF-0003` | VEREDICTO-NEGATIVO | ASENTADO (PASA; `26d57f095282…`) |
| `RESULT-ENIF-COB-C-VEREDICTO-66-89` | `CALC-ENIF-0003` | VEREDICTO-LOCALIZACION | ASENTADO (PASA; `26d57f095282…`) |
| `RESULT-ENIF-COB-C-VEREDICTO-H1` | `CALC-ENIF-0003` | VEREDICTO-HIPOTESIS | ASENTADO (PASA; `26d57f095282…`) |
| `RESULT-ENIF-COB-D-P-NINGUNA-VIA-EN-1` | `CALC-ENIF-0003` | COTA-P4-DOMINIO-1 | ASENTADO (PASA; `26d57f095282…`) |
| `RESULT-ENIF-COB-D-P-NINGUNA-VIA-EN-2` | `CALC-ENIF-0003` | COTA-P4-DOMINIO-2 | ASENTADO (PASA; `26d57f095282…`) |
| `RESULT-ENVIPE-U4-12-V11-IC-HI-TAYLOR-C2-U4` | `CALC-ENVIPE-U4-2012-v1_1` | IC-NOVEL-TAYLOR-HI | ASENTADO (PASA; `d696fdb74da6…`) |
| `RESULT-ENVIPE-U4-12-V11-IC-LO-TAYLOR-C2-U4` | `CALC-ENVIPE-U4-2012-v1_1` | IC-NOVEL-TAYLOR-LO | ASENTADO (PASA; `d696fdb74da6…`) |
| `RESULT-ENVIPE-U4-12-V11-N-ESTRATOS` | `CALC-ENVIPE-U4-2012-v1_1` | DISENO-NOVEL-ESTRATOS | ASENTADO (PASA; `d696fdb74da6…`) |
| `RESULT-ENVIPE-U4-12-V11-N-ESTRATOS-UPM-UNICA` | `CALC-ENVIPE-U4-2012-v1_1` | DISENO-NOVEL-UPM-UNICA | ASENTADO (PASA; `d696fdb74da6…`) |
| `RESULT-ENVIPE-U4-12-V11-N-UPM` | `CALC-ENVIPE-U4-2012-v1_1` | DISENO-NOVEL-UPM | ASENTADO (PASA; `d696fdb74da6…`) |

## 5 · P5 · `3c2e-01` sin asiento (DECISIÓN-DE-MESA-PENDIENTE)
Verificado: PR #1337 fusionado 29/sep 09:50 −06:00 (`9a9fde23`); `canon/catalogo-del-mexicano-v1_4.tsv` tiene 36 instrumentos y 65 480 filas en `a05b128b` (primera versión) y los mismos en `9a9fde23`; instrumentos retirados: ninguno. El asiento en `forense/firmas-pendientes.tsv` fue bloqueado dos veces por el control de permisos de la sesión y no se buscó otra vía. Queda NC `…-22ee-01`. Texto de asiento listo: estado FIRMADA; firmada_en «29/sep/2026, INTERPRETACIÓN-DECLARADA (A.12): la propia fila dice que el merge del PR es la adopción (E.2); PR #1337 fusionado 29/sep 09:50 −06:00; sin retiros (36 instrumentos, 65480 filas en a05b128b y en 9a9fde23)»; ejecutada_en `ADR-260929-GEN2-TUBERIA-TABLERO-UNICO-1-22ee-01`.

## 6 · Cierre
Suite completa no corrida desde NUBE (encargo). `python3 tests/check.py --rapido`: 0 FAIL. Arreglos de cierre (D-21): T02 (nombres de los adjuntos) y T25 (la letra «E·1» de la hoja NC-DECISIONES-1, citada en el tablero; `docs/tablero.md` y `TABLERO-PROGRAMA.md` en `_T25_ARCHIVOS_CONOCIDOS`). Hallazgos en `forense/hallazgos.md`.
