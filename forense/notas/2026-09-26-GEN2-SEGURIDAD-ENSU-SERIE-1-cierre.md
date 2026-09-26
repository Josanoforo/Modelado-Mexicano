**15 conductas con piso GEN2 por dominio: VIOLENCIA 12 · CONFIANZA 3** (VEJEZ = segmento `EDAD-60-MAS` de las 15, no conducta aparte). CALC sellados `cuenta_gen2: SI`, `adopta: NO`. Nada se evalúa prospectivamente: todo es RETROSPECTIVA.

# ACTO GEN2-SEGURIDAD-ENSU-SERIE-1 · nota de cierre

25–26/sep/2026 · CAJA · Opus 5.5 · MODO AUTÓNOMO · rama `gen2-seguridad-ensu-serie-1` · 0-bis
`591689ab` · COMMIT-1 `40f5c9a9` · ADR `ADR-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-01`.
Spec `forense/prereg-caja/ENSU-SERIE-spec-v1_0.md`; lista `forense/analisis/seguridad-ensu/lista-cerrada-P1.md`.

## 1 · Qué se selló

| CALC | qué | RESULT | verify aislado |
|---|---|---|---|
| `CALC-ENSU-PISOS-0001` | 2024T1, 2025T3, 2025T4 × 15 conductas × {TOTAL, SEXO, EDAD, ENT, CIUDAD} | 23 243 | REPRODUCE / IDENTICO |
| `CALC-ENSU-SERIE-0001` | 48 trimestres 2013T3–2025T4 × 15 conductas × {TOTAL, SEXO, EDAD} + C01 × CIUDAD; τ² y dictamen | 33 776 | REPRODUCE / IDENTICO |

Evidencia: `forense/analisis/seguridad-ensu/evidencia-replay-seguridad-ensu-2026-09-26.json`, dos filas en
`forense/replay-evidencia.tsv`. Control cruzado pre-registrado (spec §8.2): 2 356 celdas comunes a los dos
CALC, **0 distintas** (Δ máx = 0). Tablas por id: `tabla-serie-v1_0.tsv` (13 183 celdas conducta × eje ×
categoría × ola) y `tabla-dictamen-ensu-v1_0.tsv` (201 series). Mapa: las 7 afirmaciones ENSU de la cola
v1.1 pasan a `MEDIBLE-EN-CORPUS` (`redictamina_v1_1.py --verifica` OK; inventario de textos del FD
`inventario-reactivos-ensu-v1_0.tsv`).

**Ejecución previa declarada (§6 Commits):** la primera invocación de `run CALC-ENSU-SERIE-0001` se negó
en preflight (árbol sucio: `NO-EJECUTADO`) y la segunda murió con la sesión antes de escribir nada
(`resultados.json` no existió). Procedimiento y semilla intactos; ningún valor visto. El sello `31fa9e47`
es el primer resultado.

## 2 · Bloque C · CONFIRMA / MATIZA / ROMPE (regla congelada en spec §8.3: dentro del IC95 → CONFIRMA; fuera a ≤ 3 pp → MATIZA; fuera a > 3 pp → ROMPE)

Prefijo de id: `RESULT-ENSU-PISOS-`. Cifra del report entre corchetes.

| afirmación | cifra del report | RESULT (punto, IC95) | veredicto |
|---|---|---|---|
| VIOL-003 inseguro vivir en su ciudad, 2025T3 | [63.0] | `C01-INSEG-CIUDAD-2025T3-TOTAL-TODOS` 0.630 (0.622–0.638) | **CONFIRMA** |
| VIOL-014 mujeres / hombres, 2025T3 | [68.2 / 56.7] | `…-2025T3-SEXO-MUJER` 0.682 (0.671–0.693) · `…-SEXO-HOMBRE` 0.567 (0.554–0.580) | **CONFIRMA** |
| VIOL-014 mujeres inseguras en cajero | [77.8] | `C03-INSEG-CAJERO-2025T3-SEXO-MUJER` 0.778 (0.768–0.788) | **CONFIRMA** |
| VIOL-035 Culiacán, Irapuato, Chilpancingo | [88.3, 88.2, 86.3] | `C01-…-2025T3-CIUDAD-40/92/22` 0.883, 0.882, 0.863 | **CONFIRMA** (×3) |
| VIOL-035 San Pedro G.G., Benito Juárez, Piedras Negras | [8.9, 15.6, 15.0] | `C01-…-2025T3-CIUDAD-65/83/08` 0.089, 0.156, 0.150 | **CONFIRMA** (×3) |
| INTER-034 inseguridad, mar 2024 | [61] | `C01-INSEG-CIUDAD-2024T1-TOTAL-TODOS` 0.610 (0.602–0.618) | **CONFIRMA** |
| VIOL-038 corrupción con autoridad de seguridad | [47.2] | `C15-CORRUPCION-POLICIA-2025T4-TOTAL-TODOS` 0.454 (0.431–0.476) | **CONFIRMA** (el report no da ola; se midió la última abierta) |
| VIOL-001 visitar parientes, T3 / T4 | [22.4 / 23.9] | `C11-…-2025T3/T4-TOTAL-TODOS` 0.219, 0.234 | **CONFIRMA** |
| VIOL-001 objetos de valor, T3 / T4 | [40.6 / 42.5] | `C09-…-2025T3/T4` 0.392, 0.411 | **MATIZA** (1.4 pp debajo) |
| VIOL-001 caminar de noche, T3 / T4 | [35.0 / 37.1] | `C10-…-2025T3/T4` 0.338, 0.358 | **MATIZA** (1.2–1.3 pp) |
| INTER-034 / SANC-007 joyería-efectivo, mar 2024 | [47.4] | `C09-…-2024T1` 0.459 (0.450–0.468) | **MATIZA** (1.5 pp) |
| INTER-034 caminar de noche, mar 2024 | [40.8] | `C10-…-2024T1` 0.394 | **MATIZA** (1.4 pp) |
| VIOL-001 menores salgan solos, T3 / T4 | [36.9 / 38.0] | `C12-HABITO-MENORES-2025T3/T4` 0.293, 0.295 | **ROMPE** por la regla (7.6–8.5 pp) |

