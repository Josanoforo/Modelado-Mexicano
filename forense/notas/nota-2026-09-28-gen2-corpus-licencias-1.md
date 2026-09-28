# Nota de cierre · ACTO GEN2-CORPUS-LICENCIAS-1 · 28/sep/2026 · NUBE

ADR-260928-GEN2-CORPUS-LICENCIAS-1-1997-01 (raíz `1997`, 0-bis `1997e8a1`). Base `a8c3e341` (origin/main; el encargo se redactó sobre `3ac3ab7d`, 8 commits atrás: re-derivé).

## Contadores
Cero mediciones; no adopta. Payloads sin licencia (vacío o «no declarada…», regla de `tests/test_corpus_licencias.py::_sin_licencia`): **626 → 598** (Δ −28). Grafías INEGI sin acento: **72 → 0**.

## Premisas
- [EJECUTADO] 7 049 entradas; 554 sin campo `licencia` (el campo **no existe** en esas entradas, no está vacío), 29 «no declarada por la fuente», 626 en total; desglose por dominio reproduce el de dirección (ensanut 149, losmexicanos 119, «no determinada» 54, ietam 46, inegi 28, …).
- [EXISTE → cayó] `tools/manifiesto.py` no existe; la herramienta es `tests/manifiesto.py`. Logística.
- [SUPUESTO → NO-VERIFICABLE-AQUÍ] que INSP/UNAM/IETAM publican términos: el proxy de esta nube rechaza sus hosts.

## Lo hecho
1. Página de términos del INEGI: GET 200, 10 442 B, sha256 `97e97599169f75f455877e85edffcf941d512f56c5c00197ebfec783d802c67a` (idéntico al leído por GEN2-ADQ-F6-DIRIGIDA-1 el 22/sep).
2. Regla por dominio `inegi.org.mx` → «Términos de Libre Uso de la Información del INEGI (https://www.inegi.org.mx/inegi/terminos.html)», la cadena exacta de 4 816 entradas. Aplicada a los 28 payloads INEGI de ENOE 15ymas con «no declarada por la fuente».
3. Unificación: las 72 «Terminos de Libre Uso de la Informacion…» → la misma cadena.
4. Comando: `python3 forense/analisis/corpus-licencias-1/aplica_licencias.py --aplica`; verifica con `yaml.safe_load` que antes/después difieren solo en `licencia` (100 entradas; diff 100+/100−).
5. Línea base `forense/analisis/corpus-licencias-1/sin-licencia-base.tsv` (598 ids, por comando) y test huérfano `tests/test_corpus_licencias.py` (2 passed): FAIL si entra un id sin licencia fuera de la base, o si reaparece la grafía sin acento.

## Obstáculos (A.5)
- Red: 43 hosts de L1–L5 sondeados (`curl https://<host>/`, 2 intentos en los 4 mayores, 1 en el resto) → `000`; `www.losmexicanos.unam.mx` → 403 «Host not in allowlist»; WebFetch → EGRESS_BLOCKED (ensanut.insp.mx). Solo `www.inegi.org.mx` responde. NO OBTENIDO POR ESTE AGENTE. Receta de un minuto: en la configuración del entorno de nube, añadir esos dominios a la red permitida (o acceso completo) y relanzar L1–L5 con el mismo script (añadir una línea a `REGLAS` por portal).
- Registro de la página de términos en el manifiesto: `tests/manifiesto.py --registra` aborta por `estado_reserva` ajeno (`RESERVADA-ASTRA5-U1-…`, NC-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-07). Ampliar el validador lo rechazó el clasificador de permisos de la sesión; no se forzó. La página no queda registrada.
- No se escribieron placeholders en las 598: un «NO-OBTENIDO» en el campo mezclaría «no pude alcanzar la fuente» con «la fuente no tiene el dato» (§2).

## Criterio de «hecho»
Licencia vacía = 0: **NO** (554 → 554; las 28 eran «no declarada»). Resto: ver NO-CORRIDO del encargo.
