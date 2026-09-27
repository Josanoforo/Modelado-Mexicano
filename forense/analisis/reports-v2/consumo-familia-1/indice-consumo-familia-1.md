# Lote consumo y familia · reports v2

EJECUTADO: dos reports terminados, con evidencia por afirmación y reglas propuestas. Corte fijo: `2c646cba93eebc9189a8135a5369bb45e8d29b89`. Cero mediciones, cero adopciones nuevas. La cobertura incluye repeticiones entre mapa y complemento del original; no es un conteo de tesis independientes ni una tasa de refutación.

| Carril / tabla | Registros cobertura | Mapa | CONFIRMA | MATIZA | ROMPE | SIN-CIFRA | Cifras | Fuentes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [consumo](consumo/consumo-afirmaciones.json) | 213 | 38 | 0 | 79 | 0 | 134 | 22 | 5 |
| [familia](familia/familia-afirmaciones.json) | 120 | 51 | 0 | 49 | 6 | 65 | 9 | 6 |

Reports: [consumo](../../../../corpus/reports-v2/Psicología_del_Consumidor_Mexicano__Patrones__Contradicciones_y_Estrategia.md) · [familia](../../../../corpus/reports-v2/La_familia_mexicana_como_sistema_psicológico__entre_el_afecto__la_obligación_y_la_adaptación_económica.md).

Cada carril entrega `<carril>-afirmaciones.json`, `<carril>-cifras.json`, `<carril>-fuentes.json`, `<carril>-cobertura-v1.json` y su constancia de lectura/corte. Cifras v1 en la tabla son objetos históricos auditados, no cifras respaldadas. Fuentes externas no reciben RESULT ficticio. Las tablas selladas se citan con localizador y hash; el atraso de las vistas no se confunde con falta de medición. No se promedian estimandos distintos.

Comprobación y autoprueba:

```bash
python3 forense/analisis/reports-v2/consumo-familia-1/verifica_lote.py --autoprueba
```

El control verifica procedencia, cobertura, estados, valor exacto de los RESULT registrados y rechazo de referencias vetadas. No decide validez causal ni fuerza de una cita; la revisión sustantiva dirigida está en la nota y el recibo. Las cifras redondeadas en prosa se cotejaron con sus registros; el control no certifica una detección universal de toda magnitud escrita con palabras.

[Reglas propuestas](hoja-reglas-propuestas.md) · [recibo para Claude](recibo-para-claude.md) · [arranque](arranque.md). C1 no bloquea este lote; una discrepancia material exige corregir sólo las afirmaciones afectadas. No se modifica índice global ni catálogo.
