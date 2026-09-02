# ACTO MAESTRA35-L1 · RECORRE-Y-SEGMENTA — SPEC CONGELADA DEL LOTE (COMMIT-1)

**Fecha:** 2 de septiembre de 2026 · **Entorno:** UBUNTU · **Base:** `9e512da`.
**Encargo:** `forense/encargos/2026-09-02-MAESTRA35-L1-RECORRE-Y-SEGMENTA.md`
(`b1aab51`). **Censo previo:** `forense/notas/2026-09-02-MAESTRA35-L1-P0-censo.md`
(`0763c07`) — de ahí, y solo de ahí, salen los códigos de eje de este documento.

Este commit congela las cuatro specs **antes** de producir un solo resultado.
Los commits siguientes traen resultados por pieza y **no editan este documento**;
si una spec estaba mal, lo dice un commit posterior.

**Firma que gobierna el lote:** mesa, 2/sep/2026, `d1` = **`FP-238`**: «recorrer
`TRA-M-13/14` y re-medir `con_registro` con la llave correcta — acto CAJA, dos
commits, la cifra vieja se conserva con enmienda in situ». Firma citada: `DM`
(mesa, 1/sep/2026): «Si eso da eso da».

---

## §0 · Tres desviaciones de la letra del encargo, declaradas antes de medir

El censo `P0` encontró que tres supuestos del encargo no se sostienen contra el
dato. Ninguno tumba una pieza; los tres cambian cómo se ejecuta, y se declaran
aquí para que el commit de resultados no parezca haberlos decidido después.

1. **`P1` no puede unir por `(ID_TRA, NT_TIPO)`:** `sec_8` no trae `NT_TIPO` y
   no puede traerlo (es la rejilla persona × tipo, donde `ID_TRA` **es** llave
   única). Se une por **`ID_TRA`**, que es exacta y uno-a-muchos por
   construcción, con 0 huérfanos. **La sustancia de la firma `d1` queda intacta:
   lo que se corrige es la deduplicación, no la llave.** Se une «SIN deduplicar»
   exactamente como el encargo manda.
2. **`P3` pierde dos ejes y `P4` pierde uno**, por ausencia verificada en la
   fuente (§4.3 y §4.5 del censo). No se sustituyen por otros parecidos.
3. **`P4` no puede medir el corte de 15 000**: ENVIPE 2025 no publica umbral
   alguno. Se declara ausente y se añade `dominio_urbano_rural` como eje
   **propio y distinto**, no como su reemplazo.

## §1 · Lo que es idéntico en las cuatro piezas

- **Estimador:** `wprop_ic_conglomerado` de
  `tools/calibracion_mordida_encig_serie.py:81` — bootstrap conglomerado
  estratificado, remuestreo de UPM con reemplazo dentro de estrato,
  **10 000 réplicas, seed 42**. No se reescribe.
- **Una sola corrida por celda.** Sin reintentos.
- **Cada celda se rotula asociación, no coeficiente** (A-bis 1). Un eje con IC
  estrecho y signo esperado **no** autoriza escribir «el efecto de X es Y»
  (A-bis 2).
- **Comparaciones solo dentro de la misma corrida** (A-bis 3): se compara signo
  y razón entre celdas de un mismo eje. Nada se compara contra los 0.74/0.21/0.05
  de procedencia, ni `P3` contra `P4`, ni contra el 0.91 coercitivo, ni contra
  `civico.denuncia.miedo_desconfianza`: escalas distintas, sin enlace.
- **Tope:** cinco ejes por pieza, cuatro celdas por eje.
- **Cobertura < 90 % ⇒ universo restringido (A-bis 4)** para ese eje, que
  entonces **no** reconcilia sus celdas contra el marginal poblacional.

### 1.1 Vocabulario de veredicto por eje — y su precedencia

- **`CORROBORADA`**: las celdas extremas van en el signo esperado y sus IC95 **no
  se traslapan**.
