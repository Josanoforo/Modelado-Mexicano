# ACTO GEN2-OBTENCION-EXTERNA-1 · nota de cierre

Encargo: `forense/encargos/2026-09-27-GEN2-OBTENCION-EXTERNA-1.md` (A.3; sha256 del adjunto recibido `09b41e34…4b853c`; SHA de redacción `eda5bb9f`). Rama `acto/gen2-obtencion-externa-1`, 0-bis `81e18980`. ADR `ADR-260927-GEN2-OBTENCION-EXTERNA-1-81e1-01`.

**Contadores movidos: cero mediciones, cero adopciones.** Lo único que se mueve es `payloads` del manifiesto (§5).

## 1 · Arranque (salida cruda, resumida)

- `git rev-list --count HEAD..origin/main` → 0 al abrir; `git status --porcelain` vacío; duplicado: sin rama, worktree ni PR con `OBTENCION-EXTERNA` (0.c); `limpia_arbol --reporta`: base al día, `fuera_de_politica: 0`.
- `tools/entorno.py --arranque`: `ENTORNO-DERIVADO = CAJA` · `montado=SI archivos_examinados=512` · `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable` · `red: PERMITIDA (http_code=200)`. El encargo pide CAJA: coincide.
- `data/raw` enlazado a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiado del clon padre y ampliado (local, gitignorado) con `reserva_respondentes: /home/pc0/mm-corpus/reservas-respondentes`, para que `--verifica` resuelva las olas reservadas.
- Adjuntos (§3 del encargo): **no llegaron**. Ni el informe de investigación del 27/sep ni `REVISION-repo-y-fuentes-alternas-2026-09-27.md` están en `Descargas MX` ni en `Downloads` (listados con `ls -t` fuera del sandbox). El §1 del encargo es autosuficiente; sus cifras se tratan como [REPORTADO] y se re-verifican al bajar.

## 2 · Premisas re-derivadas (A.15, por id, 7 049 entradas examinadas)

| premisa del encargo | rótulo | lo que dice el manifiesto hoy | efecto |
|---|---|---|---|
| ECRIGE-CDMX 0 entradas | EJECUTADO | 0 (patrón `ecrige\|catalog/601\|regulatoria.*cdmx`) | se sostiene |
| ENVE: «hoy 2016 y 2024» | EJECUTADO | 7 entradas: **2012, 2014, 2016, 2018** (todas bases de *ejemplo* de 2.3–2.5 KB; 2018 reservada) + 2024 (datos abiertos + 2 cuestionarios) | cae (logística): las olas existen pero sólo como ejemplo; P1 completa lo público por ola |
| ENCRIGE 2016 sólo ejemplo | EJECUTADO | `cc1_inegi_encrige_2016__ejemploencrige_csv` (6 116 B, reservada) + página de programa | se sostiene |
| ENCIG 2025 FD/cuestionario «si no está» | EJECUTADO | `encig25_cuestionario_pdf` y `encig25_estructura_base_datos_pdf` **ya están** | EXISTE-SATISFACE; nada que bajar |
| `zenodo_electoral…` y `ine_conteos_censales…` «ya en corpus» | EJECUTADO | zenodo: 1 zip v1 «Static» (739 952 144 B); conteos: sólo 2024 (+ prisión preventiva y voto anticipado 2024); 2009–2021 SIN-FETCH por host `portal-pruebas.ine.mx` caído el 1/sep | P2 verifica versión y reintenta olas |
| Imai-King-Velasco 2020 por bajar | EJECUTADO | **OBTENIDO** por GEN2-ASTRA5-U5 (fila `ASTRA5-U5:IMAI-KING-VELASCO-REPLICA_2020`) | se cita; P3 sólo compara archivos |
| `python3 tools/manifiesto.py verifica <id>` | EJECUTADO | la herramienta es `tests/manifiesto.py --verifica --id <id>` | logística; se usa ésa |
| registro por `/adquiere` | EJECUTADO | `tests/manifiesto.py --registra` aborta por dos entradas ajenas con `estado_reserva` fuera de vocabulario (`enoe_2026_1t_*`, FP-…-43d6-02) | se registra por apéndice validado, mismo método que CORPUS-COMPLETO-1 (`registra_obtencion_externa.py`) |

