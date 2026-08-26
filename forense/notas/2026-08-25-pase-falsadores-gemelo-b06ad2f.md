> segunda corrida divergente del mismo encargo, sin fusionar — se preserva para adjudicación por ficha

# Pase de existencia — falsadores sin veredicto y sin vía en curso

*(Encargo `PASE-FALSADORES`, SHA de redacción `9e9132d`, dirección 25/ago/2026, ENTORNO NUBE. Un pase único: "¿este falsador pide algo que puede existir?" Sin firma — mesa decide después, ficha por ficha. CONTADOR: cero por diseño — este acto no adjudica ningún veredicto de Hito D y no mueve `20 de 27`.)*

## Nota de arranque — SHA de HEAD

HEAD al arrancar este acto era `c6a5ab3`, no `9e9132d` (el SHA de redacción citado en el encargo). Se declara la discrepancia y se continúa, conforme a instrucción del encargo ("informa si difiere, pero continúa"). `data/raw` no se consultó — ENTORNO NUBE, sin acceso a microdatos, sonda de datos saltada por diseño.

## F0 — derivación de la lista de fichas en alcance

Fuente: `forense/hitoD-preregistro-v2_0.md`, bloque `## Registro de veredictos archivados` (línea 1101, único bloque que un test puede leer como veredicto emitido). Conteo por comando (`grep -c`) da **20 fichas con veredicto archivado** de las **27 fichas totales** (`## R1.1` … `## R10.3`), coincide con `README.md:36` ("20 de 27").

Las 7 fichas SIN veredicto archivado son: `R2.1`, `R2.2`, `R3.4`, `R8.2`, `R10.1`, `R10.2`, `R10.3`.

De ellas, el propio encargo excluye 4 por tener ya vía en curso o cierre de mesa (ver tabla de exclusiones abajo). **Alcance final de este pase: `R2.2`, `R8.2`, `R10.2`** — exactamente las tres que el encargo anticipaba, y las tres que `hitoD-preregistro-v2_0.md:329` ya agrupa bajo el patrón "dato organizacional propietario": *"Ocho de veintisiete: R1.4 · R2.1 · R2.2 · R7.4/R7.5 · R8.2 · R8.3 · R10.2 · R10.3 ... Los agrupa un patrón: dato organizacional propietario (R2.2, R8.2, R10.2)..."*.

### Fichas excluidas, con cita

| Ficha | Motivo de exclusión | Cita en repo |
|---|---|---|
| `R3.4` | Vía en curso: gate A∧B∧C adjudicándose vía `#359`/`FP-157` — condición A sellada (ADR-177), B/C censadas y propuestas por `ACTO R34-BC-MECANISMO`, pendiente de que mesa adjudique | `forense/firmas-pendientes.tsv` fila `FP-157`; `forense/notas/2026-08-25-r34-bc-mecanismo-cierre.md` |
| `R2.1` | Vía en curso: `R21-FALSADOR-V2` — spec sucesora en tramitación | citado por el encargo; no se reabre ni se toca en este pase |
| `R10.1` | Spec v2.0 ya sellada (`FP-128`, `ADR-166`); acto sucesor `CORRE-R10.1` pendiente de lanzar pero ya en curso — no es "sin vía" | `forense/firmas-pendientes.tsv` fila `FP-128`; `forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md` |
| `R10.3` | Cierre ético por decisión/firma de mesa, no se reabre — el propio pre-registro ya declara: *"Solo dato secundario ya publicado y agregado; ninguna recolección primaria... D es preferible a un dato obtenido poniendo a alguien en riesgo"* | `forense/hitoD-preregistro-v2_0.md` ficha `R10.3`; `forense/hallazgos.md` §357 ("ningún veredicto vale exponer a un informante") |

Se lista `R10.3` para declarar el hueco, no para ocultarlo — no se produce veredicto triple para ella en este acto.

### Chequeo de duplicados

`grep -ril "pase.falsador" forense/` → **0 resultados**. Ningún pase idéntico ya existe en el repo.

## Veredicto triple por ficha

