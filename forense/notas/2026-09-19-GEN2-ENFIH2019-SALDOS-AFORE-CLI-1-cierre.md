# Cierre · GEN2-ENFIH2019-SALDOS-AFORE-CLI-1

## Entrega

Se creó `CALC-ENFIH2019-SALDOS-AFORE-0001` en worktree
`/home/pc0/mm-gen2-enfih2019-saldos-afore-cli-1`, rama
`codex/gen2-enfih2019-saldos-afore-cli-1`, desde
`origin/main=8e455bd6a3870566d6776fef19834c4da16d2fa9`.

COMMIT-1 `dbc34849fdf6acbcd3767fe25513e5fc3c53ec6f` congeló spec humana/YAML,
medidor, pruebas sintéticas y copia verbatim del encargo. La primera ejecución
posterior produjo 65 RESULT, quedó SELLADA y `verify` dio
`REPRODUCE · CONTEXTO=IDENTICO` para todos.

La medición principal y sus reservas están en
`forense/analisis/enfih2019-saldos-afore-cli-1/medicion.md`.

## CONSUMIDO

- `enfih2019_bd_csv_zip`, SHA-256 `be372533…f4d5`.
- `enfih2019_fd_xlsx`, SHA-256 `326b68b…48e1`.
- `CALC-ENFIH-0001` solo como control de tenencia.
- `prereg-caja-ENFIH-AFORE` y
  `2026-09-01-MAESTRA33-E18-P3-L1-spec` con exposición declarada.
- Cuestionario y diseño conceptual oficiales como documentación temporal, no
  versionada, para periodo, alcance, códigos e imputación.

## NO-CORRIDO / RESERVAS

- No se imputaron saldos parciales/desconocidos ni se extrapoló stock nacional.
- No se actualizó a precios de 2026 ni se anualizó el stock.
- No se abrieron perfiles por `CAT_POS`, ingreso, entidad ni otros cortes.
- No se midieron planeación, aportación voluntaria, formalidad, estabilidad ni
  causalidad.
- No se modificaron milpa, canon, NC/FP, decisiones, tablero, workflows ni
  sesiones ajenas.
- `cuenta_gen2`, adopción y contador permanecen `PENDIENTE-DE-MESA`.
- Falta decisión de mesa sobre consumo: aceptar la distribución como
  descriptiva del dominio cubierto, pedir hipótesis/sensibilidades sobre no
  respuesta o no usarla para parámetros del modelo.

## Pruebas y controles

- `pytest -q tests/test_enfih2019_saldos_afore.py`: 5 passed.
- `corrida0 spec-check`: 11 OK, 0 FAIL.
- `corrida0 preflight`: VERDE.
- `corrida0 run`: exit 0, SELLADO.
- `corrida0 verify`: REPRODUCE, CONTEXTO=IDENTICO, 65/65 delta cero.
- Comprobación independiente de media, mediana y varianza/IC de cobertura:
  idéntica a la salida sellada.
- `git diff --check`: limpio antes de COMMIT-1.

El replay aislado, registro derivado, segunda proyección, URL de PR y SHA final
se completan después de COMMIT-2 y se anotan sin afirmar merge o adopción.
