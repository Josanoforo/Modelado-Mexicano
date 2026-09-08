# `ACTO GEN2-E7 · READINESS-2` — nota de cierre (piezas A y B, NUBE)

8 de septiembre de 2026 · entorno **NUBE, sin corpus ni red** · `ADR-398` ·
rama `claude/nube-e7-readiness-gen2-873cj3`.

**Alcance de esta nota.** Cubre **solo las piezas A y B**. La **pieza C**
(verificación adversarial de INFRA con muestra propia; cierre de `NC-0001`)
es de **caja/UBUNTU** y **no se lanzó aquí**, según la cabecera del propio
encargo. Por eso `no_corrido_abiertas` **no baja** con este acto.

---

## 0 · Compuerta

Comando del encargo, por producto:

```
$ git show origin/main:tools/corrida0.py | grep -c "def cmd_registro\|def cmd_status"
2
```

**Nota de método, asentada porque importa.** El primer intento devolvió `0`,
con `fatal: path 'tools/corrida0.py' exists on disk, but not in
'origin/main'`. La causa era la referencia local `origin/main`
desactualizada, no una compuerta incumplida. Se resolvió con
`git fetch origin main` y se recomputó → `2`. Se deja escrito porque **un `0`
de ese origen es indistinguible, a la vista, de una compuerta real que no se
cumple**, y el acto anterior (`GEN2-E6`) ya cerró una vez con cero commits
por una compuerta que sí faltaba: confundir los dos casos cuesta un acto.

---

## 1 · Qué se entregó, pieza por pieza

### A1 · Wrapper M — `CALC-M-marco-M-sorteado-v1_3`, **sellado**

| | `emite_m.camina()` (histórico) | este wrapper |
|---|---|---|
| marco | `marco-M-sorteado-v1_1.tsv` **cableado** | input `origen: repo` con sha, verificado por `preflight` |
| escritura | escribe `corridas-M/M-<id>.json` | no escribe; `run` sella |
| reanudación | `if destino.exists(): YA-EXISTIA` | sin estado previo que saltear |
| esquema | lo lee de `corridas-M/M-TRA-M-01.json` (GEN1) | comprueba los campos que consume |

`grado_DD` sale **por conducta** (corrección de `MAESTRA38-M13`, ya en
`emite_m.py`; el wrapper no la re-implementa).

**`ciego_a_R` se verifica, no se declara.** `emite_m.py` emite una constante
`CIEGO_A_R` en cada registro; una constante es una afirmación, no una prueba.
El medidor arma un `sys.addaudithook` sobre `open` **antes** de importar
`emite_m` y de tocar el marco, cuenta toda apertura de la ventana de emisión
y levanta `AperturaProhibida` si alguna cae bajo `corridas-{R,M,L}/` o
`agregado_v1_3`. `RESULT-M-CIEGO-A-R` es el recibo del hook.

Cifras: `N-CELDAS = 14`, `N-EMITIDAS = 14`, `verify` → `REPRODUCE`.

### A2 · Adaptador R — `tools/arbitra_gen2.py`, **NO ejercido**

`arbitra.procesa_fila` llama `localiza_payload(manifiesto, encuesta, ola)`:
heurística de substring sobre `id` + `archivo` que devuelve una **lista** de
candidatos y deja `payload_id_candidatos` —en plural— en el JSON de la celda.
El adaptador **no la importa ni la llama**: el `payload_id` sale exacto de la
columna `payload_id` de `codificacion-R-v1_0.tsv` (la misma fila que declara
`tabla`, `variable`, `codificacion`, `ponderador`, `estrato`, `upm`) y su ruta
la resuelve `tests/payload_resolver.resolver_payload`, el mismo resolver único
que `corrida0.py` ya usa para todo input `origen: manifiesto`. Sin fallback:
una celda sin `payload_id` declarado levanta `SinPayloadDeclarado`.

**R no corre aquí** — necesita corpus y va a caja. Verificado en este entorno:
las 14 celdas resuelven a `AUSENTE` (no hay `data/raw/`). **No se depositó
ningún `data/corrida0/CALC-R-*/`**, como el perímetro exige; `spec_de_celda()`
emite la spec sobre un destino que el llamador da, y los tests la ejercen.

### A3 · Corredor L sucesor — `corredor_l_v1_2.py`, **CONTADOR cero**

Sucesor y no parche, por una razón concreta: `runner_l_cli.py` importa
`carga_l_v1_1.py`, que tiene cableado `L_SPEC_JSON = DIR / "L-spec-v1_1.json"`
y un `assert len(celdas) == 11` en su dry-run. El universo del marcador es de
**14**. Parchear ese cargador lo volvería dos cosas a la vez y rompería el
dry-run que él mismo declara.

