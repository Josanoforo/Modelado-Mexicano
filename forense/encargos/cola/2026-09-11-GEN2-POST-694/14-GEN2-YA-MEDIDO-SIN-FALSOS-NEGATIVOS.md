# ENCARGO · GEN2-YA-MEDIDO-SIN-FALSOS-NEGATIVOS

ENTORNO: NUBE
COMPUERTA: PR #694 fusionado; sin tarea/PR del mismo objeto.
RAMA: acto/gen2-ya-medido-tasas
MODELOS: cero llamadas nuevas.

## Resultado útil

Hacer que `tools/ya_medido.py` reconozca tasas ya medidas y cite la evidencia propia de cada regla. Evitar que los encargos actuales vuelvan a medir algo por un falso “NUNCA-MEDIDA”. Resolver NC-0109 y NC-0129 sin ampliar la herramienta a un motor de búsqueda nuevo.

## Defecto reproducido al preparar el encargo

En main `4816101`, estos dos comandos terminan en `NUNCA-MEDIDA` aunque listan medición/adopción de la regla:

```bash
python3 tools/ya_medido.py tramite.mordida.con_registro
python3 tools/ya_medido.py dinero.ahorro.horizonte_no_corto_con_seguridad_social
```

La causa asentada en NC-0109/0129 sigue vigente: el detector privilegia vocabulario de falsación y no identifica adecuadamente una tasa medida. La ventana de ±260 caracteres también puede perder evidencia del mismo bloque. El caso `tramite.gobierno_digital.util_sin_coercion` hoy imprime MEDIDA-EN, pero lo hace citando la nota que describe el defecto; no afirmar que ese contraejemplo sigue fallando exactamente igual.

NC-0129 apunta a NC-0110 como supuesto duplicado; la causa de herramienta corresponde a **NC-0109**. NC-0110 es el recorte de canales, está CERRADA y no se reabre.

## Fase 1 · Contrato de evidencia mínimo

Leer la herramienta completa, los dos NC, el cierre de GEN2-LOTE-ENCIG-1 y el de GEN2-LOTE-ENIF-1, y las entradas efectivas de las dos reglas. Distinguir: tasa ejecutada y citada; intento con veredicto NO-ESTIMABLE; adopción al motor; hipótesis/propuesta; mera mención. Mantener compatibilidad de la salida que consume T-YAMEDIDO; no convertir `MEDIDA-EN` en garantía de validez o adopción.

Un número `p`, una palabra MEDIDO en prosa, un plan de corrida o un RESULT declarado sin ejecución no bastan para acreditar medición. Resolver las referencias existentes de consumidor → CALC/RESULT/ejecución/sello cuando estén disponibles; conservar los antecedentes GEN1 con su procedencia. Usar directamente los artefactos sellados si las vistas están retrasadas; 09 está publicándolas y no es compuerta para este arreglo.

## Fase 2 · Reparación pequeña

Corregir el reconocimiento de medición y la delimitación estructural del bloque de la regla. No sustituir la ventana por búsqueda indiscriminada de todo el archivo: eso atribuiría el veredicto de una regla vecina. Identidad exacta y alias declarados, sin parecido de nombres. Las notas que diagnostican una falla pueden ser antecedentes, pero la salida debe poder citar la evidencia sustantiva que la resuelve.

No introducir embeddings, otra base de datos, índices persistentes o un inventario global. No modificar `tools/corrida0.py`, `milpa/*.yaml`, los CALC ni la clasificación científica de ninguna regla.

## Fase 3 · Pruebas que protegen el defecto

Fixtures pequeños para: tasa ejecutada con evidencia exacta; propuesta con p pero sin ejecución; dos reglas vecinas con veredictos diferentes; evidencia pertinente más allá de 260 caracteres; alias declarado; intento NO-ESTIMABLE sin confundirlo con parámetro disponible. Reutilizar los controles positivos y negativos existentes. La prueba no debe depender del conteo total del repo.

Ejecutar los dos comandos reales de arriba después de la corrección y comprobar que citan su evidencia, además de un negativo legítimo. Confirmar que la herramienta es de lectura y no modifica demanda/vistas. Verificar la integración con T-YAMEDIDO sin convertir nuevas advertencias documentales en bloqueos científicos.

## Fase 4 · Cierre y entrega

