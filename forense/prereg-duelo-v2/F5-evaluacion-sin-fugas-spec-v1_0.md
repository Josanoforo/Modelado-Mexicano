# F5 · evaluación sin fugas · contrato técnico v1.0

Estado: **PROPUESTA EJECUTABLE PARA REANÁLISIS DIAGNÓSTICO**. No es una
enmienda de `F5-contrato-triada-spec-v1_1.md`, no reescribe
`CALC-TRIADA-0001/0002` y no autoriza una evaluación nueva. Una evaluación de
un M renovado requiere, antes de correr, el resolver común de
`ACTO GEN2-LINAJE-Y-ADOPCION` (17) y el snapshot elegible de
`ACTO GEN2-MOTOR-Y-HERENCIA-EXPLICITA` (18).

Acto: `GEN2-EVALUACION-SIN-FUGAS`, 11/sep/2026. Cero llamadas a modelos y
cero microdatos. El panel de 14 ya fue inspeccionado: cualquier salida que se
derive de él se rotula `REANALISIS-DIAGNOSTICO-PANEL-CONOCIDO`, nunca
pre-registro retrospectivo, holdout o evidencia independiente.

## 1. Cláusulas que se conservan

De `F5-contrato-triada-spec-v1_1.md` y `F5-completa-spec-v1_0.md` se conservan:

- tres contendientes `L_SOLO`, `L_CORPUS` y `M`; `R` es árbitro, no
  contendiente, y `B` sigue fuera de ranking/adjudicación/veto;
- mismo punto R para los tres contendientes de una celda y mismo conjunto de
  celdas para las tres comparaciones;
- `k=8`, mediana de réplicas L válidas, faltante/abstención sin imputación,
  peso igual por celda, MAE en pp y bootstrap pareado con los mismos índices;
- 10,000 réplicas, `random.Random`, semilla 42, IC95, banda de 0.5 pp y
  tolerancia de `1e-9` pp para la primera aplicación histórica;
- prohibición de ampliar, recortar, cambiar agregación o escoger ola después
  de observar errores; cobertura separada de desempeño;
- `INCONCLUSO`, `SIN-GANADOR-UNICO` y
  `NO-ADJUDICABLE-POR-CONTROL` son salidas válidas;
- transferencia es distinta de recuperación documental y las réplicas L no
  son familias independientes.

La sucesora endurece esas cláusulas: todos esos valores viven en
`spec.yaml` y el calculador sólo consume el `contrato` normalizado que entrega
`tools/corrida0.py`. No mantiene una segunda copia de parámetros.

## 2. Clausura de inputs

La spec mecánica enumera directamente, con ID, ruta, rol y SHA-256:

- 224 respuestas L indicadas por `F5-completa-plan-v1_0.json`;
- los 14 `resultados.json` R que resuelve `universo-triada-v1_4.tsv`;
- plan, universo R, snapshot M histórico y tarjetas M/R;
- este contrato, `tools/calcula_f5_sin_fugas.py` y el módulo común de linaje
  de 17; el runner registra además el hash del medidor como script.

`corrida0` resuelve esos bytes una sola vez. El medidor recibe el mismo mapa
resuelto y carga el calculador desde los bytes verificados. El núcleo no abre
rutas. Una respuesta con el mismo prompt pero bytes distintos, o un cambio de
R/snapshot/código, bloquea por hash. La identidad del prompt no sustituye la
identidad de la respuesta.

El conjunto activo de inputs es cerrado. Un JSON adicional en el árbol no
participa; un input adicional entregado al núcleo con rol desconocido se
rechaza. Los imports de código se distinguen de lecturas de datos en la prueba
de allowlist.

## 3. Identidad y correspondencia

Antes de puntuar se exige:

1. IDs únicos y no vacíos en universo, snapshot, tarjetas y resultados R;
2. igualdad exacta de los conjuntos de celdas de plan, universo, snapshot,
   tarjetas y R;
3. posiciones únicas por `(id_celda, variante, replica)`, y rutas e
   identidades de prompt únicas; longitud, `k`, variantes y versión del plan
   iguales al contrato;
4. en cada captura, identidad, celda, variante y réplica iguales al plan;
5. en cada R, `spec_id`, ruta y `RESULT-…-PUNTO` iguales a lo declarado;
6. en cada M, identidad booleana confirmada, estado, firewall, punto y tarjeta
   aptos para el propósito declarado.

Un duplicado, ID extraño, punto booleano/no finito/fuera de `[0,1]`, JSON
malformado o correspondencia ambigua es `ContratoInvalido`: no existe una
comparación identificable y no se produce un resultado parcial fingidamente
completo.

## 4. Elegibilidad por celda, fail-closed

Una celda sólo puede entrar al conjunto puntuable si, simultáneamente:

- R tiene punto válido e identidad compatible;
- L_SOLO y L_CORPUS tienen al menos una réplica válida, después de retirar
  réplicas con identidad falsa/desconocida;
- M tiene punto numérico válido, `identidad_confirmada is true`, el estado M
  permitido y exactamente `LIMPIO-DE-OBJETIVO`;
- la tarjeta M/R acredita mismo estimando para el propósito y corte temporal;
- el resolver común de 17 devuelve `APTO`, camino explicable y
  `dependencia_objetivo=NO`.

