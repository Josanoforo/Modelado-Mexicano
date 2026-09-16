# ACTO `GEN2-CELDA-D-CAREO-1` · tres diseños ciegos, un careo, una celda registrada con su reserva intacta

**Encargo:** `forense/encargos/2026-09-17-GEN2-CELDA-D-CAREO-1-TRES-DISENOS-UN-CAREO.md` (archivado verbatim, A.3, sha256 del texto **tal como llegó** `f582ad38232e547d706e2ee6020184f2ddcccdb13fdddbc3ffc58f0ea78404f3`; las secciones `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` las añade la cascada después, por A.14, y el archivo lleva sufijo de tema por `forense/encargos/convencion.md` — encargo y nota del mismo tema colisionan en `T02`).
**Fecha nominal:** 17/sep/2026 (la de la firma de mesa y la del encargo) · **fecha de ejecución del entorno:** 2026-09-16. Las dos se conservan; no se infiere una firma futura ni se corrige una fecha que no es del ejecutor editar. Mismo tratamiento que `FP-377` y `NC-0274`.
**Base:** `9dffd64` (merge de `PR #823`), re-derivada al abrir — el encargo la declara y coincide: `git rev-list --count HEAD..origin/main` → `0`.
**Entorno (A.2, tres partes de una sola invocación):** `python3 tools/entorno.py --sonda-red` → `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` · `red=000` (el proxy de egreso responde 403 al CONNECT) · `corpus=NO(examinados=0)`, `data/raw` ausente. **Cero microdato, cero descargas, cero red efectiva.**
**Compuerta:** `ninguna`, declarada explícitamente por el encargo. `FP-376` gatea al piloto, no a este acto.

> **LO QUE ESTE ACTO NO HACE, y conviene leerlo antes que nada.** No abre microdato · **no deriva el cruce `localidad × edad` de ENIF 2024** — esa es la reserva de evaluación, y derivarla aquí la destruiría · no elicita `L` · no escribe `spec.yaml` · no firma `FP-376` · **no adjudica nada** · no toca el emisor ni el marcador. Contador de mediciones: **cero**, dicho sin disfraz.

---

## 0 · Qué entrega este acto, en cinco líneas

1. **P1** — las **87** citas `archivo:línea` de Astra resueltas en dos pasadas contra el árbol fijo `b881ee6`: **87 RESUELVEN, 0 NO-RESUELVE, 0 DICE-OTRA-COSA**. Sus tres fuentes externas quedan **SIN-FETCH** y no sostienen ninguna conclusión de este careo.
2. **P2** — el careo formal: los tres diseños contra los siete criterios, los tres hechos que lo decidieron re-ejecutados por comando, la reconciliación con atribución por hallazgo, y **16 modos de falla fundidos** en una sola tabla, cada uno cruzado contra `forense/hallazgos.md`.
3. **P3** — `NC-0275`…`NC-0279`, `FP-378` que **nace FIRMADA**, la fila de `decisiones.tsv`, las dos enmiendas fechadas, y **la primera celda-D del piloto registrada** (`celdas-d/` pasa de 3 a 4 archivos).
4. **P4** — la hoja del sucesor `GEN2-CELDA-D-PILOTO-1`, con entorno, orden de commits y compuertas.
5. **El hallazgo del careo que ninguno de los tres diseños traía solo:** en un universo donde el árbitro ya publicó todo lo que midió, la evaluación ciega no se encuentra — **se construye declarando reservada, antes de derivarla, una cantidad que nadie ha derivado todavía**. El orden del diff es el sello.

---

## 1 · P1 · Verificación del retorno de Astra (A.6)

### 1.1 · Las 87 citas al árbol fijo, en dos pasadas

Precedente: `ADR-530` (`ACTO GEN2-CROSSWALK-EJES-1`) re-verificó 31 citas; `ADR-532` (`#823`) corrió dos pasadas sobre 78. Aquí se hace lo mismo con el retorno externo, y por la misma razón: **la pasada 1 comprueba que la línea existe; no que sea la línea correcta.**

**Pasada 1 · mecánica.** Extrae del retorno toda cita con URL al árbol fijo y comprueba que la ruta existe en `b881ee6` y que el rango cabe en el archivo:

```
python3 - <<'PY'
import re, pathlib, subprocess
t = pathlib.Path('forense/notas/insumos-externos/celda-d-piloto/ASTRA-CELDA-D-DISENO-Y-ADVERSARIAL-b881ee6-v1_0.md').read_text()
pat = re.compile(r'\[([^\]]+?):([0-9]+)(?:-([0-9]+))?\]\(https://github\.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/([^#]+)#L([0-9]+)(?:-L([0-9]+))?\)')
rows = {(m.group(4), int(m.group(5)), int(m.group(6) or m.group(5)), m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))) for m in pat.finditer(t)}
...  # git show b881ee6:<ruta> | contar líneas; comparar también etiqueta contra URL
PY
```

Salida cruda:

```
TOTAL unicas=87  RESUELVE=87  NO-RESUELVE=0  etiqueta-discrepante=0
archivos distintos examinados = 22 de 22
```

Dos cosas que la pasada 1 comprobó y vale nombrar: **ninguna** de las 87 citas tiene la etiqueta desalineada de su URL (un modo de falla real: la etiqueta dice `:40` y el enlace apunta a `#L44`), y los conteos de líneas que Astra declara en su inventario coinciden con los del árbol — `propuesta-motor-adaptativo-celda-v0_3.md` 224, `v0_5` 159, `propuesta-motor-matriz-v0_1.md` 231, `tests/test_celdas_d.py` 296.

**Pasada 2 · semántica.** Para cada cita que sostiene una afirmación del retorno se abrió la línea con `git show b881ee6:<ruta> | sed -n <línea>p` y se juzgó si dice lo que el retorno afirma. **Resultado: 87 VERIFICADAS, 0 NO-RESUELVE, 0 DICE-OTRA-COSA.** Muestra de las que más peso cargan en este careo:

| cita @ `b881ee6` | qué afirma Astra | veredicto |
|---|---|---|
| `milpa/catalogo-momentos-v0_1.tsv:1-23` | «22 momentos, M01–M22, más cabecera» | **VERIFICADA** — 23 líneas, 1 cabecera + `M01`…`M22` |
| `data/corrida0/demanda-resultados.tsv:1-2` | la columna es `consumidor`, no `reglas_impacto` | **VERIFICADA** — cabecera: `resultado_id`, `consumidor`, `tipo`, … |
| `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:38` | la condición `INDECIDIBLE` verbatim vive ahí | **VERIFICADA** — `ADV1-M3`: *"si ambos caen dentro del IC de R"* |
| `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:34` | el grado `P0` va «fuera del marcador, a anexo de plomería» | **VERIFICADA** — `ADV1-M1(ii)` |
| `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:42` | el careo tiene consecuencia propia si ninguno vence a `b` | **VERIFICADA** — `ADV1-M5` casilla (4) |
| `milpa/tramite-ola5-propuesta-v0.yaml:1415-1427` | el desenlace y su definición | **VERIFICADA** — `:1426` es la línea de `definicion` |
| `milpa/tramite-ola5-propuesta-v0.yaml:1464-1473` | «el árbitro ya publica sus dos tasas por localidad e IC» | **VERIFICADA** — `<15 000` `p=0.409255` `n=4646`; `≥15 000` `p=0.329868` `n=8856` |
| `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv:10` | `localidad` es `MAPEO-N-A-1` y **sin firma** | **VERIFICADA** — y la regla de que una fila sin firma no autoriza consumo está en `:4` |
| `propuesta-motor-adaptativo-celda-v0_3.md:98-102` | `D8` es el mecanismo de coherencia conjunta | **VERIFICADA** — `D8` en `:102` |
| `forense/RONDA1-…-fable-…:68` | la multiplicidad se atiende contando patrones, no celdas | **VERIFICADA** |
| `milpa/src/theta.py:35-54` | «la ruta matricial no ejecuta θ» | **VERIFICADA** — `ThetaNoDisponible`, sin default silencioso |
| `milpa/src/matriz.py:138-160` | `g(x)=B·θ(x)` lanza `SinMagnitud` | **VERIFICADA** |
| `data/manifiesto.yaml:5500-5514` · `:5543-5558` | ENIF 2021 y 2024 registrados con archivo y sha | **VERIFICADA** — `enif_2021_enif_2021_bd_csv`, `enif_2024_enif_2024_bd_csv` |
| `data/corrida0/demanda-resultados.tsv:55` | `RES-0053` identifica la salida asignada | **VERIFICADA** — y su `escala_legacy` es `NO-DECLARADO-EN-EL-REGISTRO` |

