# ENCARGO · ACTO GEN2-PRIMERA-SILLA · UN LOTE, CUATRO PIEZAS — el grano que bloquea la adopción, la llave del WARN, la firma de los dos CALC nuevos, y la cita que ocupa la primera silla

**Archivado verbatim (0-bis A.3).** Recibido de dirección el 9/sep/2026 como texto de mesa, no como archivo en cola — se transcribe aquí sin editar para que el acto tenga encargo archivado, que es lo que A.3 exige.

**Estado:** CONSUMIDO

---

Cabecera: NUBE, Opus · COMPUERTA: ninguna (todo lo que consume está en main = 8b9f9d49) · candidatos: deriva, no heredes. CONCURRENCIA: PILOTO-SONDA corre en caja (colas/manifiesto) — disjunto.

FIRMAS DE MESA que este acto porta — mandarlo es dictarlas, el merge las sella:

FIRMA 1 (contador): «cuenta_gen2 = SI para CALC-0003-v3 y CALC-B-0001. Mesa, 8/sep/2026, conversación de dirección. v3 reproduce 128/128 con el conglomerado correcto (C3/C4 corroboradas robustas ×1.78/×1.41; C1 no-discrimina); B sellada 90/90 con REPRODUCE·IDENTICO pleno. Cuenta, no adopta, no compara con GEN1.» FIRMA 2 (adopción, condicionada a P1/P2 en verde): «La primera cita de un consumidor de milpa a un RESULT GEN2 se escribe con el patrón derivado en C0-B §5; el merge de este PR es la adopción (E.2). Una silla, un consumidor, el candidato que la derivación de C0-B dejó documentado.»

CONTEXTO MEDIDO QUE SE HEREDA (C0-B §5, FP-365/NC-0069 — pegado ahí con tabla; el ejecutor lo re-lee, no lo re-descubre): un solo campo tolerancia.abs sirve a dos preguntas distintas — reproducibilidad (1e-10, correcto, no se toca) y materialización por el consumidor (grano de milpa: seis decimales). T35(c) compara con la primera → escribir la cita hoy mete un FAIL falso. Además la llave del WARN ((rid, calc)) hace que adoptar no baje el conteo (tabla de escenarios en la nota de C0-B, «llave de HOY vs llave correcta»).

PIEZAS P1 · tolerancia_adopcion. La adopción compara contra el RESULT redondeado al grano del consumidor (o tolerancia_adopcion declarada por spec; NO-APLICA es un valor). La reproducibilidad no se afloja un decimal. Falsador con el caso medido de C0-B: el candidato real que hoy da FAIL por grano debe dar ADOPTABLE con P1, y un valor genuinamente distinto en el sexto decimal debe seguir fallando. P2 · La llave correcta del WARN. T35 cuenta SELLADA-SIN-ADOPTAR con la llave que la tabla de C0-B marca como correcta; falsador: adoptar 1 baja el conteo en exactamente 1. Cierra NC-0069; FP-365 → EJECUTADA. P3 · Las dos filas del contador (FIRMA 1, vía directa, cero simulación — la fotocopiadora ya está desarmada por CHECADOR-2 y aun así no se usa): decisiones.tsv + regenerar registro una vez + status pegado. Esperado: N_corridas_selladas 3→5; el total de resultados lo dice la máquina (v2 queda SUPERADO — no se suma doble; si la cifra sorprende, se pega y se explica, no se fuerza). P4 · La cita (FIRMA 2, solo con P1+P2 en verde): escribir en el consumidor de milpa el campo con corrida0_resultado_id + generación, correr suite: WARN baja en exactamente 1 y esa línea se pega. La silla queda ocupada y el patrón, probado para C0-D.

PERÍMETRO: tools/corrida0.py (adopción) · tests/check.py (T35 llave) · tests/test_corrida0.py (falsadores) · data/corrida0/decisiones.tsv + TSV re-derivados · milpa/ un consumidor, un campo · forense/{firmas-pendientes,no-corrido}.tsv · nota · 0-bis · cascada. Si escribes fuera, PARA. CONTADOR: sí, doble — 3→5 corridas contadas y la primera adopción real (211→210 en el WARN). ## NO-CORRIDO obligatoria; si P1/P2 no quedan en verde, P4 NO se escribe y se dice — la silla no se ocupa con calzador.

