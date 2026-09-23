# ENCARGO · ACTO GEN2-TUBERIA-PARSER-FP-1 · El digesto vuelve a ver las firmas: el parser de FP reconoce la gramática de raíz de acto y la vista `--mesa` deja de reportar cero abiertas cuando hay diecisiete

> ENTORNO: **NUBE** — cero microdato. Hook; si no coincide, PARA.

CABECERA · SHA `ab01b3fe` (22/sep/2026 19:36 −06:00; re-deriva al abrir) · una sola sesión (D-17) · MODELO: Sonnet (regex con gramática dada y test con dos ids; sube a Opus si aparece un segundo consumidor del formato) · MODO: **ABIERTO** · CONTADOR: cero mediciones; la vista `--mesa` pasa a contar las FP con raíz (reportado: FP ABIERTA en `--mesa` = FP ABIERTA en el TSV) · ids raíz de acto.

## 1 · OBJETIVO
Que `tools/digesto_tramite.py` reconozca los ids de FP acuñados con raíz de acto (D-24: `FP-<AAMMDD>-<RÓTULO>-<hhhh>-<NN>`) además de los numéricos históricos (`FP-###`), en **todos** los sitios donde hoy usa `RE_FP_ID` (`:2325` definición; `:2416` `fp_citadas = RE_FP_ID.findall(sucesor)`) y en cualquier otro regex del archivo que asuma `\d+` para NC o ADR, y que la vista `--mesa` reporte exactamente las mismas FP ABIERTA que `forense/firmas-pendientes.tsv`. «Hecho» = `python3 -c "import re, tools.digesto_tramite as d; print(d.RE_FP_ID.findall('FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01 FP-374'))"` → los dos ids completos; `python3 tools/digesto_tramite.py --mesa --stdout --sin-suite | grep -c "ABIERTA"` (o su línea de resumen) coincide con `awk -F'\t' 'NR>1 && $6 ~ /^ABIERTA/' forense/firmas-pendientes.tsv | wc -l`; `tests/test_digesto_ids_raiz.py` en verde y cableado en CI; NC `…TUBERIA-SUCESOR-1-6e60-01` CERRADA con cita.

## 2 · FIRMAS DE MESA
Ya selladas, se citan: D-2 y D-3 del sucesor (`forense/encargos/2026-09-21-GEN2-TUBERIA-SUCESOR-1.md` §2), D-24 (v2.16). Ninguna nueva: es corrección de un consumidor de formato a la gramática ya firmada.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `tools/digesto_tramite.py:2325`: `RE_FP_ID = re.compile(r"\bFP-\d+\b")`; `findall` sobre `FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01` → `['FP-260921']` (reproducido por Codex el 23/sep y por dirección hoy). `[EJECUTADO]` Efecto medido en la vista: el 22/sep `--mesa` reportó «FP examinadas 374 (0 ABIERTA)» con 17 ABIERTA en el TSV.
- `[LEÍDO]` NC `…6e60-01`: «P3 · `tools/digesto_tramite.py:2324` NO se toca: se redacta el diff de…» — el sucesor dejó el diff propuesto sin aplicar; el transfer de Codex (23/sep) advierte: «no aplicar a ciegas un diff fechado que puede haber quedado corto frente a D-24» — partir de la gramática vigente y probar un id antiguo y uno nuevo.
- `[SUPUESTO]` `RE_FP_ID` es el único regex de FP en el archivo y NC/ADR tienen el suyo propio ya ampliado (CIERRE-SIN-CHOQUE-1/2). Si resulta falso, el acto amplía los que encuentre con el mismo test, y lo declara; si encuentra consumidores fuera de `digesto_tramite.py` (p. ej. `tablero_programa.py`, `cierre_acto.py`), los lista como NC nueva — **no** los toca (perímetro).
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`git log -p -S "RE_FP_ID" -- tools/digesto_tramite.py | head` → reporta si alguien lo cambió después de `ab01b3fe`; `git ls-remote --heads origin | grep -i "parser\|digesto"` → reporta ramas con el objeto. Al redactar: ninguna.

