ENCARGO · ACTO MAESTRA38-A2 · RECENSO-Y-REGULARIZA-PERIMETRO-REAL — invoca /acto

SHA: 5f0f7093 · COMPUERTA: ninguna · ENTORNO: UBUNTU con corpus · MODELO: Opus. SPEC: forense/prereg-caja/S1-A2-spec-v1_0.md (sha en .sha256), íntegra. FIRMA — verbatim: transfer ChatGPT §17–§18 (archivado) + «Ya tenemos caja. Si no necesitamos mover nada más en nube pasamos a encargos en caja. Genéralos.» (5/sep). A.8: S1 existe y su sha coincide (comando pegado). forense/censo-raiz/ vacío en main → el estado del cron lo dice crontab -l + forense/adq-log/, no el tablero. Manifiesto 1 281. FP-282/288 ABIERTA. EJECUCIÓN: COMMIT-2 = §3 de S1 completo sin escribir en data/ (dos raíces, corpus.py, --escanea, tabla nominal de depósitos de mesa —incluidos 35024-0001-Data.dta, WB 6667, PDN S1/S2/S6, las 6 recetas de PAQUETE-RECETAS-5, las 2 de -6—, ENFIH-4 con sha). COMMIT-3 = regularización A/B/C con el criterio de parada de S1 (C1 sin_registro = 0 o residuo ≤ 10 en tablero); lo depositado por mesa entra por --escanea --grupo + --promueve y cierra sus filas (OBTENIDO, con el .dta cerrando D6). COMMIT-4 = ENFIH-4 sólo si COINCIDE 4/4. FP-282 → EJECUTADA con crontab -l pegado, o ABIERTA con lo que falta. Primer [CENSO] diario como control al día siguiente. PERÍMETRO: el de S1. NO toca Downloads (ni ls), tests/manifiesto.py, tools/**, milpa/**, las 133 NO_DETERMINADO restantes. FP/ADR: ADR-344 · FP-307 recibo · FP-308 residuo C (si > 0). CONTADOR: C1 sin_registro X → 0/residuo · depósitos de mesa sin registro M → 0 · enlaces COINCIDE +4 si ENFIH · medición: cero (último acto de plomería).

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-A2` (worktree `mm-maestra38-a2`, rama
`acto/maestra38-a2-recenso-y-regulariza-perimetro-real`), 4/sep/2026.
Commits: `09a57da` (A.3), `18bf2a6`+`fff33bc` (0-ter, cherry-pick + SUSTITUIDO
de V1), `1e8cad6` ([CENSO]), `63d5605` (COMMIT-2 staging), `890bc8c` (CIERRE
ADR-344/L0/registro-rotulos/FP-307/FP-308). PR: (pendiente de push, ver
más abajo tras `git push`).

COMMIT-3 (regularización) y COMMIT-4 (ENFIH-4) NO se ejecutaron: los seis
depósitos nominales de `prereg-caja-S1-A2` §5 están AUSENTE-EN-RAIZ en
ambas raíces, y la categoría C (`73`, `descargas_mx`) excede el umbral
`≤10` de la propia spec — dispara PARO de clasificación declarado por
la spec misma, no una decisión de este acto. FP-282 verificada ABIERTA.
