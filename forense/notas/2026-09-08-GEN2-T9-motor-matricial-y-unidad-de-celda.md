# `ACTO GEN2-T9 · EL MOTOR ES LA MATRIZ` — nota del acto

8/sep/2026 · entorno **NUBE**, sin corpus y sin red · **CONTADOR: cero GEN2**
Encargo archivado (0-bis A.3):
`forense/encargos/2026-09-08-GEN2-T9-MOTOR-MATRICIAL.md`

---

## 0 · Las tres firmas de mesa que este acto ejecuta

**D-1**, verbatim: *«decisión 1 no cuentan como Gen2, no cometamos un error
sobre los 600 PR's que ya cagamos»*.

**D-2**, verbatim: *«revisa el whitepaper, esto es una matriz, no colapsamos
a menos que la literatura y benchmark de lo que queremos lograr lo demanden,
podemos modular por ola si es lo más práctico»*.

**D-2 bis**, verbatim: *«el motor no es una matriz?, solo el modelo de
decisión? […] tenía entendido que sí es una matriz»*.

D-2 bis es la que obligó a verificar contra el árbol en vez de contra la
memoria, y es la que destapó todo lo demás.

---

## 1 · El motor ES matricial, por sello de mesa — y `D11` lo contradecía

`canon/gobernanza-v1_15.md:1550` (`ADR-91`, 17/ago/2026, `PR #246`) y su
ejecución en `ADR-100`, firma de mesa verbatim citada ahí:

> *«M1 cómputo matricial como definición del ejecutable»*

adoptado **antes** del gate de Fase 1. El ejecutable son
`milpa/src/{motor,matriz,theta,pi,celdas,momentos}.py`.

`canon/gobernanza-v1_15.md:6902` (`ADR-396`, `ACTO GEN2-E3-1`, 8/sep/2026)
propagó `D11`:

> *«`milpa/src/motor.py`, `theta.py`, `pi.py`, `celdas.py`, `momentos.py`
> son scaffold/calibración histórica, no la definición de "motor limpio
> GEN2"; el sistema numérico activo es `tramite.yaml + emisor + matriz B`»*

Las dos no pueden ser verdad. `D11` vino de una auditoría de readiness
externa y se propagó sin cotejarla contra `ADR-91` — dictar contra el árbol
sin comando, que es exactamente la clase de error que A.8 nombra.
**`D11` queda revocada por este acto; `ADR-91` rige.**

El **emisor** (`milpa/src/emisor.py` sobre `tramite.yaml`) no es el motor:
es el emisor binario de reglas que alimenta al marcador, una de las salidas
del motor.

---

## 2 · Consecuencia medida: el ejecutable sellado NO ARRANCA hoy

Esto no estaba en el encargo. Salió de correrlo:

```
$ python3 -c "from milpa.src import motor; motor.correr()"
ClaseDesconocida: ningún prefijo conocido casa con 'REFUTADO-POR-COTA'
```

`procedencia.cargar()` lanza sobre `milpa/procedencia.yaml`. **Dos** valores
de `clase:` que `milpa/src/clases.py` no conoce por prefijo (censados sobre
las 28 entradas con `clase:` del archivo):

| valor | dónde | quién lo escribió |
|---|---|---|
| `REFUTADO-POR-COTA` | `asignados_probabilidad[10]` | `ACTO MAESTRA37-N8` (D2-g, firmas 3/sep/2026) |
| `EVIDENCIA_EXPERIMENTAL_TERCEROS` | bloque homónimo | sellado por `ADR-204`; ya declarado como defecto preexistente en el comentario de `milpa/src/procedencia.py` (`ACTO MAESTRA32-E1`, 28/ago/2026) |

Sin `Procedencia` no hay `B`; sin `B` no hay `g(x) = B·θ(x)` ni
`motor.evaluar()`. **El ejecutable que `ADR-91` selló como *definición del
ejecutable* no corre**, y nadie lo había notado porque nada lo corría — que
es, punto por punto, la consecuencia de haberlo declarado «scaffold».

Este acto **no lo repara**: `milpa/src/**` está fuera de su perímetro (*«el
motor se corre, no se edita»*). Lo mide, lo publica como `RESULT` sellado
(`CALC-MOTOR-celdas-semilla`) y lo asienta en `forense/no-corrido.tsv` con
sucesor nombrado.

