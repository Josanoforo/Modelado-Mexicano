# Lanzamiento sucesor de C1 · parámetros y compuertas

PROPUESTO-POR-EJECUTOR. Corte de preparación: `7748208614570a50a97c1ba830aee72a972185f9`. Esta receta no autoriza abrir un paquete. La separación de contexto de un proveedor se acredita con un broker y una sesión nueva verificables; un proceso nuevo de Python no la acredita.

## Orden parametrizada

El operador de un lote autorizado define `PAQUETE_TAR` (solo insumos, sin reconstructor), `ALLOWLIST_JSON` (manifiesto de esos insumos), `PROMPT_NUEVO`, `BROKER_SOCKET`, `RECIBO_SESION`, `RECIBO_SHA256`, `DERIVADO_DIR`, `BUNDLE_DIR`, `MANIFEST_EJECUCION_SHA256`, `SALIDA_DIR`, `IDENTIDAD_JSON`, `TOLERANCIA_JSON`, `ANCLA_EXPORTACION`, `CONGELADO_DIR`, `CONGELACION_SHA256`, `REFERENCIA_JSON`, `REFERENCIA_SHA256`, `COMPARACION_JSON`, `BACKEND`, `SPEC_SHA256`, `CONTRATO_SHA256`, `TOLERANCIA_SHA256`, `PROVEEDOR`, `SESION_NUEVA_ID` y `AUTORIZACION_ID`. Para `BACKEND=podman|docker` define además `IMAGE_DIGEST` con forma `nombre@sha256:<64 hex>`. `RECIBO_SHA256`, `MANIFEST_EJECUCION_SHA256` y `CONGELACION_SHA256` son los valores emitidos por los pasos previos y retenidos por el orquestador fuera de sus directorios mutables. La cuenta y su credencial permanecen en el orquestador. La sesión solo recibe un prompt nuevo que enumera los archivos del paquete permitido, el contrato v3 y el objetivo de recálculo; se prohíbe transportar historial, memoria, documentos de dirección, valores de referencia y esta misión. El broker debe registrar proveedor/modelo, identificador de sesión creado, prompt SHA-256, conjunto de herramientas permitido y lista de archivos entregados. El cliente de este paquete no crea por sí solo esa sesión.

`ALLOWLIST_JSON` tiene `{version:1,input_files:[{path,sha256}],output_files:[{path,max_bytes}],max_total_output_bytes}`. El TAR contiene exactamente `input_files` y excluye `reconstructor.py`. El código llega solo en el recibo atestado del broker; `assemble` crea `input.tar`, `manifest.json` y `provenance.json` en `DERIVADO_DIR`.

```sh
python3 tools/validacion/astra6_ejecutor_v3/session_request.py request \
  --source-archive "$PAQUETE_TAR" --source-manifest "$ALLOWLIST_JSON" \
  --prompt "$PROMPT_NUEVO" --socket "$BROKER_SOCKET" \
  --receipt "$RECIBO_SESION"
# Guardar fuera del directorio mutable el receipt_sha256 emitido por request.
python3 tools/validacion/astra6_ejecutor_v3/session_request.py assemble \
  --source-archive "$PAQUETE_TAR" --source-manifest "$ALLOWLIST_JSON" \
  --receipt "$RECIBO_SESION" --prompt "$PROMPT_NUEVO" \
  --expected-receipt-sha256 "$RECIBO_SHA256" --output "$DERIVADO_DIR"
python3 tools/validacion/astra6_ejecutor_v3/runtime.py build \
  --archive "$DERIVADO_DIR/input.tar" \
  --manifest "$DERIVADO_DIR/manifest.json" --output "$BUNDLE_DIR"
# Guardar fuera del bundle el manifest_sha256 emitido por build y el SHA de seal.json.
python3 tools/validacion/astra6_ejecutor_v3/runtime.py run \
  --bundle "$BUNDLE_DIR" --output "$SALIDA_DIR" \
  --backend namespace
python3 tools/validacion/astra6_ejecutor_v3/runtime.py freeze-export \
  --export "$SALIDA_DIR" --anchor "$ANCLA_EXPORTACION" \
  --identity "$IDENTIDAD_JSON" \
  --input-manifest-sha256 "$MANIFEST_EJECUCION_SHA256"
python3 tools/validacion/astra6_ejecutor_v3/compare_v3.py freeze \
  --export "$SALIDA_DIR" --export-anchor "$ANCLA_EXPORTACION" \
  --tolerance "$TOLERANCIA_JSON" --output "$CONGELADO_DIR"
# Guardar fuera de CONGELADO_DIR el SHA impreso por freeze.
python3 tools/validacion/astra6_ejecutor_v3/compare_v3.py compare \
  --frozen "$CONGELADO_DIR" --expected-sha256 "$CONGELACION_SHA256" \
  --reference "$REFERENCIA_JSON" --reference-sha256 "$REFERENCIA_SHA256" \
  --output "$COMPARACION_JSON"
```

