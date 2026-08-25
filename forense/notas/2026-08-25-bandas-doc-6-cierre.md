# Nota · ACTO BANDAS-DOC-6 — cierre

**Entorno:** NUBE (`cloud_default`), modelo Opus, sin red/microdato (declarado, sonda saltada). **Ejecuta:** `FP-94`/`FP-126` (GO de mesa 24/ago, `ADR-155`, «FP94: GO.»). **ADR de este acto:** `ADR-160` (candidateado `ADR-159`, renumerado al fusionar `main` — ver §5).

## 0 · Arranque

Rama `claude/bandas-doc-prereg-wzwm1q`, sin commits previos al arrancar. Localizada la regla sellada (`ADR-135(e)`/`FP-83` `FIRMADA`, `canon/gobernanza-v1_15.md`), la fila de tablero que gatea el acto (`FP-94` `FIRMADA` sin `ejecutada_en`; su sucesora operativa real `FP-126`, también `FIRMADA` sin `ejecutada_en` — verificado leyendo `forense/firmas-pendientes.tsv` completo) y las seis celdas objetivo (`forense/marco-candidatas-piloto-v1_0.tsv` líneas 56–61, `DOC-01`..`DOC-06`).

## 1 · Derivación de las seis bandas

Detalle completo, celda por celda, con cálculo a la vista: `forense/prereg-duelo-v2/bandas-doc-01-06-v1_0.md`. Resumen:

| id | ancho | fuente del ancho |
|---|---|---|
| `DOC-01` | `±0.05 pp` | redondeo de publicación (HR Ratings, 1 decimal) |
| `DOC-02` | `±0.05 pp` | redondeo de publicación (HR Ratings, 1 decimal) |
| `DOC-03` | `±0.0065` | propagación de redondeo de primer orden sobre una razón de dos cifras a 1 decimal, no enunciada en ninguna fuente |
| `DOC-04` | `±0.5 pp` | rango ya publicado directamente por la fuente (SEC 10-K FirstCash) |
| `DOC-05` | `±0.5 M` (solo numerador) | redondeo del numerador (castigos, al millón); **denominador no localizado en el corpus** — banda incompleta declarada, no rellenada |
| `DOC-06` | `±0.5 pp` | redondeo del mismo emisor (HR Ratings) sobre la cifra que parametriza; nivel de la ola 4T2026 no fijado, es futuro |

Ninguna banda introduce una cuarta fuente de error distinta de las tres que `FP-83` autoriza (revisión / redondeo de publicación / ventana temporal). `DOC-05` queda con el denominador declarado como hueco, no inventado — verificado por lectura completa de `corpus/forense/compass-4-e29a28d4-credito-popular-2026.md` (126 líneas) y `grep` dirigido sobre variantes de "cartera total"/"balance"/"activos totales", cero coincidencias para Compartamos.

## 2 · Tablero

`FP-94` → `FIRMADA`, `ejecutada_en = 2026-08-25`, citando este documento y `forense/prereg-duelo-v2/bandas-doc-01-06-v1_0.md`. `FP-126` (la fila que en la práctica gatea este acto) recibe la misma `ejecutada_en`.

**Corrección declarada, no silenciosa:** el texto de `firmada_en` de `FP-94` citaba "Fila sucesora `FP-125` abierta FIRMADA" — `FP-125` es la sucesora de `FP-70` (ENASIC/U2-EV-1), no de `FP-94`. La sucesora real de `FP-94` es `FP-126` (verificado leyendo ambas filas de `forense/firmas-pendientes.tsv` una junto a la otra). Se corrige el texto a `FP-126`, sin tocar la firma de mesa verbatim ni ningún otro campo de la fila.

## 3 · Higiene heredada — resuelta en dos pasos, con el retraso declarado

