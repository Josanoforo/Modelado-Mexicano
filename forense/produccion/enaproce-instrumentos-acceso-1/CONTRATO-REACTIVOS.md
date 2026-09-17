# Contrato documental ENAPROCE 2015/2018

## Convenciones comunes

- **Nombres de variable:** el prefijo local `ENAPROCE-` evita confundir los
  códigos del cuestionario con rótulos internos del repositorio; el sufijo
  después del guion es el nombre oficial exacto en RNM.
- **Unidad:** empresa, que puede reunir uno o más establecimientos bajo una
  razón social. No es persona ni establecimiento aislado.
- **Sectores:** manufacturas, comercio y los servicios privados no financieros
  SCIAN 48-49, 54, 56, 71, 72 y 81. En PyME hay cuestionarios sectoriales de
  manufactura y de comercio/servicios; el módulo XII aquí estudiado es igual en
  ambos.
- **Tamaño:** la estratificación oficial por personal ocupado es micro `0–10`
  en los tres sectores; pequeña `11–30` en comercio y `11–50` en servicios e
  industria; mediana `31–100` en comercio, `51–100` en servicios y `51–250`
  en industria. Los cuestionarios PyME también fueron usados para empresas
  grandes, pero R03 se restringe a pequeñas y medianas. Una eventual salida
  debe filtrar por tamaño y excluir grandes; en 2018 su muestra fue declarada
  no representativa y `FAC_EXPA=1`.
- **Exposición/filtro:** ninguno de los reactivos de esta tabla exige haber
  realizado un trámite, recibido una inspección o sufrido una solicitud. Se
  pregunta al universo del instrumento; el trámite-obstáculo admite `Ninguno`.
  Blanco no debe recodificarse como cero ni como `Ninguno`.
- **Faltantes:** los cuestionarios y diccionarios revisados no documentan código
  de no sabe, rechazo o salto para los campos de carga. La ausencia debe
  conservarse como faltante hasta obtener el descriptor del archivo real.
- **Diseño:** las cuatro tablas documentan `FAC_EXPA`. RNM describe el diseño,
  pero sus diccionarios no identifican una variable ejecutable de estrato/UPM;
  esa pieza sigue faltando para errores estándar de diseño.

## 2015 · Microempresas · tabla RNM F20

Población: microempresas (0–10 personas) que realizaron actividades económicas
en 2014; cobertura nacional y por cuatro regiones. Diseño probabilístico,
estratificado y por conglomerados (municipio), con selección en dos etapas.
Muestra de diseño micro: 10,384; muestra definitiva informada por RNM: 9,103.