- **`NO-DISCRIMINA`**: los IC95 de las celdas extremas se traslapan.
- **`DISCRIMINA`**: los IC95 no se traslapan, pero el eje no traía signo
  pre-registrado (o el signo no es evaluable). Es el veredicto máximo posible de
  un eje sin predicción.
- **`CONTRARIA`**: van en signo opuesto al esperado, sin traslape.
- **Precedencia:** `CONTRARIA` manda sobre `CORROBORADA` cuando un mismo eje da
  ambas en tramos distintos; se reporta además como **no monótono**.

### 1.2 Agrupación de escolaridad — una sola, para las tres encuestas

Congelada por el censo §4.1, que verificó que `NIV` **no** significa lo mismo en
las tres (ENIF invierte `04`/`05` y separa especialidad/maestría/doctorado):

| tramo | ENCIG 2025 | ENVIPE 2025 | ENIF 2024 |
|---|---|---|---|
| hasta primaria | `0,1,2` | `00,01,02` | `00,01,02` |
| secundaria | `3` | `03` | `03` |
| media superior | `4,5,6,7` | `04,05,06,07` | `04,05,06,07` |
| superior | `8,9` | `08,09` | `08,09,10,11` |
| **fuera** | blanco | `99`, blanco | `99`, blanco |

### 1.3 Tramos de edad — una sola definición

`18-29` · `30-44` · `45-59` · `60+` (60 a 96 años cumplidos). Fuera: códigos de
no especificada (`97`/`98`/`99` según la encuesta) y blanco.

---

## §2 · `P1` · `tramite.mordida.con_registro` recorrida sin deduplicar

**Es la única pieza que no segmenta: recorre.** Firma `d1`.

- **Payload:** `encig25_base_datos_csv`
  (`47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12`).
- **Tablas y llave:** `encig2025_04_sec_7.csv` (evento de trámite; `P7_3`) ⨝
  `encig2025_05_sec_8.csv` (persona × tipo; `P8_4`) **por `ID_TRA`**,
  `how='inner'`, **SIN deduplicar**. Guardias que PARAN: si `ID_TRA` deja de ser
  llave única en `sec_8`, o si aparece un solo `ID_TRA` de `sec_7` huérfano en
  `sec_8`, el script **para** y no reporta cifra.
- **Universo:** `P8_4 ∈ {'0','1'}` (la batería está gateada a nivel persona por
  `P8_3_*`; se hereda, no se resuelve) **y** `P7_3` en el canal de la celda.
- **Desenlace:** `y = 1` si `P8_4 == '1'`, `y = 0` si `P8_4 == '0'`.
- **Unidad de análisis:** **trámite**, no persona. Cada evento de `sec_7` cuenta
  una vez; `FAC_TRA` expande trámites. Quien hizo el mismo trámite tres veces
  aporta tres eventos — que es exactamente lo que la deduplicación de
  `MAESTRA34-L1` borró (3 835 eventos).
- **Ponderador / diseño:** `FAC_TRA`, `EST_DIS`, `UPM_DIS`.

**Dos mapeos de canal, ambos pre-declarados, ambos se reportan:**

| mapeo | digital / registrado | presencial |
|---|---|---|
| **principal** (el de `MAESTRA34-L1`, para que la corrección sea comparable con la cifra sellada) | `P7_3 ∈ {3,4,5}` | `P7_3 == '1'` |
| **sensibilidad A** (el de `MAESTRA34-L5`, con `3` fuera) | `P7_3 ∈ {4,5}` | `P7_3 == '1'` |

**Se reporta por canal:** `p̂`, IC95, n de eventos, estratos, UPM — **y la razón
presencial/digital con su signo**, que es lo comparable.

### 2.1 Decisión congelada antes de ver el número

- El resultado entra como **enmienda in situ fechada** bajo
  `tramite.mordida.con_registro_encig2025` en
  `milpa/tramite-ola5-propuesta-v0.yaml`, **con el cuerpo viejo intacto**
  (A.10 corolario 1), y como **filas nuevas** `TRA-M-13b` / `TRA-M-14b` en
  `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv` con
  `estado: SUSTITUYE-A TRA-M-13` / `SUSTITUYE-A TRA-M-14` (`FP-238`, firma
  `d1`). **Las filas viejas no se tocan.**
