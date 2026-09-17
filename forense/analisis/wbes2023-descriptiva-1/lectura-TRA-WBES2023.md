# WBES México 2023 · solicitudes o expectativas de pagos informales

## Qué se estimó

La medición describe establecimientos formales privados cubiertos por WBES México 2023: al menos cinco empleados, manufacturas y servicios seleccionados, con cobertura nacional. No representa negocios informales, establecimientos menores de cinco empleados ni sectores fuera del universo WBES.

El estimando primario es la proporción ponderada de establecimientos con al menos una de seis interacciones confirmadas —conexiones eléctrica o de agua, permiso de construcción, inspección o reunión fiscal, licencia de importación y licencia de operación— que reportaron que se esperaba o solicitó un regalo o pago informal. Cinco interacciones recuerdan los últimos dos años y la fiscal el último año. El reactivo no prueba que el pago se haya realizado.

Los cuatro documentos autorizados acreditan los seis pares filtro/evento, pero no incluyen la ficha que define el agregado oficial ni su regla para respuestas parciales. Por ello el compuesto es un estimando descriptivo propio y se acompañan las seis tasas separadas; no se presenta como réplica certificada del indicador oficial de incidencia de soborno.

## Magnitud observada y denominador

De 1,322 establecimientos entrevistados, 257 tuvieron al menos una interacción confirmada. Esos expuestos representan 49,044.606 establecimientos expandidos con `wmedian`, 10.12% del total expandido cubierto (484,464.219). Los 1,049 casos sin ninguna de las seis interacciones confirmadas no se trataron como ceros; otros 16 quedaron con elegibilidad de exposición desconocida.

Entre los 257 expuestos, hubo 38 respuestas positivas, 204 negativas y 15 con desenlace desconocido. La razón ponderada entre los 242 casos clasificables fue **15.24%**. La masa ponderada desconocida fue 2.33% del denominador expuesto. Si todos los desconocidos fueran negativos, el resultado sería 14.89%; si todos fueran positivos, 17.21%. Éstos son límites lógicos por faltantes, no intervalos de confianza.

| Tamaño WBES | n entrevistado | n expuesto | Peso expuesto | Punto entre clasificables | Masa desconocida | Límites por faltantes |
|---|---:|---:|---:|---:|---:|---:|
| Total cubierto | 1,322 | 257 | 49,044.606 | 15.24% | 2.33% | 14.89%–17.21% |
| Pequeña, 5–19 | 624 | 104 | 34,956.525 | 15.38% | 0.49% | 15.30%–15.80% |
| Mediana, 20–99 | 305 | 62 | 9,680.213 | 14.15% | 5.07% | 13.43%–18.50% |
| Grande, 100–250 | 229 | 44 | 2,902.856 | 17.64% | 11.91% | 15.54%–27.44% |
| Extra grande, 251+ | 164 | 47 | 1,505.013 | 14.54% | 8.78% | 13.26%–22.04% |

Las pequeñas concentran 71.3% del peso del denominador expuesto. La mayor tasa puntual aparece en grandes (17.64%) y la menor en medianas (14.15%), una separación de 3.49 puntos porcentuales. No debe leerse como diferencia estadística: no se estimó varianza de diseño, y los límites de faltantes de grandes, medianas y extra grandes se superponen ampliamente. Incluso en pequeñas, donde casi no hay desenlace faltante, el intervalo muestral sigue sin estar disponible.

## Interacciones separadas

| Interacción | n expuesto | Punto entre clasificables | Masa desconocida | Límites por faltantes |
|---|---:|---:|---:|---:|
| Conexión eléctrica | 44 | 27.61% | 0.88% | 27.36%–28.25% |
| Conexión de agua | 14 | 26.37% | 0.00% | 26.37%–26.37% |
| Permiso de construcción | 137 | 7.31% | 4.33% | 7.00%–11.33% |
| Inspección o reunión fiscal | 75 | 5.45% | 3.59% | 5.25%–8.84% |
| Licencia de importación | 17 | 0.00% | 0.00% | 0.00%–0.00% |
| Licencia de operación | 40 | 15.72% | 2.76% | 15.29%–18.05% |

Estas tasas tienen denominadores distintos y pequeños; no deben promediarse para reconstruir el compuesto. El cero observado en licencias de importación significa que ninguno de 17 casos expuestos reportó un evento positivo en la muestra, no que la tasa poblacional esté demostrada como cero.

## Alcance para TRA

El resultado permite afirmar que, en el universo empresarial WBES cubierto, la solicitud o expectativa de regalos/pagos informales no puede describirse usando a todos los entrevistados como denominador: sólo cerca de una décima parte del peso total tuvo alguna de las seis interacciones. Dentro de ese grupo expuesto, el punto descriptivo propio es aproximadamente 15%, con una sensibilidad a faltantes acotada a 14.9%–17.2%.

No permite concluir causalidad, que un pago se efectuó, que un tamaño difiere estadísticamente de otro, ni que WBES y ENCRIGE midan magnitudes directamente comparables. La documentación acredita muestreo estratificado y pesos, pero no un procedimiento operativo completo para varianza de dominio y estratos singulares; la incertidumbre se tipa `IC-DE-DISEÑO-NO-ESTIMABLE-CON-INSUMOS-DISPONIBLES`. Ninguno de los cuatro objetos contiene una cifra oficial comparable posterior al congelamiento.

Reproducción dirigida:

```bash
python3 tools/corrida0.py preflight CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001
python3 tools/corrida0.py run CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001
python3 tools/corrida0.py verify CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001
```
