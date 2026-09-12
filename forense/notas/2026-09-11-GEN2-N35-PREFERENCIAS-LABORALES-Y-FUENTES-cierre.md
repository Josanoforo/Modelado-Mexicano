# Cierre · GEN2 N35 preferencias laborales y fuentes

## Resultado

Se ejecutó `CALC-MOTRAL2015-VALORACION-SS-0001` sobre los bytes reales de
MOTRAL 2015 y ENOE 2015-T2. La corrida quedó sellada y `verify` devolvió
`REPRODUCE` con `CONTEXTO=IDENTICO` para 42/42 RESULT y 6/6 inputs. El punto
P17 total es 0.823626705331; los 32 estimandos, denominadores y precisión se
publican en `data/motral2015-valoracion-ss/estimandos-motral2015.csv`.

El control independiente con `dbfread` reconstruyó P17 total (masas
17,498,432 / 21,245,586), el tratamiento de P16 (5,696 rankings completos,
2 incompletos con primer lugar, 6 sin primer lugar, 0 inconsistentes) y el
enlace ENOE (6,564 coincidencias, 436 pérdidas, 0 duplicados). Los 5,704
elegibles MOTRAL tuvieron enlace.

## Correspondencia documental

El cuestionario oficial 2015 ubica P16/P17 en su página 1. El descriptor
acredita `P16_1..P16_5`, `P17`, llave, diseño y `FAC_MOTRAL`. La población
analítica sigue el universo oficial 18–54 con experiencia laboral, entrevista
completa y `C_TRA` válida. Para empleo actual se usó `SDEMT215.DBF`:
`CLASE2=1` y `SEG_SOC` 1/2, unidos por
`CD_A+ENT+CON+V_SEL+N_HOG+H_MUD+N_REN`; no se sustituyó por el último empleo
retrospectivo MOTRAL.

`corrida0 spec-check` confirmó las 20 variables MOTRAL. Sus 9 variables SDEM
no aparecen aún en el inventario general porque el ZIP ENOE se adquirió en
este acto y 39 posee el extractor/overlay; el payload físico, el descriptor
oficial y la ejecución acreditan los campos. No se editó el perímetro de 39.

## Adquisición dirigida

Se obtuvieron desde los enlaces exactos de EEA-ESEM el paper de marzo de 2026
(48 páginas, SHA-256 `8a71718f...5121b3`) y la presentación de agosto de
2026 (60 páginas, `6e49c00f...8b275`). Ambos se registraron en manifiesto y
quedan fuera de Git bajo `data_raw`.

El DCE encuestó cara a cara en septiembre–octubre de 2024 a personas de
25–64 años de diez áreas metropolitanas; reporta 4,833 participantes y usa
3,922 que pasaron la trampa en la estimación base. Aleatoriza 64 bloques de
cuatro pares, orden y lado. Los atributos son seguridad social, contrato,
jornada/flexibilidad, autonomía, traslado e ingreso (0/+10/+20/+25%). La
tabla 2 publica WTP por seguridad social de 0.240 del ingreso (EE 0.023).
Es transcripción publicada, no reproducción ni parámetro adoptado.

No se localizó código, datos ni cuestionario público exacto en sesión,
páginas de autores, OSF, Dataverse, Zenodo o GitHub. El paper dice que el
instrumento está en Appendix C, pero el PDF termina en Appendix B. Queda
como residual una petición no enviada de Appendix C, asignación de bloques,
microdato anonimizado y código de tablas 2–5.

## Registro y alcance

La relación `REL-31a794c27eca54d8d773df15` se actualiza por clave, conservando
la evidencia 2012 y corrigiendo sólo el descarte excesivo de 2015. La
comparación salarial estricta sigue `EXISTE-NO-SATISFACE`; no hay adopción,
cambio de tier ni edición de NC-0164/NC-0165. El puente consumible por 40 está
en `forense/notas/2026-09-11-GEN2-N35-PREFERENCIAS-LABORALES-Y-FUENTES-puente-a-40.md`.

Worktree: `/home/pc0/mm-gen2-n35-preferencias-laborales-fuentes`.
Rama: `acto/gen2-n35-preferencias-laborales-fuentes`.
Entrega revisable: PR #747; gobernanza: `ADR-493` (renumerado tras fusionarse
PR #746 como `ADR-492`).
