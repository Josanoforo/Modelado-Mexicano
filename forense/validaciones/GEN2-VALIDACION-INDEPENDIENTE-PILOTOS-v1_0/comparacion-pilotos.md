# Comparación P2 · propios (commit `19d35aba`, a ciegas) vs sellados

## Piloto 1 · DIN · ENIF 2024 · `localidad × edad` (8 celdas)

| celda | n propio | n sellado | R9 propio | R9 sellado | Δ pp | clase | IC propio | IC sellado | clase IC | C2 propio (marg. sellados) | C2 sellado | Δ pp | clase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L1xE1 | 992 | 992 | 0.491030 | 0.491030 | +0.0000 | IDÉNTICO | [0.4427, 0.5375] | [0.4432, 0.5372] | COINCIDE | 0.486817 | 0.486817 | +0.0000 | IDÉNTICO |
| L1xE2 | 1402 | 1402 | 0.455408 | 0.455408 | +0.0000 | IDÉNTICO | [0.4163, 0.4920] | [0.4184, 0.4918] | COINCIDE | 0.428713 | 0.428713 | +0.0000 | IDÉNTICO |
| L1xE3 | 1194 | 1194 | 0.334074 | 0.334074 | +0.0000 | IDÉNTICO | [0.3022, 0.3660] | [0.3019, 0.3665] | COINCIDE | 0.377824 | 0.377824 | +0.0000 | IDÉNTICO |
| L1xE4 | 1057 | 1057 | 0.325498 | 0.325498 | +0.0000 | IDÉNTICO | [0.2860, 0.3654] | [0.2869, 0.3644] | COINCIDE | 0.323636 | 0.323636 | +0.0000 | IDÉNTICO |
| L2xE1 | 1932 | 1932 | 0.400035 | 0.400035 | +0.0000 | IDÉNTICO | [0.3680, 0.4311] | [0.3682, 0.4304] | COINCIDE | 0.402640 | 0.402640 | +0.0000 | IDÉNTICO |
| L2xE2 | 2854 | 2854 | 0.333258 | 0.333258 | +0.0000 | IDÉNTICO | [0.3065, 0.3612] | [0.3065, 0.3601] | COINCIDE | 0.347773 | 0.347773 | +0.0000 | IDÉNTICO |
| L2xE3 | 2217 | 2217 | 0.324128 | 0.324128 | +0.0000 | IDÉNTICO | [0.2970, 0.3508] | [0.2975, 0.3515] | COINCIDE | 0.301423 | 0.301423 | +0.0000 | IDÉNTICO |
| L2xE4 | 1844 | 1844 | 0.252724 | 0.252724 | +0.0000 | IDÉNTICO | [0.2247, 0.2826] | [0.2237, 0.2820] | COINCIDE | 0.253724 | 0.253724 | +0.0000 | IDÉNTICO |

Marginales de un eje (D9, ENIF 2024) — propios vs `…-G-C2-MARG-*` sellados del CALC de emisiones y vs los públicos del árbitro citados en la spec:

| marginal | n propio | n sellado | p propio | p sellado (CALC) | Δ pp | p público árbitro (spec) | Δ pp vs público |
|---|---|---|---|---|---|---|---|
| localidad <15 000 | 4645 | 4645 | 0.409076 | 0.409076 | +0.0000 | 0.409255 | -0.0179 |
| localidad >=15 000 | 8847 | 8847 | 0.331066 | 0.331066 | +0.0000 | 0.329868 | +0.1198 |
| edad 18-29 | 2924 | 2924 | 0.432063 | 0.432063 | +0.0000 | 0.432063 | -0.0000 |
| edad 30-44 | 4256 | 4256 | 0.375709 | 0.375709 | +0.0000 | 0.375709 | +0.0000 |
| edad 45-59 | 3411 | 3411 | 0.327505 | 0.327505 | +0.0000 | 0.327505 | +0.0000 |
| edad 60+ | 2901 | 2901 | 0.277212 | 0.277212 | +0.0000 | 0.277317 | -0.0105 |
| nacional | 13492 | 13492 | 0.357935 | 0.357935 | +0.0000 | 0.357153 | +0.0782 |

## Piloto 2 · TRA · ENVIPE 2025 · `escolaridad × dominio` (12 celdas)

