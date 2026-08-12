# `merge=union` vs. el botón de GitHub — verificado, receta cerrada

**Por qué existe.** `.gitattributes:10-12` declaraba, desde el 5/ago/2026 (Encargo CU), una pregunta abierta: si el botón "Merge pull request" de GitHub honra el driver `merge=union` del lado servidor. Esta nota sube esa pregunta de "sin verificar" a verificada y archiva la receta que ya existía pero no estaba marcada como probada.

## 1 · El hecho

El botón "Merge pull request" de GitHub **no honra** el driver `merge=union` declarado en `.gitattributes`. Un PR cuya única divergencia es un append concurrente a `forense/hallazgos.md` se reporta como *"This branch has conflicts that must be resolved"* en la interfaz, **mientras el mismo merge en un clon local con `.gitattributes` en el árbol resuelve automáticamente y sin conflicto**.

## 2 · El universo de la observación, declarado (A.4/A.5)

Dos PRs del 12/ago/2026: **#175** (`claude/new-session-zmjq8w`, ENCARGO C) y **#179** (`mesa/s-svystat-4celdas`, ACTO S). En ambos, el archivo reportado en conflicto por la interfaz fue exclusivamente `forense/hallazgos.md`. **Formulación obligatoria:** observado por este programa en 2 PRs, ambos el 12/ago/2026, contra la interfaz web de GitHub en esa fecha. No se afirma nada sobre otras fechas, otros repos, ni sobre por qué GitHub lo hace — no se sondeó su implementación y el corte de entrenamiento no es fuente.

Corroboración independiente encontrada al revisar el propio cuerpo de PR #178 (verificado con la API de GitHub en esta sesión, no solo citado): su descripción ya afirma, sobre su propio merge local de `origin/main`, *"nunca el botón de GitHub — mismo criterio verificado en #175, GitHub no honra el driver del lado servidor"* — el hallazgo ya estaba registrado de forma dispersa antes de este acto; lo que faltaba era subirlo a `.gitattributes`, que es donde cualquiera mira antes de fusionar.

## 3 · El contraejemplo que acota el hallazgo

**#178** también reportó conflicto, pero en `canon/gobernanza-v1_15.md` — archivo **sin** `merge=union` (`git check-attr` lo confirma: `unspecified`). Ese conflicto es **legítimo** y se reproduce igual en local (el propio cuerpo de #178 lo documenta: *"conflicto real (ambas ramas tocaron los mismos sitios de cascada)"* en `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md`, resuelto a mano). **#178 no es una instancia de este hallazgo.** Sin esta distinción, el hallazgo se leería como "GitHub conflictúa de más siempre", que es falso: conflictúa exactamente donde el driver habría ayudado y no se aplica.

## 4 · La receta, que ya existía y solo estaba marcada sin verificar

El merge se hace local, en un clon con `.gitattributes` en el árbol, **fusionando `main` HACIA la rama** y empujando; tras eso `main` queda como ancestro y el botón fusiona sin conflicto. Comandos y verificación, en el orden en que se corren:

```bash
git fetch origin && git checkout <rama> && git pull --ff-only origin <rama>
git merge --no-ff -m "Merge origin/main into <rama> — union driver local (GitHub no lo honra)" origin/main
sort forense/hallazgos.md | uniq -d | grep -v "^$"    # vacío — el modo de falla del union
python3 tests/check.py --baseline                      # comparar contra la línea base antes de empujar
git push origin <rama>
```

## 5 · Lo prohibido, con su razón

**No se usa el editor web de conflictos de GitHub** para archivos con `merge=union`: resuelve a mano, salta el driver, y es la vía por la que se viola la regla de `forense/hallazgos.md` de *"quien rebase re-aplica su entrada al final y jamás resuelve borrando la ajena"*. Un merge local con el driver conserva ambas entradas por construcción; el editor web depende de que quien lo use no se equivoque.

## 6 · La condición del driver, revalidada en esta ocasión

`merge=union` solo es seguro si el archivo **siempre termina en salto de línea** — si deja de cumplirse, dos ramas que apendicen a la vez duplican en silencio la última entrada compartida en vez de conflictuar. Verificado en esta sesión, crudo:

```bash
python3 -c "
import subprocess
for r in ['origin/main']:
    b=subprocess.run(['git','show',r+':forense/hallazgos.md'],capture_output=True).stdout
    print(r, 'termina en newline:', b.endswith(b'\n'))
"
```
```
origin/main termina en newline: True
```
