# `ACTO MAESTRA34-A1 · REGISTRA-Y-EVALUA-DESCARGAS-2` — cierre

Encargo archivado (A.3):
`forense/encargos/2026-09-01-MAESTRA34-A1-REGISTRA-Y-EVALUA-DESCARGAS-2.md`.
SHA de redacción `6d9692d` (merge `PR #451`), que es también la base real de
este acto — `origin/main` no se movió durante la corrida. Entorno UBUNTU
(`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable`, sonda
`https://www.inegi.org.mx/` = `200`, corpus compartido montado). Compuerta:
ninguna.

**Relanzamiento de `MAESTRA33-A4`** (`PR #440`), que cerró con `+0` payloads
porque corrió antes de que mesa bajara nada. Mismo mecanismo, ahora con insumo.

---

## CONTADOR

| magnitud | antes | después |
|---|---|---|
| payloads `OBTENIDO` (entradas en `data/manifiesto.yaml`) | 807 | **845** (+38) |
| filas `OBTENIDO` en la cola del registro | 46 | **53** (+7) |
| fuentes nuevas dadas de alta | — | **+1** (SICEE) |
| filas de `relaciones.tsv` con `capa2_manifiesto = SI` | 51 | **65** (+14) |
| reglas que pasan a `EXISTE-SATISFACE` | — | **0** (ver §4) |
| necesidades `fp190-*` que se mueven | — | **0** (ver §4) |

---

## 1 · P1 — inventario, corpus y registro

**A.13 — universo examinado.** `find "/mnt/c/Users/PC0/Descargas MX" -type f` =
**160 archivos**; con `-newermt 2026-08-14`, **38 nuevos**. (`MAESTRA33-A4` vio
122 y 0 nuevos: la diferencia son exactamente los 38 de mesa.)

**A.8 antes de registrar.** 0 de 38 `sha256` estaban ya en `data/manifiesto.yaml`
(803 entradas con `sha256` examinadas). Los catálogos World Bank 6453 y 2028 que
las recetas #1 y #8 nombran tampoco estaban (0 coincidencias); sí estaban otros
5 catálogos WB, que son otras fuentes — inspeccionado a mano, no aceptado por
coincidencia de un solo lado.

**Anti-`PR #77`.** Los 38 se copiaron a `/home/pc0/mm-corpus/raw` y el `sha256`
se **recalculó en el corpus**: 38/38 idénticos, 0 discrepancias; 38/38 visibles
por `data/raw`. Corpus 328 → 366 entradas de primer nivel. Dos archivos se
renombraron al depositarlos (`Cero Desabasto csv` y `Exportación pública de
Insumos y reportes.xlsx`): 0 de los 328 nombres del corpus traen espacios o
acentos, y el nombre original queda en la `nota` de cada entrada.

**Integridad de contenedor (A.7, la parte que no exige red).** Un hallazgo:
`Catalogos_de_Urgencias_2008_2016.zip` **no es un ZIP** — `zipfile` da
`BadZipFile`, y los primeros bytes son `37 7a bc af 27 1c`: es un archivo **7z
mal etiquetado por el servidor de DGIS**. Abre limpio con `py7zr` (21 miembros,
`test()` sin error). Registrado con su formato real, no con su extensión.

**Capa payload.** 38 entradas nuevas, una invocación de `tests/manifiesto.py
--registra` por `--id` (A.1), todas con `--descargado-por mesa-navegador`.

**Capa cola.** 7 filas cambian de estado a `OBTENIDO`. **Tres de ellas estaban
en `NO-ACCESIBLE` por muro de credencial** que dos caminatas programáticas
habían confirmado (filas 9, 10 y 57): cayeron con navegador y cuenta gratuita.
La fila 9 **no tenía receta** en el paquete — mesa la resolvió de paso.

Dos filas **no** suben de estado aunque llegaron payloads, siguiendo el
precedente que la propia fila 9 traía escrito (documentación registrada en
`ids_manifiesto`, microdato no):

- `MEXICO_PANEL_STUDY_2012` (19): llegó el codebook (205 pp., 374 variables) y
  el registro DATS; el microdato **no** — la única `distribution` del JSON trae
  `size: 0` y `availability: "Unable to determine availability"`, y hay 0
  archivos `.dta/.sav/.tab/.csv` con prefijo 35024 en la raíz.
