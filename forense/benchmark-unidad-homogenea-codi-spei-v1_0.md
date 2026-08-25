# BENCHMARK · Unidad homogénea CoDi↔SPEI — bordes del programa y crítica publicada · insumo para la firma de `FP-104`

**25/ago/2026 · sesión de dirección (maestra), conversación del proyecto · contra `origin/main = c502a43` (clonado y verificado en la misma sesión).**
**CONTADOR: cero, declarado** — este documento no mueve Hito D, llaves, tiers ni `milpa/`; estresa una cláusula ya propuesta y produce propuestas para mesa. **PROPUESTA, no sellada.**

**Mandato.** Firma de mesa en la conversación de dirección, 25/ago/2026, verbatim: *«Pues si el benchmark fue para esos pares de encuestas hagamos lo mismo para CODI/SPEI.»* — el referente es `forense/benchmark-enlace-invarianza-v1_0.md` (13/ago) y su cadena (`EDGE-CASES-y-literatura-reciente.md` §E5 → `ADR-80(b)`, estándar «argumento de vinculación declarado»). Este documento replica ese método para el par `CoDi ↔ SPEI` de la condición A de `R3.4`.

**Procedencia, por clase.**
- Repo, tipo (1), leída en esta sesión contra `c502a43`, con archivo:línea en cada cifra: `forense/ficha-r34-conda-v2-spec.md` (§2, §5, §10.4, §10.6, §10.7), `forense/notas/2026-08-24-r34-conda-v2-cierre.md:62,107-108`, `forense/notas/2026-08-25-serie-homogenea.md`, `forense/firmas-pendientes.tsv` fila `FP-104`, `canon/gobernanza-v1_15.md` (ADR-160/168(c)/170).
- Externa, tipo **(3+)**, mismo estándar que el precedente: cada cita verificada en esta sesión contra ≥1 resultado de búsqueda con título/autores/fuente exactos, **nada abierto byte a byte** desde este entorno (sin salida a esos dominios) — toda URL externa lleva de facto la marca `SIN-FETCH` de `A.6` y se cita como localizada, no como leída.
- Ninguna cifra proviene del espejo del proyecto.

**Perímetro.** No toca `canon/`, no re-corre microdato, no re-computa la razón, no adjudica. La escala de lectura vigente es la del §5 de la ficha (`A < 10 %`, `ADR-37`, `ASIGNADO`) y no se mueve aquí. Quien aterrice este archivo lo hace verbatim (sha256 al pie) y en commit propio.

**Método (idéntico al precedente).** Cada borde se estresa por dos lados: (a) **bordes del programa** — condiciones reales del repo donde la cláusula podría no aplicar limpio; (b) **crítica publicada** — literatura 2017-2026 que ataca al método mismo. Cada borde cierra con veredicto `SOSTIENE / ACOTA / ROMPE`. Estrés que no rompe es certificación, y también se reporta.

---

## §A · La cláusula bajo estrés

La enmienda **§10.7** de la ficha propone leer las filas `A1`/`A2` del §5 con la cláusula sustituida: de *«razón computada con enlace firmado»* a *«razón computada **sobre unidad homogénea, sin enlace**»*. Bajo ella, el veredicto propuesto (no firmado) es **fila A1 — A satisfecha**: razón CoDi/SPEI en **número de operaciones de usuarios finales** (Cuadro A 8 vs Cuadro A 1 de los informes anuales de Banxico) = 0.08254 % (2020) · 0.12318 % (2021) · 0.10793 % (2022) · 0.10507 % (2023) · 0.07803 % (2024); robustez en **monto a pesos constantes** = 0.00139 % · 0.00202 % · 0.00206 % (2022-2024). Cinco de cinco y tres de tres, dos órdenes de magnitud bajo `A < 10 %`.

Lo que este benchmark pregunta: **¿hay algún borde del programa o crítica publicada bajo el cual esa lectura sea inválida o el veredicto pueda voltear?**

---

## §B · Bordes del programa

### B1 · El borde que ya ocurrió: dos lecturas legales, veredictos opuestos — es la razón de ser de la cláusula
`forense/notas/2026-08-24-r34-conda-v2-cierre.md:107-108`: **0.35 %** (257.8 mil cuentas CoDi / 73.5 M personas físicas SPEI → A *pasaría*) contra **12.68 %** (0.09/0.71, capa máquina pre-D3 → A *fallaría*). Mismo par, dos unidades, veredictos opuestos — el edge case en carne viva que `A-bis` 3 existe para atrapar y que `ADR-160` documentó con `PARO`. La unidad homogénea no es un atajo: es la única lectura del par que no depende de un tipo de cambio nunca firmado. **Veredicto: SOSTIENE** — el borde certifica la necesidad de §10.7, no la debilita.

