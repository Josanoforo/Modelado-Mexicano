# Integración y plan de trabajo · MILPA
### `milpa-plan` · **v0.1**

> | | |
> |---|---|
> | **ARCHIVO** | `milpa-plan-v0.1.md` |
> | **REEMPLAZA A** | `03-integracion-y-plan-de-trabajo.md` — **borrar** |
> | **VERIFICAS ASÍ** | la cabecera dice `milpa-plan` y trae la serie de lectura |
> | **NOMBRE ESTABLE** | **`milpa-plan`** — cítalo así, **nunca por nombre de archivo** |

> **Serie MILPA — orden de lectura.** *(El `01/02/03` anterior codificaba el orden en el nombre y no la versión; ADR-36 lo invierte. El orden vive aquí, explícito.)*
>
> **1.** `milpa-whitepaper` — el **porqué** · **2.** `milpa-spec` — el **cómo** · **3.** `milpa-plan` — el **cuándo**


*Documento 3 de 3. Requiere el Whitepaper (1) y la Especificación técnica (2).*

---

## Parte I · Integración esperada

### 1. Mapa: artefacto del corpus → módulo del sistema

| Artefacto existente | Alimenta | Forma concreta |
|---|---|---|
| **Ficha canónica del modelo** | `rules/`, `pop/profiles`, `world/generators` | **Fuente de verdad ejecutable.** Se compila a YAML. Es el único artefacto que el motor lee directamente. |
| **Modelo de decisión §1 (perfiles)** | `pop/profiles.yaml` | Los 6 perfiles con sus 9 parámetros base + reglas de asignación probabilística por celda |
| **Modelo §2 (generadores G1–G6)** | `world/generators.yaml` | Mapeo *capa estructural → coeficiente sobre parámetro*, con su cláusula falsable |
| **Modelo §3 (motor SI-ENTONCES, 10 dominios)** | `rules/<dominio>.yaml` | Una regla por entrada, con tier, generador, fuente y disparadores |
| **Modelo §3 (7 disparadores)** | `engine/triggers.py` | Evaluadores de contexto; se calculan antes de resolver la regla |
| **Modelo §1.4 (frontera de alcance)** | `world/scope_mask.geojson` | Máscara `OUT_OF_MODEL` para municipios de usos y costumbres |
| **Modelo §5 (límites y baja confianza)** | `epistemics/confidence.yaml` | Pesos del mapa de confianza; zonas declaradas de vacío |
| **Modelo §7 (validación Ronda 4)** | `tests/backtests/` | Los 5 casos como tests bloqueantes |
| **Integrador (30 reports)** | `docs/` + `tests/tensions/` | Documentación conceptual; las contradicciones no reconciliadas se vuelven **tests de tensión** (el sim no debe "resolverlas" por accidente) |
| **Los 30 reports temáticos** | `docs/glosario/`, catálogo de fuentes | Trazabilidad: cada regla apunta al report que la sostiene |
| **Meta-auditoría de comunicación** | `rules/comunicacion.yaml` | Driver corregido: *adaptación racional + face bajo dignidad*, nunca "honor"; constructos de diáspora marcados |
| **Instrucciones del proyecto v2 (Bloque A/B/C)** | `CONTRIBUTING.md` | Gobernanza del repo: qué se puede agregar y con qué evidencia |
| **Report de genómica** | *(nada)* | **Firewalleado.** No entra al cerebro del agente. Documentado como exclusión explícita. |

### 2. La ficha canónica como contrato

La decisión de arquitectura más importante del programa:

> **La ficha canónica deja de ser un documento de lectura y se vuelve un artefacto compilable.**

```
ficha-canonica-modelo.md  ──(compilador)──▶  rules/*.yaml  ──▶  motor
                                   │
                                   └─▶ validación de esquema (tier + fuente obligatorios)
```

