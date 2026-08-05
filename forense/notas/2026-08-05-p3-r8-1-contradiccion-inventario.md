# P3 · La contradicción de R8.1 — verificación, análisis de Umbral y clasificación

*5 de agosto de 2026, ~12:59 hora local del repo (UTC-6, `TZ=America/Mexico_City`). Encargo P3, mesa
#20. Rama `claude/r8-1-inventory-contradiction-c1wcu2`, clon existente en
`/home/user/Modelado-Mexicano` (no se clonó uno nuevo). Entorno: `cloud_default`
(`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`), sonda de red saltada por diseño del acto.*

---

## §0 · Arranque — las cinco líneas, y la diferencia de SHA

1. **Repo.** Clon existente en `/home/user/Modelado-Mexicano` (no home). No se clonó nada nuevo.
   `git log -1 --format="%h %s"` al abrir: `3de5a28 Merge pull request #124 from
   Josanoforo/claude/sellar-conf06-adr64-ygbaqx`. `git status`: limpio, en la rama designada
   `claude/r8-1-inventory-contradiction-c1wcu2`. Un solo worktree (`git worktree list`), no se creó
   ninguno adicional.
2. **SHA.** El encargo se redactó contra `a7f807e`. `git fetch origin main` trajo `b93ffc6..3de5a28`.
   `git merge-base --is-ancestor a7f807e origin/main` confirma que `a7f807e` es ancestro directo —
   **`main` avanzó 3 commits** desde la base declarada (`git rev-list a7f807e..origin/main --count` =
   `3`), el último de ellos `7d590df` **ENCARGO M-5: sella `conf.06` con ADR-64** (relevante para §4
   más abajo: cambia el estado de R8.3 respecto a lo que el encargo pudo haber asumido). La rama de
   trabajo ya estaba sincronizada con `origin/main` en `3de5a28` al momento de empezar — no fue
   necesario re-derivar nada, se reporta la diferencia por disciplina.
3. **`data/raw`.** Ausente (`ls data/raw` → `No such file or directory`). No se usa en este acto — no
   es paro.
4. **Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` — valor correcto en la nube
   (ADR-59(b)). Sonda de red saltada, por diseño: este acto no toca red.
5. **Espejo.** No se derivó ninguna cifra del espejo del proyecto. Toda cifra de esta nota sale del
   clon anterior, con el comando a la vista en cada sección.

**Concurrencia viva** (`git branch -r`, `git fetch origin` sin filtrar): solo existe
`origin/claude/r8-1-inventory-contradiction-c1wcu2` (esta rama) entre las remotas. Ninguna rama de
A5, P2 o CORRIDA-IDG3 es visible desde este clon en el momento de este acto — se pega cruda la
salida, sin inventar concurrencia que no se ve:

```
$ git branch -r | grep -iE "a5|p2|idg3|r8|contra"
  origin/claude/r8-1-inventory-contradiction-c1wcu2
```

---

## §1 · Las dos citas, verificadas por línea

**Cita 1 — `forense/cruce-catalogo-fichas-v2_0.md:91`**, verificada carácter por carácter:

```
| R8.1 | Contribución ≥60% sostenida ≥2 años sin sanción/monitoreo, fuera de usos y costumbres |
Ninguna con inventario de comités | — | — | — | **NO EXISTE** — inventario de comités con/sin
mecanismo de sanción. Ninguna de las 6 clases nuevas lo cubre (no hay padrón ni registro
administrativo de comités vecinales identificado en el barrido). |
```

Coincide exacto con lo transcrito en §0 del encargo. **Confirmada.**

**Cita 2 — `data/inventarios/inventario_fuentes_capital_social_mexico.md:258`**, verificada:

```
| Registros de comités de contraloría social y comités de obra | Secretaría de Bienestar,
Secretaría de la Función Pública | Publicación como bases descargables; continuidad tras las
reorganizaciones de 2019–2023 |
```

Coincide exacto con lo transcrito en §0 del encargo. **Confirmada.**

**Pero el encargo omite el encabezado bajo el que vive la cita 2**, y esa omisión es el hallazgo
central de esta nota (desarrollado en §3). Línea 258 no vive en el cuerpo numerado del inventario
(entradas `## 1.`–`## 14.`): vive dentro de una sección aparte, empezando en la línea 240:

```
$ sed -n '240,244p' data/inventarios/inventario_fuentes_capital_social_mexico.md
# Fuentes que se sospecha existen pero no pudieron confirmarse

Pistas de búsqueda, no afirmaciones. Ninguna fue verificada.

| Fuente probable | Institución probable | Qué falta verificar |
```

La columna donde vive el texto citado por el encargo ("Publicación como bases descargables;
continuidad tras las reorganizaciones de 2019–2023") se llama **"Qué falta verificar"**, no
"Contenido" ni "Descripción". El encargo la transcribe con la forma de una descripción confirmada;
en el archivo real es la lista de lo que **todavía no se sabe** sobre esa fuente. La cita, tomada
literalmente, es exacta. Leída con su encabezado, dice algo más débil que lo que el encargo implica
al oponerla a la cita 1. Esto no dispara el "PARA" de §2 (la cita existe y dice exactamente eso) —
pero cambia el análisis de §3 de raíz, así que se reporta aquí, antes de continuar, como pide la
regla de "verificar antes de obedecer".

---

## §2 · Premisas verificadas

- `git fetch` hecho, diferencia de `main` reportada arriba (§0.2).
- Las dos citas de §0 del encargo existen y dicen lo que se transcribe (§1). Ninguna dispara el PARO.
- **R8.1 no tiene veredicto `RX.Y` archivado.** Receta de T18 (`tests/check.py:684`, mismo regex
  `` `(R\d+\.\d+)`\s*→\s*veredicto\s*`([A-E])` `` corrido contra el bloque
  `## Registro de veredictos archivados` de `hitoD-preregistro-v2_0.md`, no contra prosa):

  ```
  $ python3 -c "
  import re, glob
  h = sorted(glob.glob('forense/hitoD-preregistro-v*.md'))[-1]
  texto = open(h, encoding='utf-8').read()
  m = re.search(r'^## Registro de veredictos archivados.*\$', texto, re.M)
  bloque = texto[m.end():]
  V = re.compile(r'\`(R\d+\.\d+)\`\s*→\s*veredicto\s*\`([A-E])\`')
  found = [mm.groups() for l in bloque.split(chr(10)) for mm in [V.search(l)] if mm]
  print('R8.1 archivado?', any(f[0]=='R8.1' for f in found))
  print('R8.3 archivado?', any(f[0]=='R8.3' for f in found))
  "
  R8.1 archivado? False
  R8.3 archivado? False
  ```

  Ninguna aparece. No hay PARO por este motivo.

---

## §3 · El Umbral de R8.1, transcrito completo, y el análisis condición por condición

`forense/hitoD-preregistro-v2_0.md:216-224`, transcrito íntegro, sin resumir:

> ## R8.1 · Monitoreo + sanción → contribuye `[FUERTE]`
> **SI** hay comité con liderazgo confiable + monitoreo + sanción visible **ENTONCES** contribuye;
> **SI** no hay monitoreo ni sanción **ENTONCES** free-riding racional
>
> **Falsador.** Bien público mexicano con contribución alta y sostenida **sin monitoreo ni
> sanción**.
> **Umbral.** Tasa de contribución **≥60%** durante ≥2 años sin mecanismo de sanción identificable
> ni liderazgo con capacidad de excluir.
>
> 🚫 **Frontera obligatoria:** la **faena/tequio bajo usos y costumbres** queda **fuera del modelo**
> (ADR-10). No es un caso de este dominio: es obligación institucional de otro orden. **Usarla como
> contraejemplo sería error categorial** y el veredicto no contaría. El falsador debe buscarse en
> **pueblo mestizo o urbano**.
>
> **A** ≥60% sostenido sin sanción, fuera del sistema comunal · **B** contribución alta con sanción
> informal no registrada (presión vecinal cuenta como sanción) · **C** exigiría inventario de
> comités con y sin mecanismo · **D** posible.

### Condición por condición, contra el candidato (`Registros de comités de contraloría social y
comités de obra`, Secretaría de Bienestar / SFP)

| Condición del Umbral | Qué pide | Qué ofrece el candidato, hasta donde se puede leer | ¿Coincide? |
|---|---|---|---|
| Unidad de observación: comité individual | Necesita poder identificar comités concretos, no un agregado | El inventario no dice la unidad — la columna disponible es "qué falta verificar", no "granularidad". No confirmado. | **No determinable por lectura** |
| Tasa de contribución ≥60% de los miembros/vecinos | Necesita una variable de comportamiento — cuánta gente contribuye al bien público del comité | Un **registro administrativo de comités** (su existencia, institución responsable, fecha de alta/reorganización) es, por diseño de ese tipo de instrumento, un padrón de organizaciones — no una encuesta de comportamiento de sus miembros. Nada en la cita ni en el resto de la ficha del inventario sugiere que capture tasa de participación. | **Fuerte sospecha de no, no confirmable sin abrir la base** |
| Sostenida ≥2 años | Necesita serie temporal o al menos dos cortes | La cita solo promete "continuidad tras las reorganizaciones de 2019–2023" como algo **por verificar**, no como hecho confirmado | **No determinable por lectura** |
| Sin mecanismo de sanción identificable ni liderazgo con capacidad de excluir | Necesita clasificar comités como *con* o *sin* sanción (el criterio C de la propia ficha: "exigiría inventario de comités **con y sin** mecanismo") | "Comité de contraloría social" es, por definición institucional (Ley General de Desarrollo Social / Reglas de Operación de Bienestar), un cuerpo ciudadano cuya función es **vigilar/fiscalizar el ejercicio de recursos públicos** — es decir, es él mismo un mecanismo de vigilancia, no un comité vecinal neutral que pueda o no tener sanción sobre sus propios contribuyentes. Esto es una discordancia de **tipo de entidad**, no solo de variable faltante — y es leíble sin abrir el instrumento. | **Discordancia de dominio, detectable por lectura** |
| Fuera de usos y costumbres (frontera ADR-10) | Debe ser pueblo mestizo o urbano, no sistema comunal-indígena | No hay elemento en la cita que confirme ni descarte esto — Bienestar/SFP operan en todo el país | **No determinable por lectura** |

**Lectura de conjunto.** El candidato falla al menos una condición por razón de **tipo**, no solo
por dato faltante: un "comité de contraloría social" está definido institucionalmente como
mecanismo de vigilancia sobre el gasto público, mientras que el Falsador de R8.1 pide un comité que
administra un bien público comunitario y cuya membresía sí o no responde a un mecanismo de sanción
interno. Aun si el registro existiera confirmado y fuera descargable mañana, no es evidente que esté
midiendo el fenómeno que el Umbral pide — sería, en el mejor caso, una fuente para estudiar *otro*
tipo de comité (vigilancia de programas sociales), no el free-riding en la provisión de un bien
público comunitario. Esto **no se puede resolver del todo sin ver el instrumento** (podría, por
ejemplo, incluir comités de obra que sí administran una faena o cooperación no de contraloría), pero
la discordancia de tipo entre "comité fiscalizador" y "comité proveedor de bien público con
free-riding" es suficientemente fuerte para no tratar este candidato como un lead limpio.

---

## §4 · La respuesta de §3 del encargo, con argumento

**Respuesta: (c) — nadie corrió el mecanismo de resolución contra este candidato**, con dos matices
que ninguna de las otras tres respuestas captura:

1. **No es (a).** No se puede decir que "el candidato sirve y R8.1 debe reclasificarse" porque el
   candidato mismo **no está confirmado que exista** en forma descargable/usable — la propia tabla
   donde vive dice explícitamente "Pistas de búsqueda, no afirmaciones. Ninguna fue verificada." Afirmar
   (a) sería inflar un lead no verificado a un hallazgo confirmado — exactamente el error que costó
   ENASEM/ENSANUT/CLUES/Cero Desabasto el 4/ago, solo que en la dirección contraria (aquí sería
   *sobre*-confiar en un candidato débil en vez de subestimar uno fuerte).
2. **No es (b) en sentido estricto.** (b) dice "existe el registro y no satisface el Umbral" — pero
   la existencia misma del registro **no está confirmada**. Sí se puede argumentar una discordancia
   de tipo por lectura (§3, última fila de la tabla) sin abrir el instrumento — y esa es la parte
   fuerte de esta nota — pero declarar (b) completo exigiría primero confirmar que la base existe y
   después leer sus variables, dos pasos que este acto no puede dar sin red.
3. **No es (d).** El inventario no está mal. Es honesto y se etiqueta a sí mismo correctamente: la
   sección se llama "Fuentes que se sospecha existen pero no pudieron confirmarse" y la fila declara,
   en su propia columna, qué falta verificar. No describe algo distinto de lo que su título promete
   — el problema no está en el inventario, está en cómo el encargo citó una fila de esa sección **sin
   el encabezado** que la califica.
4. **Es (c), con el motivo exacto nombrado:** el candidato está catalogado (no inventado, no fantasma)
   pero **nadie ha ido a verificar si la base de "Registros de comités de contraloría social y comités
   de obra" existe públicamente, qué unidad de observación tiene, y si permite clasificar comités como
   con/sin sanción** — el criterio **C** que la propia ficha de R8.1 ya nombraba antes de este acto
   (`hitoD-preregistro-v2_0.md:224`: "**C** exigiría inventario de comités con y sin mecanismo").

**Las palabras exactas que distinguen (c) de las otras tres, para que quede sin ambigüedad:**
*el recurso está catalogado como sospecha sin confirmar, nadie ha verificado si existe ni qué
contiene, y no se puede decidir si satisface el Umbral sin hacerlo* — no es "existe y sirve" (a), no
es "existe y no sirve" (b, aunque hay indicios fuertes de discordancia de tipo que apuntan hacia
ahí), y no es "el inventario describe mal la fuente" (d, el inventario es honesto sobre su propia
incertidumbre).

**Por qué la "contradicción" del encargo se disuelve, no solo se clasifica.** Más allá de la
respuesta (c), hay una razón mecánica, verificable, de por qué el cruce v2.0 nunca vio este
candidato — no es un descuido humano aislado, es un límite de diseño del pipeline:

- La definición operativa de `NO EXISTE` en el propio cruce (`cruce-catalogo-fichas-v2_0.md:36`) es
  explícita y acotada: *"ninguna fuente de ninguna de las **6 clases** de
  `inventario_fuentes_clase-fuente-mexico.md`"* — un archivo específico (compilado 4/ago, Encargo AA),
  no "ningún inventario de todo `data/inventarios/`". `inventario_fuentes_capital_social_mexico.md`
  es un inventario **distinto y anterior** (compilado 30/jul), fuera de esa definición por diseño.
- Más abajo en el pipeline, `data/catalogo-fuentes-v2_0.md` (el insumo real que el cruce cita) se
  regenera con `tests/catalogo.py`, que **separa explícitamente** las secciones "Fuentes que se
  sospecha..."/"Fuentes sospechadas" en un bucket `sospechadas` distinto del bucket `fuentes`
  (`tests/catalogo.py:45,60`) — y ese bucket `sospechadas` **nunca aparece** en
  `data/catalogo-fuentes-v2_0.md` ni se usa en `tests/dedup.py`:

  ```
  $ grep -n "sospechad" data/catalogo-fuentes-v2_0.md tests/dedup.py
  (sin resultados)
  ```

  Es decir: **toda entrada catalogada como "sospecha sin confirmar", en cualquiera de los cuatro
  inventarios que tienen esa sección (migración, capital social, cultura/valores, trámites/Estado —
  ver §5), queda estructuralmente invisible para cualquier veredicto del cruce que se apoye en
  `catalogo-fuentes-v2_0.md`.** No es que el barrido de R8.1 haya sido descuidado — es que el
  candidato vive en una capa del pipeline que ningún cruce, tal como está construido, puede alcanzar.
  Esto no cambia la respuesta (c) — el candidato sigue sin resolverse — pero sí cambia el diagnóstico:
  no es un error puntual de un acto, es un gap estructural del pipeline que probablemente reaparecerá
  en otros dominios si alguna vez una "sospecha sin confirmar" resulta relevante para otra ficha.

---

## §5 · Qué haría falta para resolverlo — mecanismo nombrado para el acto siguiente

Esto es (c): se nombra el mecanismo, no se ejecuta aquí (exige red, fuera del perímetro de este
acto).

1. **Verificar existencia y acceso.** Buscar si Secretaría de Bienestar y/o Secretaría de la Función
   Pública publican, en datos.gob.mx o en sus propios portales, una base descargable de "comités de
   contraloría social" y/o "comités de obra" — nombres institucionales a probar: Sistema de
   Información de la Contraloría Social (SICS), Padrón de Comités de Contraloría Social, o el
   sucesor tras la reorganización SFP→Función Pública/Bienestar de 2019–2023 que la propia entrada
   del inventario señala como incierta.
2. **Si existe: verificar unidad de observación.** ¿Es por comité individual (con domicilio/localidad/
   folio) o solo un agregado nacional/estatal? Sin unidad de comité individual, no sirve para el
   Umbral aunque exista.
3. **Si la unidad es comité individual: verificar si captura contribución.** Ningún registro
   administrativo de "alta de comité" mide, por diseño típico, cuánto contribuyen los vecinos — buscar
   si el instrumento tiene un componente de seguimiento/reporte (actas de asamblea, listas de
   asistencia, aportaciones registradas) más allá del acto de constitución del comité.
4. **Verificar si distingue con/sin mecanismo de sanción** (criterio **C** de la ficha, ya
   pre-registrado) — esto es lo más improbable de encontrar en un registro administrativo de este
   tipo, porque "contraloría social" es en sí misma una función de vigilancia impuesta por el programa
   social de origen, no una propiedad variable del comité.
5. **Resolver la discordancia de tipo de §3 antes que nada:** confirmar con la normativa pública
   (Reglamento de la Ley General de Desarrollo Social, Lineamientos de Contraloría Social de
   Bienestar) si "comité de contraloría social" es, por definición, un comité que vigila el ejercicio
   de un programa social (lo que lo excluiría de la unidad de análisis de R8.1) o si "comités de
   obra" (el segundo término de la fila del inventario) es una categoría distinta y más cercana a un
   comité vecinal de gestión de un bien público concreto (tequio urbano, faena de infraestructura
   fuera de usos y costumbres) — la fila del inventario junta ambos términos sin distinguirlos.

Ninguno de estos cinco pasos requiere abrir microdato de encuesta ni tocar `canon/`/`milpa/` — es
búsqueda de red + lectura de normativa pública. Es, tal como dice el encargo, un acto de Ubuntu con
otro perímetro.

---

## §6 · Barrido propio de las filas `NO EXISTE`, con receta a la vista

**Receta:** parsear la columna Veredicto de las 7 tablas `§3.x` de
`forense/cruce-catalogo-fichas-v2_0.md`, quedarse con las filas cuyo primer token es `NO EXISTE`, y
para cada una revisar si su "Fuente candidata" declarada es "Ninguna" (o variante) y si, pese a eso,
algún inventario en `data/inventarios/` (los 11, no solo `inventario_fuentes_clase-fuente-mexico.md`)
trae un candidato — confirmado o "sospechado" — que la fila no cita.

```
$ grep -n "NO EXISTE" forense/cruce-catalogo-fichas-v2_0.md
```

14 filas primarias con veredicto `NO EXISTE` (excluyendo menciones de prosa en la leyenda §Veredictos,
el §Resumen que se cita a sí mismo, y "Lo que este documento no hace" — ninguna de esas es fila de
tabla):

`R1.1` (con reserva declarada) · `R1.3` (2ª fila) · `R1.4` · `R2.1` · `R2.2` · `R4.1` (1ª fila) ·
`R7.3` (el diseño, no la fuente) · `R7.4/R7.5` · `R8.1` · `R8.2` · `R9.1` (2ª fila, variable
específica) · `R10.1` · `R10.2` · `R10.3`.

Para cada una, verificación contra `data/` de hoy (`grep -rni` por tema — receta cruda, sin
inventar coincidencias):

| Ficha | Tema | ¿Candidato en algún inventario, confirmado o "sospechado"? |
|---|---|---|
| R1.1 | Fondos de Aseguramiento Agrícola/AGROASEMEX | `grep -rni "AGROASEMEX\|Aseguramiento Agrícola" data/` → 0. Ninguno. |
| R1.3 (2ª) | Canal de alta de fintech propietario | Por diseño de clase (Regulador no-INEGI/CNBV no publica esto). Ninguno. |
| R1.4 | Panel de consumo D/E por marca | `grep -rni "panel de consumo" data/` → 0. Ninguno. |
| R2.1 | Clima organizacional / reporte de errores | `grep -rni "clima organizacional" data/` → 0. Ninguno. |
| R2.2 | Rotación/productividad, liderazgo | STPS existe pero es PDF agregado por entidad, sin microdato — descartado por granularidad, no ausencia. Ninguno de tipo comité/individuo. |
| R4.1 (1ª) | Panel/evento fechado, farmacia-consultorio | La propia fila ya cita SINERHIAS como candidata parcial no verificada — ya hedged, no es hallazgo nuevo. |
| R7.3 | Diseño RDD listo | La fila ya reconoce PUB+INE como insumos separados — es hueco de diseño, no de fuente no vista. |
| R7.4/R7.5 | Registro de eventos de protesta/autodefensa | `grep -rni "protesta\|autodefensa" data/inventarios/inventario_fuentes_seguridad_justicia_mexico.md` → 0. Revisadas también las 4 secciones "sospechadas" del §6 más abajo — ninguna trae registro de eventos. Ninguno. |
| **R8.1** | **Inventario de comités con/sin sanción** | **Sí — `inventario_fuentes_capital_social_mexico.md:258`, sección "sospechadas", no citado por la fila.** |
| R8.2 | Tandas digitales, plataforma propietaria | `grep -rni "tandas" data/` → 0. Ninguno. |
| R9.1 (2ª) | Variable "no consultó a nadie" dentro de ENSANUT | No es hueco de fuente, es de diseño de cuestionario dentro de un instrumento que sí existe. No aplica. |
| R10.1 | Estudio académico Félix-Brasdefer | No es dato de encuesta/registro por diseño. No aplica. |
| R10.2 | Retro pública/privada, dato organizacional | Mismo vacío de clase que R2.1/R2.2. Ninguno. |
| R10.3 | Testificar tras protección a testigos | Bloqueo ético declarado por la ficha, no ausencia de dato. No aplica. |

**Resultado del barrido propio: confirmo que solo hay una — R8.1 — entre las 14 filas `NO EXISTE`.**
Además, para las cuatro filas cuyo tema podría en principio cruzar con una sección "sospechada"
(R1.1, R7.4/R7.5, R2.1/R2.2, R8.2), revisé el contenido de las cuatro secciones "sospechadas" que
existen en todo `data/inventarios/` (`grep -ln "Fuentes que se sospecha\|Fuentes sospechadas"
data/inventarios/*.md` → migración, capital social, cultura/valores/opinión,
trámites/Estado) y ninguna trae una entrada relevante a esos temas. **Confirmo también el barrido ya
hecho por el acto A4 (`forense/notas/2026-08-04-a4-auditoria-reparto-cruce-v2_0.md` §4), llegando
independientemente a la misma cifra y a la misma fila excepcional (R8.1)** — con la extensión
adicional, no presente en A4, de haber verificado *por qué* mecánicamente ninguna sección
"sospechada" de ningún inventario puede alcanzar al cruce (§4 de esta nota, el hallazgo de
`tests/catalogo.py`).

**Confirmando con las palabras del encargo: solo hay una.** No se colapsa este resultado con "no hay
más contradicciones en absoluto" — solo se afirma que, dentro de las 14 filas `NO EXISTE` del cruce
v2.0 y los 11 inventarios de `data/inventarios/` de hoy, ninguna otra fila tiene un candidato
(confirmado o sospechado) que no haya citado.

---

## §7 · Estado de R8.3 tras el cierre de `conf.06`

`R8.3` (`hitoD-preregistro-v2_0.md:236-246`, `cruce-catalogo-fichas-v2_0.md:93` — "NO ENLAZA /
bloqueado por conflicto de cifras") **no tiene veredicto `RX.Y` archivado** (verificado en §2, misma
receta de T18). `conf.06` se cerró **después** de la base declarada del encargo (`a7f807e`), en el
merge `7d590df` que ya está en `main` (§0.2) — `ENCARGO M-5: sella conf.06 con ADR-64`.

**Texto del sello, `forense/hallazgos.md:137`, ADR-64(e), transcrito:**

> **`R8.3`** — condición B se levanta, sigue sin falsador (marca C3 vigente, condición A), veredicto
> `D` no cambia, no se adjudica.

**Qué se levanta:** la condición **B** de R8.3 — dejar de haber cinco (en realidad seis, per C-06a)
cifras de confianza interpersonal en conflicto que invaliden cualquier resultado que se apoye en
ellas. `conf.06` está `CERRADO` por ADR-64: 21.8%=`AP5_1_1` · 32.1%=`AP5_1_3` (vecinos) ·
62.1%=`AP5_1_2`, los tres a corte ≥8/10, reproducidos contra microdato ENCUCI real por el acto C-06b.

**Qué sigue bloqueado:** la condición **A** — el Falsador de R8.3 exige un dato que mida disposición
a transar con desconocidos **por nivel de enforcement** (alto vs. bajo), y la advertencia de C-06a
sigue vigente: el dato candidato de ENCUCI (`radio_confianza`) tiene **marca C3 (circular)** contra
la regla exacta que R8.3 prueba (`cooperacion.confianza.puente_personal`,
`modelo-decision-v4_0.md:498`) — su desenlace observado en Tabla B es el mismo reactivo `AP5_1_2`
(`milpa/procedencia.yaml:226-228`). Reconciliar `conf.06` limpia el ruido de magnitud entre fuentes,
pero **no le da a R8.3 un falsador propio**: sigue sin existir una fuente que mida enforcement
alto/bajo cruzado con disposición a transar con desconocidos, fuera del reactivo circular.

**Confirmando la advertencia de C-06a explícitamente, sin prometer un desbloqueo que no ocurre:**
"el efecto matiza hacia abajo, no hacia arriba" se cumple — R8.3 sigue con veredicto `D` (no
adjudicado, no cambia), sigue "NO ENLAZA / bloqueado", y lo único que cambia es que el bloqueo ya no
tiene la etiqueta doble (conflicto de cifras + circularidad): ahora es solo circularidad (marca C3).
No hay ADR nuevo que este acto pueda o deba sellar sobre R8.3 — CERRADO `conf.06`, R8.3 sigue abierta.

---

## §8 · Recomendación a mesa (recomendación, no decisión)

Con la clasificación (c) de §4 y el hallazgo estructural del pipeline (§4, última parte), la
recomendación de esta nota es:

**No procede un cruce v3.0 que reclasifique R8.1 todavía.** Reclasificar exigiría primero resolver
el mecanismo de §5 (verificar existencia/contenido del registro vía red) — sin eso, cualquier
reclasificación sería tan prematura como declarar (a) directamente. Lo que sí procede,
recomendado pero no decidido aquí:

1. **Un acto de Ubuntu** (con red, perímetro propio) que ejecute los cinco pasos de §5 contra
   "Registros de comités de contraloría social y comités de obra" — el resultado de ese acto sí
   alimentaría una fila de excepción o una nota de v2.1, no un cruce completo nuevo.
2. **Considerar, aparte de R8.1, si vale la pena una revisión ligera de si `tests/catalogo.py` debería
   exponer el bucket `sospechadas` de alguna forma visible para actos de cruce futuros** — no como
   fuente confirmada, sino como lista de "candidatos sin resolver" consultable — para que este tipo de
   gap de tercer tipo no dependa de que un acto de auditoría lo encuentre por lectura manual, dominio
   por dominio. Esto es una recomendación de infraestructura, mesa decide si amerita su propio
   encargo.
3. **La nota basta por sí sola** para dejar registrado el estado de R8.1 (gap de tercer tipo, no
   contradicción real) y de R8.3 (condición B levantada, A sigue bloqueada) — no hace falta ningún
   otro acto de lectura antes de que el de red corra.

---

## Lo que este acto no hizo

No editó `forense/cruce-catalogo-fichas-v2_0.md` (append-only) ni ningún inventario de
`data/inventarios/`. No adjudicó veredicto para `R8.1` ni `R8.3`. No selló ningún ADR. No tocó
`canon/`, `milpa/`, `tests/` ni `data/`. No abrió red ni microdato — todo el análisis de §3-§7 sale de
lectura de archivos ya presentes en el clon. Sesión limpia para pre-registrar contra cualquier
fuente.
