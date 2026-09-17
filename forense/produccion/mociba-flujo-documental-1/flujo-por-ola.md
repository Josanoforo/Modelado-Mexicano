# Flujo documental de P12_5 · MOCIBA 2021/2022

Estado: **definición resuelta; cero respuestas reales abiertas**. La regla de
entrada es igual en las dos olas, pero se acredita por separado y no se infiere
por igualdad de nombres.

## Evidencia adquirida

| ola | original oficial | bytes | SHA-256 | verificación |
| --- | --- | ---: | --- | --- |
| 2021 | `mociba2021_cuestionario.pdf` | 847,961 | `2ffadcc44db5c6e965c8dd6e767a234e94f3e42a0967cedc24e4c52d50b5622d` | PDF 1.6, 7 pp.; texto extraíble; pp. 5-6 verificadas visualmente |
| 2022 | `mociba2022_cuestionario.pdf` | 1,044,877 | `a37f17509ec028a412d6db75e61e17daeaf51bc221665c3de4e73591b03bc219` | PDF 1.6, 7 pp.; texto extraíble; pp. 5-6 verificadas visualmente |

URLs oficiales: `https://www.inegi.org.mx/contenidos/programas/mociba/2021/doc/mociba2021_cuestionario.pdf`
y `https://www.inegi.org.mx/contenidos/programas/mociba/2022/doc/mociba2022_cuestionario.pdf`.
Descarga válida el 16/sep/2026. El primer intento en CAJA falló por DNS; el
reintento autorizado fuera del sandbox devolvió ambos PDF completos. No se
abrieron resultados, tabulados, notas de prensa ni microdatos.

## Tabla de decisión documental

| condición | MOCIBA 2021 | MOCIBA 2022 | decisión ejecutable |
| --- | --- | --- | --- |
| Población base | Persona elegida de 12 y más años que use Internet; cuestionario p. 1. `EDAD` y `P7_1` en FD, filas 2578–2582 y 2597–2598. | Persona elegida de 12 o más años que use internet; cuestionario p. 1. `EDAD` y `P7_1` en FD, filas 2812–2814 y 2830–2831. | `EDAD>=12` y `P7_1=1`; falta/edad no especificada produce `INDETERMINADO`. |
| Ventana P4 | Agosto de 2020 a la fecha; cuestionario pp. 2–5 y FD `TMOCIBA`. | Julio de 2021 a la fecha; cuestionario pp. 2–5 y FD `TMociba`. | No se intercambian ventanas entre olas. |
| Entrada a P12 | P4 indica: si registra 2 o 9 en **todas** las opciones, pase a 13; pp. 2–5. | P4 indica: si registra 2 o 9 en **todos** los renglones, pase a 13; pp. 2–5. | Al menos un `P4_01..P4_13=1` abre P5–P12. Todos `2/9` saltan P12. Sin un sí y con batería incompleta/código inválido: `INDETERMINADO`. |
| Desenlace | P12 p. 6: opción 05 «Denunciar ante el Ministerio Público o policía», hasta tres códigos. FD fila 2503: `P12_5`, `1=Sí`, `2=No`. | Mismo texto y modalidad, p. 6. FD filas 2728–2730: `1=Sí`, `2=No`, `b=blanco`. | `1` evento; `2` no-evento. `P12_99=1` es no sabe/no responde. No se inventa 9/99 dentro de `P12_5`. |
| Blanco/salto | El FD no documenta blanco para `P12_5`. | El FD documenta `b=blanco`. | Dentro del universo, ausencia/blanco es no respuesta; fuera, salto estructural. Ninguno equivale a `2`. |
| Unidad/peso/diseño | Persona seleccionada; `FACTOR`, `UPM_DIS`, `EST_DIS`, FD filas 2531 y 2542–2543. | Persona seleccionada; mismos campos, FD filas 2765 y 2776–2777. | Se acredita la existencia/etiqueta de campos, no un estimador de varianza completo. |

Hashes FD: 2021 `375bf7c1bcdbcc9b0716cd3b63fe940906a97783a3b69f2afad35f35950b1e25`;
2022 `923fa85a665219200d6c87d1f5af25090870bf91957d16f1008726e78edc396e`.

## Universo y respuesta válida

El universo total de P12 son las personas que pasan las compuertas base y
tienen por lo menos un `1` en P4. Ese conteo conserva a quienes no contestaron
P12_5. El estimando descriptivo computable por este contrato usa como
denominador sólo elegibles con `P12_5` válido (`1/2`) y sin `P12_99=1`, y debe
nombrarse «proporción entre respondentes válidos» junto con elegibles totales y
no respuesta. No se presenta como tasa sobre todos los elegibles. Una persona
fuera del universo nunca se convierte en «no denunció».

## Diferencias y límite material

La ruta P4→P12 coincide documentalmente. Cambian la ventana y la documentación
del blanco: sólo el FD 2022 incluye `b`. Resolver el filtro no vuelve elegible a
M: `civico.denuncia.miedo_desconfianza` mide una razón entre no denunciantes de
delitos y no produce la denuncia total de ciberacoso. Firma, llamadas, L y R
siguen cerrados.
