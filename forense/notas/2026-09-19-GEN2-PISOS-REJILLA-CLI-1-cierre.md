# GEN2-PISOS-REJILLA-CLI-1 · cierre para B y Claude

Fecha de verificación: 2026-09-19. Base de preparación:
`843a5f977e024ef5d74863e95856c763bee9e58d`. La rejilla íntegra y sus
valores están en `forense/pisos-rejilla-entrega.tsv` (SHA-256
`93191b9642a54b2822b357b1fc84313500990dc26058ca72f0212643f526f4c3`).

## Resultado ejecutivo

Quedaron publicadas tres corridas sucesoras, reproducibles y con contexto
idéntico:

| Instrumento | CALC vigente | Desenlace | Celdas construidas |
|---|---|---|---:|
| ENVIPE 2024 | `CALC-PISOS-ENVIPE2024-EJES-0002` | evasión | 13 |
| ENVIPE 2024 | el mismo | denuncia por cobertura de seguro | 2 |
| ENCIG 2023 | `CALC-PISOS-ENCIG2023-EJES-0002` | adopción digital | 10 |
| ENIF 2021 | `CALC-PISOS-ENIF2021-EJES-0003` | `ahorra_solo_informal` (D9) | 14 |
| ENIF 2021 | el mismo | `informal_cualquiera` | 14 |

Son 53 celdas construidas de 57 identidades objetivo. Las cuatro restantes
están dictaminadas `NO-CONSTRUIBLE`: formalidad × {sin seguridad social, con
seguridad social} para cada desenlace ENIF, porque no existe en ENIF 2021 un
`P3_13` comparable. No son fallas de montaje ni ausencias por soporte. Así, la
cobertura potencial de esta porción completa del árbitro es 53/57 = 92.98 %
con valor numérico y 57/57 = 100 % con dictamen. El 57 es el denominador
derivado de esta rejilla concreta; no se propone como denominador universal.

Cada celda construida tiene RESULT separados para punto, IC95, n sin ponderar,
denominador ponderado y réplicas válidas. Todos los IC tienen 10 000 réplicas
válidas. El IC expresa incertidumbre muestral en t−1; no es predicción de t ni
afirmación causal.

## Universos, códigos y diagnósticos

- ENVIPE: 37 614 delitos en el universo de evasión; `BP1_20` fuera de {1,2},
  incluidos blancos: 0. El universo de denuncia es 1 027 delitos con
  `BPCOD=01`, `BP2_1` válido y `BP1_20` válido. El join demográfico deja 0
  filas sin pareja. Como referencia, la denuncia ponderada es 0.6335238483
  entre no asegurados y 0.7740559546 entre asegurados.
- ENCIG: 123 186 filas de trámite; 20 934 integran el universo `N_TRA=01` con
  `P7_3` en {1,2,4,5,6}; se excluyen 122 respuestas restantes. El join persona
  es m:1 y deja 0 filas sin demografía.
- ENIF: 13 554 personas y 0 desenlaces indefinidos en ambos desenlaces. D9
  distingue ahorro informal y ausencia de cualquiera de las nueve vías de
  ahorro formal; el secundario mide cualquier ahorro informal. Por ejemplo,
  D9 es 0.2874266387 con cuenta y 0.4700404206 sin cuenta.

Los códigos se normalizan antes de filtrar. Edad es 18–29, 30–44, 45–59 y
60–96; escolaridad usa cuatro categorías propias de cada ola. En ENIF,
`TLOC` {1,2} significa 15 000 y más y {3,4}, menor de 15 000.

La evidencia documental de cuenta/débito está en
`data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001/spec.md`, §0.1:
el FD de 2021 identifica `P5_6_k` como tenencia de tarjeta de débito y
`P5_7_k` como ahorro en la cuenta. Por eso este piso usa `P5_4_1..9` para
tenencia de cuenta y `P5_7_1..9` para ahorro formal; no usa P5_6 como proxy de
cuenta. El input documental sellado `enif2021_fd_zip` tiene SHA-256
`6f4e3aab705ddb6910607be15aa711eca56ef5060dcc60bc941d201ef3079457`.

## Congelamiento, incertidumbre y sucesión

El snapshot de 57 identidades se congeló antes de abrir respuestas en
`forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv`; su fuente es
`forense/notas/2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv`, SHA-256
`7320bedbf8b7e5c7f5c6139063bea82c0b0bbdf0bd624a90b42600a59b558451`.
El snapshot no contiene resultados de la ola actual. Specs, sidecars y los
tres medidores autocontenidos se congelaron en COMMIT-1
`e2d8d1674a982a5e3333843fff810e37cf5c979f`.

Los medidores hacen bootstrap estratificado de UPM, 10 000 réplicas, PCG64 y
seed 42. Un plan se comparte entre celdas y desenlaces del instrumento; los
estratos con una UPM permanecen explícitos y las réplicas con denominador vacío
no se convierten automáticamente en números.

Linaje publicado:

- ENVIPE `0001 → 0002`.
- ENCIG `0001 → 0001-v1_1 → 0002`. El intermedio queda superado, no adoptado.
- ENIF `0001 → 0002 → 0003`.

La primera apertura de respuestas con ENIF `0002` reveló que su negación
formal alineaba por nombre columnas `P5_4_*` y `P5_7_*`, produciendo ceros
espurios. No se comprometieron ni publicaron esos resultados. Se preservó la
spec/código expuestos, se dejó `0002` como `NO-CORRIDA` y se creó `0003` como
sucesor/repetición con comparación posicional. `0003` es el único resultado
vigente. No se reescribió historia.

