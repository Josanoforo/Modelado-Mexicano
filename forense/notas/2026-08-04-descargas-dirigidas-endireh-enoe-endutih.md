Contadores movidos: 0.

# Encargo E (mesa #18) + Enmienda 1 — Descargas dirigidas, sin abrir contenido

## 0 · Verificación del entorno

- `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → sin declarar (no `cloud_default`).
- `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` → `200`, dos veces (antes de premisas y antes de empezar la cola).
- `data/raw` → ausente al inicio de la sesión ejecutora; creado con `mkdir -p` por Enmienda 1 (no es PARO). No se commitea (ver §3).
- `python3 tests/manifiesto.py --help` → corre, disponible.

## 1 · Premisas

| # | Verificación |
|---|---|
| PE-1 | `data/manifiesto.yaml` parseado con PyYAML en esta sesión: **193 entradas exactas**. Se sostiene. |
| PE-2 | `endireh2021_fd_pdf` ya registrado: `idBiinegi=3117` vía API `archivoscompaginacion`, `tipodocto=0`, sha256 presente (64 hex verificados). Se sostiene. |
| PE-3 | `forense/hallazgos.md` (entrada ENDIREH 4/ago) confirma `TB_VD` ("Tabla de variables derivadas") como tabla objetivo — leído el hallazgo, no el instrumento. Se sostiene. |
| PE-4 (parcial) | ENDUTIH/MOCIBA **RESPONDE 2/2** en el barrido — confirmado y re-verificado por esta sesión (ver §4). ENOE/ENNViH "siguen intactas" (no contaminadas) — confirmado: `forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md` §8 lista 9 fuentes tocadas por esa sesión y ninguna es ENOE/ENNViH. **La cláusula "son la vía al pseudo-panel de los 15 coeficientes" no se sostiene limpiamente contra la cita dada** — ver hallazgo nuevo abajo. No paró la cola porque la parte accionable (conseguir microdatos) resultó ya satisfecha, no porque la premisa se haya verificado completa. |
| PE-5 | `forense/notas/.../barrido-alcanzabilidad-27fuentes.md` §4/línea 181: ENCUP **RESPONDE (con salvedad: cadena TLS incompleta)** — coincide con "responde pero con cadena TLS no verificable". Se sostiene. |

## 2 · Hallazgos de esta sesión (proceso, no solo resultado)

1. **Discrepancia "cuatro" vs. fuentes reales de §4 del Encargo.** El Encargo dice "para cada una de las cuatro" pero la cola de §2 nombra 3 renglones que cubren **5 fuentes distintas** (ENDIREH, ENOE, ENNViH, ENDUTIH, MOCIBA). Ni 3 ni 5 es 4. No se silencia: la tabla del §4 de esta nota reporta por las **5 fuentes**, no por 4 ni por 3 renglones.
2. **Orden estricto de la cola no se respetó por esta sesión**: se trabajó ítem 1 (ENDIREH) y luego, por apuro, ítem 3 (ENDUTIH·MOCIBA) antes de verificar ítem 2 (ENOE+ENNViH). Al verificar ítem 2 después, resultó que no requería acción — pero el orden se rompió igual y se declara aquí, no se oculta.
3. **La premisa "ENOE y ENNViH son la vía al pseudo-panel de los 15 coeficientes" no está sostenida por la cita que el Encargo da (`canon/estado-programa-v1_9.md`)**: la cadena "pseudo-panel" no aparece en ese archivo. Lo que sí dice ese archivo (línea 119) es lo opuesto en un punto concreto: `unico_calibrable_hoy` se retiró por ADR-49 porque "la vía ENOE no identifica conducta financiera". `canon/glosario-v5_6.md:378` y `canon/modelo-decision-v4_0.md:384` son estructurales: "un coeficiente es una elasticidad, y el corpus es transversal — da estados, no ritmos" — ningún instrumento transversal, incluido ENOE, puede dar los 15 coeficientes hoy; el único documento que sí describe una ruta de pseudo-panel de cohortes (`forense/metodologia-identificacion-vs-ajuste-v0_1.md:120`) cita como olas candidatas ENVIPE/ENIGH/ENOE/ENIF — **no ENNViH** — y declara explícitamente "Nadie ha construido ese panel de cohortes". No se resuelve aquí (es debate metodológico de mesa, no de este acto de logística); se reporta.
4. **El punto 3 resultó no bloquear nada**, porque el ítem 2 de la cola (conseguir microdatos de ENOE+ENNViH) ya estaba satisfecho por sesiones anteriores — ver §4 fila ENOE/ENNViH.

## 3 · Declaración de durabilidad (Enmienda 1 §3, obligatoria)

**Efímera, con evidencia directa**: `data/raw` estaba ausente al iniciar esta sesión (verificado: `ls data/raw` → "No such file or directory" en el turno anterior de la misma cadena de ejecución), y este clon es un `git clone` fresco hecho minutos antes en un directorio de scratchpad de sesión. Los tres payloads que esta sesión bajó (ENDIREH microdatos, ENDUTIH, MOCIBA) viven solo en ese `data/raw` local; no hay indicio de un volumen persistente montado. Lo que perdura es lo que se commiteó: las tres entradas nuevas en `data/manifiesto.yaml` con `url_origen` real, sha256 y tamaño — cualquier sesión futura re-descarga por esa URL y verifica contra el hash. Los bytes mismos se pierden con la sesión.

## 4 · Reporte por fuente (5 fuentes, vocabulario exacto de §4)

| # | Fuente | Estado | Mecanismo que resolvió | Recurso | id de manifiesto | sha256 (truncado) | Tamaño |
|---|---|---|---|---|---|---|---|
| 1 | ENDIREH 2021 (microdatos) | **RESPONDE** | Verificado por `idBiinegi=3117` vía API `archivoscompaginacion` (ya registrado en `endireh2021_fd_pdf`); URL de microdatos confirmada contra el patrón del portal, verificada con `-r 0-0` antes de bajar completa | `.../endireh/2021/microdatos/bd_endireh_2021_csv.zip` | `endireh2021_bd_csv_zip` | `e4f1e7b1...c6037e` | 78 902 567 B |
| 2 | ENOE (panel rotativo, olas del pseudo-panel) | **RESPONDE** — ya registrado por sesiones previas, no requirió descarga nueva | N/A esta sesión — `--verifica` confirma 36/36 entradas `enoe*`/`enoen*` con sha256+tamaño ya presentes en el manifiesto (28 trimestres 2019-2026, coincide con "ENOE 28 trimestres" citado en `forense/metodologia-identificacion-vs-ajuste-v0_1.md:120`) | (36 archivos, ver manifiesto) | ids `enoe_*`/`enoen_*` (36) | — (no recalculado; `--verifica` reporta AUSENTE en disco, esperado: sesión efímera sin esos bytes) | — |
| 3 | ENNViH/MxFLS (olas del pseudo-panel) | **RESPONDE** — ya registrado por sesión previa (CAL-G3 Fase A, `forense/bitacora.md:538`), sellado, no se reabre | N/A esta sesión — `--verifica` confirma 27/28 entradas `ennvih*` con sha256+tamaño (la 28ª, `ennvih_mxfls_licencia`, es un registro de licencia sin payload por diseño) | (27 archivos, tres olas 2002/2005/2009, ver manifiesto) | ids `ennvih*` (27 con payload) | — (no recalculado; mismo motivo que ENOE) | — |
| 4 | ENDUTIH 2024 (microdatos) | **RESPONDE** | API `archivoscompaginacion`, URL ya verificada por el barrido previo, re-verificada con `-r 0-0` por esta sesión antes de bajar | `.../endutih/2024/microdatos/endutih2024_bd_dbf.zip` | `endutih2024_bd_dbf_zip` | `ef723ed1...0f0a7ab` | 8 823 853 B |
| 5 | MOCIBA 2024 (microdatos) | **RESPONDE** | API `archivoscompaginacion`, URL ya verificada por el barrido previo, re-verificada con `-r 0-0` por esta sesión antes de bajar | `.../mociba/2024/microdatos/mociba2024_bd_csv.zip` | `mociba2024_bd_csv_zip` | `105e2e26...0a7ab` (ver manifiesto, hash completo) | 1 500 882 B |

Fuera de alcance, cumplido: **ENCUP no descargada** (cadena TLS no verificable, decisión de mesa — no se usó `--insecure`). **ENSU no descargada** (fuera de alcance declarado).

## 5 · Declaración de no-apertura

No se abrió, leyó ni extrajo el contenido de ningún microdato, cuestionario, FD o diccionario en esta sesión. Los tres ZIP descargados (ENDIREH, ENDUTIH, MOCIBA) se verificaron por tamaño exacto contra `Content-Range` (sin firma de soft-404: ninguno pesa 2263 ni 13370 bytes) y por `sha256` calculado sobre el archivo completo — nunca se descomprimieron ni se abrió ningún miembro. Las tablas ya registradas (ENOE, ENNViH) no se tocaron en absoluto: solo se les corrió `--verifica`, que hashea/stat el archivo, no lo abre.

**Queda por tanto disponible para pre-registro limpio**: los tres ejes nuevos de esta sesión — `TB_VD` de ENDIREH (`exposicion_violencia`, U2 rama B), y `acceso_digital` vía ENDUTIH/MOCIBA. ENOE/ENNViH ya estaban disponibles para pre-registro limpio desde las sesiones que los registraron (esta sesión no los contaminó, no los abrió).

## 6 · Suite

Corrida después de la última edición de este documento — ver stdout adjunto al PR. `check.py --baseline` mantiene el rojo pre-existente ya declarado antes de esta sesión (no se intentó arreglar). `validador_registro_ids.py` en verde, sin cambios de esta sesión sobre `canon/`.
