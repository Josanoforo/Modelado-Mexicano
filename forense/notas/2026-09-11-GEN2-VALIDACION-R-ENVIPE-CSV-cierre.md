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
la sola coincidencia del punto. Tras fusionarse PR #710, el overlay común
`data/corrida0/validaciones-independientes.tsv` proyecta por RESULT la
validación posterior: 9 `PASA` para punto/n/denominador y 12
`CONCUERDA-NO-APROBADA` para EE/IC/CV, con referencia y SHA verificados. Las
specs y resultados sellados siguen intactos. La cascada de #712 rederiva sólo
la huella de `data/corrida0/resultados.tsv` en el snapshot de consumo del
emisor; sus emisiones permanecen idénticas y los snapshots científicos
F5/TRIADA no cambian. `NC-0159` conserva únicamente la
vía de diseño: roster completo de UPM o servicio oficial de varianza y spec
prospectiva. Ninguna adopción, uso de consumidor o firma de contador se
infiere; contador científico: cero.

Reproducción:

```bash
python3 forense/validaciones/GEN2-VALIDACION-R-ENVIPE-CSV-v1_0/valida_r_envipe.py --self-test
python3 forense/validaciones/GEN2-VALIDACION-R-ENVIPE-CSV-v1_0/valida_r_envipe.py --write
python3 tools/corrida0.py registro --escribe
python3 tools/corrida0.py status
```
