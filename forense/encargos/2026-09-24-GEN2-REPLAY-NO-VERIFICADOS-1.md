# ENCARGO · ACTO GEN2-REPLAY-NO-VERIFICADOS-1 · Las seis corridas `cuenta_gen2 = PENDIENTE-DE-MESA` con replay NO-VERIFICADO (EDER ×2, ENFIH ×2, ENSAFI, WBES) pasan por `verify` en caja; las que reproduzcan se adoptan bajo la firma M sin trámite nuevo; las que no, quedan dictaminadas

> ENTORNO: **CAJA** — replay sobre microdato ya abierto (EDER 2017, ENFIH 2019, ENSAFI 2023, WBES 2023; ninguna reservada). Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `c12a0d87` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-replay-no-verificados-1` (D-17) · MODELO: Opus (mide; no bajar) · MODO: RÍGIDO: verify de corridas selladas; cero cambios de procedimiento · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero corridas nuevas (`verify` no sella); mueve `cuenta_gen2` de hasta seis corridas de PENDIENTE-DE-MESA a SI (eje E.1) y asienta seis filas en `replay-evidencia.tsv` (E.7). No mueve `adoptados` (eje E.2, otro consumidor).

## 1 · OBJETIVO
El hallazgo 2 del -1 de ADOPCION: seis corridas selladas que nunca pasaron la segunda pregunta de E.2 (¿pasó validación / replay?). Correr `python3 tools/corrida0.py verify <id>` sobre cada una en caja, asentar RESULTADO y CONTEXTO por corrida (E.3: NO-VERIFICABLE no se degrada a NO-REPRODUCE), y aplicar la regla firmada: REPRODUCE → `cuenta_gen2: SI` con fila en `decisiones.tsv` citando M; NO-REPRODUCE → dictamen y NC a su acto de origen; NO-EJECUTABLE → causa (dependencia, entorno, insumo) y NC.
«Hecho»: seis filas en `forense/replay-evidencia.tsv` con `resultado_replay` ∈ {REPRODUCE, NO-REPRODUCE, NO-EJECUTABLE} y `contexto_replay` ∈ {IDENTICO, DISTINTO, NO-VERIFICABLE} · `decisiones.tsv` con una fila por REPRODUCE citando M · `corridas.tsv` (en el siguiente `[deriva]`) sin `NO-VERIFICADO` para esos seis ids · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
- **M** (24/sep, ADOPCION-1 §2): «Se adoptan en bloque las diez corridas ENIGH con replay REPRODUCE (fila en decisiones.tsv por CALC); EDER-0002, ENFIH-0001/0002 y WBES-0001 quedan PENDIENTE-DE-MESA hasta replay afirmativo.»
- **Lectura de dirección de M, declarada para no volver a mesa:** «hasta replay afirmativo» significa que el replay afirmativo es la condición; cumplida, entran bajo M sin nueva firma, con la misma regla que las diez ENIGH. EDER-0001 y ENSAFI-0001 (que M no nombra porque el -1 los encontró después) siguen la misma regla porque son el mismo predicado (`PENDIENTE-DE-MESA ∧ NO-VERIFICADO`) que M resuelve. Si mesa no comparte esta lectura, lo dice al lanzar y esas dos quedan como NC.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` Cierre de ADOPCION-1 l.105-118: los seis ids: `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001` y `-0002`, `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001` y `-0002`, `CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001`, `CALC-WBES2023-PRECISION-INTERACCIONES-0001`; predicado verificado sobre `corridas.tsv` por `/revisa`. NC `ec71-02`.
- `[EJECUTADO]` cada uno tiene `sello.json`, `spec.yaml`, `ejecucion.json`, `medidor.py` en `data/corrida0/` (226+ sellos). `[SUPUESTO]` que sus payloads están en el corpus de caja con el sha del manifiesto (A.15: verificar por id, con conteo; un payload ausente = NO-EJECUTABLE con causa, no PARO).
- E.3: `run` se niega sobre sellado; `verify` no muta; reejecutar es CALC nuevo — aquí no se reejecuta nada.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -c 'EDER2017\|ENFIH2019\|ENSAFI2023\|WBES2023' forense/replay-evidencia.tsv` → reporta (esperado 0 filas afirmativas). `git ls-remote --heads origin | grep -i replay` → 0.

## 5 · PIEZAS
P1 · Payloads por id contra manifiesto (conteo). P2 · `verify` por corrida, salida cruda pegada, seis asientos. P3 · `decisiones.tsv`: fila por REPRODUCE con M; NC por NO-REPRODUCE (a su acto de origen) y por NO-EJECUTABLE (causa). P4 · Cierre de `ec71-02`.

## 6 · LATITUD
Orden libre. Obstáculos reversibles: dependencias, rutas. Pregunta a mesa: ninguna prevista salvo §2.

## 7 · PAROS — lista cerrada
a) abrir dato reservado (ninguna de las seis lo es; si `verify` intenta leer una ola reservada por un input mal citado, PARA esa corrida) · b) reescribir un sello; `run` sobre sellado; `--force` · c) mover `adoptados` o escribir en `milpa/` · d) cambiar procedimiento · e) NUBE · f) las seis ya tienen replay afirmativo en origin/main.

## 8 · COMPUERTAS
«`verify` solo; ningún `run`» protege: **borrar/reescribir**. «`cuenta_gen2: SI` solo con REPRODUCE y cita a M» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/replay-evidencia.tsv` (append), `milpa/decisiones.tsv` (append), `no-corrido.tsv`, nota, L0, cascada. Ajeno: todo lo demás. En CAJA: nadie más con reserva; U0 y ADOPCION-2 son nube.

## 10 · LO QUE NO HACE · SUCESORES
No sella, no releva, no adopta en consumidor. Sucesor: ADOPCION-3 si algún REPRODUCE tiene consumidor que cablear.
