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
mesa; el diff final no se aplica hasta tener esa decisión.

**PROPUESTA (no implementada; ACTO GEN2-CATALOGO-CONTRATO-Y-TEST-1,
`FP-260924-GEN2-CATALOGO-CONTRATO-Y-TEST-1-23e3-01`, espera firma):**
(a, recomendada) mismo esquema que `milpa/tramite.yaml` — en la entrada de
`procedencia.yaml` junto al valor: `corrida0_resultado_id`,
`corrida0_generacion: GEN2` y `clase_respaldo: <clase del RESULT>`; el
registro ya lee esos dos primeros campos en `procedencia.yaml`, así que
`T-REPRO` lo cubre sin código nuevo. (b) Sidecar
`milpa/procedencia-citas.tsv` (llave `(gen, coef)`, RESULT, CALC, sello,
clase): no toca el YAML, pero exige un lector nuevo y reabre la
contradicción que tuvo el catálogo (el valor vive en un archivo y la cita
en otro). Una prueba negativa
cambia solo la escala o el signo del RESULT y exige diff vacío; otra mantiene
el valor pero cambia el par `(gen, coef)` y también exige diff vacío.

## Catálogo: 23 filas

`plan-catalogo-23.tsv` registra rol, dependencia y operación de cada momento.
El catálogo sellado de `ADR-68` se conserva. `valor_de()` lanza para los
15 HOLDOUT y para AJUSTE no implementado. Un CALC no modifica el catálogo.

**Enmienda (ACTO GEN2-CATALOGO-CONTRATO-Y-TEST-1, 24/sep/2026, Decisión 3
de mesa de ADOPCION-2).** La «cita lateral» de la versión anterior no podía
pasar `T-REPRO(c)`: el test compara la cifra que el consumidor MATERIALIZA
contra el RESULT (`tests/check.py`, bloque (c)), y para un momento del
catálogo esa cifra era `NO-DECLARADO-EN-EL-REGISTRO`
(`tools/corrida0.py::_consumidores_momentos`, `valor_legacy=NO_DECLARADO`;
el pin de mesa copia ese mismo `valor_legacy`). La operación revisable pasa
a ser: **el catálogo lleva el valor GEN2 y su cita en columnas propias**,
añadidas al final del TSV, sin tocar ninguna columna sellada (id, rol,
universo, reserva):

```diff
- id_momento … spec_ref
+ id_momento … spec_ref  valor_gen2  corrida0_resultado_id  corrida0_generacion  calc_gen2  sello_gen2  discrepancia_gen1
+ Mxx … <sellado intacto>  <valor RESULT>  RESULT-<id>  GEN2  CALC-<id>  <sha256 sello.json>  NO-REPRODUCE-GEN1: unidad DELITO
```

`T-REPRO(c)` verifica `valor_gen2 == RESULT` con la vara de adopción;
rechaza valor sin cita completa (RESULT, CALC y sello) y cita sin valor.
`discrepancia_gen1` rotula el choque con la cifra GEN1 y **no bloquea**.
Escribe las columnas solo el escritor (ADOPCION-4), nunca a mano. Casos:
`tests/test_corrida0.py::t_catalogo_*` (un positivo sobre el momento 08, dos negativos).

## Celdas-D: seis YAML y seis referencias de código

`reconciliacion-146.tsv` identifica los seis YAML. El escritor de celda-D
requiere contrato de adjudicación, eje, reserva intacta, RESULT y CALC,
comparador y sello de la celda. Debe emitir una **propuesta de sucesora** con
hash nuevo, no alterar el YAML sellado. El diff seco se limita al nuevo
sidecar y a su registro de enlace; `milpa/src/celdas.py` queda intacto en U2.
Prueba negativa: falta de reserva, `NO-EJECUTABLE` o diferencia de universo
deja diff vacío. Antes/después: consulta real debe resolver la sucesora,
RESULT, CALC, generación y valor. Hoy esas seis lecturas permanecen legacy.

| Slot | YAML sellado | Candidato cotejable y dependencia de escritor |
|---|---|---|
| `RES-0171` | `DIN.ahorro_solo_informal.enif2024.localidad_x_edad` | `CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001` y `-EMISIONES-0001`; HOLDOUT ya consumido, champion ninguno: falta sucesora adjudicada y reserva nueva. |
| `RES-0172` | `G5.familismo_obligacion.actitud` | Sin CALC de relevo declarado en la fila; fijar instrumento, eje de actitud y reserva antes de una sucesora. |
| `RES-0173` | `G5.obligacion_medida.conducta` | Sin CALC de relevo declarado en la fila; no sustituir conducta con actitud; fijar cuestionario, eje y reserva. |
| `RES-0174` | `G5.radio_confianza.encuci_vs_enbiare` | Sin CALC de relevo declarado en la fila; se necesitan comparabilidad ENCUI/ENBIARE, eje y reserva. |
| `RES-0175` | `TRA.evade_norma.envipe2025.escolaridad_x_dominio` | `CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001` y `-EMISIONES-0001`; reserva de cruce consumida, champion ninguno. |
| `RES-0211` | `GOB.gobierno_digital.encig2025.edad_x_escolaridad` | `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` y `-EMISIONES-0002` requieren cotejo de eje y reserva; no se presume sucesora por el nombre. |

Diff revisable por slot, antes de cualquier aplicación:

```diff
 data/curacion-registro/celdas-d/<slot>.yaml  <sha sellado, intacto>
+data/curacion-registro/celdas-d/<slot>-sucesora.yaml  <nuevo sha; RESULT/CALC/eje/reserva/dictamen>
+forense/analisis/astra4-relevo/enlaces-celdas-d.tsv  <slot; sha previo; sha sucesor; firma mesa>
```

El acto del escritor debe probar seis fallos independientes: llave equivocada,
eje invertido, reserva gastada, resultado sin sello, valor previo discordante
y ausencia de firma. Ninguno puede crear la sucesora ni cambiar la referencia
activa de `milpa/src/celdas.py`.

## Separación de contadores

`corrida0.py status` arroja 146 lecturas legacy activas **según pines**:
34 motor, 6 celdas-D, 23 catálogo, 40 procedencia y 43 marco. `RES-0028`
figura en `usos.tsv` como GEN2 por el pin derivado y queda fuera de esas
146. Antes de #1080, `milpa/tramite.yaml` conservaba el literal
`p=0.705687` sin cita GEN2. #1080, fusionado en `main` (`f16dd3d7`),
añadió la cita y probó la consulta exclusivamente para esa fila. El
contador de 146, por sí solo, no acredita consumo
efectivo. No se informa cero ni se firma adopción por la presente nota.
