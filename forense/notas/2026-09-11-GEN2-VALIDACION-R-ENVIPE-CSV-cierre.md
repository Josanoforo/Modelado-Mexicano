# Cierre · GEN2-VALIDACION-R-ENVIPE-22

Fecha: 11 de septiembre de 2026. Entorno: CAJA Ubuntu/WSL2, corpus ENVIPE
compartido montado, cero llamadas nuevas a modelos y cero cambios a objetos
congelados.

El informe íntegro, protocolo previo, código y evidencia reproducible viven en
`forense/validaciones/GEN2-VALIDACION-R-ENVIPE-CSV-v1_0/`.

## Veredicto

- Punto: `VALIDADO` en 3/3 para `CIV-M-10`, `CIV-M-12` y `CIV-M-13`.
- Incertidumbre histórica: `CONCUERDA` numéricamente en 3/3.
- Aptitud inferencial de esos IC: `NO-APROBADA`.

La implementación separada reconstruye identidad, filtros, unidad DELITO,
`n`, numerador, denominador y punto. También reproduce la linealización
histórica, pero los 19/33/20 estratos singleton de `U_R` desaparecen cuando se
conservan las UPM observables de `TVivienda` con contribución cero. No están
acreditados como unidades de certeza. `TVivienda` tampoco trae el roster
explícito completo de selección, de modo que el diagnóstico no sustituye
retrospectivamente los intervalos congelados.

`NC-0096` cierra por validación formal ejecutada con veredicto completo, no por
la sola coincidencia del punto. `NC-0157` conserva la integración al contrato
común del encargo 17, cuyo PR #710 sigue abierto al corte. `NC-0158` conserva
la vía de diseño: roster completo de UPM o servicio oficial de varianza y spec
prospectiva. Ninguna adopción, uso de consumidor o firma de contador se
infiere; contador científico: cero.

Reproducción:

```bash
python3 forense/validaciones/GEN2-VALIDACION-R-ENVIPE-CSV-v1_0/valida_r_envipe.py --self-test
python3 forense/validaciones/GEN2-VALIDACION-R-ENVIPE-CSV-v1_0/valida_r_envipe.py --write
```
