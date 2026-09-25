# Estructura ENCODAT 2016-2017 — investigación de metadatos

## RESERVA
No se abrió nada con `encodat_2025`, `ensanut_2025` ni `reserva_respondentes`. Confirmado por diseño de la tarea.

## Archivos y verificación sha256 (todos leídos SOLO metadatos vía `pyreadstat.read_dta(metadataonly=True)`, encoding UTF-8)

| id | sha256 manifiesto | resultado |
|---|---|---|
| encodat_2016_2017__encodat_2016_2017_individual_stata_stata_zip | bb0c7d99...346 | COINCIDE |
| encodat_2016_2017__encodat_2016_2017_integrantes_stata_stata_zip | 938a23ea...ffe0c3 | COINCIDE |
| encodat_2016_2017__encodat_2016_2017_hogar_stata_stata_zip | 716f58f8...d0d781 | COINCIDE |
| encodat_2016_2017__encodat_2016_2017_individual_catalogo_xlsx | 12afb670...490b8b | COINCIDE |
| encodat_2016_2017__encodat_2016_2017_integrantes_catalogo_xlsx | b7affa16...ff1fb5a0 | COINCIDE |
| encodat_2016_2017__encodat_2016_2017_hogar_catalogo_xlsx | c125d639...82db81e | COINCIDE |
| encodat_2016_2017__cuestionario_encodat_individual_2016_2017_cuestionarios_pdf | 6236d6f3...b3c85a2 | COINCIDE |
| encodat_2016_2017__cuestionario_encodat_hogar_2016_2017_cuestionarios_pdf | bc0175e2...984ed7a | COINCIDE |

Nota técnica: los .dta requieren `encoding="UTF-8"` explícito en `pyreadstat.read_dta` (el default falla o produce mojibake en Individual/Hogar).

## A) Diseño muestral y llaves de unión

- **Hogar** (n=55907 filas de hogar; 48 variables): `id_hogar`, `entidad`, `desc_ent`, `munici`, `desc_mun`, `locali`, `desc_loc` (identificación geográfica); `estrato` ("Estrato"), `code_upm` ("UPM"), `est_var` ("Estrato" — nombre repetido, posible variable de varianza distinta a `estrato`), `ponde_hh` ("Ponderador") = factor de expansión del hogar.
- **Integrantes** (n=203087 filas de integrante; 20 variables): llave `id_hogar` + `intp` ("Integrante en el Hogar", numerador dentro del hogar) → llave compuesta integrante↔hogar. Trae también `entidad`, `munici`, `locali`, `est_var` ("Estrato de varianza"), `code_upm` ("UPM en muestra"), `estrato` ("Estrato"), `ponde_ii` ("Ponderador INTEGRANTES"), `intsel` ("Seleccionado cuestionario individual" — bandera de selección del individual dentro del hogar).
- **Individual** (n=56877 filas de respondiente individual; 1715 variables) — aún por examinar llaves exactas (ver abajo, sección en construcción).
- No se ha confirmado aún si existe variable de "región" (8 regiones ENCODAT) o "entidad" en Individual — pendiente de grep sobre las 1715 etiquetas.

**Individual (56877 filas, 1715 variables):** llave propia `id_pers` ("Identificador de la persona", ancho de columna 22 — cadena, probablemente compuesta; no se leyó ningún valor, solo el catálogo, que no documenta la composición). También trae `entidad`, `desc_ent`, `munici`, `desc_mun`, `locali`, `desc_loc` (geografía) y `ponde_ss` ("Ponderador SELECCIONADOS para rondas 1 y 2 (6 de febrero)") = factor de expansión propio del individual. **No tiene** variables `estrato`/`upm`/`est_var`/`code_upm` propias — el diseño (estrato, UPM, varianza) vive en Hogar/Integrantes y debe unirse vía la llave de hogar (no confirmado el nombre exacto del campo de unión en Individual: no hay `id_hogar` ni `intp` como nombres de columna en Individual; sólo `id_pers`).
**No existe variable de "región" (8 regiones ENCODAT)** en ninguno de los tres archivos (grep `region` → 0 resultados en nombres/etiquetas de Hogar, Integrantes, Individual). `entidad` sí existe en los tres.

