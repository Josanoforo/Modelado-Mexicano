# ACTO GEN2-RESIDUAL-81-1 · EL PUENTE QUE FALTABA: 9 195 IDENTIDADES CIEGAS RECUPERADAS SIN SALIR DEL REPO — nota de cierre

**16/sep/2026 · entorno NUBE · Opus · cero llamadas a modelo · cero microdato abierto · cero descargas · cero adopciones · contador científico CERO.**

Base: `origin/main = 10f8617` (merge de `PR #801`), 0 commits detrás al arrancar.
Encargo archivado verbatim (0-bis A.3): `forense/encargos/2026-09-16-GEN2-RESIDUAL-81-1.md`.
Entorno crudo (`python3 tools/entorno.py`): `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default · git_status=LIMPIO(0) · python=3.11.15 · numpy/pandas/scipy/pyreadstat AUSENTES · raices=data_raw:NO · corpus=NO(examinados=0)`.

## 0 · El titular

`ACTO GEN2-REACTIVOS-RESIDUALES-2` (`ADR-519`) dejó **mapeado y no ejecutado** el residual de `NC-0136`: 18 grupos ciegos cuya capa FD ya estaba en el repo, 16 815 filas. Este acto lo ejecuta — y al intentarlo encuentra **por qué nadie lo había hecho**: el cruce por identidad exacta daba **CERO**.

No porque faltara el texto. Porque las dos capas **escriben el mismo miembro de tres maneras distintas**, y nadie lo había medido.

**Resultado: 9 195 de 16 815 filas ciegas (54,7%) recuperan su enunciado por identidad exacta `instrumento + tabla + variable`, sin corpus, sin descarga y sin aflojar una sola regla de acreditación.**

## 1 · El defecto, medido antes de escribir nada (A.8)

```
$ (cruce crudo por (archivo_miembro, variable_id) sobre las 16 815 filas)
  emparejan por (tabla,variable): 0
  emparejan solo por variable   : 10765
```

Cero. Y la salida engañosa es la segunda línea: **10 765 filas emparejarían por nombre de variable**, y publicarlas habría sido el error exacto que `ACTO GEN2-REACTIVOS-RESIDUALES-BUSQUEDA-UTIL` prohibió por escrito («no hay propagación entre olas ni *fallback* cruzado por el mero nombre de variable»). **Ninguna de esas 10 765 se publica.**

La causa real son **tres diferencias de ortografía del miembro**, cada una con su motivo material:

| el índice escribe | el descriptor escribe | por qué |
|---|---|---|
| `thogar.csv`, `mod_2017_ciberacoso.dbf` | `THOGAR`, `MOD_2017_CIBERACOSO` | el índice nombra el **miembro del payload**; el FD, la **hoja del descriptor** |
| `enut_2019/THOGAR.csv` | `THogar` | el índice guarda a veces la **ruta dentro del paquete**; el FD nunca la lleva |
| `tr_enasem24_master_follow_up_file.csv` | `TR_ENASEM24_MASTER_FOLLOW_UP_FI` | la hoja está **truncada a 31 caracteres** — el límite de nombre de hoja de Excel |

## 2 · El puente, declarado y acotado

Tres pasos, ninguno de los cuales decide identidad — sólo normalizan cómo se escribió el miembro:

1. quitar la **ruta interna** del paquete;
2. plegar a minúsculas y quitar la **extensión conocida**;
3. si eso no empareja, aceptar **prefijo de 31 caracteres** (el límite de Excel) **sólo cuando la hoja candidata es única** en ese instrumento.

**Lo que el puente NO hace**, y está probado con falsador propio: no empareja por `variable_id` con la tabla sin resolver · no propaga texto entre olas · no resuelve una tabla ambigua por cercanía de nombre (`TABLA_AMBIGUA` sale al residual, no se adivina).

```
$ python3 tools/recupera_reactivos_fd.py --escribe
GRUPOS · 18 con capa FD limpia (censo de ADR-519) · archivos examinados = 3 (A.13)
FILAS CIEGAS EXAMINADAS · 16815
  RECUPERADAS por identidad exacta · 9195
      EXACTO               7417
      EXACTO_PREFIJO_31    1778
      texto_tipo ETIQUETA_VARIABLE      2356
      texto_tipo PREGUNTA_DICCIONARIO   6839
  RESIDUAL · 7620
      TABLA_SIN_FD         5482
      VARIABLE_SIN_FD      2138
```

**El rotulado también se declara en vez de suponerse.** El FD mezcla, en la misma columna, etiquetas de variable («Condición de actividad») y preguntas literales («6.33.1 En promedio, ¿cuántas horas a la semana dedica…?»). Rotular todo como etiqueta subdeclararía; rotular todo como pregunta sobredeclararía. Se separa por un rasgo observable —la marca de interrogación— y se dice que es una **heurística de rotulado, no una afirmación sobre la fuente**. Nunca `PREGUNTA_COMPLETA`: ese rótulo lo reserva `contexto-v1_1` para el enunciado íntegro leído del cuestionario.

## 3 · Por instrumento, con el residual a la vista

