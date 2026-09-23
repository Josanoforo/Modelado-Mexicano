# ASTRA5-U4 · TECNOLOGÍA, INTERNET Y CIBERACOSO COMPLETOS

**CAJA · `codex/astra5-tecnologia-1`. Dos instrumentos: MOCIBA y ENDUTIH. Prioridad de caja después de ENOE.**

## Resultado

Pisos de uso de internet/celular, actividades digitales, razones de no uso, exposición a ciberacoso y respuestas observadas, por olas comparables y segmentos admitidos. Reports: Tecnología, Juventud y componente medible de Sanción Social. No convertir ciberacoso en medida de chisme, envidia o aceptación cultural.

## Reutilización obligatoria

Lee forense/produccion/mociba-flujo-documental-1/{dictamen.md,contrato-elegibilidad.yaml,flujo-por-ola.md,tarjetas-sucesoras.yaml}, su clasificador y tests/test_mociba_flujo_documental.py. Su conclusión de septiembre acredita flujo P12 en 2021/2022, pero NO autoriza un enlace predictivo ni una apertura reservada. Reutiliza la lógica válida sin rehabilitar el candidato descartado. Esta misión es descriptiva; verifica qué olas puede abrir y continúa las no reservadas.

ENDUTIH: tools/medidor_gobierno_digital_endutih.py y data/l6-gobierno-digital-endutih-v1_0.json son antecedentes por revisar. El último es medición histórica, no nuevo RESULT GEN2; no ingerirlo para producir un piso. Consume CALC GEN2 equivalente si existe; si la cadena falta, re-mide desde raw con protocolo. Busca también archivos bajo alias, no solo prefijos.

## Especificación

1. Por ola, texto, código, universo y periodo de referencia de internet, celular, actividades, ciberacoso y respuesta. No asumir que MOCIBA tiene el mismo diseño desde su primer año: comprueba población etaria, cobertura estatal, instrumento anfitrión y cambios. Distingue prevalencia sobre usuarios de internet de prevalencia sobre población total.
2. Elegibilidad de preguntas posteriores a acoso: salto estructural, no respuesta, NS y «no» separados. En P12/otras matrices distingue respuesta múltiple de categorías excluyentes. «Bloquear» y «denunciar» pueden coexistir; no sumarlos como partición ni interpretar blanco como no acción. Congela contrato por cada ola, no transfieras códigos por memoria.
3. No uso: cobertura, acceso/costo y preferencia por texto y unidad correspondiente. Razones de hogar no son preferencias de una persona. Enlace con ENCIG/ENIF solo conceptual y por referencia: no juntar muestras distintas como panel ni usar uso de internet para sustituir gobierno digital sin coerción.
4. Sexo, edad, escolaridad, localidad y entidad según diseño y disponibilidad; ejes univariados, mínimo n y supresión antes del dato. Menores incluidos únicamente si el instrumento los incluye y con universo rotulado; no comparar directamente tasas 6+, 12+ y 18+ como la misma conducta.
5. IC de diseño por estratos/UPM/pesos; réplicas compartidas para dominios de una ola. Dependencia entre MOCIBA y ENDUTIH si comparten muestra se declara; no contar dos muestras independientes por tener dos archivos. Serie/calibración solo en tramos comparables, con evaluación temporal separada del ajuste.
6. Congela spec humana por instrumento y medidores, corre todas las olas elegibles acordadas, conserva RESULT no estimables y réplica agregada útil. Fricción de un módulo no suspende medición de otro. No abrir nuevas olas reservadas para alcanzar longitud de serie.

## Producto y perímetro

