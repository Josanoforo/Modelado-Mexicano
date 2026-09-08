# ACTO GEN2-E3-1-1 · CABLEADO-FINAL-DEL-RUNNER

Archivado por A.3 (0-bis de `/acto`). Texto verbatim del encargo tal como
llegó pegado en el mensaje que invocó la skill, 8/sep/2026.

---

ACTO GEN2-E3-1-1 · CABLEADO-FINAL-DEL-RUNNER
ENTORNO: NUBE
MODELO: Opus
TIPO: ejecución directa, no planeación
CONTADOR GEN2: cero
OBJETIVO: cerrar los cuatro cables materiales restantes de `corrida0.py` antes de permitir `CALC-0001`.

AUTORIDAD Y COMPUERTA

Trabaja contra `origin/main` actual.
Antes de tocar nada:

```
git fetch --prune origin
git status --short
git rev-parse HEAD
git rev-parse origin/main
git log -1 --oneline origin/main
```

Confirma por producto que PR #608 está fusionado:

```
git show origin/main:tools/corrida0.py | grep -q 'CALC-INMUTABLE'
git show origin/main:tools/corrida0.py | grep -q 'contrato_ejecutable'
git show origin/main:tools/corrida0.py | grep -q '_verifica_sello'
```

Si alguno falta, PARA. No recrees #608.
Crea una rama/worktree limpio siguiendo `/acto`.

PERÍMETRO

Puedes modificar solamente lo necesario en:

```
tools/corrida0.py
tests/test_corrida0.py
data/corrida0/CALC-SMOKE-0003/    solo si hace falta un smoke nuevo
forense/notas/<fecha>-GEN2-E3-1-1-cableado-final.md
forense/encargos/...                solo cierre/cascada habitual de /acto
forense/no-corrido.tsv              solo si A.14 lo exige
canon/...                           solo cascada mecánica normal del acto
```

`tests/check.py` únicamente si es indispensable para registrar los nuevos tests existentes en `tests/test_corrida0.py`; no abras nuevos controles generales.

NO tocar:

```
CALC-SMOKE-0001/
CALC-SMOKE-0002/
demanda
spec-check
negativo
data/manifiesto.yaml
tramite.yaml
procedencia.yaml
milpa/**
emite_m.py
arbitra.py
runner_l_cli.py
corridas-R/
corridas-M/
corridas-L/
registro/status/vigencia/delta
specs de CALC-0001/0002/0003
valores del modelo
```

No conviertas este acto en E5 ni E6.

A.8 · CONFIRMACIÓN ANTES DE CAMBIAR

Confirma por lectura los cuatro defectos. Si alguno ya fue corregido por un commit posterior, no lo vuelvas a implementar.

D1 · Doble resolución de payload

Confirma que:

1. `preflight()` llama a `resolver_payload()` y devuelve detalle de inputs.
2. `_inputs_para_medidor(spec)` vuelve a llamar independientemente a `resolver_payload()`.
3. `_ejecuta(spec)` recibe solamente `spec`, no el snapshot resuelto por `preflight`.

Defecto:

```
preflight verifica bytes X
→ intervalo
→ resolver vuelve a mirar disco
→ medidor puede recibir bytes Y
→ ejecucion.json puede registrar X
```

El requisito es snapshot único por intento de corrida.

D2 · Contrato permite omisiones silenciosas

Confirma que `contrato_ejecutable()` usa patrones como:

```
spec.get("universo", "NO-APLICA")
spec.get("filtros", "NO-APLICA")
spec.get("ponderador", "NO-APLICA")
spec.get("transformacion", "NO-APLICA")
spec.get("estimando", "NO-APLICA")
```

y que `preflight` no exige que esas dimensiones existan explícitamente.

Defecto:

```
campo olvidado
```

se vuelve indistinguible de:

```
NO-APLICA declarado
```

También confirma que:

```
seed:
  aplica: true
  valor: 42
```

puede pasar sin `rng`.

D3 · `verify` compara con tolerancia global, no por RESULT

Confirma que `verify` hace esencialmente:

```
tol = spec.get("tolerancia") or {}
_compara(previos[k], valores[k], tol)
```

para todos los RESULT.
El tipo autoritativo debe ser:

```
resultados:
  - id: RESULT-X
    tipo: entero|flotante|proporcion|texto
```

No el `tipo` global de `tolerancia`.
Confirma además que la salida reejecutada por `verify` no pasa primero por `_valida_outputs()`.

D4 · Fallo del sellador puede terminar en EJECUTADO

Confirma que `run()` ejecuta `sella_sha256.py`, pero su veredicto final depende del `exit_code` del medidor y no del `returncode` del sellador.
Debe ser imposible devolver `EJECUTADO` sin sello válido.

P1 · SNAPSHOT ÚNICO DE INPUTS

