**SHA de redacción:** `d55ae72` (`origin/main`, merge #221 · INV-DESCMX · verificado por comando el 13/ago/2026, cero ramas vivas).
**Entorno asignado:** repo-only, NUBE. NO requiere caja, NO requiere red, NO requiere `data/raw`. NO se lanza en la caja — ahí el turno es de `REG-LOTE3`.
**Estado:** VIVO — ejecutado en esta sesión (ACTO FIRMAS-2). Marcar `CONSUMIDO` con el PR que fusione este acto.

Texto completo del encargo, tal como se lanzó, sin resumir:

---

# ACTO FIRMAS-2 · las dos firmas que desbloquean el carril de caja

`SONDEO-COMPLETO` · `argumento de vinculación declarado`

* SHA de redacción: `d55ae72` (`origin/main`, merge #221 · INV-DESCMX · verificado por comando el 13/ago/2026, cero ramas vivas).
* Entorno asignado: repo-only, NUBE. NO requiere caja, NO requiere red, NO requiere `data/raw`. NO lo lances en la caja — ahí el turno es de `REG-LOTE3`.
* Estado: `VIVO`. Gate: ninguno. ADR-79 y ADR-76 ya están en `main`.
* ADR: deriva al sellar. Contra `d55ae72`: `únicos 79 · max 79 · huecos []` → 80.
* Perímetro: `canon/gobernanza-v1_15.md` (un ADR + dos enmiendas in situ), `canon/estado-programa-v1_10.md` (cascada), `forense/notas/2026-08-13-firmas-2.md`, `forense/hallazgos.md`. Nada más. ⚠️ Es el único acto que puede tocar `canon/gobernanza` mientras corre. Verifica con `git ls-remote --heads origin`; si hay otra rama viva que lo toque, PARA. Con la frase: "si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════
1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · `git log -1 --format="%h %s"` · `git status` ⚠️ No arranques desde el home. ⚠️ `pwd` antes de todo comando de estado, y `git -C <ruta>` en vez de `cd`.
2 · SHA. Confirma contra `d55ae72`. Si `main` se movió: NO es PARO — refresca, re-deriva el número de ADR con la receta de T15, reporta la diferencia antes de editar. ⚠️ La línea base está congelada en `3d0d1e5` (ADR-76(f)). Corre `--baseline` contra ése; el vigente es 20 FAIL · 107 WARN, VERDE.
3 · data/raw. AUSENTE NO ES PARO y este acto no la necesita. Reporta y salta.
4 · ENTORNO. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → valor crudo. Este acto no toca microdato ni red: salta la sonda y dilo.
5 · ESPEJO. Toda cifra sale del clon de (1), con el comando a la vista.
════════════════════════════════════════════════════════════════════
═══ VERIFICACIÓN DE EXISTENCIA — contestada aquí, por quien escribe ═══
1 · ESTRUCTURA. Dominio 7 de `data/INFRAESTRUCTURA-v1_0.md` — sellar una decisión de gobierno. Tablas gobernantes: `canon/gobernanza-v1_15.md` §4 + cascada obligatoria a `canon/estado-programa-v1_10.md`. Escribe las dos, ninguna más.
2 · CONTENIDO. Verificado contra `d55ae72`:

```
ADR-79(i)  → "REGISTRADO, NO SELLADO ... Este ADR no sella ningún alcance para (i)"
ADR-76(d)(4) → "mesa decide antes de correr el acto cuál estándar de éxito aplica"
```

`EXISTE-NO-SATISFACE` en los dos casos: la pregunta está escrita y sellada, la firma no. Este acto la aporta.
3 · COBERTURA RETROACTIVA. ADR-76 y ADR-79 son de hoy. Sin brecha.
════════════════════════════════════════════════════════════════════
§0 · Qué hace este acto y por qué es propio
Dos firmas de mesa que ya se dieron y no están escritas. Nada más.
Por qué no las firman los actos que las necesitan: ADR-76(d)(4) dice, verbatim, "mesa decide antes de correr el acto". Si `INVARIANZA` sellara su propio estándar de éxito, sería autoadjudicación — el defecto que ACTO RES cometió esta mañana. Lo mismo con `TRIAGE-63 COMMIT 2` y su propio alcance.
El ejecutor propaga y deriva. No decide. Las dos firmas van abajo entre comillas; si algo no está entre comillas, se para.
INCISO (a) · D-M — alcance del sondeo
Firma de mesa, verbatim: "Sondeo Completo."
Se sella `SONDEO-COMPLETO`: las 27 filas `CANDIDATA-A-SONDEO` entran al sondeo, con las 17 que gatean una ficha del Hito D primero, por orden de palanca.
Enmienda in situ fechada sobre `ADR-79(i)`, mismo mecanismo y misma redacción que ADR-75 y ADR-76 ya usaron:
(Enmienda in situ, 13/ago/2026, ACTO FIRMAS-2, sellada por `ADR-80` — mismo criterio que ADR-48 a ADR-79: el número de versión no sube, el archivo no se renombra.) El alcance queda firmado: `SONDEO-COMPLETO`. Las 27 candidatas entran al sondeo; las 17 que gatean una ficha del Hito D van primero, por palanca. Las 10 restantes no quedan fuera — van después, en el mismo acto o en su continuación declarada.
No borres el texto original de (i). Su registro de "REGISTRADO, NO SELLADO" es la prueba de que el ejecutor no se autoadjudicó, y esa auditoría vale más que la limpieza.
Y va incluida la corrección del umbral, que ADR-79(i) ya recogió y este ADR ratifica: el PARO de "más de 20 candidatas" del encargo original no tenía fundamento — ningún ADR fija tope por acto, y los únicos umbrales de 20 del corpus son de magnitud estadística. El PARO queda retirado. El COMMIT 1 de TRIAGE-63 no se invalida: su triaje es correcto y su clasificación se conserva íntegra.
INCISO (b) · Estándar de éxito de la invarianza ENCUCI↔ENBIARE
Firma de mesa: "Benchmark web" → aclarada por mesa como "usa lo que el benchmark ya dijo", es decir: se adopta el estándar que `BENCHMARK-ENLACE` (#210) identificó como el único ejecutable hoy.
Se sella `ARGUMENTO DE VINCULACIÓN DECLARADO` — la segunda de las dos opciones que `ADR-76(d)(4)` puso sobre la mesa, verbatim: "anclas de diseño + invarianza parcial".
Enmienda in situ fechada sobre `ADR-76(d)`:
(Enmienda in situ, 13/ago/2026, ACTO FIRMAS-2, sellada por `ADR-80` — mismo criterio que ADR-48 a ADR-79.) La decisión que (4) reservaba a mesa queda firmada: aplica el `argumento de vinculación declarado`, no la invarianza clásica. La invarianza clásica queda declarada inalcanzable con los datos de hoy —dos ítems próximos, sin muestra puente— y el acto no la intenta formalmente: reportar "no se puede" sobre algo que este ADR ya declara inalcanzable gasta capacidad para producir un resultado ya escrito.
Fundamento que el ADR debe citar, todo del repo, todo tipo (1):

* `forense/benchmark-enlace-invarianza-v1_0.md` §D10 Pregunta 4 — la secuencia estándar del campo (configural → métrica → escalar, ítems ancla, invarianza parcial como estado reconocido) es, verificado, el vocabulario correcto, y es el que `ADR-67(a)` ya usaba.
* Pregunta 5(a) — la secuencia clásica no exige muestra compartida; lo que falta aquí es otra cosa: solo hay dos ítems próximos y no hay muestra puente.
* Pregunta 5(b) — el programa ya adoptó este estándar para el par estructuralmente idéntico ENCUCI/ENCIG (`forense/EDGE-CASES-y-literatura-reciente.md` §E5). No se inventa criterio: se aplica el precedente que ADR-76(d) señala por nombre.
* Literatura citada por el benchmark: Robitzsch & Lüdtke (2023) — la invarianza total, parcial o aproximada no es prerrequisito para comparaciones válidas entre grupos; más Raykov (2024) y Kusano.

⚠️ Lo que este inciso NO hace, y va declarado: no adelanta el veredicto del acto. `ENCUCI` sigue baseline y `ENBIARE` challenger sin poder de sustitución (`PROXY_PARCIAL`, fijado por `ADR-67(a)`) hasta que el acto corra — punto 5 de la Propuesta 2, intacto. Este ADR fija contra qué se juzga, no qué sale.
§1 · Lo que este ADR desbloquea — decláralo por nombre

* `TRIAGE-63 COMMIT 2` — caja con red. Alcance firmado: las 27, las 17 primero.
* `INVARIANZA ENCUCI↔ENBIARE` — caja con corpus. Estándar de éxito firmado.

Ninguno de los dos corre en este acto. Se nombran como desbloqueados, con la advertencia de que compiten por la caja y van uno a la vez, después de `REG-LOTE3`.
§2 · Lo que NO hace
No corre ningún diseño. No adjudica ningún resultado. No toca `data/`, `milpa/`, `tests/`, ni `canon/modelo-decision-v4_0.md`. No reabre `ADR-67(a)`. No borra el texto original de ADR-79(i) ni de ADR-76(d).
Contadores que NO se mueven, uno por uno: `13 de 27` (Hito D) · `9 de 14` (condicionales) · `0 de 15` (coeficientes) · `1 de 2` (llaves) · `4 de 144`. Ninguno. Este acto firma; no mide.
§3 · Cascada y numeración

```bash
python3 - <<'EOF'
import re, collections
t=open("canon/gobernanza-v1_15.md",encoding="utf-8").read()
n=[int(x) for x in re.findall(r"^\*\*ADR-(\d+)", t, re.M)]
print("únicos:",len(set(n)),"max:",max(n),"dups:",sorted(k for k,c in collections.Counter(n).items() if c>1),"huecos:",sorted(set(range(1,max(n)+1))-set(n)))
EOF
```

Contra `d55ae72`: `únicos 79 · max 79 · huecos []` → 80. Deriva al sellar, contra el `main` real, sin dejar hueco — T15 falla sobre huecos, no solo sobre el máximo. Ha colisionado cinco veces.
Sitios de cascada: `canon/gobernanza-v1_15.md:2` (cabecera) · `canon/estado-programa-v1_10.md` (tabla + §L0). Derívalos con `grep -rn "[0-9]\+ ADR" canon/ README.md` y pega la salida. La cifra `N FAIL · M WARN` se recalcula por corrida real, nunca se copia.
Cierre
`python3 tests/check.py --baseline` VERDE contra `3d0d1e5`, cifra reportada, antes y después. Nota en `forense/notas/2026-08-13-firmas-2.md`. Una línea en `forense/hallazgos.md`. El encargo se commitea a `forense/encargos/` antes o junto con su lanzamiento (A.3), con SHA de redacción, entorno y estado. Merge local, `main` HACIA la rama; el editor web de conflictos de GitHub está prohibido.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fn -- "2026-08-13-FIRMAS2-carril-caja.md" canon/gobernanza-v1_15.md` cita ADR-80, pero el bloque mezcla lenguaje de ejecución y de encargo pendiente (o el rótulo del ADR es compartido entre varios encargos sin desenlace individual claro) — rastro parcial, no se decide aquí. Para mesa: verificar manualmente contra ADR-80 en canon/gobernanza-v1_15.md.

## CERRADO-POR-HISTORIA

Regla mecánica (b) de la resolución de mesa sobre FP-290 (2026-09-04):
sin hermano de rótulo compartido con desenlace ya sellado (regla a no
aplicó -- ver tabla en forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md,
enmienda 2026-09-04), este encargo queda cerrado por antigüedad e
inacción declarada, no por evidencia positiva de ejecución o
sustitución. Si aparece evidencia nueva, esta marca se reabre -- no es
`## CONSUMIDO`.
