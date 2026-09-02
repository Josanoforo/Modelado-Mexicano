# ACTO MAESTRA35-L1 · P0 · CENSO A.4 de ejes de segmentación

**Fecha:** 2 de septiembre de 2026 · **Entorno:** UBUNTU · **Base:** `9e512da`
(el encargo se redactó contra `11af678`; `main` avanzó por el merge de la
propia compuerta, `PR #468`).
**Encargo:** `forense/encargos/2026-09-02-MAESTRA35-L1-RECORRE-Y-SEGMENTA.md`
(archivado verbatim en `b1aab51`).
**Script:** `tools/censo_ejes_maestra35_l1.py` — su salida cruda es lo que este
documento transcribe.

Este censo se corrió **antes** de cualquier medición y **sin cruzar jamás
ningún eje contra ningún desenlace**: aquí solo hay llaves, códigos y
denominadores. Los códigos de cada eje **no se infieren del nombre de la
variable**: salen del FD o del catálogo del propio payload, citados fila por
fila abajo.

## 0 · Payloads y sus firmas

| payload | sha256 | tablas usadas |
|---|---|---|
| `encig25_base_datos_csv` | `47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12` | `encig2025_04_sec_7.csv`, `encig2025_05_sec_8.csv`, `encig2025_02_residentes_sec_2.csv`, `encig2025_01_sec1_A_3_4_5_8_9_10.csv` |
| `enif_2024_bd_csv` | `00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` | `TMODULO.csv` |
| `envipe2025_csv` | `8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa` | `tmod_vic_…csv`, `tsdem_…csv` |

Fuentes de códigos (documentos, no memoria):
`data/raw/encig25_estructura_base_datos.pdf` (FD de ENCIG 2025),
`data/raw/enif_2024_fd.xlsx` (FD de ENIF 2024, hoja `TMODULO`),
los `diccionario_de_datos/` y `catalogos/` **dentro** de
`envipe2025_csv.zip`, y `data/raw/fd_envipe2025.pdf`.

---

## 1 · Pregunta (i) del encargo — ¿`encig2025_05_sec_8.csv` trae `NT_TIPO`?

**NO.** Y la premisa que el encargo construye encima resulta **falsa en la
mecánica y verdadera en el fondo**. Los números:

```
sec_8 trae NT_TIPO: False
sec_7: 124,314 filas · ID_TRA distintos 113,717 · (ID_TRA,NT_TIPO) grupos 124,314
sec_8: 1,083,672 filas · ID_TRA distintos 1,083,672 · ID_TRA es llave única: True
ID_PER en sec_8: 40,136 · N_TRA distintos: 27 · 40136 x 27 = 1,083,672
ID_TRA de sec_7 sin fila en sec_8 (huérfanos): 0
```

Lo que esto dice, y que ni el encargo ni `ADR-287` tenían del todo:

- **`sec_8` no está al grano de evento.** Es la rejilla completa
  persona × tipo-de-trámite: 40 136 informantes × 27 tipos = 1 083 672 filas
  exactas, y `ID_TRA` es su **llave única**. `NT_TIPO` no está ahí porque no
  tiene dónde estar: `sec_8` no distingue eventos repetidos del mismo tipo.
- **`sec_7` sí está al grano de evento**, y ahí `(ID_TRA, NT_TIPO)` es llave
  única (124 314 grupos para 124 314 filas), tal como `ADR-287` midió.
- Por lo tanto **el join `sec_7 × sec_8` por `ID_TRA` es exacto y
  uno-a-muchos por construcción**: cada evento de `sec_7` recibe exactamente
  un `P8_4`, y no hay un solo huérfano (0 de 113 717).

**Veredicto A.4 de la pieza P1: `EXISTE-NO-SATISFACE`**, tal como el encargo
anticipó — pero por una razón distinta de la que supuso. El defecto de
`MAESTRA34-L1` **no fue la llave del join**: fue la **deduplicación posterior**.
La mejor llave disponible es `ID_TRA`, no se inventa ninguna, y no hace falta:

```
universo P8_4 ∈ {0,1}: 21,139 filas de sec_8; al bajar a evento de sec_7
  -> 24,974 eventos en 21,139 ID_TRA
eventos que una deduplicación por ID_TRA descartaría: 3,835
ID_TRA con más de un evento: 2,576
   ...de esos, con P7_3 distinto entre sus eventos: 160
valores de P7_3 en sec_7: ['1','2','3','4','5','6','7','8','9','NA']
```

Los tres números de `ADR-287` (24 974 / 21 139 / 3 835, y 2 576 / 160) se
**reproducen exactos**. La corrección que la firma `d1` pide sigue en pie sin
cambio de fondo: *no deduplicar*.

### 1-bis · Una afirmación del marco sellado que el censo desmiente

`TRA-M-13` declara en su `universo_filtro`, verbatim:

> `sec_7 (124314 filas, 113717 ID_TRA unicos tras deduplicar 10597 duplicados`
> `EXACTOS -- verificado, mismos valores en P7_3/FAC_TRA/EST_DIS/UPM_DIS)`

Contado sobre `sec_7` completo:

```
ID_TRA con más de una fila: 7,430
   ...que DIFIEREN en P7_3   :   501
   ...que DIFIEREN en FAC_TRA:     0
   ...que DIFIEREN en EST_DIS:     0
   ...que DIFIEREN en UPM_DIS:     0
   ...que DIFIEREN en N_TRA  :     0
   ...que DIFIEREN en NT_TIPO: 7,430
filas repetidas idénticas en TODAS las columnas salvo NT_TIPO: 5,860 de 18,027
```

La mitad de la afirmación se sostiene (`FAC_TRA`, `EST_DIS`, `UPM_DIS`
efectivamente no varían) y **la otra mitad no**: 501 `ID_TRA` repetidos traen
`P7_3` distinto entre sus filas, y solo 5 860 de 18 027 filas repetidas son
idénticas en todo lo demás. No eran duplicados exactos: eran **eventos de
trámite distintos del mismo tipo hechos por la misma persona**, que es
precisamente para lo que existe `NT_TIPO`. La fila sellada **no se edita**
(`ADR`/`ENMIENDA-1-PROCEDIMIENTO-R`); esto entra como `TRA-M-13b`/`TRA-M-14b`.

## 2 · Pregunta (ii) — tabla de persona de ENCIG 2025 y llave trámite→persona

```
residentes_sec_2: 123,181 filas · ID_PER llave única: True · ID_VIV 40,136
informantes (sec1_A): 40,136 · presentes en residentes: 40,136
ID_PER de sec_7 presentes en residentes: 0 ausentes de 33,963
```

**Llave declarada: `ID_TRA --(sec_7)--> ID_PER --> encig2025_02_residentes_sec_2`.**
Cobertura perfecta: cero trámites sin persona. La pieza `P3` **no** para.
`residentes_sec_2` es la tabla de persona y trae `SEXO`, `EDAD`, `NIV`, `GRA`,
`C_ACT`, `V_ACT`, `POS`.

## 3 · Pregunta (iii) — tabla de persona de ENVIPE 2025 y llave delito→persona

```
tmod_vic: 40,280 delitos · ID_PER distintos 22,295 · trae SEXO y EDAD en la propia tabla: True
tsdem   : 300,654 personas · ID_PER llave única: True
delitos cuyo ID_PER no aparece en tsdem: 0 de 22,295
```

**Llave declarada: `ID_PER`.** `sexo` y `edad` ni siquiera necesitan el join
(viven en `tmod_vic`); `escolaridad` sí. Cero huérfanos. La pieza `P4` **no**
para.

---

## 4 · Pregunta (iv) — los ejes, con sus códigos y sus denominadores

### 4.1 Códigos de escolaridad: las tres encuestas **no** comparten codificación

Verificado uno por uno contra el FD/catálogo de cada payload. `NIV` se llama
igual en las tres y **no significa lo mismo**:

| código | ENCIG 2025 (FD, 1 dígito) | ENVIPE 2025 (`catalogos/niv.csv`, 2 dígitos) | ENIF 2024 (FD xlsx, 2 dígitos) |
|---|---|---|---|
| 4 / 04 | Carrera técnica con secundaria | Carrera técnica con secundaria | **Normal básica** |
| 5 / 05 | Normal básica | Normal básica | **Estudios técnicos con secundaria** |
| 9 / 09 | Maestría **o doctorado** | Maestría **o doctorado** | Especialidad |
| 10, 11 | — | — | Maestría; Doctorado |

**ENIF invierte 04/05** respecto de las otras dos, y separa
especialidad/maestría/doctorado donde las otras agregan. Agrupados a los cuatro
tramos que el encargo pide la inversión no altera el tramo (ambos caen en
«media superior»), pero cualquier uso a nivel de código suelto sí se vería
afectado. Agrupación congelada, idéntica en las tres:

- **hasta primaria** = {0/00, 1/01, 2/02} · **secundaria** = {3/03}
- **media superior** = {4..7 / 04..07} · **superior** = {8,9 / 08..11}
- fuera: 99 «no sabe», blanco.

### 4.2 ENCIG 2025 — universo de `P1` (`P8_4 ∈ {0,1}` y `P7_3` válido)

n = **19 541 eventos** de trámite, 4 078 personas distintas.

| eje | cobertura | celdas (n) |
|---|---|---|
| sexo (`residentes.SEXO`) | **100.0000 %** | 1 Hombre 11 902 · 2 Mujer 7 639 |
| edad (`residentes.EDAD`) | **99.6878 %** | 18-29 4 177 · 30-44 8 697 · 45-59 4 767 · 60+ 1 839 · (fuera 61) |
| escolaridad (`residentes.NIV`) | **100.0000 %** | hasta primaria 701 · secundaria 2 508 · media superior 5 125 · superior 11 207 |
| tamaño de localidad | — | **NO-ENCONTRADO** |
| formalidad laboral | — | **NO-ENCONTRADO** |

### 4.3 ENCIG 2025 — universo de `P3` (`N_TRA='01'`, `P7_3 ∈ {1,2,4,5,6}`)

n = **20 203 trámites** = 20 203 personas (coincide exacto con la n de
`MAESTRA34-L5 P1`).

| eje | cobertura | celdas (n) |
|---|---|---|
| sexo | **100.0000 %** | 1 Hombre 9 998 · 2 Mujer 10 205 |
| edad | **99.4308 %** | 18-29 2 806 · 30-44 7 008 · 45-59 5 799 · 60+ 4 475 · (fuera 115) |
| escolaridad | **100.0000 %** | hasta primaria 2 299 · secundaria 4 216 · media superior 5 582 · superior 8 106 |
| tamaño de localidad | — | **NO-ENCONTRADO** |
| formalidad laboral | — | **NO-ENCONTRADO** |

**Los dos `NO-ENCONTRADO` de ENCIG, con su prueba:**

- **Tamaño de localidad.** El universo de la encuesta es «la población de 18
  años y más **en ciudades de 100 mil habitantes o más**» (FD, pág. 1,
  verbatim). `NOM_AREAM` tiene 33 áreas y una de ellas se llama literalmente
  «RESTO DE CIUDADES DE 100 MIL HABITANTES Y MÁS». El corte de 15 000 que el
  encargo pide **no existe en ENCIG por diseño muestral**, no por omisión.
- **Formalidad laboral.** La tabla de residentes cierra en `POS` («posición en
  la ocupación»: jornalero / empleado / cuenta propia / patrón / sin pago), que
  es posición, **no** prestaciones. Negativo con control positivo sobre el FD
  (4 540 líneas, 585 210 bytes examinados):
  `prestacion` → 0 · `seguridad social` → 0 · `aguinaldo` → 0 ·
  **control positivo** `SEXO` → 1, `NIV` → 16, `POS` → 22.
  `IMSS` da 16 aciertos y `ISSSTE` 12, todos en la sección 5 (evaluación del
  **servicio de salud** del IMSS) y en el catálogo de tipos de trámite —
  ninguno es un ítem de derechohabiencia por el trabajo; revisados uno por uno.