Todo valor desconocido es inelegible. La ausencia de una cadena no prueba
independencia. Copiar o renombrar el objetivo no rompe su origen; un padre o
derivado del mismo R conserva `dependencia_objetivo=SI` y queda reservado.
La clasificación de origen no se reimplementa aquí: llega por import de la
interfaz común de 17.

| Condición | Punto | Cobertura/exclusión | Efecto de control |
|---|---|---|---|
| `CONTAMINADO-POR-OBJETIVO` o dependencia directa/indirecta de R | no entra | conserva celda y camino | `NO-ADJUDICABLE-POR-CONTROL` si altera el conjunto congelado |
| identidad M falsa/desconocida | no entra | `IDENTIDAD-M-NO-CONFIRMADA` | mismo efecto |
| firewall/origen/procedencia desconocidos | no entra | motivo indeterminado | mismo efecto |
| punto M ausente, booleano, no finito o fuera de escala | no entra | `PUNTO-M-AUSENTE-O-MALFORMADO` | mismo efecto |
| réplica L ausente/abstiene | no se imputa | cuenta en su estado | celda sin mediana queda fuera |
| réplica L con identidad rota | no entra | error de identidad | comparación congelada comprometida |
| R ausente, cambiado, sin punto o con spec equivocada | no entra | se reporta/bloquea por identidad | no se adjudica |
| estimando o corte no acreditado | no entra | causa de tarjeta | no se resuelve por cercanía numérica |

Las celdas inelegibles nunca aportan a MAE ni bootstrap. Si los controles
cambian el `U3` congelado, pueden calcularse resúmenes **diagnósticos** sobre
el subconjunto apto, pero el único veredicto admisible es
`NO-ADJUDICABLE-POR-CONTROL`.

## 5. Parámetros ejecutables

`spec.yaml` declara y el calculador valida: versión de plan, 224 posiciones,
ocho réplicas, las dos variantes y su mapeo, selección por mediana, 10,000
réplicas de bootstrap, semilla/RNG, nivel de IC, delta, tolerancia, pares,
contendientes, propósito, estados aptos y `U3` congelado. Plan y contrato deben
coincidir. Cambiar cualquiera de estos valores cambia el resultado o bloquea;
ninguno se toma de constantes del calculador histórico.

## 6. Capas de incertidumbre que no se colapsan

El reporte mantiene por separado:

- error puntual contra R;
- variación entre las ocho réplicas L;
- incertidumbre de encuesta de R y la calidad de su diseño;
- dependencia entre celdas/familias y número de familias realmente nuevas.

El bootstrap histórico trata R como fijo y remuestrea celdas; no es
incertidumbre total. Conforme al benchmark web de las cuatro decisiones del
11/sep/2026, `DIN-M-01` conserva su punto R descriptivo de 15.56%, mientras
SRS y constante+folio son sensibilidades: el hogar no acredita UPM ni una
varianza oficial. Un IC estable bajo esa receta no se promueve a ground truth.
La misma separación impide que réplicas L o celdas de una sola familia se
presenten como familias independientes.

## 7. Reanálisis del panel conocido

Las tarjetas `F5-reanalisis-tarjetas-M-R-v1_0.tsv` fijan el criterio sin usar
errores para seleccionar:

- CIV no alinea unidad, recorte, códigos ni ola;
- TRA-M-02 no alinea encuesta, población ni evento;
- DIN y FAM-M-01 conservan puntos descriptivos, pero no tienen armonización
  poblacional/corte acreditada para esta transferencia;
- ENIGH y TRA-ENCIG alinean evento/unidad en distinto grado, pero el M del
  snapshot usa una ola futura respecto al objetivo.

Por tanto, el panel conocido no se renombra holdout. `CALC-TRIADA-0002`
permanece `SIN-GANADOR-UNICO`, U3=12/14 y sus cifras no se sustituyen. El
reanálisis protegido se presenta al lado y, cuando una celda no acredita cada
condición, dice indeterminado/no comparable en vez de completar por
suposición.

## 8. Productos científicos sucesores

Dos preguntas incompatibles no comparten veredicto ni conjunto:

1. `F5-documental-dirigida-spec-v1_0.md`: capacidad de recuperar evidencia
   permitida para DIN/TRA, 32 llamadas; copiar el dato explícito es
   recuperación documental, no generalización.
2. `F5-transferencia-reservada-spec-v1_0.md`: familias realmente retenidas,
   R revelado después de congelar predicciones y acceso; el panel de 14 y sus
   reestimaciones, traducciones o derivados quedan excluidos.

La exposición del LLM durante preentrenamiento no puede certificarse desde el
repo. El control acredita únicamente el contexto experimental, prompts,
fuentes y respuestas observables y fijados.

## 9. Criterio de activación

Este contrato puede cerrarse con código, pruebas y reanálisis. Una evaluación
nueva sólo se habilita cuando:

- 17 está integrado y su API de linaje es el import real del medidor;
- existe un snapshot nuevo de 18 con tarjeta M/R por celda y cadena apta;
- mesa adopta una de las specs científicas y autoriza su coste;
- inputs completos pasan preflight y el conjunto se congela antes de R/error.

No se cambia el competidor al modelo que ejecuta Codex ni se interpreta un
plan Pro como permiso de API.
