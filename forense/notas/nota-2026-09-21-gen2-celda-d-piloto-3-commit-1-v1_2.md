# `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_2` · los dos CALC del piloto 3 pasan el preflight que sella, sin tocar una línea del código ni de la spec humana

**PREFLIGHT-PASÓ:** `corrida0 preflight CALC-GOB-DIGITAL-EXE-EMISIONES-0002` → **`VERDE`** en CAJA (`/home/pc0/mm-piloto-3-v12`, corpus `mm-corpus/raw` montado en `data/raw`), con el payload `encig25_base_datos_csv.zip` **`COINCIDE`** (37 624 925 B, sha256 `47daf2f7…`, sólo hasheado); `…-ADJUDICACION-0001` → `BLOQUEADO` **exactamente** por las cuatro entradas `emisiones_*` de la lista escrita antes (§2). Commit de las llaves: `351f5133`; ambos `.py`, `spec.md` y su sidecar byte a byte iguales a `826bf3a1`.

**21/sep/2026 (20/sep 22:20 CST) · CAJA (`ENTORNO-DERIVADO`: `corpus=SI(examinados=419)`, `raices=data_raw:SI descargas_mx:SI`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, python 3.14.4, numpy 2.3.5, pandas 2.3.3) · Opus 5 · rama `acto/gen2-celda-d-piloto-3-commit-1-v1_2`, worktree `/home/pc0/mm-piloto-3-v12`.**

**Base declarada:** `PR #941` **no estaba fusionado al abrir** → se arranca de su cabeza, como el encargo prevé. La cabeza ya no era `b1f1cb13`: antes de apilar, esta misma sesión fusionó `origin/main` (`887aecb6`, que trae `#939` con `ADR-577`) en `#941` y renumeró su ADR `577→578`; cabeza nueva `b6fc096e`. `FP-407` vive ahí (ABIERTA). Encargo archivado (A.3): `forense/encargos/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_2.md` + sidecar `.sha256` (`6fe87bd8…`, `sha256sum -c` → OK), commit `a798f8b3`, rama empujada antes de cualquier paso sustantivo. El sidecar verifica el texto **tal como se archivó en ese commit** (`git show a798f8b3:<encargo> | sha256sum` = `6fe87bd8…`); las secciones `## NO-CORRIDO` y `## CONSUMIDO` que la cascada añade después lo hacen fallar sobre el árbol, igual que en el precedente `2026-09-20-GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1.md` — el sello es del texto recibido, no del archivo vivo.

**Exposición de esta sesión (F3, `FP-407` a):** es la sesión que paró en `#941`. No tiene los diseños A/B ni el careo; de ENCIG 2025 sólo vio el `sha256` del preflight de `#941` y de los preflight de este acto. Por F3, **esta sesión no corre los COMMIT-2/3**.

---

## 1 · Arranque y §4 (búsqueda por objeto, con mi acceso)

- 0.a `HEAD..origin/main` = 0 tras el merge en `#941`. 0.b limpio. 0.c: `git ls-remote --heads origin | grep -i v1_2` → 0 ramas; `git worktree list` → 0 worktrees `v1_2`; `gh pr list --search v1_2` devolvió `#942` (`GEN2-RELEVO-TANDA-3`, coincidencia de texto, no del rótulo) → sin duplicado. 0.d como en `#941`.
- `data/raw` enlazada a `/home/pc0/mm-corpus/raw`; `raices.local.yaml` copiada. `tools/entorno.py`: `montado=SI`.
- **Objeto «`spec.yaml` del piloto 3 que pasa preflight»:** `git diff --stat origin/main origin/<rama> -- <los dos spec.yaml>` sobre **todas** las ramas remotas (≠ main) → 0 ramas con diferencia. Ninguna rama lo arregla. Ningún directorio `CALC-GOB-DIGITAL-EXE-*` tiene sello (E.3 no protege nada aquí).
- Premisas `[EJECUTADO]` de dirección, re-corridas aquí: huellas de los tres `resultados.json` sellados (`285eeb55…`, `b7d3dfe9…`, `be24d879…`) — idénticas a las que `#941` reportó y a las del encargo; `git show 826bf3a1:forense/firmas-pendientes.tsv` trae `FP-399 FIRMADA` y su `sha256` es `c79e37d7…`; el libro vivo hoy es `17b24afc…` (era `e0f1ec86…` en `04a2edeb` y `5df43a05…` en `b1f1cb13`: **tres huellas en dos días**, la premisa del cuarto defecto se sostiene). `medidor.py:103-111`: la guardia lee `ruta_absoluta` y sólo exige `estado = FIRMADA` de `FP-399`. `decisiones.tsv`: 63 filas `cuenta_gen2=SI`, **2** filas `CALC-GOB-DIGITAL-EXE-EMISIONES-0001` (F1-bis y F3, no `cuenta_gen2`), **0** para `-0002`/`ADJUDICACION-0001`.
- `dependencias_materiales` derivadas de los `import`: `medidor.py` → `numpy`, `pandas` (más stdlib `io`, `json`, `math`, `zipfile`, `pathlib`); `adjudicacion.py` → `numpy`, `pandas` (más stdlib `hashlib`, `importlib`, `json`, `math`, `pathlib`). Forma de la casa: `[numpy, pandas]` (39 specs).

