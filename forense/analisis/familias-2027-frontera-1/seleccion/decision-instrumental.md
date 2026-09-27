# P1 · Cuatro decisiones instrumentales

**PROPUESTO-POR-EJECUTOR · corte `11602de8e375c10b90807d1b74e088f6b9e99c8b` · 26/sep/2026.**
Worktree `/home/pc0/mm-astra6-c2-frontera-1`, rama `codex/astra6-c2-frontera-1`.
Excepción de entorno comunicada por la sesión responsable: la instrucción posterior
del usuario «corre el encargo» permite realizar también documentación en CAJA.
No levanta ninguna reserva. Estas decisiones no son adopción ni emisiones congeladas.

## Decisiones

| Instrumento | Pregunta falsable propuesta y horizonte | Decisión y razón material | Siguiente gate |
|---|---|---|---|
| ENSU | ¿La proporción de personas 18+ que considera insegura su ciudad en el área CD=01, por sexo, permanece dentro de la banda fijada en el contrato respecto del oro 2025T4 en 2027T4? | Preparar un paquete condicional. Continuidad del reactivo y del área documentada; mismo trimestre para reducir estacionalidad; no predice México total. | Oro propio, potencia, documentación futura y comparabilidad del área/reactivo antes de activar. |
| ENOE | ¿La proporción de empleo informal entre ocupados15–98 con precódigo válido, por sexo, en2027T4 permanece dentro de la banda del contrato respecto de2024T4? | Preparar paquete marginal condicional. Se acredita EMP_PPAL1/2, universo ocupado y era post2023; trimestre fijo limita confusión estacional. No mide transiciones individuales. | Oro2024T4, códigos exactos, peso trimestral, diseño, dependencia de rotación y comparabilidad futura. |
| ENSANUT | ¿La prevalencia de síntomas depresivos CESD-7 en adultos, por sexo, en la edición de referencia 2027 permanece dentro de una banda histórica comparable? | Diferir el desenlace compuesto: tres catálogos limpios confirman continuidad de los siete reactivos y diseño nominal, pero no definen puntaje, inversión del ítem positivo ni umbral de prevalencia. No inventar corte clínico ni asimilar una respuesta triste a diagnóstico. Falta población/modo acreditados por módulo, no continuidad de columnas. | Cuestionarios/descriptores limpios 2021–2023, acreditación por ola de módulo adulto, escala, puntuación, sexo y diseño; documentación de 2027. |
| MOCIBA | ¿La proporción que denuncia ante Ministerio Público o policía entre víctimas usuarias de internet 12+ con respuesta válida, por sexo, en referencia 2027 permanece dentro de una banda histórica comparable? | No lanzar con el oro permitido disponible: históricos abiertos 2015–2017 cambian universo y significado de denuncia; 2021/2022 documentan P12_5 pero sus respuestas siguen reservadas para F6. No heredar el enlace M de miedo/desconfianza entre no denunciantes. | Acto que autorice oro histórico comparable específico, sin abrir reservas por este documento, y contrato descriptivo independiente con ventana/exposición verificadas. |

Resultado de selección: **dos familias candidatas, dos olas futuras propuestas; dos decisiones
de no lanzamiento/diferimiento**. La ejecución de los paquetes puede aún recomendar no lanzar
por precisión. Ninguna decisión convierte la disponibilidad pública en autorización.

## ENSU: comparabilidad que justifica el paquete

Fuente dirigida: `forense/analisis/seguridad-ensu/lista-cerrada-P1.md`, §§1–4,
lista previa a microdatos basada en FD y cuestionarios. El cierre material previo
`forense/analisis/familias-2027/astra6-cierre-material-1/cierre-material-nota.md`
corresponde a ENIF/ENCIG/ENVIPE; esta propuesta no cambia esas seis emisiones.

| Dimensión | Histórico/documentación | Contrato propuesto y límite |
|---|---|---|
| Universo | Persona seleccionada 18+ en áreas urbanas ENSU. | Sólo CD=01 y edad válida 18+; no ciudad como municipio ni todo México. |
| Reactivo/código | C01: `BP1_1`, seguro=1, inseguro=2, NS/NR=9, continuo 2016–2025. | Numerador 2, denominador 1/2/9; preservar NS/NR y reportarlo, sin convertirlo en no respuesta excluida. |
| Geografía | FD2016T1 y FD2025T4 identifican CD01 Campeche/San Francisco de Campeche como mismo nombre propio. | Nombre es evidencia documental, no prueba de límites idénticos: gate explícito de área/cartografía2025T4→2027T4; detener ante redefinición. |
| Esquema | Era tercera, 2021T2–2025T4: `SEXO`, `EDAD` en CB; `FAC_SEL`, `EST_DIS`, `UPM_DIS`. | Oro2025T4, grupo único SEXO; comprobar campos efectivos antes de leer respuestas y no usar unión CB/CS de eras anteriores. |
| Diseño | Estrato CD+EST_DIS, UPM_DIS; mediciones trimestrales. | Incertidumbre por conglomerados, mismo remuestreo para sexos; no suponer independencia entre grupos ni cortes. |
| Modo/continuidad | La lista distingue eras por cuestionario/archivo, no acredita invariancia del modo ni del marco futuro. | Cambio de nombre de columna admite adaptación documentada; cambio de captación/universo/significado exige dictamen antes de R. |
| Periodo | Oro2025T4 abierto; 2026 reservado; ENSU2020T2 cancelado, 2021T1 no encontrado. | 2027T4 es posterior al corte; no interpolar huecos ni usar2026 como covariable. |

