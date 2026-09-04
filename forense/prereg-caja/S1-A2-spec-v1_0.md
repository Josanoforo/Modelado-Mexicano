# S1 · Pre-registro de `MAESTRA38-A2 · RECENSO` — congelado antes de que caja corra

### `prereg-caja-S1-A2` · **v1.0** · 4 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S1-A2-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S1-A2`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La spec congelada del futuro `ACTO MAESTRA38-A2 · RECENSO`: universo, comandos en orden, regla de exclusión de copias/auxiliares, umbral de tolerancia, y la tabla nominal de lo que se espera encontrar depositado en `descargas_mx/`. |
> | **QUÉ NO ES** | No es un censo — no corre ningún comando de los de abajo. No abre ningún byte de microdato. No promueve nada al manifiesto. No es caja: este acto corre en **NUBE**, sin corpus montado (`ls data/raw/` vacío, confirmado al arrancar). |
> | **VERIFICAS ASÍ** | El primer censo real que corra `MAESTRA38-A2` compara su salida contra §2 (comandos), §5 (tabla nominal) y §6 (árbol de categorías); toda desviación se declara, no se silencia. |

**Acto:** `ACTO MAESTRA38-N3 · PRE-REGISTRO-DE-CAJA`, 4/sep/2026, entorno **NUBE**, sobre `origin/main = 0ff3d7106793e7352df92bd658e3e25293a025db`.

---

## 0 · Lo que este pre-registro encontró al verificar el encargo — declarado antes de fijar nada

El encargo (`forense/encargos/2026-09-04-MAESTRA38-N3-PRE-REGISTRO-DE-CAJA.md:7`) pide fijar cuatro piezas — universo de "dos raíces, downloads excluida", comandos, "patrones B (auxiliar/copia)" y "umbral C ≤ 10" — como si ya tuvieran regla escrita en el repo. Verificado por búsqueda exhaustiva (`grep -rniE` sobre `forense/ canon/ tools/ data/`): **ninguna de las cuatro tiene precedente nombrado así en ningún otro archivo.** Lo que sí existe, y que este documento adopta como base:

- **Raíces**: `tests/manifiesto.py:62-67` corrige un diseño anterior — *"RAÍCES (30/jul, corrección de diseño): hay tres, nunca dos. `data_raw` ... `descargas_mx` ... `downloads` ... NO es una carpeta de datos: tiene archivos ajenos al proyecto."* Las "dos raíces, downloads excluida" del encargo son exactamente el subconjunto de datos de esas tres: `{data_raw, descargas_mx}`, con `downloads` excluida porque el propio código ya la marca como no-dato (`RAICES_QUE_EXIGEN_GRUPO = {"downloads"}`, `tests/manifiesto.py:772`).
- **Patrones B / umbral C**: sin regla escrita en ningún tool ni documento. §3 y §4 fijan una regla nueva, declarada como nueva, con la base analógica más cercana que el repo trae.

Este pre-registro **no hereda de prosa** (D-13): fija la regla desde cero, con la razón escrita, tal como exige el propio bloque D-13 para todo lo que el árbol no ya tenía.

---

## 1 · Universo

**Raíces en alcance: `data_raw` y `descargas_mx`.** `downloads` queda excluida del universo del recenso — no es raíz del programa (`tests/manifiesto.py:66-67`; confirmado también en `forense/notas/2026-08-06-map1b-censo-raices.md:267-269`: *"Solo `data_raw` y `descargas_mx` — `downloads` no es raíz del programa, sus candidatos van aparte en (E)"*).

Rutas reales: no versionadas, viven en `data/raices.local.yaml` (gitignorado, resuelto por `manifiesto.resolver_raiz()`), distintas por máquina. `data/raw` es además la "raíz integrada" (`.claude/commands/acto.md:40-41`): AUSENTE no es PARO, se resuelve por código.

**Fuera de alcance, declarado, no descubierto:** `downloads` (raíz completa — sus hallazgos van a categoría E, §6, sólo si aparecen candidatos a payload ahí, nunca como universo del recenso).

---

## 2 · Comandos exactos, en orden

El único censo automatizado que existe hoy (`ACTO MAESTRA37-N6`, `tools/adquiere_cron.sh` paso `2.5`) cubre **solo `descargas_mx`** — no `data_raw`. El recenso de `A2` extiende el mismo mecanismo a las dos raíces del universo (§1), en este orden:

1. **Resolver cada raíz en esta máquina**, antes de censar nada:
   ```
   python3 -c "import sys; sys.path.insert(0,'tests'); import manifiesto; print(manifiesto.resolver_raiz('data_raw', '.', 'data/raw') or '')"
   python3 -c "import sys; sys.path.insert(0,'tests'); import manifiesto; print(manifiesto.resolver_raiz('descargas_mx', '.', 'data/raw') or '')"
   ```
   Si una raíz no resuelve: `PARO-RAIZ: <raíz> no resuelve en esta máquina (data/raices.local.yaml)` — mismo texto que `tools/adquiere_cron.sh:93` ya usa para `descargas_mx`; el recenso sigue con la raíz que sí resolvió, declarado.

2. **Censar `descargas_mx`** (comando ya en producción, sin cambio):
   ```
   python3 tests/manifiesto.py --escanea descargas_mx
   ```

3. **Censar `data_raw`** (extensión nueva de este acto — `RAICES_QUE_EXIGEN_GRUPO` sólo exige `--grupo` para `downloads`, `data_raw` no está en ese conjunto, así que el mismo modo directo aplica):
   ```
   python3 tests/manifiesto.py --escanea data_raw
   ```

4. **Escribir el censo del día**, mismo contrato que `forense/censo-raiz/AAAA-MM-DD.txt` (`data/INFRAESTRUCTURA-v1_0.md:580`): resumen (`Total en disco · nuevos · ya registrados · conflicto`) como primera línea, salida cruda de las dos corridas debajo, un archivo por raíz o uno combinado con sección por raíz — **A2 decide y lo declara en el propio archivo**, esta spec no lo prescribe porque el censo hoy sólo conoce una raíz.

5. **Clasificar cada archivo nuevo** contra el árbol de categorías de §6 (A–E), aplicando la regla de exclusión de §3 y el umbral de §4.

6. **Cruzar contra la tabla nominal de §5** — todo lo que §5 espera y el censo no encuentra se reporta `AUSENTE-EN-RAIZ` citando este censo (A.8); todo lo que el censo encuentra y §5 no anticipaba se reporta como hallazgo nuevo, no se descarta.

7. **Commit `[CENSO] AAAA-MM-DD`**, separado del resto del acto, empujado según el mismo patrón que `tools/adquiere_cron.sh:79-88` ya usa.

**Comando que NO corre en este acto:** ningún `--registra`/`--promueve` — el recenso censa, no adquiere ni promueve al manifiesto (eso es un acto `A` posterior, per `data/INFRAESTRUCTURA-v1_0.md:576-587`).

---

## 3 · Patrones B (auxiliar/copia) — regla de exclusión, fijada aquí por primera vez

**No hay regla previa con este nombre.** El precedente reutilizable es la copia de navegador con sufijo numérico, documentada dos veces de forma independiente:

- `forense/firmas-pendientes.tsv:251` (FP-259): *"Los otros 9 son las 8 rutas que son copia byte-identica de otra ruta del mismo arbol (patron (1)/(2)/(3) del navegador, registradas una sola vez por dedup de sha256) mas descargas.php..."*
- `forense/notas/2026-08-06-map1b-censo-raices.md:456-464`: *"copias repetidas del mismo archivo bajado dos o más veces por el navegador (sufijo "(1)", "(2)"…)"*
- `forense/encargos/2026-09-03-MAESTRA37-N6-CENSO-DIARIO-DE-RAIZ.md:6`: *"9 objetos con 21 copias de navegador (1)…(4)"*

En los tres casos, el mecanismo real que colapsó la copia **nunca fue un regex de nombre por sí solo** — fue dedup por `sha256`. Este pre-registro fija la regla en ese mismo orden, para no introducir un falso positivo (dos archivos genuinamente distintos que comparten sufijo "(1)" por coincidencia, no por ser la misma descarga):

**Regla de exclusión B, fijada:**

Un archivo del censo se clasifica **patrón B (auxiliar/copia)** si y sólo si, **en este orden**:

1. Su `sha256` coincide con el de otro archivo ya indexado en la misma raíz (dedup por contenido — condición necesaria, nunca por nombre solo), **Y**
2. Su nombre matchea el patrón de copia de navegador — sufijo ` (N)` (espacio, paréntesis, uno o más dígitos, paréntesis) inmediatamente antes de la extensión, p. ej. `archivo (1).pdf`, `archivo (2).zip` — **O** es `descargas.php`/cualquier página guardada bajo `EXTENSIONES_PAGINA` (`.php`/`.html`/`.htm`, `map1b:278-279`) que no se promueve por diseño.

