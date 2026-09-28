# R24 · Transporte literal de la ventana del catálogo v1.2 a 767 identidades · expediente

`ACTO GEN2-C1-SUCESORES-Y-LOTE-3`, P2 · `FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-02` · 28/sep/2026.

## Firma de mesa, verbatim

`forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md`, R24 **(2)**: «Autorizo el carril de transporte: copiar la ventana literal del catálogo v1.2 a las 767 identidades, sin cambiar método ni el DISCREPA/NO-RECALCULABLE histórico. Los contratos nuevos (NIV-terminal-v1, P14_22_14 leyes, exclusión EDAD 98/99) quedan pendientes de firma por bloque; ninguno se presenta como equivalente del histórico.»

La opción (2) es la del recibo (`hoja-para-mesa-recibo-astra6-2.md` L115–122): separar el carril de transporte del de contratos nuevos.

## Ejecución, derivada por comando

`p2_tablas.py` escribe `r24-transporte-ventana-767.tsv` con un join, sin recalcular nada:

- **Identidades:** `catalogo-1-incertidumbre-spec/p3/identidades-799.tsv` (sha256 `b53ef8b7…f42d`), filas con `clase_sucesor = RESTAURACION-DE-TRANSPORTE-DOCUMENTADA`: **767**, todas distintas. Las otras 32 de las 799 (31 CAMBIO-MATERIAL-DE-ESTIMANDO-DE-DOMINIO y 1 ACLARACION-QUE-MODIFICA-INTERPRETACION, P14_22_14) no se transportan: van por contrato nuevo.
- **Ventana literal:** columna `reserva` de `canon/catalogo-del-mexicano-v1_2.tsv` (sha256 `2592df41…5d4c`), por `llave`. Se copia byte a byte. Guardia: la `reserva` de cada una de las 767 termina en `ventana=<ventana_demostrada>`; si una no, el comando PARA. Pasó 767 de 767.
- **Método y estado histórico:** `SIN-CAMBIO` en las 767. El DISCREPA/NO-RECALCULABLE histórico no se toca.

Los contenedores `-entradas-ventana-v1` de `catalogo-1-reempaqueta-ventana/` (100 + 96 + 100 + 471 = 767) son el transporte material para una sesión futura. Esta tabla es el registro por identidad que les faltaba y cita el catálogo por sha.

## Lo que no hace

No escribe el catálogo. No abre ENDIREH 2021: el acceso está firmado por `ee49-01`, pero ninguna de las 767 está en este lote, así que su lanzamiento es de `GEN2-ASTRA6-C1-LOTE-4`. No firma NIV-terminal-v1, P14_22_14 ni la exclusión EDAD 98/99.
