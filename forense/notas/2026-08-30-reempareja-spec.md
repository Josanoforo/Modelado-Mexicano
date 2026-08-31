# Especificación congelada · MAESTRA32-E4 · RE-EMPAREJA

COMMIT-1 del acto (`forense/encargos/2026-08-30-MAESTRA32-E4-RE-EMPAREJA.md`). Escrita **antes** de correr `tools/reempareja.py`. Este acto no inventa una búsqueda nueva: re-corre la spec congelada de `MAESTRA32-E2` (`forense/notas/2026-08-28-empareja-spec.md`, COMMIT-1) **verbatim** sobre un universo de reactivos ampliado. Todo lo que sigue es (a) el universo exacto, (b) la declaración de cero cambios de contenido frente a E2, (c) la elevación del código con su diff, y (d) el pre-registro B-bis, en ese orden — el mismo orden que exige el encargo.

## (a) · Universo exacto, re-derivado por comando

Comando (Python 3, UTF-8, salta las líneas de comentario `#` antes de contar — A.2/A.13):

```
$ python3 -c "
for f in ['data/inventario-reactivos-v1_2.tsv','data/inventario-reactivos-ext-v1_0.tsv','data/inventario-fd-v1_1.tsv']:
    with open(f, encoding='utf-8') as fh:
        lines = fh.readlines()
    ncomment = 0
    for l in lines:
        if l.startswith('#'):
            ncomment += 1
        else:
            break
    header = lines[ncomment].rstrip('\n')
    ndata = len(lines) - ncomment - 1
    print(f, 'comentarios=', ncomment, 'columnas=', len(header.split(chr(9))), 'filas_datos=', ndata)
"
data/inventario-reactivos-v1_2.tsv     comentarios=3 columnas=9 filas_datos=178246
data/inventario-reactivos-ext-v1_0.tsv comentarios=4 columnas=9 filas_datos=63345
data/inventario-fd-v1_1.tsv            comentarios=3 columnas=9 filas_datos=17094
```

Las tres tablas comparten el mismo esquema de 9 columnas (`payload_id`, `sha256_12`, `instrumento`, `ola`, `archivo_miembro`, `variable_id`, `texto_reactivo`, `metodo`, `universo_declarado`), verificado columna a columna por el comando de arriba (mismo `header.split('\t')` para las tres). Coincide exactamente con lo que la dirección declaró en la VERIFICACIÓN DE EXISTENCIA del encargo (63,345 filas en la tabla ext) — sin drift.

**Regla de concatenación (declarada aquí, aplicada tal cual en el código de (c)):** el universo de "tabla de reactivos" de este acto es `data/inventario-reactivos-v1_2.tsv` ∪ `data/inventario-reactivos-ext-v1_0.tsv`. Se concatenan como filas adicionales sobre el mismo espacio de búsqueda — **sin deduplicar por diseño**, porque un mismo `payload_id` no aparece en ambas tablas (v1_2 cubre el universo de `MAESTRA31-E4`/`MAESTRA32-E6`; ext-v1_0 cubre exclusivamente los 133 payloads causa B de `data/cobertura-composicion-v1_0.tsv` que `MAESTRA32-E3` v2 extrajo por primera vez, `ADR-228`). Cada fila candidata conserva su tabla de origen real (`v1_2` o `ext-v1_0`) en la columna `tabla` de la salida, para poder reportar deltas por tabla de origen en COMMIT-2. `data/inventario-fd-v1_1.tsv` entra sin cambios, exactamente como en la re-corrida de E6.

## (b) · Cero cambios de contenido frente a la spec de E2

Ningún término, regex, criterio de `CANDIDATO`, regla de circularidad ni orden de prioridad cambia frente a `forense/notas/2026-08-28-empareja-spec.md`. Cita archivo:sección de cada pieza que este acto reutiliza sin tocar:

- Método de búsqueda (Python/`csv`/UTF-8, normalización NFKD sin diacríticos, substring match, columnas exploradas): `forense/notas/2026-08-28-empareja-spec.md` §1 (líneas 20-22).
- Los 9 pares, su θ, su desenlace y su lista cerrada de términos: `forense/notas/2026-08-28-empareja-spec.md` §2 (líneas 24-82).
- Criterio de `CANDIDATO` (match + lectura de homónimo, `instrumento` nunca genera candidato por sí solo): `forense/notas/2026-08-28-empareja-spec.md` §3 (líneas 84-91).
- Criterio de co-observación (mismo valor exacto de `instrumento`, co-familia no basta): `forense/notas/2026-08-28-empareja-spec.md` §4 (líneas 93-95).
- Exclusión de circularidad, incluida la batería ENIF `P9_9_1..6`: `forense/notas/2026-08-28-empareja-spec.md` §5 (líneas 97-99).
- Prioridad de corrida (`G5.familismo_apoyo` → … → `G6.deferencia`): `forense/notas/2026-08-28-empareja-spec.md` §6 (líneas 101-113).
- Las 18 entradas de `DESCARTES` (excepciones DESCARTADO-con-razón), incluidas las dos claves que `ACTO MAESTRA32-E6` re-clavó de `"(raiz)"` a `"censo2020"`/`"enut2019"`: `forense/notas/2026-08-30-etiqueta-v1_2-cierre.md` (bloque de re-corrida, líneas 148-168 del bloque, preámbulo del propio bloque líneas 111-132). Este acto no re-clava ninguna clave nueva — el universo ampliado no introduce ningún homónimo adicional que la spec ya no cubriera por construcción (el criterio de `CANDIDATO`/`DESCARTES` opera por `(variable_id, instrumento, término)`, no por tabla de origen).

