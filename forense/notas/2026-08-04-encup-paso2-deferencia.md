# ENCUP paso 2 — medición de `deferencia`: la compuerta NO pasa

**Contadores movidos: 0.** Este acto no mide: verifica si la nota de paso 1
deja lo necesario para congelar una especificación de medición sin abrir el
instrumento (ADR-46, sesión limpia). No lo deja — por dos razones
independientes, cualquiera basta sola. PARO antes de Commit 1. El entregable
de este acto es este reporte.

PARALELO P-A, mesa (letra/número no provisto en el encargo), emitido
4/ago/2026 contra `origin/main = 4b27869`. Rama `sesion/encup-paso2-deferencia`,
worktree `mm-encup-paso2-deferencia`.

## 0 · Entorno

```
$ git -C Modelado-Mexicano fetch origin
   6a7954b..4b27869  main  -> origin/main
$ python3 tests/bitacora.py --abre
HEAD:         4b278699fe44c38142146429fc85ee875e0933ae
origin/main:  4b278699fe44c38142146429fc85ee875e0933ae
Divergencia:  ninguna — HEAD == origin/main
check.py --baseline:        exit=0 · VERDE
validador_registro_ids.py:  exit=0 · OK, 49 IDs verificados
Instrucciones vigentes: v2.3 (4fb7964, 2026-08-04)
```

`origin/main` sí es `4b27869` exacto — no hubo que re-derivar. No existía
worktree previo para este acto (a diferencia de paso 1, ninguna rama
`*paso2*encup*` ni `*deferencia*` sin usar); se creó con
`git worktree add mm-encup-paso2-deferencia -b sesion/encup-paso2-deferencia
origin/main`, mismo patrón que los ~28 worktrees hermanos.

### 0.1 · Anomalía de concurrencia durante la creación del worktree