## B) Segmentadores en Individual/Integrantes

- Sexo: `ds2` "Marque el sexo del entrevistado" (Individual); `h303` "¿(NOMBRE) es hombre o mujer?" (Integrantes).
- Edad: `ds3` "¿Qué edad tiene usted?" (Individual, escala) + `ds4a/b/c` fecha de nacimiento; `h304` "¿Cuántos años cumplidos tiene (NOMBRE)?" (Integrantes).
- Escolaridad: `ds9` "¿Cuál fue el último grado que ha completado o completó en la escuela?" (Individual); no hay variable "escolaridad" nombrada como tal, ni "nivel"/"grado" en Integrantes.
- Localidad urbano/rural o tamaño de localidad: **no encontrado** como variable — sólo `locali`/`desc_loc` (código y nombre de localidad, geografía, no clasificación urbano/rural).
- Entidad: `entidad`/`desc_ent` en los tres archivos.
- Estado civil: `ds6`. Indígena: `ds5`/`ds5a`. Religión: `ds7`.

(sección B: barrida por 1715 nombres/etiquetas de Individual con regex sobre "sexo","edad","escolar","grado","nivel","estudi","urbano","rural","region","entidad","municip" + 48 de Hogar y 20 de Integrantes)

## C) Prefijos de bloques temáticos identificados en Individual (1715 variables)

Conteo por prefijo (primeras letras del nombre de variable): `di`=225, `tb`=191 (tabaco), `dm`=88, `tg`=77, `cd`=76, `al`=75 (alcohol), `tp`=68, `dda..ddl`=61×12=732 (12 bloques repetidos, probablemente detalle por tipo de sustancia), `cod`=36, `ts`=31, `ds`=30 (sociodemográficos), `pr`=26, `ed`=23, `pc`=19, `dp`=5, `dr`=5.

(sección C — se documenta bloque por bloque a continuación, en construcción)

### C1 Alcohol (prefijo `al`, 75 variables) — CUBIERTO
- `al1` "¿Ha consumido alguna vez cualquier bebida que contenga alcohol?" — valores {1:Sí, 2:No} → consumo alguna vez en la vida.
- `al4` "En los últimos 12 meses, ¿tomó alguna bebida que contenga alcohol?" {1:Sí,2:No} → consumo último año.
- `al9` "En los últimos 30 días, ¿tomó alguna bebida que contenga alcohol?" {1:Sí,2:No} → consumo último mes.
- `al7a` "¿Alguna vez ha tomado 4 copas o más en una misma ocasión?" {1:Sí,2:No}
- `al7b` "¿Alguna vez ha tomado 5 copas o más en una misma ocasión?" {1:Sí,2:No}
- `al7c` "¿Alguna vez ha tomado 12 copas o más en un mismo periodo de 12 meses?" {1:Sí,2:No}
- `al11` "Durante los últimos 12 meses ¿Cuál es el mayor número de copas que usted ha tomado...?" valores: {1:"24 o más copas en un solo día",2:"12 a 23...",3:"8 a 11...",4:"5 a 7...",5:"4 copas en un solo día",6:"1 a 3 copas en un solo día",9:"No sabe/No contesta"} — escala de copas máximas en un día, no separa por sexo en el nombre/etiqueta de la variable (la definición estándar 5+/4+ hombres/mujeres no aparece como corte explícito en una sola variable; se arma con `al7a`/`al7b`/`al11` combinados con sexo `ds2`).
- `al12a`-`al12j`: frecuencia de consumo por umbral de copas (24+, 12-23, 8-11, 5-7, 4, 1-3) — bloques `g`a`j` repiten para hombre/mujer explícitamente ("5 o más copas..." dos veces, "4 o más copas..." dos veces): posible desagregación sexo-específica de la definición de consumo excesivo.
- `al3`/`al3_1`/`al3_2`: edad primera bebida.
- `al8`: frecuencia habitual de consumo total.
- `al13a-g`, `al14`, `al15`, `al16`: tipo de bebida y frecuencia por tipo (vino, coolers, cerveza, destilados, pulque, alcohol puro) a distintos umbrales (5+, 4, 1-3 copas).
- `al17` frecuencia de "tomar lo suficiente" en 12 meses; `al18` copas para sentirse borracho; `al19`/`al20` preferencia/marca.
- No se detectó una variable ya-construida de "prevalencia" nombrada como tal (p.ej. "prev_alc"); la prevalencia se derivaría de `al1`/`al4`/`al9`.

