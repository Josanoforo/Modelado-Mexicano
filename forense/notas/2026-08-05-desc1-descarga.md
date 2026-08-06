# ENCARGO DESC-1 — descarga priorizada desde el XML de canasta (2026-08-05)

Worktree `/home/pc0/wt-desc1`, rama `desc1-descarga`, base `f0cb60e` (verificado: `git rev-parse HEAD` = `f0cb60efb5b20d01af8a9be15e6b54dded99289e`, `git worktree list` lo confirma junto a `wt-ver1` y `wt-conf17` corriendo en paralelo).

`data/raw` no existía en el worktree nuevo — se enlazó al corpus compartido: `ln -s /home/pc0/mm-corpus/raw /home/pc0/wt-desc1/data/raw` (mismo patrón que `wt-ver1`/`wt-conf17`).

## ARRANQUE §4 — firma de entorno (cuatro valores crudos)

```
$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200
$ ls data/raw/ 2>/dev/null | head -1
BD_ENCUCI2020_dbf.zip
$ df -h /home/pc0 | tail -1
/dev/sdd       1007G  7.1G  949G   1% /home/pc0
```

Los cuatro valores están dentro de lo esperado. No hay PARO.

## PASO 0 — localización y verificación del XML por contenido (REGLA A.7)

El único XML ya presente en el corpus compartido (`mm-corpus/raw/DescargaMasivaOD_382026_131650.xml`) **NO es la canasta nacional de este encargo**: verificado por contenido da 576 URLs, 8.23 GB, todas bajo `/programas/ccpv/2020/` — es una canasta de CPV 2020 solamente, generada el 3/ago. Esto no es el caso "misma canasta, `aut` distinto" de REGLA A.7 — es una canasta *distinta* (otro alcance, no solo otro token). Se documenta como hallazgo (ver `forense/hallazgos.md`), el archivo NO se toca (no es destructivo tocarlo, pero no es el insumo de este acto).

La canasta nacional (7,930 URLs) se localizó en `/mnt/c/Users/PC0/Downloads/DescargaMasiva_582026_17154.zip` (generada hoy, 5/ago, 17:15), dentro del zip como `DescargaMasivaOD.xml`:

```
$ python3 -c "
import zipfile
z = zipfile.ZipFile('/mnt/c/Users/PC0/Downloads/DescargaMasiva_582026_17154.zip')
for i in z.infolist(): print(i.filename, i.file_size)"
DescargaMasivaApp.exe 850432
leeme.txt 434
DescargaMasivaOD.xml 1010608
```

Verificación por contenido (script del encargo, sobre el XML extraído):

```
bytes 1010608
sha256 crudo    ebd66f3dd4975252bf18f28e8495cb9be2a2f66c8ca538dcaef339dbbcbbcb8d
sha256 sin aut  4687abd60d236aebc21c7f4daf07e5f19f36cd188ac8a3856d6b1fe630f5ed1f
sha256 set URL  9a98e161fea26a553cc8910af2a36329ccd1f7e53620bee796ff4247ba7efa20
urls unicas 7930
aut token: cf4f56bb-d7cc-4cfd-a749-132dcc21a662
totalMb: 51.00 GB
```

Los tres hashes coinciden EXACTOS con los valores de control de mesa (sin aut `4687abd6...`, set de URLs `9a98e161...`, 7,930 URLs). El `aut` (`cf4f56bb-…`) coincide incluso con el primero de los dos citados en el encargo — es el mismo archivo, bit a bit, no solo el mismo contenido. Sin PARO.

Se encontró una segunda copia, más tardía, en `/mnt/c/Users/PC0/Descargas MX/DescargaMasiva_582026_175614.zip` (17:56, 41 min después): mismo tamaño (1,010,608 bytes), mismo `sha256 sin aut` y `sha256 set URL` — caso limpio de REGLA A.7 (misma canasta regenerada, `aut` distinto), confirmado empíricamente, no solo citado.

El XML verificado se copió al corpus compartido bajo un nombre que no colisiona con el archivo viejo/erróneo: `mm-corpus/raw/DescargaMasivaOD_582026_171540_NACIONAL_7930url.xml` (sha256 `ebd66f3d…`, idéntico al crudo).

