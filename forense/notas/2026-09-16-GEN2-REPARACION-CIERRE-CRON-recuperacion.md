# GEN2 · recuperación de cierres IHSN y ENPOL

Fecha: 2026-09-16. Entorno: CAJA/WSL. Este acto no invocó al modelo, no
investigó y no descargó bytes. Revalidó los JSON finales originales y los
bytes ya adquiridos; los `exit=65` históricos permanecen intactos en los logs
operativos y en sus recibos publicados.

## Referencias preservadas

| PR | SHA | Aporte absorbido |
|---|---|---|
| #805 | `6bb4545c245eddd4e1a28af93f5e81d1af364e77` | IHSN ENNViH-3: fila canónica, manifiesto, estado y nota de adquisición |
| #807 | `44a4c01cacb155dc5a0c5e20850e7c9d4a268be6` | evidencia del censo de 2026-09-16; la proyección de demanda se regenera contra el corte vigente, no se copia |
| #808 | `c13e85a0a579e0396c715e563d46a74a53c535d0` | ENPOL 2016, avance de las tres investigaciones y última frontera/cursor respaldados |

El archivo `forense/censo-raiz/2026-09-16.txt` de #807 tiene SHA-256
`2d4f2837cfec494f64b1f52dda1f9133d59927e305137b746f2ec38498f50017`.
Su recibo conserva `run_id=2026-09-16T000001-216797`, `exit=65`,
`resultado=resultado_invalido`, reserva `3/5/3900s`, consumo `3/2/742s` y
devolución `0/3/3158s`. La proyección vieja de ese PR, SHA-256
`31f17fb583ac3c03a1429ec3cc0f32d2a8868bd2b05837d7dff4ca9ef1bd386d`,
queda superada por la regeneración canónica de este acto.

## Defecto y regla reparada

El cierre comprobaba pertinencia sólo buscando el ID literal del objeto dentro
de `usado_para`. Los dos recibos declaraban correctamente el ID de manifiesto y
la fila canónica exacta del objeto lo vinculaba en `ids_manifiesto`, pero el
texto humano describía el consumidor/uso. La regla reparada acepta, para cada
ID informado, el vínculo exacto en `ids_manifiesto` de la fila canónica del
mismo objeto; conserva como alternativa compatible la coincidencia literal en
`usado_para`. Un ID presente sólo en otra fila no acredita el objeto.

La revalidación de IHSN descubrió un segundo defecto del mismo cierre: junto a
la ref Git verificable había un enlace informativo al PR. Ahora al menos una
referencia `refs/heads/<rama>` con SHA remoto exacto sigue siendo obligatoria;
un enlace GitHub adicional se permite como contexto, pero una URL sola no
acredita publicación.

## Revalidación de originales

Se montaron árboles separados en los SHA originales de #805 y #808, apuntando
`data/raw` al corpus local existente. Se cargó la función corregida desde esta
rama y se llamó con el JSON final, la selección de objetos y la selección de
investigación originales, primero sin red y después con
`comprobar_remoto=True`. Ambos informes devolvieron:

`{"cierre_exitoso":true,"errores":[],"publicacion_trabajo":"publicada","resultado_trabajo":"descubrimiento_y_adquisicion","valido":true}`.

| run_id | árbol/contexto original | JSON final original (SHA-256) | resultado histórico | revalidación | investigaciones / objetos / bytes acreditados | remanente tras liquidación |
|---|---|---|---|---|---|---|
| `2026-09-15T222751-201668` | launcher `48a875a0990dbf8b60dda4dfa309e4742a503f6f`; trabajo #805 | `f8da1a0aefa81acc699e3472ea61308e378f9440bba51ce86e36c575c46fa167` | `exit=65`, `resultado_invalido`; errores originales: pertinencia textual y enlace PR tratado como ref Git | original, no reconstrucción: válida; ref remota #805 comprobada | 1 investigación; 1 objeto IHSN; 10,243,502 bytes | `0/4/2952s` (necesidades/objetos/segundos) |
| `2026-09-16T000001-216797` | launcher `9fd59d0632428b3344b02e187ddb51f65b71d0b3`; trabajo #808; recibo #807 | `fc95e60f5106d5451003adb88e83432be1897f8ac507f451b7f9730644af98d8` | `exit=65`, `resultado_invalido`; error original: pertinencia textual ENPOL | original, no reconstrucción: válida; ref remota #808 comprobada | 3 investigaciones; 2 checkpoints de objeto consumidos, 1 objeto nuevo ENPOL; 16,801,537 bytes nuevos | `0/3/3158s` |

