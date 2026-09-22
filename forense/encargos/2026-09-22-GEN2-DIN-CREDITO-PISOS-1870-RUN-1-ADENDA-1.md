Decisión: (a), versión corregida — registro de lo ya sellado, sin run. Tu lectura es la correcta: el CALC corrió sobre ENIF 2021 real en 17d27f82 (21/sep 20:31) y la fila la borró 344739d1 («CI: revierte derivados protegidos»). Un -0002 sería un segundo "primer resultado" y cae en PARO b/d, como dices.

OBJETIVO reescrito: preflight + verify del -0001 existente (réplica sobre ENIF 2021, dos ejes), asiento en replay-evidencia.tsv con cita a 17d27f82, registro --verifica --escribe --lote del -0001, nota. «Hecho» = verify REPRODUCE · fila en corridas.tsv · asiento con los hashes de identidad. Se retira el criterio sobre medidor_ejecutado_al_congelar: es un campo de COMMIT-1 y describe la prueba sintética a propósito; error de redacción de dirección.

Firma ff56-01: existe en #1001 (TRÁMITE-FIRMAS-6, abierto, CONFLICTING) — tipo (3) para ti. No la necesitas para registrar: la firma autorizaba el run, y el run ya ocurrió bajo el contador del acto padre (GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1). Cítala como #1001 y no la asientes; mesa resuelve el conflicto de #1001 aparte.

K2-BANCARIA-HISTORIA: misma situación (corrió en el mismo commit, NO-CORRIDA en la vista). Va en lote contigo (D-11) — pero solo cuando mesa confirme que la sesión del worktree ~/mm-gen2-din-credito-k2-historia-run-1 está muerta (mesa: contesta eso en tu siguiente mensaje). Si está viva, registras solo el -1870 y dejas K2 en ## NO-CORRIDO con DIFERIDO-A: K2-HISTORIA-RUN-1, y esa sesión hace su propio registro en vez de run. Nunca dos escritores sobre los derivados.

Un hallazgo de aparato, con fila: un CI que revierte corridas.tsv/resultados.tsv puede borrar el registro de corridas selladas y dejar el contador mintiendo (E.7). Abre la NC con 344739d1 y el diff como evidencia; sucesor SIN-ASIGNAR (dirección lo redacta: "qué protege ese revert y qué destruye").

Tu memoria («un CALC sellado sin fila puede deberse a esa reversión de CI») va también a hallazgos.md, con cita.
