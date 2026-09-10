# `CALC-R-DIN-M-01-v3` — sucesor técnico de replay del árbitro R

 **Corrección adversarial PR #680:** sucede al sello `-v2` sin mutarlo. FP-370 conserva su alcance y no se extiende a este identificador técnico. **Celda:** `DIN-M-01`.

Hereda sin cambio los campos y resultados esperados congelados en `-v2`. Se crea después de la medición únicamente para completar la cadena de replay del estimando fijado en
`codificacion-R-v1_2.tsv`, sucesora registral de v1.1 que conserva el estimando y explicita reservas: payload `ennvih1_2002_hogar_dta`,
tabla `ehh02dta_all/ehh02dta_b3b/iiib_cr.dta`, variable `cr27`, universo `19802 filas del libro 3B (seccion CR) de ENNViH-1 2002; cr27 tiene etiqueta 'TIENE AHORROS' con 2665 en '1', 17074 en '3', 60 en '7' y 3 nulos; sin filtro adicional`,
codificación `y=1 si cr27=='1' (Si); y=0 si=='3' (No); 7 y 8 (no sabe / no responde) fuera`, ponderador `fac_3b@ehh02w_all/ehh02w_b3b.dta[folio+ls]`, estrato
`DISENO-APROXIMADO:CONSTANTE (un solo estrato: el estrato de diseno real -alto/medio/bajo, 14 indicadores de la ENE 2001- NO se publica en el microdato, ver ennvih_diseno/ennvih-1_muestra.pdf p.3; y `ent` no existe en ninguna de las dos tablas que esta fila nombra)` y UPM `DISENO-APROXIMADO:folio (hogar; la UPM real es un conglomerado de viviendas y NO se publica: grep -i upm sobre guiausuariov1.pdf, doc/ehh02cb_bc.pdf y doc/eloc02cb_bcc.pdf da 0 aciertos en los tres)`. Ninguno de esos campos se elige en la corrida.

El punto ponderado descriptivo queda separado del EE/IC bajo DISENO APROXIMADO, NO AUTORIZADO COMO GROUND TRUTH INFERENCIAL DE TRIADA SIN FIRMA DE MESA (FP-371 ABIERTA). Salida esperada por nombre, nunca por valor: punto, EE/IC con esa reserva, n, masa,
exclusiones, estratos y UPM. El medidor no abre L, corpus, M, TRIADA ni R legado.
Este sucesor técnico no añade una medición: hereda el conteo único de la cadena desde `CALC-R-DIN-M-01-v2`, cuyo objeto firmado es la medición R de `DIN-M-01`.
