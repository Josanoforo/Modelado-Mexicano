SHA de redacción: `3e4c9f7` (`origin/main`, verificado por `git ls-remote` el 18/ago/2026)
Entorno asignado: NUBE (sesión nueva, clon fresco). Código + pruebas, sin corpus. NO lo lances en Ubuntu: ahí corre `ACTO GATE-DURABLE-V7`. Perímetros disjuntos por construcción — este acto toca `integrate_barrido2.py` y `tests/check.py`; aquél toca `barrido2_material.py` y los productos. Cero archivos en común salvo la colisión esperada de número de ADR.
Estado: CONSUMIDO — rama `claude/acto-t23-integrador-cableado-is3bv2`, commits `53b6ee8` (COMMIT 1), `53b9477` (COMMIT 2), y el cierre de este mismo commit (COMMIT 3, `ADR-98`). Sin PR abierto en esta sesión — nadie lo pidió; la rama queda lista para que mesa lo abra.

════════ ARRANQUE ════════
1 · REPO. Clon fresco si no hay. Reporta ruta · `git log -1` · `git status`. Verifica no superficial (`git rev-parse --is-shallow-repository` → `false`).
2 · SHA. Contra `3e4c9f7`; si main se movió (p. ej. fusionó #255), re-deriva y reporta. La rama `acto-b2-v7`/`gate-durable` viva no te afecta: archivos disjuntos.
3 · data/raw. AUSENTE NO ES PARO — este acto no la usa. Repórtalo y sigue.
4 · ENTORNO (A.2): variable cruda · sonda INEGI (`curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/`, nunca `-I`) · `ls data/raw/ | head -1`. Un 403 aquí es la allowlist de esta caja, no INEGI (A.5).
5 · ESPEJO. Toda cifra del clon, con comando.
════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por quien escribe ═══
Estructura. Gobiernan: `tools/curador_registro/integrate_barrido2.py` (+ sus schemas y `tools/curador_registro/tests/`), `tests/check.py` y `tests/baseline.json`. Este acto escribe los dos primeros y `check.py`. NO escribe `tests/baseline.json` (prohibido congelar), ni `barrido2_material.py`, ni ningún producto de `data/`. Contenido, derivado contra `3e4c9f7`:

```
grep -n "def preflight" tools/curador_registro/integrate_barrido2.py → :137 (consumido en :406)
grep -cE "T23|T-CABLEADO|require-cableado" tests/check.py            → 0   NO-ENCONTRADO
espec de T23: forense/notas/2026-08-17-b2-derivaciones-c4.md §4 (:215+) EXISTE-SATISFACE
  — "El número es T23, derivado: ^def t\d+ da 1..22" · 19 condiciones de FAIL · WARN · 2 pruebas negativas
defecto del integrador: declarado en forense/notas/2026-08-18-b2-transfer.md (C5) — una
  PROPUESTA_ALTA VALIDADA aborta el lote como error de preflight, en vez de terminar en
  uno de los cuatro estados que §19 exige                              EXISTE-NO-SATISFACE
autorización: ADR-95(a) lista cerrada — "(5) vía fail-closed de capa 4"; y el encargo
  madre §0: "T-CABLEADO pertenece a tests y no amplía esta lista"      EXISTE-SATISFACE
suite hoy: 19 FAIL · 135 WARN · línea base VERDE contra 997482b (re-derívalo tú)
```

Cobertura retroactiva. `integrate_barrido2.py` nunca corrió contra datos reales (cero celdas de capa 4 cambiadas); sus dos pruebas del §22 del acto anterior están verdes. El defecto lo encontró la auditoría de cinco agentes, no una corrida.
═══════════════════════════

PERÍMETRO. `tools/curador_registro/integrate_barrido2.py` · `tools/curador_registro/tests/` · `tests/check.py` · `canon/gobernanza-v1_15.md` (ADR) · `canon/estado-programa-v1_10.md` solo la cascada `:27`/`:101` (⚠️ FP-48) · `forense/notas/` · `forense/hallazgos.md` (append) · `forense/encargos/`. Fuera de esta lista: PARA. 🚫 No congeles. Este acto debe cerrar VERDE por construcción — ver el control C4 abajo. Si no cierra verde, el acto está mal, no el congelado.

COMMIT 1 · `integrate_barrido2.py` — una ALTA validada no es un error
El defecto: `preflight()` (`:137`) trata una `PROPUESTA_ALTA` validada como error que aborta el lote. La conducta correcta, del propio encargo madre (§19/§21): toda `PROPUESTA_ALTA` existente termina en `INTEGRADA / RECHAZADA_FAIL_CLOSED / CONFLICTO_MATERIAL / REQUIERE_DECISION_FP24`; y el high path solo se implementa si existe al menos una validada — decisión de acto, no de preflight.
El arreglo, acotado: `preflight` acepta la ALTA validada; el integrador la emite en estado `PROPUESTA_ALTA` (pendiente de high path) con WARN en la decisión de integración, sin abortar el lote y sin integrar nada de ella. No construyas el high path — eso sigue condicionado a que exista una validada en corrida real. Lee el CLI y los schemas reales antes de tocar (el encargo madre lo exige: "no inventes flags sin implementar ni probar").
Pruebas: (a) fixture con una ALTA validada + N propuestas ordinarias → el lote procesa las N y la ALTA sale en `PROPUESTA_ALTA`, rc≠abort; (b) la ALTA no aparece integrada; (c) las dos pruebas verdes existentes del §22 siguen verdes; (d) idempotencia: segunda corrida, diff cero.

COMMIT 2 · `T23 · T-CABLEADO`, nacido inactivo, y la bandera que dejaba de ignorarse
Fuente única de la especificación: `forense/notas/2026-08-17-b2-derivaciones-c4.md §4`. Léela completa y impleméntala tal cual — las 19 condiciones de FAIL, los WARN de conteo, y las dos pruebas negativas obligatorias (una relación histórica de las 20 decidible por evidencia específica con `dependencia_fp24=NO` integra ordinariamente; cualquier propuesta con `dependencia_fp24=SI` no puede quedar `INTEGRADA` mientras FP-24-sustancia esté pendiente). Deriva el número T con `grep -E "^def t[0-9]+" tests/check.py` — la espec dice T23; si otro acto ocupó el 23, renumera y dilo. T23 no conoce los 20 IDs históricos, ni denominadores, ni cuotas (§22 del encargo madre, verbatim).
Semántica de la bandera: hoy `check.py` ignora en silencio `--require-cableado` (solo lee `--strict/--baseline/--freeze` — el defecto está declarado en el transfer y en `derivaciones-c4`). Con este commit: sin bandera y sin producto, T23 emite nada (inactivo, ni ok ni warn); con `--require-cableado` y sin `data/cableado-universo-v1_0.tsv`, FAIL. Con producto presente, las 19 condiciones rigen siempre.
El control que decide si este commit está bien — C4, y pégalo crudo:

```
python3 tests/check.py            → MISMO conteo que antes del commit (T23 inactivo no suma)
python3 tests/check.py --baseline → VERDE, sin tocar baseline.json
python3 tests/check.py --require-cableado → FAIL de T23 por producto inexistente (y solo por eso)
```

Si la primera línea cambia el conteo, T23 no nació inactivo: arréglalo, no congeles.

COMMIT 3 · Cierre
ADR nuevo — re-deriva el número al escribirlo y otra vez al fusionar: `GATE-DURABLE-V7` corre en paralelo y la colisión es esperada (protocolo de renumeración, cinco precedentes). Cascada `:27`/`:101` con el número final. Nota del acto. Línea en `hallazgos.md`. Encargo `CONSUMIDO` con su PR. Merge local siempre; si el merge toca `estado-programa:101`, cláusula por cláusula (FP-48).

Módulo de auditoría — lo aplicable: contadores sobre México: cero, en una línea. Lo que sí mueve: el bloqueo de C5 (integrador que aborta) pasa de abierto a cerrado, y `--require-cableado` de ignorado-en-silencio a implementado — los dos con su prueba.
Lo que NO hace: no crea `build_cableado.py` ni `cableado-universo-v1_0.tsv` (C6, exige decisiones de la fase semántica) · no toca `barrido2_material.py` ni productos de `data/` · no cierra ninguna FP · no congela.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fn -- "2026-08-18-INTEGRATE-T23-integrador-cableado.md" canon/gobernanza-v1_15.md` cita ADR-99, pero el bloque mezcla lenguaje de ejecución y de encargo pendiente (o el rótulo del ADR es compartido entre varios encargos sin desenlace individual claro) — rastro parcial, no se decide aquí. Para mesa: verificar manualmente contra ADR-99 en canon/gobernanza-v1_15.md.

## CERRADO-POR-HISTORIA

Regla mecánica (b) de la resolución de mesa sobre FP-290 (2026-09-04):
sin hermano de rótulo compartido con desenlace ya sellado (regla a no
aplicó -- ver tabla en forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md,
enmienda 2026-09-04), este encargo queda cerrado por antigüedad e
inacción declarada, no por evidencia positiva de ejecución o
sustitución. Si aparece evidencia nueva, esta marca se reabre -- no es
`## CONSUMIDO`.
