# Cierre · ACTO GEN2-ESTADO-V16-1

Retrata el estado del programa del 18–23/sep en `canon/estado-programa-v1_16.md`: cabecera nueva + §0–§14 heredadas verbatim de `v1_15` (`diff` vacío sobre las líneas 17–789) + §15 nueva (status íntegro de `corrida0.py`, cierre de la etapa de retadores, régimen operativo — canal por PR, sello externo, auto-merge —, misiones de Astra, cobertura de dominios, frente público, FP abiertas, decisiones de mesa del 23/sep) + §16 nueva ("Lo que este estado no puede afirmar"). `canon/estado-programa-v1_15.md` queda intacto — no se le aplica T01 esta vez, a diferencia de la transición `v1_14 → v1_15`.

Premisas de dirección (§3 del encargo) verificadas contra el árbol de hoy (`e792419`, no la cabecera `6a2cd6c7`): `status` coincide dígito a dígito (219 selladas · 219 `celdas_validadas` · 72 adoptados). El `[SUPUESTO]` sobre `CONTADORES-2` resultó falso — esa rama sólo tiene su 0-bis (`749c11e`), sin PR — y §15/§16 lo declaran en vez de forzar la atribución que el encargo previó.

Hallazgo declarado: la etapa de retadores cierra con **cero `VENCE` puro** entre 18 celdas-D con dictamen (`NADIE-VENCE`×5, `NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO`×2, `PROPUESTA-CON-RESERVA`×2, `FALSADOR-DEBIL`×6, `SIN-CANDIDATO-SUPERIOR`×3). Las tres condiciones de la regla de salida de θ (`FP-…-8a1f-06`) están satisfechas, pero el retiro de código de `g()`/`Theta.valor` no ha corrido — `NC-…-fa47-02`.

Un agente de sólo lectura ayudó a localizar comandos y citas para las 32 afirmaciones de §15; este ejecutor volvió a correr cada uno antes de citarlo (`tests/test_estado_derivado.py`, nuevo, VERDE 32/32).

Suite: `python3 tests/check.py --rapido` → VERDE, 0 FAIL (tras escribir la entrada de `canon/gobernanza-v1_15.md` antes de que `T15` reclamara la cita al propio ADR — mismo defecto que ya documentó `ADR-260922-GEN2-ESTADO-V15-1-7e23-01`). `tests/test_cierre_acto.py` y `tests/test_tuberia_ids_union.py` (fixtures renombrados a `v1_16`) VERDE, sin regresión.

Perímetro respetado. Cero microdato, cero contadores del programa movidos (`cuenta_gen2 = NO-APLICA`). Tres piezas quedan `NC` (retiro de código de θ, puntero público README/docs fuera de perímetro, confirmación en vivo de GitHub Pages) — ver `## NO-CORRIDO / RESERVAS` del encargo archivado.
