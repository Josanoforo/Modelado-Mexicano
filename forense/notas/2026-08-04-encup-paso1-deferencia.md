# ENCUP paso 1 — ¿hay reactivo de deferencia?

**Contadores movidos: 0.** Sin módulo de auditoría (v2.3). Este acto no mide,
desbloquea: verifica si el descriptor de ENCUP 2012 trae un reactivo que
opere `deferencia` por wording literal.

Encargo M, mesa #18, emitido 4/ago/2026. Rama `sesion/encup-paso1-deferencia`,
worktree `mm-encup-paso1-deferencia`.

## 0 · Entorno (protocolo §0)

```
$ python3 tests/bitacora.py --abre
HEAD: 58c809c == origin/main (ref local, sin fetch — se hizo fetch aparte
      antes de abrir la rama, ver §0.1)
check.py --baseline:       exit=0 · VERDE — nada nuevo frente a baseline
validador_registro_ids.py: exit=0 · OK, 49 IDs verificados
$ echo "$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE"
sin_variable
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200
$ ls data/raw | wc -l
133 (antes de reparar el wiring, ver §0.2) → sin cambio de conteo después
    (el wiring no crea archivos nuevos en el árbol del repo, solo en el
    corpus compartido fuera de git)
```

### 0.1 · Base declarada vs. HEAD real — discrepancia, no PARO

El encargo declara "Base: main con PR #79 fusionado". Verificado contra
GitHub: **PR #79 sigue `OPEN`** al abrir esta sesión (no fusionado). No es
ninguno de los cuatro disparadores de PARO listados en el encargo (premisa
(1) falsa · sha256 no coincide · reparto no cierra en 14 · el acto empuja a
medir) — es un descriptor de base desactualizado por concurrencia (PR #79
es la sesión que mide `exposicion_violencia`, tema no relacionado con este
acto). Se procedió desde el tip real de `origin/main` (`58c809c`, PR #78
fusionado) y se documenta la discrepancia en vez de fingir que no existió.

### 0.2 · `data/raw` — ausente en el sentido correcto, reparado

