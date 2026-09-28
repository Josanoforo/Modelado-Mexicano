# PDR1 · ENUT 2024 (+ ENUT 2019 ola previa de 6.17) · spec v1.0

ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1, pieza P-ENUT2024, entorno CAJA.
CALC: `data/corrida0/CALC-PDR1-ENUT2024-0001` (medidor `medidor.py`). Encargo:
`forense/encargos/2026-09-28-GEN2-PISOS-DOMINIOS-Y-REGLAS-1.md`. Universo de la pieza =
filas `pieza=P-ENUT2024` de `forense/analisis/pisos-dominios-1/tabla-apertura-v1_0.tsv`:
afirmaciones ASTRA5-U0-TIME-002, -TIME-020, -VEJEZ-009 (TIEMPO), -RURAL-002 y
-VEJEZ-032 parte (a) (RURAL_INDIGENA), y la regla RG-3920de961d (CAPITAL_SOCIAL).
Todo es **RETROSPECTIVA** (ENUT 2024 ya abierta por CALC sellados; ENUT 2019 ya abierta).

## 0 · Premisas, reserva y lectura previa

- Reserva (E.6): `motivo_reserva` → LIBRE para `enut2024_bd_csv` y `enut2019_bd_csv`.
  ENUT 2024 es la ola más reciente del programa, pero ya la abrieron CALC sellados
  (`CALC-ENUT-0001`, `CALC-ENUT2024-DISTRIBUCION-HORAS-0001/-0002`,
  `CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001`, `CALC-ENUT2024-NUCLEO-EJES-0001`, todos
  con `sello.json`). Ninguna spec de `forense/prereg-caja` la declara RESERVADA; el único
  cruce reservado de ENUT 2024 es `reparto_hogar × sexo_edad` (spec ENUT-NUCLEO §3): esta
  pieza no lo toca (no hay celda de hogar ni cruce sexo×edad).
- Lectura de estructura antes del COMMIT-1 (permitida, declarada): FD
  `enut2024_fd_xlsx` (hojas TMODULO, TVAR_CREA, TVIVIENDA), FD `enut2019_fd_xlsx` (TModulo),
  cuestionario `enut2024_cuestionario_pdf` (texto) y la **cabecera** de columnas de
  `tmodulo.csv`, `tvar_crea.csv`, `tsdem.csv` (2024) y `enut_2019/TMODULO.csv` (2019).
  Se leyeron también los `resultados.json` ya sellados de
  `CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001` (ola vista). Ningún registro de microdato
  leído, contado ni tabulado.
- E.5 (lo sellado se cita): los CALC ENUT 2024 sellados miden **sólo horas de cuidado**
  (Σ de los cuatro `CUID_*_CON_CP`, núcleo C2/C3, percentiles), por sexo×edad o por un eje.
  Ninguno mide `TRAB_NO_REM_VOL` (el agregado doméstico+cuidados+voluntario de TIME-002 /
  VEJEZ-009), convivencia (6.21), medios (6.22), tiempo total de trabajo, `P6_17_3`
  (comunitario) ni la condición de hablante. `CALC-ENUT2019-NUCLEO-EJES-0001` no usa
  `P6_17_2`. `tools/ya_medido.py RG-3920de961d` → NUNCA-MEDIDA. Por tanto todo lo de abajo
  es medición nueva; se cita como contexto (no como el mismo estimando)
  `RESULT-ENUTPI-A-CON-PARTICIPACION-NACIONAL` (participación en cuidado, 4 familias CON_CP,
  no `TRAB_NO_REM_CON_CP`).

## 1 · Variables por texto (A.15)

ENUT 2024, base nacional (`tmodulo.csv` 1 fila por persona de 12+ del módulo; unida 1:1
por `LLAVEMOD` a `tvar_crea.csv`):