- **Si el IC95 nuevo del canal digital contiene `0.027358`** → se reporta
  **«corrección sin cambio material»**.
- **Si no lo contiene** → **«cifra sellada VENCIDA EN ALCANCE — re-sello de
  mesa»**, y se reclama `FP-241`.
- **En ningún caso se edita `milpa/tramite.yaml`.** El sello es de mesa, en RH.
- **Contra-hipótesis declarada:** si la razón presencial/digital cae **por
  debajo de 2×** con la llave correcta, el hallazgo de `MAESTRA34-L1` («el
  registro rompe la trampa social») queda **ACOTADO** y se dice. La cifra
  sellada hoy da 0.116000 / 0.027358 = **4.24×**.

---

## §3 · `P2` · `dinero.ahorro.via_informal` por ejes, ENIF 2024

- **Payload:** `enif_2024_bd_csv`
  (`00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039`),
  tabla `TMODULO.csv`.
- **Universo:** las **13 502** personas elegidas 18+ (`LLAVEMOD` llave única,
  `EDAD_V` 18-98, cero menores de 18 — verificado en el censo).
- **Ponderador / diseño:** `FAC_PER`, `EST_DIS`, `UPM_DIS`.

**Desenlaces:**

```
ahorra_solo_informal = (alguna P5_1_1..P5_1_6 == '1') ∧ (ninguna P5_6_1..P5_6_9 == '1')   [PRINCIPAL]
informal_cualquiera  = (alguna P5_1_1..P5_1_6 == '1')                                     [SECUNDARIO]
```

El **blanco por secuencia** en `P5_6_*` cuenta como **no** haber ahorrado por esa
vía — la misma lectura que `MAESTRA34-L5 P4` congeló (su **§1.3**, no §1.5 como
el encargo cita): sin cuenta no hay ahorro en esa cuenta.

### 3.1 Ejes, con los códigos que el censo fijó

| eje | ítem | celdas | cobertura |
|---|---|---|---|
| `sexo` | `SEXO` | 1 Hombre · 2 Mujer | 100.0000 % |
| `edad` | `EDAD_V` | 18-29 · 30-44 · 45-59 · 60+ | 99.8889 % |
| `escolaridad` | `NIV` | los 4 tramos de §1.2 | 99.9630 % |
| `localidad` | `TLOC` | `{1,2}` = 15 000 y más · `{3,4}` = menor de 15 000 | 100.0000 % |
| `formalidad` | `P3_13` | `{1..6}` = con seguridad social por el trabajo · `{7}` = sin | **68.9676 %** |
| `cuenta_formal` | `P5_4_1..9` | alguna `'1'` = con cuenta · ninguna = sin cuenta | 100.0000 % |

**`formalidad` declara universo restringido (A-bis 4)** y no reconcilia contra el
marginal poblacional: el 31 % fuera es blanco por secuencia (a quien no trabajó
no se le pregunta).

### 3.2 Pre-registro B-bis, escrito antes de abrir el dato

Mecanismo `G3` / `informal_sin_puente`: **`solo_informal` MÁS alto**…

| eje | signo esperado | veredictos posibles |
|---|---|---|
| `cuenta_formal` | más alto **sin cuenta** | ver §3.3 |
| `localidad` | más alto en **menor de 15 000** | `CORROBORADA` / `NO-DISCRIMINA` / `CONTRARIA` |
| `escolaridad` | más alto con **menor escolaridad** | idem |
| `formalidad` | más alto **sin trabajo formal** | idem |
| `edad` | **sin signo esperado** | `DISCRIMINA` / `NO-DISCRIMINA` |
| `sexo` | **sin signo esperado** (se mide, no se predice) | `DISCRIMINA` / `NO-DISCRIMINA` |

