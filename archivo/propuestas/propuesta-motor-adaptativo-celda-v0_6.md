# El motor adaptativo por celda: el piso no vencido es el estimador adjudicado
### Propuesta sin sello · v0.6 · 19/sep/2026

> | | |
> |---|---|
> | **ARCHIVO** | `propuesta-motor-adaptativo-celda-v0_6.md` |
> | **REEMPLAZA A** | `propuesta-motor-adaptativo-celda-v0_5.md`, que se conserva como historia. |
> | **CLASE** | Enmienda de contrato para los pilotos ADR-538 y ADR-542; no mide, no modifica CALC ni activa consumidores. |

## 0–2 · Sin cambio

La tesis, las colisiones de vocabulario y la identidad de celda-D son las de
v0.5 §§0–2. Los conjuntos cerrados se interpretan por `vocabulario_version`.
Las versiones 0.4 y 0.5 siguen siendo válidas.

## 3 · Contrato v0.6

Además de v0.5 §3, v0.6 incorpora cuatro correcciones.

1. **Piso adjudicado.** Si ningún retador vence a un piso bajo el criterio
   declarado, ese piso es el estimador adjudicado de la celda. Un candidato
   debe tener `id_candidato`; `champion_actual` contiene dicho id, no el id de
   una observación. Para una celda segmentada, `adjudicacion_por_celda` es un
   mapa cuya clave es el segmento definido por la spec y cuya entrada contiene
   `id_candidato`, `calc`, `resultado_puntual`, `ic95inf`, `ic95sup` y
   `decision_ref`. Las referencias son IDs, no valores editables. El piso se
   adopta por la firma y merge de mesa salvo veto; esta representación no
   equivale a consumo activo.
2. **Persistencia.** `estrategia` admite `persistencia`: el valor de la ola
   anterior para el mismo estimando, texto/semántica de reactivo, universo y
   categorías comparables. `regla_composicion` es obligatoria y declara la
   identidad temporal o el ajuste. Los nombres técnicos de variable pueden
   diferir entre olas.
3. **PISO.** `PISO` es el alias de rol de `BASELINE_INGENUO` cuando el corredor
   es un piso del marcador (persistencia o marginales sin interacción). Ambos
   nombran el mismo conjunto cerrado; no se duplican tokens.
4. **Identificación.** Este contrato no define vocabulario de identificación:
   su fuente canónica es `milpa/theta-esquema-e1-v1_0.yaml`,
   `vocabulario_identificacion`.

Un piso solo puede adjudicarse con decisión existente, rol admisible,
`estado_decidibilidad` `PUNTUADA` o `INDECIDIBLE` y veredicto
`SIN-CANDIDATO-SUPERIOR`; `INDECIDIBLE` por sí solo no adjudica. Los retadores
son credencial para emitir donde no existe piso y no sustituyen al piso donde
sí existe.

## Changelog

**v0.5 → v0.6 (19/sep/2026).** Se corrigen `champion_actual: NINGUNO` pese a
un piso no vencido, el enum ausente de persistencia (NC-0305), el alias de
rol del piso y el puente con E1. La firma histórica de mesa es 17/sep/2026:
«Un piso no vencido en su celda-D es el estimador adjudicado de esa celda y se
adopta salvo veto de mesa. Se adoptan las 20 celdas de ADR-538 y ADR-542
(piso C2) como estimadores por celda de sus reglas consumidoras. El
vocabulario celda-D v0.6 lo escribe. Los retadores son credencial para emitir
donde no hay piso, no sustitutos del piso donde lo hay.»
