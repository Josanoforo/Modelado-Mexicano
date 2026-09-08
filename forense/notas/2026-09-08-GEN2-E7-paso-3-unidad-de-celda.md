# Paso 3 del marco: la unidad de celda — tabla de opciones, sin decisión

ACTO GEN2-E7 · READINESS-2 · Pieza A, **A5**.

Este documento **verifica el paso 3 como diseño, no como código** y **no toma
la decisión**. La unidad de celda es decisión de mesa. Lo que aquí se entrega
es (1) el diagnóstico mecánico, medido, no supuesto; (2) las opciones con lo
que cada una cuesta y lo que cada una compra; (3) lo que la mesa tendría que
firmar en cada caso. Nada de esto se implementó en este acto.

---

## 1 · El diagnóstico, medido

`CALC-M-marco-M-sorteado-v1_3` emite `RESULT-M-P-DISTINTOS`. Sobre el marco
vigente (14 celdas, `elegible_v1_1 = SI` en las 14) el valor es **5**.

Las 14 celdas se reparten en cinco grupos, y dentro de cada grupo M emite el
**mismo punto** para todas:

| grupo (regla · conducta) | celdas | `p` emitida | olas del árbitro |
|---|---|---|---|
| `civico.denuncia.miedo_desconfianza` · `denuncia_con_miedo_o_desconfianza` | CIV-M-01, -02, -04, -10, -12, -13 (6) | 0.294313 | ENVIPE 2012, 2013, 2015, 2021, 2023, 2024 |
| `dinero.ahorro.tiene_ahorros` · `tiene_ahorros` | DIN-M-01 (1) | 0.174804 | ENNViH/MxFLS 2002 |
| `familia.apoyo.recibe_dinero_familiares` · `recibe_dinero_familiares_para_vejez` | FAM-M-01 (1) | 0.457707 | ENIF 2018 |
| `familia.seguro.volatilidad_ausencia_estado` · `recibe_remesas` | FAM-M-05, -06, -07 (3) | 0.045694 | ENIGH 2016, 2018, 2020 |
| `tramite.mordida.discrecional` · `paga_mordida_encig2025` | TRA-M-02, -03, -07 (3) | 0.085118 | ENCUCI 2020, ENCIG 2013, ENCIG 2021 |

**Lo que esto significa, dicho sin adorno:** el marco distingue 14 celdas por
(encuesta, ola, instrumento). M distingue 5, porque `emitir_binaria` toma
`(regla, conducta)` y nada más. Seis celdas que el árbitro mide sobre olas de
ENVIPE separadas por doce años reciben de M el mismo punto.

Contra R, esto no invalida el marcador: la celda sigue siendo comparable
porque R sí varía por ola. Lo que hace es **cambiar qué mide el eje M**: no
mide si M acierta ola por ola, mide si M acierta el nivel de la conducta y
cuánto castiga la variación temporal que M no modela. Son dos preguntas
distintas, y hoy el marcador contesta la segunda mientras el nombre de la
tabla sugiere la primera.

### 1-bis · Corrección al `diagnostico-14-celdas-v1_0.tsv`

`forense/prereg-duelo-v2/diagnostico-14-celdas-v1_0.tsv` (el diagnóstico de
MAESTRA38-M13) trae `p_emitida = 0.62` para TRA-M-02/-03/-07. Contra el marco **vigente**
esas tres celdas emiten **0.085118**, no 0.62. El motivo no es un error del
diagnóstico: entre v1_2 y v1_3 esas tres celdas fueron re-apuntadas de la
conducta `paga_mordida` a `paga_mordida_encig2025` (es el re-apunte que
`agregado_v1_3.py` declara en `CONDUCTA_NUEVA` / `IDS_REAPUNTADOS`). El
diagnóstico es correcto para v1_2 y **quedó atrás** para v1_3.

Las otras once filas del diagnóstico coinciden con lo emitido hoy. Este acto
no edita ese TSV (está fuera del perímetro): se asienta la discrepancia y su
causa, para que nadie la lea como si fuera de v1_3.

### 1-ter · Lo que MAESTRA38-M13 sí cerró

El aviso de `L-spec-v1_2.json` dice que DIN-M-01 «NO tiene M: el emisor se
negó a emitirla». **Ya no es cierto.** Con `grado_DD` derivado por conducta
(la corrección de MAESTRA38-M13, ya en `emite_m.py`), DIN-M-01 emite:
`p = 0.174804`, `grado_DD = P1 PUNTUA`. Las 14 de 14 celdas del marco vigente
emiten. Ese aviso de la spec de L está obsoleto y se asienta aquí; corregirlo
en el JSON sellado es acto aparte, no éste.

---

## 2 · Las opciones

