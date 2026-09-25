# Piso C2 de ahorro solo informal ENIF 2024 (localidad × edad), re-medido desde microdato · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-PISOS-GEN2-2`, 24/sep/2026, CAJA, rama `acto/gen2-pisos-gen2-2`,
0-bis `25185b7e`. Encargo archivado: `forense/encargos/2026-09-24-GEN2-PISOS-GEN2-2.md` (P2).
Congelada en el COMMIT-1, **antes** de ejecutar su medidor sobre ENIF 2024.

## 0 · Por qué existe, y qué se interpreta del encargo

El censo P1 (`forense/analisis/pisos-gen2/censo-antes-8358b891.tsv`) clasifica
HEREDADO-DE-LEGACY los 8 `-C2-P` que el marcador consume de
`DIN.ahorro_solo_informal.enif2024.localidad_x_edad`: `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001`
(`medidor.py:373,391-408`) los compone con `parametros.marginales_sellados_D9`, seis decimales
tecleados de `milpa/tramite-ola5-propuesta-v0.yaml` (E1-E4, L1-L2) y de `milpa/tramite.yaml`
(nacional).

**INTERPRETACIÓN-DECLARADA (cláusula 1/2).** El encargo dice «piso medido desde microdato de la
ola anterior». El C2 de esta celda-D **no es de la ola anterior**: es
`expit(logit p₂₄(L) + logit p₂₄(E) − logit p₂₄)`, marginales de **la misma ola (2024)** sin
interacción; lo legacy son los **números**, no la ola. Un piso de 2021 cambiaría el contendiente
C2 (PARO d, regla 6). Se sigue el precedente que mesa ya resolvió en el mismo punto
(`ENCIG2025-PISOS-GOBDIGITAL-spec-v1_0.md` §0, respuesta verbatim «Marginales 2025
(Recommended)»: «C2 con la MISMA definición, re-medido desde el microdato»). Por eso el CALC es
`CALC-ENIF2024-PISOS-…`. (El encargo nombra el patrón `CALC-ENCIG2023-PISOS-GOBDIGITAL-0001`; el
CALC sellado de #1116 es `CALC-ENCIG2025-PISOS-GOBDIGITAL-0001`: discrepancia de rótulo,
declarada.)

## 1 · Estimando, universo, celdas

**Mismo objeto que las emisiones** (`DIN-ahorro-solo-informal-lxe8-spec-v1_2.md` §3): personas
elegidas de 18 años y más de TMODULO ENIF 2024; `D9` = ahorra por alguna vía informal
(`p5_1_1..6 = 1`) y por ninguna de las nueve formales (`p5_6_1..9 = 1`). Universo: los tres
filtros de las emisiones en su orden (`18 ≤ edad_v ≤ 97` sin centinelas 98/99; `tloc ∈ {1..4}`;
`fac_per > 0`), **ejecutados desde los bytes del medidor sellado de las emisiones**. Ponderador
`fac_per`; diseño `est_dis × upm_dis`.

**Marginales (7):** L1 (`tloc` 3-4, menos de 15 000 hab.), L2 (`tloc` 1-2), E1-E4 (18-29 · 30-44
· 45-59 · 60-97), NAC. **Celdas C2 (8):** `L×E` por `piso_log_aditivo` de
`tests/test_celda_d_c2.py` (el objeto que usaron las emisiones); marginal 0/1 → `None`.

**Agrupación: UNA sola variable, siempre.** `_Guardia.registra` PARA ante dos ejes; el cruce de
2024 ya lo derivó el -0001 (E.6) y este CALC no lo necesita.

## 2 · Incertidumbre

Bootstrap de conglomerados estratificado de las emisiones (`_replicas`, `_punto_e_ic`):
**10 000 réplicas, `PCG64(42)`**, estratos y UPM en orden lexicográfico. IC de C2: percentiles
2.5/97.5 de la composición réplica a réplica, sólo si el control 1 da `REPRODUCE` y ninguna
réplica queda indefinida; si no, `None` con el estado en `G-C2-IC-ESTADO`.

## 3 · Controles (umbrales declarados antes de correr)

1. **Oro: las emisiones selladas** (`funcion: CONTROL-HISTORICO`). Mismo código, misma semilla y
   mismo universo: los 7 marginales (`-N` exacto; `-P`, `-IC95*` a `1e-10`), el
   `-C2-P-REDERIVADO` y el `-C2-IC95*` de las emisiones, a `1e-10` → `REPRODUCE`. Prueba que este
   piso es la composición que las emisiones ya habían re-derivado del manifiesto, ahora en un CALC
   de cadena limpia. Condiciona el IC.
2. **Árbitro marginal** `CALC-ARBITRO-MARGINALES-ENIF2024-0001`. Su universo **no es el mismo**:
   edad 18-96 y cada eje sobre su propio denominador válido. Los valores sellados de ambos CALC,
   leídos antes de abrir el dato, muestran que E1-E3 coinciden (Δ 0.0, `-N` igual) y que L1, L2,
   E4 y NAC difieren por el universo (E4: 60-97 contra 60-96, 5 personas de 97; L/NAC: el árbitro
   conserva filas sin edad válida). Gating: **E1-E3** a `1e-10` y `-N` exacto; L1, L2, E4, NAC
   se emiten como Δ descriptivos. Un `NO-REPRODUCE` se reporta; no ajusta nada.
3. **Contra el C2 legacy, descriptivo** (`origen_numerico: MIXTO` de esta fila): `C2-P − C2-P
   (emisiones)` por celda y su máximo absoluto. El propio CALC de emisiones ya decía
   `CTRL-ARBITRO-VEREDICTO = NO-REPRODUCE` (Δ 1.20e-3): se espera un Δ de ese orden.

## 4 · Guardias (PARA si fallan)

Lista cerrada de ocho inputs; el sha de `emisiones_resultados` y el de
`arbitro_enif2024_resultados` deben estar en sus `sello.json`; ninguna agrupación de dos ejes.

## 5 · Secuencia y validación D-22

COMMIT-1: esta spec, `spec.yaml`, `medidor.py`, `tests/test_pisos_gen2_2.py`. COMMIT-2: `corrida0
run`, sello, asiento E.7. D-22 (payloads fabricados): cadena completa con controles REPRODUCE;
control que no reproduce (sin IC, el -0002 PARA); inputs fuera de lista; sello falso; guardia de
dos ejes; `resultados:` = ids emitidos por la corrida sintética. **Ninguna ejecución diagnóstica
sobre ENIF 2024:** el primer `run` es el resultado.

## 6 · Auditoría (afirma sobre México)

Proporciones de **personas de 18+** que ahorran sólo por vías informales; «localidad menor de
15 000» es tamaño de localidad, no ruralidad administrativa. Un gradiente por edad o tamaño de
localidad describe **acceso y oferta** (sucursales, corresponsales, cuenta) antes que
preferencia. **RETROSPECTIVA:** sellado después de que el -0001 derivó R; su fórmula no tiene
variante y no lee R. **Cifra escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
