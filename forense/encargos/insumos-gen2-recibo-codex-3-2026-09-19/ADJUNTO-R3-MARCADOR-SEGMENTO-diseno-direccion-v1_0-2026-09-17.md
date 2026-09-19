# MARCADOR POR SEGMENTO SOBRE EL CATÁLOGO · Diseño de dirección · v1.0
**Dirección (Fable) → mesa · 17/sep/2026 · derivado contra `9eff694` con comando a la vista. Sucede a `MARCADOR-C0-D` (ADR-521-era, 15/sep) bajo `ADR-531` (M1 con alcance precisado) y `FP-383` (el emisor fuera del marcador). Cero cifras nuevas: todo lo que cita ya está sellado.**

---

## 0 · Qué decide este diseño y qué no

Decide qué **es** el marcador por segmento a partir de hoy: qué compara, contra qué piso, con qué estados, qué deriva sin caja y qué exige medir. No decide ningún número, no adjudica ninguna celda, no adopta nada al motor, y no reabre los dos pilotos: los consume.

## 1 · Lo que cambió, con cita

`MARCADOR-C0-D` (`forense/notas/2026-09-15-GEN2-MARCADOR-C0-D-A8-hueco.md` §7) nombró tres prerrequisitos: (i) `θ(x)` computable, (ii) crosswalk firmado, (iii) columna de segmento en `marco-M-sorteado-v1_3.tsv`. Desde entonces:

- **(i) queda superado por `ADR-531`:** la matriz compone, no estima; la `M` de una celda es el estimador que su celda-D adjudicó, y hoy hay dos celdas-D adjudicadas (`ADR-538`, `ADR-542`). `θ(x)` vuelve a importar solo si una celda-D pone a la matriz a competir y ésta gana.
- **(ii) está hecho:** `FP-376` firmada; `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv` — 1 `EQUIVALENTE` (`edad`), 2 `MAPEO-N-A-1` (`localidad`, `formalidad`), 1 `NO-EQUIVALENTE` (`dominio`), 11 `SIN-CORRESPONDENCIA`.
- **(iii) queda sin objeto por `FP-383`:** `ADR-536` midió que 89 de 97 celdas del emisor son copia verbatim del árbitro; el emisor sale de la comparación. El marco del marcador ya no es el marco M sorteado: es la tabla de este diseño. `NC-0300` se cierra por superación, no por ejecución.

`GO-MARCADOR` (`tests/gonogo_marcador.py`, 6/6) sigue acreditando lo que acreditaba — el eje `x = ∅` — y nada de esto.

## 2 · Objetos, nombrados una vez

- **Celda del árbitro:** `(regla, instrumento-ola, eje, categoría)` con `R = (p, IC95)` sellado en `milpa/tramite-ola5-propuesta-v0.yaml` (`_ejes_`, 74 celdas por eje con IC; el censo de `ADR-536` cuenta 97 con las nacionales y compuestas).
- **Celda de cruce:** `(regla, instrumento-ola, eje₁ × eje₂, categoría₁ × categoría₂)`; `R` **no existe** hasta que un piloto lo derive en su COMMIT-3. Es la reserva.
- **Piso:** el estimador que no requiere saber nada de la celda que se evalúa y que cualquier candidato debe vencer. Hay dos, por tipo de celda (§3).
- **Estimador adjudicado:** el `champion_actual` de una celda-D registrada en `data/curacion-registro/celdas-d/` con su `RESULT` sellado; hoy `NINGUNO` en las dos celdas-D adjudicadas.
- **Diagnóstico del emisor:** `|p_nacional(emisor) − R|` por celda. Se muestra; **no** compite (`FP-383`).

## 3 · La regla de los pisos (esto es lo que mesa firma)

**3.1 · Celdas de cruce: el piso es "marginales públicos de la misma ola, sin interacción".** `p̂(a,b) = expit(logit p(a) + logit p(b) − logit p)`, con los marginales **sellados** del árbitro (nunca re-derivados para esto). Dos pilotos en dos dominios lo pusieron primero con MAE 1.47 y 1.57 pp; persistencia, elicitación y "persistencia + interacción" perdieron (`ADR-538` §2, `ADR-542` §2.1). Un candidato entra al marcador en una celda de cruce solo si su celda-D lo adjudicó **contra este piso** con las condiciones `INDECIDIBLE` del programa (`CAREO-ADV-DUELO-diseno-v2:38`).