`git worktree add` reportó dos veces `error: could not write config file
.git/config: Device or resource busy` (el resto de la operación completó:
rama creada, HEAD correcto, tracking de rama no quedó escrito — verificado
después, `git config --get branch...remote` vacío, sin impacto porque este
acto no depende de tracking automático). Consistente con el registro ya
abierto `I-11` (`forense/bitacora.md`, hallazgos congelados: "Un checkout
compartido entre sesiones de escritura se bloquea sin que ninguna sesión
haga nada mal — `.git/HEAD` es del directorio, no de la sesión") — misma
familia de fenómeno (escritura concurrente sobre metadatos `.git`
compartidos entre worktrees), consistente con que Acto 1 corría en paralelo
sobre el mismo repositorio en ese instante. Se verificó `git config --list
--local` después: el archivo parsea limpio, sin corrupción. No es uno de
los disparadores de PARO del encargo. No se abre un `I-` nuevo por esto —
ya está cubierto por `I-11`.

### 0.2 · `data/raw`

Igual que paso 1 §0.2: el worktree nació sin `data/raw`. Se enlazó
`data/raw -> /home/pc0/mm-corpus/raw` (wiring estándar, gitignorado —
`.gitignore:5` declara `data/raw/`, aunque por ser symlink y no directorio
el patrón con `/` final no lo cubre vía `git check-ignore`; sí aparece como
`??` en `git status`. Anotado para no hacer `git add -A` nunca en este
acto — solo se añaden archivos por nombre explícito).

## 1 · Premisas del encargo

| # | Premisa | Verificación |
|---|---|---|
| 1 | `main = 4b27869` | **Sostiene.** `fetch` + `log origin/main -1`: exacto, `rev-list --count 4b27869..origin/main` = 0 |
| 2 | **La compuerta** — proxy declarado y completo para congelar sin abrir instrumento | **NO sostiene.** Ver §2 abajo, dos razones independientes |
| 3 | Payload `encup_2012_base_datos_xlsx` en manifiesto y en corpus, por nombre/tamaño | **Sostiene.** `data/manifiesto.yaml:3277-3292`: registrado, `tamano_bytes: 4814178`. En disco (`data/raw`, symlink al corpus): `stat` reporta `4814178 bytes`, mismo nombre. Sin recalcular sha (patrón Encargo W) |
| 4 | Contador vigente = 9 de 14 | **Sostiene.** `canon/modelo-decision-v4_0.md:277,621,725` (HEAD `4b27869`): "Condicionales medidas sobre atributos: ~~8~~ 9 de 14", corregido 4/ago/2026 por Encargo K. Sin corrección posterior (`grep` de "10 de 14"/"11 de 14"/"12 de 14" en `canon/`, `forense/`, `milpa/`: los tres hits son de un contador distinto — "alcanzables", no este) |
| 5 | Ejes de estratificación estrictos para ENCUP | **Ninguno estricto** (paso 1 §7: `grep -i encup` contra el inventario de Tabla B, cero resultados — ENCUP no está en la Tabla B). Cláusula de salvedad de la propia premisa 5 aplica: de haber seguido, la condicional se habría declarado con los ejes que el instrumento permite, rotulados (paso 1 §8: `edad` directo y limpio, `n`=3750 sin faltantes; el resto parcial-no-equivalente o ausente). No es, por sí sola, disparador de PARO — queda documentado porque la premisa 2 sí lo es |

Premisa 1, 3, 4 sostienen. Premisa 5 sostiene con la salvedad prevista. **Premisa 2 no sostiene** → PARO, por instrucción explícita del encargo.

## 2 · Por qué la compuerta no pasa — dos razones independientes

**(A) No hay reactivo que declarar.** El checklist de premisa 2 exige
"reactivo(s) con código de variable" como primer elemento. La nota de paso 1
examinó el cuestionario completo (84 preguntas, 11 páginas, `pdftotext
-layout`) contra una frase-criterio escrita *antes* de abrir el PDF (paso 1
§2) y llegó a un veredicto negativo explícito:

> "**LA FUENTE NO TIENE EL DATO.** [...] ninguna cumple la frase-criterio de
> §2. `deferencia` sigue en `PROXY CON SUPUESTO DECLARADO (M3, Latinobarómetro
> `P4NOIJ`, ADR-51(f))` — **sin cambio**" (paso 1 §11)

Las dos candidatas que sí superaron el barrido de vocabulario (`P44A`,
`P68`) fueron descartadas con argumento, no por falta de dato: `P44A`
("obedecer siempre las leyes") cae del lado de legitimidad-legal, no
jerarquía-interpersonal — precedente directo y casi textual con `ENCUCI
AP5_11`, descartado por la misma razón en Encargo C (paso 1 §3, cita
`forense/notas/2026-07-31-encargo-c-familismo-deferencia-reactivo.md:113-115`).
`P68` cae del lado horizontal (consenso mayoritario), no vertical. Esta es
exactamente la tensión legitimidad-legal vs. jerarquía-interpersonal que la
premisa 2 del encargo anticipa que §11 "asoma" — y al asomarla, la resuelve
en contra de que exista reactivo, no a favor. No hay "reactivo con código de
variable" que declarar en Commit 1 porque paso 1 concluyó, con argumento
verificable, que no existe.

**(B) Ponderador/estrato/UPM no están nombrados en la nota, en ningún
lugar.** `grep -inE "ponderad|estrato|UPM|conglomerad|factor de
expansion|factor_expansion|diseño muestral"` contra la nota completa de
paso 1 → cero coincidencias sobre diseño muestral (la única aparición de
"estrato" es "estrato de ingreso del hogar/persona", sobre la variable de
ingreso ausente — no sobre diseño de muestreo). La premisa 2 ya prevé este
caso exacto: "ENCUP 2012 es xlsx único — si el diseño muestral no está
resuelto en la nota, no es derivable sin abrir instrumento". No está
resuelto. Y por ser xlsx único sin documento de diseño separado, resolverlo
exige abrir el xlsx — la acción que ADR-46 reserva para después de Commit 1.
Esta razón habría bastado sola, incluso en un mundo donde (A) no aplicara.

Cualquiera de las dos cierra la premisa 2. Las dos aplican a la vez.

## 3 · Sesión limpia — declaración ADR-46

Esta sesión **no abrió** `Cuestionario-Quinta_2012_ENCUP.pdf` ni
`BaseDatos_ENCUP_2012_Final.xlsx`. Se leyó únicamente: la nota de paso 1
completa, `milpa/procedencia.yaml` (grep dirigido), `canon/modelo-decision-v4_0.md`
(grep dirigido + líneas citadas arriba), `canon/glosario-v5_6.md` (grep
`deferencia`, sin resultado), y `data/manifiesto.yaml` (una entrada). El
tamaño del payload se verificó por metadato de filesystem (`stat`), no por
apertura de contenido. Esta sesión **queda habilitada** para pre-registrar
contra `ENCUP` en un acto futuro — a diferencia de la sesión de paso 1, que
`§12` de su propia nota inhabilitó.

## 4 · Lista para mesa — lo que este acto no puede decidir

1. **¿Se cierra formalmente la candidatura ENCUP→`deferencia`?** Hoy queda
   en `solo proxy` (3 de 14, sin cambio) de forma indistinguible entre
   "nadie lo ha revisado" y "se revisó y no hay dato". El veredicto de paso 1
   es un cierre de facto (búsqueda exhaustiva, argumento por descarte,
   precedente directo) pero esa sesión no podía registrar el cierre
   (estaba contaminada, `§12`) y este acto no tiene mandato para mover
   ninguna fila de `canon/modelo-decision-v4_0.md` (fuera de mi perímetro,
   además). Si mesa decide que sí es cierre, la fila de `deferencia` podría
   pasar de "solo proxy" a algo formalmente equivalente a "sin reactivo —
   búsqueda cerrada" (el estado que ya usan `aversion_riesgo`/`sens_estatus`,
   `canon/modelo-decision-v4_0.md:725`) — sin que el conteo `9 de 14` se
   mueva, porque `deferencia` seguiría sin `MEDIDO`.
