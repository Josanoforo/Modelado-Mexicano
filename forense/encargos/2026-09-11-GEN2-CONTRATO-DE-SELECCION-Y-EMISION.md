# ACTO GEN2-CONTRATO-DE-SELECCION-Y-EMISION — encargo archivado

- **SHA de redacción:** `70c64d9ead92384ece0eaf18cbfb53372bb88a74`
  (`origin/main` al iniciar la ejecución).
- **Entorno asignado:** NUBE; compatible también con Codex CLI.
- **Estado:** `CONSUMIDO`.

## VERIFICACIÓN DE EXISTENCIA

- **Estructura:** existen `milpa/src/emisor.py`, `milpa/src/linaje.py`,
  `tools/baseline_temporal.py`, `tools/snapshot_motor_gen2.py`,
  `tests/test_motor_gen2_explicito.py`, las vistas bajo `data/corrida0/`, el
  snapshot GEN2 explícito v1.0 y la nota de cierre de #712.
- **Contenido:** el contraejemplo indicado se reprodujo en `origin/main`: la
  consulta y la transferencia aceptan `RESULT-R-CIV-M-01-P-C1-U1` y emiten
  `0.29557241046799515` para `recibe_remesas`. Los únicos llamadores reales de
  la interfaz GEN2 están en el constructor del snapshot; las demás llamadas
  son pruebas.
- **Cobertura retroactiva:** #712 y #718 están fusionados. Al iniciar no había
  PR abierto ni correctivo remoto del mismo objeto; este acto parte del
  `origin/main` vigente y preserva el snapshot v1.0 como antecedente.
- **Medición ya existente:** salida final de
  `python3 tools/ya_medido.py familia.seguro.volatilidad_ausencia_estado`:
  `MEDIDA-EN: CALC-B-0001, tramite-ola5-propuesta-v0.yaml, tramite.yaml`.

## Texto del encargo, verbatim

