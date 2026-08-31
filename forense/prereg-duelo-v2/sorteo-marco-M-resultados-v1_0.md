# Sorteo del marco-M — `ACTO MAESTRA32-E14 · MARCO-M-SORTEA` (ACTO B′), resultados

## Pre-registro del primer commit (antes de correr el PRNG)

- `SHA_A` (merge de `PR #403`, `ACTO MAESTRA32-E13 · MARCO-M-CONGELA`, verificado ancestro de `origin/main` por `git merge-base --is-ancestor f4d9b7f506aa5205231f6e7b355645d1206dd031 origin/main`, y tip literal de `origin/main` al arrancar este acto): `f4d9b7f506aa5205231f6e7b355645d1206dd031`.
- `scope_id = "MARCO-M-v1"` (E13 §e, no elegido por este acto).
- Semilla derivada por `sorteo_v2.semilla_desde_sha_merge(SHA_A, "MARCO-M-v1")` (misma función que `ACTO B` original, no reinventada): **`63114853283919194858838455602446543838`**.
- `N_elegibles`: leído de `forense/prereg-duelo-v2/CONGELADO-M-v1_0.sha256` → `N_elegibles=2`. sha256 recomputado de `marco-M-congelado-v1_0.tsv` (`e71c2f105d4c9fce537d385e0e4233cb86ea35345955602863e3c14bf03a830e`) coincide byte a byte con el declarado en ese archivo. **Control PASA** — sin este control no habría corrida.
- Regla de tamaño (`forense/notas/2026-08-31-marco-M-spec.md` §e, fijada por E13 antes de ver `N`): `N < 15 → sin sorteo (todas las elegibles)`. Con `N_elegibles=2`: `n_sorteo = N_elegibles = 2`; `cuota_max = floor(0.20·2) = 0`.
- **Hallazgo, no decisión de este acto**: `N_elegibles=2 < 15` — el "sorteo" es la identidad (`sorteo_marco_m.sortear_marco_m` no invoca el PRNG bajo ese piso; ver docstring). La semilla se deriva y se declara igual, aunque no participe en la selección — el pre-registro es el mismo protocolo esté o no activo el PRNG.
- Invocación exacta a ejecutar:
  ```python
  from sorteo_marco_m import cargar_marco_m, sortear_marco_m, semilla_desde_sha_merge, regla_de_tamano

  SHA_A = "f4d9b7f506aa5205231f6e7b355645d1206dd031"
  semilla = semilla_desde_sha_merge(SHA_A, "MARCO-M-v1")
  marco = cargar_marco_m()  # marco-M-congelado-v1_0.tsv, assert n == N_elegibles de CONGELADO-M-v1_0.sha256
  n_sorteo, cuota_max = regla_de_tamano(len(marco))
  resultado = sortear_marco_m(marco, n_sorteo=n_sorteo, cuota_max=cuota_max, semilla=semilla)
  ```
- La semilla anulada `867948c` (`ADR-135(d)`) y la semilla del `ACTO B` original (`174266824551963846210387427777144587800`, distinto `scope_id`) NO se reutilizan bajo ninguna circunstancia (§3.4) — `scope_id="MARCO-M-v1"` ya las distingue por construcción.

**El primer resultado que produzca este procedimiento es el que se reporta.**

---

## Resultado (segundo commit — salida íntegra, una sola corrida)

`sortear_marco_m(marco, n_sorteo=2, cuota_max=0, semilla=63114853283919194858838455602446543838)` sobre `marco-M-congelado-v1_0.tsv` (2 filas elegibles, `N_elegibles` verificado contra `CONGELADO-M-v1_0.sha256`). Como `N_elegibles=2 < 15`, el resultado es la identidad: entran las 2 filas, sin invocar `random.Random`.

### Las 2 filas sorteadas (= todas las elegibles, identidad por §e)

| # | id | estrato | grado | publicada |
|---|----|---------|-------|-----------|
| 1 | TRA-M-01 | tramite\|P1\|MEDIA | P1 | NO |
| 2 | TRA-M-02 | tramite\|P1\|MEDIA | P1 | NO |

Sin `SKIP`, sin estratos excluidos (la rama identidad no evalúa infactibilidad — con un solo estrato no vacío y todas sus filas entrando, no hay cuota que fallar).

**Discrepancia observada, no corregida por este acto:** la columna `publicada` del `.tsv` real viene vacía (no `"NO"` literal como narra `forense/notas/2026-08-31-marco-M-spec.md` §(b)) — verificado con `csv.reader` campo por campo, 17 columnas contra 17 encabezados, sin desalineación de tabs. `sorteo_marco_m.cargar_marco_m` trata la celda vacía como `"NO"` (mismo default declarado en la spec de E13), documentado aquí porque es una lectura de dato, no un hallazgo nuevo de este acto — corresponde a quien audite E13 decidir si el `.tsv` se corrige o si el default basta.

### Verificación de las tres invariantes del reglamento

- **Tamaño**: `len(resultado) = 2 == n_sorteo = 2` ✓ (`len(resultado) <= n_sorteo` con igualdad, caso identidad).
- **`publicada=SI` ≤ `cuota_max`**: `count(publicada=SI) = 0 ≤ cuota_max = 0` ✓ (cumple con margen cero — no hay ninguna fila `SI` en el universo elegible completo).
- **Piso 1 por estrato no vacío**: único estrato presente en el marco-M (`tramite|P1|MEDIA`) tiene sus 2 filas en el resultado (`2 ≥ 1`) ✓. No aplica un segundo estrato — el universo entero es monoestrato.

### Determinismo

Misma semilla (derivada de `SHA_A` fijo) + mismo `.tsv` (sha256 verificado) ⇒ mismo resultado, por construcción: la rama identidad ni siquiera depende de la semilla (ver `TestSortearMarcoMIdentidad.test_semilla_no_importa_bajo_el_piso` en `tests_sorteo_marco_m.py`), y la rama con PRNG (no activa aquí) hereda el determinismo ya probado de `sorteo_v2.sortear`.

### sha256 de este registro

`sha256` de este registro (calculado sobre el contenido hasta esta línea, antes de añadirla): `74d1f3117f84fc9b2a1b228f547844cae5ce8b3e822a1b3fc974f1ad03b98bdd`