## PASO 1 — índice completo (`data/indice-descarga-masiva-2026-08-05.tsv`, 7,930 filas)

Columnas: `url · programa · anio · carpeta · archivo · formato · en_manifiesto · bytes_declarados`.

- `programa`: segmento crudo tras `/programas/` (sensible a mayúsculas — ver hallazgo `Cnije`/`cnije` abajo). 420 URLs no cuelgan de `/programas/` (viven bajo `/investigacion/bienestar/`, `piloto` y `ampliado`) — reportadas aparte, `programa` vacío, NO descartadas.
- `carpeta`: `microdatos|doc|otro`, detectado case-insensitive (había 2 URLs con `Microdatos` en mayúscula que un primer intento case-sensitive clasificó mal como `otro`; corregido). Resultado: 7,632 microdatos · 296 doc · 1 otro genuino (`caas/2015/tabulados/...`, carpeta `tabulados`, no microdatos/doc).
- `anio`: primer token de 4 dígitos (19xx/20xx) en cualquier segmento de la ruta o el nombre de archivo.
- 72 URLs son duplicadas dentro del XML (8,002 tags `<Archivo>`, 7,930 únicas tras dedup) — reportado, no oculto.

### Reconciliación de las dos cifras que la receta de mesa no reprodujo

- **"137 programas"**: mi TSV da **136 slugs distintos bajo `/programas/`** (sensibles a mayúscula/minúscula: 135 si se normaliza a minúsculas, porque `cnije`/`Cnije` son el mismo programa con dos grafías) **+ 1 categoría fuera de `/programas/`** (las 420 de `/investigacion/bienestar/`) **= 137**. Coincide exacto con la cifra de mesa.
- **"Microdatos 4,928" (pestaña) vs 7,930 (XML)**: mi propio conteo de `carpeta=microdatos` da **7,632**, que tampoco es 4,928 ni 7,930 — consistente con el marco del encargo (la pestaña cuenta *títulos* de conjunto de datos, el XML/mi TSV cuentan *archivos* individuales; no son la misma unidad y no se fuerza a que coincidan).

### Hallazgo: `Cnije`/`cnije`, defecto de mayúsculas en la canasta

La lista de exclusión ⛔ del encargo suma 2,427 URLs usando `cnije: 346` — y mi TSV confirma exactamente ese número **para el slug en minúsculas**. Pero hay **20 URLs adicionales bajo `Cnije` (con mayúscula)**, del mismo programa (Censo Nacional de Impartición de Justicia Estatal, 2012), que quedan **fuera** de esa suma de 2,427 porque el conteo de mesa usó el slug literal. Total real de justicia/gobierno con este único programa correctamente unificado: 2,447 URLs, no 2,427. Se reporta la diferencia, no se resuelve (no se tocan esas URLs — siguen fuera del perímetro de descarga de este acto en cualquier caso).

## PASO 2 — sondeo de tamaños (antes de bajar un byte)

### TRAMO A (72 URLs: encuci·enif·endutih·elcos·enasic·eder·enaproce·enestyc)

```
$ cat tramoA_urls.txt | xargs -P 6 -I{} curl -sL -r 0-0 -D - -o /dev/null --max-time 30 "{}" | ...
```

72/72 sondeos con código 200. Presupuesto por programa:

| programa | MiB |
|---|---|
| eder | 197.6 |
| endutih | 26.9 |
| enif | 14.2 |
| encuci | 8.3 |
| elcos | 4.0 |
| enasic | 3.8 |
| enestyc | 0.2 |
| enaproce | 0.1 |
| **TOTAL** | **~255 MiB (0.25 GB)** |

Muy por debajo del umbral de 20 GB. Se procede a bajar TRAMO A completo.

### TRAMO B (214 URLs: envipe·mociba·encig·endireh·engasto)

214/214 sondeos con código 200, 0 fallas. Presupuesto por programa:

| programa | GB |
|---|---|
| engasto | 1.122 |
| endireh | 1.076 |
| envipe | 0.715 |
| encig | 0.564 |
| mociba | 0.057 |
| **TOTAL** | **3.534 GB** |

Muy por debajo del umbral de 20 GB. Se procede a bajar TRAMO B completo.

## PASO 3/4 — descarga y revisión estructural, TRAMO A

Cruce contra el corpus antes de bajar: 12/72 ya presentes (de actos previos), 60 faltantes. Los 60 se bajaron por curl directo (ver `tests/manifiesto.py --registra`, campo `descargado_por`); 1 intento inicial falló por conexión (`ejemplobd_enestyc_1999_dbf.zip`, code=000) y se reintentó con éxito (code=200, 7895 bytes — coincide exacto con el sondeo previo). 72/72 confirmados en disco tras el reintento.

Revisión estructural (sha256, sniff de tipo por magic bytes, `zipfile.namelist()`, encabezado crudo de cada CSV dentro de cada zip — **sin abrir filas de microdato**, ADR-46):

- **eder** (2011/2017/2025, 34 URLs): tablas consistentes entre olas (`persona/vivienda/antecedentes/historiavida/hogar`, +`domestico/informante/salud` desde 2025). Universo declarado, literal del descriptor 2025: encuesta longitudinal, reconstrucción de historia de vida de personas de 18 a 64 años, sobre migración/educación/trabajo/nupcialidad/fecundidad/mortalidad/anticoncepción/discapacidad. Para 2017 se buscó "universo"/"cobertura"/"objetivo" en los dos PDF de documentación (texto completo, `pdftotext`) y no aparece ninguna coincidencia literal — NO LOCALIZADO EN ESTE PAYLOAD, no se inventa. El descriptor 2011 (`.xls` OLE binario antiguo) no se pudo leer en este entorno (falta `xlrd`).
- **elcos** (2 URLs): ya estaban registrados por otro acto (M-3 ya lo auditó, per el encargo). Confirmado el hueco: no se reabre.
- **enasic** (3 URLs): 2 ya registrados; se registró el PDF nuevo (`889463927082.pdf`). Universo declarado, literal: "la base de datos de la Enasic 2022 tiene como objetivo ofrecer... los microdatos para la generación de información relacionada con la necesidad de cuidados en los hogares..." — cinco factores de expansión distintos (vivienda/hogares/cuidadoras/población seleccionada 15-60/hogares unipersonales); una misma persona puede estar en más de un universo.
- **encuci** (2 URLs): ambos ya registrados por otro acto. Confirmado que **no** es "solo doc" pese a ser solo 2 URLs — es 1 zip de microdatos + 1 PDF descriptor, la oferta completa de ENCUCI 2020 en esta canasta (regla A.5 satisfecha: no es un defecto de la canasta, es la estructura real del programa).
- **endutih** (6 URLs, 2023/2024/2025): 2024 ya registrado; 2023 y 2025 se registraron nuevos. Mismas 5 tablas por ola (`tic_AAAA_viviendas/hogares/residentes/usuarios/usuarios2`). No se localizó párrafo de universo/objetivo en las primeras filas de la hoja índice de ningún FD.
- **enaproce** (14 URLs, 2015/2018): **ADVERTENCIA reportada, no adjudicada** — todos los archivos de microdatos de este programa en esta canasta llevan "ejemplo"/"ciega" en el nombre (`ejem_base_micro_ciega_*`, `ejem_base_pyme_ciega_*`) y pesan 4–33 KB descomprimidos — tamaño inconsistente con microdato real de encuesta nacional. Confirmado empíricamente: los archivos `csv`/`dta` de 2018 son **byte-idénticos** (mismo sha256) a los de 2015 — el registro los rechazó por deduplicación de contenido. La canasta no ofrece microdato real de ENAPROCE, solo una base de ejemplo/plantilla reutilizada entre olas. No hay URL `/doc/` para este programa en la canasta — no hay universo declarado que citar.
- **enestyc** (15 URLs, 1992/1995/1999/2001/2005): mismo patrón — todos los nombres llevan `ejemplobd_` (ejemplo de base de datos), tamaños de 4–63 KB. No hay URL `/doc/` para este programa en la canasta.
- **enif** (16 URLs, 2012/2015/2018/2021/2024): 2012 y 2015 completos y nuevos; 2018/2021/2024 mezcla de registros previos + nuevos (modelos entidad-relación, bases CSV/DBF nuevas). Universo declarado, literal del descriptor 2012: "Esta base de datos contiene 203 viviendas en las que no tienen personas en el tramo de edad de interés de la encuesta, esto es, entre 18 y 70 años" — población objetivo 18-70 años. 2015 no declara universo en las primeras filas de su hoja índice (mismo patrón editorial que 2012, que sí lo declara en su hoja de notas aclaratorias, no en el índice).

