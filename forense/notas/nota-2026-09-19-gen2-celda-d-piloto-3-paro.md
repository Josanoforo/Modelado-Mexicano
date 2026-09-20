# ACTO GEN2-CELDA-D-PILOTO-3 · COMMIT-1 · cierre por hallazgo

**19/sep/2026 · NUBE `cloud_default`, Opus 5 · sin corpus montado, cero microdato, cero red de datos.**
Encargo archivado verbatim por 0-bis A.3 en `forense/encargos/2026-09-19-GEN2-CELDA-D-PILOTO-3.md`.
**Contadores movidos: cero.** No se congeló spec, no se congeló código, no se registró celda-D.

**Enmienda fechada (20/sep/2026, al fusionar `origin/main`):** `GEN2-C2-COMPUESTO-RESERVADAS-1` (`ADR-549`) fusionó primero y **emitió el C2 compuesto para este mismo par** — `c2-compuesto-dictamen-v1_0.tsv`: `edadxescolaridad` ENCIG 2025 sale `EMITIBLE`, 16 celdas, y la columna de piso del marcador pasa de `SIN-PISO` a `EMITIDA-SIN-EVALUAR`. El `estado` del par **sigue `RESERVADA`** y este acto sigue sin tocarlo; lo que cambia es que el piso a vencer ya existe, en un estado que el motor no puede leer como adoptado. Ese acto **no decide el cruce ni la elegibilidad** (cero menciones de coherencia o elegibilidad en su `spec.yaml`), así que el hallazgo de abajo queda intacto: lo que bloquea `edad × escolaridad` sigue siendo `PARO-COHERENCIA-UNIVERSO`, no el soporte, y sigue siendo de mesa. 

## 0 · Veredicto

`PARO-PREMISA` en dos puntos independientes, cada uno suficiente por sí solo para
que `COMMIT-1` no se congele hoy:

1. **P0, la compuerta de contenido declarada «antes que nada», no es ejecutable en
   este entorno** (`NO-VERIFICABLE-AQUÍ`, no `AUSENTE`): los tres cuestionarios y sus
   FD viven en `data/raw`, que no está montado, y la red de datos está caída.
2. **F1 apoya la enmienda en un diagnóstico que los dos CALC sellados que cita
   contradicen.** El bloqueo de `edad × escolaridad` no es el soporte, y por tanto
   enmendar la regla de soporte no lo levanta.

El segundo es el hallazgo del acto. El fondo sustantivo de F1 **es correcto y se
verifica aquí**; lo que no se sostiene es el instrumento de gobierno que invoca.

## 1 · Entorno y compuerta (ARRANQUE, Bloque D)

- `git rev-list --count HEAD..origin/main` → `0`. Base declarada por el encargo
  `6f365928`; base real al abrir `97a1fae`, **16 commits adelante** (`#885`, `#886`
  y su cascada). Re-derivado, no heredado; ninguna cifra de esta nota viene del SHA
  declarado.
- `python3 tools/entorno.py --sonda-red` → `acceso_corpus.montado = NO`
  (`archivos_examinados = 0`), `raices_logicas: data_raw configurada = NO`,
  `red = 000`, `numpy`/`pandas`/`scipy`/`pyreadstat` AUSENTES.
- **COMPUERTA: cumplida POR PRODUCTO**, no por `grep` de log.
  `git ls-tree -r --name-only origin/main` confirma los tres directorios con su
  `sello.json` y `sello.sha256`:
  `CALC-ENCIG2023-CRUCES-HISTORICOS-0002`, `CALC-ENCIG2021-CRUCES-HISTORICOS-0003`,
  `CALC-PISO-PERSISTENCIA-ERROR-0001`.
- **Duplicado (0.c): ninguno.** `git ls-remote --heads origin` → `main`,
  `censo/2026-09-19`, `claude/beautiful-fermi-mct15n`. Barrido de las tres ramas
  vivas: ninguna archiva este encargo (las tres coincidencias de `PILOTO-3` en `main`
  son los adjuntos del careo, no el encargo). PR abiertos: `0`.
- **A.3, adjuntos: los cuatro presentes**, con hash verificado en
  `forense/analisis/gen2-encig-cruces-historicos-cli-1/adjuntos/SHA256SUMS.md`:
  careo `796689c4dce6f43d…` y brief 03 `f48171b735534bb3…` coinciden con los que el
  encargo exige; Diseño A (`02-DISENO-A-…`) y Diseño B (`01-DISENO-ASTRA-…`) presentes.