- `CNGMD` (29): llegó el esquema conceptual de los 7 módulos, 4 cuestionarios en
  blanco y **el instalador** de Descarga Masiva; 0 de las 87 URLs de datos
  abiertos que su propio XML indexa.

El contador de intentos **no sube** en ninguna: este acto no hace peticiones de
red.

**Alta de SICEE** (fuente nueva): fila en `aliases-fuentes.tsv` (4 → 5 familias)
y fila nueva en la cola del registro (79 → 80). Se conserva identidad propia y
**no** se fusiona con la fuente canónica `INE` — misma institución, objeto
distinto, no forzado.

---

## 2 · P2 — veredicto A.4 en la capa de relación

`via_capa2.py --root .` **en lectura, antes de escribir**: 199 filas,
`COINCIDE=51`, **0 diffs**. Ninguna fila resolvía contra los ids nuevos porque
`id_manifiesto` estaba en `NO_DETERMINADO` en las 14 filas de estas fuentes. Lo
que faltaba era escribir la terna, no volver a correr el script.

Se abrió cada payload y se escribió el veredicto en las 14 filas existentes:

| filas | necesidad / regla | capa4 | clasificación |
|---|---|---|---|
| 6 (WBES 2023) + 3 (panel 2006-2010) | N22/`R2.1`, N23/`R2.2`, N32/`R10.2` | `EXISTE-NO-SATISFACE` | `NEGATIVA` |
| 2 (ICPSR 35024) | N26/`R7.3`, N27/`R7.4`-`R7.5` | `SATISFACE-UMBRAL-DOCUMENTAL` | `CANDIDATA` |
| 1 (CNGMD) | N28/`R8.1` | `INDEXADO-NO-DESCARGADO` | `CANDIDATA` |
| 2 (INE / PREP 2024) | N25/`R7.1`, N26/`R7.3` | `EXISTE-NO-SATISFACE` | `CANDIDATA` |

**El negativo de WBES no se afirma, se verifica.** Sobre las etiquetas reales:
**0 de 357** variables declaradas en el DDI 2023 y **0 de 477** del panel
2006-2010 mencionan voz o iniciativa ascendente, reporte de errores, disenso,
canal anónimo, estilo de liderazgo ni práctica de retroalimentación — las tres
cosas que los falsadores de `R2.1`, `R2.2` y `R10.2` exigen. **Control positivo
del mismo barrido**: `employee`/`worker` 38 y 51 aciertos, `training` 7,
`sector`/`size` 13. **Falsos positivos descartados a mano**: `quit` sólo aparece
dentro de `Equity` (`k5i`); `supervisor` es `a13` «Supervisor code» (control de
campo); `family` en el panel es `JRb7` (empleados familiares del fundador **al
arranque**), `k3d`/`k5d` (financiamiento de familia/amigos) y `Ll14b2`
(programas de balance familia-trabajo) — ninguna es una clasificación jerarquía
tradicional/plana. La unidad es el **establecimiento**, no el empleado.

Las 3 filas del panel estaban en `SATISFACE-UMBRAL-DOCUMENTAL`: **ese veredicto
sigue siendo cierto al nivel documental**; el nuevo es al nivel del microdato,
que hasta hoy no se había podido abrir.

`via_capa2.py --escribe`: 14 diffs aplicados, `NO_REFERENCIADO → SI`, los 14 con
`estado=COINCIDE`.

**Payloads sin fila donde escribir.** Cero Desabasto, MACU, DGIS Urgencias y
CAFR León **no corresponden a ninguna fila** de `relaciones.tsv`: sus objetos de
modelo no están en el universo `N1..N35`. En particular el registro individual
de Cero Desabasto es un candidato directo al falsador de **`R4.3`**
(*desabasto → abandono*), y `R4.3` **no tiene necesidad `N` asignada** —
`necesidad-objeto-modelo.tsv` no la incluye. Es un hueco del mapa de
necesidades, no de este acto; se reporta, no se repara (`necesidad-objeto-modelo.tsv`
es de sólo lectura en este perímetro). Al tablero como parte de **`FP-230`**.

