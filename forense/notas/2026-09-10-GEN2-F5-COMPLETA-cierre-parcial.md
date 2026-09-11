# GEN2-F5-COMPLETA · cierre parcial por cuota

> Registro histórico superado por el cierre completo del mismo acto en
> `2026-09-10-GEN2-F5-COMPLETA-cierre.md`. Las 30 posiciones se reanudaron sin
> reemplazar las 194 `OK` y terminaron correctamente.

**Resultado útil:** el corpus sucesor y el diseño completo quedaron construidos,
la sonda aceptó el paquete máximo y se intentaron las 224 posiciones nuevas. El
cliente entregó 194 respuestas y después devolvió 30 fallos técnicos `HTTP 429`
por límite semanal. El análisis observado sobre `U3=12/14` da
`SIN-GANADOR-UNICO`, pero es **provisional**: no cierra NC-0146, no habilita F6
ni adopta ningún brazo. La reanudación exacta queda disponible después del
reinicio de cuota anunciado para **12/sep/2026 11:00 America/Mexico_City**.
El avance está publicado en **PR #687**, deliberadamente sin marca
`CONSUMIDO` y sin merge.

## Qué cambió respecto de PR #681

PR #681 comparó la tríada sobre `U3=3/14`, con preguntas desalineadas y el
paquete v1.0. Este acto usa las 14 preguntas v1.4, crea paquetes pertinentes por
celda sin truncamiento y congela 224 capturas enteramente nuevas porque las tres
ENIGH históricas no acreditaban versión real comparable. Con lo observado sube
la cobertura de punto de `L_SOLO` de 6 a 14 celdas y la de `L_CORPUS` de 3 a 12;
la intersección común sube de 3 a 12. Dos celdas siguen sin punto de
`L_CORPUS` por abstención válida, no por imputación ni por error del extractor.

## Transporte, identidad y desviaciones

- Cliente: Claude Code `2.1.267`; alias solicitado `opus`; herramientas
  deshabilitadas; una vuelta por posición.
- Cada una de las 194 respuestas exitosas reporta en `modelUsage` el modelo
  competidor canónico `claude-opus-5`. El mismo sobre menciona
  `claude-haiku-4-5` como componente interno del cliente; no se lo confunde con
  el competidor. El campo superior `model` ya no existe en este formato, por lo
  que `modelo_reportado=null` en las capturas iniciales es una limitación del
  parser resumido y no ausencia de evidencia en el sobre original.
- Embudo: 224 archivos con identidad correcta; 194 `OK`; 149 puntos; 45
  abstenciones válidas; 30 `ERROR_TECNICO`; 0 malformadas; 0 errores de
  identidad. Los 30 fallos conservaron tres intentos y el sobre original.
- Desviación instrumental: el mensaje nuevo decía `weekly limit`, frase que la
  primera versión del detector no reconoció como parada sistémica. Por eso se
  intentaron las posiciones restantes en lugar de detenerse en el primer 429.
  La corrección posterior reconoce esa frase, conserva antecedentes, retoma
  sólo estados no `OK` y detiene un cambio de modelo.
- Errata del contrato: la frase narrativa de la sección 3 dice semilla de orden
  `20260910`, pero el plan ejecutable congelado, sus 224 identidades y el runner
  usan `42`. El orden real es el listado íntegro de
  `F5-completa-plan-v1_0.json`; no se reconstruye ni se reordena. Fue una
  permutación determinista, no un contrabalanceo estricto por celda. Los 30
  fallos quedaron balanceados 15/15 entre brazos por el orden observado, pero
  distribuidos entre celdas. Esta discrepancia se declara y no se corrige a
  posteriori en los artefactos congelados.
- Ajuste registral postcaptura: `manifiesto.json` se renombró a
  `manifiesto-F5-v2_0.json` porque T02 normaliza basenames y detectó colisión
  con el manifiesto histórico. Sus bytes y SHA256 no cambiaron; por eso el
  plan y las identidades congeladas siguen reproduciendo. La ruta narrativa
  de la spec sellada se conserva como registro histórico de la ruta usada.

## Tabla 14/14 observada

`v/8` es el número de réplicas numéricas válidas. Un guion significa que todas
las respuestas transportadas se abstuvieron o fallaron técnicamente.

| Celda | R | L solo (v/8) | L corpus (v/8) | M |
|---|---:|---:|---:|---:|
| CIV-M-01 | 25.90% | 24.50% (6/8) | 25.00% (7/8) | 29.43% |
| CIV-M-02 | 24.34% | 27.00% (6/8) | 24.50% (6/8) | 29.43% |
| CIV-M-04 | 24.37% | 25.00% (7/8) | 25.00% (8/8) | 29.43% |
| CIV-M-10 | 20.49% | 22.50% (6/8) | 23.00% (5/8) | 29.43% |
| CIV-M-12 | 20.81% | 22.00% (7/8) | 24.00% (8/8) | 29.43% |
| CIV-M-13 | 19.46% | 21.25% (8/8) | 22.00% (8/8) | 29.43% |
| DIN-M-01 | 15.56% | 18.00% (2/8) | — (0/8) | 17.48% |
| FAM-M-01 | 55.72% | 30.00% (5/8) | 30.00% (1/8) | 45.77% |
| FAM-M-05 | 4.75% | 5.00% (7/8) | 4.70% (6/8) | 4.57% |
| FAM-M-06 | 4.73% | 5.00% (7/8) | 5.00% (7/8) | 4.57% |
| FAM-M-07 | 4.38% | 5.00% (6/8) | 5.00% (7/8) | 4.57% |
| TRA-M-02 | 12.60% | 15.00% (4/8) | 15.00% (1/8) | 8.51% |
| TRA-M-03 | 4.45% | 10.50% (6/8) | 12.00% (6/8) | 8.51% |
| TRA-M-07 | 7.18% | 10.00% (2/8) | — (0/8) | 8.51% |

## Lectura provisional

Sobre el mismo `U3=12`, los MAE observados son `L_SOLO=3.7490 pp`,
`L_CORPUS=3.8775 pp` y `M=4.9867 pp`. Ninguna de las tres comparaciones
pareadas demuestra dominancia con la banda práctica de 0.5 pp:

- `L_CORPUS - L_SOLO`: +0.1285 pp, IC95 [-0.5000, +0.6910], inconcluso;
- `M - L_SOLO`: +1.2376 pp, IC95 [-2.6845, +4.1563], inconcluso;
- `M - L_CORPUS`: +1.1092 pp, IC95 [-2.7981, +3.9308], inconcluso.

Es un resultado sobre los datos observados, no una conclusión nacional ni un
ranking autorizante. El nuevo CALC científico no se sella todavía: hacerlo con
30 fallos de cuota convertiría un estado reanudable en una falsa terminación y
obligaría a crear otro sucesor tras el reinicio.

## Continuación exacta

Desde la raíz del worktree y con la misma sesión del cliente:

```bash
python3 forense/prereg-duelo-v2/runner_l_completa.py --correr
python3 tools/calcula_f5_completa.py --escribir
```

El primer comando vuelve a verificar cliente/spec/corpus/plan, omite las 194
capturas `OK`, reintenta sólo las 30 no completas y preserva sus antecedentes.
Después deben comprobarse `224 OK`, recalcular, congelar y ejecutar
`CALC-TRIADA-0002` mediante `preflight -> run -> verify`, y sólo entonces
actualizar NC-0146, contador, decisiones y cascada. NC-0147 sí queda resuelta
instrumentalmente por la tolerancia prospectiva y sus cuatro pruebas de borde.
