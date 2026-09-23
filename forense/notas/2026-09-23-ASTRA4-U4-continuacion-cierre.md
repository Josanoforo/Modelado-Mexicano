# Cierre de continuación ASTRA4-U4 · PR #1076

Base: rama `codex/astra4-familias-prospectivas-1`, HEAD heredado `d21f1551c571b77e43e1f72bc9a36a91151f63a3`. Rama remota consultada con fetch autorizado y sin divergencia.

## Producto

Se preservan intactas las seis specs selladas v1.0; se añaden specs humanas v1.1 y sidecars con propuestas de tolerancia ±2 pp, soporte por unidad, faltantes, comparabilidad y reglas de dictamen. La hoja actualizada mantiene las familias CONDICIONALES hasta fecha oficial y cotejo instrumental. HVD requiere estimación conjunta, porque el CALC derivado no trae incertidumbre conjunta. Se mantienen fuera microdatos, olas reservadas, pilotos, retadores y cambios en CALC.

## Verificación

`python3 forense/analisis/familias-2027/genera.py` produce seis specs. Las seis parejas CALC/RESULT/SHA coinciden con `sello.json` y `sello.sha256`; se verificó cada sidecar nuevo por bytes. `tools/sella_sha256.py --verifica --cuerpo` confirma el cuerpo del encargo original.

`python3 tests/check.py --baseline`: T06 2 FAIL, T08 1 FAIL, T22 1 FAIL, más WARN globales de referencias/firmas. T06/T08 son deudas preexistentes declaradas en `tests/check.py`. El worker T35 aislado devuelve cero FAIL. Sin pruebas sobre microdatos ni replay de los CALC fuente.

## NO-CORRIDO / RESERVAS

La actualización de calendario en línea falló inicialmente por DNS; no se afirma que no haya anuncio posterior al calendario 2026 ya leído. No se abre dato ni se corre CALC. Potencia y efecto mínimo detectable siguen no calculables por falta de los vectores de réplica adecuados; no se reconstruyen desde extremos de IC. No se fusiona.

## CONSUMIDO

PR existente #1076 actualizado en `codex/astra4-familias-prospectivas-1`; producto preparado para revisión. No se creó rama ni PR.
