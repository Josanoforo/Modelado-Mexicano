# K2 · FAMILIA BANCARIA · descriptivo rotulado con frontera · ENIF 2012-2021 · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-DIN-CREDITO-HISTORIA-1 (21/sep/2026, CAJA), pieza P4. CALC
reservado: `CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001`. Encargo archivado por
A.3 en `forense/encargos/2026-09-21-GEN2-DIN-CREDITO-HISTORIA-1.md` (sello de
cuerpo `a66577f187bb778a75a7acdbad9cbf00227a5ff6679044ab1dc78ed5428f428b`).
Firma de mesa FP-404 (2): «K2 familia bancaria: opción (iii) para la serie —no
se compara 2021<->2024, es CAMBIO-DE-INSTRUMENTO— y (i) rotulado para el
descriptivo. La cifra del corpus 'bancaria +5.2 pp desde 2021' no se cita sin
esa frontera.»

**Estado al congelar: COMMIT-1 sin corrida.** El CONTADOR del encargo «sella
hasta cuatro corridas» y las cuatro ya están selladas (2018, 2015, 2012,
ENFIH). Esta spec queda congelada y con `preflight` VERDE; su `corrida0 run`
es una quinta corrida y se PREGUNTA a mesa (encargo §6, D-19): (a)
autorizarla en este mismo acto, (b) DIFERIR a un sucesor, (c) no medir los
niveles y dejar sólo la frontera. **Recomendación del ejecutor: (a)** — el
código está congelado, no abre 2024 y el costo es una corrida de ~10 s.

## 0 · La frontera, en una frase (P4 «la frase de por qué»)

La familia bancaria de K2 **no se compara entre 2021 y 2024** porque el ítem
6.2.2 de 2024 cambió de «tarjeta de crédito bancaria» a «tarjeta de crédito
bancaria **u otra institución financiera**» (fila K2·2024 de
`data/credito-comparabilidad-texto-v1_1.tsv`: `CAMBIO-DE-INSTRUMENTO`); una
diferencia 2021→2024 mezclaría el cambio de conducta con el cambio de familia
medida, así que «bancaria +5.2 pp desde 2021» no es una cifra de este
programa. Entre 2012, 2015, 2018 y 2021 el ítem dice exactamente «tarjeta de
crédito bancaria» (6.6.1 · 6.9.2 · 6.8.2 · 6.2.2): los niveles se rotulan con
su población (18-70 hasta 2018; 18+ en 2021) y con el filtro de tenencia de
cada ola.

## 1 · Exposición declarada (ADR-46)

Mismos documentos que `DIN-CREDITO-PISOS-HISTORIA-spec-v1_0.md` §0 (ya
leídos por P2); nada nuevo. El microdato de 2018/2015/2012 ya fue abierto por
las corridas selladas de P2 (bancaria no se leyó en ellas: FP-404) y el de
2021 por #943 y por el ORO. ENIF 2024 **no se abre** (PARO a; reserva
`reserva:enif2024-credito`).

## 2 · Estimando y desenlace

Por ola (2012, 2015, 2018, 2021): proporción ponderada de personas elegidas
con tarjeta de crédito bancaria (`BANCARIA`, unidad P, base toda persona
elegida) y entre tenedores de algún producto formal
(`BANCARIA-ENTRE-TENEDORES`, base K1 = 1), celda `NACIONAL-TODOS`, IC95
bootstrap. Variable por ola del mapa v1.1 (`DIN-CREDITO-PISOS-HISTORIA-mapa-v1_1.tsv`,
rol `k2_bancaria`: 2012 `P6_6_1` —ítem 1 por el orden invertido—, 2015
`P6_9_2`, 2018 `P6_8_2`, 2021 `P6_2_2`); 1 si = 1; 0 si = 2 o blanco de quien
dijo No al filtro de la ola; indefinido en otro caso (contado). El medidor
CONTRASTA el reactivo con la fila K2·ola de la tabla v1.1 y PARA si K2·2024
no está declarado `CAMBIO-DE-INSTRUMENTO` por la familia bancaria.

## 3 · Procedimiento congelado

Lectura y marco **por bytes** del medidor sellado de los pisos históricos
(`CALC-DIN-CREDITO-PISOS-ENIF2018-0001/medidor.py`, input `MEDIDOR-HISTORIA`;
oro: reproduce #943): ponderador de persona > 0, diseño estrato × UPM,
bootstrap de UPM con reemplazo dentro de estrato, 10 000 réplicas
`PCG64(42)`, IC percentil; **un plan de réplicas por ola** (cuatro llamadas a
`_estimate`, una por payload). Guardias: soporte `n < 200`; unidad P.
Ejecución diagnóstica sobre microdato: ninguna; el medidor corrió sobre los
cuatro sintéticos (60 y 120 réplicas) antes de congelarse.

Salidas de texto: `2024-BANCARIA = RESERVADA-NO-MEDIDA`,
`2024-VEREDICTO-TEXTO`, `DIFERENCIA-2021-2024 = NO-SE-COMPARA: …` (§0),
`CIFRA-DEL-CORPUS-MAS-5-2-PP = NO-SE-CITA …`.

## 4 · Lo que esta spec no hace

No abre ENIF 2024; no calcula ninguna diferencia 2021↔2024; no cruza por
ejes; no presenta la serie 2012-2021 como piso (es descriptivo rotulado); no
adopta.