| celda | n propio | n sellado | R propio | R sellado | Δ pp | clase | IC propio | IC sellado | clase IC | C2 propio (marg. sellados) | C2 sellado | Δ pp | clase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1xD1 | 792 | 792 | 0.392575 | 0.392575 | +0.0000 | IDÉNTICO | [0.3448, 0.4404] | [0.3458, 0.4405] | COINCIDE | 0.338220 | 0.338220 | +0.0000 | IDÉNTICO |
| S1xD2 | 871 | 871 | 0.489283 | 0.489283 | +0.0000 | IDÉNTICO | [0.4160, 0.5629] | [0.4217, 0.5569] | COINCIDE | 0.452363 | 0.452363 | +0.0000 | IDÉNTICO |
| S1xD3 | 1828 | 1828 | 0.536772 | 0.536772 | +0.0000 | IDÉNTICO | [0.4891, 0.5833] | [0.4932, 0.5788] | COINCIDE | 0.523883 | 0.523883 | +0.0000 | IDÉNTICO |
| S2xD1 | 1221 | 1221 | 0.426276 | 0.426276 | +0.0000 | IDÉNTICO | [0.3848, 0.4683] | [0.3849, 0.4678] | COINCIDE | 0.407817 | 0.407817 | +0.0000 | IDÉNTICO |
| S2xD2 | 1884 | 1884 | 0.527000 | 0.527000 | +0.0000 | IDÉNTICO | [0.4902, 0.5630] | [0.4924, 0.5604] | COINCIDE | 0.526753 | 0.526753 | +0.0000 | IDÉNTICO |
| S2xD3 | 4634 | 4634 | 0.613712 | 0.613712 | +0.0000 | IDÉNTICO | [0.5859, 0.6407] | [0.5879, 0.6391] | COINCIDE | 0.597209 | 0.597209 | +0.0000 | IDÉNTICO |
| S3xD1 | 985 | 985 | 0.376673 | 0.376673 | +0.0000 | IDÉNTICO | [0.3230, 0.4329] | [0.3243, 0.4319] | COINCIDE | 0.384566 | 0.384566 | +0.0000 | IDÉNTICO |
| S3xD2 | 2412 | 2412 | 0.509383 | 0.509383 | +0.0000 | IDÉNTICO | [0.4746, 0.5430] | [0.4757, 0.5415] | COINCIDE | 0.502475 | 0.502475 | +0.0000 | IDÉNTICO |
| S3xD3 | 8079 | 8079 | 0.572187 | 0.572187 | +0.0000 | IDÉNTICO | [0.5429, 0.5996] | [0.5434, 0.5992] | COINCIDE | 0.573619 | 0.573619 | +0.0000 | IDÉNTICO |
| S4xD1 | 769 | 769 | 0.416138 | 0.416138 | +0.0000 | IDÉNTICO | [0.3597, 0.4736] | [0.3631, 0.4685] | COINCIDE | 0.430510 | 0.430510 | +0.0000 | IDÉNTICO |
| S4xD2 | 2847 | 2847 | 0.543324 | 0.543324 | +0.0000 | IDÉNTICO | [0.5109, 0.5756] | [0.5128, 0.5740] | COINCIDE | 0.549918 | 0.549918 | +0.0000 | IDÉNTICO |
| S4xD3 | 13858 | 13858 | 0.607824 | 0.607824 | +0.0000 | IDÉNTICO | [0.5895, 0.6260] | [0.5896, 0.6255] | COINCIDE | 0.619417 | 0.619417 | +0.0000 | IDÉNTICO |

Marginales de un eje (ENVIPE 2025) — propios vs `…-G-M25-MARG-*` sellados:

| marginal | n propio | n sellado | p propio | p sellado | Δ pp | clase |
|---|---|---|---|---|---|---|
| hasta primaria | 3491 | 3491 | 0.493221 | 0.493221 | +0.0000 | IDÉNTICO |
| secundaria | 7739 | 7739 | 0.567369 | 0.567369 | +0.0000 | IDÉNTICO |
| media superior | 11476 | 11476 | 0.543368 | 0.543368 | +0.0000 | IDÉNTICO |
| superior | 17474 | 17474 | 0.590093 | 0.590093 | +0.0000 | IDÉNTICO |
| rural | 3770 | 3770 | 0.403310 | 0.403310 | +0.0000 | IDÉNTICO |
| complemento urbano | 8039 | 8039 | 0.522090 | 0.522090 | +0.0000 | IDÉNTICO |
| urbano | 28471 | 28471 | 0.592703 | 0.592703 | +0.0000 | IDÉNTICO |
| nacional | 40280 | 40280 | 0.562774 | 0.562774 | +0.0000 | IDÉNTICO |

