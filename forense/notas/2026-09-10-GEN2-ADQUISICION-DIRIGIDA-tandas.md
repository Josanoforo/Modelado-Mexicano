# GEN2-ADQUISICION-DIRIGIDA-Y-DIN · búsqueda académica sobre tandas

Fecha de búsqueda: 10 de septiembre de 2026. Pregunta: evidencia mexicana
medible de selección, reputación, incumplimiento, sanciones, frecuencia y monto
en ROSCA/tandas. Se partió del informe `GEN2-UNIVERSO-C` y se siguieron autores,
citas y repositorios; no se reabrió la vía comercial diferida por D18.

## Veredicto

La conclusión previa de “sin ruta mexicana” no sobrevive. Hay una ruta
inmediata para mecanismos y atributos de grupo (Campos 1998) y otra para
participación, montos, duración y transiciones individuales (ENNViH 2002–2012,
ya en el corpus). Sigue sin aparecer un ledger mexicano abierto de grupos,
turnos y pagos que permita calcular una tasa de incumplimiento. El `10%` de
Campos es una razón de abandono entre ex participantes, no una tasa de impago.

## Candidatos priorizados

### 1. Pilar Campos (1998) — ruta directa de mecanismo y atributos

Dos encuestas: nacional de noviembre de 1997 (`n=1 200`, 68 localidades, 32
entidades, muestra multietápica) y DF/Guadalajara/Monterrey de enero de 1996
(`n=741`). Permite transcribir participación, razón de entrada y salida, número
de miembros, duración, periodicidad y fondo total. La narración documenta
conocimiento laboral/vecinal como filtro, admisión de personas cumplidas,
exclusión futura, daño reputacional, reserva de la organizadora y presión
comunitaria.

Resultados útiles: 66% declara ahorro como razón principal; 10% de quienes
dejaron tandas menciona pago incompleto; la mitad reporta grupos de diez
miembros, una quinta parte de once; cerca de un tercio describe dos meses con
pagos semanales; 40% reporta fondos de 500–1 000 pesos nominales de los noventa.

Acceso y recibo: `campos_1998_tandas_mexico_pdf`, URL
`https://sociologicamexico.azc.uam.mx/index.php/Sociologica/article/download/560/533/1103`,
sha256 `6cb62eaa7b3e26db6da9a01ac664ba5119c23e00fd29a893f9c33cdb07e53748`,
3 805 683 bytes, PDF de 24 páginas legible, dos descargas idénticas, payload en
`data_raw:academico_tandas_mexico/Campos-1998-Las-tandas-en-Mexico.pdf` y fuera
de Git. Condición: artículo académico de acceso público UAM, uso de
investigación con atribución.

Paso de medición: digitalizar tablas/gráficas conservando denominador y encuesta
de origen; separar `salida_pago_incompleto`, `tamano_grupo`, `duracion`,
`periodicidad`, `fondo_nominal`, `filtro_reputacional_descrito` y
`sancion_descrita`. Reserva: el texto da 49% de participación alguna vez y una
nota 41%; varias gráficas tienen pie nacional 1997 aunque el texto las atribuye
a tres ciudades 1996. Registrar `procedencia_ambigua`, no resolver por
inferencia.

### 2. ENNViH/MxFLS 2002–2012 — ruta individual longitudinal

Panel nacional urbano/rural y regional: línea base aproximada de 8 400 hogares,
35 000 personas y 150 comunidades; olas 2002, 2005–06 y 2009–12. Los ZIP ya
están en `data_raw:ennvih/` y en el manifiesto.

- 2002/2005, `iiib_cr.dta`: `cr04` participación; `cr05a_2` aportado,
  `cr05b_2` recibido y `cr05c_2` por recibir.
- 2009, `iiib_cr.dta`: `cr04` participación últimos doce meses; `cr05_2`
  recibido/por recibir; `cr05a_1` unidad y `cr05a_21/22/23` duración en
  días/semanas/meses.
- 2005/2009, `iiib_rg.dta`: `rg08_11`, probabilidad hipotética de invertir el
  ingreso mensual en una tanda; no es incumplimiento ni reputación observada.

Paso de medición: excluir proxies, recodificar especiales, enlazar personas
longitudinalmente, usar los ponderadores correctos, deflactar montos y homologar
duración. Produce participación por ola, entrada/salida y asociaciones con
ingreso, sexo, escolaridad, pareja y preferencias. No identifica grupo,
organizadora, turno, cuota incumplida ni sanción. `cr04` no mide número de tandas
por año y en 2009 se registra la más reciente. El cuestionario gobierna la
semántica de `cr05`; la etiqueta inglesa “amount given” es inconsistente con él.

