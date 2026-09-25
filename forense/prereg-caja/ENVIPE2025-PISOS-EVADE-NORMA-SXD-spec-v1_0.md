# Piso C2 de evasión de la norma ENVIPE 2025 (escolaridad × dominio), re-medido desde microdato · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-PISOS-GEN2-2`, 24/sep/2026, CAJA, rama `acto/gen2-pisos-gen2-2`,
0-bis `25185b7e`. Encargo: `forense/encargos/2026-09-24-GEN2-PISOS-GEN2-2.md` (P2). Congelada en
el COMMIT-1, **antes** de ejecutar su medidor sobre ENVIPE 2025.

## 0 · Por qué existe

El censo P1 clasifica HEREDADO-DE-LEGACY los 12 `-C2-P` que el marcador consume de
`TRA.evade_norma.envipe2025.escolaridad_x_dominio`: `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001`
(`medidor.py:223,281-291`) los compone con `parametros.marginales_sellados` (seis decimales de
`milpa/tramite-ola5-propuesta-v0.yaml:1715-1731`; nacional de `milpa/tramite.yaml:497`).

**INTERPRETACIÓN-DECLARADA** (cláusula 1/2), idéntica a la del piso ENIF
(`ENIF2024-PISOS-AHORRO-INFORMAL-LXE-spec-v1_0.md` §0): el C2 es la composición de marginales de
**la misma ola (2025)**; lo legacy son los números. Se re-miden los marginales 2025 desde el
manifiesto con la misma definición (precedente de mesa en #1116). ENVIPE 2025 no es ola
reservada del encargo (§7 a nombra ENVIPE 2026).

## 1 · Estimando, universo, celdas

**Mismo objeto que las emisiones** (`TRA-evade-norma-sxd12-spec-v1_0.md`): DELITOS de `tmod_vic`
con `BP1_20 ∈ {1,2}`; `evade_norma` = `BP1_20 == 2` y `BP1_23 ∈ {04,05,06,08}`; ponderador
`FAC_DEL`; escolaridad_proxy de `tsdem.NIV` (S1 hasta primaria · S2 secundaria · S3 media
superior · S4 superior); dominio D1 Rural · D2 Complemento urbano · D3 Urbano. Todo desde los
bytes de `tools/celda_d/marginales_reproduccion.py` (sha en el `spec.yaml`), el módulo congelado
que usaron las emisiones, con la ola cargada **`reservada=True`**: `cruce()` lanza `ReservaRota`
y el medidor lo prueba en cada corrida (`G-GUARDIA-CRUCE-DERIVADO = NO`).

**Marginales (8):** S1-S4, D1-D3, NAC; punto e IC de cada uno por `wprop_ic_conglomerado`
(la función del árbitro). **Celdas C2 (12):** `S×D` por `piso_log_aditivo`.

## 2 · Incertidumbre

Réplicas compartidas del módulo (`replicas_compartidas`, **10 000, `PCG64(42)`**). IC de C2:
percentiles 2.5/97.5 de `expit(logit p_r(s) + logit p_r(d) − logit p_r)` sobre las réplicas
definidas (misma línea de las emisiones); sólo si el control 1 da `REPRODUCE` y ninguna réplica
queda indefinida.

## 3 · Controles (umbrales declarados antes de correr)

1. **Oro: las emisiones selladas** — `G-M25-MARG-*` (`-N` exacto; `-P`, `-IC95*` a `1e-10`),
   `G-M25-P-NACIONAL`, `-C2-P-REDERIVADO` y `-C2-IC95*` a `1e-10` → `REPRODUCE`. Condiciona el IC.
   El módulo ganó ejes aditivos (`sexo`, `edad`; `d8adce0b`, 19/sep) después del sello de las
   emisiones (`cdd78f99`, 17/sep); `wprop_ic_conglomerado` siembra por llamada, así que el orden
   de ejes no afecta: si afectara, este control lo delata.
2. **Árbitro** `CALC-ARBITRO-MARGINALES-ENVIPE2025-0001`: los 8 `-P` a `1e-10` y `-N` exacto
   (leídos sellados antes de abrir: Δ 0.0). Sus IC usan otro remuestreo y no se comparan.
3. **Contra el C2 legacy, descriptivo** (MIXTO): se espera Δ del orden de 1e-6 (el propio CALC de
   emisiones dio `-C2-P-REDERIVADO` a 1.1e-6 del legacy).

## 4 · Guardias (PARA si fallan)

Lista cerrada de nueve inputs; sellos de emisiones y árbitro verificados por sha; cruce sobre la
ola reservada debe lanzar.

## 5 · Secuencia y validación D-22

Como el piso ENIF (§5 de su spec). **Ninguna ejecución diagnóstica sobre ENVIPE 2025.**

## 6 · Auditoría (afirma sobre México)

Proporciones de **delitos** (no de víctimas) no denunciados por razones atribuibles a la
autoridad (pérdida de tiempo, trámites, desconfianza, hostilidad). La escolaridad es de la
víctima reportada en `tsdem`, proxy. Un gradiente por dominio describe **oferta institucional**
(distancia al ministerio público) antes que actitud. **RETROSPECTIVA:** sellado después de R.
**Cifra escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
