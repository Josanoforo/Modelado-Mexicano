**SHA de redacción:** `b7aa67c` (merge #205, `origin/main` en el momento de abrir este acto — ninguna base distinta fue declarada por quien lanzó el encargo)
**Entorno asignado:** NUBE, repo-only. Sin gate.
**Estado:** VIVO

---

ACTO RECONCILIA-PUERTAS — los dos artefactos de ADR-69 y ADR-70

Cierra D11 · Entorno: NUBE, repo-only · Sin gate

**Nota de archivo (A.3).** Este encargo llegó como parte de un despacho único que lanzaba cinco actos en paralelo (ADJ-4 · BENCHMARK-ENLACE · RECONCILIA-PUERTAS · REAPERTURA-52A-54 · ENASIC-SPLIT) más dos notas de mesa (GDELT-UCDP-RECON, D5). Se archiva **verbatim, íntegro**, el texto tal como se recibió — mismo criterio que ADR-72 usó para sus ADDENDA 4/5 (texto completo, no una selección silenciosa de qué parte "aplica"). **Solo la sección `RECONCILIA-PUERTAS` pertenece a este acto**; el resto (`LANZAMIENTO` y sus filas) se archiva por fidelidad de lo recibido, no se ejecuta aquí.

---

Por qué

ADR-70 lo dejó textualmente "pendiente nombrado, de mesa": data/UNIVERSO-MINIMO-FUENTE-v1_0.md (ADR-69, regla de proceso: qué recorrer antes de declarar NO-ENCONTRADO) y data/universo-puertas-2026-08-12.tsv (ADR-70, regla de registro: la RNM entra al universo consolidado) cubren territorio solapado desde dos ADR distintos, y nadie sabe cuál manda cuando difieren.

COMMIT 1 — el mapa del solape

Qué dice cada uno, campo por campo · dónde se solapan y dónde difieren · y la pregunta que hay que contestar: cuando una fuente aparece en los dos con estados distintos, ¿cuál gobierna? Insumo ya derivado que no hay que re-derivar: el puntero tiene 114 filas, de las cuales 62 son gap_mapeo_map_b con universo interno ("buscada en el puntero y en la cola-adquisicion" — dos tablas del propio programa, ningún portal) y ~15 fuentes tienen hoy dos filas contradictorias porque SONDA-1 las sondeó sin retirar la vieja, declarándolo. Ese es el caso testigo de la reconciliación.

COMMIT 2 — la propuesta

No fusiona los artefactos por su cuenta. Entrega a mesa: (a) la regla de precedencia propuesta —candidata: "cuando dos filas describen la misma fuente, manda la de fecha_sondeo más reciente cuyo universo_declarado cite un portal, no una tabla interna"— (b) el diff exacto que la implementaría, y (c) el ADR propuesto que la sellaría. Contador: filas contradictorias del puntero: hoy ~15, propuestas a 0.

LANZAMIENTO
ahora, en paralelo	entorno	cierra
ADJ-4	nube	D2(a) · D6 · D7 · D8
BENCHMARK-ENLACE	nube + web	D4 · D10
RECONCILIA-PUERTAS	nube	D11
REAPERTURA-52A-54	caja + corpus	D1
ENASIC-SPLIT	caja + corpus	D3

Al fusionar ADJ-4: R5.1-D3 (caja). Cuando la caja tenga hueco: GDELT-UCDP-RECON — es el de menor palanca de los siete y el único que llena disco.

⚠️ Tres actos van a caja y P·LOTE-2 puede seguir corriendo ahí. REAPERTURA y ENASIC-SPLIT son de lectura de diccionarios: ligeros. GDELT-UCDP-RECON es el pesado — ese sí espera.

Sin encargo, y a propósito: D5. Mesa decidió esperar a que cierren más entradas del registro antes de sellar A.7. Queda anotado, no se lanza.
