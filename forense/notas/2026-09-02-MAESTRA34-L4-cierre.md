# `ACTO MAESTRA34-L4 · CIVICA-Y-CORPUS` — cierre

2/sep/2026 · entorno **UBUNTU** · `ADR-283` · `COMPUERTA: ninguna`
Encargo: `forense/encargos/2026-09-01-MAESTRA34-L4-CIVICA-Y-CORPUS.md`
(dirección/Fable, `SHA de redacción a39073d`, archivado verbatim por A.3 en el
primer commit del acto). Ejecutado con `/acto` (`ADR-237`).
La medición vive aparte, en `forense/notas/2026-09-02-MAESTRA34-L4-P3-spec.md`
(spec congelada + resultados, dos commits).

---

## 0 · Lo que este acto encontró que no esperaba encontrar

**Dos actos consecutivos habían dado por inexistente una fuente que estaba en
enlaces planos del portal de su propio organismo electoral.** `MAESTRA34-A1`
(`ADR-278`) y `MAESTRA34-L3` (`ADR-280`) concluyeron que faltaban enteras la
elección local 2023 y la mitad local de 2024 de Coahuila y del Estado de México;
`MAESTRA34-L3` **no redactó su sucesor** por eso, y este acto sólo existe porque
dirección lo redactó de todos modos con las firmas dentro.

Las sondas anteriores no se equivocaron en lo que midieron: probaron
agregadores **nacionales** —`ine.mx/voto-y-elecciones/resultados-electorales/`
(sólo cómputos federales), `computos2024.ine.mx` (403 de Cloudflare), SICEE
(Tableau), `datos.gob.mx` (sin API viva)— y la fila 65 de la cola dejó escrito
con precisión por qué se cerraba: «existe por estado, universo de 32 portales
fuera del alcance de un intento por fila». Era la conclusión correcta **para una
caminata de cola nacional**.

Lo que faltaba no era red: era una **firma**. En cuanto `F232-b` priorizó dos
entidades, la ruta (i) del propio protocolo —el portal del organismo que
organiza esa elección— entregó las dos mitades completas, sin muro de
credencial. La lección, que va a `hallazgos.md`: un `NO-ENCONTRADO` de una
caminata nacional **no** es un `NO-ENCONTRADO` de la fuente, y una fila de cola
cuyo bloqueo declarado es «hay que elegir el estado» se desbloquea con una firma,
no con más peticiones.

---

## 1 · `P1` — las dos mitades, adquiridas y registradas

**A.8 antes de la primera petición de red:** 0 aciertos de host `iec.org.mx`, 0
de `ieem.org.mx`, 0 de `legislacion.edomex.gob.mx` en `data/manifiesto.yaml`.
Control positivo (A.13): **1 184** aciertos de `url_origen` en el mismo archivo
— el `grep` sí lo examinó.

**16 payloads `OBTENIDO`**, todos con A.7 (doble descarga, `sha256` idéntico en
las dos) y estructura de contenedor verificada (`zipfile.testzip()=None` en los
13 XLSX/ZIP, `%%EOF` en los 2 PDF, cabecera y conteo de filas en el CSV):

| origen | año | qué |
|---|---|---|
| IEC Coahuila | 2023 | gubernatura por municipio y por casilla; diputaciones por distrito y por casilla |
| IEC Coahuila | 2024 | ayuntamientos por municipio y por casilla |
| IEEM Edomex | 2023 | gubernatura por municipio, por casilla, y el paquete CSV |
| IEEM Edomex | 2024 | ayuntamientos por municipio, sección y casilla, y el paquete CSV |
| INE/DEOE (ruta iv) | 2024 | catálogo nacional de ubicación de casillas, 170 180 casillas con `Listado Nominal`, 32 entidades |
| calendario | — | acuerdo `IEC/CG/206/2023` y Gaceta del Edomex del 28/dic/2023 (Decreto 229) |

El catálogo del INE **no** está en el listado estático del portal de datos
abiertos —ninguno de sus 101 enlaces lo nombra—: se localizó por su API JSON
propia, `ine.mx/wp-json/datos-abiertos/v1/`. Es la ruta (ii) aplicada al objeto
de la ruta (iv).

**Cobertura contada por este acto, no heredada de la sonda** (A.13, abriendo cada
XLSX con `openpyxl`): Coahuila 2023 → 42 filas con municipio no vacío = 38
municipios + 1 agregada `VMRE_VA_VPPP` + 3 de nota al pie; Coahuila 2024 → 38;
Edomex 2023 → 128 = 125 + 3 que no son municipios; Edomex 2024 → 125.

**Tres trampas medidas antes de medir nada**, y las tres habrían producido un
defecto silencioso:

1. la cabecera del Edomex **no** está en la misma fila en los dos años — 6 en
   2023, **8** en 2024;
2. en 2024 hay nombres de municipio con sufijo numérico (`LUVIANOS 18`), así que
   cruzar por nombre entre años es inseguro: se cruza por `ID_MUNICIPIO`;
3. las filas no municipales hay que excluirlas explícitamente, y la exclusión
   **se comprueba**: los 38 municipios de Coahuila 2023 suman 1 343 764/2 355 025
   y, con la fila `VMRE_VA_VPPP` que se excluyó, reproducen exactamente el total
   que publica el IEC (1 344 882/2 377 964).

**Del lado del host, declarado:** `iec.org.mx` aplica un WAF `openresty`
**intermitente** sobre `/v1/index.php/*` — 403 de 150 B en 3 de 4 intentos, 200
de 77 152 B en el cuarto tras espera — y devuelve 403 en `robots.txt` y
`sitemap.xml`. Los ficheros bajo `/v1/images/` y `/v1/archivos/` no lo sufren.
Un solo 403 sobre ese portal no cierra nada. Las URLs de 2024 llevan acento y
espacios en la ruta (`C%C3%B3mputos2024`, `AYUNTAMIENTOS2024%20X%20CASILLA.xlsx`)
y exigen *percent-encoding* o `curl` las rechaza.

### 1.1 · `F232-a`, contestada con fuente primaria

**¿Hubo en 2024 municipios de Coahuila o del Edomex sin comicio local el 2 de
junio? No se encontró ninguno**, por tres vías independientes:

- **Edomex**, Decreto 229 (Gaceta del 28/dic/2023, 96 págs., 322 165 caracteres
  extraídos y contados): convoca a «integrantes de Ayuntamientos de los **125
  Municipios del Estado**» (5 aciertos) y «las elecciones a que se convoca se
  realizarán el **domingo 2 de junio del año 2024**» (2 aciertos). **0** aciertos
  de «excepción», **0** de «usos y costumbres|sistemas normativos».
- **Coahuila**, acuerdo `IEC/CG/206/2023` (25 págs., 53 576 caracteres): «los
  **treinta y ocho** comités electorales», 11 aciertos de `02/06/2024`; el único
  «extraordinaria» del documento es un tipo de casilla, no una elección.
- **Y la decisiva, que es de resultado y no de calendario:** los dos OPLE
  publican resultado municipal para los 38 y para los 125.

Luego la robustez (a) queda **`NO-APLICA`** y no se compró nada más para ella,
como el encargo manda.

### 1.2 · Registro por las tres capas

1. **Manifiesto** `937 → 953` (+16, una invocación de `--registra` por id, A.1).
2. **Cola del registro:** la fila 65 `EXT_OF_03_PARTICIPACION_LOCAL_2024` pasa a
   `OBTENIDO` —con la acotación escrita de que **no** cubre las otras 30
   entidades—, más 3 filas nuevas (`IEC_COAHUILA`, `IEEM_EDOMEX`,
   `GACETA_GOBIERNO_EDOMEX`). `OBTENIDO` **54 → 58**. Vista regenerada con
   `tools/vista_cola_adquisicion.py` (T26).
3. **Relación con la necesidad cívica y `R7.1`:** no hubo que crear ninguna
   necesidad, porque **`N25` ES `R7.1`** (`necesidad-objeto-modelo.tsv` l. 29) —
   y crear necesidades es perímetro de `MAESTRA34-N6`, no de este acto. +2
   relaciones `CONFIRMADA` contra `N25`, +2 procedencias, +2 filas de utilidad,
   **en una sola operación**, por la vía de `GUIA-CURADOR-REGISTRO §alta`
   (`ADR-279`), con `relacion_id` **importado** de `baseline.py` y no
   reimplementado. +3 familias de alias con la decisión de **no fusión** escrita:
   el IEC no es el INE, el IEEM no es el IEC, la Gaceta no es el IEEM.
   Validador **VERDE** (`ok=true`, `errores=[]`): relaciones 205→207, evidencias
   206→208, utilidad 205→207, confirmadas 3→5, familias de alias 5→8, candidatas
   147 sin cambio. `baseline.json` recifrado. `via_capa2.py --root .`: **0**
   diffs propuestos, `COINCIDE=54`, `NO_COINCIDE=0`.

**Anti-PR#77:** los 16 payloads viven en
`/home/pc0/mm-corpus/raw/electoral_local_2023_2024/`, con layout por organismo y
año (la lección de `MAESTRA34-L3`: un layout plano habría colisionado), y hay
**0** ficheros de datos fuera de `data/raw` dentro del worktree.

