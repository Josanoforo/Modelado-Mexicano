# MAESTRA37-INFRA-2 · Frente D — medición completa, cero enlaces nuevos

Corregido el PARO anterior: el corpus SÍ existe en esta máquina
(`/home/pc0/mm-corpus/raw`, symlinkeado en `data/raw`; `data/raices.local.yaml`
declara `descargas_mx`/`downloads`) — el worktree previo simplemente nunca
recibió el symlink/config (gitignorados, per-worktree). Corregido en
`~/mm-maestra37-infra2-frente-d`, rama `claude/maestra37-infra-2-frente-d`,
desde `origin/main` en `1c55a79` (merge de PR #522).

Compuerta de arranque completa: `python3 tools/curador_registro/baseline.py
data/curacion-registro` → `ok:true`; `python3 tests/check.py --baseline` →
VERDE.

## Medición previa a D (los 4 comandos obligatorios)

1. `relaciones.tsv`: **219 totales · 82 con `id_manifiesto` · 137
   `NO_DETERMINADO`** (coincide con la cifra de referencia sin corpus del
   documento de planificación).
2. `python3 -m tools.curador_registro.via_capa2 --root .` (lectura):
   `COINCIDE=83 · NO_COINCIDE=0 · AUSENTE=110 · SIN_PAYLOAD=0 ·
   RAIZ_NO_CONFIGURADA=0`. **Diffs propuestos: 0.** Diagnóstico auxiliar
   (nombre/alias, nunca identidad): 98 filas.
3. IDs explícitos citados en `relaciones.tsv` que no resuelven contra
   `data/manifiesto.yaml`: **0** (ya estaba en 0, se mantiene).
4. `python3 tests/corpus.py` (antes de tocar código): **304 WARN (C1=37 ·
   C2=0 · C3=267)**. Salida completa guardada en el journal de esta
   sesión (no comiteada aparte).

## D-A · Filas que ya tienen `id_manifiesto`

`via_capa2.py --root .` en lectura da **0 diffs propuestos** — las 83
filas `COINCIDE` (de 219 totales) ya están correctamente reflejadas en
`capa2_manifiesto`/`capa3_disco_real`; no hay nada legítimo que
`--escribe` promueva. Por indicación del AJUSTE DE DIRECCIÓN ("si
`via_capa2.py` no se modifica en este paso, no correr la suite completa
por esto — el comportamiento no cambió"), no se corrió `--escribe` (nada
que aplicar) ni se tocó el código de `via_capa2.py` para D-A.

## D-B · Filas sin `id_manifiesto` — búsqueda de evidencia estructurada exacta

Búsqueda exhaustiva de las tres vías que el AJUSTE permite (nunca el
diagnóstico por nombre/alias, que no es identidad):

**(a) SHA exacto ya comprometido** (`sha256_fuente` de una fila
`NO_DETERMINADO` que coincide con un `sha256` real del manifiesto):
**0 de 137** — las 137 filas `NO_DETERMINADO` tienen literalmente
`sha256_fuente=NO_DETERMINADO`; el campo no se usa en ningún lugar hoy
(confirma la corrección propia de la sesión de planificación, §1.1).

**(b) ID de manifiesto explícitamente citado en `evidencia_ref`/
`evidencia_textual_breve`/`nota`, aún no trasladado a `id_manifiesto`**:
búsqueda de substring contra las 1233 claves `id` reales del manifiesto
sobre las 137 filas `NO_DETERMINADO` — **60 filas** mencionan un id real
en su texto. Lectura íntegra de las 60 (no solo una muestra): **ninguna**
es un caso de "identidad ya fijada, falta copiar el campo". Se dividen
en dos orígenes, ambos actos previos que YA adjudicaron explícitamente
NO enlazar:

- **16 filas** (`[GEMELAS-20 2026-08-25] ADR-93 fila a fila: NO SE
  ENLAZA`): la fuente citada tiene una sola entrada en el manifiesto,
  compartida con su "fila gemela" que ya está `SI`/enlazada por otra vía;
  no hay una entrada *distinta* que citar, que es la condición literal
  que ADR-93 exige para enlazar la gemela restante.
- **4 filas** (`ADR-93 fila a fila: SE ENLAZA` — el veredicto semántico
  POSITIVO de GEMELAS-20): **tampoco cuentan.** La propia nota de estas 4
  filas lo declara verbatim y sin ambigüedad: *"Adjudicar no es enlazar:
  id_manifiesto=NO_DETERMINADO en las 22, luego via_capa2.py no puede
  promover ninguna, satisfaga o no la condición."* — GEMELAS-20 distingue
  expresamente entre su propio juicio analítico (¿el objeto de evidencia
  puede razonablemente asociarse con este payload?) y la escritura
  mecánica de `id_manifiesto` que exige identidad exacta verificable por
  `verificar_entrada()`. Tratar "SE ENLAZA" de ADR-93 como entrada válida
  de `--vincula` sería exactamente el error que D-B prohíbe: convertir
  una adjudicación semántica en certeza estructural.
- **40 filas** (`[ENLACE-2 2026-08-14]`): el payload citado SÍ existe en
  el manifiesto, pero cada nota documenta por qué no satisface la
  condición — contenido verificado que no es el que la necesidad reclama
  (p. ej. `r7_3_pub_beneficiarios_bienestar_csv`: agregado
  ENTIDAD×TRIMESTRE, no el inventario nominal que pide N28), múltiples
  candidatos sin que la fila fije cuál corresponde (5 payloads GPS,
  "la referencia analítica de la fila nunca fijó objeto"), o coincidencia
  de texto accidental ya señalada como tal (`r2_1_ecco_reporte_se_2023`:
  el "SE" de la sigla casa por accidente contra el pronombre reflexivo
  "se", y su `usado_para` real es R2.1, no R1.4/N21).

**(c) Decisión explícita de mesa ya registrada en nota forense para esa
relación puntual**: cubierta por (b) — las 60 filas anteriores SON esa
decisión explícita, ya registrada dentro de la propia fila (`nota`), no
en un documento aparte. Ninguna decisión adicional encontrada en
`forense/notas/` que apunte a una `relacion_id` específica no cubierta
arriba.

Las 77 filas `NO_DETERMINADO` restantes (137 − 60) no mencionan ningún id
de manifiesto en su texto — no hay evidencia de que se haya considerado
un candidato específico; permanecen `NO_DETERMINADO` sin más, correcto y
sin necesidad de una etiqueta especial (no son un caso de identidad
rechazada, son simplemente trabajo de fuente aún no hecho, fuera de
perímetro de este acto).

## Regla de bifurcación — resultado

**Enlaces nuevos exactamente resolubles: 0.** Por el AJUSTE DE DIRECCIÓN:
*"Si el número de enlaces nuevos exactamente resolubles es 0: no crear
`--vincula`. Declarar... y cerrar D después de D-A. Este es el resultado
esperado por defecto, no un fracaso."* No se modifica `tools/curador_registro/via_capa2.py`. No se escribe `relaciones.tsv`. No hace falta
recifrar `baseline.json` (D-sincronización solo aplica si D escribió
`relaciones.tsv`, y no lo hizo).

## D6 — `IDENTIDAD_NO_DEMOSTRADA`, declarado

Ninguna de las 137 filas `NO_DETERMINADO` queda muda: las 60 con
evidencia textual ya llevan, en su propia columna `nota`, la razón
concreta y específica de por qué no se adjudica (compartida con su
gemela, contenido no satisface, candidato múltiple sin fijar, colisión
de texto accidental) — más específica y verificable que una etiqueta
genérica `IDENTIDAD_NO_DEMOSTRADA` habría sido. Las 77 restantes son
ausencia de evidencia considerada, no identidad rechazada.

## Cierre

D-A: 0 diffs. D-B: 0 enlaces construibles. Cero cambios de código.
Este commit es puramente la medición y su cierre declarado.