## 5 · PIEZAS
- **P1 · Gramática.** Un solo regex que acepte `FP-\d{1,4}` (histórico) y `FP-\d{6}-[A-Z0-9-]+-[0-9a-f]{4}-\d{2}` (D-24), sin capturar prefijos parciales; lo mismo para cualquier regex hermano de NC/ADR del archivo que siga en `\d+`. Docstring con la gramática y la cita a D-24.
- **P2 · Test.** `tests/test_digesto_ids_raiz.py`: un id histórico, uno con raíz, uno con guion interior en el rótulo, y un negativo (`FP-260921` solo, sin sufijo) — el parser no debe aceptar el prefijo suelto como id. Cableado en `verify.yml` (NC-0331).
- **P3 · Vista.** `--mesa` antes/después con las cifras de FP ABIERTA y el mismo conteo desde el TSV, pegados. NC `…6e60-01` → CERRADA; línea en `hallazgos.md`: «la vista de mesa no vio ninguna firma con raíz de acto del 21 al 22/sep; el parser leía el prefijo; dos días de decisiones se llevaron a mesa desde el TSV, no desde la vista».

## 6 · LATITUD
DECIDES TÚ: forma del regex, nombre del test. PREGUNTAS A MESA: ninguna prevista. NO DECIDES: §7.

## 7 · PAROS
a) no aplica · b) tocar `check.py` fuera de cablear el test, o T15 · c) no aplica · d) no aplica · e) caja · f) inalcanzable.

## 8 · COMPUERTAS
Ninguna.

## 9 · PERÍMETRO
Propio: `tools/digesto_tramite.py` (regex y sus usos) · `tests/test_digesto_ids_raiz.py` (nuevo) · `.github/workflows/verify.yml` (un paso de test) · `forense/no-corrido.tsv` (6e60-01) · `forense/hallazgos.md` · nota · `canon/L0/<raíz>.md`. Ajeno: `tablero_programa.py`, `cierre_acto.py`, `acto.md` (6e60-02 es otro objeto), T15. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No toca el chequeo 0.c de `acto.md` (6e60-02), no censa consumidores de orden (6e60-07), no reabre el careo. Sucesor: 6e60-02 (despacho duplicado por contenido) como acto propio de tubería. Auditoría: no aplica. Cierre por /acto.

## NO-CORRIDO / RESERVAS

- **Alinear `tools/nc_por_clase.py::RE_FP` (y `estado_comun.RE_ADR`) a D-24** (§3 `[SUPUESTO]` del encargo, que preveía esta rama explícitamente: «si encuentra consumidores fuera de `digesto_tramite.py`, los lista como NC nueva — no los toca»). `FUERA-DE-PERÍMETRO:GEN2-TUBERIA-SUCESOR-1` — §9 lo lista por nombre como AJENO. Impacto: 6 pares `(NC, FP)` que `nc_por_clase.py` sigue sin resolver (2 ids reales que D-24 admite y esa gramática rechaza). Sucesor: `NC-260923-GEN2-TUBERIA-PARSER-FP-1-9641-01`.
- **`tools/estado_comun.py::lee_tablero` cuenta líneas físicas, no filas** (hallazgo adyacente, no pedido por el encargo). `FUERA-DE-PERÍMETRO:GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1` — no aparece ni en lo propio ni en lo ajeno de §9; es de otro acto. Impacto: la vista `--mesa` publica «FP examinadas: 464» sobre 462 filas reales; ninguna adjudicación se mueve. Sucesor: `NC-260923-GEN2-TUBERIA-PARSER-FP-1-9641-02`.
- **`ADENDA-1` de `GEN2-TRAMITE-FIRMAS-8`, recibida junto con este encargo, no se archivó**. `PARO-PREMISA` — D-17 (una sola sesión por encargo) impide a esta sesión ser un segundo escritor sobre `GEN2-TRAMITE-FIRMAS-8`, vivo en PR #1027 (rama `claude/new-session-edpgs6`, ya con `## CONSUMIDO`). Impacto: mientras no se archive, el aparato tiene dos firmas de mesa contradictorias sobre el auto-merge (`…9a2c-01` FIRMADA «NO instrumentado» vs `…e889-01` ABIERTA «sí se instrumenta»); es exactamente el choque que `ACTO GEN2-TUBERIA-RUTINAS-AUTOMERGE-1` reportó hoy como PARO. Sucesor: `DIFERIDO-A:GEN2-TRAMITE-FIRMAS-8` (PR #1027) o su acto de trámite sucesor.

## CONSUMIDO

PR #1029.
