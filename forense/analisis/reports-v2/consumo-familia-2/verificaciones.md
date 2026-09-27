# Verificaciones · corte final

EJECUTADO: `python3 tests/check.py --baseline --parallel`, código de salida 0. Árbol de corrección con origin/main `1eeb8552` incorporado; no se modifica baseline ni se reparan fallos heredados. La primera rápida detectó duplicados T02 propios; se resolvieron distinguiendo fuente y producto y retirando copias nuevas innecesarias, sin parchear CI/tests.

```text
  FAIL (3)
────────────────────────────────────────────────────────────────────────
  · T06: 2
      7 valores distintos de **Gini** en el corpus: 0.39 (1x, Confianza_y_Desconfianza_en_:165(s/f)) · 0.391 (4x, El_Clasemediero_Mexicano__Id:182(2024)) · 0.449 (1x, El_Clasemediero_Mexicano__Id:37(2016)) · 0.45 (2x, Psicología_del_Consumidor_Me:28(s/f)) · 0.56 (1x, Psicología__Conducta_y_Socie:113(s/f)) · 0.59 (1x, Confianza_y_Desconfianza_en_:165(s/f)) · 43.5 (1x, Psicología__Conducta_y_Socie:231(2023))
      12 valores distintos de **confianza interpersonal** en el corpus: 12 (4x, Confianza_y_Desconfianza_en_:221(2009)) · 15 (4x, Psicología__Conducta_y_Socie:3(2025)) · 16 (1x, Report_26__The_Contemporary_:161(s/f)) · 20 (1x, El_Mexicano_y_el_Tiempo__Est:137(2024)) · 22 (5x, Confianza_y_Desconfianza_en_:9(2018)) · 28 (1x, Behavioral_Finance_Mexicano_:17(s/f)) · 33 (2x, Confianza_y_Desconfianza_en_:295(2018)) · 34 (1x, La_arquitectura_invisible_de:43(1990)) · 5 (1x, Confianza_y_Desconfianza_en_:219(2017)) · 50 (1x, La_familia_mexicana_como_sis:109(s/f)) · 66 (1x, Confianza_y_Desconfianza_en_:205(2022)) · 70 (1x, Sanción_Social_Horizontal_en:231(s/f))
  · T08: 1
      7 reports sin mapa de evidencia — todo constructo suyo es DERIVADO, no LEÍDO: Humor_in_Mexican_Psychological_Life__2023-2026 · La_arquitectura_invisible_de_la_interacción_so · Mexican_Population_Genomics__2025-2026_Scienti · Mérito__Movilidad_Social_y_Desigualdad_en_Méxi · Non-Family_Social_Capital_in_Mexico__Cooperati · Psicología__Conducta_y_Sociedad_en_el_México_C · Psicología_del_Trabajo_en_México__Un_Mapa_Basa

════════════════════════════════════════════════════════════════════════
  3 FAIL · 230154 WARN
════════════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — sin FAIL nuevos frente a tests/baseline.json (HEAD congelado 7100cd0317132b1f4513b2efdc04058fd7ae89a2)

```

  LÍNEA BASE: VERDE — sin FAIL nuevos frente a tests/baseline.json (HEAD congelado 7100cd0317132b1f4513b2efdc04058fd7ae89a2)

EJECUTADO: productores --check REPRODUCE, verificador sucesor sin errores e índice reproducible; mutaciones materiales rechazadas. `verifica_sidecars.py`: FAIL 0, advertencia heredada sobre cabecera ENIF ajena. `git diff --check` limpio. Estos controles no equivalen a validación C1, identificación causal ni recibo independiente. Log completo local: `/tmp/astra6-c3-consumo-familia-2-baseline.log`.

WARN nuevos frente al baseline congelado se conservan como [salida cruda](warn-nuevos.txt); no adjudican y no se reparan referencias ajenas en este lote.
