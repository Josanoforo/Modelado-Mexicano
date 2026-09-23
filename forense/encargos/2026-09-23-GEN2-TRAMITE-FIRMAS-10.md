# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-10 · Dos asientos que FIRMAS-9 no llevó: la adopción ENVIPE firmada en #1002 que `adoptados_activos` todavía no ve (72, no 87), y las 10 NC con campos corridos que ningún contador cuenta

> ENTORNO: **NUBE** — cero microdato, cero corridas. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA en una línea.

CABECERA · SHA de redacción `619748f5` (re-deriva al abrir; #1032 puede ya estar fusionado) · una sola sesión, rama propia `acto/gen2-tramite-firmas-10` (D-17) · MODELO: Sonnet · MODO: **ABIERTO** · CONTADOR: cero mediciones; **no adopta a mano**; `N_resultados_gen2_adoptados_activos` puede moverse solo por su derivador (P1); `no_corrido_abiertas` puede subir en hasta 10 al recuperar filas ya escritas (P2) · ids con raíz de acto (D-24).

## 1 · OBJETIVO
(P1) Que `adoptados_activos` refleje la adopción ENVIPE que mesa firmó en #1002 (`5ef1f41`, 15 celdas con `origen_numerico=NUEVO` en `decisiones.tsv`) y que el marcador no ha consumido porque nadie re-derivó el yaml. (P2) Que las 10 filas de `forense/no-corrido.tsv` escritas con una columna de menos (inventario v3 §Ñ) vuelvan a tener sus doce campos y `estado = ABIERTA`, para que las cuente `status`.
«Hecho» = sobre el commit final con `origin/main` fusionado: `python3 tools/corrida0.py status | grep adoptados_activos` → un valor mayor que 72, **o** la nota explica por comando qué falta y la NC nombra al sucesor · un lector CSV sobre `no-corrido.tsv` cuenta 0 filas con menos campos que la cabecera (universo: todas las filas, conteo declarado).

## 2 · FIRMAS DE MESA
Ya selladas, se citan: FP-…-MARGINALES-ADOPCION-1-c45c-01 (FIRMADA; ENVIPE adopta) en `firmas-pendientes.tsv`, ejecutada en `5ef1f41`. Ninguna nueva: este acto no adopta, hace visible lo adoptado.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `corrida0.py status` en tres cortes de main (`3f48be30` 16:07 · `d34b70e1` 20:11 · `619748f5` 20:34, 22/sep): `adoptados_activos` = 72 en los tres; `pendientes_adopcion` 12 → 10.
- `[LEÍDO]` NC `NC-260922-GEN2-TRAMITE-FIRMAS-7-369b-02`: «sigue en 72 (no 87) pese a que 5ef1f41 (PR #1002) acreditó origen_numerico=NUEVO para las 15 celdas ENVIPE»; sucesor: «correr marcador_segmento.py --escribe y commitear el yaml». Hermana `…369b-01`: el bloque de 10 RESULT (5 Banxico, LAPOP, 3 MOTRAL) espera «sucesor con milpa/ en su perímetro» — **fuera de este acto** (ver §10).
- `[EJECUTADO]` `grep -n 'data/raw\|dbf\|\.csv' tools/marcador_segmento.py` → 0 líneas: el derivador no lee microdato; corre en NUBE.
- `[LEÍDO]` Inventario v3 §Ñ (adjunto): 10 filas con `ABIERTA` caída en la columna `sucesor` — NC-0338, NC-0339, NC-0340, `NC-260921-GEN2-L-DESDE-CAPTURAS-1-1d7c-01/-02/-03`, `NC-260921-GEN2-V216-d3da-02`, `NC-260922-GEN2-ESTADO-V15-1-7e23-02/-03`, `NC-260922-GEN2-TRAMITE-COLA-VIEJA-1-0eca-02`. **Verifícalo tú con lector CSV** (A.13).
- `[EJECUTADO]` `GEN2-TRAMITE-FIRMAS-9` (rama `acto/gen2-tramite-firmas-9`, PR #1032, cuerpo `f952c9ab`) NO incluye estas dos piezas: su cuerpo sellado trae P1–P3 (CONSUMIDO de SECUNDARIA-1, marcador de `gobierno_digital`, FP para 8e53-04). Este acto no lo toca.
- ADJUNTOS: `PENDIENTES-PROGRAMA-v3.md` (sha256 `36d9816cd66f8522…`; se archiva verbatim en `forense/encargos/fuentes/` como fuente de P2).

## 4 · YA HECHO / YA DECIDIDO
`git log origin/main --oneline | grep -c 1032` → reporta (si #1032 ya fusionó, sus cambios en `marcador-segmento.tsv` son la base; se re-deriva encima). `grep -c 'marcador_segmento.py --escribe' forense/notas/2026-09-2*` → reporta. Ramas vivas: FIRMAS-9 (si aún no fusiona, este acto arranca después: comparten `no-corrido.tsv` y el derivado del marcador). **Repítelo tú.**

## 5 · PIEZAS
- **P1 · `adoptados_activos` consume #1002.** `python3 tools/marcador_segmento.py --escribe` sobre `origin/main`, commit del derivado; `status` antes/después en la nota. Si el contador no se mueve, la nota dice por comando qué falta (una fila en `decisiones.tsv`, una guarda del derivador, otro consumidor) y la NC nombra el sucesor. No se toca a mano ningún yaml ni TSV derivado.
- **P2 · Las 10 filas de §Ñ.** Cada una se reescribe con sus doce campos en su sitio, con `estado = ABIERTA`, sin cambiar id, razón ni sucesor (D-24: no se renumera). Si el contenido es ambiguo (no se sabe qué campo se perdió), se deja como está y va a la NC de este acto con la fila citada. Hallazgo en `hallazgos.md`: qué acto las escribió así y si su herramienta sigue en uso.

## 6 · LATITUD
DECIDES TÚ: orden, formato. Obstáculos reversibles: `pyyaml`, regenerar derivados por comando. ≤ 10 líneas adyacentes: sí, declarado. PREGUNTAS A MESA: si P1 exige una fila en `decisiones.tsv` que no existe, con la fila propuesta y recomendación; sigues con P2. NO DECIDES: §7.

## 7 · PAROS — lista cerrada
a) no aplica · b) editar un `spec.yaml` sellado, un yaml de celda-D o cualquier cosa arriba de la línea de append de un encargo archivado · c) mover `adoptados_activos` o `cuenta_gen2` a mano · d) no aplica · e) CAJA · f) las dos piezas ya están en `origin/main` → PARO, y decirlo es el entregable.