## 2 · Lista esperada — escrita ANTES de correr los preflight (compuerta §8)

- `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` → **`PRE-FLIGHT: VERDE`** (sin bloqueos; se admiten avisos, p. ej. `spec_md_no_esta_en_origin_main`, que no bloquean).
- `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` → **`PRE-FLIGHT: BLOQUEADO`** exactamente por estas cuatro entradas y ninguna otra:
  1. `input_repo_ausente=emisiones_resultados:data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/resultados.json`
  2. `input_repo_no_commiteado=emisiones_resultados`
  3. `input_repo_ausente=emisiones_sello:data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/sello.json`
  4. `input_repo_no_commiteado=emisiones_sello`

Cualquier otra entrada en cualquiera de los dos → PARO (g), sin quinta llave.

## 3 · Salida cruda de los dos preflight (corridos tras commitear P1/P3, porque `preflight` exige árbol limpio)

```
$ python3 tools/corrida0.py preflight CALC-GOB-DIGITAL-EXE-EMISIONES-0002
PRE-FLIGHT CALC-GOB-DIGITAL-EXE-EMISIONES-0002   (data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002)
  [COMMITEADO] forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md
  [COMMITEADO] data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/spec.yaml
  [EN-MAIN-COINCIDE] spec_md_sha256
              declarado en spec.yaml = 62d8d07d70dd4d53544975bf8b541e5cd63079080d9537b5fde8414115579eb5
              arbol                  = 62d8d07d70dd4d53544975bf8b541e5cd63079080d9537b5fde8414115579eb5
              origin/main            = 62d8d07d70dd4d53544975bf8b541e5cd63079080d9537b5fde8414115579eb5
  [UNICOS] ids de resultados: 565 declarados
  [UNICOS] ids de inputs: 5 declarados
  [EXISTE] script data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/medidor.py
              script_blob_sha256 = 05d4c2058ea00bd3a2074a2ba3aa5cef4bbe24a407e523b294bb5bfe6075d4dc
  inputs declarados: 5
    [COINCIDE] encig25_base_datos_csv  origen=manifiesto  raiz=data_raw
              ruta_absoluta   = /home/pc0/mm-piloto-3-v12/data/raw/encig25_base_datos_csv.zip
              sha256 esperado = 47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12
              sha256 actual   = 47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12
              tamano          = 37624925
    [COINCIDE] encig2021_cruces_resultados  origen=repo  ruta=data/corrida0/CALC-ENCIG2021-CRUCES-HISTORICOS-0003/resultados.json
              sha256 real     = 285eeb552c0ab99cb9cc9cab1d0622209d3ddda837baa29193d98670fefbe9f5
              sha256 declarado= 285eeb552c0ab99cb9cc9cab1d0622209d3ddda837baa29193d98670fefbe9f5
    [COINCIDE] encig2023_cruces_resultados  origen=repo  ruta=data/corrida0/CALC-ENCIG2023-CRUCES-HISTORICOS-0002/resultados.json
              sha256 real     = b7d3dfe9aae42276961c5bf5676f0aa5f3de7e9a2218e44a58a613ef5cb7773e
              sha256 declarado= b7d3dfe9aae42276961c5bf5676f0aa5f3de7e9a2218e44a58a613ef5cb7773e
    [COINCIDE] c2_compuesto_resultados  origen=repo  ruta=data/corrida0/CALC-C2-COMPUESTO-RESERVADAS-0001/resultados.json
              sha256 real     = be24d879d22d28a05c36441b471976a6b0b3d40f2877efa2cd514a13e5bae3cb
              sha256 declarado= be24d879d22d28a05c36441b471976a6b0b3d40f2877efa2cd514a13e5bae3cb
    [COINCIDE] firmas_pendientes_tsv  origen=repo  ruta=data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/fp399-firmada-826bf3a1.tsv
              sha256 real     = c79e37d780198c904142b089caf8d235e30add02b514d67e7a762f0203466bdf
              sha256 declarado= c79e37d780198c904142b089caf8d235e30add02b514d67e7a762f0203466bdf
  [ENDURECIDO] esquema de spec   (etiquetas.generacion = GEN2)
  [DECLARADO] parametros = {"bootstrap_replicas": 10000, "delta_mae_umbral_pp": 0.5, "fuera_de_soporte_global_si_fallan": 5, "lambda_congelada": 0.8937949410086089, "lambda_sigma_bar2": 0.003001124084482884, "lambda_tau2": 0.02525670198316379, "lambda_var_entre": 0.028257826067646673, "metodo_ic": "bootstrap UPM con reposicion dentro de estrato; singleton de certeza; percentiles 2.5/97.5; replicas compartidas; PCG64(20260919) como CALC-ENCIG2023-CRUCES-HISTORICOS-0002", "n_minimo_celda": 200, "ola": "2025", "olas_para_soporte": ["2021", "2023", "2025"], "payload_id": "encig25_base_datos_csv", "reserva_s2_fraccion": 0.01, "retador_gana_si_vence_c2_en_fraccion": 0.75, "s1_veredicto": "CAMBIO-MENOR"}
  [DECLARADO] tolerancia = {"abs": 1e-10, "razon": "mismo payload, transformacion y sumas float64; bootstrap determinista por semilla", "tipo": "flotante"}
  [DECLARADO] seed       = {'aplica': True, 'valor': 20260919, 'rng': 'numpy.PCG64'}
  [LIMPIO] git status --porcelain (0 lineas)
  [SIN-SELLO-PREVIO] sello previo   [python3 tools/sella_sha256.py --verifica data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/sello.json]

PRE-FLIGHT: VERDE
```

