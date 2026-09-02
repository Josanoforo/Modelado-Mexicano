# MAESTRA33-E17 · L-ENMIENDA-CLI — cierre

`ACTO MAESTRA33-E17 · L-ENMIENDA-CLI`, 2/sep/2026, entorno NUBE (`cloud_default`,
repo-only), `SHA de redacción ee6a8a2` = tip literal de `origin/main` al arrancar
(`git log -1` confirmado, `git status` limpio), sin drift que refrescar.
`COMPUERTA: ninguna`, declarada por el encargo — no dispara verificación, se
continúa directo al 0-bis A.3.

## §0 · ARRANQUE

1. Repo: clon existente en `/home/user/Modelado-Mexicano`, `HEAD` `ee6a8a2`
   (`Merge pull request #436 from Josanoforo/acto/maestra33-c6-arbitra-r-lote-3`).
2. SHA de redacción del encargo (`ee6a8a2`) idéntico a `HEAD` — sin drift.
3. `data/raw`: ausente, esperado en clon fresco de NUBE — no es PARO. Este
   acto no toca microdato.
4. Entorno: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (no
   `sin_variable`, pero este acto no toca red ni microdato, declarado y no se
   profundiza); `data/raw/` ausente (0 archivos, A.13). Este acto no llama a
   ningún modelo ni abre red — no se corrió la sonda de `curl` porque no
   aplica (declarado en vez de omitido en silencio).
5. Espejo: no consultado — todas las cifras salen del clon de (1).

## §1 · P1 — enmienda pre-registrada

`forense/prereg-duelo-v2/prereg-corrida-v1_0.md`, nueva sección **"F2 ·
enmienda 2026-09-01"** (mismo procedimiento de fila fechada que la sección ya
sellada `prereg-corrida-v1_0.md:56`, "Regla de enmienda, no de silencio"),
insertada después de la tabla (a) de F2 sin sobreescribirla. Tabla de seis
filas (cliente, temperatura, prompt de sistema, herramientas, `modelo_id`, `k`
y variantes) con valor viejo → valor nuevo → razón, razón verbatim = firma de
mesa ("dame una opcion donde no tenga que usar API ni gastar en API..."). `k`
y las dos variantes declaradas explícitamente SIN cambio.

## §2 · P2 — `runner_l_cli.py`, `--dry-run`

`forense/prereg-duelo-v2/runner_l_cli.py` (nuevo): reutiliza
`cargar_celdas_l_spec`/`celda_a_spec`/`VARIANTES`/`K_CORRIDAS_SELLADO` de
`carga_l_v1_1.py` por importación de ruta (sin editarlo ni duplicar su
derivación), construye el comando CLI exacto que P2 fija
(`claude -p --model opus --output-format json --system-prompt "<P1>" --tools
"" --max-turns 1 "<prompt>"`), y escribe/parsea al esquema
`RespuestaCorrida` del piloto (mismos campos: `id_celda`, `variante`,
`indice`, `texto_crudo`, `valor_extraido`, `fuente_citada`, `timestamp`, más
`modelo_real` extraído del JSON de salida). Modo `--correr` (reanudable: salta
archivos ya escritos) queda implementado para la sesión ejecutora futura,
**no ejercido por este acto**.

```
$ python3 forense/prereg-duelo-v2/runner_l_cli.py --dry-run
OK -- 22 pares (celda, variante) x k=8 = 176 rutas de salida verificadas
OK -- esquema de salida (campos del piloto) verificado contra CIV-08__L-solo__01.json
OK -- comando CLI construido para las 176 corridas: claude -p --model opus --output-format json --system-prompt '<P1>' --tools '' --max-turns 1 '<prompt>'
OK -- ningún subproceso `claude` invocado en este acto (--dry-run)
Ejemplo de ruta: forense/prereg-duelo-v2/corridas-L/L-CIV-M-01-M__L-solo__01.json
Total esperado: 176
```

