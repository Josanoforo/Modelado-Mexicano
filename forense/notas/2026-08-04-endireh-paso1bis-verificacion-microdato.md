# ENDIREH paso 1-bis — verificación del microdato contra el archivo, no contra el descriptor

**Contadores movidos: 0.** Sin módulo de auditoría (v2.3). Este acto no mide, no adjudica CP-1 (agregado vs. desglose) y no decide si `exposicion_violencia` cambia de clase en la tabla de reparto.

Encargo F, mesa #18, emitido 4/ago/2026. Base declarada: main con PR #74 fusionado.

## 0 · Verificación del entorno y de la base

`HEAD` verificado **antes** de tocar nada: al abrir esta sesión, PR #74
("CAL-CONF Fase B, pos4 rehecho paso 1 (ENVIPE)") seguía **OPEN**
(`mergedAt: null`), no fusionado — la premisa de base del encargo **no se
sostenía todavía**. Mientras se verificaba esto, una sesión concurrente en
el mismo host resolvió un conflicto append-only pendiente en
`forense/hallazgos.md` (rama `sesion/cal-conf-faseb-pos4-envipe-paso1`,
mismo checkout compartido `/home/pc0/Modelado-Mexicano`) y fusionó PR #74
(`mergedAt: 2026-08-04T04:09:45Z`, merge commit `53bdd3a`). Se esperó a que
`origin/main` reflejara ese merge antes de derivar ninguna premisa — no se
adivinó el resultado ni se procedió sobre la rama sin fusionar.