**Perímetro mal calculado, declarado en vez de rodeado.** El encargo pide
«relación en `relaciones.tsv`» para SICEE. **No es posible dentro del perímetro**:
`tools/curador_registro/baseline.py` exige que toda relación tenga al menos una
procedencia en `evidencias.tsv`, que `utilidad-modelo.tsv` sea proyección 1:1, y
que `len(evidencias) − len(relaciones)` sea exactamente el número de fusiones.
Añadir una fila a `relaciones.tsv` sola rompe las tres. Los dos archivos que
harían falta **no están en el perímetro del encargo**. Se paró y se reporta: la
alta de SICEE queda completa en las capas payload y cola; para la capa relación
mesa necesita autorizar `evidencias.tsv` + `utilidad-modelo.tsv` en un sucesor. Al
tablero como **`FP-230`**, junto con el hueco de `R4.3`.

**`baseline.json` del curador recifrado** (el perímetro lo autoriza «si el
validador lo pide», y lo pedía): pasa de 5 errores a `"ok": true`. Uno de los 5,
`hash inválido: relaciones.tsv`, **ya estaba roto en `origin/main` `6d9692d`
antes de este acto** — verificado corriendo el validador sobre el árbol limpio.
Este recifrado también lo cierra.

---

## 3 · P3 — tachado

`forense/notas/2026-09-01-MAESTRA34-A1-descargas-pendientes-v2.md` y enmienda
fechada al paquete de recetas (texto original intacto). **6 cumplidas · 2
parciales · 3 no ejecutadas · 4 que nunca fueron descargas.** Los tres hallazgos
—el instalador de CNGMD sin correr con sus 87 URLs ya en la mano, la base
histórica de Cero Desabasto que sí llegó, y la fila sin receta que mesa resolvió—
están ahí con su evidencia.

---

## 4 · P4 — mapeo y sucesores

### 4.1 · `/mapea` no se pudo correr sobre los payloads nuevos, y por qué

`tools/busca_reactivos.py` **no lee payloads**: lee dos inventarios de reactivos
ya construidos, `data/inventario-reactivos-v1_2.tsv` (178 246 filas) y
`data/inventario-reactivos-ext-v1_0.tsv` (63 345) — **241 591 filas de universo
declarado**. Los 38 payloads de este acto no están en ese universo, porque
entrar en él exige un acto de inspección/extracción que no es éste.

Medido, no supuesto (A.13, con control positivo):

| `--encuesta` | candidatas |
|---|---|
| `urgencias` · `dgis` · `desabasto` · `macu` · `cuidados` · `cngmd` · `wbes` · `prep` · `icpsr` · `cafr` · `panel_study` | **0** cada una |
| `enterprise` | **1** — y es `ADQ15_WB870_Enterprise_Survey_MX_2010`, una variable `ID` del DDI **de la documentación vieja**, no del microdato nuevo |
| **control positivo** `ENCIG` / `ENVIPE` / `ENIF` / `ENASEM` | **14 581 / 31 140 / 6 747 / 6 496** |

Así que el mapeo de abajo se hizo **abriendo los payloads y leyendo sus
diccionarios de variables**, con el vocabulario A.4 del skill `/mapea`, que es
la sustancia que el encargo pide. Que el instrumento nombrado no aplique se
declara aquí en vez de rodearse.

### 4.2 · Contra las 6 necesidades de `FP-190`

| necesidad | qué pide | veredicto contra los 38 payloads nuevos |
|---|---|---|
| `fp190-1` SFT-04 | diccionario ENASEM, ayuda para bañarse | `NO-ENCONTRADO` — ningún payload nuevo es ENASEM |
| `fp190-2` CIV-08 | texto del reactivo ENVIPE, inseguridad en la calle | `EXISTE-NO-SATISFACE` — WBES trae obstáculos de crimen **a nivel firma**, no percepción individual en la calle |
| `fp190-3` TIC-06 | diccionario ENTI, trabajo infantil «cada mes» | `NO-ENCONTRADO` |
| `fp190-4` DIN-07 θ | texto del reactivo Banxico, presupuesto del hogar | `EXISTE-NO-SATISFACE` — CAFR trae módulo de hogar (220×435), pero esta fila es **extracción de texto** sobre un payload ya obtenido, no una fuente nueva |
| `fp190-5` DIN-11 | conocimiento de cuentas sin comisión | `NO-ENCONTRADO` — universo ya agotado en 241 591 filas |
| `fp190-6` SFT-06 | acuerdo de cuidado entre hermanos | `NO-ENCONTRADO` — MACU es municipal, no de hogar |

