# Contratos pendientes por consumidor · U2

Corte 23/sep/2026. #1080 escribe **exclusivamente** `RES-0028`; estas
operaciones no invocan ni amplían ese escritor. Los ejemplos son diffs secos
para revisión; ningún valor nuevo ni firma se atribuye a GEN2 aquí.

## Procedencia: 40 filas

`uso-efectivo-procedencia.tsv` individualiza cada llave. Las siete entradas
`coeficientes_generador_sellados` y ocho `asignados_coeficiente` entran en
`B`; una de estas ocho es `SIN MAGNITUD`. Las 13 listas de
`asignados_probabilidad` se cargan como YAML, pero `motor.correr()` no lee sus
valores para emitir. Las 12 condicionales entran en `consumibles()`, aunque
`Theta.valor()` lanza y el motor no las usa numéricamente. Ninguna fila se
declara histórica sin firma de mesa.

El escritor propio de procedencia exige una selección por `slot` y ruta YAML
exacta, hash previo, RESULT/CALC sellados y replay afirmativo, clase, escala,
ola, unidad, asociación frente a efecto, y valor de origen coincidente. Debe
reconstruir `B` y comparar la llave compuesta `(gen, coef)` antes/después;
rechaza un override que borre el fallback o convierta `SIN MAGNITUD` en cero.
Para probabilidades comprueba cardinalidad, suma y denominador de cada
conducta. Para condicionales comprueba eje, población y que exista una θ
cargable; una cita no vuelve numérico `Theta.valor()`. Diff seco de ejemplo
para una sola entrada `G2.aversion_riesgo`, **sin valor propuesto**:

```diff
   - gen: G2
     coefs:
-      aversion_riesgo: <legacy-exacto>
+      aversion_riesgo: <RESULT-valor-en-escala-idéntica>
```

La cita RESULT y el respaldo de clase requieren un campo/esquema acordado por
mesa; el diff final no se aplica hasta tener esa decisión. Una prueba negativa
cambia solo la escala o el signo del RESULT y exige diff vacío; otra mantiene
el valor pero cambia el par `(gen, coef)` y también exige diff vacío.

## Catálogo: 23 filas

`plan-catalogo-23.tsv` registra rol, dependencia y operación de cada momento.
El catálogo sellado de `ADR-68` se conserva. `valor_de()` lanza para los
15 HOLDOUT y para AJUSTE no implementado. Un CALC no modifica el catálogo;
la operación revisable es una **cita lateral** por `Mxx` con RESULT, CALC,
sello y rol. El adaptador propio rechaza cualquier cambio de rol, universo,
reserva o bytes del catálogo sellado. Diff de salida esperada en registro
lateral:

```diff
+ Mxx  RESULT-<id>  CALC-<id>  <sello>  <rol-sellado>  <dictamen>
```

## Celdas-D: seis YAML y seis referencias de código

`reconciliacion-146.tsv` identifica los seis YAML. El escritor de celda-D
requiere contrato de adjudicación, eje, reserva intacta, RESULT y CALC,
comparador y sello de la celda. Debe emitir una **propuesta de sucesora** con
hash nuevo, no alterar el YAML sellado. El diff seco se limita al nuevo
sidecar y a su registro de enlace; `milpa/src/celdas.py` queda intacto en U2.
Prueba negativa: falta de reserva, `NO-EJECUTABLE` o diferencia de universo
deja diff vacío. Antes/después: consulta real debe resolver la sucesora,
RESULT, CALC, generación y valor. Hoy esas seis lecturas permanecen legacy.

## Separación de contadores

`corrida0.py status` arroja 146 lecturas legacy activas **según pines**:
34 motor, 6 celdas-D, 23 catálogo, 40 procedencia y 43 marco. `RES-0028`
figura en `usos.tsv` como GEN2 por el pin derivado y queda fuera de esas
146. Antes de #1080, `milpa/tramite.yaml` conservaba el literal
`p=0.705687` sin cita GEN2. #1080, fusionado en `main` (`f16dd3d7`),
añadió la cita y probó la consulta exclusivamente para esa fila. El
contador de 146, por sí solo, no acredita consumo
efectivo. No se informa cero ni se firma adopción por la presente nota.