Los tres sucesores se publican `SELLADA`, `REPRODUCE/IDENTICO` y
`cuenta_gen2=PENDIENTE-DE-MESA`; esta entrega no decide SI/NO. Los cuatro CALC
vetados y `tools/pisos_ejes.py` conservan sus bytes. Frente a ellos, los
sucesores normalizan códigos, corrigen 60–96, escolaridad, localidad y cuenta,
restringen el universo ENCIG, añaden denuncia y ambos desenlaces ENIF, y emiten
RESULT numéricos por celda en vez de una tabla textual agregada.

## Controles

El control de conjuntos usa `(input_id, outcome)` como clave y compara las 57
identidades congeladas contra celdas emitidas más dictámenes; rechaza
duplicados, faltantes, sobrantes y categorías `nan`. Resultado dirigido: 0
fallos.

El control puntual independiente relee los ZIP sin importar los medidores.
Coincidieron exactamente, con delta absoluto 0, ENVIPE evasión/sexo=1, ENCIG
digital/sexo=1, ENIF D9/sexo=1 y ENIF informal-cualquiera/sexo=1. Evidencia:
`forense/evidencia-control-independiente-pisos-2026-09-19.json`, SHA-256
`7a0b642ea6bc4e82f28f5f59f46bf0f6efb2cf9af1aa0356b5cfc444a88ad96f`.

`spec-check` terminó 13/13 ENVIPE, 10/10 ENCIG y 31/31 ENIF. `verify` terminó
`REPRODUCE/IDENTICO` en las tres corridas. Las pruebas de `corrida0` pasan
94/94 y las pruebas estáticas de la rejilla, 0 fallos.

## Acceso y replay

El bloqueo era de montaje/configuración, no ausencia del corpus. Se dejó fuera
de Git `data/raw` enlazado al corpus compartido y `data/raices.local.yaml`; una
terminal nueva y un subproceso resuelven con hash `COINCIDE` ENVIPE, ENCIG,
ENIF, ENCRIGE y ENSANUT. No se copió microdato al repositorio ni se publican
rutas privadas.

Se conservaron las 41 verificaciones aisladas ya obtenidas: se publicaron las
38 `REPRODUCE/IDENTICO` autorizadas y DIN emisiones permanece
`NO-REPRODUCE/IDENTICO`. DIN conserva NC-0313 y la discrepancia
`G-R-EXISTE-AL-CERRAR`; no se degradan sus puntos/IC C2 por RESULT.

La nueva verificación concluyente reemplaza las dos limitaciones locales:
ENCRIGE corrupción reproduce 15/15 RESULT y 3/3 inputs; ENSANUT reproduce
28/28 y 2/2 inputs. Ambos tienen contexto idéntico y conservan sus sellos. Los
tres pisos nuevos también tienen asiento previo a publicación. Fuente cruda:
`forense/evidencia-replay-pisos-rejilla-2026-09-19.json`, SHA-256
`deb4f470feec4ac1854abc9d8b32017f5f1aaf67836c8e301dfba65c979be768`.
La fuente tabular queda en 121 asientos: 99 `REPRODUCE/IDENTICO`, uno
`NO-REPRODUCE/IDENTICO` y 21 veredictos/contextos distintos ya existentes.

El guardia se validó con un lote explícito de 44 CALC y luego se escribieron
`corridas.tsv`, `resultados.tsv` y `usos.tsv` mediante el generador. Una segunda
proyección dio cero líneas de diff: 211 corridas, 7 256 resultados y 208 usos.
Los 7 110 avisos son el baseline informativo de resultados/corridas sin
consumidor; no se silenciaron ni redefinieron.

## Mapa para consumo posterior

`forense/pisos-rejilla-entrega.tsv` es el mapa técnico: identidad fuente y
objetivo, unidad, eje/categoría, desenlace, estado/dictamen, CALC/corrida,
punto, IC, n, denominador, réplicas y consumidor previsto. Los tres prefijos
vigentes son:

- `RESULT-PISOS-ENVIPE2024-V2-*`
- `RESULT-PISOS-ENCIG2023-V2-*`
- `RESULT-PISOS-ENIF2021-V2-*`

`data/corrida0/usos.tsv` contiene cero usos de esos RESULT. Esto los deja listos
para que Claude haga la adopción, pero no la anticipa ni modifica marcador,
motor, mapa de adopción, crosswalk, θ o R.

## NO-CORRIDO / RESERVAS

- No se abrió ENVIPE 2025, ENCIG 2025 ni ENIF 2024 para recalibrar o comparar
  desempeño. Las únicas reaperturas adicionales fueron corridas históricas
  existentes ENCRIGE/ENSANUT para resolver replay.
- ENIF `0002` no tiene ejecución/resultados publicados; su defecto queda
  documentado y su sucesor es `0003`.
- Las cuatro celdas de formalidad no se imputan ni sustituyen por otro eje.
- `cuenta_gen2` de los tres sucesores queda `PENDIENTE-DE-MESA`.
- No hay adopción productiva ni decisión sobre el marcador en este PR.

## CONSUMIDO

- Microdatos autorizados: ENVIPE 2024, ENCIG 2023 y ENIF 2021, solo después de
  COMMIT-1.
- Documentación técnica y FD de esas mismas olas para universos/códigos.
- Para replay de corridas ya existentes: ENCRIGE 2020 y ENSANUT 2024.
- Snapshot de metadatos del árbitro, no sus valores/resultados actuales.
- Evidencia aislada de las 41 verificaciones previas, sin repetirlas por rutina.

Coordinación: el PR #868 debe permanecer abierto; su SHA remoto observado fue
`9e9e89225f0d986cf51b955940ebee7526809f1b`. No se tomó su commit mixto ni sus
cambios de motor/lector/mapa/usos. Las modificaciones pendientes del worktree
03 quedaron preservadas localmente en `8ac076d` y `f653869` antes de iniciar
esta rama.
