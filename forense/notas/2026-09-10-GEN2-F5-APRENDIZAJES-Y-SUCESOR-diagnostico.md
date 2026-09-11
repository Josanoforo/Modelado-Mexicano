# GEN2-F5-APRENDIZAJES-Y-SUCESOR · diagnóstico técnico

Fecha: 10/sep/2026. Naturaleza: reanálisis exploratorio del panel ya conocido,
sin llamadas nuevas, sin microdatos y sin alterar capturas, snapshots, medidores
ni sellos. El M observado es exclusivamente
`snapshot-M-triada-v1_0.json`; el motor vivo se usa sólo para interpretar qué
cambió después. `CALC-TRIADA-0002` conserva su veredicto
`SIN-GANADOR-UNICO`; este acto no abre F6.

## 1. Reconciliación y localización

`F5-aprendizajes-sucesor-v1_0/analiza.py` reconstruye desde el resultado y la
extracción sellados las 14 filas, las 224 posiciones y las contribuciones al
MAE. Reproduce `U3=12` y, antes del redondeo tabular, los MAE exactos:
`L_SOLO=3.9573621816`, `L_CORPUS=3.8890257471` y `M=4.9866732398` pp. Las dos
filas fuera de U3, DIN-M-01 y TRA-M-07, permanecen visibles y no aportan al
denominador común.

La agrupación siguiente es descriptiva. Una familia comparte parámetro o
mecanismo y no aporta réplicas independientes para inferencia post-hoc.

| Familia/mecanismo | celdas (U3) | L solo | L corpus | M |
|---|---:|---:|---:|---:|
| CIV-ENVIPE | 6 (6) | 1.014777 | 0.842274 | **3.434614** |
| FAM-ENIF-apoyo | 1 (1) | **2.143271** | **2.143271** | 0.829046 |
| FAM-ENIGH-remesas | 3 (3) | 0.095671 | 0.074837 | 0.043955 |
| TRA-ENCIG | 2 (1) | 0.503850 | 0.628850 | 0.338167 |
| TRA-ENCUCI | 1 (1) | 0.199793 | 0.199793 | 0.340891 |
| DIN-ENNViH | 1 (0) | — | — | — |

Las cifras son contribuciones acumuladas al MAE de U3, en pp. En particular,
las seis filas cívicas explican 68.88% del MAE de M; no son seis confirmaciones
del mismo defecto. La única fila FAM-M-01 explica 54.17% del MAE de ambos L.
No se adjudican ganadores por familia.

## 2. Qué significa el error de M

La traza completa está en `traza-motor.tsv` y distingue fuente, ola, población,
evento y transformación.

1. **CIV no identifica un fallo aritmético del motor.** El snapshot repite
   legítimamente la calibración vigente ENVIPE 2025 (`0.294313`), pero F5 la
   enfrenta a seis olas históricas de otro estimando: M colapsa a persona,
   usa el recorte U1/U4 y códigos `{01,02,06,08}`; R usa delito y `{01,02,06}`
   sobre otro conjunto de razones válidas. #689 hizo explícitos evento,
   dominio y complemento después del snapshot. Esa mejora revela que la
   mayor parte del error observado es **uso/evaluación no alineados**, no seis
   bugs ni evidencia de que deba ajustarse `p` a los R.
2. **La repetición ENIGH sí es una regla defendible.** M usa la ola vigente
   2022; las tres celdas R son 2016/2018/2020 con el mismo hogar, evento
   `remesas>0` y ponderación. La serie ya está en el contrato vivo y las tres
   filas juntas aportan sólo 0.043955 pp al MAE de M. No amerita cambiar el
   parámetro puntual por este panel.
3. **Hay un uso ya corregido.** TRA-M-02 comparó el `0.085118` de ENCIG 2025
   con la unión ENCUCI 2020 solicitud-o-entrega. #689 agregó la transición y
   su dominio: `0.126006`, frente a `R=0.1260248695`. No cambia el snapshot,
   pero evita repetir el uso equivocado. Para TRA-M-03 y TRA-M-07, la serie
   ENCIG vigente ya contiene las olas correspondientes; falta que un
   consumidor temporal elija por contrato y no por cercanía a R.
4. **FAM-M-01 requiere una serie comparable.** M usa ENIF 2024 bajo una
   elegibilidad declarada y R usa ENIF 2018. El mismo inciso general no basta
   para asumir idéntico universo entre versiones. #691 corrigió otras reglas
   ENIF de horizonte laboral y población no trabajadora; no corrige ni valida
   retrospectivamente esta transferencia.

Como sensibilidad sobre el panel conocido, seleccionar las olas ya presentes
para ENIGH/ENCIG y la unión ENCUCI corregida reduce el MAE de M de 4.986673 a
4.263829 pp (−0.722844). Es un reanálisis descriptivo que reutiliza R; no es
confirmación independiente ni una nueva adjudicación.

## 3. Tres fuentes de incertidumbre separadas

- **Error contra el panel:** `celdas.tsv` reporta `|brazo−R|` y su aporte al
  MAE. No es por sí solo error causal del motor si los contratos difieren.
- **Variación de capturas:** el IQR por ocho respuestas está separado. La
  mediana de los IQR no vacíos es 1.75 pp en L solo y 1.00 pp en L corpus;
  FAM-M-01 llega a 8.00 pp en L solo y sólo tiene 1/8 puntos en L corpus.
