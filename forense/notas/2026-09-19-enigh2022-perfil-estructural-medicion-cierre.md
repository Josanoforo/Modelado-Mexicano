# Cierre — perfil estructural ENIGH 2022

Universo: integrantes del hogar de 18 a 96 años con factor persona válido; unidad: persona; escala: proporción en [0, 1]; evidencia (a), datos primarios en México.

## Dictamen

La corrida sellada `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003` estima P1 y P2. P3 queda exactamente `NO-ESTIMABLE-POR-DEFINICION-NO-ACREDITADA`: la descripción de la base, p. 75, contrapone «cinco años antes de la entrevista» con «octubre de 2005» para ENIGH 2022 y no acredita de manera suficiente el universo por edad ni los saltos. Por ello no se abrió la columna de respuestas `residencia`.

El universo analítico contiene 217,080 personas muestrales y representa 91,619,046 personas. Parte de 309,684 registros (masa 128,999,038), conserva 309,534 integrantes oficiales del hogar (masa 128,889,708), y excluye por separado 137 trabajadores domésticos (104,837), 13 huéspedes (4,493), 92,298 menores de 18 (37,208,808) y 156 mayores de 96 (61,854). No hubo edad ni peso inválidos, pérdida en los joins ni diseño faltante.

## Lectura sustantiva

En este universo, 49.63% declaró haber cotizado alguna vez a la seguridad social y 50.37% no. `segsoc` conserva ese significado documental: no es una tasa oficial de informalidad laboral. Los tramos de edad representan 26.32% (18–29), 28.76% (30–44), 25.03% (45–59) y 19.89% (60–96).

Por tamaño de localidad, 48.75% reside en localidades de 100,000 habitantes o más, 14.64% en las de 15,000–99,999, 13.84% en las de 2,500–14,999 y 22.77% en las de menos de 2,500. El estrato socioeconómico nativo se distribuye en 18.59% bajo, 50.77% medio bajo, 21.09% medio alto y 9.56% alto; no se interpreta como cuartil de ingreso.

La tenencia en el hogar es 64.50% con conexión a internet y 93.76% con celular. No son mediciones de uso personal, smartphone ni banca digital, y ninguna se elige automáticamente como el corte `acceso_digital`.

La conjunta `segsoc × tramo_edad × tam_loc × est_socio` cubre las 217,080 personas y toda su masa: no pierde casos completos. Enumera las 128 combinaciones; 120 son observadas y ocho son `CERO-MUESTRAL`. Esas ocho corresponden a `tam_loc=4 × est_socio=3` en ambos valores de `segsoc` y los cuatro tramos de edad. No se declaran imposibles ni ausencia poblacional. La celda de mayor masa es «Sí × 30–44 × 100,000 y más × medio bajo», con proporción 0.04134, n=7,236 y 2,427 UPM.

## Incertidumbre y controles

Los puntos usan el factor persona. La incertidumbre usa 1,000 réplicas de bootstrap de UPM dentro de los 560 estratos `est_dis`, con semilla PCG64 20260919 y un plan compartido; hay 10,211 UPM y ningún estrato con una sola UPM. Los IC son percentiles 2.5/97.5 y los EE son la desviación de las réplicas.

Las llaves persona son únicas; los joins persona–hogar fueron m:1 sin expansión ni faltantes. Las seis variables P1 tienen cobertura total en el universo. Las particiones suman uno, la marginalización de P2 coincide con sus marginales hasta `3e-12`, y el contraste independiente reproduce `P(segsoc=1)` a `3.3e-13`. Un bootstrap independiente para 18–29 obtuvo EE 0.0014304 frente a 0.0013766 sellado (diferencia 0.0000538, dentro de la tolerancia focal congelada de 10%).

## Comprobación final del marco de diseño