### 3.3 El eje de cuenta es NO-FALSABLE contra el desenlace principal

Hallazgo del censo §4.4: `P5_4_*` **gatea** a `P5_6_*`. Sin cuenta, las nueve
`P5_6_*` quedan en blanco por secuencia y `ahorra_solo_informal` **se reduce por
construcción del cuestionario** a `informal_cualquiera` en toda esa celda. El
signo esperado lo garantiza el instrumento, no la conducta. Congelado:

- Contra el **principal**: vocabulario limitado a `DISCRIMINA`/`NO-DISCRIMINA`.
  **Nunca `CORROBORADA`**, salga el número que salga.
- Contra el **secundario** (`informal_cualquiera`, que **no** está anidado en la
  tenencia): el eje **sí** es falsable, y ahí admite `CORROBORADA`/`CONTRARIA`,
  con el mismo signo esperado (más informal sin cuenta).

**Escala:** proporción. Nada contra los 0.74 / 0.21 / 0.05 de procedencia.

---

## §4 · `P3` · `tramite.gobierno_digital.util_sin_coercion` por ejes, ENCIG 2025

- **Payload:** `encig25_base_datos_csv` (mismo sha256 que `P1`).
- **Desenlace y universo EXACTOS de `MAESTRA34-L5 P1`, la dicotomización NO se
  toca:** `N_TRA == '01'` (pago ordinario del servicio de luz);
  `adopta = P7_3 ∈ {4,5}`; `no adopta = {1,2,6}`; **fuera** `{3,7,8,9,blanco}`.
- **Ponderador / diseño:** `FAC_TRA`, `EST_DIS`, `UPM_DIS`.
- **Unidad = TRÁMITE** (quien pagó doce veces contribuye doce veces, como en
  `L5`): **se declara en cada celda**. n del universo = **20 203**.
- **Llave a los ejes:** `ID_TRA --(sec_7)--> ID_PER --> encig2025_02_residentes_sec_2`,
  verificada en el censo con **0 ausentes de 33 963**. La pieza **no** para.
- **Diff sobre `tools/medidor_gobierno_digital_encig25.py`:** gana un parámetro
  de eje y nada más. El diff se declara en el commit de resultados.

### 4.1 Ejes

| eje | ítem | celdas | cobertura |
|---|---|---|---|
| `sexo` | `residentes.SEXO` | 1 Hombre · 2 Mujer | 100.0000 % |
| `edad` | `residentes.EDAD` | los 4 tramos de §1.3 | 99.4308 % |
| `escolaridad` | `residentes.NIV` | los 4 tramos de §1.2 | 100.0000 % |
| ~~localidad~~ | — | **AUSENTE**: el universo de ENCIG son ciudades de 100 mil y más (FD pág. 1) | — |
| ~~formalidad~~ | — | **AUSENTE**: no hay ítem de prestaciones ni seguridad social en el FD | — |

### 4.2 Pre-registro B-bis

**Adopción MÁS alta** con **mayor escolaridad** y con **menor edad**;
`sexo` **sin signo predicho**. La predicción de localidad del encargo
(«15 000+») queda **sin objeto**: el eje no existe en esta fuente.

| eje | signo esperado | veredictos posibles |
|---|---|---|
| `escolaridad` | más alto en **superior** | `CORROBORADA` / `NO-DISCRIMINA` / `CONTRARIA` |
| `edad` | más alto en **18-29** | idem |
| `sexo` | ninguno | `DISCRIMINA` / `NO-DISCRIMINA` |

---

## §5 · `P4` · `tramite.evasion_norma` por ejes, ENVIPE 2025

- **Payload:** `envipe2025_csv`
  (`8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa`).
- **Desenlace y universo EXACTOS de `MAESTRA34-L5 P3`:** universo = delitos con
  `BP1_20 ∈ {1,2}` (n = **40 280**);
  `evade_norma = 1 ⟺ BP1_20 == '2' ∧ BP1_23 ∈ {04,05,06,08}`.
  **Es la CONJUNTA, no la condicional** — se repite en cada celda.
