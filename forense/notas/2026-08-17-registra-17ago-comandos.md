# ACTO REGISTRA-17AGO — las cinco firmas de mesa del 17/ago, los dos benchmarks, y las filas que faltaban

**Acto:** ACTO REGISTRA-17AGO · **Encargo:** `forense/encargos/2026-08-17-REGISTRA-17AGO.md` (archivado verbatim por A.3, primer commit) · **Entorno:** NUBE, repo-only, sin `data/raw` · **SHA de redacción del encargo:** `1282ae3` · **SHA real de arranque:** `1282ae3` (idénticos — sin deriva) · **Depende de:** `ADR-91` (sella el tablero como fuente única, fija el formato de `firmada_en`, precedente directo de este acto), `ADR-79(i)` (firma verbatim entre comillas).

---

## §0 · ARRANQUE — las cinco líneas, crudas

**1 · REPO.** Ruta absoluta: `/home/user/Modelado-Mexicano`. Rama de trabajo: `claude/new-session-wk4z60` (asignada por el arnés).

```
$ pwd && git log -1 --format="%h %s" && git status
/home/user/Modelado-Mexicano
1282ae3 Merge pull request #247 from Josanoforo/claude/celda-d-complemento-conflict-jursjw
On branch claude/new-session-wk4z60
nothing to commit, working tree clean
$ git rev-parse --is-shallow-repository
true
```

Clon superficial detectado en el arranque. Conforme al encargo y al precedente E-HIG, se corrió `git fetch --unshallow` **antes de emitir cualquier veredicto**:

```
$ git fetch --unshallow
From https://github.com/Josanoforo/Modelado-Mexicano
 * [new branch]      codex/barrido-2 -> origin/codex/barrido-2
 + f8eb2e3...1282ae3 main            -> origin/main  (forced update)
```

Tras el `--unshallow`, `origin/main` sigue en `1282ae3`, idéntico al HEAD local y al SHA de redacción del encargo. **Sin deriva que clasificar.** `git diff --name-only HEAD origin/main` → vacío.

**2 · SHA.** Base declarada `1282ae3`, base real `1282ae3`. Re-verificado antes de cerrar (`git fetch origin main`, después de los dos commits de contenido): `origin/main` sigue en `1282ae3`. **`main` no avanzó durante el acto — no hubo merge que hacer.**

**3 · `data/raw`.** Este acto **no toca microdato**. Dicho y saltado, per el encargo.

**4 · ENTORNO.**

```
$ echo "CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-<unset>}"
CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
$ curl -sS -o /dev/null -w "HTTP_STATUS:%{http_code}\n" https://github.com/ --max-time 15
HTTP_STATUS:400
```

Variable presente (`cloud_default`) — firma correcta de un acto de nube. La sonda cruda a `https://github.com/` da `400`, mismo patrón ya declarado por `ACTO FUENTE-UNICA-DECISIONES` (proxy de agente de la sesión, no GitHub — el acceso real por MCP y por `git fetch`/`push` funcionó en los dos commits de este acto). Discrepancia ya precedentada, sin efecto sobre ninguna cifra.

**5 · ESPEJO.** Ninguna cifra de esta nota viene del espejo del proyecto. Todas salen del clon, con el comando a la vista.

---

## §1 · Perímetro real, y la corrección a la verificación de concurrencia del encargo

**Escrito por este acto:** `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` (`ADR-92` + cabecera) · `forense/BENCHMARK-conf02-policronia-2026-08-17.md` (nuevo) · `forense/BENCHMARK-conf05-consumo-compensatorio-2026-08-17.md` (nuevo) · `forense/notas/2026-08-17-registra-17ago-comandos.md` (esta nota) · `forense/hallazgos.md` (una entrada) · `forense/encargos/2026-08-17-REGISTRA-17AGO.md` (A.3).

**No escrito, verificado:** `data/**`, `tools/**`, `canon/estado-programa-v1_10.md`, `canon/glosario-v5_6.md`, `canon/integrador-*`, `corpus/**`, `tests/**`, `instrucciones-proyecto-*` — cero archivos de estas rutas en los dos commits de contenido.

**La verificación de concurrencia del encargo tiene un error, y se corrige aquí.** El encargo afirma, "verificado con `git diff --name-only origin/main...origin/codex/barrido-2`", que `firmas-pendientes.tsv` **no** lo toca BARRIDO-2. Re-corrido el mismo comando contra el árbol real:

```
$ git rev-list --count origin/main..origin/codex/barrido-2
11
$ git diff origin/main...origin/codex/barrido-2 -- forense/firmas-pendientes.tsv
[...]
+FP-38	Re-firma de los cuatro expedientes de analista de produccion (ESP-OPACA-A/B/C/D) tras el cambio de baseline. [...]
```

Dos discrepancias, ninguna cosmética:

1. **BARRIDO-2 está 11 commits por delante, no 10** como decía el encargo.
2. **`firmas-pendientes.tsv` sí lo toca BARRIDO-2** — un append puro de una fila, `FP-38`, tema no relacionado (re-firma de expedientes de analista tras cambio de baseline del bootstrap semántico). No edita ninguna fila existente — verificado en el diff completo (única línea `+`, ningún `-`). **Sin colisión de contenido** con `FP-22`/`FP-25`/`FP-27`/`FP-28`/`FP-36` ni con `FP-15`/`FP-29`/`FP-31`. **Sí hay colisión de numeración**: el encargo instruye derivar las cinco filas nuevas del segundo commit "desde `FP-38` (verificado libre contra `1282ae3`)" — libre contra mi base, ya tomado en la rama de BARRIDO-2. Se declara en `ADR-92` con el mismo mecanismo ya precedentado para números de ADR: renumera quien fusione después, `T15` arbitra.

`forense/hallazgos.md` también lo toca BARRIDO-2, también por apéndice puro (cuatro entradas nuevas al final, cero ediciones a las existentes):

```
$ git diff origin/main...origin/codex/barrido-2 -- forense/hallazgos.md
[...]
+- **2026-08-17** · **El índice E2 de BARRIDO-2 conserva evidencia semántica en el 4.09 % [...]
+- **2026-08-17** · **Una heurística de nombre de persona [...]
+- **2026-08-17** · **El fail-closed de producción funcionó [...]
+- **2026-08-17** · **El estado material de un acto de barrido vive fuera de git por diseño [...]
```

Bajo riesgo — `merge=union`, sin editar líneas existentes, consistente con la política declarada de ese archivo.

**El resto de la verificación de concurrencia del encargo se sostiene.** El número de ADR (`91` contra `1282ae3`, sin huecos) coincide exactamente; el ADR nuevo se deriva a `92` y se declara renumerable si BARRIDO-2 fusiona primero, mismo mecanismo que BARRIDO-2 ya se aplicó a sí mismo (`d4b4242`, su propio ADR renumerado 91→92 al fusionar `origin/main`).

---

## §2 · Verificación de existencia — recorrida, no heredada

```
$ python3 -c "..." | grep -E 'FP-(22|25|27|28|36)'
FP-22: ABIERTA  firmada_en=(vacío)
FP-25: ABIERTA  firmada_en=(vacío)
FP-27: ABIERTA  firmada_en=(vacío)
FP-28: ABIERTA  firmada_en=(vacío)
FP-36: ABIERTA  firmada_en=(vacío)

$ ls forense/ | grep -i "benchmark.*conf"
(cero resultados)
```

Coincide exactamente con lo que el encargo declaraba: las cinco filas `EXISTE-NO-SATISFACE`, los dos benchmarks `NO-ENCONTRADO`.

**Número de ADR, receta de T15:**

```
$ grep -oP '^\*\*ADR-\K[0-9]+' canon/gobernanza-v1_15.md | sort -n | uniq -d
(vacío — sin duplicados)
$ python3 -c "nums=...; print('max:',max(nums),'count:',len(nums),'missing:',...)"
max: 91  count: 91  missing: []
```

Contra `1282ae3` da `91`, igual que el encargo predijo. `ADR-92` es el número derivado.

**FP-22, contención derivada, no heredada:**

```
$ python3 -c "
a=open('instrucciones-proyecto-v2_9.md',encoding='utf-8').read()
b=open('instrucciones-proyecto-v2_10.md',encoding='utf-8').read()
for k in ['A.9','A.10','A.12']: print(k, k in a, k in b)
print(a.count(chr(10)), b.count(chr(10)))
"
A.9 True True
A.10 True True
A.12 True True
356 384
```

