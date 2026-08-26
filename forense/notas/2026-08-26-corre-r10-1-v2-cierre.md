# Nota de cierre · `ACTO CORRE-R10.1-v2`, Fase B — 26 de agosto de 2026

**Entorno:** UBUNTU, caja del acto `/home/pc0/mm-corre-r10-1`, rama `acto/corre-r10-1-v2-faseb`
sobre `origin/main` `cd6d10c`. **ADR:** `ADR-205`. **Firma:** `FP-161`, cerrada. **Contador del
Hito D: 24 de 27 → 25 de 27**, `13D·4B·4A·2E·2C`, re-derivado por parser.

---

## 1 · Arranque — lo que el encargo pidió comprobar antes de tocar nada

| paso | resultado |
|---|---|
| **1 · repo** | Caja del acto, no el worktree principal (`feedback_f0_corre_en_la_caja_del_acto`). Limpia al abrir. |
| **2 · SHA vs `ba0a7e4`** | `main` avanzó **54 commits** desde la redacción del encargo, y **38** desde el `HEAD` de la Fase A. Además, `PR #366` (Fase A) ya estaba **MERGED** (26/ago 02:50Z) y `HEAD` era ancestro de `origin/main`. Refrescado: rama nueva desde `origin/main`. **No fue PARO** — el propio ARRANQUE lo resuelve, tal como la nota de dirección anticipó. |
| **3 · `data/raw` sustantiva** | Corpus montado: **321 entradas, 9.6 GB**. |
| **4 · firma de entorno, tres partes (`A.2`)** | (i) `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` **sin definir** (`env \| grep -c CLAUDE_CODE_REMOTE` → 0), esperado en UBUNTU; (ii) sonda INEGI **cruda**, `GET` y no `curl -I`: `http=200`, `153,606` bytes, `text/html` — red viva y **no** el soft-404 del INEGI (200 + 2,263 bytes); (iii) `ls data/raw/` no vacío. **UBUNTU confirmado.** |
| **5 · cero cifras del espejo** | Todo número de esta corrida se computó hoy con `tests/hitod_r10_1_kappa_v2_1.py`; nada se heredó. |

**`F0-B`.** La línea de compuerta *«Códigos del codificador 2 adjuntos, transcritos sin edición»*
llegó **verbatim** y la tabla de 12 filas llegó **completa**, con notas por unidad. Se ingesta.

## 2 · Lo que se hizo

1. **Se abrió el sello de la Fase A.** Los cuatro `sha256` comprometidos el 25/ago —tabla de
   códigos, razonamiento, paquete, material de origen— **COINCIDEN** dígito por dígito.
2. **Se ingestó verbatim la codificación 2** de Jonatan Guadarrama (RANURA 1), con su `sha256`
   canónico en el commit. `diff` contra la codificación 1 en el mismo formato: **3 filas** — control
   que coincide con las 3 discrepancias que el `κ` encontró.
3. **`κ` de Cohen, dos niveles y dos universos.** Nivel 1 sobre las 12 = **`0.7209`** → el gate de
   `§3.4` aprueba. Nivel 2 = `0.6571`. Sobre 11 sin `U10`: `0.6901` y `0.6333`. Los cuatro del mismo
   lado de `0.60`.
4. **Consenso** sobre las 3 discrepancias, con ambas codificaciones a la vista y sin tercer
   codificador. Documentado unidad por unidad en `forense/hitoD-R10_1-corrida-v2_1.md §5`.
5. **Recuento, IC y rama.** `+P` 4/4 = `100.00 pp`; `−P` 1/3 = `33.33 pp`; diferencia `66.67 pp`;
   los dos IC cruzan 15 pp → rama 4 → **fila `C`**, con "no adjudica" bajo `A-bis`.
6. **Archivado** en el bloque append-only del preregistro con sus siete reservas, bajo la RANURA 2.
7. **Set de sincronía completo:** los **cuatro** sitios marcados `T20:HITO-D` re-derivados del
   Registro real (`README.md:36`, `canon/modelo-decision-v4_0.md:65`, `canon/estado-programa-v1_10.md:95`
   y `:280`), `ADR-205` en gobernanza, `L0` recifrado `204→205`, `FP-161` con `ejecutada_en`.

**Comando que re-deriva el contador** (misma lógica que el parser `_VEREDICTO_CANONICO` de
`tests/check.py`, que deduplica por regla — por eso `R4.3`, con dos emisiones, cuenta una vez):

```
python3 - <<'X'
import re
t=open('forense/hitoD-preregistro-v2_0.md',encoding='utf8').read()
b=t[re.search(r"^## Registro de veredictos archivados.*$",t,re.M).end():]
f={}
for l in b.split("\n"):
    m=re.search(r"`(R\d+\.\d+)`\s*→\s*veredicto\s*`([A-E])`",l)
    if m: f[m.group(1)]=m.group(2)
from collections import Counter
c=Counter(f.values())
print(len(f),"de 27 —","·".join(f"{c[k]}{k}" for k in "DBAEC" if c[k]))
X
```

→ `25 de 27 — 13D·4B·4A·2E·2C`.

