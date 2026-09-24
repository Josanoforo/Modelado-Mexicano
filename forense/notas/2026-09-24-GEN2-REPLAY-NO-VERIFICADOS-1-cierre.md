# ACTO GEN2-REPLAY-NO-VERIFICADOS-1 · cierre por PARO (f)

Contadores movidos: **cero**. Ninguna corrida nueva, ningún asiento de replay, ninguna fila en `decisiones.tsv`, `cuenta_gen2` sin cambio para los seis ids, `adoptados` sin cambio.

- Encargo: `forense/encargos/2026-09-24-GEN2-REPLAY-NO-VERIFICADOS-1.md` (0-bis `822a90ba`, `.cuerpo.sha256` = `0b639382…`).
- ADR: `ADR-260924-GEN2-REPLAY-NO-VERIFICADOS-1-822a-01`.
- Entorno: CAJA (`tools/entorno.py --arranque --sonda-red` → `ENTORNO-DERIVADO = CAJA`, `montado=SI archivos_examinados=490`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, red `http_code=200`). Modelo: Opus 5.5 durante todo el acto; la sesión arrancó en Sonnet 5 y pasó a Opus antes del ARRANQUE, sin tocar el árbol.
- Base: `origin/main` = `c12a0d87`, igual al SHA de redacción; `git rev-list --count HEAD..origin/main` → 0.

## 1 · Qué se encontró

**Los seis ids ya tienen replay afirmativo y vigente en `origin/main`.** Es el PARO (f) de la lista cerrada del encargo: «las seis ya tienen replay afirmativo en origin/main».

§4 del encargo, corrido tal cual: `grep -c 'EDER2017\|ENFIH2019\|ENSAFI2023\|WBES2023' forense/replay-evidencia.tsv` → **14** (se esperaban 0 filas afirmativas). De esas 14, las que corresponden a los seis ids:

| línea | calc_id | corrida_id (sufijo) | resultado · contexto | fecha | procedencia |
|---|---|---|---|---|---|
| 189 | `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001` | `381e847667f5` | REPRODUCE · IDENTICO | 2026-09-22 | VERIFY-AISLADO · GEN2-PENDIENTES-CAJA-1 |
| 190 | `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002` | `18e3c08247d5` | REPRODUCE · IDENTICO | 2026-09-22 | VERIFY-AISLADO · GEN2-PENDIENTES-CAJA-1 |
| 192 | `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001` | `f22dc8014aec` | REPRODUCE · IDENTICO | 2026-09-22 | VERIFY-AISLADO · GEN2-PENDIENTES-CAJA-1 |
| 193 | `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0002` | `cd853c64a584` | REPRODUCE · IDENTICO | 2026-09-22 | VERIFY-AISLADO · GEN2-PENDIENTES-CAJA-1 |
| 205 | `CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001` | `db6b218d5fa5` | REPRODUCE · IDENTICO | 2026-09-22 | VERIFY-AISLADO · GEN2-PENDIENTES-CAJA-1 |
| 212, 225 | `CALC-WBES2023-PRECISION-INTERACCIONES-0001` | `7f2a0899f700` | REPRODUCE · IDENTICO | 2026-09-22 y 2026-09-19 | VERIFY-AISLADO · GEN2-PENDIENTES-CAJA-1 / GEN2-REPLAY-Y-PISOS-CLI-1 |

Las otras 8 son de CALC distintos (WBES CORRUPCION/PRECISION, ENFIH SALDOS-AFORE, ENSAFI `-v1_1`, DIN-CREDITO-K8) o asientos más viejos de EDER-0002 (`8507f8cf7e3f`, 19/sep).

**Los asientos son de la corrida sellada de hoy.** Los seis `corrida_id` casan exactamente con `data/corrida0/<CALC>/ejecucion.json`. Y son **vigentes** para la identidad de hoy (`spec_yaml_sha256`, `script_blob_sha256`, `input_sha256_efectivos`), medido con la función del propio registro, en solo lectura:

```
python3 -c "… corrida0._evidencia_vigente(ev[calc], ejecucion.json) …"
CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001  vigente: True
CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002  vigente: True
CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001    vigente: True
CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0002    vigente: True
CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001     vigente: True
CALC-WBES2023-PRECISION-INTERACCIONES-0001     vigente: True
```

`corrida0._proyecta_replay(calc, ejecucion, None, evidencia)`, sin `verify`, da `REPRODUCE IDENTICO EVIDENCIA-HISTORICA` para los tres que probé (EDER-0001, WBES, ENSAFI). Es decir: **una re-derivación de la vista con el código de hoy los publicaría como REPRODUCE · IDENTICO.**

## 2 · Por qué la vista dice NO-VERIFICADO

`data/corrida0/corridas.tsv` en `origin/main` (y en los dos `[deriva]` del 23/sep, `ae672a46` y `3e3a85a6`, que ya tenían los asientos en su árbol) trae los seis como `cuenta_gen2=PENDIENTE-DE-MESA · resultado_replay=NO-VERIFICADO · contexto_replay=NO-VERIFICADO`, con `fuente_replay=SIN-FUENTE` en cinco. En EDER-0002 la fuente apunta al asiento viejo del 19/sep. Eso es lo que leyó ADOPCION-1: su `NC-260924-GEN2-ADOPCION-BLOQUE-Y-PINES-1-ec71-02` dice textualmente «ninguna de las 6 tiene replay afirmativo **en corridas.tsv**». Leyó la vista, no la fuente (E.7: la fuente es `forense/replay-evidencia.tsv`).