## Piloto 3 · GOB · ENCIG 2025 · `edad × escolaridad` (16 celdas, 15 PUNTUADA)

| celda | n propio | n sellado | R propio | R sellado | Δ pp | clase | IC propio | IC sellado | clase IC | C2 propio (marg. propios, universo del cruce) | C2 sellado | Δ pp | clase | soporte sellado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 18-29|HASTA-PRIMARIA | 67 | 67 | 0.326142 | 0.326142 | +0.0000 | IDÉNTICO | [0.1896, 0.4841] | [0.1860, 0.4795] | COINCIDE | 0.484525 | 0.484525 | +0.0000 | IDÉNTICO | FUERA-DE-SOPORTE-EX-ANTE |
| 18-29|SECUNDARIA | 417 | 417 | 0.598783 | 0.598783 | +0.0000 | IDÉNTICO | [0.5218, 0.6752] | [0.5211, 0.6729] | COINCIDE | 0.656803 | 0.656803 | +0.0000 | IDÉNTICO | PUNTUADA |
| 18-29|MEDIA-SUPERIOR | 934 | 934 | 0.711304 | 0.711304 | +0.0000 | IDÉNTICO | [0.6643, 0.7548] | [0.6648, 0.7549] | COINCIDE | 0.756631 | 0.756631 | +0.0000 | IDÉNTICO | PUNTUADA |
| 18-29|SUPERIOR | 1388 | 1388 | 0.844839 | 0.844839 | +0.0000 | IDÉNTICO | [0.8131, 0.8742] | [0.8134, 0.8740] | COINCIDE | 0.864378 | 0.864378 | +0.0000 | IDÉNTICO | PUNTUADA |
| 30-44|HASTA-PRIMARIA | 286 | 286 | 0.541764 | 0.541764 | +0.0000 | IDÉNTICO | [0.4510, 0.6327] | [0.4495, 0.6316] | COINCIDE | 0.516250 | 0.516250 | +0.0000 | IDÉNTICO | PUNTUADA |
| 30-44|SECUNDARIA | 1380 | 1380 | 0.631109 | 0.631109 | +0.0000 | IDÉNTICO | [0.5939, 0.6686] | [0.5935, 0.6684] | COINCIDE | 0.684822 | 0.684822 | +0.0000 | IDÉNTICO | PUNTUADA |
| 30-44|MEDIA-SUPERIOR | 1977 | 1977 | 0.749003 | 0.749003 | +0.0000 | IDÉNTICO | [0.7179, 0.7799] | [0.7178, 0.7794] | COINCIDE | 0.779240 | 0.779240 | +0.0000 | IDÉNTICO | PUNTUADA |
| 30-44|SUPERIOR | 3365 | 3365 | 0.875950 | 0.875950 | +0.0000 | IDÉNTICO | [0.8536, 0.8957] | [0.8541, 0.8953] | COINCIDE | 0.878583 | 0.878583 | +0.0000 | IDÉNTICO | PUNTUADA |
| 45-59|HASTA-PRIMARIA | 630 | 630 | 0.414209 | 0.414209 | +0.0000 | IDÉNTICO | [0.3574, 0.4726] | [0.3566, 0.4736] | COINCIDE | 0.385596 | 0.385596 | +0.0000 | IDÉNTICO | PUNTUADA |
| 45-59|SECUNDARIA | 1529 | 1529 | 0.599980 | 0.599980 | +0.0000 | IDÉNTICO | [0.5587, 0.6412] | [0.5578, 0.6403] | COINCIDE | 0.560979 | 0.560979 | +0.0000 | IDÉNTICO | PUNTUADA |
| 45-59|MEDIA-SUPERIOR | 1646 | 1646 | 0.677690 | 0.677690 | +0.0000 | IDÉNTICO | [0.6430, 0.7121] | [0.6417, 0.7124] | COINCIDE | 0.674883 | 0.674883 | +0.0000 | IDÉNTICO | PUNTUADA |
| 45-59|SUPERIOR | 1994 | 1994 | 0.801192 | 0.801192 | +0.0000 | IDÉNTICO | [0.7737, 0.8273] | [0.7739, 0.8269] | COINCIDE | 0.809720 | 0.809720 | +0.0000 | IDÉNTICO | PUNTUADA |
| 60-96|HASTA-PRIMARIA | 1294 | 1294 | 0.342590 | 0.342590 | +0.0000 | IDÉNTICO | [0.3042, 0.3822] | [0.3032, 0.3826] | COINCIDE | 0.219770 | 0.219770 | +0.0000 | IDÉNTICO | PUNTUADA |
| 60-96|SECUNDARIA | 872 | 872 | 0.397749 | 0.397749 | +0.0000 | IDÉNTICO | [0.3448, 0.4522] | [0.3457, 0.4527] | COINCIDE | 0.364472 | 0.364472 | +0.0000 | IDÉNTICO | PUNTUADA |
| 60-96|MEDIA-SUPERIOR | 1002 | 1002 | 0.507426 | 0.507426 | +0.0000 | IDÉNTICO | [0.4590, 0.5583] | [0.4579, 0.5582] | COINCIDE | 0.482310 | 0.482310 | +0.0000 | IDÉNTICO | PUNTUADA |
| 60-96|SUPERIOR | 1307 | 1307 | 0.639806 | 0.639806 | +0.0000 | IDÉNTICO | [0.5993, 0.6798] | [0.6007, 0.6778] | COINCIDE | 0.656345 | 0.656345 | +0.0000 | IDÉNTICO | PUNTUADA |