Coincide exactamente con la cifra que el encargo predijo contra `1282ae3`.

---

## §3 · Los dos benchmarks — verificados por hash antes de commitear

```
$ cp .../270be283-BENCHMARKconf02policronia20260817.md forense/BENCHMARK-conf02-policronia-2026-08-17.md
$ cp .../33bc200e-BENCHMARKconf05consumocompensatorio20260817.md forense/BENCHMARK-conf05-consumo-compensatorio-2026-08-17.md
$ sha256sum forense/BENCHMARK-conf02-policronia-2026-08-17.md
30588ca05b31b9df774aa7309cce9d99aac8fc26cad9a46bdb8fba131dbc7064  forense/BENCHMARK-conf02-policronia-2026-08-17.md
$ sha256sum forense/BENCHMARK-conf05-consumo-compensatorio-2026-08-17.md
c39aa4b675c62163e908dc0217d0103c1559adaee2ff8ac3067b982512934a72  forense/BENCHMARK-conf05-consumo-compensatorio-2026-08-17.md
```

Ambos **concordantes** con la tabla del encargo, byte a byte (copiados directamente del archivo adjunto al lanzamiento, cero transcripción manual — la copia de archivo evita el riesgo de error de transcripción que habría exigido re-verificar por hash de todos modos). No hubo discordancia que forzara un PARO.

---

## §4 · Commit 2 — cada cita del barrido, verificada contra el árbol real

Todas las citas de las cinco filas nuevas y las tres correcciones se recorrieron contra el árbol antes de escribir la fila, no se heredaron del encargo. Comando por comando:

**`glosario:136` (FP-38):**
```
$ grep -n "Consumo compensatorio" canon/glosario-v5_6.md
136:| **Consumo compensatorio** | **Fuerte** (consumidor) / **Hipótesis** (salud) ⚠️ | (a)+(c) | `LEÍDO` | Velandia-Morales 2022 (base latinoamericana). [...]
```
Confirmado: procedencia `(a)+(c)`, exactamente como el benchmark conf.05 §1(d) lo describe.

**`integrador` — conf.02 (FP-39):**
```
$ sed -n '245p' canon/integrador-psicologia-mexicano.md
- **Evidencia en contra / límites.** La policronía de Hall (1959-1983) es cualitativa, antigua y esencialista; no hay medición nacional reciente de "policronía mexicana" (VACÍO grande). [...]
$ sed -n '351p' canon/integrador-psicologia-mexicano.md
- *Del tiempo:* "el mexicano es impuntual por naturaleza [...]". La "policronía mexicana" de Hall es marco antiguo y esencialista, no dato reciente.
```
Confirmado: ambas líneas toman partido por el mecanismo de `Tiempo`, sin ADR que lo respalde.

**`integrador` — conf.05, la auto-contradicción (FP-39):**
```
$ sed -n '36p' canon/integrador-psicologia-mexicano.md
8. **[Fuerte · la ironía maestra]** [...] Consumo compensatorio es **Fuerte** (Velandia-Morales 2022); [...]
$ sed -n '204p' canon/integrador-psicologia-mexicano.md
- **Evidencia a favor.** **Fuerte**: consumo compensatorio (Velandia-Morales 2022); [...]
$ sed -n '255p' canon/integrador-psicologia-mexicano.md
- **Evidencia en contra / límites.** [...] el consumo compensatorio como driver del refresco/botana es **Hipótesis**; [...]
```
Confirmado exactamente: `:36` y `:204` tratan el constructo como una sola rama `Fuerte`; `:255` ya lo separa, tratando la rama salud como `Hipótesis` sin decirlo explícitamente. Coincide con lo que el benchmark conf.05 §3 nombra como "el único sitio del corpus que ya tenía la partición correcta."

**`El Mexicano y el Tiempo:49` (FP-40):**
```
$ sed -n '49p' "corpus/reports/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md"
- La evidencia es **cualitativa y antigua** (décadas). No hay medición nacional reciente de "policronía mexicana". Esto es un VACÍO, no un dato.
```
Confirmado verbatim, línea exacta.

