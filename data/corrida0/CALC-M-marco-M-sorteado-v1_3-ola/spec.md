# `CALC-M-marco-M-sorteado-v1_3-ola` — modulación por ola, demostrada

`ACTO GEN2-T9 · EL MOTOR ES LA MATRIZ`, 8/sep/2026, P3(c)/(e).
Entorno **NUBE**, sin corpus y sin red. **CONTADOR: cero.**

## 1 · La firma que la ordena

D-2, mesa, 8/sep/2026, verbatim: *«revisa el whitepaper, esto es una matriz,
no colapsamos a menos que la literatura y benchmark de lo que queremos
lograr lo demanden, podemos modular por ola si es lo más práctico»*.

Dos mandatos, y esta corrida obedece los dos: **no colapsar** (las 14 celdas
siguen siendo 14, ninguna ola se promedia ni se funde) y **modular por ola
donde sea práctico** (donde la conducta ya trae serie medida).

## 2 · La regla — última ola estrictamente anterior

> **ADENDA DE MESA, 8/sep/2026, recibida en vuelo (precisión 1).** Esta
> sección sustituye a la regla original de este acto —«ola más cercana
> distinta a la del árbitro, empate → anterior»—, que queda derogada.

Por celda elegible del marco vigente:

  · si la conducta trae `serie_olas`, el punto usa la **última ola
    ESTRICTAMENTE ANTERIOR** a la de la celda del árbitro. Se declara
    `SERIE-PREVIA · ola_usada=<n>` con su fuente, la ola del árbitro, la
    distancia y el **origen** de la entrada;
  · si hay serie pero **ninguna ola anterior**, `SIN-PREVIA`: la celda **no
    modula**. No se usa una posterior y no se promedia;
  · si no hay serie, `modela_ola: NO`. No se inventa una.

**Por qué «anterior» y no «más cercana».** Con una serie que no trae ninguna
ola anterior, «más cercana» elige una **posterior**: el punto se construiría
con información que no existía en el momento que se predice. Eso es **fuga
temporal**, y una demostración que la enseñe enseña el patrón equivocado
aunque el número salga bien — es el mismo corte que la evaluación clásica de
series hace al partir el conjunto por tiempo y no al azar, y es lo que D-2
pedía al invocar *«el benchmark de lo que queremos lograr»*.

Sigue siendo *leave-one-out* por construcción: exigir **estrictamente**
anterior deja fuera la ola del árbitro. Usar su misma ola haría que M y R
leyeran el mismo número y el duelo dejaría de ser un duelo — M estaría
copiando su respuesta del examen que se le aplica. `TRA-M-03` es el caso que
lo hace visible: su árbitro es ENCIG **2013** y la serie trae una entrada
2013 cuyo `metodo` es, literalmente, `R-json (TRA-M-03, ya público)` — su
propio resultado arbitrado. La regla la excluye.

**Medido al instalar la regla:** sobre las 6 celdas que hoy modulan,
**ninguna cambia de ola** — las seis ya tenían una anterior, y las dos
reglas coinciden en las seis. Se instala por lo que impide mañana, no por lo
que corrige hoy, y decirlo así es parte de instalarla. `SIN-PREVIA` no es
hipotético: con árbitro en 2011 (el primer año de la serie ENCIG) la regla
vieja habría tomado 2013 —posterior **y** `ORIGEN-ARBITRO`— y la nueva
declara `SIN-PREVIA`.

## 2-bis · `ORIGEN-ARBITRO` — la entrada que no puede puntuar

> **ADENDA DE MESA, 8/sep/2026 (precisión 2).**

Tres entradas de la serie de `tramite.mordida.discrecional:enmienda_encig2025`
—ENCIG **2013**, **2017** y **2021**— traen `metodo: "R-json (TRA-M-0X, ya
público)"`: su valor **no** nace de una medición propia, sino del `R-json` de
un duelo ya arbitrado.

`F-DD` (`ADR-237`) cubre el par **misma-encuesta-misma-ola**; **no** cubre la
reutilización **cruzada** de un valor que ya pasó por el árbitro. Una celda
que modulara con una de esas entradas estaría puntuando contra un número que
el árbitro ya vio, y `F-DD` no lo atraparía.

Regla: toda celda cuya ola modulada consuma una entrada `ORIGEN-ARBITRO`
queda **`VERIFICACION-NO-PUNTUA`**, no `P1`, con el rótulo en el propio
`RESULT` (`RESULT-MOLA-<id>-GRADO-DD`).

Para GEN2 real esto es discutible-*moot* —`C0-B` recompone las series con
cadena propia, regla `E.1`—, pero la demostración no debe enseñar el patrón
contaminado. **Hoy:** `RESULT-MOLA-N-ORIGEN-ARBITRO = 0` (ninguna de las 6
celdas cae ahí), y las tres entradas se inventarían igual en
`RESULT-MOLA-ENTRADAS-ORIGEN-ARBITRO-EN-SERIES` — el guard se declara aunque
no muerda, porque el día que muerda nadie estará mirando.

Se lee el campo `metodo` y nada más: una entrada que no lo declara es
`ORIGEN-MEDICION`. No se adivina procedencia desde el `payload_id` ni desde
el acto.

## 3 · `F-DD` contra la ola usada

Si el punto viene de 2013, la dependencia declarativa que le toca es la de
2013. Anclarlo a la ola del árbitro sería puntuar un número con el ancla de
otro. `RESULT-MOLA-<id>-ANCLA-F-DD` lleva la ola efectivamente usada.

## 4 · Lo que NO hace

No promedia series. No ajusta tendencias. No colapsa olas. No toca la
métrica sellada de `procedimiento-scoring-v1_2.md` ni ningún `corridas-M/`.
Los puntos LOO que emite son **demostración del aparato**: son modelo nuevo
y van a `C0-B` con spec propia antes de que ninguna cifra suya entre a un
veredicto.

## 5 · Alcance medido, declarado por adelantado

Hoy tienen `serie_olas` **2 reglas** de las que el marco vigente usa, y
cubren **6 de las 14** celdas elegibles: `FAM-M-05/06/07`
(`familia.seguro.volatilidad_ausencia_estado`, 6 olas) y `TRA-M-02/03/07`
(`tramite.mordida.discrecional:enmienda_encig2025`, 8 olas). Las otras 8
salen `NO`. La demostración es sobre 2 reglas y eso se asienta en
`## NO-CORRIDO / RESERVAS`, no se presenta como cobertura.

`TRA-M-02` es el caso cruzado: el árbitro es ENCUCI 2020 y la serie es
ENCIG. La corrida lo declara en el propio `RESULT` (fuente y ola del
árbitro a la vista) en vez de silenciarlo — decidir si una serie de un
instrumento puede modular la celda de otro es de mesa, no del medidor.

## 6 · Por qué `cuenta_gen2: NO`

D-1 + regla E.1: los insumos son `milpa/tramite.yaml` (aparato GEN1) y el
marco vigente. Por completa que sea la cadena, el número viene de GEN1.

## 7 · Determinismo

`seed.aplica: false`. Todo sale de dos archivos versionados con SHA
declarado. Dos corridas sobre el mismo árbol dan los mismos bytes.
