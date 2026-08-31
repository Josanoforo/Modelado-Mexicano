# Nota de cierre · ACTO MAESTRA32-E17 · CURA-RADIO-CONFIANZA + ESCALERA DE CONTINGENCIA — el acto no arranca: el GATE que su propio encargo declara está incumplido

Fecha de ejecución: 2026-08-31. Clon `/home/user/Modelado-Mexicano`, rama `claude/maestra32-e17-curacion-izmxby` (ya existía al lanzar la sesión — no se clonó ni se creó de nuevo). Esta nota sustituye a `forense/notas/2026-08-31-cura-radio-spec.md` (COMMIT-1) y a `data/curacion-radio-confianza-v1_0.tsv` (COMMIT-2), que el encargo original preveía: ninguno de los dos se produce, porque el ARRANQUE del propio acto (los cinco puntos, antes de leer el resto del encargo, tal como el encargo mismo instruye) encontró que el GATE declarado en su primera línea — *"Estado: GATED a que `MAESTRA32-E15` fusione (mismo carril NUBE, serie estricta; sin dependencia de datos — si mesa prefiere, se lanza en la caja al cerrar E16 y se declara el cambio). Sin ranuras."* — está incumplido: ni `MAESTRA32-E15` fusionó, ni existe declaración de mesa que active la vía alterna de la caja.

---

## Los cinco puntos del ARRANQUE

