# Nota de cierre · ACTO GEN2-MARCO-M-CONSUMIDOR-1

Encargo: `forense/encargos/2026-09-22-GEN2-MARCO-M-CONSUMIDOR-1.md`.
Mapa: `forense/notas/2026-09-22-GEN2-MARCO-M-CONSUMIDOR-1-mapa.tsv` (116 filas: 46 de código + 70 de lectura legacy activa).
Test en seco huérfano: `tests/test_marco_m_en_seco.py` (3 casos, los tres verdes; discovery por `tests/test_*.py`, D-21, no toca `verify.yml`).

## Verificación de premisas (§4.1 de la skill)

- `[EJECUTADO]` de dirección declaraba 8 archivos / 29 referencias sobre `grep -rn "marco-M-sorteado" tools/ tests/ milpa/`. Re-corrido en esta sesión: **13 archivos / 46 referencias** (los 5 archivos y 17 referencias adicionales están en `tests/`: `check.py`, `test_score_render.py`, `test_corredores_gen2.py`, `test_corrida0.py`, `gonogo_marcador.py`). Premisa `[EJECUTADO]` desactualizada por deriva del repo entre el 20/sep (plan de aceleración) y hoy — logística, no estimando: el criterio de «hecho» del propio encargo usa el conteo en vivo (`≥ el conteo de grep…`), así que el mapa se construyó sobre 46, no sobre 29, y eso satisface el criterio sin ajustar nada.
- `[EXISTE]` sobre `milpa/estimadores-por-segmento.yaml`: dirección declaró no saber si estaba vacío. **No está vacío**: 4084 líneas, 20 celdas ya emitidas por `tools/marcador_segmento.py` (ACTO GEN2-MARCADOR-REDISENO-1, 19/sep/2026), fuente `adopcion:piso-C2-20-celdas`. `grep -n "marco-M-sorteado\|marco_m_sorteado" tools/marcador_segmento.py` → sin coincidencias: el marcador **no** lee el marco M. Esto resuelve por sí sola la pregunta de LATITUD §6 (¿sustituto «previsto, no existente» o esperar la firma de marginales?): el sustituto para el eje que ya migró **ya existe y está en uso**, no es hipotético.
- `[SUPUESTO]` «retirar el marco M rompe GO-MARCADOR y `emite_m.py`, y no rompe nada del catálogo ni de las celdas-D» — **parcialmente confirmado, con matiz que el mapa ya recoge**:
  - `emite_m.py` opera sobre `marco-M-sorteado-v1_0.tsv`/`v1_1.tsv` (constantes `RUTA_MARCO_V1_0`/`RUTA_MARCO_V1_1`, literales). **No lee v1_3** en ninguna de sus 10 referencias — la premisa de dirección sobreestimaba el impacto sobre esta herramienta. `emite_m.py --help` (en realidad corre P2/regresión — el flag `--help` no está cableado, se ejecutó igual como pieza P2 y no crasheó) confirma que v1_3 ausente no lo toca.
  - `tests/gonogo_marcador.py` sí rompe (confirmado por P2, ver abajo): `MARCO_VIGENTE_REL`, `CALC_M`, `CALC_AGG` y la regex `_RE_MARCO` citan v1_3 directamente.
  - `tools/corrida0.py` rompe, pero **no en el subcomando que el encargo nombró** (`status`): `MARCO_VIGENTE` sólo la consumen `_consumidores_celdas` (usada por `cmd_numera_res`) y `cmd_demanda`, ninguno es `status`. `corrida0.py status` en seco no crasheó; `corrida0.py demanda` sí (`FileNotFoundError` en la línea 423, confirmado). El mapa quedó corregido a este nivel de granularidad (por subcomando, no por archivo) porque P2 lo exigió («si no coincide, el mapa se corrige, no el test»).
  - Ninguna celda-D ni `milpa/estimadores-por-segmento.yaml` citan el marco M — la parte «no rompe el catálogo ni las celdas-D» de la premisa se sostiene.

## P1 · Mapa de lecturas

116 filas ≥ 46 referencias de código (criterio de «hecho» cumplido: `awk -F'\t' 'NR>1' forense/notas/2026-09-22-GEN2-MARCO-M-CONSUMIDOR-1-mapa.tsv | wc -l` → 116; `grep -rn "marco-M-sorteado" tools/ tests/ milpa/ | wc -l` → 46).

