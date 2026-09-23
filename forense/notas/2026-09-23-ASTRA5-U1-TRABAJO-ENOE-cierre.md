# ASTRA5-U1 · Trabajo ENOE · cierre de medición

**23/sep/2026 · CAJA · RETROSPECTIVA · adopta NO.** Encargo archivado en
`forense/encargos/2026-09-23-ASTRA5-U1-TRABAJO-ENOE.md` (cuerpo SHA-256
`bf42d6b5ccdbcf7388fd000c40d9e1eee5264d2909b9c59a1e23f0152244d23d`).
Base `origin/main` al abrir: `8e41f72fa8b00a20e83f28c92f6b2964e66b0081`.
Rama `codex/astra5-trabajo-enoe-1`. COMMIT-1 final de pisos `dffd28a4`;
COMMIT-2 `873005af`. Primeras dos versiones fallaron sin RESULT ni sello;
logs conservados como `run-v1_0-fallo.log` y `run-v1_1-fallo.log`.
COMMIT-1 de persistencia: método humano y código `a436e3f0`, cableado de
hashes `19a54f29`; COMMIT-2 `88053b0d`.

## EJECUTADO

* **Pisos:** `CALC-ENOE-PISOS-0003`, `RESULT-ENOE-PISOS-TABLA`, sello SHA-256
  `3b916aacd14b5bc2c027485dae82dae5d1d68408c3a754b5aa39c99bc9398b8c`.
  **43/43 paquetes trimestrales elegibles**, 13 conductas distintas con piso
  GEN2 (contador inicial de este acto: 0; final: **13**), **26,273 celdas**
  por ola/segmento (no son 26,273 conductas). Calidad: 23,137 ALTA, 1,818
  MODERADA, 1,318 BAJA. Tabla de consumo
  `forense/analisis/dominios/enoe/pisos-v1_0.tsv`: punto, IC95 de diseño,
  n, n efectivo Kish, UPM, calidad, RESULT/CALC/sello y disponibilidad de
  calibración en cada fila. 200 réplicas por UPM dentro de estrato y ola,
  compartidas entre dominios de la misma ola. `verify`: REPRODUCE,
  CONTEXTO=IDENTICO, 5/5 RESULT, 48/48 inputs; log SHA-256
  `57460f5e4aa2e82e388a712f76dfcc5738151d39c312fb8a1906772172656041`.
* **Persistencia descriptiva:** `CALC-ENOE-PERSISTENCIA-0001`,
  `RESULT-ENOE-PERSISTENCIA-TABLA`, sello SHA-256
  `fd0951c2e47be94efd09a08e42679562635118bd0049b374f79e241ab9689481`.
  20,304 pares trimestrales agregados de 12 conductas, sin ingreso nominal;
  9,024 clásica, 5,076 ENOEN y 6,204 post-2023. 18,612 tienen origen
  suficiente para pronóstico de tendencia retrospectivo. La comparación
  descriptiva `destino dentro de IC95 de diseño del origen` ocurre en
  14,502/20,304 pares; **no es cobertura predictiva ni validación** por el
  solapamiento del panel. En 20,304/20,304 pares el IC predictivo es nulo:
  `SIN-COVARIANZA-LONGITUDINAL-PARA-CALIBRAR`. Tabla de consumo
  `forense/analisis/dominios/enoe/persistencia-v1_0.tsv`, con
  RESULT/CALC/sello en cada fila. `verify`: REPRODUCE, CONTEXTO=IDENTICO,
  3/3 RESULT, 3/3 inputs; log SHA-256
  `9cf202521ff00e5ca3526dfbefd19487fce9a273f729d3e7ac725bec72f38f78`.
  El método consume solo el RESULT agregado de pisos y nunca enlaza personas.

La tabla de pisos conserva las cuatro olas aisladas 2005T1, 2008T1,
2012T1, 2014T1; el tramo continuo 2016T1–2020T1, la era ENOEN
2020T3–2022T4 y la post-2023 2023T1–2025T4. No interpola 2020T2 ni une
eras por compartir nombre de variable. La tabla de saltos, códigos y
denominadores está en `forense/prereg-caja/ENOE-PISOS-spec-v1_2.md` y la
matriz congelada `data/enoe-reactivos-olas-v1_0.tsv` (559 filas).

## LEÍDO Y REPORTADO · corte U0

El insumo U0 es `8f7e8de0`, copia SHA-256
`fb7a0385b70278cff5c84ecaf3abb6b44fdc4a0e21ae1fdb832f4f03e81a79ac`.
Los tres contrastes siguientes son **ENOE 2024T3 nacional**, personas 15+,
ponderadas, escala proporción; los IC son de diseño en la propia ola:

| U0 | Componente medido y universo | Punto (IC95) · n | Dictamen limitado |
| --- | --- | --- | --- |
| 001 | Empleo informal, ocupados con `EMP_PPAL` válido | 54.64% (54.17–55.09), n=193,623 | **CONFIRMA** mayoría de ocupados informales en el trimestre. El 55.7% anual publicado en el report no es el mismo estimando temporal; no se comprueba causa cultural ni horizonte de planeación. |
| 002 | Sin contrato escrito, **subordinados elegibles** con `TIP_CON` válido | 41.49% (40.97–42.01), n=134,250 | **Sin contraste directo** con «over half work without a formal contract»: todos los ocupados y formalidad laboral completa son denominador y concepto distintos de P3i. Tampoco se mide confianza o lealtad. |
| 003 | Más de 50 horas en semana de referencia, ocupados con horas válidas | 22.09% (21.73–22.48), n=185,214 | **MATIZA** el componente semanal para 2024T3 frente al 28.7% del report sin fecha comparable acreditada; no ROMPE el valor de otra fecha ni prueba estrés o burnout. |

