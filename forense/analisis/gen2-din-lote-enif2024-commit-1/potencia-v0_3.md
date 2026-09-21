# Potencia de la regla v0.3 sobre datos ya abiertos — lote ENIF 2024

`tools/lote_enif2024/potencia_v0_3.py`, PCG64(20260921), 20000 lotes simulados por punto. Sellados leídos por id: pilotos 1 (`CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001`), 2 (`CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001`) y 3 (`CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001`). **Reporta la curva; no cambia la regla.**

- Celdas en el pool: **35** puntuadas de 36 nominales (8 + 12 + 15; la 16.ª del piloto 3 está fuera de soporte ex ante); EE del árbitro por celda: mediana 1.92 pp, mín 0.92, máx 4.65.
- Efecto del piloto 3 (15 celdas puntuadas): ΔMAE(S½) = 1.101 pp (sellado 1.101, IC95 [0.256, 1.484]); ΔMAE(Sλ) = 1.465 pp (sellado 1.465, IC95 [0.439, 2.115]). Desviación por celda de Δ_c: 1.319 pp.
- Calibración del ruido: κ = 0.5164 → con las 15 celdas del piloto 3 el EE simulado de Δ̂ es 0.3303 pp (sellado por réplica 0.3303).

| efecto | Δ (pp) | n celdas | P(IC95 despeja 0.5 pp) | P(IC95 despeja 0) | SE medio (pp) |
|---|---|---|---|---|---|
| 0.00 | 0.00 | 15 | 0.007 | 0.095 | 0.293 |
| 0.00 | 0.00 | 35 | 0.001 | 0.093 | 0.192 |
| 0.00 | 0.00 | 44 | 0.001 | 0.095 | 0.172 |
| 0.00 | 0.00 | 68 | 0.000 | 0.093 | 0.138 |
| 0.50 | 0.50 | 15 | 0.095 | 0.441 | 0.293 |
| 0.50 | 0.50 | 35 | 0.095 | 0.658 | 0.193 |
| 0.50 | 0.50 | 44 | 0.095 | 0.736 | 0.172 |
| 0.50 | 0.50 | 68 | 0.095 | 0.865 | 0.138 |
| S-MEDIO | 1.10 | 15 | 0.524 | 0.880 | 0.293 |
| S-MEDIO | 1.10 | 35 | 0.783 | 0.994 | 0.192 |
| S-MEDIO | 1.10 | 44 | 0.851 | 0.999 | 0.172 |
| S-MEDIO | 1.10 | 68 | 0.942 | 1.000 | 0.138 |
| S-LAMBDA | 1.47 | 15 | 0.813 | 0.976 | 0.293 |
| S-LAMBDA | 1.47 | 35 | 0.977 | 1.000 | 0.192 |
| S-LAMBDA | 1.47 | 44 | 0.992 | 1.000 | 0.172 |
| S-LAMBDA | 1.47 | 68 | 0.999 | 1.000 | 0.138 |
| 2.00 | 2.00 | 15 | 0.983 | 0.999 | 0.293 |
| 2.00 | 2.00 | 35 | 1.000 | 1.000 | 0.192 |
| 2.00 | 2.00 | 44 | 1.000 | 1.000 | 0.172 |
| 2.00 | 2.00 | 68 | 1.000 | 1.000 | 0.138 |

**Lectura, escrita antes de medir (spec v1_0 §7):** la potencia depende del efecto real y del ruido por celda; la curva de arriba es una cota superior (celdas tratadas como independientes; el bootstrap real comparte UPM entre celdas). Si con 44 celdas y el efecto del piloto 3 la regla no despeja 0.5 pp con probabilidad alta, **eso se declara antes de abrir y la consecuencia la decide mesa**, no el ejecutor y no después de ver el resultado.
