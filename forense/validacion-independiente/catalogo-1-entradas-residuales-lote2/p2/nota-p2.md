# P2 · entradas humanas punto y ventanas

EJECUTADO: recuperados descriptores públicos completos ENBIARE2021, ENCUCI2020 y ENIGH2022. Los tres SHA256 coinciden con el manifiesto vigente. Fuentes, fechas y localizadores se fijan en fuentes.json; las specs históricas completas se referencian sin duplicar bytes. Esas specs contienen contexto/resultados y permanecen exteriores. Los PDFs y specs/ sí son candidatos de entrada; el mapa residuales-p2-decisiones.tsv permanece exterior.

LEÍDO: ENBIARE FD PDF p6 y p17–18; spec histórica 24/sep §1–3. ENCUCI humana 09/sep §3.5 identifica B-P-RUR-AGR como rural y AP4_3_2=1. ENIGH humana 15/sep §1.3, §2.1–2.2 identifica complemento como d==0 contado directamente. Descriptores oficiales respaldan los códigos y nombres. Las definiciones ENCUCI/ENIGH son anteriores a sus intentos y restauran contenido omitido en la extracción; no modifican el histórico ni convierten sus hallazgos previos en coincidencias.

PROPUESTO: ENBIARE edad98 no se asigna a ningún tramo; CESD7 requiere edad conocida para todos los ejes y conserva umbrales históricos. Las otras conductas conservan adulto98 en ejes sin edad. Esta elección afecta denominadores y comparabilidad y requiere firma de contenido; fecha27/sep posterior al resultado conocido. No es fuente humana original ni restauración. El descriptor sí restaura la semántica y ventanas, pero no aporta la regla ausente de desconocidos.

NO-VERIFICADO: ningún recálculo, punto, IC o equivalencia numérica. No se abrió microdato ni productor. No se pretende resolver el contrato aleatorio P3. No se encontró cláusula humana histórica de tratamiento edad98 para tramos/CESD7; esa ausencia local se distingue de la existencia del FD original completo.

Comandos: curl -fL URL -o PDF (URLs en fuentes.json); pdftotext -layout PDF salida.txt; sha256sum PDFs; lector csv.DictReader sobre tabla estimadores para causas. La primera descarga falló por DNS del sandbox y se completó con escalación autorizada. El resto del material proviene de lectura dirigida de fuentes humanas existentes.

EJECUTADO: git blame de cláusulas ENCUCI435–436 y ENIGH173–174 y git log dirigido de sello.json acreditan commits COMMIT-1 anteriores a COMMIT-2 (residuales-p2-precedencia.json), sin abrir resultados ni código. ENCUCI fuente19:59:41 y sello20:01:17 CDMX09/sep; ENIGH fuente16:02:13Z y sello16:23:38Z15/sep.
