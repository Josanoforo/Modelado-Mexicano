# ACTO GEN2-ENIF-POBLACION-Y-ADOPCION · cierre

Fecha: 10/sep/2026. Entorno: CAJA (Ubuntu/WSL2), corpus montado. Rama:
`acto/gen2-enif-poblacion`. Encargo archivado verbatim en
`forense/encargos/2026-09-10-GEN2-ENIF-POBLACION-Y-ADOPCION.md` (sha256
`00a44e57d3b313e902cb24b783aa9f2ee11812e00d2b2e662c44ef190b8a75bc`).

## 1. Resultado útil

La decisión D04 se puede adoptar sin recalcular: `CALC-ENIF-0001` ya mide
exactamente A/A. Entre personas que trabajan sin seguridad social, 54.1343%
tiene `P4_10∈{1,2}`; entre quienes trabajan con seguridad social, 37.3130%.
Los complementos sobre el mismo denominador son 45.8657% y 62.6870%.

La pieza nueva `CALC-ENIF-0002` mide la celda D05 sin imputar `P3_13`: entre
personas que no trabajaron el mes anterior, 63.2782% tiene `P4_10∈{1,2}`
(IC95% [60.8904%, 65.6366%], n=3,462, masa expandida 25,090,350). El
complemento exacto es 36.7218% (IC invertido [34.3634%, 39.1096%]).

## 2. Correspondencia y límites del instrumento

- El cuestionario pregunta `P4_10` a toda la persona elegida de 18 años o
  más. `P4_10=1` dice literalmente «Menos de una semana / No tiene ahorros»:
  no permite separar ambos componentes. `NC-0126` sigue ABIERTA y visible.
- Trabaja = `P3_8∈{1,2}` o `P3_9∈{1..6}`. No trabaja = `P3_8=8` o
  `P3_9=7`. Un blanco de `P3_13` no se convierte en no trabajador: también
  aparece por salto entre trabajadores sin pago (`P3_10=6`).
- Seguridad social sólo parte a trabajadores: con = `P3_13∈{1,2,3,4}`;
  sin = `P3_13=7`; `{5,6,9,b}` permanece residual visible.
- La salida científica directa es `p(corto)`; cada `p(no_corto)` adoptado es
  el complemento determinista sobre el mismo universo, con su IC invertido.
  Así se preserva la dependencia exacta y no se inventa un `RESULT-*`.

## 3. Tabla para el motor

| Personas representadas | Horizonte corto | IC95% | n / masa expandida | Uso en motor |
|---|---:|---:|---:|---|
| Trabaja, sin SS (`P3_13=7`) | 0.541343 | [0.521597, 0.561928] | 4,973 / 35,086,918 | `dinero.ahorro.horizonte_corto`, sólo con `actividad_laboral=true` y `seguridad_social_laboral=false` |
| Trabaja, con SS (`P3_13∈{1..4}`) | 0.373130 | [0.349888, 0.393834] | 3,969 / 26,064,281 | `dinero.ahorro.horizonte_no_corto_con_seguridad_social`, sólo con ambos disparadores verdaderos |
| No trabajó el mes anterior | 0.632782 | [0.608904, 0.656366] | 3,462 / 25,090,350 | regla nueva `dinero.ahorro.horizonte_no_trabajadores`, sólo `actividad_laboral=false` |
| Trabaja, SS residual | 0.596182 | [0.550272, 0.638973] | 526 / 3,899,919 | descriptivo; sin consumidor automático |
| Toda persona 18+ con `P4_10` válido | 0.520528 | [0.507667, 0.533833] | 12,930 / 90,141,468 | descriptivo; no sustituye reglas por dominio |

Cobertura poblacional sobre masa total 18+ de 94,221,441: trabaja con SS
27.6628%; trabaja sin SS 37.2388%; no trabaja 26.6291%; trabajador residual
4.1391%; `P4_10` faltante/no válido 4.3302%. La partición es exhaustiva y
disjunta y cierra con delta ponderado cero. El total se estimó como razón
directa dentro de cada réplica de diseño, no como promedio de tasas.

## 4. Ejecución y reproducción

La spec y el medidor se congelaron en el commit `5f5469b5e95b` antes del primer
acceso a microdatos de este acto. Fuente efectiva: payload
`enif_2024_enif_2024_bd_csv`, sha256
`00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039`, más
el `resultados.json` de `CALC-ENIF-0001`, sha256
`2a90c52e532e0c8f17ff87f31c70567f7810f337274f895f3a4623d08f4c57e6`.

Secuencia: `preflight` VERDE → `run` exit 0 → `verify` **REPRODUCE** con
`CONTEXTO=IDENTICO` y 59 resultados coincidentes. Corrida
`CALC-ENIF-0002--5f5469b5e95b`; sello
`2614029cbbb998787253c6dc92c1119c51f09aca74e12e4e7bd62b71c0cc02c1`.
El asiento con identidad completa y procedencia `VERIFY-ESTRUCTURADO` queda en
`forense/replay-evidencia.tsv` para lote08. La comparación interna declara
`RESULT-ENIF-POB-G-REUSO-CALC-ENIF-0001=COINCIDE`.

El bootstrap fue por UPM dentro de estrato, 1,000 réplicas, PCG64, semilla
20260910. Siete estratos de la celda no trabajadora tienen UPM única; el IC se
rotula `IC-CON-ESTRATOS-DE-UPM-UNICA` y se interpreta como límite inferior de
anchura, no como exacto.

## 5. Adopción, historia y registro

D04/D05 quedan materializadas en `milpa/tramite.yaml` y
`milpa/procedencia.yaml`. El B/B histórico no se borra: se conserva bajo
`historico_gen1`, explícitamente no vigente. Pruebas de emisión confirman que
las dos reglas trabajadoras requieren `actividad_laboral=true` y que una
persona no trabajadora no cae por ausencia de seguridad social en una regla
trabajadora.

`NC-0124` CIERRA por adopción efectiva; `NC-0128` CIERRA porque la celda
independiente fue medida, adoptada y su cobertura/residual quedó explícita.
`NC-0126` permanece ABIERTA por límite del reactivo.

`corrida0 demanda` rederiva 207 resultados activos y 82 corridas requeridas.
Las dos conductas nuevas entran después de `RES-0064`, por lo que el esquema
posicional vigente desplaza en +2 los `RES-*` posteriores; los `RESULT-*`
científicos no cambian. `corrida0 registro --escribe --lote CALC-ENIF-0002`
aplicó correctamente el candado `NC-0094` y escribió cero vistas: detectó 32
corridas ajenas cuya evidencia publicada cambiaría con el árbol actual. No se
autorizó esa mutación ajena ni se copió un TSV antiguo. Queda como residual de
integración global para lote08; la evidencia fuente de este CALC sí está
versionada y vigente.

## 6. Validación

- `python3 -m unittest tests.test_enif_poblacion`: 2/2 OK.
- `python3 tools/corrida0.py spec-check CALC-ENIF-0002`: 8 OK, 0 FAIL;
  inventario de 317,718 filas.
- `preflight` / `run` / `verify`: VERDE / 0 / REPRODUCE-IDENTICO.
- Smoke de `milpa.src.emisor`: tres dominios emiten 0.541343/0.458657,
  0.373130/0.626870 y 0.632782/0.367218; cruce inválido no tiene cobertura.
- El gate integral y la reconciliación administrativa se registran al cierre
  del PR.
