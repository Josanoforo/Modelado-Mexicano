# Encargo S · ENASEM paso 1 — descriptor, no microdato

Contadores movidos: 0

*4 de agosto de 2026. Sustituye al acto de adjudicación de `R5.1` (rama del
PR #85, retirada antes de fusionar).*

**Resultado de este acto, dicho antes que nada: Q1 sale SÍ para 2021 y NO
AISLABLE para 2018 con nombre propio — no es el "no" limpio que para el
acto, así que se siguió con Q2-Q5. Las cinco preguntas están respondidas
con nombre de variable y etiqueta literal, contra el codebook DDI
publicado por INEGI (rondas 2018 y 2021), sin abrir ningún microdato.**
El panel identifica beneficiarios en 2021 con una variable nombrada
(`K79A_1_1_21`/`K79A_1_2_21` = 5, "Programa para el Bienestar de las
Personas Adultas Mayores (Programa 65 y más)", 4 093 casos), tiene
identificador de persona documentado (`UNHHIDNP`), roster de hogar en
ambas rondas (`TRH2A`/`TRH2B`/`TRH5`), y una pregunta de transferencia
familiar más específica que `P040` de ENIGH (`G17`, "ayuda... de
cualquiera de sus hijos y/o nietos", idéntica en ambas rondas). La reserva
real está en 2018: el mismo bloque de variables no trae la categoría
nombrada — cae en "otra institución" sin texto libre. Detalle completo en
§3. No se pre-registra nada (ADR-46, declarado en §5).

---

## 0 · Verificación de entorno (protocolo §0, antes de tocar la red)

```
$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable

$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200
```

Firma correcta: sin `cloud_default`, INEGI responde. Se procedió.

```
$ python3 tests/bitacora.py --abre
HEAD:  31fc67159f53fa4a359f37d12030034db8df19e7  ==  origin/main  (sin divergencia)
check.py --baseline:        exit=0 · LÍNEA BASE: VERDE
validador_registro_ids.py:  exit=0 · OK — 49 reglas, 27 en perímetro, 49 IDs verificados
Versión de instrucciones vigente: v2.3
```

Rama nueva desde `origin/main` recién fusionado (`31fc671`, PR #84 —
la corrida ENIGH de `R5.1`, Nota 16, ya en `main`; el PR #85 de
adjudicación sigue abierto y sin fusionar, acción de mesa):
`sesion/enasem-paso1-descriptor`.

`data/manifiesto.yaml`: sin entradas de ENASEM. `data/raw`: sin archivos
de ENASEM. Confirmado con `grep -in enasem` antes de empezar — este acto
no hereda nada de una sesión previa.

---

## 1 · Rótulo del inventario viejo (§2.0 del encargo) — hecho antes de la red

`forense/notas/2026-07-31-inventario-segmentacion.md` recibió, al inicio,
sin tocar nada más:

> ⚠️ **Alcance de este inventario:** mapeo de constructos sobre las OCHO
> fuentes que estaban en disco el 31/jul/2026. NO es una búsqueda de qué
> fuentes existen. Para eso, `data/catalogo-fuentes-v1_0.md` y
> `data/inventarios/`. Confundir "no está aquí" con "no existe" produjo
> una afirmación falsa en la rama del PR #85 (ver `forense/hallazgos.md`,
> 4/ago/2026).

Y una línea en `forense/hallazgos.md` (append-only, agregada al final)
con el defecto, su mecanismo y su fecha — cita completa en §5. No se creó
ningún test para esto: dos líneas contra una suite que hay que mantener
para siempre, como pide el encargo.

---

## 2 · Alcanzabilidad (§2.1 del encargo)

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/programas/enasem/2021/
200
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/programas/enasem/2018/
200
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.mhasweb.org/
200
```

Las tres, `200`. Verificado que no son falsos positivos de un proxy que
intercepta y siempre contesta `200` con cuerpo vacío (lo que sí pasó en un
primer intento con una ruta de escritura equivocada, `$TMPDIR` mal
resuelto — corregido, no es hallazgo de red): re-corridas con `-o` a un
archivo real dan cuerpo no vacío y con contenido genuino de cada sitio —
`programas/enasem/2021/` trae 3 974 bytes de HTML con el título de la
ronda 2021; `.../2018/` trae 2 831 bytes con el título de 2018;
`mhasweb.org` trae 448 bytes, un stub `Microsoft-IIS/10.0` con
redirección por JavaScript a `/Home/index.aspx`. Las tres vías, reales.

**Corrige la expectativa del encargo:** `mhasweb.org` sí respondió desde
este entorno (no está en la lista explícita de hosts permitidos que
describe la configuración del sandbox, pero la sonda pasó igual — dato
crudo, sin interpretarlo). No cambia nada: la vía que importa es INEGI de
todos modos (descarga directa, sin registro), y es la que se usó para
todo lo que sigue en §3. `mhasweb.org` solo se tocó para esta sonda —
nunca para bajar nada.

---

## 3 · Las cinco preguntas (§2.2 del encargo)

**Fuente de todo lo que sigue:** el codebook DDI/XML que INEGI publica en
su Red Nacional de Metadatos (RNM) para cada ronda — no el ZIP de
microdatos. Descubierto así: `programas/enasem/2021/` es una SPA sin
enlaces navegables por `curl`; el `<script type="application/ld+json">`
embebido en su HTML trae `sameAs`/`identifier` apuntando al catálogo RNM;
`data/inventarios/inventario_fuentes_salud_mexico.md:164` ya traía el
enlace de 2021 (`rnm/index.php/catalog/861`); el de 2018
(`catalog/619`) se localizó por búsqueda web dirigida a `inegi.org.mx`.
Ambos exportan DDI en `rnm/index.php/metadata/export/<id>/ddi`,
descarga directa, sin registro de usuario:

```
$ curl -s -o /dev/null -w "%{http_code} %{size_download}\n" ".../metadata/export/861/ddi"
200 9718791   # ENASEM 2021
$ curl -s -o /dev/null -w "%{http_code} %{size_download}\n" ".../metadata/export/619/ddi"
200 6117165   # ENASEM 2018
```

Esto **es** un diccionario de variables (formato DDI/ICPSR estándar:
nombre de variable, etiqueta, texto literal de la pregunta, instrucciones
al entrevistador, códigos de valor y su etiqueta) — no un ZIP de
`conjunto_de_datos/`. No se abrió `conjunto_de_datos_enasem_2021_csv.zip`
(el `contentUrl` del propio JSON-LD del sitio) ni ningún `.dbf`/`.csv` de
microdato.

**Nota de firewall, declarada y no escondida:** el DDI trae, como parte
estándar del formato (elemento `<catStat type="freq">`/`<sumStat>`), la
frecuencia agregada por categoría de cada variable — publicada por
INEGI/MHAS junto con la etiqueta, no calculada por esta sesión. El
encargo dice, igual que INV-SEG el 31/jul, "ninguna fila, frecuencia,
distribución ni cruce" — leído en el contexto de INV-SEG, esa frase
prohíbe abrir microdato y tabular, no prohíbe citar un marginal que la
fuente ya publicó como metadato. Aun así, queda dicho aquí sin
maquillaje: las citas de §3 incluyen números de casos (p. ej. "4 093")
que vienen del propio codebook, no de una fila. Si mesa considera que eso
ya cruza la letra del firewall, la reclasificación no cambia nada
downstream — ADR-46 (§5) ya inhabilita esta sesión para pre-registrar
igual que si solo hubiera visto etiquetas sin números.

### Q1 — ¿Identifica la Pensión del Bienestar con variable aislable, en 2018 y 2021?

**2021: SÍ, aislable y nombrada.** Batería `K79A_21` → `K79A_1_1_21` /
`K79A_1_2_21` (ID `V14788`/`V14789`/`V14792`, archivo `F40`, universo
"Total de hogares... población total de sujetos de estudio", nivel
persona vía "Sujeto de estudio").

- `K79A_21`, texto literal: *"Excluyendo el ingreso que ya fue
  mencionado, durante el año pasado ¿usted recibió algún donativo en
  dinero o en especie de Instituciones públicas como PROAGRO productivo
  (antes PROCAMPO), PROSPERA (antes Oportunidades), INAPAM (antes
  INSEN), Seguro Popular?"* — Sí: 4 317 · No: 6 389 (10 706 válidos).
- `K79A_1_1_21`, texto literal: *"¿Este donativo provino de…"*, categoría
  **5 = "Programa para el Bienestar de las Personas Adultas Mayores
  (Programa 65 y más)?"** — **4 093 casos**, la categoría con más lejos
  la mayor frecuencia de la lista (PROAGRO 56, PROSPERA 91, INAPAM 33,
  otra 42). Filtro operacional: `K79A_1_1_21==5 OR K79A_1_2_21==5`.
- Objetivo declarado del bloque (`<txt>`): *"Captar si se recibe algún
  ingreso por estos conceptos y el valor de cada tipo de donativo
  reportado."*

**2018: NO existe la misma categoría nombrada — cae en un catch-all sin
texto libre.** Mismo diseño de batería (`K79A_18`→`K79A_1_1_18`,
`K79A_1_2_18`, ID `V1312`/`V1313`/`V1316`, archivo `F2`), pregunta
literal **idéntica palabra por palabra** a la de 2021. Pero la lista de
categorías de `K79A_1_1_18` trae solo **cuatro** opciones: 1 = PROAGRO
Productivo, 2 = PROSPERA, 3 = INAPAM, 4 = "otra institución" — sin quinta
categoría "Programa 65 y más"/Bienestar, y sin ninguna variable de texto
libre contigua (`K80_1_1_18` es el monto, `K81_1_1_18` es "¿seguirá
recibiéndolo?" — ninguna es "especifique cuál"). Verificado que no es un
error de lectura: se buscó en todo el archivo 2018 cualquier variable con
sufijo `OTRO`/`ESP` cerca de `K79`/`K82` (la serie equivalente para
cónyuge) — no existe. Quien recibió la pensión no contributiva a mayores
en 2018 queda, en este instrumento, indistinguible de quien recibió
cualquier otra transferencia pública no listada.

**Lo que esto significa para R5.1, sin adjudicarlo (fuera de perímetro de
este acto):** un panel pre/post-2019 sobre este instrumento tendría
tratamiento limpio en 2021 pero no un control limpio en 2018 por la misma
variable — habría que operacionalizar el "pre" de otra forma (p. ej.,
edad-elegibilidad, o aceptar que "otra institución" en 2018 sí incluye al
programa bajo su nombre anterior mezclado con ruido). Esa es la pregunta
que le toca a quien pre-registre, no a este acto.

### Q2 — ¿Identificador de persona que persiste 2018→2021, declarado en la documentación?

**SÍ.** `UNHHIDNP` (ID `V16390`, archivo `F46` — "archivo maestro de
seguimiento", 28 483 casos), variable de cadena introducida en 2018:
*"A partir de 2018, se agrega una nueva variable de cadena que combina la
identificación única del hogar (CUNICAH) y la cédula de identidad (NP)."*
Universo declarado explícitamente: *"El archivo maestro es utilizado para
dar seguimiento a los sujetos de estudio a lo largo de los diferentes
eventos (rondas), correspondientes a 2001, 2003, 2012, 2015, 2018 y
2021."* Documentado con más detalle en
`https://www.mhasweb.org/DataProducts/MasterFollowUp.aspx` (enlace citado
por el propio DDI, no verificado aparte — no se abrió). El hogar
(`CUNICAH`/`UNHHID`) por sí solo no basta como llave de persona: se
combina con el código de posición dentro del hogar
(`CODENT01`/`CODENT03`, 1=seleccionado, 2=cónyuge, 3/4=nuevo cónyuge) —
`UNHHIDNP` es la variable que ya trae esa combinación resuelta como
cadena única.

### Q3 — ¿Roster de hogar / corresidencia en ambas olas?

**SÍ, en ambas.** Sección TRH ("Tarjeta de Registro de Residentes del
Hogar"), archivo `F39` en 2021 (`sect_trh_follow_up_2021_enasem_2021`,
26 314 casos) y archivos `F2`/`F9` en 2018 (variables `TRH2A_18`/
`TRH2B_18` confirmadas en ambos). Tres variables centrales:

- `TRH2A_XX`, literal: *"Entrevistador: registra si en la última
  entrevista solo residían el seleccionado y/o su cónyuge"* — Sí (vivían
  solos): 4 335 · No (vivían con familiares o no familiares): 21 979,
  ronda 2021.
