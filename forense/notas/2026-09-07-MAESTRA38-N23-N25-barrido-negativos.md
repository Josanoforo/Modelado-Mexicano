# `MAESTRA38-N23-N25` · barrido de vocabulario por regla sobre los tres inventarios — script, salida cruda y las cuatro discrepancias con el encargo

### 7 de septiembre de 2026 · entorno **NUBE** (`cloud_default`) · base `origin/main = 604793fa` (PR #591)

> | | |
> |---|---|
> | **QUÉ ES** | La evidencia de existencia (A.8/A.13) sobre la que se congelan `S14`/`S15`/`S16`. Un patrón por regla, corrido sobre las **317 718 filas** de los tres inventarios vigentes, con el conteo de filas examinadas en cada negativo. |
> | **QUÉ NO ES** | No abre microdato: lee TSV de inventario (metadato de reactivo), nada más. No mide. No reclasifica ninguna de las ocho reglas que el encargo sostiene — las recuenta y deja el número. |
> | **REPRODUCES ASÍ** | `python3 tools/barrido_negativos_m38.py` (script en este mismo commit). Sin argumentos corre las 15 reglas más los tres bloques de detalle. `--regla R7.4` limita a una. |

---

## 0 · Universo examinado — declarado antes de cualquier negativo (A.13)

| inventario | filas de datos (sin cabecera ni comentarios `#`) |
|---|---|
| `data/inventario-reactivos-v1_2.tsv` | 178 246 |
| `data/inventario-reactivos-descargas-mx-v1_2.tsv` | 76 127 |
| `data/inventario-reactivos-ext-v1_0.tsv` | 63 345 |
| **total** | **317 718** |

El encargo declara 317 721 (178 247 · 76 128 · 63 346). La diferencia es de **3 filas, una por inventario**: la cabecera de columnas. `grep -vc '^#'` cuenta la cabecera; el lector CSV no. **Ningún negativo de esta nota cambia por esas tres filas** — se declara porque la cifra del encargo y la de aquí no coinciden y saber por qué vale más que elegir una.

Campos barridos en cada fila: `variable_id` **y** `texto_reactivo`, insensible a mayúsculas.

---

## 1 · Las tres reglas que el acto reabre — veredicto

| regla | cierre vigente que se revisa | lo que el inventario devuelve | veredicto de esta nota |
|---|---|---|---|
| `R7.4` `civico.protesta.agravio_urbano_multiola` | «sin instrumento hoy: ENVIPE 2025 no trae desenlace de protesta» (FP-329 (c)) | **197** aciertos de protesta en 317 718; desenlace presente en ENCUP 2012, Cultura Política y Cultura Constitucional 3ª | la cláusula **es correcta sobre ENVIPE y excede su universo**: hay desenlace fuera de ENVIPE. Pero `VÍCTIMA` es **0** en las tres encuestas (§3) → `S14` cierra `EXISTE-NO-SATISFACE` |
| `R4.5` `salud.consumo.sellos_precio_similar` | `SIN-COBERTURA` / `HIPÓTESIS-SIN-INSTRUMENTO` (N10) | módulo **ETI de ENSANUT 2024** con **140 filas** en el inventario `ext`, **con etiquetas verbatim** | **EXISTE-SATISFACE-PARCIAL**: disparador y desenlace existen y son nombrables hoy; la condición «a precio similar» no la controla el instrumento (§4) |
| `R9.3` `informacion.credibilidad.allegado_confianza` | `SIN-COBERTURA` / hipótesis | batería **`p53_1…p53_25`** de Sociedad de la Información, **con la fuente de cada ítem en la etiqueta** | **EXISTE-SATISFACE**: `p53_1` familia, `p53_17` amigos, `p53_23` vecinos, contra medios formales e internet (§5) |

---

## 2 · Las cuatro discrepancias entre el encargo y lo que el barrido devuelve

El encargo manda propagar, no decidir (SELLA-3). Estas cuatro no son decisiones: son cifras que no reproducen, y A.13 obliga a declararlas en vez de copiarlas.

1. **`R4.5`: los «292 aciertos» no reproducen.** El patrón del encargo verbatim (`SELLO|ETIQUETADO|OCTAGON|EXCESO (AZUCAR|CALORIAS|SODIO|GRASA)`) devuelve **8**, no 292; el patrón más estricto de esta nota devuelve **5**. Lo que sí reproduce el orden de magnitud es el **prefijo de nombre de variable** `^ETI`: **253** aciertos, de los cuales 85 en el miembro `.csv` y 85 en el `.dta` del mismo módulo. **El hallazgo del encargo se sostiene íntegro** (el módulo existe, nadie lo había leído con vocabulario de regla); lo que no se sostiene es el número, y el número es lo que un sucesor citaría.
2. **`R4.5`: el inventario SÍ trae las etiquetas.** El encargo declara «sin etiquetas en el inventario (csv sin metadatos)» y por eso manda ir al cuestionario PDF con receta A.5 de respaldo. Es cierto **del miembro `.csv`** (85 filas, `texto_reactivo` vacío) y falso **del miembro `.dta`** del mismo payload, en `inventario-reactivos-ext-v1_0.tsv`: **140 filas con el enunciado verbatim** (`eti04 ¿Me puede decir si ha visto estos sellos?`, `eti21 ¿Usted utiliza los sellos de "EXCESO" para decidir la compra...`, `eti27 Piense en la última vez que fue de compras...`). **`S15` se congela desde el inventario, sin depender del PDF** — que es exactamente el defecto que el hallazgo `PARA-v2.13` de este acto describe, cometido una vez más dentro del encargo que lo denuncia.
3. **`R9.3`: son `p53_1…p53_25`, no `p53_1…p53_10`.** Veinticinco fuentes, no diez. Y la pregunta que el encargo deja condicionada («si entre las fuentes hay allegados … se verifica en el cuestionario antes de sellar») **ya está contestada por el inventario**: `p53_1` = «Su familia», `p53_17` = «Sus amigos», `p53_23` = «Sus vecinos». No hace falta abrir el cuestionario para saberlo.
4. **Las ocho reglas que se sostienen: los conteos no son comparables.** El encargo da un número por regla (`R6.4` 52, `R8.2` 74, `R6.3` 333…) sin dar el patrón que lo produjo. Los patrones de esta nota son propios y devuelven otros números (§6). **No se reclasifica ninguna de las ocho** — el encargo lo prohíbe y esta nota no lo hace; se deja el conteo de esta corrida junto al del encargo para que un sucesor sepa que las dos cifras miden cosas distintas, no que una esté mal.

---

## 3 · `R7.4` — por qué las tres encuestas no bastan: `VÍCTIMA` es 0 en las tres

Patrón de victimización deliberadamente ancho (`VICTIM|DELITO|DELINCUEN|ROBO|ROBAR|ASALT|EXTORSI|SECUESTR|INSEGURID|LE HA PASADO|HA SUFRIDO|FUE OBJETO|CRIMEN`), para que un negativo signifique algo:

| encuesta | filas examinadas | `PROTESTA` | `VÍCTIMA` | `FALLA_ESTATAL` | `RED_PREVIA` | `URBANO/RURAL` | `PONDERADOR` |
|---|---|---|---|---|---|---|---|
| ENCUP 2012 | 282 | 4 vars | **0 útiles** (1 acierto: `P67_4`, «probara alguna vez alguna droga» — falso positivo por `droga`≠, ver salida) | 35 vars | 35 vars | **0** | `factor`, `POND` |
| losmexicanos Cultura Política | 610 | 13 vars | **0 útiles** (4 aciertos, todos `p13_*` «juzgar a los delincuentes» — atribución de funciones, no victimización) | 54 vars | 16 vars | `Estrato`, `Tam_loc`, `loca` | `Pondi2`, `Pondi_v` |
| Cultura Constitucional 3ª | 864 | 12 vars | **0 útiles** (12 aciertos, todos `P55_*` «juzgar a los delincuentes») | 67 vars | 2 vars | `LOC` (id de localidad) | `Pondi2` |

