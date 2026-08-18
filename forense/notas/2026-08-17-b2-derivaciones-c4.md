# Nota · BARRIDO-2 C4 — derivaciones previas a la curaduría

**Fecha:** 2026-08-17 · **Rama:** `codex/barrido-2` · **PR:** #244 (borrador)
Complementa `forense/notas/2026-08-17-b2-relevo.md`. Se escribe **antes** de la fase de
curaduría, no después: todo lo que sigue es insumo derivado que la curaduría consume,
y dejarlo solo en la sesión repetiría el corte que este mismo acto vino a reparar.

Las cuatro derivaciones corrieron en agentes independientes de solo lectura, en
paralelo. Cada cifra que este documento sostiene fue **re-verificada por comando por
el ejecutor** antes de escribirse; donde no lo fue, se dice.

---

## 1 · Cobertura de fuentes — el denominador real es 150, no 110

El barrido léxico resolvió 21 de 77 fuentes canónicas (110 relaciones). Una auditoría
dirigida sobre las 56 restantes encontró **23 falsos negativos**, que aportan 40
relaciones más.

| | antes | después |
|---|---:|---:|
| fuentes con material | 21 / 77 | **44 / 77** |
| relaciones con material | 110 / 199 | **150 / 199** (75.4 %) |
| fuentes reales sin material, con frontera declarada | — | 25 |
| entradas que no son fuentes | — | 8 |

**Por qué falló el barrido léxico, y no es mala suerte.** El manifiesto **no tiene campo
`fuente`**. Sus campos son `archivo, descargado_por, entorno_descarga, fecha,
fecha_descarga, formato, hecho, id, licencia, nota, raiz, sha256, tamano_bytes,
url_origen, url_origen_procedencia, usado_para, verificacion_tamano`. La procedencia
vive en `url_origen` (dominio o catálogo) y en `usado_para`, que muchas veces trae el
nombre canónico literal. GDELT se resuelve por `url_origen: http://data.gdeltproject.org/gdeltv2/`,
no por su nombre: sus payloads se llaman `20260813130000_export_csv`. Son **13**, no 14
— el propio `usado_para` dice «muestra de 13 archivos export de 15min», y la entrada
número 14 que aparece buscando `export` es `642348348mexico_2004_export_version`, que
es LAPOP.

**Las ocho que no son fuentes** y no deben contarse como hueco de cobertura: `01-` y
`02-` (prefijos truncados de dos nombres de PDF, sin archivo ni URL en ninguna parte),
`FABLE` (es un modelo revisor, no un dato), `RELLABORALESPRUEBA` (slug de prueba del
portal INEGI: sus URLs contienen literalmente `prueba.pdf`, `pruebaPre`),
`SIN_CANDIDATO_IDENTIFICADO` (centinela de hueco, declarado como tal en su propia nota),
`REPOSITORIOS_UNAM_COLMEX_ITAM_DATAVERSE_ICPSR` (registro consolidado de búsqueda
negativa), `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH` y
`DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` (los dos, registros negativos del mapa
oficial). Descontadas, la cobertura ajustada es **44 de 69 fuentes reales**.

**Reglas deterministas que engancharían 21 de las 23** sin adivinar, todas sobre datos
duros del manifiesto: sha256 → `id_manifiesto` (prerrequisito, recupera 49 ids);
host de `url_origen` → fuente; path de catálogo del Banco Mundial → fuente; slug
`inegi.org.mx/programas/<slug>` → fuente; prefijo de carpeta en `archivo` → fuente;
cadena canónica literal en `usado_para`. **Dos casos solo por decisión curatorial**, y
hay que decirlo: `GLOBAL_PREFERENCES_SURVEY ≡ GPS` (el propio registro ya lo declara
«declarada y no resuelta») y las dos formas del instrumento Banxico de competencias
financieras. Ninguna regla puede derivar que dos nombres canónicos distintos son el
mismo instrumento; eso es un acto de alias.

**Reserva declarada:** `CNGMD` y las entradas `descargamasiva_*` son material
instrumental —el propio `usado_para` avisa «NO es el payload»— y contarlas como
cobertura sin esa reserva sobreestimaría la apertura.

---

## 2 · FP-24 — la cifra defendible hoy es 0, y el «4» es un candidato, no un veredicto

Esta sección se escribió primero afirmando **«4 dependen, 195 no»**, derivado de forma
independiente y reproducible. Una verificación adversarial encargada a propósito —cuyo
trabajo era refutarla, no reproducirla— la devolvió como **NO DEMOSTRADA**, y tenía
razón en tres puntos que el ejecutor volvió a comprobar por comando antes de aceptar la
corrección. Se deja el rastro completo porque el «4» sigue siendo útil, pero no como
cifra sellada.

