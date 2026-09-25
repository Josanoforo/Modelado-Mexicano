# Re-adjudicación de TRA.evade_norma.envipe2025.escolaridad_x_dominio con piso de cadena limpia · CALC -0002 · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-PISOS-GEN2-2`, 24/sep/2026, CAJA, rama `acto/gen2-pisos-gen2-2`,
0-bis `25185b7e`. Encargo: `forense/encargos/2026-09-24-GEN2-PISOS-GEN2-2.md` (P3). Congelada en el
COMMIT-1, antes de sellar el piso y de correr este árbitro. Firmas y nombre: idénticos a
`DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002-spec-v1_0.md` §0 (sucesor de
`CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001`).

## 1 · Herencia por identidad de archivo

El medidor de `CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001` (input `medidor_0001`, `funcion: CODIGO`,
sha256 en el `spec.yaml`) **se ejecuta sin editar**; su `spec.md`
(`TRA-evade-norma-sxd12-spec-v1_0`) se cita por sha; sus parámetros y semilla se copian verbatim
(+ `tol_oro_0001`). Mismos: R (12 celdas de ENVIPE 2025 por la receta del árbitro), soporte en las
tres olas, criterio por celda, umbrales, orden de parada, B-bis leído mecánicamente y
**contendientes: C1 y C2 pisos, C6 y C7 retadores**. C1, C6 y C7 siguen siendo los sellados en
las emisiones (C6/C7 se construyeron en su día sobre el C2 legacy y no se re-emiten: hacerlo
después de ver R los volvería retrospectivos).

## 2 · El único cambio, y lo que se añade

**Cambio:** en una copia de las emisiones selladas (escrita en un directorio temporal que se borra
al salir, porque el -0001 las lee por ruta) se sustituyen `RESULT-TRA-SXD12-C2-P-{celda}`,
`-C2-IC95INF-{celda}` y `-C2-IC95SUP-{celda}` por los de
`CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001`, **por id**. El -0001 usa el IC de cada candidato
sólo para el diagnóstico de signo (`SIGNO-*`), que no adjudica.

**Se añade:** ids `…-ARB-*` → `…-ARB2-*`; `-C2-P/IC95*-{celda}` del piso; `-C2-P-EMISION-0001-{celda}`;
`G-FUENTE-C2`, `G-PISO-C2-SHA256`; oro del -0001 a `1e-10` sobre todo id que no depende de C2
(excluye `-D-C2-`, `-DENTRO-IC-R-C2-`, `-SIGNO-C2-`, `-VS-C2-`, `-VEREDICTO-CELDA-`,
`-GANA-A-AMBOS-PISOS`, `-INDECIDIBLES`, `-G-SIGNO-ESTABLE-C2`, `-G-MAE-C2`,
`-G-MEJOR-CANDIDATO-POR-MAE`, `-G-CHALLENGER-GANADOR`, `-VENCE-A-C2-EN-CELDAS`, `-G-B-BIS-LEIDO`);
`G-DICTAMEN-0001`, `G-DICTAMEN-CAMBIA`. Guardia: la de DIN, más `CTRL-ARBITRO-VEREDICTO =
REPRODUCE` del piso.

## 3 · Qué se espera y qué no se decide aquí

Δ legacy/medido ~1e-6 (las emisiones midieron 1.1e-6): se espera que nada cambie, **sin
predecirlo**; el primer resultado es el que se reporta. Registro como en DIN §3. **No adopta
retadores.**

## 4 · Secuencia

La de DIN §4.

## 5 · Auditoría (afirma sobre México)

Hereda la del -0001: proporciones de **delitos** no denunciados por razones atribuibles a la
autoridad, por escolaridad proxy de la víctima × dominio; oferta institucional antes que actitud.
**C2 RETROSPECTIVA**; C1/C6/C7 PROSPECTIVA. `celdas_validadas` no cambia de número.

El primer resultado que produzca este procedimiento es el que se reporta.