## 2 · Verificación de existencia (A.8 / A.13)

| Comprobación del encargo | Resultado | Comando |
|---|---|---|
| celdas-D registradas | **5**, ninguna ENCIG | `ls data/curacion-registro/celdas-d` ; `\| grep -ic encig` → `0` |
| `PILOTO-3` fuera de `forense/encargos` | **7 archivos** (canon, INFRAESTRUCTURA, los 3 adjuntos, prereg, encargo hermano) — no `0` como declaraba el encargo, pero **ninguno es una celda-D ni una spec de este piloto**: `NO-ENCONTRADO` se sostiene para el objeto, no para el token | `git grep -l "PILOTO-3" \| grep -v "^forense/encargos"` |
| marcador: `edad × escolaridad` ENCIG 2025 | **`RESERVADA`** (`CRUCE-GRUPO::…::edadxescolaridad`, `16 celdas agrupadas`, `SIN-PISO`, `RESERVADA-SIN-R`) — confirmado | `grep … data/corrida0/marcador-segmento.tsv` |
| `edad × escolaridad` sobre derivados `encig25*` | **0**, sobre **2** archivos rastreados cuyo nombre casa `encig25\|encig2025` (A.13: el barrido completo examinó **5 926** archivos rastreados) | `git ls-files \| grep -iE "encig25\|encig2025" \| xargs grep -ilE …` |
| ningún piloto previo tocó ENCIG | confirmado (pilotos 1 y 2: ENIF y ENVIPE) | — |

## 3 · P0 · Compuerta de contenido: `NO-VERIFICABLE-AQUÍ`

P0 pide leer, de los cuestionarios y FD de 2021, 2023 y 2025, la **redacción del
reactivo, las opciones y códigos de `P7_3`, el filtro `N_TRA`, el flujo que lleva a
la pregunta y el catálogo de trámites**.

**Alcanzabilidad de los tres payloads (A.13):**

| id de manifiesto | archivo | estado en esta sesión |
|---|---|---|
| `encig2021_cuestionario_pdf` | `encig21_cuestionario.pdf` | **NO-ALCANZABLE** |
| `encig23_cuestionario_pdf` | `encig23_cuestionario.pdf` | **NO-ALCANZABLE** |
| `encig25_cuestionario_pdf` | `gen2_corrupcion_fuente_general/encig25_cuestionario.pdf` | **NO-ALCANZABLE** |

Causa única: `data/raw` no existe y `data/raices.local.yaml` tampoco; la sonda de red
da `000`. **No es `AUSENTE-EN-RAIZ`**: el último censo disponible
(`forense/censo-raiz/2026-09-18.txt`, «Total en disco: 551 · nuevos: 89») escanea la
raíz `descargas_mx` y no lista ninguno de los tres, pero tampoco lista
`encig21_cuestionario`/`encig23_cuestionario`, que el repo sí acredita descargados —
es decir, el censo no cubre la raíz donde viven. Un negativo de un comando que examinó
**0** de esos archivos no es un negativo (A.13): el rótulo correcto es
`NO-VERIFICABLE-AQUÍ`, y la pregunta queda como pregunta.

**Lo que sí se agotó del universo alcanzable, y por qué no basta.**

- **2021 ↔ 2023: ya acreditado y sellado.** `04-nota-resultados.md` (§ «Comparabilidad
  y 2021») declara que «Cuestionario y descriptor acreditan el mismo reactivo P7.3,
  códigos, tipo de trámite, ponderador y categorías demográficas». Ese lado de P0 no
  hace falta re-abrirlo.
- **2023 ↔ 2025: es el lado que P0 existe para cerrar, y no hay cita de texto.** La
  única lectura del instrumento 2025 que el repo tiene
  (`forense/notas/2026-09-10-GEN2-CORRUPCION-FUENTE-GENERAL-investigacion.md` §3.1)
  transcribe el reactivo **8.3** (corrupción) y dice de paso que «`P7_3` registra el
  canal de cada evento `(ID_TRA,NT_TIPO)`», con universo 18+ urbano de 100 mil y más,
  trietápico, 46 mil viviendas. **No transcribe la redacción de `P7_3`, sus opciones,
  el filtro `N_TRA`, el flujo ni el catálogo de trámites.**
