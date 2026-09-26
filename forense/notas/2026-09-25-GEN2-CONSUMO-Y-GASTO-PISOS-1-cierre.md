**Contador: 57 conductas con piso GEN2 por dominio — CONSUMO 48 · DINERO 9** (`python3 tools/dominios/consumo/tabla_pisos.py`, sobre los sellados; antes de este acto CONSUMO tenía 0 según `canon/catalogo-del-mexicano-v1_1.md:135`). No se adopta nada; no se evalúa prospectivamente.

# GEN2-CONSUMO-Y-GASTO-PISOS-1 · cierre

25/sep/2026 · CAJA (`tools/entorno.py --arranque`: `ENTORNO-DERIVADO = CAJA`, corpus `montado=SI archivos_examinados=511`) · Opus 5.5 (arranque y acto entero; el encargo pide Opus) · rama `acto/gen2-consumo-y-gasto-pisos-1` · base `40058c09` = SHA de redacción · 0-bis `2d37b23b` · encargo `forense/encargos/2026-09-25-GEN2-CONSUMO-Y-GASTO-PISOS-1.md` · MODO AUTÓNOMO.

## 1 · Qué se midió

| CALC | olas | conductas | RESULT | verify aislado | commit de sello |
|---|---|---|---|---|---|
| `CALC-ENGASTO-CONSUMO-PISOS-0001` | 2012 (2013 RESERVADA) | 22 | 1 660 | REPRODUCE / IDENTICO, 1 660/1 660, max\|Δ\| = 0 | `f09ab2ea` |
| `CALC-ENIGH-CONSUMO-PISOS-0001` | 2016, 2018, 2020, 2022 (2024 RESERVADA) | 35 | 23 100 | REPRODUCE / IDENTICO, 23 100/23 100, max\|Δ\| = 0 | `55d7def9` |
| `CALC-ENIGH-CONSUMO-PISOS-0002` (sucede a 0001) | ídem | 35 | 23 101 | REPRODUCE / IDENTICO, 23 101/23 101, max\|Δ\| = 0 | `7f0d3801` |

Secuencia: COMMIT-1 `5b2dc18c` (lista cerrada P1, dos specs humanas + `spec.yaml` + medidores + test D-22, **sin microdato**; `corrida0 preflight` VERDE en ambos CALC) → COMMIT-2a ENGASTO → COMMIT-2b ENIGH 0001 → COMMIT-3 `4d61d466` (spec v1.1 + CALC 0002, congelados antes de correr) → COMMIT-4 ENIGH 0002. Tabla conducta × segmento × ola con id de RESULT: `forense/analisis/consumo-gasto/tabla-pisos-consumo-v1_0.tsv` (4 470 filas, derivada por `tools/dominios/consumo/tabla_pisos.py`; ENIGH desde 0002). Asientos E.7: tres filas en `forense/replay-evidencia.tsv`, evidencia `forense/analisis/consumo-gasto/evidencia-replay-consumo-gasto-*.json`.

**IC calibrado de persistencia** (ENIGH, 4 olas): τ² por conducta × eje con la receta común (`persistencia`/`ic_calibrado` de `tools/dominios/salud/pisos_diseno.py`, método `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001` §4) → columnas `-ICC-LO/-HI` sobre el piso 2022, ids `RESULT-ENIGH-CONSUMO-PISOS-<conducta>-<eje>-TAU2`. Es un parámetro reutilizable por conducta × eje. 2020 (pandemia) entra y ensancha τ² donde hubo choque (p. ej. HOG-ALI-FUERA: IC de diseño 2022 [0.440, 0.451], calibrado [0.224, 0.690]).

### 1.1 · Premisas que cayeron y qué se hizo (cláusula de autonomía, puntos 1-2)

