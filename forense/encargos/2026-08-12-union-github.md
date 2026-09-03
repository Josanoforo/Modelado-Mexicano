# ENCARGO · NUBE · registrar el hallazgo `merge=union` vs. el botón de GitHub, y cerrar la pregunta que `.gitattributes` dejó abierta

- **SHA de redacción:** `f9e58e8` (merge #180)
- **Entorno asignado:** NUBE — no toca microdato ni red
- **Estado:** CONSUMIDO — PR de la rama `claude/new-session-xer383` (PR pedida: `mesa/union-vs-boton-github`), detalle en `forense/notas/2026-08-12-union-vs-boton-github.md`

---

12/ago/2026 · base declarada: `origin/main = f9e58e8` (merge #180) · suite **VERDE 22 FAIL · 104 WARN**, baseline congelado en `e7cd99d` — verificados por comando al escribir

> **PROCEDENCIA.** `.gitattributes:10-12` declara, desde el 5/ago/2026 (Encargo CU), una pregunta abierta textual: *"**Sin verificar:** si el botón 'Merge pull request' de GitHub honra este driver del lado servidor — la ruta garantizada es el merge local"*. Esa pregunta quedó respondida empíricamente el 12/ago en dos PRs. Este acto sube el hecho de observación a nota y **corrige el comentario que lo declara sin verificar** — que es donde el conducto de ADR-70(c) manda que aterrice, porque `.gitattributes` es la tabla consolidada de esta clase de restricción: es donde cualquiera va a mirar antes de fusionar.
>
> **Ninguna cifra de este encargo es criterio sin re-derivar en PASO 1.**

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

**ENTORNO ASIGNADO — y el que NO.** **NUBE.** Firma esperada `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` **sin sonda de red** — es la firma correcta de un acto de nube según ADR-59(b), no un desajuste. **Este acto no toca microdato ni red: dilo y salta el punto 4.** NO se lanza en caja local. NO en paralelo en otro entorno.

**PERÍMETRO.** SOLO: `.gitattributes` · `forense/notas/2026-08-12-union-vs-boton-github.md` (nuevo) · `forense/hallazgos.md` (append, 1 entrada) · `forense/encargos/2026-08-12-union-github.md` (copia literal de este encargo). **NO** toca `canon/`, `tools/`, `tests/`, `data/`, `milpa/`, ni ninguna rama viva. *Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.*

**CONCURRENCIA.** `e4c/r5-1-d2`, `mesa/s-svystat-4celdas` (#179) y `claude/cuatro-decisiones-firmadas-9z54wq` (#181) pueden estar vivas. Ninguna toca `.gitattributes` — **verifícalo**. Único solapamiento: `forense/hallazgos.md`, que resuelve `merge=union`… y que es, con ironía, exactamente el archivo de este hallazgo. **Tu propio merge va local, nunca por el botón** — y si te toca hacerlo, es evidencia adicional: anótala.

---

## PASO 1 · Premisas — corre y pega crudo

```bash
git log -1 --format="%h %s"                                   # f9e58e8 o posterior
git check-attr merge forense/hallazgos.md                     # esperado: merge: union
git check-attr merge canon/gobernanza-v1_15.md                # esperado: merge: unspecified
sed -n '10,12p' .gitattributes                                # el texto "Sin verificar" que este acto corrige
git diff --stat origin/main...origin/e4c/r5-1-d2 -- .gitattributes
git diff --stat origin/main...origin/mesa/s-svystat-4celdas -- .gitattributes
git diff --stat origin/main...origin/claude/cuatro-decisiones-firmadas-9z54wq -- .gitattributes
python3 tests/check.py --baseline                              # esperado: VERDE
```
**PARO si** alguna rama viva toca `.gitattributes`, o si `--baseline` arranca en ROJO.

---

## PASO 2 · La nota — `forense/notas/2026-08-12-union-vs-boton-github.md`

Corta, con estas seis cosas y nada más:

**1 · El hecho.** El botón "Merge pull request" de GitHub **no honra** el driver `merge=union` declarado en `.gitattributes`. Un PR cuya única divergencia es un append concurrente a `forense/hallazgos.md` se reporta como *"This branch has conflicts that must be resolved"* en la interfaz, **mientras el mismo merge en un clon local con `.gitattributes` en el árbol resuelve automáticamente y sin conflicto**.

**2 · El universo de la observación, declarado (A.4/A.5).** Dos PRs del 12/ago/2026: **#175** (`claude/new-session-zmjq8w`, ENCARGO C) y **#179** (`mesa/s-svystat-4celdas`, ACTO S). En ambos, el archivo reportado en conflicto por la interfaz fue exclusivamente `forense/hallazgos.md`. **Formulación obligatoria:** *observado por este programa en 2 PRs, ambos el 12/ago/2026, contra la interfaz web de GitHub en esa fecha.* No se afirma nada sobre otras fechas, otros repos, ni sobre por qué GitHub lo hace — no se sondeó su implementación y **el corte de entrenamiento no es fuente**.

**3 · El contraejemplo que acota el hallazgo, y es lo que impide sobre-generalizarlo.** **#178** también reportó conflicto, pero en `canon/gobernanza-v1_15.md` — archivo **sin** `merge=union` (`git check-attr` lo confirma: `unspecified`). Ese conflicto es **legítimo** y se reproduce igual en local. **#178 no es una instancia de este hallazgo.** Sin esta distinción, el hallazgo se leería como "GitHub conflictúa de más siempre", que es falso: conflictúa exactamente donde el driver habría ayudado y no se aplica.

**4 · La receta, que ya existía y solo estaba marcada sin verificar.** El merge se hace local, en un clon con `.gitattributes` en el árbol, **fusionando `main` HACIA la rama** y empujando; tras eso `main` queda como ancestro y el botón fusiona sin conflicto. Comandos y verificación, en el orden en que se corren:
```bash
git fetch origin && git checkout <rama> && git pull --ff-only origin <rama>
git merge --no-ff -m "Merge origin/main into <rama> — union driver local (GitHub no lo honra)" origin/main
sort forense/hallazgos.md | uniq -d | grep -v "^$"    # vacío — el modo de falla del union
python3 tests/check.py --baseline                      # comparar contra la línea base antes de empujar
git push origin <rama>
```

**5 · Lo prohibido, con su razón.** **No se usa el editor web de conflictos de GitHub** para archivos con `merge=union`: resuelve a mano, salta el driver, y es la vía por la que se viola la regla de `forense/hallazgos.md` de *"quien rebase re-aplica su entrada al final y jamás resuelve borrando la ajena"*. Un merge local con el driver conserva ambas entradas por construcción; el editor web depende de que quien lo use no se equivoque.

**6 · La condición del driver, revalidada en esta ocasión.** `merge=union` solo es seguro si el archivo **siempre termina en salto de línea** — si deja de cumplirse, dos ramas que apendicen a la vez duplican en silencio la última entrada compartida en vez de conflictuar. **Verifícalo tú, en esta sesión, y pega el resultado crudo:**
```bash
python3 -c "
import subprocess
for r in ['origin/main']:
    b=subprocess.run(['git','show',r+':forense/hallazgos.md'],capture_output=True).stdout
    print(r, 'termina en newline:', b.endswith(b'\n'))
"
```

---

## PASO 3 · `.gitattributes` — la pregunta abierta se cierra, el resto no se toca

Sustituye **solo** el fragmento de las líneas 10-12 que dice *"Sin verificar: si el botón 'Merge pull request' de GitHub honra este driver del lado servidor — la ruta garantizada es el merge local (`git merge`, con este archivo en el árbol)."*

Por, en el mismo estilo de comentario y sin reescribir el resto del bloque:

> `# VERIFICADO 12/ago/2026: el botón "Merge pull request" de GitHub NO honra`
> `# este driver del lado servidor -- dos PRs (#175, #179) reportaron conflicto`
> `# en forense/hallazgos.md en la interfaz mientras el mismo merge resolvía`
> `# limpio en clon local. La ruta garantizada, y la única, es el merge local`
> `# (git merge con este archivo en el árbol), fusionando main HACIA la rama.`
> `# NO usar el editor web de conflictos en archivos union: resuelve a mano y`
> `# es la vía por la que se borra la entrada ajena. Receta completa en`
> `# forense/notas/2026-08-12-union-vs-boton-github.md.`

**Las líneas 3-9 y 13-14 no se tocan**, ni el bloque de `hitoD-preregistro` de abajo. **Ningún archivo gana ni pierde `merge=union` en este acto.**

⚠️ **Después de editar `.gitattributes`, corre `git check-attr merge` sobre los dos archivos union y pega el resultado** — es un archivo que git parsea, y un comentario mal cerrado puede desactivar una regla en silencio. Es la única forma de comprobar que solo cambiaste prosa.

---

## PASO 4 · La entrada de `forense/hallazgos.md`

Una sola, fechada, con la forma que ya usan las del 12/ago. Debe contener, sin adornos: el hecho (GitHub no honra `merge=union`), el universo (2 PRs, #175 y #179, 12/ago), **el contraejemplo #178 y por qué no cuenta**, la receta en una línea con puntero a la nota, y que `.gitattributes` pasó de "sin verificar" a verificado.

**Y la línea que justifica que este acto exista**, porque es doctrina del propio programa: *un hallazgo que se queda en una nota y no llega a una receta no protege — se pagó dos veces antes de subirlo al archivo que la gente lee antes de fusionar* (ADR-69, corolario).

---

## PASO 5 · Cierre

Siete líneas. `--baseline` cruda en el cuerpo del PR. **PR `mesa/union-vs-boton-github`, NO FUSIONAR sin mesa.**

**Contadores de medición movidos: 0**, y está declarado: este acto no mide nada sobre México. Su entregable es que el siguiente PR no pierda una sesión averiguando lo mismo por tercera vez, y que nadie resuelva un conflicto de `hallazgos.md` por el editor web.

**Lo que este acto deliberadamente NO hace:** no añade ADR (no crea regla nueva — corrige un comentario que ya contenía la regla, marcada como no verificada) · no añade test (nada de esto es verificable desde la suite: el botón de GitHub vive fuera del repositorio, e instrumentarlo sería vigilar lo que el test no puede ver) · no cambia qué archivos son `union` · no toca `hitoD-preregistro`, que está fuera de `union` a propósito y por una razón escrita que sigue vigente.

## NO-EJECUTADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). Cero rastro: `grep -Fc -- "2026-08-12-union-github.md" canon/gobernanza-v1_15.md` → 0 · `git log --all --oneline --grep="2026-08-12-union-github.md"` → 0 · `git grep -Fl -- "2026-08-12-union-github.md"` (excluyendo forense/digesto/ y el propio archivo) → 0 resultados en los 327 ADR ni en el historial de commits. Sin nota de cierre, sin FP, sin cita posterior.
