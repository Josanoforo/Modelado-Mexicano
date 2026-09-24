# ASTRA5-U2 · ENDIREH completo · cierre de medición en rama sucesora

**CAJA · 23/sep/2026 · RETROSPECTIVA · adopción NO.** Encargo original `forense/encargos/2026-09-23-ASTRA5-U2-GENERO-ENDIREH.md`, SHA256 `f99f62f9a7be2a9be86f2591d12c938318b950bb7c6ec228a2b57c2f5d71bf91`. Base de esta rama: `origin/main` `6a2cd6c7`, después del merge de #1093. Worktree sucesor `/home/pc0/mm-astra5-genero-endireh-sucesor-1`; el worktree de #1093 se dejó intacto. Este cierre es de cobertura y medición, no de adopción ni de publicación del registro.

## EJECUTADO

- Se consumieron los nueve CALC finales sellados de #1093 por sus RESULT, matrices, recibo y replay; no se ejecutaron otra vez ni se editaron. Se congelaron seis CALC nuevos antes de abrir filas: 2021 discriminación 8.3 y pareja no física/servicios B/C; 2016 ámbitos restantes y discriminación 7.3; 2011 módulos A/B/C; 2006 módulos MC/MD/MS. Cada primera corrida exitosa quedó en RESULT y sello independientes. El primer intento 2006 0001 falló con `KeyError: decision_gasto` antes de sello; quedó documentado, y 0002 corrigió el acceso a resultados exclusivos de MC sin alterar la spec 0001.
- Se exportaron seis [tablas de consumo](../analisis/dominios/genero/2026-09-23-endireh-matriz-y-pendientes.md): **6,617 celdas**, 6,008 publicables, 609 suprimidas. Cada TSV lleva CALC, RESULT, SHA de `resultados.json`, ventana, corte, n, UPM, punto, IC95, error estándar, masa ponderada, número de réplicas y causa de supresión. Las réplicas agregadas de las celdas publicables permanecen en los RESULT sellados; no se liberan identificadores ni filas. La [matriz detallada](../analisis/dominios/genero/endireh-matriz-conducta-ola-ambito.tsv) enumera 360 dictámenes nacionales medidos, excluidos por diseño o dependientes de una pieza externa.
- El [dictamen 2003](../analisis/dominios/genero/endireh-2003-dictamen-documental.md) verificó la metodología oficial: la muestra sí tiene UPM y estratos, pero los cinco CSV liberados no documentan la asignación por registro. La pieza precisa faltante es llave `LLAVE`→UPM/estrato o pesos replicados equivalentes con factor actualizado. No se abrió fila de 2003 ni se produjo punto sin IC.
- El [ADR raíz](../analisis/dominios/genero/endireh-adr-raiz.md) y [FP/NC](../analisis/dominios/genero/endireh-fp-nc.md) fijan alcance, falsadores, dependencia y estado de publicación. Los contadores derivados del registro pasan de **219 a 225 corridas selladas** y de **65,567 a 65,579 RESULT GEN2 sellados**. `celdas_validadas=219` no cambia.

## LEÍDO Y REPORTADO · contraste limitado de U0

Los siguientes puntos son proporciones de mujeres elegibles con respuesta conocida e IC95 de **diseño dentro de la ola**. Los textos de cada spec fijan los reactivos, códigos y denominadores; cada línea remite a su RESULT y a la tabla indicada arriba. No se interpretan como transiciones ni diferencias causales.

