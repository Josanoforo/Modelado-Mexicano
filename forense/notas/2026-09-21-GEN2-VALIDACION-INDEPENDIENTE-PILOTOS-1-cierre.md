# Nota de cierre · `ACTO GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1` · 21/sep/2026

**Contadores movidos: cero** (`N_corridas_selladas`, `adoptados_activos`, `celdas_validadas` intactos; este acto no mide ni adopta: valida). Lo que sí mueve: la segunda pregunta de E.2 —¿pasó validación independiente?— pasa de «no hecha» a **hecha, `COINCIDE` en los tres pilotos** para las 35 celdas que sostienen la frase del producto.

## 0 · Arranque (skill `/acto`, cinco líneas)

- **REPO:** clon existente `/home/pc0/Modelado-Mexicano` en `main = fc13cdcc` (= `origin/main` = SHA de redacción); worktree del acto `/home/pc0/mm-validacion-independiente-pilotos-1`, rama `acto/gen2-validacion-independiente-pilotos-1`, empujada con el 0-bis desde el primer minuto (`7ef3b678`).
- **Guards 0.a–0.d:** base al día (0 detrás), árbol limpio, rótulo sin duplicado en remoto/worktrees/PR abiertos (sólo el propio), `limpia_arbol --reporta`: 22 worktrees, 10 ramas remotas sin PR (ajenas, no se tocan).
- **data/raw:** enlazada a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiada del clon padre.
- **ENTORNO:** `python3 tools/entorno.py --arranque` → `ENTORNO-DERIVADO = CAJA`, `montado=SI archivos_examinados=422`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, red PERMITIDA (200). El encargo pide CAJA: coincide.
- **COMPUERTA:** el encargo no trae `COMPUERTA:`/`GATED a` de merge; su única compuerta (§8) es interna —«P1 commiteado y en `origin`» protege **abrir dato** (los sellados)— y se cumplió: `19d35aba` empujado y verificado con `git ls-remote` antes de leer el primer `resultados.json`.

## 1 · Qué se hizo, en orden

| commit | contenido | dato abierto |
|---|---|---|
| `7ef3b678` | 0-bis: encargo verbatim + sello de cuerpo `4901869501b8…` | ninguno |
| `19d35aba` | **P1**: `valida_pilotos.py` (escrito desde las tres specs humanas + descriptor + catálogos) y `resultados_propios.json` (R e IC95 por celda, C2 por celda, marginales, conteos de universo) | ENIF 2024 (`localidad × edad` y marginales), ENVIPE 2025 (`escolaridad × dominio` y marginales), ENCIG 2025 (`edad × escolaridad` sobre luz y marginales). **Ningún `resultados.json` sellado.** |
| `265c9a7d` | **P2–P4**: `compara.py`, `comparacion-pilotos.{json,md}`, `informe-pilotos.md` | los seis `resultados.json` sellados |
| cascada | test huérfano `tests/test_validacion_independiente_pilotos.py` + fila propia en el censo de guardias; ADR, L0, rótulo, hallazgos, NC | — |

**Independencia (PARO a, verificable por el orden del diff y por declaración):** no se abrió `medidor.py`, `adjudicacion.py`, `captura_l.py` ni `spec.yaml`/`spec.md` de ningún CALC; ni `tests/test_celda_d_c2.py`, `tests/test_marginales_una_variable.py`, `tests/test_piloto3_v11.py`, `tools/celda_d/`, `tools/calibracion_mordida_encig_serie.py`, `tools/medidor_gobierno_digital_encig25.py`, `tools/ejes_maestra35_l1.py`, `tools/medidor_evasion_norma_envipe25.py`. Sí se leyeron: las specs humanas (`DIN…v1_2`, `TRA…v1_0`, `GOB…v1_1` + `v1_0`), `encig25_estructura_base_datos.pdf`, cabeceras de los cinco CSV y —una variable a la vez— conteos de `N_TRA`, `P7_3`, `NIV`, `EDAD` de ENCIG 2025 para el formato de código. Sesión nueva, sin ninguno de los tres pilotos en contexto. **Contaminación declarada (ADR-46):** esta sesión abrió microdato de ENIF 2024, ENVIPE 2025 y ENCIG 2025 y queda inhabilitada para pre-registrar contra esas fuentes.