**Primer paso.** El encargo pide archivar `forense/encargos/2026-08-24-RECENSO-DISENO-2.md` como `CONSUMIDO` citando `PR #321`. Verificado por `ls forense/encargos/` (comando, no memoria): **ese archivo no existía en el árbol** — ni con ese nombre ni con ninguna variante de mayúsculas/Ñ. Lo único que existía con ese nombre de acto era la **nota** de salida, `forense/notas/2026-08-24-recenso-diseno-2.md` (`ACTO RECENSO-DISEÑO-2`, `ADR-153`, cierra `FP-117`/`FP-120`, abre `FP-123`), cuyo propio cierre declara verbatim:

> "No se marca el encargo como CONSUMIDO ni se hizo commit/push — instrucción explícita del encargo; el worktree queda con los cambios sin commitear para revisión del supervisor."

Esa frase confirma que un encargo `.md` para `RECENSO-DISEÑO-2` existió como texto (citado por su propia nota) pero **nunca se commiteó al árbol** — incumpliendo la convención propia de este directorio (`forense/encargos/convencion.md`: "todo encargo que se lance se commitea aquí antes o junto con su lanzamiento"). La fila `FP-123` del tablero lo corrobora: su columna `encargo` dice "instruccion directa sin encargo .md propio" para el sucesor de `RECENSO-DISEÑO-2`. Este acto no fabricó el archivo faltante en ese momento — la convención exige "el texto completo del encargo tal como se lanzó, no un resumen", y no se tenía ese texto; inventarlo habría sido exactamente la clase de invención que el propio encargo de este acto prohíbe ("sin inventos nuevos").

**Segundo paso, misma conversación.** Dirección aportó el texto verbatim del encargo original (`ENCARGO · ACTO RECENSO-DISENO-2 — «damos de alta TODO» (las 37 llaves)`, redactado 24/ago/2026, `SHA` de redacción `754eb86`). Con el texto en mano, se archivó `forense/encargos/2026-08-24-RECENSO-DISENO-2.md`, verbatim, con su cabecera completa y un `## Cierre` que cita el resultado real ya conocido por `forense/notas/2026-08-24-recenso-diseno-2.md`/`FP-117`/`FP-120`/`FP-123`: **13 llaves reales, no 37** — la discrepancia que el propio bloque de VERIFICACIÓN DE EXISTENCIA del encargo ya anticipaba ("la lista manda sobre el 37 con la discrepancia declarada") — fusionado como `PR #321` (`3bae09f`, citado en `ADR-155`). No se reabre ni edita `data/diseno-muestral.yaml` ni `forense/firmas-pendientes.tsv`: ya reflejan ese resultado desde el 24/ago.

## 4 · Perímetro

Escrito: `forense/prereg-duelo-v2/bandas-doc-01-06-v1_0.md` (nuevo) · `forense/encargos/2026-08-25-BANDAS-DOC-6.md` (nuevo, verbatim, `CONSUMIDO`) · `forense/encargos/2026-08-24-RECENSO-DISENO-2.md` (nuevo, archivado `CONSUMIDO` en el segundo paso de §3, verbatim + `## Cierre`) · `forense/notas/2026-08-24-recenso-diseno-2-cierre.md` (renombrada en §5, contenido sin editar) · `forense/firmas-pendientes.tsv` (`FP-94`/`FP-126` `ejecutada_en`; corrección de `firmada_en` de `FP-94`) · `canon/gobernanza-v1_15.md` (`ADR-160`) · `canon/estado-programa-v1_10.md` (conteo de ADR y recifrado de la suite, ver §5) · esta nota. **No** se tocó `forense/marco-candidatas-piloto-v1_0.tsv` (solo lectura — las bandas viven en el documento nuevo, no en el marco), `scoring-adv1-m3.py` ni ningún otro script del duelo (el árbitro no corrió sobre ninguna celda), `milpa/`, `data/` (incl. `diseno-muestral.yaml`, ya reflejaba el resultado real desde el 24/ago), `corpus/` (solo lectura), `canon/modelo-decision-v4_0.md`, ni ningún `resultado.tsv`. Ningún contador de Hito D, condicionales o coeficientes se mueve.

