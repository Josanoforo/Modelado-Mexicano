# `CALC-ENIF-0002` — población y horizonte de ahorro, ENIF 2024

**Spec congelada antes de abrir `TMODULO.csv` en este acto.** Fuente de la
decisión: `MESA-10SEP:D04/D05` en `data/corrida0/decisiones.tsv` y
`forense/encargos/2026-09-10-MESA-CONCILIACION-E01.md`: conservar el histórico,
adoptar A/A (`P4_10 ∈ {1,2}`; `P3_13 ∈ {1,2,3,4}` frente a `{7}`), mostrar el
residual y añadir una celda de no trabajadores sobre el universo poblacional.

## 1. Correspondencia y reuso

La unidad es la persona elegida de 18 años o más en `TMODULO.csv`; el peso es
`FAC_PER`. `CALC-ENIF-0001` ya midió exactamente las dos celdas trabajadoras
autorizadas y se reutiliza por identidad de fuente, universo, códigos y método:

- con seguridad social: `P3_13 ∈ {1,2,3,4}`;
- sin seguridad social: `P3_13 = 7`;
- horizonte corto: `P4_10 ∈ {1,2}`; no corto: `{3,4,5}`.

Este CALC no vuelve a medir esas celdas ni repite las familias B/C. Lee el
`resultados.json` sellado de `CALC-ENIF-0001` como insumo versionado y verifica
sus cuatro puntos antes de producir la celda nueva. El histórico GEN1
(`P4_10={1}` y otra agrupación de `P3_13`) permanece identificable y no es
insumo.

`P4_10=1` significa literalmente «Menos de una semana / No tiene ahorros».
Ninguna salida separa ambas partes. Esta es una limitación del instrumento
(`NC-0126`), no falta de cálculo.

## 2. Dominio independiente de no trabajadores

El cuestionario pregunta `P4_10` a todas las personas elegidas. La condición
de actividad se resuelve con los saltos, sin imputar `P3_13`:

- **trabajadora:** `P3_8 ∈ {1,2}` o, tras la verificación, `P3_9 ∈ {1..6}`;
- **no trabajadora:** `P3_8 = 8` (limitación permanente que impide trabajar,
  pase directo a 3.14) o `P3_9 = 7` (no hizo actividad por un ingreso);
- `P3_13` se usa únicamente para partir a quienes trabajan. Su blanco es
  estructural tanto para no trabajadores como para trabajadores sin pago
  (`P3_10=6`), por lo que blanco nunca equivale por sí solo a no trabajador.

El dominio nuevo es `U_NT = no_trabajadora ∧ P4_10∈{1..5} ∧ FAC_PER>0`.
Se miden directamente `p(corto|U_NT)` y `p(no_corto|U_NT)`, con numeradores
disjuntos. `P4_10∈{8,9}`, blanco o código inválido se cuenta y excluye; no se
imputa.

## 3. Partición y cobertura poblacional

Sobre `P4_10` válido se publica una partición exhaustiva y disjunta:

1. trabaja con seguridad social (`P3_13∈{1..4}`);
2. trabaja sin seguridad social (`P3_13=7`);
3. no trabaja (definición de §2);
4. residual trabajador (`P3_13∈{5,6,9,b}`), incluida la persona trabajadora
   sin pago a quien el salto de `P3_10=6` no pregunta `P3_13`.

Una guardia para si actividad trabajadora/no trabajadora se solapa o deja una
fila válida sin clasificar. Las masas se expanden con `FAC_PER`; además se
publica la cobertura de `P4_10` válido sobre toda la población y el faltante.

El total poblacional, al ser estimable, se calcula **directamente** como razón
ponderada sobre todas las filas con `P4_10` válido. No es un promedio simple
de tasas de celdas. Su IC se obtiene en las mismas réplicas del diseño, por lo
que conserva automáticamente masas y covarianza entre dominios.

## 4. Diseño e incertidumbre

Punto: `Σ FAC_PER·1(resultado) / Σ FAC_PER` en orden fijo de fila. IC95:
bootstrap de `UPM_DIS` con reemplazo dentro de `EST_DIS`, 1,000 réplicas,
`numpy.PCG64`, semilla `20260910`, percentiles 2.5/97.5. Las llaves de diseño
se leen como texto opaco. Un estrato con una sola UPM aporta varianza cero y el
IC se rotula `IC-CON-ESTRATOS-DE-UPM-UNICA`, límite inferior de anchura, no
exacto. Si falta todo el diseño, se conserva el punto y el IC sale no
estimable.

## 5. Alcance de adopción

El CALC es descriptivo y cuenta como GEN2 por el objeto explícito de este
encargo: `cuenta_gen2=SI para CALC-ENIF-0002`, ejecutando D04/D05. La adopción
al motor sólo aplica cada tasa a su dominio; la tasa de no trabajadores no se
propaga a trabajadores ni viceversa. El residual se muestra y se mide, pero no
gana automáticamente un consumidor. El resultado poblacional es una vista
descriptiva, no una regla para ignorar dominios.
