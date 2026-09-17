# Archivo de encargo · GEN2-ENCO-DOS-OLAS-RESERVADAS-1

Procedencia: archivo entregado por Jonás en la sesión CAJA; ruta privada no reproducida en el producto.
Consumo: 16/sep/2026 America/Mexico_City (emisión declarada 17/sep/2026 UTC).
SHA-256 del archivo recibido: `5a76d586e9602adabec52b0342b16a09e7f52e36e97ef38aa6de7969aa25d626`.
Estado: `CONSUMIDO-PARA-EJECUCION`; la transcripción siguiente es verbatim.

## Texto del encargo (verbatim)

# ENCARGO · GEN2-ENCO-DOS-OLAS-RESERVADAS-1

**Entorno:** Codex CLI en CAJA con acceso a descargas oficiales.  
**Resultado:** dos olas ENCO adquiridas, identificadas y reservadas, más un contrato documental y preparación sintética que indique con exactitud qué permitirían medir y qué falta para compararlas con M. **Este encargo no abre sus respuestas ni ejecuta el duelo F6.**

## 1. Hueco que se resuelve

`forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv`, fila `R10-DIN-ENCO-AHORRO`, identifica una candidata del dominio DIN con reactivo ya localizado y adquisición de dos olas pendiente. `data/manifiesto.yaml` registra solamente `enco_2026_agosto_dbf` y `c_enco_b_v4` para esta ruta en el corte consultado.

El cuestionario, ítem 10, pregunta posibilidades actuales de ahorrar; el panel documenta 1=Sí, 2=No, 3=No sabe, 4=No tiene ingresos. **Esto no mide tenencia de ahorro.** No copiar la afirmación del panel de que sólo falta adquisición como si ya acreditara equivalencia de estimandos. El código debe confirmar además quién responde: no dar por hecho que la respuesta de una persona seleccionada es un atributo de todos los integrantes del hogar.

Insumos de sólo lectura:

- Fila R10 y reservas del panel vigente; `forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/` únicamente para interfaces y límites generales, no resultados de R01/R09.
- `c_enco_b_v4`, SHA `f7e9d6b99e927a29535a85b1d1aac955764c2b38f0726627f7dfd2100323cda6`.
- Identidad de agosto 2026: `enco_2026_agosto_dbf`, SHA `5eb3fd6850c6cb7713640196e4977b077ebb95f8234c1c8ddbbfffdc8984b19d`. **No abrir ese DBF**: queda como ola de control declarada por el panel.
- Demanda de adquisición y reserva vigente pertinente: buscar R10/ENCO en la proyección, cola y actos sucesores; distinguir ENCO de ENCOAP 2023, instrumento distinto y expuesto.

## 2. Fijar las fechas sin mirar las cifras

Primero verifica si una instrucción vigente ya fijó dos olas y las encargó/adquirió. En ese caso usa esas fechas y coordina con la ejecución existente sin duplicarla. Si sólo hay una petición genérica sin fechas, **este lanzamiento fija junio 2025 y junio 2026**, elegidas por mismo mes, separación anual y exclusión de agosto 2026, no por el valor del ahorro. Registra la elección y roles antes de solicitar paquetes.

La pareja queda reservada para factibilidad posterior; ambas siguen sin abrir y ninguna es automáticamente holdout confirmatorio. Dos meses de una encuesta son una familia; el panel rotatorio puede producir dependencia, que la documentación debe describir. Igual mes no demuestra igualdad de cuestionario ni elimina cambios de diseño.

Si falta publicación de una de las fechas o cambia la batería, no recorrer otros meses hasta hallar el desenlace deseado: entrega la ola conseguida y el impedimento, sin sustitución de fechas no autorizada. Una nueva decisión temporal puede tomarse después sin perder lo adquirido.

## 3. Adquisición efectiva y reserva