La observación sobre el plan estrato–UPM queda cerrada sin modificar el CALC sellado. Con el mismo payload de 90,030,937 bytes y SHA-256 `3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06`, se comparó el conjunto exacto de pares de diseño de todas las 309,684 filas con factor persona finito y positivo contra el de las 217,080 personas del universo principal.

Ambos conjuntos son idénticos: 10,211 pares estrato–UPM, 560 estratos y huella canónica SHA-256 `4db8099b048d52a0d70cb8084417d6f7e8f59c2700353528e24709dfe95a178a`. Hay cero pares exclusivos del marco, cero pares exclusivos del dominio, cero estratos perdidos y cero estratos con UPM única en ambos conjuntos. Tampoco hay claves `est_dis` o `upm` faltantes en ninguno. Las 92,604 personas con peso válido fuera del dominio no hacen desaparecer ninguna UPM.

Para este estimando de dominio, cada persona fuera del dominio tendría indicador cero y, por tanto, aporte cero tanto al numerador como al denominador de todos los cocientes publicados. Omitir esas filas de aporte cero no cambia los totales por UPM. Como además el conjunto ordenado de pares y la partición de UPM por estrato son exactamente los mismos, el algoritmo multinomial consume el mismo plan de remuestreo con la misma semilla; no cambia puntos, réplicas, EE ni IC. No se requiere sucesor ni nueva corrida.

Las claves faltantes se trataron explícitamente: una fila sin `est_dis` o `upm` no forma un par; el medidor sellado desactiva toda la precisión si encuentra cualquiera dentro del universo principal, sin imputarla ni crear una UPM artificial. El conteo observado fue cero. El tratamiento congelado de singleton —remuestrear la única UPM a sí misma— tampoco entra en operación porque el conteo fue cero tanto en marco como en dominio.

Evidencia y mandato reproducible: `forense/analisis/enigh2022-perfil-estructural-cli-1/enigh2022_perfil_compara_marco_diseno.py data/raw/enigh2022_nc_csv.zip`. La salida agregada, sin identificadores de microdatos, está en `enigh2022-perfil-comparacion-marco-diseno.json`. No se reabrieron `segsoc`, residencia ni los resultados sustantivos.

Para este cierre se integró `origin/main` vigente en la rama y se regeneraron `corridas.tsv`, `resultados.tsv` y `usos.tsv` exclusivamente mediante `corrida0 registro --escribe --lote CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003`; el lote no autorizó replay ajeno. Una segunda proyección informó `sin diferencia con el archivo en disco` para las tres vistas.

## Mapa RESULT → significado → demanda

| RESULT | Significado | Relación con `CORR-0076` |
|---|---|---|
| `RESULT-ENIGH22-PERFIL-P1-*` | 18 filas marginales, cobertura, puntos e incertidumbre | Aporta evidencia descriptiva para `RES-0165` formalidad, `RES-0166` edad, `RES-0167` urbanización, `RES-0168` ingreso/estrato y `RES-0169` acceso digital; no releva ningún slot. |
| `RESULT-ENIGH22-PERFIL-P2-*` | 128 celdas conjuntas y 14 marginales de casos completos | Informa soporte empírico conjunto para decidir la composición de π; no adjudica la malla ni calibra pesos. |
| `RESULT-ENIGH22-PERFIL-P3-*` | Estado y evidencia de no estimabilidad documental | Delimita lo que falta para `RES-0170`; no propone un corte de migración. |
| `RESULT-ENIGH22-PERFIL-UNIVERSO-*`, `EMBUDO-*`, `DISENO-*`, `JOIN-*` | Universo, exclusiones y trazabilidad material | Controles del alcance persona y del diseño; no son cortes del motor. |
| `RESULT-ENIGH22-PERFIL-USO` | `DESCRIPTIVO-NO-ADOPTA-PI-NO-RELEVA-RES-0165-A-0170` | Prohíbe interpretar esta oferta como uso activo o cierre de demanda. |