Ninguna es gratis y ninguna es obviamente correcta. Se presentan con lo que
cuestan.

### Opción A — Mantener `regla × ola × instrumento` (statu quo)

La celda es lo que es hoy: 14 celdas, M emite 5 puntos distintos.

- **Compra:** cero trabajo. El marco sellado no se toca. Las 424 capturas L
  GEN1 y las corridas R existentes siguen apuntando a las mismas celdas.
- **Cuesta:** el eje M queda estructuralmente penalizado por una variación
  (la temporal) que M no pretende modelar, y el marcador no puede separar
  «M erró el nivel» de «M no modela la ola». Los seis CIV pesan seis veces
  en el agregado marginal de M con un único punto detrás — un empate o un
  error se multiplica por seis sin que haya seis mediciones de M.
- **Qué firmaría la mesa:** que el eje M se lee como «nivel de conducta
  contra ola concreta», y que el agregado marginal de M no se interpreta
  como precisión por celda.

### Opción B — `regla × segmento` (colapsar las olas)

La celda pasa a ser (regla, conducta); las olas de una misma conducta se
agregan en un solo renglón. 14 celdas → 5.

- **Compra:** el eje M mide lo que M pretende. Desaparece la multiplicación
  del mismo punto. El agregado deja de estar dominado por el grupo con más
  olas.
- **Cuesta:** el universo se reduce a **5 celdas**. Un marcador de 5 celdas
  tiene poder estadístico muy pobre: los IC bootstrap del agregado ya son
  anchos con 14. Además, R y L sí varían por ola, y colapsarlas obliga a
  decidir **cómo** se agrega el lado R (¿promedio simple de olas?, ¿la ola
  más reciente?, ¿ponderar por n?) — una decisión sustantiva nueva, no un
  cambio de formato.
- **Qué firmaría la mesa:** la regla de agregación del lado R y L, y aceptar
  n = 5.

### Opción C — Celda `regla × ola`, M declara `NO-MODELA-OLA`

La celda no cambia (14). Lo que cambia es que M emite, junto al punto, una
marca explícita de que su punto **no depende de la ola**, y el agregado
reporta dos cifras: una por celda y una por grupo de conducta.

- **Compra:** no se toca el marco sellado ni las capturas GEN1; el marcador
  gana la distinción que hoy le falta sin perder poder; el lector ve las dos
  lecturas y elige.
- **Cuesta:** dos cifras en vez de una, y hay que definir la de grupo (que es
  la misma decisión de agregación de la Opción B, pero como **cifra
  secundaria**, no como universo). Riesgo real de que se cite la conveniente.
- **Qué firmaría la mesa:** que la cifra principal sigue siendo la de 14
  celdas, y la regla de agregación de la secundaria.

### Opción D — Enriquecer M para que module la ola

Que `emitir_binaria` reciba la ola y emita un punto distinto por ola.

- **Compra:** la unidad de celda deja de ser un problema; el eje M mide
  precisión por celda de verdad.
- **Cuesta:** es un cambio **del modelo**, no del marcador. Requiere que
  `tramite.yaml` traiga calibración por ola donde hoy trae una sola
  (`ola_calibracion` es un campo único por regla, y para varias reglas dice
  literalmente «única ola disponible para este universo»). No hay dato para
  hacerlo hoy en la mayoría de las reglas. **Fuera del alcance del
  marcador**: es trabajo de modelo, con su propio pre-registro.
- **Qué firmaría la mesa:** un acto de modelo, no de marcador.

---

## 3 · Lo que este acto NO hizo

- No eligió opción.
- No editó `marco-M-sorteado-v1_3.tsv`, ni el sorteo, ni
  `diagnostico-14-celdas-v1_0.tsv`, ni `L-spec-v1_2.json`.
- No cambió `emitir_binaria` ni el cálculo de `grado_DD`.
- No produjo ningún número nuevo del modelo: los cinco puntos de la tabla §1
  son los que el emisor ya emitía; lo nuevo es que ahora nacen dentro de una
  corrida con spec, contrato, snapshot de inputs, recibo y sello.

## 4 · Lo que la mesa recibe para decidir

- La tabla §1, derivada mecánicamente de `RESULT-M-*` de
  `CALC-M-marco-M-sorteado-v1_3` (reproducible con
  `python3 tools/corrida0.py verify CALC-M-marco-M-sorteado-v1_3`).
- El número `RESULT-M-P-DISTINTOS = 5` contra `RESULT-M-N-CELDAS = 14`.
- Las dos correcciones de §1-bis y §1-ter, que cambian lo que dos documentos
  vigentes afirman.
- Las cuatro opciones con su costo.

La decisión es de mesa. Este acto la deja lista para tomarse, no tomada.
