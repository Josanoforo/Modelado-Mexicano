# CALC-ENCUCI-0001-COMPLEMENTO-DERIVADO-0001

Spec fijada el 24/sep/2026 por ACTO GEN2-RELEVO-MOTOR-34-1 antes de ejecutar
el derivado. Clase `iii-DERIVADO-DE-GEN2` (firma 7bf5-02, 21/sep/2026): un
solo padre, `CALC-ENCUCI-0001`, SELLADA, `cuenta_gen2=SI`, replay
`REPRODUCE · IDENTICO`. No abre microdatos ni agrega información muestral
independiente. Mismo medidor que `CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001`.

## Estimando y unidad

Padre `p = RESULT-ENCUCI-A-P-CUALQUIERA`: unión ponderada solicitud ∪ entrega
(`AP5_17=1 o AP5_18=1`) entre personas con contacto con funcionario en los
últimos 12 meses y respuesta válida (universo U-A del padre). El derivado es
`q = 1 − p` en el **mismo** universo: `AP5_17=2 y AP5_18=2`, que es lo que el
motor rotula `sin_solicitud_y_sin_entrega_encuci2020` (`clase:
DERIVADO·q=1-p(unión), mismo universo e incertidumbre`, `complemento_de:
solicitud_o_entrega_mordida_encuci2020`). Legacy: 0.873994.

El padre declara `EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-U-A`. NC-0139
(forense/no-corrido.tsv:137) dejó abierta la pregunta de denominador: sobre la
población 15+ completa la unión da 0.079958. Este derivado **no** la resuelve:
hereda el denominador U-A del padre, que es el que el motor ya consume para la
conducta primaria (RES-0005, `RESULT-ENCUCI-A-P-CUALQUIERA`, GEN2).
`q` es complemento dependiente, no evidencia independiente.

## Transformación, incertidumbre, relación con el legacy

Idénticas a `CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001`: `q = 1-p`,
`IC95(q) = [1-IC_hi(p), 1-IC_lo(p)]` en `Decimal`; método de IC heredado
(`IC-CON-ESTRATOS-DE-UPM-UNICA`, cota inferior de la anchura); rechazo por
sello, `VEREDICTO`, método, finitud o límites; `COMPATIBILIDAD-LEGACY` con
tolerancia 1e-6. El legacy es constante de comparación, no insumo.

«El primer resultado que produzca este procedimiento es el que se reporta.»