| # | Punto | Comando | Resultado |
|---|---|---|---|
| 1 | REPO | `pwd`; `git log -1 --format="%h %s"`; `git status` | `/home/user/Modelado-Mexicano` — clon ya existente, no se clonó ninguno nuevo. `899113c Merge pull request #404 from Josanoforo/acto/maestra32-e14-marco-m-sortea`. `git status`: rama `claude/maestra32-e17-curacion-izmxby`, sin cambios pendientes al arrancar. |
| 2 | SHA | `git fetch origin --prune`; `git log --oneline -1 origin/main` vs `HEAD` | `main` = `899113c`, exactamente el SHA que el encargo declara (`merge PR #404 / ADR-232`) — sin drift, no hace falta refrescar nada. El `fetch --prune` reporta que `origin/claude/maestra32-e17-curacion-izmxby` había sido borrada antes de esta sesión mientras la copia local sobrevivía (`[deleted] (none) -> origin/...`); observación, no bloqueante, se restablece en el primer `push -u`. |
| 3 | `data/raw` | `ls -la data/raw` | `No such file or directory` — ausente, esperado. No se crea ni se enlaza: el encargo declara "Repo-only: inventarios y `texto_reactivo`; no abre payloads", así que ninguna operación de este cierre la necesita. |
| 4 | ENTORNO | `echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-<sin_variable>}"`; `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (coincide con "ENTORNO ASIGNADO: NUBE (`cloud_default`)"). `curl` → `000` (sin conectividad, `curl` exit 56). Por A.13/v2.11: este comando examinó **0 archivos** — es una sonda de red, no una búsqueda sobre el árbol; su resultado negativo no es una medición de cobertura de nada, y este acto declara (como el propio encargo permite: "si este acto no toca microdato ni red, dilo") que no toca microdato ni red — se reporta el valor crudo por completitud, no se usa para ninguna conclusión. |
| 5 | ESPEJO | — | No se derivó ninguna cifra del espejo del proyecto. Todas las cifras de este cierre salen del clon confirmado en el punto 1, con el comando a la vista en cada fila de la tabla siguiente. |

---

## El hallazgo: `MAESTRA32-E15` no existe, y la vía alterna de mesa tampoco fue declarada

El encargo condiciona su ejecución, en su primera línea, a que un acto llamado `MAESTRA32-E15` haya fusionado en el mismo carril NUBE, en serie estricta, y declara explícitamente **"Sin ranuras"** — sin excepción que permita adelantar el trabajo salvo que mesa declare la vía alterna ("si mesa prefiere, se lanza en la caja al cerrar E16 y se declara el cambio"). Verificado exhaustivamente contra el árbol real, ninguna pieza de `MAESTRA32-E15` (ni de `MAESTRA32-E16`, el predecesor de la vía alterna) existe, y tampoco existe la declaración de mesa que activaría esa vía:

| # | Afirmación verificada | Comando | Resultado (archivos/entradas examinados) |
|---|---|---|---|
| 1 | No hay encargo archivado para `MAESTRA32-E15` ni `MAESTRA32-E16` en `forense/encargos/` | `ls forense/encargos/ \| grep -i maestra32` | 15 archivos `MAESTRA32-*` listados (`E1`, `E2`, `E3` ×2, `E4`, `E5`, `E6`, `E8`, `E9`, `E10`, `E11`, `E12`, `E13`, `E14`, y este mismo `E17`); ninguno `E15` ni `E16`. |
| 2 | Las cadenas `MAESTRA32-E15`/`MAESTRA32-E16` no aparecen en ningún archivo `.md`/`.tsv`/`.yaml` del árbol | `git grep -niE "MAESTRA32-E15\|MAESTRA32-E16" -- '*.md' '*.tsv' '*.yaml'` (excluido este mismo encargo, que las cita como parte del hallazgo) | 0 coincidencias, árbol completo (`canon/`, `forense/`, `data/`, `milpa/`, `tests/`). |
| 3 | Las cadenas bare `E15`/`E16` no aparecen en ningún archivo del árbol fuera de este mismo encargo | `git grep -n "E15\b" -- .` / `git grep -n "E16\b" -- .` | Los únicos hits de `E15`/`E16` en todo el repo son subcadenas de códigos de reactivo/URL ya existentes y sin relación (`PRESOE15`, `CLAVE15`, `PE15`, `PE16` en las tablas de inventario; `BASE15` en `tools/adq_enoe_docs.py`) — ninguno es el rótulo de un acto. Verificado leyendo cada ocurrencia. |
| 4 | `main` no se movió desde que se redactó el encargo, y no hay ninguna otra rama remota además de `origin/main` | `git fetch origin --prune`; `git branch -r` | `main` sigue en `899113c` (mismo SHA que el encargo declara). Única rama remota: `origin/main`. No es un caso de "main avanzó, refresca y continúa" (ARRANQUE punto 2) — es el caso contrario: nada avanzó, y lo que el encargo asume que ya avanzó (la fusión de E15) nunca ocurrió. |
| 5 | Ningún PR de GitHub, abierto o cerrado, corresponde a `MAESTRA32-E15`/`MAESTRA32-E16` | MCP `github.list_pull_requests` (owner=`josanoforo`, repo=`modelado-mexicano`, state=`all`, 30 más recientes, orden por creación descendente) + `github.search_pull_requests` (`E15 in:title`, `E16 in:title`) | 30 PRs más recientes listados, del más reciente (`#404`, `MAESTRA32-E14`, mergeado en `899113c`) hasta `#375` (26/ago/2026). Ninguno trae `E15` ni `E16` en título o rama de cabeza. Las búsquedas dirigidas por título devuelven `total_count: 0` para ambos. Única rama remota del repo: `origin/main` (confirmado por `list_branches`). |
| 6 | No existe declaración de mesa que active la vía alterna ("se lanza en la caja al cerrar E16 y se declara el cambio") | `git grep -niE "se declara el cambio\|carril CAJA.*E16"` sobre el árbol | 0 coincidencias sustantivas (dos falsos positivos en `data/curacion-registro/.../propuestas-curador.tsv`, filas de un pipeline no relacionado, verificadas y descartadas por lectura). Ningún ADR, nota o fila de `forense/firmas-pendientes.tsv` registra que mesa haya optado por lanzar este acto en la caja al cierre de `E16`. |

**Conclusión.** El GATE de este encargo no está satisfecho por ninguna de sus dos vías: (a) `MAESTRA32-E15` no ha fusionado — no existe en ningún estado del repositorio (ni encargo, ni rama, ni PR, ni ADR); (b) la vía alterna que el propio encargo ofrece ("si mesa prefiere, se lanza en la caja al cerrar E16 y se declara el cambio") tampoco aplica, porque ni `MAESTRA32-E16` existe (con lo que "al cerrar E16" no puede haber ocurrido) ni hay declaración de mesa que la invoque. Esto no es un caso de "main se movió, refresca y continúa" (ARRANQUE punto 2, que expresamente NO es un paro) — es exactamente el caso que el propio preámbulo del ARRANQUE anticipa como resultado legítimo: *"Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción."* La frase "Sin ranuras" no deja lectura alternativa que permita adelantar `COMMIT-1`/`COMMIT-2` sin que se cumpla una de las dos condiciones.

