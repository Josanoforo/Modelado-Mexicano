# Cobertura completa de Ola 6 — mapa de dominio y plan por regla

`ACTO MAESTRA38-N10 · COBERTURA-COMPLETA-OLA6`. Corrida 5/sep/2026, entorno
**NUBE**, contra `origin/main = 25383f35`. Encargo archivado en
`forense/encargos/2026-09-05-MAESTRA38-N10-COBERTURA-COMPLETA-OLA6.md`.
COMPUERTA `N9 fusionado` verificada por producto: `test -f tools/ya_medido.py`
contra `origin/main` → existe (`9e767a8`, `PR #538`).

**Mandato de mesa, verbatim (4/sep/2026):** «Entiendo que hay un mínimo y ese
mínimo para lanzar una ola es una cosa. Pero hoy no tenemos lo mínimo y no
quiero hacerlo al mínimo no después de haber invertido tanto en la
infraestructura que creamos.» Este acto no busca el mínimo que abre un
dominio: busca el mapa completo de las 25 reglas de los 6 dominios candidatos
y el plan para cubrirlas todas. El criterio 2 de `motor-nucleo-medible-v1_0.md`
§3.a se reporta abajo como consecuencia — no se relaja, no se reinterpreta, no
se optimiza para que pase.

**Resumen ejecutivo (5 líneas).** De 25 reglas: **3 `MEDIBLE-COMO-ESTÁ`**,
**3 `CON-CANDIDATA`**, **19 `HIPÓTESIS-SIN-INSTRUMENTO`**, **0 sin ruta**. Con
lo medible hoy, el criterio 2 (`≥3 EXISTE-SATISFACE` por dominio) da **0 de 6**
— igual que `MAESTRA34-N5`/`MAESTRA36-N6`. Con lo medible **más** las 3
adquisiciones ya identificadas con ficha, **sigue en 0 de 6**: ningún dominio
llega a 3 aun agotando todo lo que hoy se puede nombrar. Pese a eso, **los 6
dominios se declaran `COMPLETABLE`**: las 25 reglas, sin excepción, tienen una
ruta escrita — medir hoy, adquirir con ficha, o diseñar el instrumento mínimo
de la hipótesis. Lo que falta no es mapa: es **fieldwork** (instrumentos
nuevos) y **tiempo de caja** (abrir 3 fuentes administrativas ya identificadas).

---

## 1 · COMMIT-1 · Universo y criterio

### 1.1 · Universo, derivado por comando y congelado

```
$ sed -n '508,514p;524,531p;541,547p;562,569p;571,577p;579,588p' canon/modelo-decision-v4_0.md \
  | grep -c '^\- \*\*SI\*\*'
25
```

Verificado dos veces por mecanismos independientes: (1) conteo de bullets
`- **SI**` dentro del rango de línea de cada sección (`§3.2` 508-514, `§3.4`
524-531, `§3.6` 541-547, `§3.8` 562-569, `§3.9` 571-577, `§3.10` 579-588) →
**4+5+4+4+4+4 = 25**; (2) el `REGISTRO` congelado de
`tests/validador_registro_ids.py` (Hito D, 29/jul/2026) trae exactamente 4
`R2.*`, 5 `R4.*`, 4 `R6.*`, 4 `R8.*`, 4 `R9.*`, 4 `R10.*` — **25** filas para
estas seis secciones, cero huecos, cero duplicados. El encargo estimaba
«~30»; **el real es 25 — se declara, no se fuerza a 30.**

Una fila del universo (`salud.vacunacion.disponible`, `R9.2`) trae dominio
equivocado en su propio `id` (`salud.*` en una regla de `§3.9`, no `§3.4`) —
anomalía ya declarada por el propio canon y por `forense/hallazgos.md`, **no
se corrige aquí** (fuera de perímetro: `canon/modelo-decision-v4_0.md` no se
toca salvo ADR). Se cuenta en `§3.9` (su sección real), no en `§3.4`.

### 1.2 · Criterio de clasificación — cerrado, cita el precedente de la casa

Mismo vocabulario que `MAESTRA38-N5` §1.3 (`REFORMULABLE`/`SIN-INSTRUMENTO`/
`CON-CANDIDATA`), con una categoría más que ese acto no necesitaba porque sus
9 reglas ya venían todas sin `EXISTE-SATISFACE`: aquí `MAESTRA34-N5` ya había
encontrado 2 `EXISTE-SATISFACE`, así que el universo de N10 necesita nombrar
también ese caso.

- **MEDIBLE-COMO-ESTÁ** — antecedente y desenlace de la regla están medidos
  **en la misma persona, en el mismo instrumento** del corpus. Traducción al
  vocabulario `EXISTE-SATISFACE` de `MAESTRA34-N5`/`MAESTRA36-N6`, con un
  requisito más estricto (*misma persona, mismo instrumento*, no solo *ambos
  términos aparecen en el corpus*) — declarado así porque el encargo lo pide
  explícito y porque las dos filas que califican (ver `§2.2`, `§2.5`) lo
  cumplen de sobra.
- **REFORMULABLE** *(N5 §1.3.a)* — existe un reactivo que mide el mismo
  *driver* con otro desenlace observable, o el mismo desenlace con otro
  encuadre del *driver*: el objeto se reescribe para anclarse a lo que el
  reactivo realmente mide, **conservando driver y signo, cambiando una sola
  cosa** — sin inventar dato. Precedente de la casa, citado y no repetido:
  `civico.voto.clientelar_si_observable` → `..._lapop2019` y
  `civico.protesta.agravio_urbano` → `..._multiola` (`MAESTRA38-N5` §2.6/§2.8,
  cargadas por `MAESTRA38-N6`/`FP-298` como «tercera formulación
  complementaria» — ninguna de las dos pertenece al universo de Ola 6, se
  citan solo como método, **no se reclasifican aquí**).
- **CON-CANDIDATA** *(N5 §1.3.c)* — existe una fuente nombrada y conocida
  (encuesta o administrativa) que podría resolver el objeto, identificada
  **dentro** del corpus o el manifiesto pero pendiente de adquisición, de
  lectura completa, o de abrir bytes para confirmar alcance — el caso de
  referencia es `N34`/ENCRIGE (`MAESTRA38-N5` §2.3-2.4).
- **HIPÓTESIS-SIN-INSTRUMENTO** *(N5 §1.3.b)* — ningún instrumento nacional
  mide hoy la condición que la regla exige; se escribe el instrumento mínimo
  (una pregunta, una población).

**Regla de honestidad (c), verbatim del encargo, aplicada literalmente en las
25:** si conservar el *driver* exige un reactivo que no existe, no es
`REFORMULABLE` aunque haya algo parecido. Ruido de substring no cuenta (N5
§2.0) — un acierto de `busca_reactivos.py` que solo coincide por texto sin
relación conceptual con el mecanismo de la regla se declara ruido y el
veredicto cae a `HIPÓTESIS-SIN-INSTRUMENTO` o `CON-CANDIDATA` según
corresponda. Esta nota descarta explícitamente, regla por regla, cada acierto
que resultó ser ruido — no se omite el intento fallido (ver detalle por
dominio).

### 1.3 · `tools/ya_medido.py`, corrido para las 25 ANTES de clasificar

```
$ for id in trabajo.jerarquia.deferencia_iniciativa_suprimida trabajo.liderazgo.benevolencia_legitima \
    trabajo.prestaciones.formalidad_pesa_mas_que_salario trabajo.rotacion.joven_urbano_sin_culpa \
    salud.atencion.leve_sin_imss salud.atencion.grave salud.prevencion.hombre_sin_permiso \
    salud.adherencia.desabasto_vs_cuidadora salud.consumo.sellos_precio_similar \
    tiempo.puntualidad.formal_vs_social tiempo.compromiso.si_voy_incierto \
    tiempo.bomberazo.recursos_escasos_urgencias tiempo.cumplimiento.recordatorio_baja_barrera \
    cooperacion.comite.monitoreo_sancion_visible cooperacion.tanda.conoce_organizadora \
    cooperacion.confianza.puente_personal cooperacion.faena.sancion_social_pueblo_mestizo \
    informacion.credibilidad.allegado_confianza informacion.deferencia.costo_acceso_experto \
    salud.vacunacion.disponible informacion.escuela.miedo_a_caer_clase_media \
    comunicacion.rechazo.indirecto_face comunicacion.retroalimentacion.privada_publica_capital_social \
    comunicacion.inseguridad.ver_oir_callar comunicacion.directividad.regional_generacional; do
  python3 tools/ya_medido.py "$id" | tail -1
done
```

