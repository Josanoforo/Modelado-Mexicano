# Cierre · GEN2-CONSULTA-OPERATIVA-CON-CONTRATO

Fecha: 11/sep/2026
Entorno: NUBE, Codex CLI
PR: #729
ADR: ADR-485

## Resultado

`tools/consulta_gen2.py` ofrece una entrada terminal real al emisor GEN2. La
petición exige consumidor por identidad exacta, propósito `consulta` o
`transferencia`, contexto de dominio explícito y uso solicitado. La interfaz
acepta banderas o JSON, lista consumidores/campos de dominio y reproduce lotes
sin generar el snapshot completo.

La respuesta humana y JSON incluye RESULT y fuente, población, unidad, evento,
periodo, transformación y dependencia, aptitud, validación independiente
disponible, alcance, versión/hash del contrato y referencias utilizadas.
`valor` sólo aparece si `estado=EMITE`; todo fallo cerrado conserva una causa
concreta. Una proporción poblacional se rotula expresamente como tal y no como
diagnóstico o probabilidad personalizada.

La ruta normal es GEN2 y no se expone una ruta histórica. Consulta usa sólo el
RESULT adoptado. Transferencia exige el objeto `SELECCION-TEMPORAL-v1`
completo y lo entrega a la autenticación incorporada por #720; el wrapper no
acepta parámetros sueltos como selección. No hay fallback numérico legacy,
cero, imputación ni sustitución por R.

Después del merge de #731, el comando consume sin recalcular la proyección de
`data/corrida0/resultados.tsv` que entrega `cargar_indice_linaje_emision()`. La
verificación exhaustiva de las identidades publicadas por
`listar_consumidores()` confirma 16 RESULT directos: 16 `EMITE` y 16 `PASA`.
No se importó ni ejecutó el validador independiente de #731.

## Recorrido demostrado

`forense/ejemplos/GEN2-CONSULTA-OPERATIVA-CON-CONTRATO/peticiones.json` y
`respuestas.json` conservan once recorridos reproducibles:

- CIV, DIN, FAM y TRA emiten respectivamente `0.29431298745731216`,
  `0.541343`, `0.04569409956405095` y `0.08511814556534456`;
- dominio falso y consumidor legacy en GEN2 devuelven `NO_COVERAGE`;
- ENIGH 2020→2022 emite `0.04377543852935772` con rol
  `OBSERVACION-SERIE-PREVIA`;
- ENVIPE→remesas por parámetros sueltos y una selección posterior al corte
  devuelven `NO_COVERAGE`;
- el complemento adoptado emite `0.8739943899100835` con padre y `1-p`;
- el proxy r2 pedido como `MEDICION-GEN2` devuelve `NO_COVERAGE` por uso.

Total: seis `EMITE` y cinco `NO_COVERAGE`. Los ejemplos sólo escriben en su
directorio propio. Cualquier otro `--salida` rehúsa sobrescribir un archivo
existente salvo `--sobrescribir` explícito; ningún camino escribe snapshots.

## Evidencia dirigida

- `python3 -m unittest tests.test_consulta_gen2 -v`: 8/8 después de publicar
  la respuesta dorada; su primer caso recorre además las 16 identidades GEN2
  directas y exige `EMITE`, RESULT exacto y `PASA`.
- `python3 -m unittest tests.test_motor_gen2_explicito tests.test_motor_usos_complementos -v`:
  pruebas de regresión del emisor y complementos.
- Las tres suites juntas: 37/37.
- `python3 -m tools.snapshot_motor_gen2 --verifica forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_2.json`:
  `OK`.
- `python3 tools/consulta_gen2.py --lote .../peticiones.json --verifica .../respuestas.json`:
  `OK`.
- `git diff --check`: limpio.
- `python3 tests/check.py`: ningún fallo introducido; permanecen tres `FAIL`
  heredados (`T06` ×2 y `T08` ×1), fuera del perímetro de esta consulta.

El snapshot v1.0 conserva SHA-256
`05350667baa245c79c3ed487aeb1403d74b4612fcae69e16845b8d42f1a5eaa8`; el
v1.1 conserva
`95d36cef4735f85a22f0346bc04dabdab2f13724c96e9a19179996cb93bca3bb`.
Ninguno fue modificado. El snapshot vigente v1.2, recibido de #731, verifica
con SHA-256
`ca083554b8cd844b1a54a6147d37e26ff4096f15037e8cae6b4450f64ee763e6`.

Las respuestas reproducibles fueron actualizadas contra el estado vivo: los
RESULT directos que antes declaraban `NO-HECHA` ahora declaran `PASA`. La única
`NO-HECHA` restante es `RESULT-B-ENIGH-2020-P` en la transferencia histórica;
no pertenece al conjunto directo validado por #731 y coincide con la vista
vigente, por lo que no contradice el overlay.

## Alcance y residual

No se modifican por este acto `milpa/src/emisor.py`, criterios científicos,
RESULT, usos, capturas, specs, snapshots ni overlay de validación. El comando
consume el estado de validación que publique la interfaz vigente y la regresión
fija la cardinalidad contractual actual en 16 RESULT directos con `PASA`. No
abre F6, no calibra, no adopta, no evalúa
generalización y no incrementa el contador científico. No queda residual
técnico dentro del encargo; sólo falta la revisión y fusión del PR por Jonás.
