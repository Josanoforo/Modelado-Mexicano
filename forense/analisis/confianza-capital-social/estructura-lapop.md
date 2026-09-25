# LAPOP México · estructura por ola (sólo metadatos)

Generado sólo con `pyreadstat.read_dta(..., metadataonly=True)` (nombres de
variable, etiquetas de variable, etiquetas de valor) más el texto del
cuestionario impreso 2023 (`data/raw/lapop_abmex2023_cuestionario.pdf`,
manifiesto `lapop_abmex2023_cuestionario_mexico`) para comparar texto. **No se
leyó ningún valor de microdato** (no `head()`, no frecuencias, no medias). El
`.dta` y el `.sav` de **2023 no se abrieron**: 2023 está OLA RESERVADA (E.6) y
sólo entra aquí como texto de cuestionario para comparación textual.

Este documento no repite los reactivos ya sellados a nivel nacional en
`forense/prereg-caja/LAPOP-PISOS-OLAS-spec-v1_0.md` y
`forense/analisis/dominios/politica/lapop-dictamen-olas-v1_0.tsv`
(`b18`, `b21`, `eff1`, `eff2`, `pol1`, `d1`–`d4`, `clien1n`). El foco es
reactivos NUEVOS de confianza institucional, religión, participación,
autoridad y tolerancia.

## 1. Tamaño y diseño por ola (confirmación de variables sellada por la spec)

| ola | payload | filas | columnas | `estratopri`/`mestrat` | `upm`/`mprov`×`msec` | peso |
|---|---|---|---|---|---|---|
| 2004 | `642348348mexico 2004 export version.dta` | 1556 | 235 | AUSENTE por ese nombre; diseño real es `mestrat`/región (spec) | no verificado aquí por nombre exacto (spec usa `mprov`×`msec`) | spec: 1 |
| 2006 | `518939279mexico_lapop_final 2006 data set 092906.dta` | 1560 | 225 | `ESTRATOPRI` presente, etiquetas Norte/Centro-Occidente/Centro/Sur | `UPM` presente | spec: 1 |
| 2019 | `Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta` | 1580 | 221 | `estratopri` presente, mismas etiquetas | `upm` presente | `wt` no inspeccionado aquí (ya fijado por spec) |
| 2021 | `MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta` | 2998 | 262 | `estratopri` presente, etiqueta de variable = «Región» (mismas etiquetas de valor) | `upm` presente | `wt` no inspeccionado aquí; `strata` presente mas etiquetado «Peso estandarizado» (spec ya advierte no usarla) |

No se abrió 2023 en formato de datos; su diseño (`estratopri`/`upm`/`wt`) ya
está fijado por la spec sellada y no se reverifica aquí.

Nota: en 2004 el nombre `estratopri` no existe como tal en el `.dta` (no lo
busqué por nombres alternos más allá de `estratopri`); esto es consistente
con que la spec ya declara el diseño 2004 con `mestrat`/`mprov`×`msec`, no con
`estratopri`.

## 2. Segmentación por ola

| variable | 2004 | 2006 | 2019 | 2021 |
|---|---|---|---|---|
| `q1` sexo | `Sexo`: 1 Hombre, 2 Mujer | `Q1.Género`: 1 Hombre, 2 Mujer | `Sexo`: 1 Hombre, 2 Mujer | **AUSENTE** (2021 usa otro esquema, p.ej. `q1tb`, no confirmado como sexo) |
| `q2` edad | `¿Cuál es su edad…?`, sin etiquetas de valor (numérica) | ídem | `Edad`, `{'a':'No sabe'}` | `Edad`, sin etiquetas |
| `ed` escolaridad (años) | `{'88':'NS/NR'}` | `{'0':'ninguno','88':'No sabe/no responde'}` | `Años de educación` `{'0':'Ninguno','18':'18+','a':'No sabe','b':'No responde','c':'No Aplica'}` | **AUSENTE** (no hay `ed`; hay `edr`, no explorado en detalle) |
| `ur` urbano/rural | `Subestratos` 1 Urbano, 2 Rural | `UR` 1 Urbano, 2 Rural | `Urbano/Rural` 1 Urbano, 2 Rural | **AUSENTE** (hay `ur1new`, no explorado) |
| `tamano` tamaño de localidad | 1 Capital nacional…5 Área rural | mismas 5 categorías (2 DF por «México DF») | mismas 5 categorías | **AUSENTE** |
| `estratopri` región | AUSENTE por ese nombre | 101 Norte…104 Sur | 101 Norte…104 Sur | 101 Norte…104 Sur (etiqueta de variable «Región») |
| `colorr` color de piel | AUSENTE | AUSENTE | `Color de piel`: 1 Más claro … 11 Más oscuro, c No Aplica | AUSENTE |
| `quintall` riqueza | no encontrada en ninguna ola (búsqueda exacta) | — | — | — |
| ingreso | `q10` rangos en pesos (0 Ningún ingreso…10 más de $13501, 88 NS) | `q10` rangos equivalentes | `q10new` rangos distintos y más finos (17 categorías, a/b/c NS/NR/NoAplica) | **AUSENTE** (`q10new` no encontrada; hay `q10newt`, no explorada) |
| ocupación | AUSENTE (`ocup4a` no existe en 2004/2006) | AUSENTE | `ocup4a` `Situación laboral`, 7 categorías + a/b/c | `ocup4a` presente, mismas 7 categorías (con signo `?` en el texto de etiqueta, cosmético) |

