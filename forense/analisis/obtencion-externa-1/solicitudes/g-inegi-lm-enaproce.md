# (g) Laboratorio de Microdatos INEGI · ENAPROCE 2015/2018 para la parte PyME de R03 — ARCHIVADA COMO NO NECESARIA

Estado: **ARCHIVADA-NO-NECESARIA** (28/sep/2026). No se envía.

## Regla del encargo
P4-g: «**solo** si MAPA-INSTRUMENTOS-ALTERNOS-1 concluye que ENCRIGE/ENVE no cubren la parte PyME de R03; si no, la solicitud de `P4-I1-solicitud-LM.md` se archiva como no necesaria y se dice por qué».

## Estado del acto del que depende
- 27/sep ~21:10: la rama de MAPA sólo tenía su 0-bis (`4b11076a`); esta pieza quedó CONDICIONADA.
- 28/sep: [EJECUTADO] `gh pr view 1255` → `MERGED` 2026-09-28T14:37:48Z (merge `8f62e71c` en `origin/main`). El mapa está en `canon/mapa-instrumentos-alternos-v1_0.tsv` (commit `37d10fbc`), fusionado a esta rama.

## Por qué no es necesaria (LEÍDO, filas R03 del mapa y hoja para mesa)
- **ENCRIGE 2020** — unidad «empresa (razón social); universo nacional, **todos los tamaños**»; dictamen `EXISTE-SATISFACE-PARCIAL(los cinco ítems i–v existen por variable con texto de pregunta; faltan vía de acceso al microdato y variables de diseño ejecutables)`; reactivos `P9_3_1..P9_3_3`, `P9_2`, `P9_4/P9_5` (mordida en trámites) y `P5_5`, `P5_7/P5_8`, `P8_3`, `P8_7` (carga regulatoria). El tamaño PyME se obtiene filtrando por `P1_4CAL`.
- **ENVE 2024** — «establecimiento; universo nacional por estrato de tamaño×sector»; `EXISTE-SATISFACE-PARCIAL(experiencia directa de corrupción, tamaño, sector y factor de expansión; faltan ii y iii)`.
- `hoja-para-mesa-mapa-instrumentos-alternos.md` §I1: «La mordida en la empresa **sí se mide en el corpus**, pero no en ENAPROCE» · recomendación (d): ENAPROCE NO-ACCESIBLE para R03 y R03 fundida con R08 sobre ENCRIGE 2020, porque «no abre trámite de identidad por ENAPROCE».
- Lo que ENAPROCE daría por Laboratorio es sólo carga regulatoria (su cuestionario no pregunta pago informal: `P4-I1-nota.md`), y el mapa encuentra carga regulatoria y mordida juntas, con todos los tamaños, en ENCRIGE 2020.

Conclusión: la condición («ENCRIGE/ENVE **no** cubren la parte PyME») **no se cumple**; se toma la otra rama del encargo. La solicitud de `forense/analisis/obtencion-previa-1/P4-I1-solicitud-LM.md` queda archivada como no necesaria para R03.

## Lo que esto no decide
- No firma I1 (d) ni funde R03 con R08: eso es de mesa (texto de firma listo en la hoja de MAPA).
- La solicitud **opcional** de microdato ENCRIGE 2020 al Laboratorio (`TR_ENCRIGE2020`, `TR_ENCRIGE2020_TRAMITES`) que MAPA menciona es otra solicitud, de otro objeto; «la decide mesa aparte» (texto de MAPA). No se redacta aquí.
- Si mesa rechaza (d) y elige (a) de la hoja de MAPA, el texto listo sigue en `P4-I1-solicitud-LM.md` (formato del LM en corpus por sha: id `inegi_laboratorio_microdatos_solicitud_uso`, `5a5d041d…15c19`; la ruta que cita esa nota no es la registrada).
