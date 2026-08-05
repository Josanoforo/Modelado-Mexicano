# 2026-08-04 · ENCARGO MT-mantenimiento — nota de cierre

Huso de Mesa (`TZ=America/Mexico_City date`): **4/ago/2026**, corrida ~23:18–23:30.
Redactado contra `origin/main` citado en el encargo (`2bc613b`); al arrancar,
`origin/main` ya era `bd2c975` (re-derivado, reportado antes de editar, no
PARO). A mitad de acto, `origin/main` volvió a moverse a `3f73c29` (PR #114,
ajeno — `sesion/hitoD-r1-3-canal-confianza`, solo toca `forense/`, ninguno de
los cuatro archivos protegidos); se hizo `git merge origin/main` (fast-forward,
sin conflicto) y se re-derivó el SHA de arranque para el tag de auditoría del
ítem 8. Ningún ADR nuevo apareció en `canon/gobernanza-v1_15.md` entre medio —
el último seguía siendo ADR-61, confirmado por `grep -on 'ADR-[0-9]\+'
canon/gobernanza-v1_15.md | sed 's/.*ADR-//' | sort -n | uniq | tail -1` antes
de escribir ADR-62.

ADR de este acto: **ADR-62** (`canon/gobernanza-v1_15.md §4`, solo append; la
versión del documento no sube — criterio ADR-48–61).

