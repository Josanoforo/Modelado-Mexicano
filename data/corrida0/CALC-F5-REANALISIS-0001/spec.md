# CALC-F5-REANALISIS-0001 · panel conocido bajo controles sin fugas

**Acto:** `GEN2-EVALUACION-SIN-FUGAS`, 11/sep/2026. **Naturaleza:**
`REANALISIS-DIAGNOSTICO-PANEL-CONOCIDO`. **Cuenta GEN2:** `NO`: este cálculo
audita material ya inspeccionado, no constituye una evaluación independiente
ni sustituye `CALC-TRIADA-0002`.

## Objeto y compuerta

Aplicar a las 224 capturas L, catorce resultados R y snapshot M históricos el
contrato técnico `F5-evaluacion-sin-fugas-spec-v1_0.md`. El medidor sólo puede
correr cuando importa desde bytes fijados la interfaz común de linaje que
entrega el acto 17. No contiene un resolver alternativo. El snapshot renovado
del acto 18 no es input de esta corrida y no se evalúa aquí.

## Inputs cerrados

`spec.yaml` enumera directamente cada captura y cada `resultados.json`, además
del plan, universo, snapshot, tarjetas M/R, contrato, calculador y módulo común
de linaje. Cada miembro lleva SHA-256. `corrida0` resuelve una sola instantánea
y entrega esos mismos bytes al medidor. El núcleo no abre el árbol; verifica
otra vez estado, hash, rol e igualdad exacta entre las celdas y posiciones de
los insumos.

La identidad de prompt no sustituye el hash de respuesta. La ruta R debe ser
exactamente la declarada por el universo y cada JSON debe corresponder al
`spec_id` y resultado puntual fijados. Un archivo adicional en el árbol no se
descubre ni se consume.

## Elegibilidad y cálculo

Se conservan los parámetros históricos: dos brazos L, ocho réplicas, mediana
de válidas sin imputar faltantes, MAE en puntos porcentuales, bootstrap pareado
de celdas con 10,000 réplicas, `random.Random(42)`, IC95, banda de 0.5 pp y
tolerancia `1e-9` pp. El conjunto congelado es el U3 de doce celdas publicado
por `CALC-TRIADA-0002`; no se recorta después de observar errores.

Para puntuar una celda se exige punto y correspondencia R; ambos puntos L;
punto M numérico e identidad confirmada; estado M y firewall aptos; tarjeta
M/R con estimando y corte acreditados; y clasificación de linaje `APTO` con
`dependencia_objetivo=NO`. Desconocido nunca equivale a limpio. Copia, rename,
padre o derivado del objetivo conservan su reserva mediante el resolvedor
común.

Una celda inelegible permanece en cobertura y exclusiones, pero no entra en
MAE ni bootstrap. Si cambia el U3 congelado, el veredicto global es
`NO-ADJUDICABLE-POR-CONTROL`; los resúmenes que queden son sólo diagnósticos.
Un ganador requiere además no tener menor cobertura que sus rivales.

## Alcance de las salidas

Las salidas escalares registran cobertura, estados, U3, MAE y comparaciones.
Los flotantes pueden ser `NO-ESTIMABLE` si no existe universo puntuable. La
tabla por celda se publica en la nota del acto con criterio, fuente, decisión
y efecto. Punto R, incertidumbre de encuesta, variación de L y dependencia de
familias permanecen separados. En particular, el punto DIN puede describirse,
pero sus sensibilidades SRS/constante+folio y los intervalos S6 no se promueven
a verdad terreno ni arreglan un estimando no comparable.

No abre microdatos, no llama modelos, no adopta un contendiente, no abre F6 y
no autoriza usar un M renovado. Una futura transferencia usa otra spec, un
snapshot elegible posterior al acto 18 y familias realmente reservadas.
