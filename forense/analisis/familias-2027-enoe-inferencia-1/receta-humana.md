# Receta humana previa · ENOE2024T4

Estado: PROPUESTO-POR-EJECUTOR. Fijada antes del recálculo sucesor de incertidumbre: 2026-09-27T18:08:53.422930+00:00. Preparación informada por el oro y el lector históricos; no validación ciega. No modifica p0, bandas, escenarios ni emisiones históricas.

## Estimando, universo y razón

Proporción nacional de empleo informal entre ocupados de 15–98 por SEX=1/2. Universo de entrevista R_DEF=00 (0 equivalente serializado), C_RES=1/3. Dominio D_g=1 para edad15–98, SEX=g, CLASE2=1 y EMP_PPAL=1/2; cero fuera. Numerador X_g=sum FAC_TRI D_g 1(EMP_PPAL=1), denominador Y_g=sum FAC_TRI D_g; p_g=X_g/Y_g. Blancos EMP_PPAL excluidos y contados, códigos ajenos detienen entre ocupados. Pesos positivos finitos; llave persona ENT+UPM+CON+N_PRO_VIV+V_SEL+N_HOG+H_MUD+N_REN. Mantener puntos históricos exactos; cualquier diferencia de punto se explica y exige acto separado.

## Marco y llaves

Conservar todas las UPM presentes en residentes entrevistados R_DEF=00/0 y C_RES=1/3 antes de aplicar dominio, edad, ocupación o sexo. Crear contribución cero para UPM sin integrantes del dominio. Auditar adicionalmente UPM del archivo completo para revelar posibles pérdidas por entrevista/residencia; no incorporar pesos o unidades de entrevistas no logradas como si fueran mediciones.

INEGI §3.11 define entidad e, estrato h dentro de e y UPM i. Clave propuesta (ENT, EST_D_TRI) y UPM anidada dentro de esa clave. No asumir que claves crudas sean globales. Auditar EST_D_TRI→ENT, UPM→ENT/estrato y CD_A/tamaño de localidad. Si EST_D_TRI ya es global, prefijar ENT debe resultar equivalente; si colisiona cambia agrupación y se declara. No añadir CD_A ni colapsar estratos automáticamente: CD_A es área de cobertura, no una instrucción de varianza. Si los invariantes no resuelven la estructura, bloquear hasta crosswalk oficial.

## Incertidumbre principal condicionada a identificabilidad

Aplicar conglomerados últimos con linealización de Taylor de la razón, conforme INEGI Métodos y procedimientos 2020 §3.11 p54 vinculado por RNM al trimestre2024T4. Para cada UPM i en estrato h de entidad e, z_ehi,g=sum_i FAC_TRI D_g(1(EMP_PPAL=1)-p_g)/Y_g. Con m_eh UPM del marco completo y media zbar_eh,g, V_g=sum_eh [m_eh/(m_eh-1)]sum_i(z_ehi,g-zbar_eh,g)^2; SE_g=sqrt(V_g). El centrado dentro del estrato es el término publicado; no se usa centrado entre estratos para suplir singleton. Esta es una aproximación de conglomerados últimos con pesos finales fijos, no la varianza exacta de todas las etapas/calibración.

No aplicar FPC: la fórmula publicada p54 no incluye (1-f); el CSV/descriptor consultado no aporta N_eh ni probabilidades de inclusión de primera etapa para estimarla. No deducir FPC de FAC_TRI, conteo de personas o viviendas. La omisión es parte de la aproximación propuesta publicada, no prueba de fracciones pequeñas.

Un estrato con m=1 permanece BLOQUEADO-POR-SINGLETON-NO-IDENTIFICADO. No declarar certeza porque haya una UPM, tamaño residual o residuo cero. Certeza requiere evidencia oficial de inclusión de esa UPM con probabilidad1 y tratamiento de etapas inferiores; ninguna obtenida en P1. Incluso certeza de primera etapa no demuestra varianza total cero cuando etapas inferiores son aleatorias. No eliminar singleton ni imputar su contribución como cero. Si persiste, reportar solo suma identificable de m>=2 como componente parcial, nunca como SE total ni entrada válida a potencia. Solicitud mínima: crosswalk de EST_D_TRI/ENT/CD_A/UPM, condición de certeza/probabilidad de inclusión y regla oficial de varianza para cada estrato afectado, o réplicas oficiales compatibles con FAC_TRI2024T4.

## Sensibilidades, comparación y decisión

Variantes de llaves se auditan para diagnóstico antes de interpretar SE; no se elige la que mejora potencia. Kish no reemplaza diseño. Colapso, average/adjust de singleton o réplicas inventadas carecen aquí de fundamento oficial; no método principal. Comparar réplicas solo si existe esquema sustentado de selección/calibración o pesos oficiales. Ante singleton real, NO-LANZAR sin alimentar potencia con suma parcial.

Si ambos SE son identificables, usar sucesor de potencia con ambos grupos y seis escenarios históricos intactos. Distinguir inferencia condicionada a p0 fijo de cambio entre poblaciones: SE_d²=SE_oro²+SE_futura²-2 rho SE_oro SE_futura. rho=0 supuesto; cinco visitas no prueban independencia de UPM entre olas. No cambiar alpha, banda±.05, horizonte2024T4→2027T4, dependencia ni adverso. Rechazar grupos faltantes/SE inválidos/escenarios incompletos. Regla propuesta hasta firma.

Fuentes y hashes: [documentacion/fuentes.md](documentacion/fuentes.md).
