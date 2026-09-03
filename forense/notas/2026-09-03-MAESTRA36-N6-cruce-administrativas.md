# Cruce que faltaba — fuentes administrativas registradas × las 25 reglas de Ola 6

`ACTO MAESTRA36-N6 · CORRIGE-N5-Y-REMAPEA-OLA6-ADMINISTRATIVAS`, P2 y P3.
Corrida 3/sep/2026, entorno **NUBE**, contra `origin/main = bbc57f0`.
Encargo archivado por A.3 en
`forense/encargos/2026-09-03-MAESTRA36-N6-CORRIGE-N5-Y-REMAPEA-OLA6-ADMINISTRATIVAS.md`.

**Este acto no abre ningún dominio.** Corrige un negativo falso (P1) y corre
el cruce que ningún acto tenía asignado (P2), para que la evaluación del
criterio 2 sea completa. La lectura del criterio y la apertura son de mesa.

**Ninguna búsqueda abrió microdato.** Todo lo de abajo se resuelve con
metadato versionado: `data/manifiesto.yaml` (campo `usado_para` y `nota`),
la nota de A1 y los descriptores registrados. `ls data/raw/` → **0 archivos**
(corpus compartido ausente, esperado en nube). Lo que no se puede resolver
sin abrir bytes se marca `CANDIDATO-ABRIR-EN-CAJA` y **no se promueve**.

---

## §0 · Por qué este cruce faltaba (cobertura retroactiva, verificada)

`/mapea` (`.claude/commands/mapea.md`, `ADR-247`) corre
`tools/busca_reactivos.py` sobre `data/inventario-reactivos-v1_2.tsv` +
`data/inventario-reactivos-ext-v1_0.tsv` — **241 591 filas de reactivos de
encuesta**. Las fuentes administrativas registradas **no tienen filas ahí
por construcción**: no son encuestas, no tienen reactivos, y ningún
inventario de reactivos las indexa. `MAESTRA34-A1` ya lo había medido con
control positivo y lo dejó escrito (`ADR-278`: «`/mapea` **no es ejecutable
sobre payloads nuevos**… `0` para `urgencias`/`dgis`/`desabasto`/`macu`/
`cngmd`», contra `ENCIG` 14 581 · `ENVIPE` 31 140 de control).

La otra vía posible tampoco lo cubría:

```
$ grep -aciE 'salud\.' data/curacion-registro/utilidad-modelo.tsv
0
```
(universo: 1 archivo, 207 filas de proyección — el curador **no liga
ninguna fuente a ninguna regla de salud**.)

Luego el cruce «fuentes administrativas registradas × 25 reglas de Ola 6»
**nunca se corrió**: no es que diera negativo, es que **nadie corrió el
mecanismo** — la tercera variante de v2.4. `utilidad-modelo.tsv` nace el
29/ago (`ADR-267`); las fuentes de A1/A2 entran el 1–2/sep; el mapeo de N5
es del 3/sep. Ningún acto en esa ventana lo tenía asignado.

---

## §1 · Universo declarado (A.13) — 7 programas, 178 entradas de manifiesto

Derivado por bloque de entrada sobre las **1 104** entradas de
`data/manifiesto.yaml` (`- id:` a columna 0), no por `grep` de línea suelta:

| programa | entradas | qué es la unidad de registro | qué mide |
|---|---|---|---|
| **CNGMD 2023** (INEGI) | 94 | **gobierno municipal / demarcación** | censo de gobiernos: m1 ayuntamientos y alcaldías, m2 administración pública (`participa_ciudadana`, `tramites_servicios`, `programas_sociales`, `contrata_publica`, `ctrl_inter_anticorr`, `marco_regulatorio`, `rec_huma`, `servicios_publicos`…), m3 seguridad pública, m4 protección civil, m5 justicia cívica, m6 agua, m7 residuos |
| **SICEE / INE cómputos locales** | 65 | **casilla / sección / municipio** | resultados electorales locales, calendarios PEL, lista nominal |
| **DGIS Urgencias** (Salud) | 11 | **evento de urgencia** (+ CLUES del establecimiento) | descriptores 2008-2017 / 2018 / 2019 / 2023-2025, catálogos CLUES, microdato 2008, 2009, 2025, 2026 |
| **Observatorio de Cuidados / MACU** (Inmujeres) | 4 | **municipio / territorio** | indicadores territoriales de cuidados (+ ENASIC 2022 y ELCOS 2012, que **sí son encuestas** y no entran a este cruce) |
| **Cero Desabasto** | 2 | **reporte × insumo** | agregado entidad×cuatrimestre; y la base histórica: 11 036 filas = 7 914 reportes distintos, 2019-02-18 a 2024-09-03, con `Fecha de Registro` (0 % nula), `Tipo de informante`, `Padecimiento`, `Entidad`, `Institución`, `CLUES`, `Hospital o clínica` |
| **CompraNet / ComprasMX** | 2 | **contrato / expediente** | contratos 2022-2023, expedientes 2019-2023, llaves proveedor-procedimiento-sanción |