```
$ python3 tools/corrida0.py preflight CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001
PRE-FLIGHT CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001   (data/corrida0/CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001)
  [COMMITEADO] forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md
  [COMMITEADO] data/corrida0/CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001/spec.yaml
  [EN-MAIN-COINCIDE] spec_md_sha256
              declarado en spec.yaml = 62d8d07d70dd4d53544975bf8b541e5cd63079080d9537b5fde8414115579eb5
              arbol                  = 62d8d07d70dd4d53544975bf8b541e5cd63079080d9537b5fde8414115579eb5
              origin/main            = 62d8d07d70dd4d53544975bf8b541e5cd63079080d9537b5fde8414115579eb5
  [UNICOS] ids de resultados: 349 declarados
  [UNICOS] ids de inputs: 7 declarados
  [EXISTE] script data/corrida0/CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001/adjudicacion.py
              script_blob_sha256 = 0727a18b6d6cae24737e8f8dcc700795eae17d0c57e661d9aa81fecc1c27048f
  inputs declarados: 7
    [COINCIDE] encig25_base_datos_csv  origen=manifiesto  raiz=data_raw
              ruta_absoluta   = /home/pc0/mm-piloto-3-v12/data/raw/encig25_base_datos_csv.zip
              sha256 esperado = 47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12
              sha256 actual   = 47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12
              tamano          = 37624925
    [COINCIDE] encig2021_cruces_resultados  origen=repo  ruta=data/corrida0/CALC-ENCIG2021-CRUCES-HISTORICOS-0003/resultados.json
              sha256 real     = 285eeb552c0ab99cb9cc9cab1d0622209d3ddda837baa29193d98670fefbe9f5
              sha256 declarado= 285eeb552c0ab99cb9cc9cab1d0622209d3ddda837baa29193d98670fefbe9f5
    [COINCIDE] encig2023_cruces_resultados  origen=repo  ruta=data/corrida0/CALC-ENCIG2023-CRUCES-HISTORICOS-0002/resultados.json
              sha256 real     = b7d3dfe9aae42276961c5bf5676f0aa5f3de7e9a2218e44a58a613ef5cb7773e
              sha256 declarado= b7d3dfe9aae42276961c5bf5676f0aa5f3de7e9a2218e44a58a613ef5cb7773e
    [COINCIDE] c2_compuesto_resultados  origen=repo  ruta=data/corrida0/CALC-C2-COMPUESTO-RESERVADAS-0001/resultados.json
              sha256 real     = be24d879d22d28a05c36441b471976a6b0b3d40f2877efa2cd514a13e5bae3cb
              sha256 declarado= be24d879d22d28a05c36441b471976a6b0b3d40f2877efa2cd514a13e5bae3cb
    [COINCIDE] firmas_pendientes_tsv  origen=repo  ruta=data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/fp399-firmada-826bf3a1.tsv
              sha256 real     = c79e37d780198c904142b089caf8d235e30add02b514d67e7a762f0203466bdf
              sha256 declarado= c79e37d780198c904142b089caf8d235e30add02b514d67e7a762f0203466bdf
    [AUSENTE+NO-COMMITEADO] emisiones_resultados  origen=repo  ruta=data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/resultados.json
              sha256 real     = None
              sha256 declarado= (ninguno)
    [AUSENTE+NO-COMMITEADO] emisiones_sello  origen=repo  ruta=data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/sello.json
              sha256 real     = None
              sha256 declarado= (ninguno)
  [ENDURECIDO] esquema de spec   (etiquetas.generacion = GEN2)
  [DECLARADO] parametros = {"bootstrap_replicas": 10000, "delta_mae_umbral_pp": 0.5, "fuera_de_soporte_global_si_fallan": 5, "lambda_congelada": 0.8937949410086089, "lambda_sigma_bar2": 0.003001124084482884, "lambda_tau2": 0.02525670198316379, "lambda_var_entre": 0.028257826067646673, "metodo_ic": "bootstrap UPM con reposicion dentro de estrato; singleton de certeza; percentiles 2.5/97.5; replicas compartidas; PCG64(20260919) como CALC-ENCIG2023-CRUCES-HISTORICOS-0002", "n_minimo_celda": 200, "ola": "2025", "olas_para_soporte": ["2021", "2023", "2025"], "payload_id": "encig25_base_datos_csv", "reserva_s2_fraccion": 0.01, "retador_gana_si_vence_c2_en_fraccion": 0.75, "s1_veredicto": "CAMBIO-MENOR"}
  [DECLARADO] tolerancia = {"abs": 1e-10, "razon": "bootstrap determinista por semilla; mismas multiplicidades que el CALC de emisiones", "tipo": "flotante"}
  [DECLARADO] seed       = {'aplica': True, 'valor': 20260919, 'rng': 'numpy.PCG64'}
  [LIMPIO] git status --porcelain (0 lineas)
  [SIN-SELLO-PREVIO] sello previo   [python3 tools/sella_sha256.py --verifica data/corrida0/CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001/sello.json]

PRE-FLIGHT: BLOQUEADO input_repo_ausente=emisiones_resultados:data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/resultados.json input_repo_no_commiteado=emisiones_resultados input_repo_ausente=emisiones_sello:data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/sello.json input_repo_no_commiteado=emisiones_sello
```

