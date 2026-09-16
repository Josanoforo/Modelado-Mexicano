# ENCARGO · GEN2-DERIVADOS-CORRECTIVO-Y-DESPLIEGUE

Fecha: 16 de septiembre de 2026.
Repositorio: `Josanoforo/Modelado-Mexicano`.
Ejecutor: Codex CLI en CAJA, con corpus montado y acceso efectivo a Windows/WSL. No requiere Opus ni llamadas a modelos durante la rutina.
Producto: un PR correctivo pequeño, con derivación fiable y comprobación del despliegue. Las fusiones quedan con Jonás.

## 1. Objetivo y estado de partida

Completar la rutina determinista de derivados para que produzca un universo y tablero vigentes, detecte correctamente cuándo nada cambió y comunique fallos reales. Terminar la integración operativa solicitada; no entregar otra propuesta de instalación.

Consulta realizada al preparar este encargo: `origin/main` estaba en `1366d65b9a75046bdf0310b2ab0768558386f27a`, con #814 (derivados) y #815 (panel F6) fusionados. Los defectos siguientes siguen presentes en `tools/deriva_cron.sh` de ese corte:

- Lee `snapshot_t0_sha256` del resumen anterior, aunque escribe `snapshot_sha256_del_dia`.
- Actualiza `main` y luego cambia a una rama diaria existente sin incorporar necesariamente ese `main`.
- Ignora los fallos de universo y tablero con `|| true`; captura los códigos de registro/status sin hacerlos determinar el resultado final.
- En `NADA-QUE-HACER` intenta borrar la rama diaria con `git branch -D`, aunque puede contener commits pendientes.
- Puede informar éxito aunque no haya logrado abrir el PR requerido.
- El registro §11 propone una tarea independiente y declara que no fue instalada. El encargo original pedía compartir scheduler y launcher.

Son premisas que debes actualizar al comenzar, no instrucciones para repetir correctivos que ya se hayan integrado. Lee `AGENTS.md`, el encargo original `forense/encargos/2026-09-16-GEN2-RUTINA-DERIVADOS-1.md`, el runner, launcher y runbook pertinentes. Reporta ruta, rama, HEAD y estado del worktree. Usa un worktree propio desde `origin/main` vigente.

No reabrir F6 ni el contrato de adquisición corregido por #813. No integrar ni borrar ramas administrativas o censos históricos dentro de este encargo. Los ZIP de agosto no son necesarios.

## 2. Corregir comparación, conservación y propagación de fallos

### Universo

Normaliza la lectura de la huella: reconoce el campo del T0 original y el del resumen fechado. Usa una representación consistente para las nuevas salidas sin reescribir históricos. Un campo ausente o inválido debe dar diagnóstico explícito; no debe convertirse silenciosamente en «el universo cambió».

Con iguales insumos, dos ejecuciones consecutivas deben dar el mismo resultado sustantivo. La segunda no crea otro snapshot ni un commit por fecha, timestamp o metadatos autorreferentes. Si hay cambios reales durante el mismo día, conserva la evidencia anterior conforme a la convención existente; no destruyas la comparación de referencia.

Completa la parte pendiente del encargo original: arrastrar inspecciones por identidad/hash con el mecanismo existente y mostrar separadamente activos declarados, adquiridos e inspeccionados. Verificación local de identidad no equivale por sí sola a inspección. No inventes un porcentaje de inspección a partir de archivos adquiridos. Si el ledger no permite una cuenta comparable, presenta el dato disponible y la limitación precisa. T0 y sellos previos permanecen intactos.

### Árbol efectivo y ramas

Deriva sobre un árbol que contenga el corte actualizado de `origin/main`, incluidos los commits útiles de una rama diaria existente. No basta actualizar `main` y después ejecutar sobre una rama antigua. Haz la sincronización antes de ejecutar las derivaciones y su gate; registra el SHA efectivo.

Conserva trabajo concurrente. No uses `checkout -B`, `reset --hard`, `clean`, force-push ni borrado de ramas para resolver colisiones. Si la rama está ocupada, utiliza el mecanismo de aislamiento ya disponible o informa el paro concreto conservando el trabajo. Evita cambiar de rama en un clon usado por adquisición u otra sesión: un lock propio de derivados no protege el árbol frente a otro servicio.

`NADA-QUE-HACER` significa cero cambios nuevos: no autoriza borrar la rama diaria ni abandonar commits que todavía deban publicarse. Distingue «sin cambios y sin publicación pendiente» de «sin cambios nuevos, pero con commits/PR pendientes». Reutiliza el PR diario existente. Si ya fue fusionado y no hay cambios nuevos, no abras otro; si aparecen cambios sustantivos posteriores, conserva su evidencia para la siguiente publicación conforme al límite vigente de un PR diario.

### Resultado y publicación

Propaga errores de universo, tablero, registro y publicación. Examina la semántica real de los códigos de `registro --verifica`: un diff esperado no debe confundirse con fallo de ejecución. El recibo final debe reflejar lo ocurrido y la fase afectada. Un cálculo fallido no puede terminar como éxito ni `NADA-QUE-HACER`.

Ante fallo de una derivación obligatoria, conserva la evidencia local y no publiques salidas parciales como una actualización completa. Un fallo de push o apertura/actualización de PR deja publicación pendiente con código de fallo y receta concreta, sin perder commits locales. No consumas cambios ajenos ya staged; añade sólo los archivos del acto.

Mantén locks y heartbeat con dueño efectivo, el cierre legible y el código de salida hasta Windows. Reutiliza la infraestructura existente; no crees un framework de ejecución.