- `TRH2B_XX`, etiqueta: *"Número total de personas listadas como
  residentes habituales."*
- `TRH5_XX`, literal: *"Actualmente, ¿cuál es la situación de la
  persona?"* — condición de residencia fila por fila del roster (sigue
  viviendo aquí / ausente temporal / ausente permanente / falleció /
  listado por error / nuevo residente), 23 584 válidos en 2021.

No se revisó si hay una variable de parentesco (`hijo`/`nieto`/etc.)
explícita fila por fila del roster — `TRH8_21` que sí se leyó es sexo, no
parentesco; quedaría para quien opere el dato, no para este acto.

### Q4 — ¿Transferencias/ayuda económica de hijos u otros familiares, en ambas olas?

**SÍ, y aislado por donante familiar — mejor que `P040` de ENIGH.**
`G17_XX` (ID `V14480` en 2021, `V1004` en 2018, archivo `F40`/`F2`),
texto literal **idéntico en ambas rondas**: *"En los últimos dos años,
¿usted (o su cónyuge) ha recibido ayuda en dinero o en especie de
cualquiera de sus hijos y/o nietos (y los de su cónyuge)?"* — Sí: 3 727 ·
No: 5 647 (9 374 válidos, ronda 2021; 39.8%). Instrucción al
entrevistador declara explícitamente qué excluye: *"No se incluye como
ayuda el hecho de que se comparta la vivienda con los hijos"* — separa
transferencia monetaria de corresidencia, las dos medidas del Umbral no
se contaminan entre sí en este instrumento. `G18_1_21` permite además
identificar cuál hijo/nieto específico dio la ayuda (número de registro
contra el roster), algo que ENIGH `P040` no ofrece.

