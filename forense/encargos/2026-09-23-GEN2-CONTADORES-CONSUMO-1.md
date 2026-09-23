# ENCARGO · ACTO GEN2-CONTADORES-CONSUMO-1 (lote D-11, dos piezas) · Los dos contadores que no se mueven aunque todo esté fusionado: el marcador entra al canal de publicación, y `celdas_validadas` aprende a contar las celdas-D de crédito (por conducta) y las de ENCIG 2025 (sufijo `-D-C2`)

> ENTORNO: **NUBE** — derivados, tests y CI; cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `183bb163` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-contadores-consumo-1` (D-17) · MODELO: Opus · MODO: ABIERTO (una pieza que PARA no tumba la otra) · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: cero mediciones; no adopta; `adoptados_activos` y `celdas_validadas` se mueven **solo** por sus derivadores sobre lo que mesa ya fusionó; antes/después en la nota.

## 1 · OBJETIVO
Hoy `origin/main` tiene 179 corridas selladas, la adopción ENVIPE firmada (#1002), nueve celdas-D de crédito (#1058) y dos de ENCIG 2025 (#1060), y los contadores dicen 72 y 92 porque (A) `data/corrida0/marcador-segmento.tsv` no lo publica nadie — el job de #1050 lo dejó fuera a propósito («publicarlos ahora añade 21 FAIL de línea base», FP `…DUELO-ENCIG2025-CIERRE-1-657c-04`) — y (B) `tools/celdas_validadas.py` no reconoce la clase «celda-D por conducta» de crédito ni el sufijo `-D-C2` de ENCIG (NC de #1058 y #1060, DECISIÓN-DE-MESA-PENDIENTE). Mesa ya decidió lo de fondo (D3 «que cuenten»; adopción ENVIPE #1002): esto es hacer que los contadores lean lo decidido.
«Hecho» sobre el commit final con origin/main fusionado y el siguiente PR `derivados/auto-*` fusionado: `python3 tools/corrida0.py status` en clon fresco muestra `adoptados_activos` > 72 y `celdas_validadas` > 92, con los valores que los derivadores den (citados, no tecleados) · `grep -c marcador_segmento .github/workflows/verify.yml` ≥ 1 en el paso que abre el PR de derivados · `tests/test_celdas_validadas_spec.py` VERDE con la spec humana actualizada · `check.py --baseline` VERDE sin `--force`.

## 2 · FIRMAS DE MESA
D3 (23/sep, «Que cuenten.»; FIRMAS-11) y la unidad de crédito (una celda-D por conducta del -0002; ejecutada en #1058). Adopción ENVIPE: FP `…MARGINALES-ADOPCION-1-c45c-01` FIRMADA, `decisiones.tsv` `5ef1f41`. Ninguna nueva: si (A) exige mover la línea base de `check.py`, eso es una **pregunta a mesa** con el conteo de FAIL y su causa, no una firma implícita.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` FP `…657c-04` (rama del duelo, ya en #1060): el marcador es derivado protegido, ningún PR lo lleva, y el job publicador (#1050) lo excluye con la razón de los 21 FAIL. `[LEÍDO]` nota de FIRMAS-10 l.7-12: `marcador_segmento.py --escribe` en local da 87; el mecanismo es el job de push.
- `[LEÍDO]` `verify.yml` paso «Deriva vistas y abre PR automático verificado»: corre `lote_desde_asientos.py`, `corrida0.py registro --verifica --escribe --lote`, `resuelve_citas.py tabla --escribe`; **no** corre `marcador_segmento.py`. Los tres PR `derivados/auto-*` abiertos al redactar tocan solo `corridas.tsv` y `resultados.tsv`.
- `[LEÍDO]` NO-CORRIDO de #1060: «`tools/celdas_validadas.py` no reconoce el sufijo `-D-C2`»; de #1058: «decidir si `celdas_validadas.py` se extiende con una clase» (DECISIÓN-DE-MESA-PENDIENTE). `[EXISTE]` `tests/test_celdas_validadas_spec.py` (spec vs módulo, bloqueante) y `tests/test_celdas_validadas.py` (métrica rectora en la primera línea del tablero): cualquier cambio al módulo exige cambiar su spec humana primero.
- `[SUPUESTO]` que los 21 FAIL de línea base son de tests que asertan el estado actual del marcador (RESERVADA en ENCIG, cobertura, conteos) y caen al re-derivarlo con las adjudicaciones nuevas. **Es la premisa que verificas primero en (A)**: corre el derivador en rama, `check.py --baseline`, y lista los FAIL con archivo y aserción. Si son aserciones de estado (constantes que describen el marcador viejo), se actualizan con la derivación y se declara cada una; si alguno protege una medición o decisión, PARA esa pieza y va a mesa con la lista.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`git log --oneline -3 -- data/corrida0/marcador-segmento.tsv` → reporta (última publicación). `grep -c 'C2\|conducta' tools/celdas_validadas.py` → reporta. Ramas vivas: `derivados/auto-*` (canal), ninguna toca el marcador ni `celdas_validadas.py`.

## 5 · PIEZAS
- **P-A · El marcador entra al canal.** (1) En rama: `python3 tools/marcador_segmento.py --escribe`, `check.py --baseline`; tabla de FAIL con causa (§3). (2) Corregir las aserciones de estado que describen el marcador viejo (cada una citada con su acto de origen); ninguna medición se toca. (3) Añadir `marcador_segmento.py --escribe` al paso «Deriva vistas y abre PR automático» de `verify.yml`, dentro del mismo PR `[deriva]`, y quitar la exclusión que #1050 declaró (cita la línea). (4) Con `derivados_protegidos.py`: el marcador sigue sin poder commitearse a mano; solo el job. (5) `status` antes/después en la nota; la fila `gobierno_digital × edadxescolaridad` y las dos de ENCIG 2025 dejan de decir RESERVADA por derivación (FIRMAS-9 P2 y #1060 lo esperaban).
- **P-B · `celdas_validadas` cuenta las clases nuevas.** (1) Leer la spec humana de `celdas_validadas` (la que `test_celdas_validadas_spec.py` compara) y ADR-68. (2) Añadir a la spec, antes de tocar el módulo: clase «CELDA-D POR CONDUCTA» (crédito: una celda-D = una conducta con n celdas puntuadas dentro; cuenta 1, no n — igual que el piloto 4 cuenta una por cruce; **si el piloto 4 cuenta por celda puntuada, se cuenta igual aquí y se dice**: la regla es una sola para todas) y el sufijo `-D-C2` de ENCIG 2025 como celda-D válida. (3) Módulo y test. (4) Cerrar las dos NC de #1058/#1060 y `…ESCOLARIDAD-2-0af9-02` con `DECISIÓN-DADA`.

## 6 · LATITUD
Orden libre; P-A y P-B independientes. ≤ 10 líneas adyacentes: sí. Pregunta a mesa (sigues con la otra pieza): si un FAIL de línea base protege una medición (§3) o si la spec de `celdas_validadas` obliga a elegir entre «1 por celda-D» y «1 por celda puntuada» — recomendación de dirección: la regla que ya usa el piloto 4, sin cambiarla.

## 7 · PAROS — lista cerrada
a) no aplica · b) commitear el marcador a mano, `--force`, `--excluye`, editar `registro`, o bajar una aserción que proteja una medición · c) mover contadores a mano; cambiar `champion_actual` de cualquier celda-D · d) no aplica · e) CAJA · f) ambas piezas ya están en origin/main.