---

## 3 · Tres cifras del encargo que el árbol no sostiene

El encargo se redactó, en su propia sección de verificación, con cifras que
no coinciden con lo medido. Se corrigen aquí; el encargo archivado **no se
edita** (A.3).

| el encargo dice | el árbol da | comando |
|---|---|---|
| «Θ: 18 `MEDIDO·PARCIAL` + 5 `MEDIDO·NACIONAL`» (= 23) | **10 + 2 = 12** | `grep -c 'clase: "MEDIDO·PARCIAL'` / `'…NACIONAL'` sobre `milpa/procedencia.yaml` — la fórmula oficial de `procedencia.contador_condicionales_medidas()`, la misma que `tests/check.py` T19b/T19c |
| «77 entradas `_ejes_` con IC por eje» | **7 entradas**, **24 ejes**, **74 puntos por eje** (los 74 con `ic95`) | `RESULT-AGGOLA-{ENTRADAS-EJES,EJES,PUNTOS-POR-EJE-CON-IC}` de `CALC-AGG-marco-M-sorteado-v1_3-ola` |
| «`celda_R/M/L/AGREGADO 14/14/28/14` = 162» | **correcto**, verificado fila por fila | ver §4 |

La **conclusión** del encargo sobre los ejes no cambia — existen puntos por
eje con IC95 y ninguna celda del marcador consume ninguno (verificado: ni
`milpa/src/emisor.py` ni `tools/emite_m.py` mencionan `ejes`). La **cifra**
sí. Las tres se publican por separado para que la próxima cita no tenga que
adivinar cuál de ellas quiso decir «77».

---

## 4 · P2 · La demanda re-derivada (C0-A bis)

`C0-A` (`ACTO GEN2-E2`) derivó su cierre transitivo desde el emisor y el
marcador, **nunca desde el ejecutable sellado**. Las 162 filas de
`demanda-resultados.tsv` no tenían ni una para Θ, π, celdas-D o momentos.

`cmd_demanda` gana cuatro consumidores, **leídos de los módulos**:

| tipo | n | de dónde se lee | peldaño |
|---|---|---|---|
| `corte_pi` | 6 | `celdas.CORTES_C1` (4 sellados bajo M2, 2 `PENDIENTE`/`FP-53`) | 0 |
| `celda_D` | 3 | `motor.celdas_semilla()` — `listdir`, no de memoria | 0 |
| `momento` | 22 | `momentos.cargar_catalogo()` (8 `AJUSTE` / 14 `HOLDOUT`) | 1 |
| `condicional_theta` | 12 | el mismo recorrido de `procedencia._recorrer`, clases `MEDIDO·PARCIAL`/`MEDIDO·NACIONAL` | 2 |

**Contadores:** `N_resultados_activos` **162 → 205**;
`N_corridas_requeridas` **79 → 86**;
`dependencias_numericas_legacy_activas` **162 → 205** — y eso es lo
correcto: la deuda no creció, se hizo visible.

Los peldaños **no se renumeran**. Se declara un peldaño 0 para la malla
(estructura que precede a toda medición) y los otros dos tipos caen donde ya
vive su gemelo: un momento es un estadístico observado como una tasa base
(1), y Θ se consume junto a `B` en `matriz.g(B, θ(x))` (2).

**Nada se recalcula.** Las filas nuevas se añaden al final, y las 162
previas quedan **byte-idénticas**:

```
$ diff <(git show origin/main:data/corrida0/demanda-resultados.tsv) \
       <(head -164 data/corrida0/demanda-resultados.tsv) && echo IDENTICAS
IDENTICAS
```

### 4-bis · Lo que la re-derivación destapó, y no decide

Las Θ declaran ejes que **no son** los seis del vector de atributos de
`clases.EJES`: `urbanización` y `migración` (con acento, contra
`urbanizacion`/`migracion`), y además `dominio`, `sexo`, `escolaridad`,
`estrato`, `ESTRATO`. Son **11 líneas** en la salida de ambigüedades de
`cmd_demanda`. El registro las lista y **no decide** si el eje sobra en la
clase o falta en los cortes: eso es de mesa.