**Ninguna de las tres pregunta si la persona fue víctima de un delito.** Los aciertos son de conocimiento cívico («¿quién juzga a los delincuentes?»), no de victimización. El `SI` de `R7.4` tiene cinco términos y a las tres encuestas les falta el primero — el que define el universo del contraste. Por eso `S14 §2` cierra `EXISTE-NO-SATISFACE` y **no** habilita `L22`.

---

## 4 · `R4.5` — el módulo ETI, nombrado ítem por ítem

Disparador (exposición/atención): `eti03`, `eti04`, `eti05a`, `eti05b`, `ETI05A1…ETI05F1` (¿dónde los ha visto), `eti17`, `eti18`, `ETI181A…E`, `eti19`.
Desenlace (uso declarado en la decisión de compra): `eti21`, `eti21a`, `eti21b`, `eti25`, `eti27` (última compra concreta), `ETI32A/B/C`.
Diseño: `ponde_f` (Ponderador), `estrato` («Estrato urbanidad/ruralidad»), `est_sel`, `upm`, `FOLIO_I`/`FOLIO_INT`.
Comprensión (no es la regla, se anota): `eti06`, `eti07`, `eti11`, `eti12a…f`, `ETI12GA…J`, `ETI14A…J`.

**La condición «a precio similar» no aparece en ningún ítem del módulo** — barrido específico incluido en la salida. Es condición de diseño experimental, no de reactivo; `S15 §3` la declara sin prueba.

---

## 5 · `R9.3` — las 25 fuentes de `p53`, con allegados dentro

Allegados: `p53_1` Su familia · `p53_17` Sus amigos · `p53_23` Sus vecinos.
Medios formales: `p53_2` televisión nacional · `p53_6` periódicos · `p53_13` radio · `p53_10` televisión extranjera.
Internet: `p53_19` el internet · `p53_5` redes sociales · `p53_25` blogs de internet.
Escala verbatim: «pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da…?»

Corroboración secundaria `p33` (Medio Ambiente): existe la batería (`p33_1…p33_8`, ordenamiento por confiabilidad), pero **las etiquetas del inventario solo dicen «1ª MENCIÓN … 8ª MENCIÓN»** — qué medio es cada mención vive en las etiquetas de valor, que el inventario no captura. `S16` la deja como corroboración **condicionada** con cláusula PARA, no como dato.

---

## 6 · Las ocho que se sostienen — conteo de esta corrida, sin reclasificar

| regla | aciertos, patrón de esta nota | número que el encargo declara | comentario |
|---|---|---|---|
| `coercitivo` | 1 | 2 | patrones distintos; el encargo lo gobierna con FP-273, no se toca |
| `G4.horizonte_temporal` | 0 | 11 | 0 con patrón de vocabulario explícito de elección intertemporal |
| `R6.1` puntualidad | 27 | 24 | |
| `R6.2` compromiso | 0 | 2 | |
| `R6.4` recordatorio | 71 | 52 | |
| `R10.1` rechazo | 7 | 13 | |
| `R10.2` retroalimentación | 14 | 24 | |
| `R2.1` iniciativa | 21 | 31 | |
| `R4.2` permiso | 35 | 103 | |
| `R8.2` tanda | 93 | 74 | |
| `R6.3` bomberazo | 52 | 333 | |

**Ninguna se reclasifica en este acto.** Las cifras de las dos columnas miden cosas distintas porque los patrones son distintos, y el del encargo no está escrito. Un sucesor que quiera comparar tiene que fijar el patrón primero.

---

## 7 · Salida cruda, verbatim

