# W1-P: ¿la reversión de signo de W1 es composición por contacto con autoridad de seguridad?

Encargo W1-P · v2 (parchado), mesa #20, 2026-08-04 (TZ America/Mexico_City, verificado
contra `git log --date=local`). Rama `sesion/encargo-w1-p-policial`, tras
`git merge origin/main` limpio (fast-forward `4dca34c..65302f7`, sin conflictos,
`milpa/procedencia.yaml` no tocado por el merge). Ejecutor: sesión Claude Code,
Ubuntu, worktree `/home/pc0/mm-encargo-w1-p-policial`, `data/raw` enlazada al
corpus compartido (`/home/pc0/mm-corpus/raw`, ya existía, no se creó ni se descargó).

## 0 · Filiación con el encargo

v2 parchado respecto de v1: este acto son dos commits, no tres (el commit 3 de v1,
que verificaba un recuento de la nota de X, se reasignó fuera de este acto porque
citaba contenido de una sección prohibida por el propio §0 de v1 — defecto de mesa,
no del ejecutor). Entra la regla de desempate §0.1 (declarar y seguir ante duda de
contaminación, parar solo si se abrió el resultado del estimando que se va a
pre-registrar). Mesa se declaró contaminada respecto del agregado de W1 (vio las
celdas, signos e intervalos de Encargo X) y por eso no escribe el falsador ni el
umbral de este acto — eso es todo el contenido de esta ficha.

## 0.1 · Declaración de duda de contaminación del ejecutor (regla de desempate)

Antes de escribir el falsador, dos exposiciones a declarar:

1. Para derivar el esquema de campos que voy a escribir en `milpa/procedencia.yaml`
   (commit 2), leí completos los bloques hermanos `G1_confianza_institucional` (W2,
   ENCIG 2023) y `G3_familismo_apoyo` (W3, ENIF 2024) bajo
   `coeficientes_generador_medidos` — **deliberadamente no abrí el bloque
   `G1_radio_confianza`** (líneas 660-686 antes del merge), que es el bloque
   prohibido por el encargo. Vía: necesitaba un patrón de esquema real
   (`clase/antes/fuente/n_util/eje_condicionante/beta_hat/nota/marca_cN/adr57_a`) y
   elegí los dos hermanos no prohibidos en vez de adivinar la forma del campo nuevo.
   Eso me mostró que, **para esos otros dos coeficientes**, condicionar por eje
   (Encargo X) invirtió el signo del marginal en varias celdas — W2 revierte a
   positivo en las cuatro celdas de edad; W3 se invierte a negativo en las celdas
   mayoritarias de formalidad/urbanización/migración/acceso digital. Es evidencia de
   que el procedimiento de condicionamiento de Encargo X **tiende, en este corpus, a
   encontrar inestabilidad de signo** — un patrón de fondo del método, no una cifra
   de `radio_confianza`.
2. Leí, permitido explícitamente por el encargo, `forense/notas/2026-08-04-x-
   condicionamiento-y-forma.md` §0-§3 completos (especificación de estratificación
   X1 y de forma funcional X2, y lo que el procedimiento declara no hacer) — sin
   resultados, solo método, heredado sin cambios en este acto.

**Por qué no informa mi umbral:** no vi ninguna cifra de `G1_radio_confianza` ni del
eje policial (nadie lo ha corrido — es justo el estimando que este acto pre-
registra). El patrón de fondo de (1) podría sesgarme a *esperar* que el signo
también se mueva aquí; lo declaro para que la auditoría pueda juzgar si el umbral
de §5 es más permisivo de lo que sería sin esa exposición. Contra-medida tomada:
el umbral es **simétrico** — el mismo criterio (2 de 3 ítems) y la misma vara de
evidencia (signo opuesto + al menos un IC95% que excluye cero) sirven tanto para
CONFIRMADA como para DESCARTADA, para no inclinar la balanza hacia el resultado que
el patrón de fondo sugeriría.