- **«ENGASTO 28 payloads» es una canasta, pero son dos olas.** Por identidad (trazado contra `engasto12_fd.pdf`, sha256, número de campos): `engasto2012/` = ola 2012 (HOGAR 161 campos); `engasto2013/` = ola 2013 (173 campos, `recurso_*`, `cubr_gasto`). 24 de los 28 ids `engasto_2012_*` apuntan a archivos de `engasto2013/` con `url_origen` `/2012/`. INTERPRETACIÓN-DECLARADA: E.6 aplica, 2013 queda RESERVADA y no es input (guardia en el medidor); se abre 2012 por los ids que apuntan a `engasto2012/`. Detalle: `forense/analisis/consumo-gasto/lista-cerrada-P1.md` §1.
- **`[SUPUESTO]` «ENGASTO trae factores y diseño por trimestre»:** falso en la forma; el FD trae un factor por hogar para la ola, anualizado. Unidad temporal declarada: la ola.
- **§4 del encargo, `ls data/corrida0 | grep -ic 'ENGASTO\|CONSUMO'` → esperado 0, dio 1**: `ensafi2023-fichas-consumo-v1_0.tsv` (fichas ENSAFI, no un CALC). No cambia nada.
- **ENIGH 2016 y 2018: `gastoshogar` del ZIP integrado truncado.** El sello de 0001 emitió `G-2016-FILAS-GASTO = G-2018-FILAS-GASTO = 1048575`; el miembro tiene 1 048 576 líneas (límite de Excel) y corta en la entidad 19. Además 0001 da HOG-COMPRA-FIADO 2016 y 2018 = 0.0000 exacto, lo que la truncación sola no explica: el archivo integrado difiere también en contenido. 0001 se reporta tal cual (primer resultado) y **sus conductas desde `gastoshogar` en 2016/2018 no son válidas** (PART-EFECTIVO, PART-CANAL-*, HOG-COMPRA-FIADO, -TARJETA-CREDITO, -INTERNET, -INTERNET-SI-CONEXION, y su τ²/ICC). Tercer commit, no corrección hacia atrás: spec v1.1 + `CALC-ENIGH-CONSUMO-PISOS-0002` leen `gastoshogar` 2016/2018 de la descarga por tabla `cc1_inegi_enigh_{2016,2018}__…_gastoshogar_csv` (completa: 4 190 742 y 4 405 251 líneas, termina en entidad 32). **Oro interno declarado antes de correr: COINCIDE** — 18 580 de 18 580 RESULT que no dependen de esos archivos son idénticas entre 0001 y 0002 (`python3 tools/dominios/consumo/oro_0001_0002.py`). Magnitud del error evitado: HOG-COMPRA-INTERNET 2016 0.0077 (0001) vs 0.0114 (0002); τ² de esa conducta 0.887 vs 0.536.

## 2 · Controles externos

Tabulados publicados de ENIGH 2016–2022: `NO-VERIFICABLE-AQUÍ` — el manifiesto tiene 1 id de resultados/tabulados de ENIGH y es el reporte 2024, RESERVADO (`grep -c -E "^- id: .*enigh.*(tab|present|result|comunicado|reporte)" data/manifiesto.yaml` = 1). Control cruzado ENGASTO ↔ ENIGH (orden y dirección): celular 2012 0.739 [0.726, 0.750] → ENIGH 2016 0.836; internet 2012 0.260 [0.247, 0.272] → ENIGH 2016 0.363; compra por internet 2012 0.009 → 2016 0.011. Coherentes en dirección.

## 3 · Bloque C por report

Evidencia de todo lo de abajo: **(a)** microdato primario mexicano, autorreporte de hogares (diario y cuestionarios de gasto). Cada cifra es un RESULT sellado de la tabla; hogar, nunca persona.

### *Psicología del Consumidor Mexicano*