Invariante
Dentro de un intento de corrida:

```
resolver
   ↓
preflight
   ↓
MISMO snapshot
   ├─→ medidor
   └─→ ejecucion.json
```

No:

```
resolver → preflight
resolver otra vez → medidor
```

Implementación
Haz que `preflight()` devuelva un objeto estructurado de inputs resueltos, por ejemplo:

```
pre["inputs_resueltos"]
```

Cada entrada debe incluir como mínimo:

```
id
origen
ruta_absoluta
raiz_logica
sha256
estado
```

Para `origen: repo`, el snapshot también debe contener los bytes identificados por el SHA verificado.
Para `origen: manifiesto`, debe venir directamente del resolver compartido.

Modifica la cadena para que:

```
run()
    preflight()
    _ejecuta(spec, inputs_resueltos)
```

y:

```
_inputs_para_medidor(...)
```

no vuelva a resolver payloads.
Puede transformar el snapshot al formato esperado por `medir()`, pero no volver a mirar manifiesto/disco para decidir identidad.
`ejecucion.json.input_sha256` debe salir del mismo snapshot.

Verify
En `verify`, resuelve cada input una sola vez por invocación de verify.
Ese mismo snapshot debe alimentar:

```
comparación de CONTEXTO
+
reejecución del medidor
```

No resolver una vez para contexto y otra vez para ejecutar.

P2 · SPEC EXPLÍCITA, NO `NO-APLICA` INVENTADO

Endurece `preflight`.
Toda spec nueva bajo el esquema endurecido debe contener explícitamente:

```
variables:
universo:
filtros:
ponderador:
transformacion:
estimando:
parametros:
seed:
dependencias_materiales:
resultados:
tolerancia:
```

El valor puede ser:

```
ponderador: NO-APLICA
```

cuando corresponda.
Lo que no puede pasar es:

```
ponderador ausente
→ runner inventa NO-APLICA
```

Compatibilidad
No rompas artificialmente `CALC-SMOKE-0001`, que es legado sellado.
Si necesitas compatibilidad de lectura para CALC históricos, hazla explícita según generación/esquema existente.
Pero cualquier nuevo CALC que pretenda pasar `preflight VERDE` bajo el esquema actual debe declarar las dimensiones.

Seed
Acepta únicamente:

```
seed:
  aplica: false
```

o:

```
seed:
  aplica: true
  valor: 42
  rng: numpy.PCG64
```

Si:

```
aplica: true
```

faltan `valor` o `rng`:

```
PRE-FLIGHT: BLOQUEADO
```

No inventes RNG.

Resultados
Antes de abrir microdato, `preflight` debe validar la declaración del schema de outputs:

```
id no vacío
id único
tipo permitido
unidad no vacía
permite_no_estimable booleano si aparece
```

La validación de los valores producidos sigue perteneciendo a `run`.

P3 · VERIFY REALMENTE POR RESULT

Construye un mapa desde la spec:

```
resultado_id -> declaración del RESULT
```

Para cada RESULT reejecutado:

entero

```
tipo Python entero
no bool
comparación exacta
```

texto

```
tipo str
comparación exacta
```

flotante

```
finito
abs(delta) <= tolerancia declarada aplicable
```

proporcion

```
finito
0 <= valor <= 1
abs(delta) <= tolerancia aplicable
```

Antes de comparar contra el recibo:

```
problemas = _valida_outputs(spec, valores_replay)
```

Si los outputs reejecutados violan el contrato:

```
RESULTADO = NO-EJECUTABLE
```

o una denominación equivalente ya consistente con P5, pero no `REPRODUCE`.

Tolerancia
No uses `spec["tolerancia"]["tipo"]` para decidir si un RESULT es entero/flotante.
El tipo lo fija cada entrada de:

```
resultados:
```

La tolerancia puede seguir siendo global como magnitud por defecto si la spec así lo diseña, pero la semántica de comparación viene del RESULT.
Si el esquema ya admite tolerancia por RESULT, úsala. Si no existe, no inventes un esquema complejo en este acto.

Regla suficiente:

```
entero/texto = exacto
flotante/proporcion = abs declarada
```

P4 · EJECUTADO SOLO SI EL SELLO QUEDÓ VÁLIDO

Después de escribir:

```
ejecucion.json
resultados.json
sello.json
```

y ejecutar:

```
tools/sella_sha256.py
```

comprueba:

```
r.returncode == 0
```

y después verifica el sello recién generado con el mecanismo existente.
Solo entonces:

```
veredicto = EJECUTADO
```

Si falla la creación o verificación del sello:

```
veredicto = FALLO-SELLADO
exit != 0
```

No declares el CALC `SELLADO`.
Los JSON intermedios pueden quedar como intento incompleto si limpiarlos introdujera más riesgo que beneficio. Al no existir un sello válido, `run` debe poder reintentarlos.
No fabriques un sidecar para recuperar automáticamente.