- **Incertidumbre del árbitro:** los EE de R van de 0.101159 a 0.748351 pp y
  se publican por celda. El MAE/bootstrapping actual trata R como fijo y no
  integra simultáneamente EE de R ni variación de réplicas L. Por ello sus IC
  pareados no deben leerse como incertidumbre total.

## 4. Las 16 abstenciones

Las 16 respuestas L_CORPUS de DIN-M-01 y TRA-M-07 terminaron en
`ABSTENCION`. Las justificaciones son concordantes y la clasificación por
réplica queda en `abstenciones.tsv`:

- DIN recibió 108,455 caracteres, 40 extractos y 15 fuentes, hash de contenido
  `3b95e879…f860590`; ninguna era ENNViH/MxFLS ni contenía cr27 de 2002.
- TRA recibió 54,023 caracteres, 21 extractos y 9 fuentes, hash
  `765e6c71…134e04`; ninguna contenía la tabulación de ENCIG 2021 P8_3_1.
- En ambos prompts sí estaban encuesta, año, unidad, universo, evento y
  codificación verbal. El acceso al paquete funcionó; faltaron el documento
  específico y evidencia cuantitativa pertinente. El brazo se abstuvo
  correctamente ante mucho contexto temático pero no convertible.

TRA-M-07 no es el mismo objeto que NC-0153: éste pide una tasa general **por
canal sobre trámites elegibles**, mientras TRA-M-07 es P8_3_1 sobre personas
18+ con respuesta válida. No se duplica ni se cierra NC-0153. NC-0152 sigue
abierta hasta obtener cobertura nueva; este diseño no equivale a ejecutarla.

## 5. Acciones priorizadas

1. **Hacer contractual la selección por dominio, evento y ola.** Consumir la
   transición ENCUCI ya implementada y las series ENIGH/ENCIG cuando el caso
   declara año; si falta coincidencia exacta, `NO_COVERAGE`. Resultado esperado:
   evitar usos como TRA-M-02 y extrapolaciones silenciosas. Lo refuta una
   prueba prospectiva en olas retenidas donde la selección contractual no
   reduce error o rompe cobertura legítima.
2. **Cambiar la evaluación cívica antes de tocar `p`.** Construir una tarjeta
   M/R con igual unidad, recorte, códigos y ola, o excluir la pareada como no
   comparable. Resultado esperado: que el principal 3.434614 pp deje de mezclar
   desfase semántico y temporal con precisión. Lo refuta demostrar, antes de
   ver nuevos resultados, que ambos contratos ya son idénticos campo a campo.
3. **Ejecutar el sucesor de cobertura dirigido, no repetir 224 llamadas.**
   Incorporar documentos fuente específicos para DIN y TRA y comparar
   contemporáneamente contra el paquete contextual actual. Esto prueba acceso
   documental; no completa retrospectivamente el ranking de 14.

La decisión recomendada es aceptar el resultado F5 tal como está, aplicar las
correcciones de uso y mejorar la comparabilidad. No hay base para perseguir un
ganador cambiando M con los R del mismo panel.

## 6. Experimento sucesor prospectivo

**Pregunta:** ¿un paquete fuente dirigido, con documento de la encuesta,
reactivo, universo y evidencia cuantitativa del mismo estimando, convierte la
abstención en punto trazable sin inducir sustituciones entre encuestas o
universos?

**Diseño mínimo comparativo:** dos celdas × dos brazos contemporáneos
(`contextual-v2` y `fuente-dirigida-v1`) × ocho réplicas = **32 posiciones**.
Mismo modelo real acreditado, cliente, prompt, ventana de captura y orden
aleatorio congelado. Las fuentes se adquieren y congelan antes de capturar; no
se seleccionan por cercanía a R. El brazo dirigido debe contener evidencia
independiente y citable del mismo estimando; una tarjeta construida copiando R
no cuenta como confirmación.

**Éxito preregistrable:** en cada celda, al menos 6/8 respuestas dirigidas son
puntos trazables al documento correcto, cero sustituciones semánticas y una
mejora de cobertura de al menos 4/8 frente al control contemporáneo. Una
abstención es válida y aceptable cuando la fuente no permite el estimando, pero
no cuenta como punto. Sólo se reintenta error técnico, máximo dos veces; nunca
se reintenta una respuesta válida.

**Parada:** terminar tras las 32 posiciones o antes si cambia la identidad del
modelo/cliente, aparece contaminación con R, o dos fallos sistémicos consecutivos
indican autenticación/cuota. Si cualquiera de las dos celdas no alcanza el
umbral, se detiene la línea de capturas y se vuelve a adquisición/definición;
no se amplía `k` hasta obtener una cifra. Un éxito habilita una prueba posterior
en celdas nuevas, no reabre ni cambia `TRIADA-0002`.

## Artefactos

- `celdas.tsv`: R, M congelado, medianas, válidas/abstenciones, IQR, errores y
  contribuciones; incluye las dos celdas excluidas.
- `familias.tsv`: tamaños y contribuciones exploratorias por mecanismo.
- `traza-motor.tsv`: fuente/año/población/evento/transformación y diagnóstico.
- `abstenciones.tsv`: las 16 justificaciones y su clasificación.
- `figura-contribucion-mae.svg`: figura compacta por celda y brazo.
- `F5-aprendizajes-sucesor-resultados-v1_0.json`: hashes de insumos,
  reconciliación y sensibilidad rotulada.
