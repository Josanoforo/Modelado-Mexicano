# Cobertura del modelo por clase AMAI · P4 · GEN2-CLASE-AMAI-1 · RETROSPECTIVA

Contadores movidos por este trabajo: seis CALC sellados (`cuenta_gen2: SI`, `adopta: NO`) y «conductas con piso por NSE» de 0 a **28**. Toda cifra de abajo sale de `resumen-p4-v1_0.json`, `pisos-nse-v1_0.tsv`, `potencia-alto-bajo-v1_0.tsv` y `cobertura-u1-por-clase-v1_0.tsv`, derivados por `python3 -m tools.dominios.amai.cobertura` de los `resultados.json` sellados; la tabla completa conducta × grupo × ola está en `tabla-conducta-nse-ola-v1_0.md`.

## 1 · NSE construido y validado (P2)

| CALC | Dictamen P1 | Validación contra AMAI (Figura 1, ENIGH 2022) | Desvío máx. grupo / nivel (pp) |
|---|---|---|---:|
| `CALC-AMAI-NSE-ENIGH-2022-0001` | CALCULABLE | **CALCULABLE-REPRODUCE-AMAI** | 0.07 / 0.05 |
| `CALC-AMAI-NSE-ENIF-2021-0001` | APROXIMABLE | APROXIMACION-CONFORME | 0.35 / 0.43 |
| `CALC-AMAI-NSE-ENIF-2024-0001` | APROXIMABLE | APROXIMACION-CONFORME | 3.01 / 3.93 |
| `CALC-AMAI-NSE-ENDUTIH-2023-0001` | APROXIMABLE | APROXIMACION-CONFORME | 4.72 / 3.85 |
| `CALC-AMAI-NSE-ENDUTIH-2024-0001` | APROXIMABLE | **APROXIMACION-DESVIADA** | 6.97 / 4.90 |
| `CALC-AMAI-NSE-ENDUTIH-2025-0001` | APROXIMABLE | **APROXIMACION-DESVIADA** | 9.72 / 5.55 |

ENIGH 2022 reproduce la distribución publicada por AMAI a menos de 0.05 pp por nivel: el procedimiento es la regla, no una lectura de ella. La aproximación ENDUTIH aplicada a los propios hogares ENIGH 2022 clasifica igual que la regla exacta al 84.8 % de hogares por grupo y al 60.5 % por nivel (`RESULT-AMAI-NSE-ENIGH-2022-PROXY-ENDUTIH-CONCORDANCIA-GRUPO|NIVEL`). Las dos olas ENDUTIH `DESVIADA` mueven masa de BAJO a MEDIO (BAJO 42.0 % en 2024 y 39.3 % en 2025 contra 49.0 % de referencia): mezcla de deriva real 2022→2025 (internet fijo al alza) y del sesgo de imputar desde 2022; este acto no separa las dos. Sus pisos se publican con el rótulo y **no** deben leerse como distribución de clase de su año. Los conteos de hogares con y sin NSE están en los RESULT `-N-HOGARES-CON-NSE|SIN-NSE` de cada CALC.

## 2 · Cobertura del modelo por clase (la cifra del §3)

- **Catálogo U1** (`forense/analisis/catalogo/inventario-consumo-gen2.tsv`, filas vigentes, sin pisos históricos ni sellados de contexto): 69 identidades; 14 son celdas o interacciones (L×E, `R`), quedan **55 identidades de conducta**.
- Con piso por NSE: **17 de 55** (15 directas + 2 reglas de ejes cuya conducta base se midió por NSE sin extender sus cruces). En celdas conducta × grupo: **49 de 165** publicables (29.7 %). Por grupo: BAJO 17, MEDIO 16, ALTO 16 — la única conducta sin MEDIO ni ALTO es `desconfia_conoce_proteccion` (n = 130 y 52 < 200, SUPRIMIDA-N).
- **Donde el modelo no tiene nada por clase:** 23 de 55 identidades (41.8 %) son de ENVIPE (18) y ENCIG (5) — victimización, denuncia, evasión de norma, trámites y mordida —, instrumentos donde el NSE AMAI es NO-CONSTRUIBLE por texto (P1). Otras 14 identidades son de instrumentos fuera del alcance AMAI de este acto (ENCUCI, EDER, ENSANUT, ENUT, LAPOP, Banxico, MOTRAL, ENNViH, ENFIH) y una es el complemento `no_recibe_remesas`, no medido aparte.
- **Fuera del inventario U1:** las diez medidas ENDUTIH adoptadas por FIRMAS-15 T: 90 celdas (10 × 3 grupos × 3 olas), 88 publicables; dos `VARIANZA-NO-ESTIMABLE` en `no_celular_cobertura` (tasa ~0.1–0.7 %).
- En total: **28 conductas con piso por NSE**, 144 celdas, 140 publicables.

