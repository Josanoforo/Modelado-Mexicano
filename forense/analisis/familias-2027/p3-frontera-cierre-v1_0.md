# P3 · frontera-1 (#1195) y astra6-cierre-material-1 · identidades, rótulo de oros y cruces «consumidos» · v1.0

Acto: GEN2-ASTRA-CONTINUIDAD-C2-1 · pieza P3 · HEAD `ba6ccd23`, origin/main fetch en sesión (último merge visible #1248 `b88b92b1`). Contadores movidos: cero. No se abrió microdato ni ola reservada.

## 1 · Tabla de dictámenes y objetos

sha256 = `sha256sum` EJECUTADO en esta sesión. «Casa» = EJECUTADO `sha256sum -c` contra el registro indicado (en frontera, además, contra `frontera-inventario.json`: 32/32 COINCIDE).

| Dictamen | Objeto | Ruta (bajo forense/analisis/) | sha256 | ¿Casa con registro? | Oro: ola vista · rótulo |
|---|---|---|---|---|---|
| ENOE-INFORMALIDAD · NO-LANZAR-BAJO-CONTRATO-PROPUESTO (singleton) | paquete: spec.yaml | familias-2027-frontera-1/paquetes/ENOE-INFORMALIDAD/enoe-spec.yaml | 8e2db05c3ddd40d600e777159dd4b6c3ee8b5e8b7ab84c68063293230585c875 | OK enoe-hashes.sha256 (7/7) | — |
| idem | paquete: spec humana | …/ENOE-INFORMALIDAD/enoe-spec-humana.md | c8c218562cca2445513ab70d27355422c856845051d10d3328e78572848c1b93 | OK enoe-hashes | — |
| idem | paquete: lector | …/ENOE-INFORMALIDAD/enoe_lector.py | 171d79a9ff9ebd0b3b44e7586e67befbe6072d02600e487c14cbaa95d056520a | OK enoe-hashes | — |
| idem | oro | …/ENOE-INFORMALIDAD/enoe-oro.json | 9174bad5645deff3f9f6b04b1a6c8a8dc6bc20983d16779e9db374aa7ad96258 | OK enoe-hashes; = `oro_sha256` en frontera-disposiciones.json | 2024T4 (payload 817f28d2…7305) · estado DIAGNOSTICO-HISTORICO-ABIERTO · `retador: null` → descripción/calibración retrospectiva, no retador |
| idem (sucesor #1222) | potencia | familias-2027-enoe-inferencia-1/potencia/enoe-escenarios.tsv | 45e969c32343e6f3be3d32affcc57c6c67b8ffaed833f392639cfa4970e9c398 | OK enoe-producto.sha256 | idem |
| ENSU-CAMPECHE-INSEGURIDAD · NO-LANZAR-BAJO-CONTRATO-PROPUESTO (potencia) | paquete: spec.yaml | familias-2027-frontera-1/paquetes/ENSU-CAMPECHE-INSEGURIDAD/ensu-spec.yaml | beb72e88ed8cacb2c054bd45e0f93a6e08da9217c44d943cd7d1e0df594eaaf9 | OK ensu-hashes.sha256 (7/7) | — |
| idem | paquete: lector | …/ENSU-CAMPECHE-INSEGURIDAD/ensu_lector.py | 9332b45565afbce445c4bbecc7366b06aae7c8b50a199efdc4fe94b393744d7b | OK ensu-hashes | — |
| idem | oro | …/ENSU-CAMPECHE-INSEGURIDAD/ensu-oro.json | 43b294091a6da33855498d0a7bd22134ada513796456b27b7bdcd30d55e00e94 | OK ensu-hashes; = disposiciones | 2025T4 (payload 317ed14f…, id manifiesto `ensu2025_bd_csv_zip`, sin `estado_reserva`) · DIAGNOSTICO-HISTORICO-ABIERTO · `retador: null` |
| ambos | potencia | familias-2027-frontera-1/potencia/escenarios.tsv | 0fab087249723cd3b201a22b74ed59d6e71311eaa2980026666b79df6585d1bb | OK frontera-inventario.json | — |
| ambos | potencia | familias-2027-frontera-1/potencia/frontera-potencia-resultados.json | 916f59201e11702f9646d2b7eb5f2b9dc9ac7dee41487fd6cc7475bfecf7b0a4 | OK frontera-inventario.json | — |
| ambos | disposiciones | familias-2027-frontera-1/frontera-disposiciones.json | 0163b6b39e333a591409d0cd9618e0ab915a09c73dde07cda8dc6cd5e0a9a7ae | OK frontera-inventario.json | — |
| cierre-material: ENCIG-PAGO-DIGITAL SUSPENDIDO/NO-ESTIMABLE; ENIF ×2, ENCIG-MORDIDA, ENVIPE ×2 CONDICIONAL | hoja común | familias-2027/astra6-cierre-material-1/hoja-comun.tsv | 330288e198d6fa57aa6a14d8f02e0897d83c090f42e3f4279f151b118dc6399a | OK paquete-control-hashes.json | ENIF/ENCIG/ENVIPE: oros = RESULT sellados (p0 citados por result_id); emisión PROSPECTIVA hacia olas 2027 |
| idem | nota / hoja firma | …/cierre-material-nota.md · hoja-firma-propuesta.md | 0dcdfc89…8683 · 8cc5d8ef…0da3 | OK paquete-control-hashes.json | — |
| idem | contrato ENIF | …/contrato-efectivo-enif.md | 8f1e75a3…0085 | OK paquete-control-hashes.json | — |

EJECUTADO: `paquete-control-hashes.json` 18/18 COINCIDE (14 archivos del acto + 4 de tools/familias-2027/cierre-material-1/). Ningún hash-discordante ni AUSENTE (A.1) en los tres registros.

Rótulo de oros (regla 6): LEÍDO en `enoe-spec.yaml:52` y `ensu-spec.yaml:28` `retador: null`; `enoe-spec-humana.md:3` «No retador»; `enoe-hoja-decision.md` «Todo aquí es RETROSPECTIVO/planificación informada». Los oros 2024T4/2025T4 son olas ya vistas usadas para p0 y potencia → rótulo correcto: **RETROSPECTIVA (descripción/calibración)**, no retador; no hay RETROSPECTIVA-MECÁNICA (no hay validación de origen móvil). Conforme a regla 6.

Pregunta a verificar (no hecho): el incidente de #1242 (`reports-v2/salud-juventud-tiempo-1/tiempo/incidente-documental-olas-reservadas.md:3`) trata «ENSU dic/2025» como publicación de ola reservada, mientras frontera-1 usa ENSU 2025T4 como oro abierto (manifiesto sin `estado_reserva`). O la ENSU 2025T4 ya no es la última ola (hay 2026T1–T2 publicadas) y el incidente sobre-declaró, o el oro de frontera tocó una ola reservada. Mesa/recibo debe resolverlo contra el manifiesto por id.

## 2 · «Ambos grupos y escenarios completos obligatorios» (REPORTADA → verificada)

LEÍDO `familias-2027-frontera-1/potencia/calcula.py:17-50`: `EXPECTED_GROUPS=('1','2')`, `TEMPORAL_SCENARIOS=(0,.01,.03)`; `gold_family` bloquea GRUPO-AUSENTE / GRUPO-NO-PREVISTO / SE nula o inválida; `complete_family` exige que no haya bloqueo, que el conjunto de (grupo, ρ, escenario) sea exactamente el esperado sin duplicados y SE oro/futura finitas y positivas; si no, no hay PREPARAR-LANZAMIENTO-CONDICIONAL. **Se sostiene en el código** (EXISTE-SATISFACE). Matiz: el nombre literal «obligatorios» en el paquete solo aparece como `campos_obligatorios` (spec.yaml); la obligación de cobertura vive en `calcula.py` y en `frontera-correccion-grupos.md:3`, no en el spec del paquete. No se corrió `frontera_test_potencia.py` en esta sesión (NO-CORRIDO abajo).

## 3 · PR #1242 y #1248: cruces propuestos como «consumidos»

EJECUTADO `git log --oneline origin/main`: `4037264f Merge #1242` (codex/astra6-c3-salud-juventud-tiempo-1) y `b88b92b1 Merge #1248` (GEN2-RECIBO-ASTRA6-3). La propuesta está en `recibo-astra6-3/hoja-para-mesa-recibo-astra6-3.md:20-21` (FP-260927-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1-b544-02): «se declara consumido para esos cruces (E.6)» — pero enumera **olas/publicaciones** (EDER2025, ENADID2023, ENCODAT2025, ENUT2024/ENIF2024/ENSU-dic2025), no cruces. Por E.6 lo consumido es el cruce visto; la firma debería listar estos:

| Cruce visto (instrumento × estimando) | Evidencia (archivo:línea) | Tipo de exposición |
|---|---|---|
| EDER 2025 × salida del hogar antes de 18 por cohorte | reports-v2/salud-juventud-tiempo-1/juventud/revision-material.md:24; juventud/tabla.tsv:2 (JUV-001) | extracto web de comunicado |
| EDER 2025 × primera unión antes de adultez por cohorte | revision-material.md:24; tabla.tsv:3 (JUV-002) | idem |
| ENADID 2023 × fecundidad adolescente (cambio 2018→2023) | revision-material.md:24; tabla.tsv:5 (JUV-004) | extracto PDF de resultados |
| ENADID 2023 × tasa global de fecundidad | revision-material.md:24; tabla.tsv:6 (JUV-005) | idem |
| ENCODAT 2025 × nota de cuestionario / comparabilidad serie opioides | salud/incidente-documental-encodat2025.md:7; salud/afirmaciones.tsv:40 (SALUD-039) | fragmento de búsqueda; tabla de prevalencias NO leída (misma línea 7) |
| ENUT 2024 × tiempo disponible (TIME-002/-019/-020) | tiempo/incidente-documental-olas-reservadas.md:5 | publicación consultada |
| ENIF 2024 (publicación externa) × metas de ahorro/planeación (TIME-001, T-EXTRA-01) | incidente-documental-olas-reservadas.md:5 | idem |
| ENSU dic/2025 × percepción de amenaza (TIME-016) | incidente-documental-olas-reservadas.md:5 | idem |

No listado como cruce (pregunta a verificar): ENIGH 2024 (salud/afirmaciones.tsv:14 dice «no se reabre») y ENCODAT 2025 binge/regional (afirmaciones.tsv:9,18) aparecen solo como SIN-CIFRA por reserva, sin evidencia de haber sido vistos → no consumidos. La ola completa no queda consumida: los demás cruces de EDER 2025, ENADID 2023, ENCODAT 2025, ENUT 2024, ENIF 2024 y ENSU 2025T4 siguen disponibles para una prueba pre-registrada. Recomendación de texto: sustituir «esos cruces» por la enumeración de la tabla.

## NO-CORRIDO / RESERVAS
- `frontera_test_potencia.py` y `frontera-verifica.py` no se corrieron: DIFERIDO-A recibo; la afirmación §2 descansa en LEÍDO de código.
- Tensión ENSU 2025T4 reservada/abierta: DECISIÓN-DE-MESA-PENDIENTE (consulta por id en manifiesto y regla de reservas).
