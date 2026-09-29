# Nota de cierre · ACTO GEN2-MEDICION-CARRILES-2

28/sep/2026 · CAJA · rama del acto `acto/gen2-medicion-carriles-2` (0-bis `8fdfacd9`) con tres hijas por instrumento, apiladas: ENIF 2024 (PR #1311, ADR `…-8fdf-01`), ENSANUT 2024 (PR #1314, `…-8fdf-02`), ENVIPE 2025 + cierre (este PR, `…-8fdf-03`). Mesa en sesión: una hija = un PR a main, a lo más dos abiertos (luego levantado: «hay espacios libres, termina el encargo»); catálogo derivado regenerado por comando (autorizado).

Contadores movidos: `reglas_con_cifra` +1 (`canon/reglas-contrastadas-v1_2.tsv`: SIN-CIFRA-GEN2 141 → 140); afirmaciones MEDIBLE-EN-CORPUS con dictamen propio +32; carriles ROJO 0 (ver §3).

## 1 · P4 · conteos por comando (`python3 forense/analisis/medicion-carriles-2/tabla_apertura_mc2.py`, `conteos-apertura.json`, `conteos-reglas.json`)

| objeto | conteo |
|---|---|
| afirmaciones MEDIBLE-EN-CORPUS (mapa v1.1) | 235 |
| · medidas por este acto (dictamen propio) | 32 (ENIF 18, ENSANUT 4 + 1 NO-CONSTRUIBLE, ENVIPE 8 + 2 NO-CONSTRUIBLE) |
| · citadas E.5 (PDR1 u otro CALC sellado) | 16 |
| · con juicio C3 sin RESULT propio verificado | 75 |
| · DIFERIDO-A R06 (ENIF 2024 módulo 7) | 3 |
| · NO-CONSTRUIBLE por texto (fuera de fragmentos) | 1 |
| · PENDIENTE (por instrumento, ver tabla) | 108 |
| reglas SIN-CIFRA-GEN2 v1.1 → v1.2 | 141 → 140 (RG-41d71be87f MATIZA) |
| · NO-CONSTRUIBLE v1.1 sin motivo nuevo | 137 · NO-CONSTRUIBLE confirmado 2 · INCOMPARABLE 1 |
| CALC sellados (verify REPRODUCE) | 3: `CALC-MC2-ENIF2024-0001`, `CALC-MC2-ENSANUT2024-0001`, `CALC-MC2-ENVIPE2025-0001` |
| cruces de segmentación nuevos por eje | ENIF: 16 indicadores × {sexo 2, edad 4, escolaridad 4, localidad 2, región 6, formalidad 2}; ENSANUT: acceso/no-grave × {estrato 5, sexo 2, edad 3}, suspensión × {pago 2, estrato 2, sexo 2}; ENVIPE: delito × {sexo 2, dominio 3}, percepción 2024 × {sexo 2, dominio 3, edad 4}, AP4_3_3 2025 × {sexo, dominio, edad, Sinaloa} |
| payloads nuevos | 0 (P3 no corrido; §4) |
| olas reservadas abiertas | 0 (ENIF 2024 m7, ENSANUT 2025, ENVIPE 2026 no son input; guardia m7 con prueba) |

## 2 · Qué se midió (todo RETROSPECTIVA; no adopta)

- **ENIF 2024** — 5 CONFIRMA · 10 MATIZA · 3 ROMPE. Los ROMPE: «24 % tiene cuenta» (65.5 %), tandas ~30 % (18.6 %), 49.5 % sin crédito formal (64.5 %). Formalidad separa afore/seguro/vivienda (+55, +31, +11 pp).
- **ENSANUT 2024** — RG-41d71be87f MATIZA (rural busca atención −6.1 pp vs metro; barreras de acceso entre no buscadores +8.0 pp con IC que toca 0; «no era grave» 66 %). SALUD-032, SALMEN-032, JUV-009 MATIZA.
- **ENVIPE 2025** — cifra negra 93.6 % [93.2, 93.9], denuncia, extorsión telefónica 85.6 %, inseguridad primera preocupación 2024 (60.8 %), cajero el espacio más temido (72.4 %), Sinaloa +25.8 pp 2024→2025: 7 CONFIRMA (3 PARCIAL), 1 MATIZA, 2 NO-CONSTRUIBLE.

## 3 · Premisa del tablero (SUPUESTO del encargo) y propuesta

`tools/tablero_carriles.py:53`: ROJO = ningún dominio NÚCLEO con cifra **adoptada** del catálogo v1.3. Un acto que mide y no adopta no puede sacar un carril de rojo; el criterio «menos rojos en el commit final» es inalcanzable por construcción antes del merge y del cierre siguiente. Los 7 ROJO (RURAL_INDIGENA, DUELO, TIEMPO, HUMOR, JUVENTUD, EMOCIONES_MORALES, AUTORIDAD) tampoco tienen instrumento nuevo en este acto (sus pisos PDR1 esperan adopción). **Propuesta** (PROPUESTO-POR-EJECUTOR): añadir un estado intermedio NARANJA = «núcleo con RESULT GEN2 sellado sin adoptar» (misma fuente que la columna «CALC GEN2 sin adoptar» del catálogo), para que el tablero distinga «sin medir» de «medido, esperando mesa».

## 4 · No corrido (detalle en `## NO-CORRIDO / RESERVAS` del encargo y en `forense/no-corrido.tsv`)

P3 adquisición y las hijas ENOE, ENIGH, ENUT, ENDUTIH, ENCUCI, ENADID y resto: DIFERIDO-A GEN2-MEDICION-CARRILES-3 (sucesor que nombra el encargo §10). Hoja RH: `forense/analisis/medicion-carriles-2/hoja-rh.md`.

## 5 · Hallazgos (una línea cada uno en `forense/hallazgos.md`)

- Los generadores de catálogo v1.1–v1.3 recuentan todo CALC sellado: un CALC nuevo puede mover la columna derivada y romper `test_catalogo_v1_*` si no se regenera.
- Control ENVIPE 2024 Sinaloa AP4_3_3: MC2 0.554961 vs sellado 0.554711 (Δ 2.5e-4): la construcción sellada difiere en algo menor (denominador/códigos); no cambia dictamen.
- El mapa v1.1 y `ya_medido.py` no ven los CALC sellados después de su fecha (Latinobarómetro 2023, ENSANUT 2024): la tabla de apertura debe cruzar contra CALC, no contra el mapa.

## 6 · Módulo de auditoría (v2.16)

Contadores: +1 regla con cifra, +32 afirmaciones. Todo RETROSPECTIVA; ninguna cifra PROSPECTIVA. Unidades: persona (ENIF, ENSANUT, ENVIPE percepción) y delito (ENVIPE módulo), nunca promediadas. Incentivo antes que psicología: afore/seguro siguen a la formalidad (oferta institucional); no buscar atención se explica más por «no era grave» que por acceso, pero el rural busca menos; la suspensión de tratamiento se asocia a pagar (IC toca 0). Sin clase NSE en ENIF (declarado). Firewall genético: sin variables de ascendencia.
