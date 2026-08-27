# Perímetro alcanzable de los 30 parámetros del motor · v1.0

`ACTO MAESTRA31-E3 · PERIMETRO-ALCANZABLE`, 26/ago/2026. Encargo: `forense/encargos/2026-08-26-MAESTRA31-E3-PERIMETRO-ALCANZABLE.md` (dirección, maestra-31, archivado por A.3 antes de ejecutar).

**Universo declarado (A.10):** `origin/main = e5a36ab` (Merge PR #382), worktree propio `/home/pc0/mm-maestra31-e3-perimetro-alcanzable`. Seis censos consultados, todos re-derivados por comando propio (no se confió en la cifra de dirección): `milpa/procedencia.yaml`, `forense/censo-estimabilidad-coeficientes-v1_2.md`, `forense/cobertura-motor.md`, `data/coef-universo-v1_0.tsv`, `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv`, `forense/prereg-duelo-v2/enlace-M-v1_0.md`. Ninguno de los seis se tocó (solo lectura). No se abrió ningún payload (ver §4).

---

## 1 · Las seis cifras re-derivadas

### 1.1 · `milpa/procedencia.yaml` — 30 parámetros

Comando (conteo por sección, unidad natural de cada clase):

```
$ awk '/^medidos:/{f=1;next} /^derivados:/{f=0} f && /^  - /' milpa/procedencia.yaml | wc -l
4
$ awk '/^derivados:/{f=1;next} /^# ══/{if(f)exit} f && /^  - /' milpa/procedencia.yaml | wc -l
6
$ awk '/^asignados_probabilidad:/{f=1;next} /^# ══/{if(f)exit} f && /^  - regla:/' milpa/procedencia.yaml | wc -l
13
$ awk '/^evidencia_experimental_terceros:/{f=1;next} /^# ══/{if(f)exit} f && /^  - regla:/' milpa/procedencia.yaml | wc -l
1
$ sed -n '849,861p' milpa/procedencia.yaml | grep -c "^    - {gen:"
6
```

**4 medidos · 6 derivados · 13 asignados_probabilidad · 1 experimental_terceros · 6 asignados_coeficiente = 30.** Coincide exacto con la cifra de dirección.

**Rutas (`rutas_estimabilidad_coeficiente.detalle`, 15 filas gen×coef — NO son los 6 `asignados_coeficiente`, ver hallazgo de granularidad abajo):**

```
$ sed -n '1108,1127p' milpa/procedencia.yaml | grep -oE "ruta: [A-Z-]+" | sort | uniq -c
      3 ruta: RUTA-A
      2 ruta: RUTA-C
      1 ruta: RUTA-I
      9 ruta: SIN-RUTA
```

**3 RUTA-A · 2 RUTA-C · 1 RUTA-I · 9 SIN-RUTA = 15.** Coincide exacto con la cifra de dirección y con la línea `reparto:` declarada en el propio archivo (`procedencia.yaml:1127`).

⚠️ **Hallazgo de granularidad (nuevo, no citado por el encargo):** el conteo "30" trata `asignados_coeficiente` como **6 filas** (una por generador G1..G6, cada una con 1-4 coeficientes agrupados). El conteo "15" de rutas usa una unidad **distinta**: pares gen×coeficiente. Cruzando ambas estructuras por comando (ver `forense/notas/2026-08-26-perimetro-alcanzable-cierre.md` §1 para el script completo): de los 6 generadores, **G1, G2, G5, G6 tienen ruta uniforme** dentro de sí mismos (todos sus coeficientes caen en la misma clase de ruta), pero **G3 y G4 son MIXTOS** — G3 mezcla RUTA-I + SIN-RUTA + RUTA-A entre sus tres coeficientes; G4 mezcla RUTA-C + RUTA-C + SIN-RUTA + SIN-RUTA entre los suyos cuatro. Esto significa que **no existe una "ruta declarada" única y limpia para 2 de los 6 `asignados_coeficiente`** cuando se los cuenta como parámetros del motor (ver filas `SIN-CLASIFICAR` en §3).

### 1.2 · `forense/censo-estimabilidad-coeficientes-v1_2.md`

Reproducido por comando (herramienta declarada del propio archivo), no solo leído:

```
$ python3 tools/censo_estimabilidad.py --write $TMPDIR/censo-v1_2-repro.md
escrito: /tmp/claude-1000/censo-v1_2-repro.md
$ grep -E '^\| [0-9]+ \|' $TMPDIR/censo-v1_2-repro.md | grep -oE 'RUTA-[CIA]|SIN-RUTA' | sort | uniq -c
      3 RUTA-A
      5 RUTA-C
      1 RUTA-I
      6 SIN-RUTA
$ diff $TMPDIR/censo-v1_2-repro.md forense/censo-estimabilidad-coeficientes-v1_2.md
(sin diferencias)
```

**3 RUTA-A · 5 RUTA-C · 1 RUTA-I · 6 SIN-RUTA = 15**, byte-idéntico al archivo comprometido. Coincide exacto con la cifra de dirección.

### 1.3 · `forense/cobertura-motor.md`

El "ENTREGABLE" del propio documento declara **15 de las 49 reglas con valor numérico**, refutando explícitamente el "18/31" que `procedencia.yaml` `estado:` citaba en su momento. Coincide exacto con la cifra de dirección. **Universo distinto del de §1.1**: aquí la unidad es "regla del motor" (49 reglas de `canon/modelo-decision-v3_4.md` §3.B), no "número/parámetro de `procedencia.yaml`" (30 o 144 según el corte) — ver C3 abajo.

Control de fecha: `git log --follow --format="%h %ad %s" --date=short -- forense/cobertura-motor.md` → **un solo commit, `2026-07-31`**. El encargo cita esta fuente como "(24/ago)"; la fecha real, verificada por comando, es 31/jul/2026 — el archivo nunca se tocó de nuevo. Se reporta la discrepancia sin corregir el encargo (A.3, no se edita verbatim).

### 1.4 · `data/coef-universo-v1_0.tsv`

```
$ python3 -c "
import csv
rows = list(csv.DictReader(open('data/coef-universo-v1_0.tsv'), delimiter='\t'))
from collections import Counter
c = Counter(r['veredicto_a4'] for r in rows)
print('total filas:', len(rows))
for k,v in c.most_common(): print(k, v)
"
total filas: 58
EXISTE-SATISFACE 27
EXISTE-NO-SATISFACE 21
NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO 10
```

**27 EXISTE-SATISFACE · 21 EXISTE-NO-SATISFACE · 10 NO-ENCONTRADO(-EN-UNIVERSO-INSPECCIONADO) = 58.** Coincide exacto con la cifra de dirección (el nombre completo del tercer veredicto es más largo que "NO-ENCONTRADO" a secas; mismo valor).

### 1.5 · `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv`

```
$ awk -F'\t' 'NR>1{c[$8]++} END{for(k in c) print k, c[k]}' data/curacion-registro/cruce-oferta-demanda-v0_1.tsv
NO-ACCESIBLE 1
NO-ENCONTRADO 41
EXISTE-NO-SATISFACE 7
$ tail -n +2 data/curacion-registro/cruce-oferta-demanda-v0_1.tsv | wc -l
49
```

**0 EXISTE-SATISFACE · 7 EXISTE-NO-SATISFACE · 41 NO-ENCONTRADO · 1 NO-ACCESIBLE = 49.** Coincide exacto con la cifra de dirección.

### 1.6 · `forense/prereg-duelo-v2/enlace-M-v1_0.md`

```
$ sed -n '45,104p' forense/prereg-duelo-v2/enlace-M-v1_0.md | grep -oE '\*\*EMITE\*\*|NO-EMITE' | sort | uniq -c
      1 **EMITE**
     59 NO-EMITE
$ sed -n '45,104p' forense/prereg-duelo-v2/enlace-M-v1_0.md | grep -c "^|"
60
```

**1 EMITE (`CIV-01`) de 60, 59 NO-EMITE.** Coincide exacto con la cifra de dirección.

**Resultado del paso 1: las seis cifras de dirección se re-derivaron y las seis coinciden con el comando propio.** No hubo que corregir ningún número — el hallazgo de este acto está en cómo se relacionan las cifras entre sí (§2), no en su exactitud individual.

---

## 2 · Las tres contradicciones

### C1 · `procedencia.yaml` (2 RUTA-C · 9 SIN-RUTA) vs `censo-estimabilidad-v1_2` (5 RUTA-C · 6 SIN-RUTA)

**Veredicto: RECONCILIADA.**

`milpa/procedencia.yaml` está desactualizado. La sección `rutas_estimabilidad_coeficiente` declara explícitamente su propia fuente como obsoleta:

```yaml
rutas_estimabilidad_coeficiente:
  version_censo: "1.0"
  fuente: forense/censo-estimabilidad-coeficientes-v1_0.md
```

(`milpa/procedencia.yaml:1109-1110`). El censo avanzó de v1.0 a v1.1 el **17/ago/2026** por `ACTO RUTA-SELLO` (`ADR-89`, `canon/gobernanza-v1_15.md:1459`), que reclasificó **tres coeficientes** (los tres del generador G5: `familismo_apoyo`=N12, `familismo_obligacion`=N13, `radio_confianza`=N14) de `SIN-RUTA` a `RUTA-C`, bajo la regla "sube a RUTA-C si `relaciones.tsv` trae, para la misma necesidad, `capa4_apertura_mapeo=EXISTE-SATISFACE` + `clasificacion_relacion=CONFIRMADA`". Verificado contra el TSV real:

```
$ python3 -c "
import csv
r=[x for x in csv.DictReader(open('data/curacion-registro/relaciones.tsv'), delimiter='\t') if x['necesidad_id'] in ('N12','N13','N14')]
for row in r:
    print(row['necesidad_id'], row['capa4_apertura_mapeo'], row['clasificacion_relacion'])
" | grep -E "EXISTE-SATISFACE.*CONFIRMADA"
N12 EXISTE-SATISFACE CONFIRMADA
N13 EXISTE-SATISFACE CONFIRMADA
N14 EXISTE-SATISFACE CONFIRMADA
```

Las tres, confirmadas. `censo-estimabilidad-coeficientes-v1_2.md` (24/ago) es la misma foto de v1.1, re-derivada por herramienta (`tools/censo_estimabilidad.py`, verificado reproducible byte a byte en §1.2) en vez de escrita a mano — no reabre ninguna fila, solo verifica que el mecanismo reproduce lo ya sellado por `ADR-89`.

**Cuál está desactualizada, fecha y acto:** `milpa/procedencia.yaml` no se actualizó tras `ADR-89` (17/ago/2026, `ACTO RUTA-SELLO`) ni tras la re-verificación por comando del 24/ago (`ENCARGO CENSO-CMD`, `FP-37`). No es un número falso — es un archivo vivo que no se sincronizó con un sello ya hecho hace 9 días. `censo-estimabilidad-coeficientes-v1_2.md` es la fuente gobernante vigente para rutas de coeficientes de generador; `milpa/procedencia.yaml` no se toca aquí (fuera de perímetro — "corregir procedencia.yaml" está explícitamente prohibido; queda para un sucesor con firma, mismo criterio que el 18/31 de C3).

### C2 · `coef-universo` (27/58 EXISTE-SATISFACE) vs `cruce-oferta-demanda` (0/49) — ¿mismo universo?

**Veredicto: DOMINIOS DISJUNTOS.**

Las dos tablas comparten vocabulario A.4 (`EXISTE-SATISFACE`/`EXISTE-NO-SATISFACE`/`NO-ENCONTRADO`) y, en su subconjunto de coeficientes de generador, el mismo identificador base (`G1..G6` × nombre de coeficiente). Pero preguntan cosas **distintas** por ese identificador:

- `data/coef-universo-v1_0.tsv` (columna `universo_declarado`, ver filas N12/N13/N14 citadas arriba): pregunta si existe un **candidato de datos con el reactivo/instrumento co-observado** (exposición o desenlace) que sirva de insumo a la necesidad de estimabilidad del censo — el criterio de `RUTA-A`/`RUTA-C` del censo (§1 de `censo-estimabilidad-coeficientes-v1_0.md`: "existe un β̂ marginal ya medido" o "existe un reactivo... y un desenlace candidato"). Esto es satisfacible por una simple **asociación observacional**.
- `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv`, filas `tipo=ASIGNADO_coef` (las 15 que corresponden exactamente a los 15 gen×coef de arriba, verificado por comando):

```
$ python3 -c "
import csv
rows = list(csv.DictReader(open('data/curacion-registro/cruce-oferta-demanda-v0_1.tsv'), delimiter='\t'))
sub = [r for r in rows if r['tipo']=='ASIGNADO_coef']
print(len(sub), 'filas')
for r in sub[:2]: print(r['demanda_id'], '|', r['veredicto_A4'], '|', r['que_le_falta'])
"
15 filas
ASIGNADO_coef:G3.horizonte_temporal | NO-ENCONTRADO | magnitud empírica y escala compatible del coeficiente G3.horizonte_temporal
ASIGNADO_coef:G1.confianza_institucional | NO-ENCONTRADO | magnitud empírica y escala compatible del coeficiente G1.confianza_institucional
```

pregunta si existe un candidato que dé la **magnitud empírica en la escala compatible del coeficiente** — una elasticidad en la escala del índice del generador, no una asociación marginal en la escala arbitraria de un reactivo. Las 15 filas `ASIGNADO_coef` dan `NO-ENCONTRADO`, sin excepción.

Esto **no es un accidente de matching**: `milpa/procedencia.yaml` diagnostica la misma razón estructural, de forma independiente y anterior a este acto (`asignados_coeficiente.diagnostico`, línea 838): *"un coeficiente es una ELASTICIDAD, y el corpus es transversal — da estados, no ritmos... No existían [elasticidades] para ser citadas."* Las propias entradas de `coeficientes_generador_medidos` (G1_radio_confianza, G1_confianza_institucional, G3_familismo_apoyo, G4_*) declaran explícitamente, cada una, que su β̂ marginal **"no es comparable en magnitud"** contra el valor ASIGNADO del generador — exactamente la brecha que separa los dos criterios A.4.

**Por qué no son comparables:** `coef-universo` mide estimabilidad de una **asociación** (techo: RUTA-A); `cruce-oferta-demanda` (subconjunto `ASIGNADO_coef`) mide disponibilidad de la **magnitud en escala de coeficiente** (una elasticidad transversal que el corpus, por diseño, no produce). El 27/58 y el 0/15(de 49) no se contradicen: responden preguntas de estrictez distinta sobre el mismo vocabulario de identificadores. **Hipótesis de trabajo para C2, declarada y no cerrada por este acto:** si se necesitara un solo número "estimabilidad de los 15 coeficientes", habría que elegir explícitamente cuál pregunta se está haciendo — ese es un acto de mesa, no de este.

**No se abrió ningún payload para esta adjudicación** (ver §4) — se resolvió comparando columnas ya derivadas de las dos tablas y el diagnóstico ya escrito en `procedencia.yaml`.

**Consecuencia declarada para RANURA M-RELOJ (FP-169):** la condición de dirección es *"se reabre \[el Instrumento] si y solo si la adjudicación de C2 confirma que el cero es real (no artefacto de dominio disjunto)"*. Este acto encontró **DOMINIOS DISJUNTOS** — el cero de `cruce-oferta-demanda` en el subconjunto `ASIGNADO_coef` es explicable por comparar contra un criterio más estricto que `coef-universo`, no por un error de cómputo, pero **sí** es, por la letra literal de la condición ("no artefacto de dominio disjunto"), un caso de dominio disjunto. Bajo la lectura más defendible del texto (el paréntesis define "real" como "no artefacto de dominio disjunto"), **la condición de reapertura NO se satisface** — el Instrumento permanece sin re-especificar. Se declara esta lectura de forma explícita, con la interpretación alternativa nombrada, para que mesa la revise: es una decisión de lectura, no de fondo (ver §5, FP-169).

### C3 · `cobertura-motor.md` refutó 18/31 por escrito — ¿sigue el árbol diciendo 18/31?

**Veredicto: RECONCILIADA — y la premisa del encargo es incorrecta, no solo desactualizada.**

Búsqueda exhaustiva por comando (`command grep`, no `ugrep`) sobre 1,116 archivos `*.md`/`*.yaml`/`*.tsv`/`*.py` bajo `canon/`, `forense/`, raíz (excluyendo `.git` y `data/raw`):

```
$ command grep -rn "18/31\|18 con valor\|18 reglas.*31\|18-31" --include="*.md" --include="*.yaml" --include="*.tsv" --include="*.py" . 2>/dev/null | grep -v "^\./data/raw" | grep -v "\.git/"
```

Los únicos hits vigentes son **citas históricas** de la corrección ya hecha, no un valor vivo:

- `milpa/procedencia.yaml:107` cita `"18 con valor, 31 sin"` **dentro de la narración de su propia corrección** ("CORREGIDO 31/jul/2026 (decisión de mesa, D4): decía..."). El valor VIVO del campo `estado:` es **15 con valor, 34 sin** (líneas 103-113).
- `forense/hallazgos.md:43-44` y `canon/gobernanza-v1_15.md:447,3924` registran la misma corrección, con fecha.
- `forense/cobertura-motor.md:92,102` cita "18/31" solo para nombrar qué refuta.

**La corrección ya ocurrió — el mismo día, no "dos días después".** `cobertura-motor.md` se escribió el **31/jul/2026** (commit único `3651687`, verificado en §1.3 — no 24/ago como cita el encargo). La corrección de `procedencia.yaml` `estado:` (D4, decisión de mesa, sin ADR) es **del mismo 31/jul/2026**, citada verbatim en el propio archivo. El árbol **no** sigue diciendo 18/31 hoy, 26/ago — dejó de decirlo hace 26 días. La premisa del paso C3 del encargo ("ese estado: sigue diciendo 18/31 en el árbol dos días después") no se sostiene contra el árbol real; se reporta como hallazgo de arranque, no se corrige el texto del encargo (A.3, verbatim).

**Nota de universo, no adjudicada aquí:** `cobertura-motor.md` cuenta **reglas del motor** (49, `canon/modelo-decision-v3_4.md` §3.B); `procedencia.yaml` (§1.1 de este documento) cuenta **números/parámetros** (30 en el corte de este acto, 144 en el corte completo del archivo). Son ejes distintos — una regla puede tener 0, 1 o 2 números asociados. Esto es una tercera nota de universo-disjunto, mencionada por completitud y no adjudicada como contradicción propia porque el encargo no la nombró como tal.

---

## 3 · Estampa de universo — los 30 parámetros, fila por fila

**Universo:** `origin/main = e5a36ab`, `milpa/procedencia.yaml` (30 parámetros del corte de este acto), fuentes A.4 consultadas: `data/coef-universo-v1_0.tsv` y `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv` (solo aplican al subconjunto `asignados_coeficiente`, ver C2), ruta de estimabilidad gobernante: `forense/censo-estimabilidad-coeficientes-v1_2.md` (C1). Fecha: 26/ago/2026.

**Columnas:** clase · parámetro · ¿tiene valor hoy? · ruta declarada (fuente gobernante: censo v1.2) · veredicto A.4 de la fuente gobernante · contradicción que lo toca · **¿alcanzable?**

| # | clase | parámetro | ¿valor hoy? | ruta | veredicto A.4 | contradicción | alcanzable |
|---|---|---|---|---|---|---|---|
| 1 | MEDIDO | civico.voto.agencia_con_secreto→voto_clientelar (0.06) | Sí | N/A (fuera del alcance de la taxonomía de rutas) | N/A (fuera del universo de las dos tablas A.4) | — | **SÍ** — ya en base medida |
| 2 | MEDIDO | civico.voto.clientelar_si_observable→voto_clientelar (0.63) | Sí | N/A | N/A | — | **SÍ** |
| 3 | MEDIDO | civico.participacion.contingente→vota (0.13) | Sí | N/A | N/A | — | **SÍ** |
| 4 | MEDIDO | civico.denuncia.sin_seguro→no_denuncia (0.93) | Sí | N/A | N/A | — | **SÍ** |
| 5 | DERIVADO | civico.voto.agencia_con_secreto (0.94, complemento de #1) | Sí | N/A | N/A | — | **SÍ** — aritmética sobre un MEDIDO |
| 6 | DERIVADO | civico.voto.clientelar_si_observable (0.37, complemento de #2) | Sí | N/A | N/A | — | **SÍ** |
| 7 | DERIVADO | civico.participacion.contingente (0.87, complemento de #3) | Sí | N/A | N/A | — | **SÍ** |
| 8 | DERIVADO | civico.denuncia.sin_seguro (0.07, complemento de #4) | Sí | N/A | N/A | — | **SÍ** |
| 9 | DERIVADO | salud.vacunacion.disponible→acepta_vacuna (0.89, salto de dominio) | Sí | N/A | N/A | — | **SÍ** (con reserva de salto de dominio ya declarada en el archivo, no re-adjudicada aquí) |
| 10 | DERIVADO | (0.11, complemento de #9) | Sí | N/A | N/A | — | **SÍ** |
| 11 | ASIGNADO_PROBABILIDAD | dinero.ahorro.informal_sin_puente | Sí (juicio) | SIN RUTA declarada — la taxonomía nunca se extendió a esta clase | N/A | — | **NO** — juicio informado, sin dato que sostenga magnitud, sin ruta a base medida |
| 12 | ASIGNADO_PROBABILIDAD | dinero.ahorro.con_puente_y_respaldo | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 13 | ASIGNADO_PROBABILIDAD | dinero.planeacion.formal_estable | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 14 | ASIGNADO_PROBABILIDAD | dinero.credito.scoring_alternativo | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 15 | ASIGNADO_PROBABILIDAD | dinero.consumo.estatus_mediado_por_credito | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 16 | ASIGNADO_PROBABILIDAD | salud.atencion.leve_sin_imss | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 17 | ASIGNADO_PROBABILIDAD | salud.atencion.grave | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 18 | ASIGNADO_PROBABILIDAD | salud.prevencion.hombre_sin_permiso | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 19 | ASIGNADO_PROBABILIDAD | tramite.mordida.discrecional | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 20 | ASIGNADO_PROBABILIDAD | tramite.mordida.con_registro | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 21 | ASIGNADO_PROBABILIDAD | tramite.gobierno_digital.coercitivo | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 22 | ASIGNADO_PROBABILIDAD | tramite.gobierno_digital.util_sin_coercion | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 23 | ASIGNADO_PROBABILIDAD | civico.denuncia.con_seguro | Sí (juicio) | SIN RUTA | N/A | — | **NO** |
| 24 | EVIDENCIA_EXPERIMENTAL_TERCEROS | dinero.credito.baja_friccion_usura_dano_downstream | Sí (evidencia de terceros) | fuera de la taxonomía RUTA-A/C/I/SIN-RUTA (octava clase, mecanismo distinto) | N/A | — | **SIN-CLASIFICAR** — la evidencia (RCT Compartamos, `ADR-204`) corrobora dirección del mecanismo; no calibra la magnitud vigente de la regla (`procedencia.yaml:824`, verbatim: "NO calibra ni sustituye la magnitud"). Ni "tiene ruta" ni "no tiene ruta" describe esto limpiamente — no se fuerza |
| 25 | ASIGNADO_COEFICIENTE | G1 (confianza_institucional, radio_confianza) | Sí (juicio, magnitud sin sostener) | **RUTA-A** (uniforme en G1, ambos coeficientes) | `coef-universo`: 3 EXISTE-SATISFACE·3 EXISTE-NO-SATISFACE (asociación); `cruce-ASIGNADO_coef`: 2/2 NO-ENCONTRADO (escala compatible) | C1 (ruta ya estable en v1.0→v1.2, no cambió), C2 (los dos veredictos A.4) | **SÍ** — RUTA-A es la ruta más fuerte de la taxonomía (asociación ya corrida) |
| 26 | ASIGNADO_COEFICIENTE | G2 (sens_estatus, aversion_riesgo) | Sí (juicio) | **SIN-RUTA** (uniforme en G2) | `coef-universo`: 4 NO-ENCONTRADO·2 EXISTE-NO-SATISFACE; `cruce-ASIGNADO_coef`: 2/2 NO-ENCONTRADO | C2 | **NO** |
| 27 | ASIGNADO_COEFICIENTE | G3 (horizonte_temporal, aversion_riesgo, familismo_apoyo) | Sí (juicio) | **MIXTO** — RUTA-I (horizonte_temporal) + SIN-RUTA (aversion_riesgo) + RUTA-A (familismo_apoyo), sin cambio v1.0→v1.2 | `coef-universo`: 1 EXISTE-SATISFACE·1 EXISTE-NO-SATISFACE; `cruce-ASIGNADO_coef`: 3/3 NO-ENCONTRADO | C1 (granularidad), C2 | **SIN-CLASIFICAR** — la fila-generador mezcla tres rutas distintas; no cae limpio como una sola respuesta SÍ/NO |
| 28 | ASIGNADO_COEFICIENTE | G4 (exposicion_violencia, confianza_institucional, horizonte_temporal, sens_estatus) | Sí (juicio) | **MIXTO** — RUTA-C + RUTA-C + SIN-RUTA + SIN-RUTA, sin cambio v1.0→v1.2 | `coef-universo`: 15 EXISTE-SATISFACE·6 EXISTE-NO-SATISFACE·2 NO-ENCONTRADO; `cruce-ASIGNADO_coef`: 4/4 NO-ENCONTRADO | C1 (granularidad), C2 | **SIN-CLASIFICAR** — mismo motivo que #27 |
| 29 | ASIGNADO_COEFICIENTE | G5 (familismo_apoyo, familismo_obligacion, radio_confianza) | Sí (juicio) | **RUTA-C** (uniforme en G5 **bajo censo v1.2**; era SIN-RUTA uniforme bajo `procedencia.yaml`/v1.0 — este es el corazón de C1) | `coef-universo`: 8 EXISTE-SATISFACE·4 EXISTE-NO-SATISFACE·1 NO-ENCONTRADO; `cruce-ASIGNADO_coef`: 3/3 NO-ENCONTRADO | **C1** (la reclasificación misma), C2 | **SÍ** — RUTA-C es candidata con instrumento identificado (bajo la fuente gobernante, censo v1.2); no llega a RUTA-A/I pero no está SIN-RUTA |
| 30 | ASIGNADO_COEFICIENTE | G6 (deferencia) | Sí (juicio) | **SIN-RUTA** (uniforme en G6) | `coef-universo`: 5 EXISTE-NO-SATISFACE·2 NO-ENCONTRADO; `cruce-ASIGNADO_coef`: 1/1 NO-ENCONTRADO | C2 | **NO** |

### Conteo final

| Alcanzable | # de parámetros | Filas |
|---|---|---|
| **SÍ** | **12** | 1-10 (MEDIDO+DERIVADO), 25 (G1), 29 (G5) |
| **NO** | **15** | 11-23 (ASIGNADO_PROBABILIDAD), 26 (G2), 30 (G6) |
| **SIN-CLASIFICAR** | **3** | 24 (experimental_terceros), 27 (G3), 28 (G4) |
| **Total** | **30** | — |

## **N = 12 de 30 alcanzables**

**Universo declarado en la misma línea (A.10):** `origin/main = e5a36ab`; censos consultados: `milpa/procedencia.yaml` (30 parámetros, definición de clase), `forense/censo-estimabilidad-coeficientes-v1_2.md` (ruta gobernante, C1), `data/coef-universo-v1_0.tsv` + `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv` (veredicto A.4, dominios disjuntos, C2); fecha 26/ago/2026. **Denominador explícito: 30** (el corte de `procedencia.yaml` que dirección declaró, no los 144 números totales del archivo — ver §2 nota de C3 sobre el eje distinto de 49 reglas).

**"Alcanzable" definido por este acto (elección interpretativa, declarada para que mesa la revise, no forzada como canon):** un parámetro es alcanzable si **ya está en base medida** (MEDIDO/DERIVADO, 10 de 30) **o** tiene una **ruta declarada distinta de SIN-RUTA** bajo la fuente gobernante (RUTA-A o RUTA-C uniformes, 2 de 30: G1 y G5). No se cuenta como alcanzable el juicio puro sin ruta (ASIGNADO_PROBABILIDAD, 13) ni las rutas SIN-RUTA uniformes (G2, G6). **3 quedan SIN-CLASIFICAR** por diseño (no se fuerza una respuesta limpia donde el propio dato es mixto o de otro tipo): dos filas-generador con rutas mezcladas entre sus coeficientes (G3, G4) y la octava clase de evidencia experimental de terceros, que corrobora dirección de mecanismo sin calibrar magnitud.

---

## 4 · Payload abierto

**Ninguno.** La adjudicación de C2 se resolvió comparando columnas ya derivadas de `data/coef-universo-v1_0.tsv`, `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv` y el diagnóstico ya escrito en `milpa/procedencia.yaml` (`asignados_coeficiente.diagnostico`, línea 838) — ninguna pregunta de este acto requirió abrir microdato crudo.

---

## 5 · Los tres hallazgos de las últimas 48h — ¿una sola cosa medida por separado?

El contexto del encargo pregunta si "M emite 1 de 60", "el cruce da 0 de 49" y "la palanca #1 da 0 de 8" **podrían ser una sola cosa medida por separado**. Con el dato de este acto: **no exactamente la misma cosa, pero sí la misma familia de causa.**

- `enlace-M-v1_0.md` (1/60 EMITE) mide si existe una **cita real `(regla, conducta)`** que un candidato pueda ejercer contra las 5 reglas de `milpa/tramite.yaml` — un problema de **enlace/crosswalk**, no de disponibilidad de dato.
- `cruce-oferta-demanda` (0/49, y específicamente 0/15 en el subconjunto `ASIGNADO_coef`) mide si existe una **magnitud en escala de coeficiente/elasticidad** — un problema de **disponibilidad de dato en la escala correcta** (C2 de este acto).
- La palanca #1 (`disparador_sin_base:riesgo_fiscal_percibido`, 0/8, `ADR-210`) es un caso particular de `cruce-oferta-demanda` (`tipo=disparador_sin_base`), mismo mecanismo que el punto anterior.

Los dos últimos **sí son la misma cosa** (ambos son filas del mismo TSV, mismo mecanismo de censo). El primero (`M`) es un problema **distinto y anterior** en la cadena: antes de preguntar si hay magnitud en escala, `M` pregunta si hay siquiera una regla del motor a la que amarrar la variable. Los tres comparten la causa raíz de fondo (el motor v4.0 tiene mucho más aparato declarado — 30 parámetros, 49 reglas, 60 celdas del duelo — que evidencia empírica en la forma exacta que cada capa exige), pero no son la misma medición repetida tres veces; son tres compuertas distintas de la misma tubería, cada una capturando una fase distinta del embudo.
