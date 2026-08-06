# AUDITORÍA DE PREMISAS DE LO SELLADO · sin el halo de "cerrado = canon"
### v1.0 · 7/ago/2026 · mesa Fable contra `origin/main = aa87828` · encargo directo del usuario

## §0 · Qué estuvo mal en mi afirmación anterior, dicho primero

Ayer escribí "los sellos aguantan" tras correr **una sola receta de grep** (frases de disponibilidad) sobre el registro de veredictos. Eso no audita premisas: audita vocabulario. Y confundí dos cosas distintas: el mecanismo **append-only** (que protege la historia — nadie reescribe) con una **garantía epistémica** (que nadie otorgó — el mismo proceso que selló esos veredictos produjo los ~16 "no existe", el CUBIERTA=0 y el espejo desfasado). Este documento repite el examen con el lente correcto: cada artefacto sellado o calculado, contra las cinco clases del gap, con evidencia derivada, y con la columna **NO-VERIFICADO** en vez de bendiciones para lo que no leí.

Nota previa indispensable: **las letras A–E no son una semántica global** — cada ficha declara su propia escala (B-bis). Un `D` de R4.1 y un `D` de R7.2 no significan lo mismo; el examen es por ficha, contra la definición textual de su fila.

## §1 · El lente — las cinco clases del gap

(a) cierre negativo sin universo declarado ("no existe" cuando era NO-ENCONTRADO / NO-ACCESIBLE / nadie-corrió-el-mecanismo) · (b) restricción supuesta y jamás medida · (c) integridad del corpus (truncación, carrera de registro, payload fuera del corpus, identidad por nombre) · (d) encontrado-por-búsqueda ≠ verificado byte a byte, incluidas cadenas de prensa · (e) contabilidad del programa sobre sí mismo. La clase (e) **sí alcanzó ADRs**: ADR-51 existe porque ADR-50 traía "29 = 14+15" y eran 22 = 7+15 — el aparato se auto-corrigió una vez; no hay razón para asumir que fue la única.

## §2 · Hallazgo transversal, derivado — clase (c): ninguna medición consumió los bytes dañados

```
grep -rln "envipe_2023_bd_envipe_2023\|endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf" forense/notas/ tests/ milpa/
→ 5 archivos, TODOS diagnóstico/reparación (map1b, int1, crc, repair1, map2). Cero corridas. Cero en milpa/. Cero en tests/.
```
Los tres payloads afectados se registraron el 5/ago 19:05 y ningún acto de medición los abrió antes de que la capa de integridad los atrapara. Las condicionales y G4 corrieron sobre **ENVIPE 2025** (íntegra, 72/76 payloads de la familia); conf.06 sobre ENCUCI con spec congelada pre-DBF. **La contaminación de clase (c) sobre resultados sellados es, hoy y derivado: cero.** Esto es un hecho del grep, no un acto de fe — y es re-derivable en un comando.

## §3 · Los 14 registros de veredicto, uno por uno