**Corrección/adenda a B:** en Hogar, `estrato` tiene etiquetas de valor {1:"Rural", 2:"Urbano", 3:"Metropolitano"} — es SÍ el segmentador urbano/rural/metropolitano buscado en B, pero vive en Hogar y se une a Individual vía folio de hogar (ver nota de llaves abajo), no es una variable propia de Individual. `est_var` (Hogar) no tiene etiquetas de valor definidas (probablemente numérico de estrato de varianza, sin diccionario).

**Corrección/adenda a A — llave de unión:** el cuestionario PDF de Individual (`cuestionario_encodat_individual_2016_2017.Cuestionarios.pdf`, página 1) muestra en la carátula "1. IDENTIFICACIÓN GEOGRÁFICA" + "2. FOLIO DEL HOGAR" — confirma que el diseño usa un FOLIO DE HOGAR para unir el cuestionario individual con el de hogar; `id_pers` (Individual, ancho 22) es consistente con incluir ese folio de hogar más un consecutivo de persona, pero el catálogo no lo documenta explícitamente y no se leyeron valores para confirmarlo (regla dura: no se lee microdato). El cuestionario también documenta el nombre real del estudio en la carátula: "ENCUESTA NACIONAL DE ADICCIONES 2016" (nombre previo/alterno de ENCODAT en el cuestionario impreso) y un filtro de "RANGO DE EDAD" en el resultado de la visita (código 02: "ENTREVISTA CANCELADA PORQUE ESTA FUERA DEL RANGO DE EDAD"), consistente con el universo 12-65 mencionado en el encargo, aunque el rango numérico exacto no apareció en las primeras 6 páginas revisadas del PDF (no se recorrió el PDF completo de 77 páginas por límite de tiempo del encargo).

### C2 Tabaco (prefijo `tb`, 191 variables) — CUBIERTO
- `tb01` "En toda su vida ¿ha fumado más de 100 cigarros, es decir, 5 cajetillas?" {1:Sí,2:No} → fumador alguna vez (criterio de 100 cigarros, estilo CDC).
- `tb02` "¿Actualmente fuma tabaco todos los días, algunos días o no fuma actualmente?" {1:Todos los días,2:Algunos días,3:No fuma actualmente,7:No sabe,9:No responde} → fumador actual.
- `tb05` "¿Ha fumado tabaco alguna vez en su vida, aunque sea una sola fumada?" {1:Sí,2:No} → alguna vez (criterio más laxo que tb01).
- `tb08` "¿Cuándo fue la última vez que se fumó un cigarro?" → deriva último mes/año.
- `tb09`/`tb06`/`tb32`/`tb35` edad de inicio (varias versiones, ex-fumadores vs actuales).
- `tb10a-tb10ff`: cantidad diaria/semanal por tipo de producto (manufacturado, liado, pipa, puro, pipa de agua, otros).
- `tb11a-o`: escala tipo Fagerström/dependencia (urgencia al despertar, dificultad de abstenerse, motivos psicológicos).
- `tb12-tb19b`: intentos de dejar de fumar, métodos usados, consulta médica, líneas de ayuda.
- `tb20-tb31`: compra (presentación, marca, precio, gasto semanal, exigencia de identificación).
- `tb37a-ff`: mismo bloque de cantidades pero en pasado ("fumaba" vs "fuma").
- `tb54-tb62`: exposición a humo ajeno (casa, transporte, restaurante, bar, escuela).
- `tb63-tb70`: exposición a publicidad/promoción de tabaco.
- `tb71-tb73`: percepción de riesgo/daño a la salud.
- `tb74-tb79`: opinión sobre políticas públicas (impuestos, publicidad, pictogramas, Ley General para el Control del Tabaco).
- No hay una variable "fumador_actual" ya derivada con ese nombre; se arma de `tb02`/`tb08`.

