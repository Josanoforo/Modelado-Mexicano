# GEN2-DISENO-FASE1-CIERRE · P1 — auditoría por fuente de las fuentes restantes de fase 1 (COMMIT-1, sólo descriptores)

**Acto:** `ACTO GEN2-DISENO-FASE1-CIERRE` · 14/sep/2026 · CAJA (Ubuntu/WSL2) · base `origin/main = 4fedf1cf` (PR #757)
**Encargo:** `forense/encargos/2026-09-14-GEN2-DISENO-FASE1-CIERRE.md`
**Objeto:** `NC-0086` — «FP-201 declaró para las CINCO fuentes de fase 1 que no había campo de diseño UPM/estrato reproducible».

> Escrita en el COMMIT-1, antes de abrir un solo valor de microdato (E.5).
> Lo abierto: descriptores (`eder2017_fd.pdf`, `eder2017_descripcion_calculoR.pdf`),
> cabeceras de CSV y de `.dta` (nombres y etiquetas de variable), manifiesto,
> `data/diseno-muestral.yaml`, notas y encargos ya fusionados.

---

## 1 · Universo declarado (A.13): las cinco fuentes de `FP-201` cruzadas con las revisiones ya selladas

`FP-201` (`forense/firmas-pendientes.tsv:193`, 31/ago/2026) midió cinco reglas
sobre cinco fuentes «sin campo de diseño UPM/estrato reproducible en el
perímetro de este acto para ninguna de las 5 fuentes, declarado». Cruce contra
`origin/main` al abrir:

| # | fuente de fase 1 | regla de `FP-201` | ¿revisión de diseño ya sellada? | dónde | estado al abrir este acto |
|---|---|---|---|---|---|
| 1 | ENVIPE 2025 | `civico.denuncia.miedo_desconfianza` | **SÍ** — `EST_DIS`/`UPM_DIS`, re-estimada con diseño | `GEN2-LOTE-ENVIPE-1` (PR #653, `CALC-ENVIPE-0001`); abrió `NC-0086` | fuera del perímetro («no toca ENVIPE») |
| 2 | ENIF 2024 | `familia.apoyo.recibe_dinero_familiares` | **SÍ** — `EST_DIS`/`UPM_DIS`/`FAC_PER` en `TMODULO` | `GEN2-LOTE-ENIF-1` (PR #667, `CALC-ENIF-0001`) | fuera del perímetro |
| 3 | ENCUCI 2020 | `tramite.mordida.discrecional` (enmienda) | **SÍ** — `EST_DIS`/`UPM_DIS`/`FAC_SEL`; spec §3.7 «FP-201 se verifica, no se hereda» | `GEN2-LOTE-ENCUCI-1` (PR #673, `CALC-ENCUCI-0001`) | fuera del perímetro |
| 4 | **ENNViH/MxFLS ola 2 (2005-06)** | `dinero.ahorro.tiene_ahorros` | existencia revisada tres veces (§2.1), **nunca cerrada contra `NC-0086`** | `RECENSO-DISENO-14` · `CAL-G3-PUNTUAL` PASO 0 · `GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL` → `NC-0156` | **PENDIENTE en `NC-0086`** — este acto la cierra por cita |
| 5 | **EDER 2017** | `familia.corresidencia.adulto_familiar` | existencia **MAPEADA** (`RECENSO-DISENO-14`, 24/ago) — **nadie re-estimó** la tasa con diseño | `data/diseno-muestral.yaml` fila EDER | **PENDIENTE en `NC-0086`** — este acto audita el descriptor y re-estima |

Lista exacta de fuentes pendientes derivada aquí: **{ENNViH ola 2, EDER 2017}**
— coincide con la que dirección redactó. Ninguna quedó «revisada por un acto
que dirección no vio» en el sentido de *re-estimada*; sí hubo revisiones de
*existencia* que se citan en vez de repetirse.

`python3 tools/ya_medido.py` (`TZ=UTC`, ADR-340) sobre los dos ids:

```
=== ya_medido: familia.corresidencia.adulto_familiar ===
-- milpa/tramite.yaml --                       (sin apariciones)
-- milpa/tramite-ola5-propuesta-v0.yaml --
  :110  situacion=SELLADA-SIN-CARGA tier=MEDIA p=0.996086  [TASA-EJECUTADA]
-- data/corrida0 (RESULT + ejecución + sello) -- (sin apariciones)
MEDIDA-EN: tramite-ola5-propuesta-v0.yaml

=== ya_medido: dinero.ahorro.tiene_ahorros ===
-- milpa/tramite.yaml --
  :631  situacion=SELLADA tier=FUERTE p=0.174804  [CONTRARIA]
-- milpa/tramite-ola5-propuesta-v0.yaml --
  :47   situacion=PENDIENTE-DE-MESA tier=SELLADA p=0.174804
  :903  situacion=PENDIENTE-DE-MESA tier=SELLADA p=0.642080  [TASA-EJECUTADA]  (id …_enif2024)
-- data/corrida0 (RESULT + ejecución + sello) -- (sin apariciones)
MEDIDA-EN: tramite-ola5-propuesta-v0.yaml, tramite.yaml
```

Ambas están medidas (GEN1) y ninguna tiene `RESULT` GEN2: el sucesor que
nazca aquí es el primero de su tasa.

---

## 2 · Veredicto por fuente (vocabulario A.4), con cita textual del descriptor

### 2.1 · ENNViH / MxFLS, ola 2 (2005-06) — **`EXISTE-NO-SATISFACE`** (diseño completo pendiente de `NC-0156`)

**Ponderador:** existe. `ehh05w_all.zip` trae un `.dta` por libro con una
columna de factor cada uno; la ola 2 declara `fac_lib1`, `fac_lib2`,
`fac_3a`, **`fac_3b`** («FACTOR DE EXPANSIÓN LIBRO 3B» — el que fase 1 usó),
`fac_4`, `fac_5`, `fac_libc`, `fac_ea`, `fac_en`, `fac_s` y `fac_3a_px`/
`fac_3b_px`/`fac_4_px` (proxy). Verificado en este acto leyendo **sólo nombres
y etiquetas de variable** de los 11 `.dta` de `ehh05w_all.zip`.

**Estrato y UPM de diseño: no existen en el payload público.** Control
positivo de este acto, cabeceras (nombre + etiqueta) de los **147 `.dta` de
`ehh05dta_all.zip` + 11 de `ehh05w_all.zip` = 158 archivos, 158 leídos sin
fallo**, patrón `estrat|upm|usm|conglom|psu|strat|fac_` excluyendo los falsos
cognados `primaria`/`estrategia`: **un solo acierto no-ponderador**,
`ehh05dta_bc/c_portad.dta::estrato` («ESTRATO»), que las tres revisiones
previas ya identificaron como **tamaño de localidad** (cuatro clases), no como
estrato de muestreo. Cero columnas de UPM/conglomerado.

Revisiones selladas que este acto **cita y no repite**:

1. `ACTO RECENSO-DISENO-14` (24/ago/2026, `ADR-149`) — `data/diseno-muestral.yaml:460-…`,
   `estado: SIN_DISEÑO_PUBLICADO`: «NO PUBLICA por confidencialidad y no
   existe como columna en el microdato. La FAQ oficial de ENNViH responde
   expresamente que municipio, localidad y UPM no pueden hacerse del dominio
   público (…) se leyó la cabecera de TODOS los .dta de las tres olas — 137 en
   ehh02dta_all.zip, 147 en ehh05dta_all.zip y 141 en ehh09dta_all.zip, 425
   archivos, 425 examinados sin fallo». FIRMADO 25/ago (`FP-118`).
2. `ACTO CAL-G3-PUNTUAL` PASO 0 (`forense/notas/2026-08-24-cal-g3-puntual-cierre.md:12-20`):
   «**Resultado: AGOTADO** (universos a+b+c, con conteos)» — cabeceras de los
   425 `.dta`, las tres guías de usuario con doble extractor, y el espejo
   RAND/ICPSR bloqueado por WAF.
3. `ACTO GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL` (10/sep/2026,
   `forense/notas/2026-09-10-GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL-contraste.md`):
   la nota oficial `ennvih1_muestra_diseno` describe «un diseño probabilístico,
   polietápico, estratificado y por conglomerados» con **180 UPM** en tres
   estratos socioeconómicos, y «No hay hoy diseño público ejecutable».
   Deja `NC-0156` **ABIERTA**: «`NO-HAY-DISENO-PUBLICO-EJECUTABLE` (…) titular
   envía con identidad real; al recibir una vía operativa, sucesor congela
   spec en CAJA».

**Consecuencia para este acto:** ENNViH **no se re-estima aquí**. La tasa de
fase 1 `dinero.ahorro.tiene_ahorros` (`p = 0.174804`, `n = 6028`, `fac_3b`,
`milpa/tramite.yaml:631-653`, `RES-0029`/`RES-0030`) conserva su punto y su IC
de bootstrap simple **rotulado como lo que es**; la re-estimación con diseño es
el sucesor declarado por el encargo («cuando `NC-0156` entregue el diseño»).
`NC-0086` cierra su parte ENNViH **por frontera escrita**: el residuo vive en
`NC-0156` y en ninguna otra fila — dos filas para la misma espera es duplicar
deuda.

Hallazgo de registro que se re-confirma, no se genera: `data/manifiesto.yaml`
sigue sin `id:` para `ehh05dta_all.zip`/`ehh05w_all.zip` (fase 1, hallazgo 1;
`CORR-0008` en la demanda dice `NO-LOCALIZADO`). Fuera del perímetro de este
acto (no toca el manifiesto).

### 2.2 · EDER 2017 — **`EXISTE-SATISFACE`**

**Descriptor oficial** `data/raw/eder2017/eder2017_fd.pdf` («INEGI. Encuesta
Demográfica Retrospectiva (EDER) 2017. Descripción de la base de datos.
2018», `sha256 dd4d9311…5890541`), tabla VIVIENDA (p. 15), tipo tal como el
catálogo lo declara:

| # | variable | descripción | tipo |
|---|---|---|---|
| 107 | `est_dis` | Estrato de diseño muestral | `C (4)` |
| 108 | `upm` | Unidad primaria de muestreo | `C (5)` |
| 109 | `factor` | Factor de expansión | `N (5)` |

Definiciones (p. 40), verbatim: `est_dis` «Son los estratos seleccionados en
la segunda etapa del muestreo y corresponden a grupos de UPMs de acuerdo con
su estrato geográfico (entidad-ámbito-zona). Nota: Variable definida en el
diseño muestral.» — `upm` «(…) Estas unidades son seleccionadas en la primera
etapa del muestreo y corresponden a áreas geográficas con límites
identificables en el terreno (…). Nota: Variable definida en el diseño
muestral.» Tabla ANTECEDENTES (p. 17) #52 **`factor_per`** «Factor de
expansión», `N (5)` (definición p. 66). §1.1.3 (p. 8): «En la EDER 2017 el
factor de expansión para las personas de 20 a 54 años de edad, se encuentra en
la variable factor_per de la tabla ANTECEDENTES. En la ENH 2017 el factor de
expansión para las tablas que complementan la EDER 2017, como son: VIVIENDA,
HOGAR y PERSONA, se encuentra en la variable factor de la tabla VIVIENDA.»

**Receta de varianza del productor** `eder2017_descripcion_calculoR.pdf`
(`sha256 01c21e5e…6ff2e6f`): p. 5 `options(survey.lonely.psu="adjust")` «#
Opción para tratar los casos de los estratos con una sola una UPM»; p. 8
`DIS <- svydesign(id=~upm, strata=~est_dis, data= tabla_fin, weights=~factor_per)`.

**Cabecera real de los CSV** (primera línea, sin valores): `vivienda.csv`
(109 columnas) termina en `…,tam_loc,est_socio,est_dis,upm,factor`;
`antecedentes.csv` (52) termina en `…,factor_per`. `data/inventario-reactivos-v1_2.tsv`
lista `vivienda.csv::est_dis/upm/factor/tipo_adqui` y `antecedentes.csv::factor_per`
para `eder2017/eder2017_bases_csv.zip` — control positivo del inventario, no la
fuente del veredicto.

**Antecedente que `FP-201` no vio:** `data/diseno-muestral.yaml` (fila EDER,
`estado: MAPEADO`, `RECENSO-DISENO-14`, 24/ago/2026) ya citaba `est_dis`
«C(4) — eder2017_fd.pdf líneas 551 y 2289 (entrada #107)» y la receta
`svydesign` — **una semana antes** de que `FP-201` (31/ago) declarara la
ausencia para las cinco fuentes. La propia spec de fase 1 (§(c)4) escribió
«EDER trae est_dis/upm de diseño — si el tiempo del acto lo permite se usa
diseño real» y cerró con bootstrap simple «sin campo de diseño UPM/estrato
reproducible dentro del perímetro de este acto». **`FP-201` cae por quinta
fuente.**

**Consecuencia:** spec sucesora congelada en este mismo commit —
`forense/prereg-caja/EDER-CORRESIDENCIA-DISENO-spec-v1_0.md`
(`sha256 b6c755447c0ad33b40e44efe44c593725539a2dd51a4727a498dd82d91eb5a41`) y
`data/corrida0/CALC-EDER-0001/` (`spec.md`, `spec.yaml`, `medidor.py`). Mismo
estimando que fase 1 (E.3), varianza por bootstrap de `upm` dentro de `est_dis`
con regla de UPM única pre-declarada, Taylor de cotejo con la receta de INEGI,
control positivo posterior sobre el punto, y la sensibilidad `factor_per` que
la cláusula `se_mueve_si` de la propuesta pide (sin adjudicarla).

---

## 3 · Tabla de P1

| fuente | veredicto A.4 | ponderador | estrato | UPM | qué hace este acto |
|---|---|---|---|---|---|
| ENNViH ola 2 | `EXISTE-NO-SATISFACE` (pendiente de `NC-0156`) | `fac_3b` (`ehh05w_all/ehh05w_b3b.dta`) | ✗ (`estrato` = tamaño de localidad) | ✗ (no público, FAQ) | declara, enlaza a `NC-0156`, **no re-estima** |
| EDER 2017 | `EXISTE-SATISFACE` | `factor` (vivienda, N 5) · `factor_per` (antecedentes, N 5) | `est_dis` (C 4) | `upm` (C 5) | spec sucesora congelada → `CALC-EDER-0001` en COMMIT-2 |

**El primer resultado que produzca el procedimiento congelado es el que se reporta.**