Cerrar NC-0109 y NC-0129 por corrección ejecutada; rectificar el enlace errado de NC-0129 conservando su antecedente. No cerrar NC-0110 otra vez ni reabrirla. Un solo PR con el script, pruebas pertinentes y cierre.

Puede fusionarse antes o después de 09. Los seis encargos actuales deben incorporar el arreglo desde main cuando esté fusionado; no copiar el script entre ramas activas ni detener mediciones ya bien identificadas para esperarlo.

## Perímetro y aceptación

`tools/ya_medido.py`; pruebas propias y referencia T-YAMEDIDO sólo si la interfaz lo exige; NC-0109/0129 y administración común. Cero cambios de medición, motor, inventario de reactivos, cron o vistas corrida0.

Aceptación: desaparecen los dos falsos negativos reproducidos; una hipótesis con p sigue sin acreditarse como ejecutada; no se confunden veredictos vecinos; cada positivo muestra una fuente pertinente; cierre trazable sin otra capa de control. D-14: evita el error ya ocurrido de redescubrir reglas medidas y cuesta menos que otro sondeo/cálculo duplicado.

## Contrato común, incluido para ejecutar este archivo por separado

Autoridad: decisiones de mesa asentadas por #685 y solicitud de revisar decisiones y preparar trabajo adicional mientras corren los encargos 07R/09–13. Este documento es un encargo preparado por ChatGPT: se ejecuta cuando mesa lo entregue a Codex. No convierte recomendaciones metodológicas pendientes en firmas. Base consultada: `origin/main=4816101e506f527d018dd2c47467a8b57bfbd487`, 11/sep/2026 UTC. El corte incluye #694, que encoló el paquete anterior la noche del 10/sep en México; sus seis tareas están declaradas en curso por mesa. `main` acredita lo consolidado; un PR abierto acredita trabajo en curso.

**Arranque y autorización operativa.** Lee `AGENTS.md`, este archivo completo, las instrucciones vigentes y `.claude/commands/acto.md` en lo aplicable; Codex ejecuta sus comandos equivalentes sin necesitar Claude. Reporta ruta absoluta, rama, HEAD y estado. Usa un worktree propio desde el clon existente; consulta main, ramas, worktrees y PR del mismo objeto antes de crear trabajo duplicado. Continúa una rama compatible cuando proceda. Archiva el encargo por 0-bis A.3. Al lanzarlo quedan autorizados sus cambios, commits, push y PR propio revisable; **el merge pertenece a mesa**. No cerrar PR ajenos, borrar worktrees, descartar cambios ajenos ni modificar el candado de `/despacha`.

**Entorno.** `ENTORNO` en la cabecera identifica dónde terminar. Cloud/NUBE puede trabajar código, documentos públicos y resultados agregados. Los microdatos se abren únicamente en CAJA/Ubuntu, según el repo. Usa `tools/entorno.py` y las raíces configuradas; enlaza correctamente el corpus compartido antes de concluir que falta. No inventes rutas Windows/WSL, no copies microdatos ni credenciales a Git. Si una capacidad falta, completa las fases independientes y entrega la continuación exacta; no confundas NO-VERIFICABLE con AUSENTE. Dos intentos razonables y una alternativa bastan para registrar un bloqueo.

**Concurrencia e integración.** Estas son tareas manuales separadas; no cambian la regla de una sesión del despacho automático. Verifica compuertas por ascendencia y producto, conforme a ADR-277, no buscando un título en el log. No reserves números de ADR/NC/FP: derívalos contra main al cerrar. Se aplica el precedente ya utilizado en #687–#693: **quien fusiona después renumera**. Integra main en tu rama, conserva las filas ajenas por identidad y significado y reconcilia referencias del acto; nunca reemplaces un TSV completo por la copia vieja de tu rama. Los IDs que aparecen abajo son los definitivos en main al corte, no los candidatos antiguos del cuerpo de un PR.

Usa `tools/cierre_acto.py` primero en seco y luego `--aplica` cuando corresponda para la cascada existente. Conserva una única ancla L0. Ejecuta las pruebas materiales sobre la integración final; verifica también la sincronización del HEAD remoto mediante el procedimiento vigente de `/acto`. Un push posterior a la revisión requiere comprobar su delta pertinente. Serializar merges, no necesariamente todos los trabajos.

