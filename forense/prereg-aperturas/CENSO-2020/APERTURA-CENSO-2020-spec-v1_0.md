# Expediente de apertura · Censo 2020 (muestra censal) · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: el Censo 2020 sigue RESERVADO para
los contendientes que lo declaran (E.6); lo levanta el código congelado de este expediente, en caja, en el commit que
mesa autorice, o mesa por escrito.

## 0 · Premisas

- [LEÍDO] Contendientes sellados (regla 6: ninguno nuevo) que declaran la ola «RESERVADA (E.6), no es input»:
  `CALC-EIC-HOGARES-2015-0001` (Intercensal 2015, unidad HOGAR, tabla `TR_VIVIENDA15`: 4 conductas de `TIPOHOG` ×
  {TOTAL, JEFATURA, TAMLOC, ENTIDAD}; «Censo 2020 RESERVADO (E.6), no es input»; spec `forense/prereg-caja/COLA-EIC-HOGARES-spec-v1_0.md`)
  y `CALC-CCPV-FAM-PISOS-0001` (muestra censal 2010, 32 ZIP `MC2010_<ee>_dta`; 12 proporciones y 1 media de hogar × {TOTAL,
  SEXO-JEFE, EDAD-JEFE, ESCOLARIDAD-JEFE, TLOC, ENT} y PER60-VIVE-SOLO de persona × {TOTAL, SEXO, EDAD, TLOC, ENT}; «2010
  abierta (muestra censal); 2020 RESERVADA»; spec `forense/prereg-caja/CCPV-FAM-PISOS-spec-v1_0.md`). Los dos publican P, EE,
  IC-LO, IC-HI, N con IC de diseño; ninguno publica persistencia.
- [EJECUTADO] Microdato de la muestra censal 2020 en `data/manifiesto.yaml` (lector YAML; 218 ids con `2020` y censo/cpv/ccpv
  en el id): los 32 `cc1_inegi_ccpv_2020__censo2020_ca_<ent>_csv` («Muestra (cuestionario ampliado)», ZIP de 3 miembros,
  raíz `data_raw`) y el nacional `cc1_inegi_ccpv_2020__censo2020_ca_eum_csv` (486 238 463 B; la suma de los 32 estatales es
  489 009 377 B: mismo contenido partido por entidad). Se usan **los 32 estatales**, como el contendiente CCPV usó los 32 de
  2010; el nacional no se lee (no se abre dos veces lo mismo). No son microdato de la muestra y quedan fuera: ITER, CL
  (localidades), CAAS (alojamientos de asistencia social), CEU (entorno urbano), CPV_CB_*_ejemplo (ejemplos del básico),
  cuestionarios, diccionarios, clasificaciones.
- [EJECUTADO] **Hallazgo:** ninguno de esos ids lleva `estado_reserva` en el manifiesto; la reserva del Censo 2020 vive sólo
  en las etiquetas de los dos contendientes (A.16: el estado no está en el campo) y la vista
  `aperturas-pendientes-v1_0.tsv` no tiene fila CCPV 2020. La spec del contendiente CCPV (§0, 25/sep) decía «la muestra 2020
  no está en el corpus»; entró el 25/sep por GEN2-CORPUS-COMPLETO-1 sin nacer RESERVADA (E.6). Se reporta; no se corrige aquí.
- [EJECUTADO] Ningún CALC sellado lee un id `censo2020_ca_*` (`grep` sobre los 390 `data/corrida0/*/spec.yaml` → 0).
- [LEÍDO] Nombres de columna 2020 por el diccionario del cuestionario ampliado indexado en `data/inventario-fd-v1_1.tsv`
  (`diccionario_cuestionario_ampliado_cpv2020.xlsx`, documentación, no dato): VIVIENDAS trae `ENT`, `ID_VIV`, `TIPOHOG`,
  `NUMPERS`, `JEFE_SEXO`, `TAMLOC`, `FACTOR`, `ESTRATO`, `UPM`; PERSONAS trae `ENT`, `ID_VIV`, `SEXO`, `EDAD`, `PARENTESCO`,
  `NIVACAD`, `FACTOR`, `ESTRATO`, `UPM`, `TAMLOC`. **No** trae `TAM_LOC` ni `PARENT` (nombres 2010 del contendiente CCPV).
- [SUPUESTO→rama prevista] NUBE sin corpus montado: los códigos no se leen aquí; se fijan **sobre la ola de cada piso** (EIC
  2015; muestra 2010), rotulado así (§5). Nombres de miembro `Viviendas*.csv` / `Personas*.csv` por las tablas del
  diccionario; el medidor los resuelve por patrón (cero o más de uno → PARO).

### 0.1 · Celdas ya vistas (RETROSPECTIVAS)

