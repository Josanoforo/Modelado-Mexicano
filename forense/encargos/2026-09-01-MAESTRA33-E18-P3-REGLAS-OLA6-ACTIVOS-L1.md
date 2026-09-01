**SHA de redacción:** `b827824` (base real de MAESTRA33-E18 tras refrescar contra `ce5e10d`)
**Entorno asignado:** Ubuntu (carga microdato — ver `data/raw`)
**Estado:** VIVO
**COMPUERTA:** ninguna
**Origen:** P3 de `forense/encargos/2026-09-01-MAESTRA33-E18-MAPEO-ACTIVOS.md`, sobre las EXISTE-SATISFACE de `forense/notas/2026-09-01-MAESTRA33-E18-P2-mapeo-tabla.md`

---

# LOTE REGLAS-OLA6-ACTIVOS-L1

Único lote que este acto abre — de las 23 reglas SI-ENTONCES de los 4
dominios ACTIVOS sin `p` medida (P1), `/mapea` (P2) devolvió **3**
`EXISTE-SATISFACE`, no las 4-12 que un lote de ≤4 reglas ×3 podría llenar.
Las otras 20 (`EXISTE-NO-SATISFACE`/`NO-ENCONTRADO`) van al registro del
curador (A5), no a un lote — ver P2, sección "Ruta". Este lote trae las
3 que sí calificaron, ordenadas por olas disponibles en corpus (todas
empatan en 6 olas o son de una sola ola con evidencia más débil — el
orden de abajo es de mayor a menor solidez de la candidata, no solo
conteo de olas).

⚠️ **Ninguna `p` se mide en este documento.** Es spec congelable para que
`/acto` (en Ubuntu, contra microdato real) la ejecute. Los nombres de
ponderador/diseño muestral de abajo son los **estándar declarados por el
propio instrumento** (INEGI, documentación técnica pública) — no
confirmados contra el microdato real en este acto (`data/raw` ausente en
esta sesión, NUBE, ver ARRANQUE de `/acto`): quedan marcados
**PENDIENTE-VERIFICACIÓN-EN-ACTO-SUCESOR**, y el acto que ejecute este
lote los confirma con `head -1`/lector real antes de calcular nada.

---

## Regla 1 · `familia.seguro.volatilidad_ausencia_estado`

- **Modelo (§3.5):** SI ingreso volátil / ausencia de Estado (`segsoc`=2
  ∨ `residencia` ∈ {EUA, Otro país} ∨ hogar con remesas P041) ENTONCES la
  familia opera como seguro (corresidencia, pooling, **remesas**) —
  PORQUE G5 — `[FUERTE]`.
- **Candidata (P2):** variable `remesas`, tabla `concentradohogar` de
  ENIGH — **6 olas**: `enigh2012` (`v1_2:105963`), `enigh2014`
  (`v1_2:106914`), `enigh2016` (`v1_2:107955`), `enigh2018`
  (`v1_2:109041`), `enigh2020` (`v1_2:110230`), `enigh2022`
  (`v1_2:111486`) — todas `INSPECT_ZIP`, `en_corpus=SI`.
- **Variable:** `remesas` (ingreso corriente monetario del hogar por
  remesas, columna de `concentradohogar.csv`).
- **Dicotomización:** `recibe_remesas` = 1 si `remesas` > 0, 0 si
  `remesas` = 0 (o vacío/NA tratado como 0, a confirmar con el
  diccionario de datos de cada ola — puede variar 2012→2022).
- **Universo:** hogares (unidad de observación = hogar, no persona) de
  cada ola de ENIGH — Nueva Serie desde 2016 (`_ns`); 2012/2014 en su
  serie propia. Universo completo del hogar, sin filtro adicional
  declarado por la regla.
- **Ponderador:** `factor` (factor de expansión de hogar, estándar
  ENIGH) — **PENDIENTE-VERIFICACIÓN-EN-ACTO-SUCESOR** contra
  `head -1 concentradohogar.csv` de cada ola.
- **Diseño:** muestreo complejo, diseño probabilístico polietápico
  estratificado y por conglomerados (ENIGH) — requiere variables de
  diseño (`est_dis`, `upm`) para IC correcto; **PENDIENTE-VERIFICACIÓN**
  su presencia en cada payload.
