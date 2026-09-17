# ENCARGO · GEN2-ENAPROCE-INSTRUMENTOS-Y-ACCESO-1

**Entorno:** CLI/CAJA; Claude Cloud si tiene acceso a los documentos públicos. **Producto:** contrato documental 2015/2018 de la candidata R03, con reactivos/filtros reales y decisión de si vale tramitar acceso institucional. No abre ni estima respuestas de F6.

## 1. Problema y límite conocido

R03-TRA-ENAPROCE-TRAMITES está RETENIDA-NO-EJECUTABLE en `forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv`: 2015/2018 tienen inventario de variables, pero lo registrado son bases de ejemplo cegadas, no microdatos reales; faltan FD/textos y permanece la decisión de unidad empresa.

Hay una aclaración ya acreditada en el manifiesto que evita repetir una búsqueda: los catálogos oficiales RNM 330 (2015) y 518 (2018), adquiridos el 6/ago, señalan acceso indirecto por Laboratorio de análisis de datos. No se debe perseguir descarga pública de los datos reales sin evidencia nueva. Que un nombre de archivo deje de decir “ciega” no demuestra que sea dato real.

Este acto resuelve primero si el **instrumento** mide de forma utilizable carga regulatoria, solicitud/pago informal o sólo percepción/obstáculo. Con ese resultado, mesa decide mantener la candidata y tramitar acceso, limitarla a otro uso o descartarla para la pregunta actual. No fabricar una familia elegible para alcanzar una cuota.

## 2. Insumos existentes

- `forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv`, R03.
- `forense/prereg-duelo-v2/F6-falta-conseguir-v1_0.tsv`, R03.
- `data/reactivos-ciegos-81-v1_0.tsv`: enaproce2015, 1269 filas; enaproce2018, 1310 al corte de su censo. Son filas de inventario, no tamaños muestrales ni 2579 preguntas únicas.
- Inventarios de reactivos y manifiesto para identificar tablas/variables sin leer respuestas.
- `inegi_rnm_catalog_330_enaproce2015`: `R2.1_R2.2_R10.2_RNM_microdato/inegi_rnm_catalog_330_enaproce2015.html`, SHA-256 `25d01ec9153514adb967c76979923e1ac4a195bb5d4f4361496f7c46e6854881`.
- `inegi_rnm_catalog_518_enaproce2018`: misma raíz lógica, archivo homónimo .html, SHA-256 `67dac48414d11adfcaf2b0fd25c1848a54f3233b33194dbc5eccbdf3ad7b1ffd`.
- `inegi_rnm_518_download_19219`: informe final de levantamiento 2018, ya identificado. No volver a presentarlo como descriptor ni como base de datos.

Leer esos documentos mediante raíces existentes antes de buscar en web. No abrir paquetes estadísticos de ejemplo: sus cabeceras ya están inventariadas y no se necesitan filas.

## 3. Adquisición acotada y reserva

Adquirir, sólo si faltan, hasta **seis documentos oficiales** entre las dos olas: cuestionarios micro/PyME, descriptor/diccionario y manual metodológico que acredite filtros/universo. Reutilizar documentos compartidos entre versiones sólo cuando lo declaren. Priorizar piezas que contengan los reactivos de trámites y corrupción, no acumular PDFs de presentación.

Fuentes: enlaces documentales de los catálogos RNM y páginas de INEGI de cada edición. Guardar documento real, URL, fecha, tamaño y SHA-256. Diferenciar enlace descubierto, documento descargado y documento leído. No registrar error HTML como PDF; OCR local de páginas pertinentes si hace falta y revisión de saltos/tablas.

No abrir tabulados, resultados, reportes con frecuencias del objetivo, bases reales ni ejemplos cegados. No introducir lo adquirido al corpus L. Si una pieza muestra incidentalmente distribuciones del objetivo, detener su lectura y declarar exposición por alcance/ola/variable sin copiar cifras; la reserva no se conserva por no repetir el número.

No solicitar acceso ni enviar mensajes, formularios o correos. No abrir cuentas ni asumir elegibilidad institucional de Jonás. No comprar datos. La política de acceso ya documentada basta para identificar el canal; verificar sólo un cambio material si surge nueva evidencia oficial.

## 4. Contrato por ola y tipo de empresa

Preparar una tabla por los cuatro cruces ola × instrumento (2015/2018, micro/PyME), admitiendo que alguno no contenga el módulo. Para cada reactivo pertinente:

- tabla/variable exacta y texto con página/sección;
- periodo de referencia, población, unidad (empresa/establecimiento), tamaño y cobertura sectorial/geográfica;
- filtro de exposición: realizó trámite, inspección, solicitud u otra condición, y quién queda fuera;
- desenlace y escala: frecuencia, monto, solicitud, pago efectivo, percepción u obstáculo; no equipararlos;
- códigos, multirrespuesta, no sabe/rechazo/salto y denominador;
- ponderador/diseño documentados y qué falta para una estimación real;
- correspondencia con la hipótesis R03: directa, proxy limitado, no equivalente o indeterminada.

No equiparar microempresa con pequeña empresa WBES ni copiar segmentos de ENCRIGE. No derivar causalidad de una pregunta de opinión. Si la unidad cambia respecto del modelo de personas, conservar explícita esa incompatibilidad: la firma F-19 de usos descriptivos empresariales no autoriza por sí sola F6 ni la adjudicación de R03.

Comparar 2015/2018 por texto, universo, código y periodo; una coincidencia de código no establece una serie. Si el instrumento usa año de levantamiento distinto del periodo de referencia, mostrar ambos. No producir una especificación numérica ficticia si todavía no existe un desenlace identificable.

## 5. Producto ejecutable y decisión de acceso

En `forense/produccion/enaproce-instrumentos-acceso-1/` entregar:

1. Tabla de reactivos pertinentes con referencias verificadas y contrato de universo por instrumento.
2. Si existen condiciones computables, función pequeña de elegibilidad/codificación y fixtures sintéticos para los casos de flujo relevantes; no lector de microdatos. Si no hay reactivo equivalente, no escribir código muerto: entregar la tabla que lo demuestra.
3. Nota de máximo dos páginas que responda: ¿qué puede medir R03 realmente?, ¿son comparables las dos olas?, ¿qué decisión permite obtener los datos?, ¿cuál es la pieza que falta?
4. **Sólo si el instrumento justifica acceso**, una adenda breve lista para incorporar al expediente institucional existente: variables/tablas mínimas, población, cálculo propuesto y salida agregada solicitada. Localizar/reutilizar el expediente existente; no crear una campaña ni duplicar contactos. Si no existe expediente, entregar el alcance técnico en la misma nota, sin inventar identidad, afiliación ni compromisos del titular. El envío queda sin ejecutar.

Búsqueda negativa acotada: declarar documentos, módulos y términos usados (“trámite”, “inspección”, “corrupción”, “pago informal”, “obstáculo” y equivalentes que los documentos realmente empleen). No concluir “no existe” sólo por cero coincidencias OCR; revisar el módulo pertinente visualmente o rotular NO-ENCONTRADO-EN-LO-REVISADO.

## 6. Perímetro y cierre

Permitidos: directorio propio, fixtures/script propios cuando útiles, hasta seis adiciones precisas de manifiesto. No modificar el panel F6, código F6, firmas, inventarios/overlays globales, cola, corpus L, ejemplo estadístico ni documentos previos. Esta tanda no pretende cerrar los 55 grupos de NC-0258: sólo aborda los dos instrumentos ligados a R03.

Verificación proporcional: todas las reglas materiales de filtro/código tienen referencia; las cuatro combinaciones instrumento/ola están resueltas o tienen faltante preciso; fixtures representan los saltos documentados, no una interpretación deseada; no se abrieron respuestas ni se declaró ejecutable una familia por tener su cuestionario.

Dos intentos y una alternativa directa por documento. Si sólo una ola queda completa, entregarla sin esconder lo pendiente. Terminado con definición útil y decisión fundada de acceso o descarte; un listado de enlaces sin lectura del instrumento no satisface el encargo.

## Ejecución, autoridad y concurrencia comunes

Preparado el 17/sep/2026 UTC contra `main @ 402d1a3d0e96f6d159e5c4763bbd93c01f234295` de `Josanoforo/Modelado-Mexicano`. Al ejecutar manda origin/main vigente. Este archivo autoriza su perímetro cuando Jonás lo lanza; no constituye una firma ya registrada ni una adopción científica.

