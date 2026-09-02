ENCARGO · ACTO MAESTRA34-L1 · MORDIDA-SERIE — invoca /acto
SHA de redacción: 8598a72 (merge PR #447). Redacta dirección (Fable), 1/sep/2026, contra instrucciones v2.12. Estado: LISTO PARA LANZAR — las cuatro piezas firmadas (D2-b, D3-a).

ENTORNO ASIGNADO: UBUNTU (caja con corpus). NO se lanza en NUBE: abre microdato ENCIG (A.2). MODELO SUGERIDO: Opus (lote medidor de dos commits, D-13).
CARRILES: ningún otro acto de caja hasta el merge de éste. Nube puede correr MAESTRA34-N1 en paralelo (perímetros disjuntos salvo cascada; renumera quien fusiona segundo).

FIRMAS DE MESA — verbatim, 1/sep/2026 (mensaje único de mesa: «D1 - a,  D2-b,  D3-a, D4-a, D5-b si ya dio frutos se mantiene.»). La firma formal es el merge del PR [COLA] que archiva este encargo; el ejecutor propaga, no decide (SELLA-3).
- Hallazgo ADR-270 (1/sep): prior ASIGNADO p=0.62 de `paga_mordida` contra R = 0.045–0.077 (ENCIG 2013/2017/2021).
- D2-b: alcance completo — calibración ENCIG 2025 + serie 2011/2015/2019/2023 como referencia histórica no cargada + censo de `tramite.mordida.con_registro`. Se ejecutan P1, P2 y P3.
- D3-a: la regla cívica se persigue AHORA como pieza 4 (diseño de L1-spec.md:502-508, cómputos INE concurrentes vs no concurrentes), con la salvaguarda escrita: si el portal no responde, la pieza reporta NO-OBTENIDO-POR-ESTE-AGENTE con receta y se detiene sin afectar a P1–P3.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — contestada por dirección contra 8598a72 ═══
(1) ESTRUCTURA: Dominio 4 de data/INFRAESTRUCTURA-v1_0.md (estimación: spec → expediente → producción). Tabla de dicotomización gobernante: forense/prereg-duelo-v2/codificacion-R-v1_0.tsv. Destino de la p: milpa/tramite-ola5-propuesta-v0.yaml (precedente ADR-273). Motor milpa/tramite.yaml NO se toca.
(2) CONTENIDO:
  - `grep -n paga_mordida milpa/tramite.yaml` → l.45 `p: 0.62, clase: ASIGNADO` (id tramite.mordida.discrecional) · l.59 `paga_mordida_encuci2020 p=0.125822 MEDIDO` (regla distinta, disparador contacto_declarado; NO se toca) · l.91 `p: 0.12 ASIGNADO` (tramite.mordida.con_registro).
  - `grep -c "encig23\|encig25\|encig2019\|encig2015\|encig_2011" codificacion-R-v1_0.tsv` → 0. Filas P8_3 para 2013/2017/2021: EXISTE-SATISFACE (TRA-M-03/05/07). Para 2011/2015/2019/2023/2025: NO-ENCONTRADO (buscado en codificacion-R y tools/, términos encig25/P8_3, 1/sep).
  - Payloads: manifiesto ids encig_2011_*, encig2015_csv, encig2019_csv, encig23_base_datos_csv, encig25_base_datos_csv → EXISTE-SATISFACE (5 olas libres).
  - Receta reutilizable: forense/prereg-duelo-v2/corridas-R/TRA-M-07.json (variable P8_3_1, FAC_P18, EST_DIS/UPM_DIS, universo sección VIII). EXISTE-SATISFACE.
  - Cómputos electorales locales concurrentes/no concurrentes (P4): `grep -il "computo\|INE\|OPLE" data/manifiesto.yaml` → verifica tú y pega la salida; dirección lo clasifica NO-ENCONTRADO en manifiesto al 1/sep.
(3) COBERTURA RETROACTIVA: codificacion-R nació 1/sep (C3); las olas libres nunca pasaron por ella → su ausencia no prueba nada; se añaden filas de calibración (solo eso).

SPEC CONGELABLE POR PIEZA — CIEGO a corridas-M/L y scoreboard (declara que el R de TRA-M-03/05/07 ya es público).
P1 · CALIBRACIÓN 2025. COMMIT-1 congela: payload encig25_base_datos_csv; tabla sección VIII; variable = homóloga de P8_3_1 verificada en la estructura de base 2025 (si el nombre cambió, se escribe el nuevo con cita de página del FD y sigue); codificación idéntica a TRA-M-07 (1=Sí, 2=No, 9 fuera); ponderador FAC_P18 o su homólogo declarado; diseño EST_DIS/UPM_DIS; escala [0,1]; IC95 seed 42 por conglomerado. Frase de sello: «el primer resultado que produzca este procedimiento es el que se reporta». COMMIT-2: p, IC95, n_efectivo; entrada MEDIDO·p en la propuesta que SUSTITUYE al 0.62 con `tier: PENDIENTE-DE-MESA`; la vieja se conserva en la propuesta con cabecera `REFUTADA-POR-R` citando ADR-270 y las tres R. Fila nueva en codificacion-R (calibración, no celda del marco).
P2 · SERIE 2011/2015/2019/2023. Mismo procedimiento que P1, un COMMIT-1 conjunto congelando las cuatro variables homólogas (ENCIG 2011 es DBF: declara lector). COMMIT-2: `serie_olas` en la misma entrada, formato del precedente familia.seguro (p+IC por ola, NO promediadas). Con 2013/2017/2021 públicas, la serie queda de 8 olas: escríbelo en la nota como θ informativa, sin cargar nada.
P3 · CENSO `tramite.mordida.con_registro`. COMMIT-1: censo del cuestionario/FD ENCIG 2025 (y 2021 si hace falta) buscando ítem que distinga trámite con registro/testigo/digital vs presencial-discrecional. Veredicto A.4 con archivos examinados (A.13). Si EXISTE-SATISFACE: COMMIT-2 mide p condicionada, misma spec de P1, entrada nueva PENDIENTE-DE-MESA. Si EXISTE-NO-SATISFACE / NO-ENCONTRADO: la pieza cierra ahí, con lo que le falta nombrado (precedente L1-spec regla 3).
P4 · CÍVICA CONCURRENTE (firmada D3-a). Diseño de L1-spec.md:502-508. COMMIT-1: fuente = cómputos distritales locales INE/OPLE, año(s) con elección local concurrente y no concurrente en el mismo estado; unidad = municipio/distrito; desenlace = participación; contraste = concurrente vs no; universo y años congelados antes de bajar nada. Adquisición vía /adquiere (≥4 rutas antes de NO-OBTENIDO, receta de navegador ≤1 min). COMMIT-2: diferencia de participación + IC; entrada PENDIENTE-DE-MESA. Si el portal no responde: NO-OBTENIDO-POR-ESTE-AGENTE EN N INTENTOS, receta, y la pieza cierra sin tumbar el lote.

PERÍMETRO Y CONCURRENCIA: milpa/tramite-ola5-propuesta-v0.yaml · codificacion-R-v1_0.tsv (solo filas de calibración) · tools/ (script nuevo, reutiliza tasas_base_ola6_activos.py como patrón) · data/manifiesto.yaml solo si P4 registra · forense/notas/ · tablero (recibo) · A.3 · cascada. En paralelo: MAESTRA34-N1 (milpa/tramite.yaml, propuesta solo campo estado/SELLADA, tablero). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: FP máx hoy 223 → rango FP-224…FP-227 (deriva de nuevo al arrancar). ADR candidato por comando de la casa contra 8598a72: 274 (renumera si N1 fusiona antes).
CONTADOR: prior→MEDIDO +1 (P1) · θ informativas +4 (P2) · reglas medidas +1 si P3 satisface · +1 si P4 corre. Declara el real al cierre.
LO QUE NO HACE: no carga al motor; no toca milpa/tramite.yaml; no re-emite M de v1_1; no toca corridas-R de TRA-M; no promedia olas.
SUCESORES: MAESTRA34-N1 (o su relanzamiento) sella lo que mesa firme de aquí; MAESTRA34-N2 hereda la regla nueva como celda v1_2.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA34-L1 · MORDIDA-SERIE` (`ADR-276` — renumerado
dos veces: `274`→`275` cuando `PR #449`/`MAESTRA34-N1` fusionó primero,
`275`→`276` cuando `PR #450`/`MAESTRA34-N2` fusionó también antes que
este PR; regla de la casa, renumera quien fusiona segundo), entorno
UBUNTU). P1 (calibración ENCIG 2025, p=8.5118%) y P2 (serie histórica
8 olas, 4.45%–8.51%) medidos completos contra microdato real. P3
(censo `tramite.mordida.con_registro`): `EXISTE-SATISFACE`, medido
(presencial 11.60% vs digital/registrado 2.74%, IC95 sin traslape). P4
(cívica concurrente, D3-a): `NO-OBTENIDO-POR-ESTE-AGENTE (5 intentos)`
— cierra sin afectar P1-P3, receta de navegador dejada. FP/ADR
candidatos del encargo (`FP-224…227`) quedaron obsoletos a mitad de
acto: `PR #449`/`MAESTRA34-N1` ya había tomado `FP-224/225/226` al
fusionar antes; este acto no abrió fila nueva de tablero. ADR candidato
`274` renumerado dos veces: `PR #449`/`MAESTRA34-N1` lo tomó primero
(→`275`), y `PR #450`/`MAESTRA34-N2` fusionó también antes que este PR
y tomó el `275` (→`276` final) — regla de la casa, renumera quien
fusiona segundo, aplicada dos veces. Detalle completo:
`forense/notas/2026-09-01-MAESTRA34-L1-MORDIDA-SERIE-cierre.md`. PR:
https://github.com/Josanoforo/Modelado-Mexicano/pull/451
