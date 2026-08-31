# Nota de cierre · ACTO MAESTRA32-E9 · PROPAGA-2

Encargo: `forense/encargos/2026-08-30-MAESTRA32-E9-PROPAGA-2.md` (dirección, maestra-32, 30/ago/2026, archivado por A.3 antes de ejecutar; redactado contra `main = 1f455ea`, merge de PR #395). Entorno **NUBE** (`cloud_default`); `data/raw` ausente, no usada, no necesaria; sin red, sin API, sin microdato. Acto de propagación (SELLA-3, `ADR-76`/`ADR-79`): sin falsador, sin ranuras — las siete firmas venían dadas verbatim.

## 0 · ARRANQUE (las cinco líneas)

1. **REPO** — clon existente en `/home/user/Modelado-Mexicano`, no se clonó ninguno nuevo. `git log -1`: `1f455ea Merge pull request #395 from Josanoforo/claude/maestra32-e6-cloud-launch-8qu0hw`. `git status` al arrancar: rama `claude/maestra32-e9-launch-55zzlu`, árbol limpio.
2. **SHA** — coincide exacto con lo que el encargo declara (`main = 1f455ea`). Sin diferencia que resolver.
3. **data/raw** — ausente, como se esperaba (`ls data/raw` → `No such file or directory`); `ls data/raw/ 2>/dev/null | head -1` (A.2, tercera parte) → vacío (0 archivos examinados por ese comando). No se creó ni se enlazó: este acto no abre ningún payload.
4. **ENTORNO** — este acto no toca microdato ni red. Sonda corrida igual por completitud, mismo tratamiento no-discrepante que `E2`/`E5`/`E6` ya dieron: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (coincide con "ENTORNO ASIGNADO: NUBE" de la cabecera del encargo). `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `000` (sin conexión). Regla A.13 v2.11: el comando que produjo este negativo es un `curl`, examinó **0 archivos** — declarado explícitamente; el punto no gobierna nada de este acto.
5. **ESPEJO** — ninguna cifra de este documento se derivó del espejo del proyecto. Toda cifra sale de comandos corridos contra el clon de (1), reproducidos abajo.

## 1 · Verificación contra el árbol antes de escribir

Los tres puntos de la VERIFICACIÓN DE EXISTENCIA de dirección se re-derivaron por comando, no se heredaron del texto:

- **1 · ESTRUCTURA** — las cuatro tablas gobernantes existen: `forense/firmas-pendientes.tsv` (176 filas, `csv.DictReader`), `canon/gobernanza-v1_15.md`, `milpa/procedencia.yaml` (secciones `coeficientes_generador_sellados` y `rutas_estimabilidad_coeficiente.detalle`), `tests/test_matriz_sellados.py`. Confirma.
- **2 · CONTENIDO** — (i) tablero hoy: `FP-168/171/173/174/178/179` `ABIERTA`, `FP-169` `FIRMADA-PARCIAL`, `FP-180` `ABIERTA` (no tocada) — confirma exacto. (ii) `coeficientes_generador_sellados`: 5 entradas, 3 con `valor_ejecutable` (`G1.confianza_institucional`, `G3.familismo_apoyo`, `G4.exposicion_violencia`), ninguna para `G3.horizonte_temporal` — confirma, `NO-ENCONTRADO`. (iii) El β vive en `forense/notas/2026-08-24-cal-g3-puntual-cierre.md:112-113` (tabla) y `:36` (θ) — confirma línea a línea. (iv) `FP-179(5)` texto verbatim — confirma; `ADR-134` (`canon/gobernanza-v1_15.md:2679`) la ejecutó, `0` de `8` `EXISTE-SATISFACE`.
- **3 · COBERTURA RETROACTIVA** — confirma: el barrido de escalas del 25/ago (`ACTO ESCALAS-COMPLETAS-P1`) buscó θ en `condicionales_escalares*` y no la encontró para `horizonte_temporal`; la fuente real vive en la corrida CAL (`pr02`), fuera de ese barrido. `rutas_estimabilidad_coeficiente.detalle` fila G3/horizonte_temporal traía `escala_derivada: SUBDETERMINADA-PERSISTENTE` por esa razón exacta, verificado leyendo el campo completo (no truncado).

Sin discrepancias entre lo que el encargo supone y el terreno real — no hay PARO que reportar en el arranque.

## 2 · Paso 1 — tablero (mismo commit que lo que propaga, A.12)

`forense/firmas-pendientes.tsv`, editado por script (`csv.DictReader`/`csv.writer` de campo, nunca reserializando el archivo completo — el archivo mezcla filas con y sin *quoting* RFC4180 y una reserialización total habría reformateado 176 filas no tocadas; verificado antes y después con un `diff` fila por fila contra `HEAD`, 0 discrepancias en filas no objetivo):

- `FP-168` → `FIRMADA` (F1): `nivel_ic=0.95`, `seed=42`, cita verbatim de mesa.
- `FP-169` → `FIRMADA` (de `FIRMADA-PARCIAL`, F2): append sobre `firmada_en`, cita verbatim "D2 - Ratificadas."
- `FP-171`/`FP-173`/`FP-174`/`FP-178` → `FIRMADA` (F3): cita verbatim "3 Enterado." en cada una.
- `FP-127.ejecutada_en`: append "Superada por firma b1 (30/ago), ver ADR-224." (F5).
- `FP-179.qué_se_firma`: enmienda fechada append-only sobre la entrada (5) — `CONSUMIDA-PREEXISTENTE` por `ADR-134` (+`ADR-194`/`198`), error de dirección 30/ago (F6). Texto original de las cinco entradas intacto.
- `FP-181` nueva (`ABIERTA`): "mesa recibe la entrada CAL-G3 en el ejecutable (F5) con su escala declarada" — informativa, no gatea nada.

Total: 176 → 177 filas. Verificado por `csv.DictReader` antes/después: las 176 filas preexistentes que no son objetivo de este acto son idénticas byte a byte a `HEAD` (comparación de diccionario completo, 9 columnas, 0 discrepancias).

## 3 · Paso 2 — F5 al ejecutable, por script

**2a · Orden de pre-registro, verificado por `git log`, no asumido.** `canon/gobernanza-v1_15.md`, `ADR-157`, confirma que `ACTO CAL-G3-PUNTUAL` congeló θ/desenlace antes de correr. El `git log` de la nota de cierre lo confirma con dos commits separados y timestamps:

```
$ git log --format="%h %ad %s" --date=iso-strict -- forense/notas/2026-08-24-cal-g3-puntual-cierre.md
8cfe8ce 2026-08-24T21:19:43-06:00 Merge remote-tracking branch 'origin/main' into acto/cal-g3-puntual
93199a6 2026-08-24T20:31:25-06:00 ACTO CAL-G3-PUNTUAL, Commit 2: corrida (PASO 2) -- CAL-G3 EJERCIDA_ACOTA, 3 de 3
b16ffe1 2026-08-24T20:30:57-06:00 ACTO CAL-G3-PUNTUAL, Commit 1: PASO 0 (AGOTADO) + spec B-bis congelada (PASO 1)
```

`b16ffe1` (Commit 1: PASO 0 + spec congelada) precede a `93199a6` (Commit 2: corrida) por 28 segundos. Pre-registro ciego confirmado — no hay PARO que reportar.

**2b · Lectura.** Líneas crudas del cierre CAL (`forense/notas/2026-08-24-cal-g3-puntual-cierre.md`):

- `:36` — "θ (generador `G3 → horizonte_temporal`) = `pr02` recodificada 1-7 (entero, mayor = horizonte más largo), dominio restringido a las 7 categorías sustantivas; `8` y `98` se excluyen del universo analítico (declarado, no imputado)."
- `:112-113` (tabla) — β propuesto `+0.0146` (IC95% `[+0.0047, +0.0245]`, HC1/MAS; `[+0.0056, +0.0248]` bootstrap-hogar); escala "pp de probabilidad de 'tener ahorros' por punto de categoría ordinal de horizonte temporal (`pr02`, 1-7), primeras diferencias intra-persona, ENNViH olas 2-3 (2005-06 → 2009-12)".

**2c · Enlace de escala — declarado por dirección, no firmado por mesa.** θ = `pr02` (1-7) se reescala linealmente a `[0,1]` como `(pr02 − 1)/6`. Bajo un modelo lineal en θ: `valor_ejecutable = β × 6`, `ic = IC × 6`:

```
β × 6      = 0.0146 × 6  = 0.0876
IC HC1/MAS × 6  = [0.0047×6, 0.0245×6] = [0.0282, 0.1470]
IC bootstrap × 6 = [0.0056×6, 0.0248×6] = [0.0336, 0.1488]
```

`valor_origen`/`unidad_origen` quedan verbatim ("pp por punto ordinal 1-7"). Alternativa no tomada: dicotomizar `pr02` sería post-hoc sobre un resultado ya visto.

**2d · Escritura.** Verificado antes de escribir: `coeficientes_generador_sellados` era la última clave raíz del archivo (línea 1210 de 1259) — no se re-serializó el YAML, se usó `Edit` de texto anclado al final del archivo. Entrada añadida (verificada con `yaml.safe_load` después de escribir):

```
gen: G3, coef: horizonte_temporal
valor_ejecutable: 0.0876
ic: IC95% +0.0282,+0.1470 HC1/MAS; +0.0336,+0.1488 bootstrap-hogar
rotulo: ASOCIACION-MEDIDA·CAL·INTRA-PERSONA·SIGNO-OPUESTO-AL-ASIGNADO
```

`rutas_estimabilidad_coeficiente.detalle`, fila G3/horizonte_temporal: `escala_derivada` recibió append-only ("Paso 3 (30/ago/2026, ADR-224): θ con fuente = `pr02` ..., deja de ser SUBDETERMINADA-PERSISTENTE"). Comparación de los dos dicts (`yaml.safe_load` antes/después, `old_detalle` vs `new_detalle` por clave `(gen, coef)`): **un solo campo cambió, en una sola fila** (`('G3', 'horizonte_temporal')`, campo `escala_derivada`) — ninguna otra fila ni ningún otro campo se movió.

**2e · Test y suite.**

```
$ python3 tests/test_matriz_sellados.py
  test_fallback_intacto_para_los_nueve_sin_medicion: ok
  test_multi_item_no_se_consume: ok
  test_no_rompe_conteos_globales_de_b: ok
  test_override_para_los_cuatro_uni_valor: ok
  test_quince_celdas_sin_cambio_de_conteo: ok
  test_universo_cuatro_mas_dos: ok
T-MATRIZ-SELLADOS: 6 prueba(s) ok, 0 saltada(s)
```

Universo re-derivado contra el árbol de hoy (E8/carril CAJA no había fusionado al momento de escribir — `coeficientes_generador_sellados` seguía con 5 entradas antes de este acto, no 7): `3 → 4` pares uni-valor con `valor_ejecutable`, `2` multi-ítem sin cambio, `10 → 9` pares en fallback puro (15 pares totales, sin cambio).

```
$ python3 tests/check.py --baseline
19 FAIL · 136 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
(5 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

Las 5 entradas que dejan de aparecer son consecuencia directa del Paso 1 (las filas `FP-168/169/171/173/174/178` que salían como `ABIERTA`/`FIRMADA-PARCIAL` en `T22` bajan de antigüedad al firmarse) — mejora, no se fuerza con `--freeze`.

## 4 · Paso 3 — ADR y cascada

`canon/gobernanza-v1_15.md`: candidato re-derivado por comando (`grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1` → `223`, sin huecos) → **`ADR-224`**, contiguo; sin colisión detectada al momento de escribir (el carril CAJA, `E3`/`E8`, no había fusionado). `ADR-224` trae F1-F7 verbatim, el enlace de escala 2c con la frase "declarado por dirección, no firmado por mesa", el retiro de `E7 · CANDIDATOS-MARCO-M` (su objeto era la opción (ii) de D1; mesa firmó (i)), y la corrección F6 con cita a `ADR-134`. Cabecera de conteo del documento: `223 → 224 ADR`.

`canon/estado-programa-v1_10.md`: recifrado `L0` (`223 → 224`), nota nueva prepend antes de la de `ADR-223`; tabla de canon (`§L2`) recifrada `223 → 224`; conteo de ejecutables con base medida `3/15 → 4/15`, derivado del test, no tecleado.

`canon/registro-rotulos.tsv`: fila nueva `MAESTRA32-E9` — token pelado `E9` colisiona con `MAESTRA31-E9 · ESTIMA-RUTAC` (censado, ninguno gana, mismo patrón que `M5`); se censa, no se reclama.

`tests/check.py` `_T25_ARCHIVOS_CONOCIDOS`: encargo y esta nota de cierre añadidos (traen `E9`/`E10`/`E8`/`E3`/`E7`/`E6`/`E4`/`E2` pelados, todos referencias narrativas a actos ya censados o al propio acto declarándose).

`python3 tests/check.py --baseline` final, con el ADR y la cascada ya escritos: **19 FAIL · 136 WARN, LÍNEA BASE VERDE**, sin `--freeze`.

## Contador

Firmas propagadas: **7 filas** (`FP-168`, `FP-169`, `FP-171`, `FP-173`, `FP-174`, `FP-178`, `FP-127`). Correcciones de dirección registradas: **2** (`FP-179(5)`, retiro de `E7`). Coeficientes ejecutables con base medida: **`3 → 4` de 15** (derivado del test).

## Cierre

- Nota: este archivo.
- `forense/encargos/2026-08-30-MAESTRA32-E9-PROPAGA-2.md`: `CONSUMIDO`, ver `## CONSUMIDO` al pie con el PR.
- `forense/firmas-pendientes.tsv`: siete filas propagadas, `FP-181` nueva.
- `milpa/procedencia.yaml`: una entrada nueva en `coeficientes_generador_sellados`, un campo (`escala_derivada`) append-only en `rutas_estimabilidad_coeficiente.detalle`.
- `tests/test_matriz_sellados.py`: universo re-derivado, 6/6 pruebas ok.
- `canon/gobernanza-v1_15.md`: `ADR-224`.
- `canon/estado-programa-v1_10.md`: `L0` y tabla de canon recifrados.
- `canon/registro-rotulos.tsv`: `MAESTRA32-E9` censado.
- `tests/check.py`: `_T25_ARCHIVOS_CONOCIDOS` ampliado.
- **No tocó**: la sección A de `milpa/procedencia.yaml`, ningún `ASIGNADO`, `milpa/src/matriz.py`, `forense/prereg-duelo-v2/scoring-adv1-m3.py`, el marco congelado, nada de `MAESTRA32-E10`. No lanzó `E3` ni `E8` (carril CAJA, ya listos y firmados por separado).
- Sucesores declarados, no lanzados: `MAESTRA32-E10 · COBERTURA-15` (mismo carril, tras este merge); `E3`/`E8` en caja; `E4 · RE-EMPAREJA` tras extractores.