Consecuencias prácticas:
- **Una sola fuente de verdad.** Se acabó el problema que tuvo el vertical V1 (reconstruir el modelo de memoria porque no pudo leer los documentos).
- **Toda actualización del corpus se propaga.** Cuando una ronda de validación cambia una regla (como pasó con "calidad/dignidad > precio", degradada a no validada), se edita la ficha, se recompila, y **los backtests dicen si el simulador sigue siendo consistente**.
- **Auditoría real.** `git diff` sobre `rules/` muestra exactamente qué cambió del conocimiento y cuándo. Un cambio de regla sin cambio de fuente es un olor a captura.

### 3. Catálogo de fuentes de datos

| Fuente | Aporta | Granularidad real | Necesita SAE |
|---|---|---|---|
| **Censo INEGI 2020** | Marginales de población, hogar, escolaridad, lengua indígena | Municipio / AGEB | No |
| **ENOE** (trimestral) | Informalidad, ocupación, ingreso, **dinámica** (panel rotativo) | Estatal / áreas urbanas | Sí (a municipio) |
| **ENIGH** (bienal) | Ingreso-gasto, deciles | Estatal | Sí |
| **CONEVAL** | Pobreza multidimensional, carencias | **Municipal** | No |
| **SESNSP** | Homicidio, extorsión, delitos | **Municipal, mensual** | No |
| **ENVIPE** (anual) | Victimización, cifra negra, denuncia | Estatal | Sí |
| **ENSU** (trimestral) | Percepción de inseguridad | Urbana | Sí |
| **ENCIG** (bienal) | Trámites, corrupción, confianza institucional | Localidades 100k+ | **Sí, fuerte** |
| **ENCUCI** | Cultura cívica, participación, capital social | 100k+ | Sí, fuerte |
| **ENIF** (CNBV/INEGI) | Inclusión financiera, ahorro, crédito, metas, tandas | Estatal / urbano-rural | Sí |
| **ENDUTIH** | Conectividad, uso digital | Estatal | Sí |
| **ENSANUT** | Salud, obesidad, acceso, adherencia | Estatal | Sí |
| **ENUT** | Uso del tiempo, brecha de cuidado | Estatal | Sí |
| **CEEY** | Movilidad social intergeneracional, colorismo | Regional (5 regiones) | Sí, fuerte |
| **CNBV** | IMOR, corresponsales, sucursales | Municipal (infraestructura) | No para infraestructura |
| **Banxico** | Remesas, crédito, estabilidad financiera | Municipal (remesas) | No |
| **INE** | Participación electoral | **Sección electoral** | No |
| **LAPOP / Latinobarómetro / Pew** | Confianza generalizada, actitudes | Nacional | No usar bajo estatal |

**Advertencia que debe viajar con el proyecto:** la mitad de las capas más importantes para los generadores (G1 confianza, G4 percepción, G3 informalidad fina) **no existen a nivel municipal** y llegan por SAE. Ese es el techo de resolución real del simulador, y el mapa de confianza debe hacerlo visible en todo momento.

### 4. Gobernanza del repo

`CONTRIBUTING.md` codifica el Bloque A/B/C del programa como reglas de contribución:

- Toda regla nueva: **tier + fuente + generador**, o no compila.
- Toda regla `FUERTE`: cláusula `falsable_si` obligatoria.
- Toda capa nueva: `{v, ic, src, sae}` completos.
- **Prohibiciones duras en CI:** ninguna variable de ascendencia en `pop/` ni en `rules/`; ninguna regla aplicada a celdas `OUT_OF_MODEL`; ninguna salida a nivel de individuo real.
- Cambio de regla que altera un backtest: requiere justificación escrita en el PR (qué evidencia nueva lo motiva).

---

## Parte II · Plan de trabajo

Siete fases. Cada una con **criterio de salida verificable** — no "terminamos la fase", sino "el sistema hace X".

### Fase 0 · Fundación (2–3 semanas)
Repo, esquema del DSL, compilador `ficha canónica → YAML`, validación de esquema en CI, `CONTRIBUTING.md` con las prohibiciones duras.
**Salida:** las reglas del modelo existen como YAML validado y versionado; un test falla si alguien mete una regla sin fuente.

