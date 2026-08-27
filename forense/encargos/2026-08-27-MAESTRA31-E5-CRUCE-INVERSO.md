ENCARGO E5 · CRUCE-INVERSO — el motor declara 79 variables; el corpus tiene 36,809 y nadie las ha cruzado
Dirección (maestra-31), 27/ago/2026 · Redactado contra `main = 07b1452` (clon propio, no espejo). No gated. `#381`, `#382`, `#384`, `#385` fusionados. El inventario está en `main`.
ENTORNO ASIGNADO: NUBE (`cloud_default`). NO lanzar en UBUNTU — ahí corre `MAESTRA31-E6`. Este acto no necesita `data/raw`: sus dos insumos, `data/inventario-reactivos-v1_0.tsv` y `milpa/procedencia.yaml`, están versionados. Sin red, sin API (`FP-165`). Rótulo: `ACTO MAESTRA31-E5` (D-6). Token pelado `E5` colisiona; se censa, no se reclama.
════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════
Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.
1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · `git log -1 --format="%h %s"` · `git status` ⚠️ No arranques desde el home.
2 · SHA. Confirma contra qué base trabajas y compáralo con el declarado. Si `main` se movió: NO es PARO — refresca, re-deriva y reporta la diferencia antes de editar.
3 · `data/raw`. AUSENTE NO ES PARO y este acto no la usa. Repórtalo y sigue. ⚠️ Si te encuentras abriendo un payload, el perímetro estaba mal: el inventario ya lo hizo.
4 · ENTORNO. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → esperado `cloud_default`. Este acto no toca microdato ni red: dilo y salta la sonda, con la razón escrita. ⚠️ Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo declara cuántos archivos —o cuántas filas— examinó el comando que lo produjo.
5 · ESPEJO. Prohibido derivar cifras del espejo. Toda cifra sale del clon de (1), con el comando a la vista.
════════════════════════════════════════════════════════════════════
═══ VERIFICACIÓN DE EXISTENCIA — CONTESTADA por dirección (clon propio, `07b1452`, 27/ago/2026) ═══
1 · ESTRUCTURA. Insumos, ambos versionados y ninguno se edita: `data/inventario-reactivos-v1_0.tsv` (178,246 filas · 36,809 variables distintas · 74 instrumentos · `ADR-213`) · `milpa/procedencia.yaml` + `milpa/tramite.yaml` (30 parámetros) · `construir_crosswalk` en `milpa/src/emisor.py`, reparado por E8 (`ADR-208`). Gobernante del veredicto: A.4. Este acto produce artefacto nuevo, no escribe en tabla gobernada.
2 · CONTENIDO — el cruce NO existe. Comando y salida cruda:

```
grep -rIl --exclude-dir=.git "inventario-reactivos" .
  → forense/firmas-pendientes.tsv · forense/hallazgos.md
  → forense/notas/2026-08-26-orden-superior-cierre.md
  → forense/encargos/2026-08-26-MAESTRA31-E4-ORDEN-SUPERIOR.md
  → data/inventario-reactivos-v1_0.tsv.meta · tools/inventario_reactivos.py
  → canon/estado-programa-v1_10.md · gobernanza-v1_15.md · registro-rotulos.tsv
(A.13: 2,185 archivos de texto examinados)
```

Los nueve son o registros que citan todo, o los propios subproductos de E4. Ninguno cruza el inventario contra el motor. Resultado A.4: NO-ENCONTRADO — universo: árbol completo salvo `.git` y `data/raw`, 27/ago/2026.
Y las dos magnitudes que hacen falta:

```
tokens tipo-variable en procedencia.yaml + tramite.yaml   →     79
variables distintas en el inventario                       → 36,809
crosswalk existente: alcance                               →     60 celdas del marco → 1 EMITE
```

