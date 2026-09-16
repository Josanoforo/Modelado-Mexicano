# GEN2-DESPLIEGUE-CAJA-Y-CIERRE-OPERATIVO · cierre

**Fecha:** 15/sep/2026 · **Caja:** FF-5563 (WSL Ubuntu) · **Clon operativo:** `/home/pc0/mm-adq`
**Worktree del acto:** `/home/pc0/mm-gen2-despliegue-caja` · **Rama:** `acto/gen2-despliegue-caja-cierre-operativo` · **PR:** #804

## 0 · Qué se pidió y qué se encontró

El encargo pedía acreditar que la tarea existente ejecuta la versión integrada del
correctivo #801 y que su recorrido **regenera y publica** la demanda. La premisa de
partida era que podía faltar el despliegue.

**El despliegue no faltaba.** Lo que fallaba era el recorrido, por dos defectos
distintos, ambos reproducidos en producción y ambos ajenos a la premisa del encargo.

## 1 · Tarea y recorrido reales

Hay **dos** disparadores registrados en Windows Task Scheduler:

| Tarea | Acción | Estado |
|---|---|---|
| `\ModeladoMexicano\AdquiereCron` | `powershell -EncodedCommand` → `wsl.exe` → `env ADQ_DISPARADOR=windows-task-scheduler ADQ_COMPROBACION_LIGERA=1 ADQ_DEPLOY_REVISION=… bash -lc /home/pc0/mm-adq/tools/adquiere_launcher.sh` | **la vigente**; 07:30 diaria + repetición horaria + inicio de sesión |
| `\MM-adquiere` | `wsl.exe -d Ubuntu -u pc0 -- bash -lc "cd /home/pc0/mm-adq && ./tools/adquiere_cron.sh >> forense/adq-log/cron-stdout.log 2>&1"` | **legado, habilitado**; invoca el runner **sin pasar por el launcher** |

