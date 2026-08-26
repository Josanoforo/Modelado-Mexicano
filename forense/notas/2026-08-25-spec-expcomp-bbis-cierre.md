# `SPEC-EXPCOMP-BBIS` — la pieza faltante hacia llaves 5/5
### Nota de cierre · 25 de agosto de 2026 · entorno NUBE (`cloud_default`) · `ADR-193`

> | | |
> |---|---|
> | **ENCARGO** | `forense/encargos/2026-08-25-SPEC-EXPCOMP-BBIS.md` (archivado en este mismo acto, `A.3`) |
> | **QUÉ PRODUJO** | `forense/spec-bbis-exp-compartamos-v1_0-PROPUESTA.md` — la spec B-bis que `forense/registro-llaves-identificacion-v1_0.md:64` declaró faltante para ejercer `EXP-COMPARTAMOS-1` |
> | **CONTADOR** | **Cero, declarado.** Llaves ejercidas: `4` de `5`, sin movimiento — la spec habilita el ejercicio futuro, no lo es |
> | **PERÍMETRO** | La spec nueva · `forense/firmas-pendientes.tsv` (una fila, `FP-160`) · `canon/gobernanza-v1_15.md` (`ADR-193`) · `canon/estado-programa-v1_10.md` · esta nota · el encargo. **No se tocó `milpa/`, no se abrió microdato, no se ejerció la llave** |

---

## 0 · Arranque

