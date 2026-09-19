# Lectura ISSP México 2017 · primera fuente para pedir prestada una gran suma

## Resultado

**Ficha exacta.** Variable integrada: `v26`; etiqueta acreditada de la pregunta: “Q8a Whom or where to ask for help: borrow large sum of money?”; ponderador: `WEIGHT`, documentado como `WEIGHT=1 (No weighting)` para México. Universo elegible: personas de 18 años o más de la muestra nacional mexicana. Códigos sustantivos y denominador común de la distribución: `v26=1..7`; `8=No puedo elegir` y `9`/vacío=`No respuesta` se informan como faltantes separados y no entran al denominador válido.

Entre las 983 respuestas válidas de 1,002 personas adultas de la muestra mexicana, la primera opción mencionada fue **familiares o amigos cercanos (49.95%)**. Le siguieron compañías privadas (16.79%), otras personas (13.73%), servicios públicos (8.44%), otras organizaciones (5.09%), ninguna persona u organización (3.97%) y organizaciones sin fines de lucro o religiosas (2.03%). `WEIGHT` vale 1 para los casos mexicanos, de modo que masas ponderadas y conteos coinciden; el cálculo conserva, no supone, esa propiedad.

| Respuesta Q8a | Total (%) | Hombres (%) | Mujeres (%) |
|---|---:|---:|---:|
| Familiares o amigos cercanos | 49.95 | 49.16 | 50.69 |
| Otras personas | 13.73 | 15.06 | 12.48 |
| Compañías privadas | 16.79 | 17.15 | 16.44 |
| Servicios públicos | 8.44 | 8.16 | 8.71 |
| Organizaciones sin fines de lucro o religiosas | 2.03 | 1.67 | 2.38 |
| Otras organizaciones | 5.09 | 5.23 | 4.95 |
| Ninguna persona u organización | 3.97 | 3.56 | 4.36 |

Las mujeres mencionaron familiares o amigos cercanos en 50.69% de las respuestas válidas y los hombres en 49.16%. El contraste descriptivo mujeres menos hombres es **+1.53 puntos porcentuales**. No hay EE ni IC porque no se acreditaron UPM y estrato ejecutables; por tanto, la diferencia no demuestra una separación poblacional ni un efecto de género.

La vista publicable completa está en `tabla-descriptiva-apoyo-monetario-total-sexo.csv`: conserva las siete categorías en los tres dominios e incluye n elegible, faltantes, n y masa del denominador válido y n/masa por categoría. Su comprobador exige que mujeres y hombres del contraste reutilicen exactamente el código 1, la categoría y los denominadores de la distribución. Los puntos de la tabla son **porcentajes**; la resta mujeres−hombres está expresada en **puntos porcentuales**, no como cambio porcentual relativo.

## Cobertura y denominadores

| Dominio | Elegibles n/masa | Válidos n/masa | No puede elegir n/masa | No respuesta n/masa | Peso inválido n | Cobertura válida |
|---|---:|---:|---:|---:|---:|---:|
| Total México | 1,002 / 1,002 | 983 / 983 | 18 / 18 | 1 / 1 | 0 | 98.10% |
| Hombres | 487 / 487 | 478 / 478 | 9 / 9 | 0 / 0 | 0 | 98.15% |
| Mujeres | 515 / 515 | 505 / 505 | 9 / 9 | 1 / 1 | 0 | 98.06% |

No hubo sexo no clasificable ni pesos inválidos. La reconstrucción total desde hombres, mujeres y el dominio residual coincide tanto en n como en masa. En cada dominio las siete proporciones suman uno dentro del denominador válido.

## Lectura y límites

El resultado describe una intención hipotética: a quién o dónde acudiría primero la persona si necesitara pedir prestada una suma grande. La categoría dominante combina familiares y amigos y no permite separar esos vínculos. Es una red o fuente de apoyo declarada ante ese supuesto: no mide una propensión general al ahorro informal, recepción efectiva de dinero, que el préstamo estuviera disponible, causalidad, ni el mismo patrón en México en otra fecha.

El informe integrado oficial GESIS de ZA6980 v2.0.0 acredita `v26/Q8a` y los códigos 1–9. Su tabla histórica para México contiene los mismos conteos totales y denominador válido; la igualdad se comprobó sólo como reconciliación posterior. El producto nuevo es la ejecución preespecificada y sellada, con dominios por sexo, cobertura, contraste y controles; no se presenta la tabla histórica como una medición GEN2 nueva. La adquisición del codebook, indispensable para resolver la correspondencia, también hacía visibles esos tabulados; por eso la operación permanece expresamente no ciega y ninguna regla se eligió por cercanía a esas cifras.

## Precisión

El documento mexicano de variables de contexto acredita `WEIGHT=1 No weighting` y marca que no hubo ajuste por probabilidades desiguales ni por no respuesta. Ni ese documento ni el contenedor integrado aportan identificadores ejecutables de UPM/estrato para México. Se publican puntos con `EE-IC-NO-DISPONIBLES-DISENO-NO-ACREDITADO`; no se fabrican intervalos iid, Kish o bootstrap.
