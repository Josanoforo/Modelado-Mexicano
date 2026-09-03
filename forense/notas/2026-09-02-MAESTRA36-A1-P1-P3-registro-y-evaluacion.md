# MAESTRA36-A1 · P1, P2 y P3 · escáner recursivo, registro y evaluación A.4

**Acto:** MAESTRA36-A1 · ESCANEA-RECURSIVO-Y-REGISTRA-DESCARGAS · **ADR-310**
**Encargo:** `forense/encargos/2026-09-02-MAESTRA36-A1-ESCANEA-RECURSIVO-Y-REGISTRA-DESCARGAS.md`
(SHA de redacción 9af8407, + enmienda de dirección a mitad de acto, archivada con él)
**Fecha:** 2026-09-02 · **Caja:** Ubuntu (WSL2), `/home/pc0/mm-maestra36-a1`
**Antecede:** `forense/notas/2026-09-02-MAESTRA36-A1-P0-barrido.md`

---

## P1 · `--escanea` recursivo

`tests/manifiesto.py` usaba `os.listdir` + `isfile`: veía el nivel superior de la raíz y
no entraba a ninguna subcarpeta. `tests/corpus.py` usaba `os.walk` + `relpath`. Los dos
recorridos del proyecto no miraban el mismo árbol, y esa asimetría es la causa de que a
mesa se le volviera a pedir lo que ya había bajado.

El parche adopta la convención que ya era vigente de archivo: `archivo` = ruta relativa a
la raíz, con subcarpeta si la hay. Es la que tienen las 49 entradas `Descargas Manuales/…`
desde la corrección T2 del 18/ago/2026.

### Control de regresión, corrido ANTES de usar el parche

| | universo | staging |
|---|---:|---|
| **A** — sin parchar, raíz real | 148 archivos | 233 líneas |
| **B** — parchado, copia plana (`cp -p` del nivel superior, mtimes verificados idénticos) | 148 archivos | 233 líneas |

`diff A B` → **exit 0, byte-idénticos**. Re-verificado al final contra el código que
efectivamente se entrega (con los dos arreglos de abajo): sigue en exit 0.

**Control positivo del comparador** (A.13 / «todo negativo va con control positivo»):
alterando un solo `tamano_bytes` en B, `diff` devuelve 1. El «byte-idénticos» no viene de
un comparador que no sabe fallar.

Sobre la raíz **real** el parche pasa de ver 148 a ver 224 archivos, y su desglose coincide
exactamente con el del barrido independiente de P0: 183 registrados · 41 no · 0 conflictos.
Dos mecanismos distintos, la misma cifra.

`--grupo` pasa a aplicar `fnmatch` sobre la ruta relativa, no sobre el basename. Dicho en
la ayuda del flag y en el docstring de `--escanea`.

### Dos defectos que aparecieron al usar el parche — ninguno buscado

**(1) `_yaml_valor` partía los valores largos y corrompía el staging.** Preexistente, no
introducido aquí. Hacía `yaml.safe_dump` con el ancho por defecto (80): un escalar más
largo se parte en varias líneas con sangría de **dos** espacios, la misma que la clave que
sus siete llamadores escriben a mano en `data/manifiesto-staging.yaml`; la continuación se
lee entonces como una clave nueva sin `:`.

Reproducido **contra 9af8407 sin el parche** (importando el módulo tal como sale de
`git show`): un `--url` de 105 caracteres devuelve una cadena con `\n`. `--escanea`
escribía el staging roto **sin fallar**, y `--promueve` reventaba después con
`yaml.scanner.ScannerError`. Y no se cura solo: `--escanea` lee el staging previo para
preservar otras raíces, así que con el staging corrupto revienta también el único comando
que podría regenerarlo — hay que restaurarlo a mano. Lo pagué en vivo: una corrida de
regresión salió silenciosamente stale por esto.

El manifiesto real nunca estuvo expuesto: `escribir_manifiesto` usa `yaml.dump` sobre la
estructura entera, que sangra las continuaciones más que la clave. Arreglado con
`width=10**9`; controles a 105 y 5 000 caracteres, y cadena corta intacta.

