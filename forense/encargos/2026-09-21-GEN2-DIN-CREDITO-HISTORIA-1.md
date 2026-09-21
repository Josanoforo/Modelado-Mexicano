# ENCARGO · ACTO GEN2-DIN-CREDITO-HISTORIA-1 · CRÉDITO GANA HISTORIA: SE SABE QUÉ OLAS DE ENIF SON COMPARABLES, SE MIDEN SUS PISOS, K8 SE TRIANGULA FUERA DE ENIF Y LA BANCARIA QUEDA DESCRITA CON SU FRONTERA — SIN TOCAR ENIF 2024

> ENTORNO: **CAJA** (corpus montado: abre microdato de ENIF 2012/2015/2018, ENSAFI 2023 y ENFIH 2019). Si el hook no dice CAJA, PARA en una línea. NO es NUBE.

CABECERA · SHA de redacción `55c8d57c`; re-deriva al abrir · una sola sesión, rama `acto/gen2-din-credito-historia-1` · MODELO: Opus (mide) · MODO: **ABIERTO** hasta cada COMMIT-1; desde ahí el procedimiento de esa pieza es RÍGIDO · LOTE (D-11): cuatro piezas, un PR; una que PARA no tumba las otras · CONTADOR: sella hasta cuatro corridas; `cuenta_gen2 = SI` (§2); `adoptados_activos` no se mueve · FP/ADR/NC: raíz de acto.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación** (27 MB por duplicaciones; TUBERÍA la repara). Si `canon/L0/` ya existe al cerrar, tu anotación va ahí.

## 1 · OBJETIVO
El dominio crédito tiene un solo piso (ENIF 2021, `#943`). Con una sola ola de historia no hay forma de saber si una interacción se repite: el piloto 3 mostró que la interacción cruda es peor que el piso (10.6 pp) y la encogida por estabilidad es la primera señal de valor añadido (1.9 contra 3.4). Para que crédito pueda tener su lote prospectivo sobre ENIF 2024 —que está RESERVADA— necesita primero su historia. Y mesa mandó el orden: **predecir antes de describir**; este acto es el paso (3) de ese orden.
«Hecho» significa: la tabla de comparabilidad de crédito deja de decir `NO-VERIFICABLE-AQUÍ` para 2012 y 2015 · pisos sellados de crédito en cada ola histórica que el texto permita, **conmensurables con `#943`** · K8 medido en ENSAFI 2023 y ENFIH 2019 con su comparabilidad declarada · el descriptivo de K2-bancaria, rotulado · una nota: cuántas olas de historia tiene cada conducta K1–K7.

## 2 · FIRMAS DE MESA — verbatim
FP-404 (21/sep, FIRMADA; `[LEÍDO: forense/firmas-pendientes.tsv]`): «(1) K8 'destino del ultimo credito' sale de la serie ENIF: no tiene instrumento en 2021 ni 2024 y en 2012-2018 solo 2018 esta verificado por texto. Opcion (i): se triangula en ENSAFI 2023 / ENFIH 2019 en acto propio; no se construye serie 2012-2018. (2) K2 familia bancaria: opcion (iii) para la serie -no se compara 2021<->2024, es CAMBIO-DE-INSTRUMENTO- y (i) rotulado para el descriptivo. La cifra del corpus 'bancaria +5.2 pp desde 2021' no se cita sin esa frontera.»
Alcance (20/sep) `[REPORTADO por PRODUCTO-DINERO]`: «Confirmo el alcance v0 y en paralelo medimos crédito.» Reserva (20/sep) `[REPORTADO; dirección buscó "RESERVADA desde hoy" en decisiones.tsv y firmas-pendientes.tsv y solo halló la de ENVIPE 2026]`: «La sección de crédito de ENIF 2024 queda RESERVADA desde hoy, con el hueco declarado: el par "crédito por app" (n=200) está visto y consumido; no se relanza sobre él.» → **P0 la busca por objeto y, si no está, la asienta con este texto** (A.12). D-22 ampliada (21/sep): «Congelado exige: `preflight` VERDE sobre el commit final con main fusionado; que `_valida_outputs` acepte la salida de cada rama terminal del procedimiento, incluida la de celda rara, sobre sintético y sobre oro; que todo id que el código pueda emitir nulo por lectura estática esté declarado; y ningún input con hash sobre un archivo vivo.»
**Propuesta de dirección — el lanzamiento es el sello:** «Las corridas de GEN2-DIN-CREDITO-HISTORIA-1 cuentan (`cuenta_gen2 = SI`): miden desde microdato con cadena completa. Una ola cuyo texto sea CAMBIO-MENOR entra a la serie con su matiz escrito en cada RESULT; una que sea CAMBIO-DE-INSTRUMENTO no entra.»

