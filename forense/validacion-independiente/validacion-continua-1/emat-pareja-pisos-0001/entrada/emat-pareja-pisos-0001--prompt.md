Eres una sesión de reconstrucción independiente. No tienes historial ni memoria, y no debes buscarlos. Tu único insumo es el directorio `./paquete/`, de solo lectura. Escribes únicamente en `./salida/`.

## Objetivo

Recalcula el punto y, donde la spec lo defina, el IC95 de cada una de las 3304 llaves de `paquete/esquema-identidades.tsv`. Implementa tú mismo el método de la spec humana `paquete/docs/spec-humana.md`, apoyándote en la documentación de `paquete/docs/`, en Python 3 (numpy, pandas). Para leer `.sav` o `.dbf` tienes `pyreadstat` y `dbfread` en `paquete/lib/` (`sys.path.insert(0, "paquete/lib")`); son lectores de terceros, sin método del programa. `.dta` se lee con `pandas.read_stata`. La spec menciona funciones de un código previo: no existe en el paquete, no debes buscarlo, y su comportamiento solo vale en la medida en que la spec lo describe en prosa. Las columnas `conducta`, `eje`, `segmento` y `ola` del esquema dicen qué estima cada llave.

- Formato de salida: `CONTRATO-v3.md` (`version` = 3).
- `FIRMAS-Y-ACCESO.md` registra qué firmó mesa y el alcance de tu acceso.

## Límites de acceso (autorización delimitada)

Del microdato puedes leer la fila de encabezados (o la lista de variables) completa, y de las filas solo estas columnas; en pandas usa `usecols` / `columns`:
- `datos/matri10.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri11.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri12.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri13.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri14.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri18.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri19.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri15.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri16.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri17.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri20.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri21.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri22.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.
- `datos/matri23.dbf`: `ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1`, `SEXO_CON2`, `EDAD_CON1`, `EDAD_CON2`, `CONACTCON1`, `CONACTCON2`, `ESCOL_CON1`, `ESCOL_CON2`.

Si el método exige una columna que no está en esta lista, no la leas: marca las llaves afectadas con `BLOQUEADO-POR-ACCESO` y escribe el `motivo`. No imprimas filas de microdato; conteos y agregados sí. No uses la red ni leas nada fuera de `./paquete/`.

## Qué entregar en `./salida/`

1. `salida/resultado.json`: exactamente el documento de `CONTRATO-v3.md`; `version` = 3; `identidad` = `{"paquete": "emat-pareja-pisos-0001", "version_entrada": "validacion-continua-1", "sha256_entrada": "ce83abdc757dce2c6f0d83afc8dc41a5b33a30e3fee516d5dabef7caf2cf7a6e"}`; una fila por llave del esquema, con `llave` y `unidad` literales. Con estimación: `estado: "RECONSTRUIDO"`, `punto` y `estado_ic` explícito (`CALCULADO` con `ic95_inf`/`ic95_sup`, `SIN-IC` si la spec no define IC para esa llave, o `NO-IDENTIFICADA` con `motivo_ic`). Sin estimación: el estado del contrato que corresponda, con `motivo`. Números como strings `repr(float(x))`, sin redondear. No suprimas celdas por publicabilidad.
2. `salida/diagnostico.json`: por llave, n válido y exclusiones por causa; y las decisiones de implementación que tomaste donde la spec admitía más de una lectura, cada una con la frase que la motiva.
3. `salida/codigo/`: todo tu código; `python3 salida/codigo/reconstruye.py`, desde el directorio de trabajo, regenera los archivos 1–2 desde `paquete/`.
4. `salida/entorno.txt`: versiones de python, numpy, pandas y de cualquier lector usado, y `uname -a`.
5. `salida/archivos-leidos.txt`: cada ruta que abriste, una por línea.
6. `salida/insuficiencias.md`: lo que la spec humana no alcanzó a fijar, por llave o grupo; «Ninguna.» si nada.

## Reglas

- Si falta método, acceso o un dato, informa el faltante sin adivinar (`NO-RECALCULABLE-DESDE-SPEC` con `motivo`).
- El primer resultado completo que produzca tu código es el que se entrega. No tienes valores esperados y no debes buscarlos.
- Trabaja por lotes si el esquema es grande; no dejes llaves sin fila.
- Al terminar, escribe el sha256 de cada archivo de `salida/` en `salida/SELLO.txt` y no modifiques nada después.
- La última línea de tu respuesta final es `RECONSTRUCCION-TERMINADA sha256(resultado.json)=<hex>`.
