# Nota de cierre · GEN2-DUELO-ENVIPE2026-EJECUCION-1

**Acto:** `GEN2-DUELO-ENVIPE2026-EJECUCION-1` · **Fecha:** 22/sep/2026 · **Entorno:** CAJA (`ENTORNO-DERIVADO = CAJA`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, corpus montado, 436 archivos examinados) · **Rama:** `acto/gen2-duelo-envipe2026-ejecucion-1` · **0-bis:** `c2b4ffe3` (raíz `c2b4`) · base `origin/main = 02eda845` (0 detrás) · **Modelo:** Opus 5.5, sin sub-agentes · **Modo:** RÍGIDO.

Encargo: `forense/encargos/2026-09-22-GEN2-DUELO-ENVIPE2026-EJECUCION-1.md` (sello de cuerpo `409cdc84…`).

## §0 · Premisas

- `[EJECUTADO]` `data/manifiesto.yaml:30381` `envipe2026_csv`, `sha256 dd79f589…` — **confirmada**; también `envipe2026_fd_pdf` (`4a076ce3…`), `_cuest_principal_pdf`, `_cuest_modulo_pdf`.
- `[LEÍDO]` nota COMMIT-1 §3/§4 — confirmada. `[EXISTE]` los dos CALC de 2026 (`SPEC-FIJADA`, sólo `spec.yaml` + `medidor.py`), `CALC-DUELO-ORIGEN-MOVIL-0001`, `tools/duelo/`, `tests/test_duelo_prospectivo.py` — confirmadas. `grep -c envipe2026 data/corrida0/corridas.tsv` → 5 filas: 3 de los CALC sellados `ENSAYO-ENVIPE2025-*`/`ORIGEN-MOVIL` (casan por nombre, no leen 2026) y 2 `SPEC-FIJADA` de los CALC de 2026 (sin corrida); ninguna corrida abrió 2026. `reserva:envipe2026` → RESERVADA.
- `[SUPUESTO]` preflight pasa sin otra causa de bloqueo — **verdadera**, sin cableado D-18 (§1).
- `[SUPUESTO]` el FD 2026 no cambió los reactivos de los desenlaces — **verdadera** (§1.3).
- **PREMISA CAÍDA (toca firma → pregunta a mesa).** El encargo pide emisiones «sobre 2018–2025», «ciegas a 2026», y pone como PARO a) «cualquier lectura de `envipe2026_csv` fuera de `ADJUDICACION-0001` en COMMIT-3». La spec sellada (`DUELO-PROSPECTIVO-ENVIPE2026-spec-v1_0.md` §2, §8 fila `CALC-DUELO-ENVIPE2026-EMISIONES-0001`, §9 «Guardia de una sola variable de agrupación sobre la ola nueva en emisiones») y el medidor congelado (`envipe_duelo.py::emisiones`, `_carga_olas(..., reservada_nueva=True)`) **abren `envipe2026_csv` en las emisiones** por el guardián `tools/celda_d/marginales_reproduccion.py` con `reservada=True`: marginales de UN eje de la ola nueva para C2 (autorizado por diseño, F7), `cruce()` lanza `ReservaRota`, no se emiten nacional, marginales crudos ni numerador. Correr las emisiones sin abrir 2026 exige editar la spec (PARO b/d). Pregunta a mesa (22/sep/2026) con tres opciones; respuesta de mesa, verbatim: **«Correr según la spec (Recom.)»** — es decir: PARO a) se lee como «fuera del código congelado para ello» (texto de `reserva:envipe2026`); `EMISIONES-0001` abre 2026 sólo por el guardián `reservada=True`, tal como selló F7; el criterio de «hecho» `git log -p -S envipe2026 -- data/corrida0/CALC-DUELO-ENVIPE2026-EMISIONES-0001` vacío (imposible: el `spec.yaml` congelado ya contiene la cadena) se sustituye por la prueba de guardia `…-G-RESERVA-GUARDIA-PROBADA` y `…-G-RESERVA-OLA-CARGADA-RESERVADA` en los `RESULT` sellados.
- Firma §2 del encargo («Se autoriza el COMMIT-3 …»): presente en el encargo lanzado → sellada por el lanzamiento (mismo patrón que `reserva:enigh2024`, `GEN2-TRAMITE-FIRMAS-4`).

