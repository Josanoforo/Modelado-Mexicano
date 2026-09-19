# Informe del programa · v1.1

**Modelado Mexicano — «Psicología del Mexicano Contemporáneo».**
Documento del programa, escrito para un lector externo. 17 de septiembre de 2026.

### `informe-programa` · **v1.1** · DOCUMENTO DEL PROGRAMA

> | | |
> |---|---|
> | **ARCHIVO** | `informe-programa-v1_1.md` |
> | **REEMPLAZA A** | `informe-programa-v1_0.md` (15/sep/2026), retirada del árbol por T01 al sellar ésta; historia recuperable por SHA. La v1.0 no se reabre: lo que aquí cambia son dos días de hechos nuevos, no una relectura de los viejos |
> | **VERIFICAS ASÍ** | cada cifra del cuerpo tiene su fila en `canon/informe-programa-v1_1-ANEXO.md` (= anexo v1.0 verbatim + §A.9–A.13 nuevas), con universo (`A.10`) y comando; el módulo de auditoría va contestado en §6 |
> | **NOMBRE ESTABLE** | **`informe-programa`** — cítalo así, **nunca por nombre de archivo** |

> **Estampa de universo (A.10), global.** Derivado contra `origin/main = 9eff694` (merge de `PR #860`, 17/sep/2026), desde un clon del repositorio sin corpus montado. **Fuentes: solo registro derivado, tablero y notas selladas.** Este informe no abre microdato, no llama a ningún modelo, no sella ninguna corrida y no mueve ningún contador. Una cifra sin universo declarado no entra aquí.
>
> **Lo que este documento NO es:** no es una adjudicación, no reabre ningún veredicto, y no es el diseño del marcador ni el vocabulario v0.6, que se citan como decisiones de mesa del 17/sep y se ejecutan en actos propios.

---

## 0 · En una página

El programa construye un modelo de decisión sobre conducta en México (`canon/modelo-decision-v4_0.md`) a partir de fuentes públicas mexicanas, con un aparato que obliga a que toda cifra que entra al modelo tenga fuente, universo, unidad, ola y código verificables.

Hay cinco piezas que conviene no confundir — dos más que en la v1.0, porque en dos días el programa cambió de régimen:

| pieza | qué es | qué NO es |
|---|---|---|
| **R** | la estimación derivada del microdato por el propio programa: el **árbitro**. Diseño muestral, ponderador y códigos explícitos; 97 celdas por regla y eje, con error estándar | no es «la verdad»; se publica con su intervalo |
| **M** | en F5, el **emisor**: la regla del modelo emitiendo un punto nacional por celda. Desde el 17/sep, medido: en la ola actual **89 de 97 celdas del emisor son copia del árbitro** | no es un predictor acreditado, y donde es copia no es comparable con R |
| **el motor** | desde `ADR-531`: un **conjunto de estimadores por celda** adjudicados uno a uno, más una matriz que **compone** (no estima) | no es una fórmula única que emite para todas las celdas |
| **P · el piso** | el estimador más barato construible con lo público: en celdas de cruce, marginales de la misma ola sin interacción; en celdas marginales, la ola anterior por eje. **Desde el 17/sep, donde nadie lo vence, es el estimador adoptado de la celda** | no es una tesis sobre México; es aritmética sobre datos públicos |
| **L** | un modelo de lenguaje respondiendo la misma pregunta, con o sin paquete documental | no es una fuente; en tres comparaciones no ha vencido a ningún piso |

Entre agosto y el 17 de septiembre el programa corrió un duelo (**F5**) sobre 14 celdas nacionales y **dos pilotos por celda** sobre 20 celdas de cruce con evaluación reservada. Este informe dice qué salió, qué se puede usar y qué no.

---

## 1 · La tesis, tal como la mesa la fijó

Se reproduce **verbatim** de la firma de mesa del 15/sep/2026 (§D1). Este documento no la reinterpreta ni la suaviza:

> **D1 · Tesis.** Se acepta: mediciones reproducibles, éxito documental local y persistencia competitiva; el valor predictivo añadido de M queda por demostrar. M conserva sus otras funciones (organización de evidencia, aplicación consistente de reglas, escenarios), que se distinguen de la precisión predictiva y se acreditan por función. Esta reserva no es un juicio negativo del proyecto.