Regla de reserva aplicada (fila `reserva:ola-nueva-de-encuesta-con-historia` de `data/corrida0/decisiones.tsv`, lectura operativa (a): «encuesta con historia» = el manifiesto ya trae ≥ 1 ola): ENVE 2018/2020/2022, ENCRIGE 2016 y toda ola de ECCO distinta de 2023 entran RESERVADAS; ENVE 2012/2014/2016 (olas ya abiertas), ECRIGE-CDMX 2019 (encuesta sin historia en el corpus) y todos los registros administrativos (INE, IECM, Mecanismo, QQP) entran ABIERTOS. Se declara para que mesa lo corrija si lee otra cosa.

## 3 · Instrumento

- `forense/analisis/obtencion-externa-1/baja.py`: doble descarga con UA de navegador, sha crudo y neutralizado (A.7), estructura (ZIP `testzip`, PDF `%%EOF`, JSON), detector del soft-404 de INEGI. **Control positivo** (antes de usarlo): `ejemploencrige_csv.zip` → sha `6e0dfb28…9b772`, idéntico al manifiesto; **control negativo**: ruta inventada → `FALLO-SOFT404-HTML` (2 263 B). Los dos archivos de prueba se borraron.
- `forense/analisis/obtencion-externa-1/registra_obtencion_externa.py`: deriva sha y tamaño del disco, exige bitácora A.7, deduplica por sha, anexa con validación completa.
- Ejecución: P1, P2(i–ii), P2(iii–iv) y P3 en cuatro subagentes Sonnet con perímetro propio (sólo su `lote-*.tsv`, su bitácora y su carpeta); P4, el registro y la auditoría en el hilo principal (Opus). Declarado según D-13 y la cabecera del encargo.

## 4 · P4 · solicitudes con identidad

Once archivos en `forense/analisis/obtencion-externa-1/solicitudes/` (índice `00-LEEME.md`). Vía verificada en la sesión: LGTAIP (DOF 20-03-2025) bajada y registrada (`oe1_p4_lgtaip_dof_2025_03_20_pdf`), arts. 3-V, 130, 134, 144 leídos; PNT viva con módulo SISAI. Estado por letra: (a) Banxico, (b) IECM, (c) Segob, (d) Félix-Brasdefer, (e) Delaney/FIU, (f) Worldpanel: PREPARADA, NO ENVIADA · (g) LM INEGI: **CONDICIONADA** (MAPA-INSTRUMENTOS-ALTERNOS-1 sólo tiene su 0-bis; no hay conclusión que aplicar) · E1: cuatro registros listados con URL comprobada.

## 5 · Hallazgo lateral: la NC de caja de OBTENCION-PREVIA-1

`NC-260928-GEN2-OBTENCION-PREVIA-1-8e6a-02` (ABIERTA, «DIFERIDO-A:caja -- bajados desde nube; no están en el corpus compartido»). Al verificar `P4-I1` por id, los 14 payloads que ese acto registró desde nube estaban AUSENTES en caja. Se trajeron por id y **14 de 14 COINCIDEN** (`tests/manifiesto.py --verifica`): 1 por `--descarga --id` (el ZIP de datos abiertos), 13 por curl con comparación de sha contra el manifiesto antes de colocar (`--descarga` rechaza URL sin extensión: las 8 páginas de programa y las 5 descargas del RNM). La fila NC no se edita (es ajena; PARO b): **mesa o el trámite la cierra citando esta nota**. Además, la solicitud del LM de ese acto cita el formato en una ruta que no es la registrada: el mismo sha (`5a5d041d…`) está bajo `inegi_laboratorio_microdatos_solicitud_uso`.
