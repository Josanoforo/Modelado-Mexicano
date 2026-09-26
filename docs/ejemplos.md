---
title: Ejemplos de consulta
---

# Ejemplos de consulta

[Portada]({{ '/' | relative_url }}) · [Consultar]({{ '/consultar.html' | relative_url }}) · [Contrato]({{ '/consulta.html' | relative_url }}) · [Verificar]({{ '/verificar.html' | relative_url }})

Cinco preguntas reales, una por dominio, más un límite. Todo lo de abajo es salida cruda de `python3 tools/benchmark.py` sobre el catálogo `v1_1`; esta página se regenera con `python3 tools/benchmark.py ejemplos` y un test comprueba que no se desfasa. Ninguna cifra está tecleada.

## 1 · TRABAJO

**Pregunta.** ¿Qué proporción de las mujeres ocupadas tiene empleo informal en el último trimestre medido?

```
python3 tools/benchmark.py consulta --conducta empleo_informal --segmento sexo=mujer --ola 2025T4
```

```
catálogo v1_1 · consulta {'conducta': 'empleo_informal', 'segmento': ['sexo=mujer'], 'ola': '2025T4'} · filas=1 (mostradas 1)

empleo_informal · ENOE 2025T4 · sexo=MUJER
  punto 0.558383 · IC95 [0.553643, 0.565008] (diseno: IC95-DE-DISENO) · unidad proporcion
  RETROSPECTIVA · origen NUEVO · ADOPTADO · DESCRIPTIVO-DE-OLA
  cita RESULT-ENOE-PISOS-TABLA#25664 · CALC-ENOE-PISOS-0003 · resultados 243c7ea54033 · sello 3b916aacd14b
  oferta: NO-APLICA
  reserva: piso retrospectivo; calidad=ALTA

Términos: uso no comercial libre con atribución; uso comercial por acuerdo; contacto = correo de CITATION.cff.
```

**Verificación** de la primera fila:

```
python3 tools/benchmark.py verificar 'RESULT-ENOE-PISOS-TABLA#25664'

fila RESULT-ENOE-PISOS-TABLA#25664 · catálogo v1_1 · CALC-ENOE-PISOS-0003
[1] sha256(sello.json)=3b916aacd14b5bc2c027485dae82dae5d1d68408c3a754b5aa39c99bc9398b8c = sello.sha256 · OK
[2] sello.json[resultados.json]=243c7ea54033afd760d97b22d031e5aaa0009b6d3f25dec3b10a00a2fa772c86 = sha256(resultados.json) · OK
[3] valor sellado 0.5583834923197161 = punto del catálogo · OK
[4] hashes = forense/analisis/catalogo/v1_1/calcs.tsv · OK
[5] spec.yaml sha256=0ca8e82381f3d1f8c33d42f52499101ad0e99d5d94df77df6e9561d48599dc19 · ejecucion.json presente · OK
CADENA-VERIFICADA (no recalcula: `python3 tools/corrida0.py verify CALC-ENOE-PISOS-0003` necesita el corpus)
```

## 2 · GÉNERO

**Pregunta.** ¿Cuántas mujeres con escolaridad superior declaran violencia en el ámbito laboral (ENDIREH 2021)?

```
python3 tools/benchmark.py consulta --conducta laboral --segmento escolaridad=superior
```

```
catálogo v1_1 · consulta {'conducta': 'laboral', 'segmento': ['escolaridad=superior']} · filas=2 (mostradas 2)

laboral · ENDIREH 2021 · escolaridad=superior
  punto 0.120919 · IC95 [0.113288, 0.127819] (diseno: IC95-DE-DISENO) · unidad proporcion
  RETROSPECTIVA · origen NUEVO · ADOPTADO · DESCRIPTIVO-DE-OLA
  cita RESULT-ENDIREH2021-LAB-TABLA#58 · CALC-ENDIREH-PISOS-2021-LABORAL-0001 · resultados 16732c7b6c5c · sello 34f57f6e532c
  oferta: NO-APLICA
  reserva: piso retrospectivo; ventana=desde_octubre_2020

laboral · ENDIREH 2021 · escolaridad=superior
  punto 0.25874 · IC95 [0.250435, 0.267817] (diseno: IC95-DE-DISENO) · unidad proporcion
  RETROSPECTIVA · origen NUEVO · ADOPTADO · DESCRIPTIVO-DE-OLA
  cita RESULT-ENDIREH2021-LAB-TABLA#8 · CALC-ENDIREH-PISOS-2021-LABORAL-0001 · resultados 16732c7b6c5c · sello 34f57f6e532c
  oferta: NO-APLICA
  reserva: piso retrospectivo; ventana=vida

Términos: uso no comercial libre con atribución; uso comercial por acuerdo; contacto = correo de CITATION.cff.
```

