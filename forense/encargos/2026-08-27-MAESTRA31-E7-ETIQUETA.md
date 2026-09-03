ENCARGO E7 · ETIQUETA — el 58% del inventario dice `(raiz)`, y ya contaminó dos cifras ante mesa
Dirección (maestra-31), 27/ago/2026 · Redactado contra `main = f1b0d79` (clon propio, no espejo). No gated. Corre en paralelo con `E6`, que está en otra caja.
ENTORNO ASIGNADO: NUBE (`cloud_default`). NO lanzar en UBUNTU — ahí termina `E6`. Este acto no necesita `data/raw` y tiene prohibido abrir un payload: opera sobre TSV ya versionados. Sin red, sin API (`FP-165`). Rótulo: `ACTO MAESTRA31-E7` (D-6). Token pelado `E7` colisiona; se censa, no se reclama.
════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════
Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.
1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · `git log -1 --format="%h %s"` · `git status` ⚠️ No arranques desde el home.
2 · SHA. Confirma contra qué base trabajas. Si `main` se movió: NO es PARO — refresca, re-deriva y reporta la diferencia antes de editar. Es probable que `main` se haya movido: `E6` fusiona en paralelo.
3 · `data/raw`. AUSENTE NO ES PARO y este acto no la usa. Repórtalo y sigue. ⚠️ Si te encuentras abriendo un payload, PARA: el perímetro estaba mal.
4 · ENTORNO. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → esperado `cloud_default`. Este acto no toca microdato ni red: dilo y salta la sonda, con la razón escrita. ⚠️ Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo declara cuántas filas examinó el comando que lo produjo.
5 · ESPEJO. Prohibido derivar cifras del espejo. Toda cifra sale del clon de (1), con el comando a la vista.
════════════════════════════════════════════════════════════════════
═══ VERIFICACIÓN DE EXISTENCIA — CONTESTADA por dirección (clon propio, `f1b0d79`, 27/ago/2026) ═══
1 · ESTRUCTURA. Tabla gobernante: `data/inventario-reactivos-v1_0.tsv` (`ADR-213`) y su consumidor `data/cruce-inverso-v1_0.tsv` (`ADR-214`). Este acto produce sucesores versionados; no edita ninguno de los dos.
2 · CONTENIDO — el defecto está derivado, no supuesto. Mecanismo, con la línea:

```
tools/inventario_reactivos.py:125
    instrumento = rel.split("/", 1)[0] if "/" in rel else "(raiz)"
```

La etiqueta de instrumento es el primer componente de la ruta relativa. Todo payload que viva en la raíz de `data/raw` recibe `(raiz)`. Magnitud:

```
awk -F'\t' 'NR>1 && $3=="(raiz)"' data/inventario-reactivos-v1_0.tsv | wc -l   → 103,302  (58% de 178,246)
… | awk '{print $1}' | sort -u | wc -l                                          →     119  payloads distintos
awk -F'\t' 'NR>1 && tolower($1) ~ /encuci/' data/inventario-reactivos-v1_0.tsv | wc -l                           →     458  filas, instrumento=(raiz)
```

Contaminación ya materializada en artefactos ante mesa, derivada por dirección:

* `FP-172` / `ADR-214` (E5): 16 de los 20 veredictos `EXISTE-NO-SATISFACE` citan un payload de `(raiz)`. El veredicto significa "existe, pero bajo otro instrumento" — y en esos 16 el "otro instrumento" es el cubo, no un instrumento.
* La misma nota concluye que ENCUCI 2020 no está entre los 74 instrumentos y lo registra como "hallazgo de cobertura del corpus". Es falso: ENCUCI tiene 458 filas. Es hallazgo de etiqueta.
* `n_olas_distintas` se calcula sobre `instrumento`. Con 119 payloads colapsados en uno, el conteo está mal en las dos direcciones: infla el de variables que solo viven en `(raiz)`, y desinfla el de las que viven en `(raiz)` más carpetas nombradas. Los máximos publicados (`P4_10`=17, `BP1_20`/`AP7_1`/`AP3_10`=16) están todos en esa condición.
* `FP-171` / `ADR-213` (E4): la cifra "74 instrumentos" cuenta `(raiz)` como uno.

