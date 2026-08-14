# ACTO C · Correcciones de registro que ENLACE-2 dejó declaradas, y la ADENDA-1 de M-APERTURA

**Base:** `origin/main = cf0dd68` (post-#236) · **Entorno:** LOCAL, corpus montado, **sin red** · **Autorización:** §2 del plan de remediación adjudicado por mesa el 14/ago — *"C1+C2+C3 · GO — arranca ya, un PR chico, sin gate ni ADR"*; A1 es propagación de un texto firmado por mesa, no adjudicación nueva. **No sella ADR. No mueve ningún contador.**

---

## §1 · A1 — ADENDA-1 al §6 (M-APERTURA), archivada verbatim

Se archiva en `forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo.md` por A.3, con el texto de mesa **verbatim** y sin editar.

**Lo único que este acto añade a esa adenda es verificación.** Las dos cifras que declara se re-derivaron con el propio script del gate contra el árbol post-#236, antes de archivarla:

```
$ awk -F'\t' '$3=="ENFIH" || $3=="ENSAFI"' data/curacion-registro/relaciones.tsv \
    | awk -F'\t' '{print $3" "$11}' | sort | uniq -c
      7 ENFIH  EXISTE;COINCIDE;INTEGRO
      5 ENFIH  NO_REFERENCIADO
      8 ENFIH  SI_O_PARCIAL
      7 ENSAFI EXISTE;COINCIDE;INTEGRO
      4 ENSAFI NO_REFERENCIADO
      9 ENSAFI SI_O_PARCIAL
```

Coincide exacto con lo que la adenda declara (7/5/8 y 7/4/9). Bajo el gate nuevo — *"procede si cada fuente tiene ≥1 fila con `capa3 EXISTE;COINCIDE;INTEGRO`"* — hoy hay 7 y 7. **M-APERTURA queda lanzable:** sus dos gates (esta adenda + `#236` fusionado en `cf0dd68`) están cumplidos.

---

## §2 · C1 — las tres correcciones, y por qué una de ellas no es la que ENLACE-2 anunció

### (a) Cita con número de línea equivocado — corregida

`REL-0c03e53054567fc014b50bc0` (N8/ENVIPE) declara el objeto `AP7_3_10..14` citando `forense/matriz-impacto-universal-2026-08-06.md:L82`. Esa línea **no lo contiene** — habla de `BP1_23`. El objeto vive en **`:L96`** del mismo expediente (*"exposicion_violencia | ENVIPE `AP7_3_10..14`, `MEDIDO·PARCIAL`"*), abierto y confirmado.

Corregido en `evidencias.tsv`: `evidencia_ref` pasa a `:L96`, con la corrección y su razón anotadas en `incertidumbre`. **El enlace no cambia** — `envipe2025_csv` seguía siendo el payload correcto por otra vía (§2c) y su `capa2` no se toca.

### (b) Campo `formato` vencido en el manifiesto — corregido

`encig23_base_datos_csv` declaraba *"Solo se leyeron `encig2023_04_sec_7` y `encig2023_05_sec_8` — las otras cuatro tablas no se inspeccionaron"*. Cierto al registrarse el 29/jul; **vencido desde el 4/ago**, cuando Encargo W abrió `encig2023_01_sec_11` (batería XI) y publicó frecuencias reales de `P11_1_23` (`forense/notas/2026-08-04-w-coeficientes-generador-paso1.md`, líneas 179 y 272) — el objeto que ENLACE-2 enlazó para N1/ENCIG.

El campo ahora fecha lo que era cierto al registrar, declara la parte vencida con su fuente, y deja el conteo correcto: **quedan tres tablas sin inspeccionar**, no cuatro.

### (c) La tercera no era lo que ENLACE-2 dijo — se retracta, no se "corrige"

ENLACE-2 declaró que las gemelas `REL-45672e7d…` y `REL-ba510588…` (ambas N6/ENFIH, sin par, mismo `L10` de `abrir4-variables`) cierran distinto y que **"lo único que las separa es cómo quedó escrita la cita"**. Al abrir las dos entradas completas de `evidencias.tsv` para corregirlas, eso resultó **sobredicho**:

| | `REL-45672e7d…` | `REL-ba510588…` |
|---|---|---|
| `tipo_evidencia` | `INSTRUMENTO_LOCAL_PARCIAL` | `EVIDENCIA_ACEPTADA_PREVIA` |
| `evidencia_ref` | el TSV, sin línea | `…tsv:L10` |
| `evidencia_localizador` | `L9-L14` | `NO_DETERMINADO` |
| dónde vive la afirmación del par | `parte_necesidad_cubierta` | `texto_evidencia` |
| qué dice su propio texto | *"no demuestra para esta clave el par constructo–desenlace exigido"* | *"esta evidencia no satisface N6"* |

**No se pinea la cita.** Pinearla a `:L10` fabricaría un objeto que ese registro **deliberadamente no nombra** (`variable_reactivo_tabla = NO_DETERMINADO`, y su `texto_evidencia` declina demostrar el par *para esta clave*) — y lo haría con una edición mía, para después justificar con ella un cambio de veredicto. Eso es circular, y es exactamente la clase de movimiento que la jerarquía de MAP-B existe para impedir.

**El veredicto distinto se mantiene y su fundamento sigue siendo concreto:** la cita de la gemela fija `:L10` y resuelve a un objeto nombrado (`P9_12_1..6`); ésta da un rango sin nombrar variable. Lo que se corrige es **la afirmación de ENLACE-2**, reescrita en la `nota` de la fila. **`capa2` no se mueve: sigue en 51.**

---

## §3 · C2 — ENVIPE 2025 está registrada dos veces, y ahora cada entrada lo dice

`envipe2025_csv` (datos abiertos, sha256 `8a7a99fd…`, 17.6 MB) y `envipe_2025_bd_envipe_2025_csv` (canasta masiva de DESC-1, `ecb39b86…`, 18.9 MB) coexisten, ambas verifican `COINCIDE`, y **ninguna de las dos declaraba la existencia de la otra**. La segunda decía solo `usado_para: sin uso asignado`.

Las dos entradas llevan ahora referencia cruzada explícita, con el hecho que decide: las mediciones del 4/ago (`AP7_3_10..14` y `BP2_1`) abrieron **la primera** — su sha256 aparece citado en `forense/notas/2026-08-04-medicion-exposicion-violencia-envipe.md` línea 89, y `…-envipe-tper-vic2-tmod-vic-paso1.md` línea 482 declara haber contado filas de `TPer_Vic2` y `TMod_Vic` dentro de ese zip. La segunda se registró **un día después**. No son intercambiables por nombre, y ahora quien las lea lo sabrá sin reconstruirlo.

---

## §4 · C3 — `.gitignore` no ignoraba el symlink del corpus

`.gitignore:5` traía `data/raw/`. Ese patrón, **con barra final, casa un directorio y no un symlink** — y `data/raw` es un symlink al corpus compartido en todos los worktrees. Consecuencia medida: cada árbol arrastraba `?? data/raw` en `git status` y cada PR abría con el aviso *"1 uncommitted change"*, con el riesgo latente de que alguien lo añadiera al índice.

Añadida la entrada sin barra. Verificado: `git check-ignore -v data/raw` → `.gitignore:6:data/raw`. La entrada con barra se conserva — cubre el caso de que alguien monte el corpus como directorio real en vez de symlink.

---

## §5 · Verificación

- **La vía, sin cambio:** `COINCIDE=51 · Diffs propuestos 0`, antes y después de las cuatro ediciones.
- **El manifiesto sigue parseando:** 631 entradas, y los tres payloads tocados (`envipe2025_csv`, `envipe_2025_bd_envipe_2025_csv`, `encig23_base_datos_csv`) siguen dando `COINCIDE` contra disco, con `sha256` y `tamano_bytes` intactos.
- **Los dos TSV conservan su forma:** `evidencias.tsv` 201 líneas × 27 columnas, `relaciones.tsv` 198 × 19; una sola línea cambiada en cada uno.
- **Defecto de edición hallado y declarado, porque volverá a morder:** el primer intento de escribir estas entradas rompió el YAML dos veces. (1) `: ` dentro de un escalar plano lo parte; (2) — el más traicionero — **` #` abre comentario dentro de un escalar plano**, así que escribir `(PR #236)` truncaba la línea y el parser fallaba varias líneas más abajo, lejos de la causa. Ambos se detectaron al re-parsear antes de commitear. Quien escriba `usado_para` largo debe evitar `: ` y ` #`, o entrecomillar el escalar entero (que es lo que hacen las entradas ya existentes que sí traen dos puntos).

**Contadores: ninguno se mueve.** `capa2 SI` sigue en 51, `13 de 27`, `11 de 15`, `0 de 15` y `1 de 2` intactos. Este acto es higiene de registro y propagación de una firma.

**La frase:** el primer resultado que produjo este procedimiento es el que se reporta — incluida la corrección que retracta una afirmación propia de hace unas horas.