- **Trabajo no remunerado doméstico, de cuidados y voluntario** = `TRAB_NO_REM_VOL`
  (FD TVAR_CREA fila 35: «Trabajo no remunerado doméstico, de cuidados y voluntario»,
  horas/semana, rango 0–466.5). Blanco/no numérico/negativo = inválido, fuera del
  denominador, contado (`DIAG-TNR-INVALIDOS`); 0 es cero genuino.
- **Cuidado a integrantes del hogar** = `TRAB_NO_REM_CON_CP` (FD TVAR_CREA fila 44:
  «Trabajo no remunerado de cuidado a integrantes del hogar, con cuidados pasivos»);
  participación = valor > 0.
- **Tiempo total de trabajo** = `ACTIV_PROD_CON_CP` (FD TVAR_CREA fila 28: «Actividades
  productivas o de trabajo, con cuidados pasivos — Tiempo total de trabajo (TTT)»).
- **Convivencia familiar y social** = bloque 6.21 (cuestionario p.24; FD TMODULO filas
  1342–1381), sus cuatro ítems: «…¿usted dedicó tiempo especial (sin hacer otra actividad) a
  integrantes de su hogar para platicar…?» (`P6_21_1`), «…asistió o participó en actividades o
  celebraciones religiosas?» (`P6_21_2`), «…celebraciones cívicas o políticas?» (`P6_21_3`),
  «…conversó o se reunió con familiares o amistades, asistió o participó en fiestas…?»
  (`P6_21_4`); códigos 1 Sí / 2 No. Participa = algún ítem = 1. Horas = Σ ítems de
  `h_LV + min_LV/60 + h_SD + min_SD/60` (`P6_21A_i_1..4`; blanco «por secuencia» = 0).
- **Medios masivos / entretenimiento** = bloque 6.22 (cuestionario p.24; FD TMODULO filas
  1382–1441), seis ítems «…¿usted PARA ENTRETENERSE…?»: TV/películas/videos (`_1`), radio/
  música (`_2`), lectura (`_3`), subir contenido a redes (`_4`), correo/redes (`_5`), otra
  actividad en internet (`_6`). Misma regla de participación y horas.
- **Trabajo comunitario gratuito** = `P6_17_3` (cuestionario p.22; FD TMODULO fila 1282):
  «6.17 Durante la semana pasada, ¿usted hizo actividades o servicios gratuitos para la
  comunidad como tequio, faena, mano vuelta, mayordomía, fiestas patronales o sembrar árboles,
  limpiar calles, ríos, mercados, etcétera?» 1 Sí / 2 No; otro/blanco fuera del denominador
  (`DIAG-COMUN-FUERA-1-2`). Horas entre participantes: `P6_17A_3_1..4`.
- **Hablante de lengua indígena** = `P4_1` (cuestionario p.10; FD TMODULO fila 37): «4.1
  ¿Usted habla algún dialecto o lengua indígena?» 1 Sí / 2 No; otro fuera del segmento.
- **Autoadscripción indígena** = `COND_IND` (FD TVAR_CREA fila 164: 1 «Sí se considera
  indígena», 2 «No se considera», 9 no especificado → fuera del segmento).
- **Tamaño de localidad** = `TLOC` (FD TMODULO filas 1608–1611): 4 «menos de 2 500
  habitantes» = RURAL; 1–3 = URBANO. `MENOR10` (FD TVAR_CREA fila 157: 1 = «Localidades con
  una población de 1 a 9 999 habitantes») = MENOR10; resto con TLOC válido = MAYOR10.
- Sexo `SEXO` 1 hombre / 2 mujer; edad `EDAD_V` (FD TMODULO fila 34; 98 «no sabe» fuera
  del eje) en 12-17, 18-29, 30-39, 40-59, 60+.

ENUT 2019 (ola previa, sólo para 6.17 / RURAL-002; base nacional `enut_2019/TMODULO.csv`,
nunca `enut_2019_indigena/`): `P6_17_2` (FD 2019 TModulo fila 995, mismo texto literal que
2024), `P4_1` (fila 25), `TLOC` (fila 1318), `FAC_PER`, `EST_DIS`, `UPM_DIS`.