Un archivo que cumple (2) pero **no** (1) — mismo sufijo de nombre, `sha256` distinto — **no** es patrón B: es un archivo genuinamente distinto que sólo comparte convención de nombrado, y se censa como candidato normal. Un archivo que cumple (1) pero no (2) (mismo contenido, nombre sin sufijo de copia) sigue siendo dedup por `sha256` — pertenece a la categoría D (§6), no a B; B es específicamente la subclase de D cuyo nombre delata su origen (copia de navegador).

**Consecuencia declarada:** ningún archivo se excluye del censo por coincidencia de nombre sola. `capa2_manifiesto`/`capa3_disco_real` sólo se afirman `SI` sobre lo que el censo realmente examinó (A.13).

---

## 4 · Umbral C ≤ 10 — fijado aquí por primera vez

**No hay precedente nombrado.** El candidato analógico más cercano en el repo es la categoría **C · "raíz declarada no coincide con dónde vive el archivo"** del único censo de tres raíces que corrió (`forense/notas/2026-08-06-map1b-censo-raices.md:425-433,504`), que dio **0** la única vez que se midió.

**Regla fijada:** categoría **C** = archivos cuya raíz declarada en `data/manifiesto.yaml` (campo `raiz` o inferencia por vecindad de registro) **no coincide** con la raíz donde el recenso los encontró físicamente. **Umbral ≤ 10**: si `|C| ≤ 10`, el recenso lo reporta y **no** dispara PARO — sigue el acto, categoría anotada. Si `|C| > 10`, **PARO**: el recenso se detiene y reporta a mesa antes de clasificar el resto, porque un volumen de más de 10 discrepancias raíz-declarada-vs-real es indicio de un problema estructural (raíz mal configurada, `data/raices.local.yaml` apuntando al lugar equivocado), no de casos aislados.

**Por qué 10 y no otro número, declarado antes de correr (A.4):** es un margen conservador de una orden de magnitud sobre el único precedente medido (0). No hay base para un número más preciso sin haber corrido el recenso de dos raíces al menos una vez — este pre-registro fija el corte con el margen que menos castiga un primer resultado limpio y más protege contra un problema sistémico, siguiendo el mismo criterio que `hitoD-R7_3-especificacion-v1_0.md §5.1` usa para elegir el borde de un rango ("la dirección honesta cuando la ficha da un rango y no un número" es la que le pone la prueba más difícil al falsador, no a la regla) — aquí, la lectura más conservadora de "esto sigue siendo ruido, no sistema roto".

---

## 5 · Tabla nominal de depósitos de mesa — nombres esperados

**Estado verificado al sellar esta spec: ningún depósito ha ocurrido todavía.** `descargas_mx/` no existe en el filesystem de esta sesión (NUBE); `forense/censo-raiz/` está vacío salvo `.gitkeep`; el encargo `MAESTRA38-A1` (línea 17) prometió "una línea aquí con los nombres" y ninguna de sus dos enmiendas posteriores (sonda lateral 3/sep, restauración FP-291/FP-292 4/sep) la trae. Esta tabla fija los nombres **esperados**, para que el primer recenso real los busque por nombre, no a ciegas.