| instrumento | recuperadas | residual | lectura |
|---|---:|---:|---|
| `enasem2024` | 2 158 | 64 | prácticamente completo |
| `enasic2022` | 1 319 | 37 | prácticamente completo |
| `enut2019` | 1 303 | 4 | lo desbloqueó el paso de la ruta interna |
| `enut2024` | 885 | 0 | **completo** — es el instrumento de `CORR-0014` |
| `enadid2023` | 674 | 21 | incluye `P3_27_AG`, el objeto de `CORR-0013` |
| `enfih2019` | 664 | 0 | **completo** — es el instrumento de `CORR-0012` |
| `endutih2024` / `endutih2023` | 477 / 467 | 13 / 12 | casi completos |
| `mociba2016` / `mociba2017` / `mociba2015` | 412 / 340 / 136 | 6 / 4 / 184 | la serie del panel `F6` |
| `enasem2018` / `enasem2021` | 184 / 176 | 1 994 / 1 920 | **mayoría residual**: sus hojas de FD no cubren las tablas del payload |
| `endutih2025` | 0 | 509 | el índice usa abreviaturas (`ti25hog.dbf`) y el FD nombres largos (`tic_2025_hogares`): **no es ortografía, es un mapeo semántico** — no se adivina |
| `censo2020`, `cpv2020`, las dos `CNBV` | 0 | 2 852 | tablas del payload sin hoja correspondiente en el descriptor indexado |

**La lectura honesta del 54,7%:** el puente resuelve lo que es diferencia de escritura. Lo que queda es diferencia **material** —una hoja que no existe en el descriptor, o un nombre que sólo un humano puede emparejar—, y eso no se cierra con una regla: se declara.

## 4 · Utilidad demostrada, antes y después

Consultas donde el universo vigente es ciego **por construcción**:

| consulta | `vigente` | `fd_recuperado` | qué aparece |
|---|---:|---:|---|
| `trabajo no remunerado` | **0** | 5 | `enut2024` · `TRAB_NO_REM_CUID_HOG`, `TRAB_NO_REM_CON_CP`… — trabajo de cuidados del hogar |
| `horas a la semana` | **0** | 9 | `enasic2022` · `P6_33_1..3`, *«En promedio, ¿cuántas horas a la semana dedica de manera EXCLUSIVA al cuidado o apoyo de estas personas?»* |

Que las dos consultas caigan en **cuidados y uso del tiempo** no es casualidad: `ENUT` y `ENASIC` son justamente instrumentos que el índice nunca pudo buscar por texto.

**Control de conservación:** cinco consultas contra `vigente` (`tanda`, `atraso`, `ahorro`, `corrupcion`, `no denuncio`) dan cifra **idéntica** con el archivo nuevo y con `git show origin/main:tools/busca_reactivos.py`. La clave `fd_recuperado` es **explícita**: nunca entra en `vigente` ni en `--fuente`, mismo convenio que `fd`/`fd_ext`/`contexto_v1_0`.

**Y no toca el overlay del lote:** la cobertura prioritaria sigue siendo **43 020/55 895**. Son otros instrumentos, otra capa y otro grado de promesa; sumarlos sería inflar una cifra que mide otra cosa.

## 5 · Lo que este acto NO hizo

No re-extrajo de ninguna fuente (no hay corpus) · no modificó ningún índice histórico, ni el overlay del lote ni su residual, ni el censo de los 81 · no publicó ninguna identidad que no sea exacta · no propagó entre olas ni por nombre de variable · **no cerró `NC-0136` ni `NC-0235`** (quedan los 55 grupos sin FD, los 8 `CANDIDATA-FD-EXT-POR-VERIFICAR` y las 7 620 filas del residual de hoy) · no abrió `F6` · no adquirió · no firmó por mesa · no adoptó nada.

## 6 · Verificación

- `python3 -m unittest tests.test_recupera_reactivos_fd`: **11/11**, incluido el falsador de que ninguna fila publicada llega por una vía distinta de las dos exactas.
- Control de conservación del buscador: **5/5** idénticas (§4).
- Idempotencia: dos corridas seguidas escriben los dos TSV byte a byte iguales.
- `python3 tests/check.py --baseline`: **3 FAIL · 4 351 WARN**, **LÍNEA BASE VERDE**. Los 3 `FAIL` son los heredados del corpus documental (`T06` ×2, `T08`). La primera corrida sí dio `ROJO` por **`T16`**, que es autorreferente: `ADR-520` declaraba `3 FAIL · 4348 WARN` y la corrida real daba 4 351. Se corrigió **declarando la cifra medida en el `ADR` nuevo**, no tocando el test. De los `+3`: **2** son las filas `NC-0243`/`NC-0244` que este acto abre (`T34`, como `A.12` manda) y **la tercera no es de este perímetro** — `ADR-520` midió sobre `1fac27a` y este acto cierra sobre `10f8617`, con cuatro PR ajenos fusionados en medio; no se atribuye a este acto un WARN que no se midió como suyo.
  **Y hubo un segundo `ROJO` de `T16` después de declarar la cifra propia:** el test vigila **toda** afirmación vigente de `canon/*.md`, así que la de `ADR-520` (`3 FAIL · 4348 WARN`, verdadera cuando se midió sobre `1fac27a`) pasó a contradecir la corrida real. Se resolvió con el mecanismo que el propio test documenta —marcarla `{cita-historica}` con la nota de por qué—, **no corrigiendo el número ajeno ni tocando el test**: una cifra que fue verdadera cuando se midió es historia, no defecto.
- Contador científico: **cero**.
