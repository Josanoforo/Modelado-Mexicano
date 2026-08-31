# Agente de despacho · v1.0 — runbook de mesa

**P3** de `ACTO MAESTRA33-E2 · AGENTE-DESPACHO-1`
(`forense/encargos/2026-08-31-MAESTRA33-E2-AGENTE-DESPACHO-1.md`, SHA de
redacción `af41796`).

Este archivo es para **mesa**, no para el ejecutor. Dice cuatro cosas:
qué se congeló (§0), qué se pega en la segunda tarea recurrente (§1),
qué esperar de cada tick y cómo leerlo en dos minutos (§2), y cuándo
apagar la tarea (§3).

La primera automatización (`ACTO MAESTRA33-E1 · AGENTE-TRAMITE-1`,
`ADR-239`) puso un agente que **hace el papeleo**: corre la suite, lista
lo que envejece, redacta el PR de trámite. Esta segunda pone uno que
**ejecuta encargos**: toma el más antiguo de una cola que mesa autorizó,
lo marca en curso y lo corre con `/acto`. Son deliberadamente distintos:
el de trámite nunca decide nada, y el de despacho nunca decide **qué**
se ejecuta — solo **cuándo**, y solo sobre lo que mesa ya fusionó.

---

## §0 · SPEC CONGELADA — COMMIT-1 del acto

Las cuatro piezas quedan congeladas aquí antes de que el despachador
mueva un solo encargo. **El primer resultado que produzca este
procedimiento es el que se reporta.**

### P1 · La convención de cola — `forense/encargos/cola/`

Un directorio nuevo bajo `forense/encargos/`, con **un archivo por
encargo**, nombrado con la convención que ya rige el directorio padre
(`forense/encargos/convencion.md`): `AAAA-MM-DD-<CÓDIGO>-<tema>.md`.

Cada archivo tiene **dos partes**, y la frontera entre ellas es lo que
hace la pieza segura:

```
ESTADO: LISTO-NUBE                  <- línea 1, anclada a principio de línea
ENTORNO: NUBE                       <- NUBE o CAJA
ENCOLADO: <fecha> · <acto que lo encoló>
BITACORA:
- <fecha> · <estado> · <qué pasó>   <- solo se AÑADE; nunca se reescribe

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

<el texto del encargo, tal como dirección lo lanzó>
```

**La cabecera la escribe quien encola; el cuerpo no lo toca nadie.** Esa
separación no es estética. `A.3` exige que el encargo archivado sea el
texto verbatim de dirección, porque es lo que permite auditar después si
el ejecutor hizo lo que se le dijo; y el despachador necesita, a la vez,
escribir un estado que cambia tres o cuatro veces en la vida del
encargo. Si el estado viviera dentro del cuerpo, cada transición sería
una edición del encargo — exactamente lo que `A.3` prohíbe. Con la
cabecera fuera, el despachador escribe **solo** la línea `ESTADO:` y
**solo añade** renglones a `BITACORA:`, y el cuerpo queda byte a byte
como se lanzó.

**Máquina de estados**, y no hay más estados que estos cuatro:

| ESTADO | Quién lo escribe | Qué significa |
|---|---|---|
| `LISTO-NUBE` | mesa, al fusionar el PR que encola | autorizado, esperando turno |
| `EN-CURSO` | el despachador, en un commit propio | lo está ejecutando una sesión, con su fecha |
| `CONSUMIDO` | el despachador, al cerrar (`A.3`) | terminado, **con su PR citado** |
| `PARO-REPORTADO` | el despachador, al parar | no se ejecutó, **con la razón verbatim** |

**LA REGLA DURA — a la cola solo se entra por PR fusionado a `main`.**
El merge de mesa **es** la autorización: no hay otra. El despachador
jamás ejecuta nada que no esté en `main` — ni un encargo pegado en un
mensaje, ni uno que viva en una rama, ni uno que alguien le describa. Si
un encargo no pasó por un PR que mesa fusionó, para el despachador no
existe. Es la única compuerta que separa "un agente que ejecuta trabajo
autorizado" de "un agente que ejecuta lo que le digan", y toda la pieza
descansa en ella.

