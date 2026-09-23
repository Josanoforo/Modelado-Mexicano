# ENCIG · intervalo de persistencia · spec v1.0 congelable

Acto ASTRA-3 U2, 22/sep/2026. El primer resultado que produzca este procedimiento es el que se reporta. Generación GEN2; cuenta_gen2 SI; adopta NO. La evaluación es RETROSPECTIVA, nunca un holdout nuevo. Esta spec y `spec.yaml` se congelan en un commit anterior a cualquier lectura de los RESULT históricos por esta sesión.

## Objeto y exposición

Diez celdas `digital × {sexo 2, edad 4, escolaridad 4}` de `forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv` (SHA256 `1715da9303957dac11146bd14e5498d11c554671edcdfb9c6ea7230845433a95`). Piso 2023: `CALC-PISOS-ENCIG2023-EJES-0002`, **no** un CALC ARBITRO, que puede contener R2025. Mismo estimando en las cuatro olas: proporción ponderada de trámites de pago ordinario de luz (`N_TRA=01`, `P7_3∈{1,2,4,5,6}`) por canal digital útil (`P7_3∈{4,5}`); ponderador `FAC_TRA`, estrato `EST_DIS`, UPM `UPM_DIS`; ejes sexo, edad y escolaridad de residentes. Persona elegida de 18+ en ciudades de 100 mil habitantes o más; unidad de observación TRÁMITE. No se agrega nacional ni se mezclan ejes.

Fuente de cada punto e IC95 muestral: RESULT sellados `CALC-ENCIG-SERIE-CANAL-2017/2019/2021` y piso `CALC-PISOS-ENCIG2023-EJES-0002`. Los cuatro medidores originales aplicaron 10 000 réplicas bootstrap de UPM estratificado, plan común a las celdas por ola, PCG64(42), percentiles 2.5/97.5. Esta corrida consume RESULT por hash, sin reabrir microdato. Es cálculo derivado de microdato sellado; `origen_numerico` se rotula conforme a ese linaje. No se presume independencia de celdas o transiciones que comparten una ola.

Exposición de esta sesión antes del freeze: specs, tabla de identidad, tabla documental, hashes y presencia de payloads; **ningún valor** de los cuatro RESULT consultado. Los microdatos 2017/2019/2021/2023 están presentes en CAJA y sus SHA256 coinciden con el manifiesto. `encig2021_csv` (SHA `c92ea34c…`) es el que usó la serie; el paquete `encig_2021_encig21_base_datos_csv` (SHA `4463e585…`) es diferente y no se sustituye. ENCIG2025 y sus resultados no se abren.

## Comparabilidad congelada antes de valores

`data/encig-canal-comparabilidad-texto-v1_0.tsv` SHA256 `0f8a718050f42d09c6694baa2deecba58d03e5f298f50f280d2e6542aac965aa`: 2017 y 2019 son MISMO-INSTRUMENTO contra ancla 2021; 2021 es MISMO-INSTRUMENTO; 2023 es CAMBIO-MENOR (redacción «etc.»→«etcétera» y cambios en otros códigos de trámites, no en `N_TRA=01` ni `P7_3`). La tabla cita cuestionarios y FD de cada ola, flujo de 6.1 a 7.3, nueve opciones y códigos, unidad y ponderador. Se incluyen 2017→2019, 2019→2021 y 2021→2023. Ningún par se excluye por magnitud observada. La misión general atribuye un salto al instrumento, pero el ADR de #972 dice SALTO-SIN-EXPLICAR; prima la corrección explícita U2. No se atribuye causalmente a pandemia ni psicología.

## Secuencia obligatoria

1. Congelar esta spec, su sidecar, `spec.yaml` y medidor completo por commit. El medidor verifica que identidad y veredictos documentales sean los congelados.
2. Preflight. Abrir RESULT sellados **2017/2019/2021**; calcular por celda cada `Δ = logit(p_fin)−logit(p_inicio)`. Si alguna `p` es 0, 1 o nula, Δ es SIN-DEFINIR. Para cada grupo `g = DIGITAL × eje`, dentro de cada transición promediar `Δ²` de celdas elegibles; entre transiciones promediar esas medias con peso igual. `τ²_train` usa **sólo** 2017→2019 y 2019→2021. No se centra ni descuenta error muestral: es segundo momento empírico del cambio observado, con ruido muestral, no varianza pura del proceso.
3. Construir y congelar en memoria el IC retrospectivo centrado en 2021, antes de leer la cantidad 2023. `ee_logit=(logit(IC-HI)−logit(IC-LO))/(2×1.959964)`; `IC=expit(logit(p_piso) ± 1.959964 sqrt(ee_logit²+τ²_g))`. Si punto/límites no están estrictamente en (0,1), o falta τ², queda NO-CALIBRABLE con causa. La fórmula es aproximada y puede ser conservadora.
4. Abrir sólo entonces los RESULT del piso 2023. Contar cobertura de punto 2023 dentro del IC retrospectivo, por celda y eje. Luego, con **la misma regla**, calcular `τ²_final` incorporando también 2021→2023 y el IC final alrededor del piso 2023. Identificadores TRAIN y FINAL distintos. La cobertura 2021→2023 no valida `τ²_final`.
5. Reportar `N` elegibles/cubiertas/no calibrables, cobertura por eje y global, Wilson binomial por celda sólo como referencia heurística. Las celdas se solapan. Hay sólo tres grupos eje; no se produce bootstrap de grupos ni un IC con falsa precisión. Reportar mediana/rango y ancho por celda en puntos porcentuales. El ancho mínimo simétrico descriptivo para alcanzar el punto 2023 se calcula alrededor de cada punto 2021, con límites recortados a [0,1], sin ajustar la regla. Comparar 35 pp de ENIF sólo como escala de ancho.
6. `run`, `verify` con tolerancia absoluta `1e-10`, asiento append en replay, nota y recibo. Cualquier fallo material se corrige conservando la primera emisión. Sin búsqueda de multiplicador por cobertura.

## Entradas y alcance

RESULT 2017 SHA256 `9bbe13c04dc7273d0253a23a63db8e07c1f28022483af9332a357a4a1ebcc340`; 2019 `3e4d5bda11dcfba16013a16a42edb3ebc8149d022e98abb00c9d19f916db9bf0`; 2021 `0db4eda8ad7754e7432a8f23e9e41f5d7c575bcf8fed203e1da69357173f4b53`; piso2023 `bd13a97b01f2d1251c54ddd3ff8c2d1ab5d16f68bc77f2b4041c1b617ee78568`. No ENCIG2025, no piloto 5, sin adopción ni modificación del registro.