**Salida: `NUNCA-MEDIDA` en las 25, sin excepción.** Consistente con lo que
`MAESTRA34-N5`/`MAESTRA36-N6` ya habían dejado escrito (criterio 1 y criterio
2 evaluados, cero medición real corrida sobre Ola 6): las cinco fuentes que
`ya_medido.py` cruza (`milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.
yaml`, `canon/modelo-decision-v4_0.md` §7, `forense/notas/*-L*-*.md`,
`forense/prereg-caja/S*-spec-*.md`) no traen ninguna falsación real sobre
ninguna de las 25 — ni siquiera las 2 que `MAESTRA34-N5` ya había encontrado
`EXISTE-SATISFACE` por reactivo. **No hay discrepancia que declarar contra
`ya_medido.py`** en esta pieza (ver `§5 · Hallazgos`): `MAESTRA34-N5`/
`MAESTRA36-N6` nunca afirmaron que hubiera medición corrida — afirmaron
existencia de reactivo, una pregunta distinta, y las dos lecturas coinciden.

### 1.4 · Tercer insumo que `MAESTRA34-N5`/`MAESTRA36-N6` no tenían asignado

`MAESTRA34-N5` buscó en `inventario-reactivos-v1_2.tsv` + `-ext-v1_0.tsv`
(241 591 filas, encuestas). `MAESTRA36-N6` cruzó `data/manifiesto.yaml`
(1 104 entradas, fuentes administrativas). **Ninguno de los dos acto corrió
`busca_reactivos.py --tablas descargas_mx_v1_1`** (42 548 filas, 42 536
examinadas — universo que el propio encargo de N10 nombra) — la tabla que
`MAESTRA38-N5` sí usó, en otro dominio, y que trae `LAPOP AmericasBarometer`
(2004/2006/2019/2021/2023), `World Values Survey` (ola 7), `ENSANUT 2024`
crudo, y paneles `AEJ`/Compartamos (`round2_mexico_anon.dta`,
`round5_mexiconew_anon.dta`) que **no están indexados** en `v1_2`/`ext`. Este
acto corre esa tercera pasada, regla por regla — **75 corridas** (3
formulaciones × 25 reglas, reusando literalmente las formulaciones ya
diseñadas por `MAESTRA34-N5` para cada regla, contra la tabla nueva, sin
inventar vocabulario de búsqueda nuevo). Comandos y salidas crudas:
`/tmp/claude-0/…/scratchpad/busca_v11/{trabajo,salud,tiempo,cooperacion,
informacion,comunicacion}.txt` (efímero de sesión, no versionado — cada
comando se reproduce con la línea citada en cada regla de abajo).

---

## 2 · COMMIT-2 · Clasificación con evidencia, por dominio

Convención de columnas en las seis tablas: **id** (regla) · **R-n** (canon,
registro congelado) · **tier** · **antecedente** (resumido; verbatim completo
en `canon/modelo-decision-v4_0.md` §3, línea citada) · **desenlace**
(resumido) · **`ya_medido.py`** · **clasificación N10**.

### 2.1 · `trabajo` (§3.2, líneas 510-513) — 4 reglas, **0 medibles, 0 con-candidata, 4 hipótesis**

| id | R-n | tier | antecedente | desenlace | `ya_medido.py` | clasificación |
|---|---|---|---|---|---|---|
| `trabajo.jerarquia.deferencia_iniciativa_suprimida` | R2.1 | `[FUERTE]` | jerarquía tradicional/empresa familiar (`segsoc`=2 ∧ `tam_loc`∈{3,4}) | deferencia hacia arriba, iniciativa suprimida, "sí" que significa "probablemente" | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `trabajo.liderazgo.benevolencia_legitima` | R2.2 | `[MEDIA-FUERTE]` | liderazgo benévolo (provee/protege/cuida) vs. autoritario no-benévolo | lealtad/satisfacción altas vs. peor desempeño | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `trabajo.prestaciones.formalidad_pesa_mas_que_salario` | R2.3 | `[MEDIA]` | prestaciones formales (IMSS, Infonavit) | pesan más que el salario nominal (preferencia comparada) | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `trabajo.rotacion.joven_urbano_sin_culpa` | R2.4 | `[MEDIA]` | trabajador joven urbano (15-29, `tam_loc`=1) | cambia de empleo sin culpa, exige justificación de decisiones | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |

**`deferencia_iniciativa_suprimida`.** `MAESTRA34-N5`: `NO-ENCONTRADO` — los
80 aciertos de `jefe` en `v1_2`/`ext` son `jefe de hogar` (composición del
hogar), 0/241 591 en `iniciativa`/`contradecir`. `MAESTRA36-N6`
(administrativo): `NO-APLICA`. **v1_1 (este acto):** `--regex "jefe|superior
jerarquic|obedec"` → **32/42 536**, inspeccionados los 32: `jefe de hogar`/
`jefe de familia` (ENNVIH `round5_mexiconew_anon.dta` `rhparen`/`h3_*`,
`basehogaresmicro_anon.dta` `h3_*`), satisfacción con la delegación/alcaldía
(LAPOP `st4`, no jefe laboral), `ENSANUT2024` parentesco con el jefe del
hogar. **Ninguno mide jerarquía laboral ni obediencia a un superior — ruido
de substring, descartado por §1.3.c.** `iniciativa`/`contradecir`: 0/42 536.
**Instrumento mínimo:** a trabajador dependiente, "cuando no está de acuerdo
con una decisión de su jefe/superior directo, ¿se lo dice o prefiere no
contradecirlo?" + "¿ha propuesto alguna vez un cambio o idea en su trabajo?",
población ocupada asalariada.

**`benevolencia_legitima`.** N5: `NO-ENCONTRADO` (jefe-trata/apoya 0,
satisfacción laboral 0; los 4 de "trato-jefe" son "PATRON/CONTRATO" como
fuente de pago de un viaje, `mt18_1d`/`mg29_1d`). N6: `NO-APLICA`. v1_1: 0/0/0
en las tres formulaciones. **Instrumento mínimo:** "¿su jefe/patrón lo trata
con respeto y se preocupa por sus empleados, o es autoritario y no se
preocupa?" + satisfacción laboral / intención de permanencia, población
ocupada.

**`formalidad_pesa_mas_que_salario`.** N5: `EXISTE-NO-SATISFACE` — el
*driver* sí está medido y bien (`aguinaldo`/`prestacion` en ENIGH 2012-2022,
`imssissste` en ENOE); el desenlace («pesan más que el salario nominal») es
preferencia comparada, ningún reactivo la pide. N6 (administrativo):
`EXISTE-NO-SATISFACE` — CNGMD levanta prestaciones del personal *municipal*
(`m2_rec_huma`), unidad de análisis equivocada (gobierno, no trabajador) y la
misma preferencia sin medir. v1_1 (este acto, tres intentos de reformulación
dirigidos a un desenlace conductual disponible): `--regex
"important\w+.{0,30}(prestacion|salario)|prefer\w+..."` → 0 · `--regex
"antiguedad.{0,20}(empleo|trabajo|puesto)|permanenci\w+..."` → 0 · `--regex
"(razon|motivo).{0,20}(elegi|acepto|prefirio)..."` → 0. **Los tres intentos
de reformulación honesta fallan — no hay reactivo, ni para la preferencia
declarada ni para un proxy conductual (antigüedad, razón de elección del
empleo). Por la regla de honestidad (c), esto NO es `REFORMULABLE` aunque el
*driver* esté medido: cae a `HIPÓTESIS-SIN-INSTRUMENTO`.** Es la más barata
de diseñar de las 4 del dominio — solo falta el desenlace, el *driver* ya
tiene instrumento.

