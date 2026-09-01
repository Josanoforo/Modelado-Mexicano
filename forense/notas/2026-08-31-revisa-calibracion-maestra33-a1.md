# Calibración de `/revisa` · corrida post-hoc sobre `PR #414`

**P3** de `ACTO MAESTRA33-E5 · REVISOR-PR-1`
(`forense/encargos/2026-08-31-MAESTRA33-E5-REVISOR-PR-1.md`). 31/ago–1/sep/2026 (el acto cruzó la medianoche; los archivos
conservan el prefijo de fecha del encargo), entorno **NUBE**, clon `/home/user/Modelado-Mexicano`, rama
`claude/revisor-pr-automatizado-yg8d0v`.

**Modo `--post-hoc`: no se comentó nada en GitHub.** El `PR #414` está
fusionado desde el 31/ago; resucitar su conversación con un veredicto
tardío no le sirve a nadie. El veredicto vive aquí y sólo aquí, que es
lo que la skill manda para este modo (`.claude/commands/revisa.md` §1.4).

---

## §0 · Qué prueba esta calibración, y qué no

**Prueba** que la lista de diez puntos, tal como quedó escrita, es
**ejecutable** —cada punto se traduce en comandos que corren— y que
**atrapa cosas reales** en un PR que ya pasó por mesa.

**No prueba** que la lista sea completa: un PR no es una muestra. Y no
prueba que sus pesos estén bien calibrados; eso lo dirá el falsador a un
mes (`forense/agente-revisor-v1_0.md` §3), no esta nota.

Y una disciplina que esta nota se aplica a sí misma, porque es la que su
propio punto 2 exige: **la lista se congeló en el commit `aa9a1bb`,
antes de que esta corrida existiera.** Lo que la calibración encontró
incómodo se reporta; no se legisla hacia atrás. Si mesa decide que algún
peso está mal puesto, ése es su commit, después de éste, y con su razón
escrita — no una edición silenciosa de la spec para que el resultado
cuadre.

---

## §1 · El objeto y las tres identidades

| | |
|---|---|
| PR | `#414` · `ACTO MAESTRA33-A1 · AGENTE-ADQUISICION-1` |
| merge | `737a851` |
| `BASE` (`^1`) | `26cb24c` (`PR #413`) |
| `HEAD` del PR (`^2`) | `1efd335` |
| encargo | `forense/encargos/2026-08-31-MAESTRA33-A1-AGENTE-ADQUISICION-1.md` |
| reporte del ejecutor | `forense/notas/2026-08-31-agente-adquisicion-1-cierre.md` + `ADR-242` |

En post-hoc la vista previa **es** el merge que ya ocurrió, así que los
comandos de la skill se traducen: el diff del PR es
`git diff 737a851^1 737a851`, sus commits son `737a851^1..737a851^2`, y
el contenido de un archivo fusionado sale de `git show 737a851:<ruta>`.

```
$ git log --oneline --reverse 737a851^1..737a851^2
35fae4b 0-bis A.3: archiva encargo verbatim — ENCARGO MAESTRA33-A1 AGENTE-ADQUISICION-1
7a53d26 P1: tabla viva data/cola-adquisicion-v1_0.tsv — absorbe las 5 colas de agosto
e1d01b6 P2: skill /adquiere — camina la cola por prioridad, adquisición programática
db5a9bc Fusiona origin/main (PR #413, ACTO MAESTRA33-E2 AGENTE-DESPACHO-1)
7bc20dd P3: primera caminata (15 de FP-17 + radio_confianza) + cascada ADR-242
1efd335 hallazgos.md: una tabla de cola queda stale cuando el complemento no escribe de vuelta
```

---

## §2 · Los diez puntos

### Punto 1 · Encargo archivado verbatim (A.3) — **`RESERVA`**

