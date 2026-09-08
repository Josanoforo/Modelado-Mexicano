# Codebooks abiertos y `spec.yaml` congeladas — `ACTO GEN2-E5-0 · SPECS EJECUTABLES`

**Fecha:** 8/sep/2026 · **Entorno:** UBUNTU (caja), corpus montado · **Modelo:** Opus
**Base:** `origin/main = d8b5f0b` · **Rama:** `acto/gen2-e5-0-specs-ejecutables`

**Esta nota no trae ningún número del modelo** — ninguna proporción, ningún IC95,
ninguna celda, ninguna `n` de universo. Las únicas cifras que aparecen son
**contadores de auditoría** que A.13 exige (cuántos archivos y cuántas variables
examinó cada barrido) y **números de página** de codebook. El acto terminó en el
`COMMIT-1`: **no abrió microdato y no calculó**.

---

## 1 · Qué se abrió, con id de manifiesto y página

| id de manifiesto | qué se abrió | cómo | para qué |
|---|---|---|---|
| `cide_cses2015_nacional_poselectoral` | metadato del `.sav` | `pyreadstat.read_sav(metadataonly=True)` | códigos de `pcyc13`/`pcyc14`, desenlace, ponderador |
| `cide_cses2015_nacional_preelectoral` | metadato del `.sav` | ídem | réplica del disparador; desenlace de otro cargo |
| `cide_cses2015_estatal_preelectoral` | metadato del `.sav` | ídem | `pvoto1`/`pvoto2`/`pvoto3` |
| `mexico_lapop_americasbarometer_2019_v1_0_w` | metadato del `.dta` | `read_dta(metadataonly=True)` | búsqueda del desenlace de denuncia; escalas; UPM/estrato |
| `mex_2021_lapop_americasbarometer_v1_2_w` | metadato del `.dta` | ídem | ídem |
| `mex_2023_lapop_americasbarometer_v1_0_w` | metadato del `.dta` | ídem | ídem |
| `ennvih1_2002_hogar_dta` | metadato de 9 miembros `.dta` | ídem, desde el zip | tablas de institución, llaves, presencia de variables |
| `ennvih1_2002_ponderador` | metadato de 2 miembros `.dta` | ídem | `fac_3b`, `fac_3b_px`, `fac_3a_px` |
| `ennvih1_2002_hogar_q` | **`ehh02q_b3b.pdf`**, cuestionario del Libro IIIB | `zipfile-deflate64` + `pdftotext` | **ventanas** de `ES09` (**pág. 5**), `EC01` (**pág. 10**), `CE01` (**pág. 12**), `HS01` (**pág. 18**) |
| `ehh02cb_b3b` | manual de codificación del Libro IIIB (suelto en la raíz) | `pdftotext` | **códigos** de `es09` (**pág. 8**), `ec01*` (**pág. 18**), `ce01` (**pág. 21**), `hs01` (**pág. 28**) |
| `ennvih1_2002_hogar_cb` | **`ehh02cb_bx.pdf`**, manual del Libro Proxy | `zipfile-deflate64` + `pdftotext` | **códigos** del brazo `bx`: `es09` (**pág. 49**), `ce01` (**pág. 56**), `hs01` (**pág. 60**) |

Los tres payloads de `ENNViH` y los dos manuales **ya estaban en la raíz** — no se
pidió ninguna descarga (`/acto` paso 3: «si el censo lista el archivo, no se pide»).

---

## 2 · A.8 — `ya_medido.py` sobre las reglas que este acto pre-registra

`python3 tools/ya_medido.py R10.3` → **`MEDIDA-EN: L18`**. Es la corrida de 2004 de
`comunicacion.inseguridad.ver_oir_callar` (`veredicto_Bbis = NO-DISCRIMINA`,
`SELLADA-SIN-CARGA`). **Este acto no la re-mide, no la reclasifica y no la
mueve**: congela la cara mecánica de una spec ya sellada, y su `CALC` declara
explícitamente `veredicto_D2h: NO-CONSTRUIBLE`.

`ya_medido.py` sobre `S12`/`S6` devuelve las piezas gemelas ya `SELLADA-SIN-CARGA`
que las specs selladas ya citan (`…_lapop2019`, `salud.atencion.grave_ennvih2002`
en `NO-ESTIMABLE-EN-v1_1`). Ninguna se toca.

---

## 3 · Los tres veredictos del acto