### 3. BANSEFI–CIESAS–UIA (2006) — puente cualitativo

Estudia 116 hogares de 21 localidades en 13 estados, seleccionados desde la
EACPM. Aporta casos y tablas sobre confianza, vínculos preexistentes,
organizador, frecuencia/duración, aportación y fondo: 10–30 semanas o 10–20
quincenas, aportaciones de 50–1 500 pesos y fondos de 1 000–22 500 pesos; la
mayoría de usuarias observadas participaba una vez al año y algunas dos.

Acceso y recibo: `bansefi_patmir_estudio_cualitativo_2006_pdf`, URL
`https://www.gob.mx/cms/uploads/attachment/file/302502/7.2_Estudio_Cualitativo_BANSEFI-PATMIR-Abril_2006.pdf`,
sha256 `f1ff23f78bce4e7ef076422163bcda41e4bf2f865cae79886cbd6a8bcc13b98a`,
1 116 816 bytes, PDF de 233 páginas legible, dos descargas idénticas, payload en
`data_raw:academico_tandas_mexico/Estudio-Cualitativo-BANSEFI-PATMIR-2006.pdf`,
fuera de Git. Condición: documento público BANSEFI-PATMIR en gob.mx, uso con
atribución. Codificar como casos cualitativos; no ponderar ni presentar como
prevalencia nacional.

### 4. Luengas-Sierra (2023) — selección hacia participación

Usa mujeres mexicanas en pareja en MxFLS 2005–06/2009–12 (`n=2 056` agrupadas;
1 029 primeras diferencias, 90 municipios). Desenlace exacto `cr04`, tandas en
últimos doce meses; predictores de ingreso relativo, paciencia y participación
de pareja. Working paper:
`https://pavellsierra.com/WPIntrahouse.pdf`. Las regresiones publicadas no usan
ponderadores; el paso defendible es reproducir diferencias/IV y después ampliar
con monto y duración del instrumento local.

### 5. Fuentes Paniagua (2019) — observación de un grupo

“Los años dorados”, Nezahualcóyotl: 13 mujeres y dos hombres, cuatro meses de
observación, 24 entrevistas y 24 relatorías. Documenta tandas consecutivas,
ingreso ocasional por recomendación, cuota/turno fijos, registro de la
organizadora e incumplimiento descrito como excepcional y concentrado en turnos
tempranos. Acceso:
`https://revistacienciasyhumanidades.com/index.php/inicio/article/download/235/236/745`.
Sirve para codificar reglas y episodios; “excepcional” no se convierte en tasa.

### 6. Vélez-Ibáñez (1983) — mecanismo, acceso pendiente

Más de 60 participantes mezclando México y Estados Unidos; la síntesis disponible
menciona cuatro personas que conocían desfalcos luego restituidos y un grupo con
veinte años de repetición y 75% de miembros originales. Catálogo:
`https://openlibrary.org/books/OL4271712M`. Sólo se usarán casos explícitamente
mexicanos si se obtiene el libro; “cuatro conocían casos” no es incidencia.

## Separación y descartes

Datos individuales: ENNViH, ENIF/ENSAFI y Luengas-Sierra; permiten participación,
perfil, monto y transiciones, no impago grupal. Datos de grupo: no apareció una
base abierta; Campos trae atributos reportados por individuos y las fuentes
cualitativas aportan casos. Experimentos mexicanos sobre exclusión o
incumplimiento: ninguno localizado. Un experimento japonés de exclusión informa
mecanismo, no calibra México.

Universo de búsqueda: combinaciones español/inglés de tanda/ROSCA con
incumplimiento/default, reputación/trust, selección/recruitment,
sanción/exclusion, organizador, monto y frecuencia, en web y repositorios UAM,
CIDE, CIESAS, Colmex, UNAM, INEGI/CNBV, gob.mx, MxFLS, Dataverse, Zenodo y OSF;
se siguieron las citas de Campos, Vélez-Ibáñez, Kurtz/Showman y Cope/Kurtz.

Descartes para no repetir: no se localizó microdato CIDAC/Reforma ni la base
NVivo BANSEFI; ENIF/ENSAFI no contienen reputación/sanción/incumplimiento de la
tanda; muestras mexicano-americanas en EE. UU. no calibran México; crédito
grupal de microfinancieras no es ROSCA; “Tandas para el Bienestar” es un programa
de microcrédito; fraude/Ponzi/prensa carecen de denominador. La búsqueda termina
porque ya hay ruta medible para atributos e individuos; la tasa de
incumplimiento queda residual explícita, no una afirmación de inexistencia
mundial.
