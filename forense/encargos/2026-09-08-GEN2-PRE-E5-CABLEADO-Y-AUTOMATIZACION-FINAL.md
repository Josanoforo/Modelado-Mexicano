ACTO GEN2-PRE-E5 · CABLEADO-Y-AUTOMATIZACION-FINAL

ENTORNO: NUBE
MODELO: Opus
TIPO: ejecución directa
ORDEN: ejecutar DESPUÉS de que GEN2-E7 esté fusionado y antes de GEN2-E5-0.
CONTADOR GEN2: cero.
OBJETIVO: cerrar las últimas piezas mecánicas del aparato antes de congelar
specs reales. Esta debe ser la última intervención de infraestructura previa
a E5-0, salvo defecto material encontrado al ejecutarla.

FUENTE DE DIRECCIÓN

Usar como autoridad para el orden y los cuerpos de E5-0/E5:

ENCARGOS-GEN2-v1_5-aparato-antes-de-calcular-2026-09-08.md

El orden firmado es:

V213 → E6 → E7 → E5-0 → E5

V213/E6 ya están fusionados. E7 debe estar fusionado antes de iniciar este acto.

No reinterpretar el orden.

────────────────────────────────────────────────────────────
0 · COMPUERTA
────────────────────────────────────────────────────────────

Antes de tocar nada:

git fetch --prune origin
git status --short
git rev-parse HEAD
git rev-parse origin/main
git log -1 --oneline origin/main

Verifica POR PRODUCTO:

1. E6:
   git show origin/main:tools/corrida0.py |
     grep -c "^def cmd_registro\|^def cmd_status"
   → 2

2. E7:
   localizar la nota fusionada de GEN2-E7 y comprobar que contiene:
   GO-MARCADOR

3. Suite:
   python3 tests/check.py --baseline
   → línea base VERDE

4. No iniciar si E7 sigue solo en rama/PR abierto.

Si E7 no está fusionado:
PARA con CERO COMMITS.

────────────────────────────────────────────────────────────
1 · A.8 · CONFIRMA LOS CUATRO HUECOS
────────────────────────────────────────────────────────────

Antes de implementar, confirma contra origin/main:

A. No existe todavía una función pública/pura
   estado_calc(calc_id) que derive el estado del CALC.

B. T35 determina hoy `generacion_leida=GEN2` a partir de la existencia de
   `corrida0_resultado_id`, y después intenta detectar el caso
   "GEN2 sin corrida0_resultado_id".

   Si sigue así, el check es circular:
   el caso que pretende detectar no puede construirse.

C. `status` distingue correctamente medición GEN2 de LEGACY, pero no separa
   todavía:
   - resultado GEN2 ya sellado;
   - resultado GEN2 pendiente de adopción por mesa;
   - resultado GEN2 ya adoptado por un consumidor activo.

   En consecuencia existe riesgo de interpretar "medido" como "adoptado".

D. Los cuerpos actuales de cola de E5-0/E5 no coinciden íntegramente con
   ENCARGOS-GEN2-v1_5, especialmente E5:
   - debe ocurrir después de E6 y E7;
   - debe rederivar registro/status;
   - debe convertir T35 WARN → FAIL al cierre;
   - E6 ya no puede aparecer como sucesor futuro.

Si alguno ya fue corregido por E7 u otro commit posterior, NO lo
reimplementes. Reporta RESUELTO-POR:<commit> y continúa.

────────────────────────────────────────────────────────────
P1 · ESTADO DERIVADO ÚNICO DE CALC
────────────────────────────────────────────────────────────

Implementar en tools/corrida0.py una función pura:

estado_calc(calc_id, evalua_preflight=False)

No crear un archivo persistente de estado.

Derivar exclusivamente de artefactos reales:

sin spec.yaml
    → BORRADOR

spec.yaml presente, sin ejecución
    → SPEC-FIJADA

spec.yaml presente y,
si evalua_preflight=True,
preflight devuelve VERDE
    → PRE-FLIGHT-VERDE

ejecucion.json/resultados.json presentes,
sin sello válido
    → EJECUTADA-NO-SELLADA

sello completo válido
    → SELLADA

SUPERADO→sucesor sigue siendo una propiedad derivada por registro a partir
de la cadena de sucesión. No duplicarla dentro del CALC.

Añadir CLI pequeño:

python3 tools/corrida0.py estado CALC-X

con salida humana y --json si encaja barato con el parser existente.

