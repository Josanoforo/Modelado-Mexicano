# Contrato v2 · PROPUESTO-POR-EJECUTOR

Este contrato y su JSON ejecutable cierran el transporte antes de lanzamientos reales futuros. El cierre técnico se acredita por hashes de contrato y adaptador en la congelación; un cambio exige versión nueva. La preparación conoce resultados históricos y no constituye validación ciega ni concede apertura. El adaptador v1 y todos los originales permanecen intactos.

LEÍDO: se consultaron exclusivamente cabeceras TSV de reconstrucciones y nombres de rechazos de `catalogo-1-ejecucion-lote2/p3`, además del adaptador y contrato v1. No se leyó raw ni productores. Los nueve originales rechazados se reproducen mediante cifras sintéticas, no reinterpretando cifras históricas:

| Intento | Punto | IC inferior | IC superior |
|---|---|---|---|
| eder-0003-v4 | valor | ic_025 | ic_975 |
| enbiare-pisos-bienestar-0001-v3 | estimacion | ic95_inf | ic95_sup |
| encig-0001-v5 | p | ic95_inf | ic95_sup |
| encodat-pisos-sustancias-0001-v3 | valor | ic95_inferior | ic95_superior |
| encuci-0001-v3 | estimacion | ic95_inf | ic95_sup |
| enfih-0001-v4 | valor | ic95_inf | ic95_sup |
| enigh2020-intensidad-remesas-0001-v4 | valor | ic95_inf | ic95_sup |
| envipe-0001-v5 | estimacion | ic95_inferior | ic95_superior |
| envipe-denuncia-seguro-0001-v4 | estimacion | ic_025 | ic_975 |

También se observaron `proporcion` en ENDIREH y `ic_inferior/ic_superior` en ENIGH; sus comparaciones v1 no son uno de los nueve rechazos. Una cabecera alias es cableado, no evidencia de coincidencia científica. Los dictámenes posteriores separados no convierten esos nueve rechazos en éxito v1.

El documento JSON contiene exactamente `version:2`, `identidad` y `filas`. La identidad contiene exactamente strings no vacíos `paquete`, `version_entrada`, `sha256_entrada` (SHA-256 hexadecimal). El hash debe corresponder a los bytes de entrada congelados. Cada fila contiene `llave`, `unidad`, `estado`; sus opcionales son `estado_ic`, `motivo`, `motivo_ic` y como máximo un alias por campo numérico. No se transportan columnas auxiliares históricas: un futuro reconstructor emite este esquema explícito. Se rechazan extras, duplicados JSON y de llaves, colisiones aunque tengan valores iguales, booleanos, arrays, NaN, infinito, números no decimales, identidad incompleta y unidades diferentes de la referencia. `unidad` es texto literal; el contrato nunca convierte porcentajes en proporciones.

La derivada conserva cada número o string decimal recibido y solo renombra campos. Para JSON leído desde disco conserva el lexema decimal como string y conserva los bytes originales por separado. No redondea, rellena ni reescala. Punto ausente, punto `null` y número son distintos; RECONSTRUIDO exige punto numérico. IC ausente y extremos `null` son distintos. `estado_ic:SIN-IC` exige ambos extremos ausentes y representa una declaración explícita distinta del simple silencio; `CALCULADO` exige extremos numéricos. Un IC parcial, null parcial o invertido se rechaza. Estados previos a revelación: RECONSTRUIDO, NO-EVALUADO, NO-RECALCULABLE-DESDE-SPEC, BLOQUEADO-POR-ACCESO; los tres últimos se conservan, no se transforman en coincidencia.

La normalización devuelve mapa por llave de campo canónico a alias recibido (o null si ausente). `freeze` crea un directorio nuevo, copia original, entrada, código propio, adaptador, contrato y tolerancia, y escribe derivada y manifiesto con todos los hashes. El SHA del manifiesto se conserva fuera de ese directorio como ancla antes de revelación; el hash no prueba tiempo por sí solo. La sesión responsable debe acreditar el orden mediante commit/atestación previa y registro de entrega al comparador. `verify_freeze` exige ese SHA externo, verifica todos los archivos y vuelve a derivar desde el original. La referencia solo se abre después de estas verificaciones y requiere SHA externo predeclarado. Rechaza alteración de entrada, números, código, mapa, contrato, tolerancia o manifiesto. Los nombres de miembros son locales sin symlinks. Un actor capaz de reemplazar también todas las anclas externas queda fuera de esta garantía: esas anclas deben custodiarse por el orquestador.

La tolerancia se recibe explícita como JSON `{abs:decimal,rel:decimal}` no negativa y queda congelada. La comparación usa exactamente `abs(a-b) <= max(abs_tol, rel_tol*max(abs(a),abs(b)))` mediante decimal con precisión suficiente para los operandos; conserva umbrales y no los adapta a los valores revelados. Las llaves e identidades de ambos documentos deben coincidir. Ausencia/null/SIN-IC diferentes producen DISCREPA, sin inventar intervalos. COINCIDE/DISCREPA responden solo coincidencia numérica, no estimando, adopción o autorización de apertura.

Comandos desde raíz (sin sobrescribir archivos existentes):

```sh
python3 tools/validacion/astra6_aislamiento_v2/adaptador.py normalizar original.json derivada.json
python3 tools/validacion/astra6_aislamiento_v2/adaptador.py congelar /tmp/congelacion-v2 original.json entrada tolerancia.json reconstruir.py
python3 tools/validacion/astra6_aislamiento_v2/adaptador.py verificar /tmp/congelacion-v2 SHA_MANIFIESTO_EXTERNO
python3 tools/validacion/astra6_aislamiento_v2/adaptador.py comparar /tmp/congelacion-v2 SHA_MANIFIESTO_EXTERNO referencia.json SHA_REFERENCIA_EXTERNO comparacion.json
```

API Python: `normalize(document, contract=None)`, `freeze(artifact_dir, original_path, code_paths, entry_path, tolerance_path, contract_path=CONTRACT)`, `verify_freeze(artifact_dir, expected_manifest_sha256)`, `compare(artifact_dir, expected_manifest_sha256, reference_path, expected_reference_sha256)`. `read_json` es obligatorio para lectura estricta sin duplicados. La comparación devuelve identidad, hashes de contrato/comparador/tolerancia/ancla/referencia y resultados por campo, con estados actual/referencia, delta decimal y dentro de tolerancia. Su SHA final se calcula sobre el archivo escrito por CLI y se archiva en evidencia del circuito.
