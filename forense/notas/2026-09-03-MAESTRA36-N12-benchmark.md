# `ACTO MAESTRA36-N12` · `P0` — benchmark web, con fuente y sin decidir

Consulta: **3/sep/2026**, desde la nube. Toda cifra de `L8` sale del clon en
`18fd2bd`, con el comando a la vista; toda cifra externa sale de la red y trae
URL y fecha. Este documento **no propone nada**: es el insumo de `P1`.

---

## §0 · Reserva de conducto — el encargo pidió *abrir* tres documentos; este acto no pudo

`A.13`. El encargo ordena «el acto abre los tres». **No se abrió ninguno.** La
política de egreso de este entorno de nube deniega la salida a los tres
dominios de las fuentes de partida:

| comando | dominio | salida cruda |
|---|---|---|
| `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` | `www.inegi.org.mx` | `000` |
| `WebFetch` | `portalanterior.ine.mx` | `EGRESS_BLOCKED` |
| `WebFetch` | `www.te.gob.mx` | `EGRESS_BLOCKED` |
| `WebFetch` | `centralelectoral.ine.mx` | `EGRESS_BLOCKED` |
| `WebFetch` | `en.wikipedia.org` (control negativo) | `EGRESS_BLOCKED` |
| `curl -sS "$HTTPS_PROXY/__agentproxy/status"` | — | `recentRelayFailures: connect_rejected — gateway answered 403 to CONNECT (policy denial)` |

El control con `en.wikipedia.org` establece que **el bloqueo no es de esos tres
dominios sino de `WebFetch` en general** en este entorno: no es señal sobre las
fuentes. `WebSearch` **sí** funciona, y es el único conducto que este acto tuvo.

**Consecuencia, declarada y no disimulada:** ninguna cita de abajo es
`VERIFICADA-EN-DOCUMENTO`. Todas son `SNIPPET-DE-BÚSQUEDA` — texto que el
índice devolvió, no texto que esta sesión leyó en el PDF. La columna
`procedencia` de la tabla de §1 lo marca fila por fila, y **ninguna cifra
externa entra al motor** (el encargo ya lo prohibía: «corroboración externa del
tamaño, no dato del motor»). Un acto en Ubuntu, o una sesión de nube con
política de egreso abierta a `ine.mx`/`te.gob.mx`, cierra esta reserva
abriendo los tres PDF; hasta entonces la corroboración de §1 es **indiciaria**.

---

## §1 · (a) Tamaño del efecto — tabla `fuente × efecto × unidad × diseño`

Punto de comparación interno, re-derivado en esta sesión contra `18fd2bd`:

```
$ python3 -c "import json; d=json.load(open('data/l8-resultados-tipo-boleta-v1_0.json')); print(d['estimador']['beta_pres_pp'], d['estimador']['wild_cluster_beta_pres']['ic95'], d['estimador']['ic95_bootstrap_municipio']['ddp'])"
4.016715486813227 [0.04917010866182059, 7.887405629522231] [3.3466938538022744, 4.683895737304484]
```