**Coincide con §2 entrada por entrada: compuerta cumplida; el v1.2 queda congelado.** El único aviso de EMISIONES fue ninguno: `spec_md_sha256` salió `EN-MAIN-COINCIDE` porque la spec humana ya está en `origin/main` desde `#926`.

## 4 · P1, P3, P4, P5 — qué se cambió y qué se probó

**P1 · Cuatro llaves, edición por línea (sin reserializar):** `git diff --stat` del commit de llaves: `EMISIONES-0002/spec.yaml` 11 líneas (+8/−3), `ADJUDICACION-0001/spec.yaml` 17 (+14/−3, incluye P3), más el archivo nuevo `data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/fp399-firmada-826bf3a1.tsv` (= `git show 826bf3a1:forense/firmas-pendientes.tsv`, sha256 `c79e37d7…`, 389 líneas; los dos CALC apuntan a él bajo el mismo `id` `firmas_pendientes_tsv`, así que `medidor.py:103-111` lo lee sin cambio). Llaves: `spec_md: ../../../forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md` (`spec_md_sha256` intacto, `62d8d07d…`); `sha256` en `encig2021_cruces_resultados` (`285eeb55…`), `encig2023_cruces_resultados` (`b7d3dfe9…`), `c2_compuesto_resultados` (`be24d879…`) — derivados con `sha256sum` en la sesión; `dependencias_materiales: [numpy, pandas]` derivadas de los `import`. Nada más del `spec.yaml` cambió: parámetros, semilla, tolerancia, rejilla, candidatos, resultados y guardias, intactos (`git diff` lo muestra línea a línea).

