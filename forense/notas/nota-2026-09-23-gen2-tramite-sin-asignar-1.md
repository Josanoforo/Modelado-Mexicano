# Nota de cierre · ACTO GEN2-TRAMITE-SIN-ASIGNAR-1

Objetivo: que ninguna NC ABIERTA tenga `sucesor = SIN-ASIGNAR`. Verificación
de "hecho":

```
awk -F'\t' 'NR>1 && $10 ~ /ABIERTA/ && $9 ~ /SIN-ASIGNAR/' forense/no-corrido.tsv | wc -l
```
→ `0` (antes: `43`).

Ruteo aplicado: dinero → PRODUCTO-DINERO · CI/vistas/`corrida0`/`check.py`/`verify.yml` →
TUBERIA · adquisición/nube → NUBE-MEDICIÓN · gobierno/marcador/informe/perímetro/A.3 →
DIRECCION · lo que no se rutea por objeto (decisión de mesa, permiso explícito, texto
que solo mesa tiene, o «si mesa quiere X») → MESA, con la pregunta en una línea · lo ya
resuelto por su propia spec → CERRADA con cita.

## P1 · Tabla de ruteo

| NC | objeto | regla aplicada | sucesor |
|---|---|---|---|
| NC-0159 | roster UPM / varianza oficial ENVIPE R | sin conversación; requiere decisión de mesa (texto ya dice "Titular de mesa") | MESA |
| NC-0247 | re-verificación de 6 filas de deuda (NC-0012/0024/0026/0213/0230/0233) | gobierno de la deuda del programa | DIRECCION |
| NC-0280 | cómo dirección calcula el perímetro de un acto que archiva adjuntos verbatim | gobierno/perímetro | DIRECCION |
| NC-0285 | encargo del PR #831 no archivado en forense/encargos/ | gobierno/A.3 | DIRECCION |
| NC-0290 | cuarta condición del bin 1 de la regla de adopción en bloque | gobierno; el texto ya dice "Dirección" | DIRECCION |
| NC-0298 | `tools/corrida0.py` lee `escala` por regla, no por conducta | corrida0 | TUBERIA |
| NC-0299 | citas `origen:` del emisor GEN1 desfasadas por rango de línea | decisión de mesa sobre si el emisor admite corrección | MESA |
| NC-0305 | vocabulario celda-D v0.6, falta enum `estrategia: persistencia` | requiere abrir versión nueva del vocabulario; decisión de mesa | MESA |
| NC-0307 | regla de extracción de intervalo de L, pre-registro antes de ver capturas | requiere acto nuevo pre-registrado; decisión de mesa | MESA |
| NC-0308 | disciplina E.5 (congelar spec antes de microdato) incumplida en v1_2 | gobierno/proceso | DIRECCION |
| NC-0313 | falsador de orden para RESULT tipo snapshot | diseño de medición nuevo; decisión de mesa | MESA |
| NC-0348 | ramas `claude/*` vivas no nombradas por el encargo | pregunta explícita a mesa en el texto | MESA |
| NC-0374 | núcleo común ENUT 2019/2024 como estimando nuevo | el texto ya dice "si mesa quiere" | MESA |
| NC-0375 | mismo objeto que NC-0374 | depende de la misma decisión | MESA |
| NC-0381 | cablear `tests/test_c2_ic_enif2024_guardia.py` en `.github/workflows/verify.yml` | CI/verify.yml | TUBERIA |
| NC-0382 | guardia en `tools/cierre_acto.py` que exija `registro --escribe --lote` | vistas/`corrida0` | TUBERIA |
| NC-0383 | `tools/marcador_segmento.py` no toma el IC del CALC sellado | marcador | DIRECCION |
| NC-0385 | error de persistencia de 6 celdas ENIF2021 (CALC nuevo, ver FP-396) | estimando nuevo; decisión de mesa | MESA |
| NC-0396 | `tests/test_adq_descubrimiento.py` FALLA-DE-VERDAD, en SKIP de `guardias` | CI | TUBERIA |
| NC-0398 | `tests/test_censo_derivado.py` FALLA-DE-VERDAD | CI | TUBERIA |
| NC-0399 | `tests/test_cierre_acto.py` FALLA-DE-VERDAD | CI | TUBERIA |
| NC-0400 | `tests/test_consulta_gen2.py` FALLA-DE-VERDAD | CI | TUBERIA |
| NC-0401 | `tests/test_motor_gen2_explicito.py` FALLA-DE-VERDAD | CI | TUBERIA |
| NC-0403 | `tests/test_relevo_encuci_f2.py` TIMEOUT sin diagnosticar | CI | TUBERIA |
| NC-0445 | `p` de tramite.evade/cuidado vs RESULT sellado + `ola_calibracion` faltante | fuera del perímetro de MOTOR-LINAJE-1; decisión de mesa | MESA |
| NC-0446 | dueño de `forense/ejemplos/GEN2-*` para re-sellar respuestas de ejemplo | decisión de mesa | MESA |
| NC-0449 | piloto de crédito, sucesor 2 de DIN-CREDITO-PISOS-ENIF2021-1 §10 | dinero/crédito | PRODUCTO-DINERO |
| NC-0450 | `tests/test_relevo_remesas_f3.py` vs veredicto de #942 (remesas) | dinero/remesas | PRODUCTO-DINERO |
| NC-...THETA-CONGELADA-1-e8fa-01 | `motor.py:20,:129` citan BARRIDO-2 en vez de ADR-531 | requiere permiso explícito de mesa (PARO c) | MESA |
| NC-...THETA-CONGELADA-1-e8fa-02 | `commit_declaracion` de ADR-68 para catálogo/motor | decisión de mesa | MESA |
| NC-...SIDECAR-CUERPO-1-3d08-01 | cita rota del sidecar del insumo codex `pisos-enif2021-0002` | insumo externo, solo el dueño lo re-sella; decisión de mesa | MESA |
| NC-...SIDECAR-CUERPO-1-3d08-02 | texto de adendas del 19–21/sep que el repo no guarda | solo mesa tiene el texto | MESA |
| NC-...MARCADOR-E-INFORME-1-48d4-01 | re-sellar `snapshot-M-gen2-explicito-v1_2.json` al universo vigente | MOTOR; decisión de mesa | MESA |
| NC-...MARCADOR-E-INFORME-1-48d4-03 | 3 candidatos SIN-IC-EN-NINGUNA-CELDA | gobierno/informe/disciplina de spec | DIRECCION |
| NC-...MARCADOR-E-INFORME-1-48d4-04 | cobertura con réplicas de bootstrap (CAJA, no Wilson) | requiere acto en CAJA; decisión de mesa | MESA |
| NC-...DIN-LOTE-ENIF2024-A-a98a-04 | sha256 declarado del Anexo A no coincide (canal de chat renormalizó tabuladores) | solo mesa tiene el original byte a byte | MESA |
| NC-...DUELO-ENVIPE2026-COMMIT-1-8796-02 | `S1`/`MAE(C2)` NO-VERIFICABLE-AQUÍ a 1e-10 | el propio texto: "no requiere acto: atribuido y declarado en la spec §9" | **CERRADA** (cita: spec GEN2-DUELO-ENVIPE2026-COMMIT-1 §9 + hallazgos.md) |
| NC-...TUBERIA-ENRUTAMIENTO-PR-1-9a2c-01 | `/revisa` lea la clase del resumen en vez de deducirla | TUBERIA (comando `/revisa`), condicionado a evidencia de uso | TUBERIA |
| NC-...TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-02 | registro de tests en `tests/check.py`, lista única en conflicto (19.4% de PR) | TUBERIA | TUBERIA |
| NC-...TRAMITE-FIRMAS-5-958c-02 | re-sello de FP-374, fila FP-...-958c-01 sin dueño | gobierno/firmas | DIRECCION |
| NC-...PENDIENTES-RECONCILIA-1-38c3-01 | revisión individual de las 41 filas de §2.9 | gobierno; el texto ya dice "dirección al revisar clasificacion.tsv" | DIRECCION |
| NC-...PENDIENTES-RECONCILIA-1-38c3-02 | patrón DECISION-DE-MESA-PENDIENTE superada, sobre las 62 filas DE-MESA | gobierno; alternativa nombrada es "dirección o GEN2-TRAMITE-FIRMAS-6" | DIRECCION |
| NC-...DIN-CREDITO-PISOS-1870-RUN-1-009f-02 | revert `344739d1` dejó la vista 18 corridas atrás | gobierno; el texto ya dice "dirección redacta el encargo" | DIRECCION |