El worktree nació sin `data/raw` ni `data/raices.local.yaml` (ambos
gitignorados, no viajan solos a un checkout nuevo — mismo patrón que
`I-11`/`forense/notas/2026-07-31-p1-enigh-semilla.md`). Se enlazó
`data/raw -> /home/pc0/mm-corpus/raw` (el wiring estándar de todos los
demás worktrees). Con eso, `--verifica` reportó los seis payloads de ENCUP
**AUSENTES** — no porque el registro de `data/manifiesto.yaml` fuera falso,
sino porque **la sesión que los bajó (`sesion/encup-certificado-fijado`,
`PR #77`) los descargó dentro de su propio `data/raw` local (un directorio
real, no un symlink al corpus compartido) y nunca los copió al corpus**
(`/home/pc0/mm-corpus/raw`). Verificado con `sha256sum` directo sobre los
seis archivos en ese worktree contra `data/manifiesto.yaml`: coinciden
byte a byte los seis. Se copiaron (no se movieron, no se sobreescribió
nada) al corpus compartido y `--verifica` pasó a **COINCIDE** en los seis.
Esto es exactamente el gap de wiring que **no** dispara PARO por
instrucción explícita del encargo ("`data/raw` ausente no es PARO: se
crea o se enlaza"), y deja el corpus compartido consistente para
cualquier worktree futuro — no solo para este acto.

## 1 · Premisas

| # | Premisa | Verificación |
|---|---|---|
| PM-1 | Seis payloads de ENCUP registrados y en disco | **Sostiene**, con la reparación de §0.2. `grep -n "^- id: encup_" data/manifiesto.yaml` → 6 entradas (`encup_2012_base_datos_xlsx`, `encup_2001/2003/2005/2008/2012_cuestionario_pdf`). `--verifica` los seis: **COINCIDE** (sha256 y tamaño), incluido `encup_2012_base_datos_xlsx` en 4 814 178 B exacto |
| PM-2 | C-bis dejó ENCUP abierta sin leer el cuestionario — bloqueo de portal, no de contenido | **Sostiene**, cita literal contra archivo: `forense/notas/2026-08-03-cbis-deferencia-externas.md` §5.3, veredicto textual "**NO DETERMINABLE — espejo fuera del sandbox**... el portal INEGI de ENCUP sí resultó ser una SPA sin instrumento descargable... Ruta de recuperación anotada: (a) descarga manual del archivo por el autor... (b) una sesión futura con ese host agregado a la lista de hosts permitidos" — exactamente lo que Encargo L ejecutó |
| PM-3 | `deferencia` en reparto del motor: M3, Latinobarómetro P4NOIJ, ADR-51(f); reparto cierra en 14 | **Sostiene, con matiz de fecha.** `canon/modelo-decision-v4_0.md:271`: `deferencia (M3, Latinobarómetro P4NOIJ, ADR-51 (f))`, fila "Proxy declarado, pendiente de medición", cuenta 3. Tabla completa (línea 268-272) cierra hoy en **8+1+2+3=14**, no en 9+0+2+3 — la cifra del encargo asume `PR #79` (que mueve `exposicion_violencia` de 1→0 sumando a 8→9) ya fusionado, y no lo está (§0.1). El total sigue cerrando en 14 de cualquier forma: no es el reparto lo que falla, es la composición interna, y **no es uno de los disparadores de PARO** ("el reparto no cierra en 14" ≠ "la fila que sube no es la que el encargo esperaba") |
| PM-4 | H-07 (edad) y H-08 (tam_loc) son las hipótesis que `deferencia` debe discriminar | **Sostiene**, cita literal `canon/modelo-decision-v4_0.md:220-221`: H-07 "E[`deferencia` \| joven] < E[`deferencia` \| mayor]", eje `edad`; H-08 "E[`deferencia` \| tam_loc∈{3,4}] > E[`deferencia` \| tam_loc=1]", eje `tam_loc`. Ambas en estado "PROXY CON SUPUESTO DECLARADO (parcial)... forma PENDIENTE, no comprobable hoy" |
| PM-5 | ENCUP descontinuada, la base real es 2012 | **Sostiene**, cita literal `forense/notas/2026-08-04-encup-certificado-fijado.md:50`: "PL-3 — ENCUP está descontinuada; última edición 2012 — Sostiene. Portal... no lista edición posterior a `Cuestionario-Quinta_2012_ENCUP.pdf`/`BaseDatos_ENCUP_2012_Final.xlsx`"; y `data/manifiesto.yaml` (nota de cada entrada): "Fuente descontinuada: ENCUP no tiene edición posterior a 2012; este payload es la última edición conocida" |

Ninguna premisa (1) falla. No hay PARO.

## 2 · Frase-criterio — escrita antes de abrir el PDF

```
deferencia = disposición declarada a acatar la decisión de una autoridad
-jerárquica, institucional o de edad- aun sin acuerdo propio; distinta de
(a) confianza en instituciones [ya condicional propia, 6 componentes],
(b) obediencia como valor de crianza a inculcar en terceros [el proxy
actual, P4NOIJ, cae aquí], y (c) conformidad social entre pares
[horizontal, no jerárquica].

Objetivo final del motor (R2.1, canon/modelo-decision-v4_0.md:442, id
trabajo.jerarquia.deferencia_iniciativa_suprimida): deferencia ante
jerarquía interpersonal/laboral/familiar CONCRETA (jefe, patrón, cabeza de
familia), con efecto conductual nombrado -- iniciativa suprimida, el "sí"
que significa "probablemente".
```

Esta frase se escribió y se guardó en el scratchpad de la sesión antes de
ejecutar `pdftotext` sobre `encup_2012_cuestionario_pdf.pdf` — verificable
por el orden de los comandos de esta sesión, no solo por declaración.

## 3 · Candidatas — wording literal × universo × catálogo × distinción

El barrido cubrió el cuestionario completo (11 páginas, `pdftotext -layout`,
84 preguntas, XIV secciones). Ningún ítem menciona "jefe", "patrón",
"jerarquía" o "padre/madre" como objeto de una pregunta actitudinal —
las tres ocurrencias de "jerarquía" son categorías de la clasificación de
ocupación (D, "empleado de cualquier jerarquía"), no un reactivo. Dos
candidatas superaron el barrido de términos por acercarse al vocabulario
de acatamiento; ninguna cumple el criterio, con argumento por descarte.

| Candidata | Wording literal | Universo | Catálogo | Por qué NO cumple |
|---|---|---|---|---|
| **P44A** (var. `P44A` en el XLSX) | *"¿Qué tan de acuerdo o en desacuerdo está usted con la frase 'Los ciudadanos deben obedecer siempre las leyes aún cuando sean injustas'"* | Población general, sin filtro previo | Muy de acuerdo / De acuerdo / En desacuerdo / Muy en desacuerdo / No sabe / No contesta | **(a)** — objeto de actitud es la ley como institución abstracta frente al Estado, no una jerarquía interpersonal/laboral/familiar concreta. Precedente directo y casi textual: `ENCUCI AP5_11` ("las personas deben obedecer siempre las leyes aunque sean injustas") fue descartado por la misma razón en Encargo C (`forense/notas/2026-07-31-encargo-c-familismo-deferencia-reactivo.md:113-115`), sin calificar ni como proxy — "objeto de actitud distinto (autoridad legal-política, no jerarquía personal/laboral/familiar) y sin el componente conductual". Aplicado sin relajar |
| **P68** | *"En nuestro país existen personas que piensan con ideas diferentes a la mayoría de la población, en su opinión esas personas deben…"* → opción 1: *"Obedecer la voluntad de la mayoría, dejando de lado sus ideas"* | Población general, sin filtro previo | 1 Obedecer la mayoría / 2 Tener ideas sin convencer / 3 Tener ideas e intentar convencer / No sabe / No contesta | **(c)** — el objeto de acatamiento es "la voluntad de la mayoría", horizontal (consenso social/numérico), no una autoridad jerárquica vertical concreta |

**Descartadas sin tabla, por no acercarse al criterio ni por vocabulario:**
la familia de ítems de preferencia por régimen autoritario (P13, P14A-C,
P22A-D, P24, P25 — "gobierno que impone sus decisiones", "líderes duros",
"presidente que use la fuerza") mide **preferencia por un estilo de
gobierno a nivel de régimen político**, no la disposición del propio
respondiente a deferir ante una jerarquía concreta — mismo objeto de
actitud excluido que P44A, un peldaño más arriba (régimen, no ley). P36,
P49, P74 (estilo de liderazgo preferido, estrategia para acercarse a
autoridades) preguntan cómo debería comportarse un tercero o el grupo, no
la disposición del respondiente a acatar.

**Ninguna candidata cumple el criterio.** No hay reactivo de `deferencia`
en `ENCUP 2012` bajo la frase-criterio de §2.

## 4 · Correspondencia cuestionario ↔ base, con `n`

Ambas candidatas descartadas SÍ existen en `BaseDatos_ENCUP_2012_Final.xlsx`
(hoja `BaseDatos_ENCUP_2012_Final`, `n` total = 3750 filas de datos, leído
con parser propio stdlib — `zipfile`+`xml.etree`, sin dependencias
externas porque el entorno no tiene `pip`/`openpyxl` — verificado contra
el wording del PDF, coincide palabra por palabra):

| Variable | Columna (0-index) | `n` total | Válidas (excl. No sabe/No contesta) |
|---|---|---|---|
| `P44A` | 113 | 3750 | 3683 (1750 En desacuerdo, 1399 De acuerdo, 341 Muy en desacuerdo, 193 Muy de acuerdo; 67 No sabe/No contesta) |
| `P68` | 207 | 3750 | 3592 (2046 opción 2, 859 opción 3, 687 opción 1 "obedecer mayoría"; 158 No sabe/No contesta) |

Esto es el chequeo que distingue "el instrumento lo pregunta" de "el dato
existe": aquí las dos afirmaciones coinciden (ambas preguntas existen con
datos), y aun así ninguna sirve — el descarte es por objeto de actitud, no
por ausencia de dato.