### B2 · Margen extensivo vs. intensivo: «operaciones» mezcla quién usa con cuánto usa
Riesgo teórico real: un conteo de operaciones puede divergir del constructo de adopción (usuarios). La literatura de difusión lo formaliza — Comin & Mestieri distinguen el margen extensivo (rezago de adopción) del intensivo (penetración de uso) y documentan que pueden evolucionar en direcciones opuestas entre países (§C3). La reserva 4 de §10.6 ya lo declara.
Lo medido, del árbol y de fuentes externas independientes del par: **todas las lecturas legítimas caen del mismo lado del umbral con holgura** — intensivo-conteo 0.078–0.123 %, intensivo-valor 0.0014–0.0021 %, extensivo interno 0.35 % (cuentas/personas, la lectura que `A-bis` 3 prohíbe como *adjudicadora* pero que sirve como triangulación de dirección), y extensivo externo ~1.6 % de la población ha usado CoDi al menos una vez a 2024 (§C4, OECD). La única lectura ≥10 % jamás producida (12.68 %) no es una unidad del par sino una proporción de otra capa que la firma D3 retiró. **Veredicto: SOSTIENE, con la reserva 4 viajando tal cual** — los márgenes son constructos distintos (la crítica es válida en general) y aquí no divergen en el lado del umbral (la crítica no muerde este caso).

### B3 · Denominador: ¿«todo SPEI» infla la vara con tráfico no comparable?
Dos capas, ambas verificables:
1. **La serie ya es el corte de usuario final.** El numerador del denominador no es el volumen interbancario bruto: el Cuadro A 1 reporta operaciones de **usuarios finales** (nota `1/`: tercero a tercero, incluye CoDi) — `forense/notas/2026-08-25-serie-homogenea.md:142`. El re-corte «retail» grueso ya está hecho por elección de serie.
2. **Cota aritmética contra cualquier re-corte fino.** Con razón ~0.10 %, para cruzar `10 %` el subconjunto «relevante» del denominador tendría que ser **menor a ~1/100** de las operaciones de usuarios finales. El propio informe de Banxico reporta que la **mayoría** de las operaciones SPEI son de bajo valor (<MX$8,000) (§C5) — cualquier re-corte plausible (bajo valor, móvil, P2P) mueve el denominador por un factor de 2-3, no de 100. El veredicto es insensible al re-corte por dos órdenes de magnitud.
**Veredicto: SOSTIENE.** Se deja escrita una sensibilidad opcional **no bloqueante** (§E, P2) por si mesa quiere el cinturón además de los tirantes.

### B4 · Contención parte/todo (CoDi ⊂ SPEI)
Reserva 1 de §10.6, ya computada en la corrida: la variante excluyente `CoDi/(SPEI−CoDi)` mueve la razón entre 0.00006 y 0.00015 pp y no cambia de lado en ningún año. **Veredicto: SOSTIENE** — borde medido, no argumentado.

### B5 · El confusor de quince años (§2 de la ficha): nivel vs. causa
La firma A1 adjudica el **nivel** de la condición A, no la atribución causal a `utilidad_marginal_sobre_sustituto`; el §10.6.2 ya declara que ninguna lectura atribuye la brecha entera a ese driver. Dos observaciones que acotan sin adjudicar: (i) la serie no muestra despegue — la razón *cae* de 0.123 % (2021) a 0.078 % (2024), cinco años post-lanzamiento, lo que debilita la lectura «solo es joven» como explicación completa del nivel; (ii) la literatura de difusión (§C3) separa rezago de penetración precisamente porque el tiempo no garantiza el cierre. **Veredicto: ACOTA la lectura causal, no ROMPE el veredicto de nivel** — la reserva §2 viaja con la firma, como ya estaba.

### B6 · Borde nuevo, declarado por honestidad: circularidad de emisor
Numerador y denominador salen del **mismo emisor** (Banxico, mismos informes anuales). Para homogeneidad metodológica es la fortaleza del diseño; para independencia de fuente es un límite: no existe una serie de operaciones CoDi de un emisor distinto del regulador, y las corroboraciones externas de nivel (§C4-C6) reprocesan en última instancia datos del propio Banxico. Es un límite del universo, no un defecto de la ficha — se declara para que la firma no lo herede en silencio. **Veredicto: SOSTIENE con límite declarado.**

---

## §C · Crítica publicada (2017-2026) — cada cita (3+), verificada por título/autores/fuente en esta sesión

**C1 · El conteo de operaciones por instrumento es la métrica estándar del campo, no una improvisación local.** CPMI (2017), *Methodology of the statistics on payments and financial market infrastructures in the CPMI countries (Red Book statistics)*, CPMI Papers No 168, BIS — la metodología canónica de las estadísticas de pagos usa el **volumen (número) de operaciones sin efectivo por instrumento** como indicador central de uso (tabla comparativa T5 del portal de datos del BIS), e incorpora *fast payments* como categoría desde esa revisión. → La unidad elegida por §10.3 es la unidad con la que el campo mide exactamente esta pregunta. **SOSTIENE.**