- **Evidencia estructural concordante, declarada y NO dispositiva.**
  `tools/medidor_gobierno_digital_encig25.py:12-14,36` — código ya corrido sobre el
  microdato 2025 — usa exactamente el mismo contrato que las specs de 2021 y 2023:
  universo `N_TRA=='01'`, `adopta = P7_3 ∈ {4,5}`, `no adopta = {1,2,6}`, teléfono
  `{3}` fuera, ponderador `FAC_TRA`, diseño `EST_DIS × UPM_DIS`. Es decir, **la columna
  y su conjunto de códigos sobreviven a 2025**.
- **Por qué eso no cierra P0.** A.15 manda leer el texto del reactivo, no inferirlo de
  la columna; y el propio `forense/hallazgos.md` del **19/sep/2026** (`ACTO
  GEN2-FAM-UNION-ESTIMANDO-1`, `ADR-546`) acaba de documentar el caso en que códigos,
  cifras y `verify` coincidían y aun así la regla medía **otro estimando** —«la única
  señal disponible era leer el texto de la pregunta de los dos instrumentos». Cerrar
  P0 por igualdad de códigos sería cometer, el mismo día, el defecto que ese hallazgo
  acaba de asentar.

**Consecuencia:** el `+11 pp` de `CALC-PISO-PERSISTENCIA-ERROR-0001` sigue sin poder
atribuirse a adopción digital ni a cambio de instrumento. **No se re-rotula** el error
de persistencia de ENCIG como `NO-COMPARABLE` — eso sólo procede si se acredita que el
instrumento cambió, y aquí no se acreditó ni lo uno ni lo otro. Sucesor en caja, donde
los PDF son legibles.

## 4 · F1 · El diagnóstico que los CALC sellados contradicen

F1 razona así: la regla congelada exige `n ≥ 200` **en todas** las celdas;
`edad × escolaridad` falla en **una de 16**; la casa tolera hasta ⅓; luego la regla de
dirección fue «más estricta que la casa, por error de redacción», y la enmienda
levanta el bloqueo.

**Las dos primeras premisas son ciertas. La conclusión no se sigue.**

`forense/analisis/gen2-encig-cruces-historicos-cli-1/03-controles.tsv`, derivado de los
dos CALC sellados que el encargo declara como compuerta:

| ola | cruce | min_n | coherencia | **elegible** | puntaje | celdas IC δ ≠ 0 |
|---|---|---:|---|---|---:|---:|
| 2023 | SEXO-EDAD | 1 644 | `PARO-COHERENCIA-UNIVERSO` | SI | 0.7945 | 0 |
| 2023 | SEXO-ESCOLARIDAD | 1 239 | `COHERENTE` | SI | 0.8708 | 1 |
| 2023 | EDAD-ESCOLARIDAD | **70** | `PARO-COHERENCIA-UNIVERSO` | **NO** | 2.1535 | 7 |
| 2021 | SEXO-EDAD | 1 614 | `PARO-COHERENCIA-UNIVERSO` | SI | 1.0004 | 1 |
| 2021 | SEXO-ESCOLARIDAD | 1 362 | `COHERENTE` | SI | 0.6653 | 0 |
| 2021 | EDAD-ESCOLARIDAD | **110** | `PARO-COHERENCIA-UNIVERSO` | **NO** | 1.6001 | 4 |

**(a) El bloqueo no es el soporte; es la coherencia de universo.**
`edad × escolaridad` sale `elegible = NO` en **las dos olas** por
`PARO-COHERENCIA-UNIVERSO`: el cruce sólo reconstruye los marginales sellados si se
añade un residuo de **107 trámites (masa ponderada 571 754)** en 2023 y **104
(672 707)** en 2021, cuya edad cae fuera de la rejilla efectiva 18–96
(`04-nota-resultados.md`). La regla congelada, en palabras de la propia nota, «exige
parar esos cruces y pedir una definición; no autoriza convertir 97/98/99 en 60+,
eliminar el residuo ni comparar puntajes sobre universos distintos». **Relajar
`n ≥ 200` a la tolerancia de ⅓ de la casa deja ese `PARO` intacto**: son dos reglas
distintas y F1 enmienda la que no bloquea.

