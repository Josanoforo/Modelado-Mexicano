ADENDA · ACTO GEN2-RELEVO-USOS-1 · REGLA DE ADOPCIÓN EN BLOQUE

CABECERA DE ARCHIVO (A.3 / `forense/encargos/convencion.md`) — la escribe el acto que archiva, **no** es texto de dirección. El texto de dirección va íntegro abajo, verbatim, bajo la línea `PIEZA DE DIRECCIÓN`.

- **SHA de redacción** — archivado contra `582d4e9` (`origin/main`, merge de `PR #779`, `ACTO GEN2-MEDICION-DEMANDA-1`), 0 commits detrás en el momento del archivo.
- **Entorno asignado** — no lo fija esta pieza: hereda el del `ACTO GEN2-RELEVO-USOS-1`, cuyo encargo **todavía no existe en el árbol** (ver A.8 (2) abajo). Esta adenda **no** es un encargo despachable por sí sola y por eso **no** va a `forense/encargos/cola/`: gobierna el `P4` de otro acto.
- **Estado** — `VIVO`.
- **Compuerta que la propia pieza declara** — «aplica en cuanto abra tu compuerta de `P4`, el merge de `FIRMAS-MESA-1`». Ninguno de los dos rótulos existe hoy en el árbol; la pieza llega **antes** que el acto que gobierna.
- **Procedencia del texto** — archivo entregado por mesa en la sesión de la nube del 15/sep/2026, `sha256 = 23ad347ecaffb2bc9dde008837c478cc7e939549676ce487a366f3fb774b31aa` (4 898 bytes, 31 líneas). Se copia **verbatim**: sin resumir, sin corregir, sin reordenar.
- **Rótulos censados en `canon/registro-rotulos.tsv` por este archivo** — ninguno. `GEN2-RELEVO-USOS-1`, `FIRMAS-MESA-1` y `SELLA-3` no son de la serie `MAESTRA<nn>-<letra><n>` que `/encola` §3 censa, y la casa censa el rótulo de un acto **al cerrarlo**, con su ADR y su PR — no al encolar su instrucción. Censarlo aquí declararía un habitante que todavía no vive.

VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2 — contestada por quien archiva, contra `582d4e9`, con comando):

**(1) ¿Existe ya la estructura?** SÍ, completa, y la pieza no inventa ninguna pieza de maquinaria:

```
$ ls data/corrida0/demanda-resultados.tsv data/corrida0/decisiones.tsv milpa/procedencia.yaml forense/hallazgos.md
data/corrida0/decisiones.tsv   data/corrida0/demanda-resultados.tsv
forense/hallazgos.md           milpa/procedencia.yaml
$ python3 tools/corrida0.py delta --help | head -2
usage: corrida0 delta [-h] --entrada PARES.yaml [--formato {humano,json,tsv}]
                      [--salida-dir DIRECTORIO]
```

`corrida0 delta` **está implementado** y ya pide exactamente el contrato que la regla exige («contrato `GEN2-DELTA-1` con ambos objetos, uso y comparabilidad» = «hashes, uso y contrato explícitos — nunca a mano»). Discrepancia **no material** declarada, no corregida aquí (fuera de perímetro): la cabecera de `tools/corrida0.py` sigue listando `delta` y `vigencia` como declarados y vacíos, a la espera del `ACTO GEN2-E7`, texto que el propio árbol contradice. `demanda-resultados.tsv` trae hoy **207 slots** (209 líneas − cabecera `# DERIVADO — NO EDITAR` − fila de columnas), con `consumidor`, `valor_legacy`, `escala_legacy`, `clase_legacy`, `corrida_natural`, `estado`, `vigencia` y `validacion_independiente` ya como columnas. `decisiones.tsv` tiene las cuatro columnas (`objeto`, `decision`, `fuente`, `fecha`) que el paso 1 de PROPAGACIÓN usa.

**(2) ¿Existe ya el contenido?** NO, en las dos direcciones que importan, y por eso esto se archiva en vez de ejecutarse:

```
$ grep -rl "RELEVO-USOS" --include=*.md --include=*.tsv --include=*.py .   # 0 líneas
$ grep -rl "FIRMAS-MESA-1" . | grep -v '^\./\.git'                        # 0 líneas
$ grep -n "PARA-v2.14" forense/hallazgos.md                               # 0 líneas
```

Ni `ACTO GEN2-RELEVO-USOS-1` ni `FIRMAS-MESA-1` existen en el árbol: no hay `P4` que propagar ni compuerta que pueda abrirse hoy. `PARA-v2.14` tampoco existe todavía — `instrucciones_vigentes` es v2.13, entregada íntegra el 8/sep/2026 (`ACTO GEN2-V213`), y la última serie acumulada, `PARA-v2.13`, quedó absorbida por esa entrega. La entrada `PARA-v2.14` que pide el paso 2 de PROPAGACIÓN sería la **primera** de su serie.

**(3) Cobertura retroactiva.** No hay nada retroactivo que cubrir: la pieza **precisa** `E.2`, no la sustituye. `E.2` vive en `instrucciones-proyecto-v2_13.md:446` y ya fija las tres preguntas que no se colapsan, con la tercera verbatim: *«¿se adopta? (humana, por merge de mesa)»* — que es el gozne sobre el que la regla apoya «el merge de mesa del PR que trae un bloque ES la adopción de ese bloque». Ningún slot de `demanda-resultados.tsv` se reclasifica por archivar esto, y ninguna adopción pasada se revisa: la regla gobierna relevos futuros.