| # | fuente | efecto reportado | unidad de análisis | diseño | procedencia |
|---|---|---|---|---|---|
| 0 | **`L8`** (interno, `data/l8-resultados-tipo-boleta-v1_0.json`) | **`β_pres` = +4.017 pp**; IC95 wild cluster entidad `[+0.049, +7.887]`; IC95 bootstrap municipio `[+3.347, +4.684]`; `β_int` = +0.286 `[−1.222, +1.794]` | municipio × elección de ayuntamiento (`participación = 100·votos/lista_nominal`) | DD escalonado por tipo de boleta federal; 864 transiciones municipio, 9 entidades, 7 tratadas medibles | verificado por comando, esta sesión |
| 1 | INE, *Estudio muestral sobre la Participación Ciudadana 2015* — `portalanterior.ine.mx/archivos2/DS/recopilacion/CG.ex201606-29in_01P11-00.pdf` | **53.3 % con concurrencia local vs 50.2 % sin → +3.1 pp** (cifra que **dirección** declara haber verificado el 3/sep; este acto NO la reprodujo) | distrito electoral federal, elección **federal** (diputados 2015) | comparación descriptiva de medias entre grupos de distritos; sin control ni panel | **NO ABIERTO** — `EGRESS_BLOCKED`; el buscador devuelve la URL pero no el número |
| 2 | TEPJF (2020), *Elecciones concurrentes y participación electoral en México, 1991-2018* — `te.gob.mx/editorial_service/media/pdf/250320241355301010.pdf` (y `…/JEA_Elecciones_concurrentes.pdf`) | **no aísla un efecto de concurrencia.** Lo que el índice devuelve son series de participación en intermedias: «66 %, 58 %, 41 %, 45 % y 48 %», con cambios «−8, −17, +4 y +3» pp **entre elecciones consecutivas** — variación temporal, no contraste concurrente/no-concurrente | elección nacional × año | descriptivo longitudinal | `SNIPPET-DE-BÚSQUEDA` (`WebSearch`, 3/sep/2026) |
| 3 | INE, *Estudio Muestral de Participación Ciudadana 2024* (concurrentes, 2/jun/2024) — `repositoriodocumental.ine.mx/xmlui/handle/123456789/178351` | **no aísla el efecto: no hay grupo de control.** Reporta niveles — «participación del 59.8 % en el PEF 2023-2024», mujeres 64.3 % / hombres 54.8 %, Campeche 62.3 % máx., Baja California 37.7 % mín. | casilla → agregado nacional/estatal/distrital; muestra de **20 160 casillas** (300 muestras aleatorias, una por distrito) | muestreo descriptivo; **2024 fue concurrente en las 32 entidades**, así que no existe contrafactual dentro del año | `SNIPPET-DE-BÚSQUEDA` (`WebSearch`, 3/sep/2026) |
| 4 | Hajnal y Lewis (2003), vía literatura comparada *on-cycle/off-cycle* — `electionlab.mit.edu/research/election-timing`, `evenyear.org/turnout` | **+36 pp** (elecciones municipales concurrentes con la presidencial vs fuera de ciclo) | ciudad × elección municipal (California) | comparación entre ciudades con controles | `SNIPPET-DE-BÚSQUEDA` (`WebSearch`, 3/sep/2026) |
| 5 | Wood, citado en la misma literatura | **−29 pp** por calendario fuera de ciclo, media de 57 ciudades | ciudad × elección municipal | comparación entre ciudades | `SNIPPET-DE-BÚSQUEDA` |
| 6 | Caren, citado en la misma literatura | **≈ −27 pp** | ciudad × elección municipal | comparación entre ciudades | `SNIPPET-DE-BÚSQUEDA` |
| 7 | Anzia (2014), *Timing & Turnout* — `gspp.berkeley.edu/assets/uploads/research/pdf/Election_Timing_5_19_10.pdf` | no da un pp único; la tesis es que el calendario fuera de ciclo **favorece a grupos organizados** vía baja participación | ciudad/distrito escolar × elección | comparación y diferencia-en-diferencias sobre cambios de calendario | `SNIPPET-DE-BÚSQUEDA` |

Citas ≤ 15 palabras, con fecha de consulta **3/sep/2026**:

- Fila 2 — «66 %, 58 %, 41 %, 45 % y 48 %; cambios de −8, −17, +4, +3 puntos» ([te.gob.mx](https://www.te.gob.mx/editorial_service/media/pdf/250320241355301010.pdf), vía `WebSearch`).
- Fila 3 — «Se alcanzó una participación del 59.8 % en el PEF 2023-2024» ([repositoriodocumental.ine.mx](https://repositoriodocumental.ine.mx/xmlui/handle/123456789/178351), vía `WebSearch`).
- Fila 3 — «20,160 casillas … 300 muestras aleatorias e independientes, una por distrito» (misma fuente).
- Fila 4 — «city elections concurrent with presidential have turnout 36 percentage points higher» ([electionlab.mit.edu](https://electionlab.mit.edu/research/election-timing), vía `WebSearch`).
- Fila 5 — «off-cycle timing dampened city turnout by 29 points across fifty-seven cities» (misma fuente).
- Fila 6 — «turnout significantly lower in cities not concurrent with presidential, about 27 points» (misma fuente).

### §1.1 · Lectura del benchmark — dos estimandos, no uno

La tabla parece contradictoria (+3 pp mexicano contra +27…+36 pp
estadounidense). **No lo es: son dos estimandos distintos, y solo uno es el de
`L8`.**

- Las filas 4-6 comparan una elección municipal celebrada **en otra fecha**
  contra la misma celebrada el día de la presidencial. El contrafactual
  *off-cycle* estadounidense arranca de una participación de ~10-25 %.
- `L8` compara un ayuntamiento mexicano **no concurrente** contra uno
  **concurrente**, y en México el contrafactual no concurrente ya participa
  entre **30.5 % y 71.0 %** (§2 de la nota de propuesta). La jornada local no
  concurrente sigue siendo una jornada estatal organizada, con casilla única y
  boleta entregada en el mismo acto cuando concurre — no un martes de abril
  con 12 % de asistencia.

Por eso **la fila 1 (INE 2015, +3.1 pp) es el comparador correcto en orden de
magnitud, y las filas 4-6 no lo son**, aunque nombren el mismo fenómeno. La
fila 1 mide, además, el efecto sobre la elección **federal** (dirección
inversa a `L8`, que mide el efecto sobre la **local**) — la corroboración es
de **orden de magnitud y signo**, no de estimando.

**Corroboración externa disponible:** débil pero consistente. `+4.0 pp` de
`L8` cae en el mismo orden que el `+3.1 pp` que dirección leyó en INE 2015, con
el mismo signo. Ninguna de las otras fuentes aísla el efecto. **Lo que el
benchmark NO hace:** validar el tamaño con un estudio de diseño comparable
sobre municipios mexicanos — ese estudio no apareció en la búsqueda, y su
ausencia es parte del entregable.

---

## §2 · (b) Cómo se convierte una diferencia en pp a probabilidad individual

### §2.1 · Las dos convenciones

Sea `p₀` la probabilidad base de que un individuo vote en su municipio, y
`Δ = 0.040167` el efecto de `L8` expresado en proporción.

**(i) Diferencia de riesgo (aditiva, escala de probabilidad).**

```
p₁ = p₀ + Δ,   acotada a [0, 1]
```

El efecto es **constante en pp** por construcción; es lo que estima
directamente un modelo lineal de probabilidad, y es la escala en la que `L8`
está medido (`β` es un coeficiente de MCO sobre participación en pp). Traducirlo
así es una **identidad de escala, no una conversión**.

**(ii) Razón de momios (multiplicativa, escala logit).**

```
logit p₁ = logit p₀ + δ,   δ = log OR,   p₁ = 1/(1 + e^−(logit p₀ + δ))
```

El efecto es constante **en log-momios**; su tamaño en pp depende de `p₀`, y es
máximo en `p₀ = 0.5`, tendiendo a cero en los extremos.

### §2.2 · Cuándo divergen

La equivalencia entre ambas **depende de la tasa base** — es el punto de Grant
(2014), *Converting an odds ratio to a range of plausible relative risks*, BMJ
348:f7450, y de la viñeta `effectsize` sobre conversión OR↔RR con `p0`:

- Cita ≤15 palabras — «one odds ratio can mean several different relative risks, depending on baseline risk» ([easystats.github.io/effectsize](https://easystats.github.io/effectsize/articles/convert_p_OR_RR.html), consulta 3/sep/2026, `SNIPPET-DE-BÚSQUEDA`).
- Cita ≤15 palabras — «risk difference is variation dependent on baseline risk; odds ratio is variation independent» (misma fuente).

**Divergen en tasas base extremas** (`p₀ → 0` o `p₀ → 1`) y **coinciden por
construcción en el `p₀` de calibración**. Además, solo la convención (ii)
respeta el soporte `[0,1]` sin recorte: la (i) puede empujar `p₁` fuera del
intervalo cuando `p₀ > 1 − Δ`, y ahí hay que acotar (con `Δ = 0.040`, para
`p₀ > 0.96`).

### §2.3 · Qué usa la literatura de turnout para efectos de contexto

**La aditiva.** El modelo lineal de probabilidad es la convención dominante
cuando el efecto es de **contexto** (calendario, concurrencia, reglas) y no de
atributo individual, precisamente porque sus coeficientes ya están en escala de
probabilidad:

- Cita ≤15 palabras — «LPM coefficients remain on the probability scale, read directly as percentage point changes» ([arxiv.org/pdf/2308.15338](https://arxiv.org/pdf/2308.15338) y discusión asociada, consulta 3/sep/2026, `SNIPPET-DE-BÚSQUEDA`).
- Cita ≤15 palabras — «linear specification keeps all observations; logit drops groups with all-zero or all-one outcomes» ([Political Analysis, Cambridge Core](https://www.cambridge.org/core/journals/political-analysis/article/estimating-grouped-data-models-with-a-binarydependent-variable-and-fixed-effects-via-a-logit-versus-a-linear-probability-model-the-impact-of-dropped-units/AD6E3A3EA15BEDECA6B6FD49FE0216B3), consulta 3/sep/2026, `SNIPPET-DE-BÚSQUEDA`).

Toda la literatura de la tabla §1 (filas 1-6) reporta **puntos porcentuales**,
ninguna reporta razones de momios. El logit aparece en turnout sobre todo en
regresiones **individuales** de encuesta con covariables demográficas — que no
es el caso de `L8`.

**Consecuencia para `P1`:** la convención que la literatura del propio fenómeno
usa es la **aditiva**, y es también la escala nativa de la medición de `L8`.
El logit se corre como **sensibilidad**, no como alternativa en pie de
igualdad. La cuantía de esa sensibilidad está medida en la nota de propuesta.

---

## §3 · Qué queda abierto

1. **Los tres PDF no se abrieron** (§0). La fila 1 de §1 sigue apoyada en la
   lectura de dirección, no en una verificación de esta sesión.
2. **No hay estudio externo con el estimando de `L8`** (municipio mexicano,
   elección de ayuntamiento, concurrencia con presidencial, diseño de panel).
   Si existe, la búsqueda de este acto no lo encontró.