**Lo que la refutación derribó, verificado de nuevo:**

1. **La premisa central era falsa.** El criterio descansaba en que ENSAFI, ENFIH y
   ENBIARE tienen *una sola entrada de manifiesto cada una*. Medido sobre
   `data/manifiesto.yaml` y confirmado en el ledger: **ENSAFI 1, ENFIH 2, ENBIARE 2**
   (`enfih2019_bd_csv_zip` además de `enfih2019_fd_xlsx`; `enbiare2021_bd_csv_zip`
   además de `enbiare2021_fd_pdf`). El texto propuesto de la política condiciona el
   enlace a que el objeto sea *«evidenciable con una entrada distinta del manifiesto»*,
   con lo cual la segunda entrada es precisamente la escapatoria que disolvería el
   conflicto. La premisa se puede reparar —«una sola entrada **abierta**», porque ambas
   segundas entradas declaran «No se abrio ni extrajo»— pero tal como estaba escrita,
   no se sostiene.
2. **La unidad estaba mal.** `ADR-92(c)` y el §17 del encargo miden la dependencia
   **por propuesta**, no por relación, y prohíben expresamente derivarla de necesidad
   compartida, de fuente común o del rótulo «gemela» — que son las tres piezas con las
   que se construyó el conjunto de partida. Y **no existe ninguna propuesta**:
   `integracion-barrido/propuestas-recibidas.tsv` e `integracion-propuestas.tsv` tienen
   una línea cada uno, la cabecera. La población que la regla gobierna todavía no nació.
3. **Hay un contraejemplo vivo entre las 195.** `REL-45672e7d7c5ac7c69edaede4` (N6/ENFIH)
   y `REL-cf53a5e4bf5bf666390fa543` (N6/ENSAFI) están fuera del conjunto de 20, su
   necesidad no está entre las seis, y ambas tienen `BUSQUEDA_DIRIGIDA` activa en
   `trabajo-semantico.tsv` — confirmado por comando. Si esa búsqueda tiene éxito,
   aceptarla obliga a decidir cuál de las dos filas se queda con la única entrada
   abierta que su hermano `SI` ya ocupa. Declararlas «no dependen» es falso para ellas.

**La cifra que este acto sostiene:**

| lectura | cifra |
|---|---|
| Regla vigente (`ADR-92(c)`, unidad = propuesta), hoy | **0** — no hay propuestas que medir |
| Población estructuralmente expuesta, a vigilar cuando existan | **22 relaciones en 7 necesidades** (N3, N4, N6, N10, N12, N13, N14) |
| Gemelas cuyo objeto resuelve a la entrada del gemelo, aplicando el criterio a la evidencia citada y no a la celda del registro | 5 |
| De esas 5, vivas y no cerradas como `TERMINAL_LEGACY_PRESERVADO` | 3 |

El encargo lo dice sin ambigüedad: *«El número final puede ser 0, menor que 20, 20 o
mayor que 20. Lo produce BARRIDO-2. No se preescribe.»* Sellar «4» hoy sería
preescribirlo. La cifra formal se emite contra las propuestas cuando existan, y las 22
expuestas son la lista de vigilancia del supervisor.

**Lo que sí queda sellado, porque sobrevivió a los seis ataques:**
la resolución de las cuatro variables contra el archivo de variables cuadra línea por
línea, con el gemelo `SI` citando la misma línea y distinto objeto canónico en los
cuatro casos; y la derivación **no está contaminada** por la lista histórica — los
cuatro IDs se obtienen con un filtro sobre tablas sin abrir la nota que ya los proponía,
y la tabla de evidencias no ha cambiado desde el baseline semántico original. El «4» es
un candidato pre-derivado, mecánicamente reproducible y limpio de circularidad. No es
un veredicto.

**Defecto lateral, encontrado de paso y confirmado:** el bootstrap de este mismo acto
(`93160c3`) añadió dos filas cuya `fuente_canonica_normalizada` es `01-` y `02-` — el
prefijo numérico del nombre de un PDF tomado como fuente canónica. Cualquier agrupación
por fuente sobre `relaciones.tsv` produce dos grupos espurios de tamaño 1 mientras no se
corrija, y ya afectó al conteo de este apartado (`SI_O_REFERENCIADO` es 22, no 20).

### Derivación original, conservada como rastro