Traducido para un externo, sin añadir nada: **el programa mide bien y deja rastro; que su motor *prediga mejor que una alternativa barata* todavía no está demostrado.** Dos días después, la tesis se sostiene con más dato — y con una consecuencia que la v1.0 no podía dar: **la alternativa barata ya es el estimador del programa donde existe** (firma de mesa del 17/sep, §2.1).

---

## 2 · Qué podemos usar hoy, y para qué

La regla de lectura sigue siendo **por función acreditada**, no por nombre del artefacto.

### 2.1 · Lo que está acreditado y se puede usar

| pieza | función acreditada | evidencia | límite |
|---|---|---|---|
| **R** | **medición descriptiva reproducible** con diseño muestral | 82 corridas en la vista (16 más selladas en disco sin registrar, §4), 4 405 RESULT GEN2, 215 con validación independiente, `diferencias_materiales=0` | descriptiva; no es efecto causal |
| **P · piso por celda** — 20 celdas de cruce (DIN: ahorro solo informal × localidad × edad; TRA: evasión de norma × escolaridad × dominio) | **estimador por celda adoptado**, con intervalo y cadena completa | dos pilotos con reserva de evaluación intacta; MAE del piso 1.47 y 1.57 pp; ningún candidato lo venció | proporción por celda de una ola; no dice nada de la población más allá de la celda (H5) |
| **B · persistencia** | **piso de comparación** en celdas nacionales y marginales | D-A sellado (`CALC-TRIADA-B-PISO-0001`, 9 celdas); en TRA anual, corroborada como piso (4.31 pp, peor que P) | **no es ciega** (contaminación declarada); no es una tesis sobre México |
| **Recuperación documental sobre paquete preparado** | **convertir una fuente nativa en un punto trazable** | 16/16 réplicas dirigidas; 0/16 con contexto temático | **local**: dos celdas, dos paquetes ya adquiridos |
| **`edad` como eje compartido** | el único eje del modelo **equivalente** al del árbitro | crosswalk firmado (`FP-376`), corte sellado (`ADR-537`); 16 celdas del árbitro con celda del modelo | los demás ejes: dos mapeos con pérdida, uno sin mapeo, once sin correspondencia |
| **M · el motor** | **organización de evidencia · aplicación consistente de reglas · escenarios** (D1) | el aparato de linaje, procedencia y trámite | **no** precisión predictiva (2.2); **no** compite en la ola actual por eje: es el árbitro copiado |

### 2.2 · Lo que NO está acreditado

**El valor predictivo añadido de M — ahora con tres lecturas, no una.**
- *F5, nacional:* `SIN-GANADOR-UNICO` sobre 12 celdas; el orden se invierte al cambiar la ponderación (§3.1). Sin cambio desde la v1.0.
- *Pilotos, por celda:* en 20 celdas de cruce **ningún candidato del programa venció al piso** — ni la persistencia, ni la elicitación (L, −9 pp), ni la persistencia con interacción (empeora), ni la matriz, que **no pudo presentarse**: para competir necesitaría una función de salida por regla que no existe y parámetros que hoy no tienen magnitud.
- *Ola actual por eje:* **no hay comparación posible.** El emisor copió el árbitro en 89 de 97 celdas (`ADR-536`); compararlos mediría identidad. Por firma de mesa (`FP-383`) el emisor sale del marcador y aparece solo como diagnóstico.

**Los parámetros del motor como efectos.** La capa E1 (`ADR-535`) censó 43 parámetros condicionados: **0** con argumento explícito de identificación; 4 asociaciones medidas; 8 ausencias declaradas; 24 ausencias de facto. Cargarlos como coeficientes causales no está acreditado, y el programa dejó escrito dónde vive cada uno para que nadie lo haga sin darse cuenta.

**La interacción entre ejes como información aprovechable.** Medida en TRA: las interacciones por celda entre olas son inestables (solo 4/12 y 5/12 con intervalo que excluye cero; una cambia de signo). Que los candidatos no la exploten **no** dice que no exista (H5): dice que estos candidatos no la saben usar.

**La transferencia de M a familias no vistas (F6).** No se ha probado y hoy no se puede: 0 familias elegibles (`FP-374` vencida en alcance por su propia premisa; §4).

---

## 3 · Qué comparaciones son válidas — y cuáles no

### 3.1 · La dependencia de composición, declarada

