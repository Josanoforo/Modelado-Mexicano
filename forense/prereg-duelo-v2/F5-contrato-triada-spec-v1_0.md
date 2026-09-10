# `F5-CONTRATO-TRIADA` — spec congelada de la comparación de tres — v1.0

**Acto:** `GEN2-F5-CONTRATO-TRIADA` (NUBE, Opus). Redactado contra
`origin/main = eab46ed` (merge de `PR #674`, `ACTO GEN2-F5-DUELO-CALC`),
10/sep/2026. **CONTADOR: cero** — este documento congela el contrato de
comparación; no calcula un solo error final, no toca microdato, no toca
captura. Es **spec sucesora**, no enmienda: `F5-duelo-contemporaneo-spec-v1_0.md`
(COMMIT-1 de `ACTO GEN2-F5-RECAPTURA-L`) queda intacta, sin una línea
editada. Esta spec la sucede en el orden de prioridad de preguntas
(§0), reutilizando sin reescribir todo lo que ya estaba sellado y sigue
siendo válido (universo de 224 capturas, `k=8`, bootstrap B-bis, banda
`δ=0.5`).

**Firma de mesa que redefine la pregunta primaria (verbatim, objeto
explícito, citada íntegra):** *"La afirmación central que este contrato
debe poder adjudicar es: en el mismo panel y contra el mismo árbitro,
cuál rinde mejor entre LLM solo, LLM con corpus y motor. TRANSFERENCIA
queda secundaria. R es árbitro, no contendiente. B es diagnóstico, no
contendiente. M no puede calibrarse contra los resultados del panel
después de congelar este contrato."* — y la instrucción de alcance que
la acompaña: *"Esta firma sustituye para el siguiente duelo la
prioridad anterior de TRANSFERENCIA como pregunta primaria. No
reescribe la spec histórica F5 v1.0; nace una spec sucesora."*

---

## 0 · Qué cambia respecto a `F5-duelo-contemporaneo-spec-v1_0.md`, y qué no

| | `F5 v1.0` (COMMIT-1 de `RECAPTURA-L`) | `F5-CONTRATO-TRIADA` (este documento) |
|---|---|---|
| Pregunta primaria | TRANSFERENCIA (corte temporal por celda, `L_SOLO` vs `L_CORPUS`) | **USO DOCUMENTAL / operacional**: `L_SOLO`, `L_CORPUS` y `M`, mismo panel, mismo árbitro `R` |
| Pregunta secundaria | Uso documental, paquete completo | Transferencia (§6), con el mismo corte temporal ya congelado |
| Contendientes | Dos (`L_SOLO`, `L_CORPUS`) | **Tres** (`L_SOLO`, `L_CORPUS`, `M`) |
| Rol de `R` | Árbitro | Árbitro (sin cambio — nunca contendiente) |
| Rol de `B` | No entra a la escala (§5 de `F5 v1.0`, `procedimiento-scoring-v1_2.md` §4: hoy sin fila para las 14 celdas) | Piso diagnóstico al final, explícitamente fuera de `U3`/ranking/adjudicación/veto (§7) |
| Unidad de la cantidad pareada | `z = (punto−R)/EE(R)`, adimensional | **Puntos porcentuales** (`error_X,i = |predicción_X,i − R_i|`, `MAE_X`, `Δ(A,B)`) — la firma de mesa fija "todo en puntos porcentuales" |
| Banda de indiferencia | `δ=0.5` en unidades `z` | `δ=0.5` **pp** — mismo valor numérico, unidad distinta; no es el mismo umbral reinterpretado, es una constante nueva fijada por esta firma "por continuidad" |
| Reglas de agregación por celda, `k=8` | Selladas | **Heredadas sin cambio** (§2) |
| Bootstrap pareado (semilla, réplicas, IC95) | Sellado | **Reutilizado sin alterar su significado** (§4) |
| Universo de 224 capturas | Sellado por `RECAPTURA-L` | El mismo — no se recaptura nada |
| Contaminación de `M` | No evaluada explícitamente contra `R` (M era secundario, sin veto) | **Regla explícita de exclusión** (§1): `M` no puede haberse calibrado contra el mismo `R` que lo evalúa |

