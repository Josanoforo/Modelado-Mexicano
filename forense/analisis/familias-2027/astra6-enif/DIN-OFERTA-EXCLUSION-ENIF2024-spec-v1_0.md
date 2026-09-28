# DIN-OFERTA-EXCLUSION-ENIF2024 · spec humana v1.0 · exclusión por oferta al lado del marginal de ahorro formal

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-ASTRA6-C2-EJECUCION-1` · 28/sep/2026 · CAJA · 0-bis `e897d3df`. CALC: `CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001` (cara mecánica `spec.yaml` y `medidor.py` en ese directorio; ningún parámetro vive en los dos sitios).

**Por qué existe.** La firma de mesa del 28/sep sobre `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-15` (E4, opción 1) termina con «Antes de habilitar R se añade la medida de exclusión por oferta junto al marginal». A pregunta de este acto, mesa asignó esa medida a **ENIF ahorro** (`ENIF-AHORRO-FORMAL`, `ENIF-HORIZONTE-AHORRO`); ver `enmienda-firmas-c2-v1_0.md` §4. La regla de fondo es v2.16 §3: «todo marginal de conducta de mercado (crédito, ahorro, canal) se publica con la medida de exclusión por oferta al lado».

**Qué NO es.** No es candidato, retador ni piso. No entra al dictamen de ninguna familia 2027 ni cambia su spec v1_3, su emisión o su sello. No atribuye causa y no se adopta. Es una **descripción retrospectiva** de una ola vista (ENIF 2024), rotulada RETROSPECTIVA. Ninguna frase de producto la mezcla con la emisión PROSPECTIVA.

## 1 · Procedimiento del que es sucesor

Es `forense/prereg-caja/DIN-OFERTA-EXCLUSION-ENIF-spec-v1_0.md` (sha256 `ae00315815604830b04c13c9b5bd85e954825418bc8f5707cff4877eeffca0b5`; CALC selladas 2012, 2015, 2018 y 2021), que excluyó ENIF 2024 («No se abre ENIF 2024…»). De v1.0 se hereda **verbatim la regla de clases**:

> OFERTA: rechazo anticipado, requisitos, distancia/ausencia, intereses, comisiones, saldo mínimo, cierre de sucursal/institución. […] PREFERENCIA: no necesitar/interesar, no querer endeudarse, preferir ahorro/préstamo informal, no usarla, desinterés tras trabajo/apoyo. Desconfianza *o mal servicio* es OTRO/NS por ambigüedad de una sola opción […]. Ingreso insuficiente solo, impuestos, fraude, mala experiencia inespecífica, desconocimiento y «otro» son OTRO/NS.

Cambian solo tres cosas, las tres declaradas aquí antes del dato:
- **(a) Universo.** El de las familias de ahorro: U_B, personas elegidas de 18 años y más con FAC_PER finito y mayor que 0. El v1.0 usaba 18–70, pero el objeto de esta medida es ir al lado del marginal de ahorro, que usa U_B.
- **(b) Dominio.** Solo NACIONAL. Los ejes de v1.0 (sexo, edad, escolaridad, localidad, formalidad) se apartan sin abrir: ningún consumidor de este acto los pide.
- **(c) Lector y bootstrap.** Los del piso de ahorro, no los de la serie de crédito: `_abre`, `_cod`, `_peso`, `_llave`, `_p` e `_ic` de `data/corrida0/CALC-ENIF-0001/medidor.py`, importados por bytes con sha256 fijado en el `spec.yaml`. Así la medida comparte lector y trato de diseño con el piso al que acompaña.

## 2 · Texto, pase y clases (LEÍDO: cuestionario y descriptor, sin bytes de casos)

Fuentes:
- Cuestionario `data/raw/enif_2024_cuestionario.pdf` (manifiesto `enif2024_cuestionario_pdf`, sha256 `32e37cc1…`), sección 5, páginas impresas 16–17.
- Descriptor `diccionario_datos_tmodulo_enif2024.csv` dentro de `enif2024_csv.zip`.
- Microdato: miembro `TMODULO.csv` de `enif_2024_enif_2024_bd_csv` (sha256 `00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039`), el mismo payload del piso `CALC-ENIF-0001`.

Pase:
- **5.4.1–5.4.9**, «¿Usted tiene…» nómina, pensión, apoyos de gobierno, ahorro, cheques, plazo fijo, fondo de inversión, cuenta por internet o aplicación no bancaria, otro. Códigos 1 = sí, 2 = no. «SI TODAS TIENEN CÓDIGO 2, PASE A 5.19».
- **5.19**, «¿Alguna vez tuvo una cuenta o tarjeta de un banco, institución financiera o de apoyo de gobierno?». Códigos 1 = sí (PASE A 5.21), 2 = no.
- **5.20** (`P5_20`, códigos 01…10), «¿Cuál es la razón principal por la que no tiene una cuenta o tarjeta?». Se hace a quien nunca tuvo cuenta.
- **5.21** (`P5_21`, códigos 1…9), «¿Cuál es la razón principal por la que dejó de tener su cuenta o tarjeta?». Se hace al ex usuario.

**No usuario** = los nueve incisos de 5.4 valen 2. **Usuario** = algún inciso vale 1. Cualquier otro caso es **uso desconocido**: se cuenta y no entra. **Nunca** = no usuario con 5.19 = 2. **Ex usuario** = no usuario con 5.19 = 1.

| var | código | texto (verbatim del cuestionario 2024) | clase | submotivo |
|---|---|---|---|---|
| P5_20 | 01 | La sucursal le queda lejos o no hay | OFERTA | |
| P5_20 | 02 | Los intereses son bajos o las comisiones son altas | OFERTA | |
| P5_20 | 03 | No confía en instituciones financieras o le dan mal servicio | OTRO/NS | DESCONFIANZA-O-SERVICIO |
| P5_20 | 04 | Piden requisitos que no tiene | OFERTA | |
| P5_20 | 05 | Prefiere otras formas de ahorro (tanda, guardar en su casa, etcétera) | PREFERENCIA | |
| P5_20 | 06 | No la necesita | PREFERENCIA | |
| P5_20 | 07 | No le alcanza, sus ingresos son insuficientes o variables | OTRO/NS | INGRESO-INSUFICIENTE |
| P5_20 | 08 | No sabe qué es o cómo usarla | OTRO/NS | DESCONOCIMIENTO |
| P5_20 | 09 | No quiere que le cobren impuestos | OTRO/NS | IMPUESTOS |
| P5_20 | 10 | Otro | OTRO/NS | OTRA |
| P5_21 | 1 | Dejó de trabajar y ya no la usaba para que le pagaran su salario | PREFERENCIA | |
| P5_21 | 2 | Dejó de recibir apoyo gubernamental | PREFERENCIA | |
| P5_21 | 3 | No la utilizaba | PREFERENCIA | |
| P5_21 | 4 | Tuvo una mala experiencia con la institución financiera | OTRO/NS | MALA-EXPERIENCIA |
| P5_21 | 5 | No cumplía con el saldo mínimo o por cobro de comisiones | OFERTA | |
| P5_21 | 6 | Los intereses que le pagaban eran muy bajos | OFERTA | |
| P5_21 | 7 | Fue víctima de un fraude | OTRO/NS | FRAUDE |
| P5_21 | 8 | No quería que le cobraran impuesto | OTRO/NS | IMPUESTOS |
| P5_21 | 9 | Otro | OTRO/NS | OTRA |

Cada fila repite la clase que v1.0 dio al mismo texto en 2021 (`forense/analisis/din-oferta-exclusion/conmensuracion-v1_0.tsv`, filas `CUENTA 2021`). La 5.20 de 2024 es **idéntica** a la 5.21 de 2021, opción por opción. La 5.21 de 2024 **no trae** «Cerró la institución financiera o la sucursal» (código 07 en 2021), así que sus códigos 7–9 corresponden a los 08–10 de 2021. Por eso ningún contraste de ex usuarios 2021↔2024 es conmensurable código a código, y este CALC no emite ninguno.

Los códigos se comparan como entero tras quitar blancos (`'01'` y `'1'` son el mismo código de su variable). Un código fuera de dominio o en blanco no se clasifica: el caso queda en NO-RESPUESTA si su pase es conocido.

## 3 · Estimandos (todos proporción [0,1], unidad persona, peso FAC_PER, NACIONAL)

La cohorte es la de los no usuarios de cuenta en U_B con diseño válido (EST_DIS y UPM_DIS no vacíos). Sobre ella:
- **OFERTA**, **PREFERENCIA** y **OTRO-NS**: partición de la cohorte por la clase de la razón principal de su pase. OTRO-NS incluye además el pase estructural y la no respuesta, de modo que las tres suman 1.
- **COBERTURA**: fracción de la cohorte con razón observada.
- **PASE-ESTRUCTURAL**: 5.19 no está en {1, 2}.
- **NO-RESPUESTA**: pase conocido sin razón válida.
- **SUB-<submotivo>**: uno por submotivo de OTRO/NS.

Contexto, con denominador distinto y declarado: **SIN-CUENTA-UB**, la proporción de no usuarios entre las personas de U_B con diseño válido y uso conocido.

La pregunta es de respuesta única, así que «cualquier oferta» coincide con OFERTA y la intersección es vacía. No se emiten. La razón se pregunta **sólo a quien no tiene cuenta**: quien tiene cuenta y no ahorró en ella (F = 0 del marginal) no declara razón. La medida acompaña al marginal y **no descompone** su complemento. Eso se declara en la lectura, no se imputa.

## 4 · Diseño e incertidumbre

- Punto: `_p` de `CALC-ENIF-0001`, con sumas en orden fijo de fila.
- IC95 percentil: `_ic` de `CALC-ENIF-0001`, bootstrap de UPM_DIS con reemplazo dentro de EST_DIS.
- Réplicas: **2 000**. Semilla **20260909** (`numpy.default_rng`, PCG64). Es el mismo plan para cada estimando, porque el generador se reinicia con la semilla en cada llamada.
- Estratos de UPM única: se conservan fijos y el método se reporta como `IC-CON-ESTRATOS-DE-UPM-UNICA`, con su conteo. No hay selección de método por anchura.
- Tolerancia de replay: absoluta 1e-10. Enteros y textos se comparan exactos.

## 5 · Faltantes y ramas terminales (todas por el conducto, D-22(2))

- Columna declarada ausente: `ESTADO = NO-ESTIMABLE-COLUMNA-AUSENTE:<cols>`, proporciones null y conteos enteros.
- Cohorte vacía: `NO-ESTIMABLE-COHORTE-VACIA`, proporciones null.
- Sin diseño en toda la cohorte: punto reportado, IC null y método `NO-ESTIMABLE-DISENO-INCOMPLETO`.
- Peso inválido: se cuenta y queda fuera de U_B.
- EDAD_V fuera de 18…98 se cuenta en `N-EDAD-FUERA`. Es guardia de población, no filtro, igual que en la familia.
- Ningún cero sustituye falta de dato.

## 6 · Guardia (E.6, en el medidor)

La única ola que el código puede abrir es ENIF 2024. `medir` rechaza, con `ValueError('GUARDIA: …')` y **antes de leer el zip**, cualquiera de estos casos:
- (i) un conjunto de inputs de manifiesto distinto de exactamente `{enif_2024_enif_2024_bd_csv}`;
- (ii) `parametros.ola` distinto de `'2024'`;
- (iii) un sha256 del zip distinto del fijado;
- (iv) un sha256 del medidor base `CALC-ENIF-0001/medidor.py` distinto del fijado.

La variable de agrupación es una sola: el id de payload. Prueba por mutación en `tests/test_din_oferta_enif2024.py`: cada mutación (i)–(iv) debe hacer fallar la guardia. Además, las ramas terminales del §5 pasan por `corrida0._valida_outputs` sobre un ZIP sintético.

## 7 · Exposición declarada (ADR-46)

Antes de este freeze, la sesión leyó:
- cuestionario y descriptor de ENIF 2024 y 2021;
- el encabezado de columnas de TMODULO 2024;
- el manifiesto, las specs y los medidores sellados de las familias ENIF y de DIN-OFERTA v1.0;
- los **ids** de RESULT de la serie DIN-OFERTA 2012–2021, no sus valores.

No leyó bytes de casos de ENIF 2024 ni el valor de ningún RESULT de oferta. Sí sabe que el piso de ahorro formal existe (`RESULT-ENIF-AHO-B-P-FORMAL-P`) y no leyó su valor. `exposicion_historica: CIEGO-A-VALORES-ESTRUCTURA-LEIDA`.

## 8 · Módulo de auditoría v2.16

- ¿Cuántos contadores mueve? Un CALC GEN2 descriptivo (`cuenta_gen2: SI`, `adopta: NO`). Cero celdas validadas.
- Escala y unidad: proporción de personas no usuarias de cuenta. No se compara con el marginal de ahorro sin decir que sus denominadores difieren (§3).
- PROSPECTIVA / RETROSPECTIVA: esta cifra es RETROSPECTIVA (ola vista). Las emisiones 2027 son PROSPECTIVA. No se mezclan.
- Oferta antes que preferencia: esta medida **es** el lado de oferta. Aun así, «preferencia declarada» no es preferencia psicológica. «No la necesita» y «prefiere tanda» pueden ser adaptación racional a ingresos bajos o variables, y la opción de ingreso insuficiente está aparte, en OTRO/NS, justo para no leerla como gusto.
- Riesgo de lectura simplista: leer una OFERTA baja como «los mexicanos no quieren bancos». La partición depende de un solo reactivo de razón principal, y desconfianza o mal servicio queda indistinguible por diseño del cuestionario.
- Sesgo de clase: la cohorte de no usuarios está sobrerrepresentada en hogares rurales y de ingreso bajo. Una cifra nacional no describe a la clase media urbana formal ni al sistema indígena-comunal.
