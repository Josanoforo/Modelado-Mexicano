# ASTRA-3 U2 · intervalo de persistencia ENCIG · resultado y recibo

**EJECUTADO.** `CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001` (GEN2, `cuenta_gen2=SI`, `adopta=NO`, origen numérico NUEVO por cálculo de RESULT de microdato sellados). Freeze en `ca4475f0` y corrección de campo `parametros` exigido por preflight en `c8788ffc`, ambos antes de valores. `python3 tools/corrida0.py preflight …` VERDE; `run …` primera y única emisión; `verify …` REPRODUCE con 117/117 RESULT, siete insumos COINCIDE y tolerancia absoluta `1e-10`. Sello SHA256 `637fe73d154d33086b0d6cd1b69a1b0b7b7c5040da0d2e53f9c0005baa67942d`.

**LEÍDO.** Documentación de 2017/2019/2021/2023 por `data/encig-canal-comparabilidad-texto-v1_0.tsv`, specs de la serie y del piso `CALC-PISOS-ENCIG2023-EJES-0002`; los paquetes históricos del manifiesto se verificaron por hash en CAJA sin tabularlos de nuevo. El cálculo leyó sólo RESULT sellados, cuyos hashes figuran en `spec.yaml`. Ni ENCIG2025 ni CALC ARBITRO de esa ola se abrieron. El primer acceso de esta sesión a valores históricos fue `run` después del freeze. La misión general dice que #972 atribuyó el salto al instrumento; U2 corrige esa premisa: el ADR dice SALTO-SIN-EXPLICAR y los tres pares están incluidos por texto.

## Resultado retrospectivo 2021→2023

Comando: `python3 tools/corrida0.py run CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001`; fuente numérica: `data/corrida0/CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001/resultados.json`. Unidad de los puntos: **TRÁMITE** de pago ordinario de luz de persona elegida 18+ en ciudad de 100 mil habitantes o más; escala de proporciones [0,1], anchos en puntos porcentuales. Es evaluación **RETROSPECTIVA**, no holdout ciego.

| Grupo `digital × eje` | τ² train, logit² | τ² final, logit² | Cubiertas/elegibles | Wilson por celda 95%, referencia |
|---|---:|---:|---:|---:|
| Sexo | 0.018924 | 0.013787 | 2/2 | [0.342, 1.000] |
| Edad | 0.030828 | 0.024576 | 4/4 | [0.510, 1.000] |
| Escolaridad | 0.020512 | 0.032865 | 3/4 | [0.301, 0.954] |
| **Total** | — | — | **9/10 = 0.90** | **[0.596, 0.982]** |

Hay 10 elegibles, 9 cubiertas y 0 no calibrables. `τ²_train` usa exclusivamente 2017→2019 y 2019→2021. `τ²_final` añade 2021→2023 y sirve para un intervalo futuro alrededor del piso 2023; la cobertura 9/10 **no** lo valida. Los cambios consecutivos comparten ola y las celdas se solapan; Wilson por celda es sólo referencia heurística. Tres grupos completos son insuficientes para un bootstrap de grupos con precisión defendible, aun antes de considerar que comparten muestra.

| Eje | Categoría | Cubierta | Ancho evaluado pp | Mínimo simétrico para alcanzar 2023 pp | Ancho final pp |
|---|---|---:|---:|---:|---:|
| Sexo | 1 | sí | 13.22 | 3.92 | 11.61 |
| Sexo | 2 | sí | 13.63 | 1.09 | 11.77 |
| Edad | 18–29 | sí | 16.69 | 0.83 | 15.14 |
| Edad | 30–44 | sí | 16.33 | 5.26 | 14.27 |
| Edad | 45–59 | sí | 17.13 | 7.55 | 15.65 |
| Edad | 60+ | sí | 17.37 | 5.19 | 15.27 |
| Escolaridad | Hasta primaria | **no** | 14.43 | 18.44 | 16.15 |
| Escolaridad | Secundaria | sí | 14.62 | 11.15 | 17.84 |
| Escolaridad | Media superior | sí | 14.44 | 2.31 | 17.88 |
| Escolaridad | Superior | sí | 12.11 | 5.08 | 14.31 |

El ancho evaluado tiene mediana **14.53 pp** y rango **12.11–17.37 pp**. El final tiene mediana **15.21 pp** y rango **11.61–17.88 pp**. El mínimo simétrico descriptivo tiene mediana **5.14 pp** y rango **0.83–18.44 pp**; no se usó para ajustar τ². En la celda no cubierta, el punto 2021 era 0.4043, el punto 2023 0.3121 y el IC evaluado [0.3342, 0.4785]. Los IC finales ocupan aproximadamente [0.237, 0.796] entre todos sus extremos; no hay saturación junto a 0 o 1. La amplitud mediana final equivale a menos de la mitad de los 35 pp del IC ENIF; esa comparación sólo indica escala y no igualdad de instrumentos, desempeño o calidad.

## Lectura para mesa

**REPORTADO.** Propuesta: **DIFERIR la adopción como IC de cobertura garantizada**. La regla discrimina más que el rango ENIF de 35 pp, pero falló una de diez celdas en una sola evaluación histórica; sólo hay dos transiciones para entrenar y tres grupos solapados para valorar incertidumbre. Puede usarse como análisis de sensibilidad del piso 2023, con `τ²_final` y rótulo `muestral + segundo momento empírico del cambio observado`, sin presentarlo como validación futura. Una aplicación nueva requeriría el juicio de mesa y evaluación autorizada independiente; esta unidad no abre ENCIG2025 ni adopta nada.

## NO-CORRIDO / RESERVAS

- ENCIG2025, piloto 5 y CALC ARBITRO de esa ola: reservados. Ninguna cobertura prospectiva ni causalidad atribuida al salto.
- Bootstrap de grupos: sólo tres grupos, además dependientes por muestra; incertidumbre de cobertura insuficientemente determinada.
- Microdato no se reestimó en este CALC: se consumieron estimaciones por diseño ya selladas, con hash de cada RESULT origen. `data/raw` no está montado en este worktree; la presencia y los hashes de los paquetes se verificaron en la CAJA compartida.

## CONSUMIDO

PR [#1041](https://github.com/Josanoforo/Modelado-Mexicano/pull/1041), rama `codex/astra3-encig-persistencia-1`. Mesa recibe el CALC sellado y la propuesta de diferir adopción; fusión y adopción quedan a su cargo.

## Seguimiento CI tras #1039

**EJECUTADO 23/sep/2026.** #1039 ya estaba fusionado (`74289983`); se hizo `git fetch origin` y se integró `origin/main` (`f28d1038`). El merge `d631d354` conserva alcanzables los commits originales `ca4475f0`/`c8788ffc` del freeze y la primera emisión `e6241bba`; el CALC original sigue `verify = REPRODUCE`, contexto IDENTICO. El CI previo de #1041 fallaba por dos cambios propios: T02 trataba el basename genérico `medidor.py` de `tools/astra/` como documento duplicado, y `guardias` no tenía la fila del test nuevo en su censo. Se indexa la identidad de módulos Astra por ruta para T02, sin eximirlos del chequeo de contenido; se añadió sólo la fila clasificada por `tools/ci_guardias.py::clasifica` al censo, y el test tiene invocador de módulo ejecutable sin pytest. T02 dirigido: cero FAIL; `ci_guardias.py --ejecuta-huerfanos`: 91 ejecutados, 70 saltados por causas del censo, cero fallidos; test propio: 4/4. Los tres FAIL restantes de la suite (T06×2, T08×1) están en la línea base del corpus y no proceden de U2.