Resultado A.4 sobre el entregable: NO-ENCONTRADO — ningún archivo del árbol repara la etiqueta ni re-deriva lo que depende de ella. Universo: árbol completo salvo `.git` y `data/raw`, 2,189 archivos de texto examinados, 27/ago/2026.
3 · COBERTURA RETROACTIVA. El inventario nació el 26/ago y el cruce el 27/ago; ambos son posteriores a toda tabla gobernante y ninguno pudo consultar una corrección que no existía. Sin brecha.
⚠️ Si al ejecutar encuentras que esto ya está reparado, o que mi diagnóstico no se sostiene contra el archivo, PARA y repórtalo. Dirección ya se equivocó una vez sobre este mismo caso —afirmó "ENCUCI no está en el inventario, hueco de cobertura" cuando está y es hueco de etiqueta—, así que trata este bloque como premisa a verificar, no como hecho.
════════════════════════════════════════════════════════════════════
OBJETO
Reparar la etiqueta de instrumento sin volver a extraer nada, y re-derivar lo que dependía de ella, para que las cifras que están ante mesa digan lo que el corpus dice.
Tres entregables, en orden:

1. `data/inventario-reactivos-v1_1.tsv` — misma tabla, columna `instrumento` derivada por una regla que sí funciona para payloads de raíz. `v1_0` queda SUPERADO en cabecera, no editado.
2. `data/cruce-inverso-v1_1.tsv` — el cruce de E5 re-corrido sobre `v1_1`, con la misma especificación congelada de E5, sin cambiarla. El delta contra `v1_0` es el entregable: cuántos veredictos se mueven y en qué dirección.
3. Enmiendas fechadas a `FP-171` y `FP-172` con las cifras corregidas, y a la nota de E5 sobre la conclusión falsa de ENCUCI — por adición, con el texto original intacto, precedente `## F1` de `ADR-208` y la enmienda de `ADR-213`.

Lo que este acto NO hace: no re-extrae, no abre payloads, no cambia la especificación de E5, no toca `tools/`, no adjudica qué significa el resultado.
PASOS
0-bis · A.3. Commitea este encargo íntegro y verbatim en `forense/encargos/2026-08-27-MAESTRA31-E7-ETIQUETA.md` antes de nada. `## CONSUMIDO` al cerrar, con el número de PR.
1 · COMMIT-1 — congela la regla de etiqueta ANTES de aplicarla.

* Cómo se deriva `instrumento` para un payload de raíz. Dirección no prescribe la regla, y hay al menos tres familias visibles en los 119 (`BD_ENCUCI2020_dbf.zip`, `2016trim1_csv.zip`, `conjunto_de_datos_enoe_*`) que probablemente no se resuelven con un solo patrón. Obsérvalas antes de escribir la regla. Si un payload no cae limpio, va a `(sin-instrumento-derivable)` con la razón — no lo fuerces. Un cubo honesto de 12 vale más que 119 mal asignados.
* Y la trampa que esto tiene: `ola` se deriva hoy del mismo lugar. Declara si tu regla la toca y qué pasa con las que ya estaban bien; una corrección que arregla `instrumento` y rompe `ola` no es una corrección.
* El control positivo, obligatorio: los payloads que hoy tienen instrumento correcto (`encig2023`, `envipe2025`, …) deben conservarlo byte a byte. Verifícalo con comando y pega la salida. Si tu regla los cambia, la regla está mal.
* B-bis antes de ver el dato: qué significa que muchos veredictos se muevan y qué significa que casi ninguno lo haga. Si el delta es pequeño, la contaminación era menor de lo que dirección estimó — dilo y no lo maquilles; ese resultado corrobora a E5 y es tan publicable como el contrario.
* Frase de sello verbatim: «El primer resultado que produzca este procedimiento es el que se reporta.»

