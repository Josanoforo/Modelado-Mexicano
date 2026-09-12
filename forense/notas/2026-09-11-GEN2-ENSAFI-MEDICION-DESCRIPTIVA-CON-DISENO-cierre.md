# ACTO GEN2-ENSAFI-MEDICION-DESCRIPTIVA-CON-DISENO · cierre

Fecha de ejecución: 11/sep/2026. Entorno: CAJA Ubuntu/WSL2, Python 3,
corpus local montado y sin llamadas a modelos. Worktree:
`/home/pc0/mm-gen2-ensafi-medicion-diseno`; rama:
`acto/gen2-ensafi-medicion-descriptiva-con-diseno`. El acto partió de
`origin/main=a6d731db26a90b5b81eb6c5415c01e26c179aef9`, con #723 ya fusionado,
y árbol inicial limpio.

Publicación: **[PR #730](https://github.com/Josanoforo/Modelado-Mexicano/pull/730)**;
HEAD al abrir `4acdbb5a3cfce138743627086e7547755c1f401a`. La fusión corresponde a
Jonás.

Antes de la validación final se integró sin conflicto
`origin/main=e37367581d5186ce4d4cf497377c83ebcd61cf93`; su único cambio frente al
corte inicial fue el snapshot concurrente del censo, que se conservó.

## 1 · Resultado ejecutivo

Se congeló y ejecutó `CALC-ENSAFI-DISENO-0001`, una extensión analítica con
identidad propia de las tablas descriptivas conocidas en #723. La corrida
publica 226 RESULT para 13 estimandos nominales: cuatro tasas de atraso del
hogar por clase amplia de deuda, una tasa general de atraso entre personas con
deuda y ocho estrategias de afrontamiento ante ingreso insuficiente.

La estimación usa el factor de la unidad correspondiente (`FAC_HOG` o
`FAC_ELE`) y linealización de dominio sobre la muestra completa, con UPM
anidada en estrato (`EST_DIS×UPM_DIS`), aproximación con reemplazo de
conglomerado último, grados de libertad de diseño e intervalo t de 95%
truncado a [0,1]. No elimina observaciones fuera del dominio antes de construir
la varianza. Las reglas para PSU singleton, frontera y denominador nulo estaban
fijadas antes de correr: no se inventan agrupaciones y la precisión no
acreditada se publica nula con causa, nunca como cero.

El diseño observado tiene 277 estratos, 2,915 UPM anidadas, 2,638 grados de
libertad, cero estratos singleton, cero UPM que crucen estratos, cero registros
sin diseño y cero pesos inválidos en ambas tablas.

## 2 · Resultados utilizables

| estimando | punto | EE | IC95 | n expuesto / válido / desconocido |
|---|---:|---:|---:|---:|
| hogar · deuda formal agregada | 27.8268% | 0.8810 pp | 26.0993–29.5543% | 4,897 / 4,855 / 42 |
| hogar · caja/familia/amistades | 30.0838% | 2.1035 pp | 25.9590–34.2085% | 922 / 921 / 1 |
| hogar · casa de empeño | 27.6593% | 2.7778 pp | 22.2125–33.1062% | 399 / 397 / 2 |
| hogar · prestamista/agiotista | 32.8204% | 3.2535 pp | 26.4407–39.2000% | 354 / 351 / 3 |
| persona · atraso general entre personas con deuda | 27.2627% | 0.8514 pp | 25.5932–28.9322% | 7,894 / 7,894 / 0 |
| afrontamiento 1 · préstamo familiar/amigos | 41.5863% | 1.0114 pp | 39.6030–43.5695% | 6,224 / 6,224 / 0 |
| afrontamiento 2 · uso de ahorros | 31.9620% | 1.1860 pp | 29.6363–34.2877% | 6,224 / 6,224 / 0 |
| afrontamiento 3 · reducción de gastos | 68.3070% | 1.0745 pp | 66.2000–70.4139% | 6,224 / 6,224 / 0 |
| afrontamiento 4 · venta/empeño | 9.7363% | 0.6198 pp | 8.5211–10.9516% | 6,224 / 6,224 / 0 |
| afrontamiento 5 · adelanto/extra/temporal | 10.4045% | 0.5784 pp | 9.2703–11.5388% | 6,224 / 6,224 / 0 |
| afrontamiento 6 · tarjeta/crédito formal o tienda | 10.2793% | 1.2763 pp | 7.7766–12.7820% | 6,224 / 6,224 / 0 |
| afrontamiento 7 · atraso de crédito/préstamo | 10.0741% | 0.6294 pp | 8.8399–11.3083% | 6,224 / 6,224 / 0 |
| afrontamiento 8 · cajas/prestamistas/agiotistas | 2.1154% | 0.2132 pp | 1.6973–2.5336% | 6,224 / 6,224 / 0 |

La tabla completa conserva también numerador y denominador ponderados, masa de
desconocidos, grados de libertad y estado de precisión en
`data/corrida0/ensafi2023-atraso-afrontamiento-diseno-v1_0.tsv`. Las fichas de
consumo por estimando están en
`data/corrida0/ensafi2023-fichas-consumo-v1_0.tsv`.

## 3 · Contrastes y controles

Los trece puntos coinciden exactamente con las tablas de #723: delta máximo
`0`. La tasa de persona 27.2627% reproduce por redondeo el 27.3% oficial; la
codificación no se ajustó a esa cifra. La implementación independiente no
importa el medidor y reconstruyó 156 campos numéricos de los trece estimandos;
delta máximo `4.718447854656915e-13`.

La corrida canónica es
`CALC-ENSAFI-DISENO-0001--f301beff795e`, sello
`e52423d6d1ecd177a6bbf59538a781066e9fa6394febd71d8f1843292968ad17`.
`preflight` fue VERDE, `run` terminó con código 0 y `verify` informa
`REPRODUCE`, `CONTEXTO=IDENTICO`, 226/226 resultados y 5/5 payloads
coincidentes. El registro independiente conserva una fila por campo y el
asiento de replay señala esta nota como evidencia.

## 4 · Uso y límites

El uso propuesto es contexto descriptivo nacional de ENSAFI 2023:
prevalencia de atraso dentro de cada clase amplia de deuda del hogar,
prevalencia general entre personas de 18 años y más con deuda, y respuestas
múltiples de personas cuyo ingreso no alcanzó para cubrir gastos en el último
mes. Las clases de deuda y las estrategias no son categorías excluyentes y no
se suman.

Estos resultados no identifican BNPL, CAT, costo, baja fricción o usura; el
atraso general de persona no se liga a producto ni trae una ventana explícita.
Tampoco convierten la comparación entre prestamista y crédito formal en un
efecto causal ni una tasa de hogar en riesgo individual. No se cambia el
motor, no se abren capturas F5 y no se adopta parámetro para N34/R1.7.

`NC-0164` permanece **ABIERTA**: falta una fuente o instrumento que enlace en
la misma unidad producto exacto, exposición/costo/CAT o fricción y daño causal.
La siguiente acción no es volver a producir estas tablas; es localizar ese
enlace o decidir un diseño nuevo que pueda identificarlo.

## 5 · Registro y reproducibilidad

La spec y el ejecutor se congelaron en el commit informativo
`f301beff795e9bcf553593cc212e08ea84a5b337`. La vía canónica publicó una
corrida y 226 RESULT propios; las vistas completas quedaron en 154 corridas,
3,763 resultados y 207 usos. No se creó uso/adopción activa para este CALC.

Comprobaciones principales:

```bash
python3 -m unittest tests/test_ensafi_diseno.py
python3 tools/corrida0.py spec-check CALC-ENSAFI-DISENO-0001
python3 tools/corrida0.py verify CALC-ENSAFI-DISENO-0001
python3 data/corrida0/CALC-ENSAFI-DISENO-0001/control_independiente.py
python3 tools/corrida0.py registro --lote CALC-ENSAFI-DISENO-0001
python3 tests/check.py --baseline
```

**Contador científico:** una medición GEN2 registrada (`cuenta_gen2=SI`) con
13 estimandos dentro de una sola muestra/operación analítica; no trece fuentes
ni trece muestras. **Adopciones:** cero.