## 5 · Denominador

Ninguna de las dos candidatas está condicionada a un trámite, empleo o
subgrupo: `P44A` y `P68` se preguntan sobre el universo completo de la
encuesta (`n`=3750 respondientes, sin filtro de aplicabilidad previo en el
cuestionario ni salto de sección). El denominador no es el problema aquí
— es el único de los cuatro chequeos que ambas candidatas pasan limpio.

## 6 · C2 — ¿ENCUP observa desenlaces de los generadores que usan `deferencia`?

`grep -n "PORQUE G6" canon/modelo-decision-v4_0.md` → tres reglas invocan
`G6`:

1. `trabajo.jerarquia.deferencia_iniciativa_suprimida` (R2.1) — desenlace:
   iniciativa suprimida ante jerarquía laboral/familiar concreta
2. `trabajo.rotacion.joven_urbano_sin_culpa` — desenlace: cambio de empleo
   sin culpa, exige que las decisiones se justifiquen
3. `comunicacion.retroalimentacion.privada_publica_capital_social` —
   desenlace: retroalimentación debe ser privada, no pública

**Cierra, no queda abierto.** `ENCUP 2012` no tiene sección de trabajo,
empleo o comunicación interpersonal más allá de la clasificación de
ocupación (D) y el estado civil (F) — ningún wording de las tres salidas
vive en el cuestionario (barrido de términos "culpa", "rotación",
"retroalimentación", "privad-", "renuncia", cero coincidencias con
sentido). Aunque hubiera candidata de `deferencia`, este instrumento no
podría identificar `β` contra estos tres desenlaces en la misma encuesta
(criterio C1-C4 de P2 §2.b) — es un cierre doble, por objeto de actitud
(§3) y por ausencia de desenlace observable (aquí).