**Lectura (no cambia los veredictos).** Las cifras de percepción reproducen el comunicado INEGI al decimal:
el medidor, el ponderador y el denominador de C01/C03/C15 son los de INEGI. En los hábitos la diferencia es
**de denominador, no de dato**: la lista §3 dejó «No aplica» dentro del universo de C09–C12 (declarado antes
de abrir); todo indica que el comunicado lo excluye (el hueco crece justo donde «No aplica» es grande:
hogares sin menores en C12). Es una diferencia de **universo** (v2.16 §4: un estimando restringido no se
compara contra uno poblacional): el ROMPE de C12 dice «la cifra del report no es la proporción de adultos
urbanos», no «el report se equivoca». No se re-mide aquí (procedimiento congelado, PARO d): sucesor
`CALC-ENSU-PISOS-0002` con universo sin «No aplica» (NC-…-03). Afirmación del report que sí se sostiene
con cualquier denominador: el miedo reorganiza la conducta de ≥ 1 de cada 5 adultos urbanos en cada hábito.

## 3 · Serie 2013–2025 y dictamen DONDE-CAMBIO (vocabulario #1125)

**τ² de persistencia (parámetro nuevo reutilizable, logit²):** trimestral
`RESULT-ENSU-DICTAMEN-TAU2-TRIMESTRAL-{TOTAL,SEXO,EDAD,CIUDAD}` = 0.0154, 0.0189, 0.0211, 0.1182;
semestral (C15) `…-TAU2-SEMESTRAL-{TOTAL,SEXO,EDAD}` = 0.0060, 0.0129, 0.0196. La ciudad persiste mucho
menos que el agregado (τ² ×7.7): un piso de ciudad del trimestre anterior predice el siguiente con un IC
mucho más ancho que su IC muestral.

**Conteo (201 series, 0 sin dictamen):** agregadas (105): ESTABLE 76 · SALTO-DE-INSTRUMENTO 11 ·
SALTO-SIN-EXPLICAR 11 · CAMBIO-SOSTENIDO 7 · SIN-SERIE 0. Ciudad, C01 (96): ESTABLE 43 · SALTO-SIN-EXPLICAR
40 · CAMBIO-SOSTENIDO 13.

**Lo que sí cambió (agregado):**
- **C05 «la delincuencia empeorará en 12 meses» — CAMBIO-SOSTENIDO BAJA** en TOTAL (2016T1–2025T4,
  `…-C05-EXPECT-EMPEORA-TOTAL-TODOS-DELTA-PP` = −7.8 pp), HOMBRE, MUJER, 18-29, 45-59 y 60-MAS (60-MAS
  −17.2 pp). El pesimismo a 12 meses bajó de forma sostenida; la percepción presente (C01) no.
- **C12 menores, 60-MAS — CAMBIO-SOSTENIDO SUBE** (+12.2 pp). Único hábito con cambio sostenido.
- **C01 inseguridad en la ciudad, TOTAL** 2013T3–2025T4 (k = 48): SALTO-SIN-EXPLICAR (1 par fuera),
  −4.2 pp netos. No hay cambio sostenido de la percepción agregada en doce años.
- **C14 efectividad de la policía municipal: SALTO-DE-INSTRUMENTO en los 7 segmentos** (el par 2020T1→2020T3,
  R2, cae fuera): el salto coincide con el cambio documentado de 2020, no se atribuye a la policía.
