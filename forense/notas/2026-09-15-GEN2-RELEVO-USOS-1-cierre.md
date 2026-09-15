# ACTO GEN2-RELEVO-USOS-1 · cablear la última milla — nota de cierre

**Acto:** `ACTO GEN2-RELEVO-USOS-1`, 15/sep/2026, NUBE (`data/raw` ausente,
corpus `montado=NO`, `numpy`/`pandas`/`scipy`/`pyreadstat` **AUSENTES** —
verificado con `python3 tools/entorno.py`).
**Base observada al arrancar:** `origin/main = ce16af3b`.
**Base integrada:** `origin/main = 5973f121` (merge de `PR #785`,
`ACTO GEN2-FIRMAS-MESA-1`) — la compuerta de P4 se abrió durante el acto.
**Encargo archivado verbatim (0-bis A.3):**
`forense/encargos/2026-09-15-GEN2-RELEVO-USOS-1.md`.

## Qué hace este acto

El registro GEN2 tenía los dos extremos y no el cable. La demanda declara 207
slots (`RES-####`, un consumidor activo del aparato GEN1 cada uno) y la oferta
declara 3 255 RESULT GEN2 sellados; entre ambos, `demanda-resultados.tsv:sucesor`
estaba **vacío en las 207 filas** y `demanda-corridas.tsv` no tiene columna
`CALC` — su `medidor_o_spec_candidato` nombra un *script*
(`tools/emite_m.py`, `milpa/src/motor.py`, …), no un `CALC-*`. Por eso el
encargo manda **derivar** el cruce `CORR↔CALC` y no heredarlo por parecido de
nombres: `CALC-ENCIG-0001` no dice `CORR-0002` en ninguna parte de su id.

Este acto construye ese cable, lo comprueba contra sí mismo, mide la distancia
GEN1↔GEN2 de cada par con el contrato explícito de B-7, clasifica la
materialidad por consumidor y adopta lo que resultó adoptable.

## P1 · La tabla, derivada por cuatro canales declarados

`tools/relevo_usos.py` (nuevo) escribe `data/corrida0/relevo-usos-v1_0.tsv`
(`# DERIVADO — NO EDITAR`, 32 columnas, **una fila por cada uno de los 207
slots**) con el escritor canónico `corrida0._escribe`. No hay un solo enlace
elegido por parecido: cada uno sale de una declaración, y la columna `canal`
dice de cuál.

| canal | de dónde sale | qué fija |
|---|---|---|
| `C0-CONSUMIDOR` | el propio `milpa/`, leído con `corrida0._ids_corrida0_declarados` | la cita que YA existe — es el **control**, no un descubridor |
| `C1-MAPA` / `C1-SINGULAR` | `parametros.adopcion*` de la spec sellada | consumidor **y** RESULT |
| `C2-RESULTADO` | `resultados[].unidad` con verbo de enlace explícito (`releva`, `ADOPTABLE`, `candidato a`) | RESULT por RESULT |
| `C3-CORRIDA` | `etiquetas.demanda_que_releva`, **recortada antes de la primera negación** | sólo cobertura de la corrida |

El recorte de C3 no es cosmético: es exactamente donde viven los «NO releva
RES-0031/RES-0032», y un lector ingenuo los convertiría en candidaturas.

### El falsador del propio método

Una derivación que propone enlaces nuevos no vale nada si no reproduce los que
ya existen. `control_c0` es esa prueba, y se corre sola:

> **17 de las 18 citas GEN2 vigentes se reproducen exactamente desde la spec
> sellada. Cero discrepancias. La 18ª (`RES-0065`) no es derivable desde
> ninguna oferta y queda rotulada, no callada** (`NC-0212`).

### Veredicto por slot (207)

| veredicto | n | qué significa |
|---|---|---|
| `YA-ADOPTADO` | 18 | el consumidor ya cita GEN2 (16 al arrancar + las 2 de P4) |
| `LISTADO-PARA-MESA` | 11 | CALC sellada, rama de adopción sellada, **falta el pin de RESULT** (`NC-0215`) |
| `NO-ADOPTABLE-POR-VEREDICTO-SELLADO` | 8 | la corrida ya selló que no se cita |
| `VETADO-POR-DECISION` | 1 | `RES-0006`, `SIN CITA` firmado (D1/`NC-0108`) |
| `CANDIDATO-GEN2` | 1 | `RES-0028` |
| `SIN-CANDIDATO` | 168 | 137 `CORR-SIN-CALC-DECLARADA` · 19 `CALC-DECLARADA-NO-SELLADA` · 12 `CORR-CON-CALC-SIN-RESULT-FIJADO` |

