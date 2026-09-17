# Spec fijada · WBES México 2023, solicitudes o expectativas de pagos informales

Estado: `FIJADA-ANTES-DE-ABRIR-RESPONDENTES`. Producto descriptivo para la sección TRA admitida por F-19. No transfiere parámetros de personas a establecimientos, no calibra el motor, no abre F6 y no se combina numéricamente con ENCIG o ENCRIGE.

## Pregunta consumidora y título del estimando

> Entre los establecimientos WBES 2023 que tuvieron al menos una de seis interacciones documentadas con gobierno, ¿qué proporción ponderada reportó que se esperaba o solicitó un regalo o pago informal, y cuánto cambia por tamaño WBES?

El título dice **solicitud o expectativa**, no pago realizado. Los seis reactivos preguntan si un regalo o pago informal fue “expected or requested”; no acreditan que el establecimiento lo haya entregado.

## Unidad, universo, cobertura y periodo

La unidad es el **establecimiento**. El universo de inferencia documentado comprende negocios formales del sector privado en México, con al menos 1% de propiedad privada, registrados ante la autoridad pertinente y con cinco o más empleados. Incluye manufacturas ISIC Rev. 4 10–33 y servicios 41–43, 45–47, 49–53, 55–56, 58, 61–62, 69–75, 79 y 95; excluye cooperativas y colectivos. La cobertura geográfica es nacional. Localizador: *Mexico 2023 ES Implementation Report*, §§II.1–II.2 y Fact Sheet (p. 8); DDI XML, `stdyInfo/method/dataColl`.

El levantamiento ocurrió entre marzo y octubre de 2023, pero el desenlace no tiene una sola ventana anual:

- conexión eléctrica, conexión de agua, permiso de construcción, licencia de importación y licencia de operación: **últimos dos años**;
- visitas, inspecciones o reuniones con funcionarios fiscales: **último año**.

El compuesto se rotula “durante la ventana propia de cada interacción”; no se reinterpreta como año calendario 2023. Localizador: cuestionario B-READY 2023, C.3/C.5 (p. 6), C.12/C.14 (p. 7), G.2/G.4 (p. 30), J.3/J.5 (pp. 41–42), J.10/J.12 y J.13/J.15 (pp. 45–46).

## Batería fijada y elegibilidad

| Interacción | Filtro de interacción | Evento | Ventana |
|---|---|---|---|
| Conexión eléctrica | `c3 == 1` | `c5` | últimos dos años |
| Conexión de agua | `c12 == 1` | `c14` | últimos dos años |
| Permiso de construcción | `g2 == 1` | `g4` | últimos dos años |
| Inspección/reunión fiscal | `j3 == 1` | `j5` | último año |
| Licencia de importación | `j10 == 1` | `j12` | últimos dos años |
| Licencia de operación | `j13 == 1` | `j15` | últimos dos años |

El cuestionario y el DDI acreditan cada par, sus saltos y sus códigos, pero los cuatro objetos autorizados no contienen la ficha que define el agregado oficial ni una regla oficial para casos parcialmente observados. El Implementation Report sólo enlaza externamente a `Indicator-Description.pdf`, objeto que no se adquirirá en este acto. Por ello:

1. se publican seis tasas separadas, una por interacción inequívocamente documentada;
2. el primario es un **compuesto descriptivo propio** de esas seis interacciones, no una réplica certificada del indicador oficial de incidencia de soborno.

Un establecimiento está expuesto al compuesto si al menos un filtro de interacción vale `1`. Todos los filtros en `2` significan “sin interacción” y quedan fuera; si ninguno vale `1` y al menos uno está vacío o tiene código especial, la elegibilidad queda `DESCONOCIDA` y se publica aparte. La ausencia de interacción nunca se convierte en cero del desenlace.

## Evento, faltantes y denominadores

