# 33 · Corpus adquirido, disponible para todas las sesiones

ENTORNO: CAJA

## Contrato de ejecución autónomo

Repositorio: `Josanoforo/Modelado-Mexicano`. Entorno: Codex CLI en CAJA Windows/WSL. Este MD contiene el encargo completo.

Al despacharlo, Jonás autoriza las fases y el alcance expreso de este documento, los commits, push y PR. La fusión queda con Jonás. No se firman por extensión adopciones, materialidad científica, FP-371/372/373/374, F6 ni acceso comercial. No enviar correos/formularios, aceptar compromisos de terceros o comprar; sí descargar material público y usar accesos previamente autorizados.

Lee `AGENTS.md`; reporta worktree absoluto, rama, SHA y estado. Usa worktree/rama propios. Contrasta main y PR abiertos pertinentes antes de editar: los encargos 27–32 están en ejecución o integración y no deben duplicarse. Corte de esta propuesta: main `e37367581d5186ce4d4cf497377c83ebcd61cf93`, #721–724 fusionados, #725–728 abiertos. El estado cambia: toma el efectivo al comenzar.

Resuelve montaje y dependencias antes de la ejecución. El corpus compartido sirve como entrada; temporales y resultados intermedios van al directorio de cada tarea. No sobrescribas archivos que otra sesión está leyendo. Publica incorporaciones por identidad y de forma atómica con los mecanismos existentes, preservando hashes, padres, sellos y evidencia ajena. No uses salidas GEN1 como insumo numérico GEN2 ni reetiquetes datos conocidos como retenidos.

Reutiliza herramientas y decisiones existentes. Evita otra cola, otro scheduler y wrappers sin necesidad. Valida los riesgos concretos y ejecuta sobre trabajo real: no entregues sólo fixtures, un inventario o un plan. Continúa las fases sin pedir otro encargo. Si una parte depende de un acceso externo, termina las independientes y deja el objeto y acción precisos; no inventes datos ni cierre completo.

Cierra encargo → resultado → evidencia → registros/vistas pertinentes → nota → ADR/L0/rótulo cuando aplique → PR. Actualiza filas comunes por clave canónica; quien integra después concilia y deriva desde el árbol conjunto, sin restaurar tablas completas de su rama. Pruebas dirigidas y gates aplicables, sin limpiar CI heredada ni rehacer la auditoría general.

## Resultado encargado

Que los datos ya adquiridos resuelvan correctamente desde worktrees nuevos y desde el clon de adquisición. Reparar ubicación/montaje y recuperación de bytes identificados; no volver a investigar las fuentes por cada sesión.

**Antecedente concreto:** NC-0059 sigue abierta: falta comprobar que los 29 payloads de #635 estén en el corpus compartido y no únicamente en `/home/pc0/mm-gen2-sonda-caja-1`. Eso es una obligación pendiente, no prueba de que hoy falten físicamente. Los encargos 27, 30, 34 y 35 necesitan fuentes locales identificadas; esta tarea debe ayudarles sin asumir el control de sus worktrees.

## Fase 1 · Perímetro por identidad, no barrido de toda la máquina

Lee `forense/notas/2026-09-08-GEN2-SONDA-CAJA-1.md`, NC-0059, `data/manifiesto.yaml`, `tests/manifiesto.py`, `tests/corpus.py` y la configuración de raíces. Deriva los IDs exactos del lote de 29 y los inputs de los cálculos activos de ENSAFI, ENNViH/tandas y parámetros vigentes. Deduplica por hash; no fijes que el total actual sea 29.

Reutiliza `tests/manifiesto.py --verifica --id <ID>` (admite IDs repetidos). Distingue raíz no configurada, archivo ausente, hash distinto y archivo correcto bajo otra raíz. No recorrer Downloads personales ni raíces excluidas por la política física vigente.

## Fase 2 · Reparar disponibilidad real

Para cada ausencia de este perímetro:

1. Resolver primero la configuración local de raíces.
2. Si los bytes correctos están en un worktree del proyecto, copiarlos al destino compartido permitido, conservando el origen. Verificar tamaño/hash antes de publicar la copia; una coincidencia de nombre no basta.
3. Si faltan físicamente, recuperar el objeto público exacto por su receta/manifiesto. Descarga temporal, valida y publica sin sobreescribir contenido diferente. Si el proveedor cambió el archivo, registrar un objeto/versionado distinto; no sustituir bajo el hash antiguo.
4. Si necesita un acceso nuevo, registrar el residual en coordinación con #726; no duplicar la búsqueda científica del encargo 36.

Respetar simultaneidad: copia atómica en la misma raíz y no cambiar enlaces de datos bajo un proceso activo. No editar configuraciones de otras sesiones mientras ejecutan. Entregar y aplicar una receta local común para nuevos worktrees; usar la configuración de raíces existente, no crear un segundo resolvedor.

## Fase 3 · Automatización mínima útil

Si ya existe una operación para preparar/verificar un conjunto de IDs, úsala. Si falta, añade un modo acotado a la herramienta adecuada: previsualización por defecto y ejecución explícita, lista de IDs, origen/destino y resultado. No escanear y copiar todo el corpus por defecto. La repetición sobre contenido idéntico no descarga ni duplica. El inventario, hashing y resolución siguen siendo los canónicos.

Esta operación es para materialización local/recuperación de objetos conocidos; no selecciona qué ciencia hacer y no modifica el cron de #726.

## Fase 4 · Demostrar uso

Desde un worktree nuevo, comprobar que un lector real de cada familia afectada abre su input identificado usando las raíces comunes. Para el lote NC-0059 comprobar todos sus IDs; no cerrar 29/29 desde tres muestras. Confirmar también que el clon operativo puede resolver las mismas raíces bajo su identidad, sin reiniciar una adquisición activa.

Entregar tabla ID → ubicación lógica → hash/estado → consumidor habilitado. Cerrar NC-0059 sólo si todo su alcance está acreditado. No añadir microdatos ni rutas privadas de usuario a Git.

## Concurrencia y término

Puede iniciar ahora, junto a #726, porque no toca scheduler, selector ni `tools/adq_*`. Congela el conjunto de IDs inicial y no persigas altas concurrentes. #728 ya prepara los inputs DIN/TRA de F5: no absorberlos ni alterar sus paquetes en esta tarea. Los encargos 34/35 pueden usar sus archivos existentes sin esperar todo este lote; si necesitan uno reparado, toman el archivo después de su publicación verificada. Termina con inputs utilizables, no sólo con una lista de ausencias.