Los 32 RESULT canónicos están en `resultados.json`. Las tablas legibles son `marginales.csv`, `marginales-casos-completos.csv` y `conjunta.csv`; sus SHA-256 son, respectivamente, `82e035a90d3f1bc578cc291ec990097567ec0c26deee521d432f7f81d7e9cf20`, `06b9399a55f348ce51256c9a3e0b5b78817e6af86358b3539e54e16421be8224` y `182a3402d598bc0bf8159c667cb905ffaa34a7a70c2191b04d10464427cc1b5f`.

## Qué puede decidir dirección

Dirección puede usar las marginales para conocer la masa observada de cada categoría y la conjunta para evaluar soporte muestral, concentración y celdas vacías antes de especificar π. No identifica causalidad, psicología, conducta o cultura; tampoco decide equivalencias semánticas entre variables ENIGH y cortes del modelo. Para construir π aún faltan la adjudicación de categorías/crosswalks, la decisión sobre acceso digital, una definición acreditada de migración, la regla de tratamiento de celdas poco apoyadas o vacías, la calibración y la adopción por mesa.

## Sucesión y sello

El congelamiento inicial fue `8f614f7`. `0001` falló antes de abrir respuestas por el cableado del descriptor de input; `0002` lo sucedió y falló, también antes de abrir respuestas, por la representación mojibake del BOM de la cabecera. Ambos intentos permanecen intactos y sin resultados publicados. `0003`, congelado en `b26ad24`, es el primer procedimiento que abrió respuestas y produjo resultados. Su sello es `b2aaa04402de50705f7a516e784fb8bc4b70b914dbdb6ebdfb2abecec6222654`.

El replay dirigido posterior a la publicación reprodujo 32/32 RESULT y 3/3 inputs con `CONTEXTO=IDENTICO`. El asiento está en `forense/replay-evidencia.tsv` y su evidencia compacta en `evidencia-replay-dirigido.json`. `corrida0 registro --escribe --lote CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003` publicó una medición sellada y sus 32 RESULT; registró además los dos predecesores como superados, sin crear un uso activo para esta oferta. Una segunda proyección dejó sin diferencias las tres vistas canónicas.

## Recibo Claude requerido (sin asignar FP/ADR/NC)

- Decidir si la oferta se enlaza como antecedente descriptivo de `CORR-0076` sin cerrar `RES-0165`–`RES-0170`.
- Adjudicar el crosswalk semántico de `segsoc`, `tam_loc`, `est_socio`, `conex_inte` y `celular` hacia los cortes del motor.
- Resolver o encargar la definición documental de residencia/migración antes de cualquier medición de P3.
- Decidir el tratamiento de las ocho celdas con cero muestral y del soporte pequeño sin confundirlo con imposibilidad estructural.
- Mantener `cuenta_gen2=PENDIENTE-DE-MESA` hasta una firma de mesa; esta entrega registra una medición nueva, no una adopción.

## NO-CORRIDO / RESERVAS

- No se abrieron respuestas de `residencia`.
- No se ejecutó IPF/IPU, reponderación, imputación ni producto de marginales.
- No se consumieron ENIF 2024, ENCIG 2025, ENVIPE 2025 ni momentos HOLDOUT.
- No se modificaron `milpa/**`, π, cortes, motor, firmas, decisiones, tablero, slots ni usos activos.
- No se asignaron identificadores FP, ADR o NC, ni se hizo merge.

## CONSUMIDO

- ENIGH 2022 nueva construcción, payload `enigh2022_nc_csv`, SHA-256 `3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06`.
- Descripción de la base ENIGH 2022, SHA-256 `7b0c4e6bd36ceb9eae7cc852fce5a38dbcf4f2da6b133d35df6b1443fc76836c`.
- Nota técnica ENIGH 2022, SHA-256 `4f79f457d69c1f066d7fd319b1650f7b631f4008cb74e1046e6c644c65be0647`.
- Corpus local montado en CAJA; no se versionaron microdatos ni rutas privadas.
