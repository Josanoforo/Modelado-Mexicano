<!-- PROCEDENCIA: insumo de DIRECCIÓN, pegado por mesa en la conversación de dirección el 15/sep/2026. Es la LECTURA ESTRATÉGICA F5 v1.1 que NC-0219 pide: la versión corregida tras el adversarial de Astra, y la que la FIRMA DE MESA del 15/sep cita. Archivada verbatim por ACTO GEN2-ARCHIVO-LECTURA-F5-1. sha256 del adjunto original: a51daa0976e765221972b203f4838702d84bf1c29b9507211102f41534f2da63 -->

# LECTURA ESTRATÉGICA · F5 leída entera · v1.1 · 15/sep/2026
**Dirección → mesa. v1.1 tras el adversarial de Astra (15/sep); cada corrección marcada [CORREGIDO] fue verificada por dirección contra el repo con comando (`celdas.tsv` del sucesor, `resultados.tsv`, spec B-MARCO, `adq-demanda-activa-v1_0.json`). Derivada de `582d4e93`+#785. Cada cifra trae su universo (A.10); nada se compara entre universos distintos (A-bis 4).**

---

## 1 · Lo que sabemos, con su universo

**Primaria — `CALC-TRIADA-0002`, SELLADA, U3 = 12 celdas de 14** [CORREGIDO: CIV-M-01/02/04/10/12/13, FAM-M-01/05/06/07, TRA-M-02, **TRA-M-03**]. MAE (pp) sobre U3: L_CORPUS 3.889 < L_SOLO 3.957 < M 4.987; las tres pareadas INCONCLUSO → **SIN-GANADOR-ÚNICO**. Ningún brazo se adopta.

*Lo que dice y lo que no* [CORREGIDO]: "M último" es una **descripción de este panel, no un diagnóstico del motor**. Las seis celdas cívicas concentran **68.88%** del error de M; una sola celda concentra 54.17% del error de ambos L. Con igual peso a los cinco grupos presentes en U3 el orden puntual **se invierte** (M 5.028 < L_SOLO 7.315 < L_CORPUS 7.529) — sin adjudicar nada tampoco. La conclusión honesta: **ningún contendiente es fiablemente mejor; M es el peor en el bloque cívico, L es el peor en las celdas sueltas, y el veredicto depende de la composición del panel.**

**El diagnóstico de alineación** (aprendizajes §2): parte de la evaluación compara unidades, códigos y periodos distintos (M calibrado a ENVIPE 2025 persona enfrentado a olas históricas de otro estimando). [CORREGIDO] Eso **impide atribuir el error a `p`, y tampoco valida `p`**. La formulación defendible: *primero comparar el mismo estimando, después medir el error residual*. El contrato de selección afirmativa (ya fusionado) mejora el uso; no demuestra mejor predicción.

**B — qué es y qué mide** [CORREGIDO, el error más importante de la v1.0]. B no es medición directa del objetivo. La spec B-MARCO lo define: `B(celda) = p(última ola de la MISMA serie disponible al corte)`. Es **persistencia temporal** — la regla más simple posible. Sobre las **9 celdas comunes** de U3 con B (6 cívicas + 3 remesas ENIGH), tabla derivada del repo:
| contendiente | MAE (pp), 9 celdas |
|---|---|
| **B · persistencia** | **0.885** |
| L_CORPUS | 1.223 |
| L_SOLO | 1.481 |
| M | 4.638 |

B yerra menos que M en 7 de 9. *Lo que dice y lo que no:* una regla trivial es una **referencia competitiva** y M está a cinco veces de ella donde hay serie. No dice que "medir supera al motor": dice que **M no ha demostrado valor sobre el piso más simple**. El subconjunto es solo cívico y remesas: no acredita superioridad general de nadie. (Los MAE de L de NC-0180 —11.9/21.3— son de otro snapshot y otro universo: no se mezclan.)

**Secundaria — RUN-2, PR #764.** 2 celdas × 2 brazos × 8 réplicas; dirigido 8/8 y 8/8, control 0/8 y 0/8; 16/16 trazables. [CORREGIDO] Es **éxito observado completo en las dos celdas evaluadas, con paquetes fuente preparados**; son 8 repeticiones de 2 tareas, no 16 tareas. No prueba que el servicio encuentre fuentes nuevas por sí mismo, seleccione reactivos ni construya paquetes. Cierra **NC-0152** por producto (el diseño 2×2×8 que pedía corrió y cumplió), conservando intacta la primaria.

