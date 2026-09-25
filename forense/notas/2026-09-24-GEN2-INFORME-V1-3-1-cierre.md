# ACTO GEN2-INFORME-V1-3-1 · cierre

24/sep/2026 · NUBE · rama `claude/new-session-unv469` (fijada por la plataforma;
el encargo lo prevé: «o la que fije la plataforma; se declara») · 0-bis `b1aa7461`
(hhhh `b1aa`) · base `origin/main` `8358b891` (SHA de redacción del encargo,
0 commits de diferencia al abrir) · encargo `forense/encargos/2026-09-24-GEN2-INFORME-V1-3-1.md`
(`.cuerpo.sha256` = `8186d26e…`).

## 0 · ARRANQUE y premisas

Guard 0: `rev-list HEAD..origin/main` = 0 · árbol limpio · duplicado: 0 ramas
remotas, 0 worktrees ajenos, 0 PR abiertos con el rótulo · `limpia_arbol.py
--reporta`: base al día. ENTORNO (`tools/entorno.py --arranque`):
`ENTORNO-DERIVADO = NUBE` (coincide con el declarado por el encargo — no hay
PARO), `corpus=NO(examinados=0)`, `red=DENEGADA-POR-POLITICA`. Acto de sólo
lectura: no toca `data/raw`, no lo enlaza ni lo crea (no lo necesita).

| premisa (rótulo) | verificación | resultado |
|---|---|---|
| `[EJECUTADO]` v1.2: 414 líneas, estructura en §1 | `wc -l canon/informe-programa-v1_2.md` | se sostiene (414) |
| `[EJECUTADO]` anexo v1.3 en main | `git show origin/main:canon/informe-programa-v1_3-ANEXO.md \| wc -l` | se sostiene (59 líneas) |
| `[EJECUTADO]` Celdas-D: 10+ | `ls data/curacion-registro/celdas-d/*.yaml \| wc -l` | 21, no «10+» ambiguo — se cita exacto |
| `[SUPUESTO]` contadores «en main» citan `celdas_validadas` desde «commit de #1078» | `git log --oneline -- tools/celdas_validadas.py` | **premisa falsa**: es `38dd709`/`PR #1086`. Corregido, declarado (§1.2 del informe) |
| `[SUPUESTO]` `celdas_d_adoptadas_activas` sigue en 6 | `python3 tools/tablero_programa.py` | **premisa falsa**: 17. El «6» de v1.2 coincidía por fecha con `legacy_activas_por_consumidor__celdas_D`, contador distinto |
| `[SUPUESTO]` PISOS-GEN2-2/DONDE-CAMBIO/CLASE-AMAI no habrán cerrado | `git log origin/main --oneline \| grep -c` por rótulo | se sostiene: los tres tienen rama abierta, ninguno fusionado |
| Censo de pisos #1116, mapa #1079 (1 396/208/768/420) | `PR #1116`/`#1079` en `git log --merges` | ambos ya en `origin/main`, verificados por comando (§3.5, §4 del informe) |

## 1 · P1 · Derivación

El «script del README GEN2, #1083» resultó ser el propio `README.md` como
artefacto derivado (patrón `<!-- deriva: … -->`), no un script aparte —
`#1083` es el PR que lo fusionó (`ACTO GEN2-FRONT-1`), verificado por objeto.
`forense/analisis/informe-v1_3/censo_evaluaciones.py` (nuevo) cubre los
agregados que sí exigían cómputo (6 evaluaciones, 4 instrumentos, 137 celdas,
7 familias de retador) citando y verificando contra `canon/informe-programa-
v1_3-ANEXO.md` y `canon/estado-programa-v1_16.md` — falla en voz alta si la
cita fuente se mueve, no transcribe números a mano. **INTERPRETACIÓN-
DECLARADA** (Cláusula de Autonomía §2): P1 se satisface con el patrón
inline `<!-- comando: … -->` + el script de agregados + `tests/test_informe_
derivado.py`, no con un binario monolítico que «imprima todo el informe».

## 2 · P2 · Ensamble

`canon/informe-programa-v1_3.md`: misma estructura que v1.2 (§0–§7) más §2.5
(corroboración externa) y §3.5 (de dónde venían los pisos), citando el
ANEXO por sección. El texto de dirección (§11 del encargo) viaja verbatim;
las cifras entre «⟨⟩» se derivaron por comando — dos de ellas contradecían
al comando (§0 arriba) y se corrigieron, declarándolo en el propio cuerpo
del informe (§1.2, §4).

## 3 · P3 · Auditoría

