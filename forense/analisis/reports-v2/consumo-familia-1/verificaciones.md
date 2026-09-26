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
