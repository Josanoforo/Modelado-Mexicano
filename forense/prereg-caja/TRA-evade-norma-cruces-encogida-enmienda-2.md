# PILOTO 4 · enmienda de incorporación y adjudicación · 22/sep/2026

Esta enmienda acompaña la spec humana congelada en `445531a3` y la
`ADENDA-1` congelada en `b5a76652`. No altera sus cuerpos ni los RESULT
sellados en `COMMIT-2` (`eb7f7c25`).

## Plazo vigente de C-ASTRA

La instrucción posterior de Jonás sustituye exclusivamente el plazo de
`ADENDA-1` y de §4.1 de la spec: un CALC C-ASTRA solo es elegible si está
en `origin/main` **antes de COMMIT-2** del piloto. La presencia en COMMIT-1
dejó de ser requisito. Siguen vigentes las condiciones de identidad de
celda, congelación prospectiva, sello y tipo de intervalo.

`COMMIT-2` ocurrió en `eb7f7c25` con los 38 RESULT `C-ASTRA-P` vacíos y
`C-ASTRA-ESTADO=NO-ENTRA`. El PR #1031 seguía abierto, sin fusión a main;
los cuatro CALC no estaban en `origin/main`. Por tanto, C-ASTRA perdió la
ventana de este piloto. Una fusión posterior no modifica esta decisión ni
autoriza copiar sus puntos retroactivamente a las emisiones selladas.
El avance del HEAD del PR desde `7130ce2e5` hasta `159dc874` no cambió
ningún archivo de los cuatro CALC ni sus specs científicas; ese avance no
fue la causa de exclusión.

## Comparación científica y B-bis

La decisión posterior de Jonás limita C-ASTRA, si hubiera sido elegible,
a **comparación secundaria**. El B-bis primario conserva dos retadores
(`C7`, `C-ENCOGIDA`), cuatro cruces y ocho comparaciones. C-ASTRA no
altera su adjudicación global. Para evaluar puntos emitidos, el contrato
ya mantiene fijos los puntos de cada candidato y del piso, y remuestrea
el mismo R por conglomerado dentro de estrato para ambos errores en
cada réplica. Ese IC de `ΔMAE` es condicional a las emisiones. El intervalo
predictivo de ASTRA, también condicionado a marginales 2025, se reportaría
aparte; sus sorteos no se emparejan por posición con réplicas de R.
Como la ventana se perdió, esta regla secundaria queda sin ejecución en
este piloto y no se abren sus puntos ni R para recuperarla.

## Corrección del ejecutable antes de COMMIT-3

La spec §3 adjudica victoria solo cuando el límite inferior del IC de
`ΔMAE` frente a C2 supera 0 **y** 0.5 pp. Un límite inferior entre 0 y
0.5 pp es `PROPUESTA-CON-RESERVA`; un IC que incluye 0 no da victoria.
El conteo de celdas `≥¾` es descriptivo. El código de COMMIT-1 marcaba
`GANA` con `IC inferior > 0` **o** el conteo de celdas. Se corrige ese
desfase antes de abrir R, sin cambiar el criterio firmado ni las emisiones.

El `preflight` de COMMIT-3a exigió además `filtros` y `transformacion`,
campos omitidos del YAML de COMMIT-1 aunque definidos en la spec humana
§0 y §4. Se completan en el YAML del árbitro junto con los dos SHA256
de emisiones ya selladas. No se cambia la receta de R ni se abre el
cruce en COMMIT-3a.
