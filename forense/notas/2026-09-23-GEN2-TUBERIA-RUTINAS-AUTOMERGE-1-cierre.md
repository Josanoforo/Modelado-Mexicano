# Cierre · ACTO GEN2-TUBERIA-RUTINAS-AUTOMERGE-1 · 23/sep/2026

## Arranque
- Repo: `/home/user/Modelado-Mexicano`, `origin/main` al día tras `git fetch --prune` (`git rev-list --count HEAD..origin/main` = 0, base `f9628e5`).
- Duplicado: `git ls-remote --heads origin | grep -i "RUTINAS-AUTOMERGE"` → 0 líneas; `git worktree list` → 1 (este); ningún PR ni rama viva con ese rótulo. Sin duplicado.
- Higiene (`tools/limpia_arbol.py --reporta`): 1 worktree vivo, 1 rama local ya fusionada y viva, base al día. `gh` no disponible en este entorno → punto D `NO-VERIFICABLE-SIN-GH`.
- `data/raw`: ausente, no se enlaza — este acto no toca microdato ni red de datos.
- Entorno (`tools/entorno.py --arranque`): `ENTORNO-DERIVADO = NUBE`, coincide con lo declarado por el encargo. Corpus no montado (0 archivos examinados). Red `DENEGADA-POR-POLITICA`.
- Espejo: no se usó — toda cita sale de este clon.

## Encargo
El archivo ya estaba archivado en el repo por `[COLA] encola TANDA-5` (commit `d324994`), sin sidecar de sello. Este acto corrió `tools/sella_sha256.py --cuerpo` sobre `forense/encargos/2026-09-22-GEN2-TUBERIA-RUTINAS-AUTOMERGE-1.md` como su propio 0-bis (commit `e8893b78`, sha `43a94d70…`).

## Compuerta
El encargo no trae línea `GATED a` / `COMPUERTA:` con rótulo — nada que verificar en el paso 2 de la skill.

## Verificación de premisas (§4 de la skill)
- `[EJECUTADO]` "merges de rutina en los últimos 4 días, cuatro por día" — no re-verificado exhaustivamente (no cambia el resultado del PARO); tomado como dado por su rótulo.
- `[LEÍDO]` `.github/workflows/verify.yml` no trae auto-merge — confirmado: `grep -n "auto-merge\|automerge" .github/workflows/*.yml` → 0 líneas, código de salida 1.
- `[SUPUESTO]` "el repositorio permite merge por token de Actions con la protección de rama actual" — **no verificado**: verificarlo antes de tener la firma de §2 sería construir alrededor de una premisa de mesa que todavía no existe. Queda para el sucesor, si mesa firma.
- `NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-04` releída (A.17): sigue `ABIERTA`, sin cambio de estado desde el 22/sep.

## PARO — por qué
§2 del encargo es, textualmente, una propuesta de dirección que el propio encargo somete a sello o borrado de mesa, con la instrucción explícita: «Sin texto → PARA (nada que instalar).» El cuerpo archivado no trae ninguna firma de mesa después de esa propuesta. Búsqueda por objeto (no por memoria):

```
grep -n "RUTINAS-AUTOMERGE" forense/firmas-pendientes.tsv   # 0 líneas
grep -n "RUTINAS-AUTOMERGE" forense/decisiones.tsv 2>/dev/null   # 0 líneas (no existe ese archivo con ese nombre; ver data/corrida0/decisiones.tsv)
```

Esto toca directamente una firma de mesa (§2 de la skill: "toca … una firma de mesa → PARA y reporta. Nunca se ajusta el procedimiento para que cuadre"). No se construyó P1 (`forense/rutinas-clases-v1_0.tsv`), P2 (el workflow) ni P3 (huella en `hallazgos.md` + nota de clases) porque las tres piezas son exactamente lo que la firma ausente autorizaría a instalar.

## Hallazgo agravante — no es un PARO nuevo, es evidencia de por qué el PARO es correcto
`forense/firmas-pendientes.tsv` fila `FP-260921-GEN2-TUBERIA-ENRUTAMIENTO-PR-1-9a2c-01` (FIRMADA, 20/sep/2026) ya resolvió esta misma pregunta en la dirección contraria hace tres días: mesa firmó, verbatim, que «el auto-merge queda anotado como NO instrumentado, con su razón (9 % de los merges, ninguna de las renumeraciones), reevaluable si esa fracción crece.»

El encargo actual (P5 del plan, "clases de auto-merge") es exactamente el tipo de reevaluación que esa firma contempla — pero la firma la condiciona a que "esa fracción crezca", y el encargo no aporta esa medición: §3 `[EJECUTADO]` cuenta 4 merges de rutina por día en 4 días, pero no los divide entre el total de merges de esos días (el numerador que definía el 9 % original). Sin ese cociente, no hay evidencia de que la condición de reevaluación se cumplió — la firma del 20/sep sigue rigiendo tal cual, y este encargo es, en efecto, la petición de una nueva firma que la sustituya, no una autorización ya dada.

Se recomienda a dirección, si vuelve a llevar esto a mesa: (a) medir la fracción actual de merges de rutina sobre el total (mismo método que `FP-9a2c-01`), y (b) presentar §2 junto con esa cifra y la firma anterior citada, para que mesa decida con las dos cosas a la vista.

## Suite
`python3 tests/check.py --rapido` → VERDE, 0 FAIL, 296 WARN (sin cambio atribuible a este acto).

## No corrido
Ver `## NO-CORRIDO / RESERVAS` en el encargo archivado y filas nuevas en `forense/no-corrido.tsv`.
