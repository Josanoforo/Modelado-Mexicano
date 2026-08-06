# ENCARGO MAP-1b — Censo de las tres raíces (2026-08-06)

Contador: **0** (acto de inventario, no de medición). Perímetro: este archivo,
`data/censo-raices-2026-08-06.tsv`, una línea en `forense/hallazgos.md`. No se
tocó `data/manifiesto.yaml` ni `tests/` en ningún momento. No se movió, copió,
renombró ni borró ningún archivo de `data_raw`/`descargas_mx`/`downloads`.

## Arranque

- Clon: `/home/pc0/Modelado-Mexicano` (localizado por `find`; sentado en una
  rama ajena, `sesion/cal-conf-faseb-pos4-envipe-paso1` — no se tocó).
- Worktree propio: `/home/pc0/wt-map1b-censo-1786000741`, rama
  `map1b-censo-1786000741`, creado con `git worktree add ... origin/main`.
  `git worktree add` emitió dos veces `error: could not write config file
  .git/config: Device or resource busy` (contención esperable — TC-1, MAP-1 y
  CONF-17 corrían en paralelo en la misma máquina); el worktree quedó íntegro
  pese al error (`git status` limpio, rama correcta, HEAD correcto — verificado
  después, no asumido).
- SHA base: `58a307c` (`Merge pull request #142 from Josanoforo/desc1-descarga`)
  — coincide exactamente con el SHA que el encargo declaró como base. `main`
  no se movió.
- `git worktree list` al momento de crear el propio mostraba, además del
  propio: `wt-conf17` (6cea7e6), `wt-desc1` (e4092b0, acto ya cerrado),
  `wt-map1-1786000558` (58a307c, MAP-1 concurrente), `wt-tc1-010528-2`
  (0076d3c), `wt-ver1` (4da6759, ya cerrado) — confirma los tres actos
  concurrentes declarados por el encargo, ninguno tocado.

**Las tres rutas, crudas:**
```
$ ls -ld data/raw && readlink -f data/raw
ls: cannot access 'data/raw': No such file or directory      # antes de crear el symlink
/home/pc0/wt-map1b-censo-1786000741/data/raw                 # readlink -f sobre ruta inexistente: resuelve léxicamente, no confirma existencia

$ ls -ld "/mnt/c/Users/PC0/Descargas MX"
drwxrwxrwx 1 pc0 pc0 4096 Aug  5 18:09 /mnt/c/Users/PC0/Descargas MX

$ ls -ld "/mnt/c/Users/PC0/Downloads"
drwxrwxrwx 1 pc0 pc0 4096 Aug  5 18:30 /mnt/c/Users/PC0/Downloads
```

`data/raw` no existe en un worktree recién creado — ni siquiera como symlink roto.
El symlink es infraestructura por-worktree que `git worktree add` no reproduce
(gitignorado, igual que `raices.local.yaml`). Se verificó en los seis worktrees
existentes de esta máquina: los cinco con trabajo activo en `data_raw`
(`wt-tc1-010528-2`, `wt-conf17`, `wt-desc1`, `wt-ver1`, y el clon base) tienen
idénticamente `data/raw -> /home/pc0/mm-corpus/raw`; `wt-map1-1786000558` (MAP-1
concurrente) tampoco lo tenía todavía. Se creó el mismo symlink en el worktree
propio (`ln -s /home/pc0/mm-corpus/raw data/raw`) — no es mover/copiar/renombrar
un archivo de las tres carpetas, es la misma plomería de acceso que ya existe en
cinco worktrees de esta máquina. Confirmado después: `git status --short` marca
`?? data/raw` — defecto ya declarado en memoria de sesiones previas (patrón
`data/raw/` con slash final en `.gitignore` no matchea un symlink); no es un
hallazgo nuevo de este acto. Consecuencia práctica: en ningún `git add` de este
acto se usó `-A` ni `.`, solo nombres de archivo explícitos.

`data/raices.local.yaml` — ausente en el worktree fresco (gitignorado, por
máquina), como anticipa el encargo. Copiado de `/home/pc0/Modelado-Mexicano`
(el clon base; es el único de los seis worktrees inspeccionados que lo tiene).
Contenido crudo:
```yaml
# data_raw es INERTE para tests/manifiesto.py: RAIZ_INTEGRADA se resuelve
# por código (rutas() -> <root>/data/raw), raices_configuradas() filtra
# esta clave explícitamente. El valor de abajo es documentación del path
# real (ahora externo, compartido por los tres worktrees vía symlink en
# <root>/data/raw), no una redirección que el script lea. No lo edites
# esperando que cambie a dónde mira --verifica -- edita el symlink.
data_raw: /home/pc0/mm-corpus/raw
descargas_mx: /mnt/c/Users/PC0/Descargas MX
downloads: /mnt/c/Users/PC0/Downloads
```
Este comentario ya adelanta el resultado del PASO 1: `data_raw` en este archivo
es decorativo, la resolución real ocurre en código.

**Firma de entorno (A.2, v2.5), cuatro valores crudos:**
```
$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable
$ ls data/raw/ | head -1
BD_ENCUCI2020_dbf.zip
$ df -h /mnt/c | tail -1
C:\             931G  665G  267G  72% /mnt/c
$ python3 --version
Python 3.14.4
```
`sin_variable` = firma Ubuntu-con-red (no `cloud_default`) — entorno correcto
asignado. `data/raw/` resuelve y tiene contenido; `/mnt/c` está montado y vivo.
Los tres montajes confirmados operativos antes de censar nada.