**(2) `_derivar_id` tomaba la ruta entera.** Consecuencia directa del parche recursivo:
con `archivo` ya como ruta, el slug daba `descargas_manuales_ingresostributarios`. Las 49
entradas que ya tienen prefijo derivan **todas** su id del basename
(`mex_2010_iepep_v01_m_v01_a_puf`, `ages_125_alumnos_10`); ninguna lleva el nombre de la
carpeta. Tomar la ruta habría abierto dos convenciones de id en la misma raíz. Corregido a
basename; la colisión entre basenames iguales en carpetas distintas la resuelve el sufijo
numérico que la función ya tenía (`export_crudo` / `export_crudo_2`, control corrido).

### Criterio de aceptación de P1

`tests/corpus.py` sobre la raíz real: **C1 187 → 155**, baja de **exactamente 32**, que es
el número que P2 registró. **C3 = 0, no sube.** C2 = 0.

## P2 · registro por la vía de las 106 entradas existentes

`--registra` no era la vía: es solo para `data/raw/` y no acepta raíz (0 líneas de `--raiz`
en el script, verificado). Se usó `--escanea`/`--promueve`, siete pases, uno por grupo,
cada uno con su `--grupo` sobre la ruta relativa. Nada se tecleó: sha256, tamaño y
`fecha_descarga` los deriva el script del archivo real.

| pase | patrón | objetos | clase |
|---|---|---:|---|
| 1 | `descargas manuales/*[!)].xls` | 9 | (a) SAT |
| 2 | `icpsr35024*[!)].csv` | 2 | (a) ICPSR |
| 3 | `export_crudo.txt` | 1 | (a) ICPSR |
| 4 | `leeme*.txt` | 2 | (a) ICPSR |
| 5 | `*oecd*.docx` | 1 | (a) OECD |
| 6 | `descargas manuales/itin*.pdf` | 11 | (b) SHCP |
| 7 | `descargamasiva*.zip` | 6 | (b) INEGI |

**Manifiesto 1 070 → 1 102 (N = 32).** Las 8 rutas duplicadas las absorbió el dedup por
sha256 — `--promueve` las reportó como «ya registrado … no se duplica» y no se tocó ni una
copia en disco. `descargas.php` no se promueve por diseño (es página, no dato) y es el
único archivo del árbol que queda fuera del manifiesto: 223 de 224.

**`--verifica`: 32 invocaciones, una por `--id` (A.1).** 32 COINCIDE. Las tres respuestas
sin colapsar: `no_coincide=0 · ausente=0 · sin_configurar=0`, exit 0 en las 32.

**Anti-PR#77.** La raíz es absoluta y externa a todo clon (`/mnt/c/Users/PC0/Descargas MX`);
los `raices.local.yaml` del clon principal y de esta caja son idénticos (`diff` exit 0); y
re-hasheando los 32 payloads **resolviendo la raíz por el `raices.local.yaml` del clon
principal**: 32 COINCIDE, 0 ausentes, 0 discordantes, 32 archivos abiertos.

**Cola.** Editada línea por línea. Antes de tocarla se corrió el control que exige la
casa: reserializar el archivo entero con el módulo `csv` **cambiaría 3 filas ajenas**
(29 `CNGMD`, 47 `INE`, 94 `IEECH_CHIHUAHUA`), así que se dejan intactas byte a byte. Las 3
filas objetivo sí reserializan idénticas. `git numstat`: 5 inserciones, 3 bajas — las 3
editadas más las 2 nuevas, nada más.

**Tres tablas del curador: cero altas, y es el resultado de aplicar la regla, no un
faltante.** La enmienda ordena alta «solo para clase (a) con necesidad identificable», y
«fuente sin N → no se inventa». Medido: `SAT_MEXICO` tiene **0 filas** en `relaciones.tsv`
y ninguna `N` que la nombre → no es alta, se declara. `MEXICO_PANEL_STUDY_2012` (N26, N27)
y `OECD` (N30) **ya tienen relación**, así que no son fuente nueva; y sus relaciones
apuntan a otro objeto de evidencia (el codebook, y `NO_DETERMINADO`), que no es lo que este
acto registró. Adjudicar los crosstabs como evidencia es del sucesor L12, no de aquí.

