# GEN2-RELEVO-RECONCILIA-1 — el contador de legacy subcuenta: reconciliación por identidad de slot

**Acto:** `ACTO GEN2-RELEVO-RECONCILIA-1` · 20/sep/2026 · entorno NUBE (`ENTORNO-DERIVADO = NUBE`,
`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, corpus `montado=NO archivos_examinados=0`, red
`DENEGADA-POR-POLITICA`).
**Base:** `dfb07b9` (el encargo declaraba `93f68f2e`; main se movió, se re-derivó todo contra `dfb07b9`).
**CONTADOR:** `cuenta_gen2 = NO`. **Este acto no mide y no adopta: propone.**
`dependencias_numericas_legacy_activas` sigue en **173** y `N_resultados_gen2_adoptados_activos` en **57**,
verificado por `python3 tools/corrida0.py status` antes y después.

Derivado: `reconcilia-173-v1_0.tsv`, una fila por slot legacy, por
`reconcilia_relevo.py`. Todo lo de abajo sale de esa corrida; nada está tecleado.

---

## 0 · Qué cambia para mesa, en una línea

De los 173 slots que el contador declara pendientes de GEN2, **37 ya tienen su cifra dentro de un CALC
GEN2 sellado** y la vista de relevo no los ve — no porque falte la corrida, sino porque **todos los
canales de la vista están tecleados sobre el número `RES-####`, y ese número es posicional.**

## 1 · La reconciliación (P1) — 173 slots examinados (A.13)

Universo examinado: 166 directorios `data/corrida0/CALC-*` con `spec.yaml`; de ellos **73** están
`SELLADA` con `cuenta_gen2 = SI` (estado derivado por `corrida0.estado_calc`, nunca por lectura de un
campo). 173 slots `LEGACY-GEN1` de `relevo-usos-v1_0.tsv`.

| estado | slots |
|---|---|
| `SIN-REHACER` | 115 |
| `YA-REHECHO-EN-GEN2` | 28 |
| `CANDIDATO-POR-IDENTIDAD-SIN-CASAR` | 21 |
| `REHECHO-CON-DIFERENCIA` | 9 |

### 1.1 · Tres clases de relevo que NO se colapsan

La spec de `CALC-TRIADA-0001` declara, RESULT por RESULT, de dónde sale cada punto. Leerlas juntas
sería inflar el hallazgo:

| clase | slots | qué significa | evidencia en la spec |
|---|---|---|---|
| `RE-MEDIDO-EN-GEN2` | 14 | medición nueva sobre microdato en GEN2 | `-R` → «citado de `data/corrida0/CALC-R-<celda>/resultados.json`» |
| `INGERIDO-CON-CADENA-NO-RE-MEDIDO` | 14 | la MISMA cifra GEN1, ahora con cadena E.2 (input con sha256) — **no se volvió a medir** | `-M` → «punto del **snapshot sellado**»; y el propio snapshot declara `todas_las_14_celdas_identicas_al_estado_previo` |
| `RE-DERIVADO-EN-GEN2` | 9 | punto recalculado en GEN2 desde las 224 capturas con el extractor v1.3 sellado | `-L-*` → «mediana de réplicas EXTRAIBLE» |

**Esta distinción es la decisión de mesa, no mía.** Las palabras de la firma del 20/sep son «qué
mediciones de Gen1 se hicieron y cuáles se **re-hicieron** en Gen2 pero ahora con la trazabilidad que
nos faltaba». Los 14 R se re-hicieron. Los 14 M ganaron la trazabilidad **sin** re-hacerse. Si mesa
quiere que el contador signifique «re-medido», los 14 M no bajan de 173; si quiere que signifique
«con cadena GEN2», sí. No lo decido aquí.

### 1.2 · Los 14 árbitros R: delta exactamente `0.0`, 14 de 14

El valor legacy de cada `:R` vive en `forense/prereg-duelo-v2/corridas-R/<celda>.json` (GEN1). El
valor GEN2 es `RESULT-R-<celda>-PUNTO` del CALC sellado. Comparados por identidad de celda
(`parametros.id_celda`), **los 14 dan delta `0.0`**. Eso es reproducción, no coincidencia de nombre:
`CALC-R-CIV-M-01` declara contaminación (la sesión había leído el punto GEN1) pero su medidor no
recibe el valor por ningún parámetro y lee el DBF de cero.

*Reserva:* el control positivo pre-declarado de la spec (`R-ENVIPE-SERIE-DBF-control-gen1.py`, cuatro
ramas) exige microdato y por tanto CAJA. **No lo corrí aquí y no reporto su veredicto.** Lo que sí
está derivado en esta sesión es la igualdad de los puntos sellados contra los JSON GEN1, con comando.

### 1.3 · `[SUPUESTO-TRIADA]`: verdadero en parte, y la parte falsa es demanda

`CALC-TRIADA-0001` **sí** emite por celda `-M`, `-L-SOLO`, `-L-CORPUS` y `-R`. Pero:

* **AGREGADO — 14 de 14 `SIN-REHACER`.** `NO-ENCONTRADO`: TRIADA no emite ningún RESULT de agregado
  por celda. El mecanismo no cubre esa identidad. Universo examinado: los 259 RESULT de
  `CALC-TRIADA-0001/resultados.json`.
* **L — 19 de 28 `SIN-REHACER` por una razón distinta.** El RESULT existe y vale `null`:
  `CORRIDO-SIN-PUNTO`, con `NOTA-DE-CORTE = «fuera de U3: sin punto válido de L_SOLO/L_CORPUS»`. El
  mecanismo **sí corrió** contra esas celdas y no produjo punto. Eso no es lo mismo que «nadie corrió
  el mecanismo», y la tabla los separa (§2 de las instrucciones).

Los 33 slots `SIN-REHACER` del marco (14 AGREGADO + 19 L) llevan en la tabla su receta y su entorno
de la demanda: **NUBE**. Es demanda lista para lanzar.

## 2 · La causa, reproducida (P2)

`tools/relevo_usos.py` documenta sus cuatro canales de descubrimiento. **Los cuatro están tecleados
sobre el token literal `RES-####`** escrito en la spec del CALC. Y el `RES-####` es posicional: su
autoridad, `demanda-resultados.tsv`, se deriva por orden, así que insertar un slot recorre a todos los
de abajo (NC-0343: 37 filas corridas en uno al entrar el slot DIN). Una spec sellada **no se puede
editar** (E.3). El pin queda congelado apuntando a un número que ya es de otro slot.

| causa | slots | caso testigo |
|---|---|---|
| `SIN-OFERTA-QUE-VER` | 82 | no es ceguera: no hay oferta GEN2 sellada |
| `CALC-SIN-PIN` | 64 | `CALC-TRIADA-0001` y los 8 `CALC-R` v3/v4 no escriben **ningún** `RES-####` |
| `CANDIDATO-POR-CLAVE-PIN-NO-EVALUADO` | 13 | casados por clave de consumidor; el pin no aplica |
| `NO-ES-CEGUERA-VEREDICTO-SELLADO-OBEDECIDO` | 8 | la vista **sí** los ve y obedece un veredicto sellado `NO-ADOPTABLE` |
| `PIN-A-RES-AJENO` | 6 | los seis `CALC-R-CIV-*` |

**Causa 1 reproducida, con el desplazamiento medido.** Los seis pines CIV están corridos **+2, de
forma uniforme** — no es un error suelto, es deriva posicional:

| CALC | pin en la spec sellada | ese `RES` hoy es | slot que el CALC realmente mide | offset |
|---|---|---|---|---|
| `CALC-R-CIV-M-01` | `RES-0093` | `tramite.gobierno_digital.util_sin_coercion` | `CIV-M-01:R` = `RES-0095` | +2 |
| `CALC-R-CIV-M-02` | `RES-0098` | `CIV-M-01:L:L+corpus` | `CIV-M-02:R` = `RES-0100` | +2 |
| `CALC-R-CIV-M-04` | `RES-0103` | `CIV-M-02:L:L+corpus` | `CIV-M-04:R` = `RES-0105` | +2 |
| `CALC-R-CIV-M-10` | `RES-0108` | `CIV-M-04:L:L+corpus` | `CIV-M-10:R` = `RES-0110` | +2 |
| `CALC-R-CIV-M-12` | `RES-0113` | `CIV-M-10:L:L+corpus` | `CIV-M-12:R` = `RES-0115` | +2 |
| `CALC-R-CIV-M-13` | `RES-0118` | `CIV-M-12:L:L+corpus` | `CIV-M-13:R` = `RES-0120` | +2 |

El pin de `CALC-R-CIV-M-01` es peor que un número corrido: el encargo ya notaba que apunta a
`CORR-0024`, que hoy es **CIV-M-02**. El pin está corrido en los dos ejes, `RES` y `CORR`.

**Causa 2, `CALC-SIN-PIN`.** Once CALC sellados no escriben ningún `RES-####`:
`CALC-TRIADA-0001`, `CALC-R-DIN-M-01-v4`, `CALC-R-{FAM-M-01,FAM-M-05,FAM-M-06,FAM-M-07,TRA-M-02,TRA-M-03,TRA-M-07}-v3`,
`CALC-C2-COMPUESTO-IC-ENVIPE2025-0001`, `CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001`. En el caso de
TRIADA está **declarado a propósito**: su spec dice «Ninguna demanda de `milpa/` — este acto no adopta
a ningún consumidor». Es decir: el CALC que carga 37 de las cifras que la vista busca declaró, con
razón, que no adoptaba nada — y nadie previó que la vista lo leería como «no hay cifra».

**Causa 3, `FUNCION-INDETERMINADA` (#914): NO REPRODUCIDA AQUÍ.** Reproducirla exige escribir un pin
en `tramite.yaml`, que es **PARO** de este encargo (§7). El mecanismo existe
(`tools/corrida0.py:3623`). Queda `NO-VERIFICABLE-AQUÍ`, con sucesor.

**Causa 4, el guion bajo.** La identidad de celda viaja con guion en el marco (`CIV-M-01`) y con guion
bajo en los RESULT de TRIADA (`CIV_M_01`). No es la causa de la ceguera de hoy (la vista no casa por
celda en absoluto), pero es una trampa puesta para el que escriba el enlace. Se normaliza en el
reconciliador.

**No arreglé `relevo_usos.py`.** El arreglo mínimo (casar por `parametros.id_celda` cuando el
consumidor es el marco M) no cabe en ≤10 líneas y movería el contador. Propuesta, no parche.

## 3 · Propuesta de firma (P3) — este acto no escribe ningún pin

### Bin 3 — bloque `RE-MEDIDO-EN-GEN2` · 14 árbitros R, delta 0.0 (14/14)

| slot | celda | CALC GEN2 | RESULT | valor GEN2 = valor legacy | delta |
|---|---|---|---|---|---|
| RES-0095 | CIV-M-01:R | `CALC-R-CIV-M-01` | `RESULT-R-CIV-M-01-PUNTO` | 0.25899878251638075 | 0.0 |
| RES-0100 | CIV-M-02:R | `CALC-R-CIV-M-02` | `RESULT-R-CIV-M-02-PUNTO` | 0.24339981393062482 | 0.0 |
| RES-0105 | CIV-M-04:R | `CALC-R-CIV-M-04` | `RESULT-R-CIV-M-04-PUNTO` | 0.24366832225578466 | 0.0 |
| RES-0110 | CIV-M-10:R | `CALC-R-CIV-M-10` | `RESULT-R-CIV-M-10-PUNTO` | 0.20493399286059008 | 0.0 |
| RES-0115 | CIV-M-12:R | `CALC-R-CIV-M-12` | `RESULT-R-CIV-M-12-PUNTO` | 0.20811159524290274 | 0.0 |
| RES-0120 | CIV-M-13:R | `CALC-R-CIV-M-13` | `RESULT-R-CIV-M-13-PUNTO` | 0.1946118021509308 | 0.0 |
| RES-0125 | DIN-M-01:R | `CALC-R-DIN-M-01-v4` | `RESULT-R-DIN-M-01-PUNTO` | 0.15558094338412926 | 0.0 |
| RES-0130 | FAM-M-01:R | `CALC-R-FAM-M-01-v3` | `RESULT-R-FAM-M-01-PUNTO` | 0.5571925669683186 | 0.0 |
| RES-0135 | FAM-M-05:R | `CALC-R-FAM-M-05-v3` | `RESULT-R-FAM-M-05-PUNTO` | 0.04745859252351374 | 0.0 |
| RES-0140 | FAM-M-06:R | `CALC-R-FAM-M-06-v3` | `RESULT-R-FAM-M-06-PUNTO` | 0.04728548395278385 | 0.0 |
| RES-0145 | FAM-M-07:R | `CALC-R-FAM-M-07-v3` | `RESULT-R-FAM-M-07-PUNTO` | 0.04377543852935772 | 0.0 |
| RES-0150 | TRA-M-02:R | `CALC-R-TRA-M-02-v3` | `RESULT-R-TRA-M-02-PUNTO` | 0.12602486953090247 | 0.0 |
| RES-0155 | TRA-M-03:R | `CALC-R-TRA-M-03-v3` | `RESULT-R-TRA-M-03-PUNTO` | 0.04453797671500066 | 0.0 |
| RES-0160 | TRA-M-07:R | `CALC-R-TRA-M-07-v3` | `RESULT-R-TRA-M-07-PUNTO` | 0.07181522879909936 | 0.0 |

### Bin 2 — uno por uno · 14 puntos M `INGERIDO-CON-CADENA-NO-RE-MEDIDO`

| slot | celda | CALC GEN2 | RESULT | valor | delta |
|---|---|---|---|---|---|
| RES-0096 | CIV-M-01:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-CIV_M_01-M` | 0.294313 | 0.0 |
| RES-0101 | CIV-M-02:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-CIV_M_02-M` | 0.294313 | 0.0 |
| RES-0106 | CIV-M-04:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-CIV_M_04-M` | 0.294313 | 0.0 |
| RES-0111 | CIV-M-10:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-CIV_M_10-M` | 0.294313 | 0.0 |
| RES-0116 | CIV-M-12:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-CIV_M_12-M` | 0.294313 | 0.0 |
| RES-0121 | CIV-M-13:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-CIV_M_13-M` | 0.294313 | 0.0 |
| RES-0126 | DIN-M-01:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-DIN_M_01-M` | 0.174804 | 0.0 |
| RES-0131 | FAM-M-01:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-FAM_M_01-M` | 0.457707 | 0.0 |
| RES-0136 | FAM-M-05:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-FAM_M_05-M` | 0.045694 | 0.0 |
| RES-0141 | FAM-M-06:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-FAM_M_06-M` | 0.045694 | 0.0 |
| RES-0146 | FAM-M-07:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-FAM_M_07-M` | 0.045694 | 0.0 |
| RES-0151 | TRA-M-02:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-TRA_M_02-M` | 0.085118 | 0.0 |
| RES-0156 | TRA-M-03:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-TRA_M_03-M` | 0.085118 | 0.0 |
| RES-0161 | TRA-M-07:M | `CALC-TRIADA-0001` | `RESULT-TRIADA-TRA_M_07-M` | 0.085118 | 0.0 |

### Aparte — `REHECHO-CON-DIFERENCIA` · 9 puntos L re-derivados

| slot | celda:variante | RESULT | GEN2 | legacy | delta (pp) |
|---|---|---|---|---|---|
| RES-0137 | FAM-M-05:L:L-solo | `RESULT-TRIADA-FAM_M_05-L-SOLO` | 0.045 | 0.046125 | -0.113 |
| RES-0138 | FAM-M-05:L:L+corpus | `RESULT-TRIADA-FAM_M_05-L-CORPUS` | 0.046 | 0.045875 | +0.013 |
| RES-0142 | FAM-M-06:L:L-solo | `RESULT-TRIADA-FAM_M_06-L-SOLO` | 0.045 | 0.04875 | -0.375 |
| RES-0143 | FAM-M-06:L:L+corpus | `RESULT-TRIADA-FAM_M_06-L-CORPUS` | 0.05 | 0.04725 | +0.275 |
| RES-0147 | FAM-M-07:L:L-solo | `RESULT-TRIADA-FAM_M_07-L-SOLO` | 0.045 | 0.052875 | -0.787 |
| RES-0148 | FAM-M-07:L:L+corpus | `RESULT-TRIADA-FAM_M_07-L-CORPUS` | 0.05 | 0.051625000000000004 | -0.163 |
| RES-0152 | TRA-M-02:L:L-solo | `RESULT-TRIADA-TRA_M_02-L-SOLO` | 0.14 | 0.15125 | -1.125 |
| RES-0157 | TRA-M-03:L:L-solo | `RESULT-TRIADA-TRA_M_03-L-SOLO` | 0.125 | 0.1225 | +0.250 |
| RES-0162 | TRA-M-07:L:L-solo | `RESULT-TRIADA-TRA_M_07-L-SOLO` | 0.146 | 0.14425 | +0.175 |

**Lectura de los 9 con diferencia.** Todos son puntos L re-derivados en GEN2 desde las mismas 224
capturas con el extractor v1.3 sellado. Los deltas van de `-0.79 pp` a `+0.28 pp`. **No son escalas
distintas** (A-bis.3): ambos son proporción en `[0,1]` sobre la misma celda y la misma variante. La
diferencia es de procedimiento de agregación entre GEN1 y el `mediana de réplicas EXTRAIBLE` de la
spec sellada. **Casar el estimando por texto en cinco dimensiones sigue pendiente para estos 9** y es
lo que mesa necesita antes de firmar: los listo aparte, no en bloque.

**Los 21 `CANDIDATO-POR-IDENTIDAD-SIN-CASAR`** (20 del motor, 1 de celdas-D) tienen un CALC GEN2
sellado que **nombra su clave de consumidor** en la spec — entre ellos `RES-0028`, el caso de #914,
que cae en `CALC-R-CIV-M-10/12/13`. No los propongo para firma: un acierto de clave no es un
estimando casado, y A-bis.3/4 prohíben aparear cifras sin enlace declarado. Son la cola del sucesor.

## 4 · Desglose aditivo (P4) — `status` y el test que lo sostiene

`corrida0 status` publica ahora, junto al contador y **sin cambiarle nombre ni valor**:

```
dependencias_numericas_legacy_activas=173
legacy_activas_por_consumidor__motor=35
legacy_activas_por_consumidor__procedencia=40
legacy_activas_por_consumidor__catalogo_de_momentos=23
legacy_activas_por_consumidor__marco_del_duelo=70
legacy_activas_por_consumidor__celdas_D=5
legacy_activas_por_consumidor__otro=0
```

35 + 40 + 23 + 70 + 5 + 0 = **173**. `T45 · T-LEGACY-DESGLOSE-SUMA` lo exige mecánicamente y además
falla si la clase residual `otro` deja de estar vacía — un consumidor nuevo que nadie mapee rompe el
test en vez de desaparecer del desglose en silencio. Los cinco son **relevables**: ninguno se declara
fuera del contador.

**El `[SUPUESTO]` del encargo sobre el oro es FALSO, y a favor.** `tests/test_corrida0_oro.py` es un
arnés opt-in (`CORRIDA0_ORO=…`) que sella contra una copia del árbol en el momento; **no hay ningún
oro commiteado** (`git ls-files | grep -i oro` → solo el propio script). No hubo nada que regenerar.

## 5 · Módulo de auditoría (afirma sobre el programa)

* **¿Cuántos contadores movió este trabajo?** **Cero, por diseño.** `dependencias_numericas_legacy_activas`
  = 173 y `adoptados_activos` = 57, antes y después. Lo que mueva, lo moverá mesa en el sucesor.
* **¿En qué escala está cada cantidad?** Los R, M y L son proporciones en `[0,1]` sobre la misma celda;
  los deltas de la tabla de diferencias se expresan en **pp** y están rotulados. Los agregados legacy
  son z-scores y **no se compararon contra nada** (A-bis.3): no hay función de enlace y TRIADA no emite
  un agregado por celda.
* **¿Qué afirmación sobre el estado del corpus fue escrita a mano?** Ninguna cifra de este informe.
  Todas salen de `reconcilia_relevo.py` o de un comando citado. Las cifras del duelo que sí derivé
  (`U3-N = 12`, `MAE-M = 4.9867 pp`, `MAE-L-SOLO = 3.9574`, `MAE-L-CORPUS = 3.8890`,
  `VEREDICTO-GLOBAL = SIN-GANADOR-UNICO`) salen de `CALC-TRIADA-0002/resultados.json`.
* **Lo peligroso leído simple, en las dos direcciones.** El duelo de tres dice, **con 12 celdas e IC
  anchos y las tres deltas pareadas `INCONCLUSO`**, que el motor no se distingue de un LLM con o sin
  corpus a nivel nacional, y en el punto queda ~1 pp por detrás. Ese resultado es del emisor v1 y de
  celdas nacionales. **Ningún artefacto debe escribir «el motor le gana a un LLM».** Tampoco lo
  contrario: `SIN-GANADOR-UNICO` **no** es «el motor no sirve» — es un IC que no despeja. Y un
  `celdas_validadas` alto **no** sería «acierta».
* **¿Qué deuda asumida a propósito caducó?** La de TRIADA: declarar «ninguna demanda de `milpa/`» era
  correcto para su acto y hoy es la causa de que 37 cifras estén invisibles. La deuda no era del
  CALC — era de la vista, que lee ausencia de pin como ausencia de cifra.
* Este informe **no afirma nada sobre México**: afirma sobre el aparato. El módulo de §3 no aplica.
