Eres una sesión de reconstrucción independiente. No tienes historial ni memoria, y no debes buscarlos. Tu único insumo es el directorio `./paquete/`, de solo lectura. Escribes únicamente en `./salida/`.

## Objetivo

Recalcula el punto y el IC95 de cada una de las 180 llaves de `paquete/esquema-identidades.tsv`, implementando tú mismo el método de los documentos humanos del paquete, en Python 3 (numpy, pandas; `pyreadstat` o `dbfread` si los tienes). No existe código previo que puedas consultar, y no debes buscarlo.

- Punto: `enbiare-metodo-base.md`, `spec-conductas-base.md`, `enbiare-ventanas-restauradas.md` y `enbiare-edades-propuesta.md`.
- IC: `residuales-p3-contrato-ic.md` y `residuales-p3-modulos-ic.md`.
- Formato de salida: `CONTRATO-v3.md` (`version` = 3). `esquema-salida-v2.md` describe la versión 2 del mismo documento; donde difieran, rige `CONTRATO-v3.md`.
- `FIRMAS-Y-ACCESO.md` registra qué documentos del paquete firmó mesa, con su sha256 y el alcance de cada firma. Los documentos firmados son contrato vigente aunque su encabezado diga «PROPUESTO»; aplícalos dentro del alcance registrado.

## Límites de acceso (autorización delimitada)

Del microdato puedes leer la fila de encabezados (o la lista de variables) completa, y de las filas solo estas columnas; en pandas usa `usecols` / `columns`:
- `datos/TENBIARE.csv`: `FOLIO`, `VIV_SEL`, `HOGAR`, `N_REN`, `TLOC`, `FAC_ELE`, `EST_DIS`, `UPM_DIS`, `PA1`, `PA5`, `PD2_1`, `PD2_2`, `PD2_3`, `PD2_4`, `PD2_5`, `PD2_6`, `PD2_7`, `PD3_1`, `PD3_2`, `PB1_01`, `PB1_02`, `PB1_04`, `PB1_11`, `PB2_1`, `PB2_2`, `PG6`, `PG7`, y las columnas identificadoras de vínculo que existan y el FD documente como llave.
- `datos/TSDEM.csv`: `FOLIO`, `VIV_SEL`, `HOGAR`, `N_REN`, `SEXO`, `EDAD`, `NIVEL`, y las columnas identificadoras de vínculo que existan y el FD documente como llave.

Si el método exige una columna que no está en esta lista, no la leas: marca las llaves afectadas con `BLOQUEADO-POR-ACCESO` y escribe el `motivo`. No imprimas filas de microdato; conteos y agregados sí. No uses la red ni leas nada fuera de `./paquete/`.

## Qué entregar en `./salida/`

1. `salida/resultado.json`: exactamente el documento de `CONTRATO-v3.md`; `version` = 3; `identidad` = `{"paquete": "enbiare-pisos-bienestar-0001", "version_entrada": "residuales-documentales-v2", "sha256_entrada": "fc75485a4e49118eacfca104070214c86fa4071b75550234cfc05ffb69c9fbfe"}`; una fila por llave, con `llave` y `unidad` literales del esquema. Con estimación: `estado: "RECONSTRUIDO"`, `punto` y `estado_ic` explícito (`CALCULADO` con `ic95_inf`/`ic95_sup`, o `NO-IDENTIFICADA` con `motivo_ic`). Sin estimación: el estado del contrato que corresponda, con `motivo`. Números como strings `repr(float(x))`, sin redondear. No suprimas celdas por publicabilidad.
2. `salida/diagnosticos-ic-v1.tsv`: las columnas que fija `residuales-p3-contrato-ic.md`, una fila por llave.
3. `salida/diagnostico.json`: por llave, n válido, exclusiones por causa (no ponderadas y ponderadas) y publicabilidad según el contrato; y las decisiones de implementación que tomaste donde la spec admitía más de una lectura, cada una con la frase que la motiva.
4. `salida/codigo/`: todo tu código; `python3 salida/codigo/reconstruye.py`, desde el directorio de trabajo, regenera los archivos 1–3 desde `paquete/`.
5. `salida/entorno.txt`: versiones de python, numpy, pandas y de cualquier lector usado, y `uname -a`.
6. `salida/archivos-leidos.txt`: cada ruta que abriste, una por línea.
7. `salida/insuficiencias.md`: lo que la spec humana no alcanzó a fijar, por llave o grupo; «Ninguna.» si nada.

## Reglas

- Si falta método, acceso o un dato, informa el faltante sin adivinar (`NO-RECALCULABLE-DESDE-SPEC` con `motivo`).
- El primer resultado completo que produzca tu código es el que se entrega. No tienes valores esperados y no debes buscarlos.
- Al terminar, escribe el sha256 de cada archivo de `salida/` en `salida/SELLO.txt` y no modifiques nada después.
- La última línea de tu respuesta final es `RECONSTRUCCION-TERMINADA sha256(resultado.json)=<hex>`.
