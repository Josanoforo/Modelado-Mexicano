# ACTO MAESTRA38-C1 · RE-ASIENTO · CANDIDATAS · ENFIH-4 · APIPIE · PONDERADOR-ENNVIH

Archivado verbatim por A.3 (0-bis). Texto tal como llegó de mesa, 7/sep/2026.

---

CAJA · ACTO MAESTRA38-C1 · RE-ASIENTO · CANDIDATAS · ENFIH-4 · APIPIE · PONDERADOR-ENNVIH — invoca /acto

COMPUERTA: ninguna · ENTORNO: UBUNTU con corpus (capa3_disco_real), sin red · MODELO: Sonnet (Opus si alta_relacion.py exige juicio) · SPEC: forense/prereg-caja/S3-C1-spec-v1_0.md, reducida: 1 re-asiento bajo N36 (etiquetado → R4.5/N45), no 7 (corrección de N3). FIRMAS — verbatim: N8 «re-asiento… revertido, sucesor declarado»; revisión 5/sep: «una necesidad sobre una fuente que ya está en corpus es una relación CANDIDATA, no una fila de cola»; FP-288 (4/sep §3: enlazar las 4 ENFIH por el criterio (b) de Frente D); D6 «Creamos las cuentas y bajamos archivos»; mesa 6/sep «a completamente»; mesa 7/sep (benchmark §B de SELLO-2): «qué necesitaríamos para moverlo» → pieza (h). Premisas (verificadas por el ejecutor de CARGA-LAPOP y por dirección; se re-verifican en el 0-bis): (i) 3 filas PENDIENTE con el id de regla en la columna 1 de data/cola-adquisicion-v1_0.tsv (salud.adherencia.desabasto_vs_cuidadora, cooperacion.comite.monitoreo_sancion_visible, cooperacion.faena.sancion_social_pueblo_mestizo); (ii) N42–N45 no existen en necesidad-objeto-modelo.tsv (máximo N41); propuestas en MAESTRA38-N11:72, TABLERO-PROGRAMA y registro-rotulos.tsv → si D1 no se ejecutó, C1 la ejecuta como pieza (a0) con el texto de N11:72, y lo dice; (iii) FP-288 ABIERTA, 4 filas de relaciones.tsv (N3, N10, N13, N14, ENFIH) con id_manifiesto = NO_DETERMINADO; sha de ENFIH COINCIDE en A4 (be372533…2ef4d5, manifiesto.yaml:4115); (iv) MEX_2016_APIPIE_v01_M_Stata.zip → 0 en manifiesto; fila IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016 PENDIENTE-DE-MESA; (v) grep -cE "APIPIE|6667" forense/hallazgos.md → 0; (vi) relaciones.tsv 223 líneas, SE ENLAZA 20, N36 11; (vii) ENNViH 2002: ennvih1_2002_hogar_dta (ennvih/ehh02dta_all.zip) y ennvih1_2002_hogar_cb (ennvih/ehh02cb_all.zip) registrados — ADR-357 los dio por ausentes. EJECUCIÓN — COMMIT-2, por pieza: (a0) alta de N42–N45 si aplica (D1). (a) re-asiento por alta_relacion.py (relación nueva, id determinista) + situacion: SUPERADA-POR <id> en la vieja, 0 líneas borradas. (b) las 3 filas con id de regla → 3 relaciones CANDIDATA: R4.3 → Cero Desabasto + MACU (OBTENIDO), R8.1 y R8.4 → CNGMD (646 entradas; nota «diseño multinivel pendiente: ¿el CNGMD codifica monitoreo/sanción como atributo del comité?»); filas → estado: SUPERADA-POR <relacion_id> + nota, no se borran. (c) ENFIH-4: COINCIDE 4/4 → id_manifiesto + sha256_fuente + via_capa2 --escribe; FP-288 → EJECUTADA / CERRADA-NO-COINCIDE. (d) python3 tests/manifiesto.py --verifica --id <id> una invocación por id sobre los 18 de L2-LISTA (2 list + 16 Dataverse), tres resultados sin colapsar; si COINCIDEN, los 16 «nuevos» del censo del 6/sep en ACADEMICO-dataverse-mps2012/ son falso positivo del emparejador → hallazgo con el nombre exacto, nada se promueve de esa carpeta. (e) Promover MEX_2016_APIPIE_v01_M_Stata.zip: A.7, testzip, prefijo adq15_wb6667_, raiz: descargas_mx; fila → OBTENIDO con reserva en nota: («§2.1 del 3/sep: sin reactivo de deferencia ni desenlace laboral; no responde N15/G6 sin cruce por texto»). (f) hallazgos.md: «6/sep: petición manual WB 6667 cubrió 24 archivos; 23 ya en corpus desde 18/ago; sólo el .zip Stata faltaba — A.8 contra el manifiesto, no contra la página». (g) baseline.py {"ok": true}, baseline.json recifrado, via_capa2 lectura sin diffs nuevos. (h) Ponderador ENNViH (B33, sólo listar): tools/inventario_fd.py (o inventario_fd_ext.py) sobre ennvih/ehh02cb_all.zip y ennvih/doc/ehh02cb_b*.pdf → tabla data/ennvih2002-ponderadores-candidatos-v1_0.tsv: variable · etiqueta verbatim · libro · n no-nulo en ehh02dta_all.zip (libro bx y hogar) · rango. Los tres candidatos que ADR-357 llamó ambiguos, más cualquier otro que aparezca. No adjudica: dirección lo hace con la tabla a la vista (sucesor: L16-bis/L17-bis rama A). PERÍMETRO. Toca: data/curacion-registro/{relaciones,evidencias,utilidad-modelo,necesidad-objeto-modelo}.tsv + baseline.json · cola (3 filas + APIPIE) + vista · manifiesto (+1) · staging · data/ennvih2002-ponderadores-candidatos-v1_0.tsv (nuevo) · forense/notas/2026-09-0X-MAESTRA38-C1-*.md · hallazgos · tablero (recibo; FP-288) · A.3 · cascada. NO toca: milpa/** · canon (salvo ADR) · data/l*-* · specs · el clon ACADEMICO-list-cran/ (regla #559) · tests/*.py · tools/*.py. En paralelo: LOTE-CRUCE (data/cruce-*, inventario v1_2, S11-*, modulo-propio-v0). CONTADOR: relaciones de salud bajo N correcto +1 · CANDIDATA +3 · filas de cola con id de regla 3 → 0 · SE ENLAZA 20 → 24 si ENFIH · payloads +1 · candidatos a ponderador ENNViH 0 → k (listados) · medición: cero.

---

## A.8 · `tools/ya_medido.py` — apéndice del ejecutor, NO parte del texto verbatim

El bloque de arriba es el encargo tal como llegó y no se edita (A.3). Esto es apéndice
del acto: la regla de `ADR-340` exige que todo acto que CLASIFIQUE, PRE-REGISTRE, CARGUE
o SELLE una regla del motor pegue aquí la salida de la herramienta. `MAESTRA38-C1` da de
alta relaciones `CANDIDATA` sobre `R4.3`/`R8.1`/`R8.4` y re-asienta una bajo `R4.5`.
**Las cuatro salen `NUNCA-MEDIDA`, y este acto tampoco las mide: medición del motor = cero.**

```
=== ya_medido: salud.adherencia.desabasto_vs_cuidadora ===
  resuelto por canon: salud.adherencia.desabasto_vs_cuidadora -> R4.3 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): salud.adherencia.desabasto_vs_cuidadora, R4.3

-- milpa/tramite.yaml --
  (sin apariciones)

-- milpa/tramite-ola5-propuesta-v0.yaml --
  (sin apariciones)

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:704  tier=[MEDIA]
      - **49 reglas** *(42 en v2 · 43 en v2.1 por conf.07 · 44 en v2.3 al partir la diagonal)*. **Hito D (perímetro de 27 reglas, subconjunto de las 49): 26 de 27 corridas archivadas**<!-- T20:HITO-D pob=re
  canon/modelo-decision-v4_0.md:723  tier=[FUERTE]
      ⚠️ **Corrección de RÓTULO, 29/jul/2026 (cambio 34).** Este renglón decía *"20 `[FUERTE]` + 5 `[MEDIA-FUERTE]` + 2 compuestas"*. Solo existe **una** compuesta: `R4.3` (`[FUERTE / MEDIA]`), cuya propia 
  canon/modelo-decision-v4_0.md:749  tier=[FUERTE / MEDIA]
      | `R4.3` | L243 | Desabasto → abandono / familia cuidadora → adherencia | `[FUERTE / MEDIA]` — compuesta | Sí |

-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-03-MAESTRA37-L1-censo.md:72  
      - `salud.adherencia.desabasto_vs_cuidadora`: `--regex "(dejo\|abandon\|interrump).{0,30}(tratamiento\|medicament)"` · `--regex "surti\w+.{0,25}(medicament\|receta)\|receta.{0,25}surti"` · `--regex "fa
  forense/notas/2026-09-03-MAESTRA37-L1-remapeo.md:27  
      | `salud.adherencia.desabasto_vs_cuidadora` | NO-ENCONTRADO | EXISTE-NO-SATISFACE (Cero Desabasto, disparador sin desenlace) | **NO-ENCONTRADO** — 0/0/0 en las tres formulaciones dirigidas |
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:113  
      ## R4.3 · `salud.adherencia.desabasto_vs_cuidadora` — desabasto: **`NO-ACCESIBLE` → `EXISTE-SATISFACE`** · cuidadora: `NO-ENCONTRADO` sin cambio
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:216  
      existente»*, declarando que no afirmaba que sirvieran a R4.3 y dejando la
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:230  
      **El componente que sí sirve a R4.3 no está entre las ocho altas: es `adultos`**,
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:232  
      existía para R4.3). La adjudicación queda hecha: **1 de 8 altas tiene regla
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:250  
      | `salud.adherencia.desabasto_vs_cuidadora` | NO-ENCONTRADO | EXISTE-NO-SATISFACE | NO-ENCONTRADO | NO-ACCESIBLE (desabasto) + NO-ENCONTRADO (cuidadora) | **EXISTE-SATISFACE** (desabasto, 337/337 y 67
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:256  
      > `salud.adherencia.desabasto_vs_cuidadora` rama desabasto). Era 1.
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:269  
      El falsador que L3 dejó escrito —*«se espera que R4.3 pase a EXISTE-SATISFACE y
  forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md:101  
      ## R4.3 · `salud.adherencia.desabasto_vs_cuidadora` — `NO-ACCESIBLE` (rama desabasto) · `NO-ENCONTRADO` (rama cuidadora)
  forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md:164  
      Lo que falta es **instrumento**, no sólo adquisición — a diferencia de R4.3.
  forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md:217  
      | `salud.adherencia.desabasto_vs_cuidadora` | NO-ENCONTRADO | EXISTE-NO-SATISFACE (Cero Desabasto) | NO-ENCONTRADO | **NO-ACCESIBLE** (desabasto: reactivo exacto `a0313`/`a0314`, microdato ausente) · 
  forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md:236  
      | `salud.adherencia.desabasto_vs_cuidadora` | **el archivo `adultos_ensanut2024_w.stata.stata.zip`** | **ADQUISICIÓN** — el reactivo ya existe y satisface; es la única de las cuatro que puede voltear 
  forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md:250  
      tres capas del curador, doble hash, y re-veredicto de R4.3 y R4.2 contra
  forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md:251  
      microdato. Se espera que R4.3 pase a `EXISTE-SATISFACE` y R4.2 se quede en
  forense/notas/2026-09-06-MAESTRA38-LOTE-ENSANUT-resultados.md:145  
      `salud.atencion.desabasto`, R4.3)** — antes de este acto. Este lote **mide

-- forense/prereg-caja/S*-spec-*.md --
  forense/prereg-caja/S3-C1-spec-v1_0.md:42  
      | `REL-ff6da3b0a22322433d42b4eb` | `CERO_DESABASTO` | `OE-9ccc0aa9606acf5881179a4e` | pre-A1, objeto de evidencia original de `N36`/`R4.3` — **fuera de alcance de C1** |

-- canon/registro-rotulos.tsv (alias) --
  canon/registro-rotulos.tsv:112  
      N	MAESTRA34-N6
  canon/registro-rotulos.tsv:150  
      N	MAESTRA36-N6
  canon/registro-rotulos.tsv:151  
      N	MAESTRA37-N1
  canon/registro-rotulos.tsv:155  
      L	MAESTRA37-L3
  canon/registro-rotulos.tsv:159  
      L	MAESTRA37-L3-BIS

========================================
NUNCA-MEDIDA

=== ya_medido: cooperacion.comite.monitoreo_sancion_visible ===
  resuelto por canon: cooperacion.comite.monitoreo_sancion_visible -> R8.1 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): cooperacion.comite.monitoreo_sancion_visible, R8.1

-- milpa/tramite.yaml --
  (sin apariciones)

-- milpa/tramite-ola5-propuesta-v0.yaml --
  (sin apariciones)

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:704  tier=[MEDIA]
      - **49 reglas** *(42 en v2 · 43 en v2.1 por conf.07 · 44 en v2.3 al partir la diagonal)*. **Hito D (perímetro de 27 reglas, subconjunto de las 49): 26 de 27 corridas archivadas**<!-- T20:HITO-D pob=re
  canon/modelo-decision-v4_0.md:768  tier=[FUERTE]
      | `R8.1` | L278 | Comité con monitoreo + sanción visible → contribuye; sin ellos, free-riding | `[FUERTE]` | Sí |

-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-03-MAESTRA37-L1-censo.md:82  
      - `cooperacion.comite.monitoreo_sancion_visible`: `--regex "comite\w*"` · `--regex "(participa\|pertenece\|miembro).{0,40}(organizacion\|asociacion\|comite\|grupo)"` · `--regex "(coopera\w+\|aport\w+)
  forense/notas/2026-09-03-MAESTRA37-L1-remapeo.md:50  
      | `cooperacion.comite.monitoreo_sancion_visible` | 0·0·0 | **NO-ENCONTRADO** |

-- forense/prereg-caja/S*-spec-*.md --
  forense/prereg-caja/S8-L18-spec-v1_0.md:197  
      **Medición: caja, acto `MAESTRA38-L18` (rótulo derivado por continuidad de la serie `L` — máximo registrado hoy en `canon/registro-rotulos.tsv` es `L14`; `L15` queda deliberadamente sin usar aquí porq

-- canon/registro-rotulos.tsv (alias) --
  (sin apariciones)

========================================
NUNCA-MEDIDA

=== ya_medido: cooperacion.faena.sancion_social_pueblo_mestizo ===
  resuelto por canon: cooperacion.faena.sancion_social_pueblo_mestizo -> R8.4 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): cooperacion.faena.sancion_social_pueblo_mestizo, R8.4

-- milpa/tramite.yaml --
  (sin apariciones)

-- milpa/tramite-ola5-propuesta-v0.yaml --
  (sin apariciones)

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:771  tier=[MEDIA]
      | `R8.4` | L281 | Pueblo mestizo con sanción social → participa; urbano sin sanción → baja | `[MEDIA]` | No |

-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-03-MAESTRA37-L1-censo.md:85  
      - `cooperacion.faena.sancion_social_pueblo_mestizo`: `--palabra faena --palabra tequio --palabra "cooperacion vecinal"` · `--regex "(coopera\w+\|aport\w+).{0,35}(obra\|comunidad\|colonia\|vecin)"` · `
  forense/notas/2026-09-03-MAESTRA37-L1-remapeo.md:53  
      | `cooperacion.faena.sancion_social_pueblo_mestizo` | 0·0·0 | **NO-ENCONTRADO** |

-- forense/prereg-caja/S*-spec-*.md --
  forense/prereg-caja/S8-L18-spec-v1_0.md:197  
      **Medición: caja, acto `MAESTRA38-L18` (rótulo derivado por continuidad de la serie `L` — máximo registrado hoy en `canon/registro-rotulos.tsv` es `L14`; `L15` queda deliberadamente sin usar aquí porq

-- canon/registro-rotulos.tsv (alias) --
  (sin apariciones)

========================================
NUNCA-MEDIDA

=== ya_medido: salud.consumo.sellos_precio_similar ===
  resuelto por canon: salud.consumo.sellos_precio_similar -> R4.5 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): salud.consumo.sellos_precio_similar, R4.5

-- milpa/tramite.yaml --
  (sin apariciones)

-- milpa/tramite-ola5-propuesta-v0.yaml --
  (sin apariciones)

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:750  tier=[MEDIA]
      | `R4.5` | L244 | Producto con sellos + precio similar → elige menos sellos | `[MEDIA]` | No |

-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-03-MAESTRA37-L1-censo.md:73  
      - `salud.consumo.sellos_precio_similar`: `--regex "sello\w*.{0,30}(product\|alimento\|etiquet)\|etiquetado frontal"` · `--regex "grave\|gravedad\|severidad"` (control) · `--regex farmacia` (control)
  forense/notas/2026-09-03-MAESTRA37-L1-remapeo.md:28  
      | `salud.consumo.sellos_precio_similar` | NO-ENCONTRADO | NO-APLICA | **NO-ENCONTRADO** — 0/31 677 |
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:157  
      ## R4.5 · `salud.consumo.sellos_precio_similar` — **`NO-ENCONTRADO` → `EXISTE-NO-SATISFACE`**
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:208  
      con sello y del sustituto) o una tarea de elección con precio enunciado. **R4.5
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:221  
      | **etiquetado** | **R4.5** `salud.consumo.sellos_precio_similar` | `eti21`/`eti25`/`eti27`/`eti33*` miden el desenlace de la regla; es el único componente que la toca |
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:222  
      | **actividad física** | **ninguna** de R4.1–R4.5 | mide conducta de ejercicio; ninguna regla de §3.4 la condiciona ni la predice. *(El encargo la sugería como «apoyo» de R4.2: no lo es — no contiene 
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:233  
      (etiquetado→R4.5); 7 de 8 no la tienen** y su `clasificacion_relacion =
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:251  
      | `salud.consumo.sellos_precio_similar` | NO-ENCONTRADO | NO-APLICA | NO-ENCONTRADO | NO-ENCONTRADO | **EXISTE-NO-SATISFACE** — módulo `etiquetado`; falta «precio similar» |
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:273  
      mirar: *«si etiquetado levanta sellos frontales × decisión de compra, R4.5 puede
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:275  
      levanta sellos frontales × decisión de compra —eso era correcto— y aun así R4.5
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:291  
      | `salud.consumo.sellos_precio_similar` | **un ítem de precio**: el del producto con sello y el del sustituto, o una tarea de elección con precio enunciado | **INSTRUMENTO** | **No** — pero es la brec
  forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:299  
      podía decir: **la brecha más barata es un solo ítem de precio en R4.5.**
  forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md:172  
      ## R4.5 · `salud.consumo.sellos_precio_similar` — `NO-ENCONTRADO`
  forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md:218  
      | `salud.consumo.sellos_precio_similar` | NO-ENCONTRADO | NO-APLICA | NO-ENCONTRADO | **NO-ENCONTRADO** — 0/0 en los 4 términos, con control positivo |
  forense/notas/2026-09-03-MAESTRA37-L3-veredictos.md:239  
      | `salud.consumo.sellos_precio_similar` | todo: sellos y precio | **INSTRUMENTO** — ENSANUT 2024 no levanta etiquetado frontal en sus cinco módulos |

-- forense/prereg-caja/S*-spec-*.md --
  forense/prereg-caja/S3-C1-spec-v1_0.md:25  
      > | **etiquetado** | **R4.5** `salud.consumo.sellos_precio_similar` | es el único componente que toca el desenlace de la regla |
  forense/prereg-caja/S3-C1-spec-v1_0.md:26  
      > | actividad física / antropometría / frecuencias / rec24h / lactancia / plomo / sangre (7 componentes) | **ninguna** de R4.1–R4.5 | ... |
  forense/prereg-caja/S3-C1-spec-v1_0.md:28  
      > **"1 de 8 altas tiene regla (etiquetado→R4.5); 7 de 8 no la tienen y su `clasificacion_relacion = CANDIDATA` es correcta y se queda."**
  forense/prereg-caja/S3-C1-spec-v1_0.md:81  
      **Entrada YAML ya llenada para `tools/curador_registro/alta_relacion.py`**, construida copiando los valores reales de la fila `N36` (`relaciones.tsv:213`, `evidencias.tsv:214`, `utilidad-modelo.tsv` f
  forense/prereg-caja/S3-C1-spec-v1_0.md:91  
      ENSANUT Continua 2024 a R4.5/N41. Mismo payload, misma fuente, mismo objeto que
  forense/prereg-caja/S3-C1-spec-v1_0.md:110  
      Re-asentado bajo N41/R4.5 por adjudicacion de MAESTRA37-L3-BIS (etiquetado -> unico
  forense/prereg-caja/S3-C1-spec-v1_0.md:115  
      la lectura de eti21/eti25/eti27/eti33 (variables que sirven a R4.5 segun L3-BIS) es
  forense/prereg-caja/S3-C1-spec-v1_0.md:130  
      (unico de 8 componentes que sirve a una regla de salud: R4.5). Ninguna variable
  forense/prereg-caja/S3-C1-spec-v1_0.md:141  
      siguiente_accion: "C1 (o sucesor): abrir el componente, leer eti21/eti25/eti27/eti33, confirmar que sirven a R4.5."
  forense/prereg-caja/S3-C1-spec-v1_0.md:142  
      objeto_modelo_origen: R4.5
  forense/prereg-caja/S3-C1-spec-v1_0.md:143  
      objeto_modelo_origen_ref: "canon/modelo-decision-v4_0.md:411 (salud.consumo.sellos_precio_similar)"
  forense/prereg-caja/S3-C1-spec-v1_0.md:148  
      reserva: "Re-asentado por adjudicacion documental de L3-BIS, no por lectura de variable. Requiere abrir el componente y confirmar eti21/eti25/eti27/eti33 antes de parametrizar R4.5."
  forense/prereg-caja/S3-C1-spec-v1_0.md:149  
      verificacion_requerida: "Abrir el componente etiquetado, mapear eti21/eti25/eti27/eti33, confirmar que cubren R4.5 (sellos_precio_similar)."
  forense/prereg-caja/S3-C1-spec-v1_0.md:152  
      siguiente_accion: "C1 (o sucesor): lectura de eti21/eti25/eti27/eti33 y parametrizacion de R4.5."

-- canon/registro-rotulos.tsv (alias) --
  canon/registro-rotulos.tsv:159  
      L	MAESTRA37-L3-BIS

========================================
NUNCA-MEDIDA

```

---

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-C1 · RE-ASIENTO` (7/sep/2026, CAJA con corpus), `ADR-370`.
Rama `acto/maestra38-c1-re-asiento`, COMMIT-2 `7765c21`. **PR #577** (abierto, NO fusionado — el merge es de mesa).
Desenlace: **ejecutado completo**, con tres correcciones de premisa declaradas (`N45` no existe,
`SE ENLAZA 20→24` inalcanzable, «16 nuevos» no reproducible) y dos desvíos declarados en la pieza (e)
(prefijo de id no alcanzable sin tocar `tests/`, A.7 doble descarga no reproducible).
Nota de cierre: `forense/notas/2026-09-07-MAESTRA38-C1-cierre.md`.