Distribución:
- Código (46 filas): 22 con `se_rompe=SI` (7 herramientas/tests: `tools/corrida0.py`, `tools/pines_mesa.py`, `tools/tablero_programa.py`, `tools/arbitra_gen2.py`, `tests/gonogo_marcador.py`, `tests/test_corredores_gen2.py`, `tests/test_corrida0.py`) todas `SIN-SUSTITUTO`; 24 con `se_rompe=NO` (comentarios, docstrings o constantes que citan v1_0/v1_1/v1_2, no v1_3 — `NO-APLICA`; o parámetros invocables a mano — `SIN-USO-ACTIVO`).
- Legacy activo (70 filas, por `resultado_id` de `data/corrida0/usos.tsv`, columna `consumidor`): **27 `YA-ADOPTADO`** (pin de mesa de `GEN2-RELEVO-TANDA-3`/`TANDA-4`, campos R y M en su mayoría — no se rompen: ya tienen reemplazo firmado); **0 `CANDIDATO-GEN2`**; **43 `SIN-CANDIDATO`** (28 filas `celda_L`, 14 `celda_AGREGADO`, 1 `celda_M` huérfana — `DIN-M-01:M` — sin `via_relevo` ni pin). Consistente con `corrida0.py status`, en vivo: `legacy_marco_M_por_campo__L=28`, `__AGREGADO=14`, `__M=1` (`DIN-M-01`), `__R=0`.

**Costo real del retiro** (para P3): 22 filas de código `SIN-SUSTITUTO` + 43 filas legacy `SIN-CANDIDATO` = **65 filas sin sustituto declarado**, sobre **7 herramientas/tests** que habría que adaptar.

## P2 · Prueba en seco

Copia temporal con `git archive HEAD | tar -x` (nunca el clon; 399 MB, borrada al cerrar). `marco-M-sorteado-v1_3.tsv` renombrado a `.HISTORICO` dentro de la copia.

| comando | resultado |
|---|---|
| `python3 tests/gonogo_marcador.py` | **NO-GO — 3 fallos**, los tres `LEGACY-NO-LEIDO` (corredor M, adaptador R, agregado), `FileNotFoundError` sobre `marco-M-sorteado-v1_3.tsv`. Coincide con el mapa (filas `SI`/`SIN-SUSTITUTO` de `gonogo_marcador.py`). |
| `python3 tools/emite_m.py --help` | Corrió P2/regresión (el flag no está cableado como ayuda) — **verde**, sin tocar v1_3. Coincide con el mapa (`emite_m.py` sólo cita v1_0/v1_1). |
| `python3 tools/corrida0.py status` | **Verde**, sin `FileNotFoundError`. `python3 tools/corrida0.py demanda` (pieza adyacente de la misma constante `MARCO_VIGENTE`) **sí crashea** — confirma que el riesgo es real pero no en el subcomando nombrado. Mapa corregido a granularidad de subcomando (ver arriba). |

`tests/test_marco_m_en_seco.py` (huérfano) automatiza estos tres casos con `cp -al` (hardlinks; renombrar en la copia no toca el inode del repo real) para que quede como regresión permanente: si algún día el costo real diverge del mapa, este test lo señala primero.

## P3 · FP de retiro

`FP-260922-GEN2-MARCO-M-CONSUMIDOR-1-02e6-01` en `forense/firmas-pendientes.tsv` — vocabulario cerrado del §2 del encargo. Recomendación del ejecutor (marcada como tal): **`HISTÓRICO-SIN-RETIRO`** — de los tres, es el único que no deja huérfanas 65 filas de golpe: rotula el archivo como histórico (deja de ser candidato a nuevas lecturas) sin romper las 7 herramientas que hoy lo leen para su eje `x = ∅`, mientras el relevo (vía `via_relevo`/pin de mesa) termina de vaciar las 43 filas `SIN-CANDIDATO`. `RETIRAR-CON-MAPA` exige antes adaptar las 7 herramientas (acto de tubería, ya declarado como sucesor). `CONSUMIDOR-VIGENTE` no aplica: ningún consumidor GEN2 (marcador por segmento, celdas-D) lee el marco M.

## Consistencia con el contador

`CONTADOR: cero mediciones` se cumple: este acto no tocó `data/corrida0/decisiones.tsv`, no adoptó nada, no movió `adoptados_activos` ni `dependencias_numericas_legacy_activas`. La corrida de `corrida0.py status` en el árbol REAL (no en la copia temporal) para dejar constancia del valor vigente, sin escribir nada:

```
dependencias_numericas_legacy_activas=146
legacy_marco_M_por_campo__R=0  __M=1  __L=28  __AGREGADO=14
legacy_marco_M_celdas_M_pendientes=DIN-M-01
```
(el 184 que citaba el encargo al redactar es el mismo contador, medido el 17-20/sep; hoy son 146 — la diferencia la explican los relevos de `TANDA-3`/`TANDA-4`/`TANDA-5`, ajenos a este acto).
