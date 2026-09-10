# F5 completa · contrato prospectivo v1.0

**Acto:** `GEN2-F5-COMPLETA`. **Fecha:** 2026-09-10. **Base:**
`486eda19944a94d978791eb423559144de98d16b`. Esta spec y el plan de 224
posiciones se comprometen antes de la primera respuesta nueva.

## 1. Pregunta y objetos congelados

La pregunta primaria es **uso documental/operacional** dentro de las 14
celdas de `L-spec-v1_4.json`; transferencia es secundaria. Los estimandos
humanos proceden de `L-estimandos-v1_4.tsv`. M es el snapshot ya sellado en
`snapshot-M-triada-v1_0.json`; R es la colección de 14 resultados citada por
las filas vigentes de `codificacion-R-v1_2.tsv`. Ninguno se modifica.

Las capturas v1.3 pidieron `--model opus`, pero las 224 tienen
`modelo_real=null`: el cliente 2.1.267 no registró la versión resuelta. Por
ello no se acredita comparabilidad de FAM-M-05/06/07 y se congela una corrida
íntegramente nueva: 14 celdas × 2 brazos × 8 réplicas = **224 posiciones**.

## 2. Tratamientos

- `L-solo`: pregunta v1.4 y contrato de salida, sin corpus.
- `L+corpus`: exactamente lo anterior más el paquete de la celda reconstruido
  desde `paquete-corpus-F5-v2_0/manifiesto.json`.

El paquete v2.0 selecciona secciones por una regla temática determinista,
anterior a resultados, y hereda las exclusiones temporales del v1.0. No lee
R, M, capturas ni errores. Registra fuente, hash, encabezado, líneas, razón de
inclusión, contenido entregado por hash y tamaño. No hay truncamiento. Los
conteos de caracteres/bytes/palabras son diagnósticos, no tokens exactos; la
aceptación del mayor paquete se comprueba con una sonda de transporte que no
es réplica ni produce una estimación.

El contexto no contiene R ni resultados TRIADA. Una celda sin evidencia
directa conserva esa etiqueta: contexto legible no equivale a cifra presente.

## 3. Cliente, prompt y orden

Cliente: Claude Code CLI autenticado por `claude.ai`, sin API de pago. Modelo
solicitado: alias fijo `opus`; herramientas deshabilitadas; `--max-turns 1`;
prompt por stdin; system prompt fijo. Cada captura registra versión del
cliente, alias solicitado y todo identificador que el sobre JSON reporte en
`model`/`modelUsage`. Un cambio de cliente o de identidad de posición aborta
la reanudación; no se mezclan versiones silenciosamente.

El orden es una permutación determinista con semilla `20260910` sobre las 224
tuplas. `k=8`. Cada respuesta debe terminar con una de estas líneas:

```text
ESTIMACION_PUNTUAL=<número entre 0 y 100>%
ABSTENCION
```

Se permiten como máximo dos reintentos por **fallo técnico** (timeout, salida
CLI no JSON o retorno no cero). Una respuesta válida, incluida abstención, no
se reintenta. La captura conserva el sobre original, stdout, stderr técnico,
timestamps, intentos e identidad/hash del prompt y paquete.

## 4. Extracción, faltantes y cálculo

La regla prospectiva lee sólo la última línea no vacía de `texto_crudo`:

- `ESTIMACION_PUNTUAL=N%`, con `0 <= N <= 100`, es `VALIDA` y se normaliza a
  proporción `N/100`;
- `ABSTENCION` es `ABSTENCION`;
- cualquier otra terminación es `MALFORMADA`;
- un fallo técnico agotado es `ERROR_TECNICO`.

No se rellena ningún faltante con cero. Por celda y brazo se informa número
programado, ejecutado, válido, abstención, malformado, error técnico y posible
contaminación. El punto L de una celda/brazo es la mediana de réplicas válidas;
si no hay ninguna, queda ausente.

El universo común `U3` contiene sólo celdas con punto de `L-solo`,
`L+corpus`, M y R. Sobre ese mismo U3 se calcula el MAE en puntos porcentuales
de cada brazo frente a R. Se informan además denominadores sobre las 14 celdas.
Bootstrap pareado por celda: 10,000 réplicas, semilla heredada `42`, mismos
índices para los tres brazos; intervalo percentil 95% de diferencias de MAE.
Los reportes por familia son diagnósticos, sin IC si sólo hay una celda.

## 5. Adjudicación y tolerancia D02

Margen práctico: `δ=0.5 pp = 0.005` en proporción. Tolerancia numérica:
`tol=1e-9 pp`, derivada del máximo de redondeo de operaciones binarias sobre
valores publicados a seis o más decimales; es ocho órdenes menor que δ y no
lo sustituye.

Para una diferencia pareada `d = MAE(A)-MAE(B)` en pp:

- `EMPATE-PRACTICO` si todo el IC está dentro de `[-δ-tol, +δ+tol]`;
- `A-DOMINA` si el límite superior es `< -δ-tol`;
- `B-DOMINA` si el límite inferior es `> +δ+tol`;
- en otro caso, `INCONCLUSO` (falta de dominancia).

Se prueban borde exacto, residuo numérico, diferencia material y simetría.
La salida exhaustiva distingue empate práctico, falta de dominancia y
cobertura insuficiente. Se conserva la escala global de
`F5-contrato-triada-spec-v1_1.md`: un ganador necesita ganar sus dos pareadas
y no tener menor cobertura que sus rivales; `U3` vacío o un control roto da
`NO-ADJUDICABLE-POR-CONTROL`, y los demás casos dan `SIN-GANADOR-UNICO`.

## 6. Parada y alcance

Ante autenticación/cuota sistémica se conserva el avance y se paran llamadas
inútiles. La conclusión sólo cubre este marco y los datos observados; no prueba
generalización nacional ni autoriza adopción al motor o F6. Un ranking puntual
no es una decisión de adopción.
