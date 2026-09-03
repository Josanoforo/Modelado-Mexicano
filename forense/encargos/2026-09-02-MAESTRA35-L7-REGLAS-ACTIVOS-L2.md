# ENCARGO · ACTO MAESTRA35-L7 · REGLAS-ACTIVOS-L2

Archivado por A.3 (0-bis) el 2/sep/2026. Texto verbatim del encargo tal como
lo entregó dirección. No se edita en ningún punto salvo la sección
`## CONSUMIDO` que la cascada de cierre añade al pie.

Cabecera obligatoria (`forense/encargos/convencion.md`):

- **SHA de redacción** — `19770f2` (merge PR #481), declarado por dirección.
- **Entorno asignado** — UBUNTU con corpus, sesión nueva, worktree propio. **NO** en NUBE.
- **Estado** — `VIVO`.
- **Bloque VERIFICACIÓN DE EXISTENCIA (A.8)** — contestado por dirección dentro del texto, más abajo.

---

ENCARGO · ACTO MAESTRA35-L7 · REGLAS-ACTIVOS-L2 — invoca /acto SHA de redacción: 19770f2 (merge PR #481). Redacta dirección (Fable), 2/sep/2026, contra v2.12. Estado: LISTO PARA LANZAR — en paralelo con L4 (ciega), A1 (registro), L8 (cívica). COMPUERTA: ninguna. ENTORNO ASIGNADO: UBUNTU con corpus, sesión nueva, worktree propio. NO en NUBE. Tercera parte de la firma de entorno: ls data/raw/ | head -1. MODELO SUGERIDO: Opus (lote medidor, dos commits por pieza).

CARRILES: L4/L5 (sesiones ciegas: corridas-R) · A1 (manifiesto, cola) · L8 (cívica: civico.*, adquisición electoral) · N5/N6/N7 (nube: motor, canon). Este acto appendea al pie de la propuesta (civico.*/familia.*/dinero.*: si L8 también appendea civico.*, re-aplica quien fusiona segundo), escribe medidores nuevos y NO descarga.

FIRMAS DE MESA — verbatim. El ejecutor propaga, no decide (SELLA-3).

Mesa, 2/sep/2026: «vamos con todo, los encargos corriendo … Encargos paralelos». Nombre del lote por la aclaración de dirección en MAESTRA33-S2 (verbatim): «"ACTIVOS" = reglas nuevas dentro de los 4 dominios ya activos (tramite, civico, dinero, familia). No es apertura de Ola 6; MAESTRA33-E14/ADR-265 sigue vigente.» (serie añadida por dirección al citar; el verbatim de S2 trae el rótulo pelado) Precedente: MAESTRA33-E18-P3 (lote L1: remesas ENIGH, AFORE ENFIH), cargado por D1-a.
Regla de señal (v2.3) y A-bis 1–4: tasas base y celdas por ejes son asociaciones dentro de una corrida; escala declarada; universo restringido no se reconcilia contra el marginal.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — contestada por dirección contra 19770f2 ═══ (1) ESTRUCTURA. Modelo canon/modelo-decision-v4_0.md §7 (49 reglas; tabla L213-L300). Motor milpa/tramite.yaml (10 reglas). Acumulador (append al pie). Medidores: precedente wprop_ic_conglomerado (tools/calibracion_mordida_encig_serie.py:81). Artefactos nuevos en data/ → data/INFRAESTRUCTURA-v1_0.md (T27 lo exige; lección de MAESTRA35-L6). (2) CONTENIDO. Las cuatro reglas de abajo NO están en el motor (grep -c "id: civico.denuncia.sin_seguro\|id: familia.union\|id: familia.cuidado\|id: dinero.ahorro.volatilidad" milpa/tramite.yaml → 0) ni en la propuesta (mismo grep sobre tramite-ola5-propuesta-v0.yaml → 0). Mapeo previo (forense/notas/2026-09-01-MAESTRA33-E18-P2-mapeo-tabla.md) las dejó EXISTE-NO-SATISFACE por el inventario de reactivos sin texto — no por el instrumento: ENVIPE «la fuente natural» sale con texto_reactivo vacío; ENUT y EDER/ENADID no se abrieron. Fuentes en corpus (grep -n '^- id:' data/manifiesto.yaml): envipe2025_csv (306) · enut2019_bd_csv (2989) + FD (3014) · enut2024_bd_csv (3070) · eder_2017_eder2017_bases_csv (4324) · ENADID: 4 ids (grep -c -i '^- id: .*enadid' → 4; el censo fija cuál) · enif_2024_enif_2024_bd_csv (5427). → EXISTE (ítem por verificar) ×4. (3) COBERTURA RETROACTIVA. Mapeo del 1/sep; instrumentos registrados antes; cubierto.

P0 · CENSO A.4 (un commit, antes de medir; denominadores sin cruzar contra el desenlace), por regla y con el texto de la regla verbatim del modelo: (a) R7.2 · civico.denuncia.sin_seguro/con_seguro — «Delito sin cobertura de seguro → no denuncia (cifra negra)» — ENVIPE 2025, módulo de victimización: ¿hay ítem de tenencia de seguro para el delito (robo de vehículo / vivienda)? ¿denuncia (BP1_20) y razón? Denominador por tipo de delito. Veredicto A.4. (b) R5.3 · familia.union.baja_garantia_institucional — «Baja garantía institucional del matrimonio → unión libre» — EDER 2017 (historia de uniones: tipo de primera unión por cohorte) y/o ENADID (situación conyugal, sit_conyugal): tasa de unión libre por cohorte de nacimiento y por escolaridad/ámbito. El disparador «baja garantía institucional» NO está medido en el instrumento: se declara y se mide la tasa base con ejes, no la condicional. (c) R5.2 · familia.cuidado.recae_mujeres_40mas — «Cuidado (mayores/niños/enfermos) → recae en mujeres 40+» — ENUT 2019 (y 2024 si el FD lo permite): horas semanales de cuidado por sexo × edad; proporción del total de horas de cuidado del hogar que hacen mujeres de 40+; unidad persona, ponderador y diseño del FD. (d) R1.1 · dinero.ahorro.volatilidad_horizonte_corto — «Volatilidad/informalidad → horizonte corto, ahorro informal» — ENIF 2024: P4_10 (meses que cubriría sin ingreso: horizonte) × sin seguridad social por trabajo (eje ya usado por MAESTRA35-L1, cobertura 68.97 %, universo restringido A-bis 4) × ahorro informal (L1 P2). Precedente: MAESTRA35-L1 midió formalidad sobre ahorra_solo_informal; aquí la conducta es horizonte corto. COMMIT-1 del lote: spec congelada por pieza (variables, universo, ponderador, diseño, dicotomización, escala, ejes ≤5 con ≤4 celdas, cobertura por eje) y pre-registro B-bis por regla con signo esperado y veredicto CORROBORADA / NO-DISCRIMINA / CONTRARIA (precedencia CONTRARIA, pares consecutivos en el orden declarado — regla que L1 operacionalizó). Frase de sello. Una pieza EXISTE-NO-SATISFACE en P0 se cierra ahí con su veredicto y no tumba el lote. P1–P4 · MEDICIÓN por pieza (COMMIT-2 resultados; COMMIT-3 sólo si una spec estaba mal): proporción ponderada con bootstrap conglomerado 10 000 réplicas seed 42 donde el FD traiga estrato/UPM; donde no, EE con la aproximación declarada y la reserva escrita (precedente FP-249). Entradas nuevas al pie de la propuesta, una por regla: civico.denuncia.con_seguro_envipe2025, familia.union.libre_eder2017 (o _enadid), familia.cuidado.mujeres40_enut2019, dinero.ahorro.horizonte_corto_enif2024, con situacion: PENDIENTE-DE-MESA, tier: PENDIENTE-DE-MESA, clase con escala, celdas con IC, veredicto por eje, estampa A.10, sha256 y payload_manifiesto_id. Sin cargar al motor (sello de mesa en RH).

PERÍMETRO Y CONCURRENCIA: tools/medidor_denuncia_seguro_envipe25.py, tools/medidor_union_libre.py, tools/medidor_cuidado_enut.py, tools/medidor_horizonte_enif24.py (nuevos) · forense/notas/ · milpa/tramite-ola5-propuesta-v0.yaml (append al pie) · data/l7-*.json|tsv si produces artefactos + su fila en data/INFRAESTRUCTURA-v1_0.md · forense/hallazgos.md · forense/firmas-pendientes.tsv · A.3 · cascada. NO toca milpa/tramite.yaml, procedencia.yaml, corridas-*, medidores existentes, manifiesto, data/raw. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR CANDIDATOS: un recibo del lote (sello de las cuatro entradas, en RH); primer FP/ADR libres al arrancar (249/298 en 19770f2; #480 y otros pueden fusionar antes).

CONTADOR: reglas del modelo con dato (fuera del motor, pendiente sello): +hasta 4 · celdas con IC +N · reglas del motor: sin cambio. Declara el real.

Lo que este acto NO hace: no carga al motor; no abre Ola 6 (ADR-265); no toca cívica electoral (L8); no descarga; no edita instrucciones.

Sucesores declarados, no lanzados: acto NUBE de propagación tras firma de mesa (patrón MAESTRA35-N4).

## CONSUMIDO

Ejecutado por `PR #486` (`ACTO MAESTRA35-L7 · REGLAS-ACTIVOS-L2`), 2/sep/2026,
worktree `/home/pc0/mm-maestra35-l7`, `ADR-303` (renumerado de `302` al
fusionar por segunda vez — `PR #487`, `ACTO MAESTRA35-L8`, se llevó `302`
primero), `FP-252` (`ABIERTA`). Las
cuatro piezas `EXISTE-SATISFACE` en el censo P0 y `CORROBORADA` contra el
signo pre-registrado en `COMMIT-1`. Cuatro entradas nuevas al pie de
`milpa/tramite-ola5-propuesta-v0.yaml`, todas `PENDIENTE-DE-MESA`, ninguna
cargada al motor. No abrió Ola 6, no tocó cívica electoral, no descargó
nada. Detalle completo: `forense/notas/2026-09-02-MAESTRA35-L7-{P0-censo,
spec,resultados}.md`.
