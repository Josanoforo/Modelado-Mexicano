# PISOS ENIF 2021 · conductas de crédito K1–K7 por ejes · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-DIN-CREDITO-PISOS-ENIF2021-1 (21/sep/2026, CAJA). CALC reservado:
`CALC-DIN-CREDITO-PISOS-ENIF2021-0001`. Encargo archivado por A.3 en
`forense/encargos/2026-09-21-GEN2-DIN-CREDITO-PISOS-ENIF2021-1.md`
(sha256 `6f36a4a852b7c5c3d13af738796a8f32b9ac4e8078f6deefcbc0066701858371`).
Compuerta única (protege: abrir dato): esta spec, `spec.yaml` y `medidor.py`
congelados en el COMMIT-1, con el sidecar verificado y
`medidor_ejecutado_al_congelar` declarando el payload sintético, antes de
tocar `TMODULO` de 2021.

## 0 · Exposición declarada (ADR-46)

- Leídos antes de congelar: `data/credito-comparabilidad-texto-v1_0.tsv`
  (40 filas; las 8 de 2021 íntegras), `PISOS-ENIF2021-ejes-spec-v2_1.md`,
  `PISOS-ENIF2021-formalidad-spec-v1_0.md`, las dos tablas de identidad GEN2
  (`PISOS-REJILLA-arbitro-metadatos-v1_0.tsv`, 32 filas ENIF 2021;
  `PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv`, 6 filas), los medidores
  sellados de `CALC-PISOS-ENIF2021-EJES-0003` y
  `CALC-PISOS-ENIF2021-FORMALIDAD-0001`, la nota de cierre de
  `GEN2-MARCADOR-ENLACE-2` (#925), y del ZIP `enif2021_csv` **sólo la
  estructura**: `diccionario_datos_tmodulo_enif_2021.csv` (nombres, rangos) y
  los catálogos `p6_1_1`, `p6_2_1`, `p6_4_1`, `p6_4a_1`, `p6_7`, `p6_14`,
  `p6_15`, `p6_17` (códigos y etiquetas).
- NO abierto: ningún microdato de ENIF 2021 (ni `conjunto_de_datos_tmodulo`
  ni ninguna otra tabla) ni de ninguna otra ola. ENIF 2024 no se abre en este
  acto en ninguna forma (PARO a).
- El payload sintético de D-22 lo fabrica `tests/test_din_credito_pisos_enif2021.py`
  (`payload_sintetico`, 2 400 filas, `default_rng(7)`); no se parece a la
  distribución real y no produce ninguna cifra esperada.
- Cifra esperada: ninguna. Las del corpus (~37.3 % con crédito formal,
  departamental 22.6 % > bancaria 15.7 %, «no le gusta endeudarse» 38.4 %) son
  `[REPORTADO]` y no validan ni invalidan nada; «bancaria +5.2 pp desde 2021»
  no se cita (FP-404).
- `[SUPUESTO]` del encargo verificado por el diccionario del ZIP: `FAC_ELE`,
  `EST_DIS` (001…235) y `UPM_DIS` (0000001…0002013) existen en `TModulo` 2021
  con esa ortografía; `P6_4A_k` se escribe con `A` mayúscula en el archivo.

## 1 · Alcance (P1) — leído de la tabla de comparabilidad, no tecleado

Entran, con reactivo, códigos, filtro y unidad citados **desde la fila `K·2021`
de `data/credito-comparabilidad-texto-v1_0.tsv`** (`ACTO
GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1`, PR #932, sha256
`f76e965e2a23dc3b…`); el medidor recibe esa tabla como input `origen: repo` y
**PARA si el reactivo de una conducta no está escrito en su fila**:

| conducta emitida | fila | reactivo (de la tabla) | unidad (de la tabla) | base poblacional |
|---|---|---|---|---|
| `K1` | K1 | `P6_2_1..P6_2_9`; complemento `P6_14` | P | toda persona elegida 18+ |
| `K2-DEPARTAMENTAL` · `K2-NOMINA` · `K2-AUTOMOTRIZ` | K2 | `P6_2_1`, `P6_2_3`, `P6_2_5` | P por familia | toda persona elegida |
| `K3` | K3 | `P6_1_1..P6_1_5` | P | toda persona elegida |
| `K4A-AUTOEXCLUSION` · `K4B-OFERTA` (+ `K4B1-REQUISITOS`, `K4B2-ACCESO`, `K4B3-RECHAZO-ANTICIPADO`, rotulados aparte como pide la fila) | K4 | `P6_15`; base `P6_2_1..9 = 2` ∧ `P6_14 = 2` | P | **«nunca ha tenido»** crédito formal — no «no tiene hoy»; los ex-usuarios (`P6_14 = 1`) quedan fuera |
| `K5` · `K5-ENTRE-SOLICITANTES` | K5 | `P6_17` | P | toda persona elegida (código 3 = nunca solicitó, cuenta como 0) · solicitantes (`P6_17 ∈ {1,2}`) |
| `K6-PR` · `K6-P-TENEDORES` | K6 | `P6_4_1..P6_4_9` | **PR** (por producto) · agregable a P | productos formales tenidos (`P6_2_k = 1`) · tenedores de ≥ 1 producto |
| `K7-SUCURSAL` · `-APP` · `-INTERNET` · `-ESTABLECIMIENTO` · `-PROMOTOR` · `-OTRO` | K7 | `P6_7` | **PR** (último crédito; una observación por persona) | tenedores de ≥ 1 producto formal |

**No entran, por FP-404 firmada:** `K8` (fila 2021 `NO-ESTIMABLE`; el
medidor lo verifica y no la mide) y la familia **bancaria** de K2 (`P6_2_2`
no se lee ni se emite; su descriptivo rotulado es de otro acto).
`RESERVA` (20/sep): el par «crédito por app» `P6_2_8 × P6_7` está consumido en
`CALC-ENIF-FINTECH-0001` y no se relanza; `K7-APP` aquí es el marginal del
canal `P6_7 = 2` entre todos los tenedores, otro objeto, y no se cruza con
`P6_2_8`. **Componentes sin reactivo en 2021** (fiado, gota a gota, «durable»
como categoría propia) no se inventan: `K3` es la unión de los cinco ítems de
6.1 que la fila declara con reactivo (caja de ahorro, empeño, conocidos,
familiares, otro) y así se rotula.

## 2 · Desenlaces (códigos de la tabla; `_code` despoja ceros a la izquierda)

- `K1` = 1 si algún `P6_2_k = 1`; 0 si los nueve `= 2`; indefinido en otro caso.
- `K2-*` = 1 si `P6_2_k = 1`; 0 si `= 2` (k = 1, 3, 5).
- `K3` = 1 si algún `P6_1_k = 1`; 0 si los cinco `= 2`.
- `K4*`: sobre la base «nunca ha tenido» (`P6_2_1..9 = 2` ∧ `P6_14 = 2`) con
  `P6_15 ∈ 1..9`: `K4A-AUTOEXCLUSION` = `P6_15 ∈ {6,7}`; `K4B-OFERTA` =
  `P6_15 ∈ {1,2,3}`; `K4B1` = `{1}`; `K4B2` = `{2}`; `K4B3` = `{3}`. Los códigos
  4, 5, 8, 9 son «ni a ni b» y cuentan como 0 en todos. Fuera de la base o
  fuera de catálogo → indefinido (contado).
- `K5` = 1 si `P6_17 = 1`; 0 si `∈ {2,3}`. `K5-ENTRE-SOLICITANTES`: 0 sólo si
  `= 2`; `3` indefinido.
- `K6-PR` (una fila por par persona × producto con `P6_2_k = 1`): 1 si
  `P6_4_k = 1`; 0 si `= 2`; `8`, `9`, blanco → indefinido. Comparación
  **posicional** k↔k (el defecto de alineación por nombre de -0002 se
  evita con `.to_numpy()`).
- `K6-P-TENEDORES` (persona con ≥ 1 producto): 1 si algún producto tenido
  tiene `P6_4_k = 1`; 0 si todos los tenidos tienen `= 2`; si no, indefinido.
- `K7-<canal>` (tenedores): 1 si `P6_7 = código`; 0 si `P6_7` es otro de
  `1..6`; `9` y blanco → indefinido (contados).

## 3 · Ejes y rejilla — de la tabla de identidad GEN2, nunca del trámite

Categorías leídas en tiempo de ejecución de `PISOS-REJILLA-arbitro-metadatos-v1_0.tsv`
(filas `ENIF·2021·CONSTRUIBLE`: `sexo {1,2}` · `edad {18-29, 30-44, 45-59,
60+}` · `escolaridad {hasta_primaria, secundaria, media_superior, superior}`
· `localidad {menor de 15 000, 15 000 y mas}` · `cuenta {sin cuenta, con
cuenta}`) y de `PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv` (`formalidad
{sin seguridad social, con seguridad social}`). El medidor PARA si falta un
eje o si el dato produce una categoría que no está en la rejilla. Los
**cortes** son los del medidor sellado de -0003, importado por bytes
(`_age`: EDAD 18–29/30–44/45–59/60–96; `_school`: `P3_1_1` 00–02 / 03 /
04–07 / 08–09, 99 fuera; `TLOC` 1–2 → 15 000 y más, 3–4 → menor; `cuenta`
por `P5_4_1..9`). `milpa/tramite-ola5-propuesta-v0.yaml` **no es input ni se
lee** (nota b de dirección; FP-395/396/397).

**`formalidad` se cita, no se decide (P2).** Mapa de
`PISOS-ENIF2021-formalidad-spec-v1_0.md` §1 (sha256 `50b471e3e0521336…`):
`P3_10 ∈ {1..5}` → con seguridad social; `6` → sin; `9`/blanco fuera y
contados. Universo del eje: **quien trabaja** (`P3_10 ∈ 1..6`). Bajo la regla
de precedencia de `GEN2-MARCADOR-ENLACE-2` (#925: manda la tabla más
reciente, `SUCEDE-A`, `T-PRECEDENCIA`), esa spec y el dictamen de #908
(`3.13` de 2024 = `3.10` de 2021) suceden a las cuatro filas `NO-CONSTRUIBLE
· P3_13 comparable no existe en ENIF 2021` de la rejilla (#871), que aquí se
filtran por `status = CONSTRUIBLE` y no se editan.

Celdas por conducta: `NACIONAL-TODOS` + 14 categorías de los cinco ejes + 2
de formalidad + `UNIVERSO-TRABAJA` = 18; 20 conductas → 360 celdas. Por
celda: `-P`, `-IC-LO`, `-IC-HI`, `-N`, `-DEN-W`, `-B-VALIDAS`, `-SOPORTE`.

## 4 · Procedimiento congelado y guardias (P3, P4)

- Payload `enif2021_csv` (manifiesto, sha256 `0f314fa3733b4b55…`), miembro
  `conjunto_de_datos_tmodulo_enif_2021.csv`, lectura idéntica a -0003 (`_csv`
  importado: `utf-8-sig`/`latin-1`, `dtype=str`).
- Marco heredado verbatim del piso de ahorro: `FAC_ELE`; diseño
  `EST_DIS × UPM_DIS`; bootstrap de UPM con reemplazo dentro de estrato,
  **10 000 réplicas, `numpy.PCG64(42)`**, IC percentil 2.5/97.5; **un solo
  plan de réplicas para todas las conductas y todas las celdas**: una única
  llamada a `_estimate` (importado de -0003) sobre un marco combinado (todas las
  filas persona del archivo + una fila por producto tenido, con el peso y la llave de
  diseño de su persona). Las llaves `EST_DIS×UPM_DIS` del marco son las
  mismas que en -0003 y -FORMALIDAD-0001, así que el plan es el mismo.
- Filtro de diseño: `FAC_ELE > 0`, `EST_DIS` y `UPM_DIS` no vacíos. Sin
  filtro de edad ni de otro eje: cada eje conserva su denominador válido.
- **Guardia 1 · Unidad.** Cada conducta emite `-UNIDAD` (`P` o `PR`) y sus
  celdas llevan su propio denominador; el medidor no suma ni promedia
  conductas. Consecuencia declarada: emitir a la unidad de la fila; el test
  falla si una celda no pertenece a exactamente una conducta o la unidad
  difiere de la tabla. `K6-PR` y `K7-*` no se comparan con conductas `P` sin
  función de enlace (A-bis 3).
- **Guardia 2 · Soporte.** `n` sin ponderar `< 200` (piso de la casa:
  `GOB-gobierno-digital-exe15-spec`, `ENCIG` cruces) → `-SOPORTE =
  BAJO-N-MENOR-200`; la celda se emite igual. Nunca se colapsan categorías.
- **Guardia 3 · Coherencia.** Por conducta y eje: `|num_w(nacional) −
  Σ_cat num_w(cat) − num_w(eje indefinido)|` y lo mismo con `den_w`, con
  tolerancia `1e-6 × den_w(nacional)`; para `formalidad` contra
  `UNIVERSO-TRABAJA` (mismo universo, A-bis 4), sin término indefinido.
  Consecuencia declarada: **si no cierra, el medidor lanza `RuntimeError` y la
  corrida PARA**. Se emiten `-COHERENCIA-<EJE>-DELTA-NUM-W`, `-DELTA-DEN-W` y
  `-EJE-<EJE>-INDEFINIDO-N`.
- Ejecución diagnóstica sobre microdato: **ninguna**. El medidor corrió antes
  de congelarse **sólo** sobre el payload sintético del test (D-22), con 120
  réplicas; la primera corrida real es la que se reporta.

## 5 · Diagnóstico y exclusiones (se reportan, no se corrigen)

`FILAS-PERSONAS`, `FILAS-PRODUCTO`, `TENEDORES-N`, `SIN-PRODUCTO-N`,
`P6-2-INDEFINIDO-N`, `NUNCA-HA-TENIDO-N`, `EX-USUARIOS-N`,
`P6-15-FUERA-DE-CATALOGO-N`, `P6-15-FUERA-DE-BASE-N` (respondió 6.15 sin
estar en la base: discordancia de flujo), `P6-17-FUERA-DE-CATALOGO-N`,
`P6-7-NO-SABE-N`, `P6-7-BLANCO-EN-TENEDORES-N`, `P6-7-FUERA-DE-BASE-N`,
`P6-4-NO-SABE-NO-RESPONDE-N`, `P6-4-BLANCO-EN-PRODUCTO-TENIDO-N`,
`FORMALIDAD-N-UNIVERSO`, `FORMALIDAD-EXCLUIDOS-P3-10-NO-SABE`,
`FORMALIDAD-EXCLUIDOS-P3-10-BLANCO`, `UPM-EN-PLAN`; por conducta
`-N-UNIVERSO`.

## 6 · Lo que esta spec no hace

No abre ENIF 2024; no adjudica ni corona; no escribe reglas en el motor; no
mide K8 ni K2-bancaria; no edita ninguna spec, tabla de identidad ni CALC
sellado; no toca `tools/marcador_segmento.py` ni
`data/corrida0/marcador-segmento.tsv`; no adopta (`cuenta_gen2 = SI` firmado
por mesa, cuenta y no adopta).