El crosswalk vigente compara 60 celdas. El motor declara 79 variables. El corpus tiene 36,809. Nadie ha verificado nunca si las 79 existen donde el motor cree que existen.
3 · COBERTURA RETROACTIVA. El inventario nació el 26/ago (`ADR-213`); `procedencia.yaml`, el crosswalk y `enlace-M` son todos anteriores. Ninguno pudo consultarlo. Su silencio sobre él no prueba nada: es la brecha que A.8(3) manda declarar, y este acto la cierra.
⚠️ Si al ejecutar encuentras que este cruce ya está hecho, PARA y repórtalo. Este programa ya perdió jornadas por no verificarlo.
════════════════════════════════════════════════════════════════════
OBJETO
Correr el emparejamiento en dirección oferta → demanda por primera vez, y contestar tres preguntas que el programa nunca ha hecho. Las tres por token exacto de variable, ninguna semántica.
Q1 · ¿Existe lo que el motor cita? De las 79 variables que el motor declara, cuántas aparecen en el inventario, en qué payload, en qué instrumento y en qué ola. Hoy el motor cita variables y nadie ha verificado que estén donde supone. Vocabulario A.4 por variable: `EXISTE-SATISFACE` (aparece con la encuesta que el motor declara) · `EXISTE-NO-SATISFACE` (aparece, pero en otro instrumento u otra ola) · `NO-ENCONTRADO` (con el universo y el término al lado).
Q2 · ¿En cuántas olas vive cada una? Para las que existen, el conteo de olas distintas. Una variable presente en ocho olas es una oportunidad de panel o de réplica que el motor no sabe que tiene. Este es el rendimiento esperado del acto y su resultado no es predecible desde el escritorio.
Q3 · ¿A cuántos parámetros NO puede llegar este método, y por qué? De los 30 parámetros, cuántos citan al menos una variable y cuántos no citan ninguna. Dirección espera que los 13 `ASIGNADO_PROBABILIDAD` —juicio puro sin ruta, según `forense/perimetro-alcanzable-v1_0.md`— no citen ninguna, y por tanto sean inalcanzables por token exacto por construcción, no por escasez de datos. Confírmalo o refútalo con comando. Si se confirma, ése es el hallazgo más importante del acto, porque dice que el techo del emparejamiento por token no es un problema de cobertura y no se arregla con más corpus.
Lo que este acto NO hace: no empareja por texto ni por semántica · no propone qué medir · no toca el motor · no adjudica ningún parámetro a ninguna fuente · no promueve nada a acto medidor.
PASOS
0-bis · A.3. Commitea este encargo íntegro y verbatim en `forense/encargos/2026-08-27-MAESTRA31-E5-CRUCE-INVERSO.md` antes de nada. `## CONSUMIDO` al cerrar, con el número de PR.
1 · COMMIT-1 — congela la especificación ANTES de cruzar. Contiene y nada más:

* Cómo se extraen las 79 del motor. Dirección las obtuvo con una regex de forma (`[A-Z]{1,4}[0-9]+(_[0-9A-Z]+)*`) sobre los dos yaml. Esa receta es de dirección, no está probada, y probablemente tiene falsos positivos (constantes, códigos de ola, identificadores que no son variables). Deriva la tuya, pruébala contra un caso donde conozcas la respuesta —los tres `CANDIDATO-EMITE` del crosswalk v1.1, `CIV-01/ENCIG/P8_3_1`, sirven de control positivo— y si tu conteo difiere de 79, manda el tuyo y dilo. Una regex de forma no distingue una variable de un código: declara cómo lo resuelves.
* La regla de emparejamiento: token exacto, y si exiges coincidencia de instrumento, cómo normalizas los nombres entre `procedencia.yaml` y la columna `instrumento` del inventario — que no tienen por qué usar la misma grafía. Ese mapeo de nombres es la trampa de este acto; decláralo antes, no lo improvises al chocar.
* El esquema de salida y la escala A.4 con las tres respuestas de Q1.
* B-bis, antes de ver el dato: qué significaría un resultado alto en Q2 y qué significaría cero. Si Q1 sale casi completo —las 79 existen donde deben— eso corrobora la construcción del motor y es un resultado interesante, no un no-hallazgo; dilo por escrito ahora para que nadie lo lea después como fracaso.
* Frase de sello verbatim: «El primer resultado que produzca este procedimiento es el que se reporta.»