**23 de las 82 corridas naturales ya tienen CALC sellada** — la respuesta
literal a la pregunta de P1 — y cubren **89 de los 207 slots**.

### El hallazgo que reordena el resto del acto

Varias specs **pre-declararon, antes de medir**, un RESULT de texto cuyo valor
es la rama de adopción del slot, y ese veredicto está medido y sellado. Este
acto lo **lee y lo obedece**; no lo recalcula ni lo reabre. Es la diferencia
entre cablear y re-decidir:

```
RESULT-ENCIG-MOR-ADOPCION-P3-RES-0009    = NO-ADOPTABLE-POR-GRANO:-0.000032000
RESULT-ENCIG-MOR-ADOPCION-P3-COMPLEMENTOS = COMPLEMENTO-CON-DENOMINADOR-RECORTADO
RESULT-ENVIPE-DEN-ADOPCION-P3            = ADOPTABLE-POR-REPLICA
RESULT-ENUT-A-ADOPCION                   = LISTADO-PARA-MESA-REPRODUCE
```

Sin esta capa, 9 slots habrían salido «candidatos» perfectamente cableados que
un sellado previo ya había prohibido citar.

## P2 · El delta, por script y con contrato

`tools/relevo_usos.py --contrato` genera el contrato `GEN2-DELTA-1` — **27
pares**, uno por slot con RESULT fijado, adoptados o no — y
`corrida0 delta` lo ejecuta. Ni los pares, ni los hashes, ni las citas se
teclean.

```
python3 tools/relevo_usos.py --contrato forense/relevo-usos/relevo-usos-pares-v1_0.yaml
python3 tools/corrida0.py delta --entrada forense/relevo-usos/relevo-usos-pares-v1_0.yaml --formato humano
```

> **27 pares examinados · 24 comparables · 0 incompatibles · 3 con
> comparabilidad no determinable · 24 deltas calculados · 4 materiales.**

Dos decisiones de construcción, ambas con motivo:

- **El lado A es el archivo del consumidor**, no la vista derivada:
  `milpa/tramite.yaml` con selector `yaml` y camino exacto, verificado contra
  `valor_legacy` antes de emitir el par. Es «la fuente legacy anterior a
  adopción» que `NC-0048` pide, y la vista derivada además no es
  direccionable (su cabecera `# DERIVADO` sería leída como encabezado por un
  `csv.DictReader`).
- **Los ya adoptados no se excluyen.** Para ellos el par es la correspondencia
  GEN1↔GEN2 declarada por identidad que `NC-0048` lleva abierta pidiendo, y el
  control permanente de que la cita sigue apuntando a la cifra que el
  consumidor materializa.

Las ocho dimensiones de comparabilidad las **declara este acto**, agrupadas en
cinco familias asignadas por derivación (veredicto sellado + canal), y cada
familia queda **anclada a un texto que tiene que seguir existiendo, literal, en
la spec sellada**. Si el ancla desaparece, el generador **para** en vez de
emitir un juicio que el árbol ya no sostiene. La diferencia entre una
declaración auditable y una suposición es que la de aquí se puede falsar con
`grep` — y de hecho ya paró dos veces durante la construcción.

### Control cruzado que nadie pidió y que salió bien

El delta, calculado por un camino independiente (archivo del consumidor →
`resultados.json`), **reproduce los dos veredictos sellados
`NO-ADOPTABLE-POR-GRANO`**: `RES-0009` da `−3.227042e−05` frente al
`-0.000032000` sellado, y `RES-0011` da `−2.362342e−06` frente al
`-0.000002000`. La corrida de septiembre y la de hoy coinciden a seis
decimales por vías distintas.

## P3 · Materialidad por consumidor (E.4), no por spec

Las cuatro pruebas del encargo, derivadas y escritas en la tabla:

- **signo** — se comprueba, no se supone; ambos lados son proporciones en
  [0,1], así que sale `NO` en los 24.
- **grano** — **dos umbrales, porque el árbol declara dos y no coinciden**:
  `umbral_grano_milpa = 1e-06` fijo, y el grano con que el consumidor
  *escribe* la cifra (`p: 0.116` son 3 decimales), que es el que aplica el
  comparador canónico de adopción. Se reportan por separado y se clasifica
  `MATERIAL` si **cualquiera** se cruza: la dirección conservadora manda a
  mesa en vez de adoptar. Que discrepen es un hallazgo (`NC-0214`), no un
  detalle.
- **clasificación** — una adopción es una **cita**: el `p` no se mueve, así
  que la `clase` sólo tendría que cambiar si cambiara la cifra. Se deriva del
  grano, no de leer etiquetas.
- **coeficiente central** — entra a mesa aunque el delta sea cero.

El **tier no se deriva**: subirlo o bajarlo es firma de mesa. Se reporta el
vigente (`FUERTE` en los 24) con el rótulo `NO-DERIVABLE-SIN-FIRMA`.

> **4 MATERIAL · 20 NO-MATERIAL · 3 NO-DETERMINABLE.**

### MATERIALES — a mesa, uno por uno, con su delta

| slot | consumidor | `reglas_impacto` | RESULT candidato | legacy | GEN2 | delta B−A | qué lo hace MATERIAL | veredicto sellado |
|---|---|---|---|---|---|---|---|---|
| `RES-0009` | `tramite.mordida.con_registro:paga_mordida_encig2025_presencial` | `tramite.mordida.con_registro` | `RESULT-ENCIG-MOR-B-P-PRE-CD` | 0.116 | 0.11596773 | `−3.227042e−05` | umbral `1e-06` (al grano escrito, 3 decimales, **no** cruza) | `NO-ADOPTABLE-POR-GRANO:-0.000032000` |
| `RES-0010` | `tramite.mordida.con_registro:tramite_normal_encig2025_presencial` | `tramite.mordida.con_registro` | `RESULT-ENCIG-MOR-B-P-NORMAL-PRE-CD` | 0.884 | 0.88403227 | `+3.227042e−05` | ídem (es el complemento de `RES-0009`) | `COMPLEMENTO-CON-DENOMINADOR-RECORTADO` |
| `RES-0011` | `tramite.mordida.con_registro:paga_mordida_encig2025_digital` | `tramite.mordida.con_registro` | `RESULT-ENCIG-MOR-B-P-DIG-CD` | 0.027358 | 0.02735564 | `−2.362342e−06` | **ambos**: grano escrito (6 dec.) y umbral | `NO-ADOPTABLE-POR-GRANO:-0.000002000` |
| `RES-0012` | `tramite.mordida.con_registro:tramite_normal_encig2025_digital` | `tramite.mordida.con_registro` | `RESULT-ENCIG-MOR-B-P-NORMAL-DIG-CD` | 0.972642 | 0.97264436 | `+2.362342e−06` | **ambos** (complemento de `RES-0011`) | `COMPLEMENTO-CON-DENOMINADOR-RECORTADO` |

Los cuatro caen sobre **una sola regla**, `tramite.mordida.con_registro`, y
los cuatro ya traen un veredicto sellado que impide la cita. **Ninguno se
adopta.** La pregunta que suben a mesa no es «¿se adoptan?» sino la de
`NC-0214`: cuál de los dos criterios de grano declarados gobierna, porque
`RES-0009`/`RES-0010` salen `IGUAL-AL-GRANO` y `MATERIAL` a la vez.

### NO-DETERMINABLE — 3, y en los tres el registro se niega con razón

| slot | RESULT candidato | por qué el delta no se calcula |
|---|---|---|
| `RES-0005` | `RESULT-ENCUCI-A-P-CUALQUIERA` | población `INFORMACION-INSUFICIENTE`: el veredicto sellado es `NO-ADOPTABLE-POR-DISCREPANCIA`, y una rama que no acredita no puede acreditar identidad de denominador (`NC-0217`) |
| `RES-0028` | `RESULT-ENVIPE-DEN-P-COMPLEMENTO-C2-U1` | el legacy es `1 − p(C2,U4)` y el candidato se cuenta sobre **U1**; el registro no declara que U1 y U4 sean el mismo universo, y este acto no lo supone |
| `RES-0035` | `RESULT-B-ENIGH-2022-P` | dos veredictos sellados en conflicto (`NC-0216`) |

