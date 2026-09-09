> **Insumo externo (ChatGPT/Astra) · entregado a dirección 9/sep/2026 · registrado por ACTO GEN2-REVISA-CALC conforme a A.3 y regla de mesa 4 · el texto de abajo no se edita.**
>
> **Documento histórico, anterior a PR #651; la corrección posterior vive en #651/ADR-428 — NO se usa para reabrir defectos ya corregidos.**
>
> Fuente: `REVISION-ADVERSARIAL-PR649.md` · SHA-256 re-derivado en esta sesión, comando y salida:
> ```
> $ sha256sum REVISION-ADVERSARIAL-PR649.md
> ccd2219a5522a00db60feebb81eda6353bb9b1153dd4931c2c8df2c2212139fd  REVISION-ADVERSARIAL-PR649.md
> ```
> MATCH con el sha256 esperado declarado en el encargo (`forense/encargos/2026-09-09-GEN2-REVISA-CALC.md`).

---

# Revisión adversarial del PR #649

Revisión de ChatGPT (Astra), 9 de septiembre de 2026. Entrega a dirección para valoración y registro; no constituye una firma de mesa ni un encargo despachado.

**Veredicto: la medición es reproducible; la adjudicación exige corrección.** El defecto principal ya afecta al resultado publicado: `NO-DISCRIMINA` se convierte en una explicación que los datos no demuestran. Dos pruebas adversariales descubren además ramas que adjudican incorrectamente resultados inequívocos. Hay una cuarta discrepancia entre el encargo y la condición que activa el sucesor de alcance.

## Alcance y evidencia