**Por la regla de desempate (§0.1 del encargo): no paro.** Ninguna de las dos
exposiciones es el resultado del estimando que voy a pre-registrar — nadie ha
corrido la partición policial de `radio_confianza`. Declarado y adentro.

## 1 · Ítem de AP5_16 identificado como autoridad de seguridad

Fuente: `data/raw/FD_ENCUCI2020.pdf` (Descriptor de archivos, INEGI, 61 páginas,
extraído con `pdftotext -layout`), sección de la Sec. 4-5, pregunta 5.16,
consecutivos 148-157.

Wording literal de la pregunta 5.16: *"En los últimos 12 meses, es decir, de agosto
de 2019 a la fecha, ¿ha tenido contacto con alguno de los siguientes funcionarios o
servidores públicos, incluso a través de un intermediario?"*

Los diez ítems (Cons. · etiqueta literal · mnemónico — códigos de respuesta
idénticos en los diez: `1` Sí / `2` No / `9` No sabe/no responde):

| Cons. | Etiqueta literal (FD) | Mnemónico |
|---|---|---|
| 148 | "1. Policía (de tránsito, Seguridad pública)" | `AP5_16_1` |
| 149 | "2. Ministerio Público" | `AP5_16_2` |
| 150 | "3. Jueces" | `AP5_16_3` |
| 151 | "4. Médico(a), Enfermero(a), Servidor(a) social en hospital o clínicas públicas" | `AP5_16_4` |
| 152 | "5. Maestros(as) de escuelas o universidades públicas" | `AP5_16_5` |
| 153 | "6. Autoridades de seguridad social y bienestar" | `AP5_16_6` |
| 154 | "7. Empleados de oficinas de gobierno en los municipios o alcaldías" | `AP5_16_7` |
| 155 | "8. Empleados de oficinas de gobierno estatal o federal" | `AP5_16_8` |
| 156 | "9. Guardia Nacional" | `AP5_16_9` |
| 157 | "10. Ejército y Marina" | `AP5_16_10` |