Cifras publicadas de hogares 2020 citadas en el repo antes de este expediente: `canon/mapa-dominios-v1_1.tsv` FAM-025
(«24.4% ampliados, 12.4% unipersonales», instrumento no identificado por el report: Censo 2020, Intercensal o ENIGH),
VEJEZ-006 («16.8% [de hogares con 60+] eran unipersonales — 1.8 millones de personas de 60+ viviendo solas», Censo 2020) y
la spec del contendiente CCPV §5 («82 % / 16.8 % entre hogares con 60+»). Por conservadurismo (E.6: tabulados y comunicados
cuentan como vistos) son **RETROSPECTIVAS 7 celdas**: `EIC15-HOGAR-AMPLIADO-TOTAL-TODOS`, `EIC15-HOGAR-UNIPERSONAL-TOTAL-TODOS`,
`CCPV10-HOG-AMPLIADO-TOTAL-TODOS`, `CCPV10-HOG-UNIPERSONAL-TOTAL-TODOS`, `CCPV10-AM-HOG-UNIPERSONAL-TOTAL-TODOS`,
`CCPV10-AM-HOG-NUCLEAR-O-AMPLIADO-TOTAL-TODOS` y `CCPV10-PER60-VIVE-SOLO-TOTAL-TODOS` (su numerador expandido se citó). Su R
se emite; **no puntúan** en la primaria PROSPECTIVA (el medidor les pone lo = hi = None: constante `VISTAS`); la nota de
apertura reporta su cobertura aparte, rotulada RETROSPECTIVA. Las otras **793 celdas** son PROSPECTIVAS.

## 1 · Estimandos

Por cada celda de cada contendiente (800: EIC15 160 = 4 × 40; CCPV10 640 = 13 × 46 + 1 × 42): **R = Σw·y / Σw** en la muestra
censal 2020, con la recodificación y el marco del contendiente (medidores sellados importados por bytes con sha256 fijado en
`APERTURA-CENSO-2020-spec.yaml`). Ids `<EIC15|CCPV10>-<conducta>-<eje>-<cat>`.
- EIC15 (spec del contendiente §2): HOGAR-AMPLIADO `TIPOHOG` = 2 sobre {1,2,3,5,6}; HOGAR-NUCLEAR = 1; HOGAR-UNIPERSONAL = 5;
  HOGAR-AMPLIADO-ENTRE-FAMILIARES = 2 sobre {1,2,3}. Ejes: JEFATURA (`JEFE_SEXO` 1 H / 3 M), TAMLOC (1–5), ENTIDAD (`ENT`).
- CCPV10 (spec del contendiente §0–§3, `prepara()`, `conducta_hogar()`, `conducta_persona()`): tipos de hogar de `tipohog`;
  presencia de 60+ / <18 por `edad` de PERSONAS unida por `ent|id_viv`; jefe = única persona con `parent` = 1; tres
  generaciones por `parent`; HOG-TAMANO-MEDIO = **media** de `numpers` (1–60), R en personas por hogar (tipo `flotante`);
  PER60-VIVE-SOLO sobre personas 60+ con `tipohog` = 5.

## 2 · Universo, unidad, ponderador, diseño