IMPORTANTE:
`cmd_registro` debe reutilizar estado_calc en lugar de mantener otra
implementación independiente de la misma máquina de estados.

Cerrar NC-0010 si esto queda demostrado.

No persistir `estado` en un cuarto archivo.

────────────────────────────────────────────────────────────
P2 · FIREWALL GEN2 NO CIRCULAR
────────────────────────────────────────────────────────────

Corregir T35 para que la generación del CONSUMIDOR se derive de una señal
independiente de `corrida0_resultado_id`.

Adoptar un campo explícito y namespaced para consumidores activos:

corrida0_generacion: GEN2

Un consumidor GEN2 adoptado debe declarar ambas cosas:

corrida0_generacion: GEN2
corrida0_resultado_id: <RESULT>

No modificar consumidores LEGACY existentes solo para rellenar la marca.

Reglas:

corrida0_generacion=GEN2
+
corrida0_resultado_id ausente
    → T35 WARN ahora / FAIL después de E5

corrida0_resultado_id presente
+
corrida0_generacion != GEN2
    → WARN por cadena incompleta

corrida0_generacion=GEN2
+
resultado_id no resuelve
    → WARN/FAIL

corrida0_generacion=GEN2
+
resultado resuelve a LEGACY-GEN1
    → WARN/FAIL

corrida0_generacion=GEN2
+
RESULT sellado GEN2
+
valor materializado distinto
    → WARN/FAIL con comparación por tipo

La detección de generación NO puede depender de la misma marca cuya
ausencia se intenta detectar.

No convertir todavía T35 entero a FAIL.
Eso sigue reservado para el cierre de E5, tal como manda v1.5.

────────────────────────────────────────────────────────────
P3 · SEPARAR MEDICIÓN DE ADOPCIÓN
────────────────────────────────────────────────────────────

No alterar la semántica actual:

dependencias_numericas_legacy_activas

debe contar lo que el motor/consumidor ACTIVO sigue leyendo.

Por tanto, si E5 mide un RESULT pero mesa todavía no lo adopta:

legacy activa NO baja.

Añadir al status únicamente los contadores derivados necesarios para hacer
visible la transición:

N_resultados_gen2_sellados

N_resultados_gen2_pendientes_adopcion

N_resultados_gen2_adoptados_activos

Definiciones:

SELLADO:
RESULT de una corrida con cuenta_gen2=SI y sello válido.

PENDIENTE_ADOPCION:
RESULT sellado GEN2 citado por una entrada de propuesta
PENDIENTE-DE-MESA, pero aún no por un consumidor activo GEN2.

ADOPTADO_ACTIVO:
RESULT sellado GEN2 citado por un consumidor activo con:
corrida0_generacion=GEN2
corrida0_resultado_id=<ese RESULT>

No infieras adopción únicamente porque el resultado existe.

No reduzcas `dependencias_numericas_legacy_activas` hasta que el consumidor
activo realmente cambie.

El flujo esperado debe quedar:

E5:
  sellados             0 → k
  pendientes adopción  0 → k'
  adoptados activos    0
  legacy activas       162

SELLO/adopción posterior:
  pendientes adopción  ↓
  adoptados activos    ↑
  legacy activas       ↓

Los números exactos se DERIVAN, nunca se codifican.

Actualizar tools/tablero_programa.py para mostrar estos contadores leyendo
`status`, nunca recalculándolos.

────────────────────────────────────────────────────────────
P4 · SINCRONIZAR DESPACHO CON v1.5
────────────────────────────────────────────────────────────

Este defecto ya ocurrió: la dirección emitió v1.5 pero los archivos de cola
conservaron cuerpos anteriores.

Automatizar solamente lo suficiente para que no vuelva a ocurrir.

1. Incorporar al repo, verbatim, el documento de dirección:

ENCARGOS-GEN2-v1_5-aparato-antes-de-calcular-2026-09-08.md

en la ubicación de encargos maestros que mejor siga la convención existente.

Añadir sidecar SHA256.

No reescribir su cuerpo.

2. Como E7 ya habrá sido ejecutado/fusionado, NO reescribir su historia
retroactivamente.

3. Sincronizar los cuerpos activos que todavía faltan ejecutar:

GEN2-E5-0
GEN2-E5

con las secciones respectivas de v1.5.

En particular E5 debe contener:

- E6 ya fusionado;
- GO-MARCADOR de E7;
- preflight → run → verify;
- COMMIT-2;
- registro + status después de cada CALC;
- T35 WARN → FAIL al cierre;
- no adopta automáticamente valores;
- no toca spec.yaml;
- no lista E6 como sucesor futuro.

4. Crear un verificador pequeño y determinista, por ejemplo:

tools/verifica_encargos_gen2.py

Modo mínimo:

python3 tools/verifica_encargos_gen2.py --verifica

Debe comprobar que un encargo GEN2 ACTIVO en cola coincide con la sección
que le corresponde de la versión maestra vigente.

No necesita ser un framework de despacho.

Si difiere:

PARO · ENCARGO-GEN2-DESFASADO

con:
archivo
versión maestra
sección
sha esperado
sha observado

No corregir automáticamente por defecto.

Si agregar `--aplica` es trivial y seguro, puede existir únicamente para
copiar verbatim una sección a su archivo de cola. Sin decisiones.

Añadir la verificación al arranque de /acto SOLO para encargos GEN2 si el
costo es pequeño.

────────────────────────────────────────────────────────────
P5 · TABLERO MATERIALIZADO
────────────────────────────────────────────────────────────

E6 ya corrigió el DERIVADOR pero el archivo committeado del tablero quedó
atrás.

Después de P1-P4:

python3 tools/tablero_programa.py --actualiza

Verificar:

python3 tools/tablero_programa.py --json

y confirmar que el bloque materializado contiene los contadores GEN2
actuales y el marco vigente derivado.

Cerrar NC-0014 si procede.

No añadir un test periódico solo para comparar el tablero si el propio
--actualiza ya es determinista.

────────────────────────────────────────────────────────────
P6 · TESTS, SOLO LOS DEFECTOS OBSERVADOS
────────────────────────────────────────────────────────────

Añadir únicamente estos falsadores:

T-ESTADO-CALC-DERIVADO

Prueba:
BORRADOR
SPEC-FIJADA
PRE-FLIGHT-VERDE
EJECUTADA-NO-SELLADA
SELLADA

y que registro reutilice la función en vez de divergir.

T-GEN2-SIN-RESULTADO-ID

Fixture:
corrida0_generacion: GEN2
valor materializado presente
corrida0_resultado_id ausente

T35 DEBE avisar.

Este test es obligatorio porque el mecanismo anterior no podía construir
el caso que decía detectar.

T-RESULTADO-ID-SIN-GENERACION

Fixture:
corrida0_resultado_id presente
corrida0_generacion ausente

Debe avisar por cadena incompleta.

T-STATUS-MIDE-NO-ADOPTA

Fixture:
RESULT GEN2 sellado
+
propuesta pendiente que lo cita
+
consumidor activo todavía LEGACY

Debe resultar:

sellado = sí
pendiente_adopcion = sí
adoptado_activo = no
legacy_activa = sí

Luego cambia únicamente el consumidor fixture a:

corrida0_generacion: GEN2
corrida0_resultado_id: RESULT-X

Debe resultar:

pendiente_adopcion = no
adoptado_activo = sí
legacy_activa = no

T-ENCARGO-GEN2-DESFASADO

Fixture maestro/cola:
una diferencia de un byte debe hacer fallar --verifica.

No añadir tests de nombres, ADR, formato o anomalías no relacionadas.

────────────────────────────────────────────────────────────
P7 · NO IMPLEMENTAR AHORA
────────────────────────────────────────────────────────────

NO implementar `vigencia` ni `delta` en este acto.

Razón:
el cuerpo v1.5 no define suficientemente su contrato operativo y `delta`
todavía no tiene valores GEN2 reales sobre los que medir materialidad.

Deben seguir declarados como pendientes.

No inventar definición para llenar el hueco.

NO construir todavía un orquestador general:

preflight → run → verify → commit → registro → status

Primero queremos observar E5 sobre tres CALC reales.

Si el ritual se repite sin cambios después de E5, ése será el momento de
automatizarlo.

NO tocar:

CALC-0001
CALC-0002
CALC-0003
sus specs
microdatos
M/R/L/agregado de E7
tramite.yaml activo
procedencia.yaml activo
valores del modelo

────────────────────────────────────────────────────────────
P8 · VALIDACIÓN
────────────────────────────────────────────────────────────

Ejecutar:

python3 tests/test_corrida0.py
python3 tests/check.py --baseline
python3 tools/verifica_encargos_gen2.py --verifica
python3 tools/corrida0.py status --json
python3 tools/tablero_programa.py --json