2 · COMMIT-2 — las dos tablas y el delta. `v1_1` de ambas, con universo declarado en cabecera (A.10). El delta reportado por clase de veredicto: cuántos `EXISTE-NO-SATISFACE` pasan a `EXISTE-SATISFACE`, cuántos `NO-ENCONTRADO` se mueven, y cómo cambian los conteos de olas de las cuatro variables cuyos máximos se publicaron. Y el conteo nuevo de instrumentos distintos, que sustituye al 74.
3 · Las enmiendas. Fechadas, por adición, en `FP-171`, `FP-172` y la nota de cierre de E5. La conclusión falsa de ENCUCI se retracta con esas palabras —"hallazgo de etiqueta, no de cobertura"— con el comando al lado. No se suaviza y no se borra el original: es el registro de qué se sabía y con qué alcance (A.10, corolario 1).
4 · Cierre. Nota `forense/notas/2026-08-27-etiqueta-cierre.md` con los conteos A.13 · `FP-174` con el delta ante mesa · línea en `forense/hallazgos.md` sobre el patrón, no sobre el archivo: una etiqueta derivada de la ruta hereda la forma del directorio, no la del dato, y falla en silencio aguas abajo · ADR (máximo re-derivado por conteo entero contra el árbol ya fusionado; renumera quien fusione segundo — `E6` fusiona en paralelo) · recifrado `§L0` · rótulo en `canon/registro-rotulos.tsv` y `tests/check.py` si `T25` lo exige · `python3 tests/check.py --baseline` VERDE (🚫 jamás `--freeze`) · PR.
REGLA DE TOPE
1 · Cero re-extracción. `payload_id` ya está en la tabla; la etiqueta se re-deriva de ahí. Si te encuentras abriendo `data/raw`, PARA.
2 · `tools/inventario_reactivos.py` no se edita. Se lee y se cita. Que el extractor conserve la regla vieja es hallazgo del sucesor, no de este acto — y así el `v1_0` sigue siendo reproducible desde su propio código, que es lo que lo hace auditable.
3 · La especificación de E5 no se cambia. El cruce se re-corre igual, solo cambia el insumo. Si al re-correr descubres que la spec de E5 tenía otro defecto, anótalo y no lo arregles: mezclar dos correcciones en una corrida hace imposible atribuir el delta.
4 · Una vuelta. Si tu regla deja más de la mitad de los 119 en `(sin-instrumento-derivable)`, se reporta así y se para: significa que la etiqueta no es derivable del nombre y hace falta otra fuente. No se itera la regla para subir el número.
PERÍMETRO Y CONCURRENCIA
Toca: `forense/encargos/2026-08-27-MAESTRA31-E7-ETIQUETA.md` · `data/inventario-reactivos-v1_1.tsv` (nuevo) + cabecera SUPERADO de `v1_0` · `data/cruce-inverso-v1_1.tsv` (nuevo) + cabecera SUPERADO de `v1_0` · `forense/notas/2026-08-27-cruce-inverso-cierre.md` (solo enmienda fechada al final) · `forense/notas/2026-08-27-etiqueta-cierre.md` (nuevo) · `forense/firmas-pendientes.tsv` (`FP-174` nueva · enmienda a `FP-171` y `FP-172`, nada más) · `forense/hallazgos.md` · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` · `canon/registro-rotulos.tsv` · `tests/check.py` (solo `_T25_ARCHIVOS_CONOCIDOS`).
NO toca: `tools/**` · `milpa/**` · `data/raw` · el `.meta` del inventario · `data/inventario-fd-v1_0.tsv` (es de `E6`, en vuelo) · `forense/perimetro-alcanzable-v1_0.md` · `forense/prereg-duelo-v2/**` · `R10.3`.
Concurrencia: `MAESTRA31-E6 · DICCIONARIOS-FD` cierra en UBUNTU; toma `FP-173` y candidatea `ADR-215`. Este acto toma `FP-174`. Colisión en `gobernanza` / `estado` / `registro-rotulos` / `check.py`: renumera quien fusiona segundo, con el máximo re-derivado contra el árbol ya fusionado, no por aritmética. `E6` escribe `data/inventario-fd-v1_0.tsv`; este acto no lo lee ni lo integra — la unión es de un sucesor.
"Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."
PROHIBIDO
Abrir cualquier payload · editar `tools/` o el extractor · cambiar la especificación del cruce de E5 · editar `v1_0` de cualquiera de las dos tablas (solo cabecera SUPERADO) · borrar o suavizar la conclusión falsa de ENCUCI en vez de retractarla por adición · iterar la regla tras ver el conteo · integrar la tabla de `E6` · adjudicar qué significa el delta · red o API · derivar cifra del espejo.
CONTADOR
El delta de veredictos entre `v1_0` y `v1_1`, y el conteo real de instrumentos distintos que sustituye al 74. Es la primera vez que el programa mide cuánto de una conclusión suya venía de una etiqueta y no del dato.
Si el delta resulta pequeño, ése es el contador y corrobora a E5: se reporta con esa palabra y no como decepción.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fn -- "2026-08-27-MAESTRA31-E7-ETIQUETA.md" canon/gobernanza-v1_15.md` cita ADR-216, pero el bloque mezcla lenguaje de ejecución y de encargo pendiente (o el rótulo del ADR es compartido entre varios encargos sin desenlace individual claro) — rastro parcial, no se decide aquí. Para mesa: verificar manualmente contra ADR-216 en canon/gobernanza-v1_15.md.
