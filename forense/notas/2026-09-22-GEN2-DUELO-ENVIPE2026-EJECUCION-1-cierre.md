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
