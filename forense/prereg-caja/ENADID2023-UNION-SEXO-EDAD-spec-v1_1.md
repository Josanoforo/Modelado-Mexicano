# Sucesión de contrato · ENADID 2023 · unión actual por sexo y edad

`CALC-ENADID2023-UNION-SEXO-EDAD-0002` sucede al intento no sellado 0001.
La primera ejecución del 0001 terminó antes del sello porque los tres RESULT
firmados (diferencias que pueden ser negativas) estaban declarados como
`proporcion`, tipo restringido a [0,1]. El registro rechazó correctamente
`RESULT-ENADID-USE-DIF-ESTANDAR-MH=-0.02633498480239227` y no creó sello.

El sucesor conserva sin cambio el universo, filtros, código estadístico,
semilla, 800 réplicas, regla singleton, degeneraciones, estandarización,
salidas y tolerancia congelados en
`ENADID2023-UNION-SEXO-EDAD-spec-v1_0.md`. Los únicos cambios son:

1. nuevo `calc_id` 0002 y RESULT propios `RESULT-ENADID-USE2-*`;
2. los tres contrastes firmados usan `tipo: flotante`, unidad diferencia de
   proporciones con signo en [-1,1];
3. la prueba propia apunta al medidor sucesor.

No se corrigió un valor después de verlo ni se modificó el método. Los cinco
archivos generados por el intento fallido se conservan bajo
`forense/analisis/enadid2023-union-sexo-edad-cli-2/intentos/0001-fallo-tipo-result/`;
no son resultados sellados ni se registrarán.
