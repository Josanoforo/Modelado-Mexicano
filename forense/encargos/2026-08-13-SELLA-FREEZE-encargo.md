# ENCARGO ACTO SELLA-FREEZE · el recongelado sin ADR, los dos cambios de tests/ sin sello, y la fecha del pegado de v2.8

- **SHA de redacción**: `84b2acf` (`origin/main`, merge #228 · ACTO TRIAGE-63 COMMIT 2) — derivado por comando el 13/ago/2026, no heredado. Refrescado al arrancar este acto (14/ago/2026): idéntico, sin movimiento de `main`.
- **Entorno asignado**: NUBE — repo-only, sin red, sin corpus.
- **Estado**: `CONSUMIDO` — ejecutado por `PR #229` (rama `claude/encargo-acto-sella-freeze-6l3za7`), `ADR-81` en `canon/gobernanza-v1_15.md`; detalle comando por comando en `forense/notas/2026-08-13-sella-freeze.md`.

---

## Texto completo del encargo, tal como se recibió

SHA de redacción: 84b2acf (origin/main, merge #228 · ACTO TRIAGE-63 COMMIT 2) — derivado por comando el 13/ago/2026, no heredado.
Estado: VIVO.
Gate: ninguno. Todo lo que este acto sella ya ocurrió y está en main.
Archívese este archivo en forense/encargos/ antes o junto con el lanzamiento (A.3). Su texto está completo aquí: no cita ningún documento que no esté en el repo.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════
Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.
1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.
2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.
3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.
4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto.
5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.
════════════════════════════════════════════════════════════════════
Sobre el punto 4 en este acto: este acto no toca microdato ni red. Dilo y salta el punto, per la propia excepción del bloque.
═══ VERIFICACIÓN DE EXISTENCIA — contestada por quien escribe el encargo ═══
1 · ESTRUCTURA. Dominio 7 de data/INFRAESTRUCTURA-v1_0.md — "Sellar una decisión de gobierno (ADR + cascada)" — derivado del índice, no de memoria. Salida cruda del índice:
## Dominio 7 · Sellar una decisión de gobierno (ADR + cascada)
`canon/gobernanza-v1_15.md` §4 ("Registro de decisiones") ...
- Vía de escritura: A MANO, exclusivamente ...
- Numeración: estrictamente secuencial sin huecos, validada por T15
  (regex ^\*\*ADR-(\d+), tests/check.py:482-507).
- Cascada real: el ADR mismo + cabecera de conteo en canon/gobernanza-v1_15.md
  (línea 2) y el contador en canon/estado-programa-v1_10.md (líneas 27, 99).
ESCRIBE: canon/gobernanza-v1_15.md (el ADR nuevo + la enmienda in situ de §3) y canon/estado-programa-v1_10.md (cascada del contador).
NO ESCRIBE, con razón: tests/check.py y tests/baseline.json — este acto sella lo ya hecho, no lo rehace; volver a tocarlos sería sellar y ejecutar en el mismo acto, que es la autoadjudicación que ADR-76(f) existe para impedir. canon/modelo-decision-v4_0.md — el índice dice que solo entra si el ADR toca reglas o tiers del motor; éste no. data/, milpa/ — ningún dominio de este acto los alcanza.
⚠️ Trampa que el propio índice declara y que este acto DEBE atender: "cualquier ADR nuevo que no recalcule y actualice esa cifra en ambos archivos arriesga sumar una 5ª línea NO congelada, que sí rompe python3 tests/check.py --baseline". Hoy T16 reporta 6 divergencias, no 4 — estado-programa:129,221 y gobernanza:764,856 declaran 18 FAIL · 107 WARN y la corrida real da otra cifra. Recalcúlala por corrida real y actualízala en los dos archivos.
2 · CONTENIDO. Comandos ejecutados contra 84b2acf y salida cruda:
$ python3 -c "import json;print(json.load(open('tests/baseline.json'))['head'])"
0ad9b7b759e138b251129c639f6ef943d6ee0fe7
$ grep -rn "0ad9b7b" canon/
(cero líneas — rc=1)
$ grep -niE "recongel" canon/gobernanza-v1_15.md
1104: **(f) El recongelado de la línea base — el precedente, sellado.** ...
1118: **Reversión.** ...
1148: **Lo que este ADR NO hace.** ... No recongela tests/baseline.json ...
1156: **Enmienda in situ, 13/ago/2026 — mesa autoriza el freeze que este ADR había dejado pendiente.** ... (--freeze, HEAD 3d0d1e5)
$ git log --since="2026-08-13 00:00" --format="%h|%s" -- tests/check.py
4a30a40|ACTO PROC-10-bis COMMIT 3: corrige T19b/T19c (no reconocian MEDIDO·NACIONAL) y recongela
1224c37|ACTO PROC-11 COMMIT 2: ejecuta el mapa congelado -- renombre de la theta, celda-D de obligacion_medida, D:14->15
536650b|ACTO A8-LAND: mesa autoriza freeze de baseline, CI en VERDE
4cc2131|Resuelve el hallazgo T15: excepción histórica, mismo mecanismo que T03
Resultado por objeto, vocabulario A.4:
objeto a sellar	clasificación	evidencia
ADR que sella el recongelado a 0ad9b7b (PROC-10-bis COMMIT 3)	NO-ENCONTRADO	grep -rn "0ad9b7b" canon/ → cero líneas. Buscado en todo canon/, por el SHA congelado.
ADR que sella el cambio de check.py de PROC-11 (1224c37, T19b/T19c 14→15)	NO-ENCONTRADO	ningún inciso de gobernanza cita 1224c37 ni el cambio de regex de T19c.
ADR que sella el cambio de check.py de PROC-10-bis (4a30a40, MEDIDO·NACIONAL)	NO-ENCONTRADO	ídem.
Precedente de que "solve to merge" cuenta como firma de mesa	EXISTE-SATISFACE	gobernanza:1156 (enmienda de ADR-78) + ENCARGO ADR-PROVISIONALIDAD §9 / PR #199. No hay que re-litigarlo: se cita.
Regla que exige ADR para recongelar	EXISTE-SATISFACE	gobernanza:1104, ADR-76(f), verbatim: "recongelar la línea base exige ADR de mesa; un ejecutor que encuentre drift lo reporta y no lo recongela. Sin condiciones adicionales".
Fecha del pegado de v2.8 en el proyecto de Claude (A.9 / ADR-78)	EXISTE-NO-SATISFACE	el inciso existe y dice PENDIENTE — no sellada hasta el pegado (gobernanza, bloque ADR-78). Falta solo la fecha.
3 · COBERTURA RETROACTIVA. Nacimiento de cada tabla gobernante, git log --diff-filter=A:
canon/gobernanza-v1_15.md        8a341da  2026-07-30
canon/estado-programa-v1_10.md   a6d5d40  2026-08-04
tests/baseline.json              1afaea0  2026-07-29
tests/check.py                   343d589  2026-07-29
Las cuatro son anteriores al trabajo que se sella (13/ago/2026). Sin brecha retroactiva: la ausencia del ADR en gobernanza sí prueba que no se selló, porque la tabla existía y estaba en uso ese mismo día (ADR-75 a ADR-80 se escribieron en ella).
════════════════════════════════════════════════════════════════════
ENTORNO ASIGNADO: NUBE — repo-only, sin red, sin corpus. NO lo lances en la caja: no necesita microdato ni data/raw, y la caja es la capacidad escasa que hoy solo R5.1-D3 y PROD-P638 pueden usar.
PERÍMETRO Y CONCURRENCIA.
Escribe: canon/gobernanza-v1_15.md · canon/estado-programa-v1_10.md · forense/notas/2026-08-13-sella-freeze.md (nueva) · forense/hallazgos.md (una línea, merge=union) · forense/encargos/2026-08-13-SELLA-FREEZE-encargo.md (este archivo, A.3).
No toca: tests/** · data/** · milpa/** · canon/modelo-decision-v4_0.md · ningún encargo ajeno.
⚠️ Colisión real, no hipotética: A10-ESTAMPA y RUTA-SELLO también sellan ADR y por tanto escriben las mismas dos líneas de gobernanza y la misma cascada de contador. No corran en paralelo. Serialízalos: quien fusione primero obliga al siguiente a re-derivar su número. Ha colisionado cinco veces.
"Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."
§0 · Qué se sella, y por qué es un ADR y no una línea de hallazgos
Tres hechos ocurridos el 13/ago/2026, los tres en main, ninguno registrado en canon/:
tests/baseline.json fue recongelado a HEAD 0ad9b7b por ACTO PROC-10-bis COMMIT 3.
tests/check.py cambió dos veces sin ADR: 1224c37 (PROC-11, las dos regex gemelas de T19b/T19c, 14→15) y 4a30a40 (PROC-10-bis, T19b/T19c suman MEDIDO·NACIONAL).
El pegado de instrucciones-proyecto-v2_8.md en el proyecto de Claude ya ocurrió (13/ago/2026, reportado por dirección) y ADR-78 lo tiene como PENDIENTE.
Los tres necesitan ADR y no hallazgo, por razón escrita: ADR-76(f) dice, verbatim, que recongelar exige ADR de mesa. Una línea en hallazgos.md no satisface esa exigencia — la registraría como incidente en vez de como decisión, y el próximo ejecutor que encuentre drift no tendría precedente que citar.
Este acto no rehace nada. El recongelado ya está hecho y la suite está VERDE. Lo que falta es el registro, y el registro es lo que hace auditable la diferencia entre "mesa lo autorizó" y "un ejecutor lo hizo y nadie lo vio".
§1 · Inciso (a) — el recongelado a 0ad9b7b
La autorización existe y está documentada; no la inventes ni la re-litigues. Cítala verbatim de donde está:
forense/hallazgos.md, entrada de PROC-10-bis COMMIT 3: "El usuario pidió explícitamente «pull and solve CI» — autorización directa que sustituye a la firma de mesa ausente."
Precedente idéntico, ya sellado: gobernanza:1156 (enmienda de ADR-78), donde "solve to merge" se aceptó como autorización de mesa dada fuera del marco del encargo y por encima de él; y antes, ENCARGO ADR-PROVISIONALIDAD §9 / PR #199 ("solve Pr cant merge").
Lo que el inciso sella: el recongelado del 13/ago a HEAD 0ad9b7b queda autorizado ex post, con la autorización citada, no supuesta.
Alcance, y va acotado a propósito: este inciso no generaliza. No establece que toda autorización en línea de mesa sustituya un ADR; sella este recongelado y ratifica que ADR-76(f) sigue vigente sin condiciones adicionales. Si mesa quiere generalizar, es firma aparte. (Reversión: solo por ADR de mesa que revierta el freeze o que fije condiciones.)
Deriva y reporta, no copies: el head actual de tests/baseline.json, el diff de residuo que ese freeze absorbió (7×T03 + 6×T16, según la nota de PROC-10-bis — re-cuéntalo, no lo heredes), y la corrida real python3 tests/check.py --baseline.
§2 · Inciso (b) — los dos cambios de tests/check.py
Sella los dos, por separado, con su commit citado:
1224c37 (PROC-11 COMMIT 2). Cambio: las dos regex gemelas del contador de condicionales, 14→15. Está documentado como hallazgo (forense/notas/2026-08-13-proc-11.md §6.2: el perímetro nombraba la constante _CONTADOR_14 y el contador estaba vigilado desde dos sitios). Mesa firmó extender el perímetro en ese acto; lo que falta es el ADR.
4a30a40 (PROC-10-bis COMMIT 3). Cambio: tests/check.py:918,1001 suman count('clase: "MEDIDO·NACIONAL'). Sin él, la séptima clase sellada por ADR-79(a) es invisible para su propio test.
Los dos son mecánicos y ninguno cambia lógica de test — verifícalo con git show de cada uno y pega el diff en la nota. Si alguno resulta no ser mecánico, PARA y repórtalo: eso cambiaría qué hay que sellar.
Patrón que el inciso debe nombrar, porque es la tercera vez: un encargo nombró la constante en vez de la afirmación, y el contador vivía en dos sitios. Mismo defecto que I-07. Formulación propuesta para el ADR: el perímetro de un acto que toca un contador se declara por la afirmación que el contador sostiene, no por el nombre de la variable que la implementa.
§3 · Inciso (c) — enmienda in situ a ADR-78: la fecha del pegado
Localiza en el bloque de ADR-78 la línea que hoy dice:
Fecha en que instrucciones-proyecto-v2_8.md se pegó en el proyecto de Claude: PENDIENTE — no sellada hasta el pegado.
Enmienda in situ fechada — mismo mecanismo que ADR-75, ADR-76, ADR-78 y ADR-80 ya usaron; no borres el texto original, es la prueba de que la regla se aplicó a sí misma antes de cumplirse. La enmienda registra:
Fecha del pegado: 13/ago/2026.
Procedencia, declarada sin adorno: tipo (3) — reportado por dirección, no verificable por ningún acto con herramientas de repo. El proyecto de Claude vive fuera del repositorio; ninguna sesión puede leerlo. Es la limitación que la propia A.9 declara ("el pegado ocurre a mano, fuera de este repositorio"), no un defecto de este acto.
A.9 pasa de PENDIENTE a vigente.
§4 · Cascada y numeración
El número se deriva AL SELLAR, contra el main real, sin dejar hueco. Receta de T15 — córrela tú, no heredes el número de este encargo:
python3 -c "
import re
t=open('canon/gobernanza-v1_15.md',encoding='utf-8').read()
n=[int(x) for x in re.findall(r'^\*\*ADR-(\d+)',t,re.M)];s=sorted(set(n))
print('únicos',len(s),'max',max(s),'huecos',[i for i in range(1,max(s)+1) if i not in s])
"
Contra 84b2acf da únicos 80 · max 80 · huecos []. Si al sellar da otra cosa, ése es tu número, no el 81. T15 falla sobre huecos, no solo sobre el máximo.
Sitios de cascada — derívalos con grep -rn "[0-9]\+ ADR" canon/ README.md y pega la salida: canon/gobernanza-v1_15.md:2 (cabecera de conteo) y canon/estado-programa-v1_10.md (las dos citas, no solo el cierre del listado — lección de perímetro que ACTO RES ya pagó en ese archivo).
La cifra N FAIL · M WARN se recalcula por corrida real y se actualiza en los dos archivos (ver la trampa declarada arriba).
Contadores que este acto NO mueve, y decláralo uno por uno: 13 de 27 (Hito D) · 10 de 15 (condicionales) · 0 de 15 (coeficientes) · 1 de 2 (llaves) · 4 de 144. Ninguno. Mueve el conteo de ADR y nada más. Este acto es de gobierno puro y no mueve ningún contador de medición sobre México — dilo así en hallazgos.md, sin justificarlo (regla de señal, v2.3).
§5 · Lo que este acto NO hace
No toca tests/. Ni check.py ni baseline.json. Sella lo hecho; no lo rehace ni lo revierte.
No generaliza la autorización en línea como sustituto de ADR — §1 lo acota expresamente.
No reabre ADR-76(f), ni ADR-77, ni ADR-79, ni ADR-80.
No adjudica el rótulo A.7, disputado. Si A10-ESTAMPA ya fusionó cuando este acto corra, cita su resolución y no la re-decidas.
No re-examina ningún veredicto del Hito D.
§6 · Cierre
python3 tests/check.py --baseline antes y después, cifra reportada en ambas, LÍNEA BASE VERDE en las dos · nota propia en forense/notas/2026-08-13-sella-freeze.md con cada comando y su salida cruda · una línea en forense/hallazgos.md · este encargo commiteado a forense/encargos/ y marcado CONSUMIDO con su PR al cerrar (A.3: no se borra — un encargo consumido es el registro de qué se pidió exactamente) · merge local, origin/main HACIA la rama, editor web de conflictos prohibido (GitHub no honra merge=union sobre hallazgos.md).
Si al arrancar main se movió: no es PARO. Refresca, re-deriva el número de ADR y la cifra de suite, y reporta la diferencia antes de editar.
