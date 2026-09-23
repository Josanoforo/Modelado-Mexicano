# L0 · ADR-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01

**ACTO GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2**, 23/sep/2026. `tools/marcador_segmento.py` ahora reconoce celdas-D con prefijo `GOB.` como piloteadas (defecto real: sólo reconocía `DIN.`/`TRA.`), lo que levanta la reserva del par `edadxescolaridad` de ENCIG 2025 y cierra `NC-…3619-01`. Las 32 marginales de ENIF 2024 entran adoptadas con `ADOPTADO-CON-RESERVA-DE-ANCHO` (firma F2) y el IC calibrado de `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001`. DUELO-ENVIPE2026, DIN-LOTE-ENIF2024 (P1) y ENUT (P3) quedan diferidos — la primera por falta de celda-D que los respalde y una discrepancia de universo (24 vs. 42) sin reconciliar; la segunda por no poder verificar sin teclear cifras que el enlace real a `CALC-ENUT2019-NUCLEO-EJES-0001` ya está en la tabla de identidad.

Ver `canon/gobernanza-v1_15.md` (entrada completa) y `forense/notas/2026-09-22-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-nota.md`.
