ENCARGO · ACTO MAESTRA38-N18 · S6/S7-L16/L17 v1.1 CON PONDERADOR — invoca /acto

Ejecutor: Sonnet, patrón del encargo N7 anterior (búscalo en forense/encargos/ para copiar formato), se ejecuta DESPUÉS de TRAMITE-5.

Crear forense/prereg-caja/S6-L16-spec-v1_1.md (+ archivo .sha256 con el hash del .md) como copia de la spec v1.0 existente (busca forense/prereg-caja/S6-L16-spec-v1_0.md o similar) con la sección §1.3 reescrita para declarar:

- Universo de bx = subpoblación respondida por proxy (miembros ausentes), declarado explícitamente como subpoblación (referencia A-bis 4), nunca comparado contra un marginal poblacional general.
- Ponderador: fac_3b_px (fuente: ennvih1_2002_ponderador, archivo ehh02w_all/ehh02w_bx.dta), con llave folio/ls normalizada a entero antes del join (nota: sin normalizar, todos los joins dan 0 — esto viene de una nota de C1, verifícalo si puedes).
- La rama directa b3b usa fac_3b (sin _px) y se reporta POR SEPARADO de bx — nunca agrupados, porque b3b usa la etiqueta "SERIO" y p_es/bx usa "GRAVE".
- Verificación de consistencia obligatoria antes de correr: sobre las filas de p_es.dta con es09 no nulo, n_no_nulo_gt0 de fac_3b_px debe ser ≥ el de fac_3a_px y fac_4_px; si no se cumple, la asignación libro→factor es incorrecta y el proceso se PARA (documentar esto como un chequeo explícito en la spec, con el comando/pseudocódigo de verificación).
- Fila B-bis, y "se_mueve_si" copiado verbatim de la fila 2 de SELLO-2 (busca ese documento en el repo).

Deja v1.0 intacta (no la borres ni modifiques). Si existe una spec S7-L17 con rama A que use el mismo libro/proxy (b3b/ES), crea también forense/prereg-caja/S7-L17-spec-v1_2.md con el mismo tratamiento; si su rama A usa un libro distinto, NO la toques y dilo en el commit.

Actualiza el contador de specs en el tablero si existe ese conteo (era 21, pasa a 22 o 23 según cuántas specs nuevas creaste).

