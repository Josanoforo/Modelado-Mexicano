# P3 — LCA de segmentación sobre ENIGH: ejecución de Fase B contra el pre-registro sellado

*4 de agosto de 2026.*

**Procedencia.** Tipo (1) para todo lo verificado contra archivo en esta sesión
(`forense/p3-lca-preregistro-v1_0.md` v1.0; `canon/modelo-decision-v4_0.md`
§1.1.A/§1.1.D; `canon/gobernanza-v1_15.md` ADR-51; el paquete ENIGH en disco).
Tipo (3), no re-verificada aquí más allá de lectura dirigida, la premisa de
que el pre-registro fue escrito por una sesión limpia (nube) — eso lo declara
el propio documento en su §0 y no es objeto de esta ejecución.

**Sesión-tipo: Ubuntu microdato.** Worktree `mm-p3-lca`, rama
`sesion/p3-lca-segmentacion`, sobre `origin/main` = `6a09a37` (PR #60 ya
fusionado). `data/raw` **no existía en este worktree** al abrir la sesión —
consistente con la advertencia del propio encargo ("un entorno sin
`data_raw` reporta todo AUSENTE"): se recreó como symlink a
`/home/pc0/mm-corpus/raw` (mismo patrón que el resto de los worktrees vivos;
`data/raw` es infraestructura local no rastreada por git, no un artefacto
del repo). Con el symlink en su lugar, el payload **sí estaba presente**.

## 0 · Verificación de premisas antes de obedecer (ADR-39)

| Premisa (del pre-registro, o de esta ejecución) | Verificada contra | Resultado |
|---|---|---|
| Canon vigente v4.0, §1.1 por síntesis sobre atributos | `canon/modelo-decision-v4_0.md` cabecera + §1.1.A/§1.1.D | ✔ Sostenida |
| Los seis ejes con variable, módulo, llave; tres de hogar | `modelo` §1.1.A, tabla | ✔ Sostenida, citada verbatim en el pre-registro §2.1 |
| ADR-51 corrigió los g.l. reales a 22 (7+15) | `canon/gobernanza-v1_15.md`, ADR-51 | ✔ Sostenida |
| `enigh2022_nc_csv` sha256 verificado por P1 | `data/manifiesto.yaml:398` vs `sha256sum` real del archivo | ✔ **Coincide exacto**: `3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06` |

Las cuatro premisas se sostienen. Se procede.

## 1 · Datos de partida — lo que el pre-registro ordenó derivar, no teclear

**Universo 18+ (§2.1, "no predicho").** `n = 217 375` personas, de un total
de `309 684` registros en `poblacion`. **100 % de los 217 375 tienen match**
en `concentradohogar` y en `hogares` (0 sin match) — la herencia hogar→persona
de I4–I7 no perdió a nadie.

**Variables de diseño (§5.1, hueco declarado por el pre-registro — CERRADO
aquí).** `factor` (factor de expansión), `est_dis` (estrato) y `upm` viven
**directo en `poblacion`, a nivel persona** — el mismo módulo que I1/I2/I3.
No hizo falta trasladar un factor de hogar ni inventar una regla de
traslado: se localizaron por nombre exacto, no se tecleraron de memoria.

**Referencia temporal de `residencia` (§2.3).** *La fuente no lo trae.* El
diccionario de datos de `poblacion` (fila 46, `residencia`) solo dice
"Categorías en el catálogo de residencia" — sin texto de pregunta.
`metadatos_enigh_2022_ns.txt` no menciona `residencia` en ninguna parte (0
coincidencias). Se buscó en los dos únicos lugares que el pre-registro
señala como candidatos y ninguno trae el periodo de referencia. No es "no
pude confirmarlo" (no hay ambigüedad de dónde más buscar): es que el paquete
público, tal como está en disco, no incluye esa información.

**¿`est_socio` es función determinista de `ing_cor`? (§2.4).** **No.** Sobre
los 90 059 hogares con ambos valores, los rangos de `ing_cor` se traslapan
casi por completo entre las cuatro categorías de `est_socio` (p. ej. el
rango de la categoría 1 "Bajo" llega hasta $7.15M trimestrales, por encima
del máximo de la categoría 4 "Alto"), y **29.2 % de los pares consecutivos**
(ordenados por `ing_cor`) violan monotonicidad estricta. `est_socio` es un
índice multivariado de INEGI, no un corte de ingreso — se reporta, no se
asume.

**Faltantes por indicador (§5.3.c, antes de ajustar).** Solo `I1_formalidad`
(`segsoc`) tiene faltantes: **139 de 217 375 (0.064 %)**. I2–I7: **0 %**. Muy
por debajo del umbral del 10 % — no se corrió la solución de casos completos
por separado (§5.3.c solo la exige por encima de ese umbral).

**Reescalamiento de pesos (§5.2).** Suma cruda de `factor` = **91 786 096**
(población nacional expandida). Reescalada para sumar el `n` efectivo de
muestra (**217 375**) con constante **2.368278×10⁻³**. BIC/aBIC del ajuste
principal se computan sobre ese `n` reescalado, no sobre la suma expandida.

## 2 · Los ocho ajustes — tabla completa (§3.2), ponderado-reescalado

500 arranques por `k`, 50 mejores llevados a convergencia final (§3.4).
`n` parámetros = `(k−1) + k·Σ(categorías−1)`, con 7 indicadores de
cardinalidad (2,4,3,4,4,2,2).

| k | logL | # parám. | BIC | aBIC | AIC | Entropía | Prevalencias (ponderadas) | Replican mejor logL (/50) | Señales de frontera (0/1) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | −1 210 384.96 | 14 | 2 420 941.98 | 2 420 897.48 | 2 420 797.93 | — | 1.00 | 50 | 0 |
| 2 | −1 125 853.11 | 29 | 2 252 062.62 | 2 251 970.45 | 2 251 764.22 | 0.794 | .374/.626 | 50 | 2 |
| 3 | −1 107 685.29 | 44 | 2 215 911.31 | 2 215 771.48 | 2 215 458.58 | 0.753 | .413/.202/.385 | 50 | 2 |
| 4 | −1 103 252.12 | 59 | 2 207 229.31 | 2 207 041.80 | 2 206 622.24 | 0.750 | .056/.393/.353/.199 | **35** | 3 |
| 5 | −1 099 969.31 | 74 | 2 200 848.04 | 2 200 612.86 | 2 200 086.62 | 0.730 | .057/.199/.333/.073/.338 | **1** | 3 |
| 6 | −1 097 281.17 | 89 | 2 195 656.09 | 2 195 373.24 | 2 194 740.34 | 0.733 | .309/.070/.052/.336/.135/.098 | **1** | **7** |
| 7 | −1 095 891.82 | 104 | 2 193 061.74 | 2 192 731.23 | 2 191 991.65 | 0.656 | .146/.059/.143/.211/.058/.221/.163 | **2** | 12 |
| 8 | −1 094 900.17 | 119 | 2 191 262.77 | 2 190 884.58 | 2 190 038.33 | 0.659 | .049/.176/.073/.128/.156/.045/.193/.179 | **1** | 12 |

**El BIC decrece de forma estrictamente monótona de `k=1` a `k=8`, sin
mínimo interior — el mínimo observado está en el borde del rango probado
(`k=8`).** Ninguno de los ocho ajustes reporta clases con prevalencia
ponderada bajo 5 % (ver §4), pero la replicación de la mejor log-verosimilitud
se derrumba después de `k=4` (35/50 → 1/50) y las señales de frontera crecen
con `k` (0 → 12 en `k=7`/`k=8`).

## 3 · Regla de decisión, §3.3, en su orden literal y sin discreción

1. **BIC mínimo → `k=8`.**
2. **aBIC se reporta, no manda → también mínimo en `k=8`** (no discrepan).
3. No hay discrepancia BIC/aBIC que resolver.
4. **Regla de "sin separación" (2 % del rango total de BIC observado en
   1–8).** Rango = `2 420 941.98 − 2 191 262.77 = 229 679.21`. Umbral =
   `4 593.58`. Caminando desde `k=8` hacia abajo: `k=7` vs `k=8` difieren
   `1 798.9` (< umbral, empatados); `k=6` vs `k=8` difieren `4 393.3` (<
   umbral, empatados); `k=5` vs `k=8` difieren `9 585.2` (**≥ umbral, la
   cadena se rompe aquí**). El primer (menor) `k` dentro de la banda de
   empate es **`k=6`** → **`k_primario = 6`** por la regla mecánica de
   parsimonia.
5. La entropía no seleccionó `k` en ningún paso de lo anterior (se reporta
   en la tabla de §2, nada más).
6. **Perfiles completos `k=5,6,7`** (el vecindario de `k_primario`): ver
   `forense/notas/_p3_lca/ck_principal.json` → `perfiles_k_vecinos` (φ y π
   completos por clase, los tres valores de `k`). Se omiten de esta nota por
   extensión — están en el JSON auditable, no se resumen aquí para no
   perder precisión.

**⚠️ Lo que esto significa y que el pre-registro anticipó explícitamente
(§3.1): "si el BIC sigue decreciendo en `k=8`, eso es un resultado (§6·D6),
no una invitación a probar 9."** La regla de "sin separación" del paso 4
produce mecánicamente un `k_primario=6` — pero esa mecánica es un
desempate de parsimonia para cuando SÍ existe una meseta; no crea un
mínimo interior donde no lo hay. El hecho de fondo, verificado en la
tabla de §2, es que **el BIC nunca dio la vuelta dentro del rango probado**.
Las dos lecturas (mecánica → `k=6`; forma de la curva → sin mínimo interior)
se reportan ambas, íntegras, en §7.

## 4 · Estabilidad, §3.5 — evaluada sobre `k_primario=6`

**(E1) Replicación de log-verosimilitud ≥ 5 arranques: FALLA.** Solo 1 de
los 50 arranques llevados a convergencia final replica la mejor log-verosimilitud
(`< 5`) → **NO REPLICADA** (§3.4).

**(E2) Replicación en mitades, partición aleatoria por UPM: PASA.**
10 211 UPM totales, partidas en dos mitades de 5 105/5 106 UPM
(108 787/108 588 personas). Reajustado `k=6` en cada mitad y emparejadas las
seis clases por máxima correlación (fuerza bruta sobre las 720 permutaciones):

| Mitad | Correlaciones del emparejamiento (por clase) | Mínima |
|---|---|---|
| A | .998 / .996 / .992 / 1.000 / .999 / .994 | **.992** |
| B | .998 / .999 / .998 / 1.000 / .999 / .978 | **.978** |

Ambas mitades ≥ 0.90 → **E2 pasa**. Los *perfiles* de clase son reproducibles
entre mitades independientes, aunque la superficie de log-verosimilitud
tenga múltiples óptimos casi-empatados (lo que hace fallar a E1).

**(E3) Sin clases degeneradas: FALLA.** Ninguna clase cae bajo el umbral de
prevalencia del 5 % (las seis van de 5.2 % a 33.6 %), pero hay **7
probabilidades condicionales pegadas a frontera (0/1)** dentro de `k=6`
(p. ej. la clase de prevalencia 7.0 % tiene `P(est_socio=3)=0.000` y
`P(est_socio=4)=0.000` exactos; la clase de prevalencia 33.6 % tiene
`P(est_socio=3)=0.000`, `P(est_socio=4)=0.000`). Basta una señal de frontera
para que E3 falle.

**Basta que falle una de las tres → INESTABLE.** E1 y E3 fallan (E2 por sí
sola no habría bastado para sostener la solución).

## 5 · Las cuatro sensibilidades obligatorias (§9.5)

**S1 — solo indicadores de persona (I1, I2, I3; §2.5.c).** BIC mínimo en
**`k=4`** (interior, no en el borde), tras la regla de no-separación baja a
**`k_primario=3`**. **Cambia respecto al principal (6 → 3).** Este es
exactamente el patrón que §2.5.b predijo y declaró *antes* de ver el dato:
quitar los tres ejes de hogar (urbanización, nivel socioeconómico, acceso
digital) **colapsa la estructura aparente a la mitad de las clases**. La
independencia local violada por diseño (personas del mismo hogar
comparten I4–I7) está inflando el número de clases del ajuste principal —
tal como el pre-registro advirtió que sesgaría el resultado **a favor de
H-A y en contra de H-B**.

**S2 — partición de edad alternativa `{18–24·25–39·40–59·60+}` (§2.2).**
Reajustado el rango completo 1–8: BIC mínimo también en el borde (`k=8`),
regla de no-separación selecciona **`k_primario=7`**. **Cambia respecto al
principal (6 → 7).** Por instrucción explícita del pre-registro: **se
reporta con la advertencia pegada — el eje de edad no sostiene estructura
estable.** No se intentó forzar una congruencia de perfiles entre `k=6` y
`k=7` porque no son el mismo modelo (números de clase distintos no son
comparables perfil a perfil).

**S3 — formalidad vía módulo `trabajos`, 3 categorías (§2.4/§5.3.a).**
Operacionalización declarada aquí (el canon no fija la regla exacta): para
el trabajo principal (`id_trabajo=1`), `formal_ocupado` si `pres_8='08'`
(aportación a SAR/AFORE — proxy citado por el propio pre-registro),
`informal_ocupado` en otro caso; `no_ocupado` si la persona no tiene fila en
`trabajos`. BIC mínimo en el borde (`k=8`), regla de no-separación selecciona
**`k_primario=6`** — **no cambia** respecto al principal. La operacionalización
de formalidad no es la fuente de la inestabilidad del ajuste principal.

**S4 — BIC sin pesos, rango completo 1–8 (§5.2).** Mismo patrón: BIC mínimo
en el borde (`k=8`), regla de no-separación selecciona **`k_primario=6`** —
**no cambia** respecto al ponderado-reescalado. El reescalamiento de pesos
tampoco es la fuente de la inestabilidad.

**Lectura conjunta de las cuatro.** Dos sensibilidades (S3, S4) confirman
que la operacionalización de formalidad y el tratamiento de pesos no mueven
la selección. Las otras dos (S1, S2) **sí la mueven**, y por razones
distintas y ambas pre-registradas como riesgo antes de correr nada: S1
apunta al eje de hogar (§2.5.b), S2 al corte de edad arbitrario (§2.2). Ninguna
de las dos es un defecto del código — son exactamente los dos puntos donde
el propio pre-registro dijo, por adelantado, que la estructura podía ser
frágil.

## 6 · Correspondencia y dominancia, §6.0 — computadas sobre `k=6` aunque el resultado sea INESTABLE

El pre-registro exige evaluar esto **antes de escribir una sola línea de
conclusión** (§9.6), así que se reporta íntegro, con la advertencia de que
un desenlace INESTABLE lo vuelve no vinculante para canon (§7).

**Correspondencia (perfil modal de cada clase contra `modelo` §1.1.D, techo
4/6 — descriptores 3 y 4 no recuperables por construcción):**

| Descriptor | Definición (§1.1.D) | ¿Alguna clase lo recupera? |
|---|---|---|
| **1** Clasemediero urbano formal | `segsoc`=1 ∧ `tam_loc`=1 ∧ `est_socio`=3 | **Sí — una sola clase** (prevalencia 30.9 %): modal `formal` (p=.801), `tam_loc`=1 (p=.885), `est_socio`=3 (p=.479). Match limpio, sin competencia de otra clase |
| **2** Popular informal | `segsoc`=2 ∧ `est_socio`∈{1,2}; `tam_loc` sin restringir | **Ambiguo.** CUATRO clases (prevalencias 7.0 %, 5.2 %, 33.6 %, 13.5 %) tienen modal `informal` ∧ `est_socio`∈{1,2} simultáneamente. Por la regla de inyectividad se asigna a la de mayor probabilidad conjunta en las variables nombradas (7.0 %, conjunta ≈0.918×1.00=0.918). **Las otras tres NO se cuentan como recuperación — pero satisfacen la misma definición modal**, lo que es en sí mismo un hallazgo: el descriptor 2, tal como está definido, no distingue entre lo que el LCA separa en variantes por edad/urbanización/acceso digital |
| **5** Joven Gen Z urbano conectado | `edad`=18–29 ∧ `tam_loc`=1 ∧ `conex_inte`=1 | **Sí — una sola clase** (prevalencia 9.8 %): modal `18-29` (p=.840), `tam_loc`=1 (p=.873), `conex_inte`=`si` (p=.920). Match limpio |
| **6** Migrante/transnacional | `residencia`∈{EUA,Otro país} ∨ `remesas`>0 | **No.** Ninguna de las seis clases tiene `misma_entidad` como categoría NO modal — las seis tienen `misma_entidad` como modal (94.3 %–99.1 %). `extranjero` nunca es la moda de ninguna clase (es solo 0.43 % del universo). El componente `remesas` de la definición **no es verificable desde este LCA**: `remesas` no es indicador (§2.4, es auxiliar), así que el modelo no produce una probabilidad condicional para él — se declara la limitación en vez de inventar un sustituto |

**Correspondencia = 3 de 4 recuperables (1, 2, 5) → PARCIAL** (§6.0: SUFICIENTE
exige 4/4; aquí hay 3 limpios más una ambigüedad de asignación en el propio
2, y el 6 no se recupera en absoluto).

**Dominancia (§6.0, máxima diferencia absoluta entre clases por eje, margen
≥1.5× el segundo):**

| Eje | Distancia máxima entre clases |
|---|---|
| `est_socio` | **0.951** |
| `tam_loc` | 0.881 |
| `conex_inte` | 0.876 |
| `edad` | 0.753 |
| `formalidad` | 0.719 |
| `celular` | 0.416 |
| `migración` | 0.048 |

Razón entre el primero y el segundo: `0.951/0.881 = 1.08` — **muy por debajo
de 1.5**. → **"Sin eje dominante"**, tal como el pre-registro instruye
reportar cuando ningún eje alcanza el margen. `est_socio`, `tam_loc`,
`conex_inte`, `edad` y `formalidad` separan las seis clases con fuerza
comparable; ninguno "gana".

## 7 · Veredicto — tabla §6.1

**Ninguno de D1, D2, D3, D4 aplica limpio.** D2 exige `k=2` estable (no es
el caso: `k` seleccionado es 6, y el ajuste explícito de `k=2` en la tabla
de §2 no es la solución primaria bajo ninguna regla). D3 exige `k≥5` **estable**
con correspondencia **SUFICIENTE (4/4)** — falla en los dos requisitos:
correspondencia es PARCIAL (3/4, con ambigüedad en el 2), y la solución no
es estable (§4). D4 exige `k=3 o 4` estable (no es el `k` seleccionado por
la regla mecánica) o `k≥5` con correspondencia PARCIAL/NULA **estable** — la
correspondencia sí calza (PARCIAL), pero la estabilidad no (§4 falla en E1
y E3).

**El veredicto es D5 — INESTABLE.** Tres señales independientes, cada una
suficiente por sí sola bajo §3.5/§6.1, convergen:

1. **E1 falla** (1/50 arranques replican la mejor log-verosimilitud en
   `k=6`) y **E3 falla** (7 señales de frontera) — §4.
2. **S1 cambia la solución** (6 → 3) — y lo hace exactamente por la vía que
   el pre-registro predijo antes de correr nada (§2.5.b: los ejes de hogar
   inflan el conteo de clases y sesgan a favor de H-A). Esto activa la nota
   propia de la fila D5: *"si S1 muestra que los ejes de hogar dominan la
   solución, se habilita el LCA multinivel de §2.5 como extensión"* — que
   es exactamente lo que S1 mostró.
3. **S2 cambia la solución** (6 → 7) — el eje de edad, con corte declarado
   ARBITRARIO en dos de sus tres cortes (§2.2), no sostiene estructura
   estable.

**Nada de esto es apoyo al statu quo, y se dice con las palabras del propio
pre-registro (§1, §6.1·D5): "el desenlace INESTABLE no cuenta como victoria
de ninguna hipótesis... el statu quo no gana por empate."** H-A, H-B y H-C
quedan sin decidir por esta prueba: **la prueba no decidió.**

**Lo que SÍ vale la pena decir, con la precisión que separa un hallazgo de
un lugar común:** la forma de la curva de BIC (monótona decreciente,
mínimo en el borde del rango probado, §2) es el patrón que el pre-registro
reservó para D6 ("lo que hay es un gradiente, no clases"), y dos de las
cuatro sensibilidades (S3, S4) confirman que ese patrón no depende de la
operacionalización de formalidad ni del tratamiento de pesos — es robusto a
esas dos decisiones. Pero clasificar el desenlace como D6 puro pasaría por
alto que S1 y S2 **sí** mueven la solución, que es precisamente la condición
que la fila D5 nombra aparte y que el pre-registro no permite fundir en
D6 sin decirlo. Se reportan ambas lecturas explícitas — la mecánica de
decisión aterriza en D5 por la letra de §3.5/§6.1, y la forma de la curva
es congruente con la fenomenología de D6 — y se deja constancia de la
tensión en vez de resolverla por conveniencia. **Es una enmienda, no una
interpretación libre, si alguien de mesa decide que el patrón amerita
tratarse como D6 a pesar de S1/S2; esta nota no toma esa decisión.**

**Consecuencia sobre los seis descriptores de §1.1.D (bajo D5): nada
cambia en `canon/`.** No se reescribe `modelo` §1.1.D bajo ningún desenlace
(§6.1·D4, §7.8) — y bajo D5 la instrucción es aún más directa: la tabla no
se toca en absoluto. Lo que esta nota propone, **no ejecuta**, como
consecuencia de mesa: (a) evaluar si el LCA multinivel condicional de
§2.5 (clases de persona anidadas en clases de hogar) resuelve la
inestabilidad que S1 diagnostica; (b) si se decide fijar el corte de edad
en algún momento, hacerlo ANTES de repetir este LCA, dado que S2 muestra
que el resultado depende del corte elegido.

## 8 · Qué NO se movió (§6.2, verificado explícitamente)

- **`0 de 14` condicionales medidas sigue en 0.** Este LCA no estima ningún
  θ_k — sus indicadores son atributos, no reactivos de parámetro (misma
  garantía de C3 que el pre-registro cita en §2.4). **No se toca.**
- **`8 de 14`** (Fase B, `modelo` §1.1.F) **sigue en 8.** No se abrió
  ENVIPE, ENCUCI ni ENIF en esta sesión — solo ENIGH.
- **`4 de 144`** sigue congelado (`forense/hallazgos.md`, 31/jul/2026). No
  se tocó.
- **Los 22 g.l. reales del ajuste (7+15, ADR-51)** no cambian: un LCA no
  añade ni quita grados de libertad al ajuste del motor.
- El veredicto de identificabilidad de P2/ADR-51 no se toca — la
  subidentificación bajo atributos persiste, con su causa en la medición
  y no en la segmentación.
- **No se escribió ninguna columna de clase por persona al repo** (§4,
  prohibición de asignación modal). El entregable son parámetros
  agregados (`φ`, `π`) y probabilidades posteriores agregadas para el
  cálculo de entropía — nunca microdato etiquetado. `forense/notas/_p3_lca/`
  solo contiene tablas de índices y matrices de parámetros de clase (`k`
  filas), no una fila por persona.
- **No se tocó `canon/` ni `milpa/`.** Los únicos archivos nuevos son esta
  nota, `tests/p3_lca_data.py`, `tests/p3_lca_em.py`, `tests/p3_lca_run.py`,
  `tests/p3_lca_stage.py` y `forense/notas/_p3_lca/*.json`.

## 9 · Límite de lectura declarado (ADR-46) y reproducibilidad

**Microdato abierto:** `enigh2022_nc_csv.zip` → tablas `poblacion`,
`concentradohogar`, `hogares`, `trabajos` (columnas usadas: `segsoc`, `edad`,
`residencia`, `entidad`, `tam_loc`, `est_socio`, `celular`, `conex_inte`,
`ing_cor`, `remesas`, `factor`, `est_dis`, `upm`, `id_trabajo`, `pres_8`),
más los diccionarios de datos y catálogos de las cuatro tablas y
`metadatos_enigh_2022_ns.txt`. **No se abrió** `viviendas`, `ingresos`,
`gastoshogar`, `gastospersona`, `erogaciones`, ni ningún otro módulo de
ENIGH más allá de los cuatro necesarios. **No se abrió ENVIPE, ENCUCI ni
ENIF.**

**Entorno: sin numpy/scipy/pandas/sklearn, sin pip ni ensurecip
instalables** (confirmado antes de escribir una línea de EM — mismo límite
que documenta `tests/svystat.py` de la sesión CAL-CONF Fase B/ola 2). El LCA
completo (`tests/p3_lca_em.py`) está escrito en Python puro de librería
estándar, colapsando el universo a patrones de respuesta únicos agregados
(895 patrones para 217 375 personas en el ajuste principal) — lo que vuelve
factibles los 500 arranques por `k` que exige §3.4 sin necesitar
paralelismo ni aproximar el número de arranques hacia abajo.

**Reproducir:**
```
python3 tests/p3_lca_stage.py universo_meta
python3 tests/p3_lca_stage.py principal
python3 tests/p3_lca_stage.py s1
python3 tests/p3_lca_stage.py s2
python3 tests/p3_lca_stage.py s3
python3 tests/p3_lca_stage.py s4
python3 tests/p3_lca_stage.py e2
python3 tests/p3_lca_stage.py assemble
```
Todos los resultados numéricos citados en esta nota viven en
`forense/notas/_p3_lca/resultados.json` (consolidado) y en los
`ck_*.json` individuales de la misma carpeta — auditables línea por línea,
no transcritos de memoria.

---

*Suite (`tests/check.py` y `tests/check.py --baseline`) corrida como último
paso, después de cerrar esta nota — resultado en el mensaje de cierre de
sesión/PR, no en este cuerpo, para no tener que reabrir el archivo si algo
cambia entre el commit de la nota y el commit final.*
