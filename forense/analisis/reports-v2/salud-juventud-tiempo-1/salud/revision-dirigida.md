# Revisión dirigida · salud física

27/sep/2026 · lectura completa del original en bloques 1–150, 151–220 y 221–285; mapa de 39 filas leído por CSV. Trece afirmaciones materiales compuestas o repetidas fuera de ese mapa se añadieron en `decisiones-editoriales.json` como `EX01–EX13`. Productor: `python3 forense/analisis/reports-v2/salud-juventud-tiempo-1/salud/producir.py`; verificador: `python3 forense/analisis/reports-v2/salud-juventud-tiempo-1/salud/verificar.py`.

## Comparaciones y mecanismos revisados a mano

| Objeto | Resolución |
|---|---|
| Impuesto a refrescos | Compras del panel urbano vs contrafactual modelado. No ingesta ni efecto clínico; heterogeneidad por ingreso no demuestra beneficio de salud. |
| Etiquetado | Reformulación de productos, ventas y compra declarada son desenlaces separados. Coincidencia temporal no identifica por sí sola todo efecto. |
| Consultorio adyacente a farmacia | 2022 y 2024 tienen cambio de catálogo `u0201`; se cita el piso 2024 con reserva, sin inferir caída real. No se transporta proporción entre utilizadores a consultas mensuales nacionales. |
| Necesidad y búsqueda por sexo | Denominadores distintos; la brecha en búsqueda condicional no mide gravedad, permiso laboral ni machismo. |
| Alcohol, vapeo y opioides | Ventana de doce meses frente a alguna vez; vapeo 2016 tiene filtro; comparabilidad de opioides con ola reservada queda sin acreditar. No se crea serie de olas incompatibles. |
| Sustancias y violencia | Prevalencia, tratamiento, decomisos y tráfico tienen unidades distintas. No se imputan cifras reservadas de 2025. |
| Herbolaria y curandero | Uso doméstico, alguna vez, frecuente y lugar de última atención no son equivalentes. |

La segunda lectura cambió cuatro juicios preliminares de `ROMPE` a `MATIZA`: coincidencia prohibición–vapeo, narrativa esencialista, posposición masculina y beneficio clínico del impuesto por ingreso. Su evidencia disponible limita la inferencia, pero no refuta empíricamente la versión precisa de esas proposiciones. Resultado final: cero `ROMPE` defendibles; no se fabricó una para llenar una cuota.

La consulta `python3 tools/consulta.py result RESULT-ENSANUT-PISOS-SALUD-ATENCION-CONSULTORIO-FARMACIA-2022-TOTAL-TODOS-P` devolvió `NO-ENCONTRADO` en la vista derivada. El RESULT está en la tabla sellada; `cifras.json` fija fila, identificador y SHA-256 de `resultados.json`. Esta anomalía de vista no se convierte en rechazo de la cifra adoptada ni se corrige fuera del perímetro.