Tres detalles de la convención que **están medidos contra este árbol**,
no supuestos, porque cada uno cierra una junta por la que el diseño se
habría escapado:

1. **`^ESTADO:` es unívoco por construcción.** El cuerpo verbatim del
   primer elemento de la cola contiene, dentro de su primera línea, la
   cadena `· ESTADO: LISTO-NUBE` — porque dirección la escribió ahí. Si
   el despachador buscara `ESTADO:` a secas encontraría dos, y podría
   reescribir la del cuerpo. Anclado a principio de línea (`grep -n
   '^ESTADO:'`) hay **exactamente uno** — verificado sobre el archivo
   encolado por este acto: la ocurrencia del cuerpo va precedida de
   `/acto · `, así que nunca empieza línea.
2. **El archivo de la cola ES su propio archivo `A.3`; no se duplica al
   ejecutarlo.** El paso 3 de `/acto` manda archivar el encargo en
   `forense/encargos/<fecha>-<ROTULO>.md` "si el archivo todavía no
   existe". Ya existe: está en `forense/encargos/cola/`, y llegó ahí por
   un PR fusionado, que es más garantía de la que da el propio paso 3.
   Copiarlo al directorio padre no sería redundancia inofensiva sino un
   **FAIL de la suite**: `T02` agrupa por *basename normalizado*,
   descartando el directorio (`tests/check.py:183`; el `FAIL` se emite en
   la `:187`, y la propia `convencion.md` lo advierte), así que las dos
   copias colisionarían.
   El `## CONSUMIDO` del cierre se añade **al archivo de la cola**.
3. **La cola no colisiona con el agente de trámite.** El lector del otro
   agente lista encargos sin marca con `glob.glob(.../encargos/*.md)`
   —plano, no recursivo— en `tools/digesto_tramite.py:366`, y declara ese
   comando en su propia salida (`grep -L '^## CONSUMIDO'
   forense/encargos/*.md`). `cola/` queda fuera de ese universo, así que
   un encargo encolado y todavía no ejecutado **no** aparece como
   "encargo sin marca" ni tienta a la otra skill a marcarlo. Verificado
   por lectura del código, no por suposición.

### P2 · `.claude/commands/despacha.md` — el actor

Un **tick** del despachador es esto, en orden, y nada más:

1. **Arranque ligero** — clon y SHA contra `origin/main`. No es el
   ARRANQUE de cinco puntos de `/acto`: el despacho en sí no abre
   microdato ni descarga nada. El encargo que ejecute correrá su propio
   ARRANQUE completo, que es donde eso importa.
2. **CANDADO** — mecánico, dos comprobaciones. Si **cualquiera** de las
   dos da positivo: reporta y **termina con cero commits**. Una sesión de
   nube a la vez.
3. **Selección** — el `LISTO-NUBE` más antiguo con `ENTORNO: NUBE`, por
   orden de nombre de archivo (que empieza por la fecha). Determinista.
4. **Marca `EN-CURSO`** en un **commit propio**, empujado antes de
   empezar el trabajo: es lo que hace que el candado del siguiente tick
   vea que hay algo en vuelo.
5. **Ejecuta** el encargo con `/acto` **verbatim**, sobre el cuerpo del
   archivo de la cola.
6. **Cierra**: `CONSUMIDO` con su PR, o `PARO-REPORTADO` con la razón.

**Guardrails**, que mandan sobre cualquier otra línea de la skill:

- **Nunca edita el cuerpo de un encargo.** Una premisa que no se
  sostiene es **`PARO-REPORTADO`**, y eso **es un entregable**, no un
  fracaso: encontrar que el terreno no es el que el encargo supone vale
  más que un resultado producido sobre terreno equivocado.
- **No reintenta un PARO por su cuenta.** Un `PARO-REPORTADO` se queda
  parado hasta que mesa lo vuelva a encolar. Un agente que reintenta
  solo convierte un hallazgo en un bucle.
- **No crea ni redacta encargos.** Eso es de dirección. El despachador
  solo ejecuta lo que ya está en `main`.
