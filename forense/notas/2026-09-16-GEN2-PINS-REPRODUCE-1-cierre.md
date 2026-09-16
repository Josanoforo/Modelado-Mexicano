# ACTO GEN2-PINS-REPRODUCE-1 · materializar el bloque REPRODUCE, y por qué P2/P3 no corrieron tal cual — nota de cierre

**Acto:** `ACTO GEN2-PINS-REPRODUCE-1`, 16/sep/2026, NUBE (`cloud_default`; sin
`data/raw` montado — confirmado, no es PARO para este perímetro).
**Base observada al arrancar:** `origin/main = 9fd59d0` (merge de `PR #806`,
`ACTO GEN2-VIGENCIA-DEUDA-1`); `git rev-list --count HEAD..origin/main` = 0.
**Encargo archivado verbatim (0-bis A.3):**
`forense/encargos/2026-09-16-GEN2-PINS-REPRODUCE-1.md`. El texto llegó como
descripción de tarea de sesión, sin encargo previo commiteado en
`forense/encargos/` — defecto de origen, no de este acto; este acto lo
resuelve con su propio 0-bis antes de tocar nada sustantivo.

## Premisa verificada antes de ejecutar (A.7/A.8)

Las cuatro cifras del encargo se contrastaron contra el árbol vivo antes de
actuar (`python3 tools/corrida0.py status`, `python3 tools/relevo_usos.py`):

| cifra del encargo | estado | evidencia |
|---|---|---|
| "80 selladas" | **vigente** | `N_corridas_selladas=80` |
| "Contador: 207, 189 y 18" | **vigente al arrancar** | `N_resultados_activos=207`, `dependencias_numericas_legacy_activas=189`, `N_resultados_gen2_adoptados_activos=18` |
| "11 pins REPRODUCE" | **vencida** | Hoy `tools/relevo_usos.py` cuenta 15 `LISTADO-PARA-MESA` (9 `-REPRODUCE`, 2 bare de `CALC-EDER-0003`, 4 `-NO-REPRODUCE` nuevos — `RES-0039..0042` — que ni RELEVO-USOS-1 ni CAJA-SUCESORES-1 vieron, sellados después por `MEDICION-DEMANDA-2`) |
| "89 con oferta / 78 = 89−11 / 118 sin oferta" | **vencida, no reconstruible** | Cifra de `RELEVO-USOS-1` con 23/82 corridas selladas; hoy son 80/82 y las categorías vivas (ver P2/P3 abajo) no suman ni 89 ni 118 bajo ninguna combinación |

El "11 pins REPRODUCE" del encargo es, en realidad, el bloque de 9 que
`ACTO GEN2-CAJA-SUCESORES-1` ya pineó y dejó pendiente de adopción en
`NC-0243` (`forense/notas/2026-09-15-GEN2-CAJA-SUCESORES-1-cierre.md` P2).
Este acto ejecuta esa deuda — no la de "11" del encargo, que no corresponde
a nada abierto hoy.

## P1 · materializar el bloque REPRODUCE (`NC-0243`)

Perímetro: `milpa/tramite.yaml`, solo bin 1 (regla de bloque de
`RELEVO-USOS-1`, `forense/encargos/2026-09-15-GEN2-RELEVO-USOS-1-ADENDA-REGLA-ADOPCION-EN-BLOQUE.md`).
Ningún `spec.yaml` sellado se editó (E.3).

**6 de 9 citados, verificados y adoptados en bloque — sin firma individual**
(el merge de este PR es la adopción, E.2):

| slot | conducta | RESULT citado | delta vs GEN1 |
|---|---|---|---|
| RES-0036 | no_recibe_remesas | RESULT-ENIGH-A-P-COMPLEMENTO | −9.956e-08 |
| RES-0037 | tiene_afore | RESULT-ENFIH-A-P | +2.874e-07 |
| RES-0038 | no_tiene_afore | RESULT-ENFIH-A-P-COMPLEMENTO | −2.874e-07 |
| RES-0045 | share_horas_mujeres_40mas | RESULT-ENUT-A-R | −1.853e-05 |
| RES-0063 | razon_no_vacunacion_logistica | RESULT-ENSANUT-A-P-LOGISTICA | −3.591e-07 |
| RES-0064 | razon_no_vacunacion_no_logistica | RESULT-ENSANUT-A-P-NO-LOGISTICA | +3.591e-07 |

Cada valor se releyó directamente de
`data/corrida0/CALC-*/resultados.json` (no se confió solo en la tabla de la
nota de `CAJA-SUCESORES-1`) y coincide dígito a dígito con el `p` ya
materializado en `milpa/tramite.yaml`. `python3 tools/corrida0.py status`
corrido después de las seis citas: sin `PARO`, y:

```
dependencias_numericas_legacy_activas: 189 -> 183
N_resultados_gen2_adoptados_activos:    18 -> 24
```

`python3 tools/relevo_usos.py --escribe` (el escritor canónico de esta
vista — no tiene dependencia de corpus, es derivación por lectura, ver
"Entorno" abajo) re-escribió `data/corrida0/relevo-usos-v1_0.tsv`: las seis
filas pasan de `LISTADO-PARA-MESA-REPRODUCE` a `YA-ADOPTADO`,
`YA-ADOPTADO` global 16→22, sin tocar ninguna otra fila (diff aislado,
verificado línea por línea).

**3 de 9 (`RES-0050/0051/0052`, `participa_p0_minimo/maximo/media`,
`CALC-L8-CONVERSION-0001`) NO se pudieron citar — hallazgo nuevo, `NC-0253`.**
`corrida0.py status` **PARA** con `USO-NO-APTO`: el origen numérico de
`RESULT-L8CONV-A-P-*` resuelve a `INDETERMINADO` porque su único insumo
material (`data/l8-resultados-tipo-boleta-v1_0.json`) no está en el
whitelist mecánico de linaje (`INSUMOS_LEGACY_ARCHIVO` /
`INSUMOS_LEGACY_DIRECTORIO` / `FUENTES_NUEVAS_ACREDITADAS`,
`tools/corrida0.py:3313-3327`), y `milpa/src/linaje.py:59-60` niega aptitud
a **todo** uso `MEDICION-GEN2` con origen `INDETERMINADO`, sin excepción.
Confirmado que no es un efecto de este acto: el mismo `PARO` ocurre en el
árbol limpio, sin ninguna de mis ediciones (`git stash` de
`milpa/tramite.yaml` y reintento). Corregirlo exige o ampliar el whitelist
de linaje (juicio de auditoría: ¿el JSON de L8 cuenta como fuente legacy
acreditada?) o declarar `origen_numerico` explícito en el `spec.yaml`
sellado de `CALC-L8-CONVERSION-0001` (prohibido aquí por E.3) — ninguna de
las dos cabe en el perímetro de este acto (`milpa` citas, bin 1). Se
revirtieron las tres ediciones antes de escribir el registro derivado, para
que `corrida0.py status`/`relevo_usos.py --escribe` corrieran limpios.

**2 de 9 (`RES-0043/0044`, `CALC-EDER-0003`) NO son bin 1 — disposición de
mesa pendiente, `NC-0254`.** Confirmado, releyendo el `spec.yaml` sellado:
`RESULT-EDER-UNION-A-DELTA-VS-GEN1 = NO-APLICA-ESTIMANDO-DISTINTO` (GEN1
mide ENADID 2023, situación conyugal actual; esta corrida mide EDER 2017,
tipo de primera unión). `milpa/tramite.yaml` ya cita EDER2017 como eje de
**corroboración** (no de reemplazo), y las cuatro celdas por cohorte
coinciden dígito a dígito con lo ya citado. No hay nada que este acto pueda
adoptar aquí sin exceder bin 1; se presenta a mesa, se rotula, no se calla.

`NC-0243` se cierra **parcial** (6/9 resuelto, 2 sucesores nuevos por los
3+2 restantes). `tests/check.py --baseline` corrido después de las seis
citas: ver sección Suite abajo.

## P2 · por qué no corrió — `NC-0255`

El encargo pide clasificar "los otros 78 slots con oferta (89 menos 11)" en
bin 1/2/3. Verificado contra el árbol vivo: "89" es la cifra de
`RELEVO-USOS-1` con 23/82 corridas selladas (hoy 80/82). La re-derivación
de `tools/relevo_usos.py` sobre el árbol post-P1 da, de los 207 slots:

```
YA-ADOPTADO=22  LISTADO-PARA-MESA=9  CANDIDATO-GEN2=12
NO-ADOPTABLE-POR-VEREDICTO-SELLADO=8  CONFLICTO-ENTRE-CANALES=2
VETADO-POR-DECISION=1  SIN-CANDIDATO=153
```

Ninguna combinación de estas categorías reconstruye 89 ni 78. Clasificar
bin 1/2/3 sobre una cifra vencida arriesga adoptar o rechazar el slot
equivocado — exactamente lo que la regla de bloque existe para prevenir.
**No se ejecutó.** El análogo vivo más cercano a "slot con oferta sin pin
declarado todavía" son los 12 `CANDIDATO-GEN2`; el sucesor de `NC-0255` es
correr `corrida0 delta` / comparación explícita por slot sobre esos 12
antes de proponer bin.

## P3 · por qué no corrió — `NC-0256`