1. **COMMIT 1:** reserva documental de las dos fechas, propósito, objetos permitidos/prohibidos y receta de adquisición. No esperar a obtener tasas para escribirla.
2. Consultar manifiesto y raíz del corpus; si el objeto ya existe y coincide en identidad, reutilizarlo. Revisar la ejecución del servicio de adquisición para evitar dos dueños del mismo objetivo. Reutilizar su mecanismo de exclusión y presupuesto cuando aplique; no reiniciar presupuesto, saltar reservas o modificar cron. Si la cuota aplicable está agotada, preparar el comando acotado para su siguiente ventana y seguir la documentación/sintéticos, declarando adquisición pendiente, no realizada.
3. Localizar los enlaces reales desde la página/API oficial de INEGI. No fabricar URLs por sustitución de mes y dar un HTTP 200 por adquisición. Descargar **dos paquetes mensuales como máximo**, más hasta dos documentos estructurales que sean imprescindibles y todavía falten. Sin cuentas nuevas, contratos, pagos ni solicitudes a terceros. Una descarga final por objeto y validación de integridad suficientes salvo contrato vigente material distinto; no descargar todo el histórico.
4. Validar identidad por URL final, tipo, tamaño, SHA y contenedor; listar miembros sin imprimir registros. Se permite leer cabecera de DBF para nombres/tipos y metadatos de estructura; **no filas, frecuencias, mínimos/máximos, marginales, tasas, previews ni muestras**. No cargar una tabla completa con una librería para luego decir que sólo se miró su cabecera. Rechazar HTML disfrazado de ZIP, errores internos y periodo/documentación discordantes.
5. Depositar bytes en la raíz duradera de corpus que el proyecto ya usa, con ruta propia, sin sobreescribir otro objeto ni agregar respondentes a Git. No ponerlos en una carpeta que los indexadores generales de L consuman: conservar la reserva explícita en el mecanismo existente. Si éste no garantiza que la rutina omita las respuestas, mantener los paquetes en área reservada existente fuera del escaneo general y declarar esa ruta lógica. No crear una automatización nueva.
6. **COMMIT 2:** recibos y entradas aditivas de manifiesto con fecha, procedencia, periodo, SHA, tamaño y estado de reserva. No afirmar `OBTENIDO` sin bytes ni que `testzip` acredita semántica. Entradas nuevas únicas; no reemplazar agosto 2026. Esta es la única excepción estrecha de este acto a la prohibición general de modificar manifiesto. Resolver adiciones concurrentes conservando ambas; no ejecutar regeneraciones globales ni promover resultados al corpus L.

## 4. Preparación documental y técnica

Con documentación de esas fechas, confirmar: P10 o su equivalente exacto, universo y unidad de respuesta, filtro, códigos especiales, factor, diseño, rotación de muestra, cobertura y comparabilidad interanual. Extraer sólo estructura del DDI si incluye estadísticas; exposición accidental se documenta y retira la pretensión de cegamiento de la pieza afectada.

Escribir una spec propuesta **PREPARADA-NO-AUTORIZA-RESPUESTAS-NI-EMISIONES**, con:

- Estimando sugerido: proporción que responde Sí a posibilidades de ahorrar en el universo elegible. Incluir No y No tiene ingresos en el denominador de respuestas sustantivas si el instrumento confirma esa semántica; No sabe/faltante se reporta por separado, nunca recodificado en silencio. Distinguir universo completo de un posible escenario restringido a personas con ingresos, sin escogerlo por resultado.
- Misma regla en ambas fechas sólo si la estructura la sostiene; transformaciones explícitas, peso y manejo de diseño/estratos singulares. Ausencia de varianza operativa se declara sin inventarla.
- Comparación con `dinero.ahorro.tiene_ahorros`: el salto entre stock existente y posibilidad percibida no está identificado. No definir `P(posibilidad)=P(tenencia)` ni complementar por comodidad. Si M carece de enlace preexistente, marcar `M-NO-ELEGIBLE-PARA-ESTE-ESTIMANDO`. Preparar una medición descriptiva posterior sigue siendo útil; no disfrazarla de transferencia.
- B: la ola anterior podría servir de persistencia únicamente para el mismo estimando, una vez autorizada su lectura y resuelto el orden de emisiones. No consumir junio 2025 para fabricar B durante este encargo. Aclarar que abrirla luego puede afectar la reserva.
- Presupuesto posterior: posiciones y candidatos sólo si existen elegibles; ninguna llamada ahora. No diseñar otra batería F6 ni ampliar el panel global. Conservar por separado adquisición completa, definición completa y elegibilidad experimental.

