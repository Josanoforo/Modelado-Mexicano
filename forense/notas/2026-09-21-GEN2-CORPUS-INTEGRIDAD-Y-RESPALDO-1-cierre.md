# Nota de cierre · ACTO GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1 · 21/sep/2026

Encargo archivado (A.3): `forense/encargos/2026-09-21-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1.md`, 0-bis `3d567239`, sello de cuerpo `64515eee…`, raíz de acto `3d56`. Rama `acto/gen2-corpus-integridad-y-respaldo-1`, una sola sesión, Opus 5 (el encargo sugería Sonnet; se subió), sin sub-agentes, MODO ABIERTO, COMPUERTA: ninguna. Todo lo de este acto vive en `forense/analisis/corpus-integridad-1/` (`LEEME-corpus-integridad-1.md` ahí).

## 0 · ARRANQUE (salida cruda)

- 0.a `git rev-list --count HEAD..origin/main` → `0`; base `fc13cdcc` = SHA de redacción del encargo. 0.b `git status --porcelain` vacío. 0.c rótulo: rama remota `grep -i integridad` → nada; worktree → sólo el propio; `gh pr list --search CORPUS-INTEGRIDAD --state open` → nada. 0.d `limpia_arbol.py --reporta`: 24 worktrees vivos, base al día, 12 ramas remotas sin PR (ajenas, sólo reporte).
- `data/raw` → enlazada a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiada del clon padre (`data_raw`, `descargas_mx`).
- `python3 tools/entorno.py --arranque`:
  ```
  ENTORNO-DERIVADO = CAJA
  senal-corpus: montado=SI archivos_examinados=422
  senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable
  red: PERMITIDA (http_code=200, http_connect=000, x_deny_reason=ausente, via_proxy=NO)
  ENTORNO · commit=fc13cdcc56bd · git_status=LIMPIO(0) · python=3.14.4 · … · raices=data_raw:SI descargas_mx:SI · corpus=SI(examinados=422)
  ```
  CAJA = lo que el encargo exige.

## 1 · Firma de mesa recibida durante el acto (verbatim)

Pregunta (§2 del encargo, al empezar): «¿A dónde va el respaldo del corpus (P3)? Sigo con P1 (censo) mientras contestas.» Opciones: disco externo (recomendada) · nube de mesa cifrada · las dos · sin destino por ahora.
**Respuesta de mesa: «Sin destino por ahora».** Consecuencia (prevista por el encargo): el juego queda armado y verificado en un directorio de la caja, **y eso todavía no es un respaldo** (mismo disco físico que el corpus). Fila `FP-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01` ABIERTA para el destino.

## 2 · Premisas del encargo, verificadas