2. **¿Vale la pena instrumentar el diseño muestral de ENCUP 2012 alguna
   vez?** Es xlsx único, sin documento de diseño separado en el corpus.
   Nombrar ponderador/estrato/UPM exige abrir el archivo — contaminación
   garantizada por ADR-46 para quien lo haga. Sin una sesión que acepte
   ese costo una vez y lo deje escrito en una nota, **ningún acto futuro
   con sesión limpia puede pasar la premisa de diseño muestral para
   ningún constructo vía ENCUP 2012**, no solo `deferencia` — es un
   bloqueo estructural del patrón CAL-CONF contra esta fuente específica,
   no un defecto de este acto. `confianza_institucional[electoral]`
   (candidata de posición 9, ya anotada en el manifiesto) tropezaría con
   el mismo muro si alguna vez se intenta medir con sesión limpia.
3. **(Menor) ¿Revisitar la frase-criterio de `deferencia` (paso 1 §2) para
   admitir legitimidad-legal?** Cambiaría el veredicto sobre `P44A`, pero
   reabre una decisión conceptual ya tomada en Encargo C con `ENCUCI
   AP5_11` bajo el mismo criterio. No se recomienda sin evidencia nueva;
   se deja escrita por completitud, no como sugerencia.

## 5 · Contador

**Sin movimiento. 9 de 14**, confirmado vigente contra HEAD real
(`canon/modelo-decision-v4_0.md:277/621/725`, `4b27869`). `deferencia`
permanece `PROXY CON SUPUESTO DECLARADO (M3, Latinobarómetro `P4NOIJ`,
ADR-51(f))`, cuenta 3 de 14, sin cambio.

## 6 · Perímetro

No se tocó `README.md`, `AVISO-DE-ALCANCE.md`, `canon/estado-*`,
`canon/modelo-decision-v4_0.md` (contenido), ni `tests/check.py` — eso es de
Acto 1. No se creó `tests/cal_encup_deferencia.py` — no hay medición que
correr. No se tocó `milpa/procedencia.yaml` — no hay entrada de medición que
declarar. Este acto solo agrega esta nota y una línea en
`forense/hallazgos.md`.

## 7 · Suite, corrida al cierre

```
$ python3 tests/check.py --baseline
exit=0 · LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
$ python3 tests/validador_registro_ids.py
exit=0 · OK — 49 IDs verificados, todos con ancla y tier consistentes
$ git status --short   (antes y después de la suite, idéntico)
?? data/raw
```
