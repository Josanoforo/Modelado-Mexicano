# Cierre local · Civismo · 27/sep/2026

**EJECUTADO:** homónimo v2 completo y tabla reproducible con 43/43 afirmaciones del mapa, tres desdobles y catorce cláusulas materiales adicionales; revisión manual de ROMPE, tres reglas analíticas propuestas y auditoría final. El reporte permite distinguir cuatro objetos que el v1 mezclaba: confianza institucional, apoyo a la democracia, participación electoral y legitimidad/motivo individual.

**Sostiene:** ENVIPE 2025 muestra cifra negra alta para delitos de 2024, el estudio muestral INE 2024 describe diferencias de participación por sexo y Latinobarómetro registra el cambio en apoyo declarado. **Cambia:** el 59.8% muestral de INE no reemplaza el 61.04% del cómputo presidencial; el 12.86% judicial del v1 se retiene sólo como frase histórica no identificada por cargo/corte; una comparación electoral no prueba motivos ni identidad de electores; «ni broker» es una frase histórica retirada por FP-57 y contradicha en su universalidad por investigación de 2025.

**LEÍDO:** original completo, mapa v1.1, memoria operativa, especificación `CALC-ENVIPE-DENUNCIA-SEGURO-0001`, consultas de dos RESULT, decisión del momento 08 en `decisiones.tsv:292`, fuentes primarias en `fuentes.md`. **NO-VERIFICADO:** panel de los mismos electores; mecanismo causal de confianza, denuncia o voto; base primaria de linchamientos; cifra judicial con cargo y corte; magnitudes comparativas de polarización. **PROPUESTO-POR-EJECUTOR:** reglas CIV-P1 a P3, sin adopción.

**Reservas materiales:** no se abrió ni usó ENVIPE 2026; las cifras externas quedan como evidencia externa. Los dos RESULT de denuncia por seguro tienen sello coincidente y grano delito/robo total de vehículo, validación independiente no hecha y `n_usos=0`; la decisión del momento 08 impide convertirlos en la regla previa de persona/ENIGH. Se usan sólo de modo provisional y descriptivo. El entorno documental CLI fue declarado INDETERMINADO por `tools/entorno.py --arranque` en la sesión responsable; ningún microdato se abrió en este subproducto.

**Comandos ejecutados:**

```text
python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/civismo/producir.py
python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/civismo/verificar.py
python3 tools/consulta.py result RESULT-ENVIPE-SEG-CON-P-DENUNCIA
python3 tools/consulta.py result RESULT-ENVIPE-SEG-SIN-P-DENUNCIA
```

**Resultado de control:** 43 filas del mapa y diecisiete adicionales, cobertura exacta, dos RESULT existentes y sellados, reserva declarada; verificador dirigido VERDE. Falta recepción independiente de mesa; este subproducto no la presume.