De paso, el sucesor deja de necesitar `celda_a_spec`, que colapsaba
`variable`/`estimador` a `conducta` y dejaba `frase_discriminacion` vacía para
alimentar un `SpecCelda` escrito para el marco piloto: `L-spec-v1_2.json` ya
trae `pregunta_L` redactada y sellada, y el prompt se toma **verbatim**.

Salida en **`corridas-L-gen2/`**. Las 424 capturas de `corridas-L/` son GEN1:
no se releen, no se re-nombran, no se pisan, y el esquema de salida se declara
en `ESQUEMA_SALIDA` en vez de verificarse contra un ejemplo de ellas (que es
lo que hacen los dos dry-run existentes). `--dry-run`: 224 corridas
planificadas, 224 rutas únicas, **ninguna llamada al modelo**.

### A4 · Agregado sucesor — `CALC-AGG-marco-M-sorteado-v1_3`, **sellado**

Corrida **derivada**, `ci_replayable: true`: sus dos insumos son archivos
versionados con sha (`resultados.json` de `CALC-M` + el marco vigente). Frente
a `agregado_v1_3.py`, que resuelve por **convención de nombre**
(`ORDEN_RESOLUCION_M`) y lista `corridas-{R,M,L}/` en disco —donde un archivo
suelto entra a la cifra sin que nada lo declare, y con un doble conteo en
`a13_conteo_archivos_examinados` que el propio script documenta y no corrige—,
este consume **solo lo declarado**.

**Lo que no se puede estimar se declara.** `N-CON-R = 0`, `N-CON-L = 0`, y
por tanto `EJE-M-VS-R` / `EJE-M-VS-L` en `NO-ESTIMABLE` **con el motivo
escrito**. No se rellenan con la cifra GEN1. El delta contra
`agregado-v1_3-resultado.json` **no se calcula**: mientras R y L no tengan
corrida GEN2, compararía un agregado de un eje contra uno de tres. Cuando
exista, el encargo lo permite como input `valor_legacy` — lectura declarada,
no insumo; hoy ninguna spec la declara.

`RESULT-AGG-M-P-DISTINTOS` se **re-deriva** desde los `RESULT-M-*` en vez de
copiar `RESULT-M-P-DISTINTOS`. Coincide (5). Copiar el número habría hecho
imposible notar una discrepancia entre las dos corridas.

### A5 · Paso 3 — verificado como **diseño**, decisión **no tomada**

`forense/notas/2026-09-08-GEN2-E7-paso-3-unidad-de-celda.md`: el diagnóstico
medido, cuatro opciones con su costo y lo que la mesa firmaría en cada una.
**La unidad de celda es decisión de mesa y este acto no la toma.**

### B · Go/No-Go → **`GO-MARCADOR`**

```
  [PASA] MARCO-VIGENTE-UNICO      [PASA] L-SPEC-v1_2
  [PASA] M-DESDE-CONTRATO         [PASA] AGREGADO-DERIVADO
  [PASA] R-SIN-HEURISTICA         [PASA] LEGACY-NO-LEIDO
```

---

## 2 · Los dos defectos que este acto cometió y corrigió

**(1) El Go/No-Go medía comentarios.** La primera versión escaneaba el
**texto** de los artefactos y reportó **36 fallos**, casi todos falsos:
marcaba como violación de `LEGACY-NO-LEÍDO` la línea del docstring que dice
«este corredor no abre `corridas-L/`» y la constante `LEGADO_PROHIBIDO`, que
existe precisamente para prohibirlo. **Un check que castiga a la defensa por
nombrar al atacante no mide nada.**

Se rehízo sobre dos herramientas, una por propiedad:

- **«no LLAMA a la API del legado»** → **AST**. Se recolectan identificadores
  reales (`Name.id`, `Attribute.attr`, módulos importados, el argumento de
  `spec_from_file_location`). La prosa de un docstring no es un identificador.
- **«no ABRE archivos del legado»** → **audithook** alrededor de la ejecución
  real de cada corredor en su modo de readiness. Atrapa la ruta armada por
  concatenación, que ningún escaneo estático ve.

**(2) `constantes_str` no veía la línea que tenía que leer.** Sólo miraba
`NOMBRE = "literal"`, así que no veía
`L_SPEC_JSON = DIR / "L-spec-v1_2.json"` — un `BinOp` — que es exactamente la
línea de la que depende `L-SPEC-v1_2`. Se camina el valor entero de la
asignación.

