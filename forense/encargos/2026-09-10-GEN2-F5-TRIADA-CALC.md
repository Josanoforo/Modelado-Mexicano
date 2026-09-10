# ENCARGO · ACTO GEN2-F5-TRIADA-CALC

Recibido en mesa 10/sep/2026 (despacho 5/5 y último de la batería que la
firma de mesa pidió el 9/sep — "necesito que midas al menos 5 encargos a
correr en claude code... dame 5 completos"). Texto verbatim del
lanzamiento:

> ENCARGO 5/5 · ACTO GEN2-F5-TRIADA-CALC
>
> LLM SOLO vs LLM CON CORPUS vs MOTOR
>
> OBJETIVO: adjudicar la pregunta central del programa sobre una generación común de evidencia:
> ¿qué rinde mejor en el panel sellado: L_SOLO, L_CORPUS o M?
>
> CABECERA: NUBE, Opus. Cero microdato. Cero llamadas nuevas a Claude. Consume exclusivamente productos sellados de 1/5, 2/5, 3/5 y 4/5.
>
> COMPUERTA, POR PRODUCTO:
> Deben existir y verificarse:
>
> 1. extractor L v1.3 + manifiesto de extracción;
> 2. spec TRIADA sellada;
> 3. `UR` congelado y árbitros R sellados;
> 4. snapshot M congelado y firewall por celda.
>
> Si falta cualquiera, PARO. No improvisar sustituto.
>
> FIRMA DE CONTADOR CON OBJETO:
> `cuenta_gen2 = SI para el CALC-TRIADA que este acto selle`.
> El merge perfecciona la firma.
>
> FIRMA DE ADJUDICACIÓN:
> Mesa autoriza aplicar exactamente la escala de la spec TRIADA. La firma autoriza aceptar como salida válida tanto un ganador como `SIN-GANADOR-UNICO` o `NO-ADJUDICABLE-POR-CONTROL`. No existe obligación de coronar a nadie.
>
> P1 · ESPEJO DEL CONTRATO, COMMIT-1
> Crear `CALC-TRIADA-*`.
> Su `spec.yaml` copia por hash, sin reinterpretar:
>
> * `U0`;
> * `UR`;
> * regla para `U3`;
> * 3 contendientes;
> * regla de agregación L;
> * snapshot M;
> * árbitros;
> * MAE;
> * Δ pareados;
> * bootstrap;
> * δ=0.5 pp;
> * cobertura;
> * escala pareada;
> * escala global;
> * secundaria TRANSFERENCIA;
> * rol diagnóstico de B.
>
> Declarar todos los RESULT antes de calcular.
> Como mínimo:
> Cobertura
>
> * `RESULT-TRIADA-U0-N`
> * `RESULT-TRIADA-UR-N`
> * `RESULT-TRIADA-U3-N`
> * cobertura L_SOLO
> * cobertura L_CORPUS
> * cobertura M
> * exclusiones por contaminación/identidad
>
> Primarios
>
> * `MAE-L-SOLO`
> * `MAE-L-CORPUS`
> * `MAE-M`
>
> Pareadas
>
> * Δ L_CORPUS - L_SOLO + IC95 + veredicto
> * Δ M - L_SOLO + IC95 + veredicto
> * Δ M - L_CORPUS + IC95 + veredicto
>
> Global
>
> * ranking puntual 1/2/3
> * `VEREDICTO-TRIADA`
>
> Secundaria
>
> * resultados de TRANSFERENCIA bajo el universo donde sus cortes sean comparables.
>
> Cierra P1 con:
> «El primer resultado producido por este procedimiento es el reportado. No se amplía universo, no se cambia agregación, no se recalibra M y no se vuelve a capturar L después de observar el ranking.»
>
> P2 · CÓMPUTO, COMMIT-2
> Ejecutar:
> `preflight → run → verify`.
> Por cada celda de `U3`, producir una fila durable:
> `id · R · L_SOLO · error_L_SOLO · L_CORPUS · error_L_CORPUS · M · error_M · cobertura/réplicas · firewall · notas de corte`.
> Usar exactamente el mismo conjunto de celdas para los tres MAE.
> Los bootstrap pareados usan los mismos índices de celda en los tres contendientes.
> Prohibido:
>
> * quitar outliers;
> * cambiar a mediana porque la media no gustó;
> * dar más peso a una familia;
> * contar las 8 réplicas como 8 tareas independientes;
> * elegir la mejor réplica;
> * volver a correr un brazo;
> * calibrar M;
> * completar R;
> * modificar extractor;
> * reinterpretar B como cuarto contendiente.
>
> Un defecto material descubierto produce PARO/INCONCLUSO, no una reparación dentro del mismo cómputo.
>
> P3 · VEREDICTO
> La nota de cierre abre con una frase inequívoca:
> RESULTADO PRIMARIO: [GANADOR-TRIADA-L_SOLO / GANADOR-TRIADA-L_CORPUS / GANADOR-TRIADA-M / SIN-GANADOR-UNICO / NO-ADJUDICABLE-POR-CONTROL], sobre `U3 = n` celdas del marco de 14.
> Después:
>
> 1. tabla MAE y ranking puntual;
> 2. tres comparaciones pareadas con IC95 y veredicto;
> 3. cobertura sobre todo `U0`;
> 4. tabla por celda;
> 5. secundaria TRANSFERENCIA;
> 6. B, sólo como diagnóstico si aporta información;
> 7. sensibilidad pertinente ya pre-registrada;
> 8. límites.
>
> P4 · LECTURAS PERMITIDAS
> Si gana L_SOLO:
> En este panel, añadir el corpus no produjo mejor desempeño operacional que usar el LLM solo y el motor tampoco lo superó bajo la regla fijada.
> Si gana L_CORPUS:
> En este panel, el LLM con corpus superó tanto al mismo LLM sin corpus como al motor bajo la regla fijada.
> Si gana M:
> En este panel, el motor superó tanto al LLM solo como al LLM con corpus bajo la regla fijada.
> Si no hay ganador:
> El panel no permite identificar un ganador único bajo la magnitud, incertidumbre y cobertura pre-registradas.
> Ninguna salida autoriza por sí sola:
>
> * causalidad;
> * «todos los mexicanos»;
> * «todos los LLM»;
> * cualquier modelo/versionado futuro;
> * cualquier tarea fuera del marco;
> * declarar que corpus «explica» la diferencia sólo porque L_CORPUS gane;
> * declarar que el motor es universalmente mejor porque gane 14 tareas.
>
> P5 · QUÉ SIGUE SEGÚN EL RESULTADO
> El sucesor no se decide por preferencia por un contendiente, sino por el diagnóstico:
>
> * Si hay ganador único con cobertura suficiente: F6 · COSECHA, informe central con cadena citable.
> * Si L_CORPUS > L_SOLO pero M no se distingue de L_CORPUS: siguiente experimento debe discriminar arquitectura, no hacer más corpus por inercia.
> * Si M > ambos L: siguiente paso es validación prospectiva/holdout, no recalibración retrospectiva.
> * Si L_SOLO ≈ L_CORPUS: investigar utilidad real del acceso documental antes de ampliar corpus.
> * Si `SIN-GANADOR-UNICO`: estudiar la fuente dominante de incertidumbre o ampliar prospectivamente el marco bajo una spec nueva. No añadir celdas a este CALC.
> * Si control/identidad bloquea: sucesor mínimo al defecto concreto.
>
> PERÍMETRO Y CONCURRENCIA
> Toca:
>
> * `data/corrida0/CALC-TRIADA-*/`
> * vistas corrida0 derivadas;
> * `forense/notas/` resultado;
> * `forense/no-corrido.tsv`;
> * `data/corrida0/decisiones.tsv` por firma de contador;
> * 0-bis;
> * cascada.
>
> NO toca:
>
> * capturas;
> * extractor;
> * spec TRIADA;
> * R sellados;
> * snapshot M;
> * `milpa/`;
> * marcador histórico;
> * F5 v1.0;
> * B;
> * corpus.
>
> Si al correr se necesita editar cualquiera de esos inputs, PARO. El contrato estaba incompleto y saberlo es el resultado correcto.
>
> CIERRE
> Orden obligatorio:
>
> 1. resultado primario;
> 2. cifras y universo;
> 3. cobertura;
> 4. pareadas;
> 5. secundaria;
> 6. límites;
> 7. contadores antes/después;
> 8. cascada;
> 9. `## NO-CORRIDO / RESERVAS`;
> 10. `## CONSUMIDO` con PR.
>
> Éste es el acto que debe contestar la pregunta del proyecto. No termina cuando alguien gana. Termina cuando sabemos, con una regla fijada antes del resultado, si L_SOLO, L_CORPUS o M rindió mejor en el panel que decidimos usar.

---

## Compuerta verificada (por producto, contra `origin/main = c439065`)

10/sep/2026, antes de cualquier edición sustantiva. Los cuatro productos
que el encargo exige existen en `origin/main` y se citan por hash:

| # | Producto exigido | Ruta | `sha256` en `origin/main` |
|---|---|---|---|
| 1 | extractor L v1.3 | `tools/extrae_l_v1_3.py` | `ecfbd8491f9b353d9eebdb25f0afa6eddf4f0d3082cff50c3db7d8f5ddd8ff5e` |
| 1 | manifiesto de extracción | `forense/prereg-duelo-v2/manifiesto-extraccion-L-v1_3.json` | `a1e5d609fe0044eef44d3365b308004daeaa8d511f4692464b422e1296e75809` |
| 2 | spec TRIADA sellada | `forense/prereg-duelo-v2/F5-contrato-triada-spec-v1_1.md` | `db6b24c579e72dc705c772200ca2c4066bd9708cc6c06c85c5101d56b081b4f5` (coincide con su `.sha256` sellado) |
| 3 | `UR` congelado (14/14) | `forense/prereg-duelo-v2/universo-triada-v1_4.tsv` | `840fc68ce7261686426221effbf9df313ef17e2876fa6345b3c00589bab80f80` (coincide con su `.sha256` sellado) |
| 3 | árbitros R sellados | 14 `CALC-R-*` citados por el sidecar | 14/14 con `resultados.json` + `sello.json` + `sello.sha256` + `spec.yaml` en `origin/main` |
| 4 | snapshot M congelado + firewall por celda | `forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json` | `b53ac6d51d1b50ce929fdf1b3e14b124c11db39fb216a15d7073a287ed3f065c` (14/14 celdas con `estado_firewall` y `razon_firewall`) |

Comandos: `git cat-file -e origin/main:<ruta>` + `git show origin/main:<ruta> | sha256sum`
para cada fila; para los 14 `CALC-R`, `git cat-file -e` sobre los cuatro
archivos de cada directorio nombrado en la columna `fuente_R` de
`universo-triada-v1_4.tsv`. **COMPUERTA CUMPLIDA — 4/4.**