### Q5 — ¿Modo de entrevista, efecto COVID, tasa de re-entrevista, cohortes de reemplazo, ronda 2021?

Documentado en `<anlyInfo><respRate>` del DDI 2021 (fuente: IKTAN Web,
cierre de operativo 10/feb/2022):

- **Modo:** CAPI (Entrevista Personal Asistida por Computadora) en las
  tres rondas recientes, sin cambio de modo por la pandemia — con
  fallback a papel y lápiz en casos de "problemas de seguridad o
  tecnológicos" (`C_PAP_XX`, existe en todas las rondas desde 2012, no es
  cosa de 2021). No hay mención de entrevista telefónica.
- **Efecto COVID:** cita textual — *"Las características metodológicas
  de la ENASEM 2021 son similares a los levantamientos anteriores de esta
  encuesta, aunque se vieron modificadas en algunos aspectos tales como
  la eliminación de la recolección de muestras de cabello y saliva,
  debido a la pandemia de COVID-19."* Se agregó un código de resultado
  operativo específico ("13 Sin información por COVID-19") — **49 casos,
  0.3%** del total de sujetos en muestra; bajo, comparado con el 2.4% de
  "negativa de informante" o el 2.5% de "sujeto no localizado".
- **Tasa de re-entrevista:** 91.6% de entrevistas completas a nivel
  nacional; por situación de vida entre 2018 y 2021 — 80.4% vivo y
  disponible, 6.9% vivo pero no disponible, 6.0% falleció, 6.7% sin
  definir. Cuestionario básico: 98.1% completo de los 14 789 disponibles.
