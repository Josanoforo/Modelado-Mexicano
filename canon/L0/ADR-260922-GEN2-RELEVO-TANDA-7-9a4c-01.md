# L0 · ADR-260922-GEN2-RELEVO-TANDA-7-9a4c-01

**GEN2-RELEVO-TANDA-7** (22/sep/2026). P1: `pines_mesa.py::_tiene_crudo`
(guarda (b)) deja de reconocer un manifiesto de capturas solo por el nombre
del archivo; ahora abre un input `origen: repo` en JSON y acepta cuando
enumera capturas con hash propio (regla, no excepción) — acepta el plan real
(`F5-completa-plan-v1_0.json`) y el manifiesto real (`manifiesto-capturas-
P3-v1_0.json`); `NC-...-TANDA-6-7510-01` CERRADA. P2 PARA de nuevo, con un
hallazgo NUEVO: las 18 filas de F-L ya pasan `pines_mesa.valida_pin`
(verificado por mutación), pero escribirlas y adoptarlas por el camino
mecánico (`corrida0 registro --verifica --escribe`) levanta `ParoRegistro:
USO-NO-APTO` — `CALC-L-DESDE-CAPTURAS-v1_0/spec.yaml` no declara
`dependencias_numericas` por RESULT, así que `RESULT-LDESC-TABLA-JSON`
hereda el origen `INDETERMINADO` de dos inputs GEN1 que solo alimentan OTRO
resultado del mismo CALC. Se revirtieron las 18 filas antes de cerrar para
no dejar un riesgo latente que tumbaría el `registro --verifica --escribe`
sin `--lote` para TODOS los CALC. Contador sin cambio (146).
`NC-260922-GEN2-RELEVO-TANDA-7-9a4c-01` abierta, `DECISION-DE-MESA-PENDIENTE`.

Vista completa: `python3 tools/l0_vista.py`.
