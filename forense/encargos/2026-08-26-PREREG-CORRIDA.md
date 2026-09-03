**SHA de redacción:** `9c25f28`
**Entorno asignado:** NUBE (`cloud_default`). No UBUNTU, no doble.
**Estado:** CONSUMIDO — ver `forense/prereg-duelo-v2/prereg-corrida-v1_0.md`, `canon/gobernanza-v1_15.md` ADR-197, `forense/firmas-pendientes.tsv` FP-162/FP-163, `forense/notas/2026-08-26-prereg-corrida-cierre.md`.

---

Texto completo del encargo, tal como se lanzó:

> Encargo `PREREG-CORRIDA` — el pre-registro de la corrida del duelo: hashes antes de `R`, elicitación M2 congelada, TOST derivado para tu sello · y `L-solo` como comparación principal
> SHA de redacción: `9c25f28`. Dirección, 25/ago/2026. ENTORNO: NUBE (`cloud_default`). No UBUNTU, no doble. CONTADOR: cero por diseño — este acto fabrica las condiciones bajo las que el primer marcador será legible.
> FIRMA 1 (cuál-L), precargada con la decisión de mesa de hoy — el ADR lleva además su razonamiento verbatim: «si el motor le gana al modelo pues sí podría ser mérito del corpus y si es así está bien, es lo que venimos trabajando, ¿o me quieres decir que Claude tiene acceso a esta misma data de forma centralizada?» (mesa, 25/ago). Y la respuesta de dirección, para el registro: no — el corpus curado no está centralizado en ningún modelo; lo único que un Claude pelado puede traer son fragmentos de tabulados públicos en su entrenamiento, y ese riesgo ya lo acota la cuota de publicadas del sorteo (2 de 15).
> RANURA 1: `FIRMO comparacion_principal_id = L-solo. L+corpus corre como auxiliar no-gating.` RANURA 2 (D-iii, quién corre la tubería L): `DESIGNO para las corridas L: sesiones limpias fuera del proyecto, mismo patrón que las adversariales.` — adopta o nombra otra cosa.
> ════ ARRANQUE ════ 1·REPO. 2·SHA vs `9c25f28`; ramas en vuelo pueden fusionar — renumera quien fusiona segundo. 3·data/raw ausente OK. 4·`cloud_default`; sin microdato ni red: salta sonda; negativos con conteo (A.13). 5·Cero cifras del espejo. ════
> ═══ EXISTENCIA (dirección, contra `9c25f28`) ═══ El sorteo existe (`sorteo-resultados-v1_0.md`: 15 IDs, semilla pública, 2 publicadas). La tubería existe: `pipeline-L-adv1-m2.py` · `corredor-B-tasa-base.py` · `corredor-E-combinacion-LM.py` · `scoring-adv1-m3.py` (`#330`: exige `comparacion_principal_id` predeclarada, sin default — `escala-cinco-casillas-piloto-v2_0.md:31`). El método de banda existe: `banda-tost-margen-v1_0.md`. Ningún pre-registro de corrida existe y ningún `R` (árbitro) existe — verifícalo con `find` y conteo (A.13); si algo de eso ya existe → PARA (A.8): comprometer hashes después de `R` invalida el diseño.
> F0 · Compuertas
> 1. RANURA 1 presente como línea propia (candado `FP-63`) — sin ella, PARO. RANURA 2 presente o adoptada.
> 2. A.8 en fresco (bloque de arriba). Cero salidas de árbitro en el árbol — este es el candado que da sentido a todo lo demás.
> F1 · Hashes comprometidos — antes de que `R` exista
> `sha256sum` de los CUATRO corredores (`pipeline-L-adv1-m2.py`, `corredor-B-tasa-base.py`, `corredor-E-combinacion-LM.py`, `scoring-adv1-m3.py`) + del marco congelado + de `sorteo-resultados-v1_0.md` → al pre-registro y al ADR, con la frase: «estos hashes se comprometen antes de que exista cualquier valor de árbitro; toda corrida posterior se verifica contra ellos.» Si un corredor cambia después, no se re-hashea en silencio: es enmienda fechada con razón.
> F2 · Spec de elicitación M2, congelada (el corazón del doc)
> `forense/prereg-duelo-v2/prereg-corrida-v1_0.md` fija, ANTES de correr nada: (a) modelo+versión+fecha+temperatura de las sesiones L — valores concretos propuestos por el acto leyendo M2 y el patrón adversarial previo, sellados aquí; (b) `k` fijado dentro de 5–10 (un valor, con razón); (c) agregado pre-registrado: mediana+cuantiles en numéricas, self-consistency en categóricas; (d) TODAS las corridas se registran, cero descartes, dispersión reportada; (e) el formato de captura por celda×corrida×variante (L-solo / L+corpus) que la tubería consumirá; (f) la plantilla de prompt por celda, derivada SOLO del marco congelado (frase de la celda + lo que la spec de elicitación permita) — sin una palabra que revele árbitro, banda o fuente de referencia; (g) `comparacion_principal_id = L-solo` escrito donde el ejecutable lo lee, con `L+corpus` declarado auxiliar no-gating (enmienda fechada al doc de interfaz si corresponde).
> F3 · Banda TOST y margen material — derivados, no inventados (D-iv)
> Aplica el método sellado de `banda-tost-margen-v1_0.md` al set sorteado (los EE reales que el método exija; donde una celda no los tenga aún, la banda queda condicionada al árbitro y se dice — no se rellena). Entrega el número con su justificación y ábrele su fila: mesa lo sella, no lo sella este acto — «firmar una constante a ciegas sería el defecto v2.1 de siempre» (CAREO D-iv, verbatim).
> F4 · Cierre
> Tablero: fila `FIRMADA` nacida con el verbatim de RANURA 1 (A.12; gatea: corridas L y scoring) · fila `ABIERTA` «mesa sella banda TOST/margen del piloto» · fila o nota de RANURA 2. ADR con todo (incluido el razonamiento de mesa y la respuesta de dirección). Estado (línea del duelo: «pre-registro sellado; L listas para correr; árbitro después de L»). Nota `-cierre`. Suite `--baseline` (🚫 jamás `--freeze`). Encargo `CONSUMIDO`. CONTADOR: cero, declarado.
> Lo que este acto NO hace
> No corre ninguna L. No computa ningún `R` ni CV. No toca el sorteo, el congelado ni los corredores (solo los hashea). No fija la banda por mesa. No decide quién corre L más allá de propagar la RANURA 2. Orden sagrado del diseño, repetido: hashes → L → R → scoring — jamás `R` antes de los hashes, y las sesiones L jamás ven `R`.

---

**Bloque VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2):**

- Estructura: `forense/prereg-duelo-v2/` existe con los cuatro corredores, el marco congelado, `sorteo-resultados-v1_0.md` y `banda-tost-margen-v1_0.md` — verificado por `ls` contra `9c25f28`.
- Contenido: ningún archivo del árbol contiene una salida de árbitro `R` — verificado por `find forense/prereg-duelo-v2 -iname "*arbitr*" -o -iname "*-R-*" -o -iname "*resultado-R*"` → vacío. Ningún archivo `forense/prereg-duelo-v2/prereg-corrida*.md` preexistía — verificado por `find` antes de escribir este acto.
- Cobertura retroactiva: no aplica — este acto no recomputa nada que ya exista; F1 hashea los cuatro corredores y los tres artefactos ya sellados (marco congelado, sorteo, `CONGELADO-v1_0.sha256`) tal como están, sin tocarlos.

## CONSUMIDO

Derivado mecánicamente por `/tramite` (puertas 1–3 de la acción 3.3): único merge que introduce este archivo y toca otros además de él — `PR #367` (`dad74ee7`, 2026-08-25, `Merge pull request #367 from Josanoforo/claude/prereg-corrida-setup-yeytx1`, 7 files changed).
