# ACTO GEN2-CELDA-D-PILOTO-3-P0 · cierre por premisa de entorno

**20/sep/2026 · NUBE `cloud_default`, Opus 5 · sin corpus montado, cero microdato, red de datos denegada por política.**
Encargo archivado verbatim por 0-bis A.3 en `forense/encargos/2026-09-20-GEN2-CELDA-D-PILOTO-3-P0.md`.
**Contadores movidos: cero.** No se congeló spec, no se congeló código, no se registró celda-D, no se emitió cruce.

## 0 · Veredicto

`PARO-PREMISA`, por **una** razón, distinta de las dos de #894:

> **La cabecera declara `ENTORNO: CAJA (corpus montado)`. El entorno real es `cloud_default`, sin corpus y con la red de datos denegada en la compuerta.** Esa declaración es la premisa sobre la que descansa el encargo entero — «EN CAJA» está en el título — y no se sostiene. P0 vuelve a ser `NO-VERIFICABLE-AQUÍ`.

Lo importante es lo que **no** falló esta vez. El defecto de gobierno que fue el
entregable de #894 **está corregido**: `F1-bis` nombra la causa correcta
(`PARO-COHERENCIA-UNIVERSO`, la rejilla de edad) en vez de la incorrecta (el soporte),
y por tanto **sí** es el instrumento capaz de levantar el bloqueo. `F1-bis` y `F3`
vienen por texto en el archivo, selladas por el lanzamiento, y se asientan aquí como
definiciones de mesa vigentes. **`FP-389` queda firmada por `F1-bis`** — lo que sigue
abierto no es la definición, sino su ejecución, que gatea `NC-0355` (P0 en caja).

`P2` no corre (gateado por P0, que no pasó). `P3` no dispara (P0 no «no pasa»: queda
sin determinar, que no es lo mismo — A.13).

## 1 · Entorno, re-derivado (no heredado)

El encargo declara SHA de redacción `4dedab48` y manda re-derivar.