El launcher hizo su trabajo en cada ciclo: `git fetch origin main`, resolución de la
revisión y `checkout --detach` bajo el mismo lock que hereda el runner.
`10f86175` (#801) **es ancestro** de `622fae2a`, de modo que el SHA que llegó al
runner sí contenía el correctivo.

## 2 · H6 · una rama `censo/<fecha>` tomada por otro worktree mataba al runner

**Ocho** corridas horarias consecutivas (15:00 → 22:00) murieron con `exit=128`:

```
fatal: 'censo/2026-09-15' is already used by worktree at '/home/pc0/mm-adq-censo-correction'
```

`censo/<fecha>` es un nombre **compartido**. El worktree `mm-adq-censo-correction`
—de otro acto, abandonado desde las 12:28— lo tenía tomado. `git checkout` aborta con
128 y, bajo el `set -euo pipefail` del runner, se lleva el proceso entero.

Al fusionarse #801 (18:58:15) la muerte se **adelantó** de `CENSO-RAIZ` (línea 1079) a
`SELECCION-INVESTIGACION` (línea 995) — la primera sentencia de
`publica_proyeccion_demanda()`, cuya documentación promete que «su fallo NUNCA bloquea
la selección ni la investigación». La promesa era falsa. El adelanto costó además el
montaje del corpus, PDN, la sonda de red y la huella `[ADQ]`.

**Corrección:** poseer el *nombre local* de la rama no es requisito para publicar en
ella. Si está tomada, la corrida trabaja con HEAD desprendido sobre la punta del
**origen** y empuja por refspec explícito `HEAD:refs/heads/<rama>`, declarándolo como
`CENSO-RAMA-TOMADA`. **El árbol ajeno no se toca nunca.**

## 3 · H7 · la proyección se regeneraba con el árbol de `censo/<fecha>`

Levantado H6, la primera corrida en que `publica_proyeccion_demanda()` llegó a
ejecutarse de verdad (`run_id 2026-09-15T222751-201668`) **tampoco publicó**. La
función hacía `checkout_o_crea_censo` **antes** de regenerar, y cambiar de árbol no
sustituye sólo la vista: sustituye las **herramientas** y los **insumos**. Con el árbol
en la punta del censo (`5e2e87e8`, de las 12:28):

- `tools/adq_investigacion.py` era **anterior a #801** y no conocía el flag que la
  propia función acababa de introducir —
  `error: unrecognized arguments: --compara-proyeccion`— y el fallo se **tragaba** en la
  rama «sin cambio pertinente» (la sustitución de comando devuelve vacío, y vacío
  `!= "si"`). La corrida declaraba normalidad y no publicaba nada;
- `forense/no-corrido.tsv` y `data/adq-investigacion.yaml` eran también los de esa punta
  vieja, así que la vista se regeneraba desde insumos de **otro corte**.

Es decir: la fotografía desfasada que #801 venía a eliminar seguía viva, y **la función
nunca había publicado ni una sola vez en producción**.

**Corrección:** el «antes» se lee con `git show`, sin cambiar de árbol; la regeneración
y la comparación corren sobre el árbol **desplegado**; sólo se cambia de árbol para
commitear; y un `--compara-proyeccion` que falla ya **no** se lee como «sin cambio»
—sube `PUBLICACION_FALLIDA` y declara `PARO-COMPARA-PROYECCION`.

## 4 · Acreditación en CAJA

Dos activaciones **manuales de verificación** por el mecanismo existente
(`tools/adquiere_launcher.sh`, `modo=revision-fijada`), declaradas como tales:

| run_id | SHA | Resultado |
|---|---|---|
| `2026-09-15T222751-201668` | `48a875a0` (H6) | Sobrevivió la colisión, `fase=FIN`, `publicacion=OK`; publicó `[CENSO]`, `[ADQ-PDN]` y la huella `[ADQ]` por refspec. Investigación NC-0202: `exit=65`, `resultado_invalido`. **Esta corrida midió H7.** |
| `2026-09-15T223728-210778` | `09fd359b` (H6+H7) | **`[ADQ-DEMANDA] 2026-09-15`: proyección regenerada y publicada** en `censo/2026-09-15` (`bfe1a6dd..86b2c1bc`). |

**Huellas de la vista publicada: 10/10 `fuentes_sha256` corresponden al SHA desplegado**
(`09fd359b`); 5 de ellas **difieren** del árbol viejo del censo — prueba de que la
regeneración usó los insumos de este corte y no los heredados. El efecto es material:
la corrida con árbol viejo dio `total_activas=59, contrato_incompleto=39`; con el árbol
desplegado, `65` y `47`.

**Consumo:** techo diario `3/5/3900s`; usado `3/1/948s`; disponible al cierre
`0/4/2952s`. **Objetos nuevos 0, bytes nuevos 0** — cero descargas.

**Continuidad automática:** el ciclo de las 23:00 disparó solo
(`disparador=windows-task-scheduler`) y cerró `exit=0` en `COMPROBACION-LIGERA` con
`sin despacho`. Es una **espera legítima**, no un fallo: el cupo diario de necesidades
estaba consumido (3/3) y la cola de adquisición tenía 0 elegibles. Esa corrida no tocó
la rama del censo y por eso no chocó.

## 5 · Despliegue del correctivo

`tools/windows/instala-tarea-adquisicion.ps1 -DeploymentRevision 09fd359b…` (el
procedimiento del repositorio; calendario derivado de `data/adq-config.yaml`, sin tocar
frecuencia, límites, modelo ni privilegios). Respaldo verificado de la definición anterior —codifica
`ADQ_DEPLOY_REVISION=70a2a8f59b76221a52155416499ea7aed1c16a79`— en el clon operativo,
**sin versionar** (el repo es público y el XML lleva el SID de la máquina):

```
/home/pc0/mm-adq/forense/cron/RESPALDO-TAREA-20260915T2245.xml
```

Reversión exacta, desde Windows:

```
schtasks.exe /Create /TN "\ModeladoMexicano\AdquiereCron" ^
  /XML "\\wsl$\Ubuntu\home\pc0\mm-adq\forense\cron\RESPALDO-TAREA-20260915T2245.xml" /F
```

**Es estado desplegado, NO integrado.** Al fusionarse #804 el launcher verá la revisión
contenida en `main` y volverá solo a seguir `main` (`modo=main-contiene-revision`); no
hace falta revertir nada.

**Próximo disparo a revisar: 2026-09-16 00:00** (hora local). Es también el cambio de
fecha: cupo diario nuevo y `censo/2026-09-16` libre, así que esa corrida sí debería
recorrer el runner completo con el correctivo.

## 6 · Reservas

- **`\MM-adquiere` sigue habilitada** y llama al runner **sin launcher** (sin fetch, sin
  despliegue, sin fijación de revisión). Próximo disparo 16/sep 07:30 —la misma hora que
  la tarea vigente—, de modo que compiten por el lock; si ganara la legada, el runner
  correría con el árbol que hubiera quedado en `mm-adq`, sin desplegar. No se tocó: es
  un disparador preexistente y conocido, fuera del perímetro de este encargo. Para
  desactivarla: `schtasks.exe /Change /TN "\MM-adquiere" /DISABLE`.
- **El worktree `mm-adq-censo-correction` sigue tomando `censo/2026-09-15`.** No se tocó
  (el intento de desprender su HEAD fue denegado por el clasificador, y tampoco era
  necesario: H6 hace innecesario liberarlo). Su commit `5e2e87e8` ya está fusionado en
  `origin/main` vía PR #783, así que no guarda trabajo único.
- La investigación NC-0202 de la primera activación cerró `resultado_invalido`; es
  materia del contenido de la investigación, no del despliegue ni de la publicación.
- El encargo llegó por prompt y no existe como archivo en `forense/encargos/`; no hay
  nada que archivar ahí.

## 7 · Dictamen

| Eje | Veredicto | Razón |
|---|---|---|
| **Despliegue** | **Acreditado** | El launcher resolvió y entregó el SHA en cada ciclo; `#801` contenido en `622fae2a`; el correctivo se desplegó por el instalador del repo y la tarea lo codifica. |
| **Recorrido de demanda** | **Acreditado** | `[ADQ-DEMANDA] 2026-09-15` publicado en `censo/2026-09-15`; 10/10 huellas corresponden a los insumos del corte desplegado. |
| **Continuidad automática** | **Acreditada como disparo; pendiente de observar un ciclo que recorra el runner** | Las 23:00 dispararon solas y cerraron bien, pero con `sin despacho` legítimo. Próximo disparo a revisar: 16/sep 00:00. |
| **Adquisición** | **Acreditada como cero** | 0 objetos, 0 bytes. Cero descargas es compatible con el encargo: no había cola elegible. |

## 8 · ¿Quedó el proyecto más cerca de una explicación, medición, decisión o modelo mejor?

Sí. El servicio operativo volvió a **atender y publicar necesidades vigentes**: llevaba
ocho ciclos consecutivos sin publicar nada y con la fotografía de demanda desfasada, que
es la vista que mesa consulta para decidir qué medir. Ahora se regenera desde los
insumos del corte y se publica, sin perder estado ni duplicar trabajo, y sin tocar
trabajo ajeno. No se descargó ningún archivo y no se promete habilitación científica por
ello: lo que se recuperó es la capacidad de decidir con una demanda al día.
