# S16 · Pre-registro de `R9.3` sobre la batería `p53` de Sociedad de la Información (UNAM-IIJ) — el único de los tres negativos que el inventario deja `EXISTE-SATISFACE`

### `prereg-caja-S16` · **v1.0** · 7 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S16-R9-3-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S16`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.sav`, de `informacion.credibilidad.allegado_confianza` (`R9.3`) sobre la batería **`p53_1…p53_25`** de la Encuesta Nacional de Sociedad de la Información (UNAM-IIJ): credibilidad 0–10 declarada por fuente, con **allegados y medios formales en la misma escala y el mismo respondente**. |
> | **QUÉ NO ES** | No abre dato. No mide. No mueve el tier de `R9.3` (`[MEDIA]`). No usa `p33` de Medio Ambiente como dato: §3 la deja como corroboración **condicionada**, porque el inventario no revela qué medio es cada mención. |
> | **VERIFICAS ASÍ** | Caja abre el `.sav` y confirma, antes de calcular, que las 25 variables existen con ese nombre y que la escala es 0–10 con los códigos de no-respuesta identificados. Si una no existe, **PARA**. |

**Acto:** `ACTO MAESTRA38-N23-N25 · TRES-SPECS-NEGATIVOS`, 7/sep/2026, entorno **NUBE** (`cloud_default`), sobre `origin/main = 604793fa` (PR #591).

**Evidencia de existencia:** `forense/notas/2026-09-07-MAESTRA38-N23-N25-barrido-negativos.md` §5 y §2(3).

---

## 0 · Ficha bajo prueba, cierre que se revisa y corrección de premisa

### 0.1 · Definición vigente

`canon/modelo-decision-v4_0.md:772`: `R9.3 | L287 | Allegado de confianza → sube credibilidad inicial | [MEDIA] | No`.

`python3 tools/ya_medido.py R9.3` (corrido al redactar): resuelve a `informacion.credibilidad.allegado_confianza`; **`milpa/tramite.yaml`: sin apariciones**; veredicto del script al redactar: **`NUNCA-MEDIDA`** (una corrida posterior devuelve `MEDIDA-EN: S16` porque el script indexa esta misma spec — no es una medición, es esta pieza citándose; se declara para que nadie lo lea como tal). Cierre vigente: `SIN-COBERTURA` en el cruce de Ola 6 / `HIPÓTESIS-SIN-INSTRUMENTO` (`N10`), firmado en bloque por **FP-303**. **Esta spec no reabre FP-303 en bloque.**

### 0.2 · Corrección de premisa del encargo — son 25 fuentes, no 10, y la pregunta que dejaba abierta ya está contestada

El encargo escribe «`p53_1…p53_10`» y condiciona el veredicto: *«EXISTE-SATISFACE **si** entre las fuentes de p53 hay allegados (familiares/amigos/vecinos) además de medios — se verifica en el cuestionario antes de sellar»*.

**Verificado contra el inventario, sin abrir dato y sin abrir cuestionario: la batería tiene 25 ítems y sí trae allegados.** El inventario captura el enunciado completo de cada variable, y el enunciado **incluye la fuente al final**:

> «53 Ahora quiero que me diga, pensando en una escala del 0 al 10, como en la escuela, donde 0 es no cree en nada de lo que le dicen y 10 es cree totalmente en lo que le dicen ¿qué tanto cree en la información que le da…? **Su familia**»

No hace falta el cuestionario para contestar la condición del encargo. Este es —otra vez, dentro del mismo acto— el defecto que el hallazgo `PARA-v2.13` describe: dar por no consultable lo que el inventario ya listaba.

---

## 1 · La batería `p53` — las 25 fuentes, nombradas

Verificadas en `data/inventario-reactivos-v1_2.tsv`, miembro `losmexicanos_unam_iij/sociedaddelainformacion/Encuesta_Nacional_de_Sociedad_de_la_Informacion.sav`. Escala común 0–10 («0 = no cree en nada de lo que le dicen», «10 = cree totalmente»).

| grupo pre-registrado | variables |
|---|---|
| **`ALLEGADOS`** (el `SI` de la regla) | `p53_1` Su familia · `p53_17` Sus amigos · `p53_23` Sus vecinos |
| **`MEDIOS_FORMALES`** (contraste primario) | `p53_2` La televisión nacional · `p53_6` Los periódicos · `p53_13` La radio · `p53_10` La televisión extranjera |
| **`INTERNET`** (contraste secundario) | `p53_19` El internet · `p53_5` Las redes sociales · `p53_25` Blogs de internet |
| no entran en ningún grupo (se listan para que la asignación sea auditable, no para medirse) | `p53_3` publicidad de la radio · `p53_4` Presidente de la República · `p53_7` Los maestros · `p53_8` publicidad del Gobierno Federal · `p53_9` comerciales de televisión · `p53_11` Los empresarios · `p53_12` gobernador de su estado · `p53_14` libros de texto · `p53_15` curas, sacerdotes o ministros · `p53_16` famosos que salen en televisión · `p53_18` partidos políticos · `p53_20` Los diputados · `p53_21` Los cantantes · `p53_22` organizaciones sociales · `p53_24` Instituto Nacional Electoral |

**La asignación de los tres grupos se congela aquí, antes de ver dato.** `p53_7` (maestros) y `p53_15` (curas) son figuras de proximidad local pero **no allegados** en el sentido de la regla (lazo personal previo): se dejan fuera y se dice por qué, en vez de moverlos después según convenga al resultado.

---

## 2 · Contraste pre-registrado

Sobre el mismo respondente, escala idéntica, **diferencia pareada** (cada persona es su propio control — la ventaja de que las 25 fuentes vengan de una sola batería):

```
D_allegados_medios = media(ALLEGADOS) − media(MEDIOS_FORMALES)      [contraste primario]
D_allegados_internet = media(ALLEGADOS) − media(INTERNET)           [contraste secundario]
```

* Media dentro de cada grupo = promedio simple de sus ítems válidos para ese respondente; un respondente entra si tiene **al menos un ítem válido en cada uno de los dos grupos** del contraste. Se declara la `n` real y cuántos quedaron fuera por esa regla.
* **IC95 por diferencia pareada**, ponderado por el ponderador del archivo (§4).
* Los dos contrastes se reportan **por separado, nunca promediados**: internet y televisión no son el mismo objeto y agregarlos escondería el resultado interesante.
* **Códigos de no-respuesta** (típicamente 98/99 o similares en esta serie) se identifican en el mapa de valores al abrir y se excluyen **antes** de promediar. El inventario no los captura — **cláusula PARA si el mapa no permite distinguirlos de un 9 legítimo de la escala**.

---

## 3 · `p33` de Medio Ambiente — corroboración **condicionada**, no dato

El encargo la manda como corroboración secundaria. Verificada: la batería existe (`p33_1`…`p33_8`, ordenamiento por confiabilidad de medios de información ambiental, «donde el 1 es el más confiable y el 8 el menos confiable»). **Pero el inventario solo captura «1ª MENCIÓN … 8ª MENCIÓN»: qué medio ocupa cada mención vive en las etiquetas de valor, que el inventario no captura.**

**Consecuencia:** `p33` **no se pre-registra como corroboración**. Se declara así:

* Si caja, al abrir el `.sav` de Medio Ambiente, encuentra que la lista de ocho medios **incluye allegados** (familia/amigos/vecinos), `p33` se usa como corroboración por ordenamiento y se reporta aparte, con la lista transcrita.
* Si la lista es **solo de medios de comunicación** —lo que el enunciado sugiere («De los siguientes **medios** que proporcionan información sobre el ambiente»)—, `p33` **no corrobora nada de `R9.3`** y se reporta como `NO-APLICA`, sin forzar la analogía.
* En ningún caso se combina con `p53`: instrumentos distintos, encuestas distintas, escalas distintas (0–10 continuo vs. ordenamiento 1–8).

---

## 4 · Escala de falsación `B-bis` — qué significaría corroborar

| fila | qué la satisface |
|---|---|
| `CORROBORADA` | `D_allegados_medios` **positivo** con IC95 íntegramente sobre 0: la información que da un allegado se cree más que la de los medios formales — la dirección que `R9.3` afirma |
| `CONTRARIA` | `D_allegados_medios` **negativo** con IC95 íntegramente bajo 0 |
| `NO-DISCRIMINA` | IC95 cruza 0 con ambos grupos estimables |
| `NO-ESTIMABLE` | `n` con ambos grupos válidos `< 10`, o el mapa de valores no permite separar no-respuesta de escala (§2) |
| **`EXISTE-SATISFACE`** | **la fila que esta spec devuelve hoy**: la regla tiene instrumento, nombrado ítem por ítem, con antecedente y desenlace en la misma batería y el mismo respondente. **De los tres negativos que este acto reabre, es el único que llega hasta aquí** |

**Lo que este contraste NO prueba, declarado antes de correr:** `R9.3` habla de *credibilidad inicial* — cuánto se cree **un mensaje nuevo** según quién lo trae. `p53` mide **credibilidad general atribuida a la fuente**, no la actualización ante un mensaje concreto. Es el operacionalizable más cercano que el corpus tiene, y la distancia entre uno y otro se reporta con el resultado, no en nota al pie. Un `CORROBORADA` corrobora *«se atribuye más credibilidad general a los allegados que a los medios»*.

**Guardia de n mínima:** `< 10` ⇒ `NO-ESTIMABLE`, misma que `S4 §3`, `S5 §3.1`, `S13 §2`, `S14 §3`, `S15 §4`.

**Ponderador:** **no localizado en el inventario para esta encuesta** — el barrido de `FACTOR|PONDER|WEIGHT|FEXP|PESO|EXPANSION` sobre el miembro no devuelve candidato, a diferencia de las otras encuestas UNAM-IIJ (`Pondi2`/`Pondi_v` en Cultura Política, `Pondi2` en Cultura Constitucional). Caja lo busca al abrir; **si no existe, se reporta sin ponderar y se dice** — no se importa el ponderador de otra encuesta de la serie. Mismo criterio que `S2-L2 §1.0` fija para payloads sin diseño muestral visible en el censo.

**Cláusula PARA (patrón S6/S12, verbatim):** **si la variable no existe en el archivo, PARA.**

---

## 5 · Archivos que la caja necesita abrir

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `encuesta_nacional_de_sociedad_de_la_informacion_3` | `losmexicanos_unam_iij/sociedaddelainformacion/Encuesta_Nacional_de_Sociedad_de_la_Informacion.sav` | `6e821f3b652ccf8940f78b96771e0c50f3ea3450297c9dc73a2b144d9f45e789` |
| `encuesta_nacional_de_sociedad_de_la_informacion_2` (gemelo `.dta`, verificación) | `losmexicanos_unam_iij/sociedaddelainformacion/Encuesta_Nacional_de_Sociedad_de_la_Informacion.dta` | `fc289a36cbf5396690999a2ebf7a48915ae8a9a821974fcbd1a482a55ccb3a12` |
| `encuesta_nacional_de_medio_ambiente_3` (solo si §3 aplica) | `losmexicanos_unam_iij/medioambiente/Encuesta_Nacional_de_Medio_Ambiente.sav` | `aac4b2f73f6b14b604a8b93fadf8bd67cdcb1b4b9cee23ecba1cb380fda7b927` |

---

## 6 · Qué NO hace este acto

No abre ninguno de los archivos de §5. No mide, no calcula ninguna media ni IC95. No mueve el tier de `R9.3` ni la carga al motor. No reabre FP-303 en bloque. No combina `p53` con `p33` (§3). No reasigna `p53_7`/`p53_15` a `ALLEGADOS` (§1). No toca `S14`/`S15` ni ninguna spec existente, ni `data/cruce-ola6-v1_0.tsv`, ni `milpa/**`.

**El primer resultado que produzca este procedimiento es el que se reporta.**
