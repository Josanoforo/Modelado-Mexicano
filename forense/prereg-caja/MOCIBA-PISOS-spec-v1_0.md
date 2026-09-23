# MOCIBA-PISOS · especificación humana v1.0 · ASTRA5 U4

**El primer resultado que produzca este procedimiento es el que se reporta.**
Las olas elegibles aquí son 2015, 2016 y 2017, cada una en su CALC
`CALC-MOCIBA-PISOS-YYYY-0001`. La lectura de los FD y cuestionarios se hizo
antes de congelar, sin abrir la BD. `cuenta_gen2: SI`, `adopta: NO` y
`RETROSPECTIVA`. Los resultados son tres cortes separados, no una serie
homogénea ni un enlace de predicción F6.

## Identidad y universo por ola

| Ola | Anfitrión y universo | Ventana de acoso | Archivo y diseño |
| --- | --- | --- | --- |
| 2015 | ENDUTIH 2015, informante elegido 12+ usuario de internet o celular; 32 entidades | últimos 12 meses | `tciberacoso.dbf`, `FAC_MOCIBA`, `UPM`; el FD no documenta `EST_DIS` y no se construye IC de diseño |
| 2016 | ENDUTIH 2016, informante elegido 12+ usuario de internet o celular en tres meses previos | últimos 12 meses | `MOD_2016_CIBERACOSO.DBF`, `FAC_MOCIBA`, `EST_DIS`, `UPM_DIS`, `ENT` |
| 2017 | submuestra ENDUTIH 2017, informante elegido 12–59 usuario de internet en tres meses previos; 32 entidades | junio 2016 a entrevista 2017 | `mod_2017_ciberacoso.dbf`, `FAC_MOCIBA`, `EST_DIS`, `UPM_DIS`, `ENT` |

Fuentes primarias: FD de cada ola, ids de manifiesto en el `spec.yaml`; [portal
2015](https://www.inegi.org.mx/programas/mociba/2015/), [portal
2016](https://www.inegi.org.mx/programas/mociba/2016/), [portal
2017](https://www.inegi.org.mx/programas/mociba/2017/), y cuestionarios
[2015](https://www.inegi.org.mx/contenidos/programas/mociba/2015/doc/mociba2015_cuestionario.pdf),
[2016](https://www.inegi.org.mx/contenidos/programas/mociba/2016/doc/mociba2016_cuestionario.pdf),
[2017](https://www.inegi.org.mx/contenidos/programas/mociba/2017/doc/mociba2017_cuestionario.pdf).
En las tres olas la BD MOCIBA contiene al informante elegido, no a toda la
población. La prevalencia de acoso tiene denominador de personas elegidas
usuarias de la tecnología pertinente y que responden sí/no a toda la batería.
No se rotula como prevalencia sobre la población mexicana total.

## Reactivos y códigos congelados

| Ola | Ciberacoso: batería 1/2/9 | Bloqueo tras acoso: matriz 1/2/blanco | Comunicación a autoridad / servicio: matriz 1/2/blanco |
| --- | --- | --- | --- |
| 2015 | `P3_1..P3_10`: «En los últimos doce meses ... ¿a usted ...?» | `P7_i_1`: «Bloquear a la persona» por situación `P3_i=1` | `P7_i_5`: «Denunciar ante alguna autoridad» por situación `P3_i=1` |
| 2016 | `P1_1..P1_10`: «En los últimos doce meses ... ¿ha vivido ...?» | `P7_i_1`: «Bloquear a la persona» por situación `P1_i=1` | `P7_i_6A`: «Denunciar o informar ante Policía u otras autoridades» por situación `P1_i=1` |
| 2017 | `P4_01..P4_10`: «De junio de 2016 a la fecha ... ¿alguien ...?» | `P10_1`: «Bloquear (a la persona, cuenta o página)» | `P10_5`: «Denunciar ante el ministerio, policía o el proveedor del servicio»; **incluye proveedor, no es tasa pura ante autoridad** |

En la batería de exposición, cualquier `1` → víctima; todos `2` → no
víctima; sólo `2/9` con al menos un `9` → `NS`; resto → `NR`.
Para 2015/2016, sólo las situaciones con exposición `1` abren `P7_i_*`.
Cualquier respuesta `1` entre esas situaciones → sí; todas `2` → no;
blanco/incompleta sin sí → `NR`. Para 2017, una víctima abre `P10`; se lee
`P10_1` y `P10_5` por separado con `1` sí, `2` no, blanco `NR`. Fuera del
universo de P7/P10 es `SALTO`. Son matrices de respuesta múltiple, así que
bloquear y denunciar pueden coexistir. «No responder» como acción elegida
en el cuestionario no equivale a no respuesta al cuestionario.

Filtro base: `EDAD` 12–97 en 2015/2016, 12–59 en 2017;
`FAC_MOCIBA>0` finito; en 2016/2017 `EST_DIS` y `UPM_DIS` no vacíos.
`EDAD=98` (no especificada) queda excluida. No se imputan respuestas.

## Salida y precisión

Cada ola produce una tabla JSON con 3 medidas (`ciberacoso`, `bloqueo`,
`denuncia`) × ejes univariados disponibles: total, sexo, edad 12–17/18–29/
30–59/60+ (60+ sólo 2015/2016), escolaridad `NIVEL` 00–02/03–05/06–11,
entidad 01–32 sólo 2016/2017. Localidad no consta en estos FD y no se
infiere de UPM. La celda con menos de 100 respuestas sí/no queda
`SUPRIMIDA-N-MENOR-100` antes de punto e IC.

Punto: razón de sumas de `FAC_MOCIBA` entre respuestas válidas. En 2016/2017,
IC95 percentil a partir de 399 réplicas de UPM con reemplazo dentro de cada
`EST_DIS`, semilla `20260923`/`numpy.PCG64`, la misma matriz para todas las
celdas de la ola. Singleton se trata como certeza. Menos de 380 réplicas con
denominador positivo → `NO-ESTIMABLE-REPLICAS`. Se conserva la réplica agregada
de cada total. En 2015, el FD no documenta estrato: estado
`NO-ESTIMABLE-SIN-EST_DIS` por celda, sin punto ni IC; se conservan `n` y
estados de respuesta. No se inventa estrato con una codificación de UPM.

Entre MOCIBA y ENDUTIH hay anfitrión común en varias olas; no se tratan como
dos muestras independientes. El cambio de población en 2017 y las distintas
redacciones/respuestas impiden calibrar una serie con estos tres puntos.
Estado `SIN-HISTORIA-PARA-CALIBRAR`. No se comparan directamente tasas 12+
con la población ENDUTIH 6+, ni se deriva conducta grupal de genética.

## Reservas y producto

El contrato documental previo de P12 en 2021/2022 se cita como antecedente,
pero sus respuestas continúan reservadas para F6; 2019/2020/2025 están
nombradas reserva confirmatoria en `F5-panel-candidatos-v1_3.tsv`.
2023/2024 tienen exposición previa en el marco piloto, pero este acto no
interpreta esa exposición como autorización para abrir microdatos nuevos.
Esas seis olas se declaran fuera de la corrida real. La misión descriptiva
no rehabilita el enlace predictivo descartado.
