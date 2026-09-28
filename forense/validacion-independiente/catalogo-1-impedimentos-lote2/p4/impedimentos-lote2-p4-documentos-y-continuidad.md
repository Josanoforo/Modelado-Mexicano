# Documentos P4 resueltos y continuidad ejecutable

EJECUTADO: se verificaron diez documentos exactos públicos, cinco FD XLSX y cinco cuestionarios PDF, para ENDUTIH2023/2024/2025 y MOCIBA2016/2017. Fuentes oficiales y hashes constan en documentos-publicos-contrato.json; el informe documentos-resueltos.json conserva revisión por documento. Se usaron documentos ya adquiridos, no se repitió red. Cuestionarios2023/2025 y MOCIBA16/17 proceden de #1185; los cinco FD y cuestionario2024 estaban físicamente disponibles en corpus documental público. Los hashes coinciden con las referencias humanas históricas. No se abrió ni hasheó ningún ZIP de microdatos, incluido ENDUTIH2025.

Custodia externa materializada: /tmp/astra6-c1-impedimentos-lote2-p4-documentos, diez documentos únicos más recibo. Los ocho contratos remiten por hash a este juego documental compartido, sin duplicar bytes en repo. Si esta custodia falta en otra máquina, el materializador propio vuelve a verificar/copiar sólo los archivos públicos exactos declarados; ninguna firma de reserva se infiere. La receta usa documentos locales previamente adquiridos y no concede acceso a ZIP.

Revisión semántica: FD ENDUTIH trae hojas usuarios/usuarios2 de cada ola, llave persona UPM,VIV_SEL,HOGAR,NUM_REN, FAC_PER/EST_DIS/UPM_DIS y ejes. P7_1 tres meses, P7_10_2 expresa15+, P7_35_4 doce meses; no fusionar ventanas. MOCIBA2016 FD MOD_2016_CIBERACOSO documenta P1_i y P7_i_1/P7_i_6A, FAC_MOCIBA/EST_DIS/UPM_DIS, EDAD12–97. FD2017 documenta P4_01–10, P10_1/P10_5; denuncia incluye proveedor; cuestionario restringe12–59 y junio2016–entrevista2017. Los formularios vacíos confirman filtros y acciones. El informe localiza por hoja/fila y términos/líneas cada evidencia; el materializador revisa tipo/ola/variables base, la interpretación humana anterior revisa la relación con el estimando. No se convierte un hallazgo de campo en reparación del método histórico.

La ausencia documental y revisión documental insuficiente de #1185 ya no son impedimentos actuales en estos ocho paquetes. Persisten firma tolerancia, acceso/disponibilidad microdatos y contrato IC. ENDUTIH2025 sigue reservado. Esta resolución transportable no declara LISTO ni validación integral. La hoja P4 deja firma puntual separable; materialización de documentos fue ejecutada sin comparación ni resultados.

Comando reproducible:

    python3 forense/validacion-independiente/catalogo-1-impedimentos-lote2/p4/impedimentos-lote2-p4-materializa-documentos.py --custodia /tmp/astra6-c1-impedimentos-lote2-p4-documentos

Salida observada: PASS documentos10 microdatos_abiertos0. El comando también produce recibo documental con hashes/rutas y revisión. Para IC el plan histórico debe definirse humanamente antes de comparar; un nuevo plan propuesto no reemplaza el congelado.
