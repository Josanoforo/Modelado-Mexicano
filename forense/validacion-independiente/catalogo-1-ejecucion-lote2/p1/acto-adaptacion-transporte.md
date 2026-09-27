# P1 · Adaptación de transporte v1

EJECUTADO: contrato para once entradas/425 identidades congelado antes de primer lanzamiento, con originales y sucesores separados. Los bytes de tolerancia.json de cada sucesor coinciden con los del contenedor original; no se fijan nuevas tolerancias. Los hashes de tar/manifiesto coinciden con p3-verificacion.json de #1185. La correspondencia de llaves es completa, biyectiva e idéntica a las entradas originales.

EJECUTADO: cinco pruebas sintéticas rechazan hash equivocado, versión desconocida, llaves repetidas, llaves ausentes y salida sin congelación. Un recibo sintético válido y la cobertura exacta pasan. Archivo de resultados: pruebas-sinteticas-v1.json. Ningún valor numérico esperado fue leído: el contrato conserva únicamente SHA-256 del archivo histórico completo y las identidades procedentes de estimandos.tsv.

LEÍDO: lanzamientos-lote2.md, hoja de firma y p3-verificacion.json. La preparación histórica no constituye autorización de nuevas reservas ni rehabilita un veto. La vigencia/permiso específico de entrega se revalida por el responsable antes de materializar; este contrato no sustituye ese gate.

El adaptador verifica su propio hash y el contrato, identidad sucesora, SHA de reconstrucción y pertenencia a commit inmutable antes de leer esperados. Mantiene los estados y tolerancias del legado. Publicabilidad, insuficiencia de spec y defecto conceptual requieren adjudicación separada; coincidencia no acredita adopción ni validez del estimando. No se lanzaron sesiones ni recálculos desde P1.

API: compare(reconstruction, receipt, digest, output). CLI: python3 tools/validacion/astra6_lote2/adaptador_comparador_v1.py --reconstruccion R --recibo REC --sha256-recibido SHA --salida NUEVA.

Recibo: paquete (identidad sucesora con sufijo vN), paquete_original, version_entrada (entero), sha256_contenedor, sha256_manifiesto, reconstruccion_sha256, congelado_antes_de_revelacion (true), commit_reconstruccion y checkout_reconstruccion. La reconstrucción TSV usa las llaves del paquete, estado y punto/ic95_inf/ic95_sup. Los únicos estados previos permitidos son RECONSTRUIDO, NO-EVALUADO, NO-RECALCULABLE-DESDE-SPEC y BLOQUEADO-POR-ACCESO.

La congelación se publica en congelacion-adaptador-v1.json. Cualquier cambio posterior del procedimiento requiere objeto sucesor; no se alterará este adaptador para acomodar resultados.