Comando de derivación y conteos crudos por término (universo declarado: **1
archivo, 1 104 entradas, 21 480 líneas**):
`sicee` 148 · `cngmd` 646 · `dgis` 50 · `desabasto` 14 · `cuidados` 9.

**El hecho estructural que gobierna las 25 filas de abajo, escrito antes de
la tabla:** las seis unidades de registro de arriba son
**establecimiento, municipio, evento administrativo o contrato**. Las 25
reglas de Ola 6 son, sin excepción, reglas de **conducta individual**
(`SI` una persona está en el estado X `ENTONCES` hace Y). El tercer término
del vocabulario A.4 —**¿misma unidad de análisis?**— es por tanto el que
decide la mayoría de los pares, y se aplica igual en las 25. Esto no se
descubrió al final: se declara aquí para que no parezca conclusión ad hoc.

---

## §2 · Veredicto por par (A.4), las 5 de `salud` primero

Criterio A.4 aplicado verbatim y uniforme, el mismo de N5: una regla es
`EXISTE-SATISFACE` sólo si la fuente trae **el desenlace que la regla
predice Y el disparador que la condiciona**, en **la unidad de análisis de
la regla**. Si sólo aparece uno, o la unidad no corresponde, es
`EXISTE-NO-SATISFACE` con lo que falta escrito. Si ninguna fuente
administrativa toca ninguno de los dos términos, es `NO-APLICA`.

### `salud` (§3.4) — 5 reglas · **0 `EXISTE-SATISFACE`**

| regla | fuente(s) examinadas | desenlace | disparador | unidad | A.4 |
|---|---|---|---|---|---|
| `salud.adherencia.desabasto_vs_cuidadora` | **Cero Desabasto** (base histórica) + **MACU** | **NO.** El desenlace es *abandono o intermitencia del tratamiento crónico* de un paciente. Cero Desabasto registra **el reporte de que faltó el insumo**, no si el paciente abandonó. Nadie sigue al paciente | **SÍ, y bien.** `desabasto` medido con registro individual: 7 914 reportes, fecha, padecimiento, institución, entidad, CLUES, 2019-2024. La segunda mitad («familia cuidadora») sólo como **indicador territorial** MACU, a nivel municipio | reporte×insumo (Cero Desabasto) y municipio (MACU) vs. **persona** | **EXISTE-NO-SATISFACE** — *falta el desenlace entero* |
| `salud.atencion.leve_sin_imss` | **DGIS Urgencias** (descriptores + catálogos CLUES) | **parcial y sesgado.** DGIS registra sólo a quien **sí** acudió a urgencias públicas. La rama que la regla predice —farmacia con consultorio o automedicación— **no genera registro administrativo alguno**: el brazo de interés es invisible por construcción, y no hay denominador poblacional | `segsoc` plausiblemente presente como derechohabiencia; gravedad plausiblemente en el motivo de urgencia. **Ninguno de los dos confirmable por `usado_para`** | evento de urgencia vs. **persona** | **EXISTE-NO-SATISFACE** — *falta el brazo no atendido y el denominador*; ver `CAND-1` |
| `salud.atencion.grave` | **DGIS Urgencias** | mismo sesgo de selección: todos los registrados ya fueron al sistema público, así que el contraste público/privado que la regla predice no se puede leer | gravedad plausible en motivo de urgencia, no confirmable por metadato | evento vs. persona | **EXISTE-NO-SATISFACE** *(la regla ya es `EXISTE-SATISFACE` por encuesta — N5; lo administrativo no añade)* |
| `salud.prevencion.hombre_sin_permiso` | — | ninguna fuente administrativa registra *posponer un chequeo* | ninguna registra *permiso laboral* | — | **NO-APLICA** |
| `salud.consumo.sellos_precio_similar` | — | ninguna registra elección de producto con sellos | ninguna registra etiquetado frontal ni precio relativo | — | **NO-APLICA** |