## 3. Completar el cableado y despliegue en CAJA

La instrucción de mesa sigue siendo aprovechar el scheduler y launcher existentes. Corrige la sustitución unilateral por una segunda tarea meramente propuesta. Integra la derivación diaria de forma determinista, con lock propio y árbol aislado, sin supeditarla a que adquisición encuentre necesidades elegibles o tenga presupuesto para investigar. Una activación horaria no debe repetir una derivación diaria ya completada sin cambios pertinentes.

El acoplamiento debe ser mínimo y conservar el funcionamiento del servicio de adquisición: no alterar sus horarios, modelo, presupuesto, cursores, reservas ni política de selección. No convertir esta rutina en una invocación a Codex/Claude. Si el launcher requiere un pequeño tramo de coordinación para independizar ambas salidas, está dentro del perímetro; no añadas otro scheduler por comodidad.

Comprueba el instalador/configuración y el comando que Windows ejecuta realmente. Usa la vía Windows/WSL ya disponible; no declares que falta acceso al host sólo por estar dentro de WSL. Un impedimento real de permisos debe reportarse con el comando y resultado, sin eludir controles.

Publica el correctivo y verifica su SHA remoto exacto. Despliega mediante el mecanismo existente que permite fijar una revisión pendiente de merge, si está disponible y es aplicable. Distingue revisión publicada, cargada por el proceso e integrada en `main`. No hagas que un fetch/pull interno restaure el runner antiguo durante la prueba. Tras fusión debe retomar `main` por la vía existente; no dejar una fijación permanente.

Realiza una ejecución controlada del recorrido corregido en CAJA y una repetición sin cambios. Para verificar scheduler utiliza una activación controlada del tramo determinista, sin nuevas llamadas adquisitivas ni descargas; si hace falta un selector mínimo de ese tramo, inclúyelo. No dispares a ciegas el cron completo. Registra fielmente si la activación fue manual o por trigger: establecer una variable `windows-task-scheduler` no prueba por sí solo un disparo programado.

Si no existe una vía segura para cargar el SHA del PR antes del merge, entrega el PR listo, la comprobación local real y el comando exacto para completar el despliegue después de la fusión. No lo marques instalado ni operativo hasta acreditarlo. La limitación no excusa dejar sin completar código, publicación y pruebas posibles.

## 4. Verificación suficiente

Añade regresiones pequeñas para defectos ya observados, usando fixtures y repositorios temporales, sin corpus copiado a tests:

1. T0 y resumen fechado se comparan correctamente; repetición idéntica no genera cambios falsos.
2. Rama diaria antigua con commits propios incorpora el `main` nuevo antes de derivar; una repetición sin cambios conserva commits y publicación pendiente.
3. Fallo real de cada paso obligatorio o publicación produce cierre fallido, nunca éxito aparente. Reutiliza un caso parametrizado.
4. El tramo diario puede ejecutarse aunque adquisición no tenga despacho, sin invocar modelo ni modificar su ledger.

En CAJA acredita las cuatro derivaciones del encargo original y la repetición. El denominador proviene del corpus real; los fixtures no acreditan la medición productiva. Compara el gate con el baseline vigente. No recongeles baseline, desactives checks ni persigas WARN heredados. Resuelve sólo bloqueos de integración directamente ligados a este cambio y ejecuta el CI requerido para el PR.

Actualiza el runbook y §11 con el mecanismo realmente instalado, el comando, SHA y comprobación. Usa una nota breve de cierre; no añadas ADR, índices o auditoría general salvo exigencia material del encargo vigente. Conserva el registro de la corrida anterior: documenta la corrección como sucesión.

## 5. Entrega y parada

Archiva este encargo según el mecanismo existente. Abre un único PR correctivo, separado de F6 y de limpieza administrativa. Autoriza commits, push y apertura/actualización de ese PR; no fusiones ni cierres PR ajenos, ni borres ramas remotas.

Entrega:

- Enlace al PR, SHA y CI; qué defectos quedaron corregidos.
- Tabla corta de las cuatro derivaciones y de la repetición: resultado, cambios y publicación.
- Cifras actuales de declarados/adquiridos/inspeccionados, con denominador y reservas reales.
- Estado exacto del despliegue: tarea/comando, SHA cargado, activación probada y resultado. Indica el único paso posterior al merge si todavía existe.

Termina al tener el correctivo revisable y suficientemente probado, con despliegue comprobado o un impedimento externo concreto. No amplíes a nuevas adquisiciones, F6, trámite/despacho o auditoría general. El avance útil es disponer de derivados actuales que no inventen cambios ni oculten errores, sin recalcularlos a mano cada día.

## Prompt de lanzamiento

> Ejecuta íntegramente ENCARGO-GEN2-DERIVADOS-CORRECTIVO-Y-DESPLIEGUE.md en CAJA, con corpus y acceso Windows/WSL. Actualiza origin/main: #814 y #815 ya estaban fusionados al redactarlo; corrige sólo lo que siga pendiente. Autorizo el correctivo de derivados, las regresiones dirigidas, completar el cableado al scheduler/launcher existente, la comprobación determinista y el despliegue reversible de su SHA remoto mediante el mecanismo autorizado. Autorizo commits, push y apertura/actualización de un único PR correctivo. Los merges quedan conmigo. No invoques modelos ni hagas nuevas adquisiciones durante las comprobaciones. Preserva T0, inspecciones, corpus, commits pendientes, trabajo ajeno y el estado de adquisición. No borres ramas ni integres huellas administrativas. Completa el trabajo posible ahora; distingue claramente pruebas locales, ejecución efectiva, despliegue y fusión pendiente.