## 3 · LO QUE DIRECCIÓN SABE (contra `55c8d57c`, sin corpus)
- `[EJECUTADO sobre data/credito-comparabilidad-texto-v1_0.tsv]` ola 2018: K1–K6 `CAMBIO-MENOR` · K7 `NO-ESTIMABLE` · K8 `CAMBIO-DE-INSTRUMENTO`. Olas 2012 y 2015: las ocho `NO-VERIFICABLE-AQUÍ` — **porque faltaban los cuestionarios, que entraron hoy** (`#960`): `enif_2012_cuestionario_pdf`, `enif_2015_cuestionario_pdf`, más `enif_2012_fd_enif2012` y `enif_2015_enif_2015_fd` `[EJECUTADO sobre el manifiesto]`. Los dos PDF se registraron desde nube: **tráelos a la caja por id** (`tests/manifiesto.py --descarga --id`), que verifica el sha registrado.
- `[EXISTE]` el molde: `CALC-DIN-CREDITO-PISOS-ENIF2021-0001` (2 939 RESULT, sellado) y `forense/prereg-caja/DIN-CREDITO-PISOS-ENIF2021-spec-v1_0.md`. `[REPORTADO]` usa `FAC_ELE`, `EST_DIS × UPM_DIS`, 10 000 remuestras `PCG64(42)`, un solo plan de réplicas, rejilla leída de la tabla de identidad GEN2. **Mismo marco, para que todo nazca conmensurable.** Nemónicos y ponderadores cambian entre olas: se resuelven por texto de pregunta (A.15).
- `[EJECUTADO sobre el manifiesto]` `ensafi2023_bd_csv_zip`, `ensafi2023_cuestionario_pdf`, `ensafi2023_fd_xlsx_zip`, `enfih2019_bd_csv_zip`, `enfih2019_fd_xlsx`. `[LEÍDO: nota de #960]` no existe ola nueva de ENSAFI ni de ENFIH.
- `[REPORTADO]` K4 mide «nunca ha tenido», no «no tiene hoy»; los ex-usuarios caen en otra pregunta. K3: empeño y gota a gota **no se colapsan**. Unidad por fila: persona, salvo K7–K8 (producto).

## 4 · YA HECHO
Por objeto («crédito», «K8», «bancaria», «ENIF2018») en encargos, `prereg-caja`, `data/corrida0/` y ramas remotas: comparabilidad v1.0 (`#932`), piso 2021 (`#943`); nada para 2012/2015/2018, ni K8 fuera de ENIF, ni el descriptivo. **Repítela tú.**

## 5 · PIEZAS
**P0 · Firma y cuestionarios.** La reserva de §2, si falta. Los dos PDF, por id.
**P1 · Comparabilidad de crédito en 2012 y 2015.** Las 16 filas que hoy dicen `NO-VERIFICABLE-AQUÍ`, con texto literal, opciones, filtro y flujo, unidad y población base; sucesor `…-v1_1.tsv` (el v1.0 no se edita); el test existente se extiende.
**P2 · Pisos de crédito por ola histórica.** Una corrida por ola que tenga al menos una conducta utilizable. Por pieza: COMMIT-1 (spec con sidecar + `spec.yaml` + medidor; «congelado» es D-22 ampliada, con su oro: el mismo punto de entrada reproduce `#943` sobre ENIF 2021) → COMMIT-2 (`corrida0 run`, sello, vista y replay). Todo marginal de crédito se publica **con K4(b) y K5 al lado**: oferta antes que preferencia.
**P3 · K8 en ENSAFI 2023 y ENFIH 2019.** Primero por texto: ¿preguntan lo mismo, a la misma unidad, con el mismo periodo de referencia? Si no son comparables entre sí, se miden por separado y **no se presenta como serie**. Mismos dos commits.
**P4 · Descriptivo de K2-bancaria.** Rotulado con su frontera (FP-404): niveles por ola, sin diferencia 2021↔2024, y la frase de por qué.