Ninguno de los dos se sustituye por otro parecido (regla del propio encargo).
`P3` corre con **tres** ejes.

### 4.4 ENIF 2024 — universo de `P2` (las 13 502 personas elegidas de `TMODULO`)

`LLAVEMOD` es llave única; `EDAD_V` 18-98, cero menores de 18. **Los seis ejes
viven en la misma tabla: no hace falta ninguna llave.**

| eje | ítem | cobertura | celdas (n) |
|---|---|---|---|
| sexo | `SEXO` | **100.0000 %** | 1 Hombre 6 082 · 2 Mujer 7 420 |
| edad | `EDAD_V` | **99.8889 %** | 18-29 2 924 · 30-44 4 256 · 45-59 3 411 · 60+ 2 896 · (fuera 15) |
| escolaridad | `NIV` | **99.9630 %** | hasta primaria 3 249 · secundaria 3 635 · media superior 3 408 · superior 3 205 · (fuera 5) |
| tamaño de localidad | `TLOC` | **100.0000 %** | 15 000 y más 8 856 · menor de 15 000 4 646 |
| formalidad laboral | `P3_13` | **68.9676 %** ⚠ | con seg. social 4 170 · sin 5 142 · (fuera 4 190) |
| tenencia de cuenta | `P5_4_1..9` | **100.0000 %** | con cuenta 9 156 · sin cuenta 4 346 |

- **`TLOC` da el corte exacto que el encargo pide**, por FD: 1 = 100 000 y más;
  2 = 15 000 a 99 999; 3 = 2 500 a 14 999; 4 = menor de 2 500. Congelado:
  `{1,2}` = 15 000 y más, `{3,4}` = menor de 15 000.
- **`P3_13` es el ítem de formalidad**, por FD: «3.13 Por parte de su trabajo,
  ¿usted tiene derecho a los servicios médicos… 1 IMSS · 2 ISSSTE · 3 ISSSTE
  estatal · 4 PEMEX/Defensa/Marina · 5 seguro privado · 6 otra institución ·
  7 Entonces, ¿carece de derecho a servicios médicos por parte de su trabajo…?
  · 9 No sabe · b blanco por secuencia». Congelado: `{1..6}` = con seguridad
  social por el trabajo, `{7}` = sin.
- ⚠ **`P3_13` cubre 68.97 % < 90 %.** La pieza `P2` declara **universo
  restringido (A-bis 4)** para ese eje y **NO reconcilia sus celdas contra el
  marginal poblacional**. El 31 % fuera es blanco por secuencia: a quien no
  trabajó no se le pregunta.

**Hallazgo del P0 sobre el eje de cuenta — anidamiento por secuencia.**
`P5_4_*` («¿usted **tiene** cuenta o tarjeta de X?») **gatea** a `P5_6_*`
(«¿guardó o **ahorró en** esa cuenta?»), que es la pata formal del desenlace de
`P2`. Sin ninguna cuenta, las nueve `P5_6_*` quedan en blanco por secuencia, y
`ahorra_solo_informal = (alguna P5_1_*) ∧ (ninguna P5_6_*)` **se reduce por
construcción del cuestionario** a `informal_cualquiera` en toda la celda «sin
cuenta». El eje no puede refutar el mecanismo contra el desenlace principal:
el signo esperado está garantizado por el instrumento, no por la conducta.
Consecuencia congelada en la spec: contra el desenlace **principal** el eje de
cuenta se pre-registra como **NO-FALSABLE por construcción** y su vocabulario
de veredicto se limita a `DISCRIMINA`/`NO-DISCRIMINA`; contra el desenlace
**secundario** (`informal_cualquiera`, que no está anidado en la tenencia) el
eje **sí** es falsable y ahí sí admite `CORROBORADA`/`CONTRARIA`.

### 4.5 ENVIPE 2025 — universo de `P4` (`BP1_20 ∈ {1,2}`, unidad delito)

n = **40 280 delitos**, 22 295 personas distintas.

