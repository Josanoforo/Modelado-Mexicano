# Cierre · `ACTO MAESTRA32-E20 · LOTE-NUBE-1`

31/ago/2026 · entorno NUBE · encargo archivado por A.3 en
`forense/encargos/2026-08-31-MAESTRA32-E20-LOTE-NUBE-1.md` · specs congeladas
antes de correr en `forense/notas/2026-08-31-lote-nube-1-spec.md` · ejecutado
con la skill `/acto` (`ADR-237`, D-10 de `instrucciones-proyecto-v2_12.md`).

Las cuatro piezas corrieron. **Ninguna PARÓ.** Orden interno respetado:
`P0 → P2`; `P1` y `P3` en sus huecos.

---

## ARRANQUE y COMPUERTA

Reportados íntegros en `…-lote-nube-1-spec.md` §0. Lo esencial:

- **SHA.** El encargo se redactó contra `aa920f1`; `origin/main` real al
  arrancar = `d510a63`. **Main se movió y NO es PARO**: los 10 commits de
  diferencia son exactamente `MAESTRA32-E19` (`PR #409`, `ADR-237`), el acto que
  abre la compuerta de este lote. Todo conteo se re-derivó contra `d510a63`.
- **COMPUERTA CUMPLIDA**, mecánicamente: `git log --oneline origin/main | grep -c
  "maestra32-e19"` → `1`; `git merge-base --is-ancestor d510a63 origin/main` →
  ancestro; el encargo de `E19` con `## CONSUMIDO`; `ADR-237` en `gobernanza`.
- **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`; sonda de red
  `000`; `data/raw` ausente (`ls -d` examinó 1 ruta). **Ninguna de las cuatro
  piezas abre microdato**, así que nada de eso bloquea nada. **Nada se descargó**
  → anti-PR#77 no aplica, declarado.

## Verificación de existencia — cinco afirmaciones, cinco comandos

Todas confirmadas (tabla completa en la spec §0-bis), con **una corrección de
cifra**: el encargo describe `milpa/tramite.yaml` como de "46+ líneas"; el
archivo tenía **127**. Cierto pero engañoso sobre el tamaño; se re-derivó, no se
heredó. Los 0 hits de `denuncia|ahorro|recibe_dinero` sí eran exactos.

---

## P0 · PROPAGA-REGLAS-F1 — `FP-200` = (b)

**Cuatro cargas, exactamente cuatro.** Motor **5 → 8 reglas**, dominios activos
**1 → 4** (`tramite` · `civico` · `dinero` · `familia`), verificado por
`cargar_reglas()`, no por prosa.

### Smoke obligatorio — las 4 salidas crudas, pegadas

```
cargar_reglas() -> 8 reglas
dominios activos -> 4: ['civico', 'dinero', 'familia', 'tramite']

emitir_binaria('civico.denuncia.miedo_desconfianza', 'denuncia_con_miedo_o_desconfianza')
  -> PrediccionM(tipo_escala='binaria', valor_punto=0.294313, valor_categoria='denuncia_con_miedo_o_desconfianza',
                 clase='MEDIDO·p(tasa base ponderada)', regla_id='civico.denuncia.miedo_desconfianza', estado='EMITE')
  p de la propuesta = 0.294313   ==  -> True

emitir_binaria('dinero.ahorro.tiene_ahorros', 'tiene_ahorros')
  -> PrediccionM(tipo_escala='binaria', valor_punto=0.174804, valor_categoria='tiene_ahorros',
                 clase='MEDIDO·p(tasa base ponderada)', regla_id='dinero.ahorro.tiene_ahorros', estado='EMITE')
  p de la propuesta = 0.174804   ==  -> True

emitir_binaria('familia.apoyo.recibe_dinero_familiares', 'recibe_dinero_familiares_para_vejez')
  -> PrediccionM(tipo_escala='binaria', valor_punto=0.457707, valor_categoria='recibe_dinero_familiares_para_vejez',
                 clase='MEDIDO·p(tasa base ponderada)', regla_id='familia.apoyo.recibe_dinero_familiares', estado='EMITE')
  p de la propuesta = 0.457707   ==  -> True

