**SHA de redacción:** `ce5e10d` (merge PR #441)
**Entorno asignado:** NUBE A — NO CAJA; puede convivir con E13 en nube B (perímetros disjuntos salvo cascada; renumera quien fusiona segundo)
**Estado:** VIVO

---

ENCARGO · MAESTRA33-E18 · MAPEA-DENTRO-DE-ACTIVOS — invoca /acto (y /mapea)
SHA de redacción: ce5e10d (merge PR #441). ENTORNO: NUBE A — NO CAJA; puede convivir con E13 en nube B (perímetros disjuntos salvo cascada; renumera quien fusiona segundo). COMPUERTA: ninguna. MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim, 2/sep/2026): "Nos resetearon el uso en claude, podemos explotarlo al máximo de aquí al sábado".
A.8 (dirección contra ce5e10d): (1) ESTRUCTURA — reglas del motor: milpa/tramite.yaml (8, vía FP-200-style con sello de mesa); propuestas: milpa/tramite-ola5-propuesta-v0.yaml; θ: milpa/procedencia.yaml; inventarios: data/inventario-reactivos-v1_1(+ext); todo indexado en INFRAESTRUCTURA D4 — cita la línea al arrancar. (2) CONTENIDO — reglas de los 4 dominios ACTIVOS en canon/modelo-decision-v4_0.md sin p medida: se derivan por comando al arrancar (NO-ENCONTRADO como lista: grep de "p=" en tramite.yaml contra las reglas del modelo → deriva). Mapeo previo dentro de activos: solo FP-190 (fase 2), 8 objetos. (3) T25: cita rótulos con serie completa.
P0 · .claude/commands/acto.md, paso 2: una línea COMPUERTA que cite un rótulo sin serie (E<n>, C<n>, A<n>, S<n> sin MAESTRA<nn>-) es AMBIGUA → PARO con cero commits y el texto "rótulo ambiguo: cita MAESTRA<nn>-…". Precedente: #437 resolvió E13 a MAESTRA32-E13.
P1 · Lista derivada: por cada dominio ACTIVO (trámite, cívico, dinero, familia), todas las reglas SI-ENTONCES del modelo sin p medida, con su PORQUE y generador; conteo A.13.
P2 · /mapea por regla (≥3 formulaciones) contra los inventarios; por candidata: encuesta, ola, variable, texto, tipo, en_corpus (manifiesto por la vía del índice), vocabulario A.4. Tabla completa en forense/notas.
P3 · Con las EXISTE-SATISFACE: hasta 3 lotes de caja de ≤4 reglas (REGLAS-OLA6-ACTIVOS-L1/L2/L3), ordenados por olas disponibles en corpus (más olas = más celdas P1 para el marco), cada uno con su spec congelable por regla (variable, dicotomización, universo, ponderador, diseño, escala) listos para /acto — SIN medir nada aquí. Las EXISTE-NO-SATISFACE y NO-ENCONTRADO van como necesidades nombradas al registro del curador por la vía de A5 (decide_acquisition o vía manual precedentada), no a ninguna tabla nueva.
PERÍMETRO: acto.md (P0), forense/notas, forense/encargos/ (3 borradores LISTO-CAJA), data/curacion-registro/* (por script), tablero (recibo), A.3, cascada. Frase exacta vigente. FP/ADR: deriva. CONTADOR: cero (mapeo); reglas candidatas EXISTE-SATISFACE +N, declarado.
LO QUE NO HACE: no mide p; no carga reglas; no toca el marco-M; no abre dominios nuevos.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-E18 · MAPEA-DENTRO-DE-ACTIVOS`, 1/sep/2026,
rama `claude/maestra33-e18-mapeo-activos-ts2huk`. P0:
`.claude/commands/acto.md` paso 2. P1:
`forense/notas/2026-09-01-MAESTRA33-E18-P1-reglas-activos-sin-p.md`. P2:
`forense/notas/2026-09-01-MAESTRA33-E18-P2-mapeo-tabla.md`. P3:
`forense/encargos/2026-09-01-MAESTRA33-E18-P3-REGLAS-OLA6-ACTIVOS-L1.md`.
Cascada: `canon/gobernanza-v1_15.md` ADR-270 (renumerado de `ADR-269`
candidato tras choque con `ACTO MAESTRA33-E13 · AGREGA-1`/`PR #444`, que
fusionó primero y tomó el `269`), `canon/estado-programa-v1_10.md` L0,
`canon/registro-rotulos.tsv`, `tests/check.py::_T25_ARCHIVOS_CONOCIDOS`.
PR: ver el PR abierto contra `main` desde esta rama.