## 5 · Merge de `main` (post-push) — colisión de `ADR`, autocolisión `T02`, recifrado `T15`/`T16`

Al empujar esta rama, PR #329 quedó `mergeable_state: dirty` — conflicto real contra `main`, que en el ínterin había fusionado `PR #327` (`ACTO SPEC-R10.1-v2`). Resuelto con `git merge origin/main`:

- **Colisión de `ADR`:** `ACTO SPEC-R10.1-v2` tomó `ADR-159` antes que este acto. Regla de la casa (renumera quien fusiona segundo, escrita en decenas de ADR anteriores): este acto renumera su entrada a **`ADR-160`**, re-verificado contra el árbol fusionado (`origin/main = e8ce5ef`) por `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -1` — máximo `159`, único `160`, sin huecos. `forense/firmas-pendientes.tsv` fusionó sin colisión de `id` (`FP-128`, de `SPEC-R10.1-v2`, es disjunta de `FP-94`/`FP-126`).
- **Autocolisión `T02`, propia de este acto:** el nombre normalizado de `forense/encargos/2026-08-24-RECENSO-DISENO-2.md` (archivado en §3) colisiona con la nota preexistente `forense/notas/2026-08-24-recenso-diseno-2.md` — mismo defecto que `forense/encargos/convencion.md` ya advierte por construcción (T02 no distingue directorio). Resuelto renombrando la nota a `forense/notas/2026-08-24-recenso-diseno-2-cierre.md`, sin editar su contenido — mismo mecanismo que `ADR-135`/`ADR-158`/`ACTO SPEC-R10.1-v2` ya usaron para el mismo defecto.
- **Recifrado `T15`:** las citas a `159 ADR` en la cabecera de `canon/gobernanza-v1_15.md` y en `canon/estado-programa-v1_10.md` (incluida la del propio párrafo de `SPEC-R10.1-v2`, que era correcta cuando se escribió) se recifran a `160`; la cita histórica de `SPEC-R10.1-v2` se marca `{cita-historica}` en vez de editarse, mismo mecanismo que el resto del archivo ya usa.
- **Recifrado `T16`:** el WARN total vigente baja de 145 a **143** por causas ajenas a este acto (ya presentes en `main` antes de fusionar, no re-derivadas aquí en detalle — fuera de perímetro). Declarado en dos sitios de `canon/estado-programa-v1_10.md` (línea de `T03`/WARN total y la cabecera de la suite) con un nuevo párrafo `*(Recifrado ...)*` propio de este acto, sin editar el de `SPEC-R10.1-v2`.
- **Verificación final:** `python3 tests/check.py --baseline` → `19 FAIL · 143 WARN`, mismas seis categorías de FAIL que el núcleo histórico (T09:8·T05:5·T02:2·T06:2·T08:1·T11:1), **`LÍNEA BASE: VERDE`** — nada nuevo frente a `tests/baseline.json`, sin `--freeze`.

Perímetro de este merge: los cinco archivos de arriba, ninguno más. No se editó ninguna línea de contenido de `ACTO SPEC-R10.1-v2` (`forense/encargos/2026-08-25-R10_1-SPEC-V2-PROPUESTA.md`, `forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md`, `forense/notas/2026-08-25-r10-1-spec-v2-propuesta-cierre.md`) más allá de lo que el merge automático ya resolvió sin conflicto.

**Este acto no calculó, en ningún punto, un estimado puntual de ninguna variable mexicana del piloto** — solo derivó anchos de banda a partir de la precisión ya publicada de las cifras del corpus (o, en `DOC-05`, declaró que un operando no está localizado). El árbitro no corrió: el cierre del documento de bandas es explícito — "el primer resultado que produzca el árbitro contra estas bandas es el que se reporta".
