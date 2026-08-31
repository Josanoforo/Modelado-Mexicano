# COMMIT-1 — Especificación congelada · ACTO MAESTRA32-E6 · ETIQUETA-v1_2

`forense/encargos/2026-08-30-MAESTRA32-E6-ETIQUETA-v1_2.md`, 30/ago/2026. Congelada ANTES de escribir `data/inventario-fd-v1_1.tsv`, `data/inventario-reactivos-v1_2.tsv` ni `data/emparejamiento-motor-v1_1.tsv`. El diseño de la regla (b) se validó con sondas de scratch (no en el repo, no tocan `data/`) contra `data/manifiesto.yaml` real antes de congelarla aquí — mismo patrón que `forense/notas/2026-08-27-etiqueta-regla.md` §1 ("observación de las familias antes de escribir la regla").

## 0 · Universo, re-derivado antes de escribir esta spec

```
$ python3 -c "..."  # data/inventario-reactivos-v1_1.tsv, columna instrumento
(raiz): 0
(sin-instrumento-derivable): 28799
```

Confirma la premisa 1 del encargo: cero `(raiz)` en `inventario-reactivos-v1_1.tsv` (178,246 filas). Los 28,799 placeholders `(sin-instrumento-derivable)` se reparten, por payload, exactamente en los 39 `payload_id` que `forense/notas/2026-08-27-etiqueta-regla.md:68-76` ya había descompuesto por motivo (16 `<año>trim<N>_csv.zip` + 13 `<timestamp>.export.CSV.zip` + 2 `DescargaMasivaOD_*.xml` + 3 `banxico_encuesta_competencias_financieras_*.xlsx` + 3 `cses5_*` + 1 `ucdp_ged261_csv.zip` + 1 `zenodo_electoral_*` = 39) — re-derivado por comando, no heredado del encargo:

```
$ python3 -c "..."  # payload_id distintos con instrumento == '(sin-instrumento-derivable)'
distinct payload_ids: 39
```

Capa FD: `data/inventario-fd-v1_0.tsv` (17,094 filas) trae 10 `payload_id` distintos con `instrumento == '(raiz)'`, 4,390 filas de datos:

```
Censo2020_CAAS_descriptor_bd.xlsx (259) · Censo2020_CEU_descriptor_bd.xlsx (116) ·
diccionario_cuestionario_ampliado_cpv2020.xlsx (201) · enif_2015_fd.xlsx (520) ·
enif_2018_fd.xlsx (382) · enif_2024_fd.xlsx (443) · enut2019_fd.xlsx (656) ·
enut2024_fd.xlsx (885) · fd_enadid23.xlsx (675) · fd_enif2012.xlsx (253)
```

Confirma la premisa 2: `P4_8_4` (θ de `G4.horizonte_temporal`) vive en `enif_2018_fd.xlsx`/`enif_2024_fd.xlsx`, y `P4_6_4` en esos dos más `enif_2015_fd.xlsx` (los tres con `instrumento='(raiz)'` hoy) — resolver la capa FD decide si esa θ queda con instrumento nombrado.

## 1 · (a)/(b) — las dos reglas, en el orden en que se aplican

**Orden general, por tabla:** (1) regla v1_1 (regex sobre `payload_id`, capa FD únicamente — la capa de reactivos ya la recibió completa en `MAESTRA31-E7`, 0 `(raiz)` restantes); (2) lo que (1) no resuelve pasa por la regla v1_2 (campos de `data/manifiesto.yaml`, las dos tablas); (3) lo que ninguna resuelve queda `(sin-instrumento-derivable)`.

### 1.1 · Regla v1_1 — citada tal cual, sin editar una letra

Tabla completa de `forense/notas/2026-08-27-etiqueta-regla.md` §2, en el mismo orden (primera regex que hace match sobre `payload_id`, case-insensitive, gana):