Lo que **no** cambia: el universo de captura (224 invocaciones, 14 celdas ×
2 variantes × k=8), el paquete-corpus F5 congelado, el corte temporal por
celda de transferencia (ahora secundaria, §6), la prohibición de ampliar
`n` o re-elegir agregación después de ver resultado, y el principio de que
`INCONCLUSO`/`SIN-GANADOR-UNICO` son salidas válidas, no fracasos de
diseño.

---

## 1 · P1 · UNIVERSO — tres conjuntos, congelados en este commit

**Marco inicial:** `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv`, 14
celdas (verificado: 1 cabecera + 14 filas, columna `elegible_v1_1=SI` en
las 14).

### 1.1 · `U0` — las 14 celdas del marco

Fijo, sin condición. Lista completa (id · encuesta · ola):

```
CIV-M-01 · ENVIPE · 2012      CIV-M-02 · ENVIPE · 2013
CIV-M-04 · ENVIPE · 2015      CIV-M-10 · ENVIPE · 2021
CIV-M-12 · ENVIPE · 2023      CIV-M-13 · ENVIPE · 2024
DIN-M-01 · ENNViH/MxFLS · 2002 (ola 1)
FAM-M-01 · ENIF · 2018
FAM-M-05 · ENIGH · 2016       FAM-M-06 · ENIGH · 2018       FAM-M-07 · ENIGH · 2020
TRA-M-02 · ENCUCI · 2020      TRA-M-03 · ENCIG · 2013       TRA-M-07 · ENCIG · 2021
```

### 1.2 · `UR` — celdas con árbitro `R` válido, sellado, de identidad compatible

Derivado por censo directo de `data/corrida0/CALC-R-CIV-M-*/` contra las
14 celdas de `U0` (comando: `ls data/corrida0/ | grep CALC-R`, corrido en
esta sesión):

**`UR = {CIV-M-01, CIV-M-02, CIV-M-04, CIV-M-10, CIV-M-12, CIV-M-13}`, 6/14.**

Las 8 celdas restantes (`DIN-M-01`, `FAM-M-01/05/06/07`, `TRA-M-02/03/07`)
no tienen `CALC-R-*` en el árbol — **`NO-EXISTE`, no `AUSENTE`**: ningún
acto ha calculado su árbitro `R` todavía (el marco mismo las marca
`ola_calibracion=PENDIENTE-D-D` para el estimador correspondiente). Quedan
fuera de `UR` por ausencia de insumo, no por descarte de juicio. "Identidad
compatible" (la segunda condición de `UR`, además de "válido y sellado")
se verifica por el mismo criterio que `A-bis.4` de la spec `R-ENVIPE-SERIE-DBF`
ya declara: el `R` de cada una de las 6 celdas es el estimando **primario**
de su `CALC-R` (no el "secundario homologado" `U1`/`C1` de la misma
corrida — esos dos no se comparan entre sí y `U1` no es el árbitro de esta
tríada).

Sidecar de este censo, con la evidencia por celda: `universo-triada-v1_0.tsv`
(§9).

### 1.3 · `U3` — intersección de `UR` con punto válido de `L_SOLO`, `L_CORPUS` y `M`

**Regla, fijada aquí, antes de tener los tres insumos completos:**

```
U3 = { i ∈ UR : L_SOLO tiene punto válido en i
              ∧ L_CORPUS tiene punto válido en i
              ∧ M tiene punto válido en i
              ∧ i no está CONTAMINADA-POR-OBJETIVO }
```

Una celda **no** se elimina de `U3` porque su error resulte grande — el
filtro de arriba es la única puerta de entrada, y es sobre insumo
disponible/válido, nunca sobre el resultado del error.

**Punto válido de `L_SOLO`/`L_CORPUS`:** el agregado por celda (§2) existe
y proviene de réplicas cuyo `valor_extraido` salió de un extractor
**validado** contra el formato real de `corridas-L/*__v1_3.json`. A la
fecha de este commit **no existe ese extractor** — `tools/extrae_l_v1_1.py`
está declarado `NO-VALIDADO-PARA-FORMATO-REAL-DE-CORPUS` por `NC-0142`
(`ACTO GEN2-F5-DUELO-CALC`, `PR #674`: 0/96 capturas reales traen el
encabezado que busca, su *fallback* capturó cifras de contexto que el
propio modelo declaró explícitamente que no eran la estimación pedida).
Mientras `NC-0142` siga abierta, **ninguna celda tiene "punto válido" de
`L_SOLO`/`L_CORPUS` bajo esta regla** — no porque el dato no exista, sino
porque el único instrumento de lectura disponible está descalificado por
medición propia, no por sospecha.

