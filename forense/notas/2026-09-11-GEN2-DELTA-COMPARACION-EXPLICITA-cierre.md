# Cierre · ACTO GEN2-DELTA-COMPARACION-EXPLICITA

Fecha: 11/sep/2026  
Entorno: CAJA Ubuntu/WSL2  
Worktree: `/home/pc0/mm-gen2-delta-comparacion-explicita`  
Rama: `acto/gen2-delta-comparacion-explicita`  
Base observada al arrancar: `origin/main=d9c251954bce1c08abba6f47696adde9d7a2913a`  
Primera base integrada: `origin/main=d14d715339227c7de3c8c4d7ef35e0b2a14f7325`.
Base integrada final: `origin/main=d318bef1b336e6d1a56bc6d21416b5242f727449`.
Commit de implementación: `4503dc7`  
PR: #733.

## Resultado

`python3 tools/corrida0.py delta --entrada PARES.yaml` ya no devuelve
`NO-IMPLEMENTADO`. El módulo `tools/delta_comparacion.py` implementa el
contrato `GEN2-DELTA-1` y el adaptador de `tools/corrida0.py` se limita a
delegar en él.

El contrato exige pares explícitos y verificables. Una fuente YAML/JSON/TSV
se identifica por ruta, versión, tipo, SHA-256 y selector unívoco. Un RESULT
se identifica por CALC, corrida y resultado, por los hashes de spec,
resultados y sello y por el sello validado con el verificador canónico. No se
buscan nombres parecidos, versiones recientes ni filas cercanas.

La comparación separa tres decisiones:

1. comparabilidad en unidad, escala, dirección, población, evento, códigos,
   periodo y transformación;
2. representación mediante el comparador canónico de adopción;
3. materialidad sólo cuando existe un criterio sustantivo explícito y citado.

Calcula B−A y magnitud; añade puntos porcentuales para proporciones y cambio
relativo sólo cuando el contrato lo autoriza y A no es cero. Ruptura,
información insuficiente, faltante, `NO-ESTIMABLE`, selección ambigua,
resultado ausente y base cero conservan estados propios.

## Ejecución real

Entrada congelada:
`forense/ejemplos/GEN2-DELTA-COMPARACION-EXPLICITA/pares-v1_0.yaml`
(`sha256=3a26d9f27496a30347f412934c5b74294f61d205420e75780e1bb12b98c5acf6`).

Resumen: tres pares examinados, dos comparables, uno incompatible, dos deltas
y tres materialidades `NO-DETERMINABLE`.

- #647: el valor preadopción `0.045694`, congelado en la spec de
  `CALC-B-0001`, se contrasta con `RESULT-B-ENIGH-2022-P`
  (`0.04569409956405095`). B−A es `9.956405094824206e-08`, o
  `9.956405094824206e-06` pp; ambos son iguales a seis decimales. Eso no se
  interpreta como materialidad.
- ENIF crédito/app: `RESULT-ENIF-FINTECH-2021-CREDITO-CANAL-APP`
  (`0.69803002012`) frente al punto publicado 2024 (`0.575`). La comparación
  temporal documentada produce B−A `-0.12303002012000008`, equivalente a
  `-12.303002012` pp, y cambio relativo `-0.17625319337820125`. Es cambio
  descriptivo, no significancia, causalidad o superioridad.
- ENIF cuenta/app: el contrato marca incompatibilidad por población, evento y
  códigos; no calcula delta sustantivo.

Salidas reproducibles:

| archivo | SHA-256 |
|---|---|
| `delta.json` | `b9b28e4aa9c3574de64db2300dee6b64dec04e9e6c4694fa98aed83b55f59195` |
| `delta.tsv` | `8b4b0aa15af7866622d1834c4144ab5b2c5b43a76bdf19d9e86b41dee1b50e97` |
| `delta.md` | `ab40096fa00c1b112b3f3b73f939800d3901f94990b0f235a1ed2e00961a94db` |

Sin `--salida-dir`, el comando sólo lee y escribe el formato solicitado en
`stdout`. Con destino explícito publica JSON, TSV y lectura humana de forma
atómica. La guía terminal documenta ambos modos y los códigos de salida.

## Verificación

- `python3 -m unittest tests/test_delta_comparacion.py`: 11/11 OK.
- `python3 tests/test_corrida0.py`: 91/91 OK.
- `python3 -m py_compile tools/delta_comparacion.py tools/corrida0.py`: OK.
- `python3 tests/check.py --baseline`: LÍNEA BASE VERDE; 3 FAIL y 3113 WARN
  heredados, cero novedad frente a `tests/baseline.json`.
- `git diff --check`: OK.

Las pruebas dirigidas incluyen #647, comparación temporal, ruptura, base
cero, faltante, resultado ausente sin fallback, TSV ambiguo, hash discordante,
lenguaje de totales, formatos/salidas atómicas y reemplazo efectivo del stub.

## Registros y límites

`NC-0091` CIERRA porque la capacidad es utilizable y está demostrada.
`NC-0048` permanece ABIERTA: el componente mecánico B-7 quedó resuelto, pero
no existen correspondencias declaradas para afirmar nada sobre los 211 RESULT
históricos. `valor_legacy`, `delta_legacy` y `diferencias_materiales` no se
rellenan ni reinterpretan.

No cambian `milpa/`, adopciones, tiers, specs, resultados, sellos, vistas,
contadores, cron, F6 ni firmas. El contador científico es cero: se comparó
evidencia existente. ADR-487, renumerado desde el candidato 484 al integrar
PR #731 como ADR-484, PR #729 como ADR-485 y PR #736 como ADR-486,
fusionados antes.
