**CONSUMIDO** — `ADR-139` (`canon/gobernanza-v1_15.md`), `ACTO LANDING-EMISOR-M1`, 21/ago/2026. Ejecutado: §1 (los cuatro adjuntos de código/test/tsv, hashes verificados exactos), §2 (las tres salidas crudas coinciden con lo esperado), §3 (ADR-139), §4 (`FP-103` FIRMADA, `FP-104` ABIERTA, tres líneas en `hallazgos.md`). Hueco declarado, no oculto: los cuatro documentos de sesión de §1 (diseño/benchmark/nota) no llegaron adjuntos a este acto y no se archivaron — ver `ADR-138(c)`. **Renumerado desde el candidato original `ADR-137`/`FP-99`/`FP-100`:** `main` fusionó `PR #306`/`ACTO REPARA-T22` mientras este PR seguía abierto, y esos números ya quedaron ocupados con contenido distinto — regla de la casa, quien fusiona segundo renumera.

# ENCARGO · LANDING-EMISOR-M1 — aterrizar el código del emisor del corredor M
**Entorno asignado: NUBE (repo-only). NO lanzar en Ubuntu. Modelo: Opus. Redactado por la sesión EMISOR-M (dirección, Fable) el 20/ago/2026 contra `origin/main = 8b73aee`; si main se movió, NO es PARO — refresca y re-deriva. Gate ya cumplido: firma de mesa Q1-bis (abajo, verbatim).**

## 0 · ARRANQUE (Bloque D) — las cinco líneas, y no empieces sin ellas
1 REPO: clon existente; ruta · `git log -1` · `git status`. 2 SHA vs `8b73aee`. 3 `data/raw`: AUSENTE NO ES PARO (este acto no lo toca). 4 ENTORNO: variable + sonda — este acto no toca microdato ni red de datos: dilo y salta. 5 ESPEJO: ninguna cifra de él.
**VERIFICACIÓN DE EXISTENCIA (A.8), contestada por quien escribe:** (1) estructura: `milpa/src/` + `tests/` + `forense/`, gobernadas por suite `tests/check.py` y baseline — derivado del árbol, no de memoria. (2) contenido: `ls milpa/src/emisor.py tests/aceptacion_r3_4.py tests/test_emisor_fidelidad.py forense/crosswalk-pregunta-regla-v1_0.tsv` contra `8b73aee` → **NO-ENCONTRADO los cuatro** (universo: árbol completo, 20/ago; premisa cero verificada con 123 `.py`/0 hits en la nota de premisas adjunta). (3) cobertura retroactiva: n/a — archivos nuevos.

## 1 · Adjuntos y verificación (PARO real si un hash no coincide tras revisar A.7)
Coloca los cuatro adjuntos EXACTAMENTE en estas rutas y verifica sha256:
```
d2abaff8c473180c42d61b2ead4748ec920d7a599fc26e479330271aa4468f68  milpa/src/emisor.py
4d4ef9388c61d460024c1730c73fa82f3395907f2c843a6b0be83ef2d0567287  tests/test_emisor_fidelidad.py
12d461d8a558cdd71f4bf8ea272109988bbdf676b6a1c41a53c3fc620443ac86  tests/aceptacion_r3_4.py
21a336b3a567c3fa76300302b66749f6d1c3a5bf2dbae0af0edb2b0028300f1d  forense/crosswalk-pregunta-regla-v1_0.tsv
```
Archiva además, en `forense/` (diseño/benchmark) y `forense/notas/` (nota), los cinco documentos de sesión adjuntos: `NOTA-VERIFICACION-PREMISAS…` → `forense/notas/2026-08-20-emisor-m-verificacion-premisas.md` · `DISENO-EMISOR-M-v1_0.md` · `DISENO-EMISOR-M-v1_1-DELTA.md` · `BENCHMARK-INTERVALO-CORREDOR-M-2026-08-20.md` → `forense/` con esos nombres · este encargo → `forense/encargos/2026-08-20-landing-emisor-m1.md`, marcado CONSUMIDO con el PR al cerrar (A.3).

