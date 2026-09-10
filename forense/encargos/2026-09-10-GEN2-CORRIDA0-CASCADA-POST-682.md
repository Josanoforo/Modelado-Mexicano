# ENCARGO · GEN2-CORRIDA0-CASCADA-POST-682

## OBJETIVO

Cerrar `NC-0145` y publicar correctamente las vistas derivadas de `corrida0`, sin degradar silenciosamente corridas históricas y sin recalcular, re-sellar o modificar resultados sustantivos salvo que la evidencia obligue a un acto posterior.

Partimos de `main` DESPUÉS de PR #682.

PR #682 ya resolvió `NC-0140` restaurando la identidad histórica de `CALC-ENCIG-0001`.

El bloqueo restante está acotado a estas tres corridas:

* `CALC-C0D-MARCADOR`
* `CALC-C0D-MARCADOR-v2`
* `CALC-M-marco-M-sorteado-v1_3`

y posteriormente a publicar `CALC-TRIADA-0001` en las vistas derivadas.

## PRINCIPIO DE DECISIÓN YA FIJADO POR MESA

Un `CALC` sellado no debe perder identidad histórica simplemente porque uno de sus inputs fue editado posteriormente in situ.

Para cada una de las tres corridas:

1. identifica exactamente qué input sellado difiere hoy;
2. recupera el hash esperado desde la propia spec/sello;
3. encuentra mediante Git el blob histórico que producía ese hash;
4. determina cuándo y por qué cambió;
5. clasifica el caso:

### A · MUTACIÓN HISTÓRICA IN SITU

Si el input citado por la corrida fue editado después del sello y el cambio posterior podía/debía vivir como versión sucesora:

* preservar/restaurar byte por byte el input histórico bajo la identidad que el CALC selló;
* mover o conservar el contenido posterior en una versión sucesora cuando sea necesario;
* actualizar únicamente referencias posteriores que inequívocamente deban apuntar a la sucesora;
* NO recalcular el CALC;
* NO re-sellar el CALC;
* verificar que vuelva a `REPRODUCE / CONTEXTO=IDENTICO` o al estado histórico correcto.

Éste es el precedente de PR #682.

### B · TRANSICIÓN REAL Y LEGÍTIMA

Si el input no fue indebidamente mutado, sino que la corrida realmente debe adquirir el nuevo estado:

* demostrarlo con historia Git + hashes + semántica del input;
* registrar explícitamente la transición;
* no disfrazarla como reparación de identidad;
* no ampliar el acto a ninguna otra corrida.

Si para aceptar esa transición hace falta una decisión epistemológica de mesa, PARA esa corrida y déjala como `DECISION-DE-MESA-PENDIENTE`. No inventes la decisión.

## P1 · DIAGNÓSTICO DE LAS TRES

Reproduce el `registro --verifica` que originó `NC-0145`.

Para cada corrida entrega una tabla mínima:

| CALC | estado publicado | estado proyectado | input discrepante | hash sellado | hash actual | commit que lo cambió | clasificación A/B | acción |
| ---- | ---------------- | ----------------- | ----------------- | ------------ | ----------- | -------------------- | ----------------- | ------ |

Debes explicar particularmente:

* por qué `CALC-C0D-MARCADOR` y `CALC-C0D-MARCADOR-v2` pasan de `REPRODUCE/IDENTICO` a `NO-REPRODUCE/CONTEXTO-DISTINTO` por `IN-MANIFIESTO`;
* por qué `CALC-M-marco-M-sorteado-v1_3` pasa de `REPLICA-RESULTADO` a `NO-REPRODUCE`, incluyendo `IN-EMITE-M` e `IN-TRAMITE`.

No audites el resto de `corrida0`.

## P2 · REPARACIÓN / ADJUDICACIÓN

Aplica únicamente las reparaciones mecánicamente justificadas por P1.

Restricciones:

* cero cambio en valores `RESULT`;
* cero recalibración de `M`;
* cero cambios sustantivos en `milpa/` salvo que fueran estrictamente necesarios para restaurar un blob histórico y exista versión sucesora correcta;
* cero `--force`;
* cero re-sellado para hacer desaparecer una discrepancia;
* cero reparación incidental de otras NC;
* no tocar el resultado ni la spec sellada de `CALC-TRIADA-0001`.

Si una de las tres requiere mesa, no bloquees las demás: deja evidencia y `NO-CORRIDO / RESERVAS` precisa.

## P3 · COMPUERTA

Después de P2 corre nuevamente `registro --verifica`.

GO únicamente si las tres transiciones están:

* restauradas a su estado históricamente correcto, o
* explícitamente adjudicadas con evidencia suficiente.

No permitas ninguna degradación adicional fuera de estas tres.

Compara el universo completo antes/después y reporta cualquier cuarta corrida que cambie. Si aparece una cuarta, PARA la escritura.

## P4 · PUBLICAR VISTAS

Si P3 da GO, publica las vistas derivadas incluyendo:

* las tres corridas expresamente tratadas;
* `CALC-TRIADA-0001`.

Usa la sintaxis vigente de `tools/corrida0.py`; consulta `--help` si `--lote` requiere forma específica.

Objetivo esperado después de incorporar TRIADA:

* `139` corridas derivadas;
* `2889 RESULT`.

No tomes esos números como autoridad si la derivación real contradice alguno: en ese caso reporta la diferencia antes de modificar cualquier contador canónico.

Las vistas objetivo son exclusivamente las derivadas que el propio registrador produzca. No edites TSV derivados a mano.

## P5 · NC-0145

Si P4 termina correctamente:

* cerrar `NC-0145`;
* citar este acto como `cerrado_por`;
* dejar explícito qué ocurrió con cada una de las tres corridas;
* registrar que `CALC-TRIADA-0001` ya fue incorporado a las vistas.

Si P4 no puede ejecutarse por una decisión genuina de mesa, mantener `NC-0145 ABIERTA` y especificar exactamente una decisión pendiente, no una investigación genérica.

## P6 · VERIFICACIÓN

Verifica al menos:

* `CALC-ENCIG-0001` continúa `REPRODUCE / CONTEXTO=IDENTICO`;
* `CALC-TRIADA-0001` continúa `REPRODUCE / CONTEXTO=IDENTICO`;
* las tres corridas objeto tienen el estado adjudicado en P1/P2;
* las vistas contienen TRIADA si P4 dio GO;
* ningún `RESULT` sellado cambió.

Ejecuta `tests/check.py --baseline` de forma que NO incorpore al PR los efectos secundarios conocidos de `NC-0141` sobre `data/corrida0/demanda-*.tsv`. Usa worktree temporal o restaura explícitamente esos archivos después de la prueba.

Baseline heredado no es motivo para ampliar el perímetro.

## PERÍMETRO

Toca solamente lo necesario para:

* los inputs históricos/versionados directamente responsables de las tres discrepancias;
* referencias posteriores que deban apuntar inequívocamente a una sucesora;
* `data/corrida0/corridas.tsv`;
* `data/corrida0/resultados.tsv`;
* `forense/no-corrido.tsv`;
* nota breve de cierre;
* encargo archivado;
* cascada mínima de estado/gobernanza requerida por las reglas actuales del repo.

No reparar `NC-0141`, `NC-0146`, `NC-0147`, `NC-0148` ni otras NC en este acto.

## ENTREGA

Haz un cambio pequeño y fusionable.

Abre PR contra `main`.

En el cuerpo del PR coloca primero:

1. `VEREDICTO NC-0145`;
2. tabla de las tres corridas;
3. qué identidad se restauró o qué transición se adjudicó;
4. resultado final de `registro --verifica --escribe`;
5. conteos finales;
6. `NO-CORRIDO / RESERVAS`;
7. verificación.

NO fusiones el PR.

Al terminar, devuelve el número de PR y detente.
