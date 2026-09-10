# `CALC-R-DIN-M-01-v2` — preregistro mecánico del árbitro R

**Acto:** `GEN2-R-COMPLETA-MARCO`, FP-370, 9/sep/2026. **Celda:** `DIN-M-01`.

Congelado antes de abrir microdato. Mide el estimando ya fijado en
`codificacion-R-v1_1.tsv`, sucesora byte-idéntica de v1.0: payload `ennvih1_2002_hogar_dta`,
tabla `ehh02dta_all/ehh02dta_b3b/iiib_cr.dta`, variable `cr27`, universo `19802 filas del libro 3B (seccion CR) de ENNViH-1 2002; cr27 tiene etiqueta 'TIENE AHORROS' con 2665 en '1', 17074 en '3', 60 en '7' y 3 nulos; sin filtro adicional`,
codificación `y=1 si cr27=='1' (Si); y=0 si=='3' (No); 7 y 8 (no sabe / no responde) fuera`, ponderador `fac_3b@ehh02w_all/ehh02w_b3b.dta[folio+ls]`, estrato
`DISENO-APROXIMADO:CONSTANTE (un solo estrato: el estrato de diseno real -alto/medio/bajo, 14 indicadores de la ENE 2001- NO se publica en el microdato, ver ennvih_diseno/ennvih-1_muestra.pdf p.3; y `ent` no existe en ninguna de las dos tablas que esta fila nombra)` y UPM `DISENO-APROXIMADO:folio (hogar; la UPM real es un conglomerado de viviendas y NO se publica: grep -i upm sobre guiausuariov1.pdf, doc/ehh02cb_bc.pdf y doc/eloc02cb_bcc.pdf da 0 aciertos en los tres)`. Ninguno de esos campos se elige en la corrida.

Salida esperada por nombre, nunca por valor: punto, EE/IC o reserva, n, masa,
exclusiones, estratos y UPM. El medidor no abre L, corpus, M, TRIADA ni R legado.
`cuenta_gen2 = SI` para este `CALC-R-DIN-M-01-v2`; objeto explícito: la medición R de `DIN-M-01`.
