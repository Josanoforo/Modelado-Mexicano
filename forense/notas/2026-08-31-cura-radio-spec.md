# COMMIT-1 · receta congelada de CURA-RADIO-CONFIANZA (re-emisión)

`ACTO MAESTRA32-E20 · LOTE-NUBE-1 · P1`, 31/ago/2026. Re-emisión verbatim del
`COMMIT-1 §(a)-(e)` del encargo archivado
`forense/encargos/2026-08-31-MAESTRA32-E17-CURA-RADIO-CONFIANZA.md`, que cerró
por hallazgo de compuerta (`ADR-234`) sin llegar a correr. La receta es la de
E17, sin cambios; lo único nuevo son los **conteos, re-derivados contra el árbol
de hoy** (`d510a63`), nunca heredados de aquel encargo.

Se escribe y se congela **antes** de recorrer los inventarios. No se edita
después de correr.

## Firma que la autoriza

**D-B**, mesa 31/ago/2026, verbatim: *"Curémosla, pero si no da necesito que me
des una solución, porque entonces es un coeficiente menos que tiene de dónde
obtenerse."*

## (a) Regla de curación del homónimo

Todo reactivo con `confía`/`confianza` en `texto_reactivo` de cualquier ola de
ENDIREH (2006/2011/2016/2021, en `ext` y `v1_2`) se clasifica por referente con
**lista cerrada**:

- **INTERPERSONAL** — familiares, parientes, vecinos, amigos, conocidos,
  compañeros, "la gente"/"las personas".
- **INSTITUCIONAL** — autoridades, gobierno, policía, ministerio público,
  jueces, instituciones, iglesia.
- **OTRO** — pareja/esposo (relación diádica, no radio) y lo no clasificable.

**Solo INTERPERSONAL cuenta como θ de `radio_confianza`.** El orden de
resolución se fija aquí, antes de ver un solo reactivo: se prueba OTRO primero
(pareja/esposo desplaza a cualquier otra lectura, porque es la trampa que la
curación existe para atrapar), luego INSTITUCIONAL, luego INTERPERSONAL; lo que
no case con ninguna, OTRO por defecto. Sin este orden, un reactivo como "¿confía
en su pareja o en sus familiares?" caería en dos casillas y la clasificación
dejaría de ser función.

## (b) Co-observación válida

≥1 reactivo **INTERPERSONAL** y ≥1 **desenlace de G5** en la **misma base**
(`bd_mujeres` u otra), con instrumento identificado. "Misma base" se opera como
el mismo `archivo_miembro` dentro del mismo `payload_id`; se reporta además el
resultado laxo (mismo `payload_id`, distinto `archivo_miembro`), etiquetado como
tal, porque un choque a nivel payload no garantiza muestra común y decirlo es
parte del hallazgo.

Términos de desenlace G5, de la spec de E2
(`forense/notas/2026-08-28-empareja-spec.md:62`), **sin cambios**: `pooling`,
`corresidencia`, `vive con`, `hogar extendido`, `cuidado de familiares`, `carga
de cuidado`, `cuidador`, `cuida a`, `comparte gastos del hogar`, `hogar
compartido`, `mudarse con la familia`, `se mudó con`, `se mudo con`.

## (c) Escalera de contingencia — 5 peldaños, **completa aunque uno dé positivo**

Se corre entera para que mesa vea todo el mapa, no solo el primer sí. Cada
peldaño con sus **conteos A.13** (filas de inventario examinadas, hits, olas):

1. **ENDIREH**, todas las olas.
2. **`encup2012`**, batería `P30` (27 ítems "confía en"): mismo clasificador por
   referente; desenlace G5 en el mismo instrumento.
3. **ENNViH/MxFLS**: `ehh05dta_all.zip` y las olas 2-3 de CAL-G3 — módulo de
   capital social/confianza + transferencias familiares/corresidencia.
4. **ENCUCI 2020**: tiene la θ ancla `radio_confianza`
   (`milpa/procedencia.yaml:280-293`, `AP5_1_1/2/3`); se busca el desenlace G5
   ahí (apoyo entre vecinos/familia, cuidado).
5. **WVS y Latinobarómetro México** (descargados desde el 12/ago,
   `data/manifiesto.yaml`): confianza en familia/vecinos/conocidos es su ítem
   canónico; se busca desenlace G5.

**Universo de búsqueda**: la unión de los cuatro inventarios de reactivos
(`data/inventario-reactivos-v1_2.tsv`, `-ext-v1_0`, `data/inventario-fd-v1_1.tsv`,
`data/inventario-fd-ext-v1_0.tsv`). Búsquedas en Python UTF-8, sin acento
sensible (se normaliza para comparar, no se reescribe el dato). Repo-only: **no
se abre ningún payload de microdato**.

**Límite declarado antes de correr** (heredado de `MAESTRA31-E4`/`FP-171`, F1):
`texto_reactivo` viene **vacío** en el 100% de las filas de método
`INSPECT_ZIP`. Un peldaño cuyo instrumento solo tenga filas `INSPECT_ZIP` no
puede clasificarse por referente **por ausencia de texto, no por ausencia de
reactivo** — y eso se reporta como tal, con el conteo, nunca como un negativo
sobre el instrumento (A.13).

## (d) Si ningún peldaño da co-observación — la solución, pre-escrita

- **(d1)** El par queda `EXISTE-NO-SATISFACE` con las **medias parejas nombradas
  por peldaño**: es un mapa, no un vacío.
- **(d2)** Estatus del coeficiente mientras tanto: sigue
  `ASIGNADO · SOLO-SIGNO·NO-COMPARABLE` (`ADR-220`), sin magnitud medida. **No**
  se inventa un valor ni se transporta uno de otro constructo.
- **(d3)** Fila de adquisición **con nombre**, para `FP-179`: el instrumento que
  en el peldaño 5 tenga la θ más limpia (WVS ola 7 México o Latinobarómetro) más
  el módulo faltante del lado desenlace; o bien ENCUCI 2020 si su desenlace G5
  existe pero la θ falla. Se escribe cuál, con los reactivos, para que la compra
  sea una línea y no una búsqueda.
- **(d4)** Vía alterna **declarada, no ejecutada**: medir `radio_confianza` como
  coeficiente compuesto de dos instrumentos, solo si mesa lo firma después. No
  cabe en (ii)/(i′) y se dice.

## (e) B-bis

Positivo en el peldaño 1 → medidor de caja sucesor sobre ENDIREH. Positivo solo
en 2-5 → medidor sobre ese instrumento. Negativo total → (d) completo.

## Salida

`data/curacion-radio-confianza-v1_0.tsv` — reactivo × referente × instrumento ×
ola × peldaño. Veredicto A.4 por peldaño en la sección fechada que esta
re-emisión añade al final de `forense/notas/2026-08-31-cura-radio-cierre.md`
(el cierre de E17 queda **intacto**, A.10) y en la nota de cierre del lote.

**Intocables, `git diff --stat` vacío al terminar P1**: los cuatro inventarios,
`data/emparejamiento-motor-v1_2.tsv`, la spec de E2, `milpa/**`.

---

"El primer resultado que produzca este procedimiento es el que se reporta."