P5 · TESTS MÍNIMOS OBLIGATORIOS

Añade solamente estos casos nuevos.

T-SNAPSHOT-INPUT-UNICO
Instrumenta/mokea `resolver_payload`.
Debe demostrar:

```
run/preflight → resolver llamado una sola vez por input
```

y que el mismo SHA/ruta llega a:

```
medidor
ejecucion.json
```

Idealmente el mock devuelve valor A en primera llamada y B en segunda. El test debe demostrar que no existe segunda llamada.

T-SPEC-NO-APLICA-EXPLICITO
Dos casos:

```
ponderador: NO-APLICA
```

→ no bloqueo por ponderador.
Ponderador ausente:

```
→ bloqueo campo_sustantivo_ausente
```

Repite el patrón suficiente para probar que el mecanismo cubre todas las dimensiones, sin crear un test por campo.
Incluye:

```
seed.aplica=true sin rng → BLOQUEADO
```

T-VERIFY-TIPO-POR-RESULT
Una spec con:

```
tolerancia:
  tipo: flotante
  abs: 1e-10

resultados:
  - id: RESULT-N
    tipo: entero
```

Reejecución devuelve:

```
1.0
```

contra sellado:

```
1
```

Debe NO reproducir como entero válido.
Eso demuestra que `verify` usa el tipo del RESULT y no la tolerancia global.
Incluye un flotante dentro de tolerancia para comprobar que ese sí reproduce.

T-SELLADOR-FALLA-NO-EJECUTADO
Simula:

```
medidor OK
outputs OK
sella_sha256 returncode != 0
```

Debe resultar:

```
veredicto != EJECUTADO
```

y no debe considerarse CALC sellado/inmutable.

P6 · SMOKE

No toques `CALC-SMOKE-0001` ni `0002`.
Si los cuatro tests anteriores ejercitan de manera suficiente el cableado, no crees `CALC-SMOKE-0003` solo por ceremonia.
Crea `CALC-SMOKE-0003` únicamente si hace falta demostrar el snapshot único o el fallo del sellador en un flujo que los fixtures no puedan representar razonablemente.
Si nace:

```
generacion: LEGACY-GEN1
tipo: REPLAY-SMOKE
cuenta_gen2: "NO"
validacion_independiente: NO-HECHA
repite_de: CALC-SMOKE-0002
```

Nunca cuenta como resultado GEN2.

MÁQUINA DE ESTADOS

PR #608 dejó pendiente que los estados sean consultables externamente.
No implementes registro/status de E6.
Pero, si los primeros CALC de E5 necesitan saber su estado, deja una función pura derivada, no un archivo nuevo de control, por ejemplo:

```
estado_calc(calc_id)
```

derivada exclusivamente de artefactos:

```
sin spec.yaml                         → BORRADOR
spec válida, sin ejecución            → SPEC-FIJADA
preflight verde durante operación     → PRE-FLIGHT-VERDE
ejecucion+resultados sin sello válido → EJECUTADA-NO-SELLADA
sello completo válido                 → SELLADA
```

No persistir estado duplicado si se puede derivar.
`SUPERADO` queda para registro derivado/sucesor posterior.
Si esto no es necesario para cerrar los cuatro defectos, déjalo explícitamente para E5-0 como ya declaró #608.

COMPROBACIONES DE SALIDA

Ejecuta:

```
python3 tests/test_corrida0.py
python3 tests/check.py --baseline
```

Además demuestra:

```
SNAPSHOT-INPUT-UNICO=PASS
SPEC-EXPLICITA=PASS
SEED-RNG-OBLIGATORIO=PASS
VERIFY-TIPO-POR-RESULT=PASS
SELLADOR-FALLA-NO-EJECUTADO=PASS
CALC-INMUTABLE-REGRESION=PASS
CALC-SMOKE-0002-INMUTABLE=PASS
BASELINE=VERDE
```

Re-verifica que:

```
python3 tools/corrida0.py run CALC-SMOKE-0002
```

siga respondiendo:

```
CALC-INMUTABLE · YA-SELLADO
```

sin modificar un byte.
No necesitas que `verify CALC-SMOKE-0002` diga `IDENTICO` después de avanzar el commit, porque un cambio de contexto puede producir correctamente `REPLICA-RESULTADO · CONTEXTO-DISTINTO`. No alteres el smoke para forzar un verde cosmético.

CRITERIO DE GO

El acto se considera logrado únicamente si:

```
1. El payload se resuelve una vez y ese snapshot exacto llega al medidor y al recibo.
2. Ninguna dimensión sustantiva omitida se convierte silenciosamente en NO-APLICA.
3. seed.aplica=true exige valor + rng.
4. verify valida outputs de replay y compara según tipo declarado POR RESULT.
5. El sellador debe terminar y verificar correctamente antes de devolver EJECUTADO.
6. Un CALC ya sellado sigue siendo inmutable.
7. Suite baseline no introduce regresión.
```

Salida final esperada:

```
GEN2-RUNNER-READY=SI
GO-CALC-0001=SI
```

Si cualquiera de los puntos 1–5 queda parcial:

```
GEN2-RUNNER-READY=NO
GO-CALC-0001=NO
```

y reporta únicamente el bloqueo concreto.

NO HACER

No implementar:

```
registro
status
vigencia
delta
T-REPRO
dashboard
replay CI de microdatos
marcador R/M/L
E7
mediciones reales
CALC-0001
CALC-0002
CALC-0003
```

No abrir una auditoría nueva del repo.
No añadir JSON Schema universal.
No añadir tests para anomalías que no protejan uno de estos cuatro defectos.
No refactorizar por estética.

CIERRE

En el PR reporta primero:

```
qué cambió
por qué importa
GO-CALC-0001 = SI/NO
```

Después:

```
## NO-CORRIDO / RESERVAS
```

y la cascada normal de `/acto`.
El objetivo de este acto es ser la última modificación del runner antes de preparar las tres specs reales, no inaugurar otra ronda de infraestructura.

---

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «MÁQUINA DE ESTADOS · deja una función pura derivada, no un archivo nuevo de control, por ejemplo `estado_calc(calc_id)`» | `DIFERIDO-A:GEN2-E5-0` | Ningún contador se mueve. No hace falta para cerrar ninguno de los cuatro defectos D1–D4, y el propio encargo lo autoriza («Si esto no es necesario para cerrar los cuatro defectos, déjalo explícitamente para E5-0 como ya declaró #608»). Los primeros CALC de E5 no podrán consultar su estado por función todavía. | `GEN2-E5-0` · `forense/no-corrido.tsv` NC-0010 |
| «`data/corrida0/CALC-SMOKE-0003/` solo si hace falta un smoke nuevo» (P6) | `NO-VERIFICABLE-AQUÍ` — no hizo falta | Ninguno. Los siete tests nuevos ejercitan el snapshot único (mock de `resolver_payload`) y el fallo del sellador (mock de `subprocess.run`) sin corpus; el encargo prohíbe crearlo «solo por ceremonia». No queda deuda: el cableado queda cubierto por fixtures, no sin cubrir. | Ninguno — cerrado por no aplicar |
| Verificación del endurecimiento P2/P3 contra los `spec.yaml` reales de `CALC-0001/0002/0003` | `NO-VERIFICABLE-AQUÍ` | El endurecimiento se probó contra fixtures y contra las dos specs `LEGACY-GEN1` selladas; las tres specs reales todavía no existen, así que no se pudo medir cuántos campos sustantivos les faltarían. | `GEN2-E5-0` · `forense/no-corrido.tsv` NC-0011 |
| Ejecución de `run()` de punta a punta sobre un fixture temporal | `NO-VERIFICABLE-AQUÍ` | Ninguno nuevo: `run` exige `preflight` VERDE, que exige `spec.yaml` COMMITEADO, y un fixture vive fuera del repo. `t_sellador_falla_no_ejecutado` sustituye `preflight` por su resultado ya calculado para ejercer el tramo posterior al medidor —que es justo lo que el caso mide—, mismo patrón que la nota de cabecera de `tests/test_corrida0.py` ya declara para los catorce casos de `PR #608`. Límite ya conocido y ya declarado, no deuda nueva. | Ninguno — límite estructural declarado |

## CONSUMIDO

Ejecutado por **PR #610** (`ACTO GEN2-E3-1-1 · CABLEADO-FINAL-DEL-RUNNER`),
rama `claude/cableado-final-runner-w94qj6`, 8/sep/2026, contra
`origin/main = df9336c` (merge de PR #608), sincronizado después con
`origin/main = 7ed877f` (merge de PR #609). `canon/gobernanza-v1_15.md`
**ADR-396** — renumerado desde `395`, que `PR #609` (`ACTO GEN2-V213`) tomó
al fusionar primero: renumera quien fusiona segundo. Por la misma colisión,
las reservas A.14 de este acto son `NC-0010` y `NC-0011` (`NC-0009` es de
`#609`).

Los cuatro defectos (D1 doble resolución de payload · D2 omisiones
silenciosas · D3 `verify` con tolerancia global · D4 sellador sin
consecuencia) quedan cerrados y con test propio. `GEN2-RUNNER-READY=SI` ·
`GO-CALC-0001=SI`.

Este encargo no se edita en ningún otro punto: es el registro de qué se
pidió, para poder auditar si el ejecutor hizo lo que se le dijo.