## 2 · Universo, unidad, ponderador, diseño, IC, agregador

- Unidad: **persona de 12 años y más**, residente de vivienda particular, semana de
  referencia. Escala: horas/semana (medias) o proporción [0,1] (participación).
- Universo: filas de la tabla del módulo nacional. Sin tope a 168 h (agregados con
  simultaneidad, como publica INEGI).
- Ponderador `FAC_PER` (FD TMODULO fila 1620). Diseño: estrato `EST_DIS`, UPM `UPM_DIS`
  (llaves opacas de texto). Fila sin ponderador positivo o sin diseño sale de todo, contada.
- Agregador (E.1): razón ponderada Σw·y/Σw por celda. Tres estimandos de horas:
  **INT** = E(h | h>0) (intensidad entre quien realiza la actividad; convención de los
  tabulados INEGI, *primario* para cifras publicadas), **MEDIA** = E(h) con ceros,
  **PART** = P(h>0) (o P(Sí) para 6.17). Diferencias (brechas) = celda a − celda b en la misma
  réplica.
- IC95: bootstrap de UPM con reemplazo dentro de estrato, **2 000 réplicas**, `PCG64(42)`,
  un plan por ola; estrato de UPM única se remuestrea a sí mismo (varianza cero, contado);
  percentiles 2.5/97.5. Celda vacía → P/IC null (`permite_no_estimable`), N se conserva.
- Segmentación mínima (§3, México no es bloque): nacional, sexo, cinco grupos de edad,
  rural/urbano para TRAB_NO_REM_VOL y para 6.17; más hablante/no hablante y
  autoadscripción para 6.17; sexo dentro de MENOR10, MAYOR10, hablante y no hablante para la
  brecha de TRAB_NO_REM_VOL. No se emite ningún cruce sexo×edad.
- Salida: sólo RESULT escalares (flotante/entero), ids `RESULT-PDR1-ENUT2024-…` con sufijos
  `-P`, `-IC95-INF`, `-IC95-SUP`, `-N`; ningún texto (regla de 1024 bytes).

## 3 · Pre-registro de falsación B-bis (fijado antes del dato)

Regla general: cifra dentro del IC95 → CONFIRMA; mismo signo/orden pero fuera del IC →
MATIZA; signo u orden contrario → ROMPE. Cuando una afirmación tiene varios componentes, el
dictamen es el **peor** (ROMPE > MATIZA > CONFIRMA). Estimando que manda = el nombrado aquí.

- **B1 · TIME-002** («mujeres 39.7 y hombres 18.2 h/sem de trabajo no remunerado; brecha
  21.5; cerca de 26 h en localidades < 10 000»). Manda `TNR-INT-BRECHA-SEXO` contra 21.5:
  CONFIRMA si 21.5 ∈ IC95; ROMPE si punto ≤ 0; MATIZA en otro caso. Se reportan (no
  mandan) `TNR-INT-MUJER` vs 39.7, `TNR-INT-HOMBRE` vs 18.2 y `TNR-INT-BRECHA-SEXO-MENOR10`
  vs 26, y las MEDIA equivalentes. La inferencia sobre planeación no es observable.
- **B2 · VEJEZ-009** (67.8 % dedicó tiempo a cuidados; 39.7/18.2). Componentes: (i)
  `TNR-INT-BRECHA-SEXO` con la regla de B1 (mismo RESULT; dedup con TIME-002, no es evidencia
  adicional); (ii) `CUID-PART-NAC` contra 0.678: CONFIRMA si ∈ IC95; ROMPE si punto < 0.5
  (deja de ser mayoría); MATIZA en otro caso. Dictamen = peor de (i),(ii).
