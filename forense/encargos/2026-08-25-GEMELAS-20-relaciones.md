# `ACTO 3 · GEMELAS-20` — encargo archivado

| campo | valor |
|---|---|
| **SHA de redacción** | `654a940` (tip de `ACTO SERIE-HOMOGENEA-CODI`) |
| **Entorno asignado** | **UBUNTU** — el pack completo va a Ubuntu; este acto lee tablas del árbol y el material del curador |
| **ESTADO** | **CONSUMIDO** — 25/ago/2026, rama `gemelas-20` |
| **Fila que ejecuta** | `FP-24` (su sustancia; la política estaba sellada desde `ADR-93`) |

## Bloque VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2)

**Estructura.** Existen al SHA de redacción: `data/curacion-registro/relaciones.tsv` (199 filas, 19 columnas),
`data/curacion-registro/evidencias.tsv`, `data/curacion-registro/ejecucion-semantica/barrido2/`
(`tareas-semanticas-barrido2.tsv`, `cobertura-fuentes-barrido2-detalle.tsv`), `tools/curador_registro/via_capa2.py`,
`tools/curador_registro/schemas/adjudication-proposal.schema.json`, y en `canon/gobernanza-v1_15.md` los
`ADR-93`, `ADR-95`, `ADR-109` y `ADR-128`.

**Contenido.** La premisa del encargo —«las 20 filas con par (ENSAFI 9 · ENFIH 8 · ENBIARE 3)»— **se sostiene**:
re-derivada contra el árbol, la partición reproduce exacta. Lo que el encargo no dice es que hay **22**
`SI_O_REFERENCIADO`, no 20: las 2 restantes son los PDF `MHB` que `ADR-109(a)` ya había apartado.

**Cobertura retroactiva.** `ADR-109` (18/ago) adjudicó estas mismas 20 **por fuente** y dejó dicho que «no cierra
`FP-24`». `ADR-168(e)` (25/ago) la dio por ya ejecutada vía `FP-46`. Ninguno de los dos escribió la adjudicación
**fila a fila** dentro de `relaciones.tsv`, que es lo que `ADR-93` reservó a acto propio y lo que este acto hace.

## ARRANQUE (A.2, tres partes)

`sin_variable` · sonda `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → **200**
· `ls data/raw/ | head -1` → `2005trim1_csv.zip` (**321** entradas). `pgrep -af claude` → sólo el propio shell.

## Texto del encargo, verbatim

> **ACTO 3 · GEMELAS-20 — la adjudicación fila-a-fila que FP-24/FP-46 reservan a acto propio (Opus; contador:
> cero)**
>
> TAREAS: (1) lee la regla sellada (ADR-93, texto en la fila FP-24) y las 20 filas con par de
> data/curacion-registro/relaciones.tsv (ENSAFI 9 · ENFIH 8 · ENBIARE 3 — re-deriva el conteo); (2) por par: abre
> los descriptores de ambos objetos en corpus y adjudica bajo la regla (¿mismo dato real → cuál fila gobierna,
> cuál se marca subordinada?), con cita por adjudicación; nada por parecido de nombre — el criterio del propio
> curador; (3) escribe la adjudicación en la columna que la regla mande (derívala del esquema del curador);
> (4) FP-24 → ejecutada; reporte fila-a-fila en la nota, con las que NO se pudieron adjudicar (descriptor
> insuficiente → veredicto A.4 + qué falta). PERÍMETRO: data/curacion-registro/relaciones.tsv · tablero ·
> gobernanza · estado · nota 2026-08-25-gemelas-20.md · encargo · scratchpad.

**Reglas comunes del pack, verbatim.**

> 🚫 --freeze · pgrep -af claude · iconv -f utf-8 -t utf-8 -c · ⚠️ [v2.11] A.13 en todo negativo · nada del espejo
> · ADR re-derivado, renumera si colisiona · recifrado con punto fijo · suite VERDE con tail · encargo CONSUMIDO ·
> fuera del perímetro: PARA.

## CONSUMIDO — resumen de ejecución

Conteo re-derivado y reproducido (**ENSAFI 9 · ENFIH 8 · ENBIARE 3**, más 2 fuera de las 20). Adjudicación fila a
fila con el criterio del propio curador y cita por fila: **4 SE ENLAZA · 16 NO SE ENLAZA · 2 `A.4`
inadjudicables**. Escrita en la columna `nota` — no en `capa2_manifiesto` ni en `clasificacion_relacion`, porque
*adjudicar no es enlazar*. Control con la herramienta del curador: **0 diffs de `capa2`**. Dos hallazgos: la
adjudicación por fila **no reproduce** la de `ADR-109(b)`, que fue por fuente, y `id_manifiesto` sigue
`NO_DETERMINADO` en **22 de 22**, lo que hace la condición **necesaria pero no suficiente**. Desviación declarada:
la cláusula se escribió en las **22** y no sólo en las 20, para no dejar dos filas mudas en el mismo archivo.
Detalle: `forense/notas/2026-08-25-gemelas-20.md` · `ADR-171`.