## 8 · COMPUERTAS
«Spec humana de `celdas_validadas` cambia antes que el módulo» protege: **congelar** (D-15). «Marcador solo por el job; aserciones de estado actualizadas una por una con cita» protege: **adoptar** (el contador refleja adopciones firmadas y nada más). «FAIL que protege medición → mesa» protege: **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `.github/workflows/verify.yml` (solo el paso de derivados), `tools/derivados_protegidos.py` (si hace falta listar el marcador), tests con aserciones de estado del marcador (los que P-A liste), `tools/celdas_validadas.py` + su spec humana + `tests/test_celdas_validadas*.py`, `no-corrido.tsv`, `hallazgos.md`, nota, L0, cascada. Ajeno: `marcador_segmento.py` (el derivador no cambia), `corrida0.py registro`, CALC, celdas-D. En vuelo: `derivados/auto-*` (canal; se fusionan antes o se rebasa), `GEN2-ASTRA-ENVIPE-ADJUDICACION-2` (caja; no toca esto), `codex/astra3-*`.

## 10 · LO QUE NO HACE · SUCESORES
No adopta, no mide, no cambia el derivador del marcador. Sucesor: ninguno si «Hecho» se cumple; `GEN2-CONTADORES-CONSUMO-2` para lo que PARE.
