# E5-0 · ACTO GEN2-E5-0 · SPECS EJECUTABLES

- **SHA de redacción (base del encargo):** `df9336c5` (reencolado por `ACTO GEN2-V213`, 8/sep/2026). **SHA de ejecución:** `origin/main = d8b5f0b` (113 commits después; `df9336c5` es ancestro — verificado con `git merge-base --is-ancestor`, main avanzó, no divergió).
- **Entorno asignado:** UBUNTU (caja), worktree nuevo desde `origin/main`, Opus. **NO se lanza en NUBE** (lo dice el propio cuerpo).
- **Estado:** VIVO.


## E5-0 · ACTO GEN2-E5-0 · SPECS EJECUTABLES — códigos y ponderadores desde metadato; congelar `spec.yaml`

Cabecera: **UBUNTU (caja)**, worktree nuevo desde `origin/main` · **Opus** · COMPUERTA por producto: E7 fusionado con `GO-MARCADOR` en su nota (`git show origin/main:forense/notas/<nota-E7> | grep -c GO-MARCADOR` ≥ 1); `python3 tools/limpia_arbol.py --reporta` sin árboles ni ramas fuera de política; gates de spec en `main`: S12 `870522a3…`, S13 `c41235b8…`, S6 v1.2 `c1cd3b63…` (íntegros del sidecar). NO se lanza en NUBE.
Principio (E.5 de v2.13): «spec conceptual pre-registrada → abrir **solo** codebook/metadato → resolver códigos y ponderador → congelar `spec.yaml` → COMMIT-1 → (E5) abrir microdato → calcular». **Termina en el COMMIT-1; no abre microdato ni calcula.** Adivinar códigos para lograr un `preflight` VERDE está prohibido.
**CALC-0001 / S12 (CIDE-CSES 2015).** Codebook y metadatos del `.sav` (etiquetas y códigos, sin valores): `pcyc13`, `pcyc14`, `pvoto1/2/3`, desenlace §2, ponderador. Si el desenlace no existe con esos códigos → `NO-CONSTRUIBLE` declarado (outputs `null` solo en ese brazo). `spec.yaml` (D-15), `spec-check` y `preflight` VERDE, COMMIT-1.
**CALC-0002 / S13 (LAPOP 2019/2021/2023, R10.3).** **No se convierte ausencia de desenlace en veredicto D2-h.** (a) Confirmar en los codebooks de las tres olas si existe desenlace comparable al de la corrida 2004 (leer en la nota de LOTE-LAPOP cuál usó); (b) si existe: escribir **S13 v1.1** (md + sidecar, antes de cualquier microdato) y `spec.yaml` contra v1.1; (c) si no: `spec.yaml` contra v1.0 con `veredicto_D2h: NO-CONSTRUIBLE` y solo outputs descriptivos pre-registrados. Las dos rutas están autorizadas; el acto reporta cuál y por qué, con codebook citado.
**CALC-0003 / S6 v1.2 (ENNViH 2002).** Riesgo técnico: `seed {aplica: true, valor, rng}`, `dependencias_materiales: [zipfile-deflate64, …]`, `ponderador` por brazo (`fac_3b`; `fac_3b_px` y `fac_3a_px` en pareja), rutas de los ocho `.dta` por `resolver_payload`, ventanas de `es09`/`ce01` leídas de `ennvih1_2002_hogar_q` y citadas con página **en el yaml**, outputs con tipo/unidad y `NO-ESTIMABLE` permitido por celda. `spec-check` y `preflight` VERDE, COMMIT-1.
Común: un COMMIT-1 por CALC con «el primer resultado que produzca este procedimiento es el que se reporta»; sidecars; nota con codebooks abiertos (id de manifiesto, página) y **ningún número**. Cierre A.14; rama fusionada o borrada.
Perímetro: `data/corrida0/CALC-000{1,2,3}/spec.yaml` (+ `spec.md` local citando la spec sellada) · `forense/prereg-caja/S13-R10-3-spec-v1_1.md` + sidecar (solo ruta b) · `forense/notas/` (1) · `forense/firmas-pendientes.tsv` (recibo) · cascada. **No toca microdato, `tramite.yaml`, canon ni S12/S6.** Si te encuentras escribiendo fuera de esta lista, PARA.
Contador: cero; tres CALC en `PRE-FLIGHT-VERDE`.

---

## A.8 · `ya_medido.py` sobre las reglas que este acto pre-registra

```
$ python3 tools/ya_medido.py R10.3
=== ya_medido: R10.3 ===
  resuelto por canon: R10.3 -> id `comunicacion.inseguridad.ver_oir_callar`
                      (canon/modelo-decision-v4_0.md §3, tag **id:**)
  ...
========================================
MEDIDA-EN: L18
```

`R10.3` **ya está medida** (`ACTO MAESTRA38-L18`, `veredicto_Bbis = NO-DISCRIMINA`
sobre LAPOP 2004; la pieza está `SELLADA-SIN-CARGA`). Este acto **no la re-mide, no
la reclasifica y no la mueve de tier**: congela la cara mecánica (`spec.yaml`) de una
spec ya sellada, y su `CALC` declara `veredicto_D2h: NO-CONSTRUIBLE` precisamente
porque la segunda medición que `D2-h` pide no tiene ola que la dispare.

`ya_medido.py` sobre las piezas gemelas de `S12`/`S6` devuelve lo que esas specs ya
citan (`civico.clientelismo…_lapop2019` y `salud.atencion.grave_ennvih2002`, esta
última en `NO-ESTIMABLE-EN-v1_1`), todas `SELLADA-SIN-CARGA`. Ninguna se toca.

## NO-CORRIDO / RESERVAS