| `CALC` | spec sellada | estado |
|---|---|---|
| `CALC-0001` | `prereg-caja-S12` (`870522a3…`) | `PRE-FLIGHT: VERDE` |
| `CALC-0002` | `prereg-caja-S13` (`c41235b8…`) | `PRE-FLIGHT: VERDE` · **ruta (c)** |
| `CALC-0003` | `prereg-caja-S6-L16` v1.2 (`c1cd3b63…`) | `PRE-FLIGHT: VERDE` |

`spec-check`: **117 pares (archivo, variable) declarados, 0 FAIL**, sobre 317 718
filas de inventario examinadas en cada corrida (22 · 21 · 74).

---

## 4 · Los cuatro hallazgos que cambian lo que la corrida de `ACTO GEN2-E5` va a hacer

### 4.1 · `es09` no tiene el código `0` — `CALC-0003` habría salido degenerado

`S6 v1.2 §1` congeló «`T1 = 0` si `es09 == 0`». Los `.dta` de `ENNViH` 2002 **no
traen ninguna etiqueta de valor**, así que el manual es la única autoridad, y dice
que «No» es **`3`**: el `0` no existe. Corrida verbatim, el grupo `T = 0` habría
quedado **vacío**, sin error y sin aviso, y las **seis filas** de contraste habrían
salido indefinidas. Se congela `no: 3`, **sin editar la spec sellada**, y se declara.
Fuente: `ehh02cb_b3b.pdf` pág. 8 y `ehh02cb_bx.pdf` pág. 49.
**Es exactamente el defecto que este acto existe para atrapar.** → `FP-349`.

### 4.2 · El desenlace que `S12` dio por no construible **existe**

`S12 §2` declaró el desenlace `NO-CONSTRUIBLE-SIN-CODEBOOK` y mandó abrir el
cuestionario antes de decidir. Abierto: **`peledip`**, voto emitido para diputados
federales del 7-jun-2015 — la misma elección de la campaña que `pcyc13`/`pcyc14`
preguntan. El falsador principal **no** queda `NO-ESTIMABLE`. Tres correcciones de
premisa se declaran con él: (i) el desenlace existe; (ii) el archivo llamado
`nacional_preelectoral` trae ítems **post**-electorales; (iii) por eso **no es
réplica del desenlace** — su voto emitido es de **otro cargo**. → `FP-350`.

### 4.3 · Los códigos de partido de oferente y de voto **no son el mismo esquema**

`pcyc13_1` y `peledip` coinciden en los códigos `3, 4, 8, 9, 10, 12` con **partidos
distintos** (p. ej. `4` es PT en uno y PRD en el otro). Una igualdad directa
`oferente == voto` habría producido alineamientos falsos **sin error**. El crosswalk
va congelado código a código en el `spec.yaml`, con la coalición `PRI-PVEM`
resuelta antes del dato.

### 4.4 · `S13` ruta **(c)**: no hay desenlace de denuncia en ninguna ola ≥2019

El desenlace de la corrida 2004 es `aoj1` (leído en la nota de `LOTE-LAPOP`).
**Ausente en las tres olas**, y el barrido por etiqueta (`denunc|report`) da **0
aciertos**. **Control positivo del negativo (A.13):** las tres olas traen etiqueta
en **el 100 % de sus variables** — **3 archivos, 678 variables examinadas** — así
que el cero no es un archivo mudo leído como vacío. `veredicto_D2h:
NO-CONSTRUIBLE`; **`S13 v1.1` no se escribe**, porque la ruta (b) no se dispara y
escribirla habría sido inventar un desenlace sin mandato de mesa.

---

## 5 · Lo que el codebook confirmó de las specs, y lo que corrigió

**Confirmó** (no supuesto): las tres tablas de institución de `S6 §2.1` casan con
el `.dta` **sin un solo desajuste** (0 declaradas-y-ausentes, 0 reales-sin-
clasificar, erratas `IMMS`/`CONsultorio` incluidas) — **ninguna reclasificación**;
y `fac_3a_px`/`fac_3b_px` comparten **etiqueta idéntica**, que es justo por lo que
`S6 §3.2` mandó correr la pareja en vez de adjudicar.

**Corrigió, declarado y no absorbido:**

- **`S6 §3.5` dice que la localidad «no está en los archivos». Está** — `c_portad`
  trae `loc` e `id_loc`. **No se usa**: cambiar el conglomerado aquí sería
  re-pre-registrar la varianza después de mirar. → `FP-351`.