### C3 Cigarro electrónico (dentro de prefijo `tb`, 5 variables) — CUBIERTO
- `tb46`: definición leída al entrevistado.
- `tb47` "¿Actualmente consume cigarros electrónicos todos los días, algunos días, o actualmente no?" {1:Todos los días,2:Algunos días,3:Actualmente no consume,9:No responde} → uso actual/último mes (aproximado por frecuencia, no hay corte explícito de "último mes").
- `tb48`: hace cuánto tiempo lo ha usado.
- `tb49`: dónde compró la última vez.
- `tb50` "¿Alguna vez, aunque haya sido una vez, usó un cigarro electrónico?" {1:Sí,2:No,9:No responde} → uso alguna vez.

### C4 Drogas ilegales / drogas médicas fuera de prescripción (prefijos `di`=225, `dm`=88, `ed`=23, `cod`=36, `dd[a-l]`=732) — CUBIERTO
Bloque `di` (drogas ilegales), 9 sustancias con pregunta base "¿Me podría decir si ha tomado, usado, probado 'SUSTANCIA'...?" {1:Sí,2:No,9:No sabe/No contesta} — universo aparente: toda la vida:
  - `di1a` MARIGUANA (también 'hashish', 'mota', 'café', 'yerba') — texto completo obtenido del catálogo XLSX (el .dta trunca etiquetas a ~80 caracteres; el catálogo `.xlsx` trae el texto íntegro).
  - `di1b` COCAÍNA.
  - `di1c` CRACK ('piedra').
  - `di1d` ALUCINÓGENOS (hongos, peyote, LSD, etc.).
  - `di1e` INHALABLES (thiner, PVC, cemento, etc.).
  - `di1f` HEROÍNA, opio ('chiva').
  - `di1g` ESTIMULANTES TIPO ANFETAMÍNICO / droga de diseño / éxtasis / MDMA / cristal (METANFETAMINAS).
  - `di1h` OTRAS DROGAS: ketamina (special K), GHB ('éxtasis líquido').
  - `di1i` Mariguana Sintética (Spice, K2).
  Cada sustancia repite un sub-bloque `di2xx`/`di3xx` (nombre del producto consumido, vía de uso) — no hay variable de "cualquier droga ilegal alguna vez" ya combinada con ese nombre exacto; se construiría como máximo/unión de `di1a..di1i`.
- Bloque `dm` (drogas médicas fuera de prescripción/sin receta), 4 categorías con el mismo patrón {1:Sí,2:No,9:No sabe/No contesta}:
  - `dm1a` Opiáceos: "para aliviar el dolor severo como la morfina, nubain, darvon, demerol, roxanol, codeína, talwin, láudano, bupreno[rfina]" (texto completo vía catálogo xlsx) — **no menciona tramadol explícitamente por nombre**, pero es la categoría de opioides.
  - `dm1b` Tranquilizantes (para calmar).
  - `dm1c` Sedantes y Barbitúricos (para dormir/relajar: equanil, mandrax, sevenal, sopor — 'pastas'/'chochos'/'quesos'/'pacidinas').
  - `dm1d` Anfetaminas o estimulantes (para bajar de peso/energía: ritalín, asenlix, diestet, benzedrina, actedrón, captagón, tenuate).
  - Existe un set `dm1a2..dm1d2` que repite la pregunta con etiqueta idéntica (segunda ronda del cuestionario, ver también `di1a2` etc. no listado arriba por espacio) — patrón de "dos rondas" (posiblemente ronda de recordatorio/ronda de verificación, sin documentación adicional en el catálogo).
  - No se encontró variable con "tramadol", "opioide", "morfina", "codeína" o "fentanilo" como *nombre de variable* — sólo aparecen como ejemplos dentro del texto de la etiqueta de `dm1a` (opiáceos).