Se excluyen CD07 (Torreón→La Laguna, posible redefinición), antiguas divisiones
del DF y ciudades partidas Guadalajara/Monterrey. No seleccionar área por su
valor observado; CD01 se fija por la continuidad documental y el orden de código.
Un área con poco soporte produce no lanzamiento, no sustitución oportunista por otra.

## Fundamento de los otros dictámenes

ENOE: `forense/prereg-caja/ENOE-PISOS-spec-v1_2.md`, §§Insumos, Unidad,
Serie y límites, acredita 43 olas y los cambios ENOE clásica→ENOEN→post2023.
El hueco2020T2 es ETOE y no se interpola. La misma columna no prueba mismo
modo. Los pesos FAC/EST_D y FAC_TRI/EST_D_TRI son transversales; cinco visitas
no crean un peso longitudinal. Se propone por ello una proporción marginal: EMP_PPAL=1 numerador,
EMP_PPAL1/2 y CLASE2=1 denominador; R_DEF=00, C_RES1/3, edad15–98,
FAC_TRI positivo y EST_D_TRI/UPM presentes; agrupación única SEX1/2.
Oro2024T4 y meta2027T4 conservan T4 y era post2023. Cambiar nombres admite
adaptación documentada; cambiar precódigo o marco exige dictamen. La rotación
y los conglomerados compartidos impiden asumir independencia temporal sin
verificación; la potencia debe incluir escenarios de covarianza. No se usan
los valores impresos en el registro de exposición2026T1 para fijar esta pregunta.

MOCIBA: `forense/prereg-caja/MOCIBA-PISOS-spec-v1_0.md` acredita que 2015/2016
incluyen usuarios de internet **o celular** 12+, mientras2017 limita a usuarios
de internet12–59. P7_i_5/P7_i_6A/P10_5 no son un mismo desenlace:2017 agrega
proveedor del servicio a la denuncia. No calibrar una serie con esos tres cortes.
`forense/produccion/mociba-flujo-documental-1/flujo-por-ola.md` sí acredita
2021/2022: internet12+, P4_01..P4_13 abre P12 si hay al menos un sí;
P12_5=1/2 válido, P12_99 excluye NS/NR, blanco dentro de universo es no respuesta.
Sólo2022 documenta blanco; ventanas agosto2020/julio2021 a entrevista distintas.
La spec histórica §Reservas mantiene2021/2022 fuera del oro real; no usar documentos
de esas olas como permiso de leer respuestas. Denominador conectado y víctima
con respuesta válida nunca se presenta como población mexicana total.

ENSANUT: lectura directa con openpyxl de catálogos XLSX adultos2021,2022,2023,
con filas/hash archivados en `ensanut-catalogos-limpios.json`, sin leer respuestas.
Los siete ítems a0211..a0217 conservan texto de última semana y cuatro categorías:
1 menos de un día,2 uno-dos días,3 tres-cuatro días,4 cinco-siete días.
Los cambios son tipográficos (guion/espacios/acentos), no cambian significado.
ASEXO1 Hombre/2 Mujer, AEDAD, ponde_f, est_sel y upm constan en los tres;
UPM es texto de13 posiciones, y no debe convertirse a entero perdiendo ceros.
El ítem a0216 «disfrutó de la vida» es positivo, mientras los demás describen
síntomas negativos. Sumar códigos con igual dirección alteraría el estimando.
Estos catálogos no prescriben puntuación ni punto de corte del compuesto CESD,
ni acreditan selección/población del módulo o equivalencia del modo de captación.
Por ello no se propone prevalencia clínica ni se fija p0 para ese desenlace aún.
El bloqueo es de definición del compuesto y acreditación del universo/método,
no una afirmación de falta de continuidad: el esquema nominal sí es continuo.
Un sucesor puede aportar la regla de puntuación validada y metodología limpia
por módulo, o proponer explícitamente un ítem descriptivo distinto con nueva
justificación. No se sustituye el desenlace para completar cupo. Nunca usar2024
como fuente para completar huecos documentales históricos.

## Calendario y exposición

Todas las metas se refieren a referencia2027, verdaderamente futura al construir
el contrato26/sep/2026. No son «última ola publicada». Ventanas **esperadas y no
confirmadas**: ENSU2027T4 hacia enero2028; ENOE2027T4 hacia febrero2028; ENSANUT
y MOCIBA2027 sin ventana de publicación acreditada en esta selección. Son
expectativas operativas por periodicidad, no fechas oficiales. La fuente previa
`forense/analisis/familias-2027/calendario-y-exclusiones.md` verificó el calendario
INEGI2026 y no encontró calendario aprobado2027 el23/sep; no permite inventar fechas.
La sesión responsable consultó26/sep/2026 el PDF limpio oficial
https://www.inegi.org.mx/contenidos/saladeprensa/doc/cal_2026.pdf:
p22 ENSU2025T4 publicado23/ene/2026; p19 ENOE2025T4 publicado24/feb/2026.
Enero/febrero2028 son inferencias de esa pauta, no fechas oficiales2028.
No se navegaron páginas mezcladas con resultados reservados.

Exposición de esta pieza: lectura de documentos históricos y de specs, sin
microdatos ni resultados para escoger pregunta. Se leyó el registro
`forense/analisis/dominios/exposicion-enoe2026t1-v1_0.md`; ese registro imprime
cifras previamente expuestas2026T1, que no se usan aquí; no se reabrió el boletín.
El rango1–120 de `forense/analisis/salud-bienestar/estructura-ensanut.md` resultó
mezclar metadatos2024 con2021/2022. No contiene respuestas leídas en esta pieza,
pero se declara exposición documental incidental y se descartó como insumo de diseño.
No se promete ceguera respecto de esos documentos ni respecto de resultados históricos
ya presentes en el proyecto. El horizonte2027 evita presentar una ola pasada como futuro.