Sin cambio desde la v1.0, porque el dato no cambió: **68.88 %** del error de M en F5 lo aportan seis celdas de una sola familia cívica; **el orden se invierte** al pesar por familia (M 5.03 vs 7.53/7.32) en vez de por celda (M 4.99 vs 3.89/3.96). El panel no tiene resolución para adjudicar. Tabla en el anexo §A.2.

### 3.2 · La reserva de evaluación, y lo que cuesta romperla

Los dos pilotos evaluaron celdas cuyo valor **nadie había calculado**: cruces de dos ejes cuyos marginales eran públicos y cuyo cruce no. Se congelaron candidatos y criterio, se produjeron las emisiones, y solo entonces se derivó el árbitro (tres commits en orden). En el segundo piloto la reserva se protegió con código: la función que reproduce marginales acepta una sola variable de agrupación y lanza con dos. La razón está documentada: el primer intento del piloto 2 rompió la reserva con un script exploratorio, y ese cruce (`edad × dominio`, ENVIPE 2025) quedó **consumido sin piloto** — se declara y no se usa. Un cruce visto no se puede desver.

### 3.3 · Universos que no se mezclan

| comparación | válida | por qué |
|---|---|---|
| M vs L sobre las 12 celdas de `U3` (F5) | **SÍ**, con §3.1 pegada | mismo universo, mismo árbitro |
| B vs M vs L sobre las 9 celdas comunes (D-A) | **SÍ**, descriptiva | sellada como `CALC-TRIADA-B-PISO-0001` |
| P vs C1/C3 en DIN (8 celdas) y P vs C1/C6/C7 en TRA (12) | **SÍ**, cada piloto en su celda-D | reserva intacta, criterio declarado antes |
| MAE de DIN contra MAE de TRA | **NO** | otro dominio, otra encuesta, otro universo; que el piso gane en los dos es un hecho, no una cifra sumable |
| el emisor contra el árbitro en la ola actual por eje | **NO** | 89 de 97 son el mismo número (`ADR-536`) |
| la vista de corridas (82) contra el disco (98 selladas) | **NO como una sola cifra** | son dos cifras y hoy difieren (§4) |
| F5 nacional contra los pilotos por celda | **NO como un solo veredicto** | miden cosas distintas: precisión nacional del emisor vs. estimación por celda con reserva |

### 3.4 · La regla general

**Un cierre no puede concluir más ancho que el universo que declaró** (A.10, corolario 2). Antes de citar cualquier cifra de este informe, lea su fila en el anexo.

---

## 4 · Dónde falta evidencia

Ordenado por lo que bloquea.

| hueco | estado | qué lo desbloquea |
|---|---|---|
| **74 celdas marginales del árbitro sin piso** | el marginal público de la misma ola *es* R; el único piso honesto es la ola anterior por eje, y no está sellada para ninguna | medirla: ≈40 de 74 tienen ola anterior con el mismo reactivo en el corpus (ENVIPE 2024, ENCIG 2023, ENIF 2021); acto en caja ya redactado |
| **Corridas selladas fuera de la vista** | 16 sin fila; 24 publicadas sin asiento de evidencia; el guardia se niega a escribir en silencio, correctamente | asentar la evidencia de 40 corridas, una a una, y escribir la vista una vez; acto en caja ya redactado |
| **Transferencia de M (F6)** | `FP-374` **VENCIDA EN ALCANCE**: 7 → 2 → 0 familias elegibles | acreditar R09-ISSP (codebook integrado) y ordenar adquisición dirigida; hoy en espera |
| **Identificación de θ** | 0 de 43 | diseños que identifiquen (instrumentos, discontinuidades, paneles); no existen para casi ningún nombre |
| **La matriz como candidata** | inejecutable en las dos celdas piloteadas: sin función de salida por regla, con parámetros sin magnitud | que una celda-D la ponga a competir con sus faltantes resueltos; `ADR-531` le permite competir, no la obliga |
| **Comparabilidad cívica** (el 68.88 %) | diagnosticado, no reparado | misma unidad, recorte, códigos y ola — o excluir la pareada |
| **Interacción aprovechable** | inestable entre olas por celda (TRA) | probar interacción agregada o encogida a cero, en un cruce no derivado; queda por diseñar |

---

## 5 · Reglas de decisión

Forma `SI [condición] ENTONCES [qué se puede hacer] — PORQUE [evidencia]`. Las nueve de la v1.0 se conservan (renumeradas donde hizo falta); las nuevas van marcadas.

