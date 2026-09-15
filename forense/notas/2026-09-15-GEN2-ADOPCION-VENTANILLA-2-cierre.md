# ACTO GEN2-ADOPCION-VENTANILLA-2 · la ventanilla no se vacía por decreto: se lee, se dispone y se dice

Nota de cierre. Encargo archivado verbatim en
`forense/encargos/2026-09-15-GEN2-ADOPCION-VENTANILLA-2.md` (0-bis A.3).

**Base:** redactado por dirección contra el corte del 14/sep noche y
**re-derivado al abrir** contra `origin/main = a29d873` (`PR #759`), como la
propia cabecera manda. `git rev-list --count HEAD..origin/main` → `0`.

**Entorno (NUBE, cero microdato), `python3 tools/entorno.py`:**

```
numpy=AUSENTE  pandas=AUSENTE  pyreadstat=AUSENTE  scipy=AUSENTE  yaml=6.0.1
data/raw ausente -- normal en un clon fresco / en la nube
git_commit=a29d873b5a662d154604df4d110b32bbc6df29d9  git_status=LIMPIO
```

**COMPUERTA: ninguna** — el encargo lo declara; no dispara verificación.
Corrió en paralelo con `VERIFICACION-CAJA-2` (caja); **cero pisadas**: el
único archivo compartido posible era `forense/no-corrido.tsv`, y este acto
sólo **appendea** (`NC-0185`/`NC-0186`/`NC-0187`), no reescribe filas ajenas.

---

## P1 · El censo de la ventanilla, leído del registro

### 1.1 · Los cinco persistentes — **son los mismos**, no entraron nuevos

```
$ python3 tools/corrida0.py status
N_resultados_gen2_pendientes_adopcion=5
N_resultados_gen2_adoptados_activos=16
```

Los ids se derivan re-ejecutando la lógica de `status`
(`tools/corrida0.py:4177-4187`: `_resultados_citados_en(PROPUESTA) ∩
ids_sellados_gen2 − ids_adoptados`), no se copian de la nota anterior:

```
$ python3 - <<'EOF'
  ... (misma expresión que status, en memoria)
PENDIENTES: ['RESULT-C1-POSEL-AMENAZA-VEREDICTO', 'RESULT-C1-POSEL-OFERTA-VEREDICTO',
             'RESULT-CTX-2019-P-ALTO', 'RESULT-CTX-2021-P-ALTO', 'RESULT-CTX-2023-P-ALTO']
ADOPTADOS: 16
```