**Registro en manifiesto**: 55/60 archivos nuevos se registraron con éxito vía `tests/manifiesto.py --registra` (un id por payload, `nota` con estructura+universo, `usado_para: sin uso asignado` — NO apendizado). 5 fueron rechazados por deduplicación de sha256 contra contenido YA registrado:

| archivo nuevo (rechazado) | id existente con el mismo sha256 |
|---|---|
| `eder2025/889463930242.pdf` | `eder2025_descripcion_bd_pdf` (mismo PDF, dos nombres/URLs) |
| `enaproce2018/ejem_base_micro_ciega_csv.zip` | `enaproce_2015_ejem_base_micro_ciega_csv` |
| `enaproce2018/ejem_base_micro_ciega_dta.zip` | `enaproce_2015_ejem_base_micro_ciega_dta` |
| `enaproce2018/ejem_base_pyme_ciega_csv.zip` | `enaproce_2015_ejem_base_pyme_ciega_csv` |
| `enaproce2018/ejem_base_pyme_ciega_dta.zip` | `enaproce_2015_ejem_base_pyme_ciega_dta` |

No se crea una segunda entrada para el mismo contenido (diseño intencional de `--registra`, ver su `--help`); la trazabilidad de la URL 2018 hacia el id 2015 queda aquí, en esta nota. Total TRAMO A: 72/72 archivos en disco, 72/72 con procedencia trazable en `manifiesto.yaml` (12 previos + 55 nuevos + 5 duplicados documentados).

## PASO 3/4 — descarga y revisión estructural, TRAMO B

Cruce contra el corpus antes de bajar: 20/214 ya presentes, 194 faltantes. Primer intento de descarga secuencial (`subprocess` un archivo a la vez, dentro de una invocación con `run_in_background` + `timeout` corto) murió sin completar y sin dejar log — diagnóstico: el `timeout` de la invocación mata el proceso de fondo aunque `run_in_background` esté activo; con archivos de hasta ~60 MB y descarga secuencial, 194 archivos no caben en esa ventana. Se relanzó como descarga **paralela** (`xargs -P 8`) con log incremental por archivo (append inmediato, no solo al final) para que un corte a medio camino no pierda el progreso. Completado: 214/214 en disco, 0 fallas de código HTTP.

Revisión estructural (mismo método que TRAMO A — sha256, sniff de tipo, `zipfile.namelist()`, encabezado crudo de CSV, sin abrir filas):

- **envipe** (52 URLs, 2011-2025, quince olas): universo declarado, literal del descriptor de la ola 2025 (no releído ola por ola — cita representativa): "la base de datos de la Envipe tiene como objetivo dar respuesta a los requerimientos de aquellos usuarios especializados... la percepción de la seguridad pública, el desempeño institucional, la victimización en el hogar y la victimización personal." Unidad de análisis: población de 18 años y más.
- **mociba** (48 URLs, 2015-2025): el descriptor de la ola más reciente (xlsx) no trae párrafo de universo/objetivo, solo diccionario de variables — pero declara explícitamente que parte de sus variables "corresponden al módulo de usuarios de ENDUTIH": MOCIBA es un módulo adosado al levantamiento de ENDUTIH, no una encuesta con marco muestral propio. Se reporta, no se adjudica si eso basta o no para R10.1/R10.3.
- **encig** (28 URLs, 2011-2025): universo declarado, literal del descriptor 2025: "obtener información que permita generar estimaciones con representatividad a nivel nacional y estatal sobre las experiencias, percepciones y evaluación de la población de 18 años y más en ciudades de 100 mil habitantes o más..." — incluye estimaciones de prevalencia de víctimas de actos de corrupción.
- **endireh** (40 URLs, 2003-2021): universo declarado, literal del descriptor 2021: "la base de datos de la ENDIREH tiene como objetivo dar respuesta a los requerimientos de los usuarios especializados... indagar la frecuencia, características y magnitud de la violencia ejercida por las distintas personas agresoras contra las mujeres."
- **engasto** (46 URLs, 2012-2013): universo declarado, literal del único descriptor en la canasta (2012): "dar respuesta a los requerimientos de aquellos usuarios especializados... análisis más detallado del monto, la estructura y el destino de los gastos del hogar."

