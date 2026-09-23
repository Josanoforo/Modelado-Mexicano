# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-11 · Asienta las siete firmas del 23/sep, cierra por verificación las NC «de mesa» que el canal y los duelos ya superaron, define INDETERMINADO, y diagnostica por qué el canal de publicación no ha commiteado en main

> ENTORNO: **NUBE** — cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `f28d1038` (re-deriva al abrir; main movido no es PARO) · una sola sesión, rama propia `acto/gen2-tramite-firmas-11` (D-17) · MODELO: Sonnet (sube a Opus para P4) · MODO: ABIERTO · ids con raíz de acto (D-24) · perímetro de cierre permanente (D-21) aplica sin enumerarlo · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: cero mediciones; no adopta; `no_corrido_abiertas` baja por cierres verificados (P2); `adoptados_activos` solo por el canal (P4), nunca a mano.

## 1 · OBJETIVO
Que las decisiones de mesa del 23/sep existan en el repo con su texto verbatim (A.12), que las NC «DECISIÓN-DE-MESA-PENDIENTE» ya resueltas por otros actos queden cerradas con su sustituto citado, que INDETERMINADO tenga definición legible, y que se sepa por comando por qué `origin/main` no muestra los 27 sellados sin fila ni el 87 de adoptados que FIRMAS-10 midió.
«Hecho» sobre el commit final con origin/main fusionado: `grep -c 'FIRMAS-11' forense/firmas-pendientes.tsv` ≥ 7 con estado FIRMADA y texto verbatim · FP `…CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01` sigue ABIERTA con `vence: 2026-09-27` en su campo · lector CSV sobre `no-corrido.tsv`: las NC de P2 en estado CERRADA con `SUSTITUIDO-POR:<acto>` o, si la verificación falla, siguen ABIERTAS y la nota dice qué objeto faltó · `grep -c INDETERMINADO docs/registro-glosario.md` (o el archivo que P3 declare) ≥ 1 · la nota de P4 cita un run de Actions por id o dice NO-ACCESIBLE con conteo.

