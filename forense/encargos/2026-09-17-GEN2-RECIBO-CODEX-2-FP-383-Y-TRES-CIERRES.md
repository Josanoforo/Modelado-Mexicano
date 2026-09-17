# ENCARGO · ACTO GEN2-RECIBO-CODEX-2 · RECIBO DE LA SEGUNDA TANDA CODEX + FP-383 + TRES CIERRES DE MESA

**CABECERA** · redactado contra `67fa97e`; re-deriva al abrir · **ENTORNO: NUBE** — cero microdato · **COMPUERTA:** ninguna · MODELO SUGERIDO: **Sonnet** (recibo mecánico; sube a Opus si una pieza dejada a mesa exige juicio) · FP/ADR/NC: deriva al cierre, no heredes (máximos hoy: FP-384, NC-0314, ADR-539) · vehículo: `/acto` · **una sola sesión:** si al arrancar ya existe una rama con este encargo archivado, PARA — TRÁMITE-4 corrió dos veces (#845/#848) por eso.

**FIRMAS DE MESA, verbatim (cerradas en conversación de dirección el 17/sep/2026; su archivo aquí las sella):**
> **FP-383:** "(a) Las 89 celdas IDÉNTICO salen de la comparación M-vs-R con rótulo 'emisor = árbitro'. (b) Ola anterior del mismo instrumento se lee como persistencia, no como acuerdo. (c) Mismo payload con otra dicotomización NO es comparación: el emisor queda fuera del marcador por segmento. El marcador se rediseña sobre el catálogo de momentos — estimadores adjudicados por celda-D contra R — gated por celda a NC-0239 y a la columna de segmento del marco del árbitro (NC-0300)."
> **NC-0293:** "Los 24 campos con 'ausencia declarada de facto' reciben el token propio `AUSENCIA_DE_FACTO(censo E1 §3)`, distinto de `AUSENCIA_DECLARADA`; se añade al vocabulario de la capa con su definición."
> **NC-0295:** "El universo vive en la capa E1; `procedencia.yaml` no se toca; `fuente:+n_util:` no es universo declarado."
> **NC-0282:** "La referencia pedida es el hallazgo de fecha 17→16/sep registrado por ADR-534 P3(b); rige 16/sep; cierra."
> **Recibo (D5, ya sellada por ADR-534):** "Los PR del carril Codex entran al tablero por un recibo en lote por tanda."

**VERIFICACIÓN DE EXISTENCIA (A.8, dirección, contra `67fa97e`):**
- (1) Estructura: Dominios 7/8/9, `no-corrido.tsv`, `decisiones.tsv`, `milpa/theta-esquema-e1-v1_0.yaml` (capa E1, ADR-535). Cubren.
- (2) Contenido: la tanda sin recibo son los merges #832–#843 (`acto/gen2-wbes2023-descriptiva-1`, `l8-linaje-heredado-1`, `enco-dos-olas-reservadas-1`, `relevo-remesas-f3-1`, `encrige-carga-intensidad-1`, `codex/gen2-wbes2023-precision-1`, `envipe-u4-2013-2015-1`, `gen2/encig2023-flujo-estimando-1`, `mociba-flujo-documental-1`, `relevo-encuci-f2-1`, `enigh2022-intensidad-remesas-1`, `enaproce-instrumentos-acceso-1`) más las rutinas del 17/sep (`adq`, `censo`, `derivados`, despacho) cuando fusionen. ADR-534 recibió #824–#831; de #832 en adelante: NO-ENCONTRADO ningún ADR de recibo (`grep "#83[2-9]\|#84[0-3]" canon/gobernanza-v1_15.md` → reporta el conteo). FP-383 `ABIERTA`; NC-0282/0293/0295 `ABIERTA` con `DECISION-DE-MESA-PENDIENTE`. Hallazgo sin fila: TRÁMITE-4 corrió en dos sesiones (#845 cerrado sin fusionar, cero aporte: `merge-tree` idéntico a main).
- (3) Cobertura retroactiva: los PR de la tanda nacieron después del recibo de ADR-534; ninguno pudo entrar a él.

### PIEZAS

**P1 · Recibo #832–#843 (+ rutinas del 17/sep).** Un ADR de recibo en lote: por PR, rama · producto (CALC sellado / nota / tabla) · contador declarado · qué dejó a mesa (leer su encargo o nota de cierre). No registra corridas: eso es `GEN2-REGISTRO-CAJA-1` (caja, en paralelo); el ADR cita que 12 de estos PR dejaron CALC sellados en disco pendientes de registro. Una NC por pieza dejada a mesa, con sucesor.

**P2 · FP-383 → FIRMADA con el verbatim;** NC-0275 → CERRADA citando FP-383 y este acto; NC-0300 recibe enmienda fechada (columna de segmento del árbitro = prerrequisito del marcador, sucesor `GEN2-MARCADOR-REDISENO-1`, que redacta dirección). Fila en `decisiones.tsv` (objeto `marcador:emisor-fuera`).

**P3 · Tres cierres de mesa.** NC-0293: añadir al vocabulario de `milpa/theta-esquema-e1-v1_0.yaml` el token `AUSENCIA_DE_FACTO(censo E1 §3)` con definición, y aplicarlo a los 24 campos (lista derivada del propio archivo, conteo pegado); test de la capa actualizado si asierta el enum. NC-0295: enmienda fechada en la capa declarando que el universo vive ahí; ninguna edición en `procedencia.yaml`. NC-0282: CERRADA citando ADR-534 P3(b) y la firma. `decisiones.tsv`: una fila por cierre.

**P4 · Hallazgo del duplicado.** Línea en `hallazgos.md` (PARA-v2.14): "TRÁMITE-4 corrió en dos sesiones del mismo entorno (#845 cerrado, #848 fusionado); ENTORNO ASIGNADO no basta: el encargo nombra la sesión o la rama, y la skill PARA si el encargo ya está archivado en otra rama viva" — que es la primera línea de la cabecera de este encargo, aplicada a sí mismo.

**PERÍMETRO Y CONCURRENCIA:** `canon/gobernanza-v1_15.md` (ADR de recibo + ADR del acto) · `forense/firmas-pendientes.tsv` · `forense/no-corrido.tsv` · `data/corrida0/decisiones.tsv` · `forense/hallazgos.md` · `milpa/theta-esquema-e1-v1_0.yaml` (P3) · `tests/test_theta_esquema_e1.py` (solo si asierta el enum) · nota de cierre · cascada. **No toca** `procedencia.yaml`, `data/corrida0/` (registro es de caja), `milpa/src/`, el marcador ni el catálogo. En paralelo: `GEN2-REGISTRO-CAJA-1` (caja: derivados de `corrida0`) — sin archivo común salvo el tablero al cierre; las ramas de rutina — sin archivo común. «Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»

**CONTADOR:** cero mediciones, dicho sin disfraz; una FP a FIRMADA, cuatro NC cerradas, N NC nuevas (reportado). **LO QUE NO HACE:** no registra corridas · no rediseña el marcador (lo redacta dirección con FP-383 firmada) · no toca `procedencia.yaml`. **SUCESORES:** `GEN2-MARCADOR-REDISENO-1` (dirección) · `GEN2-GUARDIAS-1` (NC-0302/0305/0309/0313, tests) · bandera `--excluye` del registro. **CIERRE:** cascada + `## NO-CORRIDO / RESERVAS` + `## CONSUMIDO`.
