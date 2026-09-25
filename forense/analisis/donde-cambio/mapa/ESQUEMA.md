# Mapa de series · esquema y regla de par (COMMIT-1b, antes de leer valores)

Desarrolla `forense/prereg-caja/DONDE-CAMBIO-spec-v1_0.md` §1–§2 (sellada en `9aea5a09`); no
cambia vocabulario ni umbral. Un fragmento TSV por familia en este directorio, generado por un
script reproducible en `tools/series/mapa_<familia>.py`. **Sólo ids, nunca valores.**

Columnas (tab, UTF-8, una fila por serie × ola, ordenadas por `serie_id`, `ola`):

`serie_id · instrumento · dominio · conducta · conducta_texto · eje · segmento · unidad · ola ·
calc · result_p · result_lo · result_hi · par_con_anterior · cita_par · marca_2020 · nota`

- `serie_id` = `<INST>-<CONDUCTA>-<EJE>-<SEGMENTO>` en mayúsculas ASCII, guiones.
- `eje`/`segmento`: `NACIONAL`/`TOTAL` cuando no hay eje.
- `result_*`: ids exactos que existen como llave en `data/corrida0/<calc>/resultados.json`
  (se verifica por llave, sin leer el valor). `result_lo/hi` vacíos si la ola no tiene IC.
- `par_con_anterior` para la primera ola: `PRIMERA`.

Regla de par (spec §2), derivada de las tablas `data/*-comparabilidad-texto-v*.tsv`, que
dictaminan cada ola contra una **ola ancla**:

- las dos olas del par con veredicto MISMO-INSTRUMENTO o CAMBIO-MENOR contra el ancla (el ancla
  misma cuenta como MISMO) → `COMPARABLE`;
- alguna de las dos con CAMBIO-DE-INSTRUMENTO para esa conducta/objeto → `CAMBIO-DOCUMENTADO`;
- la tabla dice que el constructo no se construye/no es el mismo → `NO-COMPARABLE`;
- sin fila para la conducta o la ola → `NO-DOCUMENTADO`.

Si la conducta combina varios objetos (desenlace + eje), el par toma el **peor** estado de sus
objetos (orden: NO-COMPARABLE > NO-DOCUMENTADO > CAMBIO-DOCUMENTADO > COMPARABLE).
Una spec sellada de serie que dictamine por texto la comparabilidad (p. ej. ENVIPE-SERIE-COMPLETA,
ENOE-PISOS/ENOE-PERSISTENCIA por era, ENIF-FINTECH `NO-ESTIMABLE-RUPTURA-ESTRUCTURAL`) es fuente
equivalente; `cita_par` nombra archivo y fila/sección.

`marca_2020` = `SI` si alguna ola del par se levantó o refiere a 2020.
