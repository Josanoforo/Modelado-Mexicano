# CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001

Spec fijada el 24/sep/2026 por ACTO GEN2-RELEVO-MOTOR-34-1 antes de ejecutar
el derivado. Clase `iii-DERIVADO-DE-GEN2` (firma 7bf5-02, 21/sep/2026): un
solo padre, `CALC-ENCIG-0001`, SELLADA, `cuenta_gen2=SI`, replay
`REPRODUCE · IDENTICO`. No abre microdatos ni agrega información muestral
independiente. Precedente de forma: `CALC-ENVIPE-RES0028-U4-DERIVADO-0001`.

## Estimando y unidad

Para cada primario `p` del padre, el derivado es `q = 1 - p` **dentro del
mismo recorte y universo del padre** (unidad trámite/usuario, ponderador y
diseño del padre, escala `[0,1]`). Los cuatro pares:

| prefijo | padre `p` | consumidor del motor (`q`) | legacy |
|---|---|---|---|
| `…-A-` | `RESULT-ENCIG-MOR-A-P-SOL1` | `tramite.mordida.discrecional:tramite_normal_encig2025` | 0.914882 |
| `…-B-PRE-SD-` | `RESULT-ENCIG-MOR-B-P-PRE-SD` | `tramite.mordida.con_registro:tramite_normal_encig2025_presencial_r2` | 0.858959 |
| `…-B-DIG-SD-` | `RESULT-ENCIG-MOR-B-P-DIG-SD` | `tramite.mordida.con_registro:tramite_normal_encig2025_digital_r2` | 0.970132 |
| `…-C-` | `RESULT-ENCIG-MOR-C-P-ADOPTA` | `tramite.gobierno_digital.util_sin_coercion:rechaza_servicio_encig2025_luz` | 0.326607 |

`q` es complemento **dependiente**: no es evidencia independiente ni tasa de
la población completa. El padre declara `VEREDICTO-EXHAUSTIVIDAD =
EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-EL-RECORTE`; NC-0108 (forense/no-corrido.tsv:109)
midió los residuos que el recorte excluye: 0.002258 (A, `P8_3_1=9`),
0.219818 (B, canal) y 0.011176 (C, `P7_3 ∈ {3,7,8,9}`). Por eso los
RESULT `COMPLEMENTO` de la propia corrida padre quedaron
`COMPLEMENTO-CON-DENOMINADOR-RECORTADO`; este derivado no los sustituye ni los
reinterpreta: declara `q` exactamente como el motor ya lo rotula
(`clase: DERIVADO·q=1-p`, `complemento_de: <primario>`).

## Transformación e incertidumbre

`q = 1-p`, `IC95(q) = [1-IC_hi(p), 1-IC_lo(p)]`, restas en `Decimal` sobre la
representación JSON publicada. Se heredan el método de IC del padre y todas
sus limitaciones (`IC-CON-ESTRATOS-DE-UPM-UNICA` sigue siendo cota inferior de
la anchura).

La corrida rechaza: sello o sidecar del padre que no cubra sus bytes,
`spec_id` distinto, `VEREDICTO` distinto de `TASA-REPORTADA`, método de IC
no estimable, punto/IC no numéricos o no finitos, y `0 ≤ IC_lo ≤ p ≤ IC_hi ≤ 1`
violado. Un `null` o texto de no-estimabilidad nunca se convierte en cero.

## Relación con el legacy

`DELTA-VS-LEGACY = q − legacy`; `COMPATIBILIDAD-LEGACY` es
`COINCIDE-AL-GRANO` si `|delta| ≤ 1e-6`. El legacy entra solo como constante
de comparación del contrato, nunca como insumo del estimador. La corrida no
edita consumidores: el escritor (`tools/escribe_relevo_consumo.py`) lo hace en
commit aparte y la adopción es el merge de mesa (E.2).

«El primer resultado que produzca este procedimiento es el que se reporta.»
