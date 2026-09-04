**Estado: CONSUMIDO.** Ejecutado por `ACTO SELLA-OPLUS`, 21/ago/2026, nube, Opus. Ver `canon/gobernanza-v1_15.md` `ADR-141` y `forense/notas/2026-08-21-sella-oplus-cierre.md`.

---

4 · `SELLA-OPLUS` — NUBE · Opus · gate: #3 fusionado

Firma de mesa, verbatim: «D-a». Sella el operador `⊕` del corredor `E`.

La definición, y va completa porque hoy no existe en ningún punto del corpus (verificado: las tres menciones de `⊕` son nominales, ninguna con fórmula):

`E` combina TRES corredores — `L-solo`, `L+corpus` y `M` — con peso igual y sin entrenar, tomando la MEDIANA por cuantil.

Las tres razones, todas del benchmark del 20/ago y ninguna de preferencia:

* Peso igual, no óptimo. Es el forecast combination puzzle: la combinación con pesos óptimos estimados típicamente no funciona bien y la media aritmética suele ganarle, porque cuando el peso óptimo es ½ el ruido de estimarlo introduce una penalización que hace ganar al peso fijo. La ganancia teórica del peso óptimo suele quedar tapada por el error de estimación.
* Mediana, no media. Entre varias opciones de ensamble, la elección más influyente y mejor fue usar la mediana en vez de la media, sin importar el método de ponderación. El hub europeo lo cambió en operación: los pronósticos anómalos en un ensamble de media producían incertidumbre extremadamente ancha.
* Tres, no dos. Con dos corredores la mediana es la media y la robustez se pierde. Con `L-solo`, `L+corpus` y `M` la mediana está definida y un corredor descarrilado no arrastra al ensamble.
* Sin entrenar, con razón escrita: los ensambles entrenados con selección de componentes sí superaron al de mediana con peso igual — pero requieren historial de desempeño, y este es el primer piloto. No hay qué entrenar.

T1 · `forense/prereg-duelo-v2/corredor-E-combinacion-LM.py` deja de ser propuesta: implementa la mediana por cuantil sobre los tres, con la definición y sus fuentes en el encabezado. No se ejecuta en este acto. T2 · `forense/prereg-duelo-v2/mesa-pendientes.md` §3 → RESUELTA con fecha y cita del ADR. No se borra — el propio archivo lo fija. T3 · ADR + tablero: la fila de `⊕` que `REPARA-T22` abrió pasa a `FIRMADA`. ⚠️ Verifica que esa fila existe antes de crear otra — duplicarla es el defecto de `FP-58`.

Contador: medición = 0. El corredor `E` deja de estar bloqueado. PERÍMETRO. `corredor-E-combinacion-LM.py` · `mesa-pendientes.md` (solo marcar RESUELTA) · gobernanza · tablero · hallazgos · nota · encargo.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fn -- "2026-08-21-SELLA-OPLUS.md" canon/gobernanza-v1_15.md` cita ADR-142, pero el bloque mezcla lenguaje de ejecución y de encargo pendiente (o el rótulo del ADR es compartido entre varios encargos sin desenlace individual claro) — rastro parcial, no se decide aquí. Para mesa: verificar manualmente contra ADR-142 en canon/gobernanza-v1_15.md.
