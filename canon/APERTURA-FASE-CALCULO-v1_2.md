# APERTURA · FASE DE CÁLCULO v1.1 — el diff del plan contra hoy, y el marcador que falta
**Dirección, 19/ago/2026, contra `b4a9b3f` (#292) + `PLAN-CALCULO-TOTAL-v1_0` (12/ago, leído del espejo del proyecto — ⚠️ ese plan NO está en el repo; sellarlo es la tarea T-SELLO de abajo).**

> **Nota de procedencia (20/ago/2026 · `T-SELLO`, `ADR-131`):** aterrizado verbatim desde el adjunto de la compuerta de arranque, recibido con cabecera declarada `sha256 a35b5452…`, 8 870 bytes, 54 líneas. sha256 del adjunto, verificado exacto contra ese declarado: `a35b545269948bd02651f0b5ae324a694953da4f3a3720895b82b529d6c1bad1`; bytes y líneas coinciden. Archivado como `canon/APERTURA-FASE-CALCULO-v1_2.md` — v1.1 pasa a v1.2 porque `§5` queda marcado `SUSTITUIDO` por el careo de dirección (banner de una línea en el propio `§5`, abajo; el texto original no se borra, `A.10` corolario 1). `diff` contra el adjunto: sin diferencia de cuerpo — las únicas líneas nuevas son esta cabecera y el banner de `§5`; el salto final es el mismo. Primera entrada de este documento al repo: `git ls-files | grep -i calculo-total` y la búsqueda por título (`APERTURA.*FASE.*CALCULO`, `MAESTRA OPUS`) dan **cero** contra tu SHA, universo árbol completo menos `.git` — **1 727 archivos**, recontado hoy y no heredado del **1 717** que declaró quien escribió el encargo: la diferencia son los archivos que entraron con la fusión de `PR #295` (`ACTO SELLA-ADV`) y `PR #296` (`ACT-PIL-1 · CONTRATO-v0_5`) después de esa cuenta.

## §0 · La esencia, verbatim de mesa, para que gobierne este documento
> "La construcción de todo esto es en sí: **si un LLM puede superar lo que un motor como el que creamos con data real pueda retornar**. Si nos estamos enfocando más en el cumplimiento de ADRs, o en los gates, o los congelados, estamos perdiendo el enfoque."
El whitepaper lo dice en espejo: el riesgo central del simulador es volverse *"bellísimo, fluido y equivocado"* — y el riesgo central del programa es volverse **riguroso, ordenado y quieto**. El antídoto es el mismo: un marcador que se mueve o no se mueve.

## §1 · Diff OLA por OLA — plan v1.0 (12/ago) contra lo derivado hoy
| OLA | Plan decía | Hoy, derivado | Queda |
|---|---|---|---|
| **0** | J · ACTO S · corrida e4c → llaves 0→1 · mesa adjudica D2 | **HECHA**: llaves = 1/2 ejercida; R5.1-D2 adjudicada; R5.1-D3 corrió (fila B, EJERCIDA_INDECISA) | FP-68/FP-69 (firmas en LOTE-NUBE T6) |
| **1** | U1 (10ª θ) · U2 (validación externa) · U3 (backfill) · liberar las 8 de radio (ADR-71(a)) | U1 ✓ (condicionales 9→**12/15**) · U3 ✓ (#288) · U2 **parada en adquisición** (FP-67; material → LOTE-UBUNTU T1) · liberación-8-radio: **estado no derivado** | T1 del LOTE-UBUNTU · en LOTE-NUBE T4, el ejecutor lee ADR-71(a) y declara si la liberación quedó hecha o pendiente |
| **2** | **Abrir ENFIH/ENSAFI a nivel variable** → hasta 4 SIN-RUTA ganan ruta → mesa reabre 52A/54 acotado | **NO HECHA.** Sigue siendo "la palanca más grande dormida del corpus" (palabras del plan). El census de β del plan quedó superado por `coef-universo` (50 filas, 21 co-observables) — se re-deriva de ahí | **APERTURA-ENFIH-ENSAFI** (§3, el encargo que faltaba) |
| **3** | DESC-1 (5 fuentes) + INDICE-3 | Mayormente hecha por otra vía: ADQ-15 (#277, 89 payloads), WVS/ISSP/Latinobarómetro en manifiesto; LAPOP "sin reactivo" (ADR-111) | Verificación puntual de EMOVI en LOTE-UBUNTU (una línea en T2) |
| **4** | **Piloto celda-D**: E0 nube → E1-E2 auditor/veto → E3 caja → 10-15 celdas FIN → **7 umbrales por comando → mesa firma GO/NO-GO** | E0 **aterrizado** (#266: `milpa/src/celdas.py`, `clases.py`, validador en main). E1-E3: **sin correr**. `milpa-spec`/`plan` cargan banner de incompatibilidad parcial (gobernanza:754) — declarado, no bloquea | **PILOTO-E1E3** (§4) — esto ES abrir la fase de cálculo |
| **5** | Catálogo de momentos · AJUSTADO · ENNViH ejerce llave (ii) | Catálogo v0.1 en `milpa/` · **ENNViH murió como llave (ADR-107)**; FP-64/T3 deriva candidatos | Post-GO, como el plan manda |

**Traducción de §4 del plan, vigente hoy:** *"Nada nuevo de estructura"* sigue siendo cierto. Lo que falta para calcular son **tres actos y un marcador** — no más infraestructura, no más reglas.

## §2 · Los cuatro desbloqueos, en orden
**D1 — Residuo OLA 1** → ya escrito: LOTE-UBUNTU-ADQ-1 T1 (material de U2) + LOTE-NUBE T4 (liberación-8-radio: declarar estado).
**D2 — APERTURA-ENFIH-ENSAFI (§3)** → la ola de mayor β-por-sesión del tablero, intacta desde el 12/ago.
**D3 — PILOTO-E1E3 (§4)** → el simulador corre sus primeras 10-15 celdas y produce los 7 umbrales; mesa firma GO/NO-GO. **Ese GO es la apertura formal de la fase de cálculo.**
**D4 — DUELO-PREREGISTRO (§5)** → la esencia, por fin escrita como B-bis del programa entero. Sin esto, el piloto produce números sin árbitro y "superar" queda a opinión.

## §3 · ENCARGO embebido · APERTURA-ENFIH-ENSAFI — UBUNTU · Opus · tras LOTE-UBUNTU-ADQ-1
Ley de fondo: PLAN-CALCULO-TOTAL §3-OLA2 + celdas objetivo del censo de β (re-derivado de `data/coef-universo-v1_0.tsv`, filas ENFIH/ENSAFI). Doctrina de lote aplica (tareas, PARO por tarea, contador por tarea).
**T1** · Abre ENFIH 2019 y ENSAFI 2023 **a nivel variable** contra las celdas objetivo, con términos pre-registrados en tu COMMIT A antes de abrir un solo archivo (los términos salen de las necesidades del censo β, no de exploración libre). `command grep` con conteo de examinados; codebooks primero, microdato después.
**T2** · Por celda objetivo: veredicto A.4 con variable nombrada (`variable_id`), universo del instrumento y escala declarada. Tabla `data/apertura-enfih-ensafi-v1_0.tsv`.
**T3** · Si aparece reactivo que reabre ADR-52A/54: **NO reabres** — escribes la propuesta acotada con el reactivo exacto a la vista y abres fila para mesa (la reapertura es firma de mesa, el plan lo dice).
**T4** · Cierra: cuántos de los SIN-RUTA ganaron ruta (número dicho), fichas B-bis para lo medible ya, ADR, fila(s), nota. Contador: β con ruta antes→después.
ARRANQUE de Bloque D completo (el de LOTE-UBUNTU-ADQ-1, textual, con las tres partes de entorno y la regla del grep). Perímetro: la tabla nueva · coef-universo (columna ruta) · tablero · gobernanza · estado (cascada) · hallazgos · nota · encargo. Microdato solo lectura.

## §4 · ENCARGO embebido · PILOTO-E1E3 — E1-E2 NUBE · E3 UBUNTU · Opus
Ley de fondo: PLAN-CALCULO-TOTAL §3-OLA4 + `milpa-spec` (con su banner: donde spec y `milpa/src` diverjan, **main gobierna y la divergencia se anota, no se resuelve aquí**) + `tests/test_celdas_d.py`.
**T1 (nube)** · E1: emite las celdas-D de la cola con las 3 semillas primero; auditor y veto conforme a la ley; cada celda con su clase de procedencia A LA VISTA (procedencia.yaml manda; un valor sin clase no entra).
**T2 (nube)** · E2: corrida de las celdas emitidas; salidas con universo y escala declarados (A-bis 3/4); **ninguna celda se compara contra otra escala sin enlace**.
**T3 (caja)** · E3: el gate de semana-1 contra microdato (ENFIH/ENSAFI ya abiertas por §3 lo vuelven casi gratis — el plan lo predijo).
**T4** · Los **7 umbrales del plan, por comando**, en tabla, sin adjetivos → fila de mesa **GO/NO-GO**. Contador: celdas FIN (meta 10-15), umbrales cumplidos N/7.
Desde E0 rige el congelamiento del motor (ADR-68(a)): el piloto NO edita reglas del motor; lo que quiera editar se anota como candidato de OLA 5.

## §5 · DUELO-PREREGISTRO — la esencia como B-bis, para firma de mesa

> ⚠️ **`§5` SUSTITUIDO (20/ago/2026, `T-SELLO`, `ADR-131`) por el careo de dirección `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md`** — el DISEÑO v2 de su `§B` (cuatro corredores L/M/B/E, mecanismos `ADV1-M1`…`ADV1-M6`) y las decisiones `D-i`…`D-iv` de su `§C` reemplazan el diseño de duelo de tres corredores que este `§5` proponía. El texto original de este `§5` **no se borra** — queda íntegro debajo, como historia de lo que se proponía antes del careo (`A.10`, corolario 1: un sello vencido se reactiva por re-sello encima, nunca por edición del viejo).

Tres corredores por pregunta, mismas preguntas, sellado ANTES de ver la primera salida del piloto:
- **Corredor L (LLM):** respuesta congelada del corpus/LLM a la pregunta, con su tier, SIN acceso al motor ni al microdato. Se congela primero (commit propio) — si se escribe después de ver al motor, el duelo nace muerto.
- **Corredor M (motor):** la celda-D del piloto para la misma pregunta, con su clase de procedencia.
- **Árbitro R (dato real):** el benchmark adjudicado contra microdato/desenlace documentado (patrón ya probado: conf02-policronia, conf05-consumo, R51D3, crédito-popular N=11).
**Marcador:** por pregunta, distancia de L y de M al árbitro R, en la escala del árbitro (A-bis 3). "Superar" = pre-declarado: quién queda más cerca de R en ≥X de N preguntas, con empates definidos. **Decisiones de mesa para sellar el duelo (tres):** (1) N y el set de preguntas v1 — propuesta: los momentos del catálogo v0.1 que ya tienen árbitro posible, mínimo 10; (2) X y la regla de empate; (3) qué pasa con cada resultado — L gana / M gana / empate — escrito antes (fila E de corroboración, como manda B-bis).
**Regla de señal de fase (propuesta, hereda v2.3):** abierta la fase, *cada semana produce al menos una celda FIN o una fila del marcador del duelo — o produce nada y lo dice.* Los ADRs, gates y congelados quedan al servicio del marcador: un acto que no alimenta ni una celda ni el marcador ni una decisión que los destrabe, se anota y no se lanza.

## §T-SELLO · Gobernanza mínima de este documento
Un acto NUBE corto committea: este documento + `PLAN-CALCULO-TOTAL` v1.1 (el v1.0 del espejo con la tabla §1 como delta fechado, original intacto) a `canon/`, con ADR que cite la firma de mesa de apertura. Sin esto, la fase abre en una conversación y no en el canon — el defecto A.9 exacto.

## Lo que este documento deliberadamente NO hace
No espera los 15 β identificados para abrir la fase — el motor corre con clases a la vista y mejora por iteración (eso es OLA 5); esperar la identificación perfecta era el aparato comiéndose a la esencia. No resuelve la divergencia spec↔src (banner declarado; main gobierna). No re-audita el corpus completo: la validez "no tan sólida" del trabajo pre-fuentes se re-deriva **bajo demanda del duelo** — lo que un corredor L afirme y el árbitro R contradiga se re-tieriza ahí, con su acto; lo demás queda fechado (doctrina FP-57, y la lección del 30/jul).