**Una sola cita de las 87 corrigió algo, y no es de Astra sino de dirección.** El diseño v1.0 §2.2 C3 entrecomilla del contrato: *"gana o pierde esa celda por el mismo criterio que cualquier otro challenger"*. La línea real (`propuesta-motor-adaptativo-celda-v0_3.md:101`) dice **`criterio_adjudicacion`**, no «criterio». Es una comilla que parafrasea dentro de las comillas. No cambia el sentido y no mueve nada del careo; se registra porque una cita textual que no es textual es exactamente lo que estas dos pasadas existen para atrapar, y porque v1.0 es historia y no se edita. El diseño vigente v1.1 §2 C4 no repite el error: no entrecomilla.

### 1.2 · Las tres fuentes externas — **SIN-FETCH**, y ninguna sostiene nada

| fuente | uso que Astra le da | estado |
|---|---|---|
| Cawley & Talbot (2010), *On Over-fitting in Model Selection…*, JMLR 11:2079–2107 | §3.7 — selección como parte del ajuste; evaluación anidada | **SIN-FETCH** |
| Benjamini & Hochberg (1995), DOI `10.1111/j.2517-6161.1995.tb02031.x` | §3.2 — distinción FDR/FWER | **SIN-FETCH** |
| Hyndman & Athanasopoulos, *FPP3* §5.8 | §3.4 — separar error de evaluación y de ajuste; baseline comparable | **SIN-FETCH** |

**Sonda, con su A.13:** se probaron **5** URLs (`www.inegi.org.mx`, `doi.org`, `www.jmlr.org`, `otexts.com`, `rss.onlinelibrary.wiley.com`); `http_code` = `000` en las cinco; el proxy de egreso reporta `connect_rejected — gateway answered 403 to CONNECT`. Un negativo producido por un comando que sí ejecutó cinco intentos, no por «lo miré».

**Receta manual de un minuto** (para el primer acto con red, o para mesa):

```
curl -sL -o /tmp/cawley10a.pdf https://jmlr.org/papers/volume11/cawley10a/cawley10a.pdf   # §5-§6: sesgo de selección
curl -sL "https://doi.org/10.1111/j.2517-6161.1995.tb02031.x"                              # resumen: FDR ≠ FWER
curl -sL https://otexts.com/fpp3/accuracy.html                                             # §5.8: error de evaluación vs de ajuste
```

**Consecuencia declarada, y es la regla del propio encargo: nada `SIN-FETCH` sostiene una conclusión de este careo.** Las tres sostienen argumentos de Astra cuyo **estado en el contrato** se deriva aquí del corpus del repo (`v0.3`, `v0.5`, `RONDA1`, `CAREO-ADV-DUELO`), todo él verificado por comando. Lo que queda sin verificar es la **atribución bibliográfica** de tres argumentos, no los argumentos. Fila: `NC-0278`.

### 1.3 · Los dos errores del brief de dirección, que atrapó el externo

| afirmación del brief | realidad, por comando | dónde |
|---|---|---|
| «los **23 momentos** del catálogo» | **22** momentos `M01`–`M22`; 23 líneas = 22 + cabecera | `milpa/catalogo-momentos-v0_1.tsv:1-23` |
| «un consumidor identificado (**`reglas_impacto`** en la demanda)» | la columna se llama **`consumidor`**; `reglas_impacto` vive en `usos.tsv` | `data/corrida0/demanda-resultados.tsv:2` |

Van a `forense/hallazgos.md` como línea **A.13 de dirección**, con la lección escrita: un brief que exige `archivo:línea` a su destinatario debe derivar por comando las suyas. Ninguna de las dos mueve el veredicto — pero la primera pudo: si el brief hubiera pedido «la fila 23 del catálogo», el retorno habría descrito una fila que no existe.

---

## 2 · P2(a) · Los tres diseños contra los siete criterios

Los siete, como el brief los fija: **(a)** estimando con escala y universo declarados · **(b)** población expresable en cortes del modelo **y** en celdas del árbitro · **(c)** dato ya adquirido y en `data/manifiesto.yaml` · **(d)** ≥2 candidatos elegibles de familias distintas · **(e)** persistencia construible, o por qué no · **(f)** consumidor identificado · **(g)** partición de evaluación no vista por nadie.

| | **dirección v1.0** (ciego) | **Opus `#823`** (ciego) | **Astra** (ciego, externo) |
|---|---|---|---|
| universo barrido | 3 celdas-D · 7 entradas `_ejes_` · 22 momentos · 207 demandas · 15 filas de crosswalk · 22 ENIF del manifiesto | 3 celdas-D · 7 `_ejes_` (74 celdas, 64 con IC) · 22 momentos · 42 filas `conducta_p_medido` | 3 YAML completos · 207 demandas · catálogo completo · crosswalk · panel `F5` |
| **(a)** | pasa en la ganadora | **falla en 3 de 7**: `escala_legacy = NO-DECLARADO-EN-EL-REGISTRO` | pasa en el caso más cercano |
| **(b)** | pasa con 2 ejes mapeables (`formalidad`, `localidad`) | **falla en 6 de 7**: sólo `formalidad` tiene corte firmado (F-17), 6 de 74 celdas | `NE` en todas: «la fila de localidad no tiene firma» |
| **(c)** | pasa (5 olas ENIF en manifiesto) | pasa | pasa |
| **(d)** | pasa (≥3 familias) | **falla en la ganadora de dirección**: «sólo `L`» | `NE`/`F` en todas |
| **(e)** | pasa — *y es el punto que el careo derriba* | **falla**: `P5_6_6/7` ausentes en 2021; `P3_13` ausente en 2021 | «comparabilidad exacta previa `NE`» |
| **(f)** | pasa (`milpa/tramite.yaml:1306`) | pasa | pasa |
| **(g)** | pasa **con reserva declarada**: «ya vistas por dirección, no por `L`» | **falla en las 7 bajo lectura estricta**; y aun ignorándolo, ninguna pasa | **F**: «resultado publicado en el árbol» |
| **celda elegida** | **`dinero.ahorro.via_informal`** (`…v1_0…:47,49`) | **NINGUNA** (`…DISENO-CIEGO-1.md:331`) | **NINGUNA ACREDITADA** (`…ASTRA…:73`) |