**Punto válido de `M`:** un punto por celda, procedente del snapshot
sellado de `ACTO GEN2-ENCARGO-4/5` (aún no ejecutado al momento de este
commit — es sucesor declarado de este mismo contrato, §8). Antes de que
ese snapshot exista, ninguna celda tiene "punto válido" de `M` bajo esta
regla tampoco.

**Consecuencia, declarada sin rodeos:** `U3` **no se puede derivar en su
membresía final hoy** — dos de sus tres condiciones de entrada dependen de
insumos que este mismo contrato nombra como sucesores (extractor validado,
snapshot de `M`). Lo que **sí** se congela en este commit es la **regla**
de `U3` completa y ejecutable (arriba) más la parte que **sí** es
derivable hoy sin esos insumos: `U3 ⊆ UR` siempre, así que **ninguna de
las 8 celdas sin árbitro puede entrar a `U3` bajo ninguna circunstancia
futura** — esa parte de la membresía queda cerrada ya, con las 6 celdas de
`UR` como el techo (`|U3| ≤ 6`). Reserva declarada como `NC-0143`
(`forense/no-corrido.tsv`, `ABIERTA`, sucesor: quien resuelva `NC-0142` +
`ACTO GEN2-ENCARGO-4/5` + el ejecutor de P2 bajo este contrato) — ver
también `## NO-CORRIDO / RESERVAS` del encargo archivado: es la reserva
declarada, no un hueco silencioso.

### 1.4 · `CONTAMINADA-POR-OBJETIVO` — regla y verificación disponible hoy

**Regla:** una celda `i ∈ UR` queda `CONTAMINADA-POR-OBJETIVO` y fuera de
`U3` si la cadena de cálculo de `M` para esa celda consume, directa o
indirectamente, el mismo resultado `R` que se usa para evaluarla en esta
tríada. **Una calibración independiente no es contaminación automática**
— la prueba es la cadena documentada (qué objeto concreto, con qué id,
alimenta a cuál), no la coincidencia de encuesta o de variable.

**Verificación disponible hoy, sobre las 6 celdas de `UR` (censo
mecánico, no exhaustivo de todo el árbol pero sí de la ruta obvia de
contaminación — la calibración del propio motor):**

La regla de `M` que emite para las 6 celdas `CIV-M-*` es
`civico.denuncia.miedo_desconfianza` (`milpa/tramite.yaml:584`). Su
calibración (`p=0.294313`) procede de `payload_manifiesto_id:
envipe2025_csv` (ENVIPE **2025**, `milpa/tramite.yaml:493`) — la propia
regla trae una nota de no-comparabilidad verbatim
(`milpa/tramite.yaml:488`): *"p=0.294313 sale de la misma variable de la
misma encuesta pero NO es comparable: distinta unidad (delito vs
persona), ponderador (FAC_DEL vs FAC_ELE), denominador (todas las
víctimas vs solo no denunciantes), particiones cruzadas del numerador y
distinto estimador de IC (conglomerado vs simple)."* El árbitro `R` de
cada una de las 6 celdas (`CALC-R-CIV-M-01/02/04/10/12/13`) se computa,
en cambio, de la lectura directa de `Tmod_Vic.DBF` de **su propia ola**
(2012, 2013, 2015, 2021, 2023, 2024 respectivamente) — un archivo y una
ola que **nunca** es la ENVIPE 2025 que calibra a `M`.

**Hallazgo de este censo:** las 6 celdas de `UR` **no** muestran
contaminación por esta vía — objeto de calibración de `M` (ENVIPE 2025
CSV) y objeto de cómputo de `R` (DBF de la ola propia, 2012–2024) son
dos payloads distintos, y la propia regla del motor declara por escrito
que no son comparables. Esto **no** cierra la pregunta de contaminación
para siempre: es la verificación de la ruta obvia (calibración directa
del generador que emite en estas celdas), hecha con el insumo de `M`
disponible hoy (`corridas-M/` legacy) — el snapshot real que entrará a
`U3` es el de `ACTO GEN2-ENCARGO-4/5`, y esa verificación se repite
contra ESE snapshot antes de aceptar cada celda en `U3`, no se hereda de
este censo por default.