| Comprobación | Comando | Resultado |
|---|---|---|
| base contra `origin/main` | `git rev-list --count HEAD..origin/main` | **4** al abrir (tras `git fetch`, `origin/main` recibió *forced update* `ce16af3` → `a92126f`, PR #901). `origin/main..HEAD` → `0`. |
| rama | — | `claude/lucid-lamport-32k9t3`, `git_status` **LIMPIO** (0 líneas) |
| entorno | `python3 tools/entorno.py --sonda-red` | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = **`cloud_default`** |
| corpus | *ídem* | `acceso_corpus.montado` = **NO**, `archivos_examinados = 0`; nota del propio script: «`data/raw` ausente — normal en un clon fresco / en la nube» |
| raíces lógicas | *ídem* | `data_raw` **configurada = NO**; `data/raices.local.yaml` **no existe** (gitignorado, `.gitignore:7`) |
| red | *ídem* | `http_code` = **`000`** contra `https://www.inegi.org.mx/` |
| materiales | *ídem* | `numpy`, `pandas`, `scipy`, `pyreadstat` **AUSENTES**; `yaml 6.0.1`; Python 3.11.15 |

El SHA `4dedab48` que la cabecera declara **existe** en el árbol (`4dedab4`, merge del
PR #898) pero **no** es la base de esta sesión: HEAD abrió en `fef26af`. Ninguna cifra
de esta nota viene del SHA declarado.

## 2 · Compuerta: **cumplida**, verificada POR PRODUCTO

`git ls-tree -r --name-only origin/main`:

- **#894** — `forense/notas/nota-2026-09-19-gen2-celda-d-piloto-3-paro.md` → presente.
- **#889** — `data/corrida0/CALC-C2-COMPUESTO-RESERVADAS-0001/` → presente con
  `sello.json` y `sello.sha256`, más `ejecucion.json`, `medidor.py`, `resultados.json`.

Los dos CALC de cruces que el acto anterior declaró compuerta siguen en su sitio
(`CALC-ENCIG2023-CRUCES-HISTORICOS-0002`, `CALC-ENCIG2021-CRUCES-HISTORICOS-0003`).

## 3 · P0 · `NO-VERIFICABLE-AQUÍ` — las tres rutas, agotadas

P0 pide leer texto de tres PDF. Las tres vías de alcanzarlos se probaron y se cerraron:

| Ruta | Prueba | Resultado |
|---|---|---|
| **Disco (`data_raw`)** | `ls data/raw` | `No such file or directory`; `.gitignore:5-6` lo excluye por diseño (el payload nunca se commitea) |
| **Raíces declaradas** | `ls data/raices*.yaml` | ausente; `raices_logicas: data_raw configurada = NO`; `MODELADO_RAICES = sin_variable` |
| **Red** | `curl -sI … /encig/2021/doc/encig21_cuestionario.pdf` | **`HTTP/1.1 403 Forbidden`** |

**El 403 es nuevo respecto de #894 y vale registrarlo con precisión**, porque cambia el
rótulo de la causa. #894 escribió «la red de datos está caída» (`000`). Aquí el `000`
del script es un artefacto de que `curl` sin proxy no sale; la causa real se lee en la
compuerta del entorno, `curl -sS "$HTTPS_PROXY/__agentproxy/status"`:

```
"recentRelayFailures": [
  { "kind": "connect_rejected",
    "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
    "host": "www.inegi.org.mx:443" }, …
]
```

No es una red caída ni un fallo transitorio que reintentar: `inegi.org.mx` **no está en
la política de salida de este entorno**. La adquisición programática de los tres
payloads —que habría sido la salida legítima, porque los tres traen `sha256` sellado en
`data/manifiesto.yaml` y admitirían verificación A.1 de tres estados— **queda cerrada
por política, no por error**. Tampoco hay extractor de PDF (`pdftotext`, `pypdf`,
`pymupdf`: los tres ausentes), de modo que la ruta sigue cerrada aguas abajo aunque el
payload apareciera.

Los tres ids y su estado, como en #894 y por la misma causa única:

| id de manifiesto | archivo declarado | estado |
|---|---|---|
| `encig2021_cuestionario_pdf` | `encig21_cuestionario.pdf` (`sha256 9ee82981…`) | **NO-ALCANZABLE** |
| `encig23_cuestionario_pdf` | `encig23_cuestionario.pdf` | **NO-ALCANZABLE** |
| `encig25_cuestionario_pdf` | `gen2_corrupcion_fuente_general/encig25_cuestionario.pdf` (`sha256 807196d6…`) | **NO-ALCANZABLE** |

**Consecuencia, sin cambios:** el `+11 pp` de `CALC-PISO-PERSISTENCIA-ERROR-0001` sigue
sin atribución entre adopción digital real y cambio de instrumento. **No se re-rotula**
el error de persistencia de ENCIG como `NO-COMPARABLE`: eso sólo procede si se acredita
que el instrumento cambió, y aquí no se acreditó ni lo uno ni lo otro.

## 4 · P1 · Lo que sí se acredita sin payload, y lo que no

P1 pide dos cosas. Una es citable desde lo sellado; la otra no.

**(a) Citable — la rejilla, y por qué 97+ cae fuera.** No hacía falta el PDF para fijar
la rejilla: **está congelada en las dos specs selladas, y es idéntica en ambas olas**.

- `data/corrida0/CALC-ENCIG2023-CRUCES-HISTORICOS-0002/spec.yaml:32,37`
- `data/corrida0/CALC-ENCIG2021-CRUCES-HISTORICOS-0003/spec.yaml:31,36`

ambas, palabra por palabra:

```
transformacion: "Evento P7_3 en {4,5}; edad 18-29/30-44/45-59/60-96; NIV agregado …"
  edad: ["18-29", "30-44", "45-59", "60-96"]
```

La banda superior **cierra en 96**. Ése es el hecho estructural que hace que `97`, `98`
y `99` queden fuera del universo del cruce: no es una regla aparte ni una omisión, es el
borde de la cuarta banda tal como se congeló. La descripción de `F1-bis` —«los trámites
cuya edad cae fuera de las cuatro bandas (códigos de no especificado y 97+)»— **describe
correctamente el objeto sellado**.

**(b) Citable — el conteo**, como el encargo manda (citar, no re-medir), de
`03-controles.tsv`:

| ola | cruce | `n_completos` | residuo (eje edad) | masa ponderada |
|---|---|---:|---:|---:|
| 2023 | EDAD-ESCOLARIDAD | 20 827 | **107** | 571 754 |
| 2021 | EDAD-ESCOLARIDAD | 21 048 | **104** | 672 707 |

**(c) NO citable — el significado por texto.** Qué significa cada uno de `97`, `98` y
`99` **en cada ola** (¿97 = «97 y más»? ¿98 = «no sabe»? ¿99 = «no especificado»? ¿es la
misma asignación en 2021, 2023 y 2025?) exige el descriptor de archivo / FD, que es
payload. **El árbol no lo contiene.** La nota sellada sólo acredita el hecho negativo de
que la regla congelada «no autoriza convertir 97/98/99 en 60+». Distinguir «97+ es edad
real censurada» de «98/99 son no-respuesta» **importa**, y no de forma menor: si parte
del residuo es edad real, `F1-bis` lo está expulsando del universo; si es no-respuesta,
lo está tratando como corresponde. **Esa pregunta queda abierta y es la primera que debe
cerrar la sesión en caja.**

## 5 · `F1-bis` y `F3` · asentadas, bien fundadas, no ejecutadas

**`F1-bis` está bien fundada** — es exactamente lo que #894 pidió y lo que `FP-389`
dejó pendiente. Nombra `PARO-COHERENCIA-UNIVERSO` (la causa real), no el soporte (la
causa que F1 nombraba mal), y opera sobre las dos reglas en el orden correcto: primero
define el universo, y **sólo entonces** la tolerancia de ⅓ pasa a ser pertinente. Ese
orden —«si mesa define, la enmienda de soporte pasa a ser necesaria y suficiente, en ese
orden, no al revés»— es literalmente el camino (1) que #894 §5 enumeró.

**`F3` se asienta y ya está en vigor de hecho**: Codex salió del programa, `F2` del
encargo anterior queda sin objeto, y la separación pasa a ser entre sesiones de Claude.
Este acto no congela ningún COMMIT-1, así que no consume `F3`; la deja escrita para el
sucesor.

**Un apunte para quien ejecute P2, que este acto NO ejecuta.** P2 exige re-aplicar la
regla de elección *«sobre los RESULT ya sellados (sin abrir dato)»*. Esa condición
**parece satisfacible, y conviene que el sucesor lo verifique antes de comprometerse**:
`03-controles.tsv` ya trae `n_completos` —el universo **sin** el residuo, que es
precisamente el universo de `F1-bis`— junto al residuo desglosado por eje
(`residuo_n_a`/`residuo_n_b`). Es decir, el insumo que `F1-bis` define ya está sellado y
no hay que re-medirlo.

Se deja dicho como **bandera, no como resultado**, y deliberadamente **no se nombra
ningún cruce ni se ordena ningún puntaje**: la elección depende también de la tolerancia
de ⅓ y de la condición de no-piloto, que son P2, y P2 está gateado por P0. El encargo
dice «no te digo cuál sale»; esta nota tampoco.

## 6 · Por qué no disparan P2 ni P3

- **P2** — condición: «Si P0 pasa **y** `F1-bis` viene firmada». `F1-bis` viene firmada;
  **P0 no pasó**. Falla la conjunción. Cero archivos del perímetro sustantivo escritos:
  ninguna spec en `forense/prereg-caja/`, ningún `CALC-GOB-DIGITAL-*-EMISIONES-0001/`,
  ningún `tests/test_piloto3_guardias.py`, ninguna celda-D.
- **P3** — condición: «Si P0 **no pasa**». P0 no falló: quedó **sin determinar**.
  Confundir `NO-VERIFICABLE-AQUÍ` con un veredicto negativo es exactamente el error que
  A.13 prohíbe, y dispararía la consecuencia más cara del encargo — re-rotular el error
  de persistencia como `NO-COMPARABLE` y declarar «no hay piloto» — **sobre un comando
  que examinó cero archivos**. No se dispara.

**No se abren NC nuevas.** `NC-0355` (P0 en caja) y `NC-0356` (piezas de COMMIT-1) ya
cubren exactamente estas dos ausencias, están **ABIERTAS**, y su sucesor declarado
—acto en caja con corpus montado— no cambia. Este acto las **re-confirma**; duplicarlas
inflaría el registro sin añadir información.

## 7 · Handoff para la sesión en caja

Para que el sucesor cierre en una sola pasada, con todo lo payload-independiente ya
resuelto aquí:

1. **Verificar los tres payloads por A.1** contra `data/manifiesto.yaml`
   (`encig2021_cuestionario_pdf`, `encig23_cuestionario_pdf`, `encig25_cuestionario_pdf`;
   ojo: el de 2025 vive bajo `gen2_corrupcion_fuente_general/`).
2. **P1 primero, no P0** — el significado de `97/98/99` por ola (§4c) condiciona la
   lectura de `F1-bis`, y es más barato que P0.
3. **P0**: transcribir reactivo 7.3, opciones y códigos, filtro `N_TRA`, flujo y
   catálogo, en tabla de tres columnas. **No cerrar por igualdad de códigos** — el
   contrato del medidor 2025 (`tools/medidor_gobierno_digital_encig25.py:12-14,36`) ya
   concuerda con 2021/2023 y aun así no basta: A.15 manda leer el texto, y `ADR-546`
   (19/sep) documenta el caso en que códigos y cifras coincidían midiendo otro estimando.
4. **P2** sólo si P0 sale `MISMO-INSTRUMENTO` o `CAMBIO-MENOR`; con la bandera de §5.
5. **`F3`**: quien congele COMMIT-1 no corre COMMIT-2/3.

## 8 · Auditoría (afirma sobre México)

Se hereda el módulo del encargo, sin debilitarlo y sin cifra nueva. Esta nota **no
publica ninguna cifra de ENCIG 2025** y no abre la ola reservada; el par
`edadxescolaridad` sigue `RESERVADA` en el marcador, intacto.

El riesgo central es el que el encargo nombra: **un salto uniforme de once puntos en
todas las celdas es sospechoso de instrumento antes que de conducta**, y hasta que P0
cierre ningún artefacto del programa puede citar el `+11 pp` como adopción digital. Si
resultara real, sería cambio de nivel **entre quienes hicieron trámites** —población con
contacto institucional, más urbana y más formal—, no confianza en el Estado. Edad y
escolaridad son marcadores de cohorte y acceso, no de actitud.

Esta nota agrega un riesgo propio, de §4: **tratar la rejilla `18–96` como si fuera una
descripción de la población**. No lo es; es un borde de codificación. Los 107 y 104
trámites del residuo son un objeto cuyo contenido sustantivo —edad censurada o
no-respuesta— **todavía no se ha leído**, y `F1-bis` los expulsa del universo *antes* de
que nadie lo sepa. La definición es correcta como regla de gobierno y sigue siendo lo
que desbloquea el piloto; pero su justificación sustantiva depende de §4c, que está
pendiente. Evidencia clase (a).

---

# ENMIENDA POR ADENDA DE MESA · 20/sep/2026

Mesa lanzó una adenda a este mismo encargo. Sella el PARO y los dos juicios de §6 (no
duplicar NC, no disparar P3), y **reordena una compuerta**: `P0` deja de gatear el
`COMMIT-1` y pasa a gatear el `COMMIT-2`. Congelar spec y código no abre microdato, así
que no depende de `P0`. Con eso, y con `F1-bis` firmada, `P2` **sí corre**.

## E.1 · Reorden de compuertas (adenda 2)

`NC-0356` queda enmendada por fecha en `forense/no-corrido.tsv`: su sucesor pasa a decir
que el `COMMIT-1` está desbloqueado y se congela en este acto, y que si `P0` en caja
resulta `CAMBIO-DE-INSTRUMENTO` **la spec se retira sin correr** (`SUPERADO`,
`n_resultados = 0`). **`NC-0355` sigue ABIERTA y gatea toda apertura de dato.** El texto
original de 19/sep se conserva íntegro en el mismo campo, marcado como superado.

## E.2 · `P2(a)(b)` · La restricción, medida en vez de asumida

Mesa tenía razón en que mi observación de §5 estaba incompleta: `n_completos` da el
universo, no los marginales ni el EE. El procedimiento de la adenda (3a–3b) se ejecutó
íntegro, **sin abrir dato**, y es reproducible con un comando:

```
python3 forense/notas/2026-09-20-p2-seleccion-f1bis.py
```

| ola | cruce | celdas | `DEN-W` total | `p_all` | peor cociente |
|---|---|---:|---:|---:|---:|
| 2021 | SEXO-EDAD | 8 | 107 478 297.0 | 0.572960 | **0.000e+00** |
| 2021 | SEXO-ESCOLARIDAD | 8 | 108 151 004.0 | 0.573227 | **0.000e+00** |
| 2021 | EDAD-ESCOLARIDAD | 16 | 107 478 297.0 | 0.572960 | **0.000e+00** |
| 2023 | SEXO-EDAD | 8 | 107 107 269.0 | 0.559957 | **0.000e+00** |
| 2023 | SEXO-ESCOLARIDAD | 8 | 107 679 023.0 | 0.560382 | **0.000e+00** |
| 2023 | EDAD-ESCOLARIDAD | 16 | 107 107 269.0 | 0.559957 | **0.000e+00** |

El cociente `|δ_F1bis − δ_sellado| / EE_sellado` es **exactamente 0 en las 48 celdas**,
no meramente `< 0.10`. **La razón es estructural y conviene asentarla con precisión,
porque corrige el supuesto sobre el que la adenda construyó su umbral:** el script
congelado de los dos CALC define los cuatro marginales sobre el mismo filtro de casos
completos —

```
complete = frame[axis_a].notna() & frame[axis_b].notna()
a = complete & frame[axis_a].eq(category_a)  ;  all_common = complete
```

`tools/encig_cruces_historicos.py:381-387`. El residuo de edad **nunca entró en
`p_ab`, `p_a`, `p_b` ni `p_all`**. Es decir: **los `δ`, `EE` e `IC` sellados ya estaban
calculados sobre el universo de `F1-bis`**. No son una «aproximación declarada» como la
adenda 3c preveía — **son exactos sobre ese universo**, y la condición del umbral se
satisface trivialmente porque no había nada que aproximar.

**Qué era entonces el `PARO-COHERENCIA-UNIVERSO`.** No era que `δ` usara el universo
equivocado. Es la bandera `RESIDUO-OTRO-EJE`: la rejilla no puede reconstruir los
**marginales sellados del CALC de pisos** —calculados sobre el universo completo,
residuo incluido— porque le falta ese residuo. `F1-bis` manda verificar la coherencia
contra los marginales **recalculados sobre el universo del cruce**, no contra los
sellados con otro denominador; con esa definición la causa se disuelve por construcción.
Verificado además que **ninguna** de las seis combinaciones dispara la otra causa posible
(`NO-REPRODUCE-PISO`): la única causa sellada en las seis es `RESIDUO-OTRO-EJE`.

## E.3 · `P2(c)` · Regla completa y cruce elegido

| ola | cruce | celdas `n<200` | frac | ≤ ⅓ | elegible | puntaje | celdas IC δ ≠ 0 | coherencia F1-bis |
|---|---|---:|---:|:--:|:--:|---:|---:|---|
| 2021 | EDAD-ESCOLARIDAD | 1 / 16 | 0.062 | SI | **SI** | 1.6001 | 4 | COHERENTE |
| 2021 | SEXO-EDAD | 0 / 8 | 0.000 | SI | SI | 1.0004 | 1 | COHERENTE |
| 2021 | SEXO-ESCOLARIDAD | 0 / 8 | 0.000 | SI | SI | 0.6653 | 0 | COHERENTE |
| 2023 | EDAD-ESCOLARIDAD | 1 / 16 | 0.062 | SI | **SI** | 2.1535 | 7 | COHERENTE |
| 2023 | SEXO-EDAD | 0 / 8 | 0.000 | SI | SI | 0.7945 | 0 | COHERENTE |
| 2023 | SEXO-ESCOLARIDAD | 0 / 8 | 0.000 | SI | SI | 0.8708 | 1 | COHERENTE |

Desempate congelado del careo (§4(2), «mayor media `|δ|/EE`» sobre `δ₂₃`, entre los
elegibles en ambas olas): **2.1535 > 0.8708 > 0.7945**.

> **CRUCE ELEGIDO: `edad × escolaridad`.** 15 celdas `PUNTUADA`; `18–29 × HASTA-PRIMARIA`
> queda **`FUERA-DE-SOPORTE` declarada ex ante** (n = 110 en 2021, 70 en 2023, única celda
> bajo `n ≥ 200` y en las dos olas). La **condición de no-piloto no dispara**: el ganador
> tiene 7 celdas con IC95 de δ que excluye 0.

**Una ambigüedad de `F1-bis` que se midió en vez de resolverse a dedo.** `F1-bis` declara
las celdas sin soporte `FUERA-DE-SOPORTE` ex ante pero no dice si entran en el puntaje.
Importa en principio —un cruce no debería ganar por la fuerza de una celda declarada
inutilizable— así que se calcularon **las dos lecturas**: con las 16 celdas, 2.1535; con
las 15 con soporte, 2.2142. **El orden y el ganador son idénticos en ambas** y el margen
es de más del doble sobre el segundo, así que la ambigüedad **no es dispositiva aquí** y
no se resuelve por este acto: queda señalada para que mesa la cierre cuando importe.

**Convergencia con el encargo del 19/sep, que vale la pena hacer explícita.** La `F1`
original ya proponía «`edad × escolaridad`, 15 celdas puntuables, `18–29 × hasta primaria`
`FUERA-DE-SOPORTE` ex ante». Es **exactamente** lo que la regla arroja sola bajo `F1-bis`.
La intuición de dirección era correcta; lo que estaba mal fundado era el instrumento que
invocaba (`ADR-551`). Con la rejilla definida, la regla la alcanza sin ayuda.

**Límite declarado, heredado de la nota sellada y no debilitado:** las 7 celdas con IC que
excluye 0 se usan aquí **sólo** para verificar que la condición de no-piloto no dispara.
**No** constituyen evidencia confirmatoria independiente, porque se leen después de
seleccionar entre celdas y entre cruces. Ese límite viaja a la spec.

## E.4 · `λ`, derivada y congelada

`Sλ = C2 + λ·δ̄(a,b)`, `δ̄ = (δ₂₁+δ₂₃)/2`, `λ = τ̂²/(τ̂²+σ̄²)` con
`τ̂² = max(0, Var_entre(δ̄) − σ̄²)`. Derivada de los `DELTA`/`DELTA-EE` sellados sobre las
**15 celdas `PUNTUADA`**, con `Var(δ̄) = (EE₂₁² + EE₂₃²)/4` por celda:

| cantidad | valor |
|---|---:|
| `k` | 15 |
| `media(δ̄)` | +0.011039613 |
| `Var_entre(δ̄)` | 0.028257826 |
| `σ̄²` | 0.003001124 |
| `τ̂²` | 0.025256702 |
| **`λ`** | **0.893794941** |

`τ̂² > 0`, así que el `max(0, ·)` no ata. Control con las 16 celdas (no se congela):
`λ = 0.831050904`. **Se congela `λ = 0.893794941`**; no se teclea, se deriva con el
comando de E.2. Que `λ ≈ 0.89` dice que la varianza entre celdas domina al ruido de
muestreo —la interacción es señal, no dispersión—, consistente con los 13 de 16 signos
estables.

## E.5 · `COMMIT-1` congelado (adenda 4)

Con `P0` fuera del camino del `COMMIT-1` y el cruce elegido, se congela. **Cero
microdato**: ninguna cifra de ENCIG 2025 se leyó para escribir nada de esto.

| artefacto | qué lleva |
|---|---|
| `forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_0.md` | spec humana; `sha256 20c358b6ae3025cf…` |
| `…-spec-v1_0.sha256` | sidecar |
| `data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0001/spec.yaml` | contrato ejecutable, `resultados_esperados: []` |
| `…/medidor.py` | código congelado, `medidor_ejecutado_al_congelar: NO` |
| `tests/test_piloto3_guardias.py` | **24 guardias, 24 en verde** (6 saltadas por falta de `numpy`/`pandas`) |

**Las dos condiciones suspensivas son mecánicas, no prosa.** Viven en
`_guardia_suspensiva()`, que corre **antes** de cualquier medición y levanta
`ParoDeGuardia`:

- **S1** — `COMMIT-2` no corre hasta que `NC-0355` cierre `MISMO-INSTRUMENTO` o
  `CAMBIO-MENOR`. Con `CAMBIO-DE-INSTRUMENTO` la spec **se retira sin correr**
  (`SUPERADO`, `n_resultados = 0`): el código lo dice y el test lo pina.
- **S2** — si la lectura de caja encuentra que alguno de `97`/`98`/`99` es **edad real
  censurada**, para y **reporta a mesa antes de emitir**. La rejilla del árbitro
  (`60-96`) no se toca aquí.

**`λ` congelada = `0.8937949410086089`**, en los tres artefactos, y el test verifica que
sean el mismo número **y** que satisfaga su propia identidad `τ̂²/(τ̂²+σ̄²)`.

> **La guardia se ganó el sueldo en el acto.** La primera versión declaraba `λ` y sus
> momentos redondeados a 9 decimales; `G2` falló por **2.7e-9** —`λ` no reproducía
> `τ̂²/(τ̂²+σ̄²)` a partir de los momentos escritos—. Se corrigió guardando los momentos a
> precisión completa en los tres sitios, no aflojando la tolerancia del test. Un
> pre-registro cuyo parámetro no se re-deriva de sus propios insumos no es un
> pre-registro.

## E.6 · Lo que NO se pudo registrar, y por qué es un hallazgo

**La celda-D `GOB.gobierno_digital.encig2025.edad_x_escolaridad` no se escribió.**
`PARA`, y no por falta de tiempo:

`tests/test_celdas_d.py:79` fija `UNIDADES_OBJETIVO = {persona, hogar, establecimiento,
agregado_geografico}`. **La unidad de este estimando es `TRÁMITE`** — así la declaran los
`RESULT` sellados de 2021 y 2023 (`unidad: "trámites"`), el docstring de
`tools/medidor_gobierno_digital_encig25.py` y el propio marcador («unidad = TRÁMITE:
quien pagó doce veces contribuye doce veces»). Un trámite no es una persona, ni un hogar,
ni un establecimiento, ni un agregado geográfico: **es un evento**.

Las dos salidas disponibles son malas y por eso no se tomó ninguna:

1. Registrarla con `unidad_objetivo: persona` **re-comete exactamente el defecto que
   `ADR-548` corrigió hace dos días**, cuando `unidad_dato` se infería del id y ENCIG 2025
   salía `persona` contra el árbitro que dice `TRÁMITE`.
2. Enmendar el enum vive en `tests/test_celdas_d.py`, **fuera del perímetro** de este
   encargo, que sólo autoriza `tests/test_piloto3_guardias.py`.

`NC-0362` abierta y **`FP-391` a mesa**: o se añade `evento` al enum, o se declara que
las celdas-D sobre eventos no se registran. **No bloquea el piloto** —el `COMMIT-2` corre
sin ella— pero sí deja hoy un estimando congelado que el registro no puede nombrar.
Celdas-D siguen en **5**.

## E.7 · Contadores al cierre

`cuenta_gen2` **NO-APLICA**. Cero corridas selladas, cero resultados, cero adopciones,
cero microdato. Dos filas nuevas en `decisiones.tsv` (`F1-bis` y `F3`, ambas firmas de
mesa selladas por el lanzamiento). `FP-389` FIRMADA; `FP-391` nueva, ABIERTA. `NC-0355` y
`NC-0356` siguen ABIERTAS —la segunda con enmienda fechada—, `NC-0362` nueva. El par
`edad × escolaridad` de ENCIG 2025 sigue **`RESERVADA`** en el marcador, que este acto no
tocó ni re-derivó.
