# Nota de cierre · ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1

28/sep/2026 · CAJA · rama `acto/gen2-pisos-dominios-y-reglas-1` · 0-bis `7cd0f8e2` · ADR `ADR-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-01`.
Contadores: `reglas_con_cifra` +4 (SIN-CIFRA-GEN2 145 → 141 en `canon/reglas-contrastadas-v1_1.tsv`); `mapa11_dominios_medidos` no se mueve en este PR (lo mueve CIERRE-SEMANAL-3 al llevar los pisos al catálogo): 4 dominios con piso propuesto → 17 + 4 = 21 si mesa los adopta.

## 1 · Qué se midió (todo RETROSPECTIVA; no adopta; adopción por merge de mesa)

| pieza | CALC sellado | dominio / regla y dictamen |
|---|---|---|
| ENCUCI 2020 | `CALC-PDR1-ENCUCI2020-0002` | AUTORIDAD: AUTOR-001/002/031 MATIZA · 003/010/030 CONFIRMA · RG-67c84a2224 MATIZA (conjunta derecho×secreto 0.382 [0.365, 0.399])|
| ENSU 2024 T1 | `CALC-PDR1-ENSU2024-0001` | SANCION_SOCIAL: SANC-007 CONFIRMA (0.474 [0.465, 0.483])|
| ENUT 2024 | `CALC-PDR1-ENUT2024-0001` | TIEMPO: TIME-002/020, VEJEZ-009 MATIZA · RURAL_INDIGENA: VEJEZ-032(a) MATIZA, RURAL-002 CONFIRMA · RG-3920de961d CONFIRMA (rural−urbano +5.6 pp [4.8, 6.5])|
| ENADID 2023 | `CALC-PDR1-ENADID2023-0001` | RURAL_INDIGENA: TEC-010 MATIZA (brecha +5.2 pp; 19 % / 24.2 % del report no reproducen)|
| ENVIPE 2025 | `CALC-PDR1-ENVIPE2025-0001` | RG-b91375cbd5 CONFIRMA en su mitad observable (+5.1 pp [3.3, 6.7]); mitad «crisis» NO-CONSTRUIBLE|
| ENIGH 2022 | `CALC-PDR1-ENIGH2022-0001` | RG-cc1c9ab8f1 CONFIRMA en conducta (privada V–VIII − I–IV urbano +7.3 pp [6.3, 8.2]); motivo no observable; gradiente sigue hasta D10|
| INE (cita E.5) | `CALC-INE-PISOS-SICEE-0002` | RG-7c6dd83a03 INCOMPARABLE (banda fijada tras ver el dato; degradada por el hilo principal) · RG-b723d6e18b NO-CONSTRUIBLE (cómputo judicial 2025 no está en el corpus; 7 198 ids examinados)|

Tabla de apertura (P1): `forense/analisis/pisos-dominios-1/tabla-apertura-v1_0.tsv` (`tabla_apertura.py`). Fragmentos por pieza y ensamblado: `ensambla_pdr1.py` → `canon/reglas-contrastadas-v1_1.tsv` (v1.0 intacta; filas no dictaminadas byte a byte) y `conteos-v1_0.json`. Cada `resultado_id` citado existe en el `spec.yaml` de su CALC y cada CALC tiene `sello.json` (el ensamblador lo exige).

## 2 · Lo que no cerró (detalle en `## NO-CORRIDO / RESERVAS` del encargo y en `forense/no-corrido.tsv`)

- **Reserva E.6 rota (PARO a, D-19), por categoría:** `corpus_loader.motivo_reserva` no codifica «ola más reciente de un programa con historia nace RESERVADA» (MEMORIA-OPERATIVA §1) y la primera versión de la tabla de apertura se apoyó sólo en él. Dos piezas abrieron olas declaradas RESERVADAS en specs previas: Latinobarómetro 2024 (sellado y PR #1292, **cerrado sin fusionar**) y Censo 2020 ITER (la corrida `-0001` leyó el payload; el conducto la rechazó sin escribir ni imprimir valores). Mesa decidió seguir con la opción 1 (retirar y continuar). La tabla de apertura corregida lista `RESERVA_E6` con su cita; EDER 2025 no se abrió.
- **Ejecuciones descartadas por el conducto** (§6 Commits; procedimiento y semilla intactos): `CALC-PDR1-ENCUCI2020-0001` (VALOR-LARGO > 1024 bytes; sucesor `-0002` sellado) y `CALC-PDR1-CPV2020ITER-0001` (idem; sucesor `-0002` congelado, sin correr por la reserva).
- DUELO (3 afirmaciones documentales ONU), EMOCIONES_MORALES, INTERACCION, GENETICA, GENOMICA: sin afirmaciones medibles en corpus o fuera por diseño; HUMOR y JUVENTUD sólo tenían olas reservadas.
- 80 de las 88 reglas con instrumento nombrado son prescriptivas/metodológicas (NO-CONSTRUIBLE por texto en la v1.0): siguen SIN-CIFRA, ningún piso las confirma ni las rompe.

## 3 · Hallazgos (una línea cada uno en `forense/hallazgos.md`)

- `corrida0 run` rechaza RESULT texto > 1024 bytes (VALOR-LARGO); `_valida_outputs` no lo ve: la prueba sintética debe asertarlo.
- `tools/ya_medido.py` dio NUNCA-MEDIDA en 5 casos con RESULT sellado equivalente (ENSU C09 2024T1, INE SICEE, LB 2023): busca por rótulo, no por reactivo.
- Las cifras de report para TIME-002/VEJEZ-009 (ENUT) y TEC-010 (ENADID) no reproducen con la construcción declarada: cotejar antes de citarlas.

## 4 · Módulo de auditoría (v2.16)

Contadores movidos: `reglas_con_cifra` +4; `mapa11_dominios_medidos` 0 en este PR (propuestos 4). Todo es RETROSPECTIVA (olas vistas); ninguna frase mezcla PROSPECTIVA. Unidades: persona (ENCUCI, ENSU, ENUT, ENADID, ENVIPE — hogar reportado por la persona en Y1), hogar (ENIGH), lista nominal (INE); ninguna se promedia con otra. Segmentación publicada por sexo, edad y tamaño de localidad/estrato en cada CALC; la ENVIPE usa estrato del área, no clase del individuo. ¿Incentivo o psicología? Los CONFIRMA de RG-3920 (trabajo comunitario rural) y RG-cc1c (colegiatura privada) confirman conducta, no el motivo (obligación normada, «miedo a caer»): leídos simplistas convertirían una diferencia de oferta y estructura en cultura. ¿Clase media urbana? RG-cc1c muestra que el gradiente de escuela privada crece hasta el decil X: no es rasgo específico de la clase media.
