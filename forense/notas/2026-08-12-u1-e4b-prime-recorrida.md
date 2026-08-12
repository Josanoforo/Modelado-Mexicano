# U1 · E4b′ — enmienda pre-dato de `periodo_levantamiento` (ESP-OPACA-B-d13ec4fe / `CRES-7cb78abf`)

**Acto:** ENCARGOS FINALES · CIERRE DE BRECHA — U1 · **Entorno:** CAJA LOCAL Ubuntu CC · **Base real de este commit:** `e078e46` (origin/main, PR #183 fusionado) · **Depende de:** E4b SELLO-B/CORRIDA-B (`8df61b0`…, PR #173, MERGED) — verificado ancestro de `origin/main` antes de abrir este acto.

Este commit (1b) enmienda un solo campo material de una especificación ya sellada. No corre el motor. Ningún resultado vive en este commit. Legítimo porque `CORRIDA-B` (PR #173) produjo exactamente `campos_materiales_faltantes:periodo_levantamiento` — cero cómputo, ningún resultado fue jamás visto — y porque `ADR-69(b)` (`canon/gobernanza-v1_15.md`, sellado 12/ago) ya declaró por escrito qué desbloquea esto: *"E4b puede completar `periodo_levantamiento` de `CRES-7cb78abf` en un tercer commit sobre su propia especificación — no lo hace este acto, no es su perímetro."* Este commit es ese tercer commit.

## §0 · Premisas verificadas (ARRANQUE + PREMISAS U1)

- Worktree dedicado `~/mm-u1-e4b-prime`, rama `u1/e4b-prime-recorrida`, creada sobre `origin/main` fresco (`e078e46`, PR #183). `git worktree add` emitió el error conocido de contención de `.git/config` en esta máquina (ver memoria del proyecto) — la rama quedó creada pero el worktree no; verificado con `git worktree list` (ausente) y reintentado sin `-b` reutilizando la rama huérfana, que ya apuntaba a `e078e46` — sin pérdida.
- `git merge-base --is-ancestor 8df61b0 origin/main` → PASA. `curl` a `https://www.inegi.org.mx/rnm/index.php/catalog/922` → PASA (200). `data/curacion-registro/expedientes-produccion/` → PASA (existe).
- `data/raw` ausente en el worktree fresco, enlazada a `/home/pc0/mm-corpus/raw` (mismo mecanismo que todo worktree hermano, defecto PR #77).
- `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable` · `curl` a `inegi.org.mx` = `200`.
- Ningún otro acto U1/U2/U3 tiene rama, PR ni worktree previo en esta caja ni en `origin` — verificado (`git branch -r | grep -iE "u1|u2|u3|e4b|ev1|doc-backfill"`, vacío; `gh pr list --search brecha`, sin resultado para estos actos). Este es el primer acto del programa post-revisión del 12/ago.

## §1 · La enmienda: `periodo_levantamiento` desde la ficha RNM 922, releída de primera mano

**Fuente:** `https://www.inegi.org.mx/rnm/index.php/catalog/922` · **fecha_consulta:** `2026-08-12` · re-abierta por esta sesión, no heredada de `ADR-69` ni de la fila ya existente en `data/universo-puertas-2026-08-12.tsv` — ambas se citan como corroboración independiente en §2, ninguna como fuente.

**Método de extracción, declarado porque cambió a mitad de acto (ver §4):** `curl` trae la ficha completa server-rendered (241 042 bytes; a diferencia del buscador `/programas/`, que notas previas del corpus —`2026-07-31-perimetro-descarga.md`, `2026-08-07-explora1.md`, `2026-08-08-explora2.md`— ya documentaron como SPA no reproducible por `curl`, esta ficha individual sí lo es, confirmado también por el PASA de premisas). Las tablas de fechas se parsearon por `<tr>`/`<td>` explícitos con un script Python de una sola pasada (regex sobre HTML crudo, sin dependencias nuevas) — no por conversión a texto plano, que difumina el límite entre filas de una tabla.

La tabla **"Periodo de ejecución del proyecto estadístico"** trae 16 filas (`Inicio`, `Fin`, `Período`/etiqueta), una por fase del proyecto. La fila con la etiqueta exacta **"Levantamiento"**:

```
Inicio: 2022-10-24    Fin: 2022-12-16    Período: Levantamiento
```

**Reserva, declarada por escrito antes de adoptar (instrucción explícita del encargo):** la prosa de la sección **SUPERVISIÓN**, subsección "1. Levantamiento de la información", dice verbatim: *"La etapa de recolección de información se llevó a cabo del 24 de octubre al 10 de diciembre de 2022…"* — cierre **10 de diciembre**, seis días antes del cierre de tabla (16 de diciembre). Discrepancia interna de la ficha, no resuelta por la fuente misma. Se adopta la tabla estructurada (campo con nombre exacto "Levantamiento", extraído sin ambigüedad de un único `<tr>`) sobre la prosa narrativa del operativo; no se encontró razón contraria escrita para preferir la prosa. La prosa queda citada aquí, verbatim, como reserva — no se concilian los seis días.

**Valor escrito en `especificaciones-produccion.json#ESP-OPACA-B-d13ec4fe`:**
```
"periodo_levantamiento": "2022-10-24/2022-12-16"
```
Formato de rango ISO, consistente con el único precedente del corpus para este campo (`ESP-OPACA-A-7baf278d`, ENBIARE 2021: `"2021-06-03/2021-07-23"`).

`criterio_parada` se actualiza en el mismo commit por consistencia interna — su texto anterior *era sobre* `periodo_levantamiento` ("No calcular mientras periodo_levantamiento no esté fijado…"); dejarlo intacto habría creado una especificación gobernada que se contradice a sí misma. `tools/curador_registro/produce.py::execute` no lee `criterio_parada` en ninguna rama de su lógica (grep confirmado, cero referencias fuera de `prepare_production.py::MASTER_REQUIRED`, que solo exige que el campo exista, no un valor concreto) — es documentación obligatoria, no un gate operativo; el gate real son los `MATERIAL_FIELDS` de `produce.py:19-23`, ninguno de los cuales cambia de mecanismo en este commit.

## §2 · Corroboración de los otros campos ya fijados por SELLO-B (ninguno cambia de valor)

La misma ficha 922, fuente independiente del FD/PDF que usó SELLO-B (11/ago), corrobora tres de los seis campos que SELLO-B ya fijó:

- **`periodo_referencia`** — tabla "Periodo de referencia" de la ficha, fila `2022-10-24 / 2022-12-16 / "El mismo día de la entrevista, de acuerdo a la variable"`. Corrobora (no cambia) `periodo_referencia_por_variable.P7_12_7 = "Momento de la entrevista (reactivo sin ventana retrospectiva explícita)"` ya fijado en SELLO-B.
- **`FAC_ELE`→`TPER_ELE`** — campo "Factores de expansión" de la ficha, verbatim: *"FAC_ELE Ponderador de la población de 15 a 60 años. Tabla TPER_ELE"*. Corrobora (no cambia) `ponderador = "FAC_ELE"` ya fijado en SELLO-B.
- **Diseño oficial** — §1 "Diseño estadístico" de la ficha: *"Su diseño es probabilístico, estratificado, unietápico y por conglomerados"*. Idéntico verbatim a `diseno_muestral.tipo` ya fijado en SELLO-B.

Ningún valor cambia; los tres quedan re-confirmados contra una segunda fuente independiente. Nota aparte, no verificada aquí por estar fuera de perímetro: la ficha también trae `DEFF=3.05`, confianza `90%`, tamaño de muestra `6,761→7,021` viviendas — mismas cifras que cita U2 en su propio texto; U2 las verificará si las necesita.

## §3 · Corrección de una premisa del propio encargo, verificada contra código antes de escribir

El encargo instruye declarar: *"documentacion_fuente no existía como campo al momento de esta enmienda; la documentación viaja en la nota del expediente."* **Verificado contra el código antes de escribir esta especificación (misma disciplina que E4b SELLO-B §0 aplicó a un mensaje inyectado — ver `forense/notas/2026-08-11-e4b-sello-b-corrida-b.md`): la premisa es falsa tal como está escrita.** `documentacion_fuente` sí existe como campo reconocido — `tools/curador_registro/prepare_production.py:21` (conjunto `FORBIDDEN`), con esquema propio en `tools/curador_registro/schemas/production-spec.schema.json` (`type: array`, `{url, fecha_consulta, campos_resueltos}` requeridos) y validador `tools/curador_registro/validate.py::documentacion_fuente_errors` — los tres ya en `origin/main` vía PR #177 ("ESTRUCTURA", P3), fusionado el 12/ago **antes** de que este acto abriera. `PROPUESTA-remediacion-brecha-documental.md` (la propuesta que originó este mismo programa U1-U2-U3, entrada verbatim al repo por CABLEADO-100) confirma que P3 es precisamente este campo.

**La razón real por la que `ESP-OPACA-B-d13ec4fe` no lo puebla no es que el campo falte: `tools/curador_registro/validate.py:52-57` lo exime por nombre.** `ADR-70(b)` declara `documentacion_fuente` obligatorio solo para especificaciones nuevas; una lista cerrada (no una heurística de fecha) exime explícitamente a las tres especificaciones ya selladas al momento del ADR — `ESPECIFICACIONES_SELLADAS_SIN_DOCUMENTACION_FUENTE = {"ESP-OPACA-A-7baf278d", "ESP-OPACA-B-d13ec4fe", "ESP-OPACA-C-9ecb5c61"}` — con la nuestra nombrada explícitamente. **La conclusión operativa del encargo (la documentación de esta enmienda viaja en esta nota, no en el campo estructurado) es correcta; la premisa que la sostenía no lo era.** No se puebla `documentacion_fuente` en este commit — consistente con la exención real, no con la premisa original. Se deja constancia aquí porque la clase de error (una cita a código no verificada antes de gobernar un artefacto) es exactamente la que este programa lleva quince sesiones combatiendo (`PROPUESTA-remediacion-brecha-documental.md`, tabla "EL DEFECTO, NOMBRADO").

## §4 · Hallazgo de método, relevante para U3 (ocho fichas RNM por leer la próxima sesión)

Un primer intento de leer esta misma ficha con la herramienta de fetch web resumida por un modelo pequeño **atribuyó mal el rótulo de fila en ambas tablas de fecha**: reportó *"Levantamiento específico: 2023-01-23 a 2023-05-26"* (esas fechas pertenecen, verificado por `<tr>` crudo, a la fila **"Documentación"**) y *"Ejecución de recolección: 2022-09-05 a 2022-12-23"* (esas fechas pertenecen a la fila **"Capacitación"**), y colocó el rango correcto (`2022-10-24/2022-12-16`) bajo "Periodo de referencia" en vez de bajo la fila "Levantamiento" de la tabla de ejecución donde también aparece verbatim. El número final coincidió con la fuente por una coincidencia real del dominio (el ítem de referencia "mismo día de la entrevista" comparte fecha con el levantamiento cuando el marco temporal del reactivo es el día mismo de campo) — no porque la herramienta haya leído bien la tabla. **No se usa una herramienta de fetch resumida por IA para extraer texto de fichas RNM con más de una tabla de fechas — se pide el HTML crudo y se parsea por `<tr>`/`<td>` explícitos.** Aplicable directo a U3, que abre ocho fichas de la misma familia la próxima sesión.

## §5 · Qué NO se calcula en este commit

Ningún resultado se calcula. `tools/curador_registro/produce.py` no se invoca. Los seis campos materiales restantes no se tocan — siguen exactamente como los fijó SELLO-B, 2026-08-11.

**El primer resultado que produzca este procedimiento es el que se reporta.**
