# ACTO GEN2-ARCHIVO-LECTURA-F5-1 · cierre

**Trámite de archivo.** Mesa pegó los documentos que `NC-0219` pedía; este acto los commitea
verbatim con cabecera de procedencia y `sha256` re-derivado. **Contador: cero** — cero corridas
selladas, cero RESULT, cero adopciones, cero llamadas, cero microdato. Ningún archivo de `canon/`
se toca salvo el censo de rótulo. Ninguna cifra se re-adjudica.

## 1 · Qué llegó y qué se archivó

| adjunto de mesa (nombre del adjunto, no ruta del árbol) | sha256 del adjunto | qué es | destino |
|---|---|---|---|
| LECTURA-ESTRATEGICA-F5-v1_1-2026-09-15 (.md), 59 ln | `a51daa09…` | **la lectura v1.1** — la que `NC-0219` pedía y no había llegado | `forense/notas/LECTURA-ESTRATEGICA-F5-v1_1-2026-09-15.md` |
| ADVERSARIAL-ASTRA-1-LECTURA-F5-2026-09-15 (.md), 148 ln | `1de3c742…` | el adversarial de Astra, **con** su cabecera de procedencia ya puesta | `forense/notas/ADVERSARIAL-LECTURA-ESTRATEGICA-F5-2026-09-15.md` |
| ADVERSARIAL-LECTURA-ESTRATEGICA-F5-2026-09-15 (.md), 146 ln | `00c3fec1…` | **el mismo texto sin cabecera** | **no se archiva** — duplicado, ver §2 |
| LECTURA-ESTRATEGICA-F5-2026-09-15 (.md), 80 ln | `7fc366ef…` | la **v1.0**, objeto del adversarial. `NC-0219` no la pedía | `forense/notas/LECTURA-ESTRATEGICA-F5-2026-09-15.md`, declarada SUPERADA |
| ASTRA-RECOMENDACIONES-2-CINCO-PREGUNTAS-2026-09-15 (.md), 4 ln / 446 B | `37bfbed1…` | **marcador vacío, no el texto** | **PARO** — `NC-0225`, ver §4 |

`sha256` de lo commiteado (`forense/notas/*.sha256`, re-derivado sobre el archivo tal como queda en el árbol):

| archivo | sha256 |
|---|---|
| `LECTURA-ESTRATEGICA-F5-2026-09-15.md` | `c1b59043aef39d1ca3ca4497402734f0ec7b4fe972d75787d725ee38dee059a0` |
| `LECTURA-ESTRATEGICA-F5-v1_1-2026-09-15.md` | `498e5adcb32e4a78043ce6cddf05c16c06d5d38fb9debaa80f0aecfe79b563de` |
| `ADVERSARIAL-LECTURA-ESTRATEGICA-F5-2026-09-15.md` | `1de3c74203f851a456a6d86e862ba4c986269ffe3b6d7773ff057879527dc0e0` |

El del adversarial **coincide con el del adjunto**: como ya traía su cabecera, el archivo
commiteado es byte-idéntico al que mesa pegó (`cmp`, exit 0). Los otros dos difieren del adjunto
solo en las dos líneas de cabecera que este acto antepone; el cuerpo se verificó verbatim con
`diff <(tail -n +3 archivado) adjunto` → sin diferencias en los dos casos.

## 2 · El duplicado, declarado

Mesa pegó el adversarial **dos veces**. `diff` entre la versión sin cabecera y la versión con
cabecera menos sus dos líneas de cabecera: **idénticos**. Se archiva **una sola vez**, la que
trae la procedencia. No hay dos adversariales y este acto no inventa uno segundo.

## 3 · Control de contenido, no solo de procedencia

Un trámite de archivo no adjudica; pero una comprobación era gratis y se corrió, porque decide si
la v1.1 es un documento nuevo o una paráfrasis del anterior:

**La corrección material de identidad del adversarial §2 — «U3 incluye `TRA-M-03`, no `TRA-M-07`» — REPRODUCE.**
`data/corrida0/CALC-TRIADA-0002/resultados.json` (sellado) lista
`CIV-M-01/02/04/10/12/13, FAM-M-01/05/06/07, TRA-M-02, TRA-M-03`; `TRA-M-07` **no aparece**.
La v1.0 §1 la tenía mal; la v1.1 §1 la corrige y marca `[CORREGIDO]`.

Consecuencia para el archivo: **la v1.1 no es una paráfrasis de la v1.0** — incorpora correcciones
verificables, y la única comprobable sin gasto reproduce contra el sellado. Eso es lo que justifica
archivar las dos y declarar la v1.0 superada en vez de sustituirla en silencio.

*Lo que este acto NO hace:* no verifica las demás cifras de la v1.1 (`68.88%`, `54.17%`, la tabla
de 9 celdas, la inversión por ponderación). La cabecera de la v1.1 dice que dirección las verificó
contra el repo con comando; este acto lo **archiva como afirmación de dirección**, no lo acredita.
Las tres primeras ya están acreditadas por otra vía —`GEN2-INFORME-INTERNO-F5-1` §A.2/§A.3— y no
por este trámite.

## 4 · Lo que sigue sin llegar

El **segundo documento de Astra** (recomendaciones sobre las cinco preguntas) **no viajó**: su
adjunto trae 4 líneas y 446 bytes, y su único contenido es la cabecera más la línea que dice que
el acto de archivo lo toma del adjunto de mesa y que si el adjunto no viaja, PARO. Es el marcador,
no el texto.

