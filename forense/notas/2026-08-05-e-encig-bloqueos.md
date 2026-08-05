# Acto E-ENCIG · Sellar D-ABC, medir el genérico, re-estimar β(edad) — los tres bloqueados, ninguno inventado

Contadores movidos: 0

*5 de agosto de 2026 (00:54 CST, `TZ=America/Mexico_City date`).*

**Resultado de este acto, dicho antes que nada: NO SE SELLÓ NINGÚN ADR, NO
SE MIDIÓ NINGÚN GENÉRICO, NO SE RE-ESTIMÓ NINGÚN β(edad).** Las tres
tareas del encargo se verificaron contra el árbol real y las tres tienen
un bloqueo concreto, no una dificultad que ceder resuelva:

1. **Tarea 0 (D-A/D-B/D-C).** El encargo instruye sellar "con el texto
   que mesa ya te dio, verbatim". Ese texto no está en el encargo recibido
   por este acto, ni existe en ningún archivo del repo (buscado
   explícitamente, §2). Sellar habría exigido que este acto *inventara*
   la función de enlace o la propia redacción de la decisión — exactamente
   lo que el encargo mismo prohíbe.
2. **Tarea 1 (genérico servidores públicos).** Este entorno es
   `cloud_default`, sin `data/raw` poblado y sin corpus compartido
   montado en ningún punto del disco. La sonda de red a INEGI confirma
   bloqueo de política, no ausencia del recurso. El encargo afirmaba "Sí
   abre microdato ENCIG (está en disco)" para este entorno — no se
   sostiene contra el terreno verificado.
3. **Tarea 2 (β(edad) en escala invariante).** Mismo bloqueo de dato que
   Tarea 1. Además, verificado que los agregados ya publicados por actos
   previos no traen lo necesario para derivar razón de momios/riesgos por
   celda de edad sin abrir microdato (§4).

Cada uno se documenta abajo con el comando y la cita que lo sostiene. Los
tres son "impidió medir", no "no impidió medir" — las tres tareas
sustantivas del encargo quedan sin producir el número que pedían.

---

## 0 · ARRANQUE (Bloque D v2.4)

**1 · REPO.** Clon existente, no clonado de nuevo:

```
$ pwd
/home/user/Modelado-Mexicano
$ git log -1 --format="%h %s"
06d04be Merge pull request #118 from Josanoforo/claude/encargo-m4-r1-3-adjudicacion-czqze3
$ git status
On branch claude/bloque-arranque-verificacion-4rps2k
nothing to commit, working tree clean
```

No se arrancó desde el home.

**2 · SHA.** El encargo declara base `06d04be` — coincide exactamente con
`HEAD` (arriba), sin refresco necesario. `git branch -a` confirma
`origin/main` y `origin/claude/bloque-arranque-verificacion-4rps2k` (esta
rama) únicamente — cero ramas vivas ajenas, coincide con lo que el
encargo declaraba en su §2.

**3 · data/raw.** Ausente — esperado, raíz gitignorada:

```
$ ls data/raw
ls: cannot access 'data/raw': No such file or directory
```

Este acto SÍ necesita microdato (Tareas 1 y 2), así que corresponde
enlazar al corpus compartido. Barrido para encontrarlo, con resultado
negativo:

```
$ find / -xdev -iname "*encig*" | grep -v /proc | grep -v Modelado-Mexicano/forense
(sin resultados)
$ find / -xdev -iname "conjunto_de_datos*" -o -iname "*TMODULO*" -o -iname "encig*.csv" -o -iname "encig*.zip"
(sin resultados)
$ find / -xdev -iname "raices.local.yaml"
(sin resultados)
$ mount | grep -v "^cgroup\|^proc\|^sys\|^tmpfs\|^devpts\|^mqueue\|^shm"
devtmpfs on /dev ...
/dev/vda on / type ext4 (rw,relatime,...)
/dev/vdb on /opt/rclone type squashfs (ro,...)
/dev/vdc on /opt/claude-code type ext4 (ro,...)
/dev/vdd on /opt/env-runner type ext4 (ro,...)
/dev/vde on /mnt/skills/public type squashfs (ro,...)
/dev/vdf on /mnt/skills/examples type squashfs (ro,...)
$ ls /home/user/
Modelado-Mexicano   ← único directorio, sin worktrees hermanos
```

