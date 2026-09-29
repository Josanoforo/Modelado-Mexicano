# ENCARGO · ACTO GEN2-REPLAYS-Y-RECIBOS-CAJA-1 · cuatro deudas de nube (un replay de ENOE, una adjudicación secundaria de ENVIPE, dos recibos con red) cerradas con salida cruda desde CAJA

> ENTORNO: **CAJA** — la pieza P1 abre el microdato `enoe_2024_4t_microdatos` y la P2 el de ENVIPE 2025 (corpus montado); las piezas P3 y P4 necesitan egreso a fuentes externas, que la NUBE no tiene (la sonda del arranque de hoy dio `DENEGADA-POR-POLITICA`). El hook de arranque imprime ENTORNO-DERIVADO; si no coincide, PARA en una línea.

CABECERA · SHA de redacción `a7a91f41` (origin/main al redactar; re-deriva al abrir) · una sola sesión (D-17) · MODELO: **Opus** (D-13) · MODO: **RÍGIDO** · CONTADOR: mueve `celdas_validadas` solo si P2 sella una adjudicación con veredicto (secundaria, rotulada por el orden de sellos); no mueve `cuenta_gen2` ni adopta nada; NO debe moverse ninguna cifra de los CALC ya sellados · CALC-id reservado: uno para la adjudicación de P2 (id de raíz de acto, lo acuña el acto; se cita por su llave hasta que su número entre a main) · FP/ADR/NC candidatos: raíz de acto (D-24) — no se derivan aquí, los deriva `tools/cierre_acto.py` contra el 0-bis; no se renumeran nunca.
REDACCIÓN: PROPUESTO-POR-EJECUTOR (GEN2-PENDIENTES-4, 29/sep/2026). Este encargo NO está lanzado: dirección o mesa lo lanza adjuntando su archivo `.md` (§0), y `/acto` lo archiva verbatim en su 0-bis con su propio sello de cuerpo.

## 1 · OBJETIVO
Cerrar cuatro deudas que la nube no pudo pagar (`NO-VERIFICABLE-AQUÍ` o `PARO-ENTORNO`) con la evidencia cruda que sí puede dar una sesión de CAJA: (P1) el replay `--oro` + `cmp` de los 39 estratos singleton de ENOE; (P2) la comparación primaria de las cuatro emisiones de C-ASTRA sobre ENVIPE 2025 contra el piso C2, con IC por réplica de R, con el procedimiento del piloto 4 sin parámetro nuevo; (P3) el recibo con red de las 10 citas externas de la muestra de #1243; (P4) la lectura primaria de las cinco cifras externas de consumo. Habilita retirar cuatro filas del libro sin cerrarlas por decreto y deja a Astra/mesa una lectura con procedencia.

