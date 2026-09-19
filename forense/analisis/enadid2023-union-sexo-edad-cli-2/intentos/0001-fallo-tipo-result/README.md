# Intento 0001 no sellado

Comando: `python3 tools/corrida0.py run CALC-ENADID2023-UNION-SEXO-EDAD-0001`.

El preflight fue verde y el medidor escribió estos cinco archivos, pero el
runner rechazó el contrato antes de crear `ejecucion.json`, `resultados.json`
o sello:

```text
RUN: FALLO -- nada se sella:
  RESULT-ENADID-USE-DIF-ESTANDAR-MH: proporcion_fuera_de_rango=-0.02633498480239227
```

Causa: una diferencia de proporciones con signo fue declarada erróneamente
como `tipo: proporcion`. Los archivos se conservan como evidencia del intento,
no son resultados publicados ni se registran. El sucesor 0002 cambia sólo el
tipo registral/identidades RESULT y conserva el método estadístico.
