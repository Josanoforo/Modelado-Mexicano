ENCARGO · ACTO GEN2-C2-COMPUESTO-RESERVADAS-1 · EL PISO COMPUESTO SE EMITE EN TODO CRUCE RESERVADO DONDE LOS MARGINALES LO PERMITEN: COBERTURA SIN ABRIR NINGUNA OLA, CON UN ESTADO QUE EL MOTOR NO PUEDE CONFUNDIR CON ADOPCIÓN

CABECERA (D-12) · SHA de redacción `8e455bd6`; re-deriva al abrir · ENTORNO: NUBE — cero microdato: solo marginales sellados del árbitro; NO caja · una sola sesión, rama propia; `/acto` PARA si ya está archivado en otra rama viva · COMPUERTA: `GEN2-MARCADOR-PISOS-ENLACE-1` fusionado (los dos actos editan `tools/marcador_segmento.py`; en serie, no en paralelo). Si al abrir no ha fusionado, no esperes de brazos cruzados: corre P1 y P2 completos (no tocan ese archivo) y deja P3 para cuando fusione · MODELO: Opus · FP/ADR/NC: deriva al cierre; renumera quien fusione segundo · CONTADOR: P2 sella una corrida; `cuenta_gen2 = SI` propuesto, nace `PENDIENTE-DE-MESA` salvo firma; no adopta nada y `adoptados_activos` no debe moverse — si se mueve, PARA.

FIRMA DE MESA (19/sep/2026; verbatim «Aprobado» a la propuesta del careo `CAREO-PILOTO-3-direccion-2026-09-19.md` §4, sha256/16 `796689c4dce6f43d`, que viaja adjunto; texto operativo:)

"Se emite C2 compuesto para cada par `RESERVADA` cuyos marginales compartan desenlace, universo, unidad y ola; el resto queda `NO-EMITIBLE` con causa. Estado `EMITIDA-SIN-EVALUAR`: disponible para exploración, excluida de la estimación adoptada del motor y de toda decisión automática. Una emisión no pasa a adoptada por uso: solo por piloto que la evalúe fuera de muestra o por firma de mesa con alcance declarado. Ninguna ola reservada se abre."

VERIFICACIÓN DE EXISTENCIA (A.8; dirección contra `8e455bd6`)