### Hallazgo fuerte: ENGASTO 2013 reusa 18 de sus 21 archivos de microdatos, byte a byte, de ENGASTO 2012

Confirmado por deduplicación de `--registra` (no es una sospecha, es un rechazo real del script por sha256 idéntico): las tablas `gasto`, `gasto_de_consumo_ajustado[_constante]`, `gasto_mujeres`, `hogar` y `persona` de la carpeta `/engasto/2013/` son **exactamente el mismo archivo** (mismo sha256) que su contraparte en `/engasto/2012/`, en las tres variantes de formato (dbf/dta/sav) cada una — 18 de 21 archivos. La excepción es la tabla de vivienda: 2012 la publica como `vivienda_*.zip` (singular) y 2013 como `viviendas_*.zip` (plural, contenido distinto, registrado sin conflicto). 2013 tampoco trae su propio descriptor (`_fd.pdf`) — usa el de 2012. Lectura literal: la canasta no ofrece una segunda ola independiente de gasto/hogar/persona para ENGASTO; solo la tabla de vivienda cambió entre 2012 y 2013. No se adjudica si esto es un error de publicación de INEGI o una reedición intencional (p.ej. actualización solo del módulo de vivienda) — se reporta el hecho, verificable por cualquiera con `sha256sum` sobre los dos archivos.

**Registro en manifiesto**: 176/194 archivos nuevos registrados con éxito. 18 rechazados por deduplicación exacta de sha256 (los 18 de ENGASTO 2013 arriba descritos) — trazabilidad de la URL 2013 hacia el id 2012 queda documentada aquí, no se crea una segunda entrada para el mismo contenido. Total TRAMO B: 214/214 archivos en disco, 214/214 con procedencia trazable en `manifiesto.yaml` (20 previos + 176 nuevos + 18 duplicados documentados).

## Numerador — payloads con dato propio para las 14 reglas abiertas

Mapeo programa→regla es el que trae el encargo (derivado por mesa); este acto no lo re-deriva ni lo adjudica, solo reporta si el programa asociado ya tiene payload en disco tras este acto:

| regla | programa(s) asociado(s) | ¿con payload tras este acto? |
|---|---|---|
| R1.4 | engasto | SÍ (TRAMO B) |
| R2.1 | elcos, enaproce, enestyc | SÍ — con reserva: enaproce/enestyc son bases "ejemplo"/"ciega", ver hallazgo arriba |
| R2.2 | elcos, enaproce, enestyc | SÍ — misma reserva |
| R3.4 | enif, endutih | SÍ (TRAMO A) |
| R7.1 | encuci | SÍ (TRAMO A) |
| R7.3 | encuci (mcs queda en TRAMO C, no tocado) | SÍ, vía encuci |
| R7.4 | encuci, envipe | SÍ |
| R7.5 | envipe | SÍ (TRAMO B) |
| R8.1 | encuci | SÍ |
| R8.2 | enif | SÍ |
| R8.3 | encuci | SÍ |
| R10.1 | mociba | SÍ (TRAMO B) |
| R10.2 | elcos, enaproce, enestyc, endireh | SÍ — misma reserva sobre enaproce/enestyc |
| R10.3 | envipe, mociba, endireh | SÍ |