## 7 · C3 — circularidad contra Tabla B

`grep -n -i "encup" forense/notas/2026-07-31-inventario-segmentacion.md`
→ **cero resultados.** ENCUP no está entre las fuentes de la Tabla B de
segmentación. Cierra limpio, sin circularidad que declarar.

## 8 · Ejes de atributos — cuáles de los seis existen en la base 2012

| # | Eje (motor, `§1.1.A`) | ¿Existe en ENCUP 2012? | Variable / `n` |
|---|---|---|---|
| 1 | Formalidad laboral (`segsoc`) | **Parcial, no equivalente** | `D. ¿Cuál es su principal ocupación?` (col. 255) — 11 categorías (Trabajador en gobierno/sector privado/cuenta propia/comerciante/empresario/ama de casa/desempleado/jubilado/estudiante), `n`=3743 válidas de 3750. Es clasificación ocupacional, no derechohabiencia (`segsoc` es específicamente afiliación a seguridad social) — proxy temático, no la misma variable |
| 2 | Edad | **Sí, directo** | `B) Edad` (edad exacta, col. 13) y `B_ Grupo de edad` (4 bandas: 18-24/25-34/35-49/50+, col. 14), `n`=3750/3750, sin faltantes |
| 3 | Urbanización/`tam_loc` | **Parcial, no equivalente** | `Tipo de sección` (col. 8), 3 categorías (1: n=2590, 2: n=750, 3: n=410), `n`=3750/3750 sin faltantes — **catálogo no verificado en este acto** (no hay hoja de códigos en el XLSX); no es evidentemente el mismo corte que `tam_loc` del motor (4 categorías por umbral poblacional de localidad, `canon §1.1.A`) — "tipo de sección" es clasificación electoral (urbana/mixta/rural), variable distinta aunque temáticamente adyacente |
| 4 | Ingreso | **No presente** | Sin variable de monto ni de estrato de ingreso del hogar/persona. Lo más cercano (`A1`, escolaridad del principal aportador) mide educación, no ingreso |
| 5 | Acceso digital | **No presente como tenencia** | `P4` (medio más usado para informarse de política, incluye "internet"/"redes sociales") mide **uso de medios**, no tenencia de dispositivo/conexión — construcción distinta de `celular`/`conex_inte` del motor |
| 6 | Condición migratoria | **No presente como estatus** | `P84`-`P87` (habla lengua indígena/extranjera; ha vivido fuera del país, cuánto tiempo, por qué) son conducta/experiencia migratoria puntual, no el catálogo de 34 categorías de `residencia` (32 entidades + EUA + otro país) que usa el motor |

**Advertencia previsible, cumplida:** ninguno de los ejes 4-6 existe con
la misma operacionalización que el motor usa hoy (2022, vía ENIGH); de
existir, "acceso digital 2012" tampoco significaría lo mismo que hoy — la
salvedad no llegó a aplicarse porque el eje 5 no está, punto más simple
que el previsto.

