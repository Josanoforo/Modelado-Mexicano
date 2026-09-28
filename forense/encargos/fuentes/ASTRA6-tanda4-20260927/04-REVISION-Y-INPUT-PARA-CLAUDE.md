# Revisión de PR y disposición · 27/sep/2026

Repositorio: https://github.com/Josanoforo/Modelado-Mexicano
Recomendación de Astra para mesa; no constituye fusión, aprobación publicada ni adopción.

## PR abiertos al último corte

| PR / HEAD revisado | Disposición | Alcance y reserva |
|---|---|---|
| #1202 / 3316f9038954d3feab3c88a3d1e1affecc560621 | Favorable a fusionar como evidencia con reservas | 425 identidades reconciliadas; 333 dictaminadas no significa 333 validadas. Conservar separación de componentes y reserva de red. C1 no cierra. |
| #1203 / bd0cd6e1ebe5ebff0b52057676fbb837e51394d1 | Favorable a fusionar como preparación documental | 859 identidades únicas = 767+92. No hay permiso de lanzamiento implícito. Mantener método/tolerancia e intento anterior. |
| #1209 / 7d54456820b39a15fad2e656bccfab096df36188 | No dar orden de fusión en el corte actual | Derivados; API reporta mergeable=false. Dejar al circuito automático vigente renovar/resolver su vigencia. No repararlo a mano ni crear encargo científico para ello. |

Orden recomendado por trazabilidad: #1202 → #1203. En la comprobación final ambos conservan el HEAD revisado y la API informa mergeable=false. La recomendación es favorable por contenido, condicionada a integrar main y resolver la incompatibilidad conservando actos ajenos; revisar el diff de esa integración antes de fusionar. No es una dependencia de código que exija bloquear la preparación. #1209 es independiente. #1207 está cerrado sin fusión y ya no entra en la cola.

## Hallazgos de contenido

**#1202.** Punto: 275 coinciden, dos discrepan bajo tolerancia cero, 56 no se reconstruyen; 92 apartadas. IC: tres coinciden, ocho discrepan, 312 insuficientes, diez sin referencia; 92 apartadas. Las dos diferencias de punto son −4.440892098500626e-16 y −1.8189894035458565e-12: conservar DISCREPA histórica sin llamarlas efecto material probado. Ocho diferencias de IC requieren distinguir receta de remuestreo incompleta de fallo inferencial. Los nueve alias rechazados mantienen rechazo original y dictamen posterior separado. Se conserva el intento de las 92 identidades y se reconoce que la advertencia previa no se detectó a tiempo. Recibir evidencia no certifica ceguera plena: falta aislamiento de red verificable.

**#1203.** Cinco paquetes 100+96+100+471+92=859; mapa por llave, solo ventana transportada. Las 119 exclusiones de NF y las 32 identidades D-15 no se incorporan a esta cohorte. Conserva metodología histórica, no adopta por transporte #1194 ni la aclaración #1205. Fuente publicada posterior al productor declarada como tal. La observación antigua de que c58810f1 no era ancestro corresponde al HEAD f4122ec; el HEAD revisado bd0cd6e sí lo incorpora, comprobado por comparación remota. No repetir esa objeción como vigente. Los permisos propuestos ee49-01/02 y el aislamiento siguen siendo condiciones de lanzamiento.

**#1209.** 76 archivos; respecto a #1207, los patches solo difieren en dos tableros/procedencia. No se identificó cambio de adjudicación en ese perímetro. 219 celdas validadas se conserva; los cambios de otras vistas no prueban nuevas validaciones. La revisión no ejecutó regeneración completa ni verifica cada sidecar por replay. mergeable=false impide recomendar fusionar tal cual ahora; no se atribuye causa precisa sin evidencia.

**Correcciones ya incorporadas.** #1195: ambos grupos válidos y escenarios completos son obligatorios; una familia parcial no obtiene cota conjunta ni permiso de lanzamiento. #1196: FIN022/FIN029 separan hipótesis y alcance inferencial; no queda el salto de país a persona ni precio a valoración identificada. #1197: ya fusionado al corte final; V-020-02 es SIN-CIFRA/no comparabilidad, retirada la multiplicación entre años/poblaciones incompatibles. El incidente documental ENADID2023 sigue declarado pendiente en la entrega y sin recibo visible en comentarios consultados; su fusión no acredita adjudicación. Mesa debe recibirlo por alcance, preservando la recepción separable de migración/pareja. No hace falta rehacer los tres reports.

## Verificación realizada y límites

Lectura de diffs, código relevante, notas y reservas; recuento independiente de tablas de 425 y 859 identidades; 12 pruebas sintéticas de transporte y seis regresiones de potencia ejecutadas con éxito. No se reejecutó microdato, los once reconstruidores del lote2, su verificador completo con artefactos, ni el replay general del repositorio. No se inspeccionó por extracción cada uno de los cinco tar. Las afirmaciones de ejecución más amplia pertenecen a sus autores y no se convierten aquí en verificaciones propias.

## Próximos encargos

01: entradas residuales de lote2, listo para preparación documental referida a #1202. 02: aislamiento/adaptador, listo para implementación y pruebas sintéticas en CAJA. 03: ENOE, listo sobre histórico autorizado de #1195. Pueden trabajar en paralelo con perímetros distintos; no constituyen un lanzamiento de reconstrucciones ciegas. Antes de cualquier futuro intento real, consumir los recibos y permisos aplicables, congelar contrato/entrada y abrir contexto nuevo.
