# `corrida0 delta` · guía terminal

`delta` compara exclusivamente parejas declaradas. No busca correspondencias
por nombre, no adopta el resultado y no modifica `milpa/`, las vistas de
`corrida0`, specs ni sellos.

## Ejecución

Lectura humana por `stdout`, sin escribir:

```bash
python3 tools/corrida0.py delta \
  --entrada forense/ejemplos/GEN2-DELTA-COMPARACION-EXPLICITA/pares-v1_0.yaml
```

JSON o TSV por `stdout`:

```bash
python3 tools/corrida0.py delta --entrada PARES.yaml --formato json
python3 tools/corrida0.py delta --entrada PARES.yaml --formato tsv
```

Los tres formatos, con destino explícito y publicación atómica:

```bash
python3 tools/corrida0.py delta \
  --entrada forense/ejemplos/GEN2-DELTA-COMPARACION-EXPLICITA/pares-v1_0.yaml \
  --salida-dir forense/ejemplos/GEN2-DELTA-COMPARACION-EXPLICITA
```

El directorio recibe `delta.json`, `delta.tsv` y `delta.md`. Sin
`--salida-dir`, el comando no escribe. Códigos: `0` petición ejecutada
(incluye una incompatibilidad científica legítima), `1` al menos una
referencia solicitada no se pudo resolver y quedó explícita en el informe,
`2` contrato inválido.

## Contrato `GEN2-DELTA-1`

Cada elemento de `pares` contiene:

- `id`, `consumidor` y un `uso` con descripción y evidencia citada por ruta y
  SHA-256;
- referencias `a` y `b`; el signo siempre es `B − A`;
- una referencia `resultado` con `calc_id`, `corrida_id`, `resultado_id` y
  hashes exactos de spec, resultados y sello, o una referencia `fuente` con
  versión, hash y selector exacto YAML/JSON/TSV;
- las ocho dimensiones de comparabilidad: unidad, escala, dirección,
  población, evento, códigos, periodo y transformación, cada una con estado y
  razón, más la evidencia del contrato;
- unidad/escala del delta y autorización explícita del cambio relativo;
- si aplica, qué lado es el RESULT preciso y qué lado es el valor publicado
  para reutilizar el comparador canónico de adopción;
- criterio de materialidad citado, o `criterio: null`.

Estados compatibles son `COINCIDE`, `DISTINTO-INTENCIONAL` y
`DERIVA-DOCUMENTADA`. `RUPTURA`/`INCOMPATIBLE` impiden calcular el delta
sustantivo; `INFORMACION-INSUFICIENTE` lo deja no determinable. Un periodo
distinto puede ser intencional sin volver comparables las demás dimensiones.

El selector TSV debe resolver exactamente una fila. Un RESULT debe aparecer
exactamente una vez en la spec y en los artefactos de su corrida sellada. Un
hash discordante, una selección ambigua o un resultado ausente nunca eligen
la fila «más cercana» o la versión «más reciente».

## Lectura de resultados

`comparabilidad`, `representacion` y `materialidad` son veredictos separados.
La tolerancia o el grano que hacen iguales dos valores publicados no son un
umbral sustantivo. Sin criterio explícito y citado, materialidad siempre sale
`NO-DETERMINABLE`.

En escala de proporción, el informe añade puntos porcentuales. El cambio
relativo sólo se calcula cuando el contrato lo permite y A no es cero. Un
faltante/`NO-ESTIMABLE`, una base cero y una ruptura conservan estado propio;
no se convierten en cero.

El ejemplo real examina tres pares: remesas ENIGH 2022 de #647, crédito/app
ENIF 2024 menos 2021 permitido por #706 y cuenta/app ENIF con ruptura. Los
resultados publicados junto a esta guía son una ejecución del mismo contrato,
no entradas numéricas GEN2 ni una declaración de coincidencia general.