## §1 · COMMIT-1 · congelación real

### §1.1 · `preflight` (salida cruda, resumida a las líneas de estado)

```
$ python3 tools/corrida0.py preflight CALC-DUELO-ENVIPE2026-EMISIONES-0001
  [EN-MAIN-COINCIDE] spec_md_sha256
    [COINCIDE] envipe2023_csv  origen=manifiesto  raiz=data_raw
    [COINCIDE] envipe2024_csv  origen=manifiesto  raiz=data_raw
    [COINCIDE] envipe2025_csv  origen=manifiesto  raiz=data_raw
    [COINCIDE] envipe2026_csv  origen=manifiesto  raiz=data_raw
              sha256 esperado = dd79f589eb6ed7d3675cc86e21ac9bbdbf269913963091d8698d6e28e0540a17
              sha256 actual   = dd79f589eb6ed7d3675cc86e21ac9bbdbf269913963091d8698d6e28e0540a17
              tamano          = 20258782
    [COINCIDE] serie_nd  origen=repo  ruta=data/corrida0/envipe-serie-denuncia-v1_0.tsv
  [ENDURECIDO] esquema de spec   (etiquetas.generacion = GEN2)
  [LIMPIO] git status --porcelain (0 lineas)
  [SIN-SELLO-PREVIO] sello previo
PRE-FLIGHT: VERDE

$ python3 tools/corrida0.py preflight CALC-DUELO-ENVIPE2026-ADJUDICACION-0001
    [COINCIDE] envipe2023/2024/2025/2026_csv, serie_nd
    [AUSENTE+NO-COMMITEADO] emisiones_selladas  sha256 declarado= PENDIENTE-COMMIT-3a
PRE-FLIGHT: BLOQUEADO input_repo_ausente=emisiones_selladas:… input_repo_no_commiteado=emisiones_selladas
```

El único bloqueo de la adjudicación es el previsto (emisiones aún no selladas). **Ningún cableado D-18 hizo falta: cero ediciones.** `preflight` sólo hashea el zip; no lo descomprime ni lista.

### §1.2 · sha de spec y medidores (idénticos a #968/#982)

```
4204b07b77bcd2dc12a518738479abfe3cd36ce5739b3e9bb0b861b6a4dd740b  forense/prereg-caja/DUELO-PROSPECTIVO-ENVIPE2026-spec-v1_0.md   (sha256sum -c del .sha256: OK)
83ae23dfac780538c52bcf114652e78803d03f0e5271e8a804c87c6be730781a  tools/duelo/envipe_duelo.py  = …EMISIONES-0001/medidor.py = …ADJUDICACION-0001/medidor.py
a41bdb07d1d975fe84a0b5653232f8532d38c56952c1eafeffd29bae89f9ee3b  tools/duelo/cruces_familia.py
430e56154232a7bf7f1d6c008465af5789637e21277b2c59442c4d0ece649db7  tools/duelo/tendencia_nacional.py
4df2c630179c194345594d959d012b7dd18d94ac93fab3f48b8f6683753dafd6  tools/celda_d/marginales_reproduccion.py
e5ffbebfe02f53468bcffaeb19ded1246570cb59c6370172e47f12c0896e7d59  …EMISIONES-0001/spec.yaml
d9e3b45b97f9c99b5d2426ad5a8bd40ce802b589d60ebb930c1f341431c60a84  …ADJUDICACION-0001/spec.yaml
```

