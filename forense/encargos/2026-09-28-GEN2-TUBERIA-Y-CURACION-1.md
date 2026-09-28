# ENCARGO · ACTO GEN2-TUBERIA-Y-CURACION-1 · Las letras de tubería y curación que mesa firmó el 28/sep se ejecutan en un solo lote: el marcador del canal por rango (G1), el lector de ids con la gramática de raíz de acto (H1), el tablero que cuenta registros y no líneas (H2), la guardia anti-envejecimiento de docs/index.md (H5), la prueba del auto-merge citando el run real (C2), los ejemplos congelados del motor re-sellados con dueño (F1), el rótulo ENGASTO 2012→2013 corregido en el manifiesto (D2) — y una verificación que nadie pidió pero el contador exige: por qué legacy pasó de 67 a 82 con RESUMEN-SUITE-1

> ENTORNO: **NUBE** — tubería, tests, manifiesto (solo rótulos), canon. Cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `65da69fd` (re-deriva al abrir) · una sesión, rama propia; la sesión decide los PR (un PR por grupo afín, cada uno con su ADR) · MODELO: **Opus** (H1, la verificación de legacy y F1 son juicio; G1/H2/H5/C2/D2 son receta y pueden ir en Sonnet si se separan) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0) · ids con raíz de acto (D-24) · D-21 aplica.
CONTADOR: **cero mediciones; no adopta**. Puede cambiar el valor de `dependencias_numericas_legacy_activas` **solo** si la verificación de P8 demuestra que 82 es un defecto de conteo (H1: parser que no reconoce ids con raíz), y lo declara con antes/después y la marca de definición.

