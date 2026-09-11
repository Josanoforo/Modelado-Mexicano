# ACTO: GEN2-FUENTES-FINANCIERAS-CONTINUACION-EFECTIVA

ENTORNO: CAJA  
EJECUTOR: Codex CLI con corpus local y acceso a red.  
REPOSITORIO: Josanoforo/Modelado-Mexicano

## Objetivo

Continuar #717 desde sus barreras reales:

A. Obtener historia mensual oficial de IMOR por producto, o una publicación
oficial equivalente con su alcance explícito.

B. Obtener evidencia pertinente del lado consumidor-deudor para N34, con
causa, población y denominador interpretables.

Entregar datos utilizables cuando sean accesibles. No repetir el inventario de
los 29 CSV ni la identificación de ENCRIGE ya resueltos.

## Autoridad y operación

Se autoriza búsqueda pública dirigida, descarga por vías disponibles y
autorizadas, extracción descriptiva, incorporación al corpus/registro,
documentación, commits, push y PR. No se autorizan compras, suplantación,
aceptación de acuerdos institucionales, envío de mensajes o formularios
externos ni compromisos en nombre de Jonás. Cualquier actuación indispensable
del titular debe quedar concreta y lista para su intervención.

Leer `AGENTS.md`; reportar worktree, rama, HEAD, estado y corpus; resolver la
configuración local antes de extraer; usar worktree propio y escritores
canónicos.

## Antecedentes

Leer la nota `GEN2-CNBV-CONDUSEF-FUENTES-Y-SERIES` de #717,
`tools/extrae_fuentes_financieras.py`, `data/fuentes-financieras-20/`, el
manifiesto y las filas afectadas, y los consumidores R1.6 y N34/R1.7. Usar
expedientes de #715 sólo si resuelven un acceso de este alcance.

El R16 obtenido contiene sólo diciembre de 2021 y su macro depende de
infraestructura interna. Los conteos CONDUSEF no identifican clientes únicos
ni prevalencia; ENCRIGE observa empresas acreedoras/contratantes.

## Fases

1. Fijar antes de descargar dos tarjetas: para IMOR, institución/universo,
   producto, frecuencia, periodo, numerador, denominador, escala y cambios de
   definición; para N34, consumidor-deudor, daño o causa, producto, población,
   periodo y denominador. Separar contexto, conteo administrativo y tasa
   poblacional.
2. Abrir rutas nuevas y concretas. Para CNBV, buscar exportaciones históricas,
   archivos estáticos o publicaciones oficiales equivalentes sin hacer pasar
   un agregado por IMOR por producto. Para N34, priorizar tablas o microdatos
   del consumidor con causa, producto y exposición y contrastar cuestionario y
   diccionario. Descargar datos y documentación; comprobar fallos y
   alternativas; respetar autenticación y permisos.
3. Para lo obtenido, registrar procedencia, consulta, bytes y hash; extraer
   periodo, unidad, escala y faltantes; preservar canales y cambios
   metodológicos; comprobar duplicados, denominadores y continuidad sin
   interpolar ni convertir vacíos a cero. Entregar mapa objeto → estimando →
   consumidor → uso → límite → siguiente cálculo.
4. Actualizar manifiesto, registro y proyección por identidad estable. Separar
   documentación, datos, extracción, satisfacción científica y adopción. Si
   queda acceso externo indispensable, entregar receta exacta y reutilizar un
   expediente existente cuando corresponda.
5. Entregar PR con objetos, corpus, tablas reproducibles, límites, registro,
   obligaciones, residual y siguiente acción científica. No cerrar la serie
   con la foto 2021; no cerrar N34 con empresa o quejas; no declarar tasa sin
   denominador.

No se modifica motor, cron ni evaluación. Sólo se concilian las filas propias
al integrar otros encargos. La fusión corresponde a Jonás.

## A.8 · medición previa comprobada antes de fijar estados

```text
$ python3 tools/ya_medido.py dinero.credito.scoring_alternativo
resuelto por canon: dinero.credito.scoring_alternativo -> R1.6
milpa/tramite.yaml: sin apariciones
milpa/tramite-ola5-propuesta-v0.yaml: sin apariciones
data/corrida0: sin apariciones
canon/modelo-decision-v4_0.md §7: R1.6, tier [MEDIA], medido No
NUNCA-MEDIDA

$ python3 tools/ya_medido.py dinero.credito.baja_friccion_usura_dano_downstream
resuelto por canon: dinero.credito.baja_friccion_usura_dano_downstream -> R1.7
milpa/tramite.yaml: sin apariciones
milpa/tramite-ola5-propuesta-v0.yaml: sin apariciones
data/corrida0: sin apariciones
canon/modelo-decision-v4_0.md §7: R1.7, tier [MEDIA], medido No
NUNCA-MEDIDA
```

Este acto incorpora y extrae evidencia descriptiva, pero no crea una medición
sellada ni cambia esos estados de adopción.

## NO-CORRIDO / RESERVAS

- `NC-0163` cierra mediante la publicación oficial equivalente de Banxico; la
  exportación R16 CNBV exacta queda como mejora opcional, no como acceso
  indispensable para el objeto A.
- `NC-0164` permanece abierta sólo para el mecanismo que ENSAFI no enlaza:
  producto exacto, exposición/CAT/BNPL o fricción y daño causal en la misma
  unidad. No se creó spec, CALC ni adopción sin decisión de mesa.

## CONSUMIDO

Ejecutado por **[PR #723](https://github.com/Josanoforo/Modelado-Mexicano/pull/723)**,
rama `acto/gen2-fuentes-financieras-continuacion-efectiva`, HEAD al abrir el PR
`a36cc07e311f38592f99074fd353597de7a631c0`, contra
`origin/main=70c64d9ead92384ece0eaf18cbfb53372bb88a74`. Entrega la serie oficial
equivalente Banxico, la evidencia ENSAFI consumidor-deudor, nueve tablas
reproducibles y la conciliación canónica. `ADR-481`; `NC-0163` cierra y
`NC-0164` conserva el residual causal. Renumerado a `ADR-481` al integrar
`origin/main=5f4bfeac` con PR #720/#722 ya fusionados. Línea base verde sin entradas nuevas;
la fusión corresponde a Jonás.