* (1) Gobiernan: `milpa/tramite-ola5-propuesta-v0.yaml` (marginales R con IC y n), `data/corrida0/marcador-segmento.tsv` (22 pares `RESERVADA` + 1 `CONSUMIDA-SIN-PILOTO`), `milpa/estimadores-por-segmento.yaml` + `milpa/src/estimadores_segmento.py` (lector), registro GEN2. Cubren.
* (2) `git grep -l -E "EMITIDA-SIN-EVALUAR|C2-COMPUESTO"` → 0 de 5 769 archivos; `ls data/corrida0 | grep -iE "C2|COMPUEST"` → 0 de 130 CALC. NO-ENCONTRADO. La forma de C2 está sellada dos veces y se cita, no se reinventa: `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001/spec.yaml:187` y `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001/medidor.py:149` — `expit(logit p(a) + logit p(b) − logit p)`.
* (3) El marcador nació hoy (#873): nadie pudo emitir sobre su lista antes.

PIEZAS

P1 · Dictamen de emisibilidad, par por par, antes de calcular nada (COMMIT-1). Para los 22 pares: ¿los dos ejes y el nacional comparten desenlace, universo, unidad, ola y ponderador? Se lee del yaml del árbitro, campo por campo, con cita de línea. Casos que dirección ya vio y que no se fuerzan: en ENIF, `formalidad` vive en el universo de quien trabaja — no se compone con ejes de universo completo (A-bis 4); ENUT `reparto_hogar × sexo_edad` tiene un eje que ya es compuesto; marginales con p = 0 o 1. Salida: tabla `par → EMITIBLE / NO-EMITIBLE(causa)`. No te doy cuántos saldrán emitibles. La spec congela además: la forma de C2 (citada), el nacional que se usa y de dónde sale, y la frase «el primer resultado que produzca este procedimiento es el que se reporta».

P2 · `CALC-C2-COMPUESTO-RESERVADAS-0001` (COMMIT-2). Un `RESULT` por celda emitible: punto en proporción, con `unidad_dato` y universo heredados del árbitro (delito / trámite / persona elegida 18+). Incertidumbre: no se fabrica. Los marginales de una misma ola salen de la misma muestra; su covarianza no está sellada, y el IC de los C2 adoptados se obtuvo en caja réplica por réplica (`tipo_incertidumbre: IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS`). Aquí: `tipo_incertidumbre = NO-PROPAGADA-COVARIANZA-NO-SELLADA`, sin IC. Se reporta aparte, rotulado como diagnóstico y no IC, el rango que resulta de mover cada marginal a los extremos de su IC95. Registro en la vista y asiento de replay en el mismo acto (E.7).

P3 · Marcador y lector (tras el merge de ENLACE). Estado nuevo `EMITIDA-SIN-EVALUAR` en `marcador-segmento.tsv` (token en el campo, A.16), con el cruce todavía `RESERVADA` para evaluación — las dos cosas a la vez, en columnas distintas: emitir no consume. En `estimadores_segmento.py`: `estimador_de_celda(...)` por defecto devuelve solo adoptadas; las emitidas salen únicamente con un argumento explícito (`incluir_no_evaluadas=True`) y traen el estado en la respuesta. Guardia única (D-14): test que falla si una celda `EMITIDA-SIN-EVALUAR` sale por la vía por defecto o si cuenta en `ADOPTADO_ACTIVO`. El defecto que atrapa ya ocurrió hoy en pequeño: 8 celdas adoptadas por firma que el contador no veía porque dos compuertas distintas se leían como una.

P4 · Trámite. Fila `decisiones.tsv` (objeto `emision:c2-compuesto-reservadas`); `T-RESERVA` sigue verde (ningún cruce reservado con R); dominio del marcador en `INFRAESTRUCTURA`; nota con tabla afirmación → comando y cuántas celdas ganó el motor, derivado.

PERÍMETRO Y CONCURRENCIA

`forense/prereg-caja/C2-COMPUESTO-RESERVADAS-spec-v1_0.md` + sidecar · `data/corrida0/CALC-C2-COMPUESTO-RESERVADAS-0001/` · `tools/c2_compuesto.py` (nuevo) · `tools/marcador_segmento.py`, `marcador-segmento.tsv`, `milpa/estimadores-por-segmento.yaml`, `milpa/src/estimadores_segmento.py` (solo P3) · `tests/test_c2_compuesto.py` · derivados por comando · `replay-evidencia.tsv` (asiento propio) · cascada. No toca: ningún payload de ola alguna · el yaml del árbitro · celdas-D · `tools/corrida0.py` · `tramite.yaml` · `tools/celda_d/marginales_reproduccion.py`. En paralelo: FAM-UNION-ESTIMANDO-1, RECIBO-CODEX-4 (TSV de gobierno: renumera el segundo) y Codex en ENCIG 2023 (caja, sin archivo común). «Si te encuentras escribiendo fuera de esta lista, PARA.»

LO QUE NO HACE

No abre microdato · no deriva ni mira R de ningún cruce · no adopta · no propaga IC (sucesor en caja) · no evalúa C2 · no elige el cruce del piloto 3.

SUCESORES

(Codex, caja) IC réplica por réplica de estas emisiones con el módulo guardado de una sola variable de agrupación — encargo aparte, después de este merge · PILOTO-3 como chequeo fuera de muestra de una de estas rejillas · informe v1.1.

MÓDULO DE AUDITORÍA (afirma sobre México: aplica completo)

Un C2 compuesto supone que no hay interacción entre los dos ejes en escala logit; no lo mide. Donde la interacción sea real — p. ej. edad × escolaridad en gobierno digital, brecha de acceso por cohorte — la emisión estará sesgada hacia el centro precisamente en las celdas más vulnerables (mayores con baja escolaridad, localidades chicas sin cuenta): es donde un lector aplicado más se equivocaría. La nota lo dice y la emisión lo lleva en un campo `supuesto: sin-interaccion`. Los ejes son marcadores de estructura (ingreso, formalidad, oferta institucional), no rasgos culturales. La rejilla no ve región ni condición indígena: límite declarado. Clase de evidencia: (a). Escala: proporción; unidad por fila; ningún número cruza unidad. Ninguna cifra esperada en este encargo. Peligroso leído simplista: "el motor ya estima todos los segmentos" — estima bajo un supuesto que dos pilotos no refutaron y ninguno ha probado en estos cruces.

---

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| ~~**P3 completa**~~ — **CORRIDA, no diferida** | La compuerta no había fusionado al abrir; fusionó como `PR #883` **durante** el acto, se verificó por producto, se trajo a la rama (merge `7866dcd7`) y P3 se ejecutó completa: columna `emision` (16 grupos `EMITIDA-SIN-EVALUAR` con `estado` = `RESERVADA` intacto), clave separada `emitidas_sin_evaluar` (206 celdas, ids `CRUCE-EMITIDA::…` sin solape con las 20 adoptadas), `incluir_no_evaluadas=False` por defecto, y guardia **D-14** verificada por mutación | **Ninguno: la pieza se corrió.** `adoptados_activos` delta 0 por este acto (46 sin P3, 46 con P3; el 36→46 lo produjo `#883`) | `NC-0351`, **CERRADA** en el mismo acto |
| **Verificación del careo adjunto** (`CAREO-PILOTO-3-direccion-2026-09-19.md` §4, sha256/16 `796689c4dce6f43d`) | `NO-VERIFICABLE-AQUÍ`: el archivo no está en el árbol ni llegó adjunto — `git ls-tree -r --name-only HEAD \| grep -ic "CAREO-PILOTO"` → **0 de 5 769** archivos examinados | El sha256/16 de la propuesta firmada no se contrastó. **No invalida el acto**: el texto **operativo** de la firma viaja verbatim en este encargo (A.3) y es el que se ejecutó. Lo que queda sin verificar es que el §4 del careo diga eso mismo | `NC-0349` |
| **`cuenta_gen2 = SI`** para `CALC-C2-COMPUESTO-RESERVADAS-0001` | `DECISIÓN-DE-MESA-PENDIENTE`: la spec lo **propone**, como el encargo pide; el registro aplica la regla E.1 (`ACTO GEN2-T9`, D-1) y lo baja a `NO` por el input legacy GEN1 `milpa/tramite.yaml` (`envuelto_legacy = SI`) | Las 206 emisiones no cuentan en `N_resultados_gen2_sellados`. **No se quitó el input** para forzar el contador: pinar por sha256 la procedencia de los cuatro nacionales vale más que un flag | `NC-0350` |
| **IC de las emisiones** | `DIFERIDO-A:` el sucesor en caja que el propio encargo declara (IC réplica por réplica con el módulo guardado de una sola variable de agrupación) | Las 206 celdas van **sin IC** (`NO-PROPAGADA-COVARIANZA-NO-SELLADA`). Es lo pedido, no una omisión: los marginales de una misma ola salen de la misma muestra y su covarianza no está sellada. El rango `DIAG-*` es diagnóstico y **no** un IC | El sucesor en caja ya declarado en `SUCESORES` (encargo aparte, tras este merge) |
| ~~**Corrección de `unidad_dato` en el marcador**~~ — **RESUELTA AGUAS ARRIBA** | `SUSTITUIDO-POR:GEN2-MARCADOR-PISOS-ENLACE-1` (`PR #883`), que corrigió `_unidad_dato()` para leer el `payload` del árbitro. **Qué absorbe**: la corrección entera; **qué queda huérfano**: nada | El marcador ya publica `tramite`/`delito`. El caso del test **no se borró** al desaparecer la discrepancia: fija **de quién** se hereda la unidad, y eso vale igual ahora que coinciden | Cerrado por `#883`; sin sucesor pendiente |
| **22 `RESULT` y 1 corrida de `CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001` que este PR arrastró** | `FUERA-DE-PERÍMETRO`: ese CALC fusionó por `PR #881` pero sus filas nunca se publicaron a las vistas (antes de `#889`, `corridas.tsv` de `origin/main` → **0** filas suyas; su hermano `APOYO-MONETARIO-0001` → 1). `corrida0 registro --escribe` las recogió correctamente | **Ya ocurrió**: `main` trae hoy esas 22 filas, entradas por el PR de otro acto. **No se quitaron a mano**: sacarlas exige editar un archivo `# DERIVADO — NO EDITAR`. Sin pérdida: **0** RESULT de `origin/main` ausentes en el `HEAD` (7 927 → 8 581; 632 `C2COMP` propios + 22 `ISSP` ajenos). El contenido es correcto; lo que está mal es la **procedencia** de la publicación | `NC-0358` (renumerado desde `NC-0352`: `GEN2-RECIBO-CODEX-5` tomó ese id al fusionar antes) |

## CONSUMIDO

Ejecutado por **`PR #889`** (`claude/beautiful-fermi-mct15n`) — `ACTO GEN2-C2-COMPUESTO-RESERVADAS-1`, 19/sep/2026, NUBE `cloud_default`, Opus 5, cero microdato.

Las **cuatro piezas** se corrieron. P3 empezó diferida por compuerta y terminó corrida: `GEN2-MARCADOR-PISOS-ENLACE-1` fusionó como `PR #883` durante el acto, se verificó por producto y se trajo a la rama (merge `7866dcd7`). `ADR-549` (renumerado desde 546 por fusionar segundo), `NC-0349`/`NC-0350` abiertas, `NC-0351` cerrada en el mismo acto.