**Identificación: `AP5_16_1`** ("Policía (de tránsito, Seguridad pública)") es el
ítem de autoridad de seguridad. Es el único de los diez cuya etiqueta contiene
textualmente "Seguridad pública" — coincide con el término exacto de las dos
referencias externas del encargo (INEGI/ENCIG 2023: "autoridades de seguridad
pública"; Sanabria-Pulido y Langbein 2025: "la policía"). Identificación única, sin
ambigüedad léxica — no hay PARO por esta vía.

Dos exclusiones declaradas explícitamente, para que no se lean como omisión:

- **`AP5_16_6` ("Autoridades de seguridad social y bienestar") no es autoridad de
  seguridad pública — es un falso amigo léxico.** "Seguridad social" en el uso
  administrativo mexicano refiere a instituciones de bienestar/pensiones (tipo
  IMSS/ISSSTE), no a policía ni a fuerzas de seguridad. Se excluye del estrato
  policial.
- **`AP5_16_9` ("Guardia Nacional") y `AP5_16_10` ("Ejército y Marina") se excluyen
  del estrato policial**, aunque ambas son fuerzas con función de seguridad pública
  de facto en México. Razón: las dos referencias externas que motivan el acto usan
  específicamente "policía" / "seguridad pública" (INEGI/ENCIG) y "policía"
  (Sanabria-Pulido y Langbein) — ninguna se refiere a fuerzas armadas ni a Guardia
  Nacional. Incluirlas mezclaría policía civil (el canal que documentan ambas
  referencias) con instituciones militares/paramilitares de dinámica de contacto y
  de discrecionalidad distinta, y ampliaría "policial" más allá de lo que el ancla
  externa define. Decisión de alcance tomada ahora, no un hallazgo — una definición
  ampliada (Policía + GN + Ejército/Marina) queda declarada como sensibilidad
  posible, no ejecutada en este acto.

## 2 · Partición: estrato policial / no policial

Universo base: idéntico, sin cambio, al de `2026-08-04-w-coeficientes-generador-
paso1.md` §1.1 — subpoblación con contacto (`AP5_16_1..10`, al menos un `'1'`),
verificado 13 435 de 21 519.

- **Estrato policial (P):** personas del universo base con `AP5_16_1='1'`.
  Incluye a quienes *además* tuvieron otros contactos (la batería admite múltiples
  `'1'`) — no es "solo policía". Se reporta como diagnóstico, no como partición
  adicional, qué fracción de P tiene al menos un `'1'` más en `AP5_16_2..10`
  (tasa de contacto mixto), para que P no se lea como aislado.
- **Estrato no-policial (NP):** personas del universo base con `AP5_16_1 ∈ {'2','9'}`
  (cualquier valor que no sea `'1'`). Por construcción del universo base (ya exige
  al menos un `'1'` entre los diez ítems), NP automáticamente tiene su `'1'`
  calificador en algún ítem `AP5_16_2..10` — no hace falta verificarlo aparte, es
  consecuencia lógica de una regla ya sellada, no una regla nueva.
- `'9'` (No sabe/no responde) en `AP5_16_1` se trata como **no-policial**: `'1'` es
  el único valor que establece afirmativamente el contacto policial en la
  codificación del propio instrumento; `'9'` no lo establece. Decisión de
  codificación declarada ahora, no ajustada después de ver cuántos `'9'` hay.
- P y NP son exhaustivos y mutuamente excluyentes dentro del universo base — todo
  el universo base cae en uno de los dos.

n mínimo por celda, heredado sin cambio de X1 (`2026-08-04-x-condicionamiento-y-
forma.md` §1, mismo umbral de toda Fase B): **30 sin ponderar en cada uno de los dos
grupos (`θ=1`, `θ=0`) de la celda**. Celda bajo el mínimo se reporta **SIN SOPORTE**
con su n — no se colapsa con la celda vecina ni se omite.

## 3 · Marginal restringido — restricción 1 (A-bis 4)

Este acto no compara ninguna celda contra el β̂ marginal general de W1 (el que vive,
sin abrir, en `milpa/procedencia.yaml → coeficientes_generador_medidos.
G1_radio_confianza`, campo `beta_hat` — prohibido hasta después del commit 1, y no
necesario después tampoco). La comparación de este acto es enteramente interna: β̂
del estrato policial contra β̂ del estrato no-policial, ambos calculados frescos
aquí, cada uno sobre su propio universo restringido — nunca una proporción de un
estrato contra el denominador del otro, y nunca contra una cifra marginal externa
sin restringir (el error que el rider 4432748 ya corrigió en otro lugar de W1).

## 4 · Escala secundaria invariante a tasa base — restricción 2 (A-bis 3)

Elijo **razón de riesgos** (RR = p̂(confía=1)/p̂(confía=0), calculada dentro de cada
estrato) sobre razón de momios:

1. Interpretación directa ("X veces más probable"), sin el paso de traducir momios
   a probabilidad.
2. La razón de momios diverge de la razón de riesgos cuando la prevalencia del
   desenlace no es rara; la cifra externa citada por el encargo (INEGI/ENCIG 2023:
   ~59.4% de quienes tuvieron contacto con seguridad pública reportan alguna
   experiencia de corrupción) sugiere que "rara" no aplica aquí — se usa como
   motivación externa (tipo 3, no ancla de validación), declarada antes de ver la
   cifra real de este acto.
3. Es la extensión de menor complejidad sobre lo ya calculado: se deriva de las
   mismas `p_hat`/`se` que devuelve `prop_ultimate_cluster`, sin estimador nuevo.

Fórmula fijada ahora, para que el commit 2 solo sustituya números:

```
RR            = p̂₁ / p̂₀
SE(ln RR)     = sqrt( (se₁/p̂₁)² + (se₀/p̂₀)² )     [delta method sobre las se
                                                     ya ponderadas y ajustadas
                                                     por conglomerado que
                                                     devuelve prop_ultimate_
                                                     cluster — post-proceso de
                                                     su salida, no un estimador
                                                     nuevo, no toca svystat.py]
IC95%(RR)     = exp( ln(RR) ± 1.96 · SE(ln RR) )
```

Caso borde declarado ahora: si `p̂₀ = 0`, RR no está definido; se reporta "RR no
definido (`p̂₀=0`)" y la celda se lee solo por β̂/IC95%.

Nota de equivalencia, para no duplicar criterio: un cambio de signo en β̂ (p̂₁ vs p̂₀)
es el mismo evento que RR cruzando 1. El falsador (§5) se define sobre signo/
significancia de β̂; RR se reporta como lectura de magnitud invariante a tasa base,
no como un criterio adicional del umbral.

## 5 · Falsador, umbral, y escala de desenlaces

**Hipótesis bajo prueba (H-policial):** el comportamiento del estimando W1 está
dominado por el contacto policial — restringir a NO-policial cambiaría
sustancialmente el patrón frente a restringir a policial.

**Criterio de discrepancia, por ítem `i` ∈ {`AP5_1_1`, `AP5_1_2`, `AP5_1_3`}** (solo
sobre celdas CON SOPORTE):

- **DISCREPANTE(i)** si los signos de β̂ policial,i y β̂ no-policial,i son
  **opuestos** Y **al menos uno** de los dos IC95% excluye cero.
- **ESTABLE(i)** si los signos coinciden, o si ningún IC95% excluye cero (no hay
  señal que comparar), o si el punto central de un estrato cae dentro del IC95% del
  otro (no hay evidencia de diferencia real pese a un posible cambio de signo
  puntual).

**Regla de agregación** (no se promedia θ — los tres ítems se reportan por
separado; esto es solo la regla de veredicto sobre los tres veredictos ya
calculados, no un estimador nuevo). **Precedencia — se evalúa en este orden, la
primera fila que aplique manda (gobierna sobre cualquier legend genérico, ADR-58(b),
ADR-59(a)):**

1. **INEJECUTABLE POR N** — si en ≥2 de los 3 ítems, alguna de las cuatro celdas
   (policial×confía1, policial×confía0, no_policial×confía1, no_policial×confía0)
   cae bajo el mínimo de n=30 sin ponderar.
2. **COMPOSICIÓN POLICIAL CONFIRMADA** — si no aplica (1), y ≥2 de 3 ítems son
   DISCREPANTE.
3. **COMPOSICIÓN POLICIAL DESCARTADA** — si no aplica (1) ni (2), y ≥2 de 3 ítems
   son ESTABLE.
4. **ACOTADA** — ningún patrón anterior alcanza mayoría (p. ej., 1 discrepante + 1
   estable + 1 sin soporte aislado que no basta para la fila 1).

**Fila de no-refutación (Bloque B-bis):** el falsador intenta tumbar H-policial. Que
el falsador **no refute** significa que se alcanza la fila 2 (CONFIRMADA) — los
datos son consistentes con que el contacto policial domina el comportamiento del
estimando; H-policial sobrevive el intento de refutación.

## 6 · Qué resultado sería interesante bajo corroboración

Los dos desenlaces sustantivos (filas 2 y 3) son informativos, ninguno es "fracaso"
del acto — el fracaso sería la fila 4 o la fila 1 sin poder concluir nada:

- **CONFIRMADA** (el falsador no refuta H-policial) es el resultado que **activa una
  acción concreta sobre el ejecutable**: cambia el estado registrado de
  `G1_radio_confianza` (resuelve la condición escrita en ADR-60(e), que dejó el
  coeficiente en ASIGNADO · SIGNO BAJO PRUEBA apuntando explícitamente a este acto).
  Es el resultado "interesante" en el sentido de que exige seguimiento — no en el
  sentido de ser el resultado deseado. Declarado antes de correr para que una
  corroboración no se lea como fracaso del diseño.
- **DESCARTADA** cierra, con dato y de forma permanente, una hipótesis explicativa
  competidora que el propio encargo cita por nombre — no vuelve a proponerse. Es el
  otro resultado sustantivo, igual de válido como cierre del acto.

## 7 · Confundidores no aislados (declarados antes de correr)

1. **Límite estructural del desenlace, el más importante:** `tramite.mordida.
   discrecional` es un compuesto sobre AP5_17/AP5_18, que preguntan "de esos
   contactos" en general — **no preguntan qué autoridad específica pidió o recibió
   la dádiva.** Para una persona en P que también tuvo contactos no-policiales
   (tasa de traslape, reportada en §2/commit 2), una mordida-compuesta positiva no
   es atribuible únicamente al contacto policial. Este acto no puede resolver esa
   granularidad — es un límite de la variable de desenlace ya sellada (nota-W
   §1.1), no algo que esta partición pueda aislar. El resultado de este acto habla
   de "personas con contacto policial" (posiblemente entre otros), no de "mordida
   causada por policía" en sentido estricto.
2. **Colisión / selección (restricción 3, A-bis 2):** el contacto policial no está
   aleatorizado. Quien tiene contacto con policía puede diferir sistemáticamente de
   quien no (exposición a control de tránsito, zona de residencia, actividad
   delictiva reportada, uso de vehículo) por vías que este diseño no separa —
   condicionar en un colisionador puede inducir asociación espuria en cualquier
   dirección. Los resultados de este acto son asociación estratificada, no
   identificación causal (A-bis 1).
3. **Tamaño de submuestra:** dado que la policía es, por la cifra externa citada
   (~59.4% de prevalencia de corrupción en ese trámite, la más alta de ENCIG), un
   contacto plausiblemente común, el estrato NP podría ser considerablemente más
   chico que P — riesgo conocido de caer en SIN SOPORTE o en la fila 1, declarado
   ahora, no como sorpresa después de correr.
4. **Alcance de "autoridad de seguridad":** la exclusión de Guardia Nacional y
   Ejército/Marina (§1) es una decisión de alcance defendible pero no la única
   posible — un resultado DESCARTADA o CONFIRMADA bajo esta definición estricta no
   se extiende automáticamente a una definición ampliada de fuerzas de seguridad,
   que queda fuera de este acto.

---

**El primer resultado que produzca este procedimiento es el que se reporta.**

---
---

## 8 · Resultados — primera y única corrida (commit 2)

Script: `tests/w1_p_policial.py` (nuevo, no modifica `tests/svystat.py` ni
`tests/dbfmini.py`). Corre desde la raíz: `python3 tests/w1_p_policial.py`.

**Validación de pipeline, antes de leer nada nuevo:** autochequeo interno de
`svystat.py` (`_caso_conocido`, SRS n=200/k=80) coincide a 9 decimales. El universo
de contacto reconstruido desde `AP5_16_1..10` reproduce **13 435 de 21 519**,
cifra por cifra igual al ya verificado en `2026-08-04-w-coeficientes-generador-
paso1.md` §1.1 — confirma que la lectura de la batería es correcta antes de
particionarla. Nota de implementación: `AP5_16_*` está codificado en el DBF como
campo Numérico de texto ancho fijo (`"1.000000000000000"`), no como carácter
simple `"1"` — el primer intento de lectura ingenua comparó contra `'1'` y dio
`n_contact=0`; detectado y corregido por la propia guarda de reproducción antes de
construir la partición sobre datos mal parseados.

**Partición ejecutada:** estrato policial n=4087; estrato no-policial n=9348
(suma exacta 13 435). Del estrato policial, **3605 (88.2%) tuvieron además al
menos otro contacto** de la batería (municipal/estatal/salud/educación/etc.) — el
estrato "policial" está lejos de ser "solo policía"; ver confundidor 1 de §7.

**Prevalencia de `tramite.mordida.discrecional` por estrato** (agrupada sobre
`confía`, referencia estable, independiente del ítem):

| Estrato | n | p̂ | IC95% |
|---|---|---|---|
| Policial | 4084 | 27.30% | [24.92%, 29.68%] |
| No-policial | 9328 | 5.35% | [4.65%, 6.04%] |

**Tabla completa, por ítem × estrato** (β̂ = p̂(confía=1) − p̂(confía=0); RR =
p̂(confía=1)/p̂(confía=0); "sig." = IC95% excluye cero al 95%):

| Ítem θ | Estrato | n(confía=1) | n(confía=0) | β̂ | IC95%(β̂) | RR | IC95%(RR) |
|---|---|---|---|---|---|---|---|
| AP5_1_1 (mayoría de las personas) | policial | 2030 | 2047 | **−5.37pp** | [−9.92, −0.82] sig. | 0.821 | [0.691, 0.975] |
| AP5_1_1 | no-policial | 4400 | 4898 | +0.80pp | [−0.58, 2.18] n.s. | 1.160 | [0.899, 1.498] |
| AP5_1_2 (personas que conoce) | policial | 3284 | 796 | −5.18pp | [−10.62, 0.27] n.s. | 0.836 | [0.698, 1.001] |
| AP5_1_2 | no-policial | 7383 | 1930 | +0.13pp | [−1.55, 1.81] n.s. | 1.025 | [0.745, 1.410] |
| AP5_1_3 (vecinos) | policial | 2273 | 1799 | **−5.53pp** | [−10.09, −0.98] sig. | 0.817 | [0.691, 0.966] |
| AP5_1_3 | no-policial | 5371 | 3922 | −0.45pp | [−1.87, 0.96] n.s. | 0.919 | [0.707, 1.195] |

Ninguna celda cae bajo el mínimo n=30 — las seis tienen soporte (la más chica,
policial×AP5_1_2×confía=0, n=796).

**Veredicto por ítem** (criterio de §5 de esta ficha):

- `AP5_1_1`: signos opuestos (policial negativo sig., no-policial positivo n.s.) →
  **DISCREPANTE**.
- `AP5_1_2`: signos opuestos pero ningún IC95% excluye cero → **ESTABLE**.
- `AP5_1_3`: signos iguales (ambos negativos) → **ESTABLE**.

**Veredicto agregado** (regla de precedencia de §5): 0 items SIN SOPORTE → no
aplica fila 1. 1 de 3 DISCREPANTE (no alcanza 2 de 3) → no aplica fila 2. 2 de 3
ESTABLE (alcanza 2 de 3) → aplica fila 3.

## **→ COMPOSICIÓN POLICIAL DESCARTADA**

### 8.1 · Lectura honesta más allá del tag (declarada por la restricción 3 — no sub- ni sobre-reportar)

El veredicto mecánico de la regla pre-registrada es DESCARTADA, pero el patrón
fino es más específico que "el estrato policial no importa" — y esa lectura
gruesa **no** se sostiene con la tabla completa:

En los tres ítems, el punto central de β̂ en el estrato **policial** es negativo
(coherente con el signo ASIGNADO, −0.35) y significativo al 95% en dos de tres
(`AP5_1_1`, `AP5_1_3`), marginal en el tercero (`AP5_1_2`, el IC95% roza cero por
0.27pp). En el estrato **no-policial**, los tres puntos centrales son pequeños,
sin patrón de signo consistente (+0.80pp, +0.13pp, −0.45pp), y ninguno es
significativo. Es decir: **la señal negativa que sostiene el signo ASIGNADO se
detecta, en este corte, únicamente dentro del estrato de contacto policial** — no
porque el estrato no-policial muestre el signo contrario con fuerza estadística
(eso habría contado como DISCREPANTE en más ítems), sino porque el estrato
no-policial no muestra señal detectable en ninguna dirección.

La regla pre-registrada en §5 se diseñó para detectar *reversión de signo* (el
riesgo que el encargo nombra: "W1 no mide lo que su rótulo dice"). El patrón que
aparece aquí es distinto: *concentración de significancia sin reversión de
signo*. Bajo la escala de cuatro filas de §5, eso cuenta como DESCARTADA (la
hipótesis de que el estrato policial *invierte* el comportamiento del estimando
no se sostiene) — pero no equivale a "el contacto policial es irrelevante para
W1". Ambas lecturas son ciertas a la vez y no se contradicen: la partición
policial no cambia el *signo* del estimando (por eso DESCARTADA), pero si el
estimando marginal de W1 resulta significativo, este corte sugiere que gran parte
de esa significancia proviene del subconjunto con contacto policial, no del
resto. Esta observación no mueve el veredicto (la escala de §5 no tiene una fila
para "concentración sin reversión") ni se declara como hallazgo nuevo fuera de
esa escala — se dejan las cifras completas de la tabla para que mesa lea el
patrón fino, no solo el tag.

### 8.2 · Validación contra caso conocido — declarado como límite

No existe ancla externa publicada para este corte estratificado (policial vs.
no-policial de `radio_confianza`×`tramite.mordida.discrecional`) — es un corte
nuevo de este acto, nadie lo ha corrido antes. Lo que sí se validó: (a) el
autochequeo interno de `prop_ultimate_cluster` contra el caso SRS degenerado; (b)
el pipeline de lectura de `AP5_16_*` contra el 13 435 ya publicado y verificado
en otro acto. Ninguna de las dos es una validación del *estimando estratificado
en sí* — se declara como límite, no se inventa un ancla que no existe.

### 8.3 · Contexto adicional (post-hoc, no parte del falsador pre-registrado)

Ahora que el commit 1 ya está sellado, es lícito leer `G1_radio_confianza` en
`milpa/procedencia.yaml` y `forense/hallazgos.md` — se leen aquí por primera vez,
después de correr y reportar §8; no informan el falsador ya committeado. Nota
para el registro, no para revisar el veredicto de arriba (que no cambia):

El β̂ marginal de W1 (sin condicionar) es negativo en los tres ítems pero pequeño
y solo significativo en `AP5_1_3` (vecinos, −0.0269). Al condicionar por
formalidad/edad/ingreso (Encargo X), la prosa de `eje_condicionante` en
`milpa/procedencia.yaml:665` cita "28 de 39 celdas... positivas... 12
significativas" — cifra que `forense/hallazgos.md` (entrada ENCARGO M-1,
ADR-60(f)) ya declaró errónea, recontada por aritmética directa sobre
`2026-08-04-x-condicionamiento-y-forma.md` §4.1 en **33 de 39 positivas, 9 de 39
significativas (las nueve positivas)** — discrepancia declarada por ese acto, no
corregida ahí (tarea asignada al commit 3 de la v1 de este mismo encargo,
**eliminado y reasignado fuera de este acto por el propio §-1 de la v2** que este
acto ejecuta; no se corrige aquí tampoco, mismo motivo — fuera de perímetro). Con
cualquiera de las dos cifras la lectura cualitativa es la misma: la mayoría de
las celdas de formalidad/edad/ingreso invierten a signo positivo, y toda celda
significativa es positiva.

