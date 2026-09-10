# `CALC-DUELO-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA
`forense/prereg-duelo-v2/F5-duelo-contemporaneo-spec-v1_0.md`
(**COMMIT-1 de `ACTO GEN2-F5-RECAPTURA-L`**,
sha256 declarado ahí para el propio documento: ver §1-§9 del archivo).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-F5-DUELO-CALC`, 10/sep/2026, NUBE, cero microdato/cero
red — consume capturas ya selladas y los seis `CALC-R-CIV-M-*` GEN2, ambos
ya en `origin/main` (compuerta: `PR #669`, `ACTO GEN2-F5-RECAPTURA-L`,
fusionado).

---

## Qué mide (la pregunta primaria, TRANSFERENCIA)

Sobre las **6 celdas CIV-M con árbitro `R` calculado**
(`CIV-M-01/02/04/10/12/13`, ENVIPE 2012–2024, `denuncia_con_miedo_o_
desconfianza`): compara, POR CELDA, dos brazos de `L` —`L-solo` (sin
corpus) y `L+corpus` (con el paquete-corpus F5, corte temporal por
celda)— contra el mismo árbitro `R`, en unidades `z = (punto−R)/EE(R)`.
La cantidad pareada primaria es `dif_abs_pareada = |z_LCORPUS| − |z_LSOLO|`
(negativo ⇒ el corpus acerca la estimación a `R`; positivo ⇒ la aleja),
bootstrapeada (`seed=42`, `replicas=10000`, `nivel_ic=0.95`) sobre el
universo pareado de hasta 6 celdas, con la escala de adjudicación
EXHAUSTIVA B-bis (`banda δ=0.5`) que la spec sellada §5 fija.

`agregado(brazo)` = **mediana** de las réplicas con `valor_extraido`
EXTRAIBLE de las 8 de esa (celda, variante) — reutilizando, sin editar,
`pipeline-L-adv1-m2.py::agregar_continua`. `valor_extraido` sale de aplicar
el único extractor de prosa libre que existe en el repo,
`tools/extrae_l_v1_1.py` (sellado por `MAESTRA33-E21` contra las 176
capturas v1.1), a las 96 capturas reales (`__v1_3.json`) de estas 6 celdas.

## El hallazgo que este acto mide y declara ANTES de adjudicar

**Ninguna de las 96 capturas trae el encabezado Markdown con "estimaci"**
que `extrae_l_v1_1.py` busca — 0/96, medido, no supuesto — así que el 100%
de las extracciones cae a su *fallback* de "buscar el primer número en todo
el documento". De las 96, 59 (61%) quedan `EXTRAIBLE` por ese camino.
Verificado a mano contra tres de esas 59 (citadas en `RESULT-DUELO-
DIAGNOSTICO-EJEMPLO-*` con su sha256): en los tres casos el modelo **rechaza
explícitamente** dar una estimación del reactivo pedido y el número que el
extractor captura es una cifra de **contexto** que el propio texto marca
como "no es una estimación puntual" (la "cifra negra" ~90–94% de la ENVIPE,
citada como conocimiento general, no como respuesta). El extractor v1.1 fue
calibrado contra un corpus de captura DISTINTO (v1.1/v1.2, con encabezados
"## Estimación"); aplicado sin validación a este nuevo formato de prosa
libre real-corpus, produce contaminación medida, no hipotética.

**Consecuencia, declarada, no improvisada:** este medidor SÍ calcula el
número que el procedimiento sellado produciría con este extractor
(`RESULT-DUELO-PAREADA-VEREDICTO-BANDA-BRUTO`, transparencia — "el primer
resultado que produzca este procedimiento es el que se reporta") pero **no
lo adopta**. `RESULT-DUELO-PAREADA-VEREDICTO-ADOPTADO = INCONCLUSO`, razón
`INSTRUMENTO-DE-EXTRACCION-NO-VALIDADO-PARA-FORMATO-REAL-DE-CORPUS` — una
ENMIENDA fechada a la escala de la spec sellada §5 (que no preveía esta
clase de hueco: la escala asume un `agregado(brazo)` confiable, no que el
único extractor disponible fuera calibrado para un formato de texto
distinto al que las capturas reales trajeron). No se inventa un extractor
nuevo en este acto — sería exactamente el tipo de regla improvisada tras
ver resultados que el propio procedimiento prohíbe (§5: "prohibido ampliar
n... o elegir variantes de agregación después de ver resultados" aplica en
espíritu a inventar un extractor sobre la marcha). Se declara el hueco y se
deja como sucesor.

## Secundaria (b) USO DOCUMENTAL — descriptiva, acotada

Sobre las 48 capturas `L+corpus` de las mismas 6 celdas: el campo
estructurado `fuente_citada` está `null` en el 100% (0/48) — el runner nunca
lo puebla por parseo. Lectura cualitativa (en la nota de cierre, no aquí):
el modelo sí describe correctamente qué encuestas/temas contiene o no
contiene el paquete-corpus entregado, aun cuando rechaza estimar — engagement
real con el corpus, sin que eso se traduzca en el campo estructurado ni en
una cifra adoptable.

## Cobertura

`RESULT-DUELO-COBERTURA-*` cita, sin recalcular, el embudo ya sellado de
`ACTO GEN2-F5-RECAPTURA-L` (`manifiesto-capturas-P3-v1_0.json`): 224/224 OK,
0 rechazadas, sobre las 14 celdas completas del marco.

## Perímetro de este medidor

Lee: las 96 capturas de las 6 celdas CIV-M (`__v1_3.json`), los 6
`resultados.json` de `CALC-R-CIV-M-*`, los 6 `corridas-M/M-*.json`
correspondientes, `tools/extrae_l_v1_1.py`, `pipeline-L-adv1-m2.py`,
`scoring-adv1-m3.py` (importados por ruta, sin editar), y el manifiesto de
capturas sellado. No abre `data/raw`, no re-corre `L`, no toca `corridas-R/`
más allá de leer sus `resultados.json` ya escritos.

## Dependencias materiales

Ninguna — todo el cómputo usa `statistics`/`math`/`random` de la biblioteca
estándar (los mismos que `pipeline-L-adv1-m2.py` y `scoring-adv1-m3.py` ya
usan).