```
$ git log --oneline --reverse 737a851^1..737a851^2 | head -1
35fae4b 0-bis A.3: archiva encargo verbatim — ENCARGO MAESTRA33-A1 AGENTE-ADQUISICION-1

$ git log --oneline 737a851^1..737a851^2 -- forense/encargos/2026-08-31-MAESTRA33-A1-AGENTE-ADQUISICION-1.md
7bc20dd P3: primera caminata (15 de FP-17 + radio_confianza) + cascada ADR-242
35fae4b 0-bis A.3: archiva encargo verbatim — ENCARGO MAESTRA33-A1 AGENTE-ADQUISICION-1

$ git diff 35fae4b 7bc20dd -- forense/encargos/2026-08-31-MAESTRA33-A1-AGENTE-ADQUISICION-1.md | grep -E '^[+-]' | grep -v '^[+-][+-]'
+
+## CONSUMIDO
+
+Ejecutado por `ACTO MAESTRA33-A1 · AGENTE-ADQUISICION-1`, 31/ago/2026, worktree `/home/p…
```

El 0-bis es el primer commit; el segundo toque al encargo es **puro
`+`**, todo después de `## CONSUMIDO`, **cero líneas borradas** del
cuerpo. Los dos mecánicos pasan limpio.

La coherencia con el reporte deja **un `RESERVA`**. `P1` manda absorber
**las 5 colas de agosto**; se absorbieron **cuatro**:

```
$ for c in aperturas academico civil general oficial; do
    git show 737a851:data/cola-adquisicion-v1_0.tsv | awk -F'\t' -v p=$c 'NR>1 && $6 ~ ("cola-"p) || $6 ~ ("cola-ext-"p)' | wc -l; done
0   ← aperturas      (data/cola-aperturas-externas-2026-08-06.tsv, 15 filas)
3   ← academico
2   ← civil
3   ← general
9   ← oficial
```

Y el reporte **no lo oculta**: dice *"los cuatro `cola-ext-*`"*, no
"los cinco". Por eso **no** es el caso `BLOQUEA` del punto 2.1 —el
reporte no afirma algo que el diff no muestra—. Lo que falta es la línea
que explique **por qué** la quinta aportó cero, y la razón es buena y
está a la vista: `cola-aperturas-externas` tiene **otro esquema**
(`orden · fuente · objetos · accion_minima · impacto · probabilidad ·
costo …`), sin `url` ni estado de adquisición; no es una cola de
descarga. Mención de "apertura" en la nota de cierre: **0** sobre 1
archivo examinado (A.13). El arreglo es una frase.

*(Nota de método: un agente independiente de la corrida de §5 calificó
esto `BLOQUEA`. Se bajó a `RESERVA` tras leer la nota entera y comprobar
que dice "los cuatro". Dos de tres lentes adversariales coincidieron en
bajarlo.)*

### Punto 2 · Orden de commits, spec antes de resultados — **NO-APLICA**

```
$ git show 737a851:forense/encargos/…-A1-….md | grep -oE 'CONTADOR:.*'
CONTADOR: payloads OBTENIDO 0→N (adquisición, no medición — declarado).
```

El propio encargo declara que **no mide**: adquiere. El punto 2 sólo
aplica en actos que miden, así que `NO-APLICA`, con esa razón.

### Punto 3 · Perímetro declarado vs. tocado — **1 `BLOQUEA` · 1 `RESERVA`**

Declarado: `data/cola-adquisicion-v1_0.tsv`, `data/manifiesto.yaml`,
`data/raw` (payloads), `.claude/commands/adquiere.md`, `forense/notas`
propia, archivo A.3, tablero, cascada.

```
$ git diff --name-only 737a851^1 737a851 | sort
.claude/commands/adquiere.md
canon/estado-programa-v1_10.md
canon/gobernanza-v1_15.md
canon/registro-rotulos.tsv
data/cola-adquisicion-v1_0.tsv
forense/encargos/2026-08-31-MAESTRA33-A1-AGENTE-ADQUISICION-1.md
forense/firmas-pendientes.tsv
forense/hallazgos.md
forense/notas/2026-08-31-agente-adquisicion-1-cierre.md
tests/check.py
```

Los cuatro de `canon/` y `tests/check.py` caen dentro de "cascada" —y
`tests/check.py` además **se declara en su propio diff**: *"Extension
minima de perimetro por desviacion mecanica"*, con su razón. Ése es
`RESERVA` por la regla, y de los benignos.

**`forense/hallazgos.md` es el hallazgo `BLOQUEA`.** Está tocado, no
está en el perímetro declarado, no es parte de la cascada de `/acto`
(los nueve pasos no lo nombran), y **no se declara en ninguna parte**:

```
# entrada ADR-242 aislada = líneas 4189..4205 de gobernanza en el merge
$ sed -n '4189,4205p' <gobernanza@737a851> | grep -ci 'hallazgos\.md'
0
$ git show 737a851:forense/notas/…-adquisicion-1-cierre.md | grep -ci 'hallazgos\.md'
0
```

Cero sobre **2** archivos examinados —el ADR y la nota de cierre—, más
el encargo (que tampoco lo nombra): **3 archivos** (A.13). La entrada
`ADR-242` tampoco trae bloque `Perímetro:`, que es la costumbre de la
casa y es donde el desborde se habría declarado.

Y conviene decir qué **no** es este hallazgo: el contenido añadido a
`hallazgos.md` —*"una tabla de cola con columnas de estado queda stale
cuando el acto complementario no escribe de vuelta"*— es un hallazgo
genuino y valioso. Nadie querría quitarlo. Lo que falta es **una línea
que lo declare**, y ése es el arreglo entero.

*(Disidencia registrada, y es el dato que el falsador `§3(b)` va a
querer: **2 de 3** lentes adversariales bajarían esto a `RESERVA`,
argumentando que el commit dedicado `1efd335` —cuyo título nombra el
archivo y lo que se le añadió— ya es declaración suficiente. Se mantiene
`BLOQUEA` porque la regla escrita pide declarar **el desborde con su
razón**, y un título que describe el contenido añadido no dice que el
archivo esté fuera del perímetro. Si mesa juzga que esto es un bloqueo
en falso, es el primero de los tres que `§3(b)` cuenta.)*

En la otra dirección: **`data/manifiesto.yaml` y `data/raw` están
declarados y no se tocaron** (0 archivos de cada uno en el diff). El
propio reporte lo explica —la caminata no obtuvo ningún payload nuevo—,
así que es `RESERVA` de la clase "el perímetro se declaró optimista",
no defecto.

### Punto 4 · Negativos con conteo de archivos (A.13) — **`RESERVA`**

El negativo portante del acto —que las 15 filas `EXISTE-NO-VERIFICADO`
que el encargo daba por vivas ya estaban en cero— **está bien hecho**:
se re-derivó con comando, se citó la fuente (`§4` de la nota de
`ACTO ADQ-15`) y se explicó por qué el `grep` crudo daba `42`. Los
negativos secundarios de la nota nombran su archivo pero no siempre
escriben el conteo. `RESERVA`, de la clase documental.

### Punto 5 · Toda cifra re-derivada — **1 `BLOQUEA`**

Re-derivadas **5** cifras del reporte; **4 confirman**, **1 no**.

Confirma (ejemplo, y es de las buenas):

```
$ git show 737a851:data/cola-adquisicion-v1_0.tsv | awk -F'\t' 'NR>1 && NF {print $6}' | sed 's/[:;].*//' | sort | uniq -c
     54 cola-adquisicion-2026-08-12.tsv
      9 cola-ext-oficial-2026-08-06.tsv
      3 cola-ext-general-2026-08-06.tsv
      3 cola-ext-academico-2026-08-06.tsv
      1 cola-ext-civil-2026-08-06.tsv
      2 data/universo-puertas-2026-08-14.tsv (FP-17…)
```

54 + 16 + 2 = **72**, y la nota dice exactamente eso, con los dos
nombres de las filas extra: *"56 heredadas … (las 54 originales +
`EXPERIMENTO_INFORMACION_ELECTORAL_2009` + `FINANZAS`)"*. Precisa.

**Y la que no confirma.** El reporte afirma el desglose
*"(21 `OBTENIDO`, 44 `PENDIENTE`, 6 `NO-ACCESIBLE`,
1 `NO-OBTENIDO-POR-ESTE-AGENTE`)"*. La tabla dice otra cosa:

```
$ git show 737a851:data/cola-adquisicion-v1_0.tsv | awk -F'\t' 'NR>1 && NF {print $2}' | sort | uniq -c | sort -rn
     43 PENDIENTE
     21 OBTENIDO
      6 NO-ACCESIBLE
      1 NO-OBTENIDO-POR-ESTE-AGENTE(15 intentos)
      1 NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)
```