---

## 2 · P2 · PRODUCTO DE CADA CONTENDIENTE

**`L_SOLO` y `L_CORPUS`:** se conserva `k=8` (sin cambio, `RECAPTURA-L`).
La agregación por celda es la regla histórica ya sellada para F5 —
**mediana** de las réplicas con `valor_extraido` `EXTRAIBLE`
(`agregar_continua`/`agregar_categorica`, `pipeline-L-adv1-m2.py` §5, la
misma que `F5-duelo-contemporaneo-spec-v1_0.md` §5 ya cita y
`CALC-DUELO-0001` ya aplicó). **No se elige** promedio, mediana o mejor
réplica después de ver el resultado — la mediana ya estaba elegida antes
de este contrato y este contrato no la reabre.

**Cobertura de la primaria operacional:** una captura que el extractor
**validado** declare `NO-EXTRAIBLE` cuenta en cobertura — no se sustituye
por cero, no se descarta silenciosamente. (El extractor validado es, hoy,
un insumo pendiente — §1.3; esta regla gobierna su comportamiento en
cuanto exista, no retrocede a `tools/extrae_l_v1_1.py` sin validar.)

**`M`:** un punto por celda, procedente del snapshot sellado de `ACTO
GEN2-ENCARGO-4/5`. Este contrato no adopta ningún punto de `M` hoy — el
snapshot es insumo de un sucesor, no de este documento.

**`R`:** un punto árbitro por celda con su incertidumbre (`EE(R)`) y
diseño disponibles (`FAC_DEL`/`EST`/`UPM`, `codificacion-R-v1_0.tsv`). `R`
**nunca** entra al ranking — es la vara, no un contendiente.

---

## 3 · P3 · MÉTRICA PRIMARIA

Todo en **puntos porcentuales** (pp) — no en unidades `z` como
`F5 v1.0` §5. Por celda:

```
error_X,i = |predicción_X,i − R_i|        para X ∈ {L_SOLO, L_CORPUS, M}
```

`predicción_X,i` y `R_i` expresados en la misma escala (proporción ×100,
o el punto porcentual nativo del estimador de esa celda — la escala de
`R` gobierna, según `escala` de `marco-M-sorteado-v1_3.tsv`).

**Resumen primario por contendiente:**

```
MAE_X = media(error_X,i)     sobre el mismo U3, para X ∈ {L_SOLO, L_CORPUS, M}
```

**Comparaciones pareadas, las tres obligatorias, ninguna omitible:**

```
Δ(A,B) = media(error_A − error_B)     — negativo favorece A
```

1. `Δ(L_CORPUS, L_SOLO)`
2. `Δ(M, L_SOLO)`
3. `Δ(M, L_CORPUS)`

Cada `Δ` se computa sobre el mismo `U3` que las otras dos — nunca sobre
universos distintos por comparación (si eso ocurriera, sería síntoma de
que `U3` no está bien definido para las tres, y el cómputo se para, no se
improvisa un universo por par).

---

## 4 · P4 · INCERTIDUMBRE Y BANDA

**Bootstrap pareado, reutilizado sin alterar su significado** — mismo
aparato que `procedimiento-scoring-v1_2.md` (`generar_indices_bootstrap`,
`derivar_seed_scope`) y que `F5-duelo-contemporaneo-spec-v1_0.md` §5 ya
adaptó para la comparación de dos brazos:

- mismas celdas de `U3` en cada réplica (nunca un subconjunto distinto
  por comparación);
- **mismos índices de remuestreo para los tres contendientes** — una
  réplica de bootstrap remuestrea celdas, y las tres series
  (`error_LSOLO`, `error_LCORPUS`, `error_M`) se indexan con el mismo
  vector de índices en esa réplica, condición necesaria para que las tres
  comparaciones pareadas compartan la misma estructura de correlación
  intra-celda;