Revisé [PR #649](https://github.com/Josanoforo/Modelado-Mexicano/pull/649), ya fusionado el 9/sep/2026 a las 04:16:16 UTC, comparando base `9ce9774e01389be6769fec501832e475462f50b1` con cabeza `cb10eb9ef5e9089141423236800d76ee57a18815`. Merge: `be6b852e309b2991543cd7b4680b1d74d40a8c51`. Los cuatro hallazgos siguientes afectan a piezas añadidas por este PR. El medidor y la spec v1.1 coincidían también con `origin/main` obtenido durante esta revisión.

- Verifiqué los SHA-256 de los **260 insumos** declarados por `CALC-C0D-MARCADOR-v2`.
- Ejecuté directamente `medir(inputs, spec)` con sus bytes y reproduje **152 de 152 resultados exactamente**.
- Ejecuté dos escenarios sintéticos de adjudicación y una mutación de identidad, exclusivamente en memoria, sin modificar artefactos sellados.
- Contrasté encargo, specs, medidor, resultados, nota de cierre y propagación en ADR-426. No ejecuté la suite completa ni recalculé R/M desde microdatos; la reproducción prueba esta transformación, no la validez independiente de todos sus insumos.

## 1. P1 · La incertidumbre se convierte en una explicación demostrada

**Observado.** [Medidor, líneas 380–381](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/data/corrida0/CALC-C0D-MARCADOR-v2/medidor.py#L380) asigna `EXPLICADO-POR-METRICA` cuando el intervalo incluye cero. Implementa fielmente [spec v1.1, §5.2](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/forense/prereg-caja/C0D-MARCADOR-spec-v1_1.md#L150), que afirma que la diferencia es «la sombra de unas pocas celdas con error grande». Esa lectura se propaga a la nota y a [ADR-426](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/canon/gobernanza-v1_15.md#L7446).

Los resultados reproducidos son:

| Comparación | Diferencia de MAE, corpus menos solo |
|---|---:|
| Marginales, universos distintos | +7.9116 pp |
| Universo común de 13 celdas | +4.6978 pp |
| Media de diferencias pareadas | +4.6978 pp |

La igualdad de las dos últimas filas es algebraica: sobre las mismas celdas, `media(|e_corpus| − |e_solo|) = MAE_corpus − MAE_solo`. La métrica sigue siendo el error absoluto en puntos porcentuales. El pareo aporta una evaluación conjunta de la incertidumbre; no elimina la diferencia puntual. El IC95 es `[−0.8022, +11.2747]`.

**Interpretación.** Es correcto decir que la regla preregistrada no confirma una dirección. No es correcto deducir que la diferencia quedó explicada por la métrica, ni que las celdas grandes sean un artefacto por ser grandes. El intervalo también admite un empeoramiento material; no demuestra equivalencia. La concentración en tres celdas es una descripción adicional, no una explicación causal o un criterio de invalidez. Es el mismo límite inferencial que distingue falta de evidencia contra una hipótesis de evidencia a su favor, recogido por la [declaración de la ASA](https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108).

**Consecuencia.** El programa puede tratar una comparación inconclusa como un problema ya explicado. El error está tanto en la spec como en su implementación y propagación; cambiar sólo la prosa dejaría el resultado mecánico equivocado.

**Corrección mínima.** Mantener `NO-DISCRIMINA` como destino del hallazgo cuando ése es el resultado. Separar el cambio de universo —medido— de la incertidumbre —medida— y de la causa del patrón —no identificada—. No introducir una prueba de equivalencia o un umbral elegido después de mirar estos datos.

## 2. P2 · Un cambio de posición de M puede anular una primaria concluyente

**Observado.** [Medidor, líneas 378–379](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/data/corrida0/CALC-C0D-MARCADOR-v2/medidor.py#L378) compara la ordenación de los **tres corredores** y da precedencia a `EXPLICADO-POR-UNIVERSO` sobre `CORPUS-ESTORBA`.

Contraejemplo ejecutado con el medidor real: 14 celdas, R=0.20; error absoluto de solo=5 pp y corpus=6 pp. Falta solo en una celda. M tiene error de 4 pp en las 13 comunes y de 34 pp en la excluida. Actualicé también los puntos del agregado de control para que representaran el mismo escenario. Ambos controles pasan.

| Salida | Resultado reproducido |
|---|---|
| Orden marginal | `L_SOLO=5 < L_CORPUS=6 < M=6.1429` |
| Orden común | `M=4 < L_SOLO=5 < L_CORPUS=6` |
| Primaria | `+1 pp`, IC95 `[+1,+1]`, n=13; `CORPUS-ESTORBA` |
| Adjudicación | `EXPLICADO-POR-UNIVERSO` |
| Sucesor | `NO-APLICA` |

**Interpretación.** Sólo M cambia de posición. El contraste corpus–solo conserva el orden y empeora exactamente un punto en todas las parejas. El cambio de ranking de un tercero no explica ese hallazgo. La adjudicación contradice la prioridad declarada de la comparación L↔L.

**Consecuencia.** Es un defecto latente, no la rama que cayó en los datos actuales. Con insumos admisibles puede ocultar una primaria inequívoca y desactivar su sucesor.

**Corrección mínima.** Derivar la adjudicación primaria exclusivamente de L↔L en `U_LL`. Reportar el efecto de igualar universos como diagnóstico separado. Si se conserva una categoría explicativa por universo, su condición debe comprobar el contraste relevante y no puede invalidar evidencia primaria que continúa presente.

## 3. P2 · CORPUS-AYUDA no tiene una adjudicación propia

**Observado.** El [else final, líneas 384–385](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/data/corrida0/CALC-C0D-MARCADOR-v2/medidor.py#L384) también asigna `EXPLICADO-POR-METRICA`. Sin embargo, la spec §5.2 condiciona esa explicación a `NO-DISCRIMINA` y §4 declara que `CORPUS-AYUDA` refuta el hallazgo de empeoramiento.

Contraejemplo ejecutado: R=0.20 en 14 celdas; corpus=0.20, solo=0.30, M=0.22. Universos idénticos y controles conformes. Resultado: media d=−10 pp, IC95 `[−10,−10]`, `CORPUS-AYUDA`; adjudicación: `EXPLICADO-POR-METRICA`.

**Interpretación.** Hay evidencia inequívoca en dirección contraria dentro del escenario. El código la clasifica con una rama cuya condición no se cumple. No es sólo una etiqueta poco expresiva: fusiona dos desenlaces que el encargo exige distinguir.

**Consecuencia.** Defecto latente que no cambia la cifra de esta corrida, pero vuelve incompleta la promesa de tres desenlaces.

**Corrección mínima.** Hacer explícita y exhaustiva la correspondencia entre las ramas: ayuda → hallazgo de empeoramiento refutado con alcance; estorba → confirmado con alcance; no discrimina → inconcluso. Dirección determina los tokens compatibles con el árbol. Eliminar el `else` que convierte cualquier caso restante en explicación.

## 4. P2 · La condición del sucesor de alcance se estrecha respecto del encargo

**Observado.** El [encargo, P3](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/forense/encargos/2026-09-09-GEN2-C0-D-MARCADOR.md#L11) pide nombrar el sucesor de recaptura cuando las capturas sean pre-GEN2. La spec §5.3 y el [medidor, líneas 387–389](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/data/corrida0/CALC-C0D-MARCADOR-v2/medidor.py#L387) sólo lo activan ante `CONFIRMADO-CON-ALCANCE`. En esta corrida sale `NO-APLICA` y [la nota, línea 23](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/forense/notas/2026-09-09-GEN2-C0-D-MARCADOR-cierre.md#L23) afirma que el límite de alcance no muerde para esta rama.

**Interpretación.** El resultado estadístico no actualiza el corpus observado. La limitación temporal permanece tanto si el contraste ayuda como si estorba o no discrimina. No identifiqué en las piezas revisadas una autorización independiente para estrechar esa condición; queda como pregunta concreta para dirección si existe fuera de ellas.

**Consecuencia.** Hay dos lecturas en conflicto: la salida mecánica dice que no aplica sucesor y la deuda `NC-0077` sí conserva la recaptura. **La deuda no desapareció**, y eso mitiga el defecto. Pero un consumidor del resultado puede concluir que el alcance quedó resuelto cuando sólo cambió la rama estadística.

**Corrección mínima.** Mantener separadas la conclusión estadística y la necesidad de actualizar el alcance. Reutilizar `NC-0077` como referencia del sucesor de alcance, sin abrir otra deuda ni ejecutar una recaptura en este arreglo. Alinear la nota y el resultado futuro con la condición del encargo, o citar la decisión que la modifica.

## Observaciones menores y límites que no elevo a bloqueo

**13, no 14.** La nota, línea 32, afirma que M gana «sobre estas 14 celdas». Las dos secundarias declaradas y reproducidas tienen n=13. Corregir el enunciado a las 13 celdas comunes y conservar su carácter secundario; no es una falla del cómputo.

**Correspondencia no equivale a identidad de contenido.** Intercambié en memoria las capturas SOLO de CIV-M-01-01 y CIV-M-02-01: los 152 resultados siguieron idénticos y la guardia emitió `CORRESPONDE`. El código construye la llave con el nombre del input y sólo comprueba `variante`, no `id_celda` e `indice` del JSON. No encontré identidades incorrectas en las 224 capturas reales. Además, intercambiar bytes después del sellado sería detenido por los hashes del runner: esta prueba se hizo directamente sobre `medir`, no es una evasión de preflight. Es una limitación de lo que acredita esa guardia, no evidencia de contaminación de esta corrida. Si se refuerza la guardia en una sucesora, basta contrastar ambos campos existentes.

La v1 fallida quedó preservada y la v2 reparó la fuente L. Las reservas de segmentación, adopción, B incompleto y metadatos no se convierten aquí en nuevos hallazgos: ya están declaradas. Tampoco atribuyo a este PR fallos generales de CI o carencias anteriores del corpus.

## Encargo correctivo mínimo propuesto a dirección

Como el PR está fusionado, procede un acto correctivo sucesor, registrado por el circuito vigente; conservar las corridas y los sellos históricos. No hace falta rehacer la infraestructura ni recapturar datos para corregir esta adjudicación.

1. Registrar esta revisión y decidir la corrección de la tabla de adjudicación. El asunto material es qué conclusión permite la evidencia, no la reproducción de los decimales.
2. Preparar spec y medidor sucesores con ramas explícitas, sin veto de M sobre L↔L y con el sucesor de alcance separado del signo del contraste. Elegir identificadores desde el árbol del día.
3. Reejecutar sobre los mismos insumos. Las cifras de la primaria deben permanecer `+4.6978 pp`, IC95 `[−0.8022,+11.2747]`, n=13; el destino debe conservar la incertidumbre sin presentarla como explicación.
4. Validar los dos contraejemplos de esta revisión y el caso real. Son pruebas dirigidas a fallos demostrados. Conservar también la precedencia de controles inválidos y cobertura insuficiente.
5. Corregir mediante cita de sucesión la nota, la adjudicación propagada y el enunciado n=14. Reutilizar `NC-0077`. Mesa sella el acto correctivo mediante su merge.

**Texto sustantivo que sí sostiene la corrida:** «En las 13 celdas comparables, L con corpus tiene un error absoluto medio 4.70 pp mayor que L solo. El IC95 bootstrap va de −0.80 a +11.27 pp: la comparación no discrimina la dirección bajo la regla preregistrada. Igualar el universo reduce la diferencia marginal; no demuestra que el resto esté explicado por la métrica. La conclusión se limita a las capturas y al corpus observados.»
