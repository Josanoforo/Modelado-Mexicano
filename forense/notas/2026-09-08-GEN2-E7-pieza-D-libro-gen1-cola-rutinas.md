# `ACTO GEN2-E7 · READINESS-2` pieza D — nota de cierre

8 de septiembre de 2026 · entorno **NUBE, sin corpus ni red** · `ADR-398`
(segunda pasada, mismo rótulo) · rama
`claude/nube-e7-readiness-gen2-873cj3`, la misma de las piezas A y B.

Enmienda de dirección del mismo día, redactada contra
`origin/main = 9a950c92` más la rama de la pieza C (`PR #612`). La
enmienda dice *«piezas A y B aún no lanzadas»*; para cuando llegó ya
estaban ejecutadas y commiteadas en esta rama, así que la pieza D va
**en la misma rama**, que es la opción que la propia enmienda deja
abierta («misma rama que A/B o PR propio si A/B ya arrancó»).

---

## 1 · Las dos decisiones que gobiernan la pieza

**`D13` — no hay retrofit 2.** Los encargos GEN1 sin marca no se
clasifican uno por uno. Firma de mesa, verbatim: *«Realmente queremos
comenzar a revolver Gen1 vs Gen2? siento que eso estaríamos haciendo con
el retrofit»*.

**`D14` — no se crean rutinas nuevas.** Se ajustan las tres que existen.
Firma: *«revisemos actualizar de una vez estas rutinas, ajustarlas o
crear nuevas que valgan la pena»*.

---

## 2 · D1 · El libro GEN1, cerrado

`tools/cierra_libro_gen1.py` — nuevo, **de un uso**, idempotente.

```
$ python3 tools/cierra_libro_gen1.py --aplica
forense/encargos/*.md examinados: 374 (A.13)
  EXCLUIDO     314
  ROTULA       60

  de los ROTULA: 53 «sin PR que lo cite» · 7 «⚠️ NO MARCAR»

APLICADO: 60 encargo(s) rotulados HISTÓRICO-GEN1.

$ python3 tools/cierra_libro_gen1.py          # idempotencia
  EXCLUIDO     314
  YA-ROTULADO  60
```

Cuatro condiciones para rotular, y las cuatro se declaran por archivo:
prefijo de fecha · sin encabezado `## CONSUMIDO`/`## SUSTITUIDO`/
`## HISTÓRICO` · fechado **antes** del cierre de GEN1 · **no citado por
ningún `NC-` ABIERTA** (un encargo con deuda viva asentada no es historia
todavía).

### 2-bis · Dos cifras reconciliadas, no copiadas

La enmienda declara **62** sin marca (48 + 13 + 1). Medido:

| | |
|---|---|
| sin marca por el criterio del digesto (sólo `## CONSUMIDO`) | **62** ✓ coincide |
| de esos, rotulables por `D1` | **60** |
| diferencia | **2**, y ambos explicados |

Los dos son `2026-09-03-MAESTRA37-L2-MPS-CODEBOOK-Y-P3.md` (ya trae
`## HISTÓRICO`) y `2026-09-04-MAESTRA38-V1-CORROBORA-Y-RECONCILIA.md` (ya
trae `## SUSTITUIDO`). `D1` los excluye **explícitamente** — *«Los
SUSTITUIDO existentes no se tocan»*. El desglose también difiere: medido
**53 + 7**, declarado **48 + 13**. Se reporta el medido.

**Consecuencia en el digesto.** §D deja de listar lo rotulado y lo cuenta
en una línea. Y como esos dos **sí** tienen marca de cierre —sólo que no
`## CONSUMIDO`—, llamarlos «sin marca» era una inexactitud medida: se
cuentan aparte, con su nombre. Resultado:

```
Con marca: 310. Sin marca: 0.
`HISTÓRICO-GEN1`: 60 — ... No se listan ...
Con otra marca de cierre (`## SUSTITUIDO` / `## HISTÓRICO`): 2 — ...
```

**`encargos_sin_marca`: 62 → 0.**

---

## 3 · D2 · La cola, y el tick que no llegó a ocurrir

El defecto, **medido** el 8/sep: cinco encargos GEN2 ya fusionados
seguían abiertos en la cola.

| encargo | ESTADO en cola | PR real (verificado) |
|---|---|---|
| `GEN2-E1-LIMPIEZA-C1` | `LISTO-CAJA` | `#602` |
| `GEN2-E2-C0-A-DEMANDA` | `GATEADO` | `#600` |
| `GEN2-E3-AUTOMATIZA-GEN2-1` | `GATEADO` | `#601` |
| `GEN2-E4-LIMPIEZA-C2-PODA` | `GATEADO` | `#604` |
| `GEN2-E6-AUTOMATIZA-GEN2-2` | **`LISTO-NUBE`** | `#611` |

Los cinco PR se verificaron **contra el historial de merges**
(`git log origin/main --grep="pull request #N"`), no se copiaron de la
enmienda. `#612` todavía no aparece: la pieza C sigue en vuelo, que es
consistente con lo que la enmienda dice.

