# ACTO MAESTRA38-L16-BIS-2 · COMMIT-2 · resultados · Rama A de `salud.atencion.grave` (`R4.4`) contra `prereg-caja-S6-L16` v1.1

**Fecha:** 7 de septiembre de 2026. **Entorno:** UBUNTU (caja, corpus montado). **Base:** `origin/main` = `3d6dee33`.
**Spec consumida:** `prereg-caja-S6-L16` **v1.1**, sha256 `7a0120a3a471fe81a732035dec6c2a9ed292d9b722cc408248eaec96d2e6643a` — compuerta verificada por producto contra `origin/main`, no por rótulo.
**COMMIT-1** (spec citada antes de abrir un solo `.dta`): `forense/notas/2026-09-07-MAESTRA38-L16-BIS-2-spec-congelada.md`.
**Resultado maquinable:** `data/l16bis2-atencion-grave-rama-a-v1_0.json`.

---

## Veredicto

> **Rama A (`ENNVIH` 2002) — `NO-ESTIMABLE`.** Es exactamente la fila que `§4` pre-registró como *"la fila que `B-bis` exige"*, y se dispara por **dos causas independientes**, cualquiera de las cuales bastaba por sí sola.

Los **dos brazos se reportan por separado y ninguno se agrupa ni se promedia** (`§1.3`, `A-bis 4`):

| brazo | archivo | `es09` etiqueta verbatim | `n` filas | `es09`=1 | ponderador prescrito | proporción ponderada | IC95 | veredicto |
|---|---|---|---|---|---|---|---|---|
| **`bx`** (Proxy, miembros ausentes) | `ehh02dta_all/ehh02dta_bx/p_es.dta` | «HA TENIDO PROBLEMA SALUD GRAVE» | 1 848 | 414 (no=1 419, NS/NC=15) | `fac_3b_px` | **no se declara** | **no se declara** | **`NO-ESTIMABLE`** |
| **`b3b`** (universo directo) | `ehh02dta_all/ehh02dta_b3b/iiib_es.dta` | «HA TENIDO PROBLEMA SERIO SALUD» | 19 804 | 3 972 (no=15 832) | `fac_3b` | **no se declara** | **no se declara** | **`NO-ESTIMABLE`** |

**Escala de reporte (`A-bis 3`): proporción ponderada.** No se declara ninguna — **no se construyó ninguna celda**. Los `n` de la tabla son el conteo bruto del disparador, no un estimando; se publican como diagnóstico, no como resultado.

---

## Disparador D1 — el CHEQUEO DE CONSISTENCIA de `§1.3` **FALLA**

`§1.3` prescribe correr el chequeo **antes de calcular una sola celda**, y que si falla **el proceso se PARA**. Se corrió el pseudocódigo de la spec, tal cual, sobre el subconjunto real:

- `p_es.dta` con `es09` no nulo → **1 524 folios distintos**; el join normalizado a entero contra `ehh02w_all/ehh02w_bx.dta` resuelve **7 467 filas** de ponderador (0 filas perdidas por el bug de `folio` cadena/`float64`: la normalización de `C1` se aplicó).

| candidato | `n_no_nulo_gt0` sobre el subconjunto `es09` no nulo | `n_no_nulo_gt0` sobre el libro `bx` completo (reproducido) |
|---|---|---|
| `fac_3a_px` | **5 128** | 21 631 |
| `fac_3b_px` | **5 103** | 21 645 |
| `fac_4_px` | 1 972 | 9 037 |

**El orden se invierte.** `fac_3b_px` (5 103) queda **25 observaciones por debajo** de `fac_3a_px` (5 128). El `assert` de `§1.3` se dispara con su propio mensaje: *"PARA: la asignación libro→factor es incorrecta"*.

**La spec lo anticipó y no se equivocó al anticiparlo.** `§1.3` escribió, antes de ver el dato: *"con margen estrecho contra `fac_3a_px` (14 observaciones de diferencia)... Si el subconjunto restringido a `es09` no nulo invierte el orden entre `fac_3b_px` y `fac_3a_px` (el margen de 14 es lo bastante estrecho para que eso sea posible), la asignación libro→factor es incorrecta y el proceso se PARA."* La columna del libro completo **reproduce exactamente** las tres cifras que `C1` midió y que `§1.3` heredó (21 631 / 21 645 / 9 037): el dato de `C1` es correcto; lo que no se sostiene es la **extrapolación** de ese margen de 14 al subconjunto que el falsador realmente usa.

Consecuencia ejecutada al pie: **no se calculó ninguna celda con `fac_3b_px`.** Re-adjudicar el ponderador con el subconjunto real es trabajo de un acto sucesor, no de éste — y no se sustituye `fac_3b_px` por `fac_3a_px` sobre la marcha: eso sería elegir el ponderador después de ver el dato, exactamente lo que el pre-registro existe para impedir.

