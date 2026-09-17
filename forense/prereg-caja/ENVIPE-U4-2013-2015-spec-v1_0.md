# ENVIPE U4 2013/2015 · especificación prospectiva v1.0

**Acto:** `GEN2-ENVIPE-U4-2013-2015-1` · **estado al congelar:** medidor probado
sólo con fixtures sintéticos; ningún registro de los DBF fue abierto. La sesión
conoce los puntos históricos públicos U1/R por delito y U4 de 2012/2025. No es
un ejercicio ciego y ningún valor previo selecciona filtros, unión o ponderador.

## Fuentes documentales e identidad

Se verificaron los cuatro bytes usados contra el manifiesto. ENVIPE 2013 es la
ola levantada en 2013 sobre victimización de 2012; ENVIPE 2015, la ola levantada
en 2015 sobre victimización de 2014.

| ola | módulo de delitos | tabla persona | identidad y vínculo acreditados | diseño de persona |
|---|---|---|---|---|
| 2013 | `tmod_vic.dbf` | `tper_vic.dbf` | `(CONTROL,VIV_SEL,HOGAR,R_SEL)`; FD 2013, hojas `TMod_Vic` filas 19–47 y `TPer_Vic` filas 19–30 | `EST`,`UPM`; `FAC_ELE` en `TPer_Vic` fila 1047 y diseño filas 1053–1055 |
| 2015 | `TMod_Vic.dbf` | `TPer_Vic2.dbf` | unión `(UPM,VIV_SEL,HOGAR,R_SEL)`; `ID_PER` identifica la persona en `TPer_Vic2`; FD 2015 pp. 5, 7–8 y 32 | `EST_DIS`,`UPM_DIS`; `FAC_ELE` y diseño pp. 49–50 |

Las cabeceras DBF, leídas como metadato antes de congelar, confirman esos
miembros, campos y tipos. En 2015 `UPM` (llave de vínculo, longitud 7) no se
sustituye por `UPM_DIS` (UPM de diseño, longitud 5). `EST` de 2013 y `EST_DIS`
de 2015 son los campos documentados de diseño; `EST_SOC`/`ESTRATO` no entran a
esta ruta. No se necesita `TSDem` para ninguna ola.

## Universo, partición y punto

`U1` contiene filas de delito personal con `BPCOD` 05–15, `BP1_20=2`, razón
`BP1_23` válida 01–08 y `FAC_DEL` finito positivo. Los catálogos y etiquetas de
las dos olas son iguales: C1={01,02,06}, C2={01,02,06,08}; código 08 significa
actitud hostil de la autoridad. La razón, no el tipo de delito, define el
desenlace. Los códigos 09, 99, blancos y otros quedan fuera, no se vuelven cero.

`U4` es una fila por persona seleccionada con al menos un evento U1, vínculo
uno-a-uno a la tabla de personas, identidad válida y `FAC_ELE` finito positivo.
Una persona con varios eventos cuenta una vez y su desenlace es el máximo. Una
llave ausente, vínculo cero/múltiple, identidad ambigua o peso inválido se
excluye y cuenta por motivo. `FAC_DEL` sólo guarda la elegibilidad heredada del
evento; el punto persona es razón de sumas `FAC_ELE`.

Se emiten `p(C2,U4)`, `q=1-p` en el mismo universo, `p(C1,U4)`, n personas,
eventos de origen y enlazados, numeradores y denominador ponderados, embudo de
exclusiones y cobertura. `q` no representa código 09 ni personas fuera de U4.

## Precisión congelada antes del resultado

Para la sensibilidad de dominio se conserva toda fila de la tabla oficial de
personas que tenga identidad única, `FAC_ELE`, estrato y UPM válidos. Fuera de
U4 aporta cero a numerador y denominador; no se restringe el marco al desenlace.
Se remuestrean UPM con reemplazo dentro de estrato, manteniendo el número de UPM,
2 000 réplicas `numpy.PCG64`, semilla `20260909`, percentiles 2.5/97.5. Un
estrato observado con una UPM queda fijo en las réplicas. No se colapsan ni se
inventan estratos.

Este intervalo se etiqueta
`SENSIBILIDAD-...-MARCO-PERSONAS-OBSERVADO;...;NO-APROBADA-INFERENCIA`:
la pareja física y el ponderador están documentados, pero no hay política
oficial acreditada para estratos singulares ni roster completo de UPM
seleccionadas. `NC-0159` impide llamarlo IC plenamente inferencial. Tampoco se
llama límite inferior. El intervalo de q se obtiene como `[1-U,1-L]`.

## Guardas y alcance

- Miembro o columna ausente, llave indocumentada o U4 vacío: la ola se detiene.
- Se detectan colisiones de `ID_PER` (2015), llaves duplicadas y pérdida de join.
- No se calcula diferencia entre olas ni se combinan intervalos.
- Son puntos descriptivos, no efectos causales, cohorte, calibración de θ,
  persistencia nueva ni actualización de RES-0027/0028.
- `AP5_*` y `EST_SOC` quedan fuera porque no participan en identidad, universo,
  punto o diseño de esta medición.

El primer resultado producido por esta especificación es el que se publica.