| Variable | Texto/escala y código | Periodo | Página | Correspondencia con R03 |
|---|---|---|---|---|
| [`ENAPROCE-M61`](https://www.inegi.org.mx/rnm/index.php/catalog/330/variable/F20/V2494) | Principal problema para crecer; selección única. `6 = Exceso de trámites gubernamentales`; `15 = No tiene problemas`. | Situación declarada en encuesta; actividad 2014 | Cuestionario micro, p. 27 | **Proxy limitado:** percepción/obstáculo, no exposición ni corrupción. |
| [`ENAPROCE-M62`](https://www.inegi.org.mx/rnm/index.php/catalog/330/variable/F20/V2495) | Principal trámite al que dedica más tiempo y recursos y considera obstáculo. Códigos `1–8, 11, 12`; `13 = Ninguno`. | Situación declarada; actividad 2014 | p. 27; definiciones pp. 26 y 28 | **Proxy limitado:** tipo de obstáculo; no mide tiempo, monto ni pago informal por categoría. |
| [`ENAPROCE-M63`](https://www.inegi.org.mx/rnm/index.php/catalog/330/variable/F20/V2496) | Pesos en un mes normal para cumplir obligaciones fiscales federales. Incluye contador, papelería y servicios; excluye impuestos. | Mes normal de 2014 | p. 27 | **Directa sólo para costo formal de cumplimiento fiscal**; no es pago informal. |
| [`ENAPROCE-M64`](https://www.inegi.org.mx/rnm/index.php/catalog/330/variable/F20/V2497) | Horas aproximadas en un mes normal para trámites gubernamentales distintos del pago de impuestos. | Mes normal de 2014 | p. 29 | **Directa para carga temporal**; no identifica trámite, exposición ni corrupción. |

## 2015 · Pequeñas/medianas · tabla RNM F19

Población: pequeñas y medianas empresas activas en 2014; cobertura nacional por
sector/tamaño y entidad × sector estratégico. Diseño probabilístico y
estratificado. RNM informa muestra de diseño PyME de 16,613; la tabla de
distribución del catálogo tiene una inconsistencia tipográfica interna en el
subtotal pequeña, por lo que no se usa ese subtotal. Muestras definitivas
informadas: 10,701 pequeñas y 3,921 medianas. El instrumento también se aplicó
a grandes, que quedan fuera del contrato R03.

| Variable | Texto/escala y código | Periodo | Página | Correspondencia con R03 |
|---|---|---|---|---|
| [`P79`](https://www.inegi.org.mx/rnm/index.php/catalog/330/variable/F19/V2257?name=P79) | Principal problema para crecer; selección única. `6 = Exceso de trámites gubernamentales`; `16 = No tiene problemas`. | Situación declarada; actividad 2014 | Ambos cuestionarios PyME, p. 35 | **Proxy limitado:** percepción/obstáculo. |
| [`P80`](https://www.inegi.org.mx/rnm/index.php/catalog/330/variable/F19/V2258?name=P80) | Principal trámite al que dedica más tiempo y recursos y considera obstáculo. `1–8, 11, 12`; `13 = Ninguno`. | Situación declarada; actividad 2014 | p. 37; definiciones p. 36 | **Proxy limitado:** tipo de obstáculo. |
| [`P81`](https://www.inegi.org.mx/rnm/index.php/catalog/330/variable/F19/V2259?name=P81) | Pesos en un mes normal de cumplimiento fiscal federal; incluye servicios de cumplimiento y excluye impuestos. | Mes normal de 2014 | p. 37 | **Directa para costo formal**, no pago informal. |
| [`P82`](https://www.inegi.org.mx/rnm/index.php/catalog/330/variable/F19/V2260?name=P82) | Horas aproximadas en un mes normal para trámites gubernamentales distintos del pago de impuestos. | Mes normal de 2014 | p. 37 | **Directa para carga temporal**, no corrupción. |

## 2018 · Microempresas · tabla RNM F1

Población: microempresas del marco MENUE/RENEM actualizado al tercer trimestre
de 2017; cobertura nacional por sector/tamaño. Diseño probabilístico y
estratificado. Muestra de diseño micro: 3,302, de las cuales 2,945 pertenecían
al panel 2015 y 357 completaban diseño. RNM informa 18,491 respuestas para el
total de 23,928 unidades de todos los tamaños, sin desglose realizado por
instrumento en la pieza leída.

| Variable | Texto/escala y código | Periodo | Página | Correspondencia con R03 |
|---|---|---|---|---|
| [`ENAPROCE-M64_1`](https://www.inegi.org.mx/rnm/index.php/catalog/518/variable/F1/V223), [`ENAPROCE-M64_2`](https://www.inegi.org.mx/rnm/index.php/catalog/518/variable/F1/V224), [`ENAPROCE-M64_3`](https://www.inegi.org.mx/rnm/index.php/catalog/518/variable/F1/V225) | Tres problemas principales ordenados; cada campo usa `1–8, 11–16, 19`; `6 = Exceso de trámites`, `16 = No tiene problemas`, `19 = Otro`. Multirrespuesta ordenada, no tres indicadores independientes. | Situación declarada; actividad 2017 | Cuestionario micro, p. 29 | **Proxy limitado.** No es comparable como “principal único” con 2015 sin armonización explícita. |
| [`ENAPROCE-M65`](https://www.inegi.org.mx/rnm/index.php/catalog/518/variable/F1/V227) | Principal trámite-obstáculo. `1–8, 11, 12`; `13 = Ninguno`; `19 = Otro`. | Situación declarada; actividad 2017 | p. 29 | **Proxy limitado.** Categorías 1–13 comparables con 2015; 19 es nuevo. |
| [`ENAPROCE-M66`](https://www.inegi.org.mx/rnm/index.php/catalog/518/variable/F1/V229) | Pesos en un mes normal de cumplimiento fiscal federal; excluye impuestos. | Mes normal de 2017 | p. 29 | **Directa para costo formal**, no pago informal. |
| [`ENAPROCE-M67`](https://www.inegi.org.mx/rnm/index.php/catalog/518/variable/F1/V230) | Horas aproximadas en un mes normal para trámites gubernamentales distintos del pago de impuestos. | Mes normal de 2017 | p. 31 | **Directa para carga temporal**, no corrupción. |

## 2018 · Pequeñas/medianas · tabla RNM F2

Población: pequeñas y medianas empresas del marco MENUE/RENEM 2017; cobertura
nacional por sector/tamaño y entidad × sector estratégico. Diseño
probabilístico y estratificado. Muestra de diseño PyME: 18,886 (14,585 panel y
4,301 para completar diseño). Las 1,740 grandes agregadas con fines descriptivos
no son representativas y quedan fuera del contrato R03.

| Variable | Texto/escala y código | Periodo | Página | Correspondencia con R03 |
|---|---|---|---|---|
| [`P81_6`](https://www.inegi.org.mx/rnm/index.php/catalog/518/variable/F2/V541?name=P81_6) | Exceso de trámites entre tres problemas principales. El diccionario lo rotula como columna de opción y conserva `6` como categoría, pero no documenta el valor de opción no seleccionada: se requiere FD real antes de recodificar blancos. | Situación declarada; actividad 2017 | Ambos cuestionarios PyME, p. 39 | **Proxy limitado.** Cambian número de selecciones y almacenamiento frente a 2015. |
| [`P82`](https://www.inegi.org.mx/rnm/index.php/catalog/518/variable/F2/V552?name=P82) | Principal trámite-obstáculo. `1–8, 11, 12`; `13 = Ninguno`; `19 = Otro`. | Situación declarada; actividad 2017 | p. 41; definiciones p. 40 | **Proxy limitado.** |
| [`P83`](https://www.inegi.org.mx/rnm/index.php/catalog/518/variable/F2/V554?name=P83) | Pesos en un mes normal de cumplimiento fiscal federal; excluye impuestos. | Mes normal de 2017 | p. 41 | **Directa para costo formal**, no pago informal. |
| [`P84`](https://www.inegi.org.mx/rnm/index.php/catalog/518/variable/F2/V555?name=P84) | Horas aproximadas en un mes normal para trámites gubernamentales distintos del pago de impuestos. | Mes normal de 2017 | p. 41 | **Directa para carga temporal**, no corrupción. |

## Comparabilidad 2015/2018

| Constructo | Comparabilidad | Condición |
|---|---|---|
| Horas mensuales de trámites | **Alta en texto y unidad** | `ENAPROCE-M64↔ENAPROCE-M67`, `P82↔P84`; comparar 2014 con 2017, no “2015 con 2018”. Requiere mismos tratamientos de faltante y diseño. |
| Gasto mensual de cumplimiento fiscal | **Alta en texto y unidad nominal** | `ENAPROCE-M63↔ENAPROCE-M66`, `P81↔P83`; deflactar pesos antes de comparar niveles y no llamarlo impuesto ni pago informal. |
| Trámite principal obstáculo | **Alta para códigos comunes** | 2018 añade `19=Otro`; `13=Ninguno` existe en ambas. No es filtro de exposición. |
| Exceso de trámites como problema | **No es una serie directa** | 2015 pide uno principal; 2018 pide tres. Puede construirse “mencionó exceso” por ola, pero cambia el estimando y el almacenamiento micro/PyME. |
| Solicitud/pago informal o corrupción | **No equivalente / no encontrado en lo revisado** | Ningún reactivo, filtro o código en el módulo XII ni en los diccionarios examinados. |

## Ponderación y faltante para una estimación real

Los cuatro archivos RNM enumeran `FAC_EXPA`; los catálogos documentan ajuste
por no respuesta y estimadores. Para producir una estimación se requieren aún:

1. microdatos reales de cada ola/instrumento, no bases de ejemplo;
2. descriptor de archivo definitivo con códigos de blanco, no sabe, rechazo,
   imputación y cualquier tope/edición de pesos u horas;
3. identificadores de estrato y UPM o réplicas oficiales (especialmente el
   conglomerado municipal de micro 2015), o una salida agregada calculada por
   INEGI con error estándar/IC95;
4. regla acordada sobre panel: corte transversal por ola o análisis panel; y
5. firma de la mesa para usar unidad empresa. Nada de lo anterior autoriza F6.