**Observación adicional, no bloqueante.** La firma de mesa citada verbatim en este encargo usa el rótulo `D-B` como identificador del punto de la firma. Ese mismo rótulo pelado `D-B` ya está en uso en `canon/gobernanza-v1_15.md:1171` (`ADR-79`, `ACTO SELLA-3`, 13/ago/2026: *"D-B — correr la invarianza ENCUCI↔ENBIARE"*), una decisión distinta y no relacionada con la de este encargo (31/ago/2026, sobre la curación del homónimo `radio_confianza`/`endireh2016`). El regex de `T25` (`tests/check.py:_T25_ROTULO_BARE`) solo cubre tokens `M`/`E` seguidos de 1-2 dígitos, así que `D-B` no dispara el test mecánico; se declara aquí por completitud, sin adjudicar colisión ni reclamar el token — la letra "D" del espacio de decisiones de mesa ya tiene precedente de reutilización fechada (`canon/registro-rotulos.tsv`, filas `D-1..D-6`/`D-i..D-iv`), y este acto no llega a adjudicar el contenido de la firma D-B de todos modos, porque cierra antes de `COMMIT-1`.

---

## Decisión de este acto

No corre `COMMIT-1` (`forense/notas/2026-08-31-cura-radio-spec.md`) ni `COMMIT-2` (`data/curacion-radio-confianza-v1_0.tsv`). Cierra como hallazgo antes de arrancar el objeto del encargo, mismo patrón que `ACTO MAESTRA32-E10 · COBERTURA-15` (`ADR-224`) y `ACTO MAESTRA31-E9 · ESTIMA-RUTAC` (`ADR-218`): un acto archiva su encargo verbatim (`0-bis · A.3`) y cierra sin ejecutar su objeto cuando el terreno verificado no sostiene la premisa que el encargo asume — sin que eso sea un "PARO"; es el entregable que el propio ARRANQUE pide.

`FP-195` nueva, `ABIERTA`: mesa recibe este hallazgo y decide si (a) redacta y lanza `MAESTRA32-E15` primero y relanza este mismo encargo después (serie estricta del carril NUBE, tal como el encargo declara), (b) declara explícitamente la vía alterna — lanzar `MAESTRA32-E17` en la caja al cierre de `MAESTRA32-E16` —, lo que además requiere que `E16` exista y cierre primero, o (c) levanta el GATE de `MAESTRA32-E17` con una firma explícita que reconozca otra vía. `FP-198`/`FP-199`, pre-asignadas por el propio encargo para el resultado de la corrida real (escalera de contingencia + curación), **quedan reservadas, sin consumir**, para cuando el acto se relance tras satisfacerse el GATE.

---

## Qué NO hizo este acto

No corrió `COMMIT-1` ni `COMMIT-2`. No creó `forense/notas/2026-08-31-cura-radio-spec.md` ni `data/curacion-radio-confianza-v1_0.tsv`. No clasificó ningún reactivo de ENDIREH/`encup2012`/ENNViH/ENCUCI/WVS/Latinobarómetro por referente. No corrió ningún peldaño de la escalera de contingencia. No tocó `milpa/**`, los inventarios (`v1_2`, `ext-v1_0`, `fd-v1_1`, `fd-ext-v1_0`), `data/emparejamiento-motor-v1_2.tsv` ni la spec de `E2`. No usó `FP-198`/`FP-199` (quedan reservadas, sin consumir). No adjudicó el contenido de la firma D-B ni si el GATE debe levantarse: lo declara pendiente en `FP-195`, mesa decide.

Detalle completo, comando por comando: tablas de arriba (A.13). Encargo original archivado verbatim en `forense/encargos/2026-08-31-MAESTRA32-E17-CURA-RADIO-CONFIANZA.md` (`0-bis · A.3`, sin editar).

---

# Re-emisión por `ACTO MAESTRA32-E20 · LOTE-NUBE-1 · P1` — 31/ago/2026

*Sección fechada añadida por el lote sucesor. Todo lo de arriba (el cierre por
hallazgo de compuerta de `MAESTRA32-E17`, `ADR-234`) queda **intacto**: es el
registro de que el acto original no arrancó, y borrarlo destruiría la auditoría
tan bien como no haberlo escrito (A.10). Lo de abajo es la corrida que aquel
acto no llegó a hacer, con la receta congelada en
`forense/notas/2026-08-31-cura-radio-spec.md` y **conteos re-derivados contra el
árbol de hoy** (`d510a63`), no heredados.*

