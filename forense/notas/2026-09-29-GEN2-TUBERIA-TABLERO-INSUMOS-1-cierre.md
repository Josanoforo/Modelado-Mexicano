# GEN2-TUBERIA-TABLERO-INSUMOS-1 · nota de cierre · 29/sep/2026

ADR `ADR-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` · NUBE (`ENTORNO-DERIVADO = NUBE`, el que declara el encargo) · base `9d2550b9` (= SHA de redacción = `origin/main` = HEAD al arrancar; `main` avanzó a `90345dff` durante el acto y se fusionó sin conflicto) · 0-bis `c6aa3615`.

Contadores: cero lecturas, cero adopciones, cero celdas (`celdas_validadas` 219 → 219, Δ0). Mueve la clasificación de NC (EN-CURSO 42 → 0; VENCIDA-CANDIDATA 0 tras dictaminar) y `no_corrido_abiertas` 334 → 324, solo por cierres con cita. `status` gana cinco líneas.

## ARRANQUE
- Guardias 0.a–0.d, crudas en la sesión: `git rev-list --count HEAD..origin/main` = 0 · `git status --porcelain` vacío · duplicado: 0 ramas con el rótulo (de 10 en `git ls-remote --heads origin`), 1 worktree (el propio), 0 PR abiertos con el rótulo (4 abiertos: #1309–#1312) · `limpia_arbol --reporta`: 1 worktree, 0 commits detrás.
- `data/raw` AUSENTE: no es paro; el acto no abre microdato ni descarga.
- Entorno: el hook imprimió `ENTORNO-DERIVADO = NUBE`, `senal-corpus: montado=NO archivos_examinados=0`, `senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, `red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403 …)`: coincide con el encargo.
- El encargo llegó **pegado en el mensaje, no como adjunto `.md`** (§0/A.3): el sello de cuerpo `b3945fbf…` cubre el texto tal como llegó.
- Modelo: el encargo sugiere Opus; D-13 solo impide bajar en actos que miden y este no mide.

## Premisas del encargo, por rótulo
| premisa (§3) | rótulo | resultado | comando |
|---|---|---|---|
| `suite-resumen.tsv` ausente; 0 commits; sin rama de resumen | EJECUTADO | se sostiene | `ls data/derivados/suite-resumen.tsv` → no existe · `git log --all --oneline -- data/derivados/suite-resumen.tsv \| wc -l` → 0 · `git ls-remote --heads origin \| grep -ic resumen` → 0 |
| verify.yml:104-115 y 785-830 | LEÍDO | se sostiene | leí 96-120 y 775-862 |
| 42 filas EN-CURSO de cuatro actos con encargo CONSUMIDO y rama no viva | EJECUTADO | se sostiene | `nc_por_clase.py --json` → 42; los cuatro encargos traen `## CONSUMIDO`; sus ramas no están entre las 10 de `git ls-remote --heads origin` (fusionados: #1299, #1304, #1302, #1294) |
| «19 de 27 ADQUISICION sin SOLICIT ni FP» | EJECUTADO | **no se reproduce**: 21 (sucesor sin `SOLICIT` ni id de FP), 15 (sin distinguir mayúsculas), 26 (gramática nueva) | ver P4 |
| «18 de 18 APERTURA sin FP»; f18c-04 SIN-ASIGNAR | EJECUTADO | se sostienen | `nc_por_clase.py --json` |
| `status` sin fecha de vista; último [deriva] 28/sep 10:20; `derivados/auto-36495085433` en cola | EJECUTADO | se sostenía al arrancar; hoy #1309 está cerrado («Superado por #1315») y el [deriva] vivo es #1315 | `git log --first-parent -1 --format='%H %cI' --grep='^\[deriva\]' -- data/corrida0/usos.tsv` → `1f4bf1cc… 2026-09-28T10:20:35-06:00` |
| MEMORIA §5 da `canon/TABLERO-PROGRAMA.md`, que no existe | LEÍDO | se sostiene; corregida | `ls canon/TABLERO-PROGRAMA.md` → no existe; el tablero vive en `forense/tablero/` |
| SIN-UNION stopper ADQUISICION en 31 de 31 carriles | EJECUTADO | se sostiene (y 7 ROJO, 15 con SIN-UNION como siguiente) | `python3 forense/analisis/tablero-insumos-1/simula_opcion_b.py` |
| «el nocturno no corrió o falló desde #1224» | SUPUESTO | **falsa**: corrió y publicó su PR; ver P2 | API de Actions (solo lectura) |

