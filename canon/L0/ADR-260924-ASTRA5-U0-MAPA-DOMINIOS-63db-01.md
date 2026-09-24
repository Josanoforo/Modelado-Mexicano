**L0 · ADR-260924-ASTRA5-U0-MAPA-DOMINIOS-63db-01.** Cierra ASTRA5-U0 (PR #1079): `canon/mapa-dominios-v1_0.tsv`
publica 1 396 afirmaciones de los 37 archivos del censo, una fila por
afirmación, con dictamen cerrado: 208 MEDIBLE-EN-CORPUS, 768
MEDIBLE-CON-ADQUISICIÓN y 420 NO-MEDIBLE-POR-DISEÑO, 10 fusiones entre
archivos y cobertura completa de G/P/T/fichas. `ensambla_mapa.py` deriva y
verifica byte a byte la proyección para ASTRA4-U1 (medibilidad,
autorización y RESULT separados), la tabla report→dominio para FRONT y la
hoja de adquisición derivada. Diez contratos con RESULT sellado quedan
EN-MEDICIÓN hasta que `GEN2-TUBERIA-VISTA-NORMALIZADA-2` destrabe el
`[deriva]` (E.7). 131 filas quedan `NO-ACCESIBLE-DESDE-SANDBOX` (no «no
existe»), con sucesor `GEN2-ASTRA5-U5-ADQUISICION-1` y la receta de acceso
archivada; la herramienta de acceso de la ADENDA-1 no se instaló (opción 2).
No mide, no adopta, `celdas_validadas` intacto; merge de mesa.