Este acto corrió en un **worktree nuevo** (`git worktree add`, rama
`sesion/cal-conf-faseb-pos4-endireh-paso1bis`) apuntando a `origin/main`
en `53bdd3a`, no en el checkout compartido — el primer intento de crear
el worktree falló con `error: could not lock config file .git/config:
File exists` (escritura concurrente de otra sesión sobre el mismo
`.git/config`); reintentado, quedó creado. Esto reproduce exactamente
`I-01` de la cola de hallazgos congelados (`I-11`, "un checkout
compartido entre sesiones de escritura se bloquea sin que ninguna sesión
haga nada mal") — un tercer caso, no dos.

Verificación del entorno (protocolo §0), corrida en el worktree:

```
$ python3 tests/bitacora.py --abre
HEAD:         53bdd3a34dcec24ad4f396df88823a70945fba4e
origin/main:  53bdd3a34dcec24ad4f396df88823a70945fba4e
Divergencia:  ninguna — HEAD == origin/main
check.py --baseline:        exit=0 · LÍNEA BASE: VERDE
validador_registro_ids.py:  exit=0 · OK

$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable

$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200

$ ls data/raw | wc -l
(ausente al abrir; mkdir -p data/raw — no es PARO, es esperable de un worktree nuevo)
```

Firma del entorno: **buena** — `sin_variable`, sonda en `200`. Sonda
corrida sin `-I`. No se pegó la ruta real de `data/raw` en esta nota ni
se pegará en el PR.

## 1 · Premisas — re-verificadas contra `53bdd3a`, no heredadas

| # | Premisa | Verificación en `53bdd3a` |
|---|---|---|
| PF-1 | `endireh2021_bd_csv_zip`: URL, 78 902 567 bytes, sha256 `e4f1e7b1…037e` | **Sostiene.** `data/manifiesto.yaml:3232-3241`, grep directo |
| PF-2 | `endireh2021_fd_pdf`: URL bajo `/doc/`, 10 369 637 bytes, sha256 `5c30a3f7…d180` | **Sostiene.** `data/manifiesto.yaml:3216-3224` |
| PF-3 | Sesión que bajó el ZIP se declaró efímera, no abrió contenido | **Sostiene.** `forense/notas/2026-08-04-descargas-dirigidas-endireh-enoe-endutih.md:31` — cita textual: "estaba ausente al iniciar esta sesión… este clon es un `git clone` fresco… los bytes mismos se pierden con la sesión" |
| PF-4 | Paso 1: once candidatas en `TB_VD`, universo mujeres 15+, C3 pasa, C2 abierto | **Sostiene** como *descripción del acto*, con una corrección de detalle abajo (§2, hallazgo VFAM) — el archivo `forense/notas/2026-08-04-cal-conf-faseb-pos4-endireh-paso1.md` existe y `forense/hallazgos.md:77` describe exactamente eso |
| PF-5 | ENVIPE/`TPer_Vic1`: LA FUENTE NO TIENE EL DATO, ninguna candidata sirve | **Sostiene, y solo ahora es verificable contra `main`** — vivía únicamente en PR #74, sin fusionar al abrir esta sesión (ver §0). `forense/notas/2026-08-04-cal-conf-faseb-pos4-envipe-paso1.md:9-11,264`: "**LA FUENTE NO TIENE EL DATO**… ninguna candidata sirve" |
| PF-6 | `TMod_Vic`/`TPer_Vic2` no abiertas, fuente no agotada | **Sostiene.** Misma nota, líneas 221/296/312: "No se leyeron `TMod_Vic`, `TPer_Vic2` ni las Secciones VI/VII" |

Ninguna premisa (1) falló contra el `HEAD` real en el momento de actuar
— pero **PF-5/PF-6 no eran verificables hasta que PR #74 se fusionó**, y
eso ocurrió mientras esta sesión ya estaba en curso, no antes. Se declara
así en vez de silenciarlo.

## 2 · Acto A — verificación del payload

```
$ python3 tests/manifiesto.py --verifica --id endireh2021_bd_csv_zip
endireh2021_bd_csv_zip [data_raw]: AUSENTE — no está en la raíz 'data_raw'
$ python3 tests/manifiesto.py --verifica --id endireh2021_fd_pdf
endireh2021_fd_pdf [data_raw]: AUSENTE — no está en la raíz 'data_raw'
```

AUSENTE, esperable (worktree nuevo, PF-3 confirma que la raíz que los
bajó era efímera). Re-descarga por `url_origen` registrada, sin
reconstruir nombres:

```
$ curl -s -D - -o /dev/null -r 0-0 --max-time 20 \
  https://www.inegi.org.mx/contenidos/programas/endireh/2021/microdatos/bd_endireh_2021_csv.zip
HTTP/1.1 206 Partial Content
Content-Type: application/x-zip-compressed
Content-Range: bytes 0-0/78902567

$ curl -s -D - -o /dev/null -r 0-0 --max-time 20 \
  https://www.inegi.org.mx/contenidos/programas/endireh/2021/doc/endireh2021_fd.pdf
HTTP/1.1 206 Partial Content
Content-Type: application/pdf
Content-Range: bytes 0-0/10369637
```

Ni 2 263 ni 13 370 bytes (firma de soft-404) en ninguno de los dos.
`Content-Type` correcto en ambos. Descarga completa: 78 902 567 y
10 369 637 bytes exactos.

```
$ sha256sum bd_endireh_2021_csv.zip
e4f1e7b1898cc53b3126ed959a9089091afd2ffdd1439911f5419e6c99c6037e
$ sha256sum endireh2021_fd.pdf
5c30a3f7f88123ca672f1042ec3b5c37cc1d7989f07fd23ecbf088cca6dda180

$ python3 tests/manifiesto.py --verifica --id endireh2021_bd_csv_zip
endireh2021_bd_csv_zip [data_raw]: COINCIDE — sha256 y tamaño (78902567 bytes) verificados
$ python3 tests/manifiesto.py --verifica --id endireh2021_fd_pdf
endireh2021_fd_pdf [data_raw]: COINCIDE — sha256 y tamaño (10369637 bytes) verificados
```

**Veredicto de durabilidad, en el sentido positivo:** el hash coincidió
exactamente en una sesión distinta, un host lógico distinto (worktree
nuevo), sin ningún byte heredado de la sesión que descargó originalmente.
El par `url_origen` + `sha256` **reprodujo el payload**. A diferencia del
incidente del 3/ago con el CPV (dos hashes distintos para la misma URL y
mismo tamaño, causa no determinada), aquí **no hubo discrepancia** — el
modelo "los bytes son desechables, la procedencia no" funcionó para este
par, esta vez.

## 3 · Acto B — las once variables contra el archivo, no contra el descriptor

El ZIP contiene **27 tablas** (no una lista aparte de "diccionario"): `TVIV`,
`TSDem`, `TB_SEC_III`…`TB_SEC_XX` (con partes `_2` y `XIII.I`),
`TB_SEC_FIN_ENTREV`, `TB_VD`. **No hay diccionario de datos embebido en
el ZIP como archivo separado** — el único texto de catálogo/wording
disponible para este paquete es el mismo `endireh2021_fd.pdf` ya
registrado. El chequeo "wording del diccionario del paquete vs. FD en
PDF" que pedía el encargo **no aplica tal como estaba planteado**: no hay
una segunda fuente independiente dentro de este ZIP con la que
contrastar — se declara así en vez de fabricar una comparación.

`TB_VD.csv`: 110 127 filas, 42 columnas — coincide exacto con "Número de
variables 42" que el FD declara para `TB_VD` (`fd.txt:676`). `POBT` (col.
13, "Población total de mujeres de 15 años y más") es **constante en 1**
en las 110 127 filas: confirma que la tabla completa **es** el universo
"mujeres 15 años y más", sin que sobre ni falte una fila.