| Ficha | Veredicto | Bosquejo / fuente candidata | Letra máxima honesta alcanzable | Qué falta |
|---|---|---|---|---|
| `R2.2` | **SIN-DATO-GENUINO**, inejecutabilidad **DEL MUNDO** | Ninguna re-especificación pública identificada. Requeriría panel de clima organizacional (rotación voluntaria + productividad auditada) con etiqueta independiente de estilo de liderazgo (benévolo/autoritario), controlando sector, salario y prestaciones | Ninguna — el propio pre-registro ya declara `D probable`: "el dato de clima suele ser propietario y auto-reportado por parte interesada" | Encuesta pública mexicana de clima organizacional con desempeño/rotación auditados (no auto-reportados) y clasificación de estilo de liderazgo. No se identificó ninguna en el censo previo (`matriz-impacto-universal-2026-08-06.md` no la lista; `cruce-catalogo-fichas` tampoco). Vía llave en mano clase (iii): partnership con una consultora de clima organizacional (tipo Great Place to Work México) con acceso a microdato de encuestas de clima por firma — costo aproximado: orden de decenas de miles de USD por convenio de acceso a datos agregados por firma, más alto si se exige microdato por empleado (pendiente de verificación, no es cifra medida) |
| `R8.2` | **SIN-DATO-GENUINO**, inejecutabilidad **DEL FALSADOR** (parcialmente) — ver nota | La sustancia (enforcement de plataforma sustituye a la confianza personalizada en esquemas de ahorro rotativo) SÍ podría contrastarse fuera del corte estrictamente propietario de "app de tanda digital": el falsador tal como está redactado pide la métrica de incumplimiento de una plataforma privada específica, pero el fenómeno también vive, en principio, en cooperativas de ahorro reguladas (SOCAPs) o en programas de microfinanzas con enforcement institucional y sin vínculo personal previo entre ahorradores — dato que podría ser público vía CNBV/reguladores si publican tasas de cartera vencida por tipo de producto | Si se re-especifica al nivel de SOCAP/microfinanciera con enforcement institucional (en vez de app de tanda), la letra cae de un falsador `[FUERTE]` limpio a lo sumo `C`: la comparación deja de ser "tanda de desconocidos vs. tanda de conocidos" y pasa a ser un traslado de dominio (ahorro cooperativo regulado, no ROSCA informal entre desconocidos) — correlacional, no el "más limpio del perímetro" que la ficha original reclama | Verificación puntual pendiente: si alguna app de ROSCA digital mexicana (u operador de tandas online) publica tasa de incumplimiento agregada — no se encontró en el censo del repo (`matriz-impacto-universal-2026-08-06.md`: "candidata MINES resultó sitio de apuestas; ninguna candidata directa abierta"). Búsqueda web puntual queda pendiente de verificación por un humano (receta de 1 minuto: buscar "app tanda México tasa de incumplimiento" o "ROSCA app default rate Mexico" en buscador; SIN-FETCH en este acto — NUBE, sin WebFetch confiable invocado) |
| `R10.2` | **RE-ESPECIFICABLE** | Sustancia: retroalimentación negativa pública vs. privada y su efecto en desempeño/rotación. Nivel donde el dato vive: en vez de panel organizacional con retro pública/privada etiquetada (lo que la ficha pide y que es dato de clima propietario), la sustancia podría acercarse con **estudios de caso publicados en literatura de administración/recursos humanos sobre México** (revistas académicas, tesis, casos de escuela de negocios) que documenten episodios de feedback público y su desenlace — o con **encuestas de clima laboral públicas de terceros** (si algún operador de encuestas de clima publica desagregado por práctica de feedback, cosa no verificada) | Correlacional en el mejor caso, con **n pequeño y sin control formal de sector/salario/prestaciones** — la ficha exige "diferencia <10% con control de sector"; una recopilación de casos de estudio degrada, a lo sumo, a una fila `B` (anecdótico sin control), nunca a `A`. Se pierde toda capacidad de adjudicar el umbral cuantitativo que la ficha exige | Un censo real de estudios de caso mexicanos sobre feedback público/privado en el trabajo — no se ejecutó en este acto (es medición, prohibida aquí). Sin ese censo no se sabe si siquiera existe volumen suficiente de casos para una lectura `B` honesta |

## Un párrafo por ficha, para mesa

