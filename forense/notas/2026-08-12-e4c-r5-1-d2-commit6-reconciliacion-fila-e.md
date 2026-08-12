# E4c · R5.1-D2 — Commit 6: reconciliación con la fila `E` sellada por ADR-71(b)

**No edita Commits 1, 3, 4 ni 5.** Mientras esta rama esperaba mesa, `origin/main` avanzó con ACTO M-6 (PR #178), que selló ADR-71 y apendizó una fila `E` real al pre-registro (`forense/r5-1-diseno-por-regla-preregistro-v1_0.md`, apéndice 12/ago/2026, citando explícitamente los Commits 4 y 5 de este acto). Ese apéndice responde, con autoridad de mesa, la misma pregunta sustantiva que Commit 1 §3 de este acto había declarado por su cuenta —qué significa que el falsador no refute— con una construcción distinta a la mía en un punto real. Se reconcilia aquí, no se ignora.

## 1 · Lo que ADR-71(b) selló — leído del apéndice real, no de memoria

Verbatim, `forense/r5-1-diseno-por-regla-preregistro-v1_0.md`, apéndice 12/ago/2026:

> **E** — DiD >20pp en al menos uno de los dos desenlaces, decisivo (IC95% que despeja el umbral por completo), y monto documentado como suficiente —la misma exigencia que ya pesa sobre A—, y identificación de §2 exitosa. Corroboración acotada... **Precedencia:** el orden pasa a ser A → E → B → C → D. La cláusula de "monto insuficiente" de B gana sobre E, exactamente como ya gana sobre A: si el monto no está documentado como suficiente, el resultado es B (ambiguo) sea cual sea la magnitud del DiD.

Tres hechos verificados contra el texto, no supuestos:

1. **Fila E es de un solo nivel.** No distingue "decisivo en uno de los dos desenlaces" de "decisivo en ambos" — ambos casos caen en la misma fila E, etiquetada uniformemente "corroboración acotada", nunca una fila más fuerte.
2. **La precedencia está decidida, y en el sentido contrario al que Commit 1 §3 de este acto había propuesto.** "Monto insuficiente" gana sobre E **sin excepción por magnitud del DiD**.
3. **No toca el registro de llaves.** El apéndice vive en el pre-registro, no en `forense/registro-llaves-identificacion-v1_0.md` — ese archivo sigue `SELLADA_NO_EJERCIDA`, sin fila E reflejada en su columna `escala` (que todavía dice textualmente "INCOMPLETA — no nombra el desenlace de no-refutación", ahora desactualizada frente al apéndice — no se corrige aquí, fuera de perímetro de este acto, el registro de llaves no está en la lista de archivos que este acto puede escribir).

**Confirmado sin resultado de por medio:** el propio ADR-71(b) declara "es pre-dato... ningún resultado de R5.1-D2 existe" — igual que todo lo que esta rama ha producido hasta ahora. No hay adjudicación que reabrir, no hay corrida que reconciliar.

## 2 · Reconciliación — mi declaración de dos niveles queda superada, no la precedencia

**Commit 1 §3 declaró, explícitamente como acto propio y no como enmienda al sellado:** dos filas nuevas, `EJERCIDA_ACOTA` (decisivo en uno de los dos desenlaces) y `EJERCIDA_CORROBORA` (decisivo en ambos, "la lectura más limpia que este diseño puede producir"). Esa declaración se hizo porque, al momento de escribirla, no existía ninguna resolución de mesa sobre la fila que le faltaba a la escala — y se dijo así, sin fingir autoridad que este acto no tiene sobre un documento sellado.

**Ahora existe esa resolución, y difiere en un punto concreto: fila E no tiene un nivel "corrobora" separado de "acota".** Se reconcilia, no se disputa — mesa tiene la autoridad que este acto declaró no tener:

- **`EJERCIDA_ACOTA` es la única fila de corroboración que aplica a R5.1-D2, decisivo en uno o en ambos desenlaces.** No hay `EJERCIDA_CORROBORA` propia de este diseño — la fila E del pre-registro no la contempla, y el registro de llaves no tiene mecanismo para que un acto ejecutor invente un nivel que el diseño sellado no declaró. Si Paso 3 corre y ambos desenlaces resultan decisivos, se reporta como `EJERCIDA_ACOTA` igual que si solo uno lo fuera — declarando en el propio resultado cuántos de los dos desenlaces cruzaron el umbral, como Commit 1 §3 ya pedía, pero sin promoverlo a un estado de registro distinto.
- **La regla de precedencia 2 que Commit 1 §3 proponía —un DiD decisivo grande gana sobre "monto insuficiente"— no se sostiene.** Commit 3 §4 ya la había retirado como regla vigente y la había reformulado como **propuesta a mesa, no autoadjudicada** — precisamente para no fijar por cuenta propia algo que le correspondía a mesa. **ADR-71(b) confirma la lectura contraria a la que Commit 1 §3 proponía**: monto insuficiente gana siempre, sin excepción por magnitud. La retirada de Commit 3 §4 queda validada por el resultado, no por el argumento que yo había ofrecido — que un DiD grande con monto pequeño apuntara al canal de elegibilidad en vez del canal de monto era una lectura razonable, pero no la que mesa selló. Se declara así, sin reescribir Commit 1 ni Commit 3 — el registro de que se propuso algo y mesa decidió otra cosa es, él mismo, el valor forense de no editar hacia atrás.

**Observación de forma, no de fondo, no corregida aquí:** el apéndice de ADR-71(b) se anexó inmediatamente después del cuerpo de §6, antes del separador que lleva a §7 — no dentro de "## 9 · Enmiendas", que es donde el propio §9 del pre-registro dice que debe vivir cualquier cambio a §6 ("cualquier cambio a... §6... posterior a la fecha del sello se anexa aquí"). §9 sigue mostrando "Ninguna a la fecha del sello" pese a que existe una enmienda real en el documento. Es una inconsistencia de ubicación dentro de un documento ya sellado por otro acto — no está en el perímetro de este commit tocar `forense/r5-1-diseno-por-regla-preregistro-v1_0.md` (perímetro del encargo de Commit 4, sin cambio), se declara para que quien audite el documento lo sepa.

## 3 · `folioviv` — el ítem que Commit 3 §3.4 dejó abierto ya se cerró, en otro acto

Commit 3 §3.4 encontró el defecto de `folioviv` en ENIGH 2018 (`poblacion`/`ingresos` pierden el cero inicial para entidades 01-09) y declaró explícitamente: *"cualquier acto previo de este repo que haya cruzado estas tres tablas de 2018 por `folioviv` sin este ajuste tiene el mismo punto ciego... se deja constancia para que mesa decida si amerita revisión aparte."*

**ACTO J (PR #180, fusionado) es esa revisión aparte, y generaliza el hallazgo correctamente:**

- Confirma los números de 2018 exactos a los de Commit 3 (83,070/269,206 `poblacion`, 30.86%; mismas nueve entidades).
- Encuentra que **2016 tiene el mismo defecto** (magnitud casi idéntica), no detectado por Commit 3 porque su perímetro era solo 2018/2022.
- Encuentra que **2012 NO está roto** — usa un esquema `folioviv` de 6 caracteres propio y autoconsistente, no un `C(10)` truncado; un `zfill(10)` ciego lo habría corrompido.
- El arreglo comprometido (`tests/r5_1_pension_bienestar.py::procesar_ola()`, `tests/p3_lca_data.py::construir_universo()`) generaliza el `zfill(10)` fijo de Commit 3 a un ancho derivado de la propia `concentradohogar` de cada ola — **cita explícitamente esta rama y el commit 3 como origen del hallazgo**, en el propio comentario del código.

**Verificado, no supuesto, que no hay divergencia:** esta rama nunca comprometió su `zfill(10)` a ningún archivo de `tests/` — vivió solo en el script de análisis local de Commit 3 (scratch, no commiteado) y en la nota. `git diff origin/main...e4c/r5-1-d2 -- tests/r5_1_pension_bienestar.py tests/p3_lca_data.py` da vacío antes de este merge — no había nada que reconciliar en código, y ahora, tras el merge de `origin/main` en este mismo commit, esta rama hereda el arreglo generalizado de ACTO J directamente.

**Reserva heredada, no adjudicada aquí:** ACTO J midió (sin re-adjudicar) que el join corregido mueve la brecha del falsificador de R5.1 (recepción declarada, ADR-58, veredicto `A` sellado) a menos de la mitad en 2016 y ~37% en 2018 — `R5.1→A` queda **expuesto**, no reabierto, por ese acto. Es una ficha distinta de `R5.1-D2` (Commit 1 §0 de este acto ya declaró la diferencia de diseño entre ambas), pero relevante como contexto para quien eventualmente compare los dos veredictos — no se toca aquí, fuera de perímetro.

## 4 · Lo que este commit no resuelve

- El registro de llaves (`forense/registro-llaves-identificacion-v1_0.md`) sigue sin reflejar la fila E ni la reconciliación de este commit — no está en el perímetro de este acto.
- La observación de forma sobre dónde vive el apéndice de ADR-71(b) (§2 arriba) se declara, no se corrige.
- La remediación oficial de `folioviv` (correr `r5_1_pension_bienestar.py --estratos` en modo oficial sobre las seis olas) sigue propuesta y sin ejecutar por ACTO J — decisión de mesa, no de este acto.
- Paso 3 de E4c (la corrida real) sigue diferido, ahora con la especificación completa: umbral (Commit 4), regla de hogar (Commit 4), clustering (Commit 4), varianza DDD (Commit 5, implementada en ACTO S/PR #179, ya fusionado a `main`), y ahora la fila E reconciliada (este commit). Lo único que sigue sin regla vigente es la propuesta original de precedencia 2 sobre "monto insuficiente" — que ya no hace falta resolver: ADR-71(b) la resolvió, en el sentido contrario al propuesto.

---

*Commit 6 de este acto (Bloque D). No edita Commits 1, 3, 4 ni 5. Reconcilia la declaración provisional de Commit 1 §3 con la fila E sellada por ADR-71(b) — `EJERCIDA_CORROBORA` propia de R5.1-D2 queda retirada, `EJERCIDA_ACOTA` es la única fila de corroboración vigente. Ningún resultado de R5.1-D2 se produce aquí.*