**F6 / FP-374** [CORREGIDO — la v1.0 mezclaba dos experimentos]. La hipótesis de FP-374 es la **ventaja de M frente a L_SOLO en familias retenidas** (`d_f = error_M − error_L_SOLO`, H0: E[d_f] ≥ −0.02, unidad inferencial = familia): 6 piloto + 12–30 confirmatorias, lista previa con consumidores y reserva. **No** es "¿escala la recuperación documental?" — ése sería otro experimento, con otro diseño. Al 11/sep: 0 familias retenidas. Y dos cosas que la v1.0 daba por hechas y no lo son: (i) B extendido, EDER y el lote **no son familias retenidas** — sus resultados ya se vieron; retenida es la que no se ha evaluado; (ii) **el servicio de adquisición no está llenando ese panel**: NC-0161/0162 están rutadas `ESPERA_O_DELEGADA`, excluidas de investigación automática.

---

## 2 · La lectura, v1.1

**La tesis que se sostiene** (y es la de Astra, adoptada): tenemos **mediciones reproducibles** (72 corridas selladas, cadena completa), **éxito documental local** (dos celdas, paquetes preparados) y **una referencia temporal simple que es competitiva** (persistencia). **Todavía falta demostrar qué valor añade M y dónde.** Reservar M "para donde no hay fuente" no lo valida: ahí M se presenta como **escenario o hipótesis** mientras se reúne evidencia — no como estimador acreditado.

Lo que sí cambia de fase, sin cambiar la tesis: el programa ya produce números con procedencia y ya sabe recuperar puntos documentales; la fase de cálculo (medir, cablear en bloque) ya empezó. Lo que M sea en el informe depende de un experimento que aún no ha corrido.

---

## 3 · Las tres decisiones, corregidas

**D-A · B como piso.** El reanálisis descriptivo **ya está hecho** (tabla de §1, reproducida en el repo). Lo que falta es **sellarlo**: una corrida de registro (`CALC-TRIADA-B-PISO-0001`, nube, cero llamadas) que congele la comparación en las 9 celdas comunes con |error| por celda y, si se quiere adjudicar, las pareadas con IC — con B-bis declarado (qué significa que B no refute). Consume B-MARCO (cierra NC-0187 por consumo, no por adopción); cierra NC-0180. *Recomendación: hacerlo, como sello de lo que ya sabemos, no como investigación nueva.*

**D-B · Qué es F6, antes de cuántas familias.** Primero elegir **cuál experimento**: (1) transferencia de M vs L_SOLO en familias retenidas (el protocolo de FP-374 tal cual), o (2) recuperación documental en **tareas nuevas** no preparadas (otro diseño, todavía sin escribir). Después el panel: familias retenidas = fuentes **adquiridas y no evaluadas**, y eso requiere rutear NC-0161/0162 (o una adquisición dirigida explícita) — hoy nadie las está buscando. FP-374 no se re-sella ni se vence hasta que exista esa lista; hoy sigue vigente y correcta. *Recomendación: decidir (1) vs (2) en esta conversación; lo demás es consecuencia.*

**D-C · El informe.** Escribirlo **ahora**, con lo que hay: primaria SIN-GANADOR-ÚNICO con su dependencia de composición declarada; B como **diagnóstico** (piso de persistencia), no como tesis; secundaria como éxito local; F6 como propuesta pendiente con su gate. *Recomendación: sí, tras sellar D-A; y el informe dice de M lo que la evidencia dice: valor por demostrar.*

---

## 4 · Cierra por producto (firma, no encargo)
- **NC-0152** → CERRADA citando #764 (tratamiento sucesor cumplido; primaria intacta).
- **NC-0161 / NC-0162** → su ruteo es la decisión D-B(ii): salen de ESPERA solo si mesa elige el experimento (1) y ordena la adquisición dirigida.
- **NC-0180 / NC-0187** → cierran con D-A.

## 5 · Preguntas para la conversación
1. ¿Aceptas la tesis de §2 — mediciones reproducibles + éxito documental local + persistencia competitiva, y **M con valor por demostrar**? Es la premisa del informe y cambia cómo se presenta el motor.
2. D-A: ¿sello del reanálisis hoy (barato, nube)?
3. D-B: ¿F6 es transferencia de M (protocolo FP-374) o recuperación documental en tareas nuevas? Una sola, primero.
4. Si es (1): ¿ordenas la adquisición dirigida de familias retenidas — sacar NC-0161/0162 de espera? Sin eso F6 no tiene panel.
5. ¿El informe lo quieres como documento del programa o para lector externo?