**Lectura del careo.** Dos de tres dijeron «ninguna» y el tercero eligió una. **El careo no lo resuelve por mayoría: lo resuelve por comando**, y los comandos dan la razón a los dos que dijeron «ninguna» — pero sólo sobre la celda *tal como v1.0 la definió*. Los tres coinciden en algo más importante que el veredicto: **ninguno encontró una evaluación ciega**, y los tres lo dijeron por razones distintas que resultan ser la misma. Esa convergencia es lo que la firma de mesa acepta en su primera cláusula.

---

## 3 · P2(b) · Los tres hechos que decidieron el careo, re-ejecutados aquí

Ninguno se hereda de prosa. Los tres se corrieron en este acto, contra `9dffd64`, con su A.13.

### Hecho 1 · `P3_13` no existe en ENIF 2021 — y por eso sale `formalidad`

```
# sobre data/inventario-reactivos-v1_2.tsv, 178 256 líneas examinadas
filas enif2021                      → 1 607
filas enif2021 ∧ p3_13              → 0
filas enif2024 ∧ p3_13              → 4
```

Las 4 de 2024: los dos catálogos `…/catalogos/p3_13.csv` (`cve`, `descrip`), la columna en `conjunto_de_datos_tmodulo_enif2024`, y `TMODULO.csv:P3_13` en el ZIP de microdatos. **Encontrado por Opus (`#823` §1.7); re-verificado aquí.** Consecuencia: el único eje con corte del modelo firmado (`formalidad`, F-17) es justamente el que no se puede persistir. `formalidad` **sale** del piloto — no por preferencia, por ausencia de la variable en la ola anterior.

### Hecho 2 · `P5_6_6` y `P5_6_7` no existen en 2021 — y por eso el desenlace se redefine

```
catálogos p5_6_* en enif2021 → p5_6_1 p5_6_2 p5_6_3 p5_6_4 p5_6_5 p5_6_8 p5_6_9      (7)
catálogos p5_6_* en enif2024 → p5_6_1 … p5_6_9                                        (9)
catálogos p5_1_* en enif2021 → p5_1_1 … p5_1_6      (idéntico a 2024)
tloc, edad en enif2021       → presentes (TMODULO y TSDEM, con catálogo)
```

**Encontrado por Opus (`#823` §1.6); re-verificado aquí.** Consecuencia, y es la que el diseño v1.1 asume con la diferencia escrita: el desenlace se define sobre los **siete códigos comunes**, lo que lo convierte en **un estimando distinto del marginal del árbitro** (`milpa/tramite-ola5-propuesta-v0.yaml:1426` usa 1..9). Quien ahorra sólo por `P5_6_6/7` cuenta aquí como «sin vía formal». Es `EXISTE-NO-SATISFACE` respecto de la entrada del árbitro; la alternativa —definir por ola— rompería la persistencia, que es el piso del piloto. Va a mesa como punto 2 de v1.1 §7.

### Hecho 3 · El emisor copió al árbitro — y por eso el emisor sale de la competencia

```
ids `_ejes_` en milpa/tramite-ola5-propuesta-v0.yaml     → 7
  :1415 via_informal · :1600 util_sin_coercion · :1672 evasion_norma · :1993 denuncia.con_seguro
  :2041 union.libre  · :2089 reparto_mujeres40  · :2159 horizonte_corto
de esas 7, citadas dentro de milpa/tramite.yaml          → 6   (0 aciertos: horizonte_corto)
"copiada verbatim" en milpa/tramite.yaml                 → 12 líneas, 3 de ellas sobre entradas `_ejes_`
```

Desglose, que **afina** lo que el diseño v1.1 registró como «5 de 7»:

| entrada `_ejes_` | dónde vive dentro del emisor | forma de la copia |
|---|---|---|
| `util_sin_coercion` | `milpa/tramite.yaml:437` `segmentacion_ejes_encig2025` | `origen: … copiada verbatim` (`:441`) |
| `evasion_norma` | `:537` `segmentacion_ejes_envipe2025` | `origen: … copiada verbatim` (`:541`) |
| `via_informal` | `:708` `segmentacion_ejes_enif2024` | `origen: … copiada verbatim` (`:712`) |
| `union.libre` | `:1047` `segmentacion_ejes_eder2017_enadid2023` | celdas y `p` del árbitro, sin la etiqueta |
| `reparto_mujeres40` | `:1106` `segmentacion_ejes_enut2024` | celdas y `p` del árbitro, sin la etiqueta |
| `denuncia.con_seguro` | `:1004`/`:1026` (universo «copiado de la entrada …») | **el número**: `RES-0041 = 0.672` vs árbitro `0.672014` (`:2012`) |
| `horizonte_corto` | — | **sin rastro** (0 aciertos) |

