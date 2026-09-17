# GEN2 ADQ · diagnóstico y revalidación del cierre 2026-09-17

Run: `2026-09-17T091024-412182`. Corte forense: 17/sep/2026. Esta nota no
reescribe el recibo histórico: conserva como hechos publicados
`[ADQ-RESULTADO] ... null`, `resultado=resultado_invalido`, `exit=65` y
`necesidades_atendidas=0`. El dictamen siguiente es una revalidación
posterior del artefacto original, no un cambio retroactivo del cierre.

## Artefactos originales

Las rutas viven en el clon operativo y siguen gitignoradas; no se copiaron al
repositorio. Tamaños y SHA-256:

| Artefacto runtime | Bytes | SHA-256 |
|---|---:|---|
| `forense/adq-log/2026-09-17T091024-412182-codex.jsonl` | 230122 | `78d689d698af56c937af5509f3418b2cdc216b06507fc3054858d446146de630` |
| `forense/adq-log/2026-09-17T091024-412182-codex.stderr.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `forense/adq-log/2026-09-17T091024-412182-codex-final.json` | 103708 | `d63f38b0359991fe91439fdc033c9d9eb652994d819833280ae694b0a3ab50e2` |
| `forense/adq-log/resultado-2026-09-17T091024-412182.json` | 8431 | `7dc27a567d422ff2353de51e25054e66a4e026a59076e203407f29d12d2f1c11` |
| `forense/adq-log/2026-09-17T091024-412182-seleccion.json` | 31482 | `b532cde361f0bb5240712d06e49b59255b793bcb7579cf01e43eadee658e9d15` |
| `forense/adq-log/2026-09-17T091024-412182-investigacion-seleccion.json` | 90913 | `d9f9984615093b2be99400590dff1f0a9cc9665dced9474d88537f1af19f2e45` |
| `forense/adq-log/2026-09-17T091024-412182-prompt.txt` | 118001 | `a1147a328b34784d645604bee6242eef92ce62b6835bb23e1411045db6d9bbee` |
| `forense/adq-log/2026-09-17T091024-412182-validacion-resultado.json` | 260 | `3d23250f55ed91c3776157b87c28b8bedf09e52f1d919c4e083b0ac0c35ff005` |
| `forense/adq-log/2026-09-17.log` | 23730 | `bf5c7203c99a9ee9b510bf42cb035a8a1c1ed7e64eb5eb42dfb4f78bed597eb8` |
| `forense/adq-log/estado/presupuesto-2026-09-17.json` | 2091 | `6f5501ec7c1f64e5e5254bfe5be6b00fc574c01a41829d31fa1f2032cfd29d9c` |
| `forense/adq-log/estado/2026-09-17T091024-412182-comprobacion.json` | 9986 | `a8edbc17b8f3ae1a902de50845aab34e3547ec9ed1543010e0b43878c9ecdd17` |
| `forense/adq-log/estado/2026-09-17T091024-412182-recuperacion-presupuesto.json` | 610 | `822f3aef21cc960ec2323ed727b5880851f63596592c87bd5dd6ee4cd6aa5150` |

La salida normalizada quedó materializada sobre `codex-final.json`; el
temporal `.normalizado` fue movido por el wrapper. El informe de validación
registró un solo error: `NC-0202: evidencia de investigación inexistente:
data/raw/ennvih_diseno/ennvih-1_muestra.pdf`.

## Primer punto de pérdida

El caso comprobado es **D: el objeto existió y fue rechazado por la
validación**, no B ni C.

1. Ejecución: Codex terminó en 430 s y el JSONL contiene un último
   `agent_message` estructurado. `codex-final.json` es un objeto JSON, no el
   literal `null`.
2. Transporte: `--output-last-message` escribió ese objeto a las 09:28:49 y
   el wrapper normalizó las selecciones autoritativas.
3. Validación: la evidencia citada existía y su SHA coincidía con el
   manifiesto, pero `data/raw` resolvía por symlink a
   `/home/pc0/mm-corpus/raw`. La rama del validador para investigaciones sólo
   permitía `realpath` bajo el clon; la rama para objetos ya permitía el
   corpus compartido. Esa asimetría produjo el falso negativo.
4. Publicación del recibo: `RESULTADO_PUBLICO` sólo se asignaba después de
   validar. Al fallar el paso anterior quedó en `null`, que es el valor
   publicado por `[ADQ-RESULTADO]`. Por tanto, el `null` publicado fue una
   consecuencia del rechazo, no ausencia del canal final.

El artefacto temprano `resultado-2026-09-17T091024-412182.json` fue un handoff
temporal original, pero no sirve como sustituto: declara
`publicacion_trabajo=no_aplica` pese a tres investigaciones y difiere del
cierre final. El selector corregido lo rechaza por esas dos contradicciones.
No se reconstruyó ningún resultado desde #853, notas, diffs o checkpoints.

## Revalidación posterior

Se revalidó el `codex-final.json` exacto, normalizado otra vez con las dos
selecciones originales, sobre un worktree desprendido de
`adq/2026-09-17@55377305827a387ddf0fc15229db95fb9a8f95fa`, con el corpus
montado. El validador de producción corregido comprobó esquema, orden y versión
de las tres investigaciones, evidencias existentes y la ref remota exacta
`refs/heads/adq/2026-09-17@55377305827a387ddf0fc15229db95fb9a8f95fa`.
Resultado: `valido=true`, `cierre_exitoso=true`,
`resultado_trabajo=descubrimiento_documentado`; el candidato temporal siguió
inválido. Existe por tanto **exactamente un candidato completo revalidable**.

La revalidación produjo en runtime un objeto aceptado con SHA-256
`ad51437e6b823c88fd7c7dc202cba0e46eb5a26930975471a8db95505d9717cc`
y un informe con SHA-256
`b774a6f8500f4daab8e16380ee44d99bbab5ea0b91152d5978f97dd328db7c62`.
No se versionan esos archivos runtime.

## Trabajo, adquisición y salud

El ledger conserva cuatro checkpoints: ejecutor y las tres necesidades. La
liquidación histórica sigue siendo `3/0/430s`, con devolución `0/5/3470s`.
La comparación mecánica entre el estado del SHA desplegado
`1746e1a0c7d37d6e0bd93378bc0c527a948990df` y el resultado revalidado da:

- investigaciones seleccionadas/iniciadas/validadas: `3/3/3`;
- objetos intentados/adquiridos/bytes nuevos: `0/0/0`;
- investigaciones con evidencia nueva: `3` (rutas nuevas existentes o
  candidata nueva estructurada);
- investigaciones con reducción de brecha: `1` (`NC-0162`, diseño
  `PARCIAL -> ACREDITADA`);
- salud mecánica agregada: `REDUCCION_BRECHA`.

Lectura acotada por necesidad:

- `DEM-AHORRO-STOCK-DURACION-01`: quinto ciclo, evidencia/candidata nueva
  incompatible y ninguna mejora de suficiencia; conserva la acción de mesa.
- `NC-0202`: evidencia existente del diseño basal, pero sigue
  `INCOMPATIBLE` para el uso completo; no aporta PSU/estrato ejecutable para
  olas 2/3.
- `NC-0162`: mejora documental/de diseño; el uso queda sólo
  `APTA_ALCANCE_MENOR`.

Esto no consolida ciencia: #853 sigue abierto. #852 también sigue abierto en
`censo/2026-09-17@ff844de460c66ebf00a79c41354ef503f5752524`; ninguno de los dos
PR ni el recibo histórico fue reescrito.