Y demostrar:

ESTADO-CALC-UNICO=PASS
T35-NO-CIRCULAR=PASS
GEN2-SIN-RESULTADO-ID-DETECTADO=PASS
MEDICION-SEPARADA-DE-ADOPCION=PASS
LEGACY-NO-BAJA-POR-MEDIR=PASS
DESPACHO-v1.5-SINCRONIZADO=PASS
TABLERO-ACTUALIZADO=PASS
BASELINE=VERDE

Además:

python3 tools/corrida0.py run CALC-SMOKE-0002

debe seguir respondiendo:

CALC-INMUTABLE · YA-SELLADO

sin modificar un byte.

────────────────────────────────────────────────────────────
CRITERIO DE SALIDA
────────────────────────────────────────────────────────────

Solo declarar:

APARATO-GEN2-PRE-E5=READY
GO-E5-0=SI

si todos los PASS anteriores se cumplen.

Si falla uno material:

APARATO-GEN2-PRE-E5=NO
GO-E5-0=NO

y reportar el fallo exacto.

No abrir otra auditoría general.

────────────────────────────────────────────────────────────
NO-CORRIDO / RESERVAS
────────────────────────────────────────────────────────────

Cerrar únicamente las reservas que este producto realmente resuelva.

Esperadas:

NC-0010 → CERRADA si estado_calc queda operativo.
NC-0014 → CERRADA si tablero materializado queda actualizado.

NC-0011 sigue para E5-0 porque exige probar las specs reales.

No hace falta cerrar aquí:
NC-0007/NC-0012
NC-0008/NC-0013
NC-0002

si no afectan E5-0 ni cambian una medición.

No duplicar una reserva ya existente para volver a decir lo mismo.

────────────────────────────────────────────────────────────
CIERRE
────────────────────────────────────────────────────────────

Un PR.

Primero reportar:

1. qué cable se cerró;
2. qué automatización queda operativa;
3. cómo queda separada medición de adopción;
4. APARATO-GEN2-PRE-E5 = READY/NO;
5. GO-E5-0 = SI/NO.

Después:
## NO-CORRIDO / RESERVAS

Cascada normal de /acto.

No hacer cálculos.

──── FIN DEL CUERPO VERBATIM (A.3) ────

## NO-CORRIDO / RESERVAS

- **P7 · `vigencia`/`delta` (contrato B-6/B-7).** DECISIÓN-DE-MESA-PENDIENTE
  — `ENCARGOS-GEN2-v1_5` no define su contrato operativo y `delta` no
  tiene todavía un `valor_gen2` real contra el que medir materialidad; no
  se inventa definición para llenar el hueco. Impacto: `vigencia`/`delta`
  siguen `NO-IMPLEMENTADO` (`corrida0.py`), `diferencias_materiales` sigue
  derivando `0` declarado. Sucesor: SIN-ASIGNAR (mesa define el
  contrato).
- **P7 · orquestador general `preflight→run→verify→commit→registro→
  status`.** FUERA-DE-PERÍMETRO — el propio encargo manda observar
  `GEN2-E5` sobre tres CALC reales antes de automatizar el ritual.
  Impacto: ninguno — cada paso de `GEN2-E5` se sigue ejecutando a mano,
  un comando a la vez. Sucesor: acto posterior a `GEN2-E5`, si el ritual
  se repite sin cambios.

## CONSUMIDO

`PR #614` (`https://github.com/Josanoforo/Modelado-Mexicano/pull/614`),
rama `claude/gen2-pre-e5-cableado-kyo7fh`. Implementa P1-P6 sobre
`tools/corrida0.py`/`tests/check.py`/`tests/test_corrida0.py`/
`tools/tablero_programa.py`, incorpora `ENCARGOS-GEN2-v1_5` con sidecar
sha256, resincroniza `GEN2-E5-0`/`GEN2-E5` en cola, añade
`tools/verifica_encargos_gen2.py`, y refresca
`forense/tablero/TABLERO-PROGRAMA.md`. Cierra `NC-0010` y `NC-0014`.
`APARATO-GEN2-PRE-E5=READY` · `GO-E5-0=SI`. `python3 tests/check.py
--baseline`: **LÍNEA BASE VERDE** (3 FAIL preexistentes/189 WARN).
**NO fusionado por este acto** — el merge es de mesa (`.claude/commands/
acto.md` paso 9).
