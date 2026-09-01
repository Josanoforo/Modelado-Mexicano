# `REGLAMENTO-SORTEO-MARCO-M` · regla 3 con implementación exacta — SELLADO, 1/sep/2026

**Estado: SELLADO, 1/sep/2026 (`ADR-262`, `FP-216`).** Copia sellada de
`forense/prereg-duelo-v2/reglamento-sorteo-v1_1-PROPUESTA.md`, byte a byte
en el cuerpo (§0-§6 abajo son copia literal, sin ningún cambio de contenido
— solo esta cabecera es nueva). `sha256` de la PROPUESTA verificado al
sellar (`sha256sum reglamento-sorteo-v1_1-PROPUESTA.md`):
`ee97ab79c4b4f7973b44a428791987523d4de9a8efc833a223345f343138b828` — ver
`reglamento-sorteo-v1_1.sha256` adjunto (hash del propio archivo sellado,
mismo patrón que `L-spec-v1_1.sha256`). La PROPUESTA **no se borra ni se
edita**: sigue íntegra en su ruta original, registro de lo redactado antes
de la firma (A.10).

**Firma de mesa (verbatim, 1/sep/2026):** «[sello reglamento sorteo v1.1]»
— responde las cuatro preguntas de §5 (abajo) así. **(1)** SÍ, esta
implementación exacta — piso 1 por estrato no vacío + Hamilton sobre el
resto, con el efecto general que §3 documenta (cambia resultados más allá
de los casos límite) — es la que se sella; la alternativa "quirúrgica" que
§5 punto 1 menciona no se escribió en este documento y no es lo que este
sello adopta. **(2)** NO reabre `v1_1` — confirma, no reinterpreta, lo que
`FP-213`/opción A ya resolvió (`B″` se acepta tal cual). **(3)** La segunda
cláusula de la regla 3 (`n_sorteo < n_estratos_no_vacios`, §2.2) **sigue
sin implementar** — este sello no la resuelve ni la necesita resuelta:
`sorteo_v3.asignar_asientos_proporcional_v3` sigue lanzando
`NotImplementedError` explícito si se presenta, tal como la PROPUESTA lo
declaraba; ningún sorteo del marco-M la ha necesitado hasta hoy (`v1_0`: 1
estrato; `v1_1`: 2 estratos, `n_sorteo=11`) — queda `PENDIENTE-DE-MESA`
para cuando un acto futuro la necesite, exactamente como la PROPUESTA ya
lo declaraba. **(4)** Número: `ADR-262` / `FP-216` (este acto, `ACTO
MAESTRA33-E12 · SELLA-1`), mismo patrón que `ADR-178`/`FP-150` selló el
reglamento original. Firmar esto **no ejecuta nada**: ningún sorteo corre
ni se re-corre por este sello; `sorteo_v3.py`, `sorteo_marco_m.py`,
`sorteo_marco_m_v1_1.py` y `sorteo-act-pil-3-v2-PROPUESTA.md`/`ADR-178`
siguen sin tocarse.

---

## 0 · Perímetro y qué NO hace este documento

Cubre **sólo** la regla 3 (piso 1 por estrato no vacío) del sorteo del
**marco-M** (`v1_0`/`v1_1`/sucesores) — no reabre ni redefine las reglas
1, 2, 4 y 5 de `sorteo-act-pil-3-v2-PROPUESTA.md` §2, que este documento
**hereda tal cual** para el marco-M (ver §1). No edita
`sorteo-act-pil-3-v2-PROPUESTA.md` ni `ADR-178` — ese documento sigue
gobernando `ACT-PIL-3` exactamente como está sellado; este es un
reglamento **sucesor**, específico del marco-M, no una enmienda del
original. No re-sortea `v1_1` (`FP-213`, opción A: se acepta tal cual). No
sella nada — sellar es de mesa.

## 1 · Por qué el marco-M necesita su propio reglamento

