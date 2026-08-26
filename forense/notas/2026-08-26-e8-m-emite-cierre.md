# Nota de cierre · ACTO MAESTRA30-E8 · M-EMITE-Y-RESELLO

26/ago/2026. Ejecuta los caminos (ii)+(iv) de la RANURA de `FP-166`, sobre
`main` en `efd443b` (merge de `PR #378`, `acto/e7-r-scoring`). Entorno
**NUBE** (`cloud_default`, repo-only) — determinista, cero API, cero
microdato.

## Compuerta cero

- `PR #378` **fusionado**: `git log -1 --format="%h %s"` → `efd443b Merge
  pull request #378 from Josanoforo/acto/e7-r-scoring`. La rama de trabajo
  de este acto ya arrancó igualada a `main` (mismo SHA), sin necesidad de
  reconciliar divergencia.
- RANURA de mesa presente y leída, verbatim en el encargo.
- Tres hits de subcadena de `DERIVACION-M-v1_0.md` (líneas 26-28),
  reproducidos:
  - `DIN-03`/ENIF/`P7_1` → `AP7_1` de ENCUCI (`procedencia.yaml:468`) y
    `P7_12_7` de ENASIC (`:504,:527`).
  - `DIN-11`/ENIF/`P5_3` → `AP5_3_XX` de ENVIPE 2025 (`:231`) y
    `AP5_3_6/7/8` de ENCUCI 2020 (`:254`).
  - `TIC-06`/ENTI/`P2` → la cadena documental `(P2 §2.d)` (`:298,:317`).

## data/raw, entorno, espejo (ARRANQUE)

`data/raw` ausente, esperado en un clon fresco — este acto no la toca.
`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (NUBE, correcto). La
sonda `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10
https://www.inegi.org.mx/` devolvió `000` — **0 archivos examinados por
ese comando** (A.13): no es un negativo sustantivo, es el sandbox de shell
sin salida a ese host; este acto no toca red de verdad y no lo necesita.
Ninguna cifra de este acto sale del espejo del proyecto — todas del clon
de `/home/user/Modelado-Mexicano`, comando a la vista en cada sección de
abajo.

## Paso 2 · `construir_crosswalk` reparado

`milpa/src/emisor.py:485-529` (antes `486-508`): el emparejamiento exigía
solo `if var and var in l` — subcadena, sin comparar `encuesta`. Ahora
exige **encuesta** (acrónimo, primer token antes de espacio/paréntesis/
slash) **en la misma línea** que la **variable por token exacto** (no
subcadena, frontera `(?<![\w])...(?![\w])`).

Verificado con un script equivalente antes de tocar el código fuente
(reproducido después con la función real):

```
$ python3 -c "
from pathlib import Path
from milpa.src.emisor import construir_crosswalk
n = construir_crosswalk(Path('/tmp/crosswalk_v1_1_body.tsv'))
print('rows:', n)
"
rows: 60
$ grep -c CANDIDATO-EMITE /tmp/crosswalk_v1_1_body.tsv
3
```

Sobre las 60 filas: **3 `CANDIDATO-EMITE`** (`CIV-01`, `CIV-06`, `CIV-07`)
/ **57 `NO-EMITE`** — antes 10/50. Sobre las **15 sorteadas** (`CIV-08,
DIN-03, DIN-05, DIN-07, DIN-11, DOC-06, EMP-02, EMP-04, EMP-05, SFT-04,
SFT-06, TIC-01, TIC-06, TIC-08, TIC-12`, derivadas por `ls
forense/prereg-duelo-v2/corridas-L | sed 's/__.*//' | sort -u`): **0
`CANDIDATO-EMITE`** — los tres falsos positivos de v1_0 caen a `NO-EMITE`
y ninguna de las tres celdas nuevas (`CIV-01/06/07`) pertenece a la
muestra de 15.

Test nuevo: `tests/test_crosswalk_encuesta.py` — 6 casos (helpers
unitarios, los tres falsos positivos fijados como negativos, `CIV-01`
fijado como positivo de control). Suite de `emisor`: **13/13** pasan
(`python3 -m pytest tests/test_crosswalk_encuesta.py
tests/test_emisor_fidelidad.py tests/test_emisor_m2.py -q`).