```text
ACTO: GEN2-CONTRATO-DE-SELECCION-Y-EMISION
ENTORNO: NUBE
Compatible también con Codex CLI.
REPOSITORIO: Josanoforo/Modelado-Mexicano

OBJETIVO

Cerrar el hueco de la interfaz de emisión incorporada por PR #712:
un RESULT de otro estimando no debe convertirse en el valor de un
consumidor por pasarlo como selección externa.

Entregar código integrado, snapshot vigente reproducible y PR.
Preservar las emisiones legítimas y la transferencia temporal correcta.

AUTORIDAD Y OPERACIÓN

Este encargo autoriza su implementación, comprobación dirigida,
documentación necesaria, commits, push y apertura o actualización del PR.
La fusión queda en manos de Jonás.

Trabaja en un worktree y una rama propios. Lee AGENTS.md y las instrucciones
aplicables. Reporta ruta absoluta, rama, HEAD y estado inicial.
Actualiza las premisas desde origin/main y PR abiertos. Si existe un
correctivo del mismo objeto, continúa ese trabajo sin duplicarlo.

Archiva este encargo mediante el procedimiento vigente. Reutiliza los
contratos, escritores y registros existentes; no crees otra gobernanza.

ANTECEDENTE REPRODUCIDO

En main posterior a #718, emitir_binaria_contrato permite:

- regla: familia.seguro.volatilidad_ausencia_estado
- conducta: recibe_remesas
- contexto: {}
- modo: GEN2
- proposito: consulta, o transferencia
- resultado_id_seleccionado: RESULT-R-CIV-M-01-P-C1-U1
- valor_seleccionado: el valor de ese RESULT en el registro

En ambos casos devuelve EMITE con 0.29557241046799515.

Ese RESULT corresponde a ENVIPE 2012, unidad delito y FAC_DEL.
No mide recepción de remesas. El snapshot publicado de #712 utiliza el
selector correcto y no presenta esta mezcla.

ARCHIVOS INICIALES

- milpa/src/emisor.py
- milpa/src/linaje.py
- tools/baseline_temporal.py
- tools/snapshot_motor_gen2.py
- tests/test_motor_gen2_explicito.py
- Registro de resultados y usos bajo data/corrida0/
- forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_0.json
- Nota de cierre GEN2-MOTOR-Y-HERENCIA-EXPLICITA de #712

FASE 1 — FIJAR EL CONTRATO MÍNIMO

Reproduce el caso y localiza los llamadores reales.

En consulta, una selección externa no puede saltarse el RESULT adoptado
por el consumidor. Rechaza esa combinación o elimina la posibilidad de
expresarla desde esa ruta.

En transferencia, transporta una selección estructurada y verificable:
objetivo, estimando, unidad, población, codificación, transformación,
periodo, disponibilidad, corte temporal y evidencia de procedencia.

Reutiliza las estructuras existentes. Define qué comprueba el selector
y qué vuelve a comprobar el emisor. El contrato no debe depender de una
afirmación libre del llamador sobre compatibilidad o rol.

Una ausencia de evidencia produce NO_COVERAGE con causa concreta.

FASE 2 — IMPLEMENTAR Y CONECTAR

Corrige el emisor y sus llamadores reales.

Comprueba que:
- El RESULT seleccionado pertenece a la serie y uso permitidos.
- El valor coincide con la evidencia.
- Se respeta el corte temporal.
- El rol respecto al experimento se resuelve desde evidencia acreditada.
- Renombrar un RESULT o escribir OPERATIVO no elimina su dependencia
  respecto del objetivo.
- Un complemento conserva la transformación y dependencia de su padre.

No uses prefijos como RESULT-R como única regla de exclusión: el rol
depende del uso experimental y de la procedencia.

Mantén las restricciones existentes sobre origen heredado, mixto o
indeterminado. No uses probabilidades legacy, cero o R como sustitutos
cuando GEN2 no tiene cobertura.

FASE 3 — VERIFICAR EL RESULTADO UTILIZABLE

Comprueba de forma dirigida:
1. El contraejemplo ENVIPE→remesas deja de emitir.
2. Consulta no permite activar transferencia mediante parámetros.
3. Una selección incompatible o posterior al corte se rechaza.
4. La transferencia ENIGH legítima sigue funcionando.
5. Las emisiones directas GEN2 vigentes conservan sus valores.
6. Los complementos y roles siguen aplicando su contrato correcto.

En el corte revisado eran 16 emisiones directas. Deriva el conjunto actual;
no congeles ese total como una condición eterna de los tests.

Regenera únicamente el snapshot derivado correspondiente. Si modifica
su contrato o formato, registra la sucesión y sus consumidores.
No reescribas snapshots ni resultados experimentales sellados.

FASE 4 — CIERRE

Entrega PR con:
- Contrato implementado y llamadores actualizados.
- Evidencia breve del rechazo del caso y conservación de usos válidos.
- Snapshot derivado coherente con el código.
- Cadena administrativa aplicable y pendiente asociado conciliado.
- Reservas limitadas a obligaciones realmente no satisfechas.

Un test dirigido protege este defecto material. No abras una auditoría
general ni repitas suites costosas sin una incertidumbre concreta.

DEPENDENCIAS Y LÍMITES

Puede correr en paralelo con los encargos 24, 25 y 26.
Coordina con 25 el formato del contrato; 25 no modifica el emisor.
No autoriza nuevas capturas F5, adopciones, firmas metodológicas ni
modificación de resultados históricos.
```

## NO-CORRIDO / RESERVAS

- No se fusiona el PR: esa decisión queda expresamente en manos de Jonás.
- `NC-0158` sigue abierta por roles retenidos de confirmación independiente;
  no es una obligación creada ni satisfecha por este contrato de emisión.
- No quedan reservas técnicas propias de este acto.

## CONSUMIDO

Consumido el 11/sep/2026 por PR #720, rama
`acto/gen2-contrato-seleccion-emision`. El archivo fue fijado verbatim en
`525bd05`; la implementación y el snapshot sucesor quedaron en `67aa13d`, y
la cadena de cierre en el commit posterior del mismo PR. Consulta rechaza toda
selección externa; transferencia exige `SELECCION-TEMPORAL-v1` y la revalida
contra evidencia sellada. El contraejemplo ENVIPE deja de emitir, la
transferencia ENIGH legítima y las 16 emisiones directas se conservan, y el
snapshot v1.0 permanece intacto. ADR-479; contador científico cero; la fusión
queda en manos de Jonás.