**PLAN-MULTIFASE-F0-F6-2026-08-13.md** *(citado sin backticks a propósito: vive fuera del repo y T03 no distingue mención de referencia — mismo remedio que `forense/notas/2026-08-14-enlace2-clase-limbo.md:3`)* **y "cuatro preguntas del transfer" (FP-42):**
```
$ find / -iname "PLAN-MULTIFASE-F0-F6-2026-08-13.md" 2>/dev/null
(cero resultados)
$ grep -rn "cuatro preguntas" . --include="*.md"
./forense/hallazgos.md:145: [...] ENCARGO M-1 [...]
./forense/notas/2026-08-05-m1-ensanut-mapa.md:81: ## Las cuatro preguntas
./forense/encargos/2026-08-05-m1-ensanut.md:38: Las cuatro preguntas que este acto contesta [...]
./PROPUESTA-remediacion-brecha-documental.md:16: [...] **U3 · DOC-BACKFILL** — las cuatro preguntas del transfer [...]
```
**Precisión sobre el texto del encargo:** el encargo dice que el grep "solo devuelve las de M-1/ENSANUT" — son tres, no todas. Hay una cuarta coincidencia: la propia cita de origen de `FP-33` (`PROPUESTA-remediacion-brecha-documental.md:16`), que nombra la necesidad de "las cuatro preguntas del transfer" sin enumerarlas. No cambia el fondo — sigue sin existir un documento `TRANSFER` que las defina —, pero la fila `FP-42` registra el conteo real, no el que el encargo escribió. `grep -rln "TRANSFER"` (mayúsculas, sin acento) devuelve 14 archivos, ninguno un documento `TRANSFER` propiamente dicho — todos son coincidencias parciales o menciones de paso.

**`tests/check.py:286` (FP-41):**
```
$ sed -n '285,299p' tests/check.py
CANONICO = {"FUERTE", "MEDIA", "MEDIA-FUERTE", "HIPÓTESIS"}
def t07_tier_vocabulary():
    [...]
                if tok.strip().upper() not in CANONICO:
                    ajenos[tok.strip()] += 1
```
Confirmado: `CANONICO` no coincide con Bloque A (fuerte · media · hipótesis razonable · narrativa popular) — añade `MEDIA-FUERTE`, omite `narrativa popular`. Confirmado el artefacto de conteo: el chequeo usa `.strip().upper()`, el conteo usa solo `.strip()` — `Moderada`/`MODERADA` cuentan como dos entradas distintas en `ajenos` aunque el propio chequeo las trate como una.

**`MOTOR-1 §4` (corrección de `FP-15`):**
```
$ grep -n "57(c)\|1 llave ejercida\|0 compuertas" forense/encargos/2026-08-14-MOTOR-1-consolidado.md
16:  - **COMMIT 1 — ejecutado [...]** Los incisos 1 [...], 3 (E5/ADR-57(c)) [...] corrieron completos. [...]
64: 3. **La cifra "0 llaves ejercidas" que `motor-matriz §4.3` usa está vencida.** Hoy es **`1` de `2`** [...]
```
Confirmado: `57(c)` corrió con veredicto SIN CAMBIO (inciso 3, "corrieron completos"), y la cifra vencida que E5 no debe copiar es exactamente "1 de 2", no "0".

**`propuesta-motor-adaptativo-celda-v0_4.md:122`, `ADR-71(d)`, `ADR-68` (corrección de `FP-31`):**
```
$ sed -n '118,126p' propuesta-motor-adaptativo-celda-v0_4.md
## 8 · Preguntas para mesa — resueltas, 12/ago/2026

La única pregunta que esta versión responde es la que `ADR-71(d)` ya adjudicó: el enum se corrige partiéndolo en dos [...]
$ grep -n "^\*\*ADR-68 \|^\*\*ADR-71 " canon/gobernanza-v1_15.md
908:**ADR-68 · Mesa adopta el contrato celda-D (v0.3) como formato del registro [...]**
960:**ADR-71 · Mesa firma las cuatro decisiones abiertas del transfer del 11/ago: [...] y el enum de `fuerza` del contrato celda-D se corrige antes del piloto.**
```
Confirmado línea 122 verbatim, y los dos ADR existen con el contenido que la corrección les atribuye.