- **CONS-016 (90 % prefiere tienda física) / CONS-015 (e-commerce 17.7 % del retail)** — **MATIZA.** Los hogares que registran alguna compra por internet en la semana/periodo de referencia son 0.069 [0.066, 0.072] en 2022 (0.011 en 2016); con conexión en casa (columna de oferta) 0.101 [0.096, 0.105]. La adopción es real y crece, pero la brecha es de oferta y de ingreso: D01 0.008 vs D10 0.218; Chiapas 0.017 vs CDMX 0.103. «Prefiere tienda física» es, en la mayoría de hogares, no tener conexión (D01 con internet: 0.177). El 17.7 % es de valor de retail, esto es de hogares: **escalas distintas, no se comparan**.
- **CONS-017 (OXXO infraestructura de efectivo)** — **CONFIRMA la parte de efectivo, MATIZA la de conveniencia.** El 0.813 [0.800, 0.823] del gasto directo G1 de 2022 se paga en efectivo (0.923 en D01, 0.627 en D10). Pero la tienda de conveniencia pesa 0.016 del gasto en alimentos para el hogar en las cuatro olas y 0.001 como lugar de la gran compra (ENGASTO 2012): la infraestructura de pagos de OXXO no es su peso como canal de alimentos.
- **CONS-023 (CDMX gasta 2.5× Chiapas)** — **CONFIRMA en orden, MATIZA en magnitud.** Gasto monetario mensual por hogar 2022, pesos corrientes: CDMX 19 633 [17 587, 22 253], Chiapas 8 648 [8 239, 9 057]; razón de puntos ≈ 2.3 (19 633 / 8 648); cotas por extremos de los IC 1.9–2.7 (no es un IC de la razón, que no se estimó). Es primero estructura (ingreso, precios, tamaño de hogar), no cultura regional.
- **CONS-001/CONS-004 (calidad sobre precio, lealtad)** — **NO-COMPARABLE**: ENIGH/ENGASTO no miden criterios de elección ni marcas.
- **Canal (APUEST-003 Bodega Aurrera; «el mercado y el tianguis»)** — **MATIZA.** En 2012 la gran compra se hacía en supermercado o club en 0.732 de los hogares que la hacen (86 % en ≥ 100 mil hab., 43 % en < 2 500), y fruta y verdura en mercado/tianguis/ambulante en ~0.52. En gasto de alimentos 2022 (ENIGH): abarrotes 0.278, específicas del ramo 0.313, súper/club 0.162, mercado 0.101, tianguis/ambulante 0.093. El gradiente por decil del súper (D01 0.048 → D10 0.327) y de la tiendita (D01 0.423 → D10 0.145) coincide con el de TLOC: **oferta de formatos no medida (NO-CONSTRUIBLE); no se lee como preferencia.**

### *Finanzas conductuales* (Behavioral Finance Mexicano)

- **CONS-011 (10–15 % de adultos tiene tarjeta de crédito)** — **NO-COMPARABLE en escala; MATIZA en dirección.** Hogares con al menos una tarjeta de crédito: 0.296 [0.291, 0.302] en 2022 (persona ≠ hogar; la cifra por persona está en ENIF, citada abajo). Gradiente D01 0.070 → D10 0.700.
- **FIN-009/FIN-024 (aversión a endeudarse; deuda como herramienta y trampa)** — **MATIZA.** Pagan deudas no hipotecarias 0.065 de los hogares en 2022 y reciben préstamos 0.047, ambos a la baja desde 2020. El pago de deudas **sube** con el ingreso (D01 0.026, D10 0.087): la deuda formal registrada es de quien tiene acceso. «No les gusta endeudarse» no se puede separar de no tener oferta — columna de oferta: `RESULT-DIN-OFERTA-EXCLUSION-ENIF{2012,2015,2018,2021}-CREDITO-*` (persona, ENIF; citada, no combinada).
- **Fiado (CONS-025 BNPL «llena el vacío de crédito formal»; FIN-019 confianza radial)** — **MATIZA.** Hogares con alguna compra al fiado: 0.128 (2016) → 0.085 [0.082, 0.088] (2022), IC calibrado [0.063, 0.113]; **más** en D10 (0.099) que en D01 (0.051) y más en localidades < 2 500 (0.103) que en ≥ 100 mil (0.070). No es un sustituto del crédito que usen los más pobres; es un circuito de proximidad rural. Oferta de fiado NO-CONSTRUIBLE.
- **Uso de tarjeta en alimentos, condicional a tenerla (oferta):** 0.230 [0.220, 0.240] en 2022 — entre quienes tienen tarjeta, 3 de 4 no la usan para comida en el mes (CONS-033, desconfianza del pago con tarjeta: **CONFIRMA en dirección**, sin aislar el motivo).

### *El Clasemediero Mexicano*