## Disparador D2 — `BUSCA_PUBLICO` es `NO-CONSTRUIBLE-SIN-DIRECTORIO-EXTERNO`; caja **no** confirma `clave1`/`clave2`

`§3` dejó la puerta abierta: `NO-CONSTRUIBLE-SIN-DIRECTORIO-EXTERNO` *"salvo que caja confirme `clave1`/`clave2` (solo 2002) como suficiente"*. **Caja no lo confirma**, leído del descriptor del `.dta`, no del inventario:

- `clave1`/`clave2` existen en **8 archivos** de `ehh02dta_all.zip`. Sus etiquetas verbatim son **«ID CLINICA COMUNITARIO»** y **«ID PROVEEDOR SALUD COMUNITARIO»** (en `b3a/iiia_ed.dta` son de escuelas: «ID ESCUELA PRIMARIA/SECUNDARIA COMUNITARIO»). Son **llaves de entrada a un directorio comunitario externo**, no una clasificación público/privado. Sin ese directorio —que no está en el corpus— no clasifican nada.
- **Control positivo del barrido:** se recorrieron las etiquetas de todos los `.dta` de 2002 buscando `PUBLIC|PRIVAD|IMSS|ISSSTE|SSA|SEGURO SOCIAL|SECTOR`. El barrido **sí encuentra** aciertos —`iiib_ca.dta` `ca02a`/`ca02b`/`ca02e`/`ca02f` («TIENE SEGURO IMSS/ISSSTE/PRIVADO…»), `iiia_tb.dta` `tb33p_d-f`, `ii_nna1.dta` `nna20c/d`, `iiia_ed.dta` `ed241-244` («PRIMARIA PUBLICA/PRIVADA/ABIERTA»)—, así que no es un falso negativo del método. Pero **todos** son **stock de aseguramiento** o **tipo de escuela**: ninguno pregunta **a dónde acudió** tras el síntoma.

**El desenlace de `R4.4` no existe en `ENNVIH` 2002.** No hay contraste público vs. privado que medir sobre el antecedente `es09`.

---

## Qué se sigue de esto (`§5`, citado, no forzado)

`§5` de la spec: *"Si Rama A cae por `NO-ESTIMABLE` (§4, incluido el fallo del chequeo de consistencia de §1.3), `se_mueve_si` de la regla completa queda sin poder evaluarse con la Rama A — hallazgo a reportar, no a forzar; la Rama B, medida, ya no sostiene el `ENTONCES` de la regla por sí sola."*

Se reporta. **`R4.4` sigue sin una falsación que la sostenga:** la Rama B midió `NO-DISCRIMINA` (`ENSANUT2024`, `ACTO LOTE-ENSANUT`, PR #565) y la Rama A no llega a construirse. Los **dos** `EXISTE-SATISFACE` sellados que `§0.2` señaló como sin reconciliar siguen sin reconciliar, y ahora con un dato más: el linaje `ENNVIH` **no tiene el desenlace**. Eso es materia de mesa, no de este acto.

## Lo que este acto NO hizo

No re-corrió la Rama B. **No enmendó `S6` v1.1** — la cumplió al pie: el chequeo falla, el proceso PARA, y la spec ya traía la fila `NO-ESTIMABLE` para exactamente este desenlace. No sustituyó el ponderador. No movió tier ni cargó al motor. No abrió 2005 ni 2009. No corrió la corroboración `ENDIREH` (`§1.2`/`§4` la declaran no-sustituto del falsador; no cambia el veredicto). No promedió ramas ni brazos.

## Nota sobre la spec contra el dato (tercer commit, no corrección hacia atrás)

**La spec no resultó mal contra el dato.** Sus dos cifras heredadas de `C1` se reprodujeron exactas, su bug de join se confirmó y se evitó, y su cláusula de PARO capturó el caso real. Lo único que la spec no podía saber —y dijo que no podía saber— es de qué lado caería el margen de 14 sobre el subconjunto `es09`. Cayó del lado que la spec previó como posible. **No hay nada que corregir hacia atrás.**

## Sucesores declarados, no lanzados

- **`SELLO-3` (dirección + merge):** decisión de mesa sobre `salud.atencion.grave_ennvih2002` con el dato a la vista.
- Un acto sucesor que **re-adjudique el ponderador del libro `bx`** contra el subconjunto real (`es09` no nulo), no contra el libro completo — `fac_3a_px` lidera ahí por 25, pero adjudicar por ese solo criterio, después de ver el dato, requiere spec propia.