**Lo que este bloque sí cambia, y es el único cambio de estatus del acto:**
`salud.adherencia.desabasto_vs_cuidadora` estaba en **`NO-ENCONTRADO`**
en N5 (`0/241 591` en dos formulaciones dirigidas: ni abandono de
tratamiento ni surtido de receta existen como reactivo de encuesta). Con
las fuentes administrativas registradas **sube a `EXISTE-NO-SATISFACE`**:
el disparador que N5 no encontró **sí existe en el corpus**, con registro
individual, fecha y CLUES. Sigue sin llegar a `EXISTE-SATISFACE` porque
falta el desenlace, y **el conteo del criterio 2 no se mueve** — pero deja
de ser cierto que el corpus no toca esta regla.

### `cooperación` (§3.8) — 4 reglas · **0 `EXISTE-SATISFACE`**

| regla | fuente(s) | veredicto A.4 |
|---|---|---|
| `cooperacion.comite.monitoreo_sancion_visible` | **CNGMD** `m2_participa_ciudadana`, `m2_ctrl_inter_anticorr`, `m2_marco_regulatorio` | **EXISTE-NO-SATISFACE.** El **disparador institucional** —existencia de comité, de control interno, de mecanismo de sanción— es exactamente lo que un censo de gobiernos municipales levanta, y a nivel municipio se puede leer. El **desenlace es la contribución del individuo bajo monitoreo**, y ningún censo de gobiernos la registra. Es el mismo hueco que N5 midió por encuesta desde el otro lado (16 aciertos de membresía, `0/241 591` de monitoreo y sanción): ahora **hay disparador sin desenlace**, antes había desenlace sin disparador, y **los dos no son de la misma unidad de análisis**, así que no se suman. Ver `CAND-2` |
| `cooperacion.faena.sancion_social_pueblo_mestizo` | **CNGMD** `m2_marco_regulatorio`, `m2_participa_ciudadana` | **EXISTE-NO-SATISFACE.** Si el CNGMD codifica cooperación vecinal normada u obligación de faena en el marco regulatorio municipal, el disparador quedaría medido a nivel municipio; el desenlace (participa o no esta persona) no existe administrativamente. Que lo codifique **no se puede confirmar por `usado_para`** → `CAND-3` |
| `cooperacion.tanda.conoce_organizadora` | — | **NO-APLICA.** La tanda es informal por definición: no deja registro administrativo |
| `cooperacion.confianza.puente_personal` | — | **NO-APLICA.** El puente personal no es objeto de registro administrativo |

### `comunicación` (§3.10) — 4 reglas · **0 `EXISTE-SATISFACE`**

| regla | fuente(s) | veredicto A.4 |
|---|---|---|
| `comunicacion.inseguridad.ver_oir_callar` | **CNGMD** `m3` seguridad pública, `m5` justicia cívica | **EXISTE-NO-SATISFACE.** El CNGMD registra denuncias y procedimientos **que ocurrieron**, por municipio. La regla predice el **silencio** — la no-denuncia — y un registro de denuncias **no tiene denominador de testigos**: el evento que la regla predice es precisamente el que no genera registro. Mismo defecto de selección que DGIS en `salud`, por el lado opuesto |
| `comunicacion.rechazo.indirecto_face` | — | **NO-APLICA** |
| `comunicacion.retroalimentacion.privada_publica_capital_social` | — | **NO-APLICA** |
| `comunicacion.directividad.regional_generacional` | — | **NO-APLICA** |

### `información` (§3.9) — 4 reglas · **0 `EXISTE-SATISFACE`**

| regla | fuente(s) | veredicto A.4 |
|---|---|---|
| `informacion.deferencia.costo_acceso_experto` | **DGIS** catálogos **CLUES** | **EXISTE-NO-SATISFACE.** CLUES da la **oferta territorial de establecimientos** — un proxy defendible del *costo de acceso al experto*, que la enmienda `D-04` vuelve **la** prueba de esta regla, y que N5 no encontró en ninguna encuesta. El desenlace (a quién le cree y a quién consulta esta persona) no existe administrativamente. Disparador proxy sin desenlace |
| `salud.vacunacion.disponible` *(id con dominio equivocado; regla de §3.9)* | — | **NO-APLICA.** El corpus no trae registro administrativo de vacunación *(la regla ya es `EXISTE-SATISFACE` por encuesta — N5)* |
| `informacion.credibilidad.allegado_confianza` | — | **NO-APLICA** |
| `informacion.escuela.miedo_a_caer_clase_media` | — | **NO-APLICA** |

