**L0 · ADR-260923-ASTRA5-U3-POLITICA-df0d-01.** El acto archiva el
encargo A.3 con hash `bc255836ca9e8ed7a32c578961e302d99a79e7b855eb809ba4863660aa6bc679`,
clasifica los 45 ID INE, congela antes de abrir cada fuente y sella cuatro
CALC (INE 2024, ENCUP 2012 dos versiones, LAPOP 2019). Tres activos y el
primer resultado adverso ENCUP 0002 archivado con sello intacto. Tres tablas útiles
se leen en `forense/analisis/dominios/politica/RESULTADOS-ASTRA5-U3.md`.
El intento ENCUP 0001 falló antes del sello; 0002 se conservó con dos
NO-ESTIMABLE; 0003 recodificó etiquetas explícitamente. Los tres CALC
útiles pasaron verify RESULTADO=REPRODUCE, CONTEXTO=IDENTICO. No adopta.
El registro global permanece **sellada en disco, no registrada** hasta el
canal del push a `main`. `corrida0 status` deriva tras archivar ENCUP 0002;
no se reescribió un sello ni se modificaron vistas globales.
NC-260923-ASTRA5-U3-POLITICA-df0d-01 conserva el fallo y su cierre;
NC-260923-ASTRA5-U3-POLITICA-df0d-04 conserva la publicación pendiente.
Los RESULT son retrospectivos, sin inferencia ecológica ni causalidad de
oferta clientelar. `forense/replay-evidencia.tsv` contiene tres asientos
activos; ENCUP 0002 queda como antecedente histórico con sello verificado.
