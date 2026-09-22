**ADR-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-01**, `ACTO GEN2-ENUT-NUCLEO-CELDAS-1`, 22/sep/2026, CAJA (`sin_variable`), Opus 5.5, sin sub-agentes. El acto paró en el ARRANQUE (PARO-PREMISA) sin medir nada y mesa aceptó el PARO. Se cayeron tres premisas:
- el CALC-id reservado `CALC-ENUT2024-NUCLEO-EJES-0001` ya estaba sellado por PR #976 (el negativo del §4 salió de un `head -5` truncado);
- las celdas del marcador son 10 cruces `sexo_edad`, más la razón y una reservada: 12 filas, no «21»;
- la firma (a)(b)(c) no estaba en el árbol.

El acto asienta la firma de mesa (a)(b′)(c) sobre `FP-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-01` → FIRMADA, con la enmienda «21 → 12 filas»:
- (a) C2×2019 = CAMBIO-DE-INSTRUMENTO, en una tabla nueva `v1_1`, porque la `v1_0` es input fijado por hash de tres CALC;
- (b′) 10 `sexo_edad` NO-CONSTRUIBLE-POR-CRUCE, y la razón se enlaza sin medir (0.2379 → 0.2255, ambas selladas);
- (c) `cuenta_gen2 = SI`.

Sucesor: `GEN2-ENUT-ENLACE-MARCADOR-1` (NUBE, cero mediciones). Cero CALC, no adopta, `sin_piso` 15 → 15.
