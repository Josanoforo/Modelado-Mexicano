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

## Replay y registro

Después de COMMIT-2, `tools/verifica_aislada.py` produjo
`forense/analisis/enfih2019-saldos-afore-cli-1/replay-aislado.json`:
`REPRODUCE · CONTEXTO=IDENTICO`, 65/65 RESULT y 3/3 inputs. Se asentó una
fila propia en `forense/replay-evidencia.tsv`.

`corrida0 registro --escribe`, sin `--lote`, añadió una corrida y 65 RESULT.
La regeneración sobre la base actual también materializó 20 usos de marcadores
ya presentes; son derivados del comando vigente, no cambios manuales ni
replay ajeno aceptado. Una segunda proyección fue estable byte a byte:

- `corridas.tsv`: `a5a5c8f5e84fd713f09030e6e39c9f1550f3efb7c40c2bba9868d07150d443d2`
- `resultados.tsv`: `126577abb2b9d31b3a9223cfb6f4ce36ba8b8372b740e36ecebaa03d8983ff5b`
- `usos.tsv`: `7f475593df1bf4c7a85ee92a7e0d812c7800afa7cd2cf923dee9308bffbfbe01`

Estado derivado final: `SELLADA`; contador y adopción siguen
`PENDIENTE-DE-MESA`. La URL del PR y el SHA de punta se reportan en la entrega
del ejecutor, sin afirmar merge.

## Continuación: alcance de concentración y cronología de exposición

La aclaración posterior preserva 0001 y añade
`CALC-ENFIH2019-SALDOS-AFORE-CONCENTRACION-0001`. El dominio de concentración
de 0001 —totales completos positivos— fue una elección admisible bajo el texto
original “monto válido y total positivo”; no se reescribió ni se declaró
erróneo. La unidad sucesora mide el 10% superior entre todos los totales
completos, incluidos ceros, y compara ambos dominios con réplicas compartidas.

### Cronología verificable

1. **Antes de COMMIT-1 de 0001:** durante la acreditación se abrieron
   `P9_10/P9_11` y se observaron 1,660 hogares con `V_AFORE>0` y al menos un
   tenedor con código especial. Esto quedó declarado en el preregistro que
   entró en `dbc34849fdf6`; por tanto nunca se afirma congelación anterior a
   toda apertura de respuestas ni ceguera.
2. **Después de `dbc34849fdf6`:** se ejecutó 0001. Su clasificación completa
   produjo 1,681 parciales en total, publicó el dominio positivo y quedó
   sellada en `c57cc3f34b4d`; replay y registro siguieron en `7974c60778f8`.
3. **Continuación actual:** `72e3d72` integró la base vigente sin tocar los
   artefactos de 0001. `babd8ac9a00c` congeló el nuevo spec, medidor, contrato
   y pruebas, declarando exposición completa a 0001. Solo después se ejecutó;
   `f336f7f` publicó su ejecución y sello.

### Resultado adicional

| Dominio | n | Masa | Top 10% del saldo | IC95 |
|---|---:|---:|---:|---:|
| Todos los completos, ceros incluidos | 3,637 | 7,332,887 | 58.5915% | 43.5462–69.7493% |
| Solo completos positivos | 3,601 | 7,271,752 | 58.4482% | 43.3330–69.6356% |
| Diferencia todos−positivos | — | — | +0.1433 pp | +0.0850 a +0.2239 pp |

Los 36 ceros válidos agregan masa, no saldo. Su inclusión eleva levemente la
fracción porque el decil superior del dominio completo debe abarcar más masa.
El comparativo positivo coincide exactamente con 0001. Los tres intervalos
usan 2,000/2,000 réplicas válidas compartidas.

### Qué quedó aclarado y qué se midió

- **Aclarado documentalmente:** el resultado de 0001 responde al dominio
  positivo y no se invalida; la exposición preparatoria precedió su COMMIT-1.
- **Medido adicionalmente:** concentración con ceros dentro del denominador
  poblacional, concentración positiva reestimada y diferencia pareada.
- **Reserva vigente:** solo 37.16% de la masa de tenedores tiene total completo;
  parciales y desconocidos siguen excluidos sin imputación.

La unidad sucesora quedó sellada y su replay aislado dio
`REPRODUCE · CONTEXTO=IDENTICO`, 18/18 RESULT y 4/4 inputs. Un cálculo
independiente reprodujo n, masa, ambos puntos y la diferencia. Contador,
adopción y cualquier uso en el modelo permanecen `PENDIENTE-DE-MESA`.

`corrida0 registro --escribe`, sin `--lote`, publicó la corrida y sus 18
RESULT y regeneró las vistas sobre la base integrada. Una segunda proyección
fue estable byte a byte:

- `corridas.tsv`: `a7f4a15bc727119f7dcfb6b2431d6052380c8ea2fa9b87d1f2f71ab3850b55c8`
- `resultados.tsv`: `a680483c4141ee8032f181b6a1859e9fcf26629662751800673032bd15f8c962`
- `usos.tsv`: `939a06e39277a184490263b24cd86a537301cf0bed918271eba51c68e95ef1bd`

Los hashes de los siete artefactos sellados de 0001 permanecieron idénticos a
los del inicio de esta continuación. La deriva adicional de las vistas procede
de la base actual integrada y del generador vigente; no se resolvió a mano ni
se aceptó replay ajeno.
