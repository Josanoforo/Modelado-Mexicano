# Pisos de confianza institucional por eje · ENCIG 2023 · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-PISOS-Y-ADENDAS-1` (P1), 28/sep/2026, CAJA, rama `acto/gen2-pisos-y-adendas-1`, 0-bis `fa42a3c1`. Encargo `forense/encargos/2026-09-28-GEN2-PISOS-Y-ADENDAS-1.md`; firma de mesa **H4 (a)** (28/sep/2026, «firmado», interpretación declarada en `forense/encargos/2026-09-28-GEN2-TRAMITE-HOJA-FIRMAS-21-1-ADENDA-1.md`; FP `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-27`). CALC `CALC-ENCIG2023-CONFIANZA-PISOS-0001`. MODO RÍGIDO desde este COMMIT-1: spec, códigos y medidor (`data/corrida0/CALC-ENCIG2023-CONFIANZA-PISOS-0001/medidor.py`) se congelan juntos **antes de abrir el microdato**; los códigos salen del descriptor y del cuestionario por texto de pregunta (A.15). Ninguna ejecución diagnóstica sobre el dato: la primera corrida es `corrida0 run`.

**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas (A.8, E.5)

- `[EJECUTADO]` Ningún CALC sellado mide confianza desde ENCIG: 44 carpetas previas `data/corrida0/CALC-*ENCIG*` (45 con la de este acto), `rg -l "P11_1"` → 1 archivo y `rg -il confianza` → 1, en ambos casos sólo el `medidor.py` de este CALC; control positivo: `rg -l "P7_3"` → 53 archivos en esas mismas carpetas. Lo sellado de ENCIG mide trámite digital (`P7_3`: `CALC-PISOS-ENCIG2023-EJES-0001/-0002`, `CALC-ENCIG2023-CRUCES-HISTORICOS-*`, `CALC-ASTRA-ENCIG-*`), mordida (`P8_3/P8_4`: `CALC-ENCIG-2023-0001`, `CALC-B-MARCO-ENCIG-0001`) y la rejilla 2025 del árbitro (`CALC-ARBITRO-MARGINALES-ENCIG2025-0001`); la serie de `ENCIG-SERIE-Y-TENDENCIA-1` (#972) tampoco usa la sección XI. **Se citan; no se re-miden**, y no hay oro sellado contra el cual reproducir: esta es la primera medición de la sección XI. Coincide con la NC `NC-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-02` (0 de 41 entonces).
- `[EJECUTADO]` **Ola.** El encargo prohíbe abrir ENCIG 2025 fuera de lo que su árbitro abrió (PARO a); el árbitro abrió la rejilla de gobierno digital, no la sección XI. Aunque `canon/MEMORIA-OPERATIVA.md` §1 lista «ENCIG 2025: abierta», este acto se rige por su lista cerrada de PAROS: **P1 usa ENCIG 2023** y lo declara. 2023 es ola ya vista por otros CALC (otras secciones): toda cifra es **RETROSPECTIVA**.
- `[EJECUTADO]` Payload `encig23_base_datos_csv` (`encig23_base_datos_csv.zip`, sha256 `af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d`, COINCIDE en caja). Miembros por envoltura (A.7, sin abrir): `encig2023_01_sec_11.csv` (15 534 403 B) y `encig2023_02_residentes_sec_2.csv` (22 587 145 B), entre seis.
- `[LEÍDO]` Descriptor `encig23_estructura_base_datos_pdf` (sha256 `eb89820cd58af0d8799387a376b9e60b062ed59daea74cdbea7ff3b4ee13a906`; el manifiesto lo registra como sustituto funcional del FD) §2.1 y §3.6 (tabla `encig2023_01_sec_11`, 68 variables, llave `CVE_ENT, UPM, V_SEL, R_ELE`), §3.2 (`encig2023_02_residentes_sec_2`); cuestionario `encig23_cuestionario_pdf` (sha256 `65000ad38419da504e46b34a0a2426f218d1ba6e604ad37a14762bbd07881e1e`) sección XI, p. 23.

## 1 · Unidad, universo, diseño

- **Unidad: persona** de 18 años y más, informante seleccionado de la vivienda (tabla de la sección XI). Ninguna cifra de este CALC es de unidad hogar, trámite ni delito; ninguna se promedia con una de otra unidad.
- **Universo de la encuesta** (descriptor, objetivo): «población de 18 años y más en **ciudades de 100 mil habitantes y más**». No hay cobertura rural ni de localidades menores: toda afirmación es sobre ese universo urbano.
- **Marco**: filas de `encig2023_01_sec_11.csv` con `FAC_P18` (factor de expansión para la población de 18 años y más) numérico, finito y > 0, y `EST_DIS` (estrato de diseño) y `UPM_DIS` (UPM de diseño) no vacíos tras recortar espacios. `EST_DIS`/`UPM_DIS` son **llaves de texto opacas**: nunca se convierten a número ni se rellenan.
- **Enlace**: `SEXO`, `EDAD` y `NIV` salen de `encig2023_02_residentes_sec_2.csv` por `ID_PER` (texto recortado; unión izquierda; `ID_PER` único en residentes o el medidor falla). Una persona sin enlace queda en el marco (nacional y entidad) y sin categoría en sexo, edad y escolaridad; se cuenta en `…-FILAS-SIN-ENLACE-RESIDENTES`.

## 2 · Reactivos (por texto; A.15)

Pregunta 11.1 del cuestionario, sección XI «CONFIANZA EN INSTITUCIONES»: «En su opinión, ¿cuánta confianza le generan…», un solo código, tarjeta B. Códigos (descriptor §3.6, idénticos en los 25 reactivos): `1` Mucha confianza · `2` Algo de confianza · `3` Algo de desconfianza · `4` Mucha desconfianza · `5` No aplica · `9` No sabe / No responde. Los 25 reactivos, **tal como están escritos** (variable `P11_1_<nn>`; id en RESULT `I<nn>`):

01 Universidades públicas · 02 Policías · 03 Hospitales públicos · 04 Presidencia de la República y Secretarías de Estado · 05 Empresarios(as) · 06 Gubernatura de su estado/Jefatura de gobierno (CDMX) · 07 Compañeros(as) del trabajo (Jefes[as] o subordinados[as]) · 08 Presidencias municipales de su estado/Alcaldías (CDMX) · 09 Parientes como tíos(as), primos(as), sobrinos(as), etcétera · 10 Sindicatos · 11 Vecinos(as) · 12 Cámaras de Diputados y Senadores · 13 Medios de comunicación · 14 Institutos electorales · 15 Comisiones de derechos humanos · 16 Escuelas públicas de nivel básico · 17 Jueces(ezas) y Magistrados(as) · 18 Instituciones religiosas, su iglesia o grupo religioso · 19 Partidos políticos · 20 Guardia Nacional · 21 Ejército y Marina · 22 Ministerio Público o Fiscalía Estatal · 23 Servidores(as) públicos(as) o empleados(as) de gobierno · 24 Organizaciones de la Sociedad Civil (ONG'S) · 25 Organismos Públicos Autónomos/Descentralizados (CONAPRED, INE, CNDH, INEGI, etcétera).

Se miden los 25 porque el encargo pide «instituciones del cuestionario tal como están escritas» y el cuestionario los pregunta juntos; 05, 07, 09 y 11 son **actores**, no instituciones, y así se leen (confianza interpersonal por rol). `P11_1A_*` (calificación de desempate) no se usa.

**Lectura de códigos**: texto recortado convertido a entero (así `1` y `01` son el mismo código; lo no convertible no tiene código). **Desenlace** por reactivo: 1 si el código es 1 ó 2 («mucha» o «algo de confianza»); 0 si es 3 ó 4; **fuera del denominador** si es 5, 9, vacío u otro. Nada se imputa. Por reactivo se reportan además, sobre el marco y sin ponderar, los conteos de `5` (`-N-NO-APLICA`), `9` (`-N-NSNR`) y de todo lo demás fuera de 1–5/9 (`-N-OTRO`, que debería ser 0 o casi: si no, la lectura de códigos está mal y se ve).

## 3 · Ejes (univariados; uno a la vez, nunca cruces)

Orden fijo; los códigos se leen como enteros (texto recortado); lo que no cae en una categoría queda **fuera sólo de ese eje**, y se cuenta en `…-EJE-<EJE>-N-SIN-CATEGORIA`.
1. `NACIONAL`: `MX`.
2. `ENTIDAD`: `CVE_ENT` de la sección XI, 1–32 → `01`…`32` (catálogo de entidad del descriptor).
3. `SEXO`: `1` Hombre → `HOMBRE`; `2` Mujer → `MUJER`.
4. `EDAD` (años cumplidos; `97` = «97 años o más»; `98`/`99` = edad no especificada): 18–29 → `18-29`; 30–44 → `30-44`; 45–59 → `45-59`; 60–97 → `60-MAS`; 98, 99, < 18 o no entero → sin categoría.
5. `ESCOLARIDAD` (`NIV`, pregunta 2.7 «¿Hasta qué año o grado aprobó (NOMBRE) en la escuela?»): `0` Ninguno, `1` Preescolar → `NINGUNA`; `2` Primaria, `3` Secundaria → `BASICA`; `4` Carrera técnica con secundaria terminada, `5` Normal básica, `6` Preparatoria o bachillerato → `MEDIA-SUPERIOR`; `7` Carrera técnica con preparatoria terminada, `8` Licenciatura o profesional, `9` Maestría o doctorado → `SUPERIOR`; blanco u otro → sin categoría. `GRA` no se usa.
6. **Tamaño de localidad: NO-CONSTRUIBLE** (E.5, A.15). Texto buscado (`rg -ic`, `pdftotext -layout`): `TLOC`, `TAM_LOC`, «tamaño de localidad», «localidad», «rural», «urbano» en el descriptor completo (las seis tablas, §3.1–§3.6, 4 462 líneas) y en el cuestionario (1 860 líneas). Aciertos: «localidad» 0 en el descriptor y 1 en el cuestionario (el campo de identificación geográfica de la portada, no una pregunta ni una variable); «urbano» 3 + 3, todos «transporte público tipo autobús urbano» (5.9); los demás 0. Ninguna variable de tamaño de localidad. Por diseño la encuesta sólo cubre ciudades de 100 mil habitantes y más, así que el eje no tiene variación que medir. `AREAM` (área metropolitana: «Resto de ciudades de 100 mil habitantes y más» y áreas metropolitanas nombradas) no es tamaño de localidad y **no se sustituye**; `EST` (1–4, «Estrato», sin etiquetas en el descriptor) tampoco. Queda como NC con su razón.

## 4 · Estimación

Por reactivo × eje × categoría (25 × 43 celdas):
- **Punto** `P` = Σ `FAC_P18`·desenlace / Σ `FAC_P18` sobre las personas del marco en la celda con desenlace 0/1 (factor sin normalizar). `N` = número de esas personas, sin ponderar. Si la masa es 0, `P` es nulo.
- **IC por diseño**: bootstrap de UPM con reposición **dentro de estrato**, sobre el **marco entero** (una UPM sin personas en la celda aporta (0, 0) y sigue en su estrato). Conglomerado = par (`EST_DIS`, `UPM_DIS`); pares ordenados lexicográficamente; estratos en orden lexicográfico; generador `numpy.random.Generator(PCG64(20260928))`; `R = 2000` réplicas; para cada estrato con `m` UPM, una sola llamada `integers(0, m, size=(R, m))` que fija los conteos de las `R` réplicas; las **mismas** réplicas sirven a todas las celdas. Estrato con una sola UPM: se re-sortea a sí misma (aporta varianza cero; se declara, no se colapsa con otro estrato). Réplica = Σ conteo·numerador / Σ conteo·denominador. `IC-LO`/`IC-HI` = percentiles 2.5/97.5 (`numpy.percentile`, lineal); `EE` = desviación estándar de las réplicas (`ddof = 1`).
- **Contrato conservador**: si alguna réplica tiene denominador 0, `IC-LO`, `IC-HI` y `EE` son nulos (no se descartan réplicas). No hay supresión por precisión: cada celda lleva su `N` y su IC, y quien consuma el piso decide; una celda con `N` pequeño se lee con su IC.
- **Globales**: `FILAS-SEC11`, `FILAS-MARCO`, `FILAS-SIN-ENLACE-RESIDENTES`, `UPM`, `ESTRATOS`.
- Tolerancia de replay: flotante `abs 1.0e-10` (determinista por semilla, sumas float64).

## 5 · Controles y secuencia

- Antes del COMMIT-1: prueba sintética (`forense/notas/2026-09-28-GEN2-PISOS-Y-ADENDAS-1/p1_prueba_sintetica.py`): ZIP fabricado con los mismos miembros y columnas, `medir()` real, y `corrida0._valida_outputs` sobre (i) caso normal, (ii) una entidad sin personas (masa 0 → nulos) y (iii) una categoría con una sola UPM; más `corrida0 preflight` VERDE sobre el CALC. No toca el corpus.
- `resultados:` del `spec.yaml` se genera de `esquema_resultados()` del medidor (no a mano).
- COMMIT-1 (esta spec + sidecar + `spec.yaml` + `medidor.py`) → `corrida0 run` → COMMIT-2 (sello y tabla de lectura en la nota). Nada se re-corre para mejorar un resultado.

## 6 · Auditoría (afirma sobre México; v2.16)

- **Contadores:** mueve `cuenta_gen2` (RESULT nuevos con cadena E.2); **no adopta** (la adopción es de mesa por merge: ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR); no mueve `celdas_validadas` (no hay R).
- **Unidad y escala:** persona 18+; proporción de «mucha o algo de confianza» en la escala de 4 puntos de ENCIG. No se compara con la confianza 1–7 de LAPOP, la 1–4 de WVS/Latinobarómetro ni ninguna otra escala sin función de enlace; sólo dirección descriptiva, rotulada.
- **PROSPECTIVA / RETROSPECTIVA:** todo RETROSPECTIVO (ola 2023 ya vista en otras secciones); nada es PROSPECTIVA y ninguna frase las mezcla.
- **¿Qué parece psicológico y es incentivo o exposición?** La confianza institucional por entidad refleja primero **exposición y desempeño** (victimización, trato en trámites, presencia de Guardia Nacional o Ejército, alternancia política local), no una «actitud regional»; un gradiente por escolaridad es primero ingreso, empleo formal y contacto con las instituciones. Baja confianza en policías o partidos puede ser evaluación racional de instituciones con desempeño medible.
- **Sobregeneralización desde clase media urbana:** el universo es **sólo urbano de 100 mil habitantes y más**; nada de aquí describe al México rural, indígena o de localidades pequeñas, y el eje de tamaño de localidad es NO-CONSTRUIBLE por eso mismo. No se trata a los mexicanos como bloque: los pisos son por eje.
- **Procedencia de la evidencia:** (a) datos primarios en México (INEGI). Nada es (b) ni (c).
- **Evidencia débil / intuición fuerte:** un piso descriptivo no identifica causa; «confían más en el Ejército que en la policía» es una marginal, no un mecanismo.
- **Cifra escrita a mano:** ninguna; conteos del §0 con su comando.