- `cod_*`: variables abiertas para capturar el NOMBRE textual del producto consumido por categoría (op=opiáceos, tra=tranquilizantes, sed=sedantes, anf=anfetaminas, mar=mariguana, coc=cocaína, cra=crack, alu=alucinógenos, inh=inhalables, her=heroína, met=metanfetaminas, od=otras drogas), hasta 3 nombres por categoría — 36 variables, probablemente texto abierto codificado post-hoc; es la vía por la que "tramadol" (si alguien lo mencionó) quedaría registrado como texto libre codificado, no como variable dedicada.
- `dd[a-l]`: bloque de 12 sustancias × 61 preguntas cada uno (732 variables) — patrón tipo escala de dependencia/abuso (se observó texto de `dda7a`: "¿Alguna vez tuvo síntomas de abstinencia... cuando consumía menos, dejaba de consumir o estaba sin consumir 'opiáceos'?"), replicado para cada una de las 12 categorías de sustancia (dda=opiáceos, ddb=tranquilizantes, ddc=sedantes/barbitúricos, ddd=anfetaminas/estimulantes, dde=mariguana, ddf=cocaína, ddg=crack, ddh=alucinógenos, ddi=inhalables, ddj=heroína/opio, ddk=?, ddl=otras drogas ketamina/Special K/GHB) — parece ser el módulo de criterios de dependencia/abuso (tipo DSM) aplicado por sustancia, con sufijo `ab` para repetir "¿Pasó esto en los últimos 12 meses?" (recorte alguna-vez vs último año).
- `ed1-ed11`: oferta/disponibilidad de mariguana y otras drogas (regalada/para comprar), edad de la primera oferta, percepción de facilidad para conseguir drogas (`ed11`, escala Imposible→Muy fácil).
- Mariguana específica: cubierta dentro de `di1a` (alguna vez) y en `dd e*` (dependencia), no tiene bloque propio separado de "último año" explícito fuera de los sufijos `ab`="¿Pasó esto en los últimos 12 meses?" dentro de `dd*`.

### C5 Salud mental (Kessler, ideación/intento suicida, depresión) — NO ENCONTRADO
Se buscaron los términos "suicid", "depres", "psicológic", "Kessler", "malestar", "ansiedad", "ánimo" sobre los 1715 nombres y 1715 etiquetas completas (catálogo xlsx) de Individual: 0 coincidencias para suicidio, depresión, psicológico o Kessler. "malestar" aparece 36 veces pero siempre dentro de la frase fija de síntomas de abstinencia por sustancia (bloque `dd*`, ver C4), no una escala de malestar psicológico general. "ansiedad" aparece 2 veces (`tb11h` fumar-para-controlar-ansiedad; `pr11` "me ayuda a disminuir la ansiedad" en el contexto de "pre-copeo"/alcohol), no como ítem de tamizaje de salud mental. Los bloques `dp` (5 variables) y `dr` (5 variables) son escalas de discapacidad/funcionamiento (0-10, estilo WHODAS) atribuidas específicamente al consumo de sustancias/alcohol en los últimos 12 meses (capacidad de trabajar, relaciones, vida social, días incapacitado) — NO son una escala general de salud mental. Conclusión: ENCODAT 2016-2017 Individual, tal como está documentado en catálogo+.dta, no trae un módulo de salud mental general (Kessler K6/K10, PHQ, ideación suicida); no se revisó Hogar/Integrantes para C5 porque no aplica (serían del respondiente, no del hogar) y sus 48+20 variables ya fueron listadas íntegras arriba sin ningún ítem de salud mental.