### `trabajo` (§3.2) — 4 reglas · **0 `EXISTE-SATISFACE`**

| regla | fuente(s) | veredicto A.4 |
|---|---|---|
| `trabajo.prestaciones.formalidad_pesa_mas_que_salario` | **CNGMD** `m2_rec_huma`, `m2_admi_rh_cap` | **EXISTE-NO-SATISFACE.** El CNGMD levanta plantilla y condiciones del **personal del gobierno municipal**. Aun tomándolo como muestra de trabajadores, el desenlace de la regla es una **preferencia comparada** («pesan más que el salario nominal») y una preferencia no se registra administrativamente — es el mismo hueco que N5 midió por encuesta. Además la unidad es el gobierno municipal, no el trabajador |
| `trabajo.jerarquia.deferencia_iniciativa_suprimida` | — | **NO-APLICA** |
| `trabajo.liderazgo.benevolencia_legitima` | — | **NO-APLICA** |
| `trabajo.rotacion.joven_urbano_sin_culpa` | — | **NO-APLICA** |

### `tiempo` (§3.6) — 4 reglas · **0 `EXISTE-SATISFACE`**

| regla | fuente(s) | veredicto A.4 |
|---|---|---|
| `tiempo.bomberazo.recursos_escasos_urgencias` | **DGIS Urgencias** — **homonimia, declarada** | **NO-APLICA.** El `id` de la regla dice `urgencias` y hay un programa llamado *Base de Datos de Urgencias*, pero **no son la misma cosa**: la regla habla de *urgencias compitiendo* en la vida cotidiana de una persona con recursos escasos; DGIS registra **atenciones en el servicio de urgencias hospitalario**. Ni desenlace ni disparador. Misma clase de falso positivo que los `jefe de hogar` y el `Retrasar un embarazo` que N5 descartó a mano |
| `tiempo.puntualidad.formal_vs_social` | — | **NO-APLICA** |
| `tiempo.compromiso.si_voy_incierto` | — | **NO-APLICA** |
| `tiempo.cumplimiento.recordatorio_baja_barrera` | — | **NO-APLICA** |

**SICEE / INE cómputos locales (65 entradas) y CompraNet (2) no producen
ningún par con las 25**, y se dice en vez de omitirse: su unidad es la
casilla/sección/municipio y el contrato, y ninguno de los seis dominios
candidatos de Ola 6 es electoral ni de contratación. La regla cívica que sí
los usa (`civico.participacion.contingente`, `ADR-284`) **no es de Ola 6**:
está en el acumulador de Ola 5.

---

## §3 · Lo que quedó `CANDIDATO-ABRIR-EN-CAJA` (no promovido)

Tres preguntas cuyo veredicto **no se puede cerrar sin abrir bytes**. Se
declaran; **ninguna se cuenta a favor de ninguna regla**:

- **`CAND-1` · DGIS Urgencias.** ¿Los descriptores 2008-2017 / 2018 / 2019 /
  2023-2025 traen **derechohabiencia** y **graduación de severidad** entre
  sus variables? Si sí, `salud.atencion.leve_sin_imss` y `.grave` tendrían
  disparador administrativo medido. **No cambiaría el veredicto de ninguna
  de las dos**: el sesgo de selección (sólo aparece quien acudió) y la falta
  de denominador poblacional son independientes de esa respuesta. Resolver
  sólo si se diseña un uso propio de DGIS.
- **`CAND-2` · CNGMD `m2_participa_ciudadana` + `m2_ctrl_inter_anticorr`.**
  ¿Codifican **monitoreo** y **sanción** como atributos del comité, o sólo
  su existencia? Decide si `cooperacion.comite.monitoreo_sancion_visible`
  tiene disparador institucional medido a nivel municipio — que es lo que
  haría viable un diseño multinivel, no un `EXISTE-SATISFACE`.
- **`CAND-3` · CNGMD `m2_marco_regulatorio`.** ¿Codifica cooperación
  vecinal normada / faena / obligación de contribuir a obra?

Sucesor si mesa lo quiere: `L15 · ABRE-ADMINISTRATIVAS-SALUD` (caja).

---

## §4 · P3 · Recuento corregido del criterio 2, dos columnas

