# ACTO GEN2-PANEL-F6-EXPANSION-1 · EL ALIMENTADOR DE F6 — sonda CONSTRUCTO/HERMANAS sobre instrumentos sin exposición

**SHA de redacción:** `0cdbd72` (`origin/main`, merge de PR #789, re-derivado al abrir el 15/sep/2026 — el encargo llegó pegado en el mensaje de lanzamiento, sin SHA propio)
**Entorno asignado:** NUBE — el encargo lo dice en su primera palabra
**Modelo:** Opus, integral
**Rama:** `claude/ecstatic-curie-70hpwk` (rama de sesión asignada por el entorno remoto)
**Estado:** CONSUMIDO (PR #798)
**Compuerta:** ninguna declarada en el texto
**Llamadas a modelo:** cero, por instrucción explícita («Sin llamadas»)

## ENCARGO (verbatim, tal como se lanzó)

NUBE · ACTO GEN2-PANEL-F6-EXPANSION-1 (Opus, integral) — el alimentador de F6. Sonda CONSTRUCTO/HERMANAS sobre instrumentos sin exposición al desarrollo (la auditoría de exposición que #791 ya probó: milpa + corpus de L + traza-motor; una fuente que afinó reglas no cuenta aunque no se haya evaluado), en los cuatro dominios de M. Objetivo declarado: ≥6 familias retenidas ejecutables con reserva, cada una con los cuatro campos de tu D4. Incluye el paso barato que convierte a MOCIBA en firme (leer los FD 2021/2023 y fijar la batería de denuncia), deja la Enterprise Survey como pregunta a mesa sin resolverla, y entrega al servicio de adquisición la tabla de "qué falta conseguir" por familia — sin escribir en su cola. Parada: cuando la lista nominal llegue a 6+12 o cuando el universo de instrumentos no expuestos se agote, declarado con A.4. Sin llamadas.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «Incluye el paso barato que convierte a MOCIBA en firme (leer los FD 2021/2023 y fijar la batería de denuncia)» | `NO-VERIFICABLE-AQUÍ` — entorno NUBE sin raíz montada (`tools/entorno.py`: `corpus=NO`, `archivos_examinados=0`, `data_raw: configurada=NO`) y red a `inegi.org.mx` en `000` / `CONNECT 403` por política del proxy, con dos intentos y la alternativa (inventarios y `data/reactivos-contexto-*.tsv`) agotada: las etiquetas de `mociba202x` son iguales al nombre de variable en 561 filas, y `reactivos-contexto` tiene 0 filas MOCIBA. `NO-ACCESIBLE-AQUÍ`, **no** `AUSENTE`: el FD 2021 está en manifiesto con `sha256 375bf7c1…` | `R01` sigue RETENIDA y no congelable; el panel no gana la familia que el encargo pedía volver firme. **Compensado en parte:** el mismo paso barato se dio sobre `R09 · ISSP`, donde el inventario canónico sí trae etiquetas, y esa familia quedó con reactivo, universo, ponderador y dominios fijados | `NC-0230` (MOCIBA) y `NC-0231` (ISSP, la codificación que falta) → CAJA/Ubuntu |
| «≥6 familias retenidas ejecutables con reserva» / «la lista nominal llegue a 6+12» | `PARO-PREMISA` — la lista nominal llega a 27 filas y 10 retenidas, pero las ejecutables con reserva siguen siendo 2 y ninguna de las dos se puede congelar desde la nube. Se declara en vez de estirar la lista, por segunda vez | `FP-374` sigue ABIERTA y sin ruta; `F6` no se abre | `NC-0234`; parada por la segunda condición del propio encargo, declarada con A.4 en §4 de la nota de cierre |
| «deja la Enterprise Survey como pregunta a mesa sin resolverla» | Cumplido tal cual: **no se resolvió**. Se registra aquí porque el acto encontró que la misma pregunta ahora gobierna **dos** familias (`R02 · WBES` y `R08 · ENCRIGE`), lo que cambia su precio, no su contenido | Dos familias del dominio TRA, no una, esperan la misma firma | `NC-0233` → mesa |
| Regeneración de `data/adq-demanda-activa-v1_0.json` (proyección derivada del servicio de adquisición) | `FUERA-DE-PERÍMETRO` — el generador corre, pero su salida difiere del árbol en 403/238 líneas y el grueso es deriva de otros actos. Regenerarla atribuiría a este acto trabajo ajeno | Ninguno sobre el ruteo: se hizo en la fuente (`forense/no-corrido.tsv`) y se verificó importando `tools/adq_investigacion.py` — `NC-0230` sale `LISTA_SONDA` / `servicio-gen2-38` | quien regenere la proyección a continuación (cualquier acto del servicio `adq`) |
| Cuestionario de ENCO y segunda ola de ENPOL/ENCRIGE/ENAPROCE | `NO-VERIFICABLE-AQUÍ` (el cuestionario, ya adquirido) y `DIFERIDO-A:` adquisición (las olas) | El dominio `DIN` se queda sin ninguna familia limpia ejecutable | `NC-0232` y `forense/prereg-duelo-v2/F6-falta-conseguir-v1_0.tsv`, filas `R10`, `R11`, `R08`, `R03` |

## CONSUMIDO

PR [#798](https://github.com/Josanoforo/Modelado-Mexicano/pull/798), rama `claude/ecstatic-curie-70hpwk`, abierto el 15/sep/2026 contra `main` — ejecutado por `ACTO GEN2-PANEL-F6-EXPANSION-1` (`ADR-518`; nota `forense/notas/2026-09-15-GEN2-PANEL-F6-EXPANSION-1-cierre.md`). Productos sustantivos: `forense/prereg-duelo-v2/F5-panel-candidatos-v1_2.tsv` (27 filas) y `forense/prereg-duelo-v2/F6-falta-conseguir-v1_0.tsv` (9 filas). Contador de medición: cero. `FP-374` intocada y `F6` sin abrir. El merge pertenece a mesa.
