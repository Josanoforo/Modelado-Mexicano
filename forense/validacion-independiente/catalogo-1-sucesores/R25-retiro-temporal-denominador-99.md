# R25 · Retiro temporal, denominador institucional, elegibilidad nacional 99 y sucesores · expediente

`ACTO GEN2-C1-SUCESORES-Y-LOTE-3`, P2 · `FP-260926-ASTRA6-C1-ADJUDICACION-PUNTOS-1-39de-01` · 28/sep/2026.

## Firma de mesa, verbatim

`forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md`, R25 **(1)** «en lo no cubierto por beee-02»: «En lo no cubierto por FP-…-beee-02: autorizo el retiro temporal de identidades con defecto documental, el denominador institucional, la elegibilidad nacional 99 y la ejecución de sucesores nuevos, sin adopción automática.»

Mesa eligió la opción (1), no la (2) que recomendaba el recibo (`hoja-para-mesa-recibo-astra6-2.md` L151–163). La (2) difería el denominador a la spec del sucesor.

## Qué queda «no cubierto por beee-02», derivado por comando

`p2_tablas.py` → `r25-cobertura-beee02.tsv`. Cruza por llave las 685 decisiones de `catalogo-1-adjudicacion-puntos/decisiones-por-objeto.tsv` (sha256 `6869ad95…92c`) con la tabla de beee-02 (`forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1/…tabla-result-estado-efecto.tsv`, sha256 `aaa8c4b7…30e`):

| Decisión propuesta en 39de-01 | Filas | Trato ya firmado en beee-02 |
|---|---:|---|
| PROPONER-RETIRO-TEMPORAL-Y-SUCESOR | 679 | ACOTAR 679 |
| MANTENER-AMBIGUEDAD-CON-RESERVA (institucionales #1656–#1661) | 6 | PROPONER-SUSPENDER 6 |

**Retiro temporal: 0 identidades.** Las 685 ya tienen trato en beee-02 (catálogo v1.3). El retiro autorizado aplica solo a lo no cubierto, que en llaves es un conjunto vacío, así que no se retira ninguna y las 679 siguen ACOTADAS. Esta lectura es INTERPRETACIÓN-DECLARADA (cláusula v1.0 §2): la firma no dice «sustituye ACOTAR por retiro», y cambiar un trato de producto ya firmado sería adoptar.

## Lo que sí queda autorizado, como contrato de los sucesores

- **Denominador institucional** (6 identidades 2011, #1656–#1661): el sucesor conserva la composición entre solicitantes con nombre explícito. Es la propuesta de `c1-puntos-hoja-para-mesa.md` L5 y `p4/especificacion-sucesores.md` L3. La alternativa excluyente (`p4/institucion-afectadas-alternativa.patch`) no se firma.
- **Elegibilidad nacional 99**: en los universos nacionales de los sucesores, EDAD 98/99 (edad desconocida) quedan fuera de los cortes etarios. `p4/especificacion-sucesores.md` L3 y L9.
- **Ejecución de sucesores nuevos** (`sucesor2011`, `sucesor2021`; parches en `catalogo-1-adjudicacion-puntos/p4/`): autorizada sin adopción automática. Ninguno existe hoy como CALC ni como spec en `prereg-caja/`: el comando `grep -ril "sucesor2011\|sucesor2021"` da 1 archivo, el propio `especificacion-sucesores.md`.

## Lo que no hace

Este acto no escribe ni corre los sucesores 2011/2021, porque su perímetro no incluye esos CALC. Quedan como NC con sucesor. No toca el catálogo ni cambia ACOTAR por retiro.