**Perímetro administrativo permitido.** Copia archivada de este encargo, una nota de cierre, sus filas de `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`, cola y decisiones cuando corresponda, y la cascada existente en `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_12.md`, `canon/registro-rotulos.tsv`. Resolver renombres al lanzamiento. No crear otra plantilla, índice, tablero o ADR de política para problemas ya cubiertos. Modificar las vistas globales sólo si el encargo lo incluye; de otro modo entregar comprobantes al responsable de publicación.

**Medición y decisiones.** Corre `tools/ya_medido.py <regla>` antes de clasificar o medir una regla; conserva la salida pertinente. Para una medición nueva, congela pregunta, universo, codificación, unidad, ponderador, exclusiones, método y aceptación en un commit previo al primer resultado. Un diagnóstico posterior a ver datos se etiqueta exploratorio; no se vende como prueba confirmatoria. Usa el flujo `spec-check → preflight → run → verify` cuando corresponda. Verifica fuente, periodo, muestra, transformación y relación con el parámetro. Preserva specs, resultados, snapshots y sellos históricos; una sucesora no reescribe su antecedente. Un mismo número reutilizado o un replay técnico no es otra medición independiente. `cuenta_gen2` sigue las firmas y reglas existentes; los CALC científicos nuevos explicitan objeto y cita. **Contar, reproducir, validar independientemente y adoptar son actos diferentes.**

**Límites de gasto y comunicación externa.** Salvo el ejecutor productivo configurado del cron, estos encargos no requieren llamadas nuevas a modelos. No cambiar proveedor ni abrir gasto de API para destrabar una tarea. Las vías comerciales de tandas siguen diferidas. Preparar solicitudes no autoriza firmarlas, aceptar acuerdos o enviarlas en nombre del usuario. No fabricar identidad, afiliación o recepción. Si una fase exige una decisión científica aún abierta, dejar producto y opciones concretas; continuar las demás.

**Pruebas y parada.** Validar primero el resultado material; correr el baseline requerido sin ampliarlo para ocultar fallos. No perseguir los tres FAIL históricos por rutina. No volver a arreglar NC-0141/0148: #690 ya lo hizo. Revisar el diff después de las pruebas y añadir sólo archivos deliberados. D-14: cualquier automatización adicional debe evitar un error observado con efecto material y costar menos que su corrección repetida; si no, resolver directamente. Auditoría aproximadamente 20%, salvo riesgo material en números, identidad o decisión.

Avanza entre fases ya autorizadas sin pedir confirmación. Termina cuando entregues el resultado suficiente o un residual externo concreto. Cadena de cierre: autorización → producto → evidencia → consumidor cuando aplique → obligaciones → vistas/cola → PR → merge de mesa. Una fila mixta conserva su parte pendiente. No cerrar por palabra coincidente ni por recomendación. Respuesta final del ejecutor: resultado útil, fases cumplidas/pendientes, PR/SHA, pruebas, y tabla `obligación | evidencia | cerrada/residual | siguiente acción`.

## NO-CORRIDO / RESERVAS

Ninguna fase material quedó sin ejecutar. La fusión del PR permanece, por
contrato del encargo, reservada a mesa y no constituye una medición pendiente.

## CONSUMIDO

Ejecutado el 10/sep/2026 en la rama `acto/gen2-ya-medido-tasas`; entrega
revisable en **PR #705**. El archivo fue archivado inicialmente por A.3 en
`002bb80`; al aparecer esta copia oficial byte-idéntica en `main`, la copia
duplicada se retiró del árbol final y permanece recuperable en ese commit.

Producto `b789cca`: `tools/ya_medido.py` reconoce identidad estructural y
resuelve RESULT + ejecución + sello. Los dos falsos negativos terminan en
`MEDIDA-EN` citando `CALC-ENCIG-0001` y `CALC-ENIF-0001`; el negativo legítimo
permanece `NUNCA-MEDIDA`. Cierre `49004ec`, integración `da4bdc9` y
reconciliación `9f0019d`: `NC-0109`/`NC-0129` cerradas, `NC-0110` intacta y
acto renumerado a ADR-466.

Validación sobre `origin/main=7d55234`: 8/8 regresiones dirigidas OK;
`tests/check.py --baseline` terminó con código 0 y `LÍNEA BASE: VERDE`, con
T02/T15/T25/T30/T30b en `ok`. Las cinco huellas de demanda/vistas corrida0
fueron idénticas antes y después. No hubo medición, cambio científico, llamada
a modelos ni escritura de vistas. El único residual es la fusión por mesa.
