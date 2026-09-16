# ACTO `GEN2-CELDA-D-DISENO-CIEGO-1` · segundo diseño independiente del primer piloto celda-D

**Nota de acto · 17/sep/2026 · nube, Opus · encargo archivado:
`forense/encargos/2026-09-17-GEN2-CELDA-D-DISENO-CIEGO-1-SEGUNDO-DISENO-INDEPENDIENTE.md` (0-bis A.3, commit `1c7796c`).**

> **CIEGO — declarado antes de cualquier otra línea.** Esta sesión **no** leyó el
> diseño v1.0 de dirección (17/sep), no lo pidió y no lo infirió. No estaba en el
> árbol y no se pegó en el lanzamiento — si se hubiera pegado, el encargo ordena
> PARO y no habría nota. Tampoco se leyó ningún retorno externo sobre el mismo
> tema: `ls forense/notas/insumos-externos/ 2>/dev/null` → **el directorio no
> existe** (salida vacía, código 2). Cero insumos externos.

---

## 0 · Cabecera de universo (A.10)

| | |
|---|---|
| **SHA real al abrir** | `10afea15e19efabc6ef41b3d67d34b1cba8b4f0a` (`10afea1`, `Merge pull request #821 from Josanoforo/derivados/2026-09-16`). El encargo se redactó contra `b881ee6`. |
| **Diferencia `b881ee6..10afea1`** | **1 archivo, +2/−2**: `forense/tablero/TABLERO-PROGRAMA.md` (`git diff --stat b881ee6..HEAD`). Ningún archivo del universo de este acto se movió. **Al abrir, `main` se había movido por `[DERIVADOS] 2026-09-16` (`PR #821`), no por `GEN2-M1-ALCANCE-1`** — la previsión de la cabecera del encargo era correcta pero prematura: `GEN2-M1-ALCANCE-1` fusionó **durante** el acto, no antes (ver la fila de concurrencia). |
| **Sync a mitad del acto** | `origin/main` pasó de `10afea1` a `d69eed1` (`PR #822`, `GEN2-M1-ALCANCE-1`, 7 commits) mientras esta sesión escribía. Merge con tres conflictos, los tres del cierre y ninguno sustantivo (`canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_13.md`, `canon/registro-rotulos.tsv`): resueltos conservando **las dos** entradas, la suya primero. Las enmiendas que trajo se **añadieron al final** de cada propuesta, así que **ninguna cita `archivo:línea` de esta nota se desplazó** salvo una, `milpa/src/matriz.py`, re-derivada y corregida (ver `F3`). |
| **Rama** | `claude/admiring-meitner-yghskh` |
| **Entorno** | `python3 tools/entorno.py` → `commit=10afea15e19e · git_status=LIMPIO(0) · python=3.11.15 · numpy=AUSENTE pandas=AUSENTE scipy=AUSENTE yaml=6.0.1 pyreadstat=AUSENTE · CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default · red=no-ejecutada · raices=data_raw:NO · corpus=NO(examinados=0)`. |
| **Microdato** | **Cero payloads abiertos.** `data/raw` ausente (normal en nube) y el encargo lo declara irrelevante: A.15b — la construibilidad se lee de inventarios, FD y catálogos del repo. Sonda de red no ejecutada: este acto no toca red. |
| **Compuerta** | `ninguna` (declaración explícita del encargo; no dispara verificación). |
| **Contador de mediciones** | **Cero, dicho sin disfraz.** Este acto no mide nada sobre México. Produce diseño. |
| **Concurrencia observada, y cómo cambió a mitad del acto** | **Al abrir:** `GEN2-M1-ALCANCE-1` vivía en `origin/claude/affectionate-sagan-u8484q` (4 commits, `CIERRE · … · ADR-531`), **sin fusionar y sin PR abierto** (`list_pull_requests state=open` → `[]`); por eso no se tocó ninguno de sus archivos y las propuestas se leyeron **como están en `main`**, sin sus enmiendas. **Al cerrar: ya había fusionado** (`PR #822` → `d69eed1`, 7 commits, `ADR-531`). Se aplicó entonces la otra mitad de la instrucción del encargo —«*si al abrir ya fusionó, cita su ADR y lee las propuestas con sus enmiendas*»—: se sincronizó, se **renumeró este ADR de `531` a `532`** (regla de la casa: renumera quien fusiona segundo), y se releyeron las enmiendas. **Dos cosas cambiaron y las dos están asentadas**, con la fecha en que se leyeron: la firma verbatim de `M1` llegó al árbol (§0.3) y `milpa/src/matriz.py::g()` quedó corregida (`F3`, `P4 §4.1`). Ninguna mueve `P1`. |

### 0.1 · Archivos examinados por pieza, con conteo (A.13)

| pieza | archivos / filas examinados | comando |
|---|---|---|
| **A.8 (2)** re-verificación | **2 133** archivos `.md`+`.tsv` | `find . -path ./.git -prune -o \( -name "*.md" -o -name "*.tsv" \) -print \| wc -l` |
| **P1 · celdas-D** | **3** archivos | `ls data/curacion-registro/celdas-d/ \| wc -l` |
| **P1 · árbitro** | **1** archivo, **4 111** líneas, **7** entradas `_ejes_` | `grep -c "^  - id: .*_ejes_" milpa/tramite-ola5-propuesta-v0.yaml` |
| **P1 · momentos** | **22** filas de datos, **12** columnas | `milpa/catalogo-momentos-v0_1.tsv` + `.md` (146 líneas) |
| **P1 · demanda** | **207** filas de datos; **42** `conducta_p_medido` | `data/corrida0/demanda-resultados.tsv` |
| **P1 · crosswalk** | **15** filas de datos | `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv` |
| **P1 · manifiesto** | **30 065** líneas | `data/manifiesto.yaml` |
| **P1 · inventario (A.15a)** | **178 246** filas de datos, cabecera en `:10` | `data/inventario-reactivos-v1_2.tsv` (vigente; **no** v1_0/v1_1) |
| **P1 · motor** | `milpa/tramite.yaml` (1 458 líneas), `milpa/src/celdas.py` (110) | lectura completa de los bloques citados |
| **P3** | `forense/hallazgos.md` (**846** líneas), v0.3 (224), v0.5 (159), `RONDA1-…-fable-…` (131), `CAREO-ADV-DUELO-…` (56) | lectura completa |
| **P4** | `propuesta-motor-matriz-v0_1.md` (231), `catalogo-momentos-v0_1.md`/`.tsv`, `milpa/src/pi.py` (94), `milpa/src/matriz.py` (176), `milpa/src/momentos.py` (134) | lectura completa |

### 0.2 · Dos correcciones a la cabecera del encargo, derivadas por comando

1. **A.8 (2) reproduce, con un archivo más — el propio encargo archivado.**
   `grep -rln "CELDA-D-PILOTO\|piloto celda-D\|piloto de celda-D" --include=*.md --include=*.tsv .`
   devuelve hoy **2** archivos: `PROPUESTA-remediacion-brecha-documental.md` (el que
   dirección midió) y `forense/encargos/2026-09-17-GEN2-CELDA-D-DISENO-CIEGO-1-SEGUNDO-DISENO-INDEPENDIENTE.md`
   (creado por el 0-bis de este acto, commit `1c7796c`). El `NO-ENCONTRADO` de
   dirección **se sostiene**: no existe diseño del primer piloto celda-D en el árbol.

2. **A.8 (3) es impreciso en la letra y se corrige aquí sin reescribirlo.** El encargo
   dice «nunca ha corrido una celda con ≥2 candidatos ejecutables». Medido:
   `G5.radio_confianza.encuci_vs_enbiare.yaml` tiene **dos candidatos y los dos
   corrieron** — `BASELINE`/ENCUCI con `resultado: "vigente — MEDIDO·PARCIAL(formalidad,
   edad, dominio)…"` (`:83`) y `CHALLENGER`/ENBIARE con `resultado: "EJECUTADO —
   ENCARGO 9 (13/ago/2026)…"` (`:106`). Lo que **nunca ha ocurrido** es lo otro, y es
   lo que importa: **ninguna celda-D se ha adjudicado por competencia de estimadores
   contra una evaluación**. Esa celda se cerró con un acto de **vinculación-invarianza**
   (`criterio_adjudicacion.escala: "INVARIANZA PARCIAL — configural sostenida…"`,
   `:131`) y `champion_actual` **no cambió** (`:139`). Y las **tres** celdas-D del
   registro traen `momentos_holdout_refs: []` — vacío (`:69`, `:111`, `:138`
   respectivamente). Sin holdout no hay evaluación, con o sin dos candidatos.
   La corrección importa para el careo: el hueco no es «dos candidatos», es
   «una evaluación».

### 0.3 · Reserva sobre la firma de mesa (se declara, no se resuelve aquí)

El encargo trae la **FIRMA DE MESA** como marcador literal sin sustituir:
`[FIRMA M1 — A o B]`. El texto verbatim de mesa **no llegó**. Lo que sí llegó, y es
lo que este acto toma como gobernante, es la sustancia que el propio encargo
escribe en la línea siguiente:

> «cada celda tiene su estimador, su ruta y su dato; el motor no tiene un
> estimador único; la matriz compone y, donde compita, es un candidato más —
> nunca el estimador por defecto.»

No es PARO: los dos PARO que el encargo declara son (i) que mesa pegue el diseño de
dirección y (ii) escribir fuera del perímetro. Ninguno ocurrió. Todo `P1`–`P4` se escribió
contra esa paráfrasis, no contra la firma.

> **RESERVA RESUELTA A MITAD DEL ACTO, y se dice cómo.** `GEN2-M1-ALCANCE-1` fusionó
> (`PR #822`, `ADR-531`) mientras este acto corría, y **trajo el verbatim al árbol**. La
> firma de mesa del 17/sep/2026 sobre `M1`, citada verbatim en la enmienda fechada que ese
> acto estampó sobre las propuestas
> (`propuesta-motor-adaptativo-celda-v0_5.md:164`, `propuesta-motor-matriz-v0_1.md:236`) y
> asentada en `forense/hallazgos.md:847` como `PARA-v2.14`, dice:
>
> > «*el cómputo matricial es la forma de **composición** del ejecutable, no el estimador
> > de ninguna celda. La estimación de cada insumo la gobierna el contrato celda-D
> > (`ADR-68`); la matriz compite en él como **candidato**, nunca por defecto.*»
>
> **Coincide en sustancia con la paráfrasis contra la que se escribió este diseño** — «la
> matriz compone y, donde compita, es un candidato más — nunca el estimador por defecto».
> `ADR-91` **no se revoca**: la firma del 17/ago (*«cómputo matricial como definición del
> ejecutable»*) sigue en pie y lo que se precisa es su **alcance**. Nada de `P1`–`P4`
> cambia por esta lectura, y se declara que se hizo **después** de escribirlos: el orden
> importa para el careo. La reserva sobrevive sólo en su forma débil — el marcador
> `[FIRMA M1 — A o B]` del encargo sigue sin decir cuál de las dos opciones («A» o «B»)
> eligió mesa, y este acto **no lo infiere**.

---

## P1 · Elegir la primera celda-D — y por qué no las otras

### 1.1 · El universo, derivado por comando (no heredado)

**(i) Las tres celdas-D registradas** — `ls data/curacion-registro/celdas-d/` → **3**:

| id | `tipo_adjudicacion` | candidatos | `diseno_datos` | `momentos_holdout_refs` | `champion_actual` |
|---|---|---|---|---|---|
| `G5.familismo_obligacion.actitud` | `CALIBRACION_CONJUNTA` | **1** (`BASELINE`/ENASIC) | `transversal` | `[]` | `BASELINE.ENASIC` |
| `G5.obligacion_medida.conducta` | `CALIBRACION_CONJUNTA` | **1** (`BASELINE`/ENASIC) | `transversal` | `[]` | `BASELINE.ENASIC` |
| `G5.radio_confianza.encuci_vs_enbiare` | `COMPARACION` | **2** (`BASELINE`/ENCUCI, `CHALLENGER`/ENBIARE) | `transversal`, `transversal` | `[]` | `BASELINE.ENCUCI` |

Las tres declaran `vocabulario_version: 0.4` — ninguna es del piloto ADV-DUELO
(`propuesta-motor-adaptativo-celda-v0_5.md:43`, `:108`).

**(ii) Las entradas del árbitro con puntos por eje** —
`grep -c "^  - id: .*_ejes_" milpa/tramite-ola5-propuesta-v0.yaml` → **7**:

| # | id (`milpa/tramite-ola5-propuesta-v0.yaml:<línea>`) | payload | ejes (celdas) |
|---|---|---|---|
| 1 | `dinero.ahorro.via_informal_ejes_enif2024` `:1415` | `enif_2024_enif_2024_bd_csv` | sexo, edad, escolaridad, localidad, formalidad, cuenta_formal — **×2 desenlaces** (principal `:1426`, secundario `:1499`) |
| 2 | `tramite.gobierno_digital.util_sin_coercion_ejes_encig2025` `:1600` | `encig25_base_datos_csv` | sexo `:1611`, edad `:1621`, escolaridad `:1633` |
| 3 | `tramite.evasion_norma_ejes_envipe2025` `:1672` | `envipe2025_csv` | sexo `:1683`, edad `:1693`, escolaridad_proxy `:1705`, dominio_urbano_rural `:1719` |
| 4 | `civico.denuncia.con_seguro_ejes_envipe2025` `:1993` | `envipe2025_csv` | cobertura_seguro `:2003` |
| 5 | `familia.union.libre_ejes_eder2017` `:2041` | `eder_2017_eder2017_bases_csv` | cohorte_nacimiento `:2051` |
| 6 | `familia.cuidado.reparto_mujeres40_ejes_enut2024` `:2089` | `enut2024_bd_csv` | reparto_hogar `:2100`, sexo_edad `:2115` |
| 7 | `dinero.ahorro.horizonte_corto_ejes_enif2024` `:2159` | `enif_2024_enif_2024_bd_csv` | formalidad `:2170` |

Total de celdas del árbitro: **74**, de las cuales **64 con IC95** — reconciliado en
`data/crosswalk-ejes-arbitro-modelo-v1_0.tsv:5-7` contra
`RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC = 74` (`NC-0241`). Suma verificada aquí sobre la
columna `n_celdas_total_arbitro` del crosswalk: 6+4+3+16+12+4+8+10+4+4+2+1 = **74**.

**(iii) El catálogo de momentos** — `milpa/catalogo-momentos-v0_1.tsv`: **22** filas,
**12** columnas, `rol_calibracion` = 8 `AJUSTE` / 14 `HOLDOUT`. Y los tres valores que
deciden todo lo demás, constantes en las 22 filas:
`universo_candidatos = "POR DECLARAR (ADR-68(a)…)"` **22/22**,
`instrumentos_candidatos = "POR DECLARAR"` **22/22**,
`estatus_disponibilidad = "NO-VERIFICADO"` **22/22**.

**(iv) La demanda activa** — `data/corrida0/demanda-resultados.tsv`, **207** filas de
datos, **42** de tipo `conducta_p_medido`, **21** reglas distintas. Cruzadas contra (ii):
**14** filas pertenecen a una regla con entrada `_ejes_` del árbitro; **28** no.
`escala_legacy` de las 42: **22** `p (proporcion ponderada)` · **15**
`NO-DECLARADO-EN-EL-REGISTRO` · **3** `ecologica` · **2** una escala larga propia.

### 1.2 · Los siete criterios, operacionalizados antes de aplicarlos

| | criterio | cómo se decide, y contra qué archivo |
|---|---|---|
| **(a)** | estimando con **escala y universo declarados** | escala: columna `escala_legacy` de la fila de demanda (`demanda-resultados.tsv`) — la columna que el registro tiene **para eso**; un número de escala enterrado en `clase_legacy` no la sustituye (mismo criterio que `propuesta-motor-adaptativo-celda-v0_5.md:69` impone a `margen_material` frente a `criterio_adjudicacion.texto`). Universo: campo `universo:` de la entrada del árbitro. |
| **(b)** | población **expresable en cortes del modelo y en celdas del árbitro** | `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv`, con su propia regla de admisión, verbatim `:4`: «`firma` vacia = PROPUESTA A MESA, sin firmar. **Una fila sin firma NO autoriza consumo por el marcador.**» Cortes del modelo: `milpa/src/celdas.py:74-81` (`CORTES_C1`). |
| **(c)** | dato **y su ola anterior** ya en `data/manifiesto.yaml` | `grep -n "^- id: <payload>"` sobre las 30 065 líneas |
| **(d)** | **≥2 candidatos elegibles de familias distintas** | «elegible» = **ejecutable hoy**, la lectura que el propio encargo fija en su A.8 (3) («≥2 candidatos ejecutables»). Familias: persistencia · matriz (`estrategia: momentos`) · `L` · medición transversal directa. |
| **(e)** | **persistencia construible** (A.15a) | `data/inventario-reactivos-v1_2.tsv` (vigente, **nunca** v1_0/v1_1), patrón sobre `variable_id` y conteo de filas del payload de la ola anterior |
| **(f)** | **consumidor identificado** en la demanda | columna `consumidor` de la fila `conducta_p_medido` |
| **(g)** | **evaluación no vista por el candidato evaluado** | dos lecturas, ambas aplicadas abajo — ver §1.5 |

Dos notas de método, declaradas antes de la tabla:

- **La medición transversal directa sobre la ola del árbitro queda fuera como
  candidato por construcción**: sería el árbitro mismo. Es el paréntesis del propio
  encargo («medición transversal directa **si no es circular con el árbitro**») y
  coincide con el grado `P0` de `ADV1-M1` (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:34`:
  «P0 (misma encuesta+ola que parametrizó `M`) **fuera del marcador**, a anexo de plomería»).
- **La matriz no es candidato ejecutable hoy, para ninguna celda.** No es juicio:
  `milpa/src/momentos.py:130` levanta `NotImplementedError` al pedir el valor de un
  momento; `milpa/src/pi.py:68-69` levanta `FuentePiPendiente` con el texto «π(x) no
  tiene hoy fuente cargable»; y `propuesta-motor-matriz-v0_1.md:79` declara que la
  forma de `h_r` «es justo lo que `D-ABC` dejó pendiente y ADR-65 probó que no se lee
  de las curvas». Entra en P2 como challenger con su lista de faltantes — pero **no
  cuenta** para satisfacer (d).

### 1.3 · Criterio (b) — el crosswalk, fila por fila

De las **15** filas de `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv`, **12** son
`ARBITRO->MODELO` y **3** son `MODELO->ARBITRO` (cortes sellados sin un solo punto del
árbitro: `ingreso` `:21`, `acceso_digital` `:22`, `migracion` `:23`).

| eje del árbitro | celdas | veredicto | `firma` | ¿autoriza consumo? |
|---|---|---|---|---|
| `formalidad` `:9` | 6 | `MAPEO-N-A-1` | **F-17 (mesa, 16/sep/2026, NC-0240)** | **SÍ** |
| `localidad` `:10` | 4 | `MAPEO-N-A-1` | *(vacía)* | **NO** |
| `dominio_urbano_rural` `:11` | 3 | `NO-EQUIVALENTE` | *(vacía)* | NO |
| `edad` `:12` | 16 | `PENDIENTE-FP-53` | *(vacía)* | NO |
| `escolaridad` `:13` | 12 | `SIN-CORRESPONDENCIA` | *(vacía)* | NO |
| `escolaridad_proxy` `:14` | 4 | `SIN-CORRESPONDENCIA` | *(vacía)* | NO |
| `sexo` `:15` | 8 | `SIN-CORRESPONDENCIA` | *(vacía)* | NO |
| `sexo_edad` `:16` | 10 | `SIN-CORRESPONDENCIA` | *(vacía)* | NO |
| `cuenta_formal` `:17` | 4 | `SIN-CORRESPONDENCIA` | *(vacía)* | NO |
| `cohorte_nacimiento` `:18` | 4 | `SIN-CORRESPONDENCIA` | *(vacía)* | NO |
| `cobertura_seguro` `:19` | 2 | `SIN-CORRESPONDENCIA` | *(vacía)* | NO |
| `reparto_hogar` `:20` | 1 | `SIN-CORRESPONDENCIA` | *(vacía)* | NO |

**Un solo eje de los doce autoriza consumo: `formalidad`, y con mapeo N-a-1.** De las
74 celdas del árbitro, **6** (8.1%) caen sobre un corte del modelo por una fila firmada.

**Qué resolución se pierde en los `MAPEO-N-A-1`** (la pregunta explícita del encargo):

- **`formalidad`** (`:9`, la firmada) — **no** colapsa celdas (2 contra 2), pero pierde
  tres cosas que el crosswalk enumera y que un diseño debe cargar: (i) **instrumento y
  variable distintos** — `P3_13` de ENIF, no `segsoc` de ENIGH; (ii) **7 códigos nativos
  colapsados a 2**; (iii) **universo restringido**: el eje del árbitro excluye a quien no
  trabaja — cobertura `0.689676` en `via_informal` y `0.668937` en `horizonte_corto`, con
  `universo_restringido: true` escrito en el propio yaml
  (`milpa/tramite-ola5-propuesta-v0.yaml:1476`) y la cita de **A-bis 4** al lado. Y una
  cuarta, que es de constructo y no de resolución: **`segsoc` es derechohabiencia por
  cualquier vía; `P3_13` pregunta por servicio médico *por parte de su trabajo*** — quien
  es derechohabiente por su cónyuge es `segsoc=1` y `P3_13=7`. Es decir: la fila firmada
  mapea dos particiones de igual cardinalidad que **no parten a la misma gente**.
- **`localidad`** (`:10`, sin firma) — pierde **la mitad de la resolución del eje**:
  4 celdas selladas del modelo (`tam_loc` 1/2/3/4) colapsan a 2. El marcador no puede
  distinguir `tam_loc=1` (100 000+) de `tam_loc=2` (15 000–99 999), ni `tam_loc=3` de
  `tam_loc=4`. Las 4 celdas del árbitro caen sobre 2 coordenadas, no sobre 4. Sin firma,
  además, **no entra**.

### 1.4 · Criterios (c) y (e) — manifiesto y persistencia, medidos

**(c) Dato y ola anterior en `data/manifiesto.yaml`** — los diez `id` citados por línea:

| ola del árbitro | `manifiesto.yaml` | ola anterior | `manifiesto.yaml` |
|---|---|---|---|
| ENIF 2024 | `enif_2024_enif_2024_bd_csv` `:5543` · `enif2024_csv` `:214` | ENIF 2021 | `enif2021_csv` `:201` |
| ENCIG 2025 | `encig25_base_datos_csv` `:4330` | ENCIG 2023 | `encig23_base_datos_csv` `:28` |
| ENVIPE 2025 | `envipe2025_csv` `:325` | ENVIPE 2024 | `envipe2024_csv` `:311` |
| EDER 2017 | `eder_2017_eder2017_bases_csv` `:4440` | EDER 2011 | `eder_2011_eder2011_bases_dbf` `:4382` |
| ENUT 2024 | `enut2024_bd_csv` `:3186` | ENUT 2019 | `enut2019_bd_csv` `:3105` |

**(c) pasa 7 de 7.** Tener el zip de la ola anterior, sin embargo, no es tener el
reactivo — que es exactamente lo que (e) pregunta.

**(e) Persistencia construible (A.15a)** — inventario vigente
`data/inventario-reactivos-v1_2.tsv` (cabecera en `:10`, **178 246** filas de datos),
patrón `fullmatch` sobre `variable_id`, conteo de filas del payload declarado:

| candidato | reactivo que define el desenlace / el eje | ola del árbitro | **ola anterior** | veredicto |
|---|---|---|---|---|
| 1 · `via_informal` | `P5_1_1..6` ∧ ninguna `P5_6_1..9` (`:1426`) | 2024: 6/6 y **9/9** (1 726 filas) | 2021: 6/6 y **7/9** — faltan `P5_6_6`, `P5_6_7` (1 607 filas) | **NO** — el desenlace cambia de definición |
| 1,7 · eje `formalidad` | `P3_13` | 2024: **1** acierto | 2021: **0** aciertos sobre 1 607 filas (ENIF 2021 cierra en `P3_11`) | **NO** |
| 7 · `horizonte_corto` | `P4_10` (`:2164`) | 2024: 1 | 2021: **1** | sí para el marginal; **NO** para la celda segmentada, por `P3_13` |
| 2 · `util_sin_coercion` | `P7_3` (`:1605`) | 2025: 1 (954 filas) | 2023: **1** (2 337 filas) | **SÍ** |
| 3 · `evasion_norma` | `BP1_20`, `BP1_23` (`:1672`) | 2025: 2/2 (2 987 filas) | 2024: **2/2** (2 902 filas) | **SÍ** |
| 4 · `denuncia.con_seguro` | `BPCOD`, `BP2_1` (`:1998`) | 2025: 2/2 | 2024: **2/2** | **SÍ** |
| 5 · `union.libre` | `edo_civil1`, `anio_retro` (`:2046`) | EDER 2017: 2/2 (864 filas, `historiavida.csv`) | EDER 2011: **0/2** sobre **270** filas; miembros `eder2011_antecedentes/caratula/tablaretro` — **no existe `historiavida`** | **NO** |
| 6 · `reparto_mujeres40` | agregados de `tvar_crea.csv` (`:2093`) | ENUT 2024: `tvar_crea.csv` presente (60 filas) | ENUT 2019: miembros `THOGAR/TMODULO/TSDEM/TVIVIENDA` — **`tvar_crea` no existe** | **NO** |

La última fila tiene, además, respaldo documental propio del árbol:
`forense/hallazgos.md:421` mide que **ENUT no es una serie sino tres instrumentos**
(«2014-2019 con 11 ítems y filtro de una condición; 2024 con 14 ítems y filtro de dos»),
y que 2002/2009 «**no** son reconstruibles al esquema 2014-2024 sin perder» información.
Y el mismo hallazgo mide el defecto gemelo en ENVIPE — el mnemónico cambia de constructo
entre olas — que es la razón por la que (e) se verifica **por archivo y por código**,
no por nombre de variable (A.15c).

### 1.5 · Criterio (g) — la evaluación y quién ya la vio

El encargo fija el ancla: **`U3` ya fue observada: no cuenta.** `U3` es la intersección
de 14 celdas del duelo (`forense/prereg-duelo-v2/F5-contrato-triada-spec-v1_1.md:104-113`,
`UR` cerrado en 14/14 `:93-95`), y sus errores están publicados por celda
(`forense/prereg-duelo-v2/scoreboard-v1_3-AGREGADO.md`, tabla §1, `z = (corredor − R)/EE_R`).
Sus olas son ENVIPE 2012/13/15/21/23/24 · ENNViH 2002 · ENIF 2018 · ENIGH 2016/18/20 ·
ENCUCI 2020 · ENCIG 2013/2021 (`universo-triada-v1_4.tsv`, 14 filas). **Ninguna de las 7
entradas del árbitro cae en esas olas** — así que la exclusión nominal de `U3` no elimina
a ninguna por sí sola. El problema es otro, y es peor.

**Medido: las 7 entradas del árbitro son la fuente de la que el motor copió su número.**
No es que `M` «haya visto» la evaluación: en cinco de las siete, la evaluación **está
dentro de `milpa/tramite.yaml`**, verbatim.

| # | entrada `_ejes_` | payload del árbitro | fila de demanda del motor | payload del motor | dónde vive la evaluación dentro del motor |
|---|---|---|---|---|---|
| 1 | `via_informal` | `enif_2024_enif_2024_bd_csv` | `RES-0057`/`RES-0058` | `enif_2024_enif_2024_bd_csv` | `milpa/tramite.yaml:708` `segmentacion_ejes_enif2024`, `:712` **«copiada verbatim»** |
| 2 | `util_sin_coercion` | `encig25_base_datos_csv` | `RES-0021`/`RES-0022` | `encig25_base_datos_csv` | `milpa/tramite.yaml:437` `segmentacion_ejes_encig2025` |
| 3 | `evasion_norma` | `envipe2025_csv` | `RES-0025`/`RES-0026` | `envipe2025_csv` | `milpa/tramite.yaml:537` `segmentacion_ejes_envipe2025` |
| 4 | `denuncia.con_seguro` | `envipe2025_csv` | `RES-0039`…`RES-0042` | `envipe2025_csv` | `milpa/tramite.yaml:1026` universo **«copiado de la entrada `civico.denuncia.con_seguro_ejes_envipe2025`»** |
| 5 | `union.libre` | `eder_2017_eder2017_bases_csv` | `RES-0043`/`RES-0044` | `eder_2017_eder2017_bases_csv` | `milpa/tramite.yaml:1047` `segmentacion_ejes_eder2017_enadid2023`; `ola_calibracion: "EDER 2017 … + ENADID 2023"` `:1042` |
| 6 | `reparto_mujeres40` | `enut2024_bd_csv` | `RES-0045` | `enut2024_bd_csv` | `milpa/tramite.yaml:1106` `segmentacion_ejes_enut2024` |
| 7 | `horizonte_corto` | `enif_2024_enif_2024_bd_csv` | `RES-0046`/`RES-0048` | `enif_2024_enif_2024_bd_csv` | `ola_calibracion: "ENIF 2024"` `milpa/tramite.yaml:1142` |

Dos comprobaciones numéricas, para que no quede en afirmación:

- **`denuncia.con_seguro`.** Celdas del árbitro (`:2012-2013`): no asegurado
  `p = 0.672014`, asegurado `p = 0.790906`. Filas del motor: `RES-0041` (`sin_seguro:
  denuncia`) `= 0.672`, `RES-0039` (`con_seguro: denuncia`) `= 0.7909`. **Las «dos celdas
  del árbitro» y las «dos reglas del motor» son el mismo par de números.**
- **`horizonte_corto`.** Sensibilidad pre-declarada del árbitro `P4_10∈{1,2}`
  (`:2186-2187`): sin seguridad social `54.13%`. Motor: `RES-0046 = 0.541343`
  (`milpa/tramite.yaml:1129`). **Identidad al cuarto decimal.**

Esto es el grado **`P0`** de `ADV1-M1` en su forma extrema — no «misma encuesta+ola»,
sino **mismo número**. Bajo el filtro que el careo ya selló, va «fuera del marcador, a
anexo de plomería» (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:34`).

