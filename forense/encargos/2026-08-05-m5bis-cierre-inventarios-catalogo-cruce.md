# Encargo "§6 · Encargo M-5 · Cierre" — inventarios, catálogo y cruce v3.0

**SHA de redacción:** `16d9dbdd2f32747fe779b2d486ea6092059aa6e1` (`origin/main`,
mismo verificado que el encargo hermano `§5`, ver
`2026-08-05-m4bis-encup-lapop-latinobarometro.md`).

**Entorno asignado:** nube, solo git. Compuerta: requiere M-1 a M-4
fusionados.

**Estado:** VIVO — **no ejecutado**. La compuerta ("requiere M-1 a M-4
fusionados") no está satisfecha bajo ninguna lectura verificable al
cerrar el acto que recibió este encargo: el "M-4" del mismo lote (`§5`,
ver el archivo hermano) es, él mismo, el acto que cierra esta rama sin
fusionar todavía — no puede estar "fusionado" antes de existir como PR.
No hay evidencia en el repositorio de "M-1"/"M-2"/"M-3" de este mismo
lote (distinto del `M-1`/`M-2` ya sellados el 4/ago para `R3.1`/`W1-P`,
sin relación de contenido — ver colisión de etiqueta declarada en el
archivo hermano). Por disciplina de compuerta (mismo criterio que
`forense/notas/2026-08-04-m1-adjudicacion-r3-1-paro.md` aplicó cuando
paró antes del Commit 1 al encontrar dos PR requeridos todavía
`open`), este acto **no toca ningún archivo del perímetro de `§6`**:
`data/inventarios/*.md`, `data/catalogo-fuentes-v2_0.md`,
`forense/cruce-catalogo-fichas-v3_0.md`, `tests/dedup.py`. Queda `VIVO`
para que una sesión futura lo retome cuando la compuerta esté
verificablemente satisfecha — ver
`forense/notas/2026-08-05-m4bis-encup-lapop-latinobarometro-bloqueo.md`
§5 para el razonamiento completo.

*(Re-verificado 17/ago/2026, ACTO E-HIG/HIGIENE-VIVOS, contra `f3873c2`: `ls forense/cruce-catalogo-fichas-v3_0.md` → no existe; `git log --all --oneline --grep="cruce-catalogo-fichas-v3_0"` → sin resultados de creación. Sigue `VIVO`, misma razón, gate propio [M-1 a M-4 del lote] todavía no verificable como satisfecho.)*

---

## Texto del encargo, verbatim

§6 · Encargo M-5 · Cierre — inventarios, catálogo y cruce v3.0
ENTORNO ASIGNADO: nube, solo git. Compuerta: requiere M-1 a M-4 fusionados.

Perímetro: data/inventarios/*.md · data/catalogo-fuentes-v2_0.md (sección de cifras) · forense/cruce-catalogo-fichas-v3_0.md (nuevo, si mesa lo autoriza) · hallazgos.md. ⛔ forense/cruce-catalogo-fichas-v2_0.md es append-only. ⛔ hitoD-preregistro-v2_0.md no se toca.

1 · Los defectos de dedup.py, con caso de prueba. Hoy cuenta como distintas: CENSO DE POBLACIÓN Y VIVIENDA con y sin espacio final · ENNVIH y ENNVIH / MXFLS · ENOE y su nombre largo · nombres truncados a 30 caracteres. El caso de prueba es el propio catálogo: la cifra de operables corregida debe bajar de 54.

2 · Re-derivar las cifras del catálogo y sustituir la tabla congelada por el bloque derivado con el comando a la vista, o dejar declarado que son históricas y remitir al comando.

3 · Alta en inventarios de lo que M-1 a M-4 hayan descrito, con la ficha completa y la clase de procedencia — confirmada vs. sospechada, y la sección "sospechadas" se respeta: una fila de ahí no es fuente catalogada.

4 · Las 17 operables sin bajar entran al inventario con su clase. ⚠️ ACS y CPS son encuestas de Estados Unidos: entran marcadas como población de diáspora, o no entran. Y reconcilia el estado de CLUES — el catálogo la da por operable sin bajar, B-4b-α la reportó con host inalcanzable.

5 · Cruce v3.0, solo si mesa lo autoriza. Reclasificación de las filas NO EXISTE con lo que M-1 a M-4 encontraron. Cada fila que cambie de clase declara qué la cambió, con archivo y línea.

⚠️ Y la regla nueva que este cruce debe llevar escrita en su cabecera:

Ninguna fila se marca NO EXISTE sin un cruce previo contra data/manifiesto.yaml. El cruce v2.0 razonó sobre data/inventarios/ —lo que sabemos que existe— y nunca sobre el manifiesto —lo que efectivamente tenemos. Ésa es la causa de las siete filas insostenibles.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-05-m5bis-cierre-inventarios-catalogo-cruce.md" canon/gobernanza-v1_15.md` → 0 (sin cita en ningún ADR). Rastro fuera de gobernanza, sin nota de cierre propia: canon/citas-sha-obsoletas-purga-2026-08-10.tsv, tests/check.py. Insuficiente para CONSUMIDO, insuficiente para NO-EJECUTADO — rótulo/evidencia parcial, se lista para mesa.

## CERRADO-POR-HISTORIA

Regla mecánica (b) de la resolución de mesa sobre FP-290 (2026-09-04):
sin hermano de rótulo compartido con desenlace ya sellado (regla a no
aplicó -- ver tabla en forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md,
enmienda 2026-09-04), este encargo queda cerrado por antigüedad e
inacción declarada, no por evidencia positiva de ejecución o
sustitución. Si aparece evidencia nueva, esta marca se reabre -- no es
`## CONSUMIDO`.