**Espejo:** ninguna cifra de esta nota sale de `canon/estado-programa-*` ni de
ningún otro documento espejo — todo lo que sigue sale de comandos corridos en
este worktree, con el comando a la vista.

## PASO 1 — por qué 404 entradas no declaran `raiz`

Código leído: `tests/manifiesto.py`, funciones `rutas` (153-155),
`raices_configuradas` (161-172), `resolver_raiz` (175-181), y el cuerpo de
`cmd_verifica` (341-444); también `cmd_registra` (277-336) y `cmd_promueve`
(856-944) para entender qué escribe cada camino de escritura.

**(a) ¿Qué hace `--verifica` cuando una entrada no trae `raiz`?**
Asume `data_raw`. Línea exacta:
```python
383: nombre_raiz = entrada.get("raiz", RAIZ_INTEGRADA)
```
con `RAIZ_INTEGRADA = "data_raw"` (línea 158). No falla, no busca en las tres
raíces — toma `data_raw` como si la entrada lo hubiera declarado, y de ahí en
adelante la entrada es indistinguible de una que sí escribió `raiz: data_raw`.

**(b) ¿Ese default está escrito en el código, o es efecto de que el campo sea opcional?**
Escrito en el código, explícitamente, en esa misma línea 383 — un
`dict.get(clave, DEFAULT)` con el default nombrado por una constante que trae
su propio comentario (línea 158: `# resuelta por código (rutas()); nunca por
archivo`). No es un efecto colateral de un esquema laxo: es una decisión de
diseño con nombre y comentario. Más aún, el default no es solo tolerado por el
lector — está **impuesto por uno de los dos escritores**: `cmd_registra`
(277-336) no tiene parámetro `--raiz` en absoluto; resuelve siempre contra
`raw_dir` (línea 296: `ruta_absoluta = os.path.join(raw_dir, a.archivo)`) y
aborta si el archivo no está ahí (297-301); el diccionario que escribe
(315-327) nunca incluye la clave `raiz`. Una entrada creada por `--registra`
no puede tener otra raíz que `data_raw` — no por convención del operador, sino
porque el código no le da manera de declarar otra cosa, y ya verificó que el
archivo vive en `data/raw` antes de escribir la entrada. El otro escritor,
`cmd_promueve` (staging → manifiesto, usado tras `--escanea`), hace lo
opuesto: **siempre** escribe `raiz` explícita, incluso cuando vale `data_raw`
(línea 928: `"raiz": e.get("raiz", RAIZ_INTEGRADA)`, sobre una entrada de
staging que según 79-83 siempre trae `raiz` declarada). Es decir: los dos
únicos escritores están de acuerdo en el resultado (`data_raw` cuando
corresponde) pero en representación distinta — uno omite, el otro declara
explícito — y es el lector (línea 383) el que los vuelve equivalentes.

**(c) ¿Desde cuándo existe el campo `raiz`? ¿Las 404 son simplemente anteriores?**
```
$ git log -S"raiz" --date=iso --format="%h %ad %s" --reverse -- tests/manifiesto.py data/manifiesto.yaml | head -3
48ea7c7 2026-07-30 20:01:54 -0600  manifiesto.py: tres raíces (data_raw/descargas_mx/downloads), campo raiz
021ccdf 2026-07-30 20:03:46 -0600  Migra las 29 entradas ya promovidas a raiz: descargas_mx
0229ff7 2026-07-30 20:31:17 -0600  Corrige procedencia fabricada en 28 entradas ENOE/ENOEN (no solo 5)
```
El campo nace el 2026-07-30 20:01. Dos minutos después se migran retroactivamente
las 29 entradas `descargas_mx` que ya existían. Media hora después, la corrección
de procedencia ENOE/ENOEN deja 28 entradas con `raiz: data_raw` **explícita**
(verificado por conteo: exactamente 28 entradas `enoe_*`/`enoen_*` tienen `raiz`
escrita, coincide con "28 entradas" del mensaje del commit). 29+28 = 57 — el total
de entradas con `raiz` declarada hoy.

Conteo actual (`data/manifiesto.yaml`, 461 entradas, 457 con payload):
```
sin campo raiz:            400  (+ 4 entradas sin payload/sha256, sin campo `raiz`
                                   tampoco → 404 sobre el total de 461, cifra que
                                   cita el encargo)
con raiz=descargas_mx:      29
con raiz=data_raw:          28
```
El propio docstring del script (líneas 72-74) documenta el conteo histórico de
la migración: *"Las 53 entradas de payload anteriores a este campo no tienen
`raiz` -- su ausencia SIGNIFICA data_raw; no se les migra un valor retroactivo
que nadie declaró entonces."* Solo **53** entradas están explícitamente
reconocidas como "anteriores al campo, y por eso sin migrar". La cifra actual,
400/404, es casi ocho veces esa. La diferencia (≈347) no puede ser "anterior
al campo" — son entradas creadas **después** del 30/jul y que aun así no
declaran `raiz`. El propio encargo ya identificó el ejemplo más grande: las
231 entradas que DESC-1 registró el 2026-08-05, seis días después de que el
campo existiera.