**El último de la tabla es el que importa.** `/despacha` toma el
`LISTO-NUBE` **más antiguo**. `GEN2-E6` lo era. En su siguiente tick, el
despachador habría vuelto a ejecutar un acto ya fusionado, entero, sin
más candado que la memoria de quien mirara.

### 3-bis · La corrección de diseño

El homónimo se empareja **por RÓTULO** —el nombre sin el prefijo
`AAAA-MM-DD-`—, no por basename:

```
cola/2026-09-07-GEN2-E6-AUTOMATIZA-GEN2-2.md
     2026-09-08-GEN2-E6-AUTOMATIZA-GEN2-2.md   ← archivado
          ↑ la cola lleva la fecha de REDACCIÓN, el archivado la de EJECUCIÓN
```

Emparejar por nombre completo habría producido **un sincronizador que no
dispara nunca y un verde que no significa nada**. Falsado: revertí el
`ESTADO:` de `GEN2-E6` a `LISTO-NUBE` y el detector lo encontró y nombró su
PR; restauré.

Una sola función —`cierre_acto.cola_desincronizada`— la consumen los
tres: el reconciliador (`--aplica`), el test de la suite y la skill. No
pueden discrepar sobre qué cuenta como desincronizado.

**Colisión de numeración, declarada.** La enmienda pide el test como
`T36`. `T36` ya lo tomó `T-CORREDORES-GEN2`, de la **pieza A de este
mismo acto**. El test entra como **`T37`**; renumerar el de la pieza A
habría sido peor, porque va en el mismo PR.

---

## 4 · D3 / D4 / D5 · Las tres rutinas

**`/despacha`** — bloques nuevos **2-ter** (no tomar un `LISTO-*` cuyo
homónimo archivado ya trae `## CONSUMIDO`; corregir el `ESTADO:` en
commit propio y seguir), **2-quater** (evaluar la compuerta de los
`GATEADO` y **promover** si pasa contra `origin/main` — nunca al revés,
nunca a mano) y **7** (huella en `forense/rutinas.tsv`, en los **cuatro**
desenlaces, en la rama del día). Perímetro propio: dos rutas → tres.

**`/revisa`** — disparador «al abrir PR» además del diario; `--post-hoc`
en **PR propio** `[REVISA]` con sólo la nota, sobre **rama propia**. El
guardrail 2 se conserva verbatim y **este modo no lo relaja: lo
satisface** —la rama del `[REVISA]` es nueva y sale de `origin/main`; la
revisada no recibe un byte—. Punto **2.11** nuevo, peso `BLOQUEA`:
cotejar `## NO-CORRIDO / RESERVAS` contra el diff y contra el encargo.
Con la salvedad declarada del **encargo de dos entornos**: una pieza de
caja ausente del PR de nube no bloquea —bloquear ahí sería exigirle a un
PR el trabajo que su encargo mandó a otra máquina—. «Diez puntos» → once,
en las seis menciones.

**`/tramite` y el digesto** — sección **I** «Rutinas (últimos 7 días)» y
sección **J** «Revisiones». Dos decisiones de honestidad en ellas:

- Una rutina **sin líneas** en la ventana se reporta **`SIN HUELLA`**,
  no «sana y ociosa». Es lo que de verdad se midió: *no se midió que
  corriera; no se afirma que no corriera*.
- `J` declara derivar **huellas** (notas `*revisa*.md` + ramas
  `claude/revisa-*`) y **no** el conjunto de PR, porque `gh` no existe en
  este entorno. Un `/revisa` en línea deja su veredicto como comentario
  de GitHub y no deja huella en el árbol.

`forense/rutinas.tsv` nace con su formato documentado en la cabecera y
una línea de ejemplo declarada como tal, para que la primera rutina que
corra tenga un formato que copiar en vez de uno que inventar.

---

## 5 · D6 · El lock, y por qué protegía lo que no hacía falta

Antes, el lock del manifiesto era siempre `<root>/data/.manifiesto.lock`,
con `root` = el árbol desde el que se invoca. **`git worktree add`
produce un `data/` propio**, así que dos actos en dos worktrees del mismo
clon tomaban locks **distintos** y no se veían.

Dicho de frente: el lock protegía contra el escritor con el que ya se
compartía todo, y **no** contra el único del que había algo que proteger.
Es la puerta del defecto `ACTO R` / `ACTO R″` (`FP-345`, hallazgo de la
pieza C).

Desde aquí se resuelve a la **raíz de escritura compartida**
(`descargas_mx` de `data/raices.local.yaml`, gitignorado — la ruta real
nunca se commitea), común a todos los worktrees de una máquina. El
fallback es **declarado, no silencioso**:

```
$ python3 -c "...aviso_lock_manifiesto(...)"
lock: /home/user/Modelado-Mexicano/data/.manifiesto.lock (ambito POR-ARBOL:
'descargas_mx' no esta en data/raices.local.yaml, asi que el lock NO cubre
otros worktrees del mismo clon)
```