«Hecho» son estos comandos sobre el commit final con `origin/main` fusionado (hoy todos dan el «antes» que el encargo cambia; los archivos nombrados los crea este acto):
- P1: `grep -c '^CMP-SALIDA: 0$' forense/analisis/replays-recibos-caja-1/enoe-oro-cmp.txt` → 1 (hoy: el archivo no existe).
- P2: `ls data/corrida0/CALC-ASTRA-ENVIPE-*ADJUDIC*/sello.json | wc -l` → ≥ 1 y `python3 tools/consulta.py nc NC-260923-GEN2-ASTRA-ENVIPE-ADJUDICACION-1-970c-01` con `estado=CERRADA` (hoy: 0 CALC y `estado=ABIERTA`).
- P3: `python3 -c "import csv;r=list(csv.DictReader(open('forense/analisis/replays-recibos-caja-1/recibo-con-red-8c5c-08.tsv',newline='',encoding='utf-8'),delimiter='\t'));print(len(r),sum(1 for x in r if x['localizador'].strip()))"` → `10 10`, o cada fila sin localizador pasada a receta de mesa con su motivo en la columna `estado_fila`.
- P4: `python3 -c "import csv;r=list(csv.DictReader(open('forense/analisis/replays-recibos-caja-1/lectura-primaria-con-red-9d28-03.tsv',newline='',encoding='utf-8'),delimiter='\t'));print(len(r))"` → 5 (las cinco cifras `tipo: externa` de `consumo-cifras.json`).
- Cierre: `python3 tools/consulta.py nc <id>` de cada una de las cuatro NC de §4 con `estado=CERRADA` y cita a estos archivos, y `python3 tests/check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA
- `FP-260923-GEN2-TRAMITE-FIRMAS-11-05da-01` · `FIRMADA` · 23/sep/2026, verbatim, mesa: «Integrar los dos, nada es fuera de plazo, todo se utiliza.» Es la firma que ordena adjudicar las cuatro emisiones ENVIPE de Astra (#1031) contra la R del piloto 4; su ejecución quedó a `GEN2-ASTRA-ENVIPE-ADJUDICACION-1` (que paró por entorno). P2 la ejecuta; no requiere firma nueva.
- Ninguna otra firma es necesaria: P1, P3 y P4 son recibos de lectura, no adoptan ni miden un estimando nuevo. Si en P2 el procedimiento heredado exige una decisión que el piloto 4 no tomó (por ejemplo, cuántas réplicas), esa pieza queda `NO-LANZADO (firma pendiente)` y las demás siguen.

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo
- [EJECUTADO] `python3 tools/consulta.py payload enoe_2024_4t_microdatos` → `archivo=enoe_microdatos_post2019/enoe_2024_trim4_csv.zip · sha256=817f28d20a43fa4fed08195e62df58bf320b31c323a3049fe09b5194a1677305 · fecha_descarga=2026-08-24`.
- [EJECUTADO] `python3 tools/familias-2027/enoe_inferencia_1/enoe_diagnostico.py --help` → flags `--oro ORO --salida SALIDA`; `ls forense/analisis/familias-2027-enoe-inferencia-1/diagnostico/` → `diagnostico.md`, `enoe-auditoria.json`.
- [LEÍDO] `forense/analisis/familias-2027/p2-enoe-v1_0.md:20-50`: el veredicto REPRODUCE se derivó del artefacto `enoe-auditoria.json`, no del diseño muestral; deja el límite de procedencia y la receta para caja.
- [EJECUTADO] `ls data/corrida0 | grep -ciE 'ASTRA-ENVIPE'` → 4 (los `CALC-ASTRA-ENVIPE-{DOMINIOXSEXO,EDADXESCOLARIDADPROXY,EDADXSEXO,ESCOLARIDADPROXYXSEXO}-0001`); `ls data/corrida0 | grep -ciE 'ASTRA-ENVIPE.*ADJUDIC'` → 0.
- [LEÍDO] `forense/notas/2026-09-23-GEN2-ASTRA-ENVIPE-ADJUDICACION-1-cierre.md:3-12`: el procedimiento heredado propaga ΔMAE con réplicas bootstrap de R sobre el microdato ENVIPE 2025 (`tools/celda_d/marginales_reproduccion.py::replicas_compartidas`); por eso el acto paró por entorno.
- [LEÍDO] `data/curacion-registro/celdas-d/TRA.evade_norma.envipe2025.edad_x_sexo.yaml:9` dice «C-ASTRA NO-ENTRA: #1031 no estaba en main antes de COMMIT-2; la comparación secundaria no se ejecuta». Ese sello no se edita (A.10): la adjudicación de P2 es un CALC nuevo y su marcador sale del orden de los sellos.
- [LEÍDO] `canon/MEMORIA-OPERATIVA.md:10`: «Regla 6: sin retadores, pilotos ni duelos sobre olas vistas». C-ASTRA es un contendiente ya sellado y firmado (05da-01), no un retador nuevo; la lectura es de dirección y la sesión la revisa antes de correr (rama en §5 P2).
- [LEÍDO] `forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-3/pr-1243.md:22`: la muestra de 10 es `random.seed(20260928)` sobre las 148 filas de las tablas; ids SANC-V1-X01, INTER-037, HUM-009, INTER-020, HUM-025, EMOC-031, EMOC-007, INTER-016, EMOC-002 y SANC-013.
- [EJECUTADO] `python3 -c` sobre `forense/analisis/reports-v2/consumo-familia-1/consumo/consumo-cifras.json` → 28 cifras: 23 `propia` y 5 `externa` (`CONS-QUAL`, `CONS-FISICO`, `CONS-TRADE2011`, `CONS-PRIVADA2011`, `CONS-TRADE2023`).
- [REPORTADO] Otra sesión (investigador de este acto, 28/sep) dice que CAJA abrió fuentes externas en actos previos; no lo verifiqué. Si CAJA no alcanza una URL, esa fila pasa a receta de mesa de un minuto (A.5), no a NC muda.
- [SUPUESTO] El corpus compartido en CAJA trae `enoe_2024_4t_microdatos` y `envipe2025_csv` con el sha del manifiesto; lo creo porque el manifiesto los lista, y lo verifica el arranque (A.1: AUSENTE · raíz-no-configurada · hash-discordante, salida cruda).

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO, no por frase
Búsqueda por objeto (universo: `forense/no-corrido.tsv` 1097 filas, `forense/firmas-pendientes.tsv` 649 filas, `forense/encargos/**` y `data/corrida0/` por nombre; comando de cada una en §3):
- El replay ENOE no está hecho: ninguna corrida `enoe_diagnostico.py --oro` está asentada (el único archivo del diagnóstico es el artefacto de nube).
- La adjudicación de C-ASTRA no está hecha: 0 CALC `*ADJUDIC*` de ASTRA-ENVIPE; homónimo descartado: `GEN2-ASTRA-ENVIPE-ADJUDICACION-1` (23/sep) es el acto que paró; este encargo es su sucesor y no repite su spec.
- `forense/analisis/reports-v2/recibo-con-red-1/` no existe (`ls` → error) y `forense/analisis/replays-recibos-caja-1/` tampoco.
NC que este encargo absorbe (sucesor `DIRECCION-ENCARGO (GEN2-REPLAYS-Y-RECIBOS-CAJA-1)`):
- NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-13 (replay ENOE `--oro` + `cmp`)
- NC-260923-GEN2-ASTRA-ENVIPE-ADJUDICACION-1-970c-01 (comparación primaria de C-ASTRA)
- NC-260926-GEN2-ASTRA6-C3-CONSUMO-FAMILIA-2-9d28-03 (lectura primaria de cifras externas de consumo)
- NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-08 (10 citas de la muestra de #1243)
NC hermana (no absorbida aquí; la cierra el acto `GEN2-PENDIENTES-4` como duplicada): `NC-260928-GEN2-ASTRA-CONTINUIDAD-C2-1-ba6c-01`, la misma deuda del replay ENOE abierta 12 horas después.

## 5 · PIEZAS — resultado esperado de cada una, no receta
**P1 · replay ENOE con corpus montado.** Produce `forense/analisis/replays-recibos-caja-1/enoe-oro-cmp.txt` con: el comando exacto, la salida cruda de `enoe_diagnostico.py --oro data/raw/enoe_microdatos_post2019/enoe_2024_trim4_csv.zip --salida <tmp>`, el resultado de `cmp <tmp> forense/analisis/familias-2027-enoe-inferencia-1/diagnostico/enoe-auditoria.json` como línea `CMP-SALIDA: <código>`, el sha256 del zip contra el del manifiesto (A.1) y el conteo de archivos examinados (A.13). Bien hecho: `CMP-SALIDA: 0` (REPRODUCE) o un diff explícito (NO-REPRODUCE, que se reporta y no se «arregla»). Si el zip no está montado o su hash discrepa, el reporte trae el estado A.1 crudo y la pieza queda `NO-VERIFICABLE-AQUÍ` con receta.

**P2 · adjudicación secundaria de C-ASTRA (ENVIPE 2025, cuatro cruces).** Dos commits mínimo (D-15, D-22): COMMIT-1 congela spec humana + `spec.yaml` que heredan el procedimiento del piloto 4 (`TRA-evade-norma-cruces-encogida-spec-v1_0.md`) sin parámetro nuevo, con el conducto que sella aceptando cada rama terminal (todas con soporte, parcial, cero puntuadas, celda rara vaciada) y con `preflight` VERDE de `corrida0` antes de abrir dato; COMMIT-2 trae las réplicas de R, ΔMAE por cruce con IC por réplica y el dictamen de vocabulario cerrado del piloto (vence · propuesta con reserva · nadie vence). El rótulo PROSPECTIVA/RETROSPECTIVA sale del orden de los sellos y del diff, no se elige; el dictamen no edita el sello de la celda-D. El id de cada CALC lleva `ASTRA-ENVIPE` y `ADJUDIC` (para que el comando de «hecho» lo encuentre). Bien hecho: un `sello.json` por cruce con soporte, replay afirmativo en `RESULTADO` y fila en la vista (E.7). Rama prevista: si «todo se utiliza» (05da-01) y la regla 6 resultan incompatibles para el ejecutor, la lectura de dirección cede a la firma de mesa y el resultado se rotula RETROSPECTIVA y descriptivo; si el procedimiento heredado no corre sin cambiarlo, es PARO (g) y eso es el entregable.

**P3 · recibo con red de la muestra de 10.** Produce `recibo-con-red-8c5c-08.tsv` con columnas `id_fila · fuente · url_o_doi · localizador · universo · periodo · hallazgo · estado_fila`, una fila por id de la muestra. Bien hecho: `10 10` en el comando de §1. Una fuente tras muro de pago o con acceso por solicitud pasa a receta de mesa con la fila nombrada (no se inventa el localizador).

**P4 · lectura primaria de las cinco cifras externas de consumo.** Produce `lectura-primaria-con-red-9d28-03.tsv` con la misma forma por cada cifra `externa` de `consumo-cifras.json`: localizador, universo, periodo, alcance, y si repone, confirma o mantiene retirada la cifra. Las fuentes con cuenta (McKinsey Direct, GWI) se separan como receta de mesa; ninguna se compra ni se negocia (D17/D18). Bien hecho: 5 filas. Ninguna cifra externa se promueve a evidencia de clase (a) (procedencia §3): son (b) o (c) según su muestra.

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
  e) entorno equivocado: este encargo abre microdato o corpus montado y va a CAJA; si el arranque no monta el corpus compartido, PARA en una línea (microdato se baja siempre desde CAJA)
  f) el OBJETIVO dejó de ser alcanzable o dejó de tener sentido → PARO, y eso es el entregable; leído estricto (D-19): solo sin ruta legítima
  g) el código congelado no corre → no se parcha (MODO RÍGIDO)
Enmienda de cableado (D-18): mientras el CALC no tenga `ejecucion.json`, un bloqueo de preflight de cableado puro (ruta de spec, sha de un input origen-repo, `dependencias_materiales`, constancia en lugar de archivo vivo, `permite_no_estimable`) se corrige en commit propio, declarado, y NO es PARO.

## 8 · COMPUERTAS — cada una declara qué protege
- «Abrir microdato de ENOE 2024T4 y ENVIPE 2025 solo desde CAJA con el corpus montado» protege: abrir dato (ambas olas están abiertas por MEMORIA-OPERATIVA; ENVIPE 2026 no se toca).
- «COMMIT-1 de P2 (spec + medidor + preflight VERDE) antes de tocar el microdato» protege: congelar spec.
- «Ninguna fila se cierra sin la cita a los archivos de §1» protege: borrar (una NC cerrada sin cita equivale a borrar la deuda).
- «No se adopta ni se pide adopción del resultado de C-ASTRA» protege: adoptar.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/analisis/replays-recibos-caja-1/**` · el CALC nuevo de P2 y su spec en `forense/prereg-caja/` · `forense/no-corrido.tsv` (estado, `cerrado_por`, `fecha_cierre` de las cuatro NC) · nota, ADR y fragmento L0 propios.
Ajeno que no se toca: los `CALC-ASTRA-ENVIPE-*-0001` y `CALC-TRA-EVADE-NORMA-*` sellados (se citan, no se re-miden), la celda-D `TRA.evade_norma.envipe2025.edad_x_sexo.yaml`, `forense/analisis/familias-2027-enoe-inferencia-1/diagnostico/enoe-auditoria.json` (solo se compara), las vistas `data/corrida0/*.tsv` (las publica el canal).
ARCHIVOS QUE OTRO ACTO EN VUELO ESTÁ TOCANDO (`git diff --name-only origin/main...origin/<rama>` filtrado a tools, tests, canon, libro, firmas y CI; corrido el 29/sep/2026 sobre `a7a91f41`; re-derívalo al abrir):
- `origin/acto/gen2-medicion-carriles-2--{enigh,enoe,naranja}`: `tests/test_mc2_*.py`, `tests/test_tablero_carriles.py`, `tools/tablero_carriles.py`, `tests/check.py`, `canon/gobernanza-v1_15.md`, `canon/L0/ADR-260928-GEN2-MEDICION-CARRILES-2-8fdf-0{5,6}.md`, `forense/firmas-pendientes.tsv`.
- `origin/claude/new-session-8tmg5a` (GEN2-CIERRE-Y-PRODUCTO-3): `canon/informe-programa-v1_6.*`, `canon/catalogo-del-mexicano-v1_4.*`, `canon/tabla-de-piso-v1_3.tsv`, `canon/reglas-bloque-adopcion-1.*`, `tools/cierre_acto.py`, `tools/genera_deck.py`, `tools/genera_tabla_piso_v1_3.py`, `tests/check.py`, `tests/test_cierre_acto.py`, `canon/gobernanza-v1_15.md`, `canon/registro-rotulos.tsv`, `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`.
- El PR de `GEN2-PENDIENTES-4` (#1326) mientras esté abierto (`forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`, `canon/gobernanza-v1_15.md`, `canon/registro-rotulos.tsv`, `tests/check.py`, `forense/analisis/pendientes-4/**`) y el PR [deriva] (`derivados/auto-*`, rota en cada push a main: `data/corrida0/*.tsv` y demás vistas).
Los apéndices compartidos dan conflicto de apéndice al fusionar: se conservan ambas tandas.
«Si te encuentras escribiendo fuera de esta lista, PARA.» Si te encuentras escribiendo fuera de esta lista, PARA.
PERÍMETRO DE CIERRE — permanente, no hay que pedirlo: el test propio entra a CI como HUÉRFANO (`ci_guardias --ejecuta-huerfanos`), sin editar `verify.yml` ni `check.py` (D-21) · publicar en la vista las filas propias y su asiento de replay (E.7) · registrar en INFRAESTRUCTURA la tabla propia · dejar el fragmento L0 propio en `canon/L0/<ADR-raíz>.md`, nunca en la línea `L0` compartida ni en `canon/estado-programa-v1_N.md` · la cascada de /acto · hallazgos, NC y FP propios, con ids de raíz de acto (D-24) — nunca «el siguiente número libre». Fuera del perímetro y necesario para terminar → es LATITUD (≤ 10 líneas, declarado) o es PREGUNTA. «FUERA-DE-PERÍMETRO» como razón de una NC queda para lo que de verdad es de otro acto, y se nombra ese acto.

## 10 · LO QUE NO HACE · SUCESORES · AUDITORÍA · CIERRE
Lo que NO hace: no adopta C-ASTRA ni mueve `cuenta_gen2`; no corrige `enoe-auditoria.json` ni las cifras de consumo si el replay o la lectura discrepan (se reporta y una NC/receta lleva el sucesor); no abre ENVIPE 2026 ni ninguna ola reservada; no re-mide el piloto 4; no negocia acceso a fuentes con cuenta.
Sucesores: si P1 da NO-REPRODUCE, un encargo de corrección del diseño muestral de ENOE; si P2 da «propuesta con reserva», mesa decide la firma de adopción (no este acto); recetas de mesa de P3/P4 en `GEN2-PENDIENTES-4` no se duplican: las lleva su nota.
Auditoría (afirma sobre México): ¿pobreza, violencia o informalidad confundidas con cultura en las cifras de consumo (P4)? Se lee cada cifra con su universo y su clase de evidencia (a/b/c); ninguna cantidad de unidad delito o trámite se promedia con una de unidad persona (P1 y P2 usan hogar y persona según su encuesta y no se mezclan); ¿qué cifra es PROSPECTIVA y cuál RETROSPECTIVA? (P2, por el orden de sellos); ¿cuántos contadores movió el trabajo? (la nota lo dice en una línea al inicio; si cero, también).
El cuerpo de este encargo no lleva campos para rellenar ni líneas de estado: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` las añade /acto al final del archivo archivado (A.3), nunca editando lo de arriba. Adendas de mesa recibidas durante la ejecución: archivo propio `<este-encargo>-ADENDA-N.md`, sellado al recibirse, citado sólo en el CIERRE.