Rareza: `quintall` (quintil de riqueza AmericasBarometer) no aparece con ese
nombre exacto en ninguna de las cuatro olas abiertas; no se buscó por
variantes de nombre más allá de la coincidencia exacta.

Rareza mayor: **2021 (CATI) carece de las variables demográficas/urbanas
estándar** `q1`, `ed`, `ur`, `tamano`, `q10new` bajo esos nombres — consistente
con el cambio de modo (telefónico, sin marco de localidad/tamaño de
municipio) que ya documenta la spec como ruptura de modo y población.

## 3. Reactivos candidatos (confianza, religión, participación, autoridad, tolerancia)

Escala mostrada = escala del `.dta` de cada ola (según etiquetas de valor
leídas); "2023-cuestionario" es sólo texto/escala del PDF impreso, no datos.

| variable | etiqueta / pregunta | etiquetas de valor (incl. NS/NR) | 2004 | 2006 | 2019 | 2021 | 2023-cuestionario |
|---|---|---|---|---|---|---|---|
| `it1` confianza interpersonal | «¿diría que la gente de su comunidad es muy confiable, algo confiable, poco confiable o nada confiable?» | 1 Muy…4 Nada; NS(8/a) | presente, idéntico texto | presente, idéntico texto | presente (etiqueta corta «Confianza interpersonal», texto de origen 2019 no verificado aquí pero mismas categorías) | presente, mismas categorías | **IDÉNTICO** — mismo texto exacto en PDF 2023 (línea 281) |
| `b10a` confianza sistema de justicia | «¿Hasta qué punto tiene confianza en el sistema de justicia?» | 1-7; NS(8) | presente | presente | **AUSENTE** | **AUSENTE** | presente, texto idéntico, escala 1-7 |
| `b11` confianza en elecciones/INE | 2004/2006: «elecciones»/IFE; 2023: «Instituto Nacional Electoral (INE)» | 1-7; NS(8) | presente («confianza en las elecciones») | presente (IFE) | **AUSENTE** | **AUSENTE** | presente, CAMBIA-TEXTO (IFE→INE, cambio de nombre institucional real, no de instrumento) |
| `b12` confianza Fuerzas Armadas | «¿Hasta qué punto tiene confianza en las Fuerzas Armadas?» | 1-7; NS | presente | presente | presente (`Confianza en las Fuerzas Armadas`) | presente (`Confianza en los militares`, etiqueta corta distinta, mismo objeto por valor) | presente, texto idéntico |
| `b13` confianza Congreso | «…confianza en el Congreso (Nacional)» | 1-7; NS | presente | presente | presente | presente (`Confianza en la legislatura`) | presente, texto idéntico |
| `b14` confianza Gobierno | «…confianza en el Gobierno Nacional/Federal» | 1-7; NS | presente | presente | **AUSENTE** | **AUSENTE** | **AUSENTE del cuestionario 2023** (no localizada) |
| `b20` confianza Iglesia Católica | «…confianza en la Iglesia Católica» | 1-7; NS | presente | presente | presente | **AUSENTE** | **AUSENTE del cuestionario 2023** (no localizada) |
| `b20a` confianza iglesias evangélicas | «Confianza en la Iglesia Protestante» | 1-7; NS/NR/NoAplica | AUSENTE | AUSENTE | presente | **AUSENTE** | **AUSENTE del cuestionario 2023** (no localizada) |
| `b21a` confianza presidente | «…confianza en el presidente» | 1-7; NS | AUSENTE | AUSENTE | presente | presente (`Confianza en el ejecutivo`) | presente, texto idéntico |
| `b37` confianza medios | «…confianza en los medios de comunicación» | 1-7; NS | presente | presente | presente | **AUSENTE** | presente, texto idéntico |
| `b47`/`b47a` confianza elecciones (país) | 2004 `b47`: «…confianza en las elecciones»; 2023 `B47A`: «…confianza en las elecciones en este país» | 1-7; NS | presente (`b47`) | AUSENTE | AUSENTE | AUSENTE | presente (`B47A`), CAMBIA-TEXTO leve (agrega «en este país») |
| `q3cn` religión (denominación) | «¿podría decirme cuál es su religión?» | católico/protestante/evangélica/otras/ninguna/agnóstico-ateo/otro/NS/NR | AUSENTE | AUSENTE | presente (11 categorías) | AUSENTE | presente, mismo objeto (`Q3CN`), catálogo de categorías no verificado línea a línea contra 2019 |
| `q5a` asistencia a servicios religiosos | «Asistencia a servicios religiosos» | 1 más de 1×semana…5 nunca; NS/NR/NoAplica | AUSENTE | AUSENTE | presente | AUSENTE | **AUSENTE del cuestionario 2023** (no localizada por ese código) |
| `q5b` importancia de la religión | «¿qué tan importante es la religión en su vida?» | 1 Muy…4 Nada; NS/NR | AUSENTE | AUSENTE | presente | AUSENTE | presente, texto y escala idénticos |
| `cp5` resolvió problema comunidad | «¿ha contribuido…para la solución de algún problema…?» | 1 Sí, 2 No; NS | presente | presente | AUSENTE | AUSENTE | **AUSENTE del cuestionario 2023** (no localizada) |
| `cp6` reuniones organización religiosa | «¿Asiste a reuniones de alguna organización religiosa?» | 1 semanal…4 nunca; NS | presente | presente | presente | AUSENTE | **AUSENTE del cuestionario 2023** (no localizada) |
| `cp7` reuniones asociación de padres | ídem escala | 1 semanal…4 nunca; NS | presente | presente | presente | AUSENTE | **AUSENTE del cuestionario 2023** (no localizada) |
| `cp8` reuniones comité de mejoras | «¿Reuniones de un comité o junta de mejoras para la comunidad?» | 1 semanal…4 nunca; NS/NR | presente | presente | presente | AUSENTE | presente, texto y escala idénticos |
| `cp9` reuniones asociación profesional | «…asociación de profesionales, comerciantes, productores…» | 1 semanal…4 nunca; NS | presente | presente | AUSENTE | AUSENTE | **AUSENTE del cuestionario 2023** (no localizada) |
| `cp13` reuniones partido político | «¿Reuniones de un partido o movimiento político?» | 1 semanal…4 nunca; NS | presente | presente | presente | AUSENTE | presente, texto y escala idénticos |
| `cp20` reuniones grupo de mujeres | «¿Reuniones de asociaciones o grupos de mujeres?» | 1 semanal…4 nunca; NS/NR/NoAplica | AUSENTE | AUSENTE | presente | AUSENTE | presente, texto y escala idénticos; PDF anota filtro «sólo mujeres, según `Q1TC`» |
| `jc10` golpe militar (delincuencia) | «Frente a mucha delincuencia, ¿se justificaría…golpe de estado?» | 1 Sí, 2 No; NS | presente | presente | presente (texto más largo, mismo objeto) | AUSENTE | presente, texto y escala idénticos (agrega código 999999 Inaplicable) |
| `jc13` golpe militar (corrupción) | «Frente a mucha corrupción…» | 1 Sí, 2 No; NS | presente | presente | presente | presente | presente, texto y escala idénticos |
| `jc16a` disolución Corte Suprema | «¿se justifica que el presidente disuelva la Suprema/Corte Suprema de Justicia…?» | 1 Sí, 2 No; NS/NR/NoAplica | AUSENTE | AUSENTE | presente | AUSENTE | presente; CAMBIA-TEXTO (2019 habla de «el ejecutivo»; 2023 nombra explícitamente al presidente y a la «Suprema Corte de Justicia de la Nación») |
| `aoj11` inseguridad en el barrio | «pensando en la posibilidad de ser víctima…» | 1 Muy seguro…4 Muy inseguro; NS | presente | presente | presente | presente | texto no comparado línea a línea (el reactivo aparece 8 veces en el PDF; no se leyó cada variante) |
| `aoj12` confianza en castigo judicial (víctima robo) | «Si fuera/usted fuera víctima de un robo o asalto, ¿cuánto confiaría…?» | 1 Mucho…4 Nada; NS | presente | presente | presente | AUSENTE | presente, texto y escala idénticos |
| `e16` justicia por propia mano | «…aprobaría o desaprobaría que las personas hagan justicia por su propia mano…» | 1-10 (2004) / sólo NS=88 visible (2006, escala no confirmada por valor); AUSENTE 2019/2021 | presente | presente | AUSENTE | AUSENTE | **AUSENTE del cuestionario 2023** (no localizada) |
| `dem2` preferencia por democracia | «Con cuál de las siguientes tres frases está usted más de acuerdo…» | 3 frases fijas; NS | presente | presente | AUSENTE | AUSENTE | **AUSENTE del cuestionario 2023** (no localizada) |
| `aut1` líder fuerte sin elección | «necesitamos un líder fuerte que no tenga que ser elegido…» | 1 líder fuerte, 2 democracia electoral; NS | presente | presente | AUSENTE | AUSENTE | **AUSENTE del cuestionario 2023** (no localizada) |
| `d5` tolerancia homosexuales candidatos | «¿…homosexuales se puedan postular a cargos públicos?» | 1-10; NS | presente | presente | presente | AUSENTE | presente, texto casi idéntico (2023 agrega «Y ahora, cambiando el tema, y pensando en los homosexuales.» como lead-in, igual que 2004/2006), escala 1-10 idéntica |
| `d6` matrimonio igualitario | 2004: «…salgan en la televisión…»; 2019/2023: «…parejas del mismo sexo puedan tener el derecho a casarse» | 1-10; NS | presente (**objeto distinto**, ver discrepancia abajo) | AUSENTE | presente | AUSENTE | presente, texto igual a 2019, escala 1-10 idéntica |