Conteo por sucesor: MESA 20 · DIRECCION 13 · TUBERIA 9 · PRODUCTO-DINERO 2 ·
CERRADA 1 (= 45 filas contadas con las 2 de NC-0374/0375 que comparten
objeto; 43 NC en total).

## P2 · Enmiendas

Las 43 filas se editan directamente en `forense/no-corrido.tsv` (columnas
`sucesor` y `estado`, línea por línea, sin tocar el texto de la fila ni
ningún otro campo); NC-...-DUELO-ENVIPE2026-COMMIT-1-8796-02 pasa de
`ABIERTA` a `CERRADA` con la cita anotada en el propio campo `estado`
(perímetro de este acto no incluye editar `cerrado_por`/`fecha_cierre`).

## P3 · Lista de mesa (RH)

Veinte filas requieren una decisión que solo mesa puede tomar. Se agrupan
por tipo de pregunta:

**Titularidad / permiso para tocar código vedado (4):**
- NC-0159 — ¿designa mesa un titular para el roster de UPM / servicio de varianza ENVIPE R?
- NC-0299 — ¿el emisor GEN1 admite corrección de sus 11 citas `origen:` por id?
- NC-...THETA-CONGELADA-1-e8fa-01 — ¿autoriza mesa tocar `motor.py:20,:129`?
- NC-...MARCADOR-E-INFORME-1-48d4-01 — ¿se encarga a MOTOR re-sellar el snapshot?

