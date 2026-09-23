# Política y vida cívica · tres instrumentos separados

**RETROSPECTIVA.** Este producto conserva tres tablas y sus unidades. No
calibra una serie, no selecciona votantes y no adopta parámetros al modelo.
La clasificación de los 45 ID `ine_*` del manifiesto está en
`ine-45-clasificacion.tsv`: 33 calendarios/acuerdos, 5 piezas cartográficas,
3 conteos (general y dos modalidades especiales), 2 fiscalizaciones, 1 PREP
y 1 catálogo de casillas. Sólo el conteo general aquí mide marcas de voto.

## Tabla 1 · INE, elección federal 2024

| Fuente / unidad | Numerador | Denominador | Resultado | Calidad |
|---|---:|---:|---:|---|
| Conteos Censales DECEyEC; registros en cuadernillos de lista nominal de casillas catalogadas, 32 entidades | SV = 54 899 228 | LN = 98 330 348 | 55.8314% | NS = 6 325 654; 9 773 730 filas de 2024; 0 descuadres LN/SV/NV/NS |
| Mismo universo, sólo marcas conocidas | SV = 54 899 228 | SV+NV = 92 004 694 | 59.6700% | Es diagnóstico de cobertura, no reemplazo de la tasa sobre LN |

`RESULT-INE-PISOS-2024-TABLA`, `CALC-INE-PISOS-2024-0001`, resultados SHA256
`5d5e0ce5bef544457e4c49f34a92b08672c692bf20b83f932b6db44a6da068ca`.
El conteo usa la cartografía DERFE 2023, `EDOCVE` y sección por versión; el
producto agrega numeradores/denominadores, nunca porcentajes de sección.
Excluye casillas especiales y voto desde el extranjero. LN, marcas de voto,
boletas y votos válidos son objetos distintos. PREP tampoco es cómputo
definitivo. No se calculó IC de muestreo sobre este censo administrativo.
Las celdas por sexo con LN<30 se rotularon SUPRIMIDA por calidad; los totales
adyacentes permiten reconstruir algunas por resta. No son una garantía de
confidencialidad secundaria y no deben presentarse como tal. La tasa 55.83%
no refuta la cifra de participación presidencial basada en otra fuente y
denominador que figura en el report forense de clientelismo.

## Tabla 2 · ENCUP 2012, respuestas de la base publicada

| Reactivo / escala | Respuesta seleccionada | n válido | Proporción entre válidos |
|---|---|---:|---:|
| P37 interés en política, 1 mucho/2 poco/3 nada | Mucho | 3 731 | 15.7867% |
| P51_2 influencia ciudadana, 1 mucho/2 poco/3 nada | Mucho | 3 712 | 28.6638% |
| P30_15 confianza en IFE, 0–10 | 8–10 | 3 714 | 34.5450% |
| P30_10 confianza en vecinos, 0–10 | 8–10 | 3 730 | 39.8123% |

`RESULT-ENCUP-PISOS-2012-TABLA`, `CALC-ENCUP-PISOS-2012-0003`, resultados
SHA256 `417560d3947963b842e7569cbec23028069fa0bf0129324216a9f673fe6a64e2`.
La hoja contiene 3 750 entrevistas. Son distribuciones descriptivas sin
peso, estrato o UPM verificados; no se ofrecen IC de diseño ni inferencia
representativa por entidad o país. Las categorías `Mucho/Poco/Nada` del XLSX
se recodifican según el cuestionario; P30 conserva números 0–10. Las cinco
olas con cuestionario no forman aquí una serie de cinco bases. IFE 2012 no
se rebautiza INE 2024. P44A trata obediencia a leyes y P68 consenso de
mayoría; ninguno mide jerarquía interpersonal.

`CALC-ENCUP-PISOS-2012-0001` falló antes del sello por confundir códigos con
cabeceras completas. `0002` se selló con P37 y P51_2 NO-ESTIMABLE porque
las columnas tenían etiquetas, no números. Su resultado se conserva con
el sello intacto en `forense/historico/ASTRA5-U3-POLITICA/CALC-ENCUP-PISOS-2012-0002.tar`
(SHA256 `17f1121fb33b43e2b2b40d0607b00ca880eb7ea1831116e7b0e00a6dd6648213`,
sello verificado tras extracción); `0003` es la
remedición explícita desde raw, sin alterar los sellos previos.

## Tabla 3 · LAPOP México 2018–19, v1.0_W

