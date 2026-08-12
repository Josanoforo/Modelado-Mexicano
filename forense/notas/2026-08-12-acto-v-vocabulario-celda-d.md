# ACTO V · Vocabulario celda-D — `fuerza` se parte en dos (`ADR-71(d)`)

## 1 · El defecto, verificado antes de escribir vocabulario nuevo

`fuerza: ASIGNADO | AJUSTADO | IDENTIFICADO` (`propuesta-motor-adaptativo-celda-v0_3.md` §3) describe el **coeficiente** de `milpa/procedencia.yaml` que una condicional alimenta — no la condicional misma. Las dos únicas celdas-D que existen hoy escriben fuera del enum, cada una con su propia reserva razonada en el YAML:

- `G5.familismo_obligacion.actitud.yaml` (línea 58, antes de este acto): `fuerza: NO_DETERMINADO` — "los tres valores del enum caracterizan un VALOR existente en `milpa/procedencia.yaml`, y aquí no hay valor que caracterizar."
- `G5.radio_confianza.encuci_vs_enbiare.yaml` (línea 144, antes de este acto): `fuerza: "MEDIDO·PARCIAL(x)"` — "ninguno de los tres nombra con precisión una medición condicional directa de microdato... El COEFICIENTE que este valor alimenta (`radio_confianza=0.15` en G5, `milpa/procedencia.yaml:629`, "magnitud: asignada") sí es `ASIGNADO` — pero es un objeto distinto... no la condicional misma que esta celda compara."

`radio_confianza` ya diagnosticó su propio defecto de raíz, en su propio comentario, antes de este acto. `ADR-71(d)` ordena la corrección.

## 2 · Colisión de terreno, no prevista al escribir el encargo — verificada, no supuesta

