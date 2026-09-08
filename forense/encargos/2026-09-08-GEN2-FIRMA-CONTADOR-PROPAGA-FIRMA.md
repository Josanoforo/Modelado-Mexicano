ENCARGO · ACTO GEN2-FIRMA-CONTADOR · TRES FILAS EN decisiones.tsv — el acto cuyo único trabajo es propagar la firma que E5-1 se negó (con razón) a inferir

Cabecera: NUBE, Sonnet (propagación de una decisión dictada; deriva de TSVs y specs del repo, cero microdato) · COMPUERTA: PR #634 fusionado (`git cat-file -e origin/main:data/corrida0/CALC-0003-v2/sello.json`) · redactado contra `4acc1f77` + rama de #634 · candidatos al redactar: ADR-413 · FP-360 · NC-0048 — deriva, no heredes (TABLERO-2 corre en paralelo y también renumera). CONCURRENCIA: UNIVERSO-C (caja) y TABLERO-2 (NUBE) — cero archivos comunes con ambos.

LA FIRMA, con la autoridad, fecha y objeto que el ejecutor de E5-1 exigió — y mesa la dicta al mandar este encargo (mandarlo ES dictarla; el PR fusionado la sella):

FIRMA DE MESA · 8/sep/2026 · conversación de dirección: «cuenta_gen2 = SI para CALC-0001, CALC-0002 y CALC-0003-v2. Los tres reproducen 83/83 y 128/128 tras la reparación del verificador (PR #634); las etiquetas rojas eran del checador, no de las cifras. Esta firma cuenta trabajo sellado en la nómina GEN2 — no compara con GEN1 y no adopta nada al motor.» Contexto que el ejecutor verifica antes de escribir (A.8): FP-356 ABIERTA · las 3 filas de `data/corrida0/decisiones.tsv` con formato fuente = D-N (mesa fecha, ACTO) como precedente de formato · los cuatro CALC hoy en PENDIENTE-DE-MESA.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — contestada por quien redacta, 8/sep, contra `4acc1f77` + rama de #634 ═══

* `git cat-file -e origin/main:data/corrida0/CALC-0003-v2/sello.json` → existe (PR #634 fusionado, `d1a97cd`).
* `grep -c "PENDIENTE-DE-MESA" data/corrida0/decisiones.tsv` sobre CALC-0001/0002/0003-v2 → a verificar por el ejecutor antes de escribir; debe volverse 0 tras P1.
* `grep -rlI "FIRMA SIMULADA" data/ forense/ canon/` → debe ser vacío antes y después del acto (P1 prohíbe simular).
* FP-356 vive en `forense/firmas-pendientes.tsv`; NC-0045/NC-0046 viven en `forense/no-corrido.tsv` — el ejecutor confirma su estado exacto antes de tocarlos.

PIEZAS P1 · Las tres filas, por la vía directa — NUNCA por la simulación. FP-359 dejó declarada la trampa: el procedimiento de control positivo de E5/E5-1 regenera vistas derivadas con la firma simulada y la cascada puede publicarla. Este acto NO simula nada: escribe las tres filas reales en `decisiones.tsv` (objeto: CALC-0001, CALC-0002, CALC-0003-v2 · `cuenta_gen2 = SI` · fuente: esta firma con fecha y este encargo/PR como cita), y SOLO DESPUÉS regenera registro y status una vez, en ese orden, en el mismo commit. En ningún commit del acto existe un estado simulado. Verificación: `grep -c "PENDIENTE-DE-MESA"` sobre los tres CALC → 0; `grep -rlI "FIRMA SIMULADA" data/ forense/ canon/` → 0.

P2 · El contador se mueve y se pega. `corrida0.py status` completo en la nota: esperado `N_corridas_selladas` 0→3 · `N_resultados_sellados` 0→211 (83+128). Si las cifras difieren de las esperadas, se pegan las reales y se explica la diferencia — no se fuerzan (las esperadas vienen de la nota de #634, no de este encargo).

P3 · El registro al día. FP-356 → FIRMADA con esta firma citada · NC-0045/NC-0046 → CERRADAS · T35 se ejerce por primera vez sobre cadena GEN2 real: pegar su salida (es el test que E5-1 escaló a FAIL y que nunca ha mordido nada verdadero — hoy muerde o pasa, y cualquiera de las dos es noticia).

PERÍMETRO: `data/corrida0/decisiones.tsv` · `data/corrida0/{corridas,resultados,usos}.tsv` (re-derivados post-firma) · `forense/{firmas-pendientes,no-corrido}.tsv` · nota · 0-bis · cascada (gobernanza · registro-rotulos · estado-programa §L0 · no-corrido · encargo archivado). No toca sellos, specs, milpa, canon del modelo ni el tablero. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

CONTADOR: éste es el acto que lo mueve — 0→3 corridas, 0→211 resultados.

## NO-CORRIDO / RESERVAS

- **qué:** `tests/test_corrida0.py::t_status_arbol_real_no_cuenta_smokes` (`T-STATUS-SMOKES`) sigue con la premisa pre-firma en su docstring y sus asertos (`N_corridas_selladas==0`, `N_resultados_sellados==0` como «la cifra correcta»); `tests/check.py::t35_repro` (`T35`/`T-REPRO`) muerde por primera vez sobre cadena GEN2 real (211 fail, ramal (a): 211 `RESULT` activos GEN2 sin consumidor en `milpa/`). **por qué:** `FUERA-DE-PERÍMETRO` — actualizar falsadores en `tests/` no está en la lista de este acto, y los 211 fallos de (a) son la cadena de adopción (E.2), que este mismo encargo declara explícitamente que no hace. **impacto:** `python3 tests/check.py --baseline` sale ROJO con 213 entradas nuevas frente a la línea base (211 de T35 + 2 de T-CORRIDA0); ningún consumidor real quedó sin marcar — es la firma la que les dio universo a los tests, no un defecto que la firma introdujo. **sucesor:** `NC-0053` — acto que (a) actualice el falsador `T-STATUS-SMOKES` a los valores post-firma y (b) revise, uno por uno, los 211 casos del ramal (a) de T35 (adopción E.2, cada consumidor de `milpa/` que debiera citar `corrida0_resultado_id` y no lo hace todavía).

Lo que NO hace: no adopta al motor (E.2: adopción humana, por merge, otro día) · no corre delta (B-7, sin implementar) · no toca CALC-0003 v1 (SUPERADO, historia) · no simula absolutamente nada.