---

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| **La firma de contador de `CALC-0003-v4`** | FIRMA 1 nombra `CALC-0003-v3` y `CALC-B-0001`, verbatim y sin `v4`. Firmarla desde aquí sería inventar el objeto de una firma de mesa. | El contador cuenta hoy `CALC-0003-v3`, que está `SUPERADO→CALC-0003-v4`, y NO la corrida VIGENTE. En la cifra son **1 id** (v4 aporta 1 sobre los 142 de v3); lo que queda raro es *cuál* corrida está contada. | `NC-0071`. Mesa: firmar `v4`, o declarar que contar `v3` es lo que se quiso. `FP-362` queda FIRMADA-PARCIAL. |
| **La segunda silla y las siguientes** | El encargo pidió **una** silla, y se escribió esa una: la que la derivación de `C0-B` §5 dejó documentada. | **442** RESULT GEN2 sellados siguen sin adoptar y el WARN sigue gritando por todos ellos. `C0-B` §5.2 ya midió por qué no se pueden ocupar con más citas: los otros CALC producen deltas, marginales y veredictos, y ninguno es una probabilidad de conducta del motor — la única ranura que el registro reconoce. | `NC-0072`. `C0-D`, con el patrón ya probado punta a punta. La segunda silla necesita un CALC nuevo, no otra cita. |
| **Ningún CALC corrió: este acto no midió nada** | Por diseño. El perímetro es aparato (`tools/`, `tests/`), una firma de mesa y una cita. | Las cifras que se mueven son de CONTEO y de ADOPCIÓN, no de medición: **ningún número del programa cambió de valor**. `RESULT-B-ENIGH-2022-P` vale hoy lo mismo que el 8/sep y el `p: 0.045694` del motor no se tocó — sólo se declara de dónde viene. | `NC-0073`. n/a — por diseño. |
| **Las dos cifras del encargo que salieron distintas** | No se forzaron para que cuadraran. El WARN va de **443 a 442** (no 211→210) porque P3 firma dos CALC antes de que P4 adopte, así que el universo del WARN sube antes de bajar; la resta sigue siendo 1. Y `N_resultados_gen2_sellados` da **315** (no 301) porque la simulación de `C0-B` firmaba sólo `CALC-B-0001`, mientras FIRMA 1 firma dos, y `v3` repite 128 de sus 142 ids de `v2` por cadena `repite_de`. | Ninguno: las dos cifras están derivadas de la máquina y explicadas en la nota §3 y §4. | n/a — explicado, no pendiente. |

## CONSUMIDO

Ejecutado por **`ACTO GEN2-PRIMERA-SILLA`**, 9/sep/2026, NUBE, Opus, rama `claude/tender-franklin-sh9430`, base `main = 8b9f9d4`.

Las cuatro piezas se ejecutaron. **P1** (`tolerancia_adopcion` / `_compara_adopcion`, `FP-365` → EJECUTADA, `NC-0069` → CERRADA) · **P2** (llave del WARN sobre `usos.corrida0_resultado_id`, `FP-364` → EJECUTADA, `NC-0068` → CERRADA) · **P3** (FIRMA 1: dos filas en `decisiones.tsv`, `N_corridas_selladas` 3→5, `FP-366` → FIRMADA-EJECUTADA, `FP-362` → FIRMADA-PARCIAL con la reserva de `v4`) · **P4** (FIRMA 2: la cita escrita, WARN 443→442, `N_resultados_gen2_adoptados_activos` 0→1, `NC-0053` → CERRADA).

**Dos cifras del encargo salieron distintas y se pegan sin forzarlas:** el WARN no iba de 211 a 210 sino de **443 a 442** (la firma de contador de P3 sube el universo del WARN antes de que P4 lo baje), y `N_resultados_gen2_sellados` no dio 301 sino **315**. Las dos se explican en la nota de cierre §3 y §5.

Nota de cierre: `forense/notas/2026-09-09-GEN2-PRIMERA-SILLA-cierre.md`.