Un lock por árbol sigue siendo correcto cuando hay un solo árbol. Lo que
no puede pasar es que el caso degradado se parezca al bueno.

---

## 6 · D4(d) · Las reservas de `#597`

Asentadas en `forense/hallazgos.md` como **una línea**, no como `NC-`.
Un `NC-` es una pieza **de este programa** que alguien va a correr; éstas
son observaciones sobre un acto histórico cuyo producto **GEN2 no
reutiliza** — `CALC-M` re-emite desde el motor, `CALC-AGG` re-agrega
desde `RESULT-*`, y ninguno lee `corridas-M/` ni
`agregado-v1_3-resultado.json` (verificado por audithook en la pieza A).

**Corrección de cifra.** La enmienda las llama «las cuatro de #597». El
cuerpo del PR lista **seis** bajo `## Reservas materiales`. Se asientan
las seis, diciendo cuáles quedan sin efecto para GEN2 —(1) orden de
lectura del §11, (3) `tra_m_02_informativo`, (4) `n_celdas` del
bootstrap— y cuáles siguen vivas y son de mesa —(2) el mismo defecto de
calibración en `con_registro / paga_mordida`, (5) el PARO
`CalibracionAmbigua` sin documentar, (6) la cadena `ADR-270`/`ADR-276`
que `ADR-270` no sostiene—.

---

## 7 · Lo que la pieza D NO pudo hacer — `NC-0018`

Tres incisos dependen de artefactos que viven en la **pieza C**
(`PR #612`, **no fusionado**) y **no existen en este árbol**:

| pedido | por qué no |
|---|---|
| `FP-345` → `FIRMADA` | el máximo de `forense/firmas-pendientes.tsv` aquí es **`FP-343`** |
| `FP-344` (cablear `test_alta_relacion.py`) | `tests/test_alta_relacion.py` **no existe** aquí |
| `NC-0016` → `CERRADA` | **el `NC-0016` de este árbol no es el de la enmienda** |

El tercero es el que más importa. La enmienda se redactó contra
`origin/main` + la rama de la pieza C, **antes** de que la pieza A de
este mismo acto añadiera `NC-0015`/`NC-0016`/`NC-0017`. Aquí `NC-0016` es
la fila del **corredor L** (las 224 corridas no ejercidas). Cerrarla
habría escrito una falsedad sobre una fila ajena; firmar dos `FP`
inexistentes, otra.

**Por tanto el contador de la enmienda no se cumple en dos renglones, y
se declara:** `no_corrido_abiertas` **no** baja −1 y `fp_abiertas`
**no** baja −2 con esta pieza.

Lo que sí se hizo del inciso `D6` es su **cambio de fondo** —la ruta del
lock—, que no depende de la pieza C.

`NC-0018` lleva la instrucción exacta para el sucesor, incluida la
advertencia de **identificar la fila de la pieza C por su TEXTO**
(`PARO-PREMISA` con sucesor `FP-344`) y **no por su número**, porque la
numeración se corrió.

---

## 8 · Contador y suite

**Cero mediciones.** Ninguna cifra del modelo se movió: se cerró un
libro, se sincronizó una cola, se ajustaron tres rutinas y se corrigió
dónde vive un archivo de lock.

| contador | declarado por la enmienda | real |
|---|---|---|
| `encargos_sin_marca` | 62 → 0 | **62 → 0** ✓ |
| `no_corrido_abiertas` | −1 | **sin cambio** (`NC-0018` explica) |
| `fp_abiertas` | −2 | **sin cambio** (`NC-0018` explica) |

```
tests/check.py --baseline
  3 FAIL · 188 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

Los 3 `FAIL` son de la línea base congelada. **Un `FAIL` nuevo apareció
durante la pieza D y se corrigió**: la nota de cierre de las piezas A/B,
al *describir* el hallazgo de `T25` del propio acto, volvió a escribir el
rótulo pelado que el hallazgo denunciaba. Se reformuló sin nombrarlo — y
la frase que lo reformula lo dice, porque el tropiezo es la mejor prueba
de que el test sirve.

### Defecto preexistente, medido y no causado por esta pieza

`tools/digesto_tramite.py` no puede emitir el digesto hoy:

```
PARO — la neutralización no fue completa; el digesto NO se escribe:
  · T25: rótulo pelado `_E7` sobrevivió a la neutralización
```

*(El rótulo de esa línea va aquí con un `_` delante — la misma
neutralización que el propio digesto aplica al copiar texto del árbol.
Escribirlo pelado haría fallar `T25` sobre esta nota exactamente igual
que sobre el digesto, que es el defecto que la línea describe.)*

Comprobado con `git stash`: **falla idéntico en `HEAD` antes de esta
pieza**. No lo causé y no lo arreglo — el cuerpo de los encargos está
fuera del perímetro de `D`. Las secciones `I` y `J` nuevas se verificaron
llamando `seccion_i()` / `seccion_j()` directamente, y sus salidas están
en §4. Queda dicho para que nadie lea el `PARO` como consecuencia de esta
pieza.