**Verificación** de la primera fila:

```
python3 tools/benchmark.py verificar 'RESULT-ENDIREH2021-LAB-TABLA#58'

fila RESULT-ENDIREH2021-LAB-TABLA#58 · catálogo v1_1 · CALC-ENDIREH-PISOS-2021-LABORAL-0001
[1] sha256(sello.json)=34f57f6e532cf4fb4ee507a6d0bde9775f19a709553b00e1044c29e01e0de7ca = sello.sha256 · OK
[2] sello.json[resultados.json]=16732c7b6c5cae762ba44d089a84d75745f6e3d4d17df6b1f8aae6a204bc435c = sha256(resultados.json) · OK
[3] valor sellado 0.12091943362561124 = punto del catálogo · OK
[4] hashes = forense/analisis/catalogo/v1_1/calcs.tsv · OK
[5] spec.yaml sha256=f3e4869e5994ecc51e2cb0be684dc22ba5dfee484136de014495a30f292927f9 · ejecucion.json presente · OK
CADENA-VERIFICADA (no recalcula: `python3 tools/corrida0.py verify CALC-ENDIREH-PISOS-2021-LABORAL-0001` necesita el corpus)
```

## 3 · TECNOLOGÍA

**Pregunta.** ¿Qué proporción de la población usa internet, a nivel nacional, en la ENDUTIH más reciente?

```
python3 tools/benchmark.py consulta --conducta internet --segmento nacional= --instrumento ENDUTIH --ola 2025
```

```
catálogo v1_1 · consulta {'conducta': 'internet', 'segmento': ['nacional='], 'instrumento': 'ENDUTIH', 'ola': '2025'} · filas=1 (mostradas 1)

internet · ENDUTIH 2025 · TOTAL=TOTAL
  punto 0.860526 · IC95 [0.856306, 0.865446] (diseno: IC95-DE-DISENO) · unidad proporcion
  RETROSPECTIVA · origen NUEVO · ADOPTADO · DESCRIPTIVO-DE-OLA
  cita RESULT-ENDUTIH-PISOS-2025-TABLA#46 · CALC-ENDUTIH-PISOS-2025-0001 · resultados b2adcea4c19a · sello 63fbc8320d3d
  oferta: NO-APLICA
  reserva: piso retrospectivo; sin uso predictivo

NO CONTESTA · FUERA-POR-REGLA · NSE-FUERA-DE-RESERVA-DE-INSTRUMENTO: 6 celda(s), p. ej. RESULT-AMAI-NSE-ENDUTIH-2024-internet-BAJO-P

Términos: uso no comercial libre con atribución; uso comercial por acuerdo; contacto = correo de CITATION.cff.
```

**Verificación** de la primera fila:

```
python3 tools/benchmark.py verificar 'RESULT-ENDUTIH-PISOS-2025-TABLA#46'

fila RESULT-ENDUTIH-PISOS-2025-TABLA#46 · catálogo v1_1 · CALC-ENDUTIH-PISOS-2025-0001
[1] sha256(sello.json)=63fbc8320d3d2cd9dd1553d5c46acfec17c606a1f7c48d296fc232d87a8574f0 = sello.sha256 · OK
[2] sello.json[resultados.json]=b2adcea4c19abbae3c655a35fa4313f5ec3dd3c7f0ed0f4801c16fe83d84620d = sha256(resultados.json) · OK
[3] valor sellado 0.8605264595792668 = punto del catálogo · OK
[4] hashes = forense/analisis/catalogo/v1_1/calcs.tsv · OK
[5] spec.yaml sha256=006684cc5ffa51e169bb1e538b9db6774bd6b11702a62ee4d13d677c1cea7c13 · ejecucion.json presente · OK
CADENA-VERIFICADA (no recalcula: `python3 tools/corrida0.py verify CALC-ENDUTIH-PISOS-2025-0001` necesita el corpus)
```

## 4 · DINERO

**Pregunta.** ¿Quién ahorra solo por vías informales (ENIF 2024), y qué se sabe de la oferta?

```
python3 tools/benchmark.py consulta --conducta ahorra_solo_informal
```

