# Nota de cierre — ACTO E5-SELLA-FP164-OCTAVA (ADR-204)

26/ago/2026 · SHA base `8b317d3` (origin/main tras fusionar #373/#374, `git status` limpio) · Entorno NUBE (`cloud_default`), no toca microdato ni red.

## Arranque

1. **REPO.** Clon existente en `/home/user/Modelado-Mexicano`. `git log -1`: `8b317d3 Merge pull request #374 from Josanoforo/acto/e3-ejerce-llave-compartamos`. `git status`: working tree limpio. No se clonó nada nuevo.
2. **SHA.** Coincide exactamente con el declarado por el encargo (`8b317d3`). Sin desfase, sin re-derivación necesaria.
3. **data/raw.** Ausente (`ls data/raw` → No such file or directory). No es paro: este acto no toca microdato, no se creó ni se enlazó — no hace falta para editar `milpa/`, `forense/` ni `canon/`.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (coincide con lo esperado). Este acto no toca microdato ni red — se omite la sonda `curl` contra INEGI (0 archivos examinados por ninguna sonda, porque no se corrió ninguna; no hay veredicto negativo que declarar aquí).
5. **ESPEJO.** No se usó. Toda cifra de esta nota sale del clon de (1), comandos a la vista abajo.

## Compuerta de mesa

Verbatim recibido en el encargo, opción (b) afirmativa:

> FIRMO FP-164: opción (b) — "Entonces a tu pregunta, entra a fila nueva con la octava clase." (mesa, chat de dirección, 26/ago/2026).

Compuerta abierta: se procede a escribir en `milpa/`.

## Compuertas de contenido

```
$ awk -F'\t' '$1=="FP-164"{print $6}' forense/firmas-pendientes.tsv
ABIERTA
```
(única fila del tablero con ese estado en `FP-164`, verificado antes de tocar el tsv).

```
$ grep -n "EVIDENCIA_EXPERIMENTAL_TERCEROS" milpa/procedencia.yaml
59:#   EVIDENCIA_EXPERIMENTAL_TERCEROS — octava clase, sellada 25/ago/2026
744:      EVIDENCIA_EXPERIMENTAL_TERCEROS -- la regla sigue ASIGNADO (la fuente citada, en conjunto con
```
2 hits sobre 1 archivo: `:59` definición (clase VACÍA en ese momento), `:744` excepción fechada de `Progresa_RCT` (no es fila de la clase). Confirma NO-ENCONTRADO como entrada de datos antes de esta fila.

```
$ sha256sum forense/resultado-exp-compartamos-v1_0.md
513925ecff6cfcbcad6eed8c2ddd93b4f074340cb8dbe0015a8eabcdea6eba42  forense/resultado-exp-compartamos-v1_0.md
```
Coincide con el prefijo declarado por el encargo (`513925ecff6cfcbc…`). Sin discordancia — no hay PARO.

## Qué se escribió

1. **`milpa/procedencia.yaml`** — nueva sección `evidencia_experimental_terceros:` (antes del bloque `asignados_coeficiente`), con una entrada bajo la regla `dinero.credito.baja_friccion_usura_dano_downstream`, clase `EVIDENCIA_EXPERIMENTAL_TERCEROS`, campos: `llave_id: EXP-COMPARTAMOS-1`, `cita` (Angelucci, Karlan & Zinman, AEJ: Applied, openICPSR 116334-V1), `valor` (el ITT/IC/N/G/gl/ola/variable verbatim de la fila FP-164), `primera_etapa` (contexto de identificación, declarado explícitamente como no-un-segundo-número-a-sostener), `escala` (pp de `A_ever_late_not_cond`, sin enlace declarado a otras escalas — A-bis regla 3), `que_sostiene` (dirección del mecanismo, NO calibra ni sustituye el `[MEDIA](a)` de `canon/modelo-decision-v4_0.md:501`, que queda intacto), `universo` (estampa A.10: este paquete, esta ola, este N, un experimento/un estado/un producto), `reservas` (las tres reservas verbatim de la fila FP-164), `fecha` y `adr`.
   El comentario de cabecera de la clase (líneas 59-81) se actualizó para reflejar que la clase ya no nace vacía hoy — pasó de "Nace VACÍA: cero números en esta clase hoy" a "Nació VACÍA 25/ago/2026; primer consumo 26/ago/2026 (FP-164 opción (b), ADR-204...)". No se tocó nada de la excepción `Progresa_RCT` (`:744` intacta, sigue ASIGNADO).
2. **`forense/firmas-pendientes.tsv`** — fila `FP-164`: `estado` ABIERTA → FIRMADA; `firmada_en` = verbatim de la RANURA del encargo; `ejecutada_en` = `ADR-204 (ACTO E5-SELLA-FP164-OCTAVA)`. El resto de la fila (qué_se_firma, dónde, creado, gatea, encargo) queda intacto. Tablero: **0 ABIERTA** tras esta firma (`awk -F'\t' '$6=="ABIERTA"' forense/firmas-pendientes.tsv | wc -l` → 0).
3. **`forense/encargos/2026-08-26-E5-SELLA-FP164-OCTAVA.md`** — el encargo íntegro, commitado por A.3, con bloque `## CONSUMIDO` añadido al cierre.
4. **`canon/estado-programa-v1_10.md`** — recifrado `estado §L0`: dos entradas vigentes (`:210`, `:303`) que declaraban `19 FAIL · 129 WARN` se actualizaron a `19 FAIL · 128 WARN` con una nueva entrada de historial `(Recifrado 129→128 WARN · ... ACTO E5-SELLA-FP164-OCTAVA ...)`, siguiendo el mismo patrón que los recifrados anteriores (`CIERRA-4-FIRMAS`, `CIERRA-FP157`, etc.). Además, una entrada histórica de `ACTO MAESTRA30-E3 · EJERCE-LLAVE-COMPARTAMOS` (que declaraba `19 FAIL · 129 WARN` sin el marcador `{cita-historica}`) se corrigió para llevar ese marcador — ajuste mínimo, cero lógica nueva, exigido porque `T16` la contaba como vigente y ahora contradice la corrida real tras el cambio de este acto. Recifrado de ADR (203→204) en tres sitios: la línea `L0` misma, la tabla de artefactos (`:27`) y `canon/gobernanza-v1_15.md` (cabecera + bloque `ADR-204` + su `Cascada`). No se tocó ninguna otra línea de ese archivo.
5. **`canon/gobernanza-v1_15.md`** — bloque `ADR-204` (con su párrafo `Cascada`, máximo re-derivado por `re.findall(r'ADR-(\d+)')` → `203`, sin huecos → `204`) insertado inmediatamente después de la `Cascada` de `ADR-203`, siguiendo el orden cronológico ya establecido en el archivo. Cabecera de conteo (`:2`) recifrada `203 ADR` → `204 ADR`.

### Extensión mínima de perímetro, declarada (mismo patrón que `#372`/`#373`/`#374` con `T25`/`T22`)

El encargo listaba como tocable solo `milpa/procedencia.yaml`, `forense/firmas-pendientes.tsv`, la nota nueva, el encargo archivado, `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md` y `tests/` bajo el paso 4. Al correr `tests/check.py --baseline` con el encargo y esta nota ya escritos, salieron dos fallos nuevos, ambos del mismo tipo mecánico que ya atraparon `E1`/`E3`/`E4`:

- **`T22`** — el encargo archivado (`forense/encargos/2026-08-26-E5-SELLA-FP164-OCTAVA.md`) y esta nota citan verbatim la RANURA de firma de mesa y el texto de `FP-164` (que hablaba de la fila "PROPUESTO"); ninguno es un pendiente nuevo sin dueño — la firma que citan ya está capturada en `FP-164` `FIRMADA`. Añadidos a `_T22_ARCHIVOS_CONOCIDOS` en `tests/check.py`, con la razón inline (autocaptura, no un pendiente real).
- **`T25`** — ambos archivos traen el rótulo pelado `E5` (el nombre que dirección le dio al encargo), que colisiona en forma bare con `E4x`/`E4`/`E-3`/`E3-TRIAGE`/`MAESTRA30-E1..E4` (referentes reales distintos, ninguno gana — mismo patrón que `M5`). Censado en `canon/registro-rotulos.tsv` (fila nueva `E5`) y añadidos a `_T25_ARCHIVOS_CONOCIDOS` en `tests/check.py`.

`canon/registro-rotulos.tsv` no estaba en la lista explícita del perímetro, pero tocarlo para censar el rótulo es la misma extensión mínima que `ACTO DISEÑO-ENSAFI`/`ACTO MAESTRA30-E3` ya declararon para el mismo defecto — el texto de dirección (el encargo, archivado verbatim por `A.3`) no se edita para complacer un test. Ambos ajustes de `tests/check.py` son adiciones a conjuntos de exclusión ya existentes, sin lógica nueva.

## Por qué no se tocó `canon/modelo-decision-v4_0.md` ni `milpa/refutations.yaml`

La vía (b) firmada no compite por el sitio del `[MEDIA](a)` — eso sigue exigiendo acto propio de mesa (vía (a), no ejecutada, no pedida). `milpa/refutations.yaml` no forma parte del perímetro de este acto y no se abrió.

## Test suite

Antes del acto (HEAD `8b317d3`): `python3 tests/check.py` → 19 FAIL · 129 WARN.

Después del acto:

```
$ python3 tests/check.py --baseline
...
19 FAIL · 128 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
(5 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

El cambio de conteo neto es el esperado: `T22` deja de contar `FP-164` `ABIERTA` (−1 WARN neto). `T16` (auto-chequeo de coherencia estado/corrida) exigió el recifrado declarado arriba en `canon/estado-programa-v1_10.md`; sin ese ajuste, `T16` fallaba porque el estado declarado (129) ya no coincidía con la corrida real (128). Los dos archivos nuevos de este acto (encargo + nota) dispararon `T22`/`T25` por citar verbatim texto ya rastreado (ver "Extensión mínima de perímetro" arriba) — resueltos añadiéndolos a los conjuntos de exclusión ya existentes en `tests/check.py`, sin lógica nueva. Ningún archivo de `tests/` cambia su comportamiento, solo sus conjuntos declarativos de excepciones conocidas.

## Contador

Tablero: 1 → 0 ABIERTA. La octava clase `EVIDENCIA_EXPERIMENTAL_TERCEROS` pasa de VACÍA a 1 fila — primer consumo formal de evidencia clase (iii) de `ADR-57(c)` en el programa. Cero cifras nuevas: el número ya se midió en `#374` (`forense/resultado-exp-compartamos-v1_0.md`); este acto solo lo aloja en el ejecutable.
