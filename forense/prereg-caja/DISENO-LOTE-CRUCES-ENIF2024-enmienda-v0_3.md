# DISEÑO · LOTE DE CRUCES ENIF 2024 · enmienda v0.3 — texto verbatim de mesa

Hermana de `DISENO-LOTE-CRUCES-ENIF2024-protocolo-unico-v0_1.md` y de la
`…-enmienda-v0_2.md`. **Ninguna de las dos se edita.**

**Instrumento.** Propuesta de dirección tras el veredicto del piloto 3. **El
lanzamiento de mesa del encargo `GEN2-DIN-LOTE-ENIF2024-A` con este texto dentro es el
sello** (así lo declara el propio encargo, §2). Este acto la asienta en
`forense/firmas-pendientes.tsv` como `FIRMADA` (A.12: toda firma dada se marca con su
ADR/PR en el mismo commit).

**Texto verbatim de mesa:**

> «Lote ENIF 2024, enmienda v0.3: la estadística primaria es la diferencia de error medio entre C2 y R2 sobre las celdas puntuadas de los 5 pares, con IC95 por réplica. Vence si el IC despeja 0.5 pp; propuesta con reserva si despeja 0 pero no 0.5; nadie vence si incluye 0. El conteo de ¾ de celdas pasa a secundario, descriptivo. El COMMIT-1 incluye una simulación de potencia de esta regla sobre datos ya abiertos (pilotos 1 a 3). El veredicto del piloto 3 no se toca: sigue siendo FALSADOR DÉBIL.»

**Qué cambia respecto de la v0.1 y la v0.2.** La regla de victoria. La v0.1 §5 pedía
**dos condiciones a la vez**: ganar en ≥ ¾ de las celdas puntuadas **y** un IC95 de ΔMAE
que despeje 0.5 pp. La v0.3 hace del **ΔMAE con IC95 por réplica la estadística
primaria y única**, con tres salidas explícitas y excluyentes, y degrada el conteo de ¾
a **secundario, descriptivo**.

**Por qué, con la cifra que lo motivó.** En el piloto 3 (rama de `PR #961`) las dos
reglas se contradijeron sobre las mismas 15 celdas: por el conteo de ¾ **nadie vencía**
(3/15 victorias, 12 indecidibles, 0 derrotas), mientras que el ΔMAE de la encogida era
**1.47 pp con IC95 [0.44, 2.12]** — un intervalo que despeja 0 pero no 0.5. Con 15
celdas y 12 indecidibles, el conteo de ¾ no tiene potencia para decir nada; el ΔMAE sí.
Una regla que no puede moverse con el dato disponible no adjudica: mide el tamaño de la
muestra de celdas, no el mérito del retador.

**Las tres salidas, escritas antes de ver el dato del lote:**

| condición sobre el IC95 de ΔMAE (C2 − R2, en pp) | veredicto |
|---|---|
| el intervalo **despeja 0.5 pp** | **R2 VENCE** |
| despeja **0** pero **no 0.5** | **PROPUESTA CON RESERVA** (A-bis: un punto que satisface un umbral con un IC que no lo despeja no adjudica) |
| **incluye 0** | **NADIE VENCE** |

**Qué obliga al COMMIT-1.** Una **simulación de potencia** de esta regla sobre datos
**ya abiertos** (pilotos 1 a 3). No es opcional y no gasta reserva: los tres pilotos ya
están abiertos.

**Qué NO toca.** El veredicto del piloto 3 **sigue siendo FALSADOR DÉBIL** y no se
reescribe (E.1/E.3: una corrida sellada es evidencia histórica). Cambiar la regla hacia
adelante no re-adjudica hacia atrás.