**`hitoD-preregistro:322`, escala de R8.3 (corrección de `FP-29`):**
```
$ sed -n '322p' forense/hitoD-preregistro-v2_0.md
| **D-06** | R8.3 | Depende de `conf.06`, **abierto**: ninguna cifra de confianza interpersonal es usable. **Cualquier veredicto apoyado en ellas no cuenta** |
$ sed -n '249p' forense/hitoD-preregistro-v2_0.md
**A** <10 puntos con enforcement variado · **B** cualquier resultado apoyado en las cifras en conflicto — no cuenta · **C** exigiría reconciliar conf.06 primero · **D** pre-registrado como probable mientras conf.06 siga abierto.
```
Confirmado verbatim, ambas líneas.

**Vocabulario Bloque A (fuerte · media · hipótesis razonable · narrativa popular):** confirmado en uso extendido por 42 archivos del corpus (`grep -il "narrativa popular\|hipótesis razonable"`), consistente con la caracterización del encargo.

---

## §5 · PR — abierto temprano para conocer su propio número

Empujado el primer commit (archivo del encargo, A.3) y abierto `PR #248` (borrador) **antes** de escribir ninguna fila que cite su propio número — evita el mecanismo de "backfill" que `6f78d06`/`408a3d1` necesitaron. Los dos commits de contenido citan `PR #248` directamente, sin marcador pendiente.

---

## §6 · Cierre — `tests/check.py --baseline`, antes y después

**ANTES** (antes de tocar ningún archivo de contenido):

```
$ python3 tests/check.py --baseline
[...]
  20 FAIL · 128 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 6f78d066ae2aecf61ca63046e19242d46f4a255d)
```

Congelado `6f78d06`, igual al que el encargo declaraba al redactar.

**DESPUÉS** (tras los dos commits de contenido):

```
$ python3 tests/check.py --baseline
[...]
  28 FAIL · 128 WARN
  LÍNEA BASE: ROJO — 8 entradas nuevas frente a tests/baseline.json (HEAD congelado 6f78d066ae2aecf61ca63046e19242d46f4a255d)
  · T15: canon/estado-programa-v1_10.md: cita 91 ADR; gobernanza tiene 92 únicos
  · T16: canon/estado-programa-v1_10.md: declara 18 FAIL · 128 WARN vigente; la corrida real da N WARN
  · T16: canon/gobernanza-v1_15.md: declara 18 FAIL · 128 WARN vigente; la corrida real da N WARN
  · T22: FP-38 ABIERTA [...]
  · T22: FP-39 ABIERTA [...]
  · T22: FP-40 ABIERTA [...]
  · T22: FP-41 ABIERTA [...]
  · T22: FP-42 ABIERTA [...]
  (5 entradas de la línea base ya no aparecen — mejora, no bloquea)
```

**Se declara, no se recongela** — `--freeze` exige ADR de mesa (`ADR-76(f)`) y este acto no lo trae firmado, exactamente como el encargo anticipó. Desglose de las 8 entradas:

- **5 son `T22` (T-FIRMAS) imprimiendo las cinco filas nuevas de `FP-38`..`FP-42`.** Señal, no defecto — el encargo lo dice explícitamente: *"T-FIRMAS va a imprimir las filas nuevas y las firmas: eso es señal, no defecto."*
- **3 son `T15`/`T16`, consecuencia directa y esperada de la `CASCADA NO ESCRITA` declarada en `ADR-92`.** El conteo de ADR subió de 91 a 92 (cabecera de `gobernanza`, dentro de mi perímetro) pero `canon/estado-programa-v1_10.md` sigue citando 91 — porque ese archivo está fuera de mi perímetro (lo escribe activamente `BARRIDO-2`, verificado en §1). Mismo desborde que `ADR-91` ya declaró para sí mismo (*"T15 y T16 lo alcanzan por construcción y el mismo encargo exige --baseline VERDE en cada commit; las dos exigencias no pueden cumplirse a la vez"*). Quien fusione la cascada de ADR en `estado-programa-v1_10.md` cierra estas 3 entradas.

**Ninguna de las 8 entradas es un defecto introducido por error** — las cinco son el propósito declarado del acto (hacer visibles los pendientes), y las tres restantes son el costo ya aceptado de no invadir el perímetro de `BARRIDO-2`.

`git diff --check` sobre los dos commits de contenido: limpio, sin marcas de conflicto ni espacio en blanco al final de línea.

---

## §7 · Corrección post-revisión — el conteo de §6 estaba mal, y dos de las ocho eran mías