`git diff 80b71c81 HEAD` (merge de #982) sobre esos archivos: vacío (sólo aparece `tools/duelo/credito_prediccion_2024.py`, archivo nuevo de otro acto que el duelo no importa). Contra `de35a0d8` (merge de #968): sólo la línea `congelado:` de los dos `spec.yaml`, que es la edición de #982. `tests/test_duelo_prospectivo.py`: 25 passed (sintético; su única mención de 2026 es un zip fabricado `envipe2026_raro.zip`).

### §1.3 · FD 2026 por texto (antes de COMMIT-3)

`fd_envipe2026.pdf` (`4a076ce3…` = manifiesto) contra `fd_envipe2025.pdf` (`83fe0246…`), `pdftotext -layout`, bloque por mnemónico, diff por tokens:

| reactivo | texto de la pregunta | catálogo | veredicto |
|---|---|---|---|
| `BP1_20` (1.20 ¿Acudió … a denunciar el delito?) | idéntico | 1 Sí · 2 No — idéntico | construible |
| `BP1_23` (1.23 razón principal de no denunciar) | idéntico | 01–09, 99, b — idéntico, mismos textos | construible |
| `BPCOD` (códigos para delitos, 01–15) | — | mismos 15 códigos; cambios de redacción en 01/02 («camioneta, camión» → «camioneta o camión»), 03 (+«o daños»), 09 («Amenazas, presiones o engaños» → «Presiones, engaños o advertencias», sigue siendo «(extorsión)») | construible; hallazgo (abajo) |
| `NIV` (tsdem) | — | 00–10 + 99 idénticos salvo mayúscula «Doctorado» y «No sabe / no responde» | construible |
| `DOMINIO` U/C/R, `SEXO`, `EDAD`, `EST_DIS`, `UPM_DIS`, `FAC_DEL` | — | idénticos (sólo cambian posición/consecutivo y pie de página) | construible |

Nombres de tabla (`TMod_Vic`, `TSDem`): mismas menciones. **Ninguna celda `NO-CONSTRUIBLE`; ningún catálogo renumerado** (la pregunta de latitud §6 no se activa). Hallazgo, una línea: la redacción del código 09 de `BPCOD` (extorsión) cambió en 2026; el código y el grupo (personales 5–15 de la serie ND) no cambian, así que el procedimiento congelado lo cuenta igual, pero una variación del universo ND en 2026 podría venir del instrumento — se declara, no se ajusta.

**COMMIT-1 cumplido:** compuerta «`preflight` VERDE con payload COINCIDE — protege: congelar spec» satisfecha sin edición.

## §2 · COMMIT-2 · emisiones ciegas (`e4e4bc75`)

`corrida0 run CALC-DUELO-ENVIPE2026-EMISIONES-0001` → `corrida_id …--e876d9d730fa`, `exit_code=0`, 762 `RESULT`, sello COINCIDE (`d3f34fcf…`), `resultados.json` sha `28354202…`. `verify` → **REPRODUCE** (CONTEXTO=IDENTICO), 762/762 RESULT. Guardia, en los `RESULT` sellados: `G-RESERVA-OLA-CARGADA-RESERVADA = SI`, `G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO = NO`, `G-RESERVA-GUARDIA-PROBADA = ReservaRota: ENVIPE 2026 está RESERVADA: el cruce no se deriva hasta que las emisiones estén selladas`, `G-VETO-EXD-2025-PROBADO = ReservaRota`. Empujado a `origin` antes de COMMIT-3a (compuerta §8).

## §3 · COMMIT-3a (`00884852`) y COMMIT-3 (`f57bbaf9`)

COMMIT-3a: una línea (`inputs.emisiones_selladas.sha256: PENDIENTE-COMMIT-3a` → `28354202…`); `preflight` de la adjudicación → VERDE. Compuertas: preflight VERDE ✓ · firma §2 presente ✓ · emisiones en `origin` ✓ · FD 2026 verificado por texto ✓ (§1.3).

`corrida0 run CALC-DUELO-ENVIPE2026-ADJUDICACION-0001` → `corrida_id …--008848523778`, `exit_code=0`, 762 `RESULT`, sello COINCIDE (`bcaa9e81…`). `verify` → **REPRODUCE** (CONTEXTO=IDENTICO). `G-EMISIONES-REPRODUCIDAS = SI` (Δ máx 0.0), `G-MEDIDOR-IDENTICO-A-TOOLS = SI`, `G-OLA-NUEVA-ABIERTA = SI`. El código leyó sólo `tmod_vic` y `tsdem` del zip.

## §4 · P5 · Lo que mesa lee primero (sin adoptar) — rótulo **PROSPECTIVA**

Las emisiones se sellaron (COMMIT-2) antes de que existiera R (COMMIT-3); `tests/test_duelo_envipe2026_ejecucion.py` lo lee del historial.

**Cruces — regla v0.3 (spec §4), retador primario SL, 12 celdas puntuadas por par.** ΔMAE = MAE(C2) − MAE(retador), pp.

| par | contendiente | MAE (pp) | ΔMAE (pp) | IC95 ΔMAE | veredicto (spec) | cobertura R∈IC cand. | IC95 Wilson |
|---|---|---|---|---|---|---|---|
| SXD | C2 (piso) | 2.274 | — | — | PISO | 9/12 | [0.47, 0.91] |
| SXD | **SL** (primario) | 2.705 | −0.431 | [−0.910, +0.360] | **NADIE-VENCE** | 8/12 | [0.39, 0.86] |
| SXD | S1 | 3.155 | −0.881 | [−1.688, +0.391] | NADIE-VENCE | 10/12 | [0.55, 0.95] |
| SXD | P | 3.655 | −1.381 | [−3.018, −0.407] | NADIE-VENCE | 6/12 | [0.25, 0.75] |
| SXD | AP | 3.836 | −1.561 | [−2.971, −0.321] | NADIE-VENCE | 7/12 | [0.32, 0.81] |
| EXD | C2 (piso) | 1.624 | — | — | PISO | 10/12 | [0.55, 0.95] |
| EXD | **SL** (primario) | 1.263 | +0.361 | [−0.405, +0.773] | **NADIE-VENCE** | 11/12 | [0.65, 0.99] |
| EXD | S1 | 1.299 | +0.325 | [−0.998, +1.086] | NADIE-VENCE | 11/12 | [0.65, 0.99] |
| EXD | P | 3.655 | −2.031 | [−3.677, −0.550] | NADIE-VENCE | 8/12 | [0.39, 0.86] |
| EXD | AP | 3.488 | −1.864 | [−3.542, −0.344] | NADIE-VENCE | 9/12 | [0.47, 0.91] |

Cobertura por conglomerado (los dos pares juntos, 24 celdas; las celdas de un par comparten réplicas, así que el Wilson es optimista): C2 19/24 [0.60, 0.91] · SL 19/24 [0.60, 0.91] · S1 21/24 [0.69, 0.96] · P 14/24 [0.39, 0.76] · AP 16/24 [0.47, 0.82]. La cobertura es lectura derivada de `…-R-DENTRO-IC-CAND-*` sellados, no un RESULT nuevo.

**Veredicto por par: `NADIE-VENCE` en SXD y en EXD** (vocabulario v0.3 de la spec; el vocabulario `VENCE-AL-PISO / NO-VENCE / C-PISO-ADOPTADO` del encargo es el del diseño ENIGH y no está en esta spec). C2 se sostiene de piso. P y AP pierden con IC que no toca 0 (la regla v0.3 no tiene rótulo de «pierde»: la spec los llama `NADIE-VENCE`); SL mejora a C2 en EXD por punto (+0.36 pp) y empeora en SXD (−0.43 pp), sin despejar en ninguno. **General:** ningún retador vence al piso C2 en la ola prospectiva. No se acuña `C-PISO-ADOPTADO`: este acto no adopta.

**Nacional (no adjudica solo — F7 A; se lee con el origen móvil).**

| estimando | R 2026 [IC95] | K | T3 | T5 | TC | lectura mecánica (medidor) |
|---|---|---|---|---|---|---|
| EN `evade_norma` (n=40 199) | 0.5462 [0.5342, 0.5582] | 0.5628, err +1.65 pp, **fuera** | 0.5820, err +3.57 pp, **fuera** | NO-CONSTRUIBLE (3<5) | NO-CONSTRUIBLE (3<6) | «FILA-4 acotada: ningún contendiente se distingue de otro; FILA-6 candidata: todos yerran en el mismo sentido» · mejor por error: K |
| ND `p_c1_u1` (n=20 462) | 0.2244 [0.2121, 0.2379] | 0.2317, +0.73 pp, dentro | 0.2223, −0.21 pp, dentro | 0.2268, +0.24 pp, dentro | 0.2209, −0.35 pp, dentro | «FILA-3 falsador débil: T3,T5,TC gana en punto, el IC no despeja» · mejor por error: T3 |

Origen móvil sellado (`CALC-DUELO-ORIGEN-MOVIL-0001`), ND, ventana común 2018–2025 (8 olas): MAE K 1.24 · T3 2.18 · T5 1.48 · TC 1.12 pp; cobertura 75 / 62.5 / 62.5 / 50 %. Con eso a la vista: en ND los cuatro contendientes caen dentro del IC de R y sus errores de 2026 (0.2–0.7 pp) están por debajo de su MAE retrospectivo; T3 gana el punto de 2026 pero fue el peor en la retrospectiva — una ola no los separa. EN no tiene ventana común (sólo 3 olas selladas), así que no hay retrospectiva contra la cual leer; K y T3 yerran hacia arriba y el R de 2026 cae fuera de los dos IC (baja de 0.563 a 0.546, primera caída tras dos subidas).

**E+ por eje (EN, T3, 13 celdas comparables):** persistencia gana en 10 de 13; E+ gana en D1, S3 y la celda de edad 60+.

## §5 · Qué NO significa lo de arriba

- No adopta nada: `uso_motor: NO-ADOPTA-NADA` en los dos CALC; celda-D y marcador no se tocan (su dueño consume el veredicto por id, NC-…-c2b4-03).
- `NADIE-VENCE` no es «C2 es correcto»: C2 yerra 2.3 pp (SXD) y 1.6 pp (EXD) de MAE y cubre 19 de 24 celdas; sólo dice que ningún retador mecánico lo supera con IC que despeje, a este n y en una ola.
- `evade_norma` es una proporción entre delitos no denunciados por razones de desconfianza/costo institucional (`BP1_23 ∈ {04,05,06,08}`); su baja de 2026 no dice nada sobre si se denuncia más, ni sobre victimización. ND (`p_c1_u1`) es delito personal no denunciado: su R de 2026 cae dentro de las cuatro predicciones.
- El código 09 de `BPCOD` cambió de redacción en el FD 2026 (§1.3): cualquier movimiento del universo ND podría ser de instrumento; no se ajustó nada.
- La fila `L` (LLM) no entra: firma §2 «Fila L: NO-ENTRA (spec §5)».

## §6 · Verificación y perímetro

`verify` REPRODUCE ×2 · `tests/test_duelo_envipe2026_ejecucion.py` 6/6 (control positivo del test de fuga: el mismo patrón `-R-` con prefijo `ADJ` sí encuentra `…-R-ND-P`/`…-R-EN-P`) · `tests/test_duelo_prospectivo.py` 25/25 · `git log --format=%s`: COMMIT-2 → COMMIT-3a → COMMIT-3. Escrito: los dos CALC (sellos, `ejecucion.json`, `resultados.json`; `spec.yaml` de adjudicación sólo la línea de COMMIT-3a), `forense/replay-evidencia.tsv` (2 filas), `data/corrida0/decisiones.tsv` (1 fila: `reserva:envipe2026-consumida-por-duelo`), `forense/no-corrido.tsv` (4 filas propias + cierre de `NC-…-8796-03`, `-8796-04`, `NC-…-69b5-01`), test propio + su fila de censo, esta nota, hallazgos (1 línea), cascada. `tools/duelo/`, `CALC-DUELO-ORIGEN-MOVIL-0001` y la spec: intocados. `corridas.tsv` no se tocó (derivado protegido; NC-…-c2b4-02).