**Las dos lecturas de (g), y por qué el resultado no depende de cuál se elija.**

- **Lectura estricta** (la que este diseño aplica): la evaluación debe ser invisible para
  el candidato evaluado; P2 obliga a que la matriz —el motor— sea uno de los candidatos;
  el motor **es** la evaluación. **(g) falla en las 7.**
- **Lectura débil**: (g) sólo excluye las 14 celdas de `U3` por nombre; las 7 entradas
  no son `U3`. **(g) pasa en las 7.**

Se aplican las dos en la tabla de eliminación. **Bajo ninguna de las dos pasa una sola
celda los siete criterios** — el hallazgo no depende de la interpretación.

### 1.6 · Tabla de eliminación

`✓` pasa · `✗` falla · `(g)!` = falla sólo bajo lectura estricta.

| candidato | (a) escala+universo | (b) crosswalk firmado | (c) manifiesto | (d) ≥2 familias | (e) persistencia | (f) consumidor | (g) evaluación no vista | veredicto |
|---|---|---|---|---|---|---|---|---|
| **1 · `via_informal_ejes_enif2024`** | ✗ `RES-0057/0058` escala `NO-DECLARADO-EN-EL-REGISTRO` | ✓ `formalidad` F-17 | ✓ | ✗ sólo `L` | ✗ faltan `P5_6_6/7` en 2021 | ✓ | `(g)!` | **ELIMINADA** (4 fallos) |
| **2 · `util_sin_coercion_ejes_encig2025`** | ✗ `RES-0021/0022` `NO-DECLARADO` | ✗ sexo/edad/escolaridad: `SIN-CORRESPONDENCIA` y `PENDIENTE-FP-53` | ✓ | ✓ persistencia + `L` | ✓ `P7_3` en 2023 | ✓ | `(g)!` | **ELIMINADA** (3 fallos) |
| **3 · `evasion_norma_ejes_envipe2025`** | ✗ `RES-0025/0026` `NO-DECLARADO` | ✗ `dominio_urbano_rural` = `NO-EQUIVALENTE`; resto sin corte | ✓ | ✓ | ✓ `BP1_20/23` en 2024 | ✓ | `(g)!` | **ELIMINADA** (3 fallos) |
| **4 · `denuncia.con_seguro_ejes_envipe2025`** | ✓ `p (proporcion ponderada)` | ✗ `cobertura_seguro` `SIN-CORRESPONDENCIA` | ✓ | ✓ | ✓ `BPCOD`,`BP2_1` en 2024 | ✓ | `(g)!` | **ELIMINADA** (2 fallos) — **la más cercana** |
| **5 · `union.libre_ejes_eder2017`** | ✓ | ✗ `cohorte_nacimiento` `SIN-CORRESPONDENCIA` | ✓ | ✗ | ✗ EDER 2011 sin `historiavida` | ✓ | `(g)!` | **ELIMINADA** (4 fallos) |
| **6 · `reparto_mujeres40_ejes_enut2024`** | ✓ | ✗ `reparto_hogar` no es eje de segmentación; `sexo_edad` sin corte y **sin IC** (10/10) | ✓ | ✗ | ✗ ENUT 2019 sin `tvar_crea` | ✓ | `(g)!` | **ELIMINADA** (4 fallos) |
| **7 · `horizonte_corto_ejes_enif2024`** | ✓ `RES-0046` `p (proporcion ponderada)` | ✓ `formalidad` F-17 | ✓ | ✗ sólo `L` | ✗ `P3_13` ausente en ENIF 2021 | ✓ | `(g)!` | **ELIMINADA** (3 fallos) — **la segunda más cercana** |
| **8 · `G5.familismo_obligacion.actitud`** | ✓ `output_nativo.escala` `:78`, `poblacion_objetivo` `:38` | ✗ ENASIC no aparece en ninguna de las 7 entradas del árbitro | n/a | ✗ **1** candidato | ✗ no evaluada | ✗ `RES-0171`: el consumidor es el propio archivo de celda, no una regla del motor | ✗ `momentos_holdout_refs: []` `:69` | **ELIMINADA** |
| **9 · `G5.obligacion_medida.conducta`** | ✓ `:118`, `:68` | ✗ ENASIC fuera del árbitro | n/a | ✗ **1** candidato | ✗ | ✗ `RES-0172`, ídem | ✗ `[]` `:111` | **ELIMINADA** |
| **10 · `G5.radio_confianza.encuci_vs_enbiare`** | ✓ `:148`, `:31` | ✗ ENCUCI/ENBIARE fuera del árbitro | n/a | ✗ 2 candidatos, **ambos `transversal`** — misma familia | ✗ | ✗ `RES-0173`, ídem | ✗ `[]` `:138` | **ELIMINADA** |
| **11 · los 22 momentos `M01`–`M22`** | ✗ el catálogo **no tiene columna `escala`** (12 columnas, ninguna); `universo_candidatos = POR DECLARAR` 22/22 | ✗ sin instrumento no hay eje | ✗ `estatus_disponibilidad = NO-VERIFICADO` 22/22 | ✗ `instrumentos_candidatos = POR DECLARAR` 22/22 | ✗ | parcial | ✗ `valor_de()` levanta `NotImplementedError` (`milpa/src/momentos.py:130`) | **ELIMINADOS en bloque en (a)** |
| **12 · las otras 28 filas `conducta_p_medido`** | mixto | ✗ **ninguna** tiene entrada `_ejes_` del árbitro: cero celdas del árbitro | ✓ | ✗ | — | ✓ | — | **ELIMINADAS en bloque en (b)** |

### 1.7 · Veredicto de P1

> **NINGUNA de las candidatas del universo obligatorio pasa los siete criterios.**
> Ese es el hallazgo, y por instrucción explícita del encargo **P2 no se escribe.**

El resultado se sostiene bajo las dos lecturas de (g): incluso ignorando (g) por
completo, la mejor candidata (`civico.denuncia.con_seguro_ejes_envipe2025`) sigue
fallando **(b)**, y la única con (b) firmado (`dinero.ahorro.horizonte_corto_ejes_enif2024`)
sigue fallando **(d)** y **(e)**.

**Los dos huecos son complementarios, y esa es la forma exacta del hallazgo:**

1. **Nadie tiene puente de población firmado *y* línea base ingenua construible a la vez.**
   Las únicas dos celdas con puente firmado (`formalidad`, F-17) son las dos de ENIF 2024,
   y **`P3_13` no existe en ENIF 2021** — el eje que las conecta con el modelo es
   precisamente el que no se puede persistir. Las tres con persistencia construible
   (ENCIG 2025, ENVIPE 2025 ×2) segmentan por ejes que el modelo **no tiene**.
2. **Nadie tiene una evaluación que el motor no haya consumido ya.** Las 7 entradas del
   árbitro *son* la calibración del motor, cargadas verbatim, con dos identidades
   numéricas comprobadas arriba.

**Lo que cambiaría el veredicto, nombrado y con dueño** (ninguna de estas cuatro es
decisión de este acto):

| # | qué falta | quién lo puede cerrar | costo declarado |
|---|---|---|---|
| **i** | Firmar `localidad` en el crosswalk (hoy `MAPEO-N-A-1` **sin firma**, `:10`) | mesa, sobre `FP-376` | cero medición; una firma sobre una fila ya escrita — y aceptar que el marcador pierde la mitad de la resolución del eje |
| **ii** | Sellar el corte de `edad` (`PENDIENTE-FP-53`, `:12`; `milpa/src/celdas.py:77`) | acto propio con dato mexicano; `FP-53` ya firmada con la convención **15-29**, su mitad empírica en cola | desbloquea **16** celdas del árbitro — el bloque más grande. **Aviso ya escrito en el crosswalk `:12`: `18-29` del árbitro *no* será equivalente a `15-29`** |
| **iii** | Una ola de árbitro **posterior** a la calibración del motor (ENIF 2027, ENVIPE 2026, ENCIG 2027…) o una ola **retenida** parametrizando con la vieja | `ADV1-M1(v)` ya lo pide: «≥3-5 celdas post-corte u ola-retenida» (`CAREO…:34`) | es la única vía que arregla (g) sin cambiar de universo |
| **iv** | Declarar la escala en `escala_legacy` de las 15 filas `NO-DECLARADO-EN-EL-REGISTRO` | acto de registro; **no** de medición | arregla (a) en tres de las siete |