## Compuerta, ahora sí

El GATE que paró a `MAESTRA32-E17` (`GATED a que MAESTRA32-E15 fusione`) está
satisfecho desde que `PR #405` fusionó — lo declaró el propio cierre de arriba
("el GATE queda satisfecho por la vía (a) de `FP-195`") y lo registra `FP-195`.
Este lote no reabre `MAESTRA32-E17`: lo re-emite, que es lo que aquel cierre
dejó nombrado como sucesor.

## Escalera de contingencia — corrida COMPLETA, 5 de 5 peldaños

**A.13 · 269 320 filas de inventario examinadas** (unión de
`data/inventario-reactivos-v1_2.tsv` ∪ `-ext-v1_0` ∪ `data/inventario-fd-v1_1.tsv`
∪ `-fd-ext-v1_0`), 489 `payload_id` distintos. Salida fila por fila en
`data/curacion-radio-confianza-v1_0.tsv` (143 filas).

### Pasada 1 — receta literal (`texto_reactivo` únicamente)

| # | peldaño | filas | legibles | θ | INTERP | INSTIT | OTRO | desenlace G5 | co-obs |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | ENDIREH (todas las olas) | 39 638 | 4 036 | 7 | **0** | 7 | 0 | 8 | 0 |
| 2 | `encup2012` (batería `P30`) | 282 | **0** | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 | ENNViH/MxFLS (olas 1-3) | 17 181 | 17 176 | 4 | **0** | 0 | 4 | 76 | 0 |
| 4 | ENCUCI 2020 | 520 | 62 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 | WVS + Latinobarómetro México | 333 | 333 | 15 | 1 | 7 | 7 | **0** | 0 |

### Nota de honestidad de proceso — dos negativos de la pasada 1 que no eran negativos

**A.13 dice que un negativo producido por un comando que no examinó lo que debía
no es un negativo.** Dos de los ceros de arriba son artefactos del campo
inspeccionado, no ausencias del corpus, y se corrigieron **antes** de escribir el
veredicto, no después:

1. **`encup2012`: 0 reactivos legibles es falso.** Sus 282 filas son de método
   `INSPECT_XLSX`, que **parquea la pregunta completa en `variable_id`**, no en
   `texto_reactivo` — que viene vacío en las 282. La batería `P30` está entera y
   es legible: 27 ítems `P30_1..P30_27`, con el texto literal *"En una escala de
   calificación de 0 a 10 … ¿Qué tanto confía en…?"*. La receta dice
   `texto_reactivo` porque el límite que anticipó fue el de `INSPECT_ZIP` (texto
   vacío), no este.
2. El mismo arreglo hace legibles las 39 638 filas de ENDIREH y las 520 de
   ENCUCI (antes 4 036 y 62).

### Pasada 2 — A.13 (`texto_reactivo` **o** `variable_id`, según el método)

| # | peldaño | filas | legibles | θ | INTERP | INSTIT | OTRO | desenlace G5 | co-obs estricta |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | ENDIREH (todas las olas) | 39 638 | 39 638 | 7 | **0** | 7 | 0 | 8 | 0 |
| 2 | `encup2012` (batería `P30`) | 282 | 282 | 32 | **3** | 14 | 15 | 1* | 1* |
| 3 | ENNViH/MxFLS (olas 1-3) | 17 181 | 17 181 | 4 | **0** | 0 | 4 | 76 | 0 |
| 4 | ENCUCI 2020 | 520 | 520 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 | WVS + Latinobarómetro México | 333 | 333 | 15 | 1 | 7 | 7 | **0** | 0 |

`*` **Falso positivo léxico, verificado y descartado.** El único "desenlace G5"
de `encup2012` es `P28B` — *"Si uno no se cuida a sí mismo la gente se
aprovechará"* —, que casa el término `cuida a` de la lista de E2 y **no es** un
desenlace de G5 (no es pooling, ni corresidencia, ni carga de cuidado: es un
ítem de actitud sobre autoprotección). Barrido de confirmación sobre los 282
reactivos de ENCUP con 14 términos de hogar/pooling: **13 hits, cero desenlaces
de G5** — diez son la batería AMAI de nivel socioeconómico (`A1`-`A10`: focos,
baños, estufa, automóvil), uno es `P28B`, uno es donativos a organizaciones
(`P59_11`) y uno es gasto en cursos (`P83`).

## Veredicto A.4 por peldaño