176 verificadas, ningún subproceso `claude` invocado (`CONTADOR: 0`). Hash
sellado: `sha256sum forense/prereg-duelo-v2/runner_l_cli.py` →
`1ae70bc2b55e6aa129f742d1d3914e13b6b0f2e0b860109edfd2d650967f4086`.

**ENMIENDA (2/sep/2026, ACTO MAESTRA34-N4 · PLOMERIA-v1_2, P1).** El hash de
arriba queda como historia -- no se borra. `runner_l_cli.py` se editó para
derivar `total_esperado` de `len(cargar_celdas_l_spec())` en vez de traer
`11`/`176` cableados en 4 puntos (líneas 188/190/198/219; ver
`PAQUETE-L-v1_2/PAQUETE-L-v1_2.md` §6, parche propuesto ahí, aplicado aquí).
Regresión: `--dry-run` con `L-spec-v1_1.json` → 176 rutas (verde, sin
cambio); con `L-spec-v1_2.json` → 224 rutas (verde). Hash nuevo:
`sha256sum forense/prereg-duelo-v2/runner_l_cli.py` →
`0c10e9ab95350ce2b3596216eeda0c23e270bce492177bd14c5657c6e28598e2`.

## §3 · P3 — `PAQUETE-L-v1_1.md` §4-bis + tabla §1

Nueva sección **§4-bis** (comando exacto, checklist de `claude auth status`,
tabla comparativa §4 vs §4-bis, comando completo con `--dry-run`/`--correr`).
Fila nueva en la tabla de §1 (hash de `runner_l_cli.py`). Checklist de mesa
(al final del documento) reorganizado: bloque vigente (§4-bis) primero,
bloque histórico (§4, API directa) tachado y marcado sin borrarlo. Nota
añadida a §7 aclarando que el destino de red bajo §4-bis ya no es
`api.anthropic.com` sino la sesión autenticada del CLI.

## §4 · Perímetro y contador

**CONTADOR: 0** — ninguna celda `L` corrida, ningún archivo de `corridas-L/`
tocado (verificado por `git status --porcelain forense/prereg-duelo-v2/corridas-L`
limpio en todo el acto). No edita `pipeline-L-adv1-m2.py`, `carga_l_v1_1.py`
ni `L-spec-v1_1.json` (verificado: `git status --porcelain` sobre los tres
sin cambios). No cambia `k` ni las dos variantes (declarado explícitamente en
la tabla de F2·enmienda). `D-6` aplicado: el acto se declara
`ACTO MAESTRA33-E17` en todo archivo que escribe.

## §5 · Cascada

- **ADR.** `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE
  '[0-9]+' | sort -n | tail -1` → `263`, sin huecos → candidato **`ADR-264`**,
  contiguo. Ningún otro acto en vuelo conocido al escribir esto. Entrada
  nueva al final de `§4. Registro de decisiones` de `canon/gobernanza-v1_15.md`
  (sección cronológica ascendente, se agrega al final, no se prepende).
  Cabecera de conteo: `263 → 264 ADR`. La auto-cita de `ADR-263`/`C6`
  ("`262 → 263 ADR`", en su propio párrafo de cascada) recibió la marca
  `{cita-historica}` — sin ella, `T15` la reportaría como afirmación vigente
  incorrecta ahora que el conteo real subió a 264 (mismo mecanismo de
  `ADR-262`/`MAESTRA33-E12`).
- **L0.** `canon/estado-programa-v1_10.md`: conteo `263→264` en la tabla de
  artefactos (línea 27) y en la cabecera de la línea `L0`; anotación nueva
  insertada **antes** de la de `ADR-263`/`MAESTRA33-C6`, sin tocar ninguna de
  las que ya estaban.
- **`registro-rotulos.tsv`.** Fila nueva `MAESTRA33-E17` en el espacio `E`,
  al final del archivo (después de `MAESTRA33-C6`, la más reciente hasta
  ahora) — mismo patrón que las filas previas de la serie maestra-33.
