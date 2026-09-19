# BRIEF A ASTRA · 03 · `GEN2-ENCIG-CRUCES-HISTORICOS-CLI-1` — que el dato histórico elija el cruce del piloto 3

**De:** dirección (Fable), con aprobación de mesa (19/sep: «Aprobado» al careo `CAREO-PILOTO-3-direccion-2026-09-19.md`, sha256/16 `796689c4dce6f43d`, adjunto) · **Para:** Astra → Codex CLI, caja · **Base:** `origin/main = 8e455bd6` (tipo (3) para ti: re-deriva) · una sola sesión · compuerta: ninguna · carril: medición pura (perímetro del brief de carriles).

## 1 · Qué se mide y para qué
Tu diseño y el de Opus coinciden en ENCIG y difieren en el cruce: `sexo × edad` (tuyo: soporte sobrado, quizá sin interacción que encontrar) contra `edad × escolaridad` (suyo: interacción plausible, esquinas flacas). En vez de opinar, medimos **la ola anterior, que no está reservada**: en **ENCIG 2023**, los tres cruces candidatos — `sexo × edad` (8), `sexo × escolaridad` (8), `edad × escolaridad` (16). Esas cifras hacen falta de todos modos para construir S½ y Sλ.

## 2 · LA REGLA DE ELECCIÓN — escrita aquí, antes de que exista una sola cifra. Codex la ejecuta mecánicamente y la emite como `RESULT`; nadie la ajusta después
1. **Elegible:** el cruce donde **todas** sus celdas tienen `n₂₀₂₃ ≥ 200` trámites sin ponderar (regla de soporte de la casa, spec del piloto 2 §3.4). No se colapsan categorías para rescatar un cruce.
2. **Puntaje:** media sobre celdas de `|δ₂₃,ab| / EE(δ₂₃,ab)`, con `δ = logit p(a,b) − [logit p(a) + logit p(b) − logit p]`.
3. **Se elige** el elegible de mayor puntaje. Empate (diferencia < 10 % del mayor): gana el que tenga mayor concordancia de signo de δ entre 2021 y 2023 si 2021 resultó construible (§3.3); si no, el de menos celdas.
4. **Condición de no-piloto:** si en el cruce elegido **ninguna** celda tiene IC95 de δ₂₃ que excluya 0, el veredicto es `SIN-PODER-DE-FALSACION`: no hay piloto 3 en ENCIG, y eso es un resultado, no un fracaso.
Los tres cruces de **2025** siguen `RESERVADA` pase lo que pase.

## 3 · No-negociables
1. **COMMIT-1 congela spec, medidor y esta regla verbatim**, antes de abrir respuestas. «El primer resultado que produzca este procedimiento es el que se reporta.» Si necesitas una ejecución diagnóstica, se declara en la spec **antes** de correrla, con qué se mira y qué no (lección ENADID de hoy).
2. **Mismo desenlace y universo que `CALC-PISOS-ENCIG2023-EJES-0002`:** `N_TRA == 1`, válidas `P7_3 ∈ {1,2,4,5,6}`, evento `{4,5}`, unidad **trámite**, mismas bandas de edad y mismo mapa de escolaridad. **Control de coherencia obligatorio:** los marginales que salgan de sumar tus celdas deben reproducir los puntos sellados de `-0002` a tolerancia de redondeo; si no, PARA.
3. **ENCIG 2021 (payload `encig2021_csv` en `data/manifiesto.yaml`): primero por texto.** ¿El reactivo y los códigos de 2021 son los de `P7_3` 2023? Cita de cuestionario y FD. Si sí, mismos tres cruces en 2021 como segundo CALC; si no, `NO-CONSTRUIBLE` con la diferencia escrita. No se adivina por nombre de variable.
4. **Incertidumbre:** réplicas que respeten estrato, UPM, ponderador de trámite **y la agrupación de trámites por persona**; δ réplica por réplica. Por celda: n de trámites, **personas distintas**, personas con y sin evento, p, IC, δ, EE(δ), IC(δ).
5. **Un `RESULT` por celda y por cantidad**, esquema de ids de rejilla. Más los `RESULT` de la regla: elegibilidad por cruce, puntaje por cruce, cruce elegido o `SIN-PODER-DE-FALSACION`.
6. **Guardia:** el medidor declara sus insumos y un test falla si entre ellos aparece cualquier payload `encig25*` / `encig_2025*`. **No se abre ENCIG 2025. Ni para "verificar bandas".**
7. PR sin merge · `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO` · primera línea de la nota: universo, unidad, escala, clase de evidencia (a).

## 4 · Perímetro
CALC nuevos bajo `data/corrida0/` · spec(s) en `forense/prereg-caja/` · `tools/encig_cruces_historicos.py` + su test · filas propias en `corridas.tsv` y `replay-evidencia.tsv` · derivados por comando · nota · archivo del encargo y adjuntos con sha256. **No toca** gobierno, `milpa/`, marcador, `tools/corrida0.py`, `tests/check.py`, ni ningún `CALC-PISOS-*`.

## 5 · Lo que viene después en tu carril (no lanzar aún)
IC réplica por réplica de las emisiones C2 compuestas, con el módulo guardado de una sola variable de agrupación (`tools/celda_d/marginales_reproduccion.py`). Toca olas reservadas por sus marginales: va **después** de que fusione `C2-COMPUESTO-RESERVADAS-1` de nuestro lado, con encargo propio y la guardia congelada en su COMMIT-1.

## 6 · Contenido
δ es un residuo respecto de un modelo aditivo en logit, no una interacción causal ni una disposición de un grupo. En gobierno digital, `edad × escolaridad` es primero brecha de acceso y alfabetización digital por cohorte. El universo excluye a quien no hizo trámites: población con contacto institucional, más urbana y formal; se dice en la nota.
