# ACTO FP58-PROPAGA-CANON — el residual del 22% llega a los cinco sitios que lo citan

### 19 de agosto de 2026 · Entorno **NUBE**, repo-only, sin `data/raw` · derivado contra `20c7dee` (merge de `PR #283`, `ACTO REFUTACIONES-SIN-OBJETO`)

---

## §0 · Verificación de existencia, re-corrida contra el árbol

**1 · Estructura.** `grep -rln "22[ .]*%" canon/` → 5 archivos: `glosario-v5_6.md` · `estado-programa-v1_10.md` · `modelo-decision-v4_0.md` · `gobernanza-v1_15.md` · `integrador-psicologia-mexicano.md`. `corpus/` no entra: es base de evidencia fechada (`FP-57`/`ADR-114`) y no se retoca.

**2 · Contenido.** `modelo-decision-v4_0.md:585` (§5.0 regla 3) mostraba, antes de este acto, el residual sin adjudicar: *"Las otras tres del racimo (12% WVS 2012, 22% Latinobarómetro/LAPOP, 18% Pew 2025) no son ENCUCI y siguen sin establecer"* — **EXISTE-NO-SATISFACE**, `ADR-111` (18/ago) ya lo había adjudicado pero el canon seguía sin decirlo. Cada uno de los cinco sitios se re-derivó individualmente (§2 abajo); ninguno citaba ya `ADR-111` antes de este acto, así que ninguno fue EXISTE-SATISFACE por adelantado.

**3 · `data/raw`.** Este acto no abre microdato: las tres cifras que cita (10.51%, 26.06%, 18%) se re-derivan de `forense/notas/2026-08-18-fp29-adjudicacion.md` §3.2/§4, no de una corrida nueva.

