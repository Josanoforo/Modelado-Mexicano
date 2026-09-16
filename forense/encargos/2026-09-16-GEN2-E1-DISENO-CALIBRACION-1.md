# ENCARGO · ACTO GEN2-E1-DISENO-CALIBRACION-1

**Archivado verbatim (0-bis A.3).** Llegó como mensaje de lanzamiento de la
sesión de NUBE del 16/sep/2026. No se edita: lo que este acto midió y
diseñó contra él va en el documento de diseño y en `## NO-CORRIDO /
RESERVAS`, no aquí.

---

NUBE · ACTO GEN2-E1-DISENO-CALIBRACION-1 (Opus, integral; gated a F-18). NC-0239 ya lo nombra como sucesor de las siete filas del marcador: hacer θ cargable por celda. Tal como te lo dejé: diseño primero, nombre por nombre de procedencia.yaml, con escala, universo y argumento de identificación o su ausencia (A-bis 1/2); cero números hasta spec congelada. Sin tu firma no se lanza — y es la que decide si el motor por celda existe.

## COMPUERTA — F-18, verificada

`gated a F-18` se dejó sin poder verificarse en el primer intento de arranque de esta sesión: `F-18` no aparecía en ningún archivo del árbol (`canon/registro-rotulos.tsv`, `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`, `canon/gobernanza-v1_15.md`) — cero coincidencias reales, solo subcadenas dentro de hashes/URLs (ruido, A.13). Reportado así, con cero commits.

Mesa respondió en el mismo canal con el texto verbatim de `F-18` (y, en el mismo mensaje, `F-17`, objeto de otra pieza — ver abajo). Ambos se archivaron íntegros, primer commit sustantivo de esta sesión, en `forense/encargos/2026-09-16-GEN2-FIRMAS-MESA-3.md`. Ese archivo es el producto contra el que esta compuerta se verifica: `git show HEAD:forense/encargos/2026-09-16-GEN2-FIRMAS-MESA-3.md` — `F-18 · Abrir el diseño de E1 → misma cabecera`, autorizando el diseño de la calibración E1 de Θ(x) sobre `NC-0239`, con el mandato exacto que este encargo ya pedía (nombre por nombre, escala, universo, identificación-o-ausencia, cero números). Compuerta cumplida.

`F-17` (objeto distinto: crosswalk de ejes, citando `NC-0226 renumerada`) llegó en el mismo mensaje pero no es la compuerta de este acto y su número de NC no corresponde a su propio objeto (ver el archivo de firmas) — queda fuera de este perímetro, registrado en `## NO-CORRIDO / RESERVAS`.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| `F-17` (crosswalk de ejes árbitro↔modelo, citado en el mismo mensaje que `F-18`) | `FUERA-DE-PERÍMETRO` — el objeto de este acto es la calibración de Θ (`NC-0239`), no el vocabulario de ejes (`NC-0240`/`NC-0226`); mezclar los dos perímetros en un solo acto viola A.10 | `NC-0240` sigue sin firma resuelta y con una discrepancia de numeración sin aclarar (ver `forense/encargos/2026-09-16-GEN2-FIRMAS-MESA-3.md`); registrada como `NC-0254` | acto propio de crosswalk, después de que mesa aclare si `F-17` quería decir `NC-0240` |
| La corrida de calibración de Θ(x) (asignar valores numéricos a las celdas del marcador) | `PARO-PREMISA` — el propio encargo lo ordena: "ningún número hasta que la spec de identificación esté congelada; la corrida es acto de caja posterior" | Las 14 celdas del marcador siguen con `x = vacío`; `theta.valor()` sigue lanzando `ThetaNoDisponible` | acto de caja posterior, una vez que mesa firme la spec de identificación que este acto entrega congelada |
| Tocar `milpa/src/theta.py` o `milpa/src/motor.py` | `PARO-PREMISA` — el propio encargo lo ordena: "theta.py no se toca en el diseño" | El motor sigue exactamente como estaba; ningún cambio de código en este acto | mismo acto de caja posterior |
| Llenar los campos de escala/universo/identificación que el censo (ver documento de diseño) marca como `FALTA-*` | `DECISIÓN-DE-MESA-PENDIENTE` / `NO-VERIFICABLE-AQUÍ` — varios huecos exigen una decisión de mesa (p.ej. qué universo declarar para `asignados_probabilidad`, si los 90 `params_base_de_perfil` tipológicos entran o no al esquema) que un acto de diseño no puede tomar por sí solo | La spec de identificación no puede darse por "congelada en su totalidad": queda congelada en lo que el censo cubrió, con los huecos nombrados uno por uno; registrada como `NC-0253` | mesa firma los huecos listados en el documento de diseño, sección "Huecos abiertos para mesa" |

`NC-0239` recibe enmienda fechada (no se cierra: solo el diseño se ejecutó, la corrida sigue pendiente) — ver `forense/no-corrido.tsv`.

## CONSUMIDO

Pendiente — se añade en el commit de cierre de esta sesión, citando el PR real.
