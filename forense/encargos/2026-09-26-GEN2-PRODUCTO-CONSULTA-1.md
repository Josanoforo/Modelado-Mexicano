# ENCARGO · ACTO GEN2-PRODUCTO-CONSULTA-1 · Lo que un usuario externo hace con el Benchmark: una consulta que devuelve, para una conducta y un segmento, el piso con su IC, unidad, ola, origen, PROSPECTIVA/RETROSPECTIVA, cita verificable y columna de oferta — como CLI, como archivo estático consultable desde Pages, y como contrato documentado para el reto público

> ENTORNO: **NUBE** — catálogo, motor, RESULT sellados, `docs/`. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `34949751` (re-deriva al abrir) · una sesión por rama (varias ramas si el acto lo pide, declaradas) · MODELO: Opus · MODO: **AUTÓNOMO-AMPLIO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
CONTADOR: cero mediciones; no adopta; ninguna cifra que la consulta devuelva puede diferir del RESULT sellado que cita (test de equivalencia sobre todo el catálogo).

## 1 · OBJETIVO
El programa tiene 285 corridas, un catálogo, un motor y un tablero, y **ningún camino por el que alguien de fuera haga una pregunta y reciba una respuesta citable**. (P1) **Contrato de consulta** (`docs/consulta.md`, spec primero, D-15): entrada = conducta (por id de catálogo o por texto con búsqueda) + segmento (sexo, edad, escolaridad, localidad, formalidad, región, NSE) + instrumento/ola opcional; salida = punto, IC (tipo: diseño / calibrado / IC-CON-R), unidad, ola, PROSPECTIVA/RETROSPECTIVA, origen del piso, `RESULT-*` y CALC con hash, columna de oferta si es marginal de mercado, tier y falsador de la regla SI-ENTONCES si existe, y **qué no puede contestar** (segmento no estimable por n, dominio no medido, ola reservada) con la razón. (P2) **CLI** `python3 tools/benchmark.py consulta …` sobre el catálogo vigente (reusar `tools/consulta.py` de RENDIMIENTO-1 y `vista.py`), salida humana y JSON; `verificar <RESULT>` que reproduce la cadena hasta el sello. (P3) **Consulta estática en Pages**: exportar el catálogo a `docs/data/catalogo-v1_N.json` (derivado por comando, tamaño acotado) y una página `docs/consultar.md` con búsqueda del lado del cliente (sin servidor, sin dependencias externas: CSP de Pages), que muestre exactamente lo que el contrato define y enlace a «Verifica en 5 minutos». (P4) **Contrato del reto público** (`docs/reto.md` v1.1): cómo un tercero entrega predicciones para una familia 2027 (formato, sello previo, recibo, comparación primaria) usando el mismo contrato de consulta como formato de salida. (P5) Pruebas de uso: cinco preguntas reales (una por dominio) documentadas en `docs/ejemplos.md` con la salida completa y su verificación.
«Hecho»: contrato en `docs/consulta.md` · CLI con tests (incluido el de equivalencia catálogo ↔ salida) · `docs/consultar.md` funcional en un navegador sin red (probado, captura o registro en la nota) · `docs/reto.md` v1.1 · cinco ejemplos verificados · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
D2 (benchmark auditable; no promete cambios entre olas; declara dónde ganan los otros), F-FRONT-1/2 (nombre; términos de uso en la salida), reto público (plan de visibilización §3.6, aprobado en bloque). Regla 6 (la consulta no recomienda retadores; devuelve pisos).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` `tools/consulta.py` (RENDIMIENTO-1, #1156?) con `result/corrida/celda/payload/fp`; `tools/vista.py`; catálogo v1.1 (`canon/catalogo-del-mexicano-v1_1.{md,tsv}`); tabla de piso v1.0 (72 filas); `docs/` Jekyll simple; motor `milpa/src/emisor.py` con `emitir_binaria` GEN2 (B1). `[SUPUESTO]` que Pages sirve JSON estático y JS inline (sí, sin CSP restrictiva por defecto); si la sesión no puede probar Pages (no activa hasta el domingo), prueba local con `file://` y lo dice.

## 4 · YA HECHO / YA DECIDIDO
`ls docs | grep -c 'consulta\|consultar\|ejemplos'` → 0. `ls tools | grep -c benchmark` → 0.

## 5 · PIEZAS
Las decide la sesión; sugerencia: contrato → CLI → export JSON → página → reto v1.1 → ejemplos.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR) + AMPLITUD DE MANDATO
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja.
**Amplitud (mandato de mesa, 26/sep: «resolvemos antes las firmas y las dudas, y le damos la suficiente amplitud a la sesión para que decida»):** el orden, la agrupación en piezas, la profundidad por objeto y qué se difiere los decide la sesión; una sola hoja de firmas al cierre (no una FP por instrumento durante el acto); lotes D-11 de hasta cuatro piezas por PR, o más de un PR por acto si el volumen lo pide (se declara). Pregunta a mesa prevista: **ninguna**; si surge una de contenido, se resuelve con la opción recomendada y se rotula para ratificación.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) tocar sellos, vistas, catálogo (lo lee) · c) devolver una cifra que no sea un RESULT sellado; adoptar · d) no aplica · e) CAJA.

## 8 · COMPUERTAS
«Salida = RESULT sellado, por test sobre todo el catálogo» protege **congelar / adoptar**. «Spec del contrato antes que el código» protege **congelar** (D-15).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `docs/consulta.md`, `docs/consultar.md`, `docs/ejemplos.md`, `docs/reto.md` (v1.1), `docs/data/`, `tools/benchmark.py` + tests, nota, L0, cascada. Ajeno: catálogo (lee; CIERRE-SEMANAL escribe v1.2: la consulta apunta a la versión vigente por puntero), motor, CALC, CI. En vuelo: CIERRE-SEMANAL-1 (si ambos tocan `docs/index.md`, rebasar), COLA-COMPLETA-1 (caja).

## 10 · LO QUE NO HACE · SUCESORES
No sirve API en servidor (D-14: sin servidores); no promete lo que INEGI no preguntó. Sucesores: FRONT-3 con lo que el reto reciba; API servida solo si mesa la pide y con su propia firma.