### 1.3 · Defecto propio, atrapado y revertido

La primera escritura de las tres tablas del curador usó `csv.writer`, que
**re-citó una fila ajena** de `evidencias.tsv` (`PROV-2fcf25ae…`, que guarda
comillas sin escapar). Se vio en `git diff --numstat` —1 línea borrada donde
debía haber 0—, se revirtió con `git checkout` y se reescribieron **por línea**.
Diff final: 2 añadidas / 0 borradas en cada una de las tres. Es el reverso del
defecto ya conocido de que el módulo `csv` *despoja* comillas de filas ajenas:
también las **añade**.

---

## 2 · `P2` — `FP-231` cerrada, y la letra de su firma era imposible

Contado en `hallazgos.md` y en `ADR-283`; en resumen: `--registra` aborta por
dedup de contenido, la re-derivación que `F231-a` ordena **ya existía desde el
2026-08-06** (`ENCARGO REPAIR-1`), y lo único pendiente era retirar la entrada
vieja. Hecho sin borrarla —la firma pide «se retira **con nota**»—, quitándole
los tres campos que afirman un payload, que es la vía que el propio
`cmd_verifica` reconoce.

`--verifica` sobre el corpus: **`coincide=826 · no_coincide=0 · ausente=0`**,
exit 0. Era `no_coincide=1`.

A.13 sobre el payload, para que la adjudicación quede medida y no supuesta: 24
tablas `.dbf` + 1 PDF, **111 256 filas cada tabla** (2 670 144 en total),
comprobado por dos caminos independientes (cabecera DBF vs
`(tamaño − cabecera)/long_registro`, coincidencia exacta en las 24); campos por
tabla de 25 a 221.

**El remedio (c) que la ficha ofrecía —instrumentar `--verifica` en la suite para
que un `no_coincide` sea `FAIL`— NO se ejecuta**: el encargo lo puso fuera de
perímetro explícitamente. Queda para `MAESTRA34-E1`/mesa, con el corolario ya
escrito en `hallazgos.md`: *`--verifica` no está en la suite; un `no_coincide`
sólo se ve si alguien lo corre*.

---

## 3 · `P3` — la medición

Detalle completo en `forense/notas/2026-09-02-MAESTRA34-L4-P3-spec.md`. Aquí,
sólo el resultado y su reserva:

| | |
|---|---|
| **Δ participación municipal 2024 − 2023** | **+10.4790 pp** |
| **IC95** (bootstrap sobre municipios, B=10 000, seed 42) | **[+9.6890, +11.2652]** |
| n | **163 de 163** municipios (38 Coahuila + 125 Edomex) |
| ¿cruza cero? | **NO** |
| Coahuila / Edomex | +10.1289 [+8.5478, +11.8838] / +10.5855 [+9.6889, +11.4965] |
| Edomex − Coahuila | +0.4565 [−1.4331, +2.2600] — **cruza cero** |

Controles, todos exactos: reagregar acta por acta reproduce la tabla por
municipio con `|Δvotos| = 0` y `|Δlista nominal| = 0` en los dos años de
Coahuila; `% PART` publicada vs recalculada, diferencia máxima **0.000000 pp**;
0 municipios fuera de `(0,100]`.

**La reserva es de identificación, no de precisión, y estaba escrita antes de
medir** (`§0.4` del commit de spec): el cargo no es el mismo en los dos años
—gubernatura en 2023, ayuntamiento en 2024— y hay una elección presidencial de
por medio. Este diseño **no separa** concurrencia de jerarquía del cargo ni de
calendario. Las dos lecturas secundarias acotan sin resolver: contra las
diputaciones locales de 2023 el Δ de Coahuila es prácticamente el mismo
(+10.1023), y contra la boleta federal de 2024 el salto respecto de 2023 sigue
ahí (+7.66 y +9.26 pp).

---

## 4 · Contador

| | antes | después |
|---|---|---|
| payloads en `data/manifiesto.yaml` | 937 | **953** (+16) |
| `OBTENIDO` en la cola | 54 | **58** |
| relaciones del curador | 205 | **207** |
| fichas corregidas | — | **+1** (`FP-231`) |
| reglas con Δ `MEDIDO` en el acumulador | 10 | **11** |
| cargas al motor | 0 | **0** |
| corridas de Hito D | — | **0** |

Hito D **sin movimiento**: esto no es una corrida de falsador. Es una instancia
compatible con `R7.1`, cuyo veredicto `A` ya está archivado por `ADR-145`, y no
lo toca.

---

## 5 · Sello para mesa — REDACTADO, NO LANZADO (formato RH)

El encargo pide redactarlo sin lanzarlo. Va aquí para que mesa lo firme o lo
rechace; **este acto no lo ejerce**.

