# GEN2-PISOS-REJILLA-CLI-1 · cierre para B y Claude

Fecha de verificación: 2026-09-19. Base de preparación:
`843a5f977e024ef5d74863e95856c763bee9e58d`; `main` integrado hasta
`33650571c509676657cc5da35a63aeea15da2297` (merge de #872). La rejilla íntegra y sus
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

La trazabilidad de escolaridad, antes implícita en cada medidor, queda
publicada por instrumento en
`forense/prereg-caja/PISOS-REJILLA-escolaridad-catalogos-v1_0.tsv` (SHA-256
`6f640d5d7b4b14d0a4ba2f719eae0bd28c55f65f6035e7990bbb020ae561695c`).
El extracto conserva miembro del ZIP, variable, código, texto literal del
catálogo y categoría de piso. ENVIPE 2024 y ENCIG 2023 usan `NIV`; ENIF 2021
usa `P3_1_1`. En los tres casos 0/00–2/02 → `hasta_primaria`, 3/03 →
`secundaria`, 4/04–7/07 → `media_superior` y 8/08–9/09 → `superior`; 99 y
blancos no se asignan. Esta adición es documental: no reabre respuestas ni
cambia un RESULT sellado.

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

La cobertura del código autocontenido está inventariada en
`forense/pisos-rejilla-congelamiento.tsv` (SHA-256
`d9fa8d7c4c7846b68885c2fe11051b1a70bd3e485224c6d541ebc92594bfa4e9`).
Los medidores publicados no importan un helper mutable: su `medidor.py` quedó
congelado antes de abrir/correr y el hash de ese mismo archivo figura dentro de
cada `sello.json`. ENIF `0002` se distingue deliberadamente: quedó congelado,
pero nunca se corrió ni selló; el hallazgo cambió la medición y por eso se
preparó `0003`, sin corregir `0002` en sitio.

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

El control de conjuntos compara las 57 identidades congeladas contra la
entrega por la tupla completa: `cell_id`, `input_id`, desenlace, instrumento,
edición y periodo fuente, instrumento, edición y periodo objetivo, unidad,
eje, categoría, estado, razón, consumidor y procedencia. Además rechaza
duplicados, faltantes, sobrantes y categorías `nan`; exige seis campos
numéricos en cada una de las 53 RESULT y ninguno en los cuatro dictámenes.
Resultado dirigido: 0 fallos. No es una validación por mero número de filas.
La evidencia compacta está en
`forense/evidencia-identidades-pisos-2026-09-19.json` (SHA-256
`34137072bcadeec6333f9e26019a73c03bdbd08b1e15c9fb69e288955e57f447`):
ambas proyecciones producen el mismo hash de identidad
`b3389121df71d4da24786664871bbab98b9390477efb20cb2b8faa2fcad08d9a`,
incluidos los cinco desenlaces y las unidades DELITO, TRAMITE y PERSONA
ELEGIDA 18+.

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
38 `REPRODUCE/IDENTICO` autorizadas y DIN emisiones permanece globalmente
`NO-REPRODUCE/IDENTICO`. No se fabrica un replay global exitoso: DIN conserva
NC-0313 y la discrepancia `G-R-EXISTE-AL-CERRAR`. A la vez, la evidencia
aislada registra delta 0 para los RESULT de punto/IC de C2 y la mesa firmó el
uso de C2; esa utilizabilidad por RESULT no cambia el veredicto del CALC
completo. La distinción está en
`forense/evidencia-replay-aislado-2026-09-19.json` y `data/corrida0/decisiones.tsv`.

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

Tras integrar #872 se ejecuta D3 solo mediante la capa posterior de decisiones:
`CALC-PISOS-ENCIG2023-EJES-0001` recibe `cuenta_gen2=NO` y deja de contar; la
evidencia y sucesión apuntan a `CALC-PISOS-ENCIG2023-EJES-0002`. No se tocó la
spec ni el sello antiguos. Los tres sucesores de esta entrega conservan
`PENDIENTE-DE-MESA`: que exista un piso no firma su adopción.
Con la cadena de sucesión visible se cierran `NC-0333` como MOOT —sin volver a
correr los cuatro pisos vetados— y `NC-0334` por publicación/rederivación. Se
conserva `NC-0336`: los briefs 01/02 incorporados aquí no se hacen pasar por el
archivo distinto `BRIEF-ASTRA-01-PISOS-REJILLA-2026-09-19.md` que #872 declaró
ausente.

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
`2d662e78b143f9b00a8e2b06fb7ff6cfe0ea15a1`, no `9e9e8922`. Sus artefactos
de pisos quedaron preservados de forma permanente fuera de `data/corrida0` en
`forense/historico/PR-868-2d662e78/artefactos-pisos.tar.gz` (SHA-256
`5640cb318c2f5b6d542a2796e2ab1914d80b984a43e2fdce39029827b1009c92`).
El mapa verificable de colisiones es
`forense/historico/PR-868-2d662e78/mapa-colisiones.tsv`: califica cada homónimo
por commit, ruta, corrida y hashes, sin mezclar resultados. En particular,
ENIF `0002` de #868 sí contiene resultados; ENIF `0002` de esta historia es
`NO-CORRIDA` y no los contiene. La candidatura de #871 es exclusivamente
ENVIPE `0002`, ENCIG `0002` y ENIF `0003` identificados en ese mapa. No se tomó
el commit mixto de #868 ni sus cambios de motor/lector/mapa/usos.

Los briefs 01 y 02 están incorporados con hashes y commits de ingreso en
`forense/encargos/fuentes/GEN2-PISOS-REJILLA-CLI-1/PROCEDENCIA.tsv` (SHA-256
`24b63962787e7e2616b53baf710d3b76f90ac1a9598c2261830e06d73c44cee2`).
`informal_cualquiera` ya forma parte de las 14 celdas ENIF publicadas en esta
entrega; no se vuelve a encargar.