Unidad HOGAR (vivienda particular habitada de VIVIENDAS; `FACTOR` de vivienda) y PERSONA 60+ en PER60-VIVE-SOLO (`FACTOR` de
PERSONAS). Válido: `FACTOR` > 0, `ESTRATO` y `UPM` no vacíos. R es un punto (media en HOG-TAMANO-MEDIO); no se calcula IC de R.
Payloads: los 32 `cc1_inegi_ccpv_2020__censo2020_ca_<ags…zac>_csv` en orden de clave de entidad (01 ags … 32 zac); el
medidor exige que cada ruta sea `Censo2020_CA_<ent>_csv.zip` de su entidad (si no, PARO).
**IC del contendiente por celda:** IC-LO/IC-HI sellados de su ola (EIC 2015; CCPV 2010), de diseño; punto = P sellado.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada (para la media, la misma razón
Σw·y/Σw con y = `numpers`); un cruce levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su
propio archivo. Única lectura: `lee_payload_reservado` (cabecera de cada miembro → columnas presentes → `lee_csv_zip`). La
agregación por vivienda dentro de `prepara()` del sellado CCPV (conteos de 60+, <18, parentesco por `ent|id_viv`) es una sola
llave de hogar, no un cruce de ejes. Estructura ausente (VIVIENDAS: `ENT`, `ID_VIV`, `FACTOR`, `ESTRATO`, `UPM`; PERSONAS: además
`EDAD`) → PARO; conducta o eje ausente → vacío → R None. Probado sobre sintético con los esquemas de los dos contendientes:
`tests/test_apertura_censo_2020.py` (con soporte con nombres del piso; nombres 2020 sin `PARENT`/`TAM_LOC`; categoría vacía;
estructura ausente; entidad mal resuelta; celdas vistas no puntúan; auditoría y las 9 mutaciones) y `tests/test_prereg_aperturas.py`.

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi y R finitos (las 7 vistas no puntúan). **Primaria** (una sola, sobre las celdas de los dos
contendientes): cobertura k/n = #celdas con lo ≤ R ≤ hi, con IC de Wilson al 95 %. **CALIBRADO** si 0.95 ∈ Wilson;
**SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Orden: NO-ESTIMABLE > SUBCUBRE
> SOBRECUBRE > CALIBRADO (excluyentes). La cobertura es un conteo de celdas (unidad: celda), por eso junta hogar, persona y la
media. Secundarias, descriptivas: cobertura por conglomerado (`EIC15-<conducta>`, `CCPV10-<conducta>`) y error absoluto medio
punto-vs-R **sólo sobre proporciones de hogar** (la media y PER60 no se promedian con ellas: punto = None en esas celdas).
B-bis: los IC son de diseño de pisos de 5 (EIC) y 10 (CCPV) años antes, sobre muestras enormes (IC de décimas de punto): no son
intervalos de predicción. **SUBCUBRE es el desenlace esperado aun sin error del piso**; se lee «el piso de la ola anterior con
su IC de diseño no anticipa 2020», nunca «cambió la familia mexicana». CALIBRADO = pisos **corroborados en alcance**;
SOBRECUBRE = **acotados**. Falsador débil por construcción, declarado. Una apertura sirve a los dos sellados a la vez (E.6);
lo que se aparta sin abrir: la cobertura por contendiente como primaria (queda secundaria, por conglomerado).

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- `TAM_LOC` (2010, 4 tramos) y `PARENT` (2010) no existen con ese nombre en 2020 (§0, `TAMLOC`, `PARENTESCO`). Por la regla,
  sin recodificación ad hoc: TLOC del contendiente CCPV y todo lo que depende del jefe (SEXO-JEFE, EDAD-JEFE,
  ESCOLARIDAD-JEFE, HOG-JEFA-MUJER, HOG-TRES-GENERACIONES) salen **NO-ESTIMABLE**. Sucesor declarado: si mesa lo quiere
  medido, una v1_1 de este expediente **antes de abrir**, con el mapeo `PARENTESCO`→`parent` y `TAMLOC`→`tam_loc` verificado
  por texto y código contra el diccionario 2020 (documentación; E.6 lo permite).
- Mismo nombre, códigos posiblemente distintos [SUPUESTO a verificar en la receta paso 3]: `NIVACAD` (el catálogo 2020 podría
  desagregar bachillerato y normal de otro modo que el 0–12 de 2010), `TAMLOC` (5 tramos en EIC 2015), `TIPOHOG`, `SEXO`,
  `JEFE_SEXO` (1 H / 3 M en 2010 y 2015).
- Regla fijada: columna ausente → NO-ESTIMABLE (R None) y se declara en la nota. Columna presente con códigos distintos → el
  acto de apertura PARA antes de correr y se emite una v1_1 (el código congelado no distingue códigos). Leer el diccionario y
  el cuestionario no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-CENSO-2020-<EIC15|CCPV10>-<conducta>-<eje>-<cat>-R` (800; `-R` de HOG-TAMANO-MEDIO es `flotante`, el resto
`proporcion`), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`, `-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA: las 7 vistas no entran en K/N).
Ningún None/NaN fuera de R NO-ESTIMABLE, Wilson y MAE cuando n = 0. Contrato: `APERTURA-CENSO-2020-spec.yaml` (calc_id
`CALC-APERTURA-CENSO-2020-0001`; 32 payloads con sha del manifiesto; medidores sellados, sus `resultados.json`, receta, motor,
guardia y plantilla como inputs `origen: repo` con sha). Sin `estado_reserva` en el manifiesto, el paso 4a de la receta no mueve
nada; el acto que tenga el manifiesto en su perímetro debe poner la reserva en el campo antes de la firma (§0).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA: contendientes sellados (EIC 2026-09-26T18:52Z; CCPV 18:05Z) sin que nadie haya leído la muestra 2020; 7 celdas
  RETROSPECTIVAS por cifras publicadas (§0.1), fuera de K/N y reportadas aparte. Ninguna frase mezcla las dos columnas.
- Unidad: **hogar** (y persona 60+ en PER60, media de personas por hogar en HOG-TAMANO-MEDIO); nada se promedia entre unidades
  en el MAE; la cobertura cuenta celdas.
- Escala: proporción 0..1 salvo la media; «R dentro del IC de diseño del piso».
- Instrumentos: EIC 2015 es encuesta intercensal, no censo; su piso compite contra la muestra censal 2020 (instrumento
  hermano, mismo `TIPOHOG` de INEGI), declarado.
- Estructura ≠ cultura: la composición del hogar responde a vivienda, ingreso, migración y envejecimiento; un hogar ampliado no
  es «familismo» (familismo es de clase (b), diáspora). TLOC y TAMLOC son tamaño de localidad, no clase.
- Cifras escritas a mano: ninguna en el medidor salvo los ids de `VISTAS`, derivados de las citas de §0.1.
