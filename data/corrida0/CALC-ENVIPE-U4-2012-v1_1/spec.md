# `CALC-ENVIPE-U4-2012-v1_1` — cara mecánica

Gobierna esta corrida la spec SELLADA
`forense/prereg-caja/ENVIPE-2012-U4-spec-v1_1.md` (**`prereg-caja-ENVIPE-2012-U4` v1.1**,
sucesora de v1.0, que no se edita; sha256 en el sidecar y en `spec.yaml`).
COMMIT-3 de la pieza P2 de `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1` (D-11:
corrección hacia adelante). Corrida v1.0 intacta: `data/corrida0/CALC-ENVIPE-U4-2012/`.

## Lo único que cambia

El par de diseño `(EST, UPM)` de cada persona de `U4` sale de `Tmod_Vic.DBF`
por hogar (estrato de diseño de 3 dígitos, 361 valores), no de `tper_vic.dbf`
(cuyo `EST` trae 4 valores y no es el de diseño, contra lo que el FD declara).
Guardias: par único por hogar en `Tmod_Vic`; `UPM` coincidente entre tablas;
control exacto del punto contra v1.0 (`G-CONTROL-V1-0`).