- **CLASE-014 («72 % de los mexicanos gasta más de lo que gana»)** — **ROMPE como cifra poblacional.** Hogares con gasto monetario trimestral > ingreso corriente trimestral: 0.171 [0.168, 0.175] en 2022, estable 0.17–0.19 en 2016–2022 (IC calibrado [0.152, 0.193]). Es 0.450 en D01 (ingreso transitoriamente bajo, gasto con ahorro o transferencias no captadas: efecto de medición de un trimestre, no conducta) y 0.053 en D10. La cifra del report viene de clientes de una reestructuradora de deudas (muestra seleccionada), no de hogares.
- **CLASE-015 (el crédito permite «aparentar» clase media)** — **NO-COMPARABLE**: no hay motivo en el dato. Sí se puede decir que la tenencia y el uso de tarjeta se concentran en D8–D10.

### Estructura del gasto (encargo §1)

Participaciones del gasto monetario agregado 2022 (razón de totales): alimentos 0.377 [0.373, 0.380] (D01 0.511, D10 0.283: Engel, no cultura); transporte (incluye comunicaciones) 0.193; educación y esparcimiento 0.098; vivienda 0.095; personales 0.077; limpieza 0.061; vestido y calzado 0.038; salud 0.034; transferencias 0.028. Comida fuera: 0.196 de lo gastado en alimentos (D10 0.355, D01 0.082), con el hoyo de 2020 (0.134). Bebidas: 0.068 del gasto en alimentos, casi plano por decil (SALUD-001/SALUD-026: el «consumo compensatorio» de los hogares pobres **no se ve** como mayor participación de bebidas — MATIZA; el dato no separa refresco de alcohol). Comunicaciones 0.049 del gasto; 0.903 de hogares gasta algo en ellas; celular 0.923, internet 0.606. **Remesas:** se citan `CALC-ENIGH{2016,2018,2020,2022}-REMESAS-CONTEXTO-0001` e `-INTENSIDAD-REMESAS-0001`; no se re-midieron.

## 4 · Módulo de auditoría

- **Contadores:** mueve «N conductas con piso GEN2 por dominio» (CONSUMO 0 → 48; DINERO +9). Ningún otro.
- **¿Pobreza/informalidad confundidas con cultura?** El riesgo mayor del report: canal, efectivo, fiado y tarjeta siguen al decil y al tamaño de localidad. Todo gradiente se lee primero como ingreso y oferta; la oferta de formatos y de fiado es NO-CONSTRUIBLE y así se dice.
- **¿Clase media urbana?** Los pisos van por decil, TLOC y entidad; D01 y < 2 500 hab. se publican aparte. El 17.7 % de e-commerce y el 72 % de «gasta más de lo que gana» son cifras de clase media urbana conectada o de muestras seleccionadas.
- **¿Qué parece psicológico y es incentivo?** Pagar en efectivo en D01 (0.92) y no usar la tarjeta que se tiene: costos, comisiones y oferta, no «desconfianza cultural» sin más.
- **¿Qué afirmación se escribió a mano?** Ninguna cifra; todas de la tabla derivada o de RESULT por id.
- **Escalas y unidades:** hogar en todo el acto; participaciones = razón de totales (no el hogar típico); media en pesos corrientes, no comparable entre olas; nada se promedia con persona (ENIF).
- **PROSPECTIVA/RETROSPECTIVA:** nada prospectivo; todo es descripción retrospectiva de olas abiertas.
- **Peligroso leído simplista:** «el mexicano paga en efectivo» (es el pobre y el rural); «los ricos usan fiado» (es la localidad pequeña y el comercio de proximidad; D10 rural existe).
- **Deuda caducada / marcos importados / firewall genético:** no aplica; evidencia (a) únicamente.

## 5 · Adopción por instrumento (F-ASTRA-5-4)

Tres filas FP en `forense/firmas-pendientes.tsv`: `FP-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-01` (ENIGH, recomendada CON-RESERVA-DE-ANCHO), `-02` (ENGASTO, recomendada CON-RESERVA-DE-ANCHO), `-03` (retiro de las conductas desde `gastoshogar` 2016/2018 de 0001 como piso, recomendada VETAR esas filas de 0001 y adoptar las de 0002).