**Dirección revisó y corrigió: la corrida real da 11 entradas, no 8, y dos son responsabilidad de este acto, arreglables dentro de su propio perímetro.** Re-corrido `python3 tests/check.py --baseline` contra el estado tras los dos commits de contenido — confirmado, 11, no 8:

```
$ python3 tests/check.py --baseline
[...]
  30 FAIL · 129 WARN
  LÍNEA BASE: ROJO — 11 entradas nuevas [...]
  · T02: nombre normalizado colisiona: forense/notas/2026-08-17-registra-17ago.md · forense/encargos/2026-08-17-REGISTR[...]
  · T03: forense/notas/2026-08-17-registra-17ago.md: cita PLAN-MULTIFASE-F0-F6-2026-08-13.md (sin backticks aquí, mismo motivo que abajo), que no existe
  · T15: canon/estado-programa-v1_10.md: cita 91 ADR; gobernanza tiene 92 únicos
  · T16: canon/estado-programa-v1_10.md: declara 128 WARN vigente; [...]
  · T16: canon/estado-programa-v1_10.md: declara 18 FAIL · 128 WARN vigente; [...]
  · T16: canon/gobernanza-v1_15.md: declara 18 FAIL · 128 WARN vigente; [...]
  · T22: FP-38..FP-42 (5)
```

**T02 — mías, arregladas.** `forense/notas/2026-08-17-registra-17ago.md` y `forense/encargos/2026-08-17-REGISTRA-17AGO.md` normalizan (`t02_duplicates`: NFKD, ascii, minúsculas, solo alfanumérico) al mismo nombre: `20260817registra17agomd`. Arreglado renombrando la nota, no el encargo (el encargo es el archivo A.3, verbatim, y ya lleva el nombre que el propio documento adjunto traía):

```
$ git mv forense/notas/2026-08-17-registra-17ago.md forense/notas/2026-08-17-registra-17ago-comandos.md
$ python3 -c "...norm('2026-08-17-REGISTRA-17AGO.md')..."
encargo:  20260817registra17agomd
new note: 20260817registra17agocomandosmd
```
Distintos. Las tres referencias propias a la nota (en `canon/gobernanza-v1_15.md` ×3, `forense/hallazgos.md` ×1, y la línea `CONSUMIDO` que este mismo acto añadió en `forense/encargos/2026-08-17-REGISTRA-17AGO.md`) se actualizaron al nombre nuevo. **Las dos citas a la nota que viven dentro del texto *verbatim* del encargo (líneas 43 y 125 de `forense/encargos/2026-08-17-REGISTRA-17AGO.md`) NO se tocaron** — son el archivo A.3, y editarlas rompería la razón de ser de archivarlo verbatim: quedan como constancia de que el nombre original instruido colisionaba, no como referencia viva.

**T03 — mía, arreglada con el precedente exacto que dirección señaló.**
```
$ sed -n '3p' forense/notas/2026-08-14-enlace2-clase-limbo.md
**Encargo:** [...] (citado sin backticks a propósito: vive fuera del repo y T03 no distingue mención de referencia — mismo remedio que ENLACE-1 Commit 3)
```
Mismo remedio aplicado: el encabezado de la nota que citaba PLAN-MULTIFASE-F0-F6-2026-08-13.md entre backticks (el archivo no existe, es justo lo que `FP-42` documenta) pasa a citarlo sin backticks, con la misma glosa entre paréntesis. *(Y esta propia línea lo cita sin backticks, a propósito, por la misma razón — T03 escanea también dentro de bloques de código y de comillas dobles de markdown, no distingue mención de referencia en ningún contexto.)*

**T16 — la parte que dirección no nombró, y que sí era mía: el conteo real subió de 18 a 20 FAIL (núcleo, T16 excluido de sí mismo) porque `T15` ahora falla dos veces (`estado-programa:27` y `:101`), y eso rompió las CINCO citas "mutables" `**18 FAIL · 128 WARN**` de `gobernanza-v1_15.md` (líneas 764, 856, 1274, 1387, 1393) que antes coincidían.** Estas cinco se distinguen por texto propio de las dos verdaderamente congeladas (`:1106`/`:1136`, `18 FAIL · 104 WARN`, historia sellada de `ADR-76(f)`, nunca tocadas): las cinco dicen explícitamente *"cifra mantenida en sincronía por T16, no historia congelada"*. Mismo mecanismo, mismo remedio, que `ADR-91` ya aplicó sobre sí mismo: *"los sitios vigentes de **N FAIL · M WARN** en canon/, cambio de dígito únicamente, sin reescribir la prosa alrededor; los dos 'permanentes' [...] no se tocan."*