Añadir tarjetas legibles y una función/preflight pequeño con fixtures exclusivamente sintéticos; reutilizar interfaces sin modificar `tools/f6_factibilidad_prepara.py`. Pruebas: códigos especiales, sin ingresos, denominador vacío, pesos inválidos, escala y lectura accidental prohibida. No producir un CALC real, un R ni un número de ahorro. Pruebas sintéticas nunca deben incluir el valor objetivo publicado.

## 5. Entregables y perímetro

- `forense/produccion/enco-dos-olas-reservadas-1/`: reserva inicial, recibos, spec, tarjetas, sintéticos y cierre de una página. El resumen debe indicar por fecha: bytes presentes, identidad, reserva, definición, falta concreta para medir y para comparar con M.
- Un adaptador autónomo `tools/enco_reserva_prepara.py` y prueba específica sólo si hacen falta; prohibido leer respondentes en su modo de preparación.
- `data/manifiesto.yaml`: sólo las entradas nuevas de las dos olas y documentación efectivamente adquirida; ninguna edición incidental. Se deja fuera cualquier mecanismo que obligue a indexar las respuestas reservadas.
- Encargo verbatim y cierre propios. Sin panel F6, cola global, inventarios globales, CALC reales, motor o decisiones.

No termines en “hay que adquirir dos olas” si el acceso está disponible: adquiere y deja los objetos utilizables bajo reserva. Si el acceso falla, conservar recibos y entregar la petición/comando exactos; no declarar cumplida esa parte. Una vez adquiridas, la decisión siguiente es autorizar medición descriptiva o aprobar un enlace científicamente defendible para M; este acto no decide ese enlace.

## Autoridad, arranque y trabajo simultáneo

Encargo para lanzar por Jonás · emitido 17/sep/2026 UTC (la sesión en CDMX puede seguir fechada 16/sep). Repositorio: `Josanoforo/Modelado-Mexicano`. Base consultada: `main @ 4fff914f286021574ac0897273ee0e6971b38f04`. Las premisas descritas corresponden a ese corte; al ejecutar manda `origin/main` vigente. Este documento no es una firma ya registrada: su prompt final define lo autorizado al lanzarlo.

1. Lee este archivo completo, `AGENTS.md` y las instrucciones aplicables a los archivos del perímetro. Reporta worktree absoluto, rama, HEAD y `git status --short`. Haz fetch y consulta PR/ramas del rótulo para no duplicar una ejecución. Revalida sólo las premisas materiales.
2. **Puedes continuar en la misma sesión CLI.** Si su PR anterior fue fusionado, usa un worktree y una rama sucesora desde `origin/main` para este encargo. No reaproveches el nombre de una rama fusionada para esconder un acto nuevo. Si hay cambios posteriores sin publicar, consérvalos: determina con diff cuáles corresponden a este encargo y traslada sólo esos cambios con commits/parches explícitos, sin reset, limpieza ni stash de árboles ajenos. Si ya corre exactamente este encargo, continúa su rama y PR; no abras un duplicado. Un squash merge no acredita ancestralidad por sí solo: compara el contenido pertinente.
3. No ejecutes este encargo encima de otro todavía activo. Sincronizar cambios propios y resolver conflictos locales de implementación está autorizado; no interpretar una contradicción científica como conflicto de texto resoluble automáticamente.
4. Los corpus se resuelven con `tools/entorno.py`, las raíces existentes y `tools/prepara_corpus.py` según sus opciones reales. Un worktree sin `data/raw` no significa que falten archivos en CAJA. No copies microdatos a Git ni expongas rutas privadas, credenciales o identificadores individuales en entregables.
5. Al lanzar quedan autorizados los cambios delimitados, pruebas pertinentes, commits, push sin force y un PR por encargo. **Las fusiones quedan con Jonás.** No enviar correos, mensajes ni solicitudes a terceros. Cero llamadas de brazos experimentales a modelos; usar CLI para desarrollar no equivale a emitir L.

