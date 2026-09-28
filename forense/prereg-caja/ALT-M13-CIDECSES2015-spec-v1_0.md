# M13 · CIDE-CSES 2015 (poselectoral nacional) · participación y peso percibido del voto por concurrencia local

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-CALC-ALTERNOS-LOTE-1` (0-bis `795b1053`), fila 32 de
`canon/mapa-instrumentos-alternos-v1_0.tsv`. Firma R08 A2 (b), 28/sep/2026:
«M13 (CIDE-CSES 2015 con clasificador de concurrencia del calendario INE)».
La fila 33 (CSES Módulo 5) es RESERVADA (R04) y no se abre: `DIFERIDO-A`
apertura. Un CALC: `CALC-ALT-M13-CIDECSES2015-0001`.

## Clasificador de concurrencia: del marco del propio estudio, no de un calendario externo

El calendario INE no está en el corpus (la fila lo marca «OBTENER si no está
en el corpus»). El propio estudio CIDE-CSES 2015 trae un segundo
levantamiento, `cide_cses2015_nacional_preelectoral.sav`, cuyo `p3` pregunta
«¿Pudo usted votar en la elección para gobernador/pdte mpal (DF: jefe
delegacional) del pasado 7 de junio?» y cuyo `dominio2` es «Tipo de elección
local» (`Gobernador` / `Sólo Presidente Mpal`): es la muestra de las
entidades **con elección local el 7 de junio**. Las etiquetas de valor de su
`edompio` (metadato, leído con `metadataonly=True`, sin valores) nombran
municipios de 16 entidades: `3` BCS, `4` Campeche, `6` Colima, `9` DF,
`11` Guanajuato, `12` Guerrero, `14` Jalisco, `15` México, `16` Michoacán,
`17` Morelos, `19` Nuevo León, `22` Querétaro, `24` San Luis Potosí,
`26` Sonora, `27` Tabasco, `31` Yucatán. Clasificador, fijado aquí:
`CONCURRENTE` := `estado` ∈ esas 16; `NO-CONCURRENTE` := las otras 16.
Límite declarado: el marco muestral de un levantamiento local no es un
calendario oficial; Chiapas (elección local el 19 de julio, no concurrente
con el 7 de junio) queda en `NO-CONCURRENTE`, que es su clasificación
correcta para la jornada federal. El detalle Gobernador frente a sólo
municipal no se usa (exigiría abrir valores del otro levantamiento).

## Qué ya está medido (E.5)

`ya_medido.py R7.1` → `NUNCA-MEDIDA`. `CALC-0001`/`-v2` usan CIDE-CSES 2015
para alineamiento partidista (`pcyc*`, `peledip`); ninguno `p3`, `p17`, `p18`.

## Estimando, unidad, escala, universo

- **Unidad:** persona del levantamiento poselectoral nacional (electorado
  federal, intermedia del 7/jun/2015).
- **Reactivos (A.15, etiquetas del .sav):**
  - `p3` — «¿Pudo usted votar en la elección para diputados federales del
    pasado 7 de junio?» Válidos `{1 Sí, 2 No}`; evento `{1}`; `3 No tenía
    edad`, `8 NS`, `9 NC` fuera y contados.
  - `p17` — «… UNO significa que NO importa qué partido es el que gobierna y
    CINCO … SI HAY UNA GRAN DIFERENCIA». Válidos `1–5`; evento `{4, 5}`.
  - `p18` — «… UNO significa que el voto NO influye mucho … y CINCO que el
    voto hace una GRAN diferencia». Válidos `1–5`; evento `{4, 5}`.
- **Escala:** proporción ponderada; contrastes en diferencia de
  proporciones.
- **Celdas:** nacional, `CONCURRENTE`, `NO-CONCURRENTE`. Contrastes
  pre-registrados `CONCURRENTE − NO-CONCURRENTE` para los tres reactivos.
  n mínimo 30.

## Ponderador y diseño

`PONDFIN` («Ponderador nacional»), estrato `dominio` (`11/12/13`, estados
por partido gobernante), UPM `upmmn`. IC95 bootstrap UPM en estrato, 2 000
réplicas, semilla PCG64 `20260928`, pareado.

## Agregador (E.1)

Razón de sumas ponderadas por celda.

## Qué pasa si el falsador no refuta

Participación declarada (sobre-reporte conocido) y concurrencia no asignada
al azar. Si el contraste de `p3` tiene IC95 > 0, la lectura «la elección
local concurrente acompaña más participación» es **consistente**; si cubre
0, **no se corrobora** en esta ola. `p17`/`p18` se leen igual para el peso
percibido. Ninguna lectura es causal ni adjudica R7.1.

## Auditoría v2.16

- **Unidad:** persona. **Escala:** proporción.
- **RETROSPECTIVA:** 2015, ola vista (no la más reciente de CSES).
- **¿Incentivo o psicología?** Concurrencia = más en juego (incentivo);
  `p17`/`p18` = percepción. No se separan causalmente.
- **¿Clase media urbana?** Nacional; sin corte urbano/rural en este CALC.
- **HOLDOUT gastado: `M13`** (censo C2: 0 menciones de M13/R7.1 en 140
  archivos, control positivo 66). `holdout_gastado = M13`.
