# R26 · Contrato ENBIARE de edades/CESD-7 y receta de IC sucesora · expediente

`ACTO GEN2-C1-SUCESORES-Y-LOTE-3`, P2 · `FP-260927-GEN2-ASTRA6-C1-ENTRADAS-LOTE2-RESIDUALES-1-1653-01` · 28/sep/2026.

## Firma de mesa, verbatim

`forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md`, R26 **(2)**, la opción del recibo (`forense/analisis/recibo-astra6-3/hoja-para-mesa-recibo-astra6-3.md`): separar (a) y (b) y atarlas a un hash.

> «(a) Apruebo para un nuevo intento, con identidades sucesoras, el contrato ENBIARE de edades/CESD-7 identificado por el SHA-256 de p2/specs/enbiare-edades-propuesta.md; EDAD=98 queda fuera de tramos y de CESD-7; reconozco el cambio de denominador. (b) Apruebo la receta IC sucesora identificada por los SHA-256 de p3/entradas/residuales-p3-contrato-ic.md y residuales-p3-modulos-ic.md, solo como reproducibilidad diagnóstica y subordinada al protocolo que resulte de FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-01; no certifica cobertura del 95%. Ninguna modifica intentos previos.»

## Objetos firmados, por sha256 (verificados en el árbol y dentro de los contenedores v2)

| Parte | Archivo (`catalogo-1-entradas-residuales-lote2/`) | sha256 |
|---|---|---|
| (a) | `p2/specs/enbiare-edades-propuesta.md` | `95f614a43f0cc01ea3caaeb59b1ecc59ca4328d351a6b91b2c6fb09c604dd67d` |
| (b) | `p3/entradas/residuales-p3-contrato-ic.md` | `f09ffd47ee2bfbb80d210b4af0d2c29c1b0e7515f92ca85a051d3654ab9338bb` |
| (b) | `p3/entradas/residuales-p3-modulos-ic.md` | `d360280cd34b7067ef35af8a42091c3c03a352910faba4be33659a41d0006c98` |

El mismo byte a byte viaja dentro de `p4/enbiare-pisos-bienestar-0001-residuales-documentales-v2.tar.gz` (sha256 `fc75485a…fbfe`). (b) viaja también en los contenedores de ENCODAT (`c8b50b57…0ec0`), ENCUCI y ENIGH.

## Alcance, con lectura declarada

- **(a) solo ENBIARE.** Su propio texto dice que abarca las 12 conductas y sus ejes: excluye EDAD = 98 de tramos y de CESD-7, excluye 97, 99, blanco y códigos fuera del FD del universo adulto, y conserva 98 en TOTAL/SEXO/ESCOLARIDAD/TLOC de las conductas cuyo corte no depende de la edad. «Identidades sucesoras»: el valor que produce un intento bajo (a) es de una identidad sucesora. En las 54 llaves ENBIARE que el lote 2 dejó NO-RECALCULABLE-DESDE-SPEC, el estimando cambia por firma, así que su comparación contra el sellado es solo diagnóstica. En las 126 que ya concordaban (R28), la comparación contra el sellado es la re-comparación ciega de R28, y una diferencia se dictamina por causa con los conteos de exclusión que el contrato obliga a publicar.
- **(b) todas las cohortes que la usan.** La firma no enumera cohortes, y la hoja de P5 pedía enumerarlas. Se lee como firmada para las cuatro (ENBIARE, ENCODAT, ENCUCI, ENIGH): los cuatro contenedores traen el mismo par de archivos y la firma los nombra por hash, no por cohorte. INTERPRETACIÓN-DECLARADA (cláusula v1.0 §2). Está subordinada a R23: diagnóstica, sin margen, no adjudica.

## Estado de ejecución

Estos contratos rigen el paquete ENBIARE y el ENCODAT de P1. Al cierre de P2, P1 no ha lanzado. Ver `catalogo-1-lote3/` y la nota del acto.
