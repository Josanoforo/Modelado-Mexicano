# Solicitud de recibo · GEN2-RECIBO-ASTRA-PRODUCTO-N · C3 síntesis transcultural

**Para Claude, por el circuito de recibos de producto.** [PR #1247](https://github.com/Josanoforo/Modelado-Mexicano/pull/1247). Solicito revisar este PR como producto editorial de ASTRA6-C3-SINTESIS-TRANSCULTURAL-1. Esta solicitud no acredita recibo emitido. La mesa conserva fusión y adopción; no se propone mover contadores ni cargar reglas al motor.

## Objetos y hashes SHA-256

| Objeto | Hash |
|---|---|
| `corpus/reports-v2/Psicología__Conducta_y_Sociedad_en_el_México_Contemporáneo__Análisis_Transcultural_y_Estructural.md` | `7800e76e530e8fae4545b2c0f42fce32ebce20e007e0d98c961efca5ba1cd870` |
| `corpus/reports-v2/INDICE.md` | `2601b634933f944ff4943713abce9b1cfe0308a10f5372ba0692c24846936ee9` |
| `forense/analisis/reports-v2/sintesis-transcultural-1/tabla-afirmaciones.tsv` | `415f68679bf131015d1e31336713b7ad74499f475de95b9a0980bfa387c7724d` |
| `forense/analisis/reports-v2/sintesis-transcultural-1/tabla-decisiones.tsv` | `904b5028fdfce4aa85a5e7d23ee9bc964882f32a0d88d083f2bb57c745b13a8c` |
| `forense/analisis/reports-v2/sintesis-transcultural-1/hoja-reglas-propuestas.md` | `b46a9c24b7488506e1738b9b6c4822f30abe8d091366c692cc3f5919e866e3b6` |
| `forense/analisis/reports-v2/sintesis-transcultural-1/indice.py` | `64fdd8a942aacdd30742ceb7cfda63f0cc1e881b6dfe546cc3bfc37425d5f56a` |

El cuerpo archivado del encargo tiene sidecar `3065678872e3a5786aad6f58175588b8438e45f943401f8f1ae58dfe418517d1`; el blob Git del v1 es `fecc7d53112f2e25170efbaa3eb15eaa677abedf` y su SHA-256 `2ead6a5a8c3e16b7e94e32be1d3eebd6bfe476ed815ec5ebe6cbaed426915404`. Los adjuntos embebidos coinciden con sus tres hashes declarados. Se preservan cuerpos previos.

## Resultado y revisión pedida

**EJECUTADO.** Report general sustantivo con tiers de frecuencia y mecanismo separados, evidencia (a)/(b)/(c), comparaciones internacionales con versiones y muestras, causas rivales, implicaciones, reglas falsables y auditoría final. Tabla explícita de 105 tesis: 28 del mapa y 77 adicionales, con dictámenes 2 CONFIRMA, 61 MATIZA, 22 ROMPE, 20 SIN-CIFRA. Índice: una fila por cada uno de los 31 originales; 24 en main, 3 en PR ajenos, uno en esta rama y 3 sin entrega al corte `a8c3e341`. C3 global sigue abierto.

**Revisión independiente solicitada.** Revisar las 22 filas ROMPE, en particular índices Hofstede/GLOBE, compensación familiar del bienestar, confianza y cifra negra, estructura/cultura/adaptación, Smith 2017 y comparaciones por segmento. Comprobar que los 20 SIN-CIFRA no se presentan como refutaciones. Verificar fuente/denominador de las cifras externas y que ningún report editorial se contó como estudio independiente. La [nota de lectura](tabla-lectura.md) distingue fuente heredada de primaria reabierta.

**LEÍDO.** v1 completo, mapa, reportes temáticos pertinentes entre los 24 homónimos fusionados al corte y fuentes primarias citadas en la síntesis. La corrección de Smith se tomó del report de interacción ya fusionado, que cita método y tablas del objeto primario. El PR #1242 se consultó por SHA sólo para estado y conteos editoriales del índice; #1240 se integró desde main tras su fusión. No se abrió microdato ni se consultó ola reservada.

**PROPUESTO.** Cuatro reglas candidatas con consumidor, condición, evidencia, tier y falsador en [hoja-reglas-propuestas.md](hoja-reglas-propuestas.md). Recomendación: recibir la síntesis y el índice como producto editorial con límites explícitos; mantener reglas sin adopción hasta decisión de contenido de mesa. No se pide una cuota de reglas ni renumeración de otros lotes.

**NO-VERIFICADO.** Recibo de Claude, decisión de mesa sobre reglas, fusión de este PR, adopción de otros PR y cierre C3. La ejecución de `tests/check.py --rapido` dio 0 FAIL y 624 WARN ajenos al producto. `tabla-verifica.py` y `indice.py --verify` pasaron; éstos son controles de cobertura y enlaces, no validación de tesis. La hoja de [cierre](cierre.md) precisa sucesores.
