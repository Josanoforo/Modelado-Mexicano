# ENCARGO · ACTO GEN2-FALSADOR-PLANTILLA-V22-1 · la medición, a tres meses del sello, del falsador de la plantilla de encargo (NC nuevas con PARO-PREMISA, PARO-ENTORNO o FUERA-DE-PERÍMETRO), con su veredicto CONFIRMA o ROMPE

> ENTORNO: **NUBE** — es una lectura de `forense/no-corrido.tsv` por comando; no abre microdato ni necesita red. El hook de arranque imprime ENTORNO-DERIVADO; si no coincide, PARA en una línea.

CABECERA · SHA de redacción `a7a91f41` (origin/main al redactar; re-deriva al abrir) · una sola sesión (D-17) · MODELO: **Sonnet** (D-13) · MODO: **ABIERTO** · CONTADOR: ninguno (`cuenta_gen2`, `celdas_validadas` y `legacy_activas` NO deben moverse); no adopta ni retira la plantilla · CALC-id reservado: ninguno · FP/ADR/NC candidatos: raíz de acto (D-24) — no se derivan aquí, los deriva `tools/cierre_acto.py` contra el 0-bis; no se renumeran nunca.
REDACCIÓN: PROPUESTO-POR-EJECUTOR (GEN2-PENDIENTES-4, 29/sep/2026). Este encargo NO está lanzado: dirección o mesa lo lanza adjuntando su archivo `.md` (§0), y `/acto` lo archiva verbatim en su 0-bis con su propio sello de cuerpo.

## 1 · OBJETIVO
Producir la lectura del falsador de `PLANTILLA-ENCARGO-v2_0.md` que la ventana de tres meses sigue debiendo: cuántas de las NC nuevas del 20/sep al 20/dic/2026 llevan `PARO-PREMISA`, `PARO-ENTORNO` o `FUERA-DE-PERÍMETRO`, comparado con la base de 75 de 160 (46.9 %), y el veredicto de vocabulario cerrado CONFIRMA (bajó a menos de un tercio) · ROMPE (no bajó) · INCONCLUSO (con la razón). Habilita que mesa decida si la plantilla se revisa, con un número y no con una impresión.

ORDEN SUGERIDO, no compuerta: no lanzar antes del 21/dic/2026, porque la ventana cierra el 20/dic/2026 y medirla antes la trunca; hoy es 29/sep/2026. Si se lanza antes, el resultado se rotula PARCIAL con los días transcurridos y la NC no se cierra.

