# GEN2-F5-COMPLETA · cierre

**Resultado:** Claude Opus completó las 224/224 posiciones nuevas y la tríada
termina `SIN-GANADOR-UNICO` sobre `U3=12/14`. No se adopta ningún brazo y F6 no
procede. `CALC-TRIADA-0002` quedó sellado y reproduce en contexto idéntico.

## Embudo e identidad

- Cliente: Claude Code `2.1.267`; alias solicitado `opus`; competidor canónico
  acreditado por los sobres exitosos: `claude-opus-5`.
- 224 capturas `OK`: 171 estimaciones numéricas, 53 abstenciones válidas,
  0 errores técnicos finales, 0 malformadas y 0 errores de identidad.
- Las 30 posiciones que inicialmente toparon el límite semanal se reanudaron
  exactamente; las 194 `OK` previas no se reemplazaron y los antecedentes 429
  permanecen en las capturas reanudadas.
- `L_CORPUS` queda sin punto en `DIN-M-01` y `TRA-M-07` porque sus 16/16
  respuestas se abstuvieron válidamente. Esto abre `NC-0152`; no se imputa.

## Cobertura y tabla final

Cobertura con punto: `L_SOLO=14/14`, `L_CORPUS=12/14`, `M=14/14`. La
intersección congelada es `U3=12`: CIV-M-01/02/04/10/12/13, FAM-M-01/05/06/07
y TRA-M-02/03. `v/8` indica réplicas numéricas válidas.

| Celda | R | L solo (v/8) | L corpus (v/8) | M |
|---|---:|---:|---:|---:|
| CIV-M-01 | 25.90% | 23.50% (8/8) | 25.00% (8/8) | 29.43% |
| CIV-M-02 | 24.34% | 27.50% (8/8) | 24.00% (8/8) | 29.43% |
| CIV-M-04 | 24.37% | 25.50% (8/8) | 25.00% (8/8) | 29.43% |
| CIV-M-10 | 20.49% | 23.00% (8/8) | 23.00% (8/8) | 29.43% |
| CIV-M-12 | 20.81% | 22.00% (8/8) | 24.00% (8/8) | 29.43% |
| CIV-M-13 | 19.46% | 21.25% (8/8) | 22.00% (8/8) | 29.43% |
| DIN-M-01 | 15.56% | 18.00% (2/8) | — (0/8) | 17.48% |
| FAM-M-01 | 55.72% | 30.00% (5/8) | 30.00% (1/8) | 45.77% |
| FAM-M-05 | 4.75% | 5.00% (8/8) | 4.75% (8/8) | 4.57% |
| FAM-M-06 | 4.73% | 5.00% (8/8) | 5.00% (8/8) | 4.57% |
| FAM-M-07 | 4.38% | 5.00% (8/8) | 5.00% (8/8) | 4.57% |
| TRA-M-02 | 12.60% | 15.00% (4/8) | 15.00% (1/8) | 8.51% |
| TRA-M-03 | 4.45% | 10.50% (6/8) | 12.00% (6/8) | 8.51% |
| TRA-M-07 | 7.18% | 10.00% (2/8) | — (0/8) | 8.51% |

## Adjudicación primaria

Sobre el mismo `U3=12`, los MAE son `L_SOLO=3.957362 pp`,
`L_CORPUS=3.889026 pp` y `M=4.986673 pp`.

- `L_CORPUS - L_SOLO`: -0.068336 pp, IC95 [-0.788343, 0.577497],
  `INCONCLUSO`.
- `M - L_SOLO`: +1.029311 pp, IC95 [-2.825633, 3.933770], `INCONCLUSO`.
- `M - L_CORPUS`: +1.097647 pp, IC95 [-2.798037, 3.906318], `INCONCLUSO`.

Ningún brazo gana sus dos comparaciones: veredicto final
`SIN-GANADOR-UNICO`. Transferencia conserva el resultado secundario
`SIN-UNIVERSO` del contrato vigente porque las 14 celdas son
`M-NO-COMPARABLE-EN-TRANSFERENCIA`; no bloquea la primaria.

## Sello y reproducción

`CALC-TRIADA-0002` declaró 27 RESULT y `cuenta_gen2=SI` con objeto explícito.
Secuencia: preflight `VERDE`, run `exit=0`, verify `REPRODUCE` con
`CONTEXTO=IDENTICO`. Sello SHA256:
`e0e7c229db9aca39e7dfe117ed1081bfe3f53b973ad0a73100ac6849a55c26b8`.
El recibo estructurado quedó en `forense/replay-evidencia.tsv`.

La escritura de vistas corrida0 se intentó tanto con replay en vivo como desde
los recibos. `NC-0094` detuvo ambas antes de escribir porque habrían cambiado
evidencia de 28/32 corridas ajenas al lote. Se conserva la coordinación pedida
con el lote 08: este acto aporta el recibo estructurado propio y no autoriza ni
duplica cambios globales ajenos.

## Reservas preservadas

- La spec narrativa dice semilla de orden `20260910`; plan, runner e
  identidades congeladas usan `42`. Mandó el listado exacto del plan. Fue una
  permutación determinista, no contrabalanceo estricto; no se reescribe tras
  observar resultados.
- El manifiesto del corpus declara dónde la evidencia directa fue insuficiente;
  entregar contexto no equivale a afirmar que contiene la respuesta exacta.
- El cierre parcial se conserva como historia del bloqueo por cuota. La nueva
  ejecución no borra sus sobres ni convierte abstenciones en fallos.
- NC-0146 y NC-0147 cierran; NC-0152 conserva el único residual sustantivo.