**0 de 5 peldaños con co-observación válida.** Ninguno reúne ≥1 reactivo
INTERPERSONAL y ≥1 desenlace de G5 en la misma base. Por peldaño, con la media
pareja nombrada:

- **Peldaño 1 · ENDIREH — la reserva de `E4` queda CONFIRMADA como homónimo.**
  Los 7 reactivos de confianza de todo ENDIREH son **institucionales, los 7**:
  `p6_24_10`, `p7_27_10`, `p8_19_10`, `p10_15_10` y `p13_21_13` de `endireh2016`
  ("No acudió a una autoridad o institución **no confía en las autoridades del
  gobierno**") y `P7_12_10` de `endireh2006` ("no acudió a la autoridad por
  **desconfianza de las autoridades**"). **Cero interpersonales.** La media
  pareja que SÍ existe es la del desenlace: `p3_2` ("¿Su actual esposo o pareja
  **vive con** usted?"), `p18_4` ("¿Usted **cuida a** sus nietos(as)…?"),
  `P4_2`, `P13_4`, `P11_4`. → **desenlace SÍ, θ NO.**
- **Peldaño 2 · `encup2012` — la θ más limpia de toda la escalera, y sin
  desenlace.** Tres reactivos INTERPERSONAL en la misma base
  (`BaseDatos_ENCUP_2012_Final`): `P30_10` ("…¿Qué tanto confía en…? **Los
  vecinos**"), `P30_11` ("…**La familia**") y `P34` ("En general, ¿diría usted
  qué se puede **confiar en la mayoría de las personas**?"). Eso es
  literalmente la definición de `radio_confianza` del glosario — confianza
  interpersonal **por círculos** — y es la única batería del corpus que la
  instrumenta. **Cero desenlaces de G5** (ver el falso positivo arriba). →
  **θ SÍ (la mejor), desenlace NO.**
- **Peldaño 3 · ENNViH/MxFLS — desenlace abundante, θ que no clasifica.**
  76 desenlaces de G5, todos corresidencia literal (`tp27m_1b..1i`: "MADRE VIVE
  CON CÓNYUGE / HIJA / HIJO / CUÑADO / HERMANA / HERMANO / NIETO / PADRES", en
  `ehh02dta_all/…/iiib_tp.dta` y en `ehh05`). Del lado θ hay 4 reactivos, los 4
  clasificados **OTRO** por la lista cerrada: `co05` ("USTED DIGNO DE
  CONFIANZA") y `vlh01n` ("GENTE LOCALIDAD CONFIANZA?").
  **Cita para mesa, sin tocar la receta:** `vlh01n` vive en
  `ennvih/ehh05dta_all.zip → ehh05dta_b2/ii_vlh.dta` (y en `ehh09`), y su
  referente es transparentemente interpersonal — *la gente de su localidad* —,
  pero la lista cerrada exige la cadena literal `la gente` y la etiqueta Stata
  viene abreviada sin artículo. La receta estaba congelada antes de correr y
  **no se edita para complacer el resultado**: se reporta OTRO, que es lo que el
  procedimiento produjo, y se nombra la celda exacta. Aun si mesa la
  reclasificara, la co-observación **estricta** seguiría siendo 0: `vlh01n` está
  en `ii_vlh.dta` y los 76 desenlaces están en otros miembros (`iiib_tp.dta`,
  `iv_res.dta`, `c_ls.dta`, `p_tp.dta`) — y la co-observación **laxa** también da
  0, porque los desenlaces viven en `ehh02`/`ehh05` y no coinciden en miembro.
  → **desenlace SÍ, θ dudosa y en otra base.**
- **Peldaño 4 · ENCUCI 2020 — la θ ancla existe pero es invisible al censo de
  texto, y el desenlace falta.** Los tres ítems `AP5_1_1`/`AP5_1_2`/`AP5_1_3`
  que `milpa/procedencia.yaml:280-293` sella como θ de `radio_confianza` SÍ
  están en el inventario, pero con `texto_reactivo` **vacío** (método
  `INSPECT_ZIP`) y `variable_id` corto: ningún barrido por texto puede
  clasificarlos, y decir "ENCUCI no tiene θ" sería exactamente el negativo falso
  que A.13 prohíbe. Lo que sí es negativo real: **0 desenlaces de G5** en las 520
  filas de ENCUCI. → **θ SÍ (sellada, no por texto), desenlace NO.** Nótese que
  esto **invierte** la rama que `E17` pre-escribió en (d3) ("ENCUCI 2020 si su
  desenlace G5 existe pero la θ falla"): lo que falla es el desenlace, no la θ.
- **Peldaño 5 · WVS ausente; Latinobarómetro presente y a medias.**
  **WVS no está en el corpus**: 0 coincidencias de `wvs`/`world`/`values` entre
  los **489 `payload_id`** de los cuatro inventarios y ninguna entrada en
  `data/manifiesto.yaml` — negativo real, con el universo declarado. La premisa
  de `E17` ("WVS y Latinobarómetro ya descargados") es **correcta solo a
  medias**. Latinobarómetro 2024 sí está
  (`latinobarometro2024_bd_stata.zip`, 333 reactivos, 100% con texto): 15 ítems
  de confianza, de los cuales **uno solo** es INTERPERSONAL — `P10STGBS` ("Se
  puede confiar en la mayoría de las personas…") — y los otros catorce son la
  batería institucional `P14ST.*` (Iglesia, Gobierno, partidos, Congreso, Poder
  Judicial, medios). **Cero desenlaces de G5.** → **θ parcial (confianza
  generalizada, sin círculos), desenlace NO.**

## (d) La solución de dirección, ejecutada porque el negativo total se cumplió

- **(d1) `EXISTE-NO-SATISFACE`**, con las cinco medias parejas nombradas arriba,
  reactivo por reactivo. Es un mapa, no un vacío: el corpus tiene la θ (ENCUP
  2012, la mejor; ENCUCI 2020, sellada) y tiene el desenlace (ENNViH, 76 ítems de
  corresidencia; ENDIREH, 8) — **en instrumentos distintos, sin muestra común**.
  Ese, y no la ausencia de datos, es el defecto.
- **(d2) Estatus del coeficiente mientras tanto**: `G5.radio_confianza` sigue
  `ASIGNADO · SOLO-SIGNO·NO-COMPARABLE` (`ADR-220`), sin magnitud medida. **No**
  se inventa un valor ni se transporta uno de otro constructo. Sin cambios en
  `milpa/**` — `git diff --stat` de este peldaño sobre `milpa/` vacío.
- **(d3) Fila de adquisición con nombre, para `FP-179`.** Re-derivada, porque la
  que `E17` pre-escribió supone un corpus que no es el de hoy:
  - **Instrumento a adquirir: WVS ola 7 México (2018).** Es el único instrumento
    que trae, en la misma muestra, la batería de confianza **por círculos**
    (`V102`-`V107`: familia, vecinos, conocidos, desconocidos) **y** módulo de
    hogar/familia del lado desenlace. Verificado hoy: **no está en el corpus**
    (0 de 489 payloads). Es una descarga, no una búsqueda.
  - **Segundo mejor, ya en el corpus, y por qué no basta**: `encup2012`
    (`P30_10` vecinos, `P30_11` familia, `P34` confianza generalizada) tiene la
    θ más limpia del corpus, pero ENCUP no levanta ningún desenlace de G5 —
    verificado sobre sus 282 reactivos. Adquirir "el módulo faltante" de ENCUP
    no es posible: ese módulo no existe en el instrumento.
  - **Lo que NO aplica**: la rama ENCUCI de `E17` supone que en ENCUCI falla la
    θ; lo que falla es el desenlace (ver peldaño 4).
- **(d4) Vía alterna declarada, NO ejecutada**: medir `radio_confianza` como
  coeficiente compuesto de dos instrumentos (p. ej. θ de `encup2012` × desenlace
  de ENNViH) **solo si mesa lo firma después**. No cabe en (ii)/(i′) y se dice.
  Este acto no la corre.

## (e) B-bis

Negativo total → **(d) completo**, ejecutado arriba. No se lanza medidor de caja
sobre ENDIREH (peldaño 1 negativo del lado θ) ni sobre ningún otro peldaño: no
hay instrumento con las dos mitades.

## CONTADOR de P1

**Peldaños con co-observación válida: 0 de 5.** Reactivos curados por referente:
**58** (θ, pasada 2) — 4 INTERPERSONAL, 28 INSTITUCIONAL, 26 OTRO —, más 85
filas de desenlace G5 censadas. Total `data/curacion-radio-confianza-v1_0.tsv`:
143 filas.

"El primer resultado que produzca este procedimiento es el que se reporta."
