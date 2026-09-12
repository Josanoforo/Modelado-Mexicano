# Spec congelada · MOTRAL 2015, valoración de seguridad social

**CALC:** `CALC-MOTRAL2015-VALORACION-SS-0001`  
**Objeto:** `trabajo.prestaciones.formalidad_pesa_mas_que_salario` (`R2.3`)  
**Fecha de congelación:** 11/sep/2026, antes de observar los estimandos.

## Fuente, población y unidad

MOTRAL 2015, tabla `motral2015_cuestionario.dbf`, persona seleccionada. La
población elegible son entrevistas completas (`R_DEF=00`) de 18–54 años
(`EDA`) con experiencia laboral (`C_TRA in {1,2}`), de las 32 ciudades
autorrepresentadas. Se usa `FAC_MOTRAL`, factor final ajustado por no respuesta
y proyecciones. Cobertura: nacional urbana del segmento definido, no México
total.

Fuentes oficiales congeladas: cuestionario `motral2015_cuestionario`, base
`motral2015_bases_datos_dbf`, descriptor `motral2015_estructura_bd` y documento
`motral2015_documento_metodologico`. P16/P17 están en la tabla de cuestionario;
no se deducen desde `motral2015_empleos.dbf`.

## Variables y códigos

- `P17`: 1 Sí, 2 No, blanco no aplica. Estimando: proporción 1 entre 1/2.
- `P16_1…P16_5`: seguro médico, seguro de vida, accidentes de trabajo,
  pensión y crédito de vivienda, respectivamente; cada columna registra rango
  1–5, 9 no especificado. Primer lugar = la única columna con código 1.
- `SEX`: 1 hombre, 2 mujer. `EDA`: edad verificada en años.
- Diseño: estrato `(CD_A,EST_D)`, UPM `UPM`, factor `FAC_MOTRAL`.

Un ranking es **completo** si es una permutación exacta de 1–5;
**incompleto-con-primero** si conserva un único 1 pero le faltan otros rangos;
**inconsistente** si repite un rango válido o tiene más de un 1; e
**incompleto-sin-primero** si no permite identificar el primero. La
distribución usa toda persona con primer lugar único, incluso si el resto del
ranking está incompleto; nunca promedia rangos ni cuenta cinco filas por
persona. Se publican las cuatro clases de calidad.

## Estimandos predeclarados

1. P17 afirmativo para total, hombres, mujeres, edades 18–34 y 35–54.
2. Distribución de primer lugar P16 (cinco prestaciones separadas) en esos
   mismos cinco dominios.
3. Entre elegibles que enlazan uno-a-uno con SDEM ENOE 2015-T2 y están
   ocupados (`CLASE2=1`), P17 afirmativo por cobertura actual: con acceso
   (`SEG_SOC=1`) y sin acceso (`SEG_SOC=2`). `SEG_SOC=3` se cuantifica como no
   especificado y no entra en esos dos denominadores.

Son 32 celdas descriptivas en una sola operación analítica. No son 32
mediciones independientes ni parámetros adoptados.

## Enlace ENOE

Entrada `enoe_2015_trim2_dbf`, tabla `SDEMT215.DBF`. Llave estándar documentada
en el proyecto: `CD_A+ENT+CON+V_SEL+N_HOG+H_MUD+N_REN`, todos caracteres. El
preflight material halló 7,000 llaves MOTRAL únicas, 6,564 enlaces SDEM únicos,
436 pérdidas y cero muchos-a-muchos. El medidor vuelve a comprobarlo y aborta
ante duplicados. Se usa `FAC_MOTRAL`, no `FAC` ENOE, porque la unidad y el
marco analítico siguen siendo la persona seleccionada del módulo. El cruce es
condicional a enlace y ocupación; no corrige la pérdida de enlace y no usa
`SEG_SOC` retrospectivo de MOTRAL ni el último empleo de la trayectoria.

## Faltantes, precisión y salidas

Cada celda reporta n expuesto, n válido, desconocidos y su masa, n y masa del
numerador, masa del denominador, punto, EE, IC95 y grados de libertad. Pesos
no positivos/no finitos se excluyen y cuentan.

La varianza usa linealización de razón por UPM, estrato `(CD_A,EST_D)` y la
muestra completa (fuera del dominio aporta cero), según el documento
metodológico MOTRAL: conglomerados últimos y Taylor. IC95 normal bilateral,
truncado a [0,1], sin FPC. Estratos singleton no se agrupan y no aportan
varianza. Diseño incompleto o denominador nulo produce precisión no disponible.

Uso permitido: evidencia descriptiva de valoración declarada y de asociación
con cobertura actual. P17 pregunta por aceptar pagos/aportaciones para obtener
seguridad social; no enfrenta dos salarios explícitos, no identifica WTP ni
prueba que la formalidad pese más que cualquier salario. La comparación
salarial estricta conserva `EXISTE-NO-SATISFACE`. Sin causalidad ni adopción.
