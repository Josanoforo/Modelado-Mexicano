---
archivo_verbatim: true
nombre_propio: GEN2-MOCIBA-FLUJO-DOCUMENTAL-1
fuente_recibida: /mnt/c/Users/PC0/Descargas MX/ENCARGO-GEN2-MOCIBA-FLUJO-DOCUMENTAL-1.md
archivado_el: 2026-09-16
nota: El contenido desde el primer encabezado se conserva verbatim; estos metadatos quedan fuera del bloque recibido.
---

# ENCARGO · GEN2-MOCIBA-FLUJO-DOCUMENTAL-1

**Entorno:** Codex CLI en CAJA; Claude Cloud puede ejecutar el mismo acto si dispone de los FD y acceso a documentación oficial. Una sola sesión, rama y PR. **Producto:** resolver la definición del universo de P12_5 de MOCIBA 2021/2022 con documentación, contrato de elegibilidad y ejecución sintética; cero respuestas reales.

**Corte de preparación:** `Josanoforo/Modelado-Mexicano`, `main @ 018956261ca57fb5fb124f72faaf977e27e4df6e`, 17/sep/2026 UTC. Al ejecutar manda origin/main vigente.

## 1. Resultado que importa

#825 dejó las dos celdas MOCIBA con `FILTRO-NO-ACREDITADO`: el FD acredita P12_5, códigos, FACTOR, UPM_DIS y EST_DIS, pero no el flujo que determina a quién se pregunta P12. La hipótesis «algún P4_01..P4_13=1» no quedó acreditada. Repetir la búsqueda en los mismos FD no resuelve el problema: falta cuestionario o manual de las olas exactas.

Este encargo debe **resolver ese bloqueo documental** y dejar un clasificador de elegibilidad probado sólo con sintéticos. Resolver la definición NO hace elegible M: la regla del motor mide razón de no denuncia por miedo/desconfianza entre no denunciantes de delitos; no es la tasa total de denuncia de ciberacoso. No se inventa un puente ni se usa un complemento para disimular esa diferencia.

El final esperado es «definición resuelta; M sigue sin enlace firmado y no se abre R», o una pieza documental faltante exactamente identificada tras adquisición real intentada. No prometer una familia lista para el duelo sólo por recuperar un PDF.

## 2. Insumos precisos

- `AGENTS.md` e instrucciones del perímetro.
- `forense/notas/2026-09-16-GEN2-F6-FACTIBILIDAD-PREPARACION-1-cierre.md`.
- `forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/spec.md` y `tarjetas.yaml`, sólo lectura.
- `tools/f6_factibilidad_prepara.py` y `tests/test_f6_factibilidad_prepara.py`, como reutilización de preflight y funciones sintéticas; no editar sus políticas para aceptar una candidata.
- `data/reactivos-contexto-verificados-v1_0.tsv`, filas MOCIBA pertinentes, y manifiesto, sin búsquedas generales de resultados.
- FD `mociba_2021_mociba2021_fd`, SHA-256 `375bf7c1bcdbcc9b0716cd3b63fe940906a97783a3b69f2afad35f35950b1e25`, hoja TMOCIBA.
- FD `mociba_2022_mociba2022_fd`, SHA-256 `923fa85a665219200d6c87d1f5af25090870bf91957d16f1008726e78edc396e`, hoja TMociba.

No leer `data/apertura-issp-variables-2026-08-13.tsv`, capturas L, resultados R, distribuciones de MOCIBA ni otros miembros de los paquetes estadísticos. ISSP queda fuera del encargo; la pérdida de cegamiento conocida no se repara aquí.

## 3. Adquisición documental dirigida