**Abrir un estimando/vocabulario nuevo (5):**
- NC-0305 — ¿vocabulario celda-D v0.6 con `estrategia: persistencia`?
- NC-0307 — ¿pre-registro de regla de extracción de intervalos de L?
- NC-0313 — ¿falsador de orden nuevo para RESULT tipo snapshot?
- NC-0374 / NC-0375 — ¿núcleo común ENUT 2019/2024 como estimando nuevo?
- NC-0385 — ¿CALC-PISO-PERSISTENCIA-ERROR-0002 para 6 celdas ENIF2021?

**Texto o artefacto que solo mesa tiene (3):**
- NC-...SIDECAR-CUERPO-1-3d08-01 — ¿quién re-recibe/re-sella el insumo codex `pisos-enif2021-0002`?
- NC-...SIDECAR-CUERPO-1-3d08-02 — texto de las adendas del 19–21/sep, ¿lo aporta mesa?
- NC-...DIN-LOTE-ENIF2024-A-a98a-04 — ¿mesa conserva el Anexo A byte a byte en otro sitio?

**Decisión ajena/pendiente ya etiquetada (4):**
- NC-0348 — ¿siguen en uso `claude/fervent-johnson-m47pdg` y `claude/practical-turing-kbqc08`?
- NC-0445 — ¿quién resuelve el `p` desalineado y la `ola_calibracion` de `tramite.evasion_norma`?
- NC-0446 — ¿quién es dueño de `forense/ejemplos/GEN2-*`?
- NC-...THETA-CONGELADA-1-e8fa-02 — ¿quién resuelve `commit_declaracion` de ADR-68?

**Acto de caja / medición pendiente (1):**
- NC-...MARCADOR-E-INFORME-1-48d4-04 — ¿acto en CAJA para cobertura con réplicas de bootstrap?

Recomendación: agrupar estas 20 en una sola ronda de firma (patrón
GEN2-TRAMITE-FIRMAS), no una firma por fila — la mayoría son SÍ/NO de una
línea sobre trabajo ya acotado en el propio texto de la NC.

## No aplica

Ninguna premisa cayó: la única SUPUESTA (§0, "el objeto de cada NC basta
para rutearla sin leer el acto entero") se sostuvo para las 43 — ninguna
exigió leer el acto completo más allá del texto ya presente en
`forense/no-corrido.tsv`.