- **10,000 réplicas**;
- **semilla heredada**: `seed=42` (`FP-168`, la misma que `F5 v1.0` §5 y
  `procedimiento-scoring-v1_2.md` ya sellan — no se introduce una segunda
  semilla arbitraria para la tríada);
- **IC95**.

**Banda práctica, fijada antes del resultado: `δ = 0.5 pp`** — mismo
valor numérico que la banda `z` de `F5 v1.0`/B-bis, **por continuidad
declarada por la propia firma de mesa**, no porque las dos unidades sean
intercambiables (§0 lo marca explícitamente como constante nueva, no
reinterpretación).

**Escala pareada exhaustiva** (aplica a cada una de las tres
comparaciones de §3, independientemente):

| Condición sobre IC95 de `Δ(A,B)` | Veredicto |
|---|---|
| completamente `< −0.5 pp` | `A-GANA` |
| completamente `> +0.5 pp` | `B-GANA` |
| completamente dentro de `[−0.5, +0.5]` | `EMPATE-PRACTICO` |
| cualquier otro caso (el IC cruza al menos un límite de la banda) | `INCONCLUSO` |

**Escala global**, derivada de las tres pareadas:

| Condición | Veredicto |
|---|---|
| `X` gana sus dos comparaciones contra los otros dos contendientes **y** no tiene menor cobertura de celdas que ellos (§5) | `GANADOR-TRIADA-X` |
| Ningún contendiente satisface lo anterior | `SIN-GANADOR-UNICO` |
| Identidad, contaminación o cobertura rompe la comparación (p. ej. `U3` no es el mismo para las tres comparaciones, o una celda de `U3` resulta `CONTAMINADA-POR-OBJETIVO` tras auditar el snapshot real de `M`) | `NO-ADJUDICABLE-POR-CONTROL` |

**El ranking puntual de `MAE_X`** (§3) se reporta siempre, aun si la
escala global es `INCONCLUSO`/`SIN-GANADOR-UNICO`/`NO-ADJUDICABLE-POR-CONTROL`
— un ranking descriptivo no es una adjudicación con banda, y las dos
cosas se presentan por separado, nunca fusionadas en una sola cifra.

---

## 5 · P5 · COBERTURA

Se reporta sobre `U0` **y** `UR`, no solo sobre la intersección exitosa
`U3`. Por contendiente (`L_SOLO`, `L_CORPUS`, `M`):

- celdas elegibles (`|U0|=14`, `|UR|=6` — el techo de lo adjudicable);
- celdas con punto (post-extracción/post-snapshot, cuando esos insumos
  existan);
- réplicas `L` válidas (de las `k=8` por celda/variante, cuántas
  `EXTRAIBLE` bajo el extractor validado);
- abstenciones/no-extraíbles;
- contaminaciones (`CONTAMINADA-POR-OBJETIVO`, con su cadena citada);
- exclusiones y motivo (p. ej. las 8 celdas sin `R` — motivo:
  `NO-EXISTE-ARBITRO`, no un descarte de juicio).

**Prohibido proclamar ganador operacional usando únicamente `U3`** si el
supuesto ganador tiene peor cobertura (menos celdas con punto válido
sobre `UR`) que un rival — la condición de `GANADOR-TRIADA-X` en §4 ya lo
exige mecánicamente, y esta sección es donde se reporta la evidencia que
esa condición necesita para evaluarse.

---

## 6 · P6 · TRANSFERENCIA — secundaria, no primaria, no veto

Se conserva la pregunta de transferencia como secundaria (invertido
respecto a `F5 v1.0`, donde era la primaria — §0).

`L_CORPUS` mantiene los cortes temporales ya congelados por
`F5-duelo-contemporaneo-spec-v1_0.md` §2 (operacionalización del corte
por celda, calendario real de olas, paquete-corpus con exclusión por
documento — nada de eso se recalcula ni se reabre aquí).

**`M` entra a la secundaria en una celda solo si su información
disponible cumple un corte comparable** — es decir, si la calibración de
`M` para esa celda (`ola_calibracion` de `marco-M-sorteado-v1_3.tsv`) no
usa una ola posterior a la que la celda evalúa, bajo el mismo criterio
mecánico que `F5 v1.0` §2 usa para excluir documentos del paquete-corpus
(cita con año ≥ ola de la celda, o sin año determinable, excluye). Si no
cumple, la celda se marca `M-NO-COMPARABLE-EN-TRANSFERENCIA` para esa
lectura — no se fuerza un punto de `M` bajo un corte que no respeta.