## (c) · Elevación del código: `tools/reempareja.py`

El bloque de re-corrida vivía **solo** dentro de `forense/notas/2026-08-30-etiqueta-v1_2-cierre.md:110-399` (verificado en el ARRANQUE del encargo: `tools/` no lo tenía, 0 hits sobre 77+ archivos). Se copia integro a `tools/reempareja.py`, con cita a la nota de origen en su propio encabezado. La única edición funcional permitida — **leer una tabla más** — se declara aquí completa:

```diff
 REACTIVOS = load("data/inventario-reactivos-v1_2.tsv")
+REACTIVOS_EXT = load("data/inventario-reactivos-ext-v1_0.tsv")
 FD = load("data/inventario-fd-v1_1.tsv")
-TABLAS = [("inventario-reactivos-v1_2", REACTIVOS), ("inventario-fd-v1_1", FD)]
+TABLAS = [
+    ("inventario-reactivos-v1_2", REACTIVOS),
+    ("inventario-reactivos-ext-v1_0", REACTIVOS_EXT),
+    ("inventario-fd-v1_1", FD),
+]
```

```diff
-    with open(f"{ROOT}/data/emparejamiento-motor-v1_1.tsv", "w", newline="", encoding="utf-8") as f:
-        f.write("# data/emparejamiento-motor-v1_1.tsv -- ACTO MAESTRA32-E6 · ETIQUETA-v1_2, COMMIT-2 (re-corrida)\n")
+    with open(f"{ROOT}/data/emparejamiento-motor-v1_2.tsv", "w", newline="", encoding="utf-8") as f:
+        f.write("# data/emparejamiento-motor-v1_2.tsv -- ACTO MAESTRA32-E4 · RE-EMPAREJA, COMMIT-2\n")
         (... cabecera de comentario re-escrita citando este acto y las tres tablas
              de entrada, mismo patrón que el bloque de E6 citaba a E2 ...)
```

Más un tercer cambio no funcional: dos líneas nuevas de `print(..., file=sys.stderr)` al final del `__main__`, que reportan `len(REACTIVOS)`/`len(REACTIVOS_EXT)`/`len(FD)` bajo el rótulo `FILAS_EXAMINADAS_POR_TABLA (A.13)` — no leen ni cambian ninguna decisión de candidato, solo hacen explícito para A.13 lo que ya estaba en memoria. `DESCARTES`, `PARES`, todas las listas `TERMINOS_*`/`DESENLACE_*`, `BATERIA_CIRCULAR_G5`, `norm`, `load`, `descarte_razon`, `recorte`, `buscar`, `veredicto_par`: copiadas de `forense/notas/2026-08-30-etiqueta-v1_2-cierre.md:133-336` sin editar un carácter.

## (d) · B-bis — pre-registro de falsación, antes de ver el dato

Un universo de reactivos más grande (v1_2 ∪ ext-v1_0, superset estricto de v1_2 solo) **no puede quitar** ninguna coincidencia que E2/E6 ya hubieran encontrado sobre v1_2 solo — cada fila que E6 vio sigue exactamente igual en la tabla concatenada, y `buscar()` es un superconjunto monótono de comparaciones (más filas exploradas, nunca menos). Por lo tanto, para cada uno de los 9 pares:

- El veredicto A.4 de este acto **solo puede subir o quedarse igual** frente a `data/emparejamiento-motor-v1_1.tsv` (`NO-ENCONTRADO` → `EXISTE-NO-SATISFACE` → `EXISTE-SATISFACE`, nunca al revés).
- **Si algún par baja de veredicto frente a v1_1, es un bug de este script (no un resultado) y el acto PARA** antes de escribir COMMIT-2 — no se reporta como hallazgo, se corrige o se declara bloqueo.
- **`0` de `9` movimientos es un resultado informativo válido**, no un fallo del acto — y se reporta junto con el techo de etiqueta de la tabla ext ya cuantificado por la dirección: 18,390 de las 63,345 filas de `inventario-reactivos-ext-v1_0.tsv` (29.0%) traen `instrumento = "(sin-instrumento-derivable)"`, y el criterio de co-observación (§4 arriba) exige instrumento identificado — esas filas, aunque generen `CANDIDATO`, nunca pueden por sí solas mover un par a `EXISTE-SATISFACE`. Un `0` de movimientos no se lee como "la tabla ext no sirvió"; se lee contra ese techo.
- **`≥1 EXISTE-SATISFACE` nuevo habilita un medidor de caja sucesor — no lo ejecuta este acto.** Este acto no mide, no abre microdato, no calcula β̂ ni α; solo re-corre la búsqueda de candidatos y sella el veredicto A.4 por par.

El primer resultado que produzca este procedimiento es el que se reporta.