**4 · Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` — nube, sin sonda de red.

**5 · Espejo.** Las cifras de arriba se tomaron de `forense/notas/2026-08-18-fp29-adjudicacion.md:165` (WVS `Q57` = 10.51%, `IC95%[8.86,12.15]`) y `:177` (Latinobarómetro `P10STGBS` = 26.06%, `IC95%[22.45,29.67]`), re-leídas antes de escribirlas en canon, no citadas de memoria.

---

## §1 · Los ocho sitios, uno por uno

| Sitio | Estilo | Qué se hizo |
|---|---|---|
| `glosario-v5_6.md:84` | cuerpo | Corregido: la fila "Confianza radial — magnitud" cita ahora la adjudicación completa de `ADR-111`, con instrumento+ola+`IC95%` por cifra. |
| `glosario-v5_6.md:321` | cuerpo | Corregido: la entrada `conf.06` gana una anotación con la adjudicación del residual. |
| `glosario-v5_6.md:132` | — | **Saltado, falso positivo declarado**: "22% en tandas" (ROSCAs, CONDUSEF/ENSAFI) — no es confianza interpersonal, no cita `conf.06`. |
| `modelo-decision-v4_0.md:585` | cuerpo | Corregido: §5.0 regla 3 gana la adjudicación completa tras la frase que dejaba las tres cifras "sin establecer". |
| `integrador-psicologia-mexicano.md:143` | cuerpo | Corregido: "Evidencia en contra / límites" explica ahora que la variación 12%/22%/26% ya se investigó y qué se encontró. |
| `estado-programa-v1_10.md:213` | anotado | El casillero S5 de `conf.06` gana una anotación fechada; el texto original (que ya traía su propia nota fechada) no se toca. |
| `gobernanza-v1_15.md` — `ADR-64(a)` | **enmienda in situ** | Texto histórico de ADR sellado (5/ago/2026). Original intacto. Enmienda fechada debajo, estilo `A.10` Corolario 1, apuntando a `ADR-111`. |
| `gobernanza-v1_15.md` — `ADR-101(f)` | **enmienda in situ** | Ídem, ADR sellado 18/ago/2026 ("el 22% sigue sin sellar" — ya no es cierto). Original intacto, enmienda debajo. |
| `gobernanza-v1_15.md` §5.1 tabla | directo | Fila `conf.06` del casillero de pendientes irresueltos — es casillero vivo (mismas filas hermanas `conf.02`/`conf.04`/`conf.07` ya se editan directo con notas fechadas), no cita histórica de un ADR — editada directo. |

**Por qué `ADR-64(a)`/`ADR-101(f)` sí y la tabla `§5.1` no, con el mismo criterio de "texto histórico de ADR":** los dos primeros son prosa dentro del cuerpo sellado de un ADR específico, citada como lo que ese ADR dijo en su fecha. La tabla `§5.1` es un casillero de estado que el propio documento mantiene vivo — sus filas hermanas ya llevan notas fechadas insertadas directamente sin envoltura de blockquote, y tratarla como intocable habría dejado el único resumen tabular de `conf.06` desactualizado sin razón.

---

## §2 · El contenido propagado — el mismo en los ocho sitios

El 22% **no queda sustituido por otra cifra puntual**: queda sin procedencia sostenible. Las cuatro atribuciones, probadas contra microdato por `ADR-111(b)`:

| Atribución | Instrumento/reactivo | Resultado |
|---|---|---|
| WVS 2018 | `Q57`, binaria, Wave 7 México | **REFUTADA** — 10.51% `IC95%[8.86,12.15]` |
| Latinobarómetro | `P10STGBS`, binaria, única ola 2024 | **NO SOSTENIDA** — 26.06% `IC95%[22.45,29.67]` |
| LAPOP | `it1`, 4 puntos, no fielda el reactivo generalizado | **REFUTADA POR ERROR DE CATEGORÍA** |
| ENAFI | — | **INDECIDIBLE** — no adquirido |

De propina, ya establecido por `ADR-111(c)`: el 18% de Pew (`Q104`, Spring 2025) **reproduce exacto**; el 12% (WVS Wave 6, 2012) queda **indecidible** por falta de la ola, con el punto 2018 de esa misma serie fijo en 10.51%.

**Rango medible, nunca promediado entre sí (Bloque A-bis regla 3):** binarios **10.5%–26.1% (2018-2025)** · ENCUCI **21.9% a ≥8/10 (2020)**.

**Por qué opción (b) y no (a) o (c) de `FP-58`.** (a) RETIRAR habría borrado la cifra sin dejar rastro de que el corpus la citó — contra el mismo criterio que `ADR-64(c)` fijó para `corpus/reports/`. (c) ESPERAR la prueba de procedencia documental de `ADR-111(d)` deja el canon citando indefinidamente una cifra ya probada sin procedencia. (b) SUSTITUIR es lo único que deja el canon describiendo el árbol real hoy.

---

## §3 · Tablero, ADR y cascada

**`FP-58`** → `ABIERTA` → **`CERRADA`** (firmada y ejecutada en el mismo acto, mismo patrón que `FP-55`/`FP-59`: la ejecución es la decisión de dirección, no una firma aparte). Fila editada byte-preservante, sin `csv.reader`/`csv.writer` (tercer aviso del mismo cepo, `hallazgos.md`).

**`ADR-118`**, sellado en `canon/gobernanza-v1_15.md`. Número derivado, no supuesto: contra `20c7dee`, `grep -oE "^\*\*ADR-[0-9]+" canon/gobernanza-v1_15.md | sort -u | wc -l` → **117 únicos, máximo 117, sin huecos** → candidato **118**. Re-derivar al fusionar, como todo ADR de esta semana.

**Cascada del conteo:** `gobernanza-v1_15.md:2` (cabecera, 117→118), `estado-programa-v1_10.md:27` (tabla) y `:101` (`L0`). **Cascada del WARN:** un `T22` menos al cerrar `FP-58` (`ABIERTA`→`CERRADA`) — 118→117, `estado-programa-v1_10.md:204,296`.

**Suite:** `python3 tests/check.py --baseline` → **LÍNEA BASE: VERDE, 21 FAIL · 117 WARN**. Sin `--freeze`.

---

## §4 · Auditoría

**Contadores de medición sobre México movidos: 0.** Este acto no abre microdato ni corre nada nuevo — cita, no mide. Las tres cifras del §2 vienen re-derivadas de `forense/notas/2026-08-18-fp29-adjudicacion.md`, no de una corrida propia.

**Perímetro respetado.** `corpus/reports/**` no se tocó. `milpa/refutations.yaml:453` (la única celda de la capa ejecutable que cita la trayectoria refutada) queda fuera de perímetro, tal como `§6` de la nota de `FP29-RECONCILIA` ya la había puesto en cola para el sucesor — sigue en cola, no la absorbe este acto.

**Concurrencia declarada.** `FP60-ADJUDICA` corría en paralelo en nube con perímetro disjunto salvo `gobernanza-v1_15.md`/`forense/firmas-pendientes.tsv` — colisión esperada, resuelta por el protocolo ya precedentado (renumera quien fusione después).

**Escrito:** este archivo · `canon/glosario-v5_6.md` (:84, :321) · `canon/modelo-decision-v4_0.md` (:585) · `canon/integrador-psicologia-mexicano.md` (:143) · `canon/estado-programa-v1_10.md` (:213, cabecera, `L0`, cascada de WARN) · `canon/gobernanza-v1_15.md` (`ADR-118`, enmiendas in situ de `ADR-64(a)`/`ADR-101(f)`, tabla `§5.1`, cabecera) · `forense/firmas-pendientes.tsv` (`FP-58` → `CERRADA`) · `forense/hallazgos.md` (append) · `forense/encargos/2026-08-19-FP58-PROPAGA-CANON.md` (archivado, `CONSUMIDO`).

**No tocado:** `corpus/`, `data/`, `milpa/`, `tests/**`.