## Paso 3 · Enlace `SpecCelda → (regla, conducta)`

`forense/prereg-duelo-v2/enlace-M-v1_0.md` (nuevo), pasada declarada sobre
las **60** filas del marco, no solo las 15. Método: de las 3
`CANDIDATO-EMITE` de pasada 1, solo se acepta la que cita una regla real de
`milpa.src.emisor.cargar_reglas()` (las 5 reglas de `milpa/tramite.yaml`,
el único motor que `emitir_binaria` consulta) **y** `procedencia.yaml` la
declara desenlace medido (no `ASIGNADO`, no transporte fuera de dominio)
de esa regla. Resultado: **`CIV-01` → EMITE**
(`regla=tramite.mordida.discrecional`, `conducta=paga_mordida`,
`procedencia.yaml:937`, join ENCIG 2023 `P11_1_23`×`P8_3_1/2/3` por
`ID_PER`, `n=38966`, cero pérdida — escala binaria `[0,1]`, universo
declarado). `CIV-06` y `CIV-07` (`CANDIDATO-EMITE` de pasada 1 sin cita
real) y `CIV-12` (declara explícitamente transportar
`tramite.mordida.discrecional` fuera de su dominio) quedan `NO-EMITE`.

**Resultado: 1 EMITE de 60, 0 EMITE de las 15 sorteadas.** Cero honesto,
no forzado — la RANURA autoriza exactamente esta salida si M sigue en 0
tras la pasada real, y no se inventó ningún enlace donde el motor carece
de regla.

## Paso 4 · Crosswalk v1_1

`forense/crosswalk-pregunta-regla-v1_1.tsv` (nuevo, `v1_0` intacto, no
editado, cabecera de superación con fecha y `ADR-208`): re-derivado con la
función corregida, mismos números que el paso 2.

## Paso 5 · Enmienda F1 del scoring

`forense/prereg-duelo-v2/scoring-adv1-m3.py`: solo se tocó
`validar_configuracion` (roles obligatorios/opcionales, `e_id` condicional)
y la anotación de tipo de `Configuracion.e_id` (`str` → `str | None`).
Contrato nuevo: mínimo obligatorio `{(L,solo):1, (M,principal):1}`;
`(L,corpus)` y `(E,combinacion)` opcionales (0 o 1); cualquier rol fuera de
ese conjunto se rechaza explícitamente; `e_id` solo obligatoria si hay
`E` activo. `B` ya se reportaba `no evaluable` cuando falta
`error_baseline` (`_skill_de_medicion`, sin cambio) — consistente con las
9 celdas arbitrables `publicada=NO` (`FP-93`, `NO-ENCONTRADO`).

Verificado con configuraciones sintéticas (no se corre el scoring real —
prohibido, es `E9`):

- `{L-solo, M-principal}` con su par `comparaciones_l_m` → valida,
  `e_id=None`.
- Contrato viejo de 4 corredores (`L-solo, L-corpus, M-principal,
  E-combinacion`) → sigue validando sin regresión.
- Rol desconocido (`M/auxiliar`) → sigue rechazado.
- `e_id` presente sin corredor `E` activo → rechazado.
- Corredor `M-principal` ausente → sigue rechazado.

`sha256` viejo `beec0e1c2e86605bb751601a36c312e34ade4a82a8204e0ab96527beba8e0efb`
→ nuevo `63418cc8cfdb03ba5d851d01f1bba23e2f21dbac5cfbed2d88c2832cba13a8cf`,
registrado en `prereg-corrida-v1_0.md` bajo `## F1 · enmienda 2026-08-26`
(regla de enmienda de `prereg-corrida:110`, no de silencio).

## Paso 6 · Dos correcciones de pasada

**(a)** `marcador-piloto-v1_0.md` **no se toca**. Su línea 58 dice que la
constante `0.5` de la banda TOST «no está firmada por mesa (`FP-163` sigue
abierta)» — desactualizado: `firmas-pendientes.tsv` tiene `FP-163`
**FIRMADA** desde `ADR-199` (`hitoD-preregistro-v2_0.md` §L3, firma L3
verbatim «FIRMO FP-163: ...»). v1.1 (`E9`) lo dirá bien.

