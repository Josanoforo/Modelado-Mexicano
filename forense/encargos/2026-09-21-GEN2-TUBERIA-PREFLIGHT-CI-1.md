ENCARGO · ACTO GEN2-TUBERIA-PREFLIGHT-CI-1 · EL CI CORRE preflight SOBRE TODO CALC SIN SELLO QUE UN PR AÑADA O TOQUE, Y SÓLO SE PONE ROJO CUANDO EL RUNNER NO PODRÍA CORRERLO POR CABLEADO

CABECERA · redactado contra 5a888bcb (re-deriva al abrir; si main se movió no es PARO: refresca, fusiona hacia la rama, re-deriva y reporta) · ENTORNO: NUBE — Claude en la nube, CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default, con credenciales de Git y publicación de PR funcionando; cero microdato, data/raw no hace falta ni debe existir · una sola sesión, rama propia (D-17) · MODO: ABIERTO (D-18) · MODELO SUGERIDO: Opus (se puede subir, nunca bajar) · COMPUERTA: ninguna — no abre dato, no congela spec, no adopta, no borra (D-20) · CONTADOR: cuenta_gen2 = NO — no mide ninguna celda del programa · vehículo: /acto.

EL PR NO SE FUSIONA EN ESTE ACTO. Se publica y queda propuesto; mesa central lo revisa y fusiona. El acto termina con ## CONSUMIDO citando el número real de PR, verificado contra el HEAD remoto.

Ramas vivas al redactar: cinco (acto/gen2-celda-d-piloto-3-commit-2-3, acto/gen2-din-credito-pisos-enif2021-1, acto/gen2-tramite-firmas-3-propagacion, claude/focused-archimedes-fjyqf5, claude/new-session-ccjtu7). Re-deriva y declara el conteo al abrir (A.13). No necesita ventana. Si para entonces corre también GEN2-TUBERIA-SIDECAR-CUERPO-1, los dos tocan .github/workflows/verify.yml: concurrencia normal, se fusiona main hacia la rama y se re-deriva.

IDS DE ESTE ACTO.

ADR: numérico, como siempre. Máximo en main hoy: ADR-576. Deriva al cierre, no heredes; renumera quien fusiona segundo.
NC y FP: si hacen falta, la misma regla que el resto de TUBERÍA: raíz de acto (NC-<AAMMDD>-GEN2-TUBERIA-PREFLIGHT-CI-1-<4 hex del 0-bis>-<NN>) sólo si main ya contiene el merge de GEN2-TUBERIA-SUCESOR-1; si no, esquema viejo. Declara en el cierre cuál aplicó.
1 · EL MANDATO, verbatim (mesa, 21/sep/2026)

«Medí los 15 CALC sin sello que hay hoy en main: 8 pasan preflight y 7 no. De esos 7, 5 son versiones superadas y 2 son los de este piloto. Un chequeo en CI que corra preflight sobre todo CALC sin sello que un PR añada o toque habría atrapado #926 al nacer. Tarda segundos y no necesita corpus. Pasa el gate D-14: el defecto se observó tres veces, detuvo una medición un día cada vez y el chequeo cuesta menos que un solo paro.»

2 · OBJETIVO

Que ningún PR pueda fusionar un CALC sin sello que el runner no podría correr por cableado —spec que no resuelve, campo obligatorio vacío, input de repo sin hash declarado—, sin poner rojo un PR por un estado legítimo —spec congelada sin medidor todavía, CALC que espera los resultados de un hermano, corpus que no está en el runner—.

Criterio de «hecho»: el chequeo corre en CI en cada PR y en cada push a main, sólo sobre los CALC sin sello que ese cambio añade o toca; su prueba por mutación está verde; la re-corrida retrospectiva de §4 da el mismo resultado que dirección midió (7 rojos en 3 PR, cero rojos falsos); python3 tests/check.py --baseline --parallel en LÍNEA BASE VERDE; PR publicado y propuesto; ## CONSUMIDO con el PR real.

