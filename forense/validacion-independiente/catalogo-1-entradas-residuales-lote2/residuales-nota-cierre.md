# Entradas residuales lote2 · nota de entrega

Preparación documental con resultados previos conocidos. Cero recálculos y cero adopciones. Contador: celdas_validadas 219 → 219 (Δ0) @ 165308cc, derivado mediante tools/cierre_acto.py --sin-suite; el acto no cambia CALC, resultados ni decisiones adoptadas.

EJECUTADO: P1 deriva 368 filas llave×componente (56 puntos y 312 IC), unión 312, intersección 56, desde las 425 llaves del corte recibido #1202. `p1/comprobacion-corte.json` y `p1/entradas-entregadas-sha256.json` conservan evidencia y hashes. Las dos diferencias previas de punto y ocho de IC se preservan en `p1/discrepancias-previas-preservadas.tsv` y `p5/diferencias-previas.md`, sin reclasificación retroactiva.

LEÍDO: las specs humanas anteriores de ENCUCI rural y ENIGH definen las identidades faltantes en la entrega; extracción restaurada sin consultar productores. Los originales se referencian por hash y localizador en P2; nunca se modifican ni se incluyen completos si mezclan resultados. Los descriptores públicos recuperados son contenido completo, no enlaces sin bytes.

PROPUESTO: tratamiento de edad desconocida en ENBIARE y recetas de incertidumbre suficientes para sucesores. La hoja P5 recomienda decidir por cohorte y mantiene distinta la restauración de contrato histórico respecto a una firma de contrato nuevo. El nuevo contrato no vuelve histórica una receta posterior ni equivale a igualdad bit a bit con el intento anterior; ninguna tolerancia cambia.

EJECUTADO: archivo recibido íntegro, tres adjuntos embebidos extraídos y verificados en 0-bis; se retiraron las copias añadidas por este acto que duplicaban originales ya registrados y se referencian las copias ya existentes para evitar duplicación. `archivo/archivo-procedencia.json` fija SHA de redacción real del acto y fuentes. Firma «Acordado» citada desde el asiento existente; no se duplica. Interpretación del entorno CLI documental y lectura dirigida en `residuales-arranque.md`.

NO-VERIFICADO: ningún nuevo punto, IC, reproducción científica, aislamiento efectivo de una futura sesión ni recibo independiente de Claude. Una entrada materializada y verificada documentalmente no acredita ejecución ni ceguera cognitiva. No se corrieron recalculadores, microdatos, productores sellados, nuevas olas, verify de CALC ni CI adicional. El recibo se solicita en el PR por circuito de mesa; no se afirma recibido y no se fusiona.

## Decisiones y reservas

Recomendación: aceptar la restauración documental de ENCUCI/ENIGH; decidir expresamente los contratos nuevos de ENBIARE e IC de P3 por cohorte y hash, y entregar únicamente los contenedores aprobados a una sesión nueva con separación efectiva. Mantener todas las discrepancias anteriores. `FP-260927-GEN2-ASTRA6-C1-ENTRADAS-LOTE2-RESIDUALES-1-1653-01` registra la firma nueva pendiente; `NC-260927-GEN2-ASTRA6-C1-ENTRADAS-LOTE2-RESIDUALES-1-1653-01` registra el recibo externo pendiente.

La preparación cuenta con resultados conocidos y no se presenta como validación ciega. No se cambiaron contratos históricos, catálogo, adopciones, motor, CI ni archivos de ejecución lote2. Los registros comunes añadidos contienen solo identidades de este acto.

INTERPRETACIÓN-DECLARADA: el recibo solicitado se entrega como `residuales-recibo-para-claude.md`, con prefijo propio para evitar la colisión T02 de nombres normalizados. Conserva contenido y función de recibo, sin alterar actos anteriores.

EJECUTADO: `python3 tools/validacion/astra6_entradas_residuales/p1.py` PASS (368 pares, unión312); `python3 tools/validacion/astra6_entradas_residuales/p4.py --verifica` PASS (4 contenedores,312identidades,40miembros, bytes reproducibles); `git diff --cached --check` PASS; `python3 tests/check.py --rapido --baseline` VERDE, sin FAIL nuevos y 0 FAIL global. Gate documental, no evidencia científica. Detalle en `residuales-verificacion-final.json`.

PR propio publicado: https://github.com/Josanoforo/Modelado-Mexicano/pull/1229. Recibo técnico solicitado en el cuerpo del PR, aún no obtenido; merge y firma de contratos pendientes.