**0 de 6 se mueven.**

### 4.3 · Contra las reglas activas sin `p`

**Corrección de premisa.** El encargo dice «las 20 reglas sin `p` de
`forense/notas/2026-09-01-MAESTRA33-E18-P1-reglas-activos-sin-p.md`». Contra el árbol: esa nota concluye
(l.37-39) que de las **24** reglas SI-ENTONCES de los 4 dominios ACTIVOS, **23
no tienen `p` medida** y 1 sí. El «20» de esa misma nota (l.29) son las **20
reglas de dinero/cívico/familia** —las 24 menos las 4 de trámite—, cosa
distinta; y hay un tercer «20» en la nota sucesora `MAESTRA33-E18-P2` (l.56, las 20 filas
que van al registro del curador). Se evaluó contra las **23**, que es el
superconjunto honesto.

**Segunda corrección, más importante: la lista ya está desactualizada.**
`tramite.mordida.con_registro` (regla 2 de 24) **ya tiene `p` medida** desde
`MAESTRA34-L1`, fusionado en `6d9692d` — presencial 11.60 % vs
digital/registrado 2.74 %, IC95 sin traslape
(`milpa/tramite-ola5-propuesta-v0.yaml:514-581`). Van **22**, no 23 ni 20.

**Ningún payload nuevo lleva una regla a `EXISTE-SATISFACE`.** El candidato más
serio se examinó a fondo y falló por tamaño realizado, no por ausencia de
variable — se documenta porque es exactamente lo que un sucesor volvería a
intentar:

> **WBES 2023 sí trae la batería de mordida por trámite, a nivel firma**:
> `c5` (conexión eléctrica), `c14` (agua), `g4` (permiso de construcción), `j5`
> (inspección fiscal), `j12` (licencia de importación), `j15` (licencia de
> operación) — «*Informal Gift/Payment Expected or Requested*» —, más `j7a`/`j7b`
> (% de ventas y monto en pagos informales), y `j36`/`j37` (declaró/pagó
> impuestos **por vía electrónica**). Sobre el papel es el contraste que
> `tramite.mordida.con_registro` pide, en un universo distinto (firmas) y sin la
> reserva de selección que `L1` declaró para ENCIG (allá `P8_4` sólo se pregunta
> a quien ya declaró alguna práctica de corrupción; aquí `j5` se pregunta a quien
> fue inspeccionado, que es el condicionamiento correcto para `p(mordida | trámite)`).
>
> **Contra el dato, no alcanza.** De 1 322 firmas: sólo 75 fueron inspeccionadas
> (`j3`), y `j5` se pregunta sólo a esas 75 → **8 «sí»**, 60 «no», 7 NS/NC.
> Sumando las 6 baterías: **40 eventos de mordida solicitada sobre 327 preguntas
> efectivamente formuladas**. `j7a > 0` en 27 de 1 235. Y el corte por canal sólo
> existe para el trámite fiscal: cruzar `j36 × j5` deja celdas de **6 y 2**.
> Compárese con las `n` de `L1`: 9 937 presencial y 6 337 digital.
> **Veredicto: `EXISTE-NO-SATISFACE`** — la batería existe, las celdas realizadas
> no sostienen el contraste, y **no hay variable de canal por trámite** (`j36`/`j37`
> describen sólo el trámite fiscal).

Los otros candidatos, con lo que les falta nombrado:

- `dinero.planeacion.formal_estable` ← CAFR León: `EXISTE-NO-SATISFACE`. Sus
  variables de «plan» son intención de reabrir el negocio a 3 y 12 meses
  (`p1_12`, `x10`, `x11`), no compromiso financiero a horizonte largo; y **no hay
  ninguna variable de estabilidad del ingreso** (0 aciertos para
  estable/fluctuación/variabilidad/irregular/temporada). Faltan **los dos lados**
  de la regla.