1. Leer el encargo completo, AGENTS.md e instrucciones del perímetro. Reportar worktree absoluto, rama, HEAD y git status --short. Hacer fetch y comprobar si este mismo encargo ya corre o ya está integrado; continuar el trabajo existente si corresponde, sin duplicarlo. Revalidar sólo premisas materiales.
2. Una tarea/worktree/rama/PR. Se puede continuar en la misma conversación CLI. Si la rama anterior fue fusionada, abrir sucesora desde origin/main; preservar cualquier trabajo posterior mediante commits/parches explícitos. No reset/clean/force ni stash de árboles ajenos. No confundir squash merge con falta de integración: comparar contenido pertinente.
3. Resolver corpus mediante tools/entorno.py, raíces locales y las opciones reales de tools/prepara_corpus.py. Ausencia de data/raw en un worktree no demuestra ausencia del corpus. No incorporar microdatos, identificadores individuales, rutas privadas o secretos a Git.
4. Autorizados al lanzar: cambios delimitados, pruebas focales, commits, push sin force y un PR. **Fusiones con Jonás.** Cero comunicaciones externas, cuentas, compras o llamadas experimentales a modelos. CLI para desarrollar no equivale a emitir L.
5. Sincronizar antes del push final, revisar diff/perímetro y ejecutar sólo las verificaciones afectadas. No debilitar checks, no recongelar baseline ni ampliar la tarea a reparar fallos heredados sin efecto material. Si una compuerta exige escribir fuera del perímetro, entregar el producto probado y el impedimento preciso para integración serial. Resolver defectos propios de nomenclatura sin alterar el contenido del encargo archivado.

### Perímetros vivos y reserva

CAREO #827, ENCO #834, remesas/F-3 #835 y ENCRIGE-carga #836 están fusionados al corte. Precisión WBES #837 está abierto: su contenido no se trata como consolidado. ENVIPE-U4-2013-2015, ENCIG2023-FLUJO-Y-ESTIMANDO-1 y MOCIBA-FLUJO-DOCUMENTAL-1 se consideran en curso aunque todavía no aparezca un PR. MEDICION-DEMANDA-3 conserva su dueño.

Opus conserva PILOTO-1/TRÁMITE-4, firmas, corte de edad, crosswalk, θ y adopciones del piloto. **No abrir ni derivar ENIF 2024 localidad × edad**, ni leer sus capturas/resultados reservados. No abrir respuestas MOCIBA/ISSP/ENCO ni olas retenidas de F6. El merge de CAREO no levanta reservas. No ampliar corpus L ni ejecutar herramientas generales que consuman reservas incidentalmente.

Excepción temporal de cascada autorizada por el lanzamiento: archivar este encargo verbatim en el directorio propio, con metadatos de procedencia/consumo fuera del bloque, y entregar producto; diferir decisiones.tsv, no-corrido.tsv, firmas-pendientes.tsv, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar números ADR/NC/FP. No correr /tramite, /despacha, /deriva, cron ni registro --escribe. Sólo F-2 autoriza regenerar su vista específica mediante el escritor canónico; eso no autoriza una cascada global.

Manifiesto: ENIGH admite hasta dos documentos metodológicos nuevos y ENAPROCE hasta seis documentos instrumentales. Son adiciones por identidad, no regeneración completa. Preservar las adiciones concurrentes de ENCIG/MOCIBA/WBES y no duplicar un documento ya registrado. F-2 no toca manifiesto. Cada encargo tiene salidas propias.

### Cierre

Devuelve primero producto, por qué importa y decisión que habilita; después PR y rutas, SHA base/final, comandos realmente ejecutados, pruebas/CI, reservas materiales y máximo tres decisiones pendientes precisas. Distinguir PREPARADO, EJECUTADO, SELLADO, INTEGRADO y ADOPTADO. Un PR no adopta una cifra; un nuevo CALC no crea una fuente independiente.

Incluir **CIERRE COMPARTIDO DIFERIDO** con únicamente las propagaciones necesarias después del trámite de Opus. No convertirlo en otro inventario general. Aproximadamente 20% máximo del esfuerzo en control, salvo riesgo material de datos. Dos intentos razonables, una alternativa directa y receta concreta por bloqueo; continuar piezas independientes. Terminar con producto usable y siguiente acción clara, sin refinamiento por inercia.

## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-ENAPROCE-INSTRUMENTOS-Y-ACCESO-1. Autorizo adquirir hasta seis documentos oficiales faltantes de 2015/2018, registrar sólo esas adiciones, recuperar reactivos/filtros y entregar contrato y fixtures sintéticos donde procedan. Evalúa si R03 justifica acceso institucional usando la política ya acreditada; no vuelvas a buscar una descarga pública de bases reales ni abras ejemplos, microdatos o tabulados. No envíes solicitudes ni autorices F6. Autorizo pruebas, commits, push y PR; fusión conmigo. Conserva reservas y cascada diferida.