- **No ejecuta `ENTORNO: CAJA`.** Los lista como **"esperando caja"** y
  no los toca: abren microdato y van a Ubuntu, sin excepción.
- **No firma, no aprueba y no fusiona.** Fusionar es firmar.
- **Nunca dos actos a la vez.** Es lo que el candado protege.
- **CONTADOR del tick: el que muevan los encargos que ejecuta; el
  despacho en sí, cero.** El vehículo no mide; mide la carga.

**El CANDADO, con los comandos que de verdad corren en este entorno.**
Medido el 31/ago/2026 en la nube: **`gh` no existe** (`which gh` no
imprime nada y sale con 1; `gh --version` → `command not found`), así que
el candado **no puede** depender de la API de PRs. Se hace con `git`
puro, y son dos — que **no son redundantes**: `(b)` atrapa a una sesión
viva, porque durante todo un tick el `EN-CURSO` vive en una rama sin
fusionar; `(a)` atrapa un `EN-CURSO` que sí llegó a `main` y cuyo acto
nunca terminó. Quitar cualquiera de las dos abre el hueco:

- **(a) ¿Hay un `EN-CURSO` en la cola?** Se lee **de `origin/main`**, no
  del árbol de trabajo (`git ls-tree -r --name-only origin/main --
  forense/encargos/cola/` y `git show origin/main:<archivo>`): es la regla
  dura del guardrail 1 aplicada al propio candado — lo que no está en
  `main` no cuenta, ni siquiera para bloquear. Uno o más → otra sesión
  está trabajando. Se reporta, con su fecha, y se termina.
- **(b) ¿Hay una rama de acto abierta en el remoto?**
  `git ls-remote --heads origin` — **estado vivo**, y es el único que
  vale. `git for-each-ref refs/remotes/origin` refleja el último `fetch`
  y puede traer ramas que el remoto ya borró: sirve de **RESPALDO
  declarado** si el remoto no responde, nunca como fuente primaria.
  Mismo criterio que la sección C del otro agente
  (`forense/agente-tramite-v1_0.md` §0).
  Una rama distinta de `main` **no** basta para parar: una rama
  fusionada y no borrada seguiría ahí para siempre y dejaría al
  despachador apagado. "Abierta" es **no contenida en `main`**, y se
  prueba: `git fetch origin <rama>` y luego
  `git merge-base --is-ancestor FETCH_HEAD origin/main` — si es
  ancestro, ya está fusionada y no cuenta.

Los dos comprobantes declaran **cuántos archivos y cuántas ramas
examinaron** (`A.13`), y el bloqueante se reporta **con su fecha** en los
dos casos, para que mesa vea desde cuándo está cerrado. Al 31/ago/2026,
antes de que este acto empujara su propia rama, el remoto tenía **1**
rama viva (`main`).

**Lo que hace que el candado sea un candado y no una costumbre.** El
chequeo (paso 2) y la marca (paso 4) no son atómicos: entre uno y otro
caben segundos en los que otra sesión pasaría su propio chequeo. Tres
cosas cierran esa ventana, y las tres están en la skill: (1) el nombre de
rama es **invariante por encargo** (`claude/despacha-<CÓDIGO>`, sin la
fecha de hoy), así que dos sesiones que elijan el mismo encargo —y la
selección es determinista, luego lo harán— derivan el **mismo** nombre y
el segundo `push` lo rechaza el remoto; ese rechazo es el único punto
**atómico** del tick, y por eso se le deja decidir; (2) un `push`
rechazado significa **ceder**, nunca forzar ni renombrar; y (3) tras
empujar el cerrojo, la skill **re-verifica** el candado antes de empezar
a trabajar, y cede si apareció otra rama. Ceder de más cuesta un tick;
empatar y seguir los dos es lo único que esta pieza no puede permitirse.

**Consecuencia que mesa debe conocer, porque no es un defecto sino el
diseño:** el guardrail 7 prohíbe al agente fusionar su propio PR, así que
entre que un tick abre su PR y mesa lo firma, su rama sigue abierta y
`(b)` mantiene la cola parada. **La cola avanza al ritmo al que mesa
fusiona.** Si mesa tarda una semana, la cola espera una semana — y cada
tick lo dice, con la fecha, en vez de callarse.