§6 completo: siete preguntas del módulo + [v2.1]–[v2.16], incluida la
distinción PROSPECTIVA/RETROSPECTIVA (el piso `-0002` de ENCIG es
RETROSPECTIVA por E.6, las seis evaluaciones son PROSPECTIVA) y la de
unidad (persona/hogar/delito/trámite, ninguna promediada con otra).

## 4 · P4 · Test, puntero, T01, receta de release

- `tests/test_informe_derivado.py` (nuevo, patrón de `test_estado_derivado.py`):
  re-ejecuta cada `<!-- comando: … -->` de `canon/informe-programa-v1_3.md`
  contra el árbol real. `python3 tests/test_informe_derivado.py` →
  `OK T-INFORME-DERIVADO: 46 comandos citados en canon/informe-programa-v1_3.md
  reprodujeron sin error.` VERDE. (Nota: `tools/ci_guardias.py --censo` marca
  este test y su hermano `test_estado_derivado.py` como `FALLA-DE-VERDAD
  (TIMEOUT>40s)` en su propio censo — es el presupuesto de clasificación de
  40s de esa herramienta, no un fallo real: seis invocaciones de `corrida0.py
  status` a ~75s cada una superan ese presupuesto por diseño, igual que ya le
  pasa a `test_estado_derivado.py` y `test_readme_derivado.py`.)
- Puntero de informe vigente: `README.md` (3 líneas: «Informe vigente», «El
  informe documenta…», «Empieza por…»), `docs/index.md`,
  `docs/guia-lectura-publica.md` → apuntan a `v1_3`. `v1_2` no se toca
  (`git diff --stat -- canon/informe-programa-v1_2.md` vacío).
- `docs/informe.md`: **no se crea** — colisiona por nombre normalizado con
  un informe forense existente (T02), defecto ya diagnosticado por
  `GEN2-FRONT-1` el 23/sep (`docs/guia-lectura-publica.md` nace de esa
  misma colisión). `docs/guia-lectura-publica.md` ya cumple el papel
  (front-matter `title: Informe`) y se actualizó en su lugar. Declarado en
  `## NO-CORRIDO / RESERVAS` del encargo archivado, razón
  `SUSTITUIDO-POR:GEN2-FRONT-1`.
- T01: `FAILS: []` (una versión viva por artefacto; `informe-programa` no
  está en su universo — `modelo`/`glosario`/`gobernanza`/`estado` — así que
  v1.2 y v1.3 conviven sin violarlo).
- `python3 tests/check.py --baseline --parallel`: **VERDE, exit 0** — sin
  `fails_nuevos` frente a `tests/baseline.json` (HEAD `7100cd03…`, 13 FAIL /
  142 WARN congelados). La corrida de este acto reporta, además, 10 FAIL y 2
  WARN de la línea base que ya no aparecen (mejora ajena a este acto, no
  congelada sin `--freeze` explícito — no se toca `baseline.json` aquí). El
  bloque de `T03` que persiste son citas rotas preexistentes en encargos y
  notas históricas (`forense/encargos/2026-09-22-PENDIENTES-PROGRAMA.md` y
  similares), ajenas al perímetro de este acto.

## 5 · Receta de release `v2026.09`, para mesa

- **Tag:** `v2026.09`
- **Título:** Benchmark del Mexicano v1.3 — cierre de la etapa de retadores
- **Dos líneas con cifras del informe:**
  1. Seis evaluaciones prospectivas, cuatro instrumentos (ENCIG, ENIF,
     ENIGH, ENVIPE), 137 celdas de cruce: cero `VENCE` puro de 18 dictámenes
     de celda-D; una sola propuesta con reserva (crédito K1, ΔMAE +1.90 pp,
     IC95 [0.62, 2.65] pp) con umbral inalcanzable por diseño.
  2. 219 celdas validadas (20 prospectivas), 17 de 21 celdas-D adoptadas
     activas; corroborado en Corea (persistir 3.7 pp vs sintético 7.0–7.5
     pp) y en tres países (recitar la tabla nacional, 4.85 pp) — literatura,
     no promediada con RESULT propios.
- Este acto **no publica en Zenodo**: la publicación y el DOI quedan para
  mesa, con esta receta.

## 6 · Contadores

Cero mediciones, cero adopción, cero corrida sellada por este acto.
`celdas_validadas: 219 → 219 (Δ0)`, `celdas_d_adoptadas_activas: 17 → 17
(Δ0)`, `N_corridas_selladas: 246 → 246 (Δ0)` — los tres re-derivan idénticos
contra `origin/main` al cierre.