`PR` de este acto: ver `## CONSUMIDO`. Nota del acto:
`forense/notas/2026-09-08-codebooks-abiertos-y-specs-congeladas.md`.

| qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|
| «(b) si existe: escribir **S13 v1.1** (md + sidecar, antes de cualquier microdato) y `spec.yaml` contra v1.1» | `PARO-PREMISA` | La ruta (b) está condicionada a que exista desenlace comparable al de la corrida 2004, y **no existe en ninguna de las tres olas** — `aoj1` ausente, y 0 aciertos de `denunc\|report` sobre **678 variables con etiqueta en 3 archivos** (control positivo: 221/221, 262/262, 195/195). Se tomó la **ruta (c)**, que el encargo autoriza igual. `R10.3` no gana segunda medición; `veredicto_D2h` queda `NO-CONSTRUIBLE` y `D2-h` sigue sin ola que la dispare. Ningún tier se mueve | Camino A de `S13 §0.2` (desenlace sustituto con variable nombrada) — **requiere mandato de mesa, no de ejecutor** — `NC-0039` |
| «`spec-check` y `preflight` VERDE» — el `medidor.py` que ese VERDE exige | `NO-VERIFICABLE-AQUÍ` | Los tres `medidor.py` se **escribieron** en este acto y **no se ejecutaron**: el encargo prohíbe abrir microdato. `PRE-FLIGHT: VERDE` certifica la **declaración** (esquema, identidad de inputs, árbol limpio), **no** la corrección numérica del medidor. Lo que sí se verificó, con fixture **sintético** en memoria y sin tocar payload: que el juego de claves de `medir()` **coincide exacto** con los ids declarados (54 · 29 · 128) y que los tipos casan | `ACTO GEN2-E5` — su corrida es la primera ejecución real de los tres — `NC-0038` |
| Perímetro: «`data/corrida0/CALC-000{1,2,3}/spec.yaml` (+ `spec.md` local…)» | `DECISIÓN-DE-MESA-PENDIENTE` | Se escribió además `medidor.py` en cada uno de los tres directorios — **dentro** del directorio que el perímetro nombra, y **obligado por el propio encargo**: `preflight` bloquea con `script_ausente` si el script no existe, así que «`preflight` VERDE» (exigido tres veces, y puesto como contador: «tres CALC en `PRE-FLIGHT-VERDE`») es inalcanzable sin él. Se declara en vez de absorberse | mesa, en el merge: si el medidor no debía escribirse aquí, el contador del encargo no era alcanzable y hay que reescribir uno de los dos |
| COMPUERTA, tercer limbo: «`python3 tools/limpia_arbol.py --reporta` **sin árboles ni ramas fuera de política**» | `NO-VERIFICABLE-AQUÍ` | **No se cumple y no se puede cumplir desde el ejecutor.** El reporte da ramas remotas sin PR abierto (`fuera_de_politica`), todas **ajenas a esta sesión**, y `/acto` §1.0.d prohíbe expresamente decidir su borrado desde aquí (`--aplica` es `E4`/Fase IV, hoy sale con código 2). Los otros dos limbos —`GO-MARCADOR` de E7 y las tres specs íntegras— **sí se verificaron por producto**. Ver la `BITACORA` de la cola para el detalle re-derivado | mesa: o `E4`/Fase IV limpia el remoto, o el limbo se reescribe acotado a las ramas del propio acto — `SIN-ASIGNAR` |

**Contador declarado vs. medido.** El encargo dice «Contador: cero; tres CALC en
`PRE-FLIGHT-VERDE`». Los tres **están** en `PRE-FLIGHT: VERDE` y el contador GEN2 no
se mueve (ningún número del modelo se produjo). `no_corrido_abiertas`: **−1 por el
cierre de `NC-0011`** (el endurecimiento de `preflight` nunca probado contra specs
reales: esta es esa prueba) **+2 por las reservas de arriba** — neto **+1**. La
diferencia se declara, no se absorbe.

**Reservas que NO son filas `NC-` porque son deuda medida, no deuda no corrida** —
van a `forense/firmas-pendientes.tsv`: `FP-349` (`S6 §1` congela `es09 == 0` y el
código `0` no existe: «No» es `3`; corrida verbatim, las seis filas salían
degeneradas), `FP-350` (el desenlace que `S12 §2` dio por no construible existe:
`peledip`, más tres correcciones de premisa), `FP-351` (`S6 §3.5` dice que la
localidad no está en los archivos y sí está, en `c_portad`), `FP-352` (`preflight`
da `BLOQUEADO` falso dentro del sandbox para toda raíz `descargas_mx`).

## CONSUMIDO

`PR #629` — `ACTO GEN2-E5-0 · SPECS EJECUTABLES`, 8/sep/2026, entorno **UBUNTU
(caja)**, rama `acto/gen2-e5-0-specs-ejecutables`, `ADR-408` (renumerado de `407`
al fusionar `origin/main`: `ACTO GEN2-TRAMITE-FIRMAS-1` fusionó primero por
`PR #627`).

Ejecutado: `spec.yaml` congelado para `CALC-0001` (`prereg-caja-S12`),
`CALC-0002` (`prereg-caja-S13`, **ruta (c)**) y `CALC-0003` (`prereg-caja-S6-L16`
v1.2), cada uno con su `spec.md` local, su `medidor.py` y su `COMMIT-1` con la
frase de sello. Abierto **sólo** codebook y metadato; **no se abrió microdato y no
se calculó**. `spec-check`: 117 pares, **0 FAIL**. `preflight`: **VERDE los tres**.
`NC-0011` **CERRADA**. Reservas: `NC-0038`, `NC-0039`. Firmas abiertas a mesa:
`FP-349`, `FP-350`, `FP-351`, `FP-352`.