## 2 · FIRMAS DE MESA (23/sep/2026, verbatim del chat de dirección; entran al repo por GEN2-TRAMITE-FIRMAS-11 — este encargo las cita, no las asienta)
- **D1** «Integrar los dos, nada es fuera de plazo, todo se utiliza.» (#1030 y #1031 se fusionan; las cuatro emisiones ENVIPE de Astra se adjudican contra la R del piloto 4.)
- **D3** «Que cuenten.» (las adjudicaciones de crédito entran a celdas_validadas vía celda-D)
- **D4** «A, desde ya.» (main exige check.py VERDE; merge queue; el token de Actions fusiona solo PR de rutina: `claude/encola-*`, `acto/gen2-tramite-*`, `[deriva]`; lo que mide lo fusiona mesa)
- **D5** «Ya tengo un disco duro, necesito reformatearlo para dejarlo listo, no ahora, esta semana sí; vence el domingo de esta semana.» (27/sep/2026)
- **D6** «A.» (la vía (i) de relevo lee el eje RESULTADO; CONTEXTO en la nota del pin)
- **D7** «A.» (acto de MOTOR autorizado a editar `milpa/src/motor.py` en las líneas de NC …e8fa-01; los sellos afectados se suceden por CALC nuevos)
- **D8** «A, pero que se explique claramente qué significa.» (INDETERMINADO es valor válido; se define por escrito)
- **D2** no es firma: es una pregunta de mesa («¿por qué seguimos haciendo piloto del piloto?») que contesta el encargo DUELO-ENCIG2025-CIERRE-1 con su firma §2 propuesta.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` FP ABIERTAS en TSV: 2 (`…3d56-01` respaldo; `…RECIBO-ASTRA-1-4e74-01` PR de Astra). D1 cierra la segunda como FIRMADA con texto distinto al que el recibo recomendó (#1031 sí se fusiona): A.10 — se sustituye con cita, no se edita.
- `[EJECUTADO]` `git log --author=github-actions` en main → 0 commits; `verify.yml:464-491` es el job del canal (solo push a main, `[deriva]` excluido). Desde #1028 hubo ≥ 7 push a main con asientos nuevos (#1030 trajo 2) y ninguno publicó. `[SUPUESTO]` o el job falla (registro devuelve ≠0 y el paso muere, como el propio yml describe) o el commit del bot no tiene permiso de push. Lo decide P4 leyendo los runs.
- `[LEÍDO]` nota de FIRMAS-10 l.7-12: derivador local da 87; «el mecanismo de publicación es el job de push a main»; NC `…FIRMAS-10-6980-01` nombra el sucesor. P4 es ese sucesor.
- `[LEÍDO]` Inventario v3 (`forense/encargos/fuentes/PENDIENTES-PROGRAMA-v3.md` si FIRMAS-10 lo archivó; si no, adjunto sha `36d9816cd66f8522`) §D: 36 NC con razón DECISIÓN-DE-MESA-PENDIENTE. Las de P2 las eligió dirección por objeto; **verifica cada una por id y estado antes de cerrarla (A.17)**.
- ADJUNTOS: `HOJA-DE-DECISIONES-2026-09-23.md` (sha256 `0fc5b52b57e6b365…`), se archiva verbatim en `forense/encargos/fuentes/`.

## 4 · YA HECHO / YA DECIDIDO
`ls forense/encargos | grep -c FIRMAS-11` → 0. `grep -c '23/sep\|2026-09-23' forense/firmas-pendientes.tsv` → reporta. Las NC de P2 no están cerradas (`estado` ABIERTA en TSV al redactar; **repítelo**).

## 5 · PIEZAS
- **P1 · Siete firmas.** Una fila FIRMADA por decisión (D1, D3–D8) con texto verbatim de §2, `ADR/PR` = este acto, y la referencia al objeto que cada una desbloquea (NC o FP por id). `…4e74-01` pasa a FIRMADA-SUSTITUIDA citando D1. `…3d56-01` NO se cierra: se le añade `vence: 2026-09-27` y el sucesor `GEN2-CORPUS-RESPALDO-EJECUCION-1`. D7 y D6 cierran, además, las NC que las esperaban (`…MOTOR-THETA-CONGELADA-1-e8fa-01/02`, `…RELEVO-TANDA-4-dedd-02`) con `DECISIÓN-DADA:<fila>` y sucesor nombrado.
- **P2 · Superadas, cerradas por verificación de objeto.** Para cada una, comando + salida que demuestra que el sustituto existe en origin/main, y cierre `SUSTITUIDO-POR`: `…PENDIENTES-CAJA-1-c09b-01`, `…DUELO-ENVIPE2026-EJECUCION-1-c2b4-02`, `…TUBERIA-CANAL-PUBLICACION-1-7d98-01` y `-02` → sustituto `GEN2-TUBERIA-LOTE-ESTRICTO-1` (#1028) **solo si P4 confirma que el canal funciona; si no, quedan ABIERTAS y P4 lo dice** · `…DIN-CREDITO-HISTORIA-1-ff56-01` y `-03` → `CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0002` sellado (#1012) y `GEN2-DIN-CREDITO-SERIE-LECTURA-1` (en cola o cerrado: reporta) · `…ENIGH2024-SERIE-Y-COMMIT-1-7492-01` → `CALC-ENIGH-DUELO-*` sellados · `NC-0394` → si un recibo 4/5/6 ya firmó cuenta_gen2 de RES0028-derivado, cierra citándolo; si no, fila FP nueva, no decisión.
- **P3 · Definición de INDETERMINADO (D8).** Un párrafo en el documento que gobierna el registro (`data/INFRAESTRUCTURA-v1_0.md` o el glosario que exista; si no existe, `docs/registro-glosario.md` nuevo): qué campo, qué significa (el input es METADATO, dictamen o TSV sin campo `funcion`, y el registro no puede derivar si envuelve un número GEN1), qué NO implica (no bloquea `cuenta_gen2` ni adopción), y quién lo refina (TUBERÍA al tocar `_funcion_de_dependencia`). Cierra `…C2-RESTRINGIDO-1-4e12-03`, `…IC-CALIBRADO-1-2868-03`, `…DUELO-ENVIPE2026-COMMIT-1-8796-05` con `DECISIÓN-DADA`.
- **P4 · Diagnóstico del canal.** Leer los runs de Actions de los push a main desde #1028 (`gh run list --workflow verify.yml --branch main` si hay credencial; si no, la API pública con conteo de runs leídos). Tres salidas posibles y no se colapsan: (i) el paso del canal falla (pegar la salida cruda de `registro` y la NC que corresponda: un veredicto ajeno que el guardia para, la lista de CALC) · (ii) el paso pasa pero el commit/push del bot no tiene permiso (la corrección de permisos de workflow es ≤ 10 líneas de yml: se hace y se declara) · (iii) el job nunca se disparó (condición `if` mal; ≤ 10 líneas). Si la corrección excede 10 líneas o toca `registro`, NC `DIFERIDO-A: GEN2-TUBERIA-CANAL-REPARACION-1` con lo encontrado. Nunca `--force`, nunca `--excluye`, nunca vistas a mano.

## 6 · LATITUD
Orden libre (sugerido P4 → P2 → P1 → P3, porque P2 depende de P4). Obstáculos reversibles: `pyyaml`, `gh`, regenerar derivados por comando. Pregunta a mesa solo si P4 encuentra que el canal exige una decisión (p. ej. un veredicto ajeno que hay que asentar corrida por corrida).

## 7 · PAROS — lista cerrada
a) no aplica · b) editar una fila FIRMADA existente, un sello, una vista derivada a mano, o `registro` en `corrida0.py` · c) mover `adoptados_activos` o `cuenta_gen2` a mano · d) no aplica · e) CAJA · f) los objetos ya están asentados en origin/main.

## 8 · COMPUERTAS
«P1 asienta texto verbatim de §2; no parafrasea» protege: **adoptar** (una firma parafraseada es otra firma). «P2 cierra solo con sustituto verificado por comando» protege: **borrar** (cerrar una NC sin sustituto es borrar deuda). «P4 no toca `registro` ni fuerza» protege: **borrar/reescribir**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/firmas-pendientes.tsv`, `forense/no-corrido.tsv` (append/edición de campo `estado` de las filas citadas), el documento de P3, `.github/workflows/verify.yml` solo en P4 (ii)/(iii) ≤ 10 líneas, `forense/encargos/fuentes/HOJA-DE-DECISIONES-2026-09-23.md`, nota, `hallazgos.md`, `canon/L0/<ADR-raíz>.md`, cascada. Ajeno: `tools/corrida0.py`, vistas derivadas, CALC, celdas-D, `milpa/`.
En vuelo: piloto 4 (rama, por fusionar: append en `firmas-pendientes.tsv`), tres ramas `codex/astra3-*` (no tocan TSV de gobierno), `GEN2-ASTRA-ENVIPE-ADJUDICACION-1`, `GEN2-DIN-CREDITO-CELDAS-D-1`, `GEN2-TUBERIA-RUTINAS-AUTOMERGE-2` (nube, misma tanda: append en los mismos TSV; union; `git merge-file --union` local si choca).

## 10 · LO QUE NO HACE · SUCESORES
No relanza AUTOMERGE (es -2), no registra celdas-D, no adjudica, no repara el canal si excede 10 líneas. Sucesores: `GEN2-TUBERIA-CANAL-REPARACION-1` (si P4 lo pide), `GEN2-MOTOR-LOADER-Y-RESELLO-1` (D7, lo escribe dirección con las líneas de …e8fa-01), `GEN2-CORPUS-RESPALDO-EJECUCION-1` (D5, caja, vence 27/sep).

## NO-CORRIDO / RESERVAS

- **qué:** adjunto `HOJA-DE-DECISIONES-2026-09-23.md` (sha256 `0fc5b52b57e6b365…`, §3 del encargo), archivo verbatim en `forense/encargos/fuentes/`.
  **por qué:** `NO-VERIFICABLE-AQUÍ` — el adjunto no llegó a esta sesión (verificado: ausente del directorio de uploads de la sesión). Logística, no premisa de qué se mide: las siete firmas ya están verbatim en el cuerpo del propio encargo §2, así que P1 procedió sobre esa fuente sin bloquearse.
  **impacto:** `forense/encargos/fuentes/HOJA-DE-DECISIONES-2026-09-23.md` no existe en el repo; nadie puede auditar el documento fuente completo de mesa, solo las siete firmas ya extraídas.
  **sucesor:** SIN-ASIGNAR — quien tenga el adjunto (dirección) lo archiva en un acto posterior o adenda.

- **qué:** P2 — cierre de las once NC del canal de publicación (`c09b-01`, `c2b4-02`, `7d98-01`, `7d98-04`, `0af9-01`, `009f-01`, `ef6f-01`, `9428-01`, `aa3f-01`, `ff56-01`, `ff56-03`, `7492-01`) con sustituto `GEN2-TUBERIA-LOTE-ESTRICTO-1`.
  **por qué:** `PARO-PREMISA` — la condición del encargo («solo si P4 confirma que el canal funciona») no se cumplió: P4 midió que el canal sigue caído por `GH013` en todo push desde `#1028`.
  **impacto:** las 27+ corridas selladas sin fila y `adoptados_activos` (72→87 medido por FIRMAS-10) siguen sin publicarse en la vista.
  **sucesor:** `GEN2-TUBERIA-CANAL-REPARACION-1` (NC-260923-GEN2-TRAMITE-FIRMAS-11-05da-01).

- **qué:** GEN2-DIN-CREDITO-SERIE-LECTURA-1 (sucesor citado por `ff56-01`/`-03`).
  **por qué:** `FUERA-DE-PERÍMETRO` — es acto propio con su propia cabecera y ejecución; este encargo solo lo cita al verificar `ff56-01`/`-03`, no lo ejecuta ni lo cierra.
  **impacto:** ninguno sobre este acto; se reporta que sigue EN COLA (archivado, sin `## NO-CORRIDO` ni `## CONSUMIDO`).
  **sucesor:** GEN2-DIN-CREDITO-SERIE-LECTURA-1 mismo, cuando alguien lo ejecute.

- **qué:** P4 — reparación del canal de publicación (opciones (ii)/(iii), ≤10 líneas de yml).
  **por qué:** `DIFERIDO-A:GEN2-TUBERIA-CANAL-REPARACION-1` — la causa real (regla de rama `GH013` en Settings → Rules del repositorio) no es un cambio de `.github/workflows/verify.yml`: excede el margen que P4 autoriza tocar sin PARO.
  **impacto:** el canal sigue sin publicar ninguna fila desde `#1028`.
  **sucesor:** `GEN2-TUBERIA-CANAL-REPARACION-1` (NC-260923-GEN2-TRAMITE-FIRMAS-11-05da-01).

- **qué:** todo lo demás del encargo (P1, P3, y la parte de P2 que sí verificó por objeto — `NC-0394`).
  **por qué:** ejecutado — no aplica.
  **impacto:** ninguno.
  **sucesor:** N/A.

## CONSUMIDO

Ejecutado por `/acto` sobre `forense/encargos/2026-09-23-GEN2-TRAMITE-FIRMAS-11.md`, rama `acto/gen2-tramite-firmas-11`, PR [#1049](https://github.com/Josanoforo/Modelado-Mexicano/pull/1049). ADR raíz: `ADR-260923-GEN2-TRAMITE-FIRMAS-11-05da-01`. Suite `--rapido` VERDE (0 FAIL) en cada commit de esta rama. No se fusiona en este acto: mesa fusiona.
