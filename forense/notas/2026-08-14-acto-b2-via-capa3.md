# ACTO B2 · La vía deja de romper la biyección, y la suite gana el canario que faltaba

**Encargo:** `forense/encargos/2026-08-14-B2-mantenimiento-via-capa3.md` (firma B1 de mesa) · **ADR:** `ADR-84` · **Base:** `origin/main = 8925588` (post-#238) · **Entorno:** LOCAL, corpus montado, **sin red**.

---

## §0 · El reloj, medido antes de arrancar

`ADR-70(d)` congela `tools/curador_registro/` **a partir del primer registro de celda-D del piloto en E0**. Estado verificado sobre el árbol, no heredado del plan:

- **E0 existe pero no ha registrado nada.** `ACTO MOTOR-3/E0` fusionó (PR #237), y su propio commit `2abf292` se titula *"FASE-PLAN: A.3 + el diseño de milpa/src/ — **cero código**, el gate devolvió 0"*. `milpa/src/` no existe en el árbol.
- Las tres celdas en `data/curacion-registro/celdas-d/` son las **semillas previas de ADR-68** (radio, familismo.actitud, obligación), no un registro del piloto.
- **Los Compass ×3 ya aterrizaron** (PR #234, `forense/compass-1/2/3-*.md`), así que la precondición que bloqueaba MOTOR-2 murió y la cadena MOTOR-2 → E0 puede cerrar la ventana pronto.

**Conclusión: la ventana sigue abierta hoy y no se puede contar con que lo esté mañana.** Por eso este acto va ahora.

---

## §1 · (a) La vía escribe `capa3_disco_real` al promover — hecho

**El defecto.** `aplicar_diffs()` escribía `capa2_manifiesto` y nada más. Como la biyección `capa2`↔`capa3` se cumple en `relaciones.tsv` sin una sola excepción, **cada promoción producía una fila `SI`|`SI_O_PARCIAL`**: el mismo comando que actualizaba una columna rompía la correspondencia con la otra. Medido en ENLACE-2 (PR #236): **8 promociones, 8 desacuerdos**, reconciliados a mano en ese acto porque la nota los detectó. Lo que cuesta no detectarlos lo documenta CAPA3-RECONCILIA (PR #202): **19 → 0**, un acto entero.

**El arreglo, y su condición.** `derivar()` propaga ahora `estado` (y `capa3_actual`) al diff; `aplicar_diffs()` escribe `EXISTE;COINCIDE;INTEGRO` **solo** cuando `derivado == "SI"` **y** `estado == "COINCIDE"`, devuelve cuántas celdas de capa3 escribió, y `main()` lo imprime.

La condición no es el veredicto sino la verificación, y eso importa: `EXISTE;COINCIDE;INTEGRO` afirma exactamente lo que `verificar_entrada() == "COINCIDE"` comprueba —existe en disco, sha256 y tamaño coinciden—, así que el valor está **ganado, no supuesto**. `CAPA3_INTEGRO` tampoco se inventa: es el literal que ya llevan las 51 filas `SI` del archivo. Hoy `derivado = "SI" if estado == "COINCIDE"` hace imposible una promoción sin COINCIDE; si esa regla cambiara, la función debe **dejar capa3 en paz** en vez de adivinar, y hay una prueba que lo fija.

**La regla de promoción a `SI` no se toca** — igual que ADR-73.

---

## §2 · (b) `bootstrap.py` — PARO. La medición no sostiene la premisa con la que se selló

Reporté a mesa que `derive_evidence_state` casa `NO_REFERENCIADO` por subcadena sobre `f"{capa3};{capa4}"` y que por eso rotularía mal las 40 filas que ENLACE-2 degradó. Mesa lo selló con esa caracterización. **Al ir a ejecutarlo, medí el efecto de quitar el token y no es acotado:**

| | filas |
|---|---|
| `NO_REFERENCIADO` que ya existían antes de ENLACE-2 | **86** |
| de ellas, con `INDEXADO` en `capa4` (rótulo justificado por capa4) | **12** |
| de ellas, cuyo rótulo depende de la subcadena de `capa3` | **74** |
| de esas 74, hoy rotuladas `INDEXADO_NO_DESCARGADO` y **en sincronía** con lo commiteado | **50** |

Quitar el token **relabelaría esas 50 filas preexistentes que hoy están bien**, para arreglar 40 que no están mal: `INDEXADO_NO_DESCARGADO` significa *"indexación declarada sin apertura exacta vinculada"*, y eso es cierto de las 40 —todas con `capa1_universo_indexado = SI`— tanto como de las 62.

**Mi caracterización de "rótulo semánticamente falso" no sobrevive a su propia medición.** Se declara aquí en vez de ejecutar el sello a ciegas, y `bootstrap.py` **no se tocó**.

**Lo que sí queda establecido, y es el defecto real:** `bootstrap-semantico.tsv` es una tabla **derivada** que nada re-deriva y nada compara contra su fuente. ENLACE-2 la desincronizó en **45 de 48** filas —commiteado `MECANISMO_NO_EJECUTADO` ×45 + `MAPEADO_COMPLETO` ×3, derivado hoy `INDEXADO_NO_DESCARGADO` ×40 + `DESCARGADO_NO_ABIERTO` ×5 + `MAPEADO_COMPLETO` ×3— y ninguna prueba lo notó. Es **latente**: `bootstrap.py` no corre en CI (`.github/workflows/verify.yml` corre `tests/check.py --baseline` y `tests/test_svystat.py`) y `relaciones.tsv` se bulk-cargó una sola vez.

**Queda para mesa, con dos salidas nombradas y ninguna tomada aquí:** (i) re-derivar esas 48 filas de `bootstrap-semantico.tsv` para volver a sincronía —mecánico, sin tocar vocabulario—; o (ii) añadir un test que vigile la divergencia, que **hoy fallaría en 45 filas** y por tanto necesita autorización propia.

---

## §3 · (c) `T21 T-CAPA2-CAPA3` — hecho, y probado en las dos direcciones

**Por qué faltaba.** Antes de este acto, `grep -c "capa2\|capa3" tests/check.py` daba **0**. Nada en la suite vigilaba las dos columnas, y `test_via_capa2.py` tenía cuatro pruebas, ninguna sobre capa3. Ésa es la razón por la que el defecto de §1 pudo vivir callado desde que la vía existe.

`T21` declara la correspondencia, falla sobre cualquier fila que la rompa, y **avisa sin fallar** si aparece un valor de `capa2` no declarado — para que quien lo introduzca diga qué `capa3` le toca, en vez de que el test lo bloquee o lo ignore.

**Un canario que no puede fallar no sirve, así que se probó también en rojo:**

```
sobre el árbol real                              →  [ ok ]  T21 T-CAPA2-CAPA3
sobre una copia con 3 filas SI|SI_O_PARCIAL      →  [FAIL]  T21 T-CAPA2-CAPA3  (1 fail)
inyectadas (el defecto exacto de §1)
```

Y dos pruebas nuevas en `test_via_capa2.py` (**6 en total, verdes**): que la promoción arrastra `capa3` **y solo en las promovidas** (las otras tres filas del fixture conservan el suyo intacto), y que un diff con `estado != COINCIDE` **no** toca `capa3` — capa3 no se adivina desde el veredicto.

---

## §4 · Verificación y contadores

- **La vía, antes y después:** `COINCIDE=51 · Diffs propuestos 0`. Este acto **no corre `--escribe`** contra `relaciones.tsv`; el árbol de datos queda intacto.
- **`tests/check.py --baseline`:** **LÍNEA BASE VERDE**, `21 FAIL · 108 WARN`, nada nuevo frente a `tests/baseline.json` (HEAD congelado `640a74d`). T21 entra en verde y ni el ADR nuevo ni su cascada mueven T15/T16. `test_via_capa2.py`: **6 pruebas, OK**.
- **Perímetro real, tres archivos de código y dos de canon:** `via_capa2.py`, `tests/check.py`, `tools/curador_registro/tests/test_via_capa2.py`, más `canon/gobernanza-v1_15.md` (ADR-84) y `canon/estado-programa-v1_10.md` (cascada). **`bootstrap.py` no se tocó.**
- **Cascada de ADR, derivada con la receta de T15 justo antes de escribir el ADR:** 83 únicos, contiguos 1..83, sin huecos ⇒ **84**. Propagado a `gobernanza-v1_15.md:2` y `estado-programa-v1_10.md:27,101`. Coincidió con el candidato que el plan mencionaba, **sin heredarlo**.
- **Contadores: ninguno se mueve.** `capa2 SI` sigue en 51; `13 de 27` · `11 de 15` · `0 de 15` · `1 de 2` · `4 de 144` intactos.

**La frase:** el primer resultado que produjo este procedimiento es el que se reporta — incluido el inciso sellado que este acto **no** ejecutó, y la razón medida por la que no.
