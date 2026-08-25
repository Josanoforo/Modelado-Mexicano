# ACTO MARCO-SATURA-CODEX — nota de cierre (24/ago/2026)

Encargo: `forense/encargos/2026-08-24-MARCO-SATURA-CODEX.md`. Firma que ejecuta:
`FP-82`/`ADR-135(d)` (*"Se amplía a saturación para eso creamos una
infraestructura completa en CODEX, no para desperdiciarla"*), sucesor directo
del PARO de `ACTO AMPLIA-MARCO-SATURA`/`ADR-148`, gatillado por `FP-121`
(`ACTO SELLA-AGO24-D`, mesa 24/ago/2026, respuesta 1).

**Resultado: PARO.** El marco NO se amplía en este acto. `FP-82` sigue
`FIRMADA`, `FP-93` sigue `ABIERTA`. `60` de `60` sin movimiento. No es el
mismo PARO que `ADR-148`: aquí la infraestructura CODEX **sí se localiza**
(confirma la enmienda de `SELLA-AGO24-D`), pero es el curador equivocado para
este dominio.

## ARRANQUE

1. **Repo.** Clon existente `/home/pc0/Modelado-Mexicano`, worktree nuevo
   `/home/pc0/mm-marco-satura-codex`, rama `acto/marco-satura-codex`.
2. **SHA.** `git log origin/main --oneline -1` → `f154fd9`, "Merge pull
   request #321 from Josanoforo/recenso-diseno-2" — condición de `⛔ ORDEN`
   (tras fusionar `RECENSO-DISEÑO-2`) confirmada satisfecha, tal como
   dirección ya la había verificado.
3. **data/raw.** `ln -s /home/pc0/mm-corpus/raw data/raw` (mismo patrón que
   `ACTO ADQ-DISENO-1`/`ADR-152` documenta para worktrees nuevos); `ls
   data/raw | wc -l` → 318, no vacío.
4. **Entorno**, tres partes (A.2):
   - **sin_variable**: no aplica ningún sondeo de red específico a este acto
     — el PARO se determina por inspección del árbol (columnas del TSV,
     código de `tools/curador_registro/`), no por disponibilidad de red.
   - **sonda INEGI**: no ejecutada — no llegó a ser necesaria antes del PARO
     (el bloqueo es de instrumento, previo a cualquier barrido de red).
   - **ls data/raw/**: no vacío (318 entradas), confirmado arriba.
5. **Espejo.** Ninguna cifra de esta nota viene del espejo; todo se deriva
   del clon.

## Verificación de existencia

`tools/curador_registro/` **existe** y coincide con lo que `ADR-135(d)`
cita, confirmado contra `PR #164` (`codex/barrido-completo-n1-n33`) y `PR
#244` (`codex/barrido-2`) — 28 archivos, incluida
`GUIA-CURADOR-REGISTRO.md`. Esto ya lo había establecido `ACTO SELLA-AGO24-D`
como enmienda a `ADR-148`; este acto lo re-confirma en el árbol, no lo repite
a ciegas: `ls tools/curador_registro/` → 28 entradas.

## Método (GUIA leída completa antes de tocar nada)

`tools/curador_registro/GUIA-CURADOR-REGISTRO.md` (31 líneas):

- `baseline.py RUTA_AL_BASELINE` — valida un **baseline semántico
  demanda-universo**: exige `baseline.json` + TSV cuyas filas se identifican
  por la terna `(necesidad_id, fuente_canonica_normalizada,
  objeto_evidencia_id_canonico)`.
- `derive_queue.py RUTA_AL_BASELINE --output /tmp/cola.tsv` — deriva de ese
  baseline una cola reproducible; la GUIA es explícita: *"la cola no debe
  versionarse"* (por eso las corridas de este acto, si hubieran llegado a
  correr, habrían escrito solo en `/tmp`, nunca en el repo).
- `via_capa2.py --root .` — cruza `relaciones.tsv` (salida del baseline)
  contra `data/manifiesto.yaml` real, promoviendo `capa2_manifiesto` **solo**
  cuando `id_manifiesto` resuelve a una entrada con payload verificado,
  "nunca por coincidencia de nombre de fuente".

Declaración de uso previsto: `baseline.py` para validar el baseline de
partida → `derive_queue.py` para generar la cola de candidatas → 
`via_capa2.py --root .` (solo lectura primero) para verificar cada candidata
contra el manifiesto real antes de promoverla. Cero pasos inventados fuera de
la GUIA.

## Criterio de saturación (escrito antes de barrer)

Derivado de `ADV1-M1` (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B —
mismo texto que ya citó `ADR-148`, re-leído aquí, no heredado de memoria):
saturación = el barrido del universo elegible bajo los filtros **(i)**
no-publicada (prueba del bibliotecario) **(ii)** grado de dependencia
P0/P1/P2 con cuota ≥1/3 en P2 **(iii)** árbitro decidible (CV bajo el umbral
CAC-007/01/2018 + piso de `n` no ponderado) **(iv)** frase de discriminación
pre-registrada **(v)** ≥3-5 celdas post-corte deja de producir candidatas
nuevas.

## Por qué el barrido nunca arrancó

`head -1 forense/marco-candidatas-piloto-v1_0.tsv | tr '\t' '\n'` → 17
columnas: `id`, `encuesta`, `ola`, `universo`, `variable`, `estimador`,
`ponderador`, `escala`, `grado_dependencia`, `publicada`, `cv_arbitro`,
`n_no_ponderado`, `frase_discriminacion`, `post_corte_u_ola_retenida`,
`dominio`, `dificultad`, `estrato`.

`command grep -n "def \|necesidad_id\|fuente_canonica\|objeto_evidencia"
tools/curador_registro/baseline.py` confirma la identidad de fila que ese
módulo exige: `(necesidad_id, fuente_canonica_normalizada,
objeto_evidencia_id_canonico)`.

**Cero solape entre las 17 columnas del marco y la terna del curador.** El
curador identifica *relaciones de adquisición de fuente* (qué necesidad de
dato satisface qué fuente, con qué objeto de evidencia) — es el mismo dominio
que `REG-LOTE3`/`LIMPIA-CAJA` usaron (`data/curacion-registro/`, registro de
demanda-universo). El marco de candidatas del piloto identifica *specs de
pregunta/variable/ola bajo un duelo de diseño muestral L-vs-M* — dominio
disjunto, protegido por el mismo criterio de "no cruzar poblaciones de
conteo" que ya cicatrizó `FP-68`/`ADR-67(c)`.

`find . -iname "*baseline*.json" -o -iname "relaciones.tsv"` sobre el árbol
completo (excluyendo `.git`): **cero coincidencias.** No hay ningún baseline
semántico vivo hoy contra el cual correr `baseline.py`, `derive_queue.py`, ni
`via_capa2.py` con efecto real — `via_capa2.py --root .` (solo lectura) se
ejecutó como prueba de humo y corre sin error, pero no emite nada porque
`relaciones.tsv` no existe en este árbol.

```
head -1 forense/marco-candidatas-piloto-v1_0.tsv | tr '\t' '\n' | wc -l   # 17
command grep -n "necesidad_id\|fuente_canonica\|objeto_evidencia" tools/curador_registro/baseline.py
find . -iname "*baseline*.json" -o -iname "relaciones.tsv" 2>/dev/null    # (vacío, fuera de tests/baseline.json ajeno)
```

(`tests/baseline.json` sí existe, pero es el congelado de `tests/check.py
--freeze` — el baseline de regresión de la suite, no un "baseline semántico
demanda-universo"; nombre compartido, cosa distinta, verificado leyendo su
contenido: claves de conteo de FAIL/WARN, no `necesidad_id`.)

## Filtros (i) y (iii): no alcanzados, no por falta de entorno

A diferencia de `ADR-148` (entorno NUBE, sin red ni microdato — bloqueo de
*capacidad*), este acto corre en **UBUNTU con corpus montado**: el filtro
**(i)** (bibliotecario de dos pasos de `FP-93` sobre las 56 filas
`PENDIENTE-BIBLIOTECARIO`, contra `data/indice-descarga-masiva-2026-08-05.tsv`
+ `data/indice-canastas-2026-08-08.tsv`) y el filtro **(iii)** (árbitro sobre
microdato usando `data/diseno-muestral.yaml`, extendido `43→56` filas por
`ADR-153`/`RECENSO-DISEÑO-2`, `wc -l data/diseno-muestral.yaml` confirma la
extensión en el árbol) son ejecutables aquí en principio. Pero **(i)** y
**(iii)** son filtros que *reducen* un universo de candidatas ya generado —
deciden si una candidata ya identificada pasa o no pasa. Sin el generador de
candidatas nuevas (el paso que la firma asignó al curador CODEX), no hay
universo que filtrar. Ejecutar el bibliotecario de `FP-93` aislado, sobre las
56 filas ya existentes en `v1_0.tsv` sin ninguna candidata nueva que agregar,
sería un acto distinto (cierre de `FP-93` sola) no autorizado por este
encargo, que lo ata explícitamente al barrido de saturación. `FP-93` queda
`ABIERTA`, sin tocar.

## Conclusión

No hay barrido que correr con el curador localizado: `tools/curador_registro/`
es real, está probado (`PR #164`/`#244`), y su GUIA es clara — pero resuelve
identidad de *relaciones de adquisición de fuente*, no genera *specs de
pregunta/variable del marco del piloto*. El `NO-ENCONTRADO` de `ADR-148` era
de nombre; el de este acto es de **dominio**: la herramienta correcta de
nombre, aplicada al problema equivocado, no avanza el marco un renglón.
`marco-candidatas-piloto-v1_1.tsv` **no se crea** — no hay ninguna candidata
nueva que congelar, y crear un sucesor vacío sería peor que no crearlo (el
propio `v1_0.tsv` ya documenta "60 de 60" sin ambigüedad).

**Lo que mesa necesita para desbloquear**, dos vías, no excluyentes:

1. **Construir el generador.** Extender `tools/curador_registro/` (o un
   módulo hermano) a la terna `fuente·instrumento·ola·variable·filtro` del
   marco — trabajo de desarrollo, fuera del alcance de "ejecutar un barrido"
   que este encargo autorizó.
2. **Redirigir el uso previsto.** Si "saturación vía CODEX" en realidad
   significaba usar `via_capa2.py` para verificar `capa2_manifiesto` de las
   fuentes *ya presentes* en `v1_0.tsv` (un paso de validación, no de
   generación), ese es un acto distinto y más pequeño, ejecutable hoy mismo
   con lo que existe — pero no es lo que la firma de `ADR-135(d)` describe
   ("se amplía a saturación").

`ACT-PIL-3` (sorteo) sigue esperando: `867948c` sigue anulada, sin SHA de
merge nuevo que la sustituya — este PR no congela ningún marco nuevo, congela
el hallazgo de por qué el curador localizado no sirve para este barrido.

**Perímetro respetado.** Tocados en este acto: esta nota (nueva),
`canon/gobernanza-v1_15.md` (`ADR-154`), `canon/estado-programa-v1_10.md`
(línea de candidatas — nota de PARO, cifra `60` intacta — y recifrado de
conteo de ADR), `forense/firmas-pendientes.tsv` (`FP-121` recibe
`ejecutada_en`), `forense/encargos/2026-08-24-MARCO-SATURA-CODEX.md`
(archivado verbatim, `CONSUMIDO`). No se tocó
`forense/marco-candidatas-piloto-v1_0.tsv` (nada que congelar), no se creó
`v1_1.tsv`, no se tocó `Hito D`, duelo, condicionales ni coeficientes.