| Regla | Letra | Premisa de carga (textual, derivada) | Exposición | Estado |
|---|---|---|---|---|
| `R5.1` | A | Reserva verbatim Nota 16: **"ENIGH es corte transversal repetido, no panel… control limitado a tercil… `P040` no distingue donante familiar… cobertura no es 100%"** — cuatro reservas de diseño escritas; adjudicado por decisión de mesa ADR-58(c) | diseño, con alternativa superior YA redactada (DiD/ENASEM, rama #139 viva) | **EL MÁS EXPUESTO de los sellados.** Las decisiones D1/D2 de #139 dejan de ser trámite de rama: son el re-examen de fondo de este sello |
| `R5.2` | A | Reserva verbatim Nota 18: el punto satisface la fila **"pero el IC95% no despeja el umbral"** (23.98%, IC [14.39, 33.57] vs 20) | estadística, declarada | RESERVA-ESCRITA — voltearía: re-corrida con más poder (otra ola ENUT) si existe |
| `R1.2` | E | "no-satisfacción **decisiva y limpia** del falsador" — 42.98% IC [39.88, 46.08] contra umbral 15 | ninguna de las cinco toca la pierna medida | SÓLIDO en lo medido |
| `R1.3` | E | Pierna medida decisiva (3.86% IC [3.23, 4.48] vs 10; brecha 2.98pp) **+ pierna 3 "inconstruible": "ni CNBV publica canal de alta"** | pierna 3 = clase (a): ¿se sondeó CNBV/CONDUSEF o se leyó de catálogo? | PARCIAL — ASIGNA-1b sondea al regulador; si el canal existe, la acotación cae y la condición 3 se corre |
| `R1.1` | D | Bloque contiene "ninguna fuente / no existe"; y el cruce v2_0:47 declara **su propio hueco: "no se buscó específicamente… AGROASEMEX"** | clase (a) con reserva autodeclarada | **EXPUESTO** |
| `R4.1` | D | z4: "la fila `D` de la propia ficha se satisface: **'si no existe medición de trato percibido'**" — la letra es un condicional cuyo antecedente es un claim de disponibilidad; cruce:73 añade SINERHIAS sin verificar a instrumento | clase (a) por construcción de la ficha | **EXPUESTO** |
| `R9.1` | D | Misma nota z4; el claim es "la variable no existe **dentro** del instrumento poseído" (verificado por Encargo Z Nota 20) | distinta: diseño de cuestionario, no del mundo. Pendiente: ¿Nota 20 abrió el cuestionario/microdato o leyó documentación? | NO-VERIFICADO el método — receta: `grep -n -A6 "Nota 20" forense/hitoD-preregistro-v2_0.md` |
| `R4.3` A y B | D·D | z5: fila D se satisface "letra por letra: **'si solo hay adherencia auto-reportada'**" (`A0313`) | clase (a) por construcción — aparecer adherencia no-autoreportada voltea el antecedente | **EXPUESTO** (ambas mitades) |
| `R9.2` | D | z6: el Umbral exige verificación **"por fuente independiente"** ausente; cruce:102 ya nombra a Cero Desabasto "prometedora, no resuelta" | clase (a)+(d) | **EXPUESTO** |
| `R4.2` | D | y4 no usa lenguaje de disponibilidad en lo grepeado; trae además una nota de infraestructura propia: el zip `adultos_ensanut2024_w.csv.csv.zip` "no contiene microdato de fila-po…" (declarada "no cambia el veredicto") | por caracterizar | NO-VERIFICADO — leer y4 completo: `sed -n '1,60p' forense/notas/2026-08-04-y4-veredicto-r4-2.md` |
| `R7.2` | D | Registro solo apunta a Notas 11/12; R5.2 cita "la corrida **limpia** de R7.2" como benchmark — un D con corrida limpia merece leerse contra la fila D de SU escala (¿pre-ADR-58, sin fila de sobrevivencia?) | posible fila-forzada por escala vieja | NO-VERIFICADO — leer Nota 11/12 en el preregistro |
| `R3.1` | B | Nota 28; corrida completa "seis cómputos, brechas 9.28–32.73pp sin traslape de IC95%" (Nota 27) | pinta medida y decisiva | NO-VERIFICADO en detalle — no la certifico sin leerla |
| `R3.2` | B | Solo puntero a Nota 6 (29/jul, de las tres primeras, escala más vieja del programa) | por caracterizar | NO-VERIFICADO |

**Patrón que emerge y que el sello ocultaba:** varios `D` del lote del 4/ago son, **por construcción de sus propias fichas, condicionales sobre disponibilidad** ("si no existe X → D"). Fueron honestos bajo el universo de ese día; el gap demostró que ese universo era una puerta de un portal. El barrido ASIGNA puede voltear antecedentes — y con ellos, letras, por la vía limpia: corrida nueva appendizada.

## §4 · Lo demás calculado, mismo lente

- **ID-X / ficha ID-G3.** Datos abiertos byte a byte, íntegros hoy, spec congelada pre-dato, script committeado, cero clases (a)-(d) en la letra. **Retiro mi frase "muere con honra" y la reemplazo por el número:** el peor escenario del barrido S2 da 1.237 contra 1.25 — **margen vinculante 0.013 — sobre un supuesto de conglomerado (ICC) que el propio barrido declara no poder estresar, con UPM sin confirmar como columna** (§9 de la corrida, reverificado). No es clase-gap: es carga de supuesto, delgada y declarada. Si el censo v1.1 o la documentación entregan la columna UPM real, el re-estrés cuesta minutos y es lo único que podría acercar el gate a alcanzable. La honra la decide mesa leyendo 0.013, no yo adjetivándola.
- **G4 y condicionales (9).** ENVIPE 2025 íntegra (§2); universo seleccionado y techo ya rotulados por A-bis/ADR-57 — su exposición es la que sus propias entradas declaran, ninguna nueva.
- **conf.06 / ADR-64.** Spec congelada antes de abrir el DBF; además REPARÓ un defecto clase (e). Sólido.
- **Censo de estimabilidad.** **No es un sello** — se autodeclara "etiqueta de censo, no compuerta" (línea 21). Sus **9 SIN-RUTA** son cierres negativos cuyo universo fue "el corpus citable hoy" o "los cinco instrumentos del régimen" — universos declarados pero angostos, pre-gap. Dos (`sens_estatus`, `aversion_riesgo`) tienen la búsqueda cerrada **por ADR** (52A/54): reabrirlos exige decisión de mesa, no solo censo. Los otros siete se reabren gratis en v1.1. De lo más barato y rendidor del re-examen.
- **`milpa/tramite.yaml:77`** — "CoDi = 3.09M" en una `nota_validacion` del ejecutable es **cadena de prensa (clase d) dentro del motor**, ya rastreada por #149 a Cobertura360. MED-R3.4 la reconcilia contra primaria; hasta entonces es un número de prensa en el motor y así debe leerse.
- **Gate ADR-37 / R3.4.** Su ficha porta la discrepancia sin resolver de forma explícita — expuesta por diseño, que es lo correcto.
- **ADRs de decisión (49–54, 57, 58, 60, 61).** Codifican decisiones y análisis internos; su exposición dominante es (e), y el precedente ADR-50→51 demuestra que puede alcanzarlos. No los certifico en bloque: cualquier cifra empírica citada dentro de un ADR hereda la clase de su fuente.

## §5 · Cola de re-examen, priorizada por exposición × contador

1. **R5.1 ↔ #139** — mesa Opus resuelve D1/D2 sabiendo que NO es limpieza de rama: es el re-examen del sello más cargado. La opción "corrida DiD/ENASEM appendizada que supersede en autoridad sin borrar el A" existe y es la honesta.
2. **R1.1** — ASIGNA-1b sondea AGROASEMEX/padrón con nombre y apellido (el hueco es autodeclarado).
3. **R4.1, R4.3(A,B), R9.2** — antecedentes de disponibilidad al barrido: SINERHIAS a nivel instrumento; adherencia no-autoreportada; Cero Desabasto/campañas.
4. **R1.3 pierna 3** — CNBV/CONDUSEF sondeados de verdad, no leídos de catálogo.
5. **Censo SIN-RUTA ×9** — v1.1 (siete gratis; dos vía decisión de mesa por ADR-52A/54).
6. **Los 5 NO-VERIFICADOS de §3** (R4.2, R7.2, R9.1-método, R3.1, R3.2) — una lectura de nota cada uno, receta incluida; en particular R7.2: si su D fue fila-forzada por escala pre-ADR-58, la corrección es un addendum de re-rotulación, no una corrida.
7. **ID-X re-estrés ICC** — solo si aparece la columna UPM; minutos.
8. **tramite:77** — ya en la ruta de MED.

## §6 · Reglas del re-examen — para que corregir no repita el defecto

Nueva corrida = espec congelada en commit propio antes de abrir dato, resultados en el segundo, sello viejo intacto como historia con su re-rotulación appendizada al lado. **Prohibido "confirmar" un sello viejo ajustando la corrida nueva hacia él** — una cifra que se fuerza a cuadrar es el defecto que este aparato existe para atrapar, y aplica igual cuando lo que se quiere cuadrar es el pasado propio.

---
**CONTADOR: cero, y declarado.** Este artefacto no mueve mediciones: mueve la lista de qué mediciones siguen debiendo su premisa.