| familia | patrón |
|---|---|
| encig | `encig(\d{2,4})` |
| envipe | `envipe(\d{4})` |
| enigh | `enigh(\d{4})` |
| enif | `enif_?(\d{4})` |
| enadid | `enadid(\d{2})` |
| enestyc | `enestyc_(\d{4})` |
| enut | `enut(\d{4})` |
| encup | `encup_?(\d{4})` |
| encoap | `encoap_(\d{4})` |
| encuci | `encuci(\d{4})` |
| cpv | `cpv(\d{4})` |
| censo | `censo(\d{4})` |
| enoen | `enoen_(\d{4})` |
| enoe | `enoe_(\d{4})` |
| iter | `iter_nal_(\d{4})` |

Año de 2 dígitos expandido `20YY` si `YY<50`, si no `19YY` (misma convención que el original). Aplicada por primera vez a los 10 `payload_id` `(raiz)` de la capa FD (§0) — nunca se le había aplicado, porque el perímetro de `MAESTRA31-E7` fue solo `inventario-reactivos`.

### 1.2 · Regla v1_2 — nueva, para lo que la v1_1 deja sin resolver

**Campos del manifiesto que trae `data/manifiesto.yaml` para los 39 payloads y los 10 de la capa FD** (inspeccionados con `yaml.safe_load` antes de escribir esta regla, ninguno inventado): `id`, `usado_para`, `url_origen`, `fecha_descarga`, `descargado_por`, `sha256`, `tamano_bytes`, `formato`, `licencia`, `entorno_descarga`, y opcionalmente `nota`, `url_origen_procedencia`, `raiz`. Se buscan, en este orden de prioridad declarado (el primer campo con match gana, no se combinan candidatos de campos distintos): **`id` → `usado_para` → `nota` → `url_origen`**. Los demás campos (`archivo`, `sha256`, `tamano_bytes`, `formato`, `licencia`, `entorno_descarga`, `fecha_descarga`, `descargado_por`, `url_origen_procedencia`, `raiz`) se excluyen a propósito: o repiten el propio `payload_id`/`archivo` (no aportan información nueva) o son metadata operativa de la descarga (cuándo/quién/tamaño), no procedencia de instrumento.

**Lista cerrada de familias canónicas:** los *stems* (familia sin año) de los valores YA presentes en la columna `instrumento` de `data/inventario-reactivos-v1_1.tsv`, excluyendo los dos placeholders — re-derivada por comando, no a mano, 44 stems (`encig`, `envipe`, `enigh`, `enif`, `enadid`, `enestyc`, `enut`, `encup`, `encoap`, `encuci`, `cpv`, `censo`, `enoen`, `enoe`, `enoe_microdatos_post`, `iter`, `mociba`, `elcos`, `enfih`, `endutih`, `enasem`, `enasic`, `enbiare`, `endireh`, `engasto`, `enaproce`, `enpol`, `ensafi`, `eder`, `edr`, `enti`, y las cadenas `adq15_*`/`adqcorre_*`/`r*` de una sola familia cada una). Esta lista es más amplia que la tabla v1_1 (15 familias): v1_1 solo cubría las familias que necesitaba resolver en `(raiz)`; v1_2 usa el universo completo de instrumentos ya conocidos, tal como pide el encargo.

**Criterio de match, deliberadamente conservador (mismo espíritu que v1_1 §2):** para cada familia, en orden de longitud descendente (para que una familia más específica, p. ej. `adq15_cnbv_ahorrofinanciero_financiamiento`, no pierda contra un fragmento corto), se busca el patrón `(?<![A-Za-z0-9_])familia_?(\d{2,4})(?!\d)` (case-insensitive) — la familia debe aparecer como token completo (no dentro de otra palabra: **`identificadas` NO matchea `enti`**, verificado explícitamente durante el diseño, ver §4) e inmediatamente adyacente a un año de 2-4 dígitos, sin dígito extra pegado. Si un campo declarado cumple esto, `instrumento = familia + año4` (año expandido igual que v1_1). Si ningún campo de la prioridad §1.2 lo cumple para ningún `payload_id`, **queda `(sin-instrumento-derivable)` — no se fuerza ninguna otra heurística** (ni acrónimo inventado, ni vecino más parecido, ni conocimiento externo de qué encuesta es; ver Objeto del encargo sobre por qué leer `usado_para`/`nota` no viola esa prohibición: son campos declarados del propio programa, dato interno).

