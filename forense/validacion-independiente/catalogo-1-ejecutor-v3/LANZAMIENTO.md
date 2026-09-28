# Lanzamiento sucesor de C1 · parámetros y compuertas

PROPUESTO-POR-EJECUTOR. Corte de preparación: `7748208614570a50a97c1ba830aee72a972185f9`. Esta receta no autoriza abrir un paquete. La separación de contexto de un proveedor se acredita con un broker y una sesión nueva verificables; un proceso nuevo de Python no la acredita.

## Orden parametrizada

El operador de un lote autorizado define `PAQUETE_TAR` (solo insumos, sin reconstructor), `ALLOWLIST_JSON` (manifiesto de esos insumos), `RECIBO_SESION`, `DERIVADO_DIR`, `BUNDLE_DIR`, `SALIDA_DIR`, `BACKEND`, `SPEC_SHA256`, `CONTRATO_SHA256`, `TOLERANCIA_SHA256`, `PROVEEDOR`, `SESION_NUEVA_ID` y `AUTORIZACION_ID`. Para `BACKEND=podman|docker` define además `IMAGE_DIGEST` con forma `nombre@sha256:<64 hex>`. Los tres identificadores de proveedor, sesión y autorización son evidencia, no secretos. La cuenta y su credencial permanecen en el orquestador. La sesión solo recibe un prompt nuevo que enumera los archivos del paquete permitido, el contrato v3 y el objetivo de recálculo; se prohíbe transportar historial, memoria, documentos de dirección, valores de referencia y esta misión. El broker debe registrar modelo, identificador de sesión creado, prompt SHA-256, conjunto de herramientas permitido y lista de archivos entregados. El cliente de este paquete no crea por sí solo esa sesión.

`ALLOWLIST_JSON` tiene `{version:1,input_files:[{path,sha256}],output_files:[{path,max_bytes}],max_total_output_bytes}`. El TAR contiene exactamente `input_files` y excluye `reconstructor.py`. El código llega solo en el recibo atestado del broker; `assemble` crea `input.tar`, `manifest.json` y `provenance.json` en `DERIVADO_DIR`.

```sh
python3 tools/validacion/astra6_ejecutor_v3/session_request.py request \
  --source-archive "$PAQUETE_TAR" --source-manifest "$ALLOWLIST_JSON" \
  --prompt "$PROMPT_NUEVO" --socket "$BROKER_SOCKET" \
  --receipt "$RECIBO_SESION"
python3 tools/validacion/astra6_ejecutor_v3/session_request.py assemble \
  --source-archive "$PAQUETE_TAR" --source-manifest "$ALLOWLIST_JSON" \
  --receipt "$RECIBO_SESION" --output "$DERIVADO_DIR"
python3 tools/validacion/astra6_ejecutor_v3/runtime.py build \
  --archive "$DERIVADO_DIR/input.tar" \
  --manifest "$DERIVADO_DIR/manifest.json" --output "$BUNDLE_DIR"
python3 tools/validacion/astra6_ejecutor_v3/runtime.py run \
  --bundle "$BUNDLE_DIR" --output "$SALIDA_DIR" \
  --backend namespace
```

Para un host con contenedor dedicado, la cuarta orden usa `--backend podman --image "$IMAGE_DIGEST"` o `--backend docker --image "$IMAGE_DIGEST"` en vez de `--backend namespace`. `session_request.py` requiere un servicio de broker previamente provisionado en `BROKER_SOCKET`; su cliente no inventa proveedor ni credenciales. `request` verifica y sella la respuesta de código; `assemble` deriva un TAR de ejecución trazado al paquete original y al recibo de la sesión. Si no existe ese broker, la compuerta de contexto queda pendiente y se detiene el intento real.

El orquestador debe verificar primero hashes de spec, contrato y tolerancia fijados, y archivar fuera del bundle el SHA de `seal.json` creado por `build` antes de entregarlo. El bundle contiene `runtime-lock.json` con versión Python/NumPy y SHA-256 de cada archivo de runtime; `run` debe rechazar cambios desde el sello. Después entrega la entrada allowlist al proveedor nuevo, recibe código y resultados en el directorio exportado, sella todos los bytes del reconstructor y de sus diagnósticos, y solo entonces abre la referencia y compara. Si cualquier exportación se trunca, cambia después del sello o no coincide con el manifiesto, se rechaza antes de comparar. Un paquete real requiere una orden adicional de lanzamiento con parámetros concretos y sus cuatro compuertas satisfechas.

## Gates independientes por cohorte

`SÍ` exige evidencia propia por paquete. `PENDIENTE` no se hereda de un PR fusionado. Las cohortes son conjuntos de trabajo, no un denominador de resultados.

| Cohorte | APTO-TECNICAMENTE | CONTEXTO-NUEVO-ACREDITADO | CONTRATO-FIRMADO | ACCESO-AUTORIZADO |
|---|---|---|---|---|
| Lote 1 y sus sucesores | PENDIENTE de ejecución de v3 en la caja | PENDIENTE de broker/sesión remota nueva | PENDIENTE de firma material v3 | Por paquete; no inferido de ejecución anterior |
| Lote 2 preparado | PENDIENTE de ejecución de v3 | PENDIENTE de broker/sesión remota nueva | PENDIENTE de firma material v3 | Por paquete; reservas de #1222 vigentes |
| Ventanas temporales | PENDIENTE de ejecución de v3 | PENDIENTE de broker/sesión remota nueva | PENDIENTE de firma material v3 | Por paquete; 859 ventanas no habilitadas en bloque |
| Residuales documentales v2 | PENDIENTE de ejecución de v3 | PENDIENTE de broker/sesión remota nueva | PENDIENTE de firma material v3 | Por paquete; 312 residuales no habilitados en bloque |

Una prueba sintética puede poner APTO-TECNICAMENTE en `SÍ` para el runtime probado, pero no mueve los otros tres gates ni autoriza un intento C1 real. Las cuatro preguntas de E.2 siguen separadas: coincidencia numérica, validez del estimando, adopción y capacidad predictiva.