- `dinero.ahorro.informal_sin_puente` / `con_puente_y_respaldo` y `R8.2` ← CAFR
  trae módulo de tandas real (`p4_9` participación, `p4_10` cuántas, `p4_11a*`
  cuántas personas, `p4_11b*` cuánto recibió) y batería de aversión al riesgo por
  loterías (`p5_1_1lo`…, `lotBcrra` CRRA, más `p5_1ries`/`p5_2`/`p5_3`).
  `EXISTE-NO-SATISFACE` para `R8.2`: **no hay variable de relación con la
  organizadora**, que es el antecedente de la regla. Queda anotado como candidato
  vivo para las dos reglas de ahorro informal, que exigen definir «puente» y
  «respaldo» antes de poder adjudicar.
- `familia.cuidado.recae_mujeres_40mas` ← MACU: `EXISTE-NO-SATISFACE`. Es
  municipal y de oferta/demanda potencial; no hay unidad de hogar ni edad o sexo
  de quien cuida. Además **el archivo no trae año en ninguna parte** (3 hojas, 37
  columnas, 0 columna de año, 0 cita de fuente en las 4 885 cadenas del libro);
  sólo se puede acotar por sus propiedades de documento (creado 2024-11-20).
- Reglas de trámite/cívico servidas por CNGMD m3/m5: `INDEXADO-NO-DESCARGADO`.
  Las 87 URLs están identificadas; hasta correrlas no hay dato.

### 4.4 · Sucesores — ninguno de los dos condicionales se cumple

El encargo condicionaba ambos sucesores, y **ninguna condición se cumple**:

- **`MAESTRA34-L3 · CIVICA-CONCURRENTE`** — condición: «si SICEE/cómputos dan
  `EXISTE-SATISFACE` para la cívica concurrente». **No se cumple.** El PREP 2024
  es federal-only (0 menciones de local/estatal/municipal en el `LEEME` de INE,
  idéntico en los 3 paquetes) y no trae columna de municipio. Faltan las dos
  mitades: la elección local **no concurrente** (2022 ó 2023) y la granularidad
  municipal. **No se redacta**; las vías vivas quedan en la nota de pendientes
  §4, con la spec de `L1-spec.md:502-508` esperándolas.
- **`REGLAS-ACTIVOS-L2`** — condición: «si alguna de las reglas pasa a
  `EXISTE-SATISFACE`». **No se cumple**: 0 de 22 lo hacen. **No se redacta.**

Redactar cualquiera de los dos habría exigido inventarle una condición al
encargo. El hallazgo es que las condiciones no se cumplieron **y por qué**, con
la `n` exacta que las tumbó.

---

## 5 · Suite

`python3 tests/check.py --baseline` → **ROJO**: *30 761 entradas nuevas frente a
`tests/baseline.json`* — y **las 30 761 son `T27`**. Ningún otro test aporta una
sola entrada nueva. Ver §6: el defecto es previo y estructural.

**Los tests que este acto sí podía romper pasan todos**: `T15 T-ADR-COUNT` `ok`
(el recifrado de `277 ADR` en los tres sitios cuadra), `T25 T-ROTULOS` `ok`,
`T26 T-VISTA-COLA-ADQUISICION` `ok` (la vista está regenerada),
`T20 T-CASCADA-MARCADA` `ok`, `T21 T-CAPA2-CAPA3` `ok`, `T16 T-SUITE-SELF-CHECK` `ok`.

**Medición de control**: se corrió `--baseline` **tres** veces — antes de la
cascada (con los 38 payloads ya en el corpus), al cerrarla, y otra vez después de
resolver el merge de `origin/main`. **30 761 en las tres.** Ni la cascada completa
—`ADR-278`, `L0`, cabeceras, `registro-rotulos`, tablero, notas, `CONSUMIDO`— ni la
resolución del conflicto añadieron **ni una** entrada nueva. Los 10 `FAIL` restantes
(`T02`, `T05`, `T06`, `T08`, `T09`, `T11`) ya estaban en el baseline congelado.

---

## 6 · `T27` está roto para todo payload del corpus — previo a este acto