LO QUE ESTE ARCHIVO NO HACE. No ejecuta el `P4` (no hay acto que lo tenga). No abre fila en `data/corrida0/decisiones.tsv`, no deriva ADR, no escribe `PARA-v2.14`, no clasifica ningún slot en bin 1/2/3, no toca `demanda-resultados.tsv` ni `usos.tsv` ni `milpa/`. No redacta el encargo de `ACTO GEN2-RELEVO-USOS-1` ni el de `FIRMAS-MESA-1` — eso es de dirección. Sólo fija el texto por `A.3`, para que cuando el acto se lance su `P4` encuentre la regla en el árbol y no en una conversación.

---

PIEZA DE DIRECCIÓN — verbatim, tal como llegó:

════ ADENDA · ACTO GEN2-RELEVO-USOS-1 · REGLA DE ADOPCIÓN EN BLOQUE (gobierna tu P4) ════
(dirección, 15/sep/2026 · la firma viaja adentro, verbatim; el ejecutor PROPAGA, no decide — SELLA-3 · aplica en cuanto abra tu compuerta de P4, el merge de FIRMAS-MESA-1)

FIRMA DE MESA, mesa, 15 de septiembre de 2026 — verbatim: «Pues si, la regla de adopción en bloque es lo que nos permitirá dejar de enfocarnos en transacción y movernos a esta otra fase más estratégica y de cálculo.»
OBJETO: se adopta la REGLA DE ADOPCIÓN EN BLOQUE de abajo para los relevos GEN1→GEN2 de slots demandados; el merge de mesa del PR que trae un bloque ES la adopción de ese bloque (E.2: «¿se adopta? — humana, por merge»). Resuelve el gobierno de adopción para `demanda-resultados.tsv`; no toca E.2/E.3/E.4, las precisa.

── LA REGLA ──────────────────────────────────────────────────────────────────

Ámbito. Todo slot de `demanda-resultados.tsv` (consumidor + resultado legacy) para el que existe un RESULT GEN2 SELLADO en su corrida natural y un delta legacy→GEN2 calculado por `corrida0 delta` (hashes, uso y contrato explícitos — nunca a mano). Sin delta por script no hay relevo, en ningún bin.

Tres bins, y ningún relevo queda fuera de ellos:

1 · NO-MATERIAL — entra al PR en bloque; el merge lo adopta. Las tres condiciones a la vez: (i) mismo signo; (ii) el punto GEN2 no dispara la cláusula del consumidor: si el consumidor declara `se_mueve_si`, ésa manda; si no, el punto GEN2 cae dentro del IC declarado del legacy; (iii) el slot no es un coeficiente del generador (`procedencia.yaml`), ni una regla con p medida, ni insumo del marcador (M/R/L/agregado) — ésos son siempre bin 2.

2 · MATERIAL — un renglón por slot en la lista a mesa, con el delta a la vista; firma individual. Cae aquí lo que cambia signo, tier, clasificación o dispara `se_mueve_si`, y todo lo del inciso (iii), aunque el delta sea cero: para el generador y el marcador, la adopción se firma aunque no cambie nada, porque cambia quién manda.

3 · SIN-CRITERIO — el consumidor no declara `se_mueve_si` y el legacy no trae IC: no hay con qué decir "no material". Se agrupan en un bloque aparte con la tabla de deltas (valor legacy, valor GEN2, delta, escala, universo) y mesa firma ese bloque de una vez o lo devuelve. No se cuelan al bin 1 por defecto ni se degradan al bin 2 uno por uno: eso es el modo de falla de transacción que esta regla existe para cerrar.

Invariantes, sin excepción:
- Escala y universo declarados por pareja (A-bis 3 y 4): un delta entre escalas distintas o entre universos distintos (poblacional vs. subpoblación) no es un delta — va a bin 3 con la razón escrita. Nunca "difiere en Z%" entre escalas.
- Cada slot adoptado deja: fila de uso en el registro derivado (escritor canónico), cita `corrida0_*` en el consumidor, delta citado. Adoptar no es validar (E.2, tres preguntas): la validación independiente sigue reservada a lo que puede cambiar signo, tier, clasificación, marcador o coeficiente — es decir, al bin 2.
- Los replays de GEN1 no relevan nada (`cuenta_gen2 = NO`). Un bloque nunca reescribe un sello: si el legacy queda SUPERADO, es estado del registro derivado, no edición de su archivo.
- El PR del bloque lista todos los slots que adopta, uno por línea, con su bin: es lo que mesa firma al fusionar, y lo que un auditor puede leer sin reconstruir nada.

Falsador y caducidad (mismo criterio que A.3/A.8/A.9/A.10/A.12/A.13). Si en tres meses un slot adoptado por bin 1 resulta haber cambiado tier, signo o clasificación sin que la regla lo atrapara, la regla se estrecha (no se retira) y el caso se cita. Si en tres meses ningún bloque se ha fusionado, la regla no sirvió y se anota.

── PROPAGACIÓN (P4, tras tu compuerta) ────────────────────────────────────────
1 · Fila en `decisiones.tsv` con la firma verbatim de arriba y esta regla como OBJETO.
2 · ADR derivado por el comando de la casa en tu cascada, y una entrada `PARA-v2.14` en `forense/hallazgos.md` con el texto de la regla: las instrucciones se entregan por versión íntegra (firma de mesa del 2/sep), no se pegan enmiendas.
3 · Tus tres listas al cierre, con conteos derivados y no tecleados: bin 1 (adoptados por este merge), bin 2 (a mesa, uno por uno), bin 3 (bloque a mesa con tabla). `## NO-CORRIDO / RESERVAS` declara todo slot que no cupo en ningún bin y por qué.
════════════════════════════════════════════════════════════════════════════════