**`rotacion_joven_urbano_sin_culpa`.** N5: `NO-ENCONTRADO` — los 35 aciertos
de "por qué dejó" son `POR QUE DEJO DE AMAMANTAR` (`he51_1a`..`he51_1f`,
ENNVIH, homonimia); cambio de empleo y búsqueda de otro: 0/241 591 cada una.
N6: `NO-APLICA`. v1_1: 0/0/0 en las tres. **Instrumento mínimo:** a joven
urbano ocupado, "en los últimos 12 meses ¿cambió de empleo? ¿sintió que tenía
que justificarlo o dar explicaciones a su familia/entorno?", población 15-29
urbana ocupada.

**Plan de cobertura, `trabajo`.** (i) medibles hoy: **0**. (ii)
adquisiciones con ficha: **0** — ninguna fuente nombrada (encuesta o
administrativa) toca ninguna de las 4, ni por *driver* ni por desenlace, más
allá de lo ya declarado ruido. (iii) hipótesis declaradas, instrumento
mínimo escrito: **4/4**. (iv) criterio 2: con (i) **0 de 4**; con (i)+(ii)
**0 de 4** (no hay (ii) que sumar). **Veredicto: `COMPLETABLE`** — las 4
tienen ruta (diseño de instrumento), aunque ninguna es medible ni adquirible
hoy.

### 2.2 · `salud` (§3.4, líneas 526-530) — 5 reglas, **1 medible, 1 con-candidata, 3 hipótesis**

| id | R-n | tier | antecedente | desenlace | `ya_medido.py` | clasificación |
|---|---|---|---|---|---|---|
| `salud.atencion.leve_sin_imss` | R4.1 | `[FUERTE]` | padecimiento leve-moderado, sin IMSS (`segsoc`=2) | farmacia con consultorio o automedicación | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `salud.atencion.grave` | R4.4 | `[MEDIA]` | síntoma grave o crónico complejo | busca sistema público pese a la espera | NUNCA-MEDIDA | **MEDIBLE-COMO-ESTÁ** *(propuesta)* |
| `salud.prevencion.hombre_sin_permiso` | R4.2 | `[FUERTE]` | hombre trabajador sin permiso laboral | pospone el chequeo hasta síntoma grave | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `salud.adherencia.desabasto_vs_cuidadora` | R4.3 | `[FUERTE / MEDIA]` | desabasto + gasto de bolsillo alto vs. familia cuidadora + medicamento surtido | abandono/intermitencia vs. mayor adherencia | NUNCA-MEDIDA | **CON-CANDIDATA** |
| `salud.consumo.sellos_precio_similar` | R4.5 | `[MEDIA]` | producto con sellos, alternativa de precio similar | elige el de menos sellos (vs. compra igual si no hay sustituto) | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |

**`atencion.leve_sin_imss`.** N5: `EXISTE-NO-SATISFACE` — desenlace medido
(`ce04l`/`cen04l`/`ce05l CONSULTA FARMACIA`, ENNVIH, `en_corpus=SI`) y
*driver* de aseguramiento medido (`imssissste`, ENOE), pero **falta el
tercer término, que es antecedente, no adorno: "leve-moderado"** — ningún
reactivo grada severidad hacia abajo; `automedic*` es 0/241 591. N6
(administrativo): `EXISTE-NO-SATISFACE` con sesgo de selección — DGIS
Urgencias solo registra a quien **sí** acudió a urgencias públicas; la rama
que la regla predice (farmacia/automedicación) es invisible por construcción,
`CAND-1` (¿DGIS trae derechohabiencia y severidad?) **no rescataría la regla
aunque se confirmara** — el sesgo de selección es independiente de esa
respuesta, N6 lo declara explícito. v1_1 (este acto): `farmacia` 0/42 536 ·
`automedic` 0/42 536 · "dónde se atendió" → 2/42 536, inspeccionados:
`asq_cuid_hog_completa.dta` `P13_CU`/`P13e_1_CU` — encuesta de **cuidadores**
sobre la persona cuidada, no autorreporte, y sin gradación de severidad
(descartado, §1.3.c) · `grave|gravedad|severidad` → 10/42 536, inspeccionados:
todos son LAPOP "problema más grave del país" / "gravedad del cambio
climático" — homonimia de "grave" como adjetivo de opinión pública, no de
salud (descartado). **Sin instrumento que grade "leve-moderado" hacia abajo
en ninguna de las tres pasadas.** Instrumento mínimo: "la última vez que tuvo
un malestar que usted consideró leve o moderado, ¿a dónde acudió: farmacia
con consultorio, se automedicó, o fue a consulta médica formal?", población
sin seguridad social.