### Dos adopciones vigentes que su propia corrida declaró no adoptables

`RES-0005` y `RES-0035` — ambas ya citadas con `corrida0_generacion: GEN2` —
traen un veredicto sellado que dice lo contrario:
`RESULT-ENCUCI-A-ADOPCION-P3 = NO-ADOPTABLE-POR-DISCREPANCIA` y
`RESULT-B-ADOPCION-P3 = NO-ADOPTABLE-POR-GRANO`.

**Las cifras no están mal**, y conviene decirlo antes que nada: `delta` las
comparó en este acto y coinciden a seis decimales (`0.126006` vs
`0.12600561`; `0.045694` vs `0.04569410`). Lo que falla es la
**auditabilidad**: cada veredicto se selló contra un valor GEN1 anterior
(`0.125822` en ENCUCI) o contra el umbral de reproducibilidad `1e-10`, no
contra el grano del consumidor, así que quien lea sólo la oferta ve dos citas
que su propia corrida desautorizó. No se reabre ningún sellado ni se retira
ninguna cita: se rotula (`NC-0217`, y `NC-0216` para el conflicto añadido de
`RES-0035`). Son la misma pregunta de fondo que `NC-0214`.

`RES-0028` es el único `CANDIDATO-GEN2` que queda, y es también el único par
con una diferencia visible a simple vista (0.705687 frente a 0.732757, ≈ 2.7
puntos). Que salga rechazado por comparabilidad **antes** de que nadie mire el
número es exactamente lo que debe pasar: sin identidad de población acreditada,
esa resta no significa nada.

## P4 · Adopción — la compuerta se abrió durante el acto

`ACTO GEN2-FIRMAS-MESA-1` se fusionó (`PR #785`) mientras este acto corría.
Se integró su base y **se re-derivó todo encima** antes de tocar `milpa/`.

**La regla del encargo («los NO-MATERIALES entran en bloque») se aplicó junto
con los veredictos sellados, no por encima de ellos.** De los 7 NO-MATERIAL
pendientes, 5 tienen un sellado o una firma que prohíbe la cita
(`COMPLEMENTO-CON-DENOMINADOR-RECORTADO` en `RES-0004/0014/0016/0022`, y
`SIN CITA` de D1/`NC-0108` en `RES-0006`). Adoptarlos por ser inmateriales
habría violado E.3 y una decisión firmada: **la materialidad no es la única
compuerta.** Quedan dos:

| slot | consumidor | RESULT adoptado | delta | qué cambió |
|---|---|---|---|---|
| `RES-0047` | `dinero.ahorro.horizonte_corto:horizonte_no_corto` | `RESULT-ENIF-AHO-A-P-NOCORTO-SIN-P` | **0.0 exacto** | sólo la cita |
| `RES-0049` | `dinero.ahorro.horizonte_no_corto_con_seguridad_social:horizonte_no_corto` | `RESULT-ENIF-AHO-A-P-NOCORTO-CON-P` | **0.0 exacto** | sólo la cita |

Son el caso limpio de «última milla»: la cifra que `milpa/` ya materializaba
**era** la medida por `CALC-ENIF-0001`, y lo único que faltaba era decir de
dónde venía. `adopcion_p3.nota` de la spec sellada lo autoriza por su propio
criterio pre-declarado — estas celdas «se cuentan DIRECTAMENTE (P4_10 en
{3,4,5}), no como 1 menos el otro, así que satisfacen el criterio (1) y SÍ son
cantidad medida» —, y ambas son estimables con IC y diseño
(`n = 4 973` / `3 969`). **El `p` no se movió un dígito**: el diff de
`milpa/tramite.yaml` añade dos claves y dos comentarios, y nada más.

## Contadores (E.4, derivados, `corrida0 status`)