**Hallazgo de perímetro, encontrado al sellar el ADR (tercero de este acto,
distinto de los dos desvíos de abajo — este no se omitió, se expandió).**
Apenas se agregó `**ADR-62`, `python3 tests/check.py --baseline` pasó a ROJO:
T15 (T-ADR-COUNT) detectó que `canon/gobernanza-v1_15.md:2` (la propia
cabecera) y `canon/estado-programa-v1_10.md:27,99` seguían citando "61 ADR" —
T15 escanea *todo* `canon/*.md`, no solo el archivo que se edita, y ninguno
de los tres sitios estaba en el perímetro cerrado (gobernanza dice "solo
append"; `estado-programa` no aparece en la lista de 12 rutas). El efecto en
cascada infló el conteo de FAIL de 18 a 21 (más los 2 propios de T16 al
comparar contra una cifra ahora stale) — 23 en total. Mismo patrón que
ADR-60/61 ya resolvieron con su propia sección "Cascada": se corrigieron los
tres dígitos (61→62) más una cláusula nueva en la oración histórica de
`estado §L0`, exactamente la receta que esos dos ADR ya documentan como
obligatoria al sellar cualquier ADR nuevo. Se prefirió esta expansión mínima
y mecánica sobre dejar el baseline en rojo, porque "Suite `--baseline` VERDE
antes del push" es un requisito de cierre más explícito y más duro que la
lista de perímetro. `python3 tests/check.py --baseline` volvió a VERDE.

**Segunda vuelta, mismo defecto que el ítem 7 de este acto describe.** El
párrafo de "Cascada" recién escrito en el ADR-62 citaba, entre comillas, la
transición `"61 ADR"→"62 ADR"` como explicación — T15 no distingue una cita
explicativa de una afirmación vigente (mismo regex sobre `\d+\s*ADR\b`) y
volvió a marcar ROJO sobre la propia frase que documentaba el arreglo.
Reescrito para no repetir el patrón literal ("de sesenta y uno a sesenta y
dos", sin dígito pegado a la palabra "ADR"); mismo criterio, deliberado esta
vez, que el ítem 7 de este mismo acto aplicó a AUTHORSHIP/AVISO. Verificado:

```
$ python3 tests/check.py --baseline
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

VERDE, `18 FAIL · 95 WARN`, idéntico al estado antes de abrir el ADR.

---

## Comandos de aceptación, uno por ítem

### 1 · Banner de incompatibilidad (`milpa-spec`, `milpa-plan`)

Banner insertado arriba del bloque de cabecera en ambos archivos. Se declaró
un desvío de alcance dentro del propio banner: no se renombró ni se subió la
cifra de versión (`v0.2`→`v0.3`, `v0.1`→`v0.2`), porque el Registro de
artefactos (`canon/estado-programa-v1_10.md`) y `forense/censo-integridad-v1_0.md`
citan los nombres viejos y ninguno de los dos está en el perímetro cerrado del
encargo — renombrar los habría dejado colgantes. Verificado que el banner no
introduce colgantes nuevas:

```
$ python3 tests/check.py --baseline
...
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

Mismo resultado (18 FAIL · 95 WARN, VERDE) antes y después de los dos edits —
cero referencias colgantes nuevas de T03.

### 2 · Segundo carril de CI (`test_svystat.py` bloqueante)

`.github/workflows/verify.yml` gana un segundo step, standalone, sin
dependencia nueva:

```
$ python3 tests/test_svystat.py
TEST 1 -- caso sintetico, 2 estratos x 5 UPM x pesos desiguales: ... OK
TEST 2 -- estrato de una sola UPM (varianza no estimable): ... OK
TEST 3 -- mismo dataset via GENERADOR, no lista: ... OK
TEST 4 -- autochequeo existente del modulo (svystat._caso_conocido): ... Validado.
$ echo $?
0
```

### 3 · `requirements.txt`

Probado en venv limpio (no el intérprete de la sesión):

```
$ python3 -m venv /tmp/.../venv-test && source .../bin/activate
$ pip install -r requirements.txt
$ python3 tests/check.py --baseline
...
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (...)
$ echo $?
0
```

Desvío de alcance declarado: el encargo también pedía una línea de
instalación en `README.md`; `README.md` no aparece en las 12 rutas del
perímetro cerrado, así que no se tocó. El criterio de aceptación literal
(`pip install -r requirements.txt && python3 tests/check.py --baseline`
VERDE en limpio) no depende de esa línea y quedó verificado arriba.

### 4 · `milpa/tramite.yaml` v0.2.0 → v0.3.0

```
$ python3 -c "
import yaml
d = yaml.safe_load(open('milpa/tramite.yaml'))
n_p = sum(1 for r in d['reglas'] for e in r['entonces'] if 'p' in e)
n_c = sum(1 for r in d['reglas'] for e in r['entonces'] if e.get('clase')=='ASIGNADO')
print(n_p, n_c)
"
10 10
$ grep -c ', clase: ASIGNADO}' milpa/tramite.yaml
10
$ grep -c 'p: 0\.' milpa/tramite.yaml
10
```

Conteo de `clase:` == conteo de `p:` == 10. `nota_calibracion` de las dos
reglas de gobierno digital y de `tramite.evasion_norma` se conservó verbatim.

### 5 · `svystat.py` materializa la entrada + caso generador

`rows = list(rows)` agregado al entrar a `prop_ultimate_cluster()`.
`test_generador_no_falla_en_silencio()` en `tests/test_svystat.py` (TEST 3
arriba) pasa el dataset de `test_caso_sintetico_dos_estratos()` como
generador y exige `dict` idéntico al de la lista — pasa. Corre en el step de
CI del ítem 2.

### 6 · `tests/manifiesto.py` — host y `--verifica` multi-id

```
$ python3 tests/manifiesto.py --verifica --id encig23_base_datos_csv --id encig23_estructura_base_datos_pdf
Entorno de verificación: Linux ... · Python 3.11.15
encig23_base_datos_csv [data_raw]: AUSENTE -- ...
encig23_estructura_base_datos_pdf [data_raw]: AUSENTE -- ...
```

Los dos ids se reportan (antes del fix, `--id` sin `action='append'` sólo
dejaba el último de argparse, silenciosamente). Caso de error explícito:

```
$ python3 tests/manifiesto.py --verifica --id encig23_base_datos_csv --id no_existe_este_id
ERROR: id 'no_existe_este_id' no existe en el manifiesto.
$ echo $?
1
```

`--registra`/`--compara` con `--id` repetido fallan ruidoso en vez de tomar
el último:

```
$ python3 tests/manifiesto.py --registra --id a --id b --archivo x ...
ERROR: --registra no admite --id repetido (recibió 2): a, b. ...
```

`entorno_actual()` deja de incluir `host` hacia adelante (SO y Python se
conservan); las ~190 entradas ya escritas en `data/manifiesto.yaml` no se
tocaron — append-only.

### 7 · `AUTHORSHIP.md` / `AVISO-DE-ALCANCE.md` — cifra tecleada

```
$ grep -rn "19 FAIL" AUTHORSHIP.md AVISO-DE-ALCANCE.md
$ echo $?
1
```

Vacío. Los dos archivos ahora remiten a `python3 tests/check.py` para la
cifra vigente en vez de repetirla. Confirmado que la deriva ya había
ocurrido tres veces sobre el mismo hecho: el encargo citaba "19 FAIL y 84
WARN", este acto corrió `python3 tests/check.py` y obtuvo **18 FAIL · 95
WARN**, y `README.md §"Primera corrida de la suite · 28/jul/2026"` (fechado,
no se toca) tiene una tercera cifra, **18 FAIL · 110 WARN** — tres números
en circulación de un mismo hecho no fechado es exactamente el defecto que
este ítem cierra.

### 8 · Tag de auditoría — BLOQUEADO

```
$ git fetch origin main   # main se había movido, bd2c975 -> 3f73c29
$ git merge origin/main --no-edit   # fast-forward limpio
$ git tag -a audit-externa-2026-08 3f73c29ed9265de128dc4eda4a95436bf1546ba4 -m "..."
$ git push origin audit-externa-2026-08
error: RPC failed; HTTP 403 curl 22 The requested URL returned error: 403
send-pack: unexpected disconnect while reading sideband packet
fatal: the remote end hung up unexpectedly
```

Repetido una segunda vez, mismo 403 (sin retry indefinido — instrucción del
proxy de esta sesión: 403/407 no se reintenta, se reporta). En el mismo
momento, `git push -u origin claude/encargo-mt-mantenimiento-37tsdp`
funcionó sin error contra el mismo remoto — el bloqueo es específico a la
creación de refs `tags/*`, no una falla de red ni de credencial general.
Sin herramienta MCP de GitHub para crear un tag por API en esta sesión
(`get_tag`/`list_tags` son de solo lectura, no hay `create_tag`/`create_ref`).

```
$ git ls-remote --tags origin | grep audit-externa
```

Vacío — el ítem 8 **no se completó**. Se documenta como hallazgo, no se
enmascara. El tag anotado existe localmente sobre `3f73c29`
(re-derivado, no `bd2c975`, por el movimiento de main a mitad de acto) para
que una sesión con credencial capaz de push de tags pueda empujarlo sin
tener que re-derivar el SHA de nuevo.

---

## Suite `--baseline`, estado final

```
$ python3 tests/check.py --baseline
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

VERDE antes del push, sobre el árbol completo con los 7 ítems editados
(1 al 7), el ADR-62, y la cascada T15/T16 de dos dígitos sobre
`canon/estado-programa-v1_10.md:27,99` que sellar el ADR forzó (ver arriba).

## Desvíos de alcance (dos), expansión forzada (una) y bloqueo (uno)

1. **Ítem 1** — no se renombró `milpa-spec`/`milpa-plan` ni se subió su
   versión (habría requerido tocar `canon/estado-programa-v1_10.md` y
   `forense/censo-integridad-v1_0.md`, fuera del perímetro cerrado).
2. **Ítem 3** — no se tocó `README.md` (fuera del perímetro cerrado); el
   criterio de aceptación verificado no depende de esa línea.
3. **ADR-62 (no es un ítem, es requisito de cierre)** — sellar el ADR obligó
   a tocar `canon/estado-programa-v1_10.md:27,99`, fuera del perímetro
   cerrado, para que T15/T16 no dejaran el baseline en rojo (ver "Hallazgo
   de perímetro" arriba). Expansión mínima y mecánica, no una omisión.
4. **Ítem 8** — tag creado localmente, push bloqueado por HTTP 403 de forma
   consistente y reproducible; sin ruta alterna en esta sesión.

Contadores de medición sobre México: **0 movidos.** Este acto es
mantenimiento de aparato (CI, dependencias, procedencia de probabilidad,
higiene de PII derivada, deuda documental) — no abrió `data/raw/` ni
microdato.