> ### Qué dice el número
>
> En Coahuila y el Estado de México, la participación municipal fue **10.5 puntos
> porcentuales mayor** cuando la elección local se celebró el mismo día que la
> federal que cuando se celebró sola, con un intervalo de confianza del 95 % de
> **[+9.7, +11.3]** que no se acerca a cero. Ocurre en **160 de 163 municipios**,
> con la misma magnitud en los dos estados (la diferencia entre ellos cruza
> cero), y sobrevive a cambiar cuál elección de 2023 se toma como base y a
> medirlo contra la boleta federal en vez de la local.
>
> Lo que **no** dice: por qué. El cargo en disputa cambia entre los dos años
> (gubernatura → ayuntamiento) y hay una presidencial de por medio, así que el
> número mezcla concurrencia, jerarquía del cargo y calendario. Es una reserva
> de identificación declarada antes de medir, no una excusa posterior.
>
> ### Qué opción firmaría
>
> Tres opciones, y la recomendación es la **(b)**:
>
> **(a)** Sellar `civico.participacion.contingente` al motor tal cual. **No se
> recomienda, y de hecho no es posible sin transformarla**: la cifra es un Δ en
> puntos porcentuales y el motor consume probabilidades. Habría que decidir
> contra qué línea base se convierte, y eso es una decisión de modelo que este
> acto no tiene mandato para tomar.
>
> **(b) Aceptar la cifra como MEDIDA y dejarla en el acumulador con `tier`
> asignado, sin cargarla**, y abrir un acto sucesor que busque la variación de
> concurrencia **dentro** del mismo año y cargo —la que `F232-a` fue a buscar y
> no existe en estas dos entidades— en los estados cuyo calendario local sí se
> desfasa del federal, o en elecciones extraordinarias. Es lo que convierte una
> correlación grande y limpia en una identificación.
>
> **(c)** Ampliar primero la base a más entidades con el mismo diseño entre años.
> Barato (los 32 OPLE publican como estos dos y la ruta ya está probada) pero
> **no resuelve el confundidor**: más estados con el mismo diseño dan más
> precisión sobre el mismo número mezclado.
>
> ### Qué cambia en el motor
>
> Hoy, **nada**: `milpa/tramite.yaml` queda intocado y el congelamiento del motor
> (`ADR-68(a)`) sigue vigente. Si mesa firmara la (b), lo que cambia es el
> **estatus de `R7.1`**: pasa de tener un veredicto `A` archivado sobre un
> falsador de encuesta a tener, además, una instancia de comportamiento agregado
> real, con `n = 163` y control aritmético exacto, en la dirección que la regla
> predice. Eso no reabre el veredicto —no es una corrida de Hito D— pero sí es la
> primera vez que esta regla toca dato electoral y no declarativo.

---

## 6 · Lo que este acto NO hizo

No carga nada al motor (`milpa/tramite.yaml` intocado; el sello es de mesa) · no
re-descarga ENDIREH · no instrumenta `--verifica` en la suite (fuera de
perímetro) · no baja SICEE (es de mesa) · no toca corridas ni el marco · **CIEGO
a corridas-M/L** (`prereg-duelo-v2`, `scoreboard`, `agregado`: no se abrió
ninguna) · no abre Ola 6 · no toca `milpa/tramite.yaml` ni `prereg-duelo-v2`,
que son perímetro de `MAESTRA34-N4`.

**Concurrencia observada:** `origin/main` se movió de `a39073d` a `df26d3a`
mientras este acto corría — `MAESTRA34-N7` (`PR #460`, `ADR-281`) y
`MAESTRA34-N4` (`PR #459`, `ADR-282`), más `PR #461`. `git merge origin/main` no
produjo conflicto; verificado a mano tras el *sync*, como manda la regla de la
casa: **0 `ADR` duplicados**, 283 entradas contiguas de 1 a 283. El candidato de
este acto se re-derivó **después** de fusionar: `281` → `282` → **`283`**, regla
de la casa aplicada dos veces seguidas. En `hallazgos.md` el merge automático
dejó las dos líneas de este acto **antes** de las cuatro de `origin/main`; no se
reordenaron, porque la convención de orden de la casa gobierna la resolución de
un **conflicto** y aquí no lo hubo — se declara para que nadie lo lea como
descuido.

**Sucesores:** el sello de la regla cívica, que dirección redacta con firma de
mesa (borrador en `§5`) · `MAESTRA34-N5` hereda CNGMD y la cívica para Ola 6 ·
la variación intra-año de concurrencia, que es lo único que separaría los tres
efectos, queda **nombrada y no rodeada**.
