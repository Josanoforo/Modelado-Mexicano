ENCARGO · ACTO GEN2-INFORME-INTERNO-F5-1
Documento del programa: qué podemos usar, para qué, qué comparaciones son válidas, dónde falta evidencia — breve, legible por un externo, con anexo técnico

CABECERA · redactado contra `5973f12` (merge de #785 — base verificada en el ARRANQUE, 0 commits detrás de `origin/main`) · ENTORNO: **NUBE** (`tools/entorno.py`: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, `corpus=NO(examinados=0)`, `data_raw:NO`, red no ejecutada — este acto no abre microdato, no descarga y no llama a ningún modelo) · COMPUERTA: ninguna — el encargo no declara `GATED a`, `Estado: GATED a` ni `COMPUERTA:`, y declara explícitamente «Concurrencia: ninguna sobre archivos; lee lo que los demás sellan» · MODELO: Opus (integral) · Estado: VIVO · candidatos FP/ADR: deriva al cierre.
LANZAMIENTO, verbatim (mesa, 15/sep/2026): el texto de abajo —el bloque del acto y, tras él, la FIRMA DE MESA de la misma fecha sobre la LECTURA ESTRATÉGICA F5 v1.1— es el mensaje de lanzamiento tal como llegó. Este archivo lo fija por A.3 porque llegó pegado en el mensaje que invocó `/acto`, no como archivo del repo. No se edita: ni para corregir acentos, ni para desambiguar rótulos, ni para complacer a un test (D-6/T25 se resuelven en el censo de `registro-rotulos.tsv` y en el allowlist, nunca tocando el verbatim).

VERIFICACIÓN DE EXISTENCIA (A.8, contestada por el ejecutor contra `5973f12` — el lanzamiento llegó sin el bloque y A.8 manda pararse o contestarlo con comando, no suponerlo):

(1) ¿Existe ya la estructura? **NO, y ese hueco es entregable por el propio encargo.** El índice de infraestructura vigente es `data/INFRAESTRUCTURA-v1_0.md` (`forense/notas/2026-08-13-indice-infraestructura.md` es su nota). Sus nueve dominios y su tabla «Si tu encargo hace X, escribe en Y» cubren adquirir, sondear, estimar, celda-D, veredicto de Hito D, sellar gobierno, hallazgo/nota, encargo y decisión de mesa pendiente. **Ninguna fila cubre «voy a escribir un documento del programa para un lector externo»**, y las únicas rutas `canon/` que el índice gobierna son `gobernanza`, `estado-programa` y `modelo-decision`:
```
$ grep -c "documento del programa\|informe del programa\|lector externo" data/INFRAESTRUCTURA-v1_0.md
0
$ grep -n "^## Dominio" data/INFRAESTRUCTURA-v1_0.md | wc -l
9
```
(universo del negativo, A.13: `data/INFRAESTRUCTURA-v1_0.md`, 1 archivo, 866 líneas). El encargo lo anticipa —«o donde el índice de infraestructura diga; si no lo cubre, ese hueco es entregable»— así que la ruta `canon/informe-programa-v1_0.md` se toma del encargo y el índice se corrige por regla de conducto (`ADR-70(c)`), en la misma entrega.

(2) ¿Existe ya el contenido? **Las fuentes sí; el documento no.** `canon/informe-programa-v1_0.md` no existe (`git cat-file -e origin/main:canon/informe-programa-v1_0.md` → falla). Lo que sí existe, sellado, es todo lo que el informe tiene que citar: `forense/notas/2026-09-10-GEN2-F5-APRENDIZAJES-Y-SUCESOR-diagnostico.md` y su directorio de artefactos `forense/prereg-duelo-v2/F5-aprendizajes-sucesor-v1_0/` (de donde salen 68.88% y la inversión por grupo), `forense/notas/2026-09-14-GEN2-B-MARCO-cierre.md` (B, cobertura 10/14 y la tabla por celda), `forense/notas/2026-09-14-GEN2-F5-DOCUMENTAL-RUN-2-cierre.md` (la secundaria, 16/16 vs 0/16), `forense/notas/2026-09-11-GEN2-EVALUACION-SIN-FUGAS-cierre.md`, `forense/prereg-duelo-v2/F5-transferencia-reservada-spec-v1_0.md` (F6), `forense/firmas-pendientes.tsv` (FP-373 FIRMADA/EJECUTADA, FP-374 ABIERTA) y `forense/no-corrido.tsv` (NC-0152, NC-0161/0162, NC-0180, NC-0187).

(3) ¿Cobertura retroactiva? El encargo declara que el sello de **D-A** se incorpora «cuando exista, sin esperarlo». Verificado: **no existe todavía** en el árbol ni en el remoto —
```
$ git ls-remote --heads origin | grep -icE "d-a|informe"
0
$ ls forense/encargos/ | grep -c "GEN2-D-A"
0
```
(universo: 1 remoto y 336 archivos de `forense/encargos/`). La **LECTURA ESTRATÉGICA F5 v1.1** y el **adversarial de Astra** que la firma cita tampoco están en el repo (`grep -rl "LECTURA ESTRAT"` → 0 sobre `canon/` + `forense/`, 2 174 archivos examinados): son documentos de mesa. El informe no los reconstruye ni los cita como si los hubiera leído — deriva su tabla de las notas selladas, con procedencia declarada, y dice que **no** es el sello de D-A.

---

## PIEZAS — texto de mesa, verbatim

NUBE · ACTO GEN2-INFORME-INTERNO-F5-1 (Opus, integral; documento del programa — carga el módulo de auditoría de rigor extremo porque afirma algo sobre el modelo)

* Objeto: `canon/informe-programa-v1_0.md` (o donde el índice de infraestructura diga; si no lo cubre, ese hueco es entregable): qué podemos usar, para qué, qué comparaciones son válidas, dónde falta evidencia. Breve, legible por un externo, anexo técnico con las tablas y sus universos (A.10 en cada cifra).
* Tesis fija, verbatim de D1 — el acto no la reinterpreta. M: funciones acreditadas vs. valor predictivo por demostrar. B: diagnóstico (piso de persistencia), no tesis. Primaria: SIN-GANADOR-ÚNICO con su dependencia de composición declarada (68.88% cívico; inversión con igual peso por grupo). Secundaria: éxito local en dos celdas con paquetes preparados. F6: propuesta pendiente con su gate (lista nominal).
* Fuentes: solo registro derivado y notas selladas; incorpora el sello de D-A cuando exista, sin esperarlo (su tabla ya está en la lectura v1.1 con procedencia). Cierra con reglas de decisión y el módulo de auditoría contestado — incluida la pregunta v2.3 (contadores movidos: cero, dicho).
* Perímetro: el documento nuevo, su anexo, índice de infraestructura si hace falta. No toca registro, milpa ni F5. Concurrencia: ninguna sobre archivos; lee lo que los demás sellan.

FIRMA DE MESA, mesa, 15 de septiembre de 2026 — sobre la LECTURA ESTRATÉGICA F5 v1.1 y el adversarial de Astra:

D1 · Tesis. Se acepta: mediciones reproducibles, éxito documental local y persistencia competitiva; el valor predictivo añadido de M queda por demostrar. M conserva sus otras funciones (organización de evidencia, aplicación consistente de reglas, escenarios), que se distinguen de la precisión predictiva y se acreditan por función. Esta reserva no es un juicio negativo del proyecto.

D2 · D-A. Se registra la comparación descriptiva (9 celdas comunes, puntos de la tríada limpia, B de persistencia, errores y cobertura) como corrida de registro; sin pareadas nuevas ni adjudicación; SIN-GANADOR-ÚNICO se conserva; B-MARCO se consume (NC-0187 cierra por consumo, NC-0180 cierra). Cero llamadas.

D3 · F6. F6 evalúa transferencia de M (protocolo FP-374, M vs L_SOLO); B se conserva como referencia adicional con reglas fijadas antes de ver resultados, y ganarle a L no acredita ganarle a B. La adquisición sigue como servicio operativo; no se abre investigación formal de recuperación documental.

D4 · Panel. Se autoriza la preparación y adquisición dirigida de familias retenidas, con reserva previa: retenida = no evaluada y no usada para afinar M, elegir reglas ni construir el contexto de L. Primer producto: lista corta de candidatas con pregunta y dos celdas, qué emite M sin conocer el objetivo, material existente/faltante, exposición previa y cómo se preserva la reserva. Lista nominal de 6 piloto + 12 confirmatorias antes de cualquier llamada; sin ruta realista, factibilidad acotada con producto y parada definidos. Sacar NC-0161/0162 de ESPERA es consecuencia de la lista, no sustituto.

D5 · Informe. Documento del programa, iniciado ahora, breve y legible para un externo, detalles en anexo; no espera al sello de D-A. NC-0152 CERRADA citando #764.

---

## PERÍMETRO (derivado por el ejecutor, no es texto de mesa)

TOCA: `canon/informe-programa-v1_0.md` (nuevo) · `canon/informe-programa-v1_0-ANEXO.md` (nuevo) · `data/INFRAESTRUCTURA-v1_0.md` (una fila, regla de conducto) · `forense/notas/2026-09-15-GEN2-INFORME-INTERNO-F5-1-cierre.md` (nuevo) · este encargo (A.3) · la cascada de cierre (`canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_13.md`, `canon/registro-rotulos.tsv`, `forense/no-corrido.tsv`).

NO TOCA: `data/corrida0/` ni ninguna vista del registro · `milpa/` · `forense/prereg-duelo-v2/` ni `forense/prereg-caja/` · ninguna spec, medidor, sello ni corrida · `forense/firmas-pendientes.tsv` (FP-374 la mueve la lista nominal de D4, no este informe) · `tools/` · `tests/`.

## CONTADOR

Este acto **no mueve ningún contador de medición**: no sella CALC, no emite RESULT, no adopta al motor, no hace llamadas. Se dice en una línea en el módulo de auditoría, como pide la pregunta [NUEVO v2.3], sin justificarlo.

## LO QUE ESTE ACTO NO HACE

No re-adjudica `CALC-TRIADA-0002` (`SIN-GANADOR-UNICO` queda intacto) · no cierra NC-0180 ni NC-0187 (las cierra D-A al consumir B-MARCO, no un informe) · no abre F6 ni mueve FP-374 · no produce la lista nominal de D4 · no reinterpreta la tesis de D1 · no reconstruye la LECTURA ESTRATÉGICA F5 v1.1 ni el adversarial de Astra, que no están en el árbol.

---

## NO-CORRIDO / RESERVAS

(A.14. Una fila por pieza no ejecutada, parcial, distinta de lo pedido o con
reserva. Precede a `## CONSUMIDO` y nunca va después.)

| qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|
| «incorpora el sello de D-A cuando exista, sin esperarlo» | `DIFERIDO-A: ACTO D-A` | El sello **no existe** (verificado con universo: `git ls-remote --heads origin` sobre 1 remoto → 0; `ls forense/encargos/` sobre 336 archivos → 0). `§A.3` del anexo entrega la tabla de 9 celdas comunes como **derivación propia con procedencia declarada y control positivo**, no como el sello. Ninguna cifra cambia cuando D-A selle; lo que cambia es la procedencia. **Ningún contador se mueve por esta fila.** | `ACTO D-A` (`D2`). Al sellar, `§A.3` queda `VENCIDA EN ALCANCE` y se **re-sella** contra el universo nuevo, nunca editando la tabla actual (`A.10` corolario 1). Fila `NC-0218` |
| «su tabla ya está en la lectura v1.1 con procedencia» — la *LECTURA ESTRATÉGICA F5 v1.1* y el adversarial de Astra | `PARO-PREMISA` | Los dos documentos **no llegaron** y no están en el árbol (`grep -rl "LECTURA ESTRAT"` sobre `canon/` + `forense/`, **2 174 archivos examinados**, 0 coincidencias). El informe **no los reconstruye ni los cita como leídos**: rehacer un verbatim de paráfrasis sería fabricar la procedencia que el paso existe para asentar (mismo criterio que `NC-0082` y `NC-0134`). Consecuencia acotada y declarada en `§7` del informe. **Ninguna cifra del informe depende de ellos.** | mesa o dirección pega el texto verbatim y un acto de trámite lo commitea con cabecera de procedencia y `sha256` re-derivado. Fila `NC-0219` |
| «Primer producto: lista corta de candidatas…» / «Lista nominal de 6 piloto + 12 confirmatorias» (`D4`) | `FUERA-DE-PERÍMETRO` | Este acto es `D5`, no `D4`. El perímetro del encargo es «el documento nuevo, su anexo, índice de infraestructura si hace falta». El informe **documenta** la compuerta en `§A.5` (0 familias retenidas ejecutables, faltan 18/18, presupuesto no autorizado) pero **no produce la lista**. `FP-374` sigue `ABIERTA` e intocada; `NC-0161`/`NC-0162` siguen en espera | acto propio de `D4`, que mesa lance. No lo absorbe este informe ni lo sustituye |
| `NC-0180` y `NC-0187` (que `D2` declara cerradas por consumo de B-MARCO) | `FUERA-DE-PERÍMETRO` | Las cierra **D-A** al consumir B-MARCO, no un informe: un documento que no sella corridas no puede cerrar por consumo una fila cuyo cierre es exactamente ese consumo. Ambas siguen `ABIERTA`. El informe las lista en `§A.6` con esa razón explícita | `ACTO D-A` |

**Lo que SÍ se corrió y podría parecer que no:** `NC-0152` **CERRADA citando
`#764`**, que `D5` manda en la misma frase que crea este acto. Se verificó que
`#764` es el merge de `acto/gen2-f5-documental-run-2` antes de escribir el
cierre, y el alcance del cierre (cobertura residual, **no** generalización) queda
declarado en la propia fila.

---

## CONSUMIDO — PR #790

`ACTO GEN2-INFORME-INTERNO-F5-1`, ejecutado el 15/sep/2026 en NUBE (Opus,
`cloud_default`, sin corpus, sin red, sin microdato), sobre base
`origin/main = 5973f12`. PR: https://github.com/Josanoforo/Modelado-Mexicano/pull/790
(**NO FUSIONAR sin mesa** — el merge es la autorización, no un trámite del
ejecutor). Sello del acto: `ADR-515`, re-derivado por `tools/cierre_acto.py`;
renumera quien fusiona segundo.

Entregado: `canon/informe-programa-v1_0.md` + `canon/informe-programa-v1_0-ANEXO.md`
(A.10 por cifra, dos derivaciones propias con control positivo, ninguna cifra
nueva) · la fila que le faltaba al índice de infraestructura (`ADR-70(c)`) ·
`NC-0152` CERRADA citando `#764` · `NC-0218`/`NC-0219` abiertas ·
`forense/notas/2026-09-15-GEN2-INFORME-INTERNO-F5-1-cierre.md`.
**Contadores de medición movidos: cero.**
