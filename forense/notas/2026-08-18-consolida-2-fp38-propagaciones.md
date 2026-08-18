# ACTO CONSOLIDA-2 (v2) — `FP-38` ejecutada, tres propagaciones de `CONSOLIDA-17AGO` cerradas, fila abierta para el corte de edad

**Acto:** CONSOLIDA-2 (v2) · **Encargo:** `forense/encargos/2026-08-18-CONSOLIDA-2.md` (archivado verbatim por A.3, este PR) · **Entorno:** NUBE, repo-only, sin `data/raw` · **SHA de redacción del encargo:** `68a3466` (`origin/main`, merge #257).

**Contadores de medición sobre México movidos por este acto: cero — `13 de 27` · `0 de 15` · `1 de 2` intactos.** Lo que este acto mueve es la honestidad de un tier, no una medición.

---

## §0 · ARRANQUE

```
$ pwd && git rev-parse --is-shallow-repository && git branch --show-current && git status
/home/user/Modelado-Mexicano
true
claude/encargo-acto-consolida-2-v2-edbp2h
On branch claude/encargo-acto-consolida-2-v2-edbp2h
nothing to commit, working tree clean
$ git log -1 --format="%h %s"
68a3466 Merge pull request #257 from Josanoforo/claude/new-session-yzskdx
```

Clon superficial detectado. `git fetch --unshallow origin`:

```
From https://github.com/Josanoforo/Modelado-Mexicano
 * [new branch]      gate-durable-v7 -> origin/gate-durable-v7
 + f8eb2e3...68a3466 main            -> origin/main  (forced update)
$ git rev-parse --is-shallow-repository
false
$ git log -1 --format="%H %s" origin/main
68a34668a87575183004e8ebe6ce0e5831e71610 Merge pull request #257 from Josanoforo/claude/new-session-yzskdx
$ git merge-base --is-ancestor origin/main HEAD && echo "HEAD contains origin/main"
HEAD contains origin/main
```

**`main` no se movió más allá de `68a3466`.** SHA del encargo confirmado exacto — no hace falta re-derivar por deriva de rama, aunque cada premisa se re-verificó por contenido de todos modos (§1).

**3 · `data/raw`.** Ausente, confirmado, no es paro:

```
$ test -d data/raw && echo EXISTS || echo ABSENT
ABSENT
```

**4 · ENTORNO (A.2, tres partes):**

```
$ echo "[${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}]"
[cloud_default]
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
000
$ ls data/raw/ 2>/dev/null | head -1
(vacío — el directorio no existe)
```

`cloud_default` es firma correcta de un acto de nube. `000` es la allowlist de esta caja (A.5), no INEGI caído — no se reintenta, no se investiga más: el acto no usa `data/raw` ni red externa.

**5 · ESPEJO.** Ninguna cifra de esta nota viene de memoria; cada una lleva su comando arriba o en la sección correspondiente.

---

## §1 · Verificación de existencia — re-derivada contra `68a3466`, no heredada del encargo

| Ítem | Comando / lectura | Resultado |
|---|---|---|
| `glosario:136` (a)+(c), Fuerte, Velandia-Morales única cita | `Read canon/glosario-v5_6.md` líneas 120-149 | **EXISTE-NO-SATISFACE, confirmado**: `\| **Consumo compensatorio · estatus** \| **Fuerte** \| (a)+(c) \| ... Velandia-Morales 2022 (base latinoamericana) ...` |
| `glosario:137` (a)+(c), Hipótesis razonable | ídem | **EXISTE-NO-SATISFACE (sin examinar), confirmado** |
| Firma de mesa verbatim | `Read forense/encargos/2026-08-17-CONSOLIDA-17AGO.md` §PARTE 2 | **EXISTE-SATISFACE**: cita *"El expediente de F38, el experimento no aplica, no es México."* y el texto adoptado en blockquote, ambos verbatim en el archivo |
| `recovery-plan:65` | `grep -n -C2 ENIGH forense/recovery-plan-v1_0.md` | **EXISTE-SATISFACE**: `\| R1.4 \| consumo compensatorio por decil \| **ENIGH** · 6 olas \|` |
| `conf.01` resuelta | `Read canon/glosario-v5_6.md` líneas 305-324 | **EXISTE-SATISFACE, en `:316`** (no `:315` — el desfase de una línea que el propio encargo advierte es real y se verificó por contenido): `✅ **Resuelto por precedencia**: segmentado — A/B/C+ sí, D/E no` |
| `milpa/refutations.yaml` conf.01 | `Read` líneas 85-139 | **EXISTE-SATISFACE**: `conf.01.calidad_vs_precio` en `:94`, `entra: false` en `:112`, texto en modo `resolucion_propuesta` |
| `hitoD-preregistro` R1.4 | `Read forense/hitoD-preregistro-v2_0.md` líneas 50-69, 870-914 | **EXISTE**: `:59-60` trae el título sin rama (`[FUERTE como correlación]`, sin "estatus"); el bloque append-only vive al final del archivo (`## Registro de veredictos archivados`, tras la última nota narrativa), con el mecanismo de nota fechada declarado explícitamente en cada nota previa (ej. Nota 16: *"El veredicto archivado ... no cambian por esta nota. Si mesa decide adjudicar A, se registra como entrada nueva fechada en el bloque de abajo."*) |
| Fila del corte de edad | `grep -c "corte de edad" forense/firmas-pendientes.tsv` | **NO-ENCONTRADO, confirmado**: `0` |
| Sitios del corte en el modelo | ver §4 — receta validada con control positivo y negativo, **9 sitios**, no 6 (v1) ni heredado del "mi 9" de la v2 | **9, derivado, no heredado** |
| `estado-programa:136-137` | `Read canon/estado-programa-v1_10.md` líneas 93-102, y el bloque §S5 (~:136-137) | **YA EJECUTADAS**: `:136`→ *"conf.02 ✅ Resuelto por ADR-94, 18/ago/2026..."*, `:137` → *"conf.05 ✅ Resuelto por ADR-94, 18/ago/2026..."* — verificado por contenido, `MESA-18AGO`/`ADR-101(l)` ya las ejecutó. Fuera de este acto, confirmado, no tocado. |

Todas las premisas del encargo se sostienen. Ninguna obligó a un `PARA`.

---

## §2 · COMMIT 1 — `FP-38`: `glosario:136` pierde sostén de `(a)`

**1.1 Re-verificación de las dos premisas** — hecha en §1: `glosario:136` sigue `(a)+(c)`, `recovery-plan:65` sigue ENIGH·6 olas. No hay `PARA`.

**1.2 · `glosario:136`.** Procedencia `(a)+(c)` → `(c)`. El tier `Fuerte` se marca `⚠️ sin sostén por procedencia` — no se sustituye por otro tier, tal como el texto adoptado exige. Se preserva íntegro el resto de la celda (desenlace, mecanismo, la nota de partición por ADR-94, el comentario sobre V1 y el perfil 5): la corrección es de procedencia, no de análisis.

**1.3 · `glosario:137`, examen entregado.** La celda cita `Health, Body, Food:35` — **no** Velandia-Morales — como base. Verificado el contenido de esa fuente (`corpus/reports/Health__Body__Food_and_Substance_Use_in_Mexico...md`, hallazgo 14): describe la persistencia de refresco/botana en **hogares de bajo ingreso** (patrón de consumo mexicano, bien establecido en otras partes del corpus vía ENSANUT/ENIGH) interpretado con el marco de "recompensa asequible" — y el propio report ya declara *"poca medición directa"* para el mecanismo causal, razón por la que el tier ya es `Hipótesis razonable`, no `Fuerte`. La cita de `BENCHMARK-conf05-consumo-compensatorio-2026-08-17.md:72` (el acto que partió el constructo) confirma que nadie ha objetado esta celda: *"Su propio report ya declara 'poca medición directa' y eso es correcto."*

**Conclusión: `(a)+(c)` de `:137` tiene sostén propio, distinto del arrastre de `:136`.** El defecto de `:136` era específico — una cita puntual (Velandia-Morales, CIMCYC/Granada) pasada como dato mexicano cuando es un experimento español con resultado nulo. `:137` no repite esa cita ni ese error: su `(a)` describe un patrón de consumo mexicano real (aunque la interpretación causal sea, por diseño, una hipótesis débil ya reconocida como tal). No se toca.

**1.4 · Propagación a los cuatro sitios del lector**, mismo criterio (marca de procedencia rota, no re-análisis), sin reescribir el argumento de cada sitio:

- `integrador-psicologia-mexicano.md:36` (patrón 8, "la ironía maestra")
- `integrador-psicologia-mexicano.md:204` (Patrón 7, "Evidencia a favor")
- `corpus/reports/Psicología_del_Consumidor_Mexicano...md:64` (tabla de evidencia, mismo patrón que la fila 66 ya usaba para el defecto de Hofstede/ADR-06)
- `corpus/reports/Psicología_del_Consumidor_Mexicano...md:84` (prosa de "Fuerza 4")

**1.5 · Falsador, registrado sin ejecutar.** `R1.4` ↔ ENIGH 6 olas queda anotado en `glosario:136` (dentro del texto adoptado copiado verbatim) como la ruta que devolvería el tier: una medición mexicana representativa que ligue desigualdad con gasto en bienes posicionales por decil.

**Tablero.** `FP-38`: `ABIERTA` → `FIRMADA`. `firmada_en` cita la mesa del 17/ago verbatim (`CONSOLIDA-17AGO §PARTE 2`) más el texto adoptado íntegro. `ejecutada_en` queda `N/A` hasta el commit de cierre (mismo patrón que `FP-43` mostraba antes de este acto: `FIRMADA` con `ejecutada_en` vacío es un estado válido intermedio).

---

## §3 · COMMIT 2 — las tres propagaciones pendientes de `CONSOLIDA-17AGO`

Las tres son propagación de decisiones ya resueltas por otros actos. Ninguna obligó a adjudicar nada nuevo — verificado antes de cada una.

**(b) `milpa/refutations.yaml`, `conf.01.calidad_vs_precio`.** Verificado primero (§1): `glosario:316` sigue diciendo *"Resuelto por precedencia: segmentado — A/B/C+ sí, D/E no."* El yaml seguía con `entra: false` y `resolucion_propuesta` en modo propuesta — exactamente el desfase de propagación que `CONSOLIDA-17AGO` había encontrado (contra `glosario:315` en ese momento) y nunca llegó a escribir porque `PR #250` cortó el acto a medio plan. `resolucion_propuesta` se conserva verbatim (evidencia de que el motor ya lo había anticipado); se añade `resolucion_adoptada` citando `glosario:316`; `entra` pasa de `false` al string `"segmentado -- A/B/C+ sí, D/E no"`, mismo estilo no-booleano que ya usa `conf.02.policronia`.

**(c) `glosario:399`** (era `:398` en `CONSOLIDA-17AGO` contra `d0019a2` — el desfase de una línea que el propio acto de hoy advierte). Contra `68a3466`, la lista *"conf.02, conf.05, conf.07 — sin ADR"* ya no refleja el estado real: `glosario:317` y `:320` (§11, Conflictos abiertos) declaran ambos `✅ Resuelto por ADR-94, 18/ago/2026`. `conf.02` sale de la lista (`conf.02 ya la resolvió ADR-92(d)`/`ADR-94`, per el encargo — verificado contra el propio texto de `glosario:317`, que hoy cita `ADR-94`, y contra `estado-programa:136` §S5, que también lo confirma). `conf.05` sale por la misma vía (`ADR-94`, `estado-programa:137`). `conf.07` se queda: sigue `⚠️ Abierto` en `glosario:323`, sin ADR, y tiene acto propio gateado a éste (`CONF-07-CIERRE`, comparte `glosario`, se lanza cuando este PR fusione) — no se le adelanta ningún sello, tal como el encargo exige.

**(d) `hitoD-preregistro`, `R1.4`.** El archivo es registro maestro de falsación, append-only por `gobernanza` `ADR-40`; su propio cuerpo (ej. Nota 16, Nota 18) declara el mecanismo: una nota fechada al final, nunca una edición de cuerpo. Se añadió **Nota 30 · 18/ago/2026**, siguiendo exactamente esa disciplina, declarando: (i) que `R1.4` (`:59-60`) consume la rama `consumo_compensatorio.estatus` de `conf.05` — no la rama `recompensa` —, con el título/regla ya redactados por `FP-43` (`forense/notas/2026-08-17-cierra.md` §6) citados sin editar el cuerpo; (ii) que esa rama acaba de perder su sostén de tier en este mismo PR (`FP-38`, §2 arriba). **No se tocó el veredicto archivado ni el contador `13 de 27`** — verificado tras el commit: el bloque `## Registro de veredictos archivados` no ganó ninguna línea nueva, y la Nota 30 lo dice expresamente. Esto cierra `FP-43`: `ejecutada_en` cita la Nota 30; el número de PR se añade en el commit de cierre.

**Lo que `CONSOLIDA-17AGO` deja vivo — no ejecutado aquí, dicho para que no se pierda otra vez:** su `PARTE 3` (el barrido de las 212 notas de `forense/notas/` + `hallazgos.md` + `modelo-decision` + `milpa/*.yaml`, con el triaje `YA RESUELTO`/`FILA`/`SOLO ANOTADO`) y su `PARTE 4` (el ADR que sella `firmas-pendientes.tsv` como único lugar de un pendiente). Ninguna de las dos se tocó — no estaban en el perímetro de este acto.

---

## §4 · COMMIT 3 — el corte de edad: fila, no resolución

**Receta, probada contra los dos controles antes de reportar cifra.** El patrón ancho `corte` (case-insensitive) sobre `canon/modelo-decision-v4_0.md` da 15 líneas — 7 de ellas falsos positivos: `:181` (prosa general, "cortes explícitamente marcados"), `:234` (X-02, "no hay corte de atributos" — sobre el perfil 3, no sobre edad), `:259` (prosa general sobre qué ejes sí tienen partición canónica), `:554` (límite de confianza interpersonal, "a ese corte"), `:698`/`:700` (tabla de reglas L343, columnas ajenas a "PENDIENTE"), `:835` ("no hay corte publicado" sobre regiones de atributos, no sobre edad). Exactamente los 7 que el encargo anticipa por el precedente de `"cortes iniciales"` (`FP-02`).

```
$ grep -n "corte PENDIENTE" canon/modelo-decision-v4_0.md
189, 215, 219, 457, 482
$ grep -n 'Corte de `edad` PENDIENTE' canon/modelo-decision-v4_0.md
355, 357, 361
$ grep -cE "corte PENDIENTE|Corte de \`edad\` PENDIENTE" canon/modelo-decision-v4_0.md
9
$ grep -n "cortes iniciales" canon/modelo-decision-v4_0.md
(vacío — control negativo limpio en este archivo)
```

**9 sitios, confirmados, clasificados** (criterio propio, declarado — no hay una lista de mesa previa más allá de los dos ejemplos que el encargo ya nombra):

- **Regla operativa** (SI-ENTONCES viva del motor): `:457` (`R2.4`, `trabajo.rotacion.joven_urbano_sin_culpa`), `:482` (`R5.4`, `familia.cortejo.urbano_joven_apps`).
- **Hipótesis** (fila del bloque de hipótesis, §2 del modelo): `:215` (`H-02`), `:219` (`H-06`), `:220` (`H-07` — parcialmente resuelta por proxy C-bis, pero *"no comprobable hoy contra este corte de edad"* sigue vigente en su propio texto).
- **Descriptor**: `:189` (definición del perfil 5, "Joven Gen Z urbano conectado") y las tres filas de la tabla de traducción perfil→atributos (`:355` `R1.4`, `:357` `R2.4`, `:361` `R5.4`) — auditan/registran el estado de migración de cada regla, no afirman ni disparan nada por sí mismas.

**Fila abierta.** `FP-53`, `ABIERTA`, con la pregunta de mesa redactada, los 9 sitios citados y clasificados en `dónde`, la evidencia de `modelo:809` (*"un umbral de 'joven' que ningún inventario fija"*) en `qué_se_firma`, y la cita **D-10 de `ADR-101`** (*"démosle fila"*) como firma de origen — no como decisión nueva: la disposición de mesa que autoriza abrir esta fila ya está registrada, esta fila la consume, no la vuelve a pedir. No se definió el corte: exige dato mexicano propio (P1, partición canónica de `edad`) y es acto por sí mismo.

---

## §5 · Módulo de auditoría — este acto sí afirma sobre México

**¿Qué parte está sesgada por marcos extranjeros?** El hallazgo mismo: `glosario:136` marcaba `Fuerte` una celda sobre consumo compensatorio en México sostenida por un solo estudio, y ese estudio es un experimento de laboratorio español (CIMCYC, Universidad de Granada) con resultado nulo declarado adentro. **¿Caso aislado o síntoma?** Aislado, con esta evidencia — `:137` (misma familia de constructo, mismo acto de partición) se examinó expresamente y **no** repite el defecto: su base es un report con alcance mexicano declarado, no una cita mal atribuida. No se generaliza el hallazgo a "todo el dominio de consumo compensatorio está mal citado" porque eso no es lo que este examen encontró — sería la misma clase de sobre-generalización que el propio corpus ya nombra como riesgo (`meta-auditoria-comunicacion.md`). Si aparece un tercer caso en el futuro, ahí sí sería patrón; con dos casos y una sola instancia del defecto, se declara aislado.

**¿Qué conclusión sería peligrosa simplificada?** Bajar el tier de `Fuerte` a `Fuerte ⚠️ sin sostén por procedencia` **no dice que el consumo compensatorio por estatus no exista en México** — dice que la única cita que lo sostenía como "fuerte" no es evidencia sobre población mexicana. La diferencia importa: el mecanismo (desigualdad → señalización de estatus vía consumo) sigue siendo teóricamente plausible y consistente con el resto del corpus (identidad de clase media, colorismo, movilidad estancada); lo que falta es la medición mexicana directa, y el falsador que la traería (`R1.4`/ENIGH 6 olas) ya está identificado y en disco, sin ejecutar.

**¿Qué afirmación describe el estado del corpus escrita a mano?** Ninguna. Los 9 sitios del corte de edad se derivaron por comando con control positivo y negativo (arriba). Los conteos de "sale de la lista `sin ADR`" se verificaron leyendo `glosario:317`/`:320` directamente, no de memoria.

**¿Cuántos contadores movió?** Cero, en `13 de 27` (Hito D — `hitoD-preregistro` no ganó veredicto nuevo, solo una nota) · `0 de 15` (coeficientes de generador — no tocado) · `1 de 2` (llaves de identificación — no tocado). Lo que este acto mueve es la honestidad de un tier: una celda que decía `Fuerte` sin sostén claro ahora lo dice explícitamente.

---

## §6 · Cierre

**Antes** (worktree limpio contra `68a3466`, antes de cualquier edición de este acto):

```
$ python3 tests/check.py --baseline
19 FAIL · 127 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 997482bbda18b52621e24909eedbed0630c7a111)
```

**Después** (con los tres commits de contenido de este acto ya escritos):

```
$ python3 tests/check.py --baseline
21 FAIL · 126 WARN
LÍNEA BASE: ROJO — 2 entradas nuevas frente a tests/baseline.json
  · T16: canon/estado-programa-v1_10.md:129 declara 127 WARN vigente; la corrida real da 126 WARN
  · T16: canon/estado-programa-v1_10.md:221 declara 19 FAIL · 127 WARN vigente; la corrida real da 19 FAIL · 126 WARN
  (2 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

**Desglose por test, no agregado.** Las dos entradas nuevas son el mismo mecanismo de cascada que `CIERRA-17AGO`/`REGISTRA-17AGO` ya dejaron precedentado: `canon/estado-programa-v1_10.md` declara cifras de FAIL/WARN "vigentes" en dos citas históricas (`:129`, `:221`), y este acto —al cambiar el total real (19→21 FAIL, 127→126 WARN: dos FAIL nuevos son las propias entradas de `T16` citadas arriba, y el WARN neto combina la fila nueva de `T22` que `FP-53` agrega en COMMIT 3 con las dos ediciones de contenido de `glosario`/`integrador`/`corpus`/`hitoD-preregistro`)— las deja desactualizadas. `canon/estado-programa-v1_10.md` está fuera del perímetro de este acto salvo por la cascada `:27`/`:101` (conteo de ADR — sin cambio, ver abajo): no se persigue esta cascada de `T16` aquí, mismo criterio ya aplicado por `CONSOLIDA-17AGO`/`CIERRA-17AGO` para el mismo tipo de defecto, y consistente con `ADR-101(c)`/`FP-51`: un recongelado no es la vía rutinaria, y esto no es una regresión de sustancia — es una cifra citada que quedó atrás. Se declara, no se persigue, no se recongela.

**ADR y cascada `:27`/`:101`, re-derivados al escribir Y al fusionar — la colisión que el encargo anticipó ocurrió de verdad.** Ningún commit de este acto sella una decisión de mesa nueva: `FP-38` se firma citando la cita de mesa ya dada (17/ago), las tres propagaciones de COMMIT 2 propagan resoluciones ya tomadas (`ADR-94`, `glosario:316`), y la fila de COMMIT 3 se abre citando `ADR-101` sin sellar nada nuevo. **Este acto no escribe ningún ADR propio.** Al escribir (contra `68a3466`), el máximo era `101`, sin cambio frente a lo que `estado-programa:27`/`:101` ya declaraban. Al re-derivar justo antes de empujar el commit de cierre:

```
$ git fetch origin main
68a3466..afbdf4f  main       -> origin/main
$ git merge-base --is-ancestor origin/main HEAD
(falla — drift real, no falso positivo)
$ git diff --stat 68a3466 origin/main
canon/estado-programa-v1_10.md                                    |  4 +-
canon/gobernanza-v1_15.md                                         | 33 ++++++++++-
forense/encargos/2026-08-18-SELLA-RUTAS-ajustado-metodologia.md   | 49 +++++++++++++
forense/hallazgos.md                                              |  2 +
forense/metodologia-identificacion-vs-ajuste-v0_1.md              |  6 +-
forense/notas/2026-08-18-sella-rutas.md                           | 67 ++++++++++++++++
milpa/procedencia.yaml                                            |  4 +-
```

`PR #258` (`ACTO SELLA-RUTAS`) fusionó mientras este acto corría y selló `ADR-102` (procedimiento de la clase `AJUSTADO`, `forense/metodologia-identificacion-vs-ajuste-v0_1.md`). **Cero colisión de contenido** — ninguno de los archivos que `SELLA-RUTAS` toca está en el perímetro de este acto, y viceversa; el único archivo compartido es `forense/hallazgos.md`, apéndice puro en ambos lados. `git merge origin/main` limpio, sin marcadores de conflicto (`Auto-merging forense/hallazgos.md`, `Merge made by the 'ort' strategy`). `SELLA-RUTAS` ya dejó su propia cascada escrita (`estado-programa:27`/`:101` → `102 ADR`) — no hay nada que este acto necesite propagar. El máximo real, re-confirmado tras el merge:

```
$ grep -oE "^\*\*ADR-[0-9]+" canon/gobernanza-v1_15.md | sed -E 's/\*\*ADR-//' | sort -n | tail -3
100
101
102
```

**102, no 101.** La cita de `ADR-101` D-10 en `FP-53` (COMMIT 3) no cambia por esto: `ADR-101` sigue existiendo con el mismo texto, solo dejó de ser el número más alto.

**No se recongela `tests/baseline.json`** sin ADR de mesa (`ADR-76(f)`). `--freeze` no se corrió.

**`git diff --check`:** limpio, sin marcadores de conflicto ni espacio en blanco al final de línea introducidos por este acto.

**`CONSOLIDA-17AGO` marcada parcialmente consumida** (adenda fechada sobre su propio archivo, sin editar su cuerpo verbatim): PARTE 2 y PARTE 1(b)/(c)/(d) ejecutadas por este acto; PARTE 1(a) ya la había ejecutado `CIERRA-17AGO`/`ADR-92(d)`; PARTE 3 y PARTE 4 siguen `VIVO`, sin ejecutar.

Este encargo, `forense/encargos/2026-08-18-CONSOLIDA-2.md`, queda `CONSUMIDO` con el PR de este acto.
