# Nota · ACTO GEN2-CLASE-AMAI-1 · NSE AMAI por instrumento, pisos por NSE y cobertura del modelo por clase

24/sep/2026 · CAJA · MODO AUTÓNOMO · rama `acto/gen2-clase-amai-1` · 0-bis `e7732df2` · ADR `ADR-260924-GEN2-CLASE-AMAI-1-e773-01`.

**Contadores movidos:** seis CALC sellados (`cuenta_gen2: SI`, `adopta: NO`), 818 RESULT GEN2 sellados; **«conductas con piso por NSE»: 0 → 28**. No adopta, no toca el marcador.

## 0 · Arranque y reanudación

- Sesión reanudada tras apagado de la máquina. Estado encontrado: 0-bis `e7732df2` ya en origin (encargo verbatim + `.cuerpo.sha256`), un borrador sin commitear `tools/dominios/amai/regla.py` y nada más; sin PR, sin spec, sin transcripción recuperable de la sesión anterior. El borrador se revisó línea por línea contra el Anexo de la nota AMAI (puntos, topes, cortes) y se incorporó; ninguna cifra salió de la sesión caída.
- ARRANQUE: `git rev-list --count HEAD..origin/main` = 0 (base `8358b891`); árbol limpio salvo el borrador; sin duplicado (`git ls-remote`, worktrees, `gh pr list --search CLASE-AMAI` → sólo #1072 y #345, homónimos ajenos); `tools/entorno.py --sonda-red` → `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable · red=200 · raices=data_raw:SI descargas_mx:SI · corpus=SI(examinados=511)` → CAJA. `data/raw` enlazado a `/home/pc0/mm-corpus/raw`.
- Logística declarada: el sandbox de la sesión quedó atado a otro directorio tras un `cd` (memoria `cd` al directorio de memoria); los comandos corrieron fuera del sandbox, siempre dentro del worktree. Un subagente de censo no pudo ejecutar nada por la misma causa; el censo P1 lo hizo el ejecutor.

## 1 · Premisas del encargo

- `[EJECUTADO] grep -c AMAI canon/catalogo…` = 1: la tabla por instrumento **sí existía** en U1 (`forense/analisis/catalogo/matriz-amai-2024.md`, cinco olas). P1 la cita y completa (cláusula del encargo), no la rehace.
- `[SUPUESTO]` «ENVIPE/ENCIG tienen módulo de vivienda con las variables de la regla»: **FALSO** por texto (FD, diccionarios y cuestionarios 2023–2025; universo en `factibilidad-v1_0.md`). Toca qué se mide sólo para esos dos instrumentos; el objetivo sigue alcanzable con ENIGH, ENIF y ENDUTIH → no es PARO; NC con `PARO-PREMISA`.
- ENIGH 2024 está RESERVADA (`reserva:enigh2024`): no se abrió (PARO (a) evitado, no disparado). Las olas usadas (ENIGH 2022, ENIF 2021/2024, ENDUTIH 2023–2025) no tienen reserva; ninguna conducta ENIF toca la sección de crédito reservada.
- «Ya hecho»: `ls data/corrida0 | grep -ic 'AMAI\|NSE'` = 0 al abrir; ningún CALC por NSE existía.

## 2 · P1 · Factibilidad (`forense/analisis/clase-amai/factibilidad-v1_0.md`)

ENIGH 2022 **CALCULABLE** (6/6; el código R del Comité usa `conex_inte`, lo que corrige la **A** que U1 puso al internet de ENIGH) · ENIF 2021 y 2024 **APROXIMABLE** (ocupados = «personas que trabajan / con trabajo remunerado») · ENDUTIH 2023–2025 **APROXIMABLE** (4/6: sin baños ni dormitorios; auto sí/no) · ENVIPE 2024/2025 y ENCIG 2023/2025 **NO-CONSTRUIBLE**. Firma D4 (FIRMAS-12, fila `FP-260923-GEN2-TRAMITE-FIRMAS-12-c3fa-04`): con letra estricta hay un solo CALCULABLE; se sigue la forma del «Hecho» («CALCULABLE o APROXIMABLE», tres instrumentos) como INTERPRETACIÓN-DECLARADA. Este acto es el «lo incorpora» de D4; la columna `ejecutada_en` de esa fila no se edita en su sitio (D-21) y queda para el trámite de mesa.

## 3 · P2 · NSE por instrumento (spec `forense/prereg-caja/AMAI-NSE-spec-v1_0.md`, sha `4599051b…`)

COMMIT-1 `42807ece` congeló spec, medidor, agrupación (BAJO E·D·D+ / MEDIO C−·C / ALTO C+·A/B), supresión n < 200 (F-U5-2), umbral de desvío 5 pp y criterio REPRODUCE-AMAI 0.15 pp **antes** de abrir microdato; conducto probado sobre sintético en tres ramas terminales y sobre oro (`tests/test_amai_nse.py`, 29/29); `corrida0 preflight` VERDE en los seis. Resultado (primer y único resultado, sin corridas descartadas):

| CALC | Validación | Hogares con / sin NSE |
|---|---|---:|
| `CALC-AMAI-NSE-ENIGH-2022-0001` | CALCULABLE-REPRODUCE-AMAI (máx. 0.05 pp por nivel) | RESULT `-N-HOGARES-CON-NSE` / `-SIN-NSE` |
| `CALC-AMAI-NSE-ENIF-2021-0001` | APROXIMACION-CONFORME (0.35 pp) | ídem |
| `CALC-AMAI-NSE-ENIF-2024-0001` | APROXIMACION-CONFORME (3.01 pp) | ídem |
| `CALC-AMAI-NSE-ENDUTIH-2023-0001` | APROXIMACION-CONFORME (4.72 pp) | ídem |
| `CALC-AMAI-NSE-ENDUTIH-2024-0001` | **APROXIMACION-DESVIADA** (6.97 pp) | ídem |
| `CALC-AMAI-NSE-ENDUTIH-2025-0001` | **APROXIMACION-DESVIADA** (9.72 pp) | ídem |

Coincidencia verificada, no defecto: ENIF 2021 y 2024 tienen ambos 13 464 hogares con NSE (13 561 − 97 y 13 508 − 44; payloads, llaves y factores distintos). `verify` REPRODUCE / CONTEXTO IDENTICO en los seis, en proceso aislado (`tools/verifica_aislada.py`), asentado en `forense/replay-evidencia.tsv` (E.7) con la evidencia cruda en `forense/analisis/clase-amai/evidencia-replay-GEN2-CLASE-AMAI-1-2026-09-24.json`.

## 4 · P3 · Pisos por NSE

`forense/analisis/clase-amai/pisos-nse-v1_0.tsv` y `tabla-conducta-nse-ola-v1_0.md`: 28 conductas (ENIGH 1, ENIF 2024 17, ENDUTIH 10 × 3 olas), 144 celdas, 140 publicables; IC de diseño (1 000 réplicas UPM compartidas); RESULT por id `RESULT-AMAI-NSE-<INST>-<OLA>-<conducta>-<GRUPO>-P`. Unidad y universo por conducta en la spec §5.

## 5 · P4 · Cobertura por clase y FP (`cobertura-por-clase-v1_0.md`)

Del catálogo U1: 17 de 55 identidades de conducta con piso por NSE; 49 de 165 celdas conducta × grupo publicables; 23 de 55 (ENVIPE 18, ENCIG 5) sin corte AMAI posible. Potencia: 37 de 48 contrastes ALTO − BAJO despejan 0. **FP-260924-GEN2-CLASE-AMAI-1-e773-01**: NSE como eje del marcador con reserva de instrumento (recomendación en el documento). **FP-…-e773-02**: ENIGH 2024 para NSE (reserva).

## 6 · Auditoría de rigor extremo

En `cobertura-por-clase-v1_0.md` §4 («¿qué parece cultura y es clase?»): horizonte corto, informalidad del ahorro, desconfianza, familia como seguro y tecnología. Límite principal: NSE AMAI son bienes y capital escolar del hogar, no ingreso ni clase sociológica; ENDUTIH imputa 122/300 puntos; ENIF aproxima ocupados. Todo RETROSPECTIVA; ninguna cifra de hogar se compara con una de persona.

## 7 · Defectos adyacentes (D-21)

- `README.md`: las cifras de `corrida0 status` quedan desfasadas al sellar (252 corridas y 67 400 RESULT GEN2 tras este acto); actualizadas y `tests/test_readme_derivado.py` OK.
- Test nuevo con fila propia en `forense/analisis/ci-guardias/censo-tests.tsv` (sin regenerar el censo ajeno); `ci_guardias --ejecuta-huerfanos` lo reconoce (SKIP por `pytest` ausente en CI; corre en CAJA).

## 8 · Lo que no se corrió

Ver `## NO-CORRIDO / RESERVAS` del encargo y las filas `NC-260924-GEN2-CLASE-AMAI-1-e773-01..03`.