**5 segmentaciones copiadas + 1 número idéntico + 1 sin rastro.** Encontrado por Opus (`#823` §1.5); re-verificado y afinado aquí. Consecuencia: el emisor sale de la competencia del piloto por razón **estructural**, no por la circularidad de una regla (`CORR-0009`) que v1.0 había supuesto. No es que `M` «haya visto» al árbitro: en cinco de siete, el árbitro **es** lo que `M` tiene escrito. Es el grado `P0` de `ADV1-M1` en su forma extrema —no «misma encuesta+ola», **mismo número**—, que el careo ya manda fuera del marcador (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:34`). Fila: `NC-0275`.

---

## 4 · P2(c) · La reconciliación, con atribución por hallazgo

El diseño vigente v1.1 §0 lista cinco cambios sobre v1.0. Quién encontró cada uno:

| # | v1.0 decía | hallazgo | **quién** | verificado en este acto |
|---|---|---|---|---|
| 1 | `formalidad` entre las celdas, con persistencia desde 2021 | `P3_13` no existe en ENIF 2021 | **Opus** (`#823` §1.7) | §3 hecho 1 — 0 filas 2021 / 4 filas 2024 sobre 178 256 |
| 2 | desenlace idéntico en las dos olas | `P5_6_6/7` no existen en 2021 | **Opus** (`#823` §1.6) | §3 hecho 2 — 7 códigos en 2021, 9 en 2024 |
| 3 | emisor excluido «por circular» | es **estructural**: el emisor copió al árbitro | **Opus** (`#823` §1.5) | §3 hecho 3 — 5 copias + 1 número + 1 sin rastro |
| 4 | (g) «declarable»: vistas por dirección, no por `L` | **quien selecciona las vio**, y partir la misma ola no la devuelve: el total publicado reconstruye la reserva | **Astra** (§1.2, §3.6, §3.7) | no requiere comando: es lógica, y es correcta |
| 5 | «23 momentos» y columna `reglas_impacto` | son **22**, y la columna es `consumidor` | **Astra** (§1.1) | §1.3 |
| **6** | — | **la reserva por interacción**: el árbitro sólo derivó **marginales**; las 8 celdas de **cruce** `localidad × edad` **nunca se han calculado** | **dirección** | `git grep -iE "localidad × edad\|reserva por interacci"` sobre `9dffd64` → **2** coincidencias, ambas del 12/ago sobre clustering de `R5.1`, **ninguna** sobre reserva de evaluación |

**Por qué (6) reconcilia (4) con la ausencia de ola nueva — y es lo único del careo que no venía en ninguno de los tres diseños.** Astra demostró que no se puede *encontrar* una evaluación ciega en este universo, y tiene razón: el árbitro publicó todo lo que midió, y partir la misma ola no devuelve ceguera porque el total publicado permite reconstruir la parte retenida. Opus llegó al mismo sitio por otro camino y nombró la única salida conocida —una ola posterior o retenida (`#823`, vía iii)—, que hoy no existe. La salida que el careo encuentra no es ninguna de las dos: **una cantidad que nadie ha derivado todavía es una reserva legítima, si y sólo si se declara reservada antes de derivarla.** Las 8 celdas de cruce son 8 números que no existen en ningún archivo del árbol; el selector conoce los marginales, no el cruce. Bajo la lectura estricta de Astra (el selector sólo conoce marginales) y bajo la vía (iii) de Opus (ola retenida en la persistencia), **(g) se cumple** — sin descargar nada y sin esperar a ENIF 2027.

**Y su falsador viaja con ella, escrito antes de correr:** si `R` se deriva antes de que las emisiones estén selladas, el piloto **no se anula — se degrada a factibilidad y se dice**. El orden del diff es el sello, y mesa lo audita. Va a `hallazgos.md` como `PARA-v2.14`.

**Dos precisiones honestas sobre el alcance de la reserva, para que nadie la lea de más:**

1. **Protege contra el doble uso del dato, no contra la exposición a los marginales.** Los marginales de `localidad` y `edad` son públicos y están sellados; el diseño v1.1 se los entrega a `L` **de propósito** (§2 C3), porque la pregunta del piloto es precisamente si `L` añade algo **sobre** los marginales. Ése es el papel de `C2`.
2. **No convierte al piloto en desempeño global.** Son 8 celdas, una encuesta, una ola. El diseño v1.1 §6 lo llama «desempeño **local**» y esa es la palabra correcta.

---

## 5 · P2(d) · Los modos de falla de los dos adversariales, fundidos

Astra entregó 16 secciones (§3.1–§3.16, la última es la pregunta de cierre, no un modo) y Opus 10 (`F1`–`F10`). Fundidos por **mecanismo**, no por numeración: **16 modos distintos**. Cada fila trae su procedencia, su estado en el contrato, el cruce contra `forense/hallazgos.md` y si el diseño vigente v1.1 lo atrapa.

Convención del cruce: **`YA-OCURRIÓ-AQUÍ`** = hay una línea de `hallazgos.md` que lo mide en este programa · **`CONCEBIBLE`** = no hay línea que lo mida · **`NO-APLICA`** = el mecanismo no puede darse en este piloto.

| # | modo de falla | procedencia | estado en el contrato | cruce contra `hallazgos.md` | ¿lo atrapa v1.1? con qué cláusula |
|---|---|---|---|---|---|
| 1 | **Selección post-hoc** del criterio o del candidato | Astra §3.1 · Opus `F1` | `YA-PREVISTO` como prohibición (`v0_1:117-119`), **`PREVISTO-SIN-MECANISMO`** como detección (`RONDA1:71`) | `CONCEBIBLE` | **Sí, y es la cláusula fuerte del diseño:** orden de tres commits con `COMMIT-1` congelado antes de abrir microdato y la frase de sello *«el primer resultado que produzca este procedimiento es el que se reporta»* (v1.1 §5). Es verificable **por historia de git**, no por confianza |
| 2 | **Multiplicidad** al adjudicar muchas celdas | Astra §3.2 · Opus `F2` | `YA-PREVISTO` en su forma «contar patrones, no celdas» (`RONDA1:68`); **la corrección fina quedó diferida** (`CAREO-ADV:26`, `:50`) | `CONCEBIBLE` | **Sí, para este tamaño:** familia de afirmaciones declarada (8 celdas × 2 challengers), **umbral de conteo y sin valor-p** porque las 8 celdas salen de una muestra y no son independientes (v1.1 §3). No resuelve la política masiva — y el diseño no pretende que sí |
| 3 | **Champions conjuntamente imposibles**; ¿basta `D8`? | Astra §3.3 · Opus `F3` | **`PREVISTO-SIN-MECANISMO`** — `D8` pide cierre global y signos (`v0_3:98-102`), pero `momentos_holdout_refs` está vacío en las 3 celdas-D previas y `milpa/src/momentos.py:130` levanta `NotImplementedError` | `CONCEBIBLE` como incoherencia consumada; `YA-OCURRIÓ-AQUÍ` en su precondición: `forense/hallazgos.md:480` (*un `C` que pasa por ausencia de mecanismo*) | **No aplica todavía, y se dice:** con una sola celda-D del piloto no hay dos champions que puedan contradecirse. Lo que v1.1 **sí** hace es dejar de vaciar la reserva: es la **primera** celda-D con `momentos_holdout_refs` no vacío. La observación de Astra —signos opuestos **no** son contradicción si son β(x) de poblaciones distintas; el test debe comparar el mismo `parametro_compartido_id`— queda **abierta y sin dueño** |
| 4 | **Persistencia imbatida** y presión por fabricar valor añadido | Astra §3.4 · Opus `F4` | `YA-PREVISTO` con consecuencia propia (`CAREO-ADV:42`, casilla `ADV1-M5(4)`); mismo universo exigido (`TRIADA-B-PISO:59-67`) | **`YA-OCURRIÓ-AQUÍ`** — `forense/hallazgos.md:838`: `b` yerra menos que el modelo en **8 de 10** celdas (`MAE 0.885` vs `M 4.638`) | **Sí, y por adelantado:** v1.1 §3 declara **antes de correr** qué significa que nadie venza a `C1` (persistencia corroborada como piso en DIN) y qué significa que nadie venza a `C2` (la interacción no aporta información explotable a este `n`). Las dos son resultados del programa, no fracasos del piloto |
| 5 | **Ajuste clandestino al árbitro** | Astra §3.5 · Opus `F5` | `YA-PREVISTO` como prohibición y secuencia (`matriz-v0_1:128-130`, `CAREO-ADV:36`); **verificación de acceso limitada** | **`YA-OCURRIÓ-AQUÍ` en la forma que lo hace invisible** — `forense/hallazgos.md:837`: una anotación semántica correcta para una fuente es falsa para la de al lado, y el rótulo no avisa | **Sí, en su forma extrema, y por eso el emisor sale:** §3 hecho 3. Lo que v1.1 añade es que la reserva hace la fuga **verificable por el orden del diff**, no sólo prohibida |
| 6 | **Una ola calibra y evalúa** (circularidad) | Astra §3.6 · Opus `F6` | `YA-PREVISTO en principio` (`RONDA1:65`, `v0_2:80-81`), **`NO-PREVISTO` en la celda-D**: el contrato no tiene dónde declarar dependencia del árbitro | **`YA-OCURRIÓ-AQUÍ`** — `forense/hallazgos.md:838` y `:829` (`B` no podía hablar en 2 de 3 objetivos: disponibilidad, no persistencia) | **Sí, y es su aportación central:** la reserva por interacción (§4). `C1` sale de **otra ola** (2021); `R` sale de un cruce **no derivado**; el emisor —que es el árbitro— **sale de la competencia** |
| 7 | **El holdout usado para elegir deja de ser prueba final** | Astra §3.7 | **`PREVISTO-SIN-MECANISMO inequívoco`** — el doble uso se nombra (`RONDA1:65`), pero evaluar el criterio sobre el holdout no distingue selección de evaluación | `CONCEBIBLE` | **Parcialmente, y la parte que falta está declarada:** las 8 celdas **no se eligen aquí** —son el cruce completo de dos ejes que el árbitro ya selló—, así que no hay mínimo sobre el que optimizar. Lo que **no** cubre: el selector conoce los marginales. Por eso `C2` existe |
| 8 | **Mezcla de banda, punto y distribución** al componer | Astra §3.8 · Opus `F7` | **`PREVISTO-SIN-MECANISMO`** — `RONDA1:101` exige dry-run sin colapsar banda→punto, los tipos están enumerados (`v0_1:121-133`), pero no hay operador de despacho por tipo | **`YA-OCURRIÓ-AQUÍ` en la clase** — `forense/hallazgos.md:841`: cambiar la unidad de un techo sin re-dimensionarlo lo convierte en otro techo | **No se le presenta:** los cinco candidatos de v1.1 emiten **proporción `[0,1]`**, y §4 tipa la incertidumbre **por candidato** (IC muestral / IC propagado / intervalo de elicitación), prohibiendo la banda universal. Es evitación, no mecanismo — y el diseño no pretende otra cosa |
| 9 | **Dependencia entre celdas** e IC marginales combinados como independientes | Astra §3.9 | **`PREVISTO-SIN-MECANISMO`** — grafo de fuentes detecta sensibilidad, no sustituye covarianzas (`RONDA1:66`) | `CONCEBIBLE` | **Sí, y explícitamente:** v1.1 §3 dice que las 8 celdas salen de una misma muestra, **no son independientes**, y por eso **no hay valor-p** y el umbral es de conteo. `C2` propaga bajo independencia y **lo declara como supuesto del candidato**, no como propiedad del dato |
| 10 | **Extrapolación fuera de soporte** en celdas chicas | Astra §3.10 · Opus `F8` | **`PREVISTO-SIN-MECANISMO genérico`** — hay declaración de transporte (`v0_3:72`), no una máscara ejecutable de soporte | `CONCEBIBLE` | **Sí, con umbral y con su reserva:** v1.1 §4 fija `n_2021 < 200` = fuera de soporte, verificado en `COMMIT-1` con los marginales del FD y sin abrir microdato; `n` esperado mínimo ≈ 980. La objeción de Astra —no fijar un `n` mínimo universal desconectado de la pérdida— **queda en pie**: 200 es convención, no derivación |
| 11 | **Falsa desagregación del árbitro** (invertir una media gruesa en celdas finas) | Astra §3.11 | **`NO-PREVISTO`** en `v0.3`/`v0.5`/`RONDA1` como mecanismo de inversión (búsquedas `N-a-1`, `desagreg`, `inversa`) | `CONCEBIBLE` — el crosswalk (`:10`) declara la pérdida, y por eso hoy no es cosmético | **Es exactamente lo que `C2` hace — y por eso `C2` es un piso, no un challenger.** `p̂(l,e)=p̂(l)·p̂(e)/p̂` **es** la inversión que Astra describe; el diseño no la disfraza de heterogeneidad medida: la declara supuesto de independencia y la pone a competir. **La mejor respuesta a §3.11 que el careo produjo, y no la produjo Astra sino la estructura del piloto** |
| 12 | **Universos o constructos distintos bajo la misma escala** | Astra §3.12 | `YA-PREVISTO` — el contrato separa constructos y añade universo/escala (`v0_3:84-86`) | **`YA-OCURRIÓ-AQUÍ`** — `forense/hallazgos.md:842`: tres números llamados «cobertura» eran tres cantidades; y `:421`: empalmar una serie por nombre de variable pega dos cosas distintas sin error visible | **Sí, y es el hecho 2 aplicado:** v1.1 §1 declara que el desenlace de siete códigos **no es el mismo estimando** que el marginal del árbitro, con la diferencia escrita, y lo lleva a mesa. La restricción de universo de `formalidad` que v1.0 arrastraba desapareció al salir `formalidad` |
| 13 | **Escala sin función de enlace** al llegar al consumidor | Opus `F9` | `YA-PREVISTO en la celda-D`, **`NO-PREVISTO` aguas abajo** | **`YA-OCURRIÓ-AQUÍ`** — `forense/hallazgos.md:842`; y **medido hoy**: **15 de 42** filas `conducta_p_medido` traen `escala_legacy = NO-DECLARADO-EN-EL-REGISTRO`, entre ellas `RES-0057`/`RES-0058`, **el consumidor de este piloto** | **Sí dentro de la celda** (una sola escala, proporción `[0,1]`, en los cinco candidatos y en `R`), **no aguas abajo**: el consumidor sigue sin escala declarada en el registro. Fila abierta hoy: `NC-0276` |
| 14 | **Elegir por disponibilidad** y borrar los `SKIP` | Astra §3.13 | `YA-PREVISTO` — universo de candidatos, indecidibles y conteo visible (`v0_3:48`, `v0_5:51-59`, `CAREO-ADV:40`) | `CONCEBIBLE` | **Sí:** el universo es el **cruce completo** 2×4, no una selección; el umbral exige `≥6` de `8` `PUNTUADA` y `<6` obliga a reportar factibilidad con su conteo. El control de memoria puede vaciar celdas y **eso se publica**, no se esconde |
| 15 | **Costo del contrato** — cuántas celdas se pueden adjudicar | Astra §3.14 · Opus `F10` | **`PREVISTO-SIN-UMBRAL`** — `RONDA1:98-105` pide horas/celda; `v0_3:193` acepta umbrales de piloto; ninguno fija cuántas adjudicaciones valen lo que cuestan | `CONCEBIBLE` | **No lo resuelve, y no le toca:** v1.1 adjudica **una** celda. Astra lo cuantifica sin adornos: con los siete criterios hay **0 celdas inmediatamente certificables**, y el número tras resolver reservas es **no estimable** con estos metadatos. Este acto añade el primer dato duro del denominador: `celdas-d/` = **4** archivos, **0** adjudicadas |
| 16 | **Banda ancha que siempre solapa `R`** = falsa precisión decisional | Astra §3.15 | **`PREVISTO-SIN-MECANISMO universal`** — `RONDA1:67` admite empate sin adjudicación, `v0_5:61-69` abre `margen_material`; no hay operador intervalo→acción | `CONCEBIBLE` | **Sí, en la forma más fuerte disponible:** v1.1 §4 separa compatibilidad de utilidad — **emitir ≠ decidir** — y define «estable» / «ambigua» por el **signo de la modulación** respecto del nacional, que es la pregunta del consumidor real (`milpa/tramite.yaml:1306`). Y `C3` (`L`) no entrega un IC: entrega un **intervalo de elicitación**, cuya cobertura empírica **se mide**, no se supone |

### 5.1 · El saldo de la tabla

- **`YA-OCURRIÓ-AQUÍ`: 6 de 16** (filas 4, 5, 6, 8, 12, 13). Ninguno es hipotético: los seis tienen una línea de `hallazgos.md` que los mide en este programa.
- **`PREVISTO-SIN-MECANISMO` o peor: 9 de 16.** El contrato nombra casi todo y ejecuta poco: es el mismo saldo al que llegaron los dos adversariales por separado.
- **`NO-PREVISTO`: 1** (fila 11, falsa desagregación) — y el diseño v1.1 lo convierte, sin proponérselo, en un **candidato declarado** en vez de un defecto silencioso.
- **El diseño v1.1 atrapa 12 de 16 con cláusula citable.** De los 4 restantes: uno no se le presenta (8), uno no le toca (15), uno queda abierto y **sin dueño** (3, el `parametro_compartido_id` de Astra), y uno queda abierto **con dueño y con fila** (13, `NC-0276`).
- **Lo que la tabla no compra:** que un modo esté «atrapado» significa que el diseño tiene una cláusula que lo detectaría, no que el mecanismo exista ejecutado. Cinco de los doce se atrapan por **evitación** (no se le presenta el caso) y no por mecanismo. Eso es honesto para un piloto de una celda y sería insuficiente como política de motor.

### 5.2 · La pregunta de cierre de los dos adversariales

Astra (§3.16) y Opus (cierre de `P3`) llegan al mismo sitio por caminos distintos, y conviene dejarlo escrito porque es lo que mesa firmó al precisar el alcance de `ADR-91`:

> Para quien lee salidas **por celda**, «cada celda su estimador» puede ser **peor** que «un estimador único con etiqueta» —pero sólo por tres vías, y las tres son de **interfaz**, no de estimación: selección post-hoc y multiplicidad (filas 1-2), incoherencia de parámetros compartidos (fila 3), y manejo desigual de soporte, escala e incertidumbre (filas 10, 12, 13, 16). Un estimador único no cura ninguna de las otras: la fuga de `R`, los denominadores incompatibles y la falta de soporte lo dañan igual, y además le impone una escala y un sesgo a todas las celdas. **La comparación justa es política completa contra política completa, con la selección contada como parte del método.** Lo que debe ser común no es el estimador: es el **contrato semántico** y el **criterio de comparación**.

Este piloto es el primer caso donde esa afirmación se puede empezar a medir en vez de discutir.

---

## 6 · P2(e) · Módulo de auditoría de rigor extremo

Este artefacto **afirma sobre el modelo** y sobre un estimando de conducta de población mexicana. El módulo va completo.

**1 · ¿Qué parte del análisis podría estar confundiendo pobreza, desigualdad, violencia o falta de acceso con «cultura» o «psicología»?** El estimando entero es candidato. `ahorra_solo_informal` condicionado a `localidad` y `edad` mide **quién ahorra por vías informales y por ninguna formal** — y la lectura fácil («el rural prefiere la tanda») confunde una restricción de acceso con una preferencia. El árbitro ya registró la asociación como **ASOCIACIÓN, no efecto** (A-bis 1), y el piloto **no atribuye mecanismo**: mide una proporción condicionada y compara estimadores. El eje `localidad` es estructural (tamaño de localidad), no actitudinal. **Lo que este acto no puede impedir** es que el número se lea como preferencia cultural cuando salga; por eso queda escrito aquí y en la celda registrada.

**2 · ¿Qué parte podría estar sobregeneralizando desde clases medias urbanas?** Menos que v1.0, y por una razón medible: al salir `formalidad` (hecho 1) sale también su universo restringido a quien trabaja (cobertura `0.689676`), que sobre-representaba por construcción a quien tiene empleo formal. El cruce vigente `localidad × edad` **incluye** `<15 000` habitantes como mitad del eje, con `n` esperado mínimo ≈ 980 en la celda más chica. **Pero ENIF es una encuesta de viviendas particulares con marco urbano-rural del FD**: no cubre población en viviendas colectivas, ni localidades por debajo del corte de muestreo del propio diseño.

**3 · ¿Qué parte está sesgada por literatura escrita desde marcos estadounidenses o europeos?** Dos lugares, y los dos están declarados. (i) `C3` en su variante `L+corpus` hereda el sesgo del corpus `F5`, que es lo que la variante existe para medir: la comparación `L-solo` vs `L+corpus` **es** el test de si el corpus ayuda o estorba. (ii) Las tres fuentes externas de Astra (Cawley-Talbot, Benjamini-Hochberg, Hyndman-Athanasopoulos) son metodología anglófona — y por eso quedan `SIN-FETCH` **y sin sostener ninguna conclusión** (§1.2). Ningún marco teórico importado entra al estimando: el desenlace se define por códigos de un cuestionario del INEGI, no por un constructo traducido.

**4 · ¿Qué hallazgos cambiarían si el foco fuera México rural, indígena o popular?** El cruce incluye lo rural por construcción, pero **no lo indígena**: ENIF no aporta un eje de adscripción en el crosswalk y este piloto no lo añade. Si el foco fuera ése, `C2` (marginales + independencia) sería el primer candidato en romperse: la interacción entre condición étnica y acceso financiero no es plausible que factorice. Es una predicción, no un resultado, y se escribe como tal.

**5 · ¿Qué parece psicológico pero en realidad es un incentivo racional ante un entorno concreto?** Ahorrar sólo por vías informales, con alta probabilidad. Tanda, guardadito y préstamo entre conocidos tienen costos de transacción, requisitos documentales y distancias muy distintos de los de una cuenta bancaria. **El piloto no distingue preferencia de restricción y no puede hacerlo**: mide una proporción, no un mecanismo. Nombrarlo aquí es lo único que el acto puede hacer al respecto.

**6 · ¿Dónde hay evidencia débil pero intuición social fuerte?** En el signo esperado de la interacción. «Los jóvenes rurales ahorran informal más que nadie» es intuitivamente fuerte y **no está medido**: son precisamente las 8 celdas reservadas. El diseño **no pre-registra un signo esperado para la interacción**, y hace bien: pre-registrarlo sobre una intuición sería el modo de falla 1 de la tabla con otro nombre.

**7 · ¿Qué conclusiones serían peligrosas si alguien las usara de forma simplista?** Tres, en orden de daño. (i) *«Sin seguridad social se ahorra más informal → preferencia cultural»* — el propio árbitro lo registró como asociación; y además `formalidad` **ya no está en el piloto**. (ii) *«`L` le ganó a la persistencia → el LLM sabe de México»*: el careo prohíbe la palabra «supera» (`ADV1-M4`) y el piloto declara `INDECIDIBLE` antes de mirar el dato. (iii) *«La matriz quedó `INEJECUTABLE` → el motor no sirve»*: `C4` dice que **hoy no puede presentarse a esta celda** y nombra sus cuatro faltantes; no dice nada sobre el motor como arquitectura, y `ADR-91` sigue en pie con el alcance que `ADR-531` le precisó.

**8 · (v2.1) ¿Qué afirmación de este artefacto describe el estado del corpus —un conteo, una ausencia, un «no existe»— y fue escrita a mano en vez de derivada por comando?** **Ninguna.** Los conteos de esta nota traen su comando y su A.13: 87 citas sobre 22 archivos · 178 256 líneas del inventario · 7 entradas `_ejes_` · 6 citadas en el emisor · 15 de 42 filas `conducta_p_medido` sobre 209 líneas · 3→4 archivos en `celdas-d/` · 5 URLs probadas · 5 256 archivos rastreados por la búsqueda de reserva. **Una discrepancia declarada:** la verificación de existencia del encargo dice que la búsqueda de `localidad × edad|reserva por interacci` corrió «sobre 2 262 archivos»; al re-derivarla aquí, el árbol `9dffd64` tiene **5 256** archivos rastreados. El **veredicto** reproduce exacto —2 coincidencias, ambas del 12/ago sobre clustering de `R5.1`, ninguna sobre reserva de evaluación—; el **denominador** no. Se reporta, no se copia.

**9 · (v2.2) Deudas asumidas que caducan al cambiar la función del programa.** Dos. (i) El umbral de soporte `n < 200` es convención heredada, no derivación desde la pérdida del consumidor: si el consumidor cambia, el umbral debe re-derivarse, y la objeción de Astra (§3.10) ya lo dice. (ii) La definición por **siete códigos comunes** compra persistencia al precio de un estimando distinto del marginal del árbitro: si el programa dejara de necesitar persistencia, esa deuda deja de pagar y debería revertirse a la definición de 1..9. Las dos están en v1.1 §7, camino a mesa.

**10 · (v2.4) Si este artefacto contiene una cantidad estimada: ¿en qué escala está, y contra qué se compara?** Este artefacto **no produce ninguna cantidad nueva del modelo**. Las cifras que reproduce son del árbitro ya sellado (`p=0.409255` y `p=0.329868` por localidad; `0.672014`/`0.790906` de `denuncia.con_seguro`) o del emisor ya registrado (`RES-0041 = 0.672`), y se reproducen **para nombrar entradas y probar una identidad**, no para comparar ni para adoptar. Todas están en la misma escala: **proporción ponderada `[0,1]`**. Ninguna comparación de esta nota cruza escalas. Contadores del programa movidos por medición: **cero**.

---

## 7 · P4 · Hoja del sucesor · `GEN2-CELDA-D-PILOTO-1` (esqueleto)

**Esto es un esqueleto, no el encargo.** Dirección lo redacta tras este merge; aquí quedan sólo las decisiones que este acto ya fijó y que el sucesor no debe volver a discutir.

- **ENTORNO: CAJA** (Ubuntu). Abre ENIF **2021** y **2024**. Todo acto que abra microdato va a caja, sin excepción.
- **MODELO SUGERIDO:** Opus. **VEHÍCULO:** `/acto`.
- **COMPUERTA:** (1) el merge de este acto; (2) la firma de los **tres puntos de v1.1 §7** — `FP-376` (sólo para que el **marcador** consuma la celda; el piloto puede correr sin ella), la **definición por siete códigos comunes**, y la **admisión de `C2`** como segundo piso.
- **CELDA:** `DIN.ahorro_solo_informal.enif2024.localidad_x_edad`, ya registrada por este acto.

**TRES COMMITS, MÍNIMO Y EN ESTE ORDEN. El orden del diff es el sello.**

1. **`COMMIT-1` · spec congelada, sin abrir microdato.** Variables y **códigos leídos del FD de cada ola** (`enif2021_fd_zip`, `enif2024_fd_xlsx` del manifiesto); los **siete códigos comunes** `P5_6_{1,2,3,4,5,8,9}`; `tloc` y `edad` verificados **por archivo** en las dos olas (A.15c); universo (personas 18+ elegidas, `TMODULO`); ponderador `FAC_PER`, `EST_DIS`/`UPM_DIS`; el cruce 2×4; la dicotomización; `seed 42`; tolerancias; verificación de soporte `n_2021 ≥ 200` con los marginales del FD. **Frase de sello, verbatim:** *«el primer resultado que produzca este procedimiento es el que se reporta»*.
2. **`COMMIT-2` · emisiones selladas.** `C1` (persistencia 2021), `C2` (marginales + independencia) y `C3` (`L` en sus dos dietas, elicitación ciega con control de memoria) como `RESULT` GEN2 con cadena completa (E.2). **`R` no existe todavía en el árbol al cerrar este commit.**
3. **`COMMIT-3` · `R` y adjudicación.** Derivación de las **8 celdas de cruce** con la misma receta que el árbitro marginal, y adjudicación por celda con las dos condiciones `INDECIDIBLE` **verbatim**. `C4` se asienta `INEJECUTABLE` con sus cuatro faltantes nombrados. `C5` se cuantifica como diagnóstico.

**Parada.** *Factibilidad* si `C1`/`C2` calculados con cadena GEN2, `C3` elicitado y puntuado, `C4` asentado, `C5` cuantificado, adjudicación por celda escrita, **una entrada del catálogo de momentos poblada** con estimador adjudicado (hoy 22 de 22 `NO-VERIFICADO`) y el consumidor la lee sin cambiar código. *Desempeño local* sólo bajo v1.1 §3, y con la reserva de que son 8 celdas, una encuesta y una ola.

**El falsador del propio piloto, escrito antes de correrlo:** un `R` derivado antes del `COMMIT-2` **no anula** el piloto — lo **degrada a factibilidad**, y eso se declara, no se esconde.

**Lo que el sucesor hereda abierto:** `NC-0275` (emisor = árbitro, sucesor `SIN-ASIGNAR`) · `NC-0276` (15 filas sin escala, entre ellas su propio consumidor) · `NC-0278` (tres fuentes `SIN-FETCH`) · `NC-0280` (la lección de perímetro: un acto que archiva texto de terceros dispara `T02`/`T22`/`T25`/`T30`, y su perímetro debería decirlo) · la fila 3 de la tabla de §5 (`parametro_compartido_id`, sin dueño) · `FP-376` abierta.

---

## 8 · Re-verificación de las citas de esta nota, antes de cerrar

Precedente: `ADR-530` (31 citas), `ADR-532` (78 citas en dos pasadas). Esta nota corre lo mismo sobre sí misma.

**Pasada 1 · mecánica.** Extrae del propio archivo toda cita `` `ruta:línea` `` y comprueba que exista esa línea. Salida cruda:

```
CITAS `archivo:linea` DISTINTAS EN LA NOTA: 34 sobre 12 archivos -- 34 resuelven, 0 no
```

**Método, dicho porque el primer intento falló.** La primera corrida devolvió **9 FALLA**, todas de la misma clase que `#823` ya había pagado: citas en forma corta, con sólo el nombre base (`hallazgos.md`, `tramite.yaml`, `momentos.py`, `CAREO-ADV-DUELO…`), que un lector humano resuelve por contexto y un comando no. Se normalizaron a ruta completa **antes** de cerrar. Es exactamente la clase de defecto que esta pasada existe para atrapar.

**Pasada 2 · semántica.** Se abrió cada una de las 34 líneas y se comprobó que diga lo que la nota afirma. **34 PASA, 0 FALLA.** (El conteo subió de 31 a 34 al escribir esta misma sección: sus tres citas de ejemplo también cuentan. La pasada se corrió otra vez después, no antes.)

**Una reserva de método que la pasada 2 destapó, y vale más que las 34 juntas.** Las citas de la tabla de §1.1 son **@ `b881ee6`** —el árbol fijo del encargo externo— y el resto de la nota cita **@ `9dffd64`**. Una de ellas **se mueve entre los dos árboles**: `milpa/src/matriz.py:138-160` es exactamente `def g(matriz, theta, celda):` … `return salida` en `b881ee6`, y en `9dffd64` la línea 138 es `def g(matriz, theta, celda, generadores=None):` —`ADR-531` cambió la firma— y la 160 está en blanco. La cita de Astra es **correcta en su árbol y falsa en el de hoy**, y un verificador que no distinga los dos árboles la aprueba o la rechaza por el motivo equivocado. Es la misma reserva que `#823` dejó escrita sobre `milpa/tramite.yaml:712`, que cita `milpa/tramite-ola5-propuesta-v0.yaml:1162-1346` cuando la entrada vive hoy en `:1415-1599`: **una cita por línea sin SHA no es una cita, es una coordenada sin origen.** Resuelve por `id`, no por línea. No se abre fila nueva —`#823` ya la dejó como reserva al cierre— y se nombra aquí porque este acto la volvió a pisar con un archivo distinto.

---

## 9 · Universo de la estampa (A.10) y contador

**SHA:** `9dffd64`. **Instrumentos:** ninguno abierto — este acto no toca microdato. **Celdas:** las 8 de cruce, **no derivadas**. **Archivos leídos con comando y citados:** 22 del árbol fijo `b881ee6` (P1) + `data/inventario-reactivos-v1_2.tsv` (178 256 líneas), `milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.yaml`, `data/corrida0/demanda-resultados.tsv` (209), `forense/hallazgos.md`, `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`, `tests/test_celdas_d.py`, `data/INFRAESTRUCTURA-v1_0.md`.

**CONTADOR.** Mediciones: **0**. Corridas: **0**. Adopciones: **0**. Microdato: **0**. Red efectiva: **0** (5 intentos, 5 rechazos de política). Celdas-D registradas: **3 → 4**. `no_corrido_abiertas`: **+7** (`NC-0275`…`NC-0281`) — **el encargo previó +2**, y la diferencia son las cuatro filas A.14 propias de este acto: adjunto que no llegó, fuentes `SIN-FETCH`, enmienda que ya existía, **el perímetro mal calculado** (`NC-0280`: el encargo autorizaba tocar `tests/check.py` sólo por `T25` y el acto disparó cuatro tests de cascada — `T02`, `T22`, `T25`, `T30` —, que es lo que archivar cuatro adjuntos verbatim y abrir una fila de mesa dispara por construcción), y **la línea base en rojo sin congelar** (`NC-0281`, §10). Se reporta, no se ajusta el conteo al pronóstico. **De las siete, dos cierran en este mismo acto:** `NC-0277` (mesa cargó el adjunto al leer el reporte) y `NC-0281` (la línea base cierra **VERDE** por esa misma vía, sin recongelar nada). Quedan **5 abiertas**. `FP` abiertas: sin cambio (`FP-378` **nace FIRMADA**). Filas de `decisiones.tsv`: **+1**.

---

## 10 · Suite de cierre · la línea base cierra VERDE, porque mesa tomó la vía (a)

**Este apartado se escribió dos veces, y las dos versiones son parte del registro.** La primera reportó `LÍNEA BASE ROJO` con 9 entradas nuevas y puso la decisión a mesa. **Mesa respondió cargando los dos adjuntos que faltaban, en la misma sesión** — la vía (a) de `NC-0281` —, así que no hubo nada que congelar. Se deja dicho cómo se llegó aquí porque el camino es el hallazgo, no sólo el número final.

### 10.1 · Lo que se reportó, y lo que pasó después

| corrida | cifra | línea base | qué la movió |
|---|---|---|---|
| cierre (1ª) | `3 FAIL · 4364 WARN` | ROJO, 5 nuevas | el acto archivó 4 adjuntos verbatim que citan dos documentos ausentes |
| tras escribir el reporte | `3 FAIL · 4373 WARN` | ROJO, 9 nuevas | **nombrar los dos ausentes para reportarlos** creó 5 referencias colgantes más |
| tras compactar la cita cruda | `3 FAIL · 4370 WARN` | ROJO, 9 nuevas | los nombres **truncados** que la salida imprime tampoco existen |
| **mesa carga los dos adjuntos** | **`3 FAIL · 4360 WARN`** | **VERDE** | 8 de las 9 se cierran solas; la novena era otra cosa (§10.3) |

### 10.2 · Los dos adjuntos, archivados con su sha verificado

| documento | sha256 declarado | verificado por comando | dónde quedó |
|---|---|---|---|
| `D-THETA-DOCUMENTO-v1_1-post-adversarial.md` | `8a6472a72631dfdc…` | `8a6472a72631dfdcfbcd7be50db5760a214614e15b6afff9f862999ebf1e061d` ✔ | `forense/notas/insumos-direccion/` |
| `ADVERSARIAL-D-THETA-v1_0.md` | `850f9cefe4334acd…` | `850f9cefe4334acd679d7eaa38eceafa4da19d903bd38997f448534b32d082e7` ✔ | `forense/notas/insumos-externos/celda-d-piloto/` |

El sha del adversarial merece una línea: **es el que Astra declaró en su propio retorno**, sin que nadie pudiera cotejarlo contra el archivo. Al llegar el archivo, **coincide byte a byte**. Es la única afirmación de procedencia que el externo hizo sobre un objeto que no estaba en el árbol, y cuadra.

`D-THETA-DOCUMENTO-v1_1-post-adversarial.md` llegó **al tercer intento**: `#822` P5 lo dejó `NO-CORRIDO` (`NC-0271`), el lanzamiento de este acto tampoco lo trajo (`NC-0277`), y mesa lo cargó al leer el reporte. **`NC-0277` queda `CERRADA`** por este mismo acto. **`NC-0271` sigue `ABIERTA` y se dice por qué**: su premisa está resuelta —es exactamente el sucesor que ella nombra, «*dirección re-envía el adjunto y un acto de trámite lo archiva con cabecera de procedencia tipo 3*»—, pero su columna enumera **dos** piezas, y la segunda (la nota corta sobre reformular el piloto de D-θ como celda-D completa) es sustancia de `#822`, no de este acto. **Se cierra la premisa, no la pieza.**

### 10.3 · La novena entrada era otra cosa, y se declara en vez de pedirla

Archivar los dos cerró **8** de las 9. La novena apareció al hacerlo: el adversarial de Astra cita `D-THETA-DOCUMENTO-PARA-ADVERSARIAL-v1_0.md` — **la v1.0 de D-θ, el documento que él revisa**, que nunca viajó al árbol y que está **derogado por su propia sucesora**: la v1.1 abre diciendo «*la v1.0 se conserva como historia; esta v1.1 la sucede*», y es la v1.1 la que quedó archivada.

Pedírsela a mesa sería pedir historia derogada para cerrar una cita; fabricarla sería inventar procedencia. Se usa el mecanismo que el propio test documenta —`_T03_DEPENDENCIAS_PENDIENTES`, con la razón escrita, mismo patrón que `NC-0219`— para el adversarial (archivado **verbatim**, que no se edita) **y para los dos archivos donde este acto la nombra al explicar por qué cuelga**. Nombrar un archivo ausente para reportar su ausencia es lo que `T03` no sabe distinguir de citarlo esperando leerlo, y ése es el hallazgo reflexivo de §10.4: se usa el mecanismo documentado en vez de callar el nombre.

### 10.4 · El hallazgo reflexivo, que sobrevive al cierre en verde

**Reportar una ausencia crea la referencia colgante que se está reportando.** `T03` no distingue «cita un archivo que esperaba leer» de «nombra un archivo para decir que nunca llegó». Se midió al chocar con el punto fijo, dos veces (tabla de §10.1). La salida no es callar el nombre —escribir un informe de ausencia sin nombrar lo ausente, para que un test no lo cuente, es escribir para complacer al test, justo lo que la regla de los encargos verbatim protege— sino nombrarlo y declarar la dependencia con su razón.

**Y hay una segunda lección, más barata:** el adjunto que no viaja no es intendencia. Costó **9 `WARN`**, puso la línea base en rojo, obligó a un PARO-reporte y estuvo a punto de gastar una autorización de recongelado de mesa. Llegó, y se disolvió solo. `NC-0277` lo dice con fecha.

### 10.5 · Cifra final

```
════════════════════════════════════════════════════════════════════════
  3 FAIL · 4360 WARN
════════════════════════════════════════════════════════════════════════
  LÍNEA BASE: VERDE contra tests/baseline.json (HEAD congelado 5e2ad5ce…)
```

**Cero `FAIL` nuevos y cero entradas nuevas.** Los 3 `FAIL` son los heredados del corpus documental (`T06`×2, `T08`), ajenos a este perímetro y presentes en `tests/baseline.json`. **`tests/baseline.json` no se tocó** — y ése era el punto: la línea base cierra verde **sin recongelar nada**, que es siempre el mejor de los dos desenlaces que `NC-0281` ponía a mesa.

`python3 tests/test_celdas_d.py` → `4 archivo(s) de celda-D validan contra propuesta-motor-adaptativo-celda-v0_5.md §3`.