1. **SI** se necesita una cifra descriptiva sobre México con diseño muestral **ENTONCES** se usa **R**, citando ola, unidad, universo, códigos y su EE — **PORQUE** es lo único con validación independiente y `diferencias_materiales=0`.
2. **SI** se quiere afirmar que M predice mejor que una alternativa **ENTONCES** no se hace con F5 ni con los pilotos — **PORQUE** F5 es `SIN-GANADOR-UNICO` y en los pilotos el piso ganó.
3. **SI** se cita `SIN-GANADOR-UNICO` **ENTONCES** viaja con el 68.88 % y con la inversión por grupo — **PORQUE** sin ellas afirma una resolución que el panel no tiene.
4. **SI** se usa M para organizar evidencia, aplicar reglas o construir escenarios **ENTONCES** se puede, acreditando **esa** función — **PORQUE** D1 las conserva y las distingue de la precisión predictiva.
5. **SI** un duelo futuro compara brazos **ENTONCES** incluye el piso, con reglas fijadas antes de ver resultados — **PORQUE** ganarle a L no acredita ganarle a un piso.
6. **SI** se cita B **ENTONCES** se declara que no es ciega y que es diagnóstico — **PORQUE** su contaminación es total por construcción.
7. **SI** se quiere abrir F6 **ENTONCES** primero familias elegibles con acceso y consumidor, y cero llamadas antes — **PORQUE** hoy hay 0 elegibles.
8. **SI** una fuente no permite el estimando **ENTONCES** la abstención es el resultado correcto — **PORQUE** las 16 abstenciones de F5 fueron válidas.
9. **SI** dos cifras vienen de universos distintos **ENTONCES** no se restan ni se ordenan juntas — **PORQUE** A.10 corolario 2.
10. **[NUEVO]** **SI** existe dato público de la celda (sus marginales de la misma ola) o de su ola anterior por eje **ENTONCES** el estimador de la celda es el piso, adoptado, con su intervalo — **PORQUE** en 20 celdas de dos dominios ningún candidato lo venció, y la firma de mesa del 17/sep lo fija.
11. **[NUEVO]** **SI** no existe piso para una celda **ENTONCES** el motor puede emitir, **rotulado como escenario**, no como estimación — **PORQUE** su credencial para extrapolar es haber vencido pisos donde los hay, y hoy esa credencial es cero en dos dominios.
12. **[NUEVO]** **SI** se quiere mejorar el piso en celdas de cruce **ENTONCES** no se hace añadiendo la interacción de la ola anterior por celda — **PORQUE** en TRA empeora el MAE (1.57 → 2.85); lo que queda por probar es la interacción agregada o encogida.
13. **[NUEVO]** **SI** se compara el emisor con el árbitro en la ola actual por eje **ENTONCES** no se compara — **PORQUE** 89 de 97 celdas son el mismo número.
14. **[NUEVO]** **SI** se cita el marcador por segmento **ENTONCES** se cita con fecha y con sus cuatro números derivados — hoy 117 celdas, 20 evaluadas, 0 con valor añadido, 20 adoptadas, 74 sin piso — **PORQUE** cambia con cada acto de caja, y sin fecha describe otro árbol.
15. **[NUEVO]** **SI** se cita el contador de corridas selladas **ENTONCES** se dice si es el de la vista o el del disco — **PORQUE** hoy difieren en 16 y el que circula (82) es el menor.

---

## 6 · Módulo de auditoría de rigor extremo

Este documento afirma algo sobre el modelo; el módulo es obligatorio. Contestado, no recitado.

**[NUEVO v2.3] ¿Cuántos contadores movió el trabajo que produjo este artefacto?** **Cero.**

**¿Qué parte del análisis podría estar confundiendo pobreza, desigualdad, violencia o informalidad con «cultura»?** Ninguna afirmación de este informe es sobre conducta mexicana: todas son sobre el aparato de medición. Las dos celdas-D adjudicadas condicionan una conducta financiera y una de trámite a ejes estructurales (localidad, edad, escolaridad, dominio urbano-rural) y **no atribuyen mecanismo**: un piso adoptado dice qué número usar por celda, no por qué la celda es así.

