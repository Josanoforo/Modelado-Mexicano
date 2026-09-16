# S6 · `salud.atencion.grave` — enmienda de alcance inferencial

### `prereg-caja-S6-L16` · **v1.6** · 16 de septiembre de 2026 · `sucesora_de: v1_5`

Esta versión supera a `S6-L16-spec-v1_5.md` (sha256
`48f56c21c5e3bc0320c88f18437982ac8e82fb3c597998fb5d90d55e82ebb49b`)
únicamente en el estatus de `FP-372`, que v1.5 remitía como decisión
pendiente en su línea 52. `CALC-0003-v4`, sus 143 RESULT, specs, medidor y
sellos permanecen byte por byte intactos — igual que v1.5 los conservó
frente a v1.4. Ninguna otra sección de v1.5 se toca ni se reinterpreta.

## Enmienda (heredada de v1.5, sin cambios)

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

## Lectura de resultados existentes (heredada de v1.5, sin cambios)

- Los puntos ponderados y las asociaciones descriptivas C1/C3/C4 se conservan.
- `NO-DISCRIMINA` en C1 y `CORROBORADA` en C3/C4 son veredictos históricos
  condicionados al contrato de incertidumbre de v4. No se reescriben.
- Para consumo actual, incluir/excluir cero bajo esa receta es una
  sensibilidad; no autoriza inferencia poblacional basada exclusivamente en
  esos IC.
- C1 sigue siendo la fila primaria y C3/C4 secundarias. La enmienda no cambia
  la multiplicidad, la prohibición causal, los universos, ponderadores,
  clasificaciones, joins ni el tier `[MEDIA]` de R4.4.

## Regla prospectiva (heredada de v1.5, sin cambios)

Mientras no exista una vía oficial ejecutable, S6 puede usarse
descriptivamente y sus IC sólo como sensibilidad explícita. No se promueven
nuevas conclusiones por significancia de esos IC. Si el productor entrega
pesos replicados o un servicio de varianza, se congela primero una spec
sucesora en CAJA con método, escala, grados de libertad, tratamiento de UPM
únicas y aceptación; después, y no antes, puede nacer otro CALC.

## `FP-372` — estatus, corregido en esta versión (`NC-0229`)

v1.5 decía, verbatim: «La decisión de mesa sobre este uso es `FP-372`.
Redactar esta recomendación no la firma.» Eso era correcto el 10/sep/2026,
cuando v1.5 se selló, y quedó vencido cinco días después: `FP-372` consta
**FIRMADA** en `forense/firmas-pendientes.tsv`, por la FIRMA DE MESA del 15
de septiembre de 2026 (verbatim «Si a todas.», sobre la HOJA DE FIRMAS DE
MESA 2026-09-15 archivada en `forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-1.md`
y propagada por `ACTO GEN2-FIRMAS-MESA-1`, `PR #785`). OBJETO 15 de esa hoja,
verbatim: «FP-372 — opción (a) para S6/R4.4: puntos/asociaciones descriptivas
se conservan, IC por localidad solo como sensibilidad, sin promover
conclusiones nuevas basadas en cruzar cero; veredictos condicionados de
CALC-0003-v4 no se reescriben; R4.4 sigue MEDIA.»

Lectura operativa a partir de esta versión: donde v1.5 decía que `FP-372`
«decide su uso inferencial», léase que decidió — la **opción (a)** de arriba,
que es exactamente la regla prospectiva que la sección anterior ya
describía. La firma decide el **estatus inferencial** y nada más: no
reescribe ningún sello, no mueve el tier `[MEDIA]` de R4.4, y **no cierra
`NC-0156`** (vía oficial de pesos replicados o servicio de varianza, que
sigue viva; la solicitud conjunta sigue sin enviar). Mismo criterio,
verbatim, que la ADENDA fechada 15/sep/2026 que `ACTO
GEN2-MANTENIMIENTO-Y-ARCHIVO-2` (`NC-0209`) ya aplicó por *append* a
`data/diseno-muestral.yaml` (campo `supuesto_varianza`, fuente ENNViH): esta
spec sucesora lleva la misma corrección al otro sitio que v1.5 identificaba
como contradictorio — `S6-L16-spec-v1_5.md:52` — de modo que la
contradicción, que `ACTO GEN2-MANTENIMIENTO-Y-ARCHIVO-2` dejó reducida a un
solo sitio (`NC-0229`, sucesor declarado), queda ahora en cero.

`FP-371` (DIN-M-01, constante + `folio`) sigue siendo un objeto distinto: su
firma (mismo día, OBJETO 14, RECHAZO del uso inferencial de EE/IC) no
acredita ni extiende nada de S6, y esta versión no la cita salvo por este
deslinde.