**3.2 · Celdas marginales: el piso es la persistencia de la ola anterior de la misma serie.** El marginal público de la misma ola **es** `R`: usarlo sería circular. El único piso honesto es `p_{t−1}` del mismo reactivo y el mismo eje (`B-MARCO`, `forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md`). Sin ola anterior sellada por eje, la celda es `SIN-PISO` y **eso es demanda**, no hueco del marcador.

**3.3 · Lo que ningún piso hace:** identificar nada (H5). Un piso no vencido acota a los retadores.

## 4 · La tabla, derivada y no reportada (E.4)

`data/corrida0/marcador-segmento.tsv`, cabecera `# DERIVADO — NO EDITAR`, escrita por `tools/marcador_segmento.py` a partir de: `tramite-ola5-propuesta-v0.yaml` (R), `crosswalk-ejes-arbitro-modelo-v1_0.tsv` (corte del modelo), `data/curacion-registro/celdas-d/*.yaml` + sus `RESULT` (adjudicaciones), `forense/notas/2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv` (IDÉNTICO), y los `RESULT` sellados de pisos de persistencia cuando existan. Una fila por celda:

| columna | qué es |
|---|---|
| `regla · instrumento_ola · ejes · celda` | identidad; para cruces, los dos ejes |
| `tipo` | `MARGINAL` / `CRUCE` |
| `corte_modelo` | veredicto del crosswalk para el eje (o `NO-APLICA`) |
| `R · R_ic95 · n` | del árbitro; para cruces reservados, vacío y `derivado = NO` |
| `piso_tipo · piso · piso_ic95 · piso_fuente` | `PERSISTENCIA(t−1)` con su `CALC`, o `MARGINAL-SIN-INTERACCION` con los marginales citados |
| `adjudicado_id · adjudicado_valor · adjudicado_ic · incertidumbre_tipo` | la celda-D que lo adjudicó, o `NINGUNO` |
| `skill` | `1 − |err_adj| / |err_piso|` solo si hay adjudicado y R; si no, vacío |
| `emisor_p · emisor_diag` | diagnóstico `|p_nacional − R|`; `IDENTICO` si el censo lo marcó así |
| `estado` | `EVALUADA` (R + piso + adjudicado) · `SOLO-PISO` (R + piso, ningún retador) · `SIN-PISO` (R, ninguna ola anterior por eje) · `RESERVADA` (cruce, R no derivado) · `CONSUMIDA-SIN-PILOTO` (cruce cuyo R alguien vio; `NC-0328`) · `EMISOR=ARBITRO` (diagnóstico, no comparación) |
| `universo` | SHA y archivos de la derivación (A.10) |

**Lo que el marcador reporta del programa, en tres números derivados:** `celdas_con_piso / celdas_del_arbitro` (cobertura), `celdas_con_valor_anadido / celdas_evaluadas` (dónde un candidato vence al piso), y la lista `SIN-PISO` (la demanda de pisos, por instrumento y eje). Hoy, sin medir nada nuevo: cobertura de cruces 2/2 evaluadas con adjudicación `NINGUNO`; marginales con piso por eje: **0 de 74** (`ADR-536`: 0 celdas `MISMO-INSTRUMENTO-OTRA-OLA`); valor añadido: **0 de 2**. Es la foto honesta, y es la que el informe cita.

## 5 · Qué se deriva sin caja y qué exige caja

- **Sin caja (nube, cero mediciones):** la tabla completa con `R`, cortes, adjudicaciones, diagnóstico del emisor y estados; los pisos de cruce para las dos celdas-D ya adjudicadas (ya sellados en sus `CALC`); las 74 marginales en `SIN-PISO` salvo que un `CALC` sellado traiga `p_{t−1}` por eje.
- **Con caja (mediciones, cadena GEN2):** los pisos de persistencia por eje: para cada entrada `_ejes_` con serie (ENVIPE anual: `evasion_norma`, `denuncia.con_seguro`; ENCIG 2023: `gobierno_digital`; ENIF 2021: `via_informal`, `horizonte_corto`), los marginales `p_{t−1}` por eje con IC — spec congelada antes del dato, códigos por **texto** entre olas (lección `P5_6`/`P5_7`), un `CALC` por instrumento. Es la primera tanda de medición que el marcador pide, y es barata.