**La vía más corta a un primer piloto real es (iii) sobre la candidata 7**
(`horizonte_corto`): es la única que ya tiene (a), (b) firmado, (c) y (f); le faltan
(d)/(e) —que (iii) no arregla— y (g). Un pre-registro honesto de esa celda exige, antes,
resolver cómo se construye `P3_13` en la ola anterior o aceptar una línea base ingenua
**no segmentada**, que es una celda distinta de la que (b) autoriza.

---

## P2 · Pre-registro de la celda elegida — **NO SE ESCRIBE**

Instrucción literal del encargo, pieza P1: *«Si ninguna pasa los siete, ese es el
hallazgo y P2 no se escribe.»* P1 cierra con **ninguna**. Por tanto **no hay YAML de
pre-registro, no hay criterio de adjudicación, no hay umbral, no hay lista de
candidatos y no se adopta ni se rechaza `skill = 1 − error/error(b)`** en este acto.

Escribirlo de todos modos sería fabricar el objeto que P1 acaba de medir que no existe
— y el careo perdería exactamente lo que este acto vale: saber si dos diseños
independientes encontraron o no el mismo suelo.

**Lo que sí queda asentado para el sucesor, sin instanciar P2:** las cuatro
condiciones (i)–(iv) de §1.7, la reserva de la firma de mesa (§0.3), y el hecho de que
el vocabulario de contrato **sí está listo** para recibir la celda cuando exista —
`rol: BASELINE_INGENUO` (`propuesta-motor-adaptativo-celda-v0_5.md:38`), `ENSAMBLE`
(`:39`), `estado_decidibilidad` con sus cinco valores (`:54`), `margen_material`
opcional (`:64`), `variante_corredor` para las dos dietas de `L` (`:41`). El cascarón
está listo; lo que no existe es la celda. Es, palabra por palabra, la conclusión
peligrosa que la propia v0.5 se anticipó a marcar en su módulo de auditoría (`:130`):
*«el cascarón queda listo para recibirlas, que es distinto de estar poblado.»*

Una sola pieza de P2 se conserva aquí, porque P1 la produjo y no la inventa: **las dos
condiciones `INDECIDIBLE` de `ADV1-M3`, citadas verbatim** de
`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:38` — para que el careo pueda
compararlas contra las que el diseño de dirección haya adoptado:

> **«INDECIDIBLE si ambos caen dentro del IC de R o si |d_L−d_M| < 0.5·EE(R).»**

Son **disyuntivas** (basta una), y `propuesta-motor-adaptativo-celda-v0_5.md:57` ya
advierte por escrito el modo de falla: aplicar sólo la segunda deja sin marcar el caso
en que ambos aciertan dentro del intervalo del árbitro pero su distancia entre sí no es
pequeña frente a `EE(R)` — y **un validador de valor único no puede atraparlo**.

---

## P3 · Adversarial de «cada celda su estimador» como política de motor

Diez modos de falla. Cada uno: **nombre · mecanismo (una frase) · ejemplo mínimo con
números · síntoma observable · mecanismo mínimo que lo atrapa (una regla o un test, no
una capa) · estado en el contrato · cruce con `forense/hallazgos.md`**.

Convención de estado: `YA-PREVISTO` (con cita a v0.3 / v0.5 / el veredicto Fable) ·
`PREVISTO-SIN-MECANISMO` · `NO-PREVISTO`.

### F1 · Selección post-hoc del criterio

- **Mecanismo.** Pre-declarar el criterio *por celda* no impide elegir, celda por celda,
  el criterio que el challenger preferido va a ganar.
- **Ejemplo mínimo con números.** `horizonte_corto` admite dos definiciones del mismo
  desenlace, ambas pre-declaradas en el mismo archivo: `P4_10 = 1` da sin-seguridad-social
  `0.330639` / con `0.173418` (brecha **15.7 pp**), y `P4_10 ∈ {1,2}` da `0.541343` /
  `0.369700` (brecha **17.2 pp**) — `milpa/tramite-ola5-propuesta-v0.yaml:2182-2183` y
  `:2186-2187`. Quien elija la escala después de ver los dos números mueve la brecha
  1.5 pp sin tocar un dato.
- **Síntoma observable.** `criterio_adjudicacion.escala` escrito con fecha posterior al
  primer `resultado` de cualquier candidato de la misma celda.
- **Mecanismo mínimo que lo atrapa.** Un test de una línea sobre historia de git:
  `commit_declaracion` debe ser **ancestro** de todo commit que toque `resultado` en ese
  archivo. El veredicto Fable ya lo pidió como punto 1 del go/no-go
  (`RONDA1-…-fable-…:99`: «`commit_declaracion` anterior en historia de git a todo
  resultado»); hoy **nadie lo verifica**: `tests/test_celdas_d.py` valida esquema, no
  cronología.
- **Estado en el contrato.** **PREVISTO-SIN-MECANISMO** — la fila existe en el go/no-go
  (`:99`) y en la matriz de riesgos («Criterio a la medida», `:71`), y el validador no la
  toca.
- **Cruce con `hallazgos.md`.** `CONCEBIBLE` en su forma pura; pero hay un pariente
  cercano `YA-OCURRIÓ-AQUÍ`: `forense/hallazgos.md:480` mide una condición de gate que **pasó por
  ausencia de mecanismo** (`C: reducción=0.0 pasa=True`) y el módulo lo declaró al correr
  — «no descubierto post-hoc» es mérito del módulo, no del contrato.

### F2 · Comparaciones múltiples

- **Mecanismo.** *n* celdas × *k* candidatos son *n·k* adjudicaciones; sin control de
  error global, los champions falsos esperados crecen linealmente.
- **Ejemplo mínimo con números.** El careo ya midió el caso análogo: con **N=12** y regla
  «≥7», *alguien* gana **≈77%** de las veces bajo igualdad perfecta —
  `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:29`, «ambas demoliciones lo calcularon por
  separado, mismo número». Con el piloto de 10-15 celdas que v0.1 preveía, y α=0.05 por
  celda, el número esperado de adjudicaciones espurias bajo H0 es `12 × 0.05 ≈ 0.6` por
  ronda de un solo contraste — y sube a `~1.8` si cada celda admite tres candidatos.
- **Síntoma observable.** Un go/no-go que cuenta **celdas ganadas** en vez de patrones.
- **Mecanismo mínimo.** La regla ya escrita: «Go/no-go cuenta **patrones**, nunca celdas
  sueltas» (`RONDA1-…-fable-…:68`), más la prohibición de la palabra «supera»
  (`CAREO…:40`). Ninguna capa nueva.
- **Estado en el contrato.** **YA-PREVISTO** — `RONDA1-…-fable-…:68` (riesgo
  «Multiplicidad», severidad Media) y `CAREO…:40` (`ADV1-M4`: el piloto no declara
  ganador). La corrección fina (Holm sobre rebanadas) está **diferida a v2.1 con razón
  escrita** (`CAREO…:26`).
- **Cruce.** `CONCEBIBLE` — el programa aún no ha adjudicado ninguna celda, así que no
  puede haber ocurrido todavía. Es precisamente por qué el mecanismo debe entrar antes
  de la primera.

### F3 · Incoherencia entre celdas — ¿basta `D8`?

- **Mecanismo.** Champions individualmente ganadores pueden ser conjuntamente imposibles:
  cada celda optimiza su propio error y nadie comprueba que los champions compilen.
- **Ejemplo mínimo con números.** El chequeo tipo ADR-30 es exactamente esta prueba, y
  `propuesta-motor-matriz-v0_1.md:65` dice por qué: una configuración donde
  `familismo_obligacion` alto mejore **todos** los desenlaces se rechaza
  (`milpa/procedencia.yaml:629-632`). Bajo la matriz «se vuelve un test de una línea sobre
  signos de columna». Hoy `G5 × familismo_obligacion` carga como
  `CoeficienteSinMagnitud` (`milpa/src/matriz.py:95`, `:119`) y `g()` levanta
  `SinMagnitud` (`:186`) — es decir: **el test de coherencia no puede correr sobre la
  única columna que lo motivó.**
  *(Enmienda propia, 17/sep, tras el merge de `PR #822` a mitad de este acto: `ADR-531`
  corrigió `g()` a `g(matriz, theta, celda, generadores=None)`
  (`milpa/src/matriz.py:138`), de modo que una celda sin magnitud **de un generador que
  nadie pidió** ya no bloquea un cómputo en el que no entra — el defecto era que el
  docstring prometía «celda participante» en singular y el código recorría `B` entera.
  Eso levanta el bloqueo para `G1`, `G2`, `G3`, `G4` y `G6`; **no** lo levanta para `G5`,
  que es la columna que motiva el test de ADR-30. El ejemplo se sostiene, acotado a `G5`.)*
- **Síntoma observable.** Dos champions cuyos signos de columna se contradicen, sin que
  ninguna corrida falle.
- **Mecanismo mínimo.** `D8` con `momentos_holdout_refs` **globales** sellados en el
  commit 1 (`RONDA1-…-fable-…:40`, `propuesta-motor-adaptativo-celda-v0_3.md:102`).
- **¿Basta `D8`? No, y se puede decir con un número.** `D8` es una etapa, no un campo, y
  su insumo son los `momentos_holdout_refs`. Medido: **las 3 celdas-D del disco los
  traen vacíos** (`[]` en las tres) y **`milpa/src/momentos.py:130` levanta
  `NotImplementedError`** al pedir el valor de un momento. `D8` está **declarado y
  desconectado**: 0 de 3 celdas le pueden dar entrada y el lector de momentos no existe.
- **Estado en el contrato.** **PREVISTO-SIN-MECANISMO.** `v0.3 §4` lo nombra como «la
  maquinaria de esta interfaz» (`:102`); el contrato YAML tiene la ranura
  (`momentos_holdout_refs`) y **nada la exige no-vacía** — `tests/test_celdas_d.py` pide
  que la clave exista, no que tenga contenido.
- **Cruce.** `CONCEBIBLE` como incoherencia consumada; `YA-OCURRIÓ-AQUÍ` en su
  precondición: `forense/hallazgos.md:480` («un `C` que pasa por ausencia de mecanismo no es
  evidencia de anti-confusión»).

### F4 · La persistencia como piso insuperable

- **Mecanismo.** Si `B` (persistencia / tasa base de la última ola) gana casi siempre,
  el selector no está eligiendo estimadores: está midiendo inercia, y todo challenger
  entra a una competencia ya decidida.
- **Ejemplo mínimo con números — y aquí no hace falta inventarlo.**
  `forense/hallazgos.md:838`, `ACTO GEN2-B-MARCO`, 14/sep/2026, **medido**:
  `MAE_pp(B) = 0.9229 pp` frente a `M = 4.3073 pp` y `L_CORPUS = 21.3226 pp` sobre el
  mismo universo; **`B` yerra menos que el modelo en 8 de 10 celdas**. Con control
  positivo previo: la observada de cada ola objetivo reproduce el `R` de su celda con
  `Δ = 0.0` exacto, 10/10 — «sólo entonces … es una comparación y no una coincidencia
  de estimandos».
- **Síntoma observable.** `skill = 1 − error/error(B) ≤ 0` en la mayoría de las celdas
  puntuadas.
- **Mecanismo mínimo.** La casilla ya escrita: `ADV1-M5(4)` — «**Ninguno supera a `B`**
  → ninguno utilizable v1; re-tierización dirigida sin coronación»
  (`CAREO…:42`) — más el umbral de resultado `M > B` en ≥2/3 de celdas puntuadas
  (`ADV1-M6`, `CAREO…:44`). Una regla, no una capa.
- **Estado en el contrato.** **YA-PREVISTO** y **ya disparado**: `B` es corredor
  obligatorio del careo (`CAREO…:32`) y `rol: BASELINE_INGENUO` nació en v0.5
  precisamente porque `COMPLEMENTO` no servía — «`B` … **sí compite**, es la vara contra
  la que se mide el skill de todos los demás»
  (`propuesta-motor-adaptativo-celda-v0_5.md:35`).
- **Cruce.** **`YA-OCURRIÓ-AQUÍ`** — `forense/hallazgos.md:838`. Es el modo de falla con
  evidencia propia más fuerte de esta lista.