**No se archiva y no se reconstruye.** Commitear un archivo vacío bajo cabecera de procedencia
asentaría una procedencia que no existe — exactamente lo que el paso existe para impedir, y el
mismo criterio con que `NC-0219` se negó a rehacer de paráfrasis.

`NC-0219` **no lo pedía**, así que cierra completa con lo que llegó. El hueco se asienta aparte en
**`NC-0225`**, en `PARO-PREMISA`, en vez de enterrarse en el cierre de otra fila: la FIRMA DE MESA
del 15/sep (D1–D5) conserva procedencia documentada de su objeto principal —la lectura v1.1 y el
adversarial, archivados aquí— pero el segundo insumo que la firma también cita sigue sin respaldo
en el árbol. **Ninguna cifra del programa depende de él.**

## 5 · Tabla de pendientes

- **`NC-0219` → CERRADA** (`fecha_cierre` 2026-09-15), citando este PR.
- **`NC-0225` → ABIERTA**, `PARO-PREMISA`, sucesor nombrado: mesa pega el verbatim y un trámite lo
  commitea, precedente ya consumado tres veces (`NC-0082`, `NC-0134`, `NC-0219`).

Edición **quirúrgica**: se reemplazó la línea física de `NC-0219` y se añadió la de `NC-0225`.
`git diff --numstat` = `2 1`. Un primer intento por round-trip de `csv` re-citó ocho filas ajenas
(`NC-0168`, `NC-0175`, `NC-0176`, `NC-0183`, `NC-0184`…) sin cambiarles el contenido; **se
descartó con `git checkout`** y se rehízo por línea. Queda anotado porque el defecto es
reproducible: `forense/no-corrido.tsv` tiene 20 filas de 10 campos y 201 de 12, y un `csv.writer`
uniforma comillas que el árbol no tiene.

## 6 · Verificación

| qué | comando | resultado |
|---|---|---|
| suite, línea base | `python3 tests/check.py --baseline` | **VERDE** antes y después |
| cuerpo verbatim (v1.0, v1.1) | `diff <(tail -n +3 …) <adjunto>` | sin diferencias |
| adversarial byte-idéntico | `cmp <archivado> <adjunto>` | exit 0 |
| duplicado | `diff <(tail -n +3 con-cabecera) sin-cabecera` | idénticos |
| `TRA-M-03` vs `TRA-M-07` | `grep -o 'TRA-M-0[0-9]' data/corrida0/CALC-TRIADA-0002/resultados.json \| sort \| uniq -c` | `TRA-M-02` 1 · `TRA-M-03` 1 · sin `TRA-M-07` |
| esquema de la tabla intacto | `csv` sobre `forense/no-corrido.tsv` | 221 registros, 201×12 + 20×10 (los 20 son preexistentes) |

D-6 aplicado: el acto se declara `ACTO GEN2-ARCHIVO-LECTURA-F5-1` en todo archivo que escribe.
Desviación declarada: la rama la fija el arnés de la sesión (`claude/new-session-mcwr7o`), no el
rótulo; el rótulo se censa en `canon/registro-rotulos.tsv`.

## 7 · Por qué los tres archivos llevan el nombre propio del documento

No llevan el prefijo `2026-09-15-GEN2-…` de las notas de acto. Llevan el nombre con que el
documento se llama a sí mismo, y la razón es material, no de gusto:

El adversarial, en su §«Alcance y evidencia», dice *«Documento revisado:
`LECTURA-ESTRATEGICA-F5-2026-09-15.md`»*. Con los nombres de acto, `T03` marcaba esa línea como
**cita rota** — y no se podía arreglar editando el texto, porque es un verbatim. Nombrar el
archivo de la v1.0 como el documento se nombra **hace la cita verdadera**: el archivo que el
adversarial dice haber revisado existe ahora en el árbol, con ese nombre. La alternativa —dejar el
warning, o añadir una exención en `tests/check.py`— habría suprimido la señal en vez de satisfacerla.

Los otros dos toman el nombre propio por consistencia con el primero. La procedencia y el acto no
se pierden: van en la cabecera de cada archivo y en `canon/registro-rotulos.tsv`.

**Ambigüedad declarada:** mesa pegó el adversarial bajo dos nombres
(`ADVERSARIAL-ASTRA-1-LECTURA-F5-2026-09-15` y `ADVERSARIAL-LECTURA-ESTRATEGICA-F5-2026-09-15`,
mismo cuerpo). Se archivó **el contenido de la copia con cabecera** bajo el **segundo** nombre,
que es el que nombra al documento revisado. Si mesa prefiere el otro, es un `git mv` y un
`sha256` re-derivado, sin tocar el cuerpo.

## 8 · Intento fallido, anotado

El primer pase nombró los tres archivos `2026-09-15-GEN2-…` y dejó la **línea base en ROJO con 6
entradas nuevas de `T03`**: cinco por citar en el cierre los nombres de los adjuntos de mesa (que
no son rutas del árbol) y una por la cita interna del adversarial. Las cinco primeras se
arreglaron quitándoles las comillas de código —un adjunto no es un archivo del repo y no debe
citarse como si lo fuera—; la sexta, con el renombrado de §7. **Se anota porque el rojo lo causó
este acto y se corrigió dentro de él**, no porque estuviera antes.