- **Ponderador / diseño:** `FAC_DEL`, `EST_DIS`, `UPM_DIS`.
- **Unidad = DELITO.** Se declara en cada celda.
- **Llave delito→persona:** `ID_PER` (`tmod_vic` → `tsdem`), verificada con
  **0 huérfanos de 22 295**. `sexo` y `edad` viven en `tmod_vic` y no necesitan
  el join. La pieza **no** para.
- **Diff sobre `tools/medidor_evasion_norma_envipe25.py`:** gana un parámetro de
  eje y nada más.

### 5.1 Ejes

| eje | ítem | celdas | cobertura |
|---|---|---|---|
| `sexo` | `tmod_vic.SEXO` | 1 Hombre · 2 Mujer | 100.0000 % |
| `edad` | `tmod_vic.EDAD` | los 4 tramos de §1.3 | 99.7666 % |
| `escolaridad_proxy` | `tsdem.NIV` vía `ID_PER` | los 4 tramos de §1.2 | 99.7517 % |
| `dominio_urbano_rural` | `tmod_vic.DOMINIO` | `U` Urbano · `C` Complemento urbano · `R` Rural | 100.0000 % |
| ~~localidad-15k~~ | — | **AUSENTE**: ENVIPE 2025 no publica `TLOC` ni umbral alguno | — |
| ~~formalidad~~ | — | **AUSENTE**: no hay ítem de prestaciones ni seguridad social | — |

### 5.2 Pre-registro B-bis — y por qué esta pieza casi no predice

La `nota_segmentacion` de la regla pide **formalidad laboral** (subsistencia vs
cinismo). No existe en ENVIPE 2025. Se aplica **la salida que el propio encargo
declaró**: `escolaridad` entra como **proxy**, dicho proxy.

| eje | signo esperado | veredictos posibles |
|---|---|---|
| `escolaridad_proxy` | **ninguno** — la regla NO predice signo por escolaridad: las dos evasiones (subsistencia y cinismo) empujan en sentidos opuestos | **`DISCRIMINA` / `NO-DISCRIMINA`, nunca `CORROBORADA`** |
| `dominio_urbano_rural` | **ninguno evaluable** — la predicción del encargo («menor de 15 000 más alta, sanción menos creíble») estaba escrita sobre un corte que esta fuente no publica; que `R` ↔ «menor de 15 000» **no está verificado en ninguna fuente del payload** | **`DISCRIMINA` / `NO-DISCRIMINA`** |
| `edad` | ninguno (el encargo lo dice: «tramos de edad sin predicción») | `DISCRIMINA` / `NO-DISCRIMINA` |
| `sexo` | ninguno | `DISCRIMINA` / `NO-DISCRIMINA` |

Esta pieza **no puede producir una `CORROBORADA`**, por diseño y no por
resultado. Mide y describe; es todo lo que la fuente permite.

---

## §6 · Lo que cada pieza escribe al cerrar

Entrada nueva **al pie** de `milpa/tramite-ola5-propuesta-v0.yaml`
(`P1` es enmienda in situ; las otras tres son entradas nuevas), cada una con:
bloque `celdas:` (eje → celda → `p`, `ic95`, `n`, cobertura del eje),
`veredicto_por_eje`, `situacion: PENDIENTE-DE-MESA`, `tier: PENDIENTE-DE-MESA`,
`sha256_payload` y `payload_manifiesto_id`.

- `tramite.mordida.con_registro_encig2025` — enmienda in situ (`P1`)
- `dinero.ahorro.via_informal_ejes_enif2024` (`P2`)
- `tramite.gobierno_digital.util_sin_coercion_ejes_encig2025` (`P3`)
- `tramite.evasion_norma_ejes_envipe2025` (`P4`)

**Ninguna se carga al motor.** El sello es de mesa al cierre, en formato RH:
número, opción, qué cambia en el motor.

---

## §7 · Sello

**El primer resultado que produzca este procedimiento es el que se reporta.**
