# R21 · Dictámenes ENDIREH 2006/2016 y retiro de las quince llaves ENVIPE · expediente

`ACTO GEN2-C1-SUCESORES-Y-LOTE-3`, P2 · `FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-02` · 28/sep/2026.

## Firma de mesa, verbatim

`forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md`, R21 **(2)**, con el texto de `forense/analisis/hoja-firmas-21/decisiones-21.tsv`:

> «Recibo los dictámenes ENDIREH 2006 (separar MD postseparación del anual) y ENDIREH 2016 (bins NIV propios desde FD) como base de contratos sucesores, sin reescribir llaves ni sellos. El retiro de las quince llaves ENVIPE 2015 se propone al circuito de catálogo como PROPONER-SUSPENDER con sucesor por CALC nuevo; no se ejecuta por esta firma.»

La opción (2) es la del recibo (`forense/analisis/recibo-astra6-2/hoja-para-mesa-recibo-astra6-2.md` L79–86, sha256 `43fcd203…c028`). Su texto propuesto coincide palabra por palabra con la firma.

## Premisa que cae: «ENVIPE 2015»

[EJECUTADO] Las quince llaves de la fuente son `RESULT-PISOS-ENVIPE2024-V2-*` (15 de 15). Fuente: `catalogo-1-impedimentos-lote2/p2/impedimentos-lote2-p2-envipe15-retiro-sucesor.tsv`, sha256 `e252859e…3793`. La hoja de decisiones de fb50 las describe como «quince llaves 2025/persona» (`impedimentos-lote2-hoja-decisiones.md` L8). En `envipe15`, el «15» cuenta llaves y no es un año. En la fuente no hay ninguna llave ENVIPE 2015. La firma nombra su objeto por la fuente, y la fuente es única. Por eso esto se trata como un error de rótulo, no de objeto: se ejecuta sobre las quince llaves de la fuente y se declara aquí.

## Qué se ejecuta

1. **Dictamen ENDIREH 2006.** Se recibe como base de un contrato sucesor. En MD (sección VII), P7_4 se pregunta «después de separarse», no por el último año. Fuente: `impedimentos-lote2-p2-dictamen-y-hoja-firma.md` L5–13, sha256 `79c42453…487b`. El mapa `impedimentos-lote2-p2-endireh2006-llaves-anuales-revision.tsv` (sha256 `31291130…dc13`) tiene 225 celdas de `RESULT-ENDIREH2006-MOD-TABLA`: RETIRAR-MD-ANUAL 5 · SUCESOR-MC-ANUAL-SIN-POOL-MD 220. **No se reescribe ninguna llave ni sello.** El sucesor propuesto (`ENDIREH2006-PAREJA-VENTANAS-V3`) sigue sin firma de contenido: esta firma lo recibe, no lo adopta.
2. **Dictamen ENDIREH 2016.** Se reciben como base de sucesores los bins NIV propios desde el FD (`impedimentos-lote2-p2-endireh2016-bins-propuestos.json`, sha256 `ecd9e3ed…b239`): ninguna {0} · básica {1,2,3,5,8} · media superior {4,6} · superior {7,9,10,11}; 99, blanco y otros fuera del eje. Afectan a dos identidades: `endireh-pisos-2016-discriminacion-0001` y `-restantes-0001`, con sufijo sucesor `EDUCACION-CONTRATO-V2`. Es una convención nueva, no la recuperación de la histórica.
3. **Quince llaves ENVIPE.** `r21-envipe-15-llaves.tsv` (este directorio, generado por `p2_tablas.py`). Cada llave queda:
   - `RETIRADA-DEL-UNIVERSO-C1`: C1 no la valida mientras la llave histórica mezcle ola 2025/persona con un insumo 2024/delito;
   - `PROPONER-SUSPENDER` con sucesor por CALC nuevo (ola 2024, unidad delito), **propuesto** al circuito de catálogo (catálogo v1.4, `GEN2-CIERRE-SEMANAL-3`). Esta firma no lo ejecuta, y este acto tampoco toca el catálogo.

   Los consumidores por identidad (139 filas en 11 archivos, `impedimentos-lote2-p2-envipe15-consumidores.tsv`, sha256 `c5a06c0b…089e`) van por llave en la tabla.

## Lo que no hace

No adopta, no edita el catálogo ni la tabla de piso, no escribe el CALC sucesor y no firma el contenido de los sucesores 2006/2016: esas firmas (dictamen L13, L23, L27) siguen pendientes y van por bloque.