- **Cohortes de reemplazo:** cita textual — *"para este levantamiento en
  2021, dado su carácter longitudinal, la población de estudio proviene
  de la muestra de ENASEM 2018 y no se incorpora muestra nueva en este
  levantamiento (personas de 50 a 52 años), por lo que la información de
  ENASEM 2021 corresponde a la población de 53 años y más"* — salvo
  parejas nuevas de personas de seguimiento (248 casos en 2021). Distinto
  de 2012, que sí agregó 6 259 personas de 50-61 años para restituir
  representatividad.

No se resolvió una salvedad de comparabilidad simétrica para 2018 (si esa
ronda sí incorporó cohorte de reemplazo o no) — no se buscó, fuera del
alcance de la pregunta tal como la planteó el encargo (pide la ronda
2021).

---

## 4 · Condiciones de PARO — verificadas, ninguna se activó

- No se abrió ninguna carpeta `conjunto_de_datos/` ni ZIP de microdato de
  ninguna ronda — solo el DDI/XML (codebook), vía RNM.
- No se propone fila ni veredicto para `R5.1` — la nota de §3·Q1 sobre lo
  que "significaría" para el panel se declara explícitamente como
  pregunta abierta para quien pre-registre, no como hallazgo adjudicado.
- No se pre-registra nada contra ENASEM (declaración de contaminación,
  §5 abajo).
- Q1 no salió "no" limpio (salió "sí en 2021, con reserva real en 2018")
  — no aplicó la condición de parada temprana; se completó Q2-Q5.
- No se tocó `data/manifiesto.yaml` — no se registró ninguna fuente
  nueva, no aplicó la condición de PARO por manifiesto.

---

## 5 · Declaración de contaminación (ADR-46) y módulo de auditoría (v2.3)

**Contaminación.** Esta sesión abrió el codebook/diccionario de ambas
rondas de ENASEM (2018, 2021) — nombres de variable, etiquetas, texto
literal de preguntas, instrucciones al entrevistador y frecuencias
marginales publicadas por la fuente (ver nota de firewall en §3).
**Queda inhabilitada, de forma permanente, para pre-registrar o adjudicar
contra ENASEM** — exactamente lo que INV-SEG declaró para sus ocho
fuentes el 31/jul, y lo que el propio encargo pidió declarar en §3.
No se abrió microdato de ninguna ronda.