**Dos campos del encargo que la skill lee y no obedece a ciegas.**
`COMPUERTA:` es la línea de compuerta a efectos del paso 2 de `/acto`,
aunque ese paso hable de `GATED a …`: los encargos de esta cola escriben
la suya como `COMPUERTA:`, y leer que "no hay `GATED a`, luego no está
compuertado" sería adelantar el acto sin verificar, que es el defecto que
`/acto` existe para no volver a pagar. Y `MODELO SUGERIDO:` se **lee y se
reporta**, no se obedece: el modelo de la sesión lo fija la tarea
recurrente de mesa, pero si no coincide con el que el encargo sugiere, el
PR lo dice — para que mesa pueda descartar un resultado sin tener que
adivinar por qué salió raro.

### P3 · este archivo

Runbook de mesa. §1 el prompt, §2 cómo leer un tick, §3 el falsador.

### P4 · El primer elemento de la cola

`forense/encargos/cola/2026-08-31-MAESTRA33-B2-MARCO-M-SORTEA-v1_1.md`
— el encargo `MAESTRA33-B2 · MARCO-M-SORTEA-v1_1`, verbatim, con
`ESTADO: LISTO-NUBE`. Lo ejecutará el despachador en su primer tick;
**este acto no lo ejecuta**.

Sus premisas se verificaron contra el árbol antes de encolarlo, porque
encolar un encargo muerto sería el defecto que esta pieza existe para
evitar. Las seis se sostienen: los dos artefactos v1_1 están en `main`
(mismo commit `77939ce`), el `sha256` del congelado re-computa idéntico
al declarado, `semilla_desde_sha_merge` está donde el encargo dice
(`forense/prereg-duelo-v2/sorteo_v2.py:191`, dos parámetros), `ADR-231`
§e está en `canon/gobernanza-v1_15.md:4143`, el resultado v1_1 todavía
no existe, y el v1_0 da la forma del archivo a escribir.

**Y una junta que conviene tener escrita antes de que alguien la pise**
—no cambia el encargo ni una letra, solo señala lo que el propio árbol
ya advierte por escrito—: el marco congelado v1_1 trae **dos** columnas
que se pueden leer como "elegible", y **dan números distintos**:
`elegible` da 23 y `elegible_v1_1` da 22. La buena es la segunda, y
coincide con `grado_DD` (22 `P1 PUNTUA` / 5 `P0 VERIFICACION-NO-PUNTUA`).
El propio sidecar `CONGELADO-M-v1_1.sha256` lo dice en su
`nota_lectura`, y el cargador existente `sorteo_marco_m.cargar_marco_m`
apunta a rutas v1_0 y no conoce la columna nueva. Por eso el encargo
manda "deriva, no heredes" y autoriza "cargadores propios si hace falta"
(precedente `ADR-178`): quien lo ejecute filtra por `elegible_v1_1` y
**declara la columna que usó**. Con 22, `ADR-231` §e cae en el tramo
`15≤N<30` → `n_sorteo = ceil(22/2) = 11`, que es exactamente lo que
`ADR-238` ya precalculó.

---

## §1 · El prompt de la segunda tarea recurrente

Cadencia sugerida: **2 veces por día hábil, desfasada de la de
trámite**. El otro agente corre una vez al día; este corre dos, y en
horas distintas, para que las dos sesiones de nube no se pisen. Si mesa
pone la de trámite temprano, estas dos van a media mañana y media tarde.
La recurrencia vive en la tarea de mesa en Claude Code — **este acto no
crea ningún `schedule` en GitHub Actions**, por la misma razón que el
anterior: `.github/workflows/verify.yml` es compuerta de CI, y meterle
una tarea de fondo mezclaría dos cosas que fallan distinto.

Pega esto, tal cual, como prompt de la tarea recurrente:

```text
Corre /despacha sobre este clon. Entorno NUBE: no abras microdato ni descargues nada.
CANDADO primero: si hay un EN-CURSO en forense/encargos/cola/ o una rama de acto abierta en el remoto, reporta y termina con cero commits.
Si no, toma el LISTO-NUBE mas antiguo con ENTORNO: NUBE, marcalo EN-CURSO en un commit propio, y ejecutalo con /acto verbatim.
Nunca edites el cuerpo de un encargo: una premisa que no se sostiene es PARO-REPORTADO, se reporta con la razon verbatim y no se reintenta.
Abre UN PR y NO lo fusiones. Los encargos ENTORNO: CAJA se listan como esperando caja y no se tocan.
```

Cinco líneas. Todo lo demás —el candado, la selección, la máquina de
estados, los guardrails— vive en la skill, versionado en el repo, no en
el prompt: la lección de `D-10` es que el texto que se transcribe a mano
se desfasa, y el que vive en el repo no.

## §2 · Qué esperar de cada tick, y cómo leerlo en dos minutos

Un tick sano termina en **uno de tres sitios**, y los tres son
resultados legítimos:

- **CANDADO CERRADO.** "Hay un `EN-CURSO`" o "hay una rama de acto
  abierta", con su conteo de archivos y ramas examinados, **la fecha
  desde la que bloquea**, y **cero commits**. Es el resultado más común y
  es el correcto: quiere decir que la pieza está haciendo justo lo que se
  le pidió. Cuenta aquí también el cierre **tardío**: el tick que ya
  había puesto su cerrojo, vio aparecer otra rama (o le rechazaron el
  `push`) y cedió — cede el que pierde la carrera, siempre, sin forzar.
- **COLA VACÍA.** Ningún `LISTO-NUBE` con `ENTORNO: NUBE`. Lista lo que
  hay esperando caja y termina con cero commits. Que la cola esté vacía
  es información de mesa: significa que dirección no ha encolado nada.
- **UN ACTO EJECUTADO.** Un PR, con el `CONSUMIDO` (o el
  `PARO-REPORTADO`) escrito en el archivo de la cola, y la cascada de
  cierre que el propio `/acto` manda.

Y hay una asimetría que conviene tener presente al leer: bajo uso normal
el que va a saltar es el candado de **rama abierta**, no el de
`EN-CURSO`, porque durante todo un tick el `EN-CURSO` vive en una rama
sin fusionar y `main` no lo ve. El de `EN-CURSO` es el que queda cuando
la rama ya no está.

Cómo leerlo en dos minutos: mira **la línea `ESTADO:`** del archivo de
la cola que el PR toca y **su `BITACORA:`** — esas dos líneas cuentan
toda la historia del encargo. Después, el PR del acto se lee con el
criterio de siempre.

**Lo que nunca debe aparecer en un tick**, y si aparece hay que apagar:

- Un encargo ejecutado que **no venía de la cola en `main`**.
- Un cuerpo de encargo **modificado**.
- Un `PARO-REPORTADO` **reintentado** sin que mesa lo reencolara.
- **Dos** sesiones de nube trabajando a la vez.

**Fusionar es firmar**, aquí también. El despachador propone un acto
ejecutado; la firma la da mesa al fusionar.

## §3 · Falsador, a un mes

Se **apaga la tarea** y **se anota**, si en un mes ocurre cualquiera de
las dos:

- **(a)** el despachador **ejecuta algo fuera de la cola** o **fuera de
  `main`** — cualquier cosa que mesa no autorizó con un merge;
- **(b)** **dos sesiones de nube coinciden por su causa** — el candado
  falló en lo único que tiene que hacer.

Cualquiera de las dos, con el caso citado, apaga la tarea recurrente y
dispara revisión de la pieza que falló. Es el mismo criterio de
caducidad que `D-10`..`D-13` (`instrucciones-proyecto-v2_12.md`) y que
el falsador del agente de trámite (`forense/agente-tramite-v1_0.md` §3).

Y la prueba de que la pieza sirvió, para el otro lado: que un encargo
encolado por dirección **se ejecute sin que nadie abra una sesión a
mano**, y que el registro de qué se pidió, cuándo se ejecutó y con qué
PR quede completo en un solo archivo, legible por mesa sin reconstruirlo
de una conversación.

**CONTADOR de este acto: cero mediciones, declarado.** Es
infraestructura: instala el vehículo, no mide con él.
