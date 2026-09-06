# `ACTO MAESTRA38-L18` · `comunicacion.inseguridad.ver_oir_callar` (`R10.3`) sobre LAPOP México 2004 — resultados

**Pieza 3 de 3 del `ACTO MAESTRA38-LOTE-LAPOP`.** Ejecuta, sin editarla, la spec sellada
`prereg-caja-S8-L18` (`sha256 a836582d0d6e3c7e96623b85d89280fd003c2925d4cb9e5602708d8337aa4d20`,
verificado al arrancar y al cerrar). Base `origin/main = a5350e59`. Entorno **UBUNTU con corpus**.

> **Ésta es la primera falsación real de `R10.3`.** `ya_medido.py` → **`NUNCA-MEDIDA`**. Ni
> `MAESTRA34-N5` (ENDIREH, acotada a violencia contra la mujer) ni `MAESTRA36-N6` (CNGMD, sesgo de
> selección: sólo denuncias que ocurrieron, sin denominador de quienes callaron) corrieron un
> número contra ella. Nadie la había medido.

---

## 1 · Universo — el conteo que la spec pedía y nadie había hecho

Spec §0.3 dejó escrito que **nadie en el corpus había contado** cuántos casos de 2004 caen en el
subuniverso del módulo `AOJ`, y pre-registró la expectativa (5–10 %), no el número. Contado:

| | |
|---|---|
| víctimas (`vic1`=1) | **268** de 1 556 → tasa de victimización **17.22 %** |
| víctimas con `aoj1` válido | **266** |
| denunció (`aoj1`=1) | **94** |
| **no denunció** (`aoj1`=2) — el desenlace | **172** |
| **no-víctimas con `aoj1` válido** | **0** |

**El gateo es del cuestionario mismo, verificado, no supuesto.** `1671516622CAM Mexico
Questionnaire 2004.pdf` (`sha256` COINCIDE), línea 215: *«`AOJ1`. **[Si responde "Sí" a `VIC1`]**
¿Denunció el hecho a alguna institución?»*, con códigos `(1) Sí · (2) No lo denunció · (8) NS/NR ·
(9) Inap (no víctima)`. Los 0 no-víctimas con `aoj1` válido lo confirman contra el dato.

La tasa real (**17.22 %**) es **el doble** del extremo alto de la expectativa pre-registrada (5–10 %):
la spec anticipó un subuniverso más chico del que resultó. Se declara — a favor de la pieza, porque
es lo que permitió que `C_completo` sí fuera estimable.

## 2 · La dirección de la escala `B`, resuelta contra el cuestionario

`b18` y `b10a` son escalas 1..7 **sin etiquetas de valor** en el `.dta`/`.sav` de 2004. La spec
exigió resolver la dirección **antes** de calcular y no heredarla a ciegas del `.dta` de 2019.
Resuelto contra el cuestionario (Tarjeta «A», pág. 89-90), verbatim:

> *«Esta tarjeta contiene una escala de 7 puntos; cada uno indica un puntaje que va de **1- que
> significa NADA hasta 7- que significa MUCHO**.»* — y bajo la batería: `1 2 3 4 5 6 7 · Nada … Mucho`

`B10A` («¿Hasta qué punto tiene confianza en el sistema de justicia?») y `B18` («…en la Policía?»)
están dentro de esa batería. **Misma dirección que 2019** (`1='Nada'`, `7='Mucho'`): menor valor =
menos confianza. **No se invierte.**

**Corte principal, declarado antes de calcular:** mitad inferior de confianza = `{1,2,3}` (4 es el
punto medio y **no** entra). **Corte de robustez, también corrido:** `{1,2,3,4}`.

`aoj11` (1 Muy seguro … 4 Muy inseguro) y `aoj12` (1 Mucho … 4 Nada) sí traen etiquetas y coinciden
verbatim con el cuestionario (líneas 248-250 y 259-260).

## 3 · Diseño y escala

