# ENCARGO · ACTO GEN2-F5-EXTRACTOR-L-v1

Recibido en mesa 10/sep/2026 (despacho 1/5 de la batería que la firma de mesa
de ese día pidió). Texto verbatim del lanzamiento:

> ENCARGO 1/5 · ACTO GEN2-F5-EXTRACTOR-L-v1
>
> EL TERMÓMETRO ANTES DEL PARTIDO
>
> OBJETIVO: construir y sellar un extractor determinista válido para las
> capturas `__v1_3.json`, de manera que L_SOLO y L_CORPUS puedan convertirse
> en puntos numéricos sin confundir cifras de contexto con la estimación
> emitida por el modelo.
>
> CABECERA: NUBE, Opus. Cero microdato. Cero nuevas llamadas a Claude. Consume
> únicamente capturas ya selladas, sus hashes, specs y herramientas del repo.
>
> COMPUERTA: `ACTO GEN2-F5-DUELO-CALC`, PR #674, fusionado. Verificar por
> producto que existen las 224 capturas selladas del marco v1.3 y que
> `NC-0142` sigue abierto por instrumento de extracción, no por ausencia de
> capturas.
>
> FIRMA DE MESA: se autoriza construir un extractor sucesor para formato
> v1.3. Esta firma NO autoriza recapturar, seleccionar respuestas favorables
> ni modificar capturas existentes. Una respuesta ambigua puede quedar
> `NO-EXTRAIBLE`; inventar una cifra para completar cobertura está prohibido.
>
> A.8 · VERIFICACIÓN DE EXISTENCIA. Re-derivar contra `origin/main` al
> arrancar: (1) `forense/prereg-duelo-v2/F5-duelo-contemporaneo-spec-v1_0.md`.
> (2) `forense/prereg-duelo-v2/L-spec-v1_3.json` y sidecar. (3)
> `corridas-L/*__v1_3.json`: 14 celdas × 2 brazos × 8 réplicas. (4) Manifiesto
> sellado de capturas de F5-RECAPTURA-L. (5) `tools/extrae_l_v1_1.py`,
> conservado como histórico. (6) `NC-0142` y cierre de PR #674. (7) Los tres
> ejemplos ya documentados donde el fallback del extractor viejo tomó una
> cifra de contexto. Si cualquiera de estas premisas no se reproduce, A.13 y
> PARO antes de diseñar una regla nueva.
>
> P1 · CONTRATO DEL EXTRACTOR, COMMIT-1. Nace un sucesor, nunca una edición
> silenciosa de `extrae_l_v1_1.py`. Producto sugerido: `tools/extrae_l_v1_3.py`
> y su nota/spec de comportamiento en `forense/prereg-duelo-v2/`. El
> extractor devuelve por captura, como mínimo: `id_celda · variante ·
> replica · estado · valor_extraido · evidencia_textual · regla_de_extraccion
> · razon_no_extraible`. Reglas obligatorias: prohibido el fallback «primer
> número del documento»; una cifra sólo es válida si está ligada por
> estructura o texto a la respuesta/estimación solicitada; porcentajes y
> probabilidades se normalizan únicamente mediante reglas congeladas y
> explícitas; un intervalo, año, tamaño de muestra, cifra negra, estadística
> de contexto u otra cifra mencionada no puede convertirse en estimación sólo
> por ser el primer número legible; si dos candidatos sobreviven y el formato
> no permite decidir mecánicamente cuál es la respuesta, `AMBIGUA` o
> `NO-EXTRAIBLE`; la evidencia textual usada para adjudicar la extracción
> queda guardada para inspección humana; el extractor verifica además
> `id_celda`, `variante` e índice de réplica dentro del JSON contra el
> manifiesto — identidad incorrecta es fallo material, no extracción; nada de
> la regla depende del valor de R, M ni del error resultante. Antes de
> aplicarlo al universo completo, congelar los casos de prueba que
> representan las formas de salida observadas. Los tres falsos positivos ya
> medidos por #674 son controles negativos obligatorios.
>
> P2 · VALIDACIÓN Y EJECUCIÓN, COMMIT-2. Aplicar el extractor a las 224
> capturas sin editar P1. Emitir: total capturas; EXTRAIBLE; NO-EXTRAIBLE;
> AMBIGUA; error de identidad; cobertura por brazo; cobertura por celda;
> cobertura por réplica; distribución de regla de extracción empleada.
> Control positivo: ejemplos claros producen el valor respaldado por su
> evidencia. Control negativo: los tres ejemplos contaminados de #674 no
> pueden volver a devolver la cifra contextual incorrecta. Control de
> independencia: el código de extracción debe poder ejecutarse sin abrir
> ningún `CALC-R-*`, `corridas-R/`, resultado del duelo ni archivo de error
> contra R.
>
> P3 · PRODUCTO PARA EL DUELO. Sellar un manifiesto de extracción por las 224
> capturas, con hash de cada input y del extractor. No calcular aún quién
> gana. Cerrar `NC-0142` sólo en su componente instrumental si el instrumento
> queda validado. La adjudicación continúa perteneciendo al ENCARGO 5/5.
>
> PERÍMETRO: `tools/extrae_l_v1_3.py`, pruebas dirigidas del extractor,
> `forense/prereg-duelo-v2/`, manifiesto de extracción, notas, `no-corrido`,
> 0-bis y cascada.
>
> NO TOCA: capturas, `milpa/`, motor, árbitros R, `CALC-DUELO-0001`,
> resultados históricos, paquete de corpus.
>
> CONTADOR: cero. Construir un instrumento no es una medición de México.
>
> CIERRE: nota con resultado del instrumento primero; cascada; `##
> NO-CORRIDO / RESERVAS`; `## CONSUMIDO` con PR.
>
> SUCESOR: ACTO GEN2-F5-TRIADA-CALC, cuando también existan el marco R y el
> snapshot M exigidos abajo.