### C6 Acceso a tratamiento/servicios (prefijos `tg`=77, `tp`=68) — CUBIERTO
- `tg1` "¿Alguna vez ha estado en tratamiento por consumir alcohol?" {1:Sí,2:No,9:No sabe/No contesta}.
- `tg11` "¿Alguna vez ha estado en tratamiento por consumir drogas médicas sin receta o drogas ilegales?" {1:Sí,2:No,9:No sabe/No contesta}.
- `tg2`/`tg3`/`tg12`/`tg13`: cómo llegó a tratamiento (juez/ministerio público, escuela/trabajo) — vía de entrada, relevante para "oferta antes que preferencia" (entrada forzada/canalizada vs búsqueda propia).
- `tg7`/`tg17`: si el tratamiento logró dejar de consumir totalmente.
- `tg10a`/`tg21`: hospitalización por consumo de alcohol/drogas.
- `tg10d`/`tg24`: desintoxicación.
- `tg10g`: internamiento psiquiátrico/residencial por alcohol.
- `tg10j`: tratamiento ambulatorio.
- `tg10ha-tg10ke`, `tg28a-e`, `tg31a-e`: lugar donde recibió atención — {Centros de Integración Juvenil, Unidad de tratamiento pública (Secretaría de Salud/IMSS/ISSSTE), institución privada, "Anexo coordinado por ex-adictos", No sabe/No contesta} — esta variable es la más directa para "oferta antes que preferencia": distingue oferta pública vs privada vs anexo (no regulado) vs juvenil.
- `tp1` "¿Alguna vez en su vida ha consultado a algún profesional de la salud por su uso de alcohol o drogas, como por ejemplo, psiquiatra, psicólogo, grupo de autoayuda, etc.?" {1:Sí,2:No,9:No sabe/No contesta} → variable general de "¿buscó ayuda?".
- `tp2i`/`tp3i`/`tp5i`: consulta a grupo de autoayuda/Alcohólicos Anónimos, número de veces, si completó el tratamiento.
- `tp6c`/`tp6i`: barreras percibidas ("piensa que necesita ayuda pero cree que el tratamiento profesional no le ayudaría"; "el problema acabó solo y ya no necesitaba más ayuda") — razones de no búsqueda, útiles para modelar preferencia vs oferta.
- Tabaco tiene su propio sub-bloque de ayuda: `tb14a-i` (orientación, reemplazo de nicotina, medicamentos, líneas telefónicas, redes sociales), `tb45` (conoce centros de ayuda para dejar de fumar), `tb15-tb18` (consulta a médico/profesional de salud por tabaco).

## Resumen de secciones/prefijos aún sin desglosar variable por variable (mencionados pero no tabulados exhaustivamente por límite de tiempo)
- `dd[a-l]` (732 variables, 12 sustancias × 61 ítems): se examinó el patrón general (síntomas de abstinencia, con sufijo `ab`="¿pasó en últimos 12 meses?") vía el primer ítem de cada bloque; no se leyeron las 61 preguntas completas por sustancia.
- `ts` (31), `pc` (19), `pr` (26): mostrados íntegros arriba (normas sociales percibidas, prevención, pre-copeo).
- `ds` (30, sociodemográficas de Individual): mostradas íntegras (sexo, edad, fecha nacimiento, indígena, estado civil, religión, escolaridad, situación laboral).

## Archivos abiertos (resumen final)

| id | sha256 (manifiesto) | verificación |
|---|---|---|
| encodat_2016_2017__encodat_2016_2017_individual_stata_stata_zip | bb0c7d999e45bebcffb3a26da00bd2d5caa2d982de7d9e330211c11960153346 | COINCIDE |
| encodat_2016_2017__encodat_2016_2017_integrantes_stata_stata_zip | 938a23ea3b16981b9fb0d5d370e8f1b8b0dabb057a2bd40220ec31b122ffe0c3 | COINCIDE |
| encodat_2016_2017__encodat_2016_2017_hogar_stata_stata_zip | 716f58f817f3203ec2cba8d265d8812d3015bb9ffdb56a39ff50bd3ce1d0d781 | COINCIDE |
| encodat_2016_2017__encodat_2016_2017_individual_catalogo_xlsx | 12afb670424e07f5833123a71bb0d4e4b42b4c3687a7879bd16718e2d9490b8b | COINCIDE |
| encodat_2016_2017__encodat_2016_2017_integrantes_catalogo_xlsx | b7affa16021bfbc0bdd8ecb2e8fc363244b0bb625339fb64605ac108ff1fb5a0 | COINCIDE |
| encodat_2016_2017__encodat_2016_2017_hogar_catalogo_xlsx | c125d639a5766ce0861dbfe73b16ea6259c01ee64d4d2e652c67ebc8582db81e | COINCIDE |
| encodat_2016_2017__cuestionario_encodat_individual_2016_2017_cuestionarios_pdf | 6236d6f38a778b1c0bbdb8fe4f98bf6a042c1cd8a9cd0ca4c5efb9512b3c85a2 | COINCIDE |
| encodat_2016_2017__cuestionario_encodat_hogar_2016_2017_cuestionarios_pdf | bc0175e2da0975a817cee8609a96089a0397bf9ec8c31f8603e3820de984ed7a | COINCIDE |