Estrato `mestrat` (4) × PSU **`msec`** («Sección electoral», 131 pares estrato×PSU) — 2004 no trae
`upm`/`estratopri`/`cluster`, hallazgo del censo A.4 de este acto. **Sin ponderar:** `wt` de 2004
está vacía (0 válidos de 1 556). IC95 por bootstrap de conglomerado, 10 000 réplicas, seed 42.
Declarado: el IC no incorpora efecto de diseño más allá del conglomerado documentado.

Escala (A-bis 3): 1 celda principal (2 ramas) + 3 diagnósticas (2 ramas cada una) + 1 verificación
cruzada `b10a` + 1 robustez de corte = **14 celdas**, 7 contrastes, una sola ola.

Los tres proxies se tratan como **operacionalizaciones alternativas del mismo constructo**, no como
antecedentes conjuntos (spec §3): el texto de la regla no exige que las tres caras coincidan.
`INDICE_CONTEXTO` = número de indicadores en dirección de inseguridad/desconfianza (0–3);
`ALTO` = 2 ó 3, `BAJO` = 0 ó 1.

## 4 · Resultados — la variable de interés es el **silencio** (`DENUNCIA=0`)

| celda | p (silencio) | IC95 | n | num |
|---|---|---|---|---|
| `INDICE_CONTEXTO` **ALTO** | 64.9123 % | `[58.90, 70.81]` | 171 | 111 |
| `INDICE_CONTEXTO` **BAJO** | 67.4157 % | `[56.96, 76.60]` | 89 | 60 |

> **`C_completo` = −2.5034 pp · IC95 `[−13.899, +10.030]` · contiene 0**

De las 266 personas del universo, **260** entran a `C_completo`; las **6** restantes tienen alguno
de los tres indicadores faltante y quedan fuera de la construcción del índice. Están contadas, no
desaparecidas.

**Diagnósticas y robustez:**

| contraste | `d` | IC95 | |
|---|---|---|---|
| `C_barrio` (`aoj11`) | −0.622 pp | `[−12.399, +11.137]` | contiene 0 |
| `C_policia` (`b18`≤3) | +4.262 pp | `[−6.654, +15.655]` | contiene 0 |
| `C_justicia` (`aoj12`) | +1.893 pp | `[−12.057, +16.896]` | contiene 0 |
| `C_justicia` por `b10a` (verificación cruzada) | +5.531 pp | `[−5.617, +17.117]` | contiene 0 |
| `C_completo` con corte `b18`≤4 (robustez) | −5.167 pp | `[−17.678, +8.020]` | contiene 0 |
| `C_policia` con corte `b18`≤4 (robustez) | +5.797 pp | `[−7.994, +19.315]` | contiene 0 |

**El veredicto no depende del corte.** Con `{1,2,3}` y con `{1,2,3,4}`, `C_completo` sigue negativo
y sigue conteniendo 0. La verificación cruzada por `b10a` va en el mismo sentido que `aoj12` y
tampoco despeja el cero.

## 5 · Veredicto `B-bis`

> ## **`NO-DISCRIMINA`**
> IC95 de `C_completo` contiene 0 (spec §4).

**Y aquí el corazón de la regla SÍ se midió** — a diferencia de `L5`, donde `C_completo` cayó por
guardia. Las dos celdas de `C_completo` tienen numeradores 111 y 60, muy por encima de la guardia
de 10. Éste es un `NO-DISCRIMINA` sobre el contraste que la regla afirma, no un repliegue a las
diagnósticas.

Las tres diagnósticas tampoco discriminan, y además **no van todas en el mismo signo**
(`C_barrio` negativo, `C_policia` y `C_justicia` positivos): no hay «corroboración convergente por
proxy» que reportar, ni desacuerdo limpio que adjudicar — los seis IC contienen 0.

### 5.1 · Fila `B-bis`: qué significa que el falsador no refute

`R10.3` es `[FUERTE]` — el tier más alto — y afirma que el contexto de inseguridad/autoridad no
confiable **produce** el silencio. Sobre las víctimas de delito de 2004, **el silencio es casi
idéntico se perciba o no el contexto como inseguro**: 64.9 % contra 67.4 %, con el punto **al revés**
del signo esperado. Que el IC contenga 0 con `n=260` no es una anécdota de muestra chica: es que la
separación que la regla predice **no aparece**.

