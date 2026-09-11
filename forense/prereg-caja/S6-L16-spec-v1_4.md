# S6 · `salud.atencion.grave` — llave de diseño de hogar explícita

### `prereg-caja-S6-L16` · **v1.4** · 10 de septiembre de 2026 · `sucesora_de: v1_3`

Esta versión supera a `S6-L16-spec-v1_3.md` (`sha256 e075356bb5b35eb59282481435707f42f0a12f4d5edb72cda0931d7ae27de3eb`) únicamente para declarar el enlace hacia `c_portad.dta` que su §3.4 omitió. Todo lo demás de v1.3 —universo, disparadores, desenlaces, clasificación, ponderadores, estimando, incertidumbre, ventanas, escala y límites— se hereda sin cambio. Las versiones y corridas selladas previas permanecen intactas.

## Llave y procedimiento reproducible

`c_portad.dta` es una tabla de **hogares**, no de personas. Para añadir `estrato` e `id_loc` a cualquiera de las tablas de personas de S6:

1. normalizar `folio` a entero nullable tanto en la tabla de personas como en `c_portad.dta`;
2. descartar de `c_portad.dta` sólo las filas sin `folio`, pues no pueden enlazar con un hogar real;
3. comprobar que dentro de cada `folio` haya como máximo un valor no nulo de `estrato` y de `id_loc`; si no se cumple, `PARA` con `DEDUP-NO-LOSSLESS` y no elegir un valor;
4. reducir `c_portad.dta` a una fila por `folio`; y
5. hacer un `left join` **`m:1` por `folio`** desde la tabla de personas.

No se usa `(folio, ls)`: `ls` en la portada identifica al respondente de la portada y no a cada integrante del hogar. Las uniones persona↔persona y persona↔ponderador de v1.3 siguen usando `(folio, ls)`; esta excepción corresponde sólo a atributos del hogar tomados de `c_portad.dta`.

| lado izquierdo | lado derecho | cardinalidad esperada | llave | columnas incorporadas |
|---|---|---|---|---|
| persona, muchas filas por hogar | `c_portad.dta`, una fila por hogar tras guardias | `m:1` | `folio` | `estrato`, `id_loc` (y `edo/mpio/loc` sólo para control) |

## Evidencia ya producida; no se repite el cálculo

`data/corrida0/CALC-0003-v4/spec.md` §0 y su `RESULT-COBERTURA-DISENO` establecen: 8,441 filas leídas; 3 sin llave; 8,438 con llave; 8,437 hogares; una fila adicional del único `folio` repetido, con atributos idénticos; 0 folios con más de un `estrato`; 0 con más de un `id_loc`; `DEDUP-LOSSLESS`. La cobertura por `folio` fue `iiib_es` 19,799/19,804, `iiib_ec` 17,723/17,728, `iiib_hs` 19,794/19,799, `iiib_ce` 19,798/19,803 y `p_es`/`p_hs`/`p_ce` 1,847/1,848 cada una.

En las seis filas analíticas de v4, los faltantes de `estrato` y de `id_loc` fueron **0** después de aplicar el universo. Si una ejecución futura conserva personas sin cualquiera de esos dos atributos, debe contarlas y excluirlas de la inferencia de diseño; no puede convertir el faltante en un pseudoestrato o pseudoconglomerado.

Esta entrega ejecuta `FP-361`/D13 y cierra `NC-0065`. No reabre `FP-332`, no resuelve reservas de reponderación y no vuelve a correr `CALC-0003-v4`.

**El primer resultado que produzca este procedimiento es el que se reporta.**
