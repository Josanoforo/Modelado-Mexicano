# `CALC-R-TRA-M-02` — preregistro mecánico del árbitro R

**Acto:** `GEN2-R-COMPLETA-MARCO`, FP-370, 9/sep/2026. **Celda:** `TRA-M-02`.

Congelado antes de abrir microdato. Mide el estimando ya fijado en
`codificacion-R-v1_1.tsv`, sucesora byte-idéntica de v1.0: payload `encuci2020_bd_dbf`,
tabla `SEC_4_5`, variable `AP5_17|AP5_18`, universo `persona seleccionada (informante de 15 anios y mas, tabla SEC_4_5) con contacto en los ultimos 12 meses = alguna de AP5_16_1..AP5_16_10 == '1' (codigos del FD: 1 Si, 2 No, 9 No sabe/no responde); 21519 filas leidas y 13435 con contacto segun la proyeccion ciega (guardias: se reportan, no se ajustan). El filtro NO se ejecuta como codigo (limite declarado de arbitra.py): lo aplica el salto del cuestionario -- sin contacto AP5_17/AP5_18 van en blanco y caen FUERA por la codificacion`,
codificación `y=1 si AP5_17=='1' o AP5_18=='1'; y=0 si AP5_17=='2' y AP5_18=='2' -- COMPUESTO OR de dos variables (_PATRON_COMPUESTO_OR); resto FUERA (cae en n_codigo_no_valido, no se reclasifica): 9 = No sabe/no responde, b = blanco (salto del cuestionario) y cualquier otra combinacion; codigos verificados en el FD (AP5_17 y AP5_18: 1 Si, 2 No, 9 No sabe/no responde, b blanco)`, ponderador `FAC_SEL`, estrato
`EST_DIS` y UPM `UPM_DIS`. Ninguno de esos campos se elige en la corrida.

Salida esperada por nombre, nunca por valor: punto, EE/IC o reserva, n, masa,
exclusiones, estratos y UPM. El medidor no abre L, corpus, M, TRIADA ni R legado.
`cuenta_gen2 = SI` para este `CALC-R-TRA-M-02`; objeto explícito: la medición R de `TRA-M-02`.