**Ejemplo ya visible en el marco actual** (no una predicción, un hecho
citado): `FAM-M-05/06/07` (ENIGH 2016/2018/2020) calibran de
`ola_calibracion=ENIGH 2022` — posterior a las tres olas que evalúan —
así que, bajo esta regla, las tres quedarían
`M-NO-COMPARABLE-EN-TRANSFERENCIA` en cuanto entraran a la secundaria.
`TRA-M-03/07` (ENCIG 2013/2021) calibran de `ENCIG 2025`, mismo caso.
`CIV-M-*` (ENVIPE 2012–2024) calibran de `ENVIPE 2025`, mismo caso —
**las 6 celdas de `UR` quedarían `M-NO-COMPARABLE-EN-TRANSFERENCIA` bajo
la calibración de `M` disponible hoy**, dato que un sucesor que ejecute
la secundaria no puede pasar por alto ni resolver con el extractor de la
primaria.

**La transferencia no veta ni reemplaza la primaria operacional** (§3–4)
— es un reporte aparte, con su propia cobertura y sus propias
excepciones (`M-NO-COMPARABLE-EN-TRANSFERENCIA`), nunca una condición de
`GANADOR-TRIADA-X`.

---

## 7 · P7 · `B` — piso diagnóstico, fuera de la adjudicación

`B` puede aparecer al final de un reporte de esta tríada como piso
diagnóstico. Explícitamente **no** entra a:

- `U3` (§1);
- el ranking de tres (§3–4);
- la adjudicación (§4);
- la condición de `GANADOR-TRIADA-X` (§4);
- ningún veto sobre ninguna de las anteriores.

Precedente heredado: `procedimiento-scoring-v1_2.md` §4 ya declara que
`B` no tiene fila para ninguna de las 14 celdas hoy — esta regla no
depende de que eso cambie; aunque `B` llegara a tener fila para alguna
celda, el rol declarado aquí no cambia sin una firma de mesa nueva.

---

## 8 · Perímetro, sucesores y cierre

**Toca:** esta spec + `universo-triada-v1_0.tsv` (sidecar, §9) +
`forense/notas/` (nota de decisión) + `0-bis` + cascada.
**NO toca:** capturas (`corridas-L-M/`, `corridas-L/`), el extractor
(`tools/extrae_l_v1_1.py`), `M` (`corridas-M/`, `milpa/`), `R`
(`corridas-R/`, `CALC-R-*`), `milpa/` en general, ningún `CALC` histórico.
Todo lo anterior se **lee** (censo de §1.2/§1.4), nunca se escribe.

**CONTADOR: cero** — ningún `RESULT` nuevo, ningún error final calculado.
El merge de esta spec **es** la firma del contrato (cierre del encargo,
verbatim).

**Sucesores, en el orden que el propio encargo nombra:**
- `ENCARGO 3/5` y `ENCARGO 4/5` — el segundo produce el snapshot sellado
  de `M` que §1.3/§2 citan como insumo pendiente; el primero, según su
  propio objeto, puede ser el que resuelva `NC-0142` (extractor validado)
  o cualquier otro insumo que la mesa haya lanzado en paralelo.
- `ENCARGO 5/5` — presumible ejecutor de P2 (el cómputo real de `U3`,
  `MAE_X`, las tres `Δ(A,B)` y la escala de §4) una vez que el extractor
  validado y el snapshot de `M` existan; hasta entonces, `U3` permanece
  con la regla congelada pero la membresía sin cerrar (§1.3).
- Cualquier acto que reabra `NC-0142` (extractor de `valor_extraido`
  calibrado contra el formato real de `corridas-L/*__v1_3.json`) es
  prerrequisito de facto para que `U3` deje de estar vacío por ese lado.

**El primer resultado que produzca el procedimiento de este contrato,
una vez que sus insumos pendientes existan, es el que se reporta** —
mismo principio de cierre que `F5 v1.0` §9, heredado sin reescritura.