**14/14 reglas pasaron de sin-payload a con-payload en disco.** Con dos reservas explícitas, no resueltas por este acto: (1) R2.1/R2.2/R10.2 dependen parcialmente de enaproce/enestyc, cuyos archivos de microdatos son bases de ejemplo, no datos reales de encuesta — si se descarta esa fuente, esas tres reglas quedan sostenidas solo por elcos (R2.1/R2.2/R10.2) y endireh (R10.2); (2) "con payload" no es "resuelto" — ningún archivo se abrió más allá de su estructura (ADR-46), y si el payload realmente permite evaluar cada regla es una adjudicación que este acto tiene prohibido hacer.

## Recetas manuales (todas juntas)

- **CPV 2020, Cuestionario Ampliado**: la canasta de 7,930 URLs solo trae las 576 URLs del Cuestionario Básico de CCPV 2020 (confirmado: el archivo `DescargaMasivaOD_382026_131650.xml` ya presente en el corpus, aunque de otra generación, es exactamente esa selección). La muestra del Cuestionario Ampliado no está en ninguna canasta de este tipo — hay que generarla aparte desde el portal del programa (`inegi.org.mx/programas/ccpv/2020/#Microdatos`), seleccionando específicamente "Cuestionario Ampliado".
- **Cinco canastas pendientes de generar** (Tabulados 15,318 · Indicadores 392 · DENUE 486 · Sala de prensa 71 · INV 3): no están en el corpus ni en Descargas MX/Downloads (se buscó por nombre de canasta y por patrón `DescargaMasiva*`; todo lo encontrado son regeneraciones del mismo Microdatos nacional o la canasta vieja de CCPV). Receta de un clic: entrar a `inegi.org.mx/app/biblioteca/` o al selector de descarga masiva de INEGI, cambiar el filtro de "Microdatos" al apartado correspondiente (Tabulados / Indicadores / DENUE / Sala de prensa / INV), pulsar "Generar canasta" y descargar el `.zip` resultante a `Descargas MX` o `Downloads` — mismo mecanismo que ya usa este entorno para Microdatos.

## Suite `--baseline` — bloqueada, causa fuera de perímetro

```
$ python3 tests/check.py --baseline
[ ok ]  T01 fuente única de verdad
Traceback (most recent call last):
  ...
  File "tests/check.py", line 108, in t02_duplicates
    by_hash[hashlib.md5(io.open(p, "rb").read()).hexdigest()].append(rel(p))
IsADirectoryError: [Errno 21] Is a directory: 'data/raw/R7.3_PUB_Bienestar'
```

`T02` usa `glob.glob(ROOT, "**", "*.*")` para listar candidatos y luego los abre con `io.open(p, "rb")` sin comprobar `os.path.isfile` primero — cualquier **directorio** cuyo nombre contenga un punto literal revienta el script, porque el patrón `*.*` no distingue archivo de carpeta. En el corpus compartido (`mm-corpus/raw`, escrito por múltiples worktrees en paralelo esta sesión) hay al menos cuatro carpetas así: `R7.3_PUB_Bienestar`, `R2.1_ECCO`, `R7.4_R7.5_ACLED_HDX`, `R8.1_contraloria_social` — ninguna creada por este acto (nombres y contenido no relacionados con TRAMO A/B; timestamps de hoy, consistentes con trabajo concurrente de otros actos/worktrees sobre el mismo corpus compartido). Confirmado no transitorio: reintentado una segunda vez, mismo resultado.

Este defecto vive en `tests/check.py`, fuera del perímetro declarado de este acto (`data/manifiesto.yaml · corpus data/raw · data/indice-descarga-masiva-*.tsv · forense/notas/... · forense/hallazgos.md`), y las carpetas que lo disparan pertenecen a trabajo en curso de otros actos, no a este — no se tocan ni se borran. Se reporta como bloqueador, no se resuelve aquí. No se pudo confirmar `VERDE` antes de abrir PR; se abre de todas formas, con este hallazgo declarado explícitamente, para que mesa decida si merece un acto de reparación de `tests/check.py` o si las carpetas deben normalizarse.