PERÍMETRO permitido: forense/prereg-caja/ (spec nueva + .sha256), tablero (recibo), notas, A.3, cascada de ADR si aplica. NO TOCAR: milpa/**, canon/ (salvo cascada estrictamente necesaria), tests/*.py, tools/*.py, cron, data/curacion-registro/** (fuera de perímetro de este acto — ya tocada por TRAMITE-5).

## CONSUMIDO

**Renumerado a `ACTO MAESTRA38-N19` al ejecutar**: el rótulo `MAESTRA38-N18` que este encargo invoca ya está censado en `canon/registro-rotulos.tsv` por `ACTO MAESTRA38-N18` (fusionado, `PR #573`, la spec `S7-L17` v1.1 sobre el mapeo `a0927` — un acto de asunto completamente distinto que tomó el mismo número) — colisión de rótulo, regla de la casa: quien fusiona segundo renumera. Ejecutado como `ACTO MAESTRA38-N19`, 7/sep/2026, entorno **NUBE sin corpus** (`data/raw` ausente, verificado), sobre `origin/main` tras el commit de `ACTO MAESTRA38-TRAMITE-5` en esta misma rama.

**Spec nueva.** `forense/prereg-caja/S6-L16-spec-v1_1.md` (+ `.sha256`, `7a0120a3…`), copia de `S6-L16-spec-v1_0.md` (`v1.0` intacta, `sha256` re-verificado sin cambio: `317e42c3…`) con §1.3 reescrita íntegra y §0 ganando un `§0.4` que cita la razón del cambio (`ADR-357`, `FP-328`(a)/(c), `ACTO MAESTRA38-C1`). Las cinco piezas pedidas, verificadas contra el repo real, no supuestas:

1. **Universo de `bx` como subpoblación, `A-bis 4`.** Citado verbatim: `instrucciones-proyecto-v2_12.md`, Bloque A-bis, regla 4 — *"Un estimando restringido a una subpoblación no se compara contra uno poblacional… Se recalcula el marginal restringido al mismo universo, o se declara el resultado como acotado a esa subpoblación."* El libro `bx` (`p_portad.dta`, 1 903 filas) es el libro **Proxy** de `ENNVIH` — lo responde un informante en nombre de miembros ausentes del hogar, no el universo completo (8 441 filas del libro `C`). Declarado explícitamente acotado, nunca reconciliado contra un marginal general.
2. **Ponderador `fac_3b_px`.** Fuente `ennvih1_2002_ponderador` (`data/manifiesto.yaml`), archivo `ehh02w_all/ehh02w_bx.dta` — exactamente el archivo que el encargo cita. Adjudicado con la evidencia de `data/ennvih2002-ponderadores-candidatos-v1_0.tsv` (`ACTO MAESTRA38-C1`, pieza (h)): `n_no_nulo_gt0` = 21 645 para `fac_3b_px`, 21 631 para `fac_3a_px`, 9 037 para `fac_4_px` — `fac_3b_px` es el mayor de los tres. Llave de join `folio`, normalizada a entero antes de unir: **verificado que la nota es de `C1`, verbatim en la cabecera de esa misma tabla** — *"En `ehh02w_all.zip` `folio` es cadena con ceros a la izquierda (`'00001000'`) y en el microdato es `float64` (`2000.0`): sin normalizar, TODOS los joins dan 0."* Con la llave normalizada, `C1` midió 1 903/1 903 filas resueltas — cifra que esta spec cita, no re-corre.
3. **`b3b` reportado por separado, con `fac_3b` (sin `_px`).** Verificado: `fac_3b` vive en `ehh02w_all/ehh02w_b3b.dta`, etiqueta "FACTOR DE EXPANSIÓN LIBRO 3B" (distinta de "FACTOR DE EXPANSIÓN LIBRO PROXY" de los tres candidatos `_px`), `n_no_nulo_gt0` = 19 809 — archivo, etiqueta y cobertura de universo distintos de `fac_3b_px`. Confirmado también contra `S6-v1.0 §1.1`: el módulo `b3b` (`iiib_es.dta`) trae la etiqueta "SERIO" en las tres olas; solo el módulo `bx` (`p_es.dta`) trae "GRAVE" en 2002/2005 — exactamente la distinción letra por letra que el encargo describe.
4. **Chequeo de consistencia, con pseudocódigo real.** Escrito como cláusula obligatoria de §1.3 (`pyreadstat`, join por `folio` normalizado, `assert n_3b_px >= n_3a_px and n_3b_px >= n_4_px`). **Verificado contra las cifras reales que `C1` ya midió sobre el libro `bx` completo** (no sobre el subconjunto exacto `es09` no nulo, que este acto NUBE no puede abrir): la desigualdad se sostiene (21 645 ≥ 21 631 ✔, margen de solo 14 observaciones; 21 645 ≥ 9 037 ✔, margen amplio) — declarado en la spec como el estado más cercano disponible, con la advertencia explícita de que el margen estrecho contra `fac_3a_px` puede invertirse en el subconjunto restringido, y que si se invierte, el proceso se PARA de verdad, no en principio.
5. **Fila B-bis, `se_mueve_si` de "fila 2 de SELLO-2" — NO ENCONTRADA, declarado, no fabricada.** Verificado antes de escribir: `forense/encargos/2026-09-07-MAESTRA38-SELLO-2.md`, su propia sección `## CONSUMIDO`, declara **"Bloque B (filas 2-5, benchmark): NO ejecutado"**. Ninguna fila 2 de `SELLO-2` existe en prosa en este repo — ni en `canon/gobernanza-v1_15.md` (`ADR-363` cubre solo fila 1 y fila 6, "dos incisos"), ni en `milpa/tramite-ola5-propuesta-v0.yaml`. Lo más cercano que el repo mide sobre "`SELLO-2 §B`" es de `ACTO MAESTRA38-LOTE-CRUCE` (`ADR-371`, `FP-329`): tres cláusulas (`R7.7`, `R7.6` brazo proximidad, `R10.3`) condicionadas a `clien1n`/`clien1na`, que no se pueden disparar porque esas variables no existen en LAPOP 2021/2023 — pero son de una regla completamente distinta (cívico, no salud/`R4.4`). **No hay texto verbatim aplicable a copiar.** La spec declara esto explícitamente (§5) y, en su lugar, redacta una `se_mueve_si` propia para la fila B-bis basada en el propio chequeo de consistencia (punto 4), marcada sin ambigüedad como NO-verbatim.

**S7-L17 v1.2 — NO creada, con motivo verificado.** Se leyó `forense/prereg-caja/S7-L17-spec-v1_1.md` completa (la única versión de `S7` con rama A activa hoy). Su Rama A **no** usa el libro/proxy `bx` — usa el libro directo `b3b` (`ce19d_2`/`hs16d_2`, archivo `ehh02w_all/ehh02w_b3b.dta`, ponderador `fac_3b` sin `_px`), y el propio texto de `S7-L17 v1.1 §1.1` lo dice explícitamente: *"libro `bx` no aplica aquí (esta rama no usa `p_es.dta`)"*. Como el encargo instruye ("si su rama A usa un libro distinto, NO la toques y dilo en el commit"), `S7-L17` **no se toca**. Ningún `v1.2` de `S7-L17` se crea.

**Contador de specs — discrepancia de premisa, valor real usado.** El encargo asumía un contador "era 21, pasa a 22 o 23". Verificado contra el tablero real (`grep -n "specs de caja\|specs selladas" forense/tablero/TABLERO-PROGRAMA.md`): el último conteo explícito registrado es *"specs de caja `8 → 9`"* (recibo de `MAESTRA38-N15`, línea 789) — no existe ningún "21" en el tablero. Contando archivos reales en `forense/prereg-caja/` (excluyendo `.sha256`): 12 antes de este acto (`S1`–`S11`, con `S7` teniendo `v1.0`+`v1.1`), 13 después (se suma `S6-L16-spec-v1_1.md`). Contando **números de spec distintos** (`S1`–`S11`, sin contar versiones): 11 antes, 11 después — `v1.1` es una nueva versión de un `S`-número ya existente, no un `S`-número nuevo, mismo criterio que ya aplicó `S7-L17 v1.1` (que tampoco incrementó ningún contador de specs al fusionarse, verificado: su propio recibo en el tablero no toca ningún contador de "specs de caja"). **No se inventa el "21 → 22/23" que el encargo citaba** — se declara la discrepancia y se usa el valor real (12 archivos → 13; 11 números de spec → 11, sin cambio).

**Tablero.** Recibo añadido en `forense/tablero/TABLERO-PROGRAMA.md` (ver más abajo, sección propia).

**Cascada.** `ADR-374` (candidato, `python3 tools/cierre_acto.py` re-derivado tras el commit de `TRAMITE-5`) en `canon/gobernanza-v1_15.md §4`. `canon/estado-programa-v1_12.md` L0 + línea 27 (373 → 374). `canon/registro-rotulos.tsv`: censado `MAESTRA38-N19` (y no `MAESTRA38-N18`, por la colisión declarada arriba).

**Suite.** `python3 tests/check.py --baseline`: mismo estado que dejó `TRAMITE-5` — **1 FAIL declarado** (`T22`, `FP-330`, gap de `_T22_ARCHIVOS_CONOCIDOS` sobre el nombre consolidado del tablero, `tests/*.py` fuera de perímetro de ambos actos de esta rama). Sin FAIL nuevo respecto de ese estado.

**A.8 · `tools/ya_medido.py` — apéndice del ejecutor, NO parte del texto verbatim** (este archivo cita `R4.4` — la regla de la spec — y, al discutir por qué la fila `B-bis` no puede copiar `SELLO-2` verbatim, cita también `R7.7`/`R7.6`/`R10.3`, las tres reglas del hallazgo de `LOTE-CRUCE`; T-YAMEDIDO exige la salida pegada para cualquier `R-n` citado):

```
$ python3 tools/ya_medido.py R4.4
=== ya_medido: R4.4 ===
  resuelto por canon: R4.4 -> id salud.atencion.grave
  ... (S6/L16, MAESTRA38-LOTE-ENSANUT, canon/registro-rotulos.tsv:189 L MAESTRA38-L16)
========================================
MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-ENSANUT-resultados.md, S6

$ python3 tools/ya_medido.py R7.7
=== ya_medido: R7.7 ===
  ... (canon/registro-rotulos.tsv:193 S MAESTRA38-SELLO-2 [CORROBORADA])
========================================
MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md, L12, L9, MAESTRA38-SELLO-2

$ python3 tools/ya_medido.py R7.6
=== ya_medido: R7.6 ===
  ... (canon/registro-rotulos.tsv:197 N MAESTRA38-LOTE-CRUCE)
========================================
MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md, 2026-09-07-MAESTRA38-CARGA-LAPOP-2-spec.md, L11, L12, L2, L4, L9, S4, canon§7

$ python3 tools/ya_medido.py R10.3
=== ya_medido: R10.3 ===
  ... (canon/registro-rotulos.tsv:192 N MAESTRA38-N17)
========================================
MEDIDA-EN: L18
```

Las cuatro salen `MEDIDA-EN:` — ninguna sorpresa: este acto no mide ninguna, solo las cita como contexto de por qué la fila `B-bis` no puede copiar `SELLO-2` verbatim (`R7.7`/`R7.6`/`R10.3`, hallazgo de `LOTE-CRUCE`) y para qué regla existe la spec (`R4.4`). Medición de este acto: **cero**.

**Perímetro respetado.** Tocado: `forense/prereg-caja/S6-L16-spec-v1_1.md` (nuevo), `forense/prereg-caja/S6-L16-spec-v1_1.sha256` (nuevo), `forense/tablero/TABLERO-PROGRAMA.md`, `canon/gobernanza-v1_15.md` (ADR-374, cascada), `canon/estado-programa-v1_12.md` (L0 + línea 27, cascada), `canon/registro-rotulos.tsv` (censo, cascada), `forense/encargos/` (A.3). No tocado: `milpa/**`, `canon/modelo-decision-v4_0.md`, `data/curacion-registro/**` (fuera de perímetro de este acto — ya tocada por `TRAMITE-5`), `tests/*.py`, `tools/*.py`, `cron`, `forense/prereg-caja/S6-L16-spec-v1_0.md` (intacta), `forense/prereg-caja/S7-L17-spec-v1_1.md` (intacta, motivo declarado arriba). Medición de México: cero.