Selecciones originales: IHSN
`158f7ce43b419a11fa7f59e5505770ca4ec5bff759a8398f34481a529c2aebca`
y ENPOL
`1a49951f00b706268a501e55949da8216232987247f0c80726b9976bec855029`.
Los recibos de validación fallida originales conservan SHA-256
`8235bad0d1dd99c3d286d92fe7401b80d07ca3f5be7b50fcbd0dbdb55844ff57`
y `2db860a44cf8d688a981728a46019eb1e01744dcb5dc10fc59e376752ec7738a`.

Los bytes locales coinciden con sus manifiestos:

- IHSN: 10,243,502 bytes, SHA-256
  `e9a1764bf2b82d6b65bfa1a2a0d15820b7c67d775cd253d0c0bb7baf7a6d32d9`.
- ENPOL: 16,801,537 bytes, SHA-256
  `a405ed7777b8f51d338347e6cef94c5daa05f00625b6cd1709ecd49d6ab06997`.

No se recontaron adquisiciones ni se devolvió presupuesto. Los ledgers
operativos ya estaban liquidados, sin reserva activa; se conservaron. Sus
SHA-256 al revalidar eran
`3df8b43b4263ad4b9c4f934558932d280992cf84a88a5af2b8e402d4b2a405c7`
(2026-09-15) y
`7e3087b7f808a38a0dc7ec3998fd0fa13f71e3900b7444e13288be9e818c65f0`
(2026-09-16).

La demanda se regeneró con el escritor canónico para el corte 2026-09-16:
65 activas, 64 NC abiertas, SHA-256 del archivo
`d21693c034601f090bb447a8d78cc40575d699992727c6c3d24b472085734c3a`.
Su `sha256_fuente`
`fd1694075318fe29439c323a65b0e6475c9e8a8beed1da7516f420b3e0ec75b8`
coincide con `forense/no-corrido.tsv`; el JSON conserva además las huellas de
los demás insumos del mismo corte en `fuentes_sha256`.

## Alcance conservado

- IHSN ENNViH-3 queda adquirido, legible y registrado para identidad,
  inventario y descripción documental. No aporta por sí solo UPM/estrato
  ejecutables ni habilita intervalos de CORR-0008.
- ENPOL 2016 queda adquirido, legible y registrado con las condiciones ya
  declaradas. Sigue `OBTENIDO-PARCIAL`: faltan FD, reactivo, codificación,
  ponderador y comparabilidad; no habilita una evaluación confirmatoria.
- NC-0202 permanece `continua` y ABIERTA. Se preservan la última frontera y el
  último cursor de la corrida del 16 de septiembre, además de la evidencia IHSN
  del ciclo previo.
- `DEM-AHORRO-STOCK-DURACION-01` conserva el último cursor/frontera; el contador
  se fija en 4 ciclos, no 5, porque hubo una sola actualización adicional
  respaldada por esta corrida.

## Verificación del sucesor

- `tests/test_adq_cierre_verificable.py`: 13 casos correctos, incluidos los
  positivos IHSN/ENPOL y los negativos de fila ajena, subcadena y URL sin ref.
- `tests/test_adq_continua.py`: 8 grupos correctos.
- `tests/test_adq_demanda_vigente.py`: 7 casos correctos.
- `tests/manifiesto.py --verifica` aprobó por separado IHSN y ENPOL contra los
  bytes locales existentes.
- El gate completo del sucesor produjo `3 FAIL · 4347 WARN` y
  `LÍNEA BASE: VERDE`; un árbol limpio de `origin/main` produjo exactamente el
  mismo resultado. Los tres fallos son heredados, no introducidos por esta
  reparación. T16, T26 y T27 aprobaron.
- `tests/test_adq_descubrimiento.py` conserva un fallo heredado de
  `origin/main` sobre el enrutamiento de NC-0202; la comparación limpia confirmó
  que no es regresión de este cambio.

## Dictamen

- Contrato: reparado y cubierto por regresión positiva/negativa.
- Recuperación histórica: acreditada sobre los dos JSON originales; no hubo
  reconstrucción.
- Publicación histórica: las refs exactas de #805 y #808 existen en remoto; los
  recibos `exit=65` se preservan.
- Despliegue: se acredita por separado al fijar y comprobar el SHA remoto del PR
  sucesor; no se confunde con integración.
- Integración: pendiente de decisión de mesa hasta fusionar el PR sucesor.

El servicio puede reconocer el trabajo ya producido sin repetir su costo. Este
dictamen no declara el cron completamente cerrado ni cierra NC-0202/NC-0162.