**¿Qué parte podría estar sobregeneralizando desde clases medias urbanas?** F5 hereda las coberturas nacionales de sus encuestas y sobrepondera un dominio cívico (§3.1). Los pilotos, al contrario, entran por primera vez a rural (`localidad <15 000`, `dominio rural`) y a escolaridad hasta primaria — con `n` mínimos de 980 y 769, declarados. El universo de `formalidad` del árbitro cubre solo a quien trabaja (69 %) y por eso no entró como eje en ningún piloto.

**¿Qué parte está sesgada por literatura escrita desde marcos estadounidenses o europeos?** L es un modelo entrenado mayoritariamente en inglés; en DIN erró ~10 pp más que el piso y en TRA no entró. El informe no lee nada de L como conocimiento del caso mexicano. La capa E1 lleva la marca de procedencia de cada parámetro justamente para que un coeficiente importado no se lea como medido.

**¿Qué hallazgos cambiarían si el foco fuera México rural, indígena o popular?** Los pilotos ya estratifican por localidad y dominio; lo que no hay es piso para 74 celdas marginales, incluidas todas las rurales por eje. Indígena-comunal queda fuera por diseño (Bloque A).

**¿Qué parece psicológico pero en realidad es un incentivo racional ante un entorno específico?** No aplica: este documento no interpreta conducta. Su análogo de aparato: que un candidato «con interacción» empeore **parece** falta de interacción en la población y en realidad es **ruido por celda entre olas** (4/12 y 5/12 intervalos que excluyen cero). Confundirlos llevaría a descartar la interacción en vez de a estimarla mejor.

**¿Dónde hay evidencia débil pero intuición social fuerte?** En leer «0 con valor añadido» como «el modelo no sirve» — o «el piso gana» como «ya no hace falta modelo». El dato dice que donde hay dato público el dato manda, y que donde no lo hay el modelo todavía no ha demostrado saber más.

**¿Qué conclusiones serían peligrosas si alguien las usara de forma simplista?** Cuatro: (a) «el emisor y el árbitro coinciden, el motor acierta» — coinciden porque uno copió al otro; (b) «la interacción no existe» — solo estos candidatos no la explotan; (c) «82 corridas selladas» — son 98 en disco; (d) «`edad` es equivalente, luego el modelo y el árbitro comparten segmentación» — es **un** eje de doce.

**[NUEVO v2.1] ¿Qué afirmación describe el estado del corpus y no fue derivada, sino escrita a mano?** Ninguna: cada conteo (82/16/24/40, 97/89, 1/2/1/11, 43 y 24/8/4/0, 117/20/0/20/74, 4 405, 215, 543) trae comando o cita en el anexo §A.9–A.13. La única cifra de fuera del repositorio es la propia firma de mesa del 17/sep, citada verbatim.

**[NUEVO v2.2] ¿Qué deuda «asumida a propósito» debe re-examinarse porque cambió la función del programa?** Dos. La de la v1.0 —«0 familias retenidas» para F6— sigue viva y empeoró (0 elegibles). La nueva: «cero adopción al motor» fue coherente mientras el motor era una matriz sin parámetros; desde `ADR-531` el motor es un conjunto de estimadores por celda, y **no adoptar el piso que nadie vence era dejar al motor sin segmento por inercia**. La firma del 17/sep la retira.

**[NUEVO v2.4] ¿En qué escala están las cantidades, y contra qué se comparan?** Todos los MAE están en **puntos porcentuales de una proporción ponderada**, comparados contra **R** en la misma celda y la misma ola. Los pisos adoptados son proporciones `[0,1]` por celda con IC; ninguna se compara contra un índice ni un coeficiente. Los 43 parámetros de la capa E1 llevan escala declarada o `NO-DECLARADO-EN-CANON`, y ninguno entra a un cómputo desde este documento.

---

## 7 · Procedencia

Todo lo citado está sellado en el repositorio; el anexo da ruta y comando por cifra. Lo que cambió desde la v1.0 en materia de procedencia: **D-A sí existe** (`CALC-TRIADA-B-PISO-0001`), y la tabla de 9 celdas de §A.3 queda sostenida por él; el adversarial de Astra sobre la lectura F5 y la propia lectura siguen siendo documentos de mesa fuera del árbol y no se citan como leídos; el diseño del marcador y la firma del 17/sep están archivados como insumos de dirección y se citan por su sha en el anexo.

**Anexo técnico:** `canon/informe-programa-v1_1-ANEXO.md` (anexo v1.0 verbatim + §A.9–A.13).