El eje policial de este acto **no reproduce esa reversión**: donde hay señal
significativa (`AP5_1_1`, `AP5_1_3`), el signo se mantiene negativo en el estrato
policial, igual que el marginal y que el ASIGNADO. Los cuatro ejes medidos hasta
ahora (formalidad, edad, ingreso, policial) apuntan en direcciones distintas: los
tres de Encargo X reversan el signo; el policial de este acto lo mantiene y lo
concentra. Esto no cambia el veredicto de §8 (que es sobre si el eje policial
*por sí solo* reversa el patrón entre sus propios dos estratos, y no lo hace) —
se declara como contexto para que mesa, al leer los cuatro ejes en conjunto,
tenga el cuadro completo.

### 8.4 · Perímetro de cierre

No cambia el valor `ASIGNADO` (−0.35) de `G1_radio_confianza` — sigue siendo lo
que el modelo usa. No adjudica si el signo del modelo está mal — reporta signo y
estabilidad de esta partición, la lectura de qué implica para el generador es de
mesa. No sella ADR. No toca `canon/`, `data/manifiesto.yaml`, ni
`tests/svystat.py`. **Esta sesión abrió microdato de ENCUCI: queda inhabilitada
para pre-registrar cualquier otro estimando contra ENCUCI (ADR-46).**

---

**Los resultados de §8 son los que produjo la primera y única corrida de
`tests/w1_p_policial.py`. No se re-corrió con otra especificación.**