- **Corolario que el contrato aún no cubre:** `B` también puede **callarse**.
  `forense/hallazgos.md:829`: bajo el corte de disponibilidad que `D-2`/`FP-348` exige, `B` se
  abstiene (`SIN_BASELINE`) en dos de tres objetivos, «y eso es un resultado sobre
  disponibilidad, no sobre persistencia». El contrato **no tiene valor** para «el
  denominador del skill no existe en esta celda» — `estado_decidibilidad` ofrece
  `SKIP:<motivo>`, que es un cajón, no una distinción.

### F5 · Sobreajuste al árbitro — cómo se detecta, no sólo que está prohibido

- **Mecanismo.** El estimador se elige, se afina o se define **mirando** la cantidad
  contra la que se le va a evaluar; el error medido deja de estimar el error futuro.
- **Ejemplo mínimo con números.** Medido en §1.5 de esta nota: la entrada del árbitro
  `civico.denuncia.con_seguro_ejes_envipe2025` publica `no asegurado 0.672014` /
  `asegurado 0.790906` (`:2012-2013`), y el motor consume `0.672` / `0.7909`
  (`RES-0041` / `RES-0039`). **El error del motor contra ese árbitro es, por
  construcción, 0.0000.** Un skill calculado ahí no mide transporte: mide una copia.
- **Síntoma observable.** `|M − R| ≈ 0` con `EE_R > 0`, o `payload_manifiesto_id` del
  candidato **igual** al del árbitro.
- **Mecanismo mínimo que lo atrapa.** **Una comparación de cadenas, no una capa**: para
  cada celda, `payload_manifiesto_id` del candidato ≠ `payload_manifiesto_id` del
  árbitro, o la celda va a `P0` y sale del marcador. La regla ya existe en prosa
  (`ADV1-M1(ii)`, `CAREO…:34`) y el contrato triádico ya tiene el vocabulario
  (`CONTAMINADA-POR-OBJETIVO`, `forense/prereg-duelo-v2/F5-contrato-triada-spec-v1_1.md:136-141`), con su
  advertencia correcta de que la prueba es **la cadena documentada**, no la coincidencia
  de encuesta. Lo que falta es un campo que la cargue en la celda-D.
- **Estado en el contrato.** **PREVISTO-SIN-MECANISMO en la celda-D.** El contrato de
  celda-D **no tiene** ni `payload_manifiesto_id`, ni `grado_dependencia P0/P1/P2`, ni
  `CONTAMINADA-POR-OBJETIVO`: las 24 claves obligatorias de
  `tests/test_celdas_d.py:106-121` no incluyen ninguna. El vocabulario existe en el
  duelo y **no cruzó** al contrato de celda.
- **Cruce.** **`YA-OCURRIÓ-AQUÍ`** — no como sobreajuste consumado, sino en la forma que
  lo hace invisible: `forense/hallazgos.md:837` mide que una anotación semántica correcta para
  ENCIG 2025 es **falsa** para ENCUCI 2020 sobre el mismo constructo, y que el `p` que el
  motor consume quedó **71% por encima** de la tasa de pago efectivo. «El constructo no
  garantiza el instrumento» — y el rótulo de la celda no avisa.

### F6 · Circularidad en corpus de una sola ola

- **Mecanismo.** El estimando, el parámetro y el árbitro salen del mismo levantamiento;
  la comparación no tiene grados de libertad y el error mide la reproducibilidad del
  cómputo, no la calidad del estimador.
- **Ejemplo mínimo con números.** `dinero.ahorro.via_informal`: el desenlace
  (`P5_1_*`/`P5_6_*`), el eje (`P3_13`), el ponderador (`FAC_PER`) y el árbitro salen
  **todos** de `TMODULO.csv` de ENIF 2024, un solo payload
  (`sha256 00e4b0b42775…`, `milpa/tramite.yaml:1173`, idéntico al `sha256_payload` de la
  entrada del árbitro). Y el eje `cuenta_formal` de esa misma entrada es circular **por
  construcción del cuestionario**, declarado en el propio yaml `:1492-1494`:
  «`P5_4_*` gatea a `P5_6_*`, así que sin cuenta el desenlace se reduce a
  `informal_cualquiera` por construcción» — la celda «sin cuenta» mide `0.493506` contra
  `0.285463` «con cuenta», y esa brecha de **20.8 pp** es en parte aritmética del
  cuestionario, no conducta.
- **Síntoma observable.** Un eje con `veredicto: "DISCRIMINA (tope declarado en la spec:
  el eje no puede corroborar)"` — la propia entrada lo escribe (`:1489`).
- **Mecanismo mínimo.** El grado `P0/P1/P2` de `ADV1-M1(ii)` con su **cuota**: «≥1/3 del
  set en `P2`, con ≥2 desenlaces documentados no-encuesta» (`CAREO…:34`). Es una cuota
  sobre el marco, verificable por comando.
- **Estado en el contrato.** **YA-PREVISTO en el duelo, NO-PREVISTO en la celda-D.** El
  enum `diseno_datos` del contrato de celda tiene ocho valores
  (`tests/test_celdas_d.py:79-83`) y **ninguno** expresa el grado de dependencia respecto
  del árbitro; `universo_candidatos` declara qué se barrió al buscar candidatos, no de
  dónde sale el árbitro.
- **Cruce.** **`YA-OCURRIÓ-AQUÍ`**, y con la corrección ya hecha:
  `RONDA1-…-fable-…:82` rastreó la circularidad de ENCIG en `R3.2` y la resolvió
  («no es circular medir el contraste ahí, porque el contraste nunca se extrajo de ahí»)
  — prueba de que la pregunta es contestable cuando alguien la hace, y de que nadie la
  hace por defecto.

### F7 · Heterogeneidad de forma (banda vs punto) al componer

- **Mecanismo.** Una celda entrega banda (conjunto identificado) y la de al lado entrega
  punto; al componer, alguien colapsa la banda a su punto medio para que el tipo cuadre,
  y la incertidumbre desaparece sin dejar rastro.
- **Ejemplo mínimo con números.** `propuesta-motor-matriz-v0_1.md:148`: los β entran como
  **conjuntos identificados** y la salida es una **banda**, «nunca como intervalo de
  confianza»; con **15** intervalos simultáneos «que la banda no firme el signo del
  output» es **probable en la primera corrida**. Enfrente, `G5.radio_confianza` entrega
  `output_nativo.tipo: "Distribución condicional empírica"` y
  `G5.familismo_obligacion.actitud` entrega `DISTRIBUCION_DESCRIPTIVA` con `IC95` por
  linealización de Taylor — tres formas distintas en tres celdas, sobre el mismo `G5`.
  Un `h_r` que reciba `[0.312154, 0.349156]` de una celda y `0.221500` de otra **no tiene
  contrato** que le diga qué hacer.
- **Síntoma observable.** Una salida agregada con un solo número donde al menos un insumo
  era banda; o un `output_nativo.tipo` que cambia entre la celda y lo que el consumidor
  leyó.
- **Mecanismo mínimo.** **Una regla de cierre de tipo, no una capa**: la composición
  rechaza mezclar formas salvo que la regla de promoción esté declarada en la entrada del
  catálogo de momentos **antes** de componer; y el colapso banda→punto es error, no
  advertencia. El go/no-go de Fable ya lo pide con número: «≥2 tipos de output no-punto
  producidos y compilados en un dry-run … **sin colapsar banda→punto**»
  (`RONDA1-…-fable-…:101`).
- **Estado en el contrato.** **PREVISTO-SIN-MECANISMO.** `output_nativo.tipo` y `.escala`
  son obligatorios y `incertidumbre.{tipo,ref}` también
  (`tests/test_celdas_d.py:200-207`), pero **ninguno se valida contra un enum**: el
  validador exige que el campo esté lleno, no que su valor pertenezca a una lista. Tres
  celdas, tres vocabularios de `tipo`, cero colisiones detectadas.
- **Cruce.** **`YA-OCURRIÓ-AQUÍ` en la clase**: `forense/hallazgos.md:841` — «cambiar la unidad
  en que se cuenta un techo sin re-dimensionar el techo lo convierte en otro techo»
  (96 solicitudes dimensionadas a 1 turno/llamada contra 3 turnos reales; el runner paró
  en 94/96). Misma falla, otro objeto: una cantidad cambia de unidad y el consumidor no
  se entera.

### F8 · Extrapolación fuera de soporte

- **Mecanismo.** El champion se eligió sobre el universo que su instrumento cubre y se
  consume sobre un universo más ancho; nadie compara denominadores.
- **Ejemplo mínimo con números.** El eje `formalidad` —el único firmado— tiene cobertura
  `0.689676` en `via_informal` y `0.668937` en `horizonte_corto`: **~31% y ~33% de la
  población objetivo no está en ninguna celda**. Y ENCIG es peor: su universo es
  «población de 18 años y más en **ciudades de 100 mil habitantes o más**»
  (`milpa/tramite-ola5-propuesta-v0.yaml:1648-1649`) — el eje de localidad está ausente
  **por diseño muestral**, no por olvido. Reconciliar cualquiera de esos champions contra
  un marginal poblacional «no valida ni invalida nada: compara dos universos»
  (**A-bis 4**, `instrucciones-proyecto-v2_13.md:87`).
- **Síntoma observable.** Una discrepancia que **se atenúa suavemente con la cobertura
  del eje** — la señal diagnóstica que A-bis 4 nombra: «un bug no se atenúa».
- **Mecanismo mínimo.** El campo ya existe y ya se usa: `universo_restringido: true` en
  la entrada del árbitro (`:1476`, `:1549`). Falta su gemelo en la celda-D y una regla de
  una línea: si `universo_instrumento` del champion ≠ `poblacion_objetivo` de la celda, la
  salida viaja **acotada** o no viaja.
- **Estado en el contrato.** **YA-PREVISTO parcialmente.** `universo_instrumento` es
  obligatorio por candidato desde `H1` (`v0.3:53-55`; validado en
  `tests/test_celdas_d.py:237`) y `supuesto_transporte` tiene tres valores
  (`EXISTE-SATISFACE` / `ACOTADO-CON-SUPUESTO:<cual>` / `NO-TRANSPORTABLE:<por que>`,
  `v0.3:72`). Lo que **no** existe es la comprobación: nada compara el universo del
  instrumento contra la población objetivo, ni exige que `supuesto_transporte` sea
  coherente con esa diferencia.
- **Cruce.** **`YA-OCURRIÓ-AQUÍ`** — `forense/hallazgos.md:842`: tres números llamados
  «cobertura» eran **tres cantidades distintas** (`66.89 = 9 031/13 502` es la fracción
  sin ponderar del universo triple; `68.97` es `P3_13` sin ponderar; `67.53` es `P3_13`
  ponderada), y una fila del registro afirmaba que no reconciliaban. Reconciliaban: eran
  tres universos.

### F9 · Incoherencia de escala entre celdas al llegar al consumidor

- **Mecanismo.** Cada celda declara su escala, ninguna declara el enlace; el consumidor
  compone proporciones con índices y razones.
- **Ejemplo mínimo con números.** En la misma demanda activa conviven, como
  `conducta_p_medido`: **22** filas en `p (proporcion ponderada)`, **3** en `ecologica`,
  **2** en una escala propia («proporcion ponderada de PERSONAS de 18 a 70 anios SIN
  CUENTA dentro de cada celda del eje») y **15** en `NO-DECLARADO-EN-EL-REGISTRO`. Y
  `RES-0045` es una **razón** (`0.2215` = horas de mujeres 40+ / horas totales), no una
  proporción de personas — misma columna, otro objeto. Componer `0.2215` con `0.541343`
  sin enlace es el error de categoría que **A-bis 3** prohíbe
  (`instrucciones-proyecto-v2_13.md:85`).
- **Síntoma observable.** Una suma, una diferencia o un cociente entre dos filas con
  `escala_legacy` distintas.
- **Mecanismo mínimo.** Un test de igualdad de cadenas sobre `escala` antes de cualquier
  operación aritmética entre dos insumos; `NO-DECLARADO-EN-EL-REGISTRO` cuenta como
  escala distinta de todas, incluida sí misma.
- **Estado en el contrato.** **YA-PREVISTO en la celda-D, NO-PREVISTO aguas abajo.**
  `criterio_adjudicacion.escala` y `output_nativo.escala` son obligatorios (`H1`,
  `v0.3:63-70`) y el validador los exige no vacíos
  (`tests/test_celdas_d.py:198-203`) — pero el catálogo de momentos, que es la frontera
  por la que los insumos salen hacia la composición, **no tiene columna `escala`**
  (12 columnas, verificado). Ver P4.
- **Cruce.** **`YA-OCURRIÓ-AQUÍ`** — `forense/hallazgos.md:842` otra vez, y `:421` (el mnemónico
  de ENVIPE cambia de constructo entre olas: empalmar una serie por nombre de variable
  «pega dos cosas distintas **sin error visible**»).

### F10 · El costo del contrato — cuántas celdas puede adjudicar el programa hoy