## 2 · Veredicto

| piloto | celdas | R punto | R IC95 | C2 punto | marginales | n | **veredicto** |
|---|---|---|---|---|---|---|---|
| 1 · DIN · ENIF 2024 | 8 | 8/8 `IDÉNTICO` (`|Δ| ≤ 1e-6`) | 8/8 `COINCIDE` | 8/8 `IDÉNTICO` | 7/7 `IDÉNTICO` | exactos | **`COINCIDE`** |
| 2 · TRA · ENVIPE 2025 | 12 | 12/12 | 12/12 | 12/12 | 8/8 | exactos | **`COINCIDE`** |
| 3 · GOB · ENCIG 2025 | 16 (15 PUNTUADA) | 16/16 | 16/16 | 16/16 | 9/9 | exactos | **`COINCIDE`** |

Método de varianza propio: bootstrap de conglomerados estratificado sobre el marco entero, `default_rng(20260921)`, 10 000 réplicas, máscaras dentro de la réplica; tolerancia del IC declarada (extremos a ≤ 1.0 pp y razón de semianchos en [0.80, 1.25]); máximo observado 0.59 pp (`S1xD2`), razones en [0.90, 1.10]. Detalle celda por celda: `forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-v1_0/comparacion-pilotos.md`; informe: `informe-pilotos.md`.

## 3 · Hallazgos (P3) — ninguno supera la tolerancia; tres se dejan escritos

1. **Piloto 1:** los marginales públicos del árbitro (`tramite-ola5-propuesta-v0.yaml`) se estimaron sobre universos distintos por eje (localidad: 13 502 filas; edad: 13 487) y la spec v1.2 §3.1 fija uno solo (13 492): la re-derivación difiere de los públicos hasta 0.12 pp (localidad ≥15 000) y coincide `IDÉNTICO` con la del CALC, que ya lo declaró (`NO-REPRODUCE` previsto en §0.8). El punto sellado de `C2` usa los públicos, como la spec manda; con los re-derivados se movería ≤ 0.10 pp por celda.
2. **Piloto 3:** la spec humana admite dos lecturas del universo de los marginales de `C2` (universo del cruce F1-bis vs cada eje sobre su propio universo clasificable); la literal reproduce `IDÉNTICO`; la alternativa mueve `C2` ≤ 0.19 pp y ningún veredicto. Precisión pendiente para un sucesor de spec (no se edita la sellada, E.3).
3. **Piloto 3, S2:** `EDAD=97` → 1 trámite; `98` → 114; `99` → 0; fracción 0.00022 → `SIN-RESERVA`, igual que lo sellado.

**`[SUPUESTO]` del §3 del encargo (la spec humana basta):** se sostiene. Los huecos que hubo (nombres de columna y formato de código en ENCIG; universo de marginales del piloto 3) se cerraron con descriptor y catálogo, sin código, y ninguna resolución alternativa mueve más de 0.19 pp.

## 4 · P4 — lo que cambia para el producto (números propios)

MAE(`C2` vs `R`): **1.467 · 1.568 · 3.411 pp** (8 · 12 · 15 celdas), media ponderada **2.335 pp** sobre 35; máximo 12.28 pp (`60-96 × hasta primaria`, ENCIG). Cobertura del IC95 de `C2` sobre `R`: **26/35** (7/8 · 11/12 · 8/15). **Una línea:** «1.5 pp» se sostiene para DIN y TRA y se matiza en el conjunto (2.3 pp; ENCIG 3.4 pp); la cobertura del intervalo del piso es 74 %, lo esperado de un IC que sólo propaga muestreo de marginales y no error de especificación. **La cifra «18 de 20» del encargo no está en el árbol** (`git grep -E "18 de 20|18/20"` → 0 fuera del encargo; control positivo `grep "1.5 pp"` → 4 notas) ni sale de estas 35 celdas con ninguna lectura de cobertura (26/35 con IC de `C2`; 30/35 con `C2` dentro del IC de `R`): `NO-ENCONTRADO`; se pide su fuente a dirección antes de repetirla.

