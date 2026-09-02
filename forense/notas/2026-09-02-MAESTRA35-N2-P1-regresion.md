# P1 · F-DD v1.1 — regresión OBLIGATORIA — ACTO MAESTRA35-N2

Cambio: `tools/emite_m.py`, función `calcula_grado_DD` (antes `_RE_OLA_CAL =
^([^\s(]+)\s+(\d{4})`) extendida a la gramática de segmentos/rangos del
encargo (pieza P1(a)-(d)). Diff mínimo, solo esa sección del archivo.

## Condición (e) — identidad con `_RE_OLA_CAL` en las cadenas actuales

```
python3 -c "
import tools.emite_m as em
tests = [
 ('ENCIG', '2023', 'ENCIG 2023'),
 ('ENVIPE', '2025', 'ENVIPE 2025 (unica ola disponible para este universo)'),
 ('ENIGH', '2022', 'ENIGH 2022 (mas reciente de 6 olas bienales disponibles; las otras 5 van en serie_olas, NO promediadas)'),
 ('ENFIH', '2019', 'ENFIH 2019 (unica ola de ENFIH en el corpus)'),
 ('ENCUCI', '2020', 'ENCUCI 2020 (unica ola)'),
]
for enc,ola,cal in tests:
    old_m = em._RE_OLA_CAL.match(cal.strip())
    old_instr, old_anio = old_m.group(1), old_m.group(2)
    old_grado = 'P0 VERIFICACION' if (enc.strip().upper()==old_instr.strip().upper() and str(ola).strip()==old_anio.strip()) else 'P1 PUNTUA'
    new_grado, _ = em.calcula_grado_DD(enc, ola, 'r', 'c', cal)
    print(enc, ola, '->', old_grado, '|', new_grado, 'MATCH' if old_grado==new_grado else 'MISMATCH')
"
```
Salida: las 5 cadenas de la forma actual (`ENCIG 2023`, `ENVIPE 2025 (unica
ola ...)`, `ENIGH 2022 (mas reciente ...; las ...)`, `ENFIH 2019 (unica ola
...)`, `ENCUCI 2020 (unica ola)`) dan `MATCH` — idéntico veredicto (`P0
VERIFICACION` para las 5, todas la instrumento propio) entre `_RE_OLA_CAL`
(v1.0) y la gramática nueva.

También la transferencia de instrumento (`ENCUCI` vs `ENCIG 2023`, caso
`TRA-M-02`) reproduce `P1 PUNTUA` con `detalle="transferencia de instrumento
ENCUCI<->ENCIG"`, idéntico al de antes.

Y el caso nuevo (rango + múltiples instrumentos, `DIN-M-01`, ver P2):
`ola_calibracion` = `"ENNViH ola 2 (2005-06) -- ponderador fac_3b vive en
esta ola; ENIF 2024 -- ponderador FAC_PER (enmienda_enif2024)"`, celda
`(ENNViH/MxFLS, "2002 (ola 1)")` → `P1 PUNTUA`, `detalle="transferencia de
ola"` (instrumento ENNViH coincide, ninguna ola coincide: ola 1 de la celda
vs ola 2/año 2024 del insumo).

## `regresion()` (M-TRA-M-01/02), con el emisor YA editado

```
python3 -c "import tools.emite_m as em; print(em.regresion())"
```

Único campo que falla: `cita_p` (línea de `milpa/tramite.yaml:45` →
`:50`), **el mismo corrimiento ya documentado en P0** — no atribuible a
F-DD v1.1 (`calcula_grado_DD` no toca `cita_p`). Ningún otro campo falla;
`razon_grado_DD` coincide byte a byte con el original (se mantuvo el texto
`"(F-DD, ADR-237)"` sin renombrar a "v1.1" en el mensaje, precisamente para
no introducir una divergencia nueva). `grado_DD` es idéntico en ambas
celdas. `regresion()` devuelve `False` por el mismo motivo que en P0 (no
por F-DD v1.1) — declarado, no corregido (fuera de perímetro arreglar
`cita_p`/la propia `regresion()`).

## 13 celdas de P0, re-derivadas con el emisor NUEVO

Mismo script (`forense/notas/2026-09-02-MAESTRA35-N2-p0-script.py`),
re-corrido tras el cambio de P1. Resultado: **el conjunto de campos que
divergen es idéntico, celda por celda, al de la corrida P0** (`cita_p`,
`cita_ola_calibracion` — corrimiento de línea de `milpa/tramite.yaml`;
`archivos_abiertos` — nombre del marco por diseño de la metodología P0;
`TRA-M-02` — clave de esquema previo). **F-DD v1.1 no introduce ninguna
divergencia nueva** en ninguna de las 13 celdas: `grado_DD`,
`razon_grado_DD`, `p`, `valor_punto`, `clase`, `ola_calibracion`, y todo
otro campo sustantivo, coinciden byte a byte con lo comiteado en las 13
celdas, igual que en P0.

**Veredicto: PASA.** No hay ningún campo de valor distinto entre P0 (emisor
viejo) y esta corrida (emisor F-DD v1.1) en las 13 celdas ni en
`regresion()` — la extensión de la gramática no movió nada que no debía
mover. No se revierte P1.

## `.claude/commands/emite-m.md`

Se añade la sección `## Actualización · F-DD v1.1 (MAESTRA35-N2)` con la
gramática (a)-(d) verbatim, mismo patrón que `/arbitra` documenta
CODIFICA-R-1.
