<!-- PROCEDENCIA: insumo de DIRECCIÓN, pegado por mesa en la conversación de dirección el 15/sep/2026. Es la LECTURA ESTRATÉGICA F5 v1.0, el documento que el adversarial de Astra revisa. NO la pide NC-0219 (que pide la v1.1 y el adversarial): se archiva porque sin ella las marcas [CORREGIDO] de la v1.1 no tienen referente. SUPERADA POR LA v1.1 — no se cita como estado vigente. Archivada verbatim por ACTO GEN2-ARCHIVO-LECTURA-F5-1. sha256 del adjunto original: 7fc366efa7332c0e5cc3f0836ba81a9ca073bc3d9b9a4e9a19f82a2eb4aaa29a -->

# LECTURA ESTRATÉGICA · F5 leída entera · 15/sep/2026
**Dirección → mesa. Derivada de `582d4e93`. Cifras del registro derivado (`corridas.tsv`, `resultados.tsv`) y de cuatro notas: veredicto TRIADA (10/sep), aprendizajes (10/sep), panel-viable (11/sep), cierre RUN-2 (15/sep). Cada cifra trae su universo (A.10); nada se compara entre universos distintos (A-bis 4).**

---

## 1 · Lo que sabemos, con su universo

**Primaria — `CALC-TRIADA-0002`, SELLADA (13/sep), U3 = 12 celdas de 14** (CIV-M-01/02/04/10/12/13, FAM-M-01/05/06/07, TRA-M-02, TRA-M-07). Tres contendientes contra el árbitro R:
| contendiente | MAE (pp) | cobertura |
|---|---|---|
| L_CORPUS (LLM con corpus) | **3.889** | 12/14 |
| L_SOLO (LLM sin corpus) | 3.957 | 14/14 |
| **M (el motor)** | **4.987** | 14/14 |

Las tres pareadas: **INCONCLUSO** (IC95 cruza cero). Veredicto: **SIN-GANADOR-ÚNICO**. 171 estimaciones, 53 abstenciones válidas. Ningún brazo se adopta.
*Lo que dice y lo que no:* nadie gana con significancia — pero el orden puntual pone a **M último**. Y el diagnóstico de aprendizajes §2 dice por qué: la mayor parte del error de M no es aritmética ni evidencia contra `p`; es **uso/evaluación desalineados** (M calibrado a ENVIPE 2025 persona con recorte U1/U4 enfrentado a seis olas históricas de otro estimando). Ese desfase se está cerrando por contrato (selección afirmativa por dominio/evento/ola, ya fusionada). *(Nota A.10: la primera tríada del 10/sep, U3=3, tenía a M primero con MAE 0.18 — quedó VENCIDA EN ALCANCE por fuga del extractor; la limpia es la 0002.)*

**Secundaria — RUN-2, PR #764 (15/sep), 32 posiciones, 2 celdas × 2 brazos × 8 réplicas.** Es, literalmente, el "experimento sucesor" que aprendizajes §6 diseñó y que **NC-0152 pide**: ¿un paquete fuente dirigido recupera puntos válidos donde M y L no los tenían?
| celda | dirigido | control | criterio §4.3 |
|---|---|---|---|
| TRA-M-07 | **8/8** | 0/8 | ✓ margen máximo |
| DIN-M-01 | **8/8** | 0/8 | ✓ margen máximo |

16/16 trazables a fuente nativa, 0/16 con contexto. *Lo que dice y lo que no:* la **recuperación documental dirigida funciona con fiabilidad máxima**; no mide generalización a familias nuevas (eso es F6). Nota: **NC-0152 sigue ABIERTA y ya está resuelta por producto** — cierra citando #764.