## VERIFICACIÓN DE EXISTENCIA (A.8, contestada por el ejecutor, 10/sep/2026, contra `eab46ed`)

**(1) ESTRUCTURA.** Gobiernan este dominio: `forense/prereg-duelo-v2/
F5-duelo-contemporaneo-spec-v1_0.md` (la spec congelada del duelo, §2 fija la
pregunta primaria TRANSFERENCIA que este instrumento sirve) ·
`forense/prereg-duelo-v2/L-spec-v1_3.json` + `.sha256` (las 14 celdas) ·
`forense/prereg-duelo-v2/corridas-L/*__v1_3.json` (las capturas reales) ·
`forense/prereg-duelo-v2/manifiesto-capturas-P3-v1_0.json` (manifiesto sellado
de `F5-RECAPTURA-L`) · `tools/extrae_l_v1_1.py` (extractor histórico,
conservado sin editar) · `forense/no-corrido.tsv` (fila `NC-0142`) · este
encargo (nuevo, nace aquí). Este acto ESCRIBE: `tools/extrae_l_v1_3.py`, su
spec/nota en `forense/prereg-duelo-v2/`, pruebas dirigidas, un manifiesto de
extracción, `forense/no-corrido.tsv` (cierre parcial de `NC-0142`), cascada.
Deliberadamente NO escribe ni edita: las capturas mismas, `CALC-DUELO-0001/`,
`CALC-R-*`, `corridas-R/`, `milpa/`, el paquete-corpus.

**(2) CONTENIDO**, comando y salida cruda:

- `git log -1 --format='%H %ci'` → `eab46ed24a60ff94835831698648ca8df1c07da7
  2026-09-09 21:13:26 -0600` (merge de `PR #674`, `ACTO GEN2-F5-DUELO-CALC`).
  `git merge-base HEAD origin/main` == `HEAD` de la rama de trabajo: al día.
- `find forense/prereg-duelo-v2/corridas-L -iname '*__v1_3.json' | wc -l` →
  `224` (EXISTE-SATISFACE: 14 celdas × 2 variantes × 8 réplicas, verificado
  por conteo de archivo, no supuesto).
- `grep -n 'NC-0142' forense/no-corrido.tsv` → fila `NC-0142` con estado
  `ABIERTA`, causa `NO-VERIFICABLE-AQUÍ`, razón textual: *"el único extractor
  de valor_extraido... no está validado contra el formato real-corpus de las
  96 capturas v1_3... verificado a mano (3 ejemplos con hash...) el número
  capturado es una cifra de contexto..."* — abierta por instrumento, no por
  ausencia de capturas (EXISTE-SATISFACE la premisa del encargo).
- `forense/notas/2026-09-10-GEN2-F5-DUELO-CALC-veredicto.md` §1 EXISTE y trae
  los tres ejemplos con hash de archivo verificados en esta sesión:
  `CIV-M-12__L-solo__01` (`sha256(archivo)=4673f1c2c6b4…`, id_celda/variante/
  índice confirmados dentro del JSON), `CIV-M-13__L+corpus__04`
  (`sha256=5cec84f4bc4a…`, confirmado) y `CIV-M-01__L+corpus__02`
  (`sha256=7ec645203eb0…`, confirmado, no citado por hash en la nota pero
  identificado ahí por nombre de archivo). Los tres leídos íntegros en esta
  sesión: los tres cierran con un rechazo explícito de estimación puntual y,
  como contexto declarado, una "cifra negra" ENVIPE (90–94%) que el propio
  texto del modelo marca explícitamente como NO la respuesta pedida.
  EXISTE-SATISFACE.
- `tools/extrae_l_v1_1.py` EXISTE, leído íntegro: busca un encabezado Markdown
  que contenga "estimaci" y, si no lo encuentra, cae al documento completo;
  extrae por *posición* (primer candidato numérico), no por relación
  semántica con la pregunta — el defecto que este acto sucede.
  EXISTE-SATISFACE (histórico, no se edita).
- `PR #674` (`ACTO GEN2-F5-DUELO-CALC`) CERRADO/fusionado — confirmado por
  `git log` (merge commit `eab46ed`) y por el propio encargo archivado
  (`forense/encargos/2026-09-10-GEN2-F5-DUELO-CALC.md`, `## CONSUMIDO`).

**(3) COBERTURA RETROACTIVA.** `L-spec-v1_3.json` y las 224 capturas nacieron
en `ACTO GEN2-F5-RECAPTURA-L` (`PR #669`, 9/sep/2026) — anteriores a este
encargo, dentro de ventana. `tools/extrae_l_v1_1.py` nació en `MAESTRA33-E21`
(anterior, sellado contra formato v1.1/v1.2 con encabezados) — nunca pasó por
el formato real de `v1_3` (prosa sin encabezados), consistente con lo medido
por `#674`. `NC-0142` nació en el cierre de `#674` (10/sep/2026, mismo día);
no hay trabajo posterior a esa fecha que la tabla gobernante debiera cubrir y
no cubra.

Ninguna de las tres partes revela que el trabajo ya esté hecho — el hueco es
real y es exactamente el que el encargo describe.

## Estado

`VIVO`