## P1 · la fecha de la vista, en `status`
`status` imprime ahora, además de lo de antes, cinco líneas (tools/corrida0.py, `_vista_publicada()`):

```
vista_publicada_commit=1f4bf1cc319c5836e2e09b3619b5696b70d546df
vista_publicada_fecha=2026-09-28T16:20:35Z
vista_publicada_commits_posteriores=26
deriva_en_cola=1
deriva_en_cola_fuente=refs/remotes/origin/derivados/auto-* sin red; ultimo fetch de este clon 2026-09-29T00:15:17Z
```
(salida cruda de `python3 tools/corrida0.py status` completo, 3 min 34 s; `commits_posteriores` sube con cada PR fusionado.) Se derivan del historial de HEAD y de las refs locales de `origin`, **sin red y sin escribir** (D-23): la vista publicada es el último commit de la primera línea de HEAD con `[deriva]` (asunto de un squash o cuerpo de un merge de mesa) que cambió `data/corrida0/usos.tsv`; una edición a mano de esa vista no cuenta. Si el clon es superficial y el único candidato es el borde, o no trae refs de `origin`, o es de una sola rama (el checkout de CI no ve `derivados/auto-*`), se declara `NO-VERIFICABLE-CLON-SUPERFICIAL` / `-SIN-REFS-DE-ORIGIN` / `-CLON-DE-UNA-RAMA` en vez de un cero. Cubierto por `tests/test_tablero_insumos.py` (A) sobre repos git sintéticos, con un clon `--depth 1` real. El puesto que solo quiere la fecha sin esperar el `status` completo puede llamar `corrida0._vista_publicada()` (0.2 s).

