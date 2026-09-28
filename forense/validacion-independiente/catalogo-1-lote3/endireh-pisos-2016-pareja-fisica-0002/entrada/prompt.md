Eres una sesión de reconstrucción independiente. No tienes historial ni memoria, y no debes buscarlos. Tu único insumo es el directorio `./paquete/`, de solo lectura. Escribes únicamente en `./salida/`.

## Objetivo

Recalcula el punto y el IC95 de cada una de las 92 llaves de `paquete/estimandos.tsv`. Hazlo implementando tú mismo el método descrito en `paquete/metodo.md`, con ayuda de los documentos humanos del paquete (cuestionarios y FD), en Python 3 con numpy y pandas. No existe código previo que puedas consultar, y no debes buscarlo.

## Archivos del paquete, y solo estos

- `paquete/metodo.md`: especificación humana del método (universo, recodificación, ejes, ventanas, diseño muestral y remuestreo).
- `paquete/estimandos.tsv`: las 92 llaves, con las columnas `llave, calc, result_id, celda, instrumento, ola, conducta, eje, segmento, unidad, naturaleza_ic, ventana`. `ventana` vale `vida` (pregunta 13.1) o `desde_octubre_2015` (pregunta 13.3).
- `paquete/esquema.json`, `paquete/manifiesto.json`, `paquete/insumos.json`, `paquete/encargo.md`, `paquete/tolerancia.json`: identidad y metadatos del paquete.
- `paquete/endireh2016_cuestionario_{a,b,c}_pdf-semantica.json`: texto extraído de los cuestionarios.
- `paquete/fd-endireh2016.xlsx`, `paquete/fd2016-TB_SEC_XIII.json`, `paquete/fd2016-TSDem.json`: descriptor de archivos.
- `paquete/datos/TB_SEC_XIII.csv` y `paquete/datos/TSDem.csv`: los dos miembros del ZIP `bd_mujeres_endireh2016_sitioinegi_csv.zip` (sha256 del ZIP `02c06ab73a53942ddb575e3e35d8c1dd775406277b74e0605735e3eced4e6f10`), extraídos byte a byte. El resto del ZIP no se entrega.
- `paquete/CONTRATO-v3.md`: formato obligatorio de tu salida.

## Límites de acceso (autorización delimitada)

Del microdato puedes leer la fila de encabezados completa, y de las filas solo estas columnas; en pandas, usa `usecols`:
- `TB_SEC_XIII.csv`: las columnas identificadoras de vínculo (`ID_VIV`, `ID_HOG`, `ID_MUJ`, `UPM`, `VIV_SEL`, `HOGAR`, `N_REN`, las que existan), `P13_1_1`…`P13_1_9`, `P13_3_1`…`P13_3_9`, `FAC_MUJ`, `EST_DIS`, `UPM_DIS`, `DOMINIO`, `CVE_ENT` y `T_INSTRUM`.
- `TSDem.csv`: las columnas identificadoras de vínculo, `EDAD`, `NIV` y `SEXO`.

Si el método exige una columna que no está en esta lista, no la leas: marca las llaves afectadas con `BLOQUEADO-POR-ACCESO` y escribe el `motivo`. No imprimas filas de microdato en tu salida de consola; los conteos y agregados sí se pueden imprimir. No uses la red ni leas nada fuera de `./paquete/`.

## Qué entregar en `./salida/`

1. `salida/resultado.json`: exactamente el documento de `CONTRATO-v3.md`.
   - `version` vale `3`.
   - `identidad` vale exactamente `{"paquete": "endireh-pisos-2016-pareja-fisica-0002", "version_entrada": "c1-ventana-v1", "sha256_entrada": "6ce9c8a5fdcef8473e666d9fae5b1851c31f899b06f67075f1a7fbe37222a555"}`.
   - `filas` lleva una fila por cada una de las 92 llaves, con `llave` y `unidad` copiadas literales de `estimandos.tsv`.
   - Si hay estimación, la fila lleva `estado: "RECONSTRUIDO"`, `punto`, y `estado_ic: "CALCULADO"` con `ic95_inf` e `ic95_sup`. Si no, usa el estado del contrato que corresponda, con `motivo`.
   - Números: strings `repr(float(x))`, sin redondear.
   - Reporta punto e IC de toda celda estimable aunque no cumpla la regla de publicabilidad de `metodo.md`. No suprimas celdas en este archivo.
2. `salida/diagnostico.json`: por llave, `n` de respuesta conocida, número de UPM con casos, ancho del IC, CV y si la celda es publicable según `metodo.md`. Añade las decisiones de implementación que tomaste donde la spec admitía más de una lectura, cada una con la frase de la spec que la motiva.
3. `salida/codigo/`: todo el código que escribiste. `python3 salida/codigo/reconstruye.py`, ejecutado desde el directorio de trabajo, debe regenerar `resultado.json` y `diagnostico.json` desde `paquete/`.
4. `salida/entorno.txt`: versiones de python, numpy y pandas, y la salida de `uname -a`.
5. `salida/archivos-leidos.txt`: cada ruta que abriste, una por línea, incluidos los documentos.
6. `salida/insuficiencias.md`: todo lo que la spec humana no alcanzó a fijar, por llave o por grupo de llaves. Escribe «Ninguna.» si no hubo nada.

## Reglas

- Si falta método, acceso o un dato, informa el faltante sin adivinar. Usa `NO-RECALCULABLE-DESDE-SPEC` con `motivo` cuando la spec humana no baste.
- El primer resultado completo que produzca tu código es el que se entrega. No ajustes el método para acercarte a ningún valor esperado: no tienes ninguno, y no debes buscarlo.
- Al terminar, calcula el sha256 de cada archivo de `salida/`, escríbelos en `salida/SELLO.txt` y no modifiques nada después.
- La última línea de tu respuesta final es `RECONSTRUCCION-TERMINADA sha256(resultado.json)=<hex>`.