Ambos defectos tienen caso de prueba propio
(`t_gonogo_ast_ignora_la_prosa_y_ve_las_llamadas`,
`t_gonogo_ve_la_constante_armada_con_barra`): sin ellos, un verde de esos dos
checks no distinguiría «funciona» de «no mide nada».

También en `LEGACY-NO-LEÍDO`, un tercer ajuste del propio wrapper M: la
primera versión llamaba `emite_m.esquema_de_referencia()`, que lee
`corridas-M/M-TRA-M-01.json`. Es legado GEN1. Se sustituyó por la
comprobación de los campos que el medidor consume, que es lo único que ese
CALC puede afirmar.

---

## 3 · Dos afirmaciones vigentes que quedan vencidas

**(a) `diagnostico-14-celdas-v1_0.tsv`** trae `p_emitida = 0.62` para
`TRA-M-02/-03/-07`. Contra el marco **vigente** esas tres emiten
**`0.085118`**. No es error del diagnóstico: es correcto para `v1_2` y quedó
atrás en `v1_3`, donde `MAESTRA38-M13` re-apuntó esas celdas de
`paga_mordida` a `paga_mordida_encig2025`. Las otras once filas coinciden.

**(b) El `aviso_M` de `L-spec-v1_2.json`** dice que `DIN-M-01` «NO tiene M: el
emisor se negó a emitirla». **Ya no es cierto**: con `grado_DD` por conducta
emite `p = 0.174804`, `grado_DD = P1 PUNTUA`. Las **14 de 14** emiten.

Ninguno de los dos se edita: están fuera del perímetro y son archivos
sellados de otro acto. Se asienta la discrepancia y su causa (`NC-0017`).

---

## 4 · Contador

**CERO GEN2 del modelo.** Ninguna `p` de `CALC-M` es nueva: son las que
`milpa/src/emisor.py` ya emitía. Lo nuevo es que **nacen con cadena** —spec,
contrato ejecutable, snapshot de inputs con sha, `ejecucion.json`, sello y
`verify`—, que es exactamente lo que el encargo pedía: *«envuelve lo que
existe para que el primero que se produzca ya nazca con cadena»*.

Las dos corridas selladas corren sobre **insumos de repo** y nacen
`cuenta_gen2: PENDIENTE-DE-MESA` por etiqueta de su spec. Si cuentan como
GEN2 lo firma mesa en el merge, no lo decide el corredor.

---

## 5 · A.14 · NO-CORRIDO / RESERVAS

- **`NC-0015`** — A2: los `CALC-R-<celda>` no se depositaron ni corrieron.
  `FUERA-DE-PERÍMETRO` (el encargo lo excluye; NUBE no tiene corpus).
  Sucesor: acto de caja.
- **`NC-0016`** — A3: las 224 corridas reales de L no se ejercieron.
  `CONTADOR-CERO-DECLARADO`. Sucesor: acto con presupuesto y firma.
- **`NC-0017`** — A5: la decisión de unidad de celda y la corrección de los
  dos documentos vencidos. `DECISIÓN-DE-MESA` / fuera de perímetro.

**`NC-0001` sigue ABIERTA**: es de la pieza C, que no se lanzó aquí.

---

## 6 · Suite

```
tests/gonogo_marcador.py            -> GO-MARCADOR (6/6)
tests/test_corredores_gen2.py       -> 17 casos · 17 ok · 0 FALLOS
tools/corrida0.py verify CALC-M-marco-M-sorteado-v1_3    -> REPRODUCE
tools/corrida0.py verify CALC-AGG-marco-M-sorteado-v1_3  -> REPRODUCE
```

`tests/check.py --baseline`:

```
  3 FAIL · 188 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
  (HEAD congelado dee5fc544b4e6ff96d5506a1605546e1df6a68e3)
  (5 entradas de la línea base ya no aparecen — mejora, no bloquea)
```

Los 3 FAIL (`T06` ×2, `T08`) son de la línea base congelada, ajenos a este
acto. **Un FAIL nuevo apareció durante el acto y se corrigió**: `T25` marcó
un rótulo pelado del espacio `M` en la nota de A5 (D-6/ADR-128); se le dio
su prefijo de espacio, `MAESTRA38-M13`. *(Esta frase tampoco escribe el
rótulo pelado: nombrarlo aquí volvería a disparar `T25` sobre esta misma
nota, que es exactamente como se descubrió.)* El `spec.md` sellado de `CALC-M` conserva la
forma corta y `T25` no lo señala — reescribirlo rompería su
`spec_md_sha256` y su sello para complacer a un test, que es exactamente lo
que la casa no hace.
