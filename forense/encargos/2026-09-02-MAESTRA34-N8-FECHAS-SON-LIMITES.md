ENCARGO · ACTO MAESTRA34-N8 · FECHAS-SON-LIMITES — invoca /acto
SHA de redacción: df26d3a (merge PR #461). Redacta dirección (Fable), 2/sep/2026, contra v2.12. Estado: LISTO PARA LANZAR.
ENTORNO ASIGNADO: NUBE. NO se lanza en UBUNTU. MODELO SUGERIDO: Sonnet (propagación mecánica de una firma).
CARRILES: MAESTRA34-L4 corre en caja (data/, curacion-registro, propuesta) — disjunto. COMPUERTA: ninguna.

FIRMA DE MESA — verbatim, 2/sep/2026: «vi en una conversación que una fecha no se había "vencido" eso no debe ser algo que detenga nuestro progreso, la fecha es un límite y si procesamos algo antes está bien no quiero que ahora eso se vuelva algo que detenga nuestro progreso porque la fecha no ha llegado.» Regla que se propaga: una fecha en un encargo o en el tablero es `vence` (límite superior), nunca compuerta; `NO-LANZAR-ANTES-DE` queda prohibido como tipo de compuerta. Defecto medido: MAESTRA34-E1 (encolado por PR #457) trae esa compuerta y /despacha §2-bis (PR #460, l.275-277) la reconoce como válida — ambos de dirección, no del ejecutor.

A.8 contra df26d3a: .claude/commands/despacha.md §2-bis l.275-277 → EXISTE-NO-SATISFACE (acepta fecha como compuerta). forense/encargos/cola/2026-09-08-MAESTRA34-E1-REVISION-FALSADORES.md l.13 → EXISTE-NO-SATISFACE (compuerta por fecha). instrucciones-proyecto-v2_12.md: `grep -c "NO-LANZAR-ANTES-DE\|compuerta.*fecha"` → pega la salida (dirección: 0, la regla no está escrita en instrucciones; no se sube versión por esto — va a hallazgos y a las dos piezas).

P1 · /despacha §2-bis: elimina la fecha como tipo de compuerta; en su lugar, si el encargo trae `vence:` o una fecha de ejecución propuesta, /despacha la reporta como límite («propuesto 8/sep; hoy 2/sep: se ejecuta») y NO la usa para saltar el encargo. Cita esta firma y el defecto.
P2 · Enmienda fechada al pie de la cola de E1 (A.3, verbatim intacto): «COMPUERTA (sustituye): digesto del día existente en forense/digesto/. La fecha 2026-09-08 pasa a ser `vence`, no compuerta. Ejecutable desde hoy.» Renombra el archivo a 2026-09-02-… solo si /despacha ordena por nombre y eso lo dejaría al final indebidamente — si no, no lo toques y explícalo.
P3 · hallazgos.md una línea; tablero: FP-226 `vence` intacto (8/sep) con nota «ejecutable antes»; recibo.
PERÍMETRO: .claude/commands/despacha.md (§2-bis) · forense/encargos/cola/…E1… (pie) · forense/hallazgos.md · tablero · A.3 · cascada. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR: deriva al arrancar. CONTADOR: cero directo, declarado. LO QUE NO HACE: no ejecuta E1; no sube versión de instrucciones.