1. Comprobar por nombre, id y hash si el cuestionario/manual de cada ola ya está en corpus/manifiesto. No escanear textos de toda la raíz ni ejecutar búsquedas que devuelvan tabulados. Leer sólo la documentación seleccionada.
2. Si falta, buscar en páginas oficiales de INEGI del programa 2021 y 2022, limitando los enlaces a cuestionario, instrumento de captación y manual de entrevista/captación. Máximo **cuatro documentos nuevos** entre ambas olas. Un manual común sirve sólo si acredita explícitamente su aplicación a las dos.
3. No inventar enlaces exitosos ni registrar HTML/403 como PDF adquirido. Guardar bytes, URL oficial, fecha, tamaño y hash cuando exista una descarga válida; registrar sólo esas entradas de manifiesto. Si el cuestionario está escaneado, OCR local acotado a las páginas necesarias, manteniendo el original y verificando visualmente flechas y saltos.
4. No abrir presentaciones de resultados, notas de prensa, tabulados ni resúmenes estadísticos. Usar enlaces oficiales directos documentales cuando estén disponibles. Si una búsqueda o documento muestra incidentalmente resultados del objetivo, detener esa lectura, registrar la exposición sin copiar cifras y conservar la evaluación de reserva para mesa; no declarar LIMPIA por haber evitado repetir el valor.
5. No solicitar acceso, enviar correos, abrir cuentas ni aceptar contratos. Dos intentos razonables y una alternativa oficial directa por recurso bastan. Si CAJA obtiene un bloqueo de red reproducible, entregar las URLs/documentos exactos para Claude Cloud o descarga manual; no duplicar investigación en dos sesiones simultáneas.

## 4. Acreditación por ola

Para 2021 y 2022 por separado, fijar:

- población base, edad, condición de uso de internet y ventana de referencia;
- batería que define exposición, filtros previos y todas las rutas de entrada a P12;
- texto exacto y códigos de P12_5: desenlace, opción de respuesta, multirrespuesta cuando aplique;
- qué códigos significan sí, no, no sabe, rechazo, salto y blanco; no inferir códigos ausentes del FD;
- quién pertenece al universo del desenlace y quién sólo carece de respuesta;
- unidad y ponderador; campos de diseño documentados, sin afirmar que ya está acreditado todo un estimador de varianza;
- diferencias 2021/2022. Una igualdad de nombres no acredita un universo idéntico.

Cada condición del filtro cita documento/hash y página/sección. Si la documentación contradice la tarjeta original, escribir una tarjeta sucesora conservando el antecedente: no sobreescribir el texto para hacer parecer que siempre fue conocido.

El denominador debe distinguir **todos los elegibles** de **elegibles con respuesta válida**. Fijar cuál permite el estimando descriptivo y cómo se declarará no respuesta; no convertir una tasa entre respondentes en tasa de todos los elegibles. Fuera de universo no se codifica como no denunció.

## 5. Contrato y preparación ejecutable, sin microdatos

Crear `forense/produccion/mociba-flujo-documental-1/` con:

1. `flujo-por-ola.md`: evidencia y tabla de decisión documental.
2. `contrato-elegibilidad.yaml`: variables, operadores, códigos, orden de filtros, tratamiento de indeterminación y referencias, con `llamadas_autorizadas: false` y `apertura_R_autorizada: false`.
3. tarjetas sucesoras locales compatibles con el preflight existente, si el contrato lo permite. Mantener la firma pendiente y `enlace_M` no elegible; no cambiar el panel canónico ni la lista de candidatas. Si el preflight requiere las cuatro tarjetas, conservar las otras sin reinterpretarlas y reportar por separado sólo el delta MOCIBA.
4. clasificador pequeño que reciba **filas sintéticas en memoria** y devuelva `ELEGIBLE`, `NO-ELEGIBLE` o `INDETERMINADO` con la razón pertinente; no incluir resolutores de corpus, lectura de microdatos ni cliente de modelo.
5. fixtures expresamente `SINTETICO-NO-MEDICION`, resultado del preflight y dictamen de máximo dos páginas.

El clasificador debe tratar correctamente un sí con otros componentes ausentes, todos no documentados, mezcla de no y desconocido, salto previo, código inválido, desenlace vacío dentro del universo y fuera del universo. **Las expectativas dependen del flujo acreditado**, no de imponer un OR por comodidad. Si una rama es materialmente indeterminada, conservarla como tal.

Ejecutar el clasificador sobre fixtures y el preflight sobre las tarjetas sucesoras. La prueba de cierre exige que la definición pueda mejorar sin hacer pasar simultáneamente M, firma y autorización de emisiones. Añadir pruebas focales de esa frontera sólo en el perímetro propio; no cambiar los estados aceptados del verificador para conseguir verde.

Si ambas olas tienen contrato distinto, entregar ambos. Si sólo una puede acreditarse, terminarla y precisar el documento faltante de la otra; no demorar la pieza ejecutable ni inventar simetría.