«Hecho» son estos comandos sobre el commit final con `origin/main` fusionado, con fecha de commit ≥ 2026-12-21:
- `python3 tools/nc_por_razon.py --desde 2026-09-20 --hasta 2026-12-20` → salida cruda pegada en la nota con el SHA de `origin/main`, y la proporción de las tres razones sobre el total de NC nuevas de la ventana, comparada con 75/160 = 46.9 %.
- `python3 tools/consulta.py nc NC-0418` → `estado=CERRADA` con cita a la nota.
- `python3 tests/check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA
Ninguna firma nueva es necesaria: medir y reportar no adopta nada. El veredicto ROMPE no revisa la plantilla; solo pone la decisión delante de mesa con el número (§9 de las instrucciones: el falsador se revisa cuando el defecto desaparece o a los tres meses).
- Antecedente: `NC-0418` la dejó abierta con dueño de mesa fechado, y `forense/analisis/pendientes-3/decididas-por-delegacion.tsv` (fila NC-0418, `DUEÑO-MESA`) propuso dejarla abierta con el comando del falsador en la fila, hasta la ventana.

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo
- [LEÍDO] `forense/encargos/PLANTILLA-ENCARGO-v2_2.md:141-143` (§FALSADOR): «Si `PARO-PREMISA` + `PARO-ENTORNO` + `FUERA-DE-PERÍMETRO` no bajan de 47 % a menos de un tercio de las NC nuevas en los tres meses siguientes a su sello, la plantilla no resolvió el defecto y se revisa … El mismo falsador de v2.0 sigue vigente; ni v2.1 ni v2.2 reinician la ventana de medición.»
- [EJECUTADO] `python3 tools/nc_por_razon.py --help` → opciones `--desde`, `--hasta` (fecha ISO inclusive sobre la columna `fecha`) y `--tsv`; `ls tools/nc_por_razon.py` existe.
- [EJECUTADO] `date +%F` → 2026-09-29; la ventana del falsador es 2026-09-20 a 2026-12-20.
- [LEÍDO] `forense/encargos/PLANTILLA-ENCARGO-v2_2.md:5-9` (sección «Para qué existe»): entre el 16 y el 20/sep/2026, 75 de 160 NC nuevas fueron `FUERA-DE-PERÍMETRO` (48) o `PARO-PREMISA`/`PARO-ENTORNO` (27, en 18 actos): esa es la base de 46.9 %; la fila de `NC-0418` dice 47.1 % contra el árbol del sello de ADR-566 (172 NC), y el ejecutor declara contra cuál árbol compara (A.10).
- [EXISTE] `forense/encargos/PLANTILLA-ENCARGO-v2_0.md` y su sidecar, y `PLANTILLA-ENCARGO-v2_1.md`; no releí v2.0 para este encargo.
- [SUPUESTO] Que el libro siga clasificando la razón por token de prefijo (A.16) cuando el encargo se lance en diciembre: lo creo porque así lo lee `tools/nc_por_razon.py` hoy; si cambia, el ejecutor lo declara.

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO, no por frase
Búsqueda por objeto (universo: `forense/no-corrido.tsv` 1 102 filas por lector CSV; `forense/encargos/**` 1 229 rutas por nombre):
- No existe medición del falsador de v2.0: `git ls-files forense/notas | grep -ci 'FALSADOR-PLANTILLA'` → 0, y ningún encargo con ese rótulo (`git ls-files forense/encargos | grep -ci 'FALSADOR-PLANTILLA'` → 0).
- Homónimos descartados: `GEN2-V215` (redactó la plantilla y dejó la medición diferida), `GEN2-TRAMITE-INSTRUCCIONES-V217-1` (emitió la v2.2 sin reiniciar la ventana).
NC que este encargo absorbe (sucesor `DIRECCION-ENCARGO (GEN2-FALSADOR-PLANTILLA-V22-1)`):
- NC-0418 (medición del falsador de PLANTILLA-ENCARGO-v2_0 a tres meses del sello)

## 5 · PIEZAS — resultado esperado de cada una, no receta
**P1 · medición del falsador.** Corre el comando de §1 con la ventana completa, pega la salida cruda y el SHA de `origin/main`, y escribe la nota `forense/notas/<fecha>-GEN2-FALSADOR-PLANTILLA-V22-1.md` con: la proporción de las tres razones sobre las NC nuevas del 20/sep al 20/dic; la base de comparación con el árbol contra el que se comparó (A.10); el conteo de NC nuevas por acto y por razón (para distinguir un acto atípico de una tendencia); y el veredicto del vocabulario cerrado. Un dictamen «bajó de 47 % a menos de un tercio» es CONFIRMA; «no bajó» es ROMPE y el texto dice qué pieza de la plantilla no bastó según las razones más frecuentes; una ventana truncada o un cambio de clasificador es INCONCLUSO. Bien hecho: los comandos de §1. Rama prevista: si el clasificador por token cambió y la comparación no es homogénea, INCONCLUSO con el detalle y sin recalcular la base a mano.

## 6 · LATITUD
Cláusula de autonomía v1.0 (`forense/encargos/CLAUSULA-AUTONOMIA-v1_0.md`) vigente por norma (v2.17 §0): no se pega aquí. Discrepancias con el repo, interpretación declarada (`INTERPRETACIÓN-DECLARADA`), redacción rotulada (`PROPUESTO-POR-EJECUTOR`) y opción recomendada: del ejecutor.
DECIDES TÚ, y lo dices en la nota: el cómo · el orden · las herramientas · los nombres de archivo · remover obstáculos reversibles y baratos (enlazar `data/raw`, `git fetch --unshallow`, instalar una dependencia, regenerar un derivado por comando, corregir una cita rota) · arreglar un defecto adyacente de ≤ 10 líneas que te impide terminar, declarándolo.
PREGUNTAS A MESA, con 2–3 opciones y tu recomendación, y SIGUES con lo demás mientras tanto: bifurcaciones no previstas que cambian qué se entrega.
NO DECIDES: nada de la sección 7.

## 7 · PAROS — lista cerrada. Fuera de ella, no se para: se resuelve o se pregunta.
  a) abrir, derivar o imprimir dato de una ola reservada fuera del código autorizado
  b) borrar, forzar (`-D`, `--force`, `clean`) o reescribir algo sellado
  c) adoptar, o mover un contador que el encargo dice que no debe moverse
  d) cambiar estimando, universo, umbral, candidato o código de un procedimiento congelado
  e) entorno equivocado: microdato o corpus montado en NUBE (la sonda de arranque decide; si `data/raw` trae payloads, el derivador se voltea a CAJA y se declara, no es PARO)
  f) el OBJETIVO dejó de ser alcanzable o dejó de tener sentido → PARO, y eso es el entregable; leído estricto (D-19): solo sin ruta legítima
Enmienda de cableado (D-18): mientras el CALC no tenga `ejecucion.json`, un bloqueo de preflight de cableado puro (ruta de spec, sha de un input origen-repo, `dependencias_materiales`, constancia en lugar de archivo vivo, `permite_no_estimable`) se corrige en commit propio, declarado, y NO es PARO.

## 8 · COMPUERTAS — cada una declara qué protege
- «No editar `PLANTILLA-ENCARGO-v2_0.md` ni ninguna versión de la plantilla; revisarla es decisión de mesa» protege: adoptar.
- «La base de 75/160 no se recalcula ni se ajusta para que cuadre; se compara contra el árbol declarado» protege: congelar spec.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/notas/<fecha>-GEN2-FALSADOR-PLANTILLA-V22-1.md` (+ su sidecar) · `forense/no-corrido.tsv` (la NC-0418) · ADR y fragmento L0 propios.
Ajeno que no se toca: `forense/encargos/PLANTILLA-ENCARGO-v2_*.md` y sus sidecars, `tools/nc_por_razon.py` (se usa, no se edita), `forense/no-corrido.tsv` salvo la fila de NC-0418.
ARCHIVOS QUE OTRO ACTO EN VUELO ESTÁ TOCANDO (`git diff --name-only origin/main...origin/<rama>` filtrado a tools, tests, canon, libro, firmas y CI; corrido el 29/sep/2026 sobre `a7a91f41`; re-derívalo al abrir):
- `origin/acto/gen2-medicion-carriles-2--{enigh,enoe,naranja}`: `tests/test_mc2_*.py`, `tests/test_tablero_carriles.py`, `tools/tablero_carriles.py`, `tests/check.py`, `canon/gobernanza-v1_15.md`, `canon/L0/ADR-260928-GEN2-MEDICION-CARRILES-2-8fdf-0{5,6}.md`, `forense/firmas-pendientes.tsv`.
- `origin/claude/new-session-8tmg5a` (GEN2-CIERRE-Y-PRODUCTO-3): `canon/informe-programa-v1_6.*`, `canon/catalogo-del-mexicano-v1_4.*`, `canon/tabla-de-piso-v1_3.tsv`, `canon/reglas-bloque-adopcion-1.*`, `tools/cierre_acto.py`, `tools/genera_deck.py`, `tools/genera_tabla_piso_v1_3.py`, `tests/check.py`, `tests/test_cierre_acto.py`, `canon/gobernanza-v1_15.md`, `canon/registro-rotulos.tsv`, `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`.
- El PR de `GEN2-PENDIENTES-4` (#1326) mientras esté abierto (`forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`, `canon/gobernanza-v1_15.md`, `canon/registro-rotulos.tsv`, `tests/check.py`, `forense/analisis/pendientes-4/**`) y el PR [deriva] (`derivados/auto-*`, rota en cada push a main: `data/corrida0/*.tsv` y demás vistas).
Los apéndices compartidos dan conflicto de apéndice al fusionar: se conservan ambas tandas.
«Si te encuentras escribiendo fuera de esta lista, PARA.» Si te encuentras escribiendo fuera de esta lista, PARA.
PERÍMETRO DE CIERRE — permanente, no hay que pedirlo: el test propio entra a CI como HUÉRFANO (`ci_guardias --ejecuta-huerfanos`), sin editar `verify.yml` ni `check.py` (D-21) · publicar en la vista las filas propias y su asiento de replay (E.7) · registrar en INFRAESTRUCTURA la tabla propia · dejar el fragmento L0 propio en `canon/L0/<ADR-raíz>.md`, nunca en la línea `L0` compartida ni en `canon/estado-programa-v1_N.md` · la cascada de /acto · hallazgos, NC y FP propios, con ids de raíz de acto (D-24) — nunca «el siguiente número libre». Fuera del perímetro y necesario para terminar → es LATITUD (≤ 10 líneas, declarado) o es PREGUNTA. «FUERA-DE-PERÍMETRO» como razón de una NC queda para lo que de verdad es de otro acto, y se nombra ese acto.

## 10 · LO QUE NO HACE · SUCESORES · AUDITORÍA · CIERRE
Lo que NO hace: no revisa ni retira la plantilla; no mide el falsador propio de v2.2 (recibir un sha por chat o una recomendación sin opciones), que es de mesa y de lectura de hojas; no reinicia la ventana.
Sucesores: si el veredicto es ROMPE, un encargo de revisión de la plantilla con las razones más frecuentes como entrada; si es CONFIRMA, se anota y el falsador se cierra.
Auditoría: este encargo no afirma nada sobre México; pregunta [v2.3] ¿qué deuda «asumida a propósito» caducó al cambiar la función del programa? El falsador de proceso caduca a los tres meses si no atrapa nada (§9 de las instrucciones) y aquí se decide con un número; ¿cuántos contadores movió el trabajo? (cero; una línea al inicio de la nota).
El cuerpo de este encargo no lleva campos para rellenar ni líneas de estado: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` las añade /acto al final del archivo archivado (A.3), nunca editando lo de arriba. Adendas de mesa recibidas durante la ejecución: archivo propio `<este-encargo>-ADENDA-N.md`, sellado al recibirse, citado sólo en el CIERRE.