**Comando que re-deriva el máximo de ADR** (por conteo entero, no por `sort -t- -k2`, que parte en
el primer guion y devuelve un máximo falso):

```
grep -o '^\*\*ADR-[0-9]\+' canon/gobernanza-v1_15.md | grep -o '[0-9]\+' | sort -n | tail -1   # 205
grep -c  '^\*\*ADR-[0-9]\+' canon/gobernanza-v1_15.md                                          # 205  → sin huecos
```

## 3 · Lo que vale la pena que quede escrito

**El desenlace estaba predicho, por escrito, antes de correr — y el techo empeoró.** `§5.1` de la
spec calculó `±56.58 pp` suponiendo `n=6` por brazo. La regla `2.5`, que es justo la pieza que
corrigió la **validez**, mandó fuera del denominador **cinco de las doce** unidades por no ser
rechazos consumados, y dejó los brazos en **4 y 3**. La corrección de validez costó potencia. `§5.2`
lo dijo antes: caer en rama 4/5 con este corpus *no* es falla de la spec, es su confirmación.

**El sello de la Fase A hizo el trabajo para el que existía.** Los tres desacuerdos que aparecieron
son exactamente los candidatos 1, 3 y 4 que el codificador 1 había nombrado por escrito **antes** de
que existiera la otra codificación. Y el único que movió el número lo movió **en contra** de quien
lo había codificado: `U02` pasó de rechazo indirecto en `+P` a `NO-RECHAZO`, reduciendo el
denominador del brazo cuya tasa favorece a la hipótesis. Un compromiso criptográfico que solo
confirma al que lo firmó no prueba nada; este no fue el caso.

**Wald degenera y se dijo.** Con `p̂(+P) = 1.00` el término Wald de ese brazo es exactamente cero, y
el IC Wald sale **más angosto que el propio techo declarado** — por artefacto, no por potencia.
Reportar solo Wald habría reportado una precisión inexistente. Se reporta también Newcombe, que no
degenera. Los dos cruzan el umbral: la rama no depende de cuál se prefiera.

**Cinco de doce no eran rechazos.** Es el hallazgo de validez que la Pieza 1 existía para producir:
la regla léxica de `COMMIT B` las contaba todas.

## 4 · Desviaciones y huecos, declarados

1. **`RANURA-TABLA` vacía.** El relanzamiento traía las doce filas del hueco en `___` y la tabla
   real **concatenada al final del mensaje**. `F0-B` se leyó satisfecha: la línea exigida estaba
   verbatim y la tabla existía completa, con notas por unidad que solo un codificador produce. **No**
   es el caso `FP-63` de autocaptura verbatim que hizo parar al `v2` en su primera redacción —
   allí no había dato ninguno; aquí lo hay y es inequívoco.
2. **La ranura de preguntas del codificador quedó sin llenar** por mesa (ni texto ni «ninguna»). No
   gatea nada. Se declara como hueco de procedencia; no se rellena por inferencia.
3. **Un archivo fuera de la lista cerrada del perímetro:** `tests/hitod_r10_1_kappa_v2_1.py`. Lo
   ordena el propio `B2` del encargo (*"extiende el patrón de `tests/hitod_r10_1_rechazo_poder.py`"*)
   y sin él las cifras no serían reproducibles. Se declara en vez de esconderse.
4. **Campo `gatea` de `FP-161` quedó con una cifra vieja** (*"el contador del Hito D sigue en 20 de
   27"*, escrito el 25/ago, cuando ya iba en 24). **No se corrige**: es texto de creación de la fila,
   y reescribirlo sería reescribir el registro de lo que se pidió. Se señala aquí.
5. **`canon/modelo-decision-v4_0.md`** no tenía ninguna cita viva del *veredicto* de `R10.1` — su
   única mención (`:772`) es la fila del registro de IDs, que declara tier `[FUERTE]` y "tiene ficha:
   Sí", y una fila `C` no mueve el tier. Lo que sí se actualizó ahí es el contador marcado
   `T20:HITO-D` de `:65` y su lista de veredictos. Negativo verificado con
   `grep -n "R10\.1" canon/modelo-decision-v4_0.md` → 2 líneas, ambas revisadas.

## 5 · Lo que este acto NO hizo

No adjudicó nada fuera de la escala `§6`. No tocó `PRESEEA`. No editó la spec ni los tres documentos
`v1` de `R10.1` (append-only, `ADR-40`). No sustituyó al segundo codificador humano por una IA —la
spec dice persona, y dos LLMs comparten formación: el `κ` dejaría de medir independencia. **No corrió
dos veces:** el primer resultado que produjo el procedimiento es el que se reporta.

**Lo que queda abierto:** adjudicar `R10.1` de fondo —llevarla a `A` o `B` con un IC que no cruce 15
pp— exige **más rechazos mexicanos con los dos brazos de poder**, no una mejor codificación de los
mismos 12. La candidata nombrada por `§5.3` es `PRESEEA`, `NO-ACCESIBLE` desde `CONF-17`
(5/ago/2026), heredada sin re-verificar y **no reabierta aquí**.
