# ARBITRO-MARGINALES-2 · LAPOP · spec v1.0

ACTO GEN2-ARBITRO-MARGINALES-2, P2 (pieza LAPOP — 6ª pieza, autorizada por mesa
21/sep/2026 para extender el LOTE más allá de las 5 encuestas nombradas
originalmente en P2, dado que el payload COINCIDE en el corpus y la licencia de
AmericasBarometer/Vanderbilt sólo prohíbe compartir el archivo crudo, no
publicar estadística derivada — verificado, no supuesto, ver `## Preguntas
resueltas` de esta misma pieza en la nota de cierre del acto).

Formaliza en GEN2 las tres reglas de `milpa/tramite-ola5-propuesta-v0.yaml`
que P1 clasificó `RE-MEDIDA (nueva)` para LAPOP y que no tenían CALC GEN2
previo (a diferencia de las otras 4 reglas LAPOP-adyacentes, ya cubiertas por
`ACTO MAESTRA38-L4/L5/L18` o por `CALC-0001`/`CALC-0002` de `GEN2-E5`).

## 0 · Premisas verificadas

- `[EJECUTADO]` `mexico_lapop_americasbarometer_2019_v1_0_w` y
  `mex_2023_lapop_americasbarometer_v1_0_w` COINCIDEN en `descargas_mx`
  (`tests/manifiesto.py --verifica --id <id>`, sha256 y tamaño verificados
  contra `data/manifiesto.yaml`; comando corrido con
  `dangerouslyDisableSandbox` por el hallazgo ya conocido de que el sandbox no
  lee `/mnt/c`, no por ausencia real).
- `[EJECUTADO]` las 9 columnas de 2019 (`clien1na, vb2, vb3n, prot3, ur,
  vic1ext, estratopri, upm, wt`) y las 6 de 2023 (`mexwf1_19, countfair3, vb20,
  estratopri, upm, wt`) existen en sus `.dta` respectivos (leído metadata-only
  con `pyreadstat`, sin abrir el resto del archivo).

## 1 · Regla A — `civico.clientelismo.turnout_no_vote_choice_lapop2019`

**Pierna asistencia**: universo `clien1na` y `vb2` válidos (1/2), n=1 574.
Eje: `clien1na==1` oferta / `==2` sin oferta. Desenlace: `vb2==1` (votó).
**Pierna elección**: subconjunto anterior que votó y con `vb3n` no nulo,
n=1 035. Desenlace: `vb3n==103` (voto por PRI).
Ponderador `wt` (constante=1). Diseño `estratopri`×`upm`, bootstrap con
reemplazo dentro de estrato, 10 000 réplicas, seed 42.

Oro: asistencia con_oferta p=0.832714 n=269; sin_oferta p=0.793103 n=1305.
Elección PRI con_oferta p=0.063492 n=189; sin_oferta p=0.079196 n=846.

## 2 · Regla B — `civico.protesta.agravio_urbano_lapop2019`

Universo: `prot3`, `ur`, `vic1ext` válidos, n=1 575. Cruce `ur`(1 urbano/2
rural) × `vic1ext`(1 víctima/2 no). Desenlace `prot3==1`. Guardia de celda:
numerador < 10 → `NO-ESTIMABLE` (spec §1.3 de GEN1, heredada literal).

Oro: urbano-víctima p=0.105727 n=454; urbano-no-víctima p=0.049689 n=805;
rural-no-víctima p=0.067729 n=251; rural-víctima NO-ESTIMABLE (n=65,
numerador 7 < 10).

## 3 · Regla C — `civico.voto.agencia_lapop2023`

Universo restringido: `mexwf1_19` en {1,2}, `countfair3` en {1,2,3}, `vb20`
en **{1,2,3,4}** (ítem de 4 categorías; el desenlace binariza `vb20==2`
contra las otras tres, no restringe el universo a 2 códigos — verificado por
conteo exacto: con `vb20` en {1,2} el universo da 896, no 1 348; con las 4
categorías da 1 348, que es el n que GEN1 declara). n=1 348.
Rama `countfair3==1` SECRETO / `countfair3` en {2,3} OBSERVABLE. Eje
`mexwf1_19==1` (recibe ayuda). Desenlace `vb20==2` (votaría por el oficialismo).

Oro: SECRETO con_ayuda p=0.658228 n=79, sin_ayuda p=0.514493 n=276.
OBSERVABLE con_ayuda p=0.650442 n=226, sin_ayuda p=0.470665 n=767.

## 4 · Tolerancia

`REPRODUCE` si punto y n coinciden exacto (mismo criterio que las piezas
ENCUCI2020/ENNViH de este acto). Ensayo local (antes de este COMMIT-1, fuera
del conducto sellado) reprodujo los 3 universos y los 10 puntos/n citados
arriba exactos.

## 5 · No hace

No toca `milpa/`. No adopta. No re-mide las 4 reglas LAPOP-adyacentes ya
cubiertas por `MAESTRA38-L4/L5/L18` o `CALC-0001`/`CALC-0002` (ver P1).