**C2 · La lectura por operaciones para pagos rápidos es la práctica vigente del propio CPMI.** Aksonthung, Kosse & Mustafi (2026), *commentary* del CPMI sobre las Red Book statistics 2024, BIS — los pagos rápidos se usan crecientemente para pagos de bajo valor en economías emergentes y avanzadas, medidos por volumen de operaciones. **SOSTIENE.**

**C3 · La crítica de márgenes es real y publicada — y por eso la reserva 4 debe viajar.** Comin & Mestieri, *If Technology Has Arrived Everywhere, Why Has Income Diverged?* (NBER WP 19010; publicado en *AEJ: Macroeconomics*, 2018) — margen extensivo (rezago de adopción) y margen intensivo (penetración de uso) son constructos distintos que documentadamente divergen entre países y tecnologías. → Un conteo de operaciones no es «adopción» a secas; adjudica el par solo porque aquí **todas** las lecturas de ambos márgenes caen del mismo lado del umbral (§B2). **ACOTA — exactamente lo que la reserva 4 de §10.6 ya encoda.**

**C4 · Corroboración externa del nivel, margen extensivo puro.** OECD (2025), *Competition in Mobile Payment Services — Note by Mexico*, DAF/COMP/WD(2025)12 — CoDi representa menos del 1 % de las transacciones diarias; ~11.9 millones de operaciones acumuladas al 1T-2024; ~1.6 % de la población lo ha usado al menos una vez. → Nivel bajo confirmado por un organismo distinto del par, en dos márgenes, ambos ≪10 %. **SOSTIENE.**

**C5 · La composición del denominador, del propio emisor.** Banco de México, *Informe anual sobre las infraestructuras de los mercados financieros* (edición 2023; localizado vía cobertura de prensa especializada, 2024) — la adopción de CoDi avanzó por debajo de lo esperado; SPEI procesó ~3,823 millones de operaciones en 2023, la mayoría por montos menores a MX$8,000. → Sostiene la cota de §B3.2: el denominador de usuarios finales ya es mayoritariamente bajo valor. **SOSTIENE.**

**C6 · Contexto de diseño del par.** World Bank (2021), *Fast Payments Case Study: Mexico (SPEI)* — SPEI opera tanto alto valor como retail y CoDi es una funcionalidad montada sobre SPEI. → Refuerza B4 (parte/todo) y la elección de comparar dentro del mismo riel. **SOSTIENE.**

*(Nota de alcance, mismo matiz que el precedente declaró para sí: C4-C6 corroboran el **nivel** del numerador y la **composición** del denominador; ninguna de ellas computa la razón del par en la unidad de §10.3 — esa razón es del programa, con sus archivos y líneas.)*

---

## §D · Qué cambia en la firma por este benchmark

**Nada del veredicto y nada del texto de §10.7.** La cláusula «razón computada sobre unidad homogénea, sin enlace» sale del estrés **certificada**: la unidad es la métrica estándar del campo (C1-C2), el único borde que alguna vez volteó el veredicto era exactamente el que la cláusula elimina (B1), y los cuatro bordes restantes están medidos (B4), acotados con cota aritmética y respaldo del emisor (B3, C5), o viajan como reservas ya escritas (B2/C3, B5). Se **añade** al expediente: un borde nuevo declarado (B6, circularidad de emisor) y una corroboración externa citable del nivel (C4). Ninguna reserva se retira; ninguna nueva gatea.

---

## §E · Propuestas listas para mesa (ninguna sellada aquí)

**P1 — recomendada.** Firmar `FP-104` fila **A1** con la enmienda §10.7 tal cual, reservas de §10.6 y §2 incluidas, citando este benchmark como insumo — mismo patrón que `ADR-80(b)` («usa lo que el benchmark ya dijo»). Verbatim sugerido: `FIRMO FP-104: fila A1 con enmienda 10.7 (unidad homogénea, sin enlace), solo pata A, reservas de la ficha + benchmark CoDi-SPEI incluidos.`

**P2 — opcional, explícitamente NO bloqueante.** Un acto barato futuro de sensibilidad de denominador (re-correr la razón contra el sub-agregado de bajo valor/móvil de SPEI si los informes lo desglosan en unidad compatible), con la cota de §B3.2 escrita como expectativa: no puede voltear el veredicto salvo que el re-corte reduzca el denominador ~100×. Si mesa no la pide, no corre y no gatea nada.

---

**Cierre.** CONTADOR: cero. Este archivo se aterriza verbatim en `forense/` (nombre sugerido: este mismo), en commit propio, con su sha256 registrado por quien lo aterrice; la fila `FP-104` sigue `ABIERTA` hasta la firma de mesa.
