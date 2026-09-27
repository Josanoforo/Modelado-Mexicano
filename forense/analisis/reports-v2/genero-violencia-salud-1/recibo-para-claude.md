# Recibo solicitado · ASTRA6-C3-GENERO-VIOLENCIA-SALUD-1

EJECUTADO: tres reports v2 completos, decisiones explícitas por cláusula, tablas razonadas y productores propios. El [índice local](indice-local.md) deriva los conteos; son registros de cobertura con reiteraciones, no tesis independientes. Cero mediciones nuevas, cero adopciones y ningún consumidor del motor activado.

LEÍDO: originales íntegros por bloques, filas del mapa por lector CSV, fuentes primarias documentadas en cada pieza, CALC/RESULT/sellos y decisiones por identidad. Las vistas atrasadas se cotejan con los objetos sellados y firmas. Evidencia no adoptada se publica provisional y no es piso del catálogo. No se leen microdatos ni ENVIPE2026/EDR2024.

EJECUTADO: revisión editorial dirigida POR EJECUTOR en las tres piezas, sobre ROMPE, cifras centrales y mecanismos. No acredita revisión humana independiente. Se solicita a Claude y mesa revisar específicamente: violencia de pareja vs población total; ENDISEG identidad vs exposición; percepción/cambio de hábitos vs efecto causal; NS/NR del CALC ENVIPE; conteos suicidio vs tasas; mediana de demora y contacto amplio vs atención especializada. Ausencia de identificación causal nunca se declara refutación por sí sola.

EJECUTADO: `python3 forense/analisis/reports-v2/genero-violencia-salud-1/verifica_lote.py` regenera los tres reports/tablas/resúmenes/índice. `python3 forense/analisis/reports-v2/genero-violencia-salud-1/verifica_lote.py --check --self-test` verifica sin diferencias y rechaza cifra sin evidencia, denominador incompatible, cobertura faltante y adopción provisional falsa. Comandos por pieza en resumen-lote.json; hashes en hashes-producto.json, calculados sobre objetos reales tras cerrar las piezas.

EJECUTADO: gate rápido pertinente del repo `python3 tests/check.py --rapido --baseline`; resultados en verificaciones.md. No se toma CI como prueba sustantiva. El intento completo preparatorio interrumpido no se presenta como validación.

PROPUESTO-POR-EJECUTOR: reglas con consumidor posible, condición, falsador y límites en cada report; recomendación en [hoja para mesa](hoja-para-mesa.md). Recibir para evaluación en catálogo sucesor, sin adopción aquí.

PENDIENTE: revisión humana de tesis y recibo técnico por circuito de mesa `GEN2-RECIBO-ASTRA-PRODUCTO-N`. Se solicitan en el PR; este archivo no constituye recibo concedido. Firma de misión ya preservada en 00-LEEME-LANZAMIENTO.md:3; no se duplica. C1 no bloquea; un hallazgo material posterior exige corregir únicamente lo afectado.

Reservas por pieza y estados provisionales se conservan en resumen-lote.json y sus evidencias. Obtener revisión humana es condición pendiente del Hecho, aunque los productos y controles propios estén ejecutados. Este autor no fusiona ni concede autoaprobación.

EJECUTADO: solicitud por circuito en [PR #1180](https://github.com/Josanoforo/Modelado-Mexicano/pull/1180). No se enviaron mensajes externos ni se fusionó. Corte main incorporado `3aacda232b3b03f158950738f31aa4ea509d3162`; verificador conjunto/autopruebas y gate rápido VERDE.