**Respuesta a (c): no, las 404 no son simplemente anteriores al campo — la
mayoría (≈347 de 400) lo posdatan.** Pero tampoco es un descuido silencioso:
por (b), toda entrada nacida de `--registra` (que solo escribe contra
`data_raw` y lo verifica en disco antes de escribir) omite `raiz` **por
construcción del propio script**, no porque alguien haya olvidado declararla.
Las 231 de DESC-1 encajan en ese patrón. Lo que el docstring llama "53
anteriores al campo" describe el origen histórico del primer grupo que quedó
así; el mismo resultado (omisión = `data_raw`) se ha seguido produciendo desde
entonces por una vía de escritura distinta (`--registra`) que nunca tuvo
manera de declarar otra cosa. Si esa garantía estructural se sostiene para
las 400/404 entradas actuales — es decir, si de verdad **todas** viven en
`data_raw` y ninguna fue registrada a mano por otra vía (edición directa del
YAML) apuntando en realidad a `descargas_mx`/`downloads` — es exactamente lo
que el cruce del PASO 3 (categoría C) prueba empíricamente, no lo que este
paso puede concluir por lectura de código. No se decide aquí.

**(d) ¿Qué le pasa a una entrada `descargas_mx` cuando `raices.local.yaml` no existe?**
Prueba empírica, con el archivo real del worktree ocultado y restaurado en el
mismo comando:
```
$ mv data/raices.local.yaml data/raices.local.yaml.TEMP-oculto
$ python3 tests/manifiesto.py --verifica --id descargamasiva_3072026_105543

Entorno de verificación: Linux 6.6.87.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4

descargamasiva_3072026_105543 [descargas_mx]: RAÍZ NO CONFIGURADA -- este entorno no
define 'descargas_mx' en data/raices.local.yaml; no se puede verificar (no es un
error del manifiesto, puede ser válida en otra máquina)

Por raíz (sin colapsar):
  descargas_mx: coincide=0 · no_coincide=0 · ausente=0 · sin_configurar=1

[... bloque "Procedencia derivada, NO confirmada por el autor", 57 entradas, sin
relación con la pregunta ...]
EXIT CODE: 0
$ mv data/raices.local.yaml.TEMP-oculto data/raices.local.yaml
```
Ni AUSENTE ni error: un tercer estado distinto, `RAÍZ NO CONFIGURADA` (tally
`sin_configurar`), exactamente como documentan las líneas 26-27 del docstring
y produce el código en 391-397 (`resolver_raiz` devuelve `None` porque
`raices_configuradas()` devuelve `{}` cuando el archivo no existe — línea
168-169). Nota adicional no pedida por la pregunta pero visible en la salida
cruda: el exit code queda en `0` — `sin_configurar` no toca `exit_code` (solo
la rama NO COINCIDE, línea 418, lo pone en 1). Una corrida de `--verifica`
sobre entradas `descargas_mx` en una máquina sin `raices.local.yaml` termina
en éxito de proceso sin haber verificado nada. Se declara, no se corrige —
`tests/` está fuera de este perímetro.

Archivo restaurado y confirmado idéntico (552 bytes, mismo contenido) antes de
continuar.

## PASO 2 — Censo de las tres carpetas

Script ad-hoc de sesión (no vive en el repo — perímetro no lo permite; corrió
contra las rutas del worktree, solo lectura, un `sha256_de` por archivo,
reutilizado). `data/raw` censado por su destino resuelto
(`/home/pc0/mm-corpus/raw`), no por el enlace.

**Filtro de `downloads` (2141 archivos totales), declarado:** extensión ∈
`{zip csv dta dbf xlsx pdf sav xml}` — el conjunto que cita el propio encargo,
aplicado literal. Deja **378** dentro del filtro y **1763** fuera
(10 008 026 985 bytes ≈ 9.3 GiB), dominados por `.md` (1141), `.docx` (210),
`.png` (154), `.html` (70), `.txt` (37), `.exe` (35), `.json` (21), `.jsx`
(18), `.jpg` (14), `.py` (13) y una cola de extensiones sueltas.

**Aviso sobre `.docx`, no resuelto aquí:** el filtro literal excluye 210
`.docx` de `downloads` pese a que el manifiesto ya registra al menos un
payload real en ese formato (`indice_de_bienestar_cuestionarios`, raíz
`descargas_mx`, un cuestionario ENSANUT). No se amplió el filtro
unilateralmente — el encargo da la lista exacta a usar — pero se declara el
hueco: si alguno de esos 210 `.docx` es un payload real, este censo no lo
vería. Fuera de este acto decidir si se justifica un barrido `.docx` aparte.

**Segunda capa de exclusión, solo en `downloads`, solo para el hash — patrón
`takeout-*`:** 37 archivos, 55 977 532 311 bytes (≈ 52.1 GiB) — el 93% de los
bytes que el filtro de extensión había dejado dentro. Son exportaciones
personales de Google Takeout (nombre de herramienta inconfundible; ~37
archivos de ~2 GiB cada uno, escala de un respaldo completo de cuenta, cero
relación temática con microdato de encuesta). No se hashean — hacerlo habría
dominado el tiempo de corrida por valor forense nulo — pero **sí quedan
listados** en el TSV (bytes, mtime, `sha256=NO_HASHEADO_google_takeout_personal`,
`en_manifiesto=no` trivial) para que el conteo de filas siga siendo honesto.
El resto de `downloads` (WhatsApp/Instagram/Facebook/iCloud/"Fire TV", varios
cientos de MB) sí se hasheó normal — no domina el tiempo de corrida y no hay
razón para tratarlo distinto.

**Por carpeta (todas las cifras, comando a la vista arriba):**