| contador | antes | después |
|---|---|---|
| `dependencias_numericas_legacy_activas` | **191** | **189** |
| `N_resultados_gen2_adoptados_activos` | 16 | **18** |
| `N_resultados_activos` | 207 | 207 |
| `N_resultados_pendientes` | 207 | 207 |

`dependencias_numericas_legacy_activas` **baja por primera vez desde que abrió
GEN2**, que es lo que el encargo reservó a este acto. `N_resultados_pendientes`
**no se mueve, y no debía moverse**: un slot es `PENDIENTE` hasta que tenga
`valor_gen2` propio, que es una **medición**, no una adopción — medir no es
pieza de este acto.

`diferencias_materiales` sigue en 0: ese contador lee `delta_legacy` de
`resultados.tsv`, que este acto no rellena. Las 4 diferencias materiales que sí
encontró viven en `relevo-usos-v1_0.tsv` y en el informe de `delta`, y el
contador de `status` no las ve. Se dice, no se calla.

## Lo que este acto NO hizo

- **No re-derivó las tres vistas canónicas.** `corrida0 registro --escribe` se
  **negó**, y no se forzó: escribir aquí bajaría `resultado_replay` /
  `contexto_replay` de `REPRODUCE`/`IDENTICO` a `NO-VERIFICADO` en **17
  corridas publicadas ajenas a este acto**, porque este clon de nube no puede
  reejecutar `verify`. El propio comando lo dice: «No existe `--force`: un
  veredicto ajeno no se mueve sin razón explícita». Consecuencia acotada y
  declarada (`NC-0211`): las vistas quedan atrasadas **exactamente por las 2
  filas adoptadas**, y no afecta a ningún contador — `status` deriva en
  memoria, y `relevo-usos-v1_0.tsv` lee la adopción del archivo del consumidor
  y no de `usos.tsv`, justamente para no creerle a una vista sin re-derivar.
- **No midió nada**, no tocó specs ni sellos, no reabrió un veredicto sellado,
  no adoptó nada que un sellado o una firma prohibieran, y no eligió entre los
  dos criterios de grano en conflicto.

## Verificación

| comprobación | resultado |
|---|---|
| `python3 tests/check.py --baseline` | **LÍNEA BASE: VERDE** — 3 FAIL · 4 027 WARN, cero novedad frente a `tests/baseline.json` |
| `python3 tests/test_corrida0.py` | 91/91 OK |
| `python3 -m unittest tests/test_delta_comparacion.py` | 11/11 OK |
| `control_c0` de la propia derivación | 17 COINCIDE · 0 DISCREPA · 1 declarado |
| control cruzado delta ↔ veredicto sellado | reproduce los dos `NO-ADOPTABLE-POR-GRANO` |

## NO-CORRIDO abierto por este acto

`NC-0211` (vistas sin re-derivar, bloqueo de entorno) · `NC-0212` (`RES-0065`
no auditable desde la oferta) · `NC-0213` (`CALC-ENVIPE-0001` cita `CORR-0009`
donde va `CORR-0007`) · `NC-0214` (dos criterios de grano en conflicto) ·
`NC-0215` (11 slots con CALC sellada y sin pin de RESULT) · `NC-0216`
(veredictos sellados en conflicto sobre `RES-0035`) · `NC-0217` (dos
adopciones vigentes contra su veredicto sellado).

`no_corrido_abiertas` 60 → 67.

De los siete, **`NC-0215` es el lote más barato que queda en todo GEN2**: 11
consumidores que siguen leyendo GEN1 cuya medición GEN2 ya existe, ya está
sellada y ya reproduce. No hay que medir nada; hay que declarar el enlace.

## `NC-0048`

Sigue **ABIERTA**, y este acto la mueve sin cerrarla. Aporta **27
correspondencias declaradas por identidad** con consumidor, uso, fuente legacy
anterior a adopción, CALC+RESULT sellado y las ocho dimensiones —
exactamente la forma que `NC-0048` pide — y 24 deltas calculados. No la cierra
porque son 27 de los 211 RESULT históricos, y porque `valor_legacy` /
`delta_legacy` de `resultados.tsv` siguen sin rellenarse: el generador es
reutilizable, pero el resto de los pares necesita que alguien declare su pin
(`NC-0215`) o su identidad de población.