Para un host con contenedor dedicado, `run` usa `--backend podman --image "$IMAGE_DIGEST"` o `--backend docker --image "$IMAGE_DIGEST"` en vez de `--backend namespace`. **Solo namespace ha sido probado en esta caja**; OCI y otra máquina son NO-VERIFICADOS y requieren pruebas propias de versión, digest de imagen y canarios. `session_request.py` requiere un servicio de broker previamente provisionado en `BROKER_SOCKET`; su cliente no inventa proveedor ni credenciales. `request` emite `receipt_sha256` para conservar fuera del recibo; `assemble` coteja ese SHA, el prompt y la solicitud canónica, y deriva un TAR trazado al paquete original. Si no existe broker, la compuerta de contexto queda pendiente y se detiene el intento real.

El orquestador verifica primero hashes de spec, contrato y tolerancia fijados. `IDENTIDAD_JSON` contiene exactamente `paquete`, `version_entrada` y `sha256_entrada` esperados. El bundle contiene `runtime-lock.json` con versión Python/NumPy y SHA-256 de cada archivo de runtime; `run` rechaza cambios desde su sello interno. `freeze-export` fija fuera de `SALIDA_DIR` la identidad del paquete, el hash del manifiesto de entrada fijado antes de ejecutar y el hash del manifiesto de exportación. `compare_v3 freeze` copia resultado, código, diagnósticos, auxiliares, contrato, comparador y tolerancia a `CONGELADO_DIR`; el SHA que imprime se conserva por el orquestador fuera de ese directorio. Solo entonces se revela `REFERENCIA_JSON`. `compare` exige ese SHA externo y verifica todos los bytes congelados antes de abrirla; compara punto y ambos extremos IC con tolerancias v2. Un paquete real requiere una orden adicional de lanzamiento con parámetros concretos y sus cuatro compuertas satisfechas.

## Gates independientes por cohorte

`SÍ` exige evidencia propia por paquete. `PENDIENTE` no se hereda de un PR fusionado. Las cohortes son conjuntos de trabajo, no un denominador de resultados.

| Cohorte | APTO-TECNICAMENTE | CONTEXTO-NUEVO-ACREDITADO | CONTRATO-FIRMADO | ACCESO-AUTORIZADO |
|---|---|---|---|---|
| Lote 1 y sus sucesores | SÍ para namespace de esta caja en sintéticos; por paquete real PENDIENTE | PENDIENTE de broker/sesión remota nueva | PENDIENTE de firma material v3 | Por paquete; no inferido de ejecución anterior |
| Lote 2 preparado | SÍ para namespace de esta caja en sintéticos; por paquete real PENDIENTE | PENDIENTE de broker/sesión remota nueva | PENDIENTE de firma material v3 | Por paquete; reservas de #1222 vigentes |
| Ventanas temporales | SÍ para namespace de esta caja en sintéticos; por paquete real PENDIENTE | PENDIENTE de broker/sesión remota nueva | PENDIENTE de firma material v3 | Por paquete; 859 ventanas no habilitadas en bloque |
| Residuales documentales v2 | SÍ para namespace de esta caja en sintéticos; por paquete real PENDIENTE | PENDIENTE de broker/sesión remota nueva | PENDIENTE de firma material v3 | Por paquete; 312 residuales no habilitados en bloque |

Una prueba sintética puede poner APTO-TECNICAMENTE en `SÍ` para el runtime probado, pero no mueve los otros tres gates ni autoriza un intento C1 real. Las cuatro preguntas de E.2 siguen separadas: coincidencia numérica, validez del estimando, adopción y capacidad predictiva.
