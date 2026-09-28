# P5 · potencia ENOE sucesora

PROPUESTO-POR-EJECUTOR. Este cálculo de planificación no adopta una familia,
no modifica emisiones y no constituye evidencia de acierto futuro.

Decisión recomendada: **NO-LANZAR-TODAVIA**. EJECUTADO: diagnóstico del mismo
oro confirma 39 estratos singleton presentes también en el marco completo,
comunes a ambos grupos; no son 78 estratos ni un artefacto de filtrar el dominio.
No está identificada la varianza total de ninguno de los dos grupos. La tabla
`enoe-escenarios.tsv` conserva seis filas con potencia, MDE e informatividad nulas.
Se solicita instrucción oficial aplicable a ENOE2024T4 para esos estratos:
indicador de certeza y probabilidades de inclusión si corresponde, o estructura
oficial de colapso/réplicas que identifique los componentes faltantes. FAC_TRI
por sí solo no resuelve esa falta. La auditoría agregada sustenta el bloqueo;
no se ha probado que ningún método válido pueda existir con insumos adicionales.

Comando reproducible EJECUTADO: `python3
forense/analisis/familias-2027-enoe-inferencia-1/potencia/calcula_sucesor.py
--diagnostico
forense/analisis/familias-2027-enoe-inferencia-1/diagnostico/enoe-auditoria.json`.

LEÍDO: contrato corregido de frontera-1, `potencia/calcula.py` y
`criterios-previos.md`. EJECUTADO: el sucesor importa sus funciones sin llamar
al CLI histórico, que escribiría sus salidas dentro de frontera-1. Los hashes
de contrato, criterios, oro histórico y diagnóstico consumido están en
`enoe-potencia-resultados.json`.

Los seis escenarios previos son SEX1/SEX2 × desviación temporal 0/.01/.03;
alpha familiar .05, Bonferroni para dos grupos, objetivo .80, semibanda .05,
oro2024T4 → objetivo2027T4 y cambio material .10 permanecen intactos. El SE
futuro igual al del oro es supuesto. Rho=0 es supuesto del
contrato: la distancia de tres años no demuestra independencia de UPM.

El p0 fijo se toma directamente del oro histórico y nunca del punto sucesor.
Las columnas `conditional_fixed_p0_*` evalúan incertidumbre del futuro respecto
a ese número; las demás métricas de cambio incorporan incertidumbre de ambas
poblaciones. No deben intercambiarse ambas preguntas. La dispersión temporal
es un escenario separado del error muestral; tampoco se estima de una ola.

Si la familia carece de identificación, la tabla conserva los seis escenarios
y ambos p0 con métricas nulas: null significa no calculable, nunca potencia
cero. La causa y el insumo requerido se trasladan del diagnóstico; no se
sustituye el diseño por Kish, centrado arbitrario, colapso o una sensibilidad
que mejore la potencia. Las cotas conjuntas solo se calculan para ambos grupos
y todos los escenarios completos.

Pruebas materiales EJECUTADO: `python3
forense/analisis/familias-2027-enoe-inferencia-1/potencia/test_sucesor.py` (5
pruebas) y `python3
forense/analisis/familias-2027-frontera-1/potencia/frontera_test_potencia.py` (6
pruebas originales intactas). Cubren grupos ausentes, SE inválidos, escenarios
ausentes/duplicados, impedimento metodológico aunque exista un SE numérico y
preservación de p0. Los SE diminutos de fixtures no son datos históricos.

NO-VERIFICADO: precisión de la ola objetivo, dependencia real entre olas,
acierto futuro y adopción de cualquier nueva regla.