**Hallazgo — `VFAM` no se llama, ni se comporta, como el resto del
grupo "por ámbito".** El header real es:

```
…"VESC_A","VESC_12M","VLAB_A","VLAB_12M","VCOM_A","VCOM_12M","VFAM","VPAR_A","VPAR_12M"…
```

`VFAM` aparece **una sola vez** — no hay `VFAM_A`/`VFAM_12M`. El FD
(cons. 35, `fd.txt:51730`) lo confirma: la descripción literal es
*"Condición de violencia total en el ámbito familiar **en los últimos 12
meses**"* — no existe, en este archivo, una versión "a lo largo de la
vida" del ámbito familiar. `§14.3`/`§18` de `hitoE` y el hallazgo del
77/ago en `forense/hallazgos.md` describen el grupo como `"VESC/VLAB/
VCOM/VFAM/VPAR × vida/12m"`, dando a entender (sin decirlo) que las
cinco siguen el mismo patrón dual — **no es así para `VFAM`**. El
descriptor prometió una variable con esa forma; el archivo trae una
distinta. Se corrige aquí, no se edita `§14.3`/`§18` (append-only).

Las **19 columnas reales** de "condición de violencia" en `TB_VD`
(los 11 nombres del encargo, expandidos donde el archivo trae dos
ventanas temporales), contra el archivo:

| Variable | Existe (nombre exacto) | Catálogo observado | Catálogo declarado (FD) | n total | Denominador real (con valor) | Denominador condicionado por |
|---|---|---|---|---|---|---|
| `VTOT_A` | sí | 1:74 859 · 2:34 817 · 9:451 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| `VTOT_12M` | sí | 2:64 657 · 1:44 989 · 9:481 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| `VPSI_A` | sí | 1:55 205 · 2:54 681 · 9:241 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| `VPSI_12M` | sí | 2:78 189 · 1:31 600 · 9:338 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| `VFIS_A` | sí | 2:72 827 · 1:37 014 · 9:286 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| `VFIS_12M` | sí | 2:99 100 · 1:10 647 · 9:380 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| `VECO_A` | sí | 2:78 491 · 1:30 629 · 9:1 007 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| `VECO_12M` | sí | 2:92 064 · 1:17 709 · 9:354 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| `VSEX_A` | sí | 2:58 943 · 1:50 901 · 9:283 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| `VSEX_12M` | sí | 2:86 859 · 1:22 859 · 9:409 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| `VESC_A` | sí | 2:72 473 · 1:31 739 · blanco:5 915 | 1,2,9,blanco | 110 127 | **104 212** | `POB_E_A`=0 (nunca estudió) — coincide exacto, 5 915=5 915 |
| `VESC_12M` | sí | blanco:99 035 · 2:8 924 · 1:2 168 | 1,2,9,blanco | 110 127 | **11 092** | `POB_E_12M`=0 (no estudió en 12m) — coincide exacto |
| `VLAB_A` | sí | 2:63 904 · 1:23 768 · blanco:21 367 · 9:1 088 | 1,2,9,blanco | 110 127 | **88 760** | `POB_L_A`=0 (nunca trabajó) — coincide exacto |
| `VLAB_12M` | sí | blanco:54 799 · 2:43 922 · 1:10 690 · 9:716 | 1,2,9,blanco | 110 127 | **55 328** | `POB_L_12M`=0 (no trabajó en 12m) — coincide exacto |
| `VCOM_A` | sí | 2:64 381 · 1:45 746 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — (ámbito comunitario no restringe universo, a diferencia de lo que el patrón de los otros 4 ámbitos sugeriría) |
| `VCOM_12M` | sí | 2:88 308 · 1:21 806 · 9:13 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — |
| **`VFAM`** | **sí, una sola columna (no `VFAM_A`/`VFAM_12M`)** | 2:98 609 · 1:11 518 | 1,2,9 | 110 127 | **110 127 — sin condicionar** | — (y **mide solo últimos 12 meses**, ver hallazgo arriba) |
| `VPAR_A` | sí | 2:63 640 · 1:41 576 · blanco:4 849 · 9:62 | 1,2,9,blanco | 110 127 | **105 278** | `POBP`=0 (`T_INSTRUM`=C2, "nunca ha tenido novio") — coincide exacto, blanco=4 849=`C2`=4 849 |
| `VPAR_12M` | sí | 2:82 990 · 1:22 215 · blanco:4 849 · 9:73 | 1,2,9,blanco | 110 127 | **105 278** | ídem `VPAR_A` |