## 6 · Reservas

Toda celda de cruce nace `RESERVADA`. Sale de ese estado **solo** por un piloto celda-D con COMMIT-3, o entra a `CONSUMIDA-SIN-PILOTO` por declaración. Hoy: `localidad × edad` (ENIF 2024) consumida por piloto; `escolaridad_proxy × dominio` (ENVIPE 2025) consumida por piloto; `edad × dominio` (ENVIPE 2025) consumida sin piloto (`NC-0328`). Las demás combinaciones de las siete entradas `_ejes_` siguen reservadas; la tabla las lista para que nadie las "verifique" por curiosidad.

## 7 · Guardias (D-14: solo las que atrapan un defecto que ya ocurrió)

1. **`T-RESERVA`:** ninguna fila `RESERVADA` tiene `R`; falla si alguien escribe un valor en un cruce sin `CALC` de COMMIT-3. Defecto medido: 17/sep, script exploratorio.
2. **`T-EMISOR-NO-COMPARA`:** ninguna fila con `emisor_diag` derivada de una celda `IDENTICO` tiene `skill`. Defecto medido: 89/97.
3. **`T-PISO-NO-CIRCULAR`:** ninguna celda `MARGINAL` tiene piso `MARGINAL-SIN-INTERACCION`. Defecto concebible pero a un `copy-paste` de distancia del piloto: se instala porque cuesta una línea.

## 8 · Lo que el informe puede citar a partir de esto

Que el programa tiene un marcador por segmento **derivado**, con 97 celdas del árbitro, dos evaluadas, cero con valor añadido, 74 sin piso — y que el estimador por celda que gana donde se ha probado es el más barato que existe. Que el emisor es el árbitro con otro nombre y por eso no compite. Y que lo que falta es medible: pisos por eje.

## 9 · Lo que va a mesa (firma propuesta)

> "FIRMA DE MESA — marcador por segmento: (1) el marcador se deriva sobre el catálogo y las celdas-D, nunca sobre el emisor; el emisor aparece como diagnóstico. (2) Piso por defecto en celdas de cruce: marginales públicos de la misma ola sin interacción; en celdas marginales: persistencia de la ola anterior por eje; sin ola anterior, la celda es SIN-PISO y es demanda. (3) Todo cruce nace RESERVADA y sale solo por piloto con COMMIT-3. (4) Tres guardias: T-RESERVA, T-EMISOR-NO-COMPARA, T-PISO-NO-CIRCULAR. (5) NC-0024/0076/0239/0300 cierran por superación con este diseño como cita."

## 10 · Sucesores (dos encargos, en ese orden)

- **`GEN2-MARCADOR-REDISENO-1` (nube, Opus, cero mediciones):** `tools/marcador_segmento.py`, la tabla derivada, las tres guardias, `GO-MARCADOR` extendido con la distinción "eje `x = ∅`" vs "por segmento" escrita en su salida, cierre de las cuatro NC, nota. Perímetro sin archivo común con caja.
- **`GEN2-PISOS-PERSISTENCIA-1` (caja, Opus, mide):** los `p_{t−1}` por eje para las entradas con serie, un `CALC` por instrumento, cadena completa, registro en la vista en el mismo acto (regla de `ADR-540`); cierra la mayor parte de `SIN-PISO`.

## 11 · Universo (A.10) · contador · auditoría

SHA `9eff694`; fuentes: `tramite-ola5-propuesta-v0.yaml`, crosswalk, censo de `ADR-536`, notas de cierre de los dos pilotos, `tests/gonogo_marcador.py`. **Contadores movidos: cero** — es diseño. **Auditoría (acotada — este diseño afirma sobre el modelo, no sobre México):** no confunde estructura con cultura porque no interpreta; el sesgo de clase entra por el árbitro (universos restringidos como `formalidad` sobre quien trabaja) y la tabla lo lleva en `n` y `universo`; ninguna afirmación sobre el estado del corpus está tecleada — 74, 97, 89, 1/2/1/11, 0 de 74 y 0 de 2 traen su comando o cita; escala: proporción en todo objeto; ninguna comparación cruza escalas. **Lo que sería peligroso leer simplista:** "0 de 2 con valor añadido" como "el modelo no sirve" — dice que en dos celdas nadie venció al piso más barato, y que ese piso ya es un estimador por celda utilizable.
