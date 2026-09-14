# Cierre · ACTO GEN2-DISENO-FASE1-CIERRE — la declaración que mintió tres veces, auditada hasta el fondo

**Acto:** `ACTO GEN2-DISENO-FASE1-CIERRE` · 14/sep/2026 · CAJA (Ubuntu/WSL2, corpus montado) · base `origin/main = 4fedf1cf` (PR #757) al abrir, `2b502d5` (PR #758) al cerrar
**Encargo:** `forense/encargos/2026-09-14-GEN2-DISENO-FASE1-CIERRE.md` (A.3, verbatim)
**Auditoría P1:** `forense/notas/2026-09-14-GEN2-DISENO-FASE1-CIERRE-auditoria.md` (COMMIT-1, sólo descriptores)
**Spec sellada:** `forense/prereg-caja/EDER-CORRESIDENCIA-DISENO-spec-v1_0.md` (`sha256 b6c75544…eb5a41`, `0cbaba6`)
**Corrida:** `data/corrida0/CALC-EDER-0001/` (`CALC-EDER-0001--0cbaba6cea97`, 69 RESULT, `verify: REPRODUCE`, `CONTEXTO=IDENTICO`, dos veces aislado)

---

## 0 · El titular, antes de nada

`FP-201` cae por **quinta fuente**: EDER 2017 sí trae `est_dis`, `upm`, `factor` y `factor_per`, declarados en su FD con tipo y página, y hasta con la receta `svydesign` del productor. La tasa de fase 1 `familia.corresidencia.adulto_familiar` se re-estimó con ese diseño: **el punto no se movió** (`0.9960856`, `Δ = −3.98e-07`, `n = 14887` exacto) y **la varianza sí existe ahora** — IC95 de diseño `[0.994837, 0.997212]` por bootstrap de UPM dentro de estrato (291 estratos, 3 780 UPM, 3 estratos con UPM única → límite inferior). ENNViH **no tiene** diseño público (revisado tres veces antes, re-confirmado aquí sobre 158 `.dta` de la ola 2) y **no se re-estima**: su residuo vive en `NC-0156` y en ninguna otra fila. **`NC-0086` se cierra** con las dos fuentes pendientes selladas por veredicto.

Contador: **un CALC sucesor** (`CALC-EDER-0001`, `cuenta_gen2 = SI` por la firma de contador con objeto del encargo, escrita en `decisiones.tsv`; el merge la perfecciona).

---

## 1 · Compuerta, premisas y universo, re-derivados

- **Compuerta** `GATED a PR del ACTO GEN2-B-MARCO fusionado`: primer intento (11:27 CST) **paró con cero commits** — `acto/gen2-b-marco` estaba en su 0-bis (`d246556`, 11:26:39). Relanzado por instrucción de mesa («verifica el repo… y re-lanza») tras `PR #757 MERGED` (19:23Z): verificada **por producto** (`git merge-base --is-ancestor 4fedf1cf origin/main`; `forense/encargos/2026-09-14-GEN2-B-MARCO.md` con `## CONSUMIDO`).
- **Universo declarado (A.13):** cinco fuentes de `FP-201` cruzadas con `origin/main`: ENVIPE (#653), ENIF (#667), ENCUCI (#673) ya re-estimadas con diseño; **pendientes = {ENNViH ola 2, EDER 2017}** — coincide con la lista de dirección. Tabla completa y `ya_medido.py` de ambos ids en la nota de auditoría §1.
- **Premisa «los payloads de ambas EXISTEN en el manifiesto»:** cierta para EDER (`eder_2017_eder2017_bases_csv`, sha coincide con la raíz), **falsa en la letra** para ENNViH (`manifiesto.yaml` sigue sin `id:` para `ehh05*.zip`; hallazgo preexistente de fase 1 y de `CORR-0008`). No bloquea: ENNViH no se abre.

---

## 2 · P1 — veredicto por fuente (vocabulario A.4)

| fuente | veredicto | ponderador | estrato | UPM | cita textual del descriptor |
|---|---|---|---|---|---|
| **ENNViH/MxFLS ola 2** | `EXISTE-NO-SATISFACE` — diseño completo pendiente de `NC-0156` | `fac_3b` («FACTOR DE EXPANSIÓN LIBRO 3B», `ehh05w_all/ehh05w_b3b.dta`) | **no existe** (`c_portad.dta::estrato` = 4 clases de tamaño de localidad) | **no público** (FAQ oficial: municipio, localidad y UPM no se liberan) | `data/diseno-muestral.yaml` fila ENNViH (`SIN_DISEÑO_PUBLICADO`, `RECENSO-DISENO-14`, `FP-118`); `2026-08-24-cal-g3-puntual-cierre.md` PASO 0 «AGOTADO»; `2026-09-10-GEN2-S6-…-contraste.md` «No hay hoy diseño público ejecutable» (180 UPM en la nota oficial, ninguna en el payload). Control positivo de este acto: 158 `.dta` de ola 2, 158 leídos, 1 acierto (`estrato`), 0 UPM. |
| **EDER 2017** | `EXISTE-SATISFACE` | `factor` (VIVIENDA #109, `N (5)`) · `factor_per` (ANTECEDENTES #52, `N (5)`) | `est_dis` (#107 «Estrato de diseño muestral», `C (4)`) | `upm` (#108 «Unidad primaria de muestreo», `C (5)`) | `eder2017_fd.pdf` pp. 8 (§1.1.3), 15, 17, 40, 66; `eder2017_descripcion_calculoR.pdf` p. 5 (`survey.lonely.psu="adjust"`), p. 8 (`svydesign(id=~upm, strata=~est_dis, …, weights=~factor_per)`) |

**Lo que `FP-201` no vio:** `data/diseno-muestral.yaml` tenía EDER `MAPEADO` (24/ago, `ADR-149`) una semana antes de que `FP-201` (31/ago) declarara la ausencia para las cinco; y la propia spec de fase 1 §(c)4 escribió «EDER trae est_dis/upm de diseño» sin verificarlo. Un `FP` que afirma una ausencia sobre varias fuentes a la vez falla fuente por fuente; ésta es la quinta.

---

## 3 · P2 — la re-estimación de EDER (`CALC-EDER-0001`)

**Estimando (E.3, verbatim de fase 1):** personas de `historiavida.csv` cuya vivienda tiene `tipo_adqui` no blanco, `d = 1` si alguna fila del panel retrospectivo trae `padre_cor ∨ madre_cor ∨ hnos_cor ∨ suegro_cor ∨ suegra_cor = '1'`, ponderador `factor` de la vivienda. Ningún sello viejo se toca.

### 3.1 · Embudo y estructura (guardias)

| paso | conteo |
|---|---|
| miembros del ZIP · columnas vivienda / historiavida / antecedentes | 5 · 109 / 200 / 52 |
| filas vivienda / historiavida / antecedentes | 23 548 / 886 976 / 23 831 |
| `folioviv` único en vivienda · terna única en antecedentes | SÍ · SÍ |
| vivienda sin `est_dis` / `upm` / `factor` | 0 / 0 / 0 → `DISENO-PRESENTE` |
| `est_dis` distintos · `upm` distintos (vivienda) · UPM que cruzan estrato | 292 · 4 089 · **0** (`G-UPM-ANIDA-EN-EST-DIS = SI`) |
| viviendas con `tipo_adqui` no blanco / excluidas | 14 690 / 8 858 |
| personas en historiavida · sin ponderador · **`U_A`** | 23 831 · 8 944 · **14 887** (`Δn vs fase 1 = 0`) |
| `d = 1` / `d = 0` · masa `factor` | 14 828 / 59 · 17 503 330 |
| trampa de tipo `padre_cor` (cadena `'1'` vs numérico 1) | 23 867 = 23 867 → `CADENA-Y-NUMERO-COINCIDEN` |

### 3.2 · El punto (control positivo) y la varianza (lo nuevo)

| RESULT | valor |
|---|---|
| **`A-P`** (sucesor) | **0.9960856019968771** |
| `A-DELTA-VS-GEN1` · `A-REPRODUCE-GEN1` | −3.980e-07 · **REPRODUCE** (`round(·,6) = 0.996086`, `A-ADOPCION-P3-DELTA = 0.0`) |
| `A-P-COMPLEMENTO` (contado directo) · `A-SUMA` | 0.003914398 · 1.0 |
| **`A-IC-LO` / `A-IC-HI`** (bootstrap UPM en estrato, 2 000 réplicas, `seed 20260914`) | **0.994837 / 0.997212** |
| `A-METODO-IC` | `IC-CON-ESTRATOS-DE-UPM-UNICA` (3 de 291) → **límite inferior de la anchura verdadera** |
| `A-N-ESTRATOS` · `A-N-UPM` · `A-N-SIN-DISENO` | 291 · 3 780 · 0 |
| `A-EE-TAYLOR` · `A-IC-LO/HI-TAYLOR` (cotejo con la receta R de INEGI, aproximación declarada de `lonely.psu="adjust"`) | 0.000653 · 0.994805 / 0.997366 |

**Qué cambió:** la varianza — de bootstrap simple de filas a diseño (`est_dis` × `upm`). **Qué NO cambió:** el punto, el universo, la codificación y el techo casi saturado (`hallazgo` de la propuesta). **A-bis.3:** el IC de fase 1 (`[0.994794, 0.997250]`, otro método) **no se compara** con éste; ninguna salida los pone lado a lado.

### 3.3 · Sensibilidad de ponderador (`B`, la cláusula `se_mueve_si`)

La propuesta escribió `se_mueve_si: "re-corrida con factor_per (ponderador oficial) reproduce p dentro del IC → carga tier FUERTE; fuera del IC → re-especificación"`. La re-corrida, pre-declarada y no adjudicada:

| RESULT | valor |
|---|---|
| `B-N-U` (`U_A` con `factor_per` finito > 0) · sin `factor_per` / cero / inválido | 14 887 · 0 / 0 / 0 |
| **`B-P`** (`factor_per`) · `B-DELTA-VS-A` | **0.9968063** · +0.000721 |
| `B-IC-LO` / `B-IC-HI` · `B-METODO-IC` | 0.995727 / 0.997758 · `IC-CON-ESTRATOS-DE-UPM-UNICA` |
| `B-EE-TAYLOR` · Taylor LO/HI | 0.000554 · 0.995721 / 0.997892 |
| **`B-CLAUSULA-SE-MUEVE-SI`** | **`DENTRO-DEL-IC-FASE1`** (0.994794 ≤ 0.996806 ≤ 0.997250) |

La lectura literal de la cláusula da `DENTRO`; su consecuencia («carga tier FUERTE») **es de mesa** (`NC-0183`). Este acto no carga nada ni escribe cita en `milpa/`.

### 3.4 · Consumidores

El único consumidor de la tasa (`milpa/tramite-ola5-propuesta-v0.yaml:110`, `SELLADA-SIN-CARGA`, archivo que el motor no carga) **no tiene cita GEN2 vigente** → por el encargo queda **listado para adopción de mesa** (`A-ADOPCION-P3 = LISTADO-PARA-MESA-REPRODUCE`). `usos.tsv` idéntico a `origin/main` es la prueba mecánica de cero adopciones. `familia.corresidencia.adulto_familiar_actual` (`MAESTRA33-C1`, ventana actual, misma reserva de ponderador) no es tasa de fase 1: queda nombrada como sucesor (`NC-0184`).

---

## 4 · Hallazgos

1. **El FD de EDER declara `est_dis` como `C (4)` y el archivo lo trae de ancho 3 en las 23 548 filas** (`G-PERFIL-EST-DIS = ancho=3:23548`; `upm` sí es 5 como el papel). Mismo síntoma que ENVIPE (`GEN2-R-SERIE-CSV`) y ENCUCI: **manda el archivo**, y por eso las llaves se leen como texto crudo. No mordió: 0 UPM cruzan estrato.
2. **`factor` vs `factor_per`:** el FD §1.1.3 llama a `factor` ponderador de la ENH (VIVIENDA/HOGAR/PERSONA) y a `factor_per` el de las personas de 20-54 de EDER; fase 1 usó `factor` sobre personas. Con `factor_per` el punto sube +0.07 pp y cae dentro del IC viejo — la cláusula que mesa escribió se cumple en su letra. La decisión no es de este acto.
3. **`RECENSO-DISENO-14` ya tenía la respuesta** (24/ago) y `FP-201` (31/ago) no la consultó. Herencia de un negativo sobre cinco fuentes sin abrir cinco descriptores: la lección de `feedback_fp201_falso_para_enif` vale para todas.
4. **`registro --verifica --escribe`:** `CALC-M-marco-M-sorteado-v1_3` proyectó `NO-REPRODUCE` en el dry-run y `REPLICA-RESULTADO` en dos `verify` aislados y en la pasada de escritura — el veredicto inestable in-process de `NC-0182`, reproducido una vez más. No se nombró en `--lote`; la escritura salió **sin ninguna transición** y con **cero pisadas** (`corridas.tsv`, `resultados.tsv`, `usos.tsv` idénticos a `origin/main` excluyendo las filas `CALC-EDER-0001`).

---

## 5 · P3 — el cierre de la fila: tabla final

| fuente | veredicto | qué cambió en varianza | qué NO cambió |
|---|---|---|---|
| ENVIPE 2025 | re-estimada (`CALC-ENVIPE-0001`, #653) | ya con diseño | — (fuera de este acto) |
| ENIF 2024 | re-estimada (`CALC-ENIF-0001`, #667) | ya con diseño | — |
| ENCUCI 2020 | re-estimada (`CALC-ENCUCI-0001`, #673) | ya con diseño | — |
| **ENNViH ola 2** | **declarada sin diseño con cita, enlazada a `NC-0156`** | nada: sigue bootstrap simple, rotulado | punto `0.174804`, `n = 6028` (`RES-0029/0030`) |
| **EDER 2017** | **re-estimada (`CALC-EDER-0001`)** | de bootstrap simple a IC de diseño `[0.994837, 0.997212]` (límite inferior, 3 estratos de UPM única) | punto `0.996086` (Δ −3.98e-07), `n = 14887`, universo, codificación, techo saturado |

**`NC-0086` → CERRADA.** Las dos fuentes pendientes quedaron con veredicto sellado; la espera de ENNViH tiene una sola fila (`NC-0156`).

---

## 6 · Límites declarados

- Una sola ola de EDER (2017); EDER 2011/2025 no se tocan.
- IC de diseño como **límite inferior** (3 estratos con UPM única, no colapsados ni descartados).
- Taylor secundaria con **aproximación declarada** de `lonely.psu="adjust"`; no sustituye a la primaria.
- `factor_per` es sensibilidad, **no** sucesor: cambia el estimando.
- El IC de fase 1 no se compara con ninguno de aquí (A-bis.3).
- Contaminación (ADR-46): la corrida no es ciega (spec §0.3).
- ENNViH: nada estimado; la vía oficial sigue en `NC-0156`.

---

## 7 · Contador

`cuenta_gen2 = SI` para `CALC-EDER-0001` — firma de contador con OBJETO, verbatim del encargo: «cuenta_gen2 = SI para los CALC sucesores que este acto selle (solo nacen si hay diseño que re-estimar)». Escrita en `data/corrida0/decisiones.tsv`; el merge la perfecciona. Contador de `NC`: `NC-0086` cerrada; nacen `NC-0183` y `NC-0184`.

---

## 8 · A.13 — qué se examinó

- Descriptores: `eder2017_fd.pdf` (7 521 líneas por `pdftotext -layout`), `eder2017_descripcion_calculoR.pdf` (516 líneas), ambos con sha256 en la spec.
- Cabeceras: los 5 `.csv` del ZIP de EDER (nombres de columna); 158 `.dta` de ENNViH ola 2 (nombres + etiquetas; ningún valor).
- Microdato (sólo en COMMIT-2, por el medidor sellado): `vivienda.csv`, `historiavida.csv`, `antecedentes.csv` de `eder2017_bases_csv.zip` (sha `bcc7eb90…`).
- Registro: `registro --verifica` re-ejecutó todos los CALC sellados con corpus (4m35s); `spec-check` 17/17 OK sobre 317 718 filas de inventario.
- Ningún archivo de ENVIPE/ENIF/ENCUCI se abrió. `milpa/` intocado (`git diff --stat origin/main -- milpa/` vacío).