3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo
EJECUTADO · El conteo de mesa se reproduce. En main 5a888bcb hay 168 CALC con spec.yaml y 15 sin sello.json. python3 tools/corrida0.py preflight sobre los 15, sin corpus: 8 VERDE, 7 BLOQUEADO, en 44 s en total — unos 3 s por CALC.
EJECUTADO · Los 7 bloqueados. Cuatro superados por un hermano -v1_1 ya sellado (DINERO-FAMILIARES-VEJEZ-0001, EVASION-NORMA-0001, HORIZONTE-VIA-DERIVADOS-0001, TIENE-AHORROS-0001); uno superado por su sucesor del mismo piloto (GOB-DIGITAL-EXE-EMISIONES-0001, sustituido por -0002); y los dos del piloto celda-D, que trajo #926: GOB-DIGITAL-EXE-EMISIONES-0002 y GOB-DIGITAL-EXE-ADJUDICACION-0001.
EJECUTADO · El defecto de #926, a la vista. Los dos CALC declaran spec_md: forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md —ruta desde la raíz— y preflight la resuelve relativa al directorio del CALC (tools/corrida0.py, md = d / spec_md). La casa usa spec_md: spec.md en 150 CALC y ../../../forense/prereg-caja/… en 5. Además traen inputs origen: repo sin sha256 declarado.
LEÍDO · El piloto ya lo asentó. En la rama viva acto/gen2-celda-d-piloto-3-commit-2-3, forense/hallazgos.md trae: PARO (b) sin parche … el CALC que #926 congeló no corre bajo corrida0 run porque su preflight sale BLOQUEADO … El v1.1 se validó por pytest … y nunca por corrida0 preflight … la prueba del congelador no ve el cableado del runner. preflight sólo hace sha256 del zip: se puede exigir VERDE antes de congelar sin abrir la ola. Esa rama no toca data/corrida0/: el chequeo nuevo no la pone roja.
EJECUTADO · Las tres veces del gate D-14, contadas por PR que introdujo el defecto: #781 (15/sep, cuatro CALC sin spec.md, topado por GEN2-MEDICION-DEMANDA-2 el mismo día), #903 (19/sep, EMISIONES-0001 sin seed, tolerancia ni resultados, topado por la ejecución del día siguiente) y #926 (20/sep, ruta de spec_md, topado por COMMIT-2-3 esa noche). El piloto nombra #903/#924; #924 es la ejecución que topó el de #903, no uno nuevo. «Detuvo una medición un día cada vez»: REPORTADO; lo medido es de horas a un día entre la fusión y el paro.
LEÍDO · No toda BLOQUEADO es defecto — la casa lo dejó escrito. forense/notas/2026-09-15-GEN2-SPECS-DEMANDA-1-mapa-19.md, línea 324: «preflight reporta BLOQUEADO:script_ausente en los seis. Es el estado correcto de una spec congelada sin corrida, no un defecto.» Y ADJUDICACION-0001 depende de EMISIONES-0002/resultados.json, que no existe hasta que EMISIONES-0002 corra: input_repo_ausente es, ahí, un estado de cadena.
LEÍDO · preflight devuelve un diccionario, no sólo texto: {"veredicto", "bloqueos", "avisos", …} (tools/corrida0.py, def preflight(calc_id, imprime=True)). Las familias de bloqueo, derivadas del código (líneas ~1400-1900 y los helpers _bloqueos_de_inputs, _bloqueos_de_dimensiones, _bloqueos_de_seed, _bloqueos_de_resultados), son 27: ausente, calc_id_discorda, calc_ya_sellado, campo_sustantivo_ausente, ids_*, input_manifiesto_*, input_repo_ausente, input_repo_no_commiteado, input_repo_sha_discorda, input_repo_sin_sha_declarado, no_commiteado, resultado_* (cinco), script_ausente, seed_* (seis), sello_previo_incompatible, spec_md_sha256_* (dos), spec_sin_*, tolerancia_sin_tipo, working_tree_dirty.
LEÍDO · El CI no tiene la base. .github/workflows/verify.yml clona con git fetch --depth=1 la ref refs/pull/N/merge: no hay HEAD^1 ni origin/main. Para saber qué CALC toca un PR hace falta la base. D-23: una herramienta de verificación no muta el clon que verifica — el chequeo no hace fetch dentro del clon de la suite.
EJECUTADO · preflight no escribe nada (su docstring: «No mide, no escribe, no arregla nada») y, sin corpus, no puede abrir dato reservado: sólo hace sha256 de lo que hay, y en el runner no hay nada.
4 · LA PROPUESTA LITERAL PONDRÍA ROJOS FALSOS — y la clasificación que lo evita, ya medida

