ENCARGO · ACTO GEN2-CAJA-REACTIVOS-FD-1
Cierra en CAJA las dos piezas que la NUBE dejó declaradas `NO-VERIFICABLE-AQUÍ` / `PARO-ENTORNO` sobre la capa FD de reactivos: extender `tools/actualiza_reactivos_contexto.py` a los 26 grupos cuyo FD ya está en el repo (`NC-0235`) y leer el FD **real** de `endutih2025`, `censo2020`/`cpv2020` y las dos `CNBV` para publicar el **crosswalk de tablas** por instrumento (`NC-0245`). Sin medir.

CABECERA · redactado contra `9fd59d0` (merge de `PR #806`; base verificada en el ARRANQUE, `git rev-list --count HEAD..origin/main` = 0) · ENTORNO: **CAJA / Ubuntu** (`tools/entorno.py`: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable · corpus=SI(examinados=413) · raices=data_raw:SI descargas_mx:SI · python 3.14.4 · numpy 2.3.5 pandas 2.3.3 scipy 1.16.3 yaml 6.0.3 pyreadstat 1.3.6`; red **no** sondeada porque este acto no descarga nada) · COMPUERTA: ninguna declarada por el lanzamiento · MODELO: Opus · Estado: VIVO · candidatos FP/ADR/NC: derivan al cierre (ADR real en `origin/main` al arrancar: 523; `NC` máxima: `NC-0252`).

LANZAMIENTO, verbatim (mesa, 15/sep/2026): llegó pegado en el mensaje que invocó el acto, no como archivo del repo; A.3 lo fija aquí.

PIEZAS (texto de mesa, verbatim)

> CAJA · ACTO GEN2-CAJA-REACTIVOS-FD-1 (Opus; paralelo a F6-PANEL-CAJA-1, sin archivo común): NC-0235 — extender tools/actualiza_reactivos_contexto.py a los 26 grupos con FD en el repo; NC-0245 — leer los FD reales de ENDUTIH 2025, Censo 2020 y CNBV y publicar el crosswalk de tablas. Es lo que evita que /mapea y la sonda vuelvan a dar NO-ENCONTRADO por no poder abrir un descriptor. Sin medir. NC-0202 no va: el servicio ya la tomó (adq/2026-09-15-nc-0202).

LECTURA DEL LANZAMIENTO (del ejecutor, no de mesa).

- **«los 26 grupos con FD en el repo»** se resuelve mecánicamente contra `data/reactivos-ciegos-81-v1_0.tsv` (`ADR-519`): 18 filas `CABLEAR-CAPA-FD-YA-EN-REPO` + 8 filas `CANDIDATA-FD-EXT-POR-VERIFICAR` = **26**; las otras 55 son `REQUIERE-FD-EN-CORPUS` y **no** son objeto de este acto. No se infiere el conjunto «a ojo».
- **«sin archivo común» con `GEN2-F6-PANEL-CAJA-1`** es una restricción dura y verificada, no una cortesía: esa rama (`origin/acto/gen2-f6-panel-caja-1`, sin PR al arrancar) toca `data/reactivos-contexto-fuentes-v1_0.tsv` y `data/reactivos-contexto-verificados-v1_0.tsv`, que son **salidas por defecto** de `tools/actualiza_reactivos_contexto.py`.
  ```
  $ git diff --name-only origin/main...origin/acto/gen2-f6-panel-caja-1
  canon/gobernanza-v1_15.md
  data/reactivos-contexto-fuentes-v1_0.tsv
  data/reactivos-contexto-verificados-v1_0.tsv
  forense/encargos/2026-09-15-GEN2-F6-PANEL-CAJA-1.md
  forense/no-corrido.tsv
  forense/notas/2026-09-15-GEN2-F6-PANEL-CAJA-1-cierre.md
  forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv
  ```
  Consecuencia de diseño, declarada **antes** de correr nada: la extensión de `NC-0235` escribe en **rutas nuevas y propias**, nunca sobre `contexto-v1_1` / `residual-v1_1` / `fuentes-v1_0` / `verificados-v1_0`. Un acto que «extiende» pisando la salida del acto hermano no es extensión, es colisión. Los tres archivos de cascada que sí son comunes (`canon/gobernanza-v1_15.md`, `forense/no-corrido.tsv`, `canon/estado-programa-v1_13.md`) se resuelven con la convención de la casa (entrada de `origin` primero, la propia después) — ahí la colisión es esperada y tiene regla.
- **«sin medir»** es literal: cero corridas del motor, cero `RESULT`, cero adopciones, cero parámetros, cero llamadas a modelo, cero descargas, **cero microdato abierto**. Un descriptor de archivo no es microdato; abrirlo no contamina la sesión respecto de ningún valor.
- **`NC-0202` queda explícitamente FUERA** por instrucción de mesa: ya la tomó el servicio en `adq/2026-09-15-nc-0202` (`PR #805`, abierto al arrancar). Este acto no la toca ni la cierra.

VERIFICACIÓN DE EXISTENCIA (A.8, contestada por el ejecutor contra `9fd59d0`, con comando):

(1) **¿Existe ya la estructura?** SÍ, y este acto la reutiliza sin redefinirla: `tools/actualiza_reactivos_contexto.py` (825 líneas, `--objeto` repetible, por defecto `PRIORITY = ("envipe","ennvih","encuci","enif","ensafi")`) · `tools/recupera_reactivos_fd.py` y su par `data/inventario-reactivos-fd-recuperado-v1_0.tsv` / `data/reactivos-fd-recuperado-residual-v1_0.tsv` (`ADR-522`, `PR #803`) · las dos capas FD (`data/inventario-fd-v1_1.tsv` 17 094 filas; `data/inventario-fd-ext-v1_0.tsv` 10 635) · el censo `data/reactivos-ciegos-81-v1_0.tsv` (81 filas) · `tools/busca_reactivos.py`.

(2) **¿Existe ya el contenido?** NO, en las dos piezas, y está medido cuál es el hueco:

- `NC-0245` — el residual del predecesor son **7 620** filas con dos motivos, y su reparto por instrumento es el que fija el alcance de esta pieza:
  ```
  $ (data/reactivos-fd-recuperado-residual-v1_0.tsv, 7620 filas)
    TABLA_SIN_FD    5482   «la hoja no existe en el descriptor indexado»
    VARIABLE_SIN_FD 2138   «la hoja empareja; la variable no aparece en ella»
    por instrumento (los 6 mayores):
      2172  ADQ15_CNBV_AhorroFinanciero_Financiamiento  TABLA_SIN_FD
      1939  enasem2018                                  TABLA_SIN_FD
      1920  enasem2021                                  VARIABLE_SIN_FD
       504  endutih2025                                 TABLA_SIN_FD
       376  censo2020                                   TABLA_SIN_FD
       221  ADQ15_CNBV_BDIF_inclusion_financiera        TABLA_SIN_FD
  ```
  No hay ningún crosswalk de tablas en el árbol: `ls data | grep -i crosswalk` sólo devuelve `crosswalk-fuente-puerta-2026-08-1{3,4}.tsv`, que es otro objeto (fuente↔puerta, no tabla de payload↔hoja de FD).
- `NC-0235` — el tool nunca se ha corrido sobre los 26: su lista por defecto son cinco familias y ninguna de ellas está entre las 26 del censo.

(3) **¿La estructura es posterior al trabajo?** No: las capas FD son de agosto/2026, el censo y el puente son de anteayer y ayer. Este acto **no clasifica, no pre-registra, no carga y no sella** ninguna regla del motor, y no cita ningún `id` de regla ni `R-n`: `tools/ya_medido.py` no aplica.

(4) **Cobertura retroactiva / raíz.** El FD real de los cuatro instrumentos de `NC-0245` **está en la raíz montada** — este acto no pide adquisición y por tanto no declara ningún `AUSENTE-EN-RAIZ`. Censo de raíz del día citado igualmente por A.8: `forense/censo-raiz/2026-09-15.txt` — «Total en disco: 524 · nuevos: 62 · ya registrados: 462 · conflicto de nombre: 0 · fuera de alcance de dato: 0 · clones: 0».

PIEZAS DERIVADAS (lo que este acto ejecuta)

P1 · **El crosswalk de tablas, leído del FD real** (`NC-0245`). Un tool nuevo que abre el descriptor **real** de `endutih2025`, `censo2020`/`cpv2020` y las dos `CNBV` desde la raíz montada, y publica una tabla —no prosa— que empareja **miembro de payload ↔ hoja del descriptor** por instrumento, con el método de emparejamiento y su evidencia fila por fila (`payload_id`, `sha256_12`, hoja, método, y la razón cuando NO empareja). Reglas que no se aflojan: **un emparejamiento que el FD no sostiene no se publica** — se conserva como residual con motivo. `ti25hog.dbf ↔ tic_2025_hogares` sólo entra si el FD real lo dice; si lo que lo sostiene es el juicio del ejecutor, la fila sale marcada como propuesta y va a mesa, no al crosswalk acreditado.

P2 · **La extensión del extractor a los 26** (`NC-0235`). `tools/actualiza_reactivos_contexto.py` pasa a cubrir los 26 grupos con FD en repo, con salida en **rutas propias** (ver «sin archivo común» arriba) y residual acreditado por motivo para lo que no cubra. Lo que el extractor no pueda abrir se reporta como residual con el formato del FD y el error real, nunca como silencio.

P3 · **Consumo — que `/mapea` y la sonda dejen de dar `NO-ENCONTRADO` por no poder abrir un descriptor.** Se cablea la salida nueva al buscador con clave explícita (mismo convenio que `fd`/`fd_ext`/`fd_recuperado`: nunca en `vigente`) y se demuestra con consultas **antes/después** sobre instrumentos hoy ciegos por construcción. Sin demostración de consumo, las piezas P1/P2 son inventario, no cierre de `NC`.

P4 · **Cierre de las dos `NC` o declaración honesta de lo que queda.** `NC-0235` y `NC-0245` se marcan `CERRADA` **sólo** en la parte que este acto acredite; lo que no alcance se queda `ABIERTA` con sucesor nombrado, en `## NO-CORRIDO / RESERVAS`. Los 55 grupos `REQUIERE-FD-EN-CORPUS` siguen fuera.

PERÍMETRO: `forense/encargos/2026-09-15-GEN2-CAJA-REACTIVOS-FD-1.md` (este archivo) · un tool nuevo para el crosswalk y sus salidas en `data/` (rutas nuevas) · `tools/actualiza_reactivos_contexto.py` y sus salidas **en rutas nuevas** · `tools/busca_reactivos.py` (sólo `TABLAS` y su documentación) · `tests/` (prueba del tool nuevo) · `data/INFRAESTRUCTURA-v1_0.md` (filas nuevas) · `forense/notas/2026-09-15-GEN2-CAJA-REACTIVOS-FD-1-cierre.md` · `forense/no-corrido.tsv` · `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_13.md`, `canon/registro-rotulos.tsv`, `tests/check.py` (cascada).
NO toca: `data/reactivos-contexto-fuentes-v1_0.tsv` · `data/reactivos-contexto-verificados-v1_0.tsv` · `data/inventario-reactivos-contexto-v1_1.tsv` · `data/reactivos-contexto-residual-v1_1.tsv` (los cuatro, por el acto hermano) · ningún índice histórico (`inventario-reactivos-*`, `inventario-fd-*`, `reactivos-ciegos-81-v1_0`, `inventario-reactivos-fd-recuperado-v1_0`) · `forense/prereg-duelo-v2/` · `milpa/` · `data/corrida0/` · `data/manifiesto.yaml` · la cola de adquisición · `NC-0202` · el motor, las adopciones y los preregistros.

CONTADOR: **cero**. Ninguna corrida, ningún `RESULT`, ninguna adopción, ningún parámetro, cero llamadas a modelo, cero descargas, cero microdato abierto. Poder abrir un descriptor no acredita suficiencia científica de nada.

LO QUE NO HACE: no adquiere · no abre microdato · no toca `NC-0202` · no publica identidad que el FD no sostenga · no propaga texto entre olas ni por nombre de variable · no toca los 55 grupos `REQUIERE-FD-EN-CORPUS` · no abre `F6` · no firma por mesa · no fusiona ningún PR.

CIERRE: cascada completa (preflight de `tools/cierre_acto.py` → ADR → L0 → `--aplica` → rótulos → T25 → suite → push → UN PR) + `## NO-CORRIDO / RESERVAS` + `## CONSUMIDO` con el PR real.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «`NC-0235` — extender a los 26 grupos»: la **segunda mitad** del sucesor de esa fila, la **adquisición del FD de los 55 grupos** `REQUIERE-FD-EN-CORPUS` (92 941 filas ciegas) | `FUERA-DE-PERÍMETRO`. El lanzamiento pidió «los 26 grupos con FD en el repo» y eso es lo que se ejecutó. La fila `NC-0235` pedía además adquisición, y **esa mitad no se disuelve al cerrarla**: pasa íntegra a `NC-0258` | Esas 92 941 filas no cambian de estado y `NC-0136` sigue `ABIERTA`. El cableado que este acto publicó (`--fuentes` repetible + `--crosswalk`) es justo lo que las hará utilizables el día que su FD entre a la raíz | `NC-0258` · ADQUISICIÓN dirigida por la columna `demanda_hoy` de `data/reactivos-ciegos-81-v1_0.tsv`, y después una corrida del extractor con esas fuentes añadidas |
| Acreditar las **190 filas** `IDENTIDAD-INSUFICIENTE` del residual del crosswalk (`MOCIBA2015.sav` 159 · `enasem2018 SECT_B_*` 44 · `enasem2021 SECT_B_NON_RESIDENT_FOLLOW_UP` 31) | `NO-VERIFICABLE-AQUÍ`. Aflojar el umbral (cobertura ≥ 0.95, margen ≥ 0.30, emparejamiento mutuo) para que entren publicaría identidad que el FD no sostiene — el mismo atajo que `ADR-522` rechazó con las 10 765 filas que emparejarían por nombre de variable | 190 de 7 620 filas siguen sin tabla acreditada. El resto del residual (2 368) **no** es deuda: es irrecuperable por construcción y se declara como tal | `NC-0259` · MESA, si decide que un emparejamiento revisado a mano es acreditable para esos tres casos |
| Retirar del censo de filas ciegas las **2 368** que este acto acreditó como sin enunciado posible (`EJE-TRANSPUESTO` 2 172 · `MIEMBRO-ES-EL-PROPIO-FD` 150 · `NO-ES-TABLA-DE-DATOS` 46) | `FUERA-DE-PERÍMETRO`. `data/reactivos-ciegos-81-v1_0.tsv` y `tools/censa_reactivos_ciegos.py` están en la lista **NO toca** de este encargo y no se tocaron | El censo de `NC-0136` sigue contando como ciegas 2 368 filas que no pueden dejar de serlo. Sobreestima la deuda y puede desviar adquisición hacia donde no hay nada que adquirir | `NC-0260` · acto que re-derive el censo leyendo `data/crosswalk-tablas-fd-residual-v1_0.tsv`, o MESA si decide que el denominador no se recorta ni por motivo acreditado |
| `NC-0202` (sonda `CORR-0008`, tres candidatas web) | `SUSTITUIDO-POR:adq/2026-09-15-nc-0202` (`PR #805`). Instrucción explícita de mesa en el lanzamiento: «`NC-0202` no va: el servicio ya la tomó». **Qué absorbe el sustituto:** la fila completa. **Qué queda huérfano:** nada de `NC-0202` — este acto no la toca, no la cierra y no la cita como propia | Ninguno para este acto; `NC-0202` sigue en manos del servicio | `adq/2026-09-15-nc-0202` / `PR #805` |
| Que `T03` deje de dar un WARN distinto según si `data/raices.local.yaml` (gitignorado) está presente en el worktree | `FUERA-DE-PERÍMETRO`. Es un defecto de la suite, no de este perímetro: hace que la misma corrida sobre el mismo árbol dé `4355` en CAJA y `4356` en CI, y con ello un `T16` rojo en local que no existe en CI. Medido con control positivo (§6.3 de la nota) y asentado en `forense/hallazgos.md`; **no** se abrió `NC` para no inflar el ledger con una fila que ninguna compuerta espera | Todo acto de CAJA verá un `T16` rojo espurio y puede «corregir» la cifra vigente a la de local, poniendo CI en rojo — que es exactamente el defecto que `T16` existe para atrapar | SIN-ASIGNAR (candidato a acto de mantenimiento de `tests/check.py`) |

## CONSUMIDO

`PR #812` (`acto/gen2-caja-reactivos-fd-1` → `main`), abierto el 16/sep/2026 por la sesión que
ejecutó este encargo. `ADR-526` (renumerado dos veces: `ADR-524` lo tomó `GEN2-PINS-REPRODUCE-1` y
`ADR-525` `GEN2-MANTENIMIENTO-3`). Cierre en
`forense/notas/2026-09-15-GEN2-CAJA-REACTIVOS-FD-1-cierre.md`. **No fusionado por el ejecutor**: el
merge es de mesa.