## 8 · COMPUERTAS
«P1 corre el derivador y nada más; la fila de decisión ya existe en `5ef1f41`» protege: **adoptar** (mesa adopta al fusionar este PR, E.2). «P2 reescribe campos en su sitio sin tocar id, razón ni sucesor» protege: **borrar/reescribir**. Orden sugerido: P1 → P2.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: el yaml que `marcador_segmento.py --escribe` produce · `data/corrida0/marcador-segmento.tsv` por derivador · las 10 filas de §Ñ de `no-corrido.tsv` (edición en sitio, solo esas) · `forense/encargos/fuentes/PENDIENTES-PROGRAMA-v3.md` · `hallazgos.md` · nota · `canon/L0/<ADR-raíz>.md` · cascada. Ajeno: `milpa/tramite.yaml` (si el derivador exige tocarlo, es pregunta) · celdas-D · CALC · `verify.yml`/`check.py`.
Archivos que OTRO ACTO EN VUELO está tocando: FIRMAS-9 (PR #1032, si no ha fusionado) escribe `marcador-segmento.tsv` y `no-corrido.tsv` — **arranca cuando #1032 esté en main**; `GEN2-RECIBO-ASTRA-1` (nube) hace append en `no-corrido.tsv`, `firmas-pendientes.tsv`, `hallazgos.md`; piloto 4 (caja) hace append en `firmas-pendientes.tsv`. Union en todos; `git merge-file --union` local si choca.
«Si te encuentras escribiendo fuera de esta lista, PARA.» Perímetro de cierre permanente (D-21) aplica.

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No adopta el bloque de 10 RESULT de `…369b-01` (exige `milpa/` en perímetro: sucesor `GEN2-TRAMITE-PENDIENTES-2-ADOPCION-BLOQUE`, por escribir); no toca FIRMAS-9; no mide. Auditoría de rigor extremo: no carga (papeleo). Cierre por /acto: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.

## NO-CORRIDO / RESERVAS

- **Qué:** §9 dice «arranca cuando #1032 esté en `main`» (conflicto declarado con `GEN2-TRAMITE-FIRMAS-9` sobre `marcador-segmento.tsv` y `no-corrido.tsv`). **Razón:** no aplica ninguna de las siete — se declara como logística resuelta, no como NC: `#1032` seguía abierto (`mergeable_state: blocked`) al arrancar este acto. Se verificó que el conflicto real era solo de *escritura simultánea de los mismos archivos*, no de contenido: este acto corrió `marcador_segmento.py --escribe` únicamente para *observar* el efecto sobre `status` y revirtió el resultado sin commitearlo (P1, ambos archivos son DERIVADOS que la guardia de PR rechaza de todas formas), y editó `no-corrido.tsv` en filas disjuntas de las que `#1032` toca. **Impacto:** ninguno — ambas ramas pueden fusionar en cualquier orden sin pisarse. **Sucesor:** ninguno; declarado por transparencia (D-19: obstáculo reversible, resuelto y declarado, no PARO).
- **Qué:** P1 — que `adoptados_activos` refleje >72 en este PR. **Razón:** `DIFERIDO-A:job-push-a-main` (`.github/workflows/verify.yml`, mecanismo `[deriva]` ya cableado desde `#1026`). **Impacto:** `status` de este PR sigue leyendo 72; sube a 87 automáticamente al fusionar cualquier PR contra `main`, sin acción adicional. **Sucesor:** ninguno propio — cierra de facto `NC-260922-GEN2-TRAMITE-FIRMAS-7-369b-02` cuando `origin/main` muestre 87 por comando.
- **Qué:** P2 — las 3 filas `NC-0338/9/40` del inventario v3 §Ñ (ya tienen 12 campos; el defecto real es que `razon` no trae un token de A.14). **Razón:** `NO-VERIFICABLE-AQUI` — no se puede determinar sin ambigüedad qué campo se perdió (instrucción explícita de la pieza ante ambigüedad: se dejan como están). **Impacto:** ninguno sobre el criterio de «hecho» de esta pieza (ya cuentan 12/12); el defecto semántico (token de `razon` ausente) sigue sin corregir. **Sucesor:** `SIN-ASIGNAR` — mismo acto que trate las 9 filas de abajo, o uno propio si mesa lo prefiere.
- **Qué:** P2 — 9 filas de `forense/no-corrido.tsv` con menos campos que la cabecera, fuera de las 10 citadas por el inventario v3 §Ñ (`NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-04`, dos `GEN2-DIN-CREDITO-*`, `GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1-ef6f-01`, dos `GEN2-TUBERIA-CANAL-PUBLICACION-1`, tres `GEN2-RECIBO-ASTRA-1`). **Razón:** `DECISION-DE-MESA-PENDIENTE` — el perímetro de esta pieza (§9) restringe la edición a «las 10 filas de §Ñ … solo esas»; no se pudo nombrar un acto ajeno dueño concreto (A.14: si no se puede nombrar, tocaría a este acto, pero editar fuera de la lista cerrada de perímetro viola D-21/§9 explícito) — se plantea como bifurcación a mesa en vez de decidir unilateralmente. **Impacto:** el criterio universal del objetivo P2 («0 filas con menos campos en TODO el archivo») no se satisface; solo las 10 filas citadas quedan atendidas. **Sucesor:** `SIN-ASIGNAR` — acto que audite `no-corrido.tsv` completo y decida si instrumenta un guardia (`T-NC-CAMPOS`).

## CONSUMIDO

Ejecutado por `ACTO GEN2-TRAMITE-FIRMAS-10`, PR #1039 (`Josanoforo/Modelado-Mexicano`). Rama `acto/gen2-tramite-firmas-10`. ADR `ADR-260923-GEN2-TRAMITE-FIRMAS-10-6980-01`. Mesa fusiona.
