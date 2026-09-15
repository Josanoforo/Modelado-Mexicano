ENCARGO · GEN2-DEMANDA-VIGENTE-ANTES-DESPACHO

SHA de redacción: `b6245ba1d65f86b049e5c21dca904b87da50a831` (`origin/main`, fetch del 15/sep/2026). Redactado fuera del repo por mesa/Jonas y archivado en esta sesión contra las instrucciones vigentes `instrucciones-proyecto-v2_13.md`. Estado: VIVO.

ENTORNO ASIGNADO: CAJA (Windows/WSL) — el propio encargo lo declara: "Ejecutor: Codex CLI en CAJA, Windows/WSL. No requiere Opus." NO se lanza en NUBE: toca `tools/adquiere_cron.sh`/el cron de producción y una proyección de demanda que sólo tiene sentido corregida donde vive el corpus/checkout sincronizado.

MODELO SUGERIDO: Codex CLI, conforme el propio encargo (no requiere Opus ni Sonnet para ejecutarlo).

COMPUERTA: ninguna declarada explícitamente por el encargo (no trae línea `GATED a …` / `COMPUERTA: …`); no dispara verificación mecánica de compuerta al lanzarse.

CARRILES: corrección de la proyección de demanda (`data/adq-demanda-activa-v1_0.json`) y de su conexión con `tools/adquiere_cron.sh`/`tools/adq_investigacion.py`/`tools/adquiere_launcher.sh`. El propio encargo excluye explícitamente parámetros, resultados sellados, adopciones, decisiones sobre intervalos de confianza, F6 y cambios de acceso — ver "Perímetro y cierre" en el texto verbatim abajo.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — contestada por quien archiva, 15/sep/2026 ═══

1 · ESTRUCTURA. `data/INFRAESTRUCTURA-v1_0.md` no trae fila para `data/adq-demanda-activa-v1_0.json` ni para `tools/adq_investigacion.py`:

    $ grep -n "adq-demanda\|adq_investigacion" data/INFRAESTRUCTURA-v1_0.md
    (0 líneas)

   Hueco del índice, no de este acto de archivado: ninguno de los dos es un artefacto nuevo — ambos preceden este encargo y están citados en múltiples notas de mesa y encargos previos (p. ej. `2026-09-10-GEN2-SONDA-CRON-PRODUCCION-POST693.md`). Este archivado no llena el hueco porque su alcance es archivar el texto, no ejecutar la corrección; quien lo ejecute en CAJA queda advertido y puede registrar la fila si su trabajo toca la estructura.

2 · CONTENIDO. Lo que este encargo manda no es crear un artefacto nuevo — es corregir uno existente y conectar su regeneración al recorrido operativo. Verificado contra `origin/main` (`b6245ba`) que todo lo que el encargo cita EXISTE-SATISFACE:

    $ git cat-file -e origin/main:AGENTS.md && echo OK
    $ git cat-file -e origin/main:tools/adq_investigacion.py && echo OK
    $ git cat-file -e origin/main:tools/adquiere_cron.sh && echo OK
    $ git cat-file -e origin/main:data/adq-demanda-activa-v1_0.json && echo OK
    $ git cat-file -e origin/main:tests/check.py && echo OK
    → las cinco imprimen OK

   El launcher que el encargo menciona sin nombrar existe como `tools/adquiere_launcher.sh` (`git ls-tree -r --name-only origin/main -- tools | grep -i launcher`).

   La opción `--escribe-proyeccion` que el encargo pide reutilizar existe en la CLI vigente, corrida contra el blob de `origin/main` (no contra un checkout potencialmente desactualizado):

    $ git show origin/main:tools/adq_investigacion.py > /tmp/adq_investigacion.py
    $ python3 /tmp/adq_investigacion.py --help
    usage: adq_investigacion.py [-h] [--config CONFIG] [--selecciona] ...
                                [--escribe-proyeccion ESCRIBE_PROYECCION] ...
    Proyecta demanda científica activa y selecciona investigación recurrente.