Lectura: el sesgo de clase que el §3 dice que «más muerde» sólo puede medirse hoy en dinero (ENIF), remesas (ENIGH) y tecnología (ENDUTIH). Todo lo cívico y de trato con el Estado —la mitad de lo que el modelo afirma— no tiene corte AMAI posible con las encuestas del corpus; el único corte socioeconómico disponible allí es la escolaridad (ya eje del marcador), que es un componente, no la regla.

## 3 · Potencia medida y FP (¿entra NSE al marcador como eje?)

Contraste ALTO − BAJO con IC95 por réplica compartida (mismo plan de UPM en los tres grupos): **37 de 48** conductas-ola despejan 0; 9 no; 2 no estimables. ENIF: 15 de 17 (semiancho mediano del IC por grupo 1.8–2.5 pp); ENDUTIH: 21 de 30 (0.9–1.4 pp); ENIGH: 1 de 1 (0.2–0.3 pp). Los que no despejan son razones de «preferencia» (`no_celular_preferencia`, `no_internet_acceso`, `desconfia_no_conoce_proteccion`) y `no_internet_preferencia` en 2024.

**Recomendación (PROPUESTO-POR-EJECUTOR, para FP de mesa):** NSE entra al marcador **como eje, con reserva de instrumento**: sólo ENIGH 2022 (reproducción exacta) y ENIF 2024 (CONFORME, ocupados aproximados); ENDUTIH 2023 como aproximación rotulada; **no** ENDUTIH 2024–2025 (`DESVIADA`) ni ENIF 2021 (sin conducta adoptable). La potencia lo sostiene: con n ≥ 200 por grupo los semianchos son de 1–2.5 pp y 37/48 gradientes se resuelven. Dos condiciones: (i) `internet` y `celular` de ENDUTIH quedan fuera del eje por circularidad (el NSE contiene internet fijo del hogar); (ii) el eje no se compone con escolaridad sin una spec propia, porque la escolaridad de la jefatura es el componente de mayor peso de la regla (85 de 300 puntos). Alternativa: no adoptar y usar NSE sólo como diagnóstico de sesgo de muestra. Mesa decide; este acto no toca el marcador.

## 4 · Módulo de auditoría · ¿qué parece cultura y es clase?

- **«Cortoplacismo del mexicano».** El horizonte de ahorro corto baja 27–28 pp de BAJO a ALTO con y sin seguridad social (`horizonte_corto_con_ss` 53.1 → 25.9 %; `_sin_ss` 63.3 → 35.3 %) y 20 pp entre quienes no trabajan. Lo que se leería como rasgo cultural tiene un gradiente de clase del tamaño del efecto mismo; sin el corte, es sobregeneralizar desde el agregado. Tampoco es sólo clase: dentro de ALTO sigue habiendo 26–35 %.
- **Informalidad del ahorro.** `ahorra_solo_informal` baja con la clase (39.0 → 29.3 %), pero `informal_cualquiera` **sube** (50.1 → 60.8 %): el ahorro informal (tanda, caja, en casa) no es una práctica de pobreza que la formalidad sustituye, sino que se suma; lo que la clase compra es la vía formal (15.2 → 46.0 %). Leer la informalidad como «desconfianza cultural» ignora que la oferta formal sigue la clase (§3: oferta antes que preferencia).
- **Desconfianza.** Citar desconfianza o mal servicio como razón principal de no tener cuenta no tiene gradiente de clase medible (Δ −1.2 pp, IC que incluye 0): esa sí es candidata a actitud, no a restricción económica — con la reserva de n (grupos ALTO y MEDIO suprimidos en `desconfia_conoce_proteccion`).
- **Familia como seguro.** Recibir dinero de familiares para la vejez baja de 51.6 a 37.7 % y recibir remesas de 5.7 a 2.2 %: el «familismo» observable en transferencias es en parte sustitución de ingreso propio y de pensión, no sólo valor (§3: familismo es evidencia (b) en diáspora; aquí se ve como clase).
- **Tecnología.** No usar internet por **costo** es de clase (13.5 → 2.3 %); por **preferencia** («no le interesa») no lo es en celular y en internet 2024, y sube con la clase en 2023 y 2025. La «brecha digital como desinterés» es un artefacto de juntar razones: la exclusión por costo se concentra abajo. Uso de internet y celular por NSE es circular (ver §3).
- **Escala y unidad.** Remesas es proporción de hogares; ENIF y ENDUTIH son proporciones de personas; ninguna cifra se promedia con otra. Todo es RETROSPECTIVA; ninguna es predicción ni efecto causal de la clase.
- **Dónde la evidencia es débil.** ENDUTIH imputa 122 de 300 puntos desde ENIGH 2022; ENIF aproxima ocupados. El sesgo rural/indígena no se resuelve con NSE: AMAI mide bienes de hogar y en localidades rurales A/B y C+ son raros por construcción (nota, p. 10). Ninguna afirmación de estado del corpus en este documento está escrita a mano: cada cifra tiene su archivo derivado.
