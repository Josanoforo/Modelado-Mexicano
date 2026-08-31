# COMMIT-1 · specs congeladas del LOTE-NUBE-1 (P0 · P1 · P2 · P3)

`ACTO MAESTRA32-E20 · LOTE-NUBE-1`, 31/ago/2026. Encargo archivado por A.3 en
`forense/encargos/2026-08-31-MAESTRA32-E20-LOTE-NUBE-1.md` (SHA de redacción
declarado `aa920f1`; base real de esta corrida `d510a63`, ver §0).

Las cuatro recetas de abajo se escriben y se congelan **antes** de tocar
ningún archivo de salida. No se editan después de correr. Orden interno
obligatorio del encargo: **P0 → P2**; P1 y P3 en cualquier hueco.

---

## §0 · ARRANQUE y COMPUERTA (Bloque D vía skill `/acto`, `ADR-237`)

| punto | valor crudo |
|---|---|
| 1 · REPO | `/home/user/Modelado-Mexicano` · `d510a63 Merge pull request #409 from Josanoforo/claude/maestra32-e19-launch-nza01w` · `git status`: rama `claude/maestra32-e20-lote-nube-elu7me`, árbol limpio. Clon existente, no se clonó nada nuevo. |
| 2 · SHA | El encargo declara `aa920f1` (merge PR #408 / `ADR-236`). `origin/main` real = `d510a63`. **Main se movió: NO es PARO.** Los 10 commits de diferencia son exactamente `MAESTRA32-E19` (PR #409, `ADR-237`) — el acto que sella la compuerta de este lote. Todo conteo de este lote se re-deriva contra `d510a63`, no contra el SHA de redacción. |
| 3 · `data/raw` | **AUSENTE** — `ls -d data/raw` examinó 1 ruta, no existe; `ls data/raw/ \| wc -l` → `0`. No es PARO (raíz gitignorada). Este lote **no la crea ni la enlaza**: ninguna de las cuatro piezas abre microdato (P0 copia valores ya medidos por `ADR-236`; P1 es censo sobre inventarios de reactivos; P2 es censo sobre inventarios + YAML; P3 emite desde `tramite.yaml`). |
| 4 · ENTORNO | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `cloud_default` (**no** `sin_variable`; valor crudo reportado, es el entorno NUBE que el encargo asigna) · sonda de red `https://www.inegi.org.mx/` → `000` (sin salida) · `ls data/raw/ \| head -1` → vacío. **A.13**: el `000` es un negativo de red producido por un comando que examinó **0 archivos**; no se usa como evidencia sobre ningún archivo. Este lote no descarga nada, así que la sonda no bloquea nada. |
| 5 · ESPEJO | No se usa. Toda cifra de este lote sale del clon de (1), con el comando a la vista. |

**COMPUERTA — `MAESTRA32-E19` fusionado en `main`. CUMPLIDA**, verificada
mecánicamente el 31/ago/2026 contra `origin/main` tras `git fetch origin main`:

```
git log --oneline origin/main | grep -c "maestra32-e19"           → 1  (d510a63)
git merge-base --is-ancestor d510a63 origin/main                  → 0  (es ancestro)
grep -c "^## CONSUMIDO" .../2026-08-31-MAESTRA32-E19-SELLA-CAMINO-1.md → 1
grep -c "ADR-237" canon/gobernanza-v1_15.md                       → 2
git merge-base --is-ancestor origin/main HEAD                     → 0  (la rama contiene main)
```

---

## §0-bis · Verificación de existencia — re-derivada contra `d510a63` (A.13)

Lo que el encargo afirma, re-verificado por comando en el árbol de hoy. Cinco
afirmaciones, cinco comandos, cinco conteos:

| afirmación del encargo | comando | resultado |
|---|---|---|
| `milpa/tramite-ola5-propuesta-v0.yaml` existe, 5 reglas con `p`+IC+`ola_calibracion` | `yaml.safe_load` → clave `reglas_propuestas` | **CONFIRMADO**: 5 entradas, las 5 con `p`, `ic95` y `ola_calibracion` |
| `milpa/tramite.yaml` sigue con 5 reglas, todas trámite | `yaml.safe_load` → `reglas` | **CONFIRMADO**: 5 reglas, los 5 `id` con prefijo `tramite.`, `p` de las 10 salidas `clase: ASIGNADO` |
| 0 hits de `denuncia\|ahorro\|recibe_dinero` en sus "46+ líneas" | `grep -Ec` sobre **1 archivo** de **127 líneas** | **CONFIRMADO: 0 hits**. Corrección de cifra: el archivo tiene **127** líneas, no 46 — el encargo dice "46+", que es cierto pero engaña sobre el tamaño; se re-deriva, no se hereda |
| curación E17 no corrió; spec íntegra en el encargo archivado | `grep "^## CONSUMIDO"` sobre el encargo E17 | **CONFIRMADO**: cerró por hallazgo antes de COMMIT-1 (`ADR-234`), §(a)-(e) íntegro en el encargo |
| `candidatos-marco-M-v1_1.tsv` existe: 7 celdas `transferencia=SI` | `csv.DictReader`, 8 filas | **CONFIRMADO**: 8 filas, `transferencia=SI` en 7 (`TRA-M-02` instrumento + `TRA-M-03..08` ola), `NO` en `TRA-M-01`; `en_corpus=SI` en las 8 |
| congelado v1_1 y puntos M `TRA-*`: NO-ENCONTRADO | `ls` con conteo | **CONFIRMADO**: 0 de 31 archivos de `forense/prereg-duelo-v2/` casan `congelado-v1_1\|CONGELADO-M-v1_1`; `corridas-M/` tiene 17 entradas y **0** casan `M-TRA-*` |

**Categoría B — el encargo dice "14 celdas".** Este spec fija que P2 **deriva,
no hereda** esa cifra (instrucción literal del encargo): se re-recorre el censo
contra los cuatro inventarios de hoy y el número que salga es el que se reporta,
coincida o no con 14.

---

## §P0 · PROPAGA-REGLAS-F1 (`FP-200` = b)

### (a) Qué se carga y qué no

Cuatro cargas a `milpa/tramite.yaml`, **exactamente cuatro**, copiando de
`milpa/tramite-ola5-propuesta-v0.yaml` con `p` / `ic95` / `fuente` / `universo` /
`ponderador` / `ola_calibracion` / `n` / `clase` / `sha256_payload*` /
`payload_manifiesto_id` / `porque` **intactos, carácter por carácter**:

1. `civico.denuncia.miedo_desconfianza` (regla nueva)
2. `dinero.ahorro.tiene_ahorros` (regla nueva)
3. `familia.apoyo.recibe_dinero_familiares` (regla nueva)
4. la **enmienda ENCUCI** de `tramite.mordida.discrecional` (no es regla nueva)

**No se carga** `familia.corresidencia.adulto_familiar`. En la propuesta se le
añade cabecera fechada `DEVUELTA-POR-MESA (FP-200=b, 31/ago/2026)` con la
re-especificación nombrada (ventana actual — corresidencia hoy —, medible en el
mismo EDER, acto de caja sucesor). **Cuerpo intacto**: ni `p`, ni `ic95`, ni
`universo`, ni `hallazgo` se tocan. Es lo único que este lote escribe en la
propuesta.

Conteo esperado del motor tras la carga: **5 → 8 reglas**, dominios activos
**1 → 4** (`tramite` + `civico` + `dinero` + `familia`). Si el conteo real no da
8/4, **PARA y reporta** — el descongelamiento se pasó de acotado.

### (b) La enmienda ENCUCI — desviación declarada ANTES de correr

El encargo exige dos cosas a la vez sobre `tramite.mordida.discrecional`:
*"desenlace `AP5_17|AP5_18`, `FAC_SEL`, `ola_calibracion` propia"* **y** *"texto
original de la regla intacto"*. `milpa/src/emisor.py:475-481` (`emitir_binaria`)
devuelve **la primera** salida cuya `conducta` casa. Con el texto original
intacto, las salidas originales (`paga_mordida` `p: 0.62 ASIGNADO`,
`tramite_normal` `p: 0.38 ASIGNADO`) van primero y ganan siempre: la enmienda
sería inverificable por el smoke que el propio encargo ordena.

**Resolución congelada aquí, no adjudicada**: las dos salidas medidas de la
enmienda entran en el mismo `entonces`, **después** de las dos originales, con
`conducta` desambiguada por ola — `paga_mordida_encuci2020` y
`tramite_normal_encuci2020`. Justificación mecánica, no de gusto:

- Los valores que el encargo manda dejar intactos (`p`/IC/`fuente`/`universo`/
  `ponderador`/`ola_calibracion`) quedan intactos; `conducta` **no está en esa
  lista**.
- `emitir_binaria(regla, "paga_mordida")` sigue devolviendo `0.62 ASIGNADO`:
  ningún consumidor existente cambia de comportamiento.
- `emitir_binaria(regla, "paga_mordida_encuci2020")` devuelve `0.125822`, que es
  lo que el smoke exige verificar.

**Va al recibo para mesa**: si mesa quiere que la enmienda *sustituya* al `0.62`
en vez de convivir con él, es una firma nueva y un acto nuevo — este lote no la
toma. La convivencia es la lectura conservadora de "texto original intacto".

### (c) Campos `si:` en `PENDIENTE-DE-MESA`

Regla del encargo: se completan **solo** con texto SI-ENTONCES citable de
`canon/modelo-decision-v4_0.md` **§2.1-2.2** (`archivo:línea`); sin cita, el
campo queda `PENDIENTE-DE-MESA` y el recibo lo lista. **No se inventa.**

Barrido mecánico, corrido **antes** de escribir (A.13 — 46 líneas examinadas,
`canon/modelo-decision-v4_0.md:428-473`, que es §2.1 + §2.2 hasta `## 3`):

```
patrón SI…ENTONCES en §2.1-2.2                  → 0 coincidencias
'denuncia' / 'denunci' en §2.1-2.2              → 0 / 0
'vejez' / 'dinero de familiares' en §2.1-2.2    → 0 / 0
```

§2.1-2.2 es la sección de **generadores latentes**: define cláusulas falsables
("se refuta si…") y la tabla de 15 coeficientes. Las reglas SI-ENTONCES del
modelo viven en **§3.B** (`canon/modelo-decision-v4_0.md:491`, "Las 49 reglas
SI-ENTONCES") — fuera del alcance que el encargo autoriza.

**Consecuencia congelada**: los tres `si.disparadores` de las reglas nuevas
quedan `PENDIENTE-DE-MESA` y el recibo los lista. Que el texto citable exista en
§3.B **se reporta como hallazgo para mesa**, y **no se usa**: el encargo nombró
§2.1-2.2, y ampliar la fuente por cuenta propia es exactamente lo que "no se
inventa" prohíbe.

**Plomería obligada, declarada aquí**: `emisor.cargar_reglas` hace
`(si.get("disparadores") or {}).items()` — un `disparadores: PENDIENTE-DE-MESA`
(cadena) **rompe la carga** con `AttributeError` (verificado en vivo antes de
congelar este spec). Por eso el campo se escribe
`disparadores: {}` (que es además lo que la propuesta explica: *"el dato no
dicta una condicion logica de disparo … p viene de una tasa base incondicional"*)
con el marcador literal preservado en un campo hermano
`disparadores_estado: PENDIENTE-DE-MESA` — `grep`-able, listado en el recibo, e
ignorado por `cargar_reglas`. El marcador no se pierde; el motor no se rompe.

### (d) Smoke obligatorio

Para las cuatro cargas: `emisor.emitir_binaria(regla, conducta)` devuelve
`valor_punto == p` de la propuesta, comparado por igualdad exacta de `float`. Se
pegan las **4 salidas** crudas en la nota de cierre. Además: `cargar_reglas()`
devuelve 8 reglas y 4 dominios. Suite `python3 tests/check.py --baseline` en
VERDE (sin FAIL nuevo). **Cualquiera de las tres condiciones que falle: PARA y
reporta con la salida cruda** — no se sigue a P2.

### (e) Descongelamiento acotado

El ADR de este lote declara: `ADR-68(a)` recibe **excepción fechada
(31/ago/2026) por exactamente estas cuatro cargas y nada más**. No autoriza
tocar `milpa/procedencia.yaml`, `milpa/src/**`, ni ninguna otra regla.

### (f) Tablero (mismo commit, A.12)

`FP-200` → `FIRMADA` con `(b)` · el `enterado ×8` propagado a `FP-187`, `189`,
`191`, `193`, `194`, `195`, `196`, `201` · fila nueva `RE-SPEC-CORRESIDENCIA`
(ventana actual, EDER, caja; `ABIERTA` hasta lanzar).

---

## §P1 · CURA-RADIO (re-emisión de `MAESTRA32-E17`)

Se ejecuta **verbatim** el `COMMIT-1 §(a)-(e)` del encargo archivado
`forense/encargos/2026-08-31-MAESTRA32-E17-CURA-RADIO-CONFIANZA.md`. Se copia
aquí lo operativo, sin cambiarlo:

- **(a) Regla de curación del homónimo.** Todo reactivo con `confía`/`confianza`
  en `texto_reactivo` de cualquier ola de ENDIREH (2006/2011/2016/2021, en `ext`
  y `v1_2`) se clasifica por referente con lista cerrada:
  **INTERPERSONAL** = familiares, parientes, vecinos, amigos, conocidos,
  compañeros, "la gente"/"las personas";
  **INSTITUCIONAL** = autoridades, gobierno, policía, ministerio público, jueces,
  instituciones, iglesia;
  **OTRO** = pareja/esposo (relación diádica, no radio) y lo no clasificable.
  Solo INTERPERSONAL cuenta como θ de `radio_confianza`.
- **(b) Co-observación válida** = ≥1 reactivo INTERPERSONAL **y** ≥1 desenlace de
  G5 en la **misma base**, con instrumento identificado. Lista de términos de
  desenlace G5, sin cambios, de la spec de E2
  (`forense/notas/2026-08-28-empareja-spec.md:62`): `pooling`, `corresidencia`,
  `vive con`, `hogar extendido`, `cuidado de familiares`, `carga de cuidado`,
  `cuidador`, `cuida a`, `comparte gastos del hogar`, `hogar compartido`,
  `mudarse con la familia`, `se mudó con`, `se mudo con`.
- **(c) Escalera de 5 peldaños, corrida COMPLETA aunque un peldaño dé positivo**
  (para que mesa vea todo el mapa), cada uno con sus conteos A.13:
  1. ENDIREH (todas las olas).
  2. `encup2012` (`P30`, 27 ítems: mismo clasificador por referente; desenlace G5
     en el mismo instrumento).
  3. ENNViH/MxFLS (`ehh05dta_all.zip` y las olas 2-3 de CAL-G3: capital
     social/confianza + transferencias familiares/corresidencia).
  4. ENCUCI 2020 (tiene la θ ancla `radio_confianza`; buscar desenlace G5 ahí).
  5. WVS y Latinobarómetro México (ya descargados).
- **(d) Contingencia pre-escrita** si ningún peldaño da co-observación: (d1) el
  par queda `EXISTE-NO-SATISFACE` con las medias parejas nombradas por peldaño;
  (d2) el coeficiente sigue `ASIGNADO · SOLO-SIGNO·NO-COMPARABLE` (`ADR-220`),
  sin magnitud y sin transporte desde otro constructo; (d3) fila de adquisición
  con nombre para `FP-179`; (d4) vía alterna (coeficiente compuesto de dos
  instrumentos) **declarada, no ejecutada** — solo con firma posterior de mesa.
- **(e) B-bis**: positivo en peldaño 1 → medidor de caja sobre ENDIREH; positivo
  solo en 2-5 → medidor sobre ese instrumento; negativo total → (d) completo.

**Perímetro y salidas: los del propio E17.** `data/curacion-radio-confianza-v1_0.tsv`
(reactivo × referente × instrumento × ola × peldaño) y el veredicto A.4 por
peldaño. `forense/notas/2026-08-31-cura-radio-cierre.md` **ya existe** (lo
escribió E17 al cerrar por hallazgo): **no se reescribe** — la re-emisión entra
como sección fechada al final, original intacto (A.10). Intocables, `git diff
--stat` vacío al terminar P1: inventarios, `data/emparejamiento-motor-v1_2.tsv`,
spec de E2, `milpa/**`.

**Conteos re-derivados contra el árbol de hoy**, no heredados de E17.

---

## §P2 · A″ · MARCO-M-CONGELA-v1_1

### (a) Insumo

`forense/prereg-duelo-v2/candidatos-marco-M-v1_1.tsv` (8 filas, `ADR-233`) **+ el
estado post-P0 de `milpa/tramite.yaml`**. P2 no corre antes que P0.

### (b) Elegibilidad bajo F-DD (`ADR-237`)

```
elegible = (transferencia == SI) ∧ (en_corpus == SI) ∧ (la estadística tiene regla cargada)
```

"La estadística tiene regla cargada" se resuelve **por comando** contra el
`tramite.yaml` post-P0 (`cargar_reglas()`), nunca por prosa: la estadística de la
fila debe ser el desenlace de una regla que `cargar_reglas()` devuelva.

### (c) Categoría B — se re-evalúa fila por fila, **derivada, no heredada**

Las tres estadísticas de Categoría B de la spec de E15
(`forense/notas/2026-08-31-marco-M-v1_1-spec.md`, §(b)) se re-censan contra la
unión de los cuatro inventarios de hoy (`data/inventario-reactivos-v1_2.tsv` ∪
`-ext-v1_0` ∪ `data/inventario-fd-v1_1.tsv` ∪ `-fd-ext-v1_0`), con el criterio
(c) de E15 sin cambios: mismo `variable_id` (case-insensitive), misma familia de
instrumento (prefijo `encig`/`encuci`/`envipe`/`enif`/`ennvih`/`mxfls`), y para
ENNViH además respaldo por `payload_id` (el campo `instrumento` no resuelve esa
familia — hallazgo de E15 que este spec hereda como método, no como cifra):

- `BP1_23` (ENVIPE) — desenlace de `G4_exposicion_violencia`
  (`milpa/procedencia.yaml:998`). Calibración ENVIPE 2025.
- `p4_10`/`P4_10` (ENIF) — desenlace de `G3_familismo_apoyo`
  (`milpa/procedencia.yaml:969`), vía la regla
  `dinero.ahorro.volatilidad_horizonte_corto`. Calibración ENIF 2024.
- `cr27` (ENNViH/MxFLS) — desenlace del par sellado `G3.horizonte_temporal`
  (`milpa/procedencia.yaml:1286-1296`). Calibración olas 2-3.

Cada una se casa contra las reglas que P0 cargó. **La cifra "14" del encargo no
se hereda**: sale el número que salga del censo de hoy, y si difiere de 14 se
dice por qué.

**Cuarta estadística, tratada aparte y declarada aquí antes de correr**: la regla
`familia.apoyo.recibe_dinero_familiares` que P0 carga tiene como desenlace
`p9_9_4` (ENIF, `milpa/procedencia.yaml:300-319`), que **no era** parte de la
Categoría B de E15 (E15 censó `p4_10`, el desenlace de una regla distinta). Se
censa con el mismo criterio y se reporta en bloque propio, con su procedencia
dicha: es consecuencia de `FP-200`=b, no una fila heredada. Si produce celdas de
transferencia, entran al marco marcadas con esa procedencia.

### (d) Celdas de calibración

Las celdas cuya `(ola, instrumento)` **coincide** con la `ola_calibracion` de su
regla entran al marco marcadas **`VERIFICACION-NO-PUNTUA`** — control de
plomería. **No se borran.** Es F-DD operativo: calibración = verificación,
transferencia = puntúa.

### (e) Sellado

`forense/prereg-duelo-v2/marco-M-congelado-v1_1.tsv` +
`forense/prereg-duelo-v2/CONGELADO-M-v1_1.sha256`, este último con el **sha256
del TSV** y **`N_elegibles`**. Formato del TSV: cabecera `#` de procedencia, LF,
mismas columnas que `candidatos-marco-M-v1_1.tsv` más `grado_DD` y
`elegible_v1_1`, para que el sucesor B″ pueda leerlo sin traducción.

### (f) Pre-registro de B″ (en la nota de cierre, misma nota)

```
scope_id  = "MARCO-M-v1_1"
semilla   = semilla_desde_sha_merge(SHA_merge_de_ESTE_lote, scope_id)
tamaño    = regla idéntica a ADR-231 §e
cuota_max = floor(0.20 · n)
```

**B″ es sucesor, no se lanza aquí: sin SHA de merge no hay semilla.** Este lote
no sortea.

---

## §P3 · EMITE-M-v0 — primeros puntos M

Sobre las **DOS** celdas de `forense/prereg-duelo-v2/marco-M-sorteado-v1_0.tsv`
(`TRA-M-01`, `TRA-M-02`), con **C1/C2 de `ADR-233` aplicadas por referencia** —
es decir: para `TRA-M-02` se lee `variable = AP5_17|AP5_18` y
`ponderador = FAC_SEL`, citando `candidatos-marco-M-v1_1.tsv` como la fuente de
la corrección; **el archivo `marco-M-sorteado-v1_0.tsv` no se edita** (marcos
v1_0 están fuera del perímetro).

Para cada celda: localizar `p` y `ola_calibracion` **con cita `archivo:línea`**,
emitir vía `emisor.emitir_binaria`, y escribir
`forense/prereg-duelo-v2/corridas-M/M-TRA-M-01.json` y `M-TRA-M-02.json` con el
**esquema existente** de ese directorio (claves ordenadas, `indent=1`; ver
`M-CIV-08.json`) más los campos nuevos que el encargo pide: `p`, `clase`,
`ola_calibracion`, `grado_DD`.

`grado_DD`, regla congelada:

- `TRA-M-01` → **`P0 VERIFICACION`** si su `(encuesta, ola)` coincide con la
  `ola_calibracion` de su regla. Se verifica, no se asume.
- `TRA-M-02` → según **F-DD**: si `(encuesta, ola)` ≠ `ola_calibracion` de su
  regla, es validación externa → `P1 PUNTUA`.

**Ciego a R**: no se abre `forense/prereg-duelo-v2/corridas-R/` ni ninguna
columna de valor de R. La nota de cierre **lista los archivos abiertos** por P3,
uno por uno.

---

## Sello del lote

**"El primer resultado que produzca este procedimiento es el que se reporta."**

Una pieza que PARA se reporta y las demás siguen (D-11).