**1 · REPO.** Clon existente, rama `claude/spec-bbis-compartamos-1-c40kb9`. `git log -1` al arrancar: `ba0a7e4` (Merge PR #362, `ACTO ATERRIZA-GEMELO`), working tree limpio.

**2 · SHA.** El SHA de redacción del encargo (`ba0a7e4`) coincide exacto con `HEAD` al arrancar — sin avance que refrescar, sin discrepancia que reportar.

**3 · `data/raw`.** No se tocó — este acto tiene prohibido abrir microdato, y ni siquiera se verificó su presencia (irrelevante para el perímetro).

**4 · ENTORNO.** `cloud_default`, sin red de datos exigida por el acto (ninguna sonda a fuentes externas: los insumos permitidos son todos internos al repo). Cero fetches.

**5 · ESPEJO.** Cero cifras del espejo en toda la redacción — verificado por lectura del propio texto de la spec antes de cerrar: ningún número del microdato aparece.

---

## 1 · Existencia, re-derivada contra `ba0a7e4` antes de escribir

```
$ find forense -iname "*bbis*compartamos*"
(vacío)
```

**Cero.** Ninguna spec B-bis de esta llave existía al arrancar — coincide con lo que la propia fila `:64` declara (*"NINGUNO — la llave nace sin pre-registro"*) y con lo que §10 del registro (`:252`) fija como faltante. El acto no encontró una spec ya escrita, así que no PARA por `A.8`.

La necesidad de `FP-147` se verificó en `data/curacion-registro/necesidad-objeto-modelo.tsv`, fila `N34`: reclama `EXP-COMPARTAMOS-1` para `dinero.credito.baja_friccion_usura_dano_downstream`, con la cláusula literal de la opción **b** de mesa (*"no reutiliza `confianza_institucional` ni `radio_confianza`"*). El molde metodológico, `forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md`, está `SELLADA` desde `FP-128` — usado como referencia de forma (objetivo/estimando/escala/límites), no de contenido.

---

## 2 · Lo que la spec declara — resumen, detalle en el propio archivo

**Objetivo (§1).** Adopta verbatim la necesidad de `N34`/`FP-147`. Al derivar el mapeo de esa necesidad contra los siete generadores de `canon/modelo-decision-v4_0.md` §2.1, **no aparece ninguno que la reclame sin ambigüedad**: `dinero.credito.baja_friccion_usura_dano_downstream` es una regla de motor con tier propio (`[MEDIA](a)`), no uno de `G1`-`G6`, y no tiene hoy fila en `milpa/procedencia.yaml` (verificado, `grep` → 0). **Este es el hallazgo que el encargo anticipaba como posible** y este acto lo declara, sin resolverlo por invención: mesa decide, al sellar, si el número futuro compite por el sitio del `[MEDIA](a)` vigente o entra como fila nueva de la octava clase.

**Estimando (§2).** ITT por conglomerado, EE agrupados por unidad de aleatorización — la misma mecánica que las 60 regresiones de `Compartamos-AEJ-tables-2-8.do`. Universo declarado (ola de seguimiento, N=16,560) y las dos reservas nombradas con sus cifras del censo (`in_admin` 12.37%, atrición 37.43%).

**Escala del veredicto (§3), fijada antes del dato.** pp de la variable de desenlace, ITT por conglomerado. Octava clase de procedencia (`cita`+`llave_id` obligatorios, sin llave pendiente — ya sellada por `FP-144`). El número no sustituye ningún `ASIGNADO` sin acto propio de mesa.

**Escala B-bis completa (§4).** corrobora / acota / rompe / inejecutable / no-refuta, con precedencia `rompe → inejecutable → acota → corrobora → no-refuta` declarada al sellar — la fila del no-refuta se nombra ahora, corrigiendo hacia adelante el defecto que `R5.1-D2` dejó documentado (fijar la escala después de correr, no antes).

**Límites (§5).** Transversal en seguimiento, sin identificador de persona (1,823/16,560 en las dos olas), un solo experimento/estado/producto, no informa el `[MEDIA]` de `dinero.credito.scoring_alternativo`, no reabre la pregunta de los reactivos de confianza — cerrada por `FP-132`.

---

## 3 · Tablero, gobernanza y estado

**Tablero.** Fila nueva `FP-160`, `ABIERTA` — "mesa sella la spec B-bis de `EXP-COMPARTAMOS-1`" — citando la spec en `dónde` (`A.12`; marcador `PROPUESTA` de la cabecera cubierto ante `T22`, mismo patrón que `FP-128` usó para `hitoD-R10_1-spec-v2_0-PROPUESTA.md`).

**Gobernanza.** `ADR-193`, candidateado contra el máximo re-derivado (`191` sin huecos → verificado `192` tras `ADR-192`) → `193`, sin colisión al fusionar (verificado: `origin/main` sin avance nuevo desde el arranque de este acto).

**Estado.** `canon/estado-programa-v1_10.md`: conteo de ADR `192→193`; línea de llaves gana la anotación *"4 de 5 · spec B-bis de la 5ª en mesa"*, con el numerador sin movimiento.

**Suite.** `python3 tests/check.py --baseline` — nunca `--freeze`. Antes de escribir, la base ya estaba VERDE (`19 FAIL · 129 WARN`). El marcador `PROPUESTA` de la spec nueva disparó `T22` hasta que `FP-160` la citó en `dónde`; `T15`/`T16` dispararon mientras `gobernanza`/`estado` no reflejaban el ADR nuevo — las tres se corrigieron dentro del acto (cabecera de conteo, cascada del ADR, línea de suite). Cierre: **19 FAIL · 130 WARN, LÍNEA BASE VERDE**. Neto +1 WARN, por `FP-160` naciendo `ABIERTA` (`T22`(a)) — mismo patrón que cada fila de tablero nueva.

---

## 4 · Lo que este acto NO hizo

- **No abrió el microdato.** Cero archivos de `116334-V1.zip` tocados — ni siquiera para verificar su presencia en disco.
- **No ejerció la llave `EXP-COMPARTAMOS-1`.** Sigue `SELLADA_NO_EJERCIDA`; el numerador de llaves ejercidas sigue en `4` de `5`.
- **No tocó `milpa/`.** El conducto (`FP-144`, octava clase) ya existía y no se modificó.
- **No fijó ningún número.** Cero cifras del espejo en la spec.
- **No adjudicó** la disyuntiva de §1 (destino del número futuro) ni ninguna otra pregunta de mesa — las deja escritas para la firma de `FP-160`.
- **No re-congeló** `tests/baseline.json`.

**Encargo `SPEC-EXPCOMP-BBIS` → `CONSUMIDO`.**
