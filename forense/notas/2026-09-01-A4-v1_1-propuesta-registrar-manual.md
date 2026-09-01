# Propuesta A4 v1.1 — registrar una descarga manual contra el registro

`ACTO MAESTRA33-A5 · RECONCILIA-ADQUISICION-CON-CURADOR`, 1/sep/2026, P4.
Redactado como sucesor, **no** aplicado — mesa decide si canoniza esta
enmienda a `instrucciones-proyecto-v2_12.md` A.4 (vocabulario
EXISTE-SATISFACE/EXISTE-NO-SATISFACE/NO-ENCONTRADO/NO-ACCESIBLE) o si la
deja como protocolo aparte.

## Motivación

Este acto (P3) convirtió `data/cola-adquisicion-v1_0.tsv` en vista
regenerada desde `data/curacion-registro/cola-adquisicion-registro.tsv`.
`/adquiere` ya escribe contra el registro (adquisición programática). La
pieza que falta: cuando mesa o un operador humano descarga algo **a mano**
(fuera de `/adquiere`, p. ej. un portal con muro de credencial que la
receta de `PAQUETE-RECETAS` resolvió), hoy no hay protocolo escrito que
diga "regístralo aquí" apuntando al registro nuevo — solo `tests/
manifiesto.py --registra` para el payload en sí (Dominio 1, ya
EXISTE-SATISFACE, sin cambio).

## Texto propuesto (A4 v1.1)

> **A4 v1.1 — registrar una descarga manual.** Tras `tests/manifiesto.py
> --registra` (payload → `manifiesto.yaml`, obligatorio, sin excepción),
> localiza la fila de `data/curacion-registro/cola-adquisicion-registro.tsv`
> cuya `fuente_canonica` corresponda (si no existe fila, créala con
> `origen=REGISTRO_MANUAL_A4V1_1:<fecha>`) y actualiza `estado_A4A5=OBTENIDO`,
> `ids_manifiesto=<id(s) nuevos>`, `nota` con fecha, quién descargó y el
> comando de `manifiesto.py` usado. Cierra corriendo
> `python3 tools/vista_cola_adquisicion.py` para que
> `data/cola-adquisicion-v1_0.tsv` quede al día — la vista es generada
> (`MAESTRA33-A5`), nunca se edita a mano. El vocabulario de estado
> (`OBTENIDO`/`PENDIENTE`/`NO-ACCESIBLE`/`NO-OBTENIDO-POR-ESTE-AGENTE(N)`)
> es el de la cola, no el de `A.4` (`EXISTE-SATISFACE`/...) — los dos
> vocabularios miden cosas distintas (adquisición de fila vs. satisfacción
> de una celda) y no se traducen uno al otro sin una decisión explícita.

No se aplica en este acto: es texto listo para que mesa lo firme, no una
edición de `instrucciones-proyecto-v2_12.md` (fuera del perímetro de
`MAESTRA33-A5`, que solo cubre `INFRAESTRUCTURA-v1_0.md`).
