# ARBITRO-MARGINALES-2 · ENNViH · spec v1.0

ACTO GEN2-ARBITRO-MARGINALES-2, P2 (pieza ENNViH). Formaliza en GEN2 la única
regla de `milpa/tramite-ola5-propuesta-v0.yaml` que P1 clasificó `RE-MEDIDA
(nueva)` para esta encuesta: `dinero.ahorro.tiene_ahorros`. No hay CALC GEN2
previo (`CALC-TANDAS-ENNVIH-0001`/`-PANEL-0001` miden tandas de ahorro
rotativo, tema distinto).

## 0 · Premisas verificadas

- `[EJECUTADO]` los tres payloads COINCIDEN: `ennvih2_2005_hogar_dta`
  (`data/raw/ennvih/ehh05dta_all.zip`), `ennvih3_2009_hogar_dta`
  (`.../ehh09dta_all.zip`), `ennvih2_2005_ponderador_transversal`
  (`.../ehh05w_all.zip`) — sha256 verificados contra `data/manifiesto.yaml`.
- `[LEÍDO]` `forense/notas/2026-08-24-cal-g3-puntual-cierre.md` (PASO 0):
  ENNViH **no tiene diseño muestral publicado** (`data/diseno-muestral.yaml:412-439`,
  `estado: SIN_DISEÑO_PUBLICADO`) — cero columnas de UPM/estrato en los 425
  `.dta` de las tres olas. No hay bootstrap de conglomerado posible; esto no es
  un defecto de esta pieza, es un hecho ya establecido del instrumento.

## 1 · Universo (idéntico en construcción al de CAL-G3-PUNTUAL, ver nota; el n
difiere del de esa pieza porque mide un desenlace distinto y esta regla lo
declara explícitamente en el propio YAML)

- Módulo `PR` (`iiib_pr.dta`, ambas olas): `pr02` = horizonte temporal
  (1-7 sustantivo; 8/98 excluidos).
- Módulo `CR` (`iiib_cr.dta`, ambas olas): `cr27` = tiene ahorros (1=Sí, 3=No;
  cualquier otro código o NaN excluido).
- **Enlace intra-persona**: `pid_link` de ola 3 intercala un código de 2 letras
  en las posiciones [6:8) (ronda `AP`/`BP`/`CP`/`CH`); las filas de ronda `C`
  (`CP`+`CH`, nuevo entrante 2009) se excluyen ANTES de emparejar. El resto se
  despoja del código (`pid[:6] + pid[8:]`) para obtener la llave compartida
  con ola 2.
- **Universo analítico** (`pr02` y `cr27` válidos en ambas olas): **n=6 356**
  — reproduce EXACTO el `n_pre_peso` que el propio YAML declara.
- **Ponderador**: `fac_3b` (ola 2, `ehh05w_all/ehh05w_b3b.dta`, join por
  `folio`+`ls` de ola 2). **Hallazgo propio de esta pieza**: la tabla de
  ponderador tiene 1 928 pares `(folio,ls)` duplicados, de los cuales 584
  grupos traen valores de `fac_3b` genuinamente distintos entre sí — un
  defecto de la fuente, no de este medidor (declarado, no corregido a mano).
  Se resuelve determinísticamente tomando la PRIMERA fila por `(folio,ls)`
  tras leer el `.dta` en su orden nativo (elección declarada; con la fila de
  mayor `fac_3b` el resultado no cambia para las claves que este universo
  toca — verificado).
- Con ponderador válido (`fac_3b` finito y > 0): **n=5 855**.

## 2 · Estimando

Tasa base ponderada de `cr27_ola2 == 1` (tiene ahorros) sobre el universo de
arriba, ponderador `fac_3b`. Intervalo: bootstrap por PERSONA con reemplazo
(no hay clúster de diseño — Plan B de `CAL-G3-PUNTUAL` PASO 1, aplicado aquí a
una tasa base en vez de a un β de primeras diferencias), 10 000 réplicas,
seed 42, percentiles 2.5/97.5. Rotulado `IC-INFORMAL-SIN-DISENO-PUBLICADO`.

## 3 · Oro y tolerancia

GEN1 (`dinero.ahorro.tiene_ahorros`): p=0.174804 [0.15925, 0.190543],
n_pre_peso=6 356, n_con_ponderador=6 028. El propio YAML declara que este
n_con_ponderador **ya difiere** de los 6 305 de `CAL-G3-PUNTUAL` y remite a
"hallazgo de reconciliación… nota A.13" sin resolverlo — la pieza hereda una
ambigüedad de origen, no la inventa.

`REPRODUCE` exige delta de punto < 1e-3 absoluto **y** n idéntico (mismo
criterio que `CALC-ENCUCI-0001` aplicó a `tramite.mordida.discrecional`);
`NO-REPRODUCE` si el n no coincide exacto, aunque el punto esté cerca — un n
distinto significa que el denominador no es el mismo conjunto de personas, y
eso no se declara "reproducido" aunque el resultado numérico case por
casualidad.

## 4 · No hace

No toca `milpa/`. No adopta. No re-mide el CALC de tandas.
