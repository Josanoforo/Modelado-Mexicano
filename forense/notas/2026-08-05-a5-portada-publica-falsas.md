Contadores movidos: 0. (Este acto es de portada pública — README/AVISO/USO-ACEPTABLE/AUTHORSHIP —, no de evidencia. No toca Hito D, condicionales, coeficientes ni ningún contador del motor.)

# ENCARGO A5 · La portada pública afirma cosas falsas sobre el propio programa

*5 de agosto de 2026 (huso local del repo, UTC-6 — ADR-59).* Ejecutor: sesión en
la nube (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, correcto para
entorno de nube por ADR-59(b); sonda saltada — este acto no abre microdato ni
red), rama `claude/portada-publica-falsas-9nsslw`, clon existente en
`/home/user/Modelado-Mexicano`.

## 0 · Arranque

- **Repo.** Clon existente reutilizado, no se clonó uno nuevo. `git log -1`
  al abrir: `3de5a28 Merge pull request #124 from
  Josanoforo/claude/sellar-conf06-adr64-ygbaqx`. `git status`: árbol limpio,
  sobre la rama designada.
- **SHA de referencia.** El encargo cita `a7f807e` (PR #125) como `main`.
  `main` se movió una vez más desde entonces: `origin/main` está hoy en
  `3de5a28` (PR #124, "ENCARGO M-5: sella conf.06 con ADR-64"), y la rama de
  este acto ya nace exactamente en ese commit — `git merge-base origin/main
  HEAD` = `3de5a28` = `HEAD`. No es PARO (el encargo ya lo anticipa). Diff
  `a7f807e..HEAD` toca solo `canon/*` y `forense/*` (el trabajo de PR #124);
  verificado con `git diff --stat a7f807e HEAD -- README.md
  AVISO-DE-ALCANCE.md USO-ACEPTABLE.md AUTHORSHIP.md` que los cuatro
  archivos de este acto **no cambiaron** entre `a7f807e` y el HEAD de
  partida — las líneas que cita el encargo (`README:45,85`,
  `AVISO:102`, `USO-ACEPTABLE:84`, `AUTHORSHIP:71-72`) siguen exactas.
- **`data/raw`.** Ausente. No es PARO — este acto no abre microdato, solo lee
  `data/manifiesto.yaml` (metadatos, no payload).
- **Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` —
  correcto para nube (ADR-59(b)). Sonda de red: saltada, no aplica.
- **Espejo.** No se usó. Toda cifra de este acto sale del clon de arriba,
  con el comando a la vista (tabla abajo).
- **Concurrencia.** `git branch -r` → solo `origin/main` y
  `origin/claude/portada-publica-falsas-9nsslw`. `gh pr list --state open`
  (vía MCP `list_pull_requests`) → **ninguna PR abierta** al momento de
  arrancar. `CORRIDA-IDG3` (Ubuntu) no comparte archivo con este acto salvo
  `forense/hallazgos.md` (`merge=union`, apéndice de una sola línea, sin
  riesgo de conflicto real).

## 1 · Premisas — verificadas, no aceptadas por cita

1. **La afirmación falsa está viva en las cuatro.** Confirmado por lectura
   directa: `README.md:45` y `:85`, `AVISO-DE-ALCANCE.md:102` (dentro del
   bloque `## Bloque para insertar en README.md`), `USO-ACEPTABLE.md:84`,
   `AUTHORSHIP.md:71-72`. Los enunciados relacionados que "quedan cortos"
   también están donde el encargo dice: `AVISO:12`, `USO-ACEPTABLE:25`,
   `AUTHORSHIP:84`.
2. **`AUTHORSHIP.md:67` decía "43 decisiones de arquitectura".** Receta de
   T15 corrida en este acto: `grep -oE '^\*\*ADR-[0-9]+'
   canon/gobernanza-v*.md | grep -oE '[0-9]+' | sort -n -u | wc -l` → **64**,
   sin huecos (máximo también 64). T15 solo escanea `canon/*.md` — verificado
   leyendo `t15_adr_count()` (`tests/check.py:461-482`): el glob es
   `os.path.join(ROOT, "canon", "*.md")`, no la raíz. Los cuatro archivos de
   este acto viven en la raíz — invisibles para T15.
3. **`USO-ACEPTABLE.md:16` citaba `canon/modelo-decision-v3_3.md`.** No
   existe — el vigente es `modelo-decision-v4_0.md`. Verificado
   `t03_dangling_refs()` (`tests/check.py:185-201`): la clase de carácter
   del regex de nombre de archivo es
   `[A-Za-z0-9_\-áéíóúñÁÉÍÓÚÑ.]+\.(?:md|yaml)`, sin `/` — una ruta con `/`
   entre backticks no coincide con el patrón completo y el test nunca la ve.
4. **`README.md` ya está mayormente bien.** Confirmado: no se tocó nada de
   README salvo las dos líneas de la afirmación falsa (`:45`, `:85`); el
   resto de sus 6 recetas derivadas en comentario HTML (líneas 34/36/37/38/39
   y ahora 45) se dejó como estaba o se extendió con la misma disciplina.

## 2 · El enunciado corregido — las tres partes, con receta

Aplicado, con variantes de longitud según el hueco de cada archivo, en las
cuatro ubicaciones:

> **Sí hay dato primario propio:** 223 payloads con `sha256` en
> `data/manifiesto.yaml` <!-- `grep -cE '^\s*sha256:' data/manifiesto.yaml`
> --> y estimandos propios sobre ENVIPE, ENCIG, ENCUCI, ENIF y ENIGH
> (verificado en `milpa/procedencia.yaml`: entradas `fuente:` con esas cinco
> siglas y `clase: MEDIDO...`; y en `forense/notas/2026-07-31-p1-enigh-semilla.md`
> / `forense/notas/2026-08-04-hitoD-r5-1-pension-bienestar.md` para ENIGH).
> El estimador (`tests/svystat.py`) está respaldado contra tres casos de
> referencia (Encargo E-3, PR #97 — caso sintético, reproducción Hito D
> R7.2 sobre ocho olas de ENVIPE, reproducción CAL-CONF Fase B ola 2 sobre
> ENVIPE+ENCUCI) y validado contra cifras publicadas de INEGI en al menos
> dos actos: Encargo K (`forense/notas/2026-08-04-medicion-exposicion-violencia-envipe.md`
> — ENVIPE 2025, violación sexual, reproduce 279.3 contra 279 publicado por
> cada 100 mil mujeres, 0.09% de diferencia) y Encargo P /
> `forense/hitoD-preregistro-v2_0.md:888` (`forense/notas/2026-08-04-hitoD-r5-1-pension-bienestar.md`
> — ENIGH 2022, Comunicado de Prensa INEGI 420/23: total de hogares
> 37,560,123, `bene_gob` $1,777, `donativos` $1,271, `jubilacion` $5,169,
> las cuatro reproducidas a 3 decimales o mejor).
>
> **El modelo en sí sigue mayormente sin medir:** `4 de 144` <!--
> `modelo §6.1`; `forense/hallazgos.md`, 31/jul/2026, "Congelamiento de
> `4 de 144`" — decisión de mesa, congelado, no se recalcula --> · `0 de 15`
> coeficientes en escala del modelo — los tres β̂ que existen son
> asociaciones marginales, rotuladas así por ADR-57(a), no coeficientes:
> ninguna sobrevive condicionar, y ningún ADR de D-ABC ha sellado función
> de enlace (`milpa/procedencia.yaml:780`).
>
> **La mayoría de las 49 reglas sigue descansando en síntesis de
> literatura:** **36 de 49** <!-- receta de `README.md:89`: `49`
> (`python3 tests/validador_registro_ids.py`) `− 13` (fichas del bloque
> append-only `## Registro de veredictos archivados` de
> `hitoD-preregistro-v2_0.md`, `_VEREDICTO_CANONICO`, mismo parser que T18)
> `= 36` --> reglas sin corrida de falsación pre-registrada. Re-derivado en
> este acto, hoy: `grep -oE '\`R[0-9]+\.[0-9]+\`\s*→\s*veredicto\s*\`[A-E]\`'
> forense/hitoD-preregistro-v2_0.md | sort -u | wc -l` → 13 fichas únicas;
> `49 − 13 = 36`. Coincide con `README.md:89` — sin cambio desde que se
> escribió.

`README.md:85` (S1, en "Deudas abiertas") lleva la versión corta de lo
mismo, con `PD-01` separado y sin tocar — eran dos deudas empaquetadas en
una línea, S1 (la afirmación falsa) y PD-01 (14 descartes irrecuperables,
cierto, no se toca).

## 3 · Barrido completo

| Archivo:línea | Cifra vieja | Cifra derivada | Receta | Resultado |
|---|---|---|---|---|
| `README.md:45` | "Cero datos primarios propios — deuda S1" | 223 payloads + estimandos propios + estimador validado | `grep -cE '^\s*sha256:' data/manifiesto.yaml` = 223; E-3/PR#97; Encargo K/P | **Corregido** |
| `README.md:85` | "S1 · Cero datos primarios propios" | ídem, PD-01 separado y conservado | ídem | **Corregido** |
| `AVISO-DE-ALCANCE.md:13` | "31 reports... 49 reglas" (sin receta) | 31 / 49, sin cambio | `ls corpus/reports/*.md \| wc -l` = 31; `python3 tests/validador_registro_ids.py` = 49 | **Corregido** (receta añadida, cifra sin cambio) |
| `AVISO-DE-ALCANCE.md:25-32` | "144/4/15" (sin receta) | sin cambio | `modelo §6.1`; `modelo §2.2`; `milpa/procedencia.yaml` | **Corregido** (receta añadida) |
| `AVISO-DE-ALCANCE.md:60-62` | "ocho lugares" (sin receta) | 8, sin cambio hoy | `python3 tests/check.py` → T09 = 8 fail | **Corregido** (receta añadida) |
| `AVISO-DE-ALCANCE.md:75-78` | "siete/doce/siete/siete" (sin receta) | 7/12/7/7, sin cambio hoy | `python3 tests/check.py` → T06 (2 avisos: Gini=7, confianza=12) / T07=7 / T08=7 | **Corregido** (receta añadida) |
| `AVISO-DE-ALCANCE.md:102` (bloque para README) | "sin datos primarios propios" | enunciado de tres partes | ver §2 | **Corregido** |
| `USO-ACEPTABLE.md:16` | `canon/modelo-decision-v3_3.md` (colgante) | `modelo §3.B` (nombre estable) | cabecera de `canon/modelo-decision-v4_0.md`: "NOMBRE ESTABLE — modelo, cítalo así" | **Corregido** |
| `USO-ACEPTABLE.md:16` | "49 reglas" (sin receta) | sin cambio | `python3 tests/validador_registro_ids.py` | **Corregido** (receta añadida) |
| `USO-ACEPTABLE.md:22-25` | "144/4/15" (sin receta) | sin cambio | `modelo §6.1`; `modelo §2.2`; `procedencia.yaml` | **Corregido** (receta añadida) |
| `USO-ACEPTABLE.md:84` | "Cero datos primarios propios." | enunciado de tres partes | ver §2 | **Corregido** |
| `AUTHORSHIP.md:67` | "43 decisiones de arquitectura" | **64** | `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v*.md \| grep -oE '[0-9]+' \| sort -n \| tail -1` | **Corregido** |
| `AUTHORSHIP.md:71-72` | "Datos primarios propios: todo es síntesis..." | enunciado de tres partes | ver §2 | **Corregido** |
| `README.md:50-79` | "18 FAIL · 110 WARN" (corrida del 28/jul) | — | — | **Conservado como historia** (encabezado fechado, política de `estado-programa:69`) |
| `AUTHORSHIP.md:30-39` | tabla de commits (HEAD `c3adff8`, 30/jul/2026) | — | — | **Conservado como historia** (encabezado fechado) |
| `USO-ACEPTABLE.md:25` | "síntesis de literatura con estructura de modelo. No es un instrumento validado." | — | — | **Reportado, no tocado** (§4, candidato a adjudicar qué es el programa) |
| `AVISO-DE-ALCANCE.md:12` | descripción de "qué es esto" sin mencionar dato propio | — | — | **Reportado, no tocado** (misma clase que `USO-ACEPTABLE:25`) |
| `AUTHORSHIP.md:84` | "síntesis de literatura con un aparato de auditoría..." | — | — | **Reportado, no tocado** (misma clase) |
| `canon/estado-programa-v1_10.md:105-108` (§4·S1) | "Cero datos primarios propios. Deuda del programa, no de ningún report." | — | — | **Reportado, no tocado** (fuera de perímetro — ver §4 abajo) |
| `canon/glosario-v5_6.md:417` | "Cero datos primarios propios — deuda del programa, no de ningún report." | — | — | **Reportado, no tocado** (fuera de perímetro, mismo hallazgo) |

## 4 · Hallazgo no pedido: la afirmación falsa también sigue viva en canon — y ya estaba declarada caducada

No lo pidió el encargo, pero apareció leyendo `canon/estado-programa-v1_10.md`
para verificar contra qué severidad citaba README su "S1": la deuda `§4·S1`
del propio canon (línea 105-106) sigue diciendo hoy, textual, **"Cero datos
primarios propios. Deuda del programa, no de ningún report."** — la misma
afirmación que este acto corrige en los cuatro archivos de la raíz.
`canon/glosario-v5_6.md:417` repite la misma línea casi verbatim.

Lo que hace esto más que una simple inconsistencia: `canon/gobernanza-v1_15.md:340`
(ADR-44(b), 29-30/jul/2026, cuando el repo se hizo público) **ya declaró esta
deuda "caducada por completo"** — junto con las ocho refutaciones sin objeto
y el baseline de la autodeclaración falsa de `hitoD-preregistro:8` — como una
de las tres deudas que la función pública del repositorio volvió obsoletas.
Es decir: la mesa ya decidió esto hace más de una semana. La decisión nunca
se propagó a `estado §4·S1` ni a `glosario:417`, que siguen listándola como
"Grande, sin resolver". Este acto **no lo corrige** — `canon/` está fuera de
perímetro — pero lo deja registrado: cerrar `§4·S1` formalmente en canon
(retirar la entrada o reescribirla con la cifra real) es trabajo de mesa,
con su propio ADR si hace falta, no una limpieza de portada.

## 5 · Respuestas a §4 del encargo

**¿Extender T19c/T20 a los cuatro archivos de la raíz?** No se implementa
aquí (decisión de mesa), pero el argumento, leído el código de ambos:

- `T19c` (`tests/check.py:875-937`) ya asume una estructura fija: busca una
  sección `## Estado del modelo` en `README.md` y cruza tres cifras
  puntuales (corridas de Hito D, condicionales medidas, coeficientes en
  escala) contra su fuente. Los otros tres archivos no tienen esa sección ni
  esa forma — extenderlo exigiría, como mínimo, generalizar el parser de
  "sección con forma conocida" a "prosa libre con cifra en contexto", que es
  un test distinto, no una extensión.
- `T20` (`tests/check.py:1006-1045`) es aún más angosto: solo vigila el
  marcador literal `<!-- T20:HITO-D pob=reglas -->` sobre `README.md` +
  `canon/*.md`, y solo sabe verificar la población `reglas` del contador
  "N de 27" de Hito D. Ninguna de las cifras que este acto tocó (payloads,
  ADR, reports, 36/49) es esa población — T20 no las cubre aunque se
  extendiera su alcance de archivos.
- **Lo que el defecto de hoy habría necesitado** no es ninguno de los dos:
  era una cifra *ausente de receta* (43 ADR, sin comentario) y una
  *afirmación falsa en prosa libre* (cero dato primario), no una cifra
  *desincronizada de una fuente numérica única* como T19c/T20 vigilan. Un
  test que lo hubiera atrapado tendría que parsear prosa de cuatro
  documentos con estructura distinta cada uno y decidir qué frases son
  "afirmaciones de estado" — mucho más cerca de T11 (cuantificador
  absoluto) que de T19c/T20.
- **El patrón de receta-en-comentario ya reduce la necesidad**, pero no la
  elimina: una receta en comentario le dice al lector humano cómo verificar
  — no hace que la suite falle si la cifra en prosa se desincroniza de su
  receta. Es exactamente el límite que `README.md` ya tiene hoy (sus 6
  cifras con receta tampoco están vigiladas por ningún test que las
  recompute y compare) y que ADR-44(c) dejó abierto como F6, "PENDIENTE".
  **Conclusión: vale la pena, pero es una sesión de tests aparte** —
  construir el parser de prosa-a-cifra para cuatro documentos de forma
  distinta no es gratis, y el costo lo paga quien lo escriba, no quien lo
  pide.

**¿Queda algún enunciado que no se pudo corregir sin adjudicar?** Sí, tres,
mismo tipo que `USO-ACEPTABLE.md:25` (ya señalado por el encargo):
`AVISO-DE-ALCANCE.md:12` y `AUTHORSHIP.md:84`. Los tres describen "qué es
el programa" en una frase (`"síntesis de literatura con estructura de
modelo"`, `"síntesis de literatura...con un aparato de auditoría
inusualmente explícito"`) que, con seis estimandos ya medidos y un
estimador validado, ya no es del todo exacta — pero afinarla exige decidir
si el programa se autodescribe como "síntesis con un poco de medición
propia" o algo con otro nombre, y eso es exactamente la clase de juicio que
este acto tiene instrucción explícita de no tomar. **Reportados, no
tocados**, en la tabla de arriba.

## 6 · Lo que no se hizo

- No se tocó `canon/`, `milpa/`, `tests/` ni `data/` — incluida la
  contradicción de §4 arriba, que se reporta y no se corrige.
- No se re-escribió ningún registro fechado (`README.md:50-79`,
  `AUTHORSHIP.md:30-39`).
- No se selló ningún ADR.
- No se declaró el modelo validado — el enunciado corregido sostiene las
  tres partes a la vez (dato propio sí existe; modelo sigue sin medir;
  mayoría de reglas sin falsar) precisamente para no caer en el extremo
  contrario.

## 7 · Suite

`python3 tests/check.py --baseline`, corrido tras confirmar cero
marcadores de conflicto (`grep -rn '<<<<<<<' .` solo encuentra el string
citado dentro de este mismo tipo de nota, nunca un marcador real): ver
salida completa en el reporte de cierre de esta sesión.