Nota: el cuestionario de hogar (`cuestionario_encodat_hogar_2016_2017.Cuestionarios.pdf`) se verificó por sha256 pero no se leyó su texto (el cuestionario de Individual ya documentó la carátula de folio de hogar/identificación geográfica, y las 48 variables de Hogar ya se cubrieron vía el .dta + catálogo xlsx). El PDF de Individual (77 páginas) se leyó solo en su primera página (carátula) para confirmar folio de hogar, nombre del estudio y filtro de rango de edad; el resto del cuestionario no se recorrió página por página porque las 1715 variables + etiquetas completas del catálogo xlsx ya dieron el texto literal de cada pregunta.

## Metodología de búsqueda (para trazabilidad)
1. Verificación sha256 de los 8 archivos del manifiesto contra `data/manifiesto.yaml` — 8/8 COINCIDE.
2. Extracción de los 3 `.dta` desde sus `.zip` a `$TMPDIR/encodat/` con `zipfile`.
3. Lectura `pyreadstat.read_dta(..., metadataonly=True, encoding="UTF-8")` de Hogar (48 var, 55907 filas), Integrantes (20 var, 203087 filas), Individual (1715 var, 56877 filas) — el default de pyreadstat produce mojibake/falla; UTF-8 explícito resolvió los tres.
4. Como las etiquetas del .dta de Individual llegan truncadas a ~80 caracteres (límite del formato Stata), se leyó también el catálogo `.xlsx` (columna "Etiqueta" de la hoja "Variables") con `openpyxl` para obtener el texto completo de cada pregunta — 1715 etiquetas completas capturadas.
5. Búsqueda por regex (insensible a mayúsculas) sobre nombres y etiquetas completas para los temas A-C del encargo.
6. Conteo de prefijos de nombre de variable en Individual para mapear los 1715 campos a bloques temáticos (ds, al, tb, di, dm, dd[a-l], cod, tg, tp, ts, pr, ed, pc, dp, dr).
7. Lectura de `variable_value_labels` (diccionarios de códigos, metadato — no microdato) para las variables clave de cada tema.
8. Lectura de la página 1 (carátula) del cuestionario PDF de Individual con `pdfplumber` para confirmar folio de hogar y filtro de rango de edad.

## RESUMEN (5 líneas)
1. Diseño: `estrato` (Rural/Urbano/Metropolitano), `code_upm`, `est_var`, `ponde_hh` viven en **Hogar**; Individual sólo trae `id_pers` (llave propia) y `ponde_ss` (ponderador propio) — no hay `estrato`/`upm` en Individual, se debe unir vía folio de hogar (documentado en carátula del cuestionario, no confirmado en el .dta sin leer valores). No existe variable de "región" (8 regiones) en ningún archivo; sí `entidad` en los tres.
2. Segmentadores en Individual: `ds2` sexo, `ds3`/`ds4` edad, `ds9` escolaridad (último grado); urbano/rural sale de `estrato` en Hogar, no de Individual; no hay tamaño de localidad como variable propia.
3. C1 Alcohol, C2 Tabaco y C3 Cigarro electrónico: totalmente cubiertos con variable, etiquetas y filtro/universo documentados (prefijos `al`, `tb`); consumo excesivo se arma de `al7a`/`al7b`(4/5+ copas)/`al11`(máximo de copas)/`al12*` por umbral, sin una sola variable de "binge" ya combinada.
4. C4 Drogas ilegales (`di`, 9 sustancias) y drogas médicas sin receta (`dm`, 4 categorías incl. opiáceos) cubiertas variable por variable; tramadol/opioides no aparecen como variable nombrada, sólo dentro del texto de `dm1a` (categoría "Opiáceos") y potencialmente como texto libre en `cod_op1-3`. C5 Salud mental (Kessler/suicidio/depresión) **no existe** en Individual — se buscó explícitamente y sólo aparecen escalas de discapacidad por consumo (`dp`/`dr`, tipo WHODAS). C6 Tratamiento/acceso a servicios muy rico (`tg`, `tp`): incluye lugar de atención (pública/privada/anexo/CIJ) y barreras percibidas.
5. Salida completa en: `/tmp/claude-1000/-home-pc0/34676c2b-a9d9-4255-b3cf-7fb2bd70ab02/scratchpad/estructura-encodat.md`



