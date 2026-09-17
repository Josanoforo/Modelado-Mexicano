# CALC-ENVIPE-U4-2013-0001

Medición descriptiva prospectiva en unidad **persona** para ENVIPE 2013
(victimización 2012), gobernada por
`forense/prereg-caja/ENVIPE-U4-2013-2015-spec-v1_0.md`.

Une eventos elegibles de `tmod_vic.dbf` con la persona seleccionada de
`tper_vic.dbf` mediante `(CONTROL,VIV_SEL,HOGAR,R_SEL)`, colapsa C1/C2 por
máximo y pondera una vez por persona con `FAC_ELE`. La incertidumbre es sólo
sensibilidad sobre el marco observado; no está aprobada para inferencia plena.

Al congelar este archivo y su medidor sólo se habían usado documentación,
cabeceras DBF y fixtures sintéticos, no registros del microdato.