En cada evento: `1 = sí`, `2 = no`, `-8 = rechazo`, `-9 = no sabe`; vacío significa que el reactivo no fue formulado por salto o inaplicabilidad. Para el compuesto propio:

- `sí`: al menos un evento aplicable vale `1`, incluso si otra interacción aplicable falta;
- `no`: todos los eventos aplicables observados valen `2`;
- `desconocido`: no hay ningún `1` y al menos un evento aplicable está vacío, en `-8`, `-9` o en otro valor no válido.

El punto descriptivo de respuesta observada es `peso(sí) / [peso(sí) + peso(no)]`. No se imputa el desconocido. Se publican además:

- masa desconocida entre expuestos: `peso(desconocido) / peso(expuestos)`;
- límite inferior lógico: `peso(sí) / peso(expuestos)`;
- límite superior lógico: `[peso(sí) + peso(desconocido)] / peso(expuestos)`.

Los límites no son intervalos de confianza. La misma regla se aplica por separado a cada interacción. Si el denominador es cero, el valor queda vacío con estado `DENOMINADOR-VACIO`.

## Ponderación, dominios y precisión

Ponderador principal: `wmedian`, peso por supuesto mediano de elegibilidad. La elección se fijó porque el Implementation Report §III.6 dice que todos los indicadores y análisis del equipo Enterprise Surveys usan los pesos de supuesto mediano. No se promedian `wstrict`, `wmedian` y `wweak` ni se elige por cercanía a una cifra publicada.

Dominios preespecificados: total nacional cubierto y `a6a`, tamaño oficial de muestreo WBES: pequeña (5–19), mediana (20–99), grande (100–250), extra grande (251 o más). No se importan cortes ENCRIGE. Localizador: Implementation Report §II.1 y Fact Sheet; DDI `a6a`.

La documentación acredita muestreo aleatorio estratificado y aporta `strata` y pesos; también advierte que los pesos de panel pueden variar dentro de estrato. Los insumos no incluyen una variable separada de UPM, factores de corrección finita por estrato ni un tratamiento documentado de estratos singulares para esta estimación de dominio. Para no fabricar precisión, se publican puntos y límites por faltantes con `IC-DE-DISEÑO-NO-ESTIMABLE-CON-INSUMOS-DISPONIBLES`. No se usa IC binomial ni bootstrap iid.

## Integridad, salida y límites de uso

Los cuatro objetos se verifican contra los SHA-256 del manifiesto antes de medir. El ZIP de microdato debe contener exactamente `Mexico-2023-full-data.dta`; `idstd` debe ser único; las variables fijadas deben existir; `wmedian` debe ser finito y positivo; `a6a` sólo puede tomar 1–4. Se calcula una razón de totales ponderados. Un establecimiento se cuenta una sola vez en el compuesto aunque tenga varias interacciones positivas.

La salida agregada publica por indicador y dominio: `n` real entrevistado/expuesto/clasificado/sí/no/desconocido, sumas de pesos, numerador, denominadores, masa desconocida, punto y límites. No publica registros ni identificadores individuales.

Conclusiones permitidas: magnitudes descriptivas y diferencias puntuales dentro del universo WBES cubierto. No permite causalidad, generalización a negocios informales, menores de cinco empleados o sectores excluidos, afirmar pago efectivamente realizado, comparar numéricamente con ENCIG/ENCRIGE, validar el motor ni afirmar diferencias por tamaño como estadísticamente distintas sin varianza de diseño estimable.

## Exposición previa al congelamiento

Al localizar variables se imprimieron accidentalmente frecuencias y cantidades de casos del DDI antes de fijar esta especificación. También se leyó la tabla de muestra lograda del Implementation Report. La composición, códigos, ponderador, dominios y regla de faltantes se fijaron por el texto del instrumento y la metodología, no para acercarse a esas frecuencias. Esta es una descripción no ciega; no se consultó el microdato de respondentes antes de este congelamiento.