emitir_binaria('tramite.mordida.discrecional', 'paga_mordida_encuci2020')
  -> PrediccionM(tipo_escala='binaria', valor_punto=0.125822, valor_categoria='paga_mordida_encuci2020',
                 clase='MEDIDO·p(tasa base ponderada)', regla_id='tramite.mordida.discrecional', estado='EMITE')
  p de la propuesta = 0.125822   ==  -> True

no-regresion:
  emitir_binaria('tramite.mordida.discrecional', 'paga_mordida')   -> valor_punto=0.62 clase='ASIGNADO'
  emitir_binaria('tramite.mordida.discrecional', 'tramite_normal') -> valor_punto=0.38 clase='ASIGNADO'

SMOKE: VERDE
```

Comparación por **igualdad exacta de `float`**, no por tolerancia.

### Dos desviaciones, declaradas ANTES de correr (spec §P0(b) y §P0(c))

1. **Conducta desambiguada por ola en la enmienda ENCUCI.** El encargo pide a la
   vez "desenlace `AP5_17|AP5_18`, `FAC_SEL`, `ola_calibracion` propia" y "texto
   original de la regla intacto". `emitir_binaria`
   (`milpa/src/emisor.py:476-479`) devuelve **la primera** coincidencia de
   `conducta`: con el original intacto, las salidas `ASIGNADO` ganan siempre y la
   enmienda sería **inverificable** por el smoke que el propio encargo ordena.
   Resolución: las dos salidas medidas entran en el mismo `entonces`, después de
   las originales, como `paga_mordida_encuci2020` / `tramite_normal_encuci2020`.
   `conducta` **no** está en la lista de campos que el encargo manda dejar
   intactos (`p`/IC/`fuente`/`universo`/`ponderador`/`ola_calibracion`), y esos
   sí quedaron intactos carácter por carácter.
   **Para mesa**: la enmienda **convive** con el `0.62 ASIGNADO`, no lo
   sustituye. Si mesa quiere sustitución, es firma nueva y acto nuevo.
2. **`si.disparadores` como mapping vacío.** La propuesta trae
   `disparadores: PENDIENTE-DE-MESA` (una cadena), y
   `emisor.cargar_reglas` hace `(si.get("disparadores") or {}).items()`: con una
   cadena **rompe la carga** con `AttributeError` — verificado en vivo antes de
   congelar la spec. Va como `disparadores: {}` (que es además lo que la propia
   propuesta explica: *"p viene de una tasa base incondicional"*) con el marcador
   literal preservado en el campo hermano `disparadores_estado:
   PENDIENTE-DE-MESA`, `grep`-able e ignorado por `cargar_reglas`.

### Campos `si:` — se quedan `PENDIENTE-DE-MESA`, y por qué

El encargo autoriza completarlos **solo** con texto SI-ENTONCES citable de
`canon/modelo-decision-v4_0.md` **§2.1-2.2**. Barrido mecánico antes de escribir
(**A.13: 46 líneas examinadas**, `canon/modelo-decision-v4_0.md:428-473`):

```
patrón SI…ENTONCES en §2.1-2.2   -> 0
'denuncia' / 'denunci'           -> 0 / 0
'vejez' / 'dinero de familiares' -> 0 / 0
```

§2.1-2.2 es la sección de **generadores latentes**: cláusulas falsables ("se
refuta si…") y la tabla de 15 coeficientes. **No contiene ni una regla
SI-ENTONCES.** Las 49 reglas SI-ENTONCES del modelo viven en **§3.B**
(`canon/modelo-decision-v4_0.md:491`), fuera del alcance que el encargo
autoriza. **Hallazgo para mesa**: el texto citable existe, pero en otra sección;
ampliar la fuente por cuenta propia es exactamente lo que "no se inventa"
prohíbe. Los tres `si.disparadores` quedan `PENDIENTE-DE-MESA` y este recibo los
lista:

| regla cargada | campo | estado |
|---|---|---|
| `civico.denuncia.miedo_desconfianza` | `si.disparadores` | `PENDIENTE-DE-MESA` |
| `dinero.ahorro.tiene_ahorros` | `si.disparadores` | `PENDIENTE-DE-MESA` |
| `familia.apoyo.recibe_dinero_familiares` | `si.disparadores` | `PENDIENTE-DE-MESA` |

También siguen `PENDIENTE-DE-MESA`, copiados verbatim de la propuesta y sin
tocar: `situacion`, `tier`, `falsable_si` y `porque.mecanismo` de las tres.

### Corresidencia devuelta, no borrada

`familia.corresidencia.adulto_familiar` **no se carga**. En
`milpa/tramite-ola5-propuesta-v0.yaml` recibe cabecera fechada
`DEVUELTA-POR-MESA (FP-200=b, 31/ago/2026)` con la re-especificación nombrada
—ventana **actual**, instrumento **EDER**, ejecutor **acto de caja**, tablero
`RE-SPEC-CORRESIDENCIA`—. **Cuerpo intacto: `git diff` da 23 líneas añadidas y
0 borradas.** El `p=0.996` se conserva tal como salió del procedimiento que lo
produjo: devolverlo a re-especificación no es borrarlo.

### Descongelamiento acotado

`ADR-68(a)` recibe **excepción fechada (31/ago/2026) por exactamente estas
cuatro cargas y nada más**. `milpa/procedencia.yaml` y `milpa/src/**` intactos.

---

## P1 · CURA-RADIO (re-emisión de `MAESTRA32-E17`)

Receta congelada en `forense/notas/2026-08-31-cura-radio-spec.md` (E17 §(a)-(e)
verbatim). Corrida y veredicto completos en la **sección fechada de re-emisión**
al final de `forense/notas/2026-08-31-cura-radio-cierre.md` — el cierre por
hallazgo de E17 queda intacto (A.10). Salida:
`data/curacion-radio-confianza-v1_0.tsv`, 143 filas.

**Veredicto: 0 de 5 peldaños con co-observación válida** → contingencia **(d)
completa**, ejecutada. **A.13: 269 320 filas de inventario examinadas**, 489
`payload_id`.

| # | peldaño | θ INTERP | desenlace G5 | media pareja |
|---|---|---:|---:|---|
| 1 | ENDIREH | **0** de 7 | 8 | desenlace SÍ, θ NO — los 7 reactivos de confianza son institucionales; la reserva de `E4` queda **confirmada como homónimo** |
| 2 | `encup2012` | **3** | 0 | θ SÍ (la más limpia del corpus: `P30_10` vecinos, `P30_11` la familia, `P34` confianza generalizada), desenlace NO |
| 3 | ENNViH/MxFLS | 0 de 4 | 76 | desenlace SÍ (corresidencia literal), θ clasifica `OTRO` por la lista cerrada |
| 4 | ENCUCI 2020 | 0 | 0 | θ SÍ pero **sellada en `procedencia`, invisible al censo de texto**; desenlace NO |
| 5 | WVS + Latinobarómetro | 1 | 0 | **WVS AUSENTE del corpus**; Latinobarómetro 2024 con 1 sola θ interpersonal |

**Dos negativos que no eran negativos**, corregidos antes de escribir el
veredicto (A.13, mismo patrón que la nota de honestidad de `MAESTRA32-E15`):
`encup2012` parquea la pregunta completa en `variable_id`, no en
`texto_reactivo` (vacío en sus 282 filas, método `INSPECT_XLSX`) — el barrido
literal daba "0 reactivos legibles" para el peldaño con la mejor θ del corpus. Y
el único "desenlace" que la pasada corregida encontró en ENCUP es un **falso
positivo léxico** (`P28B`, *"si uno no se cuida a sí mismo la gente se
aprovechará"*, casa `cuida a`), verificado y descartado contra sus 282
reactivos: 13 hits, **cero desenlaces de G5** (diez son la batería AMAI de nivel
socioeconómico).

**Dos premisas de `E17` que el árbol de hoy corrige**: (i) "WVS y Latinobarómetro
ya descargados" es cierto **solo para Latinobarómetro** — WVS da 0 coincidencias
entre los 489 `payload_id`; (ii) la rama ENCUCI de (d3) suponía que ahí falla la
θ — lo que falla es el **desenlace**.

**(d3) ejecutada**: `FP-179` entrada **(6)** — adquirir **WVS ola 7 México
(2018)**, único instrumento con la batería de confianza por círculos y módulo de
hogar en la misma muestra. Es una descarga, no una búsqueda. **(d2)**:
`G5.radio_confianza` sigue `ASIGNADO · SOLO-SIGNO·NO-COMPARABLE` (`ADR-220`),
sin magnitud y sin transporte. **(d4)** declarada, no ejecutada.

**Intocables verificados** (`git diff --stat` vacío): los cuatro inventarios,
`data/emparejamiento-motor-v1_2.tsv`, la spec de `E2`, `milpa/**`.

---

## P2 · A″ · MARCO-M-CONGELA-v1_1

`forense/prereg-duelo-v2/marco-M-congelado-v1_1.tsv` — **27 filas, 32 columnas**.
`CONGELADO-M-v1_1.sha256`:
`8e6459dd49869063986daa16cfbb8067575ee7c747e3cadd6a35f1b51d582477`,
**`N_elegibles=22`**, `N_verificacion_no_puntua=5`.

Elegibilidad bajo F-DD resuelta **por comando**: `elegible = (transferencia==SI)
∧ (en_corpus==SI) ∧ (la estadística tiene regla en `cargar_reglas()` post-P0)`.

### La categoría B, derivada y no heredada

**A.13: 269 320 filas de inventario examinadas.** El encargo hereda de `E15` la
cifra "14 celdas"; el censo de hoy dice esto:

| estadística | regla cargada tras `FP-200`=b | filas en corpus | en familia | olas | transferencia | calibración |
|---|---|---:|---:|---:|---:|---:|
| `BP1_23` (ENVIPE) | `civico.denuncia.miedo_desconfianza` ✔ | 49 | 49 | 14 | **13** | 1 (2025) |
| `cr27` (ENNViH) | `dinero.ahorro.tiene_ahorros` ✔ | 6 | 6 | 3 | **1** (ola 1, 2002) | 2 (olas 2-3) |
| `P4_10` (ENIF) | **NINGUNA** ✘ | 71 | 5 | 2 | 1 (2021) | 1 (2024) |
| `P9_9_4` (ENIF) | `familia.apoyo.recibe_dinero_familiares` ✔ | 12 | 6 | 2 | **1** (2018) | 1 (2024) |

Enlaces estadística→regla, citados: `BP1_23` por `milpa/tramite.yaml:211`
(`fuente` → `coeficientes_generador_medidos.G4_exposicion_violencia`) ×
`milpa/procedencia.yaml:998` (*"x desenlace `BP1_23`"*); `cr27` nombrado
**literalmente** en el `universo` de la regla cargada
(`milpa/tramite.yaml:236`); `P9_9_4` nombrado literalmente en
`milpa/tramite.yaml:260` y confirmado vía `milpa/procedencia.yaml:303`.

**Tres correcciones a la cifra heredada, cada una con su razón:**

1. **`P4_10` NO se vuelve derivable.** Su desenlace pertenece a
   `dinero.ahorro.volatilidad_horizonte_corto` (`milpa/procedencia.yaml:969`),
   que **no** está entre las cuatro cargas de `FP-200`=b. Sigue sin regla, sigue
   sin producir fila — mismo criterio (e) de `MAESTRA32-E15` ("hay
   encuesta/variable, no hay regla"). Se censa y se reporta, no se inventa.
2. **`cr27` sí produce fila.** `E15` lo contó como "un hallazgo, no una fila"
   precisamente porque no tenía regla; ahora la tiene. Su ola 1 (ENNViH-1, 2002)
   entra como transferencia. Se identificó por `payload_id` (`ehh02`/`ehh05`/
   `ehh09`) porque el campo `instrumento` no resuelve la familia ENNViH —
   hallazgo de `E15` heredado como **método**, no como cifra.
3. **`P9_9_4` es una estadística que la categoría B de `E15` no tenía.** `E15`
   censó `P4_10`, el desenlace de otra regla. La cuarta carga de `FP-200`=b mide
   `P9_9_4`, y su ola 2018 es una transferencia real. Entra con su procedencia
   dicha: es consecuencia de la firma, no una fila heredada.

**Balance: las 14 celdas del encargo se vuelven 15 celdas puntuables** — 13 de
`BP1_23` + 1 de `cr27` + 1 de `P9_9_4`, menos la de `P4_10` que no cruza la
puerta.

### Composición del marco congelado

| bloque | filas | elegibles | verificación |
|---|---:|---:|---:|
| Categoría A heredada (`TRA-M-01..08`, `ADR-233`) | 8 | 7 | 1 |
| `CIV-M-01..14` (`BP1_23`, ENVIPE 2012-2025) | 14 | 13 | 1 |
| `DIN-M-01..03` (`cr27`, ENNViH olas 1-3) | 3 | 1 | 2 |
| `FAM-M-01..02` (`P9_9_4`, ENIF 2018/2024) | 2 | 1 | 1 |
| **total** | **27** | **22** | **5** |

Las 5 celdas de ola/instrumento de calibración **se conservan** marcadas
`grado_DD = P0 VERIFICACION-NO-PUNTUA` (control de plomería). Toda fila nueva
lleva `NO ESTIMADO EN ESTE ACTO` donde exigiría re-derivar contra microdato
(misma regla de columnas que `E15` §(e)): este es un censo de **existencia**
sobre inventarios, no una medición.

**Límite declarado**: la columna `ola` del inventario es `NO_DETERMINADO` en el
100% de estas filas; la ola se deriva del campo `instrumento` (`envipe2012` →
2012) o, para ENNViH, del `payload_id` contra `data/manifiesto.yaml:468-533` y
`forense/notas/2026-08-24-cal-g3-puntual-cierre.md:34-46`.

**B-bis re-leído**: `N_elegibles = 22 ≥ 8` → el marco-M **sí** llega a tamaño de
sorteo real bajo D-D. `E15` cerró en `1-7` → corto; la firma `FP-200`=b es lo
que lo saca de corto. El salto real es **2 → 22** contra el congelado v1_0.

### Aviso F-DD abierto por la propia firma (`TRA-M-02`)

La enmienda ENCUCI que P0 carga trae `ola_calibracion = ENCUCI 2020` **para la
misma regla** que `TRA-M-02` mide en ENCUCI 2020. Esta fila se evalúa por la
conducta que el marco declara (`paga_mordida`, `p=0.62 ASIGNADO`, ancla ENCIG
2023) → sigue `P1 PUNTUA`. **Pero** re-apuntar el marco a la conducta enmendada
la convertiría en `P0 VERIFICACION` bajo F-DD, porque predeciría ENCUCI 2020 con
un número medido en ENCUCI 2020. **Decisión de mesa, no de este acto**: marcos
v1_0 están fuera del perímetro y la fila lo declara en su `razon_DD`.

### Pre-registro de B″ — `MARCO-M-SORTEA-v1_1`

```
scope_id  = "MARCO-M-v1_1"
semilla   = semilla_desde_sha_merge(SHA_merge_de_ESTE_lote, "MARCO-M-v1_1")
            (forense/prereg-duelo-v2/sorteo_v2.py:191, vía sorteo_marco_m.py:37)
N         = 22                       (N_elegibles de CONGELADO-M-v1_1.sha256)
tamaño    = regla ADR-231 §e, idéntica: N>=30 -> 15 ; 15<=N<30 -> ceil(N/2) ; N<15 -> identidad
            -> 15 <= 22 < 30  =>  n_sorteo = ceil(22/2) = 11
cuota_max = floor(0.20 · n_sorteo) = floor(0.20 · 11) = 2
```

**B″ es sucesor: sin SHA de merge no hay semilla.** Este lote no sortea.

**Una nota de plomería para quien lo corra**: `N_elegibles` (22) < `N_filas`
(27), porque las 5 celdas de calibración se conservan. `sorteo_marco_m.
cargar_marco_m` compara filas leídas contra `N_elegibles` y no conoce la columna
nueva: **B″ debe filtrar `elegible_v1_1 == "SI"` antes de ese assert**. El módulo
**no se tocó** en este lote (fuera de perímetro); el cambio le toca a B″. El
archivo se escribió byte-compatible con el congelado v1_0 (cabecera en la línea
1, sin preámbulo `#`) precisamente para que ese sea el **único** cambio
necesario.

---

## P3 · EMITE-M-v0 — primeros puntos M

`forense/prereg-duelo-v2/corridas-M/M-TRA-M-01.json` y `M-TRA-M-02.json`, con el
esquema existente del directorio (claves ordenadas, `indent=1`) más `p`, `clase`,
`ola_calibracion` y `grado_DD`.

| celda | encuesta/ola | `p` | clase | `ola_calibracion` | `grado_DD` |
|---|---|---|---|---|---|
| `TRA-M-01` | ENCIG 2023 | `0.62` | `ASIGNADO` | ENCIG 2023 | **`P0 VERIFICACION`** — coincide |
| `TRA-M-02` | ENCUCI 2020 | `0.62` | `ASIGNADO` | ENCIG 2023 | **`P1 PUNTUA`** — transferencia de instrumento |

Citas `archivo:línea` dentro de cada JSON: `p` en `milpa/tramite.yaml:45`;
`ola_calibracion` en `milpa/tramite.yaml:64` (`fuente: ["ENCIG2023", …]`), fijada
por `forense/notas/2026-08-31-marco-M-v1_1-spec.md` §(a) y confirmada por
`milpa/procedencia.yaml:782-786`.

**C1/C2 (`ADR-233`) aplicadas POR REFERENCIA**: `variable = AP5_17|AP5_18` y
`ponderador = FAC_SEL` se leen de `candidatos-marco-M-v1_1.tsv`.
**`marco-M-sorteado-v1_0.tsv` no se editó** — marcos v1_0 están fuera del
perímetro.

**Ciego a R.** `forense/prereg-duelo-v2/corridas-R/` **no se abrió**; ninguna
columna de valor de R se leyó. Los cinco archivos abiertos van listados dentro de
cada JSON:

```
canon/modelo-decision-v4_0.md                        [lectura vía import del emisor]
forense/prereg-duelo-v2/candidatos-marco-M-v1_1.tsv  [lectura]
forense/prereg-duelo-v2/marco-M-sorteado-v1_0.tsv    [lectura]
milpa/procedencia.yaml                               [lectura vía import del emisor]
milpa/tramite.yaml                                   [lectura vía emisor.cargar_reglas]
```

`M-TRA-M-02.json` incorpora además el aviso F-DD de arriba, con la emisión
alterna citada (`0.125822`) y por qué este acto no la usa.

---

## CONTADOR

| cifra del encargo | resultado |
|---|---|
| reglas del motor con `p` medida: 5 → 8 | **8** ✔ (`cargar_reglas()`) |
| dominios activos: 1 → 4 | **4** ✔ |
| peldaños con co-observación válida: N de 5 | **0 de 5** — negativo total, (d) completa |
| `N_elegibles` del marco-M v1_1 | **22** (de 27 filas; v1_0 tenía 2) |
| primeros puntos M: 2, uno verificación P0 | **2** ✔, `TRA-M-01` = `P0 VERIFICACION` ✔ |

---

## Lo que este lote NO hizo

No midió β̂ ni la corresidencia re-especificada. No sorteó (B″ queda
pre-registrado, no lanzado). No calculó R ni corrió L. No tocó
`milpa/procedencia.yaml`, `milpa/src/**`, `sorteo_v2.py`, los marcos v1_0,
`corridas-R/` ni nada de caja. No descargó nada. No editó
`marco-M-sorteado-v1_0.tsv` ni el cierre original de `MAESTRA32-E17`.

## Sucesores declarados, no lanzados

`B″ · MARCO-M-SORTEA-v1_1` (semilla del merge de este lote; debe filtrar
`elegible_v1_1`) · `RE-SPEC-CORRESIDENCIA` (caja, `FP-204`) · adquisición de
**WVS ola 7 México** (`FP-179` entrada 6) y, tras ella, el medidor de
`G5.radio_confianza` · `R-MARCO-M` (caja) · `L-MARCO-M` (fuera del proyecto,
D-iii) · re-intento de scoring cuando M tenga sus puntos y R los suyos ·
**decisión de mesa** sobre si el marco re-apunta `TRA-M-02` a la conducta
enmendada, y sobre si la enmienda ENCUCI sustituye o convive con el `0.62`.

---

**"El primer resultado que produzca este procedimiento es el que se reporta."**