| eje | ítem | cobertura | celdas (n) |
|---|---|---|---|
| sexo | `tmod_vic.SEXO` | **100.0000 %** | 1 Hombre 19 399 · 2 Mujer 20 881 |
| edad | `tmod_vic.EDAD` | **99.7666 %** | 18-29 11 871 · 30-44 15 214 · 45-59 8 620 · 60+ 4 481 · (fuera 94) |
| escolaridad | `tsdem.NIV` vía `ID_PER` | **99.7517 %** | hasta primaria 3 491 · secundaria 7 739 · media superior 11 476 · superior 17 474 · (fuera 100) |
| dominio | `tmod_vic.DOMINIO` | **100.0000 %** | Urbano 28 471 · Complemento urbano 8 039 · Rural 3 770 |
| tamaño de localidad (corte 15 000) | — | — | **NO-ENCONTRADO** |
| formalidad laboral | — | — | **NO-ENCONTRADO** |

**Los dos `NO-ENCONTRADO` de ENVIPE, con su prueba:**

- **Tamaño de localidad al corte de 15 000.** ENVIPE 2025 **no publica `TLOC`**.
  Barrido de los 6 diccionarios del ZIP (2 225 líneas examinadas): la única
  variable de tamaño es `DOMINIO`, con exactamente tres claves y **sin un solo
  umbral de población**: `U` Urbano, `C` Complemento urbano, `R` Rural.
  `fd_envipe2025.pdf` (7 207 líneas, 782 014 bytes) repite las mismas tres
  etiquetas en sus cuatro apariciones y tampoco trae umbral: sondas
  `15 000` → 0, `100 000` → 0, `2 500` → 0, con **control positivo**
  `ENVIPE` → 112 y `Complemento urbano` → 6. **El corte de 15 000 no se
  inventa.**
- **Formalidad laboral.** `tsdem` cierra en `AP3_10` («posición en la
  ocupación», mismos cinco códigos que `POS` de ENCIG). Sondas sobre el FD
  (7 207 líneas) y sobre `cuest_principal_envipe2025.pdf` (987 líneas,
  132 175 bytes): `prestacion` → 0, `seguridad social` → 0, `IMSS` → 0,
  `aguinaldo` → 0, con control positivo `ENVIPE` → 112 y → 14 respectivamente.
  Se aplica **la salida que el propio encargo declaró**: escolaridad como
  **proxy** de formalidad, dicho como proxy.

**Decisión de diseño que este acto toma y declara (no es sustitución).**
`DOMINIO` **no** se usa como el eje de 15 000: ese se declara ausente. Se añade
como **eje propio y distinto**, `dominio_urbano_rural`, con sus tres celdas
publicadas y con la advertencia de que la correspondencia `R` ↔ «menor de
15 000» **no está verificada en ninguna fuente del payload**. Por eso su
vocabulario de veredicto se limita a `DISCRIMINA`/`NO-DISCRIMINA`: la
predicción de signo del encargo estaba escrita sobre el corte de 15 000, y ese
corte no es el que se mide. Total de ejes en `P4`: **4** (tope: 5).

---

## 5 · Resumen A.4 por pieza

| pieza | veredicto de entrada | ejes que corren | ejes ausentes | universo restringido |
|---|---|---|---|---|
| `P1` ENCIG mordida | **EXISTE-NO-SATISFACE** (la cifra existe, la deduplicación estaba mal) | — (P1 no segmenta: recorre) | — | no |
| `P2` ENIF ahorro | **EXISTE-SATISFACE** | sexo, edad, escolaridad, localidad, formalidad, cuenta (6) | ninguno | **sí**, solo el eje formalidad (68.97 %) |
| `P3` ENCIG digital | **EXISTE-SATISFACE** (llave `ID_PER` verificada) | sexo, edad, escolaridad (3) | localidad, formalidad | no |
| `P4` ENVIPE evasión | **EXISTE-SATISFACE** (llave `ID_PER` verificada) | sexo, edad, escolaridad-como-proxy, dominio (4) | localidad-15k, formalidad | no |

Ninguna pieza PARA. Ninguna celda de ningún eje se cruzó contra ningún
desenlace en este commit.