| premisa | rótulo | resultado |
|---|---|---|
| 1 632 entradas; sin raíz 1 016 · descargas_mx 335 · data_raw 277 · reserva_respondentes 4; 18.4 GB | `[EJECUTADO]` | **Confirmada**: `grep -c "^- id:"` = 1632; censo por `raiz_declarada`: SIN-RAIZ 1016 · descargas_mx 335 · data_raw 277 · reserva_respondentes 4; declarado 18 394 174 517 B |
| `--verifica` tabula por raíz sin colapsar | `[LEÍDO]` | Confirmada (`tests/manifiesto.py:641-818`, `payload_resolver.py`, cinco estados) |
| «corpus montado 420 archivos» vs 1 632 | `[LEÍDO]` | **Explicada, no es un hueco**: `tools/entorno.py::acceso_corpus` cuenta `len(os.listdir(data/raw))` = entradas de PRIMER NIVEL (hoy 422: 421 + el symlink `raw`), no payloads del manifiesto. 1 291 archivos reales bajo `data/raw` en 203 directorios |
| dos PDF de ENIF 2012/2015 «aún no están físicamente en la caja» (nota de #960) | `[LEÍDO]` | **Cayó (logística)**: `enif_2012_cuestionario_pdf` y `enif_2015_cuestionario_pdf` están en `data_raw` y COINCIDEN (855 195 B / 676 127 B) — alguien los trajo entre #960 y este acto. Nada que bajar |
| «Ya hecho»: censos parciales de raíz, ningún respaldo | §4 | Repetida por objeto: `grep -ril "respaldo del corpus\|backup" forense/encargos forense/notas` → 9 archivos: el `~/BACKUP-mm-mirror-2026-08-10.git` (espejo del REPO, destruido por PURGA-2 el 25/ago), podas de árboles/clones (GEN2-E1, GEN2-E4, W-prima) y «respaldo personal» como conducta medida (MAESTRA35-L6) — ninguno respalda payloads; `git ls-remote --heads origin | grep -i respaldo` → sólo esta rama; `ls -d /home/pc0/mm-respaldo*` → no existía antes de este acto. Confirmada |
| candado del agente de adquisición | `[LEÍDO]` | No se corrió ninguna descarga (P2 vacío), así que el candado no se tocó |

## 3 · P1 · Censo de integridad (A.1, sin colapsar)

`python3 tests/manifiesto.py --verifica` (fuera del sandbox; salida cruda completa en `verifica-2026-09-21.txt`, 2 245 líneas):
```
Por raíz (sin colapsar):
  data_raw: coincide=1286 · no_coincide=0 · ausente=2 · sin_configurar=0 · fuera_de_perimetro=0
  descargas_mx: coincide=335 · no_coincide=0 · ausente=0 · sin_configurar=0 · fuera_de_perimetro=0
  reserva_respondentes: coincide=0 · no_coincide=0 · ausente=0 · sin_configurar=0 · fuera_de_perimetro=4
```
(1 286 = 1 009 SIN-RAIZ→data_raw + 277 declaradas: el tool suma por raíz resuelta; el censo propio separa declarada de resuelta.)

`censo_integridad.py` (1 632 filas, `censo-2026-09-21.tsv`; **archivos hasheados = 1 627**, A.13):
```
  ESTÁ-Y-COINCIDE: 1621 · NO-ES-ARCHIVO: 5 · NO-ESTÁ: 2 · NO-VERIFICABLE: 4
  SIN-RAIZ: ESTÁ-Y-COINCIDE=1009 · NO-ES-ARCHIVO=5 · NO-ESTÁ=2
  data_raw: ESTÁ-Y-COINCIDE=277 · descargas_mx: ESTÁ-Y-COINCIDE=335 · reserva_respondentes: NO-VERIFICABLE=4
```
- **ESTÁ-Y-NO-COINCIDE: 0.** Tamaño real ≠ declarado: 0 filas.
- **NO-ES-ARCHIVO (5)**: `nota_metodologica_rotulo_pareada`, `ennvih_mxfls_licencia`, `hitoD_fase1_ediciones_requieren_navegador`, `encargoEG_ruptura_enoe_y_descriptores_pendientes_navegador` (notas puras) y `endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf` (retirada).
- **NO-ESTÁ (2) → están en el REPO**: `mociba_2021_cuestionario_pdf`, `mociba_2022_cuestionario_pdf` — `archivo:` es `forense/produccion/mociba-flujo-documental-1/documentos/*.pdf`, trackeado en git; sha256 real = manifiesto (`2ffadcc4…`, `a37f1750…`). Propuesta 2 de la tabla.
- **NO-VERIFICABLE (4) → están y COINCIDEN**: los cuatro `enco_*_reservado` viven en `/home/pc0/mm-corpus/reservas-respondentes/ENCO/…`; sha256 y tamaño = manifiesto (hasheados con `sha256sum`, **sin abrir ni listar** el contenido). `--verifica` no los alcanza porque `reserva_respondentes` no está en `RAICES_ESCANEABLES` (`ADR-358`). Propuesta 3.
- **Total: 1 627 de 1 627 payloads del manifiesto están físicamente en la caja y coinciden con su hash** (1 621 en su raíz declarada + 6 fuera de ella). Bytes reales sumados sobre lo verificado por el tool: 18 381 268 592; los 12.9 MB de diferencia con lo declarado son exactamente los 6 fuera de raíz.
- Sobre las 1 016 sin raíz: las 1 009 con payload están en `data_raw` bajo su nombre y coinciden — la convención «ausente = data_raw» de la cabecera se cumple 1 009/1 009. Propuesta 1.

Hallazgo lateral: `/home/pc0/mm-corpus/raw/raw -> /home/pc0/mm-corpus/raw` es un **symlink en bucle** (14/sep). Un recorrido con `followlinks=True` infló el índice a 51 641 «archivos» (1 291 reales). No se tocó (PARO b: ni borrar ni renombrar); el índice del juego y `rsync --no-links` lo omiten. Línea en hallazgos.

## 4 · P2 · Traer lo que falta

Conjunto `NO-ESTÁ ∩ url_origen`: los dos PDF de MOCIBA — pero están en el repo con hash correcto: no hay nada que bajar. **P2 = 0 descargas, 0 intentos**, y por eso el candado del agente no se tocó y el manifiesto no se editó. Anti-PR#77: no aplica (nada descargado).

## 5 · P3 · Juego de respaldo (en la caja; NO es respaldo todavía)

Destino: `/home/pc0/mm-respaldo-corpus/2026-09-21/` (mismo disco `/dev/sdd` que `mm-corpus`; 897 GB libres). Raíces físicas del corpus, las tres: `data_raw=/home/pc0/mm-corpus/raw` · `descargas_mx=/mnt/c/Users/PC0/Descargas MX` · `reserva_respondentes=/home/pc0/mm-corpus/reservas-respondentes`. (`mm-corpus/descargas_mx_espejo` y `f5-documental-v1_0` son copias/derivados, no raíces; fuera del juego a propósito.)

1. **Índice desde los archivos** (`--indexa`): `INDICE: archivos=1914 bytes=19817841648 (39s)` — data_raw 1291 / 17 716 486 582 B · descargas_mx 619 / 2 090 341 979 B · reserva_respondentes 4 / 11 013 087 B. `indice.tsv` + `SHA256SUMS`; copia en el repo: `indice-juego-2026-09-21.tsv`, `SHA256SUMS-juego-2026-09-21`. Excluidos: symlinks y `.manifiesto.lock`.
2. **Copia** (`rsync -rt --safe-links --no-links`): `Total transferred file size: 17,716,486,582 · 2,090,341,979 · 11,013,087 bytes`; 1 291 + 619 + 4 regulares transferidos; el symlink en bucle contado (`link: 1`) y no copiado.
3. **Verificación en destino** (rehash completo): `VERIFICA-DESTINO: examinados=1914 coincide=1914 no_coincide=0 falta=0 (15s) -> VERDE`; independiente del script: `sha256sum -c --quiet SHA256SUMS` → OK, 1 914 líneas.
4. **Prueba de restauración**: (a) muestra: `RESTAURA: 166 archivos (147 subdirectorios + 20 al azar, semilla=20260921)` → `restaurados=166 bytes=6637618524 coincide=166 no_coincide=0 -> VERDE`; (b) como «un payload por encuesta» no es derivable del manifiesto (los ids no llevan encuesta y 284+342 payloads son archivos sueltos en la raíz), se restauró **todo**: `restaurados=1914 bytes=19817841648 coincide=1914 no_coincide=0 -> VERDE` a `mm-respaldo-corpus/restauraciones-tmp/` (borrado al terminar). Primer intento con `$TMPDIR` del sandbox → `ENOSPC` (tmpfs de 7.6 GB); corregido con `--tmp` junto al destino.

Instrucción para repetirlo: `INSTRUCCION-RESPALDO.md` (cada vez que el manifiesto gane payloads o cada mes; cuatro comandos; qué pegar). Falsador a tres meses (§10 del encargo): 21/dic/2026.

## 6 · P4 · Lo irrecuperable por comando (sin tocar la red)

`irrecuperables.py` sobre las 1 627 entradas con payload, usando `clasifica_url_origen` de la casa (sobre la ruta) + señales de gestión en licencia/nota/descargado_por:
```
  DESCARGABLE: 728 entradas · 8 480 277 987 B
  LICENCIA-O-GESTION: 29 · 111 578 643 B   (ENNViH/MxFLS 27: «registro de usuario»; PEW 1 token; INEGI 1 formulario de solicitud)
  URL-DERIVADA: 67 · 1 501 615 431 B        (url_origen asignada por --escanea, no confirmada por el autor)
  URL-NO-DESCARGABLE: 803 · 8 300 702 456 B (página/portal/catálogo/servlet: --descarga --id no la trae)
  NO RE-OBTENIBLES POR COMANDO: 899 entradas · 9 913 896 530 B
```
Lectura honesta: «no re-obtenible por comando» no es «perdido para siempre» — muchas URL-NO-DESCARGABLE son portales de INEGI donde un humano vuelve a bajar; pero por `tests/manifiesto.py --descarga --id` no vuelven, y los 4 `DescargaMasiva_*.zip` del SAT y los paquetes de Dataverse/ICPSR/LAPOP/ENNViH se generan bajo demanda o tras registro. Son 55 % de las entradas y la mitad de los bytes: el juego entero es lo que hay que sacar de la máquina, no un subconjunto. La lista por id: `irrecuperables-2026-09-21.tsv`. El regex de gestión se corrigió dos veces (`registr` pelado daba 450 falsos positivos por «Registrado por ACTO…»; «sin registro ni muro de credencial» es un negativo).

## 7 · Cascada y perímetro

Propio: `forense/analisis/corpus-integridad-1/*` · `tests/test_corpus_integridad_respaldo.py` (guardia: bucle de symlink + ciclo indexa→copia→verifica→restaura sobre corpus sintético; censada como huérfana `CORRE-EN-CI` en `forense/analisis/ci-guardias/censo-tests.tsv`, una fila; `--ejecuta-huerfanos` → `OK … (0.4s)`, `ejecutados=57 saltados=45 fallidos=0`) · esta nota · `data/INFRAESTRUCTURA-v1_0.md` (sección propia) · `canon/gobernanza-v1_15.md` ADR de raíz de acto · `canon/L0/<ADR>.md` · `canon/registro-rotulos.tsv` · `forense/hallazgos.md` · `forense/no-corrido.tsv` · `forense/firmas-pendientes.tsv`. Fuera del repo: `/home/pc0/mm-respaldo-corpus/2026-09-21/` (19 GB). **No tocado**: `data/manifiesto.yaml`, ninguna raíz del corpus, ninguno de los ocho archivos de TUBERÍA, la cola de adquisición.

`cuenta_gen2 = NO-APLICA` (no mide). Ningún contador del programa se mueve por este acto; lo que se mueve es «cuánto del corpus se puede volver a verificar si el disco falla»: de 0 a un juego verificado en el mismo disco.
