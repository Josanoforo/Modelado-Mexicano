# Contrato para escritor autorizado del consumo GEN2

**Estado:** el acto separado #1080 implementó el escritor exclusivo de `RES-0028` y fue fusionado en `main` (`f16dd3d7`). Este contrato rige los demás consumidores; no autoriza aplicarles ese escritor. `tools/relevo_usos.py` deriva candidaturas; `tools/pines_mesa.py` valida `data/corrida0/pines-de-mesa.tsv`; `tools/corrida0.py` proyecta pines en la vista. Una reducción de `dependencias_numericas_legacy_activas` por pin es **trazabilidad relevada**; el consumo efectivo se comprueba en el archivo e interfaz que usan motor y celda-D.

## Entrada y precondiciones

Entrada: una fila firmada de `data/corrida0/pines-de-mesa.tsv`, consumidor lógico exacto, `RESULT` GEN2 de punto, CALC y sello, `verify` con eje RESULTADO afirmativo y CONTEXTO declarado, más valor/escalas/universo del consumidor y candidato. Las vías (i) crudo, (ii) conducta GEN2 ya presente y (iii) derivado determinista se validan por `tools/pines_mesa.py`. Para (iii), todos los insumos son RESULT GEN2 del **mismo CALC** sellado que cuenta; no se permite derivado de derivado ni número GEN1. La vía (ii) exige que la conducta del motor ya cite GEN2 en disco. Un `NO-EJECUTABLE`, `NO-REPRODUCE`, `SIN CITA`, veto, conflicto de estimando o pin sin firma aborta sin cambios.

El escritor debe comprobar la identidad de unidad, universo, denominador, ola y escala y leer la estructura vigente, no buscar y reemplazar números en texto. Si el valor coincidente proviene de distinto estimando, aborta. Debe bloquear modificación de specs selladas, `motor.py`, celdas-D a mano y cualquier archivo fuera del consumidor autorizado. Debe ser idempotente y producir antes un diff seco con hash esperado de entrada.

## Archivos y salida

El mecanismo debe aceptar solo destinos explícitos, inicialmente `milpa/tramite.yaml` para una conducta validada. `milpa/procedencia.yaml` y `milpa/catalogo-momentos-v0_1.tsv` requieren adaptadores propios con firma; `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv` está sellado y no se edita: ahí el resultado es una cita lateral/decisión histórica. Las seis celdas-D que figuran en `milpa/src/celdas.py` y los seis YAML del registro tienen mecanismos de sello separados: no se les aplica el adaptador de trámite.

Para una conducta positiva autorizada, el diff esperado es **estructuralmente**:

```diff
   - conducta: <llave de la fila firmada>
-    p: <literal GEN1 que coincide exactamente con el archivo previo>
+    p: <valor del RESULT GEN2 en escala del consumidor>
+    corrida0_resultado_id: <RESULT GEN2 validado>
+    corrida0_generacion: GEN2
```

Los marcadores `<...>` no son números ni instrucciones para sustituir hoy. Ejemplo negativo real: `RES-0039`–`RES-0042` tienen `LISTADO-PARA-MESA-NO-REPRODUCE` en `CALC-ENVIPE-DENUNCIA-SEGURO-0001`; un escritor correcto deja **diff vacío** aunque exista un CALC. Otro ejemplo negativo: `RES-0004` tiene `COMPLEMENTO-CON-DENOMINADOR-RECORTADO` en `CALC-ENCIG-0001`, por lo que tampoco se cambia su literal.

## Prueba de aceptación para el escritor

1. En una copia temporal de `milpa/tramite.yaml`, una fila de prueba con pin firmado, RESULT reproducible, identidad exacta y literal GEN1 coincidente produce solo las tres líneas del ejemplo y mantiene válido el YAML. Reaplicarla no cambia bytes.
2. Cambiar cualquiera de universo, denominador, ola, escala, firma, hash, veredicto de replay o valor previo causa rechazo atómico y diff vacío.
3. Un test de regresión del consumidor real resuelve `RESULT`, `CALC`, generación y valor después de aplicar. El contador de pines y la consulta al motor se reportan separadamente.
4. Un test de `milpa/` rechaza cualquier cifra empírica de parámetro sin RESULT resoluble; ignora números de versión, códigos de categoría y umbrales de diseño.

**Decisión solicitada a mesa:** nombrar y autorizar el escritor/acto de adaptación por consumidor, con esta compuerta. La unidad U2 no implementa el escritor ni cambia `motor.py`; mientras tanto seguirá midiendo o dictaminando las filas restantes.