## 6. Decisión preparada, no adjudicada

Dictamen por ola:

| Componente | Estados que deben quedar separados |
| --- | --- |
| Universo de P12_5 | acreditado / parcialmente acreditado / falta documento concreto |
| Respuesta real | NO ABIERTA |
| Reserva | conservada según lecturas efectuadas / exposición incidental declarada |
| Enlace predictivo de M | no elegible salvo decisión previa específica localizada; no inferir nueva firma |
| L y R | no autorizados, cero llamadas y cero estimaciones |

Recomendar a mesa el siguiente paso exacto: conservar candidato en espera de un enlace científico pre-R o considerar un uso descriptivo con encargo separado. No redactar un nuevo modelo de ciberacoso, no producir la tasa real, no consumir una ola como baseline ni escoger un desenlace vecino porque el actual no encaje.

La pregunta de cierre es «¿ya sabemos a quién se pregunta y cómo computar su elegibilidad sin mirar R?». Un enlace a un PDF sin el contrato y sus fixtures no satisface el encargo.

## 7. Git, reservas y concurrencia

Una sesión/worktree/rama/PR. Reportar ruta absoluta, rama, HEAD y status; fetch y verificar que el mismo encargo no exista en main/PR. Si la sesión proviene de una rama fusionada, abrir rama sucesora desde origin/main conservando cualquier trabajo posterior mediante commits/parches explícitos. No reset/clean/force ni alterar árboles ajenos.

Permitidos: directorio propio, script/pruebas propios y hasta cuatro entradas documentales precisas al manifiesto. Archivar el encargo verbatim con nombre propio y metadatos fuera del bloque. Mantener originales, payloads estadísticos, FD, panel y preparación v1_0 intactos.

No editar `tools/f6_factibilidad_prepara.py`, motor/milpa, corpus L, marcadores, sellos, vistas globales ni scripts de cron. No abrir ENIF 2024 localidad × edad, respuestas MOCIBA/ISSP/ENCO ni capturas/resultados reservados del piloto. CAREO #827 fusionado no equivale a autorización de R.

Opus conserva PILOTO-1/TRÁMITE-4 y firmas/crosswalk/cortes/θ. ENVIPE 2013/2015 y precisión WBES siguen en curso; #834 ENCO, #835 F-3 y #836 ENCRIGE tienen perímetros propios. ENCIG2023-FLUJO-Y-ESTIMANDO-1 trabaja otra fuente: sólo puede coincidir en adiciones al manifiesto, que se conservan por entrada al sincronizar. No regenerar el archivo entero ni reemplazar entradas concurrentes.

Al lanzar se autorizan adquisición documental pública, cambios delimitados, pruebas, commits, push sin force y PR; **fusión con Jonás**. Cero comunicaciones externas o llamadas experimentales. Excepción temporal de cascada: diferir decisiones.tsv, no-corrido.tsv, firmas, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar numeración; no ejecutar /tramite, /despacha, /deriva, cron ni registro --escribe.

Sincronizar antes del push, verificar diff/perímetro y pruebas focales. No debilitar checks ni recongelar baseline. Si CI exige escritura compartida fuera del alcance, señalarla para integración serial. Aproximadamente 20% máximo del esfuerzo en control salvo riesgo material; no abrir una auditoría de todo F6.

Devolver producto, decisión que desbloquea, PR/base/HEAD, comandos y pruebas reales, reservas y **CIERRE COMPARTIDO DIFERIDO**. Distinguir adquisición, definición, elegibilidad experimental y autorización. Terminar cuando el contrato sea usable o quede documentada la dependencia externa exacta.

## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-MOCIBA-FLUJO-DOCUMENTAL-1. Autorizo adquirir hasta cuatro documentos oficiales de cuestionario/manual MOCIBA 2021/2022, registrar únicamente sus adiciones al manifiesto y resolver el flujo hacia P12_5 por ola. Entrega contrato de elegibilidad, clasificador y fixtures sintéticos ejecutados, tarjetas sucesoras locales y preflight sin abrir respuestas. Conserva M no elegible y firma/llamadas/R no autorizados; resolver el filtro no autoriza F6. No abras tabulados, microdatos, ISSP, ENCO ni el piloto. Autorizo commits, pruebas, push y PR; fusión conmigo. Aplica cascada diferida y preserva los perímetros paralelos.