`/home/user/Modelado-Mexicano/corpus/` existe pero es el ESPEJO del
proyecto (`corpus/indice.yaml`, `corpus/reports/`, `corpus/forense/` —
reports y notas narrativas, no microdato; exactamente lo que el punto 5
del arranque prohíbe usar para cifras). No hay ningún `mm-corpus`, ningún
`data_raw` externo, ningún worktree hermano en este contenedor. **No hay
corpus compartido que enlazar** — se declara en vez de fingir que se
enlazó (ver §3 abajo para la implicación).

**4 · ENTORNO.**

```
$ echo "CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE"
CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
```

`cloud_default` es firma correcta de nube (ADR-59(b)) — coincide con lo
que el encargo declara para este acto ("Entorno: nube · NO en Ubuntu").
Este acto sí toca red (Tarea 1/2 lo exigen), sonda con `-o` a archivo
real, nunca `-I`:

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
000
$ curl -sS "$HTTPS_PROXY/__agentproxy/status"
{ ... "recentRelayFailures": [
    { "host": "www.inegi.org.mx:443",
      "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)" }
  ] }
```

`000` con `403` de política al `CONNECT` mismo — no es 404 del sitio, es
la misma firma de bloqueo de política de egreso que ya documentaron otros
actos en `cloud_default` (`forense/hallazgos.md`: entradas del 4/ago sobre
posición-4-rehecha paso 1 y su reemisión, y sobre el intento de `PR #61`).
El encargo afirmaba "Red: solo git" para este acto — consistente con lo
verificado.

**5 · ESPEJO.** No se usó para ninguna cifra de este documento. Todas las
citas salen del clon de (1) o de comandos mostrados en este mismo
archivo.

**ENTORNO ASIGNADO.** Nube (`cloud_default`), NO Ubuntu — confirmado, no
se lanzó en otro.

**PERÍMETRO Y CONCURRENCIA.** Este acto toca únicamente `forense/`
(este archivo y una línea en `forense/hallazgos.md`) — no toca `canon/`
ni `milpa/procedencia.yaml`, porque no hay nada que sellar ni medir (ver
§§2-4). `mcp__github__list_pull_requests` (state=open) devuelve un solo PR
abierto: **#119** (`sesion/p-lapop-microdato` → `main`, base `06d04be`,
mismo SHA declarado por este encargo), que solo añade
`forense/notas/2026-08-05-p-lapop-microdato.md` — sin traslape con el
perímetro de este acto. `git branch -a` no muestra ninguna otra rama
remota viva. Consistente con la declaración del encargo: "los otros tres
actos de esta tanda no tocan `canon/` ni `procedencia.yaml`".

---

## 1 · §2 del encargo (actualización de mesa) — verificado, correcto

- **M-4 cerró.** `canon/gobernanza-v1_15.md:776` trae ADR-63 completo:
  "adjudica `R1.3` → veredicto `E`". `canon/estado-programa-v1_10.md:95`
  y `:196` confirman Hito D en **13 de 27**, con `R1.3` → `E` en la lista.
  Coincide con el encargo.
- **ADR máximo = 63, sin huecos.** `canon/gobernanza-v1_15.md:8` lo dice
  explícito ("el último es **ADR-63**") y el detalle §4 enumera ADR-44 a
  ADR-63 consecutivo. Coincide.