Specs MOCIBA-PISOS-* y ENDUTIH-PISOS-*; CALC-MOCIBA-PISOS-* y CALC-ENDUTIH-PISOS-*; tools/dominios/{mociba,endutih}/**; forense/analisis/dominios/tecnologia/**; tests propios; replay y cierre. No modificar el clasificador compartido salvo propuesta fuera de esta unidad, ni el catálogo ASTRA4.

Tablas enlazables por catálogo, nota de contraste por afirmación U0 con tier/falsador, FP por instrumento y recibo. Contador de conductas digitales y de ciberacoso separado, celdas y olas como cobertura. Aceptación: dos instrumentos tratados íntegros, preguntas/denominadores auditables, verify REPRODUCE y asientos, ninguna respuesta estructural convertida a cero. Una ola bloqueada queda declarada; no elimina la obligación sobre el resto.

## Mandato de ejecución y cierre común

**Modelo Sol 6. Mesa firma mediante merge.** Este encargo autoriza preparar, implementar, congelar, ejecutar dentro de las reservas permitidas, crear commits, push y PR; no fusionar ni adjudicar por cuenta propia. Presenta las propuestas completas a revisión sin pedir aprobación previa repetida de elecciones técnicas ya delegadas. Una firma exigida para adopción no es excusa para dejar de preparar el resultado. El merge futuro no levanta hoy una reserva de datos explícita.

Al abrir: fetch origin, ruta absoluta/worktree propio, rama/HEAD/status, ramas vivas y conteo. Base de preparación `8e41f72fa8b00a20e83f28c92f6b2964e66b0081`, 23/sep/2026; re-deriva, no heredes cifras. Lee AGENTS.md, instrucciones vigentes, /acto y encargo completo. Archiva este texto verbatim por A.3 con hash. Usa ids con raíz D-24 y cierre D-21. No uses espejos ZIP como estado actual. Busca por objeto trabajo consolidado y propietario en vuelo; consume lo válido y resuelve la transferencia del pendiente sin duplicar sesiones.

Reutiliza herramientas, cuestionarios leídos, contratos y mediciones del repo. Revisa dependencias efectivas y fija hashes antes de congelar. Una medición GEN1 puede orientar el diseño y el código, pero sus valores no son input para GEN2. Consulta el manifiesto por id, archivo, descripción y alias: un prefijo sin hits no demuestra ausencia. Separa cuestionarios, FD, datos, documentación administrativa, formatos duplicados y olas. Hash declarado en manifiesto no es hash recalculado en disco. Raw/corpus primero; internet solo para documentación o faltante concreto. Nunca incorpores raw al repo.

En CAJA, antes de cada apertura: consulta decisiones, manifiesto, firmas y reservas específicas. Nada de ENCO ni ENVIPE 2026. La última ola ENOE se conserva reservada según el mandato específico. Ola antigua no significa libre por sí misma: una reserva explícita permanece hasta autorización aplicable. No incluyas tabulados/comunicados reservados en la preparación. Si el choque de reserva bloquea una ola, conserva esa pieza cerrada y continúa otras; no pidas permiso para las ya autorizadas.

Para cada CALC: especificación humana, YAML y medidor efectivo congelados en COMMIT-1 antes de abrir dato; frase «el primer resultado que produzca este procedimiento es el que se reporta». Definiciones, reactivos por texto, códigos, filtros, ponderadores, escalas, agrupación, umbral de n/supresión y análisis fijados antes de ejecutar. Preflight → run → sello → verify en COMMIT-2 con CLI vigente; nunca --force ni reescritura de sello. Primer resultado, aun adverso o no estimable, conservado. Un módulo mutable importado no queda congelado por sellar solo el shim. Pruebas sintéticas antes del freeze y pruebas de resultado pertinentes después.

Cada nueva medición lleva cuenta_gen2 conforme a reglas vigentes, adopta: NO y origen_numerico. Cada replay REAL tiene asiento en replay-evidencia.tsv en el mismo PR. Publicación del registro por canal actual; no modificar vistas globales: si sigue pendiente, rótulo «sellada en disco, no registrada» y dependencia exacta. Cifras del producto por RESULT/CALC/hash, unidad, escala, universo y temporalidad; todo este programa nuevo es RETROSPECTIVA. Réplicas o estadísticos agregados necesarios para incertidumbre posterior se conservan con contrato y hash, sin identificadores ni registros individuales.

Distingue punto muestral, piso para otra ola e IC predictivo calibrado. ≥3 olas no garantiza calibración fiable. Ajusta con pasado y evalúa con una transición no usada en el ajuste; no presentes cobertura de calibración como validación. Cuantiles extremos con pocas transiciones tienen incertidumbre. Sin soporte, conserva IC de diseño y declara SIN-HISTORIA-PARA-CALIBRAR. No construyas retadores, pilotos, duelos ni anuncies detección de cambios entre olas. No toques celdas_validadas.

Reglas sobre México: segmento/estructura/institución/adaptación racional/script/psicología se distinguen. Oferta antes que preferencia. Respeta fundamento de reports sin transformar asociación en causalidad. El contraste CONFIRMA/MATIZA/ROMPE especifica qué componente observado de la afirmación se contrastó; si la medición no la contrasta, explica «sin contraste directo» en vez de forzar uno de esos juicios. Ninguna genética poblacional predice conducta de un grupo: firewall íntegro. Evidencia primaria mexicana/diáspora/marco importado rotulada, tier y falsador por regla y auditoría de rigor extremo al final del texto sustantivo.

Cierre: producto completo y pruebas dirigidas; check.py --baseline con evidencia, resolver fallos propios materiales sin campaña de CI; nota con contador inicial/final y EJECUTADO/LEÍDO/REPORTADO, NO-CORRIDO / RESERVAS (Ninguno. cuando corresponda), CONSUMIDO con PR y recibo Codex para Claude. Perímetro de cierre permanente: encargo, nota, ADR raíz, registros de cierre, NC/FP y recibo conforme /acto. No tablero, CI, milpa, motor ni derivados globales. No cerrar tras el inventario, un prototipo o el primer lote; continúa las piezas independientes hasta cubrir todo el universo encargado. D-11 limita tamaño del PR, no alcance de la misión. Toda dependencia residual tiene pieza exacta, evidencia y siguiente operación; no convierte pendiente en completado.