Criterio 2 de `canon/motor-nucleo-medible-v1_0.md` §3.a, **tal como está
escrito** (`ADR-265`, firma 9 de mesa), sin relajar ni reinterpretar:
«≥2 encuestas en corpus **y** ≥3 reglas candidatas `EXISTE-SATISFACE`».

| dominio | reglas | (ii) `EXISTE-SATISFACE` **sólo encuestas** (N5, sin cambio) | (ii) `EXISTE-SATISFACE` **encuestas + administrativas** (este acto) | criterio 2 (ii) ≥3 |
|---|---|---|---|---|
| `trabajo` | 4 | 0 | **0** | NO-CUMPLE |
| `salud` | 5 | 1 | **1** | NO-CUMPLE |
| `tiempo` | 4 | 0 | **0** | NO-CUMPLE |
| `cooperación` | 4 | 0 | **0** | NO-CUMPLE |
| `información` | 4 | 1 | **1** | NO-CUMPLE |
| `comunicación` | 4 | 0 | **0** | NO-CUMPLE |
| **total** | **25** | **2** | **2** | **0 de 6 dominios** |

**Ninguna columna llega a 3 en ningún dominio. Ningún dominio queda
`ABRE-CANDIDATO-CON-RESERVA`. Ningún dominio abre. No se redacta ningún
lote `REGLAS-OLA6-*`.**

Composición de la columna administrativa, para que el `0` sea legible y no
una cifra pelada: de los 25 pares, **0 `EXISTE-SATISFACE` · 7
`EXISTE-NO-SATISFACE` · 18 `NO-APLICA`**. Las 7 que no son `NO-APLICA` son
las que arriba tienen fuente nombrada.

**Sobre (i) — ≥2 encuestas en corpus — este acto no se pronuncia**, porque
el encargo declara no tocarlo y porque la pregunta de si una fuente
administrativa cuenta para (i) o (ii) es de mesa (`P4.1`).

---

## §5 · El patrón, que vale más que el `0`

N5 dejó escrito que **10 de las 23 reglas que no llegan fallan por el mismo
lado**: el corpus mide el **desenlace** y no el **disparador**. Este acto
mide el cruce complementario, y encuentra que las fuentes administrativas
fallan por **el lado contrario y por una razón distinta**:

1. **De las 7 reglas donde una fuente administrativa toca algo, 5 aportan
   disparador y ninguna aporta desenlace** (desabasto sin adherencia,
   comité sin contribución, CLUES sin deferencia, marco regulatorio sin
   participación, prestaciones municipales sin preferencia). El registro
   administrativo mide **la estructura de la que la regla condiciona**, no
   **la conducta que la regla predice**. Es simétrico y no casual: un
   registro administrativo existe porque un programa opera, y los programas
   registran su propia operación, no la decisión del ciudadano.
2. **Las 2 restantes fallan por sesgo de selección, no por ausencia**
   (`leve_sin_imss` y `ver_oir_callar`): el registro **sólo contiene el
   brazo que actuó** —quien fue a urgencias, quien denunció— y la regla
   predice justamente la rama que no genera registro. Adquirir más de esos
   payloads no lo arregla; el brazo faltante no existe en ningún registro
   administrativo posible.
3. **Ninguno de los 25 pares comparte unidad de análisis con su regla.** Las
   fuentes son de establecimiento, municipio, evento o contrato; las reglas
   son de persona. Esto **no es un veredicto sobre las fuentes** —son buenas
   para lo que fueron adquiridas, y `ADR-284` las usó bien para una regla
   cívica municipal— sino sobre **este cruce**: reglas de conducta
   individual contra registros de operación institucional.

**Consecuencia que dirección debe pesar y este acto no decide.** Sumando lo
de N5 y lo de aquí, el criterio 2 tiene ahora dos negativos de naturaleza
distinta y ninguno se arregla comprando más dato del mismo tipo: por
encuesta faltan **instrumentos** (percepción y vínculo, que INEGI no
levanta); por administrativo falta **la unidad de análisis** (persona) y
**el brazo no seleccionado**. Eso es lo que va a mesa como `P4.2`.

---

## §6 · Lo que este acto NO hace

No abre ningún dominio · no relaja ni reescribe ningún criterio · no abre
bytes · no edita `.claude/commands/mapea.md` · no borra ni corrige in situ
ninguna frase de N5 (todo es append) · no lanza lotes `L1` · no toca
`milpa/**`, `data/**` ni `forense/prereg-duelo-v2/**`.