| pieza | estado en manifiesto/cola al sellar | nombre/ruta esperada bajo `descargas_mx/` |
|---|---|---|
| **ICPSR .dta** (microdato `35024-0001-Data.dta`) | Sin entrada en `data/manifiesto.yaml` (sólo documentación: codebook, cuestionario, DATS). Cola: `MEXICO_PANEL_STUDY_2012` marcada `OBTENIDO`, pero ese estado cubre solo la documentación — el `.dta` sigue `EXIGE-CREDENCIAL`/`NO-ACCESIBLE` (A.4) | por analogía con las entradas ya registradas (`ICPSR_35024/35024-Questionnaire-spanish.pdf`, `35024-0001-Codebook-spanish.pdf.zip`): `descargas_mx/ICPSR_35024/35024-0001-Data.dta` |
| **WB 6667** (microdato de `IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016`) | `PENDIENTE-DE-MESA`, `EXIGE-CREDENCIAL` confirmado 2 veces (ADQ-15 18/ago, LOTE-UBUNTU-ADQ-1 19/ago). Sólo 24 payloads de documentación/DDI ya registrados, ninguno es microdato | por analogía con `ADQ15_WB6667_Tutores_Pedagogicos_Moviles_2016/*.pdf`: `descargas_mx/ADQ15_WB6667_Tutores_Pedagogicos_Moviles_2016/<microdato>.dta` — nombre exacto del archivo de microdato NO determinable hasta que mesa lo descargue; el recenso lo busca por carpeta, no por nombre exacto |
| **PDN S1** | Sin fila ni entrada de manifiesto propia — NO ENCONTRADO | por analogía con `PDN_S3v2.zip` (único payload real hoy, bajo la fila compuesta `PDN_SESNA_S1_S2_S3_S6`): `descargas_mx/PDN_S1v2.zip` |
| **PDN S2** | Sin fila ni entrada de manifiesto propia — NO ENCONTRADO | `descargas_mx/PDN_S2v2.zip` |
| **PDN S6** | Sin fila ni entrada de manifiesto propia — NO ENCONTRADO (S3 sí: `pdn_s3v2` / `PDN_S3v2.zip`, `OBTENIDO-PARCIAL`) | `descargas_mx/PDN_S6v2.zip` |
| **"11 recetas"** | **Discrepancia declarada, no reconciliada por invención.** Los cuatro archivos `forense/notas/*PAQUETE-RECETAS*.md` que existen en el repo traen 3 (`MAESTRA38-A1-PAQUETE-RECETAS-4`), 6 (`MAESTRA37-A2-PAQUETE-RECETAS-3`), 15 (`PAQUETE-RECETAS-2026-09-01`) y 1 (`PAQUETE-RECETAS-2026-09-02`) recetas respectivamente — ninguno suma 11, y el único de los cuatro ligado al acto `MAESTRA38-A1` (RECETAS-4) trata CSES/Reuters DNR/Pew, **no** ICPSR/WB/PDN | **NO se fija un nombre nominal de "11 recetas".** El recenso, si encuentra un `PAQUETE-RECETAS-*.md` nuevo bajo ese tema con exactamente 11 entradas, lo censa como hallazgo; si no, reporta la discrepancia contra este párrafo, no inventa el conteo |
| **`ENFIH-4`** (las 4 filas de `relaciones.tsv` — `N3`/`N10`/`N13`/`N14`, `FP-288` ABIERTA — que citan `enfih2019_bd_csv_zip` como payload de registro pendiente) | Payload YA en manifiesto (no es una descarga pendiente; lo pendiente es la resolución de `id_manifiesto` en las 4 filas, ajeno al recenso de raíz) | sha256 esperado, verificado contra `data/manifiesto.yaml:4115` (`id: enfih2019_bd_csv_zip`, `archivo: enfih2019/enfih_2019_base_de_datos_csv.zip`): <br>`be372533d5043920892142e8bf792b7293a5f20ab466a6441bc89925b42ef4d5` — el recenso, al pasar por `descargas_mx/enfih2019/enfih_2019_base_de_datos_csv.zip`, confirma que el archivo en disco produce este hash antes de que cualquier acto posterior lo cite como resuelto |

---

## 6 · Árbol de categorías del recenso (A–E, precedente de `map1b` reutilizado)

Mismo esquema que el único censo de tres raíces que corrió (`forense/notas/2026-08-06-map1b-censo-raices.md`), con B y C fijadas por primera vez en §3/§4:

| categoría | definición | umbral/acción |
|---|---|---|
| **A** | huérfanos — en disco, sin entrada de manifiesto | se reporta, candidato a alta futura |
| **B** | auxiliar/copia (§3) | se excluye del conteo de candidatas nuevas, se anota, nunca se borra |
| **C** | raíz declarada ≠ raíz real (§4) | `≤10` reporta y sigue; `>10` PARO |
| **D** | mismo `sha256` en dos rutas (no cubierto por B) | se reporta, dedup declarado, ninguna ruta se borra |
| **E** | candidatos a payload dentro de `downloads` (fuera de universo, §1) | se anota aparte, **no** entra al conteo del recenso — "es información distinta" (`map1b:269`) |

---

## 7 · Qué NO hace este acto

El recenso no abre ningún byte de contenido más allá de `sha256`/metadatos de archivo. No promueve nada a `data/manifiesto.yaml`. No corre `--registra` ni `--promueve`. No decide sobre `FP-288` (ENFIH) ni sobre las filas de la cola de adquisición — sólo confirma presencia/ausencia física contra la tabla nominal de §5. No toca `downloads` salvo para anotar categoría E. No es caja: corre en NUBE y no requiere corpus montado para sellarse — el primer censo real que **sí** requiere corpus es el que ejecuta este pre-registro, en caja.

---

**el primer resultado que produzca este procedimiento es el que se reporta.**