## 9 · Viabilidad de H-07 y H-08 — si hubiera existido candidata

Aunque no hay candidata (§3), se reporta la viabilidad estructural que
pedía el encargo, para que quede escrito y no se repita el barrido:

- **H-07 (gradiente por edad):** **hubiera sido comprobable.** `B_ Grupo
  de edad` cubre las 4 bandas sobre el universo completo (`n`=3750, cero
  faltantes) — cualquier corte de "joven"/"mayor" dentro de esas bandas es
  ejecutable hoy contra este archivo.
- **H-08 (gradiente por `tam_loc`):** **no hubiera sido directamente
  comprobable.** La única variable de localidad (`Tipo de sección`, §8)
  no es `tam_loc` — 3 categorías electorales contra 4 categorías por
  umbral poblacional, sin crosswalk declarado ni verificado en este acto.
  Probar H-08 contra este archivo habría exigido una tabla de
  correspondencia entre "tipo de sección" y los cuatro cortes de `tam_loc`
  que ninguna fuente en disco declara — un cuarto motivo de cierre, no
  solo la ausencia de reactivo.

## 10 · Límite de 2012 (§4 del encargo)

`ENCUP` está descontinuada; la última edición es 2012 (PM-5). Este
descarte no depende de la fecha — se cerró por objeto de actitud (§3), no
porque el dato esté viejo —, pero si algún día una candidata de esta
fuente sí calificara, cargaría la misma marca que el proxy actual: un
corte de catorce años, mientras el resto de las condicionales miden
2020-2025. `deferencia` es de los constructos que menos se espera que se
muevan año a año, y el proxy vigente (Latinobarómetro `P4NOIJ`) ya es
n=1200, regional — la fecha viaja pegada al número también ahí. Que mesa
lo tenga a la vista si alguna vez decide entre estas dos fuentes.

## 11 · Veredicto

**LA FUENTE NO TIENE EL DATO.** Descriptor recorrido completo (84
preguntas, 11 páginas), dos candidatas por vocabulario examinadas y
descartadas con argumento (precedente directo con `ENCUCI AP5_11` para
`P44A`; objeto horizontal para `P68`), ninguna cumple la frase-criterio de
§2. `deferencia` sigue en `PROXY CON SUPUESTO DECLARADO (M3,
Latinobarómetro `P4NOIJ`, ADR-51(f))` — **sin cambio**, ahora con ENCUP
examinada y cerrada en vez de pendiente. Las cuatro ediciones de contexto
(2001, 2003, 2005, 2008) no se analizaron candidato por candidato (fuera
del objetivo declarado, §2 del encargo); un barrido de términos rápido
mostró que el ítem gemelo de `P44A` ("obedecer siempre las leyes...") ya
aparece en 2001 — la misma familia de ítem de legitimidad legal, no de
jerarquía interpersonal, es estable en la serie, no un artefacto de 2012.

## 12 · Declaración de contaminación (ADR-46)

Esta sesión abrió y leyó completo `Cuestionario-Quinta_2012_ENCUP.pdf`
(el instrumento) y `BaseDatos_ENCUP_2012_Final.xlsx` (encabezados y
recuentos de columnas, no microdato persona por persona más allá de los
conteos agregados de §4). Por tanto **queda inhabilitada para
pre-registrar contra ENCUP** (cualquier constructo, no solo `deferencia`).
Puede seguir trabajando la fuente (p. ej., la candidatura de posición 9,
`confianza_institucional[electoral]`) — la restricción es sobre
pre-registro, no sobre lectura ni sobre escritura.

## 13 · Suite, corrida tras la última edición

```
$ python3 tests/check.py --baseline
exit=0 · VERDE — nada nuevo frente a tests/baseline.json
$ python3 tests/validador_registro_ids.py
exit=0 · OK — 49 IDs verificados, todos con ancla y tier consistentes
```

No se tocó `canon/` (contenido) ni `milpa/`. No se movió ningún contador
(`deferencia` sigue en la misma fila de §3.5, "Proxy declarado, pendiente
de medición", cuenta 3 de 14).
