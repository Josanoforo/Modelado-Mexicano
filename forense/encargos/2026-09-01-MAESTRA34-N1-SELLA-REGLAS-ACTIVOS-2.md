ENCARGO · ACTO MAESTRA34-N1 · SELLA-REGLAS-ACTIVOS-2 — invoca /acto
SHA de redacción: 8598a72 (merge PR #447). Redacta dirección (Fable), 1/sep/2026, contra v2.12. Estado: LISTO PARA LANZAR — firmas D1-a y D5-b incorporadas; compuerta de sustancia (#447) cumplida al redactar, re-verifica con git fetch. Relanzamiento de MAESTRA33-S2 (ADR-271, "sello sin insumo"); el insumo ya existe: PR #447 fusionado.

ENTORNO ASIGNADO: NUBE (cloud_default). NO se lanza en UBUNTU. MODELO SUGERIDO: Sonnet (propagación mecánica, precedente MAESTRA32-E20-P0).
CARRILES: MAESTRA34-L1 corre en caja en paralelo; perímetros disjuntos salvo cascada; renumera quien fusiona segundo.

COMPUERTA: PR de EJECUCIÓN #447 (ACTO MAESTRA33-E18-P3 · REGLAS-ACTIVOS-L1) fusionado en origin/main con entradas MEDIDO·p que lo citen en milpa/tramite-ola5-propuesta-v0.yaml — cumplida al redactar, re-verifica con git fetch — Y este encargo archivado por PR [COLA] fusionado por mesa (esa fusión ES la firma). Si falta cualquiera, cero commits.

FIRMAS DE MESA — verbatim, 1/sep/2026 (mensaje único de mesa: «D1 - a,  D2-b,  D3-a, D4-a, D5-b si ya dio frutos se mantiene.»). La firma formal es el merge del PR [COLA] que archiva este encargo; el ejecutor propaga, no decide (SELLA-3).
- D1-a: se APRUEBAN ambas tal cual, tier FUERTE-MEDIDO —
  · familia.seguro.volatilidad_ausencia_estado → recibe_remesas p=0.045694 [0.043754, 0.047711], n=90,102 hogares, ENIGH 2022, serie 6 olas informativa.
  · dinero.planeacion.formal_estable → tiene_afore p=0.538502 [0.526700, 0.550616], n=17,765 hogares, ENFIH 2019.
  Lectura de dirección de «tier FUERTE-MEDIDO» (D1-a): el motor no tiene ese token; se propaga como `tier: FUERTE` (el que §3.1 y §3.5 de canon/modelo-decision-v4_0.md ya declaran para R1.2 y R5.1) con `clase: "MEDIDO·p(tasa base ponderada)"` en las p. No se crea tier nuevo.

CARGA — campo por campo, cerrado por dirección contra 8598a72 (formato = precedente de las tres tasas base ya en milpa/tramite.yaml l.193-251):
· familia.seguro.volatilidad_ausencia_estado (R5.1, modelo §3.5 l.535)
    situacion: PENDIENTE-DE-MESA · si.disparadores: {} · disparadores_estado: "el SI de §3.5 (segsoc=2 ∨ residencia ∈ {EUA, Otro país} ∨ hogar con remesas P041) es circular con el desenlace medido (recibe_remesas) y sus mitades no circulares no existen en concentradohogar; tasa base incondicional sobre universo completo de hogares, declarado en #447"
    entonces: recibe_remesas 0.045694 / no_recibe_remesas 0.954306, clase MEDIDO·p(tasa base ponderada)
    porque: {generador: [G5], mecanismo: "la familia opera como seguro (corresidencia, pooling, remesas) ante ingreso volátil / ausencia de Estado — §3.5 verbatim"}
    tier: FUERTE · falsable_si: "falsador pre-registrado de R5.1 en forense/hitoD-preregistro-v2_0.md (cita la ficha, no la reescribas)"
    fuente, ola_calibracion, ic95, n, ponderador, universo, serie_olas, sha256_payload, payload_manifiesto_id: copia verbatim de la propuesta.
· dinero.planeacion.formal_estable (R1.2, modelo §3.1 l.500)
    situacion: PENDIENTE-DE-MESA · si.disparadores: {} · disparadores_estado: "la condicional de §3.1 (segsoc=1 ∧ contrato ∧ pres_8) no es construible en ENFIH 2019 — barrido 16 tablas / 664 columnas, 0 hits de formalidad laboral, control positivo AFORE 2 hits (#447); tasa base incondicional sobre hogares"
    entonces: tiene_afore 0.538502 / no_tiene_afore 0.461498, clase MEDIDO·p(tasa base ponderada)
    porque: {generador: NO-DECLARADO-EN-§3.1, mecanismo: "el ingreso estable baja el costo esperado de comprometerse a un instrumento de horizonte largo: cae la probabilidad de incumplir y perder lo aportado — §3.1 verbatim (D-01)"}
    tier: FUERTE · falsable_si: "R1.2 en hitoD-preregistro-v2_0.md; §3.1 declara que si sale A la regla se PARTE: sobrevive 'la estabilidad permite' como capacidad, cae 'produce' — cita, no reescribas"
    fuente, ola_calibracion, ic95, n, ponderador, universo, robustez, descriptivo_no_sellado, sha256_payload, payload_manifiesto_id: copia verbatim de la propuesta.
  Si algún campo de arriba no existe en el esquema que valida tests/check.py, PARO de la pieza con el nombre del campo — no se adapta el esquema ni se omite el campo en silencio.
- D5-b: FP-222 (revisión de falsadores D-10..D-13) se ADELANTA al 2026-09-08. Cláusula verbatim de mesa: «si ya dio frutos se mantiene» — la revisión evalúa cada pieza por su fruto medido y conserva la que lo tenga.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — contestada por dirección contra 8598a72 ═══
(1) ESTRUCTURA: Dominio 4 (INFRAESTRUCTURA D4, propuesta → motor); Dominio 9 (tablero). Precedente de carga: ACTO MAESTRA32-E20-P0 (descongelamiento acotado a las ids selladas + smoke `emitir_binaria == p`).
(2) CONTENIDO: `grep -c "^  - id:" milpa/tramite.yaml` → 8 reglas del motor; las dos ids de arriba en tramite.yaml → NO-ENCONTRADO (buscado 1/sep, universo milpa/tramite.yaml). En la propuesta: EXISTE-SATISFACE, ambas con `tier: PENDIENTE-DE-MESA` y `situacion: PENDIENTE-DE-MESA` (l. de `grep -n "^  - id: familia.seguro\|^  - id: dinero.planeacion" milpa/tramite-ola5-propuesta-v0.yaml`). Fila MARCO-M-v1_2 en tablero: `grep -c "MARCO-M-v1_2" forense/firmas-pendientes.tsv` → pega la salida; si ya existe, no la dupliques.
(3) COBERTURA RETROACTIVA: no aplica — todo lo que se toca nació después de las tablas gobernantes.

PIEZAS
P1 · Carga al motor las dos reglas con el bloque CARGA de arriba, campo por campo, sin reinterpretar; descongelamiento acotado a esas ids; smoke `emitir_binaria == p` por regla; entrada de la propuesta marcada SELLADA con el PR (no se borra). Devueltas → cabecera DEVUELTA-POR-MESA con razón verbatim.
P2 · Tablero: recibo de #447 (FP-224 si L1 no lo tomó — deriva); abre fila MARCO-M-v1_2 con `vence: 2026-09-05` (gatea: merge de este acto); enmienda `vence` de FP-222 a 2026-09-08 con la cláusula verbatim de D5-b en la fila; abre fila para ACTO MAESTRA34-E1 · REVISION-FALSADORES (dirección, 8/sep) si no existe.
P3 · Nota: qué quedó cargado, qué devuelto, y que MAESTRA34-L1 traerá la sustitución de mordida para un sello posterior (MAESTRA34-N1-bis, mismo formato).

PERÍMETRO Y CONCURRENCIA: milpa/tramite.yaml · milpa/tramite-ola5-propuesta-v0.yaml (solo estado SELLADA/DEVUELTA) · forense/firmas-pendientes.tsv · forense/notas/ · A.3 · cascada. En paralelo: MAESTRA34-L1 (caja: propuesta valores, codificacion-R, tools/). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar (FP máx hoy 223; ADR candidato 274, renumera si L1 fusiona antes).
CONTADOR: reglas del motor 8 → N, declarado.
LO QUE NO HACE: no mide; no edita valores medidos; no toca el marco ni corridas; no abre Ola 6.
SUCESOR: MAESTRA34-N2 (compuerta = merge de este acto).

## CONSUMIDO

`ACTO MAESTRA34-N1 · SELLA-REGLAS-ACTIVOS-2`, 2/sep/2026, NUBE `cloud_default`, **`PR #449`**
(https://github.com/Josanoforo/Modelado-Mexicano/pull/449), rama
`claude/maestra34-n1-launch-z95iaw`. `ADR-274` (candidato, sin colisión conocida
al fusionar). Carga verbatim las dos reglas D1-a a `milpa/tramite.yaml` (8 → 10
reglas); `FP-224`/`FP-225`/`FP-226` abiertas, `FP-222` enmendada por D5-b.
Detalle: `forense/notas/2026-09-02-maestra34-n1-sella-reglas-activos-2-cierre.md`.