- **B3 · VEJEZ-032 (a)** («brecha para hablantes de lengua indígena: 27.3 h»). Manda
  `TNR-INT-BRECHA-SEXO-HABL` contra 27.3: CONFIRMA si ∈ IC95; ROMPE si punto ≤ 0; MATIZA en otro
  caso. Parte (b) (proyección CONAPO) fuera de esta pieza: NO-CONSTRUIBLE aquí (P1).
- **B4 · TIME-020** (convivencia 7.4 h con 75.9 %; medios 15.4 h con 91.7 %; trabajo total
  59.6 h, mujeres 61.1, hombres 58.0). Componentes: `CONV-INT-NAC`/7.4, `CONV-PART-NAC`/0.759,
  `MED-INT-NAC`/15.4, `MED-PART-NAC`/0.917, `TTT-INT-NAC`/59.6, `TTT-INT-BRECHA-SEXO`/3.1:
  cada uno CONFIRMA si la cifra ∈ IC95, si no MATIZA; ROMPE (orden) si
  `MED-INT-NAC` ≤ `CONV-INT-NAC`, o `MED-PART-NAC` ≤ `CONV-PART-NAC`, o
  `TTT-INT-BRECHA-SEXO` ≤ 0. Dictamen = peor.
- **B5 · RURAL-002** (sin cifra; falsador: la prevalencia de trabajo comunitario gratuito
  no es mayor entre población indígena). Manda `COMUN-PART-DIF-IND-NOIND` (autoadscripción,
  unidad persona; el falsador habla de localidades con autoidentificación, aquí se usa la
  persona: declarado): CONFIRMA si IC95 inferior > 0; ROMPE si punto ≤ 0; MATIZA si punto > 0
  con IC que toca 0. Si sale CONFIRMA pero `COMUN-PART-DIF-RURAL-URBANO` tiene punto ≤ 0,
  baja a MATIZA. Las celdas de 2019 (`OLA2019-*`) son piso de la ola previa; no deciden.
- **R1 · RG-3920de961d** (SI comunidad rural/indígena con obligación normada y sanción
  ENTONCES participa; SI urbano sin sanción ENTONCES participación voluntaria baja). Se
  contrasta la parte observable: diferencia de proporción de trabajo comunitario gratuito
  RURAL − URBANO en persona 12+ (`COMUN-PART-DIF-RURAL-URBANO`, pp en escala [−1,1]).
  CONFIRMA si IC95 inferior > 0 **y** `COMUN-PART-URBANO-P` < 0.10 («baja»: umbral fijado
  aquí); ROMPE si punto ≤ 0; MATIZA en otro caso. La «obligación normada y sanción» (multa,
  exclusión, requisito para cargo) **no es observable** en ENUT: ni se pregunta ni se
  infiere; el dictamen no dice nada del mecanismo (coerción vs. voluntad), sólo del contraste
  de participación. `COMUN-PART-DIF-IND-NOIND` y `-HABL-NOHABL` se reportan como contexto.

## 4 · Módulo de auditoría v2.16

- Unidad: persona 12+; escala horas/semana o proporción; nunca hogar.
- RETROSPECTIVA: ENUT 2024 y 2019 ya abiertas; no hay predicción.
- Segmentación: sexo, edad, rural/urbano, hablante, autoadscripción; no se trata a México
  como bloque; la brecha se lee dentro de segmento.
- ¿Incentivo o psicología? Ninguno se identifica: son descripciones de uso del tiempo. La
  regla R1 atribuye participación a coerción normativa: ENUT no la observa.
- ¿Clase media urbana? No: la pieza mide justamente la diferencia rural/indígena vs urbano.
- Peligroso leído simplista: (1) leer la brecha de horas como preferencia femenina o como
  «cultura»; (2) leer mayor participación comunitaria rural como prueba de la sanción; (3)
  sumar 6.21/6.22 como «ocio» comparable con horas de trabajo (hay simultaneidad); (4)
  presentar VEJEZ-009 como evidencia de cuidado a mayores (es el mismo agregado de TIME-002).

el primer resultado que produzca este procedimiento es el que se reporta.
