# S6 · `salud.atencion.grave` — enmienda de alcance inferencial

### `prereg-caja-S6-L16` · **v1.5** · 10 de septiembre de 2026 · `sucesora_de: v1_4`

Esta versión supera a `S6-L16-spec-v1_4.md` (sha256
`e2060c146d81841e0d1cb3fc8264b44eb1df8a331001c46dc67098d2423b1982`)
únicamente en el alcance atribuido al diseño y a los intervalos. Las versiones
anteriores, `CALC-0003-v4`, sus 143 RESULT, specs, medidor y sellos permanecen
byte por byte intactos.

## Enmienda

`c_portad.id_loc` identifica localidad y `c_portad.estrato` clasifica cuatro
tamaños de localidad. La documentación oficial de ENNViH-1 describe 180 UPM y
tres estratos socioeconómicos de selección, y la FAQ oficial indica que la UPM
no es pública. No se halló una declaración oficial que haga equivalentes
localidad/UPM o tamaño de localidad/estrato de selección, ni que admita esa
pareja como aproximación para varianza.

En consecuencia, quedan retiradas prospectivamente estas dos afirmaciones de
v1.3 heredadas por v1.4:

1. que `id_loc` es el «conglomerado correcto» del diseño; y
2. que disponer de `id_loc` permite levantar la reserva de varianza.

La receta ejecutada se nombra desde ahora **bootstrap de localidades dentro de
cuatro clases de tamaño, sensibilidad no acreditada como diseño oficial**. No
se conoce la dirección ni magnitud de su error frente al EE/IC del diseño real.
No se denomina conservadora, cota inferior ni garantía de varianza.

## Lectura de resultados existentes

- Los puntos ponderados y las asociaciones descriptivas C1/C3/C4 se conservan.
- `NO-DISCRIMINA` en C1 y `CORROBORADA` en C3/C4 son veredictos históricos
  condicionados al contrato de incertidumbre de v4. No se reescriben.
- Para consumo actual, incluir/excluir cero bajo esa receta es una
  sensibilidad; no autoriza inferencia poblacional basada exclusivamente en
  esos IC.
- C1 sigue siendo la fila primaria y C3/C4 secundarias. La enmienda no cambia
  la multiplicidad, la prohibición causal, los universos, ponderadores,
  clasificaciones, joins ni el tier `[MEDIA]` de R4.4.

## Regla prospectiva

Mientras no exista una vía oficial ejecutable, S6 puede usarse
descriptivamente y sus IC sólo como sensibilidad explícita. No se promueven
nuevas conclusiones por significancia de esos IC. Si el productor entrega
pesos replicados o un servicio de varianza, se congela primero una spec
sucesora en CAJA con método, escala, grados de libertad, tratamiento de UPM
únicas y aceptación; después, y no antes, puede nacer otro CALC.

La decisión de mesa sobre este uso es `FP-372`. Redactar esta recomendación no
la firma. `FP-371` pertenece a DIN-M-01 (constante + `folio`) y no acredita ni
autoriza automáticamente el diseño de S6.