**B como piso — NC-0180 (descriptivo, 10 celdas con B, sin IC):** MAE_pp(B)=0.92 < M=4.31 < L_SOLO=11.9 (n=9) < L_CORPUS=21.3. **B yerra menos que M en 8 de 10.** Universo distinto al de la tríada (10 celdas con B vs U3=12; snapshot distinto): los MAE de L **no son comparables** entre las dos tablas — se citan juntos solo para ver el orden. B-MARCO: 471 RESULT sellados (#757), **cero citas**, NC-0187 abierta; el propio registro dice que su consumidor es "el próximo duelo", no el motor.

**F6 / FP-374 (11/sep):** piloto de transferencia = 6 familias **retenidas** (no vistas en desarrollo) + 12–30 confirmatorias; unidad inferencial = familia; 576–1 152 llamadas lógicas. Al 11/sep: 10 familias conocidas, **todas vistas en desarrollo → 0 retenidas**, faltan 18/18. Recomendación en pie: NO AUTORIZAR HOY. Lo que entró después y FP-374 no vio: B extendido (+8 celdas), EDER (69 RESULT), 4 corridas del lote, la secundaria, y **el servicio de adquisición ya corriendo por su cuenta** (#777, #780). Lo que NO sé sin re-derivar: cuántas de esas piezas caen en familias *retenidas* — el split del panel lo decide, y ese conteo es la primera pieza de cualquier acto que abra F6.

---

## 2 · La lectura (lo que dirección concluye leyendo los cuatro juntos)

1. **Donde podemos verificar, el motor no es el mejor estimador — y la medición directa lo es por mucho.** M último en la tríada limpia (sin significancia); B a menos de un punto porcentual del árbitro donde existe. El valor del programa no está en que M *prediga* celdas que podemos medir; está en **medirlas** (B) y en usar M donde no hay fuente.
2. **El error de M es de alineación, no de `p`.** No hay caso para ajustar coeficientes hacia R; hay caso para que cada uso de M declare dominio/evento/ola por contrato (ya en curso) y para que la evaluación cívica compare unidad con unidad antes de volver a medir M.
3. **El proceso documental dirigido es la capacidad nueva, y está probada.** 16/16 vs 0/16 no es un margen: es un mecanismo que convierte "sin punto" en "punto trazable". Es lo que F6 quiere transferir, y es lo que el servicio de adquisición alimenta.
4. **La tríada sin B es una tríada incompleta.** Mientras no se corra con B como piso, ni la adjudicación (INCONCLUSO) ni el rol de M están bien planteados: el piso define qué tan lejos está cada brazo de lo alcanzable.
5. **La fase que sigue es de cálculo, no de transacción** — la misma frase de mesa al firmar la regla de bloque. Medir (caja), cablear (relevo en bloque), y documentar dirigido donde no hay fuente. F6 es la prueba de que lo tercero escala.

---

## 3 · Las tres decisiones, con opciones

**D-A · La tríada con B como piso (NC-0180 + NC-0187).**
- (a) **Autorizar la próxima corrida de tríada con B como piso** — sucesora de `prereg-caja-C0D-MARCADOR`, misma U, pre-registro que declare qué significa que B no refute (B-bis). Consume los 471 RESULT de B-MARCO; NC-0187 se cierra por consumo, no por adopción al motor. Costo: una corrida de registro (nube/caja según pre-registro), cero llamadas.
- (b) Adoptar B al motor. *No*: el registro lo excluye y sería confundir el piso con el estimador.
- (c) Nada. Deja INCONCLUSO sin piso.
**Recomendación de dirección: (a), primero y barato.** Es la pieza que hace legible todo lo demás.

**D-B · F6 y FP-374.**
- (a) Re-sellar FP-374 tal cual contra el universo nuevo (sigue "no autorizar") — si el re-conteo de familias retenidas sigue en cero.
- (b) Declarar FP-374 **VENCIDA EN ALCANCE** y autorizar el **piloto** (6 familias, 192 llamadas) — si el re-conteo da ≥6 retenidas.
- (c) Autorizar F6 sin re-contar. *No*: es firmar sobre evidencia del 11/sep con un universo que cambió cuatro veces.
**Recomendación: la decisión es del re-conteo, no de la opinión.** Un acto de nube deriva familias retenidas contra el snapshot de hoy (el `analiza.py` del panel contra el registro actual + lo que el servicio ya adquirió) y devuelve un número; con ≥6, (b); con menos, (a) y el servicio de adquisición sigue llenando el panel — su demanda ya es exactamente ésa. NC-0161/0162 caen con esta decisión.

**D-C · El informe.**
- (a) Esperar F6 para escribirlo. *No*: F6 tarda semanas y lo que hay ya es un resultado.
- (b) **Escribir el informe con lo que hay, como está**: primaria SIN-GANADOR-ÚNICO con M último y diagnóstico de alineación; secundaria ÉXITO máximo; B como piso (tras D-A); F6 como "en curso" con su gate numérico. Honesto, y es el estado real.
**Recomendación: (b), después de D-A.** El informe se escribe sobre la tríada con piso, no sobre la tríada coja.

---

## 4 · Lo que cierra por producto (sin encargo, con firma)
- **NC-0152** → CERRADA citando #764: el diseño 2×2×8 corrió y cumplió.
- **NC-0161 / NC-0162** → se resuelven con D-B, no aparte.
- **NC-0187** → cierra por consumo cuando D-A corra; nunca por adopción al motor.

## 5 · El orden que propone dirección
1. Firma D-A(a) → tríada con B (corrida barata, cierra 0180/0187).
2. Acto de nube: re-conteo de familias retenidas → devuelve el número que decide D-B.
3. D-B con número: piloto o re-sello; el servicio de adquisición sigue llenando el panel en cualquier caso.
4. Informe (D-C b) sobre la tríada con piso.
En paralelo, caja mide (MEDICION-DEMANDA-2) y el relevo en bloque cierra slots: la fase de cálculo ya empezó.

## 6 · Preguntas para la conversación
1. ¿Aceptas la lectura §2.1 — que el valor está en medir y documentar, y M queda para donde no hay fuente? Es la premisa del informe.
2. ¿D-A(a) hoy, como firma? Es lo único de esta lectura que no necesita esperar nada.
3. ¿Qué umbral de familias retenidas dispara el piloto: los 6 del protocolo, o exiges más?
4. ¿El informe lo quieres como documento del programa (doc) o como informe al lector externo? Cambia el módulo de auditoría que carga.
