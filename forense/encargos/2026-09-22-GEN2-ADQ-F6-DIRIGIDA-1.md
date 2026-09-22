# ENCARGO · ACTO GEN2-ADQ-F6-DIRIGIDA-1 · Lo que F6 necesita para tener panel, adquirido por id de manifiesto, con sha y licencia leída — y toda ola nueva entra RESERVADA

> ENTORNO: **NUBE con red `Custom`** (descargador por id, egreso a INEGI/ICPSR/fuentes públicas) — o CAJA si la red de nube no alcanza; el hook lo dice. Fuentes con acceso por identidad (ICPSR, ENNViH) **no** van aquí: bandeja del titular.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Opus · MODO: **ABIERTO** · CONTADOR: cero mediciones; payloads nuevos en `data/manifiesto.yaml` (N, reportado), cada uno con `sha256`, `url_origen`, `licencia` leída; NC-0161/0162 con sucesor cumplido o acotado · ids raíz de acto.

## 1 · OBJETIVO
Ejecutar la salida que el re-sello de FP-374 (`EN-ESPERA-PANEL`, #998) y la firma D-4 del 15/sep («se autoriza preparación y adquisición dirigida de familias RETENIDAS con reserva previa») dejaron escrita: recorrer `forense/prereg-duelo-v2/F6-falta-conseguir-v1_0.tsv` (9 filas) y, para cada una con vía conocida y sin decisión de mesa pendiente, **adquirir por id**: ENCO por mes (R10, prio 1), ENPOL 2016 (R11, prio 2), MOCIBA 2022 (R01, «POR VERIFICAR»), ENAPROCE microdato completo (R03, prio 3, «verificar si es público»); verificar sha contra lo sellado (A.1: tres estados nunca colapsados); leer la licencia de cada uno (588 payloads sin licencia, plan P4). Lo que exige decisión de mesa (R08 ENCRIGE, R02 WBES) se lista con la pregunta, no se baja. «Hecho» = `python3 tools/corrida0.py` (o `manifiesto.py`) lista los ids nuevos con `sha256` y `licencia ≠ None`; toda ola nueva de una encuesta con historia nace `RESERVADA` (E.6) con fila en `decisiones.tsv`; `F6-falta-conseguir` con columna `estado_adquisicion` por fila y comando; NC-0161/0162 enmendadas con lo conseguido y lo que sigue faltando.

## 2 · FIRMAS DE MESA
Ya selladas, se citan: D-4 (15/sep, NC-0161/0162 `sucesor`), FP-374 re-sellada `EN-ESPERA-PANEL` (`…FP374-RESELLO-1-dfbe-01`), E.6 (ola nueva nace RESERVADA). Ninguna nueva. Lo que pida firma (R08, R02) se lista para mesa.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` `F6-falta-conseguir-v1_0.tsv`: 9 filas — R09 ISSP y R01 MOCIBA 2021/2023 «MONTAJE-DE-RAIZ» (ya en manifiesto: no se bajan, se montan); R10 ENCO (cuestionario y agosto 2026 en manifiesto; faltan meses); R11 ENPOL 2016 (no en manifiesto); R08 ENCRIGE (solo tabulados; decisión de mesa); R02 WBES (decisión de mesa); R03 ENAPROCE (solo bases ciegas); R14 ENH y R12/R13/R07: NADA-ADQUIRIBLE.
- `[LEÍDO]` Plan de aceleración P4: descarga por id de manifiesto, verificada contra el sha sellado; `[EXISTE]` `tools/barrido_descargas_vs_manifiesto.py` y el carril de adquisición (`adq/` cron, `codex/adq-*`). No sé si descargan por id ni si leen licencias: **el acto lo prueba con un id conocido antes de usarlos**.
- `[SUPUESTO]` La red `Custom` de nube alcanza `inegi.org.mx`. Si resulta falso, PARO-ENTORNO por fila con la sonda cruda (nunca `-I`), receta A.5, y las filas van a caja.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
Por id en `data/manifiesto.yaml` antes de bajar nada (A.15: «ningún negativo sobre existencia de un payload sin consultar el manifiesto por id, con conteo»); `data/curacion-registro/cola-adquisicion-registro.tsv` (157 filas al 22/sep) por objeto: si el carril de adquisición ya tiene la fila en curso, se cita y no se duplica. Ramas vivas: ninguna.

## 5 · PIEZAS
- **P1 · Estado por fila**, con comando: `YA-EN-MANIFIESTO` (cita id y sha) / `ADQUIRIDA-AQUI` / `NO-OBTENIDO-POR-ESTE-AGENTE-EN-N-INTENTOS` (+ receta A.5) / `DECISION-DE-MESA` (R08, R02, con la pregunta en una línea) / `NADA-ADQUIRIBLE`.
- **P2 · Adquisición por id** para R10 (meses de ENCO que F6 nombra), R11, R03 si es público, R01-2022 si existe: entrada en el manifiesto con `sha256`, `url_origen`, `licencia` (texto leído, no supuesto), `fecha`; verificación A.1 en tres estados; **sin descomprimir ni abrir** — bajar y hashear no es abrir (E.6). Toda ola nueva de una encuesta con historia (`RESERVADA`) recibe su fila en `decisiones.tsv` con los términos de `reserva:envipe2026`.
- **P3 · Licencias.** Las de los payloads tocados, y —si cabe en el mismo acto— las de los 588 sin licencia del mismo dominio (INEGI): leídas de la página oficial, citadas por URL; lo que no se pueda leer queda `LICENCIA: NO-OBTENIDA` con receta.
- **P4 · Cierre de la deuda con nombre.** NC-0161/0162: enmienda fechada con lo conseguido y lo pendiente; `F6-falta-conseguir-v1_1.tsv` (archivo nuevo, v1_0 intacta) con `estado_adquisicion`; nota para PRODUCTO-DINERO/dirección: qué familias son ya panel real para F6 y cuáles no lo serán nunca.

## 6 · LATITUD
DECIDES TÚ: orden, herramienta de descarga (reusar el carril si baja por id), enlazar raíces. PREGUNTAS A MESA (y sigues): R08 ENCRIGE — ¿microdato 2016/2020 si INEGI lo publica, o solo tabulados? R02 WBES — ¿entra al panel F6 con su ventana y unidad empresa, o queda fuera por unidad? Recomendación de dirección: R08 sí si es público; R02 fuera (unidad empresa no es panel de M). NO DECIDES: §7.

## 7 · PAROS
**a) abrir, listar o derivar cualquier payload de ola reservada (bajar y hashear sí; `unzip -l` no)** · b) reescribir un sha ya sellado en el manifiesto · c) adoptar · d) no aplica · e) fuente que exige identidad (va a la bandeja, no aquí) · f) inalcanzable.

## 8 · COMPUERTAS
«Sonda de red VERDE a la fuente antes de cada descarga — protege: abrir dato (evita adquirir de un espejo no verificado).»

## 9 · PERÍMETRO
Propio: `data/manifiesto.yaml` (entradas nuevas; ninguna existente se edita salvo `licencia` de `None` a texto leído) · `data/curacion-registro/cola-adquisicion-registro.tsv` (filas propias) · `forense/prereg-duelo-v2/F6-falta-conseguir-v1_1.tsv` (nuevo) · `data/corrida0/decisiones.tsv` (reservas) · `forense/no-corrido.tsv` (NC-0161/0162) · nota · `canon/L0/<raíz>.md`. Ajeno: todo CALC, specs, `milpa/`, el panel F5 sellado. Otro acto en vuelo: el cron `adq/` toca la cola de adquisición — ids con raíz, sin conflicto de contenido. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No abre payloads, no mide, no decide sobre R08/R02, no relanza F6. Sucesor: si el panel resulta real, un acto de dirección re-sella FP-374 de `EN-ESPERA-PANEL` a lo que corresponda. Auditoría: no aplica. Cierre por /acto.

## NO-CORRIDO / RESERVAS

- **qué:** P2 · «Adquisición por id para R10 (meses de ENCO que F6 nombra), R11, R03 si es público, R01-2022 si existe»; «Hecho» = «lista los ids nuevos». · **por qué:** SUSTITUIDO-POR: GEN2-ENCO-DOS-OLAS-RESERVADAS-1 (R10, 16/sep) + GEN2-38 (R11, 16/sep) + el registro previo de MOCIBA 2022. Absorben toda la adquisición pública de F6; no queda nada adquirible sin cubrir (R03 y ENCRIGE 2020 no son públicos). · **impacto:** cero ids nuevos en el manifiesto; los 14 que F6 necesita existen (`F6-falta-conseguir-v1_1.tsv`). · **sucesor:** ninguno. `NC-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-01` CERRADA.
- **qué:** P2 · «R03 si es público». · **por qué:** DIFERIDO-A: BANDEJA-DEL-TITULAR. El microdato de ENAPROCE es confidencial y solo se ofrece por Laboratorio (RNM catalog/330, /518); exige identidad (PARO e). · **impacto:** R03 sin microdato; F6 no gana familia TRA. · **sucesor:** SIN-ASIGNAR (titular). `…-e7be-02`.
- **qué:** §6 · «PREGUNTAS A MESA: R08 ENCRIGE […] R02 WBES […]». · **por qué:** DECISIÓN-DE-MESA-PENDIENTE: `FP-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-01`. El microdato de ENCRIGE 2020 no es público (catalog/691); el de 2016 queda NO-VERIFICADO. · **impacto:** R02/R08 siguen sin celda. · **sucesor:** la FP. `…-e7be-03`.
- **qué:** P3 · «las de los 588 sin licencia del mismo dominio (INEGI)» y las de los payloads tocados. · **por qué:** NO-VERIFICABLE-AQUÍ. Se escriben las 34 entradas INEGI; quedan 554 de otros dominios o sin URL, y las de ZA6980, porque GESIS da CONNECT 403 del proxy de nube (NO OBTENIDO POR ESTE AGENTE EN 1 INTENTO; la receta está en la nota §2). · **impacto:** 554 siguen sin licencia; R09 sin licencia leída. · **sucesor:** SIN-ASIGNAR. `…-e7be-04`.
- **qué:** P2 · «verificación A.1 en tres estados». · **por qué:** NO-VERIFICABLE-AQUÍ. Es NUBE sin corpus: AUSENTE ×6, RAÍZ NO CONFIGURADA ×4, FUERA_DE_PERIMETRO ×2, 0 archivos examinados. · **impacto:** ningún sha re-verificado contra su payload. · **sucesor:** GEN2-F6-FACTIBILIDAD-CAJA-1. `…-e7be-05`.