- **Escala:** binaria (`recibe_remesas` 0/1) sobre `p` = proporción de
  hogares con remesas > 0, ponderada.

## Regla 2 · `dinero.planeacion.formal_estable`

- **Modelo (§3.1):** SI hay empleo formal e ingreso estable (`segsoc`=1
  ∧ `contrato` ∧ `pres_8`) ENTONCES planeación larga: **afore**, seguro,
  hipoteca — PORQUE el ingreso estable baja el costo esperado de
  comprometerse a un instrumento de horizonte largo — `[FUERTE]`.
- **Candidata (P2):** ENFIH2019, tabla `TCONCENTRADORA.csv`, variables
  `C_AFORE`/`V_AFORE` (`v1_2:98915`, `v1_2:98966`); espejo en
  ENGASTO2012/2013, variable `sar_afore` (`v1_2:99866`,
  `v1_2:100243`; texto legible en capa `-ext`: `ext:30864`/`ext:30906`,
  *"Prestación SAR o AFORE"*).
- **Variable:** `V_AFORE` (ENFIH2019, indicador de tenencia de cuenta
  AFORE) como principal; `sar_afore` (ENGASTO) como candidata
  complementaria de otra ola.
- **Dicotomización:** `tiene_afore` = 1/0 directo de `V_AFORE` (a
  confirmar codificación exacta — típicamente 1=Sí/2=No en INEGI, no
  0/1 crudo).
- **Universo:** ENFIH2019 — personas 18+ (marco estándar de la Encuesta
  Nacional de Financiamiento de Hogares/Inclusión Financiera, INEGI-CNBV);
  **PENDIENTE-VERIFICACIÓN** el filtro exacto por edad/PEA en el
  diccionario.
- **Ponderador:** `FACTOR`/`FAC_PER` — **PENDIENTE-VERIFICACIÓN-EN-ACTO-SUCESOR**
  (nombre exacto de columna en `TCONCENTRADORA.csv`).
- **Diseño:** muestreo complejo estratificado/conglomerado, estándar
  INEGI — variables de diseño **PENDIENTE-VERIFICACIÓN**.
- **Escala:** binaria (`tiene_afore` 0/1), `p` = proporción ponderada.
- **Nota de falsador (heredada del modelo):** el `ENTONCES` completo
  también nombra "seguro, hipoteca" — este lote solo congela AFORE
  (candidata con `EXISTE-SATISFACE` confirmado); seguro/hipoteca quedan
  fuera de este lote, no se inventa candidata para ellos.

## Regla 3 · `civico.participacion.contingente`

- **Modelo (§3.7):** SI el votante percibe que el acto **pesa**
  (resultado abierto y consecuencia palpable) ENTONCES participa; SI lo
  percibe decidido de antemano o sin consecuencia ENTONCES se abstiene —
  PORQUE cálculo del peso del acto — `[FUERTE]` **(a)**.
- **Candidata (P2):** ENCUP2012 (Encuesta Nacional sobre Cultura Política
  y Prácticas Ciudadanas), ítems de participación/intención electoral —
  111 candidatas en la formulación literal, **una sola ola** en el
  universo examinado por esta corrida (`encup2012`).
- **Variable:** a identificar entre las candidatas de la formulación
  literal (`--palabra "voto" --palabra "participacion electoral"`,
  `v1_2` tabla `BaseDatos_ENCUP_2012_Final`) — este lote **no** fija un
  único `variable_id` porque P2 no aisló todavía la pregunta específica
  de "peso percibido del acto" frente a las ~111 preguntas generales de
  cultura política de ENCUP; el acto sucesor decide entre las
  candidatas listadas en el log de P2 antes de congelar.
- **Dicotomización, universo, ponderador, diseño, escala:**
  **PENDIENTE-DE-MESA** — no se congela sin fijar primero el
  `variable_id` exacto (regla de la casa: no se inventa una spec sobre
  una variable todavía no elegida). Esta fila del lote es la más débil
  de las 3 y se declara así, no se disimula.

---

## LO QUE NO HACE este lote

