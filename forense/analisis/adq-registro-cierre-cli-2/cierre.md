# GEN2-ADQ-REGISTRO-Y-CIERRE-CLI-2

Fecha: 2026-09-19, America/Mexico_City. Entorno: CAJA/WSL2.
PR: https://github.com/Josanoforo/Modelado-Mexicano/pull/888.

## Resultado

La brecha quedó cerrada en dos planos. El PDF ya existente se registró con
identidad verificable y alcance documental limitado; el productor de cierres
ahora debe validar su handoff con el validador productivo antes de entregarlo.
No se reescribió el run histórico `2026-09-19T160001-63807` ni su `exit=65`.

Worktree `/home/pc0/mm-gen2-adq-registro-cierre-cli-2`, rama
`codex/gen2-adq-registro-cierre-cli-2`, base revalidada
`ea88cb3b94ad820bcd92a485eae51ce24ef07fae`. #884, #885 y #886 estaban
fusionados antes de crear la rama. La base indicada en el encargo,
`6f365928ada3714a02954a7a5be64eb8013ecc9e`, ya había sido superada.

## Registro UCLA

`tests/manifiesto.py` reconoce `estado_reserva` sólo con los dos valores
vigentes y exige que esté ligado a `reserva_respondentes`; asimismo impide que
una entrada bajo esa raíz pierda la marca. Las claves desconocidas continúan
rechazadas.

Sin repetir la descarga, `--registra` creó
`ucla_mxfls_design_summary_2007` para
`data/raw/ennvih/ucla_mxfls_design_summary_2007_a.pdf`. El hash derivado fue
`f6ae6b5f803885a03460a5cc88ca0de8173d3b489caf5deff861d4b300abc405` y
el tamaño 462842 bytes. El escritor residual canónico dejó
`UCLA_MXFLS_DESIGN_SUMMARY_2007` en `OBTENIDO`, vinculado al ID de manifiesto;
la vista se regeneró dos veces con hashes idénticos.

Ficha usable: el informe secundario alojado por UCLA describe en términos
generales una muestra probabilística multietápica MxFLS, 150 comunidades y
tres estratos construidos con 14 variables del marco ENEU. No publica IDs de
UPM/estrato por observación, réplicas ni campos ejecutables de varianza. No
habilita intervalos de confianza ni cierra NC-0202.

## Cierre estructurado

El rechazo histórico tenía dos causas independientes: el texto completo de
`intentos[].resultado` no aparecía en las evidencias citadas y la salida
declaraba `intentos_documentados` aunque contenía investigaciones, por lo que
el validador calculaba `descubrimiento_documentado`.

El prompt del productor ahora exige evidencia literal, deriva la clasificación
de la estructura y, tras escribir atómicamente el handoff, ejecuta
`tools/adq_handoff.py --selecciona-resultado` con las selecciones autoritativas.
Sólo puede entregar después de un código 0. El wrapper conserva una segunda
validación independiente. No se relajaron esquema, igualdad, comprobación de
evidencia ni conflicto entre candidatos.

Corrección posterior del recibo: la revisión inicialmente consignada,
`42bb27a0c429cbf1789824e3a026f4cc16234255`, todavía contenía los backticks
sin escapar y podía ejecutar la prevalidación mientras construía el prompt.
La revisión corregida `462bc3ada670d42988deb66d9415233c3046c4e5`
preserva el comando como texto literal. Su prueba construye la asignación con
un `python3` simulado, exige cero invocaciones y comprueba la instrucción
completa en el texto resultante.

El caso `MANUAL-SINTETICO-20260919` corrió en directorio temporal, sin runner,
modelo, publicación remota ni ledger: cierre válido `0`; clasificación
incompatible `65`; evidencia ausente `65`. Las regresiones existentes
mantienen JSON malformado en `65` y dos candidatos válidos divergentes en
`67`. Los hashes de `ultima-exitosa.json` y del presupuesto productivo se
conservaron.

## Pruebas y operación

- `tests/test_manifiesto_seguro.py`: 6 pruebas, 0 fallos.
- `tests/test_adq_cierre_verificable.py`: 14 casos, 0 fallos.
- `tests/test_adq_handoff_resultado.py`: 14 pruebas, 0 fallos.
- `tests/manifiesto.py --verifica --id ucla_mxfls_design_summary_2007`:
  `COINCIDE`, 462842 bytes.
- `git diff --check`: limpio.

El SHA corregido publicado y fijado con el instalador soportado es
`462bc3ada670d42988deb66d9415233c3046c4e5`. La tarea conservó calendario,
principal, modelo y presupuesto y no se disparó manualmente. La activación
natural de las 18:00 comenzó a las `18:00:02-06:00` con run_id
`2026-09-19T180002-311190`; el launcher resolvió y cargó exactamente esa
revisión a las `18:00:06-06:00`. Al corte `18:03:32-06:00` seguía en
`DERIVACION-DIARIA`, por lo que acredita instalación y arranque natural, no
un cierre ADQ válido. La tarea informó como siguiente ejecución natural
`2026-09-19T19:00:00-06:00`. Permanecen pendientes la terminación de la
activación de las 18:00 y, si llega a despachar adquisición, la validación
extremo a extremo del cierre corregido; no se instaló vigilancia adicional.