**Idénticos a los cinco del `ACTO GEN2-ADOPCION-COLA-5` (`PR #753`,
`ADR-495`).** La pregunta que el encargo manda dirimir *leyendo, no
suponiendo* —¿son los mismos con destino ya propuesto, o entraron nuevos?—
queda contestada: **son los mismos**, y el `#753` ya les dio destino. Este
acto **no los re-trabaja**: los re-presenta con la cita, como el encargo
ordena (*«no repite lo que #753 ya dejó propuesto»*).

| RESULT id | CALC | consumidor | disposición del `#753` | por qué sigue en la ventanilla |
|---|---|---|---|---|
| `RESULT-C1-POSEL-OFERTA-VEREDICTO` | `CALC-0001` | ninguno cargado | **NO-ADOPTABLE-POR-DECISIÓN** (`FP-357`/`ADR-422`; sucesor `CALC-0001-v2`/`ADR-456`) | el contador **no distingue** «vetado por decisión» de «pendiente de mesa» — `NC-0168`, abierta |
| `RESULT-C1-POSEL-AMENAZA-VEREDICTO` | `CALC-0001` | ninguno cargado | ídem | ídem `NC-0168` |
| `RESULT-CTX-2019-P-ALTO` | `CALC-0002` | ninguno cargado | **DECISIÓN-DE-MESA** propuesta, sin ejecutar | mesa no ha firmado |
| `RESULT-CTX-2023-P-ALTO` | `CALC-0002` | ninguno cargado | ídem | mesa no ha firmado |
| `RESULT-CTX-2021-P-ALTO` | `CALC-0002` | ninguno cargado | ídem (además `NO-ESTIMABLE-INDICE-INCOMPLETO`) | mesa no ha firmado |

La pregunta exacta para mesa sigue siendo la que el `#753` escribió y **no
se re-redacta aquí** (`ADR-495`, y `forense/notas/2026-09-14-GEN2-ADOPCION-COLA-5-cierre.md`
§P2): ¿se adopta «contexto institucional alto entre víctimas de extorsión»
(LAPOP 2019/2023) como **estimando descriptivo nuevo**, con consumidor
propio y `uso_motor` no-inferencial, dejando 2021 `NO_COVERAGE`?

### 1.2 · Los 69 de EDER (`CALC-EDER-0001`, `PR #760`)

```
$ python3 -  (derivado de data/corrida0/resultados.tsv, en memoria)
n EDER res: 69   corrida: CALC-EDER-0001--0cbaba6cea97   estado: SELLADA   cuenta_gen2: SI
familias: A=27 · B=19 · G=23
citas en milpa/: 0     citas en data/corrida0/usos.tsv: 0
```

No aparecen en `N_resultados_gen2_pendientes_adopcion` porque ese contador
sólo mira lo **citado en `PROPUESTA`**, y el consumidor de EDER
(`familia.corresidencia.adulto_familiar`,
`milpa/tramite-ola5-propuesta-v0.yaml:110`) **no trae
`corrida0_resultado_id`**: está `SELLADA-SIN-CARGA` con su `p` de fase 1.
Por eso el contador dice 5 y no 6 — la ventanilla tiene una puerta lateral
que este censo sí mira.

| grupo | n | tiene consumidor | disposición |
|---|---:|---|---|
| `RESULT-EDER-A-P` | 1 | **sí** — `familia.corresidencia.adulto_familiar`, sin cita GEN2 vigente | **DECISIÓN-DE-MESA**, ya propuesta: `NC-0183` |
| `RESULT-EDER-A-P-COMPLEMENTO` | 1 | el mismo, conducta `nunca_coreside_*` | **DECISIÓN-DE-MESA**, viaja con el primario (ver §2.2) |
| `RESULT-EDER-B-P`, `B-IC-*`, `B-EE-TAYLOR`, `B-CLAUSULA-SE-MUEVE-SI`, `B-DELTA-VS-A` | 6 | ninguno propio | **DECISIÓN-DE-MESA**, son el insumo de la cláusula `se_mueve_si` — misma pregunta, `NC-0183` |
| resto de `A` (IC, EE, embudo, veredictos, deltas vs GEN1) | 25 | ninguno | **descriptivos** — guardias y trazabilidad de la corrida |
| resto de `B` (embudo del ponderador `factor_per`) | 13 | ninguno | **descriptivos** |
| `G-*` (estructura, llaves, anidamiento, tipos) | 23 | ninguno | **descriptivos** |

**No hay ninguna cita GEN2 re-apuntable por sucesión.** La pregunta del
encargo (*«¿cuáles tienen consumidor con cita GEN2 re-apuntable?»*) se
contesta con el archivo: `familia.corresidencia.adulto_familiar` **nunca
tuvo** `corrida0_resultado_id` — su `p: 0.996086` entró por fase 1 (GEN1) y
mesa lo devolvió a re-especificación (`FP-200=b`). Re-apuntar exige **crear**
la cita, no moverla: eso es adopción nueva, y `NC-0183` la tiene reservada a
mesa.

### 1.3 · Los `B` nuevos (`PR #757`)

```
CALC-B-MARCO-ENVIPE-0001: n=226  citas_milpa=0  citas_usos=0
CALC-B-MARCO-ENCIG-0001:  n= 45  citas_milpa=0  citas_usos=0
CALC-B-MARCO-ENIGH-0001:  n= 45  citas_milpa=0  citas_usos=0
CALC-B-MARCO-MAE-0001:    n=155  citas_milpa=0  citas_usos=0
                          ------
                           471 RESULT, cero citas
```

**Destino declarado, no forzado:** disponibles para la tríada, fuera del
motor. La cita no es de este acto sino de la spec congelada **antes** de
abrir microdato — `forense/prereg-caja/B-MARCO-spec-v1_0.md`, fila «QUÉ NO
ES»: *«No mueve ninguna regla del motor: ninguna cifra suya entra a un
veredicto (`T9`)»* y *«No re-corre la tríada ni toca su veredicto
(`SIN-GANADOR-UNICO` / `INCONCLUSO` quedan como están)»*.

**Un precedente que se declara y NO se generaliza.** La sonda encontró
**una** cita viva desde un `CALC-B`:

```
$ grep -n RESULT-B- milpa/tramite.yaml
869: {conducta: recibe_remesas, ..., p: 0.045694, corrida0_resultado_id: RESULT-B-ENIGH-2022-P,
      corrida0_generacion: GEN2, ...}   # ACTO GEN2-PRIMERA-SILLA P4 (firma de mesa 8/sep/2026)
```

Es `CALC-B-0001`, no `B-MARCO`, y está adoptada **como tasa medida ENIGH
2022** para `recibe_remesas` — no como línea base de duelo. Que un `CALC-B`
haya producido un número adoptable por otro concepto no convierte a `B` en
adoptable. Queda asentado en `NC-0187` para que nadie lo lea al revés.

---

## P2 · Adopción o declaración — exactamente una salida por elemento

| elemento | salida | evidencia |
|---|---|---|
| `RESULT-C1-POSEL-OFERTA-VEREDICTO` · `RESULT-C1-POSEL-AMENAZA-VEREDICTO` | **NO-ADOPTABLE-POR-DECISIÓN** | `FP-357`/`ADR-422` (`NO-ESTIMABLE-CON-ESTA-FUENTE`, «no rescatable con `n`») + `D14`/`ADR-456` («sin mover `R7.3`/`R7.6` ni cargar tasas al motor»). Re-presentada del `#753`, no re-derivada. |
| `RESULT-CTX-2019-P-ALTO` · `RESULT-CTX-2023-P-ALTO` · `RESULT-CTX-2021-P-ALTO` | **DECISIÓN-DE-MESA** (ya propuesta) | `GEN2-E5-0` + `D15`/`ADR-456`; pregunta exacta en `ADR-495`. **No se re-ejecuta ni se re-propone.** |
| `RESULT-EDER-A-P` (+ `A-P-COMPLEMENTO`, + los 6 de la cláusula `B`) | **DECISIÓN-DE-MESA** (ya propuesta) | `NC-0183`, abierta: *«mesa: firma sobre (a) cita `corrida0_*` de `RESULT-EDER-A-P` en la propuesta y (b) la consecuencia literal de `se_mueve_si`»*. |
| los otros 61 `RESULT` de EDER | **descriptivos, sin consumidor** | sonda: 0 citas en `milpa/`, 0 en `usos.tsv`. |
| los 471 `RESULT` de `CALC-B-MARCO-*` | **NO-ADOPTABLE-POR-DECISIÓN** | `prereg-caja-B-MARCO` «QUÉ NO ES» (`T9`), congelada antes de medir; `SIN-GANADOR-UNICO` de la tríada intacto. `NC-0187`. |
| las 143 de Banxico/MOTRAL/SHED | **NO-ADOPTABLE — sin consumidor** | ver P3; `NC-0186`. |

### 2.1 · La sonda de consumo, en solo-lectura (el árbol no se tocó)

```
CALC-BANXICO-PRODUCTO-DANO-0001:    n= 35  citas_milpa=0  citas_usos=0
CALC-MOTRAL2015-VALORACION-SS-0001: n= 42  citas_milpa=0  citas_usos=0
CALC-SHED2025-BNPL-DANO-0001:       n= 66  citas_milpa=0  citas_usos=0
CALC-EDER-0001:                     n= 69  citas_milpa=0  citas_usos=0
CALC-B-0001:                        n= 90  citas_milpa=1  citas_usos=1   <-- RESULT-B-ENIGH-2022-P
CALC-B-MARCO-ENVIPE-0001:           n=226  citas_milpa=0  citas_usos=0
CALC-B-MARCO-ENCIG-0001:            n= 45  citas_milpa=0  citas_usos=0
CALC-B-MARCO-ENIGH-0001:            n= 45  citas_milpa=0  citas_usos=0
CALC-B-MARCO-MAE-0001:              n=155  citas_milpa=0  citas_usos=0
```

(`milpa` = `milpa/tramite.yaml` + `milpa/tramite-ola5-propuesta-v0.yaml`.)

### 2.2 · `D1` (complementos) — se cita con precisión, no se invoca de adorno

`D1`/`NC-0108` (`ADR-…`, gobernanza:7846) veta adoptar como **medidos** los
complementos `1 − p` **sobre denominadores con residuo heterogéneo**.
`RESULT-EDER-A-P-COMPLEMENTO = 0.003914398003122834` es `1 − p` sobre el
**mismo** universo, con `RESULT-EDER-A-SUMA = 1.0` y residuo **cero** — no
es el caso que `D1` veta. Por eso **no** se le pone
`NO-ADOPTABLE-POR-DECISIÓN`: si mesa firma `NC-0183`, entra con el primario
como `DERIVADO·q=1-p`, mismo universo e incertidumbre, y si no firma, no
entra nadie. Decirlo al revés habría sido usar una decisión vigente como
coartada.

### 2.3 · Contadores, crudos (E.4)

| contador | antes | después | por qué |
|---|---:|---:|---|
| `N_resultados_gen2_adoptados_activos` | 16 | **16** | cero adopciones ejecutadas: todo lo censado cae en `NO-ADOPTABLE-POR-DECISIÓN`, `DECISIÓN-DE-MESA` ya propuesta, o descriptivo sin consumidor. |
| `N_resultados_gen2_pendientes_adopcion` | 5 | **5** | los cinco son los mismos; el índice sigue sin tercera categoría para «vetado por decisión» (`NC-0168`, abierta). |
| `dependencias_numericas_legacy_activas` | 191 | **191** | ninguna cita nueva; `RES-0063`/`RES-0064` siguen `LEGACY-NO-DECLARADO` por `NC-0169`, que es de CAJA. |
| `N_resultados_gen2_sellados` | 2882 | **2882** | este acto no mide. |
| `no_corrido_abiertas` | 66 | **69** | `NC-0185` + `NC-0186` + `NC-0187`. |

Ningún otro contador de `status` se mueve.

### 2.4 · ENSANUT (`RES-0063`/`RES-0064`) — verificado antes de tocar, y no se toca

```
$ grep -E "^RES-006[34]" data/corrida0/usos.tsv | cut -f1,2,6
RES-0063  milpa/tramite.yaml:salud.vacunacion.disponible_ensanut2024:razon_no_vacunacion_logistica      LEGACY-GEN1
RES-0064  milpa/tramite.yaml:salud.vacunacion.disponible_ensanut2024:razon_no_vacunacion_no_logistica   LEGACY-GEN1
$ awk -F'\t' '$1 ~ /^NC-016[789]$/ {print $1, $10}' forense/no-corrido.tsv
NC-0167 ABIERTA   NC-0168 ABIERTA   NC-0169 ABIERTA
```

**EXISTE-SATISFACE:** el consumidor está sellado y cargado
(`milpa/tramite.yaml:1297-1325`, `ADR-D2i`, firma de mesa *«1, la cargamos»*)
con los dos valores exactos, y el paso que falta —registrar el `CALC` en
`corrida0`— es ejecución de infraestructura en CAJA, ya contratada por
`NC-0169`. **Se cita y no se repite**, como el encargo manda.

---

## P3 · Las fichas — enlazadas donde toca, y donde no toca se dice

La orden de mesa del 12/sep: *«comprobar el enlace desde la demanda, sólo
donde exista consumidor y uso compatible»*. Se comprobó, consumidor por
consumidor, contra los **22 consumidores cargados** en `milpa/tramite.yaml` y
las **50 reglas propuestas** en `milpa/tramite-ola5-propuesta-v0.yaml`.

| ficha | estimando que ofrece | consumidor compatible | resultado |
|---|---|---|---|
| **Banxico** (`#746`, `data/banxico-producto-dano-medicion/ficha-consumo-banxico.md`) | atraso / imposibilidad / daño combinado por **producto de crédito** y ola, Banxico 2019–2024 | **ninguno.** Las 22 reglas cargadas cubren mordida, gobierno digital, evasión de norma, denuncia, ahorro, remesas, unión, cuidado, participación, protesta y vacunación. No existe regla cuyo `p` sea una tasa de daño crediticio por producto. | **evidencia disponible, sin enlace** |
| **MOTRAL/N35** (`#747`, `data/motral2015-valoracion-ss/ficha-uso.md`) | P17 «preferencia declarada por empleo con seguridad social» (0.823627) y ranking P16 | **ninguno.** El consumidor natural sería `trabajo.prestaciones.formalidad_pesa_mas_que_salario` (R2.3) — **no está cargado en `milpa/`**: `grep` devuelve 0 en los dos YAML; sólo vive en `data/cruce-ola6-v1_0.tsv` como necesidad. Y la propia ficha declara el límite: *«R2.3 sigue sin medirse de forma estricta»*. | **evidencia disponible, sin enlace** |
| **SHED** (`#745`, `data/shed2025-bnpl-dano/ficha-uso-extranjero.md`) | uso/atraso/cargo BNPL, **Estados Unidos**, SHED 2025 | **ninguno, y por doble motivo.** No hay consumidor; y aunque lo hubiera, la ficha declara `Uso prohibido: transportar tasas a México… o adoptar un parámetro del motor`. | **evidencia disponible, sin enlace; límite extranjero intacto** |

**Cero enlaces decorativos escritos.** `milpa/tramite.yaml` y
`milpa/tramite-ola5-propuesta-v0.yaml` quedan **sin una sola línea tocada**
(`git diff --numstat milpa/` → vacío). `NC-0164` y `NC-0166` conservan sus
vías; este acto no las cierra ni las toca. La pregunta para mesa queda en
`NC-0186`.

Un matiz que se declara porque cambia la lectura: que las tres fichas no
tengan consumidor **no es un defecto de las fichas**. Las tres se midieron
para contestar necesidades del catálogo (`N34` daño crediticio, `N35`
valoración de seguridad social) que todavía no tienen regla en el motor.
Enlazarlas ahora exigiría inventar el consumidor, que es exactamente lo que
el patrón de la casa reserva a mesa.

---

## P4 · El ruteo del manifiesto ENNViH — **letra pura, ejecutada**

### 4.1 · La fila que este acto LEE (no la inventa desde el encargo)

`forense/notas/2026-09-14-GEN2-DISENO-FASE1-CIERRE-cierre.md:23`, verbatim:

> **Premisa «los payloads de ambas EXISTEN en el manifiesto»:** cierta para
> EDER (`eder_2017_eder2017_bases_csv`, sha coincide con la raíz), **falsa en
> la letra** para ENNViH (`manifiesto.yaml` sigue sin `id:` para
> `ehh05*.zip`; hallazgo preexistente de fase 1 y de `CORR-0008`). No
> bloquea: ENNViH no se abre.

### 4.2 · La discrepancia exacta: id asentado vs realidad

**Id asentado** (`data/manifiesto.yaml`, entrada `ennvih_mxfls_licencia`,
30/jul/2026), verbatim de la frase en disputa:

> No cambia el estado del payload: ningún archivo de ENNViH se ha descargado
> ni se registra aquí -- CAL-G3 sigue sin ejecutarse.

**Realidad, derivada del mismo archivo:**

```
$ python3 -c "import yaml; d=yaml.safe_load(open('data/manifiesto.yaml')); ..."
ennvih_mxfls_licencia               | (sin archivo)                | SIN-SHA
ennvih2_2005_hogar_dta              | ennvih/ehh05dta_all.zip      | fc4ea4ae7d0c | 20198874
ennvih2_2005_hogar_cb               | ennvih/ehh05cb_all.zip       | 1bbbb7ee97bd |  1184711
ennvih2_2005_hogar_q                | ennvih/ehh05q_all.zip        | e73709d1de16 |  2913036
ennvih2_2005_ponderador_transversal | ennvih/ehh05w_all.zip        | 34ee12b0c0d7 |   759009
ennvih2_2005_ponderador_longitudinal| ennvih/ehh05lw_all.zip       | 6567bcbf3386 |   698559
  ... (28 entradas ENNViH en total: olas 1, 2 y 3 + ennvih1_muestra_diseno)
```

**Las dos afirmaciones son falsas en la letra a la vez, y en direcciones
opuestas:** (a) la del manifiesto («ningún archivo … se registra aquí»), y
(b) la del `#760` («sigue sin `id:` para `ehh05*.zip`») — los cinco
`ehh05*.zip` **sí tienen `id`**, desde `PR #703` (`2bd228c`), verificado por
`git log -L 623,640:data/manifiesto.yaml`. Es decir: el `#760` escribió una
premisa correcta en el espíritu (el manifiesto **se contradice** sobre
ENNViH) y equivocada en el dato (dijo que faltaba el `id`, cuando lo que
sobra es la frase vieja).

### 4.3 · El ruteo, decidido por la evidencia

**No exige bytes.** El criterio del encargo es explícito: bytes si la
reconciliación necesita el hash del payload real. Aquí **no se necesita
ningún hash**: los `sha256` y `tamano_bytes` de las 28 entradas **ya están
escritos en el repo** desde `PR #703`; lo que está mal es una **frase**, y se
verifica contra el mismo archivo que la contiene. **Rama de letra pura →
ejecutada aquí.** Ningún byte se hasheó desde NUBE.

### 4.4 · Antes / después (`data/manifiesto.yaml`, `ennvih_mxfls_licencia`)

**Antes** — la entrada terminaba así:

```yaml
    de ENNViH como "reporta el valor" (sin verificar en esa sesión). No cambia el estado del
    payload: ningún archivo de ENNViH se ha descargado ni se registra aquí -- CAL-G3 sigue
    sin ejecutarse.
```

**Después** — la frase vieja **queda como registro y no se reescribe**
(regla de la casa), y debajo entra la corrección fechada:

```yaml
    de ENNViH como "reporta el valor" (sin verificar en esa sesión). No cambia el estado del
    payload: ningún archivo de ENNViH se ha descargado ni se registra aquí -- CAL-G3 sigue
    sin ejecutarse.
    CORRECCIÓN DE LETRA FECHADA (15/sep/2026, ACTO GEN2-ADOPCION-VENTANILLA-2, P4).
    La frase anterior queda como registro y NO se reescribe: era cierta el 30/jul/2026
    y es FALSA EN LA LETRA desde PR #703 (commit 2bd228c). Este mismo archivo registra
    hoy 28 payloads de ENNViH con id, archivo, sha256 y tamano_bytes -- entre ellos los
    cinco ehh05*.zip de la ola 2 que el ACTO GEN2-DISENO-FASE1-CIERRE (PR #760) abrió
    por cabecera: ennvih2_2005_hogar_dta (...), ennvih2_2005_hogar_cb (...),
    ennvih2_2005_hogar_q (...), ennvih2_2005_ponderador_transversal (... de donde sale
    fac_3b) y ennvih2_2005_ponderador_longitudinal (...); más las olas 1 y 3 y
    ennvih1_muestra_diseno. Corrige la premisa citada en
    forense/notas/2026-09-14-GEN2-DISENO-FASE1-CIERRE-cierre.md:23 (...): los id SÍ existen.
    ... Lo que NO cambia: ENNViH ola 2 sigue EXISTE-NO-SATISFACE por falta de
    estrato/UPM públicos (NC-0156), y la copia de esta misma frase falsa que vive en
    data/corrida0/demanda-corridas.tsv (fila CORR-0008) NO se toca desde aquí -- queda
    en NC-0185.
```

(El bloque completo, con los `sha256` largos, está en el archivo; aquí se
elide sólo el hash para que la nota sea legible.)

**Verificación del cambio:**

```
$ git diff --numstat data/manifiesto.yaml
19  0  data/manifiesto.yaml          <-- 19 líneas añadidas, 0 borradas
$ python3 -c "import yaml; print(len(yaml.safe_load(open('data/manifiesto.yaml'))))"
1608                                  <-- idéntico a antes
$ python3 tests/manifiesto.py --verifica ; echo exit=$?
exit=0                                <-- sin hashes movidos; los AUSENTE son data/raw en NUBE
```

**Lo que este acto NO hizo en P4:** no tocó ningún `sha256`, no abrió ningún
`.zip`, no corrió `--registra` ni `--promueve`, y **no corrigió** la copia de
la misma frase que vive en `data/corrida0/demanda-corridas.tsv` (fila
`CORR-0008`) y en su eco de `RES-0029`/`RES-0030`: ese archivo **no está en
el perímetro** que el encargo acota para P4 (*«`data/manifiesto.yaml` SOLO
bajo la rama de letra-pura»*). Queda en **`NC-0185`** con el paso exacto.

---

## Suite, antes y después

```
$ python3 tests/check.py     # línea base, antes de tocar nada
3 FAIL · 3656 WARN           # T06 (2) · T08 (1) -- las tres preexistentes en main

$ python3 tests/check.py     # con todos los cambios de este acto
3 FAIL · 3659 WARN           # T06 (2) · T08 (1) -- las MISMAS tres; T15 T-ADR-COUNT [ok]
```

**Cero fallas nuevas.** El delta de `+3 WARN` es exactamente `T34
T-NO-CORRIDO`, que emite un `warn` por fila `ABIERTA`: 66 → 69, las tres que
este acto abre. Intermedio declarado, no escondido: `T15 T-ADR-COUNT` **sí
falló** en la corrida previa al cerrar la cascada (`«cita 502 ADR; gobernanza
tiene 503 únicos»`, 3 fallas en `estado-programa-v1_13.md:79`, `:163` y
`gobernanza-v1_15.md:2`); es el paso de cascada que faltaba —los tres
encabezados de conteo— y se corrigió en la misma sesión, con la suite
re-corrida hasta verlo `[ok]`.

## Perímetro cumplido

Toca: `forense/encargos/2026-09-15-GEN2-ADOPCION-VENTANILLA-2.md` (0-bis) ·
`forense/notas/` (esta nota) · `forense/no-corrido.tsv` (append de
`NC-0185`/`NC-0186`/`NC-0187`) · `data/manifiesto.yaml` (rama letra-pura de
P4, única entrada) · `canon/gobernanza-v1_15.md` (ADR de cierre) ·
`canon/estado-programa-v1_13.md` (§L0) · `canon/registro-rotulos.tsv`.

**No toca:** `milpa/*.yaml` (cero adopciones ejecutadas ⇒ cero citas nuevas)
· `data/corrida0/decisiones.tsv` · ningún TSV derivado (nada que re-derivar:
`status` idéntico salvo `no_corrido_abiertas`) · ningún `CALC` sellado ·
`data/corrida0/demanda-corridas.tsv` (`NC-0185`).

Pisadas con `VERIFICACION-CAJA-2`: **cero** — verificado por archivo.

## Contador

**No mide.** Cero adopciones, cero enlaces, cero mediciones, cero firmas FP,
ningún brazo del duelo tocado, ningún complemento vetado adoptado. Lo que
mueve: sus propios registros (`NC-0185`/`NC-0186`/`NC-0187`), una corrección
de **letra** en una entrada de licencia de `data/manifiesto.yaml`, y la
cascada. `N_resultados_gen2_adoptados_activos` **16 → 16**;
`N_resultados_gen2_pendientes_adopcion` **5 → 5**;
`dependencias_numericas_legacy_activas` **191 → 191**; `no_corrido_abiertas`
**66 → 69**.

## CONSUMIDO · PR #762

`https://github.com/Josanoforo/Modelado-Mexicano/pull/762`. La adopción por
lote es firma de mesa **POR MERGE**; lo que este acto dejó como
`DECISIÓN-DE-MESA` (los tres `CTX-*`, el paquete EDER de `NC-0183`, las
fichas de `NC-0186`, el destino de `B-MARCO` en `NC-0187`) **no** se sella
con este merge: se propone, y espera firma distinta.