La pregunta del encargo es cuantitativa, y se contesta con los números de P1.

**Numerador disponible.** El árbitro publica **74** celdas (**64** con IC95). De ellas:

| filtro, aplicado en cascada | celdas que sobreviven |
|---|---|
| publicadas por el árbitro | **74** |
| con IC95 (`ADV1-M3` evalúa contra `R` como distribución, `CAREO…:38`) | **64** |
| sobre un eje con fila de crosswalk **firmada** (`formalidad`, F-17) | **6** |
| con persistencia construible en la ola anterior (`P3_13` ausente en ENIF 2021) | **0** |
| con evaluación no consumida ya por el motor (lectura estricta de (g)) | **0** |

**El programa puede adjudicar hoy, con el dato que tiene, cero celdas** bajo los siete
criterios — y **seis** si mesa renuncia a (d)/(e)/(g) y se queda con (a)(b)(c)(f).

**Dónde cuesta más adjudicar que lo que decide.** El careo ya puso el precio del duelo
en **12–15 sesiones** para un marco de 40–60 candidatas (`CAREO…:56`), es decir
~0.25 sesión/celda **una vez que el marco existe**. El costo real aquí no es ése: es el
de **fabricar la evaluación**. Con el crosswalk vigente, cada celda adicional adjudicable
exige una de tres cosas: una firma de mesa sobre una fila ya escrita (costo ~0, disponible
para **4** celdas vía `localidad`), un corte sellado con dato mexicano propio (`edad`,
`FP-53` — **16** celdas, acto propio con medición), o una **ola nueva** del instrumento
(**todas**, y no depende del programa). El punto de cruce es nítido y no hace falta
estimarlo: **adjudicar ya cuesta más que lo que decide en las 68 celdas cuyo eje no tiene
corte firmado**, porque el costo de habilitarlas es un acto de medición o un levantamiento
ajeno, mientras lo que deciden es un champion sobre una celda que el modelo no puede
consumir. Las **6** de `formalidad` son el único tramo donde adjudicar es barato — y son
justo las que fallan (e) y (g).

### Cierre de P3 · ¿Cuáles de estas fallas hacen que «cada celda su estimador» sea **peor** que «un estimador único con etiqueta», para quien lee salidas por celda?

**Tres: F5, F7 y F9. Las otras siete son igual de malas bajo las dos políticas o peores
bajo la única.** El argumento, falla por falla:

**No lo hacen peor** — F1 (post-hoc), F2 (multiplicidad), F4 (piso de persistencia),
F6 (circularidad), F8 (soporte), F10 (costo). Un estimador único sufre todas: elegirlo
una vez también es una elección post-hoc si se hizo mirando resultados, y hacerla **una
sola vez** la vuelve *menos* auditable, no más — la política por celda al menos obliga a
escribir un `criterio_adjudicacion` por celda, que es un objeto que se puede fechar. En
F4 la política por celda es estrictamente mejor: obliga a correr `B` en **cada** celda, y
`forense/hallazgos.md:838` muestra lo que eso revela (`B` gana 8 de 10) — un estimador único con
etiqueta nunca habría producido esa comparación.

**Sí lo hacen peor:**

- **F5 · sobreajuste al árbitro.** Con un estimador único hay **una** decisión de
  procedencia que auditar; con *n* celdas hay *n*, y cada una puede haber mirado su propio
  árbitro. El daño escala con el número de celdas y la auditoría no. Lo medido en §1.5 es
  el caso límite: **7 de 7** entradas del árbitro están dentro del motor, y ninguna celda
  lo declara, porque el contrato **no tiene campo donde declararlo**.
- **F7 · heterogeneidad de forma.** Un estimador único produce **una** forma de salida;
  quien lee celda por celda sabe qué está leyendo. La política por celda produce, hoy, tres
  formas distintas en tres celdas del mismo generador `G5`, y `h_r` tendría que reconciliarlas
  sin regla. El lector de salidas por celda es exactamente quien paga: ve `0.2215` junto a
  `[0.312154, 0.349156]` y no tiene cómo saber que uno es razón de horas y el otro banda de
  proporción.
- **F9 · escala.** Es F7 en el eje de la unidad en vez del de la forma, y es la **peor**
  de las tres, porque es silenciosa: **15 de 42** filas de la demanda activa dicen
  `NO-DECLARADO-EN-EL-REGISTRO` y el registro las sirve igual. Con un estimador único la
  escala es una propiedad del estimador y se declara una vez; con *n* estimadores es una
  propiedad de cada salida y hoy **no se declara en 36% de los casos**.

**Conclusión, sin adorno.** «Cada celda su estimador» es la política correcta —la firma
de mesa que gobierna este acto lo dice y P3 no encuentra razón para contradecirla— **pero
su precio es un contrato de interfaz que hoy no existe**. Las tres fallas que la hacen
peor son las tres de interfaz, no las de inferencia; y las tres se cierran con campos y
reglas de una línea, no con una capa. Eso es P4.

---

## P4 · La interfaz que la composición exige

Acotada. La pregunta es estrecha a propósito: **qué campos mínimos necesita cada entrada
del catálogo de momentos para que un `h_r` consuma una celda que entrega banda y otra que
entrega punto, con `π(x)` sobre cortes que el árbitro cubre a mitad de resolución.**

### 4.1 · Lo que la composición promete, y las tres cosas que hoy le faltan

La forma está escrita, sin ambigüedad
(`propuesta-motor-matriz-v0_1.md:73-79`, verbatim en `:75`):

> **m = Σ_celdas π(x) · h_r( B·θ(x), C(x) )**

y el mismo bloque es honesto sobre `h_r` (`:79`): su forma «es justo lo que `D-ABC` dejó
pendiente y ADR-65 probó que no se lee de las curvas»; bajo la ruta agregada es «una
**elección de mecanismo declarada antes de ajustar**».

Medido hoy, los tres factores del producto:

| factor | estado, por comando | cita |
|---|---|---|
| **`π(x)`** | **sin fuente cargable.** `construir_pi()` levanta `FuentePiPendiente` con el texto «π(x) no tiene hoy fuente cargable: `tasa_informalidad` aparece 0 veces…» | `milpa/src/pi.py:68-69`; `milpa/catalogo-momentos-v0_1.md:113` |
| **`B·θ(x)`** | **parcial.** `g()` levanta `SinMagnitud` si una celda **participante** no tiene número, y desde `ADR-531` (`PR #822`, fusionado a mitad de este acto) «participante» quiere decir lo que la palabra dice: `g(matriz, theta, celda, generadores=None)` acota quién entra. `G5 × familismo_obligacion` sigue cargando como `CoeficienteSinMagnitud`, así que la columna que motiva el test de ADR-30 sigue sin poder componerse | `milpa/src/matriz.py:138`, `:186`, `:95`, `:119`; `propuesta-motor-matriz-v0_1.md:62` («**SIN MAGNITUD**») |
| **`h_r`** | **no escrito.** `valor_de()` levanta `NotImplementedError`; el módulo del emisor declaró al correr que «un `C` no-trivial exige el enlace índice→adopción (`h_r`) — OLA futura» | `milpa/src/momentos.py:130`; `forense/hallazgos.md:480` |

**Consecuencia para P4, dicha antes de proponer campos:** la interfaz no se está
diseñando para una composición que corre y falla. Se está diseñando para una que **no
puede correr todavía**, y eso es una ventaja — los campos entran antes de que haya
entradas que migrar. Es la misma ventana que v0.5 aprovechó para `estado_decidibilidad`.

### 4.2 · El hueco medido en el catálogo de momentos

`propuesta-motor-matriz-v0_1.md:107-109` fija, verbatim, qué lleva cada entrada del
catálogo:

> `id_momento · definición · ESCALA declarada · UNIVERSO declarado · nivel
> (persona/hogar) · instrumento(s) candidato(s) · rol (AJUSTE | HOLDOUT | DIAGNÓSTICO) ·
> estatus de disponibilidad`

y `:112` nombra la obligación con dueño: «escala y universo por **A-bis reglas 3-4**».

**`milpa/catalogo-momentos-v0_1.tsv` tiene 12 columnas y ninguna es `escala`:**
`id_momento · objeto_modelo · necesidad_id · rol_calibracion · universo_candidatos ·
universo_instrumento · nivel · instrumentos_candidatos · computo_pretendido ·
estatus_disponibilidad · fuente_regla · reserva`.

El `.md` del catálogo documenta **tres** desviaciones deliberadas respecto de la propuesta
(`:86-90`: `rol_calibracion` en vez de `rol` — fix `S2`; `universo_candidatos` y
`universo_instrumento` separados — fix `M3`; `computo_pretendido` en vez de `computable`
— fix `M10`). **La cuarta, la desaparición de `ESCALA`, no está documentada en ninguna
parte.** No es una decisión declarada: es una omisión.

Y es exactamente la puerta por la que F9 entra: el catálogo es **la frontera entre el
selector y la matriz** (`propuesta-motor-adaptativo-celda-v0_3.md:100`: «el selector lo
puebla, celda por celda; la matriz lo consume»). Una frontera sin escala entrega insumos
cuya unidad el consumidor tiene que adivinar.

### 4.3 · Campos mínimos por entrada — la propuesta

Seis campos. Ninguno es una capa; los seis son columnas de un TSV append-only y su
verificación es comparación de cadenas o de tipos.

| # | campo | valores | qué falla sin él |
|---|---|---|---|
| **1** | `escala` | cadena libre, **obligatoria, sin valor centinela** — `NO-DECLARADO` **no** es legal | F9. Es el campo que la propuesta pedía en `:107` y el TSV no tiene. Sin él, `h_r` compone razones con proporciones |
| **2** | `forma` | `PUNTO` \| `BANDA` \| `DISTRIBUCION` \| `RAZON` | F7. Hoy `output_nativo.tipo` de la celda-D es texto libre no validado (`tests/test_celdas_d.py:200` exige lleno, no pertenencia) y tres celdas usan tres vocabularios |
| **3** | `familia_incertidumbre` | `IC_TAYLOR` \| `IC_BOOTSTRAP` \| `CONJUNTO_IDENTIFICADO` \| `NINGUNA` | una banda de `identified set` (Manski/Ferson, `matriz:148`) y un IC95 de Taylor **no son el mismo objeto** y no se propagan igual. El contrato de celda ya obliga a `incertidumbre.{tipo,ref}`; el catálogo no lo hereda |
| **4** | `resolucion_pi` | el corte de `CORTES_C1` sobre el que el momento está definido, o `NO-PARTICIONA` | `π(x)` sólo suma sobre cortes sellados (`milpa/src/celdas.py:74-81`). `reparto_hogar` es «una **RAZÓN** con una sola celda, no una partición de la población» (crosswalk `:20`) — sin este campo entra a una suma ponderada como si particionara |
| **5** | `resolucion_arbitro` | `EQUIVALENTE` \| `MAPEO-N-A-1:<n>-a-<m>` \| `SIN-CORRESPONDENCIA`, **copiado del crosswalk, con su `firma`** | la mitad de resolución. `localidad` colapsa **4 celdas del modelo a 2** (crosswalk `:10`) y hoy nada aguas abajo lo sabe |
| **6** | `payload_arbitro` | `payload_manifiesto_id` del árbitro de ese momento | F5/F6. Es el campo que permite la comparación de cadenas contra el `payload_manifiesto_id` del candidato — el mecanismo mínimo de §F5 |

Los seis son **append-only** sobre un catálogo que ya es append-only por diseño
(`matriz:104`), y ninguno exige mirar el disco: `escala`, `forma` y
`familia_incertidumbre` se leen de la celda-D que puebla la entrada; `resolucion_pi` y
`resolucion_arbitro` del crosswalk ya escrito; `payload_arbitro` del yaml del árbitro.
Poblarlos no viola `§3.3` (anti-circularidad: «congelar antes de escanear»,
`matriz:128-130`) porque no son estatus de disponibilidad.

### 4.4 · Qué queda prohibido

Cuatro prohibiciones. Las cuatro son **errores**, no advertencias — una advertencia que
nadie lee es el mecanismo por el que F7 y F9 sobreviven.

1. **Colapsar una banda a su punto medio en silencio.** Si `forma = BANDA` y el consumidor
   necesita `PUNTO`, la composición **para**. La promoción `BANDA → PUNTO` sólo existe si
   la entrada declara la regla **antes** de componer, y entonces la salida viaja marcada.
   Ya está pedido con número: «≥2 tipos de output no-punto … **sin colapsar banda→punto**»
   (`RONDA1-…-fable-…:101`).
2. **Componer dos insumos con `escala` distinta sin enlace declarado.** A-bis 3
   (`instrucciones-proyecto-v2_13.md:85`): «una diferencia de proporciones y un
   coeficiente de índice no son la misma cosa salvo que el modelo declare una función de
   enlace». `NO-DECLARADO` cuenta como distinta de todas, **incluida otra
   `NO-DECLARADO`**.