**`atencion.grave`.** N5: `EXISTE-SATISFACE` *(propuesta)* — "los dos
términos existen y son del mismo corpus": disparador `es09 HA TENIDO
PROBLEMA SALUD GRAVE` + `es09a` (ENNVIH, MxFLS, ventana de 4 años); desenlace
`cen10*` (ENNVIH, **mismo instrumento**, lugar de consulta) y, en segundo
instrumento, `p6_15_8_*`/`p6_17_8` (ENDIREH 2016, público vs. privado). Bajo
el criterio más estricto de este acto (misma persona, mismo instrumento):
**`es09`+`cen10*` en ENNVIH satisface `MEDIBLE-COMO-ESTÁ` sin necesitar el
segundo instrumento** — se cita ENDIREH como corroboración, no como
requisito. N6 (administrativo): `EXISTE-NO-SATISFACE` (DGIS con el mismo
sesgo de selección que arriba) — *no cambia el veredicto*, que ya viene
satisfecho por encuesta. v1_1 (este acto): `imss|issste|hospital` → 26/42 536
(IMSS-BIENESTAR conocimiento/registro en ENSANUT2024, Seguro Popular en
`asq_cuid_hog_completa`, registro patronal de negocios ante IMSS — ninguno es
"a dónde acudió por un problema grave", confirma que no hay mejor instrumento
que ENNVIH, no lo desplaza) · `grave|gravedad|severidad` → 10/42 536 (mismo
ruido LAPOP de arriba). **El PORQUE de la regla ("pese a la espera") es
mecanismo, no antecedente — no se exige medirlo, mismo criterio que N5 aplicó
aquí.** Se propone, **DIRECCIÓN revisa antes de sellar**.

**`prevencion.hombre_sin_permiso`.** N5: `EXISTE-NO-SATISFACE` — el desenlace
*positivo* existe (`ce13_1c`/`cen12_1c EXAMEN PREVENTIVO`) pero la regla
predice **posponer**, que es 0/241 591; el *driver* "sin permiso laboral" no
aparece (71 aciertos de "prestación" son montos de ingreso, no permiso). N6:
`NO-APLICA` (ninguna fuente administrativa registra posponer un chequeo ni
permiso laboral). v1_1: `chequeo/revisión/examen` → 3/42 536, inspeccionados:
`asq_cuid_hog_completa.dta P56_01_CU` ("¿lleva al niño a revisión médica?",
encuesta de cuidado infantil) y `adolescentes_ensanut2024_w.dta d0321d`
("durante el embarazo, ¿te realizaron examen general de orina?") — ninguno es
adulto varón posponiendo un chequeo propio (descartado, §1.3.c). "No
fue/pospuso" y "prestación" (permiso): 0/42 536. Instrumento mínimo: a hombre
ocupado, "en el último año, ¿pospuso un chequeo médico por no tener permiso
para faltar al trabajo?", población masculina ocupada.

**`adherencia.desabasto_vs_cuidadora`.** N5: `NO-ENCONTRADO` en `v1_2`/`ext`
— 0/241 591 en abandono de tratamiento y en surtido de receta; los 25 de
"farmacia" son lugar de consulta, no desabasto. **`MAESTRA36-N6` corrigió
esto con administrativo:** sube a `EXISTE-NO-SATISFACE` — el *driver*
(desabasto) **sí existe**, con registro individual: **Cero Desabasto**
(base histórica, 7 914 reportes distintos, 2019-02-18 a 2024-09-03, con
fecha, padecimiento, institución, entidad, `CLUES`) y **MACU/Observatorio de
Cuidados** (indicador territorial de "familia cuidadora", a nivel municipio).
Falta el desenlace (¿el paciente abandonó?) — nadie sigue al paciente. **Esto
ya está registrado como candidata, no es un hallazgo nuevo de este acto:**
`data/curacion-registro/utilidad-modelo.tsv` filas 203-205 ligan `N36`
(=`R4.3`) a Cero Desabasto y DGIS×2, estado **`CANDIDATA /
PENDIENTE_EVIDENCIA`** desde `ADR-279` (1/sep/2026), `N36` definida en
`data/curacion-registro/necesidad-objeto-modelo.tsv:41` (verificado por
`MAESTRA37-N1`/`ADR-319`, enmienda del 3/sep sobre la nota de reevaluación).
v1_1 (este acto): `dejó/abandonó/interrumpió tratamiento` → 0/42 536 ·
"surtió receta" → 0/42 536 · `farmacia` → 0/42 536. **Sin novedad de esta
tercera pasada — la ficha ya existente (`N36`) es la ruta.** Clasificación:
**`CON-CANDIDATA`**, cita la ficha ya registrada, no se re-abre.

**`consumo.sellos_precio_similar`.** N5: `NO-ENCONTRADO` — 0/241 591; el
etiquetado frontal (2020) no tiene reactivo, y la propia regla ya declara su
variable de hogar `PENDIENTE DE VERIFICACIÓN` (§1.6 del canon). N6:
`NO-APLICA`. v1_1: `sello/etiquetado` 0/42 536 · controles (`grave` 10,
`farmacia` 0, ambos ya explicados como ruido arriba, reusados aquí solo como
control negativo tal como N5 los diseñó). **Ausencia total, en las tres
pasadas y en dos vintages distintos de inventario.** Instrumento mínimo:
elección de producto con sellos de advertencia vs. alternativa de precio
similar, en punto de compra o recordado, hogares con y sin sustituto barato.

**Plan de cobertura, `salud`.** (i) medibles hoy: **1** (`atencion.grave`,
propuesta). (ii) adquisiciones con ficha: **1** (`adherencia.desabasto_vs_
cuidadora`, `N36`, ya en cola con estado `CANDIDATA/PENDIENTE_EVIDENCIA`).
(iii) hipótesis declaradas: **3** (`leve_sin_imss`, `hombre_sin_permiso`,
`sellos_precio_similar`). (iv) criterio 2: con (i) **1 de 5**; con (i)+(ii)
**2 de 5** — sube un peldaño, sigue sin llegar a 3. **Veredicto:
`COMPLETABLE`** — las 5 tienen ruta.

### 2.3 · `tiempo` (§3.6, líneas 543-546) — 4 reglas, **0 medibles, 0 con-candidata, 4 hipótesis**

| id | R-n | tier | antecedente | desenlace | `ya_medido.py` | clasificación |
|---|---|---|---|---|---|---|
| `tiempo.puntualidad.formal_vs_social` | R6.1 | `[MEDIA]` | cita formal-laboral con checador/sanción/dinero vs. social-familiar sin sanción | puntual (5-10 min antes) vs. hora aproximada | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `tiempo.compromiso.si_voy_incierto` | R6.2 | `[HIPÓTESIS]` (ya en canon) | invitación social, decir "no" sería descortés | dice "sí voy" aunque la asistencia sea incierta | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `tiempo.bomberazo.recursos_escasos_urgencias` | R6.3 | `[MEDIA]` | recursos escasos, urgencias compitiendo | pospone lo no urgente, improvisa el "bomberazo" | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `tiempo.cumplimiento.recordatorio_baja_barrera` | R6.4 | `[MEDIA]` | cita médica/trámite con costo por faltar | cumple más con recordatorio y baja barrera | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |

**Único dominio donde N5 ya declaró faltante real de dato** (`(i) ≥2
encuestas` **NO-CUMPLE**, 0 de 8 fuentes cerradas el 31/jul), no solo de
instrumento — confirmado de nuevo aquí.

**`puntualidad.formal_vs_social`.** N5: `NO-ENCONTRADO` — los 4 aciertos de
"retraso" son `Retrasar un embarazo` (EDER 2017, homonimia); `puntual*`/"llega
tarde" 0/241 591. N6: `NO-APLICA`. v1_1: `puntual/llega tarde/retraso` →
4/42 536, inspeccionados: `Padres 10 Follow-up3-Roster` (IEPEP/PROGRESA)
`PB55_1e`/`2e` "quejas por **impuntualidad de los maestros**" — es la
puntualidad de un tercero (docente) evaluada por el padre, no la conducta
propia del respondente en un encuadre formal/social (descartado, §1.3.c) ·
"posterg/pospon" → 0 · "recordatorio/mensaje cita" → 2/42 536, inspeccionados:
`rec24h_ensanut2024_w.dta fec_cap` "seleccionar fecha de recordatorio en el
calendario" — es un campo de **captura del entrevistador** para el recordatorio
dietético de 24 horas, no un reactivo sobre el respondente (descartado).
Instrumento mínimo: a la misma persona, dos escenarios (cita de trabajo con
checador vs. reunión social familiar) y el margen de tiempo declarado con el
que llega a cada una.

**`compromiso.si_voy_incierto`.** Ya `[HIPÓTESIS]` en el canon desde origen
— nunca tuvo pretensión de estar medida. N5: `NO-ENCONTRADO` (0/241 591 en
"cortesía"/"decir que no"). N6: `NO-APLICA`. v1_1: "cortés/quedar bien" →
6/42 536, inspeccionados: LAPOP `b1` "Cortes garantizan un juicio justo"
(homonimia "cortes"=tribunales, no cortesía) y `psc3_2`/`psc5` "cortes de
energía" (homonimia distinta) — cero relación con el mecanismo (descartado) ·
"decir que no/rechazar" → 0 · "puntual/llega tarde" → 4/42 536 (mismo ruido
de impuntualidad docente de arriba, reusado como control, descartado).
Instrumento mínimo: "cuando lo invitan a un evento social y no está seguro de
poder asistir, ¿suele decir que sí de todas formas para no quedar mal?" +
asistencia real registrada (para contrastar intención vs. conducta).

**`bomberazo.recursos_escasos_urgencias`.** N5: `NO-ENCONTRADO` — el único
acierto de "posterga" es una nota metodológica del propio INEGI sobre
captación, no un reactivo. N6: `NO-APLICA`, con homonimia declarada: DGIS
"Base de Datos de **Urgencias**" registra atenciones hospitalarias, no
"urgencias compitiendo" en la vida cotidiana — mismo patrón de falso positivo
que `jefe de hogar`. v1_1: "posterg/pospon" → 0 · "dejó/abandonó tratamiento"
→ 0 · "retraso" → 0. **Cero señal en las tres pasadas, sin excepción — el
faltante de dato más limpio del universo.** Instrumento mínimo: escala de
frecuencia de "improvisar/resolver de último momento" ante gastos o
urgencias competidoras, población de bajos ingresos.

**`cumplimiento.recordatorio_baja_barrera`.** N5: `NO-ENCONTRADO` — el
recordatorio es una intervención, el corpus es observacional: 0/241 591. N6:
`NO-APLICA`. v1_1: "recordatorio" → 2/42 536 (mismo campo de captura de
ENSANUT ya descartado arriba) · "no fue/pospuso" → 0 · "chequeo/revisión" →
1/42 536 (`asq_cuid_hog_completa P56_01_CU`, cuidado infantil, mismo ítem ya
descartado en `hombre_sin_permiso`). Instrumento mínimo: experimento o
pregunta retrospectiva sobre asistencia a cita con/sin recordatorio recibido,
población con costo por faltar.

**Plan de cobertura, `tiempo`.** (i) medibles hoy: **0**. (ii) adquisiciones
con ficha: **0** — no hay ninguna fuente nombrada, ni encuesta ni
administrativa, que toque ninguna de las 4. (iii) hipótesis declaradas:
**4/4**. (iv) criterio 2: 0 de 4, con o sin (ii). **Veredicto: `COMPLETABLE`**
— con la salvedad más fuerte de las seis: aquí no hay ni un solo hilo de
adquisición que tirar; las 4 rutas son, sin excepción, diseño de instrumento
nuevo desde cero.

### 2.4 · `cooperación` (§3.8, líneas 564-567) — 4 reglas, **0 medibles, 2 con-candidata, 2 hipótesis**

| id | R-n | tier | antecedente | desenlace | `ya_medido.py` | clasificación |
|---|---|---|---|---|---|---|
| `cooperacion.comite.monitoreo_sancion_visible` | R8.1 | `[FUERTE]` | comité con liderazgo confiable + monitoreo + sanción visible (vs. sin ninguno) | contribuye vs. free-riding racional | NUNCA-MEDIDA | **CON-CANDIDATA** |
| `cooperacion.tanda.conoce_organizadora` | R8.2 | `[FUERTE]` | conoce personalmente a la organizadora (vs. tanda de desconocidos) | entra a la tanda vs. evita por riesgo de fraude | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `cooperacion.confianza.puente_personal` | R8.3 | `[FUERTE]` | puente personal (conocido en común, correligionario, paisano) | confía en el desconocido vs. desconfía por defecto | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `cooperacion.faena.sancion_social_pueblo_mestizo` | R8.4 | `[MEDIA]` | pueblo mestizo con faena/cooperación normada y sanción vs. urbano sin sanción | participa (coerción normativa) vs. participación voluntaria baja | NUNCA-MEDIDA | **CON-CANDIDATA** |

**`comite.monitoreo_sancion_visible`.** N5: `EXISTE-NO-SATISFACE` — el único
`comite` en `v1_2`/`ext` es un agregado administrativo
(`comites_constituidos`), no reactivo de encuesta; los 16 aciertos son
pertenencia a organizaciones (ENCUP `P69_11`) — miden membresía, no
contribución bajo monitoreo, y ni monitoreo ni sanción aparecen (0/241 591).
**`MAESTRA36-N6` (administrativo) encontró el lado que faltaba:** CNGMD
`m2_participa_ciudadana`/`m2_ctrl_inter_anticorr`/`m2_marco_regulatorio`
levanta, a nivel **municipio**, la existencia de mecanismos de participación
y control interno — el *driver institucional* queda medido a esa unidad,
aunque el *desenlace* (contribución individual bajo monitoreo) sigue sin
registro. Es el cruce complementario exacto: encuesta mide desenlace sin
driver, administrativo mide driver sin desenlace, y **las dos unidades de
análisis no coinciden** (persona vs. municipio) — no se suman a
`EXISTE-SATISFACE`, N6 ya lo declaró así (`CAND-2`: ¿el CNGMD codifica
*monitoreo y sanción* como atributos del comité, o solo su existencia? —
decide si hay driver institucional para un diseño **multinivel**, no si la
regla individual queda medible). v1_1 (este acto): `comite\w*` → 0/42 536 ·
"participa/pertenece/miembro" → 2/42 536, inspeccionados:
`adultos_ensanut2024_w.dta a0306g` "¿lo invitaron a un Grupo de [actividad
física]?" — grupo de ejercicio, no organización civil con sanción
(descartado) · "coopera/aporta obra" → 0. **Sin novedad — la ruta sigue
siendo la ficha de N6.** Clasificación: `CON-CANDIDATA` (CNGMD, pendiente de
abrir bytes para `CAND-2`; sucesor sugerido por N6: `L15 ·
ABRE-ADMINISTRATIVAS-SALUD/COOPERACIÓN`, caja).

**`tanda.conoce_organizadora`.** N5: `EXISTE-NO-SATISFACE` — el desenlace
está medido y limpio: `cr04 PARTICIPADO TANDA`, `cr05a_2 MONTO APORTADO
TANDA`, `crh01_1e TANDA GUARDA AHORROS` (ENNVIH, `en_corpus=SI`); el *driver*
—conocer personalmente a la organizadora— es 0/241 591 en dos formulaciones
dirigidas. N6: `NO-APLICA` (la tanda es informal por definición, sin registro
administrativo). v1_1 (este acto): `tanda/tandas` → **33/42 536**,
inspeccionados los 33: **confirma el desenlace en un SEGUNDO instrumento**
— `round5_mexiconew_anon.dta` (panel Compartamos/AEJ, el mismo dataset que
`MAESTRA38-N5` ya había usado para otro dominio) trae `p4_9`
"¿Participó en tandas el año pasado?", `p4_10` "¿en cuántas?", `p4_11a1/a2`
"¿cuántas personas participan?", `p4_11b1/b2` "¿cuánto recibió?" — **ninguna
pregunta por conocer a la organizadora**; el resto de los 33 es ruido de
homonimia con "estándar"/"standard" (WVS "standard of living", LAPOP
`strata` "peso estandarizado", ENSANUT "porción estándar", encuestas de
negocios sobre software "standard") — descartado en bloque, §1.3.c. **El
patrón se sostiene con un instrumento más: desenlace medido dos veces, driver
cero veces.** Instrumento mínimo: a participante de tanda, "¿usted conocía
personalmente a quien organiza/administra esta tanda antes de entrar?",
atado a la misma pregunta de participación que ENNVIH y el panel Compartamos
ya hacen.

**`confianza.puente_personal`.** N5: `EXISTE-NO-SATISFACE` — los 2 aciertos
de "confía" son confianza generalizada tipo Rosenberg (ENCUP `P34`/
`P10STGBS`) — **exactamente lo que la regla declara que NO mide**, porque la
regla es sobre el puente, no la confianza difusa; "paisano/correligionario"
0/241 591. N6: `NO-APLICA`. v1_1: los tres 0/42 536 (confía-desconocido,
paisano-correligionario, participa-organización). **Ausencia total, tres
pasadas.** Instrumento mínimo: "cuando conoce a alguien por primera vez a
través de un conocido en común, paisano o correligionario, ¿confía más en
esa persona que en un desconocido sin esa conexión?", escenario vs. control.

**`faena.sancion_social_pueblo_mestizo`.** N5: `NO-ENCONTRADO` — 0/241 591 en
`faena`/`tequio`/`cooperación vecinal`. N6: `EXISTE-NO-SATISFACE` — si el
CNGMD codifica cooperación vecinal normada/obligación de faena en
`m2_marco_regulatorio`, el *driver* quedaría medido a nivel municipio; **no
se puede confirmar por `usado_para`** sin abrir bytes (`CAND-3`). v1_1:
`faena/tequio/cooperación vecinal` → 0/42 536 · "coopera/aporta obra" →
0/42 536 · `comite\w*` → 0/42 536. **Sin novedad.** Clasificación:
`CON-CANDIDATA` (CNGMD `m2_marco_regulatorio`, pendiente `CAND-3`).

**Plan de cobertura, `cooperación`.** (i) medibles hoy: **0**. (ii)
adquisiciones con ficha: **2** (`comite.monitoreo_sancion_visible` vía CNGMD
`CAND-2`, `faena.sancion_social_pueblo_mestizo` vía CNGMD `CAND-3` — ambas
requieren abrir bytes en CAJA para confirmar codificación, **no** dato
nuevo). (iii) hipótesis declaradas: **2** (`tanda.conoce_organizadora`,
`confianza.puente_personal`). (iv) criterio 2: con (i) **0 de 4**; con
(i)+(ii), **si ambas `CAND` se confirman**, **2 de 4** — sigue sin llegar a
3, y las dos que sí subirían tienen la misma limitación de unidad de análisis
(municipio, no persona) que N6 ya documentó, así que subir el conteo exigiría
además un diseño multinivel, no solo abrir bytes. **Veredicto:
`COMPLETABLE`.**

### 2.5 · `información` (§3.9, líneas 573-576) — 4 reglas, **1 medible, 0 con-candidata, 3 hipótesis**

| id | R-n | tier | antecedente | desenlace | `ya_medido.py` | clasificación |
|---|---|---|---|---|---|---|
| `informacion.credibilidad.allegado_confianza` | R9.3 | `[MEDIA]` | información reenviada por allegado de confianza (vs. tema de alto riesgo) | sube credibilidad inicial vs. fracción verifica en otro medio | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `informacion.deferencia.costo_acceso_experto` | R9.1 | `[FUERTE]` | experto accesible/cercano/asequible vs. caro/lejano/ya falló | defiere vs. prevalece "yo sé por experiencia" | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `salud.vacunacion.disponible` *(id con dominio equivocado — regla de §3.9)* | R9.2 | `[FUERTE]` | vacuna/servicio disponible y campaña llega | mayoría acepta (hueco es logístico, no actitudinal) | NUNCA-MEDIDA | **MEDIBLE-COMO-ESTÁ** *(propuesta)* |
| `informacion.escuela.miedo_a_caer_clase_media` | R9.4 | `[MEDIA]` | clase media con miedo a caer (`segsoc`=1 ∧ `est_socio`=3; "miedo a caer" no observado por el propio canon) vs. popular | escuela privada como seguro anticaída vs. pública con aspiración | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |

**`credibilidad.allegado_confianza`.** N5: `EXISTE-NO-SATISFACE` — el único
acierto es `P14ST.L Confianza en las redes sociales` (ENCUP) — confianza en
el **canal**, no en el **emisor allegado**, que es justo el contraste de la
regla; fuente de la información y verificación: 0/241 591 cada una. N6:
`NO-APLICA`. v1_1 (este acto): "confía/cree...información/noticia/medios" →
**8/42 536**, inspeccionados: LAPOP `B37` "¿hasta qué punto tiene confianza
en los medios de comunicación?" — presente en **cuatro olas** (2004, 2006,
2019, 2023) — **mismo defecto que ENCUP: confianza en el medio/institución,
no en el mecanismo de relevo por un allegado.** Descartado por §1.3.c (no es
ruido de substring — es un reactivo real, pero mide otra cosa: el canal
agregado, no la vía interpersonal). Nota de procedencia del canon
(enmienda `D-04`, ver `atencion.leve_sin_imss`/`deferencia.costo_acceso_
experto`): si estas fallan por el mismo lado, no son refutaciones distintas.
Instrumento mínimo: "cuando alguien de confianza (familiar, amigo) le
reenvía información, ¿la cree más que si viniera de un medio impersonal? ¿lo
hace distinto si el tema le parece de alto riesgo?", población general.

**`deferencia.costo_acceso_experto`.** N5: `EXISTE-NO-SATISFACE` — los 2
aciertos dirigidos son hospitalización (`hsn02f`), no consulta por
deferencia; el costo de acceso al experto —la prueba que la enmienda `D-04`
vuelve central— no tiene reactivo. N6: `EXISTE-NO-SATISFACE` — CLUES (DGIS)
da la oferta territorial de establecimientos, proxy defendible del *costo de
acceso*, sin desenlace (a quién le cree esta persona). v1_1: "consultó
especialista" → 0 · "atenc-imss-privado" → 0 · "chequeo/revisión" →
1/42 536 (mismo ítem de embarazo/ENSANUT ya descartado en `hombre_sin_
permiso`). **Mismo patrón que `leve_sin_imss`: driver proxy administrativo
sin desenlace, desenlace de encuesta sin driver, cero reformulación honesta
posible.** Instrumento mínimo: idéntico al de `credibilidad.allegado_
confianza`, con el eje "costo/cercanía del experto formal" en vez de
"allegado vs. medio".

**`salud.vacunacion.disponible`.** N5: `EXISTE-SATISFACE` *(propuesta)* — los
dos términos existen: desenlace `cen12_1a CONSULTA RECIBIO:VACUNACION`,
`he25c SERV EMBARAZO:VACUNA TETANOS` (ENNVIH); disparador (disponibilidad)
`ce19d_2 COSTO VACUNA CONSULTA`, `hs16d_2 COSTO VACUNA HOSPITAL` — mismo
instrumento, ENNVIH, misma persona. **Confirmado y reforzado por v1_1 (este
acto):** `vacun\w+` → **268/42 536** (frente a 81/241 591 en N5 — universo
distinto, más filas porque `descargas_mx_v1_1` indexa `ENSANUT 2024` a nivel
de variable cruda, no solo agregada): `adolescentes_ensanut2024_w.dta d0321j`
"¿te vacunaron contra el tétanos durante el embarazo?", `d0321p` "¿Tdap
(tosferina)?", sección completa de vacunación — **mismo instrumento, mismo
patrón antecedente-desenlace**, un tercer dataset (ENSANUT 2024) que
corrobora sin necesitarse para el sello. **MEDIBLE-COMO-ESTÁ, se propone,
DIRECCIÓN revisa.**

**`escuela.miedo_a_caer_clase_media`.** N5: `EXISTE-NO-SATISFACE` — desenlace
medido y limpio (`P82` ENCUP; `edn14`/`eh03`/`ed13 LA ESCUELA ES PUBLICA/
PRIVADA?`, ENNVIH); **el *driver* «miedo a caer» es 0/241 591, y el propio
canon ya lo declara "no observado" en el texto de la regla** (§1.6) — ausencia
estructural, no solo de corpus. N6: `NO-APLICA`. v1_1: "escuela privada/
pública" → 4/42 536, confirma el desenlace en un tercer instrumento
(`menores_ensanut2024_w.dta m0202`/`m0205 ¿es público o privado?`) — no
mueve el *driver*, sigue en 0 · "nivel de vida...padres/hijos" → 0 ·
"participa/pertenece" → 0. **El *driver* está declarado "no observado" por
el propio modelo, no solo ausente del corpus — es el caso más cerrado de
`HIPÓTESIS-SIN-INSTRUMENTO` del universo.** Instrumento mínimo: percepción
subjetiva de movilidad descendente ("¿le preocupa que su situación económica
empeore o que sus hijos vivan peor que usted?"), hogares clase media, ligada
a la elección de escuela ya medida.

**Plan de cobertura, `información`.** (i) medibles hoy: **1**
(`salud.vacunacion.disponible`, propuesta, reforzada por tercer instrumento).
(ii) adquisiciones con ficha: **0** — CLUES (N6) es proxy de driver sin
desenlace, no una ficha de adquisición nueva; no cuenta como (ii). (iii)
hipótesis declaradas: **3**. (iv) criterio 2: con (i) **1 de 4**; con
(i)+(ii) sigue en **1 de 4** (no hay (ii) que sumar). **Veredicto:
`COMPLETABLE`.**

### 2.6 · `comunicación` (§3.10, líneas 583-586) — 4 reglas, **1 medible, 0 con-candidata, 3 hipótesis**

| id | R-n | tier | antecedente | desenlace | `ya_medido.py` | clasificación |
|---|---|---|---|---|---|---|
| `comunicacion.rechazo.indirecto_face` | R10.1 | `[FUERTE]` | hay que emitir un rechazo | indirecto ("vamos a ver"), no directo | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `comunicacion.retroalimentacion.privada_publica_capital_social` | R10.2 | `[MEDIA-FUERTE]` | retroalimentación negativa | privada/indirecta/positiva vs. pública destruye capital social | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |
| `comunicacion.inseguridad.ver_oir_callar` | R10.3 | `[FUERTE]` | contexto de inseguridad/autoridad no confiable | "ver, oír y callar" (no denuncia) | NUNCA-MEDIDA | **MEDIBLE-COMO-ESTÁ** *(propuesta, nueva de este acto)* |
| `comunicacion.directividad.regional_generacional` | R10.4 | `[MEDIA]` | interlocutor norteño/joven-urbano vs. sur/mayor/rural | mayor directividad vs. más indirección | NUNCA-MEDIDA | **HIPÓTESIS-SIN-INSTRUMENTO** |

**`rechazo.indirecto_face`.** N5: `NO-ENCONTRADO` — los 38 aciertos de
"favor" son la muletilla del enumerador ("por favor dígame...", ENCUP), no
actos de habla del informante; "decir que no"/"cortés" 0/241 591. N6:
`NO-APLICA`. v1_1 (este acto): "favor/le pidió" → **74/42 536**, inspeccionado
en bloque: soborno/mordida (WVS `Q118`, LAPOP `EXC2`/`EXC17`), asistencia a
reuniones cívicas con guion de enumerador ("por favor dígame si asiste...",
LAPOP `cp6`-`cp13`), notas de aplicación de ENSANUT ("por favor devuelve la
tablet", "favor de indicar la cantidad") — **ninguno es un acto de habla del
respondente rechazando una petición**, todo es guion de instrumento o
homonimia de "a favor de" (posición política). Descartado en bloque, §1.3.c
· "decir que no/rechazar" → 0 · "cortés/quedar bien" → 6/42 536 (mismo ruido
LAPOP "cortes"=tribunales/apagones ya visto en `tiempo.compromiso.si_voy_
incierto`). **Cero señal real en dos pasadas independientes de inventario.**
Instrumento mínimo: viñeta de petición/invitación que el respondente no
puede o no quiere cumplir, y si su respuesta reportada es un "no" directo o
una fórmula indirecta ("vamos a ver", "déjame ver").

**`retroalimentacion.privada_publica_capital_social`.** N5: `NO-ENCONTRADO`
— los 40 aciertos de "desacuerdo" son la escala Likert de opinión política de
ENCUP ("¿qué tan de acuerdo... la democracia es peligrosa?"), no
retroalimentación interpersonal; público-vs-privado 0/241 591. N6:
`NO-APLICA`. v1_1: "regaña/critica en público" → 0 · "conflicto trabajo/jefe"
→ 0 · "desacuerdo/discusión" → **14/42 536**, inspeccionados: LAPOP `ING4`/
`PN2`/`DEM23`/`MEX7-9` — **mismo patrón que N5 ya encontró en ENCUP**, escala
de acuerdo/desacuerdo con proposiciones sobre democracia y reelección, no
retroalimentación interpersonal (descartado). **Confirma, con un segundo
instrumento, que el patrón de ruido es sistemático (boilerplate de escala
Likert de opinión política), no un artefacto de una sola encuesta.**
Instrumento mínimo: viñeta de dar retroalimentación negativa a un
subordinado/compañero, en privado vs. en público, y el desenlace declarado
sobre el vínculo.

**`inseguridad.ver_oir_callar` — hallazgo principal de este acto.** N5:
`EXISTE-NO-SATISFACE` — 170 aciertos de `denunci*` son `p6_19_1..4
¿Presentó una queja o denuncia ante…?` (ENDIREH 2016), pero **el universo de
ENDIREH es violencia contra la mujer, no "contexto de inseguridad/autoridad
no confiable" en general**, y ninguna formulación confirma el alcance por
texto — mismo estándar que N5 aplicó a `sm16`/ENNVIH en
`2026-09-01-mapeo-fp190.md`. N6 (administrativo): `EXISTE-NO-SATISFACE` con
sesgo de selección — CNGMD registra denuncias que **ocurrieron**, sin
denominador de quienes callaron. **v1_1 (este acto) encuentra un instrumento
mejor, no visto por N5/N6 porque ninguno corrió `descargas_mx_v1_1`:** el
módulo `AOJ` de **LAPOP AmericasBarometer** (2004/2006/2019/2021/2023),
población **general adulta**, no restringida a violencia de género:

  - **Desenlace**, mismo instrumento: `aoj1` "¿Denunció el hecho ante alguna
    institución?" (condicionado al filtro de victimización del propio
    módulo — igual que `es09`→`cen10*` en `salud.atencion.grave` condiciona
    al filtro de "tuvo un problema grave"), con `aoj1a` "¿ante qué
    institución?" y `aoj1b` "¿por qué no denunció el hecho?" — las tres,
    misma persona, mismas olas (verificado en `1658622845Mexico 2004 Export
    Version.sav`/`.dta`, gemelos byte-a-byte).
  - **Antecedente, mismo instrumento, mismo respondente:** `AOJ11`
    "¿se siente seguro/inseguro en su barrio ante un asalto o robo?", `B18`
    "confianza en la Policía", `B10A` "confianza en el sistema de justicia",
    `AOJ12` "si fuera víctima, ¿cuánto confiaría en que el sistema judicial
    castigaría al culpable?" — el contexto de inseguridad y la desconfianza
    en la autoridad, **exactamente el antecedente de la regla**, medidos en
    la misma encuesta, mismas cinco olas.

  Por la letra del criterio (a) —antecedente y desenlace en la misma
  persona, en el mismo instrumento— **esto satisface `MEDIBLE-COMO-ESTÁ`**:
  `AOJ11`/`B18`/`B10A`/`AOJ12` (antecedente) + `aoj1` (desenlace, no
  denuncia), LAPOP, mismo respondente. **Reserva declarada, honesta:** el
  texto del reactivo no confirma —sin abrir el códigobook en CAJA— si las
  categorías codificadas de `aoj1b` distinguen una razón de desconfianza en
  la autoridad de una razón puramente instrumental ("no tenía pruebas",
  "pérdida de tiempo"); esa distinción **no es necesaria para el SI/ENTONCES
  de la regla** (contexto inseguro → no denuncia), que ya queda satisfecho
  sin `aoj1b` — sí sería necesaria para probar el **PORQUE** (adaptación
  racional, no timidez), que aquí como en el resto del corpus se trata como
  mecanismo, no como antecedente exigible (mismo criterio que N5 aplicó en
  `salud.atencion.grave`). **Se propone `MEDIBLE-COMO-ESTÁ`, DIRECCIÓN
  revisa; si mesa prefiere el estándar más cauto, la caída natural es
  `CON-CANDIDATA`** (instrumento ya en el corpus, alcance de `aoj1b` para el
  mecanismo pendiente de abrir bytes) **— no `HIPÓTESIS-SIN-INSTRUMENTO`: el
  antecedente y el desenlace, ambos, ya están en el corpus, en el mismo
  instrumento.** Esto es evidencia nueva que ni N5 ni N6 tenían asignada
  (`§1.4` arriba) — no es un error de ninguno de los dos, es alcance
  declarado de ese universo (`v1_2`/`ext` y `manifiesto.yaml`, no
  `descargas_mx_v1_1`).

**`directividad.regional_generacional`.** N5: `NO-ENCONTRADO` — 0/241 591 en
las tres; el *driver* (región/generación) existe como atributo del hogar en
todo el corpus, el desenlace (directividad del habla) no existe en ninguna
fila. N6: `NO-APLICA`. v1_1: 0/0/0 en las tres. **Ausencia total, dos
vintages de inventario, cero rastro del desenlace.** Instrumento mínimo:
viñeta de desacuerdo con una decisión, y si la respuesta reportada es directa
("exijo una explicación") o indirecta, cruzada con región y edad ya medidas.

**Plan de cobertura, `comunicación`.** (i) medibles hoy: **1**
(`inseguridad.ver_oir_callar`, propuesta, LAPOP AOJ — hallazgo nuevo de este
acto). (ii) adquisiciones con ficha: **0**. (iii) hipótesis declaradas:
**3**. (iv) criterio 2: con (i) **1 de 4**; con (i)+(ii) sigue en **1 de 4**.
**Veredicto: `COMPLETABLE`.**

---

## 3 · Tabla resumen

| dominio | n reglas | medibles hoy | reformulables | con-candidata | hipótesis | criterio 2 (i) | criterio 2 (i)+(ii) | veredicto |
|---|---|---|---|---|---|---|---|---|
| `trabajo` | 4 | 0 | 0 | 0 | 4 | 0 de 4 | 0 de 4 | **COMPLETABLE** |
| `salud` | 5 | 1 | 0 | 1 | 3 | 1 de 5 | 2 de 5 | **COMPLETABLE** |
| `tiempo` | 4 | 0 | 0 | 0 | 4 | 0 de 4 | 0 de 4 | **COMPLETABLE** |
| `cooperación` | 4 | 0 | 0 | 2 | 2 | 0 de 4 | 2 de 4 *(pendiente diseño multinivel)* | **COMPLETABLE** |
| `información` | 4 | 1 | 0 | 0 | 3 | 1 de 4 | 1 de 4 | **COMPLETABLE** |
| `comunicación` | 4 | 1 | 0 | 0 | 3 | 1 de 4 | 1 de 4 | **COMPLETABLE** |
| **total** | **25** | **3** | **0** | **3** | **19** | **3 de 25 · 0 de 6 dominios** | **5 de 25 · 0 de 6 dominios** | **6 de 6 COMPLETABLE** |

**Ningún dominio queda `INCOMPLETABLE`.** Las 25 reglas, sin excepción,
tienen ruta escrita: 3 medibles hoy (propuesta), 3 con ficha de adquisición
ya identificada (2 de ellas pendientes de un diseño multinivel que persona↔
municipio exige, no solo de abrir bytes), 19 con instrumento mínimo
declarado. `REFORMULABLE` queda en cero **honestamente**: las 25 reglas o ya
tenían ambos términos en el mismo instrumento (medibles) o no tenían ninguno
de los dos reformulable sin inventar dato — se intentó reformulación
verificada (reactivo real, no substring) para las 10 `EXISTE-NO-SATISFACE`
originales de N5 y para las 7 `EXISTE-NO-SATISFACE` administrativas de N6, y
ninguna sobrevivió la regla de honestidad (c) salvo `ver_oir_callar`, que
resultó ser lo bastante fuerte para `MEDIBLE-COMO-ESTÁ` y no solo
`REFORMULABLE`.

---

## 4 · El criterio 2, como consecuencia — no se optimizó

Ni con lo medible hoy (3 de 25) ni sumando las 3 adquisiciones con ficha (5
de 25, y 2 de esas 5 necesitarían además un diseño multinivel) se alcanza
`≥3 EXISTE-SATISFACE` en **ningún** dominio. El techo teórico más alto es
`salud` (2 de 5 con todo agotado) y `cooperación` (2 de 4, con la reserva
multinivel). El patrón que `MAESTRA34-N5`/`MAESTRA36-N6` ya habían escrito se
sostiene y se afina con la tercera pasada: de las 22 reglas que no llegan a
`MEDIBLE-COMO-ESTÁ`, **10 fallan porque el corpus mide el desenlace y no el
disparador** (igual que N5 encontró), **7 tienen disparador administrativo
sin desenlace** (N6), y **19 en total quedan sin ningún instrumento nacional
que las mida por ninguno de los tres inventarios cruzados** (`v1_2`/`ext`,
`manifiesto.yaml`, `descargas_mx_v1_1`). Esto **no es una falla de búsqueda**
— son tres pasadas independientes, ≥3 formulaciones cada una, 25×3+25×3+25×3
≈ 225 corridas de motor entre los tres actos, sin contar las administrativas.
**Es información real sobre lo que las encuestas mexicanas existentes
levantan** (estructura y conducta agregada) **frente a lo que Ola 6 pide**
(percepción, vínculo personal, mecanismo de relevo de confianza) — la misma
lectura que N5 ya adelantó y que este acto confirma con un tercer universo.
**Cambiar el criterio 2, o aceptar que Ola 6 se abre con menos de 3 reglas
medibles por dominio, es decisión de mesa — este acto no la toma ni la
sugiere como default.**

---

## 5 · Hallazgos

**(a) Contra `ya_medido.py` — lo que el encargo pidió explícitamente.**
Ninguno. `MAESTRA34-N5` y `MAESTRA36-N6` clasificaron por **existencia de
reactivo** (`EXISTE-SATISFACE`/`-NO-SATISFACE`/`NO-ENCONTRADO`/`NO-APLICA`),
nunca afirmaron que alguna de las 25 tuviera una **falsación real corrida**
— y `ya_medido.py`, que solo detecta falsaciones reales (vocabulario
`CORROBORADA`/`CONTRARIA`/etc.), devuelve `NUNCA-MEDIDA` en las 25, consistente
con esa lectura. Se declara la ausencia de discrepancia en vez de forzar una
línea vacía.

**(b) Evidencia nueva que sí cambia una clasificación, distinta del hallazgo
(a) pedido por el encargo.** `comunicacion.inseguridad.ver_oir_callar` sube
de `EXISTE-NO-SATISFACE` (N5, household; N6, administrativo — ambos con
sesgo de selección o alcance no confirmado) a `MEDIBLE-COMO-ESTÁ` *(propuesta)*
al cruzar `descargas_mx_v1_1` (módulo `AOJ` de LAPOP, población general, no
restringida a violencia de género) — universo que ni N5 ni N6 tenían asignado
para Ola 6. No es un error de ninguno de los dos actos: es alcance de
inventario, declarado en `§1.4`.

**(c) Patrón de ruido repetido, para que quede registrado y no se re-busque
a ciegas.** Tres homonimias reaparecen en dos o más reglas distintas de este
mapeo: **"jefe" = jefe de hogar/familia** (no jerarquía laboral, `trabajo.
jerarquia`), **"cortes" = tribunales/apagones** (no cortesía, `tiempo.
compromiso`/`comunicacion.rechazo`), **"favor"/"por favor" = guion de
enumerador o "a favor de" política** (no acto de habla de rechazo,
`comunicacion.rechazo`), y **"grave/gravedad" = problema nacional/cambio
climático en LAPOP** (no severidad de salud, `salud.atencion.*`). Se declara
para que un futuro `/mapea` sobre estas mismas reglas no repita la
formulación ya descartada.

---

## 6 · Lo que este acto NO hace, NO decide

No cambia ningún dominio a `ACTIVO`. No relaja ni reinterpreta el criterio 2
de `motor-nucleo-medible-v1_0.md` §3.a. No sella ninguna de las 3 filas
`MEDIBLE-COMO-ESTÁ` — van como propuesta, igual que las 2 originales de N5.
No adquiere ningún payload nuevo ni escribe fila de cola real (`data/**` y
`cola` fuera de perímetro — las fichas de `§2` son recomendación textual, no
inserción). No reclasifica las 5 reglas de `FP-298` (`MAESTRA38-N5`/`N6`,
otro dominio) — se citaron solo como precedente de método. No toca
`canon/modelo-decision-v4_0.md` ni `milpa/**`. No abre `forense/prereg-caja/`
ni `data/raw`. **Cero medición de México — diseño, declarado**, tal como el
CONTADOR del encargo anticipaba.

---

## 7 · Verificación

`python3 tests/check.py --baseline`: ver `## CONSUMIDO` del encargo
archivado. Los tres controles de `ya_medido.py` corridos (25/25
`NUNCA-MEDIDA`) y las 75 corridas de `busca_reactivos.py --tablas
descargas_mx_v1_1` (25 reglas × 3 formulaciones, reusando las de
`MAESTRA34-N5`) verificadas a mano, salidas citadas por regla arriba.
