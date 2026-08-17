# ENCARGO B · NUBE · `svystat.diff_ultimate_cluster` — el estimador de contraste que E4c necesita para adjudicar

- **SHA de redacción:** `bfc0037` (merge de #170) · **Entorno asignado:** NUBE. **NO** la caja local Ubuntu CC — ahí corre E4b, y este acto no toca microdato ni `data/raw`. · **Estado:** CONSUMIDO — PR #172 ("Add diff_ultimate_cluster and did_ultimate_cluster estimators"). *(Re-verificado 17/ago/2026, ACTO E-HIG/HIGIENE-VIVOS: `git merge-base --is-ancestor 0ce39cd f3873c2` OK; `tests/svystat.py` ya trae `diff_ultimate_cluster`/`did_ultimate_cluster`, y ACTO S construyó `diff4_ultimate_cluster` encima. La clasificación de partida lo daba por "gateado por ley de mesa" [presunción no verificada] — el propio encargo cierra declarando "no mueve ningún contador sustantivo: entrega el mecanismo, no la medición", nunca fue una cifra de canon que gatear. Detalle en `forense/notas/2026-08-17-higiene-vivos.md` §2(iii).)*
- **Bloquea a:** E4c, commit 2. Sin esto, E4c puede reportar cuatro puntos pero no puede adjudicar, porque su umbral se decide con el intervalo de confianza del contraste y ese intervalo hoy no se puede calcular.

**PROCEDENCIA.** Verificado con comando contra un clon de `bfc0037` el 11/ago/2026. `tests/svystat.py` exporta **una sola función pública**, `prop_ultimate_cluster`, para una proporción. `tools/curador_registro/produce.py::taylor_distribution` emite un solo `tipo_producto`, hardcodeado a `DISTRIBUCION_DESCRIPTIVA` en sus tres ramas. `grep -rlniE "diferencia_en_diferencias|dif_en_dif|\bdid\b|contraste|covarianza|linealiz"` sobre `tests/` y `tools/` devuelve dos archivos y **ambos son la palabra "contraste" en prosa** (`tests/calx_g3.py:176`, `tests/calg3_fasec.py:487`), ningún estimador. No existe estimador de contraste en el programa.

**El problema, en una frase.** `R5.1-D2` es diferencias-en-diferencias por grupo de elegibilidad, ENIGH 2018 → 2022. Las dos olas son muestras independientes y sus varianzas se suman sin más. **Dentro de una ola no**: tratamiento y comparación salen de la misma muestra y comparten estratos y UPM, así que `var(p_T − p_C) ≠ var(p_T) + var(p_C)`. La covarianza es en general distinta de cero y su signo no es predecible antes de mirar. Sumar varianzas produce un error estándar equivocado, y como el umbral del §6 se evalúa con el intervalo, un SE equivocado produce un veredicto equivocado que se ve bien.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · `git log -1 --format="%h %s"` · `git status` ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. **Este acto no la necesita**: todo se valida contra datos sintéticos construidos en el propio test. Reporta si existe o no y sigue.

4 · ENTORNO. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` · `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/`. Reporta los dos valores crudos. NUNCA `curl -I`. Este acto no toca microdato ni red; los valores son para dejar la firma del entorno registrada. Sigue con cualquier resultado.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

**PERÍMETRO Y CONCURRENCIA.** SOLO escribe: `tests/svystat.py` (añade función, **no modifiques `prop_ultimate_cluster`**) · `tests/test_svystat.py` (añade casos) · `forense/notas/2026-08-12-estimador-contraste.md` (nuevo) · `forense/hallazgos.md` (append) · `forense/encargos/2026-08-12-B-estimador-contraste.md` (copia literal de este encargo). **NO** toca `tools/`, `canon/`, `milpa/`, `data/`, `tests/check.py`, `.github/`, ni ningún otro archivo de `tests/`. En la caja local puede estar corriendo E4b: perímetro disjunto salvo `forense/hallazgos.md` — si al rebasar hay conflicto ahí, re-aplica tu entrada al final y jamás resuelvas borrando la ajena. Si te encuentras escribiendo fuera de esta lista, PARA.

---

## PASO 1 · Verificación de premisas

```bash
git log -1 --format="%h %s"                                    # esperado bfc0037 o posterior
grep -n "^def " tests/svystat.py                               # esperado: prop_ultimate_cluster y _caso_conocido, nada más
grep -c "diff_ultimate_cluster" tests/svystat.py               # esperado 0 (si >=1, PARA: alguien ya lo escribió)
grep -n "test_svystat" .github/workflows/verify.yml            # confirma que el test YA está gateado por CI
python3 tests/test_svystat.py                                  # esperado: pasa hoy, antes de tocar nada
python3 -c "import numpy" 2>&1 | tail -1                       # esperado: ModuleNotFoundError
```

El último importa: **no hay numpy ni scipy**. Todo en stdlib puro, mismo estilo que el archivo existente (`math`, listas, diccionarios).

## PASO 2 · La matemática, escrita antes de codificar

Escribe `forense/notas/2026-08-12-estimador-contraste.md` con la derivación **antes** de tocar el código. No es ceremonia: es lo que permite que el revisor compruebe la fórmula sin leer Python.

**Estimando dentro de una ola.** Con `T` y `C` mutuamente excluyentes:

```
N̂_T = Σ wᵢ·1{i∈T}          p_T = Σ wᵢ·yᵢ·1{i∈T} / N̂_T
N̂_C = Σ wᵢ·1{i∈C}          p_C = Σ wᵢ·yᵢ·1{i∈C} / N̂_C
d = p_T − p_C
```

**Residual linealizado por unidad** — es el corazón del asunto, porque es lo que captura la covarianza:

```
zᵢ = 1{i∈T}·wᵢ·(yᵢ − p_T)/N̂_T  −  1{i∈C}·wᵢ·(yᵢ − p_C)/N̂_C
```

**Agregación por UPM y varianza de conglomerado último**, idéntica en forma a la que ya vive en el archivo:

```
z_hi = Σ_{i ∈ UPM (h,i)} zᵢ
var(d) = Σ_h [ m_h/(m_h−1) · Σ_i (z_hi − z̄_h)² ]
```

**Y la regla que hay que escribir explícita, porque es donde se equivoca todo el mundo:** las unidades que no pertenecen ni a `T` ni a `C` aportan `zᵢ = 0` y **permanecen en el archivo**. No se filtran. Filtrarlas cambia la estructura de estratos y UPM, puede convertir estratos en singleton artificiales y altera los grados de libertad del diseño. Esto es estimación de dominio, no submuestreo.

**DiD entre olas independientes:**

```
θ = d_post − d_pre
var(θ) = var(d_post) + var(d_pre)
```

La suma es válida **solo** porque ENIGH es transversal repetida y las dos olas son muestras independientes — el §4 del pre-registro de `R5.1-D2` lo declara así de forma explícita (*"No es panel. ENIGH es transversal repetida — 2018 y 2022 son muestras independientes, no las mismas personas."*). Cita esa línea en la nota. Si alguna vez se aplica a un panel, esta suma deja de valer y el estimador no sirve: escríbelo como límite declarado de la función.

## PASO 3 · El código

Dos funciones nuevas en `tests/svystat.py`, con docstring del mismo estilo que la existente (fórmula citada, límites declarados, referencia a Wolter).

**`diff_ultimate_cluster(rows)`** — `rows` es un iterable de `(estrato, upm, peso, y, grupo)` con `y ∈ {0,1}` y `grupo ∈ {"T", "C", None}`. Devuelve un dict con al menos: `d_hat`, `p_T`, `p_C`, `se`, `ic95`, `n_upm_total`, `n_estratos`, `n_estratos_singleton`.

**`did_ultimate_cluster(rows_pre, rows_post)`** — devuelve `theta_hat`, `d_pre`, `d_post`, `se`, `ic95`, y los contadores de singleton de cada ola por separado, sin colapsar.

Cuatro decisiones de diseño que hay que tomar y **declarar en el docstring**, no dejar implícitas:

1. **Política de singleton: replica la de `prop_ultimate_cluster`** — salta el estrato y lo cuenta en `n_estratos_singleton`. Devuélvelo siempre y di en el docstring que el llamador **debe** leerlo, porque un singleton no detectado baja el SE en silencio. Declara también, sin unificarlas en este acto, que `tools/curador_registro/produce.py::taylor_distribution` adopta la política contraria (lanza `ESTRATOS_UNA_UPM` y aborta): son dos políticas para la misma condición en el mismo programa, y eso es un hallazgo que se anota, no algo que este acto resuelva.
2. **Cuantil normal:** usa `1.959963985`, el mismo que `prop_ultimate_cluster`, no `1.96`. (`taylor_distribution` usa `1.96`; los resultados de las dos vías no coincidirán en los últimos dígitos y eso es esperado — anótalo.)
3. **`rows` se recorre dos veces.** El archivo existente ya tuvo ese problema y lo resolvió con `rows = list(rows)` y un comentario. Haz lo mismo y por la misma razón: un generador se agotaría en el primer recorrido y fallaría en silencio.
4. **Grupo vacío:** si `N̂_T = 0` o `N̂_C = 0`, devuelve `None`, igual que hace `prop_ultimate_cluster` con `N̂ = 0`. No lances excepción y no devuelvas cero.

## PASO 4 · Los tres casos conocidos — el corazón del acto

Van en `tests/test_svystat.py`, **que ya está gateado por CI** (`.github/workflows/verify.yml:64`). Añadir ahí, y no en un archivo nuevo, deja el estimador vigilado sin tocar el workflow.

**Caso 1 · Forma cerrada exacta, SRS.** Un solo estrato, una UPM por observación, pesos uniformes `w=1`, grupos `T` y `C` disjuntos, ninguna unidad fuera de grupo. Entonces `z̄ = 0` y la fórmula colapsa a:

```
var(d) = [n/(n−1)] · [ p_T(1−p_T)/n_T + p_C(1−p_C)/n_C ]      con n = n_T + n_C
```

Es exacto, no aproximado. **Exige coincidencia a 1e-9**, igual que los casos existentes. Deriva a mano el valor esperado en el docstring del test con números concretos, como hace `test_caso_sintetico_dos_estratos`.

**Caso 2 · Coherencia con el estimador que ya existe.** Con todas las unidades en `T` y ninguna en `C`, `diff_ultimate_cluster` debe devolver `d_hat` y `se` **idénticos** a `prop_ultimate_cluster` sobre las mismas filas. Es la prueba de que el estimador nuevo no contradice al viejo donde se solapan. Exige igualdad a 1e-12.

**Caso 3 · La covarianza importa, y se demuestra.** Construye un caso sintético donde `T` y `C` están correlacionados dentro de UPM — por ejemplo, UPMs donde una `y` alta en `T` va acompañada de una `y` alta en `C`. Calcula por un lado `diff_ultimate_cluster` y por otro `sqrt(var_T + var_C)` usando `prop_ultimate_cluster` sobre cada grupo por separado. **Deben diferir de forma visible**, y el test debe afirmar que difieren. Reporta ambos números en la salida.

Este tercer caso es el que justifica que la función exista. Sin él, alguien en tres meses borra el estimador pensando que sumar varianzas bastaba.

**Caso 4 (opcional, si sale barato) · Invariancia a las unidades fuera de grupo.** Añadir filas con `grupo=None` en las mismas UPM no debe cambiar `d_hat`, y el efecto sobre `se` debe ser el que la fórmula predice, no cero por casualidad.

## PASO 5 · `forense/hallazgos.md` — una entrada

Qué función se añadió y por qué; que el programa no tenía estimador de contraste, con el universo del grep que lo estableció; los tres casos conocidos y su tolerancia; las dos políticas de singleton que conviven sin unificar; y que esto desbloquea el commit 2 de `R5.1-D2`. Sin narrar el proceso.

## PASO 6 · Archivar el encargo

Copia este archivo completo y literal a `forense/encargos/2026-08-12-B-estimador-contraste.md`, con la cabecera de `forense/encargos/convencion.md` (SHA · entorno · estado `VIVO`).

## PASO 7 · Suite, git, PR — NO FUSIONAR

Corre **los dos**: `python3 tests/test_svystat.py` (el que CI gatea) y `python3 tests/check.py --baseline`. Los casos nuevos deben pasar; la línea base debe seguir verde. Si `check.py` levanta una entrada nueva por el archivo de nota, **se reporta con su texto crudo, jamás se silencia**.

Rama `estimador/diff-ultimate-cluster`. Commits: (1) la nota con la derivación, (2) el código y los tests. **En ese orden**: la fórmula se declara antes de que exista la implementación que podría haberla sugerido. PR: *"ESTIMADOR: svystat.diff_ultimate_cluster + did_ultimate_cluster, tres casos conocidos en el test gateado por CI — desbloquea commit 2 de R5.1-D2 — NO FUSIONAR sin mesa"*.

## PASO 8 · Cierre — siete líneas

Qué cambió · por qué importa · qué habilita (el commit 2 de E4c, y con él la posibilidad de adjudicar `R5.1-D2`) · qué falta (unificar la política de singleton entre `svystat` y `produce.py`, si mesa lo quiere; extender a medias y razones, si algún día hace falta) · pruebas (salida cruda de los dos runners) · reservas (el DiD suma varianzas solo bajo olas independientes — límite declarado en el docstring) · y **di explícitamente que este acto no mueve ningún contador sustantivo: entrega el mecanismo, no la medición.**
