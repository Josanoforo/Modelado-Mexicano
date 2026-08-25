# Nota del acto — 2026-08-25-purga-2

`ACTO PURGA-2`, `ADR-176`. Destrucción del segundo espejo `~/BACKUP-mm-mirror-2026-08-10.git`, autorizada bajo la cadena que `ADR-173`/`FP-151` registra.

## 1 · La cadena, citada del árbol, no de memoria

El encargo pedía citar la cadena "del ADR de SELLA-G, archivo:línea" y el verbatim original de mesa que ese ADR registra. Son dos cosas distintas y no coinciden:

- `canon/gobernanza-v1_15.md:3571` (`ADR-173`): *"`FP-151` (segundo espejo, `~/BACKUP-mm-mirror-2026-08-10.git`) pasa a `FIRMADA` bajo la cadena `AUTORIZO DESTRUIR BACKUP-mm-mirror-2026-08-10.git`, único referente del registro"*.
- `forense/firmas-pendientes.tsv:149`, columna `firmada_en` de `FP-151`: el verbatim real que mesa dio fue *"ahora dame los encargos incluyendo: autorizo destruir backup etc etc"* — no la cadena exacta. El mismo texto de `SELLA-G` declara: *"el referente inequívoco es la cadena que `FP-151` exige... no existe otro backup en el registro"* — una inferencia de `SELLA-G`, verificada por `grep` antes de escribirse, no una cita textual.

Este acto no toma la inferencia por verbatim ni el verbatim por inferencia: reporta ambos. La compuerta de `PURGA-2` (ORDEN) pedía que la cadena "esté en el árbol" y que este acto "la cite del ADR, no de memoria ni de este encargo" — esa condición SÍ se cumple: `ADR-173` está fusionado (`PR #347`, `c502a43`, `origin/main`) y la cadena exacta vive ahí como conclusión registrada. La condición no exigía que el mensaje de mesa trajera la cadena letra por letra — a diferencia de la compuerta histórica de `mm-purga.git` (`ADR-113`/`FP-63`/`FP-143`), que sí lo exigía y que dos actos anteriores (`CAJA-RESIDUOS`, `FP63-CIERRA`) pararon dos veces por esa razón exacta. Son compuertas distintas, con lenguaje distinto; no se confunden.

## 2 · Re-verificación en fresco, antes de destruir

```
$ git -C ~/BACKUP-mm-mirror-2026-08-10.git count-objects -v
count: 0
size: 0
in-pack: 3053
packs: 1
size-pack: 12574
prune-packable: 0
garbage: 0
size-garbage: 0

$ git -C ~/BACKUP-mm-mirror-2026-08-10.git fsck --unreachable --dangling
(vacío — 0 líneas)

$ git -C ~/BACKUP-mm-mirror-2026-08-10.git for-each-ref | wc -l
167

$ ls ~/BACKUP-mm-mirror-2026-08-10.git/logs
No such file or directory

$ cat ~/BACKUP-mm-mirror-2026-08-10.git/objects/info/alternates
No such file or directory
```

Sin diferencia frente a lo que `FP-151` midió (in-pack=3053, 167 refs, 0 sueltos/garbage/prune-packable, sin `logs/` ni `alternates`). La forma es la misma; se procede.

## 3 · Destrucción y verificación de ausencia

```
$ rm -rf ~/BACKUP-mm-mirror-2026-08-10.git

$ ls -d ~/BACKUP-mm-mirror-2026-08-10.git
ls: cannot access '/home/pc0/BACKUP-mm-mirror-2026-08-10.git': No such file or directory
(exit 2)

$ test -e ~/BACKUP-mm-mirror-2026-08-10.git
(exit 1)
```

Ausencia confirmada por dos vías.

## 4 · Perímetro / entorno (A.2)

Entorno UBUNTU (el espejo vivía en disco local, no en la nube). `sin_variable`: este acto no toca ningún archivo de `milpa/` ni corre el motor. Sonda INEGI: no aplica (ninguna adquisición). `data/raw`: symlink a `/home/pc0/mm-corpus/raw`, presente y enlazado (`ls data/raw | head -1` → `2005trim1_csv.zip`); este acto no lo usa. `df -h`: 12M de disco recuperados (tamaño del espejo destruido).

## 5 · Cierre

`FP-151` recibe `ejecutada_en` (`forense/firmas-pendientes.tsv:149`). `ADR-176` (`canon/gobernanza-v1_15.md`). Una línea en `forense/hallazgos.md`. `canon/estado-programa-v1_10.md` recifrado 175→176 ADR y 134→133 WARN (dos declaraciones vigentes, T15/T16). Nota renombrada `2026-08-25-purga-2-cierre.md` (sufijo `-cierre` contra la autocolisión T02 con el nombre del encargo, mismo nombre base). Suite final:

```
$ python3 tests/check.py --baseline
...
19 FAIL · 133 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
(5 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

Encargo `forense/encargos/2026-08-25-PURGA-2.md` → `CONSUMIDO`.

Contadores de medición sobre México: **cero** — higiene de disco, tablero puro.
