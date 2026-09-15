ENCARGO · ACTO GEN2-REACTIVOS-RESIDUALES-2
Continúa `NC-0136` por utilidad concreta: enumera con comando los 81 grupos históricamente ciegos que quedan fuera del lote prioritario, mide cuántos de ellos ya tienen texto de reactivo **dentro del repo** (capa FD) sin abrir corpus, y gasta esa munición en lo que hoy demandan el mapa-19 y el panel de `F6`

CABECERA · redactado contra `0cdbd72` (merge de `PR #789`, `ACTO GEN2-MEDICION-DEMANDA-2` — base verificada en el ARRANQUE, 0 commits detrás de `origin/main`) · ENTORNO: **NUBE** (`tools/entorno.py`: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default · corpus=NO(examinados=0) · raices=data_raw:NO · numpy/pandas/scipy/pyreadstat AUSENTES · python 3.11.15`; red no sondeada porque este acto no la usa) · COMPUERTA: ninguna declarada por el lanzamiento (ni `GATED a` ni `COMPUERTA:`) · MODELO: Opus (integral) · Estado: VIVO · candidatos FP/ADR/NC: derivan al cierre.

LANZAMIENTO, verbatim (mesa, 15/sep/2026): el texto de PIEZAS de abajo es el mensaje de lanzamiento tal como llegó; este archivo lo fija por A.3 porque llegó pegado en el mensaje que invocó la skill de acto, no como archivo del repo. Todo lo que sigue a PIEZAS lo deriva el ejecutor del lanzamiento y de la casa; no es texto de mesa.

PIEZAS (texto de mesa, verbatim)

> NUBE · ACTO GEN2-REACTIVOS-RESIDUALES-2 (Opus, integral; segundo turno)
>
> * NC-0136: continuar por los 81 grupos históricamente ciegos fuera del lote y por sus residuales acreditados (12 875 filas), "por utilidad concreta, no repitiendo todo el barrido": se prioriza por lo que hoy demanda el mapa-19 y el panel F6. Nube pura (índice de reactivos).

VERIFICACIÓN DE EXISTENCIA (A.8, contestada por el ejecutor contra `0cdbd72`; el lanzamiento llegó sin el bloque y A.8 manda contestarlo con comando, no suponerlo):

(1) ¿Existe ya la estructura? SÍ, y es la que este acto usa sin crear ninguna nueva: el universo del buscador (`data/inventario-reactivos-v1_2.tsv` + `data/inventario-reactivos-ext-v1_0.tsv`, 241 591 filas), el overlay acreditado del lote (`data/inventario-reactivos-contexto-v1_1.tsv`, 43 020 filas con texto), su residual por objeto (`data/reactivos-contexto-residual-v1_1.tsv`, 6 091 grupos / 12 875 filas físicas) y la **capa FD** (`data/inventario-fd-v1_1.tsv` + `data/inventario-fd-ext-v1_0.tsv`, 27 729 filas), que existe desde `ADR-215`/`ADR-216` y que `tools/busca_reactivos.py` **no consulta** por ninguna de sus claves (`FUENTES`/`TABLAS`, verificado por lectura del archivo). La demanda viva son `data/corrida0/mapa-demanda-19-corr-v1_0.tsv` y `forense/prereg-duelo-v2/F5-panel-candidatos-v1_1.tsv`.

(2) ¿Existe ya el contenido? Parcialmente, y con un hallazgo que se declara antes de escribir nada: los 81 grupos del lanzamiento **se reproducen exactos por comando** (102 instrumentos con `texto_reactivo` vacío en el 100% de sus filas, menos los 21 de las cinco familias del lote, = 81 grupos / 129 648 filas ciegas), y **26 de esos 81 (36 707 filas ciegas) ya tienen texto de reactivo publicado en la capa FD del propio repo** — entre ellos `MOCIBA` 2015/2016/2017, `ENASEM`, `ENASIC`, `ENUT`, `ENADID`, `ENFIH`, `ENDUTIH`, `censo2020` y las dos tablas `CNBV`. Recuperar ese texto no exige corpus, descarga ni extractor nuevo: exige cablear la capa que ya está escrita.

(3) ¿La estructura es posterior al trabajo? No: la capa FD es de agosto de 2026 y el hueco de cableado es anterior a `NC-0123`. Este acto no clasifica, pre-registra, carga ni sella ninguna regla del motor y no cita ningún id de regla ni `R-n` en su SPEC: `tools/ya_medido.py` no aplica.

PIEZAS DERIVADAS (lo que este acto ejecuta, derivado del «por utilidad concreta, no repitiendo todo el barrido»)

P1 · **Censo de los 81, derivado y no tecleado.** Un generador (`tools/censa_reactivos_ciegos.py`) y su salida (`data/reactivos-ciegos-81-v1_0.tsv`): una fila por grupo ciego fuera del lote, con filas ciegas, texto FD disponible en repo, ruta de recuperación y la demanda que lo reclama hoy (mapa-19 / panel `F6` / ninguna). El número 81 deja de ser prosa heredada y pasa a ser derivable con un comando.

P2 · **El cableado, no el barrido.** `tools/busca_reactivos.py` gana dos claves explícitas de `--tablas` (`fd`, `fd_ext`) con el mismo convenio que `contexto_v1_0`/`descargas_mx`: nunca entran en `vigente`, se piden por nombre. Ninguna cifra histórica del buscador cambia.

P3 · **El gasto útil, sobre la demanda de hoy.** Dos consumidores, no un barrido:
  (a) **Panel `F6`** — la compuerta que `ACTO GEN2-F5-CIERRE-Y-PANEL-1` dejó escrita para `R01 · MOCIBA` («si el FD no trae batería de denuncia ante autoridad, MOCIBA cae») se contesta contra el índice FD ya presente en el repo, con reactivo, tabla y variable citados, sin adquisición y sin abrir base.
  (b) **mapa-19** — los instrumentos que las filas `BLOQUEADA`/pendientes reclaman se cruzan contra el censo de P1: los que tienen ruta se nombran, y los que no la tienen reciben un negativo acotado por A.13/A.15, no un silencio.
  (c) **Residual del lote (12 875 filas)** — no se re-barre: se ordena por demanda, declarando qué parte del residual bloquea hoy una fila del mapa-19 y qué parte no bloquea nada.

PERÍMETRO: `forense/encargos/2026-09-15-GEN2-REACTIVOS-RESIDUALES-2.md` (este archivo) · `tools/censa_reactivos_ciegos.py` (nuevo) · `data/reactivos-ciegos-81-v1_0.tsv` (derivado por ese tool) · `tools/busca_reactivos.py` (sólo el diccionario `TABLAS` y su documentación) · `tests/test_busca_reactivos_fd.py` (nuevo) · `forense/notas/2026-09-15-GEN2-REACTIVOS-RESIDUALES-2-cierre.md` · `forense/no-corrido.tsv` · `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_13.md`, `canon/registro-rotulos.tsv`, `tests/check.py` (cascada). NO toca: ningún índice histórico (`inventario-reactivos-*`, `inventario-fd-*`, `contexto-v1_1`, `residual-v1_1`) · `tools/actualiza_reactivos_contexto.py` · `milpa/` · `data/corrida0/` · `data/manifiesto.yaml` · `data/cola-adquisicion-v1_0.tsv` · el motor, las adopciones y los preregistros.

CONTADOR: **cero**. Ninguna corrida, ningún `RESULT`, ninguna adopción, ningún parámetro, cero llamadas a modelo, cero descargas, cero microdato abierto.

LO QUE NO HACE: no re-extrae texto de ninguna fuente (no hay corpus en NUBE) · no publica un `contexto-v1_2` ni re-genera ningún índice · no cierra `NC-0136` (los 55 grupos sin FD en repo y el residual del lote siguen abiertos) · no autoriza piloto, confirmación, llamadas ni apertura de `F6` · no firma por mesa · no adquiere · no fusiona ningún PR.

CIERRE: cascada completa (preflight de `tools/cierre_acto.py` → ADR → L0 → `--aplica` → rótulos → T25 → suite → push → UN PR) + `## NO-CORRIDO / RESERVAS` + `## CONSUMIDO` con el PR.
