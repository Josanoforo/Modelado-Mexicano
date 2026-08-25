# Nota · ACTO BANDAS-DOC-6 — cierre

**Entorno:** NUBE (`cloud_default`), modelo Opus, sin red/microdato (declarado, sonda saltada). **Ejecuta:** `FP-94`/`FP-126` (GO de mesa 24/ago, `ADR-155`, «FP94: GO.»). **ADR de este acto:** `ADR-159`.

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

## 3 · Higiene heredada — lo que NO se hizo, y por qué

El encargo pide archivar `forense/encargos/2026-08-24-RECENSO-DISENO-2.md` como `CONSUMIDO` citando `PR #321`. Verificado por `ls forense/encargos/` (comando, no memoria): **ese archivo no existe en el árbol** — ni con ese nombre ni con ninguna variante de mayúsculas/Ñ. Lo único que existe con ese nombre de acto es la **nota** de salida, `forense/notas/2026-08-24-recenso-diseno-2.md` (`ACTO RECENSO-DISEÑO-2`, `ADR-153`, cierra `FP-117`/`FP-120`, abre `FP-123`), cuyo propio cierre declara verbatim:

> "No se marca el encargo como CONSUMIDO ni se hizo commit/push — instrucción explícita del encargo; el worktree queda con los cambios sin commitear para revisión del supervisor."

Esa frase confirma que un encargo `.md` para `RECENSO-DISEÑO-2` existió como texto (citado por su propia nota) pero **nunca se commiteó al árbol** — incumpliendo la convención propia de este directorio (`forense/encargos/convencion.md`: "todo encargo que se lance se commitea aquí antes o junto con su lanzamiento"). La fila `FP-123` del tablero lo corrobora: su columna `encargo` dice "instruccion directa sin encargo .md propio" para el sucesor de `RECENSO-DISEÑO-2`.

**Este acto no fabrica el archivo faltante.** La convención exige "el texto completo del encargo tal como se lanzó — no un resumen", y este acto no tiene ese texto (no vive en ninguna conversación ni archivo accesible desde este entorno). Escribir un `forense/encargos/2026-08-24-RECENSO-DISENO-2.md` con un texto reconstruido de memoria y marcarlo `CONSUMIDO` citando `PR #321` sería exactamente la clase de invención que el propio encargo de este acto prohíbe ("sin inventos nuevos") y que la convención del directorio existe para prevenir (un encargo fabricado es tan malo como uno nunca escrito — mismo principio que `PD-01` ya declaró para los descartes). Queda declarado como deuda de higiene abierta en `ADR-159(c)`, en `canon/estado-programa-v1_10.md` y aquí: falta que quien tenga el texto original del encargo lo commitee con su cabecera completa antes de que pueda cerrarse.

## 4 · Perímetro

Escrito: `forense/prereg-duelo-v2/bandas-doc-01-06-v1_0.md` (nuevo) · `forense/encargos/2026-08-25-BANDAS-DOC-6.md` (nuevo, verbatim, `CONSUMIDO`) · `forense/firmas-pendientes.tsv` (`FP-94`/`FP-126` `ejecutada_en`; corrección de `firmada_en` de `FP-94`) · `canon/gobernanza-v1_15.md` (`ADR-159`) · `canon/estado-programa-v1_10.md` (conteo de ADR, `158→159`) · esta nota. **No** se creó `forense/encargos/2026-08-24-RECENSO-DISENO-2.md` (§3). **No** se tocó `forense/marco-candidatas-piloto-v1_0.tsv` (solo lectura — las bandas viven en el documento nuevo, no en el marco), `scoring-adv1-m3.py` ni ningún otro script del duelo (el árbitro no corrió sobre ninguna celda), `milpa/`, `data/`, `corpus/` (solo lectura), `canon/modelo-decision-v4_0.md`, ni ningún `resultado.tsv`. Ningún contador de Hito D, condicionales o coeficientes se mueve.

**Este acto no calculó, en ningún punto, un estimado puntual de ninguna variable mexicana del piloto** — solo derivó anchos de banda a partir de la precisión ya publicada de las cifras del corpus (o, en `DOC-05`, declaró que un operando no está localizado). El árbitro no corrió: el cierre del documento de bandas es explícito — "el primer resultado que produzca el árbitro contra estas bandas es el que se reporta".