## P2 · por qué no hay resumen de la suite en main
El SUPUESTO del encargo era falso. Reconstruido con la API de Actions (solo lectura) y el timeline público del PR:
1. El nocturno **sí corrió**: `schedule` del 27/sep (run 36326473274, `success`, sobre `1c7b840a` = #1213, **anterior** a #1224 que trajo el job) y del 28/sep (run 36458154737, `success`, sobre `06099042` = #1273).
2. En el del 28/sep, `suite` terminó `success`, el paso «Resumen de la suite» construyó el TSV y el job `resumen-suite` (26 s, `success`) abrió el **PR #1278** «[deriva] resumen de suite VERDE @ 06099042» con `data/derivados/suite-resumen.tsv` como único archivo.
3. La suite de ese PR (dispatch 36459019121) salió ROJA por **un solo FAIL nuevo, T27**: «`data/derivados/suite-resumen.tsv`: archivo nuevo bajo `data/` sin cita en `data/INFRAESTRUCTURA-v1_0.md`». Reproducido en local: con un resumen sintético, `check.py --rapido` da `1 FAIL · T27` sin la cita y `0 FAIL` con ella.
4. Mesa cerró el PR sin fusionar a las 17:38:00Z y se borró la rama (`closed` + `head_ref_deleted`, actor `Josanoforo`, cero comentarios), con la suite todavía corriendo.
5. T27 no lo atrapó en el PR del acto (#1224) porque el TSV lo crea el job en CI: no existía en el árbol de ese PR. Una tabla que solo el CI crea la tiene que registrar el acto que define el job (D-21); no se registró.

**Corrección** (D-21, «registrar sus tablas»; seis líneas): sección de `data/derivados/suite-resumen.tsv` en `data/INFRAESTRUCTURA-v1_0.md`, junto a las vistas del registro (no al final: #1313 inserta ahí). **Lo que sigue sin ser de este acto:** (i) el cron del nocturno es `0 9 * * *`: para que el de hoy no repita T27, este PR debe estar en `main` antes; (ii) aun con T27 resuelto, el PR del resumen se verifica por `workflow_dispatch` y `automerge-rutinas.yml` no dispara sobre esos runs (0 runs de auto-merge en `derivados/auto-36495085433` tras dispatch `success`; TUBERIA-3: «los eventos creados con `GITHUB_TOKEN` no encadenan `workflow_run`»): mesa lo fusiona a mano mientras la FP f18c-01 siga ABIERTA (P5); (iii) tras fusionar este PR: Actions → Run workflow (`verify.yml`) sobre `main`. El criterio (2) del «hecho» se cumple por su segunda vía, «el acto documenta por qué el nocturno no lo publicó».

## P3 · cierre hacia atrás de los cuatro actos
Mecánica (`tools/nc_por_clase.py`): un dueño `EN-CURSO (<acto> · rama <rama>)` cuyo encargo está `## CONSUMIDO` y cuya rama ya no vive en `origin` (`git ls-remote --heads origin`, solo lee; sin red no se adivina: `--sin-red` deja la fila EN-CURSO y lo declara) es `VENCIDA-CANDIDATA`: candidata, no cierra nada. Medido con la herramienta antes de dictaminar: **42 de 42** EN-CURSO pasaron a VENCIDA-CANDIDATA. Los cuatro actos: TUBERIA-3 (#1294), CALC-ALTERNOS-LOTE-1 (#1299), C1-SUCESORES-Y-LOTE-3 (#1304), PISOS-DOMINIOS-Y-REGLAS-1 (#1302), los cuatro con `## CONSUMIDO` y sin rama viva.

Las 42 se dictaminaron **por objeto** con tres subagentes de solo lectura (uno por grupo: TUBERIA-3 19, C1-SUCESORES 15, CALC-ALTERNOS + PISOS 8), con contrato de salida en TSV (`dictamen`, texto listo para el libro, `comando`, `esperado_en_salida`, confianza). **Cada comando de evidencia lo re-ejecuté yo antes de escribir el libro** y leí completos los 42 textos y su evidencia; el conjunto de evidencia (87 filas con P4) se reproduce con `python3 forense/analisis/tablero-insumos-1/reejecuta_evidencia.py forense/analisis/tablero-insumos-1/*.tsv` (0 fallas; solo lee y compara el árbol antes/después). Verifiqué además por mi cuenta la cita de la API en `c6d9-05` (run del push de #1294: `check` de 22:54:25Z a 23:02:06Z = 7 min 41 s) y los nocturnos.

Resultado: **14 cerradas con cita** (6 `CERRADA` con producto y comando; 8 `CERRADA-POR-DISEÑO`: firma FIRMADA y ejecutada, o duplicada) y **28 siguen ABIERTA con dueño vivo**: MESA 26 (13 de TUBERIA-3 —12 con la FP f18c-01: sus CALC están sellados y asentados pero sin fila en `corridas.tsv`—, 8 de C1, 5 de CALC-ALTERNOS/PISOS) y CAJA 2 (con el encargo de aislamiento ya archivado). Ninguna quedó EN-CURSO ni se reasignó a un acto sin encargo archivado. Confianza: 0 BAJA, 15 MEDIA (juicio, no comando; motivo en la columna `evidencia`), el resto ALTA.

## P4 · dueños completos y guardia
Gramática (`nc_por_clase.py`, con la definición que un lector puede reproducir): el dueño vigente (lo anterior a ` · antes:`) de una fila ADQUISICION nombra su solicitud si cita un objeto que **existe hoy** —`cola:<fuente_canonica>` de `data/cola-adquisicion-v1_0.tsv`, una solicitud a-g de OBTENCION-EXTERNA-1 o un expediente de acceso (`.md`), `obtencion:<pieza>:<fuente>`, o una FP existente—; una fila APERTURA, si cita una FP existente. La vista derivada ahora dice qué nombra cada fila y su estado (`FP-… [FIRMADA]`), o el hueco (`SIN-SOLICITUD`, `SIN-FP`). Medido antes: 26 de 27 ADQUISICION y 18 de 18 APERTURA no nombraban un objeto existente (44 filas con esta definición; 38 con el conteo del encargo, que no se reproduce: ver premisas).

Investigación por objeto con dos subagentes de solo lectura (ADQUISICION: cola 952 filas, obtención 179, solicitudes 9, expedientes 8 y 647 FP examinados; APERTURA: tablero de 647 FP), con el mismo contrato y la misma re-ejecución de cada comando:
- **ADQUISICION (27):** 13 reescritas para nombrar su solicitud, 1 (`NC-0111`) ya la nombraba, **13 excepciones** («nadie ocupó la fila»: no hay fila de cola, solicitud, expediente ni FP que sostenga la adquisición; cada una declara el universo examinado). `…LICENCIAS-1-1997-01` no se edita porque la modifica el PR #1312: queda como excepción.
- **APERTURA (18):** 9 nombran una FP existente —**las 9 están FIRMADA**, señal de que la fila probablemente ya no espera una apertura— y **9 excepciones**: ninguna FP abre esa ola (la reserva la levanta un pre-registro futuro o mesa por escrito, E.6). **No se acuñó ninguna FP nueva:** eran siete pendientes nuevos de mesa (N1–N7, con texto y opciones en `resultado-p4-apertura.tsv`) que dirección no revisó (D-19) y que `GEN2-APERTURAS-PREREGISTRADAS-1` (PR #1313, en vuelo) inventaría.
- `f18c-04` (SIN-ASIGNAR) y `f18c-01` (fuera de la lista) pasan a `MESA (2026-10-05)` con la FP f18c-01; `f18c-04` dice cómo se verifica: `vista_publicada_fecha` posterior a 2026-09-28T22:54:21Z (merge de #1294) y `status` contra `corrida0 demanda` (pendientes 63).

**Guardia huérfana** `tests/test_tablero_insumos.py` (censada, CORRE-EN-CI, 1 s; D-14: el defecto real ya ocurrido son esas filas sin dueño real y al lector le costaba no saber de qué objeto dependía cada una): (A) fecha de la vista sobre repos git sintéticos, (B) VENCIDA-CANDIDATA, (C) gramática de dueños completos, (D) el libro real: **lista cada excepción por id con su razón (22)** y falla si una fila **nueva** (fecha ≥ 2026-09-29) incumple; las anteriores solo avisan, para no romper a los actos que ya iban en vuelo (hoy avisa de `…MEDICION-CARRILES-2-8fdf-04`, de otro acto).

## P5 · DECISIÓN-DE-MESA-PENDIENTE
`FP-260928-GEN2-TUBERIA-3-f18c-01`: `estado=ABIERTA`, `firmada_en` vacío (`python3 tools/consulta.py fp FP-260928-GEN2-TUBERIA-3-f18c-01`). La «hoja de mesa del 28/sep, renglón 1» que cita el encargo no está en el repo: `f18c-01` aparece en 11 archivos y ninguno la marca firmada. **Sin firma, P5 queda DECISIÓN-DE-MESA-PENDIENTE** (§2 del encargo). No se tocó `automerge-rutinas.yml`: implementar (a) es fusionar sin revisión humana, regla de mesa (TUBERIA-3 lo intentó y el clasificador de permisos lo negó; tampoco se rodeó aquí). Lo que queda listo para quien implemente lo que mesa firme: el síntoma **re-medido** (0 runs de auto-merge en la rama `derivados/auto-36495085433` con dispatch `success`; run del push de #1294: `check` en 7 min 41 s), la causa probable (los eventos que crea `GITHUB_TOKEN` no encadenan `workflow_run`) y las cuatro condiciones que el auto-merge ya exige y que (a) debe conservar: rama o commit `[deriva]`, `suite` verde sobre el mismo SHA, diff sin `forense/prereg-caja/`, PR abierto y mergeable. NC nueva `…c6aa-01` (sucesor MESA + FP).

## §5-bis · para mesa (texto de firma listo)
Estado re-verificado (A.17) con `python3 forense/analisis/tablero-insumos-1/simula_opcion_b.py` (solo lee): SIN-UNION es stopper ADQUISICION en **31 de 31** carriles, 7 son ROJO (CARRIL-02, 03, 08, 09, 13, 17, 22) y en **15** SIN-UNION es la siguiente acción. Con (b) esos 15 cambian (6 → LISTO, 3 → familia 2027, 3 → otro stopper de ADQUISICION, 3 → NC-PARO): el «unos 15» del encargo se sostiene. **Matiz que el encargo no decía:** dos de los 15 son ROJO (CARRIL-13 y CARRIL-17) y quedarían con siguiente = LISTO pese al rojo; «Costo: bajo» debe leerse con eso. Recomendación de dirección, sin cambio: (b) ahora y (c) como acto propio con spec. **No se cambió `tools/tablero_carriles.py`** (§10 del encargo: sin firma de 5-bis no se cambia la regla; ninguna vino verbatim). FP `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` ABIERTA, con el texto de firma listo: «Firmo la opción (b) para tools/tablero_carriles.py.» Sucesor si mesa elige (c): un acto con spec propia (sin encargo archivado hoy: línea en `forense/hallazgos.md`, no NC).

## P6
(1) `canon/MEMORIA-OPERATIVA.md` §5 apuntaba a `canon/TABLERO-PROGRAMA.md`, que no existe; el tablero vive en `forense/tablero/TABLERO-PROGRAMA.md` (y `TABLERO-CARRILES.md`, que también se cita ahora). (2) `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-02` pasa a dueño **`DIRECCION`**: lo que espera es un encargo por escribir (cambiar el chequeo 0.c de `.claude/commands/acto.md` por uno por contenido). **Interpretación declarada:** «reasignar a dirección» = ampliar en uno la lista cerrada de dueños de PENDIENTES-3 (`MESA · CAJA · ADQUISICION · APERTURA · EN-CURSO` + `DIRECCION`, clase `ESPERA-DIRECCION` en `nc_por_clase.py`); la alternativa descartada era dejarla MESA con «dirección» en la prosa, que reproduce el defecto (el dueño real solo en prosa, A.16). D-21: la regex de la prueba manual `tests/test_nc_cierre_hacia_atras.py --libro` se amplió en una línea. **Para mesa/dirección:** 173 NC ABIERTA traen «encargo por escribir» en su dueño vigente y siguen rotuladas MESA (convención de PENDIENTES-3); pasarlas a `DIRECCION` sería una pasada de una línea y cambiaría cuántas «esperan a mesa» (decisión de dirección, no de este acto).

## «Hecho», por comando
Sobre el árbol final con `origin/main` fusionado (`git rev-list --count HEAD..origin/main` = 0 tras `git fetch --prune`). Salida cruda.

**(1)** `python3 tools/corrida0.py status` (3 min 38 s; `real 3m38.986s`), líneas pedidas y vecinas:
```
no_corrido_abiertas=324
celdas_validadas=219
vista_publicada_commit=1f4bf1cc319c5836e2e09b3619b5696b70d546df
vista_publicada_fecha=2026-09-28T16:20:35Z
vista_publicada_commits_posteriores=38
deriva_en_cola=1
deriva_en_cola_fuente=refs/remotes/origin/derivados/auto-* sin red; ultimo fetch de este clon 2026-09-29T00:31:04Z
```
Las tres del criterio están (`vista_publicada_commit`, `vista_publicada_fecha`, `deriva_en_cola`). `celdas_validadas` = 219 = el valor de arranque (Δ0).

**(2)** `python3 tools/resumen_suite.py lee`:
```
suite: sin resumen publicado (data/derivados/suite-resumen.tsv ausente)
```
No imprime un estado: se cumple por la segunda vía del criterio, «el acto documenta por qué el nocturno no lo publicó» (§ P2: el nocturno corrió y publicó el PR #1278; T27 lo puso rojo; mesa lo cerró sin fusionar). Residual: NC `NC-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-03`.

**(3)** `python3 tools/nc_por_clase.py --json` (con red: `ramas_vivas` = «git ls-remote --heads origin: 8 ramas»; universo «324 filas ABIERTA de 1096 en forense/no-corrido.tsv»):
```
{'ESPERA-MESA': 269, 'ESPERA-ADQUISICION': 27, 'ESPERA-DIRECCION': 1, 'ESPERA-APERTURA': 18, 'ESPERA-ACTO-NOMBRADO': 8, 'ESPERA-FIRMA': 1}
EN-CURSO: 0 | VENCIDA-CANDIDATA: 0
```
Ninguna fila EN-CURSO cuyo acto tenga el encargo CONSUMIDO y la rama no viva (antes: 42 EN-CURSO). La clase EN-CURSO ya no existe entre las abiertas porque las 42 se dictaminaron; hacia adelante, una fila así saldría VENCIDA-CANDIDATA (probado en `tests/test_tablero_insumos.py` (B)).

**(4)** `python3 tests/test_tablero_insumos.py` (sale 0; imprime cada excepción por id, 22, y el resumen):
```
ADQUISICION: 27 ABIERTA · 13 sin solicitud ni FP | APERTURA: 18 ABIERTA · 9 sin FP | fuera de la lista cerrada: 1 | excepciones declaradas: 22
OK test_tablero_insumos (A-D)
```
Cada fila ADQUISICION nombra su solicitud y cada APERTURA su FP, **o** su excepción está listada por id (22) por la guardia huérfana (censada en `forense/analisis/ci-guardias/censo-tests.tsv`: 283 tests = 283 filas). La fila «fuera de la lista cerrada» (`…MEDICION-CARRILES-2-8fdf-04`) es de otro acto y anterior a 2026-09-29: avisa, no adjudica.

**Suite:** `python3 tests/check.py --rapido` sobre el árbol de cierre: `0 FAIL · 459 WARN` en 5.2 s (T25 `T-ROTULOS` ok; el sello del cuerpo del encargo CASA; los WARN son el libro de deuda y las FP abiertas, no adjudican, D-16). La suite completa no se corre desde NUBE (§10): la juzga el CI del PR.

## Límites declarados
1. Los dictámenes de P3/P4 los investigaron subagentes; yo re-ejecuté cada comando y leí los textos, pero 15 de los 42 de P3 y varios de P4 descansan en juicio (marcados MEDIA/BAJA en la evidencia). Dos citas (`c6d9-05`, `a387-04`) dependen de la API de Actions y no se reproducen sin red; el comando sin red solo muestra el cron.
2. `deriva_en_cola` sale de las refs locales del último fetch (declarado en `deriva_en_cola_fuente`): un clon con el fetch viejo ve una cola vieja.
3. **No se corrió la suite completa** (§10 del encargo: no desde NUBE); el juez es el CI. Sí: `check.py --rapido` (0 FAIL), `test_tuberia3.py`, `test_corrida0.py`, `test_celdas_validadas_spec.py` y `test_escribe_relevo_consumidores3.py` (47 pruebas que usan `status()`), los sidecars y el test nuevo.
4. P5 no se implementó ni se rodeó (sin firma); §5-bis no se aplicó (sin firma). No mueve lecturas, adopción ni celdas.
5. Escrituras fuera de la lista «Propio» del §9, declaradas: una línea en la regex de `tests/test_nc_cierre_hacia_atras.py` (D-21, defecto adyacente); `data/INFRAESTRUCTURA-v1_0.md` (la tabla que P2 pide registrar), `forense/analisis/tablero-insumos-1/` (evidencia propia y el re-ejecutor), la fila del censo de `ci_guardias`, `forense/hallazgos.md`, `forense/firmas-pendientes.tsv` (FP de §5-bis, A.12), y `bloqueos.tsv` (registro que escribe el hook). Ningún archivo `DERIVADO — NO EDITAR` se tocó (`nc-abiertas-por-clase.tsv` sigue con la derivación de 27/sep).
6. El `merge` de `origin/main` con `merge=union` reintrodujo una copia vieja de `…f18c-04` (id duplicado, T47); se quitó a mano y CI la habría atrapado.
7. Filas de otros actos en vuelo que no se tocaron: `…LICENCIAS-1-1997-01` (PR #1312). Las 173–177 «encargo por escribir» siguen MESA (hallazgo).
8. Para que el nocturno de hoy no repita T27, este PR debe estar en `main` antes de las 09:00 UTC.
