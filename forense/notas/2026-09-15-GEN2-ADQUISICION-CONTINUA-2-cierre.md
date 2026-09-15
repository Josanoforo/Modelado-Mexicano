# Cierre · GEN2-ADQUISICION-CONTINUA-2

**Fecha:** 2026-09-15  
**PR principal:** #782  
**HEAD funcional desplegado:** `70a2a8f59b76221a52155416499ea7aed1c16a79`  
**Evidencia operativa:** #783 y #784  
**Mediciones/adopciones científicas:** 0/0

## Necesidad y evidencia

Se continuó `DEM-AHORRO-STOCK-DURACION-01` desde su cursor vigente. La ruta
dirigida buscó el cuestionario o catálogo de variables exacto de
`MEX_2012_FCS`. El catálogo público del Banco Mundial no devolvió el estudio
exacto y los resultados indexados condujeron al informe ya examinado o a
instrumentos distintos. `MEXICO_FINANCIAL_CAPABILITY_SURVEY_2012` conserva
evidencia de diseño nacional, ahorro y gasto inesperado, pero no acredita la
duración financiable del mismo stock.

No hubo adquisición: **0 objetos intentados, 0 objetos nuevos y 0 bytes
nuevos**. El negativo es acotado a esta ruta, no una afirmación de inexistencia
del instrumento. Tras dos ciclos sin avance material quedó visible para mesa la
alternativa ya prevista: relabel acotado de #772; no se ejecutó esa decisión.

La brecha se redujo al descartar una ruta pública exacta y evitar que vuelva a
consumir otra activación. El modelo todavía no puede usar una duración del
stock de ahorro; sí conserva el diseño y los reactivos de ahorro/gasto
inesperado como evidencia parcial, sin adopción nueva.

## Presupuesto acreditado

Los techos diarios permanecen en 3 investigaciones, 5 objetos y 3,900 s de
ejecutor. La gracia de terminación se contabiliza por separado.

| Corte | Disponible antes | Reservado | Consumido | Devuelto | Disponible después |
|---|---:|---:|---:|---:|---:|
| Liquidación histórica `2026-09-15T104704-88296` | 2/0/0 s bajo el ledger legado | 1/5/3900 s | 1/0/227 s | 0/5/3673 s | 2/5/3673 s |
| Continuación `2026-09-15T121736-152735` | 2/5/3673 s | 1/5/3673 s | 1/0/283 s | 0/5/3390 s | 1/5/3390 s |
| Total del día tras la continuación | — | 0/0/0 s activas | 2/0/510 s | — | 1/5/3390 s |

En la liquidación histórica, 227 s es la ventana conservadora acreditada por
los logs entre invocación y cierre del hijo; el recibo anterior medía 250 s del
runner. La enmienda `[ADQ-LIQUIDACION]` se añadió al mismo `run_id` sin alterar
el recibo original. No hay reservas materiales pendientes de recuperación.

## Continuidad productiva

La primera activación manual recorrió la tarea Windows existente, invocó Codex,
registró checkpoints de ejecutor e investigación, midió 283 s con reloj
monotónico externo, liquidó antes de publicar y abrió #784 con la evidencia de
la continuación. El segundo disparo normal,
`2026-09-15T122712-156707`, compartió el ledger, conservó 1/5/3390 s y terminó
en `COMPROBACION-LIGERA` con `comprobacion-sin-despacho`: no había trabajo
elegible y no invocó al modelo. No se fabricó una necesidad para probarlo.

La tarea `\\ModeladoMexicano\\AdquiereCron` quedó desplegada sobre el SHA
funcional remoto indicado, con zona `America/Mexico_City`, ejecución diaria a
las 07:30 y repetición horaria. La próxima activación nominal observada en la
configuración era 2026-09-15 13:00 local; su evento automático sólo debe darse
por observado si aparece en el historial de la tarea.

## Revisión end-to-end del cableado

Se recorrió la cadena completa:

`Task Scheduler -> PowerShell oculto -> WSL -> launcher -> lock único ->
actualización al SHA -> recuperación de huérfanos -> comprobación ligera ->
wrapper -> selección/reserva -> checkpoints -> Codex -> validación -> reloj
monotónico -> liquidación -> censo/recibo -> heartbeat -> siguiente activación`.

Además del defecto original, la revisión encontró y corrigió cuatro cortes
materiales:

1. la recuperación de reservas huérfanas ocurría demasiado tarde para que la
   comprobación ligera pudiera despachar;
2. un fallo del checkpoint podía dejar que el hijo trabajara sin cargo
   acreditable;
3. el estado publicado por un PR automático aún no fusionado permitía repetir
   la misma versión de investigación desde el clon productivo restaurado;
4. dos censos idénticos del mismo día podían producir un commit/PR espurio.

El ledger V2 conserva consumo, reserva activa, devolución y recuperación
pendiente por `run_id`; sus escrituras son atómicas y la liquidación es
idempotente. Una reserva viva no se libera, una incierta queda retenida y el
checkpoint final impide repetir trabajo ya realizado aunque la publicación o
el merge de evidencia estén pendientes.

## Verificación

- `tests/test_adq_continua.py`: 8 grupos verdes.
- `tests/test_adq_cableado.py`: 34 pruebas verdes.
- Sintaxis Bash, compilación Python y `git diff --check`: verdes.
- `tests/test_adq_descubrimiento.py`: conserva el único fallo heredado de
  baseline sobre la demanda de instrumento tras el cierre de `NC-0126`; no fue
  introducido por este acto.
- Los tres consumidores `RES-0046`, `RES-0048` y `RES-0065` permanecen
  `PENDIENTE_DATOS_O_DECISION_DE_USO`, no disponibles y vinculados a la demanda
  independiente.

El proyecto queda más cerca de una decisión o modelo mejor en dos sentidos
concretos: recuperó cupo utilizable el mismo día y ejecutó una continuación que
descartó una ruta exacta sin duplicarla. No produjo una medición ni autorizó una
adopción científica.