`T27 · T-INFRA` exige que todo archivo bajo `data/` aparezca por nombre base en
`data/INFRAESTRUCTURA-v1_0.md`. Contra el árbol:

- La lista de perdón `_T_INFRA_ARCHIVOS_CONOCIDOS` tiene 213 entradas y **0 bajo
  `data/raw`**.
- `data/INFRAESTRUCTURA-v1_0.md` no cita **ningún** nombre de payload
  (`enasem2024`, `ucdp_ged261_csv.zip`, `wb2661_Baseline.zip`, `mociba2016`: 0
  cada uno).

Es decir: **ningún payload del corpus compartido puede pasar `T27` hoy**, ni los
328 previos ni los 38 de este acto. El efecto se multiplica ~18× por el symlink
autorreferente `/home/pc0/mm-corpus/raw/raw → /home/pc0/mm-corpus/raw` (12/ago,
ya documentado y no reparado).

Medido: **30 761 entradas nuevas frente a `tests/baseline.json`, y las 30 761 son
`T27`** — ningún otro test aporta una sola entrada nueva. De las 30 762 líneas
`T27`, **698 citan un archivo de este acto**; las otras **30 064 son previas**.

**No se repara**, y no por comodidad: el remedio de `T27` es escribir en
`data/INFRAESTRUCTURA-v1_0.md` o en `tests/check.py`, y **ninguno de los dos está
en el perímetro** de este encargo. Queda propuesto en el tablero como **`FP-229`**,
con los tres remedios posibles nombrados (citar los payloads en `INFRAESTRUCTURA`,
perdonar `data/raw/**` en la lista del test, o quitar el symlink autorreferente).

---

## 7 · Deriva a mitad de empuje — `ADR-277` → `ADR-278`

Al hacer `git push`, `origin/main` había pasado de `6d9692d` a `9d2e69d`:
`PR #452` / `ACTO MAESTRA34-L2 · ARBITRA-v1_2` fusionó primero y **tomó el
`ADR-277`**. Regla de la casa: renumera quien fusiona segundo. Este acto pasa a
**`ADR-278`**.

**El `git merge origin/main` NO marcó `CONFLICT` en `canon/gobernanza-v1_15.md`**
y dejó **dos `**ADR-277` idénticos**. Se detectó **contando aperturas** —278
aperturas contra un máximo de 277—, no a ojo. Es el mismo defecto que
`MAESTRA34-L1` documentó y la razón por la que el conteo se verifica siempre.
Tras renumerar: 278 aperturas, máximo 278, 0 duplicados, orden `276 · 277 · 278`.

El único `CONFLICT` real fue la línea `L0` de `canon/estado-programa-v1_10.md`.
Se resolvió tomando la línea de `origin/main` (que ya trae la anotación de `L2`)
y **anteponiendo** la de este acto, sin reescribir ninguna anterior. Verificado
por conteo: 37 anotaciones en la base `6d9692d` → 38 en `origin/main` → **39**
ahora; una sola línea `L0`; 0 marcadores de conflicto.

**Defecto previo encontrado de paso, declarado y no reparado:** la línea `L0`
ya traía **6 anotaciones duplicadas** (`ADR-236`, `238`, `239`, `240`, `241`,
`242`) **antes de este acto** — verificado corriendo el conteo sobre
`6d9692d` y sobre `origin/main`, donde aparecen idénticas. No las introdujo
este acto y repararlas es reescribir prosa sellada ajena.

**Carriles.** El encargo declara: «`MAESTRA34-L2` … **NO** arranca hasta el merge
de éste». `MAESTRA34-L2` arrancó y fusionó antes. Se reporta; no es de este acto
resolverlo. Perímetros disjuntos salvo los cuatro archivos de cascada
compartidos: `codificacion-R-v1_0.tsv`, `corridas-R/**` y
`forense/prereg-duelo-v2/**` quedan intactos por este acto.

---

## 8 · Lo que este acto no hizo

No descargó por red · no abrió microdato para **medir** (lo abrió para
caracterizar, que es lo que P2 pide: cabecera, columnas, filas, años) · no cargó
reglas · no tocó `milpa/**` ni corridas ni el marco · no fusionó su propio PR.
