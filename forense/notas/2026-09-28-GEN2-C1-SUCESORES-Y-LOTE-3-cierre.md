# Nota de cierre · ACTO GEN2-C1-SUCESORES-Y-LOTE-3

**Contadores movidos: cero PASA.** `resultados_con_validacion_independiente` 215 → 215 · `celdas_validadas` 219 → 219. Se añaden 257 asientos, todos con tolerancia citada: CONCUERDA-NO-APROBADA 253 y NO-PASA 4.

28/sep/2026 · CAJA · MODO RÍGIDO · Opus 5.5 (`claude-opus-5-5`) en la receptora y en las cuatro reconstructoras · base `3c55bfc5` (= SHA de redacción) · 0-bis `2385e777` · ADR `ADR-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-01`.

## 0 · Arranque, premisas y firmas de este chat

- **Entorno.** ENTORNO-DERIVADO = CAJA, corpus montado (515 archivos examinados), red 200.
- **Base.** `origin/main` se movió dos veces (#1289 y otros) y se fusionó en las dos. No hay duplicados del rótulo.
- **Permiso (incidencia de herramienta, no de contenido).** El clasificador del modo automático denegó dos veces escribir `FIRMAS-Y-ACCESO.md`, la hoja que viaja en el paquete, con el motivo «Instruction Poisoning». La primera vez era una hoja redactada como instrucción. La segunda, un registro en tabla. No se buscó otra vía. Mesa lo destrabó en el chat; verbatim: «Decisión: (2), regla de permiso; y si el clasificador vuelve a denegar con la regla puesta, (1) para ese paso. […] Cambia la forma del archivo, no el fondo. FIRMAS-Y-ACCESO.md no debe ser una instrucción a otro agente («debes ejecutar»): es un registro de firmas, datos que la reconstructora lee.» En el tercer intento, el registro en tabla (FP · objeto · sha256 · texto verbatim) se escribió.
- **Firma de acceso de mesa, verbatim** (28/sep/2026, chat de dirección de este acto; se asienta aquí, A.12), sobre ENCUCI 2020 y ENIGH 2022, las 2 llaves residuales: «mesa lo extiende ahora, en este chat, con el mismo régimen delimitado que ee49: olas vistas, módulos y campos del paquete, sin otra reserva. Viaja verbatim en tu nota como firma de mesa del 28/sep; las 2 llaves se lanzan, no quedan NO-LANZADO.»
- **Firma de mesa sobre el libro, verbatim:** «no sustituyas filas. Una llave con validación previa (PASA de otro acto) y una validación ciega nueva son dos validaciones, y no se colapsan: la unicidad del libro debe ser (llave, validacion_ref), no la llave sola.» Ejecutada en `dc4653ae`: `tools/corrida0.py` (6 líneas) y test en `tests/test_corrida0.py` (misma llave con misma ref sigue en PARO; con dos refs, la vista proyecta la última).
- **Premisas que cayeron.** Tocan logística o rótulo, no qué se mide:
  - **R21.** «Quince llaves ENVIPE 2015» son `RESULT-PISOS-ENVIPE2024-V2-*`: en `envipe15` el 15 cuenta llaves y no es un año (fuente `impedimentos-lote2-p2-envipe15-retiro-sucesor.tsv`, 15/15). El rótulo se corrige en la FP fb50-02 al asentarla.
  - **R25.** El retiro temporal afecta a 0 llaves: las 685 ya tienen trato en beee-02 (679 ACOTAR, 6 SUSPENDER).
  - **R33.** La «spec L51» es del `spec.yaml` del CALC. La spec sucesora es la primera de ese CALC en `prereg-caja/`.

## 1 · P2 · Ocho contratos (`forense/validacion-independiente/catalogo-1-sucesores/`)

| Firma | Qué se hizo | Evidencia derivada por comando |
|---|---|---|
| R21 | Dictámenes 2006/2016 recibidos como base de sucesores. Las 15 llaves ENVIPE pasan a RETIRADA-DEL-UNIVERSO-C1 y se proponen como PROPONER-SUSPENDER para el catálogo v1.4. | `r21-envipe-15-llaves.tsv` |
| R22 | `CONTRATO-TOLERANCIAS.md`: 1 797 identidades ENDUTIH/MOCIBA, todas proporción, con tolerancia abs 1e-8 rel 0. | `r22-tolerancias-por-identidad.tsv` |
| R23 | Protocolo como contrato diagnóstico. Los IC de las 92 y de las 312 quedan como `IC-DIAGNOSTICO-R23-NO-ADJUDICA`. El margen queda pendiente (FP 2385-01). | `dictamen-lote3-v1_1.tsv` |
| R24 | 767 ventanas literales copiadas del catálogo v1.2 (columna `reserva`), sin recalcular. | `r24-transporte-ventana-767.tsv` |
| R25 | Retiro temporal: 0 llaves. El denominador y la elegibilidad 99 quedan como contrato de los sucesores 2011/2021. | `r25-cobertura-beee02.tsv` |
| R26 | (a) aplicado a ENBIARE y (b) a las cuatro cohortes (lectura declarada). | expediente R26 |
| R28 | 130 = ENBIARE 126 + ENCIG 4. El PASA de ENCIG viene de otra validación y queda intacto. | `r28-130-no-ciegas.tsv` |
| R33 | NO-PASA formal conservado. Spec sucesora escrita con tolerancia abs 1e-10. | `prereg-caja/ENIGH2020-INTENSIDAD-REMESAS-spec-v1_1.md` |

## 2 · P1 · Las 312, a ciegas

- **Orden E.2 en git:** LANZAMIENTO con gates, paquetes con sha y la regla de dictamen/asiento (`1f089cc0`, 14:01) → números de las cuatro reconstructoras (`c2373919`, 14:11) → auditoría y congelación (`458a3440`, 14:13) → referencia desde el sellado y comparación.
- **Reconstructoras:** cuatro sesiones `claude -p` nuevas, en un namespace con `/tmp` privado, Bash sin red y solo Opus. En total 82 turnos y US$4.67. Sonda previa con control positivo (`lanzamiento-residuales/sonda-transcript.jsonl`).
- **Auditoría** (`AUDITORIA-TRANSCRIPTS-RESIDUALES.md`): 5 aciertos brutos. Cuatro son falsos positivos del patrón de rutas. El quinto es un intento real: `git log` fuera del paquete, que devolvió «not a git repository», sin contenido ni red. Queda declarado. Campos no autorizados: 0.
- **Comparación** (`compare_v3`, tol abs 1e-10):

| Paquete | Punto dentro | IC | Nota |
|---|---|---|---|
| ENCODAT 130 | 130/130 (Δ = 0 exacto) | 0/130 dentro | semilla y receta distintas por R26 (b); diagnóstico |
| ENCUCI 1 | 1/1 (Δ = 0) | referencia sin IC | ya tenía PASA de otra validación: no se añade fila |
| ENIGH 1 | 1/1 (Δ = 0) | referencia sin IC | NO-HECHA → CONCUERDA-NO-APROBADA |
| ENBIARE 126 | 56 dentro · 4 fuera · 66 sin punto | 0 dentro | 4 CESD-7 fuera: R26 (a) excluye EDAD = 98 de CESD-7 (cambio de estimando firmado). Los 66 sin punto son D-15 |
| ENBIARE 54 | diagnóstico | — | 30 identidades sucesoras `--R26A` y 24 sin punto por D-15 |

- **D-15, hallazgo nuevo** (`specs-insuficientes-v1_2.tsv`, +1). En seis escalas 0–10 (satisfacción, Cantril, cuatro de confianza; 90 llaves), el esquema y la llave dicen `proporcion` y la spec dice media. La reconstructora no adivinó.
- **Dictamen** (`dictamen-lote3-v1_1.tsv`, 404 filas): SOSTENER 278 · ACOTAR 6 · SOSTENER-SIN-CORROBORACION 120. «Coinciden» no se escribe: `compare_v3` dice DISCREPA por el IC en toda fila con IC.

## 3 · Módulo de auditoría (v2.16)

- **¿Cuántos contadores movió?** Ninguno pasa a PASA. Se añaden asientos: 253 CONCUERDA-NO-APROBADA y 4 NO-PASA.
- **¿PROSPECTIVA o RETROSPECTIVA?** Todo es RETROSPECTIVO: reconstrucción de cifras ya selladas en olas vistas.
- **¿Qué unidad tiene cada cifra?**
  - ENBIARE: persona elegida de 18 años o más.
  - ENCODAT: persona de 12 a 65 años (adolescentes 12–17 en su eje).
  - ENCUCI: persona seleccionada de 15 años o más, en zona rural.
  - ENIGH: hogar.
  - Ninguna se promedia con otra.
- **¿En qué escala está cada cantidad?** Proporciones en 0–1. Δ contra 1e-10. Las escalas 0–10 no se estimaron (D-15).
- **¿Qué sería peligroso leído simplista?**
  - «ENCODAT 130/130» dice que dos implementaciones de la misma spec dan el mismo número, no que el consumo de sustancias esté bien medido.
  - «ACOTAR CESD-7» no dice que la depresión cambie: dice que la celda sellada incluía edad no especificada, y la sucesora no.
- **¿Qué afirmación sobre el corpus se escribió a mano?** Ninguna: todos los conteos salen de scripts versionados en `catalogo-1-lote3/` y `catalogo-1-sucesores/`.
