# ENDUTIH-PISOS · cierre descriptivo

Fuente primaria mexicana: ENDUTIH 2023–2025, FD y microdato registrados en
`data/manifiesto.yaml`. Cada ola es un CALC GEN2 nuevo; `data/l6-gobierno-
digital-endutih-v1_0.json` es GEN1 y no fue input. Universo base: persona
elegida de 6+; `FAC_PER`; IC95 por 399 réplicas UPM dentro de `EST_DIS`.
`RESULT-ENDUTIH-PISOS-YYYY-TABLA` vive en `CALC-ENDUTIH-PISOS-YYYY-0001`;
`tabla-principal.tsv` enlaza el RESULT y SHA256 de `resultados.json`.

| Ola | Internet 3 meses, % [IC95] | Celular disponible, % [IC95] | Mensajería entre usuarios, % | Trámite gobierno entre usuarios, % |
| --- | ---: | ---: | ---: | ---: |
| 2023 | 81.18 [80.67, 81.71] | 82.38 [ver RESULT] | 91.37 | 17.75 |
| 2024 | 83.12 [82.66, 83.59] | 83.06 [ver RESULT] | 90.70 | 17.17 |
| 2025 | 86.05 [85.63, 86.54] | 85.55 [ver RESULT] | 89.12 | 20.70 |

Los puntos son proporciones ponderadas 0–1 en RESULT, expresadas arriba en
porcentaje. Para 2024, internet es 88.90% [88.31, 89.44] en localidades de
100 mil+ (`TLOC_1`) y 69.96% [68.75, 71.18] en localidades <2,500
(`TLOC_4`). Entre los 10,840 no usuarios observados de internet en 2024,
9.29% ponderado declaró no tener acceso aunque sabe usarlo, 10.77% falta de
recursos y 16.55% falta de interés/necesidad; son categorías de persona y
no representan los motivos de un hogar. No se suman como partición completa.
La actividad de trámites usa ventana de 12 meses pero el universo condicional
`P7_1=1` usa tres: el estimando está rotulado así y no mide coerción.

**Enmienda de `actividad_empleo` en el mismo PR.** La lectura de cuestionarios
2023/2024/2025 y FD acreditó que `P7_10_2` se aplica únicamente a elegidos
de 15 años o más. Los 5,886/6,019/6,017 blancos observados entre usuarios
de internet son íntegramente de 6–14 años: `SALTO` estructural, no `NR` ni
`NO`; entre usuarios elegibles 15+ no hay blancos. Tres CALC sucesores
`CALC-ENDUTIH-EMPLEO-15MAS-YYYY-0001` corrigen el universo y apartan edades
98/99 no especificadas. `tabla-principal.tsv` enlaza sus RESULT; la nota
`ENDUTIH-EMPLEO-15MAS-cierre.md` deja el cotejo de primeros resultados,
hashes y conteos. Los RESULT originales siguen sellados como evidencia y
sus celdas de empleo dejan de ser producto utilizable.

Cobertura utilizable: 10 medidas originales × 47 dominios × 3 olas = 1,410
celdas, más 1 medida sucesora × 47 × 3 = 141; **1,551 celdas** en total,
1,548 `ESTIMABLE`, 3 `SUPRIMIDA-N-MENOR-100`. Las 141 celdas originales de
empleo no se cuentan dos veces. `n_tabla`: 58,922 / 58,080 / 57,810.
La salida conserva estados SI/NO/SALTO/NR/NS por celda y 399 réplicas
agregadas por medida total, sin registros individuales. Los tres `verify`
devuelven `REPRODUCE`, `CONTEXTO=IDENTICO`; asiento en
`forense/replay-evidencia.tsv`. Estado de calibración
`SIN-HISTORIA-PARA-CALIBRAR`: dos transiciones **sí permiten** separar una
para ajuste y otra para evaluación temporal, pero una sola transición de
ajuste no estabiliza una distribución de errores ni un cuantil extremo para
IC predictivo, y una sola de evaluación no estima cobertura con precisión.
No se anuncia detección de cambios. La formulación contraria del spec
original queda como antecedente sellado; la errata está en el spec sucesor.

Enlace conceptual: ENCIG mide experiencias de trámites con otra unidad y
muestra; ENIF mide productos y fricciones financieras. No se unen como panel
ni se usa la posesión de internet para inferir gobierno digital coercitivo.
Las poblaciones ENDUTIH 6+ y MOCIBA 12+/12–59 son diferentes.

**Auditoría de rigor extremo.** La oferta digital y la estructura territorial
se observan, pero la causa de la brecha rural y la preferencia real no se
identifican con estas proporciones. `P7_2=3` es una respuesta declarada; no
prueba aversión cultural. Los IC son de diseño bajo la aproximación de
bootstrap declarada, no IC predictivos. La medición no incorpora genética ni
atribuciones psicológicas a grupos.
