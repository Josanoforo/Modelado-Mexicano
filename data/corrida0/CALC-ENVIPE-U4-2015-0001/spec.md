# CALC-ENVIPE-U4-2015-0001

Medición descriptiva prospectiva en unidad **persona** para ENVIPE 2015
(victimización 2014), gobernada por
`forense/prereg-caja/ENVIPE-U4-2013-2015-spec-v1_0.md`.

Une eventos elegibles de `TMod_Vic.dbf` con la persona seleccionada de
`TPer_Vic2.dbf` mediante `(UPM,VIV_SEL,HOGAR,R_SEL)`, exige `ID_PER`, colapsa
C1/C2 por máximo y pondera una vez por persona con `FAC_ELE`. `UPM_DIS`, no
`UPM`, es la UPM de diseño. La incertidumbre es sólo sensibilidad sobre el
marco observado; no está aprobada para inferencia plena.

Al congelar este archivo y su medidor sólo se habían usado documentación,
cabeceras DBF y fixtures sintéticos, no registros del microdato.