### Separación respecto del trabajo en curso

Opus conserva CAREO / CELDA-D-PILOTO-1 / TRÁMITE-4, firmas, crosswalk, corte de edad, θ y magnitud de G5. Las sesiones existentes conservan ENCIG2023-AGREGADO-CONDICIONAL-1 y ENVIPE-RES0028-DERIVADO-U4-1. No intervenir sus archivos ni rehacer sus resultados. F6 mantiene su preparación y sus reservas.

**No abrir ni derivar ENIF 2024 localidad × edad**, ni leer las capturas o resultados reservados del piloto. No leer desenlaces retenidos de MOCIBA/ISSP, ENCRIGE 2016 ni WBES 2026. Antes de correr comandos generales, comprobar que no abran/deriven esas reservas como efecto lateral. El corpus de los brazos L no se amplía.

Excepción temporal de cascada autorizada al lanzar: archivar el encargo verbatim con procedencia/consumo fuera del bloque y publicar su producto, pero diferir `decisiones.tsv`, `forense/no-corrido.tsv`, firmas, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar numeración ADR/NC/FP. No ejecutar `/tramite`, `/despacha`, `/deriva`, cron ni `registro --escribe`. Cada PR enumerará únicamente las propagaciones necesarias después del trámite de Opus, bajo **CIERRE COMPARTIDO DIFERIDO**. La excepción puntual para manifiesto, si existe, se indica en el perímetro específico.

Una modificación de SHA o un defecto de nomenclatura no detiene el producto. Resolver un bloqueo con uno o dos intentos razonables, una alternativa directa y una receta concreta; continuar las piezas independientes. No ampliar a auditoría general. Aproximadamente 20% del esfuerzo como máximo en control, salvo riesgo material de datos.

## Cierre y entrega comunes

Sincroniza `origin/main` antes del push final; revisa diff y ejecuta las verificaciones afectadas. No rehagas mediciones por cambios documentales. No debilites checks ni recongeles baseline. Compara fallos heredados con la base sólo cuando afecten la entrega; corrige dependencias declaradas del entorno antes de atribuir el fallo al código. Si CI exige una escritura compartida fuera de alcance, entrega el producto probado y el impedimento exacto para integración serial, sin fingir verde.

Devuelve: qué producto cambió y qué decisión permite; enlace al PR y artefactos; SHA base/final; comandos realmente ejecutados; pruebas/CI; reservas materiales y máximo tres decisiones pendientes con su objeto preciso. Distingue PREPARADO, EJECUTADO, SELLADO, INTEGRADO y ADOPTADO. Un PR o un sello no constituye adopción científica. Una tabla de planes sin ejecutar lo disponible no satisface el encargo.

Termina cuando exista el producto usable y siguiente acción clara; no refines por inercia. Explica en una frase si quedó más cerca una medición, explicación o decisión mejor.

## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-ENCO-DOS-OLAS-RESERVADAS-1. Autorizo adquirir las dos olas seleccionadas por su regla prospectiva y la documentación imprescindible desde fuentes públicas, preservando cuotas/reservas aplicables, sin abrir respuestas. Autorizo registrar sólo las nuevas identidades de manifiesto, preparar spec/tarjetas/sintéticos en su perímetro, commits, push y PR; fusión conmigo. Las fechas supletorias son junio 2025 y junio 2026 si ningún acto vigente fijó otras. No abras agosto 2026, no ejecutes F6 ni equipares posibilidad con tenencia de ahorro. Aplica la cascada diferida con la excepción aditiva de manifiesto indicada. Conserva trabajos previos de la sesión y usa rama sucesora si su PR ya fue fusionado. Devuelve bytes reservados realmente adquiridos y el contrato completo o el bloqueo puntual de cada pieza.
