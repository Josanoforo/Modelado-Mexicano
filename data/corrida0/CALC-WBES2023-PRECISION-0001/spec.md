# Spec fijada · precisión WBES México 2023

Estado: `FIJADA-ANTES-DEL-NUEVO-IC`. Sucesor de
`CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001`; conserva sin cambios el
compuesto, filtros, faltantes, `wmedian`, denominadores y cinco puntos ya
publicados. La salida nueva responde cuánto error muestral puede sostenerse
para total y los cuatro tamaños WBES.

## Diseño acreditado y materialización

El *Mexico 2023 ES Implementation Report* (§§II, II.1–II.4 y III.3–III.8)
documenta muestreo aleatorio estratificado: establecimientos seleccionados
por muestreo aleatorio simple dentro de estratos formados por industria,
región, tamaño y condición panel/fresco. Es una selección de establecimientos
en una etapa; no se inventa una UPM distinta. El DDI (§ Sampling Procedure y
Database Structure) y el archivo materializan el estrato en `strata`; `a6a`
es dominio de publicación, no sustituto del estrato.

El *Sampling Note—Consolidated 2-16-22* (párrs. 15–16, 25–32, en especial
párr. 29 y nota 10) define probabilidades `n_h/N_h`, selección aleatoria
simple del panel dentro de celda y advierte que un panel singleton puede ser
selección de certeza. En México hay 242 estratos y 34 singleton en la muestra
completa (29 panel, 5 frescos), pero no se publican probabilidades/FPC por
celda panel/fresco para acreditar cuáles son certeza. Los pesos finales además
incorporan elegibilidad, suavizado y combinación panel/fresco.

## Estimador y precisión fijados

Para cada dominio, `Y=sum(w*I[si])`, `X=sum(w*I[clasificable])` y
`p=Y/X`. La linealización usa `z_i=w_i(y_i-p*x_i)/X`. Se conserva la muestra
completa: fuera del dominio `x_i=y_i=0`. Con el establecimiento como unidad de
muestreo, la aproximación con reemplazo suma por estrato
`n_h/(n_h-1) * sum((z_hi-zbar_h)^2)`. No aplica FPC porque falta la probabilidad
operativa por celda panel/fresco; tampoco incorpora incertidumbre adicional
por ajustes de elegibilidad/no respuesta.

Se publican, sin escoger el menor EE, dos escenarios de singleton:

1. `SINGLETON-CERTEZA`: aporte de varianza cero, condicional a que los 34
   singleton sean unidades de certeza.
2. `SINGLETON-AVERAGE`: cada singleton recibe la contribución media de los
   estratos no singleton (`V_base * H/H_no_singleton`).

Ambos se tipan `IC-APROXIMADO-CONDICIONAL-A-SUPUESTOS`, no oficiales ni cotas.
Los grados de libertad son `sum_h(n_h-1)` sobre la muestra completa. El EE se
reporta en escala de proporción y el IC95 usa transformación logit con crítico
t. Si `p` es 0 o 1, el IC queda nulo con
`PRECISION-NO-ESTIMABLE-FRONTERA`; nunca se publica `[0,0]` como certeza.

Los límites lógicos por faltantes del padre permanecen en columnas separadas
con su nombre; no son IC y no se combinan con éstos. El cálculo no prueba
diferencias entre tamaños, no compara WBES con ENCRIGE y no corrige sesgo por
no respuesta de ítem o de encuesta.