## 6 · LATITUD
Decides tú: un CALC por ola o por familia · qué reutilizas de `#943` · orden. Replantea y sigue ante main movido o ids renombrados. `NO-CONSTRUIBLE` cita el texto buscado y las secciones del descriptor recorridas. Pregunta a mesa, siguiendo con lo demás: si 2012 o 2015 resultan comparables solo bajo un recorte de universo que 2021 no tiene.

## 7 · PAROS — lista cerrada
a) abrir cualquier variable de **ENIF 2024**, de crédito o no · b) abrir `envipe2026*` · c) colapsar empeño con gota a gota, o K4(a) con K4(b) · d) presentar como serie dos olas con `CAMBIO-DE-INSTRUMENTO` · e) cambiar un procedimiento tras su COMMIT-1 · f) `corrida0 run` no sella → no se parcha · g) adoptar · h) entorno equivocado.

## 8 · COMPUERTAS
«COMMIT-1 de la pieza en `origin` con su oro en verde» protege: **abrir dato**.

## 9 · PERÍMETRO
Propio: la tabla v1.1 y su test · CALC nuevos y sus specs · filas propias de vista y replay · la fila de firma de P0 · nota · cascada. Ajeno: `#943` y todo sello · celdas-D · `milpa/` · `tools/corrida0.py`. Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · NO HACE · SUCESORES · AUDITORÍA · CIERRE
No congela ninguna predicción de 2024 · no abre 2024. Sucesor: lote prospectivo de crédito sobre ENIF 2024, con el módulo genérico de cruces. Auditoría (afirma sobre México): no tener crédito formal no es «preferir» el informal — puede ser rechazo, requisitos o buró; por eso K4(b) y K5 viajan siempre al lado; ENIF es adulto elegido: sub-representa a quien no decide el dinero del hogar; ENSAFI y ENFIH tienen otro universo y otra unidad, y no se promedian con ENIF; toda la evidencia es clase (a). `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

- **qué:** P4 · Descriptivo de K2-bancaria: niveles por ola (`corrida0 run` de `CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001`, congelado con preflight VERDE) · **por qué:** DECISIÓN-DE-MESA-PENDIENTE: sería la quinta corrida y el CONTADOR del encargo «sella hasta cuatro corridas»; la frontera FP-404 (2) sí queda escrita · **impacto:** los niveles 2012-2021 de tarjeta de crédito bancaria no están sellados; ningún contador GEN2 se mueve por esto · **sucesor:** `FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-02` (`NC-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-01`).
- **qué:** P3 · K8 medido en ENSAFI 2023 · **por qué:** NO-VERIFICABLE-AQUÍ: por texto, ENSAFI 2023 no tiene instrumento de destino de crédito (`data/credito-k8-triangulacion-texto-v1_0.tsv`, EXISTE-NO-SATISFACE) · **impacto:** la triangulación de K8 queda con una sola fuente (ENFIH 2019, rotulada, sin serie) · **sucesor:** FP-404 ejecutada en su alcance verificable (`NC-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-02`, CERRADA por este acto).
- **qué:** P2 · pisos «conmensurables con #943»: NACIONAL y celdas fuera de edad · **por qué:** DECISIÓN-DE-MESA-PENDIENTE: exige recortar 2021 a 18-70 y #943 es sellado; las celdas 18-29/30-44/45-59 ya son conmensurables · **impacto:** la historia por eje de K1-K6 sólo se lee hoy en tres celdas de edad · **sucesor:** `FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-01` (`NC-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-03`).

## CONSUMIDO

PR #975 (`acto/gen2-din-credito-historia-1`, `ADR-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-01`), 21/sep/2026. Ejecutado íntegro salvo las reservas de arriba. Nota: `forense/notas/2026-09-21-GEN2-DIN-CREDITO-HISTORIA-1-cierre.md`.
