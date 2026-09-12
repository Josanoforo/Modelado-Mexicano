# Informe · validación independiente de parámetros activos GEN2

**Acto:** `GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS`

**Fecha:** 11 de septiembre de 2026

**Protocolo fijado antes del contraste:** commit `323b403`

**Veredicto agregado:** **16/16 PASA**

## Resultado

Una implementación separada reconstruyó desde los cinco payloads originales los
16 `RESULT` distintos que alimentan las 16 salidas directas del snapshot GEN2
v1.1. No importó ni ejecutó los `medidor.py` productores para calcular los
puntos. Los abrió sólo después de terminar los autocontroles y las mediciones,
para efectuar el contraste.

Los nueve puntos publicados a precisión completa coinciden exactamente. Los
siete puntos ENIF, publicados a seis decimales, concuerdan dentro de la
tolerancia predeclarada de media unidad del último decimal; el máximo absoluto
es `4.789432163088136e-07`. Los 16 tamaños de muestra y todas las masas que el
productor declara coinciden exactamente.

| spec | RESULT | punto independiente | punto productor | delta absoluto | n | veredicto |
|---|---|---:|---:|---:|---:|---|
| `CALC-ENVIPE-0001` | `RESULT-ENVIPE-DEN-P-C2-U4` | 0.29431298745731216 | 0.29431298745731216 | 0 | 13,023 | PASA |
| `CALC-ENCUCI-0001` | `RESULT-ENCUCI-B-P-RUR-AGR` | 0.09191244410077362 | 0.09191244410077362 | 0 | 2,050 | PASA |
| `CALC-ENCUCI-0001` | `RESULT-ENCUCI-B-P-URB-AGR` | 0.11219151313930475 | 0.11219151313930475 | 0 | 8,322 | PASA |
| `CALC-ENIF-0001` | `RESULT-ENIF-AHO-A-P-CORTO-SIN-P` | 0.5413426451419872 | 0.541343 | 3.548580128631684e-07 | 4,973 | PASA |
| `CALC-ENIF-0001` | `RESULT-ENIF-AHO-A-P-CORTO-CON-P` | 0.3731299167623308 | 0.37313 | 8.323766920170783e-08 | 3,969 | PASA |
| `CALC-ENIF-0002` | `RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P` | 0.6327820855428481 | 0.632782 | 8.554284813833135e-08 | 3,462 | PASA |
| `CALC-ENIF-0001` | `RESULT-ENIF-AHO-C-P-DESCONFIA-CONOCE-P` | 0.06077998307684667 | 0.06078 | 1.6923153330072882e-08 | 426 | PASA |
| `CALC-ENIF-0001` | `RESULT-ENIF-AHO-C-P-DESCONFIA-NOCONOCE-P` | 0.05476737995596916 | 0.054767 | 3.7995596915973984e-07 | 2,544 | PASA |
| `CALC-ENIF-0001` | `RESULT-ENIF-AHO-B-P-FORMAL-P` | 0.28492736594847873 | 0.284927 | 3.6594847874216185e-07 | 13,502 | PASA |
| `CALC-ENIF-0001` | `RESULT-ENIF-AHO-B-P-INFORMAL-P` | 0.5619195210567837 | 0.56192 | 4.789432163088136e-07 | 13,502 | PASA |
| `CALC-B-0001` | `RESULT-B-ENIGH-2022-P` | 0.04569409956405095 | 0.04569409956405095 | 0 | 90,102 | PASA |
| `CALC-ENCIG-0001` | `RESULT-ENCIG-MOR-C-P-ADOPTA` | 0.6733930340661712 | 0.6733930340661712 | 0 | 20,203 | PASA |
| `CALC-ENCIG-0001` | `RESULT-ENCIG-MOR-A-P-SOL1` | 0.08511814556534456 | 0.08511814556534456 | 0 | 40,042 | PASA |
| `CALC-ENCIG-0001` | `RESULT-ENCIG-MOR-B-P-DIG-SD` | 0.029867554626649372 | 0.029867554626649372 | 0 | 7,219 | PASA |
| `CALC-ENCIG-0001` | `RESULT-ENCIG-MOR-B-P-PRE-SD` | 0.1410407168724654 | 0.1410407168724654 | 0 | 11,167 | PASA |
| `CALC-ENCUCI-0001` | `RESULT-ENCUCI-A-P-CUALQUIERA` | 0.12600561008991654 | 0.12600561008991654 | 0 | 13,411 | PASA |

No se reutilizó evidencia numérica previa: las 21 filas que ya existían en el
overlay pertenecían a tres `CALC-R-CIV-M-*`, sin identidad exacta con estos
objetos. La ejecución sí reutilizó infraestructura neutra del repositorio para
resolver rutas y el contrato común para proyectar el resultado.

## Identidad y evidencia

- `evidencia-parametros-activos.json`: SHA-256
  `2c9669f134db034f54c422a114bb8368f55bba7e44e19c0c482ffa172f3e491f`.
- `resumen-parametros-activos.tsv`: SHA-256
  `a90512df3dd209adcaf3990bc3b601c6e0d127b00707ce42f67f46d280f4a8da`.
- El segundo `--write` reprodujo ambos hashes byte a byte.
- Los snapshots históricos no se reescribieron: v1.0 conserva SHA-256
  `05350667baa245c79c3ed487aeb1403d74b4612fcae69e16845b8d42f1a5eaa8`
  y v1.1 conserva SHA-256
  `95d36cef4735f85a22f0346bc04dabdab2f13724c96e9a19179996cb93bca3bb`.
- El sucesor `snapshot-M-gen2-explicito-v1_2.json` tiene SHA-256
  `ca083554b8cd844b1a54a6147d37e26ff4096f15037e8cae6b4450f64ee763e6`
  y pasa la verificación exacta del generador v1.2.

La evidencia agregada conserva por resultado fuente, miembro, hashes,
definición, contadores, máscaras de exclusión, numerador, denominador, n,
comparación y consumidor. No incorpora microdatos al repositorio.

## Incorporación y consumo

`data/corrida0/validaciones-independientes.tsv` añade 16 asientos `PASA` por
identidad completa `(spec_id, resultado_id)`. El resolvedor vigente los proyecta
en las tres columnas de validación de `data/corrida0/resultados.tsv`. El
snapshot sucesor v1.2 sellado devuelve 16 salidas directas, 16 `EMITE`, 16
`PASA` y 16 `RESULT` únicos; su verificación exige igualdad exacta con la
reconstrucción viva.

La regeneración integral de `corrida0 registro` detectó además un `CALC` F5 ya
fusionado pero todavía ausente de las vistas publicadas. Como ese cambio no
pertenece a este acto, no se absorbió: se aplicó sólo el overlay mediante los
resolvedores y el escritor canónicos. El diff de `resultados.tsv` contiene 16
altas de validación y ninguna alteración de valor, uso o linaje.

## Alcance del veredicto

`PASA` acredita fuente, población, unidad, codificación, ponderador,
transformación, punto y enlace al consumidor. La incertidumbre de diseño queda
`NO-COMPROBADA`: no se contrastaron EE/IC ni se declara equivalencia de diseño.
La misma muestra tampoco se convierte en evidencia experimental independiente,
holdout o medición científica nueva.

El efecto operativo es acotado: aumenta la confianza mecánica en los 16 puntos
que el motor ya emitía, sin modificar sus valores, adopción, rol, dominios ni
condiciones de activación. **Contador científico: cero.**