El encargo prohíbe heredar la cifra: *«El número final puede ser 0, menor que 20, 20 o
mayor que 20. Lo produce BARRIDO-2. No se preescribe.»* Derivado desde el registro:

- **Conjunto de partida: 20 gemelas** — mismo `necesidad_id` y misma
  `fuente_canonica_normalizada`, con `capa2_manifiesto = SI_O_REFERENCIADO` y al menos
  una fila `SI` de distinto `objeto_evidencia_id_canonico` en el grupo.
  Reparto **ENSAFI 9 · ENFIH 8 · ENBIARE 3**, necesidades N3, N4, N10, N12, N13, N14.
- **`dependencia_fp24 = SI`: 4.** **`NO`: 16.** Sobre las 199: 4 dependen, 195 no.

La derivación llegó al reparto 9/8/3 y a los cuatro IDs **sin usarlos como insumo**, y
coincide con lo que la nota histórica ya proponía. Verificado además que **ningún
script, prueba ni schema cablea los 20 IDs** — la prohibición del encargo se cumple hoy.

**El criterio, y por qué es material y no de lista.** Las tres fuentes implicadas tienen
**una sola entrada de manifiesto cada una**. Si el objeto propio de la gemela resuelve a
una variable nombrada que vive en esa única entrada, escribir su veredicto es enlazarla
a la MISMA entrada que su gemelo `SI` ya ocupa, y eso obliga a decidir cuál de las dos
se queda con la variable: **depende**. Si su objeto no nombra variable alguna, cierra en
`NO_REFERENCIADO` por política ya firmada, no enlaza nada y el gemelo no se toca: **no
depende**. Las cuatro dependientes comparten con su gemelo no solo el payload sino **la
misma línea del mismo archivo de variables**.

**Contradicción que hay que declarar, no resolver aquí.** La fila `FP-24` del tablero
define el par sin exigir misma fuente; su nota primaria lo exige explícitamente y
descarta la lectura contraria con un argumento propio: *«dos fuentes distintas no son un
par, son dos fuentes»*. La diferencia no es cosmética: **20 filas con una lectura, 155
con la otra**. Se aplicó la de la nota, porque la propia fila la cita como su `dónde`.
Mesa debe ratificar cuál rige.

**Lo que la derivación no puede cerrar.** El texto de la regla pendiente **vive fuera del
repo**: los dos documentos que lo contienen no existen en el árbol, y la única lectura
disponible es una cita de segunda mano. Si el original difiere de esa cita, la
clasificación de las cuatro puede moverse.

**Co-implicación.** Los cuatro gemelos `SI` de las cuatro dependientes están escritos y
hoy no requieren decisión, pero cualquier propuesta de `CAMBIO` o `TERMINAL` sobre ellos
también sería FP-24-dependiente, porque su contenido es la variable en disputa. Cota
superior por co-implicación: **8 filas**.

---

## 3 · M-APERTURA — las 17, y por qué el número a corregir es 17 y no 9

Las 17 se derivan de `data/lista-apertura-enlace2-2026-08-14.tsv` por
`destino = APERTURA-PENDIENTE` (las otras 2 de las 19 son `PROPUESTA-A-COLA`). El join
contra `relaciones.tsv` es **por identidad de cadena completa**, no por subcadena, y se
corroboró de cuatro maneras: unicidad de clave, ausencia en `fusiones-relaciones.tsv`,
terna canónica `(necesidad, fuente, objeto)` con 199 valores distintos en 199 filas, y
—decisivo— que **5 de las 17 tienen el par `(necesidad, fuente)` ambiguo** y que cuatro
nombres de fuente están truncados a 64 caracteres, de modo que cualquier join por nombre
es estructuralmente inseguro en esta tabla.

**Las 17 conservan hoy `capa4 = INDEXADO-NO-DESCARGADO`.** El §18.8 prohíbe que cierren
así si el payload fue observado. Bajo el enlace `payload_id` tal como estaba el ledger,
violaban 9. Bajo identidad de contenido —la prueba material correcta— violan **17**: los
23 payloads que las 17 invocan están los 23 en disco, íntegros y caracterizados en E2.
Ésa fue la punta del hilo que llevó al defecto del §4 de esta nota.

**Ocho grupos de payload cubren las 17**: CSES ×4 relaciones, ZA5900 ×2, ZA6980 ×2,
Mass Mobilization ×4, openICPSR-116334 ×2, WB-2661 ×1, IEPEP ×1, LFEPIE ×1. El trabajo
de apertura es de 8 unidades, no de 17.