**P3 · Secuencia COMMIT-2 / 3a / 3**, escrita una sola vez, como clave `secuencia_commits` del `spec.yaml` de ADJUDICACION (el archivo que el 3a edita): COMMIT-2 corre y sella EMISIONES (otra sesión); **COMMIT-3a** escribe en ese `spec.yaml` el `sha256` de `emisiones_resultados` y `emisiones_sello` recién sellados y verifica `preflight` VERDE; **COMMIT-3** deriva R y adjudica. Precedente citado: piloto 1, `c169edc9` → `39bf1af3` → `18b99142`. No cambia el procedimiento: escribe el orden que el procedimiento ya necesitaba. `yaml.safe_load` OK; `preflight` no objeta la clave (esquema endurecido no la prohíbe).

**P4 · Lo que no se tocó, probado:** `sha256sum` de `medidor.py` (`05d4c205…`), `adjudicacion.py` (`0727a18b…`), `GOB-gobierno-digital-exe15-spec-v1_1.md` (`62d8d07d…`) y su sidecar (`762916ff…`) **idénticos** a `826bf3a1`. `python3 -m pytest tests/test_piloto3_v11.py -q` → **7 passed, 21.2 s** (incluida `test_b_oro_2023_reproduce_los_sellados`), después de las llaves. `git diff --stat origin/main`, fuera de la cascada: los dos `spec.yaml`, el snapshot, dos filas de `decisiones.tsv`, tres líneas de comentario en la celda-D (cita al v1.2, §9 lo admite) y `FP-407 → FIRMADA` (A.12).

**P5 · Firma de contador, asentada donde cuenta:** dos filas en `data/corrida0/decisiones.tsv` (`objeto` = CALC-id · `decision` = `cuenta_gen2=SI · sea cual sea el veredicto (…)` · `fuente` = firma verbatim + `FP-407 (c)` + ruta del encargo COMMIT-2-3 · `fecha` = 2026-09-21). Probado con la función que resuelve, sin correr nada: `_cuenta_gen2_resuelto(calc_id, spec, _lee_decisiones())` → `('SI', 'decision de mesa (decisiones.tsv): …')` para **los dos** ids. Antes había 0 filas para estos ids (2 para `-0001`: F1-bis y F3). Ningún contador se movió: la fila decide cómo contará una corrida que aún no existe.

**Higiene (§7 b):** no se invocó ningún `tools/*` fuera de `corrida0.py preflight`, `corrida0.py registro` en seco (FP-359: sin `--escribe` no toca TSV; `git status` lo confirma), `entorno.py`, `cierre_acto.py` y `verifica_head_remoto.py`. `git status` antes de cada commit: sólo el perímetro. ENCIG 2025: sólo `sha256` del zip, dos veces (los dos preflight).

## 5 · Para mesa (lo que este acto no resuelve)

1. **D-22 debería exigir `corrida0 preflight`** en VERDE, o bloqueado sólo por una lista declarada antes de correr: el v1.1 cumplía D-22 tal como está (7/7 con oro 2023) y no corría. Regla de gobierno → DIRECCIÓN.
2. **Nada se sella contra un libro vivo:** `forense/firmas-pendientes.tsv` cambió de huella tres veces en dos días. Misma clase que el sidecar de `#932` → TUBERÍA.
3. **Colisión de números en vuelo:** `#941` (base de este acto) lleva `ADR-578`; `#943` (abierto) también declara `ADR-578` y `NC-0447`. Regla de la casa: renumera quien fusiona segundo. Este acto toma `ADR-580` sobre `#941`.
4. `forense/firmas-pendientes.tsv` trae en `origin/main` un id malformado `FP-260921` (dos filas) que hace que `cierre_acto.py` reporte «FP máximo: 260921». Ajeno; una línea.

## 6 · Sucesor

COMMIT-2 / 3a / 3 del piloto 3 en **otra** sesión (F3), con `secuencia_commits` del `spec.yaml` de ADJUDICACION y la firma de contador ya en `decisiones.tsv`. Lo que esa sesión debe correr primero: `corrida0 preflight CALC-GOB-DIGITAL-EXE-EMISIONES-0002` → VERDE (si `origin/main` movió `firmas-pendientes.tsv`, no importa: la guardia lee el snapshot).
