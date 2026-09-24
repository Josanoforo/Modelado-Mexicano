# ASTRA5 · Diseño muestral ENVIPE 2025 para POL-002

**EJECUTADO.** Se registró exclusivamente el PDF oficial [INEGI, Diseño muestral ENVIPE 2025](https://www.inegi.org.mx/contenidos/programas/envipe/2025/doc/889463926689.pdf) como `envipe2025_diseno_muestral_pdf`, archivo `envipe2025/889463926689.pdf`, SHA256 `f60661545c2980026619370b69b7d7d3988ab62100cfa7a9b33ac76b4a7f0e69`, 2,223,597 bytes. No existía id, archivo ni hash duplicado en el manifiesto. `tests/manifiesto.py --verifica --id envipe2025_diseno_muestral_pdf` devolvió COINCIDE para SHA y tamaño.

**LEÍDO.** El PDF confirma muestra probabilística, trietápica, estratificada y por conglomerados, con población elegida de 18 años o más. Su apartado «Factores de expansión del delito» distingue delitos del hogar (códigos 01–04) y personales (05–15) y ajusta incidentes repetidos del mismo tipo cuando exceden cinco. Esto afecta materialmente el denominador y peso del contrato U0 `POL-002`; la mera lectura de BP1_20/BP1_21/BP1_24 no reproduce por sí sola la cifra negra oficial. Condiciones: Términos de Libre Uso de INEGI registrados en el manifiesto.

**REPORTADO.** U0 debe consumir el id/hash después de integrar este PR a `main`. El módulo, FD y microdato ENVIPE 2025 ya estaban registrados y sus SHA físicos se comprobaron en U0. Solo el diseño era la dependencia documental. No se descargó ni abrió microdato aquí; ENVIPE 2026 sigue fuera de perímetro.

## NO-CORRIDO / RESERVAS

No se ejecutó cálculo, no se abrió microdato y no se asumió que el agregado publicado sea la fracción simple de las respuestas. El paso siguiente es cerrar el contrato de estimación por tipo de delito y factores en CAJA, con permiso de ola comprobado.