EJECUTADO · Re-corrida retrospectiva. Para cada PR fusionado a main en 14 días, tomé los CALC sin sello cuyo spec.yaml el PR añadió o modificó —25 CALC en 11 PR— y corrí preflight en el commit de ese PR, con el corrida0.py de ese commit, leyendo su diccionario de bloqueos.

Chequeo literal —rojo si preflight dice BLOQUEADO—: 7 PR rojos, de los que 4 son falsos (#775, #776, #785 por script_ausente en specs congeladas sin corrida, y #629 por corpus ausente).
Chequeo con clasificación —rojo si hay algún bloqueo fuera de la lista cerrada de estados legítimos—: 3 PR rojos, los tres verdaderos (#781, #903, #926), cero rojos falsos, cero omisiones, cero tokens desconocidos. 7 CALC en rojo, 11 en WARN, 7 limpios.

La lista cerrada de estados legítimos (WARN, no FAIL) — y todo lo demás es FAIL, porque eso es lo que preflight mismo dice cuando bloquea:

Bloqueo	Por qué es legítimo
script_ausente	spec congelada sin corrida todavía (la nota del 15/sep)
input_repo_ausente · input_repo_no_commiteado	el input es el resultado de un CALC hermano que aún no corre (cadena)
input_manifiesto_*	corpus que no está en el runner — el runner nunca tiene corpus
spec_md_sha256_discorda_origin_main	el CI no tiene origin/main; si aparece, se reporta

Fuera de alcance, sin adjudicar: calc_ya_sellado y sello_previo_incompatible (un CALC sellado no entra al chequeo) y working_tree_dirty (si aparece, el que ensució el árbol es el propio CI: es error del chequeo, no del PR).

Por qué «todo lo demás es FAIL» y no una lista de FAIL: así el chequeo no se acopla a la evolución de tools/corrida0.py, que es de dirección. Si dirección añade un bloqueo nuevo, el chequeo lo trata como preflight lo trata —bloquea— sin que nadie toque el chequeo. Sólo un estado legítimo nuevo exige tocar la lista, y eso sí debe ser una decisión visible.

5 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO (A.8)
EJECUTADO: preflight en .github/workflows/verify.yml: 0 ocurrencias; en tests/check.py: sólo un comentario (línea ~6621). Ningún test corre preflight sobre CALC de un PR. NO-ENCONTRADO.
EJECUTADO: en 14 días, 342 PR fusionados, 83 tocaron algún CALC, y 8 tocaron alguno de los 15 que hoy siguen sin sello — cada uno una sola vez, al nacer. Ningún PR volvió a tocar un CALC ya superado. El alcance «añade o toca» no dejará rojos permanentes sobre los cinco superados; si algún día un PR los toca, el chequeo los evalúa como a cualquiera.
Los dos CALC del piloto siguen BLOQUEADOS en main y no se arreglan aquí: el arreglo es del sucesor del piloto. El chequeo no los toca mientras nadie los toque; cuando el sucesor los corrija, el chequeo verifica el arreglo.
6 · PIEZAS — resultado esperado, no receta

P0 · 0-bis (A.3) y chequeo de duplicado por CONTENIDO. Este encargo verbatim a forense/encargos/. Mira también si alguna rama viva archiva ya este encargo, no sólo si su nombre lleva el rótulo. Declara cuántas ramas examinaste. Si hay duplicado: PARA con cero commits.

P-a · El chequeo. Un script o test que:

Deriva el universo del cambio: los directorios data/corrida0/CALC-*/ con algún archivo añadido o modificado entre la base y la cabeza, que no tienen sello en la cabeza.
Llama preflight(calc_id, imprime=False) importando tools/corrida0.py —sin modificarlo— y lee bloqueos.
Clasifica cada bloqueo contra la lista cerrada de estados legítimos de §4: dentro → WARN; fuera → FAIL; fuera de alcance → se reporta sin adjudicar.
Imprime, por CALC, el veredicto y cada bloqueo con su clase, de modo que un rojo diga exactamente qué lo puso rojo.
Con cero CALC en el universo, pasa y lo dice: «0 CALC sin sello tocados».

La lista de estados legítimos vive en un solo sitio, con una línea por estado que cite por qué es legítimo (la nota del 15/sep, la dependencia de cadena, la ausencia de corpus).

P-b · El cableado en CI. Un job propio en .github/workflows/verify.yml, con su propio clonado que traiga la base —por ejemplo --depth=2 sobre la ref de merge, cuyo primer padre es la punta de main—, porque D-23 prohíbe hacer fetch dentro del clon de la suite. Instala requirements.txt (PyYAML) como hace la suite. Corre en PR y en push a main. El diseño exacto del clonado es tuyo; lo que no es negociable es que el job tenga la base sin mutar el clon de otro job.

P-c · Prueba por mutación. Sobre CALC sintéticos en un directorio temporal —nunca sobre los reales—, como mínimo: uno limpio que pasa · uno con spec_md que no resuelve (el caso #926) que falla · uno con spec_sin_seed (el caso #903) que falla · uno sin spec.md (el caso #781) que falla · uno con sólo script_ausente que sale WARN · uno con sólo input_repo_ausente que sale WARN · uno con un bloqueo inventado que no está en ninguna lista y falla. Más el caso de universo vacío.

P-d · La re-corrida retrospectiva, como evidencia del acto. Repite la medición de §4 con el chequeo ya escrito —los 25 CALC de los 11 PR de los 14 días previos al redactado, cada uno en el commit de su PR— y asienta el resultado en la nota. Si no reproduce «3 PR rojos, los tres verdaderos, cero falsos», no es PARO: se reporta la diferencia con su causa y se sigue.

P-e · Hallazgos en forense/hallazgos.md:

El chequeo, el defecto que atrapa (las tres veces), y la corrección a la propuesta literal: 7 PR rojos con 4 falsos contra 3 PR rojos, todos verdaderos.
PARA-v2.16 · E.5/D-22 —semilla, sin ejecutar—: un CALC se da por congelado cuando corrida0 preflight no trae bloqueos fuera de la lista de estados legítimos; la prueba del congelador no sustituye la del runner. Motivo: el hallazgo del piloto.

P-f · Cierre. Cascada de /acto, check.py --baseline --parallel VERDE o PARO, ## NO-CORRIDO / RESERVAS al final del encargo («Ninguno.» es obligatorio), ## CONSUMIDO con el PR real. La nota de cierre lleva basename distinto del encargo (T02) y todo rótulo nuevo se registra con su prefijo de espacio (T25).

7 · LATITUD

El cómo es tuyo: dónde vive el chequeo (test en tests/ o herramienta en tools/), cómo detecta el sello, cómo arma el clonado del job, cómo escribe los CALC sintéticos. Un obstáculo reversible y barato se resuelve y se declara (D-19). Si main se mueve, fusiona hacia la rama y re-deriva.

Si al derivar las familias de bloqueo del código encuentras una que no está en §3, no es PARO: aplica la regla —fuera de la lista de legítimos, FAIL— y decláralo en la nota.

8 · PAROS — lista cerrada

Entorno sin credenciales de publicación · otra rama viva ya archiva este encargo · modificar tools/corrida0.py · correr preflight en un entorno con corpus montado o abrir cualquier microdato · que el chequeo escriba en el árbol que verifica · objetivo inalcanzable. Fuera de esta lista no se para: se resuelve, o se pregunta a mesa con opciones y recomendación y se sigue con lo demás.

9 · PERÍMETRO Y CONCURRENCIA

Escribes en: el archivo del chequeo · su test de mutación · .github/workflows/verify.yml (sólo el job nuevo) · forense/encargos/ (este encargo) · forense/notas/ (la nota de cierre) · forense/hallazgos.md · forense/no-corrido.tsv · y la cascada de gobernanza que cierre_acto.py --aplica reconcilia. Más el perímetro de cierre permanente (D-21). Si te encuentras escribiendo fuera de esta lista, PARA.

No tocas: tools/corrida0.py (de dirección; se importa, no se edita) · ningún CALC real, sellado o no, incluidos los dos del piloto · milpa/ · los jobs existentes de verify.yml · tests/check.py salvo lo que la cascada estándar exija · .claude/commands/acto.md.

10 · LO QUE NO HACE · SUCESORES

No arregla los dos CALC del piloto (sucesor del piloto) · no corre preflight sobre todos los CALC sin sello, sólo sobre los que un cambio toca · no borra ni marca los cinco superados · no cambia qué bloquea preflight · no toca la plantilla ni E.5/D-22 (sólo siembra) · no fusiona su propio PR.

Sucesores, en el orden de mesa: (3) RES/CORR con llave lógica; (4) un archivo por entrada; (5) taxonomía de PR y regla de enrutamiento. Este chequeo es la primera clase «CALC» de esa taxonomía: la regla de enrutamiento podrá leer su veredicto.

11 · FALSADOR (§9)

Si en tres meses el chequeo no ha puesto rojo un solo PR, se anota y se revisa si valía el aparato. Si pone rojo un PR por un estado que resulta legítimo, la lista de §4 está incompleta: se añade el estado con su razón, en un acto, visible —nunca se relaja la regla de «todo lo demás es FAIL».

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| **P-f · el criterio de «hecho» «`python3 tests/check.py --baseline --parallel` en LÍNEA BASE VERDE»** | `FUERA-DE-PERÍMETRO:ACTO GEN2-SENAL-1` — la suite da **2 FAIL nuevos**, los dos de `T22`, sobre `forense/encargos/2026-09-21-GEN2-SENAL-1.md` y su nota de cierre (marcador de ranura sin fila en `firmas-pendientes.tsv`). Los dos archivos son de otro acto y el PERÍMETRO de éste (§9) no los incluye. **Verificado heredado, no causado:** la misma suite sobre `origin/main` `a61dd000` limpio, en clon temporal (D-23), da **exactamente esos dos** FAIL y los mismos **25** WARN nuevos de `T03` — el conjunto de FAIL de esta rama es **idéntico** al de su base, y este acto **no añade ni un FAIL ni un WARN**. | Ninguno sobre contadores (`cuenta_gen2 = NO`, cero movidos). El impacto real: el encargo pide VERDE y la base no lo está, así que se entrega con el conjunto de FAIL idéntico al de `main`, **declarado**, en vez de tocar archivos ajenos para forzar el verde. | `ACTO GEN2-SENAL-1`, o el acto de trámite que registre la ranura en `forense/firmas-pendientes.tsv`, que es lo que `T22` pide. Fila: `NC-260921-GEN2-TUBERIA-PREFLIGHT-CI-1-9919-01`. |

Fuera de esa fila, las seis piezas (P0, P-a, P-b, P-c, P-d, P-e) se ejecutaron en este acto y P-f
es este cierre. Dos cosas que el encargo previó explícitamente y que **no** son
filas de esta sección, porque no son trabajo no corrido sino resultado
declarado:

- **P-d no reprodujo la cifra al pie de la letra y el encargo dijo qué hacer:**
  «si no reproduce, no es PARO: se reporta la diferencia con su causa y se
  sigue». La diferencia es una fila de más (`#600`, donde `preflight` aún no
  existía en `corrida0.py`) y está explicada en la nota de cierre §4 y en el
  ADR. Los tres verdaderos y los cuatro falsos reproducen **exactos**.
- **Los dos CALC del piloto siguen BLOQUEADOS en `main`** y este acto declara
  desde el encargo que no los arregla: son de `PR #944` (sucesor del piloto).
  No es deuda de este acto ni `FUERA-DE-PERÍMETRO` de nadie — es alcance
  declarado por dirección y ejecutado por otro acto vivo.