Mismo problema de premisa ("118 sin oferta" hoy son 153 `SIN-CANDIDATO`,
verificado) más un choque de alcance: `MEDICION-DEMANDA-3` **ya existe**
como nombre reservado por la ENMIENDA FECHADA de `GEN2-SPECS-DEMANDA-1`
(`forense/encargos/2026-09-15-GEN2-SPECS-DEMANDA-1.md`, líneas 94-116) para
un remanente mucho más chico (specs de `CORR-0004`, la sucesora ENADID de
`familia.union.libre`/`CORR-0013` vía `NC-0194` — abierta — y 4 celdas de
marco sin `B`). Ejecutar P3 tal cual redefiniría `MEDICION-DEMANDA-3` a un
universo ~40x mayor sin que mesa lo haya decidido así. **No se ejecutó** —
es `DECISIÓN-DE-MESA-PENDIENTE`, no un vacío de diagnóstico que este acto
pueda llenar por su cuenta.

## Contador

Antes → después de este acto (`python3 tools/corrida0.py status`):

```
N_resultados_activos:                  207 -> 207   (sin cambio; el encargo lo esperaba fijo)
dependencias_numericas_legacy_activas: 189 -> 183   (6, no los 11 que el encargo asumía)
N_resultados_gen2_adoptados_activos:    18 ->  24   (+6)
N_corridas_selladas:                    80 ->  80   (sin cambio; el encargo lo esperaba fijo)
```

Es el único acto que mueve estos tres a la vez, tal como el encargo declara
— con la corrección de que el movimiento real es 6, no "hasta 11" (3
quedaron bloqueados por `NC-0253`, ver arriba).

## Concurrencia — `F6-PANEL-CAJA-1`

El encargo declara "Concurrencia: F6-PANEL-CAJA-1 (caja, panel — sin
archivo común)". Verificado: `F6-PANEL-CAJA-1` no tiene PR abierto ni
cerrado (`search_pull_requests` sobre el repo, 0 resultados), y su único
rastro es la rama remota `acto/gen2-f6-panel-caja-1` (huérfana, sin fusión
posible verificada — `git merge-base --is-ancestor` contra `main` falla).
`ACTO GEN2-VIGENCIA-DEUDA-1` (ayer) ya la declaró muerta/sin proponer a
mesa. No hay ningún archivo en común con el perímetro de este acto
(`milpa/tramite.yaml`, `data/corrida0/relevo-usos-v1_0.tsv`,
`forense/no-corrido.tsv`, esta nota) — la cláusula de concurrencia del
encargo era boilerplate heredado, no un riesgo real, confirmado.

## Entorno

`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`; `data/raw` ausente
(esperado en NUBE). Este acto no abrió microdato ni red: los seis `RESULT`
citados se releyeron de `data/corrida0/CALC-*/resultados.json`, ya
sellados y commiteados: no requieren corpus.

**`corrida0.py registro --escribe` (las tres vistas `corridas.tsv` /
`resultados.tsv` / `usos.tsv`) NO se corrió.** Verificado con un dry-run:
`corrida0.py registro` (sin `--escribe`) proyecta un diff de 93/186 filas en
`corridas.tsv` y 4698/5239 en `resultados.tsv` **incluso sobre el árbol
limpio, sin ninguna edición de este acto** (confirmado con `git stash`) —
es deriva NUBE-vs-CAJA preexistente: sin `verify()` contra corpus real, el
comando degrada `fuente_replay` de `VERIFY-EN-ESTA-SESION` (dicho en la
última corrida con corpus montado) a `HEREDADO-DEL-REGISTRO-PUBLICADO`
(fallback fiel, pero más débil) en decenas de filas ajenas a este encargo.
Escribir esas tres vistas desde aquí degradaría procedencia ya verificada
en CAJA por un acto que no tiene nada que ver con `milpa/` — muy por fuera
del perímetro declarado ("milpa citas, solo bin 1"). `usos.tsv` sí muestra
el efecto aislado de las 6 citas nuevas (18→24 filas de diff sobre el
mismo baseline), confirmando que el único cambio real es el mío — pero
como el escritor no permite escribir una vista sin las otras dos, la
materialización de `usos.tsv`/`corridas.tsv`/`resultados.tsv` (a diferencia
de `relevo-usos-v1_0.tsv`, que sí se escribió) queda para un acto en CAJA.
No es una fila nueva de `NC` porque no cambia ningún contador del Contador
de este acto (los tres de arriba se leen de `status`, que no requiere
`--escribe`) — se deja dicho aquí y en el `## NO-CORRIDO / RESERVAS` del
encargo.

## Suite

`python3 tests/check.py --baseline` corrido después de las seis citas y de
la reescritura de `relevo-usos-v1_0.tsv` y `forense/no-corrido.tsv`:
resultado pegado en el commit de cascada (`## CONSUMIDO` del encargo cita
el mismo resultado crudo).