**Estado de la evidencia previa, medido:** `variable_reactivo_tabla = NO_DETERMINADO` en
17/17 — nadie ha llegado al nivel de reactivo. `utilidad-modelo.reserva` es la plantilla
vacía `"Escala/diseño/universo:"` en las 17, y en 99 de las 199 filas de esa tabla: el
curador no hereda ninguna reserva redactada. `requiere_decision = NO` en 17/17.

**Tres cosas que la curaduría debe resolver y que no son suyas de nacimiento:**
una relación declara `periodo 2017` pero está enlazada al módulo ISSP **2012**; una toca
`G1.radio_confianza`, que es uno de los dos coeficientes con deriva de
`requiere_decision` declarada y no corregida; y una excepción material real,
`za5900_cdb`, cuyo codebook falló con `PermissionError` y es la única representación del
subconjunto con `objetos_e2 = 0`.

**Vínculo histórico (§18.10), verificado:**
`forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo.md`, §6 en la
línea 151, marca `SUPERADO POR BARRIDO-2` en la 153, y —esto es lo que importa— el
vínculo con las 17 **no vive en el §6 sino en su ADENDA-1, línea 199**, que ya el
14/ago llamaba al rótulo *«factualmente falso»*. BARRIDO-2 lo confirma con evidencia
material: no era un juicio, era una medición pendiente. Queda pendiente propagar la
marca al gemelo archivado `…-completo-p-lote1.md`, cuyo §6 (línea 149) no la lleva.

---

## 4 · T23 · T-CABLEADO — especificación previa a su implementación

**El número es T23**, derivado y no heredado: `^def t\d+` en `tests/check.py` da 1..22
con T19 presente como `t19a`/`t19b`/`t19c`. El aparente hueco no existe. Trampa
declarada: greppear la lista literal de `main()` omite T16, que se registra aparte y
condicionado.

**El schema congelado y el §21 coinciden exacto** en las 26 columnas, su orden y los dos
enums. No hay contrato que arbitrar. Las divergencias son de **reglas** que un schema
per-fila no puede expresar, y todas se comprobaron ejecutando el validador: `fecha=""`
pasa; el límite de 160 solo cubre 5 de 26 columnas; `sha256_12` incorrecto pasa; una
`REL-` inventada bajo `INTEGRADA` pasa; y la conversa del bicondicional de FP-24
(`requiere=SI` con `dependencia=NO`) pasa. T23 cierra esas cinco brechas.

**Lo que hoy ya fallaría:** la condición de las aperturas absorbidas. Es la única de las
19 que se evalúa sin que el cableado exista.

**La dependencia dura, y es una decisión de este acto:** tres de los productos que T23
debe cruzar —`propuestas-barrido2.tsv`, la tabla de tareas semánticas y
`decisiones-integracion-barrido2.tsv`— **no tienen ruta fijada en ningún sitio**. El
integrador declara `--output-dir` obligatorio y sin valor por defecto, y el derivador de
tareas escribe bajo `.barrido2/private/`, que está gitignorado. Si la tabla de tareas
acaba ahí, T23 es inverificable en un clon limpio y en CI. **Se fijan las tres bajo
`data/curacion-registro/ejecucion-semantica/barrido2/` y se suman a la lista
«Versionable» del §24.** Es la decisión que desbloquea dos de las 19 condiciones.

**Dos límites que se declaran en vez de disimularse:** el campo `evidencia` cita un
registro del índice E2 privado, que no existe en un clon limpio, así que su
dereferencia solo será determinista si el ensamblador lo hace citar el registro durable;
y `SIN-DEMANDA-CONFIRMADO` **no tiene columna propia** en las 26 —no está en ninguno de
los dos enums—, de modo que su verificación es hoy una búsqueda de token en la fila.

**Nota de ingeniería que se adopta:** `tests/check.py` hoy no importa `jsonschema` y no
va a empezar. Sus cinco enums y tres patrones se comprueban a mano; la validación por
schema se queda en `tools/curador_registro/tests/`, donde la dependencia ya existe.

---

## 5 · Lo que estas derivaciones cambian en el plan de C4

La curaduría no arranca sobre 110 relaciones sino sobre **150**, repartidas en un número
de grupos de payload mucho menor que el de relaciones —las 17 de M-APERTURA, por
ejemplo, son 8 aperturas—. La cifra de `dependencia_fp24` que las propuestas deben
declarar está derivada y es **4**, con la reserva de que debe re-emitirse contra las
propuestas cuando existan, porque el flujo del §17 exige que salga de ahí y no del
registro. Y el cableado de C6 ya tiene su prueba especificada, con dos condiciones
bloqueadas hasta que este acto fije tres rutas.
