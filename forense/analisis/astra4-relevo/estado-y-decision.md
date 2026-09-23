# ASTRA4-U2 · estado operativo y decisión solicitada

Fecha de corte: 23/sep/2026. Rama `codex/astra4-relevo-1`. Este documento
no adopta ninguna cifra ni altera el consumo del motor.

## CAJA y censo

`data/raw` es un enlace local a `/home/pc0/mm-corpus/raw`, igual que en el
checkout principal. `data/raices.local.yaml` declara `data_raw` y
`descargas_mx`. `python3 tools/entorno.py --sonda-red` devolvió
`acceso_corpus.montado=SI` y 438 entradas examinadas. El enlace y la
configuración son locales y están ignorados por Git. Antes de abrir un
payload para un CALC nuevo aún corresponde comprobar su ID de manifiesto,
hash, reserva, cuestionario, FD, códigos, peso y universo. Configurar CAJA
no equivale a autorizar una apertura particular.

`python3 tools/corrida0.py status` y `python3 tools/relevo_usos.py --json`
rederivan **146 lecturas legacy activas**: 34 motor (28 conductas en
`milpa/tramite.yaml` y 6 referencias de `milpa/src/celdas.py`), 6 YAML
de celdas-D, 23 catálogo, 40 procedencia y 43 marco. La tabla
`inventario-operativo.tsv` registra cada llave, valor actual, candidato,
veredicto, vía y operación siguiente; `inventario.py` la regenera. La
clasificación operativa es 83 históricos por dictaminar, 23 catálogo por
medir o calendarizar, 20 sin CALC candidato, 9 con candidato no adoptable o
vetado, 7 listados para mesa y 4 con conflicto entre CALC posibles. Es una
clasificación de trabajo, no una afirmación de identidad de estimandos.

## Consumo efectivo

No hay en el árbol un comando autorizado que reescriba el consumidor
`milpa/`. `tools/relevo_usos.py` calcula oferta y `tools/pines_mesa.py`
valida pines; `data/corrida0/pines-de-mesa.tsv` puede bajar el contador de
trazabilidad sin reemplazar el literal que lee el motor. El contrato
`contrato-escritor-consumo.md` contiene entrada, guardas, destinos,
ejemplo de diff y prueba negativa. La decisión de mesa necesaria es
**autorizar y nombrar un escritor por consumidor** bajo ese contrato,
incluido un adaptador propio para celdas-D. Hasta entonces, las 40 lecturas
de motor y celdas-D siguen activas; informar cero sería incorrecto.

## Continuación concreta

La siguiente medición debe seleccionar hasta cuatro slots del mismo
instrumento, cotejar su estimando con cuestionario y FD, comprobar reserva,
congelar spec humana, YAML y medidor en COMMIT-1 y después ejecutar el
primer resultado en COMMIT-2. Los siete listados no son adopciones; los
cuatro conflictos ENCIG necesitan una correspondencia RESULT exacta. Las
83 filas históricas requieren propuesta individual de
`HISTÓRICO-SIN-RELEVO` o medición nueva si siguen siendo consumo efectivo.
Las 23 de catálogo requieren CALC o plan fechado condicionado a la
dependencia externa. Ninguna de esas operaciones está ejecutada en este
corte.

**Estado:** incumplimiento material explícito del objetivo cero; no se
solicita fusionar ni se declara U2 cerrada. Las fuentes originales de
misión y transfer están archivadas separadamente con SHA-256 en
`forense/encargos/fuentes/`.