El corte nacional 2025T4 da empleo informal 55.00% y sector informal
29.48%: las dos clasificaciones miden objetos distintos. Ninguna prevalencia
es una transición individual. La media de ingreso es **mensual nominal
positiva** por ola; no se interpreta como poder adquisitivo. `PNEA_EST=4`
se informa como **otras obligaciones**, nunca como cuidados específicos.

## NO-CORRIDO / RESERVAS

* `NC-260923-ASTRA5-U1-TRABAJO-ENOE-e422-01`: 2026T1, última ola del
  corpus (`enoe_2026_1t_csv`, `enoe_2026_1t_microdatos`), reservada en
  manifiesto y **sin abrir**. El sitio oficial lista 2026T2 al corte, ausente
  del corpus; no se descargaron datos/tabulados de esa ola. Continuación
  solo tras acto que levante reserva y preregistre nuevo CALC.
* `NC-260923-ASTRA5-U1-TRABAJO-ENOE-e422-02`: transición individual entre
  formal e informal no identificada aquí: faltan enlace longitudinal,
  elegibilidad, atrición y peso longitudinal acreditados. Las prevalencias
  transversales sí están completas. Sucesor: contrato de panel validado y
  CALC nuevo, sin reciclar diferencias de prevalencia.
* `NC-260923-ASTRA5-U1-TRABAJO-ENOE-e422-03`: cuidado específico y serie
  de ingreso real no estimables con la capa SDEM y los insumos sellados:
  PNEA_EST=4 mezcla obligaciones; falta COE P2G2 por era y deflactor oficial
  versionado. Los pisos de otras obligaciones y de ingreso nominal sí salen.
  Sucesor: contrato COE/deflactor con hashes, si se solicita ese estimando.
* `NC-260923-ASTRA5-U1-TRABAJO-ENOE-e422-04`: IC predictivo calibrado y
  afirmación de cambio entre olas no se emiten sin covarianza conjunta del
  panel rotatorio. Sucesor: réplica longitudinal con diseño y enlace
  acreditados, congelada antes del dato. El RESULT de persistencia ya agota
  la evaluación descriptiva autorizada; este residual no obliga otra corrida
  para concluir el frente.

## CONSUMIDO

U0 `8f7e8de0` (tres afirmaciones cerradas), cuestionario básico v7 y FD
registrados, PDF oficial de diseño `enoe_n_diseno_muestral_pdf` con hash
`42eaa300fcbd4bec98c2a38f3edb5912bcc2208fe69a54a0c1103b75a85dbd09`;
contratos y barridos ENOE previos solo como diseño, sin importar sus cifras
GEN1. #1009/#1041 aportaron el marco de evaluación temporal; esta versión
lo acota a origen móvil trimestral y declara la calibración no identificada.
Ambos replay REAL están asentados en `forense/replay-evidencia.tsv`.
El canal de vistas globales queda pendiente de publicación por su mecanismo
vigente; rótulo de estos CALC: **sellada en disco, no registrada** hasta que
el canal derive su vista. No se modifica catálogo U1 ni se adopta.

**Pruebas:** cuatro pruebas sintéticas ENOE pasan. `python3 tests/check.py
--baseline` terminó con código 0 y **LÍNEA BASE: VERDE, sin FAIL nuevos**;
persisten tres FAIL heredados (T06 dos, T08 uno). T02 y T27, que marcaron
tres FAIL propios en el primer pase, quedaron corregidos y pasan en el
segundo. `git diff --check` limpio. No se congela una línea base nueva.

## Paquete de consumo y rigor

Para catálogo/report Trabajo, Mérito/Movilidad y Juventud: consumir
`pisos-v1_0.tsv` para puntos transversales con sus universos; consumir
`persistencia-v1_0.tsv` únicamente como error retrospectivo de piso; citar
CALC, RESULT y sello por fila. Evidencia primaria mexicana: microdatos ENOE
en 43 olas, documentación oficial INEGI y diseño muestral; reports son
afirmaciones a contrastar, no fuentes de los puntos. Marco importado:
ninguno para los valores mexicanos. Falsadores concretos: un recálculo
sellado que no reproduzca punto/IC bajo el mismo diseño; texto/código oficial
que invalide un denominador; evidencia de enlace y peso longitudinal que
permita identificar transiciones; una serie COE/deflactor que distinga
cuidados e ingreso real. No se infieren preferencias, cultura, psicología,
causalidad ni genética de los segmentos. El IC95 de diseño describe
incertidumbre transversal por ola; no autoriza contrastes temporales.

## Recibo Codex → Claude

Acto preparado y ejecutado en la rama indicada; PR **#1087**, abierta y
fusionable al cierre, sin fusionar. Productos
revisables: specs congeladas, dos CALC sellados y reproducidos, dos TSV de
consumo, reservas y límites exactos, FP por instrumento, fragmento L0 y
registro de rótulo. Mesa decide merge/adopción; la reserva 2026T1 sigue
vigente después del merge. La rama integró `origin/main` mediante merge,
sin reescribir los commits de COMMIT-1/COMMIT-2; la línea base volvió a
dar VERDE después de la integración.
