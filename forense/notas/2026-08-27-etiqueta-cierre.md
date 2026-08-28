# Cierre — `ACTO MAESTRA31-E7 · ETIQUETA`

27/ago/2026. Encargo: `forense/encargos/2026-08-27-MAESTRA31-E7-ETIQUETA.md` (dirección, maestra-31, archivado por `A.3` antes de ejecutar). Regla congelada: `forense/notas/2026-08-27-etiqueta-regla.md` (COMMIT-1). Resultados: `data/inventario-reactivos-v1_1.tsv` y `data/cruce-inverso-v1_1.tsv` (COMMIT-2).

## Arranque (resumen)

Clon existente en `/home/user/Modelado-Mexicano`, rama `claude/etiqueta-inventario-raiz-luzdef`, `git status` limpio al empezar. `git log -1` = `9578ee6 Merge pull request #387 from Josanoforo/acto/maestra31-e6-diccionarios-fd`. **`main` se movió** de `f1b0d79` (base declarada del encargo) a `9578ee6` — `E6` fusionó en paralelo (`PR #387`, `ADR-215`, tal como el encargo anticipó); la rama de este acto arrancó ya sobre `9578ee6` (`git merge-base HEAD origin/main == 9578ee6 == HEAD`), sin diferencia adicional que resolver. `data/raw` ausente — no usado por este acto (sus dos insumos, `data/inventario-reactivos-v1_0.tsv` y `data/cruce-inverso-v1_0.tsv`, están versionados). `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, como se esperaba; sin red ni API. Ningún dato de este acto sale del espejo.

**Verificación de existencia de dirección, re-confirmada contra el archivo** antes de tocar nada: `103302` filas `(raiz)` (58% de `178246`), `119` payloads distintos, `458` filas `ENCUCI`, mecanismo en `tools/inventario_reactivos.py:125` — todo coincide exacto. **Una cifra del encargo no se sostuvo contra el archivo:** "16 de los 20 `EXISTE-NO-SATISFACE` citan `(raiz)`" es en realidad **20 de 20**, verificado por comando (`forense/notas/2026-08-27-etiqueta-regla.md`, §0). Se reporta la corrección; no cambia la lectura del encargo.

## A.13 — regla y control positivo (comando)

Regla congelada por familia+año, aplicada solo a las filas cuyo `instrumento` era `(raiz)` (`forense/notas/2026-08-27-etiqueta-regla.md`, §2). Resultado de la única corrida:

```
$ python3 deriva_instrumento_raiz.py
total payloads raiz: 119
resueltos: 80  no-resueltos: 39
```

39 de 119 (32.8%) van a `(sin-instrumento-derivable)` — bajo la mitad; la regla de tope de "una vuelta" no se disparó, y no se ajustó la regla tras ver el número. `ola` no se toca y no puede romperse: es una constante del extractor (`"ola": "NO_DETERMINADO"`, `tools/inventario_reactivos.py:110`, sin condicional), confirmado también contra el dato (`awk -F'\t' 'NR>1{print $4}' data/inventario-reactivos-v1_0.tsv | sort -u` → un solo valor). La premisa del encargo de que `ola` "se deriva hoy del mismo lugar" que `instrumento` no se sostiene contra el código: `ola` no se deriva de nada.

**Control positivo, tabla completa (no solo muestra):**

```
matched original non-raiz lines byte-for-byte: 74944 de 178247
original non-raiz lines NOT found unchanged in v1_1: 0
```

Las 74,944 filas cuyo instrumento ya era correcto en `v1_0` quedan byte a byte idénticas en `v1_1`, sin excepción.

## COMMIT-2 — las dos tablas y el delta

`data/inventario-reactivos-v1_1.tsv`: mismas 178,246 filas de `v1_0`, columna `instrumento` re-derivada para las 103,302 filas de raíz — 74,503 pasan a un instrumento real (80 payloads), 28,799 quedan en `(sin-instrumento-derivable)` (39 payloads). `data/inventario-reactivos-v1_0.tsv` queda SUPERADO en cabecera (comentario, sin editar datos); reproducible byte a byte desde `tools/inventario_reactivos.py`, que no se tocó.

`data/cruce-inverso-v1_1.tsv`: misma especificación congelada de `ACTO MAESTRA31-E5` (`forense/notas/2026-08-27-cruce-inverso-spec.md`), sin cambiar una palabra — mismas 59 variables, mismos `instrumentos_declarados_por_motor`/`n_citas_en_motor` (no dependen del insumo que cambió). Único insumo distinto: `v1_1` del inventario en vez de `v1_0`.

**Delta de veredictos** (comando: `awk -F'\t' 'NR>6{print $1,$2}'` sobre ambos archivos, comparado por `variable_id`):

| clase v1_0 → clase v1_1 | n |
|---|---|
| `EXISTE-NO-SATISFACE` → `EXISTE-SATISFACE` | **15** |
| `EXISTE-NO-SATISFACE` → `EXISTE-NO-SATISFACE` (sin cambio) | 5 |
| `NO-ENCONTRADO` → `NO-ENCONTRADO` (sin cambio) | 12 |
| `EXISTE-SATISFACE` → `EXISTE-SATISFACE` (sin cambio) | 27 |

**15 de 59 (25%) se mueven, todas en la misma dirección** (`EXISTE-NO-SATISFACE`→`EXISTE-SATISFACE`), todas por la misma causa: citaban `BD_ENCUCI2020_dbf.zip`, que pasó de `(raiz)` a `encuci2020`. Las otras 5 `EXISTE-NO-SATISFACE` no se mueven porque su instrumento declarado por el motor no tiene análogo en el corpus incluso ya reparado (p. ej. `ennvih`/`MxFLS`, confirmado ausente tras la corrección — ver enmienda a la nota de cierre de E5). Los 12 `NO-ENCONTRADO` no se mueven porque el defecto de etiqueta no cambia si un token existe o no como `variable_id` — solo cambia bajo qué instrumento aparece si existe.

**Lectura B-bis (declarada antes de ver el dato, en COMMIT-1):** un delta de 15/59 no es "casi ninguno" ni "la mayoría" — es una fracción visible (25%) pero acotada a una sola causa (ENCUCI). Esto **corrobora parcialmente ambas lecturas de COMMIT-1**: la contaminación de etiqueta sí era la causa real de una porción sustancial de los veredictos de E5 (no es un no-hallazgo), pero no fue la causa universal — las 12 `NO-ENCONTRADO` y las 5 `EXISTE-NO-SATISFACE` restantes tenían, y siguen teniendo, otra causa (instrumento genuinamente ausente del corpus, o token que no es una variable real). E5 midió razonablemente bien fuera del bolsillo ENCUCI.

**`n_olas_distintas` de los cuatro máximos publicados por E5:**

| variable | v1_0 | v1_1 | dirección |
|---|---|---|---|
| `P4_10` | 17 | **18** | infla (resuelve a instrumento nuevo, no contado antes) |
| `BP1_20` | 16 | **15** | desinfla (el payload de raíz resultó ser un instrumento ya presente en la lista — dedup) |
| `AP7_1` | 16 | 16 | sin cambio |
| `AP3_10` | 16 | 16 | sin cambio |

Se mueve en ambas direcciones, exactamente como predijo el encargo (§Contenido): el colapso de 119 payloads en `(raiz)` infla el conteo de las variables que solo vivían en el cubo, y desinfla el de las que además vivían en carpetas nombradas (porque `(raiz)` se contaba como una "ola" adicional distinta de las reales).

**Instrumentos distintos, sustituye al 74:** `109` instrumentos resueltos + `1` cubo declarado (`(sin-instrumento-derivable)`) = **110** categorías reportables en `instrumento`. El "74" de `FP-171`/`ADR-213` contaba `(raiz)` como uno de los 74; la cifra correcta de instrumentos reales identificables es 109 (no 74, no 110 — el cubo no es un instrumento).

## Lo que este acto no hizo

No re-extrajo ningún payload (`data/raw` no se abrió). No editó `tools/inventario_reactivos.py` ni ningún otro archivo de `tools/`. No cambió la especificación de `ACTO MAESTRA31-E5` — el cruce se re-corrió con la misma regla de emparejamiento, el mismo esquema de columnas, la misma escala A.4. No adjudicó qué significa el delta (si el programa debe promover algo a acto medidor, o si debe adquirir ENNViH/MxFLS) — eso queda para mesa vía `FP-174`. No integró `data/inventario-fd-v1_0.tsv` de `E6`. No usó red ni API.

## Frase de sello

«El primer resultado que produzca este procedimiento es el que se reporta.» — 15/5/12/27 sobre 59, delta = 15, instrumentos distintos = 109 (+1 cubo). Ninguno se ajustó después de verlo.