## 1 · OBJETIVO — una pieza por letra, con la firma que la ejecuta
(P1) **G1 (B)**: el marcador que publica el canal se parte por rango de CALC; ningún consumidor (status, tablero, vista) asume un archivo único; test que lo prueba. (P2) **H1 (a)**: `tools/` lector de ids reconoce la gramática D-24 `<PREFIJO>-<AAMMDD>-<RÓTULO>-<hhhh>-<NN>` además de la numérica; test con un id de cada gramática; recontar los contadores que lo usan y declarar la diferencia. (P3) **H2 (b)**: el tablero cuenta registros lógicos con lector CSV (463 vs 462: el caso del hallazgo), test. (P4) **H5 (a)**: `docs/index.md` entra al mismo `git add` y guardia anti-envejecimiento que el README, en el job del canal, una línea. (P5) **C2 (a)**: la prueba del auto-merge de rutinas cita el run real del propio NC-DECISIONES-1 (#1213) por run_id y url en la nota; sin PR sintético. (P6) **F1 (a)**: los ejemplos congelados del motor (13 → 18 pruebas) se re-sellan con dueño declarado en la spec que los gobierna; el test que hoy los reporta rotos «como esperado» pasa a verde o desaparece con razón. (P7) **D2 (a)**: en `data/manifiesto.yaml`, las entradas con `url_origen` de ENGASTO 2012 que sirven 2013 corrigen el rótulo (id, usado_para) **después de verificar por id que 2012 y 2013 existen los dos**; los huérfanos `engasto2012_*` se casan; solo rótulo, ningún sha ni licencia cambia. (P8) **Legacy 67 → 82**: `git log -p` de `tools/corrida0.py` y de los TSV derivados entre `b88b92b1` y `f70eea0f`; reproducir el contador en los dos commits con el mismo comando; dictamen de vocabulario cerrado: CAMBIO-DE-DEFINICIÓN (y la marca `_definicion_desde` lo dice) · DEFECTO-DE-CONTEO (H1 u otro; se corrige aquí) · CONTEO-CORRECTO-QUE-NADIE-EXPLICÓ (15 dependencias nuevas: cuáles y de qué acto). Con salida cruda de los dos conteos.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: un test por pieza P1–P4 y P6 como huérfanos en CI, verdes · nota con run_id de C2 · `python3 -c` con lector YAML: 0 entradas ENGASTO con rótulo 2012 y `url_origen` 2013 · P8 con los dos conteos crudos y el dictamen · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
Mesa, 28/sep/2026, verbatim «firmado», sobre la línea de respuesta de la hoja v2 de dirección; INTERPRETACIÓN-DECLARADA en `2026-09-28-GEN2-TRAMITE-HOJA-FIRMAS-21-1-ADENDA-1.md` (adjunto; el acto lo archiva con el sha que calcule): «C2 a · D2 a · F1 a · G1 B · H1 a · H2 b · H5 a». Las opciones firmadas son las de la hoja de NC-DECISIONES-1 (`forense/analisis/nc-decisiones/hoja-2026-09-27.md`, letras C2, D2, F1, G1, H1, H2, H5), cuyas FP `f2e5-*` este acto marca FIRMADA con su PR (A.12: una firma que viaja en el encargo la asienta el acto). P8 no necesita firma: E.4.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `65da69fd` · `status`: `dependencias_numericas_legacy_activas=82`; a `643a8198` era 82 y a `3a7b61db` era 67; el commit entre ambos que tocó `tools/corrida0.py` es `f70eea0f` (RESUMEN-SUITE-1: «status marca definición»). No sé si es definición o conteo: P8.
- [LEÍDO] Hoja de NC-DECISIONES-1, letras C2, D2, F1, G1, H1, H2, H5: situación y opciones (verbatim en la hoja v2 de dirección, adjunto). G1: 121 CALC atrasados en el marcador; H1: el parser subcuenta un contador; H2: 463 vs 462; D2: 24 entradas ENGASTO 2012 que sirven 2013.
- [EXISTE] `tools/corrida0.py`, `tools/tablero_programa.py`, `tools/registro…` del canal, `tests/` con huérfanos, `automerge-rutinas.yml`, `data/manifiesto.yaml`.
- [REPORTADO] RESUMEN-SUITE-1 (f70eea0f) añadió la marca de definición del legacy: si lo hizo con recuento, P8 lo verá en su diff.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'TUBERIA-Y-CURACION\|TUBERIA-CONTADORES\|CI-TIEMPO-3'` → 0. Consumidos y citados: CI-TIEMPO-2 (canal por trozos: G1 se hace sobre su job), RESUMEN-SUITE-1 (resumen nocturno, T03, marca legacy), PENDIENTES-2 (guardia de estructura de TSV; H2 no la repite), CORPUS-LICENCIAS-1 (manifiesto: D2 solo toca rótulos de ENGASTO), NC-DECISIONES-1 (hoja). En vuelo: HOJA-FIRMAS-21-1 e INSTRUCCIONES-V217-1 (disjuntos), el `[deriva]` en cola (no editar vistas), PISOS-Y-ADENDAS-1 (caja; disjunto).

## 5 · PIEZAS
P8 primero (si es defecto de conteo, H1 lo corrige y el resto hereda el conteo bueno); luego P2, P1, P3, P4, P5, P6, P7. Rama prevista: si G1 exige cambiar un consumidor fuera de `tools/` (p. ej. Pages), se hace ≤ 10 líneas declarado o NC con sucesor; si D2 encuentra que ENGASTO 2012 no está por id, PARA esa pieza (premisa de dato) y sigue el lote.

## 6 · LATITUD
Agrupación en PR, orden, formato de tests: tuyos. PREGUNTA A MESA: ninguna prevista. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato · b) editar una vista a mano, un sello, una fila FIRMADA, un sha o licencia del manifiesto · c) adoptar; mover un contador sin la salida cruda de P8 · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Ningún contador cambia sin los dos conteos crudos» protege **adoptar** (E.4) · «Solo rótulos en el manifiesto» protege **borrar** · «Las vistas las publica el canal» protege **borrar** (E.7).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `tools/corrida0.py`, `tools/tablero_programa.py`, el escritor del marcador del canal, `.github/workflows/` (solo la línea de H5 y lo que G1 exija en el job de derivados), `tests/` (huérfanos), specs de ejemplos del motor (F1), `data/manifiesto.yaml` (solo id/usado_para de ENGASTO), `firmas-pendientes.tsv` (marcar FIRMADA las siete `f2e5-*`), nota, L0, cascada. Ajeno: vistas de `data/corrida0/`, `canon/`, `milpa/`, `gobierno/`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No mide, no adopta, no toca G1 fuera del marcador, no cierra `749c-03` si G1 no lo resuelve del todo (sucesor), no ejecuta B4/E3/E4 (C2) ni F3/F4/H4 (caja). Sucesores: FIRMAS-21 (asiento de lo que no ejecute este acto), `-2` si G1 deja consumidores por adaptar. Sin módulo de auditoría (no afirma sobre México). El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-TUBERIA-Y-CURACION-1-ADENDA-N.md`, selladas al recibirse.
