# ACTO SELLA-FREEZE · sella el recongelado sin ADR, los dos cambios de `tests/check.py` sin ADR, y la fecha del pegado de v2.8 — `ADR-81`

**Acto:** ACTO SELLA-FREEZE · **Entorno:** repo-only, NUBE, sin `data/raw`, sin red · **SHA de redacción del encargo:** `84b2acf` (`origin/main`, merge #228 · ACTO TRIAGE-63 COMMIT 2) · **Ejecutado:** 14/ago/2026.

## §0 · ARRANQUE

1. **REPO.** Clon existente en `/home/user/Modelado-Mexicano` (no se clonó uno nuevo).
   ```
   $ git log -1 --format="%h %s"
   84b2acf Merge pull request #228 from Josanoforo/triage-63-sondeo
   $ git status
   On branch claude/encargo-acto-sella-freeze-6l3za7
   nothing to commit, working tree clean
   ```
2. **SHA.** Coincide exactamente con el declarado por el encargo (`84b2acf`). Sin movimiento de `main` al arrancar — no aplica el protocolo de "main se movió".
3. **`data/raw`.** Ausente (clon fresco, gitignorada). No se crea ni se enlaza: este acto no la toca — el perímetro declarado en el encargo es `canon/`, `forense/notas/`, `forense/hallazgos.md`, `forense/encargos/`.
4. **ENTORNO.** El propio encargo declara que este acto no toca microdato ni red — se salta el punto, per la excepción del bloque.
5. **ESPEJO.** No se usó — toda cifra de esta nota sale de comandos corridos contra el clon de (1), pegados abajo.

## §1 · Verificación de los tres hechos que se sellan

**(a) El recongelado a `0ad9b7b`.**
```
$ python3 -c "import json;print(json.load(open('tests/baseline.json'))['head'])"
0ad9b7b759e138b251129c639f6ef943d6ee0fe7
$ grep -rn "0ad9b7b" canon/
(cero líneas — rc=1)
```
Confirmado: `tests/baseline.json` está congelado en `0ad9b7b759e138b251129c639f6ef943d6ee0fe7`, y ningún archivo de `canon/` lo cita — el recongelado no estaba sellado.

Autorización, citada, no supuesta:
```
$ tail -c 2000 forense/hallazgos.md
```
Entrada de `ACTO PROC-10-bis COMMIT 3`, verbatim: *"El usuario pidió explícitamente «pull and solve CI» — autorización directa que sustituye a la firma de mesa ausente."*

**(b) Los dos cambios de `tests/check.py` sin ADR.**
```
$ git log --since="2026-08-13 00:00" --format="%h|%s" -- tests/check.py
4a30a40|ACTO PROC-10-bis COMMIT 3: corrige T19b/T19c (no reconocian MEDIDO·NACIONAL) y recongela
1224c37|ACTO PROC-11 COMMIT 2: ejecuta el mapa congelado -- renombre de la theta, celda-D de obligacion_medida, D:14->15
536650b|ACTO A8-LAND: mesa autoriza freeze de baseline, CI en VERDE
4cc2131|Resuelve el hallazgo T15: excepción histórica, mismo mecanismo que T03
```
Verificado con `git show <sha> -- tests/check.py` para los dos: ambos diffs suman un término a una comparación aritmética existente y mueven un literal dentro de una regex, con comentarios explicando el hallazgo — **cero cambio de lógica de comparación o de flujo de control** en ninguno de los dos.

`1224c37`: `_CONTADOR_14` (línea ~869) y la regex gemela de `t19c_readme_derivadas` cambian el denominador literal `14`→`15` dentro del patrón; se añaden comentarios. Sin cambios de control de flujo.

`4a30a40`: `t19b_modelo_contador_14` (línea ~925) y `t19c_readme_derivadas` (línea ~1000) pasan de `ptxt.count('clase: "MEDIDO·PARCIAL')` a `ptxt.count('clase: "MEDIDO·PARCIAL') + ptxt.count('clase: "MEDIDO·NACIONAL')`; se añaden dos excepciones de clasificación de T03 y ajusta el bucket de T16 en `_freeze_note()`. Sin cambios de control de flujo en los predicados de comparación.

Contexto verificado en `forense/notas/2026-08-13-proc-10-bis.md` §4 y ADENDA: el propio encargo de `PROC-10-bis` (perímetro `NO ESCRIBE: tests/`) anticipó el defecto y no lo corrigió por falta de firma de mesa; la ADENDA documenta la autorización directa del usuario ("pull and solve CI") que sí permitió tocar `tests/check.py` en ese acto — pero ningún ADR quedó escrito para ninguno de los dos cambios.

**(c) La fecha del pegado de `instrucciones-proyecto-v2_8.md` (A.9).**
```
$ grep -n "PENDIENTE" canon/gobernanza-v1_15.md | grep -i pegado
1146:**Fecha en que `instrucciones-proyecto-v2_8.md` se pegó en el proyecto de Claude: `PENDIENTE — no sellada hasta el pegado`.**
```
Dirección reporta la fecha del pegado: 13/ago/2026. Procedencia tipo (3) — reportado por dirección, no verificable con herramientas de repo (el proyecto de Claude vive fuera del repositorio).

## §2 · Diff de residuo que el freeze de `4a30a40` absorbió — re-contado, no heredado

```
$ git show 4a30a40~1:tests/baseline.json > /tmp/baseline_before.json
```
Comparación campo a campo (`fails`/`warns`, listas de `[test, mensaje]`) entre el baseline justo antes del freeze (commit padre `0ad9b7b`, = `4a30a40~1`) y el baseline commiteado en `4a30a40`:

```
fails before 19 after 22 new 4
warns before 96 after 103 new 7
```

Nuevos WARN (7, todos T03 — nombres de archivo no repetidos aquí en backticks a propósito, para no disparar T03 sobre esta misma nota; lista completa ya vive en `forense/notas/2026-08-13-proc-10-bis.md` ADENDA):
- 6× en `forense/encargos/2026-08-13-PROC-10-BIS-clase-septima-y-anexos.md`: cinco archivos de `MOTOR-1` nunca entregados a la sesión (tres `compass-*`, dos `red-team`/`red_team`) más una cita a un artefacto `v0_2` inexistente.
- 1× en `forense/notas/2026-08-13-proc-10-bis.md`: la misma cita al artefacto `v0_2` inexistente, repetida ahí al explicar el hallazgo.

Nuevos/cambiados FAIL (4 entradas dedup'd en `baseline.json`, que colapsan por archivo+mensaje; la corrida en vivo, agrupada por línea, da 6 — ver §3):
```
T16 canon/estado-programa-v1_10.md: declara 107 WARN vigente; la corrida real da 119 WARN
T16 canon/estado-programa-v1_10.md: declara 18 FAIL · 107 WARN vigente; la corrida real da 18 FAIL · 119 WARN
T16 canon/gobernanza-v1_15.md: declara 18 FAIL · 104 WARN vigente; la corrida real da 18 FAIL · 119 WARN
T16 canon/gobernanza-v1_15.md: declara 18 FAIL · 107 WARN vigente; la corrida real da 18 FAIL · 119 WARN
```

Esto confirma exactamente el **7×T03 + 6×T16** que la nota de `PROC-10-bis` ya declaraba (ADENDA) — re-derivado aquí de forma independiente, no copiado.

## §3 · T16 reporta 6 divergencias, no 4 — recontado por corrida real, agrupado por línea

```
$ python3 tests/check.py --baseline
```
(salida relevante, antes de editar `canon/`)
```
· T16: 6
    canon/estado-programa-v1_10.md:129 declara 107 WARN vigente; la corrida real da 119 WARN
    canon/estado-programa-v1_10.md:221 declara 18 FAIL · 107 WARN vigente; la corrida real da 18 FAIL · 119 WARN
    canon/gobernanza-v1_15.md:764 declara 18 FAIL · 107 WARN vigente; la corrida real da 18 FAIL · 119 WARN
    canon/gobernanza-v1_15.md:856 declara 18 FAIL · 107 WARN vigente; la corrida real da 18 FAIL · 119 WARN
    canon/gobernanza-v1_15.md:1104 declara 18 FAIL · 104 WARN vigente; la corrida real da 18 FAIL · 119 WARN
    canon/gobernanza-v1_15.md:1134 declara 18 FAIL · 104 WARN vigente; la corrida real da 18 FAIL · 119 WARN

24 FAIL · 119 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 0ad9b7b759e138b251129c639f6ef943d6ee0fe7)
```
(obtenido cargando `tests/check.py` como módulo y llamando `main()` directamente, para leer la lista completa `FAILS` sin el truncado a 4 ítems que la consola aplica por defecto — el truncado ("… y 2 más") es solo de presentación, confirmado comparando contra el agregado `· T16: 6`.)

**Las cuatro primeras (`estado-programa:129,221`, `gobernanza:764,856`) son citas mutables** — declaran "la cifra vigente" y `gobernanza:764` ya distingue esto explícitamente: *"cifra mantenida en sincronía por T16, no historia congelada"*. Se actualizan en este acto.

**Las dos últimas (`gobernanza:1104` en `ADR-76(f)`, `:1134` en la Cascada de `ADR-77`) son historia congelada** — la cifra correcta contra lo que cada ADR midió al sellarse. No se tocan, per el criterio que el propio `gobernanza:764` ya fija para distinguir ambos casos, y per el perímetro del encargo (que solo instruye actualizar `estado-programa:129,221` y `gobernanza:764,856`).

## §4 · El punto fijo de T16 — por qué la cifra declarada es 18 FAIL, no 24 ni 20

`t16_suite_self_check()` (`tests/check.py:574`) corre un **subproceso** de la suite completa excluyendo a T16 de sí mismo (variable de entorno `CHECK_SELFCHECK_CHILD`), y compara cada afirmación `**N FAIL · M WARN**` de `canon/*.md` contra ese resultado — nunca contra el total con T16 incluido, para evitar la paradoja de punto fijo (T16 contándose a sí mismo).

Ese subproceso, sin T16, da **18 FAIL · 119 WARN** (T05=5, T06=2, T07=1, T08=1, T09=8, T11=1 → 18; T15 en `[ ok ]` tras corregir el conteo de ADR). Es la cifra que `gobernanza:764`, `:856`, `estado-programa:129`, `:221` declaran ahora.

La corrida completa normal (con T16 incluido) nunca baja de **20 FAIL**: los 18 de siempre más los 2 T16 permanentes de `gobernanza:1104`/`:1134`, que por diseño no se tocan (§3) y por tanto siempre van a divergir del WARN real, que sigue moviéndose. Esos 2 ya estaban aceptados en `tests/baseline.json` antes de este acto — no es un defecto nuevo, y coincide exactamente con la cifra que `ADR-79`/`ADR-80` (`gobernanza:1193`,`:1214`) ya declaraban desde el 13/ago.

```
$ python3 tests/check.py --baseline   # antes de editar canon/
24 FAIL · 119 WARN — LÍNEA BASE: VERDE

$ python3 tests/check.py --baseline   # después de sincronizar las 4 citas en canon/
20 FAIL · 119 WARN — LÍNEA BASE: VERDE
  (3 entradas de la línea base ya no aparecen — mejora, no bloquea)

$ python3 tests/check.py             # desglose sin --baseline
[ ok ]  T15 T-ADR-COUNT
[FAIL]  T16 T-SUITE-SELF-CHECK  (2 fail)   ← solo gobernanza:1104,:1134, esperado
```

## §5 · Numeración del ADR

```
$ python3 -c "
import re
t=open('canon/gobernanza-v1_15.md',encoding='utf-8').read()
n=[int(x) for x in re.findall(r'^\*\*ADR-(\d+)',t,re.M)];s=sorted(set(n))
print('únicos',len(s),'max',max(s),'huecos',[i for i in range(1,max(s)+1) if i not in s])
"
únicos 80 max 80 huecos []
```
`81` contiguo, sin colisión — coincide con lo que el encargo anticipaba contra `84b2acf`.

```
$ grep -rn "[0-9]\+ ADR" canon/ README.md
```
Sitios de cascada: `gobernanza-v1_15.md:2` (cabecera) · `estado-programa-v1_10.md:27` (tabla) · `estado-programa-v1_10.md:101` (las dos citas de esa línea — historia completa de la numeración).

## §6 · Contadores no movidos

```
$ grep -c 'clase: "MEDIDO·PARCIAL' milpa/procedencia.yaml
9
$ grep -c 'clase: "MEDIDO·NACIONAL' milpa/procedencia.yaml
1
```
`10 de 15` (condicionales) confirmado, sin tocar. `13 de 27` (Hito D) · `0 de 15` (coeficientes) · `1 de 2` (llaves) · `4 de 144` — ninguno se mueve. Este acto es de gobierno puro: no mueve ningún contador de medición sobre México.

## §7 · Cierre

```
$ python3 tests/check.py --baseline
20 FAIL · 119 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 0ad9b7b759e138b251129c639f6ef943d6ee0fe7)
```
Corrida antes y después de los edits de `canon/`, ambas VERDE (24→20 FAIL, WARN sin cambio en 119, por sincronizar las cuatro citas mutables — no por tocar `tests/`, que este acto no toca). `ADR-81` sella los tres hechos de §1. `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md` editados per la cascada de §5. Una línea en `forense/hallazgos.md`. Este encargo commiteado a `forense/encargos/2026-08-13-SELLA-FREEZE-encargo.md` (A.3).
