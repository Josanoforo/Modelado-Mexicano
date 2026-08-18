# Nota del acto · T20-LLAVES — el vigía de "llaves de identificación ejercidas" nace en verde

18/ago/2026 · rama `claude/launcher-t20-llaves-wq28ec` · entorno NUBE, repo-only. Encargo: `forense/encargos/2026-08-18-T20-LLAVES.md`. Firma de origen: `FP-18` (`ADR-91`, `PR #246`, 17/ago — *"Incluyela."* sobre *"T20 se instrumenta en el primer acto que toque tests tras el cierre de BARRIDO-2."*).

## §0 · Verificación de existencia, re-derivada (A.8)

```
grep -oE "\"T[0-9]+[a-z]?\"" tests/check.py | sort -u   → T01..T23 ya ocupados (T19 partido en T19a/T19b/T19c)
```

`T20` ya existe en `tests/check.py` — es `T-CASCADA-MARCADA` (Encargo CU, 5/ago/2026), no libre. Mismo colisión declarada por el propio encargo como esperable ("re-deriva el número de marcador libre... misma receta que T21/T22/T23 ya usaron"). `T21`-`T23` también ocupados. Siguiente número libre: **`T24`**.

`python3 tests/check.py` al arrancar → `19 FAIL · 129 WARN`; `--baseline` → VERDE contra `997482bbda18b52621e24909eedbed0630c7a111`.

Contador citado por el encargo (`forense/registro-llaves-identificacion-v1_0.md`, §3/§5): **`1` de `2`** llaves ejercidas, movido por `ACTO ADJ-4` (13/ago/2026). Este acto no lo mueve — verificado, el acto solo instrumenta el vigía sobre el estado ya escrito.

## §1 · El marcador — `T24 · T-LLAVES-EJERCIDAS`

Deriva la cifra con la receta congelada del propio registro (§4 de `registro-llaves-identificacion-v1_0.md`): acota a `## 3 · Tabla de llaves`, extrae la columna `estado` (sexta tras dividir por `|`) de cada fila de datos, cuenta las que contienen la subcadena `EJERCIDA_` (no `startswith` — la primera versión del código sí usaba `startswith` y fallaba en falso: la celda trae la forma `` `EJERCIDA_INDECISA` `` con backtick líder, y `"`EJERCIDA_INDECISA`".startswith("EJERCIDA_")` es `False`; corregido a `"EJERCIDA_" in e`, que es exactamente la receta `grep -c 'EJERCIDA_'` original del archivo, sin anclar). `SELLADA_NO_EJERCIDA` no coincide — termina en `EJERCIDA` sin guion bajo posterior, verificado contra la propia advertencia del registro §4.

Cruza esa cifra contra la cita vigente de `canon/estado-programa-v1_10.md:99` (`"Llaves de identificación ejercidas: `N` de `M`."`) — mismo molde que `T19b`/`T19c` ya usan para sus propios contadores cruzados (cabecera vs. fuente). FAIL si difieren.

Corrida real, control positivo/negativo:

```
$ python3 tests/check.py 2>&1 | grep T24
  [ ok ]  T24 T-LLAVES-EJERCIDAS
```

Falsador probado en vivo durante la escritura: con `startswith` (bug), disparaba `FAIL` — `estado-programa` declara `1 de 2`, la receta (bug) derivaba `0 de 2`. Corregido, vuelve a `[ ok ]`. No se dejó el bug para "probar que el test prueba algo" — ya quedó demostrado por el propio ciclo rojo→verde durante la escritura, mismo criterio que T23 documentó para sus pruebas negativas sintéticas.

## §2 · Control C4 — línea base antes/después

```
antes:   python3 tests/check.py --baseline → 19 FAIL · 129 WARN, VERDE
después: python3 tests/check.py --baseline → 19 FAIL · 128 WARN, VERDE
```

La caída de un WARN **no es el marcador nuevo** (`T24` entra en `[ ok ]`, cero disparo) — es consecuencia de llenar la columna `ejecutada_en` de la fila `FP-18` en `forense/firmas-pendientes.tsv` (tarea 4 del encargo): `t22_firmas` § (c) emite un WARN por cada fila `FIRMADA` con `ejecutada_en` vacío, y `FP-18` ya estaba `FIRMADA` desde `ADR-91` — al citar la rama de este acto ahí, ese WARN se apaga. Verificado aislando el cambio: revertir solo el TSV con `T24` ya presente reproduce `129 WARN`; revertir solo `T24` con el TSV actualizado reproduce `128 WARN` sin cambio — el marcador nuevo es neutro, el TSV es la única causa del movimiento.

Cero `SENAL`: el vigía nace observando un estado que ya coincidía (`1 de 2` en ambos lados) — no hay disparo de diseño que declarar ni estado no-regresivo que justifique el precedente de `ADR-96`/`ADR-101(c)`/`FP-51`.

Cascada de la cifra (mismo mecanismo que `NOTAS-P3`/`CONSOLIDA-2`/`SELLA-RUTAS` ya usaron para sus propios recifrados): `canon/estado-programa-v1_10.md:129` y `:221` citaban `129 WARN` vigente — corregidas a `128` con parentético fechado, append, sin editar la cadena histórica previa. `tests/baseline.json` sin tocar, cero `--freeze`.

Efecto colateral atrapado por la propia suite: el primer nombre de esta nota (`2026-08-18-t20-llaves.md`) normalizaba idéntico al del encargo (`2026-08-18-T20-LLAVES...`) salvo mayúsculas — `T02` (duplicados nombre/contenido) lo marcó `FAIL` en la corrida de control. Renombrada a `2026-08-18-t20-llaves-vigia.md`; vuelve a `[ ok ]`. Queda como evidencia menor de que el propio ciclo de control (correr `--baseline` antes de cerrar, no solo al final) atrapa defectos que un cierre sin control se habría llevado por delante.

## §3 · Cierre

`FP-18` gana `ejecutada_en` = rama `claude/launcher-t20-llaves-wq28ec` (sin PR abierto en esta sesión — nadie lo pidió). Encargo `T20-LLAVES` marcado `CONSUMIDO` en su propio archivo. Línea en `hallazgos.md`.

**Contadores de medición sobre México: cero.** Este acto no mide nada nuevo — instrumenta un vigía sobre una cifra que `ACTO ADJ-4` ya había movido cinco días antes; la sustancia de la medición vive ahí, no aquí.
