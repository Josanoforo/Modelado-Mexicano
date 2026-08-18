# ENCARGO · ACTO B2-V7 — generación v7 y las tres cifras del bloque 2

**SHA de redacción:** `997482b` (merge #244, `origin/main`, verificado por `git ls-remote` el 18/ago/2026)
**Entorno asignado:** UBUNTU, worktree existente `/home/pc0/Modelado-Mexicano-barrido2`. NO clones. NO en la nube.
**Estado:** CONSUMIDO — PR #256 (`acto-b2-v7`), 18/ago/2026.
**Precedencia:** ninguna. Corrió en paralelo con ACTO CI-CATEGORÍA (nube).

> Archivado bajo A.3 por el propio acto que lo ejecuta. Texto verbatim tal como se lanzó;
> lo único añadido es esta cabecera y la marca de estado. El bloque VERIFICACIÓN DE
> EXISTENCIA que la convención exige venía ya contestado por quien escribió el encargo y
> se conserva en su sitio, más abajo.

---

## Texto verbatim del encargo

SHA de redacción: 997482b (merge #244, origin/main, verificado por git ls-remote el 18/ago/2026) Entorno asignado: UBUNTU, worktree existente /home/pc0/Modelado-Mexicano-barrido2. NO clones. NO lo lances en la nube: .barrido2/ (~30 GB) no está en ningún remoto y un clon fresco nace sin índice E2 ni snapshot — reconstruirlo son 672 inspecciones. Estado: VIVO Precedencia: ninguna. Corre en paralelo con ACTO CI-CATEGORÍA (nube).

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════ Reporta las cinco líneas de abajo y NO empieces hasta tenerlas.

1 · REPO. Ve al worktree existente /home/pc0/Modelado-Mexicano-barrido2. Si no existe, o si existe y .barrido2/ no está dentro: PARO y decisión de mesa. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status

2 · SHA. Este encargo se escribió contra 997482b, que ya incluye el merge de #244 — tu rama codex/barrido-2 ya fusionó. Empieza desde main actualizado, no desde la rama vieja. Si main se movió más: refresca y reporta, no es PARO.

3 · data/raw + .barrido2/. Aquí sí importan. Reporta la salida cruda de:

```sh
ls data/raw/ 2>/dev/null | head -3
du -sh .barrido2/ 2>/dev/null
ls .barrido2/private/t0/snapshot-v4.json .barrido2/private/t0/ledger-v7.tsv 2>&1
ls -d .barrido2/tasks-v7 .barrido2/staging-v7 2>&1
ls -lh .barrido2/private/e2-neutral-index.jsonl 2>&1
```

⚠️ snapshot-v4.json es el vigente. El de v2 está superado y sus cifras contradicen el PRISMA. Si lo que encuentras es v2, PARA.

4 · ENTORNO. Reporta las tres partes crudas (A.2):

```sh
echo "[${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}]"
curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
ls data/raw/ 2>/dev/null | head -1
```

Firma esperada de esta caja: sin_variable + sonda que responde + corpus montado. Si el corpus no está montado, PARA — es la firma que mató a E-ENCIG y S-IDG3 el 5/ago. NUNCA curl -I.

5 · ESPEJO. Toda cifra sale de este worktree con el comando a la vista.
════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por quien escribe el encargo ═══

1 · ESTRUCTURA. Gobiernan este dominio: .barrido2/private/t0/ledger-v7.tsv (el ledger), data/curacion-universo/contrato-barrido2-v1_0.json (el contrato) y data/curacion-registro/** (los productos). Este encargo escribe el ledger, los 672 expedientes de staging-v7, los productos de data/curacion-registro/ y su nota forense. NO escribe tests/baseline.json — deliberadamente, ver PROHIBICIÓN abajo.

2 · CONTENIDO. Corrido contra 997482b, salida cruda por objeto:

```
tools/curador_registro/inspect_assets.py            EXISTE-SATISFACE
tools/curador_registro/write_barrido2_w0.py         EXISTE-SATISFACE
tools/curador_registro/write_barrido2_material.py   EXISTE-SATISFACE
tools/curador_registro/barrido2_material.py         EXISTE-SATISFACE  (exento_estructural():283)
tools/curador_registro/integrate_barrido2.py        EXISTE-SATISFACE
data/curacion-universo/contrato-barrido2-v1_0.json  EXISTE-SATISFACE
find . -name "correr-olas*" -o -name "*olas*v7*"    NO-ENCONTRADO
```

⚠️ correr-olas-v7.py NO ESTÁ EN EL REPO. El transfer lo cita como <scratchpad>/correr-olas-v7.py, y la sesión que lo tenía cerró con el contexto al 100%. Es una infracción viva de A.3 y es el mayor riesgo de este acto — ver §1.

Las tres cifras del bloque 2: NO-ENCONTRADO en forense/notas/ — nunca se entregaron, por eso existe este acto.

3 · COBERTURA RETROACTIVA. Los módulos write_barrido2_* y el contrato nacieron dentro de BARRIDO-2 (agosto/2026), después del grueso del corpus. Nada anterior pasó por ellos, y su ausencia en el ledger no prueba que un activo no exista.

════════════════════════════════════════════════════════════════════

PERÍMETRO Y CONCURRENCIA. Este acto toca: .barrido2/** (fuera del repo) · data/curacion-registro/** · forense/notas/<fecha>-b2-v7.md · tools/ solo para el §1 · canon/gobernanza-v1_15.md (ADR) · forense/encargos/ (marcar CONSUMIDO). En paralelo corre ACTO CI-CATEGORÍA en la nube, cuyo perímetro es tests/check.py, tests/baseline.json y forense/firmas-pendientes.tsv. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

🚫 PROHIBICIÓN EXPLÍCITA: no corras --freeze. Bajo ninguna circunstancia. main está ROJO contra su propio congelado a propósito, con dos entradas declaradas (FP-47, FP-48, ambas T22). Mientras dure, la lectura correcta de una PR no es el color sino el desglose por test: si sube algún FAIL, hay regresión; si solo sube T22, es el tablero. ACTO CI-CATEGORÍA está arreglando esa categoría en paralelo. Si tu CI sale rojo, pega el desglose por test y sigue — no congeles.

1 · PASO 0 · El driver de olas — resuélvelo antes de nada

Sin él no hay generación v7. --barrido2-inspect procesa una tarea a la vez (--task, --roots-config, --contract, --staging-dir, verificado en inspect_assets.py:548). El bucle que recorre los 672 descriptores agrupados en las cuatro olas (W1 26 · W2 246 · W3 396 · W4 4) vivía en el scratchpad de una sesión que ya cerró.

En este orden:

Búscalo en la caja antes de reescribirlo. Puede seguir en disco:

```sh
   find / -name "correr-olas*" -o -name "*olas*v7*" 2>/dev/null | head
   ls ~/.claude* /tmp /home/pc0 2>/dev/null | head -40
```

Si aparece: commitéalo a tools/curador_registro/ tal cual, antes de correrlo. No lo mejores en el mismo commit. A.3 no admite otro ciclo de esto.
Si no aparece: recontrúyelo, y decláralo como reconstrucción, no como el original. Lo único que necesita es leer los descriptores de .barrido2/tasks-v7/, agrupar por ola e invocar --barrido2-inspect por tarea. Deriva la asignación de ola del propio descriptor o del ledger — no la teclees, y verifica que el reparto reproduce 26 · 246 · 396 · 4 = 672. Si no reproduce, PARA: el descriptor no dice lo que supones.
Commitéalo antes de la corrida larga. Si la caja muere a los 60 minutos, lo único que no se puede reconstruir es lo que nunca se empujó.

2 · La secuencia, en este orden y no en otro

Copiada del transfer del propio acto (forense/notas/2026-08-18-b2-transfer.md, en el repo, 156 líneas — es la fuente autoritativa de la mecánica; esto es el mapa).

```sh
# 1 · materializar — YA HECHO: tasks-v7 + ledger-v7 desde snapshot-v4. Verifica, no repitas.
# 2 · las cuatro olas   (~67 min · W1 26 · W2 246 · W3 396 · W4 4)
python3 <driver del §1>
# 3 · SEGUNDO materialize, CON --staging-root, o el gate falla con LEDGER_NO_TERMINAL
unshare -Urn -- python3 -m tools.curador_registro.inspect_assets --barrido2-materialize \
  --snapshot .barrido2/private/t0/snapshot-v4.json \
  --contract data/curacion-universo/contrato-barrido2-v1_0.json \
  --task-root .barrido2/tasks-v7 --ledger .barrido2/private/t0/ledger-v7.tsv \
  --staging-root .barrido2/staging-v7
# 4 · W0 ANTES que material, o el material se pierde: W0 reescribe ledger, PRISMA y baseline
unshare -Urn -- python3 tools/curador_registro/write_barrido2_w0.py …
# 5 · material
unshare -Urn -- python3 tools/curador_registro/write_barrido2_material.py …
```

Las dos trampas de orden, nombradas para que no las descubras de nuevo:

El segundo --barrido2-materialize con --staging-root no es opcional. Sin él el gate falla con LEDGER_NO_TERMINAL.
W0 va ANTES que material. W0 reescribe ledger, PRISMA y baseline; al revés, el material se pierde.

Y la trampa que costó dos reejecuciones enteras: MATERIAL_BUILD_SHA256 es el sha256 del propio barrido2_material.py. Cualquier edición del módulo invalida los 672 expedientes, aunque el cambio no pueda alterar un byte de salida. Ya pasó dos veces (la segunda dejó 399 de 672 no terminales). El remedio aplicado fue un solo predicado, exento_estructural() (barrido2_material.py:283), que usan escritor y validador. No lo separes, y no toques ese módulo durante la corrida.

Remedio de método, aplícalo: corre el gate contra tres o cuatro expedientes antes de lanzar la ola completa. Un gate que solo habla al final convierte cualquier hallazgo suyo en una corrida entera.

3 · Las tres cifras — el entregable

Sin ellas el bloque 2 no está reportado.

```
#    cifra    referencia declarada
1    value labels de SAV conservados    DTA conserva 99.5 %
2    metadatos de miembro ZIP conservados, con zip_slip presente    control ya corrido: crc=3266880665;zip_slip=NO sobrevive entero
3    PDF abiertos de los 83    control ya corrido: 77 de 78; enut2002_fd.pdf declarado con rc=/stderr=/bytes_texto=
```

Dos commits mínimo, y el orden del diff es el sello. COMMIT A congela la especificación —qué se cuenta, sobre qué universo, con qué denominador— antes de abrir ningún resultado, y cierra con la frase literal: "el primer resultado que produzca este procedimiento es el que se reporta". COMMIT B trae las cifras y no edita el COMMIT A. Si la especificación estaba mal, un tercer commit lo dice; nunca se corrige hacia atrás.

Cada cifra entra con su escala declarada (A-bis 3). Un porcentaje de conservación y un conteo absoluto no se comparan sin decir cuál es cuál, y el denominador de cada una se escribe al lado — "de los 83" y "de los 78 que abrieron" no son el mismo universo, y el propio control ya mezcla ambos.

Estampa de universo (A.10). Las tres cifras se sellan contra el SHA del worktree, la generación (v7) y el número de expedientes examinados. Si la generación cambia después, el sello queda VENCIDO EN ALCANCE — no refutado, no borrado, no vigente para el territorio nuevo.

4 · Lo que SÍ y lo que NO, después de las cifras

Sí, si sobra caja y solo en este orden:

C4 · las 17 de M-APERTURA. Siguen 17 de 17 en INDEXADO-NO-DESCARGADO, que es lo que §18.8 prohíbe. Ocho grupos de payload las cubren.
C4 · la tabla de tareas semánticas y propuestas-barrido2.tsv.

No, y son PARO si te encuentras haciéndolo:

No arranques C5. integrate_barrido2.py existe y nunca corrió; tiene un defecto abierto conocido — una PROPUESTA_ALTA validada aborta el lote como error de preflight en vez de terminar en uno de los cuatro estados que §19 exige. Correrlo antes de arreglarlo mete decisiones falsas a capa 4.
No arranques C6. No existen data/cableado-universo-v1_0.tsv, build_cableado.py ni T23, y --require-cableado es una bandera que check.py ignora en silencio (verificado: grep -c "require-cableado" tests/check.py → 0). La especificación de T23 —19 condiciones de FAIL, sus WARN y dos pruebas negativas— está en forense/notas/2026-08-17-b2-derivaciones-c4.md §4. Es acto propio.
No cierres la muestra adversarial. Build 1.0 contra 1.1, 0 de 41 hashes coinciden, sin veredicto. La exigencia 4 del §15 no está satisfecha y decirlo así es el entregable; fabricar un veredicto para cerrarla, no.

5 · Cierre

Nota del acto en forense/notas/<fecha>-b2-v7.md, con la secuencia real corrida y las desviaciones si las hubo.
ADR nuevo en gobernanza — re-derívalo, no lo teclees: grep -oE "^\*\*ADR-[0-9]+" canon/gobernanza-v1_15.md | grep -oE "[0-9]+" | sort -n | tail -1 (hoy 95, cero huecos). Si otro acto selló entre medias, renumera y dilo.
Marca este encargo CONSUMIDO con su PR.
Merge local siempre. GitHub no honra merge=union del lado servidor; el editor web de conflictos está prohibido.
⚠️ canon/estado-programa-v1_10.md:101 se automergea en silencio quedándose con un lado entero. Si tu merge lo toca, revísalo cláusula por cláusula. Es FP-48, y ya bloqueó el perímetro de cuatro actos seguidos.

Módulo de auditoría — la única pregunta aplicable: ¿cuántos contadores movió este acto? Si las tres cifras salen, la respuesta no es cero por primera vez en varios días: dilo con el contador exacto y su escala. Si no salen, di cero en una línea al inicio, sin justificarlo.
