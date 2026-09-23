# ASTRA5 · Adquisición dirigida del diseño ENIF 2024

**EJECUTADO.** Se incorporó solo el PDF de diseño muestral de ENIF 2024 para cinco contratos documentales de ASTRA5-U0 (`FIN-001` a `FIN-005`). Fuente primaria: [INEGI, Diseño muestral ENIF 2024](https://www.inegi.org.mx/contenidos/programas/enif/2024/doc/889463921127.pdf). El nombre `enif_2024_diseno_muestral.pdf` anunciado por metadatos RNM no resuelve hoy: devuelve página HTML «Esta liga ya no existe». Se usó el PDF vigente con ISBN/código `889463921127` y título interno «Encuesta Nacional de Inclusión Financiera 2024. ENIF. Diseño muestral».

La pieza nueva tiene id `enif2024_diseno_muestral_pdf`, archivo `enif2024/889463921127.pdf`, SHA256 `bc59f5f58c32831d3831a1a92ee6707e57e68caf68df1d573b8eb754e2259b76` y 1,548,004 bytes. `tests/manifiesto.py --verifica --id enif2024_diseno_muestral_pdf` devolvió **COINCIDE** en SHA y tamaño. No había entrada previa por id, nombre ni hash. El documento declara población objetivo de 18 años o más y diseño probabilístico, estratificado, por conglomerados y varias etapas; las condiciones aplicadas son los Términos de Libre Uso de INEGI registrados en el manifiesto.

Los otros componentes ya existían y sus SHA físicos se comprobaron: `enif2024_csv` (`a3507b40…`), `enif2024_cuestionario_pdf` (`32e37cc1…`) y `enif2024_fd_xlsx` (`17e2ad86…`). No se abrió ni descargó microdato; tampoco se reingresó el cuestionario o FD. El PDF físico se conserva fuera del repo en `/home/pc0/mm-corpus/raw/enif2024/889463921127.pdf`.

**LEÍDO.** Cuestionario ENIF 2024 §§5, 8 y 9; FD `TMODULO`; diseño muestral pp. iniciales; términos INEGI ya revisados en la adquisición documental de #1082. El diseño no verifica los porcentajes publicados: solo cierra la dependencia documental.

**REPORTADO.** ASTRA5-U0 debe consumir este id al integrar el PR y cotejar denominadores, filtros y RESULT existentes antes de cuantificar. Los cinco contratos permanecen `MEDIBLE-CON-ADQUISICIÓN` en la rama U0 hasta que la adquisición sea incorporada a `main`; después pueden cambiar a `MEDIBLE-EN-CORPUS` sin fingir que ya están medidos.

## NO-CORRIDO / RESERVAS

No hubo apertura de microdatos ni cálculo. No se empleó el enlace RNM obsoleto como payload. La adopción de la entrada en `main` depende del merge del PR de esta rama.
