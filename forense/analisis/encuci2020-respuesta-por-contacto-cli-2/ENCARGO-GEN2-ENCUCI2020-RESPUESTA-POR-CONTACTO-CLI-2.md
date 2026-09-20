# GEN2-ENCUCI2020-RESPUESTA-POR-CONTACTO-CLI-2

Rama: `codex/gen2-encuci2020-respuesta-por-contacto-cli-2`.
CALC propuesto: `CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001`.
Análisis/preregistro/test: `encuci2020-respuesta-por-contacto-cli-2`.

Mide el perfil de solicitud y entrega entre personas que contactaron cada tipo de autoridad. Esta NO es una tasa de corrupción atribuible a esa autoridad: AP5_17/18 son respuestas generales de persona y los contactos pueden coexistir.

## Lanzamiento y autoridad

CAJA local, repositorio Josanoforo/Modelado-Mexicano. Base revisada: ea88cb3b94ad820bcd92a485eae51ce24ef07fae. Crea worktree propio desde origin/main actualizado; reporta ruta absoluta, rama, HEAD y estado. Lee AGENTS.md y normas aplicables. Pegar este encargo autoriza commit, push y PR; no merge, contador ni adopción. No intervengas las ramas de recibo ni la sesión Claude.

Antes de medir, comprueba duplicados por contenido en CALC, análisis, encargos y ramas. Si una parte existe, úsala como control y entrega las piezas faltantes; no renombres lo mismo como medición nueva. Resuelve payloads por manifiesto/corpus y verifica hashes. Primero acredita documentación, catálogos, universo y diseño; después congela en COMMIT-1 spec humana/YAML, medidor completo, pruebas sintéticas y RESULT. Declara toda exposición previa; no afirmar ceguera. COMMIT-2 conserva el primer resultado, ejecución y sello; defecto material posterior sigue sucesión sin editar el sello previo.

## Antecedentes y fuente

Lee CALC-ENCUCI-0001 y CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001 (#882). Ya existen diez contactos marginales y respuesta por número de tipos/DOMINIO. El producto nuevo cruza respuesta con pertenencia a cada contacto, sin duplicar los totales anteriores.

Mismo payload encuci2020_bd_dbf y ENCUCI_2020_SEC_4_5.dbf, ID_PER, AP5_16_1..10, AP5_17/18, FAC_SEL y EST_DIS/UPM_DIS. Conserva unidad persona, universo/periodo/catálogo/saltos documentados. No contar tipos como número de trámites y no interpretar solicitud/entrega coobservadas como la misma transacción.

## Productos

1. Para cada tipo j, entre AP5_16_j=1: n/masa, cobertura de respuestas AP5_17/18 y distribución exhaustiva ninguna/solo solicitud/solo entrega/ambas. Publica unión, P(entrega|solicitud) y P(entrega|no solicitud), con denominadores propios y precisión. Usa rótulo «personas con contacto con X», nunca «X pidió/recibió dádiva».
2. Contraste para cada j dentro de personas con algún contacto acreditado: contacto j=1 frente a j=2, con AP5_17/18 válidas en ambos. Un AP5_16_j desconocido queda fuera de ese contraste y se cuantifica. Diferencia de unión y de ambas, con covarianza compartida. Los dos grupos de cada contraste son disjuntos, pero las diez comparaciones comparten personas: no tratarlas como independientes ni sumarlas.
3. Para cada j, entre quienes tuvieron contacto j y vector completo de diez contactos, distribución de número de OTROS tipos: 0,1,2+. Añade comparación de cobertura de AP5_17/18 entre grupo de contacto j y su subconjunto de vector completo. Esta pieza muestra cuánto solapamiento impide una lectura por autoridad; no mide respuestas de la autoridad j ni ajusta causalmente por exposición.

No cruzar con DOMINIO/sexo/edad ni estimar regresiones o tasas por evento. Publica tablas completas sin seleccionar contactos por significación o tamaño de la diferencia. Intervalos puntuales descriptivos; no adjudican un ranking de autoridades.

## Diseño y controles

Marco completo FAC_SEL válido; indicadores de dominio y réplicas comunes de UPM dentro de EST_DIS, semilla/réplicas/singleton/degeneraciones fijados. Un no-contacto por salto no se usa como no-solicitud. Desconocido no se convierte en negativo. Grupo vacío preserva no estimable sin tumbar el resto.

Pruebas materiales: múltiples contactos, algún sí con otros desconocidos, ausencia de sí con un desconocido, condicional sin denominador, contraste con grupos disjuntos y partición exhaustiva. Verifica unión=solicitud+entrega−ambas y que casos compartidos no suman personas nuevas. Control independiente de un punto y de una varianza/contraste focal. Totales del padre solo como control. La nota debe explicar por qué diferencias por perfil de contacto no identifican qué autoridad solicitó o recibió.

## Publicación, perímetro y cierre

Escritura exclusivamente en CALC nuevo y sucesores propios, su preregistro, directorio de análisis/encargo propio y prueba propia; asiento de replay de esa identidad y vistas generadas por interfaces existentes. Los padres y medidores compartidos son solo lectura: no los refactorices. No tocar milpa, motor, gobierno, decisiones, manifiesto, corrida0.py, tests/check.py, baseline o workflows. No abrir ENCIG2025, ENIF2024, ENVIPE2025, HOLDOUT, piloto 3 ni datos ajenos al contrato.

Sella, ejecuta replay dirigido, conserva evidencia y asienta la identidad propia en la fuente canónica. Proyecta sin verificación global por inercia y sin aceptar replay ajeno mediante --lote. Una segunda proyección debe ser estable. Cambios de usos derivados ya autorizados se verifican por procedencia; no son adopción nueva por aparecer en el diff. Al integrar main, regenera vistas compartidas; no resuelvas sus TSV a mano. Si queda una compuerta externa real, conserva la medición y publica el PR con comando/salida y pendiente preciso; no afirma registro exitoso.

Entrega tablas legibles y procesables, mapa RESULT→estimando/universo, hashes, n/masas/cobertura, interpretación, controles independientes y pruebas efectivamente ejecutadas, sello/replay/asiento, SHA y URL del PR. Los RESULT deben contener los valores o vincular por hash tablas deterministas reproducibles. Contador y consumo PENDIENTE-DE-MESA. No convertir un límite parcial en abandono del resto: conserva los productos estimables. Auditoría alrededor del 20%, salvo riesgo que cambie números; no sanear deuda general.