```
catálogo v1_1 · consulta {'conducta': 'ahorra_solo_informal'} · filas=4 (mostradas 4)

ahorra_solo_informal · ENIF 2024 · NSE=ALTO
  punto 0.292847 · IC95 [0.269184, 0.31697] (diseno: IC95-DE-DISENO) · unidad persona elegida 18+
  RETROSPECTIVA · origen NUEVO · ADOPTADO · DESCRIPTIVO-DE-OLA
  cita RESULT-AMAI-NSE-ENIF-2024-ahorra_solo_informal-ALTO-P · CALC-AMAI-NSE-ENIF-2024-0001 · resultados fe6acb706f08 · sello 941507266a9c
  oferta: SIN-MEDIDA-DE-OFERTA-SELLADA-PARA-ESTA-OLA-Y-CONDUCTA: exclusión por oferta sellada solo para crédito ENIF 2012/2015/2018/2021 (CALC-DIN-OFERTA-EXCLUSION-ENIF*-0001)
  reserva: eje NSE con reserva de instrumento; aproximación conforme

ahorra_solo_informal · ENIF 2024 · NSE=BAJO
  punto 0.390052 · IC95 [0.373886, 0.407387] (diseno: IC95-DE-DISENO) · unidad persona elegida 18+
  RETROSPECTIVA · origen NUEVO · ADOPTADO · DESCRIPTIVO-DE-OLA
  cita RESULT-AMAI-NSE-ENIF-2024-ahorra_solo_informal-BAJO-P · CALC-AMAI-NSE-ENIF-2024-0001 · resultados fe6acb706f08 · sello 941507266a9c
  oferta: SIN-MEDIDA-DE-OFERTA-SELLADA-PARA-ESTA-OLA-Y-CONDUCTA: exclusión por oferta sellada solo para crédito ENIF 2012/2015/2018/2021 (CALC-DIN-OFERTA-EXCLUSION-ENIF*-0001)
  reserva: eje NSE con reserva de instrumento; aproximación conforme

ahorra_solo_informal · ENIF 2024 · NSE=MEDIO
  punto 0.364562 · IC95 [0.342208, 0.386152] (diseno: IC95-DE-DISENO) · unidad persona elegida 18+
  RETROSPECTIVA · origen NUEVO · ADOPTADO · DESCRIPTIVO-DE-OLA
  cita RESULT-AMAI-NSE-ENIF-2024-ahorra_solo_informal-MEDIO-P · CALC-AMAI-NSE-ENIF-2024-0001 · resultados fe6acb706f08 · sello 941507266a9c
  oferta: SIN-MEDIDA-DE-OFERTA-SELLADA-PARA-ESTA-OLA-Y-CONDUCTA: exclusión por oferta sellada solo para crédito ENIF 2012/2015/2018/2021 (CALC-DIN-OFERTA-EXCLUSION-ENIF*-0001)
  reserva: eje NSE con reserva de instrumento; aproximación conforme

ahorra_solo_informal · ENIF 2024 · regla=dinero.ahorro.via_informal
  punto 0.357153 · IC95 sin IC identificado (sin-ic: SIN-IC-IDENTIFICADO) · unidad VER-SPEC
  RETROSPECTIVA · origen NUEVO · ADOPTADO · PARAMETRO-DE-REGLA
  cita RESULT-HVD-A-SOLO-INFORMAL · CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1 · resultados 16a03f136bf7 · sello 1c8b329fb208
  oferta: SIN-MEDIDA-DE-OFERTA-SELLADA-PARA-ESTA-OLA-Y-CONDUCTA: exclusión por oferta sellada solo para crédito ENIF 2012/2015/2018/2021 (CALC-DIN-OFERTA-EXCLUSION-ENIF*-0001)
  regla dinero.ahorro.via_informal · tier FUERTE · falsable si: Si el ahorro informal sustituyera al formal, las celdas anidadas de escolaridad/formalidad/cuenta corroborarían el desenlace secundario; se cayeron las tres CONTRARIA (ver nota_l1)
  reserva: conducta_p_asignado

Términos: uso no comercial libre con atribución; uso comercial por acuerdo; contacto = correo de CITATION.cff.
```

**Verificación** de la primera fila:

```
python3 tools/benchmark.py verificar 'RESULT-AMAI-NSE-ENIF-2024-ahorra_solo_informal-ALTO-P'

fila RESULT-AMAI-NSE-ENIF-2024-ahorra_solo_informal-ALTO-P · catálogo v1_1 · CALC-AMAI-NSE-ENIF-2024-0001
[1] sha256(sello.json)=941507266a9c96d3c76e13f55d674b2544eaf3a21f6a95d23deb397be30b99ba = sello.sha256 · OK
[2] sello.json[resultados.json]=fe6acb706f08f4f63e32ec8e2c5b95a0f0971104cdde0b0d8809bfe625a0beae = sha256(resultados.json) · OK
[3] valor sellado 0.2928474317507563 = punto del catálogo · OK
[4] hashes = forense/analisis/catalogo/v1_1/calcs.tsv · OK
[5] spec.yaml sha256=60288968a8b1ffcdeb9c542b31d1f034526e681dc7998bb68f6a3db5f681063e · ejecucion.json presente · OK
CADENA-VERIFICADA (no recalcula: `python3 tools/corrida0.py verify CALC-AMAI-NSE-ENIF-2024-0001` necesita el corpus)
```

## 5 · SALUD

**Pregunta.** ¿Qué proporción de quienes tuvieron un problema de salud buscó atención, en el estrato rural (ENSANUT 2024)?

```
python3 tools/benchmark.py consulta --conducta busco-atencion --segmento localidad=rural --ola 2024
```

```
catálogo v1_1 · consulta {'conducta': 'busco-atencion', 'segmento': ['localidad=rural'], 'ola': '2024'} · filas=1 (mostradas 1)

busco-atencion · ENSANUT 2024 · ESTRATO=RURAL
  punto 0.843758 · IC95 [0.712573, 0.921652] (calibrado: IC-CALIBRADO-PERSISTENCIA) · unidad proporcion
  RETROSPECTIVA · origen NUEVO · ADOPTADO-CON-RESERVA-DE-ANCHO · DESCRIPTIVO-DE-OLA
  cita RESULT-ENSANUT-PISOS-SALUD-BUSCO-ATENCION-2024-ESTRATO-RURAL-P · CALC-ENSANUT-PISOS-SALUD-0001 · resultados a2d6654d84c0 · sello cc0d5fe3f004
  oferta: NO-APLICA
  reserva: piso retrospectivo; sin uso predictivo

Términos: uso no comercial libre con atribución; uso comercial por acuerdo; contacto = correo de CITATION.cff.
```

**Verificación** de la primera fila:

```
python3 tools/benchmark.py verificar 'RESULT-ENSANUT-PISOS-SALUD-BUSCO-ATENCION-2024-ESTRATO-RURAL-P'

fila RESULT-ENSANUT-PISOS-SALUD-BUSCO-ATENCION-2024-ESTRATO-RURAL-P · catálogo v1_1 · CALC-ENSANUT-PISOS-SALUD-0001
[1] sha256(sello.json)=cc0d5fe3f00409344fb04388fe258ec8c38392daf4e649088ecb99d51d73310b = sello.sha256 · OK
[2] sello.json[resultados.json]=a2d6654d84c002179dc40eb1c01999f7351dd27be09c52b414d3151033537434 = sha256(resultados.json) · OK
[3] valor sellado 0.8437583114877262 = punto del catálogo · OK
[4] hashes = forense/analisis/catalogo/v1_1/calcs.tsv · OK
[5] spec.yaml sha256=757b276eddfe7fc613650743374cc995903d4b2cef567888b267b3a2d363150f · ejecucion.json presente · OK
CADENA-VERIFICADA (no recalcula: `python3 tools/corrida0.py verify CALC-ENSANUT-PISOS-SALUD-0001` necesita el corpus)
```

## 6 · LÍMITE

**Pregunta.** ¿Y el empleo en la ENOE 2026? (ola reservada: la consulta debe negarse con su razón)

```
python3 tools/benchmark.py consulta --texto empleo --instrumento ENOE --ola 2026
```

```
catálogo v1_1 · consulta {'texto': 'empleo', 'instrumento': 'ENOE', 'ola': '2026'} · filas=0 (mostradas 0)

NO CONTESTA · OLA-RESERVADA · ENOE 2026: reservada en data/manifiesto.yaml (E.6); no se abre ni se consulta

Términos: uso no comercial libre con atribución; uso comercial por acuerdo; contacto = correo de CITATION.cff.
```

**Cómo leerlos.** Todas las filas son RETROSPECTIVAS y descriptivas de su ola; el IC es el que declara `tipo_ic`. Un gradiente por localidad, escolaridad o formalidad se lee primero como estructura y oferta, no como cultura (§3 de las instrucciones).
