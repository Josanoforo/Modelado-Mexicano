# ENCARGO · ACTO GEN2-CLASE-AMAI-1 · El eje que el §3 llama «el sesgo que más muerde»: nivel socioeconómico AMAI (regla 2024 o la mejor aproximación por instrumento) construido en ENIF, ENVIPE, ENCIG, ENIGH y ENDUTIH; pisos por NSE para toda conducta adoptable; y la cobertura del modelo por clase, con cifras

> ENTORNO: **CAJA** — microdato de olas abiertas de los cinco instrumentos. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `474a126e` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-clase-amai-1` (o la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: sella CALC por instrumento (`cuenta_gen2: SI`, `adopta: NO`); mueve «N conductas con piso por NSE» (impreso en la nota); no evalúa prospectivamente; la entrada de NSE como eje del marcador es FP para mesa.

## 1 · OBJETIVO
(P1) Tabla de factibilidad por instrumento: cuáles de las variables de la Regla AMAI 2024 (escolaridad del jefe, baños, autos, internet, ocupados, dormitorios… según la nota metodológica AMAI, citada) existen por **texto de pregunta** en ENIF 2021/2024, ENVIPE 2024/2025, ENCIG 2023/2025, ENIGH 2022/2024, ENDUTIH 2023–2025; dictamen por instrumento: CALCULABLE / APROXIMABLE (con qué variables faltan y qué proxy) / NO-CONSTRUIBLE. Si el catálogo de Astra (U1, ADENDA-1) ya trae esta tabla, se cita y se completa, no se rehace. (P2) Construcción del NSE (o su aproximación declarada) como variable derivada por instrumento, con validación contra la distribución nacional AMAI publicada (cita): si la distribución se desvía más de un umbral fijado antes, se rotula `APROXIMACIÓN-DESVIADA` y se dice. (P3) Pisos por NSE (7 niveles AMAI o agrupados A/B–C+ · C–C− · D+–E, declarado antes) para toda conducta adoptable de esos instrumentos, con IC de diseño; unidad y universo por conducta. (P4) **Cobertura del modelo por clase**: qué fracción de las celdas del catálogo (U1) son estimables por NSE con n suficiente, y en qué niveles el modelo no tiene nada — la cifra que el §3 pide y nadie ha dado. FP: ¿entra NSE al marcador como eje? (recomendación al cierre, con la potencia medida).
«Hecho»: tabla de factibilidad por instrumento con cita de pregunta · ≥ 3 instrumentos CALCULABLE o APROXIMABLE con CALC sellado y `verify` REPRODUCE · tabla conducta × NSE × ola con RESULT por id · cobertura por clase con conteos derivados · FP con recomendación · módulo de auditoría (¿qué parece cultura y es clase?) · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas, verbatim
**D4 de la tarde del 23/sep (FIRMAS-12)**: «AMAI NSE como corte de clase: U1 declara variables por instrumento; U5 lo incorpora si es calculable en ≥ 2 instrumentos; no se abre frente nuevo.» INTERPRETACIÓN-DECLARADA: U5 (región) cerró su lote 1 sin el corte de clase; este acto es el «lo incorpora» con dueño propio, no un frente nuevo de medición sino el eje que el §3 exige. **F-U5-2** (umbral de n y supresión fijados en la spec). **Regla 6.**

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` `grep -c AMAI canon/catalogo-del-mexicano-v1_0.md` → 1 (una mención; la tabla de variables por instrumento puede no existir: P1 lo verifica y la hace). Ejes del marcador hoy: sexo, edad, escolaridad, localidad, formalidad, cuenta, remesas, y región (lote 1). `[LEÍDO]` informe de competencia 23/sep: AMAI como estándar reconocido por la industria; pipeline público que calcula NSE por colonia con INEGI (afirmación de tercero). `[SUPUESTO]` que ENVIPE/ENCIG tienen módulo de vivienda con las variables de la regla (verificar por FD).

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -ic 'AMAI\|NSE'` → 0. `git ls-remote --heads origin | grep -i 'amai\|clase'` → 0.

## 5 · PIEZAS
P1 factibilidad por texto → P2 NSE por instrumento con validación → P3 pisos por NSE (COMMIT-1 antes de abrir cada instrumento) → P4 cobertura y FP.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja; lo no alcanzado va a NO-CORRIDO. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir olas reservadas · b) reescribir sellos · c) adoptar; meter NSE al marcador sin firma · d) cambiar agrupación o umbrales después de COMMIT-1 · e) NUBE.

## 8 · COMPUERTAS
«Agrupación de niveles y umbral de supresión antes de abrir» protege: **congelar**. «NSE entra al marcador solo por firma» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/AMAI-*`, `data/corrida0/CALC-*-NSE-*`, `tools/dominios/amai/`, `forense/analisis/clase-amai/`, `replay-evidencia.tsv`, TSV de gobierno, nota, L0, cascada. Ajeno: marcador, celdas-D, catálogo (lo cita), `milpa/`. En CAJA: PISOS-GEN2-2, SALUD, DONDE-CAMBIO (lectura de olas comunes: sin conflicto de escritura).

## 10 · LO QUE NO HACE · SUCESORES
No adopta, no cambia el marcador. Sucesores: FIRMAS-16 (eje NSE); catálogo v1.1; informe v1.3 §cobertura por clase.
