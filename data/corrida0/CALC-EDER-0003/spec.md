# `CALC-EDER-0003` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/EDER-UNION-LIBRE-spec-v1_0.md`
(**`prereg-caja-EDER-UNION-LIBRE`**, `sha256 5901271777b1d6b6e0d86e9ebc521afcdcacb45db8deac02ae195308d7217abd`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1`, 15/sep/2026, **NUBE**, sobre `f5a5227`.
**Releva:** el **payload** de `CORR-0013` (EDER2017) → `RES-0043`, `RES-0044`.
Consumidor: `milpa/tramite.yaml:familia.union.libre` (`R5.3`).

**CONGELADO en el COMMIT-1, en NUBE, antes de abrir un solo byte de microdato.**

---

## El defecto material que esta corrida asienta

`RES-0043`/`RES-0044` declaran `payload = eder_2017_eder2017_bases_csv`
(`sha256 bcc7eb90…`) y `clase = MEDIDO·p(… ENADID 2023, p3_27_ag)`.
**El payload declarado no produjo el número.** Consecuencias: (1) un `verify`
resolvería el ZIP de EDER como INPUT de una cifra calculada sobre ENADID, y el
hash *coincidiría*; (2) `grep ENADID data/corrida0/demanda-corridas.tsv` → **0
aciertos**: el instrumento que produjo la cifra activa no aparece en ninguna
corrida; (3) **no hay control positivo posible** —
`A-DELTA-VS-GEN1 = NO-APLICA-ESTIMANDO-DISTINTO`, declarado y no calculado.

Esta corrida mide **EDER**: tipo de la **primera** unión, retrospectivo.
La celda ENADID **no se toca**; sustituirla es decisión de mesa.

## Qué mide

| familia | unidad | archivos | desenlace | ponderador |
|---|---|---|---|---|
| **A** · tipo de primera unión | **PERSONA** | `historiavida.csv` × `antecedentes.csv` × `vivienda.csv` | primer `edo_civil1` no-cero en orden de `anio_retro` | `factor_per` |
| **B** · eje de cohorte | persona | idem | idem por tramo de `anio_nac` | `factor_per` |

**El desenlace, el ponderador y el diseño viven en tres archivos distintos**
(`A.15(c)`): `edo_civil1` en `historiavida.csv`, `factor_per` en
`antecedentes.csv`, `est_dis`/`upm` en `vivienda.csv`.

## El mapa de códigos, del FD y no del nombre

`LIBRE = {1,12,13,14,17,18,126}` · `DIRECTO = {2,3,4,26,27,28,46,47,48}`,
catálogo de 27 códigos verificado línea por línea contra `eder2017_fd.pdf` por
`ACTO MAESTRA35-L7`. El código `37` queda **sin clasificar y contado**, no se
fuerza. Los de disolución `{6,7,8,60,70,80}` no aparecen como primer-no-cero
(0 casos); si aparecen, `A-CENSURA-IZQUIERDA = DETECTADA`.

## Diseño

Bootstrap de `upm` con reemplazo **dentro de** `est_dis`, 2 000 réplicas,
`numpy.PCG64`, semilla `20260915`. `milpa/` declara `ic95: NO-APLICA` para
esta regla: el IC **nace aquí**. Mismo precedente que `CALC-EDER-0001`
(`ADR-501`), que reportó 3 estratos de UPM única sobre este instrumento.

## Lo que NO hace

No abre microdato · **no escribe el medidor** (lo escribe el acto de CAJA) ·
no mide ENADID · no promedia EDER con ENADID · no corrige `milpa/` ni el
derivado `demanda-resultados.tsv` · no sucede la segmentación por cohorte ya
sellada · no toca `CALC-EDER-0001` ni `CALC-EDER-0002`.