## 4. Discrepancias de texto/escala relevantes para el dictamen de equivalencia

- **`d6` no es el mismo reactivo en 2004 que en 2019/2023.** En 2004 la
  etiqueta de variable dice «¿Con qué firmeza aprueba o desaprueba que estas
  personas salgan en la televisión…?» (visibilidad mediática de
  homosexuales), mientras 2019 y el cuestionario 2023 preguntan por el
  «derecho a contraer matrimonio». Misma escala 1-10 y mismo código `d6`,
  pero **CAMBIA-OBJETO**, no sólo texto. 2004 `d6` NO es comparable con
  2019/2023 `d6` sin esa reserva. 2006 no tiene `d6`.
- **`jc16a`** cambia de sujeto entre 2019 («el ejecutivo») y 2023 (nombra al
  «presidente» y a la «Suprema Corte de Justicia de la Nación» explícitamente),
  aunque el objeto (disolución de la Corte por decisión del Ejecutivo en
  momentos difíciles) parece el mismo — CAMBIA-TEXTO, no verificado como
  CAMBIA-OBJETO.
- **`b11`** cambia de nombre institucional real entre 2006 (IFE) y 2023 (INE)
  — es el mismo instrumento (autoridad electoral nacional), pero el
  renombre institucional real (reforma de 2014) hace que el texto no sea
  literalmente idéntico entre olas.