- **Cero ramas vivas ajenas.** Confirmado en §0 arriba (branch -a) y con
  `list_pull_requests` (un solo PR abierto, #119, sin traslape).

Nada de este bloque necesitaba corrección. Se re-derivó, no se copió.

---

## 2 · Tarea 0 — por qué D-A/D-B/D-C no se sellan

**La cita del encargo se verificó, es exacta.**
`milpa/procedencia.yaml:780-781`:

```
      comparable en magnitud contra el 0.70 ASIGNADO (ningún ADR de D-ABC
      ha sellado función de enlace a la fecha de este commit). Techo:
```

Coincide carácter por carácter con lo que el encargo cita (entrada
`G4_exposicion_violencia`).

**Las 5 entradas existen, confirmado por conteo directo:**

```
$ grep -n "^  G1_\|^  G3_\|^  G4_" milpa/procedencia.yaml
660:  G1_radio_confianza:
709:  G1_confianza_institucional:
741:  G3_familismo_apoyo:
769:  G4_exposicion_violencia:
800:  G4_confianza_institucional_justicia:
```

G1×2, G3×1, G4×2 — coincide con el encargo. Las cinco tienen β̂ con
IC95%, ninguna carece de estimación puntual.

**El bloqueo real: el "texto que mesa ya te dio, verbatim" no existe en
ningún lugar accesible a este acto.** Búsqueda explícita, antes de
escribir nada:

```
$ find . -iname "*enlace*" -not -path "./.git/*"
./corpus/forense/Apuestas_Conductuales_...   ← ESPEJO, no cuenta (arranque §5)
$ find . -iname "*especificacion*" -not -path "./.git/*" | grep -iv "R1_3\|R3_1\|R7\|R4\|R9\|R5"
(sin resultados)
$ grep -rn "D-A)\|D-B)\|D-C)\|(D-A)\|(D-B)\|(D-C)" --include="*.md" --include="*.yaml" .
(sin resultados, fuera de .git)
```

No hay un archivo de especificación pre-declarada para D-A/D-B/D-C — a
diferencia del precedente correcto de este mismo tipo de acto,
`hitoD-R1_3-especificacion-v1_0.md`, que ADR-63 (`forense/notas/2026-08-05-
m4-adjudicacion-adr-63.md §2`) sí pudo verificar palabra por palabra
contra un veredicto ya escrito. Aquí no hay nada contra qué verificar: el
encargo describe la EXISTENCIA del bloqueo (correcto, verificado arriba)
pero nunca transcribe la decisión que pide sellar.

**Componer yo mismo D-A/D-B/D-C no es una alternativa razonable — es
precisamente lo que el encargo prohíbe dos veces:**

- A-bis regla 3 (`instrucciones-proyecto-v2_4.md:85`): "Una diferencia de
  proporciones y un coeficiente de índice no son la misma cosa salvo que
  el modelo declare una función de enlace." Escribir esa función ahora,
  sin que mesa la haya decidido, sería inventarla para poder llenar la
  casilla — el error que la propia regla nombra.
- `canon/modelo-decision-v4_0.md:149`: "La forma funcional NO se inventa
  en este acto... Donde no hay evidencia, la condicional queda declarada
  con forma **PENDIENTE** y tier honesto. Inventarlas para poder
  multiplicar celdas sería teclear una cifra esperada."

Y el propio encargo (§3) lo anticipa: *"Si no puedes hacerlo sin inventar
forma funcional, PARA y repórtalo — es exactamente el punto donde una
mesa anterior se detuvo a tiempo."* Ese punto ya existe, y es anterior a
este acto: `forense/notas/2026-08-04-w-coeficientes-generador-paso1.md:298-
310` (Encargo W, el mismo acto que midió los tres β̂ marginales
originales) declaró explícitamente *"No hay función de enlace declarada
entre las dos (§1 del encargo, pendiente abierta, **no resuelta aquí**)"*
— y ADR-57(a) (`gobernanza:` detalle §4), que sí llegó a sellar sobre
estos mismos números, tampoco declaró una función de enlace: selló
"asociar ≠ identificar", no la traducción de escala. La pendiente sigue
abierta hoy, sin que este acto la pueda cerrar de forma honesta.

**Se para aquí.** `0 de 15` sigue en `0 de 15`. Ningún ADR nuevo.

---

## 3 · Tarea 1 — por qué el genérico no se mide

**La entrada existe tal como la cita el encargo.**
`milpa/procedencia.yaml:287-300`:

```yaml
condicionales_escalares_confianza_generica:
  confianza_institucional_generico_servidores_publicos:
    clase: "PENDIENTE -- medición condicional por atributos NO CORRIDA en este acto"
    instrumento: "ENCIG 2023, encig2023_01_sec_11 (batería XI, sección 'Confianza en instituciones')"
    item: "P11_1_23 -- 'servidores(as) públicos(as) o empleados(as) de gobierno' (ítem 23 de 25)"
```

Coincide con el encargo. La nota de esa misma entrada ya declara, desde
antes de este acto: *"Solo existe el β̂ MARGINAL de este reactivo... este
bloque registra el reactivo y su estado de cobertura, no lo condiciona
sobre atributos ni fabrica un número que nadie corrió."* — exactamente lo
que este acto tampoco puede hacer, por la misma razón que esa nota ya
tuvo: no hay microdato abierto.

**El bloqueo es de terreno, no de esfuerzo — verificado, no supuesto.**
Ver §0.3-§0.4 arriba: sin `data/raw`, sin corpus compartido localizable en
ningún punto de este contenedor, sin red a INEGI (`000`/`403` de
política). El patrón es idéntico, comando por comando, al que ya
documentaron tres actos previos de este mismo programa en
`cloud_default`:

- `forense/hallazgos.md`, 4/ago: *"este entorno es nube sin `data/raw/`
  poblado, y la sonda de alcanzabilidad... dio `000`... el proxy del
  entorno respondió `403` al `CONNECT` mismo... **NO ALCANZABLE DESDE
  ESTE ENTORNO**"*.
- `forense/hallazgos.md`, 4/ago (reemisión): *"`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`,
  sin `data/raw/` poblado, misma firma de bloqueo... **NO ALCANZABLE
  DESDE ESTE ENTORNO**, otra vez"*.
- ADR-59(b) mismo (`gobernanza:` detalle §4): *"`cloud_default` sin sonda
  es firma correcta de un acto de nube"* — es decir, el propio canon ya
  fijó que un acto de nube SIN red a INEGI es el comportamiento esperado,
  no la anomalía.

**El encargo, en cambio, afirmaba para este acto exacto:** *"Entorno:
nube · NO en Ubuntu · Red: solo git · Sí abre microdato ENCIG (está en
disco)."* Las primeras tres cláusulas se verificaron y son correctas. La
cuarta — "está en disco" — se verificó y es falsa contra este contenedor:
no hay ningún archivo ENCIG, en ningún directorio, en ningún punto
montado (§0.3). Es exactamente "el terreno no es el que el encargo
supone" que el propio arranque instruye reportar, no ceder.

**Se para aquí.** El contador `9 de 14` no se mueve — sigue en `9 de 14`.
La entrada de `procedencia.yaml:289` sigue `PENDIENTE`, sin editar.

---

## 4 · Tarea 2 — por qué β(edad) en escala invariante no se re-estima

Mismo bloqueo de dato que la Tarea 1 (mismo instrumento, ENCIG). Antes de
concluir que no hay nada que hacer, se revisó si los agregados YA
PUBLICADOS por el Encargo X (`forense/notas/2026-08-04-x-condicionamiento-
y-forma.md §4.2`, la fuente de `eje_condicionante` en
`procedencia.yaml:714`) alcanzan para calcular una razón de momios o de
riesgos por celda de edad sin reabrir microdato — sería reusar un número
ya corrido, no fabricar uno nuevo.

**No alcanzan.** La tabla de §4.2 trae, por celda de edad, `n(θ=1)`,
`n(θ=0)` y **la diferencia** `β̂ = p̂(θ=1) − p̂(θ=0)`:

```
| Edad | Nivel | n(θ=1) | n(θ=0) | β̂       | IC95%              |
| Edad | 18-29 | 3 680  | 4 511  | +0.0850  | [+0.0635,+0.1065]  |
| Edad | 30-44 | 5 624  | 5 747  | +0.0624  | [+0.0443,+0.0806]  |
| Edad | 45-59 | 4 635  | 5 095  | +0.0626  | [+0.0433,+0.0820]  |
| Edad | 60+   | 3 571  | 4 892  | +0.0380  | [+0.0227,+0.0533]  |
```

Una razón de riesgos o de momios exige `p̂(θ=1)` y `p̂(θ=0)` **por
separado**, en cada celda — no solo su diferencia. Esos dos valores
individuales solo están publicados para el marginal completo (sin
condicionar por edad), en `forense/notas/2026-08-04-w-coeficientes-
generador-paso1.md:272`: `p̂(θ=1)=0.0736`, `p̂(θ=0)=0.1381` (`n`
20 245/17 510). No hay una tabla equivalente por celda de edad en ningún
documento de este repo — ni en la nota de origen, ni en `procedencia.yaml`,
que solo hereda el mismo resumen cualitativo ("las cuatro celdas... signo
positivo", `procedencia.yaml:714`). Calcular las cuatro razones por edad
exigiría exactamente lo que §0 ya estableció como inalcanzable: abrir
`encig2023_01_sec_11`/`encig2023_01_sec1_A_...` y cruzar por `ID_PER`
condicionando por edad — el mismo microdato, la misma ausencia.

**Tampoco se congela una especificación huérfana.** El encargo (§6) pide
declarar universo/ejes/dicotomizaciones *"antes de abrir dato"* como
primer commit de una estimación en dos commits. Congelar esa
especificación sin ninguna vía real de producir el segundo commit no
produciría una medición ni una decisión — produciría un pre-registro sin
dueño que la próxima sesión heredaría sin saber si sigue vigente. Se
prefiere declarar el bloqueo completo, una sola vez, con el motivo exacto
por el que no hay commit 1 (ver W1-P abajo, tampoco hay dato del que
partir).

**Sobre el precedente citado, W1-P.** El encargo lo invoca correctamente
como regla ("comparación entre estratos con tasas base distintas solo es
válida en una escala invariante") — el precedente vive en ADR-61
(`gobernanza:` detalle §4): *"corrige la lectura de escala de `W1-P` de
diferencia de proporciones a razón de riesgos"*. Es la razón por la que
este acto buscó los p̂ por celda antes de rendirse (párrafo anterior), no
una regla que este acto pueda aplicar sin los dos números por celda que
exige.

**Se para aquí.** No hay β̂(edad) que reportar, en ninguna escala.

---

## 5 · Declaración ADR-46 — separando estructura de contenido

Este acto **no abrió ningún archivo de microdato** (ninguno alcanzable,
§0.3) y **no tuvo contacto de red con INEGI ni con ningún host de ENCIG**
(la única sonda de red de este acto fue `curl` contra `www.inegi.org.mx`,
que devolvió `000` — bloqueado en el `CONNECT` del proxy, sin que ninguna
petición llegara al servidor real, sin cuerpo de respuesta que leer).

Lo que este acto sí leyó, y se declara con el criterio conservador de
ADR-46(4) ("declarar más exploración, no menos"), aunque sea contacto
indirecto (vía el propio canon del proyecto, no vía la fuente):

- **Estructura:** el rótulo del ítem `P11_1_23` ("servidores(as)
  públicos(as) o empleados(as) de gobierno"), su posición (23 de 25) y el
  nombre de la batería (XI, "Confianza en instituciones") —
  `milpa/procedencia.yaml:276,291`.
- **Contenido ya publicado por sesiones previas** (no generado por este
  acto): `p̂(θ=1)=0.0736`, `p̂(θ=0)=0.1381`, β̂ marginal `−0.0645`, y los
  cuatro β̂ por celda de edad — `forense/notas/2026-08-04-w-coeficientes-
  generador-paso1.md:272` y `forense/notas/2026-08-04-x-condicionamiento-
  y-forma.md:378-385`.

Esto es lectura de registros internos del propio corpus (mismo tipo de
lectura que cualquier acto hace de `procedencia.yaml`), no contacto con
la fuente primaria — pero como ambos documentos citan contenido derivado
de microdato real, se declara explícito para que una sesión futura que sí
tenga acceso a ENCIG sepa que este acto ya conoce esas cifras y no las
está re-derivando a ciegas.

---

## 6 · Qué no se hizo

No se tocó `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`,
`canon/modelo-decision-v4_0.md` ni `README.md` — no hay contador que
cascada porque ningún contador se movió. No se editó
`milpa/procedencia.yaml`. No se selló ningún ADR (`D-ABC` sigue sin
sellar). No se registró ningún valor en `coeficientes_generador_medidos`
ni en `condicionales_escalares_confianza_generica`. No se creó ningún
enlace simbólico falso en `data/raw` (no había corpus compartido real al
que enlazarlo, §0.3 — enlazar a un directorio vacío o inexistente habría
sido peor que declarar su ausencia). No se corrió ningún commit de
"especificación congelada" sin segundo commit real detrás.

---

## 7 · Suite

Cero marcadores de conflicto (`grep` de `<<<<<<<`/`=======`/`>>>>>>>`
sobre `.md`/`.yaml`/`.py`, sin resultados) confirmado antes de correr:

```
$ python3 tests/check.py --baseline
...
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

Sin cambio frente a la línea base — esperado, este acto no tocó ningún
archivo que la suite audite.