- **`S6 §3.6`, la mala noticia que la spec mandó decir «aunque no guste»:** en las
  **cuatro** celdas la ventana del desenlace no cubre la del disparador, y la brecha
  es **mayor** que el ejemplo que la spec imaginó — `es09` no es de 12 meses, es **de
  por vida**. Las seis filas miden **co-ocurrencia, no secuencia**.
- **No existe `p_hs1.dta`**: el brazo `bx` de `C1` corre **sin filtro de motivo**,
  contra un `b3b` que sí lo lleva. Asimetría de universo entre brazos, rotulada en
  la propia fila. (Y `p_ec.dta` tampoco existe, lo que confirma `S6 §1`.)
- **`folio` es cadena (`%8s`) en los dos archivos de ponderador y numérico en todo
  el microdato** — ahí está, exactamente, el join que `S6 §3.4` temía. Normalizado,
  y con guardia de fan-out (`validate="m:1"`) que convierte una llave repetida en
  error ruidoso en vez de en una `n` inflada en silencio.
- **`S13 §3`, la trampa del nombre, en los dos sentidos:** `weight1500` tiene nombre
  de peso y etiqueta de estrato; **`strata` tiene nombre de estrato y etiqueta
  «Peso estandarizado»**. Se usa `wt`. Y `upm`/`estratopri` **sí** existen en las
  tres olas, contra el «no confirmados» de la spec.
- **`S12 §3`:** `dominio` y `upmmn` existen en los tres `.sav`, así que el IC no
  tiene que fingir muestreo aleatorio simple.

---

## 6 · `NC-0011` se paga con esta corrida

`NC-0011` (`ACTO GEN2-E3-1-1`) quedó abierta porque el endurecimiento `P2`/`P3` de
`preflight` **nunca se había probado contra specs reales** — sólo contra fixtures y
contra las dos `LEGACY-GEN1` selladas. **Esta es esa prueba**, y el endurecimiento
funcionó: las tres specs nacieron `[ENDURECIDO]`, con las once
dimensiones sustantivas declaradas, `seed {aplica, valor, rng}` completo y el schema
de outputs validado antes de abrir nada (54 · 29 · 128 ids únicos). **`NC-0011` →
`CERRADA`.**

Dos límites del `VERDE`, dichos aquí para que nadie los lea de más:

1. **`PRE-FLIGHT: VERDE` certifica la DECLARACIÓN, no el número.** Los tres
   `medidor.py` se escribieron en este acto y **no se ejecutaron en él** — `GEN2-E5-0`
   tiene prohibido abrir microdato. Lo que sí se verificó, con fixture **sintético**
   en memoria y sin tocar ningún payload: que el juego de claves que cada `medir()`
   devuelve **coincide exacto** con los ids declarados, y que los tipos casan. Los
   números que salieron de ese fixture son de datos inventados y **no se reportan**.
   → `NC-0036`.
2. **`preflight` da `BLOQUEADO` FALSO dentro del sandbox.** Todo payload cuya raíz
   lógica sea `descargas_mx` (`/mnt/c/...`) se resuelve `AUSENTE` dentro del
   sandbox de esta sesión y `COINCIDE` fuera. `CALC-0001` y `CALC-0002` sólo salen
   VERDE con el sandbox desactivado; `CALC-0003` (raíz `data_raw`) sale VERDE en
   los dos. **Quien corra `ACTO GEN2-E5` tiene que saberlo**, o leerá un bloqueo de
   entorno como un defecto de spec. → `FP-352`.

---

## 7 · Perímetro: lo que se escribió fuera de la lista literal, declarado

El encargo enumera «`data/corrida0/CALC-000{1,2,3}/spec.yaml` (+ `spec.md` local…)».
Se escribió además **`data/corrida0/CALC-000{1,2,3}/medidor.py`** — dentro del mismo
directorio nombrado, y **obligado por el propio encargo**: `preflight` bloquea con
`script_ausente` si el script no existe, de modo que «`preflight` VERDE», exigido
tres veces y puesto como contador del acto («tres CALC en `PRE-FLIGHT-VERDE`»), es
inalcanzable sin él. Se declara en vez de absorberse. `ACTO GEN2-E5` corre; no
escribe medidores.

**No se tocó** microdato, `tramite.yaml`, `canon/` (salvo la cascada de cierre), ni
`S12`/`S13`/`S6` ni sus sidecars.
