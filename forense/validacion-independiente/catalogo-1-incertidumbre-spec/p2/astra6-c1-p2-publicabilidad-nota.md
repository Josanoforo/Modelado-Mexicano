# P2 · Publicabilidad por identidad

REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA. PROPUESTO-POR-EJECUTOR; no adopción.
Worktree `/home/pc0/mm-astra6-c1-incertidumbre-spec-1`, rama
`codex/astra6-c1-incertidumbre-spec-1`, corte inicial `11602de8`, limpio
al comenzar P2. Se escriben exclusivamente archivos de esta pieza.

La fuente humana de ambos umbrales es `spec.md` de
`CALC-ENDIREH-PISOS-2011-MODULOS-0001` (línea 15) y
`CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001` (línea 11), ambas fechadas por
la semilla documental 20260923 y conservadas en el corte del encargo.
No son umbrales oficiales de INEGI ni una regla nueva de esta pieza:
n conocido ≥100, ≥5 UPM con casos, ancho IC ≤0.20 y CV ≤0.30 cuando p>0.
La igualdad pasa. Si p=0 no se exige CV; un denominador ausente o un IC
no calculable no significa p=0. El contrato debe explicitar qué ocurre con
réplicas sin denominador; no hay licencia para elegir solo réplicas favorables.
La clasificación NO-ESTIMABLE de `deriva.py` es propuesta defensiva, no
una adjudicación retroactiva de los once casos.

2011 usa módulos conyugales A/B/C, FAC_PER, estrato EST_DIS, UPM_DIS;
permisos C CP7_1 tienen códigos 1 sí, 2/3 no, otros fuera. El condicionamiento
adicional CP4_1=1/2 está en disputa en sesión01. Denuncia externa se limita
a actos 1–9 y resultado de atención entre quienes acudieron: están en disputa
columnas 1/5 frente a 1–4 y elegibilidad. Por ello seis dictámenes definitivos
quedan condicionados: conservar universo sellado mantiene las cifras
históricas disponibles; adjudicar universo independiente puede cambiar punto,
soporte y publicabilidad y exige CALC sucesor. Ninguno de esos escenarios
permite escoger semilla que publique. Los cinco permisos están próximos a
CV .30; #606 tiene ancho próximo a .20. #2039 tiene CV sellado .269 y no
debe describirse como prácticamente idéntico al umbral.

2021: P8_2=1, trabajadoras entre octubre 2016 y entrevista; eventos de embarazo
entre respuestas 1/2, código 3 fuera, unión positiva con algún 1 y negativa
solo con todos 2. FAC_MUJ, EST_DIS/UPM_DIS y UPM sin casos conservadas en
marco de réplicas. No confundir ≥5 UPM con casos para soporte con todas las
UPM del marco para remuestreo. Las cinco supresiones publican soporte y CV
independiente: todos exceden .30. El sellado cumple; las dos realizaciones
cambian disponibilidad, sin probar cambio de conclusión sustantiva. Punto e
IC independientes no publicados siguen ausentes: no se recuperan por ingeniería
inversa ni se imputan sus valores.

`dictamenes.tsv` contiene once identidades, soporte sellado, ancho y CV
calculados por comando, distancias absolutas a ambos umbrales, CV independiente
cuando existe, dependencia y consecuencias. Todas conservan DISCREPA histórico
de publicabilidad. Las once cifras selladas siguen disponibles; las once
reconstrucciones aplicaron supresión. Incertidumbre cambia y equivalencia
inferencial no está demostrada; cambiar una disponibilidad no prueba que cambie
un signo, ranking o regla consumidora.

Avance posterior descontado: `forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1/nota-recibo.md`
§3 ya recomienda ACOTAR diez y PROPONER-SUSPENDER #2039. Se cita sin adoptar:
su banda MC 0.100 no sustituye CV .30/ancho .20; una proximidad relativa no
demuestra atribución causal al RNG, particularmente con universos 2011 distintos.
El sucesor para publicación debe fijar marco, dominio, singleton, réplicas sin
denominador y regla de reporte antes de obtener otra realización, con sesión01
como dependencia de universo; no se ejecutó búsqueda de semillas ni un replay
favorable. Falta evidencia de cobertura nominal para declarar defendible el IC.

EJECUTADO: `python3 forense/validacion-independiente/catalogo-1-incertidumbre-spec/p2/deriva.py`.
Diez comprobaciones dirigidas en `pruebas.json`: igualdad y siguiente flotante
de ambos umbrales, cero/no estimable, soporte y enumeración sintética de marco
con UPM de contribución cero frente a remuestreo solo de dominio. La enumeración
demuestra cambio de distribución de denominador, no estima su magnitud real
en 2011. No se recalculó microdato ni se corrigió resultado sellado.