## 2 · Corre y pega salidas crudas (criterio de cierre)
```
python3 -m pytest tests/aceptacion_r3_4.py tests/test_emisor_fidelidad.py tests/test_motor_*.py -q
python3 -m milpa.src.emisor
timeout 900 python3 tests/check.py --baseline     # 🚫 sin --freeze
```
Esperado, derivado en origen (si difiere: PARA y reporta, no ajustes): **12 passed, 1 xfailed** (el xfail ESTRICTO es la condición A — diseño, no defecto) · gate impreso `NO-ADJUDICADO — B y C computados` con H1/H2 a la vista · `LÍNEA BASE: VERDE`.

## 3 · ADR (siguiente libre; renumera al escribir Y al fusionar) — puntos obligatorios
(a) Firmas de mesa verbatim, 20/ago/2026, capturadas por widget en la sesión EMISOR-M: **Q1 → "benchmark web"** · **Q2 → "Las reglas en prosa nos mete en problemas encuentra otra solución"** · **Q1-bis → "Sí — sella y lanza EMISOR-M-1"**. (b) Q1 resuelta por `BENCHMARK-INTERValo…` (síntesis: punto + clase-como-confianza + intervalo solo con EE real + producto CAL-ASIGNADO al piloto + bandas v2 derivadas estilo ecoinvent, pre-registradas con falsador). (c) Q2 resuelta por arquitectura sin prosa (delta v1.1): el emisor consume SOLO tramite.yaml + procedencia.yaml + Registro §7 parseado; lo solo-en-prosa = NO-EMITE; promoción prosa→máquina = mecanismo ordinario del canon, nunca del piloto; ADR-68(a) sin ambigüedad — nada se edita ni compila. (d) Estado del gate: B colapso 100% ✔ · C reducción 0% ✔ con trivialidad DECLARADA (enlace índice→adopción h_r = OLA futura) · A NO-ADJUDICADA con **H1** (comparador retail-efectivo NO-EMITE en capa máquina; universo: tramite+procedencia, 20/ago) y **H2** (spec §10.1 dice OXXO Pay; Registro §7 enuncia SPEI — cuál rige es de mesa) · diagnóstico pareja-SPEI 0.09/0.71 = **12.7% ≥ 10%** (no adjudica; si mesa firma pareja, A falla numéricamente y la vía es la calibración contra series SPEI que `nota_calibracion` ya declara). (e) Crosswalk pasada 1: **60 filas · 10 CANDIDATO-EMITE · 50 NO-EMITE** — insumo formal de la saturación del marco (FP-82). (f) Este acto NO mueve Hito D: mover 13/27 exige además FICHA-R3.4 (hitoD Nota 2/Nota 3, acto hermano) y la resolución de H1/H2.

## 4 · Tablero (`forense/firmas-pendientes.tsv`, mismo commit)
- Fila nueva **FIRMADA**: Q1-bis (síntesis benchmark + arquitectura sin prosa + CAL-ASIGNADO al piloto), cita verbatim y ADR de (3).
- Fila nueva **ABIERTA**: "Comparador de la condición A de R3.4 — H1/H2: ¿rige pareja-SPEI (A falla 12.7%≥10% → vía calibración series SPEI) o retail-OXXO (exige UN acto de promoción prosa→máquina)? Firma de mesa."
- `forense/hallazgos.md`: una línea por (i) 50/60 NO-EMITE del crosswalk → FP-82; (ii) C trivial declarado, h_r OLA futura; (iii) cifra del transfer refutada (10 p's, no 11) y conjuntos 49-reglas ≠ 49-refutaciones — ya documentados en la nota de premisas.

## 5 · Perímetro y concurrencia
Toca SOLO: los 4 archivos de §1, los 5 documentos archivados, `forense/encargos/…landing-emisor-m1.md`, ADR en gobernanza, tablero, hallazgos. En paralelo pueden correr actos de la lane ADV1-M5/⊕/FP-91 (mesa-pendientes) — cero intersección de archivos. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."
**Contador de este acto:** R3.4 corrible (harness verde: 12+1xfail) con huecos nombrados · medición sobre México: 0, dicho.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-20-landing-emisor-m1.md" canon/gobernanza-v1_15.md` → 1: citado bajo ADR-138 en canon/gobernanza-v1_15.md, con lenguaje de ejecución (archivado/ejecutado) en el bloque correspondiente. Marca ausente en el archivo era defecto de trámite, no evidencia de no-ejecución.