Eso **no la refuta** —`NO-DISCRIMINA` no es `CONTRARIA`— y este acto no la mueve. Pero es la primera
vez que hay un número contra una `[FUERTE]` en este dominio, y el número no la sostiene. Lo que sí
queda establecido: **el silencio es masivo y casi invariante** — 172 de 266 víctimas (64.7 %) no
denunciaron, con o sin contexto de desconfianza. La regla describe bien el nivel; lo que no se
sostiene es su `SI…ENTONCES`, que es lo que la hace una regla y no una descripción.

Una lectura alternativa, declarada y no adjudicada aquí: el propio `aoj1b` («¿Por qué no denunció?»)
reparte los 168 motivos entre `No sirve de nada` (90), `No tenía pruebas` (28), `No fue grave` (25),
`Es peligroso y por miedo de represalias` (22) y `No sabe adónde denunciar` (3) — el motivo de
**miedo** que el `PORQUE` de la regla nombra es el cuarto, no el primero. Es descriptivo, no un
falsador pre-registrado, y se cita como tal.

## 6 · `se_mueve_si` — verbatim de spec §5

> Si entre las víctimas de 2004 la tasa de silencio (no denuncia) en contexto de alta
> inseguridad/desconfianza (`INDICE_CONTEXTO=ALTO`) **no es mayor** que en contexto bajo, la regla
> se rompe. Si `C_completo` cae por guardia (`NO-ESTIMABLE`), `se_mueve_si` se lee sobre las tres
> diagnósticas juntas, per §4.

**`C_completo` no cayó por guardia**, así que `se_mueve_si` se lee directo sobre él: la tasa de
silencio en contexto ALTO (64.91 %) **no es mayor** que en BAJO (67.42 %). La condición del
`se_mueve_si` **se cumple** en el punto — pero el IC contiene 0, así que el veredicto pre-registrado
que corresponde es `NO-DISCRIMINA`, no `CONTRARIA`. Se reportan las dos cosas: la condición literal
se cumple, y el falsador no alcanza a excluir el cero.

## 7 · Alcance — una sola ola, y por qué

Spec §0.2 corrigió a `N10 §2.6`: el desenlace del módulo `AOJ` (`aoj1`/`aoj1a`/`aoj1b`) **no** existe
en «las mismas cinco olas», existe **sólo en 2004**. Re-verificado por el censo A.4 de este acto:
`AOJ1`/`AOJ1A`/`AOJ1B` **NO-ENCONTRADO** en 2006 (ambas capitalizaciones), y `aoj1` NO-ENCONTRADO en
2019, 2021 y 2023. El antecedente sí es estable en el tiempo (`aoj11` y `b18` están en las cinco
olas), y por eso se cita como contexto en §1.1 de la spec — pero **el falsador es de una sola ola**,
y esa limitación es del corpus, no del diseño.

## 8 · Reservas y qué NO hace

Asociación transversal, sin identificación causal. Una sola ola, **sin ponderar**. El
`PORQUE` de la regla («adaptación racional, no timidez») es mecanismo, no antecedente exigible: no
se mide en este falsador. El `.sav` gemelo (`1658622845…`, `sha256` COINCIDE) se abrió para
confirmar que da **marginales idénticas** al `.dta`; se midió sobre el `.dta`.

No mueve el tier de `comunicacion.inseguridad.ver_oir_callar` (`[FUERTE]`,
`modelo-decision-v4_0.md:585`) — eso es de mesa. **No sella la clasificación `MEDIBLE-COMO-ESTÁ`
que `N10` propone**: la propuesta sigue siendo de dirección/mesa, y este acto sólo demuestra que la
regla, en efecto, era medible. No extiende el falsador a 2006/2019/2021/2023. No reclasifica
`salud.atencion.grave` ni `salud.vacunacion.disponible` (`S6`/`S7`, otro lote). No toca canon,
`milpa/tramite.yaml`, manifiesto, cola, relaciones, staging ni ninguna spec.