Ningún valor observado cae fuera del catálogo declarado en el FD — cero
códigos sorpresa.

**Chequeo anti-`BP1_20`, por variable, con n.** El defecto retirado
medía *denuncia condicionada a haber sido victimizada* (`RESUL_H='A'`
en el 100% de los casos de `TMod_Vic`/ENVIPE) — conducta posterior, no
exposición. Contra ese patrón específico:

- **`VTOT_A/12M`, `VPSI`, `VFIS`, `VECO`, `VSEX` (×vida/12m), `VCOM`
  (×vida/12m) y `VFAM`** — **pasan.** Los 13 tienen denominador = 110 127
  = el universo completo de mujeres 15+, **sin condicionar sobre haber
  sufrido violencia ni sobre ningún subgrupo**. Miden la incidencia
  misma ("condición de violencia… con/sin incidencia"), no una conducta
  posterior a ella. Ninguno excluye de su denominador a quien no reportó
  violencia.
- **`VESC` (×vida/12m)** — denominador angosto por diseño, pero **no**
  por el defecto de `BP1_20`: el recorte es "mujeres que alguna vez
  estudiaron" (104 212) o "en los últimos 12 meses" (11 092), no
  "mujeres que ya sufrieron violencia". Es un recorte de aplicabilidad
  de ámbito, legítimo y cuantificado, distinto en naturaleza al defecto
  retirado — pero real: `VESC` no puede hablar de exposición para el
  universo completo de mujeres 15+, solo para quien estudió.
- **`VLAB` (×vida/12m)** — mismo patrón: denominador = 88 760 (alguna
  vez trabajó) o 55 328 (últimos 12 meses), recorte por aplicabilidad,
  no por victimización previa.
- **`VPAR` (×vida/12m)** — denominador = 105 278 (mujeres con pareja o
  expareja, `T_INSTRUM`≠C2), mismo tipo de recorte.

Ninguna de las 19 columnas repite el defecto exacto de `BP1_20`
(condicionar sobre la propia violencia). Tres de las once "familias"
(`VESC`, `VLAB`, `VPAR`) sí condicionan sobre aplicabilidad de dominio, y
**dos de los cinco ámbitos declarados como "progresivamente más
angostos por diseño" no lo son en los datos** — `VCOM` y `VFAM` tienen
el mismo denominador sin restringir que `VTOT`/`VPSI`/`VFIS`/`VECO`/
`VSEX`. Esto corrige, con números, la generalización de `§14.3`
("los ámbitos tienen universos progresivamente más angostos") — cierta
para 3 de 5, no para los 5.

### 3.1 · Límite de lectura de este Acto

Se abrió y se leyó por completo: `TB_VD.csv` (las 42 columnas, valor por
valor, las 110 127 filas). Se leyeron los **headers** de `TSDem.csv`,
`TVIV.csv` y `TB_SEC_IV.csv` (para el Acto C, ejes) y se contaron sus
filas, sin leer el contenido celda a celda. **No se abrieron las 23
tablas `TB_SEC_*` restantes como CSV** — su contenido se conoce solo por
el resumen de tabla de contenidos del FD (§4 abajo) y por grep de
palabras clave sobre el texto completo del FD, no por lectura íntegra
del PDF sección por sección ni por apertura de esos CSV.

## 4 · Acto C — C2, C3, ejes

### C2 — desenlaces de `G4`

