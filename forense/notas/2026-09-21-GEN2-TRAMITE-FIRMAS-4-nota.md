# ACTO GEN2-TRAMITE-FIRMAS-4 · nota de una página (21/sep/2026)

Encargo: `forense/encargos/2026-09-21-GEN2-TRAMITE-FIRMAS-4.md` (archivado verbatim por 0-bis A.3, sidecar `.cuerpo.sha256` sellado). SHA de redacción declarado: `33d97e12`; base real al abrir: `159edaf` (main al día, 0 commits de diferencia). ENTORNO: NUBE `milpa-inegi` (sonda a `www.inegi.org.mx` → 200; `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`; corpus `data/raw` ausente, esperado en nube).

MODO: `ABIERTO`. Compuerta: ninguna.

## 1 · Firmas (§2, F1–F8)

Las ocho quedaron `FIRMADA` en `forense/firmas-pendientes.tsv`, ids `FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-01` a `-08`, cada una con el texto verbatim de mesa y su verificación por objeto:

- **F1/F2 (lote ENIF2024)**: no existía firma equivalente en el repo (búsqueda por objeto, cero coincidencias). Asentadas de cero.
- **F3 (TUBERÍA)**: rastro parcial confirmado — la parte de esquema de ids NC/FP a raíz de acto ya está firmada y ejecutada por `FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01/-02`. Esta fila (-03) asienta solo lo que faltaba: L0 auto-derivada narrativamente y "T16 deja de re-ejecutar la suite", que siguen sin mecanismo construido.
- **F4, F5, F6, F8**: sin rastro previo, asentadas de cero. F6 cita que `MOTOR-THETA-CONGELADA-1` ya está en main y no se relanza (verbatim del propio encargo).
- **F7-reserva**: rastro parcial confirmado — la reserva base de ENVIPE 2026 ya vive en `data/corrida0/decisiones.tsv` (clave `reserva:envipe2026`, adenda de `GEN2-TRAMITE-FIRMAS-3`). Esta fila (-07) asienta solo las tres enmiendas de dirección (A)(B)(C) que faltaban.

Ninguna firma lanza el acto que autoriza (lote ENIF2024, duelo ENVIPE2026, TUBERÍA, D-22 ampliada, θ, `evasion_norma`): eso es "no hace" explícito del encargo (§6).

## 2 · Diseños archivados (§3)

**NO-OBTENIDOS.** Los dos adjuntos (`DISENO-LOTE-CRUCES-ENIF2024-protocolo-unico-v0_1.md` sha256 `f9ea6d4f…` y `DISENO-duelo-prospectivo-ENVIPE2026-v1_0.md` sha256 `e88d3192…`) no llegaron a esta sesión. Se buscaron por nombre en todo el árbol (`find . -iname`) y no están en el repo bajo ningún acto anterior. No se fabricó contenido con esos hashes (sería fraude de procedencia, §2 del proyecto). Van a `## NO-CORRIDO / RESERVAS` con `PARO-PREMISA`, sucesor `SIN-ASIGNAR` — quien los tenga (dirección/MOTOR) los adjunta a un acto sucesor.

## 3 · Descargas (§4, D1–D4)

- **D1 (ENVIPE 2026) y D2 (ENIGH 2024)**: encoladas en `data/curacion-registro/cola-adquisicion-registro.tsv` (filas `residual:ENVIPE_2026` prioridad 1, `residual:ENIGH_2024_NC` prioridad 2) con la regla de reserva F7 escrita en la fila de D1 (baja+hashea, NO descomprime/lista/abre, tabulados NO se bajan). Vista regenerada con `python3 tools/vista_cola_adquisicion.py` (155→157 filas). **Línea exacta para mesa:** `/adquiere` (camina toda la cola elegible) o `/adquiere 2` (limita a estas dos filas si se corre justo después de encolarlas, dado el orden por prioridad).
- **D3 (cuestionarios ENIF 2012/2015 PDF)**: **OBTENIDOS los dos**, en `milpa-inegi`, con egreso real a INEGI. El patrón `enif_AAAA_cuestionario.pdf` (con guion bajo) da `HTTP 200` para 2012 pero con el cuerpo de la plantilla "Página no encontrada" — hallazgo aparte en `hallazgos.md`. La URL real de 2012 es `enif2012_cuestionario.pdf` (sin guion bajo). Registrados en `data/manifiesto.yaml`: `enif_2012_cuestionario_pdf` (855195 bytes, sha256 `b7fc1f4a…`) y `enif_2015_cuestionario_pdf` (676127 bytes, sha256 `10688412…`), ambos vía `tests/manifiesto.py --registra`. Por PR #77, los dos PDF se removieron de `data/raw/` tras registrar — el payload físico queda pendiente de que caja lo traiga por `--descarga --id`.
- **D4 (¿ola nueva de ENSAFI/ENFIH?)**: **NO-ENCONTRADO** (A.4). Las páginas de programa `/programas/ensafi/` y `/programas/enfih/` sólo enlazan `2023` y `2019`. Tanteo directo de `ensafi/2024,2025` y `enfih/2022,2024` — las cuatro devuelven `HTTP 200` con `<title>Página no encontrada</title>`, mismo defecto de "200 no es éxito" que D3. No se afirma "no existe": otro patrón de URL podría revelar una ola que este sondeo no vio.

## 4 · Perímetro y lo que queda pendiente

Tocado: `forense/firmas-pendientes.tsv`, `forense/hallazgos.md`, `data/curacion-registro/cola-adquisicion-registro.tsv` + vista regenerada, `data/manifiesto.yaml` (D3), esta nota, la cascada de cierre. No se tocó código de motor, specs, CALC, ni `tools/emite_m.py`. No se relanzó θ. No se escribió el encargo del lote ENIF2024 ni el del duelo ENVIPE2026 (dirección).

Pendiente (ver `## NO-CORRIDO / RESERVAS` del encargo archivado): los dos diseños de §3 (PARO-PREMISA, no llegaron); D1/D2 quedan en cola, no ejecutados por diseño del encargo (microdato → caja siempre); F3 y F7 dejan mandatos firmados sin mecanismo construido (TUBERÍA, COMMIT-1/2 del duelo).