`via_capa2.py --root .` → **0 diffs propuestos**; con `--escribe`, `relaciones.tsv` no
cambió (`git diff` vacío). Validador del curador: `"ok": true`, `"errores": []`.
`baseline.json` **no necesita recifrado**: cubre 7 tablas del curador y ninguna se escribió;
la cola de adquisición no está entre ellas. **FP-246 sigue vigente y no se fuerza:** 6 filas
llevan lista `;` en `id_manifiesto` y `via_capa2.py` ni las promueve ni las contradice.
No se parcheó `via_capa2.py` — fuera de perímetro.

T26: vista regenerada, 111 filas.

## P3 · evaluación A.4

Vocabulario A.4, separado a propósito del vocabulario del registro (OBTENIDO / PENDIENTE /
NO-ACCESIBLE), que no se traduce. **Universo examinado en todos los negativos de abajo:
los 224 archivos del árbol de `descargas_mx`.** Nada se buscó en red.

### Filas que P2 movió

| fila | veredicto A.4 |
|---|---|
| `NUEVA-L6` **SAT_MEXICO** | **EXISTE-SATISFACE.** Los 9 `.xls` son el objeto de la fila: estadística tributaria del SAT, identidad verificada abriendo las hojas (Recaudación/Ingresos tributarios · Padrón/Por entidad federativa · Factura y e.firma/Certificados emitidos), no por el nombre. La fila estaba `NO-ACCESIBLE-DESDE-LA-CAJA` y mesa hizo exactamente lo que pedía. Reserva declarada: `url_origen` queda a nivel de portal, marcada no confirmada — el `.xls` concreto no tiene URL conocida. |
| `:19` **MEXICO_PANEL_STUDY_2012** | **EXISTE-NO-SATISFACE.** Lo que falta es el microdato: `35024-0001-Data.dta` (1 555 × 374) exige membresía institucional. Lo registrado son tabulaciones de segunda mano, **conteos sin ponderar** (el tablero de ICPSR no aplica los pesos del estudio), sin estrato ni UPM. Satisfacen documentación y celdas, no la fuente. |
| `:37` **OECD** | **EXISTE-NO-SATISFACE** para el microdato, y **NO-ACCESIBLE** el microdato mismo. Lo hallado es el formulario *Terms of Use* del Trust Survey PUMF, cuyo propio texto exige firmarlo y enviarlo a `govtrustinfo@oecd.org`. Por eso la fila queda `NO-ACCESIBLE` y no `OBTENIDO`: desviación deliberada del defecto de la enmienda, declarada aquí y en la nota de la fila. |
| **SHCP** (nueva) | **EXISTE-SATISFACE** como activo de inventario; **sin necesidad asignada**. No hay fila previa ni `N`, y no se inventa. Los 11 PDF son los Informes Trimestrales 2026 T1–T2, identificados por texto extraído. |
| **INEGI_DESCARGA_MASIVA_CARRITOS** (nueva) | **EXISTE-SATISFACE** como mecanismo, **NO** como microdato — precedente de las 7 entradas ya registradas de la familia. Su valor es el inventario: 25 213 URLs de descarga directa en los seis XML. |

### Objetos que dirección esperaba encontrar

**Crosstabs del Mexico Panel Study (→ habilita `MAESTRA36-L12`).**
`academico/icpsr35024/crosstabs/` **no existe**: el árbol entero de la raíz son dos
directorios, la raíz y `Descargas Manuales/`. Los crosstabs están en el nivel superior,
sueltos. Pero el contenido **sí está, y es más de lo que el encargo suponía**:

| tabla | dónde | celdas |
|---|---|---:|
| T1 · T2 · T3 · T4 | `icpsr35024_DS1_W2_crosstabs_derivado_v0.csv` | 16 · 32 · 32 · 32 |
| T5 (frecuencias P35A/P35B, experimento de lista) | `icpsr35024-ds1-w2-crosstabs-derivadas.csv` | 22 |
| T6 (P8 × W2_P8 \| W2_P41) | idem | 257 |
| T7a · T7b (W2_P41 × W2_P7 / W2_P8 \| W2_PX8) | idem | 12 · 58 |
| T8 (W2_P53 × W2_P7) | idem | 12 |
| T9a (W2_P36D × W2_P41) | idem | 10 |

Respuesta directa a la pregunta del encargo: **sí, T6–T9 ya están** (T9a; **T9b no
aparece**). Y T5 también, pese a que `LEEME-procedencia.txt` lo declara «pendiente de mesa».

**Dos discordancias de procedencia, medidas, que L12 tiene que resolver antes de usar estas
cifras:**

1. `LEEME 2-procedencia.txt` declara que `icpsr35024-ds1-w2-crosstabs-derivadas.csv` es
   «Tabla T6 … 257 celdas». El archivo trae **T5, T6, T7a, T7b, T8 y T9a — 371 celdas**.
   La procedencia describe una sexta parte de su propio archivo.
2. `LEEME-procedencia.txt` nombra `export_crudo_mesa_2026-09-02.txt` y da por pendiente T5.
   En disco el crudo se llama `export_crudo.txt` (791 líneas, 4 cruces × control W2_P36C,
   `Data source: https://doi.org/10.3886/ICPSR35024.v1`) y T5 ya está derivado.

`export_crudo_mesa_2026-09-02.txt` → **NO-ENCONTRADO-EN-DISCO** (0 coincidencias en 224
archivos). `T5_lista_W2.txt` → **NO-ENCONTRADO-EN-DISCO** (0 coincidencias). El contenido
de T5 sí está, en otro archivo. La serie de ronda 1 (P40×P7, P40×P8, P38B×P8|P36C, P39×P8)
sigue **sin derivar**: ninguna tabla del disco usa P40, P39 ni P38B como variable.

**OECD Trust (B4).** Ver arriba: `EXISTE-NO-SATISFACE` para microdato, `NO-ACCESIBLE` el
microdato. No hay Stat.Links ni xlsx de reporte en la raíz; lo que hay es el formulario.

**Bauchet 2014 (B5).** **NO-ENCONTRADO-EN-DISCO.** Búsqueda de `*2474620*` sobre los 224
archivos: **0 coincidencias**. En disco solo están `ssrn-2589578.pdf` y `ssrn-2689238.pdf`,
ya registrados, que A1-3 (1/sep) ya había reportado como distintos del pedido. La fila `:39`
queda como estaba: este acto no la mueve. Control positivo de la búsqueda: el mismo `find`
con `*icpsr*` devuelve 5 archivos, así que el 0 no es de un comando vacío.

**CompraNet / ComprasMX (EXT_OF_07, fila `:63`).** **NO-ENCONTRADO-EN-DISCO.** Búsqueda de
`*compranet*`, `*comprasmx*`, `*cnetassets*`, `DD_PIC*`, `DD_RUPC*`, `*rupc*` sobre los 224
archivos: **0 coincidencias**. Mesa no bajó nada de `datos_abiertos_contratos_expedientes/`.
La fila `:63` se deja intacta. Queda anotado en `hallazgos.md` que su etiqueta dice
`EXT_OF_07` pero su contenido es `EXT-OF-05` del mapa.

## Lo que este acto NO hizo

- No descargó nada de red.
- No reescribió ninguna de las 106 entradas `descargas_mx` existentes, ni las 49 con
  prefijo ni las 57 sin él.
- No borró ninguna de las 8 copias duplicadas del disco de mesa.
- No dio de alta ninguna `N` ni ninguna relación.
- No lanzó L12 ni el censo CompraNet: los habilita.
- No tocó `downloads`, `milpa/**`, `forense/prereg-duelo-v2/**` ni `via_capa2.py`.
