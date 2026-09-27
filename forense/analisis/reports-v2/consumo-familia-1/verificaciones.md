# Verificación final del lote

EJECUTADO sobre base main incorporada `2c646cba93eebc9189a8135a5369bb45e8d29b89`, comprobada con fetch al cierre.

```text
{"report": "consumo", "afirmaciones": 213, "mapa": 38, "cifras": 22, "fuentes": 5}
{"report": "familia", "afirmaciones": 120, "mapa": 51, "cifras": 9, "fuentes": 6}
VERDE: cobertura, cifras, referencias y estados; revisión sustantiva humana requerida
AUTOPRUEBA VERDE: cifra sin fuente y fila vetada rechazadas en copia temporal
```

`python3 tests/check.py --rapido`: baseline 0 FAIL / 529 WARN; entrega 3 FAIL / 531 WARN. Los WARN adicionales son la propuesta propia y el recibo externo pendiente, no adjudican. Salida de fallos íntegra:

```text
  FAIL (3)
────────────────────────────────────────────────────────────────────────
  · T02: 3
      nombre normalizado colisiona: forense/analisis/astra5-genero-endireh/recibo-para-claude.md · forense/analisis/reports-v2/consumo-familia-1/recibo-para-claude.md
      nombre normalizado colisiona: corpus/reports-v2/La_familia_mexicana_como_sistema_psicológico__entre_el_afecto__la_obligación_y_la_adaptación_económica.md · corpus/reports/La_familia_mexicana_como_sistema_psicológico__entre_el_afecto__la_obligación_y_la_adaptación_económica.md
      nombre normalizado colisiona: corpus/reports-v2/Psicología_del_Consumidor_Mexicano__Patrones__Contradicciones_y_Estrategia.md · corpus/reports/Psicología_del_Consumidor_Mexicano__Patrones__Contradicciones_y_Estrategia.md

════════════════════════════════════════════════════════════════════════
  3 FAIL · 531 WARN
════════════════════════════════════════════════════════════════════════
```

Los tres FAIL son nombres obligatorios distintos por ruta, con contenido diferente y enlaces completos. No falla un valor, estado, sello ni regla de trazabilidad; T02 no reconoce la identidad por ruta de los reports v2 y recibos. Se declara la discrepancia conforme AGENTS.md, sin modificar test ni CI fuera del perímetro. Sucesor: integración global C3 debe resolver la convivencia v1/v2 y recibos ante T02; este PR no simula verde global. No se exige a mesa una decisión de implementación para entregar el lote.

`git diff --check`: sin errores. Sello del cuerpo previo y hashes embebidos preservados. Sólo se añaden las secciones de cierre al encargo después de abrir el PR. Guard del HEAD remoto se ejecuta tras último push y se reporta en la entrega.

## Sync posterior a #1170 · 26/sep/2026

EJECUTADO por instrucción posterior de mesa: #1170 fusionó en `4043b1528e40eb16f7ba561c5b1f6f2f7981a809`. Fetch de main e incorporación mediante merge `283eabcd`. Único conflicto en INFRAESTRUCTURA, resuelto conservando las secciones de ambos lotes; referencia propia de tablas ajustada a nombres reales con prefijo de carril. No se modifica el cuerpo del encargo ni sus sellos, ni se reescriben resultados históricos.

EJECUTADO: verificador de consumo/familia con autoprueba VERDE; cobertura/cifras sin cambios. Suite rápida del nuevo main: 0 FAIL, 560 WARN. El reconocimiento de reports-v2 por ruta ya incorporado en main resuelve los tres T02 anteriores; no fue necesario añadir un parche propio a tests/check.py ni workflows. Diff propio contra origin/main sin errores de espacios; las líneas heredadas de main se conservan.

El corte editorial original se mantiene para fuentes y tesis. El sync integra estado operativo posterior, sin reinterpretar la literatura ni convertir reglas propuestas en adoptadas. C1 y recibo técnico externo permanecen distintos de CI. El informe previo de tres T02 describe el corte histórico y queda superado por esta comprobación.

EJECUTADO: `python3 tests/check.py --baseline --parallel` sobre merge de main `283eabcd890363b2f234e5750643ca45fd9da17d` termina exit 0: `LÍNEA BASE: VERDE — sin FAIL nuevos frente a tests/baseline.json (HEAD congelado 7100cd0317132b1f4513b2efdc04058fd7ae89a2)`. Permanecen tres FAIL heredados T06/T08; T02 pasa. No se congela ni modifica baseline. La comparación preparatoria anterior se interrumpió cuando se confirmó la fusión de #1170 y no se utiliza como veredicto. CI remoto sobre último push se comprueba por GitHub; su resultado se comunica en la entrega.
