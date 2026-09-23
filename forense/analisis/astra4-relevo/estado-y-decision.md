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

El acto separado #1080 implementa y prueba un escritor autorizado **solo**
para `RES-0028` en `milpa/tramite.yaml`. Su diff de consumo conserva el valor
`p=0.705687`, añade la cita GEN2 y registra `uso_motor`; no releva ninguna
otra fila. #1080 fue fusionado en `main` (`f16dd3d7`) y esta rama se
sincroniza con ese commit. `tools/relevo_usos.py` calcula oferta y `tools/pines_mesa.py` valida
pines; bajar el contador de trazabilidad por un pin no cambia por sí solo
el literal que lee el motor. Los demás consumidores necesitan sus propios
escritores, guardas y acto de aplicación. La comprobación de uso efectivo
se registra por separado de la trazabilidad.

## Continuación concreta

La siguiente medición debe seleccionar hasta cuatro slots del mismo
instrumento, cotejar su estimando con cuestionario y FD, comprobar reserva,
congelar spec humana, YAML y medidor en COMMIT-1 y después ejecutar el
primer resultado en COMMIT-2. Los siete listados no son adopciones; los
cuatro conflictos ENCIG necesitan una correspondencia RESULT exacta. Las
83 filas históricas requieren propuesta individual de
`HISTÓRICO-SIN-RELEVO` o medición nueva si siguen siendo consumo efectivo.
Las 23 de catálogo requieren CALC o plan fechado condicionado a la
dependencia externa. El primer lote `CALC-RELEVO-ENCIG23-P83-0001-v1_1`
ya se congeló, midió y verificó. Los cuatro conflictos
`RES-0001/0002/0007/0008` quedaron como `NO-EQUIVALENTE-PAGO`: P8_3
registra solicitud y no sustituye pago ni normalidad. Quedan los demás
lotes y las 146 lecturas por reconciliar.

**Estado:** incumplimiento material explícito del objetivo cero; no se
solicita fusionar ni se declara U2 cerrada. Las fuentes originales de
misión y transfer están archivadas separadamente con SHA-256 en
`forense/encargos/fuentes/`.

## Reconciliación por fila, 23/sep/2026

`reconciliacion-146.tsv` cubre sin duplicados 34 motor, 6 celdas-D, 23
catálogo, 40 procedencia y 43 marco. `uso-efectivo-procedencia.tsv` verifica
por llave las 40: siete valores sellados y ocho fallbacks cargan en `B`
(uno sin magnitud); trece listas se cargan sin lectura numérica del motor;
doce condicionales son entradas consumibles pero `Theta.valor()` lanza.
`motor.correr()` da 21 veredictos de estado y ninguna magnitud calibrada.
Las 43 celdas del marco conservan propuesta histórica sin firma. Las 23 de
catálogo tienen dependencia y operación fechadas en `plan-catalogo-23.tsv`;
Los momentos de evasión y ahorro informal conservan CALC previos y reserva
consumida, sin nueva adopción.

`contratos-otros-consumidores.md` da correspondencia, guardas, diffs secos y
pruebas negativas para procedencia, catálogo y celdas-D. Los pares
`RES-0029/0030` pertenecen a la serie histórica ENNViH de acervo: el CALC
ENIF 2024 de flujo para `RES-0031/0032` no los sustituye. Los cuatro pagos
ENCIG conservan `NO-EQUIVALENTE-PAGO`. Los 146 siguen pendientes de consumo
efectivo o dictamen firmado; `RES-0028` está fuera de ese contador por un
pin de trazabilidad; su cita de consumo ya está en `main` por #1080.