| raíz | archivos censados | bytes | extensiones distintas |
|---|---|---|---|
| `data_raw` | 488 | 6 732 970 093 (6.27 GiB) | 7 — csv html pdf xls xlsx xml zip |
| `descargas_mx` | 34 | 60 162 303 (57.4 MiB) | 5 — docx pdf php xlsx zip |
| `downloads` (hasheados) | 341 | 3 793 036 884 (3.53 GiB) | 4 — csv pdf xlsx zip (cero dta/dbf/sav/xml) |
| `downloads` (listados sin hash, takeout) | 37 | 55 977 532 311 (52.1 GiB) | — |

TSV: `data/censo-raices-2026-08-06.tsv`, 900 filas + cabecera (863 con hash +
37 takeout sin hash). Manifiesto: 461 entradas, 457 con payload, 457 sha256
distintos (sin colisión interna).

## PASO 3 — El cruce, en las dos direcciones

### A · Huérfanos (archivo en disco, ninguna entrada lo declara por sha256)

Solo `data_raw` y `descargas_mx` — `downloads` no es raíz del programa, sus
candidatos van aparte en (E), como pide el encargo ("es información
distinta"). **64 huérfanos, lista completa:**

**`descargas_mx` (2):**
- `DescargaMasiva_582026_175614.zip` — otra generación bajo demanda del
  paquete "Descarga Masiva" del portal (mismo patrón que documentó DESC-1:
  el portal genera un zip nuevo, con nombre nuevo, cada vez que se solicita;
  no expone URL persistente). Contenido no verificado contra ningún otro
  paquete ya registrado — no se abrió el zip, está fuera de perímetro.
- `descargas.php` — página guardada del portal, no dato. El propio código
  (`tests/manifiesto.py`, `EXTENSIONES_PAGINA = {".php", ".html", ".htm"}`,
  línea 453) la trata como evidencia de procedencia, no como payload; 48
  entradas del manifiesto citan literalmente "derivada de descargas.php por
  --escanea" en su procedencia. Consistente con que nunca se registró aparte.

**`data_raw` (62):**
```
DescargaMasivaOD_582026_171540_NACIONAL_7930url.xml
R7.3_PUB_Bienestar/padron_unico_bienestar.csv
R1_1_AGROASEMEX/PAA_componente_apoyo.csv
R1_1_AGROASEMEX/PAA_componente_subsidio_ramo_agricola.csv
R1_1_AGROASEMEX/PAA_componente_subsidio_ramo_ganadero.csv
R1_1_AGROASEMEX/padron_integrantes_sistema_nacional_aseguramiento_agropecuario.csv
R2.1_ECCO/SE_REPORTE_GENERAL_ECCO_2023.pdf
R7.4_R7.5_ACLED_HDX/mexico_demonstration_events_by_month-year.xlsx
inegi_mmsi_2016/cuestionario_mmsi_2016.pdf
inegi_mmsi_2016/manual_entrevistador_mmsi_2016.pdf
R8.1_contraloria_social/contraloria_social_2019_2025.csv
endireh2016/bd_mujeres_endireh2016_sitioinegi_dbf.zip          (*)
enaproce2018/ejem_base_micro_ciega_csv.zip                     (**)
enaproce2018/ejem_base_micro_ciega_dta.zip                     (**)
enaproce2018/ejem_base_pyme_ciega_csv.zip                      (**)
enaproce2018/ejem_base_pyme_ciega_dta.zip                      (**)
engasto2012/gasto_dbf.zip                                      (***)
engasto2012/gasto_de_consumo_ajustado_constante_dbf.zip        (***)
engasto2012/gasto_de_consumo_ajustado_constante_dta.zip        (***)
engasto2012/gasto_de_consumo_ajustado_constante_sav.zip        (***)
engasto2012/gasto_de_consumo_ajustado_dbf.zip                  (***)
engasto2012/gasto_de_consumo_ajustado_dta.zip                  (***)
engasto2012/gasto_de_consumo_ajustado_sav.zip                  (***)
engasto2012/gasto_dta.zip                                      (***)
engasto2012/gasto_mujeres_dbf.zip                               (***)
engasto2012/gasto_mujeres_dta.zip                               (***)
engasto2012/gasto_mujeres_sav.zip                               (***)
engasto2012/gasto_sav.zip                                       (***)
engasto2012/hogar_dbf.zip                                       (***)
engasto2012/hogar_dta.zip                                       (***)
engasto2012/hogar_sav.zip                                       (***)
engasto2012/persona_dbf.zip                                     (***)
engasto2012/persona_dta.zip                                     (***)
engasto2012/persona_sav.zip                                     (***)
envipe2023/bd_envipe_2023_dta.zip                                (*)
envipe2023/bd_envipe_2023_sav.zip                                (*)
R9_1_ENSANUT_utilizadores/ensanut_2018_utilizadores_servicios_salud.pdf
ennvih/doc/ehh02cb_b2.pdf
ennvih/doc/ehh02cb_b3a.pdf
ennvih/doc/ehh02cb_b3b.pdf
ennvih/doc/ehh02cb_bc.pdf
ennvih/doc/ehh02q_b2.pdf
ennvih/doc/ehh02q_b3a.pdf
ennvih/doc/ehh05cb_b2.pdf
ennvih/doc/ehh05cb_b3a.pdf
ennvih/doc/ehh05cb_b3b.pdf
ennvih/doc/ehh05cb_bc.pdf
ennvih/doc/ehh05q_b2.pdf
ennvih/doc/ehh05q_b3a.pdf
ennvih/doc/ehh09cb_b2.pdf
ennvih/doc/ehh09cb_b3a.pdf
ennvih/doc/ehh09cb_b3b.pdf
ennvih/doc/ehh09cb_bc.pdf
ennvih/doc/ehh09q_b2.pdf
ennvih/doc/eloc02cb_bcc.pdf
ennvih/doc/eloc02q_bcc.pdf
ennvih/doc/eloc05cb_bcc.pdf
ennvih/doc/eloc05q_bcc.pdf
ennvih/doc/eloc09cb_bcc1.pdf
ennvih/doc/eloc09cb_bcc2.pdf
ennvih/doc/eloc09q_bcc1.pdf
R4_1_SESTAD_ESTAD/SESTAD_reporte_2021.pdf
```

`(*)` **Estas 3 rutas NO son huérfanos simples — son la misma ruta que
declaran las 3 entradas COLGADAS de la categoría B.** Ver ahí: el archivo que
hoy ocupa esa ruta exacta no es el que el manifiesto registró. Se listan aquí
también porque, por contenido (sha256), el archivo actual no tiene entrada —
es la vista "desde el archivo" del mismo hecho que B ve "desde la entrada".

`(**)` **Discrepancia con `forense/notas/2026-08-05-desc1-descarga.md`,
verificada, no adjudicada.** Esa nota (línea ~124) afirma que los `csv`/`dta`
de `enaproce2018` son "byte-idénticos (mismo sha256)" a los de `enaproce2015`
y que por eso el registro los rechazó por deduplicación. Medido hoy,
independiente, con `sha256sum` (no solo el script de censo):
```
$ sha256sum /home/pc0/mm-corpus/raw/enaproce2018/ejem_base_micro_ciega_csv.zip
2df2046ac8d5791574fd1e68c124215f3810eadd538714b9f36cda948d4f2ef2
$ sha256sum /home/pc0/mm-corpus/raw/enaproce2015/ejem_base_micro_ciega_csv.zip
01aafb888b447badb8506ef6cf7562a885a69c666561e61fccd178903d758623
```
Distintos, y de tamaño distinto (5704 B vs 4006 B) — no son el mismo archivo.
El manifiesto sí registra 6 entradas `enaproce_2015_*` (csv/dbf/dta × micro/pyme,
apuntando a `enaproce2015/`) y 4 `enaproce_2018_*` (sav/xlsx × micro/pyme,
apuntando a `enaproce2018/`) — pero ninguna cubre los 4 `csv`/`dta` de 2018
listados arriba. No hay evidencia de que el archivo haya cambiado desde que
DESC-1 escribió su nota — solo que la medición de hoy no reproduce lo que esa
nota afirma. Se declara el conflicto; no se investiga más, está fuera de este
perímetro.

`(***)` **Mismo patrón, misma nota DESC-1, también no reproducido.** La nota
afirma "ENGASTO 2013 reutiliza 18 de sus 21 archivos de microdato,
byte-por-byte, de ENGASTO 2012". Verificado hoy, las 18 parejas
`engasto2012/<nombre>` vs `engasto2013/<nombre>` tienen sha256 **distinto**
en las 4 muestreadas a mano (`gasto_dbf`, `gasto_de_consumo_ajustado_constante_dbf`,
`hogar_dbf`, `persona_dbf`) y, por el cruce automatizado (categoría D más
abajo no las lista como duplicadas), en las 18. El manifiesto registra 18 ids
`engasto_2012_*` cuyo campo `archivo` apunta a `engasto2013/...` (no a
`engasto2012/...`) — es decir, el nombre del id dice "2012" pero el payload
registrado, hoy, vive físicamente en la carpeta `2013`. Las 18 rutas físicas
`engasto2012/*` correspondientes quedan huérfanas por contenido. Mismo aviso
que en `(**)`: se declara el conflicto contra la nota previa, no se resuelve.

Conexión ya documentada (no es hallazgo nuevo, se cita para no duplicar
trabajo): los directorios con punto en el nombre (`R7.3_PUB_Bienestar`,
`R2.1_ECCO`, `R7.4_R7.5_ACLED_HDX`, `R8.1_contraloria_social`) son exactamente
los que memoria de sesión previa liga al bloqueo de T02 en `tests/check.py`
(`IsADirectoryError`) — TC-1 lo tiene declarado y en su perímetro, no en el
mío.

### B · Colgadas (entrada en el manifiesto, ningún archivo censado la respalda por sha256)

**3 de 457** entradas con payload — lista completa:

| id | raíz declarada | archivo | sha256 manifiesto (prefijo) |
|---|---|---|---|
| `endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf` | data_raw | `endireh2016/bd_mujeres_endireh2016_sitioinegi_dbf.zip` | `784410e6b99c99b5…` |
| `envipe_2023_bd_envipe_2023_dta` | data_raw | `envipe2023/bd_envipe_2023_dta.zip` | `4a7110bea2f23a83…` |
| `envipe_2023_bd_envipe_2023_sav` | data_raw | `envipe2023/bd_envipe_2023_sav.zip` | `9c8da8e7e0b44c3d…` |

Las tres son de la misma tanda: escritas por el commit `ae4910b`
("ENCARGO DESC-1: descarga priorizada TRAMO A+B...", 2026-08-05 19:05:57).
No están AUSENTES — su ruta exacta está ocupada por otro archivo, con otro
tamaño y otro sha256:

| id | tamaño manifiesto | tamaño real hoy | mtime real |
|---|---|---|---|
| `endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf` | 2 895 872 B | 102 349 631 B | 2026-08-05T18:45:47 |
| `envipe_2023_bd_envipe_2023_dta` | 16 221 003 B | 9 289 283 B | 2026-08-05T19:14:21 |
| `envipe_2023_bd_envipe_2023_sav` | 26 786 689 B | 21 495 362 B | 2026-08-05T19:17:21 |

Para las dos de ENVIPE, el mtime real es *posterior* al commit que las
registró (19:05:57) — el archivo en esa ruta se sobrescribió después de
registrarse, sin volver a verificar. Un `--verifica --id <id>` sobre
cualquiera de las tres reportaría `NO COINCIDE` hoy mismo (existe, no
coincide), no `AUSENTE` — la herramienta ya puede detectar esto, solo no se
ha corrido sobre estos tres ids desde que ocurrió. No se especula más sobre
el mecanismo exacto (mover/sobrescribir/re-descargar) — eso excede este
perímetro.

### C · Raíz declarada no coincide con dónde vive el archivo

**Cero.** De las 454 entradas con payload cuyo sha256 sí se localizó en algún
punto del censo (457 menos las 3 COLGADAS de B), las 454 aparecieron
exactamente bajo la raíz que declaran (o, si no declaran `raiz`, bajo
`data_raw`). Esto cierra empíricamente la pregunta que quedó abierta en el
PASO 1: la convención "ausencia de `raiz` significa `data_raw`" se sostuvo,
sin excepción, en el 100% de los casos verificables hoy. No dice nada sobre
las 3 COLGADAS (no se pudieron verificar por no tener contenido localizable).

### D · Mismo sha256 en dos rutas (duplicación física)

**33 grupos, 728 393 453 bytes (694.7 MiB) de espacio redundante en total.**
Se separan en dos clases — no es el mismo hecho:

**Relevantes al programa (5 grupos, 87 966 518 B ≈ 83.9 MiB):**

| sha256 (prefijo) | archivo | rutas | bytes c/u |
|---|---|---|---|
| `af733d86…` | `encig23_base_datos_csv.zip` | `data_raw` + `downloads` | 38 309 647 |
| `ff39bb1d…` | `ITER_NAL_2020_csv.zip` | `data_raw` + `descargas_mx` | 36 604 573 |
| `0414fd59…` | `BD_ENCUCI2020_dbf.zip` | `data_raw` + `descargas_mx` | 6 913 684 |
| `9737a557…` | `eder2025/889463930242.pdf` = `eder2025/eder2025_descripcion_bd.pdf` | dos nombres, ambos dentro de `data_raw` | 4 380 365 |
| `6cd6f747…` | `FD_ENCUCI2020.pdf` | `data_raw` + `descargas_mx` | 1 758 249 |

Patrón consistente: el mismo payload sobrevive en `data_raw` (integrada,
donde quedó registrado) y también en `descargas_mx`/`downloads` (de donde se
originó o se curó) — coherente con el flujo de trabajo del proyecto, no un
error de por sí, pero es espacio duplicado real si alguna vez se quiere
recuperar.

**Ruido personal de `downloads` (28 grupos, ≈610.8 MiB):** copias
repetidas del mismo archivo bajado dos o más veces por el navegador (sufijo
"(1)", "(2)"…) — capturas de Instagram/Facebook, exports de WhatsApp,
plantillas de diseño ("mesa-de-luz-…"), hojas de cálculo de seguimiento
personal, cuadernos de preescritura, etc. Ninguno de los 28 tiene relación
temática con microdato de encuesta. Detalle completo en el TSV (agrupar por
`sha256` reproduce exactamente esta lista); no se transcribe aquí por ser,
en su totalidad, ajeno al programa — transcribir 28 nombres de archivos
personales del usuario no añade nada que el TSV no tenga ya.

### E · Archivos en `downloads` que parecen payloads del programa

De los 341 archivos hasheados en `downloads`, **13 son candidatos**
(patrón de nombre: sigla de encuesta/programa conocida en este proyecto).
Los otros 328 no matchean ningún patrón reconocible del proyecto.

**1 ya es copia, no huérfano** (mismo hallazgo que D):
`encig23_base_datos_csv.zip`, sha256 `af733d86…`, ya registrado como
`encig23_base_datos_csv` bajo `data_raw`.

**12 son candidatos genuinamente nuevos** — sha256 no aparece en el
manifiesto bajo ninguna id, y tampoco hay ninguna entrada cuyo campo
`archivo` cite ese nombre de archivo (verificado por ambas vías, no solo por
hash). Los 12 son variantes en formato SPSS/Stata de payloads ENSANUT 2024
que sí están registrados en otros formatos (csv/catálogo, bajo
`descargas_mx`):

```
NSE_Hogar_ENSANUT_2024.spss.spss.zip
NSE_Hogar_ENSANUT_2024.stata.stata.zip
NSE_Integrantes_ENSANUT_2024.spss.spss.zip
NSE_Integrantes_ENSANUT_2024.stata.stata.zip
adolescentes_ensanut2024_w.spss.spss.zip
adultos_ensanut2024_w.spss.spss.zip
hogar_ensanut2024_w_ICB.spss.spss.zip
hogar_ensanut2024_w_ICB.stata.stata.zip
integrantes_ensanut2024_w_ICB.spss.spss.zip
integrantes_ensanut2024_w_ICB.stata.stata.zip
menores_ensanut2024_w.spss.spss.zip
utilizadores_ensanut2024_w.spss.spss.zip
```

No se decide aquí si valen la pena registrar (son formatos alternativos del
mismo dato ya presente en csv, no dato nuevo en sentido estricto) — queda
para quien priorice el manifiesto.

### Contador de PASO 3

**64 huérfanos** (62 data_raw + 2 descargas_mx) · **3 colgadas** · **0
raíz-no-coincide** · **33 grupos duplicados** (5 relevantes + 28 ruido
personal) · **13 candidatos en downloads** (1 copia + 12 nuevos).

## PASO 4 — Propuestas, sin ejecutar

Nota de alcance: la mayoría de los 64 huérfanos (A) y las 3 colgadas (B) no
piden un *movimiento* — piden registro (A) o re-verificación/re-registro (B),
que son ediciones de `data/manifiesto.yaml`, fuera de mi perímetro y de lo
que esta tabla cubre. Lo que sigue es estrictamente relocalización física
entre raíces, justificada por lo que el censo ya muestra.

| archivo | de | a | por qué |
|---|---|---|---|
| `encig23_base_datos_csv.zip` | `downloads` | *(eliminar la copia; ya vive en `data_raw`, registrada)* | Categoría D — mismo sha256, `data_raw` es la raíz integrada y la que el manifiesto ya cita. Libera 38 309 647 B en una carpeta que no es de datos. |
| `ITER_NAL_2020_csv.zip` | `descargas_mx` | *(eliminar la copia; ya vive en `data_raw`, registrada)* | Categoría D. Libera 36 604 573 B. |
| `BD_ENCUCI2020_dbf.zip` | `descargas_mx` | *(eliminar la copia; ya vive en `data_raw`, registrada)* | Categoría D. Libera 6 913 684 B. |
| `FD_ENCUCI2020.pdf` | `descargas_mx` | *(eliminar la copia; ya vive en `data_raw`, registrada)* | Categoría D. Libera 1 758 249 B. |
| `eder2025/889463930242.pdf` | `data_raw` (nombre numérico) | *(eliminar; duplicado interno de `eder2025/eder2025_descripcion_bd.pdf`, misma raíz)* | Categoría D — incluso dentro de `data_raw` hay dos nombres para el mismo contenido; el nombre descriptivo ya es lo que probablemente se usa. |
| 12 archivos ENSANUT 2024 `.spss.spss.zip`/`.stata.stata.zip` (lista completa en categoría E) | `downloads` | `descargas_mx` | Sus formatos hermanos (csv/catálogo) de los mismos instrumentos ya viven registrados en `descargas_mx` — `downloads` es "destino por defecto del navegador... NO es una carpeta de datos" (docstring del propio script, línea 66-67). Mover, no registrar: el registro es decisión de quien priorice el manifiesto. |

Deliberadamente NO propuesto: mover cualquiera de los 62 huérfanos de
`data_raw` o los otros archivos de `descargas_mx`/`downloads` — ninguno tiene
hoy un conflicto de raíz (categoría C dio cero), así que no hay "raíz
incorrecta" que corregir moviendo; lo único que les falta es una entrada. Ni
las 3 colgadas — mover algo no resuelve que el contenido registrado ya no
esté en ningún lado; eso es una decisión sobre qué hacer con el registro, no
sobre dónde vive un archivo.

## ACTUALIZACIÓN — `origin/main` avanzó durante este acto

Todo lo anterior (arranque, PASO 1-4) se derivó contra la base declarada,
`58a307c`. Al llegar a PASO 5, `git fetch origin` mostró que `origin/main`
había avanzado: TC-1 (PR #144) y la reconciliación de CONF-17 sobre
`data/manifiesto.yaml` (PR #143) se fusionaron mientras este acto corría —
exactamente los dos actos concurrentes que el encargo declaró. Por
instrucción explícita del encargo ("si main se movió NO es PARO — refresca,
re-deriva, reporta la diferencia"), esto es lo que se hizo, en este orden:

```
$ git fetch origin && git log HEAD..origin/main --oneline
21cf521 Merge pull request #144 from Josanoforo/tc1-corpus-010528-2
b649995 forense/hallazgos.md: cierre de ENCARGO TC-1
...
5096c84 Merge origin/main: incorpora reconciliación de CONF-17 (PR #143)
...
$ git diff --stat 58a307c origin/main
 data/manifiesto.yaml | 8937 ++++++++++++--------
 tests/check.py       |    9 +-
 ... (7 archivos, 7005(+)/3722(-))
$ git merge origin/main --no-edit
Updating 58a307c..21cf521
Fast-forward
```
Fast-forward limpio, sin conflicto — mis dos archivos nuevos (`data/censo-raices-2026-08-06.tsv`,
esta nota) no chocan con nada que llegara de origin.

**Qué NO hubo que rehacer:** los archivos físicos de las tres raíces no se
tocaron por este merge (el diff solo toca archivos versionados del repo) —
el TSV completo (863 filas con hash) sigue siendo válido tal cual, cero
rehash.

**Qué sí se re-derivó:** las columnas `en_manifiesto`/`id_manifiesto` del TSV
(recalculadas contra el `data/manifiesto.yaml` ya fusionado, sin volver a
hashear un solo archivo) y el cruce B/C/D/E completo.

**La diferencia, precisa:**
- Manifiesto: 461→**471** entradas, 457→**467** con payload, sin `raiz`:
  400→**410** (payload) / 404→**414** (total). El mecanismo y la fecha de
  origen del campo (PASO 1) no cambian — solo el conteo actual.
- **Categoría A (huérfanos):** las 10 entradas nuevas que trajo CONF-17 son,
  exactamente, 10 de los 62 huérfanos de `data_raw` que este acto ya había
  encontrado (`R7.3_PUB_Bienestar`, las 4 de `R1_1_AGROASEMEX`, `R2.1_ECCO`,
  `R7.4_R7.5_ACLED_HDX`, `R8.1_contraloria_social`,
  `R9_1_ENSANUT_utilizadores`, `R4_1_SESTAD_ESTAD`) — confirmado id por id,
  no por coincidencia de conteo. **Huérfanos corregidos: 54** (52 en
  `data_raw` + 2 en `descargas_mx`, sin cambio). Lista `data_raw` completa,
  52:
  ```
  DescargaMasivaOD_582026_171540_NACIONAL_7930url.xml
  inegi_mmsi_2016/cuestionario_mmsi_2016.pdf
  inegi_mmsi_2016/manual_entrevistador_mmsi_2016.pdf
  endireh2016/bd_mujeres_endireh2016_sitioinegi_dbf.zip                (*)
  enaproce2018/ejem_base_micro_ciega_csv.zip                           (**)
  enaproce2018/ejem_base_micro_ciega_dta.zip                           (**)
  enaproce2018/ejem_base_pyme_ciega_csv.zip                            (**)
  enaproce2018/ejem_base_pyme_ciega_dta.zip                            (**)
  engasto2012/gasto_dbf.zip … (18 rutas engasto2012/*, sin cambio)      (***)
  envipe2023/bd_envipe_2023_dta.zip                                     (*)
  envipe2023/bd_envipe_2023_sav.zip                                     (*)
  ennvih/doc/*.pdf (25 rutas, sin cambio)
  ```
  `(*)`/`(**)`/`(***)` remiten a las mismas notas ya escritas en PASO 3-A —
  ninguna de las tres cambió con la fusión.
- **Categorías B, C, D, E: sin cambios.** Re-corridas contra el manifiesto
  fusionado, mismo resultado exacto: 3 colgadas (las mismas 3 ids), 0
  raíz-no-coincide, 33 grupos duplicados (los mismos 33 sha256), 13
  candidatos en `downloads` (los mismos 13). CONF-17 no tocó ninguna de las
  rutas o ids involucrados en B/C/D/E.
- **PASO 4 (movimientos propuestos):** sin cambios — ninguno de los 10 ids
  que CONF-17 agregó aparecía en la tabla de movimientos.
- **Suite:** el fix de TC-1 a `tests/check.py` (excluye `data/raw` de T02,
  commit `c9d37d8`) resuelve exactamente el `IsADirectoryError` que este
  acto iba a declarar como bloqueo ajeno — ver PASO 5, ya no hace falta
  declarar nada, la suite corre limpia.

El TSV en disco ya refleja el estado post-fusión (columnas
`en_manifiesto`/`id_manifiesto` recalculadas in situ); esta sección es el
registro de qué cambió y por qué, no una corrección silenciosa de los
números de PASO 1-4 arriba — esos quedan como se derivaron, contra la base
que tenían.

**Recomendación sobre las 404 entradas sin `raiz`, en tres líneas:**
Declarar el default en el código — ya está declarado (`RAIZ_INTEGRADA`,
`tests/manifiesto.py:158`, con comentario) y el cruce de este mismo acto
(categoría C: 0 de 454 verificables) confirma que se sostiene sin excepción
hoy. Añadir `raiz: data_raw` a 400+ entradas sería boilerplate puro sobre
algo que `--registra` no puede escribir de otra forma (PASO 1-b) — no cambia
ningún comportamiento verificable, solo infla el archivo. Lo único que sí
valdría una línea de cambio (no 400) es que el docstring deje de enmarcar la
omisión como deuda histórica de "53 entradas anteriores al campo" (líneas
72-74) y diga que es la convención permanente para toda entrada en
`data_raw` — pero eso es editar `tests/manifiesto.py`, fuera de este
perímetro, y queda como sugerencia, no como acción de este acto.

## PASO 5 — Suite y cierre

`python3 tests/check.py --baseline`, corrido después de la fusión con
`origin/main` (antes de fusionar, la misma corrida terminaba en
`IsADirectoryError` sobre `R7.3_PUB_Bienestar` — el bloqueo T02 que TC-1 ya
había declarado y arreglado en `origin/main`, commit `c9d37d8`, mientras este
acto corría):

```
T01 ok · T02 ok · T03 warn(29) · T04 ok · T05 FAIL(5) · T06 FAIL(2) ·
T07 FAIL(1) · T08 FAIL(1) · T09 FAIL(8) · T10 warn(65) · T11 FAIL(1) ·
T12 ok · T13 warn(1) · T14 ok · T15 ok · T16 ok · T17 ok · T18 ok · T19abc ok
· T20 ok
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
(HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```
Exit code 0. Todos los FAIL/WARN son preexistentes (el propio script lo dice:
"nada nuevo") — ninguno originado por este acto, que no tocó `canon/`,
`corpus/reports/`, ni el motor. La compuerta ("la suite no empeora por causa
de este acto") se cumple limpio, sin necesidad de declarar excepción alguna.

**Contador: 0**, declarado desde el encabezado — este es un acto de censo,
no de medición. Lo que entrega: **54 huérfanos** (52 `data_raw` + 2
`descargas_mx`, dos de ellos con discrepancia verificada contra una nota
previa — PASO 3-A), **3 colgadas** (mismo commit, `ae4910b`, contenido
sobrescrito sin re-registrar — PASO 3-B), **0 raíz-no-coincide** (cierra
empíricamente la pregunta abierta en PASO 1), **33 grupos de duplicación
física** (5 relevantes al programa, ≈84 MiB; 28 ruido personal de
`downloads`, ≈611 MiB), **13 candidatos en `downloads`** (1 copia ya
conocida, 12 nuevos — variantes SPSS/Stata de ENSANUT 2024).