## 5 · Auditoría — universo real por piloto (leído del cuestionario)

- **DIN (persona elegida 18+, `fac_per`):** quien no tiene la cuenta a su nombre no responde «ahorró en ella» (`P5_4_k` gatea a `p5_6_k`) y cuenta como sin vía formal; el desenlace mide tenencia-y-uso propio, no acceso del hogar. Se hereda, no se corrige (spec §2.2).
- **TRA (delito, `FAC_DEL`):** 40 280 delitos = archivo entero (0 con `BP1_20` fuera); el informante es el seleccionado del hogar, no necesariamente la víctima; `BP1_23` en blanco con no-denuncia cuenta 0 (conjunta, no condicional); 100 delitos sin escolaridad clasificable fuera de las 12 celdas.
- **GOB (trámite, `FAC_TRA`):** pagos de luz realizados (20 392) con canal válido (20 203; 189 fuera por teléfono/no concluido/otro/NS-NR) y edad 18–96 con `NIV` clasificable (20 088; 115 fuera por edad 97/98). Fuera quedan quien no paga la luz, no la tiene a su nombre o la paga otro del hogar; quien hizo doce pagos cuenta doce veces. Es canal de pago del que paga, no «adopción digital» de la población.

## 6 · Premisas del encargo, verificadas

`[EXISTE]` los seis CALC y las tres specs: verificado (`ls data/corrida0/CALC-*`, `sello.json` presente en los seis; piloto 3 sellado en `main` por `#961`). `[EXISTE]` precedente `GEN2-VALIDACION-R-ENVIPE-CSV-v1_0/`: verificado, forma seguida (script + evidencia + informe con sufijo propio; `informe.md` a secas colisionó en `T02` con otro `informe.md` del árbol y se renombró `informe-pilotos.md`). `[LEÍDO]` unidades y universo del piloto 3: coinciden con lo medido. `[SUPUESTO]` specs bastan: sostenido (§3). §4 «ya hecho»: por objeto, `forense/validaciones/` trae sólo ENVIPE-CSV y PARAMETROS-ACTIVOS; ninguna validación de pilotos — se hizo.

## 7 · Perímetro tocado

Propio: `forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-v1_0/` (5 archivos), esta nota, `tests/test_validacion_independiente_pilotos.py` (huérfano, lo ejecuta `ci_guardias --ejecuta-huerfanos`: 57 ejecutados, 0 fallidos), una fila propia en `forense/analisis/ci-guardias/censo-tests.tsv`, cascada (`canon/gobernanza-v1_15.md` §4 `ADR-260921-GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1-7ef3-01`, `canon/L0/ADR-260921-GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1-7ef3-01.md`, `canon/registro-rotulos.tsv`, `forense/hallazgos.md`, `forense/no-corrido.tsv`, encargo archivado: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO`). **No tocado:** ningún sello, veredicto, CALC, marcador, `tests/check.py`, `verify.yml`, `cierre_acto.py`, `tablero_programa.py`, `estado_comun.py`, `digesto_tramite.py`, `.claude/commands/`, `.gitattributes`.

## 8 · Suite

`python3 tests/check.py --baseline --parallel` (`TZ=UTC`): VERDE contra `tests/baseline.json` tras renombrar `informe.md` → `informe-pilotos.md` (T02) y sustituir los rótulos de tramo de edad (`E` + dígito) por texto legible en las tablas propias (T25, D-6: `tests/check.py` no se edita por NO-CHOCAR). Salida cruda en el PR.