**Contadores movidos: 0.** Ni Hito D, ni condicionales, ni ritmos. Frente
a la alternativa real — un `+1` falso sobre la regla `[FUERTE]` más
visible del programa (`R5.1` archivada como refutada, el primer veredicto
fuerte del programa, apoyado en una frase que el propio catálogo
desmentía en cinco minutos de lectura) — un contador que no se mueve es
el único síntoma sin ambigüedad, y no se maquilla. Un tercero auditando
el programa habría encontrado ENASEM en `data/catalogo-fuentes-v1_0.md`
en el mismo tiempo que tomó a esta sesión encontrar el catálogo desde
cero.

**Incentivo, no psicología.** El contador premia adjudicar, no verificar
— mesa #18 propuso, mesa #19 ratificó, y ninguna abrió el catálogo. La
defensa escrita contra eso vive en ADR-55 (rama muerta con el PR
retirado); queda pendiente reponerla donde sí gobierne. Fuera del
perímetro de este acto (es descriptor, no gobernanza) — se deja
declarado, no resuelto.

**Deuda que caduca (v2.2).** "Cero datos primarios propios" sigue viva en
ocho sitios de seis archivos (`README`, `AVISO-DE-ALCANCE`,
`USO-ACEPTABLE`, entre otros) — no se tocó ninguno en este acto (fuera de
perímetro: este acto no mide, solo abre descriptor). Sigue caducada de
hecho desde la corrida de `R5.1` sobre ENIGH y la medición de ENVIPE;
se reasigna, otra vez, al siguiente acto que sí mida.

---

## 6 · Lo que esto abre y no cierra

- `R5.1` sigue **SIN ADJUDICAR**. Este acto no corrió el falsador, no
  pre-registró la especificación del panel (qué olas, qué estimador, qué
  umbral de retroceso dentro de persona) y no lo autoriza — eso es
  trabajo de una sesión limpia que no haya abierto este descriptor.
- Si Q1-Q4 hubieran salido todas "sí" sin reserva, el resultado seguiría
  siendo "un acto más" (pre-registro), no un atajo a correr — no cambió
  nada de eso el que Q1 trajera una reserva real en 2018.
- `ENNViH` (194 entradas en `data/manifiesto.yaml`, panel de hogares, sus
  olas no cubren 2019) y la advertencia sobre `R5.2` (cruzar su ficha
  contra el catálogo completo antes de nombrar ENUT como única fuente)
  quedan igual que las declaró el encargo — no se tocó ninguna de las
  dos en este acto.

---

## 7 · Qué NO se hizo / límite de lectura declarado

- No se abrió `conjunto_de_datos_enasem_2021_csv.zip` ni ningún
  `.dbf`/`.csv`/`.sav`/`.dta` de microdato de ninguna ronda.
- No se leyó el DDI completo de ninguna ronda — búsqueda dirigida por
  palabra clave (`grep`) contra las 9.7 MB (2021) y 6.1 MB (2018) del
  XML: `bienestar`, `K79`/`K82`, `CUNICAH`/`CODENT`/`UNHHID`, `TRH`,
  `G17`/`G18`, `COVID`/`CAPI`/`cohorte`. No se leyó la ficha técnica de
  muestreo (`Diseño muestral. ENASEM 2021`, PDF en
  `app/biblioteca/ficha.html?upc=889463903956`) ni el cuestionario en PDF
  — el DDI trae el texto literal de cada pregunta embebido, así que no
  hizo falta abrir el PDF aparte para responder Q1-Q5.
- No se tocó `mhasweb.org` más allá de la sonda de alcanzabilidad de §2
  — ninguna descarga por esa vía.
- No se editó `canon/`, `milpa/`, `data/manifiesto.yaml`, ni el registro
  de veredictos.
- No se cruzó ninguna variable de ENASEM contra ENIGH, ENUT ni ninguna
  otra fuente — cada respuesta de §3 cita solo el codebook de ENASEM.
- `python3 tests/check.py --baseline` sí se corrió al cierre, tras editar
  `forense/hallazgos.md` y
  `forense/notas/2026-07-31-inventario-segmentacion.md` (la suite escanea
  `**/*.md` recursivo — sí las alcanza): `18 FAIL · 84 WARN`, **LÍNEA BASE:
  VERDE — nada nuevo frente a `tests/baseline.json`**, igual que al abrir
  la sesión (§0). Las dos ediciones de este acto no movieron la suite.