---

## 5 · P1 · D-1 ejecutable — la regla E.1, con nombre

> **E.1 — Ningún `CALC` cuyo input resuelva a `milpa/tramite.yaml`,
> `milpa/procedencia.yaml` o `corridas-R/M/L` cuenta como GEN2, por completa
> que sea su cadena.**

Un corredor envuelto puede tener spec endurecida, sello válido y `verify
REPRODUCE/IDENTICO` — y aun así el número que emite viene del aparato GEN1.
La calidad de la envoltura no cambia la procedencia del número.

**La regla es transitiva, y ese es el punto.**
`CALC-AGG-marco-M-sorteado-v1_3` **no nombra** `tramite.yaml` en ningún
input: consume `CALC-M-.../resultados.json`. Sin cierre transitivo habría
pasado por GEN2 limpio leyendo cifras del emisor GEN1 — que es literalmente
el error que D-1 manda no repetir. `_propaga_envuelto()` lo resuelve por
punto fijo sobre el grafo declarado de inputs.

Ningún `spec.yaml` sellado se edita (E.3): la firma de mesa vive en
`data/corrida0/decisiones.tsv` y la regla en el resolutor.

**`corredores_envueltos_legacy = 5`** — `CALC-M`, `CALC-AGG`, `CALC-M-…-ola`,
`CALC-AGG-…-ola`, `CALC-MOTOR-celdas-semilla`. `N_corridas_selladas = 0`.
`replays_legacy_sellados = 2` (los dos SMOKE, que se auto-declaran
`LEGACY-GEN1` y son otra cosa).

---

## 6 · P3 · La unidad de celda — `NC-0020` decidida

**La celda del marcador es
`regla × segmento (x, sobre los seis ejes del modelo) × ola × instrumento`.**

Las 14 celdas de hoy son el caso `x = ∅` y **se conservan**. **No se
colapsan olas.** La dimensión que falta es el **segmento**.

Esto explica el diagnóstico que abrió `NC-0020`: la constancia de `M` dentro
de CIV **no es un defecto del emisor**. Con `x = ∅` la evaluación matricial
se reduce a la `p` base de la regla, y por eso seis celdas de una regla
repiten un número. La celda no porta su punto de la matriz porque no porta
vector de atributos.

Las cuatro opciones de
`forense/notas/2026-09-08-GEN2-E7-paso-3-unidad-de-celda.md` estaban
**incompletas**: ninguna de las cuatro contenía la dimensión de la matriz.
Se anota por enmienda fechada en esa nota; no se reescribe.

### 6.a · Diseño del marcador GEN2 (para `C0-D`, después de `C0-C`)

- celda con `x ≠ ∅`: `M` se emite con el motor matricial — `p` base GEN2 de
  la regla más `g(B, θ(x))` — y `R` es el IC por eje de la entrada `_ejes_`
  correspondiente;
- celda con `x = ∅`: `M` es la `p` base y la celda lleva
  `modela_segmento: NO`.

**No se corre aquí.** Depende de `C0-C` (motor y emisor limpios) y, antes,
de que el motor arranque (§2).

### 6.b · Modulación por ola — demostrada sobre 2 reglas

Regla: si la conducta trae `serie_olas`, el punto usa la **ola más cercana
distinta de la del árbitro** (leave-one-out; empate → la anterior),
`modela_ola: SERIE-LOO · ola_usada`, y `F-DD` **contra la ola usada**. Sin
serie, `modela_ola: NO`.

El *leave-one-out* no es adorno: con la misma ola que el árbitro, M estaría
copiando su respuesta del examen que se le aplica y el duelo dejaría de ser
un duelo.

Medido: **2 reglas** con `serie_olas`, que cubren **6 de 14** celdas —
`FAM-M-05/06/07` (6 olas) y `TRA-M-02/03/07` (8 olas). Las otras 8 salen
`NO`.

Y el resultado que importa: donde el marcador de hoy emite un punto
**constante**, la modulación produce puntos **distintos** por celda
(`TRA-M-03 → 0.068328` contra `TRA-M-02/07 → 0.084484`). El aparato hace lo
que se esperaba de él.

**Nada de promediar ni ajustar tendencias.** Es modelo nuevo y va a `C0-B`
con spec propia antes de que ninguna cifra suya entre a un veredicto.