`ACT-PIL-3` (`ADR-178`) y el marco-M (`v1_0`/`v1_1`) **comparten mecanismo**
por precedente explícito (`sorteo_marco_m.py`/`sorteo_marco_m_v1_1.py`
citan `ADR-178` como precedente para reutilizar `sorteo_v2.sortear` /
`asignar_asientos_proporcional` sin reimplementar), pero el marco-M nunca
tuvo su **propio** reglamento sellado — corrió sobre la letra de
`sorteo-act-pil-3-v2-PROPUESTA.md`, un documento redactado para el universo
de 50 filas de `ACT-PIL-3` (§0-§1 de ese documento), no para el marco-M.
Esa herencia informal es exactamente donde vivía la brecha que `FP-213`
encontró: la regla 3, tal como `ACT-PIL-3`/B′ la ejercitaron, nunca había
topado un estrato de 1 fila con cuota exacta ≤0.5 empatada — `B″`/v1_1 fue
la primera corrida (de cualquiera de los dos linajes) en topar ese caso
límite (`sorteo-marco-M-resultados-v1_1.md`: *"primera vez que el mecanismo
común… ejercita este caso límite"*). Este documento formaliza, para el
marco-M específicamente, qué significa la regla 3 en código — no cambia
nada de lo que `ACT-PIL-3` ya sorteó ni de cómo `sorteo_v2.py` sigue
sellado para ese linaje.

**Reglas heredadas sin cambio** (`sorteo-act-pil-3-v2-PROPUESTA.md` §2,
citadas por referencia, no retranscritas): regla 1 (`|resultado| ==
n_sorteo`), regla 2 (`count(publicada=SI) <= cuota_max`), regla 4 (sin
reposición), regla 5 (determinismo). El marco-M además antepone su propia
regla de tamaño (`N<15` → identidad, `15<=N<30` → `ceil(N/2)`, `N>=30` →
`15`; `forense/notas/2026-08-31-marco-M-spec.md` §e, `sorteo_marco_m.
regla_de_tamano`, no tocada por este documento) — ninguna de las dos
reglas de tamaño ni de infactibilidad (§2.3 original) cambian aquí.

## 2 · Regla 3 — texto y letra completa

**Texto** (idéntico al original, `sorteo-act-pil-3-v2-PROPUESTA.md` §2,
regla dura #3 — no se re-redacta la prosa, se precisa su mecanismo):

> Todo estrato con al menos una fila en `marco` recibe **al menos una**
> fila en `resultado` si `n_sorteo ≥ n_estratos_no_vacios` (asignación
> proporcional con piso 1, resto por remanente más grande — método de
> Hamilton/mayor resto); si `n_sorteo < n_estratos_no_vacios`, se sortea
> sin reposición **cuáles** estratos entran, y se declara qué estratos
> quedaron fuera con la excusa `SIN CUPO EN n_sorteo`, no una segunda
> clase de `SKIP`.

**Lo que el mecanismo original (`sorteo_v2.asignar_asientos_proporcional`,
§2.2 del reglamento original) en realidad garantiza — no lo mismo que la
prosa de arriba**: `floor(cuota_exacta)` puro + mayor-resto sobre el
remanente. Ningún piso 1 aplicado antes del reparto — un estrato con
cuota exacta baja (p.ej. `0.5`) puede perder el desempate del remanente y
quedar en cero, aunque no esté vacío. Esto NO es un defecto de código: el
código coincide exacto con su propio pseudocódigo de §2.2. La brecha es
entre la prosa de la regla 3 (primera cláusula) y el mecanismo que ella
misma cita como implementación.

### 2.1 · Implementación exacta de la primera cláusula (`n_sorteo ≥ n_estratos_no_vacios`)

Implementada y verificada en `forense/prereg-duelo-v2/sorteo_v3.py`
(`asignar_asientos_proporcional_v3`, `sortear_v3` — P1 de este acto).
Pseudocódigo (idéntico al código real, no una versión simplificada):

```
función asignar_asientos_proporcional_v3(estratos, n_sorteo):
    n_estratos = len(estratos)                     # todos no vacíos, por construcción
    si n_sorteo < n_estratos:
        PARA -- segunda cláusula de la regla 3, no implementada (§2.2 abajo)

    asientos = {e: 1 para e en estratos}            # piso 1 por estrato no vacío
    resto = n_sorteo - n_estratos
    si resto == 0:
        devolver asientos

    total = sum(len(estratos[e]) para e en estratos)
    cuota_exacta_resto[e] = resto * len(estratos[e]) / total    # para cada estrato
    asientos_resto[e] = floor(cuota_exacta_resto[e])
    restantes = resto - sum(asientos_resto.values())
    orden = sort_by(estratos, key=(-frac(cuota_exacta_resto[e]), e))   # mismo desempate alfabético que §2.2 original
    para e en orden[:restantes]:
        asientos_resto[e] += 1

    devolver {e: asientos[e] + asientos_resto[e] para e en estratos}
```

El resto del pseudocódigo de §2.1 original (fallback de infactibilidad
§2.3, sorteo sin reposición dentro de cada estrato, presupuesto de cuota,
postcondiciones de la Verificación final) **no cambia** — `sortear_v3`
reusa esas partes línea a línea, sólo sustituye qué función reparte
asientos, en el reparto inicial **y** en el recálculo del fallback de
§2.3 (la regla 3 aplica en cada punto donde se reparten asientos, no sólo
en el primero).

### 2.2 · Segunda cláusula (`n_sorteo < n_estratos_no_vacios`) — NO implementada

Ningún sorteo del marco-M (`v1_0`: 1 estrato; `v1_1`: 2 estratos,
`n_sorteo=11`) ha necesitado esta cláusula. `sorteo_v3.
asignar_asientos_proporcional_v3` declara `NotImplementedError` explícito
si se presenta — no la aproxima en silencio. Queda **PENDIENTE-DE-MESA**
si algún sorteo futuro del marco-M la necesita (más estratos que asientos):
la prosa original describe "sortea sin reposición cuáles estratos entran",
pero no especifica con qué distribución (¿uniforme sobre estratos?
¿ponderada por tamaño?) — la misma disciplina que `mesa-pendientes.md`
aplica a otras ambigüedades de este corpus: se documenta la pregunta, no
se decide aquí.

## 3 · Hallazgo declarado — el piso no es un parche, cambia resultados en general

Verificado por cómputo (`tests_sorteo_v3.py::TestAsignarAsientosPisoUno::
test_piso_uno_no_es_solo_un_parche_cuando_v2_ya_daba_al_menos_1`), **mesa
debe leer esto antes de sellar**: "piso 1 + Hamilton sobre el resto" no
es una corrección que sólo actúa cuando el mecanismo puro deja a algún
estrato en cero — es un método de reparto distinto en general. Ejemplo
verificado (mismo marco que el Caso 1 de `sorteo-act-pil-3-v2-PROPUESTA.md`
§5, 3 estratos de 10/6/4 filas, `n_sorteo=12`, ningún estrato en cero bajo
el método puro):

| estrato | filas | v2 (Hamilton puro) | v3 (piso 1 + Hamilton sobre el resto) |
|---|---|---|---|
| `dinero\|P2\|DIFICIL` | 10 | 6 | 5 |
| `dinero\|P2\|MEDIA` | 6 | 4 | 4 |
| `trabajo\|P1\|MEDIA` | 4 | 2 | 3 |

Dar 1 asiento "gratis" a cada estrato antes de repartir proporcionalmente
el resto favorece sistemáticamente a los estratos chicos frente al
Hamilton puro — **incluso cuando el piso no estaba en riesgo**. Adoptar
la regla 3 con esta implementación exacta cambiaría, en general, más
sorteos que sólo los casos límite que motivaron este documento. Mesa
decide si ese es el efecto que quiere (letra literal de la regla 3, tal
como está redactada desde `ADR-178`) o si prefiere precisar la prosa para
que sólo actúe cuando el método puro deje a alguien en cero — ver §5.

## 4 · Casos de prueba (verificados contra datos reales, no sólo sintéticos)

Los tres casos sintéticos de `sorteo-act-pil-3-v2-PROPUESTA.md` §5 (Caso
1/2/3) siguen aplicando sin cambio a `sorteo_v2.py` (`ACT-PIL-3`, no
tocado). Para el marco-M, `sorteo_v3.py`/`tests_sorteo_v3.py` agregan:

- **`B′` (`v1_0`, real, mono-estrato):** el piso no liga — verificado
  (`asignar_asientos_proporcional_v3` da `{'tramite|P1|MEDIA': 2}`,
  idéntico a v2). Detalle: `forense/notas/2026-09-01-sorteo-v3-regresion-v1_1.md` §1.
- **`B″` (`v1_1`, real, 2 estratos, el caso que `FP-213` encontró):** el
  piso sí liga — `{'PENDIENTE': 10, 'tramite|P1|MEDIA': 1}` en vez de
  `{'PENDIENTE': 11, 'tramite|P1|MEDIA': 0}`; `TRA-M-02` entraría,
  `CIV-M-01` saldría. Reporte informativo completo, sin re-sortear:
  `forense/notas/2026-09-01-sorteo-v3-regresion-v1_1.md` §2.
- **Caso sintético — piso no es parche (§3 arriba):** confirma que la
  divergencia v2/v3 no se limita a los casos de cuota exacta ≤0.5.
- **Infactibilidad + piso 1** (`TestSortearV3ConInfactibilidad`): el
  fallback de §2.3 recalculado bajo piso 1 no fuerza asientos en un
  estrato infactible — mismo criterio del original, no relajado.

## 5 · Pendiente de mesa — qué falta para sellar

Este documento no sella nada. Antes de que la regla 3 (con esta
implementación) rija algún sorteo futuro del marco-M, mesa decide:

1. **¿Aplica esta implementación exacta (piso 1 + Hamilton sobre el
   resto), con el efecto general de §3 (cambia resultados más allá de los
   casos límite)?** — o mesa prefiere una implementación que sólo
   intervenga cuando el método puro deje a un estrato en cero (más
   cercana al Hamilton original, más quirúrgica, no implementada aquí).
2. **¿Esta regla 3 precisada aplica retroactivamente a `v1_1` (`B″`)?**
   — `FP-213`/opción A ya resolvió que NO: `v1_1` se acepta tal cual,
   este documento no lo reabre. Se pregunta aquí sólo para que quede
   explícito que sellar este reglamento no reabre esa decisión por sí
   solo — necesitaría su propia firma si mesa quisiera lo contrario.
3. **¿Qué hace la segunda cláusula de la regla 3 (§2.2) cuando algún
   sorteo futuro tenga más estratos que asientos?** — no implementada,
   pendiente de que un acto futuro la necesite y mesa elija el
   mecanismo.
4. **Número de ADR/FP para sellar**, siguiendo el mismo patrón que
   `ADR-178`/`FP-150` selló el original (`sorteo-act-pil-3-v2-PROPUESTA.md`
   §6, fila nueva de tablero, firma de mesa verbatim) — no reservado por
   este acto, deriva al sellar.

## 6 · Lo que este documento NO hace

No sella nada (sellar es de mesa). No re-sortea `v1_1` (`FP-213`, opción
A). No edita `sorteo_v2.py`, `sorteo_marco_m.py`, `sorteo_marco_m_v1_1.py`
ni `sorteo-act-pil-3-v2-PROPUESTA.md`/`ADR-178`. No redefine las reglas 1,
2, 4 o 5 (heredadas tal cual, §1). No implementa la segunda cláusula de la
regla 3 (§2.2). No decide entre la implementación literal de §2 y la
alternativa "quirúrgica" que §5.1 menciona — documenta la opción y para,
mesa elige.