```
UNIVERSO: 317718 filas de 3 inventarios
  data/inventario-reactivos-v1_2.tsv: 178246
  data/inventario-reactivos-descargas-mx-v1_2.tsv: 76127
  data/inventario-reactivos-ext-v1_0.tsv: 63345

=== R7.4 · patron: MARCHA|PROTEST|MANIFEST|PLANTON|PLANTÓN|MITIN|BLOQUEO|HUELGA|PARO |PETICION|PETICIÓN
    aciertos: 197 / 317718
        22  (sin-instrumento-derivable) :: UNIVERSO-2026-09/CSES/cide_cses2015_nacional_poselectoral.sav
        22  (sin-instrumento-derivable) :: UNIVERSO-2026-09/CSES/cide_cses2015_nacional_preelectoral.sav
        14  (sin-instrumento-derivable) :: losmexicanos_unam_iij/culturapolitica/Encuesta_Nacional_de_Cultura_Politica.sav
        13  (sin-instrumento-derivable) :: cultura_constitucional_unam_iij/Tercera_Encuesta_Nacional_de_Cultura_Constitucional.sav
        10  (sin-instrumento-derivable) :: cultura_constitucional_unam_iij/Tercera_Encuesta_Nacional_de_Cultura_Constitucional.dta
         8  A6_MMAD_PROTESTA_MEXICO :: mmALL_073120_csv.csv
         8  (sin-instrumento-derivable) :: Descargas Manuales/1008973606Mexico_LAPOP_final 2006 data set 092906.sav
         8  (sin-instrumento-derivable) :: Descargas Manuales/1658622845Mexico 2004 Export Version.sav
         8  Descargas Manuales :: mmALL_073120_csv.csv
         8  (sin-instrumento-derivable) :: losmexicanos_unam_iij/culturapolitica/Encuesta_Nacional_de_Cultura_Politica.dta
         6  (sin-instrumento-derivable) :: Descargas Manuales/518939279mexico_lapop_final 2006 data set 092906.dta
         4  encup2012 :: BaseDatos_ENCUP_2012_Final
         4  (sin-instrumento-derivable) :: Descargas Manuales/642348348mexico 2004 export version.dta
         4  (sin-instrumento-derivable) :: Descargas Manuales/Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta
         4  (raiz) :: Data
         4  (sin-instrumento-derivable) :: losmexicanos_unam_iij/corrupcionyculturadelalegalidad/Encuesta_Nacional_de_Corrupcion_y_Cultura_de_la_Legalidad.sav
         4  (sin-instrumento-derivable) :: losmexicanos_unam_iij/derechoshumanos/Encuesta_Nacional_de_Derechos_Humanos_Discriminacion_y_Grupos_Vulnerables.sav
         3  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w (1).dta
         3  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta
         3  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.sav
         3  (sin-instrumento-derivable) :: losmexicanos_unam_iij/justicia/Encuesta_Nacional_de_Justicia.dta
         3  (sin-instrumento-derivable) :: losmexicanos_unam_iij/justicia/Encuesta_Nacional_de_Justicia.sav
         3  (sin-instrumento-derivable) :: losmexicanos_unam_iij/ninosadolescentesyjovenes/Encuesta_Nacional_de_Ninos_Adolescentes_y_Jovenes.sav
         2  (sin-instrumento-derivable) :: rec24h_alim_ensanut2024_w.dta
         2  (sin-instrumento-derivable) :: rec24h_rev_alim_ensanut2024_w.dta

=== R7.4-victimizacion · patron: VICTIMA|VÍCTIMA|DELITO|ROBO|ASALT|EXTORSION|EXTORSIÓN|SECUESTR
    aciertos: 671 / 317718
        85  (sin-instrumento-derivable) :: losmexicanos_unam_iij/seguridadpublica/Encuesta_Nacional_de_Seguridad_Publica.sav
        51  (sin-instrumento-derivable) :: losmexicanos_unam_iij/movilidadytransporte/Encuesta_Nacional_de_Movilidad_y_Transporte.dta
        51  (sin-instrumento-derivable) :: losmexicanos_unam_iij/movilidadytransporte/Encuesta_Nacional_de_Movilidad_y_Transporte.sav
        48  (sin-instrumento-derivable) :: losmexicanos_unam_iij/seguridadpublica/Encuesta_Nacional_de_Seguridad_Publica.dta
        15  (sin-instrumento-derivable) :: losmexicanos_unam_iij/derechoshumanos/Encuesta_Nacional_de_Derechos_Humanos_Discriminacion_y_Grupos_Vulnerables.sav
        14  (sin-instrumento-derivable) :: losmexicanos_unam_iij/ninosadolescentesyjovenes/Encuesta_Nacional_de_Ninos_Adolescentes_y_Jovenes.sav
        12  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_ii_caracterizacion_delito/t2_1.csv
        11  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_i_nivel_victimizacion_delincuencia/t1_19.csv
        11  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_i_nivel_victimizacion_delincuencia/t1_20.csv
        11  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_ii_caracterizacion_delito/t2_2.csv
        11  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_ii_caracterizacion_delito/t2_3.csv
        10  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_i_nivel_victimizacion_delincuencia/t1_16.csv
         9  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_i_nivel_victimizacion_delincuencia/t1_17.csv
         9  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_i_nivel_victimizacion_delincuencia/t1_18.csv
         9  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_vi_perdidas_consecuencia_inseguridad/t6_4.csv
         9  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_vi_perdidas_consecuencia_inseguridad/t6_5.csv
         9  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_vi_perdidas_consecuencia_inseguridad/t6_6.csv
         9  (sin-instrumento-derivable) :: losmexicanos_unam_iij/justicia/Encuesta_Nacional_de_Justicia.sav
         9  (sin-instrumento-derivable) :: ehh02dta_all/ehh02dta_b2/ii_vlh.dta
         8  (sin-instrumento-derivable) :: ehh05dta_b2/ii_vlh.dta
         8  (sin-instrumento-derivable) :: ehh09dta_all/ehh09dta_b2/ii_vlh.dta
         7  (sin-instrumento-derivable) :: losmexicanos_unam_iij/derechoshumanos/Encuesta_Nacional_de_Derechos_Humanos_Discriminacion_y_Grupos_Vulnerables.dta
         7  (sin-instrumento-derivable) :: ehh09dta_all/ehh09dta_b2/ii_se.dta
         6  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_ii_caracterizacion_delito/t2_5.csv
         6  UNIVERSO-2026-09 :: conjunto_de_datos/enve2024_iii_denuncia_delito/t3_3.csv

=== R4.5 · patron: SELLO|ETIQUETADO|OCTAGON|OCTÁGON|EXCESO DE (AZUCAR|AZÚCAR|CALORIAS|CALORÍAS|SODIO|GRASA)|ADVERTENCIA.{0,20}(AZUCAR|AZÚCAR|CALORIA|CALORÍA|SODIO|GRASA)
    aciertos: 5 / 317718
         5  (sin-instrumento-derivable) :: etiquetado_ensanut2924_w.dta

=== R4.5-ETI-prefijo · patron: ^ETI
    aciertos: 253 / 317718
        85  ENSANUT2024-v2026-09-01 :: etiquetado_ensanut2924_w.csv
        85  (sin-instrumento-derivable) :: etiquetado_ensanut2924_w.dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w (1).dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.sav
         1  (sin-instrumento-derivable) :: Descargas Manuales/Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta
         1  ENSANUT2024-v2026-09-01 :: actividad_fisica_ensanut2024_w-adultos_valores.csv
         1  ENSANUT2024-v2026-09-01 :: actividad_fisica_ensanut2024_w-adultos_variables.csv
         1  ENSANUT2024-v2026-09-01 :: actividad_fisica_ensanut2024_w-niños_valores.csv
         1  ENSANUT2024-v2026-09-01 :: actividad_fisica_ensanut2024_w-niños_variables.csv
         1  ENSANUT2024-v2026-09-01 :: adolescentes_ensanut2024_w_valores.csv
         1  ENSANUT2024-v2026-09-01 :: adolescentes_ensanut2024_w_variables.csv
         1  ENSANUT2024-v2026-09-01 :: adultos_ensanut2024_w_valores.csv
         1  ENSANUT2024-v2026-09-01 :: adultos_ensanut2024_w_variables.csv
         1  ENSANUT2024-v2026-09-01 :: antropometria_ensanut2024_w_valores.csv
         1  ENSANUT2024-v2026-09-01 :: antropometria_ensanut2024_w_variables.csv
         1  ENSANUT2024-v2026-09-01 :: ensasangre24_determinaciones_micronutrimentos_valores.csv
         1  ENSANUT2024-v2026-09-01 :: ensasangre24_determinaciones_micronutrimentos_variables.csv
         1  ENSANUT2024-v2026-09-01 :: etiquetado_ensanut2924_w_valores.csv
         1  ENSANUT2024-v2026-09-01 :: etiquetado_ensanut2924_w_variables.csv
         1  ENSANUT2024-v2026-09-01 :: frec_adul_ensanut2024_w_valores.csv
         1  ENSANUT2024-v2026-09-01 :: frec_adul_ensanut2024_w_variables.csv
         1  ENSANUT2024-v2026-09-01 :: frec_adul_rec_ensanut2024_w_valores.csv
         1  ENSANUT2024-v2026-09-01 :: frec_adul_rec_ensanut2024_w_variables.csv

=== R9.3 · patron: LE CREE|CREE MAS EN|CREE MÁS EN|CONFIA MAS EN|CONFÍA MÁS EN|CREDIBILIDAD|NO CREE EN NADA
    aciertos: 27 / 317718
        25  (sin-instrumento-derivable) :: losmexicanos_unam_iij/sociedaddelainformacion/Encuesta_Nacional_de_Sociedad_de_la_Informacion.sav
         1  (sin-instrumento-derivable) :: UNIVERSO-2026-09/CSES/cide_cses2015_nacional_poselectoral.sav
         1  (sin-instrumento-derivable) :: UNIVERSO-2026-09/CSES/cide_cses2015_nacional_preelectoral.sav

=== coercitivo · patron: COERCI|COACC|OBLIG.{0,10}A LA FUERZA|AMENAZ.{0,15}(PARA QUE|SI NO)
    aciertos: 1 / 317718
         1  endireh2016 :: bd_mujeres_endireh2016_sitioinegi_spss/BD_MUJERES_ENDIREH2016_SitioINEGI.sav

=== G4.horizonte_temporal · patron: HORIZONTE TEMPORAL|DESCUENTO (TEMPORAL|INTERTEMPORAL)|PREFER.{0,15}TEMPORAL|LARGO PLAZO VS|INTERTEMPORAL
    aciertos: 0 / 317718

=== R6.1 · patron: PUNTUAL|A TIEMPO|LLEG.{0,10}TARDE|IMPUNTUAL|RETRASO
    aciertos: 27 / 317718
         4  endireh2016 :: bd_mujeres_endireh2016_sitioinegi_spss/BD_MUJERES_ENDIREH2016_SitioINEGI.sav
         2  (sin-instrumento-derivable) :: Alumnos 10 Follow-up3-Roster_PUF.sav
         2  (sin-instrumento-derivable) :: Padres 10 Follow-up3-Roster_PUF.sav
         2  (sin-instrumento-derivable) :: MEX_2010_IEPEP_v01_M_v01_A_PUF_STATA8/alumnos 10 follow-up3-roster_puf.dta
         2  (sin-instrumento-derivable) :: MEX_2010_IEPEP_v01_M_v01_A_PUF_STATA8/padres 10 follow-up3-roster_puf.dta
         2  (sin-instrumento-derivable) :: losmexicanos_unam_iij/educacion/Encuesta_Nacional_de_Educacion.dta
         2  (sin-instrumento-derivable) :: losmexicanos_unam_iij/educacion/Encuesta_Nacional_de_Educacion.sav
         1  eder2017 :: historiavida.csv
         1  eder2017 :: historiavida.dbf
         1  UNIVERSO-2026-09 :: Datos abiertos/conjunto_de_datos/conjunto_de_datos_VI_Entorno_del_establecimiento_2020/t6_20.csv
         1  UNIVERSO-2026-09 :: Datos abiertos/conjunto_de_datos/conjunto_de_datos_VI_Entorno_del_establecimiento_2020/t6_21.csv
         1  UNIVERSO-2026-09 :: Datos abiertos/conjunto_de_datos/conjunto_de_datos_VI_Entorno_del_establecimiento_2020/t6_22.csv
         1  UNIVERSO-2026-09 :: Datos abiertos/conjunto_de_datos/conjunto_de_datos_VI_Entorno_del_establecimiento_2020/t6_23.csv
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/genero/Encuesta_Nacional_de_Genero.sav
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/identidadyvalores/Encuesta_Nacional_de_Identidad_y_Valores.sav
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/seguridadpublica/Encuesta_Nacional_de_Seguridad_Publica.sav
         1  eder2017 :: historiavida.dta
         1  eder2017 :: historiavida.sav

=== R6.2 · patron: CUMPL.{0,15}COMPROMISO|COMPROMISO ADQUIRIDO|PROMES.{0,10}CUMPL
    aciertos: 0 / 317718

=== R6.4 · patron: RECORDATORIO|RECUERD|AVISO PREVIO|LE RECORD
    aciertos: 71 / 317718
        14  (sin-instrumento-derivable) :: losmexicanos_unam_iij/indigenas/Encuesta_Nacional_de_Indigenas.dta
        14  (sin-instrumento-derivable) :: losmexicanos_unam_iij/indigenas/Encuesta_Nacional_de_Indigenas.sav
         8  (sin-instrumento-derivable) :: UNIVERSO-2026-09/CSES/cide_cses2015_nacional_poselectoral.sav
         8  (sin-instrumento-derivable) :: UNIVERSO-2026-09/CSES/cide_cses2015_nacional_preelectoral.sav
         5  (sin-instrumento-derivable) :: UNIVERSO-2026-09/CSES/cide_cses2015_estatal_preelectoral.sav
         4  endireh2016 :: bd_mujeres_endireh2016_sitioinegi_spss/BD_MUJERES_ENDIREH2016_SitioINEGI.sav
         3  (sin-instrumento-derivable) :: Descargas Manuales/1658622845Mexico 2004 Export Version.sav
         3  (sin-instrumento-derivable) :: Descargas Manuales/642348348mexico 2004 export version.dta
         2  (sin-instrumento-derivable) :: losmexicanos_unam_iij/genero/Encuesta_Nacional_de_Genero.dta
         2  (sin-instrumento-derivable) :: losmexicanos_unam_iij/genero/Encuesta_Nacional_de_Genero.sav
         1  (sin-instrumento-derivable) :: rec24h_ensanut2024_w.dta
         1  (sin-instrumento-derivable) :: rec24h_rev_rec_ensanut2024_w.dta
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/corrupcionyculturadelalegalidad/Encuesta_Nacional_de_Corrupcion_y_Cultura_de_la_Legalidad.sav
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/economiayempleo/Encuesta_Nacional_de_Economia_y_Empleo.dta
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/economiayempleo/Encuesta_Nacional_de_Economia_y_Empleo.sav
         1  (sin-instrumento-derivable) :: ehh02dta_all/ehh02dta_b2/ii_su.dta
         1  (sin-instrumento-derivable) :: ehh05dta_b2/ii_su.dta
         1  (sin-instrumento-derivable) :: ehh09dta_all/ehh09dta_b2/ii_su.dta

=== R10.1 · patron: RECHAZO|RECHAZ
    aciertos: 7 / 317718
         2  (sin-instrumento-derivable) :: UNIVERSO-2026-09/CSES/cide_cses2015_nacional_poselectoral.sav
         2  (sin-instrumento-derivable) :: UNIVERSO-2026-09/CSES/cide_cses2015_nacional_preelectoral.sav
         1  (sin-instrumento-derivable) :: UNIVERSO-2026-09/CSES/cide_cses2015_estatal_preelectoral.sav
         1  (sin-instrumento-derivable) :: cultura_constitucional_unam_iij/Tercera_Encuesta_Nacional_de_Cultura_Constitucional.sav
         1  (sin-instrumento-derivable) :: Latinobarometro_2024_Stata_esp_v20250817.dta

=== R10.2 · patron: RETROALIMENTACION|RETROALIMENTACIÓN|CRITICA CONSTRUCTIVA|CRÍTICA CONSTRUCTIVA|CENSUR
    aciertos: 14 / 317718
         3  (sin-instrumento-derivable) :: Descargas Manuales/1008973606Mexico_LAPOP_final 2006 data set 092906.sav
         3  (sin-instrumento-derivable) :: Descargas Manuales/1658622845Mexico 2004 Export Version.sav
         3  (sin-instrumento-derivable) :: Descargas Manuales/518939279mexico_lapop_final 2006 data set 092906.dta
         3  (sin-instrumento-derivable) :: Descargas Manuales/642348348mexico 2004 export version.dta
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/globalizacion/Encuesta_Nacional_de_Globalizacion.dta
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/globalizacion/Encuesta_Nacional_de_Globalizacion.sav

=== R2.1 · patron: INICIATIVA|AUTONOM|POR SU PROPIA CUENTA|SIN QUE (LE|LO) DIGAN
    aciertos: 21 / 317718
         8  (raiz) :: Data
         4  (sin-instrumento-derivable) :: WVS_Wave_7_Mexico_Stata_v5.1.dta
         4  (raiz) :: WVS_Wave_7_Mexico_CsvText_v5.1.csv
         1  (raiz) :: WVS_Wave_7_Mexico_Csv_v5.1.csv
         1  (sin-instrumento-derivable) :: Mexico-2026-AI follow-up data.dta
         1  eder2017 :: historiavida.dta
         1  eder2017 :: historiavida.sav
         1  (sin-instrumento-derivable) :: Latinobarometro_2024_Stata_esp_v20250817.dta

=== R4.2 · patron: PERMISO|AUTORIZACION|AUTORIZACIÓN|PEDIR.{0,15}PERMISO|POR QUE NO ACUDIO|POR QUÉ NO ACUDIÓ
    aciertos: 35 / 317718
         7  (sin-instrumento-derivable) :: losmexicanos_unam_iij/genero/Encuesta_Nacional_de_Genero.dta
         7  (sin-instrumento-derivable) :: losmexicanos_unam_iij/genero/Encuesta_Nacional_de_Genero.sav
         6  endireh2016 :: bd_mujeres_endireh2016_sitioinegi_spss/BD_MUJERES_ENDIREH2016_SitioINEGI.sav
         2  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta
         2  (sin-instrumento-derivable) :: adolescentes_ensanut2024_w.dta
         2  (sin-instrumento-derivable) :: menores_ensanut2024_w.dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/1008973606Mexico_LAPOP_final 2006 data set 092906.sav
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w (1).dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.sav
         1  (sin-instrumento-derivable) :: ensasangre24_determinaciones_micronutrimentos.dta
         1  (sin-instrumento-derivable) :: sangre_hemoglobina_ensanut2024_w.dta
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/corrupcionyculturadelalegalidad/Encuesta_Nacional_de_Corrupcion_y_Cultura_de_la_Legalidad.sav
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/envejecimiento/Encuesta_Nacional_de_Envejecimiento.sav
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/ninosadolescentesyjovenes/Encuesta_Nacional_de_Ninos_Adolescentes_y_Jovenes.sav

=== R8.2 · patron: TANDA|CUNDINA|CAJA DE AHORRO|AHORRO ROTATIVO
    aciertos: 93 / 317718
         7  (sin-instrumento-derivable) :: ehh02dta_all/ehh02dta_b3b/iiib_cr.dta
         7  (sin-instrumento-derivable) :: ehh02dta_all/ehh02dta_bx/p_cr.dta
         7  (sin-instrumento-derivable) :: ehh05dta_b3b/iiib_cr.dta
         7  (sin-instrumento-derivable) :: ehh05dta_bx/p_cr.dta
         7  (sin-instrumento-derivable) :: ehh09dta_all/ehh09dta_b3b/iiib_cr.dta
         7  (sin-instrumento-derivable) :: ehh09dta_all/ehh09dta_bx/p_cr.dta
         6  (sin-instrumento-derivable) :: round5_mexiconew_anon.dta
         5  (sin-instrumento-derivable) :: followup_survey.sav
         5  (sin-instrumento-derivable) :: followup_survey.dta
         3  (sin-instrumento-derivable) :: Mexico-2026-AI follow-up data.dta
         3  (sin-instrumento-derivable) :: Mexico-2006--full-data-.dta
         3  (sin-instrumento-derivable) :: ehh09dta_all/ehh09dta_b3b/iiib_rg.dta
         2  (raiz) :: Data
         2  (sin-instrumento-derivable) :: ehh02dta_all/ehh02dta_b2/ii_crh.dta
         2  (sin-instrumento-derivable) :: ehh05dta_b2/ii_crh.dta
         2  (sin-instrumento-derivable) :: ehh09dta_all/ehh09dta_b2/ii_crh.dta
         1  (sin-instrumento-derivable) :: 20260813133000.export.CSV
         1  (sin-instrumento-derivable) :: Compartamos_AEJ/Main/data/analysis_data_AEJ_pub.dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w (1).dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta
         1  (sin-instrumento-derivable) :: Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.sav
         1  (sin-instrumento-derivable) :: WVS_Wave_7_Mexico_Stata_v5.1.dta
         1  (raiz) :: WVS_Wave_7_Mexico_CsvText_v5.1.csv
         1  (sin-instrumento-derivable) :: ZA6980_v2-0-0.dta

=== R6.3 · patron: BOMBERAZO|URGENCIA|EMERGENCIA|ULTIMO MOMENTO|ÚLTIMO MOMENTO
    aciertos: 52 / 317718
        11  (sin-instrumento-derivable) :: ehh09dta_all/ehh09dta_bx/p_cr.dta
        10  (sin-instrumento-derivable) :: ehh09dta_all/ehh09dta_b3b/iiib_cr.dta
         7  (sin-instrumento-derivable) :: ehh05dta_b4/iv_ac.dta
         7  (sin-instrumento-derivable) :: ehh09dta_all/ehh09dta_b4/iv_ac.dta
         5  (sin-instrumento-derivable) :: ehh02dta_all/ehh02dta_b4/iv_ac.dta
         3  endireh2016 :: bd_mujeres_endireh2016_sitioinegi_spss/BD_MUJERES_ENDIREH2016_SitioINEGI.sav
         2  (sin-instrumento-derivable) :: adultos_ensanut2024_w.dta
         2  (raiz) :: Urgencias.txt
         1  (raiz) :: Catálogos/CatTipoUrgencia.csv
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/federalismo/Encuesta_Nacional_de_Federalismo.dta
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/federalismo/Encuesta_Nacional_de_Federalismo.sav
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/migracion/Encuesta_Nacional_de_Migracion.dta
         1  (sin-instrumento-derivable) :: losmexicanos_unam_iij/migracion/Encuesta_Nacional_de_Migracion.sav


########## DETALLE R7.4 -- existencia por termino y por encuesta

--- ENCUP 2012: 282 filas de inventario
    PROTESTA: 4 variables unicas
        P56_5. Para resolver un problema que afecta a usted y a otras personas, ¿alguna vez ha tratado de Asistir a manifestaciones	
        P58_7. ¿Con qué frecuencia ha realizado las siguientes actividades…? Firmar documentos en señal de protesta o solicitando algo	
        P58_8. ¿Con qué frecuencia ha realizado las siguientes actividades…? Participar en manifestaciones a favor o en contra del gobierno o por alguna causa	
        P9. ¿Conoce usted el nombre del movimiento juvenil que se ha manifestado en los últimos meses en México? (Respuesta correcta: #yosoy132)	
    VICTIMA: 1 variables unicas
        P67_4. Ahora imaginemos que usted tiene un hijo o hija adolescente (entre los 15 y los 18 años), ¿usted aceptaría o no que su hijo (…)? Probara alguna vez alguna droga	
    FALLA_ESTATAL: 35 variables unicas
        P30_1. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? La radio	
        P30_10. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Los vecinos	
        P30_11. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? La familia	
        P30_12. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? El gobierno	
        P30_13. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Las organizaciones de ciudadanos3	
        P30_14. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? El Presidente de la República	
        P30_15. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? El Instituto Federal Electoral	
        P30_16. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? La Comisión Nacional de Derechos Humanos	
        P30_17. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Los jueces	
        P30_18. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? La Suprema Corte de Justicia	
        P30_19. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Los diputados	
        P30_2. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? La prensa	
        P30_20. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Los senadores	
        P30_21. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Los gobernadores estatales o jefe de gobierno	
        P30_22. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Los presidentes municipales o Jefes delegacionales	
        P30_23. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? La Policía	
        P30_24. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? El Ejército	
        P30_25. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Los militares	
        P30_26. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Los partidos políticos	
        P30_27. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Las organizaciones indígenas y campesina	
    RED_PREVIA: 35 variables unicas
        P12. ¿A qué partido pertenece el actual gobernador (Jefe de Gobierno en caso del Distrito Federal) de su estado?	
        P26B. A cambio de vivir sin presiones económicas, estaría usted dispuesto a sacrificar su Libertad de asociación	
        P26C. A cambio de vivir sin presiones económicas, estaría usted dispuesto a sacrificar su Libertad de organización	
        P30_13. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Las organizaciones de ciudadanos3	
        P30_27. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Las organizaciones indígenas y campesina	
        P30_9. En una escala de calificación de 0 a 10 donde 0 es nada y 10 es mucho, por favor dígame ¿Qué tanto confía en…? Los sindicatos	
        P3D. En su opinión, ¿qué tanto influyen en la vida política de México Los sindicatos?	
        P3E. En su opinión, ¿qué tanto influyen en la vida política de México Las agrupaciones ciudadanas?	
        P56_4. Para resolver un problema que afecta a usted y a otras personas, ¿alguna vez ha tratado de Pedir apoyo a alguna asociación civil	
        P57_1. Durante el último año, ¿asistió a alguna reunión de las siguientes organizaciones? Juntas de vecinos	
        P57_2. Durante el último año, ¿asistió a alguna reunión de las siguientes organizaciones? Junta de colonos	
        P57_3. Durante el último año, ¿asistió a alguna reunión de las siguientes organizaciones? Reunión de condóminos	
        P57_4. Durante el último año, ¿asistió a alguna reunión de las siguientes organizaciones? Agrupación u organización de ciudadanos	
        P57_5. Durante el último año, ¿asistió a alguna reunión de las siguientes organizaciones? Asambleas de la comunidad	
        P57_6. Durante el último año, ¿asistió a alguna reunión de las siguientes organizaciones? Asociación de padres de familia	
        P57_7. Durante el último año, ¿asistió a alguna reunión de las siguientes organizaciones? Algún partido o agrupación política	
        P57_8. Durante el último año, ¿asistió a alguna reunión de las siguientes organizaciones? Sindicato	
        P57_9. Durante el último año, ¿asistió a alguna reunión de las siguientes organizaciones? De cooperativas o asamblea ejidal	
        P59_11. ¿Alguna vez usted ha llevado a cabo las siguientes acciones? Ha hecho donativos o prestado ayuda alguna organización social (agrupación de ciudadanos)	
        P69_1. Usted es o ha sido miembro de alguna de las siguientes organizaciones que le voy a mencionar Organización estudiantil	
    URBANO_RURAL: 0 variables unicas
    PONDERADOR: 1 variables unicas
        factor	

--- losmexicanos Cultura Politica: 610 filas de inventario
    PROTESTA: 13 variables unicas
        p55_1	54a ¿Y usted esta de acuerdo? Organizan bloqueos y marchas
        p56_1	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_2	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_3	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_4	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_5	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_6	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_7	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p48_12	48 Y Durante el último año, ¿ha realizado alguna de las siguientes actividades? Participado en una huelga o paro de labo
        p48_6	48 Y Durante el último año, ¿ha realizado alguna de las siguientes actividades? Participado en una protesta con violenci
        p48_7	48 Y Durante el último año, ¿ha realizado alguna de las siguientes actividades? Participado en una protesta pacíficament
        p48_9	48 Y Durante el último año, ¿ha realizado alguna de las siguientes actividades? Participado en una manifestación o march
        p54_1	54 Si las autoridades no resuelven algún problema en donde usted vive ¿Por lo general qué hacen los vecinos? Organizan b
    VICTIMA: 4 variables unicas
        p13_1	13 ¿Quién o quiénes realizan las siguientes funciones? Juzgar a los delincuente
        p13_3	13 ¿Quién o quiénes realizan las siguientes funciones? Aprobar los gastos del g
        p13_6	13 ¿Quién o quiénes realizan las siguientes funciones? Aprobar los impuestos
        p13_8	13 ¿Quién o quiénes realizan las siguientes funciones? Aprobar los tratados int
    FALLA_ESTATAL: 54 variables unicas
        p54_1	54 Si las autoridades no resuelven algún problema en donde usted vive ¿Por lo g
        p54_2	54 Si las autoridades no resuelven algún problema en donde usted vive ¿Por lo g
        p54_3	54 Si las autoridades no resuelven algún problema en donde usted vive ¿Por lo g
        p54_4	54 Si las autoridades no resuelven algún problema en donde usted vive ¿Por lo g
        p54_5	54 Si las autoridades no resuelven algún problema en donde usted vive ¿Por lo g
        p54_6	54 Si las autoridades no resuelven algún problema en donde usted vive ¿Por lo g
        p54_7	54 Si las autoridades no resuelven algún problema en donde usted vive ¿Por lo g
        p55_3	54a ¿Y usted esta de acuerdo? Acuden a otras autoridades
        p56_1	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_2	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_3	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_4	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_5	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_6	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p56_7	56 En caso de una protesta pública, las autoridades deberían o no deberían hace
        p63_1	63 ¿Y qué tanto piensa usted que el gobierno Imparte justicia mucho, algo, poc
        p64	64 En su afán por buscar la justicia, cómo deberían actuar las autoridades:
        p81_1	81 En una escala del 0 al 10, como en la escuela, donde 0 es nada de confianza
        p81_10	81 En una escala del 0 al 10, como en la escuela, donde 0 es nada de confianza
        p81_2	81 En una escala del 0 al 10, como en la escuela, donde 0 es nada de confianza
    RED_PREVIA: 16 variables unicas
        p53_1	53 En cuáles de las siguientes organizaciones participa o ha participado Asoci
        p53_2	53 En cuáles de las siguientes organizaciones participa o ha participado Asoci
        p53_3	53 En cuáles de las siguientes organizaciones participa o ha participado Parti
        p53_4	53 En cuáles de las siguientes organizaciones participa o ha participado Agrup
        p53_5	53 En cuáles de las siguientes organizaciones participa o ha participado Organ
        p53_6	53 En cuáles de las siguientes organizaciones participa o ha participado Organ
        p53_7	53 En cuáles de las siguientes organizaciones participa o ha participado Organ
        p53_8	53 En cuáles de las siguientes organizaciones participa o ha participado Organ
        p53_9	53 En cuáles de las siguientes organizaciones participa o ha participado Organ
        p55_6	54a ¿Y usted esta de acuerdo? Acuden a otras organizaciones
        p84_7	84 ¿Qué tan influyentes le parecen los sindicatos?
        p48_8	48 Y Durante el último año, ¿ha realizado alguna de las siguientes actividades? Buscado apoyo de una organización
        p54_6	54 Si las autoridades no resuelven algún problema en donde usted vive ¿Por lo general qué hacen los vecinos? Acuden a ot
        p57_7	57 Por lo que usted piensa, ¿el gobierno debería o no debería intervenir en las decisiones con respecto a la organizació
        p82_18	82 Ahora, nuevamente le pido me diga, pensando en una escala del 0 al 10 como en la escuela; donde 0 es nada de confianz
        p82_21	82 Ahora, nuevamente le pido me diga, pensando en una escala del 0 al 10 como en la escuela; donde 0 es nada de confianz
    URBANO_RURAL: 3 variables unicas
        Estrato	
        Tam_loc	Tamaño de localidad
        loca	Localidad
    PONDERADOR: 2 variables unicas
        Pondi2	Factor de expansión
        Pondi_v	Factor de expansión vivienda

--- Cultura Constitucional 3a: 576 filas de inventario
    PROTESTA: 12 variables unicas
        P54_1	P54_1. En caso de una protesta pública, las autoridades deberían o no deberían h
        P54_2	P54_2. En caso de una protesta pública, las autoridades deberían o no deberían h
        P54_3	P54_3. En caso de una protesta pública, las autoridades deberían o no deberían h
        P54_4	P54_4. En caso de una protesta pública, las autoridades deberían o no deberían h
        P54_5	P54_5. En caso de una protesta pública, las autoridades deberían o no deberían h
        P54_6	P54_6. En caso de una protesta pública, las autoridades deberían o no deberían h
        P54_7	P54_7. En caso de una protesta pública, las autoridades deberían o no deberían h
        P54_8	P54_8. En caso de una protesta pública, las autoridades deberían o no deberían h
        P90	P90. Autoridades religiosas se han manifestado en contra del matrimonio entre pe
        P52	P52. En su opinión, ¿Cuándo un grupo social exige sus derechos mediante paros, bloqueos y plantones, ¿qué debe hacer el 
        P53_4	P53_4. ¿Cuál cree que es la mejor forma de actuar para que a usted lo tomen en cuenta las autoridades? Hacer una marcha
        P53_6	P53_6. ¿Cuál cree que es la mejor forma de actuar para que a usted lo tomen en cuenta las autoridades? Hacer bloqueos o 
    VICTIMA: 12 variables unicas
        P55_3_1	P55_3_1. ¿Quién o quiénes realizan las siguientes funciones?Aprobar los gastos d
        P55_3_2	P55_3_2. ¿Quién o quiénes realizan las siguientes funciones?Aprobar los gastos d
        P55_3_3	P55_3_3. ¿Quién o quiénes realizan las siguientes funciones?Aprobar los gastos d
        P55_5_1	P55_5_1. ¿Quién o quiénes realizan las siguientes funciones?Aprobar los impuesto
        P55_5_2	P55_5_2. ¿Quién o quiénes realizan las siguientes funciones?Aprobar los impuesto
        P55_5_3	P55_5_3. ¿Quién o quiénes realizan las siguientes funciones?Aprobar los impuesto
        P55_7_1	P55_7_1. ¿Quién o quiénes realizan las siguientes funciones?Aprobar los tratados
        P55_7_2	P55_7_1. ¿Quién o quiénes realizan las siguientes funciones?Aprobar los tratados
        P55_7_3	P55_7_1. ¿Quién o quiénes realizan las siguientes funciones?Aprobar los tratados
        P55_1_1	P55_1_1. ¿Quién o quiénes realizan las siguientes funciones? Juzgar a los delincuentes 1 Mención
        P55_1_2	P55_1_2. ¿Quién o quiénes realizan las siguientes funciones? Juzgar a los delincuentes 2 Mención
        P55_1_3	P55_1_3. ¿Quién o quiénes realizan las siguientes funciones? Juzgar a los delincuentes 3 Mención
    FALLA_ESTATAL: 67 variables unicas
        P13_1	P13_1. En una escala de 0 a 10,¿qué tanta confianza tiene usted en la policía?
        P13_10	P13_10. En una escala de 0 a 10,¿qué tanta confianza tiene usted en la Suprema C
        P13_11	P13_11. En una escala de 0 a 10,¿qué tanta confianza tiene usted en los sindicat
        P13_12	P13_12. En una escala de 0 a 10,¿qué tanta confianza tiene usted en el Instituto
        P13_13	P13_13. En una escala de 0 a 10,¿qué tanta confianza tiene usted en los partidos
        P13_14	P13_14. En una escala de 0 a 10,¿qué tanta confianza tiene usted en la Comisión
        P13_15	P13_15. En una escala de 0 a 10,¿qué tanta confianza tiene usted en el Ministeri
        P13_16	P13-16. En una escala de 0 a 10,¿qué tanta confianza tiene usted en las universi
        P13_17	P13_17. En una escala de 0 a 10,¿qué tanta confianza tiene usted en los tribunal
        P13_18	P13_18. En una escala de 0 a 10,¿qué tanta confianza tiene usted en el Ejército?
        P13_19	P13_19. En una escala de 0 a 10,¿qué tanta confianza tiene usted en el INEGI?
        P13_2	P13_2. En una escala de 0 a 10,¿qué tanta confianza tiene usted en la familia?
        P13_3	P13_3. En una escala de 0 a 10,¿qué tanta confianza tiene usted en los maestros?
        P13_4	P13_4. En una escala de 0 a 10,¿qué tanta confianza tiene usted en los medios de
        P13_5	P13_5. En una escala de 0 a 10,¿qué tanta confianza tiene usted en el Presidente
        P13_6	P13_6. En una escala de 0 a 10,¿qué tanta confianza tiene usted en la Iglesia?
        P13_7	P13_7. En una escala de 0 a 10,¿qué tanta confianza tiene usted en los jueces y
        P13_8	P13_8. En una escala de 0 a 10,¿qué tanta confianza tiene usted en las organizac
        P13_9	P13_9. En una escala de 0 a 10,¿qué tanta confianza tiene usted en los diputados
        P15	P15. Si la policía sabe que un detenido violó a una mujer, pero no tiene pruebas
    RED_PREVIA: 2 variables unicas
        P13_11	P13_11. En una escala de 0 a 10,¿qué tanta confianza tiene usted en los sindicat
        P13_8	P13_8. En una escala de 0 a 10,¿qué tanta confianza tiene usted en las organizaciones no gubernamentales?
    URBANO_RURAL: 1 variables unicas
        LOC	Localidad
    PONDERADOR: 1 variables unicas
        Pondi2	Factor de expansión post-estratificado


########## DETALLE R4.5 -- modulo ETI de ENSANUT 2024 (.dta, con etiquetas)
    ETI05A1	ETI05 ¿Dónde los ha visto?
    ETI05B1	ETI05 ¿Dónde los ha visto?
    ETI05C1	ETI05 ¿Dónde los ha visto?
    ETI05D1	ETI05 ¿Dónde los ha visto?
    ETI05E1	ETI05 ¿Dónde los ha visto?
    ETI05F1	ETI05 ¿Dónde los ha visto?
    ETI12GA	ETI12G. ¿Este producto tiene exceso de algún elemento o nutriente asociado con d
    ETI12GB	ETI12G. ¿Este producto tiene exceso de algún elemento o nutriente asociado con d
    ETI12GC	ETI12G. ¿Este producto tiene exceso de algún elemento o nutriente asociado con d
    ETI12GD	ETI12G. ¿Este producto tiene exceso de algún elemento o nutriente asociado con d
    ETI12GE	ETI12G. ¿Este producto tiene exceso de algún elemento o nutriente asociado con d
    ETI12GF	ETI12G. ¿Este producto tiene exceso de algún elemento o nutriente asociado con d
    ETI12GG	ETI12G. ¿Este producto tiene exceso de algún elemento o nutriente asociado con d
    ETI12GH	ETI12G. ¿Este producto tiene exceso de algún elemento o nutriente asociado con d
    ETI12GI	ETI12G. ¿Este producto tiene exceso de algún elemento o nutriente asociado con d
    ETI12GJ	ETI12G. ¿Este producto tiene exceso de algún elemento o nutriente asociado con d
    ETI14A	ETI14 ¿Este producto tiene exceso de algún elemento o nutriente asociado con dañ
    ETI14B	ETI14 ¿Este producto tiene exceso de algún elemento o nutriente asociado con dañ
    ETI14C	ETI14 ¿Este producto tiene exceso de algún elemento o nutriente asociado con dañ
    ETI14D	ETI14 ¿Este producto tiene exceso de algún elemento o nutriente asociado con dañ
    ETI14E	ETI14 ¿Este producto tiene exceso de algún elemento o nutriente asociado con dañ
    ETI14F	ETI14 ¿Este producto tiene exceso de algún elemento o nutriente asociado con dañ
    ETI14G	ETI14 ¿Este producto tiene exceso de algún elemento o nutriente asociado con dañ
    ETI14H	ETI14 ¿Este producto tiene exceso de algún elemento o nutriente asociado con dañ
    ETI14I	ETI14 ¿Este producto tiene exceso de algún elemento o nutriente asociado con dañ
    ETI14J	ETI14 ¿Este producto tiene exceso de algún elemento o nutriente asociado con dañ
    ETI16A	ETI16 ¿Por qué?
    ETI16B	ETI16 ¿Por qué?
    ETI16C	ETI16 ¿Por qué?
    ETI16D	ETI16 ¿Por qué?
    ETI16E	ETI16 ¿Por qué?
    ETI16F	ETI16 ¿Por qué?
    ETI181A	ETI181 Dígame las etiquetas que usted lee
    ETI181B	ETI181 Dígame las etiquetas que usted lee
    ETI181C	ETI181 Dígame las etiquetas que usted lee
    ETI181D	ETI181 Dígame las etiquetas que usted lee
    ETI181E	ETI181 Dígame las etiquetas que usted lee
    ETI32A	ETI32 Actualmente, cuando usted está decidiendo si va a comprar un alimento o be
    ETI32B	ETI32 Actualmente, cuando usted está decidiendo si va a comprar un alimento o be
    ETI32C	ETI32 Actualmente, cuando usted está decidiendo si va a comprar un alimento o be
    eti01	ETI01 ¿Cuántas calorías considera usted que una persona adulta debe consumir en
    eti02	ETI02 ¿Usted sabe leer?
    eti03	ETI03 ¿Usted sabe si los alimentos empacados y las bebidas embotelladas tienen i
    eti04	ETI04 ¿Me puede decir si ha visto estos sellos?
    eti05a	ETI05A ¿Me puede decir si ha visto estas leyendas?
    eti05b	ETI05B ¿Me puede decir si ha visto los sellos de números?
    eti05c	ETI05C ¿Está usted de acuerdo con que los alimentos y bebidas tengan el etiqueta
    eti05d	ETI05D ¿Por qué?
    eti06	ETI06 ¿Cuál de los cuatro productos compraría?
    eti07	ETI07 ¿Cuál de los cuatro productos compraría?
    eti11	ETI11 ¿Cuál es el producto menos saludable?
    eti12	ETI12 ¿Qué tan fácil o difícil le resultó responder las preguntas?
    eti12a	ETI12A. ¿Cuál es el producto menos saludable?
    eti12b	ETI12B. ¿Qué tan fácil o difícil le resultó responder la pregunta anterior?
    eti12c	ETI12C. ¿Cuál es el producto menos saludable?
    eti12d	ETI12D. ¿Qué tan fácil o difícil le resultó responder la pregunta anterior?
    eti12e	ETI12E. ¿Cuál es el producto menos saludable?
    eti12f	ETI12F. ¿Qué tan fácil o difícil le resultó responder la pregunta anterior?
    eti15	ETI15 ¿Le daría este producto a un niño o niña?
    eti15esp	ETI15ESP Especifique
    eti16esp	ETI16ESP Especifique
    eti17	ETI17 ¿Usted lee la información nutrimental de los alimentos empacados y las beb
    eti18	ETI18 ¿Usted le alguna de estás etiquetas?
    eti182	ETI182 De las etiquetas que mencionó, ¿cuál es la etiqueta que usted lee con may
    eti183	ETI183 ¿Cuál de las etiquetas considera que es más confiable para saber si un pr
    eti19	ETI19 ¿Con qué frecuencia utiliza la etiqueta nutrimental que usted me mencionó
    eti21	ETI21 ¿Usted utiliza los sellos de "EXCESO" para decidir la compra de alimentos
    eti21a	ETI21A. ¿Usted utiliza las leyendas de edulcorantes y cafeína para decidir la co
    eti21b	ETI21B. ¿Usted utiliza los sellos de números para decidir la compra de alimentos
    eti22	ETI22 ¿Había escuchado anteriormente sobre esta medida?
    eti23	ETI23 ¿Cómo evaluaría esta medida?
    eti24a	ETI24A. ¿Con qué frecuencia realiza las compras de bebidas y alimentos empaqueta
    eti25	ETI25 Al momento de realizar sus compras, al ver los sellos de advertencia en lo
    eti25esp	ETI25ESP Especifique
    eti27	ETI27 Piense en la última vez que fue de compras y uno de los productos que norm
    eti27esp	ESPECIFIQUE
    eti28	ETI28 ¿Por qué?
    eti28esp	ESPECIFIQUE
    eti29	ETI29 ¿Qué producto fue?
    eti32esp	ETI32ESP Otro, Especifique
    eti33a	ETI33A Exceso calorías
    eti33b	ETI33B Exceso azúcares
    eti33c	ETI33C Exceso sodio
    eti33d	ETI33D Exceso grasas saturadas
    eti33e	ETI33E Exceso grasas trans


########## DETALLE R9.3 -- bateria p53, Sociedad de la Informacion (UNAM-IIJ)
    p53_1	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Su familia
    p53_10	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? La televisión extranjera
    p53_11	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Los empresarios
    p53_12	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? El gobernador de su estado
    p53_13	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? La radio
    p53_14	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Los libros de texto
    p53_15	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Los curas, sacerdotes o ministros
    p53_16	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Los famosos que salen en televis
    p53_17	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Sus amigos
    p53_18	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Los partidos políticos
    p53_19	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? El internet
    p53_2	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? La televisión nacional
    p53_20	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Los diputados
    p53_21	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Los cantantes
    p53_22	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Las organizaciones sociales
    p53_23	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Sus vecinos
    p53_24	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? El Instituto Nacional Electoral
    p53_25	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Blogs de internet
    p53_3	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? La publicidad de la radio
    p53_4	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? El Presidente de la República
    p53_5	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Las Redes sociales
    p53_6	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Los periódicos
    p53_7	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Los maestros
    p53_8	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? La publicad del Gobierno Federal
    p53_9	53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da...? Los comerciales de televisión


########## DETALLE R9.3 -- bateria p33, Medio Ambiente (corroboracion secundaria)
    p33_1	33 De los siguientes medios que proporcionan información sobre el ambiente, dígame en qué orden los pondría, donde el 1 es el más confiable y el 8 el menos confiable. 1ª MENCIÒN
    p33_2	33 De los siguientes medios que proporcionan información sobre el ambiente, dígame en qué orden los pondría, donde el 1 es el más confiable y el 8 el menos confiable. 2ª MENCIÒN
    p33_3	33 De los siguientes medios que proporcionan información sobre el ambiente, dígame en qué orden los pondría, donde el 1 es el más confiable y el 8 el menos confiable. 3ª MENCIÒN
    p33_4	33 De los siguientes medios que proporcionan información sobre el ambiente, dígame en qué orden los pondría, donde el 1 es el más confiable y el 8 el menos confiable. 4ª MENCIÒN
    p33_5	33 De los siguientes medios que proporcionan información sobre el ambiente, dígame en qué orden los pondría, donde el 1 es el más confiable y el 8 el menos confiable. 5ª MENCIÒN
    p33_6	33 De los siguientes medios que proporcionan información sobre el ambiente, dígame en qué orden los pondría, donde el 1 es el más confiable y el 8 el menos confiable. 6ª MENCIÒN
    p33_7	33 De los siguientes medios que proporcionan información sobre el ambiente, dígame en qué orden los pondría, donde el 1 es el más confiable y el 8 el menos confiable. 7ª MENCIÒN
    p33_8	33 De los siguientes medios que proporcionan información sobre el ambiente, dígame en qué orden los pondría, donde el 1 es el más confiable y el 8 el menos confiable. 8ª MENCIÒN
```
