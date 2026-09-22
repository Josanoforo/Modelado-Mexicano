# ENCARGO · ACTO GEN2-ENIGH2024-DUELO-COMMIT-2-3 · EL DISEÑO DEL DUELO ENIGH 2024 QUEDA ADOPTADO Y EL DUELO SE CORRE: REMESAS>0, NACIONAL, UNA APERTURA

> ENTORNO: **CAJA**. NO es NUBE. **F3:** no la sesión de `#988` (congeló).
CABECERA · SHA de redacción `bda6b60c`; una sesión, rama `acto/gen2-enigh2024-duelo-commit-2-3` · MODO **RÍGIDO** · CONTADOR: sella dos corridas; `cuenta_gen2 = SI`; no adopta; el marcador levanta la reserva de ENIGH 2024 **solo para `remesas>0` nacional** por comando. **L0 de `canon/estado-programa-v1_14.md`: si choca, toma la de `main` y re-inserta solo tu anotación; `canon/L0/` existe.**
**MODELO: Sonnet por mandato de mesa.** Procedimiento congelado o receta; latitud logística; toda duda de procedimiento se pregunta a mesa en una línea con opciones.
NO tocar (TUBERÍA): `tests/check.py`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `.github/workflows/`, `.claude/commands/`. Cierre: `tests/check.py --rapido` antes de empujar; el CI corre la suite completa. Derivados («DERIVADO — NO EDITAR») no se commitean: los re-deriva el job de main.

## 1 · OBJETIVO
`#988` construyó las series (nueve CALC sobre 2016/2018/2020), la comparabilidad 2022→2024 por texto, el origen móvil (`C-MEDIA` MAE 0.14 pp contra `C-PISO` 0.19 en tres olas retrospectivas) y el COMMIT-1 del duelo con preflight VERDE. Dejó el diseño como PROPUESTA porque la firma de adopción (`…-b7ae-02`) seguía pendiente. Este acto la asienta y corre. «Hecho»: FP b7ae-02 `FIRMADA` (viaja aquí, A.12); EMISIONES y ADJUDICACION selladas; veredicto por B-bis del diseño con el origen móvil a la vista (F7-A: el punto de 2026/2024 no adjudica solo); nota.

## 2 · FIRMAS — verbatim; el lanzamiento con este archivo es el sello
Reserva ENIGH 2024 (`#964`). **Adopción del diseño (resuelve b7ae-02):** «Se adopta el diseño `DISENO-duelo-prospectivo-ENIGH2024-v1_0.md` con el alcance que `#988` midió: estimando = proporción de hogares con remesas>0, único que pasa la regla de entrada; ventana 2016–2022 (2014 FUERA por corte de serie); contendientes mecánicos declarados juntos (persistencia/C-PISO, C-MEDIA, tendencias donde la ventana las permita), todas las variantes o ninguna; sin ejes ni cruces en esta ola (no hay piso por eje); RETROSPECTIVA-MECÁNICA del origen móvil a la vista al leer; unidad hogar; escala logit. Lo que no entra queda declarado, no rellenado.» D-22 ampliada (v2.16): preflight VERDE con main fusionado · `_valida_outputs` en cada rama terminal, celda rara incluida · nulos y NaN declarados · ningún input sobre archivo vivo. «Las corridas cuentan.»

## 3 · LO QUE DIRECCIÓN SABE (contra `bda6b60c`)
- `[EJECUTADO]` `CALC-ENIGH-DUELO-EMISIONES-0001` (COMMIT-2 previsto, preflight VERDE), `CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001` sellado; guardián `tools/enigh_duelo_guardian.py` (solo 6 columnas de `concentradohogar`; rechaza marco `reservada=True`). `[LEÍDO: nota de #988 §6]` el diseño dice «PROPUESTA, NO CONGELADA» en cabecera: con la firma de §2, la sesión escribe en la cabecera del diseño la línea de adopción con fecha y este encargo —**única edición al diseño**— y deja el resto intacto.
- `[SUPUESTO]` que existe (o el spec prevé) un CALC de adjudicación con 3a; si `#988` solo dejó EMISIONES, el 3a y la adjudicación se construyen aquí **antes** de abrir, como CALC propio con spec, sobre el molde `CALC-DUELO-ENVIPE2026-ADJUDICACION-0001`, y se congela por D-22 antes del COMMIT-2. Dilo cuál caso fue.

## 4 · YA HECHO
Series, origen móvil, comparabilidad, COMMIT-1. Sin apertura. Repítela tú.

## 5 · PIEZAS
**P0.** Firma b7ae-02 asentada; línea de adopción en el diseño; preflight VERDE con `enigh2024_nc_csv` COINCIDE; censo: nadie leyó `enigh2024*` fuera del guardián (rastro → PARO). Si aplica el `[SUPUESTO]`, construye y congela la adjudicación aquí.
**P1 · COMMIT-2.** `corrida0 run CALC-ENIGH-DUELO-EMISIONES-0001`; sella; push.
**P2 · 3a y COMMIT-3.** Sha de emisiones; `run` de adjudicación; veredicto B-bis con el origen móvil a la vista; MAE y cobertura por contendiente; una línea sobre si C-MEDIA (que ganó en retrospectiva) ganó también en prospectivo.
**P3 · Cierre.** Marcador y tablero por comando (solo `remesas>0` nacional deja de estar reservado; el resto de ENIGH 2024 sigue RESERVADA); nota: qué NO significa (remesas responden a migración, tipo de cambio y empleo en EE.UU. antes que a conducta del hogar; ENIGH sub-capta remesas informales; unidad hogar).

## 6 · LATITUD (solo logística) · 7 · PAROS
PAROS: a) leer `enigh2024*` fuera del guardián o de `corrida0 run` · b) abrir cualquier variable de ENIGH 2024 que no sea las 6 del guardián · c) elegir variante tras ver el origen móvil · d) editar spec/`.py` congelados · e) `run` no sella → no se parcha · f) sesión/entorno equivocados. Compuertas: P0 protege abrir dato. Perímetro: la línea de adopción en el diseño, FP b7ae-02, CALC del duelo (ejecución/resultados/sello; adjudicación nueva si aplica), filas propias, marcador/tablero por comando, nota, cascada. Fuera, PARA. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.
