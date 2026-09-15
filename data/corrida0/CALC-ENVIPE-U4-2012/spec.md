# `CALC-ENVIPE-U4-2012` — cara mecánica

Gobierna esta corrida la spec SELLADA
`forense/prereg-caja/ENVIPE-2012-U4-spec-v1_0.md`
(**`prereg-caja-ENVIPE-2012-U4`**, sha256 en el sidecar y en `spec.yaml`).
Sucesora por extensión de `R-ENVIPE-SERIE-DBF-spec-v1_0` (§5) y de
`ENVIPE-DENUNCIA-spec-v1_0` (`U4`); ninguna se edita. Donde este resumen y la
sellada digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1` (pieza P2, `NC-0099`),
14/sep/2026, CAJA (Ubuntu/WSL2), sobre `7de3acb4`.
**No releva ninguna `CORR-*`, no adopta, no toca `milpa/`.**

**CONGELADO en el COMMIT-1, antes de leer un solo valor del microdato.**

## Qué mide

`p(C2, U4)` y `p(C1, U4)` en ENVIPE 2012: proporción ponderada (`FAC_ELE`) de
personas seleccionadas con ≥ 1 delito personal no denunciado con razón
clasificable (`U1`) cuya razón principal, colapsada a persona por la regla
GEN1 («si algún delito califica, la persona = 1»), es miedo/desconfianza
(`C2` añade `08`). IC de diseño por `EST × UPM`.

## La ruta (lo que la fila `NC-0099` pidió declarar)

1. Delito → persona por `(CONTROL, VIV_SEL, HOGAR, R_SEL)` de `Tmod_Vic.DBF`.
2. `FAC_ELE`, `EST`, `UPM` de la persona desde `tper_vic.dbf` **por hogar**
   (regla de resolución §3.1 de la sellada: valor único en el hogar; si no,
   la única fila válida; si no, ambiguo → fuera, contado).
3. Existencia de la persona en `tsdem.DBF` por `N_REN == R_SEL` del mismo
   hogar, con cardinalidad medida (`0 / 1 / MULTI`): sólo `1` entra.

## Control interno

`P-C1-U1` y `N-U1` deben reproducir los `RESULT` sellados de
`CALC-R-CIV-M-01` (mismo payload, mismo universo `U1`): prueba de que el
lector y el universo son los mismos. `NO-REPRODUCE` no ajusta nada: se
atribuye.
