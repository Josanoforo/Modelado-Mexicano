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

## 2 · La regla, y por qué es leave-one-out

Por celda elegible del marco vigente:

  · si la conducta trae `serie_olas`, el punto usa la **ola más cercana
    DISTINTA de la del árbitro**; empate → la anterior. Se declara
    `SERIE-LOO · ola_usada=<n>` con su fuente, la ola del árbitro y la
    distancia;
  · si no la trae, `modela_ola: NO`. No se inventa una serie.

El *leave-one-out* no es un adorno estadístico. Usar la misma ola que el
árbitro haría que M y R leyeran el mismo número, y el duelo dejaría de ser
un duelo: M estaría copiando su respuesta del examen que se le está
aplicando. Por eso la regla es «distinta a la del árbitro» y no «la más
cercana».

El desempate hacia la ola ANTERIOR también se declara en vez de dejarse al
orden del YAML: `TRA-M-03` (árbitro 2013) tiene 2011 y 2015 a la misma
distancia, y sin regla escrita el resultado dependería de cómo se ordenó el
archivo.

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