Mecanismo, medido:

1. Los asientos entraron con `b953841c` (GEN2-PENDIENTES-CAJA-1 · P1, «30 verify aislados asentados»), fusionado por `PR #1004` → merge `8ddb42d6`, 22/sep 21:05Z.
2. El job de derivados de `verify.yml` re-deriva sólo un **lote**: `tools/lote_desde_asientos.py "$ANTES" HEAD --incluir-pendientes`. Recalculado hoy, en solo lectura, el lote de ese push (`8ddb42d6^1 8ddb42d6`) contiene **los seis** ids.
3. El run de CI de ese push (`35784425052`, `headSha 8ddb42d6`) terminó en `failure`. El paso fallido: `guardias :: Re-deriva por comando y commitea [deriva] si hay diff`. No hubo `[deriva]` de ese lote. Del 22/sep 20:39Z al 23/sep 03:07Z, todos los runs de `main` son `failure` o `cancelled`.
4. Ningún push posterior los recoge: el lote de cada push lleva sólo los asientos nuevos de `ANTES..HEAD`, y `--incluir-pendientes` sólo recupera sellados **ausentes** de `corridas.tsv`. Los seis tienen fila, así que el lote de pendientes de hoy da **0** de los seis (`python3 tools/lote_desde_asientos.py --incluir-pendientes --csv | grep -c …` → 0).
5. Hoy el canal está además caído por GH001 (`NC-260924-GEN2-CONTADORES-CONSUMO-2-749c-03`, ABIERTA): aunque entraran a un lote, ningún `[deriva]` llega a `main`.

Defecto de mecanismo (hallazgo, una línea): **un asiento de replay cuyo `[deriva]` falla queda fuera de todo lote posterior.** `lote_desde_asientos.py` no distingue «asiento proyectado» de «asiento que ningún `[deriva]` publicó», y la vista queda en `NO-VERIFICADO` con evidencia vigente en la fuente.

## 3 · Qué no se hizo y por qué

- **P1 (payloads contra manifiesto) y P2 (`verify` por corrida):** no se corrieron. El replay que P2 debía producir ya está asentado y vigente. Un `verify` más daría un séptimo asiento sobre la misma corrida (dos escritores sobre la misma evidencia) sin mover nada, porque lo que falta no es replay.
- **P3 (`decisiones.tsv`, fila por REPRODUCE citando M):** no se escribió. La firma M (verbatim en `forense/encargos/2026-09-24-GEN2-ADOPCION-BLOQUE-Y-PINES-1.md:14`) dice «quedan PENDIENTE-DE-MESA hasta replay afirmativo». El replay afirmativo **ya existía dos días antes de la firma**, y mesa firmó leyendo la vista. Si M cubre un replay anterior a su propia fecha es pregunta de firma, y el encargo mismo la manda a PARO (f). No lo decido yo.
- **P4 (cierre de `ec71-02`):** no se cerró. La NC sigue ABIERTA. Su razón («ninguna de las 6 tiene replay afirmativo en corridas.tsv») es cierta de la vista y falsa de la fuente. Lo que le falta ya no es replay sino la firma y la proyección.
- **Premisa logística caída, sin consecuencia:** el encargo cita `milpa/decisiones.tsv`, pero el archivo vive en `data/corrida0/decisiones.tsv` (`git ls-files | grep decisiones.tsv` → sólo ese). No se escribió en ninguno de los dos.

## 4 · Para mesa: recomendación y texto de firma

**Recomendación:** que M cubra los seis. El replay es de la misma corrida sellada, con identidad vigente, en CAJA, con el mismo vocabulario E.3 que las diez ENIGH adoptadas bajo M. Lo único que cambió es que la vista no lo mostraba. Pedir otro replay no añadiría información.

Texto listo para firmar:

> «Los seis replays REPRODUCE · IDENTICO asentados el 22/sep por GEN2-PENDIENTES-CAJA-1 (`forense/replay-evidencia.tsv` l.189, 190, 192, 193, 205, 212; PR #1004) satisfacen la condición "hasta replay afirmativo" de M. EDER-0001/0002, ENFIH-0001/0002, ENSAFI-0001 y WBES-0001 entran bajo M con fila en `data/corrida0/decisiones.tsv` por CALC.»

Con esa firma, lo que falta son seis filas en `decisiones.tsv` (el sucesor que el encargo ya nombra, ADOPCION-3, o una adenda a este acto), más la proyección de la vista. La proyección necesita que el canal de derivados vuelva (`…749c-03`) **y** que un lote incluya estos seis. Por el punto 4 del §2, no entrarán solos.

Alternativa: exigir un `verify` fresco posterior a M. Cuesta una sesión de CAJA y no cambia nada de lo medido.

Hay filas `forense/firmas-pendientes.tsv` → `FP-260924-GEN2-REPLAY-NO-VERIFICADOS-1-822a-01` y `forense/no-corrido.tsv` → `NC-260924-GEN2-REPLAY-NO-VERIFICADOS-1-822a-01..03`.