3 · COBERTURA RETROACTIVA. No aplica en sentido estricto: este acto de archivado no propone ninguna tabla gobernante nueva, así que no hay fecha de nacimiento de tabla que comparar contra fecha de trabajo. Los dos artefactos que el encargo corrige (`data/adq-demanda-activa-v1_0.json`, `tools/adq_investigacion.py`) son anteriores al defecto que el encargo describe (diagnóstico de mesa sobre `main 0cdbd72c`, citado como antecedente dentro del propio encargo, no como cifra a imponer).

PERÍMETRO Y CONCURRENCIA (de esta etapa de archivado — no del acto técnico que Codex CLI ejecutará después)

Esta sesión sólo escribió `forense/encargos/2026-09-15-GEN2-DEMANDA-VIGENTE-ANTES-DESPACHO.md`, y en el worktree nuevo (`/home/pc0/mm-gen2-demanda-vigente-despacho`, rama `acto/gen2-demanda-vigente-antes-despacho`, creada desde `origin/main` en `b6245ba`) enlazó `data/raw` y copió `data/raices.local.yaml` del clon padre sin tocar su contenido. Búsqueda de rótulo duplicado antes de crear la rama: `git ls-remote --heads origin` (7 refs vivas, ninguna con "demanda"), `git worktree list` (sin coincidencia con "demanda-vigente"/"demanda-antes-despacho"), `gh pr list --state open` (3 PR abiertos — #793, #794, #795 — ninguno sobre demanda/proyección/cron). No se hizo push de la rama. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR CANDIDATOS

No aplica a esta etapa: archivar el encargo no produce hallazgo ni gobernanza propia. El acto técnico que lo ejecute deriva su propio candidato de ADR contra `canon/gobernanza-v1_15.md` al cerrar, y su propio rango de FP contra `forense/firmas-pendientes.tsv` vigente en ese momento.

CONTADOR

Cero directo, declarado: esta sesión sólo archiva el texto del encargo; no mueve ningún contador de investigación, presupuesto ni corrida.

Lo que este acto de archivado NO hace

No ejecuta la corrección técnica descrita — eso queda para Codex CLI en CAJA, conforme el propio encargo. No hace push de la rama ni abre PR. No toca `data/adq-demanda-activa-v1_0.json`, `tools/adq_investigacion.py`, `tools/adquiere_cron.sh`, `tools/adquiere_launcher.sh` ni ningún otro archivo de producción. No reabre presupuesto, IC, F6 ni accesos. No repite ninguna investigación.

Sucesores declarados, no lanzados

El acto técnico GEN2-DEMANDA-VIGENTE-ANTES-DESPACHO en sí, a lanzar en CAJA sobre esta misma rama (`acto/gen2-demanda-vigente-antes-despacho`) o una que el ejecutor derive citando este encargo archivado como antecedente.

════════════════════════════════════════════════════════════════════

## TEXTO DEL ENCARGO, VERBATIM (tal como se pegó a esta sesión el 15/sep/2026)

GEN2 · Demanda vigente antes del despacho

Fecha: 15 de septiembre de 2026.
Repositorio: Josanoforo/Modelado-Mexicano.
Ejecutor: Codex CLI en CAJA, Windows/WSL. No requiere Opus.
Resultado: corregir la proyección desactualizada y conectar su actualización al recorrido operativo existente, sin repetir investigaciones ni cambiar decisiones científicas.

Contexto y autoridad

El último diagnóstico compartido por mesa, sobre main 0cdbd72c, encontró que data/adq-demanda-activa-v1_0.json conservaba SHA anteriores de necesidades, usos y decisiones: mostraba 66 NC abiertas frente a 65 en el registro, conservaba cinco cerradas y omitía NC-0221–0224. Es un antecedente para reproducir, no una cifra que deba imponerse al estado nuevo. No se afirma una nueva consulta de GitHub al preparar este encargo.

origin/main vigente es la autoridad. Leer AGENTS.md y el encargo completos; revisar brevemente PR abiertos para aprovechar cualquier correctivo equivalente. Trabajar en worktree propio, preservar cambios ajenos e informar ruta, rama y SHA base. Los ZIP de agosto no son insumo necesario ni autoridad para este correctivo.

El cron ya tiene evidencia de ejecución e investigación. El desfase publicado no demuestra que Windows esté detenido ni que el selector use datos antiguos. Determinar esa diferencia antes de modificar código.

Decisiones incluidas

Regenerar mediante el escritor canónico; no editar a mano los SHA, conteos o listas del JSON.

Toda selección debe usar fuentes vigentes del checkout sincronizado empleado en esa activación. La evidencia debe identificar ese corte; no prometer coincidencia perpetua con un main que sigue recibiendo cambios.

Mantener separados: necesidad abierta, ruta de atención, elegibilidad por fecha y selección efectiva con presupuesto. NC-0221–0224 deben quedar representadas si siguen abiertas, pero no convertirse automáticamente en búsquedas web: las reservas científicas y decisiones de mesa conservan su canal.

Conservar cursores, próximas revisiones, reservas, presupuesto y protección contra trabajo ya realizado pendiente de merge. Regenerar una vista no autoriza otra investigación.

No aumentar frecuencias, límites ni crear otro scheduler. No exigir llamadas horarias al modelo ni una descarga para declarar corregido este defecto.

Trabajo

1. Reproducir y actualizar

Con el corte vigente, contrastar los insumos declarados por la proyección contra los archivos reales. Identificar brevemente NC agregadas/cerradas y cambios relevantes de usos o decisiones; no reconstruir el historial general.

Reutilizar tools/adq_investigacion.py y su opción existente, verificando primero la CLI vigente:

python3 tools/adq_investigacion.py --help
python3 tools/adq_investigacion.py --escribe-proyeccion data/adq-demanda-activa-v1_0.json

Aplicar el corte y zona horaria del servicio mediante sus opciones vigentes cuando corresponda. Comprobar los SHA contra exactamente los insumos empleados y derivar los conteos del registro actual. No fijar 65 como valor esperado permanente.

2. Evitar que reaparezca en el siguiente despacho

Inspeccionar el recorrido real de tools/adquiere_cron.sh, su launcher y tools/adq_investigacion.py: sincronización, comprobación de despacho, selección y publicación de evidencia.

Resolver el delta mínimo:

Si el selector ya calcula desde fuentes vigentes, conservarlo. Conectar la regeneración/publicación que falta; no introducir un bloqueo artificial por el JSON publicado antiguo.

Si algún consumidor selecciona desde la vista persistida, verificar sus insumos y regenerarla antes de consumirla cuando estén desactualizados. Nunca continuar silenciosamente con esa vista si la regeneración falla. El fallo afecta al recorrido dependiente; no paralizar trabajo independiente que usa fuentes válidas.

Reutilizar el escritor atómico y la publicación existentes. Asegurar que selección y evidencia refieran al mismo corte de insumos; no añadir otra base de datos ni registro paralelo.

Ejecutar esta actualización mecánica también cuando la comprobación termine sin invocar al modelo. No gastar cupo de investigación para actualizar metadatos.

Publicar el cambio derivado por el canal existente cuando haya cambios pertinentes. Evitar commits/PR repetidos solo por una marca de tiempo. Si ya existe un PR de evidencia de esta operación, actualizarlo según el protocolo del repo.

Un merge posterior puede volver antigua una fotografía publicada. La garantía requerida es actualizarla al siguiente recorrido operativo y seleccionar desde fuentes vigentes; no crear una automatización por cada merge para mantenerla permanentemente idéntica a main.

3. Verificación suficiente

Usar las pruebas dirigidas existentes y añadir solo la regresión del defecto observado:

Una fixture modifica un insumo relevante después de generar la vista —por ejemplo, cerrar una NC y añadir otra—. El recorrido operativo refresca la proyección y la selección refleja el estado nuevo, con SHA correctos.

Repetir sin cambios relevantes no modifica estados de investigación, reservas ni presupuesto, ni genera otra publicación equivalente.

Comprobar que la representación de NC-0221–0224 respeta su estado y canal vigentes. NC-0202 y NC-0161/0162 conservan sus rutas y condiciones actuales; ahorro conserva su cursor y fecha, sin adelanto autorizado por este encargo.

Si el recorrido consume una vista persistida, comprobar también que un fallo de regeneración no termine en despacho basado en ella. Ampliar pruebas únicamente para un riesgo concreto. Comparar fallos heredados con baseline.

4. Comprobación en CAJA

Publicar el correctivo en un PR pequeño. Si cambia código ejecutado por la tarea, desplegar el SHA remoto exacto en la tarea existente conforme al lanzamiento; conservar sus parámetros y ledger. Si solo faltaba regenerar/publicar evidencia y el runtime ya era correcto, no redeplegar por ceremonia.

Ejecutar una comprobación por el recorrido operativo existente. Preferir su modo mecánico sin consumo, si existe y recorre la pieza corregida; no inventar una opción CLI. Si hace falta activar la tarea completa, respetar elegibilidad y presupuesto reales: puede investigar únicamente trabajo que ya corresponde atender. No adelantar continuaciones ni fabricar necesidades.

Conservar evidencia breve del SHA ejecutado, corte/huellas de insumos, resultado de actualización y decisión de despacho. Usar recibos/logs existentes. Una activación manual acredita ese recorrido; no presentarla como disparo automático. No esperar horas para cerrar el PR: indicar la próxima ejecución programada si falta observarla.

Perímetro y cierre

Incluye proyección, conexión operativa mínima, pruebas dirigidas y nota breve de cierre; archivar este encargo según el protocolo vigente. Excluye parámetros, resultados sellados, adopciones, decisiones sobre intervalos de confianza, F6 y cambios de acceso. No reabrir presupuesto ni correcciones ya acreditadas.

Entregar:

PR y SHA; actualización de demanda antes/después con diferencias relevantes.

Si el selector estaba afectado o el defecto era solo de evidencia publicada, sustentado en el recorrido observado.

Pruebas y comprobación CAJA, con SHA desplegado cuando aplique.

Próximo despacho o motivo legítimo de espera. Separar actualización de demanda, investigaciones, descargas y habilitación científica; este correctivo puede completar su objetivo con cero descargas.

Termina cuando la vista está regenerada, el recorrido evita usar una proyección desactualizada y la comprobación acredita el comportamiento. Si falta acceso a CAJA, entregar el cambio y el comando pendiente exacto, sin afirmar despliegue. Las fusiones quedan con mesa.

¿El proyecto quedó más cerca de producir una explicación, medición, decisión o modelo mejor? Sí, si el siguiente despacho representa las necesidades vigentes sin perder pendientes ni repetir trabajo; respaldar la respuesta con esa evidencia.

Prompt de lanzamiento

Ejecuta íntegramente ENCARGO-GEN2-DEMANDA-VIGENTE-ANTES-DESPACHO.md en CAJA. Usa origin/main vigente y aprovecha correctivos ya integrados. Autorizo cambios delimitados, regeneración canónica, pruebas, commits, push, apertura o actualización del PR, despliegue del SHA publicado si cambia el runtime y la comprobación mediante la tarea existente, dentro de sus fechas y presupuesto. Los merges quedan conmigo. Corrige la recurrencia del desfase con el mecanismo existente; conserva cursores, reservas y decisiones científicas. No descargues por demostrar actividad ni repitas investigaciones. No autoriza contactos a terceros, compras ni nuevos privilegios. Entrega evidencia concreta del corte utilizado y del despacho, distinguiendo comprobación manual de ejecución automática.