3. **Sumar sobre `π(x)` un momento con `resolucion_pi = NO-PARTICIONA`.** Una razón de una
   sola celda no es un término de `Σ π(x)·…`. Es el caso `reparto_hogar`, ya nombrado en
   el crosswalk.
4. **Reconciliar un momento de universo restringido contra un marginal poblacional.**
   A-bis 4 (`:87`). Con cobertura `0.689676` / `0.668937` en el eje firmado, y el universo
   de ENCIG restringido a ciudades de 100 mil habitantes o más, esto no es hipotético.

Y una quinta que no es prohibición sino orden de precedencia, porque hoy falta y ya costó
un PARO: **si dos reglas de la escala pueden satisfacerse a la vez, se declara cuál manda
al sellar y no después** (`instrucciones-proyecto-v2_13.md:115`). `forense/hallazgos.md:470` mide
el caso: `DUELO-PREREG-V2` **paró** de sellar `ADV1-M5` porque la precedencia entre sus
cinco casillas no existe en el corpus, y el operador `⊕` de `L⊕M` «nunca se define con
fórmula».

### 4.5 · La prueba pre-composición que detecta una escala mal declarada

**Una sola prueba, tres asertos, sin abrir microdato.** Corre sobre el catálogo y el
crosswalk, antes de que `h_r` toque nada:

```
para cada par (m_i, m_j) que un mismo h_r compone:
  A · m_i.escala == m_j.escala             ... o existe enlace_declarado(m_i, m_j)
  B · m_i.forma  == m_j.forma              ... o existe regla_promocion declarada
  C · m_i.resolucion_pi == m_j.resolucion_pi, y ambas != NO-PARTICIONA
cualquier aserto falso => FAIL, no WARN. Ningún valor centinela satisface A.
```

**Qué atrapa hoy, en concreto, con los datos que ya existen:** el par
(`RES-0045` = razón de horas, escala `p (proporcion ponderada)`, `forma = RAZON`,
`resolucion_pi = NO-PARTICIONA`) contra (`RES-0046` = proporción de personas, misma
cadena de escala, `forma = PUNTO`, `resolucion_pi = formalidad`) **pasa A y falla B y C**
— que es el resultado correcto, y hoy nada lo produce: las dos filas conviven en el mismo
registro con la misma cadena en la columna de escala y **no son la misma cantidad**.

**Y el falsador de la propia prueba, declarado:** si en tres meses la prueba no ha
devuelto un solo `FAIL` sobre pares reales, o es porque el catálogo sigue con
`estatus_disponibilidad: NO-VERIFICADO` en 22/22 —en cuyo caso la prueba no falla, es que
no hay pares— o porque los seis campos se están poblando por copia mecánica sin leer la
celda. Se distingue por comando: contar entradas con `escala` distinta entre sí. Si el
conteo es 1, alguien está copiando.

### 4.6 · ¿Es viable la composición con estimadores de forma distinta?

**Sí, con una condición y un precio, y conviene decir los dos.**

**Condición.** La composición es viable **si y sólo si la regla de promoción de forma se
declara por par, antes de componer, y viaja con la salida.** No hay una promoción
universal correcta: `BANDA → PUNTO` pierde la única propiedad por la que los β entran como
conjuntos identificados (`matriz:148`), y `PUNTO → BANDA` inventa incertidumbre que el
estimador no midió. Lo que sí es correcto es propagar la banda y **aceptar que la salida
sea banda** — que es lo que la propuesta ya eligió, con su riesgo dominante pre-declarado:
con 15 intervalos simultáneos, «que la banda no firme el signo del output» es el
desenlace probable de la primera corrida (`:148`).

**Precio, dicho sin adorno.** Una composición honesta de formas heterogéneas **casi
siempre entregará una banda que no firma el signo**. Eso no es un fallo de la interfaz: es
la interfaz funcionando. El fallo sería lo contrario — una cifra puntual limpia salida de
insumos que no la sostienen, que es exactamente lo que la prohibición 1 existe para
impedir.

**Lo que P4 no decide.** Ni la forma de `h_r` (`D-ABC` sigue abierto, `matriz:156`), ni la
fuente de `π(x)`, ni si los seis campos entran como columnas nuevas del TSV o como un
sidecar. Los tres son actos propios.

---

## Módulo de auditoría de rigor extremo

Carga porque P3 afirma sobre el modelo (`instrucciones-proyecto-v2_13.md:119`).

**Contadores movidos por el trabajo que produjo este artefacto: 0.** (v2.3, `:132`.)
Ninguna celda-D se registra, ninguna adjudicación ocurre, ningún número del modelo se
propone, ninguna fila de mesa se abre. Este acto produce diseño y un negativo.

**1 · ¿Qué parte del análisis podría estar confundiendo pobreza, desigualdad, violencia o
informalidad con «cultura»?** La candidata 1 (`via_informal`) lo tiene en el centro: el
eje `formalidad` mide *derecho a servicio médico por parte de su trabajo* (`P3_13`) y la
lectura fácil de «ahorra solo informal más alto sin seguridad social» es cultural. El
propio yaml del árbitro cierra esa puerta dos veces: el eje `escolaridad` sale
`veredicto: "CONTRARIA"` al signo pre-registrado (`:1454`) y el eje `cuenta_formal` es
`NO-FALSABLE contra el principal` por construcción del cuestionario (`:1492`). P1 no
promueve ninguna lectura causal; A-bis 1 gobierna: son asociaciones.

**2 · ¿Qué parte podría estar sobregeneralizando desde clases medias urbanas?** La
candidata 2 (ENCIG 2025), literalmente y por diseño muestral: su universo son ciudades de
**100 mil habitantes o más** (`:1648-1649`). Está anotado en su fila de (b) y es una de
las razones por las que el eje de localidad le falta. Si el careo la elige, hereda ese
sesgo con nombre.

**3 · ¿Qué parte está sesgada por literatura escrita desde marcos estadounidenses o
europeos?** El aparato de adjudicación (skill sobre baseline, CRPS/Brier, TOST, `FFC`,
Hewitt et al., Bisbee) es importado entero del careo, y este acto lo usa sin reabrirlo.
El único punto donde la importación muerde es `skill = 1 − error/error(B)`: da por
supuesto que existe un `B` que habla. `forense/hallazgos.md:829` mide que en este programa `B`
**se abstiene** en 2 de 3 objetivos bajo el corte de disponibilidad vigente. No se adopta
ni se rechaza la fórmula aquí (P2 no se escribe), pero queda dicho que su denominador no
es gratis.

**4 · ¿Qué hallazgos cambiarían si el foco fuera México rural, indígena o popular?** Todos
los de la candidata 2, que no los cubre. Y el de `localidad`, que es el eje donde el dato
sí discrimina (`0.409255` en localidades menores de 15 000 contra `0.329868` en 15 000 y
más, `:1472-1473`) y es justo el que el crosswalk deja **sin firma** — el eje rural/urbano
es el que hoy no autoriza consumo.

**5 · ¿Qué parece psicológico pero en realidad es un incentivo racional ante un entorno
específico?** `dominio_urbano_rural` en `evasion_norma`: la evasión sale **más alta en lo
urbano** (`0.592703`) que en lo rural (`0.403310`), con los tres IC95 sin traslape — al
revés de la corazonada sobre la que se escribió la predicción (crosswalk `:11`). El
crosswalk además advierte que forzar el mapeo **invertiría un signo ya medido**.

**6 · ¿Dónde hay evidencia débil pero intuición social fuerte?** En la igualdad
`formalidad(modelo) = formalidad(árbitro)`. La firma `F-17` la ratifica; la verificación
por definición que **la misma firma autoriza** dice `MAPEO-N-A-1` (crosswalk `:9`). La
intuición de que son «lo mismo» es fuerte y el dato dice que parten a gente distinta
(derechohabiencia por cónyuge: `segsoc=1` y `P3_13=7`).

**7 · ¿Qué conclusiones serían peligrosas si alguien las usara de forma simplista?**
Cuatro, y las cuatro son lecturas de esta nota:
(i) *«no hay celda-D piloto posible»* — falso: hay **6** celdas del árbitro sobre un eje
firmado, y el bloqueo es (d)/(e)/(g), no la ausencia de dato;
(ii) *«el motor está contaminado»* — impreciso: el motor **consume** las mediciones del
árbitro porque así se diseñó la carga, y eso es correcto como plomería; lo que no se puede
es **evaluarlo contra su propia fuente y llamarlo skill**;
(iii) *«`B` gana, el motor sobra»* — el careo lo prohíbe explícitamente
(`ADV1-M5(1)`, `:42`) y `forense/hallazgos.md:838` es descriptivo sobre 10 celdas, no un veredicto;
(iv) *«P2 no se escribió porque faltó tiempo»* — se declinó por instrucción, con el
criterio medido; escribirlo habría sido fabricar la elección.

**8 · (v2.1) ¿Qué afirmación de este artefacto describe el estado del corpus —un conteo,
una cobertura, una versión, la existencia de un archivo— y no fue derivada, sino escrita a
mano?** Barrido honesto:

- **Todo conteo de esta nota fue derivado en esta sesión**, con el comando a la vista: 7
  entradas `_ejes_`, 74/64 celdas, 3 celdas-D, 22 momentos, 207/42 filas de demanda, 15
  filas de crosswalk, 178 246 filas de inventario, 2 133 archivos `.md`/`.tsv`, 12
  columnas del catálogo, 15/22/3/2 escalas.
- **Cuatro cifras NO fueron derivadas aquí y se citan como ajenas, con su dueño:**
  `MAE_pp(B)=0.9229 / M=4.3073 / L_CORPUS=21.3226` y el «8 de 10» (de
  `forense/hallazgos.md:838`, `ACTO GEN2-B-MARCO`); el `≈77%` de falso ganador con N=12 (de
  `CAREO…:29`); el `71%` y el `49.3%` de ENCUCI (de `forense/hallazgos.md:837`); y las
  `12–15 sesiones` de costo del duelo (de `CAREO…:56`). Ninguna se re-midió: este acto no
  abre microdato.
- **Una afirmación del corpus que este acto encontró escrita a mano y desactualizada, y
  que NO corrige por perímetro:** `data/INFRAESTRUCTURA-v1_0.md:159` dice que
  `data/curacion-registro/celdas-d/` tiene «hoy **2 archivos**» y lista dos; hay **3**
  desde el 13/ago (`G5.obligacion_medida.conducta.yaml`). Fila de reserva al cierre.
- **Una segunda, de la misma clase:** `milpa/tramite.yaml:712` cita el origen de la
  segmentación como `milpa/tramite-ola5-propuesta-v0.yaml:1162-1346`; la entrada
  `dinero.ahorro.via_informal_ejes_enif2024` vive hoy en `:1415-1599`. La cita por línea
  **no resuelve**; el `id` citado en la misma línea sí. Fila de reserva al cierre.

**9 · (v2.2) Deudas asumidas que caducan al cambiar la función del programa.** Una, y es
la que P1 hace visible: **cargar el árbitro dentro del motor** fue coherente mientras la
función era *describir* con el mejor número disponible — es plomería correcta y está
documentada como «copiada verbatim» en el propio archivo. Dejó de serlo el día que el
programa pasó a **evaluar** al motor contra ese mismo número. La deuda no está registrada
como pendiente en ninguna parte: está registrada como decisión de carga. Se re-examina
aquí por primera vez.

**10 · (v2.4) Si este artefacto contiene una cantidad estimada: ¿en qué escala está, y
contra qué se está comparando?** Esta nota **no produce ninguna cantidad estimada nueva
sobre México**. Las que transcribe son ajenas y viajan con su escala y su fuente:

| cantidad | escala | contra qué se compara **en esta nota** |
|---|---|---|
| `0.672014` / `0.790906` (árbitro, denuncia) | proporción ponderada, **unidad = DELITO**, universo `BPCOD='01' ∧ BP2_1∈{1,2}`, n=1 016 | contra `0.672` / `0.7909` del motor — **misma escala, misma fuente, mismo universo**: por eso la comparación es lícita y el resultado es *identidad*, no *acuerdo* |
| `0.541343` (motor, horizonte_corto) | proporción ponderada, **unidad = PERSONA**, universo restringido «trabaja sin seguridad social», cobertura `0.668937` | contra `54.13%` de la sensibilidad pre-declarada del árbitro — **misma escala y mismo universo**; identidad al cuarto decimal |
| `0.330639` vs `0.541343` | la misma escala, **dos definiciones del desenlace** (`P4_10=1` vs `P4_10∈{1,2}`) | **no se comparan entre sí como si midieran lo mismo**: se usan en F1 precisamente para mostrar que elegir entre ellas después de verlas mueve la brecha 1.5 pp |
| `0.2215` (`RES-0045`) | **RAZÓN** de horas (mujeres 40+ / horas totales de cuidado del hogar), unidad = HOGAR | **no se compara con ninguna proporción de personas** en esta nota. Se cita en F7/F9/P4 como el ejemplo de por qué no se puede: A-bis 3 |
| `0.9229 / 4.3073 / 21.3226` pp | MAE en puntos porcentuales, ajeno (`forense/hallazgos.md:838`) | entre sí, sobre el mismo universo, **con control positivo `Δ=0.0` 10/10 verificado antes de comparar** — así lo declara su fuente, y así se cita |
| coberturas `0.689676` / `0.668937` | fracción del universo objetivo cubierta por el eje | **contra nada**: se usan para declarar universo restringido (A-bis 4), no para reconciliar |