### Fase 1 · Rebanada vertical (4–6 semanas) — *la fase que decide todo*
**Un** municipio urbano (p. ej. una alcaldía de CDMX) + **un** municipio rural mestizo, 50k agentes, **tres** dominios (dinero, trámite, salud), sin red social todavía.
**Salida:** el backtest **OXXO vs. CoDi** pasa: el producto con canal de confianza y respaldo se adopta; el institucional-frío no. Si esto no sale, el problema es el modelo, no la ingeniería — y hay que volver al corpus antes de escalar.

### Fase 2 · Capas nacionales (6–8 semanas)
ETL de todas las fuentes, SAE con incertidumbre, población sintética nacional por IPF, máscara de exclusión.
**Salida:** el mapa nacional existe con su mapa de confianza; los hechos estilizados (informalidad, cifra negra, participación) se reproducen dentro de banda.

### Fase 3 · Red social y difusión (4 semanas)
Grafo de tres lazos, difusión por umbral, calibración contra tandas (ENIF) y capital social (ENCUCI).
**Salida:** un producto lanzado por puente personal se difunde; el mismo producto por canal institucional no. Emergencia visible, no cableada.

### Fase 4 · Motor a escala (6–8 semanas)
Reescritura del núcleo en Rust, muestreo por celda, paralelización.
**Salida:** 10⁷ agentes, 40 trimestres, en minutos, con trazas.

### Fase 5 · Retroalimentación e intervenciones (5–6 semanas)
Los seis bucles nombrados, la API de intervenciones, el contrafactual automático.
**Salida:** una intervención de formalización alarga el horizonte de la población afectada y aparece ahorro formal — el hallazgo Progresa, **emergente y no programado**.

### Fase 6 · Front-end y capa epistémica (6 semanas)
Mapa doble obligatorio, mapa de confianza, fan charts, trazas navegables, modo sin-hipótesis, diario narrativo.
**Salida:** ningún resultado se puede ver sin su incertidumbre y sin su capa estructural espejo.

### Fase 7 · Endurecimiento y release (4 semanas)
Suite completa de backtests, licencia de uso, documentación, auditoría externa de sesgo.
**Salida:** los cinco backtests forenses pasan; el modo sin-hipótesis está documentado; la licencia prohíbe el uso para scoring de personas.

**Duración total:** ≈ 9–11 meses con un equipo pequeño (2 ingenieros + 1 científico de datos + 1 diseñador, a tiempo parcial); considerablemente menos con construcción agéntica intensiva.

### Puntos de decisión (go / no-go)

| Gate | Pregunta | Si la respuesta es no |
|---|---|---|
| **Fin de Fase 1** | ¿El backtest OXXO/CoDi pasa con reglas honestas (sin tunear a mano)? | Parar. El problema está en el modelo. Volver al corpus. |
| **Fin de Fase 2** | ¿El SAE deja intervalos utilizables, o la incertidumbre municipal es tan ancha que el mapa no dice nada? | Bajar la ambición espacial: trabajar a nivel estatal/zona metropolitana, no municipal. |
| **Fin de Fase 5** | ¿Los bucles producen emergencia plausible, o divergen/se congelan? | Los coeficientes dinámicos (el hueco §6.2) son insuficientes. Reducir a escenarios comparativos estáticos. |
| **Fin de Fase 7** | ¿Sobrevive el modo sin-hipótesis? | Publicar solo las conclusiones que sobrevivan, y decirlo. |

---

## Parte III · Qué se delega a Fable, y por qué

**La razón honesta no es "sabe más de México".** De eso se encargó este programa: el conocimiento ya está destilado, tierizado y validado en la ficha canónica. Lo que hace falta ahora es **ingeniería pesada y sostenida**, que es donde un modelo frontera rinde de verdad:

1. **Construcción multi-archivo con estado interdependiente.** Un ETL con 17 fuentes, un compilador de DSL, un motor de simulación, un grafo, una capa de SAE, un front-end de mapa y tres suites de tests — todo mutuamente dependiente. Es exactamente el perfil de trabajo agéntico de largo alcance.
2. **Traducción especificación → código sin deriva semántica.** El riesgo #1 al implementar este modelo es que un tier se pierda por el camino, o que un coeficiente HIPÓTESIS termine mostrándose como número duro. Mantener la disciplina epistémica *dentro del código* requiere entender por qué existe, no solo copiar el YAML.
3. **Reescritura de rendimiento (Python → Rust) preservando semántica.** Trabajo mecánicamente delicado y verificable por tests: ideal para delegar.
4. **La suite de backtests como especificación ejecutable.** Los criterios ya están escritos en lenguaje natural en `milpa-spec §10`; convertirlos en tests con umbrales es trabajo de precisión.

**Cómo entregárselo.** Los tres documentos + la ficha canónica + el modelo completo, con el encargo estructurado por fases y **el gate de Fase 1 como primer entregable** — no "constrúyelo todo", sino "haz la rebanada vertical y demuéstrame que el backtest pasa".

**Y el remate que hace que la delegación sea casi poética:** el modelo se llama **Fable**, y lo que estamos construyendo es una máquina que genera *fábulas plausibles* de un México sintético bajo condiciones que elegimos. Le estamos pidiendo a un narrador que fabule mundos — con la diferencia de que estas fábulas tienen que pasar backtests contra la realidad documentada. Que es, al final, la única diferencia entre un modelo y un cuento.

---

## Parte IV · Módulo de auditoría de rigor extremo (aplicado a este plan)

- **¿Qué parte confunde pobreza/desigualdad/violencia/informalidad con "cultura"?** Ninguna por diseño —las capas del mundo *son* la estructura y los parámetros se derivan de ellas—, pero el riesgo reaparece en la **presentación**: un mapa de conducta sin su espejo estructural se lee como mapa de carácter. Por eso el mapa doble es restricción técnica, no convención de estilo.
- **¿Qué parte sobregeneraliza desde clases medias urbanas?** Casi toda la calibración fina: las encuestas más ricas (ENCIG, ENCUCI, ENSU, ENIF) son urbanas o de localidades grandes. El simulador **predecirá mejor al perfil 1 que al 2**, que es la mayoría del país. El mapa de confianza debe mostrar esa asimetría, no disimularla.
- **¿Qué está sesgado por marcos anglosajones o muestras mexicano-americanas?** Las reglas del dominio comunicación (simpatía, machismo, marianismo). Entran ya marcadas por la meta-auditoría y con tier degradado; no deben usarse para calibrar nada estructural.
- **¿Qué cambiaría con foco rural, indígena o popular?** Casi todo lo fino. Por eso hay dos tratamientos distintos: lo **rural mestizo y popular** entra al modelo con baja confianza declarada (es el mismo sistema, peor medido); lo **indígena-comunal** no entra (es otro sistema).
- **¿Qué parece psicológico pero es incentivo racional?** Todo el motor está construido sobre esa distinción; el riesgo inverso también existe: que el simulador vuelva **infalsable** la adaptación racional (siempre habrá un incentivo que justifique cualquier conducta). Mitigación: las cláusulas `falsable_si` obligatorias y el modo sin-hipótesis.
- **¿Dónde hay evidencia débil pero intuición fuerte?** En los **coeficientes dinámicos** de los bucles: sabemos la dirección, casi nunca el ritmo. Es el hueco más serio del proyecto y está declarado en el whitepaper §6.2.
- **¿Qué conclusiones serían peligrosas si alguien las usara de forma simplista?** Un mapa que diga "aquí la gente no paga / no denuncia / no ahorra" sin su capa estructural sería munición para políticas punitivas y para discriminación territorial en crédito y seguros. Es el riesgo existencial del proyecto, y la razón de las prohibiciones duras en CI y en la licencia.