- C02 (calle): SALTO-SIN-EXPLICAR en los 7 segmentos (un par fuera, en todos a la vez: señal de trimestre,
  no de segmento). C03, C04, C06, C07, C10, C11, C13: ESTABLE en todos los segmentos.

**Dictamen por ciudad (C01) — CAMBIO-SOSTENIDO (13):** SUBE: 02 Mexicali (+12.8 pp netos), 03 Tijuana
(+3.0), 05 Campeche (+19.4), 09 Colima (+19.0), 36 Puebla (+14.7), 41 Mazatlán (+22.9), 89 Cuautitlán
Izcalli (+10.5); y 04 La Paz, 22 Chilpancingo, 25 Puerto Vallarta, 45 Villahermosa con **dirección SUBE
pero Δ neto negativo** (−15.5, −2.2, −9.9, −6.0: la mayoría de saltos fuera de banda sube, pero el tramo
termina abajo — series volátiles, auditoría §5). BAJA: 11 Tuxtla Gutiérrez (−8.9), 65 San Pedro Garza
García (−24.8). Cada cifra: `RESULT-ENSU-DICTAMEN-C01-INSEG-CIUDAD-CIUDAD-<cd>-{DICTAMEN,DIRECCION,DELTA-PP}`.

## 4 · Defectos declarados (no cambian ningún sello)

1. **2017T1 sin sexo/edad:** `RESULT-ENSU-SERIE-G-2017T1-JOIN-SIN-CS` = 14 497 (todas las personas). La
   llave 2016–2020 no casa en ese trimestre; las cuatro columnas de llave (`UPM VIV_SEL H_MUD` + `R_SEL`/`N_REN`)
   existen en ambas tablas, así que la causa (formato de valor) **no está diagnosticada** aquí.
   Efecto: las series SEXO/EDAD tienen el tramo 2017T2–2025T4 (k = 33) en lugar de 2016T1+; TOTAL y CIUDAD
   intactos. Código congelado → no se parcha (NC-…-02).
2. 2020T3/T4: 279 y 161 personas sin pareja CS; 378/224 llaves CS duplicadas (fuera de SEXO/EDAD).
3. Era 2013–2015: ≈ 2 000 personas por trimestre (32 ciudades) frente a 10 000–24 000 desde 2016; reserva
   ETIQUETA-INFERIDA-E1 (lista §3) en toda cifra 2013–2015.

## 5 · Módulo de auditoría de rigor extremo

- **¿Violencia confundida con cultura?** No se atribuye nada a «el mexicano»: percepción y hábitos son
  respuesta a un entorno; la ciudad explica más varianza que cualquier segmento (Culiacán 0.88 vs San Pedro
  0.09 el mismo trimestre).
- **¿Sobregeneralización urbana?** ENSU es sólo urbana (ciudades de interés); nada aquí habla del México
  rural. El «nacional» de ENSU cambió de 32 a 90 ciudades (R3): los pares con cambio de universo se
  dictaminan como CAMBIO-DOCUMENTADO, no como cambio de conducta.
- **¿Escala?** Todas las cifras: proporción de personas 18+ (C15: de quienes tuvieron contacto con
  policía). Ninguna se promedia con cifras de delito u hogar. Sin enlace, no se compara con ENVIPE.
- **¿Qué parece psicológico y es adaptación racional?** Dejar de salir de noche o de llevar objetos de valor
  es gestión de riesgo; que ≈ 30 % de adultos restrinja a menores (C12) es crianza bajo amenaza, no rasgo.
- **¿Qué sería peligroso leído simplista?** «DIRECCIÓN SUBE» de cuatro ciudades con Δ neto negativo; el
  rótulo del dictamen no es el signo del efecto neto. Y los ROMPE de C12: son de universo, no de dato.
- **¿PROSPECTIVA/RETROSPECTIVA?** Todo RETROSPECTIVA; las cifras de los reports se vieron antes de congelar
  (spec §0) y no hubo predicción. **¿Cifra escrita a mano?** Ninguna: cada cifra de esta nota cita su id.
- **¿Contadores movidos?** «N conductas con piso GEN2»: +15 (VIOLENCIA 12, CONFIANZA 3). `celdas_validadas`:
  219 → 219 (este acto no adjudica celdas).

## 6 · Sucesores

Familia 2027 de ENSU trimestral (PROSPECTIVA: el primer trimestre 2026 publicado después de un sello de
emisión) — propuesta, candidata natural por frecuencia. `CALC-ENSU-PISOS-0002` (hábitos sin «No aplica»).
Series por ciudad de C02–C15. Llave 2017T1. FIRMAS-20 (FP de este acto), catálogo v1.2.