### 6.c · El agregado

Conserva su métrica sellada — `procedimiento-scoring-v1_2.md` y
`agregado-v1_3-resultado.json` no se leen ni se reescriben — y añade dos
vistas informativas: **por regla** (cuenta celdas, no promedia puntos: una
mediana por regla sería colapsar por la puerta de atrás) y **por segmento**
(hoy `0`, con el otro lado del conteo al lado: 74 puntos por eje con IC95
existen y ninguna celda los consume — *el hueco es de cableado, no de
dato*).

---

## 7 · A.13 — qué se examinó

| veredicto | archivos examinados | comando |
|---|---|---|
| «el motor no arranca» | 6 | `CALC-MOTOR-celdas-semilla` → `RESULT-MOTOR-ARCHIVOS-EXAMINADOS` |
| «cero filas de motor en la demanda» | 1 (`demanda-resultados.tsv`, 162 filas, 9 tipos) | `awk -F'\t' 'NR>2{c[$3]++}'` |
| «ninguna celda del marcador consume `_ejes_`» | 2 (`emisor.py`, `emite_m.py`) | `grep -n "ejes"` → 0 líneas |
| «2 reglas con serie» | 1 (`tramite.yaml`) | `grep -n "serie_olas"` → 2 bloques |

Las tres corridas nuevas dan `verify` **`REPLICA-RESULTADO`
(`RESULTADO=REPRODUCE`)**. `CONTEXTO=DISTINTO` en las tres, y su razón es
mecánica y esperada: el `git_commit` del sello no es el de hoy, porque cada
corrida se selló en su propio commit y el árbol siguió avanzando dentro del
mismo acto.

---

## 8 · ADENDA DE MESA — recibida en vuelo, 8/sep/2026

*El encargo archivado **no** se edita (A.3). Dos precisiones a P3(c), ambas
dentro del perímetro ya declarado.*

### 8.1 · Precisión 1 — la regla es «última anterior», no «más cercana»

La regla que este acto había implementado —«ola más cercana distinta a la
del árbitro, empate → anterior»— **queda derogada**. La regla operable es:

> **última ola estrictamente anterior** al periodo de la celda del árbitro;
> sin anterior en la serie → `modela_ola: SIN-PREVIA` y la celda **no
> modula** (no se usa posterior, no se promedia).

**Por qué.** Con una serie que no trae ninguna ola anterior, «más cercana»
elige una **posterior**: el punto se construye con información que no
existía en el momento que se predice. Es **fuga temporal**, y una
demostración que la enseñe enseña el patrón equivocado aunque el número
salga bien. Es el mismo corte que la evaluación clásica de series hace al
partir el conjunto por tiempo y no al azar — lo que D-2 pedía al invocar
*«el benchmark de lo que queremos lograr»*.

**Medido, y hay que decirlo entero:**

| | |
|---|---|
| celdas que cambian de ola | **0 de 6** |
| celdas que cambian de `p` | **0 de 6** |
| `RESULT-MOLA-N-SIN-PREVIA` hoy | **0** |

Las seis celdas que modulan ya tenían una ola anterior, así que las dos
reglas coinciden en las seis y los seis puntos `p` son idénticos entre la
corrida vieja y la nueva (comparado archivo contra archivo, no afirmado).
**La regla se instala por lo que impide mañana, no por lo que corrige hoy** —
y eso la hace más creíble, no menos: no se puede acusar de haber sido
ajustada a un resultado.

**Una premisa de la adenda que el árbol no sostiene.** La adenda propone
verificar «remesas ENIGH, celda objetivo 2016 […] si la serie arranca en
2016, "más cercana distinta" daría 2018». Verificado: la serie de
`familia.seguro.volatilidad_ausencia_estado` **arranca en 2012**, no en 2016
(olas 2012·2014·2016·2018·2020·2022), así que `FAM-M-05` sí tenía anterior
—2014— y la regla vieja ya daba 2014. **La fuga no estaba viva en esa
celda.** El caso donde sí muerde es el árbitro en **2011**, el primer año de
la serie ENCIG: la regla vieja habría tomado **2013** —posterior **y**
`ORIGEN-ARBITRO`— y la nueva declara `SIN-PREVIA`. Ese es el caso que quedó
como test.