- **T25.** Verificado con el regex de `_T25_ROTULO_BARE` a mano (script
  Python con el mismo patrón) contra los cinco archivos que este acto
  escribe/edita en `forense/`: `2026-09-01-MAESTRA33-E17-L-ENMIENDA-CLI-NO-API.md`
  (0), `prereg-corrida-v1_0.md` (0 en el diff), `PAQUETE-L-v1_1.md` (0 nuevos
  — el único hit, "E2" dentro de "ACTO E2-PREP-L-RUN", es texto preexistente
  sin tocar, y el archivo ya vive en `_T25_ARCHIVOS_CONOCIDOS` desde
  `MAESTRA33-E9`), `runner_l_cli.py` (0, fuera del universo de extensión
  `.py` de todos modos), `mesa-pendientes.md` (0). Esta misma nota de cierre
  cita "E2" entre comillas al describir el hit de `PAQUETE-L-v1_1.md` de
  arriba — `T25` la marcó como rótulo pelado nuevo real (corrida real,
  §5.1 abajo); añadida a `_T25_ARCHIVOS_CONOCIDOS` con el comentario que
  explica que es la misma mención de nombre propio, no un rótulo nuevo sin
  dueño.
- **`python3 tests/check.py --baseline`.**

### 5.1 · Salida de `--baseline`

Antes de marcar la auto-cita de `ADR-263` como histórica:

```
19 FAIL · 167 WARN
LÍNEA BASE: ROJO — 1 entradas nuevas frente a tests/baseline.json (HEAD congelado c6a0d72fe298e4a98fecc67912760a012fff5d8a)
· T15: canon/gobernanza-v1_15.md: cita 263 ADR; gobernanza tiene 264 únicos
```

Después de mover el marcador `{cita-historica}` a la posición correcta
(inmediatamente tras `ADR`, antes del cierre `**` — la posición con `{cita-
historica}` después de `**` no la reconoce `MARCA_HISTORICA`, verificado
contra `tests/check.py:602`):

```
19 FAIL · 167 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado c6a0d72fe298e4a98fecc67912760a012fff5d8a)
```

Un segundo ciclo rojo apareció al escribir esta misma nota (T25 sobre su
propia cita entre comillas de "E2", ver arriba) y al añadir la sección
`## CONSUMIDO` al encargo archivado — ninguno de los dos trajo rótulo pelado
nuevo real (T25 pasó limpio tras extender `_T25_ARCHIVOS_CONOCIDOS`);
`--baseline` final, tras ambas correcciones: **VERDE**, sin `FAIL` nuevo.

Los 19 `FAIL` restantes (`T09`×8, `T05`×5, `T02`×2, `T06`×2, `T08`×1, `T11`×1)
son preexistentes, ninguno tocado por este acto.

## §6 · Archivos tocados

`forense/encargos/2026-09-01-MAESTRA33-E17-L-ENMIENDA-CLI-NO-API.md` (nuevo
por A.3; `## CONSUMIDO` añadido al cerrar) ·
`forense/prereg-duelo-v2/prereg-corrida-v1_0.md` (F2 · enmienda) ·
`forense/prereg-duelo-v2/PAQUETE-L-v1_1.md` (§1 fila, §4-bis, nota §7,
checklist) · `forense/prereg-duelo-v2/runner_l_cli.py` (nuevo) ·
`forense/prereg-duelo-v2/mesa-pendientes.md` (§6, recibo) ·
`canon/gobernanza-v1_15.md` (`ADR-264` + marca `{cita-historica}` en
`ADR-263` + cabecera de conteo) · `canon/estado-programa-v1_10.md` (L0 +
tabla de artefactos) · `canon/registro-rotulos.tsv` (fila `MAESTRA33-E17`) ·
`tests/check.py` (`_T25_ARCHIVOS_CONOCIDOS`, esta nota) · esta nota.

No tocados: `pipeline-L-adv1-m2.py`, `carga_l_v1_1.py`, `L-spec-v1_1.json`,
`corridas-L/`, `corridas-R/`, `scoreboard-v1_1.md`, `scoring-adv1-m3.py`.
