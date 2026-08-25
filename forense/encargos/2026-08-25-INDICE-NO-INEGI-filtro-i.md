# `ACTO 4 · INDICE-NO-INEGI` — encargo archivado

| campo | valor |
|---|---|
| **SHA de redacción** | `f1ed541` (tip de `ACTO GEMELAS-20`) |
| **Entorno asignado** | **UBUNTU** — abre PDF y necesita red hacia los publicadores. NO nube |
| **ESTADO** | **CONSUMIDO** — 25/ago/2026, rama `indice-no-inegi` |
| **Fila que ejecuta** | `FP-146` (`L10`-`a`) |

## Bloque VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2)

**Estructura.** Existen al SHA de redacción: `forense/marco-candidatas-piloto-v1_0.tsv` (60 filas, 17 columnas,
con **8** en `PENDIENTE-FUERA-DE-INDICE`: `DIN-07`, `DIN-08`, `DIN-09`, `DIN-10`, `DIN-12`, `DOC-03`, `DOC-05`,
`DOC-06`), la fila `FP-146` y la `FP-134` del tablero, y
`forense/notas/2026-08-25-bibliotecario-56-cierre.md`.

**Contenido.** La premisa de `FP-134` —que los dos índices de `FP-93` son 100 % INEGI y por eso no alcanzan a
estas 8— **se verificó y se sostiene**, y además se probó por comando que la ECF **no** tiene programa en INEGI
(soft-404 idéntico al de un programa inventado, con control positivo). Los payloads de microdato de la ECF ya
estaban en corpus desde `P-LOTE-2`/`ADQ-15`, pero **microdato no es publicación**: lo que el filtro (i) pregunta
es si la cifra está **publicada**, y eso vive en los informes, que este acto localizó y abrió.

**Cobertura retroactiva.** `BIBLIOTECARIO-56` (`ADR-162`) corrió los dos pasos sobre 56 filas y dejó estas 8
declaradas fuera de alcance «por construcción, no por fallo de búsqueda». Ningún acto había construido el paso 1
fuera de INEGI.

## ARRANQUE (A.2, tres partes)

`sin_variable` · sonda `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → **200**
· `ls data/raw/ | head -1` → `2005trim1_csv.zip` (**321** entradas). `pgrep -af claude` → sólo el propio shell.

## Texto del encargo, verbatim

> **ACTO 4 · INDICE-NO-INEGI — ejecuta FP-146 (L10-a): el filtro (i) completo (Opus; contador: la columna publicada
> de las 8)**
>
> TAREAS: (1) construye el paso-1 del bibliotecario para las 8 filas PENDIENTE-FUERA-DE-INDICE con los
> índices/repositorios de sus publicadores (Banxico —incluida la Encuesta de Competencias Financieras—, CNBV, BMV,
> HR), universo declarado por índice (host, rutas, cuántas entradas); (2) paso-2 idéntico al de FP-93: abrir el
> archivo y buscar la cifra adentro, doble extractor en PDF; (3) escribe publicada = SI/NO en las 8 con evidencia;
> re-deriva el cuadro de la cuota (¿cuánto queda SI sobre 60 y sobre el marcador de 50?) y pégalo — alimenta
> directo al sorteo-v2; (4) FP-146 → ejecutada; fila A.12 solo si alguna resulta inevaluable con razón nueva.
> PERÍMETRO: forense/marco-candidatas-piloto-v1_0.tsv (solo la columna publicada de esas 8) · tablero · gobernanza
> · estado (cuadro de cuota en la línea de candidatas, paréntesis fechado) · nota 2026-08-25-indice-no-inegi.md ·
> encargo · scratchpad.

**Reglas comunes del pack, verbatim.**

> 🚫 --freeze · pgrep -af claude · iconv -f utf-8 -t utf-8 -c · ⚠️ [v2.11] A.13 en todo negativo · nada del espejo
> · ADR re-derivado, renumera si colisiona · recifrado con punto fijo · suite VERDE con tail · encargo CONSUMIDO ·
> fuera del perímetro: PARA.

## CONSUMIDO — resumen de ejecución

Paso 1 construido con **cuatro** índices de publicador (Banxico 10 entradas / 545 páginas · CNBV 297+48+48
enlaces · BMV 187 · HR 131). Paso 2 con **doble extractor**. Resultado: **5 `SI` · 3 `NO` · 0 pendientes** — el
filtro (i) queda **completo**. Cuadro de la cuota re-derivado y pegado en la línea de candidatas de `estado`:
**`SI` = 33 · `NO` = 27 · `PENDIENTE` = 0**, es decir **55.0 %** sobre 60 y **66.0 %** sobre 50 contra un tope del
**20 %** — cerrar el filtro **agravó** la cuota. **`A.12` no se abre**: ninguna resultó inevaluable con razón
nueva (la única razón nueva, el certificado intermedio ausente de CNBV, se resolvió). Defecto de `DIN-09`
reportado y **no** corregido por perímetro. Detalle: `forense/notas/2026-08-25-indice-no-inegi.md` · `ADR-172`.
