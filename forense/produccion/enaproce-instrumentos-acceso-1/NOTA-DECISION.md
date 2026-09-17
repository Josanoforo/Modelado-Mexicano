# Nota de decisión · R03 / ENAPROCE 2015–2018

## Qué mide realmente

ENAPROCE sí ofrece dos desenlaces cuantitativos útiles de carga regulatoria a
nivel **empresa**: horas aproximadas dedicadas en un mes normal a trámites
gubernamentales distintos del pago de impuestos, y pesos gastados en un mes
normal para cumplir obligaciones fiscales federales, incluidos servicios de
contador/materiales y excluidos los impuestos. Además recoge cuál trámite se
considera el principal obstáculo y si el exceso de trámites figura entre los
problemas de crecimiento.

No mide, en los seis cuestionarios y cuatro diccionarios revisados, que una
autoridad haya solicitado/insinuado un pago, ni que la empresa lo haya pagado.
El gasto fiscal es formal y definido; no puede reinterpretarse como mordida.
El obstáculo es opinión y no acredita exposición, acto ni causalidad. Por
tanto, la parte `pago informal` de R03 queda sin desenlace y el instrumento no
identifica `trámite.mordida.discrecional`.

## Comparabilidad

Las medidas de horas y gasto conservan texto, unidad mensual y exclusiones
entre olas, para micro y PyME. Comparan periodos de referencia **2014 y 2017**,
no literalmente años de levantamiento 2015 y 2018. El dinero exige deflactor.
El trámite principal conserva los códigos comunes y en 2018 añade `Otro`.

La percepción de “exceso de trámites” no forma una serie directa: en 2015 se
pide un único problema principal; en 2018 se piden tres. En 2018 micro son tres
campos ordenados y en PyME el diccionario presenta columnas por opción. Una
coincidencia del código 6 no elimina ese cambio de estimando/codificación.
También cambian marco y diseño: micro 2015 usa conglomerados municipales;
2018 se documenta como probabilístico estratificado y mayormente panel 2015.

## Decisión habilitada

**No tramitar acceso institucional para la R03 actual y no promoverla a F6.**
Acceder al microdato no puede crear el desenlace de corrupción ausente del
cuestionario. La candidata puede conservarse únicamente como alternativa de
alcance menor para un descriptivo de carga regulatoria empresarial, sujeto a
dos decisiones previas de mesa: aceptar unidad empresa y retirar de su objeto
la solicitud/pago informal.

Si la mesa adopta ese alcance menor, entonces sí tendría valor el acceso
indirecto ya acreditado en RNM por Laboratorio de análisis de datos. El
expediente institucional existente es
`forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/`; no contiene
una ficha ENAPROCE. No se crea ni envía otra campaña mientras la redefinición
no exista.

## Pieza que falta y alcance técnico condicional

Para estimar carga, faltan los microdatos reales (no ejemplos) o una salida
oficial, más el descriptor definitivo de faltantes y las variables de diseño.
El pedido mínimo, sólo tras la redefinición, sería:

- 2015 micro `M63`, `M64`; 2015 PyME `P81`, `P82`;
- 2018 micro `M66`, `M67`; 2018 PyME `P83`, `P84`;
- tamaño, sector, panel/ola, `FAC_EXPA`, estrato y UPM/réplicas, y códigos de
  faltante/imputación;
- como salida agregada alternativa: media/mediana o cuantiles acordados de
  horas y gasto por ola × micro/PyME, total ponderado, `n` no ponderado,
  error estándar o IC95 y reglas de exclusión.

No se necesitan identificadores personales ni geografía fina. La salida de
gasto debe conservar pesos nominales por periodo para que el usuario aplique
un deflactor declarado. Esta especificación no es solicitud ni compromiso del
titular; permanece **PREPARADA, NO ENVIADA**.