**43 y 2**, no **44 y 1**. El total (72) cuadra en las dos versiones, así
que es **una fila reasignada**: `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO`,
la de los 15 intentos, que el reporte cuenta como `PENDIENTE` y la tabla
tiene como `NO-OBTENIDO-POR-ESTE-AGENTE`.

**No es staleness, y esto importa** — el reporte no quedó viejo respecto
de una tabla que cambió después. La fila nació así en el commit que creó
la tabla y no se movió nunca:

```
$ for c in 7a53d26 e1d01b6 db5a9bc 7bc20dd 1efd335; do
    git show $c:data/cola-adquisicion-v1_0.tsv | awk -F'\t' '$1=="BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO"{print $2}'; done
NO-OBTENIDO-POR-ESTE-AGENTE(15 intentos)   (las cinco veces)
```

Y en **el mismo commit** que escribió la cifra (`7bc20dd`), la tabla ya
decía 43/2. Es un conteo mal hecho en el momento de escribirlo, no un
desfase temporal. **Se propagó** al `## CONSUMIDO` del encargo archivado
(`44 PENDIENTE`), que es donde más caro sale, porque ese archivo es el
registro que después se audita.

Arreglo propuesto (una línea en dos sitios): corregir el desglose a
`21 / 43 / 6 / 2` en la nota de cierre y en el `## CONSUMIDO`.

**Y la segunda cifra que no confirma, que es la grave.** La fila `WVS`
declara `ids_manifiesto = (ausente)` y justifica el negativo así:
*"Verificado 31/ago: 0 de 489 `payload_id` del inventario coinciden con
wvs"*. Ese negativo se produjo **contra el universo equivocado**:

```
$ git show 737a851:data/manifiesto.yaml | grep -c 'payload_id'
0
$ git show 737a851:data/manifiesto.yaml | grep -c '^- id:'
794
```

`data/manifiesto.yaml` —el archivo que el propio encargo nombra como la
autoridad— **no tiene ningún campo `payload_id`**: tiene 794 entradas
con clave `id:`. El inventario de 489 `payload_id` que se consultó es
otro archivo. Y en el manifiesto:

```
$ git show 737a851:data/manifiesto.yaml | grep -A1 -iE '^- id:.*wvs' | grep -E '^\s*usado_para'
  usado_para: WVS7 Mexico 2018 -- cuestionario (espanol), doc. N5/N15
  usado_para: WVS7 Mexico 2018 -- informe de metodologia, doc. N5/N15
  usado_para: WVS7 Mexico 2018 -- ficha del equipo ejecutor
  usado_para: WVS7 Mexico 2018 -- diseno muestral, doc. N5/N15
  usado_para: Microdato WVS7 Mexico 2018, formato SPSS v5.1, cand. N5/N15
  usado_para: Microdato WVS7 Mexico 2018, formato Stata v5.1, cand. N5/N15
  usado_para: Microdato WVS7 Mexico 2018, formato CSV v5.1, cand. N5/N15
  usado_para: Microdato WVS7 Mexico 2018, formato Excel v5.1, cand. N5/N15
  usado_para: Microdato WVS7 Mexico 2018, formato ExcelTxt v5.0, cand. N5/N15
  usado_para: Microdato WVS7 Mexico 2018, formato CsvText v5.1, cand. N5/N15
```

**Diez entradas de WVS ola 7 México 2018, seis de ellas microdato**, en
seis formatos. El instrumento que la fila declara requerido —*"WVS OLA 7
MEXICO (2018) específicamente"*, por la batería `V102-V107`— ya estaba
adquirido y registrado. `(ausente)` es falso.

Un límite que esta corrida sí tiene, y se declara: **no puedo verificar
que los bytes estén en el corpus compartido**, sólo que el registro dice
que se adquirieron — `data/raw` no existe en este entorno de nube
(`ls data/raw/` → `No such file or directory`, **0 archivos
examinados**, A.13). El hallazgo es sobre el registro, que es el
universo que el encargo nombra.

### Punto 6 · Originales intactos — **PASA**

```
$ git diff --numstat 737a851^1 737a851 | awk '$2 != 0 {print "borradas="$2, $3}'
borradas=2 canon/estado-programa-v1_10.md
borradas=1 canon/gobernanza-v1_15.md
borradas=2 forense/firmas-pendientes.tsv
```

