# Lanzamiento · revisión de candados GEN1 → GEN2 posterior a #701

Fecha de carga: 11/sep/2026 UTC. Base de integración comprobada: `origin/main=07f15461e601eb9d88220dbd0836340ff76b36d2` (merge #701). El paquete conserva la revisión, la sonda, su salida y los tres encargos entregados por mesa. La única normalización editorial aplicada al material fuente fue usar dos veces el rótulo completo `GEN2-E0`, conforme a T25. #701 concilió la adenda de publicación; no modifica el código objeto señalado por las sondas.

## Contenido

| Archivo | Función |
|---|---|
| [Revisión de candados](REVISION-CANDADOS-GEN1-GEN2-2026-09-11.md) | Dictamen, evidencia, límites y orden de trabajo. |
| [Sonda adversarial](PRUEBAS-CANDADOS-GEN2.py) | Reproduce los huecos observados sin escribir en el árbol científico. |
| [Resultado de la sonda](RESULTADOS-PRUEBAS-CANDADOS-GEN2.json) | Salida histórica obtenida sobre el SHA declarado en el propio JSON. |
| [17 · Linaje y adopción](17-GEN2-LINAJE-Y-ADOPCION.md) | Clasificación de origen y aptitud por uso; contrato común para 18/19. |
| [18 · Motor y herencia explícita](18-GEN2-MOTOR-Y-HERENCIA-EXPLICITA.md) | Emisión GEN2 explícita y cobertura verificable. |
| [19 · Evaluación sin fugas](19-GEN2-EVALUACION-SIN-FUGAS.md) | Calculador sucesor, clausura de inputs y evaluación protegida. |

Los encargos 17–19 son autocontenidos: cada uno incluye resultado útil, fases, perímetro, aceptación, autorización operativa, pruebas y cierre. Los nombres de rama declarados en sus cabeceras no colisionaban con ramas remotas al momento de esta carga.

## Orden y concurrencia

17 puede comenzar inmediatamente. 18 puede levantar su mapa en paralelo, pero integra el contrato de linaje de 17 antes de cerrar el recorrido ejecutable. 19 puede avanzar pruebas y diseño en rutas nuevas; una evaluación de M renovado espera el contrato de 17 y el snapshot elegible de 18. No ejecutar nuevas capturas o llamadas a modelos desde este paquete.

Nombres sugeridos para distinguir las sesiones CLI:

- `gen2-17-linaje-adopcion`
- `gen2-18-motor-herencia-explicita`
- `gen2-19-evaluacion-sin-fugas`

## Prompt de lanzamiento

```text
Ejecuta el encargo adjunto completo en Josanoforo/Modelado-Mexicano.
Actualiza contra origin/main y comprueba ramas, worktrees y PR del mismo objeto.
Continúa todas las fases cuyas compuertas estén cumplidas; no pares en un plan.
Usa un worktree y rama propios; entrega commits, push y PR revisable.
Yo hago el merge. Conserva la historia GEN1, los artefactos congelados y las
decisiones ya asentadas. Ninguna etiqueta, sello o firma de contador sustituye
el linaje, la aptitud para el uso ni la separación de evaluación.
```

Al continuar entre sesiones, retomar rama/PR/SHA y fases pendientes; no reiniciar la misma tarea ni usar el resultado JSON como oráculo del comportamiento corregido.