PASO 1 del encargo pedía `grep -rln "celdas-d" tools/ tests/ --include=*.py` = vacío, como pre-condición para que el acto costara lo que se presupuestó (sin schema de código dependiente del vocabulario). Al correr el ARRANQUE de este acto, el grep ya no era vacío: `tests/test_celdas_d.py` — que no existía cuando el encargo se escribió — landed vía el merge de `remediacion/brecha-documental` (PR #177, `ENCARGO CABLEADO-100`, G4/TAREA 4.2). Leído completo antes de decidir: valida presencia de campos obligatorios (incluido `fuerza`) y algunos valores (rol, tipo_adjudicacion, dominio), pero **declara explícitamente en su propio docstring** que NO valida el valor libre de `fuerza` — "forzar aquí un enum más estricto que el que la propia propuesta ejemplifica rompería los dos archivos sellados que este validador debe aceptar." Confirmado: `grep -n "ASIGNADO\|AJUSTADO\|IDENTIFICADO" tests/test_celdas_d.py` → vacío.

La colisión real no era de VALOR — era de PRESENCIA: `REQUIRED_TOP_FIELDS` exige que el campo `fuerza` exista. Este acto lo retira (lo reemplaza por dos campos nuevos). Sin parche, `test_celdas_d.py` habría marcado FAIL en las dos celdas por "falta campo obligatorio 'fuerza'" — no era un problema hipotético, se confirmó corriendo el validador antes y comprobando qué campo exigía.

**Consultado con mesa antes de proceder** (el PASO 1 original de este acto decía PARA si algo en código validaba los YAML). Resolución de mesa, verificada independientemente antes de aceptarla:

- `ADR-68(a)` **no aplica** — su texto congela `tools/curador_registro/` ("El motor `tools/curador_registro/` NO se modifica durante el piloto"), y `tests/test_celdas_d.py` vive en `tests/`, directorio distinto. Mismo precedente que `ADR-62` (`ENCARGO MT-mantenimiento`, 4/ago/2026), que ya tocó `tests/test_svystat.py` sin reabrir el congelamiento del motor. Verificado: el texto de `ADR-68(a)` no menciona `tests/` en ninguna forma.
- El parche es de una línea: `REQUIRED_TOP_FIELDS` sustituye `"fuerza"` por `"fuerza_coeficiente", "procedencia_condicional"`. Nada de validación de valor se añade — ni el enum cerrado de `fuerza_coeficiente` ni la regla de extensibilidad de `procedencia_condicional` ganan instrumentación en este acto, por la misma regla de "no instrumentar sin defecto real ya ocurrido" que gobierna el resto del programa: bajo el diseño nuevo, las dos celdas existentes escriben `ASIGNADO` y un valor del conjunto inicial — no hay, hoy, ninguna instancia real que un validador de valor hubiera atrapado.
- **Perímetro ampliado, declarado**: `tests/test_celdas_d.py` entra al perímetro de este acto (originalmente excluido — "NO toca `tools/`, `tests/`, `canon/`, `milpa/`"), por la razón de arriba: el validador llegó después de que el encargo se escribiera, y no parchearlo habría dejado los dos únicos YAML del registro en rojo contra un validador que el propio acto de sellar `ADR-71(d)` no podía haber anticipado.

## 3 · Derivación de `fuerza_coeficiente` para `familismo_obligacion.actitud` — de archivo, no tecleada

A diferencia de `radio_confianza` (cuyo YAML ya citaba `milpa/procedencia.yaml:629` con el valor `ASIGNADO` explícito), `familismo_obligacion.actitud` no traía la cita lista. Derivado en este acto:

```
$ grep -n "familismo_obligacion" milpa/procedencia.yaml
117:    coeficiente_nuevo: "+1 · familismo_obligacion en G5, ASIGNADO y SIN MAGNITUD (spec: 'signo negativo o no monotónico')"
629:    - {gen: G5, coefs: {..., familismo_obligacion: "signo negativo o no monotónico — SIN MAGNITUD", ...}, signo: sostenido, magnitud: asignada}
899:    - {gen: G5, coef: familismo_obligacion, ruta: SIN-RUTA, prioridad: BAJA, nota: "sin magnitud asignada (ADR-30); ..."}
```

El coeficiente `familismo_obligacion` de G5 está clasificado **`ASIGNADO`** en las tres citas (:117 explícito, :629/:899 consistentes) — la clasificación de procedencia (cómo se determinaría el valor, si existiera) es un eje distinto de si la **magnitud numérica** ya existe (`SIN MAGNITUD` en las tres citas — sigue sin número, `ruta: SIN-RUTA`). `fuerza_coeficiente` responde la primera pregunta, no la segunda. Derivación: `fuerza_coeficiente: ASIGNADO` — no `sin_coeficiente_asociado: true`, porque el coeficiente **sí existe** en el registro, con clasificación de procedencia ya fijada; lo que falta es su magnitud, pregunta que este campo no hace.

## 4 · Dos hallazgos de esta corrida — anotados, no arreglados aquí (fuera de perímetro)

**(a) `tests/test_celdas_d.py` no corre en ningún carril.** `grep -rn "test_celdas_d" .github/workflows/ tests/check.py` → vacío. Mismo patrón que `tests/test_svystat.py` antes de `ADR-62(b)` (que le dio su propio carril de CI): commiteado, pero sin nada que lo ejecute automáticamente — verde en CI no dice nada sobre si las celdas-D siguen validando. Merece su propio carril, en acto propio; no es perímetro de este acto (que ya se amplió lo mínimo necesario para no dejar el registro roto).

**(b) El validador entró al canon sin conducto declarado.** `grep -n "test_celdas_d" canon/gobernanza-v1_15.md` → vacío. `ADR-70` (que selló la remediación de la brecha documental, el mismo acto de origen de este validador) no lo menciona. Es el mismo patrón "estación 3→4 sin conducto" que la propia `PROPUESTA-remediacion-brecha-documental.md`/`ADR-70` P4 existe para cerrar ("toda nota de exploración que descubra puerta, capacidad o restricción cierra su acto subiendo la fila... o declarando por qué no") — aplicado ahora al propio aparato de esa remediación. No es perímetro de este acto corregirlo; se deja constancia.

## 5 · Qué no se tocó

`propuesta-motor-adaptativo-celda-v0_3.md` no se edita (gana banner de una línea). Ninguna otra decisión de v0.3 se reabre — M1 sigue abierta, ninguna celda-D corre, ningún contador de canon se mueve. `tools/`, `canon/`, `milpa/` intactos.
