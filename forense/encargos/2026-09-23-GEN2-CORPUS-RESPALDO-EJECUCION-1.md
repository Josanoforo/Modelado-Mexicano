# ENCARGO · ACTO GEN2-CORPUS-RESPALDO-EJECUCION-1 · El respaldo del corpus (19.8 GB verificados) sale del disco del corpus al disco externo de mesa, con los cuatro comandos ya escritos y verificación de hash al final — vence el domingo 27/sep

> ENTORNO: **CAJA** — es el único entorno con el corpus montado. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `f28d1038` (re-deriva al abrir; main movido no es PARO) · una sola sesión, rama propia `acto/gen2-corpus-respaldo-ejecucion-1` (D-17) · MODELO: Sonnet · MODO: ABIERTO · ids con raíz de acto (D-24) · perímetro de cierre permanente (D-21) aplica sin enumerarlo · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: cero mediciones; cero corridas; no adopta.

## 1 · OBJETIVO
Que exista una copia del corpus verificado en un disco distinto al del corpus, con `sha256` coincidente archivo por archivo, y que la FP `…CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01` quede FIRMADA con la ruta del destino y el conteo. Habilita: que un fallo del disco de caja no pierda meses de descarga (D5).
«Hecho»: `data/RESPALDO-VERIFICACION-<fecha>.tsv` con N filas = N payloads del manifiesto con `estado: VERIFICADO`, columna `coincide` = SI en todas (o lista de las que no, con NC) · la FP marcada FIRMADA citando este acto · las cuatro propuestas de `propuestas-manifiesto-2026-09-21.tsv` aplicadas al manifiesto (raíz explícita en 1 009 entradas; dos PDF de MOCIBA) o NC por cada una no aplicable.

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
- `[LEÍDO]` FP `…3d56-01` (ABIERTA desde 21/sep): «Destino del respaldo … disco externo que mesa conecte (recomendada)». NC `…3d56-02`: cuatro propuestas de manifiesto. `[EXISTE]` `INSTRUCCION-RESPALDO.md` (del acto CORPUS-INTEGRIDAD-Y-RESPALDO-1) con los cuatro comandos y `--destino`.
- `[REPORTADO]` por mesa 23/sep: el disco existe y hay que reformatearlo; estará listo esta semana; vence 27/sep. El acto arranca cuando mesa diga «montado en <ruta>»; hasta entonces está EN-COLA con fecha.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls data/ | grep -i RESPALDO-VERIFICACION` → 0. FP `…3d56-01` ABIERTA (`awk` sobre el TSV al redactar).

## 5 · PIEZAS
- **P1 · Copia.** Los cuatro comandos de `INSTRUCCION-RESPALDO.md` con `--destino <ruta del disco>`; salida cruda pegada en la nota.
- **P2 · Verificación.** `sha256sum` del destino contra `data/manifiesto.yaml` por id, con lector de YAML, conteo total y por estado (A.13). Tres resultados que no se colapsan: COINCIDE · DISCORDANTE (id, sha esperado, sha obtenido) · AUSENTE-EN-DESTINO.
- **P3 · Manifiesto.** Aplicar las cuatro propuestas de `…3d56-02` en commit propio; cada una con antes/después por comando.
- **P4 · Firma.** FP `…3d56-01` → FIRMADA («destino: <ruta>; N/N COINCIDE; fecha»); NC `…3d56-02` cerrada.

## 6 · LATITUD
Ruta y orden de copia libres. Pregunta a mesa (sigues con P3): si el disco no cabe (19.8 GB + margen) o el sistema de archivos no acepta nombres del corpus.

## 7 · PAROS — lista cerrada
a) no aplica · b) borrar o sobrescribir algo del corpus origen · c) no aplica · d) no aplica · e) NUBE · f) el disco no está montado al abrir → no es PARO: EN-ESPERA con fecha, y se reporta.

## 8 · COMPUERTAS
«Nada se escribe en el origen; solo en `--destino`» protege: **borrar**. «Verificación por manifiesto, no por `ls`» protege: **congelar** (el respaldo es un sello del corpus).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: el disco destino, `data/RESPALDO-VERIFICACION-*.tsv`, `data/manifiesto.yaml` (solo las cuatro propuestas), `firmas-pendientes.tsv`/`no-corrido.tsv` (append), nota, L0, cascada. Ajeno: todo lo demás. En vuelo en CAJA: `DUELO-ENCIG2025-CIERRE-1` (no toca manifiesto ni disco); no coincidir con él en la escritura del manifiesto: si su rama lo tocó, rebasar.

## 10 · LO QUE NO HACE · SUCESORES
No descarga, no re-verifica el origen (ya está), no cambia reservas. Sucesor: ninguno; un cron de re-verificación del respaldo es de TUBERÍA si mesa lo pide.

## NO-CORRIDO / RESERVAS

| qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|
| P1-P4 · «Los cuatro comandos de `INSTRUCCION-RESPALDO.md` con `--destino`» · «`sha256sum` del destino contra el manifiesto» · «Aplicar las cuatro propuestas … en commit propio» · «FP `…3d56-01` → FIRMADA» | `PARO-PREMISA`: el propio encargo (§7-f) declara que el disco externo no montado al abrir no es PARO sino EN-ESPERA con fecha. Verificado (fuera de sandbox): `ls -la /mnt/` sólo muestra `c`, `d`, `e` — los tres discos internos de Windows ya conocidos, ninguno recién formateado (`df -h`: 931G/3.7T/931G en uso). Ningún disco externo nuevo montado. Consistente con la firma de mesa D5 (§2, verbatim, 23/sep): «Ya tengo un disco duro, necesito reformatearlo … no ahora, esta semana sí; vence el domingo». La FP `FP-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01`, re-verificada contra `origin/main` fresco, sigue `ABIERTA` con el mismo texto del 21/sep. | El corpus sigue en una sola máquina física; la FP `…3d56-01` sigue `ABIERTA`; el manifiesto no gana las cuatro propuestas de raíz/PDF de `…3d56-02`. | `SIN-ASIGNAR` — acto que repita `INSTRUCCION-RESPALDO.md` con `--destino` cuando mesa reporte «montado en `<ruta>`» (vence 27/sep/2026, firma D5). Dato de contexto para ese acto, no usado por este: ya existe una copia staging verificada de 19.8 GB en `/home/pc0/mm-respaldo-corpus/2026-09-21/` (mismo disco que el corpus, no cuenta como respaldo). |

## CONSUMIDO

Ejecutado por `PR #1052` (rama `acto/gen2-corpus-respaldo-ejecucion-1`, 23/sep/2026). ADR `ADR-260923-GEN2-CORPUS-RESPALDO-EJECUCION-1-a307-01`; nota `forense/notas/2026-09-23-GEN2-CORPUS-RESPALDO-EJECUCION-1-cierre.md`. Determinación: EN-ESPERA, no PARO (§7-f) — el disco externo del respaldo no está montado; cero commits de P1-P4. Fila `NC-260923-GEN2-CORPUS-RESPALDO-EJECUCION-1-a307-01`. FP `FP-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01` sigue `ABIERTA`, sin tocar. Propuesto; mesa fusiona.
