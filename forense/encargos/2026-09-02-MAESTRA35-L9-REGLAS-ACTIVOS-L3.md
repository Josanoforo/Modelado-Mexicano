# ENCARGO · ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3

- **SHA de redacción** — `9cbd8d8` (merge PR #485).
- **Entorno asignado** — UBUNTU con corpus, sesión nueva, worktree propio. **NO** en NUBE.
- **Estado** — CONSUMIDO (ver sección al pie)
- **Redacción** — dirección (Fable), 2/sep/2026, contra `instrucciones-proyecto-v2_12.md`.

---

## Texto verbatim del encargo, tal como se lanzó

ENCARGO · ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3 — invoca /acto SHA de redacción: 9cbd8d8 (merge PR #485). Redacta dirección (Fable), 2/sep/2026, contra v2.12. Estado: LISTO PARA LANZAR — en paralelo con L4, L7, L8. COMPUERTA: ninguna. ENTORNO ASIGNADO: UBUNTU con corpus, sesión nueva, worktree propio. NO en NUBE. Tercera parte de la firma de entorno: ls data/raw/ | head -1. MODELO SUGERIDO: Opus.

CARRILES: L7 (propuesta: civico.denuncia.*, familia.*, dinero.ahorro.horizonte_*) · L8 (civico.participacion.*) · L4/L5-sucesores (ciegas) — este acto appendea ids distintas al pie de la propuesta (civico.voto.*, civico.clientelismo.*, civico.protesta.*, dinero.ahorro.seguro_deposito_*); re-aplica quien fusiona segundo. No descarga.

FIRMAS DE MESA — verbatim. El ejecutor propaga, no decide (SELLA-3).

Mesa, 2/sep/2026: «vamos con todo … dame los siguientes encargos multipasos». Lote «ACTIVOS» = reglas nuevas dentro de los 4 dominios ya activos (aclaración de dirección en MAESTRA33-S2; ADR-265 vigente: no es apertura de Ola 6).
Precedentes de forma: MAESTRA35-L1 (ejes, precedencia CONTRARIA por pares consecutivos), MAESTRA35-L7 (lote L2, en curso: mismas reglas de spec y registro).
A-bis 1–4 y B-bis: asociaciones dentro de una corrida; escala declarada; universo restringido no se reconcilia; pre-registro por regla con lo que significa corroborar.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — contestada por dirección contra 9cbd8d8 ═══ (1) ESTRUCTURA. Modelo §7 (canon/modelo-decision-v4_0.md, ids civico.voto.agencia_con_secreto, civico.voto.clientelar_si_observable, civico.clientelismo.turnout_no_vote_choice, civico.transferencia.entitlement_derecho, civico.protesta.agravio_urbano, dinero.ahorro.seguro_deposito_atenua_aversion). Motor: ninguna cargada (grep -c sobre milpa/tramite.yaml → 0 para las seis). Propuesta: 0. estado-programa-v1_11 §4: civico.voto.clientelar compilaba una cifra de laboratorio (Ascencio-Chang 0.63) degradada a MEDIA — es el caso donde un dato de encuesta sustituye a uno de laboratorio. (2) CONTENIDO. Fuentes en corpus: LAPOP México — microdato 2006 (1008973606mexico_lapop_final_2006_data_set_092906, 518939279…), 2019 (mexico_lapop_americasbarometer_2019_v1_0_w + codebook), 2021 (mex_2021_lapop_americasbarometer_v1_2_w), 2023 (mex_2023_lapop_americasbarometer_v1_0_w, _2) y cuestionario 2023 (lapop_abmex2023_cuestionario_mexico); Latinobarómetro (3 ids); ENCUCI 2020 (encuci2020_bd_dbf + FD); ENIF 2024 (enif_2024_enif_2024_bd_csv, cuestionario 1662). grep -c -i lapop data/inventario-reactivos-v1_2.tsv → 0: LAPOP nunca entró al inventario de reactivos, así que el mapeo de MAESTRA33-E18 no pudo verla — el censo de este acto abre los codebooks directamente. → EXISTE (ítems por verificar). (3) COBERTURA RETROACTIVA. Payloads registrados en agosto; cubierto.

P0 · CENSO A.4 (un commit, antes de medir; denominadores sin cruzar contra el desenlace), por regla con su texto verbatim del modelo: (a) R7.7 + R7.3/R7.6 · civico.clientelismo.turnout_no_vote_choice, civico.voto.agencia_con_secreto, civico.voto.clientelar_si_observable — LAPOP 2019/2021/2023 (y 2006 como contraste): ítems de oferta de dádiva a cambio del voto (familia CLIEN1/CLIEN1N o equivalente del codebook), de participación electoral (VB2/VB10 o equivalente), de percepción de secreto/observación del voto. Estimandos candidatos: P(le ofrecieron dádiva) por ola; P(votó | ofrecieron) vs P(votó | no) — turnout; P(votó por el que dio | ofrecieron) si el ítem existe — vote choice. Lo que la regla predice: la dádiva compra asistencia, no elección (R7.7), y la agencia se conserva con secreto (R7.3) y cede donde el voto es observable (R7.6). (b) R7.4 · civico.protesta.agravio_urbano — LAPOP (PROT3 o equivalente: participó en protesta últimos 12 meses) × urbano/rural (UR o TAMAÑO) × victimización/agravio (VIC1EXT o equivalente) — celdas por ámbito. (c) R7.8 · civico.transferencia.entitlement_derecho — ENCUCI 2020 y LAPOP: ítems sobre programas sociales recibidos y percepción («es un derecho» / «favor del gobierno» / atribución); si ningún instrumento pregunta la percepción, EXISTE-NO-SATISFACE con el conteo (MAESTRA33-E18 ya descartó ENASEM: afiliación, no percepción). (d) R1.5 · dinero.ahorro.seguro_deposito_atenua_aversion — ENIF 2024: razones para NO tener cuenta (desconfianza en bancos / prefiero efectivo) y conocimiento del seguro de depósito (IPAB) si el cuestionario lo trae; celdas por tenencia de cuenta, ingreso, escolaridad. Por regla: ítem, códigos, denominador, ponderador y diseño (LAPOP publica WT/ESTRATOPRI/UPM: verificar en codebook), unidad, y veredicto EXISTE-SATISFACE con mapeo declarado / EXISTE-NO-SATISFACE (qué falta) / NO-ENCONTRADO (dónde, términos). COMMIT-1 del lote: spec por pieza (variables, universo, ponderador, diseño, dicotomizaciones, ejes ≤5 × ≤4 celdas, cobertura) y pre-registro B-bis por regla: signo esperado, CORROBORADA / NO-DISCRIMINA / CONTRARIA con precedencia CONTRARIA (pares consecutivos), y lo que significa corroborar — para (a) sería el primer dato mexicano de encuesta que separe turnout de vote-choice, sustituyendo la cifra de laboratorio 0.63. Frase de sello. Una pieza EXISTE-NO-SATISFACE se cierra en P0 y no tumba el lote. P1–P4 · MEDICIÓN (COMMIT-2 por pieza; COMMIT-3 sólo si una spec estaba mal): proporción ponderada, bootstrap conglomerado 10 000 réplicas seed 42 con el diseño del instrumento; olas múltiples de LAPOP como serie (la más reciente como principal, las otras sensibilidad). Entradas nuevas al pie de la propuesta (civico.clientelismo.turnout_no_vote_choice_lapop2023, civico.voto.agencia_lapop2023, civico.protesta.agravio_urbano_lapop2023, civico.transferencia.entitlement_<fuente>, dinero.ahorro.seguro_deposito_enif2024), situacion/tier PENDIENTE-DE-MESA, clase con escala, celdas con IC, veredicto por eje, estampa A.10, sha256 y payload_manifiesto_id. Sin cargar. P5 · Registro: si LAPOP se abre por primera vez, sus variables con texto entran a data/inventario-reactivos-v1_2.tsv SOLO si el procedimiento de ETIQUETA lo permite sin re-extracción (léelo: forense/notas/2026-08-30-etiqueta-v1_2-spec.md); si no, se deja como hallazgo y NO se edita el inventario. Artefactos data/l9-* con fila en INFRAESTRUCTURA.

PERÍMETRO Y CONCURRENCIA: tools/medidor_clientelismo_lapop.py, tools/medidor_protesta_lapop.py, tools/medidor_entitlement.py, tools/medidor_seguro_deposito_enif24.py (nuevos) · forense/notas/ · milpa/tramite-ola5-propuesta-v0.yaml (append) · data/l9-* + INFRAESTRUCTURA · forense/hallazgos.md · tablero · A.3 · cascada. NO toca milpa/tramite.yaml, procedencia.yaml, corridas-*, medidores existentes, manifiesto, data/raw, inventario de reactivos (salvo P5 con el procedimiento sellado). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR CANDIDATOS: un recibo (sello en RH); primer libre al arrancar (251/301 en 9cbd8d8; L7/L8/L4 pueden fusionar antes).

CONTADOR: reglas del modelo con dato (pendiente sello) +hasta 6 en cuatro piezas · celdas con IC +N · cifra de laboratorio sustituida por dato de encuesta: 1 si (a) satisface. Declara el real.

Lo que este acto NO hace: no carga al motor; no abre Ola 6; no toca cívica electoral (L8) ni denuncia (L7); no descarga; no edita instrucciones.

---

## CONSUMIDO

Ejecutado por `ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3` el 2/sep/2026, entorno
UBUNTU con corpus, worktree `/home/pc0/mm-l9-activos-l3`, rama
`claude/encargo-acto-maestra35-l9`. **`PR #491`**
(https://github.com/Josanoforo/Modelado-Mexicano/pull/491), abierto y **no
fusionado** — el merge es de mesa. Sellado en `canon/gobernanza-v1_15.md`
`ADR-305`.

Commits: `6412d17` (A.3) · `418a22f` (`P0` censo) · `a67e46b` (`COMMIT-1` spec) ·
`7033743` (`COMMIT-2` resultados) · `df96044` (merge de `origin/main = 78304f3`) ·
la cascada de cierre.

Entregado: seis reglas del modelo con dato (`R7.7`, `R7.3`, `R7.6`, `R7.4`,
`R7.8`, `R1.5`), 84 celdas y contrastes con IC95, cinco entradas
`PENDIENTE-DE-MESA` al pie de `milpa/tramite-ola5-propuesta-v0.yaml`, `ADR-305`,
`FP-253`. **`ADR` renumerado de `304` a `305`** al fusionar por segunda vez: `PR #492` (`ACTO MAESTRA35-N8 · SELLA-L7`) fusionó primero y se llevó el `304`. `PR #490` (`MAESTRA35-L4`) sigue abierto reclamando `304`/`FP-253`: si fusiona antes, renumera quien fusione segundo.

Lo que el encargo pedía y **no** se entregó, con su razón: la **serie de
LAPOP** (2021 no trae ninguna de las variables y 2006 no es el mismo
instrumento); la **entrada de LAPOP al inventario de reactivos** (el
procedimiento de ETIQUETA no la permite sin re-extracción — dejado como
hallazgo, que es la rama que el propio encargo prescribe); el eje **«celdas por
tenencia de cuenta»** de la pieza (d), que no es construible porque el desenlace
sólo existe para quien no tiene cuenta; y el contraste de **entorno** de la
pieza (b), que cayó por la guardia de numerador pre-registrada.

Contadores: reglas del modelo con dato **+6** (pendiente sello) · celdas con IC
**+84** · **cifra de laboratorio sustituida por dato de encuesta: 0** — el
encargo lo condicionaba a que (a) satisficiera, y (a) salió `NO-DISCRIMINA`.