**`R2.2` — Liderazgo benévolo → lealtad.** Esta ficha pregunta si un liderazgo autoritario-no-benévolo puede tener tan buena retención y desempeño como uno benévolo en México. El dato que necesita —clima organizacional con desempeño auditado, no auto-reportado— es información que las empresas casi nunca comparten fuera de sus propios departamentos de RH; no hay una encuesta pública mexicana que lo traiga. Comprar acceso a él (opción "llave en mano", tipo convenio con una firma de encuestas de clima organizacional) es plausible pero probablemente costoso —del orden de decenas de miles de dólares, sin verificar—, y nada barato garantiza que cubra justo el corte "autoritario no-benévolo con buen desempeño" que el falsador pide. Lo que este veredicto NO compra: no hay ningún atajo público conocido; declarar `D` aquí es honesto, no es pereza.

**`R8.2` — Conoce a la organizadora → entra a la tanda.** Este es el falsador que el propio pre-registro llama "el más limpio del perímetro" porque el mecanismo es explícito: si el enforcement de una plataforma (en vez de una persona conocida) también sostiene la participación en un esquema de ahorro rotativo, el mecanismo se generaliza. El diseño registrado pide la tasa de incumplimiento de una app de tandas digitales — dato que hoy es privado de la plataforma. Lo que este pase agrega: la misma pregunta (¿el enforcement institucional sustituye al personal?) también vive, en teoría, en cooperativas de ahorro reguladas por CNBV, que en principio publican indicadores de cartera. Comprar esa vía no cuesta un partnership caro — cuesta verificar, con una búsqueda puntual (pendiente, no hecha aquí porque este acto no tiene fetch confiable), si el regulador realmente desagrega esos indicadores por producto de forma que sirva. Lo que esta re-especificación NO compra: si se usa, ya no es "tanda de desconocidos" en el sentido coloquial — es ahorro cooperativo regulado, y la letra cae de una prueba limpia a una correlación de dominio distinto.

**`R10.2` — Retroalimentación negativa pública destruye capital social.** El diseño pide un panel organizacional con feedback etiquetado público/privado y desempeño medido — otro dato de clima propietario, como `R2.2`. La re-especificación honesta que se puede bosquejar es bajar el nivel de exigencia: en vez de un panel controlado, usar estudios de caso ya publicados sobre episodios de feedback público en organizaciones mexicanas. Eso compra, como mucho, una fila `B` (evidencia anecdótica, sin control de sector/salario) — nunca el umbral cuantitativo `<10%` que la ficha exige para degradar la palabra "SOLO"/"destruye". Lo que esto NO compra: no resuelve si "destruye capital social" es cierto o falso; solo ofrece una vía más barata de reunir evidencia parcial, y mesa tendría que decidir si esa evidencia parcial vale la pena frente a dejarlo en `D`.

## Regla del candado — recordatorio

Ninguna de las tres propuestas de arriba cambia lo que el falsador afirma para que algo lo confirme. `R8.2` y `R10.2` re-especifican el **nivel** donde el dato vive (cooperativa regulada en vez de app privada; estudios de caso en vez de panel propietario), no la sustancia de la relación causal que cada ficha quiere probar. `R2.2` no tiene re-especificación honesta disponible — se declara `SIN-DATO-GENUINO` sin forzar ninguna.

## Nota sobre ADR

El repo usa ADRs numerados y sellados en `canon/gobernanza-v1_15.md`, pero cada uno documenta una **decisión firmada de mesa** (numeración derivada al sellar, ranura de firma verbatim). Este acto declara explícitamente `FIRMA: ninguna` — pregunta y propone, no decide. Sellar un ADR aquí falsificaría la forma del artefacto (un ADR sin firma de mesa no es un ADR, es una nota). Por eso este pase se registra como fila `FP-158` del tablero (`ABIERTA`, sin ADR) y como encargo `CONSUMIDO` en `forense/encargos/`, no como ADR — mismo patrón que otros actos de triage/propuesta sin firma (p. ej. `R34-BC-MECANISMO`, que tampoco sella ADR propio, solo propone).

## Qué no hizo este acto

No se re-especificó oficialmente ninguna ficha. No se midió nada ni se corrió ningún estudio real. No se tocaron las fichas del preregistro (`forense/hitoD-preregistro-v2_0.md`) ni el Registro de veredictos archivados. No se abrió ninguna vía en curso nueva — los bosquejos de arriba son propuestas para que mesa decida, no enmiendas firmadas.
