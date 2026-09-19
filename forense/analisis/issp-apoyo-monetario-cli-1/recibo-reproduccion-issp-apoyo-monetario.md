# Recibo ISSP de reproducción · CALC-ISSP2017-APOYO-MONETARIO-0001

## Identidad y separación

- Base inicial: `843a5f977e024ef5d74863e95856c763bee9e58d`.
- COMMIT-1: `4ceffdd3cce6c2249bcb4e65cb8f69c7b5594b41`, spec, código, fixture y control antes de abrir filas.
- COMMIT-1B: `f2f7a3399ce7547f52057acc8f06f1a4a45789c8`, corrección literal de los campos embebidos `doi`/`version`, realizada tras leer sólo columnas de identidad y antes de ejecutar `v26`.
- Corrida: `CALC-ISSP2017-APOYO-MONETARIO-0001--f2f7a3399ce7`.
- Sello: `41bf712273e2d2194791eac91fe13f85815f74b242b117a41d5bdb947cdc9a3f`.

## Inputs

Los cinco inputs resolvieron `COINCIDE`: cuestionario mexicano, documento mexicano de variables de contexto, ZIP DTA, ZIP SAV y evidencia versionada del codebook integrado. Los SHA-256 completos constan en `ejecucion.json`. Los contenedores integrados tienen 44,492 filas y 356 columnas; sus etiquetas seleccionadas, incluidas `v26` y `SEX`, coinciden. La selección conjunta `c_alphan=MX` y `country=484` produjo 1,002 casos.

La raíz local gitignorada es `descargas_mx: /mnt/c/Users/PC0/Descargas MX`; el corpus se leyó de forma inmutable y no se reconfiguró ni movió.

## Comandos

```bash
python3 -m unittest tests.test_issp_apoyo_monetario
python3 tools/corrida0.py spec-check CALC-ISSP2017-APOYO-MONETARIO-0001
python3 tools/corrida0.py preflight CALC-ISSP2017-APOYO-MONETARIO-0001
python3 tools/corrida0.py run CALC-ISSP2017-APOYO-MONETARIO-0001
python3 tools/corrida0.py verify CALC-ISSP2017-APOYO-MONETARIO-0001
python3 data/corrida0/CALC-ISSP2017-APOYO-MONETARIO-0001/control_independiente.py \
  --dta-zip '/mnt/c/Users/PC0/Descargas MX/ZA6980_v2-0-0.dta.zip' \
  --distribution forense/analisis/issp-apoyo-monetario-cli-1/distribucion-total-sexo.csv \
  --coverage forense/analisis/issp-apoyo-monetario-cli-1/cobertura-total-sexo.csv \
  --contrast forense/analisis/issp-apoyo-monetario-cli-1/contraste-mujeres-menos-hombres.csv \
  --output forense/analisis/issp-apoyo-monetario-cli-1/control-independiente-issp-apoyo-monetario.json
```

El control separado terminó `CONTROL-INDEPENDIENTE-OK`: delta máximo de masa 0 y delta máximo de punto `4.86e-13`, con particiones, reconciliaciones y reconstrucción total verdaderas.

## Estado de publicación

La corrida y sus tablas están selladas en esta rama. No se modificaron F6, M, L, motor, marcador, adopción, crosswalk, theta, canon, firmas ni NC-0161/0162. No se asignó clasificación contable ni adopción. Los asientos globales de replay/vistas quedan pendientes de la integración secuencial indicada por el lanzamiento y de una decisión posterior explícita; el PR entrega la operación completa sin fusionarla.