Se leyó el resumen de contenido de **las 27 tablas** en el FD (`2.1
Descripción de las tablas`, `fd.txt:150-320`, texto completo, no
truncado) y se corrió `grep` sobre el documento entero (51 795 líneas)
para `protesta`, `autodefensa`, `policía comunitaria`, `ronda
comunitaria`, `manifestación`, `linchamiento`, `insegur*`: **cero
resultados en las siete búsquedas.** La única sección con contenido
adyacente a "recursos frente a un problema" es `TB_SEC_XVI` ("Recursos
sociales"), leída completa (`fd.txt:47850-48120` y siguientes): pregunta
por redes de apoyo (pedir dinero/cuidado de hijos/compañía a
vecinas/amigas/familiares) y por actividades sociales (salir con
amigas, reuniones religiosas o "de colonos o de organizaciones",
deporte) — **no** por protesta pública, autodefensa comunitaria/rondas,
ni por guardar silencio frente a inseguridad. `denunci*` da 755
resultados, pero en contexto de denuncia de la violencia sufrida por la
propia mujer (ante el Ministerio Público, síndico, etc.), no de agravio
urbano ni de conflicto agrario/rural.

**C2 se cierra, no se deja abierto**, con el límite de lectura declarado:
esta verificación cubrió el resumen de las 27 tablas completo + búsqueda
de palabras clave sobre el texto íntegro del FD (no la lectura íntegra
ítem por ítem de las ~23 secciones no relacionadas con `TB_VD`, `TVIV` o
`TSDem`). Sobre esa base, **ENDIREH no observa los tres desenlaces de
`G4`** (`civico.protesta.agravio_urbano`, `civico.autodefensa.
agravio_rural`, `comunicacion.inseguridad.ver_oir_callar`). Si una
lectura ítem-por-ítem futura encontrara algo que el resumen de tabla y
las palabras clave no capturaron, esta declaración se corrige con adenda
fechada, igual que se corrigió `VFAM` arriba — no se pretende blindaje.

### C3 — circularidad contra Tabla B, re-derivada

```
$ grep -in endireh forense/notas/2026-07-31-inventario-segmentacion.md
(sin resultados, exit 1)
```

**Pasa, re-derivado directamente contra el archivo actual** (no heredado
de `paso1`). ENDIREH no aparece entre las fuentes de `TABLA B — Reglas
del motor` (`inventario-segmentacion.md:121`).

### Ejes de atributos disponibles — del microdato real, no del descriptor

El vector de 6 ejes es de `canon/modelo-decision-v4_0.md:110` (§1.1.A,
derivado de **ENIGH**, otra fuente). Lo que sigue es qué tiene **ENDIREH**
para cada uno, verificado contra columnas reales con n:

| Eje (canon) | ¿Existe en ENDIREH? | Variable, tabla, n |
|---|---|---|
| 2 · Edad | **Sí, directo** | `EDAD`, `TSDem.csv`, n=432 746 (todos los residentes de las viviendas seleccionadas, no solo las 110 127 mujeres 15+ — habría que filtrar por `COD_M15`/`REN_MUJ_EL` para aislar exactamente ese subconjunto; no se hizo en este acto) |
| 5 · Acceso digital | **Sí, mismo nivel y misma debilidad que en ENIGH** | `P1_4_5` (teléfono celular), `P1_4_9` (servicio de internet), `TVIV.csv`, n=122 646 viviendas — tenencia binaria a nivel hogar, sin distinguir uso individual, igual límite que declara `§1.1.A` para su propio eje 5 |
| 3 · Urbanización/tamaño de localidad | **Parcial — variable distinta, escala más gruesa** | `DOMINIO` (U/Complemento urbano/R, 3 categorías), presente en `TVIV` (122 646), `TSDem` (432 746) y `TB_VD` (110 127) — **no** es `tam_loc` (4 categorías por tamaño de población); es un proxy más burdo, no intercambiable sin reclasificar |
| 4 · Ingreso | **Parcial — nivel y constructo distintos** | `TB_SEC_IV.csv`, n=110 127 (exactamente las mujeres 15+): ingreso mensual **de la mujer seleccionada**, por fuente (`P4_9_1`…`P4_9_7`: jubilación/pensión, remesas de familiares en EUA, etc.) — es ingreso **de persona**, no el `ing_cor` de **hogar** ni el catálogo `est_socio` que usa `§1.1.A`; no es sustituible sin reconstrucción |
| 1 · Formalidad laboral | **Sin equivalente confirmado** | `TSDem.csv` trae `P2_15` (posición en la ocupación: empleada/obrera/jornalera/cuenta propia/patrón/sin pago), n=88 760 (condicionado a haber trabajado) — es un constructo distinto de `segsoc`/derechohabiencia (afiliación a seguridad social); no se encontró variable de afiliación a IMSS/ISSSTE para la persona en las tablas revisadas |
| 6 · Condición migratoria | **Sin equivalente confirmado** | No se encontró variable de lugar de nacimiento, residencia previa ni residencia en EUA/otro país en `TSDem`, `TVIV` ni `TB_SEC_IV` (los únicos headers revisados). `COD_RES` (`TVIV`) es estatus de cobertura de la entrevista, no migración. **No verificado en las 23 tablas restantes** — declarado sin equivalente en lo leído, no sin equivalente en el instrumento completo |

Resumen cuantificado: **1 eje con equivalente directo confiable (edad),
1 con equivalente al mismo nivel de debilidad que el original (acceso
digital), 2 parciales de otro nivel/constructo (urbanización, ingreso),
2 sin equivalente confirmado en lo leído (formalidad laboral,
migración)**. Esto difiere de la caracterización de `§18` de `hitoE`
("edad, urbanización, acceso digital… confiables; ingreso… parcial;
formalidad laboral y migración… sin equivalente") en la clasificación de
urbanización — aquí se cuenta como parcial, no confiable, porque
`DOMINIO` no es `tam_loc` y la nota de `§18` no tenía el archivo abierto
para notar la diferencia de escala. Se declara la discrepancia en vez de
callarla.

## 5 · Declaración de contaminación (ADR-46)

Esta sesión **abrió** el ZIP de microdatos de ENDIREH 2021 (`TB_VD.csv`
completo, headers de `TSDem`/`TVIV`/`TB_SEC_IV`) y el texto completo del
FD PDF. **Queda inhabilitada para pre-registrar contra ENDIREH.**

## 6 · Declaración de durabilidad de la raíz de esta sesión

Esta sesión corrió en `/home/pc0/mm-endireh-paso1bis`, un worktree de
git bajo el `$HOME` persistente del host `FF-5563` (`Ubuntu 26.04 LTS`,
sin `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`) — **no** en un clon efímero de
sandbox de nube como el que describe PF-3. Evidencia indirecta a favor de
que esta raíz **sí** persiste entre sesiones: al abrir esta sesión ya
existían en `/home/pc0` más de 15 worktrees de sesiones anteriores
(algunas de fechas hasta el 29/jul/2026), varias con ramas locales vivas
no fusionadas y `data/raw` poblada de sesiones previas en al menos un
checkout hermano. Eso indica que el filesystem del host sobrevive entre
sesiones distintas del agente. **No se verificó de forma directa** (no
se dejó un archivo marcador y se esperó a la siguiente sesión para
confirmarlo) — se declara "probablemente durable, por evidencia
indirecta y no confirmada directamente", no "durable".

## 7 · Suite

Corrida antes de esta nota (línea base, confirmando VERDE previo) y
después de escribir todos los archivos de este acto:

```
$ python3 tests/check.py --baseline
19 FAIL · 84 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json

$ python3 tests/validador_registro_ids.py
OK — 49 reglas · 27 en perímetro · 49 IDs verificados
```

Sin rojo nuevo.

## 8 · Qué le falta a paso 2 (no se hace aquí)

Elegir entre agregado (`VTOT_A`/`VTOT_12M`) y desglose por tipo/ámbito —
CP-1, sigue en mesa. Si se elige desglose, decidir qué hacer con `VFAM`
(único sin ventana "a lo largo de la vida") y con el hecho de que
`VCOM`/`VFAM` no se recortan por ámbito mientras `VESC`/`VLAB`/`VPAR` sí.
Medir la condicional con ponderación (`FAC_MUJ`) y diseño muestral
(`UPM_DIS`/`EST_DIS`/`ESTRATO`), no solo con conteos crudos como los de
esta nota. Filtrar `TSDem`/`TB_SEC_IV` a exactamente las 110 127 mujeres
15+ para los ejes de atributos, cosa que este acto no hizo.