```
$ grep -noP '\*\*\d+\s*FAIL\s*·\s*\d+\s*WARN\*\*' canon/gobernanza-v1_15.md
764:**18 FAIL · 128 WARN**   856:**18 FAIL · 128 WARN**
1106:**18 FAIL · 104 WARN**  1136:**18 FAIL · 104 WARN**   [-- las dos permanentes, no tocadas --]
1274:**18 FAIL · 128 WARN**  1387:**18 FAIL · 128 WARN**  1393:**18 FAIL · 128 WARN**
```
Las cinco no-permanentes, cambio de dígito únicamente (18→20), script dirigido por número de línea para no arriesgar un `sed` global sobre un archivo de 1600+ líneas donde "18" aparece decenas de veces en prosa histórica que no debe tocarse:

```
$ python3 -c "... TARGET_LINES = {764, 856, 1274, 1387, 1393} ... OLD='**18 FAIL · 128 WARN**' NEW='**20 FAIL · 128 WARN**' ..."
touched: [764, 856, 1274, 1387, 1393]
```

**Estado final, re-verificado:**

```
$ python3 tests/check.py --baseline
[...]
  23 FAIL · 128 WARN
  LÍNEA BASE: ROJO — 7 entradas nuevas frente a tests/baseline.json (HEAD congelado 6f78d066ae2aecf61ca63046e19242d46f4a255d)
  · T15: canon/estado-programa-v1_10.md: cita 91 ADR; gobernanza tiene 92 únicos
  · T16: canon/estado-programa-v1_10.md: declara 18 FAIL · 128 WARN vigente; la corrida real da N WARN
  · T22: FP-38 ABIERTA [...]
  · T22: FP-39 ABIERTA [...]
  · T22: FP-40 ABIERTA [...]
  · T22: FP-41 ABIERTA [...]
  · T22: FP-42 ABIERTA [...]
  (5 entradas de la línea base ya no aparecen — mejora, no bloquea)
```

**7, no 8 ni 11 — y las 7 que quedan son exactamente lo que §6 ya argumentaba, ahora con el conteo correcto en vez de uno truncado por error propio:**

- **5 son `T22`, las filas nuevas.** Señal, no defecto — dicho explícitamente por el encargo.
- **2 son la cascada de ADR a `canon/estado-programa-v1_10.md`** (`T15` cuenta 2 sitios —`:27` y `:101`— colapsados en 1 línea en el resumen compacto; `T16` cuenta 1 sitio más, `:221`, la sexta cita "mutable" de `18 FAIL`, que vive en el archivo de `BARRIDO-2` y no en el mío). Las 2 permanentes de `gobernanza:1106`/`:1136` (`18 FAIL · 104 WARN`, historia sellada de `ADR-76(f)`) siguen fallando también, pero **ya estaban en la línea base** desde antes de este acto — no cuentan como nuevas, y no se tocan, por la misma razón que `ADR-89`/`ADR-91` ya dieron.

**Corrección al propio §6 de esta nota:** decía "3 son T15/T16" — eran 6 (las 5 mutables de `gobernanza` más la 1 de `estado-programa`), de las cuales 5 estaban en mi perímetro y se arreglaron aquí; solo la de `estado-programa` era genuinamente ajena. El conteo original de 8 entradas totales también estaba mal — la corrida real daba 11, no 8; T02/T03 no se habían medido después de escribir la nota, se habían dado por buenos sin re-correr el comando. Mismo defecto, en miniatura, que el hallazgo de `forense/hallazgos.md` sobre la verificación de concurrencia del encargo: **no basta con haber corrido el comando una vez — hay que re-correrlo después de cada cambio que pueda haberlo movido, no heredar la primera salida.**

`git diff --check`, re-verificado tras esta corrección: limpio.

**Contadores del programa que mueve este acto: 0.** Mueve el tablero de 11 a 16 `FIRMADA`, abre cinco filas (`FIRMADA-CONDICIONAL` sin cambio en 10). Ningún contador de medición sobre México.