Marginales de un eje (ENCIG 2025, universo del cruce F1-bis) — propios vs `…-MARGINAL-*` sellados:

| marginal | n propio | n sellado | p propio | p sellado | Δ pp | clase |
|---|---|---|---|---|---|---|
| 18-29 | 2806 | 2806 | 0.751812 | 0.751812 | +0.0000 | IDÉNTICO |
| 30-44 | 7008 | 7008 | 0.774735 | 0.774735 | +0.0000 | IDÉNTICO |
| 45-59 | 5799 | 5799 | 0.669153 | 0.669153 | +0.0000 | IDÉNTICO |
| 60-96 | 4475 | 4475 | 0.475822 | 0.475822 | +0.0000 | IDÉNTICO |
| HASTA-PRIMARIA | 2277 | 2277 | 0.389631 | 0.389631 | +0.0000 | IDÉNTICO |
| SECUNDARIA | 4198 | 4198 | 0.565161 | 0.565161 | +0.0000 | IDÉNTICO |
| MEDIA-SUPERIOR | 5559 | 5559 | 0.678602 | 0.678602 | +0.0000 | IDÉNTICO |
| SUPERIOR | 8054 | 8054 | 0.812325 | 0.812325 | +0.0000 | IDÉNTICO |
| TOTAL | 20088 | 20088 | 0.672905 | 0.672905 | +0.0000 | IDÉNTICO |

## Resumen

| piloto | celdas | máx |Δ| punto (pp) | clases punto | clases IC de R |
|---|---|---|---|---|
| piloto1 | 8 | 0.0000 | {'IDÉNTICO': 16} | {'COINCIDE': 8} |
| piloto2 | 12 | 0.0000 | {'IDÉNTICO': 24} | {'COINCIDE': 12} |
| piloto3 | 16 | 0.0000 | {'IDÉNTICO': 32} | {'COINCIDE': 16} |

## P4 · error del piso con los números propios (celdas PUNTUADA)

| piloto | celdas | MAE(C2 vs R) propio pp | MAE sellado pp | máx err pp | IC95(C2) propio cubre R |
|---|---|---|---|---|---|
| piloto1 | 8 | 1.467 | 1.467 | 4.375 | 7/8 |
| piloto2 | 12 | 1.568 | 1.568 | 5.436 | 11/12 |
| piloto3 | 15 | 3.411 | 3.411 | 12.282 | 8/15 |
| **total** | 35 | 2.335 (media ponderada por celdas) | — | — | 26/35 |
