# L0 · ADR-260922-GEN2-RELEVO-TANDA-6-7510-01

**GEN2-RELEVO-TANDA-6** (22/sep/2026). P1: replay de `CALC-L-DESDE-CAPTURAS-v1_0`
se re-verifica REPRODUCE/IDENTICO y el registro derivado se pone al día
(en árbol de trabajo, sin commitear por ser DERIVADO); `NC-...-TANDA-5-f54e-01`
CERRADA. P2 PARA: los 18 pines de L (F-L) quedan bloqueados por una guarda
DISTINTA a la que TANDA-5 diagnosticó — `pines_mesa.py` guarda (b)
`RECHAZADO-SIN-INSUMO-CRUDO`, porque `CALC-L-DESDE-CAPTURAS-v1_0/spec.yaml`
no declara las 224 capturas como insumo `origen: manifiesto`. Contador sin
cambio (146). `NC-260922-GEN2-RELEVO-TANDA-6-7510-01` abierta,
`DECISION-DE-MESA-PENDIENTE`.

Vista completa: `python3 tools/l0_vista.py`.