| Componente | Ola · universo/ventana | Punto (IC95) · n | Dictamen frente a U0 |
|---|---|---|---|
| Pareja física A1/A2 | 2021 · relación actual, vida | 15.60% (15.20–15.99), n=68,540 | **CONFIRMA** existencia del subcomponente físico; **sin contraste directo** del agregado U0 70.1%. `RESULT-ENDIREH2021-PF-TABLA` |
| Pareja no física A/B/C | 2021 · relación elegible, vida | 38.27% (37.66–38.80), n=105,216 | **CONFIRMA** existencia de actos no físicos; no se suma al físico ni a otros ámbitos. `RESULT-ENDIREH2021-NF-BC-TABLA` |
| Ayuda B/C tras violencia | 2021 · afectadas B1/B2/C1 con respuesta | 10.10% (9.50–10.69), n=16,526 | **MATIZA** cualquier lectura de denuncia/ayuda como medida del total de violencia; es uso declarado condicionado. Mismo RESULT anterior. |
| Prueba de embarazo para entrar | 2021 · trabajó desde octubre 2016 | 8.13% (7.88–8.41), n=66,363 | **CONFIRMA** el componente medido de discriminación; no equivale a violencia laboral interpersonal 8.9. `RESULT-ENDIREH2021-DIS-TABLA` |
| Perjuicio por embarazo, unión | 2021 · respuesta embarazada 1/2 | 4.34% (3.99–4.68), n=22,594 | El código 3 «no estuvo embarazada» queda fuera; **sin contraste directo** con prevalencia entre todas las trabajadoras. Mismo RESULT. |
| Escolar / comunitaria / familiar | 2016 · vida / vida / desde octubre 2015 | 25.31% / 38.69% / 10.31% (IC separados en tabla) | **CONFIRMA** presencia descriptiva en ámbitos distintos; no es un agregado. `RESULT-ENDIREH2016-REST-TABLA` |
| Prueba de embarazo para entrar | 2016 · trabajó desde octubre 2011 | 11.54% (11.17–11.92), n=55,895 | **CONFIRMA** componente de discriminación 7.3; ventana y muestra distintas de 2021. `RESULT-ENDIREH2016-DIS-TABLA` |
| Pareja, cualquier acto | 2011 A/B/C, vida; 2006 MC/MD/MS, vida | 47.00% (46.46–47.51), n=142,649; 43.25% (42.70–43.73), n=125,145 | Dos pisos de instrumentos propios. **Sin contraste directo** de cambio 2006→2011 ni del 70.1%. `RESULT-ENDIREH2011-MOD-TABLA`, `RESULT-ENDIREH2006-MOD-TABLA` |

El 70.1% de U0 se refiere a una unión de ámbitos y tipos de violencia que no se obtiene sumando proporciones: una mujer puede aparecer en varios ámbitos y los módulos tienen elegibilidades y ventanas distintas. No se calculó aquí la unión oficial por mujer; el juicio sobre ese número es **sin contraste directo**. La baja ayuda/denuncia declarada no identifica violencia no informada ni demuestra que una razón de no acudir sea una elección sin restricciones. Las decisiones sobre gasto y dinero son reparto declarado, no medida causal de autonomía o psicología. Ninguna genética poblacional predice conducta de grupo o persona.

## NO-CORRIDO / RESERVAS

- **NC-ENDIREH-2003-DISENO:** sin tabla 2003 hasta disponer de llave oficial por registro para UPM/estrato o pesos replicados. Los demás ámbitos 2003 se excluyen por el diseño del cuestionario verificado, no por convertir blancos en ceros.
- **NC-ENDIREH-SERIE / U0-701:** sin IC predictivo calibrado, prueba de cambio temporal ni reconstrucción del agregado 70.1%; requiere actos y población homologados y transición independiente, o un CALC nuevo de unión por mujer con definición oficial.
- **NC-ENDIREH-PUBLICACION:** las tablas están **selladas en disco, no registradas**. El canal de publicación y la firma de mesa son operaciones posteriores; un PR sin fusionar no las ejecuta. Ninguna otra reserva ENDIREH explícita bloqueó 2006–2021; ENCO, ENVIPE 2026 y ENOE reservado permanecieron cerrados.

## CONSUMIDO Y PRUEBAS

Corpus y manifiesto por alias/archivo; FD y cuestionarios primarios de 2003, 2006, 2011, 2016 y 2021; especificaciones, nueve CALC, recibo y replay de #1093; contrato U0 GEN-001 solo como afirmación de contraste. Ningún número GEN1 fue origen del producto. Los seis RESULT nuevos están sellados; los `verify` y sus asientos REAL figuran en `forense/replay-evidencia.tsv` y el registro local de cierre. Las pruebas sintéticas nuevas pasan **18/18** con pytest. La línea base `tests/check.py --baseline` y el estado de CI se consignan en el recibo sucesor una vez ejecutados. El paquete se entrega en PR sucesor sin merge.