**(b)** `lanzamiento-L-v1_0.md` §5: enmienda fechada insertada justo
después del texto viejo (intacto, no editado), corrigiendo la afirmación
de que `agregar_continua`/`agregar_categorica` son «las únicas funciones
que derivan `valor_extraido`» — materialmente falsa, tal como
`ACTO MAESTRA30-E6 · L-RUN` (`forense/notas/2026-08-26-l-run-cierre.md`
§9.1, líneas 317-442) ya lo reportó: ambas reciben listas ya extraídas y
solo agregan; el pipeline pre-registrado no contiene extractor alguno.

## Paso 7 · Cierre

`FP-166` → **FIRMADA** (`firmas-pendientes.tsv`), `firmada_en` = RANURA
verbatim, `ejecutada_en` = `ADR-208`. Tablero: `1` → `0` `ABIERTA`
(`awk -F'\t' 'NR>1{print $6}' forense/firmas-pendientes.tsv | sort |
uniq -c` → 0 `ABIERTA` tras el cambio). `ADR-208` candidateado contra el
máximo re-derivado por conteo entero (`grep -roE "ADR-[0-9]+" . | sed
's/.*ADR-//' | sort -n | uniq | tail -1` → `207`, sin huecos) → `208`.
Recifrado: cabecera de `gobernanza-v1_15.md` (207→208 ADR), tabla `§0` y
`§L0` de `canon/estado-programa-v1_10.md`; las dos citas históricas de
`ADR-207` que quedaron desincronizadas (`207 ADR`, `19 FAIL · 128 WARN`)
se marcaron `{cita-historica}` (mismo mecanismo que T15/T16 ya reconocen,
usado antes por `ADR-72`/`ADR-206`).

`tests/check.py --baseline`: **19 FAIL · 127 WARN, LÍNEA BASE VERDE**
(cinco entradas de la línea base ya no aparecen — mejora, no se bajó la
cifra congelada sin `--freeze` explícito). Dos ajustes mecánicos dentro de
perímetro para llegar ahí: `firmas-pendientes.tsv` (`FP-166`, columna
`dónde`) gana la cita de los archivos nuevos de este acto para satisfacer
`T22`; `enlace-M-v1_0.md`, el encargo archivado y esta misma nota traen
los rótulos pelados `E7`/`E8`/`E9` de la serie de dirección (maestra-30)
— censados en `tests/check.py` (`_T25_ARCHIVOS_CONOCIDOS`) con el mismo
patrón que `E4`/`E5`/`E6`, en vez de reescribir el texto de dirección
para complacer `T25`.

## Lo que este acto NO hace

No corre `M`, `R`, `B` ni `scoring` — es `E9`, sucesor gated a
este, en UBUNTU. No toca `marco-congelado-piloto-v1_0.tsv`, `ADR-141`, el
marcador v1.0 (archivado tal como está), `corridas-L/` ni `corridas-R/`.
No usa red ni API. No inventa un enlace donde el motor no tiene regla.

## Perímetro cerrado

`milpa/src/emisor.py` (una función) · `tests/test_crosswalk_encuesta.py`
(nuevo) · `forense/crosswalk-pregunta-regla-v1_1.tsv` (nuevo) ·
`forense/prereg-duelo-v2/enlace-M-v1_0.md` (nuevo) ·
`forense/prereg-duelo-v2/scoring-adv1-m3.py` (solo
`validar_configuracion`) · `forense/prereg-duelo-v2/prereg-corrida-v1_0.md`
(fila `## F1 · enmienda`) · `forense/prereg-duelo-v2/lanzamiento-L-v1_0.md`
(enmienda fechada §5) · `forense/firmas-pendientes.tsv` (`FP-166`) ·
`canon/gobernanza-v1_15.md` (`ADR-208`) · `canon/estado-programa-v1_10.md`
(recifrado) · esta nota · el encargo (`A.3`).