No mide `p`. No carga microdato. No abre `milpa/procedencia.yaml`. Las
3 specs de arriba son congelables **para AFORE y remesas** (variable
identificada, dicotomización propuesta); la de `civico.participacion.contingente`
queda con el `variable_id` sin fijar — el acto sucesor la completa o la
regresa a `EXISTE-NO-SATISFACE` si ninguna candidata del log resulta
suficiente al leerla completa.

## CONSUMIDO

`ACTO MAESTRA33-E18-P3 · REGLAS-ACTIVOS-L1`, 1/sep/2026, CAJA Ubuntu, rama
`acto/maestra33-e18-p3-reglas-ola6-activos-l1`. Régimen de dos commits por
regla (precedente `MAESTRA33-C4`/`PR #424`). `ADR-273` (candidato; renumerado
dos veces — el derivado al arrancar era `ADR-271`, que tomó `PR #445`/`S2`, y
`PR #446`/`MAESTRA33-E21` tomó el `272`).

**Nombre del lote.** Este archivo conserva `REGLAS-OLA6-ACTIVOS-L1` porque A.3
no edita un verbatim. Dirección lo corrigió en el Mensaje 2 del encargo
`MAESTRA33-S2`: los lotes de P3 se nombran **`REGLAS-ACTIVOS-L<n>`**, son
reglas nuevas **dentro de los 4 dominios ya activos** y **no** apertura de
Ola 6 (`MAESTRA33-E14`/`ADR-265` vigente). La aclaración quedó, verbatim, en la cabecera
del bloque del lote dentro del YAML.

**Este es el «PR de EJECUCIÓN» que `S2` declaró faltante.** `S2` (`PR #445`)
corrió con `P1` **SIN INSUMO** porque lo único fusionado era el lote
*redactado* por `PR #443`, sin ninguna `p` medida: *"la compuerta se cumplió
por letra, no por sustancia"*. Aquí está la sustancia. Falta todavía la
condición (b) de su relanzamiento — **firma de mesa por regla**, fuera de
corchetes —, que un ejecutor no puede darse: por eso las dos entradas van
`situacion: PENDIENTE-DE-MESA`.

**2 de las 3 reglas medidas, 1 devuelta.** Los `PENDIENTE-VERIFICACIÓN-EN-
ACTO-SUCESOR` que este encargo mandó confirmar "antes de calcular nada" se
confirmaron, y **tres de sus supuestos resultaron falsos**: el ponderador de
ENIGH es `factor_hog` en 2012/2014 (no `factor`); la tenencia de AFORE es
`C_AFORE` 0/1 crudo (no `V_AFORE`, que el FD define como el **monto en
pesos**); el universo de `TCONCENTRADORA` es de **hogares** (no de
"personas 18+"). Las tres salen del descriptor oficial y del `head -1` que
este encargo pidió, no del juicio del ejecutor.

- `familia.seguro.volatilidad_ausencia_estado` — `p`=**0.045694**,
  IC95 [0.043754, 0.047711], `n`=90 102 (ENIGH 2022), **más la serie completa
  de las 6 olas**. Primera regla del programa con `p` en seis olas de la misma
  encuesta.
- `dinero.planeacion.formal_estable` — `p`=**0.538502**,
  IC95 [0.526700, 0.550616], `n`=17 765 (ENFIH 2019).
- `civico.participacion.contingente` — **`EXISTE-NO-SATISFACE`**, la salida
  que este mismo encargo previó. Su disparador es una **conjunción** y ENCUP
  2012 no trae la mitad `resultado abierto` (0 reactivos útiles en 282
  columnas leídas una por una, control positivo 239); y el falsador que el
  modelo ya declaró es un **diseño comparativo** que un corte transversal de
  un año no puede producir.

IC95 por **bootstrap de conglomerado estratificado** (UPMs dentro de estrato,
10 000 réplicas, `seed=42`), no el simple por fila de la fase 1: las dos
fuentes sí traen diseño y se verificó presente antes de calcular.

Entradas en `milpa/tramite-ola5-propuesta-v0.yaml` (acumulador único, donde
`S2` declara que las buscará), 8 reglas sin `id` duplicado. `milpa/tramite.yaml`
intocado; `ADR-68(a)` vigente.

Detalle: `forense/notas/2026-09-01-MAESTRA33-E18-P3-L1-spec.md`.
Medidores: `tools/tasas_base_ola6_activos.py`,
`tools/censo_encup_participacion.py`.