**(b) No hay «dos candidatos empatados en todos sus desempates».**
`sexo × edad` **también** carga `PARO-COHERENCIA-UNIVERSO` (mismo residuo de edad), de
modo que el único cruce `COHERENTE` en ambas olas es `sexo × escolaridad`. Y aun
tomando sólo el desempate que el careo congeló — «se elige el de mayor razón
señal/ruido de δ₂₃ (media de |δ|/EE)» entre los cruces con **todas** las celdas
`n₂₀₂₃ ≥ 200` (`04-CAREO-PILOTO-3-direccion-2026-09-19.md` §4(2)) — el orden es
**0.8708 > 0.7945**: ganador único, `sexo × escolaridad`, con 1 de 8 celdas con IC de δ
que excluye 0, así que tampoco se dispara la cláusula «si ninguno tiene una sola celda…
no hay piloto». La «alternativa a la letra» que el encargo ofrece como concesión a
mesa **es**, de hecho, lo que la regla congelada arroja por sí sola.

**(c) El estado sellado no es «empate»: es una pregunta abierta a mesa.**
El RESULT del acto de compuerta es `SELECCION-PENDIENTE-DE-DEFINICION`, y lo que está
pendiente es precisamente **la definición de mesa sobre la coherencia de la rejilla de
edad**. F1 no la resuelve ni la menciona; sustituye esa definición por una enmienda a
otra regla. Además, la nota sellada ya había dictaminado ex ante el uso de las cifras
que F1 invoca: «Los puntajes de cruces en PARA se publican como diagnóstico pero no
ordenan candidatos. Que siete celdas de `edad×escolaridad` tengan IC puntual que
excluye cero **no rescata una rejilla no elegible** ni constituye evidencia
confirmatoria independiente después de seleccionar entre celdas y cruces.»

**(d) Lo que F1 sí acierta, verificado aquí y no en disputa.** Re-derivado de
`tabla-celdas-2021.tsv` y `tabla-celdas-2023.tsv` (lectura de resultados sellados; cero
microdato):

- **Una sola celda de 16** incumple `n ≥ 200`, y la incumple en las dos olas:
  `18–29 × HASTA-PRIMARIA` (n = 110 en 2021, 70 en 2023). Las otras 15 van de 391 a
  3 147. La lectura de soporte del encargo es exacta.
- **13 de 16 celdas conservan el signo de δ entre olas.** Las tres que lo cambian
  (`30-44 × HASTA-PRIMARIA`, `30-44 × SUPERIOR`, `45-59 × SUPERIOR`) lo hacen con |δ|
  pequeño (≤ 0.0975).
- La celda que el módulo de auditoría señala, **`60+ × hasta primaria`**, es en efecto
  la de mayor δ positivo en ambas olas (0.2951 en 2021, 0.3247 en 2023) y está bien
  soportada (n = 1 433 / 1 408). El módulo de auditoría del encargo se sostiene.

Dicho sin rodeos: **hay una interacción y es estable; el problema es que la rejilla que
la contiene está parada por otra causa, y esa causa la tiene que levantar mesa, no una
enmienda a la regla de soporte.**

## 5 · Qué necesita mesa para desbloquear (y qué no decide este acto)

Ninguna de estas opciones se elige aquí; se enumeran para que la firma sea informada.

1. **Definir la rejilla de edad** (lo que el acto sellado pidió): qué se hace con los
   97/98/99 y el residuo de 107/104 trámites. Si mesa define, `edad × escolaridad`
   puede volverse elegible **y entonces** la enmienda de soporte de F1 pasa a ser
   necesaria y suficiente — en ese orden, no al revés.
2. **Correr a la letra**: `sexo × escolaridad`, 8 celdas, `COHERENTE` en ambas olas,
   poder bajo declarado. No requiere ninguna enmienda.
3. **Declarar el piloto 3 sin poder de falsación** y dejar el compuesto como está.

En los tres casos, **P0 sigue siendo previo**: se resuelve en caja, con los PDF a la
vista, antes de congelar nada.

## 6 · Auditoría (afirma sobre México)

Se hereda completo el módulo del encargo y no se debilita: `edad × escolaridad` en
gobierno digital es, antes que actitud hacia el Estado, **brecha de acceso,
conectividad y alfabetización digital por cohorte**; el universo son trámites
realizados y excluye a quien no tuvo contacto con el Estado —más rural, más informal—;
la celda sin soporte (jóvenes con primaria o menos) es escasa **porque la cobertura
escolar subió**: su ausencia es estructura, no dato faltante. Evidencia clase (a).
Esta nota no publica ninguna cifra de ENCIG 2025 y no abre la ola reservada.

Lo peligroso leído simplista sigue siendo `«+11 pp» = «los mexicanos ya confían en el
gobierno digital»`, y esta nota **agrega** un segundo riesgo del mismo tipo: leer el
`13 de 16` como si ya autorizara el cruce. Autoriza a insistir con mesa; no autoriza a
congelar.
