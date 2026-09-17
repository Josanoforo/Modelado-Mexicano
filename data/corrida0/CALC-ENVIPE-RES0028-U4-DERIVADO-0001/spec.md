# CALC-ENVIPE-RES0028-U4-DERIVADO-0001

Spec sucesora fijada el 16 de septiembre de 2026 antes de ejecutar el
derivado. Transforma exclusivamente el resultado sellado de
`CALC-ENVIPE-0001`; no abre microdatos ni agrega información muestral
independiente.

## Estimando y unidad

El padre `p` es `RESULT-ENVIPE-DEN-P-C2-U4`: proporción ponderada de
**personas** de U4 (`FAC_ELE`) con al menos un delito elegible de U1 cuya razón
principal pertenece a C2 = `{01,02,06,08}`. La regla de agregación del padre
es `d_persona = max(d_delito)` sobre los delitos elegibles de la persona.

El derivado es `q = 1 - p`, también a nivel **persona U4**, escala `[0,1]`.
Por la regla `max`, `q` significa que **ningún** delito elegible de la persona
pertenece a C2. Una persona con un delito C2 y otro `{03,04,05,07}` vale
`p=1, q=0`. Por tanto, `q` no es automáticamente “confianza”, tasa por delito,
probabilidad de denunciar, categoría literal `09 Otra`, ni probabilidad de
tener al menos un delito residual.

## Transformación e incertidumbre

`q = 1-p` e `IC95(q) = [1-IC_hi(p), 1-IC_lo(p)]`. Se heredan el bootstrap de
UPM dentro de estrato, su semilla y todas las limitaciones del IC padre. En
particular, `IC-CON-ESTRATOS-DE-UPM-UNICA` sigue siendo un límite inferior de
la anchura verdadera. `p` y `q` comparten exactamente el mismo denominador:
13,023 personas, masa `FAC_ELE=14,982,594`.

La corrida rechaza referencias U1, unidad distinta de persona, población
distinta de U4, padre no numérico/no estimable, límites invertidos o valores
fuera de `[0,1]`. Un `null`, NS/NR o texto de no-estimabilidad nunca se
convierte en cero.

## Relación con RES-0028

La semántica viva del consumidor describe “ningún delito elegible de la
persona pertenece al grupo padre” y su valor legacy es `0.705687`. Por ello
este derivado U4 es el candidato documentalmente compatible. La adopción sigue
pendiente: esta corrida no edita consumidores, usos, decisiones ni snapshots.
La comparación histórica de PR #829 contra el candidato U1 permanece válida
como diagnóstico de incompatibilidad y no se reemplaza.