### 8.2 · Precisión 2 — `ORIGEN-ARBITRO`

Verificado en `milpa/tramite.yaml` (líneas **111**, **113**, **115**, como la
adenda indica): tres entradas de la serie de
`tramite.mordida.discrecional:enmienda_encig2025` —ENCIG **2013**, **2017**,
**2021**— traen `metodo: "R-json (TRA-M-0X, ya público)"`. Su valor no nace
de una medición propia: viene del `R-json` de un duelo ya arbitrado.

`F-DD` (`ADR-237`) cubre el par **misma-encuesta-misma-ola**; **no** cubre la
reutilización **cruzada** de un valor que ya pasó por el árbitro. Regla: toda
celda cuya ola modulada consuma una entrada `ORIGEN-ARBITRO` queda
**`VERIFICACION-NO-PUNTUA`**, no `P1`, con el rótulo en el `RESULT`.

**Hoy `RESULT-MOLA-N-ORIGEN-ARBITRO = 0`**: ninguna de las 6 celdas cae ahí.
Las tres entradas se inventarían igual en
`RESULT-MOLA-ENTRADAS-ORIGEN-ARBITRO-EN-SERIES` — el guard se declara aunque
no muerda, porque el día que muerda nadie estará mirando. Para GEN2 real es
discutible-*moot* (`C0-B` recompone las series con cadena propia, regla
`E.1`), pero la demostración no debe enseñar el patrón contaminado.

`TRA-M-03` es el caso que hace visible por qué el leave-one-out importa: su
árbitro es ENCIG **2013** y la serie trae una entrada 2013 cuyo `metodo` es,
literalmente, `R-json (TRA-M-03, ya público)` — su propio resultado
arbitrado. La regla lo excluye por exigir **estrictamente** anterior.

### 8.3 · Dónde viven las dos reglas, y por qué las corridas viejas no se tocan

Las dos son funciones **puras** en `tools/emite_m.py` —donde vivirá la
envoltura por celda que las consuma en `C0-D`— y el CALC de demostración las
**importa** en vez de recopiarlas: dos copias de una regla de mesa se separan
en cuanto una cambia. **Ninguna toca el camino de emisión vigente de
`emite_celda`**, así que ninguna `corridas-M/*.json` sellada cambia por esto.

**Las corridas selladas no se reescriben.** `corrida0 run` lo impide
(`CALC-INMUTABLE · YA-SELLADO`) y tiene razón: una corrida sellada es
evidencia histórica de lo que se corrió, **incluida la regla que se
corrió**. Así que la adenda entra por **sucesión declarada** (`repite_de`):

| predecesora | estado | sucesora |
|---|---|---|
| `CALC-M-marco-M-sorteado-v1_3-ola` | `SUPERADO→` | `CALC-M-marco-M-sorteado-v1_3-ola-v2` |
| `CALC-AGG-marco-M-sorteado-v1_3-ola` | `SUPERADO→` | `CALC-AGG-marco-M-sorteado-v1_3-ola-v2` |

Las dos predecesoras conservan sus bytes intactos y su sello `COINCIDE`. Que
las dos versiones convivan **es el punto**: así se ve qué regla produjo qué
número. Las dos sucesoras dan `verify REPRODUCE` y son `cuenta_gen2: NO` por
`D-1`. `corredores_envueltos_legacy` **5 → 7**; `N_corridas_selladas` sigue
en **0**.

### 8.4 · Un defecto latente encontrado al mover el código

`RAIZ` en los medidores usaba **tres** `dirname` para un archivo que vive
**cuatro** niveles adentro (`data/corrida0/<CALC>/medidor.py`): resolvía a
`data/`, no a la raíz. Sólo funcionaba porque `corrida0` se invoca desde la
raíz y el CWD ya estaba en `sys.path`; el día que se invocara desde otro
sitio, el import del motor habría reventado. Corregido en el medidor `-v2`
(nace con cuatro). El de `CALC-MOTOR-celdas-semilla` **queda como está** —su
corrida está sellada y el defecto no afectó su resultado—; se paga en el acto
sucesor que ya tiene `milpa/src/` en perímetro (`NC-0023`).