Ninguna cantidad de esta nota cruza de escala sin decirlo, y ninguna entra al canon.

---

## Re-verificación de citas antes de cerrar

Precedente: `ADR-530` (`ACTO GEN2-CROSSWALK-EJES-1`) re-verificó 31 citas. Este acto
corre **dos** pasadas, porque resuelven preguntas distintas.

### Pasada 1 · ¿Resuelve cada `archivo:línea` de esta nota?

Mecánica y **reproducible desde la nota misma** — extrae toda cita del propio archivo y
comprueba que el archivo existe y tiene esa línea. No necesita ninguna herramienta nueva:

```
python3 - <<'PY'
import re, io, os, collections
nota = "forense/notas/2026-09-17-GEN2-CELDA-D-DISENO-CIEGO-1.md"
t = io.open(nota, encoding="utf-8").read()
pat = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|tsv|yaml|py|json)):(\d+)(?:-(\d+))?`")
vistos = collections.OrderedDict()
for m in pat.finditer(t):
    ruta, a, b = m.group(1), int(m.group(2)), m.group(3)
    for ln in ([a] if not b else [a, int(b)]):
        vistos[(ruta, ln)] = True
ok = mal = 0
for (ruta, ln) in vistos:
    if not os.path.exists(ruta):
        print("FALLA  %s:%d  -- el archivo no existe" % (ruta, ln)); mal += 1; continue
    n = sum(1 for _ in io.open(ruta, encoding="utf-8", errors="replace"))
    if ln < 1 or ln > n:
        print("FALLA  %s:%d  -- el archivo tiene %d lineas" % (ruta, ln, n)); mal += 1
    else:
        ok += 1
print("CITAS `archivo:linea` DISTINTAS EN LA NOTA: %d -- %d resuelven, %d no" % (len(vistos), ok, mal))
PY
```

Salida cruda, contra `HEAD` de este acto:

```
CITAS `archivo:linea` DISTINTAS EN LA NOTA: 78 -- 78 resuelven, 0 no
```

Nota de método: la primera corrida devolvió **14 FALLA**, todas de la misma clase — citas
escritas en forma corta, con sólo el nombre base del archivo (*hallazgos*, *procedencia*,
*v0_5*, *CAREO-ADV-DUELO*, *F5-contrato-triada*), que un lector humano resuelve por
contexto y un comando no. Se normalizaron a ruta completa **antes** de cerrar. Es exactamente la clase
de defecto que esta pasada existe para atrapar, y ya se pagó una vez en el árbol:
`milpa/tramite.yaml:712` cita `milpa/tramite-ola5-propuesta-v0.yaml:1162-1346` y la
entrada vive hoy en `:1415-1599` — resuelve por `id`, no por línea (reserva al cierre).

### Pasada 2 · ¿Dice cada línea citada lo que la nota afirma que dice?

La pasada 1 comprueba que la línea existe; no que sea la línea correcta. La pasada 2 fija
una **subcadena ancla** por cita y verifica que aparezca en esa línea exacta —
**185 anclas** sobre **24 archivos** (las 78 citas de la nota más las de rango interior y
las de los tres módulos de `milpa/src/`). Salida cruda:

```
TOTAL 185 citas re-verificadas: 185 PASA, 0 FALLA
```

Esa pasada corrigió **9** citas antes de cerrar, todas por desplazamiento de una a cuatro
líneas (encabezado citado en vez de cuerpo, o primera línea de una lista en vez de la
lista): la sensibilidad `P4_10∈{1,2}` del árbitro (2186-2187, no 2187-2188), el párrafo de
v0.5 sobre las tres celdas existentes (43), el §3.3 anti-circularidad de la propuesta de
matriz (128-130, no 130), las tres desviaciones declaradas del catálogo de momentos (86-90,
no 86-88), las cuatro del validador de celdas-D (106-121 / 200-207 / 237, no 107-117 / 199 /
236) y la entrada del módulo de rigor extremo (117-119, no 119).
El guion de anclas vive en el scratchpad de la sesión, no en el repo: **no entra al
perímetro** (`tools/` no está en la lista de este acto). Las 185 anclas son reproducibles
leyendo la nota, que cita cada una en su sitio.

---

## Cierre

**Lo que este acto entrega.** Un segundo diseño independiente, escrito sin ver el de
dirección: un universo derivado por comando, siete criterios aplicados a **12 grupos de
candidatas**, una tabla de eliminación, **un negativo robusto a las dos lecturas del
criterio (g)**, diez modos de falla con su estado en el contrato y su cruce contra
`forense/hallazgos.md`, y una interfaz de composición de seis campos con cuatro
prohibiciones y una prueba pre-composición.

**Lo que NO entrega, y por qué.** El pre-registro P2 — por instrucción explícita del
encargo, porque ninguna candidata pasa los siete criterios. Ese es el resultado, no una
omisión.

**Lo que el careo tiene que mirar primero.** Si el diseño de dirección eligió una celda,
la pregunta no es quién tiene razón: es **cuál de los siete criterios no aplicó, o aplicó
con otra operacionalización**. Las tres candidatas a esa divergencia, por orden de
probabilidad:

1. **(g)**, si dirección leyó «no vista» como «no es `U3`» en vez de «el candidato no la
   ha consumido». Bajo esa lectura pasan las siete — y aun así ninguna pasa las otras seis.
2. **(b)**, si dirección admitió filas de crosswalk **sin firma**. Admitir `localidad`
   abre 4 celdas más y hace elegible a `via_informal` en (b); la regla que lo impide está
   escrita en `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv:4` y es de 16/sep, un día antes
   del diseño de dirección.
3. **(a)**, si dirección leyó la escala del campo `clase_legacy` en vez de
   `escala_legacy`. Eso convierte tres `✗` en `✓` y deja a `evasion_norma` y
   `util_sin_coercion` fallando sólo (b) y (g).

**Sucesor.** `GEN2-CELDA-D-CAREO-1` (nube, Opus): archiva el diseño de dirección
(sha256 `c7d55e61…`, A.3) junto a éste, carea fila por fila y escribe la hoja de decisión
para mesa. Ahí nacen las filas FP/NC — **este acto no abre ninguna**.

---

## Apéndice · Cascada y suite, con la salida cruda

**`ADR-532`** — y el camino hasta ese número es en sí un registro. Al abrir el cierre, el
máximo real en `main` era `530` y el candidato contiguo `531` estaba **ya redactado** en
`origin/claude/affectionate-sagan-u8484q` (`GEN2-M1-ALCANCE-1`, cierre escrito, **sin
fusionar y sin PR abierto**), verificado por `tools/cierre_acto.py`:

```
ADR
  Real (comando de la casa): 530
  Candidato: 531
  ¿Candidato ya redactado en alguna rama remota accesible?
    claude/admiring-meitner-yghskh: NO
    claude/affectionate-sagan-u8484q: SI
```

**Tres intentos, y los dos primeros están mal por razones distintas — se dejan escritos
porque el error es el registro.** (1) La primera redacción tomó **`532`** para esquivar el
`531` de la rama en vuelo: `T15 T-ADR-COUNT` lo rechazó con **4 `FAIL`** — `huecos en la
secuencia de ADR: [531]`, más los tres contadores, que cuentan **ADR únicos** y no el
máximo. (2) La segunda tomó **`531`**, el contiguo, aceptando de antemano renumerar si esa
rama fusionaba primero. (3) **Fusionó primero** (`PR #822`, 17/sep), así que este acto
renumera a **`532`** — que ahora no abre hueco, porque `531` ya está ocupado en `main`.
Rige la regla de la casa sin excepción y sin atajo: **renumera quien fusiona segundo**.

**Suite.** Primera corrida tras el 0-bis: **ROJA**, 4 entradas nuevas frente a
`tests/baseline.json`.

| entrada | ¿defecto real? | qué se hizo |
|---|---|---|
| `T02` nombre normalizado colisiona: encargo ↔ nota | **Sí** | La nota tiene nombre fijado por el encargo. El archivo de encargo lleva **sufijo de tema**, que es lo que `forense/encargos/convencion.md` ya prescribía: «*El archivo de encargo lleva el código del acto como prefijo tras la fecha …; su nota no. T02 normaliza sin distinguir directorio … ha ocurrido en cinco actos*» |
| `T25` ×2, rótulo pelado `M1` en encargo y nota | **Sí** | Paso 5 de `/acto`. **Un encargo verbatim (A.3) nunca se edita para complacer un test**: los dos archivos entran a `_T25_ARCHIVOS_CONOCIDOS` con el comentario que enumera cada mención (`M1` ×2 orígenes, `M3`, `M10` de `RONDA-M`, y `M01`/`M22`, que son **ids de fila** del catálogo de momentos, no rótulos). El rótulo propio, `GEN2-CELDA-D-DISENO-CIEGO-1`, sí se censa en `canon/registro-rotulos.tsv` |
| `T16` declara 3 FAIL · 4347 WARN, la corrida da 3 FAIL · **4348** WARN | **No — defecto del instrumento, por tercera vez** (y una cuarta, simétrica, ya medida en el árbol: `forense/hallazgos.md:846` documenta el mismo `T16` rojo en CAJA por `data/raices.local.yaml`, gitignorado, «*cuya "corrección" pondría CI en rojo*») | Este sandbox de nube no tenía `jsonschema`, **declarada en `requirements.txt`**, así que `T38 T-ALTA-RELACION` emitía aquí un WARN `NO-CORRIDO` que el runner no tiene. Mismo defecto que `ADR-520` y `ADR-530` ya pagaron y documentaron. **Se corrigió el instrumento, no el número**: instalada la dependencia, `T38` pasa a `[ ok ]` |

Corrida tras corregir el instrumento, **contra la base `10afea1`** (antes del sync):

```
  3 FAIL · 4347 WARN

  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 5e2ad5ce8daac333b03f344c578a9ae292fdc9db)
```

Corrida final, **contra la base `d69eed1`** (después del sync con `PR #822`):

```
  3 FAIL · 4351 WARN

  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 5e2ad5ce8daac333b03f344c578a9ae292fdc9db)
```

Los **3 `FAIL`** son los heredados del corpus documental (`T06`×2 —Gini y confianza
interpersonal con valores múltiples— y `T08` —7 reports sin mapa de evidencia—), ajenos a
este perímetro y ya en la línea base. **Neto de este acto: cero `FAIL` nuevos y cero
`WARN` nuevos, medido dos veces contra dos bases distintas.** Los **+4 `WARN`** entran con
`PR #822` y los declara `ADR-531`; aquí se reproduce su cifra sin moverla. La de `ADR-530`
(`3 FAIL · 4347 WARN`) queda vencida — **por `ADR-531`, no por este acto**.

**Perímetro, verificado por `git status` y no por memoria.** Archivos tocados:

| archivo | por qué está en el perímetro |
|---|---|
| `forense/notas/2026-09-17-GEN2-CELDA-D-DISENO-CIEGO-1.md` | el entregable, nuevo |
| `forense/encargos/2026-09-17-GEN2-CELDA-D-DISENO-CIEGO-1-SEGUNDO-DISENO-INDEPENDIENTE.md` | 0-bis A.3 + `## NO-CORRIDO / RESERVAS` + `## CONSUMIDO` |
| `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_13.md` · `canon/registro-rotulos.tsv` | «cascada de `/acto` (ADR, cabeceras, `registro-rotulos` si aparece rótulo pelado)» |
| `tests/check.py` | «`tests/check.py` **solo por T25**» — y sólo por T25: la única edición es la exención de `_T25_ARCHIVOS_CONOCIDOS` |

**No tocados, y se dice explícitamente porque el encargo los nombra:**
`data/curacion-registro/celdas-d/` · `milpa/` · `data/corrida0/` ·
`forense/firmas-pendientes.tsv` · `forense/no-corrido.tsv` · specs · resultados. Y de
`GEN2-M1-ALCANCE-1`, que sigue corriendo: `forense/tablero/`, `milpa/src/matriz.py`,
`propuesta-motor-*.md` y `forense/hallazgos.md` — **intactos**; las propuestas se leyeron
como están en `main`, sin sus enmiendas.
