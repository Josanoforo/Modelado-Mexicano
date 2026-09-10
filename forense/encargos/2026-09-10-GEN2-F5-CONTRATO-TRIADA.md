# ENCARGO · ACTO GEN2-F5-CONTRATO-TRIADA

Recibido en mesa 10/sep/2026 (despacho 2/5 de la batería que la firma de
mesa pidió el 9/sep — "necesito que midas al menos 5 encargos a correr en
claude code... dame 5 completos"). Texto verbatim del lanzamiento:

> ENCARGO 2/5 · ACTO GEN2-F5-CONTRATO-TRIADA
>
> FIJAR QUÉ SIGNIFICA «RENDIR MÁS» ANTES DE MIRAR EL PODIO
>
> OBJETIVO: congelar el contrato de comparación entre L_SOLO, L_CORPUS y M antes de calcular la tríada.
>
> CABECERA: NUBE, Opus. Cero microdato, cero captura, cero cálculo de errores finales.
>
> COMPUERTA: PR #674 fusionado y `PLAN-DE-OBRA-GEN2-v1_1` vigente. Puede correr en paralelo con ENCARGO 1/5.
>
> FIRMA DE MESA, OBJETO EXPLÍCITO:
> La afirmación central que este contrato debe poder adjudicar es: en el mismo panel y contra el mismo árbitro, cuál rinde mejor entre LLM solo, LLM con corpus y motor. TRANSFERENCIA queda secundaria. R es árbitro, no contendiente. B es diagnóstico, no contendiente. M no puede calibrarse contra los resultados del panel después de congelar este contrato.
> Esta firma sustituye para el siguiente duelo la prioridad anterior de TRANSFERENCIA como pregunta primaria. No reescribe la spec histórica F5 v1.0; nace una spec sucesora.
>
> P1 · UNIVERSO
> Marco inicial:
> `marco-M-sorteado-v1_3.tsv`, 14 celdas.
> Derivar y congelar tres conjuntos:
>
> * `U0`: 14 celdas del marco.
> * `UR`: celdas con árbitro R válido, sellado y de identidad compatible.
> * `U3`: intersección de `UR` con punto válido de L_SOLO, L_CORPUS y M.
>
> `U3` se fija antes de calcular errores.
> No se elimina una celda porque produzca un error grande.
> Una celda M que consuma directa o indirectamente el mismo resultado R usado para evaluarla queda `CONTAMINADA-POR-OBJETIVO` y fuera de `U3`. Una calibración independiente no equivale automáticamente a contaminación; documentar la cadena exacta.
>
> P2 · PRODUCTO DE CADA CONTENDIENTE
> L_SOLO y L_CORPUS: conservar `k=8`. La agregación por celda sigue la regla histórica ya sellada para F5; no elegir promedio, mediana o mejor réplica después del resultado.
> Para la primaria operacional, una captura que el extractor validado declare `NO-EXTRAIBLE` cuenta en cobertura. No se sustituye por cero ni se descarta silenciosamente.
> M: un punto por celda, procedente del snapshot sellado del ENCARGO 4/5.
> R: un punto árbitro por celda con su incertidumbre y diseño disponibles. R nunca entra al ranking.
>
> P3 · MÉTRICA PRIMARIA
> Todo en puntos porcentuales.
> Para cada celda:
> `error_X,i = |predicción_X,i - R_i|`
> para `X ∈ {L_SOLO, L_CORPUS, M}`.
> Resumen primario por contendiente:
> `MAE_X = media(error_X,i)` sobre el mismo `U3`.
> Comparaciones pareadas:
> `Δ(A,B) = media(error_A - error_B)`.
> Negativo favorece A.
> Las tres comparaciones son obligatorias:
>
> 1. L_CORPUS vs L_SOLO.
> 2. M vs L_SOLO.
> 3. M vs L_CORPUS.
>
> Ninguna puede omitirse porque otra ya parezca contestar la pregunta.
>
> P4 · INCERTIDUMBRE Y BANDA
> Reutilizar, si técnicamente aplica sin alterar su significado, el procedimiento pareado bootstrap ya sellado por F5/B-bis:
>
> * mismas celdas en cada réplica;
> * mismos índices de remuestreo para los tres contendientes;
> * 10,000 réplicas;
> * semilla heredada si el procedimiento ya la fija;
> * IC95.
>
> Mesa fija antes del resultado `δ = 0.5 pp` como banda práctica para las comparaciones de la tríada, por continuidad con el contrato F5 ya sellado.
> Escala pareada exhaustiva:
>
> * `A-GANA`: IC95 de Δ(A,B) completamente < `-0.5 pp`.
> * `B-GANA`: IC95 completamente > `+0.5 pp`.
> * `EMPATE-PRACTICO`: IC95 completamente dentro de `[-0.5,+0.5]`.
> * `INCONCLUSO`: cualquier otro caso.
>
> Escala global:
>
> * `GANADOR-TRIADA-X`: X gana sus dos comparaciones contra los otros contendientes y no tiene menor cobertura de celdas que ellos.
> * `SIN-GANADOR-UNICO`: ningún contendiente satisface lo anterior.
> * `NO-ADJUDICABLE-POR-CONTROL`: identidad, contaminación o cobertura rompe la comparación.
>
> El ranking puntual de MAE se reporta siempre, aunque la escala global sea inconclusa.
>
> P5 · COBERTURA
> Reportar sobre `U0` y `UR`, no sólo sobre éxitos.
> Por contendiente:
>
> * celdas elegibles;
> * celdas con punto;
> * réplicas L válidas;
> * abstenciones/no-extraíbles;
> * contaminaciones;
> * exclusiones y motivo.
>
> Prohibido proclamar ganador operacional usando únicamente la intersección exitosa si el supuesto ganador tiene peor cobertura que un rival.
>
> P6 · TRANSFERENCIA, SECUNDARIA
> Conservar la pregunta de transferencia como secundaria.
> L_CORPUS mantiene los cortes temporales ya congelados.
> M sólo entra a esa secundaria en una celda si su información disponible cumple un corte comparable. Si no, se dice `M-NO-COMPARABLE-EN-TRANSFERENCIA` para esa celda.
> La transferencia no veta ni reemplaza la primaria operacional.
>
> P7 · B
> B puede aparecer al final como piso diagnóstico.
> No entra a:
>
> * `U3`;
> * ranking de tres;
> * adjudicación;
> * condición de ganador;
> * veto.
>
> PERÍMETRO: nueva spec sucesora de tríada, sidecar, nota de decisión, 0-bis, cascada.
> NO TOCA: capturas, extractor, M, R, `milpa/`, CALC históricos.
> CONTADOR: cero.
> CIERRE: merge de esta spec = firma del contrato.
> SUCESORES: ENCARGO 3/5, ENCARGO 4/5 y finalmente ENCARGO 5/5.

## NO-CORRIDO / RESERVAS

| NC | Qué no se corrió | Razón | Impacto | Sucesor |
|---|---|---|---|---|
| NC-0143 | Cierre de la membresía final de `U3` (intersección de `UR` con punto válido de `L_SOLO`, `L_CORPUS` y `M`) | `DECISIÓN-DE-MESA-PENDIENTE` — dos de las tres condiciones de entrada de `U3` dependen de insumos que no existen aún al congelar este contrato: (1) extractor de `valor_extraido` validado contra el formato real de `corridas-L/*__v1_3.json` (`NC-0142`, sigue `ABIERTA`); (2) snapshot sellado de `M` de `ACTO GEN2-ENCARGO-4/5`, no ejecutado todavía | `U3` queda con su regla congelada y su techo (`|U3| ≤ 6`, las 6 celdas de `UR`) pero sin membresía final — ningún ranking ni adjudicación de la tríada puede correr hasta que esta fila cierre | Acto sucesor que resuelva `NC-0142` (extractor validado) + `ACTO GEN2-ENCARGO-4/5` (snapshot de `M`); el ejecutor de P2 bajo este contrato (presumiblemente `ENCARGO 5/5`) cierra esta fila derivando `U3` en firme |

Las siete piezas del encargo (P1–P7) se ejecutaron enteras dentro de lo
que este acto podía derivar sin los dos insumos pendientes: la regla
completa y ejecutable de cada pieza queda congelada; lo no corrido es,
puntualmente, la membresía final de `U3` (dentro de P1) — no una pieza
completa omitida.

## CONSUMIDO

`ACTO GEN2-F5-CONTRATO-TRIADA` — **CONSUMIDO**. Ejecutado por `PR #675`
(rama `claude/determined-faraday-io36oz`, contra `origin/main = eab46ed`,
`PR #674` ya fusionado). Producto: `forense/prereg-duelo-v2/F5-contrato-triada-spec-v1_0.md`
(spec sucesora) + `forense/prereg-duelo-v2/universo-triada-v1_0.tsv`
(sidecar) + `forense/notas/2026-09-10-GEN2-F5-CONTRATO-TRIADA-decision.md`
(nota de decisión). Cascada: `ADR-449` (`canon/gobernanza-v1_15.md`), `L0`
(`canon/estado-programa-v1_12.md`), rótulo `GEN2-F5-CONTRATO-TRIADA`
censado (`canon/registro-rotulos.tsv`), `NC-0143` (`ABIERTA`, sucesor
declarado). `tests/check.py --baseline` → 3 FAIL · 1688 WARN, LÍNEA BASE
VERDE.