Las tres son **reemplazos de línea**, no pérdidas: cabeceras de conteo
que suben de `241` a `242` y celdas de `TSV` reescritas. Lo que el
encargo exige preservar se preserva:

- *"absorbe las 5 colas de agosto SIN borrarlas"* → ninguna de las cinco
  aparece en el diff: **0 líneas borradas** sobre 5 archivos (A.13).
- L0 *"insertada antes de la anterior, nunca reescribiendo la que ya
  estaba"* → la línea pasa de **9524** a **11141** caracteres y las
  **diez** citas `ADR-` anteriores sobreviven; se añade `ADR-242`.

### Punto 7 · Escala y universo (A-bis 3/4) — **PASA**

La cifra central declara su universo en la misma frase (*"72 filas: 56
heredadas de … + 16 candidatos nuevos absorbidos de los cuatro
`cola-ext-*`"*) y el desglose por estado nombra la columna que lo
produce. Ninguna cantidad de este PR es una cifra sobre México: es un
inventario de adquisición.

### Punto 8 · `ADR`/`FP`, colisión y renumeración — **1 `BLOQUEA`**

```
$ git show 737a851:canon/gobernanza-v1_15.md   | grep -oE '^\*\*ADR-[0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1
242
$ git show 737a851^1:canon/gobernanza-v1_15.md | grep -oE '^\*\*ADR-[0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1
241
```

Sin colisión: `241 → 242`. Contigüidad sin huecos (barrido `awk` sobre
la serie completa: cero huecos). Las **tres** cabeceras de conteo
coinciden: `gobernanza` línea 2 → `242 ADR`; `estado-programa` `L0` →
`242 ADR`; su tabla de documentos → `242 ADR`.

Pero la **comprobación 2 de las cuatro** —referencias cruzadas tras
renumerar— encuentra una huérfana, y es el hallazgo que a mí se me pasó
en mi primera pasada y que la lista sí atrapó:

```
$ git show 737a851:.claude/commands/adquiere.md | grep -n 'ADR-'
8:Creada por `ACTO MAESTRA33-A1 · AGENTE-ADQUISICION-1` (31/ago/2026, `ADR-241`
$ git show 737a851:canon/gobernanza-v1_15.md | grep -oE '^\*\*ADR-241[^·]*· `ACTO [A-Z0-9-]*'
**ADR-241 (candidato — …) · `ACTO MAESTRA33-E2
```

La skill que este acto instala **cita como su ADR fundador el `ADR-241`,
que es de otro acto** (`MAESTRA33-E2 · AGENTE-DESPACHO-1`). El acto
arrancó candidateando el 241, `PR #413` fusionó primero y se lo llevó, y
la renumeración a `242` alcanzó a `canon/gobernanza-v1_15.md`,
`canon/estado-programa-v1_10.md` y `canon/registro-rotulos.tsv` — pero
**no al propio archivo de la skill**. Es exactamente la clase de defecto
que el punto 8.2 existe para atrapar, y **sigue vivo en `main` hoy**.

Contexto que hace el hallazgo más nítido, no menos: este PR fue **el que
fusionó primero**, y el que tuvo que renumerar *hacia el otro lado* fue
`MAESTRA33-E3` (`ADR-242→243`, `FP-209→210`), donde sí se atrapó a mano.
La renumeración que se hizo a mano en un lado dejó una punta suelta en
el otro.

Arreglo propuesto: `241` → `242` en `.claude/commands/adquiere.md:8`.

### Punto 9 · `tests/check.py --baseline` — **PASA**

```
$ git diff --stat 737a851^1 737a851 -- tests/baseline.json
(vacío)
```

`baseline.json` **no se movió**. El único toque a `tests/` es la
extensión de `_T25_ARCHIVOS_CONOCIDOS` con dos rutas, cada una con su
comentario explicando de dónde sale la mención — el patrón que el resto
de la lista ya usa, y la salida legítima para un encargo verbatim que no
se puede editar (A.3).

### Punto 10 · "Lo que NO hace" — **1 `BLOQUEA`**

Cuatro prohibiciones, cuatro comandos:

```
$ git diff --name-only 737a851^1 737a851 | grep -c '^milpa/'     → 0
$ git diff --name-only 737a851^1 737a851 | grep -c '^data/raw'   → 0
$ git log --oneline --merges 737a851^1..737a851^2
db5a9bc Fusiona origin/main (PR #413, …)      ← merge DE main HACIA la rama, no a main
```

*"No abre ni analiza microdato"* y *"no compra ni registra en portales
de pago"* no se pueden convertir en comando desde el árbol; se declaran
así y se verifican leyendo el reporte, que las respeta (`ENAFIN` y las
tres comerciales quedan `NO-ACCESIBLE` y el acto sigue).

**La cuarta prohibición no se respeta, y es la misma fila del punto 5.**
El encargo dice, literal: *"no re-sondea lo ya `OBTENIDO` en manifiesto
(A.8 por fila antes de intentar)"*. La única fuente que este acto
sondeó por red fue `WVS` —siete peticiones a `worldvaluessurvey.org`,
según su propia nota— y `WVS` ola 7 México 2018 **ya estaba `OBTENIDO`
en el manifiesto, en seis formatos de microdato**. La prohibición se
violó porque el `A.8` por fila se corrió contra el inventario
equivocado; el defecto es uno solo, pero incumple dos puntos distintos y
se cuenta en los dos.

Y hay una razón para subrayarlo por encima de su tamaño: **es el defecto
exacto que hizo nacer `A.8`.** El caso fundacional, del 13/ago/2026, fue
una cola de descarga manual cuyas dos primeras filas —GESIS/ISSP y
**`WVS`**— ya estaban descargadas y registradas, *"16 y 11 entradas
respectivamente en `data/manifiesto.yaml`"*. `A.8` se escribió para eso.
Dieciocho días después, el acto que instala **el agente de adquisición**
lo repite, contra **la misma fuente**. Que la regla exista no basta si el
comando que la implementa mira otra tabla.

---

## §3 · VEREDICTO

**`NO-FUSIONAR`** — sobre un PR que mesa **ya fusionó**.

`5 BLOQUEA · 5 RESERVA · 0 NO-VERIFICADO · 1 NO-APLICA · 3 PASA`

Los cinco `BLOQUEA`, en una línea cada uno, ordenados por lo que cuestan:

1. **La fila `WVS` declara `(ausente)` del manifiesto y es falso**: hay
   diez entradas de WVS ola 7 México 2018, seis de microdato. El
   negativo se produjo contra un inventario que ni siquiera tiene el
   campo consultado (punto 5).
2. **Por eso mismo se re-sondeó por red una fuente ya `OBTENIDO`**, que
   es la prohibición literal del `LO QUE NO HACE` del encargo, y es el
   caso fundacional de `A.8` repetido contra la misma fuente (punto 10).
   Mismo defecto que (1), contado en los dos puntos que incumple.
3. **`.claude/commands/adquiere.md:8` cita `ADR-241`**, que es de otro
   acto: la renumeración `241→242` alcanzó a `canon/` y no a la propia
   skill. Sigue vivo en `main` (punto 8).
4. **El desglose `44 PENDIENTE / 1 NO-OBTENIDO` contradice la tabla**,
   que dice `43 / 2`, en el mismo commit que lo escribió; se propagó al
   `## CONSUMIDO` (punto 5).
5. **`forense/hallazgos.md` tocado fuera del perímetro y sin declarar**
   en el ADR ni en la propia lista "Escrito" del ejecutor (punto 3) —
   con la disidencia de §2 registrada.

Los cuatro últimos se arreglan con una línea cada uno. El primero no:
obliga a re-correr el `A.8` de la fila contra el manifiesto de verdad, y
probablemente a mover `WVS` de `NO-OBTENIDO-POR-ESTE-AGENTE` a
`OBTENIDO` con sus seis `ids_manifiesto` — que es, además, **una
corrección a favor del acto**: la tabla viva queda mejor de lo que su
autor creía.

Nada de esto toca la sustancia: la tabla existe, la skill funciona, y la
corrección de estado de `FP-17` es correcta y bien argumentada. Un
`NO-FUSIONAR` aquí dice *"esto se arregla antes de fusionar"*, no
*"esto está mal pensado"*.

---

## §4 · Qué dice esta calibración sobre la lista

**Lo que salió bien.** Los diez puntos corren; ocho se resuelven con
comandos de una línea. El punto 5 hizo exactamente aquello para lo que
existe: encontró **dos** afirmaciones falsas re-derivándolas, no
leyéndolas, y una de las dos había sobrevivido a un merge de mesa. El
punto 6 evitó su propio falso positivo —tres líneas borradas que
parecían pérdida y eran reemplazos— gracias a la comprobación de
longitud de `L0` (9524 → 11141, diez citas intactas). Y el punto 8
atrapó una referencia huérfana **que a mí se me había pasado** al correr
los mismos cuatro chequeos a mano: la lista escrita vio lo que su autor
no vio.

**Lo que hay que mirar, y no se corrige aquí.** Dos cosas, y las dos
quedan anotadas para mesa, no legisladas:

- El peso `BLOQUEA` del punto 3 para un desborde **aditivo** puede ser
  demasiado filo (§2, con su disidencia de 2 de 3 lentes).
- El punto 4 no distingue hoy entre **un negativo que escribe el
  ejecutor** y **un negativo que viene citado verbatim del encargo de
  dirección**. Un agente de la corrida de §5 marcó `BLOQUEA` por un
  negativo sin conteo que está en la línea `A.8` **del encargo** — texto
  que `A.3` prohíbe editar y que el ejecutor no puede arreglar. Medir al
  ejecutor por eso es un error de categoría.

**Y por qué no se corrigen ahora.** La lista se congeló en `aa9a1bb`,
antes de que esta corrida existiera. Editarla al ver qué encontró —sobre
todo para ablandar lo incómodo— es exactamente el defecto que su propio
punto 2 prohíbe. Si mesa quiere moverlas, ése es su commit, con su
razón, después de éste.

**Para el falsador `§3(a)`.** Mesa fusionó `PR #414` con cinco cosas que
la lista atrapa, una de ellas un re-sondeo de red contra una fuente ya
adquirida. No hay punto que añadir: los puntos 5, 8 y 10 ya estaban y
funcionaron. El caso queda citado.

---

## §5 · Doble corrida independiente

La calibración se corrió **dos veces y por separado**, a propósito:

- **A mano**, por quien escribió la lista, leyendo el PR.
- **Por una flota de diez agentes** (Sonnet, uno por punto, sin contexto
  de esta sesión), a cada uno de los cuales se le dio **sólo** el objeto
  del PR y la instrucción de **leer su punto en
  `.claude/commands/revisa.md` y ejecutarlo**. Sus hallazgos pasaron
  después por tres lentes adversariales cada uno —corrección mecánica,
  contexto del encargo, y peso contra la regla escrita—, con la
  instrucción de refutar ante la duda.

Ésa es la prueba que importa y no la podía dar la corrida a mano: **la
lista es ejecutable por alguien que no estaba cuando se escribió.** Los
diez agentes resolvieron su punto leyendo sólo el texto de la skill.

Dónde coincidieron y dónde no, que es lo informativo:

| | a mano | flota | resuelto |
|---|---|---|---|
| `WVS` `(ausente)` falso | no lo vi | `BLOQUEA` | **sostenido**, verificado a mano después |
| `adquiere.md` cita `ADR-241` | no lo vi | `BLOQUEA` | **sostenido**, verificado a mano después |
| `44/1` vs `43/2` | `BLOQUEA` | `BLOQUEA` | **sostenido** |
| `hallazgos.md` fuera de perímetro | `BLOQUEA` | `RESERVA` | `BLOQUEA` por la regla, disidencia anotada |
| quinta cola no absorbida | no lo vi | `BLOQUEA` | bajado a **`RESERVA`**: el reporte dice "los cuatro" |
| negativo sin conteo del encargo | — | `BLOQUEA` | **descartado**: es texto de dirección (A.3) |

**Dos hallazgos reales que la corrida a mano no vio**, y **dos
calificaciones de la flota corregidas a la baja**. Ninguna de las dos
corridas por sí sola habría dado este resultado, y eso es un argumento
sobre cómo usar la pieza: `/revisa` no sustituye a mesa leyendo el PR —
le pone debajo un piso mecánico que no depende de que ese día alguien se
acuerde de los diez puntos.

**CONTADOR: cero mediciones, declarado (infraestructura de proceso).**
Esta nota mide un PR; no mide México.