- **`b47`/`b47a`**: 2004 pregunta «confianza en las elecciones» sin
  calificador; 2023 (`B47A`) agrega «...en este país», leve cambio de texto,
  mismo objeto aparente.
- **2021 es la ola más pobre en este bloque**: de los ~28 reactivos nuevos
  candidatos, sólo `b12`, `b13`, `b21a`, `jc13`, `aoj11`, `ocup4a` sobreviven en
  2021; todo el bloque de confianza en Iglesia/medios/justicia/INE,
  participación (`cp*`), religión (`q3cn`/`q5a`/`q5b`), autoridad
  (`e16`/`dem2`/`aut1`/`aoj12`) y tolerancia (`d5`/`d6`) está AUSENTE en 2021.
  Consistente con el diseño CATI (Core A/B con submuestras) que ya reporta la
  spec para `b18`/`b21`.
- **2004→2006** el bloque de confianza/participación/autoridad es casi
  idéntico letra por letra (mismas 5 categorías 1-4/NS o 1-7/NS, mismo texto
  salvo numeración de pregunta `Q1.`/`ED.` prefijada en 2006), consistente con
  «diseño idéntico a 2004» que ya declara la spec para el diseño muestral.
- El campo `strata` (2021) confirma lo que ya advierte la spec: está
  etiquetado «Peso estandarizado», no es un estrato.

## Nota de cobertura

No se intentó resolver por nombres alternativos cada variable AUSENTE (por
ejemplo `q10newt`, `edr`, `ur1new`, `q1tb` en 2021 no se inspeccionaron en
detalle más allá de confirmar que existen bajo otro nombre); este documento
reporta ausencia **bajo el nombre canónico** usado por las olas presenciales,
no ausencia de cualquier proxy posible.