2 · COMMIT-2 — el resultado. `data/cruce-inverso-v1_0.tsv` (una fila por variable del motor, con su veredicto A.4, payloads, instrumentos y olas) más la respuesta a Q3. Sin editar el primero; enmienda por adición si hace falta. Universo declarado en la cabecera (A.10): SHA, fecha, denominadores de los dos lados.
3 · Cierre. Nota `forense/notas/2026-08-27-cruce-inverso-cierre.md` con los conteos A.13 · `FP-172` con las tres respuestas ante mesa · línea en `forense/hallazgos.md` si Q3 confirma el techo estructural · ADR (máximo re-derivado por conteo entero; candidatea máximo+1; renumera quien fusione segundo) · recifrado `§L0` · rótulo en `canon/registro-rotulos.tsv` y `tests/check.py` si `T25` lo exige · `python3 tests/check.py --baseline` VERDE (🚫 jamás `--freeze`) · PR.
REGLA DE TOPE
1 · Cero semántica. Token exacto solamente. Nada de embeddings, difusos, ni API. `texto_reactivo` está vacío en el 100% de las 178,246 filas (`ADR-213`, enmienda F1) — no intentes rodearlo. Que el texto falte es hallazgo de `E4` y lo atiende `E6`, no éste.
2 · Cero herramientas nuevas de extracción. El inventario está hecho. Este acto lee dos TSV/YAML y escribe uno. Si te encuentras abriendo un payload, PARA.
3 · Cero iteración sobre el emparejador. Si `construir_crosswalk` no sirve tal cual para la dirección inversa, no lo edites: escribe el cruce como consulta propia sobre las dos tablas y declara por qué no lo usaste. `milpa/` está fuera de perímetro.
4 · Una vuelta. Si Q1 devuelve que casi ninguna de las 79 existe, ése es el resultado y se reporta. No se relaja el criterio de emparejamiento para subir el número. Ajustar el criterio después de ver el dato es el defecto que la frase de sello existe para impedir.
PERÍMETRO Y CONCURRENCIA
Toca: `forense/encargos/2026-08-27-MAESTRA31-E5-CRUCE-INVERSO.md` · `data/cruce-inverso-v1_0.tsv` (nuevo) · `forense/notas/2026-08-27-cruce-inverso-cierre.md` (nuevo) · `forense/firmas-pendientes.tsv` (solo `FP-172`) · `forense/hallazgos.md` · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` · `canon/registro-rotulos.tsv` · `tests/check.py` (solo `_T25_ARCHIVOS_CONOCIDOS`).
NO toca: `milpa/**` · `data/inventario-reactivos-v1_0.tsv` ni su `.meta` · `tools/**` · `forense/crosswalk-pregunta-regla-v1_1.tsv` · `forense/perimetro-alcanzable-v1_0.md` · `data/coef-universo-v1_0.tsv` · el cruce oferta↔demanda · `forense/prereg-duelo-v2/**` · `R10.3`.
Concurrencia: `MAESTRA31-E6 · DICCIONARIOS-FD` corre en UBUNTU en paralelo. Colisión posible en `gobernanza` / `estado` / `registro-rotulos` / `tests/check.py`. Tablero separado: este acto `FP-172`, `E6` `FP-173`. ADR: renumera quien fusiona segundo, con el máximo re-derivado contra el árbol ya fusionado.
"Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."
PROHIBIDO
Emparejar por texto o semántica · editar `milpa/` o `tools/` · abrir payloads · relajar el criterio tras ver el dato · proponer qué medir o adjudicar un parámetro a una fuente · promover nada a acto medidor · red o API · derivar cifra del espejo · escribir «no existe» sin comando y universo al lado.
CONTADOR
Las 79 variables del motor verificadas contra el corpus, con veredicto A.4 y conteo de olas — la primera verificación que el motor recibe de sus propias citas. Más la respuesta a Q3: cuántos de los 30 parámetros son inalcanzables por token exacto por construcción.
Si Q1 sale casi completo, el contador es esa corroboración y se reporta como tal. Un motor cuyas citas resultan correctas es un dato, no un no-resultado.

## CONSUMIDO
Ejecutado por `ACTO MAESTRA31-E5 · CRUCE-INVERSO`, 27/ago/2026. PR: https://github.com/Josanoforo/Modelado-Mexicano/pull/386