| Reactivo / universo | n | Punto ponderado | IC95 bootstrap UPM dentro de estrato |
|---|---:|---:|---:|
| `clien1na`, ofrecieron favor/regalo/beneficio por voto en última elección, sí entre sí/no | 1 578 | 17.1736% | 15.2638%–19.0871% |
| `b18`, confianza en Policía Nacional 6–7 entre 1–7 | 1 558 | 10.7189% | 9.0734%–12.4756% |

`RESULT-LAPOP-PISOS-2019-TABLA`, `CALC-LAPOP-PISOS-2019-0001`, resultados
SHA256 `40ecdc8e1f0b2228d357aea0b0284bcf18d97eddc8058831cfd95f4c78008f1f`.
Ambos puntos usan `wt`, `estratopri`, `upm`, 129 UPM en 4 estratos y 2 000
réplicas válidas. La muestra especial de terremoto 2017 queda fuera. Oferta
declarada, recepción, participación y elección declarada son variables
distintas. Ya existe el GEN2 `CALC-ARBITRO-MARGINALES-2-LAPOP-0001` para
asociaciones clientelares; se cita y no se presenta como experimento.
No hay asignación aleatoria de «ofrecieron», y el secreto del voto limita
cualquier inferencia sobre compra efectiva. No se compara `b18` con P30_15
de ENCUP: institución, escala y fecha son diferentes. Olas 2021/2023 y
2004/2006 quedan fuera de una serie temporal hasta dictamen de texto,
versión, modo, diseño y geografía. Una muestra adicional no equivale a
una nacional. No hay historia suficiente validada para IC predictivo:
**SIN-HISTORIA-PARA-CALIBRAR**.

## Enlace editorial y afirmaciones U0

| Afirmación del corpus | Componente observado | Juicio |
|---|---|---|
| Política: la participación responde a interés, eficacia y contexto | ENCUP describe interés/eficacia; INE registra marcas de voto en otro universo | Sin contraste directo del mecanismo individual; los tres niveles no se unen |
| Confianza: la confianza institucional y la cercana pueden diferir | ENCUP IFE frente a vecinos, preguntas distintas dentro de la misma ola | MATIZA: dos distribuciones descriptivas, sin prueba de mecanismo ni representatividad nacional acreditada |
| Autoridad: obedecer leyes evidencia deferencia interpersonal | P44A y P68 fueron revisadas por objeto | ROMPE ese enlace de constructo; no se estima jerarquía interpersonal |
| Forense clientelismo: oferta implica voto comprado | LAPOP mide sólo prevalencia de oferta; CALC previo mide asociación | Sin contraste directo del efecto causal; la oferta precede a cualquier preferencia |

No se asigna un patrón psicológico a una sección INE ni se unen personas
encuestadas con secciones. Tier primario mexicano: ZIP de INE, cuestionario y
XLSX ENCUP, microdato y codebook LAPOP (cada afirmación anterior cita su
RESULT o reactivo). El report forense y los medidores GEN1 sirven como marco
o diseño, nunca como origen de estos números GEN2. Falsadores: una fuente de
cierre INE que cambie el numerador/denominador bajo la misma cobertura; un
descriptor ENCUP que acredite peso/diseño y cambie las proporciones; un
codebook LAPOP que invierta códigos o muestre un modo no comparable. Estas
posibilidades obligan a un CALC sucesor, no a reescribir resultados sellados.

## Auditoría de rigor extremo

Las tasas INE son registros administrativos; ENCUP y LAPOP son respuestas
de personas con escalas y errores distintos. Todo el programa es
RETROSPECTIVA. Los porcentajes entre instrumentos no se promedian ni se
tratan como transición de la misma población. La falta de respuesta y de
captura puede sesgar, incluso cuando un IC muestral es estrecho. Cultura,
institución, estructura, incentivos y decisión individual no se colapsan.
El lente rural, indígena y popular podría modificar niveles, pero no hay
cruce autorizado que lo cuantifique aquí. Ningún dato genético se usa para
predecir conducta grupal. El peligro práctico es interpretar exposición a
una oferta como aceptación o usar diferencias geográficas para seleccionar
personas; ambos usos quedan excluidos. Las cifras del estado del corpus
proceden de la clasificación por ID del manifiesto; no de un prefijo sin
hits. Hay tres CALC activos sellados nuevos y un cuarto archivado intacto
con dos reactivos NO-ESTIMABLE de ENCUP `0002`; los activos aportan las
tablas útiles y siguen pendientes de adopción. No se altera ningún contador global ni
celdas_validadas.