## 2 · (c) — Control positivo

Toda fila que en la tabla previa (`v1_1` para reactivos, `v1_0` para FD) ya tenía `instrumento` distinto de placeholder se compara **línea completa** contra la tabla nueva y debe ser idéntica byte a byte — cualquier diferencia es PARO. Se corre después de generar las tablas (COMMIT-2), reportado con conteo de filas comparadas y diferencias (A.13), igual que exige (c).

## 3 · (d) — Falsador

Si la regla v1_2 resuelve **menos del 50% de los 39** `payload_id` de reactivos, se reporta como hallazgo sobre `data/manifiesto.yaml` (no lleva la procedencia declarada que hacía falta para el resto), **y no se itera** — no se afloja el criterio de adyacencia, no se añaden más campos, no se amplía la lista de familias. El resultado de la primera corrida (sea cual sea) es el que se reporta.

## 4 · (e) — B-bis de la re-corrida

Re-corrida **verbatim** de `forense/notas/2026-08-28-empareja-spec.md` (términos, criterio de `CANDIDATO`/circularidad/co-observación, sin editar una palabra) sobre `data/inventario-reactivos-v1_2.tsv` + `data/inventario-fd-v1_1.tsv` en vez de `v1_1`/`v1_0`. Los 9 veredictos A.4 solo pueden moverse **hacia arriba** (`NO-ENCONTRADO → EXISTE-NO-SATISFACE → EXISTE-SATISFACE`) o quedarse — una etiqueta reparada no puede *quitar* una coincidencia que ya existía; si algún veredicto baja, es bug de este acto y PARO. **0 movimientos es un resultado informativo válido** (las etiquetas no eran el cuello de botella de los 9 pares) — no dispara PARO ni exige reintentar con otra regla. `≥1 EXISTE-SATISFACE` nuevo habilita (no lanza) un medidor sucesor en caja.

**Única desviación mecánica declarada de antemano, no descubierta después:** el script de COMMIT-2 de `MAESTRA32-E2` (`forense/notas/2026-08-28-empareja-cierre.md` §3) trae un diccionario `DESCARTES` con dos entradas clavadas al instrumento literal `"(raiz)"` (`U_POB_ELAB_CUL`, `P2_6_3` — ambas de la capa FD, ambas entre los 10 payloads de §0 que la regla v1_1 resuelve en este mismo acto). Si esas dos claves no se actualizan, dejan de matchear tras la relabeled — no porque cambie el motivo del descarte (sigue siendo homónimo de contenido: cultivo agrícola / cuidador remunerado, no carga de cuidado familiar), sino porque ya no existe ninguna fila `(raiz)` que las alcance. Se re-clavan al instrumento ya resuelto (`censo2020`, `enut2019`), con la razón original sin tocar una palabra + una nota de re-clavado — mismo movimiento, mismo precedente, que `ACTO MAESTRA31-E7` aplicó al re-correr `cruce-inverso` sobre `BD_ENCUCI2020_dbf.zip → encuci2020`. Esto no es "editar la spec de E2": ningún término, ningún criterio de candidato/circularidad/co-observación cambia; es la actualización mecánica de una clave de instrumento que la propia relabeled del acto vuelve obsoleta.

**Sello, verbatim, mismo cierre que E5/E7/E2:** «El primer resultado que produzca este procedimiento es el que se reporta.»
